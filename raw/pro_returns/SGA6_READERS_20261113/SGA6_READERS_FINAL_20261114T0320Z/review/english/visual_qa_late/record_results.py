#!/usr/bin/env python3
"""Save the bounded human visual review of the recorded, hash-fixed capture.

The observations below were entered only after all eight images were displayed
individually and inspected. This script does not infer visual success from PDF
extraction, compilation, or image existence.
"""
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CAPTURE = HERE / "title_starts/PDF_OBSERVATION.json"
EXPECTED_HASH = "944527b1ec384a05e0d880043848c5f23e1bba957813d2cbd016c2e94c482f9a"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    capture = json.loads(CAPTURE.read_text())
    assert capture["sha256"] == EXPECTED_HASH
    assert sha(ROOT / capture["observed_pdf"]) == EXPECTED_HASH
    assert sha(ROOT / capture["source_pdf"]) == EXPECTED_HASH, "Final PDF changed after capture."
    assert capture["physical_page_count"] == 561
    observations = [
        {
            "source_folio": 493,
            "physical_pdf_pages": [274],
            "regions": ["Proposition 5.2 and its two displays", "triangle P, Z, Y", "exact sequence (5.2.1)", "symmetric-algebra triangle and source-494 continuation"],
            "observed": [
                "The proposition's word-group underlines leave its mathematical units separate and readable; the underlined sheaf letters and indices in the exact sequence are distinct.",
                "Both triangular diagrams fit inside the text margins. The P/Z/Y arrow directions and h/f/g labels are clear, without contact with their vertices.",
                "The symmetric-algebra triangle has the corrected lower vertex O_Y with its O rule visible. Both upward diagonals reach separate upper vertices; the top horizontal arrow and the direct-sum expression are unobstructed.",
                "The (5.2.1) tag, superscript apparatus numbers, source-folio marker and continuation text are legible. No clipping or overlap was observed."
            ]
        },
        {
            "source_folio": 519,
            "physical_pdf_pages": [288],
            "regions": ["Exposé X title, two title lines and byline", "section 1 and numeric paragraph 1.1", "opening displays and statements"],
            "observed": [
                "The Exposé X title begins on a fresh output page. The underlined exposé label, two double-ruled title lines, O. Jussila byline, appendix attribution and opening section remain together.",
                "The two title lines fit within the page width; their rules are separate from the letters and from each other. The byline and parenthetic appendix attribution do not overlap.",
                "The numeric label 1.1 is visibly normal weight. Upper and lower K dots and the independent sheaf-letter rules remain legible in the opening text and formulas.",
                "The source-520 marker and the right-side equation tags fit without clipping. No defect was observed in the requested title or opening region."
            ]
        },
        {
            "source_folio": 527,
            "physical_pdf_pages": [292],
            "regions": ["equation (1.3.9) and immediately following source-527 marker", "continuation beginning 'where w'"],
            "observed": [
                "Equation (1.3.9) renders as one complete display with its right-side tag. Its final comma and formula are clear.",
                "The source-527 marker is in the following prose line before 'where w', outside the equation. There is no stray paragraph gap, missing-item artifact, interrupted formula, or visible fragment of an environment command.",
                "The continuation and following induction conclusion are readable within the text margins. No local layout defect was observed."
            ]
        },
        {
            "source_folio": 538,
            "physical_pdf_pages": [297],
            "regions": ["Proposition 2.4.4 proof diagram", "Z to Q hook and converging isomorphism arrows"],
            "observed": [
                "The horizontal arrow from Z to Q has a visible hook at its source and a rightward arrowhead at its target.",
                "The two arrows from K(Spec(k)) and K(Spec(K)) converge on Z with separate isomorphism labels. Their arrowheads, labels and the Z node do not collide.",
                "The left vertical arrow, both Pic labels, and the two s_y labels are legible; the lower s_y rule is visible and separate from the arrow.",
                "The entire diagram, surrounding proposition/proof text and adjacent section heading fit within the margins. No clipping or overlap was observed."
            ]
        },
        {
            "source_folio": 605,
            "physical_pdf_pages": [333],
            "regions": ["R^2 formula at source-605 marker", "two exact-row diagrams", "display label 3.2 and Im delta equality"],
            "observed": [
                "The R^2 formula and following statement text are readable. The separately ruled Hom and Pic notation is not merged into adjacent prose rules.",
                "Both exact-row diagrams fit within the text block. The vertical hooks and equality lines in the first diagram are visible, with clear row separation.",
                "In the second diagram the delta labels, equality line, R^1 terms and final R^2 term remain readable. The apparatus number 585 lies separately to the left without covering a map or object.",
                "The normal-weight label 3.2 appears on the same display line as Im(delta_T^*) = Im(delta_T), with sufficient space between label and equality. The source-606 marker begins the following prose. No clipping or overlap was observed."
            ]
        },
        {
            "source_folio": 692,
            "physical_pdf_pages": [378, 379],
            "regions": ["terminological index from source-692 marker to source-693 marker", "three-column alignment and page continuation"],
            "observed": [
                "The source-692 marker is attached to the Chern-character row and is readable without covering its text or the reference columns.",
                "The entry, exposé and section columns remain visibly separate, including the longest entries. The row spacing and left/right margins are clear on both physical pages.",
                "All four S-category entries visibly retain the S rule. The upper/lower graded-group dots in the numerical-equivalence row and the tau-equivalence rows on the continuation page are distinguishable.",
                "The page break follows a complete index row and resumes with numerical equivalence. No truncated row, overlap or margin clipping was observed within the requested source interval."
            ]
        },
        {
            "source_folio": 698,
            "physical_pdf_pages": [382],
            "regions": ["mathematical index from source-698 to source-699 marker", "Gr/K dots, hatted G, Hom/M rules and L notation"],
            "observed": [
                "The source-698 marker and three index columns are readable, with clear separation between mathematical entries and their references.",
                "The upper K/Gr bullets and lower dots remain visibly distinct. Their alg/num, naive, argument and coefficient indices fit without collision.",
                "The two hatted G symbols and their t/u superscripts are legible. The Hom rule and the separate subscript-M rule are both visible. The L rule and its X/Y superscript remain clear.",
                "The source-699 marker follows the Mod(U) row without covering either row. No clipped mathematical entry, crowded reference column or margin overflow was observed."
            ]
        }
    ]
    renders = {r["physical_pdf_page"]: r for r in capture["renders"]}
    inspected_pages = sorted({p for row in observations for p in row["physical_pdf_pages"]})
    assert inspected_pages == [274, 288, 292, 297, 333, 378, 379, 382]
    inspected_images = []
    for pageno in inspected_pages:
        image = renders[pageno]
        assert sha(ROOT / image["path"]) == image["sha256"]
        inspected_images.append({**image, "actually_displayed_and_visually_inspected": True,
                                 "display_method": "one full-page image per view_image tool call"})
    for row in observations:
        row["image_paths"] = [renders[p]["path"] for p in row["physical_pdf_pages"]]
        row["status"] = "pass: no defect observed at requested output locus"
        row["defects"] = []
    report = {
        "audit_id": "ASTRA-EN-FINAL-VISUAL-LATE-7-LOCI",
        "completed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "complete",
        "scope": "Bounded visual output QA of seven requested source-folio loci in the corrected English reader with apparatus.",
        "source_pdf": capture["source_pdf"],
        "observed_pdf": capture["observed_pdf"],
        "pdf_sha256": EXPECTED_HASH,
        "pdf_bytes": capture["bytes"],
        "physical_pdf_pages": 561,
        "capture_record": str(CAPTURE.relative_to(ROOT)),
        "requested_folio_count": 7,
        "individually_viewed_full_page_image_count": 8,
        "defect_count": 0,
        "observations": observations,
        "inspected_images": inspected_images,
        "source_hash_unchanged_at_report": True,
        "source_or_final_reader_mutated": False,
        "new_source_scan_reading_claim": False,
        "limitations": [
            "Only the seven requested output loci were visually certified; this is not a whole-volume visual review.",
            "This audit checks the rendered English output. It makes no fresh claim of source-scan collation or new mathematical adjudication.",
            "The two earlier captures were superseded before any successful image viewing and carry no visual certification."
        ],
        "superseded_capture_record": "review/english/visual_qa_late/SUPERSEDED_CAPTURES.json"
    }
    (HERE / "VISUAL_QA.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Final English output: seven-locus visual review", "",
        "**Completed: no concrete defect was observed at any of the seven requested loci.** Eight full-page PNGs were displayed and inspected individually. This is bounded output QA; it does not claim a new source-scan reading or a whole-volume visual review.", "",
        f"- PDF: `{capture['source_pdf']}`",
        f"- SHA-256: `{EXPECTED_HASH}`",
        "- Physical pages in the captured PDF: **561**",
        f"- Immutable observed copy: `{capture['observed_pdf']}`",
        f"- Capture and render metadata: `{CAPTURE.relative_to(ROOT)}`",
        "- The live final PDF still had this exact hash when the report was written.",
        "- No final PDF, reader source, sealed contribution or source decision was edited.", "",
        "| Source folio | Physical PDF page(s) | Result |",
        "|---|---|---|",
    ]
    for row in observations:
        lines.append(f"| {row['source_folio']} | {', '.join(map(str,row['physical_pdf_pages']))} | No defect observed |")
    for row in observations:
        lines += ["", f"## Source {row['source_folio']}", ""]
        lines += ["- " + observation for observation in row["observed"]]
        lines += ["", "Actually inspected images:", ""]
        lines += [f"- `{path}`" for path in row["image_paths"]]
    lines += ["", "## Evidence boundaries", "",
        "The inspected images were rendered at 180 dpi from the exact captured PDF. The JSON report records every image hash and physical page. Source-folio markers were located by their literal `[print N]` form; physical footer numbers were not used as source locators.", "",
        "The earlier pre-strict-layout PDF and the pre-title-transport PDF remain in this audit directory with their original metadata. Neither received a successful image display before supersession, and neither is certified. `SUPERSEDED_CAPTURES.json` records that history.", "",
        "The absence of a defect here applies to the displayed regions and the concrete checks described above. It does not replace the volume's separate source collation, mathematical decisions, provenance audit or full build diagnostics.", ""]
    (HERE / "VISUAL_QA.md").write_text("\n".join(lines))
    manifest_files = [HERE / "VISUAL_QA.json", HERE / "VISUAL_QA.md", HERE / "record_results.py",
                      HERE / "capture_render.py", CAPTURE, ROOT / capture["observed_pdf"],
                      HERE / "SUPERSEDED_CAPTURES.json"]
    manifest_files += [ROOT / image["path"] for image in inspected_images]
    manifest = {"files": [{"path": str(path.relative_to(ROOT)), "sha256": sha(path),
                           "bytes": path.stat().st_size} for path in sorted(manifest_files)],
                "pdf_sha256": EXPECTED_HASH, "inspected_images": 8, "source_loci": 7,
                "status": "complete; no observed defect"}
    (HERE / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "pdf_sha256": EXPECTED_HASH,
                      "defects": 0, "loci": 7, "inspected_images": 8,
                      "report_sha256": sha(HERE / "VISUAL_QA.json"),
                      "manifest_sha256": sha(HERE / "MANIFEST.json")}, indent=2))


if __name__ == "__main__":
    main()
