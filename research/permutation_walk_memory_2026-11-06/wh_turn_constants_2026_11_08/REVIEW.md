# Слепая рецензия (субагент Agent, модель сессии; ~11 мин, 19 вызовов инструментов)

Дано: notes.txt v1 (17:06), скрипты и .out; задача — опровергать. Пункты §5b/§3b/§6.1 и cos2_check добавлены ПОСЛЕ старта рецензии и ею не покрыты. Скрипты рецензента: /private/tmp/claude-501/blindrev_whturn_1645/ (не в гараже). Текст ниже — дословно последний ответ рецензента.

---

**Blind review: wh_turn_constants note (Anthropic 16:45, 08.11)**

I found no false mathematics. All of (A)–(D) hold up, and the P_3 correction is right. What I did find: one unproved claim stated as fact, one under-converged constant (c₁), and three small wording issues. I touched nothing in the garage; my own scripts are in `/private/tmp/claude-501/blindrev_whturn_1645/` (colloc.py, checks_b.py, checks_root.py, check_cos2.py, dP3.py).

For an independent baseline I wrote my own solver. It splits [0,X] into unit panels with Gauss nodes and integrates the kernel exactly by splitting at its kinks. This is a different method from the note's midpoint Nyström. Its results agree to 13–15 digits across four (X, nodes) settings.

**1. Theorem A, (TV)(u) = E[H]·P(H>u). CONFIRMED.**
- Checked each step: W₋ lives on (−1,0); the Laplace identity has the right sign; F(s) = E[H]/(sP(s)) because V = E[H]·U (renewal function of the ladder heights; up and down heights agree in law by symmetry); P ≠ 0 for Re s > 0, so the cancellation is allowed; Laplace inversion is unique.
- A second derivation by duality (pre-ladder occupation measure, then integration by parts) gives the same result.
- My solver: V(0) = 1/√12, ∫TV = 0.083333333333333, 12∫u·TV = 0.227350780091995 = δ₀.
- Cosmetic: the case "m = −1" of the moment formula comes from (TV)(0) = V(0), i.e. harmonicity at 0. The integral ∫u⁻¹·TV itself diverges.

**2. The reading of §6.3 and the closed forms (C). CONFIRMED.**
- A turn wipes out the pieces j ≥ 1, and the flip weight is q = T1. So P_m = ⟨V, T^m q⟩ / ⟨V, T^m 1⟩, with the profile ∝ V by the local limit theorem.
- I redid the algebra by hand: T²1 = 1/8 − x/6 + x⁴/24, and 1/8 + 1/50400 + 1/7200 = 1577/12600.
- P_max = 0.3151600751789 and P_min = 0.2793320207862, both from my solver and from my own Siegmund quadrature. These match the paper's 10 digits, which supports the "flip after m turns" reading.

**3. P_3 correction. CONFIRMED: the paper is wrong in the 8th decimal.**
- My solver computes P_3 directly, without Theorem A or any root sums: P_3 = 0.2851903760089, P_4 = 0.2842868188670.
- My own integrals for b₁, b₃, b₅ give the same P_3.
- P_3 − 71/252 = 0.0034443442629. So the paper's 0.28519033 and 0.00344430 should be corrected as the note says.

**4. Wording in §0. REFUTED, low.**
- §0 says P_3 needs "один-два интеграла Сигмунда". It needs three. The numerator of P_3 is E[13H/360 − H²/40 + H⁵/240 − H⁶/720 + H⁷/5040], which contains a₅ + a₆ and hence b₅(1 − δ₀) ≠ 0. §4's own rule ("one new constant per turn") agrees with three.

**5. Theorem B. CONFIRMED (one wording point).**
- Even coefficients, recomputed exactly: 1/60, 1/50400, −1/2268000, 73/27941760000.
- Odd coefficients: I derived the formula myself via a contour around the right half-plane, indented at 0. Signs and the (−1)^j factor are right.
- My quadrature: δ₀ = 0.227350780091995, b₃ = −9.910252776405e−4, b₅ = 3.672823253240e−6. The note's root sum gives b₅ = 3.67282325327531e−6.
- No roots are missing: the argument principle on −12Q/s² gives 0, 8, 28, 60, 188 zeros for R = 9, 20, 50, 100, 300, exactly 4 per listed w.
- The e^{−s/2} factor is numerically right. I built P(s) from my solver (via Theorem A) and compared it with E[H]·s·e^{Bs}·Π(1 − s/s_k).
  - With B = −1/2 and truncation tails accounted for, the ratio is 1 + 1.1e−6 at |s| = 3. That residual is exactly the tail of the truncated product.
  - With B = 0 the ratio would be 4.48 and 0.22.
- The factor can also be proved by citation. P is of exponential type and bounded on the imaginary axis, with indicator 0 to the right and ess sup H = 1 to the left. For such functions (Cartwright class), Lindelöf's theorem puts the exponential factor at the midpoint of the indicator segment [−1, 0], which gives e^{−s/2}. The note's "проверить" can be closed with a reference.
- Overstated dependence: only δ₀'s root formula needs the exponent. γ₃ and every b_j with j ≥ 2 follow from Hadamard alone, but the note's text says "Адамар + показатель e^{−s/2} дают … γ₃".

**6. Theorem D formula. Numerically CONFIRMED; the proof is UNCLEAR (medium).**
- The residue at 0 is right: P(−s)/P(s) = −exp(2δ₀s + …), so the double pole gives −2δ₀, which becomes δ₀/6.
- The residue at a simple zero is right: d/ds(s²Q) = 2(s − sinh s) = 4iw(1 − σ cos w).
- Moving the contour to the left is asserted but not justified. It looks provable (|P(−s)| ≤ 2 for Re s < 0, |P(s)| grows to the left of the zeros, cut horizontally between zeros), but the note does not do it.
- The note's own K sequence shrinks about 7.3× per doubling of K. Extrapolating it gives 0.0399585997291, which equals my solver's ⟨V,TV⟩ = 0.039958599729073.

**7. Precision of c₁. REFUTED, low.**
- The note's ⟨V,TV⟩ = 0.0399585997322 and c₁ = 0.46857293283 are not converged in K. The correct values are 0.0399585997291 and c₁ = 0.4685729327940.
- So the paper's c₁ = 0.468572932794 is the accurate one; the note's is 3.6e−11 too high.
- "Сходимость по K ~2e−11" is the change in ⟨V,TV⟩ from K = 750 to 1500. In c₁ units that change is 2.3e−10.
- The note should quote c₁ = 0.4685729328 as agreeing with the paper, not set it "против".

**8. "Это не конечная комбинация δ₀, γ₃, …" REFUTED as stated, medium.**
- This is unproved, and the reason given does not follow. ⟨V,(1−t)^k⟩ are finite combinations even though V is not a polynomial.
- It should be softened to "no reduction found", so it doesn't reach the paper as a claim.

**9. The cos²θ formula (marked "численно НЕ проверен"). CONFIRMED numerically.**
- (1/12)[δ₀ + (2/π)∫cos²θ/η² dη] = 0.0399585997371, against 0.0399585997291. The 8e−12 gap is at the limit of my quadrature.

**10. Numbers against the .out files. CONFIRMED.**
- Every number in the note matches its .out file.
- Cosmetic: "корни имеют |s| ≥ 4.5" is true, but the smallest |s_k| is 9.55. 4.5 is |Re s₁|.
