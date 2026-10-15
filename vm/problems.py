"""Test systems L1 to L6 (design note, section 3)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LinearProblem:
    id: str
    title: str
    A: np.ndarray
    x_exact: np.ndarray

    @property
    def b(self) -> np.ndarray:
        return self.A @ self.x_exact

    @property
    def n(self) -> int:
        return self.A.shape[0]


def poisson1d(n: int) -> np.ndarray:
    """Tridiagonal (-1, 2, -1) matrix of order n: the 1D Poisson model problem."""
    return 2.0 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)


def poisson2d(m: int) -> np.ndarray:
    """5-point Laplacian on an m x m grid of interior points (order m*m)."""
    T, I = poisson1d(m), np.eye(m)
    return np.kron(I, T) + np.kron(T, I)


def _problems():
    p = {}
    p["L1"] = LinearProblem(
        "L1", "Burden and Faires' 4 x 4 example",
        np.array([[10.0, -1, 2, 0], [-1, 11, -1, 3], [2, -1, 10, -1], [0, 3, -1, 8]]),
        np.array([1.0, 2, -1, 1]),
    )
    p["L2"] = LinearProblem(
        "L2", "Non-symmetric, diagonally dominant 5 x 5",
        np.array([[8.0, 1, -2, 0, 1], [2, 9, 1, -3, 0], [0, -1, 7, 2, 1], [1, 0, 3, 10, -2], [-2, 1, 0, 1, 6]]),
        np.array([1.0, -1, 2, 0, 3]),
    )
    for n in (6, 10, 20, 40):
        p[f"L3n{n}"] = LinearProblem(f"L3n{n}", f"1D Poisson, n = {n}", poisson1d(n), np.ones(n))
    p["L4"] = LinearProblem("L4", "2D Poisson, 6 x 6 grid", poisson2d(6), np.ones(36))
    p["L5"] = LinearProblem(
        "L5", "Symmetric positive definite, not diagonally dominant",
        np.array([[1.0, 0.6, 0.6], [0.6, 1, 0.6], [0.6, 0.6, 1]]), np.ones(3),
    )
    p["L6"] = LinearProblem(
        "L6", "The classical counterexample",
        np.array([[1.0, 2, -2], [1, 1, 1], [2, 2, 1]]), np.ones(3),
    )
    return p


PROBLEMS = _problems()


def poisson1d_theory(n: int) -> dict:
    """Exact spectral radii for the 1D Poisson model problem."""
    rho_j = float(np.cos(np.pi / (n + 1)))
    w_opt = 2.0 / (1.0 + float(np.sin(np.pi / (n + 1))))
    return {"jacobi": rho_j, "gauss_seidel": rho_j**2, "omega_opt": w_opt, "sor_opt": w_opt - 1.0}
