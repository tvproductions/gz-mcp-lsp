"""Bounded independent LSP JSON-RPC byte transport."""

import asyncio
import json
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import cast

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.models import AdapterError, Json

type Handler = Callable[[Json], Awaitable[Json]]


def _protocol(message: str) -> AdapterError:
    return AdapterError("PROTOCOL_ERROR", message)


def _object(pairs: list[tuple[str, Json]]) -> dict[str, Json]:
    result: dict[str, Json] = {}
    for key, value in pairs:
        if key in result:
            raise _protocol("Duplicate JSON-RPC field")
        result[key] = value
    return result


def _constant(value: str) -> Json:
    raise _protocol("Nonfinite JSON-RPC value")


def _message(data: bytes) -> dict[str, Json]:
    try:
        value = json.loads(
            data.decode("utf-8"), object_pairs_hook=_object, parse_constant=_constant
        )
    except (ValueError, UnicodeError, RecursionError) as error:
        raise _protocol("Invalid JSON-RPC JSON") from error
    if not isinstance(value, dict) or value.get("jsonrpc") != "2.0":
        raise _protocol("Invalid JSON-RPC envelope")
    return cast("dict[str, Json]", value)


def _response_error(value: Json) -> AdapterError:
    if not isinstance(value, dict):
        raise _protocol("Invalid JSON-RPC error")
    code, message = value.get("code"), value.get("message")
    if type(code) is not int or not isinstance(message, str):
        raise _protocol("Invalid JSON-RPC error fields")
    domain = "UNSUPPORTED" if code == -32601 else "PROTOCOL_ERROR"
    return AdapterError(domain, "Language server rejected the request", details={"lsp_code": code})


