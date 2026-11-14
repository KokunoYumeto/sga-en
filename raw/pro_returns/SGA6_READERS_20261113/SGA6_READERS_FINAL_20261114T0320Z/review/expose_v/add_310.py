#!/usr/bin/env python3
from review_helpers import Review, HERE
r=Review();p=310
r.finding('306_310',22,'The page begins K-algèbres filtrées; page309 ends un homomorphisme de.',
 'The complete main and witness310 begin with K-algèbres; the previously inspected end of309 has neither K nor a hyphen after de. The attached boundary agrees.',
 'page start',witness=321)
r.finding('306_310',23,'The series 1+X₂t+…+Xₙ₊₁tⁿ+… uses two baseline three-dot groups.',
 'The native top crop resolves three separate low dots in each group and the following separate sentence stop. The attached ldots reading already agrees.',
 'first paragraph, after pour l’élément',witness=321)
r.finding('306_310',24,'The completion hat covers Gr followed directly by a baseline dot, without argument parentheses.',
 'The native lower crop resolves Gr and its low placeholder dot. The attached deletion of argument parentheses agrees; the inherited cdot height is amended separately by ASTRA-V-PLACEHOLDER-310.',
 'Par passage au quotient paragraph',verdict='parenthesis repair confirmed; placeholder-height treatment amended',witness=321)
r.finding('306_310',25,'Page310 ends sur l’élément; page311 begins 1+X de 1+completed K[X]⁺ est injective.',
 'The complete310 lower strip and native lower crop end at élément. The first main311 strip was separately read to verify the following mathematical expression and est injective. The attached boundary agrees. That311 regional check alone is not a full-page verdict.',
 'page end and following page first line',witness=321)
r.own_finding('ASTRA-V-ABFIL-310',p,'The sole Ab fil subscript has separate rules under Ab and fil, without full stops.',
 r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}} in the theorem Hom subscript.',
 'Render the inspected category name explicitly.',
 'Both scans resolve the two rules in the Hom subscript. This is the single310 occurrence in checker306_310#6; the patch is local to this page.',
 'Théorème1.13',witness=321)
r.patch(p,'both',r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}','ASTRA-V-ABFIL-310','Preserve the inspected category-name rules.')
r.own_finding('ASTRA-V-UNDERLINE-310',p,'The theorem underlines its lexical groups, leaving H, script G, the Hom expression, H(K[X]), commas and final punctuation independently plain.',
 r'\uline on each inspected lexical group of the310 theorem opening.',
 'Render the observed theorem word rules.',
 'The native lower crop shows Soit; un foncteur sur; à valeurs dans la catégorie des groupes abéliens filtrés séparés complets; et commutant aux invariants sous un groupe fini; Alors l’application de; dans; qui; à un morphisme de foncteurs; and associe sa valeur sur l’élément. The punctuation separating these groups lies outside the rules. All proof prose above is plain.',
 'Théorème1.13 through page end',witness=321)
old=(HERE/'page_310_diplomatic.tex').read_text().split(r'\textbf{Théorème 1.13.} ',1)[1].rstrip()
old=old.replace(r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}')
new=r"\uline{Soit} \(H\) \uline{un foncteur sur} \(\mathcal G\), \uline{à valeurs dans la catégorie des groupes abéliens filtrés séparés complets}, \uline{et commutant aux invariants sous un groupe fini}. \uline{Alors l'application de} \(\Hom_{\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}}(1+\widehat{\,\cdot\,}^{+},H)\) \uline{dans} \(H(K[X])\) \uline{qui}, \uline{à un morphisme de foncteurs}, \uline{associe sa valeur sur l'élément}"
r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-310','Preserve the complete inspected lexical grouping.')
r.own_finding('ASTRA-V-PLACEHOLDER-310',p,'All three completion-placeholder dots lie on the baseline: one after Gr and two standalone.',
 r'\,\mathord{.}\, replaces \,\cdot\, in these three completion expressions.',
 'Restore the observed baseline placeholder height.',
 'The native lower crop resolves all three low dots under their completion hats. The dot denotes the same unspecified functor argument before and after this typography repair; the maps remain 1+completed Gr(.)⁺→H∘Gr and 1+completed(.)⁺→H, with the same source in the theorem Hom expression.',
 'quotient paragraph and theorem Hom expression',kind='symbol',witness=321)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-PLACEHOLDER-310','Preserve the three observed baseline dots.',count=3)
r.own_finding('ASTRA-V-G-310',p,'The theorem category is a single script G with a connected descender; both universal φ glyphs above have the open upper-left form.',
 r'\mathcal G in the theorem; \varphi in the two proof occurrences.',
 'Retain these inspected handwritten forms.',
 'The native lower crop resolves the connected loop and descender of the category letter, matching the nine individually inspected forms on308–310. The native top crop also resolves the open-left universal-element glyphs in the proof. The final stop after résultat is a single baseline period, clearly resolved by the witness.',
 'theorem category and proof glyph comparison',kind='font',verdict='confirmed',witness=321)
r.finding('306_310',5,'All statement lexical groups on306–310 are separately underlined, with their mathematical expressions and separating punctuation independently plain.',
 'The complete pages306–310 have now been compared individually in both scans. The lemma begins306 and ends307; the theorem begins307 and ends308; lemma1.12 is on309; theorem1.13 begins310. The exact lexical spans are preserved by the local patches and own findings on those five pages. No uninspected page is included in this aggregate scope.',
 'inspected statement spans on306–310',verdict='confirmed and applied at inspected occurrences',change='Use the exact local word-rule patches recorded on306–310.',witness=321)
r.finding('306_310',6,'All nine Ab fil names on306–310 have two separate word rules and no stops: counts3,1,1,3,1 by page.',
 'Every occurrence was directly inspected: three on306, one on307, one on308, three on309 and one on310. The exact local patches preserve each form. The proposed global macro change is replaced by occurrence-specific rendering; occurrences outside this fully inspected scope are not decided by this record.',
 'the nine inspected category names on306–310',verdict='local glyph repair confirmed; global implementation amended',change='Use the nine exact local replacements rather than redefine the category macro globally.',witness=321)
for row in r.decisions:
 if row['source_id'] in ['check/findings/findings_306_310.json#5','check/findings/findings_306_310.json#6']:
  row['image']='; '.join(f'scan/SGA6_scan_360dpi.pdf#page={q+14}; scan/SGA6_witness_300dpi.djvu#page={q+11}' for q in range(306,311))
r.page(p,'K-algèbres filtrées K[X_i]_{i≥1}→A en envoyant X₁ sur0','associe sa valeur sur l’élément',
 'The full first paragraph, all series indices and bounds, four headed arrows and their labels in the square, its final semicolon, Gr(f)=Gr(f₁), both universal-element glyphs, the period after résultat, the quotient maps, all three baseline placeholders, ρ/ρ′, theorem words and exact underline spans compared. No author note.',
 witness='Native witness321 top and lower crops; witness_310_top.png and witness_310_lower.png')
r.commit()
