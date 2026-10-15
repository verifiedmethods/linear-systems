# 3. Primer: the iteration matrix and the spectral radius

This section is the heart of the unit. A table of iterates shows *that* a
method converged; the theory below says *how fast* it must converge, and the
checks compare the two.

## The error obeys a linear recurrence

Let $x^*$ be the exact solution and $e^{(k)} = x^{(k)} - x^*$ the error. For
Jacobi, $x^* = D^{-1}(b + (L + U)x^*)$ also holds; subtracting it from the
iteration gives

$$
e^{(k+1)} = T\,e^{(k)}, \qquad T = D^{-1}(L + U),
\qquad\text{so}\qquad e^{(k)} = T^k e^{(0)}.
$$

$T$ is the **iteration matrix**. Every method in this unit has one (section 4).

## The spectral radius decides everything

The **spectral radius** $\rho(T)$ is the largest absolute value of the
eigenvalues of $T$. Two facts follow from $e^{(k)} = T^k e^{(0)}$:

- the method converges for every starting vector **if and only if**
  $\rho(T) < 1$;
- after the first few sweeps, the error falls by a factor of about $\rho(T)$
  per sweep: $\lVert e^{(k+1)} \rVert \approx \rho(T)\,\lVert e^{(k)} \rVert$.

So the number of sweeps to reduce the error by a factor $\varepsilon$ (say
$10^{-8}$) is about

$$
k \approx \frac{\log \varepsilon}{\log \rho(T)}.
$$

## Measuring the factor

From two sweep numbers $k_0 < k_1$, the **observed convergence factor** is

$$
f_{\text{obs}} = \left( \frac{\lVert e^{(k_1)} \rVert}{\lVert e^{(k_0)} \rVert} \right)^{1/(k_1 - k_0)} .
$$

Gate G3 measures it on the 1D Poisson problem L3 ($n = 20$) between sweeps 100
and 200, and compares it with $\rho(T)$ computed from the eigenvalues of $T$.
A correct sweep matches to about six digits; the gate allows 0.1%.

## The model problem

For L3 the eigenvalues are known exactly, and for Jacobi

$$
\rho(T_J) = \cos\frac{\pi}{n+1} \approx 1 - \frac{\pi^2}{2(n+1)^2}.
$$

For $n = 20$ this is 0.988831. Since $\log \rho \approx -\pi^2/(2(n+1)^2)$, the
number of sweeps grows like $n^2$: doubling $n$ multiplies the work by about
four. Check this in table R1 of your report.
