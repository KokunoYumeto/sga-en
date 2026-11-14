#!/usr/bin/env python3
"""Record the 136–140 translation, retained Hom_Z shorthand and reference repair."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P136_140.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('Here is now a particular case of',native.index(r'\sgaStableTarget{sga6.e01.lem.5-8-2}'))
b=native.index(r'\sgaStableTarget{sga6.e01.para.6-2}',a)
record=dict(id='EN-EXPOSE-I-136-140',page='136–140',place='Exposé I5.8.3 through Definition6.1',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/136–140/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the literal internal Hom_Z shorthand and source functor-slot points, complete tensor–Hom comparison and truncation diagrams, underlined parf subscripts, exact aligned identities, plain final-object S, both primes in the stalk-projector identity, all six plain category C occurrences140, the dashed unlabeled triangle arrow and plain additive-function definition. The reference3.17.1→5.8.2.1 is branched with its explicit evaluation map; no Hom_Z variant is introduced after the documented restriction-compatible identity.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(140)
diplomatic,dref=load_reviewed_pages(140,'diplomatic')
en=split(chunk)
assert en[136].count('(5.8.2.1)')==1
new=dict(id='EN-VAR-106',page=136,old='(5.8.2.1)',printed='(3.17.1)',corrected='(5.8.2.1)',mode='text',
 source='ASTRA-I-REF-136; review/expose_i/own_findings.jsonl; review/expose_i/add_136_140.py',
 reason='Formula 5.8.2.1 specializes at B=Z_S and G=I to the displayed vertical map Hom_ZS(F,I) tensor_A E→Hom_ZS(Hom_A(E,F),I), sending h tensor e to (t↦h(t(e))). Replacing F by F-double-prime gives the other vertical map. The next sentence invokes Lemma 5.8.2 for invertibility. Current gives this actual formula reference; diplomatic preserves the printed 3.17.1.',
 scope_start='%%%%%%%%%%  scan idx 149  |  folio 136',scope_end='%%%%%%%%%%  scan idx 150  |  folio 137',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=150; scan/SGA6_witness_300dpi.djvu#page=147',scan_region='Proof 5.8.3, before the commutative Hom diagram')
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if x['id']!=new['id']];variants.append(new)
variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=138]
units=[m.group(0) for m in MATH.finditer(current[138]) if r'\text{\uline{et}}' in m.group(0)]
assert len(units)==1
translated=units[0].replace(r'\text{\uline{et}}',r'\text{\uline{and}}')
assert en[138].count(translated)==1
pairs.append(dict(page=138,layer='both',French_literal_unit=units[0],English_literal_unit=translated,expected_multiplicity=1,
 status='confirmed exact lexical translation of the independently underlined et to and; all mathematical characters, alignment cells and wrappers retained',
 scope='Only this complete displayed unit and exact multiplicity are approved.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 136<=p['page']<=140 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  decision='transferred in faithful English; every printed/current difference is explicitly branched'
  if p['source_id']=='ASTRA-I-HOMZ-136':decision='printed Hom_Z retained in both forms; supplied current added S was reverted by coordinator; no English variant'
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(136,141):
 counts={}
 for command in (r'\underline{S}',r'\underline{O}',r'\underline{C}',r'\underline{\Hom}',r'\underline{\mathrm{parf}}',r'\mathbb Z_S',r'\operatorname{parf.amp}'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
ledger.append(dict(page=136,source_id=new['source'],decision='explicit English printed/corrected variant',English_variant=new['id'],printed=new['printed'],corrected=new['corrected']))
hom_audit=dict(page=136,source_id='ASTRA-I-HOMZ-136',decision='source Hom_Z shorthand retained in both forms',
 source_literal=r'\(\underline{\Hom}_{\mathbb Z}(.,I)\)',
 identity='For each site object U, an additive sheaf map M|U→I|U commutes with integer repeated addition, hence with locally constant integer sections by gluing. A Z_S-linear map is additive. The identity on these maps in both directions identifies the internal Hom_Z and Hom_ZS sheaves, compatibly with restriction to each further site object. The printed shorthand already gives the required sheaf.',
 basis='Exact coordinator source and mathematical decision, review/expose_i/own_findings.jsonl; no unsupported notation normalization.')
ledger.extend([
 hom_audit,
 dict(page=136,source_id='ASTRA-I-REF-136',decision='evaluation morphism behind the reference correction is explicit',formula='h tensor e ↦ (t ↦ h(t(e))), with B=Z_S and G=I in5.8.2.1; repeat with F-double-prime for the second vertical arrow'),
 dict(page=137,source_id='reviewed source proof5.8 and Remark5.8.4',decision='no leading ellipsis is added to either truncation row; exact triangular orientation and comma cell are retained; underlined parf subscripts are independent of the plain ones'),
 dict(page=138,source_id='ASTRA-I-SITE-138; ASTRA-I-TERMS-138',decision='both final-object S occurrences in the proof are plain; all inspected topos rules and the underlined and within the aligned identities are preserved'),
 dict(page=138,source_id='reviewed source Corollary5.9 prose',decision='the second resp. condition names bounded cohomology and pseudo-coherence of E; native wording incorrectly attached pseudo-coherent directly to cohomology'),
 dict(page=139,source_id='reviewed source Lemma5.10.1 proof',decision='both occurrences of the primed stalk projector in (p-prime_s)^2=p-prime_s retained exactly; the native unprimed notation is repaired in both English forms'),
 dict(page=138,source_id='ASTRA-I-PROOFSTOP-138; ASTRA-I-PROOFSTOP-139',decision='the three inspected proof-label full stops are outside the word rules; no full stop is added to Corollary5.10 heading'),
 dict(page=140,source_id='ASTRA-I-C-140; ASTRA-I-O-140; ASTRA-I-TERMS-140',decision='all six category C letters are plain; all three structure O letters have their rules; rank alone is ruled and the defined additive-function phrase is plain'),
 dict(page=140,source_id='reviewed source Definition6.1 diagram',decision='dashed unlabeled L-double-prime-to-L-prime arrow, source + sign and all endpoint formulas retained literally'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_136_140.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_INDEPENDENT_SOURCE_ASSESSMENTS.jsonl';assessments=[json.loads(x) for x in path.read_text().splitlines()]
assessments=[x for x in assessments if x.get('page')!=136]
hom_audit['status']='coordinator proof recorded in English transfer audit; source glyph confirmed by coordinator'
assessments.append(hom_audit)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in assessments))
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[new['id']],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
