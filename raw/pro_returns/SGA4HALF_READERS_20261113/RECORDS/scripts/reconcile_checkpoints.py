"""Account for every checkpoint member against the final packaging map.

Current destinations come from package_readers.collect(); operational exclusions
come from its excluded() policy. Changed and excluded text receives a complete
unified diff after both required privacy sanitizers. Binary readers are mapped
by their exact old and final SHA-256 hashes. No checkpoint or source is changed.

Run after the final source, reports, README and checkpoint index are stable.
--check-current rechecks the saved destination hashes without writing anything.
--check-packaged checks those hashes and all retained diffs inside the three
packed final ZIPs, also without writing anything.
"""
from __future__ import annotations

import argparse
import collections
import csv
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import zipfile

from compile_reader import sanitize
from package_readers import ARCHIVES, TEXT, collect, excluded

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/records"
DIFFS = ROOT / "work/checkpoint_diffs"
TABLE = OUT / "CHECKPOINT_RECONCILIATION.tsv"
REPORT = OUT / "CHECKPOINT_RECONCILIATION_REPORT.json"
spec = importlib.util.spec_from_file_location("checkpoint_final_privacy", ROOT / "work/verification/verify_final.py")
privacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(privacy)

ALIASES = {"work/reproducibility/BUILD_SUPPORT.md": "work/reproducibility/REBUILD.md"}
METADATA = {
    "CHECKPOINT_STATUS.json": (
        "Checkpoint-only progress counts and milestone. Its archive identity and milestone remain in CHECKPOINT_INDEX.tsv; final counts are in the final verification. The complete sanitized old text remains in the deletion diff.",
        "work/records/CHECKPOINT_INDEX.tsv"),
    "CHECKPOINT_README.md": (
        "Checkpoint-only work-in-progress notice. The completed edition README supersedes that notice; the complete sanitized old text remains in the deletion diff.",
        "work/records/README.md"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean(value):
    return privacy.clean(sanitize(str(value)))


def safe_label(value):
    return clean(value).replace("\r", "\\r").replace("\n", "\\n")


def privacy_clear(value):
    return not privacy.LOCAL_PATH.search(value) and not privacy.EMAIL.search(value)


def destinations():
    direct = {}
    by_source = collections.defaultdict(list)
    for group, members in collect().items():
        for member, path in members.items():
            item = dict(archive=ARCHIVES[group], member=member, path=path)
            direct[(item["archive"], member)] = item
            by_source[path.relative_to(ROOT).as_posix()].append(item)
    chosen = {}
    for source, items in by_source.items():
        # Prefer the canonical project-relative path over a quick-access alias.
        chosen[source] = sorted(items, key=lambda i: (i["member"] != source, i["archive"], i["member"]))[0]
    return direct, chosen


def unified(old, new, old_label, new_label):
    parts = difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                 fromfile=old_label, tofile=new_label, n=3)
    result = []
    for line in parts:
        if line.endswith("\n"):
            result.append(line)
        else:
            result.extend([line + "\n", "\\ No newline at end of file\n"])
    return "".join(result)


def apply_unified(old, patch):
    """Independently apply generated hunks, including unterminated final lines."""
    if not patch:
        return old, 0, 0, 0
    lines = patch.splitlines(keepends=True)
    if len(lines) < 2 or not lines[0].startswith("--- ") or not lines[1].startswith("+++ "):
        raise ValueError("Invalid unified-diff headers.")
    hunks = []
    for line in lines[2:]:
        if line.startswith("@@ "):
            m = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?:[^\n]*)\n?", line)
            if not m:
                raise ValueError("Invalid unified-diff hunk header.")
            a, count_a, b, count_b = m.groups()
            hunks.append(dict(a=int(a), count_a=int(count_a or 1), b=int(b),
                              count_b=int(count_b or 1), operations=[]))
        elif line.startswith("\\ No newline at end of file"):
            if not hunks or not hunks[-1]["operations"]:
                raise ValueError("Detached final-newline note.")
            sign, text = hunks[-1]["operations"][-1]
            if not text.endswith("\n"):
                raise ValueError("Invalid final-newline note.")
            hunks[-1]["operations"][-1] = (sign, text[:-1])
        elif line[:1] in (" ", "+", "-") and hunks:
            hunks[-1]["operations"].append((line[0], line[1:]))
        else:
            raise ValueError("Invalid unified-diff operation.")
    source = old.splitlines(keepends=True)
    output = []
    cursor = 0
    deleted = inserted = 0
    for hunk in hunks:
        start = hunk["a"] if hunk["count_a"] == 0 else hunk["a"] - 1
        if start < cursor:
            raise ValueError("Overlapping unified-diff hunks.")
        output.extend(source[cursor:start])
        cursor = start
        consumed = produced = 0
        expected_new_start = hunk["b"] if hunk["count_b"] == 0 else hunk["b"] - 1
        if len(output) != expected_new_start:
            raise ValueError("Unified-diff new-line offset disagrees.")
        for sign, text in hunk["operations"]:
            if sign in (" ", "-"):
                if cursor >= len(source) or source[cursor] != text:
                    raise ValueError("Unified-diff deletion or context does not match the old text.")
                cursor += 1
                consumed += 1
            if sign in (" ", "+"):
                output.append(text)
                produced += 1
            deleted += sign == "-"
            inserted += sign == "+"
        if consumed != hunk["count_a"] or produced != hunk["count_b"]:
            raise ValueError("Unified-diff line counts disagree.")
    output.extend(source[cursor:])
    return "".join(output), deleted, inserted, len(hunks)


