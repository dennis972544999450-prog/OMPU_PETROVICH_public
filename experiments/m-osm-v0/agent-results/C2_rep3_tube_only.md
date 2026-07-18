```json
{
  "case_id": "M-ALPHA-17",
  "canonical_port": null,
  "production_mutation_allowed": false,
  "protected_function": null,
  "allowed_files": [],
  "required_tests": [],
  "rollback_artifact": null,
  "next_action": "isolated dry-run next",
  "open_uncertainty": null,
  "superseded_claim": null,
  "forbidden_action": "production mutation",
  "producer_identity": null,
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json"
  ],
  "unsupported_inferences": [
    "No canonical port number is present; 'corrected isolated port' does not supply an integer.",
    "No protected function name is present; 'protected Unicode behavior' names behavior, not a function.",
    "No allowed file paths or explicitly required test names are present.",
    "No rollback artifact, open uncertainty, or superseded claim is explicitly identified.",
    "active_subagent_id was not assumed to be producer_identity."
  ]
}
```

## Input bytes

- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md`: 943 bytes
- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json`: 714 bytes
- Total: 1657 bytes

## Method

Read only the two paths listed in `source_reads`. Used direct condition fields and semantic anchors only where the mapping was explicit enough to preserve the stated value. Returned `null` or an empty list where the requested value was absent, and did not consult another condition, answer key, result, history, bus, or network source.

## Failure noticed

The tube is lossy: it preserves qualitative anchors such as `corrected isolated port`, `no production mutation`, `protected Unicode behavior`, and `isolated dry-run next`, but it does not preserve the canonical port integer, a protected function name, file paths, named tests, rollback artifact, explicit uncertainty, superseded claim, or producer identity.

## Falsification condition

This response is falsified if either authorized input explicitly contains a non-null value reported here as missing, if a semantic anchor used as a value does not denote that field, or if the stated source paths or byte counts are inaccurate.
