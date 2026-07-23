from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


class BootstrapScriptTests(unittest.TestCase):
    def test_test_only_bootstrap_exports_public_material_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="satlink-bootstrap-test-") as raw:
            root = Path(raw)
            output = root / "sputnik"
            script = Path(__file__).parents[1] / "tools" / "bootstrap_sputnik_application_keys.sh"
            environment = dict(os.environ, SATLINK_TEST_ONLY="1")
            subprocess.run(
                ["bash", str(script), "--output-dir", str(output), "--test-only"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
                timeout=30,
            )
            enrollment_path = output / "public" / "PUBLIC_ENROLLMENT.json"
            enrollment = json.loads(enrollment_path.read_text(encoding="utf-8"))
            rendered = json.dumps(enrollment)
            self.assertEqual(enrollment["status"], "unbound_public_claim")
            self.assertTrue(enrollment["encryption"]["recipient"].startswith("age1"))
            self.assertNotIn("AGE-SECRET-KEY", rendered)
            self.assertNotIn("minisign secret key", rendered)
            self.assertNotIn("private/", rendered)
            for path in (
                output / "private" / "sputnik-satlink.age.identity",
                output / "private" / "sputnik-satlink.minisign.key",
            ):
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_bootstrap_refuses_existing_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="satlink-bootstrap-refuse-") as raw:
            script = Path(__file__).parents[1] / "tools" / "bootstrap_sputnik_application_keys.sh"
            result = subprocess.run(
                ["bash", str(script), "--output-dir", raw, "--test-only"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=dict(os.environ, SATLINK_TEST_ONLY="1"),
                timeout=10,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