def diff_record(old_data, new_data, member, target, cache):
    old = old_data.decode("utf-8")
    new = new_data.decode("utf-8")
    old_clean = clean(old)
    new_clean = clean(new)
    identity = (digest(old_data), digest(new_data), member, target)
    if identity in cache:
        return cache[identity]
    patch = unified(old_clean, new_clean, "checkpoint/" + safe_label(member), safe_label(target))
    reconstructed, deleted, inserted, hunks = apply_unified(old_clean, patch)
    if reconstructed != new_clean:
        raise ValueError("A sanitized unified diff did not reconstruct its destination exactly.")
    if not privacy_clear(patch):
        raise ValueError("A sanitized diff still contains a prohibited path or address.")
    filename = (identity[0][:20] + "_" + identity[1][:20] + "_"
                + digest((member + "\0" + target).encode())[:12] + ".diff")
    path = DIFFS / filename
    payload = patch.encode("utf-8")
    path.write_bytes(payload)
    record = dict(diff_path=path.relative_to(ROOT).as_posix(), diff_sha256=digest(payload),
                  diff_bytes=len(payload), diff_hunks=hunks, deleted_lines=deleted, inserted_lines=inserted,
                  old_sanitized_sha256=digest(old_clean.encode()),
                  new_sanitized_sha256=digest(new_clean.encode()),
                  old_privacy_redacted=old_clean != old, new_privacy_redacted=new_clean != new,
                  sanitized_readings_equal=old_clean == new_clean, diff_reconstruction_passed=True)
    cache[identity] = record
    return record


def checkpoint_index():
    path = OUT / "CHECKPOINT_INDEX.tsv"
    if not path.is_file():
        raise ValueError("CHECKPOINT_INDEX.tsv must be finalized before reconciliation.")
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    return {r["filename"]: r for r in rows}


