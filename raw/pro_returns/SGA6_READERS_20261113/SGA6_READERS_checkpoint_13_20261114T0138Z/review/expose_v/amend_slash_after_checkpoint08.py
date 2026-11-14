#!/usr/bin/env python3
"""Occurrence-scoped denominator grouping; immutable checkpoint08 is untouched."""
from review_helpers import Review,HERE
import json
r=Review()
proof=('The already inspected proof on325 expands the substituted monomial as t^n(1-t)^(-n), fixing rho_minus:h(t)→h(t/(1-t)). '
 'The inverse map is rho_plus:h(t)→h(t/(1+t)): the two fractional substitutions compose to t in both orders. '
 'Also lambda_t(-1)lambda_t(1)=1 and lambda_t(1)=1+t, so lambda_t(-1)=1/(1+t). '
 'The unit on327 is rho_minus(1+t)=1+t/(1-t)=1/(1-t). '
 'On329, applying rho_minus to(1+t)^x gives(1/(1-t))^x=exp(-xLog(1-t)). '
 'Thus each grouping below is fixed by an explicit map or multiplicative inverse, rather than a general change to slash notation. '
 'These are post-checkpoint08 current-only grouping amendments; the printed forms remain diplomatic and the immutable snapshot remains unchanged.')
specs=[
 ('ASTRA-V-SUBSTITUTION-325',325,
  'The five slash occurrences on325 have no denominator parentheses: three t/1-t, one t/1+t, and one1/1+t.',
  r'Current t/(1-t), t/(1+t),1/(1+t); retain all five literal slash forms diplomatically.',
  'Group the denominators in the current layer at the five individually inspected occurrences.',
  '3.2(ii), proof i) inverse series, and two proof ii) substitutions',336),
 ('ASTRA-V-SUBSTITUTION-326',326,
  'The definition of rho_t prints rho_t(t)=t/1-t.',
  r'Current \rho_t(t)=t/(1-t); diplomatic \rho_t(t)=t/1-t.',
  'Group the defining denominator only in the current layer.',
  '3.4, definition of rho_t',337),
 ('ASTRA-V-UNIT-DENOMINATOR-327',327,
  'The unit paragraph prints rho_t(1+t), soit1/1-t, with no denominator parentheses.',
  r'Current1/(1-t); diplomatic1/1-t.',
  'Group the unit denominator only in the current layer.',
  'unit paragraph before3.6',338),
 ('ASTRA-V-SLASH-329',329,
  '3.8.1 prints(1/1-t)^x without denominator parentheses.',
  r'Current(1/(1-t))^x; diplomatic(1/1-t)^x.',
  'Group the reciprocal denominator inside the current power expression.',
  '3.8.1 first equality',340),
]
for sid,p,printed,tex,change,region,witness in specs:
 r.own_finding(sid,p,printed,tex,change,proof,region,kind='notation',
  verdict='printed notation confirmed; current grouping amended after checkpoint08',witness=witness)
 r.own[-1]['amendment']='post-checkpoint08; supersedes prior current-retention decision where present'
r.patch(325,'current',r'\lambda_{t/1-t}',r'\lambda_{t/(1-t)}','ASTRA-V-SUBSTITUTION-325','Use the exact rho_minus substitution in the three inspected lambda subscripts.',count=3)
r.patch(325,'current',r'\gamma_{t/1+t}',r'\gamma_{t/(1+t)}','ASTRA-V-SUBSTITUTION-325','Use the exact inverse rho_plus substitution.')
r.patch(325,'current',r'\lambda_t(-1)=1/1+t',r'\lambda_t(-1)=1/(1+t)','ASTRA-V-SUBSTITUTION-325','Use the multiplicative inverse of lambda_t(1)=1+t.')
r.patch(326,'current',r'\rho_t(t)=t/1-t',r'\rho_t(t)=t/(1-t)','ASTRA-V-SUBSTITUTION-326','Group the denominator fixed by the preceding monomial expansion.')
r.patch(327,'current',r'soit \(1/1-t\)',r'soit \(1/(1-t)\)','ASTRA-V-UNIT-DENOMINATOR-327','Use rho_minus(1+t)=1/(1-t) for the transported unit.')
r.patch(329,'current',r'(1/1-t)^x',r'(1/(1-t))^x','ASTRA-V-SLASH-329','Use the reciprocal power identified by the adjacent exponential and rho substitution.')
packet={
 'record_type':'post_checkpoint_amendment','scope':[325,326,327,329],
 'after_checkpoint':'build/review_snapshots/expose_v_checkpoint08_through328/',
 'immutable_snapshot_modified':False,
 'source_ids':[x[0] for x in specs],
 'source_readings':[{'page':x[1],'printed_reading':x[2],'current_change':x[4]} for x in specs],
 'reason':proof,
 'counterchecks':[
  'In Z[[t]], the ungrouped ordinary-precedence expression t/1-t equals0; the intended t/(1-t) has t coefficient1 and is a substitution automorphism.',
  'In Z[[t]],1/1+t equals1+t under ordinary precedence; multiplication by1+t then gives1+2t+t^2, whereas1/(1+t) gives product1.',
  'The327 unit is1/(1-t), with t coefficient1; ordinary-precedence1/1-t is1-t, with t coefficient-1.',
  'At x=1 in329, exp(-Log(1-t))=1/(1-t), with t coefficient1, so the same reciprocal grouping is forced.'
 ],
 'evidence':'All four pages were fully compared before this amendment; native327 lower crop was reopened specifically for the unit reading.',
 'forms':'French current and corresponding corrected English; all diplomatic literal slash readings retained.'
}
(HERE/'amendment_after_checkpoint08_slash.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.commit()
