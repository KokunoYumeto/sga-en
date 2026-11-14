#!/usr/bin/env python3
"""Register the full local perfection proof and the first fibrewise criterion."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P251_255.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('of a regular immersion and a smooth morphism',native.index(r'\sgaStableTarget{sga6.e03.ex.4-1-1}'))
b=native.index(r'\(E^a/B^a\) is \(h\)-flat.',native.index('On the other hand, the Tor-amplitude',a))
record=dict(id='EN-EXPOSE-III-251-255',page='251–255',place='Relative-perfect categories, complete local criterion proof and beginning of the fibrewise criterion proof',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/251–255/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores all six source category notations and exact parf rule, the complete local-flatness/noetherian-approximation proof, omitted corollary proof and references, original triangles and full hypotheses, the original criterion note, and all three truncation/fibre displays with their observed labels. Seven source differences are explicitly represented; the fibre comparison stays unlabelled in both branches.')
decisions=[json.loads(x) for x in (R/'review/expose_iii/decisions.jsonl').read_text().splitlines()]
variants=[]
def add(no,page,old,printed,mode,finding):
 source=f'check/findings/findings_251_255.json#{finding}';d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<255 else '',scan_image=d['image'],scan_region=d['region']))
add(165,251,'is a perfect morphism.','is a perfect morphism','text',2)
add(166,252,r'g_\alpha^*(F_\alpha)\simeq F_\alpha',r'g_\alpha^*(F)\simeq F_\alpha','math',6)
add(167,253,r'\parfamp(i_*(E))\subset[a,b]\Longrightarrow\parfamp_f(E)\subset[a,b]',r'\parfamp(i_*(E)\subset[a,b]\Longrightarrow\parfamp_f(E)\subset[a,b]','math',8)
add(168,254,'It also implies (by 4.3),','It also implies. by 4.3),','text',10)
add(169,255,r'is, in a neighborhood of \(x\), acyclic outside',r'is, in a neighborhood of \(s\), acyclic outside','text',15)
add(170,255,'Thus, after localizing, we may suppose','Thus, after localizing,. we may suppose','text',18)
add(171,255,r'arrow \((t)\)',r'arrow \((*)\)','text',17)
cur,ref=load_reviewed_pages(255);dip,dref=load_reviewed_pages(255,'diplomatic');ledger=[];pairs=[];unit_count=0
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(251,256):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));missing=f-e;extra=e-f
  assert sum(missing.values())==sum(extra.values())==int(page==253),(page,layer,missing,extra)
  if layer=='current':unit_count+=sum(f.values())
  for ff,n in missing.items():
   ee=ff.replace(r'\text{ et }',r'\text{ and }');assert ee!=ff and extra[ee]==n==1
   pairs.append(dict(page=page,layer=layer,French_literal_unit=ff,English_literal_unit=ee,expected_multiplicity=1,status='confirmed complete lexical formula translation: et becomes and; all other characters remain identical',scope='The exact Proposition4.5 display in the stated source branch.'))
  counts={}
  for token in [r'\underline{O}',r'\uparf',r'\parf',r'\Ob',r'\mathrm L',r'\simeq',r'\ldots',r'\tag*',r'\notag',r'\SGAAuthorFootnote{1}','hook']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All mathematical units match literally apart from the one separately paired connective; all counted glyphs, displayed labels and original-note calls agree.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 251<=p['page']<=255:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=251,source_id='reviewed Notation4.2 and Proposition4.3',decision='Restore all three plain-parf and all three ruled-parf category names, their full explanatory paragraph and exact quasi-compact equality. Preserve the printed colon after item(i), explicit point x and image y, and the complete proof: I2.1, actual quotient truncation with low dots and no extra arrow before E^b, stalk flatness, EGAIV11.3.1, F=E^a and the final embedding reduction. No derived-category membership or scheme variable is silently substituted.'),
 dict(page=252,source_id='reviewed full noetherian approximation and corollaries',decision='Restore X=Y[t1,…,tr], every indexed affine scheme and module, both source EGA limit references, the two headless pullback comparisons and the actual ordinary/derived tensor identification. Restore the omitted proof of4.3.1, exact1.2.1(c) locators and the correct I4.15/2.11 proof citation for4.3.2. Restore the hooked triangle with X,Y,S and its low comma.'),
 dict(page=253,source_id='reviewed Propositions4.4/4.5 and Corollary4.5.1',decision='Restore the full absolute-perfect reference I4.8, explicit interval and Z, both numbered inline implications, actual three-column triangle over S, both D-minus hypotheses and complete perfectness conclusion. The source proof really cites1.11, as the reviewer resolved in both scans; retain both digits in both English branches without an invented1.1/1.11 source variant. Both corollary bounds and the derived Lf* argument are literal.'),
 dict(page=254,source_id='ASTRA-III-AUTHOR-NOTE-254 and reviewed criterion4.6',decision='Restore the complete original numerical1 note at the underlined criterion title, with its EGAIV11.3.10 flatness-by-fibers reference. Preserve plain flat after the ruled hypothesis, exact D-minus membership, full Spec(k(s)) base change and both numbered conditions. Restore the entire forward implication with its actual I5.1(i) scalar-extension comparison; keep the folio boundary inside the concluding sentence.'),
 dict(page=255,source_id='reviewed backward implication of4.6',decision='Restore the complete factorization and replacement argument, source g-perfect/h-perfect deductions and the actual1.12 and I2.1 locators, both original truncation complexes, literal t) and i*(t) labels, and the headless unlabelled fibre comparison. Preserve ordinary i* for the chosen complex and the full amplitude/flatness argument. The original255 boundary ends after the I5.1.1 citation, before the h-flat conclusion on256.'),
])
for relative in ['review/expose_iii/truncation_reference_255.json','review/english/EN_INDEPENDENT_III_TRUNCATION_AUDIT_255.json']:
 p=R/relative;assert p.exists();ledger.append(dict(page=255,source_id='check/findings/findings_251_255.json#17',source_packet=relative,source_packet_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),decision='Apply only the supported final reference(*)→(t) correction. The exact truncation chain map and LemmaI5.1.1 tensor test are retained in this independent proof audit; no label is added to the intervening unlabelled fibre comparison.',status='text/math audit with separately attributed scan observations; no fresh image claim'))
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
for pair in pairs:ledger.append(dict(page=pair['page'],source_id='individually checked complete lexical display',decision='Only et is translated.',**{k:pair[k] for k in ['layer','French_literal_unit','English_literal_unit','expected_multiplicity']}))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==9,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 251<=x['page']<=255]+pairs;path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_251_255.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('254\t')];notes.append('254\tAfter criterion of perfection by fibers title\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHOR-NOTE-254\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete analogy with the flatness-by-fibers criterion EGAIV11.3.10.');path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=len(pairs),transfer_rows=len(ledger),stable_targets=len(ot))))
