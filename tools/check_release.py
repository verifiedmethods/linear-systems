"""Smoke-test published pilot assets and the actual bundled student commands.

Run on the Ubuntu student-workflow platform, normally via pilot-release.yml.
No reference implementation is needed or published by this check.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vm import UNIT_ID, UNIT_SLUG, __version__


def main():
    import yaml

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=__version__)
    version = parser.parse_args().version.removeprefix("v")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:a[0-9]+)?", version):
        parser.error("expected a pilot or stable numeric version")
    base = f"https://github.com/verifiedmethods/{UNIT_SLUG}/releases/download/v{version}/"
    names = [f"verifiedmethods-{UNIT_SLUG}-{version}.zip", f"vm-official-{version}.zip",
             "manifest.json", "check-suite-fingerprint.txt", "SHA256SUMS"]
    with tempfile.TemporaryDirectory(prefix="verifiedmethods-release-") as folder:
        folder = Path(folder)
        for name in names:
            with urlopen(Request(base + name, headers={"User-Agent": "verifiedmethods-release-check"}), timeout=60) as response:
                (folder / name).write_bytes(response.read())
        sums = {name: digest for digest, name in
                (line.split() for line in (folder / "SHA256SUMS").read_text().splitlines())}
        for name in names[:-1]:
            assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == sums[name], name
        manifest = json.loads((folder / "manifest.json").read_text())
        assert (manifest["unit"], manifest["slug"], manifest["version"]) == (UNIT_ID, UNIT_SLUG, version)
        for name, details in manifest["files"].items():
            assert details["sha256"] == sums[name]
        assert (folder / "check-suite-fingerprint.txt").read_text().split() == [version, manifest["check_suite_fingerprint"]]
        with zipfile.ZipFile(folder / names[0]) as archive:
            archive.extractall(folder / "student")
        unit = folder / "student" / f"verifiedmethods-{UNIT_SLUG}-{version}"
        workflow = yaml.safe_load((unit / ".github/workflows/verify.yml").read_text())
        steps = workflow["jobs"]["verify"]["steps"]
        restore = next(step for step in steps if step.get("name", "").startswith("Use the official checks"))
        run = next(step for step in steps if step.get("name") == "Run the checks")
        assert version in restore["name"] and "dev" not in version
        assert sums[names[1]] in restore["run"], "checker digest is not pinned"
        (unit / "verify.py").write_text("raise RuntimeError('untrusted checker was not replaced')\n")
        marker = unit / "vm/pilot_smoke_marker.txt"
        marker.write_text("must disappear when official checker is restored")
        subprocess.run(["bash", "-e", "-c", restore["run"]], cwd=unit, check=True)
        assert not marker.exists(), "old checker was not removed"
        with zipfile.ZipFile(folder / names[1]) as official:
            for name in official.namelist():
                assert (unit / name).read_bytes() == official.read(name), name
        result = subprocess.run(["bash", "-e", "-c", run["run"]], cwd=unit,
                                env={**os.environ, "GITHUB_ACTIONS": "true"})
        assert result.returncode == 1, "untouched student stubs must fail strict submission"
        report = json.loads((unit / "report/verification-report.json").read_text())
        assert report["fingerprints"]["check_suite"] == manifest["check_suite_fingerprint"]
        assert report["unit"]["version"] == version
        assert [item["status"] for item in report["results"]] == ["not implemented"] * 3
        print(f"{UNIT_ID} {version}: published checksums, official replacement and strict starter checks passed")


if __name__ == "__main__":
    main()
