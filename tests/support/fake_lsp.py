"""Independently authored subprocess peer for lifecycle fault injection."""

import json
import os
import sys
from pathlib import Path


def send(value):
    body = json.dumps(value).encode()
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode() + body)
    sys.stdout.buffer.flush()


def receive():
    length = 0
    while line := sys.stdin.buffer.readline():
        if line == b"\r\n":
            return json.loads(sys.stdin.buffer.read(length))
        if line.lower().startswith(b"content-length:"):
            length = int(line.split(b":")[1])
    return None


def main():
    Path("fake-pid").write_text(str(os.getpid()))
    mode = Path("fake-mode").read_text() if Path("fake-mode").exists() else "normal"
    while (message := receive()) is not None:
        with Path("fake-events").open("a") as stream:
            stream.write(json.dumps(message) + "\n")
        method = message.get("method")
        if method == "initialize":
            if mode == "crash":
                return
            send(
                {
                    "jsonrpc": "2.0",
                    "id": "configuration",
                    "method": "workspace/configuration",
                    "params": {"items": [{}, {}]},
                }
            )
            send(
                {
                    "jsonrpc": "2.0",
                    "id": "edit",
                    "method": "workspace/applyEdit",
                    "params": {"edit": {"changes": {}}},
                }
            )
            send(
                {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "result": {
                        "capabilities": {
                            "positionEncoding": "utf-16",
                            "textDocumentSync": {"openClose": True, "change": 2},
                            "hoverProvider": True,
                            "definitionProvider": True,
                            "referencesProvider": True,
                        }
                    },
                }
            )
        elif method == "shutdown":
            if mode != "hang-shutdown":
                send({"jsonrpc": "2.0", "id": message["id"], "result": None})
        elif method == "exit":
            return
        elif "id" in message and method:
            send({"jsonrpc": "2.0", "id": message["id"], "result": None})


if __name__ == "__main__":
    main()
