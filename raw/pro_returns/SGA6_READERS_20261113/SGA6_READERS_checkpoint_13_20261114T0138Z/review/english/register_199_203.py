#!/usr/bin/env python3
"""Register mixed structures and the full relative principal-parts construction."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P199_203.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e02.appendix-ii-definition-of-the-analytic-index-of}')
last=native.index(r'\sgaStableTarget{sga6.e02.para.1-2-6}',a)
b=native.index('\n\\[\n i_s^*P^n_{X/S}',last)
record=dict(id='EN-EXPOSE-II-199-203',page='199–203',
 place='Appendix II introduction through the opening of1.2.6',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/199–203/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores complete introduction and numbered notes, source field/sheaf rules, exact local-model arguments and split principal-parts isomorphism, both module actions, the complete complex-coefficient symbol sequence, all source degrees and labels, full elliptic-complex definition and the actual boundary before the fiber comparison. Four explicit variants preserve the mathematical/reference/delimiter differences; the French accent-only apposition repair is separately classified without an invented English error.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']];assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

variants=[]
def add(number,page,old,printed,source,reason,mode='text',region=''):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<203 else None,
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',
  scan_region=region))
add(143,201,r'P^n_{X/S}(E)=P^n_{X/S}\otimes_{\underline{O}_X}E',
 r'P^n_{X/S}(E)=P^n_{X/S}\oplus_{\underline{O}_X}E',
 'check/findings/findings_201_205.json#4',
 'The printed sign is a circled plus, while the immediately following words specify the tensor product using the second O_X action. The balanced construction imposes (p a) tensor e = p tensor (a e), and its canonical map sends e to1 tensor e. Composition with an O_X-linear map from this construction is the factorization in1.2.2.1. Current retains the recorded tensor-product repair; diplomatic preserves the actual plus.',
 mode='math',region='Definition of the principal-parts sheaf of E')
add(144,201,r'is an $f^{-1}(\underline{O}_S)$-linear homomorphism',
 r'is an $f^{-1}(\underline{O}_X)$-linear homomorphism',
 'check/findings/findings_201_205.json#3',
 'For the specified f:X→S, the structure map is f-sharp:f^(-1)O_S→O_X. The two O_X actions on principal parts agree on that image because both projections are over S. Hence d^n(E)(a e)=u_2(a)(1 tensor e)=u_1(a)(1 tensor e) for a from f^(-1)O_S, and an O_X-linear factor h gives D(a e)=a D(e). This exact factorization identifies the source of the required base-linearity. Current uses O_S; diplomatic preserves the printed O_X in this later definition only.',
 region='Base-linearity in the differential-operator definition in1.2.2')
add(145,202,'the identifications (1.2.2.1) and (1.2.3.1)',
 'the identifications (1.2.2.1) and (1.2.4.1)',
 'check/findings/findings_201_205.json#8',
 'The explicit composition h→h composed with d^n(E) gives the real identification1.2.2.1 and complex identification1.2.3.1. The paragraph applies Hom to the exact sequence1.2.4.1 and then uses those two identifications to obtain1.2.4.2. Current repairs the second identification locator to1.2.3.1; diplomatic keeps the printed1.2.4.1. Every map and sequence is retained.',
 region='Reference sentence before the full symbol exact sequence')
add(146,203,'(considered as a monomorphism of ringed spaces) cf.~(1.1).',
 '(considered as a monomorphism of ringed spaces) cf.~(1.1)).',
 'check/findings/findings_201_205.json#12',
 'The parenthesis opening the considered-clause is already closed after spaces, and the reference opening is closed after1.1. Current deletes only the remaining unmatched final close. Diplomatic retains it, with all clause words, the reference and the sentence stop unchanged.',
 region='Opening sentence of1.2.6')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(203)
diplomatic,dref=load_reviewed_pages(203,'diplomatic')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 199<=p['page']<=203:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
  decision='transferred in faithful English; mathematical and delimiter branch differences explicitly recorded',
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(199,204):
  counts={}
  for token in [r'\underline{O}',r'\underline{\underline{R}}',r'\underline{\underline{N}}',
                r'\underline{\underline{C}}',r'\underline{\Homop}',r'\underline{n}',
                r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}',r'\SGAAuthorFootMark{1}',r'\SGAAuthorFootText{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',source=reference['bases'][page-1],counts=counts,
   reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
ledger.extend([
 dict(page=199,source_id='reviewed Appendix II introduction; ASTRA-II-NOTES-199',decision='Restore the two-line title without an unprinted stop after II, both quoted technical phrases, the exact paired references[2][17], the complete proper/local-compactness and compact-base explanations, and the original numerical1 advice to the informed reader. Preserve the single O rules and three literal double field rules.'),
 dict(page=200,source_id='reviewed mixed-variety definition; ASTRA-II-O-200; ASTRA-II-N-200',decision='Restore the primed U-prime×V-prime sheaf subscript, explicit local model in the definition, complete fiber quotient and both projection actions, source1.1 reference and plain1.2.1. Retain ten O rules, two N double rules and the two inspected lexical groups.'),
 dict(page=201,source_id='check/findings/findings_201_205.json#2',decision='The French diplomatic où and current ou differ by an accent in an apposition naming the same displayed Omega^1_(X/S). Both English forms read or relative cotangent sheaf. The French reviewer confirmed this transfer classification; no distinct English lexical error is invented. The exact French branch difference remains in the source-form ledger.',French_printed='où',French_current='ou',English_both='or'),
 dict(page=201,source_id='reviewed principal-parts formulas and lexical rules',decision='Restore the actual split isomorphism P^1≈O⊕Omega^1, all thirteen O rules, complete base-linear universal map and the explicit second module action. The six inspected lexical emphasis groups remain separate; English moves relative before tangent bundle and supplies the understood noun bundle after cotangent. The parenthetical resp. stays plain.'),
 dict(page=202,source_id='ASTRA-II-O-202; ASTRA-II-C-202; ASTRA-II-NOTES-202',decision='Restore the exact S-then-X complexification order, all twenty-three O rules and fifteen C double rules, both complete original numbered notes and their actual call positions, the tensor base in1.2.4.1, both literal baseline Hom slots, and the full complex-coefficient second line of1.2.4.2. No summary substitutes for that line.'),
 dict(page=203,source_id='reviewed symbol construction and elliptic-complex definition',decision='Restore the source Omega^1 domain and both individually underlined Hom sheaves, exact p^*(E)→p^*(F), m/n assignments of u/v and corresponding composition formula, the plain E complex name, inequality≤n_i, individually ruled n, explicit symbol complex and zero-section condition, the source disjunction[4] or[16], and the complete1.2.6 considered-clause. The fiber comparison remains outside this chunk on204.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_199_203.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [199,202])]
notes.extend([
 '199\tAfter mixed structure\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-199\tearly reviewer direct scan comparison, main PDF213\tSGAAuthorFootnote{1}\tComplete original advice to the informed reader.',
 '202\tAfter the first exact-sequence stop\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-202\tearly reviewer direct scan comparison, main PDF216\tSGAAuthorFootMark{1}; SGAAuthorFootText{1}\tComplete symmetric-power explanation.',
 '202\tAfter O_X in the tensoring clause\traised numerical2 inside baseline parentheses\t1\tASTRA-II-NOTES-202\tearly reviewer direct scan comparison, main PDF216\tSGAAuthorFootnote{2}\tComplete specification of the second module structures.'
]);path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
