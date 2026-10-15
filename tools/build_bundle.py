"""Build the student bundle and the official check suite into dist/.

    uv run python tools/build_bundle.py

Outputs (VERSION from vm/__init__.py):
  dist/verifiedmethods-linear-systems-VERSION.zip   offline bundle for students
  dist/vm-official-VERSION.zip               verify.py + vm/, fetched by student CI
  dist/SHA256SUMS                            checksums of both zips
  dist/check-suite-fingerprint.txt           value to publish on the unit page
"""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vm import __version__  # noqa: E402
from vm.fingerprint import suite_fingerprint  # noqa: E402

DATE = (2026, 1, 1, 0, 0, 0)  # fixed timestamps, so rebuilding gives identical zips

STUDENT_FILES = [
    "README.md", "LICENSE", "LICENSE-docs", "CITATION.cff", "requirements.txt", "verify.py",
    "student/steps.py", "student/student_info.txt", "student/CONTRIBUTION.md",
]
STUDENT_DIRS = ["vm", "tutorial", "briefs", "supervisors"]
STUDENT_GITIGNORE = "__pycache__/\n*.py[cod]\nreport/\n.venv/\n"


def _files(dirs):
    out = []
    for d in dirs:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
                out.append(p.relative_to(ROOT).as_posix())
    return out


def _add(zf: zipfile.ZipFile, arcname: str, data: bytes):
    info = zipfile.ZipInfo(arcname, DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    top = f"verifiedmethods-linear-systems-{__version__}"

    bundle = dist / f"{top}.zip"
    workflow = (ROOT / "tools" / "student-verify.yml.in").read_text(encoding="utf-8").replace("@VERSION@", __version__)
    with zipfile.ZipFile(bundle, "w") as zf:
        for rel in STUDENT_FILES + _files(STUDENT_DIRS):
            _add(zf, f"{top}/{rel}", (ROOT / rel).read_bytes())
        _add(zf, f"{top}/.github/workflows/verify.yml", workflow.encode("utf-8"))
        _add(zf, f"{top}/.gitignore", STUDENT_GITIGNORE.encode("utf-8"))

    official = dist / f"vm-official-{__version__}.zip"
    with zipfile.ZipFile(official, "w") as zf:
        for rel in ["verify.py"] + _files(["vm"]):
            _add(zf, rel, (ROOT / rel).read_bytes())

    (dist / "SHA256SUMS").write_text(
        "".join(f"{_sha256(p)}  {p.name}\n" for p in (bundle, official)), encoding="utf-8"
    )
    fp = suite_fingerprint()
    (dist / "check-suite-fingerprint.txt").write_text(f"{__version__} {fp}\n", encoding="utf-8")
    print(f"{bundle.name} ({bundle.stat().st_size // 1024} KB)")
    print(f"{official.name} ({official.stat().st_size // 1024} KB)")
    print(f"check-suite fingerprint {fp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
