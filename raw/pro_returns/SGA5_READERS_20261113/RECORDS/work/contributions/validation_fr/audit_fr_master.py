#!/usr/bin/env python3
"""Independently audit the French annotated master and bilingual reader credits.

Run from the supplied project root. This script reads the prepared inputs and
readers; it writes only its two audit reports beside this script. It does not
import any reader-generation or source-projection implementation.
"""
from __future__ import annotations

import bisect
import csv
import difflib
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


OUT = Path("work/contributions/validation_fr")
PREP = Path("work/build/prepared")
SNAPSHOT: dict[str, bytes] = {}


def read(path: str | Path) -> str:
    p = Path(path)
    key = p.as_posix()
    if key not in SNAPSHOT:
        SNAPSHOT[key] = p.read_bytes()
    return SNAPSHOT[key].decode("utf-8")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def command_end(text: str, pos: int) -> int:
    """Read one TeX control word/symbol, including escaped braces and percent."""
    assert text[pos] == "\\"
    pos += 1
    if pos >= len(text):
        return pos
    if text[pos].isalpha() or text[pos] == "@":
        while pos < len(text) and (text[pos].isalpha() or text[pos] == "@"):
            pos += 1
        return pos
    return pos + 1


def group(text: str, pos: int) -> tuple[str, int]:
    """Read one balanced TeX group without changing its bytes."""
    while pos < len(text):
        if text[pos].isspace():
            pos += 1
        elif text[pos] == "%":
            eol = text.find("\n", pos)
            pos = len(text) if eol < 0 else eol + 1
        else:
            break
    if pos >= len(text) or text[pos] != "{":
        raise ValueError(f"Missing balanced argument at character {pos}")
    start = pos + 1
    depth = 1
    pos += 1
    while pos < len(text):
        char = text[pos]
        if char == "\\":
            pos = command_end(text, pos)
            continue
        if char == "%":
            eol = text.find("\n", pos)
            pos = len(text) if eol < 0 else eol + 1
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:pos], pos + 1
        pos += 1
    raise ValueError(f"Unclosed balanced argument at character {start - 1}")


# Six source folios fall inside a word split across the print's page boundary.
# Their comment markers are intentionally inline and must not acquire an extra
# space before the continuation. Recognize those authentic markers as well.
MARKER = re.compile(r"%%%%%%%%%%[ \t]+scan idx (\d+)[ \t]+\|[ \t]+folio (\d+)[ \t]+%%%%%%%%%%")


def folio_at(text: str, pos: int) -> int | None:
    markers = list(MARKER.finditer(text, 0, pos))
    return int(markers[-1][2]) if markers else None


def parse_master(text: str) -> tuple[str, str, list[dict]]:
    """Project both branches, recognizing calls rather than text in comments."""
    pos = end_of_copy = 0
    diplomatic: list[str] = []
    corrected: list[str] = []
    rows = []
    while pos < len(text):
        if text[pos] == "%":
            eol = text.find("\n", pos)
            pos = len(text) if eol < 0 else eol + 1
            continue
        if text[pos] != "\\":
            pos += 1
            continue
        end = command_end(text, pos)
        if text[pos:end] != r"\SGAvar":
            pos = end
            continue
        before, end = group(text, end)
        after, end = group(text, end)
        ident, end = group(text, end)
        diplomatic.extend((text[end_of_copy:pos], before))
        corrected.extend((text[end_of_copy:pos], after))
        rows.append({
            "id": ident,
            "page": folio_at(text, pos),
            "line": text.count("\n", 0, pos) + 1,
            "before": before,
            "after": after,
            "offset": pos,
            "end": end,
            "nested_variant": r"\SGAvar" in before or r"\SGAvar" in after,
        })
        pos = end_of_copy = end
    diplomatic.append(text[end_of_copy:])
    corrected.append(text[end_of_copy:])
    return "".join(diplomatic), "".join(corrected), rows


