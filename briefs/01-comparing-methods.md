# Brief 1: Comparing Jacobi, Gauss–Seidel and SOR properly

## Question

How many sweeps does each method need on the model problem, how does that grow
with the size of the system, and how well does the theory predict it?

## What you must produce

1. **Predictions before experiments.** For the 1D Poisson problem with
   $n = 10, 20, 40, 80$, compute $\rho(T)$ for Jacobi, Gauss–Seidel and SOR with
   $\omega_{\text{opt}}$, from the formulas in tutorial section 5 and from
   `spectral_radius(iteration_matrix(...))`. Use $\log(10^{-8})/\log\rho(T)$
   to predict the sweeps needed to reduce the error norm by a factor of $10^{-8}$.
2. **Experiments.** Take the exact solution to be the vector of ones, set
   $b = A x^*$ and start from zero. Record the first sweep at which the relative
   error $\lVert x^{(k)} - x^* \rVert_2 / \lVert x^* \rVert_2$ is at most
   $10^{-8}$. The initial relative error is one. Present the predicted and
   measured counts in one table and explain the differences.
3. **Growth with $n$.** Plot sweeps against $n$ on log–log axes and measure the
   growth rates. Do they agree with $n^2$ and $n$?
4. **The choice of $\omega$.** For $n = 40$, use the same error target to find
   the best $\omega$ by experiment and compare it with $\omega_{\text{opt}}$.
   How many extra sweeps does a 5% error in $\omega$ cost, on each side of the
   theoretical optimum?
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

## Measuring the error target

`iterate` stops on the residual. To collect the error history, run with a
tighter residual tolerance and supply the known solution. For the sizes in
this brief, use a budget of 40,000 sweeps. With `A` set to your matrix and
`sweep` to the selected method (bind $\omega$ for SOR), use

```python
x_exact = np.ones(A.shape[0])
out = iterate(sweep, A, A @ x_exact, np.zeros_like(x_exact),
              tol=1e-12, maxit=40_000, x_exact=x_exact)
first = next((k for k, error in enumerate(out["error"]) if error <= 1e-8), None)
print("First sweep meeting the error target:", first)
print("Residual tolerance reached:", out["converged"])
```

If `first` is `None`, record that the error target was missed within the
observed sweeps. A false `converged` flag means the run ended before reaching
the residual tolerance. An earlier crossing of the error target can still be
read from the history. The automated report's R1 table measures a residual
target and therefore answers a different question.

## Your contribution

The predictions, the comparison with experiment, and the explanation of every
difference. Repeat items 1 to 3 for the 2D Poisson problem (`poisson2d(m)`,
$m = 5, 10, 20$ interior points in each direction). Find the spectral radii
numerically and plot the counts against $m$. For this square Poisson grid
the optimal SOR parameter uses the same formula as in one dimension, with
$m$ in place of $n$.

## Common pitfalls

- Comparing methods by seconds in Python rather than by sweeps (tutorial
  section 5).
- Reporting a single size: the growth with $n$ is the point.
