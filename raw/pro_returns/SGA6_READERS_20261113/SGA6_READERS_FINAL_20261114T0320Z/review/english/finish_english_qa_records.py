#!/usr/bin/env python3
"""Record completed, bounded output observations and source-macro dispositions.

This script records the individual images actually inspected by the English
assembler; it does not perform or claim an automated visual inspection.
"""
from pathlib import Path
import hashlib
import json
import shutil
import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "visual_qa_final"
LAYOUT = OUT / "released_layout"
AGG = HERE / "aggregate"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


APP_OBSERVATIONS = {
    "app_front_001.png": "Editorial preface, retained-source limitations, AI and human attribution, and the explicit contemporary-template attribution for the masked publisher notice are legible. No overlap or clipping observed.",
    "app_front_002.png": "Continued named source credits and rights statement are legible, with no overlap or clipping observed.",
    "app_front_003.png": "Original cover title and contributor block, followed by the original series notice, are legible. Original leaf markers remain visible.",
    "app_front_004.png": "Original manuscript instructions, eight Physics catalogue entries and the beginning of the repeated series title are legible. The series title continues onto the following output page; its text remains in source order.",
    "app_front_005.png": "Original publisher notice, ISBNs, copyright text, contributor title leaf and original Preface are legible. The two certified intervening blank leaves have no stacked visible labels.",
    "app_folio_008.png": "The distinguished triangle, formula labels and the original folio-8 boundary are legible, without collision.",
    "app_folio_008_continuation.png": "The original note call and note label have a raised star inside baseline parentheses. Note text and separator are distinct from the body.",
    "app_folio_041.png": "The four plain numerical statement references and the baseline parenthesized-star call beside formula (2.10) are visible. The note and two-row diagram are legible.",
    "app_folio_374.png": "The original folio boundary and projective-bundle formulas are legible; this output page precedes the original note.",
    "app_folio_374_continuation.png": "The parenthesized-star call and the full J.-P. Jouanolou note are legible. The note remains separated from the body.",
    "app_folio_393.png": "The source-local general-linear-group label renders with capital G and lowercase l. The adjacent formulas and section-4 heading remain legible.",
    "app_folio_440.png": "The exterior-power, Tor and exact-sequence formulas around the original folio boundary are legible.",
    "app_folio_440_continuation.png": "The four direct-image maps fit on the two recorded rows, in their unchanged order. No line protrusion or overlap observed. The source's incomplete '(IV' locator remains visible as adjudicated.",
    "app_folio_543.png": "The paragraph responsible for badness 3271 is legible. Its wider spaces do not cause clipping, overlap or formula loss.",
    "app_folio_606.png": "The two original diagrams and the ordinary display-side label 3.2 are legible. The folio-606 marker remains outside math.",
    "app_folio_606_continuation.png": "The 'Finally, let g' paragraph responsible for badness 1092 is legible, including the adjacent variant markers. No clipping or overlap observed.",
    "app_folio_630.png": "The Hilbert-polynomial paragraph responsible for badness 1325 is legible. Formula operands, intervening prose and following lemma remain distinct.",
    "app_folio_650.png": "Theorem 5.1, responsible for badness 1048, has wider interword spaces but remains legible, with no clipping or overlap.",
    "app_folio_662.png": "The ruled paragraph responsible for badness 1975 and the following lemma remain legible. The source word rules do not cross the formulas or obliterate punctuation.",
    "app_folio_681.png": "The restored double-struck coefficient-ring glyphs in the section-5 title and following formulas are visible. No layout collision observed.",
}


