# Same Count, Different History: Hidden-Height Operators, Shifted Legendre Horizons, and Euler–Bernoulli Cantilever Spectra in Permutation Random Walks

**Status:** *Research in Progress (`v0.1-wip` · Working Paper for GitHub ↔ Zenodo)*  
**Date:** November 6, 2026  
**Authors:** Dennis Belsky (`ORCID: 0000-0002-2988-7501`), Petrovich (`Codex / Anthropic / Antigravity / Grok`), Jee-AGY (`Gemini 4 Argon`), Jee A (`Stereo Lane A`), Den B (`Stereo Lane B`), X (`OMPU_X`)  
**Affiliation:** OMPU — Open Mind Philosophical University (`ompu.eu`)  
**Reproducibility:** Pure Python 3 standard library (`verify_all_theorems.py`, 0 external dependencies)

---

## Abstract

Following Wenpin Tang (*arXiv:2609.25102v1*), let $\pi = (\pi_0, \pi_1, \dots, \pi_m)$ be a uniform random permutation of $\{1, \dots, m+1\}$, let $X_i = \mathbf{1}_{\{\pi_i > \pi_{i-1}\}} - \mathbf{1}_{\{\pi_i < \pi_{i-1}\}} \in \{\pm 1\}$ be its up-down step signs, and let $S_t = \sum_{i=1}^t X_i$ be the associated discrete height walk. Because $S_{2k-1}$ is always odd and nonzero, the cumulative count of positive odd heights $A_n = \sum_{k=1}^n \mathbf{1}_{\{S_{2k-1} > 0\}}$ is uniformly distributed on $\{0, 1, \dots, n\}$ and matches classical Pólya$(1, 1)$ urn statistics in all one-dimensional and adjacent-pair marginals $(A_{n-1}, A_n)$. Yet the binary indicator process $I_k = \mathbf{1}_{\{S_{2k-1} > 0\}}$ is strictly non-exchangeable and non-Markovian.

In this working paper (*Research in Progress*), we establish five exact analytical and combinatorial results characterizing how the sign process remembers its past and how sign switches reset that memory:
1. **Direct Combinatorial Splitting via MacMahon's Ribbon Theorem (§2):** For $A_2 = 1$, the history `+-` pins $S_3 = -1$ and restricts `+-+` to a single 5-step descent signature $(+, -, -, +, +)$ ($D = \{2, 3\}$ in $\mathfrak{S}_6$), giving $\binom{6}{2,1,3} - \binom{6}{2,4} - \binom{6}{3,3} + \binom{6}{6} = 60 - 15 - 20 + 1 = 26$ permutations and $\mathbb{P}(+ \mid +-) = 13/45$, whereas `-+` pins $S_3 = +1$ and gives $\mathbb{P}(+ \mid -+) = 32/45$.
2. **Piecewise Differential-Difference Operator on Unit Intervals (§3):** In Tang's continuous triangular representation $T_k = \sum_{j=1}^k Y_j$ ($f_Y(y) = (1 - |y|)_+$), the unnormalized density $f_j(x) = f_k(j+x)$ ($x \in [0, 1]$) of $|T_k|$ satisfies:
   - **Sign switch ($\sigma_k \neq \sigma_{k-1}$):** Complete reset onto $j = 0$ ($[0, 1]$) via $(T f_0)(x) = \int_0^{1-x} (1 - x - t) f_0(t)\,dt$, i.e., $(f_0^{\text{new}})''(x) = f_0(1-x)$ with $f_0^{\text{new}}(1) = (f_0^{\text{new}})'(1) = 0$.
   - **Sign repeat ($\sigma_k = \sigma_{k-1}$):** Exact equivalence between continuous second derivatives and discrete second differences across unit intervals, $(f_j^{\text{new}})''(x) = f_{j-1}(x) - 2 f_j(x) + f_{j+1}(x)$.
3. **Exact $m$-Step Horizon via Shifted Legendre Projection $D = 2m$ (§4):** Orthogonal $L^2([0, 1])$ projection $\Pi_D$ of each unit piece $f_j(x)$ onto shifted Legendre polynomials $P_d^*(x) = P_d(2x-1)$ of degree $d \le D = 2m$ ($2m+1$ moments per unit interval) preserves the conditional probability of every $m$-step future sign continuation with **zero error ($\varepsilon = 0$)**.
4. **Euler–Bernoulli Cantilever Spectrum of Sign Switches (§5):** The compact self-adjoint turn operator $T = R\mathcal{I}^2$ on $L^2([0, 1])$ reduces under $g(u) = \phi(1-u)$ to the classical 4th-order **Euler–Bernoulli (1744) cantilever beam boundary value problem** $g^{(4)}(u) = \kappa^4 g(u)$, $g(0)=g'(0)=g''(1)=g'''(1)=0$, with characteristic equation $\cosh(\kappa_m)\cos(\kappa_m) = -1$ and eigenvalues $\lambda_m = (-1)^{m-1} / \kappa_m^2$ ($\lambda_1 \approx +0.284412871855$, $\lambda_2 \approx -0.045383393443$). Consequently, each sign switch compresses pre-turn memory by the asymptotic factor $\rho_{\text{turn}} = (\kappa_2/\kappa_1)^2 \approx \mathbf{6.266893025771}$, with alternating-sign oscillations caused by $\lambda_2 < 0 < \lambda_3$.
5. **Hierarchy of Forgotten Information, $O(r^{-2})$ Gap Decay, and Wiener–Hopf Limits (§6):** When two distinct prefixes are followed by $r$ identical signs, their one-step forecast gap decays as $O(r^{-2})$. For the 2-parameter summary $(\text{sign}, r)$, the Bayesian forecast at $r=1$ admits the exact Edgeworth expansion $\hat{p}_n(-, 1) = \frac{3}{10} - \frac{3}{175(n-1)} + O(n^{-2})$, while the extreme histories `'+'^{n-1} '-'` and `'-'^{n-2} '+-'` converge to Wiener–Hopf limits $P_{\max}(\infty) \approx 0.3151600752$ and $P_{\min}(\infty) \approx 0.2793320208$, bounding the worst-case error of $(\text{sign}, r)$ by $\frac{3}{10} - P_{\min}(\infty) \approx \mathbf{0.0206679792}$ as $n \to \infty$.

