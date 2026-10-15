# Brief 2: Steady temperature in a heated plate

## Background

A thin square plate (side 1) has its top edge held at a temperature that varies
along the edge, $100 \sin(\pi x)$ degrees, and its other three edges at 0. In
the steady state, the temperature $u(x, y)$ satisfies Laplace's equation
$u_{xx} + u_{yy} = 0$, and the exact solution is

$$
u(x, y) = 100\, \frac{\sin(\pi x)\, \sinh(\pi y)}{\sinh \pi}.
$$

On a grid with $m \times m$ interior points ($h = 1/(m+1)$), the five-point
approximation gives one equation per interior point: a linear system with
$m^2$ unknowns. This code builds it:

```python
import numpy as np
from vm.problems import poisson2d

def heated_plate(m):
    """Unknowns: the m x m interior temperatures, row by row (x fastest)."""
    h = 1.0 / (m + 1)
    xs = h * np.arange(1, m + 1)
    A = poisson2d(m)
    b = np.zeros(m * m)
    b[(m - 1) * m:] = 100.0 * np.sin(np.pi * xs)   # the top row touches the heated edge
    X, Y = np.meshgrid(xs, xs)
    exact = (100.0 * np.sin(np.pi * X) * np.sinh(np.pi * Y) / np.sinh(np.pi)).ravel()
    return A, b, exact
```

## Question

How fast do the iterations converge as the grid is refined, and when should
they stop?

## What you must produce

1. **Two errors.** For $m = 5, 10, 20$ (and 40 for SOR), compute the
   *discretisation error* (direct solution `np.linalg.solve(A, b)` against the
   exact solution) and show that it falls like $h^2$.
2. **Sweeps against grid size** for each method, to a relative residual of
   $10^{-8}$. How do the counts grow with $m$? Use $\rho(T)$ to explain.
3. **When to stop.** For each grid, find the residual tolerance at which the
   *iteration error* (iterate against direct solution) becomes smaller than the
   discretisation error. How many sweeps does stopping there save, compared with
   a tolerance of $10^{-8}$?
4. **Plot** the temperature on the finest grid you used (`plt.contourf`), and
   the error.
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

**Practical note:** Gauss–Seidel and SOR loop over rows in plain Python, so keep
Gauss–Seidel to $m \le 20$ (400 unknowns); SOR with a good $\omega$ handles
$m = 40$ in a few seconds.

## Your contribution

The separation of the two errors, the stopping rule in item 3 and the evidence
for it.
