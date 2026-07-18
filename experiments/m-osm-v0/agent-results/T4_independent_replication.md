# T4 Independent Replication Audit

Audit date: 2026-07-18

Repository: `/Users/denbell/OMPU_shared/petrovich_repos/public`

Experiment: `experiments/m-osm-v0`
Network, credentials, services, and live state: not accessed

## Promotion verdict

**HOLD: do not promote M-OSM as a general memory mechanism.**

The local engineering evidence is reproducible where tested, but it supports
bounded external evidence injection, not latent context recovery. The broad
hash-recovery and phase-vector rehydration claims remain operationally false or
unspecified. C10 supports a fixture-level `subject_id` regression fix: the
primary run scored 12/12 and the second run recovered the correct subject but
scored 11/12 because `Port 4173 is canonical.` differs lexically from the answer
key. This is useful local evidence, not proof of generality.

## Frozen inputs and snapshot drift

The received Downloads source and public frozen copy are both 21,368 bytes and
both hash to:

```text
2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668
```

Important final-snapshot hashes:

```text
6d111c5b3e9ef18836c33696fd0909687d2d83a09cff7ad291bbad265f100471  README.md
2e1c9865466455e2453986778eb133859a0d5f88c5cdccf0fdd067b5ee8ac69b  CLAIMS.md
96735c51f9769967623676bb62a1f4af65ce9502f0f4b1d757e04707256d4858  TASK.md
032eda65311be39cf4cc5fe3329f2b392c8e24e4f784e8591e6c25047eb5d2ad  SCOREBOARD.md
a8bfad10c018149a4864a33b03808fdb28de7a6fe0161d78f9dfbaed3bd29bc3  raw/scoreboard.json
003299cce418f6f61ed2fdbeee4674080e463a9948b9fa2cd972b296b11ae3da  tools/score_results.py
04196b80af697ea87b773e40e94fd54500f0742622ad22320165c93248df6413  tools/test_score_results.py
0dc21013681d29825335451f42f715cd893a1dea7cee9378a81c5f3644eb8b95  prototype/mosm_tube.py
03a360a8734e295205ba13e449f621408a2a6580fe88aff9e6cdac3914677489  prototype/test_mosm_tube.py
```

Drift was observed during the audit and was not hidden:

1. The initial scoreboard was the ten-run C0-C9 artifact at SHA-256
   `45284e19...307f24`; the final tree expanded to 16 runs and hash
   `a8bfad10...29bc3`.
2. C10/v0.2, repeated C2/C4/C7/C10 reports, T5, scorer fixes, and run labels
   landed while the audit was in progress. The final scorer and scoreboards were
   re-read and rerun after those changes.
3. T1 records the old ten-run scoreboard hash. The current canonical scoreboard
   is therefore not its frozen input. T1 was reproduced with a temporary C0-C9
   primary-only scoreboard preserving the exact condition order and recall
   sequence.
4. `agent-results/T6_final_consistency_audit.md` appeared during the final hash
   census at SHA-256
   `3354c83fff104ae3593c04fab3df8dc5029b5e3980a9d7db631026cb07ab4aa3`.
   Per the stop instruction, it was not read or replicated.

## Commands and exit codes

