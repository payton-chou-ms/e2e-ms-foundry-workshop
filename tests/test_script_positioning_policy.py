import ast
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
DATA_CONFIG_DIR = REPO_ROOT / "data" / "default" / "config"


def read_module_docstring(script_name: str) -> str:
    source = (SCRIPTS_DIR / script_name).read_text(encoding="utf-8")
    module = ast.parse(source)
    return ast.get_docstring(module) or ""


class ScriptPositioningPolicyTests(unittest.TestCase):
    def test_root_pipeline_scripts_are_labeled_as_maintainer_entrypoints(self):
        root_scripts = [
            "01_generate_sample_data.py",
            "02_create_fabric_items.py",
            "03_load_fabric_data.py",
            "04_generate_agent_prompt.py",
            "06_upload_to_search.py",
            "06a_upload_scenario_assets_to_blob.py",
            "06b_upload_to_foundry_knowledge.py",
            "07_create_foundry_agent.py",
            "07b_create_foundry_iq_agent.py",
        ]

        for script_name in root_scripts:
            with self.subTest(script_name=script_name):
                self.assertIn("維護者入口", read_module_docstring(script_name))

    def test_legacy_fabric_agent_script_remains_a_legacy_shim(self):
        docstring = read_module_docstring("05_create_fabric_agent.py")

        self.assertIn("Deprecated shim", docstring)
        self.assertNotIn("維護者入口", docstring)

    def test_foundry_knowledge_ingestion_uses_upload_documents_entrypoint(self):
        knowledge_scripts = [
            "06b_upload_to_foundry_knowledge.py",
            "pipelines/search/create_foundry_knowledge.py",
        ]

        for script_name in knowledge_scripts:
            with self.subTest(script_name=script_name):
                source = (SCRIPTS_DIR / script_name).read_text(encoding="utf-8")
                self.assertIn('with_name("upload_documents.py")', source)
                self.assertNotIn('with_name("06_upload_to_search.py")', source)

    def test_default_config_comments_use_generic_workflow_language(self):
        expected_comments = {
            "agent_ids.json": "This file is populated when you create the workshop agent, for example via scripts/admin_prepare_docs_demo.py or scripts/admin_prepare_docs_data_demo.py",
            "fabric_ids.json": "This file is populated when you prepare Fabric items for the workshop scenario",
        }
        stale_script_names = [
            "01_generate_sample_data.py",
            "02_create_fabric_items.py",
            "07_create_foundry_agent.py",
        ]

        for file_name, expected_comment in expected_comments.items():
            with self.subTest(file_name=file_name):
                data = json.loads((DATA_CONFIG_DIR / file_name).read_text(encoding="utf-8"))
                self.assertEqual(expected_comment, data["_comment"])
                for stale_script_name in stale_script_names:
                    self.assertNotIn(stale_script_name, data["_comment"])


if __name__ == "__main__":
    unittest.main()