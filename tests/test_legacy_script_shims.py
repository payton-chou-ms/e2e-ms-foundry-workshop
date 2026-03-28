import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_script_module(script_name: str, module_name: str):
    sys.path.insert(0, str(SCRIPTS_DIR))
    script_path = SCRIPTS_DIR / script_name
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover - defensive guard
        raise RuntimeError(f"Failed to load {script_name}")
    spec.loader.exec_module(module)
    return module


class LegacyScriptShimTests(unittest.TestCase):
    def test_legacy_fabric_agent_script_delegates_to_legacy_location(self):
        module = load_script_module("05_create_fabric_agent.py", "legacy_fabric_agent")

        command = module.build_command(["--scenario", "default"])

        self.assertEqual(Path(command[1]).parts[-2:], ("legacy", "create_fabric_data_agent.py"))
        self.assertEqual(command[2:], ["--scenario", "default"])

    def test_legacy_prepare_script_delegates_to_internal_prepare_demo(self):
        module = load_script_module("00_admin_prepare_demo.py", "legacy_prepare_demo")

        command = module.build_command(["--mode", "shared"])

        self.assertEqual(Path(command[1]).parts[-2:], ("internal", "prepare_demo.py"))
        self.assertEqual(command[2:], ["--mode", "shared"])

    def test_legacy_foundry_agent_test_script_prints_deprecation_notice(self):
        module = load_script_module("08_test_foundry_agent.py", "legacy_test_workshop_agent")
        stdout = io.StringIO()

        with patch.object(module, "run_command", return_value=0):
            with redirect_stdout(stdout):
                exit_code = module.main(["--foundry-only"])

        self.assertEqual(exit_code, 0)
        self.assertIn("deprecated", stdout.getvalue().lower())
        self.assertIn("participant_validate_docs.py", stdout.getvalue())

    def test_legacy_foundry_iq_test_script_delegates_to_pipeline_location(self):
        module = load_script_module("08b_test_foundry_iq_agent.py", "legacy_test_foundry_iq_agent")

        command = module.build_command(["--scenario", "default"])

        self.assertEqual(Path(command[1]).parts[-3:], ("pipelines", "agents", "test_foundry_iq_agent.py"))
        self.assertEqual(command[2:], ["--scenario", "default"])


if __name__ == "__main__":
    unittest.main()