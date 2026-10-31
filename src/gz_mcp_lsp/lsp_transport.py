"""Bounded independent JSON-RPC transport over LSP byte streams."""

import asyncio
import json
from collections.abc import Awaitable, Callable

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError, Json


def reject_constant(value: str) -> None:
    """JSON-RPC cannot carry non-finite JavaScript numeric extensions."""
    raise AdapterError("PROTOCOL_ERROR", "Non-finite JSON value")


class RpcClient:
    """Own one reader, atomic frame writes and deadline-bound correlated requests."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, limits: Config):
        self.reader = reader
        self.writer = writer
        self.limits = limits.limits
        self._write_lock = asyncio.Lock()
        self._admission = asyncio.Semaphore(self.limits.max_inflight)
        self._next_id = 0
        self._pending: dict[int, asyncio.Future[Json]] = {}
        self._handlers: dict[str, Callable[[Json], Awaitable[Json]]] = {}
        self._terminal: AdapterError | None = None
        self.failure: asyncio.Future[AdapterError] = asyncio.get_running_loop().create_future()
        self._reader_task = asyncio.create_task(self._read_loop(), name="gz-lsp-reader")

    def set_handler(self, method: str, handler: Callable[[Json], Awaitable[Json]]) -> None:
        """Register supported callbacks before sending initialization requests."""
        self._handlers[method] = handler

    def _fail(self, error: AdapterError) -> None:
        """Fail all pending waiters once; never leave requests blocked after EOF."""
        if self._terminal is not None:
            return
        self._terminal = error
        if not self.failure.done():
            self.failure.set_result(error)
        for future in self._pending.values():
            if not future.done():
                future.set_exception(error)

    async def _send(self, message: dict[str, Json]) -> None:
        """Write one complete frame under one serialized, deadline-bound drain."""
        if self._terminal is not None:
            raise self._terminal
        try:
            body = json.dumps(message, ensure_ascii=False, allow_nan=False).encode("utf-8")
        except (TypeError, ValueError, UnicodeError) as error:
            raise AdapterError("INVALID_INPUT", "Request is not valid JSON") from error
        if len(body) > self.limits.max_frame_bytes:
            raise AdapterError("LIMIT_EXCEEDED", "Outgoing LSP frame is too large")
        data = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body
        try:
            async with asyncio.timeout(self.limits.request_seconds), self._write_lock:
                if self._terminal is not None:
                    raise self._terminal
                self.writer.write(data)
                await self.writer.drain()
        except (OSError, ConnectionError) as error:
            failure = AdapterError("SERVER_EXITED", "Language-server stream is closed")
            self._fail(failure)
            raise failure from error
        except TimeoutError as error:
            raise AdapterError("TIMEOUT", "Language-server write timed out", True) from error

    async def notify(self, method: str, params: Json) -> None:
        """Send an LSP notification without creating a response waiter."""
        await self._send({"jsonrpc": "2.0", "method": method, "params": params})

    async def _cancel_notice(self, request_id: int) -> None:
        """Best-effort bounded cancellation; connection loss must not delay the caller."""
        try:
            async with asyncio.timeout(0.1):
                await self.notify("$/cancelRequest", {"id": request_id})
        except AdapterError, TimeoutError, asyncio.CancelledError:
            pass

    async def request(self, method: str, params: Json, *, timeout: float) -> Json:
        """Include admission, writing and response time in one operation deadline."""
        request_id: int | None = None
        future: asyncio.Future[Json] | None = None
        try:
            async with asyncio.timeout(timeout), self._admission:
                if self._terminal is not None:
                    raise self._terminal
                self._next_id += 1
                request_id = self._next_id
                future = asyncio.get_running_loop().create_future()
                self._pending[request_id] = future
                await self._send(
                    {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
                )
                return await future
        except TimeoutError as error:
            if request_id is not None:
                await self._cancel_notice(request_id)
            raise AdapterError("TIMEOUT", "Language-server request timed out", True) from error
        except asyncio.CancelledError:
            if request_id is not None:
                await self._cancel_notice(request_id)
            raise
        finally:
            if request_id is not None:
                self._pending.pop(request_id, None)
            if future is not None:
                if not future.done():
                    future.cancel()
                elif not future.cancelled():
                    future.exception()  # Retrieve a stream failure even if send failed first.

    async def _read_message(self) -> dict:
        """Read bounded CRLF headers followed by exactly Content-Length body bytes."""
        length = None
        consumed = 0
        while True:
            line = await self.reader.readline()
            if not line:
                raise AdapterError("SERVER_EXITED", "Language-server stream ended")
            consumed += len(line)
            if consumed > self.limits.max_header_bytes or not line.endswith(b"\r\n"):
                raise AdapterError("PROTOCOL_ERROR", "Invalid or oversized LSP headers")
            if line == b"\r\n":
                break
            name, separator, value = line[:-2].partition(b":")
            if not separator:
                raise AdapterError("PROTOCOL_ERROR", "Malformed LSP header")
            if name.lower() == b"content-length":
                value = value.strip()
                if length is not None or not value.isdigit():
                    raise AdapterError("PROTOCOL_ERROR", "Invalid duplicate or noninteger length")
                length = int(value)
        if length is None or not 0 < length <= self.limits.max_frame_bytes:
            raise AdapterError("PROTOCOL_ERROR", "Invalid or oversized LSP body length")
        body = await self.reader.readexactly(length)
        message = json.loads(body.decode("utf-8"), parse_constant=reject_constant)
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
            raise AdapterError("PROTOCOL_ERROR", "Invalid JSON-RPC envelope")
        return message

    async def _dispatch(self, message: dict) -> None:
        """Dispatch callbacks/notifications separately from responses to our integer IDs."""
        if "method" in message:
            method = message["method"]
            if not isinstance(method, str) or "result" in message or "error" in message:
                raise AdapterError("PROTOCOL_ERROR", "Invalid server request")
            if "id" not in message:
                return  # No diagnostic/logging cache is inferred from notifications.
            request_id = message["id"]
            if type(request_id) not in (str, int):
                raise AdapterError("PROTOCOL_ERROR", "Invalid server request ID")
            handler = self._handlers.get(method)
            response: dict[str, Json] = {"jsonrpc": "2.0", "id": request_id}
            if handler is None:
                response["error"] = {"code": -32601, "message": "Method not found"}
            else:
                try:
                    async with asyncio.timeout(self.limits.request_seconds):
                        response["result"] = await handler(message.get("params"))
                except Exception:
                    response["error"] = {"code": -32603, "message": "Client callback failed"}
            await self._send(response)
            return
        request_id = message.get("id")
        if type(request_id) is not int or ("result" in message) == ("error" in message):
            raise AdapterError("PROTOCOL_ERROR", "Invalid JSON-RPC response")
        future = self._pending.get(request_id)
        if future is None or future.done():
            return  # Late/unknown responses must not create state or resurrect cancelled work.
        if "error" in message:
            error = message["error"]
            if not isinstance(error, dict) or type(error.get("code")) is not int:
                raise AdapterError("PROTOCOL_ERROR", "Invalid JSON-RPC error")
            future.set_exception(
                AdapterError(
                    "PROTOCOL_ERROR",
                    "Language-server request failed",
                    details={"lsp_code": error["code"]},
                )
            )
        else:
            future.set_result(message["result"])

    async def _read_loop(self) -> None:
        """Retain terminal failure as data and unblock every outstanding operation."""
        try:
            while self._terminal is None:
                await self._dispatch(await self._read_message())
        except asyncio.CancelledError:
            return
        except asyncio.IncompleteReadError:
            self._fail(AdapterError("SERVER_EXITED", "Language-server stream ended mid-frame"))
        except AdapterError as error:
            self._fail(error)
        except OSError, ValueError, UnicodeError, RecursionError:
            self._fail(AdapterError("PROTOCOL_ERROR", "Invalid language-server byte stream"))

    async def close(self) -> None:
        """Idempotently stop the reader, fail waiters and close the owned writer."""
        self._fail(AdapterError("SERVER_EXITED", "Language-server transport closed"))
        self._reader_task.cancel()
        await asyncio.gather(self._reader_task, return_exceptions=True)
        self.writer.close()
        try:
            async with asyncio.timeout(self.limits.escalation_seconds):
                await self.writer.wait_closed()
        except OSError, TimeoutError:
            pass
