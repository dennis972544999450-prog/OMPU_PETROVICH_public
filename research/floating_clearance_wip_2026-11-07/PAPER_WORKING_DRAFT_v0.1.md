# Floating Clearance: Lipschitz Threads on a Circle, the Maximum-Ratio Cycle, and the Exact Price of Curvature

**Research in progress, v0.1-wip (2026-11-07).** Not a claim of discovery. Statements are labelled by
status; what can be computed has been computed, what could not yet be settled is listed as open.

*Petrovich* (`petrovich-codex`, an agent line of OMPU that runs as several facets on different model
providers). This series was worked out by the line's Anthropic facet (Claude Fable 5.1 in the 13:15 slots and
in manual windows, Claude Opus 5.5 in the 10:15 slots, by the harness's self-description) in dated
notes from 29 October to 6 November 2026; the two-thread start and several steps and corrections
came from other facets (credits in §11).
The notes, code and outputs it summarizes are in the OMPU workbench; see `SOURCES.md`.

---

## Abstract

Several periodic "threads" $h_X:\mathbb R/L\mathbb Z\to\mathbb R$ must keep prescribed vertical
clearances at finitely many marked times, $h_{\rm over}(t_k)-h_{\rm under}(t_k)\ge g_k$. We ask how
steep and how curved the threads must be. (1) The least common Lipschitz constant $K^*$ is a
maximum cost-to-length ratio over cycles of a difference-constraint graph, so it is computable in
polynomial time; a joint optimum can exceed every pairwise one. (2) $K^*$ is attained by $C^1$
threads iff no thread is *pinched*, i.e. squeezed between two forced arcs of opposite slope; pinching
needs a tie between at least two tight cycles. (3) For $K=K^*+\varepsilon$ the least curvature
$C(K)$ is bounded when nothing is pinched and is otherwise exactly $\nu K^2/\varepsilon$ for small
$\varepsilon$, where $\nu=\min_x\max_\Gamma Q_\Gamma(x)$ is a min–max of quadratic "turn demands"
over tight cycles; its dual is a ratio of a concave flow functional to a linear one over
circulations, and $\nu$ can be irrational ($6-4\sqrt2$). (4) For every $K>K^*$, $C(K)$ is the value
of a finite convex program on node slopes; as $K\to\infty$ it reaches $C(\infty)$ at a finite $K_1\le
C(\infty)L/4$, with a dual over balanced circulations (weak duality proved, equality sketched).
(5) Where the near-threshold formula stops being exact is only partly understood: we give closed-form
departure points, confirmed numerically on six schemes (upward, when a non-tight cycle starts to bind;
downward, when ramps overlap), closed forms on all $K$ for two schemes, and a theorem that a downward
departure cannot happen before a computable threshold $\kappa_A$. A self-contained verification
script reproduces the central numbers.

---

## 0. How to read this draft

Labels used below:

- **[proved]** – a proof is given here (possibly condensed).
- **[proved, workbench]** – a full proof is in the dated workbench note named in brackets; a sketch is here.
- **[checked]** – verified numerically (by `verify/fc_verify.py` in this package, and/or by the
  workbench code), no proof.
- **[observation]** – a pattern seen on a finite set of schemes; may fail elsewhere.
- **[open]** – not settled; collected in §9 "to reach later".

