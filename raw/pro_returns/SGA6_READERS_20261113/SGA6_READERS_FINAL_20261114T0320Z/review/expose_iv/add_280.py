#!/usr/bin/env python3
from review_helpers import Review, HERE
r=Review();p=280
for i,printed,reason,region in [
(9,'b) Le groupe K_•(_A X)_naïf…','The item label and Le begin this page. The attached marker now precedes the complete item; no boundary repair remains.','first item'),
(10,'supposé cohérent en tant que; cohérent underlined','Both images have a separate rule below cohérent. The inherited emphasis selects the correct word; the local patch gives its observed upright underlining.','2.4, first sentence'),
(11,"l’homomorphisme underlined before (2.4.2)",'The word has its own rule, while the display and reference remain independent.','2.4, assertion'),
(12,'défini par (2.4.1) est un isomorphisme.','Only the two lexical groups are underlined; the locator and final stop are plain.','after (2.4.2)'),
(13,'D(_A X) with underlined parf ↪ D^b(_A X)_coh','The lower rule belongs to parf alone. The explicit uparf form already reproduces this occurrence. The inclusion is the identity on the admitted perfect objects and their morphisms.','2.5, inclusion'),
(14,'Cependant, faisons les hypothèses suivantes :','The page ends at the colon. The attached enumeration opener contains no printed item text; the next item is after the next folio marker.','last two lines')]:
 r.finding('276_280',i,printed,reason,region,witness=291)
f=r.finding('276_280',6,'K with a raised round dot: one occurrence on 278, six on 279, and two on 280.',
 'All nine occurrences in the stated three-page scope were directly compared in both scans. The raised round mark is preserved as K^{\\bullet}; the adjacent apostrophe of d’un has its independently observed tick shape. This decision covers 278–280 only; subsequent IV pages are checked separately and are not inferred from these examples.',
 '278 §2 heading; 279 definition and remarks; 280 heading 2.5 and (2.5.1)',witness=289,
 change='Retain the attached raised-dot notation in these nine inspected occurrences.')
for row in r.decisions:
 if row['source_id']==f:
  row['image']='scan/SGA6_scan_360dpi.pdf#pages=292-294; scan/SGA6_witness_300dpi.djvu#pages=289-291'
id='ASTRA-IV-UNDERLINE-280'
r.own_finding(id,p,'2.4 and 2.5 have plain numbers, lexical title rules, and independently printed formulas; cohérent and the concluding assertion in 2.4 also have word rules.',
 'Inline headings are wholly bold; four lexical spans use emph.',
 'Use plain paragraph numbers and upright word underlining at these exact observed spans.',
 'Native witness 291 and main page 294 show the title rules ending before their stops; the K formula in the 2.5 title has no rule. No mathematical token, reference, or punctuation changes.',
 'headings 2.4/2.5 and four emphasis groups in 2.4',witness=291)
for old,new in [
 (r"\textbf{2.4. Cas d'un faisceau d'anneaux cohérent.}",r"2.4. \uline{Cas d'un faisceau d'anneaux cohérent}."),
 (r"\textbf{2.5. L'homomorphisme \(K^{\bullet}\to K_\bullet\).}",r"2.5. \uline{L'homomorphisme} \(K^{\bullet}\to K_\bullet\)."),
 (r'\emph{cohérent}',r'\uline{cohérent}'),
 (r"\emph{l'homomorphisme}",r"\uline{l'homomorphisme}"),
 (r'\emph{défini par}',r'\uline{défini par}'),
 (r'\emph{est un isomorphisme}',r'\uline{est un isomorphisme}')]:r.patch(p,'both',old,new,id,'Occurrence-specific observed word rules, with plain formulas and stops.')
r.page(p,'b) Le groupe K_•(_A X)_naïf…','les hypothèses suivantes :',
 'All prose, five-term vanishing chain, coproduct lower bound and shift, both inclusion arrows, references, and three numbered displays compared. Two raised K dots and all lower K dots checked. No author footnote on this page.',witness='Native witness 291 title, assertion, and lower formula region; review/expose_iv/witness_280_titles.png')
r.commit()
