#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=287
r.finding('286_290',10,'Cet homomorphisme est K^•(Y)-linéaire… begins 287.',
 'The displayed direct-image map (2.11.1.1) remains entirely on 286. Both attached markers agree with the directly inspected boundary.', 'page start',witness=298)
r.finding('286_290',11,'The map (2.11.1.1) on 286 has no terminal full stop.',
 'Both 286 images leave blank space after K_•(Y). The inherited deletion is verified at its actual page; its registry page reflects the former misplaced marker.', '286, last display',actual_page=286,witness=297)
r.finding('286_290',12,'formule and de projection underlined, with dite plain.',
 'Two separate rules are visible in the native top crop. The attached two emphasis spans select the correct letters and are rendered as explicit rules.', 'first paragraph',witness=298)
r.finding('286_290',13,'parf underlined in D(Y).',
 'The rule ends at the f of parf; the neighbouring comma is separate. The attached uparf preserves the observed occurrence.', 'before the derived projection formula',witness=298)
r.finding('286_290',14,'Two ordinary L capitals above the tensor symbols.',
 'Both symbols have a single upright stem and foot in the native crop. Retain the existing plain-L forms and the headless bar-with-tilde isomorphism sign.', 'projection isomorphism display',witness=298)
id='ASTRA-IV-O-287'
r.own_finding(id,p,'One O with a lower rule; X subscript outside.',r'\mathcal O_X',r'\underline{O}_X',
 'The native bottom crop distinctly shows the short rule under the structure-sheaf O.', 'last sentence, E=O_X',kind='font',witness=298)
r.patch(p,'both',r'\mathcal O_X',r'\underline{O}_X',id,'Observed structure-sheaf lower rule.')
id='ASTRA-IV-UNDERLINE-287'
r.own_finding(id,p,'formule / de projection separately underlined; 2.11.2 and 2.11.3 plain.',
 'Two emph groups; bold numbered paragraphs.', 'Use explicit word rules and plain paragraph numbers.',
 'Both source pages show plain dite and plain prose in 2.11.2–3, without a blanket statement rule.', 'first paragraph and numbered paragraphs',witness=298)
for s in ['formule','de projection']:r.patch(p,'both',r'\emph{'+s+'}',r'\uline{'+s+'}',id,'Exact lexical underline span.')
for s in ['2.11.2.','2.11.3.']:r.patch(p,'both',r'\textbf{'+s+'}',s,id,'Observed plain paragraph number.')
r.own_finding('ASTRA-IV-NOTATION-287',p,'Three raised K marks, four plain R letters in Rf_*, two plain derived-tensor L letters, and a headless horizontal bar below a tilde.',
 'Attached dot, R, L and simeq forms.', 'Retain the inspected forms.',
 'The native top crop resolves the isomorphism sign with no arrowhead and each L without added strokes. The lower crop and main page show no lower rule under the derived R letters. All displayed map orders and tensor subscripts agree.', 'projection formula and later pushforward discussion',kind='symbol',verdict='confirmed',witness=298)
r.page(p,'Cet homomorphisme est K^•(Y)-linéaire…','En fait, la définition (2.2) de K_•',
 'Complete prose, three numbered formulas, headless projection isomorphism, references, all covariant/contravariant marks and terminal continuation compared. No author footnote.',witness='Native witness 298 top projection and bottom structure-sheaf regions; witness_287_top.png and witness_287_bottom.png')
r.commit()
