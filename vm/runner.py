"""Command-line entry point behind ``verify.py``."""

from __future__ import annotations

import argparse
import ast
import contextlib
import datetime as _dt
import io
import importlib.util
import os
import platform
import re
import sys
from pathlib import Path

from . import UNIT_ID, UNIT_TITLE, __version__
from .checks import SUMMARY_GATE, SUMMARY_LABEL, load_expected, run_all
from .fingerprint import file_sha256, suite_fingerprint
from .report import build_html, build_json

ROOT = Path(__file__).resolve().parent.parent

INFO_FIELDS = ("name", "matric_number", "department", "institution", "supervisor", "ai_use")
EXPECTED_IMPORTS = {"numpy", "math"}
SUSPICIOUS_CALLS = {"__import__", "exec", "eval", "compile", "open", "globals", "setattr"}


def scan_imports(path: Path):
    """Modules imported by the student's file (read with ast, not run), and anything unexpected.

    The units need only NumPy. Other imports or calls such as exec() are not
    forbidden, but a supervisor should look at the file before trusting the report.
    """
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return [], []
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            found.add((node.module or ".").split(".")[0] if node.level == 0 else "." + (node.module or ""))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in SUSPICIOUS_CALLS:
            found.add(node.func.id + "()")
    imports = sorted(found)
    return imports, [m for m in imports if m not in EXPECTED_IMPORTS]



def read_info(path: Path) -> dict:
    """Read ``key: value`` lines; indented lines continue the previous value; '#' starts a comment."""
    info, last = {}, None
    if not path.exists():
        return info
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1].isspace() and last:
            info[last] = (info[last] + " " + raw.strip()).strip()
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip().lower().replace(" ", "_").replace("-", "_")
        value = value.strip()
        if re.fullmatch(r"<[^<>]*>", value):
            value = ""  # template placeholder left unchanged
        info[key] = value
        last = key
    return {k: info.get(k, "") for k in INFO_FIELDS}


def load_steps(path: Path):
    spec = importlib.util.spec_from_file_location("student_steps", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def environment() -> dict:
    def version(name):
        try:
            return __import__(name).__version__
        except Exception:
            return "not installed"

    return {
        "python": platform.python_version(),
        "numpy": version("numpy"),
        "scipy": version("scipy"),
        "matplotlib": version("matplotlib"),
        "os": f"{platform.system()} {platform.release()}",
    }


def main(argv=None) -> int:
    try:  # never crash on a Windows console that cannot print a character
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        prog="verify.py",
        description="Check your step functions in student/steps.py and write a verification report.",
    )
    ap.add_argument("--steps", type=Path, default=ROOT / "student" / "steps.py",
                    help="the file to check (default: student/steps.py)")
    ap.add_argument("--info", type=Path, default=None,
                    help="student information file (default: student_info.txt next to the steps file)")
    ap.add_argument("--out", type=Path, default=ROOT / "report", help="folder for the report (default: report)")
    ap.add_argument("--ci", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    steps_path = args.steps.resolve()
    info_path = (args.info or steps_path.parent / "student_info.txt").resolve()
    print(f"verifiedmethods {UNIT_ID}: {UNIT_TITLE} (version {__version__})")

    if not steps_path.exists():
        print(f"Cannot find {steps_path}.")
        return 2
    try:
        module = load_steps(steps_path)
    except Exception as exc:  # syntax errors and import errors in the student's file
        line = getattr(exc, "lineno", None)
        where = f" (line {line})" if line else ""
        print(f"Python could not read {steps_path.name}{where}: {type(exc).__name__}: {exc}")
        print("Fix this first, then run python verify.py again.")
        return 2

    print("Running the checks (a few seconds; the first run can take longer)...")
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):  # keep the student's own print() output from flooding the summary
        results = run_all(module, str(steps_path), load_expected())
    printed = captured.getvalue().splitlines()
    if printed:
        print(f"Your code printed {len(printed)} line(s) during the checks; the first few:")
        for line in printed[:5]:
            print("    " + line[:200])

    ci = args.ci or os.environ.get("GITHUB_ACTIONS") == "true"
    meta = {
        "unit": {"id": UNIT_ID, "title": UNIT_TITLE, "version": __version__},
        "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "mode": "ci" if ci else "local",
        "mode_label": "GitHub Actions run" if ci else "local run",
        "student": read_info(info_path),
        "fingerprints": {"student_code": file_sha256(steps_path), "check_suite": suite_fingerprint()},
        "student_code": dict(zip(("imports", "unexpected"), scan_imports(steps_path))),
        "environment": environment(),
    }
    if ci:
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        meta["ci"] = {
            "repository": repo,
            "commit": os.environ.get("GITHUB_SHA", ""),
            "run_url": f"{server}/{repo}/actions/runs/{run_id}" if repo and run_id else "",
        }

    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / "verification-report.html"
    html_path.write_text(build_html(results, meta), encoding="utf-8")
    (out_dir / "verification-report.json").write_text(build_json(results, meta), encoding="utf-8")

    any_failed = False
    for r in results:
        label = f"  {r.spec.name:<14}"
        if r.status != "checked":
            print(f"{label} {r.message}")
            continue
        g = next((g for g in r.gates if g.id == SUMMARY_GATE), None)
        extra = f"   {SUMMARY_LABEL} {g.value:.6f}" if g is not None and g.value is not None else ""
        print(f"{label} {r.n_passed}/{len(r.gates)} gates passed{extra}")
        failed = [g for g in r.gates if not g.passed]
        any_failed = any_failed or bool(failed)
        messages = {g.hint or g.measured for g in failed}
        if len(failed) > 1 and len(messages) == 1:  # the same error stopped every gate: say it once
            print(f"      {', '.join(g.id for g in failed)} FAILED: {messages.pop()}")
        else:
            for g in failed:
                print(f"      {g.id} FAILED ({g.title}): {g.hint or g.measured}")
    unexpected = meta["student_code"]["unexpected"]
    if unexpected:
        print(f"Note: steps.py uses {', '.join(unexpected)}. The methods need only NumPy; "
              "your report flags this for your supervisor.")
    print(f"Report: {html_path}")
    unfilled = [k for k in ("name", "matric_number", "institution", "supervisor", "ai_use") if not meta["student"].get(k)]
    if unfilled:
        print(f"Remember to fill in student/student_info.txt (still empty: {', '.join(unfilled)}).")

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if ci and summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(f"### verifiedmethods {UNIT_ID}: {UNIT_TITLE}\n\n| Method | Result |\n|---|---|\n")
            for r in results:
                res = (f"{r.n_passed}/{len(r.gates)} gates" if r.status == "checked" else r.status)
                fh.write(f"| {r.spec.name} | {res} |\n")
            fh.write("\nDownload the full report from the run's artifacts.\n")
    return 1 if any_failed else 0
