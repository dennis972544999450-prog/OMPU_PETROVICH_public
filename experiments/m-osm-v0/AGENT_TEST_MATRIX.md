# Agent Test Matrix

Every completed participant produced a Markdown artifact. Repeated conditions
used separate result files; same-path T1/T2 collisions are not counted as
independent evidence.

| Lane | Completed runs | Test performed | Result surface |
|---|---:|---|---|
| C0 full context | 1 | Blind frozen-field recall | 12/12 |
| C1 prose summary | 1 | Near-budget compression baseline | 7/12 strict, 12/12 semantic |
| C2 draft Tube only | 3 | Blind recovery without external memory | 2/12, 2/12, 3/12 |
| C3 Tube plus reference | 1 | Hash-verified rehydration | 11/12 strict, 12/12 semantic |
| C4 corrupt high-`r` | 2 | False-coherence challenge | 0/12 twice |
| C5 branch projection | 1 | Typed projection plus reference | 12/12 |
| C6 v0.1 prototype | 1 | CLI validation and rehydration | 11/12 strict, 12/12 semantic; duplicate context |
| C7 compact v0.1 | 2 | Pre-rehydrated packet | Identity error in both runs |
| C8 summary chain | 1 | Two-hop lossy handoff | 6/12 strict, 11/12 semantic |
| C9 reference chain | 1 | Two-hop pointer handoff | 11/12 strict, 12/12 semantic |
| C10 typed v0.2 | 2 | Blind repeat after identity fix | 12/12 semantic twice |
| T1 mathematics | 1 implementation, two identical reruns | Analytic threshold, C simulation, slowdown and label ablations | Scoped C01; C02/C06/C07 rejected as written |
| T2 operability | 1 canonical report | Strict JSON, schema, units, hash and fresh-process probes | Parse repair required; hash cannot rehydrate |
| T3 provenance | 1 | Primary-source field audit and attention counterexample | C03 narrowed; C08 failed |
| R1 scorer audit | 1 | Independent semantic review and adversarial scorer probes | 13 strict false negatives; three scorer defects found |
| R2 T2 repeat | 1 | Blind extraction, parse repair, and arithmetic | Independently matched T2 core results |
| T4 runtime QA | 2 equivalent probes | Path, size, hash, symlink, and verify/use checks | 11/12 protective checks; stale-read defect found |
| T5 post-fix | 1 | Independent mutation-after-verify repeat | Verified bytes preserved; 10/10 then 18/18 local tests pass |
| T4 omnibus replication | 1 late snapshot | Recompiled T1, reran T2/scorer/prototype guards, audited drift | Core outputs reproduced; general M-OSM promotion held |
| T6 consistency audit | 1 | Recomputed aggregate and semantic classifications without answer key | 121/192 strict and 135/192 semantic; no mismatch |

The omnibus replication exceeded its bounded interaction window and was stopped
without a normal final status. Its two assigned files appeared late and were
validated afterward. `SCARS.md` records this orchestration failure; the report
itself remains attributable evidence with its stated snapshot limits.