def differences(actual: str, expected: str) -> list[dict]:
    """Localize every raw discrepancy; never discard arbitrary whitespace."""
    actual_lines = actual.splitlines(keepends=True)
    expected_lines = expected.splitlines(keepends=True)
    actual_starts = [0]
    expected_starts = [0]
    for line in actual_lines:
        actual_starts.append(actual_starts[-1] + len(line))
    for line in expected_lines:
        expected_starts.append(expected_starts[-1] + len(line))
    out = []
    for tag, a, b, c, d in difflib.SequenceMatcher(None, actual_lines, expected_lines, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        aa, bb = "".join(actual_lines[a:b]), "".join(expected_lines[c:d])
        for inner, i, j, k, l in difflib.SequenceMatcher(None, aa, bb, autojunk=False).get_opcodes():
            if inner == "equal":
                continue
            actual_pos, expected_pos = actual_starts[a] + i, expected_starts[c] + k
            left, right = aa[i:j], bb[k:l]
            suffix_actual = actual[actual_starts[a] + j:]
            suffix_expected = expected[expected_starts[c] + l:]
            # A single endline immediately before display close is discarded by
            # TeX in math mode. No text-mode whitespace receives this exemption.
            display_is_open_actual = actual.rfind(r"\[", 0, actual_pos) > actual.rfind(r"\]", 0, actual_pos)
            display_is_open_expected = expected.rfind(r"\[", 0, expected_pos) > expected.rfind(r"\]", 0, expected_pos)
            display_endline = (
                {left, right} == {"", "\n"}
                and suffix_actual.startswith(r"\]")
                and suffix_expected.startswith(r"\]")
                and display_is_open_actual and display_is_open_expected
            )
            initial_empty_lines = actual_pos == expected_pos == 0 and not left.strip() and not right.strip()
            actual_gap = re.search(r"\n*$", actual[:actual_pos])[0] + left + re.match(r"\n*", suffix_actual)[0]
            expected_gap = re.search(r"\n*$", expected[:expected_pos])[0] + right + re.match(r"\n*", suffix_expected)[0]
            redundant_empty_line = (
                {left, right} == {"", "\n"} and len(actual_gap) >= 2 and len(expected_gap) >= 2
                and r"\obeylines" not in actual and r"\obeylines" not in expected
            )
            approved = display_endline or initial_empty_lines or redundant_empty_line
            reason = "No nonprinting exemption established."
            if display_endline:
                reason = "Single endline immediately before an open display's closing \\]; TeX discards it in math mode."
            elif initial_empty_lines:
                reason = "Empty lines at body start precede all printed material and are ignored in vertical mode."
            elif redundant_empty_line:
                reason = "One redundant empty line in a run that already terminates the paragraph in both strings; repeated \\par in vertical mode adds no printed content."
            out.append({
                "page": folio_at(expected, expected_pos),
                "projected_line": actual.count("\n", 0, actual_pos) + 1,
                "reference_line": expected.count("\n", 0, expected_pos) + 1,
                "projected_text": left,
                "reference_text": right,
                "context_before": expected[max(0, expected_pos - 100):expected_pos],
                "context_after": suffix_expected[:100],
                "whitespace_only": (not left or left.isspace()) and (not right or right.isspace()),
                "proven_nonprinting": approved,
                "reason": reason,
            })
    return out


def marker_audit(text: str) -> dict:
    pairs = [(int(m[1]), int(m[2])) for m in MARKER.finditer(text)]
    expected = [p for p in range(1, 485) if p != 435]
    return {
        "count": len(pairs),
        "expected_count": 483,
        "ordered_folios_match": [p for _, p in pairs] == expected,
        "every_scan_index_is_folio_plus_11": all(i == p + 11 for i, p in pairs),
        "folio_435_absent": all(p != 435 for _, p in pairs),
        "duplicates": [p for p, n in Counter(p for _, p in pairs).items() if n != 1],
        "inline_word_boundary_folios": [int(m[2]) for m in MARKER.finditer(text) if m.start() and text[m.start() - 1] != "\n"],
        "pass": len(pairs) == 483 and [p for _, p in pairs] == expected and all(i == p + 11 for i, p in pairs),
    }


def page_text(text: str, page: int) -> str:
    markers = list(MARKER.finditer(text))
    for index, marker in enumerate(markers):
        if int(marker[2]) == page:
            return text[marker.end():markers[index + 1].start() if index + 1 < len(markers) else len(text)]
    raise ValueError(f"Missing page {page}")


READERS = {
    "FR": ["SGA5_FR_diplomatique.tex", "SGA5_FR_corrige_apparat.tex", "SGA5_FR_texte_de_lecture.tex", "SGA5_FR_master_annotated.tex"],
    "EN": ["SGA5_EN_diplomatic.tex", "SGA5_EN_corrected_apparatus.tex", "SGA5_EN_reading.tex", "SGA5_EN_master_annotated.tex"],
}


def reader_forms(language: str) -> dict:
    inputs = []
    for name in READERS[language]:
        path = Path("deliverables") / language / name
        text = read(path)
        lines = text.splitlines(keepends=True)
        inputs.append((path.as_posix(), text, lines))
    reference_tail = "".join(inputs[1][2][2:])
    rows = []
    for index, (path, text, lines) in enumerate(inputs):
        selector = rf"\def\SGAform{{{index}}}" if index < 3 else r"\providecommand{\SGAform}{1}"
        rows.append({
            "file": path,
            "sha256": digest(text),
            "header": lines[0].rstrip("\r\n"),
            "selector": lines[1].rstrip("\r\n"),
            "selector_correct": lines[1].rstrip("\r\n") == selector,
            "bytes_after_first_two_lines_equal": "".join(lines[2:]) == reference_tail,
            "common_tail_sha256": digest("".join(lines[2:])),
        })
    master = inputs[-1][1]
    semantics = {
        "form_zero_uses_first_argument_other_forms_second": r"\protected\long\def\SGAvar#1#2#3{\ifnum\SGAform=0\relax#1\else#2\SGAmark{#3}\fi}" in master,
        "editorial_calls_guarded_by_form_one": "\\DeclareRobustCommand{\\SGAmark}[1]{%\n  \\ifnum\\SGAform=1\\relax\\ifSGAcontents\\else" in master,
        "apparatus_guarded_by_form_one": master.split("% SGA5_BODY_END", 1)[1].lstrip().startswith(r"\ifnum\SGAform=1\relax"),
    }
    return {"files": rows, "master_default_form": 1, "selector_semantics": semantics, "pass": all(row["selector_correct"] and row["bytes_after_first_two_lines_equal"] for row in rows) and all(semantics.values())}


def reader_body_incorporation(reader: str, body: str, reference: str) -> tuple[dict, str]:
    """Remove only the explicitly added folio/contents wrappers, not content."""
    transformations = []
    margin_pattern = re.compile(r"\\SGAFolio\{(\d+)\}(\\SGAFolioGap)?%\n")
    margins = list(margin_pattern.finditer(body))
    unwrapped = margin_pattern.sub("", body)
    transformations.append({"operation": "remove added marginal folio commands", "count": len(margins), "gap_notices_at": [int(m[1]) for m in margins if m[2]]})
    toc_pattern = re.compile(r"^\\phantomsection\\addcontentsline\{toc\}\{section\}\{[^\n]+\}\n", re.M)
    toc = toc_pattern.findall(unwrapped)
    unwrapped = toc_pattern.sub("", unwrapped)
    transformations.append({"operation": "remove added invisible contents entries", "count": len(toc), "exact_commands": toc})
    equivalent_headings = {
        r"\SGAtopheading{": (r"\section*{", r"\newcommand{\SGAtopheading}[1]{\SGAoriginalsection*{#1}\SGAcontentsentry{section}{#1}}"),
        r"\SGAprintedtopheading{": (r"\section*{", r"\newcommand{\SGAprintedtopheading}[1]{\SGAoriginalsection*{#1}}"),
        r"\SGAlevelheading{": (r"\subsection*{", r"\newcommand{\SGAlevelheading}[1]{\SGAoriginalsubsection*{#1}\SGAcontentsentry{subsection}{#1}}"),
    }
    heading_definitions_valid = True
    for old, (new, definition) in equivalent_headings.items():
        heading_definitions_valid = heading_definitions_valid and definition in reader
        transformations.append({"operation": "restore original heading command with identical printed argument", "before": old, "after": new, "count": unwrapped.count(old), "definition_confirmed": definition in reader})
        unwrapped = unwrapped.replace(old, new)
    # The marker-delimited reader body includes one separator endline immediately
    # before BODY_END. Remove precisely that wrapper endline, not strip().
    if unwrapped.endswith("\n"):
        unwrapped = unwrapped[:-1]
        transformations.append({"operation": "remove one wrapper separator endline immediately before BODY_END", "count": 1})
    diffs = differences(unwrapped, reference)
    expected_folios = [p for p in range(1, 485) if p != 435]
    result = {
        "transformations": transformations,
        "all_marginal_folios_in_order": [int(m[1]) for m in margins] == expected_folios,
        "one_gap_notice_at_436": [int(m[1]) for m in margins if m[2]] == [436],
        "heading_definitions_confirm_printed_equivalence": heading_definitions_valid,
        "unwrapped_body_byte_exact": unwrapped == reference,
        "unwrapped_body_sha256": digest(unwrapped),
        "prepared_body_sha256": digest(reference),
        "remaining_differences": diffs,
        "pass": unwrapped == reference and heading_definitions_valid and [int(m[1]) for m in margins] == expected_folios and [int(m[1]) for m in margins if m[2]] == [436],
    }
    return result, unwrapped


def folio248_token_proof(annotated: str, variants: list[dict]) -> dict:
    row = next(v for v in variants if v["id"] == "FR-0525")
    call = annotated[row["offset"]:row["end"]]
    probe = read(OUT / "folio248_token_boundary_probe.tex")
    metadata = json.loads(read(OUT / "folio248_probe_input.json"))
    transcript = read(OUT / "folio248_token_boundary_probe.log")
    expected = [
        "COMMENT_ENDLINE_DISCARDED=PASS", "FIRST_ARGUMENT_BEGIN", "LEADING_SPACE=PASS",
        "NO_PAR_TOKEN=PASS", "FIRST_ARGUMENT_END", "SECOND_ARGUMENT_EMPTY=PASS",
        "FOLLOWING_INPUT_BEGIN", "LEADING_SPACE=PASS", "NO_PAR_TOKEN=PASS", "FOLLOWING_INPUT_END",
    ]
    observed = [line for line in transcript.splitlines() if line in set(expected) or "=FAIL" in line]
    checks = {
        "probe_contains_the_exact_current_variant_call": call in probe and metadata["exact_call_sha256"] == digest(call),
        "probe_file_hash_matches": metadata["probe_sha256"] == digest(probe),
        "all_ten_TeX_token_observations_match": observed == expected,
        "diplomatic_argument_starts_with_endline_then_display": row["before"].startswith("\n\\["),
        "corrected_argument_is_empty": row["after"] == "",
        "following_actual_input_starts_with_endline_then_display": annotated[row["end"]:].startswith("\n\\["),
        "marker_termination_is_immediately_before_the_call": annotated[:row["offset"]].endswith("%%%%%%%%%%  scan idx 259  |  folio 248  %%%%%%%%%%\n"),
    }
    result = {
        "variant": "FR-0525", "folio": 248,
        "command": "source work/toolchain/env.sh; pdftex -ini -interaction=nonstopmode -halt-on-error -output-directory=work/contributions/validation_fr work/contributions/validation_fr/folio248_token_boundary_probe.tex",
        "probe": "work/contributions/validation_fr/folio248_token_boundary_probe.tex",
        "probe_sha256": digest(probe), "variant_call_sha256": digest(call),
        "observations": observed, "checks": checks,
        "interpretation": "The percent comment discards its own endline. TeX tokenizes the endline after the first argument's opening brace as one space, with no paragraph token. The corrected argument is empty; the actual input endline after the complete call is also one space, with no paragraph token. Raw textual substitution places two physical endlines next to one another, but that serialization does not retain TeX's argument-scanning state. The printed mathematical tokens are unchanged; the raw endline discrepancy is retained explicitly in the projection report.",
        "pass": all(checks.values()),
    }
    (OUT / "FOLIO248_TOKEN_PROOF.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


def audit_french() -> dict:
    annotated = read(PREP / "FR_annotated_body.tex")
    diplomatic, corrected, variants = parse_master(annotated)
    expected_d = read(PREP / "FR_diplomatic_body.tex")
    expected_c = read(PREP / "FR_corrected_body.tex")
    ledger = json.loads(read(PREP / "FR_variants_ordered.json"))
    declared = {row["id"]: row for row in ledger}
    actual = {row["id"]: row for row in variants}
    boundary_proof = folio248_token_proof(annotated, variants)
    variants_equal = [
        {"id": row["id"], "before_equal": row["before"] == declared.get(row["id"], {}).get("before"),
         "after_equal": row["after"] == declared.get(row["id"], {}).get("after"),
         "page_equal": row["page"] == declared.get(row["id"], {}).get("page")}
        for row in variants
    ]
    projections = {}
    for label, projected, reference in [("diplomatic", diplomatic, expected_d), ("corrected", corrected, expected_c)]:
        diffs = differences(projected, reference)
        for diff in diffs:
            if (boundary_proof["pass"] and diff["page"] == 248 and diff["projected_text"] == "\n" and diff["reference_text"] == ""
                    and diff["context_before"].endswith("%%%%%%%%%%  scan idx 259  |  folio 248  %%%%%%%%%%\n")
                    and diff["context_after"].startswith(r"\[")):
                diff["proven_nonprinting"] = True
                diff["reason"] = "Explicit TeX token probe of the exact FR-0525 call proves that the marker endline is discarded and the argument/following endlines yield ordinary spaces, not paragraph tokens. The extra raw endline arises only when argument strings are reserialized; see FOLIO248_TOKEN_PROOF.json."
        projections[label] = {
            "projected_sha256": digest(projected), "reference_sha256": digest(reference),
            "raw_byte_exact": projected == reference,
            "projected_characters": len(projected), "reference_characters": len(reference),
            "discrepancies": diffs, "discrepancy_count": len(diffs),
            "every_discrepancy_proven_nonprinting": all(d["proven_nonprinting"] for d in diffs),
            "pass": not diffs or all(d["proven_nonprinting"] for d in diffs),
        }
    scans = list(csv.DictReader(read("work/contributions/scans/PLACES_98_DECIDED.tsv").splitlines(), delimiter="\t"))
    scan_rows = []
    for scan in scans:
        row = actual.get(scan["id"], {})
        d_glyph, c_glyph = scan["diplomatic_reading"], scan["corrected_reading"]
        bd, bc = row.get("before", ""), row.get("after", "")
        suffix_d = bd[len(d_glyph):] if bd.startswith(d_glyph) else None
        suffix_c = bc[len(c_glyph):] if bc.startswith(c_glyph) else None
        immediate_suffix = annotated[row["end"]:row["end"] + 1] if row else ""
        passed = (row.get("page") == int(scan["folio"]) and suffix_d is not None and suffix_d == suffix_c and immediate_suffix not in ("_", "^"))
        scan_rows.append({
            "id": scan["id"], "folio": int(scan["folio"]),
            "diplomatic_reading": bd, "corrected_reading": bc,
            "ledger_glyphs_match": suffix_d is not None and suffix_c is not None,
            "identical_attached_scripts": suffix_d == suffix_c and suffix_d is not None,
            "attached_scripts": suffix_d,
            "no_script_left_outside_variant": immediate_suffix not in ("_", "^"),
            "pass": passed,
        })
    h75_d = "par $F'/G_{x'}$ l'endomorphisme"
    h75_c = "par $f'/G_{x'}$ l'endomorphisme"
    fnu_d = r"avec $F$ annulé par $\ell^{\nu+1}$"
    fnu_c = r"avec $F_\nu$ annulé par $\ell^{\nu+1}$"
    g98 = r"\underline{\operatorname{\mathbb{F}r}}_{Y/S}:Y\longrightarrow Y^{(p/S)}"
    checks = {
        "H75": {"folio": 433, "diplomatic_exact": h75_d in page_text(diplomatic, 433), "corrected_exact": h75_c in page_text(corrected, 433), "source": "PORT_5_REPORT.md:H75; OPEN_ITEMS_DECIDED.tsv:H75"},
        "SOL-EN-084": {"folio": 472, "diplomatic_exact": fnu_d in page_text(diplomatic, 472), "corrected_exact": fnu_c in page_text(corrected, 472), "source": "SOL-EN-084; OPEN_ITEMS_DECIDED.tsv:SOL-EN-084"},
        "GLOBAL-98b": {"folio": 441, "diplomatic_exact": g98 in page_text(diplomatic, 441), "corrected_exact": g98 in page_text(corrected, 441), "no_variant_at_this_expression": g98 in page_text(annotated, 441), "source": "conventions/GLOBAL_ISSUES_SGA.md:98; OPEN_ITEMS_DECIDED.tsv:GLOBAL-98b"},
    }
    for row in checks.values():
        row["pass"] = row["diplomatic_exact"] and row["corrected_exact"] and row.get("no_variant_at_this_expression", True)
    forms = reader_forms("FR")
    reader_text = read("deliverables/FR/SGA5_FR_master_annotated.tex")
    reader_body = reader_text.split("% SGA5_BODY_START\n", 1)[1].split("% SGA5_BODY_END", 1)[0]
    incorporation, unwrapped_reader_body = reader_body_incorporation(reader_text, reader_body, annotated)
    _, _, reader_variants = parse_master(reader_body)
    _, _, unwrapped_reader_variants = parse_master(unwrapped_reader_body)
    reader_variant_content = [(r["id"], r["before"], r["after"], r["page"]) for r in unwrapped_reader_variants]
    prepared_variant_content = [(r["id"], r["before"], r["after"], r["page"]) for r in variants]
    markers = {
        "annotated_body": marker_audit(annotated), "diplomatic_projection": marker_audit(diplomatic),
        "corrected_projection": marker_audit(corrected), "reader_master_body": marker_audit(reader_body),
    }
    ids = [row["id"] for row in variants]
    integrity = {
        "variant_count": len(variants), "expected_count": 1061,
        "final_reader_master_active_variant_count": len(reader_variants),
        "unique_ids": len(set(ids)) == len(ids),
        "ids_equal_ordered_ledger": ids == [r["id"] for r in ledger],
        "all_exact_ledger_readings_and_pages": all(r["before_equal"] and r["after_equal"] and r["page_equal"] for r in variants_equal),
        "ledger_mismatches": [r for r in variants_equal if not all(r[k] for k in ("before_equal", "after_equal", "page_equal"))],
        "equal_branch_variants": [r["id"] for r in variants if r["before"] == r["after"]],
        "nested_variant_calls": [r["id"] for r in variants if r["nested_variant"]],
        "reader_body_variant_content_and_order_equal": reader_variant_content == prepared_variant_content,
        "reader_variant_comparison_mapping": "Only the exact documented folio, contents and heading-wrapper reversal shown in reader_body_incorporation is applied before comparing variant IDs, both argument strings and folios. No coordinate-only or text normalization is used. The unwrapped entire body is byte-exact.",
    }
    integrity["pass"] = (len(variants) == 1061 and integrity["unique_ids"] and integrity["ids_equal_ordered_ledger"] and integrity["all_exact_ledger_readings_and_pages"] and not integrity["equal_branch_variants"] and not integrity["nested_variant_calls"] and integrity["reader_body_variant_content_and_order_equal"])
    result = {
        "audit": "Independent balanced-argument French master projection and reader consistency",
        "method": "This script independently reads three balanced arguments for every actual SGAvar call, respecting escaped braces and comments. It preserves all other characters, compares both projected strings against the two prepared bodies, and enumerates every raw difference. It imports no generator code.",
        "source_reference": "work/build/prepared/FR_annotated_body.tex",
        "annotated_body_sha256": digest(annotated),
        "projections": projections, "variant_integrity": integrity,
        "folio_markers": markers,
        "scan_ledger": {"source": "work/contributions/scans/PLACES_98_DECIDED.tsv", "count": len(scan_rows), "method": "Exact branch and folio comparison to the separately completed scan decision ledger; this audit does not claim a new visual inspection.", "rows": scan_rows, "pass": len(scan_rows) == 32 and all(r["pass"] for r in scan_rows) and {r["id"] for r in scan_rows} == {f"R98-{n:02d}" for n in range(1, 33)}},
        "specific_decisions": checks, "reader_forms": forms,
        "reader_body_incorporation": incorporation,
        "folio248_token_boundary_proof": boundary_proof,
    }
    result["pass"] = (all(r["pass"] for r in projections.values()) and integrity["pass"] and all(r["pass"] for r in markers.values()) and result["scan_ledger"]["pass"] and all(r["pass"] for r in checks.values()) and forms["pass"] and incorporation["pass"])
    return result


NAMES = [
    "Alexander Grothendieck", "Michèle Raynaud", "Michel Raynaud", "Pierre Deligne", "Nicholas Katz",
    "Michel Demazure", "Michael Artin", "Jean-Louis Verdier", "Luc Illusie", "Bas Edixhoven", "Yves Laszlo",
    "L. Bayle", "N. Borne", "O. Brinon", "J. Buresi", "M. Chardin", "F. Ducrot", "P. Graftiaux", "F. Han",
    "P. Karwasz", "L. Koelblen", "D. Madore", "S. Morel", "D. Naie", "B. Osserman", "J. Riou", "V. Sécherre",
    "C. Sabbah", "Jacob C. Reinhold", "Philippe Gille", "Patrick Polo", "Fabrice Orgogozo", "Daniel Miller",
    "I. Bucur", "C. Houzel", "J.-P. Jouanolou", "J.-P. Serre",
]
RIGHTS_EN = "The rights in the original work belong to its author or the author's representatives or heirs. Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, they are dedicated to the public domain under CC0 1.0. This edition is published for educational, non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and object to its publication here, please open a GitHub issue and we will take it down."
RIGHTS_FR = r"Les droits sur l'ouvrage original appartiennent \`a son auteur ou aux repr\'esentants ou h\'eritiers de l'auteur. Dans la mesure o\`u nous d\'etenons des droits sur la transcription, la traduction, les corrections et la composition produites par IA, ces droits sont d\'edi\'es au domaine public sous CC0 1.0. Cette \'edition est publi\'ee \`a des fins \'educatives et non lucratives, et nous ne revendiquons aucun droit que nous ne d\'etenons pas. Si vous d\'etenez des droits sur cet ouvrage et vous opposez \`a sa publication ici, veuillez ouvrir une issue GitHub et nous le retirerons."
BUILD_CREDIT = "GPT-6 Astra (OpenAI, ChatGPT Pro mode)"
AI_WORDS = ["AI-transcribed", "AI-translated", "AI-produced corrections"]


def search_text(text: str) -> str:
    # A text-only search view for accent-coded names; no source is modified.
    accents = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303"}
    text = re.sub(r"\\(['`^\"~])\{([A-Za-z])\}", lambda m: unicodedata.normalize("NFC", m[2] + accents[m[1]]), text)
    text = re.sub(r"\\(['`^\"~])([A-Za-z])", lambda m: unicodedata.normalize("NFC", m[2] + accents[m[1]]), text)
    text = text.replace(r"\c{c}", "ç").replace(r"\c{C}", "Ç").replace("~", " ")
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text))


