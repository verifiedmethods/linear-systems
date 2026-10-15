# 4. Gauss–Seidel and SOR

## Gauss–Seidel: use the newest values

When Jacobi's method computes $x_i^{(k+1)}$, the new values
$x_1^{(k+1)}, \dots, x_{i-1}^{(k+1)}$ are already known. **Gauss–Seidel** uses
them at once:

$$
x_i^{(k+1)} = \frac{1}{a_{ii}} \Big( b_i - \sum_{j < i} a_{ij} x_j^{(k+1)}
- \sum_{j > i} a_{ij} x_j^{(k)} \Big), \qquad i = 1, 2, \dots, n \text{ in order}.
$$

In matrix form $x^{(k+1)} = (D - L)^{-1}\big(b + U x^{(k)}\big)$, with iteration
matrix $T_{GS} = (D - L)^{-1} U$. The order of the rows now matters, so the
natural code is a loop over $i$ that updates a copy of $x$ in place:
start with `x_new = x.copy()`, and at row $i$ use `x_new` for the whole row
(its entries before $i$ are already new, those after $i$ still old).

## SOR: over-relax the Gauss–Seidel step

**Successive over-relaxation** moves further in the Gauss–Seidel direction,
by a factor $\omega$:

$$
x_i^{(k+1)} = (1 - \omega)\, x_i^{(k)} + \omega\, \tilde x_i,
$$

where $\tilde x_i$ is the Gauss–Seidel value for row $i$, computed with the
newest values. $\omega = 1$ gives Gauss–Seidel. The iteration matrix is

$$
T_\omega = (D - \omega L)^{-1}\big((1 - \omega) D + \omega U\big).
$$

Two classical results guide the choice of $\omega$: SOR can only converge for
$0 < \omega < 2$ (Kahan), and for a symmetric positive definite matrix it
converges for every $\omega$ in that range (Ostrowski and Reich).

## Your task

Write `gauss_seidel_sweep(A, b, x)` and `sor_sweep(A, b, x, omega)` in
`student/steps.py`, then run `python verify.py`. Points to watch (each is
caught by a gate):

- Gauss–Seidel must use the newest values; Jacobi must not.
- In SOR, relax towards the Gauss–Seidel value computed with the newest values,
  and use the *old* $x_i^{(k)}$ in the $(1 - \omega)$ term.
- Never change the input `x` (work on `x_new = x.copy()`), and never change
  `A` or `b`.
- Do not assume a particular size $n$.
