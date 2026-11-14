#!/usr/bin/env python3
"""Seal final English artifacts and link the separately scoped completed audits."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re
import fitz

EN = Path(__file__).resolve().parent
ROOT = EN.parents[1]
OUT = EN / "final"
AGG = EN / "aggregate"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def save(p, v): p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n")
def item(p): return dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=sha(p))

COMMANDS = [
    "python review/english/collect_english_aggregate.py",
    "python review/english/verify_english_aggregate.py",
    "python review/english/build_english_aggregate.py --final",
    "python review/english/audit_english_aggregate.py",
    "python review/english/audit_english_macro_expansions.py",
    "python review/english/compile_candidates.py --directory review/english/final --prefix SGA6_EN_",
    "python review/english/finalize_english_records.py",
]

def main():
    cat = read(AGG/"INPUT_CATALOG.json")
    math = read(AGG/"LITERAL_MATH_VERIFICATION.json")
    span = read(AGG/"SOURCE_SPAN_COMPLETENESS.json")
    branch = read(AGG/"SINGLE_MASTER_BRANCH_AUDIT.json")
    joins = read(AGG/"FOLIO_JOIN_AUDIT.json")
    typo = read(AGG/"TYPOGRAPHY_TRANSPORT.json")
    macro = read(AGG/"MACRO_EXPANSION_CLOSURE.json")
    changes = read(OUT/"CHANGES_EN_RECONSTRUCTION.json")
    transfer = read(OUT/"TRANSFER_LEDGER_STATUS.json")
    builds = read(OUT/"EN_CANDIDATE_BUILD_STATUS.json")
    glossary = read(EN/"terminology_final/HANDOFF.json")
    gc = read(EN/"terminology_final/FINAL_VERIFICATION.json")
    qa = read(EN/"visual_qa_final/VISUAL_QA.json")
    lqa = read(EN/"visual_qa_late/VISUAL_QA.json")
    cp = ROOT/"review/final_english_classification/CLASSIFICATION.json"
    classification = read(cp)
    variants = [json.loads(s) for s in (OUT/"VARIANTS.jsonl").read_text().splitlines() if s.strip()]
    assert len(variants) == len({v["id"] for v in variants}) == 691
    assert all(v["printed"] != v["corrected"] for v in variants)
    assert cat["full_English_transfer_complete"] and not cat["unreviewed_numeric_folios"]
    assert span["numeric_folios"] == list(range(1,701)) and len(span["original_marker_keys"]) == 720
    assert span["each_original_marker_once"] and span["source_comment_and_visible_command_order_identical"]
    assert not span["hyperlink_audit"]["dangling_hyperlinks"]
    assert math["unexpected_difference_units"] == 0 and not math["remaining_folios"]
    assert all(r["exact_reconstruction_pass"] for r in branch["branches"])
    assert all(r["only_master_switch_differs"] for r in branch["forms"])
    assert joins["forward_and_reverse_reconstruction_pass"] and joins["nonwhitespace_tokens_identical"]
    assert typo["source_specific_wrapper_transport_complete"] and typo["nested_uline_groups"] == 0
    assert macro["unresolved_page_command_groups"] == 0
    assert changes["forward_exact_reconstruction"] and changes["reverse_exact_reconstruction"]
    assert gc["passed"] and qa["concrete_defects_observed"] == 0 and classification["summary"]["unresolved"] == 0
    books = []
    for form in ["annotated_master","diplomatic","corrected_apparatus","reading"]:
        tex=OUT/f"SGA6_EN_{form}.tex"; pdf=OUT/f"SGA6_EN_{form}.pdf"; b=builds[form]
        assert b["source_sha256"] == sha(tex) and b["pdf_sha256"] == sha(pdf)
        assert b["source_unchanged_during_compile"] and len(b["runs"]) == 2
        assert all(r["exit_code"] == 0 for r in b["runs"])
        uncommented=re.sub(r"(?m)(?<!\\)%.*$","",tex.read_text())
        external=re.findall(r"\\(?:input|include|includegraphics)\b",uncommented)
        assert not external,(form,external)
        diagnostics=b["runs"][-1]["diagnostics"]
        assert all(d.startswith("Underfull ") for d in diagnostics)
        books.append(dict(form=form,tex=item(tex),pdf=item(pdf),pages=len(fitz.open(pdf)),
            two_pass_exit_codes=[r["exit_code"] for r in b["runs"]],
            final_pass_underfull_paragraphs=len(diagnostics),final_pass_overfull_diagnostics=0,
            final_pass_other_diagnostics=0,diagnostic_log=item(OUT/f"SGA6_EN_{form}.log"),
            standalone_source_external_input_commands=external))
    assert changes["final_reader_sha256"] == sha(OUT/"SGA6_EN_corrected_apparatus.tex")
    assert sha(OUT/"SGA6_EN_annotated_master.tex") == sha(OUT/"SGA6_EN_corrected_apparatus.tex")
    assert sha(OUT/"SGA6_EN_corrected_apparatus.pdf") in json.dumps(lqa)
    for r in qa["observations"]: assert r["pdf_sha256"] == sha(ROOT/r["pdf"])
    for r in glossary["deliverables"]: assert sha(OUT/Path(r["path"]).name) == r["sha256"]
    front=read(ROOT/"build/review_snapshots/english_front_rear_complete20/literal_math_verification.json")
    units=[]
    for layer in ["current","diplomatic"]:
        rows=[r for r in math["counts"] if r["layer"]==layer]
        fr=[r for r in front["checks"] if r["layer"]==layer]
        n=sum(r["French_math_units"] for r in rows); m=sum(r["English_math_units"] for r in rows)
        f=sum(r["French_math_units"] for r in fr); e=sum(r["English_math_units"] for r in fr)
        assert n==m and f==e and all(r["unexpected_difference_units"]==0 for r in fr)
        units.append(dict(layer=layer,complete_units_within_numbered_folios=n,cross_folio_units=1,
                          front_rear_units=f,total_disjoint_scopes=n+1+f))
    counts=dict(variant_groups=691,all_group_readings_differ=True,classification_source=item(cp),
        classification=classification["summary"],
        visible_apparatus_entries_by_form=dict(annotated_master=691,corrected_apparatus=691,diplomatic=0,reading=0),
        definition="An English group can carry several linked source differences in one indivisible formula or diagram. It is not identified with a French minimal atom. Unchanged-English spelling dispositions, retained author assertions and identical both-layer typography transports create no English variant.")
    save(OUT/"APPARATUS_COUNTS_EN.json",counts)
    audit_names=[
        "aggregate/INPUT_CATALOG.json","aggregate/LITERAL_MATH_VERIFICATION.json","aggregate/FRENCH_SOURCE_STATES.json",
        "aggregate/SOURCE_SPAN_COMPLETENESS.json","aggregate/ORIGINAL_NOTE_LABEL_AUDIT.json",
        "aggregate/CROSS_FOLIO_MATH_AUDIT.json","aggregate/SINGLE_MASTER_BRANCH_AUDIT.json","aggregate/FOLIO_JOIN_AUDIT.json",
        "aggregate/TYPOGRAPHY_TRANSPORT.json","aggregate/TYPOGRAPHY_current.json","aggregate/TYPOGRAPHY_diplomatic.json",
        "aggregate/MACRO_EXPANSION_STATIC_AUDIT.json","aggregate/MACRO_EXPANSION_CLOSURE.json",
        "aggregate/APPARATUS_MACRO_STATES.json","aggregate/MACRO_TRANSPORT.json","aggregate/LAYOUT_TRANSPORT.json",
        "aggregate/HEADING_FOLIO_ANCHOR_TRANSPORT.json","aggregate/EXPOSE_START_LAYOUT_TRANSPORT.json",
        "aggregate/DIAGNOSTIC_TOLERANCE_TRANSPORT.json","EN_FONT_RENDERING_RECORD.json","EN_MACRO_EXPANSION_DECISIONS.json",
        "CREDITS_REQUIRED.md","visual_qa_final/VISUAL_QA.json","visual_qa_final/VISUAL_QA.md",
        "visual_qa_late/VISUAL_QA.json","visual_qa_late/VISUAL_QA.md","terminology_final/HANDOFF.json",
        "terminology_final/GLOSSARY_AUDIT.json","terminology_final/FINAL_VERIFICATION.json","terminology_final/MANIFEST.json",
        "terminology_final/GLOSSARY_ATTESTATIONS.json","terminology_final/MULTIPLE_RENDERING_DECISIONS.json",
        "terminology_final/PRINTED_INDEX_PAIRS.json","final/CHANGES_EN.tsv","final/CHANGES_EN_RAW_HUNKS.json",
        "final/CHANGES_EN_LINE_ENDING_PROJECTION.json","final/CHANGES_EN_RECONSTRUCTION.json",
        "final/TRANSFER_LEDGER.jsonl","final/TRANSFER_LEDGER_STATUS.json","final/VARIANTS.jsonl",
        "final/EN_CANDIDATE_BUILD_STATUS.json","final/COMPILE_METADATA_AMENDMENT.json","final/APPARATUS_COUNTS_EN.json"]
    script_names=["collect_english_aggregate.py","verify_english_aggregate.py","build_english_aggregate.py",
        "audit_english_aggregate.py","audit_english_macro_expansions.py","compile_candidates.py",
        "finalize_english_records.py","english_folio_joins.py","english_typography.py","source_emphasis.py",
        "apparatus_macro_state.py","reviewed_french.py","finish_english_qa_records.py","finalize_english_release.py"]
    status=dict(status="complete; stable for coordinator archival",generated_at_utc=datetime.now(timezone.utc).isoformat(),
        final_books=books,completed_scope=dict(numbered_source_folios=700,original_front_rear_leaves=20,
            original_leaf_markers=720,exact_reviewed_translation_spans=142,remaining_numeric_folios=[],
            original_marker_order_preserved=True,certified_blank_labels_suppressed=["IV","VI","X","690","rear-715","rear-716"],
            expose_XI="The original notice that XI was not written up is retained; no XI body has been supplied."),
        source_collation_attribution="Original-image coverage is the coordinator's source review in records/PAGES_CHECKED.tsv. The English assembler attributes that evidence without inventing a new scan inspection.",
        English_transfer=dict(complete_declared_source_scope=True,exact_spans=142,ledger_rows=transfer["rows"],
            basis="Full manually compared passage contributions, exact native-span replacements, both source-variant branches, source hashes and final aggregate checks."),
        mathematical_unit_counts=units,unexpected_mathematical_units=0,
        complete_lexical_pair_records=math["complete_lexical_pair_records"],
        approved_lexical_difference_side_units=math["approved_lexical_difference_side_units"],
        original_author_note_commands_per_branch=111,
        author_note_count_definition="Every Footnote, FootMark and FootText command in its exact folio/label sequence; repeated calls and split call/text pairs are not silently counted as distinct notes.",
        apparatus=counts,
        paragraph_boundaries=dict(numeric_adjacent_joins=699,repaired_separator_boundaries=192,
            exact_forward_reverse_reconstruction=True,nonwhitespace_tokens_unchanged=True,
            front_rear_internal_joins=18,front_rear_evidence="build/review_snapshots/english_front_rear_complete20/folio_joins.json"),
        typography=dict(source_wrapper_transport_complete=True,outer_groups=387,ordinary_numeric_labels=77,
            numeric_only_structural_headings=49,nested_uline_groups=0,
            explicit_plain_exclusions=typo["plain_exclusion_counts"],source567_ruled_resp_tokens=2,
            original_note_labels_unchanged=True,scope="Exact source-specific word-rule and label correspondences; no inferred universal font convention."),
        macros=dict(equal_static_page_command_groups=macro["equal_page_command_groups"],
            approved_lexical_page_command_groups=11,unresolved_static_page_command_groups=0,
            closure="review/english/aggregate/MACRO_EXPANSION_CLOSURE.json",
            actual_TeX_capture="review/english/aggregate/APPARATUS_MACRO_STATES.json",limitation=macro["limitation"]),
        final_rendering=dict(own_individually_viewed_images=qa["directly_viewed_images"],
            independent_late_individually_viewed_images=8,all_output_pages_visually_inspected=False,
            concrete_defects_in_recorded_views=0,remaining_underfull_counts=dict(annotated_master=5,corrected_apparatus=5,diplomatic=4,reading=4),
            final_overfull_diagnostics=0,final_other_diagnostics=0,
            layout="Seven exact-inverse local row/title repairs, four observed heading-marker anchors, fourteen generated exposé page starts. Original comments and author tokens remain fixed.",
            diagnostic_tolerance="The inherited 20pt horizontal tolerance was replaced by 0.1pt at all three occurrences; remaining warnings were not suppressed."),
        exhaustive_changes=changes,
        glossary=dict(status="closed declared-inventory and complete printed-index audit",exact_counts=glossary["exact_counts"],
            declared_TSV_rows_disposed=gc["TSV_input_rows_with_explicit_dispositions"],
            manual_rows_disposed=gc["manual_lexicon_rows_with_dispositions"],original_leaf_pairs_checked=720,
            pending_known_terminology_slips=0,deliverables=[item(OUT/Path(r["path"]).name) for r in glossary["deliverables"]],
            count_and_completeness_limits=gc["limitations"]),
        retained_source_limitations="Examined assertions without a uniquely supported textual emendation retain author wording in both forms. Counterexamples and exact computations remain in the source dossier. The final preface explicitly names retained 431,443,590–592 assertions,464 locators and465 memberships. Unchanged passages create no variant.",
        credits="Original and inherited named human credits, AI attribution and rights statements remain in each form. Masked publisher-notice restitution is attributed to the matching1971 LNM228 template; hidden physical scan strokes were not recovered.",
        authoritative_audits=[item(EN/p) for p in audit_names],
        reproducibility=dict(working_directory="Common extracted project directory containing en,fr,scripts,build,review.",
            prerequisites=[item(EN/"SGA6_EN_native_flattened_UNVERIFIED.tex"),item(EN/"EN_TRANSLATION_PATCHES.jsonl"),
                item(ROOT/"en/release_v2026-11-12/07_SGA6_EN_CURRENT_LAYERED_READER.tex"),
                item(ROOT/"build/FR_current_revised.tex"),item(ROOT/"build/FR_diplomatic_revised.tex")],
            exact_sealed_packets=cat["packets"],
            packaging="All ten unchanged packet closures and original manifest members remain at the exact catalog paths. No delivery projection or relaxed manifest check is used.",
            commands_in_order=COMMANDS,scripts=[item(EN/p) for p in script_names],
            environment="scripts/tex_environment.py locates the isolated standard TeXLive environment, which is a runtime prerequisite.",
            source_state="The reviewed French loader consumes initial page packets and ordered final decision/amendment streams. Do not replay historical incremental add_*.py scripts.",
            rendered_QA="Views are bound to PDF/image hashes. A rebuilt PDF with a different hash requires renewed output inspection. finish_english_qa_records.py serializes completed observations; it is not an automatic visual verifier.",
            byte_reproducibility="Exact TeX artifacts and reversible source transports are hashed. PDF files also carry generated metadata; ordinary rebuilds do not promise identical timestamps."),
        ownership="Original en/fr inputs, prior checkpoints and sealed packets remain unchanged. The completed English directory is stable for final packaging.")
    save(OUT/"RELEASE_STATUS.json",status)
    handoff="# Final English release handoff\n\nThe complete English edition is ready for archival. Exact artifact hashes, source hashes, audit links and the bounded gate definitions are in RELEASE_STATUS.json.\n\n## Books and diagnostics\n\n| Form | Pages | Compiler exits | Remaining underfull paragraphs | Other final diagnostics |\n|---|---:|---|---:|---:|\n"
    for b in books: handoff+=f"| {b['form']} | {b['pages']} | 0 / 0 | {b['final_pass_underfull_paragraphs']} | 0 |\n"
    handoff+="""

