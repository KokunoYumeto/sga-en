#!/usr/bin/env python3
"""Register exact direct-image, base-change and limit passages in Exposé IV."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_IV_P289_293.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('Now suppose that we are in the situation');b=native.index(r'\sgaStableTarget{sga6.e04.para.3-3}',a)
record=dict(id='EN-EXPOSE-IV-289-293',page='289–293',place='Perfect direct images, full base-change proof and the three limit constructions',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by reviewer',source='build/page_packets/289–293/current.tex and diplomatic.tex; review/expose_iv/patches.jsonl',reason='Restores all direct-image alternatives, exact unit/counit comparison maps, both Cartesian squares and the cocartesian ring square, the complete original section note, every boundedness condition, actual f_ij-flat hypothesis and all three precise limit constructions. Six existing source differences and the newly scan-adjudicated III5.9(b) to III5.8(b) locator repair are explicit.')
decisions=[json.loads(x) for x in (R/'review/expose_iv/decisions.jsonl').read_text().splitlines()];variants=[]
def add(no,page,old,printed,mode,source,end=None,start=None):
 d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=d['reason'],scope_start=start or f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=end or f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',scan_image=d['image'],scan_region=d['region']))
add(193,289,r'(resp. \(K^{\bullet}(Y)\)) and',r'(resp. \(K^{\bullet}(Y)\) and','text','check/findings/findings_286_290.json#16')
add(194,292,r'K_{\bullet}',r'K','math','check/findings/findings_291_295.json#5',r'\sgaStableTarget{sga6.e04.para.3-2-1}',r'\sgaStableTarget{sga6.e04.para.3-2}')
add(195,292,r'u:\Ob\Loclib(X)\longrightarrow \varinjlim K^{\bullet}(X_i)_{\naif}',r'u:\Ob\Loclib(X)\longrightarrow \lim K^{\bullet}(X_i)_{\naif}','math','check/findings/findings_291_295.json#12')
current='\\begin{equation}\\tag{3.2.3.1} \\varinjlim K_{\\bullet}(X_i)\\xrightarrow{\\sim}K_{\\bullet}(X).\n\\end{equation}'
printed='\\begin{equation}\\tag{3.2.2.1}\n \\varinjlim K_{\\bullet}(X_i)\\xrightarrow{\\sim}K_{\\bullet}(X).\n\\end{equation}'
add(196,293,current,printed,'display','check/findings/findings_291_295.json#18','The proof is analogous to that of (3.2.1)')
end='\\[\n\\begin{tikzcd}[column sep=tiny]'
add(197,293,'via the isomorphisms (3.2.1.1) and (3.2.3.1) with','via the isomorphisms (3.2.1.1) and (3.2.2.1) with','text','check/findings/findings_291_295.json#18',end)
add(198,293,'the vertical arrows are defined by (3.2.1.1) and (3.2.3.1)','the vertical arrows are defined by (3.2.1.1) and (3.2.2.1)','text','check/findings/findings_291_295.json#18',end)
amendment=next(json.loads(x) for x in (R/'review/expose_iv_amendments/own_findings.jsonl').read_text().splitlines() if json.loads(x)['page']==289)
variants.append(dict(id='EN-VAR-200',page=289,old='(III 4.8.1 and 5.8 b))',printed='(III 4.8.1 and 5.9 b))',corrected='(III 4.8.1 and 5.8 b))',mode='text',source=amendment['source_id'],reason=amendment['reason'],scope_start='%%%%%%%%%%  scan idx 302  |  folio 289',scope_end='%%%%%%%%%%  scan idx 303  |  folio 290',scan_image=amendment['image'],scan_region=amendment['region']))
ledger=[];unit_count=0
for layer,reading in [('current','corrected'),('diplomatic','printed')]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text);fr,reference=load_reviewed_pages(293,layer,start=289)
 for page in range(289,294):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  counts={}
  for token in [r'\underline{O}',r'\underline O',r'\uparf',r'\naif',r'\Ob',r'\Hom',r'\Parf',r'\xrightarrow{\sim}',r'\begin{tikzcd}',r'\SGAAuthorFootnote{1}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every complete mathematical unit agrees literally in its source branch, including all four full diagrams and the duplicate/current equation tag. No lexical exception; original note and individual structure-sheaf rules match.',source=next(x for x in reference['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iv/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 289<=p['page']<=293:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for raw in (R/'review/expose_iv_amendments/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if p['page']==289:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Current locator repaired by the independently re-viewed exact adjunction map; printed locator retained diplomatically.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=289,source_id='full perfect direct-image conclusion',decision='Restore the two exact y-domains and their distinct inverse-image locators, all transitivity hypotheses, explicit Riemann–Roch motivation, both repeated ample-invertible-sheaf scheme names, and original sorites wording. Apply the separate post-freeze reviewer locator amendment to III5.8(b) in current, retaining5.9 in diplomatic; the exact projection comparison and all theorem hypotheses remain unchanged.'),
 dict(page=290,source_id='ASTRA-IV-AUTHOR-NOTE-290; full Proposition3.1.0',decision='Restore the original numerical1 section-title note, the plain proposition statement, complete quasi-compact/quasi-separated and Tor-independent hypotheses, exact finite-tor/finite-flat-amplitude alternatives, headed Hom-adjunction formula and all four stated cohomological bounds. The original SGA4XVII locators and exact arrow Rf_*E→Rf_*Rg_*Lg^*E are preserved.'),
 dict(page=290,source_id='check/findings/findings_286_290.json#19',decision='The French vérifié/vérifie pair repairs the finite verb after on. English we easily verify renders the same assertion in both forms, with the two displayed derived-category memberships unchanged; no artificial English tense error is introduced.'),
 dict(page=291,source_id='complete affine base-change proof',decision='Restore the Leray-covering reduction, the source cocartesian ring-square orientation, every original A/A-prime/B/B-prime position and both headed derived-tensor comparisons. The second complete Cartesian square begins Proposition3.1.1 at the exact printed boundary.'),
 dict(page=292,source_id='complete Proposition3.1.1 and vector-bundle limit construction',decision='Restore all independently ruled words, plain source locators and exact alternate domains/pullback/pushforward definitions. Restore the affine-transition scheme system, source bare limit indices and all five EGA descent references. The map u(E) is explicitly the image of cl(E_i) in the same direct-limit target, which determines the rightward-arrow repair.'),
 dict(page=293,source_id='complete perfect/coherent limit constructions',decision='Restore the source categorical capital Lim with rightward lower arrow, separate Parf(X_i) expression and all unindexed group limits. The actual hypothesis is flat f_ij, with flat f_i as its consequence; the inherited English had reversed these. Restore the displayed coherent-group comparison and the full final module diagram, including both headless isomorphism labels on their actual source sides. The tag correction and both references identify the exact beta map described in the source decision, without asserting an identification of the two K-groups.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt,(ot-nt,nt-ot)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 289<=x['page']<=293];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_IV_TRANSFER_289_293.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('290\t')];notes.append('290\tAt the end of the section3 title\traised numerical1 inside baseline parentheses\t1\tASTRA-IV-AUTHOR-NOTE-290\treviewer direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete original statement that these results are not used in ExposésV–VIII.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
