# Hostile review: PAPER_WORKING_DRAFT_v0.1.md (frozen snapshot), fc_verify.py and its output

Reviewer: subagent (same model family as the author, so this is one more angle of the same view and not an
independent witness), 2026-11-07. I wrote nothing outside `scratchpad/review/`.
Paths: `P:` = the paper snapshot (line numbers). `W/` = `/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/`.
The workbench files are cited as `folder/file:line`.

Bottom line. I read every proof the paper labels [proved, workbench] against its source. None of them broke: the
placement lemma, Thm 5.2(b)/(d), Thm 7.2 steps (1)–(4) and Thm 7.4 steps 1–3 all check line by line.
The defects are about how claims are stated:
- overstated statuses in §7.3 and §7.4;
- one row of the §6 table that its cited source does not support;
- mis-credit and misdescription in §1 (origin) and §11 (credits);
- a non-sequitur in §4;
- schemes the paper uses but never defines;
- several narrow or tautological checks in the script.

The script reproduces exactly: 71/71 PASS in 22 s, with the same numbers as `fc_verify_output.txt`; only the
timings differ (`review/my_run_output.txt`). My seven probes break no mathematical claim; their outputs are in
`review/probe*_output.txt`.

---

## A. WRONG / OVERSTATED (fix before packaging)

**1. §7.3, upward departure: label and formula.** P:390–393, and §9 item 2 at P:465–466.
- **Claim:** "[necessary condition proved; …] … a non-tight cycle Γ … binds at ε_dep = μ_Γν/(Q̂_Γ(y*) − ν)", with
  y* "the node slopes of the formula's profile".
- **Source:** `W/…-11-06-anthropic-1015/notes.txt:84–96, 186–188`. The general form comes from the subagent note
  `probe_two_thread/NOTES.md`, section "General statement (conjecture)". The source proves only this:
  - assuming the ramps fit (R = F) and the formula's slopes are unique,
  - the formula's own profile is infeasible past ε_dep.
  - The source calls that "необходимое условие". The probe calls the general rule a *conjecture* and gives it as
    ε_dep = max over free slopes of min over Γ. The formula's profile does not fix y at free nodes; #21 needs
    f′(0) chosen.
- **What is not shown:** that C itself leaves the formula by ε_dep. Another profile could still realise
  c = νK²/ε, as happens in the partners case on the downward side.
