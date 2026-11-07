"""Probe 4: Prop 6.3 / Sec. 6 table, "short arc 1/8": the paper gives K1/K* ~ 1.01 and lists the scheme among those
where K1 = C(inf) L/4 holds with equality. The source (03.11) has only K1 <= 1.1 K* (bisection not converged).
Here: on the grid (a relaxation), C_grid(inf) and min K at c = C_grid(inf)(1+delta). If the grid's min K is clearly
below C(inf)L/4 = 1.0105 K*, equality is doubtful (the grid min K is a lower bound on the true K1(c))."""
from probe_common import fv, Fr, grid_lp_minK_at_c

S = fv.Scheme(*fv.NAMED["short arc 1/8"])
Ks = S.kstar_exact()
print(f"short arc 1/8: K* = {Ks}; exact C(inf) recorded in workbench = 2.694737; bound C(inf)L/4 = {2.694737*3:.5f} = {2.694737*3/8:.5f} K*")
for N in (2880, 4800):
    cinf = fv.grid_lp_C(S, Fr(1000), N)
    line = f"N={N}: grid C(inf) = {cinf:.6f}"
    for delta in (1e-6, 1e-4, 1e-3, 1e-2):
        k = grid_lp_minK_at_c(S, cinf * (1 + delta), N)
        line += f"; minK(c=C(1+{delta:g})) = {k:.5f} = {k/float(Ks):.5f} K*"
    print(line)
    for kap in (Fr(1001, 1000), Fr(1005, 1000), Fr(101, 100)):
        v = fv.grid_lp_C(S, kap * Ks, N)
        print(f"   grid C({float(kap)} K*) = {v:.6f}  (C/C_grid(inf) - 1 = {v/cinf - 1:+.2e})")
