#!/usr/bin/env python3
"""Seal the completed raw XIII transfer without overwriting any earlier seal."""
from pathlib import Path
import csv, hashlib, json, shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EN = ROOT / 'review/english'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


status = json.loads((HERE / 'probe666/BUILD_STATUS.json').read_text())
math = json.loads((HERE / 'literal_math_verification.json').read_text())
inventory = json.loads((HERE / 'INVENTORY_SCOPE.json').read_text())
assert math['unexpected_difference_units'] == 0
assert len(status['sequential_anchor_checks']) == 54
assert all(x['unique_anchor'] for x in status['sequential_anchor_checks'])
for form, record in status['forms'].items():
    assert len(record['runs']) == 2
    assert all(run['exit_code'] == 0 for run in record['runs'])
    assert all(line.startswith('Underfull') for line in record['runs'][-1]['diagnostics'])
    assert len(record['runs'][-1]['diagnostics']) == 3
    assert sha(HERE / 'probe666' / f'PROBE_EN_XIII_{form}.pdf') == record['pdf_sha256']
counts = dict(source_folios=51, raw_chunks=10, provisional_variant_groups=54,
              transfer_rows=354, lexical_complete_unit_pairs=5,
              math_units_per_branch=1954, unexpected_math_units=0,
              sequential_unique_anchors=54, selected_term_pairs=71,
              original_author_note_records=2, internal_source_folio_joins=50)
assert inventory['selected_terminology_rows'] == counts['selected_term_pairs']
assert {sum(r['French_math_units'] for r in math['counts'] if r['layer'] == layer)
        for layer in ['current', 'diplomatic']} == {1954}
qa = dict(
    scope='Targeted disjoint English XIII 616–666 rendering inspection over unchanged aggregate prefix 1–296',
    pdf_sha256s={k: v['pdf_sha256'] for k, v in status['forms'].items()},
    output_pages={'corrected_apparatus': 409, 'diplomatic': 366},
    forms_completed_two_passes=['corrected_apparatus', 'diplomatic'],
    final_errors=0, final_overfull_boxes=0, final_underfull_boxes_each_form=3,
    directly_viewed_corrected_output_pages=[342, 345, 346, 347, 348, 407, 408, 409],
    directly_viewed_diplomatic_output_pages=[343, 344, 345, 346],
    identical_final_pixels='final_pixel_identity.json verifies the already viewed corrected pages 342, 347 and 348 after the last local paragraph repair.',
    observations=[
        dict(pages=[342], result='The complete folio 654 diagram introduction stays with its diagram. Both diagrams, all arrows, labels and exact source stops are legible.'),
        dict(pages=[345], result='Folio 660 Hilbert polynomial stays inline, with a line break after its equality and local ragged-right composition. The prior 40.86086pt margin overflow and the subsequent stretched line are both resolved. Removing only the recorded presentation commands recovers the original paragraph exactly.'),
        dict(pages=[345, 346, 347, 348], result='The final Hodge-index argument, both proportionality corrections, complete source references and bibliography are legible. Original mathematical readings remain separately visible in the diplomatic form. The probe then returns to the unchanged native XIV; that native portion is not part of this contribution.'),
        dict(pages=[407, 408, 409], result='The final printed/current apparatus readings, source evidence and exact algebraic explanations are present and legible, including the corrected divisor sequence, ideal name, degree bound, missing parenthesis, proportionality wording and bibliography variants.'),
        dict(form='diplomatic', pages=[343, 344, 345, 346], result='The original divisor sequence, I. Hermann initial, omitted ideal name and bound, unmatched parenthesis, numerical-equivalence wording and duplicated bibliography are retained. The intentionally partial underline in integral is visible.')],
    prior_targeted_visual_records=['probe635/VISUAL_QA.json', 'probe655/VISUAL_QA.json'],
    limitations=[
        'These isolated probes do not extend the registered aggregate prefix or certify every PDF page. Earlier note and body views are recorded separately and are not relabelled as new final-page inspections.',
        'The three final underfull diagnostics concern source folios 630, 650 and 662; the corresponding formulas and text remain legible. There are no final overfull boxes or TeX errors.',
        'The raw transfer preserves its exact reviewed source basis. The newly completed global statement-word convention pass, including six nested plain terms, plain resp. tokens and numerical locators, must be applied as a separately recorded English rendering map before final readers.',
        'Full aggregate macro-state, paragraph-boundary and glossary checks remain separate assembly gates.'])
