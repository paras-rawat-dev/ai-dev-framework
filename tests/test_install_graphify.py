from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import install_graphify


class GraphifyInstallTests(unittest.TestCase):
    def metadata(self) -> str:
        return json.dumps(
            {
                "version": install_graphify.GRAPHIFY["version"],
                "direct_url": {
                    "url": install_graphify.GRAPHIFY["gitUrl"],
                    "vcs_info": {
                        "vcs": "git",
                        "requested_revision": install_graphify.GRAPHIFY["commit"],
                        "commit_id": install_graphify.GRAPHIFY["commit"],
                    },
                },
            }
        )

    def test_metadata_validation_rejects_a_different_source(self) -> None:
        metadata = json.loads(self.metadata())
        self.assertTrue(install_graphify.metadata_is_valid(metadata))
        metadata["direct_url"]["url"] = "https://example.com/not-graphify.git"
        self.assertFalse(install_graphify.metadata_is_valid(metadata))

    def test_command_wrapper_blocks_ambient_remote_credentials(self) -> None:
        wrapper = install_graphify.command_wrapper(Path("/managed/graphify"), "graphify")

        self.assertIn(install_graphify.GRAPHIFY["remoteApprovalEnv"], wrapper)
        for key in install_graphify.REMOTE_ENV_KEYS:
            self.assertIn(key, wrapper)

    def test_python_discovery_includes_python_314(self) -> None:
        def which(candidate: str) -> str | None:
            return "/usr/local/bin/python3.14" if candidate == "python3.14" else None

        with patch.dict(os.environ, {"GRAPHIFY_PYTHON": ""}), patch.object(
            install_graphify.shutil,
            "which",
            side_effect=which,
        ):
            candidates = install_graphify.python_candidates()

        self.assertEqual(candidates[0], "/usr/local/bin/python3.14")

    def test_unsupported_operating_system_fails_before_install(self) -> None:
        calls: list[list[str]] = []

        def runner(
            cmd: list[str], cwd: Path | None, env: dict[str, str] | None
        ) -> tuple[int, str]:
            calls.append(cmd)
            return 0, "unexpected"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_graphify.sys,
            "platform",
            "win32",
        ), redirect_stdout(io.StringIO()):
            graphify = install_graphify.prepare_graphify_cli(Path(tmp), runner)

        self.assertIsNone(graphify)
        self.assertEqual(calls, [])

    def test_codex_skill_uses_documented_global_agent_skill_path(self) -> None:
        home = Path("/home/developer")
        path = install_graphify.graphify_skill_path("codex", home, "user", None)

        self.assertEqual(path, home / ".agents" / "skills" / "graphify" / "SKILL.md")

    @unittest.skipIf(os.name == "nt", "symlink assertion is POSIX-specific")
    def test_cli_installs_exact_reviewed_commit_in_isolated_environment(self) -> None:
        calls: list[list[str]] = []

        def runner(
            cmd: list[str], cwd: Path | None, env: dict[str, str] | None
        ) -> tuple[int, str]:
            calls.append(cmd)
            if cmd[1:3] == ["-m", "venv"]:
                binary_dir = install_graphify.venv_bin(Path(cmd[-1]))
                binary_dir.mkdir(parents=True)
                for name in ("python", "graphify", "graphify-mcp"):
                    (binary_dir / name).write_text("stub\n", encoding="utf-8")
            if len(cmd) > 1 and cmd[1] == "-c":
                return 0, self.metadata()
            if cmd[-1:] == ["--version"]:
                return 0, f"graphify {install_graphify.GRAPHIFY['version']}"
            return 0, "ok"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_graphify, "find_python", return_value="/python3.11"
        ), redirect_stdout(io.StringIO()):
            home = Path(tmp)
            graphify = install_graphify.prepare_graphify_cli(home, runner)

            self.assertIsNotNone(graphify)
            self.assertTrue(graphify.exists())
            exposed = home / ".local" / "bin" / "graphify"
            self.assertTrue(exposed.exists())
            self.assertFalse(exposed.is_symlink())
            wrapper = exposed.read_text(encoding="utf-8")
            self.assertIn(install_graphify.COMMAND_MARKER, wrapper)
            self.assertIn(str(graphify.parent / "python"), wrapper)

        pip_install = next(cmd for cmd in calls if cmd[1:3] == ["-m", "pip"])
        venv_install = next(cmd for cmd in calls if cmd[1:3] == ["-m", "venv"])
        self.assertEqual(Path(venv_install[-1]), graphify.parent.parent)
        requirement = pip_install[-1]
        self.assertIn(install_graphify.GRAPHIFY["commit"], requirement)
        self.assertIn(install_graphify.GRAPHIFY["gitUrl"], requirement)

    def test_platform_registration_uses_home_and_native_codex_skill(self) -> None:
        calls: list[tuple[list[str], Path | None, dict[str, str] | None]] = []

        def runner(
            cmd: list[str], cwd: Path | None, env: dict[str, str] | None
        ) -> tuple[int, str]:
            calls.append((cmd, cwd, env))
            return 0, "installed"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_graphify,
            "prepare_graphify_cli",
            return_value=Path(tmp) / "bin" / "graphify",
        ), patch.object(
            install_graphify,
            "enforce_skill_policy",
            return_value=True,
        ), patch.object(
            install_graphify,
            "publish_skill",
            return_value=True,
        ), redirect_stdout(io.StringIO()):
            home = Path(tmp) / "home"
            installed = install_graphify.install_graphify("codex", home, runner=runner)

        self.assertTrue(installed)
        command, cwd, env = calls[0]
        self.assertEqual(command[-3:], ["install", "--platform", "codex"])
        self.assertIsNone(cwd)
        self.assertNotEqual(env["HOME"], str(home))

    def test_failed_cli_replacement_restores_previous_environment(self) -> None:
        def runner(
            cmd: list[str], cwd: Path | None, env: dict[str, str] | None
        ) -> tuple[int, str]:
            return 1, "simulated install failure"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_graphify,
            "find_python",
            return_value="/python3.11",
        ), redirect_stdout(io.StringIO()):
            home = Path(tmp)
            destination = (
                home
                / ".local"
                / "share"
                / "ai-dev-framework"
                / "tools"
                / "graphify"
                / install_graphify.GRAPHIFY["commit"]
            )
            destination.mkdir(parents=True)
            marker = destination / "previous-install.txt"
            marker.write_text("preserve me\n", encoding="utf-8")

            graphify = install_graphify.prepare_graphify_cli(home, runner)

            self.assertIsNone(graphify)
            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve me\n")
            self.assertEqual(list(destination.parent.glob("*.invalid-*")), [])

    def test_copilot_project_scope_uses_portable_agent_skill_path(self) -> None:
        calls: list[tuple[list[str], Path | None, dict[str, str] | None]] = []

        def runner(
            cmd: list[str], cwd: Path | None, env: dict[str, str] | None
        ) -> tuple[int, str]:
            calls.append((cmd, cwd, env))
            return 0, "installed"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_graphify,
            "prepare_graphify_cli",
            return_value=Path(tmp) / "bin" / "graphify",
        ), patch.object(
            install_graphify,
            "enforce_skill_policy",
            return_value=True,
        ), patch.object(
            install_graphify,
            "publish_skill",
            return_value=True,
        ), redirect_stdout(io.StringIO()):
            root = Path(tmp)
            target = root / "project"
            installed = install_graphify.install_graphify(
                "github-copilot",
                root / "home",
                scope="project",
                target=target,
                runner=runner,
            )

        self.assertTrue(installed)
        command, cwd, _ = calls[0]
        self.assertEqual(command[-4:], ["install", "--project", "--platform", "agents"])
        self.assertNotEqual(cwd, target.resolve())

    @unittest.skipIf(os.name == "nt", "symlink assertion is POSIX-specific")
    def test_unmanaged_global_command_is_not_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            install_root = root / "install"
            binary_dir = install_graphify.venv_bin(install_root)
            binary_dir.mkdir(parents=True)
            for name in install_graphify.GRAPHIFY["commands"]:
                (binary_dir / name).write_text("managed\n", encoding="utf-8")
            command = root / "home" / ".local" / "bin" / "graphify"
            command.parent.mkdir(parents=True)
            command.write_text("user-owned\n", encoding="utf-8")

            exposed = install_graphify.expose_commands(install_root, root / "home")

            self.assertFalse(exposed)
            self.assertEqual(command.read_text(encoding="utf-8"), "user-owned\n")

    @unittest.skipIf(os.name == "nt", "symlink assertion is POSIX-specific")
    def test_managed_command_link_moves_to_new_reviewed_environment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            home = Path(tmp) / "home"
            managed_root = home / ".local" / "share" / "ai-dev-framework" / "tools" / "graphify"
            old_root = managed_root / "old"
            new_root = managed_root / "new"
            for root in (old_root, new_root):
                binary_dir = install_graphify.venv_bin(root)
                binary_dir.mkdir(parents=True)
                for name in install_graphify.GRAPHIFY["commands"]:
                    (binary_dir / name).write_text("managed\n", encoding="utf-8")
            command = home / ".local" / "bin" / "graphify"
            command.parent.mkdir(parents=True)
            command.symlink_to(install_graphify.venv_bin(old_root) / "graphify")

            exposed = install_graphify.expose_commands(new_root, home)

            self.assertTrue(exposed)
            self.assertFalse(command.is_symlink())
            self.assertIn(str(install_graphify.venv_bin(new_root)), command.read_text(encoding="utf-8"))

    def test_installed_skill_self_install_commands_are_pinned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            skill = Path(tmp) / "graphify" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "---\nname: graphify\ndescription: test\n---\n\n"
                "if [ -z \"$PYTHON\" ] && command -v uv >/dev/null 2>&1; then\n"
                "uv tool run --from graphifyy python\n"
                "uv tool install --upgrade graphifyy -q\n"
                '"$PYTHON" -m pip install graphifyy -q\n'
                "uses Gemini **only if** `GEMINI_API_KEY`/`GOOGLE_API_KEY` is already set\n"
                "**Before semantic extraction:** check whether `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set.\n"
                "If neither is set, print this one-liner to the user:\n"
                "> Tip: set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to use Gemini for semantic extraction (`pip install 'graphifyy[gemini]'`).\n"
                "If `GEMINI_API_KEY` or `GOOGLE_API_KEY` IS set, use remote extraction.\n"
                "When `GEMINI_API_KEY`/`GOOGLE_API_KEY` are unset, stay local.\n",
                encoding="utf-8",
            )

            enforced = install_graphify.enforce_skill_policy(skill, "codex")
            body = skill.read_text(encoding="utf-8")

        self.assertTrue(enforced)
        self.assertIn(install_graphify.POLICY_START, body)
        self.assertIn(install_graphify.GRAPHIFY["commit"], body)
        self.assertNotIn("--from graphifyy", body)
        self.assertNotIn("--upgrade graphifyy", body)
        self.assertNotIn("pip install graphifyy -q", body)
        self.assertIn(install_graphify.GRAPHIFY["remoteApprovalEnv"], body)
        self.assertIn("Do not use for trivial, localized", body)
        self.assertNotIn("Tip: set `GEMINI_API_KEY`", body)

    def test_skill_publish_replaces_only_after_staging(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            source = root / "source"
            destination = root / "skills" / "graphify"
            source.mkdir()
            destination.mkdir(parents=True)
            (source / "SKILL.md").write_text("governed\n", encoding="utf-8")
            (destination / "SKILL.md").write_text("previous\n", encoding="utf-8")

            published = install_graphify.publish_skill(source, destination)

            self.assertTrue(published)
            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), "governed\n")

    def test_skill_publish_restores_previous_skill_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_graphify.os,
            "replace",
            side_effect=OSError("simulated publish failure"),
        ), redirect_stdout(io.StringIO()):
            root = Path(tmp)
            source = root / "source"
            destination = root / "skills" / "graphify"
            source.mkdir()
            destination.mkdir(parents=True)
            (source / "SKILL.md").write_text("governed\n", encoding="utf-8")
            (destination / "SKILL.md").write_text("previous\n", encoding="utf-8")

            published = install_graphify.publish_skill(source, destination)

            self.assertFalse(published)
            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), "previous\n")

    def test_skill_publish_preserves_previous_skill_when_backup_rename_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            source = root / "source"
            destination = root / "skills" / "graphify"
            source.mkdir()
            destination.mkdir(parents=True)
            (source / "SKILL.md").write_text("governed\n", encoding="utf-8")
            (destination / "SKILL.md").write_text("previous\n", encoding="utf-8")

            with patch.object(Path, "rename", side_effect=OSError("simulated rename failure")):
                published = install_graphify.publish_skill(source, destination)

            self.assertFalse(published)
            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), "previous\n")


if __name__ == "__main__":
    unittest.main()
