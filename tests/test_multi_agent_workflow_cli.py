import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT_PATH = SCRIPTS_DIR / "15_test_multi_agent_workflow.py"
LEGACY_SCRIPT_PATH = SCRIPTS_DIR / "14_create_multi_agent_workflow.py"


def load_workflow_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(
        "multi_agent_workflow_script",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError("Failed to load script module")
    spec.loader.exec_module(module)
    return module


class MultiAgentWorkflowCliTests(unittest.TestCase):
    def assert_parse_rejected(self, module, argv):
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as error:
                module.parse_args(argv)
        self.assertNotEqual(error.exception.code, 0)

    def test_help_describes_single_script_demo_without_legacy_flags(self):
        module = load_workflow_module()
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as error:
                module.parse_args(["--help"])

        self.assertEqual(error.exception.code, 0)
        help_text = stdout.getvalue()
        self.assertIn("Single-entry multi-agent demo", help_text)
        self.assertNotIn("--create-only", help_text)
        self.assertNotIn("--reuse-existing", help_text)

    def test_legacy_create_only_flag_is_rejected(self):
        module = load_workflow_module()
        self.assert_parse_rejected(module, ["--create-only"])

    def test_legacy_reuse_existing_flag_is_rejected(self):
        module = load_workflow_module()
        self.assert_parse_rejected(module, ["--reuse-existing"])

    def test_scenario_all_is_rejected(self):
        module = load_workflow_module()
        self.assert_parse_rejected(module, ["--scenario", "all"])

    def test_legacy_create_script_is_removed(self):
        self.assertFalse(LEGACY_SCRIPT_PATH.exists())


if __name__ == "__main__":
    unittest.main()
