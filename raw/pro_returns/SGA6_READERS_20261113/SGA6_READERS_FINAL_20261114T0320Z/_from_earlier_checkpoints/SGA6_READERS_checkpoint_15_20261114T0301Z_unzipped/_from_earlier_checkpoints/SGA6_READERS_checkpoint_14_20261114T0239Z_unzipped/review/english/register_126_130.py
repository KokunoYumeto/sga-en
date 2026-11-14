#!/usr/bin/env python3
"""Record faithful 126–130 reconstruction and four explicit source variants."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P126_130.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e01.rem.4-12-2}')
b=native.index('in the case of the category of modules of a ringed topos',native.index(r'\sgaStableTarget{sga6.e01.para.5-0}',a))
record=dict(id='EN-EXPOSE-I-126-130',page='126–130',place='Exposé I4.12.2 through the beginning of5.0',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/126–130/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the empty-set superscripts for acyclic categories, literal + sums, exact site and left-module category expressions, local perfect-amplitude/dimension operator rules, separately plain final-object S-prime in4.19, and double-struck Lf* with plain tensor L. Four inherited source variants are branched with exact morphism and hypothesis reasons; all literal formulas and existing stable targets are preserved.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(130)
diplomatic,dref=load_reviewed_pages(130,'diplomatic')
en=split(chunk)
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 101<=int(x['id'].rsplit('-',1)[1])<=104]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text'):
 assert en[page].count(corrected)==1,(number,en[page].count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(101,126,r'\(\Kpx^b(\underline{C}_0)\longrightarrow \Dpx(\underline{C})\)',r'\(\Kpx^b(C_0)\longrightarrow \Dpx(\underline{C})\)',
 'fixes/MISPRINTS_6.json#147; check/findings/findings_126_130.json#3',
 'The first inline source category lacks the C rule in both scans. The full embedding i:C_0→C specified in the preceding sentence induces K^b(i), followed by localization into D(C). Its source is precisely the named C_0 with its independent rule. Current supplies this one omitted rule; diplomatic retains the plain C.', 'Remark4.12.2, first inline functor')
quotient=[m.group(0) for m in MATH.finditer(current[126]) if r'\longrightarrow'+'\n  '+r'\Kpx^-(' in m.group(0)]
assert len(quotient)==1
inner=quotient[0][2:-2]
printed=inner.replace(r'\Kpx^b(\underline{C}_0)/',r'\Kpx^b(\underline{C}_0)',1)
variant(102,126,inner,printed,
 'fixes/MISPRINTS_6.json#148; check/findings/findings_126_130.json#9',
 'Both scans omit the source quotient slash. The inclusion of bounded complexes into bounded-above complexes sends bounded acyclic complexes to bounded-above acyclic complexes. Composing with localization therefore factors through the bounded quotient K^b(C_0)/K^{b,emptyset}(C_0), which is already displayed earlier in the remark. Current restores that one slash; diplomatic retains the adjacent expressions.', 'Remark4.12.2, final comparison functor','math')
variant(103,129,r'\(\perfamp(F)\subset[a,b]\)',r'\(\perfdim(F)\subset[a,b]\)',
 'fixes/MISPRINTS_6.json#149; check/findings/findings_126_130.json#22',
 'Here F=F-prime+F-double-prime. Hypothesis4.17(ii) gives the stated perfect-amplitude inclusion, and the preceding truncations put its terms in C_0 above a. Lemma4.16 applies with exactly that amplitude hypothesis and gives F^a locally in C_0. Current writes parf.amp; diplomatic retains the printed parf.dim.', 'continuation of proof4.17, first line')
variant(104,129,r"\(\Dpx^*(\underline{C}')\) (4.10).",r'\(\Dpx^*(\underline{C})\) (4.10).',
 'fixes/MISPRINTS_6.json#150; check/findings/findings_126_130.json#29',
 'The displayed perfect subcategory is defined for C-prime. Definition4.9 supplies the full inclusion j:D*(C-prime)_parf→D*(C-prime), the identity on its objects and arrows, and4.10 applied to the primed triple gives its triangulated structure. Current adds the omitted prime to this ambient category; diplomatic retains the printed unprimed letter.', 'proof4.18, final ambient category')
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=130]
units=[m.group(0) for m in MATH.finditer(current[130]) if r'\text{et}' in m.group(0)]
assert len(units)==1
translated=units[0].replace(r'\text{et}',r'\text{and}')
assert en[130].count(translated)==1
pairs.append(dict(page=130,layer='both',French_literal_unit=units[0],English_literal_unit=translated,expected_multiplicity=1,
 status='confirmed exact lexical translation of et to and; mathematical characters, commands and delimiters retained',
 scope='Only this complete displayed unit and exact multiplicity are approved.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 126<=p['page']<=130 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(126,131):
 counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\underline{\perfamp}',r'\underline{\perfdim}',r'\mathbb L',r'\mathrm L',r'\varnothing',r'\ldots'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
ledger.extend([
 dict(page=126,source_id='reviewed source4.12.2',decision='empty-set superscripts of all acyclic subcategories and the terminal prime in the [V] criterion are retained literally; quasi-liftable has its observed word underline'),
 dict(page=127,source_id='ASTRA-I-OPRULE-127',decision='only parf.amp in4.14(i) and the second parf.dim in4.14.1 have the source operator rules; the defined phrase perfect dimension is plain'),
 dict(page=128,source_id='ASTRA-I-OPRULE-128',decision='only the first parf.amp in Lemma4.16 has an operator rule; the later amplitude expressions remain as printed'),
 dict(page=128,source_id='reviewed source4.17',decision='all displayed and inline direct-sum expressions retain the source + symbol; no oplus is substituted. The connective and in item(i) and i.e. in the parenthetical explanation are plain.'),
 dict(page=129,source_id='ASTRA-I-SITE-129',decision='the two final-object S-prime occurrences in proof4.19 remain plain; the topos names, maps and all other inspected site occurrences retain their individual rules'),
 dict(page=129,source_id='reviewed source4.18 and4.19',decision='empty-set choice of star, exact left/right A-module indices and all source and target categories restored from the French packet'),
 dict(page=130,source_id='ASTRA-I-SITE-130; ASTRA-I-TERMS-130',decision='all twelve inspected site rules including both fiber-product bases retained; the three derived inverse-image L letters are double-struck and each tensor superscript L remains plain'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_126_130.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
