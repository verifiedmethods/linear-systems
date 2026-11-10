"""Regression checks for source provenance and submission completeness."""

import hashlib
import json
import os
import py_compile

import pytest

from vm import runner


def test_loader_executes_current_source_despite_stale_bytecode(tmp_path):
    path = tmp_path / "steps.py"
    path.write_bytes(b'VALUE = "old"\n')
    stamp = 1_900_000_000
    os.utime(path, (stamp, stamp))
    py_compile.compile(str(path), doraise=True)
    path.write_bytes(b'VALUE = "new"\n')
    os.utime(path, (stamp, stamp))

    assert runner.load_steps(path).VALUE == "new"


def test_report_hashes_and_scans_the_executed_snapshot(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    path = tmp_path / "steps.py"
    source = b"import math\r\n"
    path.write_bytes(source)
    original_loader = runner.load_steps

    def load_then_edit(path, source=None):
        module = original_loader(path, source)
        path.write_bytes(b"import sys\n")
        return module

    monkeypatch.setattr(runner, "load_steps", load_then_edit)
    out = tmp_path / "report"
    assert runner.main(["--steps", str(path), "--out", str(out)]) == 0
    report = json.loads((out / "verification-report.json").read_text())
    assert report["fingerprints"]["student_code"] == hashlib.sha256(source.replace(b"\r\n", b"\n")).hexdigest()
    assert report["student_code"] == {"imports": ["math"], "unexpected": []}
    assert path.read_bytes() == b"import sys\n"


def test_loader_keeps_the_students_annotation_semantics(tmp_path):
    path = tmp_path / "steps.py"
    path.write_text("def step(x: int) -> int:\n    return x\n")
    assert runner.load_steps(path).step.__annotations__ == {"x": int, "return": int}


@pytest.mark.parametrize("mode", ["--strict", "--ci", "actions_environment"])
@pytest.mark.parametrize("submission", ["missing", "stubs"])
def test_submission_modes_reject_incomplete_work(root, tmp_path, monkeypatch, mode, submission):
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    path = tmp_path / "steps.py"
    if submission == "missing":
        path.write_text("# No methods yet.\n")
    else:
        path.write_bytes((root / "student" / "steps.py").read_bytes())
    args = ["--steps", str(path), "--out", str(tmp_path / "report")]
    if mode == "actions_environment":
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
    else:
        args.append(mode)

    assert runner.main(args) == 1
    report = json.loads((tmp_path / "report" / "verification-report.json").read_text())
    expected = "missing" if submission == "missing" else "not implemented"
    assert [r["status"] for r in report["results"]] == [expected] * 3
