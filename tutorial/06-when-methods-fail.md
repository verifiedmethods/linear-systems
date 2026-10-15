# 6. When the methods fail

## Sufficient conditions

Two classical results guarantee convergence:

- If $A$ is **strictly diagonally dominant** ($|a_{ii}| > \sum_{j \ne i} |a_{ij}|$
  in every row), Jacobi and Gauss–Seidel both converge.
- If $A$ is **symmetric positive definite**, Gauss–Seidel converges, and so does
  SOR for every $0 < \omega < 2$.

These conditions are *sufficient*, not necessary: a method can converge when
they fail, and Jacobi can fail even when $A$ is symmetric positive definite.
The only exact test is $\rho(T) < 1$.

## Two warning examples

**L5** has ones on the diagonal and 0.6 everywhere else. It is symmetric
positive definite (its eigenvalues are 2.2, 0.4 and 0.4) but not diagonally
dominant. Gauss–Seidel converges; Jacobi diverges, because
$T_J = I - A$ has eigenvalue $-1.2$, so $\rho(T_J) = 1.2$.

**L6** has rows $(1, 2, -2)$, $(1, 1, 1)$, $(2, 2, 1)$. Jacobi's iteration
matrix is nilpotent ($T_J^3 = 0$), so Jacobi reaches the exact solution in
three sweeps; Gauss–Seidel has $\rho(T_{GS}) = 2$ and diverges. So Gauss–Seidel
is *not* always better than Jacobi.

Result R4 in your report shows both cases for each of your methods.

## For your write-up

For any new system, compute $\rho(T)$ (the provided `vm.study` module does it:
see the briefs) before trusting an iteration, and say which sufficient
condition, if any, applies.
