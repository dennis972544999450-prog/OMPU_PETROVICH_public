# Same Count, Different History — Research in Progress (v0.1-wip)

**Full Title:** *Same Count, Different History: Hidden-Height Operators, Shifted Legendre Horizons, and Euler–Bernoulli Cantilever Spectra in Permutation Random Walks*

**Status:** Research in Progress (`v0.1-wip`, `2026-11-07`) — Open Mind Philosophical University (`OMPU.eu`)

## Overview

Continuing Wenpin Tang's work on the permutation random walk (`arXiv:2609.25102v1`), where the running count of positive odd heights $A_n = \sum_{k=1}^n \mathbf{1}_{\{S_{2k-1} > 0\}}$ matches a classical $(1, 1)$ Pólya urn in all one-dimensional marginals and adjacent pairs, this collaborative OMPU research marathon investigates the **non-Markovian hidden-height memory** carried by the walk:

1. **Theorem 1 (MacMahon Ribbon Inclusion-Exclusion):** Exact combinatorial proof without integrals that $\mathbb{P}(E_3 = + \mid +-) = 13/45$ (`26/90`) and $\mathbb{P}(E_3 = + \mid -+) = 32/45$ (`64/90`) via $\binom{6}{2,1,3} - \binom{6}{2,4} - \binom{6}{3,3} + 1 = 60 - 15 - 20 + 1 = 26$.
2. **Theorem 2 (Reflected Differential & Difference Operators):** Any sign switch resets the hidden height $X_n = |S_{2n-1}| - 2\lfloor |S_{2n-1}|/2 \rfloor \in [0, 1]$ via $(T f_0)(x) = \int_0^{1-x}(1-x-t)f_0(t)\,dt$ (`(Tf_0)''(x) = f_0(1-x)`), while any sign repeat evolves across level segments via $(f_j^{\text{new}})''(x) = f_{j-1}(x) - 2f_j(x) + f_{j+1}(x)$.
3. **Theorem 3 (Shifted Legendre Horizon & Streaming Unit-Fraction Identity):** Single-shot orthogonal projection $\Pi_D$ onto shifted Legendre polynomials of degree $D = 2m$ preserves all $m$-step future sign probabilities with **zero error** ($\varepsilon = 0$). In streaming mode starting from $f_1(x) = 1 - x$, $\Pi_D$ is exact ($\varepsilon = 0$) for all $n \le D$, and at $n = D + 1$ the first non-zero streaming error satisfies the exact unit-fraction identity:
   $$p_{D+1}^{\text{exact}} - p_{D+1}^{\text{stream}} = \frac{1}{2(2D+3)\binom{2D+2}{D+1}\,A_{D+1}} \quad (\forall\, D \ge 1)$$
   yielding `1/180, 1/7280, 1/520380, 1/58633344, 1/9538080552, 1/2115969672960` for $D = 1, \dots, 6$.
4. **Theorem 4 (Euler–Bernoulli Cantilever Eigenproblem):** The sign-switch operator $T$ is governed by the fourth-order Euler–Bernoulli clamped-free cantilever boundary value problem $g^{(4)}(u) = \kappa^4 g(u)$ with $\cosh(\kappa)\cos(\kappa) = -1$ and eigenvalues $\lambda_m = (-1)^{m-1}/\kappa_m^2$ ($\lambda_1 \approx +0.2844128719$, $\lambda_2 \approx -0.0453833934$), giving a per-turn memory compression ratio $\rho_{\text{turn}} = (\kappa_2/\kappa_1)^2 \approx 6.2668930258$.
5. **Theorem 5 (Sparre Andersen $O(r^{-2})$ Prefactor & 2nd-Order Edgeworth Asymptotics):**
   - Exact $m$-run Bayesian limits $\hat{p}_\infty(-, 1^m) = 3/10, 71/252, 182/639, 45541/160160, 168388/592033, 120686411/424337760 \to \lambda_1$.
   - Exact 2nd-order Edgeworth expansion $\hat{p}_n(-, 1) = \frac{3}{10} - \frac{3}{175(n-1)} + \frac{2}{175(n-1)^2} + O((n-1)^{-3})$.
   - Exact $O(r^{-2})$ prefactor $C(\tau, \sigma) = \frac{a_\tau - a_\sigma}{2} + \mu_1(\psi_\sigma) - \mu_1(\psi_\tau)$ via Sparre Andersen's $q_{\text{pure}}(m) = \frac{1}{2(m+1)}$, giving $C(\text{`-+`}, \text{`+-`}) = 0.4873088064$.

## Files in This Package

| File | Description |
| :--- | :--- |
| [`PAPER_WORKING_DRAFT_v0.1.md`](./PAPER_WORKING_DRAFT_v0.1.md) | Complete working paper with Theorems 1–5, Open Questions (§7), and Coverage Matrix (§8) |
| [`verify_all_theorems.py`](./verify_all_theorems.py) | Self-contained pure-Python (`stdlib` `fractions.Fraction`) verification of Theorems 1–5 |
| [`meander_prefactor_and_edgeworth2_den_b.py`](./meander_prefactor_and_edgeworth2_den_b.py) | Verification of Sparre Andersen prefactor $C(\tau, \sigma)$ and 2nd-order Edgeworth expansions |
| [`.zenodo.json`](./.zenodo.json) | Zenodo release metadata (`publication_type: workingpaper`) |

## Quick Verification

```bash
python3 verify_all_theorems.py
```

Requires only Python 3 standard library (`fractions`, `math`, `json`) and outputs `"status": "ALL_CHECKS_PASSED"`.
