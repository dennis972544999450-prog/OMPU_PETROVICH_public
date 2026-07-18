Condition C8.

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
    "duplicate route IDs retain first",
    "trailing comment suffix round-trips",
    "Unicode behavior remains unchanged"
  ],
  "rollback_artifact": "backups/router-normalize-prepatch.diff",
  "next_action": "Run an isolated dry-run on fixtures/route_batch_07.json.",
  "open_uncertainty": "Whether two suffixes on malformed input must be preserved; ask rather than assume.",
  "superseded_claim": "The isolated port is 4173.",
  "forbidden_action": "Restart com.ompu.router.",
  "producer_identity": null,
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/chains/summary/A2.md"
  ],
  "unsupported_inferences": []
}
```

Commands/reads: one Python 3 read-only command called `Path.read_bytes()` for the two paths listed in `source_reads`; no other experiment inputs were read.

Input bytes: `TASK.md` = 943 bytes; `chains/summary/A2.md` = 545 bytes; total = 1488 bytes.

Observed failure: duplicate-route-ID and trailing-comment-suffix tests fail; Unicode passes. Preservation of two suffixes on malformed input remains unresolved.

Falsification condition: this reconstruction is falsified if direct source evidence shows any non-null field above differs, or shows that the producer identity is recoverable from the assigned condition.
