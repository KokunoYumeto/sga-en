#!/usr/bin/env python3
from review_helpers import Review,read
r=Review();p=357
r.finding('356_360',3,'Comme A est a graduation finie starts an indented new paragraph at the page top.',
 'Main371 first strip and native368 top show the indent after the preceding356 display. The attached blank line below the marker already represents that paragraph break.',
 '356/357 boundary',witness=368)
bound_reason=('Both scans show strict i>1 in the first formula and i>=1 in the immediately following inverse definition. In degree i,the stated map is u_i(a)=[(0,1+C_i a)],C_i=(-1)^(i-1)(i-1)!,and its inverse extracts a_i and multiplies by C_i inverse. For i=1 both coefficients are1,so u_1(a)=[(0,1+a)] is required by the displayed inverse as well as by the declared domain A. The example A=Q[Y]/(Y^2),degree Y=1,has nonzero A1 and no higher positive degree;the printed i>1 clause does not define u on Y. The current i>=1 supplies exactly this missing component;all other formulas and the degree0 identity remain unchanged.')
r.finding('356_360',4,'The first quantifier has i>1;the inverse clause has i>=1.',bound_reason,
 'u degree bound',witness=368)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#416','Printed strict i>1 for u.',bound_reason,'u degree bound',page=p,witness=368)
r.source('fixes/RECONCILE_CODEX_6.json#304','Printed strict i>1 for u.',bound_reason,'u degree bound',page=p,witness=368)
parenthesis_reason=('Both scans show two closing parentheses after the algebra-name glyph in the introductory completed-class target. Its displayed syntax has one opening parenthesis after Ch and no opening parenthesis after Gr,so one closing parenthesis is unmatched. The target map is exactly tilde-c:x↦(epsilon(x),c(x)) into Ch(Gr of the named ring);removing the unmatched close preserves that target and every coordinate. Retain the existing current correction and literal diplomatic double close.')
r.finding('356_360',5,'The introductory target is Ch(Gr wedge)) with two final closing parentheses.',
 parenthesis_reason,'L isomorphisme target',witness=368)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#417','Two closing parentheses in the introductory Ch(Gr wedge)) target.',parenthesis_reason,'L isomorphisme target',page=p,witness=368)
r.source('fixes/RECONCILE_CODEX_6.json#305','Two closing parentheses in the introductory Ch(Gr wedge)) target.',parenthesis_reason,'L isomorphisme target',page=p,witness=368)
spelling_reason=('The scans clearly transpose the u and d in graudes. The immediately displayed associated-graded sequence specifies the same functor Gr and its components Fil^i/Fil^(i+1). The correction to gradues changes only the adjective spelling;the identity on each of those quotient components is unchanged.')
r.finding('356_360',6,'The word is printed graudes,with transposed u and d.',spelling_reason,
 'passage aux graudes associes',witness=368)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#418','Printed graudes.',spelling_reason,'associated-graded adjective',page=p,witness=368)
r.source('fixes/RECONCILE_CODEX_6.json#311','Printed graudes.',spelling_reason,'associated-graded adjective',page=p,witness=368)
definition_reason=('Both scans leave blank cells before inition,with no visible letters in that gap. The phrase refers to the definition3.10 of the canonical lambda filtration:its ideal generators are products of gamma^i(x) with augmentation-zero x and prescribed total index. Passing those generators through Fil^i→Gr^i identifies exactly the classes bar-gamma^i(x) named in the same sentence. Restoring definition therefore supplies the missing lexical prefix for this explicit construction;it introduces no new definition or mathematical operation. Preserve the blank in diplomatic and restore the three letters def with the accent in current.')
r.finding('356_360',7,'The source has la,then three blank typewriter cells,then inition.',
 definition_reason,'sentence before the generator-class test',verdict='not applied and now applied',
 change='Current restores definition;diplomatic retains hphantom{def}inition with the supplied accented prefix width.',witness=368)
r.patch(p,'current',r'\hphantom{déf}inition','définition','check/findings/findings_356_360.json#7','Restore the missing lexical prefix tied to the explicitly used3.10 generator definition.')
wedge_reason=('Seven actual357 algebra-name signs have the same unadorned two-stroke wedge shape seen on356:two in the introductory map,four in the graded sequence,and one in the following prose. Their ordinary-atom wedge transcription preserves the identity on the named augmented ring and hence on each filtration quotient and each Ch construction. No operation is added by this graphical representation.')
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_356_360.json#2').copy()
aggregate.update(verdict='actual356–357 scope decided;358–360 pending',
 printed_reading='Ten actual356 and seven actual357 algebra-name signs are small serifless wedges.',
 change=r'Use the occurrence-scoped \mathord{\wedge} replacements on356 and357 only;358–360 await direct comparison.',
 region='all actual356–357 algebra-name glyphs')
aggregate['reason']+=' '+wedge_reason
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=371; scan/SGA6_witness_300dpi.djvu#page=368'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-WEDGE-357',p,
 'Seven algebra-name signs are small unadorned wedges.',r'Use seven \mathord{\wedge} glyphs.',
 'Preserve the actual357 shape while keeping the named algebra and induced maps identical.',
 wedge_reason,'two introductory,four sequence,and one prose occurrence',kind='symbol',witness=368)
r.patch(p,'both',r'\Lambda',r'\mathord{\wedge}','ASTRA-V-WEDGE-357','Preserve all seven local ordinary-atom algebra-name glyphs.',count=7)
r.own_finding('ASTRA-V-ELLIPSIS-357',p,
 'The only complete ellipsis,in the final inline gamma-class pair,is low.',r'Use \ldots.',
 'Preserve the observed baseline series tail.',
 'Native368 lower and the main third strip show three low dots after the coefficient c^i(x);the following comma and reference are unchanged.',
 'Or gamma^i(tilde-c(x)) pair',kind='symbol',witness=368)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSIS-357','Preserve the single complete low series tail.')
r.page(p,'Comme A est a graduation finie','cl_(Gr^i)(gamma^i(tilde-c(x)))=u(c^i(x)),',
 'Full main371 four strips and native368 top/lower compared. Checked the strict source i>1 and inverse i>=1,all C_i factorial/sign factors and inverse fraction,all phi bars,exact source double parenthesis,graudes transposition,blank prefix before inition,all seven algebra-name wedges,the headed maps and middle simeq line,the degree/lambda graded subscripts,overlines on the two gamma generator classes,no prose underlines,the final low tail and comma,every word and punctuation. No author note.',
 witness='Native368 top/lower complete body;strict bound,two closes,transposed letters,blank cells,and all seven wedges resolved.')
r.commit()
