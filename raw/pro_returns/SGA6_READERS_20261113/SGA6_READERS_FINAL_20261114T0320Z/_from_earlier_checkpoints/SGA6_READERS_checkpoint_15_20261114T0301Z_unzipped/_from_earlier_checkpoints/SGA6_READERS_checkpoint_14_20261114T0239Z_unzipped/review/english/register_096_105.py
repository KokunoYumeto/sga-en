#!/usr/bin/env python3
"""Register the manually compared ten-page pseudo-coherence passage."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
files=['EN_EXPOSE_I_P096_100.tex','EN_EXPOSE_I_P101_105.tex']
chunk=''.join((HERE/f).read_text() for f in files)
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e01.prop.2-2}')
end_anchor=r"so \(\Ho^n(F'_{\leq n})\) (respectively \(\Ho^n(F''_{\leq n})\)) is of finite type"
b=native.index(end_anchor,a)
record=dict(id='EN-EXPOSE-I-096-105',page='96–105',place='Exposé I2.2–2.12, pseudo-coherence and finite presentation',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/96–105/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation preserves all displayed and inline formulas, source paragraph divisions, plain item labels, exact underlined word groups, independently underlined n and category/site symbols, the acyclic-subcategory empty-set superscript, and the literal plus signs and unbounded derived-category notation in2.12. Current variants explicitly carry the missing proposition stop100, negative degree103, qualified conclusion104 and zero bound104. The native list around2.7 is reconstructed together with its continuation to keep the source structure balanced.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(105)
diplomatic,dref=load_reviewed_pages(105,'diplomatic')
en=split(chunk)
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 84<=int(x['id'].rsplit('-',1)[1])<=87]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text',scope_start=None,scope_end=None):
 body=en[page]
 if scope_start:body=body[body.index(scope_start):]
 if scope_end:body=body[:body.index(scope_end)]
 assert body.count(corrected)==1,(number,body.count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=scope_start or f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=scope_end or f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(84,100,r'\textbf{Proposition 2.7.}',r'\textbf{Proposition 2.7}',
 'check/findings/findings_096_100.json#19',
 'The scan has a blank after the final7 before the statement. Diplomatic preserves that missing stop; current retains the restored heading punctuation.', 'Proposition2.7 label')
variant(85,103,'(-n)','n','ASTRA-I-SIGN-103',
 'Assertion2.9(ii) specifies (-n)-pseudo-coherence. Apply2.4 to the map0→F with pseudo-coherence parameter -n and quasi-isomorphism parameter1: the replacement E→F is strictly(-n)-pseudo-coherent, and0→E is the identity in degrees≥1. Thus E vanishes there and its components in degrees -n through0 supply exactly the n-presentation defined in2.8. Current supplies the missing minus sign.', 'proof2.9, strict degree of the replacement','math')
conclusion=r'\(F\) \uline{is} \(n\)\uline{-pseudo-coherent (resp.\ pseudo-coherent).}'
variant(86,104,conclusion,r'\(F\) \uline{is pseudo-coherent.}',
 'check/findings/findings_101_105.json#20; review/expose_i/decisions.jsonl',
 "The proof on105 concludes n-pseudo-coherence. Its induction uses H^i(F')=H^(i+1)(F), and the presentation index i+1-n equals i-(n-1). The printed unqualified conclusion fails on the punctual site of vector spaces: take n=0, an infinite-dimensional vector space M, and F=M[1]. All H^i(F) for i≥0 vanish and meet the stated finite-presentation assumptions, while H^(-1)(F)=M is not of finite type. Proposition2.10(b) therefore rules out (-1)-pseudo-coherence. Current restores the n-qualified conclusion and the parenthetical alternative proved by the argument.",
 'Proposition2.11(b) conclusion',scope_start=r'b) \uline{Let} \(F\in\Ob\Dpx^-(\underline{C}_S)\)\uline{. When, for every}',scope_end=r'\uline{Proof.}')
variant(87,104,'F^i=0',r'F^i\neq0',
 'check/findings/findings_101_105.json#21; review/expose_i/decisions.jsonl',
 'The given complex belongs to the bounded-above category C-minus. The displayed exact sequence removes its highest component F^(n+N), leaving F-prime zero above n+N-1. The induction therefore starts with F^i=0 for i>n+N, replacing the printed nonzero relation.', 'proof2.11(a), induction bound','math')
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))

path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page'] not in [96,104]]
for page in [96,104]:
 for unit in [m.group(0) for m in MATH.finditer(current[page]) if r'\text{pour' in m.group(0)]:
  translated=unit.replace(r'\text{pour tout }',r'\text{for every }').replace(r'\text{pour }',r'\text{for }')
  assert en[page].count(translated)==1,(page,translated)
  pairs.append(dict(page=page,layer='both',French_literal_unit=unit,English_literal_unit=translated,expected_multiplicity=1,
   status='confirmed exact lexical translation inside displayed formula; every mathematical token retained',
   scope='Only this complete literal pair and exact occurrence multiplicity are approved; no page-wide exception.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')

ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 96<=p['page']<=105 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is also explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(96,106):
 counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\underline{O}',r'\underline{n}',r'\underline n',r'\varnothing'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
ledger.extend([
 dict(page=97,source_id='main scan PDF111 top; direct English reviewer view',decision='proof paragraph continues from96; next item b has a separate observed indent'),
 dict(page=98,source_id='check/findings/findings_096_100.json#4',decision='first defined n independently underlined; the n-C0-pseudo-coherent term itself remains plain'),
 dict(page=100,source_id='reviewed French Proposition2.7(b)',decision='retain literal empty-set superscript in all three acyclic-subcategory expressions; inherited English ac notation removed'),
 dict(page=102,source_id='ASTRA-I-DEFINEDN-102',decision='first defined n independently underlined; finite-presentation term words remain plain'),
 dict(page=103,source_id='reviewed French additional macro block',decision='all fourteen supplied providecommand declarations retained at this location; existing macro meanings remain protected by providecommand'),
 dict(page=105,source_id='reviewed French Proposition2.12 and proof',decision='retain D(C_S) without an added minus and every literal direct-sum plus sign; no replacement by an oplus glyph'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_096_105.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
target_pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(target_pattern,record['old']))
new_targets=set(re.findall(target_pattern,chunk))
assert old_targets
assert old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
