"""Iteration driver and checks on what a sweep returns."""

from __future__ import annotations

import numpy as np


class StudentCodeError(Exception):
    """A sweep returned something the driver cannot use."""


def check_output(result, x: np.ndarray, name: str) -> np.ndarray:
    """Return ``result`` as a float array with the shape of ``x``, or explain why not."""
    if result is None:
        raise StudentCodeError(f"{name} returned None. Did you forget the 'return' statement?")
    try:
        arr = np.asarray(result, dtype=float)
    except (TypeError, ValueError) as exc:
        raise StudentCodeError(f"{name} returned {type(result).__name__}, which is not a numeric array: {exc}") from exc
    if arr.shape != x.shape:
        raise StudentCodeError(
            f"{name} returned an array of shape {arr.shape}; it must have the same shape as x, {x.shape}."
        )
    return arr


def iterate(sweep, A, b, x0, tol=1e-8, maxit=10000, x_exact=None, name="sweep"):
    """Apply ``sweep(A, b, x)`` until the relative residual is at most ``tol``.

    Returns a dict with ``sweeps`` (number used), ``x``, ``converged`` and the
    histories ``residual`` (relative 2-norm) and ``error`` (relative 2-norm,
    if ``x_exact`` is given), each starting with the value for ``x0``.
    """
    x = np.array(x0, dtype=float)
    nb = float(np.linalg.norm(b))
    nx = float(np.linalg.norm(x_exact)) if x_exact is not None else None
    res = [float(np.linalg.norm(b - A @ x)) / nb]
    err = [float(np.linalg.norm(x - x_exact)) / nx] if x_exact is not None else []
    k = 0
    with np.errstate(over="ignore", invalid="ignore"):
        while k < maxit and res[-1] > tol:
            x = check_output(sweep(A, b, x), x, name)
            k += 1
            r = float(np.linalg.norm(b - A @ x)) / nb
            res.append(r)
            if x_exact is not None:
                err.append(float(np.linalg.norm(x - x_exact)) / nx)
            if not np.isfinite(r) or r > 1e12:
                break
    return {"sweeps": k, "x": x, "converged": res[-1] <= tol, "residual": res, "error": err}
