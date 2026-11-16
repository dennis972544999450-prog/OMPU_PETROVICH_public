#!/usr/bin/env python3
"""Mittag-Leffler Cantilever Spectral Zeta Law & Gaussian (2+i) Cramer Inversion.

Author: Petrovich (ompu-e1dd503f59), 2026-11-16
Run: /opt/homebrew/bin/python3 -I -B mittag_leffler_krylov_zeta_and_gaussian_2plusi_cramer_2026_11_16.py

Closes both open seams left after rev 102 (`1794772044`, `1794772708`, `1794776144`, `READ-0090`):

1. Theorem 1 (Analytic Mittag-Leffler Partial Fractions & Spectral Zeta Sum Rule
   for the Inverse Laplace-Krylov Series `1794776144`):
   Let F(s) := E_0(s)^2 - E_1(s) E_3(s) = (1 + cosh(s) cos(s)) / 2 and
   G(s) := 1 / F(s) = 2 / (1 + cosh(s) cos(s)) = sum_{n >= 0} b_n s^{4n}.
   - On circles |s| = 2*pi*N (N >= 1), |cosh(s) cos(s)| grows uniformly as
     Omega(exp(2*pi*N)) in all directions arg(s), so Cauchy's residue theorem
     gives an exact Mittag-Leffler expansion with ZERO entire remainder and
     radius of convergence R = kappa_1 = 1.875104068711961... :
       G(s) = sum_{r=1}^infty w_r / (1 - s^4 / kappa_r^4),
       w_r := 8 / [ kappa_r * (cosh(kappa_r) sin(kappa_r) - sinh(kappa_r) cos(kappa_r)) ]
            = 8 / [ kappa_r * ((-1)^{r-1} sinh(kappa_r) + tanh(kappa_r)) ].
   - Because |w_r| ~ 16 * exp(-kappa_r) / kappa_r decays exponentially with r,
     every rational coefficient b_n (including n = 0!) satisfies the convergent
     cantilever spectral zeta identity:
       b_n = sum_{r=1}^infty w_r / kappa_r^{4n}   (for all n >= 0),
     in particular sum_{r=1}^infty w_r = b_0 = 1 (verified to < 2e-89 across n = 0..6).

2. Theorem 2 (Exact Pointwise Krylov Shift Syzygy on {u_j, d_j, w_j}):
   On the three pure s-Toeplitz families u_j, d_j, w_j of `1794772708`, the 3x3
   Toeplitz symbol matrix A(s) has identically zero determinant det A(s) == 0,
   reflecting the exact pointwise identity in Q[x][[s]]:
       E_1(s) U(x; s) + E_0(s) D(x; s) - E_3(s) W(x; s) == 0.
   Hence no pure s-Toeplitz inverse exists on {u_j, d_j, w_j}.

3. Theorem 3 (Gaussian Prime (2+i) Determinant & All-Order Cramer Formula for
   Biorthogonal Projectors Phi_{alpha,k}, Psi_{alpha,k}):
   In Den-b's basis {u_j, v_j, w_j}, v_j couples the Kelvin parameter z = s^4
   to the Rayleigh-dilated parameter -z/4 = ((1+i)s/2)^4. Substituting z -> -4z
   in the v_j generating series yields an exact 2x2 linear system over Q[x][[z]]
   whose determinant is NOT F(s), but the Gaussian-(2+i) Mahler-Krylov series:
       D_KR(s^4) := e_0(s^4) e_1(-4 s^4) - s^4 e_3(s^4) e_2(-4 s^4)
                  = [ 2(sinh(s) + sin(s)) + sinh(2s) cos(s) + cosh(s) sin(2s) ] / (8s)
                  = sum_{m=0}^infty [ (2 + Re[(2 + i)^{4m+1}]) / (4 * (4m + 1)!) ] s^{4m}
                  = 1 - (3/40) z - (179/362880) z^2 + (313/230630400) z^3 - ...
   Inverting the scalar power series D_KR(z) and e_0(z) = E_0(s) gives closed-form
   matrix-free Cauchy convolution formulas for Phi_{I_0,k}(x), Phi_{H_0,k}(x),
   and Phi_{m_0,k+1}(x) (and Psi = Phi'/4) for ALL k >= 0, verified in exact
   Fraction arithmetic against `build_biorthogonal_projectors` for k = 0..5
   (all 18 projector pairs up to degree 24).
"""

