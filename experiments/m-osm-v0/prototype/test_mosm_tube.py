#!/usr/bin/env python3

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("mosm_tube.py")
SPEC = importlib.util.spec_from_file_location("mosm_tube", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
TUBE_PATH = Path(__file__).with_name("case_alpha_tube_v0_1.json")
ROOT = Path(__file__).resolve().parents[1]


class MosmTubeTest(unittest.TestCase):
    def setUp(self):
        self.tube = json.loads(TUBE_PATH.read_text(encoding="utf-8"))

    def test_fixture_validates(self):
        self.assertEqual(MODULE.validate(self.tube), ["case-alpha"])

    def test_rehydrate_verifies_source(self):
        verified = MODULE.verify_sources(self.tube, [ROOT])
        self.assertEqual(len(verified), 1)
        packet = MODULE.render_packet(self.tube, verified)
        self.assertIn("canonical isolated", packet)
        self.assertIn("SHA-256", packet)
        self.assertNotIn('"confirmed_facts"', packet)

    def test_audit_packet_includes_tube_json(self):
        verified = MODULE.verify_sources(self.tube, [ROOT])
        packet = MODULE.render_packet(self.tube, verified, packet_mode="audit")
        self.assertIn('"confirmed_facts"', packet)

    def test_render_uses_the_exact_bytes_that_were_verified(self):
        source_ref = self.tube["source_refs"][0]
        original = Path(source_ref["path"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            temporary = root / "source.md"
            temporary.write_bytes(original.read_bytes())
            self.tube["source_refs"][0]["path"] = str(temporary)
            verified = MODULE.verify_sources(self.tube, [root])
            temporary.write_text("replacement after verification\n", encoding="utf-8")
            packet = MODULE.render_packet(self.tube, verified)
        self.assertIn("Relay Incident M-ALPHA-17", packet)
        self.assertNotIn("replacement after verification", packet)

    def test_v02_requires_subject_id(self):
        self.tube["schema_version"] = "mosm-tube/0.2"
        with self.assertRaisesRegex(MODULE.TubeError, "requires subject_id"):
            MODULE.validate(self.tube)
        self.tube["subject_id"] = "M-ALPHA-17"
        self.assertEqual(MODULE.validate(self.tube), ["case-alpha"])

    def test_hash_mismatch_holds(self):
        self.tube["source_refs"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(MODULE.TubeError, "hash mismatch"):
            MODULE.verify_sources(self.tube, [ROOT])

    def test_missing_required_ref_holds(self):
        self.tube["source_refs"][0]["path"] = "/tmp/does-not-exist"
        with self.assertRaisesRegex(MODULE.TubeError, "required source missing"):
            MODULE.verify_sources(self.tube, [ROOT])

    def test_unknown_evidence_ref_holds(self):
        self.tube["confirmed_facts"][0]["source_ref"] = "unknown"
        with self.assertRaisesRegex(MODULE.TubeError, "unknown source refs"):
            MODULE.validate(self.tube)

    def test_path_outside_allowed_root_holds(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(MODULE.TubeError, "outside allowed roots"):
                MODULE.verify_sources(self.tube, [Path(directory)])

    def test_claimed_coherence_is_bounded_but_not_trusted(self):
        self.tube["claimed_coherence"] = 1.1
        with self.assertRaisesRegex(MODULE.TubeError, "claimed_coherence"):
            MODULE.validate(self.tube)


if __name__ == "__main__":
    unittest.main()
