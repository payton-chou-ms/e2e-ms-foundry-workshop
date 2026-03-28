import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSHOP_DIR = REPO_ROOT / "workshop"
DOCS_DIR = WORKSHOP_DIR / "docs"
MKDOCS_CONFIG = WORKSHOP_DIR / "mkdocs.yml"


class WorkshopAppendixPathTests(unittest.TestCase):
    def test_fabric_appendix_pages_live_under_appendix_directory(self):
        appendix_paths = [
            DOCS_DIR / "05-appendix" / "01-setup-fabric.md",
            DOCS_DIR / "05-appendix" / "02-workspace-settings.md",
            DOCS_DIR / "05-appendix" / "03-manual-validation.md",
            DOCS_DIR / "05-appendix" / "04-fabric-iq.md",
        ]
        legacy_paths = [
            DOCS_DIR / "01-deploy" / "02-setup-fabric.md",
            DOCS_DIR / "01-deploy" / "04b-fabric-manual-validation.md",
            DOCS_DIR / "01-deploy" / "fabric" / "workspace-settings.md",
            DOCS_DIR / "03-understand" / "02-fabric-iq.md",
        ]

        for path in appendix_paths:
            with self.subTest(path=path):
                self.assertTrue(path.exists())

        for path in legacy_paths:
            with self.subTest(path=path):
                self.assertFalse(path.exists())

    def test_mkdocs_nav_points_appendix_to_appendix_paths(self):
        config_text = MKDOCS_CONFIG.read_text(encoding="utf-8")

        for nav_target in [
            "05-appendix/01-setup-fabric.md",
            "05-appendix/02-workspace-settings.md",
            "05-appendix/03-manual-validation.md",
            "05-appendix/04-fabric-iq.md",
        ]:
            with self.subTest(nav_target=nav_target):
                self.assertIn(nav_target, config_text)

        for legacy_target in [
            "01-deploy/02-setup-fabric.md",
            "01-deploy/04b-fabric-manual-validation.md",
            "01-deploy/fabric/workspace-settings.md",
            "03-understand/02-fabric-iq.md",
        ]:
            with self.subTest(legacy_target=legacy_target):
                self.assertNotIn(legacy_target, config_text)


if __name__ == "__main__":
    unittest.main()