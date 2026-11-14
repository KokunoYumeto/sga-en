#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=309
r.finding('306_310',11,'1+…+ā_n+… has two baseline three-dot groups, on the first line of actual page 309.',
 'The main first strip and native top crop resolve both baseline groups and the separate bar over a_n. The finding was listed at nominal308 before its page-marker repair; the attached series now stands correctly on309 and already uses ldots.',
 'first printed line of actual309',witness=320,actual_page=309)
r.finding('306_310',15,'la série 1+…+ā_n+…, où… begins the page; Son noyau follows on this same page.',
 'Both complete page-309 scans begin with la série, following the final comma on308. The attached marker now precedes exactly those words.',
 'page start',witness=320)
for n,region in [(16,'middle term of the composite defining ρ'),(17,'canonical map after that composite'),(20,'canonical map in the factorization paragraph')]:
 r.finding('306_310',n,'Gr followed directly by a baseline placeholder dot under the completion hat, without argument parentheses.',
  'The native lower crop shows the letters Gr and a baseline full-stop-shaped placeholder under one hat. There are no parentheses around that placeholder. The attached removal of the extra argument parentheses agrees. The inherited note leaves the dot at cdot height; its actual baseline height is separately restored by ASTRA-V-PLACEHOLDER-309 at all six inspected occurrences.',
  region,verdict='parenthesis repair confirmed; placeholder-height treatment amended',witness=320)
r.finding('306_310',18,'The sentence after the composite ends at the completed Gr-placeholder expression, without a final full stop.',
 'The native lower crop has only the placeholder dot under the hat; there is no additional stop after the superscript plus. The attached punctuation agrees.',
 'before On va construire',witness=320)
for n,printed,region in [(19,'On va construire… begins a new paragraph.','after the unpunctuated canonical map'),(21,'Soient A… begins a new paragraph.','after d’après1.11.')]:
 r.finding('306_310',n,printed,
  'The native lower crop confirms the indentation and paragraph break. The attached layout already agrees, without any additional change to words, formulas or punctuation.',
  region,verdict='formatting observed; no content error',witness=320)
r.own_finding('ASTRA-V-ABFIL-309',p,'Ab fil is separately underlined in all three lemma occurrences: the target of H and the two Hom subscripts.',
 r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}} in these three occurrences.',
 'Render these three inspected category names explicitly.',
 'The native top crop resolves each of the six word rules, without dots. These are the three 309 occurrences listed by checker306_310#6; no global macro is changed.',
 'Lemme1.12 and its display',witness=320)
r.patch(p,'both',r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}','ASTRA-V-ABFIL-309','Preserve the three observed category-name forms.',count=3)
r.own_finding('ASTRA-V-UNDERLINE-309',p,'Soit, un foncteur sur, alors l’homomorphisme canonique, and est un isomorphisme are separately underlined.',
 r'\uline on these four lexical spans only.',
 'Render the four inspected lemma word rules.',
 'The native top crop shows those exact lexical spans, with formulas, semicolon, colon and final stop outside. All surrounding proof prose is plain. This is the 309 statement named in checker306_310#5.',
 'Lemme1.12',witness=320)
r.patch(p,'both',r"\textbf{Lemme 1.12.} Soit \(H:\mathcal G\to\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}\) un foncteur sur \(\mathcal G\)~; alors l'homomorphisme canonique~:",r"\textbf{Lemme 1.12.} \uline{Soit} \(H:\mathcal G\to\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}\) \uline{un foncteur sur} \(\mathcal G\)~; \uline{alors l'homomorphisme canonique}~:",'ASTRA-V-UNDERLINE-309','Preserve the initial three inspected word groups.')
r.patch(p,'both','est un isomorphisme.',r'\uline{est un isomorphisme}.','ASTRA-V-UNDERLINE-309','Preserve the concluding word rule and plain final stop.')
r.own_finding('ASTRA-V-PLACEHOLDER-309',p,'All six completion-placeholder dots are typed full-stop shapes on the baseline, including the three after Gr.',
 r'\,\mathord{.}\, replaces \,\cdot\, in the six inspected completion placeholders.',
 'Restore baseline height while keeping each placeholder under its original completion hat.',
 'The native top crop resolves the first standalone placeholder. The lower crop resolves two more standalone placeholders and the three Gr-placeholder forms. Their dots align with ordinary full stops rather than the plus-sign midline. The replacement represents the same unspecified functor argument with a baseline dot; it changes neither the functor compositions nor their Hom source/target pairs.',
 'six completion placeholders throughout the page',kind='symbol',witness=320)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-PLACEHOLDER-309','Preserve the six observed baseline placeholder dots.',count=6)
r.own_finding('ASTRA-V-G-309',p,'Both lemma category letters have the script G descender, faintly broken in the first occurrence.',
 r'\mathcal G in the two lemma occurrences.',
 'Retain the two inspected script G forms.',
 'The main first category descender is faint; the native top crop resolves its small remaining downward curve, matching the fuller connected descender in the second occurrence and the six examples inspected on308. These are the two 309 usage points listed in checker306_310#14. The category in Ob(C) at the bottom remains the printed looping script C.',
 'two lemma category letters and final Ob(C) comparison',kind='font',verdict='confirmed',witness=320)
r.page(p,'la série 1+…+ā_n+…, où…','Soient A∈Ob(C), χ∈Ĝ′(A) ; on définit un homomorphisme de',
 'Complete kernel condition with i+1 and both semicolons, quotient isomorphism and final stop, lemma and all word/category rules, definition of ρ, inverse map ρ′, all six completion placeholders, every arrow and punctuation mark, and final χ/Ĝ′ forms compared. No author note.',
 witness='Native witness320 top and lower crops; witness_309_top.png and witness_309_lower.png')
r.commit()
