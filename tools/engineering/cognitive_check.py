"""Consumer-side ceiling/discovery gate for the incoming upstream cognitive engine."""

import argparse
import ast
import hashlib
import json
import platform
import sys
import tokenize
from collections import Counter
from pathlib import Path

from tools.engineering.cognitive_qualification import CONTRACT, Engine, load_engine, qualify
from tools.engineering.complexity_check import source_files

CEILING = 15


def inventory(source: str, filename: str) -> list[tuple[str, int]]:
    """Find non-enclosed functions independently across all statement containers."""
    compile(source, filename, "exec")
    found = []

    def visit(node: ast.AST, prefix: str) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.append((prefix + node.name, node.lineno))
            return  # Nested definitions fold into this unit, per the selected metric.
        if isinstance(node, ast.ClassDef):
            prefix += node.name + "."
        for child in ast.iter_child_nodes(node):
            visit(child, prefix)

    visit(ast.parse(source, filename=filename), "")
    return found


def measure(path: Path, root: Path, engine: Engine) -> dict:
    """Require complete identity discovery and valid scores on unchanged source."""
    with tokenize.open(path) as handle:
        source = handle.read()
    expected = Counter(inventory(source, str(path)))
    scores = list(engine(source, str(path)))
    if any(
        not isinstance(row.name, str)
        or type(row.line) is not int
        or row.line < 1
        or type(row.score) is not int
        or row.score < 0
        for row in scores
    ):
        raise ValueError(
            "Cognitive identities/scores must have valid names and integer locations/scores"
        )
    actual = Counter((row.name, row.line) for row in scores)
    if actual != expected:
        raise ValueError(
            f"Function discovery mismatch: expected {dict(expected)}, got {dict(actual)}"
        )
    return {
        "file": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "functions": [{"name": row.name, "line": row.line, "score": row.score} for row in scores],
    }


def assess(root: Path, paths: list[str], engine: Engine) -> dict:
    """Keep qualification errors, source errors and ceiling violations distinct."""
    receipt = {
        "contract": CONTRACT,
        "ceiling": CEILING,
        "python": platform.python_version(),
        "scope": paths,
        "modules": [],
        "errors": [],
        "violations": [],
    }
    try:
        receipt["qualification"] = qualify(engine)
        if receipt["qualification"]["status"] != "passed":
            raise ValueError("Upstream engine failed independent qualification")
        files = source_files(root, paths)
    except (ValueError, OSError) as error:
        receipt["errors"].append({"message": str(error)})
        files = []
    for path in files:
        try:
            receipt["modules"].append(measure(path, root, engine))
        except (Exception, SystemExit) as error:  # A candidate exit is not a passing measurement.
            receipt["errors"].append({"file": str(path.relative_to(root)), "message": str(error)})
    for module in receipt["modules"]:
        receipt["violations"].extend(
            {"file": module["file"], **row} for row in module["functions"] if row["score"] > CEILING
        )
    scores = [row["score"] for module in receipt["modules"] for row in module["functions"]]
    receipt["aggregate"] = {"functions": len(scores), "maximum": max(scores) if scores else None}
    receipt["status"] = (
        "error" if receipt["errors"] else "failed" if receipt["violations"] else "passed"
    )
    return receipt


def main() -> int:
    """Bind an installed upstream engine; no private or default scorer is supplied."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True, help="Installed module:scoring_function")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--paths", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        engine, identity = load_engine(args.engine)
        receipt = assess(args.root.resolve(strict=True), args.paths, engine) | identity
    except (
        Exception,
        SystemExit,
    ) as error:  # Import/adapter failures remain structured tool errors.
        receipt = {"status": "error", "engine": args.engine, "error": str(error)}
    try:
        args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        receipt = {"status": "error", "engine": args.engine, "error": str(error)}
    print(
        json.dumps({key: receipt[key] for key in ("status", "engine", "error") if key in receipt})
    )
    return {"passed": 0, "failed": 1, "error": 2}[receipt["status"]]


if __name__ == "__main__":
    sys.exit(main())