All four standalone TeX files contain no external input/include/graphics commands. Standard TeX packages remain runtime dependencies. The annotated-master and corrected-apparatus TeX files have identical bytes; the diplomatic and reading forms differ only by the one master form switch. Original Introduction, authors' and editors' notes, additions, indexes and original front/rear matter remain in every form.

The full two-pass compiler receipts are in final/EN_CANDIDATE_BUILD_STATUS.json; the four diagnostic logs are sanitized. Final passes have zero errors, zero overfull boxes and no other compiler warnings. The five distinct underfull paragraphs were individually viewed and remain legible without clipping or overlap. First-pass rerun warnings are preserved in the receipt and disappear in the second pass.

## Complete source transfer

The edition contains all700 numbered folios and all20 original front/rear leaves, with720 unique source comments and generated-marker calls in original order. Six certified blank labels are suppressed while their comments/calls remain. The original notice that ExposéXI was not written up is retained; no XI body is supplied.

The142 exact translated spans are backed by manually compared passage records and sealed contributions. The aggregate ledger contains6060 attributed rows. Every original author-note command has the same folio and label key as the reviewed French in both branches:111 commands per branch. That count includes repeated calls and split call/text helpers.

There are zero unexpected mathematical units in either branch. Exact disjoint counts follow:

| Branch | Within numbered folios | Cross-folio equation | Original front/rear | Total of these scopes |
|---|---:|---:|---:|---:|
"""
    for u in units: handoff+=f"| {u['layer']} | {u['complete_units_within_numbered_folios']} | 1 | {u['front_rear_units']} | {u['total_disjoint_scopes']} |\n"
    handoff+="""

