import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import bootstrap_project


class BootstrapProjectTests(unittest.TestCase):
    def test_bootstrap_creates_cross_agent_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(
            sys, "argv", ["bootstrap_project.py", tmp]
        ), redirect_stdout(io.StringIO()):
            result = bootstrap_project.main()
            target = Path(tmp)

            self.assertEqual(result, 0)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "CLAUDE.md").exists())
            self.assertTrue((target / ".github" / "copilot-instructions.md").exists())
            self.assertTrue((target / "PROJECT_CHARTER.md").exists())
            self.assertIn(
                "graphify-out/",
                (target / ".gitignore").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Ponytail, i-have-adhd, and Graphify",
                (target / "AGENTS.md").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
