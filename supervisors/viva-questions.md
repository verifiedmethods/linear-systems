# Viva questions for unit A2

Choose three or four. Ask the student to answer with their own code and report
in front of them.

## About the code

1. Show me where your Gauss–Seidel sweep uses the newest values, and where
   Jacobi deliberately does not.
2. Why does your sweep work on a copy of `x`? What would go wrong if it changed
   `x` itself?
3. In your SOR sweep, which value of $x_i$ appears in the $(1 - \omega)$ term,
   and why?
4. What does your SOR sweep do when $\omega = 1$? Show it.

## About the results

5. Gate G3 compares your observed factor with $\rho(T)$. Why should the error
   fall by $\rho(T)$ per sweep, and why only after the first few sweeps?
6. Why does Gauss–Seidel need about half as many sweeps as Jacobi on the 1D
   Poisson problem? Is Gauss–Seidel always better? (Point to L6.)
7. Why do Jacobi's sweeps grow about four times when $n$ doubles, but SOR's only
   about twice?
8. L5 is symmetric positive definite. Why does Jacobi still diverge on it?
9. Your relative residual is $10^{-8}$. What can you say about the error, and
   why?
10. When would you use `numpy.linalg.solve` instead of these methods?

## About the project

11. What does your project add beyond the unit's provided systems?
12. How did you choose your stopping tolerance, and what evidence supports it?
