#!/usr/bin/env python3
"""Register the faithfully compared 106–110 source passage."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import MATH, split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P106_110.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
start=r"so \(\Ho^n(F'_{\leq n})\) (respectively \(\Ho^n(F''_{\leq n})\)) is of finite type"
a=native.index(start)
b=native.index('be the derived functor of the tensor product',native.index(r'\sgaStableTarget{sga6.e01.cor.2-16}',a))
record=dict(id='EN-EXPOSE-I-106-110',page='106–110',place='Exposé I2.12 continuation through the beginning of2.16',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/106–110/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Fresh faithful translation restores the complete cartesian functor expression and [G] reference in2.13, empty-set star choice, both actual triangular diagrams and their bounds107, source categories and notation109, original starred note110 and full universal-projector argument. The parenthetical exceptions to underlining are preserved. Five explicit source variants include the invalid nilpotence-only example in2.15.1 and its justified deletion from current.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(110)
diplomatic,dref=load_reviewed_pages(110,'diplomatic')
en=split(chunk)
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if not 88<=int(x['id'].rsplit('-',1)[1])<=92]
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text',scope_end=None):
 assert en[page].count(corrected)==1,(number,en[page].count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=scope_end or f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(88,106,r"\(F'_{\leq n}\) (resp.",r"\(F'_{\leq n}\)) (resp.",
 'check/findings/findings_106_110.json#1',
 'The preceding reference(2.10.b)) is already closed. The printed extra closer after F-prime has no opener; current removes that single character.', 'continuation of proof2.12')
variant(89,108,r'and \(\underline{C}_1\).',r'and \(\underline{C}_1\)).',
 'check/findings/findings_106_110.json#23',
 'Both numbered references in this sentence are already closed. The final printed parenthesis after C_1 has no opener; current removes it and preserves every parameter substitution.', 'end of proof2.14(ii)')
radical_printed=r'\uline{is a field or when} \(\underline{\operatorname{radical}}(A_s)\) \uline{is nilpotent.}'
radical_reason=("The printed nilpotence-only alternative is an example for the stated hypothesis that finite projective stalk modules are free. For A=k×k, its radical J=0 is nilpotent, but P=k×0 is the image of the idempotent e(a,b)=(a,0). Tensoring along the two coordinate projections gives dimensions1 and0, whereas a free A-module of rank r gives r and r, so P is not free. The retained residue-field example is valid: lift a basis of P/JP to a surjection A^r→P by Nakayama; projectivity splits A^r=P plus K. The chosen basis gives K/JK=0, and K is finitely generated, hence K=0 by Nakayama. Current deletes only the unsupported alternative; the lemma's actual projective-freeness hypothesis is unchanged.")
variant(90,109,r'\uline{is a field.}',radical_printed,
 'ASTRA-I-RADICAL-109; review/expose_i/decisions.jsonl; EN_INDEPENDENT_SOURCE_ASSESSMENTS.jsonl',
 radical_reason, 'Lemma2.15.1(i), parenthetical examples of the stalk hypothesis')
variant(91,110,'Suppose (ii). Let','Suppose (ii), Let',
 'check/findings/findings_106_110.json#32',
 'Both scans show the comma followed by a capital. The diplomatic reading retains it; current separates the two sentences with a full stop.', 'proof2.15.1(ii), opening',scope_end=r'\sgaStableTarget{sga6.e01.cor.2-16}')
variant(92,110,r'\(u_n\)',r'\(U_n\)',
 'check/findings/findings_106_110.json#34',
 "The matrix(T_ij) defines one universal endomorphism. The morphism s satisfies s*(u_n)=p, and its factorization s=i composed with s-prime gives p=s-prime* i*(u_n). All three lowercase references identify that same map. Current gives its definition the lowercase name u_n as well; diplomatic retains the printed capital U_n.",
 'definition of the universal matrix endomorphism',scope_end=r'\sgaStableTarget{sga6.e01.cor.2-16}')
variants.extend(new);variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))

path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json'
pairs=[x for x in json.loads(path.read_text()) if x['page']!=108]
for unit in [m.group(0) for m in MATH.finditer(current[108]) if r'\text{Identité}' in m.group(0)]:
 translated=unit.replace(r'\text{Identité}',r'\text{Identity}')
 assert en[108].count(translated)==1
 pairs.append(dict(page=108,layer='both',French_literal_unit=unit,English_literal_unit=translated,expected_multiplicity=1,
  status='confirmed exact lexical translation of the identity label; all surrounding mathematical characters retained',
  scope='Only this complete literal pair and exact multiplicity are approved.'))
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')

ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 106<=p['page']<=110 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(106,111):
 counts={}
 for command in (r'\underline{C}',r'\underline{S}',r'\underline{O}',r'\underline{n}',r'\underline{\operatorname{radical}}',r'\underline{\Hom}',r'\underline{\End}',r'\mathbb D',r'\varnothing'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
ledger.extend([
 dict(page=106,source_id='reviewed French Proposition2.13',decision='restored explicit cartesian S-functor through the fiber-product category, plain [G] I1.4 reference and plain i.e.; preserved (*=+,-,emptyset)'),
 dict(page=107,source_id='reviewed French proof2.13',decision='restored both triangular diagrams, actual length bound ≤N−1 and actual acyclicity bound ≥m+b in both English forms'),
 dict(page=109,source_id='ASTRA-I-DEFINEDN-109; ASTRA-I-RADICALRULE-109; ASTRA-I-TERMS-109',decision='preserved the first defined n underline, separate radical operator rule, unruled resp. and left-module parenthetical, and original Bourbaki reference'),
 dict(page=110,source_id='ASTRA-I-NOTE-110',decision='original baseline parenthesized-star call and full author note restored',English_anchor=r'\SGAAuthorFootnote{*}{i.e.'),
 dict(page=110,source_id='ASTRA-I-SITE-110; ASTRA-I-O-110',decision='underlined site map and both structure sheaves retained; final-object S in both global-section arguments remains plain'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_106_110.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('110\t')]
notes.append('110\tproof2.15.1(i), after the s-pointed object U\tbaseline parenthesized star\t1\tASTRA-I-NOTE-110\tcoordinator direct scan comparison, main PDF124 and witness121\tSGAAuthorFootnote{*}\tRestore the full author definition of an s-pointed object as an actual footnote.')
path.write_text('\n'.join(notes)+'\n')
path=HERE/'EN_INDEPENDENT_SOURCE_ASSESSMENTS.jsonl';assessments=[json.loads(x) for x in path.read_text().splitlines()]
assessments=[x for x in assessments if x.get('page')!=109]
assessments.append(dict(page=109,source_id='ASTRA-I-RADICAL-109',status='independent mathematical assessment agrees with coordinator; source scan and Bourbaki reading supplied by coordinator',
 observation='The printed disjunct belongs to an example of the stated finite-projective-freeness hypothesis, not to a separate assertion of the main lemma.',
 counterexample='A=k×k, J=0, e(a,b)=(a,0), P=im(e)=k×0. The two tensor functors induced by coordinate projections send P to vector spaces of dimensions(1,0), whereas A^r maps to dimensions(r,r). These dimensions exclude every free rank.',
 retained_example_proof='For the given finite projective P and J=rad(A), a basis of P/JP over the assumed residue field lifts to A^r→P. Nakayama makes it surjective; projectivity splits A^r=P⊕K. The chosen basis gives K/JK=0; finite generation of the direct summand K and Nakayama give K=0. Thus the lifted map is an isomorphism.',
 current_action='Delete only the nilpotence-only example; retain the exact printed branch diplomatically.',English_variant='EN-VAR-090'))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in assessments))
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
