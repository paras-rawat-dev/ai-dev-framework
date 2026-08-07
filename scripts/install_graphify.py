#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "profiles" / "default.json").read_text(encoding="utf-8"))
GRAPHIFY = PROFILE["tools"]["graphify"]
POLICY_START = "<!-- ai-dev-framework:graphify-policy:start -->"
POLICY_END = "<!-- ai-dev-framework:graphify-policy:end -->"
COMMAND_MARKER = "# ai-dev-framework managed Graphify command"
REMOTE_ENV_KEYS = (
    "ANTHROPIC_API_KEY",
    "MOONSHOT_API_KEY",
    "OLLAMA_API_KEY",
    "OLLAMA_BASE_URL",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "OPENAI_API_KEY",
    "OPENAI_BASE_URL",
    "DEEPSEEK_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "AWS_PROFILE",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "AWS_WEB_IDENTITY_TOKEN_FILE",
    "AWS_ROLE_ARN",
    "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",
    "AWS_CONTAINER_CREDENTIALS_FULL_URI",
)
Runner = Callable[[list[str], Optional[Path], Optional[dict[str, str]]], tuple[int, str]]


def run(
    cmd: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as exc:
        return 127, str(exc)
    return proc.returncode, proc.stdout.strip()


def venv_bin(root: Path) -> Path:
    return root / ("Scripts" if os.name == "nt" else "bin")


def python_candidates() -> list[str]:
    candidates = [
        os.environ.get("GRAPHIFY_PYTHON", ""),
        "python3.14",
        "python3.13",
        "python3.12",
        "python3.11",
        "python3.10",
        sys.executable,
        "python3",
    ]
    resolved: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        path = candidate if Path(candidate).is_absolute() else shutil.which(candidate)
        if path and path not in resolved:
            resolved.append(path)
    return resolved


def find_python(runner: Runner = run) -> str | None:
    minimum = tuple(GRAPHIFY["minimumPython"])
    for candidate in python_candidates():
        code, output = runner(
            [candidate, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            None,
            None,
        )
        if code != 0:
            continue
        try:
            version = tuple(int(part) for part in output.split(".")[:2])
        except ValueError:
            continue
        if version >= minimum:
            return candidate
    return None


def installed_metadata(root: Path, runner: Runner = run) -> dict[str, object] | None:
    python = venv_bin(root) / ("python.exe" if os.name == "nt" else "python")
    if not python.exists():
        return None
    script = (
        "import importlib.metadata as m, json; "
        "d=m.distribution('graphifyy'); "
        "print(json.dumps({'version': d.version, "
        "'direct_url': json.loads(d.read_text('direct_url.json') or '{}')}))"
    )
    code, output = runner([str(python), "-c", script], None, None)
    if code != 0 or not output:
        return None
    try:
        return json.loads(output.splitlines()[-1])
    except json.JSONDecodeError:
        return None


def metadata_is_valid(metadata: dict[str, object] | None) -> bool:
    if metadata is None:
        return False
    direct_url = metadata.get("direct_url", {})
    if not isinstance(direct_url, dict):
        return False
    vcs_info = direct_url.get("vcs_info", {})
    if not isinstance(vcs_info, dict):
        return False
    return (
        metadata.get("version") == GRAPHIFY["version"]
        and direct_url.get("url") == GRAPHIFY["gitUrl"]
        and vcs_info.get("vcs") == "git"
        and vcs_info.get("requested_revision") == GRAPHIFY["commit"]
        and vcs_info.get("commit_id") == GRAPHIFY["commit"]
    )


def install_is_valid(root: Path, runner: Runner = run) -> bool:
    receipt = root / "ai-dev-framework-install.json"
    try:
        recorded = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    metadata = installed_metadata(root, runner)
    if not metadata_is_valid(metadata):
        return False
    graphify = venv_bin(root) / ("graphify.exe" if os.name == "nt" else "graphify")
    code, version_output = runner([str(graphify), "--version"], None, None)
    if code != 0 or str(GRAPHIFY["version"]) not in version_output:
        return False
    return (
        recorded.get("repository") == GRAPHIFY["gitUrl"]
        and recorded.get("commit") == GRAPHIFY["commit"]
        and recorded.get("version") == GRAPHIFY["version"]
    )


def managed_command(path: Path, managed_root: Path) -> bool:
    if path.is_symlink():
        try:
            path.resolve(strict=False).relative_to(managed_root.resolve())
            return True
        except ValueError:
            return False
    if not path.is_file():
        return False
    try:
        return COMMAND_MARKER in path.read_text(encoding="utf-8").splitlines()[:3]
    except (OSError, UnicodeDecodeError):
        return False


def command_wrapper(root: Path, command: str) -> str:
    python = venv_bin(root) / "python"
    module, function = (
        ("graphify.serve", "_main")
        if command == "graphify-mcp"
        else ("graphify.__main__", "main")
    )
    keys = repr(REMOTE_ENV_KEYS)
    approval = str(GRAPHIFY["remoteApprovalEnv"])
    return (
        f"#!{python}\n"
        f"{COMMAND_MARKER}\n"
        "import os\n"
        f"if os.environ.get({approval!r}) != '1':\n"
        f"    for key in {keys}:\n"
        "        os.environ.pop(key, None)\n"
        f"from {module} import {function}\n"
        f"raise SystemExit({function}())\n"
    )


def expose_commands(root: Path, home: Path, dry_run: bool = False) -> bool:
    source_bin = venv_bin(root)
    destination_bin = home / ".local" / "bin"
    managed_root = home / ".local" / "share" / "ai-dev-framework" / "tools" / "graphify"
    ok = True
    for command in GRAPHIFY["commands"]:
        source = source_bin / command
        destination = destination_bin / command
        expected_wrapper = command_wrapper(root, command)
        if dry_run:
            print(f"would expose {source} at {destination}")
            continue
        if not source.exists():
            print(f"warning: Graphify did not install expected command {source}")
            ok = False
            continue
        destination_bin.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            try:
                same = (
                    destination.is_file()
                    and not destination.is_symlink()
                    and destination.read_text(encoding="utf-8") == expected_wrapper
                )
            except (OSError, UnicodeDecodeError):
                same = False
            if same:
                print(f"kept {destination}")
                continue
            if not managed_command(destination, managed_root):
                print(f"warning: refusing to replace unmanaged command {destination}")
                ok = False
                continue
            destination.unlink()
        destination.write_text(expected_wrapper, encoding="utf-8")
        destination.chmod(0o755)
        print(f"exposed {destination}")
    return ok


def graphify_skill_path(
    platform: str,
    home: Path,
    scope: str,
    target: Path | None,
    *,
    upstream: bool = False,
) -> Path:
    if scope == "user" and platform == "claude" and not upstream:
        claude_config = os.environ.get("CLAUDE_CONFIG_DIR")
        if claude_config:
            return Path(claude_config).expanduser() / "skills" / "graphify" / "SKILL.md"
    root = (target or Path.cwd()).resolve() if scope == "project" else home
    paths = GRAPHIFY["upstreamSkillPaths"] if upstream else GRAPHIFY["skillPaths"]
    return root / str(paths[platform])


def enforce_skill_policy(skill_path: Path, platform: str) -> bool:
    if not skill_path.exists():
        print(f"warning: Graphify did not install expected skill {skill_path}")
        return False

    del platform
    git_requirement = f"git+{GRAPHIFY['gitUrl']}@{GRAPHIFY['commit']}"
    pip_requirement = f"{GRAPHIFY['package']} @ {git_requirement}"
    approval = str(GRAPHIFY["remoteApprovalEnv"])
    policy = (
        f"{POLICY_START}\n"
        "## Framework Pin And Use Boundary\n\n"
        f"This skill is managed at Graphify {GRAPHIFY['version']} commit "
        f"`{GRAPHIFY['commit']}`. Do not auto-upgrade or install an unpinned "
        "Graphify package. The exact reviewed Git requirement below overrides any "
        "generic install example in this skill.\n\n"
        f"`{pip_requirement}`\n\n"
        "Use Graphify for justified repository onboarding, architecture, RCA, "
        "migration, and cross-component work. Skip graph generation for localized "
        "edits, verify graph findings against current source, and follow project "
        "data-handling rules for generated output. Remote semantic backends are "
        f"disabled unless project policy approves them and `{approval}=1`; ambient "
        "credentials alone never authorize source transmission.\n"
        f"{POLICY_END}"
    )

    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        print(f"warning: cannot safely update Graphify frontmatter in {skill_path}")
        return False
    frontmatter, body = text[4:].split("\n---\n", 1)
    lines = frontmatter.splitlines()
    description_lines = [index for index, line in enumerate(lines) if line.startswith("description:")]
    if len(description_lines) != 1:
        print(f"warning: expected one Graphify skill description in {skill_path}")
        return False
    lines[description_lines[0]] = (
        'description: "Use only for repository-scale architecture, relationship tracing, RCA, '
        "migrations, onboarding, cross-component analysis, broad questions over an existing "
        "graphify-out graph, or an explicit /graphify request. Do not use for trivial, localized, "
        'or single-file edits."'
    )
    updated_frontmatter = "\n".join(lines)
    text = f"---\n{updated_frontmatter}\n---\n{body}"

    if POLICY_START in text or POLICY_END in text:
        if text.count(POLICY_START) != 1 or text.count(POLICY_END) != 1:
            print(f"warning: malformed framework Graphify policy in {skill_path}")
            return False
        before, remainder = text.split(POLICY_START, 1)
        _, after = remainder.split(POLICY_END, 1)
        text = before.rstrip() + "\n\n" + policy + "\n\n" + after.lstrip()
    else:
        frontmatter, body = text[4:].split("\n---\n", 1)
        text = f"---\n{frontmatter}\n---\n\n{policy}\n\n{body.lstrip()}"

    replacements = {
        "uv tool install --upgrade graphifyy -q": f"uv tool install --force '{git_requirement}' -q",
        "pip install graphifyy -q": f"pip install '{pip_requirement}' -q",
        '"$PYTHON" -m pip install graphifyy -q': (
            f'"$PYTHON" -m pip install \'{pip_requirement}\' -q'
        ),
        "uv tool run --from graphifyy python": f"uv tool run --from '{git_requirement}' python",
        'if [ -z "$PYTHON" ] && command -v uv >/dev/null 2>&1; then': (
            'if [ -z "$PYTHON" ] && [ -z "$GRAPHIFY_BIN" ] '
            '&& command -v uv >/dev/null 2>&1; then'
        ),
        "uses Gemini **only if** `GEMINI_API_KEY`/`GOOGLE_API_KEY` is already set": (
            f"uses Gemini only when `{approval}=1` and `GEMINI_API_KEY` or "
            "`GOOGLE_API_KEY` is set; ambient keys alone must be ignored"
        ),
        "**Before semantic extraction:** check whether `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set.": (
            f"**Before semantic extraction:** require `{approval}=1`, then check whether "
            "`GEMINI_API_KEY` or `GOOGLE_API_KEY` is set. Ignore ambient keys when the "
            "approval flag is absent."
        ),
        "If neither is set, print this one-liner to the user:": (
            "If approval is absent or a key is unavailable, continue without remote extraction:"
        ),
        "> Tip: set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to use Gemini for semantic extraction "
        "(`pip install 'graphifyy[gemini]'`).": (
            "> Remote extraction is disabled or unavailable; continue without sending project "
            "data to an external backend."
        ),
        "If `GEMINI_API_KEY` or `GOOGLE_API_KEY` IS set, use": (
            f"Only if `{approval}=1` and `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set, use"
        ),
        "When `GEMINI_API_KEY`/`GOOGLE_API_KEY` are unset": (
            f"When `{approval}` is not `1` or `GEMINI_API_KEY`/`GOOGLE_API_KEY` are unset"
        ),
    }

    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
        elif new not in text:
            print(f"warning: reviewed Graphify skill pattern changed in {skill_path}: {old}")
            return False

    video_old = "`pip install 'graphifyy[video]'`"
    video_new = f"`pip install 'graphifyy[video] @ {git_requirement}'`"
    reference_updates: dict[Path, str] = {}
    for reference in skill_path.parent.rglob("*.md"):
        if reference == skill_path:
            continue
        reference_text = reference.read_text(encoding="utf-8")
        if video_old in reference_text:
            reference_text = reference_text.replace(video_old, video_new)
        reference_updates[reference] = reference_text

    forbidden = (
        "--from graphifyy",
        "--upgrade graphifyy",
        "pip install graphifyy -q",
        "Tip: set `GEMINI_API_KEY`",
        "uses Gemini **only if**",
        "If `GEMINI_API_KEY` or `GOOGLE_API_KEY` IS set",
    )
    governed_files = [(skill_path, text), *reference_updates.items()]
    for path, content in governed_files:
        violation = next((pattern for pattern in forbidden if pattern in content), None)
        if violation:
            print(f"warning: unsafe Graphify skill pattern remains in {path}: {violation}")
            return False

    skill_path.write_text(text, encoding="utf-8")
    for reference, content in reference_updates.items():
        reference.write_text(content, encoding="utf-8")

    print(f"enforced reviewed Graphify pin and framework policy in {skill_path}")
    return True


def publish_skill(source: Path, destination: Path) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix=".graphify-staged-", dir=destination.parent))
    staged.rmdir()
    backup: Path | None = None
    try:
        shutil.copytree(source, staged)
        if destination.exists() or destination.is_symlink():
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            candidate = destination.with_name(destination.name + f".backup-{stamp}")
            suffix = 1
            while candidate.exists() or candidate.is_symlink():
                candidate = destination.with_name(destination.name + f".backup-{stamp}-{suffix}")
                suffix += 1
            destination.rename(candidate)
            backup = candidate
        os.replace(staged, destination)
        if backup is not None:
            if backup.is_dir() and not backup.is_symlink():
                shutil.rmtree(backup)
            else:
                backup.unlink()
        print(f"published governed Graphify skill at {destination / 'SKILL.md'}")
        return True
    except OSError as exc:
        print(f"warning: could not publish governed Graphify skill: {exc}")
        if destination.exists() and backup is not None:
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        if backup is not None and backup.exists():
            backup.rename(destination)
        return False
    finally:
        if staged.exists():
            shutil.rmtree(staged)


