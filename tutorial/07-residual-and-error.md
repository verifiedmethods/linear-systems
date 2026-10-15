# 7. Residual, error and when to stop

## You cannot see the error

In practice the exact solution is unknown, so the error
$e = x^{(k)} - x^*$ cannot be computed. What can be computed is the
**residual**

$$
r = b - A x^{(k)} = -A e .
$$

The provided code stops when the relative residual $\lVert r \rVert / \lVert b \rVert$
falls below a tolerance (for example $10^{-8}$).

## A small residual does not mean a small error

From $e = -A^{-1} r$ it follows that

$$
\frac{\lVert e \rVert}{\lVert x^* \rVert} \le \kappa(A)\,\frac{\lVert r \rVert}{\lVert b \rVert},
\qquad \kappa(A) = \lVert A \rVert\,\lVert A^{-1} \rVert ,
$$

where $\kappa(A)$ is the **condition number**. For the 1D Poisson problem it
grows like $n^2$: about 681 for $n = 40$. So a relative residual of $10^{-8}$
only guarantees a relative error below about $7 \times 10^{-6}$. Result R5 in
your report shows the actual numbers for your methods.

## Choosing the tolerance

Stop when the iteration error is small compared with the other errors in your
problem, not "as small as possible". When the system comes from a
discretised differential equation, the grid itself causes a *discretisation
error*; iterating far beyond it wastes work. Brief 2 explores this.

## Using AI tools

You may use AI tools to understand the methods or to find a bug, if you say so
in `student_info.txt`. Write the three sweep functions yourself; if any part of
your code came from an AI tool or another person, say so in your disclosure and
in `CONTRIBUTION.md`. Your analysis and write-up must be your own, and you must
be able to explain every line of your code in your viva.
