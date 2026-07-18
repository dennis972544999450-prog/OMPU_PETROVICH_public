Condition C2.

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
  "open_uncertainty": "The packet does not specify the canonical port number, exact protected function, allowed files, required tests, rollback artifact, superseded claim, or producer identity.",
  "superseded_claim": null,
  "forbidden_action": "production mutation",
  "producer_identity": null,
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json"
  ],
  "unsupported_inferences": [
    "Inferring an integer port from phase_state, momentum_gradient, coherence_index_r, inverse_temperature_beta, or attractor_state_hash.",
    "Treating the semantic anchor 'corrected isolated port' as an exact port value.",
    "Converting 'protected Unicode behavior' into an unnamed protected function or test.",
    "Treating active_subagent_id Scout-Delta as producer identity without an explicit producer relation.",
    "Inventing file scope, required tests, rollback artifact, or the text of a superseded claim."
  ]
}
```

## Inputs and method

- Files read:
  - `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md` - 943 bytes.
  - `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json` - 714 bytes.
  - `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C2_tube_only.md` - read only by the post-write verifier.
- Total assigned input: 1,657 bytes.
- File written: `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C2_tube_only.md` via the `apply_patch` tool.
- Method: literal extraction only. Missing exact values remain `null`; absent list entries remain empty arrays so the JSON retains the array types required by `TASK.md`.

## Commands actually run

```sh
perl -0777 -Mbytes -ne 'print "FILE:$ARGV\nBYTES:", length($_), "\nCONTENT:\n", $_, "\nEND\n"' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C2_tube_only.json
perl -0777 -Mbytes -MJSON::PP=decode_json -MDigest::SHA=sha256_hex -ne 'die "bad condition\n" unless /\ACondition C2\.\n/; /```json\n(.*?)\n```/s or die "missing JSON\n"; my $o=decode_json($1); my @want=sort qw(case_id canonical_port production_mutation_allowed protected_function allowed_files required_tests rollback_artifact next_action open_uncertainty superseded_claim forbidden_action producer_identity source_reads unsupported_inferences); my @got=sort keys %$o; die "bad keys\n" unless "@want" eq "@got"; die "bad sources\n" unless ref($o->{source_reads}) eq "ARRAY" && @{$o->{source_reads}} == 2; print "verified bytes=", bytes::length($_), " sha256=", sha256_hex($_), "\n"' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C2_tube_only.md
```

## Observed failure

The IdentificationTube does not contain an integer canonical port or exact names for the protected function, allowed files, required tests, rollback artifact, superseded claim, or producer role. Its numeric state and hash provide no literal decoding rule in the assigned inputs, so exact recovery of those fields fails under the no-external-memory condition.

## Concrete falsification condition

This result is falsified if either assigned input explicitly contains any omitted exact value, or if preregistered independent blind participants given only the same byte-identical C2 packet reproducibly recover the same omitted port, function, file/test scope, rollback artifact, superseded claim, and producer identity at exact-match accuracy significantly above a declared chance baseline, without reading any external source.
