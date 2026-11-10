# Pilot release procedure

Students download a versioned ZIP. This unit is not distributed through PyPI;
pip installs its numerical-library dependencies.

1. Choose a new version, such as `0.1.0a1`. Update `vm/__init__.py`,
   `pyproject.toml`, `uv.lock`, `CITATION.cff` (including release date) and
   the README. Never reuse a published tag or overwrite its assets.
2. Run the public tests and the private reference/mutation suite. Build the
   bundle with `uv run python tools/build_bundle.py`. The public bundle test
   checks deterministic output, checksums and the student's pinned checker.
3. Commit and push; require the Windows/Linux CI matrix to pass. Create and
   push an annotated tag for the reviewed commit.
4. Publish a GitHub prerelease with the student ZIP, official-checker ZIP,
   `manifest.json`, `SHA256SUMS` and `check-suite-fingerprint.txt`. Use
   `gh release create` with `--prerelease --verify-tag --notes-file`; do not
   mark a pilot as a stable release or replace an existing asset.
5. The `pilot-release` workflow runs on publication. It downloads all assets,
   validates checksums, deliberately damages a checker in an extracted student
   copy, then executes the actual bundled restore/check commands. The official
   checker must replace the damaged copy; strict checking must reject the
   untouched student stubs with exit 1 and the published checker fingerprint.
6. Download the published student ZIP into a clean environment and test it
   locally with the private reference implementation. Never upload reference
   implementations to a public repository, release or workflow artifact.
7. Regenerate website example reports; pin the unit commit in the website
   workflow. Verify that the site's mirror, published release assets, examples
   and fingerprints agree before deployment.

The student workflow's SHA-256 check detects a checker archive that differs
from the pinned bytes. It does not authenticate a student-edited workflow or
prove authorship. Lecturer inspection, a fresh-copy rerun and viva questions
remain part of assessment.

For a correction, use the next alpha version and retain the previous release.
Classroom feedback should name the unit and version. A stable release and DOI
can follow after the pilot; neither is required to begin a small trial.
