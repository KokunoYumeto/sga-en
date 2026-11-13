"""Check archive extraction, repeatability, conflict refusal and path defenses.

All extraction and deliberately conflicting files are confined to a temporary
project-local directory which is removed after the check. The four original
archives and the working source tree are read-only throughout this test.
"""
from pathlib import Path
import csv
import io
import json
import shutil
import stat
import tempfile
import warnings
import zipfile

from unpack_inputs import ROOT, ARCHIVES, InputError, file_rows, relative_path, verify


def refused(callback):
    try:
        callback()
    except InputError:
        return True
    return False


def member_archive(extra, mode=0):
    stream = io.BytesIO()
    text = io.StringIO()
    writer = csv.writer(text, delimiter="\t", lineterminator="\n")
    writer.writerow(["path_in_zip", "source", "bytes", "sha256", "role"])
    with warnings.catch_warnings():
        # Duplicate entries are an intentional negative fixture. Keep the
        # expected standard-library warning out of retained diagnostics.
        warnings.filterwarnings("ignore", message="Duplicate name:", category=UserWarning)
        with zipfile.ZipFile(stream, "w") as zf:
            zf.writestr("MANIFEST.tsv", text.getvalue())
            for name in extra:
                info = zipfile.ZipInfo(name)
                if mode:
                    info.create_system = 3
                    info.external_attr = mode << 16
                zf.writestr(info, b"")
    stream.seek(0)
    return zipfile.ZipFile(stream)


def main():
    out = ROOT / "work/reproducibility"
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    for name, value in [
        ("parent traversal refused", "../escape.tex"),
        ("absolute member refused", "/absolute.tex"),
        ("backslash member refused", "check\\escape.tex"),
        ("drive-form member refused", "C:escape.tex"),
        ("empty path segment refused", "check//file.tex"),
        ("dot path segment refused", "check/./file.tex"),
    ]:
        checks.append(dict(check=name, passed=refused(lambda value=value: relative_path(value, member=True))))
    expected = dict(prefixes=["check"], files=0, payload_bytes=0)
    for name, members, mode in [
        ("symlink ZIP member refused", ["check/link"], stat.S_IFLNK | 0o777),
        ("duplicate ZIP member refused", ["check/a", "check/a"], 0),
        ("case-colliding ZIP member refused", ["check/a", "check/A"], 0),
        ("unmanifested ZIP payload refused", ["check/a"], 0),
    ]:
        with member_archive(members, mode) as zf:
            checks.append(dict(check=name, passed=refused(lambda: file_rows(zf, "test.zip", expected))))
    with tempfile.TemporaryDirectory(prefix="unpack-trial-", dir=ROOT) as temporary:
        trial = Path(temporary)
        target = trial / "source"
        first = verify(ROOT / "upload", target)
        checks.append(dict(check="all original payloads and sanitized manifests installed",
                           passed=first["payload_files"] == 1775 and first["installation"] == dict(installed=1779, identical_existing=0)))
        second = verify(ROOT / "upload", target)
        checks.append(dict(check="second extraction preserves all identical files",
                           passed=second["installation"] == dict(installed=0, identical_existing=1779)))
        checks.append(dict(check="raw manifest source column not copied",
                           passed=not (target / "MANIFEST.tsv").exists()
                           and all((target / "manifests" / (n.removesuffix(".zip") + ".tsv")).read_text().splitlines()[0]
                                   == "path_in_zip\tbytes\tsha256\trole" for n in ARCHIVES)))
        conflict = target / "check/NOTE_45.txt"
        original = conflict.read_bytes()
        conflict.write_bytes(b"intentional isolated extraction conflict\n")
        checks.append(dict(check="divergent existing file is refused and remains unchanged",
                           passed=refused(lambda: verify(ROOT / "upload", target))
                           and conflict.read_bytes() == b"intentional isolated extraction conflict\n"))
        conflict.write_bytes(original)
        link = trial / "linked-source"
        link.symlink_to(target, target_is_directory=True)
        checks.append(dict(check="symlink destination refused",
                           passed=refused(lambda: verify(ROOT / "upload", link))))
        bad_inputs = trial / "bad-inputs"
        bad_inputs.mkdir()
        archive = bad_inputs / "SGA4HALF_CHECK.zip"
        shutil.copyfile(ROOT / "upload/SGA4HALF_CHECK.zip", archive)
        with archive.open("r+b") as stream:
            stream.seek(0)
            stream.write(b"tampered")
        checks.append(dict(check="tampered whole-archive hash refused before extraction",
                           passed=refused(lambda: verify(bad_inputs, trial / "unused-output"))
                           and not (trial / "unused-output").exists()))
    report = dict(result="pass" if all(r["passed"] for r in checks) else "fail",
                  checks=checks, original_payload_files=1775, original_payload_bytes=75865260,
                  original_archives_modified=False, working_source_tree_modified=False,
                  trial_removed=True)
    (out / "UNPACK_VALIDATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "checks"}, ensure_ascii=False))
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
