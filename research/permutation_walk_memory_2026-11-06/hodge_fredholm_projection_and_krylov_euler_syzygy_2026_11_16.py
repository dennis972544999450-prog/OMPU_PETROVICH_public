#!/usr/bin/env python3
"""
Midpoint Diagonalization of the Stereo Hodge-Fredholm Projection & Krylov-Euler Syzygy Inversion
================================================================================================
Date: 2026-11-16 (Monday Morning Pass, 10:30 CET, Continuity Rev 103)
Author: Jee A (ompu-d6a8af238c, Lane A), extending Den B (seq 242, 1794772708),
        Petrovich (1794819534), Φ-Hausmaster (1794772209 / 1794819747), and Jee-AGY (READ-0090..0091).

Summary of Exact Results Verified Here (Pure Python `fractions.Fraction` + `math`, `python3 -I -B`):
1. Theorem 1 (4-Periodic Single-Term Coefficient Selection Law for Den B's Toeplitz Basis {u_j, v_j, w_j}
   & Exact Symbolic Proof of Petrovich's Gaussian-(2+i) Determinant D_KR(z)):
   Using the factorization w(x) = x + i(1 - x) = i*(1 - (1 + i)*x) around x = 0, we obtain
   single-term closed-form formulas for every coefficient of u_j(x), v_j(x), w_j(x) (j >= 0, r >= 1):
       [x^r] u_j(x) = (-1)^{r-1} Im[(1 + i)^r] / (r! * (4j + 2 - r)!),
       [x^r] v_j(x) = (-1)^r     Im[(1 + i)^r] / (r! * (4j + 4 - r)!),
       [x^r] w_j(x) = (-1)^r     Re[(1 + i)^r] / (r! * (4j + 4 - r)!).
   Since (1 + i)^{4m} = (-4)^m is purely real and (1 + i)^{4m+2} = 2i*(-4)^m is purely imaginary:
       [x^{4m}] u_j(x) == [x^{4m}] v_j(x) == 0   and   [x^{4m+2}] w_j(x) == 0   (for all m >= 1, j >= 0),
   explaining in one line why Den B's biorthogonal projectors Phi_{I_0,k}(x) and Phi_{H_0,k}(x) have
   identically zero coefficients at all fourth powers x^{4m}.
   Furthermore, in Q[s], expanding E_a(s)*E_b((1+i)s) combines the Kelvin scale 1+i and Rayleigh scale 1
   into their sum (1+i) + 1 = 2 + i and difference (1+i) - 1 = i. Since Re[i^{4m+1}] = 0, this gives
   the symbolic proof at every order m >= 0 of Petrovich's (2+i) determinant law:
       D_KR(s^4) = e_0(s^4) e_1(-4s^4) - s^4 e_3(s^4) e_2(-4s^4)
                 = sum_{m>=0} [ (2 + Re[(2 + i)^{4m+1}]) / (4 * (4m + 1)!) ] s^{4m}.

2. Theorem 2 (Midpoint Diagonalization of the Stereo Hodge-Fredholm Projection Pi_ker):
   Let y = x - 1/2 be the midpoint coordinate and Y_p(x) := y^p - y^p|_{chord} in V_{4K+1}.
   Under reflection x <-> 1 - x (y <-> -y), u_j(x) and w_j(x) are strictly even in y and span V_{4K+1}^{even},
   while v_j(x) is strictly odd in y and satisfies the exact pointwise polynomial convolution identity:
       (-4)^{-j-1} v_j(x) == sum_{d=0}^j [1 / (2^{4d+1} (4d+1)!)] * Y_{4(j-d)+3}(x) / (4(j-d)+3)!
                           - sum_{d=0}^{j-1} [1 / (2^{4d+3} (4d+3)!)] * Y_{4(j-d)+1}(x) / (4(j-d)+1)!.
   Consequently, the Hodge-Fredholm kernel projection Pi_ker: V_{4K+1} -> ker(M) = span{P_{4m+1}}_{m=1}^K
   diagonalizes on the midpoint basis Y_p(x) across all p >= 2:
   (a) Pi_ker(Y_{2n}) == 0   (for all n >= 1),
   (b) Pi_ker(Y_{4m+1}) == ((4m + 1) / 4) * P_{4m+1}(x)   (for all m >= 1, pure single-mode projection!),
   (c) Pi_ker(Y_{4j+3}) == sum_{m=1}^j [ (4j + 3)! / (4 * (4m)!) ] * eta_{j-m} * P_{4m+1}(x),
       where sum_{d>=0} eta_d s^{4d+2} := E_3(s/2) / E_1(s/2) = (sinh(s/2) - sin(s/2)) / (sinh(s/2) + sin(s/2))
       (eta_0 = 1/24, eta_1 = -1/53760, eta_2 = 71/7664025600, ...).

3. Theorem 3 (Closed-Form Binomial-Toeplitz Law for Pi_ker(x^p - x), Elementary Cancellation at p = 4K + 4,
   & Reciprocal Krylov-Euler Elimination — Closing Seam `[=~` of seq 241):
   (a) For every p = 4K + 1 + r (K >= 1, r in {0, 1, 2, 3}) and 1 <= m <= K:
           Pi_ker(x^p - x) = sum_{m=1}^K lambda_m(x^p - x) P_{4m+1}(x),
           lambda_m(x^p - x) == (1/4) * C(p, 4m) * tau_{K-m}^{(r)},
       where the 4 Toeplitz sequences tau_d^{(r)} (d >= 0) have the exact generating functions:
           sum_{d>=0} tau_d^{(r)} s^{4d+1+r} / (4d + 1 + r)! == s * (E_{r+1}(s) - delta_{r,3}) / (2 * E_1(s/2)).
   (b) At r = 3 (p = 4K + 4), the identity E_0(s) - 1 == 4 * E_1(s/2) * E_3(s/2) cancels E_1(s/2)
       identically in the denominator, yielding the elementary closed-form formula for all d >= 0:
           tau_d^{(3)} == (d + 1) / 16^d   ==>   lambda_m(x^{4K+4} - x) == ((K - m + 1) / (4 * 16^{K-m})) * C(4K + 4, 4m).
   (c) On the normalized kernel basis P_tilde_{4K+1}(x) := ((4K + 1)/4) P_{4K+1}(x), the (4m+1)-th raw-moment
       coefficients form a pure Binomial-Toeplitz matrix:
           [x^{4m+1}] P_tilde_{4K+1}(x) == C(4K + 1, 4m + 1) / 16^{K-m}   (for all 1 <= m <= K).
       Hence its exact inverse is given by the integer 4-step Krylov-Euler numbers eps_d from
       1 / E_0(u) = 2 / (cosh u + cos u) = sum_{d>=0} eps_d u^{4d} / (4d)! (eps_0..5 = 1, -1, 69, -33661, 60376809, -288294050521):
           P^{red}_{4K+1}(x) := sum_{m=1}^K C(4K + 1, 4m + 1) * (eps_{K-m} / 16^{K-m}) * P_tilde_{4m+1}(x)
       satisfies [x^{4m+1}] P^{red}_{4K+1}(x) == delta_{m,K} for all 1 <= m <= K.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path


def gauss_pow_int(re: int, im: int, e: int) -> tuple[int, int]:
    rr, ri = 1, 0
    br, bi = re, im
    while e > 0:
        if e & 1:
            rr, ri = rr * br - ri * bi, rr * bi + ri * br
        br, bi = br * br - bi * bi, 2 * br * bi
        e >>= 1
    return rr, ri


def poly_add(
    a: list[Fraction],
    b: list[Fraction],
    sa: Fraction = Fraction(1),
    sb: Fraction = Fraction(1),
) -> list[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, c in enumerate(a):
        out[i] += sa * c
    for i, c in enumerate(b):
        out[i] += sb * c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_scale(a: list[Fraction], s: Fraction) -> list[Fraction]:
    s = Fraction(s)
    if s == 0:
        return [Fraction(0)]
    return [c * s for c in a]


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca == 0:
            continue
        for j, cb in enumerate(b):
            if cb != 0:
                out[i + j] += ca * cb
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def cpoly_pow(
    ar: list[Fraction], ai: list[Fraction], e: int
) -> tuple[list[Fraction], list[Fraction]]:
    rr, ri = [Fraction(1)], [Fraction(0)]
    br, bi = ar[:], ai[:]
    while e > 0:
        if e & 1:
            nr = poly_add(poly_mul(rr, br), poly_mul(ri, bi), Fraction(1), Fraction(-1))
            ni = poly_add(poly_mul(rr, bi), poly_mul(ri, br))
            rr, ri = nr, ni
        nr = poly_add(poly_mul(br, br), poly_mul(bi, bi), Fraction(1), Fraction(-1))
        ni = poly_add(poly_mul(br, bi), poly_mul(bi, br))
        br, bi = nr, ni
        e >>= 1
    return rr, ri


def build_ref_u_v_w(j: int) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    """Reference construction of u_j, v_j, w_j by complex polynomial power of w(x) = x + i(1 - x)."""
    wr = [Fraction(0), Fraction(1)]
    wi = [Fraction(1), Fraction(-1)]
    _, ui = cpoly_pow(wr, wi, 4 * j + 2)
    vr_4, vi_4 = cpoly_pow(wr, wi, 4 * j + 4)
    vr_4_pinned = vr_4[:]
    vr_4_pinned[0] -= Fraction(1)
    u = poly_scale(ui, Fraction(1, math.factorial(4 * j + 2)))
    v = poly_scale(vi_4, Fraction(1, math.factorial(4 * j + 4)))
    w = poly_scale(vr_4_pinned, Fraction(1, math.factorial(4 * j + 4)))
    return u, v, w


def single_term_P_4K_plus_1_coeffs(K: int) -> list[Fraction]:
    """Single-term closed-form coefficients of Cloud Jee's boundary-pinned P_{4K+1}(x)."""
    deg = 4 * K
    p_coeffs = [Fraction(0)] * (deg + 2)
    p_coeffs[1] = Fraction(K, (4 * K + 1) * (2 ** (4 * K - 4)))
    for j in range(1, deg + 1):
        _, im_part = gauss_pow_int(1, 1, j)
        sign = -1 if (j & 1) else 1
        q_j = Fraction(sign * math.comb(deg, j), 2 ** (deg - j)) * (
            Fraction(1) + Fraction(im_part, 2 ** (j + 1))
        )
        p_coeffs[j + 1] = Fraction(4, j + 1) * q_j
    return p_coeffs


