#!/usr/bin/env python3
"""Register the complete finiteness proof and analytic-index construction."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P214_218.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('Identifying $u$, by',native.index(r'\sgaStableTarget{sga6.e02.para.3-1-5}'))
b=native.index(r'$\operatorname{Ell}_n(F)$ formed',native.index(r'\sgaStableTarget{sga6.e02.para.3-2-3}',a))
record=dict(id='EN-EXPOSE-II-214-218',page='214–218',place='Sheaf maps from operator families through the first part of3.2.3',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/214–218/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores every source operator and presheaf map, the complete indexed-complex construction and three-part proof, literal Hilbert/Sobolev arguments, actual p≥q comparison, exact gamma and source EGA locator, original notes, raised-dot K group notation, full quotient category, unindexed completion limit and all underlined order symbols. The sole mathematical source variant retains the printed target r and corrected r−n with its actual evaluation map.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']];assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
old=r"u_r:\underline C'(S,C^r_2(V,E))"+'\n'+r"  \longrightarrow \underline C'(S,C^{r-n}_2(V,F))."
printed=old.replace(r'C^{r-n}_2(V,F)',r'C^r_2(V,F)')
v=dict(id='EN-VAR-149',page=214,old=old,printed=printed,corrected=old,mode='math',
 source='check/findings/findings_211_215.json#10; fixes/MISPRINTS_6.json#184',
 reason='The defining family is T(s)=phi_r(u(s)) in L(H_E,H_F), with H_E=C^r_2(V,E) and H_F=C^(r-n)_2(V,F), as displayed immediately above. On a relatively compact open W, its induced presheaf map sends a in C(bar W,H_E) to the continuous map s→T(s)a(s) in C(bar W,H_F). Continuity follows from continuous evaluation L(H_E,H_F) times H_E→H_F. This explicit map gives target C-prime(S,C^(r-n)_2(V,F)); the final bundle map also prints that exponent. Current retains r-n and diplomatic preserves the printed r only in this presheaf target.',
 scope_start='%%%%%%%%%%  scan idx 227  |  folio 214',scope_end='%%%%%%%%%%  scan idx 228  |  folio 215',
 scan_image='scan/SGA6_scan_360dpi.pdf#page=228; scan/SGA6_witness_300dpi.djvu#page=225',scan_region='Lower presheaf-map display')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines() if json.loads(x)['id']!=v['id']]+[v]
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]));path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(218);diplomatic,dref=load_reviewed_pages(218,'diplomatic');en=split(chunk)
newpairs=[]
for page in range(214,219):
 fu=Counter(m.group() for m in MATH.finditer(current[page]));eu=Counter(m.group() for m in MATH.finditer(en[page]))
 missing=fu-eu;extra=eu-fu
 assert sum(missing.values())==sum(extra.values())==int(page==215),(page,missing,extra)
 for f,n in missing.items():
  e=f.replace(r'\text{on convient que }',r'\text{we agree that }').replace(r'\text{ si }',r'\text{ when }')
  assert f!=e and extra[e]==n==1
  newpairs.append(dict(page=page,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,
   status='confirmed exact lexical translation of the convention on vanishing terms; all mathematical characters, commands, punctuation, spaces and line breaks retained',
   scope='Only this complete literal mathematical unit and its exact multiplicity in both source forms are approved; no page-wide exception.'))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';pairs=[x for x in json.loads(path.read_text()) if not 214<=x['page']<=218]+newpairs
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 214<=p['page']<=218:continue
 decision='transferred in faithful English in both source forms'
 if p['source_id']=='check/findings/findings_216_220.json#4':decision='French autre/autres plural agreement leaves the English phrase In other words unchanged in both forms; no invented English agreement error'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 a=chunk.index(v['scope_start']);b=chunk.index(v['scope_end'],a);section=chunk[a:b];assert section.count(v['old'])==1
 text=chunk[:a]+section.replace(v['old'],v[reading],1)+chunk[b:];en=split(text)
 for page in range(214,219):
  counts={}
  for token in [r'\underline{O}',r'\underline{\underline{C}}',r'\underline{\underline{Z}}',r'\underline{\underline{R}}',
                r'\underline C',r'\underline F',r'\underline M',r'\underline{n}',r'\underline n',r'\phi',r'\Gamma_S',r'\SGAAuthorFootnote{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
ledger.extend([
 dict(page=214,source_id='reviewed3.1.5 full operator-family construction',decision='Restore the actual Gamma(X|U,E) source/target, displayed label3.1.3, u_infinity name, every presheaf C-prime with its literal single rule, all four closed phi labels, source3.1.3(ii) and3.0.5 references, and the exact Hilbert-bundle map. No replacement of Sobolev notation or map arguments is made.'),
 dict(page=215,source_id='reviewed Theorem3.2.1 and beginning of proof',decision='Restore the independently ruled order n and double-ruled derived R, both plain locators inside the statement, printed comma after isomorphic, source p_*(E) without an added complex dot, the complete named differentials and indexed presheaf complexes, actual r−m_i parameter and phi_(r−m_i)d^i, plus the literal inverse-limit identity and assertion(a) boundary.'),
 dict(page=216,source_id='reviewed full proofs(b),(a-prime), beginning of(a)',decision='Restore the original numerical1 note immediately after [16] XI Theorem6, complete direct quasi-acyclic and direct acyclic terminology with their source[11]/[12] locators, the actual p≥q comparison between singly ruled sheaf F objects, source E without an added dot, the global complex M_pq rather than an inserted fiber, and the explicit sheaf cone. Proof labels keep their plain parenthesized letters outside the word rules.'),
 dict(page=216,source_id='check/findings/findings_216_220.json#4',decision='Both English forms use In other words. The French autre/autres spelling difference affects agreement of the same phrase, with no change to the complex or following assertion.'),
 dict(page=217,source_id='reviewed completion of proof and3.2.2',decision='Restore C(bar U,...) rather than inherited C-infinity(U,...), all actual r/p/q/i indices, the display without an added stop, the separately written transition quasi-isomorphism, unprimed Gamma_S, exact source EGA0_III13.2.3, plain3.2.2 identifier, raised-dot K^bullet, C-ell class notation and double-ruled R in the index. Preserve the full numerical1 note and new paragraph before the definition.'),
 dict(page=218,source_id='reviewed relation to K(S) and3.2.3',decision='Restore the full inline quotient K^b(Loclib)/K^{b,varnothing}(Loclib), exact II2.3.2(a) citation, full parenthetical argument, unindexed completion limit, all three individual order-n rules and actual family index i∈Z. The historical statement of the writer’s uncertainty remains translated as source text; no new assertion or proposed replacement hypothesis is supplied.'),
 dict(page=218,source_id='check/findings/findings_216_220.json#16; fixes/MISPRINTS_6.json#190',decision='French sous espace/sous-espace is a hyphen-only orthographic variant for the same closed subspace defined by d^(i+1)d^i=0. Both English forms use subspace; no invented English space or hyphen error is introduced.'),
 dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected mathematical variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']),
])
for pair in newpairs:ledger.append(dict(page=pair['page'],source_id='individually checked lexical formula pair',decision='only the specified French lexical text is translated',French_literal_unit=pair['French_literal_unit'],English_literal_unit=pair['English_literal_unit'],expected_multiplicity=1,layer='both'))
(HERE/'EN_EXPOSE_II_TRANSFER_214_218.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [216,217])]
notes.extend([
 '216\tAfter [16] XI Th.6 and before the closing parenthesis\traised numerical1 inside baseline parentheses\t1\tASTRA-II-AUTHOR-NOTE-216\tearly reviewer direct scan comparison, main PDF230\tSGAAuthorFootnote{1}\tFull generalization-to-elliptic-complexes note.',
 '217\tAfter corresponding Grothendieck group, before the sentence stop\traised numerical1 inside baseline parentheses\t1\tASTRA-II-AUTHOR-NOTE-217\tearly reviewer direct scan comparison, main PDF231\tSGAAuthorFootnote{1}\tComplete I6.3 and ExposéIV references.'
]);path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=[v['id']],exact_lexical_pairs=len(newpairs),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
