#!/usr/bin/env python3
"""Record the faithful 111–115 passage and two English source variants."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P111_115.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('be the derived functor of the tensor product',native.index(r'\sgaStableTarget{sga6.e01.cor.2-16}'))
b=native.index('In particular, for \\(F\\) to be pseudo-coherent',native.index(r'\sgaStableTarget{sga6.e01.cor.3-5}',a))
record=dict(id='EN-EXPOSE-I-111-115',page='111–115',place='Exposé I2.16 continuation and coherence3.1–3.5',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/111–115/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the tensor base f^(-1)(A), left A-prime derived-category object, double-struck derived L, derived tensor in Exercise2.16.2, original author note112, plain defined terms, every complete diagram including the observed broken v-arrow115, and the original split formula3.5. Current site-map and heading punctuation changes are explicitly branched; two French grammatical/spelling changes leave the English wording unchanged.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(115)
diplomatic,dref=load_reviewed_pages(115,'diplomatic')
en=split(chunk)
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 93<=int(x['id'].rsplit('-',1)[1])<=94]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text'):
 assert en[page].count(corrected)==1,(number,en[page].count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(93,111,r"X'=f^{-1}(X)",r"X'=u(X)",
 'check/findings/findings_111_115.json#5; review/expose_i/decisions.jsonl',
 "The site-object inverse-image functor f^(-1):S→S' is explicitly defined on110. The proof on111 applies that same map to U, writing U'=f^(-1)(U). The letter u in that proof denotes the derived tensor functor on complexes. Current applies the specified site map to X, giving X'=f^(-1)(X).", 'Corollary2.16, base object X-prime','math')
variant(94,112,r'\textbf{Lemma 3.3.}',r'\textbf{Lemma 3.3}',
 'check/findings/findings_111_115.json#17',
 'The printed heading ends after the numeral3. Diplomatic keeps the missing terminal stop; current supplies the heading punctuation.', 'Lemma3.3 heading')
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))

path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=115]
unit=[m.group(0) for m in MATH.finditer(current[115]) if r'\begin{split}' in m.group(0)]
assert len(unit)==1
translated=unit[0].replace('pseudo-cohérent','pseudo-coherent').replace('cohérent pour','coherent for').replace(r'\uline{et}',r'\uline{and}').replace('de type fini','of finite type')
assert en[115].count(translated)==1
pairs.append(dict(page=115,layer='both',French_literal_unit=unit[0],English_literal_unit=translated,expected_multiplicity=1,
 status='confirmed exact lexical translation of the four independently underlined formula-text phrases; all mathematical tokens and wrapper boundaries retained',
 scope='Only this complete displayed pair and its exact multiplicity are approved.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')

ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 111<=p['page']<=115 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  decision='transferred in faithful English; printed/current differences are separately classified below'
  if p['source_id']=='ASTRA-I-MODULEPLURAL-111':decision='English unchanged: a complex of left A_U-Modules; no English variant'
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(111,116):
 counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\mathbb{L}',r'\mathrm L'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
ledger.extend([
 dict(page=111,source_id='ASTRA-I-MODULEPLURAL-111',decision='English unchanged; no variant',French_printed='un complexe de A_U-Module à gauche',French_corrected='un complexe de A_U-Modules à gauche',English_both='a complex of left A_U-Modules',reason='The complex already consists degreewise of the displayed modules E^i with its differentials. The identity on each E^i and differential identifies the same complex before and after the French ending repair. The natural English translation names those module terms in both forms; the coordinator confirmed this classification.'),
 dict(page=112,source_id='check/findings/findings_111_115.json#13',decision='English unchanged; no invented English misspelling',French_printed='pseudo-oohérent',French_corrected='pseudo-cohérent',English_both='pseudo-coherent',reason='Both French strings designate the defined notion in2.3 and the correctly spelt second occurrence in the same exercise sentence. Its English rendering is pseudo-coherent in both forms; coordinator confirmed the unchanged-English classification.'),
 dict(page=112,source_id='ASTRA-I-NOTE-112',decision='original parenthesized-star author note restored outside the definition underlining',English_anchor=r'\SGAAuthorFootnote{*}{We introduce this notion'),
 dict(page=112,source_id='reviewed French Definition3.1',decision='first defined precoherent and coherent remain plain; later statement occurrences retain their inspected word-group underlining'),
 dict(page=115,source_id='reviewed French proof3.3(c)',decision='literal dashed v-arrow retained in both forms, with exact endpoint, label and full commutative diagram'),
 dict(page=115,source_id='en/glossaries/GLOSSARY_SGA4_FR_EN.tsv; en/glossaries/GLOSSARY_SGA5_INCONSISTENCIES.md',decision='finite projective and inductive limits chosen in this local passage',reason='These literal renderings are attested in the supplied SGA4 and SGA5 records and preserve the French limit terminology. Other cross-volume renderings remain listed in the candidate inventory; no global divergence claim is inferred from their counts.'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_111_115.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('112\t')]
notes.append('112\tDefinition3.1 after relative to C_0\tbaseline parenthesized star\t1\tASTRA-I-NOTE-112\tcoordinator direct scan comparison, main PDF126 and witness123\tSGAAuthorFootnote{*}\tRetain the full author note outside the underlined definition words.')
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