The cross-folio unit is equation1.3.9 across526/527; its nonprinting-comment projection has an exact inverse. The156 complete lexical pairs and532 approved difference-side units record translated words or the explicit wrapper transports inside formulas. They are not counts of independent mathematical corrections.

All699 numbered-folio joins are recorded. The192 repaired separator boundaries plus the special visible527 marker preserve every nonwhitespace token and pass forward/reverse reconstruction. The sealed front/rear packet separately records18 internal joins.

The typography pass maps387 outer source groups,77 ordinary numeric labels and49 numeric-only structural headings. It preserves the six plain nested terms, eight plain resp. tokens,21 corrected/20 diplomatic plain locator occurrences, and the two explicitly ruled resp. tokens at567. No nested underline wrapper remains.

The static macro audit records1306 equal page/command groups and11 approved lexical groups:20 red invocations, two longg invocations and four naif invocations. MACRO_EXPANSION_CLOSURE.json supplies the precise object-preserving or lexical disposition of every unequal group. The restored Gl and double-struck coefficient expansions now compare equal to the source. Actual local TeX state capture for all691 variants is a separate recorded mechanism. The static parser is not presented as a complete TeX interpreter.

## Apparatus and exhaustive change log

The691 genuine printed/current variant groups are classified as510 source-misprint corrections,45 mathematical-source corrections,128 explicit notation conventions and8 adjudicated source corrections. APPARATUS_COUNTS_EN.json links the independently resolved primary and related source IDs and per-exposé matrix. Complete diagrams or indivisible formulas may carry several source differences within one group. Unchanged-English French spelling repairs and unchanged author assertions have ledger dispositions and create no variant entry.