---

## 1. Setup and the Pólya-Urn Paradox

Let $\pi = (\pi_0, \pi_1, \dots, \pi_{2n})$ be a uniform random permutation of $\{1, \dots, 2n+1\}$, and let
$$X_i = \begin{cases} +1 & \text{if } \pi_i > \pi_{i-1}, \\ -1 & \text{if } \pi_i < \pi_{i-1}, \end{cases} \qquad S_t = \sum_{i=1}^t X_i.$$
At odd times $t = 2k-1$, the height $S_{2k-1}$ is an odd integer and therefore never zero. Let $\sigma_k = \operatorname{sgn}(S_{2k-1}) \in \{+, -\}$ denote the sign of the $k$-th odd height, and let $A_n = \sum_{k=1}^n \mathbf{1}_{\{\sigma_k = +\}}$ be the number of positive odd heights up to step $2n-1$.

By Tang (*arXiv:2609.25102v1*), the sequence of odd heights has the same law as the signs of $T_k = \sum_{j=1}^k Y_j$, where $Y_1, Y_2, \dots$ are i.i.d. symmetric triangular random variables on $(-1, 1)$ with density $f_Y(y) = 1 - |y|$. Moreover:
- $A_n \sim \operatorname{Uniform}\{0, 1, \dots, n\}$, matching the classical Pólya$(1, 1)$ urn;
- Every adjacent pair $(A_{n-1}, A_n)$ matches the Pólya$(1, 1)$ transition law $\mathbb{P}(A_n = a+1 \mid A_{n-1} = a) = \frac{a+1}{n+1}$.

However, conditioning on the ordered sign history $(\sigma_1, \dots, \sigma_{n-1})$ rather than the scalar count $A_{n-1}$ breaks exchangeability starting at $n = 3$: for $A_2 = 1$, Pólya's urn predicts $\frac{1+1}{2+2} = \frac{1}{2}$, whereas
$$\mathbb{P}(\sigma_3 = + \mid \sigma_1\sigma_2 = \text{`+-`}) = \frac{13}{45} \approx 0.2889, \qquad \mathbb{P}(\sigma_3 = + \mid \sigma_1\sigma_2 = \text{`-+`}) = \frac{32}{45} \approx 0.7111.$$

---

## 2. Theorem 1: Direct Combinatorial Proof via MacMahon's Ribbon Theorem

**Lemma 2.1 (Sign-Switch Pinning at Odd Steps).** *Because $S_{2k+1} - S_{2k-1} = X_{2k} + X_{2k+1} \in \{-2, 0, +2\}$ while $S_{2k-1}$ is odd, any sign change between consecutive odd steps ($\sigma_k \neq \sigma_{k+1}$) forces $|S_{2k-1}| = |S_{2k+1}| = 1$. Specifically:*
- $\sigma_k \sigma_{k+1} = \text{`+-`} \implies S_{2k-1} = +1,\; X_{2k} = X_{2k+1} = -1,\; S_{2k+1} = -1$;
- $\sigma_k \sigma_{k+1} = \text{`-+`} \implies S_{2k-1} = -1,\; X_{2k} = X_{2k+1} = +1,\; S_{2k+1} = +1$.

**Theorem 2.2 (Combinatorial Derivation of $26/720 = 13/360$ and $13/45$ vs $32/45$).** *In $\mathfrak{S}_6$ ($6! = 720$ permutations of $\{1, \dots, 6\}$):*
1. *Every permutation with $\sigma_1\sigma_2 = \text{`+-`}$ has $(X_1, X_2, X_3) = (+1, -1, -1)$ and $S_3 = -1$ ($90$ permutations in total, since $\mathbb{P}(\text{`+-`}) = 1/8 = 90/720$).*
2. *To reach $S_5 > 0$ from $S_3 = -1$, the next two steps are uniquely forced to be $(X_4, X_5) = (+1, +1)$ ($S_5 = +1$). Thus the event $\sigma_1\sigma_2\sigma_3 = \text{`+-+`}$ consists of a single 5-step up-down signature $(+, -, -, +, +)$, i.e.,*
   $$\pi_0 < \pi_1 > \pi_2 > \pi_3 < \pi_4 < \pi_5 \quad (\text{descent set } D = \{2, 3\} \subset \{1, 2, 3, 4, 5\}).$$
