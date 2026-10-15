"""Check your work for this unit and write a verification report.

Run it from a terminal in this folder:

    python verify.py

The report is written to report/verification-report.html; open it in any
web browser. You do not need to edit this file.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _setup_help(missing):
    """Explain how to install the packages, for the student's operating system."""
    windows = sys.platform.startswith("win")
    lines = [f"verify.py needs NumPy, SciPy and Matplotlib. Missing: {', '.join(missing)}."]
    if (HERE / ".venv").exists():
        lines.append("You have a .venv folder: activate it first, then run python verify.py again:")
        lines.append("    .venv\\Scripts\\activate" if windows else "    source .venv/bin/activate")
        lines.append("If they are still missing after that, run:  python -m pip install -r requirements.txt")
    else:
        lines.append("Set them up once, in this folder (tutorial section 0):")
        lines += (
            ["    py -m venv .venv", "    .venv\\Scripts\\activate"]
            if windows
            else ["    python3 -m venv .venv", "    source .venv/bin/activate"]
        )
        lines.append("    python -m pip install -r requirements.txt")
        lines.append("Then run  python verify.py  again. Anaconda users: run it from the Anaconda Prompt instead.")
    return "\n".join(lines)


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        print(f"verify.py needs Python 3.10 or later; this is Python {sys.version.split()[0]}.")
        sys.exit(2)
    missing = []
    for name in ("numpy", "scipy", "matplotlib"):
        try:
            __import__(name)
        except ImportError:
            missing.append(name)
    if missing:
        print(_setup_help(missing))
        sys.exit(2)

    sys.path.insert(0, str(HERE))
    from vm.runner import main

    sys.exit(main())
