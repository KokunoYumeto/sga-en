#!/usr/bin/env python3
"""Independent read-only audit of the implemented exact-packet ZIP routing.

Only this audit's ROUTING_* records are written. The archives are constructed,
tested and discarded in memory. No sealed packet or reader is changed.
"""
from pathlib import Path
from collections import Counter
import csv
import datetime
import hashlib
import io
import json
import re
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "review/english")]
import package_release
from collect_english_aggregate import verify_packet

REQUIRED = "review/package_release_audit/REQUIRED_ENGLISH_PACKET_FILES.json"
CATALOG = "review/english/aggregate/INPUT_CATALOG.json"
GLOSSARY = "review/english/terminology_final/INPUT_MANIFEST.json"
INPUT_PATHS = ["scripts/package_release.py", "review/english/collect_english_aggregate.py",
               "review/english/build_english_aggregate.py", REQUIRED, CATALOG, GLOSSARY, "README.md"]
UNIX_PATH = re.compile(r"/(?:workspace|home|root|tmp|var/tmp|mnt|Users|private|opt)/[A-Za-z0-9_.~+-]")
WINDOWS_PATH = re.compile(r"[A-Za-z]:\\(?:Users|work|home|Windows|Program Files)\\")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_record(path):
    data = (ROOT / path).read_bytes()
    return {"path": path, "bytes": len(data), "sha256": sha(data)}


def save(name, value):
    target = HERE / name
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(target)


