# Blind review of v0.1 and the response

**Reviewer.** One subagent of the same model family (Claude Opus 5.5), 2026-11-07, about 30 minutes,
given the frozen draft, the script and the workbench folders, and told to refute rather than approve.
It was not shown the author's conclusions beyond the draft itself. A same-model review is one more
angle of the same view, not an independent witness. Its full report is `review/REVIEW_v0.1_blind.md`
(line numbers `P:nnn` refer to the frozen draft, sha256 `dac535ee…`); its probe outputs are in
`review/probes/`.

**Verdict of the reviewer.** No proof labelled *proved* broke; none of seven numerical probes refuted a
mathematical claim; the script's 71 checks reproduced. Defects were in how claims were stated: labels,
one unsupported table entry, credits, one false explanatory sentence, and weak checks in the script.

**What changed** (all before the package left the scratch folder):

| # | finding | action |
|---|---|---|
| 1 | §7.3 upward rule labelled "necessary condition proved"; formula missing "max over free slopes" | relabelled: derived for the formula's own profile under two hypotheses; $C$'s departure there checked, not proved; formula written with $\max_{y_{\rm free}}\min_\Gamma$; §9.2 adjusted |
| 2 | short-arc $K_1/K^*\approx1.01$ listed as an equality case on a source that only had $\le1.1$ | now $K_1/K^*\in[1.0101,1.0105]$, lower end from the reviewer's theorem-free grid LP (probe 4), upper end the bound |
| 3 | "certificate dies exactly at $\kappa_A$ on 17 schemes" | 10 named schemes within $6.3\cdot10^{-4}$; 7 more only consistent |
| 4 | "balance is impossible, which is why $\nu$ is a square-root number" — false (probe 7: unbalanced, $\nu=2/27$) | replaced by the ramp-count reason $(1+t)^2=2(1-t)^2$; counterexample cited |
| 5 | two-thread origin described as "signs alternating" | arbitrary sign pattern |
| 6 | $n$-thread question credited to the GLM note | left open on 19.10; first attacked by the GLM note |
| 7 | transition region "known for one random scheme" | only on $(6/5,1.2786)$ for #21; irrational reduced-model root on $(1.7071,2.0549)$, not proved optimal |
| 8 | "Theorem 7.4 makes $\kappa_{\rm down}$ a lower barrier" | barrier is $\kappa_A\ge\min_e\kappa_{\rm down}(e)$; equal on asym-1, asym-3, irrational |
| 9 | "connected T and #5 are explained" | lower side explained; upper side solver-only |
| 10 | abstract overstated (duality, "exact departure points", "one family") | qualifiers added |
| 11, 28 | GLM example quoted in reduced form | full orders in paper and script ($K^*=100$ either way) |
| 12 | named schemes undefined in the paper | Appendix A |
| 13 | Theorem 7.4 notation undefined; $\sigma$ dropped in Lemma 7.3 | defined |
| 14 | slot list and credits inaccurate | actual slots listed; 19.10 named as the Anthropic facet's visit; manual window credited |
| 15 | "ratio to $\mu_{\min}$ unbounded both ways" | one direction shown, the other marked as asserted only |
| 16 | 06.11 manual note "re-derived" proofs | "re-posed and re-tested numerically" |
| 17 | 03.11 note's "$K_1=2K^*$ for #3" contradiction unmentioned | recorded in §10 |
| 18 | package files absent from snapshot | present now |
| 19 | "200 random schemes" | "of which only 11 have pinched nodes" |
| 20 | grid LPs called "approximations" | they are relaxations: rigorous lower bounds when marks are on the grid |
| 21 | stale numbering in the script | renumbered |
| 22 | V5 asserted $c$ equal to its own definition | tautology removed; V5 labelled as upper sides |
| 23 | V4 rows with $P=\varnothing$ trivial | marked trivial |
| 24 | transparent-mark check only one configuration | general identity added (3000 cases, $4\cdot10^{-15}$) |
| 25 | arc lemma: identity, not maximality | LP maximality check added (30 cases, $2\cdot10^{-5}$) |
| 26 | V6 two-sided 2.5e-3 tolerance | one-sided ($-3\cdot10^{-4}\le$ rel $\le10^{-8}$); points just below and just past upward departures added; past them the LP lower bound exceeds the formula (#3 at 1.16 by 1.3 %, asym-2 at 1.12 by 0.40 %) |
| 27 | V2.random weak | described as weak |

After the changes: 76 checks, all pass (`verify/fc_verify_output.txt`).

**Added after the review and not reviewed by anyone else:** the closed form
$\nu(\text{asym-3})=4/(1+\sqrt2+\sqrt6)^2$ with its KKT/dual certificate, the "where the square roots
come from" remark in §4, and the hint on $\sqrt2$ in §9.4.
