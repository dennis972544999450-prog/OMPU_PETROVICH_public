# T6 Final Consistency Audit

Date: 2026-07-18

## Scope and boundary

This was a read-only consistency audit of `FINDINGS.md`, `CLAIM_RESULTS.md`,
`RECEIPT.md`, `REPLICATION_AUDIT.md`, `SCOREBOARD.md`,
`raw/scoreboard.json`, `agent-results/R1_score_audit.md`, and all nine C2,
C4, C7, and C10 result Markdown files present at audit start. No browsing was
used, implementation was not modified, and `answer_key.json` was not read.

## Verdict

No arithmetic, strict-score, semantic-classification, input-byte, or targeted
result-hash mismatch was found. The synthesis is numerically consistent with
the specified result set.

Two consistency qualifications remain:

1. Several mathematical, parser, source-audit, runtime, and test claims are not
   directly evidenced by the files permitted for this audit. They may be
   supported elsewhere in the experiment, but within this audit set they are
   synthesis assertions rather than independently checkable results.
2. `RECEIPT.md` reports 24 attributable Markdown reports. That count was exact
   before this T6 file was created: 16 blind-result reports plus 8 R/T reports.
   The directory contains 25 Markdown reports after T6 is added, so 24 remains
   consistent only as a frozen pre-T6 corpus count, not as a live directory
   total.

## Recomputed arithmetic

`raw/scoreboard.json` contains 16 entries with 16 unique result paths and 12
scored fields per entry:

```text
strict = 121 / 192 = 0.6302083333...
semantic = 135 / 192 = 0.703125
```

The published totals decompose exactly as follows:

```text
C0-C9 strict:    83/120
added strict:    C10 original 12 + C2 rep2 3 + C2 rep3 2
                 + C4 rep2 0 + C7 rep2 10 + C10 rep2 11 = 38
final strict:    83 + 38 = 121/192

C0-C9 semantic:  96/120
added semantic:  C10 original 12 + C2 rep2 2 + C2 rep3 2
                 + C4 rep2 0 + C7 rep2 11 + C10 rep2 12 = 39
final semantic:  96 + 39 = 135/192
```

The R1 decimals also recompute: `83/120 = 0.691666...`, reported as `0.6917`,
and `96/120 = 0.8000`.

Run counts recompute to C0: 1, C1: 1, C2: 3, C3: 1, C4: 2, C5: 1,
C6: 1, C7: 2, C8: 1, C9: 1, and C10: 2, for 16 total runs.

All 16 stored `exact_recall` decimals equal `correct_fields / total_fields`
rounded to four decimal places. The nine C2/C4/C7/C10 report SHA-256 values in
`raw/scoreboard.json` match their current bytes. The current scoreboard hash is
`a8bfad10c018149a4864a33b03808fdb28de7a6fe0161d78f9dfbaed3bd29bc3`,
matching `RECEIPT.md`.

## Strict versus semantic classifications

| Run | Strict | Semantic | Recomputed classification |
|---|---:|---:|---|
| C2 original | 2/12 | 2/12 | The other fields are omitted or meaning-changed; the packet-completeness statement is not the target uncertainty. |
| C2 rep2 | 3/12 | 2/12 | `producer_identity = Scout-Delta` is an exact-string false positive because `active_subagent_id` does not establish producer identity. |
| C2 rep3 | 2/12 | 2/12 | Only `case_id` and the no-production-mutation constraint are supported target fields. |
| C4 original | 0/12 | 0/12 | Three populated mismatches change meaning and nine target fields are omitted under the R1 rules. |
| C4 rep2 | 0/12 | 0/12 | The provenance warning is not the target double-suffix uncertainty; no target field receives semantic credit. |
| C7 original | 11/12 | 11/12 | `case-alpha` is tube/source identity, not subject identity. |
| C7 rep2 | 10/12 | 11/12 | The superseded-claim mismatch is punctuation/case only; tube identity remains unsupported as subject identity. |
| C10 original | 12/12 | 12/12 | No adjustment. |
| C10 rep2 | 11/12 | 12/12 | The sole strict miss, `Port 4173 is canonical.`, is punctuation/case only. |

These classifications support the synthesis statements that C2 retained two
supported fields in each of three runs, C4 retained zero in both runs, both C7
runs made the same subject-identity error, and both C10 runs retained all 12
fields semantically.

## Claim support audit

### Directly supported in the specified evidence set

- The blind-result figures in `FINDINGS.md:18-30`, including byte counts and the
  C0, C1, C2, C4, C7, C8, C9, and C10 strict/semantic outcomes.
- All five replicated outcome conclusions in `REPLICATION_AUDIT.md:26-33`.
- `CLAIM_RESULTS.md` MOSM-C09, MOSM-C11, and MOSM-C12 at their stated one-fixture
  boundaries.
- The numerical corpus claims of 16 scored runs, `121/192` strict fields, and
  `135/192` semantically supported fields in `RECEIPT.md:10-15`.
- The v0.2 versus full-context byte comparison: `2965 > 2019`, so the observed
  v0.2 result is an integrity/structure result rather than a compression win.

### Partially supported

- MOSM-C04: the three C2 reports directly support failure of tube-only latent
  reconstruction. The broader fresh-process and external-source mechanism
  wording is not directly demonstrated by the permitted files.
- MOSM-C10: the C7/C10 reports and R1 audit support source-backed semantic
  preservation. Exact-byte verification and bounded runtime retrieval are not
  directly demonstrated by the permitted files.
- The `FINDINGS.md` bottom line and practical model are supported by the recall
  evidence for externalized, typed handoff content, but their mathematical and
  runtime clauses inherit the direct-support gaps below.

### Not directly supportable from the specified evidence set

- MOSM-C01, C02, C03, C05, C06, C07, and C08. Their Kuramoto, Hopfield,
  digest-preimage, scheduler-label, source-mapping, simulation, and prototype
  sensitivity evidence is not present in the files permitted for this audit.
- The six mechanism-test assertions in `FINDINGS.md:34-49`: 195 Markdown escape
  backslashes and two parses; the scoped Kuramoto theorem and simulation value;
  slowdown/frequency-narrowing behavior; held-out Hertz-label failure; the
  primary-paper mapping audit; and the verified-byte runtime bug plus post-fix
  reproduction.
- The promotion statement that no oscillator-specific claim meets the
  five-part rule, because the rule in `CLAIMS.md` was outside the permitted read
  set. The prototype-promotion state is likewise not directly inspectable here.
- The `RECEIPT.md` verification assertions for 17 passing tests, all tracked JSON
  parsing, v0.2 validation/rehydration status, source-copy identity, address
  scanning, credential scanning, and non-scoreboard frozen hashes. Only the
  16-result count and scoreboard hash were directly recomputed here.
- Claims that the runs were blind or independent beyond their distinct report
  files and self-reported `source_reads`. `SCOREBOARD.md` and R1 correctly warn
  that reads were not independently observed and the scorer does not enforce
  the blind boundary.

These are direct-evidence gaps, not contradictions. No synthesis value conflicts
with the specified underlying result reports.
