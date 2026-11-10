import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


def test_student_workflow_pins_the_official_archive_and_bundle_is_repeatable(tmp_path):
    root = Path(__file__).resolve().parents[1]
    copy = tmp_path / "unit"
    shutil.copytree(root, copy, ignore=shutil.ignore_patterns(
        ".git", ".venv", "dist", "report", "__pycache__", ".pytest_cache"))
    command = [sys.executable, str(copy / "tools/build_bundle.py")]
    subprocess.run(command, check=True, capture_output=True)
    dist = copy / "dist"
    manifest = json.loads((dist / "manifest.json").read_text())
    sums = {name: digest for digest, name in
            (line.split() for line in (dist / "SHA256SUMS").read_text().splitlines())}
    for name, digest in sums.items():
        assert hashlib.sha256((dist / name).read_bytes()).hexdigest() == digest
    student = next(dist.glob("verifiedmethods-*.zip"))
    official = next(dist.glob("vm-official-*.zip"))
    with zipfile.ZipFile(student) as archive:
        names = archive.namelist()
        workflow = archive.read(next(n for n in names if n.endswith("/.github/workflows/verify.yml"))).decode()
        assert "@VERSION@" not in workflow and "@CHECKER_SHA256@" not in workflow
        assert manifest["files"][official.name]["sha256"] in workflow
        assert "sha256sum --check -" in workflow
        assert not any("reference.py" in n or "/tests/" in n for n in names)
    with zipfile.ZipFile(official) as archive:
        assert "verify.py" in archive.namelist()
        assert all(n == "verify.py" or n.startswith("vm/") for n in archive.namelist())
    before = {p.name: p.read_bytes() for p in dist.iterdir() if p.is_file()}
    subprocess.run(command, check=True, capture_output=True)
    assert before == {p.name: p.read_bytes() for p in dist.iterdir() if p.is_file()}
