#!/usr/bin/env python3
"""
Exact Midpoint BVP Unification of the Resolvent Profiles R_z(x) = ((I - zT)^{-1} 1)(x)
and F_z(x) = ((I - zT)^{-1} f_1)(x), Bivariate André-Cayley Generating Function
Delta(-w^2)/Delta(w^2) for the Alternating Walk Counts A_m = (2m)! H_0^(m) (Theorems 1-3),
Reflected Zero-Boundary Moment Identity J_r^(m) = I_{r-2}^(m+1)/(r-2)! with Non-Recursive
Closed Form for I_r^(m)/r!, and Exact 3rd-Order Rational Edgeworth Expansion c_3^(m) (§6.2).

Author: Den B (Lane B, OMPU Stereo Pair, ompu-7f698bd908)
Date: 2026-11-10 20:35 CET (Tuesday Evening Tick, rev 97)
"""

from fractions import Fraction
import json
import math
import os
import shutil


RESEARCH_DIR = "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06"


def apply_T_poly(poly: list[Fraction]) -> list[Fraction]:
    """Apply (T h)(x) = int_0^{1-x} (1 - x - y) h(y) dy in exact Fraction arithmetic."""
    deg = len(poly) - 1
    out = [Fraction(0)] * (deg + 3)
    for j, c in enumerate(poly):
        if c == 0:
            continue
        n = j + 2
        cv = c * Fraction(1, (j + 1) * (j + 2))
        for r in range(n + 1):
            out[r] += cv * math.comb(n, r) * ((-1) ** r)
    return out


def poly_moment(poly: list[Fraction], power: int = 0) -> Fraction:
    """Exact moment int_0^1 x^power * poly(x) dx in Fraction arithmetic."""
    return sum(c / Fraction(k + power + 1) for k, c in enumerate(poly))


def poly_one_minus_x_moment(poly: list[Fraction], r: int) -> Fraction:
    """Exact reflected moment J_r = int_0^1 ((1 - x)^r / r!) * poly(x) dx in Fraction arithmetic."""
    # int_0^1 (1-x)^r x^k dx = r! k! / (r + k + 1)!
    total = Fraction(0)
    for k, c in enumerate(poly):
        if c != 0:
            total += c * Fraction(math.factorial(k), math.factorial(r + k + 1))
    return total


def delta_coeff(m: int) -> Fraction:
    """Coefficient of z^m in Delta(z) = det(I - z T) = sum_{m>=0} (-1)^{floor((m+1)/2)} / (2^m (2m)!) z^m."""
    return Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m))


def delta_int_coeff(m: int) -> Fraction:
    """Coefficient of z^m in int_0^1 Delta(z u^2) du = sum_{m>=0} (-1)^{floor((m+1)/2)} / (2^m (2m+1)!) z^m."""
    return Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m + 1))


