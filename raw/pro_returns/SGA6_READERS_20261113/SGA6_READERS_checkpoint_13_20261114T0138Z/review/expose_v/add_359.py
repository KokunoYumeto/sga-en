#!/usr/bin/env python3
from review_helpers import Review,read
r=Review();p=359
r.finding('356_360',15,'Ces relations starts an indented paragraph at the page top.',
 'Main373 first strip and native370 top show the indent after the358 relations. The supplied blank line below the marker already agrees.',
 '358/359 paragraph boundary',witness=370)
r.finding('356_360',16,'The product of the gamma powers of the x_j ends =0 followed by a semicolon.',
 'Native370 lower resolves both the upper dot and descending lower stroke of the semicolon. The attached semicolon is exact. Its four-point internal product ellipsis is separately restored with the other extended groups.',
 'Or par hypothese display ending',witness=370)
r.finding('356_360',17,'The word entraine has a dotted i and no circumflex.',
 'Both scans show the dot over i. The current lexical repair to entraine with a circumflex follows the stated corrected spelling convention already applied to the same verb in this review. The mathematical implication is unchanged:the degree-M coefficient of the gamma product is mapped to its stated zero relation.',
 'ceci entraine',verdict='not applied and now applied',change='Current entraîne;diplomatic entraine.',witness=370)
r.patch(p,'current','ceci entraine','ceci entraîne','check/findings/findings_356_360.json#17','Restore the lexical circumflex in current only.')
r.finding('356_360',18,'The final sentence prints propriete universelle de Omega applique,with no final feminine e.',
 'Both lower source views show applique. Its grammatical subject is the feminine propriete universelle;current appliquee supplies the agreement. The same universal map Omega→Gr of the named ring is induced by the completed-class theory,by sending each generator c^i(x) to the corresponding graded class. This map and the following diagram are unchanged by the agreement repair.',
 'last sentence,applique',verdict='not applied and now applied',change='Current appliquée;diplomatic appliqué.',witness=370)
r.patch(p,'current',r'\Omega\) appliqué à',r'\Omega\) appliquée à','check/findings/findings_356_360.json#18','Restore agreement with the feminine propriete universelle.')
wedge_reason=('Actual359 has six algebra-name wedges:the first map,the theory-value sentence,the Fil^1 coefficient clause,the discrete-filtration hypothesis,the Fil^n zero condition,and the x-list Fil^1 condition. All are directly resolved as unadorned small wedges in the native top crop. The historical checker count of eight belongs to its old page split;the bottom diagram is physically on360. The notation map to the attached Lambda name is the identity on the augmented ring,on its coefficient classes and on the universal theory maps. No later diagram glyph is counted as359 evidence.')
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_356_360.json#2').copy()
aggregate.update(verdict='actual356–359 scope decided;360 pending',
 printed_reading='Actual356–359 contain respectively10,7,15,6 small serifless algebra-name wedges.',
 change=r'Use occurrence-scoped \mathord{\wedge} replacements on356–359 only;actual360 awaits direct comparison.',
 region='all actual356–359 algebra-name glyphs')
aggregate['reason']+=' '+wedge_reason
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=373; scan/SGA6_witness_300dpi.djvu#page=370'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-WEDGE-359',p,
 'The six actual359 algebra-name signs are unadorned small wedges.',r'Use six \mathord{\wedge} glyphs.',
 'Preserve the actual-page glyphs and unchanged named algebra.',
 wedge_reason,'six algebra-name occurrences in the first two paragraphs',kind='symbol',witness=370)
r.patch(p,'both',r'\Lambda',r'\mathord{\wedge}','ASTRA-V-WEDGE-359','Preserve the six actual359 algebra-name glyphs.',count=6)
r.own_finding('ASTRA-V-ELLIPSES-359',p,
 'The first Chern-class product,the following gamma product,and the product after applying tilde-c0 each have four low dots. The remaining coefficient tail,index sums,and final factorial-product ellipsis have three low dots.',
 r'Preserve the three extended groups as \mathinner{....} in both forms;use \ldots for the four remaining centered controls.',
 'Restore the observed point counts and baseline heights without shortening the source extended product abbreviations.',
 'The native top/lower resolve four distinct evenly spaced ink points in each of the first three product groups;the last product below entraine has three. Every group abbreviates the same ordered product over j=1,...,p,so this graphical mapping changes no factor,order or operation. Source x-list ldots already agrees and remains unchanged.',
 'three extended products and remaining low ellipses',kind='symbol',witness=370)
r.patch(p,'both','\\[\n  '+r'c^{k_1}(x_1)\cdots c^{k_p}(x_p)=0.'+'\n','\\[\n  '+r'c^{k_1}(x_1)\mathinner{....}c^{k_p}(x_p)=0.'+'\n','ASTRA-V-ELLIPSES-359','Preserve the first product four-point abbreviation.')
r.patch(p,'both',r'\gamma^{k_1}(x_1)\cdots\gamma^{k_p}(x_p)',r'\gamma^{k_1}(x_1)\mathinner{....}\gamma^{k_p}(x_p)','ASTRA-V-ELLIPSES-359','Preserve the gamma product four-point abbreviation.')
r.patch(p,'both',r'\gamma^{k_1}(\widetilde c_0(x_1))\cdots',r'\gamma^{k_1}(\widetilde c_0(x_1))\mathinner{....}','ASTRA-V-ELLIPSES-359','Preserve the image product four-point abbreviation.')
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-359','Preserve the four remaining complete three-point low groups.',count=4)
r.own_finding('ASTRA-V-FACTORIAL-359',p,
 'The final coefficient relation prints(k1+...+kp)! without a minus1 inside the factorial.',
 'Retain the factorial exactly as printed.',
 'Verify its implication from the preceding coefficient calculation without replacing it by a sharper coefficient.',
 'Put M=sum k_j. By6.6.4 and the iterated6.5.3 product,the degree-M coefficient of the rank-zero product is(-1)^(M-1)(M-1)! product_j c^(k_j)(x_j);this is the same explicit iterated coefficient map detailed in identification_355.json. Since the product pair equals(0,1),that coefficient is0. Multiplication by the scalar(-1)^(M-1)M gives exactly the printed M! relation. In the local characteristic-zero/Q-algebra convention of6.5,that factorial is invertible and yields the required zero product. Thus the printed factorial is supported without any textual repair.',
 'last displayed factorial relation',kind='exact_identification',verdict='confirmed and retained with exact coefficient map',witness=370)
r.page(p,'Ces relations etant isobares','donne un diagramme commutatif:',
 'Full main373 four strips and native370 top/lower compared. Checked all Omega forms and six actual algebra-name wedges,the first tilde-c0 arrow and wavy element assignment,all universal coefficient-map wording and positivity bounds,Fil^n and degree>=n,three four-dot product groups and four remaining three-dot groups,source semicolon then image-pair stop,the unaccented entraine and masculine applique corrections,the exact printed M! consequence and unchanged zero product,final colon and every remaining word. No prose underline or author note.',
 witness='Native370 top/lower complete body;six wedges,three four-point groups,source adjective/verb spelling,and semicolon resolved.')
r.commit()
