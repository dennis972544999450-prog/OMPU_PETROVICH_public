#!/usr/bin/env python3
r"""Exact 4-Vector Hermite-Pade Mahler Duality, 5-Term Jacobi-Perron Recurrences,
and Simultaneous 4-Sector Spectral Convergence for the Beam Quartet (stdlib-only).

Module 22 of Lane B (Den-b, ompu-7f698bd908, Friday morning 2026-11-20, rev 110).
Closes the joint [=~ seam from seq 257 (Jee A, b0949197...) and seq 258 (Den-b, d84b2749...),
building directly atop the universal unit-fraction 4x4 minor theorem (49152) and
extending the 1-step Type II annihilator Q_{HP,s}^{II}(z) of READ-0122 (commit d30e3ae)
to the full arbitrary-order diagonal Hermite-Pade Type I / Type II ladder.

Four theorems verified by two independent hands in exact rational (Fraction) and
100-digit Decimal arithmetic (zero external or local imports; python3 -I -B -W error):
  Theorem 1: Hermite (1873) contour generator I_M(t) = (1/2pi i) oint e^{tu}/(u^4-1)^{M+1} du
             for Type I polynomials A_a^{(M)}(z), exact unit-fraction Mahler determinant
             det A_M(z) = (-1)^M z^M / (4^{4M+6} M!(M+1)!(M+2)!(M+3)!), and 2-line proof of
             Jee A's universal constant 49152 = 1 / det A_0.
  Theorem 2: Closed-form 5-term Jacobi-Perron recurrence for Type I polynomials A_a^{(M)}(z),
             exact dual Mahler matrix step W_{M+1}(z) = W_M(z) U_M(z) for W_M = adj(A_M),
             and exact scalar 5-term dual Jacobi-Perron recurrence for Type II vectors B^{(M)}(z).
  Theorem 3: Simultaneous Type II Hermite-Pade approximation B_a^{(M)} e_b - B_b^{(M)} e_a = O(z^{M+1})
             across all 6 quartet pairs at degree 3m (M = 4m), strict coefficient positivity
             (M = 1..20), exact match with S-fraction steps c_1^{(2,3)}=1/630, c_2^{(2,3)}=1/396,
             and 97-digit simultaneous Diophantine convergence to e_a(1)/e_0(1) at M = 16 (deg 12).
  Theorem 4: Exact rational Sturm theorem proof of 100% simple real positive roots for all 48
             Type II polynomials B_a^{(M)}(-x) (M = 1..12, 234 roots total), strict 4-sector
             cyclic root interlacing (M = 4, 8, 12), and 47-to-73-digit simultaneous spectral
             convergence to all four fundamental quartet eigenvalues 4*(mu_1^{(a)})^4 at M = 16.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
import hashlib
import json
from math import comb, factorial
from pathlib import Path

getcontext().prec = 110


# ---------------------------------------------------------------------------
# Exact rational polynomial helpers (lists of Fraction, low-to-high degree)
# ---------------------------------------------------------------------------
def p_trim(a):
    res = list(a)
    while res and res[-1] == 0:
        res.pop()
    return res


def p_add(a, b):
    n = max(len(a), len(b))
    out = [
        (a[i] if i < len(a) else Fraction(0)) + (b[i] if i < len(b) else Fraction(0))
        for i in range(n)
    ]
    return p_trim(out)


def p_sub(a, b):
    n = max(len(a), len(b))
    out = [
        (a[i] if i < len(a) else Fraction(0)) - (b[i] if i < len(b) else Fraction(0))
        for i in range(n)
    ]
    return p_trim(out)


def p_scale(a, s):
    if s == 0 or not a:
        return []
    return p_trim([x * s for x in a])


def p_mul(a, b):
    if not a or not b:
        return []
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if y != 0:
                out[i + j] += x * y
    return p_trim(out)


def p_mul_z(a, s):
    """Multiply polynomial a(z) by s * z."""
    if s == 0 or not a:
        return []
    return p_trim([Fraction(0)] + [x * s for x in a])


def det_poly_mat(mat):
    n = len(mat)
    if n == 1:
        return mat[0][0]
    if n == 2:
        return p_sub(p_mul(mat[0][0], mat[1][1]), p_mul(mat[0][1], mat[1][0]))
    total = []
    for c in range(n):
        if not mat[0][c]:
            continue
        sub = [[mat[r][j] for j in range(n) if j != c] for r in range(1, n)]
        term = p_mul(mat[0][c], det_poly_mat(sub))
        total = p_add(total, term) if c % 2 == 0 else p_sub(total, term)
    return total


def det_frac_mat(mat):
    n = len(mat)
    m = [row[:] for row in mat]
    sign = Fraction(1)
    det = Fraction(1)
    for col in range(n):
        piv = None
        for r in range(col, n):
            if m[r][col] != 0:
                piv = r
                break
        if piv is None:
            return Fraction(0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            sign = -sign
        pv = m[col][col]
        det *= pv
        for r in range(col + 1, n):
            if m[r][col] != 0:
                fac = m[r][col] / pv
                for j in range(col, n):
                    m[r][j] -= fac * m[col][j]
    return sign * det


# ---------------------------------------------------------------------------
# Theorem 1: Hermite (1873) contour generator for Type I polynomials A_a^{(M)}(z)
# ---------------------------------------------------------------------------
def inv_shifted_quartic_series(M):
    """Power series of G_M(v) = (4 + 6v + 4v^2 + v^3)^{-(M+1)} up to v^M."""
    base = [Fraction(4), Fraction(6), Fraction(4), Fraction(1)]
    P = [Fraction(1)] + [Fraction(0)] * M
    for _ in range(M + 1):
        nxt = [Fraction(0)] * (M + 1)
        for i in range(M + 1):
            if P[i] == 0:
                continue
            for k, c in enumerate(base):
                if i + k <= M:
                    nxt[i + k] += P[i] * c
        P = nxt
    G = [Fraction(0)] * (M + 1)
    G[0] = Fraction(1) / P[0]
    for n in range(1, M + 1):
        s = sum(P[k] * G[n - k] for k in range(1, n + 1))
        G[n] = -s / P[0]
    return G


def type1_row_contour(M):
    """Direct residue formula for [A_0^{(M)}(z), A_1^{(M)}(z), A_2^{(M)}(z), A_3^{(M)}(z)]."""
    G = inv_shifted_quartic_series(M)
    A = [[] for _ in range(4)]
    for j in range(M + 1):
        a = (-j - 1) % 4
        deg_z = (j + a - 3) // 4
        coeff = Fraction(4) * G[M - j] / factorial(j)
        while len(A[a]) <= deg_z:
            A[a].append(Fraction(0))
        A[a][deg_z] += coeff
    return [p_trim(poly) for poly in A]


# ---------------------------------------------------------------------------
# Theorem 2: Closed-form 5-term Jacobi-Perron recurrence (Type I & Dual Type II)
# ---------------------------------------------------------------------------
def jp_coeffs(M):
    """Closed-form rational coefficients for A^{(M+4)} = c3 A^{(M+3)} + c2 A^{(M+2)} + c1 A^{(M+1)} + d0 z A^{(M)}."""
    c1 = -Fraction((4 * M + 5) * (4 * M + 6) * (4 * M + 7), 64 * (M + 2) * (M + 3) * (M + 4))
    c2 = -Fraction(3 * (16 * M * M + 64 * M + 65), 16 * (M + 3) * (M + 4))
    c3 = -Fraction(3 * (2 * M + 5), 2 * (M + 4))
    d0 = Fraction(1, 256 * (M + 1) * (M + 2) * (M + 3) * (M + 4))
    return c1, c2, c3, d0


def build_type1_via_recurrence(M_max):
    rows = [type1_row_contour(m) for m in range(4)]
    for M in range(0, M_max - 3):
        c1, c2, c3, d0 = jp_coeffs(M)
        nxt = []
        for a in range(4):
            p = p_add(
                p_add(p_scale(rows[M + 3][a], c3), p_scale(rows[M + 2][a], c2)),
                p_add(p_scale(rows[M + 1][a], c1), p_mul_z(rows[M][a], d0)),
            )
            nxt.append(p)
        rows.append(nxt)
    return rows


def full_adjugate(A_rows, M):
    mat = [A_rows[M + i] for i in range(4)]
    W = [[[] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for j in range(4):
            sub = [[mat[r][c] for c in range(4) if c != a] for r in range(4) if r != j]
            cof = det_poly_mat(sub)
            if (a + j) % 2 == 1:
                cof = p_scale(cof, Fraction(-1))
            W[a][j] = cof
    return W


def build_type2_via_dual_matrix(A_rows, M_max):
    """Exact dual matrix evolution W_{M+1}(z) = W_M(z) U_M(z), returning B_list[M] = col 0 of W_M."""
    W = full_adjugate(A_rows, 0)
    B_list = [[W[a][0] for a in range(4)]]
    for M in range(0, M_max):
        c1, c2, c3, d0 = jp_coeffs(M)
        Wn = [[[] for _ in range(4)] for _ in range(4)]
        for a in range(4):
            Wn[a][0] = p_add(p_scale(W[a][0], c1), p_mul_z(W[a][1], -d0))
            Wn[a][1] = p_add(p_scale(W[a][0], c2), p_mul_z(W[a][2], -d0))
            Wn[a][2] = p_add(p_scale(W[a][0], c3), p_mul_z(W[a][3], -d0))
            Wn[a][3] = p_scale(W[a][0], Fraction(-1))
        W = Wn
        B_list.append([W[a][0] for a in range(4)])
    return B_list


# ---------------------------------------------------------------------------
# Theorem 4: Exact rational Sturm root counter & 100-digit Decimal root finder
# ---------------------------------------------------------------------------
def p_rem(a, b):
    rem = a[:]
    while len(rem) >= len(b) and rem:
        fac = rem[-1] / b[-1]
        shift = len(rem) - len(b)
        for i in range(len(b)):
            rem[shift + i] -= fac * b[i]
        rem = p_trim(rem)
    return rem


def sturm_positive_root_count(p_neg_x):
    """Exact number of distinct roots of p_neg_x(x) in (0, +inf) via Sturm's theorem."""
    if len(p_neg_x) <= 1:
        return 0
    seq = [p_neg_x[:]]
    deriv = [p_neg_x[i] * i for i in range(1, len(p_neg_x))]
    seq.append(p_trim(deriv))
    while len(seq[-1]) > 1:
        r = p_rem(seq[-2], seq[-1])
        if not r:
            break
        sc = abs(r[-1])
        seq.append([-x / sc for x in r])

    def sign_changes(vals):
        nz = [1 if v > 0 else -1 for v in vals if v != 0]
        return sum(1 for i in range(len(nz) - 1) if nz[i] * nz[i + 1] < 0)

    v0 = [poly[0] for poly in seq]
    vinf = [poly[-1] for poly in seq]
    return sign_changes(v0) - sign_changes(vinf)


