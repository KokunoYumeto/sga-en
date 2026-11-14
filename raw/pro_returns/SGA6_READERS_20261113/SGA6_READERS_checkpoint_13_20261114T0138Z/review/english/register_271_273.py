#!/usr/bin/env python3
"""Register the complete close of ExposéIII and preserve the IV macro boundary."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P271_273.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'is locally constant on \(U\). This gives constructibility.',native.index(r'\sgaStableTarget{sga6.e03.cor.5-6}'))
b=native.index(r'\sgaStableTarget{sga6.e04.expose}',a)
record=dict(id='EN-EXPOSE-III-271-273',page='271–273',place='Full semicontinuity proposition and analytic remark, complete bibliography and ExposéIV continuation macros',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/271–273/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores the exact y-indexed rank function and T-minus-p functor, actual relative uniformly-perfect category, complete alternating-rank formula and quantifiers, both Künneth hypotheses, the full analytic assertion and historical author note, original bibliography keys and all continuation macro definitions. Six source differences are explicit; two French spelling corrections leave English unchanged.')
decisions=[json.loads(x) for x in (R/'review/expose_iii/decisions.jsonl').read_text().splitlines()];variants=[]
def add(no,page,old,printed,mode,source):
 d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<273 else '% SGA_NATIVE_CONTINUATION_273',scan_image=d['image'],scan_region=d['region']))
add(181,271,r'y\mapsto\operatorname{rg}_{k(y)}H^p(E\otimes_X^{\mathrm L}k(y))',r'y\mapsto\operatorname{rg}_{k(x)}H^p(E\otimes_X^{\mathrm L}k(y))','math','check/findings/findings_266_270.json#12')
add(182,271,r'\(H^i(Rf_*(E)\otimes_Y^{\mathrm L}k(y))\) \uline{are vector spaces of finite rank over}',r'\(H^i(Rf_*(E)\otimes_Y^{\mathrm L}k(y)\) \uline{are vector spaces of finite rank over}','text','check/findings/findings_271_275.json#4')
add(183,271,r'y\longmapsto\sum(-1)^i\operatorname{rg}_{k(y)}H^i(Rf_*(E)\otimes_Y^{\mathrm L}k(y))',r'y\longmapsto\sum(-1)^i\operatorname{rg}_{k(y)}H^i(Rf_*(E)\otimes_Y^{\mathrm L}k(y)','math','check/findings/findings_271_275.json#5')
add(184,271,r'y\longmapsto\operatorname{rg}_{k(y)}H^p(Rf_*(E)\otimes_Y^{\mathrm L}k(y))',r'y\longmapsto\operatorname{rg}_{k(y)}H^p(Rf_*(E)\otimes_Y^{\mathrm L}k(y)).','math','check/findings/findings_271_275.json#6')
add(185,272,'(cf. (EGA III 6) and (IV 3.1.0))','(cf. (EGA III 6 and (IV 3.1.0)','text','check/findings/findings_271_275.json#10')
add(186,273,r'Rf_*(E)\otimes^{\mathrm L}M\longrightarrow Rf_*(E\otimes_Y^{\mathrm L}M)',r'Rf_*(E)\otimes^{\mathrm L}M)\longrightarrow Rf_*(E\otimes_Y^{\mathrm L}M)','math','check/findings/findings_271_275.json#12')
cur,ref=load_reviewed_pages(273,start=271);dip,dref=load_reviewed_pages(273,'diplomatic',start=271);ledger=[];unit_count=0
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(271,274):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  ff=fr[page].split('% Exposé IV macros')[0];ee=en[page].split('% SGA_NATIVE_CONTINUATION_273')[0];counts={}
  for token in [r'\underline{O}',r'\Ob',r'\mathrm L',r'\xrightarrow{\sim}',r'\operatorname{rg}',r'\sum',r'\uparf',r'\SGAAuthorFootnote{1}']:
   counts[token]=dict(French=ff.count(token),English=ee.count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All complete mathematical units match literally without a lexical exception. Body glyph counts exclude the separately preserved native and French continuation macro blocks; all displayed arrows and original-note calls agree.',source=next(x for x in rr['bases'] if x['page']==page),counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 271<=p['page']<=273:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=271,source_id='complete Corollary5.6 conclusion and Proposition5.7',decision='Restore the exact y-indexed rank function, source T_{-p}=H^p(E tensor baseline point), full proof locators, D^b(f)_uparf hypothesis and4.2 reference. Preserve the author’s historical2.1 proviso. Restore the complete bare alternating sum, every scalar field and repeated exact functor, all three conclusions and the local noetherian/reduced hypothesis exactly as stated.'),
 dict(page=272,source_id='full proof and Remark5.8(a)',decision='Restore the separate source paragraphs and source proof arrow without adding an isomorphism sign to that arrow. Preserve both explicit flatness alternatives in5.8(a), both precise EGA references and the visibly headed Künneth comparison, together with both ordinary/derived inverse-image alternatives. The citation delimiter repair preserves the exact original citation tokens.'),
 dict(page=273,source_id='complete analytic remark and ASTRA-III-AUTHOR-NOTE-273',decision='Restore the entire analytical projection-formula assertion, actual D-minus hypotheses and coherent-cohomology explanation, source left tensor without an addedY subscript, exact T.FII5.12 boundedness explanation, final no-additional-E-hypothesis sentence and the full original numerical1 note with its historical Grauert/EGA attribution. The source idiom tapis is rendered a body of results in this explicit exchange/semicontinuity context.'),
 dict(page=273,source_id='check/findings/findings_271_275.json#13; #19; fixes/MISPRINTS_6.json#240; #241',decision='The source isomorphime/isomorphisme and oadre/cadre pairs are French spelling repairs. English isomorphism and setting render the same expressions in both branches; no extra English lexical error or change to the mathematical map is manufactured.'),
 dict(page=273,source_id='complete source bibliography',decision='Preserve the three actual keys[1],[H],[T.F], original title wording/capitalization, ellipsis after the Grauert title, Pub.IHES wording, Lecture Notes wording and historical years. The inherited English’s added in Mathematics and automatic numeric[2]/[3] keys are removed; publication titles remain in their source languages.'),
])
start=native.index(r'\providecommand{\Ob}',native.index(r'\sgaStableTarget{sga6.e03.bibliography}'));native_block=native[start:native.index(r'\sgaStableTarget{sga6.e04.expose}',start)]
fr_block=cur[273][cur[273].index('% Exposé IV macros'):]
assert chunk.count(native_block)==1 and chunk.count(fr_block)==1
assert chunk.endswith(r'\renewcommand{\naif}{\text{naïf}}'+'\n\n')
ledger.append(dict(page=273,source_id='EN-MACRO-BOUNDARY-273',decision='Preserve the native continuation block first and the reviewed French continuation block second, at their actual post-bibliography location. The reviewed Ob/id renewals remain exact. Native naif is provided first as mathrm{naif}; the later French provide of text{naïf} would otherwise be inactive. A final explicit local renewal to text{naïf} restores exactly the reviewed French glyph expansion for the identical naive-group subscript in both reader forms. No group or map is changed; every argument of each K expression remains unchanged.',native_macro_block=native_block,native_macro_sha256=sha(native_block),reviewed_French_macro_block=fr_block,reviewed_French_macro_sha256=sha(fr_block),local_expansion_restoration=r'\renewcommand{\naif}{\text{naïf}}',status='both-form source-glyph transfer; no new source variant; runtime accented glyph verified in through273 corrected output154, see EN_PDF_VISUAL_QA.json'))
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==3,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 271<=x['page']<=273];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_271_273.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('273\t')];notes.append('273\tAfter continuity properties in Remark5.8(b)\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHOR-NOTE-273\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete historical origin note naming Grauert and EGAIII7.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
