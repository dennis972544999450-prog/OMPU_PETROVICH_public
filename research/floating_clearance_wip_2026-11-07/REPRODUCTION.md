# Re-running the workbench scripts (2026-11-07)

**What was done.** A subagent (same model family) copied the eleven `…-anthropic*` folders of the
series into a scratch directory, rewrote only the hard-coded absolute workbench path `G` in the copies
(14 lines, listed in its log), ran every script with `python3 -B` (Python 3.14.4, numpy 2.5.2, scipy
1.18.0, Apple M4), and compared each new output with the output recorded in the folder on the day.
The originals were not written to; the folders' `MANIFEST.sha256` files all check OK (salvage 159,
03.11 10, 04.11 4, 06.11/1015 53, 06.11/1315 32, manual 7 files). About 80 salvaged helper scripts
of 02.11 were not run on their own (only those imported by `check_reduction.py`).

**Result.** 48 runs. 41 reproduced on the first pass; after re-runs at lower machine load:

| folder | scripts | verdict |
|---|---|---|
| 10-29 | ratio_cycle, regression_v2 | identical |
| 10-30 | smooth_check | identical |
| 10-31 | forced_arcs | identical |
| 11-01 | curvature_price | identical |
| 11-02 (10:15) | curvature_circulation (seeds 20261102, 7, 99) | identical (timing lines aside) |
| 11-02 (10:15) | exact_reduction | numerically equal, max rel. $2.6\cdot10^{-7}$ (7th digit of a dual column; the recorded file predates the last edit) |
| 11-02 (10:15) | check_reduction (parts a–f, then g) | identical, lines 1–109 and 110–127 (the recorded file was produced by a parts string not recoverable; the default omits g) |
| 11-02 (13:15) | hand_checks | identical |
| 11-03 | dual_check; run_inf named | identical |
| 11-03 | run_inf random | identical (solo run, see below; under load it did not finish in 900 s) |
| 11-04 | rampfit named, random | identical (timing lines aside) |
| 11-06 (10:15) | recheck_t3, scan_kappa (+ JSON), partners_closed, active_cycles, partners_profile, asym3_down, onset_fit, partner_return, ramp_overlap, both probes, review scripts | identical |
| 11-06 (10:15) | cinf_check | identical when run alone; under load its own 240 s per-solve cap fires and the output differs (the recorded file itself notes a timeout on asym-3) |
| 11-06 (10:15) | probe_irrational/reduced_model | 16 of 18 lines identical; the two extra recorded lines are printed by no script (added by a separate command on the day) |
| 11-06 (13:15) | lam_bound, kappa_A, kappa_A_run, kappa_T, lam_vs_C, review/check_section1 | identical (outputs, JSON, empty stderr) |
| 11-06 (13:15) | review/counterexample, counterexample2 | JSON identical; 3 and 5 text lines differ only in an arc count ("4 arcs" now vs "3"/"2" recorded): recorded before the arc-key fix of that afternoon, every κ value equal |
| 11-06 manual | cycle_bound, v2, v3 | identical |

No script crashed. Nothing found changes a number used in the paper.

**Notes for a re-runner.** Several recorded outputs depend on machine speed (per-solve time caps
inside the scripts); this machine ran 1.2–2× slower than the recorded timings, partly because an
unrelated process held one core at 99 % throughout. `run_inf.py random` needs a solo run (here 694 s).

**Solo run of `run_inf.py random`** (started 11:50 CET, 694 s): all 51 lines byte-identical to the
recorded `run_random_output.txt` of 03.11. With it every script of the series reproduces its recorded
output, up to the three explained differences in the table.
