#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=340
r.finding('336_340',13,'340 begins B qui envoie;339 ends de A dans.',
 'Both complete boundary images were compared. The supplied marker now leaves B qui at the start of340 and the unfinished preposition at the end of339, matching the physical pages.',
 '339/340 boundary',witness=351)
r.finding('336_340',14,'The first-line word is remarque with an overtyped fifth letter: an r shoulder and foot remain, with an extra taller stem above.',
 'The native tight remarque crop and nearest-neighbour zoom resolve the r shape and the protruding overtyped stem. The main scan shows the same dark overlap. Retain the corrected typed reading remarque and record the physical overstrike; do not restore the overwritten t as a separate character.',
 'first line, remarque',witness=351)
r.finding('336_340',15,'The first three-line display ends with lambda_(minus1)N and no terminal punctuation.',
 'Both main second strip and native351 top show blank space after N. The supplied absence of the former full stop agrees.',
 '5.4 first display end',witness=351)
r.finding('336_340',16,'Comme begins a new indented paragraph after that display.',
 'Both scans show the same gap and indentation. The supplied paragraph break agrees; this is a recorded layout observation without a new content error.',
 'before Comme l anneau',verdict='formatting observed; no content error',witness=351)
r.finding('336_340',17,'The source literally prints on en desuit, with s in the verb.',
 'The main second strip and native351 top clearly resolve desuit. The preceding identity has a common nonzero polynomial lambda_(minus1)(N) in the universal integral polynomial ring; its cancellation gives the displayed5.4.1 identity. The sentence therefore says that one deduces the relation: preserve desuit diplomatically and correct only this verb to deduit in current.',
 'paragraph introducing5.4.1',verdict='confirmed and now applied in current',change='Current désuit becomes déduit; diplomatic retains désuit.',witness=351)
r.patch(p,'current','on en désuit la relation','on en déduit la relation','check/findings/findings_336_340.json#17','Repair the observed verb while keeping the exact cancellation argument.')
r.finding('336_340',18,'Considerons maintenant begins a new indented paragraph after5.4.1.',
 'The main third strip and native351 lower resolve its indentation and preceding gap. The supplied separation agrees with no changed mathematical tokens.',
 'after5.4.1',verdict='formatting observed; no content error',witness=351)
r.own_finding('ASTRA-V-LOW-DOTS-340',p,
 'Eighteen low product dots: seven in the first display, two in5.4.1, two in the next displayed identity, one in the inline lambda-minus-one product, and six in the final two-line display.',
 r'Use \mathbin{.} for these eighteen product marks.',
 'Preserve every observed low mark and all surrounding factors.',
 'Each of the listed regions was compared in the main strips and native351 top/lower. The marks consistently align beside the lower letter contours, below the equality bars. The final stops remain independent punctuation.',
 'all mathematical product dots on340',kind='symbol',witness=351)
r.patch(p,'both',r'\cdot',r'\mathbin{.}','ASTRA-V-LOW-DOTS-340','Preserve the eighteen inspected low product marks.',count=18)
r.own_finding('ASTRA-V-PARAGRAPH-LABEL-340',p,
 'The label5.4 is ordinary unruled type.',
 r'5.4. rather than \textbf{5.4.}.',
 'Restore the inspected numbered-paragraph form.',
 'Main first strip and native351 top show its ordinary weight and absent rule; the surrounding prose is also unruled.',
 '5.4 label',kind='convention',witness=351)
r.patch(p,'both',r'\textbf{5.4.}',r'5.4.','ASTRA-V-PARAGRAPH-LABEL-340','Preserve the ordinary paragraph label.')
r.page(p,'B qui envoie N sur N-double-prime','lambda^p(N-prime,x.lambda_(minus1)(N)).lambda_(minus1)(N-prime).',
 'Four complete main354 strips and native351 top/lower compared word and symbol. Checked339/340 boundary, the overtyped remarque in a tight native zoom, every double-prime and finite-degree bound, both reinforced Z letters, all eighteen low dots, the two nonzero-index conditions, absent first-display stop and present later stops, literal desuit, ordinary5.4, N/N-prime in every final factor and the last full stop. No author note or underlined body span.',
 witness='Native351 top/lower and witness_340_remarque.png with its nearest-neighbour zoom.')
r.commit()
