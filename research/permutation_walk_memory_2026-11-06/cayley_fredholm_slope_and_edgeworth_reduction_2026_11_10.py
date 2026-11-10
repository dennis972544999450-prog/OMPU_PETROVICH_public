#!/usr/bin/env python3
"""
Cayley-Fredholm Free-End Slope Theorem, Unit-Fraction Integral Generating Function
for Bayesian Cell Masses I_0^(m), and Mod-4 Moment Reduction for Edgeworth Asymptotics.

Author: Jee A (Lane A, OMPU Stereo Pair, ompu-d6a8af238c)
Date: 2026-11-10 20:30 CET (Tuesday Evening Tick, rev 97)

Main Results Verified in Exact Rational (Fraction) Arithmetic:
1. Cayley-Fredholm Free-End Slope Identity:
   Let H_0^(m) := (T^m 1)(0) = -(T^m f_1)'(0) = <1, T^{m-1} f_1>_{L^2(0,1)} (with H_0^(0) = 1).
   Then the generating function H_z(0) = ((I - z T)^{-1} 1)(0) is the ratio of the two
   even/odd Fredholm determinants det(I + z T) / det(I - z T):
       H_z(0) = sum_{m=0}^inf H_0^(m) z^m = Delta(-z) / Delta(z)
              = exp( 2 * sum_{k=0}^inf Tr(T^{2k+1}) / (2k+1) * z^{2k+1} ),
   where Delta(z) = det(I - z T) = sum_{m=0}^inf (-1)^{floor((m+1)/2)} / (2^m (2m)!) z^m.
   Consequently, H_0^(m) satisfies the pure unit-fraction recurrence:
       sum_{j=0}^m [ (-1)^{floor((j+1)/2)} / (2^j (2j)!) ] * H_0^(m-j) = (-1)^{floor(m/2)} / (2^m (2m)!).

2. Unit-Fraction Integral Generating Function for Bayesian Cell Masses I_0^(m):
   Let I_0^(m) := int_0^1 (T^m 1)(x) dx = <1, T^m 1>_{L^2(0,1)} = -(T^{m+1} 1)'(0).
   Then:
       sum_{m=0}^inf I_0^(m) z^m = <1, (I - z T)^{-1} 1> = ( int_0^1 Delta(z u^2) du ) / Delta(z)
                                 = [ sum_{m=0}^inf (-1)^{floor((m+1)/2)} / (2^m (2m+1)!) z^m ] / Delta(z),
   giving the pure unit-fraction recurrence for I_0^(m) and the m-turn Bayesian cell limits
   p_hat_inf(-, 1^m) = I_0^(m+1) / I_0^(m) without constructing the polynomials T^m 1:
       sum_{j=0}^m [ (-1)^{floor((j+1)/2)} / (2^j (2j)!) ] * I_0^(m-j) = (-1)^{floor((m+1)/2)} / (2^m (2m+1)!).

3. Mod-4 Moment Step Identity & Closed-Form Edgeworth Reduction:
   For I_r^(m) := int_0^1 x^r (T^m 1)(x) dx, two-step and four-step integration by parts using
   (T^m 1)(x) = (T^{m+1} 1)''(1-x) and (T^k 1)(1) = (T^k 1)'(1) = 0 yields for all m >= 0:
       I_1^(m) = I_0^(m) - H_0^(m+1),
       I_2^(m) = I_0^(m) - 2 H_0^(m+1) + 2 I_0^(m+1),
       I_3^(m) = I_0^(m) - 3 H_0^(m+1) + 6 H_0^(m+2),
       I_r^(m) = I_0^(m) - r H_0^(m+1) + r(r-1)(r-2)(r-3) I_{r-4}^(m+2)   (for all r >= 4).
   In particular, the normalized 2nd and 4th moments in the Edgeworth expansion of Theorem 5 (§6.2) are:
       I_2^(m) / I_0^(m) = 1 - 2 H_0^(m+1)/I_0^(m) + 2 p_hat_inf(-, 1^m),
       I_4^(m) / I_0^(m) = 1 - 4 H_0^(m+1)/I_0^(m) + 24 p_hat_inf(-, 1^m) p_hat_inf(-, 1^{m+1}).
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


def delta_coeff(m: int) -> Fraction:
    """Coefficient of z^m in Delta(z) = det(I - z T) = sum_{m>=0} (-1)^{floor((m+1)/2)} / (2^m (2m)!) z^m."""
    return Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m))


def delta_int_coeff(m: int) -> Fraction:
    """Coefficient of z^m in int_0^1 Delta(z u^2) du = sum_{m>=0} (-1)^{floor((m+1)/2)} / (2^m (2m+1)!) z^m."""
    return Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m + 1))


def verify_all() -> dict:
    M_max = 10
    t_one = [[Fraction(1)]]
    t_f1 = [[Fraction(1), Fraction(-1)]]
    for _ in range(M_max + 3):
        t_one.append(apply_T_poly(t_one[-1]))
        t_f1.append(apply_T_poly(t_f1[-1]))

    # 1. Verify Cayley-Fredholm Free-End Slope Theorem:
    # H_0^(m) = (T^m 1)(0) = -(T^m f_1)'(0) = <1, T^{m-1} f_1> via unit-fraction recurrence from Delta(-z)/Delta(z)
    d_coeffs = [delta_coeff(m) for m in range(M_max + 3)]
    H0_rec = [Fraction(0)] * (M_max + 3)
    for m in range(M_max + 3):
        rhs = Fraction((-1) ** (m // 2), (2 ** m) * math.factorial(2 * m))
        H0_rec[m] = rhs - sum(d_coeffs[j] * H0_rec[m - j] for j in range(1, m + 1))
        assert H0_rec[m] == t_one[m][0], f"H0 mismatch at m={m}: {H0_rec[m]} != {t_one[m][0]}"
        if m >= 1:
            slope_f1 = -t_f1[m][1]
            mass_prev_f1 = poly_moment(t_f1[m - 1], 0)
            assert H0_rec[m] == slope_f1 == mass_prev_f1

    # Also verify exponential Cayley relation: H_z(0) = exp(2 * sum_{k>=0} Tr(T^{2k+1})/(2k+1) * z^{2k+1})
    # Using d/dz H_z(0) = H_z(0) * (2 * sum_{k>=0} Tr(T^{2k+1}) z^{2k}):
    traces = [Fraction(1, 4) * t_f1[m - 1][0] for m in range(1, M_max + 3)]  # Tr(T^m) for m=1..M_max+2
    for m in range(1, M_max + 1):
        # m * H0[m] == 2 * sum_{k>=0, 2k+1 <= m} Tr(T^{2k+1}) * H0[m - (2k+1)]
        cayley_rhs = 2 * sum(
            traces[2 * k] * H0_rec[m - (2 * k + 1)]
            for k in range((m + 1) // 2)
        )
        assert m * H0_rec[m] == cayley_rhs, f"Cayley exp mismatch at m={m}"

    # 2. Verify Unit-Fraction Integral Generating Function for I_0^(m) = int_0^1 (T^m 1)(x) dx:
    n_coeffs = [delta_int_coeff(m) for m in range(M_max + 3)]
    I0_rec = [Fraction(0)] * (M_max + 3)
    for m in range(M_max + 3):
        I0_rec[m] = n_coeffs[m] - sum(d_coeffs[j] * I0_rec[m - j] for j in range(1, m + 1))
        exact_i0 = poly_moment(t_one[m], 0)
        slope_one_next = -t_one[m + 1][1]
        assert I0_rec[m] == exact_i0 == slope_one_next, f"I0 mismatch at m={m}: {I0_rec[m]} != {exact_i0}"

    # Verify Bayesian cell limits p_hat_inf(-, 1^m) = I_0^(m+1) / I_0^(m) for m=1..8 from recurrence alone:
    p_inf = {m: I0_rec[m + 1] / I0_rec[m] for m in range(1, 9)}
    assert str(p_inf[1]) == "3/10"
    assert str(p_inf[2]) == "71/252"
    assert str(p_inf[3]) == "182/639"
    assert str(p_inf[4]) == "45541/160160"
    assert str(p_inf[5]) == "168388/592033"
    assert str(p_inf[6]) == "120686411/424337760"

    # 3. Verify Mod-4 Moment Step Identity & Closed-Form Edgeworth Reduction for m=1..6 and r=1..8:
    edgeworth_summary = {}
    for m in range(1, 7):
        i0 = I0_rec[m]
        i1 = i0 - H0_rec[m + 1]
        i2 = i0 - 2 * H0_rec[m + 1] + 2 * I0_rec[m + 1]
        i3 = i0 - 3 * H0_rec[m + 1] + 6 * H0_rec[m + 2]
        i4 = i0 - 4 * H0_rec[m + 1] + 24 * I0_rec[m + 2]
        i5 = i0 - 5 * H0_rec[m + 1] + 120 * (I0_rec[m + 2] - H0_rec[m + 3])
        i6 = i0 - 6 * H0_rec[m + 1] + 360 * (I0_rec[m + 2] - 2 * H0_rec[m + 3] + 2 * I0_rec[m + 3])

        assert i1 == poly_moment(t_one[m], 1)
        assert i2 == poly_moment(t_one[m], 2)
        assert i3 == poly_moment(t_one[m], 3)
        assert i4 == poly_moment(t_one[m], 4)
        assert i5 == poly_moment(t_one[m], 5)
        assert i6 == poly_moment(t_one[m], 6)

        # Compute 1st and 2nd order Edgeworth coefficients c1, c2 purely from I0_rec and H0_rec:
        r2_den = i2 / i0
        r4_den = i4 / i0
        i2_next = I0_rec[m + 1] - 2 * H0_rec[m + 2] + 2 * I0_rec[m + 2]
        i4_next = I0_rec[m + 1] - 4 * H0_rec[m + 2] + 24 * I0_rec[m + 3]
        r2_num = i2_next / I0_rec[m + 1]
        r4_num = i4_next / I0_rec[m + 1]

        p0 = p_inf[m]
        a1 = -3 * r2_num
        a2 = Fraction(9, 10) * r2_num + Fraction(9, 2) * r4_num
        b1 = -3 * r2_den
        b2 = Fraction(9, 10) * r2_den + Fraction(9, 2) * r4_den
        c1 = p0 * (a1 - b1)
        c2 = p0 * (a2 - b2 - b1 * (a1 - b1))

        edgeworth_summary[f"m={m}"] = {
            "p_inf": str(p0),
            "c1": str(c1),
            "c2": str(c2),
            "I2_over_I0": str(r2_den),
            "I4_over_I0": str(r4_den),
        }

    assert edgeworth_summary["m=1"]["c1"] == "-3/175"
    assert edgeworth_summary["m=1"]["c2"] == "2/175"
    assert edgeworth_summary["m=2"]["c1"] == "65/21168"
    assert edgeworth_summary["m=2"]["c2"] == "-8497/4074840"
    assert edgeworth_summary["m=3"]["c1"] == "-5443/11977416"
    assert edgeworth_summary["m=3"]["c2"] == "197758621/663309298080"

    print("=== CAYLEY-FREDHOLM FREE-END SLOPE & EDGEWORTH MOMENT REDUCTION ===")
    for m in range(1, 9):
        print(f"  m={m}: H_0^({m}) = (T^{m} 1)(0) = -(T^{m} f_1)'(0) = {str(H0_rec[m]):>24s} | I_0^({m}) = {str(I0_rec[m]):>26s} | p_inf(-,1^{m}) = {str(p_inf[m])}")
    print("ALL_CHECKS_PASSED")

    return {
        "H0_free_end_slopes_m_0_to_8": {f"m={m}": str(H0_rec[m]) for m in range(9)},
        "I0_bayesian_masses_m_0_to_8": {f"m={m}": str(I0_rec[m]) for m in range(9)},
        "p_hat_inf_m_1_to_8": {f"m={m}": str(p_inf[m]) for m in range(1, 9)},
        "edgeworth_reduced_m_1_to_6": edgeworth_summary,
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "cayley_fredholm_slope_and_edgeworth_reduction_2026_11_10_results.json",
    )
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    if os.path.isdir(RESEARCH_DIR):
        shutil.copy2(
            os.path.abspath(__file__),
            os.path.join(RESEARCH_DIR, "cayley_fredholm_slope_and_edgeworth_reduction_2026_11_10.py"),
        )
        shutil.copy2(
            out_json,
            os.path.join(RESEARCH_DIR, "cayley_fredholm_slope_and_edgeworth_reduction_2026_11_10_results.json"),
        )
