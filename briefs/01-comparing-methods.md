# Brief 1: Comparing Jacobi, Gauss–Seidel and SOR properly

## Question

How many sweeps does each method need on the model problem, how does that grow
with the size of the system, and how well does the theory predict it?

## What you must produce

1. **Predictions before experiments.** For the 1D Poisson problem with
   $n = 10, 20, 40, 80$, compute $\rho(T)$ for Jacobi, Gauss–Seidel and SOR with
   $\omega_{\text{opt}}$, from the formulas in tutorial section 5 and from
   `spectral_radius(iteration_matrix(...))`. Predict the sweeps needed to reduce
   the error by $10^{-8}$.
2. **Experiments.** Run each method from $x = 0$ and record the sweeps actually
   needed. Present predictions and measurements in one table, and explain the
   differences.
3. **Growth with $n$.** Plot sweeps against $n$ on log–log axes and measure the
   growth rates. Do they agree with $n^2$ and $n$?
4. **The choice of $\omega$.** For $n = 40$, find the best $\omega$ by experiment
   and compare it with $\omega_{\text{opt}}$. How many extra sweeps does a 5%
   error in $\omega$ cost, on each side of the optimum?
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

## Your contribution

The predictions, the comparison with experiment, and the explanation of every
difference. Repeat items 1 to 3 for the 2D Poisson problem (`poisson2d(m)`,
$m = 5, 10, 20$), for which you must find the spectral radii numerically.

## Common pitfalls

- Comparing methods by seconds in Python rather than by sweeps (tutorial
  section 5).
- Reporting a single size: the growth with $n$ is the point.
