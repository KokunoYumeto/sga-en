"""Regional glyph rechecks after the folio181 literal-rule integration decision.

Run after the original page-specific add scripts. Each locus below was reopened
in the main scan and the named witness; no new page-completion claim is added.
"""
from review_helpers import Review
r=Review()
rule=r'\underline{\underline{R}}'
for batch,index,page,region,witness in [
 ('166_170',12,167,'First RHom expression in Remark2.1.3.1(iii)',178),
 ('166_170',13,167,'Second RHom expression in the same display',178),
 ('171_175',13,175,'Inline RΓ_S in Remark2.2.10(a)',186),
 ('181_185',7,182,'Inline RΓ_S in Proposition2.4.5(c)',193),
 ('181_185',8,182,'Following RΓ_S display',193),
 ('181_185',9,182,'RΓ_S label on the final arrow in the proof factorization',193)]:
 r.finding(batch,index,'R with two separate horizontal rules below the letter',
 'The exact locus was reopened in both scans. Two horizontal lower rules are visible. Preserve those two rules literally at this occurrence; every argument, map and degree is unchanged.',
 region,verdict='amended',change=rule+' at this inspected occurrence; the earlier mathbb representation is replaced.',witness=witness)
for page,count,witness,region in [(167,2,178,'The two RHom expressions in Remark2.1.3.1(iii)'),(175,1,186,'The inline derived global-sections functor'),(182,3,193,'The inline functor, following display, and arrow label')]:
 sid=f'ASTRA-II-R-{page}';reason=f'The {count} specified R occurrence(s) were reopened in the main scan and native witness. Each has two distinct horizontal rules beneath R. The replacement is restricted to these observed letters and preserves their original mathematical units.'
 r.own_finding(sid,page,f'{count} literal double-underlined R occurrence(s)',r'\mathbb R',rule,reason,region,kind='font',witness=witness)
 r.patch(page,'both',r'\mathbb R',rule,sid,reason,count)
for index,region in [(2,'First diagram, right vertical-arrow label'),(3,'Second diagram, right vertical-arrow label')]:
 r.finding('176_180',index,'R has a doubled vertical stem in the diagram label',
 'The main scan and native witness show the second vertical stroke adjoining R. The witness crop includes both labels. Keep their attached mathbb R forms. The earlier comparison to the lower-rule glyph on175 is amended by this occurrence-specific observation.',
 region,verdict='confirmed with amended rationale',change='Retain mathbb R in this directly observed diagram label.',witness=187)
sid='ASTRA-II-E-172';reason='All six affine-plane E letters were reopened in both scans, including the E inside the structure-sheaf subscript. Each letter has two separate horizontal lower rules. Preserve those literal strokes with underline{underline{E}}, leaving every exponent2, index k, section functor, restriction arrow and origin label unchanged.'
r.own_finding(sid,172,'Six E letters with two horizontal rules below E',r'\mathbb E',r'\underline{\underline{E}}',reason,'Doubled-origin example, all six plane symbols',kind='font',verdict='amended',witness=183)
r.patch(172,'both',r'\mathbb E',r'\underline{\underline{E}}',sid,reason,6)
sid='ASTRA-II-R-184';reason='The R in the real-coordinate space R^n was reopened in both scans. Its lower marks are two horizontal rules below the letter. Preserve those rules literally and leave the exponent n, real analytic equations, cited reference and the named space unchanged.'
r.own_finding(sid,184,'Real-coordinate R with two horizontal lower rules',r'\mathbb R',rule,reason,'Proposition2.4.8, real-coordinate space R^n',kind='font',witness=195)
r.patch(184,'both',r'\mathbb R',rule,sid,reason)
r.commit()
