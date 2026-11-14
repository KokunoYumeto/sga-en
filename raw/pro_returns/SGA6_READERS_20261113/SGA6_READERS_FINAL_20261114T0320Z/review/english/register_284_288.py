#!/usr/bin/env python3
"""Register augmented K-algebras, direct images and the restricted module action."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_IV_P284_288.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('\\[\n 1=\\cl(\\mathcal O_X).\n\\]',native.index(r'\sgaStableTarget{sga6.e04.para.2-7}'))
b=native.index('Now suppose that we are in the situation',a)
record=dict(id='EN-EXPOSE-IV-284-288',page='284–288',place='Augmented algebra structure, global-resolution comparison, covariance and finite-tor inverse images',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by reviewer',source='build/page_packets/284–288/current.tex and diplomatic.tex; review/expose_iv/patches.jsonl',reason='Restores the exact augmentation diagram and starred historical paragraph, all global-resolution cases, the complete algebraic/analytic direct-image assertions and historical discussion, bounded intermediate categories in2.12, and the source module-action expression. Four existing source differences and the newly scan-adjudicated III5.9(b) to III5.8(b) locator repair are explicit.')
decisions=[json.loads(x) for x in (R/'review/expose_iv/decisions.jsonl').read_text().splitlines()];variants=[]
def add(no,page,old,printed,source):
 d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode='text',source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',scan_image=d['image'],scan_region=d['region']))
add(189,284,r'\(K^{\bullet}(X)_{\naif}\to K^{\bullet}(X)\)) the structure',r'\(K^{\bullet}(X)_{\naif}\to K^{\bullet}(X)\) the structure','check/findings/findings_281_285.json#22')
add(190,285,'(V 3.9.1 and VI)',r'(V 3.9.1 and VI\qquad)','check/findings/findings_281_285.json#26')
add(191,285,'Deligne [1]','Deligne [5]','check/findings/findings_281_285.json#27')
add(192,286,'Thanks to the associativity','Thanks,to the associativity','check/findings/findings_286_290.json#8')
amendment=next(json.loads(x) for x in (R/'review/expose_iv_amendments/own_findings.jsonl').read_text().splitlines() if json.loads(x)['page']==287)
variants.append(dict(id='EN-VAR-199',page=287,old='(III 5.8 b))',printed='(III 5.9 b))',corrected='(III 5.8 b))',mode='text',source=amendment['source_id'],reason=amendment['reason'],scope_start='%%%%%%%%%%  scan idx 300  |  folio 287',scope_end='%%%%%%%%%%  scan idx 301  |  folio 288',scan_image=amendment['image'],scan_region=amendment['region']))
ledger=[];unit_count=0
for layer,reading in [('current','corrected'),('diplomatic','printed')]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text);fr,reference=load_reviewed_pages(288,layer,start=284)
 for page in range(284,289):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  counts={}
  for token in [r'\underline{O}',r'\uparf',r'\naif',r'\Ob',r'\Rg',r'\begin{tikzcd}',r'\textsuperscript{*}',r'\textsubscript{*}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All complete mathematical units match literally without lexical exceptions. The four-column augmentation diagram, source tensor subscripts and raised/lowered interpolation stars are preserved.',source=next(x for x in reference['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iv/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 284<=p['page']<=288:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for raw in (R/'review/expose_iv_amendments/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if p['page']==287:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Current locator repaired by the independently re-viewed exact adjunction map; printed locator retained diplomatically.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=284,source_id='complete2.7(b) conclusion and2.8',decision='Restore the inline parenthesized unit equality, precise2.6.3.2 locator, both unital-ring conclusions and full augmented algebra construction. Both inverse-image homomorphisms and all rank-compatibility locators remain explicit; no displayed group or augmented-ring arrow is contracted.'),
 dict(page=285,source_id='complete augmentation diagram and historical interpolation',decision='Restore all eight objects, all ten arrows and their labels in the augmentation diagram. The historical interpolation opens with a raised star and closes with a lowered star; it is not converted into an author footnote. Preserve its exact characteristic hypothesis, Grothendieck conjecture attribution and historical wording. The untyped gap afterVI remains a formatting variant with no invented missing numeral.'),
 dict(page=285,source_id='three global-resolution cases',decision='Preserve every source qualification and exact II reference in the divisorial, compact/soft and Stein cases, including separated or noetherian, the final-object quasi-compactness and both structure-sheaf equalities.'),
 dict(page=286,source_id='full2.10 and2.11.1',decision='Restore the source tensor_A label, exact uparf category, explicitly restricted K^bullet(Y)-module action, full finiteness proviso and omitted III2.2 locator. The displayed direct image on this folio has no added terminal stop. The stray comma in Grâce,à is represented between the two words of its exact English prepositional rendering Thanks,to only in the diplomatic branch.'),
 dict(page=287,source_id='complete algebraic and analytic projection assertions',decision='Preserve the precise y/x membership, no addedY on the left tensor in the source projection comparison, all direct-image and transitivity identities and the full analytic finiteness assertion. The separate post-freeze reviewer amendment identifies III5.8(b) by the identical adjunction-defined analytic projection map; current uses5.8 and diplomatic preserves5.9.'),
 dict(page=288,source_id='complete historical discussion and2.12',decision='Restore the source modality appears/seems, full mixed-variety and topological-vector-sheaf discussion, exact Grothendieck attribution and every finite-tor bounded-category intermediate step. These historical author statements are translated as supplied, without adding modern conclusions or a replacement definition.'),
 dict(page=288,source_id='fixes/RECONCILE_CODEX_6.json#289',decision='Retain f^*(ay)=a f^*(y) in both forms. The exact action is beta=rho_X composed with(alpha tensor identity), where alpha=f^*:K^bullet(Y)→K^bullet(X). Thus psi(rho_Y(a,y))=beta(a,psi(y))=rho_X(alpha(a),psi(y)); the printed middle expression and the proposed expanded final expression have the same displayed derived-tensor realization. No new source variant is introduced.',evidence='review/expose_iv/identification_288.json',evidence_sha256=hashlib.sha256((R/'review/expose_iv/identification_288.json').read_bytes()).hexdigest()),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt,(ot-nt,nt-ot)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 284<=x['page']<=288];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_IV_TRANSFER_284_288.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