All outputs were redirected to `/tmp/mosm-t4-audit.X1gB9b` when a canonical
experiment path would otherwise be written.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest prototype/test_mosm_tube.py tools/test_score_results.py` | 0 | 17 tests passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/score_results.py --results /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results --json-output /tmp/mosm-t4-audit.X1gB9b/score-final.json --markdown-output /tmp/mosm-t4-audit.X1gB9b/score-final.md` | 0 | 16 runs; both outputs byte-identical to canonical |
| `PYTHONDONTWRITEBYTECODE=1 python3 prototype/mosm_tube.py validate prototype/case_alpha_tube_v0_1.json` | 0 | valid, one source ref |
| `PYTHONDONTWRITEBYTECODE=1 python3 prototype/mosm_tube.py validate prototype/case_alpha_tube_v0_2.json` | 0 | valid, one source ref |
| `PYTHONDONTWRITEBYTECODE=1 python3 prototype/mosm_tube.py rehydrate prototype/case_alpha_tube_v0_1.json --allow-root /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0 --output /tmp/mosm-t4-audit.X1gB9b/prototype/v0.1-compact.md --packet-mode compact` | 0 | one verified source |
| `PYTHONDONTWRITEBYTECODE=1 python3 prototype/mosm_tube.py rehydrate prototype/case_alpha_tube_v0_2.json --allow-root /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0 --output /tmp/mosm-t4-audit.X1gB9b/prototype/v0.2-compact.md --packet-mode compact` | 0 | byte-identical to `conditions/C10_compact_v0_2.md` |
| `PYTHONDONTWRITEBYTECODE=1 python3 prototype/mosm_tube.py rehydrate prototype/case_alpha_tube_v0_2.json --allow-root /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0 --output /tmp/mosm-t4-audit.X1gB9b/prototype/v0.2-audit.md --packet-mode audit` | 0 | audit packet written only in `/tmp` |
| `PYTHONDONTWRITEBYTECODE=1 python3 prototype/mosm_tube.py rehydrate prototype/case_alpha_tube_v0_1.json --allow-root /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0` | 2 | expected argparse hold: missing `--output` |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/T2_schema_operational.py` in a copied experiment tree | 0 | all substantive T2 outcomes reproduced |
| `/usr/bin/jq -e . raw/T2_part3_raw_block.txt` | 5 | expected invalid escape at line 2 |
| `/usr/bin/jq -e . raw/T2_part3_markdown_unescaped.json` | 0 | repaired payload parsed |
| `/opt/homebrew/opt/python@3.14/bin/python3.14 -I tools/T2_fresh_process_probe.py --mode tube-only < raw/T2_fresh_process_input.json` | 2 | `insufficient_information` |
| `/opt/homebrew/opt/python@3.14/bin/python3.14 -I tools/T2_fresh_process_probe.py --mode hash-only < raw/T2_hash_only_input.json` | 2 | `hash_not_recovered` |
| `cc -O3 -std=c11 -Wall -Wextra -pedantic tools/T1_noisy_kuramoto.c -lm -o /tmp/mosm-t4-audit.X1gB9b/T1_noisy_kuramoto` | 0 | no compiler warnings |
| `/tmp/mosm-t4-audit.X1gB9b/T1_noisy_kuramoto /tmp/mosm-t4-audit.X1gB9b/t1-raw` | 0 | four CSV outputs generated |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/T1_analyze.py /tmp/mosm-t4-audit.X1gB9b/t1-raw` | 0 | five derived artifacts generated |
| `wc -l /tmp/mosm-t4-audit.X1gB9b/t1-raw/T1_k_sweep.csv /tmp/mosm-t4-audit.X1gB9b/t1-raw/T1_c06_policies.csv /tmp/mosm-t4-audit.X1gB9b/t1-raw/T1_convergence.csv /tmp/mosm-t4-audit.X1gB9b/t1-raw/T1_c07_agent_outcomes.csv` | 0 | 43, 10, 64, 1025 rows |
| `rg -n '<15 C08 field-name alternation>' tools prototype conditions fixtures chains README.md TASK.md SCOREBOARD.md SOURCE_FINGERPRINT.md CLAIMS.md` | 1 | expected: zero runnable consumers |
| `ruby -rrdoc -rrdoc/markdown -e '<parse every **/*.md>'` | 0 | 47 Markdown files parsed before T6 landed |

The historical Ruby parser scars also reproduced: loading `rdoc/markdown`
without `rdoc` exited 1; the corrected command exited 0. `kramdown` is absent
and its documented command exited 1. The C3 verifier as literally printed with
double-escaped newlines exited 1; using actual newline escapes exited 0. C5's
report already records the same first-fail/corrected-pass pair, and both were
reproduced.

## Scorer and scoreboard

The final scorer output exactly matched both canonical files:

```text
032eda65311be39cf4cc5fe3329f2b392c8e24e4f784e8591e6c25047eb5d2ad  SCOREBOARD.md and temp Markdown
a8bfad10c018149a4864a33b03808fdb28de7a6fe0161d78f9dfbaed3bd29bc3  raw/scoreboard.json and temp JSON
```

An independent implementation recomputed every row by result hash with zero
field mismatches. Totals are 121/192 over 16 reports. The primary C0-C9 total
remains 83/120; adding primary C10 gives 95/132. Condition multiplicities are
C2=3, C4=2, C7=2, C10=2, and one each for the others.

R1's historical scorer false positives for numeric scalar types, duplicate list
members, and empty required-list omissions do not reproduce against the final
scorer; those cases are now covered by tests. Exact-string false negatives
remain, including C10 rep2's punctuation/case-only superseded claim.

