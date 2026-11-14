#!/usr/bin/env python3
"""Register Exposé IV's exact K-group definitions and first tensor pairings."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_IV_P279_283.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('The last two categories are full subcategories')
tail='with the structure of a commutative ring with unit\n';b=native.index(tail,a)+len(tail)
record=dict(id='EN-EXPOSE-IV-279-283',page='279–283',place='Exact K-group definitions, coherent-ring case, bimodule pairings and inverse images',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by reviewer',source='build/page_packets/279–283/current.tex and diplomatic.tex; review/expose_iv/patches.jsonl',reason='Restores all source left/right module indices, raised/lowered K dots, unrestricted and bounded derived categories, distinct plain/ruled amplitude subscripts, actual Loclib_A-prime notation, two full comparison diagrams and original note279. Two printed/current source differences are explicit.')
decisions=[json.loads(x) for x in (R/'review/expose_iv/decisions.jsonl').read_text().splitlines()]
variants=[]
def add(no,page,old,printed,mode,source,end):
 d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=end,scan_image=d['image'],scan_region=d['region']))
add(187,281,r"K^{\bullet}({}_{A'} X'_A)_{A'}=k(D({}_{A'} X'_A)_{A'\text{-}\parf}).",r"K^{\bullet}({}_{A'} X'_A)_{A'}=k(D({}_{A'} X'_A)_{A'\text{-}\parf}.",'math','check/findings/findings_281_285.json#8','%%%%%%%%%%  scan idx 295  |  folio 282')
add(188,283,'in (2.6.5) (resp. (2.6.2))','in (2.6.2) (resp. (2.6.5))','text','check/findings/findings_281_285.json#11',r'\sgaStableTarget{sga6.e04.eq.2-7-3}')
ledger=[];unit_count=0
for layer,reading in [('current','corrected'),('diplomatic','printed')]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text);fr,reference=load_reviewed_pages(283,layer,start=279)
 for page in range(279,284):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  counts={}
  for token in [r'\underline{O}',r'\parf',r'\uparf',r'\mathrm{parf}',r'\naif',r'\Ob',r'\Loclib',r'\SGAAuthorFootnote{1}',r'\hookrightarrow',r'\Id',r'\begin{tikzcd}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All complete mathematical units match literally without a lexical exception, including both complete diagrams and every module-side index. Independent plain/ruled parfait tokens, hooked arrows and the original numerical note have matching counts.',source=next(x for x in reference['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iv/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 279<=p['page']<=283:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=279,source_id='complete Definition2.2 and ASTRA-IV-AUTHOR-NOTE-279',decision='Restore each separately stacked K-group definition with source raised/lowered dots and left A-subscript, all four source plain/ruled amplitude forms and the complete original numerical1 note before the sentence stop. The note names the literal naïf subscript whose source glyph expansion was restored at273. All definition word rules exclude the note and preserve the parenthetical alternatives.'),
 dict(page=280,source_id='complete Remarks2.3(b,c),2.4 and2.5',decision='Preserve the source A-is-coherent wording without importing an extra left-module clause from inherited English. Restore the literal five-term k-equality and inline coproduct justification, all two4.1/2.4.2 functor locators, the source hooked inclusion arrows, and the separate plain paragraph numbers/ruled headings. Keep the source assertion about the canonical homomorphism as authored; no added claim is supplied.'),
 dict(page=281,source_id='full hypotheses and2.6 bimodule setup',decision='Restore both exact hypotheses, the compact regular-local-ring example, Loclib_{A-prime} on the left-A-prime/right-f-inverse-A bimodule category, the complete underived tensor map with no added terminal comma, and all exact source D categories. The inherited English D-minus restrictions in the definition and later2.6.4 are removed because they are absent from both reviewed source layers; the explicitly D-minus derived tensor domain on282 remains as printed. Markers280 and281 follow their item commands, so no visible material precedes an initial item.'),
 dict(page=282,source_id='complete compatibility square2.6.6',decision='Restore the three individual comparison homomorphisms, actual degree-unrestricted finite-perfect-amplitude categories in2.6.4, the separately D-minus domain of derived tensor, and every object and arrow in2.6.6. The explanation identifies both horizontal maps and all three vertical comparison locators exactly. Stable link targets remain outside complete mathematical units.'),
 dict(page=283,source_id='complete2.7(a) and beginning(b)',decision='Restore the source heading without an inserted full stop, original inline morphism and Lf-star display domain, both source pairings and the complete commutative square, all three transitivity references and the exact(gf)-star identity. Preserve the individually ruled conclusion and beginning of the commutative-ring assertion, source capital Id, and the exact folio boundary before the unit formula.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt,(ot-nt,nt-ot)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 279<=x['page']<=283];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_IV_TRANSFER_279_283.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('279\t')];notes.append('279\tAfter ambient-category Mod expression, before stop\traised numerical1 inside baseline parentheses\t1\tASTRA-IV-AUTHOR-NOTE-279\treviewer direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete permission to omit A or explicitly omit the naïf subscript.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
