#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
CODEX_HOME = Path.home() / ".codex"
AGENTS_HOME = Path.home() / ".agents"


def backup(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        return
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, path.with_suffix(path.suffix + f".bak-{stamp}"))


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.strip()


def install_global_agents() -> None:
    CODEX_HOME.mkdir(parents=True, exist_ok=True)
    src = ROOT / "codex" / "global-AGENTS.md"
    dst = CODEX_HOME / "AGENTS.md"
    backup(dst)
    shutil.copy2(src, dst)
    print(f"installed {dst}")


def install_skill() -> None:
    dst = AGENTS_HOME / "skills" / "ai-dev-framework"
    dst.parent.mkdir(parents=True, exist_ok=True)
    copy_tree(ROOT / "skills" / "ai-dev-framework", dst)
    print(f"installed {dst}")


def install_agents() -> None:
    dst = CODEX_HOME / "agents"
    dst.mkdir(parents=True, exist_ok=True)
    for src in sorted((ROOT / "agents").glob("*.toml")):
        shutil.copy2(src, dst / src.name)
        print(f"installed {dst / src.name}")


def ensure_config() -> None:
    config = CODEX_HOME / "config.toml"
    if not config.exists():
        config.write_text("[features]\nmemories = true\n\n[agents]\nmax_threads = 6\nmax_depth = 1\n", encoding="utf-8")
        print(f"created {config}")
        return

    text = config.read_text(encoding="utf-8")
    changed = False
    additions: list[str] = []
    if "[agents]" not in text:
        additions.append("\n[agents]\nmax_threads = 6\nmax_depth = 1\n")
        changed = True
    if "[features]" not in text:
        additions.append("\n[features]\nmemories = true\n")
        changed = True
    elif "memories = true" not in text:
        additions.append("\n# AI dev framework recommends memories for recurring workflow context.\n# Add `memories = true` under [features] if not already configured.\n")
        changed = True
    if changed:
        backup(config)
        config.write_text(text.rstrip() + "\n" + "\n".join(additions), encoding="utf-8")
        print(f"updated {config}")
    else:
        print(f"kept {config}")


def install_ponytail() -> None:
    marketplace_code, marketplace_out = run(["codex", "plugin", "marketplace", "add", "DietrichGebert/ponytail"])
    print(marketplace_out or "ponytail marketplace already configured or added")
    if marketplace_code != 0 and "already" not in marketplace_out.lower():
        print("warning: could not add Ponytail marketplace")
        return
    plugin_code, plugin_out = run(["codex", "plugin", "add", "ponytail@ponytail"])
    print(plugin_out or "ponytail installed")
    if plugin_code != 0 and "already" not in plugin_out.lower():
        print("warning: could not install Ponytail plugin; install manually from /plugins")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the AI development framework into local Codex defaults.")
    parser.add_argument("--skip-ponytail", action="store_true", help="Do not try to install the Ponytail Codex plugin.")
    args = parser.parse_args()

    install_global_agents()
    install_skill()
    install_agents()
    ensure_config()
    if not args.skip_ponytail:
        install_ponytail()

    print("\nDone. Start a new Codex thread for global AGENTS.md and skills to be picked up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

