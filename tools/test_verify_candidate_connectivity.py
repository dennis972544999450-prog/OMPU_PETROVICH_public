#!/usr/bin/env python3

from __future__ import annotations

import unittest

from verify_candidate_connectivity import verify_candidate


def candidate(*, blocks: list[dict], edges: list[dict], outcome: str = "compacted") -> dict:
    return {
        "compaction_id": "fixture",
        "destination": "candidate",
        "live_writes": 0,
        "outcome": outcome,
        "blocks": blocks,
        "edges": edges,
    }


class CandidateConnectivityTests(unittest.TestCase):
    def test_connected_candidate_is_green(self) -> None:
        report = verify_candidate(
            candidate(
                blocks=[
                    {"block_id": "a", "kind": "observation"},
                    {"block_id": "z", "kind": "zusammenfassung"},
                ],
                edges=[{"edge_id": "e", "from_block_id": "a", "to_block_id": "z"}],
            )
        )
        self.assertTrue(report["ok"])

    def test_orphan_summary_is_red(self) -> None:
        report = verify_candidate(
            candidate(
                blocks=[
                    {"block_id": "a", "kind": "observation"},
                    {"block_id": "b", "kind": "observation"},
                    {"block_id": "z", "kind": "zusammenfassung"},
                ],
                edges=[{"edge_id": "e", "from_block_id": "a", "to_block_id": "b"}],
            )
        )
        self.assertFalse(report["ok"])
        self.assertEqual(report["unlinked_zusammenfassung_ids"], ["z"])

    def test_unknown_endpoint_is_red(self) -> None:
        report = verify_candidate(
            candidate(
                blocks=[{"block_id": "a", "kind": "observation"}],
                edges=[{"edge_id": "e", "from_block_id": "a", "to_block_id": "missing"}],
            )
        )
        self.assertFalse(report["ok"])
        self.assertEqual(report["metrics"]["unknown_endpoint_count"], 1)

    def test_quiet_without_blocks_is_green(self) -> None:
        report = verify_candidate(candidate(blocks=[], edges=[], outcome="quiet"))
        self.assertTrue(report["ok"])

    def test_quiet_cannot_carry_blocks(self) -> None:
        report = verify_candidate(
            candidate(
                blocks=[{"block_id": "a", "kind": "observation"}],
                edges=[],
                outcome="quiet",
            )
        )
        self.assertFalse(report["ok"])

    def test_live_writes_must_be_exact_integer_zero(self) -> None:
        fixture = candidate(blocks=[], edges=[], outcome="quiet")
        fixture["live_writes"] = False
        self.assertFalse(verify_candidate(fixture)["ok"])


if __name__ == "__main__":
    unittest.main()

