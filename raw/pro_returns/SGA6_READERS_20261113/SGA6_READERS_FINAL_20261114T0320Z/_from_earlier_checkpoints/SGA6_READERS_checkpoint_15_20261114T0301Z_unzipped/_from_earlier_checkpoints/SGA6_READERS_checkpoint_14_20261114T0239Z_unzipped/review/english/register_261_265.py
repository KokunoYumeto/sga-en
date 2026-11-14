#!/usr/bin/env python3
"""Register complete exchange-lemma proof and the full base-change assertion."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P261_265.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'of the form \(\mathcal O_{U,X}\)',native.index(r'\sgaStableTarget{sga6.e03.lem.5-1}'))
b=native.index(r'If \(E\) satisfies (\hyperlink{sga6.e03.lem.5-1}',native.index(r'\sgaStableTarget{sga6.e03.eq.unnamed.occ2}',a))
record=dict(id='EN-EXPOSE-III-261-265',page='261–265',place='Complete exchange lemma proof, its four remarks, exchange property and base-change lemma',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/261–265/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores all omitted functors, extension-by-zero identifications, exact truncation bounds, four complete remarks, full exchange hypotheses and canonical-arrow constructions, both original numerical notes and the entire affine and dual comparison proof. Two source differences are explicit; the French pseuso spelling error has no separate English semantic reading.')
decisions=[json.loads(x) for name in ['decisions.jsonl','own_findings.jsonl'] for x in (R/'review/expose_iii'/name).read_text().splitlines()]
variants=[]
def add(no,page,old,printed,source):
 d=next(x for x in decisions if x['source_id']==source)
 variants.append(dict(id=f'EN-VAR-{no:03}',page=page,old=old,printed=printed,corrected=old,mode='text',source=source,reason=d['reason'],scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<265 else '',scan_image=d['image'],scan_region=d['region']))
add(175,261,'strictly perfect (I 2.1)','strictly perfect (2.1)','ASTRA-III-REFERENCE-261')
add(176,262,"condition analogous to a) (resp. a'), etc.) in which","condition analogous to a) (resp. a'), etc). in which",'check/findings/findings_261_265.json#8')
cur,ref=load_reviewed_pages(265);dip,dref=load_reviewed_pages(265,'diplomatic');ledger=[];unit_count=0
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v['scope_end'] else len(text);part=text[a:b];assert part.count(v['old'])==1,(v['id'],part.count(v['old']))
  text=text[:a]+part.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(261,266):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));assert f==e,(page,layer,f-e,e-f)
  if layer=='current':unit_count+=sum(f.values())
  counts={}
  for token in [r'\underline{O}',r'\Ob',r'\mathrm L',r'\mathrm R',r'\simeq',r'\xrightarrow{\sim}',r'\underline{\Hom}',r'\underline{\mathrm{Hom}}',r'\tag',r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='All mathematical units match literally, including whitespace; no lexical math exception is needed. All counted glyphs, tags, arrow heads and original-note calls agree.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 261<=p['page']<=265:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred in the faithful English source branches.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=261,source_id='check/findings/findings_261_265.json#2; fixes/FIXLOG_6.jsonl#1188; fixes/MISPRINTS_6.json#224',decision='The French s-for-d spelling pseuso-cohérent and corrected pseudo-cohérent designate the same surrounding defined property. Both English forms use pseudo-coherent; no distinct mathematical property or English lexical error is manufactured. The original French variant remains fully recorded by its source identifiers.'),
 dict(page=261,source_id='complete proof5.1.1 and opening remarks',decision='Restore both literal baseline functor slots, the SGA4IV2.13 extension-by-zero comparison with each H^p and restriction, the source(*)/(***)/(**) references, labelled assertion5.1.1 and all three exact truncation bounds. Preserve the independent ordinary R and Hom rule, the full localization argument, and the exact local conditions of5.2(i). Mirror the original condi-/tion boundary using the same English split word.'),
 dict(page=262,source_id='complete Remarks5.2(ii)–(iv)',decision='Restore the exact finite p,q free-sheaf cokernel test, all point conditions, the full EGAIII7.4.2/I5.8.3 criterion and degree duality. Preserve D-minus, the sole lexical quasi-separated rule, every ordinary item label, both full equivalence chains and all quasi-coherent extension references. The native English had substituted three implication assertions for the actual equivalence chain and omitted most of this proof.'),
 dict(page=263,source_id='ASTRA-III-AUTHOR-NOTES-263 and full exchange property',decision='Restore the one-point-topos proof continuation, precise locally extended sheaves argument, source D-bounded hypothesis, all four conditions on this folio and every canonical-arrow composition. The two observed numerical calls1,2 retain their complete original texts. The comparison in a-prime retains its arrowhead and the comparison in b-prime is headless, exactly as separately inspected in the source.'),
 dict(page=264,source_id='complete exchange conclusion and Lemma5.3.1',decision='Restore c), the exact a↔a-prime↔b↔c←b-prime chain, historical properness/pseudo-coherence/conjecture provisos and the complete proof. Preserve the actual a↔c target, all lemma hypotheses and the numbered display5.3.1.1 with its trailing comma wholly before the folio boundary.'),
 dict(page=265,source_id='complete affine and dual comparison proof',decision='Restore both canonical arrows defining5.3.1.1, the complete A/A-prime sheaf identification argument and separate square-zero-algebra D_A(N) construction with exact printed EGA O_IV18.2.3. Restore the local strictly pseudo-coherent step before truncation, the full I7.1.2 comparison and the final starred arrow with its stop. Do not replace the printed EGA chapter letter O by a zero.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected source variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==5,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';ids={v['id'] for v in variants};rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id'] not in ids]+variants;rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 261<=x['page']<=265];path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_261_265.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('263\t')]
for label,place,body in [('1','After first Qcoh(Y) in condition(a)','Complete category definition with underlined O_Y.'),('2','After second Qcoh(Y) in condition(a)','Complete reference by(3.7).')]:
 notes.append(f'263\t{place}\traised numerical{label} inside baseline parentheses\t{label}\tASTRA-III-AUTHOR-NOTES-263\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{{{label}}}\t{body}')
path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),math_units=unit_count,lexical_pair_records=0,transfer_rows=len(ledger),stable_targets=len(ot))))
