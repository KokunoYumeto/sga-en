#!/usr/bin/env python3
"""Save completed regional visual observations for the English221 boundary."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
status=json.loads((P/'EN_CANDIDATE_BUILD_STATUS.json').read_text())
assert len(status['corrected_apparatus']['compiled_printed_markers'])==221
resolution=('All four regenerated through221 forms completed two successful passes. Final corrected112/113 and diplomatic/reading111 directly viewed: both numerical1 and numerical2 calls and their complete original note texts share corrected112, and each pair shares output111 in the other two reader forms. Corrected112–123 and apparatus392–394 were directly inspected after reflow; no clipping or overlap observed.')
f=P/'EN_RENDERING_REPAIRS.jsonl';rows=[json.loads(x) for x in f.read_text().splitlines()]
for r in rows:
 if r['id']=='EN-LAYOUT-202-01':r['status']=resolution
f.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
a=json.loads((P/'EN_RENDERING_REPAIR_APPLICATIONS.json').read_text())
for r in a['repairs']:
 if r['id']=='EN-LAYOUT-202-01':r['status']=resolution
(P/'EN_RENDERING_REPAIR_APPLICATIONS.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
f=P/'EN_BUILD_REPAIRS.jsonl';rows=[json.loads(x) for x in f.read_text().splitlines()]
assert not any(x['id']=='EN-BUILD-016' for x in rows)
rows.append(dict(id='EN-BUILD-016',kind='verified author-note pagination repair',observed='In the first through221 corrected PDF, the numerical1 call in the202 principal-parts exact sequence appeared on output112 while its note text appeared on113.',change='Apply the local EN-LAYOUT-202-01 samepage context around the unchanged1.2.4 introduction, exact sequence and complete numerical1 note. Deleting the two wrapper lines recovers every original input byte.',mathematical_change=False,validation=resolution,corrected_pdf_sha256=status['corrected_apparatus']['pdf_sha256']))
f.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
f=P/'EN_PDF_VISUAL_QA.json';q=json.loads(f.read_text());q['revision']='latest built faithful English printed1–221;52 accepted translation records;151 source-linked variants';q['latest_corrected_PDF_sha256']=status['corrected_apparatus']['pdf_sha256']
checks=[
 dict(form='corrected_apparatus',output_pages=list(range(111,124)),finding='The first through221 outputs111–123 were directly viewed, including the complete AppendixII title/introduction, principal-parts and symbol sequences, original notes, rigidity proofs and retained author claim206, full finiteness proof, source Hilbert/Sobolev notation and all18 bibliography entries. The numerical1 call/text split on112/113 was the concrete observed pagination defect. Final111 is pixel-identical in its body crop; final112–123 were directly viewed after the repair. No clipping or overlap was observed. The inherited ExposéIII opening on123 is outside the completed translation scope.',record='EN_221_RENDER_COMPARISON.json'),
 dict(form='corrected_apparatus',output_pages=[112,113],finding='After the local samepage wrapper, original202 numerical1 call and complete symmetric-power note share output112. Numerical2 call and its complete second-module-structure note also share112. The unchanged continuation starts on113; the source principal-parts formulas, text and note labels remain legible.',repair='EN-LAYOUT-202-01'),
 dict(form='corrected_apparatus',output_pages=[392,393,394],finding='Both exact readings and source explanations are legible and remain together. The inspected apparatus includes the201 tensor/plus and base-ring variants, identification locator, omitted parenthesis, shared abbreviations,214 Sobolev exponent r/r−n,219 target I(S)/I(H), and the retained French Frisch title spelling. These final apparatus bodies are also pixel-identical to the earlier directly inspected393–395 bodies, excluding footer page numbers.',record='EN_221_RENDER_COMPARISON.json'),
 dict(form='diplomatic',output_pages=[111,118,121],finding='Directly viewed the original201 plus and O_X base reading, complete202 numerical1/2 notes, printed214 target exponent r, later219 I(S), and220 French title analyliques. All inspected formulas, original notes and bibliography lines fit without clipping or overlap.'),
 dict(form='reading',output_pages=[111,118,121],finding='Directly viewed the corrected201 tensor/base reading, complete202 numerical1/2 notes, corrected214 target exponent r−n,219 I(H), and220 title analytiques. No editorial apparatus marks appear. Folio margin labels remain outside the body and the original notes are complete.'),
 dict(form='reading',output_pages=[20,21,49,110],finding='The newly reported moved-margin page110 was directly inspected in the first through221 build; folio199/200 labels are outside the body and legible. Its final full-page pixels are identical. Output20/21/49 full-page pixels match the previously inspected frozen English179 pages at matrix1.6.',record='EN_221_READING_MARGIN_COMPARISON.json; EN_221_RENDER_COMPARISON.json'),
 dict(form='annotated_master',output_pages=list(range(111,124))+[392,393,394],finding='The complete RGB renderings of these final master pages are pixel-identical to the corresponding inspected corrected/apparatus pages at matrix1.5. This transports those regional layout observations only; no full-volume visual claim is made.',record='EN_221_RENDER_COMPARISON.json')]
for x in checks:x['revision']='English through printed221,151 variants'
q['checks'].extend(checks);q['pending_render_verification']=[]
q['resolved_rendering_issues'].append(dict(id='EN-LAYOUT-202-01',issue='Original202 numerical1 call/text separated across the initial corrected112/113 boundary.',resolution=resolution,resolved_pdf_sha256=status['corrected_apparatus']['pdf_sha256']))
f.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
f=P/'README_EN_WORK.md';s=f.read_text();a=s.index('## Status');b=s.index('## Native source inventory')
s=s[:a]+'''## Status

This directory contains unfinished volume-wide work. Exposé 0 (printed 1–77),
the complete Exposé I (78–159), and the complete Exposé II (160–221) have been
freshly AI-translated from the French pages checked by the reviewers and
coordinator. The comparison follows the French paragraphs, formulas, original
notes and copyist interpolations. The live records contain52 accepted translation
records and151 source-linked variants. All are included in the latest four forms.

Corrected and annotated PDFs have394 pages; diplomatic and reading PDFs have371.
Every form completed two successful passes with unchanged source hashes. All221
visible print-folio commands are present in the compiled sources, and every start
marker was found in the corrected PDF. After221 these PDFs retain inherited
English; no completed review of that remainder is claimed. The only final
diagnostics are reading-form moved-margin warnings on output20,21,49 and110.
The first three pages are pixel-identical to their previously inspected frozen
English179 pages. Output110 was directly inspected and its final pixels remain
identical: the margin labels lie outside the body and are legible.

The earlier twelve redundant Cart wrappers, apparatus macro-state drift and
missing folio commands are repaired. Local presentation wrappers keep the
folio186 numerical3 and folio202 numerical1 display calls with their complete
original notes. The latter repair was followed by all four two-pass full builds
and direct inspection of the affected pages. The restored AppendixII body,
original notes, source variants and bibliography were regionally inspected;
all mathematical units remain unchanged by the rendering repairs. Every reader
retains its visible in-progress notice. The requested volume-wide completion
gate is unmet.

'''+s[b:]
s=s.replace('The registered Appendix II\nopening restores','The complete Appendix II\nrestores')
s=s.replace('one unchanged English apposition, as confirmed by the French reviewer.','one unchanged English apposition, as confirmed by the French reviewer. The\nrigidity and finiteness proofs are fully restored, including all original notes,\nthe stated Sobolev exponents and source-indexed complexes. The source206 claim\nand the writer’s later uncertainty remain in both forms, with independent audit\nrecords kept separate. All18 bibliography entries and the following native macro\nblock are preserved; no contemporary terminology is substituted for the printed\n“operators with index.”')
s=s.replace('6,552 literal mathematical units across\nprinted 1–203','7,127 literal mathematical units across\nprinted1–221').replace('46 paired occurrences,\nstored as 45 current-applicable','51 paired occurrences,\nstored as50 current-applicable').replace('same comparison on160–203: thirteen lexical formula translations per branch','same comparison on160–221: eighteen lexical formula translations per branch')
s=s.replace('pages20/21/49. These have been visually checked','pages20/21/49/110. These have been visually checked').replace('all198 generated','all221 generated').replace('All198 markers','All221 markers').replace('GLOSSARY_SGA6_REVIEWED_001_203.tsv','GLOSSARY_SGA6_REVIEWED_001_221.tsv').replace('contains226 reference term pairs','contains242 reference term pairs')
f.write_text(s)
f=P/'EN_PARALLEL_TRANSFER_HANDOFF.md';s=f.read_text().replace('its four forms are being rebuilt after the local folio202 note-pagination fix.','all four forms have completed two successful passes after the local folio202\nnote-pagination fix, with regional visual verification recorded.');f.write_text(s)
print('Saved completed221 visual/layout metadata and working documentation.')
