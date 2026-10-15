"""Write the verification report as a self-contained HTML file and as JSON."""

from __future__ import annotations

import base64
import html
import io
import json
import math

from . import UNIT_ID, UNIT_TITLE, __version__
from .checks import FACTOR_RTOL, METHODS
from .problems import PROBLEMS

# Categorical slots 1 to 3 of the reference palette (validated all-pairs on white;
# aqua is below 3:1 contrast, so every line is also direct-labelled and the
# numbers are in the tables).
SERIES = {
    "jacobi": ("#2a78d6", "o"),
    "gauss_seidel": ("#eb6834", "s"),
    "sor": ("#1baf7a", "^"),
}
INK, INK_2, INK_3, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"

STATEMENT = (
    "This report shows that the code with the student-code fingerprint above passed the gates marked PASS, "
    "using the check suite with the check-suite fingerprint above. It does not show who wrote the code."
)
SUPERVISOR_CHECK = (
    "To confirm it, copy the student's <code>student</code> folder into your own fresh copy of this unit and run "
    "<code>python verify.py</code>. Your report should show the same gates, and the check-suite fingerprint should "
    "match the one published for this release on the unit's page at verifiedmethods.github.io."
)

CSS = """
:root { --ink:#0b0b0b; --ink2:#52514e; --ink3:#8a8984; --line:#dcdad4; --bg:#ffffff; --soft:#f6f5f2;
        --pass-bg:#e5f3e8; --pass:#1d6b33; --fail-bg:#fbe6e4; --fail:#a3271f; --na-bg:#efeeea; --na:#52514e; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
main { max-width: 920px; margin: 0 auto; padding: 28px 16px 48px; }
h1 { font-size: 26px; margin: 0 0 2px; }
h2 { font-size: 19px; margin: 34px 0 10px; padding-top: 6px; border-top: 1px solid var(--line); }
h3 { font-size: 16px; margin: 22px 0 8px; }
.sub { color: var(--ink2); margin: 0 0 18px; }
.grid { display: grid; grid-template-columns: max-content 1fr; gap: 4px 16px; background: var(--soft);
        border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; }
.grid dt { color: var(--ink2); }
.grid dd { margin: 0; overflow-wrap: anywhere; }
code, .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 4px; font-size: 14px; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--ink2); font-weight: 600; background: var(--soft); }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.wrap { overflow-x: auto; }
.badge { display: inline-block; padding: 1px 8px; border-radius: 999px; font-size: 12px; font-weight: 700;
         letter-spacing: .02em; white-space: nowrap; }
.pass { background: var(--pass-bg); color: var(--pass); }
.fail { background: var(--fail-bg); color: var(--fail); }
.na { background: var(--na-bg); color: var(--na); }
.hint { color: var(--fail); font-size: 13px; margin-top: 4px; }
.reason { color: var(--ink2); font-size: 13px; }
.note { color: var(--ink2); font-size: 13px; }
.statement { border-left: 4px solid var(--ink); background: var(--soft); padding: 10px 14px; border-radius: 0 8px 8px 0; }
figure { margin: 10px 0 18px; }
figure img { width: 100%; max-width: 760px; height: auto; display: block; }
figcaption { color: var(--ink2); font-size: 13px; margin-top: 4px; }
table.narrow { width: auto; min-width: 50%; }
td.order { color: var(--ink2); }
footer { margin-top: 36px; color: var(--ink3); font-size: 12px; }
.block { break-inside: avoid; }
@media print { body { font-size: 12px; } main { padding: 0; } h2, h3 { break-after: avoid; }
               .block, figure, table, .statement { break-inside: avoid; }
               figure img { max-width: 470px; } }
"""


def _e(s) -> str:
    return html.escape(str(s), quote=True)


def _fmt(x, digits=2) -> str:
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "n/a"
    return f"{x:.{digits}e}"


def _badge(passed) -> str:
    if passed is True:
        return '<span class="badge pass">PASS</span>'
    if passed is False:
        return '<span class="badge fail">FAIL</span>'
    return '<span class="badge na">NOT RUN</span>'


