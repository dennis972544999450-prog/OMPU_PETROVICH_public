#!/usr/bin/env python3
"""
wick_darboux_bifurcated_beam_and_cd_moments_2026_11_14.py
Author: Jee A (ompu-d6a8af238c, Lane A of OMPU stereo pair)
Date: 2026-11-14

Exact rational verification of the Wick-Darboux Derivative Duality System
(derived from Den B's rank-1 anticommutator DT + TD = -f_1 otimes delta_0),
the Bifurcated Fourth-Order Euler-Bernoulli Beam Equations for the symmetric and
antisymmetric Christoffel-Darboux densities, the Bezoutian-Christoffel-Darboux
Synthesis (connecting Den B's Bezoutian Reflection Theorem to Petrovich's
Diagonal Christoffel-Darboux Law), and the Exact Closed-Form Moment Hierarchy
for m_0, m_1, m_2, m_3.

Main Theorems Verified (exact rational arithmetic up to m = 14 / n = 6):
1. First-Order Wick-Darboux Derivative System, Endpoint Reflection & Gradient Factorization:
   From Den B's anticommutator DT + TD = -f_1 otimes delta_0 applied to
   R_z = (I - z T)^{-1} 1 and F_z = (I - z T)^{-1} f_1 on [0, 1]:
       R_z'(x) = -z H_z(0) F_{-z}(x),
       F_z'(x) = -R_{-z}(x) - z F_z(0) F_{-z}(x)       (for all x in [0, 1]),
   where H_z(0) = R_z(0) = -F_z'(0) = Delta(-z)/Delta(z) and F_z(0) = sum_{m>=0} I_0^{(m)} z^m.
   Evaluating at x = 0 yields the Endpoint Chiral Reflection & Conservation Laws:
       F_z(0) = H_z(0) F_{-z}(0),
       rho_{z^2}(0) = F_z(0) F_{-z}(0) = (H_z(0) - H_{-z}(0)) / z = 2 sum_{n>=0} H_0^{(2n+1)} z^{2n},
       rho_{z^2}'(0) = -(F_z(0) + F_{-z}(0)) = -2 sum_{n>=0} I_0^{(2n)} z^{2n}.
   Since H_z(0) H_{-z}(0) = 1, Petrovich's Christoffel-Darboux density
       rho_{z^2}(x) := F_z(x) F_{-z}(x) = -(d/dx) G^{(2)}_{z^2}(x, x)
   admits the exact gradient factorization:
       rho_{z^2}(x) = F_z(x) F_{-z}(x) = -(1/z^2) R_z'(x) R_{-z}'(x)   (for all x in [0, 1]).

2. Reflected Chiral Wronskian & Bifurcated 4th-Order Euler-Bernoulli Beam Laws:
   Define the symmetric and antisymmetric Christoffel-Darboux modes around x = 1/2:
       rho_+(x; z^2) := rho_{z^2}(x) + rho_{z^2}(1 - x),
       rho_-(x; z^2) := rho_{z^2}(x) - rho_{z^2}(1 - x).
   Then for all x in [0, 1]:
   (a) Reflected derivative Wronskian identity:
       F_z'(x) F_{-z}'(1 - x) - F_z'(1 - x) F_{-z}'(x) = z rho_-(x; z^2),
   (b) Reflection-coupled fourth derivative:
       (d/dx)^4 rho_{z^2}(x) = 6 z^2 rho_{z^2}(x) - 10 z^2 rho_{z^2}(1 - x),
   (c) Bifurcated 4th-order Euler-Bernoulli beam equations (eigenvalue ratio 1 : -4):
       (d/dx)^4 rho_+(x; z^2) = -4 z^2 rho_+(x; z^2),
       (d/dx)^4 rho_-(x; z^2) = +16 z^2 rho_-(x; z^2),
   (d) 8th-order uncoupled beam equation for rho_{z^2}(x):
       ((d/dx)^4 + 4 z^2) ((d/dx)^4 - 16 z^2) [F_z(x) F_{-z}(x)] = 0.

3. Bezoutian-Christoffel-Darboux Synthesis (Jee A + Den B + Petrovich):
   Let G^{(2)}_{z^2}(x, y) = (G_z(x, y) - G_{-z}(x, y)) / (2z) be the even-power
   resolvent kernel. Combining Den B's Bezoutian Reflection Theorem on the diagonal
   with Petrovich's Diagonal Christoffel-Darboux Law yields:
       -(d/dx) [ G^{(2)}_{z^2}(x, x) - G^{(2)}_{z^2}(1 - x, 1 - x) ] = rho_+(x; z^2),
       -(d/dx) [ G^{(2)}_{z^2}(x, x) + G^{(2)}_{z^2}(1 - x, 1 - x) ] = rho_-(x; z^2).

4. Topological Boundary Invariants & Exact Closed-Form Moment Hierarchy (m_0, m_1, m_2, m_3):
   Let m_r(z^2) := int_0^1 x^r F_z(x) F_{-z}(x) dx = sum_{n>=0} m_r^{(2n)} z^{2n}.
   Because H_z(0) H_{-z}(0) = 1 = F_z'(1) F_{-z}'(1) for all z, the second derivatives
   of rho_+ and rho_- at x = 0 and x = 1 are topological constants independent of z:
       rho_+''(0; z^2) = rho_+''(1; z^2) = 4,
       rho_-''(0; z^2) = rho_-''(1; z^2) = 0     (for all z),
   while the third derivatives are:
       rho_+'''(0; z^2) = -rho_+'''(1; z^2) = 4 z^2 m_0(z^2),
       rho_-'''(0; z^2) = +rho_-'''(1; z^2) = -8 z^2 m_0(z^2).
   Integrating the bifurcated 4th-order ODEs by parts against 1, x, x^2, x^3 yields
   the exact closed-form moment hierarchy for EVERY n >= 0:
       m_1^{(2n)} = (1/4) m_0^{(2n)},
       m_2^{(2n)} = (1/4) m_0^{(2n)} - I_0^{(2n+2)},
       m_3^{(2n)} = (1/4) m_0^{(2n)} - (15/8) I_0^{(2n+2)} + (3/4) H_0^{(2n+3)}.
"""

