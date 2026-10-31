"""Crash only this disposable worker at a named durable transaction boundary."""

import os
import sys
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.edit_plan import plan_workspace_edit
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.workspace import Workspace


class CrashTransactions(Transactions):
    """No product configuration can enable this test-only process exit."""

    def _checkpoint(self, event: str) -> None:
        if sys.argv[3].startswith("rollback:") and event == "replace:1":
            raise OSError("trigger recovery before test-only crash")
        if event == sys.argv[3]:
            os._exit(77)


def main():
    """Build independent fixture edits; the parent verifies disk and restart outcome."""
    root, state = Path(sys.argv[1]), Path(sys.argv[2])
    config = Config(
        root,
        Path("/usr/bin/true"),
        state_directory=state,
        mutations_enabled=True,
        writable_roots=(root,),
    )
    workspace = Workspace(config)
    snapshots = {
        path.as_uri(): workspace.read(path.as_uri()) for path in (root / "a.py", root / "b.py")
    }
    edit = {
        "changes": {
            uri: [
                {
                    "range": {
                        "start": {"line": 0, "character": 0},
                        "end": {"line": 0, "character": 1},
                    },
                    "newText": "z",
                }
            ]
            for uri in snapshots
        }
    }
    plan = plan_workspace_edit(edit, snapshots, workspace.manifest())
    transaction = CrashTransactions(config, workspace)
    try:
        transaction.apply(plan)
    finally:
        transaction.close()


if __name__ == "__main__":
    main()
