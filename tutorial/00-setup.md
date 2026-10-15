# 0. Setting up

> **Done unit A1 already?** You can create a new environment here in a minute
> (step 2), or reuse your A1 environment: activate it as in A1, then go to this
> unit's folder with `cd`.

You do this once. It takes about ten minutes plus download time. Steps 1 and 2
need internet access (Python itself is about 30 MB; Anaconda is about 1 GB);
after that everything runs offline. If you have no internet at home, do steps 1
and 2 at a place that has it.

**On Windows, before you start:**

- **Unzip the unit properly.** Right-click the downloaded zip file and choose
  **Extract All**. Working inside the zip without extracting it does not work.
- **Open Command Prompt in the unit's folder.** Open the extracted folder in File
  Explorer, click the address bar at the top, type `cmd` and press Enter.
  (On Windows 11, "Open in Terminal" opens PowerShell; see the table at the end
  of this section if you use it.)

## Step 1. Python

You need Python 3.10 or later.

- **Windows:** install Python from [python.org](https://www.python.org/downloads/)
  and tick **"Add python.exe to PATH"** on the first screen of the installer.
  Or install **Anaconda** (see the box below).
- **macOS:** install Python from python.org, or with Homebrew (`brew install python`).
- **Linux:** Python 3 is usually installed already.

Check it in a terminal (on Windows, Command Prompt):

| System | Command |
|---|---|
| Windows | `py --version` |
| macOS, Linux | `python3 --version` |

## Step 2. A virtual environment for this unit

A *virtual environment* is a private copy of Python for this folder, so that
installing packages cannot break anything else on your computer. Open a
terminal **in this unit's folder** (the folder that contains `verify.py`) and
run the three lines for your system.

**Windows** (Command Prompt):

```
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

**macOS and Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The second line *activates* the environment: your prompt now starts with
`(.venv)`. **Each time you open a new terminal, run the second line again.**
Once the environment is active, the command is `python` on every system.

> **Anaconda users:** skip step 2. Open the **Anaconda Prompt**, go to this
> unit's folder with `cd`, and use `python`. NumPy, SciPy and Matplotlib come
> with Anaconda.

## Step 3. Check

```
python -c "import numpy, scipy, matplotlib; print('ready')"
```

It should print `ready`.

## If something goes wrong

| What you see | Why | What to do |
|---|---|---|
| `zsh: command not found: python` (macOS, Linux) | Outside a virtual environment the command is `python3` | Activate the environment (step 2, second line) |
| `error: externally-managed-environment` | Your system's Python does not allow installing packages directly | Use the virtual environment in step 2 |
| `No module named 'numpy'` | The packages are not installed in the Python you are using | Activate the environment, then run the `pip install` line again |
| `'python' is not recognized` (Windows) | The environment is not active, or Python is not on your PATH | Activate the environment (step 2, second line). Before step 2, use `py` instead |
| Typing `python` opens the Microsoft Store (Windows) | Windows' placeholder "app alias" for Python | Install Python from python.org, or turn off the alias in Settings, Apps, Advanced app settings, App execution aliases |
| `'py' is not recognized` (Windows) | Python came from the Microsoft Store, which has no `py` command | Use `python -m venv .venv` in step 2 instead of `py -m venv .venv` |
| `running scripts is disabled on this system` (Windows PowerShell) | PowerShell blocks the activation script | Use Command Prompt instead of PowerShell |
| `ensurepip is not available` (Ubuntu, Debian) | The virtual-environment module is not installed | Run `sudo apt install python3-venv`, then step 2 again |

## Fill in your details

Open `student/student_info.txt` in a text editor (Notepad is fine) and fill in
every line. These details appear at the top of your report.

## Run the checks for the first time

With the environment active, in this unit's folder:

```
python verify.py
```

You should see:

```
verifiedmethods A2: Iterative methods for linear systems (version ...)
Running the checks (a few seconds; the first run can take longer)...
  Jacobi         jacobi_sweep is not implemented yet.
  Gauss–Seidel   gauss_seidel_sweep is not implemented yet.
  SOR            sor_sweep is not implemented yet.
Report: .../report/verification-report.html
```

That is correct: you have not written anything yet. Open the report file in
any web browser to see what it looks like. If you see a line starting
`Remember to fill in`, some of your details are still empty.

## The folders

| Folder or file | What it is | Do you edit it? |
|---|---|---|
| `student/steps.py` | Your three sweep functions | **Yes** |
| `student/student_info.txt` | Your details and AI-use disclosure | **Yes** |
| `student/CONTRIBUTION.md` | Contribution statement for your appendix | **Yes** |
| `verify.py`, `vm/` | The checks and the report generator | No |
| `tutorial/`, `briefs/` | This tutorial and the project briefs | No |
| `.venv/` | Your virtual environment (created in step 2) | No |