import json
import os
import shutil
from fractions import Fraction

RESEARCH_DIR = "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06"


def poly_add(p1, p2, scale2=Fraction(1)):
    L = max(len(p1), len(p2))
    res = [Fraction(0)] * L
    for i, c in enumerate(p1):
        res[i] += c
    for i, c in enumerate(p2):
        res[i] += scale2 * c
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def poly_mul(p1, p2):
    res = [Fraction(0)] * (len(p1) + len(p2) - 1)
    for i, a in enumerate(p1):
        for j, b in enumerate(p2):
            res[i + j] += a * b
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def poly_deriv(poly, order=1):
    res = list(poly)
    for _ in range(order):
        if len(res) <= 1:
            res = [Fraction(0)]
        else:
            res = [k * res[k] for k in range(1, len(res))]
    return res


def poly_integrate(poly):
    return [Fraction(0)] + [c / Fraction(k + 1) for k, c in enumerate(poly)]


def poly_eval(poly, x):
    val = Fraction(0)
    for k in range(len(poly) - 1, -1, -1):
        val = val * x + poly[k]
    return val


def poly_int_moment(poly, r=0):
    return sum(c / Fraction(k + r + 1) for k, c in enumerate(poly))


def poly_reflect(poly):
    """Given P(x), return P(1 - x) in monomial basis."""
    n = len(poly)
    res = [Fraction(0)] * n
    binom = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        binom[i][0] = Fraction(1)
        for j in range(1, i + 1):
            binom[i][j] = binom[i - 1][j - 1] + binom[i - 1][j]
    for k, c in enumerate(poly):
        for j in range(k + 1):
            res[j] += c * ((-1) ** j) * binom[k][j]
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def apply_T(poly):
    """(T g)(x) = int_0^{1-x} (1 - x - y) g(y) dy."""
    return poly_reflect(poly_integrate(poly_integrate(poly)))


