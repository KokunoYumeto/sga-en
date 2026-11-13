#!/usr/bin/env python3
"""Resolve French apparatus provenance by exact source-coordinate witnesses.

Read-only by default. --apply changes source/reason metadata only in the two
prepared variant catalogues, after proving that every ID and reading is kept.
All coordinates are zero-based half-open Unicode-character or UTF-8-byte ranges
as expressly labelled; line and column coordinates are one-based.
"""
from __future__ import annotations

import argparse
import bisect
import difflib
import hashlib
import json
import re
from array import array
from collections import Counter
from pathlib import Path

from audit_fr_master import MARKER, command_end, group, parse_master


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def json_write(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


class Mapped:
    """Every emitted character retains the exact original source interval."""
    def __init__(self, text, lo=None, hi=None):
        self.text = text
        self.lo = array("I", range(len(text))) if lo is None else lo
        self.hi = array("I", range(1, len(text) + 1)) if hi is None else hi

    def cut(self, start, end):
        return Mapped(self.text[start:end], self.lo[start:end], self.hi[start:end])

    def replace(self, start, end, new, events, kind, **details):
        low = min(self.lo[start:end]) if start < end else (self.lo[start] if start < len(self.text) else self.hi[-1])
        high = max(self.hi[start:end]) if start < end else low
        event = {"event": len(events) + 1, "kind": kind, "original_start": low, "original_end": high,
                 "input_tex": self.text[start:end], "output_tex": new, **details}
        events.append(event)
        self.text = self.text[:start] + new + self.text[end:]
        self.lo[start:end] = array("I", [low]) * len(new)
        self.hi[start:end] = array("I", [high]) * len(new)
        return event

    def sub(self, pattern, replacement, events, kind, **details):
        matches = list(re.finditer(pattern, self.text))
        for match in reversed(matches):
            new = replacement(match) if callable(replacement) else match.expand(replacement)
            self.replace(match.start(), match.end(), new, events, kind, **details)
        return len(matches)


def concatenate(parts):
    return Mapped("".join(p.text for p in parts), array("I", (x for p in parts for x in p.lo)), array("I", (x for p in parts for x in p.hi)))


def line_parts(mapped):
    pos = 0
    for line in mapped.text.splitlines(keepends=True):
        yield mapped.cut(pos, pos + len(line))
        pos += len(line)


FOLIO = re.compile(r"%{5,}[ \t]*scan idx[ \t]+(\d+)[ \t]*\|[ \t]*folio[ \t]+(\d+)[ \t]*%+[ \t]*")
ALIAS = {r"\RHom": r"\RHomCore", r"\uRHom": r"\underline{\RHom}", r"\RGamma": r"\R\Gamma",
         r"\RGc": r"\R\Gamma_c", r"\RG": r"\R\Gamma", r"\Rpi": r"\R\pi", r"\Rj": r"\R j", r"\rG": r"\R\Gamma^G"}


def initial_definitions(original, body_start, layer):
    active = {}
    pattern = re.compile(r"\\(newcommand|providecommand|renewcommand)\s*\{")
    preamble = original[:body_start]
    for match in pattern.finditer(preamble):
        try:
            macro, end = group(preamble, match.end() - 1)
            if macro not in set(ALIAS) | {r"\R", r"\RHomCore"}:
                continue
            value, end = group(preamble, end)
        except ValueError:
            continue
        if match[1] == "providecommand" and macro in active:
            continue
        active[macro] = {"macro": macro, "value": value, "source_start": match.start(), "source_end": end,
                         "source_tex": preamble[match.start():end]}
    expected = {**ALIAS, r"\R": r"\mathbb{R}" if layer == "diplomatic" else r"\mathrm{R}",
                r"\RHomCore": r"\mathbb{R}\mathrm{Hom}" if layer == "diplomatic" else r"\mathrm{RHom}"}
    for macro, value in expected.items():
        assert active.get(macro, {}).get("value") == value, (layer, macro, active.get(macro), value)
    return active


def patch_source(original, layer, scans, events):
    mapped = Mapped(original)
    for decision in reversed(scans["decisions"]):
        ref = decision["fr_" + layer]
        start, end = ref["start"], ref["end"]
        assert mapped.text[start:end] == ref["source_tex"]
        new = decision["diplomatic_reading" if layer == "diplomatic" else "corrected_reading"]
        mapped.replace(start, end, new, events, "build patch", source_id=decision["id"], folio=decision["folio"])
    if layer == "current":
        changes = [
            ("OPEN-H75", 433, "par $F'/G_{x'}$ l'endomorphisme", "par $f'/G_{x'}$ l'endomorphisme"),
            ("SOL-EN-084", 472, r"avec $F$ annulé par $\ell^{\nu+1}$", r"avec $F_\nu$ annulé par $\ell^{\nu+1}$"),
        ]
        for ident, folio, old, new in changes:
            assert mapped.text.count(old) == 1, ident
            pos = mapped.text.index(old)
            mapped.replace(pos, pos + len(old), new, events, "build patch", source_id=ident, folio=folio)
        markers = list(FOLIO.finditer(mapped.text))
        marker = next(m for m in markers if int(m[2]) == 441)
        end = markers[markers.index(marker) + 1].start()
        old, new = r"\Fr_{Y/S}", r"\underline{\operatorname{\mathbb{F}r}}_{Y/S}"
        assert mapped.text[marker.end():end].count(old) == 1
        pos = mapped.text.index(old, marker.end(), end)
        mapped.replace(pos, pos + len(old), new, events, "build patch", source_id="GLOBAL-98b", folio=441)
    return mapped


def expand_with_origins(patched, original, layer, events):
    start = patched.text.index(r"\begin{document}") + len(r"\begin{document}")
    end = patched.text.rindex(r"\end{document}")
    definitions = initial_definitions(original, original.index(r"\begin{document}"), layer)
    body = patched.cut(start, end)
    stripped = []
    for line in line_parts(body):
        if FOLIO.fullmatch(line.text.rstrip("\n")):
            stripped.append(line)
            continue
        pos = 0
        while pos < len(line.text):
            if line.text[pos] == "\\":
                pos += 2
            elif line.text[pos] == "%":
                line.replace(pos, len(line.text), "", events, "discard source comment and its endline")
                break
            else:
                pos += 1
        stripped.append(line)
    body = concatenate(stripped)
    r = definitions[r"\R"]["value"]
    core = definitions[r"\RHomCore"]["value"]
    u = r"\underline{" + core + "}"
    active_r = definitions[r"\R"]
    active_u = definitions[r"\uRHom"]
    output = []
    page = 0
    for line in line_parts(body):
        marker = FOLIO.fullmatch(line.text.rstrip("\n"))
        if marker:
            page = int(marker[2]); output.append(line); continue
        match = re.search(r"\\renewcommand\{\\R\}\{(\\(?:mathrm|mathbb)\{R\})\}", line.text)
        if match:
            r = match[1]
            active_r = {"macro": r"\R", "value": r, "source_start": min(line.lo[match.start():match.end()]),
                        "source_end": max(line.hi[match.start():match.end()]), "source_tex": match[0]}
            line.replace(match.start(), match.end(), "", events, "activate scoped R definition", definition=active_r, folio=page)
        match = re.search(r"\\renewcommand\{\\uRHom\}.*?(?=\n|$)", line.text)
        if match:
            if r"\mathrm{R}\underline{\mathrm{Hom}}" in match[0]:
                u = r"\mathrm{R}\underline{\mathrm{Hom}}"
            elif r"\underline{\RHom}" in match[0]:
                u = r"\underline{" + core + "}"
            else:
                raise ValueError("Unrecognized scoped internal derived Hom")
            active_u = {"macro": r"\uRHom", "value": u, "source_start": min(line.lo[match.start():match.end()]),
                        "source_end": max(line.hi[match.start():match.end()]), "source_tex": match[0]}
            line.replace(match.start(), match.end(), "", events, "activate scoped internal derived Hom definition", definition=active_u, folio=page)
        if re.match(r"\s*\\(?:providecommand|newcommand|renewcommand|DeclareMathOperator|newenvironment|renewenvironment)", line.text):
            output.append(line); continue
        protect = r"(\\(?:underline|overline|hat|widehat|tilde|widetilde|bar|vec|dot|ddot|check|ol|wt|wh|mathrm|mathbf|mathbb|mathcal)\s*)(\\(?:RHomCore|RHom|uRHom|RGamma|RGc|RG|Rpi|Rj|rG|R))(?![A-Za-z@])"
        line.sub(protect, lambda m: m[1] + "{" + m[2] + "}", events, "brace one-token font or accent argument before expanding it", folio=page)
        replacements = {r"\uRHom": u, r"\RHomCore": core, r"\RHom": core, r"\RGamma": r + r"\Gamma", r"\RGc": r + r"\Gamma_c",
                        r"\RG": r + r"\Gamma", r"\Rpi": r + r"\pi", r"\Rj": r + "j", r"\rG": r + r"\Gamma^G", r"\R": r}
        for macro, value in replacements.items():
            witness_definitions = [active_u] if macro == r"\uRHom" else [definitions[r"\RHomCore"]] if macro in (r"\RHomCore", r"\RHom") else [active_r]
            if macro not in (r"\R", r"\RHomCore"):
                witness_definitions = [definitions[macro], *witness_definitions]
            line.sub(re.escape(macro) + r"(?![A-Za-z@])", lambda m, value=value: value, events, "literal expansion of source macro", macro=macro, definitions=witness_definitions, folio=page)
        line.sub(r"\\(mathrm|mathbb|mathcal|mathbf|mathfrak|mathscr)\s+([A-Za-z0-9])", r"\\\1{\2}", events, "brace the same single-character font argument", folio=page)
        output.append(line)
    return concatenate(output), definitions


def projected_positions(annotated, variants):
    pos_d = pos_c = previous = 0
    result = []
    for row in variants:
        common = row["offset"] - previous
        pos_d += common; pos_c += common
        result.append({**row, "diplomatic_projected_start": pos_d, "diplomatic_projected_end": pos_d + len(row["before"]),
                       "current_projected_start": pos_c, "current_projected_end": pos_c + len(row["after"])})
        pos_d += len(row["before"]); pos_c += len(row["after"])
        previous = row["end"]
    return result


def exact_alignment(a, b):
    al, bl = a.splitlines(keepends=True), b.splitlines(keepends=True)
    ai, bi = [0], [0]
    for line in al: ai.append(ai[-1] + len(line))
    for line in bl: bi.append(bi[-1] + len(line))
    blocks = []
    for tag, x, y, u, v in difflib.SequenceMatcher(None, al, bl, autojunk=False).get_opcodes():
        if tag == "equal":
            blocks.append((ai[x], bi[u], ai[y] - ai[x])); continue
        aa, bb = "".join(al[x:y]), "".join(bl[u:v])
        blocks.extend((ai[x] + m.a, bi[u] + m.b, m.size) for m in difflib.SequenceMatcher(None, aa, bb, autojunk=False).get_matching_blocks() if m.size)
    return sorted(blocks)


def locate_interval(projection, reference, blocks, start, end):
    reading = projection[start:end]
    for a, b, size in blocks:
        if a <= start and end <= a + size:
            mapped_start = b + start - a
            assert reference[mapped_start:mapped_start + len(reading)] == reading
            return mapped_start, mapped_start + len(reading), "exact equal-character alignment block"
    # FR-0525's leading endline borders the explicitly proven comment boundary.
    following = next((block for block in blocks if block[0] >= start), None)
    previous = next((block for block in reversed(blocks) if block[0] + block[2] <= start), None)
    approx = following[1] - (following[0] - start) if following else previous[1] + previous[2] + start - previous[0] - previous[2]
    candidates = [p for p in range(max(0, approx - 3), min(len(reference), approx + 3) + 1) if reference[p:p + len(reading)] == reading]
    assert len(candidates) == 1, (start, end, repr(reading[:50]), candidates)
    return candidates[0], candidates[0] + len(reading), "exact full reading at the recorded one-endline boundary adjustment"


def positions(text):
    return [0, *[m.end() for m in re.finditer("\n", text)]]


def line_column(starts, offset):
    index = bisect.bisect_right(starts, offset) - 1
    return [index + 1, offset - starts[index] + 1]


def folio_range(text, folio):
    markers = list(FOLIO.finditer(text))
    marker = next(m for m in markers if int(m[2]) == folio)
    index = markers.index(marker)
    return marker.end(), markers[index + 1].start() if index + 1 < len(markers) else len(text)


def witness(layer, mapped, original, prepared, start, end, mapping_kind, events, starts):
    low = min(mapped.lo[start:end]) if start < end else (mapped.lo[start] if start < len(mapped.text) else mapped.hi[-1])
    high = max(mapped.hi[start:end]) if start < end else low
    relevant = [event["event"] for event in events if event["original_start"] < max(high, low + 1) and event["original_end"] > low]
    quote = original[low:high]
    return {
        "archive": "SGA5_FR.zip", "path_in_zip": f"fr/sga5/{layer}/s5.tex", "layer": layer,
        "original_character_range": [low, high], "original_UTF8_byte_range": [len(original[:low].encode()), len(original[:high].encode())],
        "original_start_line_column": line_column(starts, low), "original_end_line_column": line_column(starts, high),
        "exact_original_source_tex": quote, "original_context_before": original[max(0, low - 110):low], "original_context_after": original[high:high + 110],
        "prepared_file": f"prepared/FR_{'diplomatic' if layer == 'diplomatic' else 'corrected'}_body.tex",
        "prepared_character_range": [start, end], "exact_prepared_reading": prepared[start:end],
        "projection_to_prepared_mapping": mapping_kind, "transformation_events": relevant,
        "source_interval_policy": "Every emitted character carries its exact original source interval. A literal macro expansion maps to its original macro token and its source-definition witnesses. An empty branch is an exact source boundary with both neighboring contexts.",
    }


REGISTERS = {"MISPRINTS_5": "fixes/MISPRINTS_5.json", "FIXLOG_5": "fixes/FIXLOG_5.jsonl",
             "FIXLOG_5_CURRENT": "fixes/FIXLOG_5_CURRENT.jsonl", "HANDFIX_5": "fixes/HANDFIX_5.jsonl"}


def load_registers(source):
    result = {}
    for label, path in REGISTERS.items():
        text = (source / path).read_text()
        data = json.loads(text) if path.endswith(".json") else [json.loads(line) for line in text.splitlines() if line.strip()]
        for ordinal, row in enumerate(data, 1):
            result[f"{label}:{ordinal:04d}"] = {"path": path, "ordinal": ordinal, "row": row}
    return result


def overlaps(interval, changed):
    a, b = interval; c, d = changed
    if a == b or c == d:
        return a <= c <= b or c <= a <= d
    return max(a, c) < min(b, d)


def validate_register(ident, record, before, after, originals, page):
    data = record["row"]
    old = data.get("old", data.get("print", ""))
    new = data.get("new", data.get("correct", ""))
    result = {"id": ident, "path_in_zip": record["path"], "one_based_record": record["ordinal"], "retained": False}
    if not isinstance(old, str) or not isinstance(new, str) or not old or not new or old == new:
        result["reason"] = "Record lacks two distinct nonempty literal source strings."; return result
    locations = []
    for layer, needle in (("diplomatic", old), ("current", new)):
        lo, hi = folio_range(originals[layer], page)
        hits = [lo + m.start() for m in re.finditer(re.escape(needle), originals[layer][lo:hi])]
        if len(hits) != 1:
            result["reason"] = "Full literal old/new fields do not each occur exactly once in the two source folios. Narrative register descriptions are not treated as source text."; return result
        locations.append(hits[0])
    matching = []
    for tag, a, b, c, d in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == "equal": continue
        di, ci = [locations[0] + a, locations[0] + b], [locations[1] + c, locations[1] + d]
        if overlaps(before["original_character_range"], di) and overlaps(after["original_character_range"], ci):
            matching.append({"diplomatic_changed_range": di, "current_changed_range": ci, "old": old[a:b], "new": new[c:d]})
    result["retained"] = bool(matching)
    result["matching_exact_changed_components"] = matching
    result["reason"] = "Both complete literal record fields locate uniquely at this folio, and an actual changed component intersects both exact variant source intervals." if matching else "The record strings locate, but their actual changed components do not cover this variant in both layers."
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="work/sources/SGA5_FR")
    parser.add_argument("--prepared", default="work/build/prepared")
    parser.add_argument("--contributions", default="work/contributions")
    parser.add_argument("--out", default="work/contributions/validation_fr")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    source, prep, contributions, out = map(Path, (args.sources, args.prepared, args.contributions, args.out))
    out.mkdir(parents=True, exist_ok=True)
    scans = json.loads((contributions / "scans/PLACES_98_PATCHES.json").read_text())
    originals, mapped_bodies, events_by_layer, reproduction = {}, {}, {}, {}
    for layer in ("diplomatic", "current"):
        original = (source / f"fr/sga5/{layer}/s5.tex").read_bytes().decode("utf-8")
        originals[layer] = original
        events = []
        patched = patch_source(original, layer, scans, events)
        patched_reference = (prep / f"FR_{layer}_source.tex").read_text()
        assert patched.text == patched_reference, (layer, "patched source mismatch")
        expanded, definitions = expand_with_origins(patched, original, layer, events)
        body_file = f"FR_{'diplomatic' if layer == 'diplomatic' else 'corrected'}_body.tex"
        reference = (prep / body_file).read_text()
        assert expanded.text == reference, (layer, "expanded body mismatch", sha(expanded.text), sha(reference))
        mapped_bodies[layer] = expanded; events_by_layer[layer] = events
        reproduction[layer] = {"archive_source": f"fr/sga5/{layer}/s5.tex", "original_sha256": sha(original),
                               "patched_source_sha256": sha(patched.text), "prepared_body_sha256": sha(reference),
                               "patched_source_byte_exact": True, "prepared_body_byte_exact": True,
                               "initial_source_definitions": definitions, "event_counts": dict(Counter(e["kind"] for e in events))}
    annotated = (prep / "FR_annotated_body.tex").read_text()
    dip_projection, current_projection, calls = parse_master(annotated)
    calls = projected_positions(annotated, calls)
    catalogue = json.loads((prep / "FR_variants.json").read_text())
    catalogue_by_id = {row["id"]: row for row in catalogue}
    assert len(calls) == len(catalogue) == 1061
    assert {row["id"] for row in calls} == set(catalogue_by_id)
    alignments = {"diplomatic": exact_alignment(dip_projection, mapped_bodies["diplomatic"].text),
                  "current": exact_alignment(current_projection, mapped_bodies["current"].text)}
    projections = {"diplomatic": dip_projection, "current": current_projection}
    starts = {layer: positions(originals[layer]) for layer in originals}
    registers = load_registers(source)
    witnesses, resolved, discarded = [], {}, []
    for call in calls:
        original_row = catalogue_by_id[call["id"]]
        assert (call["before"], call["after"], call["page"]) == (original_row["before"], original_row["after"], original_row["page"])
        pair = {}
        for layer in ("diplomatic", "current"):
            start, end, mapping = locate_interval(projections[layer], mapped_bodies[layer].text, alignments[layer], call[layer + "_projected_start"], call[layer + "_projected_end"])
            pair[layer] = witness(layer, mapped_bodies[layer], originals[layer], mapped_bodies[layer].text, start, end, mapping, events_by_layer[layer], starts[layer])
            assert pair[layer]["exact_prepared_reading"] == call["before" if layer == "diplomatic" else "after"]
        validations = []
        for ident in re.findall(r"(?:MISPRINTS_5|FIXLOG_5_CURRENT|FIXLOG_5|HANDFIX_5):\d{4}", original_row["source"]):
            validations.append(validate_register(ident, registers[ident], pair["diplomatic"], pair["current"], originals, call["page"]))
        retained = [v["id"] for v in validations if v["retained"]]
        discarded.extend({"variant_id": call["id"], **v} for v in validations if not v["retained"])
        direct = []
        pure_r = call["before"].replace(r"\mathbb{R}\mathrm{Hom}", r"\mathrm{RHom}").replace(r"\mathbb{R}", r"\mathrm{R}") == call["after"] and call["before"] != call["after"]
        if pure_r and any(events_by_layer[layer][e - 1]["kind"] == "literal expansion of source macro" for layer in pair for e in pair[layer]["transformation_events"]):
            direct.append("conventions/GLOBAL_ISSUES_SGA.md:98")
        if call["id"].startswith("R98-"):
            scan = next(d for d in scans["decisions"] if d["id"] == call["id"])
            assert call["before"].startswith(scan["diplomatic_reading"]) and call["after"].startswith(scan["corrected_reading"])
            assert call["before"][len(scan["diplomatic_reading"]):] == call["after"][len(scan["corrected_reading"]):]
            direct.extend(["PLACES_98_DECIDED.tsv:" + call["id"], "conventions/GLOBAL_ISSUES_SGA.md:98"])
        for event_id in pair["current"]["transformation_events"]:
            event = events_by_layer["current"][event_id - 1]
            if event["kind"] == "build patch" and event.get("source_id") in ("OPEN-H75", "SOL-EN-084"):
                direct.append("OPEN_ITEMS_DECIDED.tsv:" + event["source_id"])
        citations = retained + list(dict.fromkeys(direct))
        citations.append("FR_SOURCE_WITNESSES.json:" + call["id"])
        for layer in ("diplomatic", "current"):
            citations.append(pair[layer]["path_in_zip"] + ":L" + str(pair[layer]["original_start_line_column"][0]))
        row = {**original_row, "source": "; ".join(citations)}
        if not call["id"].startswith("R98-"):
            row["reason"] = "The two exact readings have source-layer interval witnesses at this folio. The witness records every source macro expansion and build edit affecting these intervals."
            if retained:
                row["reason"] += " The cited register entries have uniquely located literal old/new fields and overlapping changed components in both layers."
            if "conventions/GLOBAL_ISSUES_SGA.md:98" in direct:
                row["reason"] += " The complete difference is the recorded derived-functor glyph convention."
        resolved[call["id"]] = row
        witnesses.append({"id": call["id"], "folio": call["page"], "before": call["before"], "after": call["after"],
                          "annotated_master_character_range": [call["offset"], call["end"]],
                          "diplomatic": pair["diplomatic"], "current": pair["current"],
                          "prior_source_citation": original_row["source"], "register_validations": validations,
                          "retained_direct_decision_sources": list(dict.fromkeys(direct)), "resolved_source_citation": row["source"]})
    final_catalogue = [resolved[row["id"]] for row in catalogue]
    immutable_fields = ["id", "page", "expose", "before", "after", "kind"]
    assert all(all(old.get(k) == new.get(k) for k in immutable_fields) for old, new in zip(catalogue, final_catalogue))
    report = {
        "variant_count": len(witnesses), "exact_layer_interval_witnesses": 2 * len(witnesses),
        "all_prepared_readings_equal_variant_arguments": True, "all_original_sources_replayed_to_prepared_layers_exactly": True,
        "source_reproduction": reproduction,
        "register_citations_checked": sum(len(w["register_validations"]) for w in witnesses),
        "register_citations_retained": sum(v["retained"] for w in witnesses for v in w["register_validations"]),
        "register_citations_removed": len(discarded), "removed_citation_evidence": discarded,
        "source_metadata_changed": sum(old["source"] != new["source"] for old, new in zip(catalogue, final_catalogue)),
        "all_ids_readings_pages_and_order_preserved": True,
        "direct_sources": dict(Counter(source.split(":")[0] for w in witnesses for source in w["retained_direct_decision_sources"])),
        "matching_policy": "No substring-score attribution. A legacy register ID survives only when its entire old and new literal fields each locate uniquely within the exact two original source folios and an actual non-equal record component overlaps both variant source intervals. Other entries cite their exact witnessed source layers. Source-macro and current-build changes have separate explicit proof events.",
        "scope": "Provenance metadata only; no mathematical token, body, variant ID, folio or call position is changed.",
        "pass": True,
    }
    json_write(out / "FR_SOURCE_WITNESSES.json", {"coordinate_convention": __doc__, "source_reproduction": reproduction, "transformation_events": events_by_layer, "variants": witnesses})
    json_write(out / "FR_SOURCE_RESOLUTION_REPORT.json", report)
    json_write(out / "FR_VARIANTS_RESOLVED.json", final_catalogue)
    if args.apply:
        for name in ("FR_variants.json", "FR_variants_ordered.json"):
            path = prep / name
            if not path.exists(): continue
            original = json.loads(path.read_text())
            replacement = [{**row, "source": resolved[row["id"]]["source"], "reason": resolved[row["id"]]["reason"]} for row in original]
            assert all(all(old.get(k) == new.get(k) for k in immutable_fields) for old, new in zip(original, replacement))
            json_write(path, replacement)
    print(json.dumps({k: report[k] for k in ("variant_count", "exact_layer_interval_witnesses", "register_citations_checked", "register_citations_retained", "register_citations_removed", "pass")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
