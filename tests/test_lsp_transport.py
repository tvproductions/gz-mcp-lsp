"""Exercise byte framing, response correlation and bounded request lifetimes."""

import asyncio
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from typing import cast

from gz_mcp_lsp.config import Config, Limits
from gz_mcp_lsp.models import AdapterError, Json


def frame(message: dict[str, Json]) -> bytes:
    """Encode independently from the transport under test."""
    body = json.dumps(message, ensure_ascii=False).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def unpack(data: bytes) -> dict[str, Json]:
    """Decode a captured outgoing packet for assertions."""
    header, body = data.split(b"\r\n\r\n", 1)
    assert int(header.split(b":", 1)[1]) == len(body)
    return json.loads(body)


class RecordingWriter:
    """Observe complete writes and detect overlapping drain ownership."""

    def __init__(self):
        self.sent: asyncio.Queue[bytes] = asyncio.Queue()
        self.draining = False
        self.overlap = False
        self.closed = False

    def write(self, data: bytes):
        self.sent.put_nowait(data)

    async def drain(self):
        if self.draining:
            self.overlap = True
        self.draining = True
        await asyncio.sleep(0)
        self.draining = False

    def close(self):
        self.closed = True

    async def wait_closed(self):
        pass


class TransportTests(unittest.IsolatedAsyncioTestCase):
    """Assert the actual wire contract without starting product subprocesses."""

    async def asyncSetUp(self):
        try:
            from gz_mcp_lsp.lsp_transport import RpcClient
        except ImportError as error:
            self.fail(f"Transport behavior is not implemented: {error}")
        self.client_type = RpcClient
        self.config = Config(Path.cwd(), Path(sys.executable))
        self.reader = asyncio.StreamReader()
        self.writer = RecordingWriter()
        self.client = RpcClient(self.reader, cast("asyncio.StreamWriter", self.writer), self.config)
        self.client.start()
        self.addAsyncCleanup(self.client.close)

    async def test_fragmented_unicode_frame(self):
        """Content-Length counts UTF-8 bytes across arbitrary frame fragments."""
        task = asyncio.create_task(
            self.client.request("echo", {"text": "\u00e9\U0001f600"}, timeout=1)
        )
        outgoing = unpack(await self.writer.sent.get())
        self.assertEqual(outgoing["params"], {"text": "\u00e9\U0001f600"})
        incoming = frame({"jsonrpc": "2.0", "id": outgoing["id"], "result": "\U0001f600"})
        for index in range(0, len(incoming), 3):
            self.reader.feed_data(incoming[index : index + 3])
            await asyncio.sleep(0)
        self.assertEqual(await task, "\U0001f600")

    async def test_two_writers_do_not_interleave(self):
        """Complete header/body frames and drain are owned by one writer at a time."""
        await asyncio.gather(
            self.client.notify("first", {"text": "\u00e9"}),
            self.client.notify("second", {"text": "\U0001f600"}),
        )
        messages = [unpack(await self.writer.sent.get()) for _ in range(2)]
        self.assertEqual({message["method"] for message in messages}, {"first", "second"})
        self.assertFalse(self.writer.overlap)

    async def test_out_of_order_ids(self):
        """Coalesced reverse replies are delivered only to their originating calls."""
        first = asyncio.create_task(self.client.request("first", None, timeout=1))
        second = asyncio.create_task(self.client.request("second", None, timeout=1))
        a, b = unpack(await self.writer.sent.get()), unpack(await self.writer.sent.get())
        self.reader.feed_data(
            frame({"jsonrpc": "2.0", "id": b["id"], "result": "second"})
            + frame({"jsonrpc": "2.0", "id": a["id"], "result": "first"})
        )
        self.assertEqual(await first, "first")
        self.assertEqual(await second, "second")

    async def test_cancel_late_response(self):
        """Cancellation removes a waiter and a late reply cannot corrupt a later call."""
        task = asyncio.create_task(self.client.request("hold", None, timeout=5))
        old = unpack(await self.writer.sent.get())
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        cancel = unpack(await self.writer.sent.get())
        self.assertEqual(cancel["method"], "$/cancelRequest")
        self.assertEqual(self.client.pending_count, 0)
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": old["id"], "result": "late"}))
        next_task = asyncio.create_task(self.client.request("next", None, timeout=1))
        current = unpack(await self.writer.sent.get())
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": current["id"], "result": "current"}))
        self.assertEqual(await next_task, "current")

    async def test_timeout_releases_waiter(self):
        """An unanswered call really unblocks and is not retained indefinitely."""
        with self.assertRaises(AdapterError) as caught:
            await asyncio.wait_for(self.client.request("hold", None, timeout=0.02), 1)
        self.assertEqual(caught.exception.code, "TIMEOUT")
        self.assertEqual(self.client.pending_count, 0)

    async def test_eof_fails_all_waiters(self):
        """EOF fails every pending call without waiting for their request deadlines."""
        tasks = [
            asyncio.create_task(self.client.request("hold", None, timeout=10)) for _ in range(2)
        ]
        await self.writer.sent.get()
        await self.writer.sent.get()
        self.reader.feed_eof()
        results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
        self.assertTrue(all(isinstance(value, AdapterError) for value in results))
        self.assertEqual(
            [cast("AdapterError", value).code for value in results], ["SERVER_EXITED"] * 2
        )
        self.assertEqual(self.client.pending_count, 0)

    async def test_invalid_or_oversized_frame(self):
        """Malformed/duplicate/negative/missing lengths and invalid JSON fail the session."""
        malformed = [
            b"Content-Length: -1\r\n\r\n",
            b"Content-Length: 2\r\nContent-Length: 2\r\n\r\n{}",
            b"Other: value\r\n\r\n{}",
            b"Content-Length: 999999999\r\n\r\n",
            b"Content-Length: 1\r\n\r\n{",
            frame({"jsonrpc": "2.0", "id": True, "result": None}),
            frame({"jsonrpc": "2.0", "id": 1, "result": None, "error": {}}),
            b"x" * 5000,
        ]
        for data in malformed:
            with self.subTest(data=data[:60]):
                reader, writer = asyncio.StreamReader(), RecordingWriter()
                client = self.client_type(reader, cast("asyncio.StreamWriter", writer), self.config)
                client.start()
                task = asyncio.create_task(client.request("hold", None, timeout=1))
                await writer.sent.get()
                reader.feed_data(data)
                with self.assertRaises(AdapterError) as caught:
                    await asyncio.wait_for(task, 1)
                self.assertEqual(caught.exception.code, "PROTOCOL_ERROR")
                await client.close()

    async def test_callbacks_and_unknown_requests(self):
        """Callbacks can answer server requests; unsolicited unknown methods are rejected."""

        async def configuration(params: Json) -> Json:
            return [{} for _ in cast("dict[str, list[Json]]", params)["items"]]

        self.client.set_handler("workspace/configuration", configuration)
        self.reader.feed_data(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": "config",
                    "method": "workspace/configuration",
                    "params": {"items": [{}, {}]},
                }
            )
        )
        response = unpack(await self.writer.sent.get())
        self.assertEqual(response, {"jsonrpc": "2.0", "id": "config", "result": [{}, {}]})
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": "unknown", "method": "unsafe"}))
        response = unpack(await self.writer.sent.get())
        self.assertEqual(cast("dict", response["error"])["code"], -32601)

    async def test_error_reply_is_not_empty_success(self):
        """Unsupported/error responses remain errors rather than empty semantic results."""
        task = asyncio.create_task(self.client.request("unsupported", None, timeout=1))
        outgoing = unpack(await self.writer.sent.get())
        self.reader.feed_data(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": outgoing["id"],
                    "error": {"code": -32601, "message": "unsupported"},
                }
            )
        )
        with self.assertRaises(AdapterError) as caught:
            await task
        self.assertEqual(caught.exception.code, "UNSUPPORTED")

    async def test_callback_failure_fails_pending_calls(self):
        """An unexpected callback failure cannot become an unobserved task exception."""

        async def broken(params: Json) -> Json:
            raise KeyError("invented bad callback input")

        self.client.set_handler("broken", broken)
        task = asyncio.create_task(self.client.request("hold", None, timeout=0.2))
        await self.writer.sent.get()
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": "callback", "method": "broken"}))
        with self.assertRaises(AdapterError) as caught:
            await asyncio.wait_for(task, 1)
        self.assertEqual(caught.exception.code, "PROTOCOL_ERROR")
        self.assertEqual(self.client.pending_count, 0)

    async def test_pending_admission_is_bounded(self):
        """The transport rejects extra waiters before allocating unbounded state."""
        await self.client.close()
        self.reader = asyncio.StreamReader()
        self.writer = RecordingWriter()
        self.client = self.client_type(
            self.reader,
            cast("asyncio.StreamWriter", self.writer),
            replace(self.config, limits=Limits(in_flight_reads=1)),
        )
        self.addAsyncCleanup(self.client.close)
        self.client.start()
        task = asyncio.create_task(self.client.request("hold", None, timeout=10))
        outgoing = unpack(await self.writer.sent.get())
        with self.assertRaises(AdapterError) as caught:
            await self.client.request("extra", None, timeout=1)
        self.assertEqual(caught.exception.code, "WORKSPACE_BUSY")
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": outgoing["id"], "result": None}))
        await task