def sturm_count_in_interval(seq, x_lo, x_hi):
    def eval_at(poly, x):
        v = Fraction(0)
        for c in reversed(poly):
            v = v * x + c
        return v

    def sign_changes(x):
        nz = []
        for poly in seq:
            v = eval_at(poly, x)
            if v != 0:
                nz.append(1 if v > 0 else -1)
        return sum(1 for i in range(len(nz) - 1) if nz[i] * nz[i + 1] < 0)

    return sign_changes(x_lo) - sign_changes(x_hi)


def build_sturm_seq(p_neg_x):
    seq = [p_neg_x[:]]
    deriv = [p_neg_x[i] * i for i in range(1, len(p_neg_x))]
    seq.append(p_trim(deriv))
    while len(seq[-1]) > 1:
        r = p_rem(seq[-2], seq[-1])
        if not r:
            break
        sc = abs(r[-1])
        seq.append([-x / sc for x in r])
    return seq


def isolate_all_positive_roots(p_neg_x):
    """Exact rational isolating intervals [lo, hi] for all positive roots via Sturm bisection."""
    seq = build_sturm_seq(p_neg_x)
    # Cauchy upper bound for positive roots
    lead = abs(p_neg_x[-1])
    ub = Fraction(1) + max(abs(c) / lead for c in p_neg_x[:-1])
    total = sturm_count_in_interval(seq, Fraction(0), ub)
    assert total == len(p_neg_x) - 1, f"Expected {len(p_neg_x)-1} real pos roots, got {total}"
    intervals = []

    def split(lo, hi, cnt):
        if cnt == 0:
            return
        if cnt == 1:
            intervals.append((lo, hi))
            return
        mid = (lo + hi) / 2
        # Check if mid itself is a root (virtually impossible for irreducible, handle cleanly)
        val_mid = Fraction(0)
        for c in reversed(p_neg_x):
            val_mid = val_mid * mid + c
        if val_mid == 0:
            intervals.append((mid, mid))
            eps = (hi - lo) / 1024
            split(lo, mid - eps, sturm_count_in_interval(seq, lo, mid - eps))
            split(mid + eps, hi, sturm_count_in_interval(seq, mid + eps, hi))
            return
        c_left = sturm_count_in_interval(seq, lo, mid)
        split(lo, mid, c_left)
        split(mid, hi, cnt - c_left)

    split(Fraction(0), ub, total)
    return intervals


