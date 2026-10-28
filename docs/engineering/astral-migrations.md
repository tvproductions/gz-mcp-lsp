# Worked Astral migrations

These invented examples implement [Astral acceptance](astral-acceptance.md) for
an existing application, typed library and workspace. They preserve observable
behavior while moving from flat imports to installed `src/` packages. Copy files
with an editor in a disposable directory; the paths below are relative to that
directory. `before` and `after` are separate trees, preserving rollback inputs.
No command migrates a real adopter automatically.

The examples use the checkout's tested October 18 snapshot: Python 3.14.8,
uv/uv_build 0.13.1, Ruff 0.15.22, ty 0.0.89 and pre-commit 4.7.0. These are
reproduction pins, not an evergreen freshness claim or permanent adopter patch.
At real adoption verify current stable selections within approved families
through the existing maintenance workflow before recording project pins.

## Shared configuration for every after tree

Append this block to each **root** after `pyproject.toml` below. Member metadata
stays member-owned; root configuration governs workspace tools. This example
uses three baseline dev tools and no hygiene dependencies, so all-group sync is
compatible. A complete adopter must separately reconcile the full Python policy.

### common/pyproject-suffix.toml

```toml
[tool.uv]
required-version = "==0.13.1"
python-preference = "only-managed"

[dependency-groups]
dev = ["ruff==0.15.22", "ty==0.0.89", "pre-commit==4.7.0"]

[tool.ruff]
target-version = "py314"
line-length = 100

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I", "UP", "B", "SIM", "RUF"]

[tool.ty.environment]
python-version = "3.14"
```

Write `.python-version` containing `3.14.8` and ignore `.venv/`, `dist/` and
`__pycache__/`. Use the following shared hooks in each after root. Hooks run the
same locked project commands; installation into Git is a separate observed step.

### common/.pre-commit-config.yaml

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: Ruff check
        entry: uv run --locked ruff check .
        language: system
        pass_filenames: false
        always_run: true
      - id: ruff-format
        name: Ruff format
        entry: uv run --locked ruff format --check .
        language: system
        pass_filenames: false
        always_run: true
      - id: ty
        name: ty
        entry: uv run --locked ty check
        language: system
        pass_filenames: false
        always_run: true
      - id: unittest
        name: unittest
        entry: uv run --locked python -m unittest discover -s tests -v
        language: system
        pass_filenames: false
        always_run: true
```

## 1. Flat application to an installed CLI with package data

Before: `summary.py`, its sibling label and a public output test. The after
tree moves implementation/data under `src/example_summary/`, updates the test
import and declares the existing CLI behavior as an installed entry point.
Package data is read through `importlib.resources`, removing checkout-path
dependence. Operational inputs/products would stay in their existing locations.

### application/before/summary.py

```python
from pathlib import Path


def summarize(values: list[int]) -> str:
    label = Path(__file__).with_name("label.txt").read_text(encoding="utf-8").strip()
    return f"{label}: {sum(values)}"


def main() -> None:
    print(summarize([2, 5]))


if __name__ == "__main__":
    main()
```

### application/before/label.txt

```text
Total
```

### application/before/tests/test_summary.py

```python
import unittest

from summary import summarize


class SummaryTests(unittest.TestCase):
    def test_public_summary(self) -> None:
        self.assertEqual(summarize([2, 5]), "Total: 7")
```

### application/after/pyproject.toml

```toml
[project]
name = "example-summary"
version = "0.1.0"
requires-python = ">=3.14,<3.15"
dependencies = []

[project.scripts]
example-summary = "example_summary:main"

[build-system]
requires = ["uv_build==0.13.1"]
build-backend = "uv_build"
```

### application/after/src/example_summary/__init__.py

```python
from importlib.resources import files


def summarize(values: list[int]) -> str:
    label = files(__package__).joinpath("label.txt").read_text(encoding="utf-8").strip()
    return f"{label}: {sum(values)}"


def main() -> None:
    print(summarize([2, 5]))
```

### application/after/src/example_summary/label.txt

```text
Total
```

### application/after/tests/test_summary.py

```python
import unittest

from example_summary import summarize