class RpcClient:
    """Correlate requests on a single reader and serialize complete outgoing frames."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, limits: Config):
        self.reader = reader
        self.writer = writer
        self.config = limits
        self._write_lock = asyncio.Lock()
        self._pending: dict[int, asyncio.Future[Json]] = {}
        self._handlers: dict[str, Handler] = {}
        self._callbacks: set[asyncio.Task[None]] = set()
        self._reader_task: asyncio.Task[None] | None = None
        self._error: AdapterError | None = None
        self._failed = asyncio.Event()
        self._next_id = 0
        self._closed = False

    @property
    def pending_count(self) -> int:
        """Expose a bounded-state observation for transport tests."""
        return len(self._pending)

    def start(self) -> None:
        """Start once under the session's lifecycle ownership."""
        if self._reader_task is not None or self._closed:
            raise AdapterError("SERVER_EXITED", "Transport has already started or closed")
        self._reader_task = asyncio.create_task(self._read_loop())

    def set_handler(self, method: str, handler: Handler) -> None:
        """Register callbacks before the session sends initialize."""
        self._handlers[method] = handler

    def fail(self, code: str, message: str) -> None:
        """Invalidate admission and every waiter, including generation-stale sessions."""
        if self._error is None:
            self._error = AdapterError(code, message)
        for future in self._pending.values():
            if not future.done():
                future.set_exception(AdapterError(self._error.code, self._error.message))
        self._pending.clear()
        self._failed.set()

    async def wait_failure(self) -> AdapterError:
        """Allow the session to supervise wire failure even when no request is active."""
        await self._failed.wait()
        assert self._error is not None
        return self._error

    def _check(self) -> None:
        if self._error is not None:
            raise AdapterError(self._error.code, self._error.message)
        if self._closed or self._reader_task is None:
            raise AdapterError("SERVER_EXITED", "Transport is not running")

    async def request(self, method: str, params: Json, *, timeout: float) -> Json:
        """Wait no longer than the call deadline and remove every completed waiter."""
        self._check()
        if len(self._pending) >= self.config.limits.in_flight_reads:
            raise AdapterError("WORKSPACE_BUSY", "Transport request capacity is exhausted", True)
        self._next_id += 1
        identifier = self._next_id
        future: asyncio.Future[Json] = asyncio.get_running_loop().create_future()
        self._pending[identifier] = future
        try:
            async with asyncio.timeout(timeout):
                await self._send(
                    {"jsonrpc": "2.0", "id": identifier, "method": method, "params": params}
                )
                return await future
        except TimeoutError as error:
            await self._cancel(identifier)
            raise AdapterError("TIMEOUT", "Language-server request timed out", True) from error
        except asyncio.CancelledError:
            await self._cancel(identifier)
            raise
        finally:
            self._pending.pop(identifier, None)
            if future.done() and not future.cancelled():
                future.exception()

    async def notify(self, method: str, params: Json) -> None:
        """Send a notification under the same frame lock and a bounded wait."""
        self._check()
        try:
            async with asyncio.timeout(self.config.request_timeout_seconds):
                await self._send({"jsonrpc": "2.0", "method": method, "params": params})
        except TimeoutError as error:
            raise AdapterError("TIMEOUT", "Language-server notification timed out") from error

    async def _cancel(self, identifier: int) -> None:
        self._pending.pop(identifier, None)
        with suppress(AdapterError, OSError, TimeoutError):
            async with asyncio.timeout(0.1):
                await self._send(
                    {"jsonrpc": "2.0", "method": "$/cancelRequest", "params": {"id": identifier}}
                )

    async def _send(self, message: dict[str, Json]) -> None:
        try:
            body = json.dumps(message, ensure_ascii=False, allow_nan=False).encode("utf-8")
        except (ValueError, UnicodeError, RecursionError, TypeError) as error:
            raise AdapterError("INVALID_INPUT", "Outgoing message is not bounded JSON") from error
        if len(body) > self.config.limits.frame_bytes:
            raise AdapterError("LIMIT_EXCEEDED", "Outgoing LSP frame exceeds its byte limit")
        packet = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body
        async with self._write_lock:
            self._check()
            try:
                self.writer.write(packet)
                await self.writer.drain()
            except (OSError, RuntimeError) as error:
                self.fail("SERVER_EXITED", "Language-server output pipe failed")
                raise AdapterError("SERVER_EXITED", "Language-server output pipe failed") from error

    async def _frame(self) -> bytes:
        header = bytearray()
        while not header.endswith(b"\r\n\r\n"):
            value = await self.reader.readexactly(1)
            header.extend(value)
            if len(header) > self.config.limits.header_bytes:
                raise _protocol("LSP header exceeds its byte limit")
        length = _content_length(bytes(header))
        if length > self.config.limits.frame_bytes:
            raise _protocol("Incoming LSP frame exceeds its byte limit")
        return await self.reader.readexactly(length)

    async def _read_loop(self) -> None:
        try:
            while self._error is None:
                self._dispatch(_message(await self._frame()))
        except asyncio.CancelledError:
            raise
        except asyncio.IncompleteReadError:
            self.fail("SERVER_EXITED", "Language-server stream ended")
        except AdapterError as error:
            self.fail(error.code, error.message)
        except OSError, ValueError, RuntimeError:
            self.fail("PROTOCOL_ERROR", "Language-server stream failed")

    def _dispatch(self, message: dict[str, Json]) -> None:
        if "method" in message:
            self._dispatch_callback(message)
            return
        identifier = message.get("id")
        if type(identifier) not in (int, str):
            raise _protocol("Invalid JSON-RPC response ID")
        if ("result" in message) == ("error" in message):
            raise _protocol("A response needs exactly one result or error")
        error = _response_error(message["error"]) if "error" in message else None
        future = self._pending.pop(cast("int", identifier), None)
        if future is None or future.done():
            return
        if error is not None:
            future.set_exception(error)
        else:
            future.set_result(message["result"])

    def _dispatch_callback(self, message: dict[str, Json]) -> None:
        method = message["method"]
        if not isinstance(method, str) or "result" in message or "error" in message:
            raise _protocol("Invalid server request or notification")
        if "id" in message and type(message["id"]) not in (int, str):
            raise _protocol("Invalid server request ID")
        if method not in self._handlers and "id" not in message:
            return
        if len(self._callbacks) >= self.config.limits.in_flight_reads:
            raise AdapterError("LIMIT_EXCEEDED", "Server callback capacity exhausted")
        task = asyncio.create_task(self._callback(message))
        self._callbacks.add(task)
        task.add_done_callback(self._callbacks.discard)

    async def _callback(self, message: dict[str, Json]) -> None:
        identifier = message.get("id")
        method = cast("str", message["method"])
        try:
            handler = self._handlers.get(method)
            if handler is None:
                result: dict[str, Json] = {
                    "jsonrpc": "2.0",
                    "id": identifier,
                    "error": {"code": -32601, "message": "Method not supported"},
                }
            else:
                value = await handler(message.get("params"))
                result = {"jsonrpc": "2.0", "id": identifier, "result": value}
            if "id" in message:
                async with asyncio.timeout(self.config.request_timeout_seconds):
                    await self._send(result)
        except asyncio.CancelledError:
            raise
        except Exception:
            self.fail("PROTOCOL_ERROR", "Language-server callback failed")

    async def close(self) -> None:
        """Idempotently close pipe tasks; the session still owns child reaping."""
        if self._closed:
            return
        self._closed = True
        self.fail("SERVER_EXITED", "Transport closed")
        tasks = list(self._callbacks)
        if self._reader_task is not None:
            tasks.append(self._reader_task)
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self.writer.close()
        with suppress(OSError, RuntimeError, TimeoutError):
            async with asyncio.timeout(self.config.shutdown_timeout_seconds):
                await self.writer.wait_closed()


def _content_length(header: bytes) -> int:
    try:
        lines = header.decode("ascii").split("\r\n")[:-2]
    except UnicodeError as error:
        raise _protocol("Non-ASCII LSP header") from error
    values = []
    for line in lines:
        name, separator, value = line.partition(":")
        if not separator:
            raise _protocol("Malformed LSP header")
        if name.strip().lower() == "content-length":
            values.append(value.strip())
    if len(values) != 1 or not values[0].isascii() or not values[0].isdigit():
        raise _protocol("Exactly one nonnegative Content-Length is required")
    try:
        return int(values[0])
    except ValueError as error:
        raise _protocol("Invalid Content-Length") from error