3. *By MacMahon's ribbon inclusion-exclusion formula for the composition $(2, 1, 3)$ of $6$, the number of permutations in $\mathfrak{S}_6$ with descent set $D = \{2, 3\}$ is*
   $$N(\{2, 3\}) = \binom{6}{2, 1, 3} - \binom{6}{2, 4} - \binom{6}{3, 3} + \binom{6}{6} = 60 - 15 - 20 + 1 = \mathbf{26}.$$
4. *Consequently, $\mathbb{P}(\text{`+-+`}) = \frac{26}{720} = \frac{13}{360}$ and $\mathbb{P}(+ \mid \text{`+-`}) = \frac{26}{90} = \mathbf{\frac{13}{45}}$. By reflection symmetry $\pi_i \mapsto 7 - \pi_i$, $\mathbb{P}(- \mid \text{`-+`}) = \frac{13}{45}$ and therefore*
   $$\mathbb{P}(+ \mid \text{`-+`}) = 1 - \frac{13}{45} = \frac{64}{90} = \mathbf{\frac{32}{45}}.$$

*(Note: Those 64 permutations for `-++` split at $t=5$ into $59$ paths with $S_5 = +1$ and $5 = \binom{6}{1} - 1$ paths with signature $(-, +, +, +, +)$ and $S_5 = +3$.)*

---

## 3. Theorem 2: Piecewise Differential-Difference Operator for Hidden Height

In Tang's triangular representation $T_k = T_{k-1} + Y_k$ ($f_Y(y) = (1 - |y|)_+$ on $(-1, 1)$), let $U_k = |T_k| > 0$ be the continuous distance of $T_k$ from zero after a fixed sign history $\sigma = (\sigma_1, \dots, \sigma_k)$. Its unnormalized density is supported on $[0, r+1]$, where $r \ge 0$ is the number of consecutive repeats at the end of $\sigma$, and is piecewise polynomial of degree $2k-1$ on each unit interval:
$$f_j(x) = f_{U_k}(j + x), \qquad x \in [0, 1], \quad j = 0, 1, \dots, r.$$

**Theorem 3.1 (Reset on Sign Switch and Discrete-Continuous Identity on Repeat).**
1. **Sign Switch ($\sigma_{k+1} \neq \sigma_k$):** *Because $|Y_{k+1}| < 1$, a sign change is possible only from the boundary unit interval $j = 0$ ($U_k \in (0, 1)$). All higher pieces $j \ge 1$ are annihilated ($f_j^{\text{new}} \equiv 0$ for $j \ge 1$), and the new density on $[0, 1]$ is given by the reflected double-integration operator $T = R\mathcal{I}^2$:*
   $$f_0^{\text{new}}(x) = (T f_0)(x) = \int_0^{1-x} (1 - x - t)\,f_0(t)\,dt, \qquad (f_0^{\text{new}})''(x) = f_0(1 - x), \quad f_0^{\text{new}}(1) = (f_0^{\text{new}})'(1) = 0.$$
   *In particular, for the purely alternating sign sequence $+ - + - \dots$ of length $n$, the density $f_n(x)$ on $[0, 1]$ satisfies the boundary value problem $f_n''(x) = f_{n-1}(1-x)$ with $f_n(1)=f_n'(1)=0$ and $f_1(x) = 1 - x$, yielding exact probabilities $1/2,\; 1/8,\; 13/360,\; 59/5760,\; 661/226800,\; 12031/14515200$ ($397\,023 / 12!$) for $n = 1, \dots, 6$.*
2. **Sign Repeat ($\sigma_{k+1} = \sigma_k$):** *On every unit interval $[j, j+1]$ ($x \in (0, 1)$), the continuous second derivative of the updated piece equals the discrete second difference across adjacent unit intervals:*
   $$(f_j^{\text{new}})''(x) = f_{j-1}(x) - 2 f_j(x) + f_{j+1}(x).$$
3. **One-Step Forecast Functional:** *Given the pieces $\{f_j\}_{j=0}^r$ of total mass $M = \sum_{j=0}^r \int_0^1 f_j(x)\,dx$, the conditional probability that the next sign flips is determined solely by the quadratic moment on the boundary interval $j = 0$:*
   $$\mathbb{P}(\sigma_{k+1} \neq \sigma_k \mid \sigma) = \frac{1}{M}\int_0^1 \frac{1}{2}(1 - x)^2 f_0(x)\,dx.$$

---

## 4. Theorem 3: Exact $m$-Step Horizon via Shifted Legendre Projection $D = 2m$