CHANGES_EN.tsv includes every literal difference between the exact released07_SGA6_EN_CURRENT_LAYERED_READER.tex and the final corrected-apparatus TeX, including generated preface, credits, preamble, typography, source markers and apparatus. Its8443 raw hunks contain4222 line-ending-only hunks and4221 literal-source-change hunks. Actual CRLF/LF bytes are retained; the alignment-only newline projection has its own exact inverse. Full forward and reverse file reconstruction pass. The additional142 native-to-English span rows and3 English-only correction rows have distinct scope labels.

## Closed glossary

The glossary has1346 rows for1296 French headword keys,46 admitted multiple-rendering groups and111 cross-volume decisions. All234 printed index rows are paired:129 terminology and105 notation rows, including both repeated-label cases. All5134 declared TSV input rows and26 manual entries have dispositions. The648/649 generization repairs are applied; no known terminology slip remains pending in this inventory.

Each glossary row declares whether its count concerns a co-attesting leaf, a paired index entry or a literal command/token use. Those measures are not added as word totals or represented as one-to-one semantic translation frequencies. Completeness applies to the declared inventories and printed indexes; arbitrary phrase extraction is not claimed to enumerate every possible technical expression.

## Rendered evidence and retained source limits

The English assembler individually viewed28 final images:23 corrected-apparatus images and5 reading-form images. They include original and editorial front matter, original note labels, formula/title repairs, every distinct underfull paragraph, the Introduction and four exposé starts, and three apparatus pages testing local macro states. The independent late reviewer viewed8 further images at7 source loci. Exact PDF/image hashes and observations are in visual_qa_final/VISUAL_QA.json and visual_qa_late/VISUAL_QA.json. No clipping or overlap was observed in these bounded checks; every output page is not claimed visually inspected.

