#!/usr/bin/env python3
"""
noncommutative_quartet_word_traces_and_chiral_cocycle_2026_11_18.py

Self-contained stdlib-only verification module (Revision 108, Lane A, 2026-11-18 Evening).
Provides an independent two-handed operator-theoretic closure of Revision 107 (`seq 250` & `seq 251`,
`READ-0110..0112`, and Phi-Hausmaster's `1795001059` & `1795014344`) in exact `Fraction` arithmetic
(`python3 -I -B -W error`, zero external or sibling imports):

1. Theorem 1 (Finite-Rank Cubic-Subspace Trace Reduction on V_0 = span{x, x^2, x^3} &
   Two-Handed Proof of All-(p,q) Sherman-Morrison Mixed-Trace Symmetry):
   - Because every pairwise difference Delta_{beta,alpha} = G_Xi^{(beta)} - G_Xi^{(alpha)} maps
     L^2(0, 1) into the 3-dimensional cubic polynomial subspace V_0 := span{x, x^2, x^3},
     telescoping any non-commutative word W = G_{alpha_1} G_{alpha_2} ... G_{alpha_n} against
     G_alpha^n and applying cyclicity of trace yields the finite-rank operator
         K_W := \\sum_{j=1}^n Delta_{alpha_j, alpha} G_alpha^{n-j} G_{alpha_1} ... G_{alpha_{j-1}} : L^2(0, 1) -> V_0,
     whose exact L^2(0, 1) trace equals the 3x3 matrix trace on V_0 = span{x, x^2, x^3}:
         Tr_{L^2(0,1)}(W) - Tr_{L^2(0,1)}(G_alpha^n) == Tr_{V_0}(K_W|_{V_0}) = \\sum_{m=1}^3 [x^m](K_W(x^m)),
     evaluated directly from the 3x3 primal differential BVP solver `solve_primal_bvp_alpha_poly`
     with ZERO reference to e_alpha(z), R_{beta/alpha}(z), or w_0^*(s).
   - For all 6 pairs (alpha, beta) and all 1 <= p, q <= 4 with p + q <= 5 (including the non-cyclic
     anchor (p, q) = (2, 2)), Hand 2 (the 3x3 BVP operator trace Tr_{V_0}(K_{G_alpha^p G_beta^q}|_{V_0}))
     matches Hand 1 (the Sherman-Morrison series convolution -C_{alpha,beta}(p, q)) identically,
     proving Tr(G_alpha^p G_beta^q) == Tr(G_beta^q G_alpha^p) by two independent routes.

2. Theorem 2 (Inversion-Invariant 2x2 Hankel Determinant Law for the Non-Cyclic 4-Word Gap):
   - For every pair (alpha, beta), the non-commutativity splitting between the 2-block trace
     Tr(G_alpha^2 G_beta^2) and the alternating 4-letter trace Tr(G_alpha G_beta G_alpha G_beta)
     equals the 2x2 Hankel determinant (Turanian) of R_{beta/alpha}(z) = (beta! e_beta(z))/(alpha! e_alpha(z)):
         Tr(G_alpha^2 G_beta^2) - Tr(G_alpha G_beta G_alpha G_beta)
           == -(1/2) Tr([G_alpha, G_beta]^2) == r_1 r_3 - r_2^2,
     which is algebraically invariant under series inversion R(z) -> R(z)^{-1} (alpha <-> beta)
     and strictly positive across all 6 pairs:
       (0,1): 971/367783416000,   (0,2): 9403/7355668320000,  (0,3): 8773/20977276320000,
       (1,2): 19/1471133664000,   (1,3): 713/80912351520000,  (2,3): 1/4045617576000.

3. Theorem 3 (Chiral 3-Domain Triangle Asymmetry, Tetrahedral Stokes Cocycle d^2 = 0,
   and 4-Domain Hamiltonian Barycentric Pencil Closure):
   - For any three distinct domains (alpha, beta, gamma), the chiral orientation asymmetry
     A_{alpha,beta,gamma} := Tr(G_alpha G_beta G_gamma) - Tr(G_alpha G_gamma G_beta) = Tr(G_alpha [G_beta, G_gamma])
     is non-zero, totally antisymmetric under S_3, independent of the positive branch F(s), and
     given by the 3x3 Vandermonde-like determinant of c_k^{(alpha)} = alpha! / (4k + alpha)! (k = 1, 2):
         A_{alpha,beta,gamma} == -det [[1, 1, 1], [c_1^{(alpha)}, c_1^{(beta)}, c_1^{(gamma)}], [c_2^{(alpha)}, c_2^{(beta)}, c_2^{(gamma)}]],
     with the four oriented tetrahedral face values
         (A_{0,1,2}, A_{0,1,3}, A_{0,2,3}, A_{1,2,3})
           = (1/20412000, 37/523908000, 1/43659000, 1/785862000)
     obeying the exact 4-simplex Stokes cocycle identity A_{1,2,3} - A_{0,2,3} + A_{0,1,3} - A_{0,1,2} == 0.
   - Across all 24 permutations of the 4-domain Hamiltonian product G_{pi(0)} G_{pi(1)} G_{pi(2)} G_{pi(3)}
     (6 distinct cyclic classes), the sum of Hand-2 operator traces
         \\sum_{pi in S_4} Tr(G_{pi(0)} G_{pi(1)} G_{pi(2)} G_{pi(3)} - G_1^4) == -85901771/1039447879470000
     matches Hand 1 (the [z_0 z_1 z_2 z_3] logarithmic derivative coefficient of the 4-variable
     entire Barycentric Fredholm Pencil) identically.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def poly_trim(p: List[Fraction]) -> List[Fraction]:
    q = list(p)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q if q else [Fraction(0)]


def poly_add(
    p: List[Fraction],
    q: List[Fraction],
    a: Fraction = Fraction(1),
    b: Fraction = Fraction(1),
) -> List[Fraction]:
    n = max(len(p), len(q))
    res = [Fraction(0)] * n
    for i in range(len(p)):
        res[i] += a * p[i]
    for i in range(len(q)):
        res[i] += b * q[i]
    return poly_trim(res)


def series_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = min(len(a), len(b))
    res = [Fraction(0)] * n
    for i in range(n):
        res[i] = sum((a[j] * b[i - j] for j in range(i + 1)), Fraction(0))
    return res


def series_inv(a: List[Fraction]) -> List[Fraction]:
    assert a[0] != 0
    n = len(a)
    inv = [Fraction(0)] * n
    inv[0] = Fraction(1) / a[0]
    for i in range(1, n):
        s = sum((a[j] * inv[i - j] for j in range(1, i + 1)), Fraction(0))
        inv[i] = -s / a[0]
    return inv


def solve_primal_bvp_alpha_poly(alpha: int, f_poly: List[Fraction]) -> List[Fraction]:
    """
    Direct 4th-order boundary-value solver on Dom_alpha:
        L_Xi u = f_poly,   u(0) = 0,   B_j(u) = 0  (for all j != alpha)
    in exact Fraction by solving the 3x3 boundary linear system for (c_1, c_2, c_3),
    without referencing e_alpha(z), R_{beta/alpha}(z), or w_0^*(s).
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

    def eval_B(j: int, p: List[Fraction]) -> Fraction:
        u0_1 = sum(c for c in p)
        u1_0 = p[1] if len(p) > 1 else Fraction(0)
        u1_1 = sum(m * c for m, c in enumerate(p))
        u2_0 = Fraction(2) * p[2] if len(p) > 2 else Fraction(0)
        u2_1 = sum(m * (m - 1) * c for m, c in enumerate(p))
        u3_0 = Fraction(6) * p[3] if len(p) > 3 else Fraction(0)
        u3_1 = sum(m * (m - 1) * (m - 2) * c for m, c in enumerate(p))
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


