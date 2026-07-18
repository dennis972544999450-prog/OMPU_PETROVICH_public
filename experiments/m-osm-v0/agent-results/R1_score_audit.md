# R1 Independent Score Audit

## Verdict

The frozen strict scorer is reproducible and its scores remain unchanged: **83/120 exact fields (0.6917)** across C0-C9. Independent field review finds **13 strict false negatives** caused by wording-only differences. Granting credit only to those semantic equivalents yields an additive **96/120 (0.8000)** interpretation; this does not replace the strict scoreboard.

Of the 37 strict mismatches, the semantic audit classifies 13 as `semantic_equivalent`, 6 as `meaning_changed`, 17 as `omitted`, and 1 as `unsupported`. No semantically wrong value was found among the current 83 exact-matched fields. Controlled probes nevertheless confirm that the scorer can produce false positives for wrong JSON scalar types and duplicate list members.

## Method

- Read `TASK.md`, `fixtures/case-alpha/answer_key.json`, `tools/score_results.py`, `SCOREBOARD.md`, and every C0-C9 result Markdown file.
- Read each assigned condition and any condition-authorized source needed to distinguish `meaning_changed` from `unsupported`.
- Re-ran the scorer to `/tmp` with the absolute results path. Both generated scoreboard files were byte-identical to `SCOREBOARD.md` and `raw/scoreboard.json`.
- Ran `python3 -m unittest tools/test_score_results.py`: 3 tests passed.
- Ran controlled temporary-result probes. No scorer, condition, source, existing result, or scoreboard file was edited.

Classification rule: `semantic_equivalent` preserves referent, polarity, membership, target, and unresolved question; `meaning_changed` is supported but changes the proposition; `omitted` is null or an empty required collection; `unsupported` populates a field from evidence that does not warrant that field mapping.

## Score Layer

| Condition | Strict | Semantic credit | Equivalent | Changed | Omitted | Unsupported |
|---|---:|---:|---:|---:|---:|---:|
| C0 | 12/12 | 12/12 | 0 | 0 | 0 | 0 |
| C1 | 7/12 | 12/12 | 5 | 0 | 0 | 0 |
| C2 | 2/12 | 2/12 | 0 | 3 | 7 | 0 |
| C3 | 11/12 | 12/12 | 1 | 0 | 0 | 0 |
| C4 | 0/12 | 0/12 | 0 | 3 | 9 | 0 |
| C5 | 12/12 | 12/12 | 0 | 0 | 0 | 0 |
| C6 | 11/12 | 12/12 | 1 | 0 | 0 | 0 |
| C7 | 11/12 | 11/12 | 0 | 0 | 0 | 1 |
| C8 | 6/12 | 11/12 | 5 | 0 | 1 | 0 |
| C9 | 11/12 | 12/12 | 1 | 0 | 0 | 0 |
| **Total** | **83/120** | **96/120** | **13** | **6** | **17** | **1** |

## Mismatch Audit