- **Verdict:** OVERSTATED. The formula is also incomplete: it drops "max over free slopes" and both hypotheses.
- **Fix:** Relabel to "[derived for the formula's own profile under two hypotheses (ramps fit; formula slopes
  unique); departure of C there checked on three schemes]". Write
  ε_dep = max_{y_free} min_Γ μ_Γν/(Q̂_Γ(y*, y_free) − ν). Change §9.2 accordingly ("proved: the formula's profile
  becomes infeasible there; not proved: C departs there").

**2. §6, Prop 6.3 remark and Values table, "short arc 1/8".** P:302–304 and P:331.
- **Claim:**
  - "K₁/K* ≈ 1.01";
  - the short-arc scheme is listed among those where K₁ = C(∞)L/4 holds with equality [checked, workbench].
- **Source:** `W/…-11-03-anthropic-1315/notes.txt:105` gives K₁/K* "≤ 1.1". Lines 114–115 say the bisection
  returned 1.26 K* without converging ("её число не брать"). `run_named_output.txt:149–151` has C(0.97·1.26K*) = C(∞)
  and the first flat ladder step at 1.1K*. The value 1.0105 is only the *bound* C(∞)L/4/K*. Line 117 calls it
  "равенство" with no computation behind it.
- **Verdict:** OVERSTATED. The source does not support it.
- **My probe 4** (`probe4_output.txt`) uses the theorem-free grid LP, a relaxation that gives a lower bound on C and
  on K₁(c):
  - grid C(1.005K*) = 2.69748 > C(∞) = 2.694737, so K₁ > 1.005K*;
  - grid min K at c = C(∞)(1+10⁻⁶) is 1.01008K* (N = 4800), so K₁ ≥ 1.0101K*;
  - with the proved bound K₁ ≤ 1.01053K*, equality holds to 4.5·10⁻⁴.
  - The claim is therefore very likely true, but the cited source did not establish it.
- **Fix:** Write "K₁/K* ∈ [1.0101, 1.0105]" and cite a new check in the package, not the 03.11 note. Or remove the
  short-arc scheme from the equality list.

**3. §7.4, "certificate dies exactly at κ_A" on 17 schemes.** P:442–444, and §9.3 at P:467–468 ("17 schemes say
yes").
- **Source, ten named schemes:** `W/…-11-06-anthropic-1315/notes.txt:105–123`. κ_T − κ_A ranges from 0.5 to
  6.3·10⁻⁴, and the bisection is lagged by the tolerance. Acceptable.
- **Source, the reviewer's seven:** `…-1315/review/REVIEW.md` item 22. For those seven, C was evaluated only at
  κ = 1 + 1.1(κ_A − 1), one point *past* κ_A, where it is below the formula. Nothing locates the point at κ_A.
- **Verdict:** OVERSTATED.
- **Fix:** "On the ten named schemes the tight-cycle certificate dies within 6.3·10⁻⁴ of κ_A. On seven further
  schemes C is already below the formula at κ = 1 + 1.1(κ_A − 1)." In §9.3 replace "17 schemes say yes" with
  "10 schemes say yes, 7 are consistent".

**4. §4, "balance is impossible there, which is why ν is a square-root number".** P:224–225.
- **Source:** `W/…-11-02-anthropic-1015/notes.txt:136–139` says only that x = 0 would give 1/2 and that balance is
  impossible. It draws no irrationality inference.
- **Counterexample, probe 7** (`probe7_output.txt`): the scheme
  0:C>B 1; 3:A>D 2; 3:C>D 1; 11/2:D>C 2; 15/2:B>A 1; 9:C>A 2; 9:A>B 1, with L = 12.
  - It has P = {A@15/2}, L₁ = 3 and L₂ = 12.
  - The optimum is unbalanced (|x_r| = 1/3) and ν = 2/27, rational.
  - The irrationality comes from the ramp-count ratio 4:2 on the competing cycles, (1+t)² = 2(1−t)², not from
    imbalance.
- **Verdict:** WRONG (non-sequitur).
- **Fix:** "… balance is impossible there. The two competing cycle families carry 4 and 2 ramps, so the
  equalising slope solves (1+t)² = 2(1−t)², which is irrational."

**5. §1 "Origin": "one constraint per mark, signs alternating".** P:78–81.
- **Source:** `W/floating_clearance_2026-10-13/notes.txt:10, 35, 43`. The signs s_i are arbitrary, and the formula
  takes a minimum over the arcs where the sign *changes*. The 13.10 examples include ++−− (lines 63–66). With
  alternating signs every arc is a change, and the "min over sign changes" would be pointless.
- **Verdict:** WRONG (misdescription).
- **Fix:** "(both threads at every mark, one clearance per mark, arbitrary sign pattern)".

**6. §1 and §11, credit for the n-thread question.** P:82–83 ("raised in a night note of another facet
[workbench 2026-10-29, GLM facet]") and P:515.
- **Source:**
  - `W/floating_clearance_2026-10-19/notes.txt:75–76`: open item 4, "для трёх и более нитей".
  - `…-10-19/receipt.md:30`: "Либо три нити …".
  - `W/floating_clearance_2026-10-29/notes.txt:4–5`: "Открытый пункт из 19.10 …".
- **Reading:** the question was raised on 19.10 by the Claude Code facet. The GLM note *took it up*: it made the
  first attempt and the conjecture M* ≈ max pairwise + O(g/d_min), which 29.10-anthropic refuted.
- **Verdict:** MIS-CREDITED.
- **Fix:** "raised as an open item in the 19.10 note and first attacked in the GLM facet's night note (29.10)".
  Make the same change in §11.

**7. §9 item 6, transition region "known for … one random two-thread scheme".** P:473–474.
- **Source:** `W/…-11-06-anthropic-1015/probe_two_thread/NOTES.md`, item 5. The closed form for #21 holds only on
  κ ∈ (6/5, 1.278627), and is "not claimed" past κ₂.
- **Also:** the irrational scheme has a reduced-model closed form (a quartic) on (1.7071, 2.0549), whose optimality
  is not proved (`probe_irrational/NOTES.md`). The paper does not mention it.
- **Verdict:** OVERSTATED.
- **Fix:** "known for the pair and the partners; for #21 only on (6/5, 1.2786); for the irrational scheme a
  reduced-model root, not proved optimal, on (1.7071, 2.0549)".

**8. §7.3, downward: "Theorem 7.4 below makes it a lower barrier".** P:401–403.
- **Problem:** the barrier proved is κ_A, which is run-based and a sup over (𝒜, y*). The per-arc
  κ_down = 1/(1 − νd_e/a_e) at one minimizer x and one arc e is a barrier only when κ_down ≤ κ_A. That holds for the
  *smallest* per-arc value (r_fit ≤ κ_A, `…-1315/notes.txt:77–78`, remark (ii)), not for an arbitrary arc e. For
  connected T and #5 the per-arc value (1.2, 1.5) and κ_A = 2 differ.
- **Verdict:** OVERSTATED (imprecise).
- **Fix:** "Theorem 7.4 shows no downward departure before κ_A ≥ min_e κ_down(e); on asym-1, asym-3 and the
  irrational scheme κ_A equals the κ_down listed".

**9. §7.4 consequence (b): "'connected T' and #5 are explained".** P:437–438.
- **Source:** `…-1315/notes.txt:150–151` and SEE_ALSO_20261106-1315.md: "Верхняя сторона (явный профиль) там не
  построена". Theorem 7.4 explains only why C does not drop below the formula before 2. That C equals the formula
  past r_fit there rests on solver values alone.
- **Verdict:** OVERSTATED.
- **Fix:** "the lower side is explained (κ_A = 2); the upper side up to 2 is solver-only (§9.3)".

**10. Abstract (4) and (5).** P:26–32.
- **(4) "with a dual over balanced circulations":** stated without the qualifier that §6 uses, namely weak duality
  proved and equality sketched via Sion. The sketch also skips attainment of the sup over s:
  `…-11-03-anthropic-1315/notes.txt:75–78`.
- **(5) "exact departure points":** these are closed-form candidates confirmed numerically (see item 1).
- **(5) "a closed form for one family on all K":** this is one scheme, the symmetric partners. The pair (Prop 4.4)
  is a second all-K closed form.
- **Verdict:** OVERSTATED.
- **Fix:** add "(weak duality proved, equality sketched)". Say "closed-form departure points, confirmed numerically
  on six schemes" and "closed forms on all K for two schemes".

## B. MISLABELLED / UNVERIFIABLE / MIS-CREDITED (minor)

**11. §2 Examples, row "L=2 …" (the GLM example).** P:111.
- **Source:** `W/…-10-29/notes.txt` (the example near the end, g′_BC = 100), `…-10-29-anthropic/ratio_cycle.py:192–196`
  and `regression_v2.py:45`. The source scheme has full orders, six constraints: 0: A>B>C with g_AB = g_AC = 1,
  g_BC = 100; 1: A>C>B with the same values. The paper, and V1, use a reduced four-constraint scheme. K* = 100 in
  both, and "A never on a binding cycle" holds in both.
- **Verdict:** MISQUOTE (harmless).
- **Fix:** quote the source scheme, or say "reduced form of".

**12. Schemes are not defined in the paper.** P:213 ("L=12, g=1 unless stated"), §6 table and §7.
- **Problem:** "#1", "#3", "#5", "connected T", "short arc 1/8" and "asym-1/2/3" are never defined. "Partners on
  arcs 2 and 4" cannot be decoded. asym-1/2/3 use g ∈ {1/3, 2/3, 4/3, 5/3}, which the paper does not state.
- **Where they are defined:** only `fc_verify.py` NAMED, lines 397–413.
- **Verdict:** UNVERIFIABLE for a reader of the paper.
- **Fix:** add an appendix table copied from NAMED.

**13. Theorem 7.4 statement uses undefined notation.** P:425–427.
- **Problem:** Q̂^run_Γ, p_ρ, q_ρ and d_ρ are not defined. Lemma 7.3 also drops σ: it says "a, b", but the source
  uses a = σy_u.
- **Fix:** "Q̂^run_Γ(y) = Σ_{runs ρ of Γ}(p_ρ² + q_ρ²)/(2L_Γ), p_ρ = 1 − σ_ρ y_{start}, q_ρ = 1 − σ_ρ y_{end}, d_ρ the run
  length" (`…-1315/notes.txt:51–58`).

**14. §11 credits, model and slot list.** P:517–519 and P:6–9.
- "Fable 5.1 slots 13:15/20:15, Opus 5.5 slots 10:15/16:45": no note of this series comes from a 20:15 or 16:45
  slot.
- The 06.11 manual window (Fable 5.1), where the asym schemes were built in conversation with the home Codex, is
  not mentioned.
- The 19.10 step is credited to "the Claude Code facet", one of the "other facets" (P:9). Its source header says
  "Claude Code (claude-fable-5-1 по harness)", which is the same model and harness as the "Anthropic facet" of 29.10.
- **Verdict:** MIS-CREDITED (minor).
- **Fix:** list the actual slots: 13:15 Fable; 10:15 Opus; 06.11 manual window, Fable. Either call 19.10 the same
  Anthropic/Claude Code facet, or explain the distinction.

**15. §5 Remarks: "its ratio to μ_min is unbounded both ways".** P:280–281.
- **Source:** `W/…-11-02-anthropic-1015/notes.txt:214`, asserted without proof or example. Line 223 (zigzags, true
  threshold ≈ μ/(n−1)) supports only the direction where the ratio goes to 0.
- **Verdict:** UNVERIFIABLE.
- **Fix:** add "(observed; the upper direction not exhibited)", or drop it.

**16. §10, entry "06.11 (morning)".** P:503–504.
- **Claim:** "the note re-derived them under another name".
- **Source:** `…-11-06-anthropic-manual/notes.txt` re-posed the hypothesis and tested it numerically on five schemes.
  It did not re-derive the proofs.
- **Fix:** "re-posed and re-tested numerically".

**17. §10 omits an uncorrected error in a cited source.**
- **Source:** `W/…-11-03-anthropic-1315/notes.txt:103`, where the table column K₁/K* = 2.000 for #3, and lines
  107–108: "#3: … K₁ = 2K* всё равно". Both contradict the same note's k1_exact value 1.599K* (line 112) and the
  proved bound K₁ ≤ C(∞)L/4 = 1.6K*. The column is in fact the "first flat ladder step" (`run_named_output.txt:111`).
- **What the paper does:** silently uses the correct 1.599.
- **Fix:** add one line to §10, so that a reader of the source does not find a contradiction.

**18. Package files referenced but absent from the snapshot.** P:10, 42, 521–531.
- The paper refers to `verify/`, `SOURCES.md`, `COVERAGE.md` and `REPRODUCTION.md`. I could not check them.
- **Verdict:** UNVERIFIABLE.

**19. §2 and §3 coverage wording.** P:150, "[checked V2, 200 random schemes]".
- Only 11 of the 200 have pinched nodes, so only 11 actually exercise the corollary.
- **Verdict:** UNDERSTATED precision.
- **Fix:** "(200 random schemes, 11 with pinched nodes)". My probe 1b adds 153 two-mark schemes with K* > 0:
  - 0 are pinched off antipodes;
  - all 6 antipodal ones are pinched.

**20. §11 "Grid LPs are approximations".** P:534.
- **Problem:** with the marks on the grid, the grid LP is a *relaxation*, because the samples of any C^{1,1} solution
  are feasible. It is therefore a rigorous lower bound on C, up to solver tolerance. That is stronger than
  "approximation", and it is what makes V6 and my probes meaningful as one-sided evidence.
- **Verdict:** UNDERSTATED.

## C. Verification script: weak, vacuous or mislabelled checks

**21. Stale cross-references.** fc_verify.py:8–19 and the V6 texts.
- The script says: "[Prop. 1]", "[Fact 0']", "[Cor. 3.3]", "[Lemmas 5.1, 6.1, 7.4]", "[Thm 4.1, 4.2]",
  "[Prop. 4.4, Thm 7.2 …]", "[Thm 4.1, 6.3, 7.2]", "Theorem 1 formula".
- The paper numbers these Prop 2.1, Fact 3.2, Cor 3.4, Lemma 7.3, Prop 4.1 / Thm 4.2 / Thm 4.3, Prop 6.3, Thm 4.2.
- **Fix:** renumber.

**22. Tautological parts of V5.** Lines 562/567 and 576/588.
- `c == Fr(2,12)*K*K/eps` and `c == K*K/(6*eps)` are always true, because c is *defined* by that expression two
  lines above.
- V5 proves only that the profile is feasible at that c, which is the upper side.
- **Fix:** drop the tautology. State that the lower sides of Prop 4.4 and Thm 7.2 are checked only by V6, and only
  approximately: one-sided, as a relaxation.

**23. Vacuous V4 lines.** Lines 205–206.
- For P = ∅, `nu_bracket` returns (0, 0) without computing anything. The four PASS lines for short arc 1/8, cyclic
  triple, triple 0,1,7.5 and full order test nothing.
- **Fix:** drop them or mark them "(trivial, P = ∅)".

**24. Narrow V3.transparent_mark.** Lines 543–548.
- It checks one configuration only: p = 1, q = 0, with the interior slope set to the known minimiser t = m₁. The
  claim actually used in §7.4 is general: min over the interior slope of the sum of arc deficits = run deficit.
- **My probe 3b:** the general identity, with side constraints, holds to 1.3·10⁻¹⁵ on 3000 random (p, q, m₁, m₂)
  (`probe3_output.txt`).
- **Fix:** add that check.

**25. V3.arc_lemma checks an identity, not maximality.** Lines 502–513.
- It checks the integral of the *asserted* maximiser min(K, a+ct, b+c(d−t)), not that it is the maximum. Maximality
  is easy (pointwise domination), but the paper says "[checked V3]".
- **My probe 3a:** an LP maximisation over grid derivatives agrees with R(a, b) to 8·10⁻⁷, including 11 tent cases.
- **Fix:** say "identity checked", or add the LP check.

**26. V6 tolerance and two-sidedness.** Lines 621–622.
- `abs(rel) < 2.5e-3` is about 20× looser than the worst observed deviation, 1.1·10⁻⁴. A real upward departure of
  0.2 % would PASS as "formula holds".
- **Fix:** make the check one-sided (LP ≤ value + 10⁻⁷; LP ≥ value − ~3·10⁻⁴) and add a point just past each
  predicted departure, e.g. #3 at 1.16 and asym-2 at 1.12.

**27. V2.random is weak but not vacuous.** Lines 473–492.
- The generator uses integer marks, 3 threads and at most 2 constraints per mark, and finds 11 pinched schemes.
- The test counts tight cycles in the whole scheme ("≥ 2"), not two distinct tight cycles through the pinched node.
- This is acceptable, but should be described as such.

**28. V1 "GLM example".** Line 413: the reduced scheme (see item 11).

**What I checked and found sound in the script:**
- **Pinched definition:** `Scheme.pinched` takes the arcs ending and starting at the node, both forced, with opposite
  σ. This matches P:133–134 exactly. σ of a tight arc edge equals the slope sign.
- **Floyd vs cycles:** not trivial. They are different algorithms in exact rational arithmetic; parallel arcs are
  handled per edge; the negative-cycle assert is present; K* is cross-checked by LP.
- **ν bracket:** rigorous. Any x gives an upper bound, and any λ gives a lower bound by weak duality.
- **Closed forms:** hard-coded from analysis, not from the code under test.
- **V5:** the PWL profile checks (continuity at junctions, |h′| ≤ K at breakpoints, slopes ≤ c, periodicity,
  slacks) are correct for piecewise-linear derivatives.

## D. Claims checked and found OK (statement = source, label honest, numbers agree)

- **Prop 2.1** (`…-10-29-anthropic/notes.txt`): the proof is the standard difference-constraint argument.
  - The table row 3/7 and the 192/300 figure match `run_output*.txt`.
  - **Probe 1a:** grid-LP K* (no theorem inside) equals the cycle ratio to 2·10⁻¹⁶ on 120 random 4-thread schemes
    with half-integer marks (98 with K* > 0).
- **Prop 3.1** (`…-10-30-anthropic`); **Thm 3.3** and **Cor 3.4** (`…-10-31-anthropic`, a complete proof including
  the relative-interior construction).
  - The two-mark clause is true; the argument is that the long arc is dominated by the short one (probe 1b).
- **Fact 3.2** = Fact 0′ (`…-11-02-anthropic-1015/notes.txt:26–31`): the proof is complete.
- **Prop 4.1** (`…-11-01-anthropic`): the Θ(1/ε) order is proved.
  - The "ramp does not fit" case of Утверждение 2 is sloppy but vacuous for small ε: it would force c = O(ε).
- **Thm 4.2 and the placement lemma** (`…-1015/notes.txt:74–115`): I re-derived both steps of the placement lemma
  with ε_л = K*d_min²/(8Dd_max), the lower bound, and the Bellman–Ford upper construction. Proved as labelled.
  - The paper could quote ε_л.
  - **Probes 2/2b:** on six new random schemes the grid LP stays ≤ νK²/ε for every ε ≤ ε₀. At ε = K*/40 two of them
    already sit above the formula (the theorem allows this). Two schemes with P = {r} confirm equality in
    consequence (d) (L₁, L₂ = 8, 16 and 8, 12).
- **Thm 4.3 and consequences (a)–(d):**
  - Sion with a compact simplex is fine.
  - (c) "iff" holds modulo the choice of cycle decomposition.
  - **Probe 6:** 60 random schemes, 0 violations of (c) or (d), and 14 cases of P = {r} with equality.
  - **§4 table:** all ν values are reproduced by V4. The irrational scheme's x and dual weights match lines 135–141.
- **Prop 4.4** (`…-11-02-anthropic-1315`): the proof is complete. The values match `hand_checks_output.txt`.
- **Lemma 5.1 and Thm 5.2(a)–(d):** I re-derived (b) both ways, the 2-cycle condition, and (d) including
  U > 4K/d_min.
  - ε₀(irrational) = ν·2·(1/6)/4 = 0.0286, recomputed (probe 2). The "1 up to ε = 0.35" is consistent with the
    downward departure at ε = 0.3536.
- **Lemma 6.1, Thm 6.2, Prop 6.3, Cor 6.5:** proved as labelled. The Thm 6.4 label is honest: weak duality is
  re-derived, and equality is a sketch.
- **§6 table:** all entries other than the short-arc K₁ (item 2) match `…-11-03…/notes.txt:98–124`. 4νK* is
  recomputed. #3 K₁ = 1.59854 against the bound 1.6. The random range is [1.09, 2.52].
- **§7.1:** the "11 schemes (7 named + 4 random)", "7 schemes", the refutation lists and the asym-2 numbers
  (C(∞) = 0.235294 < 0.254644) match `…-11-04…/notes.txt:26–78` and `CORRECTION_20261106.md`.
- **Thm 7.2:** steps (1)–(4) re-derived. The decoupling, reflection, the crossing at a = 3c/2, the bound
  δ ≤ R₃(0,0), the sum 6K − K²/c in both regimes, the c < K/3 case and 9c ≥ 2 for K ≥ 2K* are all correct.
  - **Probe 5:** fills the gap the source admits ("профиль … при κ < 4/3 в лоб не проверял"). An explicit profile in
    exact fractions has all four slacks equal to 0 at c = K²/(6ε), for κ = 1.01, 1.1, 1.2, 1.25 and 4/3.
  - The grid LP equals the closed form at κ = 1.05, 1.3, 4/3, 1.95, 2, 2.05, to within 6·10⁻⁶.
  - The y_B values are 3c/(2K), checked algebraically.
- **§7.3 numbers** (2 − 2√5/5, 8/7, 6/5, 1.093836, 1.258819, 1 + 1/√2, 34√2 − 48, k ∈ [0.08, 75]) match
  `partner_return_output.txt`, `ramp_overlap_output.txt`, `asym3_down_output.txt`, `review/solver_checks_output.txt`
  and the probe NOTES.
- **Lemma 7.3 and Thm 7.4:** I re-derived steps 1–3 (y* ∈ U, local ⇒ global by convexity, the cycle budget per run,
  the choice of λ). Proved as labelled.
  - The κ_A table matches `…-1315/notes.txt:107–117`; asym-1 correctly uses the closed form, not 1.093845.
  - **Probe 3c:** F is non-decreasing and concave in m, with 0 violations in 5000 cases.
- **§10:** all listed corrections match their sources: 29.10, 30.10/01.11, 31.10, the 01.11 CORRECTION, 02.11
  corrections 1–5, 03.11, the 04.11 CORRECTION, and 06.11-1315 corrections 1 and 4.

## E. Probes (all in `scratchpad/review/`; run with `python3 -B`; they import the snapshot read-only)

| probe | what | result |
|---|---|---|
| probe1_kstar_grid.py | K* vs theorem-free grid LP; two-mark attainability | 2·10⁻¹⁶ on 120 schemes; 0 / 153 non-antipodal pinched, 6 / 6 antipodal pinched |
| probe2_nu_vs_gridlp.py, probe2b_eps0.py | Thm 4.2 / 5.2(d) on six new schemes; ε₀ | ε₀(irr) = 0.0286 ✓; LP ≤ formula for ε ≤ ε₀; upward departures only above ε₀ |
| probe3_lemmas.py | Lemma 5.1 maximality (LP); general transparent-mark identity; F in m | 8·10⁻⁷; 1.3·10⁻¹⁵; 0 violations |
| probe4_shortarc_K1.py | short-arc K₁ | K₁ ∈ [1.0101, 1.0105]K* (source has only ≤ 1.1) |
| probe5_partners_small_kappa.py | Thm 7.2 for κ < 4/3 (exact), grid LP near 4/3 and 2 | all PASS, slacks 0 |
| probe6_nu_bounds.py | consequences (c), (d), equality at P = {r} | 0 violations (60 schemes, 14 with P = {r}) |
| probe7_rational_unbalanced.py | §4 "imbalance ⇒ irrational" | counterexample: ν = 2/27, |x_r| = 1/3 |

**Overall:** the mathematics holds as labelled wherever a proof is claimed. Before packaging, fix the
status, credit and description defects in items 1–10, define the schemes (item 12), and tighten the vacuous or
tautological checks in the script (items 22–26).
