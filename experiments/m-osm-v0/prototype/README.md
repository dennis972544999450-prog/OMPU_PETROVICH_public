# Evidence-Backed Handoff Tube v0.2

This is the engineering residue of the M-OSM experiment. It is not a latent
memory injector and it does not assign physical frequencies to text agents.

The tube names a subject, facts, corrections, constraints, uncertainty, next
actions, and immutable source references. Rehydration reads each bounded source
once, verifies the exact bytes, and renders those same bytes. A producer's
`claimed_coherence` is untrusted metadata.

## Run

From the experiment root:

```sh
python3 prototype/mosm_tube.py validate prototype/case_alpha_tube_v0_2.json
python3 prototype/mosm_tube.py rehydrate \
  prototype/case_alpha_tube_v0_2.json \
  --allow-root . \
  --packet-mode compact \
  --output /tmp/mosm-case-alpha.md
```

The implementation has no third-party runtime dependency. The companion JSON
Schema documents the public shape; `mosm_tube.py` enforces the operational
subset used by the prototype.

## Integrity boundary

- source paths must resolve under an explicit allowed root;
- symlink escapes, missing required sources, hash mismatches, duplicate IDs,
  unknown evidence references, and size-limit violations hold with no packet;
- per-source and aggregate byte limits bound the read;
- rendering consumes the verified in-memory text, not a second path read;
- v0.2 requires `subject_id` so tube identity cannot silently replace subject
  identity.

The remaining limitation is structural: this mechanism preserves selected
external evidence. It does not reconstruct facts that were never stored.