def apply_word_poly(word: Sequence[int], p: List[Fraction]) -> List[Fraction]:
    """Apply operator product G_{w_0} G_{w_1} ... G_{w_{n-1}} to polynomial p."""
    cur = p
    for a in reversed(word):
        cur = solve_primal_bvp_alpha_poly(a, cur)
    return cur


def word_trace_diff_V0(word: Sequence[int], ref_alpha: int) -> Fraction:
    """
    Hand 2 (Direct 3x3 Cubic-Subspace BVP Operator Trace):
    Compute Tr_{L^2(0,1)}(G_{w_0} ... G_{w_{n-1}} - G_{ref_alpha}^n) as the exact 3x3 matrix trace
    of K_W = \\sum_{j=1}^n Delta_{w_{j-1}, ref_alpha} G_{ref_alpha}^{n-j} G_{w_0} ... G_{w_{j-2}}
    restricted to V_0 = span{x, x^2, x^3}.
    """
    n = len(word)
    tr = Fraction(0)
    for m_basis in (1, 2, 3):
        em = [Fraction(0)] * m_basis + [Fraction(1)]
        acc = [Fraction(0)]
        for j in range(n):
            aj = word[j]
            if aj == ref_alpha:
                continue
            cur = apply_word_poly(word[:j], em)
            for _ in range(n - 1 - j):
                cur = solve_primal_bvp_alpha_poly(ref_alpha, cur)
            d_cur = poly_add(
                solve_primal_bvp_alpha_poly(aj, cur),
                solve_primal_bvp_alpha_poly(ref_alpha, cur),
                Fraction(1),
                Fraction(-1),
            )
            acc = poly_add(acc, d_cur)
        assert len(acc) <= 4 and acc[0] == 0, f"Image escaped V_0 = span(x, x^2, x^3): {acc}"
        if m_basis < len(acc):
            tr += acc[m_basis]
    return tr


