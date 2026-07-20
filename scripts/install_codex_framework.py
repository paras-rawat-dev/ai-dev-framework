#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
CODEX_HOME = Path.home() / ".codex"
AGENTS_HOME = Path.home() / ".agents"
I_HAVE_ADHD_REPOSITORY = "https://github.com/ayghri/i-have-adhd.git"
I_HAVE_ADHD_REF = "main"
I_HAVE_ADHD_VERSION = "0.1.0"
I_HAVE_ADHD_REVIEWED_REVISION = "72c33eee81ea439cf01991e93729adfce2ffc99e"


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


def install_plugin(marketplace: str, plugin: str, label: str, ref: str | None = None) -> bool:
    marketplace_cmd = ["codex", "plugin", "marketplace", "add", marketplace]
    if ref:
        marketplace_cmd.extend(["--ref", ref])
    marketplace_code, marketplace_out = run(marketplace_cmd)
    if marketplace_out:
        print(marketplace_out)
    if marketplace_code != 0 and "already" not in marketplace_out.lower():
        print(f"warning: could not add {label} marketplace")
        return False
    if not marketplace_out:
        print(f"{label} marketplace already configured or added")

    plugin_code, plugin_out = run(["codex", "plugin", "add", plugin])
    if plugin_out:
        print(plugin_out)
    if plugin_code != 0 and "already" not in plugin_out.lower():
        print(f"warning: could not install {label} plugin; install manually from /plugins")
        return False
    if not plugin_out:
        print(f"{label} installed")
    return True


def install_ponytail() -> bool:
    return install_plugin("DietrichGebert/ponytail", "ponytail@ponytail", "Ponytail")


def git_revision(cmd: list[str]) -> str | None:
    code, output = run(cmd)
    if code != 0 or not output:
        return None
    return output.split()[0]


def install_i_have_adhd() -> bool:
    remote_revision = git_revision(
        ["git", "ls-remote", I_HAVE_ADHD_REPOSITORY, f"refs/heads/{I_HAVE_ADHD_REF}"]
    )
    if remote_revision != I_HAVE_ADHD_REVIEWED_REVISION:
        print(
            "warning: i-have-adhd main no longer matches the reviewed revision; "
            "review the upstream changes before updating the framework pin"
        )
        return False

    if not install_plugin(
        "ayghri/i-have-adhd",
        "i-have-adhd@i-have-adhd",
        "i-have-adhd",
        ref=I_HAVE_ADHD_REF,
    ):
        return False

    plugin_root = CODEX_HOME / "plugins" / "cache" / "i-have-adhd" / "i-have-adhd" / I_HAVE_ADHD_VERSION
    installed_revision = git_revision(["git", "-C", str(plugin_root), "rev-parse", "HEAD"])
    if installed_revision == I_HAVE_ADHD_REVIEWED_REVISION:
        return True

    print("warning: installed i-have-adhd revision was not the reviewed revision; removing it")
    remove_code, remove_output = run(["codex", "plugin", "remove", "i-have-adhd@i-have-adhd"])
    if remove_output:
        print(remove_output)

    list_code, list_output = run(["codex", "plugin", "list", "--json"])
    try:
        installed_plugins = json.loads(list_output).get("installed", []) if list_code == 0 else []
    except json.JSONDecodeError:
        installed_plugins = []
        list_code = 1
    still_enabled = any(
        item.get("pluginId") == "i-have-adhd@i-have-adhd" and item.get("enabled", False)
        for item in installed_plugins
    )
    if remove_code != 0 or list_code != 0 or still_enabled:
        print("warning: could not confirm the unreviewed i-have-adhd plugin is disabled")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the AI development framework into local Codex defaults.")
    parser.add_argument("--skip-ponytail", action="store_true", help="Do not try to install the Ponytail Codex plugin.")
    parser.add_argument("--skip-i-have-adhd", action="store_true", help="Do not install the i-have-adhd output-style plugin.")
    args = parser.parse_args()

    install_global_agents()
    install_skill()
    install_agents()
    ensure_config()
    plugins_ok = True
    if not args.skip_ponytail:
        if not install_ponytail():
            plugins_ok = False
    if not args.skip_i_have_adhd:
        if not install_i_have_adhd():
            plugins_ok = False

    if not plugins_ok:
        print("\nFramework files installed, but at least one companion plugin failed. See warnings above.")
        return 1

    print("\nDone. Start a new Codex thread for global AGENTS.md and skills to be picked up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
