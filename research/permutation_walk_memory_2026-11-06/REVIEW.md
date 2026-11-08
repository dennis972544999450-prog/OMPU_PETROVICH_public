# Слепая рецензия (агент general-purpose, задание опровергнуть; 9.8 мин, 20 вызовов инструментов) · 08.11.2026 13:37–13:47 CET

Дано: notes.txt, LETTER_draft.md, оба стенда, код другой стороны, §6.4/§7/§8 статьи. Отчёт агента дословно
(перевод не делался; язык отчёта английский). Что принято — в notes.txt, раздел «Правки после рецензии».

---

**Blind review — spitzer_sqrt2_2026-11-08-anthropic-1315 (notes.txt + LETTER_draft.md)**

**Verdict:** the central claim survives. I could not refute V₁ = √2·V, V(0) = σ/√2 = 1/√12, A = C/2, or the invariance of c₁, c₂, C_ρ. I confirmed it with a method different from the author's (hat-function product-trapezoid Nyström, nodes at x=ih so V(0) is read at a node, constant continuation instead of reflection; script `scratchpad/spitzer/review/indep_nystrom.py`): h²-Richardson V(0) = 0.288675136 vs 1/√12 = 0.288675135; V₁(u)/V(u) at u = 0, ½, 1 after Richardson = 1.4142136 (7 digits); ‖V‖²_[0,1] = 0.61853 = (λ/A)/2 of their code. What follows are errors of description and omissions, most severe first.

**Severe (must fix before sending)**

1. **Letter p.5 and notes l.42–43 misdescribe the grid local-limit run.** Letter: "0.97775 при n = 512 с ходом к тому же числу"; notes: "→ √(3/π) = 0.97720 (сверху …)". The author's n-sequence at h=0.02 is *increasing* (0.97672, 0.97731, 0.97760, 0.97775; differences halve) and extrapolates in n to ≈0.9779, i.e. *past* the target, not toward it. The convergence is in h, not n: I re-ran the author's own `local_limit` at h=0.04/0.02/0.01 → n-limits 0.98025 / 0.97789 / 0.97737, ratio ≈4.5 (O(h²)), h²-Richardson 0.97720. My method's Richardson-in-h sequence 0.977062, 0.977133, 0.977169 (n=512…2048) extrapolates in n to 0.977205 exactly. So the claim is true but the stated evidence ("ход к тому же числу", "сверху", "5·10⁻⁴") is wrong as written; quote the h-Richardson instead. (n ≥ 4096 at X=60 is boundary-contaminated; author's n ≤ 512 is safe.)

2. **§6.4 p.2 is inconsistent with p.1 under either normalization, and the proposed fix does not touch it.** The δ-normalized continuum eigenfunction is ψ_ξ(x) ≈ √(2/π)·ξ·V(x) only for the slope-1 V; then ∫ψ_ξψ_ξφⁿdξ gives (2/π)·√π/4·(2/(nσ²))^{3/2} = √(2/π)/σ³ = C, not A. With the paper's V₁ = √2V the prefactor in p.2 must be 1/√π (then I₂ = (1/π)∫ξ²e^{−nξ²/12}dξ = A·n^{−3/2} and the "(540−18²)/36 = 6A" arithmetic is right). The letter should name this: the √(2/π) in p.2 is a second, independent witness of the same √2.

3. **Two paper locations missing from the letter's list** (it names §6.4 p.1/p.4, §7 p.1/p.3, §8 row §6.4): §8 row §6.1, last column "boundary V₁(0) = 1/√6 exact" (l.181), and §9.1 bullet "Analytic Wiener–Hopf Spitzer Proof V₁(0)=1/√6" (l.193).

**Moderate**

4. **"Что при этом закрывается точно: K_∞(0,0) = √(3/π)"** and the proposed §8 bucket text ("V₁ = √2·V; K_∞(0,0) = √(3/π)" inside "proved as theorem") recreate the seam the letter corrects: both rest on the local-limit constant C, which notes §5 itself calls "сшивка режимов, не цитата". Write "теорема по модулю классической константы локальной теоремы (ссылка проверяется), численно 10⁻¹⁰". The letter's last sentence half-says this; the bucket wording does not.

