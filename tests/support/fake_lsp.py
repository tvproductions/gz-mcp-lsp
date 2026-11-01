"""Invented deterministic LSP peer for adapter lifecycle and failure tests."""

import json
import sys


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
    """Echo requests; lifecycle modes are added only with their owning tests."""
    while (message := read()) is not None:
        if message.get("method") == "exit":
            return
        if "method" in message and "id" in message:
            send({"jsonrpc": "2.0", "id": message["id"], "result": message.get("params")})


if __name__ == "__main__":
    main()