Let $P_d^*(x) = P_d(2x - 1)$ ($d = 0, 1, \dots$) be the orthogonal shifted Legendre polynomials on $[0, 1]$, and let $\Pi_D : L^2([0, 1]) \to \mathbb{P}_D([0, 1])$ be the orthogonal projection onto polynomials of degree $\le D$ (storing $D+1$ moments per unit interval).

**Theorem 4.1 (Single-Shot Horizon $D = 2m$ and Streaming Horizon $n \le D$ with Unit-Fraction First Error).** *Because double integration maps $\mathcal{I}^2 P_d^* \in \operatorname{span}(P_{d-2}^*, P_d^*, P_{d+2}^*)$ for $d \ge 2$ (orthogonal to $\mathbb{P}_{d-3}$) while the reflection $R P_d^*(x) = P_d^*(1-x) = (-1)^d P_d^*(x)$ preserves degree, the adjoint of each step operator raises the polynomial degree of the test functional $\frac{1}{2}(1-x)^2 \in \mathbb{P}_2$ by at most $2$ per step. Consequently:*
1. **Single-Shot Horizon ($D = 2m$):** *Applying $\Pi_D$ once to an arbitrary density $f_k$ with $D = 2m$ ($2m+1$ numbers per unit interval) preserves the exact conditional probability of every $m$-step future sign continuation $(\sigma_{k+1}, \dots, \sigma_{k+m})$ with **zero error ($\varepsilon = 0$)**.*
2. **Streaming Horizon ($n \le D$) and Exact Unit-Fraction Identity at $n = D + 1$ (Petrovich, 2026-11-07):** *In recursive streaming compression $\tilde{f}_s = \Pi_D\mathcal{L}\tilde{f}_{s-1}$ starting from $f_1(x) = 1 - x$, the forecast error is **identically zero ($\varepsilon = 0$) for all trajectory lengths $n \le D$** ($n_{\text{exact}} = \lfloor(D+1)/2\rfloor + 1 + \lfloor(D-2)/2\rfloor = D$). At the first non-exact step $n = D + 1$ along the alternating trajectory, the denominator mass is still exact ($\tilde{M}_{D+1} = M_{D+1} = A_{D+1}/(2D+2)!$, where $A_{D+1}$ is the integer count of alternating-sign permutations in $S_{2D+2}$: $A_2=3, A_3=26, A_4=413, A_5=10\,576, A_6=397\,023, A_7=20\,551\,376$), while the numerator loses the single highest Legendre mode $P_{D+1}^*$ of weight $\Delta M_{D+2} = \bigl[2(2D+3)\binom{2D+2}{D+1}(2D+2)!\bigr]^{-1}$. Thus $(2D+2)!$ cancels identically, and the first non-zero streaming error is always a **unit fraction** for all $D \ge 1$:*
   $$p_{D+1}^{\text{exact}} - p_{D+1}^{\text{stream}} = \mathbf{\frac{1}{2(2D+3)\binom{2D+2}{D+1}\,A_{D+1}}} = \frac{1}{180},\; \frac{1}{7\,280},\; \frac{1}{520\,380},\; \frac{1}{58\,633\,344},\; \frac{1}{9\,538\,080\,552},\; \frac{1}{2\,115\,969\,672\,960} \quad (D=1,\dots,6).$$

---

## 5. Theorem 4: Euler–Bernoulli Cantilever Beam Spectrum of Sign Switches

**Theorem 5.1 (Cantilever Eigenvalue Problem for $T = R\mathcal{I}^2$).** *The sign-switch operator $(T f)(x) = \int_0^{1-x} (1 - x - t) f(t)\,dt$ has symmetric kernel $K(x, t) = (1 - x - t)_+$ and is compact and self-adjoint on $L^2([0, 1])$. For any eigenfunction $T \phi = \lambda \phi$, setting $u = 1 - x$ and $g(u) = \phi(1 - u)$ yields $g''(u) = \lambda^{-1} g(1 - u)$ and hence the 4th-order boundary value problem*
$$g^{(4)}(u) = \kappa^4 g(u) \quad \bigl(\kappa = |\lambda|^{-1/2}\bigr), \qquad g(0) = g'(0) = 0, \quad g''(1) = g'''(1) = 0.$$
*This is identical to the classical **Euler–Bernoulli (1744) vibrating cantilever beam** clamped at $u = 0$ ($x = 1$) and free at $u = 1$ ($x = 0$). Its roots $\kappa_1 < \kappa_2 < \kappa_3 < \dots$ satisfy*
$$\cosh(\kappa_m)\cos(\kappa_m) = -1, \qquad \lambda_m = \frac{(-1)^{m-1}}{\kappa_m^2} \quad (m = 1, 2, 3, \dots).$$
*Numerically:*
- $m = 1:\quad \kappa_1 \approx 1.875104068712, \qquad \lambda_1 = +1/\kappa_1^2 \approx \mathbf{+0.284412871855}$;
- $m = 2:\quad \kappa_2 \approx 4.694091132974, \qquad \lambda_2 = -1/\kappa_2^2 \approx \mathbf{-0.045383393443}$;
- $m = 3:\quad \kappa_3 \approx 7.854757438238, \qquad \lambda_3 = +1/\kappa_3^2 \approx \mathbf{+0.016208187185}$.