put(HERE / 'probe666/VISUAL_QA.json', qa)
repairs = [json.loads(line) for line in (HERE / 'rendering_repairs.jsonl').read_text().splitlines()]
for repair in repairs:
    repair['status'] = 'Validated in both final two-pass probes; targeted actual output inspection recorded in probe666/VISUAL_QA.json.'
    repair['validated_pdf_sha256s'] = qa['pdf_sha256s']
(HERE / 'rendering_repairs.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in repairs))
put(HERE / 'HANDOFF_XIII.json', dict(
    scope='Complete raw English Exposé XIII 616–666 transfer', counts=counts,
    first_native_target='sga6.e13.expose', next_native_target='sga6.e14.expose',
    source_reference='Exact stored French packets and per-batch reference hashes, before the separately recorded global convention pass; image observations remain attributed to their source reviewers.',
    macro_boundaries=['Pre-616 reviewed block is supplied by the sealed XII contribution.', 'The exact reviewed six-command block at 650 is retained locally.', 'The exact reviewed four-command XIV block follows the complete XIII bibliography; providecommand semantics are retained.'],
    author_notes='Exactly two original notes, on 616 and 631, with baseline parenthesized asterisk calls and labels. The approved post-freeze source amendments and their image receipt are retained.',
    retained_scope_issue='ASTRA-XIII-SCOPE-639-POSTFREEZE: source bodies retained; the exact disjoint-union restriction map and governing convention audit are copied under attributed_source_audits.',
    rendering_status='Both disjoint probes completed two passes with no errors or overfull boxes and three legible underfull diagnostics each. Targeted visual inspection is in probe666/VISUAL_QA.json.',
    paragraph_joins='All 50 internal source-folio joins checked: 23 paragraph breaks, one next-item boundary and 26 continuations; no helper-added blank line remains.',
    pending_assembly=['Exact global word-rule exclusion transport', 'Final four-form aggregate build and typography review', 'Cross-contribution joins and macro expansion', 'Cross-volume semantic terminology adjudication']))
(HERE / 'STATUS.md').write_text('''# English Exposé XIII, folios 616–666

All 51 source folios have a complete manual prose and formula-placement comparison with both exact reviewed French forms. The ten raw chunks, 54 provisional apparatus groups and 354 transfer rows are complete. Each literal branch contains 1,954 mathematical units, with zero unexpected differences and five explicitly translated complete lexical units. All 54 sequential apparatus anchors pass.

The corrected/apparatus and diplomatic disjoint probes each completed two passes (409 and 366 output pages), with no errors or overfull boxes and three underfull diagnostics. Actual final output pages viewed and their limitations are recorded in `probe666/VISUAL_QA.json`. These full-document probes include earlier assembled and later native material; they do not certify that surrounding native material.

All 50 internal folio joins are recorded. Both original author notes are complete, with their exact parenthesized star geometry. The 71 selected terminology pairs have literal source and translation anchors; the count does not assert exhaustive semantic glossary alignment. The folio 639 retained author-scope issue is explicitly attributed and leaves both source bodies unchanged.

The separate final global convention pass supplies exact plain-term, locator and resp. exclusions. It remains an aggregate rendering operation over the frozen raw transfer, followed by full reader compilation and review. No complete-volume English certification is made by this packet.
''')
(HERE / 'HANDOFF_XIII.md').write_text('''# Sealed raw English transfer: Exposé XIII 616–666

Consume the ten chunks using `translation_spans.jsonl` in order. Their native replacement spans are exact and adjacent, beginning at `sga6.e13.expose` and ending immediately before `sga6.e14.expose`. The preceding XII seal supplies the pre-616 reviewed macro block. Preserve the source-local blocks at 650 and after the final bibliography, as recorded in their exact boundary JSON files.

The 54 provisional variant groups retain their source IDs and proofs. Keep complete display branches atomic and outside TikZ macro arguments. Bound the final apparatus scope at the next exposé target. Five complete lexical units are paired explicitly; raw formula units are otherwise literal. Two original author notes and 71 selected local terminology renderings are inventoried with exact anchors. All 50 internal folio joins are audited without added paragraph breaks.

The folio 639 author-scope issue is retained in both bodies; the coordinator's actual image evidence and exact restriction-map counterexample are copied under `attributed_source_audits`. No replacement hypothesis is supplied. The final global typography convention amendments must be transported separately, preserving this raw math/reference basis and the exact plain nested terms, locators and resp. tokens.

Generation uses the stored packet basis:

```bash
python review/english/contributions/expose_xiii/contribution.py records
python review/english/contributions/expose_xiii/make_inventories.py
python review/english/contributions/expose_xiii/build_probe.py
```

`check_contribution.py` additionally compares against the live reviewed French loader; after new global conventions, use a separate report so the frozen reference proof remains intact. `EXTERNAL_INPUTS.json` identifies source/helper copies at sealing. The probe's base master is the unchanged English prefix 1–296 and is included among those inputs. The actual PDFs, sanitized diagnostics, targeted viewed images and measured layout repairs are retained. No older checkpoint is overwritten.
''')

deps = []
for relative in ['review/english/SGA6_EN_native_flattened_UNVERIFIED.tex',
                 'review/english/DRAFT_SGA6_EN_annotated_master.tex',
                 'review/english/reviewed_french.py', 'review/english/verify_reviewed_english.py',
                 'review/english/check_contribution.py', 'review/english/build_english_candidates.py',
                 'review/english/apparatus_macro_state.py', 'review/english/compile_candidates.py',
                 'review/english/source_emphasis.py', 'review/english/EN_BUILD_REPAIRS.jsonl',
                 'scripts/tex_environment.py',
                 'build/review_snapshots/english_xii_complete595_615/XII_boundary_macros.json']:
    deps.append(ROOT / relative)
for folder in ['xiii', 'expose_xiii_amendments', 'global_conventions']:
    for name in ['patches.jsonl', 'decisions.jsonl', 'own_findings.jsonl', 'FROZEN_HANDOFF.md',
                 'coverage_audit.json', 'author_scope_639.json', 'author_note_labels_receipt.json',
                 'post_review_patches.jsonl', 'plain_exclusions.json', 'typography_groups.json']:
        path = ROOT / 'review' / folder / name
        if path.exists():
            deps.append(path)
external = []
for path in deps:
    relative = path.relative_to(ROOT)
    dest = HERE / 'external_inputs' / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)
    external.append(dict(path=relative.as_posix(), sha256=sha(path), bytes=path.stat().st_size))
