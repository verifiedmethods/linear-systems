import numpy as np
import pytest

from vm.problems import PROBLEMS, poisson1d_theory
from vm.study import iteration_matrix, spectral_radius


def test_systems_have_the_stated_solutions():
    for p in PROBLEMS.values():
        assert np.allclose(np.linalg.solve(p.A, p.b), p.x_exact, atol=1e-10)


def test_l1_and_l2_are_strictly_diagonally_dominant_and_l2_is_not_symmetric():
    for pid in ("L1", "L2"):
        A = PROBLEMS[pid].A
        assert np.all(2 * np.abs(np.diag(A)) > np.abs(A).sum(axis=1))
    assert not np.allclose(PROBLEMS["L2"].A, PROBLEMS["L2"].A.T)


@pytest.mark.parametrize("n", [10, 20, 40])
def test_poisson_theory_matches_the_eigenvalues(n):
    A, th = PROBLEMS[f"L3n{n}"].A, poisson1d_theory(n)
    assert abs(spectral_radius(iteration_matrix(A, "jacobi")) - th["jacobi"]) < 1e-12
    assert abs(spectral_radius(iteration_matrix(A, "gauss_seidel")) - th["gauss_seidel"]) < 1e-12
    # at the optimum the SOR matrix is defective, so its eigenvalues are only accurate to about sqrt(eps)
    assert abs(spectral_radius(iteration_matrix(A, "sor", th["omega_opt"])) - th["sor_opt"]) < 1e-5


def test_failure_cases():
    assert abs(spectral_radius(iteration_matrix(PROBLEMS["L5"].A, "jacobi")) - 1.2) < 1e-12
    assert spectral_radius(iteration_matrix(PROBLEMS["L5"].A, "gauss_seidel")) < 1
    # Jacobi's matrix for L6 is nilpotent (T^3 = 0); its computed eigenvalues are only ~eps^(1/3)
    T = iteration_matrix(PROBLEMS["L6"].A, "jacobi")
    assert np.allclose(np.linalg.matrix_power(T, 3), 0, atol=1e-12)
    assert abs(spectral_radius(iteration_matrix(PROBLEMS["L6"].A, "gauss_seidel")) - 2.0) < 1e-12
