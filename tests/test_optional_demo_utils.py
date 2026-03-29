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


class OptionalDemoUtilsTests(unittest.TestCase):
    def test_format_env_source_returns_plain_name_for_primary_variable(self):
        module = load_script_module("optional_demo_utils.py", "optional_demo_utils_primary")

        source = module.format_env_source(
            "CONTENTUNDERSTANDING_ENDPOINT",
            "AZURE_AI_ENDPOINT",
        )

        self.assertEqual(source, "CONTENTUNDERSTANDING_ENDPOINT")

    def test_format_env_source_explicitly_marks_generic_fallback(self):
        module = load_script_module("optional_demo_utils.py", "optional_demo_utils_fallback")

        source = module.format_env_source(
            "AZURE_AI_ENDPOINT",
            "AZURE_AI_ENDPOINT",
        )

        self.assertEqual(
            source,
            "AZURE_AI_ENDPOINT（優先使用的專用變數未設，已 fallback 到 AZURE_AI_ENDPOINT）",
        )

    def test_format_env_source_marks_shared_openai_fallback(self):
        module = load_script_module("optional_demo_utils.py", "optional_demo_utils_openai_fallback")

        source = module.format_env_source(
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_AI_ENDPOINT",
        )

        self.assertEqual(
            source,
            "AZURE_OPENAI_ENDPOINT（優先使用的專用變數未設，已 fallback 到 AZURE_OPENAI_ENDPOINT）",
        )

    def test_format_env_source_does_not_mark_specialized_alias_as_fallback(self):
        module = load_script_module("optional_demo_utils.py", "optional_demo_utils_alias")

        source = module.format_env_source(
            "CONTENT_UNDERSTANDING_ENDPOINT",
            "AZURE_AI_ENDPOINT",
        )

        self.assertEqual(source, "CONTENT_UNDERSTANDING_ENDPOINT")


if __name__ == "__main__":
    unittest.main()