#!/usr/bin/env python3
"""Register the faithfully compared 121–125 passage and exact source variants."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P121_125.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'if \(F\) is strictly perfect',native.index(r'\sgaStableTarget{sga6.e01.schol.4-4}'))
b=native.index(r'\sgaStableTarget{sga6.e01.rem.4-12-2}',a)
record=dict(id='EN-EXPOSE-I-121-125',page='121–125',place='Exposé I4.4 continuation through4.12.1 and its macro-state continuation',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/121–125/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the literal inductive-limit arrow and nonunderlined Hom in the formula4.6, the underlined M category and slice-site notation, the plain defined perfect-amplitude phrases, full author note122, local Parf operator rules and separate resp. spans, exact triangular diagrams and degree labels, source operator abbreviations and complete125 macro state. Three inherited punctuation repairs and the current missing site rule are individually branched. The native added continued-exposé heading is removed while its stable target is retained.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(125)
diplomatic,dref=load_reviewed_pages(125,'diplomatic')
en=split(chunk)
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 97<=int(x['id'].rsplit('-',1)[1])<=100]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text'):
 assert en[page].count(corrected)==1,(number,en[page].count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(97,123,r'\textbf{Proposition 4.10.}',r'\textbf{Proposition 4.10}',
 'fixes/MISPRINTS_6.json#144; check/findings/findings_121_125.json#22',
 'The main scan has a space after the numeral before the statement, with no terminal full stop. Diplomatic retains that absence; current supplies the heading punctuation.', 'Proposition4.10 heading')
variant(98,123,r'\(X\in\Ob \underline{S}\)',r'\(X\in\Ob S\)',
 'ASTRA-I-SITE-MISSING-123; review/expose_i/decisions.jsonl',
 'The printed membership leaves S without a rule. The quantified X indexes the fibers C_{0X}, and the fiber projection C_0→the base site sends their objects to X. Paragraph4.0 names that base site with underlined S; the proof124 repeats X∈ob underlined S for the same triangle fibers. Current supplies the missing site rule; diplomatic retains the observed plain letter.', 'Proposition4.10(i), quantified base object')
variant(99,123,r'\(\Tr(\Dpx(\underline{C}))\)) \uline{to an object of}',r'\(\Tr(\Dpx(\underline{C}))\) \uline{to an object of}',
 'fixes/MISPRINTS_6.json#145; check/findings/findings_121_125.json#34',
 'The middle resp. parenthesis has an opening before the category expression and no outside closer in print. Current adds that single outside parenthesis; the inner category parentheses and all mathematical tokens are unchanged.', 'Proposition4.10(ii), middle resp. clause')
variant(100,123,r'\uline{(resp.}\ \(\Tr(\Kpx^b(\underline{C}_0))\)).',r'\uline{(resp.}\ \(\Tr(\Kpx^b(\underline{C}_0))\).',
 'fixes/MISPRINTS_6.json#146; check/findings/findings_121_125.json#35',
 'The final resp. clause independently lacks its outside closing parenthesis. The two inner category parentheses are present. Current supplies only the missing outer closer; diplomatic retains its omission.', 'Proposition4.10(ii), final resp. clause')
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=124]
units=[m.group(0) for m in MATH.finditer(current[124]) if r'\text{ ou }' in m.group(0)]
assert len(units)==1
translated=units[0].replace(r'\text{ ou }',r'\text{ or }')
assert en[124].count(translated)==1
pairs.append(dict(page=124,layer='both',French_literal_unit=units[0],English_literal_unit=translated,expected_multiplicity=1,
 status='confirmed exact lexical translation of ou to or; every surrounding mathematical character and delimiter retained',
 scope='Only this complete literal unit and exact multiplicity are approved.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 121<=p['page']<=125 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(121,126):
 counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\underline{M}',r'\underline{\Hom}',r'\underline{\Parf}',r'\underline{\Qis/F}',r'\varinjlim',r'\xrightarrow[+1]'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
commands=lambda s:re.findall(r'\\(?:providecommand|renewcommand)\{[^\n]+',s)
assert commands(current[125])==commands(en[125])
ledger.extend([
 dict(page=121,source_id='ASTRA-I-DOT-121; reviewed proof4.6',decision='literal baseline point, rightward inductive-limit arrow and two plain Hom operators restored exactly in the displayed localization formula'),
 dict(page=121,source_id='ASTRA-I-M-121; ASTRA-I-TERMS-121',decision='all M category rules and independently plain defined perfect-amplitude phrase preserved'),
 dict(page=122,source_id='ASTRA-I-NOTE-122',decision='full original notation-suppression note restored with raisedstar outside the statement underlining'),
 dict(page=122,source_id='ASTRA-I-TERMS-122',decision='both defined finite-perfect-amplitude and perfect phrases remain plain; source roman abbreviation parf retained literally inside formulas'),
 dict(page=123,source_id='ASTRA-I-PARFRULE-123; ASTRA-I-TERMS-123',decision='exactly two Parf operators have independent rules; first resp. category parenthesis stays plain and later observed resp. word spans stay underlined'),
 dict(page=124,source_id='reviewed source4.10 proof',decision='both triangle degree labels remain +1 below the third arrow, without changing them to shifted endpoint expressions'),
 dict(page=125,source_id='ASTRA-I-TERMS-125',decision='rel. is within the observed word rule; the following to remains plain, corresponding to the source plain à'),
 dict(page=125,source_id='reviewed French macro-state continuation',decision='complete ordered macro block retained exactly',command_count=len(commands(current[125])),commands=commands(current[125]),reason='The actual Ob renewal, underlined Cart definition and literal parf.amp/parf.dim abbreviations are preserved; no operator spelling is translated inside source formulas.'),
 dict(page=125,source_id='English native continuation boundary',decision='removed added continued-exposé heading and retained its stable target without a heading',target='sga6.e01.expose.occ3',reason='The French source continues directly with Remark4.12.2 on126; the native English section heading has no corresponding printed heading.'),
 dict(page=122,source_id='en/glossaries/GLOSSARY_SGA4_FR_EN.tsv; en/glossaries/GLOSSARY_SGA5_FR_EN.tsv; en/glossaries/GLOSSARY_SGA7_FR_EN.tsv',decision='direct factor and finite perfect amplitude used as attested local renderings',reason='The supplied SGA4 and SGA5 records attest direct factor; SGA5 attests finite perfect amplitude; SGA7 also contains direct summand. This records the local paired choice without claiming cross-volume semantic reconciliation.'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_121_125.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('122\t')]
notes.append('122\tDefinition4.7 after finite perfect amplitude\traised star inside baseline parentheses\t1\tASTRA-I-NOTE-122\tcoordinator direct scan comparison, main PDF136 and witness133\tSGAAuthorFootnote{raisedstar}\tFull original note explaining omission of C_0 where unambiguous, outside the underlined statement.')
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
