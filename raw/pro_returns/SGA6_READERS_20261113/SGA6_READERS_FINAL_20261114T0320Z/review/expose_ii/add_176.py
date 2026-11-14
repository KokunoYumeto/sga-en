"""Folio176: two comparison diagrams and the opening of soft sheaves."""
from review_helpers import Review
r=Review()
r.finding('176_180',1,'la sous-catégorie triangulée begins the page',
    'The article la belongs to the first printed line, after the preceding folio ends est. Both attached markers already preserve that boundary.',
    'First printed line',change='Retain the existing boundary before la.')
for n,region in [(2,'Upper comparison diagram, right vertical arrow'),(3,'Lower comparison diagram, right vertical arrow')]:
    r.finding('176_180',n,'Double-marked R in the right vertical RΓ_S label',
        'The derived-functor R carries doubled strokes. The attached mathbb R preserves that form; the other vertical labels are ordinary Γ_S. All arrows and source/target indices were compared.',region)
reason='The phrase is printed à cohomologique bornée. The preposition à requires the noun cohomologie, as already used in the first paragraph of this same page. Current already restores that noun while leaving the boundedness and pseudo-coherence conditions unchanged; diplomatic retains the printed adjective.'
r.finding('176_180',4,'à cohomologique bornée',reason,'Remark2.2.10(b)',change='Retain the existing current cohomologie and diplomatic cohomologique.')
for source in ['fixes/RECONCILE_CODEX_6.json#237','fixes/FIXLOG_6_CURRENT.jsonl#354']:
    r.source(source,'à cohomologique bornée',reason,'Remark2.2.10(b)',page=176,change='Retain the existing corrected noun cohomologie.')
r.finding('176_180',5,'[T.F]. with the full stop after the closing bracket',
    'The bracketed citation has no full stop after F inside the bracket; the sentence stop follows it. Both attached layers match.',
    'Opening sentence of2.3.1')
sid='ASTRA-II-O-176';reason='The single sheaf O in Remark2.2.10(b) has a rule under the letter alone.'
r.own_finding(sid,176,'One underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'Remark2.2.10(b)',kind='font')
r.patch(176,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-NUMBER-176';reason='The paragraph number2.3.1 is typed plainly; it is separate from the accepted statement-label heading convention. Preserve its ordinary weight at this inspected occurrence.'
r.own_finding(sid,176,'Plain paragraph number2.3.1',r'\textbf{2.3.1.}','2.3.1.',reason,'First paragraph of§2.3',kind='font')
r.patch(176,'both',r'\textbf{2.3.1.}','2.3.1.',sid,reason)
sid='ASTRA-II-UNDERLINE-176';reason='The newly defined word mou alone has a rule. The surrounding definitions and discussion are plain. Its existing emphasis group has exactly the observed scope.'
r.own_finding(sid,176,'Only the defined word mou is underlined',r'\emph{mou}',r'\uline{mou}',reason,'Definition of a soft sheaf',kind='underline')
r.patch(176,'both',r'\emph{mou}',r'\uline{mou}',sid,reason)
r.page(176,'la sous-catégorie triangulée','défini par I=H^0(X,F) est un épimorphisme.',
    'The complete remark continuation, both commutative diagrams with all labels and commas, and all of2.3.1 were compared. The definition of mou and the final indexed free-module map were individually inspected.')
r.commit()
