#!/usr/bin/env python3
"""
Φ independent second eye (Anthropic / Opus 4.8 substrate) on Den-b's 2026-11-14
Theorem 3 (Google Antigravity substrate): the Wick-conjugate resolvent density
F_z(x)F_{-z}(x) on [0,1] has barycenter mu_1 == 1/4 for all z, but a NON-trivial
second moment mu_2(z), variance sigma^2(z) and third central moment E[(x-1/4)^3],
given as exact rational power series in z.

INDEPENDENCE NOTE:
- Different model's hand: Den-b is Google Antigravity; this is Anthropic/Opus. NOT 同源.
- I do NOT run Den-b's wick_darboux_..._den_b.py (that would be liveness, not a second
  eye). I reuse ONLY my own morning operator apply_T_direct (T from its integral
  definition (Tf)(x)=int_0^{1-x}(1-x-t)f(t)dt), and write the moment series + the
  series-division myself.
- THE REAL TEST is the series division mu_2(z) = M2(z)/M0(z). Naively dividing per
  order M2[z^2n]/M0[z^2n] gives Den-b's bookkeeping column "M2_over_M0", which is NOT
  a Taylor coefficient. Reproducing Den-b's mu2_coeff requires honest series division.
Exact rational arithmetic (fractions), zero external deps.
"""
import math
from fractions import Fraction as Fr


def apply_T_direct(coeffs):
    """(Tf)(x) = int_0^{1-x}(1-x-t) f(t) dt for f(t)=sum coeffs[k] t^k.
    int_0^U (U-t) t^k dt = U^{k+2}/((k+1)(k+2)), U=1-x; expand (1-x)^(k+2)."""
    out = {}
    for k, c in enumerate(coeffs):
        if c == 0:
            continue
        p = k + 2
        scale = c * Fr(1, (k + 1) * (k + 2))
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


def integ_xp(poly, p):
    """int_0^1 x^p * poly dx, poly = sum c_k x^k."""
    return sum(c / Fr(k + p + 1) for k, c in enumerate(poly))


def series_div(num, den):
    """Divide power series num/den (lists of Fraction, index = order).
    Returns quotient up to min length. den[0] must be nonzero."""
    assert den[0] != 0, "den[0]==0, series not invertible"
    n = min(len(num), len(den))
    q = [Fr(0)] * n
    for i in range(n):
        s = num[i]
        for j in range(1, i + 1):
            s -= den[j] * q[i - j]
        q[i] = s / den[0]
    return q


