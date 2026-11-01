"""Disposable crash driver. Fault selectors exist only in this test module."""

import os
import sys
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.edit_plan import plan_workspace_edit
from gz_mcp_lsp.filesystem import Transactions
from gz_mcp_lsp.models import Json
from gz_mcp_lsp.workspace import Workspace


def configuration(base: Path) -> Config:
    return Config(
        base / "workspace",
        Path(sys.executable),
        state_directory=base / "state",
        writable_roots=(base / "workspace",),
        mutations_enabled=True,
    )


def preview(config: Config, workspace: Workspace):
    paths = [config.workspace_root / name for name in ("a.py", "b.py")]
    snapshots = {path.as_uri(): workspace.read(path.as_uri()) for path in paths}
    changes: dict[str, Json] = {
        path.as_uri(): [
            {
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 1, "character": 0}},
                "newText": "first = 10\r\n" if path.name == "a.py" else "second = 20\n",
            }
        ]
        for path in paths
    }
    return plan_workspace_edit(
        {"changes": changes},
        snapshots,
        "disposable-session",
        expires_at=4102444800,
    )


def main():
    base = Path(sys.argv[1]).resolve()
    point = sys.argv[2]

    class CrashingTransactions(Transactions):
        def _write_journal(self, descriptor, record):
            if point == "journal_before" and record["phase"] == "prepared":
                os._exit(73)
            super()._write_journal(descriptor, record)
            if point == record["phase"]:
                os._exit(73)
            for index, file in enumerate(record["files"]):
                if point == f"{file['status']}:{index}":
                    os._exit(73)

        def _replace(self, source, name, target):
            if (
                point in {"rolling_back", "restore_intent:0", "restored:0", "rolled_back"}
                and name == "0001.after"
            ):
                raise OSError("Test-only second replacement failure")
            super()._replace(source, name, target)
            if point == f"replace:{target.index}" and name.endswith(".after"):
                os._exit(73)

        def _write_receipt(self, descriptor, receipt):
            super()._write_receipt(descriptor, receipt)
            if point == "receipt":
                os._exit(73)

    config = configuration(base)
    workspace = Workspace(config)
    plan = preview(config, workspace)
    (base / "plan-id").write_text(plan.plan_id, encoding="ascii")
    CrashingTransactions(config, workspace).apply(plan)
    raise SystemExit("Expected crash boundary was not reached")


if __name__ == "__main__":
    main()
