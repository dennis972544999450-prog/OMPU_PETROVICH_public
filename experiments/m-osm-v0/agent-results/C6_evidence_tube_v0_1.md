Condition C6.

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
  "open_uncertainty": "Whether malformed input with two comment suffixes should preserve both remains unresolved.",
  "superseded_claim": "port 4173 is canonical",
  "forbidden_action": "restart com.ompu.router",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/case_alpha_tube_v0_1.json",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C6_evidence_tube_v0_1.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md"
  ],
  "unsupported_inferences": []
}
```

Input bytes: `TASK.md` 943; assigned tube 2525; generated packet 4476; verified required source 1365. The two assigned inputs total 3468 bytes. Unique pre-result evidence content read totals 9309 bytes. Counting repeated command-level reads, including the successful rehydrator's tube and source reads plus final-result validation, totals 32382 evidence bytes.

Method: Read the task and assigned tube only; invoked the permitted rehydrator with the experiment root as `--allow-root`; read its generated packet; then read only the single required source whose path, size, and SHA-256 the packet verified. Values above were transcribed from the corrected tube and the verified source; no missing value was guessed.

Observed failure: The evidence reports `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` failing at 09:31Z, while `test_unicode_route_id_unchanged` passed. Separately, the first rehydrate invocation exited 2 because the required `--output` argument was omitted; the corrected invocation exited 0 and verified one source.

Falsification condition: C6 fails if rehydration cannot verify the required source or if the recovered handoff loses or changes any source-supported correction, safety boundary, rollback requirement, exact next action, unresolved uncertainty, superseded claim, forbidden action, or producer identity; it also fails if an unsupported value is supplied instead of `null`.

Command/read log:

1. `wc -c /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/case_alpha_tube_v0_1.json`
   Read 943 + 2525 = 3468 bytes to establish assigned-input sizes.
2. `sed -n '1,240p' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md`
   Read 943 bytes.
3. `sed -n '1,320p' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/case_alpha_tube_v0_1.json`
   Read 2525 bytes.
4. `python3 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py rehydrate /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/case_alpha_tube_v0_1.json --allow-root /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0`
   Exited 2 during argument validation because `--output` was required; 0 evidence-input bytes were read.
5. `python3 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py rehydrate /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/case_alpha_tube_v0_1.json --allow-root /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0 --output /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C6_evidence_tube_v0_1.md`
   Read the 2525-byte tube and 1365-byte required source, 3890 evidence bytes total; exited 0, verified one source, and generated the packet at the authorized result path.
6. `wc -c /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C6_evidence_tube_v0_1.md`
   Read 4476 bytes to establish generated-packet size.
7. `sed -n '1,400p' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C6_evidence_tube_v0_1.md`
   Read the 4476-byte generated packet.
8. `wc -c /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md`
   Read 1365 bytes to establish required-source size.
9. `sed -n '1,260p' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/fixtures/case-alpha/full_context.md`
   Read the 1365-byte required source.
10. `wc -c /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C6_evidence_tube_v0_1.md`
    Read 4937 bytes to establish the completed result's pre-validation size.
11. `sed -n '1,45p' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C6_evidence_tube_v0_1.md`
    Read the 4937-byte completed result and confirmed the required opening plus the full fenced JSON object.