5. **Monte Carlo without error bar and with an unstated bias.** Walks unfinished at 20 000 steps (0.4 %) are dropped; their eventual undershoot has mean δ₀ ≈ 0.228 < E[H], so E[H] is biased up by ≈2.5·10⁻⁴, same size as the SE (≈3·10⁻⁴ at 4·10⁵ walks). My 10⁶-walk run: 0.28926 ± 0.00022 raw (z = 2.65 vs σ/√2), ≈0.28902 after bias correction. State "0.28901 ± 0.0003, truncation bias +2.5·10⁻⁴"; σ = 0.408 is excluded either way. (Side result: E[H²]/(2E[H]) = 0.2277 by MC vs grid w(∞) = 0.22737 — notes l.73–74 "не проверял" can now say checked to 3·10⁻⁴.)

6. **Garage is incomplete:** notes §7 and the letter ("рецензия") cite REVIEW.md, LETTER.md, MANIFEST.sha256; the folder holds only six files. Hashes that are quoted (9e808893d487…, 4a8948db9a9f…, 18161aa87d7a…) all match.

**Minor wording**

7. Letter p.3 "в нуле 1.4142135624 до 10⁻¹⁰" is V₁(0)/(theoretical σ/√2), not grid-vs-code; a reader will take it as grid agreement. The author has a stronger unused fact: h²-Richardson of his own three V(0) values gives 0.28867535 (2·10⁻⁷ from 1/√12).
8. The identity V₁(0) = ∫₀¹(1−y)V₁(y)dy is harmonicity at 0 and holds for any normalization; the fix for §6.4 p.1 should call it that, not "Spitzer's boundary identity".
9. "V₁(x) ~ √2·x" (letter p.4) is inferred: V₁ is computed only on [0,1]; the global statement needs uniqueness of the positive harmonic function of the killed walk (classical, finite variance). Say "следовательно".
10. Bus ids (1794133756, 1794139939, 1794133839) not verifiable from the garage; tone toward the Antigravity facet is fair.

**Checklist**

1. step_same = killed triangular convolution — **OK.** On a scratch copy: max |step_same − exact ∫(1−|x−y|)f| ≤ 10⁻¹⁶ (d=0..2; 6·10⁻¹² for d=3, my quadrature), mass after one step from uniform = 5/6 exactly (1/6 killed), no j=−1 cell, no factor.
2. V(x) = x + E_x[−S_τ] harmonic, V(0) = E[H] — **OK.** E_x[V(S₁);S₁≥0] = E_x[S₁;S₁≥0] + E_x[−S_τ;τ>1] = E_x[S₁] + E_x[−S_τ] = V(x); continuous steps make strict/weak equal.
3. E[H] = σ/√2 from 1−φ = |1−χ₊|² — **OK.** Needs symmetric, continuous (so χ₋(ξ) = χ₊(−ξ) and ladder heights proper), finite variance (⇒ E[H] < ∞); all hold. Independent sanity: Sparre Andersen P₀(τ>n) = C(2n,n)/4ⁿ ~ 1/√(πn) and the tail √(2/π)V(0)/(σ√n) force V(0) = σ/√2.
4. C = √(2/π)/σ³ — **OK** as matching; no factor-2 trap (one-sided τ, V = V̂ by symmetry, continuous). Confirmed by (2) above and by 12·0.9772050238 = 11.7264603 = √(2/π)·6^{3/2}. Citation pending, as the note says.
5. Grid stand — **OK** in substance: g = ∫₀^{1−t}(1−t−s)s ds = (1−t)³/6 ✓; reflection harmless (X ≫ σ√n); corner quadratic fine (w ∈ C²); MC correct but see item 5 above; the n-sequence description is wrong (item 1).
6. Harness — **OK.** Identical extraction path; legval(−1) = Σ(−1)^d v1_leg[d] (both 0.4082482904644); kinf weights (2d+1) correct: B_inf[0,0] = 6.3608420636 = A·v1_leg[0]²; W·B_inf symmetric to 3·10⁻¹¹; rank-1 residual 2.5·10⁻¹¹; V₁(0) stable to 10⁻⁹ across Richardson subsets.
7. V₁/V = √2 pointwise — **OK** (independent method, 7 digits at u=0, ½, 1; raw h=0.01 at ¼, ¾ 1.41419–1.41420).
8. A = C/2 — **OK.** C/A = 2.000000; C·σ²/2 = 1/(σ√(2π)) = √(3/π) = 0.9772050238.
9. Wording — **NOT OK** on items 1, 4, 7 above; sections named correctly but incompletely (item 3).
10. Else — **NOT OK**: §6.4 p.2 prefactor (item 2); garage incomplete (item 6). Replacement bucket text needs the "modulo C" qualifier (item 4).