class SummaryTests(unittest.TestCase):
    def test_public_summary(self) -> None:
        self.assertEqual(summarize([2, 5]), "Total: 7")
```

## 2. Flat typed library to an installed distribution

Before: importable root package and unittest. Move it to `src/` with the same
public import/API and preserve the typing marker. The consumer checks the
installed inline typing contract using ty. This fixture has no runtime
dependencies; lower dependency-bound testing is N/A. Real published ranges need
separate lowest-bound behavior evidence under the acceptance contract.

### library/before/example_math/__init__.py

```python
def double(value: int) -> int:
    return value * 2
```

### library/before/tests/test_math.py

```python
import unittest

from example_math import double


class MathTests(unittest.TestCase):
    def test_public_double(self) -> None:
        self.assertEqual(double(4), 8)
```

### library/after/pyproject.toml

```toml
[project]
name = "example-math"
version = "0.1.0"
requires-python = ">=3.14,<3.15"
dependencies = []

[build-system]
requires = ["uv_build==0.13.1"]
build-backend = "uv_build"
```

### library/after/src/example_math/__init__.py

```python
def double(value: int) -> int:
    return value * 2
```

Create empty `example_math/py.typed` before and
`src/example_math/py.typed` after. Copy the before test unchanged to
`library/after/tests/test_math.py`.

### library/after/consumer.py

```python
from example_math import double

result: int = double(4)
print(result)
```

This is an ordinary inline typed package. For intentional namespaces or stub-only
packages, follow uv_build's documented layout and test that actual artifact
instead; do not manufacture namespace-parent `__init__.py` files.

## 3. Flat application/helpers to a compatible workspace

Before: one flat app importing a local helper. After: a coordinator without
`[project]`, independently packaged application/library members and an explicit
runtime edge. The root owns shared resolution/tool settings, not a fake runtime
package. Keep incompatible Python families or dependency environments separate.

### workspace/before/math_helpers.py

```python
def double(value: int) -> int:
    return value * 2
```

### workspace/before/app.py

```python
from math_helpers import double


def render() -> str:
    return f"Result: {double(4)}"


def main() -> None:
    print(render())


if __name__ == "__main__":
    main()
```

### workspace/before/tests/test_app.py

```python
import unittest

from app import render


class AppTests(unittest.TestCase):
    def test_public_render(self) -> None:
        self.assertEqual(render(), "Result: 8")
```

### workspace/after/pyproject.toml

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

### workspace/after/packages/app/pyproject.toml

```toml
[project]
name = "example-workspace-app"
version = "0.1.0"
requires-python = ">=3.14,<3.15"
dependencies = ["example-math==0.1.0"]

[project.scripts]
example-workspace-app = "example_workspace_app:main"

[build-system]
requires = ["uv_build==0.13.1"]
build-backend = "uv_build"

[tool.uv.sources]
example-math = { workspace = true }
```

### workspace/after/packages/app/src/example_workspace_app/__init__.py

```python
from example_math import double


def render() -> str:
    return f"Result: {double(4)}"


def main() -> None:
    print(render())
```

### workspace/after/tests/test_app.py

```python
import unittest

from example_workspace_app import render


class AppTests(unittest.TestCase):
    def test_public_render(self) -> None:
        self.assertEqual(render(), "Result: 8")