def visual_record():
    app = HERE / "final/SGA6_EN_corrected_apparatus.pdf"
    reading = HERE / "final/SGA6_EN_reading.pdf"
    plan = json.loads((LAYOUT / "VISUAL_PLAN.json").read_text())
    assert plan["pdf_sha256"] == digest(app)
    rows = {Path(row["image"]).name: row for row in plan["plan"]}
    for number in (4, 5):
        image = LAYOUT / f"app_front_{number:03d}.png"
        rows[image.name] = dict(source_folio="original front", pdf_page=number,
                               image=image.relative_to(ROOT).as_posix(),
                               image_sha256=digest(image))
    observed = []
    for name, observation in APP_OBSERVATIONS.items():
        row = dict(rows[name])
        assert row["image_sha256"] == digest(ROOT / row["image"])
        row.update(status="directly viewed in the final PDF render",
                   observation=observation, concrete_defect_observed=False,
                   pdf=app.relative_to(ROOT).as_posix(), pdf_sha256=digest(app))
        observed.append(row)
    apparatus_plan = json.loads((LAYOUT / "APPARATUS_VISUAL_PLAN.json").read_text())
    assert apparatus_plan["pdf_sha256"] == digest(app)
    apparatus_observations = {
        "app_apparatus_first.png": "The opening apparatus entries give legible identifiers, original folios, scan/witness references, both readings and their reasons. Mathematical readings are typeset; no clipping or collision observed.",
        "app_apparatus_393.png": "Entries 324 and 325 preserve the source-local Gl expansion in both readings. The diplomatic one/two rules and corrected group-scheme/group-sheaf typography remain distinct and legible; no macro-state drift is visible.",
        "app_apparatus_681.png": "Entries 673–675 retain the local double-struck Zell and the separately underlined Q readings. Both source and corrected coefficient formulas, locators and reasons are legible; no macro-state drift is visible.",
    }
    for row in apparatus_plan["plan"]:
        row = dict(row)
        assert row["image_sha256"] == digest(ROOT / row["image"])
        row.update(source_folio=row["marker"], status="directly viewed in the final PDF render",
                   observation=apparatus_observations[Path(row["image"]).name],
                   concrete_defect_observed=False, pdf=app.relative_to(ROOT).as_posix(),
                   pdf_sha256=digest(app))
        observed.append(row)
    rp = json.loads((LAYOUT / "READING_VISUAL_PLAN.json").read_text())
    assert rp["pdf_sha256"] == digest(reading)
    for row in rp["plan"]:
        assert row["image_sha256"] == digest(ROOT / row["image"])
        row = dict(row)
        row.update(status="directly viewed in the final PDF render",
                   observation=("The original source-folio label and the corresponding heading are on this same output page. "
                                "The title, byline where present and opening text are legible, with no clipping or overlap."),
                   concrete_defect_observed=False,
                   pdf=reading.relative_to(ROOT).as_posix(), pdf_sha256=digest(reading))
        observed.append(row)
    starts = ["1", "78", "160", "222", "274", "297", "365", "416",
              "466", "498", "519", "595", "616", "667"]
    document = fitz.open(reading)
    heading_rows = []
    for label in starts:
        matches = [(i + 1, w[1]) for i, page in enumerate(document)
                   for w in page.get_text("words")
                   if w[0] > 530 and w[4] == label]
        assert len(matches) == 1 and matches[0][1] < 100, (label, matches)
        heading_rows.append(dict(source_folio=int(label), pdf_page=matches[0][0],
                                 marker_top_pt=matches[0][1],
                                 evidence="PDF text-position extraction; individually rendered checks are listed separately"))
    late_path = HERE / "visual_qa_late/VISUAL_QA.json"
    late = json.loads(late_path.read_text())
    # The linked report contains the independently checked final PDF hash.
    assert digest(app) in json.dumps(late)
    report = dict(
        scope="Bounded final-output visual inspection, not a claim that every output page was visually inspected.",
        directly_viewed_images=len(observed),
        corrected_apparatus_images=sum(r["pdf"] == app.relative_to(ROOT).as_posix() for r in observed),
        reading_images=sum(r["pdf"] == reading.relative_to(ROOT).as_posix() for r in observed),
        observations=observed,
        all_fourteen_reading_start_labels_on_fresh_output_pages=heading_rows,
        additional_independent_late_QA=dict(path=late_path.relative_to(ROOT).as_posix(),
                                         sha256=digest(late_path)),
        concrete_defects_observed=0,
        retained_diagnostics="Five underfull paragraphs in the apparatus/master and four in the diplomatic/reading forms. Each distinct reported paragraph was directly viewed in the corrected-apparatus render. These warnings are retained in the full compile receipts.",
        earlier_captures="Earlier pre-title-start captures remain explicitly superseded and are not counted as final visual evidence.",
    )
    dump(OUT / "VISUAL_QA.json", report)
    text = ["# Final English output inspection", "",
            report["scope"], "",
            f"{len(observed)} images were individually viewed by the English assembler: 23 corrected-apparatus pages and 5 reading-form pages. "
            "The independent late reviewer viewed eight additional images at seven requested source loci; the exact report is linked in the JSON.",
            "", "No clipping or overlapping content was observed in these checks. The five distinct underfull paragraphs remain legible; their compiler warnings are preserved.",
            "", "| Form | Source folio | Output page | Observation |", "|---|---|---:|---|"]
    for row in observed:
        form = "reading" if row["pdf"] == reading.relative_to(ROOT).as_posix() else "corrected apparatus"
        text.append(f"| {form} | {row['source_folio']} | {row['pdf_page']} | {row['observation']} |")
    (OUT / "VISUAL_QA.md").write_text("\n".join(text) + "\n")
    return report