def single_term_u_v_w_coeffs(j: int) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    """Theorem 1: Single-term closed-form coefficients of u_j(x), v_j(x), w_j(x)."""
    deg_u = 4 * j + 2
    deg_vw = 4 * j + 4
    u = [Fraction(0)] * (deg_u + 1)
    v = [Fraction(0)] * (deg_vw + 1)
    w = [Fraction(0)] * (deg_vw + 1)

    for r in range(1, deg_u + 1):
        _, im_part = gauss_pow_int(1, 1, r)
        sign_u = 1 if (r & 1) else -1
        u[r] = Fraction(sign_u * im_part, math.factorial(r) * math.factorial(deg_u - r))

    for r in range(1, deg_vw + 1):
        re_part, im_part = gauss_pow_int(1, 1, r)
        sign_vw = -1 if (r & 1) else 1
        denom = math.factorial(r) * math.factorial(deg_vw - r)
        v[r] = Fraction(sign_vw * im_part, denom)
        w[r] = Fraction(sign_vw * re_part, denom)

    return u, v, w


def strip_trailing_zeros(p: list[Fraction]) -> list[Fraction]:
    out = p[:]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def build_pinned_midpoint_power(p: int) -> list[Fraction]:
    """Build Y_p(x) = (x - 1/2)^p - [(x - 1/2)^p|_{x=0} (1 - x) + (x - 1/2)^p|_{x=1} x]."""
    yp = [math.comb(p, k) * (Fraction(-1, 2) ** (p - k)) for k in range(p + 1)]
    val0 = yp[0]
    val1 = sum(yp)
    yp[0] -= val0
    yp[1] -= val1 - val0
    return strip_trailing_zeros(yp)


