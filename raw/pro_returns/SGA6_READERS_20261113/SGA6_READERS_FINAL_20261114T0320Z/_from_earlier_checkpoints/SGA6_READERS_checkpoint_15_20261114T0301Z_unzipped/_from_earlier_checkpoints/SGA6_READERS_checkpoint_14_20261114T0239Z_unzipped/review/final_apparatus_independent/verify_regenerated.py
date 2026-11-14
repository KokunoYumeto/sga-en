#!/usr/bin/env python3
"""Verify the coordinator's rebuilt970 source links without changing readers."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(path):
    return json.loads(path.read_text())


def main():
    expected = load(HERE / "EXPECTED_REGENERATED_LINKS.json")
    variants_path = ROOT / "records/FR_VARIANTS.json"
    links_path = ROOT / "records/FR_APPARATUS_SOURCE_LINKS.json"
    variants = load(variants_path)
    links_report = load(links_path)
    links = links_report["variants"]
    errors = []
    if not len(expected) == len(variants) == len(links) == 970:
        errors.append("The ordered variant counts do not all equal970.")
    for e, v, link in zip(expected, variants, links):
        vid = e["variant_id"]
        if vid != v["id"] or vid != link["variant_id"]:
            errors.append([vid, "ordered variant ID mismatch"])
        for key in ["page", "printed", "corrected", "sha256_printed", "sha256_corrected"]:
            if e[key] != v[key]:
                errors.append([vid, key, "exact alternative changed"])
        for key in ["page", "sha256_printed", "sha256_corrected"]:
            if e[key] != link[key]:
                errors.append([vid, key, "report identity changed"])
        if e["effective_source_ids"] != v["source"] or e["effective_source_ids"] != link["source_ids"]:
            errors.append([vid, "source IDs", e["effective_source_ids"], v["source"], link["source_ids"]])
    result = dict(status="passed" if not errors else "failed", variants=970,
                  expected_file="review/final_apparatus_independent/EXPECTED_REGENERATED_LINKS.json",
                  observed_summary=links_report["summary"],
                  observed_files=[dict(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                                  for p in [variants_path, links_path]], errors=errors,
                  source_text_modified=False, source_decisions_modified=False)
    (HERE / "REGENERATED_VALIDATION.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
