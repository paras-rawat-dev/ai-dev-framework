#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_HOME = Path.home() / ".codex"
AGENTS_HOME = Path.home() / ".agents"
PROFILE = json.loads((ROOT / "profiles" / "default.json").read_text(encoding="utf-8"))
PONYTAIL = PROFILE["companions"]["ponytail"]
I_HAVE_ADHD = PROFILE["companions"]["i-have-adhd"]
CODEX_UI_PLUGINS = PROFILE["uiPlugins"]["codex"]


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


def install_plugin(marketplace: str, plugin: str, label: str) -> bool:
    marketplace_cmd = ["codex", "plugin", "marketplace", "add", marketplace]
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
    return install_pinned_plugin(PONYTAIL, "Ponytail")


def git_revision(cmd: list[str]) -> str | None:
    code, output = run(cmd)
    if code != 0 or not output:
        return None
    return output.split()[0]


def install_i_have_adhd() -> bool:
    return install_pinned_plugin(I_HAVE_ADHD, "i-have-adhd")


def installed_plugin_revision(companion: dict[str, object]) -> str | None:
    marketplace = str(companion["codexMarketplace"])
    version = str(companion["version"])
    plugin_name = str(companion["codexPluginId"]).split("@", 1)[0]
    plugin_root = CODEX_HOME / "plugins" / "cache" / marketplace / plugin_name / version
    return git_revision(["git", "-C", str(plugin_root), "rev-parse", "HEAD"])


def managed_marketplace_is_valid(companion: dict[str, object]) -> bool:
    marketplace_root = ROOT / str(companion["codexMarketplacePath"])
    manifest_path = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    plugin_name = str(companion["codexPluginId"]).split("@", 1)[0]
    plugin = next((item for item in manifest.get("plugins", []) if item.get("name") == plugin_name), None)
    if plugin is None:
        return False
    source = plugin.get("source", {})
    return (
        manifest.get("name") == companion["codexMarketplace"]
        and source.get("url") == companion["gitUrl"]
        and source.get("ref") == companion["commit"]
    )


def command_removed_or_absent(code: int, output: str) -> bool:
    normalized = output.lower()
    return (
        code == 0
        or "not installed" in normalized
        or "not found" in normalized
        or "not configured" in normalized
    )


def remove_plugin_and_marketplace(plugin_id: str, marketplace: str) -> bool:
    plugin_code, plugin_output = run(["codex", "plugin", "remove", plugin_id])
    if plugin_output and not command_removed_or_absent(plugin_code, plugin_output):
        print(plugin_output)
    marketplace_code, marketplace_output = run(
        ["codex", "plugin", "marketplace", "remove", marketplace]
    )
    if marketplace_output and not command_removed_or_absent(marketplace_code, marketplace_output):
        print(marketplace_output)
    return command_removed_or_absent(plugin_code, plugin_output) and command_removed_or_absent(
        marketplace_code, marketplace_output
    )


def install_pinned_plugin(companion: dict[str, object], label: str) -> bool:
    marketplace_source = ROOT / str(companion["codexMarketplacePath"])
    marketplace = str(companion["codexMarketplace"])
    plugin_id = str(companion["codexPluginId"])
    legacy_marketplace = str(companion["marketplace"])
    legacy_plugin_id = str(companion["pluginId"])
    expected_revision = str(companion["commit"])

    if not managed_marketplace_is_valid(companion):
        print(f"warning: local {label} marketplace does not match the reviewed profile")
        return False
    if not remove_plugin_and_marketplace(legacy_plugin_id, legacy_marketplace):
        print(f"warning: could not remove the moving upstream {label} marketplace")
        return False
    if not remove_plugin_and_marketplace(plugin_id, marketplace):
        print(f"warning: could not refresh the managed {label} marketplace")
        return False
    if not install_plugin(str(marketplace_source), plugin_id, label):
        return False
    if installed_plugin_revision(companion) == expected_revision:
        return True

    print(f"warning: installed {label} revision was not the reviewed revision; removing it")
    if not remove_plugin_and_marketplace(plugin_id, marketplace):
        print(f"warning: could not confirm the unreviewed {label} plugin is disabled")
    return False


def install_ui_plugins() -> bool:
    ok = True
    for plugin in CODEX_UI_PLUGINS:
        code, output = run(["codex", "plugin", "add", plugin])
        if output:
            print(output)
        if code != 0 and "already" not in output.lower():
            print(f"warning: could not install UI plugin {plugin}")
            ok = False
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the AI development framework into local Codex defaults.")
    parser.add_argument("--skip-ponytail", action="store_true", help="Do not try to install the Ponytail Codex plugin.")
    parser.add_argument("--skip-i-have-adhd", action="store_true", help="Do not install the i-have-adhd output-style plugin.")
    parser.add_argument("--skip-ui-plugins", action="store_true", help="Do not install the default Codex UI capability plugins.")
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
    if not args.skip_ui_plugins:
        if not install_ui_plugins():
            plugins_ok = False

    if not plugins_ok:
        print("\nFramework files installed, but at least one companion plugin failed. See warnings above.")
        return 1

    print("\nDone. Start a new Codex thread for global AGENTS.md and skills to be picked up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
