# 5. Comparing the methods

## Work per sweep

One sweep of any of the three methods passes once over the matrix: about
$2n^2$ operations for a dense matrix, and about twice the number of nonzero
entries for a sparse one. So the methods can be compared by the **number of
sweeps**. (In plain Python, a Gauss–Seidel loop over the rows takes longer per
sweep than Jacobi written with whole-array operations; that is a property of
Python, not of the methods. Compare sweeps, not seconds.)

## The model problem

For the 1D Poisson problem L3 the theory is complete:

| Method | $\rho(T)$ | sweeps grow like |
|---|---|---|
| Jacobi | $\cos\frac{\pi}{n+1} \approx 1 - \frac{\pi^2}{2(n+1)^2}$ | $n^2$ |
| Gauss–Seidel | $\rho_J^2$ | $n^2$, but half as many as Jacobi |
| SOR, optimal $\omega$ | $\omega_{\text{opt}} - 1 \approx 1 - \frac{2\pi}{n+1}$ | $n$ |

with $\omega_{\text{opt}} = \dfrac{2}{1 + \sin\frac{\pi}{n+1}}$, which is
1.7406 for $n = 20$.

## Reading your report

- **Table R1:** sweeps for $n = 10, 20, 40$. Check the growth (about four
  times per doubling of $n$ for Jacobi and Gauss–Seidel, about twice for SOR),
  and compare with the prediction $\log(10^{-8})/\log \rho(T)$. Explain why the
  prediction is close but not exact.
- **Figure R2 and table R2:** sweeps against $\omega$. Find the best $\omega$
  and compare it with $\omega_{\text{opt}}$. How quickly does the work grow if
  $\omega$ is chosen badly?
- **Figure R3:** the residual against the sweep number. After the first sweeps,
  each curve should run parallel to its dashed line, which falls by $\rho(T)$
  per sweep.

## Direct or iterative?

For the small dense systems in this unit, `numpy.linalg.solve` is faster than
any of these methods. Iterative methods pay off for large sparse systems, where
elimination is far too expensive; brief 2 shows such a problem growing.