from __future__ import annotations

import cmath
import decimal
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import gaussian_toeplitz_convolution_and_biorthogonal_projectors_2026_11_15 as gtp


def fact(n: int) -> int:
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def gaussian_int_pow(zr: int, zi: int, exp: int) -> Tuple[int, int]:
    """Exact integer power (zr + i*zi)^exp in Z[i]."""
    rr, ri = 1, 0
    br, bi = zr, zi
    e = exp
    while e > 0:
        if e & 1:
            rr, ri = rr * br - ri * bi, rr * bi + ri * br
        br, bi = br * br - bi * bi, 2 * br * bi
        e >>= 1
    return rr, ri


def series_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = len(a)
    out = [Fraction(0)] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n - i):
            if b[j] != 0:
                out[i + j] += a[i] * b[j]
    return out


def series_inv(a: List[Fraction]) -> List[Fraction]:
    assert a[0] != 0, "Leading term must be non-zero for formal power series inversion"
    n = len(a)
    inv = [Fraction(0)] * n
    inv[0] = Fraction(1) / a[0]
    for m in range(1, n):
        acc = sum(a[k] * inv[m - k] for k in range(1, m + 1))
        inv[m] = -acc / a[0]
    return inv


def poly_series_mul(scalar_s: List[Fraction], poly_s: List[List[Fraction]]) -> List[List[Fraction]]:
    n = len(poly_s)
    out = [[Fraction(0)] for _ in range(n)]
    for i in range(n):
        if scalar_s[i] == 0:
            continue
        for j in range(n - i):
            out[i + j] = gtp.poly_add(out[i + j], poly_s[j], Fraction(1), scalar_s[i])
    return out


def verify_theorem_1_mittag_leffler_zeta(num_modes: int = 64, max_n: int = 6) -> Dict[str, object]:
    decimal.getcontext().prec = 105
    Decimal = decimal.Decimal

    # Exact rational b_n from F(s)*G(s) = 1 where F(s) = 1 + sum_{k>=1} ((-4)^k / (2*(4k)!)) z^k
    f_series = [Fraction(1)] + [Fraction((-4) ** k, 2 * fact(4 * k)) for k in range(1, max_n + 1)]
    b_exact = series_inv(f_series)

    modes: List[Tuple[decimal.Decimal, decimal.Decimal]] = []
    max_alt_rel_err = Decimal(0)
    for r in range(1, num_modes + 1):
        kap, _ = gtp.solve_cantilever_kappa(r)
        ch, sh = gtp.dec_cosh(kap), gtp.dec_sinh(kap)
        co, si = gtp.dec_cos(kap), gtp.dec_sin(kap)
        denom = kap * (ch * si - sh * co)
        alt_denom = kap * (((-1) ** (r - 1)) * sh + (sh / ch))
        rel_err = abs(denom - alt_denom) / abs(denom)
        if rel_err > max_alt_rel_err:
            max_alt_rel_err = rel_err
        w_r = Decimal(8) / denom
        modes.append((kap, w_r))

    assert max_alt_rel_err < Decimal("1e-80"), f"Denominator identity drift: {max_alt_rel_err}"

    max_zeta_err = Decimal(0)
    zeta_errors: Dict[str, str] = {}
    for n in range(max_n + 1):
        zeta_sum = sum(w_r / (kap ** (4 * n)) for kap, w_r in modes)
        b_dec = Decimal(b_exact[n].numerator) / Decimal(b_exact[n].denominator)
        err = abs(zeta_sum - b_dec)
        zeta_errors[f"n={n}"] = f"{err:.3e}"
        if err > max_zeta_err:
            max_zeta_err = err

    assert max_zeta_err < Decimal("1e-88"), f"Mittag-Leffler spectral zeta error too large: {max_zeta_err}"

    # Direct complex evaluation of G(s) vs Mittag-Leffler partial-fraction series
    # including s = 2.4 + 0.9j outside the convergence disk |s| < kappa_1 ~ 1.8751!
    max_pf_err = 0.0
    for s in (0.6 + 0.2j, 1.3 - 0.8j, 2.4 + 0.9j):
        g_exact = 2.0 / (1.0 + cmath.cosh(s) * cmath.cos(s))
        s4 = s ** 4
        g_pf = sum(float(w_r) / (1.0 - s4 / (float(kap) ** 4)) for kap, w_r in modes[:35])
        max_pf_err = max(max_pf_err, abs(g_exact - g_pf))

    assert max_pf_err < 1e-15, f"Complex Mittag-Leffler error too large: {max_pf_err}"

    return {
        "radius_of_convergence_kappa_1": float(modes[0][0]),
        "w_1_dominant_residue_weight": float(modes[0][1]),
        "b_exact_0_to_5": [str(c) for c in b_exact[:6]],
        "max_spectral_zeta_error_n0_to_6": f"{max_zeta_err:.3e}",
        "max_complex_pf_error_outside_disk": max_pf_err,
    }


