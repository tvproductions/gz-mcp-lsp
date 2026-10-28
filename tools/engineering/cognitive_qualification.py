"""Independent fixtures for qualifying a separately owned cognitive engine."""

import argparse
import hashlib
import importlib
import inspect
import json
import platform
import sys
from collections.abc import Callable, Iterable
from importlib.metadata import packages_distributions, version
from pathlib import Path
from typing import Protocol

CONTRACT = "gzkit-cognitive-v1"
FIXTURES = Path(__file__).with_name("fixtures") / "cognitive-v1.json"


class Score(Protocol):
    """The existing engine's located score interface, without its implementation."""

    name: str
    line: int
    score: int


type Engine = Callable[[str, str], Iterable[Score]]


def observe(engine: Engine, case: dict) -> dict:
    """Compare one independently specified result, keeping failures observable."""
    name = case["name"]
    result = {"case": name, "expected": case.get("scores", "SyntaxError")}
    try:
        observed = list(engine(case["source"], f"<qualification:{name}>"))
        rows = [{"name": row.name, "line": row.line, "score": row.score} for row in observed]
        valid = all(
            isinstance(row["name"], str)
            and type(row["line"]) is int
            and row["line"] > 0
            and type(row["score"]) is int
            and row["score"] >= 0
            for row in rows
        )
        result["observed"] = rows
        result["passed"] = valid and rows == case.get("scores")
    except SyntaxError:
        result["observed"] = "SyntaxError"
        result["passed"] = case.get("error") == "SyntaxError"
    except (Exception, SystemExit) as error:  # A candidate must not turn exit(0) into acceptance.
        result["observed"] = {"error": type(error).__name__, "message": str(error)}
        result["passed"] = False
    return result


def qualify(engine: Engine) -> dict:
    """Run the complete holdout population without changing the candidate engine."""
    payload = FIXTURES.read_bytes()
    fixtures = json.loads(payload)
    if fixtures["contract"] != CONTRACT or not fixtures["cases"]:
        raise ValueError("Missing or incompatible cognitive qualification fixtures")
    results = [observe(engine, case) for case in fixtures["cases"]]
    return {
        "contract": CONTRACT,
        "python": platform.python_version(),
        "fixtures_sha256": hashlib.sha256(payload).hexdigest(),
        "status": "passed" if all(row["passed"] for row in results) else "failed",
        "cases": results,
    }


def load_engine(entrypoint: str) -> tuple[Engine, dict]:
    """Require installed, identifiable upstream code before a CLI can accept it."""
    module, attribute = entrypoint.split(":", 1)
    engine = getattr(importlib.import_module(module), attribute)
    if not callable(engine):
        raise TypeError("Engine entry point must be callable")
    source = inspect.getsourcefile(engine)
    distributions = packages_distributions().get(module.split(".")[0], [])
    if source is None or not distributions:
        raise ValueError("Engine must have identifiable source and installed distribution metadata")
    return engine, {
        "engine": entrypoint,
        "engine_source_sha256": hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        "engine_distributions": {
            distribution: version(distribution) for distribution in distributions
        },
    }


def main() -> int:
    """Qualify an installed module entry point and emit reliable structured status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True, help="Installed module:scoring_function")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        engine, identity = load_engine(args.engine)
        receipt = qualify(engine) | identity
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
