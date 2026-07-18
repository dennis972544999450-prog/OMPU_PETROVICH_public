# M-OSM Blind Recall Scoreboard

| Condition | Run | Recall | Bytes | Correction | Safety | Uncertainty | Next action | Unsupported |
|---|---|---:|---:|---|---|---|---|---:|
| C0 | `C0_full_context` | 12/12 | 2019 | PASS | PASS | PASS | PASS | 0 |
| C1 | `C1_summary` | 7/12 | 1647 | FAIL | FAIL | FAIL | FAIL | 0 |
| C10 | `C10_compact_v0_2` | 12/12 | 2965 | PASS | PASS | PASS | PASS | 0 |
| C10 | `C10_rep2_compact_v0_2` | 11/12 | 2965 | FAIL | PASS | PASS | PASS | 0 |
| C2 | `C2_rep2_tube_only` | 3/12 | 1657 | FAIL | FAIL | FAIL | FAIL | 7 |
| C2 | `C2_rep3_tube_only` | 2/12 | 1657 | FAIL | FAIL | FAIL | FAIL | 5 |
| C2 | `C2_tube_only` | 2/12 | 1657 | FAIL | FAIL | FAIL | FAIL | 5 |
| C3 | `C3_tube_with_refs` | 11/12 | 3201 | FAIL | PASS | PASS | PASS | 0 |
| C4 | `C4_corrupted_high_r` | 0/12 | 1613 | FAIL | FAIL | FAIL | FAIL | 5 |
| C4 | `C4_rep2_corrupted_high_r` | 0/12 | 1613 | FAIL | FAIL | FAIL | FAIL | 7 |
| C5 | `C5_branch_projection` | 12/12 | 3365 | PASS | PASS | PASS | PASS | 0 |
| C6 | `C6_evidence_tube_v0_1` | 11/12 | 4833 | PASS | PASS | FAIL | PASS | 0 |
| C7 | `C7_compact_rehydrated` | 11/12 | 2935 | PASS | PASS | PASS | PASS | 0 |
| C7 | `C7_rep2_compact_rehydrated` | 10/12 | 2935 | FAIL | PASS | PASS | PASS | 0 |
| C8 | `C8_summary_chain` | 6/12 | 1488 | FAIL | FAIL | FAIL | FAIL | 0 |
| C9 | `C9_reference_chain` | 11/12 | 3078 | FAIL | PASS | PASS | PASS | 0 |

Input bytes are a transparent proxy, not a tokenizer-independent token metric.
Referenced-source bytes depend on the participant's declared `source_reads` and are not independently observed.
`Unsupported` counts participant-declared cautions, not auditor-classified unsupported answers.
A condition is not promoted on recall alone; correction, safety, uncertainty,
next action, and independent replication must also pass.
