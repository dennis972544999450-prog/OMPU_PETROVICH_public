Condition C7.

```json
{
  "case_id": "case-alpha",
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
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C7_compact_rehydrated.md"
  ],
  "unsupported_inferences": []
}
```

Exact command/read:

```sh
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md'),
    Path('/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C7_compact_rehydrated.md'),
]
for path in paths:
    data = path.read_bytes()
    print(f'<<< {path} | {len(data)} bytes >>>')
    print(data.decode('utf-8'), end='' if data.endswith(b'\n') else '\n')
    print(f'<<< END {path} >>>')
PY
```

Reads: one `read_bytes()` call for each path listed in `source_reads`; no Tube, source fixture, tool code, answer key, other condition, claims, or prior result was read.

Input bytes: `TASK.md` = 943 bytes; `C7_compact_rehydrated.md` = 1992 bytes; total = 2935 bytes.

Method: direct extraction from the assigned compact rehydrated packet, applying its stated rule that later explicit corrections override earlier statements; no plausibility completion and no external verification.

Observed failure: the packet reports that `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` were failing at 09:31Z, while `test_unicode_route_id_unchanged` was passing. No tests were run by C7.

Falsification condition: this result is falsified if the assigned hash-verified packet does not contain these values and correction ordering, if any populated value requires information outside the two authorized reads, or if the recorded byte counts/read boundary are inaccurate.