put(HERE / 'EXTERNAL_INPUTS.json', dict(
    status='Source/helper copies at sealing; the exact originally consumed page states remain separately hashed in source_packets and reference records. Global convention inputs are attached for the next rendering pass.',
    files=external))
snapshot = ROOT / 'build/review_snapshots/english_xiii_complete616_666'
assert not snapshot.exists(), 'Never overwrite a sealed snapshot'
shutil.copytree(HERE, snapshot, ignore=lambda directory, names: [n for n in names if n == '__pycache__' or n.endswith(('.aux', '.out'))])
files = [dict(path=p.relative_to(snapshot).as_posix(), sha256=sha(p), bytes=p.stat().st_size)
         for p in sorted(snapshot.rglob('*')) if p.is_file()]
put(snapshot / 'MANIFEST.json', dict(scope='Immutable raw English XIII 616–666 contribution',
    files=files, file_count=len(files), counts=counts, limitations=qa['limitations']))
manifest_sha = sha(snapshot / 'MANIFEST.json')
for path in snapshot.rglob('*'):
    path.chmod(0o555 if path.is_dir() else 0o444)
snapshot.chmod(0o555)
receipt = dict(snapshot=snapshot.relative_to(ROOT).as_posix(), manifest_sha256=manifest_sha,
               manifested_files=len(files), counts=counts, pdf_sha256s=qa['pdf_sha256s'])
put(EN / 'EN_XIII_HANDOFF.json', receipt)
print(json.dumps(receipt, ensure_ascii=False, indent=2))
