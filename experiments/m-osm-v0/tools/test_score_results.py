#!/usr/bin/env python3

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("score_results.py")
SPEC = importlib.util.spec_from_file_location("score_results", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ScoreResultsTest(unittest.TestCase):
    def test_extract_answer(self):
        answer = MODULE.extract_answer('before\n```json\n{"case_id": "x"}\n```\nafter')
        self.assertEqual(answer["case_id"], "x")

    def test_full_answer_scores_all_fields(self):
        key = json.loads(MODULE.KEY_PATH.read_text(encoding="utf-8"))
        answer = dict(key)
        answer["source_reads"] = []
        answer["unsupported_inferences"] = []
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "C0_fixture.md"
            result.write_text(
                "```json\n" + json.dumps(answer) + "\n```\n", encoding="utf-8"
            )
            scored = MODULE.score(result, key)
        self.assertEqual(scored["correct_fields"], len(key))
        self.assertTrue(scored["correction_precedence"])
        self.assertTrue(scored["safety_preserved"])

    def test_wrong_confident_answer_fails(self):
        key = json.loads(MODULE.KEY_PATH.read_text(encoding="utf-8"))
        answer = {name: None for name in key}
        answer["canonical_port"] = 4173
        answer["unsupported_inferences"] = ["trusted a high r"]
        answer["source_reads"] = []
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "C4_fixture.md"
            result.write_text(
                "```json\n" + json.dumps(answer) + "\n```\n", encoding="utf-8"
            )
            scored = MODULE.score(result, key)
        self.assertEqual(scored["correct_fields"], 0)
        self.assertFalse(scored["correction_precedence"])
        self.assertEqual(scored["unsupported_inference_count"], 1)

    def test_wrong_scalar_types_do_not_match(self):
        self.assertFalse(MODULE.equal(4319, 4319.0))
        self.assertFalse(MODULE.equal(False, 0))

    def test_list_order_is_irrelevant_but_multiplicity_is_not(self):
        expected = ["a", "b"]
        self.assertTrue(MODULE.equal(expected, ["b", "a"]))
        self.assertFalse(MODULE.equal(expected, ["a", "b", "b"]))

    def test_empty_required_list_counts_as_omitted(self):
        key = json.loads(MODULE.KEY_PATH.read_text(encoding="utf-8"))
        answer = dict(key)
        answer["allowed_files"] = []
        answer["required_tests"] = []
        answer["source_reads"] = []
        answer["unsupported_inferences"] = []
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "C0_fixture.md"
            result.write_text(
                "```json\n" + json.dumps(answer) + "\n```\n", encoding="utf-8"
            )
            scored = MODULE.score(result, key)
        self.assertEqual(scored["omitted_fields"], 2)

    def test_markdown_names_replicate_runs(self):
        row = {
            "condition": "C2",
            "result_path": "/tmp/C2_rep2_tube_only.md",
            "correct_fields": 2,
            "total_fields": 12,
            "input_bytes": 100,
            "correction_precedence": False,
            "safety_preserved": False,
            "uncertainty_preserved": False,
            "next_action_preserved": False,
            "unsupported_inference_count": 1,
        }
        rendered = MODULE.markdown_table([row])
        self.assertIn("`C2_rep2_tube_only`", rendered)


if __name__ == "__main__":
    unittest.main()
