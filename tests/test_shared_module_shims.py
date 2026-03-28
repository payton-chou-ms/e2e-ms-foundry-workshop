import importlib.util
import sys
import unittest
from pathlib import Path


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


class SharedModuleShimTests(unittest.TestCase):
    def test_load_env_root_module_reexports_shared_implementation(self):
        root_module = load_script_module("load_env.py", "root_load_env")

        self.assertEqual(root_module.load_all_env.__module__, "shared.load_env")
        self.assertEqual(root_module.get_required_env.__module__, "shared.load_env")

    def test_scenario_utils_root_module_reexports_shared_implementation(self):
        root_module = load_script_module("scenario_utils.py", "root_scenario_utils")

        self.assertEqual(root_module.resolve_scenario.__module__, "shared.scenario_utils")
        self.assertEqual(root_module.resolve_data_paths.__module__, "shared.scenario_utils")


if __name__ == "__main__":
    unittest.main()