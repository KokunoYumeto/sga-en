#!/usr/bin/env python3
"""Register the Stein derived-category proof and the analytic finiteness opening."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P180_184.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
lemma=native.index(r'\sgaStableTarget{sga6.e02.lem.2-4-3}')
a=native.index(r'\item Put $A=',lemma)
b=native.index('shrinking around $s$',a)
path=HERE/'EN_TRANSLATION_PATCHES.jsonl'
records=[json.loads(x) for x in path.read_text().splitlines()]
relocated=next(x for x in records if x['id']=='EN-EXPOSE-II-NOTES179')
old=native[a:b]
assert old.count(relocated['old'])==1
old=old.replace(relocated['old'],'',1)
record=dict(id='EN-EXPOSE-II-180-184',page='180–184',
 place='Lemma2.4.3(c) through the opening proof of Lemma2.4.8.1',layer='both',
 old=old,new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer and coordinator',
 source='build/page_packets/180–184/current.tex and diplomatic.tex; review/middle/patches.jsonl; review/expose_ii/patches.jsonl',
 reason='Restores the complete factorization and proof, original D-plus targets, every literal double-underlined R, exact source category letters and arrow labels, all three original numerical author notes, the analytic citation and plain prime-ideal notation. Removes only the unprinted inherited continuation heading while preserving its stable target and source macro state. The old anchor explicitly follows the already accepted removal of the relocated179 note paragraph.')
hits=[i for i,x in enumerate(records) if x['id']==record['id']]
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

variants=[]
def add(number,page,old,printed,source,reason,mode='math',region=''):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,
  source=source,reason=reason,
  scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<184 else None,
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',
  scan_region=region))
add(127,181,r'\underline{\underline{R}}\Gamma_S:\mathrm D^b(S)_{\coh}\longrightarrow\mathrm D^+(A)',
 r'\underline{\underline{R}}\Gamma_S=\mathrm D^b(S)_{\coh}\longrightarrow\mathrm D^+(A)',
 'check/findings/findings_181_185.json#5; fixes/REPLAY_MANUAL_6.json#4',
 'The printed equals sign separates a functor name from its domain. The preceding sentence defines R Gamma_S:D^+(S)→D^+(A); compose it with the inclusion D^b(S)_coh→D^+(S) to obtain the displayed restriction. Current uses a colon for that same functor. Both readings retain the two directly observed horizontal rules below R.',
 region='Proposition2.4.5(a), final displayed functor')
add(128,182,r'i\notin[m,n]',r'i\in[m,n]',
 'check/findings/findings_181_185.json#10; fixes/MISPRINTS_6.json#171',
 'The proof chooses E^i=0 for i>n on 182 and then truncates below m on 183. The map to the truncation preserves cohomology because the stated perfect amplitude gives vanishing below m. The resulting representative therefore vanishes outside [m,n]. Current restores notin; diplomatic preserves the printed membership.',
 region='Proposition2.4.5(b), vanishing condition')
add(129,183,r'E^m\in\Ob\Loclib(S)',r'E^m\in\Ob\Loclib(S))',
 'check/findings/findings_181_185.json#11; fixes/MISPRINTS_6.json#172',
 'The category expression Loclib(S) already has its matching close. Current removes the additional unmatched parenthesis after it; diplomatic retains that extra close. The object and membership are unchanged.',
 region='First proof sentence')
add(130,183,r'\mathrm K^b(\Loclib(S))\to\mathrm D(A)',r'\mathrm K^b(\Loclib(S))\to\mathrm D(S)',
 'check/findings/findings_181_185.json#12',
 'The preceding functor j:K^b(Loclib(S))→D(S) is retained. The second functor is explicitly induced by Gamma_S: degreewise sections define T:K^b(Loclib(S))→K^b(Mod(A))→D(A). Theorem B makes each locally free coherent term acyclic, so the canonical comparison from T to R Gamma_S composed with j is an isomorphism. Current therefore restores the A-module target of this second functor; diplomatic retains S.',
 region='Proof(c), second functor induced by global sections')
add(131,183,r'\mathrm D(A)_{\parf}',r'\mathrm D(S)_{\parf}',
 'check/findings/findings_181_185.json#13',
 'This last image clause belongs to T=Gamma_S on bounded locally free complexes. Under the canonical comparison from T to R Gamma_S composed with j, Proposition 2.4.5(c) on 182 identifies its image with D(A)_parf. The earlier D(S)_parf is the image of j and remains unchanged. Current restores A only in this final image clause.',
 region='Proof(c), last essential-image clause')
add(132,184,'J. Frisch [5]','J. Frish [5]',
 'check/findings/findings_181_185.json#16; directly identified bibliography item[5] on220',
 'The author note expressly cites item[5], whose directly inspected bibliography entry spells the surname Frisch and identifies the same analytic-functions paper. Current supplies the missing c in that attribution; diplomatic preserves Frish. The complete Grothendieck attribution and independent-discovery statement remain in both forms.',
 mode='text',region='First numerical author note to Proposition2.4.8')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(184)
diplomatic,dref=load_reviewed_pages(184,'diplomatic')
ledger=[]
for name in ['review/middle/patches.jsonl','review/expose_ii/patches.jsonl']:
 for raw in (ROOT/name).read_text().splitlines():
  if not raw.strip():continue
  p=json.loads(raw)
  if not 180<=p['page']<=184:continue
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
   decision='transferred in faithful English; mathematical, punctuation and attribution variants explicitly branched',
   patch_source=name,patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),
   source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(180,185):
  counts={}
  for token in [r'\underline{C}',r'\underline{O}',r'\underline{\underline{R}}',
                r'\underline{\operatorname{Hom}}',r'\phi',r'\varnothing',
                r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}',r'\xrightarrow{(*)}',r'\xrightarrow{(**)}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts))
ledger.extend([
 dict(page=180,source_id='ASTRA-II-NOTE-180',decision='Restore the full original numerical1 author note at the Lib/Loclib alternative, with I2.15.1. This is independent of the already removed duplicate179 note paragraph.'),
 dict(page=180,source_id='reviewed proof of2.4.3',decision='Restore the exact reference2.1.2(b)(ii), full Hom underline, all five category C rules, complete starred-arrow factorization and concluding assertion. The original item(c) boundary is before the item command; the visible folio label follows that command for valid list rendering.'),
 dict(page=181,source_id='reviewed proof and Proposition2.4.5(a)',decision='Preserve plain A/B, closed phi, inline coeffaceability formula, unstopped underlined Proof label, exact I3.5(b) citation, both literal double-underlined R letters, and original D-plus source and targets. The inherited D-b replacements are not retained.'),
 dict(page=182,source_id='ASTRA-II-R-182; reviewed Proposition2.4.5',decision='Preserve all three literal double-underlined R letters, the source D-plus targets, unbounded D(A)_parf image and exact I4.8/I4.9 references, including the inline I4.9 inside its original display.'),
 dict(page=183,source_id='check/findings/findings_181_185.json#14/#15; ASTRA-II-UNDERLINE-183',decision='Keep all three definition paragraphs, every observed word rule and the independently plain Stein. Preserve the source continuation macros, including lowercase ob. Remove the unprinted inherited continuation heading while retaining its stable link target immediately before184.'),
 dict(page=184,source_id='ASTRA-II-NOTE-184',decision='Restore both complete numerical notes with separate1/2 calls: the Grothendieck/Frisch attribution and the local Analytic Geometry admission. Keep the original heading punctuation and both note bodies outside the statement underline.'),
 dict(page=184,source_id='check/findings/findings_181_185.json#17',decision='English unchanged: French tel already introduces the displayed defining property; supplying the omitted que repairs its conjunction. Both English forms render that same relation as such that, with identical integer, equality and bound. No invented English grammatical error is introduced.'),
 dict(page=184,source_id='ASTRA-II-R-184; check/findings/findings_181_185.json#18/#19',decision='Keep the literal two lower rules on the real-coordinate R, baseline filtration dots, plain p_i, exact local-ring indices and inline quotient; restore the omitted Bourbaki locator. The French boundary splits loca/liser, represented by the English boundary after/localizing.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_180_184.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [180,184])]
notes.extend([
 '180\tAfter the Lib/Loclib proof alternative\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-180\tearly reviewer direct scan comparison, main PDF194\tSGAAuthorFootnote{1}\tComplete original stability note and I2.15.1 reference.',
 '184\tProposition2.4.8 title\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-184\tearly reviewer direct scan comparison, main PDF198\tSGAAuthorFootnote{1}\tComplete Grothendieck attribution and independent Frish/Frisch statement.',
 '184\tAfter local connectedness\traised numerical2 inside baseline parentheses\t1\tASTRA-II-NOTE-184\tearly reviewer direct scan comparison, main PDF198\tSGAAuthorFootnote{2}\tComplete original local Analytic Geometry admission and reference10.'
])
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
