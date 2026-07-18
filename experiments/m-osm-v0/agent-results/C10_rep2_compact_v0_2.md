```json
{
  "case_id": "M-ALPHA-17",
  "canonical_port": 4319,
  "production_mutation_allowed": false,
  "protected_function": "normalize_route_id",
  "allowed_files": [
    "router/normalize.py",
    "tests/test_normalize.py"
  ],
  "required_tests": [
    "test_duplicate_route_id_preserves_first",
    "test_comment_suffix_round_trip",
    "test_unicode_route_id_unchanged"
  ],
  "rollback_artifact": "backups/router-normalize-prepatch.diff",
  "next_action": "run isolated dry-run against fixtures/route_batch_07.json",
  "open_uncertainty": "whether malformed input with two comment suffixes should preserve both",
  "superseded_claim": "Port 4173 is canonical.",
  "forbidden_action": "restart com.ompu.router",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C10_compact_v0_2.md"
  ],
  "unsupported_inferences": []
}
```

- **Input bytes:** `TASK.md`: 943 bytes; `C10_compact_v0_2.md`: 2022 bytes; total: 2965 bytes.
- **Method:** Blind field extraction from the assigned condition only, applying its rule that a later explicit correction in a verified source overrides an earlier statement.
- **Failure noticed:** At 09:31Z, `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` were failing; `test_unicode_route_id_unchanged` was passing.
- **Falsification condition:** This response is falsified if either recorded source byte count differs from the input read, or if a verified source contradicts any extracted value or the precedence of the explicit port correction.
