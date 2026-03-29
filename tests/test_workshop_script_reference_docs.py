import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_ADMIN_DEPLOY = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "00-admin-deploy-share.md"
DOC_RUN_SCENARIO = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "04-run-scenario.md"
DOC_SCRIPT_SEQUENCE = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "05-script-sequence.md"
DOC_05B = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "05b-script-core-pipeline.md"
DOC_OPTIONAL_DEMOS = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "05c-script-optional-demos.md"
DOC_FOUNDRY_AGENT = REPO_ROOT / "workshop" / "docs" / "03-understand" / "02-foundry-agent.md"
DOC_APPENDIX_DATA = REPO_ROOT / "workshop" / "docs" / "05-appendix" / "05-maintainer-data-scripts.md"
MKDOCS_CONFIG = REPO_ROOT / "workshop" / "mkdocs.yml"
PUBLISH_AGENT_SCRIPT = REPO_ROOT / "scripts" / "09_publish_foundry_agent.py"


class WorkshopScriptReferenceDocsTests(unittest.TestCase):
    def test_admin_deploy_page_does_not_inline_shared_demo_wrapper_command(self):
        text = DOC_ADMIN_DEPLOY.read_text(encoding="utf-8")

        self.assertNotIn("python scripts/admin_prepare_shared_demo.py", text)

    def test_05b_is_only_a_retired_notice_and_points_data_scripts_to_appendix(self):
        text = DOC_05B.read_text(encoding="utf-8")

        self.assertIn("不再支援手動拆解與低階除錯", text)
        self.assertIn("附錄中的資料腳本對照", text)
        self.assertNotIn("02_create_fabric_items.py", text)
        self.assertNotIn("03_load_fabric_data.py", text)
        self.assertNotIn("06_upload_to_search.py", text)
        self.assertNotIn("07_create_foundry_agent.py", text)

    def test_mainline_docs_prefer_shared_prepare_entrypoint(self):
        for doc_path in (DOC_RUN_SCENARIO, DOC_SCRIPT_SEQUENCE):
            with self.subTest(doc_path=doc_path.name):
                text = doc_path.read_text(encoding="utf-8")
                self.assertIn("python scripts/admin_prepare_shared_demo.py --mode foundry-only", text)
                self.assertIn("python scripts/admin_prepare_shared_demo.py --mode foundry-iq", text)
                self.assertNotIn("python scripts/admin_prepare_docs_demo.py", text)
                self.assertNotIn("python scripts/admin_prepare_foundry_iq_demo.py", text)

    def test_mainline_docs_no_longer_route_users_to_05b(self):
        for doc_path in (DOC_RUN_SCENARIO, DOC_SCRIPT_SEQUENCE, DOC_APPENDIX_DATA, DOC_OPTIONAL_DEMOS):
            with self.subTest(doc_path=doc_path.name):
                text = doc_path.read_text(encoding="utf-8")
                self.assertNotIn("05b-script-core-pipeline.md", text)
                self.assertNotIn("進階：維護者腳本對照", text)

    def test_mkdocs_nav_no_longer_lists_05b(self):
        text = MKDOCS_CONFIG.read_text(encoding="utf-8")

        self.assertNotIn("進階：維護者腳本對照", text)
        self.assertNotIn("01-deploy/05b-script-core-pipeline.md", text)

    def test_script_sequence_footer_points_to_optional_demos(self):
        text = DOC_SCRIPT_SEQUENCE.read_text(encoding="utf-8")

        self.assertIn("[選配 demo 09-13 →](05c-script-optional-demos.md)", text)

    def test_appendix_data_script_page_covers_current_data_entrypoints(self):
        text = DOC_APPENDIX_DATA.read_text(encoding="utf-8")

        expected_strings = [
            "02_create_fabric_items.py",
            "03_load_fabric_data.py",
            "05_create_fabric_agent.py",
            "Deprecated shim",
        ]

        for expected in expected_strings:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_publish_foundry_agent_script_is_removed_from_repo_and_docs(self):
        self.assertFalse(PUBLISH_AGENT_SCRIPT.exists())

        for doc_path in (DOC_OPTIONAL_DEMOS, DOC_FOUNDRY_AGENT):
            with self.subTest(doc_path=doc_path.name):
                text = doc_path.read_text(encoding="utf-8")
                self.assertNotIn("09_publish_foundry_agent.py", text)

    def test_optional_demo_page_includes_copy_paste_agent_service_workflows(self):
        text = DOC_OPTIONAL_DEMOS.read_text(encoding="utf-8")

        self.assertIn("Microsoft Agent Service workflow 快貼範例", text)
        self.assertIn("content-pipeline", text)
        self.assertIn("translation-review-pipeline", text)
        self.assertIn("InvokeAzureAgent", text)

    def test_optional_demo_page_includes_agent_framework_script_demo(self):
        text = DOC_OPTIONAL_DEMOS.read_text(encoding="utf-8")

        self.assertIn("16_agent_framework_workflow_example.py", text)
        self.assertIn("agent-framework-core==1.0.0rc3", text)
        self.assertIn("mini-policy-workflow", text)

    def test_optional_demo_page_includes_agent_framework_magentic_example(self):
        text = DOC_OPTIONAL_DEMOS.read_text(encoding="utf-8")

        self.assertIn("Agent Framework multi-agent 範例（Magentic pattern）", text)
        self.assertIn("MagenticBuilder", text)
        self.assertIn("triage-manager-agent", text)
        self.assertIn("queue-ops-agent", text)
        self.assertIn("customer-comms-agent", text)

    def test_optional_demo_page_includes_flux_gpt_image_and_sora_prompts(self):
        text = DOC_OPTIONAL_DEMOS.read_text(encoding="utf-8")

        self.assertIn("Flux model prompt 快貼範例", text)
        self.assertIn("GPT Image prompt 快貼範例", text)
        self.assertIn("Sora prompt 快貼範例", text)
        self.assertIn("Flux Prompt A", text)
        self.assertIn("GPT Image Prompt A", text)
        self.assertIn("Sora Prompt A", text)

    def test_optional_demo_page_uses_collapsed_examples_for_commands_and_copy_paste(self):
        text = DOC_OPTIONAL_DEMOS.read_text(encoding="utf-8")

        self.assertIn("??? example \"執行指令\"", text)
        self.assertIn("??? example \"Flux Prompt A\"", text)
        self.assertIn("??? example \"最小可貼用 Python 範例\"", text)


if __name__ == "__main__":
    unittest.main()