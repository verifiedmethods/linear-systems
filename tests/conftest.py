import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def synthetic_sweep(factor, inplace=False):
    """A 'method' whose error falls by exactly ``factor`` per sweep: x_new = x* + factor (x - x*).

    It uses a direct solve to find x*, so no real Jacobi or Gauss-Seidel code appears
    in the public tests.
    """

    def sweep(A, b, x):
        xs = np.linalg.solve(A, b)
        if inplace:
            x += (1.0 - factor) * (xs - x)
            return x
        return xs + factor * (x - xs)

    return sweep


@pytest.fixture
def root():
    return ROOT
