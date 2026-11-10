# 3. Primer: the iteration matrix and the spectral radius

This section is the heart of the unit. A table of iterates shows *that* a
method converged; the theory below explains convergence and helps estimate
its eventual rate. The checks compare that estimate with a measured factor
on a specified test problem.

## The error obeys a linear recurrence

Let $x^*$ be the exact solution and $e^{(k)} = x^{(k)} - x^*$ the error. For
Jacobi, $x^* = D^{-1}(b + (L + U)x^*)$ also holds; subtracting it from the
iteration gives

$$
e^{(k+1)} = T\,e^{(k)}, \qquad T = D^{-1}(L + U),
\qquad\text{so}\qquad e^{(k)} = T^k e^{(0)}.
$$

$T$ is the **iteration matrix**. Every method in this unit has one (section 4).

## Convergence and the spectral radius

The **spectral radius** $\rho(T)$ is the largest absolute value of the
eigenvalues of $T$. The method converges for every starting vector **if and
only if** $\rho(T) < 1$.

The error norm need not decrease by exactly $\rho(T)$ at each sweep. If a
single dominant eigenmode is present in the initial error and eventually
dominates the other modes, its decay gives the approximation

$$
\lVert e^{(k+1)} \rVert \approx \rho(T)\,\lVert e^{(k)} \rVert.
$$

Transient behavior can last many sweeps, and competing modes can make the
stepwise ratios oscillate. The initial error can also miss the slowest mode:
for $T = \operatorname{diag}(0.9, 0.5)$ and $e^{(0)} = (0,1)^\top$, the error
decreases by $0.5$ at every sweep, although $\rho(T) = 0.9$.

When a factor near $\rho(T)$ describes the decay, an estimate for the sweeps
needed to reduce the error by a factor $\varepsilon$ (say $10^{-8}$) is

$$
k \approx \frac{\log \varepsilon}{\log \rho(T)}.
$$

This estimate ignores transient behavior and constant factors; it is not an
exact stopping count.

## Measuring the factor

From two sweep numbers $k_0 < k_1$, the **observed convergence factor** is

$$
f_{\text{obs}} = \left( \frac{\lVert e^{(k_1)} \rVert}{\lVert e^{(k_0)} \rVert} \right)^{1/(k_1 - k_0)} .
$$

Gate G3 measures it on the 1D Poisson problem L3 ($n = 20$) between sweeps 100
and 200, and compares it with $\rho(T)$ computed from the eigenvalues of $T$.
For the prescribed matrix, starting vector, sweep window and relaxation
factor, the reference implementations match to about six digits; the gate
allows 0.1%. This is a finite-window check on this problem, rather than a
claim about every error ratio for every matrix.

## The model problem

For L3 the eigenvalues are known exactly, and for Jacobi

$$
\rho(T_J) = \cos\frac{\pi}{n+1} \approx 1 - \frac{\pi^2}{2(n+1)^2}.
$$

For $n = 20$ this is 0.988831. Since $\log \rho \approx -\pi^2/(2(n+1)^2)$, the
number of sweeps grows like $n^2$: doubling $n$ multiplies the work by about
four. Check this in table R1 of your report.
