"""Launch the provisioned stdio adapter from one explicit JSON settings file."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from gz_mcp_lsp.config import load_config
from gz_mcp_lsp.mcp_api import create_server
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session


def main(argv: Sequence[str] | None = None) -> int:
    """Parse native CLI arguments before claiming the MCP wire."""
    parser = argparse.ArgumentParser(prog="gz-mcp-lsp")
    parser.add_argument("--config", type=Path, required=True, help="Application JSON settings")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        create_server(config, Session(config)).run(transport="stdio")
        return 0
    except ExceptionGroup as group:
        return _report_error(_group_error(group))
    except AdapterError as error:
        return _report_error(error)


def _report_error(error: AdapterError) -> int:
    print(
        json.dumps({"error": {"code": error.code, "message": error.message}}),
        file=sys.stderr,
    )
    return 2


def _group_error(group: ExceptionGroup) -> AdapterError:
    """Unwrap deliberate lifespan errors without printing SDK task-group tracebacks."""
    pending: list[BaseException] = [group]
    found = None
    while pending:
        error = pending.pop()
        if isinstance(error, BaseExceptionGroup):
            pending.extend(error.exceptions)
        elif isinstance(error, AdapterError):
            found = found or error
        else:
            return AdapterError("PROTOCOL_ERROR", "Adapter session failed")
    return found or AdapterError("PROTOCOL_ERROR", "Adapter session failed")


if __name__ == "__main__":
    raise SystemExit(main())