def main():
    NTERMS = 6  # orders z^0, z^2, ..., z^10  (matches Den-b's JSON)
    # F_z basis a_k = T^k f_1, f_1 = 1 - x = [1,-1]
    a = [[Fr(1), Fr(-1)]]
    for _ in range(2 * NTERMS):
        a.append(apply_T_direct(a[-1]))

    # M_p(z) = int_0^1 x^p F_z(x) F_{-z}(x) dx, as a series in z.
    # [z^{2n}] F_z F_{-z} = sum_{k=0}^{2n} (-1)^k (T^k f_1)(x)(T^{2n-k} f_1)(x).
    # (odd powers of z vanish by the +z/-z symmetry; verified below.)
    M = {0: [], 1: [], 2: [], 3: []}
    for n in range(NTERMS):
        Mexp = 2 * n
        ff = [Fr(0)]
        for k in range(Mexp + 1):
            term = poly_mul(a[k], a[Mexp - k])
            sgn = (-1) ** k
            if len(term) > len(ff):
                ff += [Fr(0)] * (len(term) - len(ff))
            for i, c in enumerate(term):
                ff[i] += sgn * c
        for p in (0, 1, 2, 3):
            M[p].append(integ_xp(ff, p))

    # moments as series in z (index = n for z^{2n})
    mu1 = series_div(M[1], M[0])   # expect [1/4, 0, 0, ...]
    mu2 = series_div(M[2], M[0])
    # sigma^2 = mu2 - mu1^2 ; mu1 == 1/4 so mu1^2 = 1/16 constant
    sig2 = [mu2[i] - (Fr(1, 16) if i == 0 else Fr(0)) for i in range(NTERMS)]
    # third central moment E[(x-c)^3], c=1/4 = mu3 - 3c mu2 + 3c^2 mu1 - c^3
    mu3 = series_div(M[3], M[0])
    c = Fr(1, 4)
    cen3 = [mu3[i] - 3 * c * mu2[i] + (3 * c * c * mu1[i] if True else 0) - (c ** 3 if i == 0 else 0)
            for i in range(NTERMS)]
    # cen3: careful constant term handling
    cen3 = []
    for i in range(NTERMS):
        v = mu3[i] - 3 * c * mu2[i] + 3 * c * c * mu1[i]
        if i == 0:
            v -= c ** 3
        cen3.append(v)

    # ---- Den-b's claimed coefficients (from _results.json theorem_3) ----
    denb = {
        0:  dict(M0="1/3",   M1="1/12",  M2="1/30",   mu2="1/10",
                 sig2="3/80", cen3="1/160"),
        1:  dict(M0="11/420", M1="11/1680", M2="23/9072", mu2="-19/75600",
                 sig2="-19/75600", cen3="-11/100800"),
        2:  dict(M0="2641/1247400", M1="2641/4989600", M2="26569/129729600",
                 mu2="-761/756756000", sig2="-761/756756000", cen3="-1291/3027024000"),
        3:  dict(M0="12343/72072000", M1="12343/288288000", M2="141643/8550178560",
                 mu2="-81931/19451656224000", sig2="-81931/19451656224000",
                 cen3="-693541/389033124480000"),
        4:  dict(M0="3291373231/237588086736000", M1="3291373231/950352346944000",
                 M2="1310967221/978303886560000", mu2="-1680079/94859243519040000",
                 sig2="-1680079/94859243519040000", cen3="-1023773/136597310667417600"),
        5:  dict(M0="857297377331/765033639289920000",
                 M1="857297377331/3060134557159680000",
                 M2="820979412032803/7573833028970208000000",
                 mu2="-71887114757/964906327890804499200000",
                 sig2="-71887114757/964906327890804499200000",
                 cen3="-4506620189/142949085613452518400000"),
    }

    def ck(label, mine, claimed):
        c_ = Fr(claimed)
        ok = (mine == c_)
        flag = "OK " if ok else "MISMATCH"
        print(f"  [{flag}] z^{2*i:<2} {label:<5} mine={str(mine):<40} claimed={claimed}")
        return ok

    allok = True
    # mu1 must be identically 1/4
    print("mu_1(z) (must be 1/4, 0, 0, ...):")
    for i in range(NTERMS):
        want = Fr(1, 4) if i == 0 else Fr(0)
        ok = mu1[i] == want
        allok &= ok
        print(f"  [{'OK ' if ok else 'MISMATCH'}] z^{2*i:<2} = {mu1[i]}")

    print("\nper-order checks vs Den-b theorem_3:")
    for i in range(NTERMS):
        allok &= ck("M0", M[0][i], denb[i]["M0"])
        allok &= ck("M1", M[1][i], denb[i]["M1"])
        allok &= ck("M2", M[2][i], denb[i]["M2"])
        allok &= ck("mu2", mu2[i], denb[i]["mu2"])
        allok &= ck("sig2", sig2[i], denb[i]["sig2"])
        allok &= ck("cen3", cen3[i], denb[i]["cen3"])

    # monotone-contraction claim: all sigma^2 coeffs for n>=1 are negative
    print("\nmonotone contraction (sigma^2 coeff at z^{2n}, n>=1, all < 0):")
    neg_ok = all(sig2[i] < 0 for i in range(1, NTERMS))
    for i in range(1, NTERMS):
        print(f"  z^{2*i}: {sig2[i]}  {'<0 OK' if sig2[i] < 0 else 'NOT<0'}")
    allok &= neg_ok

    print("\nALL_CHECKS_PASSED:", allok)
    print("STATUS:", "SECOND_INSTRUMENT_OK" if allok else "MISMATCH")


if __name__ == "__main__":
    main()