def refine_interval(p_neg_x, lo, hi, target_gap):
    def sgn(x):
        v = Fraction(0)
        for c in reversed(p_neg_x):
            v = v * x + c
        return 1 if v > 0 else (-1 if v < 0 else 0)

    slo = sgn(lo)
    while hi - lo > target_gap:
        mid = (lo + hi) / 2
        sm = sgn(mid)
        if sm == 0:
            return (mid, mid)
        if slo * sm < 0:
            hi = mid
        else:
            lo, slo = mid, sm
    return (lo, hi)


def frac_to_dec(f):
    return Decimal(f.numerator) / Decimal(f.denominator)


def eval_dec_poly(p_dec, x):
    v = Decimal(0)
    dv = Decimal(0)
    for c in reversed(p_dec):
        dv = dv * x + v
        v = v * x + c
    return v, dv


def e_dec_and_deriv(a, x, terms=65):
    v = Decimal(0)
    dv = Decimal(0)
    xp = Decimal(1)
    for r in range(terms):
        sign = Decimal(-1) if r % 2 == 1 else Decimal(1)
        invf = Decimal(1) / Decimal(factorial(4 * r + a))
        v += sign * xp * invf
        if r >= 1:
            dv += sign * Decimal(r) * (xp / x) * invf
        xp *= x
    return v, dv