| Field | Class | Short rule and evidence |
|---|---|---|
| C1.required_tests | `semantic_equivalent` | Same three behaviors. Result: "duplicate-first behavior; comment-suffix round-trip; unchanged Unicode." |
| C1.next_action | `semantic_equivalent` | Same action and fixture. Result: "Run the isolated dry-run against fixtures/route_batch_07.json." |
| C1.open_uncertainty | `semantic_equivalent` | Same unresolved double-suffix policy. Result: "The malformed double-comment-suffix policy is unresolved." |
| C1.superseded_claim | `semantic_equivalent` | In this field, "The isolated port is 4173" is the same stale canonical-port claim. |
| C1.forbidden_action | `semantic_equivalent` | Case and punctuation only. Result: "Restart com.ompu.router." |
| C2.canonical_port | `omitted` | Result is `null`; the tube says only "corrected isolated port." |
| C2.protected_function | `omitted` | Result is `null`; the tube says only "protected Unicode behavior." |
| C2.allowed_files | `omitted` | Result is `[]`; both answer-key file paths are absent. |
| C2.required_tests | `omitted` | Result is `[]`; all three answer-key test identifiers are absent. |
| C2.rollback_artifact | `omitted` | Result is `null`; no rollback path is supplied. |
| C2.next_action | `meaning_changed` | "isolated dry-run next" preserves the action class but loses `fixtures/route_batch_07.json`. |
| C2.open_uncertainty | `meaning_changed` | Packet incompleteness replaces the behavior question about preserving two suffixes. |
| C2.superseded_claim | `omitted` | Result is `null`; no stale claim is supplied. |
| C2.forbidden_action | `meaning_changed` | "production mutation" is broader and different from restarting `com.ompu.router`. |
| C2.producer_identity | `omitted` | Result is `null`; it correctly declines to map `active_subagent_id` to producer. |
| C3.superseded_claim | `semantic_equivalent` | "The first probe used port 4173 and called it canonical" states the same stale claim. |
| C4.case_id | `omitted` | Result is `null`, despite the unlabeled anchor "M-ALPHA-17." |
| C4.canonical_port | `meaning_changed` | Result follows corrupted anchor "port 4173 canonical" instead of corrected 4319. |
| C4.production_mutation_allowed | `omitted` | Result is `null`; no permission state is supplied. |
| C4.protected_function | `omitted` | Result is `null`; no function is supplied. |
| C4.allowed_files | `omitted` | Result is `[]`; both file paths are absent. |
| C4.required_tests | `omitted` | Result is `[]`; all test identifiers are absent. |
| C4.rollback_artifact | `omitted` | Result is `null`; no rollback artifact is supplied. |
| C4.next_action | `meaning_changed` | "restart router after patch" substitutes a restart for the isolated dry-run. |
| C4.open_uncertainty | `meaning_changed` | Missing source verification is a provenance uncertainty, not the double-suffix policy question. |
| C4.superseded_claim | `omitted` | Result is `null`; no stale claim is supplied. |
| C4.forbidden_action | `omitted` | Result is `null`; no forbidden action is supplied. |
| C4.producer_identity | `omitted` | Result is `null`; it declines to map `active_subagent_id` to producer. |
| C6.open_uncertainty | `semantic_equivalent` | "Whether ... should preserve both remains unresolved" preserves the exact question. |
| C7.case_id | `unsupported` | `case-alpha` is a tube/source handle; the embedded source explicitly says "Relay Incident M-ALPHA-17." |
| C8.required_tests | `semantic_equivalent` | Same three behaviors: duplicate-first, comment round-trip, and unchanged Unicode. |
| C8.next_action | `semantic_equivalent` | Same isolated dry-run and fixture target. |
| C8.open_uncertainty | `semantic_equivalent` | Same malformed two-suffix preservation question, with "ask rather than assume." |
| C8.superseded_claim | `semantic_equivalent` | In this field, "The isolated port is 4173" preserves the stale claim. |
| C8.forbidden_action | `semantic_equivalent` | Case and punctuation only. Result: "Restart com.ompu.router." |
| C8.producer_identity | `omitted` | Result is `null`; A2 contains no producer identity. |
| C9.superseded_claim | `semantic_equivalent` | Field context already marks supersession; "was canonical" preserves the stale 4173 claim. |

The machine-readable audit in `raw/R1_semantic_audit.json` records typed expected and actual values plus answer-key, result, and assigned-evidence quotes for every row.

## Scorer Probes

| Probe | Observed result | Audit finding |
|---|---|---|
| Exact key values with `source_reads=[]` | 12/12, safety PASS | Evidential support and blind-read compliance are not measured. |
| `canonical_port=4319.0`, `production_mutation_allowed=0` | 12/12, safety PASS | False positive: Python equality accepts task-invalid scalar types. |
| Duplicate one allowed file and one required test | 12/12 | False positive: set conversion discards list multiplicity. |
| Empty `allowed_files` and `required_tests` | 10/12, `omitted_fields=0` | False negative in omission metric: empty required collections are not omissions. |
| Claim the absolute full-context path in `source_reads` | C2 bytes rise 1657 to 3022 | Input-byte count trusts a path string and does not verify a read. |

The actual-results false negatives are the 13 `semantic_equivalent` rows. The current 83 exact matches were all supported after assigned-evidence review, so no current semantic false positive was found. The two controlled false-positive probes show that this is contingent, not guaranteed by the scorer.

## Leakage And Bias

No result declares reading `answer_key.json` or another condition, and no direct cross-condition leak is evident in the recorded read logs. This is not a proof of absence because `source_reads` is self-reported and the scorer does not enforce the blind boundary.

C6 has an observed circular provenance edge: its `source_reads` includes `agent-results/C6_evidence_tube_v0_1.md`, which the rehydrator first wrote as an intermediate packet and the agent then read before completing the result. This is intermediate-output exposure, not evidence of answer-key leakage. C3, C5, C6, and C9 intentionally dereference `full_context.md`, while C7 embeds it; those conditions measure source-backed rehydration rather than memory-only recall.

Metric biases:

- Exact lexical comparison creates 13 false negatives and causes C1/C8 safety or correction flags to fail on semantically harmless wording.
- `omitted_fields` undercounts current omissions by four: C2 and C4 each encode two missing required collections as `[]`.
- `unsupported_inference_count` counts self-disclosed strings, not unsupported populated fields. C2 and C4 report five cautions each; this audit finds one populated unsupported mismatch overall.
- `input_bytes` uses filename-selected condition size plus an exact self-reported absolute source path. Equivalent relative paths can be missed; a falsely claimed path can be counted.
- All 12 fields have equal recall weight despite different operational consequences. Separate flags only partly address this.
- The scoreboard requires independent replication for promotion, but the scorer does not encode or verify replication.

## Falsification Condition

This audit is falsified if the fingerprinted inputs no longer reproduce **83/120**, or if any row labeled `semantic_equivalent` changes a task-relevant referent, polarity, permission, list membership, action target, or unresolved question when independently judged in field context. Any failing row must be reclassified and the **96/120** semantic-credit total recomputed.
