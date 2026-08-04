import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import install_framework


class InstructionMergeTests(unittest.TestCase):
    def test_managed_markdown_merge_preserves_existing_content_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "source.md"
            dst = root / "target.md"
            src.write_text("# Framework\n\nRules.\n", encoding="utf-8")
            dst.write_text("# Mine\n\nKeep this.\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                install_framework.merge_managed_markdown(src, dst)
            first = dst.read_text(encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                install_framework.merge_managed_markdown(src, dst)

            self.assertEqual(dst.read_text(encoding="utf-8"), first)
            self.assertIn("Keep this.", first)
            self.assertEqual(first.count(install_framework.MANAGED_START), 1)
            self.assertEqual(first.count(install_framework.MANAGED_END), 1)

    def test_malformed_managed_block_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "source.md"
            dst = root / "target.md"
            src.write_text("Rules.\n", encoding="utf-8")
            dst.write_text(f"{install_framework.MANAGED_START}\nbroken\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                install_framework.merge_managed_markdown(src, dst)

    def test_unchanged_skill_copy_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "source"
            dst = root / "target"
            src.mkdir()
            dst.mkdir()
            (src / "SKILL.md").write_text("same\n", encoding="utf-8")
            (dst / "SKILL.md").write_text("same\n", encoding="utf-8")

            with redirect_stdout(io.StringIO()):
                install_framework.copy_skill(src, dst)

            self.assertEqual(sorted(root.iterdir()), [src, dst])


class CrossAgentInstallTests(unittest.TestCase):
    def test_claude_installs_required_companions_and_ui_plugins(self) -> None:
        calls: list[list[str]] = []

        def runner(cmd: list[str]) -> tuple[int, str]:
            calls.append(cmd)
            return 0, "ok"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_framework.shutil, "which", return_value="/usr/local/bin/claude"
        ), patch.object(
            install_framework,
            "prepare_claude_marketplace",
            side_effect=lambda home, companion, runner, dry_run: home
            / f"{companion['marketplace']}-reviewed",
        ), redirect_stdout(io.StringIO()):
            home = Path(tmp)
            installed = install_framework.install_claude(home, runner)

            self.assertTrue(installed)
            self.assertTrue((home / ".claude" / ".i-have-adhd-always").exists())
            self.assertTrue((home / ".claude" / "skills" / "ai-dev-framework" / "SKILL.md").exists())

        self.assertEqual(len(calls), 8)
        self.assertEqual(calls[-2:], [
            ["claude", "plugin", "install", plugin, "--scope", "user"]
            for plugin in install_framework.PROFILE["uiPlugins"]["claude"]
        ])

    def test_claude_does_not_enable_adhd_when_marketplace_fails(self) -> None:
        calls: list[list[str]] = []

        def runner(cmd: list[str]) -> tuple[int, str]:
            calls.append(cmd)
            return 1, "network unavailable"

        with tempfile.TemporaryDirectory() as tmp, patch.object(
            install_framework.shutil, "which", return_value="/usr/local/bin/claude"
        ), patch.object(
            install_framework,
            "prepare_claude_marketplace",
            side_effect=lambda home, companion, runner, dry_run: home / "reviewed",
        ), redirect_stdout(io.StringIO()):
            home = Path(tmp)
            installed = install_framework.install_claude(
                home,
                runner,
                skip_ponytail=True,
                skip_ui_plugins=True,
            )

            self.assertFalse(installed)
            self.assertFalse((home / ".claude" / ".i-have-adhd-always").exists())
        self.assertEqual(len(calls), 1)

    def test_claude_marketplace_is_fetched_and_verified_at_exact_commit(self) -> None:
        companion = install_framework.PROFILE["companions"]["i-have-adhd"]
        calls: list[list[str]] = []

        def runner(cmd: list[str]) -> tuple[int, str]:
            calls.append(cmd)
            if cmd[-2:] == ["rev-parse", "HEAD"]:
                return 0, companion["commit"]
            return 0, "ok"

        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            destination = install_framework.prepare_claude_marketplace(Path(tmp), companion, runner)

            self.assertIsNotNone(destination)
            self.assertTrue(destination.exists())

        fetch = next(cmd for cmd in calls if "fetch" in cmd)
        self.assertEqual(fetch[-1], companion["commit"])

    def test_claude_marketplace_rejects_unreviewed_existing_checkout(self) -> None:
        companion = install_framework.PROFILE["companions"]["ponytail"]

        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            home = Path(tmp)
            destination = (
                home
                / ".claude"
                / "ai-dev-framework"
                / "marketplaces"
                / f"ponytail-{companion['commit'][:12]}"
            )
            destination.mkdir(parents=True)

            prepared = install_framework.prepare_claude_marketplace(
                home,
                companion,
                lambda cmd: (0, "wrong-revision"),
            )

            self.assertIsNone(prepared)

    def test_copilot_installs_all_portable_companion_skills(self) -> None:
        calls: list[list[str]] = []

        def runner(cmd: list[str]) -> tuple[int, str]:
            calls.append(cmd)
            return 0, "ok"

        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            home = Path(tmp)
            installed = install_framework.install_copilot(home, runner)

            self.assertTrue(installed)
            self.assertTrue((home / ".copilot" / "skills" / "ai-dev-framework" / "SKILL.md").exists())

        expected_skills = sum(
            len(companion["copilotSkills"])
            for companion in install_framework.PROFILE["companions"].values()
        )
        self.assertEqual(len(calls), 1 + expected_skills)
        self.assertEqual(calls[0], ["gh", "skill", "--help"])
        self.assertTrue(all("--pin" in cmd for cmd in calls[1:]))
        reviewed_commits = {
            companion["commit"] for companion in install_framework.PROFILE["companions"].values()
        }
        self.assertTrue(all(cmd[cmd.index("--pin") + 1] in reviewed_commits for cmd in calls[1:]))

    def test_copilot_project_scope_installs_repo_visible_skills(self) -> None:
        calls: list[list[str]] = []

        def runner(cmd: list[str]) -> tuple[int, str]:
            calls.append(cmd)
            return 0, "ok"

        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            root = Path(tmp)
            target = root / "project"
            installed = install_framework.install_copilot(
                root / "home",
                runner,
                scope="project",
                target=target,
            )

            self.assertTrue(installed)
            self.assertTrue((target / ".agents" / "skills" / "ai-dev-framework" / "SKILL.md").exists())
            self.assertTrue((target / ".github" / "copilot-instructions.md").exists())

        skill_dir = str((target / ".agents" / "skills").resolve())
        self.assertTrue(all(cmd[cmd.index("--dir") + 1] == skill_dir for cmd in calls[1:]))

    def test_dry_run_does_not_write_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()):
            home = Path(tmp)
            installed = install_framework.install_claude(home, dry_run=True)

            self.assertTrue(installed)
            self.assertEqual(list(home.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
