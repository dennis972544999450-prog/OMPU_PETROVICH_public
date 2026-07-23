from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class OfflineCliTests(unittest.TestCase):
    def test_bootstrap_compose_seal_receive_shadow(self) -> None:
        with tempfile.TemporaryDirectory(prefix="satlink-cli-test-") as raw:
            root = Path(raw)
            project = Path(__file__).parents[1]
            bootstrap = project / "tools" / "bootstrap_sputnik_application_keys.sh"
            cli = project / "tools" / "satlink_cli.py"
            key_dir = root / "keys"
            subprocess.run(
                ["bash", str(bootstrap), "--output-dir", str(key_dir), "--test-only"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=dict(os.environ, SATLINK_TEST_ONLY="1"),
                timeout=30,
            )
            enrollment = json.loads(
                (key_dir / "public" / "PUBLIC_ENROLLMENT.json").read_text(encoding="utf-8")
            )
            body = root / "body.txt"
            body.write_text("CLI end-to-end fixture", encoding="utf-8")
            message = root / "message.json"
            envelope = root / "message.age"
            common = [sys.executable, str(cli)]
            subprocess.run(
                common
                + [
                    "compose",
                    "--body-file",
                    str(body),
                    "--output",
                    str(message),
                    "--sequence",
                    "1",
                    "--signing-key-id",
                    enrollment["signing"]["key_id"],
                    "--disclosure",
                    "bus_ok",
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            subprocess.run(
                common
                + [
                    "seal",
                    "--message",
                    str(message),
                    "--signing-secret-key",
                    str(key_dir / "private" / "sputnik-satlink.minisign.key"),
                    "--age-recipient",
                    enrollment["encryption"]["recipient"],
                    "--output",
                    str(envelope),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            receive = subprocess.run(
                common
                + [
                    "receive-shadow",
                    "--envelope",
                    str(envelope),
                    "--age-identity",
                    str(key_dir / "private" / "sputnik-satlink.age.identity"),
                    "--signing-key-id",
                    enrollment["signing"]["key_id"],
                    "--signing-public-key",
                    str(key_dir / "public" / "sputnik-satlink.minisign.pub"),
                    "--origin-id",
                    "cli-fixture-1",
                    "--ledger",
                    str(root / "ledger.sqlite3"),
                    "--spool-dir",
                    str(root / "spool"),
                    "--shadow-dir",
                    str(root / "shadow"),
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            receipt = json.loads(receive.stdout)
            self.assertEqual(receipt["verdict"], "accepted")
            self.assertEqual(receipt["projection"], "BUS_PROJECTED_SHADOW")
            self.assertNotIn("CLI end-to-end fixture", receive.stdout)
            self.assertEqual(len(list((root / "shadow").glob("*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
