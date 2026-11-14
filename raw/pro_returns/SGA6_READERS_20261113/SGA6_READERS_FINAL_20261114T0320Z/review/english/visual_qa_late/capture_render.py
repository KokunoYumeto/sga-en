#!/usr/bin/env python3
"""Locate source-folio markers and render requested final-output regions.

The final reader PDF is read only; this directory holds its exact observed
copy, locator evidence and page renders.  Rendering is not visual certification.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "review/english/final/SGA6_EN_corrected_apparatus.pdf"
TARGETS = [493, 519, 527, 538, 605, 692, 698]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", default=".",
                        help="Local revision subdirectory; previous captures remain unchanged.")
    args = parser.parse_args()
    destination = (HERE / args.revision).resolve()
    assert destination == HERE or HERE in destination.parents
    destination.mkdir(parents=True, exist_ok=True)
    observed = destination / "observed_corrected_apparatus.pdf"
    assert not observed.exists(), "Do not replace an inspected capture; use a separate revision directory."
    data = SOURCE.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    observed.write_bytes(data)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == digest, "PDF changed during capture."
    doc = fitz.open(observed)
    texts = [p.get_text() for p in doc]
    wanted = set(TARGETS) | {p + 1 for p in TARGETS}
    positions = {}
    for folio in sorted(wanted):
        marker = re.compile(r"\[print\s+" + str(folio) + r"\]")
        matches = [(i + 1, match.start(), match.end()) for i, text in enumerate(texts)
                   for match in marker.finditer(text)]
        assert len(matches) == 1, (folio, matches)
        pageno, start, end = matches[0]
        positions[folio] = dict(physical_pdf_page=pageno,
            source_marker=texts[pageno-1][start:end],
            text_context=texts[pageno-1][max(0, start-80):end+160])
    requested = []
    pages = set()
    for folio in TARGETS:
        start = positions[folio]["physical_pdf_page"]
        end = positions[folio+1]["physical_pdf_page"]
        chosen = list(range(start, end+1))
        if folio == 527:
            equation_pages = [i+1 for i, text in enumerate(texts)
                              if abs(i+1-start) <= 2 and "(1.3.9)" in text]
            assert equation_pages
            chosen = sorted(set(chosen) | set(equation_pages))
        pages.update(chosen)
        requested.append(dict(source_folio=folio, source_start=positions[folio],
            next_source_marker=positions[folio+1], rendered_physical_pages=chosen,
            visual_inspection_status="not yet inspected"))
    images = destination / "images"
    images.mkdir(exist_ok=True)
    rendered = []
    for pageno in sorted(pages):
        prefix = images / f"physical_{pageno:04d}"
        subprocess.run(["pdftoppm", "-f", str(pageno), "-l", str(pageno), "-r", "180",
                        "-singlefile", "-png", str(observed), str(prefix)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        image = prefix.with_suffix(".png")
        rendered.append(dict(physical_pdf_page=pageno, path=str(image.relative_to(ROOT)),
                             sha256=hashlib.sha256(image.read_bytes()).hexdigest(), dpi=180))
    record = dict(source_pdf=str(SOURCE.relative_to(ROOT)),
                  observed_pdf=str(observed.relative_to(ROOT)), sha256=digest, bytes=len(data),
                  physical_page_count=len(doc), requested_folios=requested, renders=rendered,
                  output_review_only=True, new_source_scan_reading_claim=False,
                  source_unchanged_after_render=hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest)
    (destination / "PDF_OBSERVATION.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    main()
