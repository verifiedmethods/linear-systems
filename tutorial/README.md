# Unit A2 tutorial: iterative methods for linear systems

This tutorial teaches Jacobi's method, the Gauss–Seidel method and successive
over-relaxation (SOR) for $Ax = b$, and how to *verify* your code: to show,
with evidence, how its convergence relates to the theory on specified test problems. Work
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

**What you need:** a computer with Python 3.10 or later, NumPy, SciPy and
Matplotlib. Plan several sessions; setup, tutorial and project time depend on
your background. The code and reports work offline after installation; section
0 explains how to prepare formatted tutorial material for offline reading.

**What you should know already:** matrices and vectors, eigenvalues, and basic
Python (variables, loops, functions, and NumPy arrays). Unit A1 is helpful but
not required.

**What you hand in:** your `student` folder (including `steps.py`,
`student_info.txt` and completed `CONTRIBUTION.md`), your verification report,
and the agreed assignment or project write-up.

**Further reading:** Driscoll and Braun's
[*Fundamentals of Numerical Computation*, Python edition](https://fncbook.com/python/)
provides additional explanations and examples. Your lecturer's course text
should guide the depth of theory expected.
