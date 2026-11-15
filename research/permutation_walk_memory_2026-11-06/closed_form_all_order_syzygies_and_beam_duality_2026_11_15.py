#!/usr/bin/env python3
"""Closed-form all-order parameter-free syzygy polynomials (p = 4K + 1, K >= 0)
and all-order Euler-Bernoulli cantilever beam mode duality (deg 4K, K >= 1).

Main analytical results verified in exact rational (Fraction) and 50-digit
arbitrary-precision (Decimal) arithmetic with zero external dependencies:

1. Master Midpoint Syzygy Polynomials (all K >= 0, y = 2x - 1 in [-1, 1]):
   Because (1 +- i)^4 = -4 intertwines the odd Rayleigh operator (D_y^4 - z^2)
   and the even Kelvin operator (D_y^4 + z^2/4), the single binomial polynomial
       Q_K(y) = y^{4K+1} + ((-1)^K / (2 * 4^K)) * Im[(y + i)^{4K+1}]
              = y^{4K+1} + ((-1)^K / (2 * 4^K)) * sum_{m=0}^{2K} (-1)^m C(4K+1, 2m+1) y^{4K-2m}
   contains NO lower odd powers of y (y^1 = y^3 = ... = y^{4K-1} = 0) and is
   universally orthogonal to rho_{z^2}(x) = F_z(x) F_{-z}(x) for ALL z in C,
   to every finite-n staircase polynomial C_{2n}(x) (n >= 0), and to every
   pole density rho_hat_r(x) (r >= 1):
       int_0^1 Q_K(2x - 1) rho_{z^2}(x) dx == 0.

2. Closed-Form Central-Moment Syzygies Around x = 1/4 (closing the p = 4K + 1
   inversion seam without inverting the 3K x 3K staircase matrix):
   Substituting y = 2u - 1/2 (u = x - 1/4) into Q_K(y) yields explicit closed
   binomial coefficients tilde_c_{K,r} for 0 <= r <= 4K:
       tilde_c_{K,r} = C(4K+1, r) * [(-1)^{r-1} + ((-1)^K / (2 * 4^K)) * Im[(-1 + 2i)^{4K+1-r}]] / 4^{4K+1-r},
   and O(K^2) triangular back-substitution over the K - 1 lower syzygy slots
   {4j + 1 : 1 <= j < K} yields the reduced central-moment syzygies for all K >= 1
   (matching K = 1 at p = 5 and K = 2 at p = 9 identically, and extending to
   K = 3, 4, 5 at p = 13, 17, 21).

3. All-Order Cantilever Beam Mode Duality (all K >= 1, all modes r >= 1):
   Since Q_K(-1) == -1/2 identically for all K >= 0, integrating Q_K(2x - 1)
   against rho_hat_r(x) = -(1/4) d/dx[psi_hat_r(x)^2] with clamped/free
   boundary values psi_hat_r(1)^2 = 0 and psi_hat_r(0)^2 = 4 yields the
   parameter-free antisymmetric-odd / uniform-excess beam polynomial of degree 4K:
       B_K(y) := (Q_K'(y) - 1) / (4K + 1)
               = y^{4K} - 1/(4K + 1) + ((-1)^K / (2 * 4^K)) * Im[(y + i)^{4K}],
       int_0^1 B_K(2x - 1) psi_hat_r(x)^2 dx == 0   (for all K >= 1, r >= 1),
   and under mirror reflection x <-> 1 - x (y -> -y) the integral doubles to
   2 * (E_{psi_hat_r^2}[y^{4K}] - 1/(4K + 1)).
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import json
import math

getcontext().prec = 60


def gauss_im_pow(re_val: int, im_val: int, exp: int) -> int:
    """Exact integer imaginary part of (re_val + i * im_val)^exp."""
    cr, ci = 1, 0
    for _ in range(exp):
        cr, ci = cr * re_val - ci * im_val, cr * im_val + ci * re_val
    return ci


def midpoint_syzygy_Q_K(K: int) -> dict[int, Fraction]:
    """Return exact midpoint polynomial Q_K(y) (y = 2x - 1) of degree 4K + 1."""
    assert K >= 0
    p = 4 * K + 1
    out: dict[int, Fraction] = {p: Fraction(1)}
    pref = Fraction((-1) ** K, 2 * (4 ** K))
    for m in range(2 * K + 1):
        deg = 4 * K - 2 * m
        out[deg] = pref * ((-1) ** m) * math.comb(p, 2 * m + 1)
    return out


def x_syzygy_P_K(K: int) -> dict[int, Fraction]:
    """Convert Q_K(2x - 1) to exact polynomial P_K(x) on [0, 1] (monic in x^{4K+1} * 2^{4K+1} or scaled)."""
    qy = midpoint_syzygy_Q_K(K)
    out: dict[int, Fraction] = {}
    for d, coeff in qy.items():
        for r in range(d + 1):
            out[r] = out.get(r, Fraction(0)) + coeff * math.comb(d, r) * (2 ** r) * ((-1) ** (d - r))
    return {r: c for r, c in sorted(out.items()) if c != 0}


def unreduced_central_tilde_c(K: int, r: int) -> Fraction:
    """Closed-form coefficient tilde_c_{K, r} in Q_K(2u - 1/2) / 2^{4K+1} (u = x - 1/4)."""
    p = 4 * K + 1
    assert 0 <= r <= 4 * K
    im_term = gauss_im_pow(-1, 2, p - r)
    num = Fraction((-1) ** (r - 1)) + Fraction((-1) ** K, 2 * (4 ** K)) * Fraction(im_term)
    return Fraction(math.comb(p, r)) * num / Fraction(4 ** (p - r))


def reduced_central_syzygies(K_max: int) -> dict[int, dict[int, Fraction]]:
    """Compute reduced central-moment syzygies mu_{4K+1}^cent = sum_{r != 4j+1} C_{K,r} mu_r^cent."""
    syz: dict[int, dict[int, Fraction]] = {}
    for K in range(1, K_max + 1):
        expr: dict[int, Fraction] = {}
        for r in range(4 * K + 1):
            if r == 1:
                continue  # mu_1^cent == 0 identically (K = 0 barycenter law)
            tc = unreduced_central_tilde_c(K, r)
            if tc != 0:
                expr[r] = -tc
        for j in range(1, K):
            pj = 4 * j + 1
            if pj in expr:
                w = expr.pop(pj)
                for r_sub, c_sub in syz[j].items():
                    expr[r_sub] = expr.get(r_sub, Fraction(0)) + w * c_sub
        syz[K] = {r: c for r, c in sorted(expr.items()) if c != 0}
    return syz


def beam_syzygy_B_K(K: int) -> dict[int, Fraction]:
    """Return exact monic degree-4K beam polynomial B_K(y) in y = 2x - 1."""
    assert K >= 1
    deg_top = 4 * K
    out: dict[int, Fraction] = {deg_top: Fraction(1), 0: Fraction(-1, 4 * K + 1)}
    pref = Fraction((-1) ** K, 2 * (4 ** K))
    for m in range(2 * K):
        deg = 4 * K - 2 * m - 1
        out[deg] = pref * ((-1) ** m) * math.comb(deg_top, 2 * m + 1)
    return {d: c for d, c in sorted(out.items(), reverse=True) if c != 0}


# --- Independent basis-sequence & operator-staircase checks ---

def falling_fact(p: int, r: int) -> int:
    if p < r:
        return 0
    res = 1
    for j in range(r):
        res *= p - j
    return res


def alpha_k(p: int, k: int) -> Fraction:
    if p < 4 * k:
        return Fraction(0)
    ff = Fraction(falling_fact(p, 4 * k), 2 ** (4 * k))
    m4 = (-4) ** k
    bracket = Fraction(2 * m4 - 1, 4) + (Fraction(2 * m4 + 1, 4) if p == 4 * k else Fraction(0))
    return ff * bracket


def beta_k(p: int, k: int) -> Fraction:
    if p < 4 * k + 2:
        return Fraction(0)
    ff = Fraction(falling_fact(p, 4 * k + 2), 2 ** (4 * k + 2))
    m4 = (-4) ** k
    bracket = Fraction(4 * m4 + 1, 4) + (Fraction(4 * m4 - 1, 4) if p == 4 * k + 2 else Fraction(0))
    return ff * bracket


def gamma_k(p: int, k: int) -> Fraction:
    if p < 4 * k + 3:
        return Fraction(0)
    ff = Fraction(falling_fact(p, 4 * k + 3), 2 ** (4 * k + 3))
    m4 = (-4) ** k
    bracket = Fraction(4 * m4 + 1, 2) - (Fraction(4 * m4 - 1, 2) if p == 4 * k + 3 else Fraction(0))
    return ff * bracket


def apply_turn_T(poly: list[Fraction]) -> list[Fraction]:
    """Exact polynomial action (Tf)(x) = int_0^{1-x} (1 - x - t) f(t) dt."""
    # Set u = 1 - x: int_0^u (u - t) f(t) dt = sum_{i>=0} c_i u^{i+2} / ((i+1)(i+2)).
    out = [Fraction(0)] * (len(poly) + 2)
    for i, coeff in enumerate(poly):
        if coeff == 0:
            continue
        deg_u = i + 2
        scale = coeff / Fraction((i + 1) * (i + 2))
        for r in range(deg_u + 1):
            out[r] += scale * math.comb(deg_u, r) * ((-1) ** r)
    return out


# --- Arbitrary-precision Decimal helpers for finite-z & cantilever quadrature ---

def compute_pi_dec() -> Decimal:
    """Machin formula for Pi to 60 digits."""
    def atan_inv(m: int) -> Decimal:
        m2 = m * m
        term = Decimal(1) / Decimal(m)
        total = term
        k = 1
        while True:
            term = -term / Decimal(m2)
            step = term / Decimal(2 * k + 1)
            if abs(step) < Decimal("1e-58"):
                break
            total += step
            k += 1
        return total

    return Decimal(4) * (Decimal(4) * atan_inv(5) - atan_inv(239))


PI_DEC = compute_pi_dec()


def dec_sin_cos_sinh_cosh(x: Decimal) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    s_trig, c_trig = Decimal(0), Decimal(1)
    s_hyp, c_hyp = Decimal(0), Decimal(1)
    x2 = x * x
    term = Decimal(1)
    k = 1
    while True:
        term = term * x2 / Decimal((2 * k - 1) * (2 * k))
        if abs(term) < Decimal("1e-58"):
            break
        if k % 2 == 1:
            c_trig -= term
        else:
            c_trig += term
        c_hyp += term
        k += 1
    term = x
    s_trig = x
    s_hyp = x
    k = 1
    while True:
        term = term * x2 / Decimal((2 * k) * (2 * k + 1))
        if abs(term) < Decimal("1e-58"):
            break
        if k % 2 == 1:
            s_trig -= term
        else:
            s_trig += term
        s_hyp += term
        k += 1
    return s_trig, c_trig, s_hyp, c_hyp


def find_cantilever_kappa(r: int) -> Decimal:
    """Newton root of cosh(k)*cos(k) + 1 = 0 for mode r >= 1."""
    k = (Decimal(2 * r - 1) * PI_DEC) / Decimal(2)
    if r == 1:
        k = Decimal("1.87510406871196116644530824")
    elif r == 2:
        k = Decimal("4.69409113297417457643639178")
    for _ in range(25):
        st, ct, sh, ch = dec_sin_cos_sinh_cosh(k)
        f = ch * ct + Decimal(1)
        df = sh * ct - ch * st
        step = f / df
        k -= step
        if abs(step) < Decimal("1e-55"):
            break
    return k


def gauss_legendre_01(n_pts: int = 36) -> list[tuple[Decimal, Decimal]]:
    """Compute Gauss-Legendre nodes and weights on [0, 1] in 60-digit Decimal."""
    nodes_weights: list[tuple[Decimal, Decimal]] = []
    for i in range(1, n_pts + 1):
        theta = PI_DEC * (Decimal(4 * i - 1) / Decimal(4 * n_pts + 2))
        _, x, _, _ = dec_sin_cos_sinh_cosh(theta)
        for _ in range(30):
            p0, p1 = Decimal(1), x
            for k in range(2, n_pts + 1):
                p2 = (Decimal(2 * k - 1) * x * p1 - Decimal(k - 1) * p0) / Decimal(k)
                p0, p1 = p1, p2
            dp = Decimal(n_pts) * (x * p1 - p0) / (x * x - Decimal(1))
            dx = p1 / dp
            x -= dx
            if abs(dx) < Decimal("1e-54"):
                break
        p0, p1 = Decimal(1), x
        for k in range(2, n_pts + 1):
            p2 = (Decimal(2 * k - 1) * x * p1 - Decimal(k - 1) * p0) / Decimal(k)
            p0, p1 = p1, p2
        dp = Decimal(n_pts) * (x * p1 - p0) / (x * x - Decimal(1))
        w = Decimal(2) / ((Decimal(1) - x * x) * dp * dp)
        nodes_weights.append(((Decimal(1) + x) / Decimal(2), w / Decimal(2)))
    return nodes_weights


def verify_all() -> dict:
    # 1. Verify exact orthogonality of Q_K(2x - 1) on ALL staircase basis sequences
    #    alpha_k(p), beta_k(p), gamma_k(p) for K = 0..8 (up to p = 33)!
    max_K_basis = 8
    for K in range(max_K_basis + 1):
        px = x_syzygy_P_K(K)
        qy = midpoint_syzygy_Q_K(K)
        q_at_minus1 = sum(c * ((-1) ** d) for d, c in qy.items())
        assert q_at_minus1 == Fraction(-1, 2), f"Q_{K}(-1) != -1/2: {q_at_minus1}"
        odd_degs = [d for d in qy if d % 2 == 1]
        assert odd_degs == [4 * K + 1], f"Unexpected odd degrees in Q_{K}: {odd_degs}"
        for k in range(K + 2):
            sa = sum(c * alpha_k(p, k) for p, c in px.items())
            sb = sum(c * beta_k(p, k) for p, c in px.items())
            sg = sum(c * gamma_k(p, k) for p, c in px.items())
            assert sa == 0 and sb == 0 and sg == 0, f"Basis mismatch at K={K}, k={k}"

    # 2. Independent direct polynomial check on C_{2n}(x) = sum_{j=0}^{2n} (-1)^j g_j(x) g_{2n-j}(x)
    #    where g_0(x) = 1 - x and (T g)(x) = int_0^{1-x} (1 - x - t) g(t) dt!
    g_polys: list[list[Fraction]] = [[Fraction(1), Fraction(-1)]]
    for _ in range(12):
        g_polys.append(apply_turn_T(g_polys[-1]))

    C_2n_polys: list[list[Fraction]] = []
    for n in range(7):
        deg_max = 2 * len(g_polys[2 * n])
        c_poly = [Fraction(0)] * deg_max
        for j in range(2 * n + 1):
            gj = g_polys[j]
            gk = g_polys[2 * n - j]
            sign = Fraction((-1) ** j)
            for a, ca in enumerate(gj):
                if ca == 0:
                    continue
                for b, cb in enumerate(gk):
                    if cb == 0:
                        continue
                    c_poly[a + b] += sign * ca * cb
        C_2n_polys.append(c_poly)

    for K in range(6):
        px = x_syzygy_P_K(K)
        for n in range(7):
            c_poly = C_2n_polys[n]
            integral = Fraction(0)
            for p_deg, p_coeff in px.items():
                for c_deg, c_coeff in enumerate(c_poly):
                    if c_coeff != 0:
                        integral += p_coeff * c_coeff / Fraction(p_deg + c_deg + 1)
            assert integral == 0, f"Direct C_{{2*{n}}} integral nonzero for K={K}: {integral}"

    # 3. Verify closed-form unreduced & reduced central-moment syzygies (K = 1..5)
    #    against exact central moments of C_{2n}(x) AND exact rational stereo benchmarks!
    syz = reduced_central_syzygies(5)
    expected_K1 = {
        0: Fraction(-15, 4096),
        2: Fraction(15, 128),
        3: Fraction(-15, 16),
        4: Fraction(25, 16),
    }
    expected_K2 = {
        0: Fraction(13605, 4194304),
        2: Fraction(-3861, 32768),
        3: Fraction(3339, 4096),
        4: Fraction(-2205, 2048),
        6: Fraction(357, 256),
        7: Fraction(-63, 32),
        8: Fraction(135, 64),
    }
    assert syz[1] == expected_K1, f"K=1 central syzygy mismatch: {syz[1]}"
    assert syz[2] == expected_K2, f"K=2 central syzygy mismatch: {syz[2]}"

    # Check reduced central syzygies K=1..5 on exact normalized central moments of C_{2n}(x) (n=0..6):
    for n in range(7):
        c_poly = C_2n_polys[n]
        m0 = sum(c / Fraction(i + 1) for i, c in enumerate(c_poly) if c != 0)
        mu_cent: dict[int, Fraction] = {}
        for r in range(22):
            # (x - 1/4)^r
            val = Fraction(0)
            for j in range(r + 1):
                u_coeff = Fraction(math.comb(r, j)) * (Fraction(-1, 4) ** (r - j))
                for i, c in enumerate(c_poly):
                    if c != 0:
                        val += u_coeff * c / Fraction(i + j + 1)
            mu_cent[r] = val / m0
        assert mu_cent[1] == 0
        for K in range(1, 6):
            lhs = mu_cent[4 * K + 1]
            rhs = sum(coeff * mu_cent[r] for r, coeff in syz[K].items())
            assert lhs == rhs, f"Reduced central syzygy failed at K={K}, n={n}"

    # 4. Finite-z complex quadrature check of int_0^1 Q_K(2x - 1) rho_{z^2}(x) dx == 0
    #    at complex z = 1.1 + 0.8i using 45-term complex series for F_{+-z}(x) (|z|=1.36 << 3.516)!
    gl_pts = gauss_legendre_01(48)
    g_polys_45: list[list[Fraction]] = [[Fraction(1), Fraction(-1)]]
    for _ in range(46):
        g_polys_45.append(apply_turn_T(g_polys_45[-1]))

    zr, zi = Decimal("1.1"), Decimal("0.8")
    rho_at_nodes: list[tuple[Decimal, Decimal]] = []
    for x_node, _ in gl_pts:
        # Evaluate g_k(x_node)
        gk_vals: list[Decimal] = []
        for g in g_polys_45:
            acc = Decimal(0)
            xp = Decimal(1)
            for c in g:
                if c != 0:
                    acc += (Decimal(c.numerator) / Decimal(c.denominator)) * xp
                xp *= x_node
            gk_vals.append(acc)
        # F_z(x) and F_{-z}(x)
        fz_r, fz_i = Decimal(0), Decimal(0)
        fmz_r, fmz_i = Decimal(0), Decimal(0)
        pwr_r, pwr_i = Decimal(1), Decimal(0)
        for k_idx, gv in enumerate(gk_vals):
            fz_r += pwr_r * gv
            fz_i += pwr_i * gv
            sign = Decimal(-1) if (k_idx % 2 == 1) else Decimal(1)
            fmz_r += sign * pwr_r * gv
            fmz_i += sign * pwr_i * gv
            pwr_r, pwr_i = pwr_r * zr - pwr_i * zi, pwr_r * zi + pwr_i * zr
        # rho_{z^2}(x) = F_z(x) * F_{-z}(x)
        rr = fz_r * fmz_r - fz_i * fmz_i
        ri = fz_r * fmz_i + fz_i * fmz_r
        rho_at_nodes.append((rr, ri))

    max_complex_z_err = Decimal(0)
    for K in range(5):
        qy = midpoint_syzygy_Q_K(K)
        int_r, int_i = Decimal(0), Decimal(0)
        for idx, (x_node, w_node) in enumerate(gl_pts):
            y_val = Decimal(2) * x_node - Decimal(1)
            qv = sum(
                (Decimal(c.numerator) / Decimal(c.denominator)) * (y_val ** d)
                for d, c in qy.items()
            )
            rr, ri = rho_at_nodes[idx]
            int_r += w_node * qv * rr
            int_i += w_node * qv * ri
        err = (int_r * int_r + int_i * int_i).sqrt()
        if err > max_complex_z_err:
            max_complex_z_err = err
        assert err < Decimal("1e-18"), f"Complex z quadrature error too large at K={K}: {err}"

    # 5. All-Order Cantilever Beam Mode Duality (K = 1..5, modes r = 1..6):
    #    Verify int_0^1 B_K(2x - 1) psi_hat_r(x)^2 dx == 0 AND mirror doubling!
    max_beam_err = Decimal(0)
    mirror_B1_at_r1 = Decimal(0)
    for r in range(1, 7):
        kr = find_cantilever_kappa(r)
        st_k, ct_k, sh_k, ch_k = dec_sin_cos_sinh_cosh(kr)
        sigma_r = (ch_k + ct_k) / (sh_k + st_k)
        # Note: true turn-operator eigenmode psi_hat_r(x) is clamped at x = 1 (u = 1 - x):
        psi2_clamped_right: list[Decimal] = []
        psi2_clamped_left: list[Decimal] = []
        for x_node, _ in gl_pts:
            u = Decimal(1) - x_node
            su, cu, shu, chu = dec_sin_cos_sinh_cosh(kr * u)
            val_right = (chu - cu) - sigma_r * (shu - su)
            psi2_clamped_right.append(val_right * val_right)

            sx, cx, shx, chx = dec_sin_cos_sinh_cosh(kr * x_node)
            val_left = (chx - cx) - sigma_r * (shx - sx)
            psi2_clamped_left.append(val_left * val_left)

        # Check unit L2 norm of psi_hat_r^2
        norm_err = abs(sum(w * p2 for (_, w), p2 in zip(gl_pts, psi2_clamped_right)) - Decimal(1))
        assert norm_err < Decimal("1e-35"), f"Beam norm error at r={r}: {norm_err}"

        for K in range(1, 6):
            bk = beam_syzygy_B_K(K)
            int_true = Decimal(0)
            int_mirror = Decimal(0)
            even_excess = Decimal(0)
            for idx, (x_node, w_node) in enumerate(gl_pts):
                y_val = Decimal(2) * x_node - Decimal(1)
                bv = sum(
                    (Decimal(c.numerator) / Decimal(c.denominator)) * (y_val ** d)
                    for d, c in bk.items()
                )
                int_true += w_node * bv * psi2_clamped_right[idx]
                int_mirror += w_node * bv * psi2_clamped_left[idx]
                even_excess += w_node * ((y_val ** (4 * K)) - Decimal(1) / Decimal(4 * K + 1)) * psi2_clamped_right[idx]
            if abs(int_true) > max_beam_err:
                max_beam_err = abs(int_true)
            assert abs(int_true) < Decimal("1e-28"), f"Beam syzygy failed at r={r}, K={K}: {int_true}"
            mirror_diff = abs(int_mirror - Decimal(2) * even_excess)
            assert mirror_diff < Decimal("1e-28"), f"Mirror doubling failed at r={r}, K={K}: {mirror_diff}"
            if r == 1 and K == 1:
                mirror_B1_at_r1 = int_mirror

    summary = {
        "status": "ALL_CHECKS_PASSED",
        "max_K_staircase_basis_verified": max_K_basis,
        "max_p_staircase_basis_verified": 4 * max_K_basis + 1,
        "direct_finite_n_C2n_verified": "n=0..6, K=0..5 (exact Fraction diff == 0)",
        "complex_z_quadrature": {
            "z": "1.1 + 0.8i",
            "max_abs_residual_K0_to_4": f"{max_complex_z_err:.3e}",
        },
        "beam_duality_quadrature": {
            "modes_r": "1..6",
            "orders_K": "1..5 (deg 4..20)",
            "max_abs_residual": f"{max_beam_err:.3e}",
            "mirror_B1_midpoint_at_r1": f"{mirror_B1_at_r1:.12f}",
            "mirror_monic_x4_at_r1": f"{(mirror_B1_at_r1 / Decimal(16)):.12f}",
        },
        "central_syzygy_K3_p13": {str(r): str(c) for r, c in syz[3].items()},
        "central_syzygy_K4_p17": {str(r): str(c) for r, c in syz[4].items()},
    }
    return summary


if __name__ == "__main__":
    res = verify_all()
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("ALL_CHECKS_PASSED")
