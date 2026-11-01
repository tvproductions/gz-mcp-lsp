"""Invented deterministic LSP peer for adapter lifecycle and failure tests."""

import json
import sys
import time
from pathlib import Path


def read():
    """Read one synthetic Content-Length frame from stdin."""
    length = None
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line == b"\r\n":
            break
        name, _, value = line.decode("ascii").partition(":")
        if name.lower() == "content-length":
            length = int(value)
    return json.loads(sys.stdin.buffer.read(length)) if length is not None else None


def send(message):
    """Write a complete Unicode-capable frame."""
    body = json.dumps(message, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
    sys.stdout.buffer.flush()


def main():
    """Run explicitly selected synthetic behaviors; never used by product settings."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "normal"
    record = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    initialize_id = None

    def log(message):
        if record is not None:
            with record.open("a", encoding="utf-8") as output:
                output.write(json.dumps(message) + "\n")

    def initialized(identifier):
        send(
            {
                "jsonrpc": "2.0",
                "id": identifier,
                "result": {
                    "capabilities": {
                        "positionEncoding": "utf-8" if mode == "bad-encoding" else "utf-16",
                        "textDocumentSync": {"openClose": True, "change": 1},
                    }
                },
            }
        )

    while (message := read()) is not None:
        method = message.get("method")
        if method:
            log({"method": method})
        if method == "exit":
            return
        if message.get("id") == "configuration" and "method" not in message:
            log({"reply": "configuration", "result": message.get("result")})
            send(
                {
                    "jsonrpc": "2.0",
                    "id": "apply-edit",
                    "method": "workspace/applyEdit",
                    "params": {"edit": {"changes": {}}},
                }
            )
            continue
        if message.get("id") == "apply-edit" and "method" not in message:
            log({"reply": "apply-edit", "result": message.get("result")})
            initialized(initialize_id)
            continue
        if method == "initialize":
            if mode == "exit-initialize":
                raise SystemExit(7)
            if mode == "hang-initialize":
                continue
            if mode == "stderr-flood":
                sys.stderr.buffer.write(b"x" * 1024 * 1024)
                sys.stderr.buffer.flush()
            if mode == "early-requests":
                initialize_id = message["id"]
                send(
                    {
                        "jsonrpc": "2.0",
                        "id": "configuration",
                        "method": "workspace/configuration",
                        "params": {"items": [{}, {}]},
                    }
                )
            else:
                initialized(message["id"])
            continue
        if method == "hold":
            continue
        if method == "malformed":
            sys.stdout.buffer.write(b"Content-Length: 1\r\n\r\n{")
            sys.stdout.buffer.flush()
            continue
        if method == "shutdown" and mode == "hang-shutdown":
            continue
        if method is not None and "id" in message:
            send({"jsonrpc": "2.0", "id": message["id"], "result": message.get("params")})
    if mode == "hang-eof":
        time.sleep(30)  # Deliberately unresponsive child; the owning test must kill/reap it.


if __name__ == "__main__":
    main()
