# 2. Jacobi's method

## Derivation

Row $i$ of $Ax = b$ reads $\sum_j a_{ij} x_j = b_i$. Solve it for $x_i$:

$$
x_i = \frac{1}{a_{ii}} \Big( b_i - \sum_{j \ne i} a_{ij} x_j \Big).
$$

**Jacobi's method** uses this formula for every row at once, with the *old*
values on the right-hand side:

$$
x_i^{(k+1)} = \frac{1}{a_{ii}} \Big( b_i - \sum_{j \ne i} a_{ij} x_j^{(k)} \Big),
\qquad i = 1, \dots, n.
$$

In matrix form, with the splitting of section 1,

$$
x^{(k+1)} = D^{-1}\big(b + (L + U)\,x^{(k)}\big).
$$

Because every new component uses only old values, the components can be
computed in any order, or all at once with whole-array NumPy operations.

## Your task

Open `student/steps.py` and write `jacobi_sweep(A, b, x)`. It must:

1. compute every new component from the **old** vector `x`;
2. return the new iterate as a **new** array, without changing `A`, `b` or `x`.

You may use a loop over the rows, or whole-array operations (`A @ x` and
`np.diag(A)` are useful). Then run `python verify.py`. If your sweep is correct
you will see `Jacobi 4/4 gates passed` and an observed factor of about 0.9888.

## If a gate fails

The most common Jacobi mistake is to update `x` while looping over the rows:
then later rows use new values, and the method is no longer Jacobi's. Build the
new values in a separate array.
