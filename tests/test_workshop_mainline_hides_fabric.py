import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "workshop" / "docs"


class WorkshopMainlineHidesFabricTests(unittest.TestCase):
    def test_mainline_docs_do_not_surface_fabric_label(self):
        mainline_files = [
            "index.md",
            "00-get-started/index.md",
            "01-deploy/index.md",
            "01-deploy/00-admin-deploy-share.md",
            "01-deploy/00-participant-run-validate.md",
            "01-deploy/03-configure.md",
            "01-deploy/04-run-scenario.md",
            "01-deploy/04a-manual-experiments.md",
            "01-deploy/05-script-sequence.md",
            "01-deploy/05b-script-core-pipeline.md",
            "01-deploy/05e-script-advanced.md",
            "02-customize/index.md",
            "02-customize/02-generate.md",
            "02-customize/03-demo.md",
            "03-understand/index.md",
            "03-understand/01-foundry-iq.md",
            "03-understand/02-foundry-agent.md",
            "03-understand/03-foundry-tool.md",
            "03-understand/04-control-plane.md",
            "03-understand/05-multi-agent-extension.md",
            "04-cleanup/index.md",
            "04-cleanup/next-steps.md",
        ]

        for relative_path in mainline_files:
            with self.subTest(relative_path=relative_path):
                text = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                self.assertNotIn("Fabric", text)


if __name__ == "__main__":
    unittest.main()