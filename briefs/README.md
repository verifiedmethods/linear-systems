# Project briefs for unit A2

Choose one brief with your supervisor after all three of your methods pass
their gates. Each brief lists what you must produce and what counts as your own
contribution.

| Brief | Question | Suits |
|---|---|---|
| [1](01-comparing-methods.md) | How many sweeps does each method need, and can the theory predict it? | Any final-year project in numerical analysis |
| [2](02-heated-plate.md) | How should a large system from a physical problem be solved, and when should the iteration stop? | Students interested in applications |
| [3](03-convergence-conditions.md) | When do iterative methods converge, and why? | Students who like linear algebra |

## Using the provided code in your own scripts

Write your scripts in the unit's main folder (next to `verify.py`):

```python
import numpy as np
from vm.problems import PROBLEMS, LinearProblem, poisson1d, poisson2d
from vm.iterate import iterate
from vm.study import iteration_matrix, spectral_radius, observed_factor
from student.steps import jacobi_sweep, gauss_seidel_sweep, sor_sweep

p = PROBLEMS["L3n20"]                       # or build your own system (below)
out = iterate(jacobi_sweep, p.A, p.b, np.zeros(p.n), tol=1e-8, x_exact=p.x_exact)
print(out["sweeps"], out["residual"][-1], out["error"][-1])

rho = spectral_radius(iteration_matrix(p.A, "jacobi"))   # "gauss_seidel" or "sor" (with omega=...)
sor = lambda A, b, x: sor_sweep(A, b, x, 1.5)            # SOR with a fixed omega, as a three-argument sweep
```

`iterate` returns the number of sweeps, the final `x`, and the histories of the
relative residual and (if you give `x_exact`) the relative error.

## Your own system

```python
A = np.array([[4.0, -1, 0], [-1, 4, -1], [0, -1, 4]])
x_exact = np.array([1.0, 2.0, 3.0])
mine = LinearProblem(id="M1", title="my system", A=A, x_exact=x_exact)   # mine.b is A @ x_exact
```
