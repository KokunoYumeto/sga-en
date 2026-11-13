"""Rebuild the eight readers and their evidence from frozen reviewed inputs.

Default: verify/unpack the four original archives, rebuild all 22 components,
refresh the glossary, assemble, compile each reader three times, export the
records/diffs, and run the strict independent final gate. Audit recorders are
never invoked. --dry-run prints the exact project-relative command sequence.
--stage reruns one named stage and does not claim a complete rebuild.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shlex
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/reproducibility"
STAGES = ["inputs", "components", "glossary", "assemble", "compile", "export", "verify"]
READERS = {
    "FR": ["SGA4HALF_FR_diplomatique", "SGA4HALF_FR_corrige_apparat",
           "SGA4HALF_FR_texte_de_lecture", "SGA4HALF_FR_annotated_master"],
    "EN": ["SGA4HALF_EN_diplomatic", "SGA4HALF_EN_corrected_apparatus",
           "SGA4HALF_EN_reading", "SGA4HALF_EN_annotated_master"],
}


def commands(passes=3, privacy_roots=()):
    result = {
        "inputs": [["scripts/unpack_inputs.py"]],
        "components": [
            ["scripts/rebuild_opening.py"],
            ["scripts/build_arcata_fr.py"],
            ["scripts/build_arcata_en.py"],
            ["scripts/finalize_arcata_records.py"],
            ["scripts/verify_arcata.py"],
            ["work/rapport_cycle/review_arcata_noedit.py"],
            # The first check supplies the historical cohort's table. The second
            # incorporates the freshly rechecked 147 exact English witnesses.
            ["scripts/verify_arcata.py"],
            ["work/rapport_cycle/build_components.py", "2", "3", "4", "5"],
            ["work/rapport_cycle/validate_components.py"],
            ["work/sommes/build_components.py"],
            ["work/sommes/finish_components.py"],
            ["work/sommes/complete_alignment.py"],
            ["work/sommes/validate_component.py"],
            ["work/finitude_verdier/build_components.py"],
            ["work/finitude_verdier/check_coverage.py"],
        ],
        "glossary": [
            ["work/glossary/build_glossary.py"],
            ["work/glossary/write_glossary_report.py"],
        ],
        "assemble": [
            ["scripts/edition_tex.py"],
            ["scripts/assemble_readers.py"],
        ],
        "compile": [["scripts/compile_reader.py", f"deliverables/{language}/{reader}.tex", str(passes)]
                    for language, names in READERS.items() for reader in names],
        "export": [
            ["scripts/export_records.py"],
            ["scripts/export_changes.py"],
        ],
        "verify": [
            ["work/verification/verify_arcata_own.py"],
            ["work/verification/verify_final.py", "--strict"]
            + [arg for root in privacy_roots for arg in ("--privacy-root", root)],
        ],
    }
    return result


def safe_relative(value):
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in value.split("/") or "\\" in value or ":" in value:
        raise ValueError("Additional privacy roots must be project-relative paths.")
    return p.as_posix()


def preflight(selected, plan):
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required; the reviewed build used Python 3.12.14.")
    required = {cmd[0] for stage in selected for cmd in plan[stage]}
    missing = sorted(path for path in required if not (ROOT / path).is_file())
    if missing:
        raise RuntimeError("Missing rebuild scripts: " + ", ".join(missing))
    if "compile" in selected:
        missing_tools = [name for name in ("pdflatex", "pdftex", "kpsewhich") if not shutil.which(name)]
        if missing_tools:
            raise RuntimeError("Missing TeX commands: " + ", ".join(missing_tools))
    if "verify" in selected:
        if importlib.util.find_spec("fitz") is None:
            raise RuntimeError("PyMuPDF is required by the independent PDF verifier; see requirements-rebuild.txt.")
        import fitz
        if not hasattr(fitz.Document, "resolve_names"):
            raise RuntimeError("This PyMuPDF version cannot inspect named PDF destinations; use the recorded version.")
    inventory = ROOT / "scripts/rebuild_inputs.json"
    if not inventory.is_file():
        raise RuntimeError("Missing scripts/rebuild_inputs.json.")
    retained = json.loads(inventory.read_text(encoding="utf-8"))
    if any(s in selected for s in ("components", "glossary", "assemble", "export", "verify")):
        missing = sorted(path for group in retained["frozen_inputs"].values() for path in group
                         if not (ROOT / path).is_file())
        if missing:
            raise RuntimeError("Missing frozen reviewed inputs: " + ", ".join(missing))


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def gate(script):
    """Catch legacy builders which record failures but do not return failure."""
    if script in ("scripts/build_arcata_fr.py", "scripts/build_arcata_en.py"):
        lang = "fr" if script.endswith("_fr.py") else "en"
        bad = [r for r in read_json(f"work/arcata/{lang}_build.json")
               if any(word in r.get("status", "").lower() for word in ("unmatched", "ambiguous", "failed"))]
        if bad:
            raise RuntimeError(f"Arcata {lang}: {len(bad)} source operations did not apply uniquely.")
    elif script == "work/rapport_cycle/build_components.py":
        bad = [r for part in range(2, 6) for lang in ("fr", "en")
               for r in read_json(f"work/rapport_cycle/records/{lang}_build_{part}.json")
               if any(word in r.get("status", "").lower() for word in ("unmatched", "ambiguous", "failed"))]
        if bad:
            raise RuntimeError(f"Parts 2–5: {len(bad)} source operations did not apply uniquely.")
    elif script == "work/rapport_cycle/validate_components.py":
        if read_json("work/rapport_cycle/records/accepted_fix_coverage_status.json")["unresolved"]:
            raise RuntimeError("Parts 2–5 have unresolved coverage rows.")
    elif script == "work/sommes/finish_components.py":
        if read_json("work/sommes/assembly_failures.json"):
            raise RuntimeError("Part 6 has unresolved source operations.")
    elif script == "work/sommes/validate_component.py":
        if read_json("work/sommes/coverage_unresolved.json"):
            raise RuntimeError("Part 6 has unresolved coverage rows.")
    elif script == "work/finitude_verdier/build_components.py":
        if any(r["status"] != "applied" for r in read_json("work/finitude_verdier/build_report.json")):
            raise RuntimeError("Parts 7–8/Erratum have unresolved source operations.")
    elif script == "work/finitude_verdier/check_coverage.py":
        if read_json("work/finitude_verdier/accepted_fix_coverage_status.json")["unresolved_count"]:
            raise RuntimeError("Parts 7–8/Erratum have unresolved coverage rows.")


def ensure_output_directories(selected):
    OUT.mkdir(parents=True, exist_ok=True)
    if "components" in selected:
        for owner in ("arcata", "rapport_cycle", "sommes", "finitude_verdier"):
            for child in ("fr", "en", "records"):
                (ROOT / "work" / owner / child).mkdir(parents=True, exist_ok=True)
    for relative in ("work/common", "work/build", "work/records", "deliverables/FR", "deliverables/EN"):
        (ROOT / relative).mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["all"] + STAGES, default="all",
                        help="Run all stages, or rerun one stage without claiming a complete rebuild")
    parser.add_argument("--passes", type=int, default=3, help="pdfLaTeX passes per reader (at least 2; default 3)")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing or writing files")
    parser.add_argument("--privacy-root", action="append", default=[],
                        help="Additional project-relative staged package to inspect in the final gate; repeatable")
    args = parser.parse_args()
    if args.passes < 2:
        parser.error("At least two PDF passes are needed for references and margin positions.")
    try:
        roots = [safe_relative(p) for p in args.privacy_root]
    except ValueError as exc:
        parser.error(str(exc))
    plan = commands(args.passes, roots)
    selected = STAGES if args.stage == "all" else [args.stage]
    if args.dry_run:
        for stage in selected:
            print("# " + stage)
            for cmd in plan[stage]:
                print(shlex.join(["python3"] + cmd))
        return 0
    # Imported only for an actual run: compile_reader initializes its local
    # runtime directories. --dry-run therefore has no filesystem side effects.
    from compile_reader import sanitize
    history = []
    report = dict(requested_stage=args.stage, stages=selected, pdf_passes=args.passes,
                  complete_rebuild=False, result="running", commands=history,
                  no_append_only_audit_recorders=True)
    try:
        preflight(selected, plan)
        ensure_output_directories(selected)
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env.pop("PYTHONOPTIMIZE", None)  # Assertion-based validation must run.
        number = 0
        for stage in selected:
            for cmd in plan[stage]:
                number += 1
                display = shlex.join(["python3"] + cmd)
                print(f"[{stage}] {display}", flush=True)
                start = time.monotonic()
                proc = subprocess.run([sys.executable] + cmd, cwd=ROOT, env=env,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                      encoding="utf-8", errors="replace")
                output = sanitize(proc.stdout)
                logfile = OUT / f"step_{number:02d}_{stage}_{Path(cmd[0]).stem}.txt"
                logfile.write_text(output, encoding="utf-8")
                if output:
                    print(output, end="" if output.endswith("\n") else "\n", flush=True)
                history.append(dict(stage=stage, command=["python3"] + cmd, exit_code=proc.returncode,
                                    seconds=round(time.monotonic() - start, 2),
                                    log=logfile.relative_to(ROOT).as_posix()))
                if proc.returncode:
                    raise RuntimeError(f"Command failed with exit code {proc.returncode}: {display}")
                gate(cmd[0])
        report.update(result="pass", complete_rebuild=args.stage == "all")
        print("Complete rebuild and strict verification passed." if args.stage == "all"
              else f"Stage {args.stage} passed; this was not a complete rebuild.")
        return 0
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        report.update(result="fail", error=sanitize(str(exc)))
        print("Rebuild stopped: " + sanitize(str(exc)), file=sys.stderr)
        return 1
    finally:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "REBUILD_RESULT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
