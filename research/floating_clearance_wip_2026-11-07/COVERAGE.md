# Coverage and verification matrix — floating clearance, v0.1-wip

One row per claim of `PAPER_WORKING_DRAFT_v0.1.md`. Columns:

- **Argument** — where the argument lives: *here* (proof in the paper), *wb* (full proof in the dated
  workbench note, sketch in the paper), *—* (no proof).
- **Checked by this package** — check ids of `verify/fc_verify.py` (output in `verify/fc_verify_output.txt`).
- **Checked in the workbench** — what the dated note's own code did (same line, same model family).
- **Status** — proved / checked / observation / open.

Workbench folders are abbreviated by date: `10-29a` = `floating_clearance_2026-10-29-anthropic`,
`11-02/1015` = `floating_clearance_2026-11-02-anthropic-1015`, etc. (full list: `SOURCES.md`).

| § | Claim | Argument | Checked by this package | Checked in the workbench | Status |
|---|---|---|---|---|---|
| 1 | Two threads: $K^*=g/\min d$ over sign-change arcs; centre shifts never help | wb `10-13` | V1 (pair) | enumeration on sign schemes | proved |
| 2.1 | $K^*$ = max cycle ratio $G_\Gamma/L_\Gamma$, attained by PL threads | here | V1 (15 schemes: exact cycles == LP) | `10-29a`: bisection == cycle enumeration, 5 hand + 600 random | proved |
| 2 | Example values (pair, cyclic triple, 0/1/7.5, full order, $L=2$ example) | here | V1 | `10-29a` | proved |
| 2 | Joint $K^*$ > max pairwise in 192/300 random full-order schemes | — | — | `10-29a` run_output | checked |
| 3.1 | $C^1$ is free in the infimum | here | — | `10-30a` (explicit families) | proved |
| 3.2 | Tight edge ⇔ lies on a simple tight cycle (Fact 0′) | wb `11-02/1015` | V2 (Floyd == cycles, 15 named + 200 random) | — | proved |
| 3.3 | $C^1$ attains $K^*$ ⇔ no pinched node | wb `10-31a` | V2 lists pinched nodes | `10-31a`: explicit $C^1$ construction checked exactly; 177 random schemes | proved |
| 3.4 | Pinching needs ≥ 2 tight cycles; two marks: only antipodal fails | wb `10-31a` | V2.random (200 schemes, only 11 pinched; whole-scheme count — weak); review probe 1b: 153 two-mark schemes | `10-31a` assert on every scheme | proved |
| 3 | Antipodal pair not attainable; cyclic triple attainable with ramps $L/6$ | wb `10-30a` | — | `10-30a` exact fractions | proved |
| 4.1 | $C$ bounded iff $P=\varnothing$, else $\Theta(1/\varepsilon)$ | wb `11-01a` | — | `11-01a` certificate + grid LP | proved |
| 4.2 | $C(K^*+\varepsilon)=\nu K^2/\varepsilon$ for small $\varepsilon$ | wb `11-02/1015` Thm 1 | V4 ($\nu$, 14 schemes), V6 (grid LP at κ = 1.06–1.3 on pair, partners, irrational, asym-1, #3) | `11-02/1015`: 30+60 random schemes, exact construction at $\varepsilon=10^{-6}$; 3 lenses + 5 judges | proved |
| 4.3 | Dual over circulations on $T$ | wb `11-02/1015` Thm 2 | V4 (separable dual bracket, gap < 1e-6) | `11-02/1015`: three forms agree | proved |
| 4 | Consequences (a)–(d) | wb `11-02/1015` | — | — | proved |
| 4 | $\nu$ table (pair, partners, irrational $6-4\sqrt2$, asym-1 $3-2\sqrt2$, asym-2 $(3-\sqrt5)/4$, asym-3 $4/(1+\sqrt2+\sqrt6)^2$) | wb (closed forms); asym-3: here (derived 07.11) | V4 (rigorous primal/dual bracket); `verify/asym3_closed_form.py` (KKT multipliers > 0, dual = primal to 1e-16) | `11-02/1015`, `11-06/1015` | proved (closed forms; asym-3 by derivation + numeric dual certificate) |
| 4.4 | Pair on all $K$: $(2/L)K^2/\varepsilon$ to $2K^*$, $8K^*/L$ after | here | V5 exact profiles (κ = 6/5, 3/2, 2, 5/2, 4), V6 grid LP (κ = 1.2, 1.5, 2, 3) | `11-02/1315` exact; `11-02/1015` solver | proved |
| 5.1 | Arc lemma $R(a,b)$ | wb `11-02/1015` | V3 (exact identity, ~1300 cases; maximality by LP over grid profiles, 30 cases) | `11-02/1315` (1866 cases) | proved |
| 5.2a | $C(K)$ = finite convex node program, all $K$ | wb `11-02/1015` Thm 3 | — (only through V6 values) | `11-02/1015` check_reduction a–g; subagent 195 schemes | proved |
| 5.2b | $C\le U\le\max(C,4K/d_{\min})$ | wb | — | 80 random near-tie schemes | proved |
| 5.2c | Dual of $U$ over circulations on $\hat G$ | wb | — | $|$dual/U − 1$|\le1.1\cdot10^{-7}$ | proved |
| 5.2d | Explicit $\varepsilon_0=\nu d_{\min}\mu_{\min}/4$ | wb | — | 14 + 4 points | proved |
| 6.1 | Arc lemma without cap ($m\pm W$) | here | V3 (exact, 1000 cases) | `11-03` | proved |
| 6.2 | $C(\infty)$ = convex program, attained | wb `11-03` | — | `11-03` LP-tangent / Bellman–Ford bracket ≤ 1e-9 | proved |
| 6.3 | $C(K)=C(\infty)$ for $K\ge K_1$, $K^*\le K_1\le C(\infty)L/4$ | here | V6 (pair, partners flat beyond $2K^*$) | `11-03`: 8 named + 25 random | proved |
| 6.3 | Equality $K_1=C(\infty)L/4$ on pair, partners, connected T, #5, #3 | — | — | `11-03` run outputs | checked |
| 6.3 | Short-arc scheme: $K_1/K^*\in[1.0101,1.0105]$ | upper: Prop 6.3 bound | — | blind review probe 4 (theorem-free grid LP, lower end) | checked |
| 6.4 | Duality over balanced circulations | weak: here; strong: sketch (Sion) | — | `11-03` dual_check: 8 schemes to 1e-9 | weak proved, equality sketched + checked |
| 6.5 | Formula cannot persist beyond $2K^*$; if it reaches $2K^*$ then $C(\infty)\le4\nu K^*$ | here | V6 (pair, partners at κ = 2.5/3: $C$ below formula) | `11-03`, `11-06/1015` | proved |
| 6 | $C(\infty)$, $K_1$ table | — | V6 (pair 1/9, partners 2/9) | `11-03` | checked |
| 7.1 | 11 schemes: formula to $2K^*$ ⇔ $K_1=2K^*$ ⇔ $C(\infty)=4\nu K^*$ | — | — | `11-04` (+ correction `11-06`) | observation |
| 7.1 | Ramp-fit guess refuted both ways | counterexamples | V6 (partners: formula at κ = 1.5, 1.8 > $r_{\rm fit}=4/3$) | `11-04`, `11-06/1015` | proved (by counterexample) |
| 7.1 | "Up ⇒ $C(\infty)>4\nu K^*$" false (asym-2) | counterexample | — | `11-06/1015` cinf_check | proved (by counterexample, solver values) |
| 7.2 | Two partners on all $K$ | wb `11-06/1015` §4 | V5 (exact profiles κ = 4/3, 3/2, 9/5, 2), V6 (κ = 1.2, 1.5, 1.8, 2.5) | 24 solver points to 1.5e-8; blind reviewer's LP | proved |
| 7.3 | Second-order onset of departures | — | — | `11-06/1015` onset_fit, reviewer | checked |
| 7.3 | Upward: the formula's own profile becomes infeasible at $\varepsilon_{\rm dep}$ (ramps fit; formula slopes unique; max over free slopes) | wb (sketch); general form = subagent conjecture | — | `11-06/1015` probe_two_thread | derived under hypotheses |
| 7.3 | $C$ departs exactly there: asym-2 $2-2\sqrt5/5$, #3 $8/7$, #21 $6/5$ | — | V6: at formula just below (asym-2 1.09, #3 1.1); grid LP lower bound **above** formula just past (asym-2 1.12, #3 1.16) — rigorous certificate of an upward departure there | `11-06/1015` probes | checked |
| 7.3 | Downward at ramp overlap: asym-1 1.093836, asym-3 1.258819, irrational $1+1/\sqrt2$ | — | V6 (asym-1 at formula at 1.06, below at 1.15) | `11-06/1015` | checked |
| 7.3 | Irrational: $C/\text{formula}-1=-(34\sqrt2-48)(\kappa-\kappa_{\rm down})^2+\dots$ | — | — | probe_irrational (13 points to 5e-10) | checked |
| 7.4 | Exact deficit $F$ convex; transparent marks | here | V3 (exact identity, convexity, transparent-mark identity) | `11-06/1315` + reviewer | proved |
| 7.4 | Theorem A: no downward departure before $\kappa_A$ | here (sketch), wb `11-06/1315` | V3 (both lemmas, incl. general transparent mark); V6 (irrational at κ = 1.3 < κ_A on formula) | 10 schemes + reviewer's 10 schemes / 30 points | proved |
| 7.4 | $\kappa_A$ table | — | — | `11-06/1315` kappa_A_run | checked |
| 7.4 | Certificate dies at $\kappa_A$ | — | — | 10 named schemes within 6.3e-4; 7 more consistent (one point past κ_A) | observation |
| 8 | Picture: two mechanisms + compensation | — | — | — | observation |
| 9 | Items 1–10 | — | — | — | open |

**Revised after the blind review of 2026-11-07** (`REVIEW.md`): one-sided grid-LP checks, two upward
certificates, arc-lemma maximality, general transparent mark, upper-side wording for V5.

**Not covered by this package's script**: Theorem 5.2(a)–(d) and Theorem 6.2 as programs (the script
checks their *values* only through an independent grid LP); duality at $K=\infty$; the departure
points of §7.3 as exact numbers (the grid LP brackets them from both sides only at a distance; it cannot
resolve a second-order onset); the lower sides of Prop 4.4 and Thm 7.2 (only through the grid LP); Theorem 7.4 as a statement (the script checks its two lemmas exactly).
