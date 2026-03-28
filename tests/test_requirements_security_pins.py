import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_FILE = REPO_ROOT / "requirements.txt"


def parse_requirements() -> dict[str, str]:
    requirements: dict[str, str] = {}

    for raw_line in REQUIREMENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "==" not in line:
            continue

        package, version = line.split("==", maxsplit=1)
        requirements[package] = version

    return requirements
class RequirementsSecurityPinsTests(unittest.TestCase):
    def test_requests_and_pypdf_are_pinned_to_patched_versions(self):
        requirements = parse_requirements()

        self.assertEqual(requirements["requests"], "2.33.0")
        self.assertEqual(requirements["pypdf"], "6.9.2")


if __name__ == "__main__":
    unittest.main()