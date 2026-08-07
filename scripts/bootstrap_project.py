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

TOOL_FILES = {
    "CLAUDE.md": ROOT / "claude" / "project-CLAUDE.md",
    ".github/copilot-instructions.md": ROOT / "copilot" / "project-copilot-instructions.md",
}


def write_if_missing(src: Path, dst: Path, force: bool) -> str:
    if dst.exists() and not force:
        return f"kept {dst}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"wrote {dst}"


def ensure_gitignore_entry(path: Path, entry: str) -> str:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if entry in {line.strip() for line in existing.splitlines()}:
        return f"kept {path}"
    updated = existing.rstrip()
    if updated:
        updated += "\n"
    path.write_text(updated + entry + "\n", encoding="utf-8")
    return f"updated {path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap framework project docs into a target repository.")
    parser.add_argument("target", nargs="?", default=".", help="Target project root")
    parser.add_argument("--force", action="store_true", help="Overwrite existing project docs")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    for name, src in PROJECT_FILES.items():
        print(write_if_missing(src, target / name, args.force))

    for name, src in TOOL_FILES.items():
        print(write_if_missing(src, target / name, args.force))

    print(ensure_gitignore_entry(target / ".gitignore", "graphify-out/"))

    agents = target / "AGENTS.md"
    if not agents.exists() or args.force:
        agents.write_text(
            "# Project Agent Instructions\n\n"
            "Read PROJECT_CHARTER.md, ARCHITECTURE.md, TESTING.md, and AI_WORKFLOW.md before non-trivial changes.\n\n"
            "Use the installed ai-dev-framework, Ponytail, i-have-adhd, and Graphify companions. Report a missing companion instead of pretending it ran.\n\n"
            "Follow selected stack packs and UI member choices from PROJECT_CHARTER.md.\n"
            "Challenge scope creep, unnecessary dependencies, missing verification, and UI-library drift.\n"
            "Use Graphify for justified architecture, RCA, migration, onboarding, or cross-component work; verify graph findings against source.\n",
            encoding="utf-8",
        )
        print(f"wrote {agents}")
    else:
        print(f"kept {agents}")

    print("\nNext: fill the templates with project-specific facts before major implementation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
