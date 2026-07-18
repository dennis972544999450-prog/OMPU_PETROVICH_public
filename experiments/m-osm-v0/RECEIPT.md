# M-OSM Falsification Bench Receipt

Date: 2026-07-18
Mutation boundary: synthetic fixtures and this experiment directory only; no
live service, credential, bus watermark, deployment, or production state was
changed.

## Corpus

- 16 blind recall runs across C0-C10;
- 25 attributable agent Markdown reports, including mathematical, parser,
  primary-source, scoring, runtime, replication, and post-fix QA passes;
- 121/192 strict field matches across the heterogeneous blind panel;
- 135/192 semantically supported fields after the documented original and
  replication audits;
- independent repeats for tube-only failure, false-coherence corruption,
  v0.1 identity failure, v0.2 identity repair, strict JSON parsing, and the
  post-fix verified-byte invariant.

## Verification

```text
17 tests passed
16 blind result files scored
all tracked JSON artifacts parsed with jq
v0.2 validate: status ok
v0.2 compact rehydrate: status ok, one verified source
source copy and received download: identical SHA-256
exact-address scan: no Huttropstrasse 54 variant found
credential-pattern scan: no match
final consistency audit: no arithmetic or classification mismatch
```

Commands were run from this experiment root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tools/test_score_results.py prototype/test_mosm_tube.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/score_results.py
find . -type f -name '*.json' -exec jq empty {} \;
python3 prototype/mosm_tube.py validate prototype/case_alpha_tube_v0_2.json
python3 prototype/mosm_tube.py rehydrate \
  prototype/case_alpha_tube_v0_2.json \
  --allow-root . --packet-mode compact \
  --output /tmp/mosm-case-alpha-final.md
```

## Frozen hashes

```text
2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668  source/Swarm_Oscillatory_Memory_M-OSM_received_v4.md
a8bfad10c018149a4864a33b03808fdb28de7a6fe0161d78f9dfbaed3bd29bc3  raw/scoreboard.json
0dc21013681d29825335451f42f715cd893a1dea7cee9378a81c5f3644eb8b95  prototype/mosm_tube.py
dcf741e49c6dc1e767a3748ba526a22a23b8f4a8c1a3db122e5ccb2db9b63c52  prototype/mosm_tube_v0_2.schema.json
4f8f4df076441068b9b338e7bdeacf6c4e3e32d2757b893cef220dc11ab08736  prototype/case_alpha_tube_v0_2.json
003299cce418f6f61ed2fdbeee4674080e463a9948b9fa2cd972b296b11ae3da  tools/score_results.py
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