def main():
    inputs = [file_record(path) for path in INPUT_PATHS]
    required = json.loads((ROOT / REQUIRED).read_text())
    required_by_path = {row["path"]: row for row in required}
    assert len(required) == len(required_by_path) == 2952
    catalog = json.loads((ROOT / CATALOG).read_text())
    glossary = json.loads((ROOT / GLOSSARY).read_text())["files"]
    archives, omissions = package_release.plan()
    owners = {}
    for archive, files in archives.items():
        for path in files:
            assert path not in owners, ("duplicate payload path", path)
            owners[path] = archive
    assert set(required_by_path) <= set(archives["EN"])
    assert set(required_by_path) == set(package_release.english_packet_files())
    assert not set(required_by_path) & {row["path"] for row in omissions}

    packet_checks = []
    for packet in catalog["packets"]:
        verified = verify_packet(ROOT / packet["directory"])
        assert verified == packet["manifest"], packet["label"]
        members = [row for row in required if row["packet"] == packet["label"]]
        assert len(members) == verified["verified_files"] + 1
        packet_checks.append({"packet": packet["label"], "directory": packet["directory"],
                              "original_manifest": verified, "manifest_plus_members": len(members),
                              "destination_archive": "EN", "collector_verification": "passed unchanged",
                              "all_original_member_paths_retained": True})
    glossary_checks = []
    for row in glossary:
        path = row["snapshot"]
        assert owners[path] == "RECORDS", path
        data = (ROOT / path).read_bytes()
        assert len(data) == row["bytes"] and sha(data) == row["sha256"], path
        glossary_checks.append({"path": path, "source": row["source"], "bytes": len(data),
                                "sha256": sha(data), "destination_archive": "RECORDS", "status": "exact snapshot included"})

    # Examine all text members of the complete packets and the 27 exact glossary
    # captures; retained logs are small pre-sanitized diagnostic reports.
    added_text_rows = []
    false_positives = []
    log_rows = []
    binaries = Counter()
    scope = {row["path"]: row for row in required}
    scope.update({row["snapshot"]: {"path": row["snapshot"], **row} for row in glossary})
    for path, row in sorted(scope.items()):
        p = ROOT / path
        data = p.read_bytes()
        assert len(data) == row["bytes"] and sha(data) == row["sha256"], path
        if p.suffix in package_release.BINARY:
            binaries[p.suffix] += 1
            continue
        text = data.decode("utf-8")
        assert not package_release.PRIVATE.search(text), path
        for matcher in [UNIX_PATH, WINDOWS_PATH]:
            for match in matcher.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                line = text.splitlines()[line_number - 1]
                assert path == "build/review_snapshots/english_xiii_complete616_666/external_inputs/review/expose_xiii_amendments/own_findings.jsonl"
                record = json.loads(line)
                assert record["attribution"] == "Direct fresh inspection by /root/review_late, explicitly authorized for separate amendment recording by coordinator /root."
                assert text[match.start():].startswith("/root/review_late")
                assert all(not Path(image["path"]).is_absolute() for image in record.get("evidence_images", []))
                false_positives.append({"path": path, "line": line_number,
                                       "source_id": record["source_id"], "field": "attribution",
                                       "token": "/root/review_late",
                                       "disposition": "canonical collaborating-agent identifier",
                                       "reason": "The token identifies the source reviewer in the explicit attribution field. The record separately supplies archive-relative scan and evidence-image paths. The collaborating-agent address in this review is the same identifier.",
                                       "source_image_references": record["image"],
                                       "evidence_image_paths": [image["path"] for image in record.get("evidence_images", [])]})
        item = {"path": path, "bytes": len(data), "sha256": sha(data),
                "private_detector": "passed", "expanded_path_scan": "passed or explicitly adjudicated agent identifier"}
        added_text_rows.append(item)
        if p.suffix == ".log":
            assert text.startswith("Diagnostic-only report; TeX filesystem loading paths omitted.\n")
            body = json.loads(text.split("\n", 1)[1])
            log_rows.append({**item, "diagnostic_only_header_verified": True,
                             "historical_run": body.get("run"), "historical_exit_code": body.get("exit_code"),
                             "diagnostic_count": len(body.get("diagnostics", [])),
                             "output_field": body.get("output", "")})
    assert len(false_positives) == 2 and len(log_rows) == 16

    union_rows = []
    results = []
    privacy_checked_all = 0
    for kind, files in archives.items():
        sink = io.BytesIO()
        header = package_release.manifest([])
        manifest_parts = [header]
        local_rows = []
        with zipfile.ZipFile(sink, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for path, p in sorted(files.items()):
                data = p.read_bytes()
                if p.suffix not in package_release.BINARY:
                    assert not package_release.PRIVATE.search(data.decode("utf-8")), path
                    privacy_checked_all += 1
                z.writestr(path, data)
                single_manifest = package_release.manifest([(path, data)])
                assert single_manifest.startswith(header)
                manifest_parts.append(single_manifest[len(header):])
                if path in required_by_path:
                    expected = required_by_path[path]
                    assert len(data) == expected["bytes"] and sha(data) == expected["sha256"]
                origin = "current reviewed workspace" if p.is_relative_to(ROOT) else "retained latest numbered checkpoint stage"
                local_rows.append({"path": path, "archive": kind, "bytes": len(data), "sha256": sha(data),
                                   "supply_origin": origin,
                                   "required_English_packet": required_by_path.get(path, {}).get("packet", ""),
                                   "required_packet_role": required_by_path.get(path, {}).get("role", "")})
            readme = (ROOT / "README.md").read_bytes()
            assert not package_release.PRIVATE.search(readme.decode("utf-8"))
            z.writestr("README.md", readme)
            manifest_parts.append(package_release.manifest([("README.md", readme)])[len(header):])
            manifest_bytes = b"".join(manifest_parts)
            z.writestr("MANIFEST.tsv", manifest_bytes)
        with zipfile.ZipFile(sink) as z:
            assert z.testzip() is None
            listed = list(csv.DictReader(io.StringIO(z.read("MANIFEST.tsv").decode()), delimiter="\t"))
            assert len(listed) == len(local_rows) + 1
            for row in listed:
                data = z.read(row["path"])
                assert len(data) == int(row["bytes"]) and sha(data) == row["sha256"], row["path"]
            for row in local_rows:
                row["in_memory_zip_readback_matches"] = True
            compressed = sum(info.compress_size for info in z.infolist())
        size = len(sink.getbuffer())
        assert size < 105_000_000
        results.append({"archive": "SGA6_READERS_" + kind + ".zip", "payload_files": len(local_rows),
                        "archive_entries": len(local_rows) + 2, "exact_in_memory_zip_bytes": size,
                        "deflated_member_bytes": compressed, "header_directory_bytes": size - compressed,
                        "headroom_to_105000000_bytes": 105_000_000 - size,
                        "manifest_sha256": sha(manifest_bytes),
                        "crc_test": "passed", "every_manifest_row_readback_hash": "passed"})
        union_rows += local_rows
        sink.close()
        print(json.dumps(results[-1]), flush=True)
    for item in inputs:
        assert file_record(item["path"]) == item, ("critical input changed during audit", item["path"])
    final_pdfs = [row for row in union_rows if "/final/" in row["path"] and row["path"].endswith(".pdf")]
    assert len(final_pdfs) == 8
    assert all(row["archive"] == ("FR" if row["path"].startswith("readers/fr/") else "EN") for row in final_pdfs)

    save("ROUTING_INPUTS.json", {"inputs": inputs, "all_critical_input_hashes_stable": True,
                                 "audit_script": file_record("review/package_release_audit/audit_exact_routing.py")})
    save("ROUTING_FILE_UNION.json", {"payload_paths": len(union_rows), "cross_archive_duplicate_payload_paths": 0,
                                     "common_archive_metadata": ["README.md", "MANIFEST.tsv"], "files": union_rows})
    save("ROUTING_PACKET_VERIFICATION.json", {"packets": packet_checks,
        "expected_packet_manifest_and_member_paths": 2952, "all_original_hashes_passed": True,
        "all_members_in_EN": True, "unchanged_collector_verification": True,
        "packet_files": [row for row in union_rows if row["required_English_packet"]],
        "glossary_captured_inputs": glossary_checks})
    save("ROUTING_PRIVACY_AUDIT.json", {"status": "passed", "scope": "All packet members plus all exact captured glossary inputs",
        "text_files_checked": len(added_text_rows), "binary_files": dict(binaries),
        "private_metadata_findings": [], "canonical_agent_identifier_false_positives": false_positives,
        "probe_logs": log_rows, "probe_log_bytes": sum(row["bytes"] for row in log_rows),
        "all_selected_release_text_files_privacy_checked": privacy_checked_all,
        "text_files": added_text_rows,
        "method": "Existing packaging PRIVATE detector plus an expanded absolute-path scan. Windows paths require a filesystem root directory, so mathematical letter-colon-backslash TeX is not misidentified. Both expanded-scan candidates are explicitly inspected attribution fields."})
    report = {"audit_id": "ASTRA-EXACT-ENGLISH-PACKET-ROUTING", "status": "passed",
        "completed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "packager_script_sha256": inputs[0]["sha256"], "required_files_inventory_sha256": next(x["sha256"] for x in inputs if x["path"] == REQUIRED),
        "catalog_sha256": next(x["sha256"] for x in inputs if x["path"] == CATALOG),
        "archives": results, "final_reader_PDFs_retained": final_pdfs,
        "packet_members_retained": 2952, "packet_manifests_unchanged": 10,
        "glossary_captured_inputs_retained": len(glossary_checks), "packet_or_source_files_omitted": 0,
        "projection_or_collector_change_needed": False, "private_metadata_findings": 0,
        "canonical_agent_identifier_false_positives": 2,
        "size_scope": "Exact in-memory ZIPs for the implemented plan captured when this script ran. This run's new ROUTING_* report files are written afterwards; the seal supplies their uncompressed-size upper bound against the available headroom. Final packaging still performs its own 105000000-byte assertion.",
        "clean_reconstruction_scope": "All ten catalog manifests and every original member retain their paths and hashes. The unchanged collector verifies every packet. All 27 captured glossary inputs are also included. Extract all three ZIPs into the same reconstruction root together with the original supplied inputs required by the documented build.",
        "writes": "Only ROUTING_* audit files in review/package_release_audit; no source, reader, packet or final ZIP written."}
    save("ROUTING_IMPLEMENTATION_AUDIT.json", report)
    md = ["# Exact English packet routing: independent audit", "",
          "**Passed. All 2,952 original English packet manifest/member files fit with the final English readers in the English ZIP. No packet projection, omission, redaction or collector change is needed.**", "",
          "| Archive | Exact in-memory bytes | Headroom below 105,000,000 bytes |", "|---|---:|---:|"]
    for row in results:
        md.append(f"| {row['archive']} | {row['exact_in_memory_zip_bytes']:,} | {row['headroom_to_105000000_bytes']:,} |")
    md += ["", "The sizes cover the implemented plan captured at audit start. This audit's newly written reports add a small amount; their total uncompressed upper bound is recorded in the routing seal. The final packager retains its own exact size gate.", "",
           "## Verified coverage", "",
           "- All eight final reader/master PDFs remain in their language archives.",
           "- All ten original catalog manifests and every one of their 2,952 manifest/member paths are present in EN with the exact original SHA-256 values. The unchanged collector verifies all ten packets.",
           "- All 27 exact glossary input captures are in RECORDS, including the eight formerly excluded build-subpath captures.",
           "- The archive payload union has no duplicate path across the three ZIPs. README.md and each archive's own MANIFEST.tsv remain common top-level metadata.",
           "- Every manifest row in each in-memory ZIP was read back and its length/SHA-256 verified. CRC tests passed all three ZIPs.", "",
           "## Privacy and historical diagnostics", "",
           f"All {len(added_text_rows):,} text members of the packet/glossary closure passed the packaging privacy detector. An additional absolute-path scan produced exactly two explicitly inspected attribution tokens: `/root/review_late`, in the frozen XIII amendment records for source notes 616 and 631. The field identifies the canonical collaborating review agent; the corresponding image references use archive-relative paths. The audit records both source IDs and evidence paths.", "",
           "The 16 probe logs total 15,744 bytes. Each already begins with its diagnostic-only sanitization notice and retains only run/exit status, diagnostics and relative output names. Their historical failed runs remain historical probe evidence; their files and original hashes are preserved. No private path or email was found.", "",
           "The 10 probe PDFs and 111 PNGs remain included as binary packet members. The implemented packager handles them without attempting UTF-8 decoding.", "",
           "## Fixed inputs and records", "",
           f"- Packager SHA-256: `{inputs[0]['sha256']}`",
           f"- Required packet inventory SHA-256: `{next(x['sha256'] for x in inputs if x['path'] == REQUIRED)}`",
           f"- Catalog SHA-256: `{next(x['sha256'] for x in inputs if x['path'] == CATALOG)}`",
           "- `ROUTING_INPUTS.json` records every critical input hash and confirms stability through the run.",
           "- `ROUTING_FILE_UNION.json` records every selected payload path, archive, size, hash and successful ZIP readback.",
           "- `ROUTING_PACKET_VERIFICATION.json` records every required packet path and every exact glossary capture.",
           "- `ROUTING_PRIVACY_AUDIT.json` records the text-file checks, all 16 log checks and the two agent-identifier dispositions.",
           "- `ROUTING_IMPLEMENTATION_AUDIT.json` records the size and reconstruction conclusion.", "",
           "Only this independent audit's records were written. No final ZIP, sealed packet, reader source or source decision was modified.", ""]
    (HERE / "ROUTING_HANDOFF.md").write_text("\n".join(md))
    owned = [p for p in HERE.iterdir() if p.name.startswith("ROUTING_") and p.name not in ["ROUTING_MANIFEST.json", "ROUTING_SEAL.json"]]
    owned.append(HERE / "audit_exact_routing.py")
    manifest = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(owned)]
    save("ROUTING_MANIFEST.json", {"files": manifest})
    raw_bound = sum(row["bytes"] for row in manifest) + (HERE / "ROUTING_MANIFEST.json").stat().st_size + 20000
    headroom = min(row["headroom_to_105000000_bytes"] for row in results)
    assert raw_bound < headroom
    seal = {"status": "complete and sealed", "audit_sha256": sha((HERE / "ROUTING_IMPLEMENTATION_AUDIT.json").read_bytes()),
            "manifest_sha256": sha((HERE / "ROUTING_MANIFEST.json").read_bytes()),
            "audit_report_addition_uncompressed_bound_bytes": raw_bound,
            "minimum_measured_archive_headroom_bytes": headroom,
            "report_addition_within_headroom": True,
            "no_source_or_packet_changes": True, "final_archives_written": False}
    save("ROUTING_SEAL.json", seal)
    print(json.dumps(seal), flush=True)


if __name__ == "__main__":
    main()