def e_dec_pos(a, z, terms=55):
    s = Decimal(0)
    zp = Decimal(1)
    for r in range(terms):
        s += zp / Decimal(factorial(4 * r + a))
        zp *= z
    return s


def main():
    M_max = 20
    # Build Type I via recurrence (Hand 1) and cross-check vs contour generator (Hand 2)
    A_rows = build_type1_via_recurrence(M_max + 4)

    # -----------------------------------------------------------------------
    # CHECK 1: Theorem 1 — Type I contour formula, exact order, leading 1/(4^M M!),
    #          unit-fraction Mahler determinant, and 49152 proof of Jee A's seq 257
    # -----------------------------------------------------------------------
    for M in range(0, 13):
        direct = type1_row_contour(M)
        assert A_rows[M] == direct, f"Recurrence vs contour mismatch at M={M}"
        # Leading coefficient check: sector a_lead = (-M-1)%4 has lead coeff 1/(4^M * M!)
        a_lead = (-M - 1) % 4
        expected_lead = Fraction(1, (4 ** M) * factorial(M))
        assert A_rows[M][a_lead][-1] == expected_lead, f"Lead coeff mismatch at M={M}"
        # Exact residual sum_a A_a^{(M)}(z) e_a(z) == sum_{n>=M} comb(n,M) z^n / (4n+3)!
        for n in range(M + 5):
            lhs = Fraction(0)
            for a in range(4):
                for d, c in enumerate(A_rows[M][a]):
                    if d <= n:
                        lhs += c / factorial(4 * (n - d) + a)
            rhs = Fraction(comb(n, M), factorial(4 * n + 3)) if n >= M else Fraction(0)
            assert lhs == rhs, f"Type I residual mismatch M={M}, n={n}"

    mahler_dets = {}
    for M in range(0, 10):
        mat = [A_rows[M + i] for i in range(4)]
        d_poly = det_poly_mat(mat)
        expected_coeff = Fraction(
            (-1) ** M,
            (4 ** (4 * M + 6)) * factorial(M) * factorial(M + 1) * factorial(M + 2) * factorial(M + 3),
        )
        expected_poly = [Fraction(0)] * M + [expected_coeff]
        assert d_poly == expected_poly, f"Mahler det mismatch at M={M}"
        assert abs(expected_coeff.numerator) == 1
        mahler_dets[str(M)] = str(expected_coeff)

    # 2-line proof of Jee A's universal constant 49152:
    # A_0(0) * [1/(4r+a)!]_{a,r=0..3} is upper triangular with diagonal 1/(4r+3)!
    A0_const = [[A_rows[i][a][0] if A_rows[i][a] else Fraction(0) for a in range(4)] for i in range(4)]
    E0_mat = [[Fraction(1, factorial(4 * r + a)) for r in range(4)] for a in range(4)]
    prod_0 = [
        [sum(A0_const[i][a] * E0_mat[a][r] for a in range(4)) for r in range(4)]
        for i in range(4)
    ]
    for i in range(4):
        for r in range(4):
            if r < i:
                assert prod_0[i][r] == 0
            elif r == i:
                assert prod_0[i][r] == Fraction(1, factorial(4 * r + 3))
    det_A0 = det_frac_mat(A0_const)
    det_E0 = det_frac_mat(E0_mat)
    assert det_A0 == Fraction(1, 49152)
    assert det_E0 == Fraction(49152, factorial(3) * factorial(7) * factorial(11) * factorial(15))
    # Multiply columns by a! (product 0!1!2!3! = 12 = prod_{i<j}(j-i)) to get Jee A's V_4:
    V4_from_mahler = det_E0 * Fraction(12)
    assert V4_from_mahler == Fraction(1, 2676176026524000000)

    # -----------------------------------------------------------------------
    # CHECK 2: Theorem 2 — Dual Mahler matrix step W_{M+1} = W_M U_M & scalar 5-term recurrence
    # -----------------------------------------------------------------------
    B_list = build_type2_via_dual_matrix(A_rows, M_max)
    # Cross-check against direct 3x3 cofactor adjugate at M = 0..9
    for M in range(0, 10):
        W_dir = full_adjugate(A_rows, M)
        assert B_list[M] == [W_dir[a][0] for a in range(4)], f"Dual step mismatch at M={M}"
        # Verify biorthogonality A_M(z) * B^{(M)}(z) = [det A_M(z), 0, 0, 0]^T
        for i in range(4):
            dot = []
            for a in range(4):
                dot = p_add(dot, p_mul(A_rows[M + i][a], B_list[M][a]))
            if i == 0:
                expected_coeff = Fraction(
                    (-1) ** M,
                    (4 ** (4 * M + 6)) * factorial(M) * factorial(M + 1) * factorial(M + 2) * factorial(M + 3),
                )
                assert dot == [Fraction(0)] * M + [expected_coeff]
            else:
                assert dot == []

    # Verify scalar 5-term dual Jacobi-Perron recurrence for M = 3..M_max-1
    for M in range(3, M_max):
        c1_m, _, _, d0_m = jp_coeffs(M)
        _, c2_m1, _, d0_m1 = jp_coeffs(M - 1)
        _, _, c3_m2, d0_m2 = jp_coeffs(M - 2)
        for a in range(4):
            rhs = p_scale(B_list[M][a], c1_m)
            rhs = p_add(rhs, p_mul_z(B_list[M - 1][a], -d0_m * c2_m1))
            rhs = p_add(rhs, p_mul([Fraction(0), Fraction(0), d0_m * d0_m1 * c3_m2], B_list[M - 2][a]))
            rhs = p_add(rhs, p_mul([Fraction(0), Fraction(0), Fraction(0), d0_m * d0_m1 * d0_m2], B_list[M - 3][a]))
            assert rhs == B_list[M + 1][a], f"Scalar 5-term dual recurrence mismatch at M={M}, a={a}"

    # -----------------------------------------------------------------------
    # CHECK 3: Theorem 3 — Simultaneous O(z^{M+1}) order across all 6 pairs,
    #          strict positivity (M=1..20), S-fraction links, & 97-digit z=1 convergence
    # -----------------------------------------------------------------------
    for M in range(1, M_max + 1):
        s0 = B_list[M][0][0]
        for a in range(4):
            norm_p = [c / s0 for c in B_list[M][a]]
            assert all(c > 0 for c in norm_p), f"Non-positive Type II coeff at M={M}, a={a}"
            assert norm_p[0] == Fraction(1, factorial(a))

    # Direct meeting with S-fraction staircase c_1^{(2,3)}=1/630, c_2^{(2,3)}=1/396:
    B1_2_norm = [c * 2 / B_list[1][0][0] for c in B_list[1][2]]
    B2_2_norm = [c * 2 / B_list[2][0][0] for c in B_list[2][2]]
    assert B1_2_norm == [Fraction(1), Fraction(1, 630)]
    assert B2_2_norm == [Fraction(1), Fraction(1, 396)]

    # Exact approximation order B_a^{(M)} e_b - B_b^{(M)} e_a = O(z^{M+1}) for all 6 pairs, M = 1..12
    for M in range(1, 13):
        for a in range(4):
            for b in range(a + 1, 4):
                first_nz = None
                for n in range(M + 3):
                    s = Fraction(0)
                    for k in range(n + 1):
                        ba = B_list[M][a][k] if k < len(B_list[M][a]) else Fraction(0)
                        bb = B_list[M][b][k] if k < len(B_list[M][b]) else Fraction(0)
                        s += ba / factorial(4 * (n - k) + b) - bb / factorial(4 * (n - k) + a)
                    if s != 0:
                        first_nz = n
                        break
                assert first_nz == M + 1, f"Order mismatch at M={M}, ({a},{b}): got {first_nz}"

    # Simultaneous 100-digit Diophantine convergence at z = 1
    e1_true = [e_dec_pos(a, Decimal(1)) for a in range(4)]
    z1_errors = {}
    for M in [4, 8, 12, 16]:
        vals = [sum(frac_to_dec(c) for c in B_list[M][a]) for a in range(4)]
        errs = [abs(vals[a] / vals[0] - e1_true[a] / e1_true[0]) for a in range(1, 4)]
        z1_errors[str(M)] = f"{max(errs):.3e}"
    assert Decimal(z1_errors["16"]) < Decimal("1e-96")

    # -----------------------------------------------------------------------
    # CHECK 4: Theorem 4 — Exact Sturm 100% real positive roots (M=1..12),
    #          strict 4-sector cyclic interlacing (M=4,8,12), & 47..73-digit spectral roots
    # -----------------------------------------------------------------------
    total_sturm_roots = 0
    for M in range(1, 13):
        for a in range(4):
            p = B_list[M][a]
            deg = len(p) - 1
            if deg == 0:
                continue
            s0 = p[0]
            p_neg = [(c / s0) * (-1 if k % 2 == 1 else 1) for k, c in enumerate(p)]
            cnt = sturm_positive_root_count(p_neg)
            assert cnt == deg, f"Non-real root detected at M={M}, a={a}: {cnt} != {deg}"
            total_sturm_roots += cnt

    # Strict 4-sector cyclic root interlacing via exact rational Sturm isolation at M = 4, 8, 12
    interlacing_verified = {}
    for M in [4, 8, 12]:
        m_deg = 3 * (M // 4)
        sector_intervals = []
        p_negs = []
        for a in range(4):
            p = B_list[M][a]
            s0 = p[0]
            p_neg = [(c / s0) * (-1 if k % 2 == 1 else 1) for k, c in enumerate(p)]
            p_negs.append(p_neg)
            ivs = isolate_all_positive_roots(p_neg)
            assert len(ivs) == m_deg
            sector_intervals.append(ivs)
        # Refine intervals until strict separation x_{k}^{(0)} < x_{k}^{(1)} < x_{k}^{(2)} < x_{k}^{(3)} < x_{k+1}^{(0)}
        chain = [(a, k) for k in range(m_deg) for a in range(4)]
        refined = [list(ivs) for ivs in sector_intervals]
        for idx in range(len(chain) - 1):
            a1, k1 = chain[idx]
            a2, k2 = chain[idx + 1]
            lo1, hi1 = refined[a1][k1]
            lo2, hi2 = refined[a2][k2]
            while hi1 >= lo2:
                gap1 = (hi1 - lo1) / 4
                gap2 = (hi2 - lo2) / 4
                lo1, hi1 = refine_interval(p_negs[a1], lo1, hi1, gap1)
                lo2, hi2 = refine_interval(p_negs[a2], lo2, hi2, gap2)
            refined[a1][k1] = (lo1, hi1)
            refined[a2][k2] = (lo2, hi2)
            assert hi1 < lo2, f"Interlacing failed at M={M}, ({a1},{k1}) vs ({a2},{k2})"
        interlacing_verified[str(M)] = {
            "degree_per_sector": m_deg,
            "strict_4_sector_chain_length": 4 * m_deg,
            "certified_rational_separation": True,
        }

    # 100-digit simultaneous spectral convergence to all 4 fundamental eigenvalues 4*(mu_1^{(a)})^4
    x_init = [Decimal("24.35"), Decimal("125.13"), Decimal("389.64"), Decimal("950.88")]
    x_exact = []
    for a in range(4):
        x = x_init[a]
        for _ in range(35):
            v, dv = e_dec_and_deriv(a, x)
            x -= v / dv
        x_exact.append(x)

    spectral_errors = {}
    for M in [8, 12, 16]:
        errs = {}
        for a in range(4):
            s0 = B_list[M][a][0]
            p_dec = [
                frac_to_dec(c / s0) * (Decimal(-1) if k % 2 == 1 else Decimal(1))
                for k, c in enumerate(B_list[M][a])
            ]
            x = x_exact[a]
            for _ in range(35):
                v, dv = eval_dec_poly(p_dec, x)
                x -= v / dv
            rel = abs(x - x_exact[a]) / x_exact[a]
            errs[f"alpha_{a}"] = f"{rel:.3e}"
        spectral_errors[str(M)] = errs

    assert Decimal(spectral_errors["16"]["alpha_0"]) < Decimal("1e-72")
    assert Decimal(spectral_errors["16"]["alpha_1"]) < Decimal("1e-61")
    assert Decimal(spectral_errors["16"]["alpha_2"]) < Decimal("1e-52")
    assert Decimal(spectral_errors["16"]["alpha_3"]) < Decimal("1e-46")

    # Save structured JSON certificate
    out_path = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    results = {
        "module": Path(__file__).name,
        "verdict": "ALL_CHECKS_PASSED",
        "theorem_1_mahler_determinants_unit_fractions": mahler_dets,
        "theorem_1_jee_a_constant_from_inv_det_A0": int(Fraction(1) / det_A0),
        "theorem_1_V4_vandermonde_volume": str(V4_from_mahler),
        "theorem_2_jacobi_perron_5term_type1_and_dual_type2_verified_up_to_M": M_max,
        "theorem_3_type2_strict_positivity_M_1_to_20": True,
        "theorem_3_s_fraction_bridge": {
            "2!*B_2^{(1)}(z)": [str(c) for c in B1_2_norm],
            "2!*B_2^{(2)}(z)": [str(c) for c in B2_2_norm],
        },
        "theorem_3_simultaneous_z1_max_ratio_error": z1_errors,
        "theorem_4_exact_sturm_100pct_real_positive_roots_M_1_to_12": {
            "polynomials_checked": 48,
            "total_simple_positive_roots_certified": total_sturm_roots,
        },
        "theorem_4_exact_rational_4_sector_cyclic_interlacing": interlacing_verified,
        "theorem_4_simultaneous_fundamental_eigenvalue_rel_errors": spectral_errors,
    }
    payload = json.dumps(results, indent=2, ensure_ascii=False) + "\n"
    out_path.write_text(payload, encoding="utf-8")
    res_sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    print("VERDICT: ALL_CHECKS_PASSED")
    print(f"SCRIPT_SHA256: {self_sha}")
    print(f"RESULTS_SHA256: {res_sha}")
    print(f"DET_A0={det_A0}, V4={V4_from_mahler}")
    assert total_sturm_roots == 234
    print(f"STURM_CERTIFIED_ROOTS(M=1..12)={total_sturm_roots}/234")
    print(f"Z1_ERR(M=16)={z1_errors['16']}")
    print(f"SPECTRAL_REL_ERRS(M=16)={spectral_errors['16']}")


if __name__ == "__main__":
    main()
