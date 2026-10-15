# Confirming a verification report

A report produced on the student's own computer could, in principle, have been
edited. The definitive check is to run the student's code yourself. You need
Python set up once, as in tutorial section 0.

1. **Look through the student's `steps.py` first.** It should be short, import
   only NumPy, and contain the three sweep functions. Be wary of anything else
   (other imports, file access, references to `vm`): the file runs on your
   computer, and code that changes the checks could make them pass falsely. The
   report lists the file's imports and warns about unexpected ones.
2. Download a fresh copy of the unit (the same version as on the report).
3. Copy the student's `student` folder into it, replacing the one there.
4. In the unit's main folder (the one that contains `verify.py`), run
   `python verify.py`.
4. Compare your report with the student's: the gates should match, and so should
   the **student-code fingerprint**. Your **check-suite fingerprint** should
   match the value published for this version on the unit's page.

Alternatively, point the checks at the student's file directly:

```
python verify.py --steps path/to/student/steps.py
```

This takes about two minutes. Passing the gates is strong evidence that the code
implements the method correctly; it does not show who wrote it. Use a few of the
viva questions for that.
