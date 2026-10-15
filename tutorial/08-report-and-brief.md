# 8. Reading your report and choosing a brief

Run `python verify.py` and open `report/verification-report.html`.

## Gates (must pass)

| Gate | Question it answers |
|---|---|
| G1 One sweep matches the method | Does one sweep give the same numbers as the method, up to rounding? |
| G2 No side effects | Are `A`, `b` and `x` unchanged, and is the result a new array? |
| G3 Observed factor matches $\rho(T)$ | Does the error fall by exactly the factor the theory predicts? |
| G4 Reaches the solution | Does the iteration solve a larger (36-unknown) system? |

When a gate fails, the report gives a hint. Fix the code and run again.

## Reported results (no pass mark)

R1 to R5 are the evidence for your write-up: sweeps against size (R1), the
choice of $\omega$ (R2), convergence histories (R3), the failure cases (R4),
and residual against error (R5).

## What the report shows, and what it does not

The report shows that the code with that fingerprint passed the checks. It does
**not** show who wrote the code. Your supervisor may run your `steps.py` in
their own copy of the unit and ask you to explain any line of it.

## Printing the report

Open the report in your browser and use **Print**: on paper, or **Save as PDF**
for your appendix. The first pages (details, summary, plots and statement) are
the important ones.

## Choosing a project brief

When all three methods pass, choose one brief from `briefs/` with your
supervisor:

1. [Comparing Jacobi, Gauss–Seidel and SOR properly](../briefs/01-comparing-methods.md)
2. [Steady temperature in a heated plate](../briefs/02-heated-plate.md)
3. [When do iterative methods converge?](../briefs/03-convergence-conditions.md)

Include in your appendix: the verification report, your completed
`student/CONTRIBUTION.md`, and your `steps.py`.