## T1 reproduction

The temp executable hash was
`72a2e7fd0caab89b105a49687815b4fb219a52e70e9c991f745efbbd3da34718`.
Executable bytes differ from the historical in-repo binary, but all nine output
hashes are exact matches:

```text
d8a3d43156f3f48e82e610a08f8e023165d794a5894777e91281c61c1697d43e  T1_k_sweep.csv
45db734c5a3501d80c4788d20c47ca503ac2c510bf8625373a14920d57bc3321  T1_c06_policies.csv
5836c5943db6195530b3db4a649d37a9c3d8a1b9a101a177c45ba56e7b5fb6dc  T1_convergence.csv
12ac6cf0645ccb8a581127453edaef41c1c7aeb9b44f2ce0dc03055eabc390b9  T1_c07_agent_outcomes.csv
667a6e05ba21cdf698ba34f787484b9a5b4602123ad589cf204717e1ad31b9c6  T1_c07_label_assignments.csv
83c2050ebdf9e278dc60d0bd4a0d7e84b8bda39edf2814d173b2e4590319b04b  T1_c07_fixed_labels.csv
f4159c4f23cc47905cd196074fb7afcc3546d3f4d82e3e2b3b7647e8ccb73995  T1_c07_benchmark_label_assignments.csv
f453abe1c9fa6bc7d334ec18d243b253139010135740908ab9fc4a1e8d42ee3a  T1_c07_benchmark_fixed_labels.csv
8348ffcc4227cd34d23832475dde8179fdd967f0d825a2dbb10db6ce5e8af44a  T1_summary.json
```

Independent arithmetic matched: `Kc=0.74`, draft
`r=1.6462077633154328 > 1`, simulated `r(K=3.45)=0.9030402070214578`,
steepest sampled interval `0.74..0.76`, and pure generator slowdown was
seed-for-seed identical to baseline.

## T2 and manifests

The isolated T2 harness reproduced 20/24 generated artifacts byte-for-byte.
The four nonidentical files differed only in recorded absolute temp paths:
`T2_source_fingerprint.json`, both command receipts, and `T2_results.json`.
Part 3 failed strict parsing unchanged, required exactly 195 documented
backslash deletions, then parsed. The LF-inclusive payload hashes were
`496b4929...acd505` before and `3c2f0dbd...ca01` after repair.

All 15 `T2_run_manifest.json` artifact records matched current bytes and hashes;
the claims, C2 tube, and source anchors also matched. Independent T3 arithmetic
reproduced logits, softmax weights, and Hopfield output exactly. The 15 C08
leaves count as 1 supported-scoped, 6 transformed, 2 unsupported, and 6 not
found; the runnable consumer search returned no matches.

## Prototype reliability

The temporary guard matrix passed its baseline and ten rejection probes:
missing source, empty refs, unknown evidence ref, wrong hash, duplicate ref ID,
duplicate evidence ID, oversized single source, oversized aggregate, direct
outside-root path, and symlink escape. Rejections exited 2 and produced no
packet. The independent verify-then-replace probe exited 0 and rendered the
original 1,365 verified bytes, not the later 38-byte replacement. This matches
T5 and contradicts the historical pre-fix T4 result, as expected after the code
change.

Current v0.2 compact output is byte-identical to C10. Current v0.1 output is not
byte-identical to the historical C7/raw packet; the semantic payload is the
same, while the heading and correction-precedence notice changed.

## JSON and limitations

Before these two T4 files were written, Python parsed all 37 JSON files and a
corrected `/usr/bin/jq -e true <file>` pass accepted all 37. An initial aggregate
probe used `jq -e empty`, which returns exit 4 when the filter emits no result;
that was a command-design error, not 37 parse failures, and was corrected.

Not completed because the user stopped scope expansion:

- T6 was hash-noted but not read or replicated.
- Primary papers cited by T3 were not re-fetched; network access was prohibited
  and the papers are not vendored. T3 provenance agreement is therefore not
  independent proof of the scientific source claims.
- The historical deleted T4 harness could not be rerun byte-for-byte; its probe
  matrix was independently reconstructed in temporary fixtures.
- `jsonschema` is not installed. Prototype objects were checked by both the
  current validator and unit tests; schema files received syntax validation,
  not an external JSON Schema implementation.

Agreement on this one synthetic fixture does not establish cross-task,
cross-model, or cross-session generality.