def compute_eta_series(n_terms: int) -> list[Fraction]:
    """Compute eta_d where sum_{d>=0} eta_d s^{4d+2} = E_3(s/2) / E_1(s/2)."""
    e1 = [Fraction(1, (2 ** (4 * d + 1)) * math.factorial(4 * d + 1)) for d in range(n_terms)]
    e3 = [Fraction(1, (2 ** (4 * d + 3)) * math.factorial(4 * d + 3)) for d in range(n_terms)]
    eta = [Fraction(0)] * n_terms
    for d in range(n_terms):
        acc = e3[d]
        for k in range(1, d + 1):
            acc -= e1[k] * eta[d - k]
        eta[d] = acc / e1[0]
    return eta


def compute_krylov_euler_numbers(n_terms: int) -> list[Fraction]:
    """Compute integer 4-step Krylov-Euler numbers eps_d from 1 / E_0(u) = sum_{d>=0} eps_d u^{4d} / (4d)!."""
    eps = [Fraction(0)] * n_terms
    eps[0] = Fraction(1)
    for d in range(1, n_terms):
        eps[d] = -sum(Fraction(math.comb(4 * d, 4 * k)) * eps[d - k] for k in range(1, d + 1))
    return eps


def verify_all() -> dict:
    # 1. Verify Theorem 1: Single-term u_j, v_j, w_j formulas and 4-periodic vanishing for j = 0..5
    for j in range(6):
        u_closed, v_closed, w_closed = single_term_u_v_w_coeffs(j)
        u_ref, v_ref, w_ref = build_ref_u_v_w(j)
        assert strip_trailing_zeros(u_closed) == strip_trailing_zeros(u_ref), f"u_j mismatch at j={j}"
        assert strip_trailing_zeros(v_closed) == strip_trailing_zeros(v_ref), f"v_j mismatch at j={j}"
        assert strip_trailing_zeros(w_closed) == strip_trailing_zeros(w_ref), f"w_j mismatch at j={j}"
        for m in range(1, j + 2):
            if 4 * m < len(u_closed):
                assert u_closed[4 * m] == 0, f"u_j[4m] != 0 at j={j}, m={m}"
            if 4 * m < len(v_closed):
                assert v_closed[4 * m] == 0, f"v_j[4m] != 0 at j={j}, m={m}"
        for m in range(j + 2):
            if 4 * m + 2 < len(w_closed):
                assert w_closed[4 * m + 2] == 0, f"w_j[4m+2] != 0 at j={j}, m={m}"

    # Verify symbolic Taylor proof of Petrovich's (2+i) determinant D_KR(z) for m = 0..7:
    # Each term m in e_0(z)*e_1(-4z) - z*e_3(z)*e_2(-4z) equals (2 + Re[(2+i)^{4m+1}]) / (4*(4m+1)!)
    for m in range(8):
        N = 4 * m + 1
        conv_term = Fraction(0)
        for k in range(m + 1):
            # e_0[m-k] * (-4)^k e_1[k]
            conv_term += Fraction((-4) ** k, math.factorial(4 * (m - k)) * math.factorial(4 * k + 1))
        for k in range(m):
            # - e_3[m-1-k] * (-4)^k e_2[k]
            conv_term -= Fraction((-4) ** k, math.factorial(4 * (m - 1 - k) + 3) * math.factorial(4 * k + 2))
        re_2plusi, _ = gauss_pow_int(2, 1, N)
        closed_term = Fraction(2 + re_2plusi, 4 * math.factorial(N))
        assert conv_term == closed_term, f"D_KR symbolic mismatch at m={m}: {conv_term} vs {closed_term}"

    # 2. Verify Theorem 2: Pointwise v_j convolution identity and Midpoint Diagonalization of Pi_ker
    for j in range(6):
        _, v_ref_j, _ = build_ref_u_v_w(j)
        vj_ref = strip_trailing_zeros(poly_scale(v_ref_j, Fraction(1, (-4) ** (j + 1))))
        conv_poly = [Fraction(0)]
        for d in range(j + 1):
            p = 4 * (j - d) + 3
            scale = Fraction(1, (2 ** (4 * d + 1)) * math.factorial(4 * d + 1) * math.factorial(p))
            conv_poly = poly_add(conv_poly, build_pinned_midpoint_power(p), Fraction(1), scale)
        for d in range(j):
            p = 4 * (j - d) + 1
            scale = Fraction(-1, (2 ** (4 * d + 3)) * math.factorial(4 * d + 3) * math.factorial(p))
            conv_poly = poly_add(conv_poly, build_pinned_midpoint_power(p), Fraction(1), scale)
        assert strip_trailing_zeros(conv_poly) == vj_ref, f"Pointwise v_j identity failed at j={j}"

    # Build monic echelon coimage basis E_d and kernel basis P_{4m+1} up to K = 6 (degree 28)
    E_coim: dict[int, list[Fraction]] = {}
    P_ker: dict[int, list[Fraction]] = {}
    for m in range(7):
        u, v, w = single_term_u_v_w_coeffs(m)
        E_coim[4 * m + 2] = strip_trailing_zeros(
            poly_scale(u, Fraction(-math.factorial(4 * m + 2), 2 * ((-4) ** m)))
        )
        E_coim[4 * m + 3] = strip_trailing_zeros(
            poly_scale(poly_add(v, u), Fraction(-math.factorial(4 * m + 3), 2 * ((-4) ** m)))
        )
        E_coim[4 * m + 4] = strip_trailing_zeros(
            poly_scale(
                poly_add(poly_add(w, v), poly_scale(u, Fraction(1, 2))),
                Fraction(-math.factorial(4 * m + 4), 4 * ((-4) ** m)),
            )
        )
        if m >= 1:
            P_ker[m] = single_term_P_4K_plus_1_coeffs(m)

    def project_to_kernel(poly: list[Fraction]) -> dict[int, Fraction]:
        rem = poly[:]
        lams: dict[int, Fraction] = {}
        for deg in range(len(rem) - 1, 1, -1):
            coeff = rem[deg] if deg < len(rem) else Fraction(0)
            if coeff == 0:
                continue
            if deg % 4 == 1:
                m = deg // 4
                lam = coeff * Fraction(4 * m + 1, 4)
                lams[m] = lam
                rem = poly_add(rem, P_ker[m], Fraction(1), -lam)
            else:
                rem = poly_add(rem, E_coim[deg], Fraction(1), -coeff)
        assert all(c == 0 for c in rem), f"Non-zero residual after Hodge decomposition: {rem}"
        return {m: v for m, v in sorted(lams.items()) if v != 0}

    eta = compute_eta_series(7)
    for p in range(2, 26):
        lams = project_to_kernel(build_pinned_midpoint_power(p))
        if p % 2 == 0:
            assert lams == {}, f"Even midpoint power y^{p} has non-zero kernel projection: {lams}"
        elif p % 4 == 1:
            m = p // 4
            assert lams == {m: Fraction(4 * m + 1, 4)}, f"Midpoint Y_{p} not single-mode: {lams}"
        else:
            j = (p - 3) // 4
            expected = {
                m: Fraction(math.factorial(4 * j + 3), 4 * math.factorial(4 * m)) * eta[j - m]
                for m in range(1, j + 1)
            }
            assert lams == expected, f"Midpoint Y_{p} mismatch: {lams} vs {expected}"

    # 3. Verify Theorem 3: Binomial-Toeplitz Law for Pi_ker(x^p - x), Elementary Cancellation at r=3,
    #    and Krylov-Euler Reduced Raw-Moment Syzygies P^{red}_{4K+1}(x)
    taus_closed: dict[int, list[Fraction]] = {0: [], 1: [], 2: [], 3: []}
    for r in range(4):
        for d in range(6):
            val = Fraction(4 * d + 1 + r, 2 ** (4 * d + r))
            for s in range(d + 1):
                rem_deg = 4 * (d - s) + r - 2
                if rem_deg >= 0:
                    ff = math.factorial(4 * d + 1 + r) // math.factorial(rem_deg)
                    val += Fraction(ff, 2 ** rem_deg) * eta[s]
            taus_closed[r].append(val)
            if r == 3:
                assert val == Fraction(d + 1, 16 ** d), f"Elementary r=3 cancellation failed at d={d}: {val}"

    for p in range(5, 25):
        xp_chord = [Fraction(0)] * (p + 1)
        xp_chord[1] = Fraction(-1)
        xp_chord[p] = Fraction(1)
        lams = project_to_kernel(xp_chord)
        K = (p - 1) // 4
        r = (p - 1) % 4
        for m in range(1, K + 1):
            pred = Fraction(1, 4) * math.comb(p, 4 * m) * taus_closed[r][K - m]
            assert lams.get(m, Fraction(0)) == pred, f"Binomial-Toeplitz mismatch at p={p}, m={m}"

    # Verify Krylov-Euler reduced raw-moment syzygies P^{red}_{4K+1}(x) for K = 1..6
    eps = compute_krylov_euler_numbers(7)
    assert eps[:6] == [
        Fraction(1),
        Fraction(-1),
        Fraction(69),
        Fraction(-33661),
        Fraction(60376809),
        Fraction(-288294050521),
    ]
    P_tilde = {m: [c * Fraction(4 * m + 1, 4) for c in P_ker[m]] for m in range(1, 7)}
    for K in range(1, 7):
        for m in range(1, K + 1):
            assert P_tilde[K][4 * m + 1] == Fraction(math.comb(4 * K + 1, 4 * m + 1), 16 ** (K - m))
        p_red = [Fraction(0)] * (4 * K + 2)
        for m in range(1, K + 1):
            d = K - m
            weight = Fraction(math.comb(4 * K + 1, 4 * m + 1) * eps[d], 16 ** d)
            for idx, c in enumerate(P_tilde[m]):
                p_red[idx] += weight * c
        assert p_red[0] == 0 and sum(p_red) == 0, f"P_red boundary pinning failed at K={K}"
        for m in range(1, K + 1):
            expected = Fraction(1) if m == K else Fraction(0)
            assert p_red[4 * m + 1] == expected, f"Krylov-Euler elimination failed at K={K}, m={m}"

    return {
        "script": "hodge_fredholm_projection_and_krylov_euler_syzygy_2026_11_16.py",
        "theorem_1_4periodic_u_v_w_and_symbolic_2plusi_determinant": True,
        "theorem_2_midpoint_diagonalization_of_Pi_ker_up_to_deg_25": True,
        "eta_0_to_4": [str(c) for c in eta[:5]],
        "theorem_3_binomial_toeplitz_and_krylov_euler_inversion": True,
        "tau_r0_0_to_4": [str(c) for c in taus_closed[0][:5]],
        "tau_r1_0_to_4": [str(c) for c in taus_closed[1][:5]],
        "tau_r2_0_to_4": [str(c) for c in taus_closed[2][:5]],
        "tau_r3_0_to_4": [str(c) for c in taus_closed[3][:5]],
        "krylov_euler_integers_eps_0_to_5": [int(c) for c in eps[:6]],
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    res = verify_all()
    out_path = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out_path.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
