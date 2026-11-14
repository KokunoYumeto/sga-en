#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=344
r.finding('341_345',18,'344 begins sur x,d ou le resultat;343 ends donc N0 sur N et X0.',
 'Both complete boundary images were directly compared. The supplied marker places the four initial words on344, matching the source.',
 '343/344 boundary',witness=355)
r.finding('341_345',19,'The second extended-operation target has subscript g followed by a closed downward triangle.',
 'The main third strip and native355 lower resolve both subscript characters. The triangle is the same multiplication marker as the first6.1 diagram and its restricted target. The supplied g-nabla subscript agrees.',
 'second display, gamma-prime target',witness=355)
r.finding('341_345',20,'The final completed Gr expression has a low dot after Gr, with the hat extending across that dot and the plus outside.',
 'Both main bottom strip and native355 lower resolve the dot and the hat endpoint. The supplied completed expression contains the required placeholder; its local low-dot glyph is restored separately.',
 'canonical morphism in final paragraph',witness=355)
r.own_finding('ASTRA-V-PLACEHOLDER-344',p,
 'The dot after Gr under its completion hat is a low period.',
 r'Use \widehat{\operatorname{Gr}\,\mathord{.}\,}^{+} at this occurrence.',
 'Preserve the observed low placeholder while retaining its hat scope.',
 'The native bottom crop shows the period at the lower edge of Gr, and the long hat covers it. This is the same individually inspected placeholder form as the earlier Gr occurrences; no macro-wide rule is applied.',
 'final completed graded functor',kind='symbol',witness=355)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-PLACEHOLDER-344','Preserve the low graded-functor placeholder inside the existing hat.')
r.own_finding('ASTRA-V-BINOMIAL-344',p,
 'The first section6 paragraph prints binomial with a circumflex on its o: binomial spelled binômial.',
 'Diplomatic binômial; current binomial.',
 'Remove this lexical circumflex in the corrected form.',
 'Main first strip and native355 top clearly show the small circumflex. The same base ring K is explicitly identified with2.7, where the binomial operation uses the identical integer-valued binomial polynomials. The map on the named ring and all its operations is the identity; only this adjective spelling is corrected.',
 'first paragraph of section6',kind='misprint_in_print',witness=355)
r.patch(p,'current','anneau binômial (2.7)','anneau binomial (2.7)','ASTRA-V-BINOMIAL-344','Repair only the observed adjective spelling.')
r.own_finding('ASTRA-V-FORMS-344',p,
 'Three category C forms are script, the last with typed lower o; the final category G has a connected descending tail. Five multiplication markers are closed downward triangles. The paragraph label6.1 is plain.',
 r'Retain \mathcal C, \mathcal C_0, \mathcal G and the five \nabla occurrences; replace \textbf{6.1.} by6.1.',
 'Keep the inspected category/operation forms and restore the ordinary paragraph number.',
 'Native355 top/lower resolves each script category and triangle. The C_o index follows the previously stated o/0 transcription convention. The two first-diagram markers, prose marker and two extended-diagram markers are all closed triangles, unlike the separately retained Latin v on326. The functor restriction is explicitly G-hat composed with i:C0→C, so no unrelated object identification is introduced.',
 'section6 notation paragraph and both6.1 operation diagrams',kind='convention',witness=355)
r.patch(p,'both',r'\textbf{6.1.}',r'6.1.','ASTRA-V-FORMS-344','Preserve the ordinary numbered paragraph.')
r.own_finding('ASTRA-V-AUTHOR-CLAIM-CONTINUATION-344',p,
 'The opening sentence concludes5.7 by saying the homomorphism is compatible with the filtrations.',
 'Retain the source sentence and link the exact343 counterexample and failed augmentation map.',
 'Record the dependent continuation at its actual source page.',
 'The complete main/native top line confirms this literal conclusion. In the already documented example, f sends U=N-prime_0 to-1 and the universal value gamma^2(N0,1)=-U in Fil^1A0 to1 outside Fil^1Z. Thus this exact filtration-compatibility conclusion fails for the printed unrestricted data. The coordinator independently confirmed the absence of an epsilon(N)=d condition and the counterexample. Full packet: author_claim_issue_343.json.',
 'opening continuation of5.7 proof',kind='author_claim_issue',verdict='source retained; linked transfer defect demonstrated',witness=355)
issue=json.loads((HERE/'author_claim_issue_343.json').read_text())
issue['independent_review']='Coordinator read338,340,343 and confirmed the printed hypotheses, the K=A=Z,N=0,d=1,x=1,p=2 counterexample and the failed augmentation compatibility; advised retaining the statement and sign-aware proof defect without isolated prime changes.'
issue['continuation_344']={
 'image':['scan/SGA6_scan_360dpi.pdf#page=358','scan/SGA6_witness_300dpi.djvu#page=355'],
 'region':'complete first line',
 'printed':'sur x,d ou le resultat,l homomorphisme etant compatible aux filtrations.',
 'source_id':'ASTRA-V-AUTHOR-CLAIM-CONTINUATION-344',
 'disposition':'Retain the exact sentence with the already demonstrated image f(-U)=1 outside Fil^1Z.'
}
(HERE/'author_claim_issue_343.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.page(p,'sur x,d ou le resultat','foncteurs sur script G:',
 'Full main358 strips and native355 top/lower compared. Checked the343 proof continuation, section6 title without terminal stop, literal binomial circumflex, three script C forms and final script G, ordinary6.1, every G-hat/t/u/g index, seven headed arrows, all five closed triangle markers, two gamma-prime labels, P/Q primes and R_(n,a), every comma/semicolon, final completed Gr low dot and hat scope, and the final colon. No author note or additional lexical body rule.',
 witness='Native355 top/lower: witness_344_top.png and witness_344_lower.png.')
r.commit()