**Corollaries:**
1. **Asymptotic Flip Probability of an Alternating Saw:** $\lim_{n\to\infty} \mathbb{P}(\text{flip} \mid (\text{`+-`})^n) = \lambda_1 = \kappa_1^{-2} \approx 0.284412871855$.
2. **Exact Per-Turn Memory Compression Factor:** Each sign switch contracts the projectively normalized hidden-height profile toward $\phi_1$ at the asymptotic rate
   $$\rho_{\text{turn}} = \frac{\lambda_1}{|\lambda_2|} = \left(\frac{\kappa_2}{\kappa_1}\right)^2 \approx \mathbf{6.266893025771}.$$
3. **Alternating Overshoot:** Because $\lambda_2 < 0 < \lambda_3$, the subleading correction flips sign at every consecutive turn, explaining the empirical oscillation of finite-step compression ratios (`8.62 -> 4.46 -> 4.75 -> 4.03`) around $6.267$.

---

## 6. Theorem 5: $O(r^{-2})$ Run-Decay, $m$-Run Edgeworth Asymptotics, and Wiener–Hopf Limits

### 6.1. Exact $O(r^{-2})$ Run-Decay Prefactor via Sparre Andersen Universality (Resolved 2026-11-07 by Den B)
By **Sparre Andersen's (1953) fluctuation theorem**, a pure positive run `+`$^m$ starting from $\psi_0(x) = 1 - x$ has exact half-line survival probability $M_m(1-x) = \binom{2m}{m}4^{-m}$ for all $m \ge 1$, so its flip probability at step $m+1$ is identically
$$q_{\text{pure}}(m) = 1 - \frac{M_{m+1}(1-x)}{M_m(1-x)} = \mathbf{\frac{1}{2(m+1)}} = \frac{1}{2m} - \frac{1}{2m^2} + O(m^{-3}).$$
For an arbitrary entry profile $\psi(x)$ on $[0, 1]$ after a sign switch, the normalized survival mass expands in terms of the positive half-line harmonic function $V(x)$ ($\langle V, 1-x \rangle = 1$) and the first Wiener–Hopf correction functional $V_1(x)$ ($\langle V_1, 1-x \rangle = 0$, $\langle V_1, P_0^* \rangle = \langle V_1, P_1^* \rangle \approx -0.760599464113$) as $M_m(\psi) / \bigl(\binom{2m}{m}4^{-m}\bigr) = \langle V, \psi \rangle + \langle V_1, \psi \rangle m^{-1} + O(m^{-2})$. In the ratio $M_{m+1}(\psi)/M_m(\psi)$, the leading harmonic functional $\langle V, \psi \rangle$ cancels identically at orders $O(1)$ and $O(m^{-1})$, shifting all dependence on $\psi$ to order $O(m^{-2})$:
$$q_\psi(m) = \frac{1}{2(m+1)} + \frac{\mu_1(\psi)}{m^2} + O(m^{-3}), \qquad \mu_1(\psi) := \frac{\langle V_1, \psi \rangle}{\langle V, \psi \rangle}.$$
Consequently, for any two prefixes $\tau, \sigma$ such that $\tau\,\text{`+`}^r$ has terminal positive run length $m_\tau = r + a_\tau$ with entry profile $\psi_\tau$ and $\sigma\,\text{`+`}^r$ has $m_\sigma = r + a_\sigma$ with entry profile $\psi_\sigma$, the exact leading $O(r^{-2})$ prefactor is
$$\mathbb{P}(+ \mid \tau\,\text{`+`}^r) - \mathbb{P}(+ \mid \sigma\,\text{`+`}^r) = \frac{C(\tau, \sigma)}{r^2} + O(r^{-3}), \qquad \mathbf{C(\tau, \sigma) = \frac{a_\tau - a_\sigma}{2} + \mu_1(\psi_\sigma) - \mu_1(\psi_\tau)}.$$
For the benchmark pair $\tau = \text{`-+`}$ ($a_\tau = 1, \psi_\tau = T f_1, \mu_1 \approx +0.1244750302$) vs $\sigma = \text{`+-`}$ ($a_\sigma = 0, \psi_\sigma = T^2 f_1, \mu_1 \approx +0.1117838366$), this yields
$$C(\text{`-+`}, \text{`+-`}) = \underbrace{0.5000000000}_{\text{run-length shift }\Delta m=1\text{ (97.46\%)}} - \underbrace{0.0126911936}_{\text{boundary profile shift (-2.54\%)}} = \mathbf{0.4873088064}.$$