def retire_legacy_codex_skill(home: Path, final_skill: Path) -> bool:
    legacy_skill = home / str(GRAPHIFY["upstreamSkillPaths"]["codex"])
    if legacy_skill == final_skill or not legacy_skill.exists():
        return True
    legacy_root = legacy_skill.parent
    try:
        body = legacy_skill.read_text(encoding="utf-8")
        if POLICY_START in body:
            shutil.rmtree(legacy_root)
            print(f"removed framework-managed legacy Codex skill {legacy_root}")
            return True
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = legacy_root.with_name(legacy_root.name + f".unmanaged-backup-{stamp}")
        legacy_root.rename(backup)
        print(f"moved unmanaged legacy Codex skill out of the discovery path to {backup}")
        return True
    except OSError as exc:
        print(f"warning: could not retire legacy Codex Graphify skill: {exc}")
        return False


def prepare_graphify_cli(
    home: Path,
    runner: Runner = run,
    dry_run: bool = False,
) -> Path | None:
    if sys.platform not in GRAPHIFY["supportedOperatingSystems"]:
        supported = ", ".join(GRAPHIFY["supportedOperatingSystems"])
        print(f"error: the framework Graphify installer currently supports {supported}; got {sys.platform}")
        return None
    python = find_python(runner)
    if python is None:
        minimum = ".".join(str(part) for part in GRAPHIFY["minimumPython"])
        print(f"error: Graphify requires Python {minimum} or later")
        return None

    tool_root = home / ".local" / "share" / "ai-dev-framework" / "tools" / "graphify"
    destination = tool_root / str(GRAPHIFY["commit"])
    graphify = venv_bin(destination) / ("graphify.exe" if os.name == "nt" else "graphify")
    requirement = f"{GRAPHIFY['package']} @ git+{GRAPHIFY['gitUrl']}@{GRAPHIFY['commit']}"

    if dry_run:
        print(f"would install Graphify {GRAPHIFY['version']} at reviewed commit {GRAPHIFY['commit']}")
        print(f"would run: {python} -m venv {destination}")
        print(f"would install: {requirement}")
        return graphify if expose_commands(destination, home, True) else None

    if install_is_valid(destination, runner):
        print(f"kept reviewed Graphify {GRAPHIFY['version']} at {destination}")
        return graphify if expose_commands(destination, home) else None

    tool_root.mkdir(parents=True, exist_ok=True)
    backup: Path | None = None
    if destination.exists():
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = destination.with_name(destination.name + f".invalid-{stamp}")
        suffix = 1
        while backup.exists():
            backup = destination.with_name(destination.name + f".invalid-{stamp}-{suffix}")
            suffix += 1
        destination.rename(backup)
        print(f"moved invalid Graphify environment to {backup}")

    completed = False
    try:
        commands = [
            [python, "-m", "venv", str(destination)],
            [
                str(venv_bin(destination) / ("python.exe" if os.name == "nt" else "python")),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-input",
                requirement,
            ],
        ]
        for command in commands:
            code, output = runner(command, None, None)
            if code != 0:
                if output:
                    print(output)
                print("warning: could not install reviewed Graphify")
                return None

        metadata = installed_metadata(destination, runner)
        if not metadata_is_valid(metadata):
            print("warning: installed Graphify did not match the reviewed version and commit")
            return None

        code, version_output = runner([str(graphify), "--version"], None, None)
        if code != 0 or str(GRAPHIFY["version"]) not in version_output:
            if version_output:
                print(version_output)
            print("warning: installed Graphify command could not execute at its final path")
            return None

        receipt = {
            "repository": GRAPHIFY["gitUrl"],
            "commit": GRAPHIFY["commit"],
            "version": GRAPHIFY["version"],
        }
        (destination / "ai-dev-framework-install.json").write_text(
            json.dumps(receipt, indent=2) + "\n",
            encoding="utf-8",
        )
        completed = True
        print(f"installed reviewed Graphify {GRAPHIFY['version']} at {destination}")
        if not expose_commands(destination, home):
            return None
        if backup is not None and backup.exists():
            shutil.rmtree(backup)
            print(f"removed invalid Graphify environment {backup}")
        return graphify
    finally:
        if not completed and destination.exists():
            shutil.rmtree(destination)
        if not completed and backup is not None and backup.exists() and not destination.exists():
            backup.rename(destination)
            print(f"restored previous Graphify environment at {destination}")