def macro_closure():
    path = AGG / "MACRO_EXPANSION_STATIC_AUDIT.json"
    audit = json.loads(path.read_text())
    decisions_path = HERE / "EN_MACRO_EXPANSION_DECISIONS.json"
    decisions = {d["id"]: d for d in json.loads(decisions_path.read_text())}
    ids = {"red": "EN-AGG-MACRO-RED-502", "longg": "EN-AGG-MACRO-LENGTH-520",
           "naif": "EN-AGG-MACRO-NAIF-698"}
    counts = {"red": 0, "longg": 0, "naif": 0}
    rows = []
    for d in audit["differences"]:
        command = d["command"]
        assert command in ids
        decision = decisions[ids[command]]
        assert sum(d["French"].values()) == sum(d["English"].values())
        counts[command] += sum(d["French"].values())
        rows.append(dict(page=d["page"], command=command, French=d["French"], English=d["English"],
                         disposition="approved source-scoped lexical label transport",
                         decision_id=decision["id"], exact_identity_or_translation_map=decision["proof"]))
    assert len(rows) == 11 and counts == {"red": 20, "longg": 2, "naif": 4}
    equal_glyph_rows = [d for d in audit["equal"] if d["command"] in {"GL", "Zell", "Qell"}
                       and (d["page"] == 393 or 681 <= d["page"] <= 685)]
    report = dict(
        static_audit=path.relative_to(ROOT).as_posix(), static_audit_sha256=digest(path),
        decision_file=decisions_path.relative_to(ROOT).as_posix(), decision_file_sha256=digest(decisions_path),
        equal_page_command_groups=audit["equal_page_command_groups"],
        approved_lexical_page_command_groups=len(rows), unresolved_page_command_groups=0,
        literal_invocations_in_approved_groups=counts, dispositions=rows,
        exact_source_glyph_repairs=[
            dict(decision=decisions["EN-AGG-MACRO-GL-393"], result="Source-local Gl expansion restored; corresponding post-transport groups compare equal."),
            dict(decision=decisions["EN-AGG-MACRO-ZELL_QELL-681"], result="Source-local double-struck coefficient-ring expansions restored; corresponding post-transport groups compare equal."),
        ],
        post_transport_equal_glyph_groups=equal_glyph_rows,
        apparatus_local_state_capture="aggregate/APPARATUS_MACRO_STATES.json records the actual TeX let-captures placed at the source uses and restored for the apparatus entries.",
        limitation="This closes each unequal group found by the declared static expansion audit. It does not assert that a conservative declaration parser establishes all TeX semantics; actual four-form compilation and bounded output inspection are separate evidence.",
    )
    dump(AGG / "MACRO_EXPANSION_CLOSURE.json", report)
    return report


def font_record(visual, macro):
    old = HERE / "EN_FONT_RENDERING_RECORD.json"
    historical = HERE / "EN_FONT_RENDERING_RECORD_001_296_HISTORICAL.json"
    if not historical.exists():
        shutil.copy2(old, historical)
    typo = json.loads((AGG / "TYPOGRAPHY_TRANSPORT.json").read_text())
    report = dict(
        scope="All 700 numbered source folios and the completed original front/rear transfer.",
        source_basis="Completed local French reviews and the exact final global convention and numeric-heading correspondence packets.",
        source_wrapper_transport_complete=True,
        mapped_source_outer_groups=typo["mapped_source_outer_groups"],
        plain_exclusion_counts=typo["plain_exclusion_counts"],
        ordinary_paragraph_label_transports=typo["ordinary_paragraph_label_transports"],
        numeric_only_structural_heading_transports=typo["numeric_only_structural_heading_transports"],
        retained_or_generated_uline_groups=typo["retained_or_generated_uline_groups"],
        nested_uline_groups=typo["nested_uline_groups"],
        author_note_commands=typo["author_note_commands"],
        author_note_labels_identical=typo["author_note_labels_identical"],
        exact_source_transport="aggregate/TYPOGRAPHY_TRANSPORT.json",
        macro_dispositions="aggregate/MACRO_EXPANSION_CLOSURE.json",
        original_note_label_audit="aggregate/ORIGINAL_NOTE_LABEL_AUDIT.json",
        final_output_QA="visual_qa_final/VISUAL_QA.json",
        independent_late_QA="visual_qa_late/VISUAL_QA.json",
        rendered_scope="The listed final images were individually viewed. No claim is made that every output page received a visual inspection.",
        concrete_defects_observed=visual["concrete_defects_observed"],
        unresolved_static_macro_groups=macro["unresolved_page_command_groups"],
        original_literal_bases="The sealed contribution sources remain unchanged; the exact outside-math wrapper maps and the five explicit in-display typography transports are recorded separately.",
    )
    dump(old, report)


if __name__ == "__main__":
    visual = visual_record()
    macro = macro_closure()
    font_record(visual, macro)
    print(json.dumps(dict(viewed_images=visual["directly_viewed_images"],
                          unresolved_macro_groups=macro["unresolved_page_command_groups"],
                          source_wrapper_transport_complete=True)))
