#!/usr/bin/env python3
"""Register the full tensor/coherence statements and their exact source maps."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
chunk=(H/'EN_EXPOSE_III_P231_235.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('This is a condition of local nature.',native.index(r'\sgaStableTarget{sga6.e03.def.1-5}'));b=native.index(r'\sgaStableTarget{sga6.e03.cor.1-12}',a)
record=dict(id='EN-EXPOSE-III-231-235',page='231–235',place='Tor-independence explanation through the complete proof of Proposition1.11',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/231–235/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores the actual downward arrows in1.5.1, plain derived L throughout this passage, original231 note, exact affine tensor calculation and immersion names, all omitted locators, the sufficiency direction in1.10(b), original statement diagrams and source bases, full affine-space reduction diagram, literal baseline functor placeholder, hooked cone edge, degree≥a and every final proof reference. The three actual source differences are explicit.')
cur,ref=load_reviewed_pages(235);dip,dref=load_reviewed_pages(235,'diplomatic');pages=split(chunk)
variants=[]
def add(no,page,old,printed,mode,source,reason,region):
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<235 else '',scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
tri=next(m.group() for m in MATH.finditer(pages[234]) if r'\begin{tikzcd}' in m.group());printed=tri.replace('arrow[dr,"h"','arrow[dr,"f"');assert tri!=printed
add(158,234,tri,printed,'display','check/findings/findings_231_235.json#18; fixes/FIXLOG_6_CURRENT.jsonl#375','The diagonal has endpoints X→Z and is the composite h=g composed with f. Its direct-image functor is h_*=g_*f_*, exactly the functor used in the subsequent relative condition and proof. Current retains h on this edge; diplomatic retains the printed f. The horizontal f:X→Y and vertical g:Y→Z are unchanged.','Diagonal label in Proposition1.11')
reason=json.loads((R/'review/expose_iii/projection_formula_235.json').read_text())['exact_morphism_proof']
add(159,235,'the isomorphism in (1.7)','the isomorphism (*) in the proof of (1.8)','text','check/findings/findings_231_235.json#28',reason,'Projection-formula locator in proof(a)')
add(160,235,r'h_*(E)',r'f_*(E)','math','check/findings/findings_231_235.json#27; fixes/FIXLOG_6_CURRENT.jsonl#376','Proposition1.11(b) assumes pseudo-coherence relative to h. After the stated reduction to closed immersions, its hypothesis is pseudo-coherence of h_*(E)=g_*f_*(E). With E_0=f_*(E), the following replacement X=Y and f=Id makes this precisely g_*(E_0), as used later in the proof. The conclusion remains pseudo-coherence of E_0. Only this first hypothesis in(b) changes from printed f_* to current h_*; all other f_* occurrences are preserved.','First hypothesis in proof(b)')
ledger=[]
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(231,236):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  counts={}
  for token in [r'\underline{O}',r'\operatorname{ob}',r'\operatorname{Sup}',r'\SGAAuthorFootnote{1}',r'\otimes^{L}',r'\otimes_S^{L}',r'\otimes_Y^{L}','hook',r'\xrightarrow{\sim}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every complete mathematical unit and every specified glyph count agrees literally; no mathematical-unit translation exception.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(fr[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if not 231<=p['page']<=235:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in faithful English in both source forms.',patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=231,source_id='reviewed1.5–1.7 and ASTRA-III-AUTHORNOTE-231',decision='Restore ordinary L in all derived tensor positions, the actual three downward arrows of the1.5.1 diagram, source plain statement body after its first ruled phrase, all operatorname ob forms, the inline f_i morphism and complete numerical1 note after E_i membership. Its category D(X_i)_qcoh has no extra minus superscript; the note belongs to the original source, not new apparatus.'),
 dict(page=232,source_id='reviewed affine calculation and Proposition1.8',decision='Restore the exact tensor order A_1 tensor_(B_1)^L B tensor_(B_2)^L A_2 and both source definitions of A/B, inline source intervals and membership, operatorname Sup capitalization, all source b_i bounds and actual f-prime_i factorization labels. Preserve the explicit I2.16 and1.7 locators and full proof without moving formulas into new displays.'),
 dict(page=233,source_id='reviewed Corollaries1.9 and1.10',decision='Restore the displayed cf.(1.2), all1.2/1.5 references, source square orientation, ordinary Lg*, and the actual sufficiency (il suffit) direction in the proof of1.10(b). The inherited English had necessity. Restore the omitted I2.16.2 reference. The final source à f-prime is rendered relative to f-prime by Definition1.2’s exact functor membership; no new hypothesis or variant is inserted.'),
 dict(page=234,source_id='reviewed Proposition1.11 and affine-space reduction',decision='Restore the ordinary source tensor base Y, operatorname Sup with its exact arguments, plain cf.(1.6), the complete seven-arrow affine-space diagram with three hooks and actual q:E_Z^s→Z, j_*(p^*(F)) parentheses, literal index x and reference1.2. The inherited rectangular diagram altered these edge endpoints and is replaced by the reviewed source diagram.'),
 dict(page=235,source_id='reviewed two-part proof1.11',decision='Restore the projection formula with no added left Y base or display comma, the literal baseline full-stop functor placeholder, the exact local-free/acyclic functor conditions, ordinary derived L, source ≥a induction wording, the distinct hooked upper-left triangle edge and all three term conditions E-prime^i/E-double-prime^i. Preserve every I2.10/I2.11(a)/I2.6/I2.10(b) reference and the original final sentence introducing the following corollaries.'),
 dict(page=235,source_id='review/expose_iii/projection_formula_235.json',decision='Carry the independently checked chain-map identification supporting the current locator repair, without claiming a new scan read or adding a quasi-coherence hypothesis.',source_packet_sha256=hashlib.sha256((R/'review/expose_iii/projection_formula_235.json').read_bytes()).hexdigest(),exact_morphism_proof=reason),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==7,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
(H/'EN_EXPOSE_III_TRANSFER_231_235.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('231\t')];notes.append('231\tAfter E_i membership, before the statement comma\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHORNOTE-231\tcoordinator direct primary/witness comparison, main PDF245\tSGAAuthorFootnote{1}\tComplete qcoh-subcategory note, preserving D(X_i) without a minus superscript.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=216,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