def install_graphify(
    platform_name: str,
    home: Path,
    *,
    scope: str = "user",
    target: Path | None = None,
    runner: Runner = run,
    dry_run: bool = False,
) -> bool:
    graphify = prepare_graphify_cli(home, runner, dry_run)
    if graphify is None:
        return False

    platform = (
        GRAPHIFY["projectPlatforms"].get(platform_name, GRAPHIFY["platforms"][platform_name])
        if scope == "project"
        else GRAPHIFY["platforms"][platform_name]
    )
    command = [str(graphify), "install"]
    if scope == "project":
        command.append("--project")
    command.extend(["--platform", platform])

    if dry_run:
        requested_target = (target or Path.cwd()).resolve() if scope == "project" else None
        location = f" for {requested_target}" if requested_target else ""
        print(f"would run{location}: {' '.join(command)}")
        print(f"would publish governed skill at {graphify_skill_path(platform, home, scope, target)}")
        return True

    with tempfile.TemporaryDirectory(prefix="ai-dev-framework-graphify-skill-") as tmp:
        staging_root = Path(tmp)
        staging_home = staging_root / "home"
        staging_target = staging_root / "project"
        staging_home.mkdir()
        staging_target.mkdir()
        cwd = staging_target if scope == "project" else None
        env = os.environ.copy()
        env["HOME"] = str(staging_home)
        env.pop("CLAUDE_CONFIG_DIR", None)
        code, output = runner(command, cwd, env)
        if output:
            print(output)
        if code != 0:
            print(f"warning: could not stage Graphify for {platform_name}")
            return False

        staged_skill = graphify_skill_path(
            platform,
            staging_home,
            scope,
            staging_target,
            upstream=True,
        )
        if not enforce_skill_policy(staged_skill, platform):
            print("warning: refusing to publish an ungoverned Graphify skill")
            return False
        final_skill = graphify_skill_path(platform, home, scope, target)
        if not publish_skill(staged_skill.parent, final_skill.parent):
            return False
        if platform == "codex" and scope == "user":
            return retire_legacy_codex_skill(home, final_skill)
        return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the reviewed Graphify CLI and Agent Skill.")
    parser.add_argument("--platform", required=True, choices=sorted(GRAPHIFY["platforms"]))
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--target", type=Path, help="Project root for --scope project")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.target is not None and args.scope != "project":
        parser.error("--target requires --scope project")
    if args.scope == "project" and args.platform != "github-copilot":
        parser.error("project scope is currently supported only for github-copilot")

    installed = install_graphify(
        args.platform,
        args.home.expanduser().resolve(),
        scope=args.scope,
        target=args.target,
        dry_run=args.dry_run,
    )
    return 0 if installed else 1


if __name__ == "__main__":
    raise SystemExit(main())
