# Unit A2: iterative methods for linear systems

Part of **verifiedmethods**: open, verification-first units for the
computational methods used in Nigerian STEM projects and theses.

> **Status:** prototype for trial (version 0.1.0.dev0); not yet a formal release.
>
> Website: https://verifiedmethods.github.io · Contact: abdgafartunde@yahoo.com

In this unit you write one sweep of three methods for $Ax = b$ (Jacobi,
Gauss–Seidel and successive over-relaxation), then show with evidence that they
work: the observed convergence factor against the spectral radius of the
iteration matrix, the number of sweeps as the system grows, the choice of the
relaxation factor, and the cases where the methods fail. A single command checks
your code and writes a **verification report** that your supervisor can read in
two minutes.

## Quick start

Set up once (details in [tutorial section 0](tutorial/00-setup.md)): in this
folder, create a virtual environment and install NumPy, SciPy and Matplotlib.

| Windows (Command Prompt) | macOS and Linux |
|---|---|
| `py -m venv .venv` | `python3 -m venv .venv` |
| `.venv\Scripts\activate` | `source .venv/bin/activate` |
| `python -m pip install -r requirements.txt` | `python -m pip install -r requirements.txt` |

Then, with the environment active:

```
python verify.py
```

1. Fill in `student/student_info.txt`.
2. Follow the [tutorial](tutorial/README.md), writing your sweeps in
   `student/steps.py`.
3. Run `python verify.py` after each change, and open
   `report/verification-report.html` in a browser.
4. When all methods pass, choose a [project brief](briefs/README.md).

Everything runs offline, in a few seconds, on a modest laptop.

## For supervisors

See [supervisors/](supervisors/README.md): how to confirm a report, viva
questions, a marking rubric, and an AI-use statement.

## What is in this folder

| Path | Contents |
|---|---|
| `student/` | The student's files: `steps.py`, `student_info.txt`, `CONTRIBUTION.md` |
| `verify.py`, `vm/` | The checks and the report generator (do not edit) |
| `tutorial/` | The tutorial, in nine short sections |
| `briefs/` | Three project briefs |
| `supervisors/` | Material for supervisors |
| `tests/`, `docs/dev/`, `tools/` | For maintainers (not in the student download) |

## Licence

Code: BSD 3-Clause (see `LICENSE`). Tutorial, briefs and supervisor material:
CC BY 4.0 (see `LICENSE-docs`).

## Citation

See `CITATION.cff`. A DOI will be added at the first release.
