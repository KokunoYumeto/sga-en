#!/usr/bin/env python3
"""Occurrence-scoped projective P convention, closing the VI glyph audit."""
import json
from pathlib import Path
from review_helpers import Review,read,HERE
r=Review()
comparison='For each base map T→S, the projective notation represents the set of surjections E_T→L with L invertible, modulo isomorphism of the quotient. The comparison between the two rendered P names sends every quotient to itself and has itself as inverse; it commutes with pullback. On Proj(Sym E), it is induced by id_E, hence by id on every symmetric power and every degree-zero localization chart. Thus the corrected bold P preserves precisely the represented functor while the diplomatic form reproduces the two observed lower rules.'
for p,count in {365:1,369:2,379:1,380:1,385:1,391:1,394:1}.items():
 id=f'ASTRA-VI-PROJECTIVE-P-{p}'
 why=f'Both complete source images were compared during this folio’s review. The native image was re-opened at closure of VI (native385_prop.png for385); all{count} projective P occurrences show two distinct lower rules. NOTE6 explicitly accepts the bold transport for the symmetric-algebra S, but supplies no projective-P exception. '+comparison
 r.own_finding(id,p,f'{count} projective P operators, each doubly ruled',r'\mathbf P','Diplomatic literal double rule; current retains bold P.',why,'Every projective-bundle P on this folio',kind='font',verdict='amended',witness=p+11)
 r.own[-1].update(observed_occurrences=count,is_misprint=False,correction_status='Explicit source/current notation convention')
 r.patch(p,'diplomatic',r'\mathbf P',r'\underline{\underline{P}}',id,why,count=count)
for k,p,printed,region in [(1,391,'P has two lower rules; each F has one','Top recursive projective-bundle construction'),(25,394,'D and P each have two lower rules; E has one','Rank-one flag/projective specialization')]:
 why='The complete primary/native images and the native reinspection show the stated separate rules. The diplomatic P now receives its literal double rule, matching the already restored D where present; current retains bold P. The single F/E rules remain as previously restored. '+comparison
 r.finding('391_395',k,printed,why,region,verdict='amended',change='Complete the P notation decision with a literal diplomatic double rule and bold current P.',witness=p+11,actual_page=p)
r.commit()

# Correct the former overbroad NOTE6 description in live records and its producer.
replacements={
 'Doubly ruled S and P retain the explicitly accepted NOTE_6 bold transport.':'The doubly ruled S retains the explicitly accepted NOTE_6 bold transport. The source P is separately adjudicated under ASTRA-VI-PROJECTIVE-P-365: literal double rule diplomatically, bold P currently.',
 'bold S/P retain the explicitly accepted NOTE_6 transport.':'The symmetric-algebra S retains the explicit NOTE_6 transport. Projective P occurrences are separately adjudicated in amend_projective_p.py; that exception was not stated in NOTE6.',
}
for name in ['decisions.jsonl','own_findings.jsonl','patches.jsonl']:
 rows=read(name)
 for row in rows:
  for field in ['reason','change']:
   if not isinstance(row.get(field),str):continue
   for old,new in replacements.items():row[field]=row[field].replace(old,new)
 (HERE/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
p=HERE/'add_365_370.py';s=p.read_text()
for old,new in replacements.items():s=s.replace(old,new)
p.write_text(s)
(HERE/'projective_p_convention.json').write_text(json.dumps({
 'id':'ASTRA-VI-PROJECTIVE-P-CONVENTION',
 'source_occurrences':{'365':1,'369':2,'379':1,'380':1,'385':1,'391':1,'394':1,'397':9},
 'count':17,'diplomatic':'literal two lower rules','current':'bold P',
 'comparison':comparison,
 'scope':'Only the17 reviewed projective-bundle operators, including the397 subscript and diagram. The single-rule module letters P on366 and polynomial P_i elsewhere retain their separately read forms. The bfP macro definition after415 is a definition for the following exposé, not a printed occurrence.',
 'prior_record_amendment':'Earlier live365–370 records incorrectly extended the explicit NOTE6 symmetric-S exception to P; their descriptions are amended. Previously saved checkpoints remain unchanged.'
},ensure_ascii=False,indent=2)+'\n')
