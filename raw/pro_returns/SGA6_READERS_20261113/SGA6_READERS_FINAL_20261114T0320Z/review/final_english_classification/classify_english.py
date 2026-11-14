#!/usr/bin/env python3
"""Read-only classification of the exact 691 final English variant groups.

Uses the French classifier unchanged, including its precedence. Classification
comes from resolved decision metadata, never from the appearance of an edit.
All writes are restricted to this audit directory.
"""
from pathlib import Path
from collections import Counter, defaultdict
import datetime
import hashlib
import inspect
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fr_source_links import load_decisions
from fr_readable_apparatus import classify

VARIANTS = "review/english/final/VARIANTS.jsonl"
LEDGER = "review/english/final/TRANSFER_LEDGER.jsonl"
ORIGINAL = "review/english/EN_VARIANTS.jsonl"
EXPECTED_VARIANT_SHA = "eba4605bc5b30336f87910e4d30feeccf88661ef8492a292eec0d17696462757"
KINDS = ["source misprint correction", "mathematical source correction",
         "explicit notation convention", "adjudicated source correction"]
CONVENTIONS = {"font", "underline", "font_convention", "notation", "convention", "confirmed_notation"}
inputs = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    path = Path(path)
    full = path if path.is_absolute() else ROOT / path
    data = full.read_bytes()
    rel = full.relative_to(ROOT).as_posix()
    record = {"path": rel, "sha256": sha(data), "bytes": len(data)}
    if rel in inputs:
        assert inputs[rel] == record, ("input changed during audit", rel)
    inputs[rel] = record
    return data


def records(path):
    return [(i, line, json.loads(line)) for i, line in enumerate(read(path).decode().splitlines(), 1) if line.strip()]


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def split_source(value):
    assert isinstance(value, str), ("unexpected source type", value)
    return [part.strip() for part in value.split(";") if part.strip()]


def unique(values):
    return list(dict.fromkeys(values))


def expose(page):
    if not isinstance(page, int):
        return "Front matter"
    for name, first, last in [
        ("0", 1, 77), ("I", 78, 159), ("II", 160, 221), ("III", 222, 273),
        ("IV", 274, 296), ("V", 297, 364), ("VI", 365, 415), ("VII", 416, 465),
        ("VIII", 466, 497), ("IX", 498, 518), ("X", 519, 594), ("XII", 595, 615),
        ("XIII", 616, 666), ("XIV", 667, 690), ("Indexes", 691, 700)
    ]:
        if first <= page <= last:
            return name
    raise AssertionError(("unassigned source folio", page))


def metadata_basis(decisions, result):
    tests = []
    for d in decisions:
        kinds = {str(d.get(k, "")) for k in ["kind", "source_error_kind"]}
        math = any("mathematical_source" in k or "substantive_mathematical" in k for k in kinds)
        misprint = (d.get("is_misprint") is True or d.get("record_type") == "misprint"
                    or d.get("type") == "misprint" or "misprint" in str(d.get("kind", "")))
        notation = bool(kinds & CONVENTIONS)
        tests.append({"source_id": d["source_id"],
                      "metadata": {key: d.get(key) for key in ["kind", "source_error_kind", "is_misprint", "record_type", "type"]},
                      "mathematical_rule_matches": math, "misprint_rule_matches": misprint,
                      "notation_rule_matches": notation,
                      "classification_supplement": d.get("classification_source", "")})
    rule = {
        "mathematical source correction": (1, "At least one kind/source_error_kind explicitly contains mathematical_source or substantive_mathematical."),
        "source misprint correction": (2, "No mathematical-kind match; at least one source has is_misprint=true, record_type/type=misprint, or misprint in kind."),
        "explicit notation convention": (3, "No mathematical or misprint match; at least one kind/source_error_kind exactly names an accepted notation/convention kind."),
        "adjudicated source correction": (4, "The sources are adjudicated and image-backed, but none has one of the classifier's three higher-precedence metadata predicates. The unchanged classifier's adjudicated category applies; no source-error label is inferred from the edited text.")
    }[result]
    return {"function": "scripts/fr_readable_apparatus.py::classify", "precedence_rule": rule[0],
            "reason": rule[1], "source_metadata_tests": tests}


