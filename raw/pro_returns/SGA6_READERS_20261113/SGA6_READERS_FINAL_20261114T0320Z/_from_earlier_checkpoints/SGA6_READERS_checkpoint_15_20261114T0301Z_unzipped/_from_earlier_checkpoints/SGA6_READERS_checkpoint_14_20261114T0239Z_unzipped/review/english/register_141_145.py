#!/usr/bin/env python3
"""Register the exact 141–145 source reconstruction and three source variants."""
from pathlib import Path
import json
import re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_I_P141_145.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e01.para.6-2}')
b=native.index('(the two on the left being homomorphisms of presheaves of rings)',a)
record=dict(id='EN-EXPOSE-I-141-145',page='141–145',place='Exposé I6.2 through the final display of6.9',layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by coordinator',
 source='build/page_packets/141–145/current.tex and diplomatic.tex; review/expose_i/patches.jsonl; EN_FRENCH_REVIEW_REFERENCE.json',
 reason='Faithful reconstruction restores all exact C/S/Cart/Parf rules, four phi occurrences, the bare sum, source baseline functor-slot point, raised-star author note and its K notation, page-crossing statements, literal left-module notation, and the complete diagrams. Three printed/current differences are explicitly branched: the indexing object, the lower square arrowhead and the isolated F rule. The external G II2.2.4 citation remains external rather than becoming an English internal hyperlink to Exposé II.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
indices=[i for i,x in enumerate(rows) if x['id']==record['id']]
if indices:rows[indices[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
current,ref=load_reviewed_pages(145)
diplomatic,dref=load_reviewed_pages(145,'diplomatic')
en=split(chunk)
new=[]
def variant(number,page,corrected,printed,source,reason,region,mode='text'):
 assert en[page].count(corrected)==1,(number,en[page].count(corrected))
 new.append(dict(id=f'EN-VAR-{number:03}',page=page,old=corrected,printed=printed,corrected=corrected,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}',
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',scan_region=region))
variant(107,142,r'\uline{for every} \(X\in\Ob \underline{S}\)',r'\uline{for every} \(X\in\Ob\underline{C}_X\)',
 'ASTRA-I-INDEX-142; check/findings/findings_141_145.json#9',
 'The declared family assigns f_U:ob(C_U) to F(U) to every U in ob(S). Its additivity is the identity f_U(L)=f_U(L-prime)+f_U(L-double-prime) on a direct sum or distinguished triangle in that fibre. The selecting quantifier is therefore U in ob(S), with the source dummy variable X retained; diplomatic keeps the printed fibre-object quantifier.',
 'Definition6.5(i), family-index quantifier')
diagram=r'''\[
\begin{tikzcd}
\Ob\underline{C}_Y \arrow[r,"f_Y"] \arrow[d,"u^*"'] & F(Y) \arrow[d,"F(u)"]\\
\Ob\underline{C}_X \arrow[r,"f_X"] & F(X).
\end{tikzcd}
\]'''
variant(108,142,diagram,diagram.replace(r'\arrow[r,"f_X"]',r'\arrow[r,"f_X",dash]'),
 'check/findings/findings_141_145.json#10',
 'The source lower segment has no arrowhead. The declared map f_X:ob(C_X) to F(X) determines its rightward direction, and the square states f_X(u-star L)=F(u)(f_Y(L)). Current supplies that arrowhead; diplomatic preserves the headless segment. Every endpoint, other arrow and label is identical.',
 'Definition6.5(ii), lower f_X edge','display')
variant(109,143,r'for \(f\in\Cart_{\underline{S}}(\underline{C}^{\is},\underline F)\) and',
 r'for \(f\in\Cart_{\underline{S}}(\underline{C}^{\is},F)\) and',
 'check/findings/findings_141_145.json#17',
 'The printed isolated F lacks its rule. The discrete fibred category constructed on142 assigns to x in F(U) the object (U,x), with restriction arrows given by F(u); projection to x is the inverse description. A cartesian functor sends c in C_U to (U,f_U(c)). This explicitly identifies the intended codomain with the underlined F in both adjacent phi targets. Current restores that rule; diplomatic retains the observed plain F.',
 'Definition of phi, first inline Cart membership')
variants=[json.loads(x) for x in (HERE/'EN_VARIANTS.jsonl').read_text().splitlines()]
variants=[x for x in variants if x['id'] not in {v['id'] for v in new}]+new
variants.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
(HERE/'EN_VARIANTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in variants))
ledger=[]
for p in [json.loads(x) for x in (ROOT/'review/expose_i/patches.jsonl').read_text().splitlines()]:
 if 141<=p['page']<=145 and p['layer'] in ('current','both'):
  applied=[r for r in ref['applied_patches'] if r['page']==p['page'] and r['source_id']==p['source_id'] and r['layer']==p['layer']]
  ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='transferred in faithful English; every printed/current difference is explicitly branched',
   patch_record_sha256s=[r['patch_record_sha256'] for r in applied],source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for page in range(141,146):
 counts={}
 for command in (r'\underline{S}',r'\underline{C}',r'\Cart',r'\underline{\Parf}',r'\underline F',r'\phi',r'\mathbb L',r'\Kpx(C)'):
  counts[command]=dict(French=current[page].count(command),English=en[page].count(command))
  assert counts[command]['French']==counts[command]['English'],(page,command,counts[command])
 ledger.append(dict(page=page,source_id='exact reviewed page glyph inventory',decision='literal symbol-command multiplicity agrees',current_source=ref['bases'][page-1],diplomatic_source=dref['bases'][page-1],counts=counts))
for v in new:
 ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
ledger.extend([
 dict(page=141,source_id='ASTRA-I-C-141; check/findings/findings_141_145.json#2/#3',decision='all36 plain C and the one plain D retained; no lower index added to the sum; Add(C,.) retains its baseline point'),
 dict(page=141,source_id='ASTRA-I-NOTE-141',decision='complete raisedstar note restored, including the lowercase opening and both Kpx(C) occurrences'),
 dict(page=142,source_id='ASTRA-I-TERMS-142; ASTRA-I-C-142',decision='the first two C letters remain plain; subsequent independently underlined letters and all mathematical units are unchanged despite English adjective order'),
 dict(page=142,source_id='reviewed source142–143 boundary',decision='continuous adjective–noun phrase crosses the marker with English word order',French_boundary='groupe | abélien',English_boundary='abelian | group',reason='Both lexical elements and the sentence are preserved; the source-page marker does not claim a word-for-word bilingual split.'),
 dict(page=143,source_id='check/findings/findings_141_145.json#13/#14/#15/#16',decision='all four exact phi commands restored in place of the inherited English rho commands; same declared map, evaluation formula and sequence retained'),
 dict(page=142,source_id='review/expose_i/cart_macro_audit.json',decision='twelve redundant outer Cart rules removed across142–144; the retained Cart macro already expands to exactly one rule',reason='The source125 definition is Cart=underline(operatorname(Cart)); adding another underline produced two rules in the PDF. Only the redundant wrapper was removed, preserving every endpoint, arrow, label, and single printed rule.'),
 dict(page=143,source_id='ASTRA-I-PARF-143',decision='only the second Parf operator is ruled; the first displayed k-map keeps its plain Parf'),
 dict(page=144,source_id='reviewed source proof6.7; check/findings/findings_141_145.json#24',decision='all three exact rows and vertical arrows preserved; final q.e.d. sentence has its own source paragraph; G II2.2.4 remains an external bibliography reference'),
 dict(page=145,source_id='check/findings/findings_141_145.json#27/#28',decision='double-struck L on u-star preserved, tensor superscript L plain; no extra comma appended to the square'),
 dict(page=145,source_id='reviewed source6.8/6.9',decision='left A-module subscripts, all14 underlined C and15 underlined S, both explicit2.15.1 references, and full final four-term k display restored'),
])
(HERE/'EN_EXPOSE_I_TRANSFER_141_145.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('141\t')]
notes.append('141\tParagraph6.3, after k(C)\traised star inside baseline parentheses\t1\tASTRA-I-NOTE-141\tcoordinator direct scan comparison, main PDF155 and witness152\tSGAAuthorFootnote{raisedstar}\tFull lowercase-opening note retained with the four plain C letters and both Kpx commands.')
path.write_text('\n'.join(notes)+'\n')
pattern=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
old_targets=set(re.findall(pattern,record['old']));new_targets=set(re.findall(pattern,chunk))
assert old_targets and old_targets==new_targets,dict(missing=sorted(old_targets-new_targets),extra=sorted(new_targets-old_targets))
print(json.dumps(dict(passage=record['id'],variants=[v['id'] for v in new],transfer_rows=len(ledger),stable_targets=len(old_targets)),ensure_ascii=False))
