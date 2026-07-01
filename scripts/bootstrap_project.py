#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PROJECT_FILES = {
    "PROJECT_CHARTER.md": ROOT / "projects" / "TEMPLATE.project-charter.md",
    "ARCHITECTURE.md": ROOT / "projects" / "TEMPLATE.architecture.md",
    "TESTING.md": ROOT / "projects" / "TEMPLATE.testing.md",
    "AI_WORKFLOW.md": ROOT / "projects" / "TEMPLATE.ai-workflow.md",
}


def write_if_missing(src: Path, dst: Path, force: bool) -> str:
    if dst.exists() and not force:
        return f"kept {dst}"
    shutil.copy2(src, dst)
    return f"wrote {dst}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap framework project docs into a target repository.")
    parser.add_argument("target", nargs="?", default=".", help="Target project root")
    parser.add_argument("--force", action="store_true", help="Overwrite existing project docs")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    for name, src in PROJECT_FILES.items():
        print(write_if_missing(src, target / name, args.force))

    agents = target / "AGENTS.md"
    if not agents.exists() or args.force:
        agents.write_text(
            "# Project Agent Instructions\n\n"
            "Read PROJECT_CHARTER.md, ARCHITECTURE.md, TESTING.md, and AI_WORKFLOW.md before non-trivial changes.\n\n"
            "Follow selected stack packs and UI member choices from PROJECT_CHARTER.md.\n"
            "Challenge scope creep, unnecessary dependencies, missing verification, and UI-library drift.\n",
            encoding="utf-8",
        )
        print(f"wrote {agents}")
    else:
        print(f"kept {agents}")

    print("\nNext: fill the templates with project-specific facts before major implementation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

