"""Gates and reported results for unit A2 (design note, section 4).

A *gate* must pass. A *reported result* is shown next to the theoretical
expectation with no pass threshold; the student's write-up interprets it.
"""

from __future__ import annotations

import json
import math
import traceback
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .iterate import StudentCodeError, check_output, iterate
from .problems import PROBLEMS, poisson1d_theory
from .study import iteration_matrix, observed_factor, predicted_sweeps, spectral_radius

EXPECTED_PATH = Path(__file__).with_name("expected.json")

ONE_SWEEP_RTOL = 1e-12
FACTOR_RTOL = 1e-3
FACTOR_RANGE = (100, 200)
FACTOR_PROBLEM = "L3n20"
SOLUTION_TOL, SOLUTION_MAXIT, SOLUTION_ERR = 1e-10, 5000, 1e-8
OMEGA_G1, OMEGA_G3 = 1.25, 1.5
SWEEP_NS = (10, 20, 40)
R1_TOL, R1_MAXIT = 1e-8, 20000
OMEGAS = tuple(round(1.0 + 0.05 * i, 2) for i in range(20))  # 1.00 to 1.95

# Which gate the summary line reports, and how to label it.
SUMMARY_GATE, SUMMARY_LABEL = "G3", "observed factor"


@dataclass(frozen=True)
class MethodSpec:
    key: str
    name: str
    function: str
    kind: str
    tutorial_section: str


METHODS = (
    MethodSpec("jacobi", "Jacobi", "jacobi_sweep", "jacobi", "2"),
    MethodSpec("gauss_seidel", "Gauss–Seidel", "gauss_seidel_sweep", "gauss_seidel", "4"),
    MethodSpec("sor", "SOR", "sor_sweep", "sor", "4"),
)


@dataclass
class GateResult:
    id: str
    title: str
    passed: bool
    measured: str
    tolerance: str
    reason: str
    hint: str = ""
    value: float | None = None

    def to_dict(self):
        return dict(self.__dict__)


@dataclass
class MethodResult:
    spec: MethodSpec
    status: str  # "not implemented", "missing", "checked"
    gates: list = field(default_factory=list)
    reported: dict = field(default_factory=dict)
    message: str = ""

    @property
    def n_passed(self) -> int:
        return sum(g.passed for g in self.gates)

    @property
    def all_passed(self) -> bool:
        return self.status == "checked" and all(g.passed for g in self.gates)

    def to_dict(self):
        return {
            "method": self.spec.key,
            "name": self.spec.name,
            "function": self.spec.function,
            "status": self.status,
            "message": self.message,
            "gates_passed": self.n_passed,
            "gates_total": len(self.gates),
            "gates": [g.to_dict() for g in self.gates],
            "reported": self.reported,
        }