def verify_all() -> Dict[str, object]:
    K_max = 6
    e_series = {
        a: [Fraction(math.factorial(a), math.factorial(4 * m + a)) for m in range(K_max + 2)]
        for a in (0, 1, 2, 3)
    }
    ratios: Dict[Tuple[int, int], List[Fraction]] = {}
    for a in (0, 1, 2, 3):
        inv_ea = series_inv(e_series[a])
        for b in (0, 1, 2, 3):
            ratios[(b, a)] = series_mul(e_series[b], inv_ea)

    # Full single-domain Newton traces Tr(G_alpha^n) for n = 1..5
    f_pos = [Fraction(1)] + [
        Fraction((-4) ** m, 2 * math.factorial(4 * m)) for m in range(1, K_max + 2)
    ]
    fp_p = [Fraction(m) * f_pos[m] for m in range(1, K_max + 2)]
    fp_q = series_mul(fp_p, series_inv(f_pos[:K_max + 1]))
    zeta_cant = [-fp_q[n - 1] for n in range(1, K_max + 1)]

    tr_single: Dict[int, List[Fraction]] = {}
    for a in (0, 1, 2, 3):
        ea = e_series[a]
        eap = [Fraction(m) * ea[m] for m in range(1, K_max + 2)]
        q = series_mul(eap, series_inv(ea[:K_max + 1]))
        z_neg = [((-1) ** (k + 1)) * q[k - 1] for k in range(1, K_max + 1)]
        tr_single[a] = [zeta_cant[n - 1] + ((-1) ** n) * z_neg[n - 1] for n in range(1, K_max + 1)]

    # 1. THEOREM 1: Two-Handed Verification of All-(p,q) Mixed Traces Tr(G_a^p G_b^q)
    #    for all 6 pairs (a < b) and 1 <= p, q <= 4 with p + q <= 5
    two_block_checked = 0
    non_cyclic_22_table: Dict[str, str] = {}
    for a in range(4):
        for b in range(a + 1, 4):
            r_ba = ratios[(b, a)]
            r_ab = ratios[(a, b)]
            for p_deg in range(1, 5):
                for q_deg in range(1, 6 - p_deg):
                    n_tot = p_deg + q_deg
                    # Hand 1: Sherman-Morrison series convolution C_{a,b}(p, q) and C_{b,a}(q, p)
                    c_ab = sum(
                        Fraction(m_i + 1) * r_ba[p_deg + m_i + 1] * r_ab[q_deg - 1 - m_i]
                        for m_i in range(q_deg)
                    )
                    c_ba = sum(
                        Fraction(m_i + 1) * r_ab[q_deg + m_i + 1] * r_ba[p_deg - 1 - m_i]
                        for m_i in range(p_deg)
                    )
                    tr_hand1_ab = tr_single[a][n_tot - 1] - c_ab
                    tr_hand1_ba = tr_single[b][n_tot - 1] - c_ba
                    assert tr_hand1_ab == tr_hand1_ba

                    # Hand 2: Direct 3x3 BVP operator trace on V_0 = span{x, x^2, x^3}
                    word_ab = [a] * p_deg + [b] * q_deg
                    word_ba = [b] * q_deg + [a] * p_deg
                    diff_v0_ab = word_trace_diff_V0(word_ab, ref_alpha=a)
                    diff_v0_ba = word_trace_diff_V0(word_ba, ref_alpha=b)
                    assert diff_v0_ab == -c_ab, f"Hand 2 vs Hand 1 mismatch at ({a},{b}), p={p_deg}, q={q_deg}"
                    assert diff_v0_ba == -c_ba, f"Hand 2 vs Hand 1 mismatch at ({b},{a}), q={q_deg}, p={p_deg}"
                    tr_hand2_ab = tr_single[a][n_tot - 1] + diff_v0_ab
                    tr_hand2_ba = tr_single[b][n_tot - 1] + diff_v0_ba
                    assert tr_hand2_ab == tr_hand2_ba == tr_hand1_ab
                    two_block_checked += 1
                    if p_deg == 2 and q_deg == 2:
                        non_cyclic_22_table[f"({a},{b})"] = str(tr_hand2_ab)

    # 2. THEOREM 2: Inversion-Invariant 2x2 Hankel Determinant Law for Non-Cyclic 4-Word Gap
    #    Tr(G_a^2 G_b^2) - Tr(G_a G_b G_a G_b) == -(1/2) Tr([G_a, G_b]^2) == r_1 r_3 - r_2^2
    hankel_gaps: Dict[str, str] = {}
    for a in range(4):
        for b in range(a + 1, 4):
            r_ba = ratios[(b, a)]
            r_ab = ratios[(a, b)]
            hand1_gap_ab = r_ba[1] * r_ba[3] - (r_ba[2] ** 2)
            hand1_gap_ba = r_ab[1] * r_ab[3] - (r_ab[2] ** 2)
            assert hand1_gap_ab == hand1_gap_ba, "2x2 Hankel determinant must be inversion-invariant"

            d_a2b2 = word_trace_diff_V0([a, a, b, b], ref_alpha=a)
            d_abab = word_trace_diff_V0([a, b, a, b], ref_alpha=a)
            hand2_gap = d_a2b2 - d_abab
            assert hand2_gap == hand1_gap_ab
            hankel_gaps[f"({a},{b})"] = str(hand2_gap)

    assert hankel_gaps == {
        "(0,1)": "971/367783416000",
        "(0,2)": "9403/7355668320000",
        "(0,3)": "8773/20977276320000",
        "(1,2)": "19/1471133664000",
        "(1,3)": "713/80912351520000",
        "(2,3)": "1/4045617576000",
    }

    # 3. THEOREM 3: Chiral 3-Domain Triangle Asymmetry, Tetrahedral Stokes Cocycle d^2 = 0,
    #    and 4-Domain Hamiltonian Barycentric Pencil Closure
    c1 = {a: e_series[a][1] for a in (0, 1, 2, 3)}
    c2 = {a: e_series[a][2] for a in (0, 1, 2, 3)}
    chiral_triangles: Dict[str, str] = {}
    chiral_vals: Dict[Tuple[int, int, int], Fraction] = {}

    for a, b, c in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        r_ba = ratios[(b, a)]
        r_ca = ratios[(c, a)]
        # Hand 1: Closed-form 3-domain traces and 3x3 Vandermonde-like determinant
        hand1_diff_abc = -r_ba[3] - r_ca[3] + r_ca[1] * r_ba[2]
        hand1_diff_acb = -r_ba[3] - r_ca[3] + r_ba[1] * r_ca[2]
        hand1_asym = hand1_diff_abc - hand1_diff_acb
        det3_val = -((c1[b] - c1[a]) * (c2[c] - c2[a]) - (c1[c] - c1[a]) * (c2[b] - c2[a]))
        assert hand1_asym == det3_val

        # Hand 2: Direct 3x3 BVP operator trace on V_0 = span{x, x^2, x^3}
        hand2_diff_abc = word_trace_diff_V0([a, b, c], ref_alpha=a)
        hand2_diff_acb = word_trace_diff_V0([a, c, b], ref_alpha=a)
        assert hand2_diff_abc == hand1_diff_abc
        assert hand2_diff_acb == hand1_diff_acb
        hand2_asym = hand2_diff_abc - hand2_diff_acb
        assert hand2_asym == det3_val
        chiral_vals[(a, b, c)] = hand2_asym
        chiral_triangles[f"({a},{b},{c})"] = str(hand2_asym)

    assert chiral_triangles == {
        "(0,1,2)": "1/20412000",
        "(0,1,3)": "37/523908000",
        "(0,2,3)": "1/43659000",
        "(1,2,3)": "1/785862000",
    }
    # Verify 4-simplex Stokes boundary cocycle identity d^2 = 0 on tetrahedron (0, 1, 2, 3):
    stokes_cocycle = (
        chiral_vals[(1, 2, 3)]
        - chiral_vals[(0, 2, 3)]
        + chiral_vals[(0, 1, 3)]
        - chiral_vals[(0, 1, 2)]
    )
    assert stokes_cocycle == Fraction(0)

    # All 6 cyclic Hamiltonian 4-domain words G_0 G_{pi(1)} G_{pi(2)} G_{pi(3)} vs 4-variable Barycentric Pencil
    hamiltonian_6_diffs: Dict[str, str] = {}
    sum_6_cyclic = Fraction(0)
    for perm in itertools.permutations((1, 2, 3)):
        w = (0,) + perm
        d_w = word_trace_diff_V0(w, ref_alpha=1)
        hamiltonian_6_diffs[str(w)] = str(d_w)
        sum_6_cyclic += d_w
    hand2_sum_24 = Fraction(4) * sum_6_cyclic

    # Hand 1: [z_0 z_1 z_2 z_3] of -t d/dt ln(1 + \sum_{k=1}^4 t^k R_k(z) Z^{k-1}) at t = 1
    R_forms = {k: {a: ratios[(a, 1)][k] for a in range(4)} for k in range(1, 5)}
    Z_form = {a: Fraction(1) for a in range(4)}

    def coeff_z0123(forms: List[Dict[int, Fraction]]) -> Fraction:
        return sum(
            (forms[0][p[0]] * forms[1][p[1]] * forms[2][p[2]] * forms[3][p[3]] for p in itertools.permutations(range(4))),
            Fraction(0),
        )

    hand1_pencil_z0123 = Fraction(4) * (
        -coeff_z0123([R_forms[4], Z_form, Z_form, Z_form])
        + Fraction(1, 2)
        * (
            Fraction(2) * coeff_z0123([R_forms[1], R_forms[3], Z_form, Z_form])
            + coeff_z0123([R_forms[2], R_forms[2], Z_form, Z_form])
        )
        - coeff_z0123([R_forms[1], R_forms[1], R_forms[2], Z_form])
        + Fraction(1, 4) * coeff_z0123([R_forms[1], R_forms[1], R_forms[1], R_forms[1]])
    )
    assert hand2_sum_24 == hand1_pencil_z0123 == Fraction(-85901771, 1039447879470000)

    return {
        "module": "noncommutative_quartet_word_traces_and_chiral_cocycle_2026_11_18.py",
        "revision": 108,
        "theorem_1_cubic_subspace_trace_reduction_and_pq_symmetry": {
            "two_block_pairs_checked_p_plus_q_le_5": two_block_checked,
            "non_cyclic_p2_q2_symmetric_traces": non_cyclic_22_table,
        },
        "theorem_2_inversion_invariant_hankel_4word_gaps": hankel_gaps,
        "theorem_3_chiral_triangle_cocycle_and_hamiltonian_pencil": {
            "chiral_3domain_triangle_asymmetries": chiral_triangles,
            "tetrahedral_stokes_cocycle_sum": str(stokes_cocycle),
            "hamiltonian_4domain_cyclic_trace_shifts_from_G1_4": hamiltonian_6_diffs,
            "sum_24_hamiltonian_trace_shifts_two_handed": str(hand2_sum_24),
        },
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_path = Path(__file__).with_name("noncommutative_quartet_word_traces_and_chiral_cocycle_2026_11_18_results.json")
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, ensure_ascii=False))
