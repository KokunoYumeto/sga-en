# Invoke this script with python3.
"""Verify the four original archives and safely install their source payloads.

Run from any directory. Paths supplied on the command line must be relative
to the project. Every archive hash, manifest entry, payload size and payload
hash is checked before any source payload is installed. Existing identical
files are preserved; a different existing file stops the operation.

The original manifests contain a source-location column. It is deliberately
excluded from the generated manifests and verification report.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CHUNK = 1024 * 1024
ARCHIVES = {
    "SGA4HALF_CHECK.zip": {
        "bytes": 714934,
        "sha256": "842f3472346a068a258961a8a521e6d54f1c66f362923bdc06b9600397e7c286",
        "files": 461,
        "payload_bytes": 2048241,
        "prefixes": ["check"],
    },
    "SGA4HALF_EN.zip": {
        "bytes": 2010497,
        "sha256": "91a7d91c16bf40efe37c97d59e71e95ef6a9295928e32dfe7eab05f1f574c05b",
        "files": 33,
        "payload_bytes": 3572445,
        "prefixes": ["en"],
    },
    "SGA4HALF_FR.zip": {
        "bytes": 774922,
        "sha256": "14a005bf6f6538832694351914c11373e8ec311fe2c934707cded579c3623b96",
        "files": 63,
        "payload_bytes": 2639667,
        "prefixes": ["fr"],
    },
    "SGA4HALF_SCANS.zip": {
        "bytes": 64529332,
        "sha256": "e5f28dae9c843302aeb3e41afce97aa34247b3276e7c0f6296c5472845007ce0",
        "files": 1218,
        "payload_bytes": 67604907,
        "prefixes": ["scan", "strips"],
    },
}


class InputError(RuntimeError):
    """An input or destination failed a verification requirement."""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def relative_path(value: str, *, member: bool = False) -> PurePosixPath:
    """Reject platform-dependent, absolute, ambiguous and escaping names."""
    if not value or "\\" in value or ":" in value or "\0" in value:
        raise InputError("A path is empty or contains a forbidden character.")
    p = PurePosixPath(value)
    raw = value.split("/")
    if p.is_absolute() or ".." in raw or (member and any(x in ("", ".") for x in raw)):
        raise InputError("A path is absolute, ambiguous or leaves the project.")
    return p


def project_path(value: str) -> Path:
    p = relative_path(value)
    result = ROOT.joinpath(*p.parts)
    check_no_symlinks(result)
    return result


def check_no_symlinks(path: Path) -> None:
    """Check every existing component, including a prospective output file."""
    try:
        parts = path.relative_to(ROOT).parts
    except ValueError as exc:
        raise InputError("A destination leaves the project.") from exc
    current = ROOT
    for part in parts:
        current /= part
        if current.is_symlink():
            raise InputError("A project path contains a symbolic link.")


def file_rows(zf: zipfile.ZipFile, archive: str, expected: dict) -> list[dict]:
    infos = zf.infolist()
    names = []
    folded = set()
    for info in infos:
        name = str(relative_path(info.filename, member=True))
        if name.casefold() in folded:
            raise InputError(f"{archive}: duplicate or case-colliding ZIP member.")
        folded.add(name.casefold())
        names.append(name)
        mode = stat.S_IFMT(info.external_attr >> 16)
        if info.is_dir() or mode not in (0, stat.S_IFREG) or info.flag_bits & 1:
            raise InputError(f"{archive}: a member is not an ordinary unencrypted file.")
    if "MANIFEST.tsv" not in names:
        raise InputError(f"{archive}: root manifest is missing.")
    try:
        reader = csv.DictReader(io.StringIO(zf.read("MANIFEST.tsv").decode("utf-8-sig")), delimiter="\t")
        if reader.fieldnames != ["path_in_zip", "source", "bytes", "sha256", "role"]:
            raise InputError(f"{archive}: unexpected manifest columns.")
        source_rows = list(reader)
    except (UnicodeError, csv.Error) as exc:
        raise InputError(f"{archive}: unreadable manifest.") from exc
    rows = []
    seen = set()
    for source_row in source_rows:
        if None in source_row or any(value is None for value in source_row.values()):
            raise InputError(f"{archive}: a manifest row has the wrong number of columns.")
        name = str(relative_path(source_row.get("path_in_zip", ""), member=True))
        if PurePosixPath(name).parts[0] not in expected["prefixes"]:
            raise InputError(f"{archive}: manifest payload has an unexpected top-level directory.")
        if name.casefold() in seen:
            raise InputError(f"{archive}: duplicate or case-colliding manifest row.")
        seen.add(name.casefold())
        size = source_row.get("bytes", "")
        digest = source_row.get("sha256", "").lower()
        if not size.isdigit() or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise InputError(f"{archive}: invalid manifest size or hash.")
        # Do not retain source_row['source'], even in errors or intermediate JSON.
        rows.append(dict(archive=archive, path=name, bytes=int(size), sha256=digest,
                         role=source_row.get("role", "")))
    if len(rows) != expected["files"] or sum(r["bytes"] for r in rows) != expected["payload_bytes"]:
        raise InputError(f"{archive}: manifest totals differ from the original archive inventory.")
    if set(names) != {"MANIFEST.tsv"} | {r["path"] for r in rows}:
        raise InputError(f"{archive}: manifest and ZIP inventories differ.")
    for row in rows:
        if zf.getinfo(row["path"]).file_size != row["bytes"]:
            raise InputError(f"{archive}: a member size disagrees with its manifest.")
    return sorted(rows, key=lambda r: r["path"])


def sanitized_manifest(rows: list[dict]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=["path_in_zip", "bytes", "sha256", "role"],
                            delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(dict(path_in_zip=row["path"], bytes=row["bytes"],
                             sha256=row["sha256"], role=row["role"]))
    return stream.getvalue().encode("utf-8")


def destination_status(path: Path, expected_size: int, expected_hash: str) -> str:
    check_no_symlinks(path)
    for parent in path.parents:
        if parent == ROOT:
            break
        if parent.exists() and not parent.is_dir():
            raise InputError("A destination parent is not a directory.")
    if not path.exists():
        return "missing"
    if not path.is_file() or path.stat().st_size != expected_size or sha256(path) != expected_hash:
        raise InputError("An existing destination differs from the verified source; nothing was overwritten.")
    return "identical"


def install_staged(stage: Path, output: Path, installs: list[dict]) -> dict:
    """Preflight all outputs, then install missing files without replacement."""
    counts = {"installed": 0, "identical_existing": 0}
    for row in installs:
        row["destination_status"] = destination_status(output / row["path"], row["bytes"], row["sha256"])
    for row in installs:
        target = output / row["path"]
        if row["destination_status"] == "identical":
            counts["identical_existing"] += 1
            continue
        check_no_symlinks(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        # A hard link is an atomic no-replace operation on this same filesystem.
        # It also fails safely if another process creates the destination first.
        try:
            os.link(stage / row["path"], target, follow_symlinks=False)
        except FileExistsError as exc:
            raise InputError("A destination appeared during installation; it was not overwritten.") from exc
        counts["installed"] += 1
    return counts


def verify(input_dir: Path, output_dir: Path, *, verify_only: bool = False) -> dict:
    check_no_symlinks(input_dir)
    check_no_symlinks(output_dir)
    if not input_dir.is_dir():
        raise InputError("The input directory is missing; supply the four original ZIP files.")
    archive_results = []
    all_rows = []
    inventory = []
    payload_names = set()
    # Verify every complete archive before reading or staging any payload.
    for name, expected in ARCHIVES.items():
        path = input_dir / name
        check_no_symlinks(path)
        if not path.is_file():
            raise InputError(f"Missing original archive: {name}")
        if path.stat().st_size != expected["bytes"] or sha256(path) != expected["sha256"]:
            raise InputError(f"{name}: archive size or SHA-256 differs from the supplied original.")
        with zipfile.ZipFile(path) as zf:
            rows = file_rows(zf, name, expected)
        for row in rows:
            if row["path"].casefold() in payload_names:
                raise InputError("Two archives claim the same payload path.")
            payload_names.add(row["path"].casefold())
        archive_results.append(dict(archive=name, bytes=expected["bytes"], sha256=expected["sha256"],
                                    verified=True, payload_files=len(rows), payload_bytes=expected["payload_bytes"]))
        inventory.append((name, rows))
    stage_parent = output_dir if output_dir == ROOT else output_dir.parent
    if not verify_only:
        check_no_symlinks(stage_parent)
        stage_parent.mkdir(parents=True, exist_ok=True)
    # The verified payloads are held outside the destination until every payload
    # has passed. Verify-only uses no staging directory and no source writes.
    temp = tempfile.TemporaryDirectory(prefix="unpack-stage-", dir=stage_parent) if not verify_only else None
    stage = Path(temp.name) if temp else None
    installs = []
    try:
        for name, rows in inventory:
            with zipfile.ZipFile(input_dir / name) as zf:
                for row in rows:
                    h = hashlib.sha256()
                    total = 0
                    destination = stage / row["path"] if stage else None
                    if destination:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                    output = destination.open("wb") if destination else None
                    try:
                        with zf.open(row["path"]) as stream:
                            for block in iter(lambda: stream.read(CHUNK), b""):
                                total += len(block)
                                h.update(block)
                                if output:
                                    output.write(block)
                    finally:
                        if output:
                            output.close()
                    if total != row["bytes"] or h.hexdigest() != row["sha256"]:
                        raise InputError(f"{name}: a payload failed its size or SHA-256 check.")
                    if destination:
                        destination.chmod(0o644)
                    installs.append(dict(path=row["path"], bytes=row["bytes"], sha256=row["sha256"]))
                    all_rows.append({**row, "verified": True})
            content = sanitized_manifest(rows)
            manifest_name = "manifests/" + name.removesuffix(".zip") + ".tsv"
            if stage:
                (stage / "manifests").mkdir(exist_ok=True)
                (stage / manifest_name).write_bytes(content)
                (stage / manifest_name).chmod(0o644)
            installs.append(dict(path=manifest_name, bytes=len(content), sha256=hashlib.sha256(content).hexdigest()))
        if stage:
            installed = install_staged(stage, output_dir, installs)
        else:
            states = [destination_status(output_dir / r["path"], r["bytes"], r["sha256"]) for r in installs]
            installed = dict(installed=0, identical_existing=states.count("identical"),
                             missing_not_installed=states.count("missing"))
    finally:
        if temp:
            temp.cleanup()
    return dict(verified=True, mode="verify-only" if verify_only else "verified extraction",
                input_directory=input_dir.relative_to(ROOT).as_posix(),
                output_directory=output_dir.relative_to(ROOT).as_posix(),
                archive_count=len(archive_results), payload_files=len(all_rows),
                payload_bytes=sum(r["bytes"] for r in all_rows), sanitized_manifests=4,
                manifest_source_column_retained=False, installation=installed,
                archives=archive_results, files=all_rows)


def write_report(path: Path, report: dict) -> None:
    check_no_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix="verification-", suffix=".json", delete=False) as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        temporary = Path(stream.name)
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="upload", help="Project-relative directory containing the four original ZIPs")
    parser.add_argument("--output-dir", default="source", help="Project-relative source destination")
    parser.add_argument("--report", default="work/input_verification.json", help="Project-relative privacy-safe JSON report")
    parser.add_argument("--verify-only", action="store_true", help="Verify archives and any existing outputs; do not install source files")
    args = parser.parse_args()
    try:
        result = verify(project_path(args.input_dir), project_path(args.output_dir), verify_only=args.verify_only)
        write_report(project_path(args.report), result)
        print(json.dumps({k: v for k, v in result.items() if k not in ("files", "archives")}, ensure_ascii=False))
        return 0
    except (InputError, OSError, zipfile.BadZipFile, RuntimeError) as exc:
        # Library exception messages can contain local paths; report only our
        # explicitly constructed, path-free InputError descriptions.
        detail = str(exc) if isinstance(exc, InputError) else type(exc).__name__
        print("Input verification failed: " + detail, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
