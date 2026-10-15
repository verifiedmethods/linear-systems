"""Your work for unit A2: one sweep of three iterative methods for A x = b.

Write each function below, then run   python verify.py   in this unit's
folder. The tutorial (tutorial/ folder) explains each method; section numbers
are given in each function. The provided code repeats your sweep until the
residual is small: you write ONE sweep only.

All three functions receive:

    A : the matrix, a 2-D NumPy array of shape (n, n), with nonzero diagonal.
    b : the right-hand side, a 1-D NumPy array of length n.
    x : the current iterate x^(k), a 1-D NumPy array of length n.

and must return the next iterate x^(k+1) as a NEW 1-D NumPy array.

Rules (the checks test most of them):
  * Use only NumPy (no np.linalg.solve: one sweep is not a full solve).
  * Do not change A, b or x. For Gauss-Seidel and SOR, start with
    x_new = x.copy() and update x_new only.
  * Your code must work for any n; do not assume a particular size.
"""

import numpy as np  # noqa: F401  (you will probably need it)


def jacobi_sweep(A, b, x):
    """One Jacobi sweep (tutorial section 2): every new component uses only the old x."""
    raise NotImplementedError("Write one Jacobi sweep here (tutorial section 2).")


def gauss_seidel_sweep(A, b, x):
    """One Gauss-Seidel sweep (tutorial section 4): use the newest values as soon as they are computed."""
    raise NotImplementedError("Write one Gauss-Seidel sweep here (tutorial section 4).")


def sor_sweep(A, b, x, omega):
    """One SOR sweep with relaxation factor omega (tutorial section 4). omega = 1 gives Gauss-Seidel."""
    raise NotImplementedError("Write one SOR sweep here (tutorial section 4).")
