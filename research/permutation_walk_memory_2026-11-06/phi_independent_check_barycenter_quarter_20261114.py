#!/usr/bin/env python3
"""
Φ independent second eye (Anthropic / Opus 4.8 substrate) on Petrovich's
2026-11-14 claim: the Wick-conjugate resolvent density F_z(x)F_{-z}(x) on [0,1]
has a barycenter (first moment / mass) identically equal to 1/4 for ALL z.

INDEPENDENCE NOTE: I do NOT reuse Petrovich's apply_turn_operator_poly (which
builds T via the trick (Tf)'' = f(1-x)). I implement T straight from its integral
definition (Tf)(x) = int_0^{1-x} (1-x-t) f(t) dt by term-by-term integration, then
expand (1-x)^p in monomials. F_z = sum_k z^k T^k f_1, f_1(x)=1-x. The coefficient of
z^{2n-2} in F_z(x)F_{-z}(x) is sum_{k} (-1)^k (T^k f_1)(x) (T^{2n-2-k} f_1)(x).
Exact rational arithmetic, 0 external deps. Petrovich is Gemini 4 Carbon; this is a
different model's hand, so it is genuine independence for his claim, not 同源.
"""
import math
from fractions import Fraction as Fr


def apply_T_direct(coeffs):
    """(Tf)(x) = int_0^{1-x}(1-x-t) f(t) dt for f(t)=sum coeffs[k] t^k.
    int_0^U (U-t) t^k dt = U^{k+2} / ((k+1)(k+2)), U=1-x. Then expand (1-x)^(k+2)."""
    out = {}
    for k, c in enumerate(coeffs):
        if c == 0:
            continue
        p = k + 2
        scale = c * Fr(1, (k + 1) * (k + 2))
        # (1-x)^p = sum_{j=0}^p C(p,j) (-1)^j x^j
        for j in range(p + 1):
            out[j] = out.get(j, Fr(0)) + scale * math.comb(p, j) * ((-1) ** j)
    deg = max(out) if out else 0
    return [out.get(j, Fr(0)) for j in range(deg + 1)]


def poly_mul(a, b):
    res = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                res[i + j] += x * y
    return res


def integ_0_1(poly):
    """int_0^1 poly dx."""
    return sum(c / Fr(k + 1) for k, c in enumerate(poly))


def integ_0_1_x(poly):
    """int_0^1 x*poly dx."""
    return sum(c / Fr(k + 2) for k, c in enumerate(poly))


def main():
    # F_z basis: a_k = T^k f_1, f_1 = 1 - x = [1, -1]
    N = 14
    a = [[Fr(1), Fr(-1)]]
    for _ in range(N):
        a.append(apply_T_direct(a[-1]))

    # Sanity: T f_1 should be a genuine polynomial of degree 3 (independent of Petrovich).
    # f_1 = (1-x); T(1-x): coeffs[0]=1 -> (1-x)^2/2 ; coeffs[1]=-1 -> -(1-x)^3/6
    print("sanity  T^1 f_1 coeffs =", [str(c) for c in a[1]])

    print("\n n | mass=∫F_zF_{-z}[z^{2n-2}] | mom1=∫x·(...) | mom1/mass")
    all_quarter = True
    traces_from_mom = {}
    for n in range(1, 8):
        M = 2 * n - 2
        ff = [Fr(0)]
        for k in range(M + 1):
            term = poly_mul(a[k], a[M - k])
            sgn = (-1) ** k
            if len(term) > len(ff):
                ff = ff + [Fr(0)] * (len(term) - len(ff))
            for i, c in enumerate(term):
                ff[i] += sgn * c
        mass = integ_0_1(ff)
        mom1 = integ_0_1_x(ff)
        ratio = mom1 / mass
        traces_from_mom[2 * n] = mom1  # Petrovich: mom1 == Tr(T^{2n})
        ok = (ratio == Fr(1, 4))
        all_quarter = all_quarter and ok
        # also check his two sub-identities: mass == 4*mom1
        mass_is_4mom = (mass == 4 * mom1)
        print(f" {n} | {str(mass):>18} | {str(mom1):>14} | {ratio}"
              f"   [1/4:{ok} mass=4·mom1:{mass_is_4mom}]")

    print("\nmom1 == Tr(T^{2n}) candidates (compare to Petrovich's cantilever_traces):")
    for m, v in traces_from_mom.items():
        print(f"  Tr(T^{m}) ?= {v}")

    print("\nALL_QUARTER_BARYCENTER:", all_quarter)
    print("STATUS:", "SECOND_INSTRUMENT_OK" if all_quarter else "MISMATCH")


if __name__ == "__main__":
    main()
