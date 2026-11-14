#!/usr/bin/env python3
"""Register normalization, the original Section3 notes and the coherer passage."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P185_189.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
lemma=native.index(r'\sgaStableTarget{sga6.e02.lem.2-4-8-1}')
a=native.index('shrinking around $s$',lemma)
b=native.index('\n\\[\n f_{i_0\\ldots i_p}:',a)
record=dict(id='EN-EXPOSE-II-185-189',page='185–189',
 place='Normalization proof through the opening proof of3.5.1',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/185–189/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores the complete normalization-algebra proof and nested tildes, exact local dimension expression, all four original numerical notes on186 including the Verdier attribution, source phi and coproduct notation, exact coherer construction and citations, complete adjunction references and original spectral-sequence note. The native intersection display remains outside this replacement and is aligned with190 in the next chunk.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']]
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

variants=[]
def add(number,page,old,printed,source,reason,mode='text',region=''):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,
  source=source,reason=reason,
  scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<189 else None,
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',
  scan_region=region))
add(133,185,r'that $\widetilde S$ is the analytic spectrum',r'that $S$ is the analytic spectrum',
 'check/findings/findings_181_185.json#27',
 'The previous sentence introduces the normalization S-tilde. Its finite normalization algebra has relative analytic spectrum equal to the domain S-tilde of the explicitly specified projection p:S-tilde→S. Current restores the tilde on this domain name; diplomatic preserves the printed S.',
 region='Identification of the normalization-algebra spectrum')
add(134,185,r'([10] II \S3 Prop.8)',r'(10 II \S3 Prop.8)',
 'check/findings/findings_181_185.json#28',
 'The surrounding citations identify the same work as[10] in IV section3, IV section4 and II section3. This occurrence names Proposition8 of the last section. Current restores its bibliography-number brackets; the specified work, section and proposition are unchanged.',
 region='Citation immediately before the direct-image identity')
add(135,185,r'\widetilde{E_n\cdot\widetilde{\underline{O}}_S}|V=0',
 r'\widetilde{E_n\cdot\widetilde{\underline{O}}_S}|U=0',
 'check/findings/findings_181_185.json#31',
 'The introduced open neighbourhood is V in S-tilde. The ideal carrying the outer tilde is a sheaf on S-tilde, and its restriction is inverse image along V→S-tilde. The earlier U is an open neighbourhood on S; the specified projection p:S-tilde→S relates the two spaces. Current names V in this restriction, while diplomatic preserves U.',
 mode='math',region='Vanishing on the open neighbourhood in the normalization')
add(136,186,'Thus $X$ has codimension','Thus $Y$ has codimension',
 'fixes/RECONCILE_CODEX_6.json#252; fixes/FIXLOG_6_CURRENT.jsonl#359',
 'The specified closed immersion f:X→Y is cut out by I. At the chosen point I_x is nonzero in the domain R=O_(Y,x). Every prime P containing I_x is nonzero, so the strict chain from(0) to P has positive length. This computes the positive codimension of the closed subspace X=V(I) in Y. Current restores X as the subject; diplomatic preserves Y.',
 region='Last proof sentence of Lemma2.4.8.2')
add(137,189,r'(\uline{deduced from} (3.3 b) (ii)) \uline{is an isomorphism}',
 r'(\uline{deduced from} (3.3 b) (ii)) ) \uline{is an isomorphism}',
 'ASTRA-II-PAREN-189',
 'The complete parenthetical has three opening and four closing parentheses in the print. Current removes the final unmatched close; diplomatic retains it. The reference and adjunction arrow E→RQ(E) are unchanged.',
 region='Assertion3.5.1, parenthetical reference')
add(138,189,r'(\uline{deduced from} (3.3 b)(ii)) \uline{is an isomorphism}',
 r'(\uline{deduced from} (3.3 b)(ii)) ) \uline{is an isomorphism}',
 'ASTRA-II-PAREN-189',
 'The second complete parenthetical likewise has one unmatched final close. Current deletes that delimiter only, preserving the reference and adjunction arrow RQ(E)→E; diplomatic keeps every printed delimiter.',
 region='Assertion3.5.2, parenthetical reference')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(189)
diplomatic,dref=load_reviewed_pages(189,'diplomatic')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 185<=p['page']<=189:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
  decision='transferred in faithful English; every source branch difference has an explicit English variant',
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],
  expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(185,190):
  counts={}
  for token in [r'\underline{O}',r'\underline{p}',r'\underline{\underline{R}}',r'\phi',r'\coprod',
                r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}',r'\SGAAuthorFootnote{4}',
                r'\SGAAuthorFootMark{3}',r'\SGAAuthorFootText{3}',
                r'\SGAAuthorFootMark{1}',r'\SGAAuthorFootText{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts))
ledger.extend([
 dict(page=185,source_id='reviewed normalization proof; ASTRA-II-O-185',decision='Restore all eighteen underlined O occurrences, complete projection/direct-image identity, nested tildes, products, analytic references and baseline restrictions. Only reduced, normal and the first étale carry the individually observed lexical rules; the later occurrences remain plain.'),
 dict(page=186,source_id='reviewed Lemma2.4.8.2',decision='Restore the source local-ring localization expression instead of the inherited quotient expression, every underlined prime-ideal occurrence, full local-isomorphism explanation and both analytic references. The printed subject Y and current X are separately branched with the specified immersion and height argument.'),
 dict(page=186,source_id='ASTRA-II-NOTES-186',decision='Restore all four original numerical author notes at their separate calls. Note1 qualifies the local rings, note2 gives J.L. Verdier attribution in the section title, note3 is split between the inclusion display and its full text, and note4 explains the omitted phi convention. The visible body paragraph number3.0 remains plain.'),
 dict(page=187,source_id='reviewed coherer construction',decision='Retain coherer as the supplied English name for the explicitly defined right adjoint Q. Preserve plain coherer in the definition, exact phi, tilde only over Gamma with S outside, EGA Err_I1.8.7, all four coproducts and their exact indices, the separate U_ij declaration and baseline Hom(E,.) slot. No finite-product replacement is made.'),
 dict(page=188,source_id='ASTRA-II-R-188; ASTRA-II-NOTES-188',decision='Preserve all five literal double-underlined R letters and the original numerical1 call in formula(i), with its complete subscript explanation outside the display. The conjunction and between the two memberships is plain. Keep Qf_* and f_*Q without invented space subscripts.'),
 dict(page=189,source_id='ASTRA-II-R-189; ASTRA-II-NOTES-189',decision='Restore formula label3.0, full [H] II7.19 citation, both complete adjunction-reference clauses and the original plain-R spectral-sequence author note. The word of between the two category expressions stays plain, while each displayed derived R has its two observed lower rules.'),
 dict(page=189,source_id='reviewed189/190 boundary',decision='The source189 ends after the affine assertion for f_i; the inherited intersection-inclusion display is kept outside this replacement and will be restored inline on190 with its exact source introduction. This does not claim the inherited190 continuation has been reviewed.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_185_189.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [186,188,189])]
notes.extend([
 '186\tAfter normal in Lemma2.4.8.2\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-186\tearly reviewer direct scan comparison, main PDF200\tSGAAuthorFootnote{1}\tComplete original local-ring qualification.',
 '186\tSection3 title\traised numerical2 inside baseline parentheses\t1\tASTRA-II-NOTES-186\tearly reviewer direct scan comparison, main PDF200\tSGAAuthorFootnote{2}\tExact J.L. Verdier attribution.',
 '186\tInclusion display\traised numerical3 inside baseline parentheses\t1\tASTRA-II-NOTES-186\tearly reviewer direct scan comparison, main PDF200\tSGAAuthorFootMark{3}; SGAAuthorFootText{3}\tComplete Mod/Qcoh explanation with the two source O rules.',
 '186\tAfter study\traised numerical4 inside baseline parentheses\t1\tASTRA-II-NOTES-186\tearly reviewer direct scan comparison, main PDF200\tSGAAuthorFootnote{4}\tOriginal convention concerning omitted phi.',
 '188\tFormula(i)\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-188\tearly reviewer direct scan comparison, main PDF202\tSGAAuthorFootMark{1}; SGAAuthorFootText{1}\tComplete original subscript explanation.',
 '189\tAfter immediate dévissage\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTES-189\tearly reviewer direct scan comparison, main PDF203\tSGAAuthorFootnote{1}\tOriginal spectral sequence with plain R and star abutment.'
])
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