Original-image collation is attributed to the coordinator's records/PAGES_CHECKED.tsv. Author assertions without a uniquely supported textual emendation remain in both forms, with exact counterexamples or computations in the source dossier. The final preface identifies this handling. Human credits and AI attribution are retained. Masked publisher-notice restitution is explicitly attributed to the matching1971 LNM228 template, without claiming recovery of hidden physical strokes.

## Authoritative files

All paths below are under review/english unless otherwise stated.

| Evidence | Path |
|---|---|
| Final hashes and gate definitions | final/RELEASE_STATUS.json |
| Complete compiler receipts | final/EN_CANDIDATE_BUILD_STATUS.json |
| Every final-reader difference | final/CHANGES_EN.tsv; final/CHANGES_EN_RECONSTRUCTION.json |
| Source-linked variants and transfer | final/VARIANTS.jsonl; final/TRANSFER_LEDGER.jsonl |
| Source-span, marker and hyperlink completeness | aggregate/SOURCE_SPAN_COMPLETENESS.json |
| Literal math and crossing equation | aggregate/LITERAL_MATH_VERIFICATION.json; aggregate/CROSS_FOLIO_MATH_AUDIT.json |
| Exact single-master branches | aggregate/SINGLE_MASTER_BRANCH_AUDIT.json |
| Original note geometry | aggregate/ORIGINAL_NOTE_LABEL_AUDIT.json |
| Paragraph boundaries | aggregate/FOLIO_JOIN_AUDIT.json |
| Source-specific typography | aggregate/TYPOGRAPHY_TRANSPORT.json; EN_FONT_RENDERING_RECORD.json |
| Macro dispositions and captures | aggregate/MACRO_EXPANSION_CLOSURE.json; aggregate/APPARATUS_MACRO_STATES.json |
| Actual output observations | visual_qa_final/VISUAL_QA.json; visual_qa_late/VISUAL_QA.json |
| Glossary deliverables | final/GLOSSARY_SGA6_FR_EN.tsv; final/CROSS_VOLUME_TERMS.tsv; final/GLOSSARY_INCONSISTENCIES.md |
| Glossary evidence and seal | terminology_final/HANDOFF.json; terminology_final/FINAL_VERIFICATION.json; terminology_final/MANIFEST.json |