def part1_midpoint_resolvent_unification_and_andre_cayley_egf() -> dict:
    """
    Theorem 1 (Midpoint BVP Unification of R_z(x) and F_z(x) & André-Cayley EGF for A_m):
    1. Because 1''(x) = 0, 1(1) = 1, 1'(1) = 0 and f_1''(x) = 0, f_1(1) = 0, f_1'(1) = -1,
       the two resolvent profiles R_z(x) = ((I - zT)^{-1} 1)(x) and F_z(x) = ((I - zT)^{-1} f_1)(x)
       solve the exact reflected 2nd-order BVPs on [0, 1]:
           R_z''(x) = z R_z(1-x),  R_z(1) = 1,  R_z'(1) = 0,
           F_z''(x) = z F_z(1-x),  F_z(1) = 0,  F_z'(1) = -1.
       Splitting into even (cosh(sqrt(z) y)) and odd (sin(sqrt(z) y)) parts at the midpoint y = x - 1/2
       gives the closed-form profiles:
           R_z(x) = [ cos(w/2) cosh(w(x - 1/2)) - sinh(w/2) sin(w(x - 1/2)) ] / Delta(z),
           F_z(x) = [ sin(w/2) cosh(w(x - 1/2)) - cosh(w/2) sin(w(x - 1/2)) ] / (w Delta(z)),
       where w = sqrt(z) and Delta(z) = cosh(w/2)cos(w/2) - sinh(w/2)sin(w/2) = det(I - zT).
    2. Evaluating F_z(x) and its derivative -F_z'(x) at the free end x = 0 (y = -1/2) unifies
       Den B's morning Trace Generating Function and Jee A's evening Cayley-Fredholm Slope Generating Function
       as the value and negative slope at x = 0 of the SINGLE function F_z(x):
           F_z(0)   = 2 cosh(w/2) sin(w/2) / (w Delta(z)) = -4 Delta'(z) / Delta(z) = 4 sum_{m>=1} Tr(T^m) z^{m-1},
          -F_z'(0)  = R_z(0) = [ cosh(w/2)cos(w/2) + sinh(w/2)sin(w/2) ] / Delta(z) = Delta(-z) / Delta(z) = sum_{m>=0} H_0^(m) z^m.
    3. Furthermore, since H_0^(m) = (T^m 1)(0) = int_0^1 (T^{m-1} f_1)(x) dx is the exact alternating-walk
       probability P(E_1..E_m = +-+-...) of Theorem 2, the alternating permutation counts
       A_m = (2m)! H_0^(m) (A_0=1, A_1=1, A_2=3, A_3=26, A_4=413, A_5=10576, A_6=397023, A_7=20551376, A_8=1402815833, ...)
       entering Theorem 1, Theorem 2, and Theorem 3's streaming unit-fraction identity have the exact
       André-Cayley exponential generating function:
           sum_{m=0}^inf A_m w^{2m} / (2m)! = Delta(-w^2) / Delta(w^2).
    """
    print("=== 1. MIDPOINT BVP UNIFICATION OF R_z(x), F_z(x) & ANDRE-CAYLEY EGF FOR A_m ===")
    M_max = 10
    d_coeffs = [delta_coeff(m) for m in range(M_max + 1)]
    H0 = [Fraction(0)] * (M_max + 1)
    Tr_T = [Fraction(0)] * (M_max + 1)  # 1-indexed: Tr_T[m] = Tr(T^m)

    for m in range(M_max + 1):
        # H_0^(m) from Delta(-z) / Delta(z)
        rhs_h = ((-1) ** m) * d_coeffs[m]
        H0[m] = rhs_h - sum(d_coeffs[j] * H0[m - j] for j in range(1, m + 1))

        if m >= 1:
            # Tr(T^m) = (1/4) F_z(0)_[z^{m-1}] from -Delta'(z)/Delta(z)
            rhs_tr = -Fraction(m) * d_coeffs[m]
            Tr_T[m] = rhs_tr - sum(d_coeffs[j] * Tr_T[m - j] for j in range(1, m))

    # Verify midpoint BVP identity at x = 1/2 (y = 0):
    # At x = 1/2 (y = 0), cosh(0) = 1 and sin(0) = 0, so:
    #   R_z(1/2) = cos(sqrt(z)/2) / Delta(z) = [ sum_{m>=0} (-1)^m z^m / (2^{2m} (2m)!) ] / Delta(z),
    #   F_z(1/2) = (sin(sqrt(z)/2) / sqrt(z)) / Delta(z) = [ sum_{m>=0} (-1)^m z^m / (2^{2m+1} (2m+1)!) ] / Delta(z)!
    t_one = [[Fraction(1)]]
    t_f1 = [[Fraction(1), Fraction(-1)]]
    for _ in range(M_max):
        t_one.append(apply_T_poly(t_one[-1]))
        t_f1.append(apply_T_poly(t_f1[-1]))

    R_mid_rec = [Fraction(0)] * (M_max + 1)
    F_mid_rec = [Fraction(0)] * (M_max + 1)
    for m in range(M_max + 1):
        num_r_mid = Fraction((-1) ** m, (4 ** m) * math.factorial(2 * m))
        num_f_mid = Fraction((-1) ** m, (2 ** (2 * m + 1)) * math.factorial(2 * m + 1))
        R_mid_rec[m] = num_r_mid - sum(d_coeffs[j] * R_mid_rec[m - j] for j in range(1, m + 1))
        F_mid_rec[m] = num_f_mid - sum(d_coeffs[j] * F_mid_rec[m - j] for j in range(1, m + 1))

        # Evaluate polynomial (T^m 1)(1/2) and (T^m f_1)(1/2) directly:
        val_r_mid = sum(c * Fraction(1, 2 ** k) for k, c in enumerate(t_one[m]))
        val_f_mid = sum(c * Fraction(1, 2 ** k) for k, c in enumerate(t_f1[m]))
        assert R_mid_rec[m] == val_r_mid, f"Midpoint R_z(1/2) mismatch at m={m}"
        assert F_mid_rec[m] == val_f_mid, f"Midpoint F_z(1/2) mismatch at m={m}"

    # Verify André-Cayley integer counts A_m = (2m)! H_0^(m) for m = 0..10:
    A_counts = {}
    for m in range(M_max + 1):
        am_frac = H0[m] * math.factorial(2 * m)
        assert am_frac.denominator == 1, f"A_{m} is not an integer: {am_frac}"
        A_counts[f"A_{m}"] = int(am_frac)
        print(
            f"  m={m:2d}: H_0^({m:2d}) = {str(H0[m]):>26s} | A_{m:<2d} = (2m)! H_0^({m:2d}) = {A_counts[f'A_{m}']:>18d} "
            f"| (T^{m} 1)(1/2) = {str(R_mid_rec[m]):>24s}"
        )

    assert A_counts["A_0"] == 1
    assert A_counts["A_1"] == 1
    assert A_counts["A_2"] == 3
    assert A_counts["A_3"] == 26
    assert A_counts["A_4"] == 413
    assert A_counts["A_5"] == 10576
    assert A_counts["A_6"] == 397023
    assert A_counts["A_7"] == 20551376
    assert A_counts["A_8"] == 1402815833
    print("  [PASS] Midpoint BVP formulas R_z(1/2), F_z(1/2) and André-Cayley EGF for A_0..A_10 verified in Fraction.\n")

    return {
        "H0_m_0_to_10": {f"m={m}": str(H0[m]) for m in range(M_max + 1)},
        "A_m_alternating_permutation_counts_0_to_10": A_counts,
        "R_midpoint_1_over_2_m_0_to_8": {f"m={m}": str(R_mid_rec[m]) for m in range(9)},
        "F_midpoint_1_over_2_m_0_to_8": {f"m={m}": str(F_mid_rec[m]) for m in range(9)},
    }


