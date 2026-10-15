"""Iteration matrices, spectral radii and convergence studies."""

from __future__ import annotations

import math

import numpy as np

from .iterate import check_output


def splitting(A):
    """A = D - L - U with D diagonal, L strictly lower, U strictly upper."""
    D = np.diag(np.diag(A))
    return D, -np.tril(A, -1), -np.triu(A, 1)


def iteration_matrix(A, kind: str, omega: float = 1.0) -> np.ndarray:
    D, L, U = splitting(A)
    if kind == "jacobi":
        return np.linalg.solve(D, L + U)
    if kind == "gauss_seidel":
        return np.linalg.solve(D - L, U)
    if kind == "sor":
        return np.linalg.solve(D - omega * L, (1.0 - omega) * D + omega * U)
    raise ValueError(kind)


def spectral_radius(T) -> float:
    return float(np.max(np.abs(np.linalg.eigvals(T))))


def observed_factor(sweep, A, b, x_exact, k0: int, k1: int, name="sweep", return_errors=False):
    """(||e_k1|| / ||e_k0||)^(1/(k1-k0)) from x0 = 0: the measured convergence factor.

    With ``return_errors=True``, return ``(factor, ||e_k0|| / ||x_exact||, ||e_k1|| / ||x_exact||)``.
    """
    x = np.zeros_like(b)
    e0 = None
    with np.errstate(over="ignore", invalid="ignore"):
        for k in range(1, k1 + 1):
            x = check_output(sweep(A, b, x), x, name)
            if k == k0:
                e0 = float(np.linalg.norm(x - x_exact))
    e1 = float(np.linalg.norm(x - x_exact))
    if not e0 or not math.isfinite(e0) or not math.isfinite(e1) or e1 <= 0:
        f = float("nan")
    else:
        f = (e1 / e0) ** (1.0 / (k1 - k0))
    if return_errors:
        nx = float(np.linalg.norm(x_exact))
        return f, (e0 or 0.0) / nx, e1 / nx
    return f


def predicted_sweeps(rho: float, tol: float) -> float:
    """Sweeps for the error to fall by a factor tol if it falls by rho per sweep."""
    if not (0 < rho < 1):
        return float("inf") if rho >= 1 else 1.0
    return math.log(tol) / math.log(rho)