### 6.2. Exact 1st- and 2nd-Order Edgeworth Asymptotics for $m$-Run Summaries (Jee A & Den B)
For the $m$-run summary $S_m = (\text{sign}, r_1, \dots, r_m)$, summing over all $2^{L-1}$ prefixes of length $L = n - m$ before the terminal $m$ single-step turns `+-+-...` is equivalent to applying $T^m$ to the unconditional symmetric walk density $F_0^{(L)}(x) / F_0^{(L)}(0) = 1 - \frac{3x^2}{L} + \frac{\frac{9}{10}x^2 + \frac{9}{2}x^4}{L^2} + O(L^{-3})$ ($\sigma_L^2 = L/6$, excess kurtosis $\gamma_2 = -\frac{3}{5L}$). From the exact rational moments of $T^m\mathbf{1}$, we obtain:
1. **Exact Rational Limits $\hat{p}_\infty(-, 1^m) = \frac{\int_0^1 (T^{m+1}\mathbf{1})(x)\,dx}{\int_0^1 (T^m\mathbf{1})(x)\,dx}$ (Jee A):**
   $$\hat{p}_\infty(-, 1^m) = \mathbf{\frac{3}{10}},\; \mathbf{\frac{71}{252}},\; \mathbf{\frac{182}{639}},\; \mathbf{\frac{45\,541}{160\,160}},\; \mathbf{\frac{168\,388}{592\,033}},\; \mathbf{\frac{120\,686\,411}{424\,337\,760}} \longrightarrow \lambda_1 = \frac{1}{\kappa_1^2} \approx 0.284412871855.$$
2. **Exact 1st- and 2nd-Order Rational Edgeworth Expansions (Den B):**
   - **$m = 1$ `(sign, r=1)`:**
     $$\hat{p}_n(-, 1) = \mathbf{\frac{3}{10} - \frac{3}{175(n-1)} + \frac{2}{175(n-1)^2} + O\bigl((n-1)^{-3}\bigr)},$$
   - **$m = 2$ `(sign, r=1, r_prev=1)`:**
     $$\hat{p}_n(-, 1, 1) = \mathbf{\frac{71}{252} + \frac{65}{21\,168(n-2)} - \frac{8\,497}{4\,074\,840(n-2)^2} + O\bigl((n-2)^{-3}\bigr)},$$
   - **$m = 3$ `(sign, 1, 1, 1)`:**
     $$\hat{p}_n(-, 1, 1, 1) = \mathbf{\frac{182}{639} - \frac{5\,443}{11\,977\,416(n-3)} + \frac{197\,758\,621}{663\,309\,298\,080(n-3)^2} + O\bigl((n-3)^{-3}\bigr)}.$$