# --------------------------------------------------------------------------- plots


def _figures(results):
    """Return (history_png_b64, omega_png_b64); either may be None."""
    hist = [(r.spec, r.reported["history"]) for r in results
            if isinstance(r.reported.get("history"), dict) and "residual" in r.reported["history"]]
    scan = next((r.reported["omega_scan"] for r in results
                 if isinstance(r.reported.get("omega_scan"), dict) and "rows" in r.reported["omega_scan"]), None)
    if not hist and not scan:
        return None, None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None, None

    def style(ax, xlabel, ylabel, logy):
        if logy:
            ax.set_yscale("log")
        ax.set_xlabel(xlabel, color=INK_2)
        ax.set_ylabel(ylabel, color=INK_2)
        ax.grid(True, which="major", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(INK_3)
        ax.tick_params(colors=INK_2, labelsize=9)

    def png(fig):
        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        return base64.b64encode(buf.getvalue()).decode("ascii")

    out_hist = out_scan = None
    if hist:
        fig, ax = plt.subplots(figsize=(6.6, 4.2), dpi=150)
        ends = []
        for spec, h in hist:
            color, marker = SERIES[spec.key]
            res = [v for v in h["residual"][1:] if v > 0 and math.isfinite(v)]  # sweeps 1, 2, ...
            ks = list(range(1, len(res) + 1))
            if not res:
                continue
            label = spec.name + (f" (omega = {h['omega']:.3f})" if h.get("omega") else "")
            ax.plot(ks, res, color=color, linewidth=2, label=label, zorder=3)
            rho = h.get("rho")
            if rho and 0 < rho < 1 and len(res) > 3:
                k0 = max(1, len(res) // 2)
                ref = [res[k0 - 1] * rho ** (k - k0) / 4.0 for k in ks[k0 - 1:]]
                ax.plot(ks[k0 - 1:], ref, color=INK_3, linestyle=(0, (4, 3)), linewidth=1.0, zorder=2)
            ends.append((ks[-1], res[-1], spec.name))
        # Direct labels: the curve that ends last is labelled to its right, the others just above their ends,
        # so labels never run into a neighbouring curve.
        ends.sort()
        for i, (k, r, name) in enumerate(ends):
            last = i == len(ends) - 1
            ax.annotate(name, (k, r), xytext=(5, 0) if last else (0, 8), textcoords="offset points",
                        va="center" if last else "bottom", ha="left" if last else "center", fontsize=9, color=INK)
        style(ax, "sweep k (log scale)", "relative residual", True)
        ax.set_xscale("log")
        if ends:
            ax.set_xlim(0.8, ends[-1][0] * 4)
        ax.set_title("Convergence on L3 (1D Poisson, n = 20)", loc="left", fontsize=11, color=INK)
        ax.legend(frameon=False, fontsize=9, loc="lower left")
        out_hist = png(fig)
    if scan:
        fig, ax = plt.subplots(figsize=(6.6, 3.6), dpi=150)
        color, marker = SERIES["sor"]
        rows = [r for r in scan["rows"] if r["converged"]]
        ax.plot([r["omega"] for r in rows], [r["sweeps"] for r in rows], color=color, marker=marker,
                markersize=6, linewidth=2, markeredgecolor="white", markeredgewidth=1.0, zorder=3)
        ax.axvline(scan["omega_opt"], color=INK_3, linestyle=(0, (4, 3)), linewidth=1.0)
        ax.annotate(f"optimal omega = {scan['omega_opt']:.3f}", (scan["omega_opt"], ax.get_ylim()[1]),
                    xytext=(-4, -12), textcoords="offset points", ha="right", fontsize=8, color=INK_2)
        style(ax, "relaxation factor omega", "sweeps to residual 1e-8", False)
        ax.set_ylim(0, None)
        ax.set_title("SOR: sweeps against omega (L3, n = 20)", loc="left", fontsize=11, color=INK)
        out_scan = png(fig)
    return out_hist, out_scan


# --------------------------------------------------------------------------- HTML pieces


def _summary_table(results) -> str:
    rows = []
    for r in results:
        rho = r.reported.get("rho_L3n20")
        rho_txt = f"{rho:.6f}" if isinstance(rho, float) else ""
        if r.status == "checked":
            status = _badge(r.all_passed)
            gates = f"{r.n_passed} / {len(r.gates)}"
            g3 = next((g for g in r.gates if g.id == "G3"), None)
            factor = f"{g3.value:.6f}" if g3 is not None and g3.value is not None else "n/a"
        else:
            status = f'<span class="badge na">{_e(r.status.upper())}</span>'
            gates, factor = "", ""
        rows.append(
            f"<tr><td>{_e(r.spec.name)} <span class='note mono'>{_e(r.spec.function)}</span></td>"
            f"<td>{status}</td><td class='num'>{gates}</td><td class='num'>{rho_txt}</td><td class='num'>{factor}</td></tr>"
        )
    return (
        "<div class='wrap'><table><thead><tr><th>Method</th><th>Result</th><th class='num'>Gates passed</th>"
        "<th class='num'>rho(T) on L3</th><th class='num'>Observed factor (G3)</th></tr></thead><tbody>"
        + "".join(rows) + "</tbody></table></div>"
    )


def _gates_table(r) -> str:
    rows = []
    for g in r.gates:
        hint = f"<div class='hint'>{_e(g.hint)}</div>" if g.hint else ""
        rows.append(
            f"<tr><td class='mono'>{_e(g.id)}</td><td>{_e(g.title)}<div class='reason'>{_e(g.reason)}</div>{hint}</td>"
            f"<td>{_e(g.tolerance)}</td><td>{_e(g.measured)}</td><td>{_badge(g.passed)}</td></tr>"
        )
    return (
        "<div class='wrap'><table><thead><tr><th>#</th><th>Gate</th><th>Tolerance</th><th>Measured</th><th>Result</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def _block(title, body, note=""):
    return f"<div class='block'><h3>{title}</h3>{note}{body}</div>"


def _err_or(rep, title):
    if not isinstance(rep, dict):
        return None
    if "error" in rep and len(rep) == 1:
        return _block(title, f"<p class='hint'>{_e(rep['error'])}</p>")
    return ""


def _sweeps_table(r) -> str:
    rep = r.reported.get("sweeps_vs_n")
    title = "R1. Sweeps to reach relative residual 1e-8 on L3 (1D Poisson)"
    early = _err_or(rep, title)
    if early is None or early:
        return early or ""
    sor = r.spec.kind == "sor"
    body = "".join(
        f"<tr><td class='num'>{row['n']}</td>" + (f"<td class='num'>{row['omega']:.4f}</td>" if sor else "")
        + f"<td class='num'>{row['rho']:.6f}</td><td class='num'>{row['predicted']:.0f}</td>"
        f"<td class='num'>{row['sweeps'] if row['converged'] else str(row['sweeps']) + ' (not converged)'}</td></tr>"
        for row in rep["rows"]
    )
    head = ("<th class='num'>n</th>" + ("<th class='num'>omega (optimal)</th>" if sor else "")
            + "<th class='num'>rho(T)</th><th class='num'>prediction</th><th class='num'>sweeps</th>")
    note = ("<p class='note'>Prediction: log(1e-8)/log(rho), the sweeps for the error to fall by 1e-8 if it falls by "
            "rho per sweep; it ignores constant factors.</p>")
    return _block(title, f"<table class='narrow'><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>", note)


def _omega_table(r) -> str:
    rep = r.reported.get("omega_scan")
    title = "R2. SOR: sweeps against omega (L3, n = 20)"
    early = _err_or(rep, title)
    if early is None or early:
        return early or ""
    body = "".join(
        f"<tr><td class='num'>{row['omega']:.2f}</td><td class='num'>{row['rho']:.4f}</td>"
        f"<td class='num'>{row['sweeps'] if row['converged'] else 'not converged'}</td></tr>"
        for row in rep["rows"]
    )
    note = f"<p class='note'>Theoretical optimum: omega = {rep['omega_opt']:.4f}.</p>"
    return _block(title, "<table class='narrow'><thead><tr><th class='num'>omega</th><th class='num'>rho(T)</th>"
                         f"<th class='num'>sweeps</th></tr></thead><tbody>{body}</tbody></table>", note)


def _failures_table(r) -> str:
    rep = r.reported.get("failures")
    title = "R4. When the method fails: L5 and L6"
    early = _err_or(rep, title)
    if early is None or early:
        return early or ""
    body = "".join(
        f"<tr><td>{_e(row['problem'])}: {_e(row['title'])}</td><td class='num'>{row['rho']:.4f}</td>"
        f"<td class='num'>{row['sweeps']}</td><td class='num'>{_fmt(row['error_after'])}</td><td>{_e(row['behaviour'])}</td></tr>"
        for row in rep["rows"]
    )
    note = ("<p class='note'>Relative error after the sweeps shown (at most 50), from x = 0"
            + (f", omega = {rep['omega']}" if rep.get("omega") else "") + ".</p>")
    return _block(title, "<table><thead><tr><th>System</th><th class='num'>rho(T)</th><th class='num'>sweeps</th>"
                         f"<th class='num'>error</th><th>behaviour</th></tr></thead><tbody>{body}</tbody></table>", note)


def _residual_error_table(r) -> str:
    rep = r.reported.get("residual_vs_error")
    title = "R5. Residual against error (L3, n = 40)"
    early = _err_or(rep, title)
    if early is None or early:
        return early or ""
    body = (f"<tr><td class='num'>{rep['sweeps']}</td><td class='num'>{rep['cond']:.0f}</td>"
            f"<td class='num'>{_fmt(rep['residual'])}</td><td class='num'>{_fmt(rep['error'])}</td>"
            f"<td class='num'>{_fmt(rep['bound'])}</td></tr>")
    note = ("<p class='note'>At the stopping point: relative residual, relative error, and the bound "
            "cond(A) times the relative residual.</p>")
    return _block(title, "<table class='narrow'><thead><tr><th class='num'>sweeps</th><th class='num'>cond(A)</th>"
                         "<th class='num'>residual</th><th class='num'>error</th><th class='num'>bound</th></tr></thead>"
                         f"<tbody>{body}</tbody></table>", note)


def _method_section(r) -> str:
    head = f"<h2>{_e(r.spec.name)} <span class='note mono'>{_e(r.spec.function)}</span></h2>"
    if r.status != "checked":
        return f"<section>{head}<p>{_badge(None)} {_e(r.message)}</p></section>"
    return (
        f"<section>{head}<div class='block'><h3>Gates (must pass)</h3>{_gates_table(r)}</div>"
        "<p class='note'>Reported results below have no pass mark: interpret them in your write-up.</p>"
        f"{_sweeps_table(r)}{_omega_table(r)}{_failures_table(r)}{_residual_error_table(r)}</section>"
    )


def build_html(results, meta) -> str:
    info = meta["student"]
    fp = meta["fingerprints"]
    env = meta["environment"]
    rows = [
        ("Student", info.get("name")),
        ("Matriculation number", info.get("matric_number")),
        ("Department", info.get("department")),
        ("Institution", info.get("institution")),
        ("Supervisor", info.get("supervisor")),
        ("Run", f"{meta['generated_at']} ({meta['mode_label']})"),
    ]
    if meta.get("ci"):
        ci = meta["ci"]
        rows.append(("Repository and commit", f"{ci.get('repository', '')} @ {ci.get('commit', '')}"))
        if ci.get("run_url"):
            rows.append(("CI run", ci["run_url"]))
    code = meta.get("student_code", {"imports": [], "unexpected": []})
    rows += [
        ("Imports in steps.py", ", ".join(code["imports"]) or "none"),
        ("Student-code fingerprint", f"SHA-256 {fp['student_code']}"),
        ("Check-suite fingerprint", f"SHA-256 {fp['check_suite']}"),
        ("Environment", f"Python {env['python']}, NumPy {env['numpy']}, SciPy {env['scipy']}, "
                        f"Matplotlib {env['matplotlib']}, {env['os']}"),
    ]
    grid = "".join(
        f"<dt>{_e(k)}</dt><dd class='{'mono' if 'fingerprint' in k else ''}'>{_e(v if v else '(not given)')}</dd>"
        for k, v in rows
    )
    hist, scan = _figures(results)
    figs = ""
    if hist or scan:
        figs = "<h2>Comparing the methods</h2>"
    if hist:
        figs += (
            f"<figure><img alt='Relative residual against sweep number on L3 for each implemented method, with dashed "
            f"reference lines falling by rho(T) per sweep.' src='data:image/png;base64,{hist}'>"
            "<figcaption>R3. Each residual curve should become parallel to its dashed line, which falls by rho(T) "
            "per sweep. Numbers: table R1.</figcaption></figure>"
        )
    if scan:
        figs += (
            f"<figure><img alt='Sweeps against the relaxation factor omega for SOR on L3.' src='data:image/png;base64,{scan}'>"
            "<figcaption>R2. The number of sweeps is smallest near the theoretical optimum; numbers in table R2."
            "</figcaption></figure>"
        )
    missing = [k for k in ("name", "matric_number", "institution", "supervisor", "ai_use") if not info.get(k)]
    warn = ""
    if code["unexpected"]:
        warn += ("<p class='hint'><strong>For the supervisor:</strong> steps.py uses "
                 + _e(", ".join(code["unexpected"]))
                 + ". The methods need only NumPy. Look at the file before relying on this report: "
                 "code in steps.py runs alongside the checks.</p>")
    if missing:
        warn += ("<p class='hint'>Fill in student/student_info.txt (missing: "
                + _e(", ".join(missing)) + ") before you submit this report.</p>")
    ai = info.get("ai_use")
    title = f"Verification report: {info.get('name') or 'student'}, unit {UNIT_ID}"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(title)}</title><style>{CSS}</style></head>
<body><main>
<h1>Verification report</h1>
<p class="sub">verifiedmethods · Unit {_e(UNIT_ID)}: {_e(UNIT_TITLE)} · version {_e(__version__)}</p>
<dl class="grid">{grid}</dl>
{warn}
<h2>Summary</h2>
{_summary_table(results)}
<p class="note">A method passes when all four gates pass. Gate G3 accepts an observed convergence factor within {FACTOR_RTOL * 100:g}% of the spectral radius rho(T). Details for each method follow the statement below.</p>
{figs}
<h2>AI-use disclosure</h2>
<p>{_e(ai) if ai else '(not given)'}</p>
<h2>What this report shows</h2>
<div class="statement"><p>{_e(STATEMENT)}</p><p>{SUPERVISOR_CHECK}</p></div>
{''.join(_method_section(r) for r in results)}
<footer>Generated by <code>verify.py</code>. The same results are in <code>verification-report.json</code>.
Test systems: {'; '.join(f'{p.id} {p.title}' for p in PROBLEMS.values() if not p.id.startswith('L3n') or p.id == 'L3n20')}.</footer>
</main></body></html>
"""


def _clean(o):
    """Replace non-finite floats by None so the file is valid JSON."""
    if isinstance(o, float):
        return o if math.isfinite(o) else None
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    return o


def build_json(results, meta) -> str:
    data = dict(meta)
    data.pop("mode_label", None)
    data["results"] = [r.to_dict() for r in results]
    data["statement"] = STATEMENT
    data["methods"] = [m.key for m in METHODS]
    return json.dumps(_clean(data), indent=2, allow_nan=False, default=str)
