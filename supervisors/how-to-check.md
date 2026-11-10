# Confirming a verification report

A report produced on the student's own computer could, in principle, have been
edited. The definitive check is to run the student's code yourself. You need
Python set up once, as in tutorial section 0.

1. **Look through the student's `steps.py` first.** It should be short, import
   only NumPy, and contain the three sweep functions. Be wary of anything else
   (other imports, file access, references to `vm`): the file runs on your
   computer, and code that changes the checks could make them pass falsely. The
   report lists the file's imports and warns about unexpected ones.
2. Obtain a fresh copy of the unit with the same check-suite fingerprint as
   the report. Use the versioned pilot release; keep its original zip and download SHA-256
   with each submission. Corrections will use a new version.
3. Copy the student's `student` folder into it, replacing the one there.
4. In the unit's main folder (the one that contains `verify.py`), run
   `python verify.py --strict`.
5. Compare your report with the student's: the gates should match, and so should
   the **student-code fingerprint**. Your **check-suite fingerprint** should
   match the value published for this version on the unit's page.

Alternatively, point the checks at the student's file directly:

```
python verify.py --strict --steps path/to/student/steps.py
```

Passing gives evidence about the stated test cases, not a proof for every
input or a validation of the whole project. A fingerprint identifies code;
it does not authenticate an HTML report. Your rerun confirms the results,
and the viva helps assess understanding. Allow time for setup, inspection,
the rerun and the student's explanation.
