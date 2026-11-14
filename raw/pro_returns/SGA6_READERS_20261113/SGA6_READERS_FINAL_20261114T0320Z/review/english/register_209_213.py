#!/usr/bin/env python3
"""Register the full Hilbert/Sobolev conventions and auxiliary results."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P209_213.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(' of $s$ such that',native.index(r'\sgaStableTarget{sga6.e02.cor.2-8}'))
b=native.index('Identifying $u$, by',native.index(r'\sgaStableTarget{sga6.e02.para.3-1-5}',a))
record=dict(id='EN-EXPOSE-II-209-213',page='209–213',place='Conclusion of Corollary2.8 through the opening of3.1.5',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/209–213/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores the full diagonal proof, three-row Hom comparison, precise Sobolev notation and transition direction, complete Hilbert-bundle conventions and tensor-product density proof, actual Bourbaki and Schwartz locators, closed phi map names, all original numerical notes, and full technical assertions and proof paragraphs. Two shared abbreviation variants and one exact lexical formula pair are explicitly recorded.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']];assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

variants=[]
def add(number,page,old,printed,source,reason,region):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode='text',
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<213 else None,
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
add(147,211,r'to that of $\underline{O}_S$ resp.',r'to that of $\underline{O}_S$ rep.',
 'check/findings/findings_211_215.json#2',
 'The printed shared abbreviation rep. lacks the s in resp. The real bundle is assigned its O_S section sheaf; the complex bundle is assigned its O_S tensor C section sheaf. Current restores the abbreviation linking these two stated assignments. Diplomatic preserves rep. at this occurrence; all functor data are unchanged.',
 'Real and complex Hilbert-bundle section functor in3.0.5')
add(148,213,'results of (loc.cit.):','results of (loc.cit):',
 'check/findings/findings_211_215.json#9',
 'Current supplies the missing final abbreviation stop in the shared Latin locator loc.cit. Diplomatic retains the printed loc.cit without that stop. The surrounding reference, two assertions and their separate arguments remain fully translated.',
 'Parenthetical proof of the two assertions after3.1.3')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(213);diplomatic,dref=load_reviewed_pages(213,'diplomatic');en=split(chunk)
newpairs=[]
for page in range(209,214):
 fu=Counter(m.group() for m in MATH.finditer(current[page]));du=Counter(m.group() for m in MATH.finditer(diplomatic[page]));eu=Counter(m.group() for m in MATH.finditer(en[page]));assert fu==du
 missing=fu-eu;extra=eu-fu
 assert sum(missing.values())==sum(extra.values())==int(page==210),(page,missing,extra)
 for f,n in missing.items():
  e=f.replace(r'\text{ouvert}',r'\text{open}')
  assert f!=e and extra[e]==n==1
  newpairs.append(dict(page=page,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,
   status='confirmed exact lexical translation of ouvert to open; all mathematical characters, commands, punctuation, spaces and line breaks retained',
   scope='Only this complete literal three-row mathematical unit and its exact multiplicity in both source forms are approved; no page-wide exception.'))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';pairs=[x for x in json.loads(path.read_text()) if not 209<=x['page']<=213]+newpairs
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 209<=p['page']<=213:continue
 decision='transferred in faithful English in both source forms; abbreviation differences explicitly branched'
 if p['source_id']=='check/findings/findings_206_210.json#6':decision='French singular/plural agreement difference uses the same English neighborhoods for the stated family of open neighborhoods in both forms; no invented English agreement error'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(209,214):
  counts={}
  for token in [r'\underline{O}',r'\underline{\underline{C}}',r'\underline{\underline{N}}',r'\underline{\underline{Z}}',
                r'\underline C',r'\underline E',r'\underline{\Homop}',r'\phi',r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootMark{1}',r'\SGAAuthorFootText{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
ledger.extend([
 dict(page=209,source_id='reviewed diagonal argument and Corollaries2.9/2.10',decision='Restore the full fiber-product and diagonal argument with both separate shrinkings of S, the complete SGA1 I5.1 author note, exact restriction notation, underlined resp. and projection explanation, and original induction homomorphism. The references2.5 remain plain; the source family of open neighborhoods is rendered neighborhoods in both forms.'),
 dict(page=210,source_id='reviewed3.0.1–3.0.4 conventions',decision='Restore the complete three-row Hom comparison, the actual T.F.II3.3.1 reference, all four plain paragraph identifiers, the continuous-function sheaf with its single C rule, Banach operator L, the literal Sobolev notation C^r_2 and transition C^s_2→C^r_2 for s≥r, plus the compactness and finite-rank hypotheses. No relabeling of r and s is applied.'),
 dict(page=211,source_id='reviewed3.0.5 and Lemmas3.1.1/3.1.2',decision='Restore the full additive section functor, single section-sheaf E rule, all three C-prime occurrences with the prime outside its single rule, the plain3.0.1 locator, uniform-convergence topology and both separate continuity/density assertions. The section and paragraph hierarchy follows the source.'),
 dict(page=212,source_id='reviewed tensor-product density proof and3.1.3',decision='Restore the complete finite-dimensional-image parenthesis, Bourbaki Intégration chap.III §2 lemmas1/2, full u_X equality and closure argument, all fourteen double-ruled coefficient C letters, the source [16] IX Theorem12 locator, closed phi map labels, exact Sobolev indices and source extension-of-scalars wording. The isolated continuous word remains underlined and the original complex-case note retains numerical1.'),
 dict(page=213,source_id='reviewed3.1.3 conclusion through3.1.5',decision='Retain the actual allocation of proofs: item(ii) follows from definitions, item(i) from a partition of unity and the product-derivative formula. Restore every pullback argument, complete continuous-map/isomorphism assertion and proof, separate word rule on and between E and F, and the intentional omission of the C subscript in the final display with its complete numerical1 author note.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected shared abbreviation variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
for pair in newpairs:ledger.append(dict(page=pair['page'],source_id='individually checked lexical formula pair',decision='only the specified French lexical text is translated',French_literal_unit=pair['French_literal_unit'],English_literal_unit=pair['English_literal_unit'],expected_multiplicity=1,layer='both'))
(HERE/'EN_EXPOSE_II_TRANSFER_209_213.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [209,212,213])]
notes.extend([
 '209\tAfter open immersion in the diagonal proof\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-209\tearly reviewer direct scan comparison, main PDF223\tSGAAuthorFootnote{1}\tFull analogy with Algebraic Geometry and SGA1 I5.1 reference.',
 '212\tAfter complex vector bundles\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-212\tearly reviewer direct scan comparison, main PDF226\tSGAAuthorFootnote{1}\tFull real-case analogy.',
 '213\tAfter the final3.1.5 display stop\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-213\tearly reviewer direct scan comparison, main PDF227\tSGAAuthorFootMark{1}; SGAAuthorFootText{1}\tFull explanation of the omitted coefficient subscript.'
]);path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),exact_lexical_pairs=len(newpairs),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
