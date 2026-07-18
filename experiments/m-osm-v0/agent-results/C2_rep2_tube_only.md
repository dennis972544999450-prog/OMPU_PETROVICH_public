```json
{
  "case_id": "M-ALPHA-17",
  "canonical_port": null,
  "production_mutation_allowed": false,
  "protected_function": null,
  "allowed_files": null,
  "required_tests": null,
  "rollback_artifact": null,
  "next_action": "isolated dry-run",
  "open_uncertainty": null,
  "superseded_claim": null,
  "forbidden_action": "production mutation",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json"
  ],
  "unsupported_inferences": [
    "canonical_port: the condition says corrected isolated port but supplies no integer",
    "protected_function: protected Unicode behavior is named, but no function is identified",
    "allowed_files: no file paths are supplied",
    "required_tests: semantic anchors mention behaviors but do not explicitly identify required tests",
    "rollback_artifact: no rollback artifact is supplied",
    "open_uncertainty: no value is supplied",
    "superseded_claim: no superseded claim is supplied"
  ]
}
```

## Input bytes

- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md`: 943 bytes
- `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json`: 714 bytes
- Total: 1657 bytes

## Method

Literal extraction from the two authorized inputs only. Direct identifiers and explicit constraints were mapped to the requested keys; absent exact values were set to `null`, and compressed semantic anchors were not expanded into unstated filenames, numbers, function names, artifacts, or test lists.

## Failure noticed

The tube preserves thematic anchors but omits the canonical port integer, protected function name, allowed files, explicit required-test list, rollback artifact, open uncertainty, and superseded claim.

## Falsification condition

This response is falsified if either authorized input explicitly contains an omitted exact value, contradicts a reported literal value, or explicitly identifies the behavior anchors as a required-test list.
