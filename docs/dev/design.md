# Unit A2 design: iterative methods for linear systems

Status: draft for review, 16 October 2026. Nothing is implemented yet. The numbers below come from a reference run on 16 October 2026; the script is in the private `solutions` repository (`linear_systems/reference_study.py`).

## 1. Purpose

A2 is the second undergraduate unit. It teaches the three classical stationary iterative methods for $Ax = b$, written with the splitting $A = D - L - U$ ($D$ diagonal, $-L$ and $-U$ the strictly lower and upper parts):

| Method | One sweep | Iteration matrix $T$ |
|---|---|---|
| Jacobi | $x^{(k+1)} = D^{-1}\big(b + (L + U)\,x^{(k)}\big)$ | $D^{-1}(L + U)$ |
| Gauss–Seidel | $x^{(k+1)} = (D - L)^{-1}\big(b + U x^{(k)}\big)$, computed row by row using the newest values | $(D - L)^{-1} U$ |
| SOR | each Gauss–Seidel value relaxed: $x_i^{(k+1)} = (1 - \omega)\,x_i^{(k)} + \omega\,x_i^{\text{GS}}$ | $(D - \omega L)^{-1}\big((1 - \omega) D + \omega U\big)$ |

The error satisfies $e^{(k+1)} = T e^{(k)}$, so each method converges for every starting vector exactly when the spectral radius $\rho(T) < 1$, and the error falls asymptotically by a factor $\rho(T)$ per sweep. That one fact is the verification idea of the unit: **the observed convergence factor must match $\rho(T)$**.

**Who it is for:** final-year undergraduates (the "Jacobi versus Gauss–Seidel" project); MSc students working on accelerated, preconditioned or refined variants, which are an active research line in Nigerian mathematics departments (FUT Minna in particular).

**What the student does:** writes the three sweep functions, then carries out and writes up a study: observed convergence factor against $\rho(T)$, iteration counts as the system grows, the choice of $\omega$, the cases where the methods fail, and the difference between a small residual and a small error.

## 2. Student experience

Identical in shape to A1: fill in `student/student_info.txt`; implement `jacobi_sweep(A, b, x)`, `gauss_seidel_sweep(A, b, x)` and `sor_sweep(A, b, x, omega)` in `student/steps.py`; run `python verify.py`; read the report; choose a brief. Each function returns the new iterate as a **new** array and must not change `A`, `b` or `x`. Students who already set up Python for A1 can reuse the same environment.

## 3. Test problems

| ID | System | Size | Why |
|---|---|---|---|
| L1 | Burden and Faires' 4 × 4 example: rows $(10, -1, 2, 0)$, $(-1, 11, -1, 3)$, $(2, -1, 10, -1)$, $(0, 3, -1, 8)$; $b = (6, 25, -11, 15)$; solution $(1, 2, -1, 1)$ | 4 | Familiar textbook example; strictly diagonally dominant. $\rho_J = 0.426$, $\rho_{GS} = 0.090$. |
| L2 | A non-symmetric, strictly diagonally dominant 5 × 5 system with integer entries and a known solution | 5 | Catches code that silently assumes symmetry. |
| L3 | 1D Poisson model problem: tridiagonal $(-1, 2, -1)$, $n = 10, 20, 40$ | 10–40 | Spectral radii known exactly: $\rho_J = \cos\frac{\pi}{n+1}$, $\rho_{GS} = \rho_J^2$, $\omega_{\text{opt}} = \frac{2}{1 + \sin\frac{\pi}{n+1}}$, $\rho_{SOR}(\omega_{\text{opt}}) = \omega_{\text{opt}} - 1$. For $n = 20$: 0.988831, 0.977786, 1.74058, 0.74058. |
| L4 | 2D Poisson (5-point) on a 6 × 6 grid | 36 | A larger, block-structured system. |
| L5 | Symmetric positive definite but not diagonally dominant: ones on the diagonal, 0.6 elsewhere (3 × 3) | 3 | Jacobi diverges ($\rho_J = 1.2$); Gauss–Seidel converges ($\rho_{GS} = 0.465$). |
| L6 | The classical counterexample with rows $(1, 2, -2)$, $(1, 1, 1)$, $(2, 2, 1)$ | 3 | Jacobi converges ($\rho_J = 0$, it finishes in three sweeps); Gauss–Seidel diverges ($\rho_{GS} = 2$). |

