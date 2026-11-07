"""Probe 5: Theorem 7.2 (two partners), the regime 1 < kappa < 4/3, whose upper side the source says it did NOT
check in exact fractions ("Профиль Теоремы 1 при κ < 4/3 в лоб не проверял"), and which V5 does not sample.
Construction (mine): A' trapezoids 0 -> -+K -> 0 on each arc of length 3 (slope 0 at A's marks);
B' = K on [0,3]; on the long arc [3,12]: plateau K for r = 3 - 2K/c, ramp K -> -K (length 2K/c), plateau -K for
l = 6 - 2K/c, ramp -K -> K (length 2K/c). C = B shifted by 6. c = K^2/(6 eps). Exact fractions via fc_verify helpers.
Then the theorem-free grid LP (lower bound on C) at extra kappa values incl. near 4/3 and 2."""
from probe_common import fv, Fr

L = Fr(12)
for kappa in (Fr(101, 100), Fr(11, 10), Fr(6, 5), Fr(5, 4), Fr(4, 3)):
    K = kappa / 3; eps = K - Fr(1, 3); c = K * K / (6 * eps)
    r = 3 - 2 * K / c; l = 6 - 2 * K / c
    assert r >= 0 and l >= 0
    def tr(t0, s):
        return fv.min3_profile(K, Fr(0), Fr(0), c, t0, t0 + 3, s)
    dA = fv.join(tr(Fr(0), -1), tr(Fr(3), 1), tr(Fr(6), -1), tr(Fr(9), 1))
    t1 = 3 + r; t2 = t1 + 2 * K / c; t3 = t2 + l; t4 = t3 + 2 * K / c
    assert t4 == 12
    dB = fv.PWL([(Fr(0), K), (Fr(3), K), (t1, K), (t2, -K), (t3, -K), (Fr(12), K)])
    dC = fv.shift_pwl(dB, Fr(6), L)
    starts = {"A": Fr(0), "B": Fr(-1)}
    starts["C"] = dA.integral(Fr(0), Fr(6)) - 1 - dC.integral(Fr(0), Fr(6))
    ok, txt = fv.check_profile(f"partners kappa={kappa}", K, c, {"A": dA, "B": dB, "C": dC}, L,
                               fv.NAMED["two partners"][1], starts)
    print(("PASS " if ok else "FAIL ") + txt + f"; c = K^2/(6 eps) = {c}")

S = fv.Scheme(*fv.NAMED["two partners"])
for kappa in (Fr(105, 100), Fr(13, 10), Fr(4, 3), Fr(195, 100), Fr(2), Fr(205, 100)):
    K = kappa / 3; eps = K - Fr(1, 3)
    closed = float(K * K / (6 * eps)) if kappa <= 2 else 2 / 9
    v = fv.grid_lp_C(S, K, 2400)
    print(f"grid LP N=2400 kappa={float(kappa):.4f}: C_LP = {v:.7f}, closed form = {closed:.7f}, rel {v/closed-1:+.2e}")
