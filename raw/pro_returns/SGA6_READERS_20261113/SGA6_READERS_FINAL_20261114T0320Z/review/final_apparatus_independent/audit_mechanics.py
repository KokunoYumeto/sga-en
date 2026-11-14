#!/usr/bin/env python3
"""Independent, read-only validation of the captured French provenance inputs.

Only this audit directory receives output.  Context locations are checked against
the captured bodies after inverting the 49 later numeric-font declarations in
memory; no reader, source decision, or frozen contribution is modified.
"""
from pathlib import Path
from collections import Counter
import csv
import difflib
import hashlib
import json
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SNAP = HERE / "input_snapshot"


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def split_pages(text):
    marker = re.compile(r"(?m)^%+\s*scan idx\s+(\d+)\s*\|\s*folio\s+([^%\n]+?)\s*%+.*$")
    matches = list(marker.finditer(text))
    result = {"front": text[:matches[0].start()]}
    for i, match in enumerate(matches):
        page = match[2].strip()
        assert page not in result
        result[page] = text[match.start():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
    return result


def deltas(a, b):
    return [dict(printed_offsets=[i, j], corrected_offsets=[k, l],
                 printed=a[i:j], corrected=b[k:l])
            for tag, i, j, k, l in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
            if tag != "equal"]


def check(test, label, problems):
    if not test:
        problems.append(label)


def main():
    variants = read(SNAP / "records/FR_VARIANTS.json")
    candidates = read(SNAP / "records/FR_SOURCE_LINK_CANDIDATES.json")["variants"]
    report = read(SNAP / "records/FR_APPARATUS_SOURCE_LINKS.json")
    links = report["variants"]
    decisions = read(HERE / "resolved_decisions.json")
    old_manual = {r["variant_id"]: r for r in rows(SNAP / "review/final_apparatus_links/manual_links.jsonl")}
    latest_manual_path = ROOT / "review/final_apparatus_links/manual_links.jsonl"
    latest_manual = {r["variant_id"]: r for r in rows(latest_manual_path)}
    missing_sources = {sid for row in latest_manual.values() for sid in row["source_ids"]} - decisions.keys()
    additions = {}
    if missing_sources:
        # This loader only reads the live resolved records.  Preserve the initial
        # 1482-record input and record subsequently introduced manual sources
        # separately, with their original review_file provenance.
        sys.path.insert(0, str(ROOT / "scripts"))
        from fr_source_links import load_decisions
        _, raw_by_id, current_decisions = load_decisions()
        additions = {sid: current_decisions[sid] for sid in sorted(missing_sources)}
        write("additional_registry_records.json", {sid: raw_by_id.get(sid) for sid in sorted(missing_sources)})
    write("additional_resolved_decisions.json", additions)
    decisions.update(additions)
    shutil.copy2(latest_manual_path, HERE / "manual_links_at_validation.jsonl")
    repeat_path = ROOT / "review/final_apparatus_links/repeated_full_variant_pairs.json"
    shutil.copy2(repeat_path, HERE / "repeated_full_variant_pairs.json")
    short = read(SNAP / "review/final_apparatus_links/short_pair_ambiguities.json")
    repeats = read(repeat_path)
    numeric = rows(ROOT / "review/global_numeric_headings/post_review_patches.jsonl")
    bodies = {}
    for layer in ("diplomatic", "current"):
        body = (SNAP / f"build/FR_{layer}_revised.tex").read_text()
        body = body.split(r"\begin{document}", 1)[1].rsplit(r"\end{document}", 1)[0]
        pages = split_pages(body)
        for patch in numeric:
            page = str(patch["page"])
            assert pages[page].count(patch["new"]) == 1, (layer, patch["source_id"])
            pages[page] = pages[page].replace(patch["new"], patch["old"], 1)
        bodies[layer] = pages
    assert len(variants) == len(candidates) == len(links) == 970
    assert [v["id"] for v in variants] == [f"FRV{i:04d}" for i in range(1, 971)]
    tsv = list(csv.DictReader((SNAP / "records/FR_VARIANTS.tsv").open(), delimiter="\t"))
    assert len(tsv) == 970
    audits = []
    short_ids = {r["id"] for r in short if max(map(len, r["pair"])) <= 5}
    ambiguous_ids = {r["id"] for r in short if len(r["sources"]) > 1}
    repeat_ids = {v for r in repeats for v in r["ids"]}
    weak_ids = set()
    proof_counts = Counter()
    for v, c, link, table in zip(variants, candidates, links, tsv):
        vid = v["id"]
        page = str(v["page"])
        errors = []
        check((vid, v["page"], v["printed"], v["corrected"]) ==
              (c["variant_id"], c["page"], c["printed"], c["corrected"]), "candidate identity", errors)
        check(vid == link["variant_id"] and v["page"] == link["page"], "report identity", errors)
        check(v["source"] == link["source_ids"], "cached variant/report source IDs", errors)
        for key in ["id", "page", "printed", "corrected", "status", "sha256_printed", "sha256_corrected"]:
            check(str(v[key]) == table[key], "TSV exact " + key, errors)
        check(json.loads(table["source"]) == v["source"], "TSV exact source IDs", errors)
        for layer, text_key, offset_key in (("diplomatic", "printed", "diplomatic_page_offset"),
                                            ("current", "corrected", "corrected_page_offset")):
            value = v[text_key]
            at = v[offset_key]
            check(bodies[layer][page][at:at + len(value)] == value, layer + " exact body location", errors)
            check(sha(value) == v["sha256_" + text_key] == link["sha256_" + text_key], text_key + " hash", errors)
        expected_edits = deltas(v["printed"], v["corrected"])
        check([{k: x[k] for k in expected_edits[0]} for x in c["edits"]] == expected_edits,
              "complete character-edit inventory", errors)
        if link["component_proofs"]:
            check([{k: x[k] for k in expected_edits[0]} for x in link["component_proofs"]] == expected_edits,
                  "report covers every character edit", errors)
            selected = []
            for component, candidate in zip(link["component_proofs"], c["edits"]):
                corr = component["selected_correspondence"]
                selected.append(corr["source_id"])
                check(corr == candidate["matches"][0], "selected candidate is the cached first match", errors)
                aa, bb = corr["source_pair_printed"], corr["source_pair_corrected"]
                if corr.get("proof") == "one exact source-pair replacement reconstructs this whole branch variant":
                    proof_counts["whole_replacement"] += 1
                    check(bool(aa) and v["printed"].count(aa) == 1 and v["printed"].replace(aa, bb, 1) == v["corrected"],
                          "whole replacement reconstruction", errors)
                else:
                    proof_counts["literal_component"] += 1
                    si, sj = corr["source_pair_printed_edit"]
                    sk, sl = corr["source_pair_corrected_edit"]
                    check(aa[si:sj] == component["printed"] and bb[sk:sl] == component["corrected"],
                          "literal component source slices", errors)
                    left, right = corr["common_left_literal"], corr["common_right_literal"]
                    check(aa[:si].endswith(left) and aa[sj:].startswith(right),
                          "recorded printed source literal context", errors)
                    for layer, offset_key, edit_key in (("diplomatic", "diplomatic_page_offset", "printed_offsets"),
                                                        ("current", "corrected_page_offset", "corrected_offsets")):
                        start, end = component[edit_key]
                        body = bodies[layer][page]
                        at = v[offset_key]
                        # The generator stores the printed context string and
                        # the minimum of two branch-specific matching lengths.
                        # It does not assert that the two branches' neighboring
                        # strings are mutually identical across another edit.
                        source, a_start, a_end = (aa, si, sj) if layer == "diplomatic" else (bb, sk, sl)
                        branch_left = source[a_start - len(left):a_start]
                        branch_right = source[a_end:a_end + len(right)]
                        check(body[:at + start].endswith(branch_left) and body[at + end:].startswith(branch_right),
                              layer + " literal body context", errors)
                    check(corr["literal_context_characters"] == len(left) + len(right), "context length", errors)
                    if len(left) + len(right) < 6:
                        weak_ids.add(vid)
            check(list(dict.fromkeys(selected)) == link["source_ids"], "component sources exhaust report source IDs", errors)
        else:
            check(vid in old_manual, "manual proof exists for nonautomatic link", errors)
        for selected in link["source_decisions"]:
            sid = selected["source_id"]
            base = decisions[sid]
            for key in ["page", "printed_reading", "image", "region", "reason", "review_file"]:
                check(selected.get(key, "") == base.get(key, ""), f"resolved provenance {sid}/{key}", errors)
            check(bool(base.get("image")) and bool(base.get("reason")), f"source evidence {sid}", errors)
            check(not base["verdict"].startswith(("pending", "reverted", "rejected")), f"accepted disposition {sid}", errors)
            check(str(base["page"]) in [page, "front"], f"source folio {sid}", errors)
        effective = latest_manual.get(vid)
        if effective:
            for key in ["page", "printed", "corrected", "sha256_printed", "sha256_corrected"]:
                check(effective[key] == v[key], "latest manual exact " + key, errors)
            for sid in effective["source_ids"]:
                check(sid in decisions, "latest manual source exists " + sid, errors)
                if sid in decisions:
                    base = decisions[sid]
                    check(str(base["page"]) in [page, "front"] and bool(base.get("image")) and bool(base.get("reason")) and
                          not base["verdict"].startswith(("pending", "reverted", "rejected")),
                          "latest manual accepted source evidence " + sid, errors)
        audits.append(dict(variant_id=vid, page=v["page"],
                           printed=v["printed"], corrected=v["corrected"],
                           sha256_printed=v["sha256_printed"], sha256_corrected=v["sha256_corrected"],
                           cached_source_ids=link["source_ids"],
                           effective_source_ids=effective["source_ids"] if effective else link["source_ids"],
                           mechanical_checks="passed" if not errors else "failed", errors=errors,
                           source_context_file="diplomatic_variant_contexts.json#" + vid))
    for row in audits:
        vid = row["variant_id"]
        row["risk_flags"] = [name for name, values in [
            ("literal_context_under_six", weak_ids), ("source_pair_at_most_five", short_ids),
            ("multiple_short_pair_candidates", ambiguous_ids), ("repeated_whole_pair_on_same_page", repeat_ids),
            ("manual_context_link", set(latest_manual))] if vid in values]
    write("all_970_mechanical_audit.json", audits)
    write("risk_inventory.json", [r for r in audits if r["risk_flags"]])
    summary = dict(variants=len(audits), mechanical_passed=sum(not r["errors"] for r in audits),
                   failed=[r for r in audits if r["errors"]], proof_components=dict(proof_counts),
                   original_report_manual_count=report["summary"]["manual_contextual_links"],
                   initial_snapshot_manual_count=len(old_manual), latest_manual_count=len(latest_manual),
                   latest_manual_sha256=sha(latest_manual_path.read_text()),
                   weak_context_variants=len(weak_ids), tiny_pair_variants=len(short_ids),
                   multiple_short_pair_variants=len(ambiguous_ids), repeated_pair_groups=len(repeats),
                   repeated_pair_variants=len(repeat_ids), risk_union=len({r["variant_id"] for r in audits if r["risk_flags"]}),
                   body_location_checks=1940, exact_numeric_font_inversions_in_memory=98,
                   source_text_modified=False, source_decisions_modified=False,
                   qualification="Mechanical literal correspondence does not alone prove occurrence attribution. See semantic occurrence audit.")
    write("MECHANICAL_VALIDATION.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "failed"}, ensure_ascii=False))
    for row in summary["failed"]:
        print(row["variant_id"], row["errors"])


if __name__ == "__main__":
    main()
