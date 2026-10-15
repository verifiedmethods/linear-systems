import types

import numpy as np

from conftest import synthetic_sweep
from vm.checks import METHODS, gate_factor, gate_one_sweep, gate_side_effects, gate_solution, load_expected, run_all, run_method
from vm.problems import PROBLEMS, poisson1d_theory

SPEC = {m.key: m for m in METHODS}


def test_expected_values_are_consistent():
    exp = load_expected()
    assert set(exp["values"]) == set(SPEC)
    for vals in exp["values"].values():
        for case, v in zip(exp["cases"], vals):
            assert len(v) == len(case["x0"]) == PROBLEMS[case["problem"]].n and np.all(np.isfinite(v))


def test_factor_gate_measures_the_factor():
    rho_j = poisson1d_theory(20)["jacobi"]
    ok, _ = gate_factor(synthetic_sweep(rho_j), SPEC["jacobi"])
    assert ok.passed and abs(ok.value - rho_j) < 1e-9
    bad, _ = gate_factor(synthetic_sweep(poisson1d_theory(20)["gauss_seidel"]), SPEC["jacobi"])
    assert not bad.passed and "Gauss–Seidel" in bad.hint


def test_side_effect_gate():
    assert gate_side_effects(synthetic_sweep(0.5), SPEC["jacobi"]).passed
    g = gate_side_effects(synthetic_sweep(0.5, inplace=True), SPEC["gauss_seidel"])
    assert not g.passed and "changed the input x" in g.measured

    def scales_A(A, b, x):
        A /= np.diag(A)[:, None]
        return x.copy()

    assert "changed A or b" in gate_side_effects(scales_A, SPEC["jacobi"]).measured
    assert "None" in gate_side_effects(lambda A, b, x: None, SPEC["jacobi"]).hint


def test_one_sweep_gate_rejects_a_direct_solve():
    g = gate_one_sweep(lambda A, b, x: np.linalg.solve(A, b), SPEC["jacobi"], load_expected())
    assert not g.passed and "old values" in g.hint


def test_solution_gate():
    assert gate_solution(synthetic_sweep(0.5), SPEC["jacobi"]).passed
    assert not gate_solution(synthetic_sweep(1.0), SPEC["jacobi"]).passed


def test_not_implemented_and_missing():
    def stub(A, b, x, *args):
        raise NotImplementedError

    results = run_all(types.SimpleNamespace(jacobi_sweep=stub, sor_sweep=stub), "steps.py")
    assert [r.status for r in results] == ["not implemented", "missing", "not implemented"]


def test_errors_in_student_code_are_explained(tmp_path):
    src = tmp_path / "steps.py"
    src.write_text("def jacobi_sweep(A, b, x):\n    return x + undefined_name\n", encoding="utf-8")
    ns = {}
    exec(compile(src.read_text(), str(src), "exec"), ns)
    r = run_method(ns["jacobi_sweep"], SPEC["jacobi"], load_expected(), str(src))
    assert not r.all_passed and "NameError" in r.gates[0].hint and "line 2" in r.gates[0].hint


def test_factor_gate_explains_a_direct_solve():
    g, _ = gate_factor(lambda A, b, x: np.linalg.solve(A, b), SPEC["jacobi"])
    assert not g.passed and "rounding level" in g.hint and "np.linalg.solve" in g.hint


def test_side_effect_gate_gives_one_hint_for_an_in_place_sweep():
    g = gate_side_effects(synthetic_sweep(0.5, inplace=True), SPEC["gauss_seidel"])
    assert g.measured == "changed the input x and returned it" and g.hint.count("x.copy()") == 1