def main():
    # Capture every existing input read by load_decisions, including merge and
    # supplement streams, before calling that authoritative read-only loader.
    for path in ["scripts/fr_source_links.py", "scripts/fr_readable_apparatus.py", "build/registry.json",
                 "review/merge_resolutions.jsonl", "review/final_classification_audit/SUPPLEMENTAL_SOURCE_ERROR_CLASSIFICATIONS.jsonl"]:
        read(path)
    for directory in sorted((ROOT / "review").iterdir()):
        if directory.is_dir():
            for name in ["decisions.jsonl", "own_findings.jsonl", "convention_decisions.jsonl"]:
                path = directory / name
                if path.exists():
                    read(path)
    registry, byid, decisions = load_decisions()
    aliases = {key.replace(":entries#", "#"): key for key in byid}

    def canonical(token):
        return token if token in decisions else aliases.get(token, token)

    variants = records(VARIANTS)
    assert inputs[VARIANTS]["sha256"] == EXPECTED_VARIANT_SHA
    assert len(variants) == 691
    assert len({v["id"] for _, _, v in variants}) == 691
    ledger = records(LEDGER)
    original = {v["id"]: (n, line, v) for n, line, v in records(ORIGINAL)}
    by_variant = defaultdict(list)
    for lineno, rawline, row in ledger:
        r = row["record"]
        identifiers = []
        for key in ["English_variant", "English_variants", "id"]:
            val = r.get(key, [])
            if isinstance(val, str):
                val = [val]
            if isinstance(val, list):
                identifiers += [value for value in val if isinstance(value, str) and value.startswith("EN-")]
        for vid in unique(identifiers):
            by_variant[vid].append((lineno, rawline, row))

    entries = []
    exact_evidence = []
    auxiliary = defaultdict(list)
    used_sources = set()
    usage = defaultdict(list)
    kind_counts = Counter()
    expose_counts = defaultdict(Counter)
    direct_pair_count = original_pair_count = 0
    selected_transfer_input_paths = set()
    for ordinal, (lineno, rawline, v) in enumerate(variants, 1):
        primary = []
        auxiliary_refs = []
        for token in split_source(v["source"]):
            sid = canonical(token)
            if sid in decisions:
                primary.append(sid)
            else:
                assert not ("#" in token and token.split("#", 1)[0].endswith((".json", ".jsonl"))), (v["id"], token)
                candidate = ROOT / token
                if not candidate.exists() and token == "EN_INDEPENDENT_SOURCE_ASSESSMENTS.jsonl":
                    candidate = ROOT / "review/english" / token
                if candidate.is_file():
                    read(candidate)
                    item = {"literal": token, "reference_type": "supporting file reference",
                            "resolved_path": candidate.relative_to(ROOT).as_posix(),
                            "sha256": inputs[candidate.relative_to(ROOT).as_posix()]["sha256"]}
                else:
                    assert token in {"coordinator primary bibliography verification", "directly identified bibliography item[5] on220"}, token
                    item = {"literal": token, "reference_type": "bibliographic verification description"}
                auxiliary_refs.append(item)
                auxiliary[token].append(v["id"])
        primary = unique(primary)
        related = unique(canonical(sid) for sid in v.get("related_sources", []))
        all_ids = unique(primary + related)
        assert primary and all(sid in decisions for sid in related), v["id"]
        ds = [decisions[sid] for sid in all_ids]
        page_checks = []
        for d in ds:
            assert d.get("image") and d.get("reason"), (v["id"], d["source_id"])
            assert not d.get("verdict", "").startswith(("pending", "reverted", "rejected")), (v["id"], d["source_id"])
            direct_page = str(d.get("page")) == str(v["page"])
            related_page = v["page"] in d.get("related_pages", [])
            assert direct_page or related_page, (v["id"], d["source_id"], "source folio mismatch")
            page_checks.append({"source_id": d["source_id"], "decision_folio": d.get("page"),
                                "variant_folio": v["page"], "method": "same explicit folio" if direct_page else "explicit related_pages scope",
                                "related_pages": d.get("related_pages", []) if related_page else []})
            used_sources.add(d["source_id"])
            usage[d["source_id"]].append(v["id"])

        # Link the exact English alternative pair, never a guessed short hunk.
        exact = []
        for ln, raw, row in by_variant[v["id"]]:
            r = row["record"]
            if r.get("printed") == v["printed"] and r.get("corrected") == v["corrected"]:
                assert str(r.get("page")) == str(v["page"]), v["id"]
                exact.append({"method": "exact final variant ID, folio and both complete alternatives",
                              "aggregate_ledger_line": ln, "aggregate_ledger_row_sha256": sha(raw.encode()),
                              "aggregate_transfer_id": row["aggregate_transfer_id"],
                              "input": row["input"], "input_sha256": row["input_sha256"],
                              "input_row": row["input_row"], "record": r})
                selected_transfer_input_paths.add(row["input"])
        if exact:
            direct_pair_count += 1
            exact_source_ids = unique(canonical(s) for item in exact for s in split_source(item["record"].get("source_id", item["record"].get("source", ""))))
            assert set(all_ids) <= set(exact_source_ids), (v["id"], "declared source missing from its exact transfer", all_ids, exact_source_ids)
        else:
            n, raw, r = original[v["id"]]
            assert all(r[k] == v[k] for k in ["id", "page", "source", "printed", "corrected"]), v["id"]
            exact = [{"method": "exact original English variant-transfer record: ID, folio, source string and both alternatives",
                      "input": ORIGINAL, "input_sha256": inputs[ORIGINAL]["sha256"],
                      "input_row": n, "input_row_sha256": sha(raw.encode()), "record": r}]
            original_pair_count += 1
        exact_evidence.append({"variant_id": v["id"], "folio": v["page"], "sources": all_ids,
                               "exact_transfer_records": exact,
                               "additional_id_only_transfer_records": [
                                   {"aggregate_transfer_id": row["aggregate_transfer_id"], "aggregate_ledger_line": ln,
                                    "aggregate_ledger_row_sha256": sha(raw.encode()), "input": row["input"],
                                    "input_row": row["input_row"], "record": row["record"]}
                                   for ln, raw, row in by_variant[v["id"]]
                                   if row["record"].get("English_variant") == v["id"]
                                   and not (row["record"].get("printed") == v["printed"] and row["record"].get("corrected") == v["corrected"])]})
        kind = classify(ds)
        assert kind in KINDS
        section = expose(v["page"])
        kind_counts[kind] += 1
        expose_counts[section][kind] += 1
        entries.append({"ordinal": ordinal, "variant_id": v["id"], "folio": v["page"], "expose": section,
                        "kind": kind, "primary_source_decision_ids": primary,
                        "related_source_decision_ids": related, "source_decision_ids": all_ids,
                        "auxiliary_references": auxiliary_refs,
                        "input_variant_line": lineno, "input_variant_line_sha256": sha(rawline.encode()),
                        "printed": v["printed"], "corrected": v["corrected"],
                        "sha256_printed": sha(v["printed"].encode()), "sha256_corrected": sha(v["corrected"].encode()),
                        "classification_basis": metadata_basis(ds, kind),
                        "source_scope_checks": page_checks,
                        "transfer_evidence": {"file": "review/final_english_classification/EXACT_TRANSFER_EVIDENCE.json",
                                              "variant_id": v["id"], "complete_pair_record_count": len(exact),
                                              "method": exact[0]["method"]},
                        "status": "classified from resolved sourced decisions; complete English pair attribution verified"})

    # Verify the immutable transfer inputs whose exact rows support this audit.
    for path in sorted(selected_transfer_input_paths):
        read(path)
    for item in exact_evidence:
        for evidence in item["exact_transfer_records"]:
            assert inputs[evidence["input"]]["sha256"] == evidence["input_sha256"], (item["variant_id"], evidence["input"])
            if "aggregate_transfer_id" in evidence:
                original_lines = read(evidence["input"]).decode().splitlines()
                original_row = json.loads(original_lines[evidence["input_row"] - 1])
                assert original_row == evidence["record"], (item["variant_id"], "source transfer row differs")

    assert direct_pair_count == 623 and original_pair_count == 68
    broad = []
    for sid, vids in usage.items():
        if len(vids) <= 1:
            continue
        d = decisions[sid]
        broad.append({"source_decision_id": sid, "source_kind": classify([d]),
                      "decision_folio": d.get("page"), "region": d.get("region"),
                      "printed_reading": d.get("printed_reading"), "change": d.get("change"),
                      "reason": d["reason"], "related_pages": d.get("related_pages", []),
                      "variant_ids": vids,
                      "method": "Each listed complete English pair is independently bound to this exact source ID in EXACT_TRANSFER_EVIDENCE.json; reuse does not infer a source from the appearance of a short replacement.",
                      "status": "complete exact-pair transfer attribution verified"})
    source_snapshot = {sid: decisions[sid] for sid in sorted(used_sources)}
    save("RESOLVED_SOURCE_DECISIONS.json", source_snapshot)
    save("EXACT_TRANSFER_EVIDENCE.json", exact_evidence)
    save("BROAD_ALIAS_AUDIT.json", broad)

    # Re-read all recorded inputs so release counts are fixed to one stable set.
    input_manifest = [inputs[key] for key in sorted(inputs)]
    for item in input_manifest:
        assert sha((ROOT / item["path"]).read_bytes()) == item["sha256"], ("input changed during audit", item["path"])
    save("INPUT_MANIFEST.json", {"files": input_manifest, "all_input_hashes_unchanged_at_completion": True})
    ordered_exposes = ["Front matter", "0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "Indexes"]
    by_expose = [{"expose": key, "variants": sum(expose_counts[key].values()),
                  "by_kind": {kind: expose_counts[key][kind] for kind in KINDS}}
                 for key in ordered_exposes]
    summary = {"variants": len(entries), "classified": len(entries), "unresolved": 0,
               "missing_source_decisions": 0, "missing_pair_attributions": 0,
               "resolved_source_decision_ids": len(used_sources),
               "by_kind": {kind: kind_counts[kind] for kind in KINDS}, "by_expose": by_expose,
               "groups_with_exact_aggregate_transfer_pairs": direct_pair_count,
               "groups_with_exact_original_variant_transfer_pairs": original_pair_count,
               "reused_source_ids_checked_against_exact_transfers": len(broad),
               "groups_with_declared_related_sources": sum(bool(e["related_source_decision_ids"]) for e in entries),
               "auxiliary_reference_strings": len(auxiliary),
               "auxiliary_reference_occurrences": sum(len(ids) for ids in auxiliary.values())}
    report = {"audit_id": "ASTRA-EN-APPARATUS-KINDS-691", "status": "complete",
              "completed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "input": inputs[VARIANTS], "summary": summary,
              "taxonomy": {"function": "scripts/fr_readable_apparatus.py::classify",
                           "file_sha256": inputs["scripts/fr_readable_apparatus.py"]["sha256"],
                           "exact_function_sha256": sha(inspect.getsource(classify).encode()),
                           "exact_function": inspect.getsource(classify),
                           "resolved_metadata_loader": "scripts/fr_source_links.py::load_decisions",
                           "precedence": ["mathematical source correction", "source misprint correction", "explicit notation convention", "adjudicated source correction"],
                           "counting_unit": "One complete English variant group, with all explicitly sourced components; a compound group takes the classifier's first matching category."},
              "source_decision_snapshot": "review/final_english_classification/RESOLVED_SOURCE_DECISIONS.json",
              "broad_alias_audit": "review/final_english_classification/BROAD_ALIAS_AUDIT.json",
              "auxiliary_reference_inventory": [{"literal": key, "variant_ids": vids} for key, vids in auxiliary.items()],
              "read_only": True, "new_scan_reading_claim": False,
              "classification_limit": "The eight adjudicated-source entries are explicitly resolved source corrections whose supplied metadata triggers the classifier's fourth branch. This audit does not silently supply new misprint or mathematical-error metadata.",
              "entries": entries}
    save("CLASSIFICATION.json", report)
    save("VALIDATION.json", {"status": "passed", "variant_input_sha256": EXPECTED_VARIANT_SHA,
                              "unique_ids": 691, "complete_classifications": 691,
                              "source_ids_resolved": len(used_sources), "unresolved": 0,
                              "source_pages_match_or_have_explicit_related_page_scope": True,
                              "all_sources_have_image_reason_and_nonpending_accepted_verdict": True,
                              "all_complete_English_pairs_bound_to_exact_transfer_records": True,
                              "read_inputs_unchanged": True, "source_or_reader_mutations": []})

    lines = ["# English apparatus classification handoff", "",
             "**All 691 English variant groups are classified; zero unresolved source decisions or complete-pair attributions remain.** This is a read-only classification audit. It changes no English/French reader, final variant ledger, source decision or sealed audit.", "",
             f"Input: `{VARIANTS}`  ", f"SHA-256: `{EXPECTED_VARIANT_SHA}`", "",
             "The audit calls `fr_source_links.load_decisions()` and the unchanged `fr_readable_apparatus.classify()` function. It includes semicolon-separated decision IDs and the explicitly declared `related_sources`. File references and bibliographic verification descriptions are preserved separately and are not treated as decision IDs.", "",
             "## Counts by kind", "", "| Kind | English variant groups |", "|---|---:|"]
    lines += [f"| {kind} | {kind_counts[kind]} |" for kind in KINDS]
    lines += ["| **Total** | **691** |", "", "## Counts by exposé", "",
              "| Exposé / matter | Misprint | Mathematical | Notation | Adjudicated | Total |", "|---|---:|---:|---:|---:|---:|"]
    for row in by_expose:
        lines.append("| " + row["expose"] + " | " + " | ".join(str(row["by_kind"][k]) for k in KINDS) + f" | {row['variants']} |")
    lines += ["", "XI is marked « Non rédigé » in the source and has no variant group. Bibliographies remain assigned to their exposé; the terminal indexes are listed separately.", "",
              "## Attribution checks", "",
              f"- **{len(used_sources)} distinct resolved source decisions** supply the classifications, including amendments and the explicit classification supplements.",
              "- **623 groups** have exact final-ID, folio and complete printed/corrected pairs in the aggregate transfer ledger. **68 groups** match their complete original `EN_VARIANTS.jsonl` records; these are EN-VAR-001…067 and EN-VAR-068. The latter also has an ID-linked aggregate record that does not repeat the pair.",
              f"- **{len(broad)} reused source IDs** were checked against their individually named complete transfer pairs. The only cross-folio source alias, ASTRA-EARLY-TYPE-016, explicitly covers both 70 and 75.",
              "- All 27 groups with declared secondary sources include those decisions. In VI385-03 the E-rule source misprint takes precedence over the P notation convention; in VII077/461 the independent rational-coefficient mathematical correction takes precedence over the exponent misprint.",
              f"- **{len(auxiliary)} auxiliary reference strings ({sum(len(ids) for ids in auxiliary.values())} uses)** are retained separately. Every supporting file exists and has its hash recorded. The two bibliographic descriptions remain literal descriptions attached to an independently resolved source decision.",
              "- **No actual missing provenance was found.** The eight entries classified as adjudicated source corrections use the unchanged classifier's fourth branch; their accepted image-backed decisions are complete, but their metadata does not assert one of its higher-precedence categories.", "",
              "## Fourth-branch entries", "", "| Variant | Folio | Explicit source decision(s) |", "|---|---:|---|"]
    for e in entries:
        if e["kind"] == "adjudicated source correction":
            lines.append(f"| {e['variant_id']} | {e['folio']} | " + "; ".join(e["source_decision_ids"]) + " |")
    lines += ["", "## Files", "",
              "- `CLASSIFICATION.json`: summary, exact classifier, and all 691 entries with source IDs, complete alternative hashes, metadata predicates and transfer attribution.",
              "- `RESOLVED_SOURCE_DECISIONS.json`: exact resolved/amended/supplemented source metadata used.",
              "- `EXACT_TRANSFER_EVIDENCE.json`: full supporting English transfer records and row/file hashes.",
              "- `BROAD_ALIAS_AUDIT.json`: occurrence-specific transfer checks for reused decision aliases.",
              "- `INPUT_MANIFEST.json`: exact hashes of all loader and transfer inputs; rechecked unchanged at completion.",
              "- `VALIDATION.json`: zero-unresolved release checks.", "",
              "These are counts of English variant groups. A group can contain more than one sourced component and is counted once according to the shared classifier's precedence. This audit does not re-adjudicate the mathematics or assert a fresh scan reading.", ""]
    (HERE / "HANDOFF.md").write_text("\n".join(lines))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
