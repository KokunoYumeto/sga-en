#!/usr/bin/env python3
"""Register the smooth reduction, full projection formula proof and Definition4.1."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH
H=Path(__file__).resolve().parent;R=H.parents[1]
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
chunk=(H/'EN_EXPOSE_III_P246_250.tex').read_text();native=(H/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e03.prop.3-6}');b=native.index('of a regular immersion and a smooth morphism',native.index(r'\sgaStableTarget{sga6.e03.ex.4-1-1}',a))
record=dict(id='EN-EXPOSE-III-246-250',page='246–250',place='Proposition3.6, projection formula and full proof, direct-image corollaries and definition of relative perfection',layer='both',old=native[a:b],new=chunk,status='accepted passage comparison; exact scanned French decisions supplied by coordinator',source='build/page_packets/246–250/current.tex and diplomatic.tex; review/expose_iii/patches.jsonl',reason='Restores the exact smooth-reduction tensor bases and projections, omitted square, actual bounded-category hypotheses, both original projection-formula notes, full two-case proof with the source case order, precise base-change data and references, complete corollaries and every clause of Definition4.1. The recalled relative base f/S is the sole source variant.')
proof=json.loads((R/'review/expose_iii/projection_amplitude_248.json').read_text())
old=r'Suppose \(E\) (resp. \(M\)) is of finite flat amplitude rel. to \(S\) (resp. finite flat amplitude).'
v=dict(id='EN-VAR-164',page=248,old=old,printed=old.replace(r'to \(S\)',r'to \(f\)'),corrected=old,mode='text',source=proof['source'],reason=proof['proof'],scope_start='%%%%%%%%%%  scan idx 261  |  folio 248',scope_end='%%%%%%%%%%  scan idx 262  |  folio 249',scan_image='; '.join(proof['images']),scan_region='Recalled finite-amplitude hypothesis in the projection-formula proof')
cur,ref=load_reviewed_pages(250);dip,dref=load_reviewed_pages(250,'diplomatic');ledger=[];pairs=[];unit_count=0
for layer,reading,fr,rr in [('current','corrected',cur,ref),('diplomatic','printed',dip,dref)]:
 a=chunk.index(v['scope_start']);b=chunk.index(v['scope_end'],a);part=chunk[a:b];assert part.count(v['old'])==1
 text=chunk[:a]+part.replace(v['old'],v[reading],1)+chunk[b:];en=split(text)
 for page in range(246,251):
  f=Counter(m.group() for m in MATH.finditer(fr[page]));e=Counter(m.group() for m in MATH.finditer(en[page]));missing=f-e;extra=e-f
  assert sum(missing.values())==sum(extra.values())==int(page==250),(page,layer,missing,extra)
  if layer=='current':unit_count+=sum(f.values())
  for ff,n in missing.items():
   ee=ff.replace(r'\text{ou }',r'\text{or }');assert ee!=ff and extra[ee]==n==1
   pairs.append(dict(page=page,layer=layer,French_literal_unit=ff,English_literal_unit=ee,expected_multiplicity=1,status='confirmed complete lexical formula translation: ou becomes or, with all remaining characters retained',scope='This exact Definition4.1 display in the stated source branch only.'))
  counts={}
  for token in [r'\underline{O}',r'\Ob',r'\Id',r'\mathrm L',r'\simeq',r'\operatorname{pr}_1',r'\operatorname{pr}_2',r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}','hook']:
   counts[token]=dict(French=fr[page].count(token),English=en[page].count(token));assert counts[token]['French']==counts[token]['English'],(page,layer,token)
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='Every mathematical unit agrees literally except the one independently paired connective in4.1; specified glyph and original-note multiplicities agree.',source=rr['bases'][page-1],counts=counts,reviewed_French_page_sha256=sha(fr[page]),English_page_sha256=sha(en[page])))
for raw in (R/'review/expose_iii/patches.jsonl').read_text().splitlines():
 p=json.loads(raw)
 if 246<=p['page']<=250:ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision='Transferred into the faithful English passage and its two source forms.',patch_record_sha256=sha(raw),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
ledger.extend([
 dict(page=246,source_id='reviewed Proposition3.6',decision='Restore the hooked immersion, exact parentheses around every direct-image argument, all word rules and plain case labels. Preserve the statement ending at the original folio boundary; no proof text is pulled back from247.'),
 dict(page=247,source_id='reviewed proof of3.6',decision='Restore the relative amplitudes over f/f-prime, upper-case Id, omitted Cartesian square and its actual pr2/pr1 positions, source section of both projections, both one-way implications and the full derived Ls*pr2* comparison. The inherited absolute amplitude equation, swapped projections, double implication and omitted L are replaced by the exact reviewed source.'),
 dict(page=247,source_id='ASTRA-III-AUTHOR-NOTES-247',decision='Restore original numerical1 immediately after the quoted underlined Projection formula heading and its complete cf.(H II5.6) text, including the separate following sentence stop. Restore original numerical2 immediately after the M membership and its complete qcoh explanation. Both calls preserve raised digits within baseline parentheses. Restore the statement’s exact D^b(X) hypothesis and all independent quotation/rule scopes.'),
 dict(page=248,source_id='reviewed full projection-formula proof',decision='Restore every bounded-category assertion and EGA reference, the exact source adjunction arrow and two canonical maps, all tensor bases and upright L letters, the genuine source(*) tag and both baseline full-stop placeholders. Translate non respé as first case and respé as second case with respect to the source’s preceding E(resp.M) sentence: first E has finite relative flat amplitude, second M has finite flat amplitude. This preserves the original case order; the inherited English had interchanged the two reductions. Restore the full ordinary-module, left-resolution, truncation, inductive-limit and finite-free steps.'),
 dict(page=249,source_id='reviewed base-change conclusion and Corollary3.7.1',decision='Restore S=Spec(A), the exact EGA0_IV18.2.3 locator, both structural projections with their original parentheses and f_(S-prime) name, the complete flat base-change conclusion and source EGA references. Restore the corollary’s D^b hypothesis, explicit source restriction statement, complete3.3(i)⇔(iv) citation and every universal quantifier in its proof.'),
 dict(page=250,source_id='reviewed Corollary3.7.2 and Definition4.1',decision='Restore the corollary’s source D^b hypothesis and3.1 locator, all seven clauses of4.1 including the second notation in the display, explicit nonnegative n and repeated perfect-amplitude membership, and exact plain newly defined predicates. The final definition retains the source subject f, rather than inserting an additional structure-sheaf expression. Preserve the beginning of Example4.1.1 and its open parenthesis across250/251.'),
 dict(page=248,source_id=v['source'],decision='Explicit English printed/corrected relative-base variant; the statement and both canonical maps stay unchanged.',English_variant=v['id'],printed=v['printed'],corrected=v['corrected'],source_packet='review/expose_iii/projection_amplitude_248.json',source_packet_sha256=hashlib.sha256((R/'review/expose_iii/projection_amplitude_248.json').read_bytes()).hexdigest()),
])
for pair in pairs:ledger.append(dict(page=pair['page'],source_id='individually checked complete lexical display',decision='Only the connective ou is translated.',**{k:pair[k] for k in ['layer','French_literal_unit','English_literal_unit','expected_multiplicity']}))
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}';ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot==nt and len(ot)==9,(ot,nt)
path=H/'EN_TRANSLATION_PATCHES.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()];hits=[i for i,x in enumerate(rows) if x['id']==record['id']];assert len(hits)<=1
if hits:rows[hits[0]]=record
else:rows.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id']!=v['id']]+[v];rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
path=H/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';rows=[x for x in json.loads(path.read_text()) if not 246<=x['page']<=250]+pairs;path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(H/'EN_EXPOSE_III_TRANSFER_246_250.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=H/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not x.startswith('247\t')]
notes.extend(['247\tAfter quoted Projection formula heading\traised numerical1 inside baseline parentheses\t1\tASTRA-III-AUTHOR-NOTES-247\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{1}\tComplete cf.(H II5.6) note and following body stop.','247\tAfter M membership in Proposition3.7\traised numerical2 inside baseline parentheses\t2\tASTRA-III-AUTHOR-NOTES-247\tcoordinator direct primary/native comparison\tSGAAuthorFootnote{2}\tComplete source qcoh subcategory explanation.']);path.write_text('\n'.join(notes)+'\n')
print(json.dumps(dict(passage=record['id'],variants=[v['id']],math_units=unit_count,lexical_pair_records=len(pairs),transfer_rows=len(ledger),stable_targets=len(ot))))
