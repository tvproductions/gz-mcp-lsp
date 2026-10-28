"""Generate wheel resources from the authoritative checkout files."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_PATHS = (
    "bundle.json",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    "templates/AGENTS.skills-first.md",
    "templates/skills/update-gz-template/SKILL.md",
)


def main() -> int:
    """Refresh generated resources or report drift without writing."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    destination = ROOT / "src/skills_first_starter/resources"
    stale = []
    for relative in RESOURCE_PATHS:
        source = ROOT / relative
        target = destination / relative
        content = source.read_bytes()
        if args.check:
            if not target.is_file() or target.read_bytes() != content:
                stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    if stale:
        parser.exit(1, f"Stale wheel resources: {', '.join(stale)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
