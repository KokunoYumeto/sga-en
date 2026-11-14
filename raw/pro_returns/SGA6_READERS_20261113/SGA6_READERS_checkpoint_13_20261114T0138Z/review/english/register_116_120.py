#!/usr/bin/env python3
"""Record the faithful 116–120 passage, source variants and proof audit."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P116_120.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'In particular, for \(F\) to be pseudo-coherent',native.index(r'\sgaStableTarget{sga6.e01.cor.3-5}'))
b=native.index(r'if \(F\) is strictly perfect',native.index(r'\sgaStableTarget{sga6.e01.schol.4-4}',a))
record=dict(id='EN-EXPOSE-I-116-120',page='116–120',place='Exposé I3.5 continuation through the beginning of4.4',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/116–120/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the source category in3.7(a), all underlined Hom/H/Ext operators, double-struck derived R and L, literal functor-slot periods, three actual triangles117, both ≥ induction bounds119, the two original author notes including D. Ferrand, the actual direction P_X→E_X of u in4.2, the full category rule on Qis/F, and independently observed plain final-object S and connective and. Two source citation repairs are branched. The proof bound118 is retained in both forms with its exact arbitrary-index justification in the audit ledger.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(120)
diplomatic,dref=load_reviewed_pages(120,'diplomatic')
en=split(chunk)
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 95<=int(x['id'].rsplit('-',1)[1])<=96]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text'):
 assert en[page].count(corrected)==1,(number,en[page].count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(95,118,'(SGA 4 VIII 7.8)','(SGAA VIII 7.8)',
 'ASTRA-I-SGA4-118; review/expose_i/decisions.jsonl; coordinator primary bibliography verification',
 'The printed final A is retained diplomatically. The cited definition of a point belongs to SGA 4, VIII7.8, checked against the primary text by the coordinator; current supplies the volume digit and preserves the cited exposé and paragraph.',
 'Corollary3.7.2, citation after a point of the topos')
variant(96,118,'By (3.7 a)),','By (2.22 a)),',
 'check/findings/findings_116_120.json#22; review/expose_i/decisions.jsonl',
 'The displayed comparison is the degree-zero consequence of the flat point pullback of the derived Hom comparison in3.7(a). The point inverse-image functor is exact, and applying H^0 to that isomorphism gives the two displayed Hom comparisons. Current cites3.7(a); diplomatic retains2.22(a).',
 'proof3.7.2, immediately before the displayed two Hom comparisons')
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))

ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 116<=p['page']<=120 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(116,121):
 counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\underline{O}',r'\mathbb{L}',r'\mathbb{R}',r'\underline{\Hom}',r'\underline{\Ho}',r'\underline{\Ext}',r'\underline{\Qis/F}'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
bound_audit=dict(page=118,source_id='independent exact-sequence proof audit; coordinator assessment',decision='printed comparison bound retained in both English forms; no source correction',
 observation="For a fixed approximation index n, the exact triangle TF''→TF→TF'→TF''[1] and the vanishing of H^j(TF'') and H^j(T'F'') for j≤a−n directly give the middle isomorphism in degrees i≤a−n−1. The printed sentence uses i≤a−n.",
 proof="The next sentence explicitly permits n to be arbitrarily negative. For any fixed degree i choose the approximation index n=a−i−1. Then i and i+1 are both ≤a−n, so both adjacent cohomology terms of TF'' and T'F'' vanish. The isomorphism TF'→T'F' gives H^i(TF)→H^i(T'F) as an isomorphism via the exact sequences. This proves the comparison in each degree and justifies retaining the passage's conclusion without changing the source construction.",
 basis='The English reviewer and coordinator independently checked the displayed triangle and bound; the coordinator confirmed retention of the printed wording.')
ledger.extend([
 dict(page=116,source_id='ASTRA-I-DOT-116',decision='baseline literal period retained in the functor slot in both forms; no raised-dot substitution',English_anchor=r"\(f^*=A'\otimes_A.\)"),
 dict(page=116,source_id='ASTRA-I-NOTE-116',decision='restored the complete original scheme/prescheme terminology note with its baseline parenthesized star'),
 dict(page=116,source_id='ASTRA-I-SITE-116',decision='plain final-object S retained in Dpx(_A S) and Dpx^+(_A S), separately from the underlined topos names'),
 dict(page=117,source_id='ASTRA-I-TERMS-117',decision='connective and between the two individually underlined H operators remains plain; both final-object S symbols in Dpx^± remain plain'),
 dict(page=117,source_id='reviewed source triangles in proof3.7',decision='all three complete triangular diagrams and their +1/−1 arrow labels restored in both forms; no flattened replacement diagram'),
 dict(page=118,source_id='ASTRA-I-SITE-118',decision='plain final-object S in D^b(_A S)_coh retained; source ≃ and isomorphism arrows retained literally rather than replaced by the native English qis macro'),
 bound_audit,
 dict(page=119,source_id='ASTRA-I-NOTE-119',decision='restored full D. Ferrand attribution with a raised star inside baseline parentheses after the lemma number and before its full stop',English_anchor=r'\textbf{Lemma 4.1}\SGAAuthorFootnote{raisedstar}{This lemma was communicated to the editor by D. Ferrand.}.'),
 dict(page=119,source_id='reviewed source induction in proof4.1',decision='source bounds i≥a and i≥n>a copied exactly; native English had strict inequalities at both positions'),
 dict(page=120,source_id='reviewed source4.2 diagram',decision='u has source P_X and target E_X, matching the specified arrow u:P_X→E_X; native English reversed this displayed arrow'),
 dict(page=120,source_id='reviewed source4.4 category notation',decision='whole Qis/F category underline, underlined slice-site base and literal opposite-category circle retained')
])
(HERE/'EN_EXPOSE_I_TRANSFER_116_120.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_INDEPENDENT_SOURCE_ASSESSMENTS.jsonl';assessments=[json.loads(x) for x in path.read_text().splitlines()]
assessments=[x for x in assessments if x.get('page')!=118]
assessments.append(bound_audit)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in assessments))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith(('116\t','119\t'))]
notes.extend([
 '116\tExample3.6, after the scheme S\tbaseline parenthesized star\t1\tASTRA-I-NOTE-116\tcoordinator direct scan comparison, main PDF130 and witness127\tSGAAuthorFootnote{*}\tFull terminology note distinguishes the historical scheme/prescheme words using the original wording.',
 '119\tLemma4.1 after the numeral\traised star inside baseline parentheses\t1\tASTRA-I-NOTE-119\tcoordinator direct scan comparison, main PDF133 and witness130\tSGAAuthorFootnote{raisedstar}\tFull attribution to D. Ferrand restored before the heading stop.'
])
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