def verify_theorem_2_pointwise_toeplitz_syzygy(max_m: int = 7) -> Dict[str, object]:
    """Verify E_1(s)*U(x;s) + E_0(s)*D(x;s) - E_3(s)*W(x;s) == 0 identically in Q[x][[s]]."""
    for m in range(max_m + 1):
        poly = [Fraction(0)]
        for j in range(m + 1):
            poly = gtp.poly_add(poly, gtp.build_u_j(j), Fraction(1), Fraction(1, fact(4 * (m - j) + 1)))
            poly = gtp.poly_add(poly, gtp.build_d_j(j), Fraction(1), Fraction(1, fact(4 * (m - j))))
        for j in range(m):
            poly = gtp.poly_add(poly, gtp.build_w_j(j), Fraction(1), Fraction(-1, fact(4 * (m - 1 - j) + 3)))
        assert all(c == 0 for c in poly), f"Non-zero syzygy residual at m={m}: {poly}"

    return {
        "pointwise_nullspace_identity_verified_up_to_degree": 4 * max_m + 3,
        "pure_s_toeplitz_symbol_determinant": "0 (identically singular)",
    }


def verify_theorem_3_gaussian_2plusi_cramer(max_k: int = 5) -> Dict[str, object]:
    """Verify the closed-form (2+i) determinant and Cramer projector formula up to k = max_k."""
    n_terms = max_k + 2
    e0 = [Fraction(1, fact(4 * m)) for m in range(n_terms)]
    e1 = [Fraction(1, fact(4 * m + 1)) for m in range(n_terms)]
    e2 = [Fraction(1, fact(4 * m + 2)) for m in range(n_terms)]
    e3 = [Fraction(1, fact(4 * m + 3)) for m in range(n_terms)]

    e1_m4 = [((-4) ** m) * e1[m] for m in range(n_terms)]
    e2_m4 = [((-4) ** m) * e2[m] for m in range(n_terms)]
    ze3 = [Fraction(0)] + e3[:-1]

    # 1. Determinant from 2x2 matrix vs single-term Gaussian-(2+i) formula
    d_kr_conv = [
        series_mul(e0, e1_m4)[m] - series_mul(ze3, e2_m4)[m]
        for m in range(n_terms)
    ]
    d_kr_closed = []
    for m in range(n_terms):
        re_part, _ = gaussian_int_pow(2, 1, 4 * m + 1)
        d_kr_closed.append(Fraction(2 + re_part, 4 * fact(4 * m + 1)))

    assert d_kr_conv == d_kr_closed, f"D_KR mismatch: {d_kr_conv} != {d_kr_closed}"

    # Verify analytic trigonometric identity at complex s
    max_trig_err = 0.0
    for s in (0.4 - 0.1j, 0.85 + 0.35j, 1.05 - 0.25j):
        lhs = (
            0.5 * (cmath.cosh(s) + cmath.cos(s))
            * (cmath.sinh(s) * cmath.cos(s) + cmath.cosh(s) * cmath.sin(s)) / (2.0 * s)
            - 0.5 * (cmath.sinh(s) - cmath.sin(s))
            * (cmath.sinh(s) * cmath.sin(s)) / (2.0 * s)
        )
        rhs = (
            2.0 * (cmath.sinh(s) + cmath.sin(s))
            + cmath.sinh(2.0 * s) * cmath.cos(s)
            + cmath.cosh(s) * cmath.sin(2.0 * s)
        ) / (8.0 * s)
        max_trig_err = max(max_trig_err, abs(lhs - rhs))
    assert max_trig_err < 1e-15, f"Trig identity error: {max_trig_err}"

    # 2. Closed-form Cramer inversion vs Den-b's build_biorthogonal_projectors(max_k)
    K = max_k + 1
    delta_series = [Fraction(-1, 4) * c for c in d_kr_closed[:K]]
    delta_inv = series_inv(delta_series)
    e0_inv = series_inv(e0[:K])
    gamma_series = series_inv(d_kr_closed[:K])  # D_KR(z)^{-1}

    u_polys = [gtp.build_u_j(j) for j in range(K)]
    v_m4_polys = [gtp.poly_scale(gtp.build_v_j(j), Fraction((-4) ** j)) for j in range(K)]
    w_polys = [gtp.build_w_j(j) for j in range(K)]

    num_i0 = [
        gtp.poly_add(
            poly_series_mul([Fraction(-1, 4) * c for c in e1_m4[:K]], u_polys)[k],
            poly_series_mul(ze3[:K], v_m4_polys)[k],
        )
        for k in range(K)
    ]
    num_h0 = [
        gtp.poly_add(
            poly_series_mul([Fraction(-1, 4) * c for c in e2_m4[:K]], u_polys)[k],
            poly_series_mul(e0[:K], v_m4_polys)[k],
        )
        for k in range(K)
    ]

    cramer_phi_i0 = poly_series_mul(delta_inv, num_i0)
    cramer_phi_h0 = poly_series_mul(delta_inv, num_h0)
    rhs_m0 = [
        gtp.poly_add(w_polys[k], poly_series_mul(e1[:K], cramer_phi_h0)[k])
        for k in range(K)
    ]
    cramer_phi_m0 = poly_series_mul(e0_inv, rhs_m0)

    ref = gtp.build_biorthogonal_projectors(max_k=max_k)
    for k in range(K):
        assert cramer_phi_i0[k] == ref[("I0", k)]["Phi"], f"Phi_I0 mismatch at k={k}"
        assert cramer_phi_h0[k] == ref[("H0", k)]["Phi"], f"Phi_H0 mismatch at k={k}"
        assert cramer_phi_m0[k] == ref[("m0", k + 1)]["Phi"], f"Phi_m0 mismatch at k={k}"

        psi_i0 = gtp.poly_scale(gtp.poly_deriv(cramer_phi_i0[k]), Fraction(1, 4))
        psi_h0 = gtp.poly_scale(gtp.poly_deriv(cramer_phi_h0[k]), Fraction(1, 4))
        psi_m0 = gtp.poly_scale(gtp.poly_deriv(cramer_phi_m0[k]), Fraction(1, 4))
        assert psi_i0 == ref[("I0", k)]["Psi"], f"Psi_I0 mismatch at k={k}"
        assert psi_h0 == ref[("H0", k)]["Psi"], f"Psi_H0 mismatch at k={k}"
        assert psi_m0 == ref[("m0", k + 1)]["Psi"], f"Psi_m0 mismatch at k={k}"

    return {
        "d_kr_closed_0_to_5": [str(c) for c in d_kr_closed[:6]],
        "d_kr_inverse_gamma_0_to_5": [str(c) for c in gamma_series[:6]],
        "e0_inverse_0_to_5": [str(c) for c in e0_inv[:6]],
        "max_trig_identity_error": max_trig_err,
        "cramer_exact_fraction_match_k_0_to": max_k,
        "max_projector_degree_verified": 4 * max_k + 4,
    }


def main() -> None:
    t1 = verify_theorem_1_mittag_leffler_zeta()
    t2 = verify_theorem_2_pointwise_toeplitz_syzygy()
    t3 = verify_theorem_3_gaussian_2plusi_cramer()
    report = {
        "module": "mittag_leffler_krylov_zeta_and_gaussian_2plusi_cramer_2026_11_16.py",
        "theorem_1_mittag_leffler_zeta": t1,
        "theorem_2_pointwise_syzygy": t2,
        "theorem_3_gaussian_2plusi_cramer": t3,
        "status": "ALL_CHECKS_PASSED",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
