import math

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
