import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_05B = REPO_ROOT / "workshop" / "docs" / "01-deploy" / "05b-script-core-pipeline.md"
DOC_APPENDIX_DATA = REPO_ROOT / "workshop" / "docs" / "05-appendix" / "05-maintainer-data-scripts.md"


class WorkshopScriptReferenceDocsTests(unittest.TestCase):
    def test_05b_keeps_mainline_scope_and_points_data_scripts_to_appendix(self):
        text = DOC_05B.read_text(encoding="utf-8")

        self.assertIn("附錄中的資料腳本對照", text)
        self.assertNotIn("02_create_fabric_items.py", text)
        self.assertNotIn("03_load_fabric_data.py", text)

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


if __name__ == "__main__":
    unittest.main()