def privacy_findings(text: str) -> list[dict]:
    patterns = {
        "email": r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
        "absolute_local_path": r"(?:/workspace/|/home/|/root/|/mnt/data/|file://|\b[A-Za-z]:[\\/][A-Za-z0-9_. -]+[\\/][A-Za-z0-9_. -]+)",
    }
    out = []
    # Colon followed by TeX control sequences can resemble a Windows drive.
    # The following complete arrow fragments occur in the mathematical body;
    # they have been inspected as maps, and contain no filesystem component.
    mathematical_arrow = re.compile(
        r"\b[A-Za-z]:\\(?:bar\\eta\\to|cC\\(?:to|times)\\cC|cE\\to\\cE|"
        r"Ab\\longrightarrow\\Ab|cA\\to\\cA/\\cB|cB\\to\\cA|"
        r"lambda\\rightsquigarrow\\lambda|mathcal C\\to\\mathcal D|mathbb Z_\\ell\\text)"
    )
    for kind, pattern in patterns.items():
        for m in re.finditer(pattern, text):
            if kind == "absolute_local_path" and mathematical_arrow.match(text, m.start()):
                continue
            out.append({"kind": kind, "line": text.count("\n", 0, m.start()) + 1})
    return out


def audit_credits() -> dict:
    source_paths = [
        "work/sources/SGA5_EN/en/repo/README.md", "work/sources/SGA5_EN/en/repo/ATTRIBUTION.md",
        "work/sources/SGA5_EN/en/repo/SOURCE_AUTHORITY.md",
        "work/sources/SGA5_EN/en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex",
    ]
    sources = {p: search_text(read(p)) for p in source_paths}
    source_evidence = []
    for name in NAMES:
        hits = [p.removeprefix("work/sources/SGA5_EN/") for p, t in sources.items() if name in t]
        source_evidence.append({"name": name, "present_in_supplied_credit_sources": bool(hits), "sources": hits})
    prompt = search_text(read("upload/PROMPT(20261112-230204).md"))
    prompt_exact_rights = RIGHTS_EN in prompt
    entries = []
    for language, names in READERS.items():
        for name in names:
            path = Path("deliverables") / language / name
            text = read(path)
            front = text.split(r"\begin{document}", 1)[1].split("% SGA5_BODY_START", 1)[0]
            searchable = search_text(front)
            credit_rows = [{"name": person, "present": person in searchable} for person in NAMES]
            rights = RIGHTS_EN if language == "EN" else RIGHTS_FR
            findings = privacy_findings(text)
            # These are literal source checks, including the content nested in
            # the form selector. All three branches share this front matter.
            row = {
                "file": path.as_posix(), "language": language, "sha256": digest(text),
                "human_names_expected": 37, "human_names_found": sum(r["present"] for r in credit_rows),
                "names": credit_rows,
                "AI_wording": {phrase: phrase in front for phrase in AI_WORDS},
                "forbidden_assistance_label_absent": "AI-assisted" not in text,
                "build_credit_exact": BUILD_CREDIT in front,
                "rights_literal_exact": rights in front,
                "rights_occurrences": front.count(rights),
                "third_party_CC_BY_notice_retained": "CC BY 4.0" in searchable and "Reinhold" in searchable,
                "printed_frontmatter_omissions_declared": all(x in searchable for x in ("iii--viii", "Liste des SGA", "Table des mati")),
                "bibliographic_589_1977_Springer_present": all(x in searchable for x in ("Mathematics 589", "Springer-Verlag", "1977")),
                "privacy_findings": findings,
            }
            row["pass"] = (row["human_names_found"] == 37 and all(row["AI_wording"].values()) and row["forbidden_assistance_label_absent"] and row["build_credit_exact"] and row["rights_literal_exact"] and row["rights_occurrences"] == 1 and row["third_party_CC_BY_notice_retained"] and row["printed_frontmatter_omissions_declared"] and row["bibliographic_589_1977_Springer_present"] and not findings)
            entries.append(row)
    result = {
        "audit": "All six reader sources plus both annotated masters: human credits, mandated wording, rights and privacy",
        "method": "The 37-name inventory is checked against the supplied repository attribution documents and original ported English edition credit, then against every front matter. Accent decoding and nonbreaking-space replacement are used only in a search view for names. The rights statements and build credit are checked as literal source strings. No source file is changed.",
        "human_credit_count": len(NAMES), "source_evidence": source_evidence,
        "English_rights_exactly_equal_user_instruction": prompt_exact_rights,
        "rights_EN": RIGHTS_EN,
        "French_rights_translation_checked": RIGHTS_FR,
        "reader_sources": entries,
        "English_forms_consistency": reader_forms("EN"),
        "privacy_scope": "Complete text of all eight reader/master TeX files; report findings contain type and line only, never the potentially private value. The script explicitly distinguishes inspected mathematical arrow fragments such as F: followed by TeX control words from Windows-drive syntax.",
    }
    result["pass"] = (all(r["present_in_supplied_credit_sources"] for r in source_evidence) and prompt_exact_rights and all(r["pass"] for r in entries) and result["English_forms_consistency"]["pass"])
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    french = audit_french()
    credits = audit_credits()
    modified = [name for name, data in SNAPSHOT.items() if Path(name).read_bytes() != data]
    for result in (french, credits):
        result["inputs_stable_during_audit"] = not modified
        result["inputs_changed_during_audit"] = modified
        result["pass"] = result["pass"] and not modified
    (OUT / "INDEPENDENT_FR_MASTER_AUDIT.json").write_text(json.dumps(french, ensure_ascii=False, indent=2) + "\n")
    (OUT / "READERS_CREDITS_AUDIT.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"FR_master_pass": french["pass"], "credits_pass": credits["pass"], "variants": french["variant_integrity"]["variant_count"], "projection_discrepancies": {k: v["discrepancy_count"] for k, v in french["projections"].items()}, "inputs_changed": modified}, ensure_ascii=False))


if __name__ == "__main__":
    main()