## Exact reproduction order

Extract all records and all ten unchanged packet closures into the common project directory, preserving their exact catalog paths and original manifest members. The native flattened source, accepted prefix span records, released baseline, reviewed French page packets and ordered amendment streams are required. All packet manifests are named in aggregate/INPUT_CATALOG.json and RELEASE_STATUS.json. There is no delivery projection or relaxed manifest check.

Run from the common directory containing en/,fr/,scripts/,build/,review/:

"""
    handoff+="\n".join("    "+command for command in COMMANDS)+"\n"
    handoff+="""

The supplied scripts/tex_environment.py wrapper requires its standard TeXLive environment. Do not replay historical incremental add_*.py files. finish_english_qa_records.py serializes observations already made against the listed images; it does not automatically inspect them. A different PDF hash requires renewed output inspection before a new visual receipt. Ordinary PDF builds carry generated metadata, so exact TeX reconstruction and exact archived-PDF hashes are separate recorded facts.

Original source files, old checkpoints and sealed contribution inputs remain unchanged. This English handoff is stable for final coordinator packaging.
"""
    # Correct incidental fused numerals in generated prose without touching any author text.
    handoff=re.sub(r"([A-Za-z])([0-9])",r"\1 \2",handoff)
    handoff=re.sub(r"([0-9])([A-Za-z])",r"\1 \2",handoff)
    # File names and command lines must remain exact; restore those from the known payloads.
    for old,new in [
        ("SGA 6","SGA6"),("07_SGA 6","07_SGA6"),("LNM 228","LNM228"),
        ("ExposéXI","Exposé XI"),
        ("add_*.py","add_*.py"),
    ]: handoff=handoff.replace(old,new)
    for name in ["HANDOFF.md","README_EN.md"]:(OUT/name).write_text(handoff)
    names={p.name for p in OUT.glob("SGA6_EN_*.tex")}|{p.name for p in OUT.glob("SGA6_EN_*.pdf")}|{p.name for p in OUT.glob("SGA6_EN_*.log")}|{
        "CHANGES_EN.tsv","CHANGES_EN_RAW_HUNKS.json","CHANGES_EN_LINE_ENDING_PROJECTION.json","CHANGES_EN_RECONSTRUCTION.json",
        "TRANSFER_LEDGER.jsonl","TRANSFER_LEDGER_STATUS.json","VARIANTS.jsonl","EN_CANDIDATE_BUILD_STATUS.json",
        "COMPILE_METADATA_AMENDMENT.json","APPARATUS_COUNTS_EN.json","GENERATION_STATUS.json","GLOSSARY_SGA6_FR_EN.tsv",
        "CROSS_VOLUME_TERMS.tsv","GLOSSARY_INCONSISTENCIES.md","RELEASE_STATUS.json","HANDOFF.md","README_EN.md"}
    manifest=dict(scope="Final English deliverables and accompanying records; the release status links the remaining audit and source hashes.",
                  files=[item(OUT/n) for n in sorted(names)])
    save(OUT/"MANIFEST.json",manifest)
    save(OUT/"SEAL_RECEIPT.json",dict(status=status["status"],manifest=item(OUT/"MANIFEST.json"),
        release_status=item(OUT/"RELEASE_STATUS.json"),handoff=item(OUT/"HANDOFF.md"),
        file_records=len(manifest["files"]),author_sources_or_PDFs_changed=False))
    print(json.dumps(dict(status=status["status"],release_status_sha256=sha(OUT/"RELEASE_STATUS.json"),
        manifest_sha256=sha(OUT/"MANIFEST.json"),files=len(manifest["files"]),math_counts=units,
        books=[dict(form=b["form"],pages=b["pages"]) for b in books])))

if __name__=="__main__":main()
