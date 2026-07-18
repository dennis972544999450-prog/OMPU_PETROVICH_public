```json
{
  "case_id": "case-alpha-evidence-tube-001",
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
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C7_compact_rehydrated.md"
  ],
  "unsupported_inferences": []
}
```

## Benchmark Notes

- **Input bytes:** `TASK.md`: 943 bytes; `C7_compact_rehydrated.md`: 1992 bytes; total: 2935 bytes.
- **Method:** Read only the two authorized inputs, followed the explicit later correction over the earlier port claim, and transcribed only supported values into the requested schema.
- **Failure noticed:** At 09:31Z, `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` were failing; `test_unicode_route_id_unchanged` was passing.
- **Falsification condition:** This response is falsified if sealed evaluation shows any non-null value differs from the verified condition or any reported value lacks support in the two authorized inputs.
