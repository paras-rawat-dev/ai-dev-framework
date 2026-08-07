#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "profiles" / "default.json").read_text(encoding="utf-8"))
MANAGED_START = "<!-- ai-dev-framework:start -->"
MANAGED_END = "<!-- ai-dev-framework:end -->"
Runner = Callable[[list[str]], tuple[int, str]]


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.strip()


def backup(path: Path) -> None:
    if not path.exists() or path.stat().st_size == 0:
        return
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(path, path.with_suffix(path.suffix + f".bak-{stamp}"))


def merge_managed_markdown(src: Path, dst: Path, dry_run: bool = False) -> None:
    body = src.read_text(encoding="utf-8").strip()
    block = f"{MANAGED_START}\n{body}\n{MANAGED_END}"
    existing = dst.read_text(encoding="utf-8") if dst.exists() else ""

    if MANAGED_START in existing or MANAGED_END in existing:
        if existing.count(MANAGED_START) != 1 or existing.count(MANAGED_END) != 1:
            raise ValueError(f"cannot safely update malformed managed block in {dst}")
        before, remainder = existing.split(MANAGED_START, 1)
        _, after = remainder.split(MANAGED_END, 1)
        parts = [before.rstrip(), block, after.lstrip("\r\n").rstrip()]
        updated = "\n\n".join(part for part in parts if part) + "\n"
    else:
        updated = existing.rstrip()
        if updated:
            updated += "\n\n"
        updated += block + "\n"

    if updated == existing:
        print(f"kept {dst}")
        return
    if dry_run:
        print(f"would merge {src} into {dst}")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    backup(dst)
    dst.write_text(updated, encoding="utf-8")
    print(f"updated {dst}")


def copy_skill(src: Path, dst: Path, dry_run: bool = False) -> None:
    if dry_run:
        print(f"would install {src} at {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_dir() and not dst.is_symlink() and trees_equal(src, dst):
        print(f"kept {dst}")
        return
    if dst.exists() or dst.is_symlink():
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dst = dst.with_name(dst.name + f".bak-{stamp}")
        if dst.is_symlink():
            backup_dst.symlink_to(dst.readlink())
            dst.unlink()
        else:
            shutil.copytree(dst, backup_dst)
            shutil.rmtree(dst)
        print(f"backed up {dst} to {backup_dst}")
    shutil.copytree(src, dst)
    print(f"installed {dst}")


def trees_equal(left: Path, right: Path) -> bool:
    left_files = {path.relative_to(left) for path in left.rglob("*") if path.is_file()}
    right_files = {path.relative_to(right) for path in right.rglob("*") if path.is_file()}
    if left_files != right_files:
        return False
    return all(filecmp.cmp(left / path, right / path, shallow=False) for path in left_files)


def ensure_gitignore_entry(path: Path, entry: str, dry_run: bool = False) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if entry in {line.strip() for line in existing.splitlines()}:
        print(f"kept {path}")
        return
    if dry_run:
        print(f"would add {entry} to {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    updated = existing.rstrip()
    if updated:
        updated += "\n"
    path.write_text(updated + entry + "\n", encoding="utf-8")
    print(f"updated {path}")


def run_required(cmd: list[str], label: str, runner: Runner, dry_run: bool = False) -> bool:
    if dry_run:
        print(f"would run: {shlex.join(cmd)}")
        return True
    code, output = runner(cmd)
    if output:
        print(output)
    if code == 0 or "already" in output.lower():
        return True
    print(f"warning: could not install {label}")
    return False


def install_graphify(
    home: Path,
    agent: str,
    runner: Runner,
    *,
    scope: str = "user",
    target: Path | None = None,
    dry_run: bool = False,
) -> bool:
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "install_graphify.py"),
        "--platform",
        agent,
        "--scope",
        scope,
        "--home",
        str(home),
    ]
    if target is not None:
        cmd.extend(["--target", str(target)])
    if dry_run:
        cmd.append("--dry-run")
    return run_required(cmd, "Graphify", runner, dry_run)


