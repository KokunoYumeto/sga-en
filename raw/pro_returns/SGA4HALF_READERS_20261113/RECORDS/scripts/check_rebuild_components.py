"""Prove the retained inputs rebuild all 22 components twice without ledger drift.

The trial copies only the declared modules and frozen inputs into an isolated
project. Its source directory links to the already verified, immutable source
payloads. All generated trial files are removed after the check. This is a
reconstruction test; it does not replace or repeat the primary visual audit.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

from compile_reader import sanitize
from edition_catalog import COMPONENTS, component_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/reproducibility"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    inventory = json.loads((ROOT / "scripts/rebuild_inputs.json").read_text())
    frozen = sorted({p for group in inventory["frozen_inputs"].values() for p in group})
    files = sorted(set(inventory["rebuild_modules"] + inventory["required_root_files"] + frozen))
    components = [component_path(c, lang).relative_to(ROOT).as_posix()
                  for c in COMPONENTS for lang in ("fr", "en")]
    expected = {p: digest(ROOT / p) for p in components}
    records = {p: digest(ROOT / p) for p in frozen}
    result = dict(result="running", component_count=len(components), frozen_input_count=len(frozen),
                  source="verified original payloads", passes=[], audit_repeated=False,
                  source_components_modified=False)
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="rebuild-trial-", dir=ROOT) as temporary:
            trial = Path(temporary)
            for relative in files:
                dest = trial / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, dest)
            (trial / "source").symlink_to(ROOT / "source", target_is_directory=True)
            previous = None
            for number in (1, 2):
                proc = subprocess.run([sys.executable, "scripts/rebuild_all.py", "--stage", "components"],
                                      cwd=trial, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      text=True, encoding="utf-8", errors="replace")
                (OUT / f"component_replay_pass{number}.txt").write_text(sanitize(proc.stdout), encoding="utf-8")
                if proc.returncode:
                    raise RuntimeError(f"Isolated component replay {number} failed; see its retained sanitized log.")
                actual = {p: digest(trial / p) for p in components}
                current_records = {p: digest(trial / p) for p in frozen}
                changed = [p for p in components if expected[p] != actual[p]]
                drift = [p for p in frozen if records[p] != current_records[p]]
                row = dict(pass_number=number, exit_code=proc.returncode,
                           component_hashes=actual, matches_reviewed_components=not changed,
                           differs_from_reviewed=changed, frozen_inputs_unchanged=not drift,
                           changed_frozen_inputs=drift,
                           matches_previous_pass=True if previous is None else previous == actual)
                result["passes"].append(row)
                if changed or drift or not row["matches_previous_pass"]:
                    raise RuntimeError("An isolated replay differs from reviewed components or changes frozen inputs.")
                previous = actual
        result["result"] = "pass"
        print(json.dumps(dict(result="pass", component_count=len(components),
                              full_replays=2, all_hashes_identical=True,
                              frozen_inputs_unchanged=True), ensure_ascii=False))
        return 0
    except (OSError, RuntimeError) as exc:
        result.update(result="fail", error=sanitize(str(exc)))
        print(sanitize(str(exc)), file=sys.stderr)
        return 1
    finally:
        (OUT / "COMPONENT_REPLAY_VALIDATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