### 6.3. Wiener–Hopf Extremal Limits and Asymptotic Compression of $m$-Run Error
By evolving the discrete Wiener–Hopf half-line survival profile in the tridiagonal shifted-Legendre basis up to $m = 200$ ($D = 14$) with Neville–Richardson extrapolation:
1. **Upper Extremum (`'+'^{n-1} '-'`, single turn after a long run):** $P_{\max}(\infty) = P_1(\infty) = \mathbf{0.3151600752}$.
2. **Lower Extremum (`'-'^{n-2} '+-'`, double turn after a long run):** $P_{\min}(\infty) = P_2(\infty) = \mathbf{0.2793320208}$.
3. **Limiting Worst-Case Error of $S_1 = (\text{sign}, r)$:** Attained on `'-'^{n-2} '+-'`: $\frac{3}{10} - P_2(\infty) = \mathbf{0.0206679792}$ ($\approx 2.067\text{ pp}$).
4. **Limiting Worst-Case Error of $S_2 = (\text{sign}, r, r_{\text{prev}})$ (Jee A):** Because $\lambda_2 < 0$, $\hat{p}_\infty(-, 1, 1) = 71/252 \approx 0.28174603 < \lambda_1$, so the worst-case trajectory jumps to the 3-turn branch `'+'^{n-3}\text{'-+-'}$ ($P_3(\infty) \approx 0.28519033$), giving $\lim_{n\to\infty}\text{max\_err}_2 = P_3(\infty) - \frac{71}{252} \approx \mathbf{0.00344430}$, and $\lim_{n\to\infty}\text{max\_err}_m$ contracts by $\rho_{\text{turn}} = (\kappa_2/\kappa_1)^2 \approx \mathbf{6.26689303}$ per remembered run.

---

## 7. Open Questions ("To Reach Later / Добраться позже")

In accordance with our *Research in Progress* workflow, we track what was resolved in subsequent passes and what remains open:
1. **Closed-Form Wiener–Hopf Contour Integral for $P_{\max}(\infty)$, $P_{\min}(\infty)$, and $\langle V_1, P_0^* \rangle$:** Express the 10-digit Wiener–Hopf constants $P_{\max}(\infty) \approx 0.3151600752$, $P_{\min}(\infty) \approx 0.2793320208$, and $\langle V_1, P_0^* \rangle \approx -0.760599464113$ via explicit contour integrals of $\ln\bigl(1 - s\frac{4\sin^2(\xi/2)}{\xi^2}\bigr)$.
2. **[RESOLVED 2026-11-07 10:35 CET in §6.1 by Den B] Exact Leading Constant $C(\sigma, \tau)$ of the $O(r^{-2})$ Meander Decay:** Solved via Sparre Andersen cancellation $q_{\text{pure}}(m) = \frac{1}{2(m+1)}$ and first Wiener–Hopf functional $\mu_1(\psi)$, giving $C(\tau, \sigma) = \frac{a_\tau - a_\sigma}{2} + \mu_1(\psi_\sigma) - \mu_1(\psi_\tau)$ ($0.4873088064$ for `"-+"` vs `"+-"`).
3. **Asymptotic Spectrum of Mixed Turn/Repeat Words:** Characterize the Lyapunov exponents of random products of the turn operator $T = R\mathcal{I}^2$ and the repeat second-difference operator along ergonomic/Markovian sign regimes.

---

## 8. Coverage & Verification Matrix (Updated 2026-11-07 12:00 CET)

To maintain strict epistemic hygiene between general analytical proofs, finite-horizon executable checks in `verify_all_theorems.py`, and numerical extrapolations, the table below maps each claim of the working paper:

| Section / Claim | Analytical Proof Status | Executable Check in `verify_all_theorems.py` | Open / Extrapolated Component |
|---|---|---|---|
| **§2 (Theorem 1):** $\mathbb{P}(+ \mid +-) = 13/45$ vs $\mathbb{P}(+ \mid -+) = 32/45$ (`26` vs `64` in $S_6$) | **Exact for $n=2$ ($S_6$)** via MacMahon ribbon inclusion-exclusion $\binom{6}{2,1,3} - \binom{6}{2,4} - \binom{6}{3,3} + \binom{6}{6} = 26$ | `verify_macmahon_theorem_1()` (`Fraction` arithmetic, exact) | Closed-form generating function for arbitrary descent blocks |
| **§3 (Theorem 2):** Turn reset $(T f_0)(x) = \int_0^{1-x}(1-x-t)f_0(t)\,dt$ and repeat identity $(f_j^{\text{new}})'' = f_{j-1} - 2f_j + f_{j+1}$ | **Exact for all $n \ge 1$** by differentiation of the step convolution kernel $1 - |y|$ on unit intervals $[j, j+1]$ | `verify_alternating_operator_theorem_2()` (exact `Fraction` polynomials for $n=1\dots 6$, confirming $397\,023 / 12!$) | Multi-piece symbolic check in `compact_height.py` (tested exhaustively up to $n=8$) |
| **§4 (Theorem 3a):** Single-shot shifted Legendre projection $\Pi_D$ with $D = 2m$ has $\varepsilon = 0$ on $m$-step horizon for arbitrary $f_k$ | **Exact for all $m \ge 1, D \ge 2m$** via adjoint degree bound $\deg((\mathcal{L}^*)^{m-1} g_0) = 2m$ | `verify_legendre_horizon_theorem_3()` (`single_shot_exact_horizon_D_eq_2m` for $m=1,2,3$ on arbitrary degree-7 $f_k$, exact `0`) | — |
| **§4 (Theorem 3b — 2026-11-07 Addendum):** Streaming projection $\tilde{f}_s = \Pi_D \mathcal{L}\tilde{f}_{s-1}$ from $f_1(x)=1-x$ is exact ($\varepsilon = 0$) for $n \le D$, and at $n = D+1$ satisfies the exact unit-fraction identity $p_{D+1}^{\text{exact}} - p_{D+1}^{\text{stream}} = \bigl[2(2D+3)\binom{2D+2}{D+1}A_{D+1}\bigr]^{-1}$ ($\forall D \ge 1$) | **Exact for all $D \ge 1$** (`STREAMING_VS_SINGLE_20261107.md` Theorem 1.3 + Grok-face `Fraction` audit `1794045107` + Antigravity 11:25 `1794047232`) | `verify_legendre_horizon_theorem_3()` (`streaming_unit_fraction_identity_D_1_to_6`: exact `Fraction` check of $\varepsilon = 0$ for $n \le D$ and unit fractions $1/[2(2D+3)\binom{2D+2}{D+1}A_{D+1}]$ for $D=1\dots 6$) | Analytic upper bound on the infinite-horizon telescopic streaming sum for $n \to \infty$ |
| **§4 & §6.2–6.3 (m-Run Summary Cells):** At $n=8$ (`58` cells), `(sign, r, r_prev)` compresses $\max\_\text{err}$ by $6.21\times$ (`0.01738 -> 0.00280`); as $n \to \infty$, $\hat{p}_\infty(-, 1^m) = 3/10, 71/252, 182/639, \dots \to \lambda_1$ and $\lim_{n\to\infty}\text{max\_err}_m$ contracts by $\rho_{\text{turn}} \approx 6.2669$ per run | **Resolved 2026-11-07 10:30 CET by Jee A** (`m_turn_memory_asymptotics_2026_11_07.py`): exact rational limits $\int T^{m+1}\mathbf{1}/\int T^m\mathbf{1}$ and jump of worst-case branch to `'+'^{n-3}\text{'-+-'}$ at $m=2$ | `verify_edgeworth_asymptotics_theorem_5()` (`m_turn_rational_limits_m_1_to_6` exact `Fraction` check for $m=1\dots 6$) | — |
| **§5 (Theorem 4):** $T = R\mathcal{I}^2$ reduces to Euler–Bernoulli cantilever BVP $g^{(4)} = \kappa^4 g$, $\cosh\kappa\cos\kappa = -1$, $\lambda_m = (-1)^{m-1}/\kappa_m^2$, $\rho_{\text{turn}} = (\kappa_2/\kappa_1)^2 \approx 6.266893025771$ | **Exact spectral reduction** on $L^2([0, 1])$ via $g''(u) = \lambda^{-1}g(1-u)$ and self-adjointness of $K(x,t) = (1-x-t)_+$ | `verify_cantilever_spectrum_theorem_4()` (80-step bisection for $\kappa_{1,2,3}$ matched against exact rational power iteration to $< 10^{-9}$) | Lyapunov spectrum of mixed random products of $T$ and repeat operators (§7.3) |
| **§6.1 (Theorem 5a — $O(r^{-2})$ Prefactor):** $C(\tau, \sigma) = \frac{a_\tau - a_\sigma}{2} + \mu_1(\psi_\sigma) - \mu_1(\psi_\tau)$ ($0.4873088064$ for `"-+"` vs `"+-"`) | **Resolved 2026-11-07 10:35 CET by Den B** via Sparre Andersen $q_{\text{pure}}(m) = \frac{1}{2(m+1)}$ and cancellation of leading harmonic functional $\langle V, \psi \rangle$ | Verified in `meander_prefactor_and_edgeworth2_den_b.py` | Closed-form contour integral for $\langle V_1, P_0^* \rangle \approx -0.760599464113$ (§7.1) |
| **§6.2 (Theorem 5b — 1st & 2nd Order Edgeworth):** $\hat{p}_n(-, 1) = \frac{3}{10} - \frac{3}{175(n-1)} + \frac{2}{175(n-1)^2} + O((n-1)^{-3})$ (and exact rational $c_1^{(m)}, c_2^{(m)}$ for all $m$) | **Resolved 2026-11-07 10:35 CET by Den B** via 2nd-order Edgeworth expansion $1 - \frac{3x^2}{L} + \frac{\frac{9}{10}x^2 + \frac{9}{2}x^4}{L^2}$ | `verify_edgeworth_asymptotics_theorem_5()` (`edgeworth_1st_and_2nd_order_m_1_to_3` exact `Fraction` check) | — |
| **§6.3 (Theorem 5c — Wiener–Hopf Limits):** $P_{\max}(\infty) \approx 0.3151600752$, $P_{\min}(\infty) \approx 0.2793320208$, worst-case error limit $0.0206679792$ ($m=1$) and $0.00344430$ ($m=2$) | **Numerical extrapolation (10 digits)** via shifted-Legendre evolution up to $m=200$ ($D=14$) + Neville–Richardson extrapolation | Verified in `wiener_hopf_turn_limit_2026_11_06.py` and `m_turn_memory_asymptotics_2026_11_07.py` | **Closed-form Wiener–Hopf contour integral** for $P_{\max}(\infty), P_{\min}(\infty)$ (§7.1) |

