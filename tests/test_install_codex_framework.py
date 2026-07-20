import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import call, patch

from scripts import install_codex_framework


class PluginInstallTests(unittest.TestCase):
    @patch.object(install_codex_framework, "run")
    def test_i_have_adhd_uses_codex_marketplace_and_plugin_commands(self, run) -> None:
        revision = install_codex_framework.I_HAVE_ADHD_REVIEWED_REVISION
        run.side_effect = [
            (0, f"{revision}\trefs/heads/main"),
            (0, "marketplace added"),
            (0, "plugin added"),
            (0, revision),
        ]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertTrue(installed)
        self.assertEqual(
            run.call_args_list,
            [
                call(
                    [
                        "git",
                        "ls-remote",
                        install_codex_framework.I_HAVE_ADHD_REPOSITORY,
                        "refs/heads/main",
                    ]
                ),
                call(
                    [
                        "codex",
                        "plugin",
                        "marketplace",
                        "add",
                        "ayghri/i-have-adhd",
                        "--ref",
                        "main",
                    ]
                ),
                call(["codex", "plugin", "add", "i-have-adhd@i-have-adhd"]),
                call(
                    [
                        "git",
                        "-C",
                        str(
                            install_codex_framework.CODEX_HOME
                            / "plugins"
                            / "cache"
                            / "i-have-adhd"
                            / "i-have-adhd"
                            / "0.1.0"
                        ),
                        "rev-parse",
                        "HEAD",
                    ]
                ),
            ],
        )

    @patch.object(install_codex_framework, "run")
    def test_marketplace_failure_does_not_attempt_plugin_install(self, run) -> None:
        revision = install_codex_framework.I_HAVE_ADHD_REVIEWED_REVISION
        run.side_effect = [(0, revision), (1, "network unavailable")]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        self.assertEqual(run.call_count, 2)

    @patch.object(install_codex_framework, "run")
    def test_plugin_failure_is_reported(self, run) -> None:
        revision = install_codex_framework.I_HAVE_ADHD_REVIEWED_REVISION
        run.side_effect = [(0, revision), (0, "marketplace added"), (1, "install failed")]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)

    @patch.object(install_codex_framework, "run")
    def test_already_installed_is_successful(self, run) -> None:
        revision = install_codex_framework.I_HAVE_ADHD_REVIEWED_REVISION
        run.side_effect = [
            (0, revision),
            (1, "already configured"),
            (1, "already installed"),
            (0, revision),
        ]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertTrue(installed)

    @patch.object(install_codex_framework, "run")
    def test_unreviewed_upstream_revision_stops_before_install(self, run) -> None:
        run.return_value = (0, "different-revision\trefs/heads/main")

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        run.assert_called_once()

    @patch.object(install_codex_framework, "run")
    def test_unreviewed_installed_revision_is_removed(self, run) -> None:
        revision = install_codex_framework.I_HAVE_ADHD_REVIEWED_REVISION
        run.side_effect = [
            (0, revision),
            (0, "marketplace added"),
            (0, "plugin added"),
            (0, "different-revision"),
            (0, "plugin removed"),
            (0, '{"installed": []}'),
        ]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        self.assertEqual(
            run.call_args_list[-2],
            call(["codex", "plugin", "remove", "i-have-adhd@i-have-adhd"]),
        )

    @patch.object(install_codex_framework, "run")
    def test_unreviewed_plugin_removal_failure_is_reported(self, run) -> None:
        revision = install_codex_framework.I_HAVE_ADHD_REVIEWED_REVISION
        plugin_state = {
            "installed": [
                {
                    "pluginId": "i-have-adhd@i-have-adhd",
                    "enabled": True,
                }
            ]
        }
        run.side_effect = [
            (0, revision),
            (0, "marketplace added"),
            (0, "plugin added"),
            (0, "different-revision"),
            (1, "remove failed"),
            (0, json.dumps(plugin_state)),
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        self.assertIn("could not confirm", output.getvalue())
        self.assertEqual(
            run.call_args_list[-1],
            call(["codex", "plugin", "list", "--json"]),
        )

    def test_skip_i_have_adhd_does_not_call_installer(self) -> None:
        with (
            patch.object(sys, "argv", ["install_codex_framework.py", "--skip-i-have-adhd"]),
            patch.object(install_codex_framework, "install_global_agents"),
            patch.object(install_codex_framework, "install_skill"),
            patch.object(install_codex_framework, "install_agents"),
            patch.object(install_codex_framework, "ensure_config"),
            patch.object(install_codex_framework, "install_ponytail", return_value=True),
            patch.object(install_codex_framework, "install_i_have_adhd") as install_i_have_adhd,
            redirect_stdout(io.StringIO()),
        ):
            result = install_codex_framework.main()

        self.assertEqual(result, 0)
        install_i_have_adhd.assert_not_called()

    def test_plugin_failure_makes_main_fail(self) -> None:
        with (
            patch.object(sys, "argv", ["install_codex_framework.py", "--skip-ponytail"]),
            patch.object(install_codex_framework, "install_global_agents"),
            patch.object(install_codex_framework, "install_skill"),
            patch.object(install_codex_framework, "install_agents"),
            patch.object(install_codex_framework, "ensure_config"),
            patch.object(install_codex_framework, "install_i_have_adhd", return_value=False),
            redirect_stdout(io.StringIO()),
        ):
            result = install_codex_framework.main()

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