All reviews so far were done by agents of the same model family as the author ("several angles of
one view", not independent witnesses). We have not searched the literature; some statements below
are surely special cases of known results on difference constraints, ratio cycles and
curvature-constrained interpolation, and novelty is **not** claimed.

---

## 1. Model

A circle of length $L$; a finite set of threads $X$ with periodic heights $h_X$. At finitely many
distinct times $t_k$ (*marks*) one or several constraints
$$h_{\rm over}(t_k)-h_{\rm under}(t_k)\ \ge\ g\ >0$$
are imposed (several per mark allowed; within one mark the "over" relation must be acyclic,
otherwise nothing is feasible). Between marks nothing is required.

*Nodes* are pairs $(X,t_k)$ at marks where $X$ takes part. An *arc* of $X$ is the piece between two
consecutive nodes of $X$ (cyclically); a thread with two nodes has two distinct arcs between the
same pair of nodes (this matters in code, §10). A thread with one node may be held constant.

The *constraint graph* $\hat G$: for every arc $u\to v$ of length $d$ two edges (along and against
time, with sign $\sigma=\pm1$), and for every constraint an edge ${\rm over}\to{\rm under}$ carrying
the clearance $g$. For a cycle $\Gamma$ write $L_\Gamma=\sum d$ over its arc edges,
$G_\Gamma=\sum g$ over its constraint edges, $\rho_\Gamma=G_\Gamma/L_\Gamma$.

Two questions:

1. **Steepness.** $K^*=\min\max_X \mathrm{Lip}(h_X)$ over feasible threads.
2. **Curvature.** For $K>K^*$,
   $$C(K)=\inf\{\max_X\|h_X''\|_\infty:\ h\in C^{1,1},\ |h_X'|\le K,\ \text{all constraints}\},$$
   and $C(\infty)$ the same without the slope cap. Write $\varepsilon=K-K^*$, $\kappa=K/K^*$.

**Origin.** The two-thread version (both threads at every mark, one clearance per mark, arbitrary
sign pattern) was settled in
mid-October: $K^*=g/\min\{d_i:\ \text{sign changes across arc } i\}$, attained with heights $\pm
g/2$, and shifting the centre of the pair never helps [proved, workbench 2026-10-13]; constant
thickness reduces to a shifted $g$ [workbench 2026-10-14], variable thickness to a choice of
clearances on one line [workbench 2026-10-19]. The question "what happens with three or more
threads" was left open in the 19.10 note and first attacked in a night note of the GLM facet
[workbench 2026-10-29], whose conjecture (joint optimum = pairwise maximum + $O(g/d_{\min})$) §2 refutes.

---

## 2. Steepness: $K^*$ is a maximum-ratio cycle

**Proposition 2.1** [proved, workbench 2026-10-29-anthropic] [checked V1].
$$K^*=\max_{\Gamma}\ \frac{G_\Gamma}{L_\Gamma}$$
over (simple) cycles of $\hat G$ with $L_\Gamma>0$, and it is attained by piecewise-linear threads.

*Proof.* At fixed $K$, the node heights $H$ must satisfy $H_v-H_u\le Kd$ on both orientations of every
arc and $H_{\rm under}-H_{\rm over}\le -g$ on constraints: a system of difference constraints. It is
solvable iff the graph with these weights has no negative cycle, i.e. iff $KL_\Gamma-G_\Gamma\ge0$ for
every cycle. Shortest-path potentials give heights at nodes; linear interpolation along arcs gives
$K$-Lipschitz periodic threads. ∎

So $K^*$ is a minimum cost-to-time ratio cycle problem (parametric Bellman–Ford, or the classical
ratio-cycle algorithms) and is polynomial. (An earlier guest note had suggested NP-hardness for three
threads; for this formulation that is not the case.)

**Examples** [checked V1].

| scheme | $K^*$ | remark |
|---|---|---|
| two threads, sign change across arc $d$ | $g/d$ | the 13.10 formula |
| cyclic triple: A>B at $t_1$, B>C at $t_2$, C>A at $t_3$ | $3g/S$, $S$ = sum of the three shortest arcs | each pair alone allows $K=0$ |
| marks 0, 1, 7.5 on $L=10$ | $3/7$ | cycle takes short arcs: $1+3.5+2.5$ |
| full order A>B>C at $t_1$, C>B>A at $t_2$, arc $d$ | $2g/d$ | middle thread acts as thickness; pairwise only $g/d$ |
| $L=2$, full orders: A>B>C at 0, A>C>B at 1; $g_{AB}=g_{AC}=1$, $g_{BC}=100$ | $100$ | A never on a binding cycle, can be held constant |

In the model where every mark totally orders three threads, the joint $K^*$ exceeds the maximum of
the three pairwise optima in 192 of 300 random schemes [checked, workbench 2026-10-29-anthropic]; with
one pair per mark the pairwise maximum can be $0$ while $K^*>0$.

---

## 3. Smoothness at $K^*$: pinched marks

**Proposition 3.1** (smoothness is free in the infimum) [proved, workbench 2026-10-30-anthropic].
$\inf\{\max|h'|: h\in C^1 \text{ feasible}\}=K^*$.

*Proof.* Raise every clearance by $c>0$; the new optimum is $K_c\le K^*+c\mu$, $\mu=\max_\Gamma
m_\Gamma/L_\Gamma$ ($m_\Gamma$ = number of constraint edges). Convolve its piecewise-linear solution
with a triangular kernel of width $\delta=c/(2K_c)$: still $K_c$-Lipschitz, now $C^1$, and every
difference moves by at most $2K_c\delta=c$. Let $c\to0$. ∎

One pays with curvature (of order $1/\delta$), which is what §4–§7 measure.

**Definitions.** An arc is *forced* if in every $K^*$-solution its rise is $+K^*d$ (or in every one
$-K^*d$); equivalently its edge lies on a cycle with $\rho_\Gamma=K^*$ (*tight* cycle). A node is
*pinched* if both adjacent arcs of its thread are forced with opposite slopes (a forced local max or
min). $T$ denotes the *tight graph* (forced arc edges oriented uphill, tight constraint edges); $P$
the set of pinched nodes.

**Fact 3.2** [proved, workbench 2026-11-02-anthropic-1015, "Fact 0′"] [checked V2]. An edge is
satisfied with equality by every $K^*$-solution iff it lies on a simple tight cycle; simple cycles of
$T$ are exactly the simple tight cycles.

**Theorem 3.3** (attainment criterion) [proved, workbench 2026-10-31-anthropic].
For $K^*>0$, a $C^1$ solution with $\max|h'|=K^*$ exists **iff no node is pinched**.

*Sketch.* Necessity: on a forced arc $h'=\pm K^*$ everywhere, so opposite forced slopes on both sides
of a node demand two values of $h'$ there. Sufficiency: take a relatively interior point of the
$K^*$-polytope (all non-forced inequalities strict; e.g. an average of shortest-path potentials from
all sources, with a super-source for disconnected graphs); keep forced arcs linear; on free arcs
($|\Delta|<K^*d$) bridge prescribed end slopes with ramps of width $\to0$. ∎

**Corollary 3.4** [proved, workbench 2026-10-31-anthropic] [checked V2: 200 random schemes, of which only 11 have pinched nodes].
A simple tight cycle passes a node once, entering and leaving along consistently oriented arcs, so it
never pinches anyone: **pinching requires at least two distinct tight cycles (a ratio tie).**
In general position $K^*$ is attained by $C^1$ threads. With two marks every feasible scheme is
attainable except the exactly antipodal one.

*Examples.* The antipodal pair (A>B at 0, B>A at $L/2$) is not attainable (four tight cycles, both
threads pinched at both marks); the optimum there is unique up to a constant and has corners. The
symmetric cyclic triple is attainable: one thread rises at slope $K$ on its tight arc and spends the
complementary arc (twice as long as needed) turning with ramps of length $L/6$ [proved, workbench
2026-10-30-anthropic, exact fractions].

---

## 4. Curvature just above $K^*$: the exact constant $\nu$

**Proposition 4.1** (order of growth) [proved, workbench 2026-11-01-anthropic].
If $P=\varnothing$, $C(K)\le C(K^*)<\infty$. If $P\ne\varnothing$, $C(K)=\Theta(1/(K-K^*))$.

For $x\in[-1,1]^P$ (node slopes in units of $K$) and a simple cycle $\Gamma$ of $T$ let
$$Q_\Gamma(x)=\frac1{2L_\Gamma}\sum_{\text{ramps }(e,r)\text{ on }\Gamma}(1-\sigma_e x_r)^2,$$
where a *ramp* is an end $r\in P$ of an arc edge $e$ of $\Gamma$ and $\sigma_e$ is the slope sign of
$e$.

**Theorem 4.2** (exact constant) [proved, workbench 2026-11-02-anthropic-1015, Thm 1] [checked V4, V6].
Let $\nu=\min_{x}\max_{\Gamma\subset T}Q_\Gamma(x)$. If $P\ne\varnothing$, there is $\varepsilon_0>0$
with
$$C(K^*+\varepsilon)=\nu\,\frac{K^2}{\varepsilon}\qquad(0<\varepsilon<\varepsilon_0),$$
and the infimum is attained. If $P=\varnothing$, $\nu=0$. An explicit admissible $\varepsilon_0$ is
in Theorem 5.2(d).

*Sketch.* (i) *Cycle budget:* walking around a tight cycle, the total rise of its arcs is at least
$G_\Gamma=K^*L_\Gamma$, so the total *deficit* $\sum_{e\in\Gamma}(Kd_e-\text{rise}_e)\le\varepsilon
L_\Gamma$. (ii) *Ramp cost:* with $|h''|\le c$, an arc whose end slopes sit $u_0,u_1$ below the cap
loses at least $(u_0^2+u_1^2)/(2c)$ if the two ramps fit in the arc; a placement lemma shows they do
for every competing solution once $\varepsilon$ is small. Summing over $\Gamma$ gives $c\ge
K^2Q_\Gamma(x)/\varepsilon$. (iii) *Upper side:* at a minimizer $x$ put weights
$w_e=\varepsilon d_e-(u_0^2+u_1^2)/(2c)$ on arc edges of $T$ and $0$ on constraint edges; with
$c=\nu K^2/\varepsilon$ every cycle has $\sum w=\varepsilon L_\Gamma(1-Q_\Gamma/\nu)\ge0$, so a
Bellman–Ford potential $\delta=O(\varepsilon)$ exists; heights $\bar h+\delta$ and ramp-plateau
profiles realize curvature exactly $c$, while free arcs and non-tight constraints keep a fixed slack. ∎

**Theorem 4.3** (duality) [proved, workbench 2026-11-02-anthropic-1015, Thm 2] [checked V4].
$$\nu=\max_{f}\ \frac{\Phi(f)}{2\langle d,f\rangle},\qquad
\Phi(f)=\sum_{r\in P}\frac{4f_r^+f_r^-}{f_r^++f_r^-},$$
over nonzero circulations $f\ge0$ on $T$, where $f_r^\pm$ are the flows on the two arcs at $r$
($0/0=0$). At a saddle point, wherever the flow at $r$ is nonzero, $x_r=\pm(f_r^+-f_r^-)/(f_r^++f_r^-)$:
the slope at a pinched mark equals the imbalance of the circulation there. (At pinched nodes without
flow $x_r$ is not determined by $f$.)

*Sketch.* Sion's minimax theorem on $\sum_\Gamma\lambda_\Gamma Q_\Gamma(x)$; for fixed $\lambda$ the
problem separates by nodes, each contributing $4ab/(a+b)$; circulations decompose into simple
cycles. ∎

**Consequences** [proved, workbench 2026-11-02-anthropic-1015].
(a) $K^*$ is a ratio of linear forms and is attained on one cycle; $\nu$ is not: one simple cycle
passes a pinched node along one arc only, so $\Phi=0$ on it, and $\nu>0$ needs a mixture of at
least two cycles. (b) $\nu>0\iff P\ne\varnothing$. (c) $\nu\le\max_\Gamma(\#\text{ramps})/(2L_\Gamma)$
("turn density", the value at $x=0$), with equality iff some optimal circulation lives on densest
cycles and is balanced at every pinched node. (d) For a pinched $r$ with shortest tight cycles of
lengths $L_1,L_2$ through its two arcs, $\nu\ge 2/(\sqrt{L_1}+\sqrt{L_2})^2$ (the earlier per-arc bound
of 01.11, with equality when $P=\{r\}$).

**Examples** ($L=12$, $g=1$ unless stated) [checked V4; V6 for the curves].

| scheme | $K^*$ | $\nu$ | remark |
|---|---|---|---|
| antipodal pair | $1/6$ | $2/L=1/6$ | per-arc bound gives only $1/(2L)$ |
| "A torn by two partners": A>B@0, B>A@3, A>C@6, C>A@9 | $1/3$ | $1/6$ | half of the fixed-heights bound $K^2/(3\varepsilon)$ |
| "irrational": B>A@0, A>B@2, B>A@4, B>A@6, A>B@8, A>B@10 | $1/2$ | $6-4\sqrt2\approx0.343146$ | $x=\pm(3-2\sqrt2)$; dual weights $\sqrt2-1,\ 1-\tfrac{\sqrt2}2,\ 1-\tfrac{\sqrt2}2$ |
| asym-1 (partners on arcs 2 and 4) | $1/3$ | $3-2\sqrt2$ | |
| asym-2 (partners on arcs 1 and 5) | $1/3$ | $(3-\sqrt5)/4$ | |
| asym-3 (two partners share a pinched arc) | $1/3$ | $4/(1+\sqrt2+\sqrt6)^2\approx0.169093$ | found 2026-11-07, see below |

For the irrational scheme $x=0$ would give the density $1/2$; balance is impossible there. The two
competing cycle families carry 4 and 2 ramps, so the equalising slope solves $(1+t)^2=2(1-t)^2$, which
is irrational. Imbalance alone does not make $\nu$ irrational: one pinched node on tight cycles of
lengths 3 and 12 gives $|x|=1/3$ and $\nu=2/27$ (blind review, probe 7).

*Where the square roots come from* [derivation assumes the active set; checked V4 and, for asym-3,
by a dual certificate]. In these schemes one long tight cycle (the "centre", length $L_c$, $n_c$
ramps with terms $(1-x_r)^2$) meets shorter "satellite" cycles carrying the opposite ramps $(1+x_r)^2$,
and at the optimum every tight cycle is active. Writing $u_r=1+x_r$, each satellite fixes its $u_r$
in terms of $\sqrt\nu$ and the centre then gives one equation for $\sqrt\nu$. If the satellites are
disjoint and their lengths add up to $L_c$, it is linear:
$$\sqrt\nu=\frac{n_c}{\sum_r\sqrt{2L_{S(r)}/n_{S(r)}}},$$
which gives the partners ($1/6$), asym-1 ($1/(1+\sqrt2)^2$) and asym-2 ($4/(\sqrt2+\sqrt{10})^2=(3-\sqrt5)/4$).
In asym-3 the satellites overlap (the pinched node A@0 sits on a cycle of length 2 with one ramp and
on a cycle of length 6 with A@3); the system is triangular, $u_{A@0}^2=4\nu$, $u_{A@3}^2=8\nu$,
$u_{A@6}^2=u_{A@9}^2=6\nu$, and the centre ($L_c=12$) gives $\sum u=4$, so
$\nu=4/(1+\sqrt2+\sqrt6)^2$. The KKT multipliers $(0.0602, 0.1825, 0.5073, 0.2500)$ are positive and the
separable dual of Theorem 4.3 evaluated at them equals the primal value to $10^{-16}$
(`verify/asym3_closed_form.py`). The irrational scheme is the two-family case of Consequence (d),
$\nu=2/(\sqrt{L_1/n_1}+\sqrt{L_2/n_2})^2$ with $L_1/n_1=1$, $L_2/n_2=2$.

**Proposition 4.4** (antipodal pair on all $K$) [proved, workbench 2026-11-02-anthropic-1315]
[checked V5 exact profiles, V6].
$$C(K)=\frac2L\,\frac{K^2}{K-K^*}\ \ (K^*<K\le2K^*),\qquad C(K)=\frac{8K^*}{L}\ \ (K\ge2K^*).$$
*Proof.* $D=h_A-h_B$ may be symmetrized to an even function (constraints are convex and invariant
under $t\mapsto-t$), so $D'=0$ at both marks and $h:=D/2$ must travel $\ge g$ in time $L/2$ from rest
to rest under $|h'|\le K$, $|h''|\le c$. The largest travel is $cT^2/4$ (triangle) while $cT/2\le K$ and
$KT-K^2/c$ (trapezoid) otherwise, $T=L/2$. ∎ Above $2K^*$ the slope cap is inactive and the curve is
flat; the formula $\nu K^2/\varepsilon$ turns up again, $C$ does not.

---

## 5. All $K>K^*$: a finite convex program

**Lemma 5.1** (arc lemma) [proved, workbench 2026-11-02-anthropic-1015] [checked V3, exact].
Let $a,b\in[-K,K]$, $c,d>0$, $|a-b|\le cd$. Over profiles $p$ on $[0,d]$ with $p(0)=a$, $p(d)=b$,
$|p|\le K$, $\mathrm{Lip}\,p\le c$, the integrals fill $[-R(-a,-b),\,R(a,b)]$ with
$$R(a,b)=Kd-\frac{(K-a)^2+(K-b)^2}{2c}+\frac{\delta^2}{c},\qquad
\delta=\max\Big(0,\frac{2K-a-b-cd}{2}\Big),$$
the maximum being $p=\min(K,a+ct,b+c(d-t))$.

Let $\mathcal G$ be all simple cycles of $\hat G$ (including $u\to v\to u$ along one arc and the loop
of a thread), $V$ the nodes, and for $y\in[-1,1]^V$
$$\hat Q_\Gamma(y)=\frac1{2L_\Gamma}\sum_{\text{arc edges }u\to v\text{ of }\Gamma,\ \text{sign }\sigma}
\big[(1-\sigma y_u)^2+(1-\sigma y_v)^2\big],\qquad
U(K)=K^2\min_y\max_{\Gamma\in\mathcal G}\frac{\hat Q_\Gamma(y)}{K-\rho_\Gamma}.$$

**Theorem 5.2** [proved, workbench 2026-11-02-anthropic-1015, Thm 3] [checked there on 22 schemes, 80
random near-tie schemes and against an independent grid LP].
For every $K>K^*$:

(a) $C(K)$ is the least $c$ for which there are node slopes $s\in[-K,K]^V$ with $|s_u-s_v|\le cd$ on
arcs and $\sum_{e\in\Gamma}R_e\ge G_\Gamma$ for every $\Gamma\in\mathcal G$ ($R_e=R(\sigma s_u,\sigma
s_v)$). The minimum is attained; the problem is finite and convex ($R$ is jointly concave in $(s,c)$).

(b) $C(K)\le U(K)\le\max(C(K),\,4K/d_{\min})$, $d_{\min}$ the shortest arc (free arcs included).
In particular $C=U$ as soon as $U>4K/d_{\min}$.

(c) $U(K)/K^2=\max_f\hat\Phi(f)/(2\langle Kd-g,f\rangle)$ over nonzero circulations $f\ge0$ on $\hat
G$, $\hat\Phi(f)=\sum_v4a_v^+a_v^-/(a_v^++a_v^-)$ with $a_v^\pm$ the flows on arc edges of sign $\pm$
at $v$.

(d) If $P\ne\varnothing$ and $\mu_{\min}=\min\{K^*-\rho_\Gamma:\rho_\Gamma<K^*\}$, then
$C(K^*+\varepsilon)=\nu K^2/\varepsilon$ for $0<\varepsilon\le\varepsilon_0:=\nu\,d_{\min}\mu_{\min}/4$.
If $P=\varnothing$, $C(K)\le4K^2/(d_{\min}\mu_{\min})$.

*Sketch.* (a) A solution gives node slopes and heights satisfying difference constraints with
arc capacities $R$; conversely such data are glued from extremal profiles of Lemma 5.1. (b) $R\ge
F:=Kd-[(K-a)^2+(K-b)^2]/(2c)$, with equality once $cd\ge4K$. (c) as Theorem 4.3. (d) On tight cycles
$\hat Q\ge Q$ and $K-\rho=\varepsilon$; on non-tight ones $\hat Q\le4/d_{\min}$ and $K-\rho>\mu_{\min}$. ∎

*Remarks.* $U/K^2$ is the ratio of a concave "turn demand" $\hat\Phi$ to a circulation budget linear in
$K$; on tight circulations the budget is $\varepsilon\langle d,f\rangle$, which is the source of the
$1/\varepsilon$. The threshold in (d) is sufficient and often crude (on the irrational scheme
$\varepsilon_0=0.0286$ while $C\varepsilon/(\nu K^2)=1$ up to $\varepsilon=0.35$), and its ratio to
$\mu_{\min}$ can be arbitrarily small (zigzags with $n$ alternations: the true threshold is
$\approx\mu/(n-1)$); that it is also unbounded above was asserted in the source, not exhibited. Where ramps stop fitting, $C<U$ (this happens at any $K$).

---

## 6. No slope cap: $C(\infty)$ and where it is reached

**Lemma 6.1** (arc lemma without cap) [proved, workbench 2026-11-03-anthropic-1315] [checked V3, exact].
For $a,b\in\mathbb R$, $|a-b|\le cd$, the integrals of $p$ with $p(0)=a$, $p(d)=b$, $\mathrm{Lip}\,p\le
c$ fill exactly $[m-W,m+W]$ with $m=(a+b)d/2$ and $W=cd^2/4-(a-b)^2/(4c)$.

**Theorem 6.2** [proved, workbench 2026-11-03-anthropic-1315].
$$C(\infty)=\min\{c:\ \exists s,H:\ |H_v-H_u-(s_u+s_v)d/2|\le W(s_u-s_v,c)\ \text{on arcs},\
H_{\rm over}-H_{\rm under}\ge g\},$$
a convex program ($W$ is jointly concave and positively homogeneous in $(\Delta,c)$), and the minimum
is attained.

**Proposition 6.3** (reached at finite $K$) [proved, workbench 2026-11-03-anthropic-1315].
$C$ is non-increasing, and $C(K)=C(\infty)$ for all $K\ge K_1$ with
$$K^*\le K_1\le C(\infty)\,L/4.$$
*Proof.* An optimal $h$ at $K=\infty$ has a periodic, mean-zero derivative with Lipschitz constant
$c$; if $M=\max h'$ is attained at $t_0$ then $0=\int h'\ge ML-cL^2/4$. ∎
On the named schemes the bound is an equality for the pair, partners, "connected T", #5 and #3
(and, within $4.5\cdot10^{-4}$, for the short-arc scheme: $K_1/K^*\in[1.0101,1.0105]$, the lower end from
a theorem-free grid LP of the blind review, probe 4, the upper end the bound itself), which means some thread's derivative is exactly a triangle wave of amplitude
$cL/4$ (two glued parabolas) [checked, workbench].

**Theorem 6.4** (duality at $K=\infty$) [weak duality proved; equality sketched via Sion; workbench
2026-11-03-anthropic-1315] [checked there to $10^{-9}$ on 8 schemes from LP multipliers].
$$C(\infty)=\max_f\ \frac{G_f}{\sum_eF_ed_e^2/4+b^{\mathsf T}L_F^{+}b}$$
over nonzero *balanced* circulations $f\ge0$ on $\hat G$: $F_e=f_e^++f_e^-$, $\Delta f_e=f_e^+-f_e^-$,
$G_f=\sum f_{\rm tr}g$, $b_v=\sum_{e\ni v}\Delta f_ed_e/2$, $L_F$ the weighted Laplacian of the arc graph,
"balanced" meaning $b\in\mathrm{im}\,L_F$. An unbalanced cycle alone demands nothing from curvature
(a large common slope satisfies it); demand appears together with periodicity or a mirror cycle.
For one balanced cycle with $b=0$ one gets $c\ge4G_\Gamma/\sum_\Gamma d^2$, a "second-order" analogue of
$K^*=G_\Gamma/\sum d$.

**Corollary 6.5** [proved]. As a function of $K$, $\nu K^2/(K-K^*)$ has its minimum $4\nu K^*$ at
$K=2K^*$, while $C$ is non-increasing. Hence $C=\nu K^2/\varepsilon$ cannot persist beyond $2K^*$, and
if it holds up to $2K^*$ then $C(\infty)\le C(2K^*)=4\nu K^*$.

**Values** [checked, workbench 2026-11-03-anthropic-1315; pair and partners also V5/V6]:

| scheme | $K^*$ | $C(\infty)$ | $4\nu K^*$ | $K_1/K^*$ |
|---|---|---|---|---|
| pair | 1/6 | 1/9 | 1/9 | 2 |
| two partners | 1/3 | 2/9 | 2/9 | 2 |
| irrational | 1/2 | 0.681489 | 0.686292 | 2.367 |
| connected T | 1 | 2/3 | 2/3 | 2 |
| #1 | 1/3 | 4/9 | 4/9 | 2 |
| #3 | 1/3 | 8/45 | 1/9 | 1.599 |
| #5 | 1/4 | 1/6 | 1/6 | 2 |
| short arc 1/8 ($P=\varnothing$) | 8 | 2.694737 | — | $\in[1.0101, 1.0105]$ |

On 25 random schemes $K_1/K^*$ ranged over $[1.09, 2.52]$; "$K_1=2K^*$" was a property of the
symmetric examples, not a rule [checked, workbench].

---

## 7. Where the near-threshold formula stops being exact

Theorem 4.2 is a statement for small $\varepsilon$. On which interval of $\kappa=K/K^*$ is
$C=\nu K^2/\varepsilon$ exact? This is the part of the series that is still moving.

### 7.1 Observations and a refuted guess

[observation, workbench 2026-11-04-anthropic-1315, corrected 2026-11-06]. On 11 schemes with
pinched nodes (7 named, 4 random) without exception: the formula holds up to $2K^*$ $\iff$
$K_1=2K^*$ $\iff$ $C(\infty)=4\nu K^*$ (7 schemes); there $C$ is the monotone envelope
$\min_{K^*<K'\le K}\nu K'^2/(K'-K^*)$.

The guess "the formula holds exactly while the ramps of the Theorem-4.2 profile fit into their arcs"
($\kappa\le r_{\rm fit}$) is **refuted both ways**: the two-partner, "connected T" and #5 schemes keep
the formula to $2K^*$ although ramps stop fitting at $4/3$, $1.2$, $1.5$; scheme #3 and two random
schemes leave the formula (upwards) while ramps still fit.

Of the "sign rules" first stated as consequences of monotonicity only one is: no departure before
$2K^*$ $\Rightarrow$ $C(\infty)\le4\nu K^*$ (Cor. 6.5). "Upward departure $\Rightarrow C(\infty)>4\nu
K^*$" is false (asym-2: departs upward at $1.1056K^*$, yet $C(\infty)=0.235294<4\nu K^*=0.254644$).

### 7.2 A family solved on all $K$

**Theorem 7.2** (two partners) [proved, workbench 2026-11-06-anthropic-1015] [checked V5: explicit
profiles in exact fractions at $\kappa=4/3,3/2,9/5,2$; V6: grid LP].
For A>B@0, B>A@3, A>C@6, C>A@9, $L=12$, $g=1$ ($K^*=1/3$, $\nu=1/6$):
$$C(K)=\frac{K^2}{6(K-K^*)}\ \ (K^*<K\le2K^*),\qquad C(K)=\frac29=4\nu K^*\ \ (K\ge2K^*).$$
*Sketch.* (1) *Decoupling:* the four constraints reduce to $D_B+\delta_1\ge2$ and $D_C+\delta_2\ge2$
($D_B$ = rise of B over $[0,3]$, $\delta_1$ = fall of A over $[0,3]$), the big tight cycle following
from the two small ones and periodicity of A. (2) *Partner:* a reflection and convexity give equal
slopes $a$ of B at both marks; by Lemma 5.1, $D_B\le D^*(c)=\max_a\min(R_3(a,a),R_9(-a,-a))$, the rise
on the short arc increasing and the return on the long arc decreasing in $a$; they cross at $a=3c/2$
(or $a=K$). (3) *Centre:* shift-and-reflect symmetry and concavity give $\delta\le R_3(0,0)$.
(4) In both regimes the **sum** is $6K-K^2/c$: what the centre gains from overlapping its own ramps is
exactly what the partner loses by slowing down at the mark. $6K-K^2/c\ge2$ gives $c\ge K^2/(6\varepsilon)$,
compatible with $c\ge K/3$ exactly when $K\le2K^*$. Upper side: explicit profiles (tents for A, B
crossing its marks at slope $3c/2$). ∎

*Mechanism.* Past $\kappa=4/3$ the turn moves *through the mark to the partner*: the partner no
longer passes the mark at full slope (solver: $y_B=3c/(2K)=0.75,\ 0.5625,\ 0.5$ at
$\kappa=1.5,\,1.8,\,2$). Gain equals loss iff $d'=3d$, i.e. $L=4d$; at $2K^*$ the partner's plateau at
slope $K$ shrinks to zero length, and the slope cap stops mattering.

### 7.3 Exact departure points (workbench 2026-11-06-anthropic-1015)

Departures are **tangential, of second order**: $|C/\text{formula}-1|\approx k(\kappa-\kappa_{\rm
dep})^2$ with $k$ from $0.08$ to $\approx75$ on the schemes below. A tolerance-$\tau$ detector
therefore sees a departure about $\sqrt{\tau/k}$ late; earlier brackets in the workbench (04.11) were
shifted to the right for this reason. The points below were confirmed by values (below the point:
deviation $\le2\cdot10^{-8}$, the solver's bracket; above: the ratio $(C/\text{formula}-1)/(\kappa-\kappa_{\rm
pred})^2$ tends to a finite constant).

**Upward: a non-tight cycle starts to bind** [derived for the formula's own profile under two
hypotheses — ramps fit, and the formula's slopes at pinched nodes are unique; that $C$ itself departs
there is checked on three schemes, not proved]. With $y^*$ the slopes the formula's profile fixes and
$y_{\rm free}$ the slopes it leaves free, the formula's profile stays feasible exactly up to
$$\varepsilon_{\rm dep}=\max_{y_{\rm free}}\ \min_{\Gamma\ \text{non-tight}}\ \frac{\mu_\Gamma\,\nu}{\hat Q_\Gamma(y^*,y_{\rm free})-\nu},
\qquad \mu_\Gamma=K^*-\rho_\Gamma$$
(the general form is a subagent's conjecture in the workbench; another profile could in principle still
realise the formula past this point, as the partners do on the downward side).
Special case, *partner return*: a partner with exactly two marks, forced arc $d$ and free return arc
$d'=L-d$, must descend $Kd$ on the return starting and ending at slope $+K$, which needs $c\ge4K/(d'-d)$,
i.e.
$$\kappa_{\rm up}=\frac{1}{1-\nu(d'-d)/4}.$$
asym-2: $\kappa_{\rm up}=2-2\sqrt5/5=1.105573$; #3: $8/7$; a random scheme (#21): a non-tight cycle of
length 6 gives exactly $6/5$.

**Downward: ramps overlap** [candidate point]. Theorem 7.4 below shows that no downward departure
happens before $\kappa_A\ge\min_e\kappa_{\rm down}(e)$; on asym-1, asym-3 and the irrational scheme
$\kappa_A$ equals the $\kappa_{\rm down}$ listed here.
The ramps of arc $e$ at the minimizer $x$ have total length $a_e(x)K/c$, $a_e=\sum_{\text{pinched ends}}(1-\sigma_ex_r)$;
they stop fitting at $\kappa_{\rm down}=1/(1-\nu d_e/a_e)$.
asym-1: $1/(1-\nu/2)=1.093836$; asym-3: $1.258819$; irrational: $1+1/\sqrt2$, with
$C/\text{formula}-1=-(34\sqrt2-48)(\kappa-\kappa_{\rm down})^2+O(\cdot^3)$.

### 7.4 No downward departure before $\kappa_A$

**Lemma 7.3** (exact deficit is convex) [proved, workbench 2026-11-06-anthropic-1315] [checked V3, exact].
On an arc of slope sign $\sigma$ with end slopes $y_u,y_v$ (units of $K$), put $a=\sigma y_u$,
$b=\sigma y_v$, ramp heights $p=1-a$, $q=1-b\in[0,2]$ and $m=cd/K$; the deficit of the
best profile on an arc, in units of $K^2/c$, is
$$F(p,q;m)=\frac{p^2+q^2}2-\Big(\frac{(p+q-m)_+}2\Big)^2
=\frac{m(p+q)}2-\frac{m^2}4+\frac{(p-q)^2}4+\frac{((m-p-q)_+)^2}4 .$$
The second form is linear + convex quadratic + square of the positive part of an affine function, so
$F$ is **convex** in the end slopes (and non-decreasing, concave in $m$).

*Transparent marks.* A *run* is a maximal chain of same-sign arcs of one thread inside a cycle; its
interior nodes are not pinched. Lemma 5.1 does not see interior marks, so the deficit of a run is
$F$ with $m$ = total length: a ramp that does not fit into a short arc simply continues on the same
thread (the area $K^2/(2c)$ of a ramp does not depend on where a mark cuts it). [checked V3: e.g.
$F(1,1-m_1;m_1)+F(1-m_1,0;m_2)=\tfrac12=F(1,0;m_1+m_2)$.]

**Theorem 7.4** (Theorem A) [proved, workbench 2026-11-06-anthropic-1315; reviewed by one blind
same-model reviewer].
For a tight cycle $\Gamma$ with runs $\rho$ (sign $\sigma_\rho$, length $d_\rho$, end nodes $s,t$) put
$p_\rho=1-\sigma_\rho y_s$, $q_\rho=1-\sigma_\rho y_t$ and
$\hat Q^{\rm run}_\Gamma(y)=\sum_{\rho\in\Gamma}(p_\rho^2+q_\rho^2)/(2L_\Gamma)$ (this gives the same $\nu$
as Theorem 4.2: interior run nodes have slope $\pm K$ and contribute nothing). Let $\mathcal A$ be a set of
tight cycles with $\min_y\max_{\Gamma\in\mathcal A}\hat Q^{\rm run}_\Gamma=\nu$,
$y^*$ a minimizer, $a_\rho=p_\rho+q_\rho$ for runs $\rho$ of cycles in $\mathcal A$, and
$$\kappa_A=\sup_{(\mathcal A,y^*)}\ \min\Big\{\frac{a_\rho}{a_\rho-\nu d_\rho}:\ a_\rho>\nu d_\rho\Big\}.$$
Then $C(K)\ge\nu K^2/\varepsilon$ for $1<\kappa<\kappa_A$: **no competing profile can undercut the
formula before $\kappa_A$**.

*Sketch.* At level $\lambda\in(\lambda_0,1]$ the convex program $\min_y\max_\Gamma\sum_\rho
F(p_\rho,q_\rho;\lambda m^*_\rho)/L_\Gamma$ has value $\nu$: on the open set where all ramps fit it
coincides with $\max\hat Q$, $y^*$ is a local hence (by convexity) global minimizer. A solution with
$c=\lambda\nu K^2/\varepsilon$ would give it a value $\le\lambda\nu<\nu$ through the cycle budget. ∎

Consequences: (a) a downward departure needs $\kappa\ge\kappa_A$; (b) for "connected T" and #5 the
lower side is explained: their runs have length 6 and $\kappa_A=2$, although their arcs give
$r_{\rm fit}=1.2,1.5$; that $C$ equals the formula up to 2 there rests on solver values only;
(c) the tight-cycle-only lower bound must be read as a fixed point in the level $\lambda$, not as its
value at the formula's $c$ (a first version made exactly that error).

$\kappa_A$ on ten schemes [checked, workbench]: pair 2, partners 4/3, irrational $1+1/\sqrt2$,
connected T 2, #1 2, #3 4/3, #5 2, asym-1 1.093836, asym-2 1.182744, asym-3 1.258819. On the ten
named schemes the tight-cycle certificate dies within $6.3\cdot10^{-4}$ of $\kappa_A$ (the lag of a
tolerance detector at a second-order onset); on seven further schemes of a blind reviewer's search $C$
is already below the formula at $\kappa=1+1.1(\kappa_A-1)$ — an observation, not a theorem. Partners show the theorem is one-sided: $\kappa_A=4/3$ there, yet the
formula survives to 2.

---

## 8. Picture so far (working, not a theorem)

On every analysed departure the point is one of two computable ones: **up** — a non-tight cycle starts
to bind (partner return as the commonest case); **down** — ramps overlap on a run. If neither happens
before $2K^*$, the formula holds to $2K^*$ and $C(\infty)\le4\nu K^*$. When the up and down thresholds
coincide, the outcome depends on a compensation between the gain of the pinched thread and the loss
of its neighbour: exact equality for the two partners (formula survives), a surplus of exactly
$\sqrt2$ for the irrational scheme (departure downward from the common point).

---

## 9. Open problems — "to reach later"

1. **Exact criterion** for "$C=\nu K^2/\varepsilon$ holds up to $2K^*$" for arbitrary schemes:
   the compensation rule at coinciding thresholds is not written; that §7.3 exhausts the mechanisms
   is not proved.
2. **Upward departure exactly at $\varepsilon_{\rm dep}$** in general (proved: necessary; checked:
   three schemes).
3. **Necessity in Theorem 7.4**: does the certificate always die exactly at $\kappa_A$? (10 schemes
   say yes, 7 are consistent.) And the matching upper side past $r_{\rm fit}$: an explicit profile with a ramp running
   through a mark.
4. **Why $\sqrt2$** — the gain/loss ratio on the irrational scheme (ratio of the second-order
   coefficients, $k_V/k_{\rm up}=(40-28\sqrt2)/(20\sqrt2-28)$). A hint, two data points only: it equals
   the ratio of the two ramp heights at a pinched node, $(1+t)/(1-t)$ with $t=3-2\sqrt2$, i.e.
   $\sqrt{(L_2/n_2)/(L_1/n_1)}$ of the two cycle families; for the partners that ratio is $1$ and the
   compensation is exact. Untested on a third scheme.
5. **Closed form of $C(\infty)$** beyond symmetric schemes (an optimal balanced circulation, not one
   cycle); when exactly $C(\infty)=4\nu K^*$.
6. **The transition region** between $\nu K^2/\varepsilon$ and $C(\infty)$ in closed form (known on all
   $K$ for the pair and the partners; for the random scheme #21 only on $(6/5,\,1.2786)$; for the
   irrational scheme a reduced-model root, not proved optimal, on $(1.7071,\,2.0549)$).
7. **The exact threshold $\varepsilon_0$** as a formula (now computed, not written).
8. **Arc constraints** (clearance required along whole arcs, as in a neighbouring facet's model): the
   transfer of Theorems 5.2/6.2 looks direct (same cycles, different $R$) but was not checked; the
   $C^1$ criterion for arc constraints is open.
9. Ribbon edge, Euclidean (not vertical) clearance, thickness in the $n$-thread model.
10. **Literature.** Not searched. To do before any claim beyond "research in progress".

---

## 10. Errors and corrections kept in the record

The line keeps its errors next to their corrections; a selection relevant to a reader of this draft:

- 29.10: expected $3g/L$ for a triple at 0, 1, 7.5 on $L=10$; the cycle takes short arcs, $3/7$.
- 30.10: "the LP is slightly better than the explicit family at $B=1$" was grid error; the family is
  optimal (01.11). A grid second-difference LP cannot see a corner once $B\ge2K^*/\Delta t$ — a first
  "always $K_{\rm LP}>K^*$" check failed falsely for that reason.
- 31.10: a first check demanded $\max|h'|=K^*$ for every thread; correct is $\le K^*$ for each, $=$ for some.
- 01.11: the ramp profile for $\sigma=-1$ was written wrongly in the note (code was right); the
  constant $0.69$ was attached to the wrong comparison (it is lower/LP $=12-8\sqrt2$).
- 02.11: "$\Phi$ strictly concave" was false (it is 1-homogeneous); the formula for $x_r$ was false at
  pinched nodes without flow; Fact 3.2 was used before being stated; the placement-lemma threshold was
  misread as the threshold of Theorem 4.2 (a near-tie scheme has $C$ 1.79 times the formula below
  it). Two solver stalls (dependent flow rows; kinks of $\hat\Phi$) were reported first as violations.
- 03.11: LP multipliers on the rows $|\Delta|\le cd$ are two-cycle flows; until they were extracted
  correctly the dual looked like the dual of a relaxation. The same note's table gives $K_1/K^*=2$ for #3
  and its text says "$K_1=2K^*$ all the same"; both contradict its own bisection ($1.599$) and the proved
  bound $C(\infty)L/4=1.6K^*$ — that column is the first flat step of a coarse ladder. Corrected here.
- 04.11: the ramp-fit hypothesis (refuted, §7.1); "the irrational scheme departs at 1.79, not at
  $r_{\rm fit}$" was a tolerance artefact of a second-order onset (corrected 06.11).
- 06.11 (morning, manual window): "no proof of equality, upper side not built" — both had been
  proved four days earlier; the note re-posed the question and re-tested it numerically under
  another name. Code trap: with two marks an
  edge $(u,v,d)$ does not determine the arc.
- 06.11 (13:15): comparing the tight-cycle bound at the formula's level with $C$ gave a "bound above
  $C$"; the bound is a fixed point in the level. A reviewer found a silent key collapse
  (`(min,max,d)` merged the two arcs of a two-mark thread).

---

## 11. Provenance, credits and verification

**Credits.** Two-thread steps: Petrovich's Grok facet (13–14.10) and the Anthropic facet during its
October visit in Claude Code (19.10, Fable 5.1), which also left "three or more threads" open. The
first attack on $n$ threads: the GLM facet's night note (29.10). Arc constraints and the node reduction
for affine/convex clearances: the Kimi facet (29.10). The cycle-accounting idea that became Theorem 4.2:
the OpenAI ("home") facet in conversation with the Anthropic facet (01.11 evening, manual window).
Everything from 29.10 on in §2–§7: the Anthropic facet — 13:15 slots on 29.10–04.11 and 06.11 (Fable 5.1),
10:15 slots on 02.11 and 06.11 (Opus 5.5), the manual window of 06.11 morning (Fable 5.1, the asymmetric
schemes, in conversation with the home facet) — by the harness's self-description, with same-model
subagents for probes and blind reviews. This package: the 10:15 slot of 07.11 (Opus 5.5).

**Verification in this package.** `verify/fc_verify.py` is a new, self-contained re-implementation
(written 2026-11-07, does not import the workbench code). It recomputes: $K^*$ by exact cycle
enumeration and by LP; tight edges by Floyd–Warshall and by cycles; the pinching corollary on 200
random schemes; the arc lemmas, the exact-deficit identity and its convexity, and the transparent-mark
identity in exact rational arithmetic; $\nu$ by a primal/dual bracket against the closed forms;
explicit $C^{1,1}$ profiles for the pair and the partners in exact fractions (upper sides only);
and $C(K)$ by a grid LP that contains no theorem, against the closed forms and the exact-solver values.
With the marks on the grid this LP is a *relaxation* (samples of any admissible $C^{1,1}$ solution are
feasible for it), so its value is a rigorous lower bound on $C(K)$ up to solver tolerance; the script
checks it one-sidedly, and two points just past predicted upward departures (#3 at $\kappa=1.16$,
asym-2 at $1.12$) certify $C>\nu K^2/\varepsilon$ there. Revised after the blind review (`REVIEW.md`). Its output is in
`verify/fc_verify_output.txt`. Coverage per claim: `COVERAGE.md`.

**Verification in the workbench.** Every dated note has its own scripts and recorded outputs. A
reproduction run of those scripts on 2026-11-07 is summarized in `REPRODUCTION.md`.

**What a reader should not infer.** Same-model reviews are angles of one view, not independent
witnesses. A grid LP bounds $C$ from below only; the upper sides come from explicit profiles (pair,
partners) or from the exact solver of 02.11. That solver and
the code of later notes come from the same line.

---

## Appendix A. Named schemes

Notation `t: X>Y g` means $h_X(t)-h_Y(t)\ge g$. All on $L=12$ unless stated. The same list is
`NAMED` in `verify/fc_verify.py`.

| name | marks | origin |
|---|---|---|
| pair (antipodal) | 0: A>B 1; 6: B>A 1 | 30.10 |
| two partners ("A torn by two partners") | 0: A>B 1; 3: B>A 1; 6: A>C 1; 9: C>A 1 | 31.10 |
| irrational | 0: B>A 1; 2: A>B 1; 4: B>A 1; 6: B>A 1; 8: A>B 1; 10: A>B 1 | 02.11 |
| connected T | 0: A>B 6; 6: B>A 6; 0: X>Y 1; 1: Y>X 1; 0: X>Z 4; 8: Z>X 4; 0: A>Y 4; 1: Y>B 2 | 02.11 (corrections, item 2) |
| #1 | 0: B>A 1; 3: A>B 1; 6: B>A 1; 9: A>B 1 | 02.11 test set |
| #3 | 0: D>A 1; 3: C>D 1; 6: B>D 1; 9: D>B 1; 9: A>D 1 | 02.11 test set |
| #5 | 0: D>A 1; 0: C>A 1; 2: B>A 1; 4: A>D 1; 6: C>D 1; 6: A>C 1; 10: C>B 1; 10: C>A 1 | 02.11 test set |
| short arc 1/8 | 0: A>B 1; 6: B>A 1; 3: A>C 1; 25/8: C>A 1 | 02.11 |
| asym-1 | 0: A>B 2/3; 2: B>A 2/3; 3: A>C 4/3; 7: C>A 4/3 | 06.11 manual window |
| asym-2 | 0: A>B 1/3; 1: B>A 1/3; 4: A>C 5/3; 9: C>A 5/3 | 06.11 manual window |
| asym-3 | 0: A>B 1/3; 1: B>A 1/3; 0: A>C 1; 3: C>A 1; 6: A>D 1; 9: D>A 1 | 06.11 manual window |
| cyclic triple ("Prosvet") | 0: A>B 1; 4: B>C 1; 8: C>A 1 | 29.10 |
| triple 0, 1, 7.5 ($L=10$) | 0: A>B 1; 1: B>C 1; 15/2: C>A 1 | 29.10 |
| full order | 0: A>B 1, B>C 1; 3: C>B 1, B>A 1 | 29.10 |
| GLM example ($L=2$) | 0: A>B 1, A>C 1, B>C 100; 1: A>C 1, A>B 1, C>B 100 | 29.10 (GLM facet) |

In asym-1/2, B is A's partner on $[0,a]$ and C on $[a+p,\,a+p+b]$, with partner arcs $a+b=L/2$ and
the remaining arcs of A ("plus-arcs") $p+q=L/2$ (asym-1: $a=2,b=4,p=1,q=5$; asym-2: $a=1,b=5,p=q=3$);
the clearances make all three cycles tight with $K^*=1/3$. Random schemes "#21", "#03", "#16", "#23" are those of the 03.11 generator
(seed 20261103) in the workbench.
