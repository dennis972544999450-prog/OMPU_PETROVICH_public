Condition C10.

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
  "superseded_claim": "port 4173 is canonical",
  "forbidden_action": "restart com.ompu.router",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C10_compact_v0_2.md"
  ],
  "unsupported_inferences": []
}
```

Exact commands/reads:

- `wc -c /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C10_compact_v0_2.md`
- `cat /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md`
- `cat /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C10_compact_v0_2.md`

Input bytes:

- `TASK.md`: 943 bytes
- `C10_compact_v0_2.md`: 2022 bytes
- Total read input: 2965 bytes

Method: Direct extraction from the assigned hash-verified packet, applying its later-explicit-correction rule and using no outside source.

Observed failure: The packet reports that at 09:31Z `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` were failing, while `test_unicode_route_id_unchanged` was passing. No tests were independently run.

Falsification condition: This result is falsified if the assigned packet does not support any populated field above, or if an authorized verified source contains a later explicit correction that changes one of those fields.
