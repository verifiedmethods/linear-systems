from copy import deepcopy
from types import SimpleNamespace

import numpy as np
import pytest

from conftest import synthetic_sweep
from vm import checks
from vm.iterate import iterate
from vm.study import iteration_matrix, observed_factor, spectral_radius


def test_mutating_method_leaves_other_methods_grades_and_systems_intact(monkeypatch):
    problems = deepcopy(checks.PROBLEMS)
    monkeypatch.setattr(checks, "PROBLEMS", problems)
    original = {key: p.A.copy() for key, p in problems.items()}
    probe = problems["L3n20"].A
    gs = synthetic_sweep(spectral_radius(iteration_matrix(probe, "gauss_seidel")))
    sor = synthetic_sweep(spectral_radius(iteration_matrix(probe, "sor", 1.5)))
    module = SimpleNamespace(gauss_seidel_sweep=gs, sor_sweep=lambda A, b, x, omega: sor(A, b, x))
    baseline = checks.run_all(module, "steps.py")

    def mutates_matrix(A, b, x):
        np.fill_diagonal(A, 0)
        return x.copy()

    module.jacobi_sweep = mutates_matrix
    result = checks.run_all(module, "steps.py")

    assert not result[0].gates[1].passed
    assert "changed A or b" in result[0].gates[1].measured
    for before, after in zip(baseline[1:], result[1:]):
        assert before.gates[2].passed and before.gates[3].passed
        assert after.gates == before.gates
        assert after.reported == before.reported
    for key, p in problems.items():
        np.testing.assert_array_equal(p.A, original[key])


@pytest.mark.parametrize("study", ["iterate", "observed_factor"])
@pytest.mark.parametrize("changed", ["matrix", "rhs"])
def test_study_rejects_changes_to_its_system(study, changed):
    matrix, rhs = np.eye(2), np.ones(2)

    def mutates_system(A, b, x):
        target = A if changed == "matrix" else b
        target[:] = 0
        return x.copy()

    with pytest.raises(ValueError, match="read-only"):
        if study == "iterate":
            iterate(mutates_system, matrix, rhs, np.zeros(2))
        else:
            observed_factor(mutates_system, matrix, rhs, rhs.copy(), 1, 2)
    np.testing.assert_array_equal(matrix, np.eye(2))
    np.testing.assert_array_equal(rhs, np.ones(2))
