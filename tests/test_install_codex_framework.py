import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import call, patch

from scripts import install_codex_framework


class PluginInstallTests(unittest.TestCase):
    def successful_install_outputs(self, revision: str) -> list[tuple[int, str]]:
        return [
            (1, "not installed"),
            (1, "not found"),
            (1, "not installed"),
            (1, "not found"),
            (0, "marketplace added"),
            (0, "plugin added"),
            (0, revision),
        ]

    def test_managed_marketplaces_match_reviewed_profile(self) -> None:
        for companion in install_codex_framework.PROFILE["companions"].values():
            with self.subTest(companion=companion["marketplace"]):
                self.assertTrue(install_codex_framework.managed_marketplace_is_valid(companion))

    @patch.object(install_codex_framework, "run")
    def test_i_have_adhd_installs_from_managed_pinned_marketplace(self, run) -> None:
        companion = install_codex_framework.I_HAVE_ADHD
        run.side_effect = self.successful_install_outputs(str(companion["commit"]))

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertTrue(installed)
        marketplace_root = install_codex_framework.ROOT / str(companion["codexMarketplacePath"])
        self.assertIn(
            call(["codex", "plugin", "marketplace", "add", str(marketplace_root)]),
            run.call_args_list,
        )
        self.assertIn(
            call(["codex", "plugin", "add", companion["codexPluginId"]]),
            run.call_args_list,
        )
        self.assertIn(
            call(["codex", "plugin", "remove", companion["pluginId"]]),
            run.call_args_list,
        )

    @patch.object(install_codex_framework, "run")
    def test_ponytail_installs_reviewed_revision(self, run) -> None:
        companion = install_codex_framework.PONYTAIL
        run.side_effect = self.successful_install_outputs(str(companion["commit"]))

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_ponytail()

        self.assertTrue(installed)
        expected_cache = (
            install_codex_framework.CODEX_HOME
            / "plugins"
            / "cache"
            / str(companion["codexMarketplace"])
            / "ponytail"
            / str(companion["version"])
        )
        self.assertEqual(
            run.call_args_list[-1],
            call(["git", "-C", str(expected_cache), "rev-parse", "HEAD"]),
        )

    @patch.object(install_codex_framework, "run")
    def test_invalid_local_marketplace_stops_before_commands(self, run) -> None:
        with patch.object(install_codex_framework, "managed_marketplace_is_valid", return_value=False), redirect_stdout(
            io.StringIO()
        ):
            installed = install_codex_framework.install_ponytail()

        self.assertFalse(installed)
        run.assert_not_called()

    @patch.object(install_codex_framework, "run")
    def test_legacy_marketplace_removal_failure_stops_install(self, run) -> None:
        run.side_effect = [(1, "permission denied"), (1, "not found")]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        self.assertEqual(run.call_count, 2)

    @patch.object(install_codex_framework, "run")
    def test_marketplace_failure_does_not_attempt_plugin_install(self, run) -> None:
        run.side_effect = [
            (1, "not installed"),
            (1, "not found"),
            (1, "not installed"),
            (1, "not found"),
            (1, "network unavailable"),
        ]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        self.assertEqual(run.call_count, 5)

    @patch.object(install_codex_framework, "run")
    def test_unreviewed_plugin_is_removed_with_managed_marketplace(self, run) -> None:
        companion = install_codex_framework.I_HAVE_ADHD
        run.side_effect = self.successful_install_outputs("wrong-revision") + [
            (0, "plugin removed"),
            (0, "marketplace removed"),
        ]

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_i_have_adhd()

        self.assertFalse(installed)
        self.assertEqual(
            run.call_args_list[-2:],
            [
                call(["codex", "plugin", "remove", companion["codexPluginId"]]),
                call(
                    [
                        "codex",
                        "plugin",
                        "marketplace",
                        "remove",
                        companion["codexMarketplace"],
                    ]
                ),
            ],
        )

    @patch.object(install_codex_framework, "run")
    def test_ui_plugins_are_installed_from_profile(self, run) -> None:
        run.return_value = (0, "installed")

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_ui_plugins()

        self.assertTrue(installed)
        self.assertEqual(
            run.call_args_list,
            [call(["codex", "plugin", "add", plugin]) for plugin in install_codex_framework.CODEX_UI_PLUGINS],
        )

    def test_skip_flags_do_not_call_plugin_installers(self) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "install_codex_framework.py",
                    "--skip-ponytail",
                    "--skip-i-have-adhd",
                    "--skip-graphify",
                    "--skip-ui-plugins",
                ],
            ),
            patch.object(install_codex_framework, "install_global_agents"),
            patch.object(install_codex_framework, "install_skill"),
            patch.object(install_codex_framework, "install_agents"),
            patch.object(install_codex_framework, "ensure_config"),
            patch.object(install_codex_framework, "install_ponytail") as install_ponytail,
            patch.object(install_codex_framework, "install_i_have_adhd") as install_i_have_adhd,
            patch.object(install_codex_framework, "install_graphify") as install_graphify,
            patch.object(install_codex_framework, "install_ui_plugins") as install_ui_plugins,
            redirect_stdout(io.StringIO()),
        ):
            result = install_codex_framework.main()

        self.assertEqual(result, 0)
        install_ponytail.assert_not_called()
        install_i_have_adhd.assert_not_called()
        install_graphify.assert_not_called()
        install_ui_plugins.assert_not_called()

    def test_plugin_failure_makes_main_fail(self) -> None:
        with (
            patch.object(
                sys,
                "argv",
                [
                    "install_codex_framework.py",
                    "--skip-ponytail",
                    "--skip-graphify",
                    "--skip-ui-plugins",
                ],
            ),
            patch.object(install_codex_framework, "install_global_agents"),
            patch.object(install_codex_framework, "install_skill"),
            patch.object(install_codex_framework, "install_agents"),
            patch.object(install_codex_framework, "ensure_config"),
            patch.object(install_codex_framework, "install_i_have_adhd", return_value=False),
            redirect_stdout(io.StringIO()),
        ):
            result = install_codex_framework.main()

        self.assertEqual(result, 1)

    @patch.object(install_codex_framework, "run")
    def test_graphify_failure_is_reported_as_incomplete_setup(self, run) -> None:
        run.return_value = (1, "network unavailable")

        with redirect_stdout(io.StringIO()):
            installed = install_codex_framework.install_graphify()

        self.assertFalse(installed)
        self.assertIn("install_graphify.py", run.call_args.args[0][1])


if __name__ == "__main__":
    unittest.main()
