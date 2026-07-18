# M-OSM Falsification Bench Receipt

Date: 2026-07-18
Mutation boundary: synthetic fixtures and this experiment directory only; no
live service, credential, bus watermark, deployment, or production state was
changed.

## Corpus

- 16 blind recall runs across C0-C10;
- 26 attributable agent Markdown reports, including mathematical, parser,
  primary-source, scoring, runtime, replication, and post-fix QA passes;
- 121/192 strict field matches across the heterogeneous blind panel;
- 135/192 semantically supported fields after the documented original and
  replication audits;
- independent repeats for tube-only failure, false-coherence corruption,
  v0.1 identity failure, v0.2 identity repair, strict JSON parsing, and the
  post-fix verified-byte invariant.

## Verification

```text
18 tests passed
16 blind result files scored
40 JSON artifacts parsed with jq
v0.2 validate: status ok
v0.2 compact rehydrate: status ok, one verified source; portable packet exact
source copy and received download: identical SHA-256
private-address marker scan: no match
credential-pattern scan: no match
T1 simulator/analyzer repeat: nine of nine result artifacts byte-identical
final consistency audit and scorer rerun: no arithmetic or classification mismatch
```

Commands were run from this experiment root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tools/test_score_results.py prototype/test_mosm_tube.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/score_results.py
find . -type f -name '*.json' -print0 | \
  xargs -0 -n1 jq -e 'type | length > 0'
python3 prototype/mosm_tube.py validate prototype/case_alpha_tube_v0_2.json
python3 prototype/mosm_tube.py rehydrate \
  prototype/case_alpha_tube_v0_2.json \
  --allow-root . --packet-mode compact \
  --output /tmp/mosm-case-alpha-final.md
```

## Frozen hashes

```text
2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668  source/Swarm_Oscillatory_Memory_M-OSM_received_v4.md
82dacb9db5065962a88a27c3f7abcd6af5d14f24b43615622a450c1951806437  raw/scoreboard.json
b041554d543f142186e19b69d536491d22861a003d762903a85632ab586a950c  prototype/mosm_tube.py
9363d19a4f3354a21224337ab979510d28ef20d347ef10e747a252a252dfdb13  prototype/mosm_tube_v0_2.schema.json
f5889a4ea530ab4f67ac803f2bc47d2c446de6f8768ad158a58f393c8293a9e9  prototype/case_alpha_tube_v0_2.json
2ac06a9a78c3895c9c4e03620c00ea97afff7bb5e3d9502370923fc9e2b214e3  tools/score_results.py
daaf11386b8b8ecaf6162b6acf3bcfa4b3daf97ff0d62608e43400bd5a26761f  raw/prototype_v02_portable_packet.md
```

The generated ARM64 simulator executable and Python bytecode caches are ignored
and are not publication artifacts. The C source, analyzer, raw CSV/JSON output,
and reproduction commands are included.

## Interpretation boundary

This receipt proves the recorded local tests and artifacts at these hashes. It
does not prove that language models are physical oscillators, that the single
synthetic fixture generalizes, or that a compact handoff beats full context.
The promoted mechanism is narrower: typed, evidence-backed, bounded handoff with
correction precedence and exact-byte verification.
