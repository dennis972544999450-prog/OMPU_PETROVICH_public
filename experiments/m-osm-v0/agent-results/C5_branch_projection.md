Condition C5.

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
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C5_branch_projection.json",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md"
  ],
  "unsupported_inferences": []
}
```

## Files read or written

- Read `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md` (943 bytes).
- Read `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C5_branch_projection.json` (1,057 bytes).
- Hash-verified, then read `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md` (1,365 bytes). Expected and observed SHA-256: `a1eee6c51f51f38a2332f2024a3dc400893f7e0349ff37ead02d9b5e2e8a0b7c`.
- Wrote, then read for verification `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C5_branch_projection.md` (output, excluded from input-byte total).

## Commands and tool operations

- `wc -c TASK.md`
- `wc -c conditions/C5_branch_projection.json`
- `cat TASK.md`
- `cat conditions/C5_branch_projection.json`
- `shasum -a 256 fixtures/case-alpha/full_context.md`
- `wc -c fixtures/case-alpha/full_context.md`
- `cat fixtures/case-alpha/full_context.md`
- `apply_patch` to create and correct only `agent-results/C5_branch_projection.md`
- `wc -c agent-results/C5_branch_projection.md`
- `shasum -a 256 agent-results/C5_branch_projection.md`
- `python3 -c 'import json,pathlib,re; s=pathlib.Path("agent-results/C5_branch_projection.md").read_text(); b=re.findall(r"```json\\n(.*?)\\n```",s,re.S); assert s.startswith("Condition C5.\\n") and len(b)==1; d=json.loads(b[0]); assert list(d)==["case_id","canonical_port","production_mutation_allowed","protected_function","allowed_files","required_tests","rollback_artifact","next_action","open_uncertainty","superseded_claim","forbidden_action","producer_identity","source_reads","unsupported_inferences"]; print("verification: ok")'`
- `python3 -c 'import json,pathlib,re; s=pathlib.Path("agent-results/C5_branch_projection.md").read_text(); b=re.findall(r"```json\n(.*?)\n```",s,re.S); assert s.startswith("Condition C5.\n") and len(b)==1; d=json.loads(b[0]); assert list(d)==["case_id","canonical_port","production_mutation_allowed","protected_function","allowed_files","required_tests","rollback_artifact","next_action","open_uncertainty","superseded_claim","forbidden_action","producer_identity","source_reads","unsupported_inferences"]; print("verification: ok")'`

## Input bytes

Total unique permitted input: **3,365 bytes** (`943 + 1,057 + 1,365`). Repeated reads performed for hashing and counting are not double-counted.

## Method

Read the task and assigned C5 condition, computed the required source's SHA-256, compared it with the assigned digest, and read that source only after the digest matched. Transcribed only explicit source facts. No tests, fixture execution, live service access, or production mutation was performed.

## Observed failure

The hash-verified source reports that at 09:31Z `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` were failing, while `test_unicode_route_id_unchanged` was passing. The double-comment-suffix behavior remains unresolved.

The first local structural-verification command failed because its raw regular expression over-escaped newline tokens and searched for literal `\\n` text. No result value was changed; the corrected verifier uses `\n` and is listed immediately after the failed command.

## Concrete falsification condition

Before repair, a clean isolated run on canonical port 4319 against `fixtures/route_batch_07.json` that does not reproduce both named failures while preserving a pass for `test_unicode_route_id_unchanged` falsifies the reported failure-state projection.
