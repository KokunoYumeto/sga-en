#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=313
r.finding('311_315',16,'Considérons maintement le morphisme canonique is printed in both scans.',
 'The main first strip and native top crop resolve maintement. The sentence uses the temporal adverb maintenant; the inherited corrected layer still carries the typist’s omission/substitution. Preserve the printed spelling diplomatically and restore maintenant in the corrected layer.',
 'first paragraph, second sentence',verdict='not applied and now applied',change={'diplomatic':'maintement','current':'maintenant'},witness=324)
r.patch(p,'current','Considérons maintement le morphisme canonique','Considérons maintenant le morphisme canonique','check/findings/findings_311_315.json#16','Apply the independently confirmed printed-spelling correction only in the corrected layer.')
regions={17:'first canonical morphism H→1+completed Gr(.)⁺',18:'composite morphism from Ĝ^k',19:'factorization through the kth power',20:'comparison of nth universal polynomials',21:'additive-example morphism H→completed Gr(.)⁺',22:'composition identity in the additive example'}
for n,region in regions.items():
 r.finding('311_315',n,'Gr is followed directly by a baseline placeholder dot under the completion hat.',
  'This exact occurrence was read in the main strip and native top crop. The inherited restoration of its missing placeholder agrees with the scan. Its cdot height is amended by the local twelve-occurrence placeholder record, which also checks each standalone placeholder on this page.',
  region,verdict='placeholder restoration confirmed; height treatment amended',witness=324)
r.own_finding('ASTRA-V-PLACEHOLDER-313',p,'The twelve completion-placeholder dots all sit on the baseline: six directly after Gr and six standalone.',
 r'\,\mathord{.}\, replaces \,\cdot\, in the twelve inspected occurrences.',
 'Restore all twelve observed baseline dots.',
 'The native top crop resolves the ten placeholders in the first paragraph and additive-example paragraph, including both sides of the compositional identity and the separately named standalone functor. It also shows the first Todd-example occurrence; the lower crop resolves the final one. Each dot stays under its existing hat, with its original plus and any kth power. These are identical unspecified arguments before and after the height repair; no source, target or composition is altered.',
 'all completion expressions on313',kind='symbol',witness=324)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-PLACEHOLDER-313','Preserve the twelve individually inspected low dots.',count=12)
r.own_finding('ASTRA-V-FONT-313',p,'K=Q uses an ordinary typed single-outline Q; the integer-ring Z below has a doubled diagonal. The additive-example category G has its connected descender, while the two final C_o forms have a separate lower o. The number1.16. is plain.',
 r'Render the one \mathbb Q as Q and1.16. without bold; retain \mathbb Z, \mathcal G and the two \mathcal C_0 forms.',
 'Restore the observed plain Q and paragraph number while preserving the other inspected forms.',
 'The tight witness_313_Q.png crop resolves the ordinary Q outline without a second stem. The native lower crop resolves the doubled Z diagonal and both C_o forms; the top crop resolves the sole script G descender. The font repair keeps the example’s coefficient identification q↦q on the rational field declared K=Q, and leaves the Todd series unchanged. The section-title underline is handled by the accepted heading convention; the running text and character name are plain.',
 '1.16, additive example and final paragraph',kind='font',witness=324)
r.patch(p,'both',r'\mathbb Q','Q','ASTRA-V-FONT-313','Preserve the observed plain Q at this occurrence.')
r.patch(p,'both',r'\textbf{1.16.}','1.16.','ASTRA-V-FONT-313','Preserve the inspected plain paragraph number.')
r.page(p,'Supposons en particulier que H=Ĝ','la restriction de Ĝ à C_o (1.10).',
 'Complete first-paragraph factorization and all capital Φ occurrences, weight<n and weight n statements, additive-example identity and product i≥1, all twelve completion placeholders, plain Q, complete Todd quotient X/(1−e^(−X)) with its final stop, both theorem-condition references, section title punctuation, doubled Z, exception2.9, and both final C_o restrictions compared. No author note.',
 witness='Native witness324 top/lower crops and tight Q crop; witness_313_top.png, witness_313_lower.png, witness_313_Q.png')
r.commit()
