# M-OSM Falsification Bench v0

This directory tests the received `Swarm Oscillatory Memory (M-OSM)` draft as
an engineering proposal. It does not assume that oscillator language maps to
LLM internals.

## Outcome

The strong latent-recovery claim failed. The practical survivor is a typed
handoff delta plus bounded, hash-verified external references. Start with
`RESULTS.md`, then `PROTOCOL_V0_2.md`, `SCOREBOARD.md`, and
`AGENT_TEST_MATRIX.md`.

## Core question

Can a compact handoff preserve the facts, corrections, constraints, uncertainty,
and next action needed by a fresh agent better than a normal summary at a lower
context cost?

## Conditions

| ID | Input available to the fresh agent | Purpose |
|---|---|---|
| C0 | Full context | Upper-bound baseline |
| C1 | Ordinary prose summary | Compression baseline |
| C2 | Draft Identification Tube only | Test the literal M-OSM claim |
| C3 | Tube plus immutable source references | Test retrieval-backed rehydration |
| C4 | Corrupted/stale Tube with a high claimed `r` | Test resistance to false coherence |
| C5 | Branch projection plus immutable references | Test the nonlinear-lifeline alternative |
| C6 | Evidence-backed Tube v0.1 plus verified references | Test the bounded practical prototype |
| C7 | Compact pre-rehydrated packet | Test the orchestrator-injects-evidence path without duplicate Tube JSON |
| C8 | Two-hop lossy-summary chain | Measure mutation after repeated handoff compression |
| C9 | Two-hop reference-preserving chain | Measure recovery after repeated pointer handoffs |
| C10 | Compact v0.2 packet with typed subject identity | Retest C7 after the observed heading/identity failure |

Every participant must produce a Markdown report containing its raw answer JSON,
commands or reads performed, token/byte cost, observed failure, and a condition
that would falsify its conclusion. Agents assigned C0-C10 must not read other
conditions or `answer_key.json` before committing their answer.

Independent repeats were added for C2, C4, C7, and C10. Result filenames are
shown in `SCOREBOARD.md`; repeated rows are separate blind agents, not reruns by
the same participant.

## Metrics

- exact fact recall;
- correction precedence;
- constraint/forbidden-action preservation;
- calibrated uncertainty;
- next-action fidelity;
- input bytes as a simple context-cost proxy;
- unsupported reconstruction count.

Self-reported phase coordinates, motivational frequency, and coherence are not
outcome metrics. They may be retained as hypotheses only if they predict one of
the observable measures above.

## Safety

All operational names and paths in `case-alpha` are synthetic fixtures. No live
service may be changed by this experiment.

## Reproduce

Run from the repository root:

```sh
python3 -m unittest \
  experiments/m-osm-v0/tools/test_score_results.py \
  experiments/m-osm-v0/prototype/test_mosm_tube.py
python3 experiments/m-osm-v0/tools/score_results.py
python3 experiments/m-osm-v0/tools/T2_schema_operational.py
python3 experiments/m-osm-v0/prototype/mosm_tube.py rehydrate \
  experiments/m-osm-v0/prototype/case_alpha_tube_v0_2.json \
  --allow-root experiments/m-osm-v0 \
  --output /tmp/mosm-v0.2-packet.md
```

T1's longer C simulation has exact compile/run commands and expected output
hashes in `agent-results/T1_math_kuramoto.md`.

## Result map

- `FINDINGS.md` - synthesis and the practical mechanism that survived;
- `CLAIM_RESULTS.md` - decision for each claim in the received draft;
- `SCOREBOARD.md` - strict machine scoring of every blind run;
- `REPLICATION_AUDIT.md` - semantic audit of the added repeats;
- `RECEIPT.md` - final verification surface and publication boundary;
- `agent-results/` - one attributable Markdown report per agent task;
- `prototype/` - the bounded evidence-backed handoff implementation;
- `raw/` - machine-readable measurements and scorer output;
- `SCARS.md` - failures that changed the implementation or interpretation.
