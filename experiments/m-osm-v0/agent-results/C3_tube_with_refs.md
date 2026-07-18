Condition C3.

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
  "superseded_claim": "The first probe used port 4173 and called it canonical.",
  "forbidden_action": "restart com.ompu.router",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C3_tube_with_refs.json",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md"
  ],
  "unsupported_inferences": []
}
```

## Files read

- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md` (943 bytes)
- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C3_tube_with_refs.json` (893 bytes)
- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md` (1,365 bytes; read only after its SHA-256 matched the required source reference)

## Commands run

```text
wc -c TASK.md conditions/C3_tube_with_refs.json && printf '\n--- TASK.md ---\n' && cat TASK.md && printf '\n--- C3 packet ---\n' && cat conditions/C3_tube_with_refs.json
shasum -a 256 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md
wc -c /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md && cat /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md
python3 -c 'import json, pathlib, re, sys; p=pathlib.Path(sys.argv[1]); s=p.read_text(); blocks=re.findall(r"```json\\n(.*?)\\n```", s, re.S); assert s.startswith("Condition C3.\\n"); assert len(blocks)==1; d=json.loads(blocks[0]); expected=["case_id","canonical_port","production_mutation_allowed","protected_function","allowed_files","required_tests","rollback_artifact","next_action","open_uncertainty","superseded_claim","forbidden_action","producer_identity","source_reads","unsupported_inferences"]; assert list(d)==expected; assert d["canonical_port"]==4319 and d["production_mutation_allowed"] is False; print(f"verified {p}: exact prefix, one valid JSON object, expected keys/order, corrected port, mutation=false")' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C3_tube_with_refs.md
```

## Input bytes

3,201 bytes of distinct task, packet, and required-source content (943 + 893 + 1,365).

## Method

Read the task and assigned C3 packet, verified the sole required source reference as SHA-256 `a1eee6c51f51f38a2332f2024a3dc400893f7e0349ff37ead02d9b5e2e8a0b7c`, then read that source and applied its explicit later-correction precedence. No live service was mutated.

## Observed failure

The source reports that `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` were failing at 09:31Z, while `test_unicode_route_id_unchanged` was passing. These tests were not executed in this blind read-only condition.

## Falsification condition

Condition C3's tube-with-references reconstruction is falsified if an independent blind run using only these same 3,201 byte-identical inputs, with the required source hash verified first, cannot reproduce the supported JSON fields without outside context; a specific correction-precedence failure is returning port 4173 or `null` instead of the later explicit canonical port 4319.