def prepare_claude_marketplace(
    home: Path,
    companion: dict[str, object],
    runner: Runner,
    dry_run: bool = False,
) -> Path | None:
    name = str(companion["marketplace"])
    revision = str(companion["commit"])
    destination = (
        home
        / ".claude"
        / "ai-dev-framework"
        / "marketplaces"
        / f"{name}-{revision[:12]}"
    )

    if dry_run:
        print(f"would prepare reviewed {name} marketplace at {destination}")
        print(f"would fetch and verify {companion['gitUrl']} at {revision}")
        return destination

    if destination.exists():
        code, output = runner(["git", "-C", str(destination), "rev-parse", "HEAD"])
        installed_revision = output.split()[0] if code == 0 and output else None
        if installed_revision == revision:
            print(f"kept reviewed {name} marketplace at {destination}")
            return destination
        print(f"warning: {destination} does not contain the reviewed {name} revision")
        return None

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{name}-", dir=destination.parent))
    commands = [
        ["git", "init", "--quiet", str(temporary)],
        ["git", "-C", str(temporary), "remote", "add", "origin", str(companion["gitUrl"])],
        ["git", "-C", str(temporary), "fetch", "--quiet", "--depth", "1", "origin", revision],
        ["git", "-C", str(temporary), "checkout", "--quiet", "--detach", "FETCH_HEAD"],
    ]
    try:
        for command in commands:
            if not run_required(command, f"reviewed {name} marketplace", runner):
                return None
        code, output = runner(["git", "-C", str(temporary), "rev-parse", "HEAD"])
        installed_revision = output.split()[0] if code == 0 and output else None
        if installed_revision != revision:
            print(f"warning: fetched {name} revision did not match {revision}")
            return None
        temporary.rename(destination)
        print(f"prepared reviewed {name} marketplace at {destination}")
        return destination
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def replace_claude_marketplace(
    marketplace: str,
    source: Path,
    runner: Runner,
    dry_run: bool = False,
) -> bool:
    remove_command = ["claude", "plugin", "marketplace", "remove", marketplace]
    if dry_run:
        print(f"would run: {shlex.join(remove_command)} (missing marketplace is allowed)")
    else:
        code, output = runner(remove_command)
        missing = code != 0 and "not found" in output.lower()
        if output and not missing:
            print(output)
        if code != 0 and not missing:
            print(f"warning: could not replace {marketplace} marketplace")
            return False
    return run_required(
        ["claude", "plugin", "marketplace", "add", str(source)],
        f"{marketplace} marketplace",
        runner,
        dry_run,
    )


def install_claude(
    home: Path,
    runner: Runner = run,
    *,
    skip_ponytail: bool = False,
    skip_i_have_adhd: bool = False,
    skip_graphify: bool = False,
    skip_ui_plugins: bool = False,
    dry_run: bool = False,
) -> bool:
    if not dry_run and shutil.which("claude") is None:
        print("error: Claude Code CLI is not installed or not on PATH")
        return False

    merge_managed_markdown(ROOT / "claude" / "global-CLAUDE.md", home / ".claude" / "CLAUDE.md", dry_run)
    copy_skill(
        ROOT / "skills" / "ai-dev-framework",
        home / ".claude" / "skills" / "ai-dev-framework",
        dry_run,
    )

    ok = True
    if not skip_graphify:
        ok &= install_graphify(home, "claude", runner, dry_run=dry_run)

    companions = PROFILE["companions"]
    selected: list[tuple[str, dict[str, object]]] = []
    if not skip_ponytail:
        selected.append(("ponytail", companions["ponytail"]))
    if not skip_i_have_adhd:
        selected.append(("i-have-adhd", companions["i-have-adhd"]))

    installed_companions: set[str] = set()
    for name, companion in selected:
        source = prepare_claude_marketplace(home, companion, runner, dry_run)
        marketplace_ok = source is not None and replace_claude_marketplace(
            str(companion["marketplace"]), source, runner, dry_run
        )
        ok &= marketplace_ok
        plugin_ok = False
        if marketplace_ok:
            plugin_ok = run_required(
                ["claude", "plugin", "install", companion["pluginId"], "--scope", "user"],
                companion["pluginId"],
                runner,
                dry_run,
            )
            ok &= plugin_ok
        if plugin_ok:
            installed_companions.add(name)

    if not skip_i_have_adhd and "i-have-adhd" in installed_companions:
        flag = home / ".claude" / ".i-have-adhd-always"
        if dry_run:
            print(f"would enable i-have-adhd by creating {flag}")
        else:
            flag.parent.mkdir(parents=True, exist_ok=True)
            flag.touch()
            print(f"enabled i-have-adhd with {flag}")

    if not skip_ui_plugins:
        for plugin in PROFILE["uiPlugins"]["claude"]:
            ok &= run_required(
                ["claude", "plugin", "install", plugin, "--scope", "user"],
                plugin,
                runner,
                dry_run,
            )

    return bool(ok)


