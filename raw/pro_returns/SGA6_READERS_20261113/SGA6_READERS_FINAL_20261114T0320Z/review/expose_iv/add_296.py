#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=296
r.finding('296_300',1,'The page begins (Bien entendu, pour Xi=Yi=S,…',
 'The opening parenthesis is the first character on this page in both scans, and is absent from the preceding page’s final display. The attached marker already agrees.',
 'first line',witness=307)
r.finding('296_300',2,'Xi=Yi=S, with dotted subscript i in both names.',
 'The native top crop directly compares the small dotted i with the flagged numeral 1 in n≥1 below. With both indexed schemes equal to S, the maps f_i are id_S and the tensor pairing of 3.3.3 specializes on the objects to the usual derived tensor of complexes on S. This identifies the displayed module structure without inserting a numerical subscript.',
 'opening parenthesis',witness=307)
r.finding('296_300',3,'Four raised round K dots; the single coherent-group mark is lower.',
 'All four high marks are round, as the native top crop shows; the apostrophe in d’anneau is a narrow separate tick. The attached K^{\\bullet} forms preserve these observed marks.',
 'opening paragraph, tensor-power display and final body line',witness=307)
r.finding('296_300',4,'BIBLIOGRAPHIE in typed capitals, with a lower rule.',
 'The main strip shows the capitals and their rule. The attached capitalized subsection title preserves the text under the accepted section-title convention.',
 'bibliography heading',witness=307)
for n,title in [(5,'Ein Theorem der Analytischen Garbentheorie ...'),(6,'Théorèmes de finitude pour la cohomologie des faisceaux'),(7,'Catégories dérivées')]:
 r.finding('296_300',n,title+' is plain typed text.',
  'The full bibliography and native crop show no underline or italic treatment of this title. The attached plain form matches; author names, case, dates, abbreviations and final punctuation were compared as printed.',
  'bibliography title',witness=307)
for id,name,target in [
 ('fixes/FIXLOG_6.jsonl#339','id','Id'),('fixes/FIXLOG_6_CURRENT.jsonl#304','id','Id'),
 ('fixes/FIXLOG_6.jsonl#340','Ob','Ob'),('fixes/FIXLOG_6_CURRENT.jsonl#305','Ob','Ob')]:
 r.source(id,'No printed '+target+' glyph on 296; the recorded change is an unprinted Exposé V macro reset.',
  'The source row changes providecommand to renewcommand in the Exposé V setup after the final Verdier bibliography entry and before the folio-297 marker. Code inspection confirms that it resets '+name+' to the operator '+target+'. This is a scoped implementation record, not a glyph verdict for 296 or a blanket verification of later usage. The full printed 296 ends at miméographié. and contains neither operator. Later occurrence-level checks remain attached to their actual usage pages; the first post-reset id use is at317, while no post-reset Ob body use is present in the supplied master.',
  'unprinted Exposé V setup after the bibliography',verdict='scoped implementation decision',page=p,
  change='Retain the existing macro reset; no printed-296 content patch. Carry actual usage verification to its later page.')
 r.decisions[-1]['record_type']='scoped_implementation'
 r.decisions[-1]['glyph_verification_claimed']=False
r.own_finding('ASTRA-IV-END-296',p,'Four body K marks, tensor exponent ⊗n, n≥1, bibliography labels [1], [2], [3], [V], and final word miméographié.',
 'The attached body, display and all four bibliography entries.',
 'Retain the fully compared page text.',
 'The ordinary rightward arrow in the tensor-power display has no tilde; the first exponent includes the tensor sign, while the target exponent is n alone. The whole bibliography preserves the source’s capital Analytischen, shortened Grauert title, n raised o5, numerical dates, pages 1–7 and literal [V]. No author footnote appears.',
 'complete body and bibliography',kind='symbol',verdict='confirmed',witness=307)
r.page(p,'(Bien entendu, pour Xi=Yi=S,…','[V] Verdier, J.-L., Catégories dérivées, IHES (1964), miméographié.',
 'Complete mathematical body and all bibliography entries compared, including the opening i subscripts, four raised K dots, lower K dot, tensor exponent, ordinary arrow, punctuation and labels. No author note. The subsequent TeX macro setup has no printed counterpart on this page and is recorded only as a scoped implementation decision.',
 witness='Native witness307 top and full bibliography regions; witness_296_top.png and witness_296_bibliography.png')
r.commit()