def load_expected(path: Path = EXPECTED_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def explain(exc: BaseException, student_file: str) -> str:
    """Describe an exception raised by student code, pointing at the line in their file."""
    if isinstance(exc, StudentCodeError):
        return str(exc)
    name = Path(student_file).name
    frames = [fr for fr in traceback.extract_tb(exc.__traceback__) if Path(fr.filename).name == name]
    where = ""
    if frames:
        fr = frames[-1]
        where = f" (line {fr.lineno} of {name}: {(fr.line or '').strip()})"
    return f"Your code raised {type(exc).__name__}: {exc}{where}"


def bind(step, spec: MethodSpec, omega: float):
    """A three-argument sweep; SOR gets its relaxation factor."""
    if spec.kind == "sor":
        return lambda A, b, x: step(A, b, x, omega)
    return step


def rho_of(spec: MethodSpec, A, omega: float) -> float:
    return spectral_radius(iteration_matrix(A, spec.kind, omega))


_HINT_G1 = {
    "jacobi": "Jacobi uses only the old values: compute every new component from the old vector x, "
              "and store the results in a separate new array.",
    "gauss_seidel": "Gauss–Seidel uses the newest values: for row i, the components before i come from the "
                    "new iterate and those after i from the old one.",
    "sor": "SOR relaxes each Gauss–Seidel value: x_i(new) = (1 - omega) x_i(old) + omega x_i(GS), where "
           "x_i(GS) is computed with the newest values.",
}


# --------------------------------------------------------------------------- gates


def gate_one_sweep(step, spec: MethodSpec, expected: dict) -> GateResult:
    worst, worst_case = 0.0, ""
    for case, values in zip(expected["cases"], expected["values"][spec.key]):
        prob = PROBLEMS[case["problem"]]
        x0 = np.array(case["x0"], dtype=float)
        sweep = bind(step, spec, case["omega"])
        out = check_output(sweep(prob.A.copy(), prob.b.copy(), x0.copy()), x0, spec.function)
        exp = np.array(values, dtype=float)
        rel = float(np.max(np.abs(out - exp)) / np.max(np.abs(exp)))
        if not math.isfinite(rel):
            rel = math.inf
        if rel > worst:
            worst, worst_case = rel, case["problem"]
    passed = worst <= ONE_SWEEP_RTOL
    hint = ""
    if not passed:
        hint = (f"Largest difference on {worst_case}. {_HINT_G1[spec.key]} "
                f"See tutorial section {spec.tutorial_section}.")
    return GateResult(
        "G1", "One sweep matches the method",
        passed, f"largest relative difference {worst:.1e}",
        f"≤ {ONE_SWEEP_RTOL:.0e}",
        f"One sweep from stored starting vectors on L1, L2 and L3 (n = 6){' with omega = 1.25' if spec.kind == 'sor' else ''}. "
        "Only rounding separates a correct sweep from the stored values.",
        hint, worst,
    )


def gate_side_effects(step, spec: MethodSpec) -> GateResult:
    prob = PROBLEMS["L2"]
    A, b, x = prob.A.copy(), prob.b.copy(), np.array([0.5, -1.0, 2.0, 0.25, 1.5])
    A0, b0, x0 = A.copy(), b.copy(), x.copy()
    result = bind(step, spec, OMEGA_G1)(A, b, x)
    problems, hints = [], []
    changed_x = not np.array_equal(x, x0)
    if result is None:
        problems.append("returned None")
        hints.append("Your sweep returned None: did you forget the 'return' statement?")
    else:
        try:
            shape = np.shape(np.asarray(result, dtype=float))
        except (TypeError, ValueError):
            shape = None
        if shape != (5,):
            problems.append(f"returned shape {shape} for a system of 5 equations")
            hints.append("Return the new iterate as a 1-D NumPy array with one entry per unknown.")
        elif result is x and not changed_x:
            problems.append("returned the input array x itself")
            hints.append("Return a new array (for example x_new = x.copy(), then update x_new).")
    if changed_x:
        problems.append("changed the input x" + (" and returned it" if result is x else ""))
        hints.append("Start with x_new = x.copy() (Gauss–Seidel, SOR) or a new array (Jacobi), and update x_new only.")
    if not np.array_equal(A, A0) or not np.array_equal(b, b0):
        problems.append("changed A or b")
        hints.append("Never modify A or b (for example by dividing rows by the diagonal): the caller still needs them.")
    passed = not problems
    return GateResult(
        "G2", "No side effects",
        passed, "correct" if passed else "; ".join(problems),
        "exact",
        "A sweep must return a new array and leave A, b and x unchanged; changing x in place is the most "
        "common bug in hand-written Gauss–Seidel code.",
        " ".join(hints),
    )


def gate_factor(step, spec: MethodSpec):
    prob = PROBLEMS[FACTOR_PROBLEM]
    rho = rho_of(spec, prob.A, OMEGA_G3)
    k0, k1 = FACTOR_RANGE
    f, e0, _ = observed_factor(bind(step, spec, OMEGA_G3), prob.A, prob.b, prob.x_exact, k0, k1, spec.function,
                               return_errors=True)
    rel = abs(f - rho) / rho if math.isfinite(f) else math.inf
    passed = rel <= FACTOR_RTOL
    hint = ""
    if not passed:
        if math.isfinite(e0) and e0 < 1e-12:
            hint = (f"After {k0} sweeps your error was already at rounding level ({e0:.0e}), so it cannot fall any "
                    "further. A sweep should improve the iterate a little, not solve the system: are you solving it "
                    "directly (for example with np.linalg.solve)?")
        elif math.isfinite(f):
            others = {m.name: rho_of(m, prob.A, OMEGA_G3) for m in METHODS if m.key != spec.key}
            close = [n for n, r in others.items() if abs(f - r) / r <= FACTOR_RTOL]
            hint = (f"Your error falls by {f:.6f} per sweep, but {spec.name}'s spectral radius here is {rho:.6f}."
                    + (f" Your factor matches {close[0]}'s: check which values your sweep uses." if close else
                       " Check the formula against tutorial section " + spec.tutorial_section + "."))
        else:
            hint = "The error did not shrink steadily (it was zero, infinite or not a number), so no factor could be measured."
    gate = GateResult(
        "G3", "Observed convergence factor matches the spectral radius",
        passed, f"factor {f:.6f}; rho(T) = {rho:.6f}" if math.isfinite(f) else "factor not defined",
        f"relative difference ≤ {FACTOR_RTOL:.0e}",
        f"On L3 (1D Poisson, n = 20){', omega = 1.5' if spec.kind == 'sor' else ''}, from x = 0: "
        f"(||e_{k1}|| / ||e_{k0}||)^(1/{k1 - k0}) against rho(T) from the eigenvalues of the iteration matrix.",
        hint, f if math.isfinite(f) else None,
    )
    return gate, rho


def gate_solution(step, spec: MethodSpec) -> GateResult:
    prob = PROBLEMS["L4"]
    out = iterate(bind(step, spec, OMEGA_G3), prob.A, prob.b, np.zeros(prob.n), SOLUTION_TOL, SOLUTION_MAXIT,
                  prob.x_exact, spec.function)
    err = out["error"][-1]
    passed = out["converged"] and err <= SOLUTION_ERR
    hint = ""
    if not passed:
        hint = ("The iteration did not reach the solution of the 36-unknown system. If your sweep passes G1, "
                "check that nothing in it depends on the size of the system.")
    return GateResult(
        "G4", "Reaches the solution",
        passed, f"{out['sweeps']} sweeps; relative error {err:.1e}",
        f"residual ≤ {SOLUTION_TOL:.0e} within {SOLUTION_MAXIT} sweeps; error ≤ {SOLUTION_ERR:.0e}",
        f"L4 (2D Poisson, 36 unknowns){', omega = 1.5' if spec.kind == 'sor' else ''}, from x = 0.",
        hint, float(out["sweeps"]),
    )


# --------------------------------------------------------------------------- reported results


def report_sweeps_vs_n(step, spec: MethodSpec):
    rows = []
    for n in SWEEP_NS:
        prob = PROBLEMS[f"L3n{n}"]
        omega = poisson1d_theory(n)["omega_opt"] if spec.kind == "sor" else 1.0
        rho = rho_of(spec, prob.A, omega)
        out = iterate(bind(step, spec, omega), prob.A, prob.b, np.zeros(n), R1_TOL, R1_MAXIT, None, spec.function)
        rows.append({"n": n, "omega": omega if spec.kind == "sor" else None, "rho": rho,
                     "predicted": predicted_sweeps(rho, R1_TOL), "sweeps": out["sweeps"], "converged": out["converged"]})
    return {"tol": R1_TOL, "rows": rows}


def report_history(step, spec: MethodSpec):
    prob = PROBLEMS["L3n20"]
    omega = poisson1d_theory(20)["omega_opt"] if spec.kind == "sor" else 1.0
    out = iterate(bind(step, spec, omega), prob.A, prob.b, np.zeros(prob.n), R1_TOL, R1_MAXIT, None, spec.function)
    return {"omega": omega if spec.kind == "sor" else None, "rho": rho_of(spec, prob.A, omega),
            "residual": out["residual"]}


def report_omega_scan(step, spec: MethodSpec):
    prob = PROBLEMS["L3n20"]
    rows = []
    for omega in OMEGAS:
        out = iterate(bind(step, spec, omega), prob.A, prob.b, np.zeros(prob.n), R1_TOL, 5000, None, spec.function)
        rows.append({"omega": omega, "sweeps": out["sweeps"], "converged": out["converged"],
                     "rho": rho_of(spec, prob.A, omega)})
    return {"omega_opt": poisson1d_theory(20)["omega_opt"], "rows": rows}


def report_failures(step, spec: MethodSpec):
    rows = []
    for pid in ("L5", "L6"):
        prob = PROBLEMS[pid]
        rho = rho_of(spec, prob.A, OMEGA_G1)
        out = iterate(bind(step, spec, OMEGA_G1), prob.A, prob.b, np.zeros(prob.n), 1e-300, 50, prob.x_exact,
                      spec.function)
        e = out["error"][-1]
        rows.append({"problem": pid, "title": prob.title, "rho": rho, "error_after": e, "sweeps": out["sweeps"],
                     "behaviour": "converges" if (math.isfinite(e) and e < 1e-3) else "does not converge"})
    return {"omega": OMEGA_G1 if spec.kind == "sor" else None, "rows": rows}


def report_residual_vs_error(step, spec: MethodSpec):
    prob = PROBLEMS["L3n40"]
    omega = poisson1d_theory(40)["omega_opt"] if spec.kind == "sor" else 1.0
    out = iterate(bind(step, spec, omega), prob.A, prob.b, np.zeros(prob.n), R1_TOL, R1_MAXIT, prob.x_exact,
                  spec.function)
    cond = float(np.linalg.cond(prob.A))
    return {"cond": cond, "residual": out["residual"][-1], "error": out["error"][-1],
            "bound": cond * out["residual"][-1], "sweeps": out["sweeps"]}


# --------------------------------------------------------------------------- driver


def run_method(step, spec: MethodSpec, expected: dict, student_file: str) -> MethodResult:
    probe = PROBLEMS["L1"]
    try:
        bind(step, spec, OMEGA_G1)(probe.A.copy(), probe.b.copy(), np.zeros(4))
    except NotImplementedError:
        return MethodResult(spec, "not implemented", message=f"{spec.function} is not implemented yet.")
    except Exception:
        pass

    result = MethodResult(spec, "checked")
    try:
        result.gates.append(gate_one_sweep(step, spec, expected))
    except Exception as exc:
        result.gates.append(GateResult("G1", "One sweep matches the method", False, "could not run", "", "",
                                       explain(exc, student_file)))
    try:
        result.gates.append(gate_side_effects(step, spec))
    except Exception as exc:
        result.gates.append(GateResult("G2", "No side effects", False, "could not run", "", "",
                                       explain(exc, student_file)))
    try:
        gate, rho = gate_factor(step, spec)
        result.gates.append(gate)
        result.reported["rho_L3n20"] = rho
    except Exception as exc:
        result.gates.append(GateResult("G3", "Observed convergence factor matches the spectral radius", False,
                                       "could not run", "", "", explain(exc, student_file)))
    try:
        result.gates.append(gate_solution(step, spec))
    except Exception as exc:
        result.gates.append(GateResult("G4", "Reaches the solution", False, "could not run", "", "",
                                       explain(exc, student_file)))

    reports = [("sweeps_vs_n", report_sweeps_vs_n), ("history", report_history),
               ("failures", report_failures), ("residual_vs_error", report_residual_vs_error)]
    if spec.kind == "sor":
        reports.insert(2, ("omega_scan", report_omega_scan))
    for key, fn in reports:
        try:
            result.reported[key] = fn(step, spec)
        except Exception as exc:
            result.reported[key] = {"error": explain(exc, student_file)}
    return result


def run_all(module, student_file: str, expected: dict | None = None):
    expected = expected or load_expected()
    results = []
    for spec in METHODS:
        step = getattr(module, spec.function, None)
        if step is None or not callable(step):
            results.append(MethodResult(spec, "missing", message=f"steps.py has no function named {spec.function}."))
            continue
        results.append(run_method(step, spec, expected, student_file))
    return results
