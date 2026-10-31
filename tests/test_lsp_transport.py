"""Protocol framing, dispatch and failure cleanup at the actual byte boundary."""

import asyncio
import json
import unittest
from dataclasses import replace
from pathlib import Path
from typing import cast

from gz_mcp_lsp.config import Config, Limits
from gz_mcp_lsp.lsp_transport import RpcClient
from gz_mcp_lsp.models import AdapterError


def frame(value):
    body = json.dumps(value, ensure_ascii=False).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


class Writer:
    """In-memory byte sink that yields during drain to expose concurrent writers."""

    def __init__(self):
        self.frames = asyncio.Queue()
        self.closed = False

    def write(self, data):
        self.frames.put_nowait(data)

    async def drain(self):
        await asyncio.sleep(0)

    def close(self):
        self.closed = True

    async def wait_closed(self):
        pass


class TransportTests(unittest.IsolatedAsyncioTestCase):
    """Exercise the client rather than matching an implementation's source text."""

    async def asyncSetUp(self):
        self.reader = asyncio.StreamReader()
        self.writer = Writer()
        self.config = Config(Path("/tmp"), Path("/usr/bin/true"))
        self.client = RpcClient(self.reader, cast(asyncio.StreamWriter, self.writer), self.config)
        self.addAsyncCleanup(self.client.close)

    async def outgoing(self):
        data = await asyncio.wait_for(self.writer.frames.get(), 1)
        header, body = data.split(b"\r\n\r\n", 1)
        self.assertEqual(int(header.split(b":")[1]), len(body))
        return json.loads(body)

    async def test_fragmented_unicode_frame(self):
        request = asyncio.create_task(self.client.request("hover", {"text": "😀"}, timeout=1))
        sent = await self.outgoing()
        self.assertEqual(sent["params"], {"text": "😀"})
        response = frame({"jsonrpc": "2.0", "id": sent["id"], "result": "😀"})
        for byte in response:
            self.reader.feed_data(bytes([byte]))
            await asyncio.sleep(0)
        self.assertEqual(await request, "😀")

    async def test_two_writers_and_out_of_order_ids(self):
        first = asyncio.create_task(self.client.request("first", {}, timeout=1))
        second = asyncio.create_task(self.client.request("second", {}, timeout=1))
        sent = [await self.outgoing(), await self.outgoing()]
        for request in reversed(sent):
            self.reader.feed_data(
                frame({"jsonrpc": "2.0", "id": request["id"], "result": request["method"]})
            )
        self.assertEqual(await first, "first")
        self.assertEqual(await second, "second")

    async def test_cancel_late_response_does_not_break_next_request(self):
        cancelled = asyncio.create_task(self.client.request("cancelled", {}, timeout=1))
        request = await self.outgoing()
        cancelled.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await cancelled
        self.assertEqual(len(self.client._pending), 0)
        notice = await self.outgoing()
        self.assertEqual(notice["method"], "$/cancelRequest")
        self.assertEqual(notice["params"], {"id": request["id"]})
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": request["id"], "result": "late"}))
        good = asyncio.create_task(self.client.request("good", {}, timeout=1))
        sent = await self.outgoing()
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": sent["id"], "result": "ok"}))
        self.assertEqual(await good, "ok")

    async def test_timeout_and_eof_fail_waiters(self):
        timed = asyncio.create_task(self.client.request("timed", {}, timeout=0.02))
        await self.outgoing()
        with self.assertRaises(AdapterError) as failure:
            await timed
        self.assertEqual(failure.exception.code, "TIMEOUT")
        await self.outgoing()  # Cancellation notification.
        pending = asyncio.create_task(self.client.request("pending", {}, timeout=1))
        await self.outgoing()
        self.reader.feed_eof()
        with self.assertRaises(AdapterError) as failure:
            await asyncio.wait_for(pending, 0.5)
        self.assertEqual(failure.exception.code, "SERVER_EXITED")
        self.assertEqual(len(self.client._pending), 0)

    async def test_invalid_or_oversized_frame_fails_pending(self):
        await self.client.close()
        for invalid in [
            b"Content-Length: -1\r\n\r\n",
            b"Other: 2\r\n\r\n{}",
            frame({"jsonrpc": "2.0", "id": True, "result": None}),
            b"Content-Length: 2\r\nContent-Length: 2\r\n\r\n{}",
            b"Content-Length: 17000000\r\n\r\n",
            b"Content-Length: 4\r\n\r\nnope",
        ]:
            with self.subTest(frame=invalid):
                reader = asyncio.StreamReader()
                writer = Writer()
                client = RpcClient(reader, cast(asyncio.StreamWriter, writer), self.config)
                task = asyncio.create_task(client.request("query", {}, timeout=1))
                await writer.frames.get()
                reader.feed_data(invalid)
                try:
                    with self.assertRaises(AdapterError) as failure:
                        await asyncio.wait_for(task, 0.5)
                    self.assertEqual(failure.exception.code, "PROTOCOL_ERROR")
                finally:
                    await client.close()

    async def test_server_request_handler_and_unknown_method(self):
        async def configuration(params):
            return [None for _ in params["items"]]

        self.client.set_handler("workspace/configuration", configuration)
        self.reader.feed_data(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": "server-1",
                    "method": "workspace/configuration",
                    "params": {"items": [{}, {}]},
                }
            )
        )
        response = await self.outgoing()
        self.assertEqual(response["result"], [None, None])
        self.reader.feed_data(frame({"jsonrpc": "2.0", "id": "server-2", "method": "unknown"}))
        response = await self.outgoing()
        self.assertEqual(response["error"]["code"], -32601)

    async def test_admission_is_bounded_by_request_deadline(self):
        await self.client.close()
        config = replace(self.config, limits=replace(Limits(), max_inflight=1))
        self.client = RpcClient(self.reader, cast(asyncio.StreamWriter, self.writer), config)
        first = asyncio.create_task(self.client.request("first", {}, timeout=1))
        await self.outgoing()
        with self.assertRaises(AdapterError) as failure:
            await self.client.request("second", {}, timeout=0.02)
        self.assertEqual(failure.exception.code, "TIMEOUT")
        self.assertTrue(self.writer.frames.empty())
        first.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await first