def install_copilot(
    home: Path,
    runner: Runner = run,
    *,
    scope: str = "user",
    target: Path | None = None,
    skip_ponytail: bool = False,
    skip_i_have_adhd: bool = False,
    skip_graphify: bool = False,
    skip_ui_plugins: bool = False,
    dry_run: bool = False,
) -> bool:
    if not dry_run:
        code, output = runner(["gh", "skill", "--help"])
        if code != 0:
            if output:
                print(output)
            print("error: GitHub CLI 2.90.0 or later with `gh skill` is required")
            return False

    project_scope = scope == "project"
    project_root = (target or Path.cwd()).resolve()
    instruction_source = (
        ROOT / "copilot" / "project-copilot-instructions.md"
        if project_scope
        else ROOT / "copilot" / "global-copilot-instructions.md"
    )
    instruction_destination = (
        project_root / ".github" / "copilot-instructions.md"
        if project_scope
        else home / ".copilot" / "copilot-instructions.md"
    )
    skill_destination = (
        project_root / ".agents" / "skills"
        if project_scope
        else home / ".copilot" / "skills"
    )

    merge_managed_markdown(instruction_source, instruction_destination, dry_run)
    copy_skill(
        ROOT / "skills" / "ai-dev-framework",
        skill_destination / "ai-dev-framework",
        dry_run,
    )
    if project_scope:
        ensure_gitignore_entry(project_root / ".gitignore", "graphify-out/", dry_run)

    ok = True
    if not skip_graphify:
        ok &= install_graphify(
            home,
            "github-copilot",
            runner,
            scope=scope,
            target=project_root if project_scope else None,
            dry_run=dry_run,
        )

    companions = PROFILE["companions"]
    selected = []
    if not skip_ponytail:
        selected.append(companions["ponytail"])
    if not skip_i_have_adhd:
        selected.append(companions["i-have-adhd"])

    for companion in selected:
        for skill in companion["copilotSkills"]:
            destination_args = (
                ["--dir", str(skill_destination)]
                if project_scope
                else ["--agent", "github-copilot", "--scope", "user"]
            )
            ok &= run_required(
                [
                    "gh",
                    "skill",
                    "install",
                    companion["repository"],
                    skill,
                    "--pin",
                    companion["commit"],
                    *destination_args,
                    "--force",
                ],
                f"{skill} Copilot skill",
                runner,
                dry_run,
            )

    if not skip_ui_plugins:
        print(
            "GitHub Copilot has no required cross-surface UI plugin in this profile; "
            "the framework skill supplies UI guidance and projects supply their own browser tests."
        )

    return bool(ok)


def install_codex(args: argparse.Namespace, dry_run: bool = False) -> bool:
    cmd = [sys.executable, str(ROOT / "scripts" / "install_codex_framework.py")]
    if args.skip_ponytail:
        cmd.append("--skip-ponytail")
    if args.skip_i_have_adhd:
        cmd.append("--skip-i-have-adhd")
    if args.skip_graphify:
        cmd.append("--skip-graphify")
    if args.skip_ui_plugins:
        cmd.append("--skip-ui-plugins")
    if dry_run:
        print(f"would run: {shlex.join(cmd)}")
        return True
    return subprocess.run(cmd).returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the AI development framework for a coding agent.")
    parser.add_argument("--agent", required=True, choices=["codex", "claude", "github-copilot"])
    parser.add_argument("--skip-ponytail", action="store_true")
    parser.add_argument("--skip-i-have-adhd", action="store_true")
    parser.add_argument("--skip-graphify", action="store_true")
    parser.add_argument("--skip-ui-plugins", action="store_true")
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--target", type=Path, help="Project root for --scope project")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without changing the machine")
    args = parser.parse_args()

    if args.scope == "project" and args.agent != "github-copilot":
        parser.error("project scope is currently supported only for github-copilot")
    if args.target is not None and args.scope != "project":
        parser.error("--target requires --scope project")

    home = Path.home()
    if args.agent == "codex":
        ok = install_codex(args, args.dry_run)
    elif args.agent == "claude":
        ok = install_claude(
            home,
            skip_ponytail=args.skip_ponytail,
            skip_i_have_adhd=args.skip_i_have_adhd,
            skip_graphify=args.skip_graphify,
            skip_ui_plugins=args.skip_ui_plugins,
            dry_run=args.dry_run,
        )
    else:
        ok = install_copilot(
            home,
            scope=args.scope,
            target=args.target,
            skip_ponytail=args.skip_ponytail,
            skip_i_have_adhd=args.skip_i_have_adhd,
            skip_graphify=args.skip_graphify,
            skip_ui_plugins=args.skip_ui_plugins,
            dry_run=args.dry_run,
        )

    if not ok:
        print("\nFramework setup was incomplete. Review the warnings above.")
        return 1
    print("\nDone. Start a new agent session so instructions, skills, plugins, and hooks are loaded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
