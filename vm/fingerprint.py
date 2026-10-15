"""Fingerprints (SHA-256) of the student's code and of the check suite.

Standard library only, so the site build can compute the published value
without NumPy.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

VM_DIR = Path(__file__).resolve().parent
ROOT = VM_DIR.parent


def file_sha256(path: Path) -> str:
    """SHA-256 of a text file with line endings normalised, so Windows and Linux copies agree."""
    data = Path(path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def suite_fingerprint(vm_dir: Path = VM_DIR, verify_script: Path = ROOT / "verify.py") -> str:
    """One hash over every file of the check suite (vm/*.py, vm/expected.json, verify.py)."""
    files = sorted(vm_dir.glob("*.py")) + [vm_dir / "expected.json"]
    if verify_script.exists():
        files.append(verify_script)
    h = hashlib.sha256()
    for p in files:
        h.update(p.name.encode("utf-8") + b"\0" + file_sha256(p).encode("ascii") + b"\n")
    return h.hexdigest()