---

## 9. Source Code, Workbench Artifacts, and GitHub ↔ Zenodo Release Route

### 9.1. Local Source Artifacts in OMPU
- **Unified Verification Script (0 external dependencies, checks Theorems 1–5):** `verify_all_theorems.py` (in this directory; independent verification receipts by Petrovich in `/Users/denbell/Documents/Codex/morning-20261107/research-check.json` and Grok-face `bus:1794045107_757426_70ba53`)
- **Initial Exploration & DP Engine (Petrovich / Codex):** `/Users/denbell/OMPU_Codex/reports/astra_exploration_2026-11-06/experiment.py`, `NOTE.txt`
- **Shifted Legendre Horizon $D = 2m$ & Streaming $n \le D$ (Petrovich / Antigravity & Grok):** `/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/compact_height_2026-11-06-antigravity-1620/compact_height.py`, `STREAMING_VS_SINGLE_20261107.md`
- **Turn-Reset & Convex Arc-Deficit (Petrovich / Anthropic):** `/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/turn_reset_2026-11-06-anthropic-2015/`
- **Euler–Bernoulli Cantilever Spectrum & $m$-Turn Memory Limits (Jee A / Lane A):** `/Users/denbell/OMPU_Jee/stereo_v1/a/lab/cantilever_turn_spectrum_2026_11_06.py`, `m_turn_memory_asymptotics_2026_11_07.py`
- **Edgeworth 1st/2nd Order, Sparre Andersen $O(r^{-2})$ Prefactor & Wiener–Hopf Limits (Den B / Lane B):** `/Users/denbell/OMPU_Jee/stereo_v1/b/lab/wiener_hopf_turn_limit_2026_11_06.py`, `/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06/meander_prefactor_and_edgeworth2_den_b.py`

### 9.2. Target GitHub Repository & Zenodo Release Route
- **Canonical Staging Directory:** `/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06/`
- **Target Public GitHub Mirror:** `/Users/denbell/OMPU_shared/petrovich_repos/public/` (`https://github.com/dennis972544999450-prog/OMPU_PETROVICH_public.git` / `github.com/ompu-eu`), path `research/permutation_walk_memory_2026-11-06/`, with `.zenodo.json` included at the package root for GitHub Release → Zenodo DOI archiving (`v0.1-wip`).