All matrices are dense NumPy arrays in v0.1; sparse storage is left for a later unit.

## 4. Checks

### 4.1 Gates (per method)

| # | Gate | Tolerance and reason |
|---|---|---|
| G1 | **One sweep matches the method.** One sweep from stored starting vectors on L1, L2 and L3 ($n = 6$), and for SOR with $\omega = 1.25$, agrees with stored values. | Relative difference $\le 10^{-12}$: rounding only. Stored values come from the private reference; no reference code ships. A direct solve (`np.linalg.solve`) fails this gate, since it returns the solution, not one sweep. |
| G2 | **No side effects.** After a sweep, `A`, `b` and `x` are unchanged, and the result is a new array of shape $(n,)$. | Exact. Gauss–Seidel code that updates `x` in place, or that scales the rows of `A` in place, is the most common bug. |
| G3 | **Observed convergence factor matches the spectral radius.** On L3 ($n = 20$; SOR with $\omega = 1.5$), the factor $\big(\lVert e^{(200)}\rVert / \lVert e^{(100)}\rVert\big)^{1/100}$ is compared with $\rho(T)$ computed by the harness from the eigenvalues of $T$. | Relative difference $\le 10^{-3}$. Measured: $5 \times 10^{-7}$ or less for all three methods. The tolerance separates Jacobi (0.9888) from Gauss–Seidel (0.9778), a 1.1% difference, by a factor of ten. |
| G4 | **Reaches the solution.** From $x^{(0)} = 0$ on L4, iterate until the relative residual is $\le 10^{-10}$ (at most 5000 sweeps); the relative error must be $\le 10^{-8}$. | Measured: Jacobi 212 sweeps, Gauss–Seidel 107, SOR ($\omega = 1.5$) 38; errors about $2 \times 10^{-10}$. Catches code that works only for the small G1 cases (for example a hard-coded size). |

### 4.2 Reported results (no threshold)

| # | Result | Expected (reference run) |
|---|---|---|
| R1 | Sweeps to reach relative residual $10^{-8}$ on L3 for $n = 10, 20, 40$, with the prediction from $\rho(T)$ | Jacobi 403, 1397, 4999; Gauss–Seidel 203, 700, 2501; SOR($\omega_{\text{opt}}$) 38, 70, 131. Jacobi and Gauss–Seidel grow about 4× per doubling of $n$, SOR about 2×. |
| R2 | SOR: sweeps against $\omega \in [1.00, 1.95]$ on L3 ($n = 20$), with $\omega_{\text{opt}}$ marked | a sharp minimum near 1.74 |
| R3 | Residual history (log scale) for the three methods on L3 ($n = 20$), with the lines $\rho(T)^k$ | parallel lines |
| R4 | The failure cases L5 and L6: $\rho(T)$ and the behaviour after 50 sweeps | Jacobi diverges on L5 and converges on L6; Gauss–Seidel the opposite |
| R5 | Residual against error on L3 ($n = 40$, condition number 681) at the stopping point | relative residual $1.0 \times 10^{-8}$ but relative error $2.3 \times 10^{-7}$; the bound $\kappa(A)\, \lVert r\rVert / \lVert b\rVert = 6.8 \times 10^{-6}$ |

### 4.3 Checks on the checks (private maintainer tests)

Broken versions that must fail at least one gate:

| Mistake | Expected to be caught by |
|---|---|
| Jacobi written with the newest values (so it is Gauss–Seidel) | G1, G3 |
| Gauss–Seidel written without the newest values (so it is Jacobi) | G1, G3 |
| SOR relaxing towards the wrong value, or $\omega$ applied to the whole vector after a Jacobi sweep | G1, G3 |
| Off-by-one row slices (`A[i, :i+1]`) | G1 |
| Updating the input `x` in place | G2 (and G1 for Jacobi) |
| Scaling the rows of `A` in place | G2 |
| `np.linalg.solve(A, b)` returned as the "sweep" | G1, G3 |
| Code that only works for $n = 4$ | G1 or G4 |

