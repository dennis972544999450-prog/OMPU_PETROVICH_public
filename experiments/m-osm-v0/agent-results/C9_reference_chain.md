Condition C9.

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
  "superseded_claim": "port 4173 was canonical",
  "forbidden_action": "restart com.ompu.router",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/chains/reference/B2.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md"
  ],
  "unsupported_inferences": []
}
```

Commands/reads: `sed -n '1,240p'` on `TASK.md` and `B2.md`; `shasum -a 256` on the required absolute source; after the digest matched, `wc -c` on all three permitted inputs and `cat` on `full_context.md`.

Input bytes: `TASK.md` 943 bytes; `B2.md` 770 bytes; verified `full_context.md` 1365 bytes; total 3078 bytes. The source SHA-256 was `a1eee6c51f51f38a2332f2024a3dc400893f7e0349ff37ead02d9b5e2e8a0b7c`, exactly matching `B2.md`.

Method: bounded direct extraction from the two assigned files and the sole hash-verified absolute source reference; no missing field was completed from plausibility.

Observed failure: evidence at 09:31Z showed `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` failing, while `test_unicode_route_id_unchanged` passed.

Falsification condition: this result is falsified if the same 3078 input bytes do not reproduce the stated SHA-256 and byte counts, or if any non-null value above lacks direct support in those inputs.