```

Copy the library after `pyproject.toml` **without the shared root suffix**,
`src/example_math/` including `py.typed`, and `tests/test_math.py` into
`workspace/after/packages/math/`. Copy the workspace root app test into
`packages/app/tests/test_app.py` for separate member verification. Do not add
the root tools/groups to member runtime requirements.

Membership alone is insufficient: app metadata declares `example-math` and its
workspace source. Inspect wheel `Requires-Dist: example-math==0.1.0`. At delivery,
provide both distributions; a local source entry does not publish the library.
Use explicit package/all-package selections even when a coordinator defaults
to all members on the tested uv version. The earlier
[negative control](../evidence/2026-10-18-uv-projects-probe.json) demonstrates why
passing shared-environment tests cannot prove dependency completeness.

## Execute each migration and verify the artifacts

First characterize each before tree, running from its root:

```text
uv run --no-project --python 3.14.8 python -m unittest discover -s tests -v
```

This intentionally tests the old flat layout, not baseline acceptance. Record
the old CLI output (`python summary.py` or `python app.py`) with that same
verified interpreter; expect `Total: 7` or `Result: 8` respectively.

In each after tree, add the shared config, pin/ignore files and hooks above.
Create a disposable Git repository if needed for the example. Then:

For the workspace, apply the sync/build substitutions immediately below before
running this sequence; its coordinator is not itself a buildable distribution.

```text
git init
git add .
uv lock
uv sync --locked --all-groups
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
uv lock --check
uv build --no-sources
```

For workspace sync, explicitly append `--all-packages`. Build its members with
`uv build --no-sources --package example-math` and
`uv build --no-sources --package example-workspace-app`; the coordinator is not
a distribution. Run member tests with `uv run --locked --exact --package NAME
python -m unittest discover -s packages/MEMBER/tests -v`. App selection brings
its declared math dependency. Do not run an unqualified coordinator build.

Before the gate, perform the effective-configuration/provenance inspection in
[acceptance](astral-acceptance.md#verify-effective-configuration-and-execution).
For the library, also run `uv run --locked ty check consumer.py` and
`uv run --locked python consumer.py`; expect no type errors and output `8`.
Use `--offline` during replay only when all pinned inputs are already available.
Create/commit the project lock after reviewed resolution; do not hand-edit it.

For each distribution, inspect wheel and sdist inventories using Python's
`zipfile`/`tarfile`. Check import modules, application label bytes, library
`py.typed`, entry points and Requires-Dist. Build wheels from sdists using the
default build path. Record hashes and exact tool versions for the receipt.

Create a fresh acceptance directory **outside the after tree** and a separate
environment there with `uv venv --python 3.14.8 <env>`. On Windows the interpreter
is `<env>/Scripts/python.exe`; on POSIX it is `<env>/bin/python`. Commands use
that absolute interpreter path as `PYTHON` below; replace placeholders before
executing. Use the installed command from that same environment's scripts/bin
directory as `COMMAND`, not a shell PATH fallback.

```text
uv pip install --python PYTHON --no-deps ABSOLUTE_WHEEL
PYTHON -I -m unittest discover -s ABSOLUTE_AFTER_TEST_DIRECTORY -v
PYTHON -I -c "import IMPORT_PACKAGE; print(IMPORT_PACKAGE.__file__)"
COMMAND
```

`--no-deps` is valid here because the single-package examples have no runtime
dependencies. For the workspace, install the built math wheel first, then app
wheel, and verify the app requirement against installed distribution metadata.
Test math in its own clean environment, and app in a second environment with
only app/math runtime distributions. Expect installed CLI output unchanged;
import origins must lie inside the acceptance environment, outside the source
tree. The app label and library marker must remain in the built wheel.

For the typed library's clean consumer proof, install the **verified pinned ty
tool** into a separate consumer development context; check `consumer.py` against
the installed library, outside its source tree. Demonstrate a negative control
(`double("bad")` is rejected) as well as the valid consumer. This separates
typing-tool dependencies from the clean runtime-only unittest environment.

Rollback in a real project restores the reviewed source/configuration/lock
revision together, recreates the prior environment and reruns the characterized
behavior. It does not delete preserved operational inputs/products or overwrite
unrelated work. In these examples, unchanged before trees are the rollback
control. Record remaining host/platform/deployment work through A01–A18;
successful example execution is not a real adopter acceptance claim.

## Execution evidence

The [migration receipt](../evidence/2026-10-18-astral-migrations.json) records
actual local execution, tool/runtime scope, before/after and isolated checks.
The [artifact inventory supplement](../evidence/2026-10-18-astral-migration-artifacts.json)
rebuilds the retained fixtures and checks both sdist and wheel inventories.
It does not establish remote CI, non-Windows commands, native extensions,
private registries or embedded host behavior. The
[starter acceptance receipt](../evidence/2026-10-18-astral-acceptance.md) records
how the same contract applies to this repository and its outstanding scope.