## 5. Software

The verification report, the runner (student information, import scan, captured prints, exit codes), the fingerprints and the bundle builder are the same as A1's. For v0.1 they are copied from A1 and adapted. When the template is refined (plan weekend 13) the shared parts move to one place used by every unit.

Problem-specific modules: `problems.py` (L1 to L6), `iterate.py` (the iteration driver, residual and error histories), `study.py` (convergence factor, sweep counts, $\omega$ sweep), `checks.py` (G1 to G4, R1 to R5).

Time: the full check takes under 2 seconds (Gauss–Seidel on $n = 40$ to $10^{-8}$ takes 0.12 s in plain Python).

## 6. Tutorial outline

0. Setting up (as in A1; an existing A1 environment works).
1. The problem $Ax = b$; direct and iterative methods; why large sparse systems (from differential equations) need iterative methods.
2. Jacobi's method from the splitting $A = D - L - U$; write `jacobi_sweep`.
3. **Primer: the iteration matrix and the spectral radius.** $e^{(k+1)} = Te^{(k)}$, convergence when $\rho(T) < 1$, and measuring the observed convergence factor.
4. Gauss–Seidel and SOR; write both.
5. Comparing methods: sweeps against size, work per sweep, choosing $\omega$; the theory for the model problem.
6. When the methods fail: diagonal dominance, symmetric positive definite matrices, and the two counterexamples.
7. Residual, error and stopping criteria; the condition number.
8. Reading the report and choosing a brief.

## 7. Project briefs (prototype: three)

1. **Comparing Jacobi, Gauss–Seidel and SOR properly.** Predict sweep counts from $\rho(T)$ and check the predictions; how counts grow with $n$; how to choose $\omega$, and how sensitive SOR is to a poor choice.
2. **Steady temperature in a plate.** Solve the 2D Laplace equation with given edge temperatures on finer and finer grids. Two errors are present, the discretisation error (from the grid) and the iteration error (from stopping early): show both, and choose a stopping tolerance that makes the iteration error small compared with the discretisation error. Compare the cost with a direct solve.
3. **When do iterative methods converge?** Test diagonal dominance and positive definiteness as conditions on L5, L6 and matrices of the student's own construction, and explain every result through $\rho(T)$.

**Possible fourth brief (decision needed, Section 9):** *refined and accelerated variants.* Many published variants (refinements, preconditioned and accelerated methods) report fewer iterations than the classical methods. A brief could ask the student to implement one such variant and compare it with the classical method both by iterations **and by work** (matrix–vector products or arithmetic operations per iteration). For example, a once-refined Jacobi iteration is algebraically two Jacobi sweeps, so it needs about half as many iterations at about twice the cost per iteration. This is a valuable verification lesson, and it connects the unit to local research. It also touches the published work of colleagues, so the framing must be neutral and respectful: "compare by work as well as by iterations", with no criticism of particular papers.

## 8. Supervisor pack

As in A1: how to confirm a report; about ten viva questions (for example "Why does Gauss–Seidel need about half as many sweeps as Jacobi on this problem?", "Show where your Gauss–Seidel code uses the newest values", "Why does Jacobi diverge on L5 although the matrix is symmetric positive definite?", "Your residual is $10^{-8}$; what can you say about the error?"); a rubric; the AI-use statement.

## 9. Open questions for review

1. **Methods:** Jacobi, Gauss–Seidel and SOR for v0.1? (AOR and symmetric SOR could come later.)
2. **API:** students write one sweep and the harness iterates. Agreed, or should students also write the iteration loop with its stopping test?
3. **Gate G3** tolerance of $10^{-3}$ relative: acceptable?
4. **The fourth brief** on refined and accelerated variants: include it in v0.1 (neutral framing as in Section 7), leave it for later, or drop it?
5. **Brief 2** context: is a heated plate right, or would a Nigerian example be better (for example groundwater head between rivers, or temperature in a building wall)?
6. **Unit name and address:** `linear-systems` (https://verifiedmethods.github.io/units/linear-systems/)?