def verify_all():
    M_max = 12  # up to z^12 (n = 6), with boundary generators up to m = 15
    one_poly = [Fraction(1)]
    f1_poly = [Fraction(1), Fraction(-1)]

    Tk_1 = [one_poly]
    Tk_f1 = [f1_poly]
    for _ in range(1, M_max + 4):
        Tk_1.append(apply_T(Tk_1[-1]))
        Tk_f1.append(apply_T(Tk_f1[-1]))

    # Boundary generators:
    # H_0^{(m)} = [z^m] H_z(0) = (T^m 1)(0) = -(T^m f_1)'(0)
    # F_0^{(m)} = [z^m] F_z(0) = (T^m f_1)(0) (with odd terms F_0^{(2n+1)} = m_0^{(2n)} = 4 Theta_{2n})
    # I_0^{(m)} = [z^m] I_0(z) = -(T^{m+1} 1)'(0) = int_0^1 (T^m 1)(x) dx
    H0 = [poly_eval(Tk_1[m], Fraction(0)) for m in range(M_max + 4)]
    F0 = [poly_eval(Tk_f1[m], Fraction(0)) for m in range(M_max + 4)]
    I0 = [-poly_eval(poly_deriv(Tk_1[m + 1], 1), Fraction(0)) for m in range(M_max + 3)]
    for m in range(M_max + 4):
        assert H0[m] == -poly_eval(poly_deriv(Tk_f1[m], 1), Fraction(0))

    # Check H_z(0) H_{-z}(0) = 1 and Endpoint Chiral Factorization I_0(z) = H_z(0) F_{-z}(0):
    for m in range(M_max + 3):
        conv_H = sum(((-1) ** j) * H0[j] * H0[m - j] for j in range(m + 1))
        assert conv_H == (Fraction(1) if m == 0 else Fraction(0))
        conv_HF = sum(H0[j] * ((-1) ** (m - j)) * F0[m - j] for j in range(m + 1))
        assert conv_HF == I0[m], f"Endpoint Chiral Factorization I_0(z) = H_z(0) F_{{-z}}(0) failed at m={m}"

    # =========================================================================
    # THEOREM 1: First-Order Wick-Darboux Derivative System & Gradient Factorization
    #   R_z'(x) = -z H_z(0) F_{-z}(x)
    #   F_z'(x) = -R_{-z}(x) - z F_z(0) F_{-z}(x)
    #   rho_{z^2}(x) := F_z(x) F_{-z}(x) = -(1/z^2) R_z'(x) R_{-z}'(x)
    # =========================================================================
    for m in range(M_max + 2):
        # [z^m] R_z'(x) == (T^m 1)'(x)
        lhs_R = poly_deriv(Tk_1[m], 1)
        # [z^m] (-z H_z(0) F_{-z}(x)) = - sum_{j=0}^{m-1} H0[j] (-1)^{m-1-j} Tk_f1[m-1-j]
        rhs_R = [Fraction(0)]
        for j in range(m):
            k = m - 1 - j
            rhs_R = poly_add(rhs_R, Tk_f1[k], -H0[j] * ((-1) ** k))
        assert lhs_R == rhs_R, f"R_z' Wick-Darboux failed at m={m}"

        # [z^m] F_z'(x) == (T^m f_1)'(x)
        lhs_F = poly_deriv(Tk_f1[m], 1)
        # [z^m] (-R_{-z}(x) - z F_z(0) F_{-z}(x))
        rhs_F = poly_add([Fraction(0)], Tk_1[m], Fraction(-((-1) ** m)))
        for j in range(m):
            k = m - 1 - j
            rhs_F = poly_add(rhs_F, Tk_f1[k], -F0[j] * ((-1) ** k))
        assert lhs_F == rhs_F, f"F_z' Wick-Darboux failed at m={m}"


    # Construct C_{2n}(x) = [z^{2n}] F_z(x) F_{-z}(x) and check gradient factorization
    C = {}
    for n in range(M_max // 2 + 1):
        m = 2 * n
        poly = [Fraction(0)]
        for k in range(m + 1):
            poly = poly_add(poly, poly_mul(Tk_f1[k], Tk_f1[m - k]), Fraction((-1) ** k))
        C[n] = poly

        # Check endpoint conservation laws:
        # C_{2n}(0) == 2 H_0^{(2n+1)} and C_{2n}'(0) == -2 I_0^{(2n)}
        assert poly_eval(C[n], Fraction(0)) == Fraction(2) * H0[2 * n + 1]
        assert poly_eval(poly_deriv(C[n], 1), Fraction(0)) == Fraction(-2) * I0[2 * n]

        # Check C_{2n}(x) == [z^{2n+2}] (- R_z'(x) R_{-z}'(x))
        grad_poly = [Fraction(0)]
        for k in range(1, m + 2):
            j = m + 2 - k
            grad_poly = poly_add(
                grad_poly,
                poly_mul(poly_deriv(Tk_1[k], 1), poly_deriv(Tk_1[j], 1)),
                Fraction(-((-1) ** j)),
            )
        assert C[n] == grad_poly, f"Gradient factorization failed at n={n}"

    # =========================================================================
    # THEOREM 2: Reflected Chiral Wronskian & Bifurcated 4th-Order Beam Equations
    # =========================================================================
    rho_plus = {}
    rho_minus = {}
    for n in range(M_max // 2 + 1):
        m = 2 * n
        rho_plus[n] = poly_add(C[n], poly_reflect(C[n]), Fraction(1))
        rho_minus[n] = poly_add(C[n], poly_reflect(C[n]), Fraction(-1))

        # Check (a): [z^{2n+1}] (F_z'(x) F_{-z}'(1-x) - F_z'(1-x) F_{-z}'(x)) == rho_minus[n](x)
        wronsk_refl = [Fraction(0)]
        for k in range(m + 2):
            j = m + 1 - k
            Fp_k = poly_deriv(Tk_f1[k], 1)
            Fp_j = poly_deriv(Tk_f1[j], 1)
            term1 = poly_mul(Fp_k, poly_reflect(Fp_j))
            term2 = poly_mul(poly_reflect(Fp_k), Fp_j)
            diff = poly_add(term1, term2, Fraction(-1))
            wronsk_refl = poly_add(wronsk_refl, diff, Fraction((-1) ** j))
        assert wronsk_refl == rho_minus[n], f"Reflected chiral Wronskian failed at n={n}"

        if n >= 1:
            # Check (b): D^4 C[n](x) == 6 C[n-1](x) - 10 C[n-1](1-x)
            d4_C = poly_deriv(C[n], 4)
            rhs_C = poly_add(
                poly_add([Fraction(0)], C[n - 1], Fraction(6)),
                poly_reflect(C[n - 1]),
                Fraction(-10),
            )
            assert d4_C == rhs_C, f"Reflection-coupled 4th-order ODE failed at n={n}"

            # Check (c): D^4 rho_plus[n] == -4 rho_plus[n-1] and D^4 rho_minus[n] == +16 rho_minus[n-1]
            d4_plus = poly_deriv(rho_plus[n], 4)
            d4_minus = poly_deriv(rho_minus[n], 4)
            assert d4_plus == poly_add([Fraction(0)], rho_plus[n - 1], Fraction(-4))
            assert d4_minus == poly_add([Fraction(0)], rho_minus[n - 1], Fraction(16))

        if n >= 2:
            # Check (d): 8th-order uncoupled beam equation (D^8 - 12 z^2 D^4 - 64 z^4) rho_{z^2}(x) = 0
            d8_C = poly_deriv(C[n], 8)
            d4_prev = poly_deriv(C[n - 1], 4)
            comb = poly_add(d8_C, d4_prev, Fraction(-12))
            comb = poly_add(comb, C[n - 2], Fraction(-64))
            assert comb == [Fraction(0)], f"8th-order beam equation failed at n={n}"

    # =========================================================================
    # THEOREM 3: Bezoutian-Christoffel-Darboux Synthesis (Jee A + Den B + Petrovich)
    #   For even m = 2n+2, Den B's Gohberg-Semencul diagonal K_{2n+2}(x, x) = int_x^1 C_n(s) ds
    #   satisfies Petrovich's Diagonal CD Law -(d/dx) K_{2n+2}(x, x) = C_n(x),
    #   and Den B's diagonal Bezoutian sum
    #     B_{2n+2}(x, x) = sum_{k=0}^{2n+1} [(T^k 1)(1-x)(T^{2n+1-k} f_1)(x) - (T^k f_1)(1-x)(T^{2n+1-k} 1)(x)]
    #   equals K_{2n+2}(x, x) - K_{2n+2}(1-x, 1-x) and satisfies:
    #     -(d/dx) B_{2n+2}(x, x) = C_n(x) + C_n(1-x) = rho_plus[n](x),
    #     -(d/dx) [K_{2n+2}(x, x) + K_{2n+2}(1-x, 1-x)] = C_n(x) - C_n(1-x) = rho_minus[n](x).
    # =========================================================================
    for n in range(M_max // 2 + 1):
        m = 2 * n + 2
        # From Den B's even-m Gohberg-Semencul formula on y = x: K_{2n+2}(x, x) = int_x^1 C_n(s) ds
        anti_C = poly_integrate(C[n])
        val_at_1 = poly_eval(anti_C, Fraction(1))
        Km_diag = poly_add([val_at_1], anti_C, Fraction(-1))

        # Construct Den B's Bezoutian sum on y = x:
        bez_sum = [Fraction(0)]
        for k in range(m):
            t1 = poly_mul(poly_reflect(Tk_1[k]), Tk_f1[m - 1 - k])
            t2 = poly_mul(poly_reflect(Tk_f1[k]), Tk_1[m - 1 - k])
            diff = poly_add(t1, t2, Fraction(-1))
            bez_sum = poly_add(bez_sum, diff, Fraction(1))

        bez_diag = poly_add(Km_diag, poly_reflect(Km_diag), Fraction(-1))
        sym_diag = poly_add(Km_diag, poly_reflect(Km_diag), Fraction(1))
        assert bez_sum == bez_diag, f"Bezoutian diagonal identity failed at n={n}"
        assert poly_add([Fraction(0)], poly_deriv(bez_sum, 1), Fraction(-1)) == rho_plus[n]
        assert poly_add([Fraction(0)], poly_deriv(sym_diag, 1), Fraction(-1)) == rho_minus[n]


    # =========================================================================
    # THEOREM 4: Topological Boundary Invariants & Exact Closed-Form Moment Hierarchy
    #   For EVERY n >= 0:
    #     m_1^{(2n)} = (1/4) m_0^{(2n)}
    #     m_2^{(2n)} = (1/4) m_0^{(2n)} - I_0^{(2n+2)}
    #     m_3^{(2n)} = (1/4) m_0^{(2n)} - (15/8) I_0^{(2n+2)} + (3/4) H_0^{(2n+3)}
    # =========================================================================
    moments_summary = {}
    for n in range(M_max // 2 + 1):
        m0 = poly_int_moment(C[n], 0)
        m1 = poly_int_moment(C[n], 1)
        m2 = poly_int_moment(C[n], 2)
        m3 = poly_int_moment(C[n], 3)

        # Topological 2nd derivatives at x=0 and x=1:
        d2_plus = poly_deriv(rho_plus[n], 2)
        d2_minus = poly_deriv(rho_minus[n], 2)
        expected_d2_plus = Fraction(4) if n == 0 else Fraction(0)
        assert poly_eval(d2_plus, Fraction(0)) == expected_d2_plus
        assert poly_eval(d2_plus, Fraction(1)) == expected_d2_plus
        assert poly_eval(d2_minus, Fraction(0)) == Fraction(0)
        assert poly_eval(d2_minus, Fraction(1)) == Fraction(0)

        # Exact closed-form formulas for m_1, m_2, m_3 for ALL n >= 0:
        assert m1 == Fraction(1, 4) * m0
        assert m2 == Fraction(1, 4) * m0 - I0[2 * n + 2]
        assert m3 == Fraction(1, 4) * m0 - Fraction(15, 8) * I0[2 * n + 2] + Fraction(3, 4) * H0[2 * n + 3]

        if n >= 1:
            m0_prev = poly_int_moment(C[n - 1], 0)
            d3_plus = poly_deriv(rho_plus[n], 3)
            d3_minus = poly_deriv(rho_minus[n], 3)
            assert poly_eval(d3_plus, Fraction(0)) == Fraction(4) * m0_prev
            assert poly_eval(d3_plus, Fraction(1)) == Fraction(-4) * m0_prev
            assert poly_eval(d3_minus, Fraction(0)) == Fraction(-8) * m0_prev
            assert poly_eval(d3_minus, Fraction(1)) == Fraction(-8) * m0_prev

        moments_summary[f"n={n} (z^{2*n})"] = {
            "m0": str(m0),
            "m1": str(m1),
            "m1_over_m0": str(m1 / m0),
            "m2": str(m2),
            "m3": str(m3),
            "I0_2n_plus_2": str(I0[2 * n + 2]),
            "H0_2n_plus_3": str(H0[2 * n + 3]),
            "rho_0_eq_2_H0_2n_plus_1": str(poly_eval(C[n], Fraction(0))),
            "rho_prime_0_eq_minus_2_I0_2n": str(poly_eval(poly_deriv(C[n], 1), Fraction(0))),
        }

    print("=== WICK-DARBOUX SYSTEM, BIFURCATED BEAM ODEs & CD MOMENT HIERARCHY ===")
    for n in range(M_max // 2 + 1):
        info = moments_summary[f"n={n} (z^{2*n})"]
        print(
            f"  n={n} (z^{2*n:2d}): m0={info['m0']:>25s} | m1/m0={info['m1_over_m0']} | "
            f"m2={info['m2']:>28s} | m3={info['m3']:>28s}"
        )
    print("ALL_CHECKS_PASSED")

    return {
        "theorems_verified": [
            "1. First-Order Wick-Darboux Derivative System: R_z'(x) = -z H_z(0) F_{-z}(x), F_z'(x) = -R_{-z}(x) - z F_z(0) F_{-z}(x)",
            "2. Endpoint Chiral Reflection & Conservation Laws: F_z(0) = H_z(0) F_{-z}(0), rho_{z^2}(0) = 2 sum H_0^{(2n+1)} z^{2n}, rho_{z^2}'(0) = -2 sum I_0^{(2n)} z^{2n}",
            "3. Gradient Factorization: F_z(x) F_{-z}(x) = -(1/z^2) R_z'(x) R_{-z}'(x)",
            "4. Reflected Chiral Wronskian: F_z'(x) F_{-z}'(1-x) - F_z'(1-x) F_{-z}'(x) = z [F_z(x) F_{-z}(x) - F_z(1-x) F_{-z}(1-x)]",
            "5. Bifurcated 4th-Order Euler-Bernoulli Beam Equations: D^4 rho_+ = -4 z^2 rho_+, D^4 rho_- = +16 z^2 rho_-",
            "6. Bezoutian-Christoffel-Darboux Synthesis: -(d/dx)[G^{(2)}_{z^2}(x,x) -/+ G^{(2)}_{z^2}(1-x,1-x)] = rho_{+/-}(x; z^2)",
            "7. Topological Boundary Invariants: rho_+''(0) = 4, rho_-''(0) = 0, rho_+'''(0) = 4 z^2 m_0, rho_-'''(0) = -8 z^2 m_0",
            "8. Exact Closed-Form Moment Hierarchy (for all n>=0): m_1^{(2n)} = (1/4) m_0^{(2n)}, m_2^{(2n)} = (1/4) m_0^{(2n)} - I_0^{(2n+2)}, m_3^{(2n)} = (1/4) m_0^{(2n)} - (15/8) I_0^{(2n+2)} + (3/4) H_0^{(2n+3)}",
        ],
        "moments_m0_m1_m2_m3_n_0_to_6": moments_summary,
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "wick_darboux_bifurcated_beam_and_cd_moments_2026_11_14_results.json",
    )
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    if os.path.isdir(RESEARCH_DIR):
        dst_py = os.path.join(
            RESEARCH_DIR, "wick_darboux_bifurcated_beam_and_cd_moments_2026_11_14.py"
        )
        dst_json = os.path.join(
            RESEARCH_DIR, "wick_darboux_bifurcated_beam_and_cd_moments_2026_11_14_results.json"
        )
        if os.path.abspath(__file__) != os.path.abspath(dst_py):
            shutil.copy2(os.path.abspath(__file__), dst_py)
        if os.path.abspath(out_json) != os.path.abspath(dst_json):
            shutil.copy2(out_json, dst_json)