def authoritative(minimum=16):
    checkpoints = sorted((ROOT / "output").glob("SGA4HALF_READERS_checkpoint_*.zip"))
    if len(checkpoints) < minimum:
        raise ValueError(f"Expected at least {minimum} completed checkpoints before reconciliation.")
    index = checkpoint_index()
    _, targets = destinations()
    OUT.mkdir(parents=True, exist_ok=True)
    DIFFS.mkdir(parents=True, exist_ok=True)
    current_cache = {}
    diff_cache = {}
    rows = []
    summaries = []
    unresolved = []

    def current(item):
        name = item["path"].relative_to(ROOT).as_posix()
        if name not in current_cache:
            data = item["path"].read_bytes()
            current_cache[name] = dict(data=data, sha256=digest(data), bytes=len(data))
        return current_cache[name]

    for checkpoint in checkpoints:
        number = int(checkpoint.stem.rsplit("_", 1)[1])
        archive_sha = file_digest(checkpoint)
        registered = index.get(checkpoint.name)
        if not registered or registered["sha256"] != archive_sha or int(registered["bytes"]) != checkpoint.stat().st_size:
            raise ValueError("A checkpoint does not match its finalized index identity: " + checkpoint.name)
        if number in (7, 8) and "unpublished" not in registered["status"]:
            raise ValueError("Checkpoint 07/08 must remain explicitly unpublished privacy-rejected candidates.")
        start = len(rows)
        with zipfile.ZipFile(checkpoint) as archive:
            infos = archive.infolist()
            if len({i.filename for i in infos}) != len(infos):
                raise ValueError("Duplicate member names in a checkpoint: " + checkpoint.name)
            for member_number, info in enumerate(infos, 1):
                member = info.filename
                old_data = archive.read(info)  # Reading to EOF verifies the ZIP CRC.
                old_sha = digest(old_data)
                row = dict(checkpoint_number=number, checkpoint_archive=checkpoint.name,
                           checkpoint_archive_sha256=archive_sha,
                           checkpoint_publication_status=registered["status"], member_number=member_number,
                           checkpoint_member=safe_label(member), checkpoint_member_path_sha256=digest(member.encode()),
                           checkpoint_bytes=len(old_data), checkpoint_sha256=old_sha, disposition="unresolved",
                           final_archive="", final_path="", final_bytes="", final_sha256="", reason="",
                           replacement_archive="", replacement_path="", replacement_sha256="",
                           diff_path="", diff_sha256="", diff_bytes="", diff_hunks="", deleted_lines="", inserted_lines="",
                           old_sanitized_sha256="", new_sanitized_sha256="", old_privacy_redacted=False,
                           new_privacy_redacted=False, sanitized_readings_equal="", diff_reconstruction_passed="")
                destination_name = ALIASES.get(member, member)
                item = targets.get(destination_name)
                if item:
                    now = current(item)
                    row.update(final_archive=item["archive"], final_path=item["member"],
                               final_bytes=now["bytes"], final_sha256=now["sha256"])
                    if old_sha == now["sha256"]:
                        row.update(disposition="retained hash-identical",
                                   reason="The exact checkpoint bytes are selected for the final archive."
                                   + (" The reviewed build guide was renamed to REBUILD.md." if member in ALIASES else ""))
                    elif Path(member).suffix.lower() in TEXT and Path(destination_name).suffix.lower() in TEXT:
                        row.update(disposition="superseded text", reason="The current reviewed/generated text supersedes this checkpoint version; the full sanitized unified diff accounts for every insertion and deletion.")
                        row.update(diff_record(old_data, now["data"], member, item["archive"] + "/" + item["member"], diff_cache))
                        if row["sanitized_readings_equal"]:
                            row["reason"] = "The raw hashes differ, but the two readings are identical after the required privacy redactions; the empty unified diff records that equality."
                    else:
                        row.update(disposition="superseded binary",
                                   reason="The final compiled PDF replaces this checkpoint PDF; both exact binary hashes and the final reader archive destination are recorded."
                                   if Path(member).suffix.lower() == ".pdf" else
                                   "The current binary replaces this checkpoint member; exact old/final hashes and destination are recorded.")
                else:
                    policy = excluded(member)
                    replacement = ""
                    if member in METADATA:
                        policy, replacement = METADATA[member]
                    elif policy and ("layout_review" in Path(member).parts or Path(member).name.startswith("layout_trial")):
                        replacement = "work/rapport_cycle/layout_review/FINAL_LAYOUT_VALIDATION.json"
                    elif info.is_dir():
                        policy = "ZIP directory entry only; final archive member paths recreate the directory structure."
                    if policy:
                        row.update(disposition="excluded with reason", reason=policy)
                        if replacement in targets:
                            item = targets[replacement]
                            now = current(item)
                            row.update(replacement_archive=item["archive"], replacement_path=item["member"], replacement_sha256=now["sha256"])
                        if Path(member).suffix.lower() in TEXT:
                            row.update(diff_record(old_data, b"", member, "excluded/" + member, diff_cache))
                    else:
                        row["reason"] = "No current retained destination, explicit rename, or specific exclusion policy exists."
                        unresolved.append(dict(checkpoint=checkpoint.name, member=safe_label(member)))
                rows.append(row)
        counts = collections.Counter(r["disposition"] for r in rows[start:])
        summaries.append(dict(number=number, archive=checkpoint.name, bytes=checkpoint.stat().st_size,
                              sha256=archive_sha, publication_status=registered["status"],
                              member_count=len(rows) - start, dispositions=dict(counts),
                              zip_crc_checked=True, matches_checkpoint_index=True))
        print(json.dumps(dict(checkpoint=number, members=len(rows) - start, dispositions=dict(counts)), ensure_ascii=False), flush=True)

    # A current file must not change between mapping and the saved snapshot.
    drift = [name for name, value in current_cache.items() if file_digest(ROOT / name) != value["sha256"]]
    if drift:
        raise ValueError("Current package inputs changed during reconciliation; rerun after the final snapshot is stable.")
    all_text = json.dumps(rows, ensure_ascii=False)
    if not privacy_clear(all_text):
        raise ValueError("Reconciliation metadata failed the final privacy patterns.")
    with TABLE.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts = collections.Counter(r["disposition"] for r in rows)
    used_diffs = {r["diff_path"]: {k: r[k] for k in ("diff_path", "diff_sha256", "diff_bytes", "diff_hunks", "deleted_lines", "inserted_lines", "old_sanitized_sha256", "new_sanitized_sha256", "diff_reconstruction_passed")}
                  for r in rows if r["diff_path"]}
    for name, item in used_diffs.items():
        item["member_rows"] = sum(r["diff_path"] == name for r in rows)
    (DIFFS / "INDEX.json").write_text(json.dumps(list(used_diffs.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = dict(result="pass" if not unresolved else "fail", checkpoint_count=len(checkpoints),
                  member_rows=len(rows), dispositions=dict(counts), unresolved=unresolved,
                  unique_sanitized_diffs=len(used_diffs), all_saved_diffs_reconstruct=True,
                  changed_or_excluded_text_rows=sum(bool(r["diff_path"]) for r in rows),
                  old_text_rows_with_privacy_redactions=sum(bool(r["old_privacy_redacted"]) for r in rows),
                  privacy_rejected_candidates=[7, 8], candidate_archives_republished=False,
                  current_destination_hashes_rechecked=True, final_zip_contents_checked=False,
                  current_mapping="scripts/package_readers.py collect()/excluded()",
                  sanitizers=["scripts/compile_reader.py sanitize", "work/verification/verify_final.py clean"],
                  privacy_checked=True, checkpoints=summaries,
                  final_archives=[ARCHIVES[k] for k in ("FR", "EN", "RECORDS")],
                  notes=["Every ZIP member has one table row, including unpublished candidates 07 and 08.",
                         "Original checkpoint archives and working source files were not modified.",
                         "Text diffs reconstruct the exact privacy-sanitized readings; private original tokens are represented only by raw content hashes.",
                         "Excluded textual trials and progress metadata have complete deletion diffs rather than an unrecorded disappearance.",
                         "Repeated member versions share content-addressed diff files.",
                         "Run --check-current after any final report update, and --check-packaged after final ZIP creation."])
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    explanation = ("# Checkpoint reconciliation\n\n"
                   + f"All {len(checkpoints)} immutable checkpoint archives are accounted for in {len(rows)} member rows. "
                   + f"The table has {len(unresolved)} unresolved members.\n\n"
                   + "| Disposition | Member rows |\n|---|---:|\n"
                   + "".join(f"| {name} | {count} |\n" for name, count in sorted(counts.items()))
                   + f"\nThe {len(used_diffs)} distinct unified diffs in `work/checkpoint_diffs` cover changed text and complete textual exclusions. Each diff was independently applied to its old sanitized reading and reconstructed its new reading exactly. The table gives both raw SHA-256 hashes, sanitized-reading hashes, changed-line counts, and final archive destinations. Repeated versions share the same diff.\n\n"
                   + "Checkpoints 07 and 08 are unpublished candidates rejected by privacy preflight. They remain represented by archive/member hashes and sanitized differences; their original bytes are not copied into the final package. Both the compile-log sanitizer and the final verifier’s privacy cleaner were applied before any old text was written to a diff.\n\n"
                   + "Retained binary readers map to the final French or English PDF by exact hashes. Temporary layout trials are explicitly excluded in favor of the final readers and retained layout validation. Checkpoint-only progress metadata is replaced by the final index and README, while its complete sanitized wording remains in deletion diffs.\n\n"
                   + "This record describes the stable current files selected by the packaging map. After packing, `python3 scripts/reconcile_checkpoints.py --check-packaged` verifies all named destinations and diff hashes inside the three final ZIPs without changing the package.\n")
    (OUT / "CHECKPOINT_RECONCILIATION.md").write_text(explanation, encoding="utf-8")
    return report


def check_saved(packaged=False):
    with TABLE.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    targets = {}
    for row in rows:
        if row["disposition"] == "unresolved":
            raise ValueError("The saved table contains an unresolved member.")
        for prefix in ("final", "replacement"):
            if row[prefix + "_archive"]:
                key = (row[prefix + "_archive"], row[prefix + "_path"])
                expected = row[prefix + "_sha256"]
                if key in targets and targets[key] != expected:
                    raise ValueError("The saved table has conflicting current destination hashes.")
                targets[key] = expected
        if row["diff_path"]:
            targets[(ARCHIVES["RECORDS"], row["diff_path"])] = row["diff_sha256"]
    for checkpoint in report["checkpoints"]:
        path = ROOT / "output" / checkpoint["archive"]
        if not path.exists() or file_digest(path) != checkpoint["sha256"]:
            raise ValueError("An original checkpoint is unavailable or changed: " + checkpoint["archive"])
    archives = {}
    try:
        if packaged:
            archives = {name: zipfile.ZipFile(ROOT / "output" / name) for name in ARCHIVES.values()}
            for (archive, member), expected in targets.items():
                if digest(archives[archive].read(member)) != expected:
                    raise ValueError("A packed destination differs from its reconciliation hash: " + safe_label(member))
        else:
            direct, _ = destinations()
            for key, expected in targets.items():
                if key not in direct or file_digest(direct[key]["path"]) != expected:
                    raise ValueError("A current destination differs from its reconciliation hash: " + safe_label(key[1]))
    finally:
        for archive in archives.values():
            archive.close()
    return dict(result="pass", mode="packed archives" if packaged else "current packaging map",
                checkpoints_verified=len(report["checkpoints"]), member_rows=len(rows),
                distinct_destinations_and_diffs_verified=len(targets), unresolved_members=0,
                files_modified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum-checkpoints", type=int, default=16)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check-current", action="store_true")
    group.add_argument("--check-packaged", action="store_true")
    args = parser.parse_args()
    try:
        result = check_saved(args.check_packaged) if args.check_current or args.check_packaged else authoritative(args.minimum_checkpoints)
        print(json.dumps({k: v for k, v in result.items() if k not in ("checkpoints", "notes")}, ensure_ascii=False, indent=2))
        return 0 if result["result"] == "pass" else 1
    except (OSError, RuntimeError, ValueError, KeyError, zipfile.BadZipFile, UnicodeError) as exc:
        print("Checkpoint reconciliation stopped: " + clean(str(exc)), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
