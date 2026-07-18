# Added Replication Audit

Five additional blind agents repeated the conditions most likely to distinguish
mechanism from presentation. They read only `TASK.md` and their assigned
condition. This audit separates exact-string scoring from supported meaning.

| Condition and run | Strict | Semantic | Main observation |
|---|---:|---:|---|
| C2 original | 2/12 | 2/12 | Draft tube omits the values needed for reconstruction. |
| C2 rep2 | 3/12 | 2/12 | One strict match mapped `active_subagent_id` to producer without evidence; it is an unsupported false positive. |
| C2 rep3 | 2/12 | 2/12 | Independent repeat preserved the same two supported fields. |
| C4 original | 0/12 | 0/12 | High claimed coherence accompanied stale and missing facts. |
| C4 rep2 | 0/12 | 0/12 | Conservative repeat rejected the anchors; high `r` still supplied no truth signal. |
| C7 original | 11/12 | 11/12 | v0.1 returned tube identity instead of subject identity. |
| C7 rep2 | 10/12 | 11/12 | Same identity failure; one other mismatch was punctuation-only wording of the superseded claim. |
| C10 original | 12/12 | 12/12 | v0.2 typed subject restored the full fixture. |
| C10 rep2 | 11/12 | 12/12 | Full supported meaning; strict scorer rejected punctuation-only wording. |

Across the original C0-C9 panel, R1 found 96/120 semantically supported fields.
Adding C10 and the five repeats gives 135/192 semantically supported fields,
versus 121/192 strict matches. The aggregate is descriptive, not a general
effect estimate: conditions have different mechanisms and input sizes.

## Replicated conclusions

1. Tube-only latent reconstruction failed in three of three blind runs.
2. A high self-reported coherence value failed as a truth detector in two of
   two blind runs.
3. Omitting typed subject identity caused the same attention-sink error in two
   of two v0.1 runs.
4. Adding typed subject identity repaired that error in two of two v0.2 runs.
5. v0.2 did not beat the full-context baseline on bytes: it improved structure
   and integrity, not compression efficiency.

These repeats still use one synthetic incident. A real effect requires multiple
fixtures, randomized equal budgets, mediated read logging, and held-out agents.
