# Brief 3: When do iterative methods converge?

## Background

Tutorial section 6 gives two sufficient conditions (strict diagonal dominance;
symmetric positive definiteness) and two counterexamples, L5 and L6. The exact
condition is $\rho(T) < 1$.

## Question

How useful are the sufficient conditions in practice, and what does $\rho(T)$
add?

## What you must produce

1. **The family $A(a)$** with ones on the diagonal and $a$ everywhere else
   (3 × 3), for $a$ from $-0.6$ to $0.9$. For each $a$, decide whether $A(a)$ is
   diagonally dominant and whether it is positive definite, compute $\rho(T)$
   for Jacobi and Gauss–Seidel, and check by experiment whether each method
   converges. Plot $\rho(T)$ against $a$ for both methods.
2. **Explain with eigenvalues.** Show that the eigenvalues of $A(a)$ are
   $1 + 2a$ and $1 - a$, and derive the range of $a$ for which Jacobi converges.
3. **L6.** Show by hand that $T_J^3 = 0$ for L6, and explain what that means for
   Jacobi's iterates. Confirm that Gauss–Seidel diverges.
4. **Your own matrices.** Construct a 3 × 3 matrix for which Jacobi converges but
   which is neither diagonally dominant nor symmetric, and one for which both
   methods diverge. Explain each through $\rho(T)$.
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

## Your contribution

The derivations in items 2 and 3 and the matrices in item 4, with the evidence
for each claim.
