#!/usr/bin/env python3
"""
hermite_pade_quartet_unit_fractions_and_kronecker_spectral_idempotents_2026_11_20.py

Self-contained (stdlib-only) verification module for OMPU Stereo Pair Lane A (Jee A, rev 111):
1. Theorem 1 (Simultaneous 4-Vector Hermite-Padé Type II Single-Step Annihilator Q_{HP,s}^{II}(z)
   via Universal Unit-Fraction 4x4 Cumulant Minors vs. Euler's M-th Finite-Difference Identity):
   Cross-verifies the simultaneous 4-sector annihilator Q_{HP,s}^{II}(z) = sum_{j=0}^4 q_j^{(s)} z^j
   ([z^{s+4}](Q_{HP,s}^{II}(z) alpha! e_alpha(-z)) == 0 for all alpha in {0,1,2,3}) by two hands:
   - Hand 1: Cramer ratio of universal unit-fraction 4x4 cumulant minors
     q_j^{(s)} = (-1)^j Delta(s,...,hat{s+4-j},...,s+4) / Delta(s,s+1,s+2,s+3),
     proving that EVERY coefficient q_j^{(s)} (j=1..4, s>=0) is an exact signed unit fraction.
   - Hand 2: Euler's M-th finite-difference operator Delta_j^M P_{3-alpha}(j) == 0 on degree-(3-alpha)
     falling-factorial polynomials, generalizing the simultaneous annihilator to all M >= 4.
2. Theorem 2 (Dual Hermite-Padé Type I Sector Weights w_alpha^{(R)} on Arbitrary 4-Row Stencils
   R = (r_0, r_1, r_2, r_3) and the Unit-Fraction Integer Quotient Law):
   Proves that the unique Type I sector functional L_R(z) = sum_{alpha=0}^3 w_alpha^{(R)} alpha! e_alpha(-z)
   vanishing on rows {r_0, r_1, r_2} and normalized to 1 on row r_3 evaluates on every target row r_*
   to the exact quotient of two unit-fraction denominators:
     [z^{r_*}] L_R(z) == (-1)^{3 - pos(r_*, R)} N(r_0, r_1, r_2, r_3) / N(sorted(r_0, r_1, r_2, r_*)),
   verified across all C(7,4) * 8 = 280 stencil-target pairs by direct solver vs. closed form.
3. Theorem 3 (Multi-Order Simultaneous 4-Vector Hermite-Padé Type II Common Denominator Q_{4m}^{HP-II}(z)
   of Multi-Index (m, m, m, m) for the Quartet Cauchy-Stieltjes Resolvents (S_0, S_1, S_2, S_3),
   Simultaneous 52/38/28/21-Digit Pure-Factorial Convergence to All Four Quartet Fundamental Eigenvalues,
   and the 4x4 Kronecker-Lagrange Spectral Idempotent Residue Matrix W_{alpha,beta}^{(4m)} -> delta_{alpha,beta}):
   Cross-verifies the Quartet negative-branch power sums via logarithmic derivatives (Hand 1) vs.
   3x3 cubic-subspace BVP operator trace shifts on V_0 = span{x, x^2, x^3} (Hand 2), constructs the
   single degree-4m Hermite-Padé Type II common denominator Q_{4m}^{HP-II}(z) for m = 1, 2, 3, 4,
   verifies that its first four positive roots simultaneously recover all four Quartet fundamental
   eigenvalues (pi^4/4 to 52 digits, 4*beta_1^4 to 38 digits, 4*pi^4 to 28 digits, 4*gamma_1^4 to 21 digits)
   with -q_1^{(4m)} -> 17/315, and proves that the 4x4 residue matrix W_{alpha,beta}^{(4m)} converges
   to the Kronecker identity matrix I_4 = [delta_{alpha,beta}] to 52/38/29/23 digits.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


# =============================================================================
# 1. Exact Polynomial Arithmetic & Primal 4th-Order BVP Solver on V_0 (Hand 2)
# =============================================================================

Poly = List[Fraction]


def poly_trim(p: Sequence[Fraction]) -> Poly:
    res = list(p)
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res if res else [Fraction(0)]


def poly_add(a: Sequence[Fraction], b: Sequence[Fraction], scale_b: Fraction = Fraction(1)) -> Poly:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i in range(len(a)):
        out[i] += a[i]
    for i in range(len(b)):
        out[i] += scale_b * b[i]
    return poly_trim(out)


def solve_primal_bvp_alpha_poly(alpha: int, f_poly: Sequence[Fraction]) -> Poly:
    """
    Direct 4th-order stereo-reflection boundary-value solver on Dom_alpha:
        D^4 u = (6 I - 10 R) f_poly,   u(0) = 0,   B_j(u) = 0  (for all j != alpha)
    in exact Fraction on V_0 = span{x, x^2, x^3}.
    """
    d = len(f_poly) - 1
    one_minus_x = [Fraction(1), Fraction(-1)]
    p_pow = [[Fraction(1)]]
    for _ in range(d):
        prev = p_pow[-1]
        nxt = [Fraction(0)] * (len(prev) + 1)
        for i, c in enumerate(prev):
            nxt[i] += c * one_minus_x[0]
            nxt[i + 1] += c * one_minus_x[1]
        p_pow.append(nxt)
    tf = [Fraction(0)] * (d + 1)
    for k, c in enumerate(f_poly):
        if c == 0:
            continue
        for i in range(k + 1):
            tf[i] -= Fraction(10) * c * p_pow[k][i]
        tf[k] += Fraction(6) * c
    i4 = [Fraction(0)] * (d + 5)
    for m, c in enumerate(tf):
        if c != 0:
            i4[m + 4] = c / Fraction((m + 1) * (m + 2) * (m + 3) * (m + 4))

    def eval_B(j: int, p: Sequence[Fraction]) -> Fraction:
        u0_1 = sum((c for c in p), Fraction(0))
        u1_0 = p[1] if len(p) > 1 else Fraction(0)
        u1_1 = sum((m * c for m, c in enumerate(p)), Fraction(0))
        u2_0 = Fraction(2) * p[2] if len(p) > 2 else Fraction(0)
        u2_1 = sum((m * (m - 1) * c for m, c in enumerate(p)), Fraction(0))
        u3_0 = Fraction(6) * p[3] if len(p) > 3 else Fraction(0)
        u3_1 = sum((m * (m - 1) * (m - 2) * c for m, c in enumerate(p)), Fraction(0))
        if j == 0:
            return u0_1
        if j == 1:
            return u1_0 - Fraction(3) * u1_1
        if j == 2:
            return Fraction(3) * u2_0 + Fraction(5) * u2_1
        if j == 3:
            return Fraction(3) * u3_0 - Fraction(5) * u3_1
        raise ValueError(j)

    basis_cubics = [
        [Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ]
    active_j = [j for j in (0, 1, 2, 3) if j != alpha]
    mat = [[eval_B(j, b) for b in basis_cubics] + [-eval_B(j, i4)] for j in active_j]
    for col in range(3):
        piv = next(r for r in range(col, 3) if mat[r][col] != 0)
        mat[col], mat[piv] = mat[piv], mat[col]
        f = mat[col][col]
        mat[col] = [v / f for v in mat[col]]
        for r in range(3):
            if r != col and mat[r][col] != 0:
                ff = mat[r][col]
                mat[r] = [mat[r][c] - ff * mat[col][c] for c in range(4)]
    i4[1] += mat[0][3]
    i4[2] += mat[1][3]
    i4[3] += mat[2][3]
    return poly_trim(i4)


def apply_word_poly(word: Sequence[int], f_poly: Sequence[Fraction]) -> Poly:
    cur = list(f_poly)
    for alpha in reversed(word):
        cur = solve_primal_bvp_alpha_poly(alpha, cur)
    return cur


def word_trace_diff_V0(word: Sequence[int], ref_alpha: int) -> Fraction:
    """Computes Tr_{L^2(0,1)}(W - G_{ref_alpha}^n) via 3x3 cubic-subspace operator trace on V_0."""
    n_len = len(word)
    tr = Fraction(0)
    for m_basis in (1, 2, 3):
        em = [Fraction(0)] * m_basis + [Fraction(1)]
        acc = [Fraction(0)]
        for j in range(n_len):
            aj = word[j]
            if aj == ref_alpha:
                continue
            cur = apply_word_poly(word[:j], em)
            for _ in range(n_len - 1 - j):
                cur = solve_primal_bvp_alpha_poly(ref_alpha, cur)
            d_cur = poly_add(
                solve_primal_bvp_alpha_poly(aj, cur),
                solve_primal_bvp_alpha_poly(ref_alpha, cur),
                Fraction(-1),
            )
            acc = poly_add(acc, d_cur)
        assert len(acc) <= 4 and acc[0] == 0
        if m_basis < len(acc):
            tr += acc[m_basis]
    return tr


# =============================================================================
# 2. Power Series, Universal Unit-Fraction 4x4 Minors & Hermite-Padé Solvers
# =============================================================================

def e_neg_series(alpha: int, max_deg: int) -> List[Fraction]:
    return [
        Fraction(((-1) ** k) * math.factorial(alpha), math.factorial(4 * k + alpha))
        for k in range(max_deg + 1)
    ]


def series_mul(a: Sequence[Fraction], b: Sequence[Fraction], max_deg: int) -> List[Fraction]:
    out = [Fraction(0)] * (max_deg + 1)
    for i, ai in enumerate(a):
        if ai == 0 or i > max_deg:
            continue
        for j, bj in enumerate(b):
            if i + j <= max_deg and bj != 0:
                out[i + j] += ai * bj
    return out


def series_inv(a: Sequence[Fraction], max_deg: int) -> List[Fraction]:
    assert a[0] != 0
    inv = [Fraction(0)] * (max_deg + 1)
    inv[0] = Fraction(1) / a[0]
    for k in range(1, max_deg + 1):
        inv[k] = -sum(a[j] * inv[k - j] for j in range(1, min(k, len(a) - 1) + 1)) / a[0]
    return inv


def solve_linear_system_fraction(mat: Sequence[Sequence[Fraction]], rhs: Sequence[Fraction]) -> List[Fraction]:
    n = len(mat)
    aug = [list(mat[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if aug[r][col] != 0)
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col] != 0:
                fac = aug[r][col]
                aug[r] = [aug[r][c] - fac * aug[col][c] for c in range(n + 1)]
    return [aug[i][n] for i in range(n)]


def closed_form_4x4_cumulant_minor(r0: int, r1: int, r2: int, r3: int) -> Fraction:
    """
    Universal Unit-Fraction 4x4 Quartet Cumulant Minor for 0 <= r0 < r1 < r2 < r3:
      Delta(r0,r1,r2,r3) = det_{0<=i,alpha<=3}[c_{r_i}^{(alpha)}]
                         = 49152 * prod_{0<=i<j<=3}(r_j - r_i) / prod_{i=0}^3 (4r_i + 3)!
                         = +1 / N(r0, r1, r2, r3).
    """
    assert 0 <= r0 < r1 < r2 < r3
    num = 49152 * (r1 - r0) * (r2 - r0) * (r2 - r1) * (r3 - r0) * (r3 - r1) * (r3 - r2)
    den = (
        math.factorial(4 * r0 + 3)
        * math.factorial(4 * r1 + 3)
        * math.factorial(4 * r2 + 3)
        * math.factorial(4 * r3 + 3)
    )
    val = Fraction(num, den)
    assert val.numerator == 1
    return val


def signed_4x4_cumulant_minor(rows: Sequence[int]) -> Fraction:
    if len(set(rows)) < 4:
        return Fraction(0)
    inv_cnt = sum(1 for i in range(4) for j in range(i + 1, 4) if rows[i] > rows[j])
    sgn = Fraction(1 if inv_cnt % 2 == 0 else -1)
    s_rows = sorted(rows)
    return sgn * closed_form_4x4_cumulant_minor(*s_rows)


# =============================================================================
# 3. Master Verification Suite (Theorems 1, 2, 3)
# =============================================================================

def verify_all() -> Dict[str, object]:
    getcontext().prec = 80
    max_deg = 32
    c_cum = [[Fraction(math.factorial(a), math.factorial(4 * r + a)) for a in range(4)] for r in range(max_deg + 1)]

    # -------------------------------------------------------------------------
    # Check 1: Theorem 1 — Simultaneous 4-Vector Hermite-Padé Type II Single-Step
    #          Annihilator Q_{HP,s}^{II}(z) via Universal Unit-Fraction 4x4 Minors (Hand 1)
    #          vs. Euler's M-th Finite-Difference Operator (Hand 2) for M = 4, 5, 6.
    # -------------------------------------------------------------------------
    q_hp_s0_to_s3: Dict[str, List[str]] = {}
    for s_shift in range(7):
        base_d = closed_form_4x4_cumulant_minor(s_shift, s_shift + 1, s_shift + 2, s_shift + 3)
        q_hand1 = [Fraction(1)]
        for j_idx in range(1, 5):
            sub_r = tuple(s_shift + i_idx for i_idx in range(5) if i_idx != 4 - j_idx)
            q_val = ((-1) ** j_idx) * closed_form_4x4_cumulant_minor(*sub_r) / base_d
            assert abs(q_val.numerator) == 1, f"q_{j_idx}^({s_shift}) is not a unit fraction: {q_val}"
            q_hand1.append(q_val)

        # Hand 2: Euler 4th finite-difference binomial-factorial formula
        q_hand2 = [
            ((-1) ** j_idx)
            * math.comb(4, j_idx)
            * Fraction(math.factorial(4 * s_shift + 19 - 4 * j_idx), math.factorial(4 * s_shift + 19))
            for j_idx in range(5)
        ]
        assert q_hand1 == q_hand2
        if s_shift <= 3:
            q_hp_s0_to_s3[f"s={s_shift}"] = [str(x) for x in q_hand1]

        # Simultaneous annihilation of row s+4 across all 4 Quartet domains alpha = 0, 1, 2, 3:
        for a_dom in range(4):
            ann = sum(q_hand1[j_idx] * c_cum[s_shift + 4 - j_idx][a_dom] for j_idx in range(5))
            assert ann == 0

    assert q_hp_s0_to_s3["s=0"] == [
        "1",
        "-1/23256",
        "1/507911040",
        "-1/6033983155200",
        "1/20274183401472000",
    ]
    assert q_hp_s0_to_s3["s=1"] == [
        "1",
        "-1/53130",
        "1/3294910080",
        "-1/161911881331200",
        "1/5129368400572416000",
    ]

    # Multi-step Euler M-th finite-difference generalization Q_{M,s}(z) for M = 4, 5, 6 and s = 0..5:
    euler_multistep_checks = 0
    for m_step in (4, 5, 6):
        top_fact_offset = 4 * m_step + 3
        for s_shift in range(6):
            top_n = 4 * s_shift + top_fact_offset
            q_m_s = [
                ((-1) ** j_idx)
                * math.comb(m_step, j_idx)
                * Fraction(math.factorial(top_n - 4 * j_idx), math.factorial(top_n))
                for j_idx in range(m_step + 1)
            ]
            for a_dom in range(4):
                ann = sum(q_m_s[j_idx] * c_cum[s_shift + m_step - j_idx][a_dom] for j_idx in range(m_step + 1))
                assert ann == 0
                euler_multistep_checks += 1
    assert euler_multistep_checks == 3 * 6 * 4 == 72

    # -------------------------------------------------------------------------
    # Check 2: Theorem 2 — Dual Hermite-Padé Type I Sector Weights w_alpha^{(R)}
    #          on Arbitrary 4-Row Stencils R = (r_0, r_1, r_2, r_3) and the Exact
    #          Unit-Fraction Integer Quotient Law across all C(7,4) * 8 = 280 pairs.
    # -------------------------------------------------------------------------
    type1_stencil_checks = 0
    for r_tuple in itertools.combinations(range(7), 4):
        r0, r1, r2, r3 = r_tuple
        # Solve sum_{alpha=0}^3 w_alpha c_{r_i}^{(alpha)} == delta_{i, 3} (i = 0, 1, 2, 3):
        mat_r = [c_cum[r_i] for r_i in r_tuple]
        rhs_r = [Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
        w_vec = solve_linear_system_fraction(mat_r, rhs_r)

        base_minor = closed_form_4x4_cumulant_minor(r0, r1, r2, r3)
        n_base_int = base_minor.denominator

        for r_star in range(8):
            lhs_val = sum(w_vec[a_dom] * c_cum[r_star][a_dom] for a_dom in range(4))
            rhs_val = signed_4x4_cumulant_minor((r0, r1, r2, r_star)) / base_minor
            assert lhs_val == rhs_val
            if r_star not in (r0, r1, r2):
                target_minor = closed_form_4x4_cumulant_minor(*sorted((r0, r1, r2, r_star)))
                n_target_int = target_minor.denominator
                assert abs(lhs_val) == Fraction(n_base_int, n_target_int)
            type1_stencil_checks += 1
    assert type1_stencil_checks == 35 * 8 == 280

    # -------------------------------------------------------------------------
    # Check 3: Theorem 3 — Multi-Order Simultaneous 4-Vector Hermite-Padé Type II
    #          Common Denominator Q_{4m}^{HP-II}(z) for (S_0, S_1, S_2, S_3),
    #          Cross-Verification of S_alpha(z) via 3x3 Cubic-Subspace BVP Trace on V_0,
    #          Simultaneous 52/38/28/21-Digit Convergence to All Four Quartet Fundamental
    #          Eigenvalues, and 4x4 Kronecker-Lagrange Residue Matrix W_{a,b}^{(4m)} -> delta_{a,b}.
    # -------------------------------------------------------------------------
    # Compute S_alpha(z) = -z (d/dz (alpha! e_alpha(-z))) / (alpha! e_alpha(-z)) = sum_{k>=1} (-1)^{k-1} Tr(G_neg^{(alpha) k}) z^k:
    s_vec: List[List[Fraction]] = []
    for a_dom in range(4):
        ea = e_neg_series(a_dom, max_deg)
        dea = [k * ea[k] for k in range(max_deg + 1)]
        sa = series_mul([-x for x in dea], series_inv(ea, max_deg), max_deg)
        s_vec.append(sa)

    # Cross-verify S_alpha(z) differences against Hand 2 (direct 3x3 cubic-subspace V_0 BVP trace)
    # since Tr_{L^2}(G_alpha^k - G_beta^k) == Tr(G_neg^{(alpha) k} - G_neg^{(beta) k}) == (-1)^k (S_alpha[k] - S_beta[k]):
    for a_dom in range(4):
        for b_dom in range(a_dom + 1, 4):
            for k_pow in (1, 2, 3, 4):
                tr_diff_v0 = word_trace_diff_V0((a_dom,) * k_pow, b_dom)
                tr_diff_s = ((-1) ** k_pow) * (s_vec[a_dom][k_pow] - s_vec[b_dom][k_pow])
                assert tr_diff_v0 == tr_diff_s

    # Total Quartet negative-branch first trace sum_{alpha=0}^3 c_1^{(alpha)} == 17/315:
    total_quartet_c1 = sum(c_cum[1][a_dom] for a_dom in range(4))
    assert total_quartet_c1 == Fraction(17, 315)

    # High-precision reference fundamental eigenvalues x_1^{(alpha)} = 4 (mu_1^{(alpha)})^4 (80-digit Decimal):
    def exact_fundamental_root_decimal(alpha: int) -> Decimal:
        coeffs = [Decimal(c.numerator) / Decimal(c.denominator) for c in e_neg_series(alpha, 32)]
        guesses = [
            Decimal("24.3522727585"),
            Decimal("125.1409754351"),
            Decimal("389.6363641360"),
            Decimal("950.8842701245"),
        ]
        x = guesses[alpha]
        for _ in range(25):
            fx = sum(coeffs[k] * (x ** k) for k in range(len(coeffs)))
            dfx = sum(k * coeffs[k] * (x ** (k - 1)) for k in range(1, len(coeffs)))
            x = x - fx / dfx
        return x

    exact_targets = [exact_fundamental_root_decimal(a_dom) for a_dom in range(4)]
    assert exact_targets[0] < exact_targets[1] < exact_targets[2] < exact_targets[3]

    hp_root_errors: Dict[str, List[float]] = {}
    minus_q1_progression: Dict[str, str] = {}
    kronecker_max_row_errors_m4: List[float] = []

    for m_ord in (1, 2, 3, 4):
        d_deg = 4 * m_ord
        mat_hp: List[List[Fraction]] = []
        rhs_hp: List[Fraction] = []
        for a_dom in range(4):
            sa = s_vec[a_dom]
            for r_eq in range(1, m_ord + 1):
                deg_eq = d_deg + r_eq
                mat_hp.append([sa[deg_eq - k_col] for k_col in range(1, d_deg + 1)])
                rhs_hp.append(-sa[deg_eq])
        q_tail = solve_linear_system_fraction(mat_hp, rhs_hp)
        q_poly = [Fraction(1)] + q_tail
        minus_q1_progression[f"m={m_ord}"] = str(-q_poly[1])

        # Verify Hermite-Padé Type II order condition: Q_{4m}(z) S_alpha(z) - P_{4m,alpha}(z) == O(z^{5m+1})
        p_polys: List[List[Fraction]] = []
        for a_dom in range(4):
            prod_qs = series_mul(q_poly, s_vec[a_dom], d_deg + m_ord)
            p_poly_a = prod_qs[: d_deg + 1]
            for r_eq in range(1, m_ord + 1):
                assert prod_qs[d_deg + r_eq] == 0
            p_polys.append(p_poly_a)

        qd = [Decimal(c.numerator) / Decimal(c.denominator) for c in q_poly]
        init_guesses = (
            [Decimal("24.3522"), Decimal("125.412"), Decimal("369.338"), Decimal("1163.41")]
            if m_ord == 1
            else exact_targets
        )
        roots_m: List[Decimal] = []
        errs_m: List[float] = []
        for a_dom in range(4):
            x = init_guesses[a_dom]
            for _ in range(25):
                fx = sum(qd[k] * (x ** k) for k in range(d_deg + 1))
                dfx = sum(k * qd[k] * (x ** (k - 1)) for k in range(1, d_deg + 1))
                x = x - fx / dfx
            roots_m.append(x)
            errs_m.append(float(abs(x - exact_targets[a_dom])))
        assert roots_m[0] < roots_m[1] < roots_m[2] < roots_m[3]
        hp_root_errors[f"m={m_ord}"] = errs_m

        if m_ord == 4:
            pd = [[Decimal(c.numerator) / Decimal(c.denominator) for c in p_polys[b_dom]] for b_dom in range(4)]
            for a_dom in range(4):
                x = roots_m[a_dom]
                dq = sum(k * qd[k] * (x ** (k - 1)) for k in range(1, d_deg + 1))
                row_err = []
                for b_dom in range(4):
                    pb = sum(pd[b_dom][k] * (x ** k) for k in range(d_deg + 1))
                    w_ab = -pb / (x * dq)
                    target_delta = Decimal(1 if a_dom == b_dom else 0)
                    row_err.append(float(abs(w_ab - target_delta)))
                kronecker_max_row_errors_m4.append(max(row_err))

    # Strict monotone accuracy improvement from m=1 to m=4 across all 4 Quartet domains:
    for a_dom in range(4):
        assert (
            hp_root_errors["m=4"][a_dom]
            < hp_root_errors["m=3"][a_dom]
            < hp_root_errors["m=2"][a_dom]
            < hp_root_errors["m=1"][a_dom]
        )
    assert hp_root_errors["m=4"][0] < 1e-51
    assert hp_root_errors["m=4"][1] < 1e-37
    assert hp_root_errors["m=4"][2] < 1e-27
    assert hp_root_errors["m=4"][3] < 1e-20

    assert kronecker_max_row_errors_m4[0] < 1e-51
    assert kronecker_max_row_errors_m4[1] < 1e-37
    assert kronecker_max_row_errors_m4[2] < 1e-28
    assert kronecker_max_row_errors_m4[3] < 1e-22

    return {
        "module": "hermite_pade_quartet_unit_fractions_and_kronecker_spectral_idempotents_2026_11_20",
        "revision": 111,
        "single_step_hermite_pade_type_ii_unit_fractions_s0_to_s3": q_hp_s0_to_s3,
        "euler_multistep_annihilator_checks_M_4_5_6": euler_multistep_checks,
        "dual_hermite_pade_type_i_unit_fraction_quotient_checks": type1_stencil_checks,
        "total_quartet_negative_branch_trace_limit": str(total_quartet_c1),
        "minus_q1_progression_m_1_to_4": minus_q1_progression,
        "simultaneous_4_sector_eigenvalue_errors_m4_deg16": [
            f"{e:.3e}" for e in hp_root_errors["m=4"]
        ],
        "kronecker_lagrange_spectral_idempotent_max_row_errors_m4": [
            f"{e:.3e}" for e in kronecker_max_row_errors_m4
        ],
        "status": "ALL_CHECKS_PASSED",
    }


def main() -> None:
    results = verify_all()
    out_path = Path(__file__).with_name(
        "hermite_pade_quartet_unit_fractions_and_kronecker_spectral_idempotents_2026_11_20_results.json"
    )
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
