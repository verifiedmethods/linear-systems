# Unit A2 tutorial: iterative methods for linear systems

This tutorial teaches Jacobi's method, the Gauss–Seidel method and successive
over-relaxation (SOR) for $Ax = b$, and how to *verify* your code: to show,
with evidence, that it converges exactly as fast as the theory predicts. Work
through the sections in order; each one ends with something to do.

| Section | Topic |
|---|---|
| [0](00-setup.md) | Setting up Python and running `verify.py` for the first time |
| [1](01-the-problem.md) | Linear systems: direct and iterative methods |
| [2](02-jacobi.md) | Jacobi's method: write `jacobi_sweep` |
| [3](03-iteration-matrix.md) | Primer: the iteration matrix and the spectral radius |
| [4](04-gauss-seidel-and-sor.md) | Gauss–Seidel and SOR: write `gauss_seidel_sweep` and `sor_sweep` |
| [5](05-comparing-methods.md) | Comparing the methods: sweeps, size and the choice of $\omega$ |
| [6](06-when-methods-fail.md) | When the methods fail |
| [7](07-residual-and-error.md) | Residual, error and when to stop |
| [8](08-report-and-brief.md) | Reading your report and choosing a project brief |

**What you need:** a laptop (4 GB of memory is enough), Python 3.10 or later
with NumPy, SciPy and Matplotlib, and about four to six hours for sections 0
to 7, best spread over several sittings.

**What you should know already:** matrices and vectors, eigenvalues, and basic
Python (variables, loops, functions, and NumPy arrays). Unit A1 is helpful but
not required.

**What you hand in:** your `student/steps.py`, your verification report, your
completed `student/CONTRIBUTION.md`, and the write-up for your project brief.
