"""Test handoff contract validator."""
import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
VALIDATOR = SCRIPTS_DIR / "validate_handoffs.py"
RELEASE_CHECK = SCRIPTS_DIR / "run_release_checks.py"


class HandoffContractValidatorTest(unittest.TestCase):
    def test_validator_runs_without_error(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertIn("status", report)

    def test_validator_passes_on_current_state(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")

    def test_release_check_includes_handoff_validation(self):
        result = subprocess.run(
            [sys.executable, str(RELEASE_CHECK), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")


if __name__ == "__main__":
    unittest.main()
