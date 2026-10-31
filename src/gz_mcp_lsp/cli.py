"""Explicit JSON configuration entry point; stdout belongs exclusively to MCP."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from gz_mcp_lsp.config import load_config
from gz_mcp_lsp.mcp_api import create_server
from gz_mcp_lsp.models import AdapterError
from gz_mcp_lsp.session import Session


def main(argv: Sequence[str] | None = None) -> int:
    """Validate settings before launching a subprocess or opening MCP stdio."""
    parser = argparse.ArgumentParser(prog="gz-mcp-lsp")
    parser.add_argument("--config", type=Path, required=True, help="Trusted JSON settings path")
    arguments = parser.parse_args(argv)
    try:
        config = load_config(arguments.config)
        create_server(config, Session(config)).run(transport="stdio")
    except AdapterError as error:
        print(f"{error.code}: {error.message}", file=sys.stderr)
        return 2
    return 0
