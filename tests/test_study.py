import math

import numpy as np
import pytest

from conftest import synthetic_sweep
from vm.iterate import iterate
from vm.problems import PROBLEMS
from vm.study import observed_factor, predicted_sweeps


def test_observed_factor_recovers_a_known_factor():
    p = PROBLEMS["L3n20"]
    for f in (0.5, 0.9, 0.98):
        # a range where the error is still far above rounding level
        assert abs(observed_factor(synthetic_sweep(f), p.A, p.b, p.x_exact, 5, 15) - f) < 1e-8


def test_iterate_stops_at_the_tolerance():
    p = PROBLEMS["L1"]
    out = iterate(synthetic_sweep(0.1), p.A, p.b, [0, 0, 0, 0], tol=1e-8, x_exact=p.x_exact)
    assert out["converged"] and out["residual"][-1] <= 1e-8 and out["sweeps"] == len(out["residual"]) - 1


def test_predicted_sweeps():
    assert abs(predicted_sweeps(0.1, 1e-8) - 8.0) < 1e-12
    assert math.isinf(predicted_sweeps(1.2, 1e-8))


@pytest.mark.parametrize("start", [[0.0, 0.0], [1.0, -1.0]])
@pytest.mark.parametrize("with_exact", [False, True])
def test_homogeneous_system_uses_absolute_norms(start, with_exact):
    exact = np.zeros(2) if with_exact else None
    out = iterate(lambda A, b, x: 0.5 * x, np.eye(2), np.zeros(2), start,
                  tol=1e-8, x_exact=exact)
    assert out["converged"]
    assert out["sweeps"] == (0 if start == [0.0, 0.0] else 28)
    assert out["residual"][0] == pytest.approx(np.linalg.norm(start))
    assert out["residual"][-1] <= 1e-8
    assert np.all(np.isfinite(out["residual"]))
    if with_exact:
        assert out["error"] == pytest.approx(out["residual"])
    else:
        assert out["error"] == []


def test_observed_factor_can_be_below_the_spectral_radius():
    # The initial error has no component in the slow eigendirection.
    T = np.diag([0.9, 0.5])
    exact = np.array([0.0, 1.0])
    sweep = lambda A, b, x: exact + T @ (x - exact)
    factor = observed_factor(sweep, np.eye(2), exact, exact, 5, 15)
    assert factor == pytest.approx(0.5)
    assert factor < max(abs(np.linalg.eigvals(T)))
