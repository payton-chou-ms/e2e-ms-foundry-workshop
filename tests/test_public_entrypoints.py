import importlib.util
import sys
import unittest
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


class PublicEntrypointTests(unittest.TestCase):
    def test_admin_prepare_shared_demo_skips_fabric_by_default(self):
        module = load_script_module(
            "admin_prepare_shared_demo.py",
            "admin_prepare_shared_demo",
        )

        command = module.build_command(["--scenarios", "default"])

        self.assertEqual(Path(command[1]).parts[-2:], ("internal", "prepare_demo.py"))
        self.assertEqual(command[2:], ["--skip-fabric", "--scenarios", "default"])

    def test_admin_prepare_shared_demo_allows_explicit_fabric_opt_in(self):
        module = load_script_module(
            "admin_prepare_shared_demo.py",
            "admin_prepare_shared_demo_opt_in",
        )

        command = module.build_command(["--with-fabric", "--scenarios", "default"])

        self.assertEqual(Path(command[1]).parts[-2:], ("internal", "prepare_demo.py"))
        self.assertEqual(command[2:], ["--scenarios", "default"])

    def test_admin_prepare_docs_demo_builds_foundry_only_command(self):
        module = load_script_module(
            "admin_prepare_docs_demo.py",
            "admin_prepare_docs_demo",
        )

        command = module.build_command(["--scenario", "default"])

        self.assertEqual(command[0], sys.executable)
        self.assertEqual(Path(command[1]).parts[-2:], ("internal", "prepare_demo.py"))
        self.assertEqual(
            command[2:],
            ["--mode", "foundry-only", "--scenario", "default"],
        )

    def test_admin_prepare_docs_data_demo_defaults_to_full_from_step_02(self):
        module = load_script_module(
            "admin_prepare_docs_data_demo.py",
            "admin_prepare_docs_data_demo",
        )

        command = module.build_command([])

        self.assertEqual(Path(command[1]).parts[-2:], ("internal", "prepare_demo.py"))
        self.assertEqual(command[2:], ["--mode", "full", "--from-step", "02"])

    def test_participant_validate_docs_builds_foundry_only_test_command(self):
        module = load_script_module(
            "participant_validate_docs.py",
            "participant_validate_docs",
        )

        command = module.build_command(["--agent-id", "agent-123"])

        self.assertEqual(Path(command[1]).parts[-3:], ("pipelines", "agents", "test_workshop_agent.py"))
        self.assertEqual(command[2:], ["--foundry-only", "--agent-id", "agent-123"])

    def test_author_rebuild_custom_poc_builds_clean_full_command(self):
        module = load_script_module(
            "author_rebuild_custom_poc.py",
            "author_rebuild_custom_poc",
        )

        command = module.build_command(["--industry", "Insurance"])

        self.assertEqual(Path(command[1]).parts[-2:], ("internal", "prepare_demo.py"))
        self.assertEqual(
            command[2:],
            ["--mode", "full", "--clean", "--industry", "Insurance"],
        )

    def test_entrypoint_main_delegates_to_run_command(self):
        module = load_script_module(
            "participant_validate_foundry_iq.py",
            "participant_validate_foundry_iq",
        )

        with patch.object(module, "run_command", return_value=0) as run_command:
            exit_code = module.main(["--agent-name", "demo-agent"])

        self.assertEqual(exit_code, 0)
        run_command.assert_called_once()
        delegated_command = run_command.call_args.args[0]
        self.assertEqual(Path(delegated_command[1]).parts[-3:], ("pipelines", "agents", "test_foundry_iq_agent.py"))
        self.assertEqual(delegated_command[2:], ["--agent-name", "demo-agent"])


if __name__ == "__main__":
    unittest.main()