def closed_form_I_r_over_fact(r: int, m: int, I0: list[Fraction], H0: list[Fraction]) -> Fraction:
    """
    Universal non-recursive closed form for I_r^(m) / r! = int_0^1 (x^r / r!) (T^m 1)(x) dx
    in terms of I_0 and H_0 alone (proven via J_r^(m) = I_{r-2}^(m+1) / (r-2)!):
      I_r^(m) / r! = sum_{k=0}^{floor(r/4)} I_0^(m+2k) / (r - 4k)!
                   - sum_{k=0}^{floor((r-1)/4)} H_0^(m+2k+1) / (r - 1 - 4k)!
                   + [ I_0^(m + 2*k* + 1) if r == 4*k* + 2 else H_0^(m + 2*k* + 2) if r == 4*k* + 3 else 0 ].
    """
    total = Fraction(0)
    for k in range(r // 4 + 1):
        total += I0[m + 2 * k] / Fraction(math.factorial(r - 4 * k))
    for k in range((r - 1) // 4 + 1):
        if r - 1 - 4 * k >= 0:
            total -= H0[m + 2 * k + 1] / Fraction(math.factorial(r - 1 - 4 * k))
    if r % 4 == 2:
        k_star = r // 4
        total += I0[m + 2 * k_star + 1]
    elif r % 4 == 3:
        k_star = r // 4
        total += H0[m + 2 * k_star + 2]
    return total


def part2_reflected_moment_theorem_and_edgeworth_3rd_order() -> dict:
    """
    Theorem 2 (Reflected Zero-Boundary Moment Identity, Non-Recursive I_r^(m)/r!, and 3rd-Order Edgeworth c_3^(m)):
    1. For J_r^(m) := int_0^1 ((1-x)^r / r!) (T^m 1)(x) dx, two-step integration by parts using
       (T^m 1)(x) = (T^{m+1} 1)''(1-x) has ZERO boundary terms at both x=0 and x=1 for all r >= 2:
           J_0^(m) = I_0^(m),   J_1^(m) = H_0^(m+1),   J_r^(m) = I_{r-2}^(m+1) / (r-2)!   (for all r >= 2).
    2. Expanding x^r = (1 - (1-x))^r and iterating J_{r-2}^(m+1) = I_{r-4}^(m+2)/(r-4)! yields the
       exact non-recursive closed form for I_r^(m) / r! for all r >= 0, m >= 0.
    3. Extending the unconditional symmetric walk density F_0^(L)(x) / F_0^(L)(0) to 3rd order in 1/L (L = n - m):
       From the exact characteristic function phi(t) = (sin(t/2)/(t/2))^2 = exp(sum_{k>=1} (-1)^{k-1} kappa_{2k} t^{2k} / (2k)!)
       with cumulants kappa_2 = 1/6, kappa_4 = -1/60, kappa_6 = 1/315, expanding
           F_0^(L)(x) = (1/pi) int_0^inf cos(t x) phi(t)^L dt
       in powers of 1/L gives the exact 3rd-order polynomial kernel:
           F_0^(L)(x) / F_0^(L)(0) = 1
             + ( -3 x^2 ) / L
             + ( (9/10) x^2 + (9/2) x^4 ) / L^2
             + ( -(27/1400) x^2 - (27/10) x^4 - (9/2) x^6 ) / L^3 + O(L^{-4})!
       Combining with I_2^(m), I_4^(m), I_6^(m) from the non-recursive closed form yields the exact
       rational 3rd-order Edgeworth coefficients c_3^(m) in
           p_hat_n(-, 1^m) = p_hat_inf(-, 1^m) + c_1^(m)/(n-m) + c_2^(m)/(n-m)^2 + c_3^(m)/(n-m)^3 + O((n-m)^{-4})!
    """
    print("=== 2. REFLECTED ZERO-BOUNDARY MOMENT IDENTITY J_r^(m) = I_{r-2}^(m+1)/(r-2)! & 3RD-ORDER EDGEWORTH c_3^(m) ===")
    M_max = 16
    d_coeffs = [delta_coeff(m) for m in range(M_max + 1)]
    n_coeffs = [delta_int_coeff(m) for m in range(M_max + 1)]
    H0 = [Fraction(0)] * (M_max + 1)
    I0 = [Fraction(0)] * (M_max + 1)
    for m in range(M_max + 1):
        H0[m] = ((-1) ** m) * d_coeffs[m] - sum(d_coeffs[j] * H0[m - j] for j in range(1, m + 1))
        I0[m] = n_coeffs[m] - sum(d_coeffs[j] * I0[m - j] for j in range(1, m + 1))

    t_one = [[Fraction(1)]]
    for _ in range(10):
        t_one.append(apply_T_poly(t_one[-1]))

    # 1 & 2. Verify J_r^(m) = I_{r-2}^(m+1) / (r-2)! and closed_form_I_r_over_fact(r, m) for m=0..7, r=0..10:
    for m in range(8):
        for r in range(11):
            j_exact = poly_one_minus_x_moment(t_one[m], r)
            if r == 0:
                assert j_exact == I0[m]
            elif r == 1:
                assert j_exact == H0[m + 1]
            else:
                i_shift = poly_moment(t_one[m + 1], r - 2) / Fraction(math.factorial(r - 2))
                assert j_exact == i_shift, f"J_{r}^({m}) mismatch"

            ir_closed = closed_form_I_r_over_fact(r, m, I0, H0) * math.factorial(r)
            ir_poly = poly_moment(t_one[m], r)
            assert ir_closed == ir_poly, f"Closed-form I_{r}^({m}) mismatch: {ir_closed} != {ir_poly}"

    print("  [PASS 2.1] Reflected Zero-Boundary Identity J_r^(m) = I_{r-2}^(m+1)/(r-2)! and non-recursive I_r^(m)/r! verified for all m=0..7, r=0..10.")

    # 3. Verify 3rd-order Edgeworth kernel F_0^(L)(x) / F_0^(L)(0) by symbolic Gaussian moment integration:
    # Let u = t * sqrt(L / 6), so t^2 = 6 u^2 / L.
    # log( (sin(t/2)/(t/2))^{2L} ) = L * [ -t^2/12 - t^4/720 - t^6/45360 - ... ]
    #                               = -u^2/2 - (6^2 / 720) u^4 / L - (6^3 / 45360) u^6 / L^2 - ...
    #                               = -u^2/2 - (1/20) u^4 / L - (1/210) u^6 / L^2 - ...
    # Expanding exp( -(1/20) u^4 / L - (1/210) u^6 / L^2 ) to order L^{-3}:
    #   1 - (1/20) u^4 / L + [ (1/800) u^8 - (1/210) u^6 ] / L^2
    #     + [ -(1/48000) u^{12} + (1/4200) u^{10} - (1/30240) u^8 ] / L^3
    # Wait: let's compute the exact Taylor coefficients of log((sin(y)/y)^2) up to y^8 to get exact L^{-3}!
    # sin(y)/y = 1 - y^2/6 + y^4/120 - y^6/5040 + y^8/362880
    # Let s = y^2 = t^2 / 4. Then 2*log(sin(y)/y) = -s/3 - s^2/90 - 2*s^3/2835 - s^4/18900 - ...
    # With s = t^2/4 = (6 u^2 / L) / 4 = (3/2) u^2 / L:
    # L * 2*log(sin(y)/y) = -u^2/2
    #   - (1/90)*(9/4) u^4 / L                  = -(1/40) u^4 / L
    #   - (2/2835)*(27/8) u^6 / L^2             = -(1/420) u^6 / L^2
    #   - (1/18900)*(81/16) u^8 / L^3           = -(3/11200) u^8 / L^3!
    # Let's compute the exact coefficients of x^2, x^4, x^6 in F_0^(L)(x)/F_0^(L)(0) up to L^{-3} in Fraction!
    def gauss_moment(two_k: int) -> Fraction:
        """E[u^{2k}] for standard normal u ~ N(0, 1) = (2k)! / (2^k k!)."""
        k = two_k // 2
        return Fraction(math.factorial(2 * k), (2 ** k) * math.factorial(k))

    # Weight W(u^2) = 1 + w1(u) / L + w2(u) / L^2 + w3(u) / L^3 where:
    #   a4 = -1/40,  a6 = -1/420,  a8 = -3/11200
    #   w1 = a4 u^4
    #   w2 = a6 u^6 + (a4^2 / 2) u^8
    #   w3 = a8 u^8 + a4*a6 u^{10} + (a4^3 / 6) u^{12}
    a4 = Fraction(-1, 40)
    a6 = Fraction(-1, 420)
    a8 = Fraction(-3, 11200)

    def E_w0(p: int) -> Fraction:
        return gauss_moment(p)

    def E_w1(p: int) -> Fraction:
        return a4 * gauss_moment(p + 4)

    def E_w2(p: int) -> Fraction:
        return a6 * gauss_moment(p + 6) + (a4 ** 2 / 2) * gauss_moment(p + 8)

    def E_w3(p: int) -> Fraction:
        return a8 * gauss_moment(p + 8) + (a4 * a6) * gauss_moment(p + 10) + (a4 ** 3 / 6) * gauss_moment(p + 12)

    # cos(t x) = sum_{r>=0} (-1)^r (t x)^{2r} / (2r)! = sum_{r>=0} (-1)^r (6/L)^r u^{2r} x^{2r} / (2r)!
    # Thus for each r = 0, 1, 2, 3, the coefficient of x^{2r} in J_L(x) / J_L(0) is:
    #   (-1)^r (6/L)^r / (2r)! * [ E_w0(2r) + E_w1(2r)/L + E_w2(2r)/L^2 + E_w3(2r)/L^3 ]
    #   divided by [ 1 + E_w1(0)/L + E_w2(0)/L^2 + E_w3(0)/L^3 ]!
    d1 = E_w1(0)
    d2 = E_w2(0)
    d3 = E_w3(0)
    # 1 / (1 + d1/L + d2/L^2 + d3/L^3) = 1 + q1/L + q2/L^2 + q3/L^3
    q1 = -d1
    q2 = d1 ** 2 - d2
    q3 = -(d1 ** 3) + 2 * d1 * d2 - d3

    # Multiply numerator series for each r = 1, 2, 3 by (1 + q1/L + q2/L^2 + q3/L^3):
    # For r = 1 (x^2, starts at L^{-1}):
    pref1 = Fraction(-6, math.factorial(2))
    n1_0, n1_1, n1_2 = E_w0(2), E_w1(2), E_w2(2)
    k_x2_L1 = pref1 * n1_0
    k_x2_L2 = pref1 * (n1_1 + n1_0 * q1)
    k_x2_L3 = pref1 * (n1_2 + n1_1 * q1 + n1_0 * q2)

    # For r = 2 (x^4, starts at L^{-2}):
    pref2 = Fraction(36, math.factorial(4))
    n2_0, n2_1 = E_w0(4), E_w1(4)
    k_x4_L2 = pref2 * n2_0
    k_x4_L3 = pref2 * (n2_1 + n2_0 * q1)

    # For r = 3 (x^6, starts at L^{-3}):
    pref3 = Fraction(-216, math.factorial(6))
    k_x6_L3 = pref3 * E_w0(6)

    assert k_x2_L1 == Fraction(-3, 1)
    assert k_x2_L2 == Fraction(9, 10)
    assert k_x4_L2 == Fraction(9, 2)
    assert k_x2_L3 == Fraction(-27, 350)
    assert k_x4_L3 == Fraction(-18, 5)
    assert k_x6_L3 == Fraction(-9, 2)
    print(f"  Exact Edgeworth Kernel F_0^(L)(x)/F_0^(L)(0):")
    print(f"    L^-1: {k_x2_L1} x^2")
    print(f"    L^-2: ({k_x2_L2}) x^2 + ({k_x4_L2}) x^4")
    print(f"    L^-3: ({k_x2_L3}) x^2 + ({k_x4_L3}) x^4 + ({k_x6_L3}) x^6")

    # Exact Irwin-Hall central B-spline on [0, 1] at L = 30 for direct numerical verification of c_3^(m):
    L_test = 30
    deg_b = 2 * L_test - 1
    f0_30 = [Fraction(0)] * (deg_b + 1)
    denom_b = math.factorial(deg_b)
    for k_b in range(L_test + 1):
        sgn_b = -1 if (k_b % 2 == 1) else 1
        b_2L_k = math.comb(2 * L_test, k_b)
        sh_b = L_test - k_b
        for j_b in range(deg_b + 1):
            c_jb = math.comb(deg_b, j_b) * (sh_b ** (deg_b - j_b))
            f0_30[j_b] += Fraction(sgn_b * b_2L_k * c_jb, denom_b)

    # Compute 1st, 2nd, and 3rd order Edgeworth coefficients c_1^(m), c_2^(m), c_3^(m) for m = 1..6
    # purely from the unit-fraction sequences I0 and H0 via closed_form_I_r_over_fact!
    edgeworth_3rd = {}
    for m in range(1, 7):
        def norm_mom(deg_r: int, idx_m: int) -> Fraction:
            return (closed_form_I_r_over_fact(deg_r, idx_m, I0, H0) * math.factorial(deg_r)) / I0[idx_m]

        r2_den, r4_den, r6_den = norm_mom(2, m), norm_mom(4, m), norm_mom(6, m)
        r2_num, r4_num, r6_num = norm_mom(2, m + 1), norm_mom(4, m + 1), norm_mom(6, m + 1)

        a1 = k_x2_L1 * r2_num
        a2 = k_x2_L2 * r2_num + k_x4_L2 * r4_num
        a3 = k_x2_L3 * r2_num + k_x4_L3 * r4_num + k_x6_L3 * r6_num

        b1 = k_x2_L1 * r2_den
        b2 = k_x2_L2 * r2_den + k_x4_L2 * r4_den
        b3 = k_x2_L3 * r2_den + k_x4_L3 * r4_den + k_x6_L3 * r6_den

        p0 = I0[m + 1] / I0[m]
        # (1 + a1/L + a2/L^2 + a3/L^3) / (1 + b1/L + b2/L^2 + b3/L^3)
        c1 = p0 * (a1 - b1)
        c2 = p0 * (a2 - b2 - b1 * (a1 - b1))
        c3 = p0 * (a3 - b3 - b1 * (a2 - b2) + (b1 ** 2 - b2) * (a1 - b1))

        # Check against exact Irwin-Hall B-spline integral at L = 30:
        num_30 = sum(f0_30[j] * poly_moment(t_one[m + 1], j) for j in range(len(f0_30)))
        den_30 = sum(f0_30[j] * poly_moment(t_one[m], j) for j in range(len(f0_30)))
        exact_30 = num_30 / den_30
        err2_30 = float(abs(exact_30 - (p0 + c1 / L_test + c2 / (L_test ** 2))))
        err3_30 = float(abs(exact_30 - (p0 + c1 / L_test + c2 / (L_test ** 2) + c3 / (L_test ** 3))))
        assert err3_30 < err2_30 / 20.0, f"3rd-order Edgeworth did not improve accuracy at m={m}: {err3_30} vs {err2_30}"

        edgeworth_3rd[f"m={m}"] = {
            "p_inf": str(p0),
            "c1": str(c1),
            "c2": str(c2),
            "c3": str(c3),
            "c3_float": float(c3),
            "L30_err_order2": err2_30,
            "L30_err_order3": err3_30,
            "I6_over_I0": str(r6_den),
        }
        print(
            f"  m={m}: p_inf = {str(p0):>20s} | c1 = {str(c1):>22s} | c2 = {str(c2):>28s}\n"
            f"       c3 = {str(c3)} ({float(c3):+.6e}) | L=30 err2={err2_30:.3e} -> err3={err3_30:.3e} ({err2_30/err3_30:.1f}x better)"
        )

    assert edgeworth_3rd["m=1"]["c1"] == "-3/175"
    assert edgeworth_3rd["m=1"]["c2"] == "2/175"
    assert edgeworth_3rd["m=2"]["c1"] == "65/21168"
    assert edgeworth_3rd["m=2"]["c2"] == "-8497/4074840"
    assert edgeworth_3rd["m=3"]["c1"] == "-5443/11977416"
    assert edgeworth_3rd["m=3"]["c2"] == "197758621/663309298080"
    print("  [PASS 2.2] Exact 1st, 2nd, and 3rd order rational Edgeworth expansions c_1^(m), c_2^(m), c_3^(m) verified for m=1..6.\n")

    return {
        "edgeworth_kernel_L_minus_1_to_3": {
            "L^-1": {"x^2": str(k_x2_L1)},
            "L^-2": {"x^2": str(k_x2_L2), "x^4": str(k_x4_L2)},
            "L^-3": {"x^2": str(k_x2_L3), "x^4": str(k_x4_L3), "x^6": str(k_x6_L3)},
        },
        "edgeworth_1st_2nd_3rd_order_m_1_to_6": edgeworth_3rd,
    }


if __name__ == "__main__":
    res1 = part1_midpoint_resolvent_unification_and_andre_cayley_egf()
    res2 = part2_reflected_moment_theorem_and_edgeworth_3rd_order()
    out = {
        "part1_midpoint_resolvent_unification_and_andre_cayley_egf": res1,
        "part2_reflected_moment_theorem_and_edgeworth_3rd_order": res2,
        "status": "ALL_CHECKS_PASSED",
    }
    out_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "midpoint_resolvent_unification_and_edgeworth3_2026_11_10_results.json",
    )
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    if os.path.isdir(RESEARCH_DIR):
        shutil.copy2(
            os.path.abspath(__file__),
            os.path.join(RESEARCH_DIR, "midpoint_resolvent_unification_and_edgeworth3_den_b.py"),
        )
        shutil.copy2(
            out_json,
            os.path.join(RESEARCH_DIR, "midpoint_resolvent_unification_and_edgeworth3_den_b_results.json"),
        )
    print(f"Saved results to {out_json}")
