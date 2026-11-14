#!/usr/bin/env python3
"""Register the source rigidity passage, retaining the separately audited claim."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split,MATH

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P204_208.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index('\n\\[\n i_s^*P^n_{X/S}',native.index(r'\sgaStableTarget{sga6.e02.para.1-2-6}'))
b=native.index(" of $s$ such that",native.index(r'\sgaStableTarget{sga6.e02.cor.2-8}',a))
record=dict(id='EN-EXPOSE-II-204-208',page='204–208',place='Fiber comparison through the first part of Corollary2.8',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/204–208/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores source regularity r≥1, all fiber and Hom-sheaf notation, the full two direct-limit paragraphs omitted from the inherited proof, actual A_0/A_1 and f_0/f_1 indexing, full cutoff construction, both original numerical1 notes on205 and the complete original206 note. Retains the source general Hom assertion in both forms with its separate author-claim audit; supplies no replacement hypothesis. Three exact lexical formula pairs are recorded.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
hits=[i for i,x in enumerate(records) if x['id']==record['id']];assert len(hits)<=1
if hits:records[hits[0]]=record
else:records.append(record)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
current,ref=load_reviewed_pages(208);diplomatic,dref=load_reviewed_pages(208,'diplomatic');en=split(chunk)
newpairs=[]
for page in range(204,209):
 fu=Counter(m.group() for m in MATH.finditer(current[page]));du=Counter(m.group() for m in MATH.finditer(diplomatic[page]));eu=Counter(m.group() for m in MATH.finditer(en[page]));assert fu==du
 missing=fu-eu;extra=eu-fu
 assert sum(missing.values())==sum(extra.values())=={204:0,205:0,206:0,207:1,208:2}[page]
 for f,n in missing.items():
  e=f.replace(r'\text{pour }',r'\text{for }').replace(r'\text{ouvert}',r'\text{open}')
  assert f!=e and extra[e]==n==1
  newpairs.append(dict(page=page,layer='both',French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,
   status='confirmed exact lexical translation of pour to for or ouvert to open; all mathematical characters, commands, punctuation, spaces and line breaks retained',
   scope='Only this complete literal mathematical unit and its exact multiplicity in both source forms are approved; no page-wide exception.'))
path=HERE/'EN_APPROVED_LEXICAL_MATH_PAIRS.json';pairs=[x for x in json.loads(path.read_text()) if not 204<=x['page']<=208]+newpairs
path.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
ledger=[]
for raw in (ROOT/'review/expose_ii/patches.jsonl').read_text().splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 204<=p['page']<=208:continue
 decision='transferred in faithful English in both source forms'
 if p['source_id']=='check/findings/findings_201_205.json#16':decision='French ou/où accent repair has the same descriptive English connective where in both forms; no invented English lexical error'
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],decision=decision,
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],expected_source_count=p.get('expected_count',1)))
for layer,french,reference in [('current',current,ref),('diplomatic',diplomatic,dref)]:
 for page in range(204,209):
  counts={}
  for token in [r'\underline{O}',r'\underline{\underline{R}}',r'\underline{\Homop}',r'\bar f',r'\SGAAuthorFootnote{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts,reviewed_French_page_sha256=hashlib.sha256(french[page].encode()).hexdigest(),English_page_sha256=hashlib.sha256(en[page].encode()).hexdigest()))
ledger.extend([
 dict(page=204,source_id='check/findings/findings_201_205.json#13',decision='French variétes/variétés is an accent-only spelling difference with the unchanged English plural varieties in both forms.'),
 dict(page=204,source_id='reviewed fiber comparison and rigidity conventions',decision='Restore parentheses in the principal-parts pullback and restriction arguments, the plain complex name E, original1.2.5 reference, exact r≥1 bound, quoted rigid terminology, plain2.0 number, full Hom-sheaf definition and source punctuation of2.1.1.'),
 dict(page=205,source_id='check/findings/findings_201_205.json#16',decision='Both English forms use where to describe V, the named factor in S-prime×V. Record the French printed ou/current où accent difference without changing the described factor or inventing an English error.',French_printed='ou',French_current='où',English_both='where'),
 dict(page=205,source_id='check/findings/findings_201_205.json#17',decision='Restore two separate original numerical1 notes: Proposition2.2 carries the complete A.Douady attribution, while the later T.F.II3.3.1 call carries the paracompact-neighborhood statement. Both labels are literally1; they are not merged or renumbered.'),
 dict(page=205,source_id='fixes/RECONCILE_CODEX_6.json#260',decision='Retain the source open neighborhood of x without an inserted quantifier. The reviewed stalk map sends the germ of an S-morphism h at x to the germ of its fiber restriction; this identifies the proof-local role of x without changing the transcription.'),
 dict(page=205,source_id='reviewed full local-extension proof',decision='Restore A_0, the compactness and product-neighborhood explanations, both full direct-limit displays with their distinct literal Lim forms, both sets of indexing neighborhoods, source m/n coordinate dimensions and complete target-chart clauses. No inherited summary replaces either display.'),
 dict(page=206,source_id='reviewed Lemma2.2.1; check/findings/findings_206_210.json#2',decision='Retain A_0/A_1, U_0/U_1, f_0/f_1, the exact source domains, all three plain resp. abbreviations, both separate conclusions, C^r cutoff functions, actual support condition and full bar-f formula. The single abbreviated s×U stays as printed; the map u→(s,u) identifies its image with the other explicitly braced fiber occurrences.'),
 dict(page=206,source_id='ASTRA-II-AUTHOR-CLAIM-206',decision='Retain Corollary2.3 and the adjoining proof text in both English forms. A separate English transfer packet records the exact source audit and counterexample; no replacement assertion, changed target or added hypothesis is inserted.',record='EN_AUTHOR_CLAIM_TRANSFER_206.json'),
 dict(page=206,source_id='ASTRA-II-NOTE-206',decision='Restore the full original numerical1 note at the softness assertion, including the editor\'s historical question, all three source O rules and the exact2.5 reference. The author note remains separate from the later critical audit.'),
 dict(page=207,source_id='reviewed Corollaries2.4/2.5',decision='Restore literal S=s, every inverse-image argument and tensor base, the baseline H^0(A,.) slot, all three T.F. references, and the entire parenthetical hypothesis example with its independent lexical rules.'),
 dict(page=208,source_id='reviewed Corollaries2.6/2.8 and Proposition2.7',decision='Keep the exact bar-f name, source Lim expression Hom(X|S-prime,Y) with its displayed open condition, source T.F.II3.3.1 citation, inline tangent-map expression, all source morphism arguments, and the three individually underlined resp. abbreviations in2.8. The208/209 boundary follows S-prime in the conclusion.'),
])
for pair in newpairs:ledger.append(dict(page=pair['page'],source_id='individually checked lexical formula pair',decision='only the specified French lexical text is translated',French_literal_unit=pair['French_literal_unit'],English_literal_unit=pair['English_literal_unit'],expected_multiplicity=1,layer='both'))
(HERE/'EN_EXPOSE_II_TRANSFER_204_208.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
claimpath=ROOT/'review/expose_ii/author_claim_issue_206.json';claim=json.loads(claimpath.read_text())
claim_start=en[206].index(r'\sgaStableTarget{sga6.e02.cor.2-3}')
claim_en=en[206][claim_start:]
packet=dict(source_id=claim['source_id'],status='source claim retained in both English forms; attributed transfer of the French reviewer mathematical audit, with no new scan reading claimed',
 source_packet='review/expose_ii/author_claim_issue_206.json',source_packet_sha256=hashlib.sha256(claimpath.read_bytes()).hexdigest(),
 English_source_passage=claim_en,English_passage_sha256=hashlib.sha256(claim_en.encode()).hexdigest(),
 exact_restriction_map=claim['exact_restriction_map'],allowed_example=claim['allowed_example'],obstruction=claim['obstruction'],scope=claim['scope'],
 textual_change='None. The source statement, full original author note and adjoining proofs remain translated in both branches; no replacement theorem or hypothesis is supplied.')
(HERE/'EN_AUTHOR_CLAIM_TRANSFER_206.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv';notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [205,206])]
notes.extend([
 '205\tAfter Proposition before2.2\traised numerical1 inside baseline parentheses\t1\tcheck/findings/findings_201_205.json#17\tearly reviewer direct scan comparison, main PDF219\tSGAAuthorFootnote{1}\tComplete A.Douady attribution.',
 '205\tAfter the T.F.II3.3.1 citation\traised numerical1 inside baseline parentheses\t1\tcheck/findings/findings_201_205.json#17\tearly reviewer direct scan comparison, main PDF219\tSGAAuthorFootnote{1}\tSeparate complete paracompact-neighborhood note; same printed label1 retained.',
 '206\tCorollary2.3, after the second softness assertion\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-206\tearly reviewer direct scan comparison, main PDF220\tSGAAuthorFootnote{1}\tComplete original historical question and reference2.5; separate from the critical audit.'
]);path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk));assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],new_source_variants=0,exact_lexical_pairs=len(newpairs),transfer_rows=len(ledger),stable_targets=len(ot)),ensure_ascii=False))
