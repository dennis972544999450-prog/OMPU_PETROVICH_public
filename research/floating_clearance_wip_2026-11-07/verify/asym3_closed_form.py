"""asym-3: nu = 4/(1+sqrt2+sqrt6)^2. All four tight cycles active; KKT multipliers and the separable dual (Thm 4.3)."""
import numpy as np
r2, r6 = np.sqrt(2), np.sqrt(6)
nu = 4 / (1 + r2 + r6) ** 2
s = 2 * np.sqrt(nu)                       # u_r = 1 + x_r on the private side
a, b, y = s - 1, r2 * s - 1, np.sqrt(1.5) * s - 1
Q = [(1 + a) ** 2 / 4, ((1 + a) ** 2 + (1 + b) ** 2) / 12, ((1 - a) ** 2 + (1 - b) ** 2 + 2 * (1 - y) ** 2) / 24, (1 + y) ** 2 / 6]
print("nu closed form", repr(nu))
print("x_A@0, x_A@3, x_A@6 = x_A@9:", a, b, y)
print("Q_i - nu:", [q - nu for q in Q])
g = np.array([[(1 + a) / 2, 0, 0], [(1 + a) / 6, (1 + b) / 6, 0], [-(1 - a) / 12, -(1 - b) / 12, -(1 - y) / 6], [0, 0, (1 + y) / 3]])
M = np.vstack([g.T, np.ones(4)])
lam = np.linalg.solve(M, np.array([0, 0, 0, 1.0]))
print("KKT multipliers (must be >= 0):", lam)
A = lam[2] / 24
B = [lam[0] / 4 + lam[1] / 12, lam[1] / 12, lam[3] / 12, lam[3] / 12]
dual = sum(4 * A * Bi / (A + Bi) for Bi in B)
print("dual value (weak-duality lower bound):", repr(dual), " primal - dual:", nu - dual)
print("structure: u0^2 = 4nu (L=2, one ramp), u0^2+u3^2 = 12nu (L=6), u6^2+u9^2 = 12nu (L=6), big cycle L=12:",
      "sum (2-u)^2 = 24 nu with sum u^2 = 24 nu  =>  sum u = 4  =>  sqrt(nu) = 2/(1+sqrt2+sqrt6)")
