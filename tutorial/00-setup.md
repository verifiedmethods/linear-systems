# 0. Setting up

> **Done unit A1 already?** You can create a new environment here in a minute
> (step 2), or reuse your A1 environment: activate it as in A1, then go to this
> unit's folder with `cd`.

Set up once, allowing time for downloads and troubleshooting. Steps 1 and 2
need internet access; afterwards the supplied code, data and generated reports
work offline. The zip does not include Python or its packages. For formatted
tutorials offline, save the web sections as PDFs while connected, or use a
Markdown reader that supports equations; the bundled tutorial files are
Markdown source.

**On Windows, before you start:**

- **Unzip the unit properly.** Right-click the downloaded zip file and choose
  **Extract All**. Working inside the zip without extracting it does not work.
- **Open Command Prompt in the unit's folder.** Open the extracted folder in File
  Explorer, click the address bar at the top, type `cmd` and press Enter.
  (On Windows 11, "Open in Terminal" opens PowerShell; see the table at the end
  of this section if you use it.)

## Step 1. Python

You need Python 3.10 or later. Maintainer CI currently tests Python 3.10–3.13;
lecturers should check the environment they intend to use for a class.

- **Windows:** follow the [official Python installation guidance](https://docs.python.org/3/using/windows.html).
  Current installations may use the Python install manager; older installers
  offer **"Add python.exe to PATH"**. Follow the instructions for your installer.
  Or use an existing Anaconda installation (see below).
- **macOS:** install Python from python.org, or with Homebrew (`brew install python`).
- **Linux:** Python 3 is usually installed already.

Check it in a terminal (on Windows, Command Prompt):

| System | Command |
|---|---|
| Windows | `py --version` |
| macOS, Linux | `python3 --version` |

## Step 2. A virtual environment for this unit

A *virtual environment* isolates this unit's Python packages from those used
by other projects. Open a
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
| `'py' is not recognized` (Windows) | The launcher or install manager is unavailable in this terminal | If `python --version` works, use `python -m venv .venv`; otherwise follow the official installation guidance above and reopen Command Prompt |
| `running scripts is disabled on this system` (Windows PowerShell) | PowerShell blocks the activation script | Use Command Prompt instead of PowerShell |
| `ensurepip is not available` (Ubuntu, Debian) | The virtual-environment module is not installed | Run `sudo apt install python3-venv`, then step 2 again |

## Fill in your details

Open `student/student_info.txt` in a text editor (Notepad is fine) and fill in
every line. These details appear at the top of your report.
Share the report through your lecturer's agreed submission route. Do not post
student identifiers in a public repository or issue.

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

## Edit, save and rerun

Open `student/steps.py` in a code editor or plain-text editor. Keep its
filename and the supplied function names. On Windows, check that the filename
has not become `steps.py.txt`; do not use a word processor.

Save your changes, then run `python verify.py` again in the terminal in the
unit's folder. Enter terminal commands at the system prompt, not at Python's
`>>>` prompt; type `exit()` to leave that prompt if necessary. Your browser
may need a refresh to show the new report.

## The folders

| Folder or file | What it is | Do you edit it? |
|---|---|---|
| `student/steps.py` | Your three sweep functions | **Yes** |
| `student/student_info.txt` | Your details and AI-use disclosure | **Yes** |
| `student/CONTRIBUTION.md` | Contribution statement for your appendix | **Yes** |
| `verify.py`, `vm/` | The checks and the report generator | No |
| `tutorial/`, `briefs/` | This tutorial and the project briefs | No |
| `.venv/` | Your virtual environment (created in step 2) | No |
