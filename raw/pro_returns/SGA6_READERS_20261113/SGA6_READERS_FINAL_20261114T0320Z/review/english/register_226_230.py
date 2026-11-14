#!/usr/bin/env python3
"""Register III226–230, including exact cubes, definitions and source variants."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
chunk=(H/'EN_EXPOSE_III_P226_230.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'Thus one may suppose that \(Y=Z[T_1,\ldots,T_r]\)',native.index(r'\sgaStableTarget{sga6.e03.expose}'));b=native.index('This is a condition of local nature.',a)
record=dict(id='EN-EXPOSE-III-226-230',page='226–230',place='Completion of1.1.4 and1.1, relative pseudo-coherence definitions and the opening of tor-independence',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/226–230/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores the actual ring triangle and epsilon/sigma maps, both tagged factorization diagrams, all twelve cube edges and three horizontal hooks, the source(A) labels, curved i_2 arrow and unprimed final direct image, exact source word-rule scopes and category subscripts, all three remarks, the two unmarked source triangles and table, and the independent Tor rules. Both actual source variants are explicit.')
current,ref=load_reviewed_pages(230);dip,dref=load_reviewed_pages(230,'diplomatic');pages=split(chunk)
variants=[]
def add(no,page,old,printed,mode,source,reason,region):
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<230 else '',scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
equation=next(m.group() for m in MATH.finditer(pages[226]) if m.group().startswith(r'\begin{equation}'))
printed=equation.replace('arrow[r,"i\'"','arrow[r,"i\'\'"');assert printed!=equation
add(156,226,equation,printed,'display','check/findings/findings_226_230.json#3; fixes/FIXLOG_6_CURRENT.jsonl#374','The top edge has endpoints X-prime→Y-prime. The following text names that immersion i-prime and uses its direct-image functor i-prime_*p-prime*. The next-page cube identifies the same endpoints and edge as i-prime. Thus the endpoint-preserving map from the first diagram to the corresponding cube face identifies its label with i-prime. Current keeps that single prime; diplomatic preserves the printed double prime. The distinct second factorization retains i-double-prime.','Top edge of tagged diagram(a-prime)')
add(157,230,r'\underline{\Tor}_i^S(\underline{O}_X,\underline{O}_Y)',r'\underline{\Tor}_i^S(\underline{O}_X,O_Y)','math','check/findings/findings_226_230.json#14','The source names X,Y,S with affine rings B,C,A and the tensor comparison B tensor-derived_A C→B tensor_A C. The two sheaf arguments restrict to B and C by the structure maps A→B and A→C. Thus the Y argument is the same structure sheaf of Y used in that calculation. Diplomatic retains its isolated missing rule; current retains the established rule on that same O_Y without changing the sheaf, indices or tensor map.','Second structure-sheaf argument in Definition1.5')
ledger=[];pairs=[]
for layer,reading,fr,rr in [('current','corrected',current,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text);part=text[a:b];assert part.count(v['old'])==1
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(226,231):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));missing=f-e;extra=e-f
  assert sum(missing.values())==sum(extra.values())==int(page==230),(layer,page,missing,extra)
  for ff,n in missing.items():
   ee=ff.replace(r'\uline{pour}',r'\uline{for}');assert extra[ee]==n==1
   pairs.append(dict(page=page,layer=layer,French_literal_unit=ff,English_literal_unit=ee,expected_multiplicity=1,status='confirmed complete lexical formula translation: only the independently underlined pour becomes for; all source arguments, notation, rule commands and whitespace retained',scope='This exact display in the stated source branch only.'))
  counts={}
  for token in [r'\underline{O}',r'\underline{\Tor}',r'\varepsilon',r'\sigma',r'\operatorname{ob}',r'\Ob',r'\underline n','hook','bend right',r'\coprod']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All mathematical units agree literally apart from the individually approved one-word display translation; exact command multiplicities verified.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(fr[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if not 226<=p['page']<=230:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English passage in both source forms.',patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=226,source_id='reviewed continuation of1.1.4',decision='Restore B above C with arrows u:B→A, v:C→A and epsilon:C→B, and the exact inline retraction sigma:B→C with sigma(T_i)=z_i and v sigma=u. Remove the inherited erroneous c(T_i) expression. Retain the quoted(*) reference, the section identity i=sj and both source locators. Both bare coproducts, the(a-prime) tag and the correct f-prime endpoint Y are restored.'),
 dict(page=227,source_id='reviewed proof of independence and assertion(A)',decision='Restore the(a-double-prime) tag and all references to the two diagrams. Restore the actual two square faces with common product vertices, all twelve arrows and three horizontal hooks. Preserve the literal(A) label, two hooked statement arrows, lowercase ob and full underlined predicate. The inherited serial four-row chain did not contain these source edges.'),
 dict(page=228,source_id='reviewed proof(A) and Definition1.2',decision='Restore all three diagram hooks, the curved unhooked i_2 composite and its target Y_2, all four quoted comparison conditions, final unprimed i_{2*}(E), source(a-prime) reference and complete closing proof. In Definition1.2 the first two defined predicate phrases remain plain; only the third pseudo-coherent relative to phrase is ruled, matching the independently reviewed source scopes.'),
 dict(page=229,source_id='reviewed Definition1.2 continuation and Remarks1.2.1',decision='Preserve the continuous definition paragraph, plain mathematical symbols and quotation marks, exact Y-hyphen-n-hyphen-coh and Y-hyphen-coh subscripts, and the two displayed intersections in their gathered layout. Translate every remark, retaining abbreviated rel. to and original I2.9/EGAIV1.4 locators. The English adjective full precedes subcategory across228/229 for ordinary English word order; D(X) and all remaining mathematical units stay in their corresponding source folios.'),
 dict(page=230,source_id='reviewed Proposition1.4 and Definition1.5',decision='Restore Examples1.3 reference1.1.2, both triangular diagrams with no transverse tick or written[1], their lower-level comma, all nine source table entries with exactly three ruled conclusions, lowercase lexical tor, both independently ruled Tor operators, and the locally defined hyper-tor reference. The original boundary ends after EGAIII6.5; its next explanatory paragraph begins in231.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
for pair in pairs:ledger.append(dict(page=pair['page'],source_id='individually checked exact lexical display',decision='only the source connective pour is translated',**{k:pair[k] for k in ['layer','French_literal_unit','English_literal_unit','expected_multiplicity']}))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==5
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 226<=x['page']<=230]+pairs;path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_226_230.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=171,lexical_pair_records=len(pairs),transfer_rows=len(ledger),stable_targets=len(ot))))
