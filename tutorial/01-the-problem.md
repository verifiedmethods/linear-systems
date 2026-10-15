# 1. Linear systems: direct and iterative methods

A linear system $Ax = b$ has an $n \times n$ matrix $A$, a right-hand side $b$
and an unknown vector $x$. Linear systems are everywhere: currents in an
electrical network, forces in a structure, and above all the large systems
that appear when a differential equation is discretised (for example the
temperature at every point of a grid).

## Direct methods

Gaussian elimination (or an LU factorisation) solves $Ax = b$ in a fixed number
of steps, about $\tfrac23 n^3$ arithmetic operations for a dense matrix. For
$n = 1000$ that is under a second on a laptop, so for small and moderate
dense systems a direct method is usually the right choice.

## Iterative methods

For the systems that come from differential equations, $n$ can be in the
millions, and almost every entry of $A$ is zero (the matrix is *sparse*).
Elimination then fills in many of the zeros and becomes far too expensive.
An **iterative method** starts from a guess $x^{(0)}$ and improves it, one
**sweep** at a time:

$$
x^{(0)} \to x^{(1)} \to x^{(2)} \to \cdots \to x,
$$

where each sweep costs about as much as one multiplication by $A$. The
questions are: does the sequence converge, and how many sweeps does it need?
This unit answers both, with evidence.

## The splitting $A = D - L - U$

All three methods in this unit use the same splitting of $A$: $D$ is the
diagonal of $A$, $-L$ is the part strictly below the diagonal, and $-U$ the
part strictly above. The methods need every diagonal entry $a_{ii}$ to be
nonzero.

## The test systems

| System | Description | Size | Used for |
|---|---|---|---|
| L1 | Burden and Faires' 4 × 4 example (solution $(1, 2, -1, 1)$) | 4 | gate G1 |
| L2 | A non-symmetric, diagonally dominant 5 × 5 system | 5 | gates G1, G2 |
| L3 | The 1D Poisson model problem: $2$ on the diagonal, $-1$ next to it | 6 to 40 | gates G1, G3; results R1 to R3, R5 |
| L4 | The 2D Poisson problem on a 6 × 6 grid | 36 | gate G4 |
| L5 | Symmetric positive definite, not diagonally dominant | 3 | result R4 |
| L6 | The classical counterexample | 3 | result R4 |

Every system has a known exact solution, so the error can always be measured.
