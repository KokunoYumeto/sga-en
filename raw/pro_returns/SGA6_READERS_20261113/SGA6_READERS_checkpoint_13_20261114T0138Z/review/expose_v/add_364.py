#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=364
r.finding('361_365',25,'Or si begins a new indented paragraph at the page top.',
 'Both main378 first strip and native375 top show the indent. The supplied blank line after the marker agrees with the actual boundary and paragraph.',
 '363/364 paragraph boundary',witness=375)
r.finding('361_365',26,'The first lambda-anneau is a continuous compound with no inserted space after the hyphen.',
 'Both scans show the joined word. The supplied source no longer places a whitespace-producing line end inside the compound and agrees.',
 'opening lambda-anneau',witness=375)
r.finding('361_365',27,'The lower lambda_t label of7.5.4 is above its rightward arrow.',
 'Both scans show all four arrows and their labels. The lower lambda_t matches the upper label position;both vertical psi^(k-prime) arrows point downward,with labels outside the square. The attached diagram agrees.',
 '7.5.4,complete diagram',witness=375)
r.finding('361_365',28,'Enfin starts an indented paragraph before the final unit identity.',
 'The native lower and primary third strip both show the paragraph indent. The supplied blank line agrees;the source unit equality and its integration wording remain unchanged.',
 'final proof paragraph',witness=375)
r.finding('361_365',29,'BIBLIOGRAPHIE is all capitals and has a line beneath the title.',
 'The capitalization agrees in the attached subsection heading. Its title rule is covered by the accepted section-title typography convention in NOTE_6;no mathematical or lexical distinction is erased.',
 'bibliography heading',witness=375)
r.finding('361_365',30,'The Grothendieck title is ordinary type with no rule beneath it.',
 'Both scans show the title and journal details in plain type. The supplied unemphasized title agrees. The printed volume86,year1958,and pages137 a154 are all present and exact.',
 'bibliography[1]',witness=375)
r.finding('361_365',31,'The Hirzebruch title is ordinary type with no rule beneath it.',
 'Both scans show the complete German title in plain type and the final period. The supplied title agrees word by word;no extra edition,publisher,or date is supplied.',
 'bibliography[2]',witness=375)
for source in ['fixes/FIXLOG_6.jsonl#343','fixes/FIXLOG_6_CURRENT.jsonl#308']:
 r.source(source,'There is no printed id or Id occurrence in the body of364;the source ends with the second bibliography item.',
  'This row changes a nonprinted macro block for the following expose from providecommand to renewcommand. Since id is already defined,renewcommand makes the specified subsequent scope take effect. Retain this implementation reset;its glyph validity is to be read from the actual later usage pages. It is not evidence for an id glyph on364 and does not alter this page text. The local capital Id repair on361 is literal and independent.',
  'nonprinted ExposeVI continuation block after the bibliography',verdict='confirmed as scoped implementation decision',
  change='Retain the existing next-expose macro reset;no printed-body patch on364.',witness=375,page=364)
r.own_finding('ASTRA-V-LOG-DERIVATIVE-364',p,
 'The logarithmic derivative is stated to be an isomorphism when K has the source characteristic-zero convention.',
 'Retain the assertion and all following converse-proof wording.',
 'Record the exact inverse map used in the printed integration argument.',
 'With the Q-algebra meaning explicitly stated on349,Dlog:1+tK[[t]]→K[[t]] sends f to f-prime/f. Its inverse sends g=sum_(j>=0)g_j t^j to exp(sum_(j>=0)g_j t^(j+1)/(j+1)). The integral is uniquely fixed by constant0,and the exponential by constant1;formal differentiation and Log/exp composition give both inverse identities. Equality of all Phi^k therefore gives equality of every Dlog coefficient,and then equality of f. Applying this coefficient injection to7.5.2 gives lambda_t(xy)=lambda_t(x)circ lambda_t(y);applying it to7.5.4 gives the stated commutation identity. For the unit,psi^k(1)=1 yields Dlog(lambda_t(1))=1/(1+t),whose zero-constant integral is Log(1+t),and exponentiating gives lambda_t(1)=1+t. These maps use exactly the source assumptions and supplied constant terms.',
 '7.5(ii),integration and coefficient-detection proof',kind='exact_identification',verdict='confirmed and retained with exact inverse map',witness=375)
r.own_finding('ASTRA-V-INK-364',p,
 'A small raised ink fragment occurs after l est in the line saying the right square is always commutative.',
 'Retain the attached wording without an added punctuation token.',
 'Record the observed fragment without assigning an unsupported character or physical cause.',
 'The primary second strip and native375 top show a small detached raised mark after l est. The closer native crop review/expose_v/witness_364_est_mark.png resolves it into a short upper ink piece and smaller separated points;the complete apostrophe inside l est on the same crop is a taller continuous stroke. The additional fragment establishes no complete further letter,mathematical operator,or author-note label. No additional readable token is introduced,and no cause for the ink is asserted.',
 'paragraph about7.5.2,after l est',kind='physical_observation',verdict='source ink recorded;wording retained',witness=375)
r.page(p,'Or si K est un lambda-anneau','F. Hirzebruch ... algebraischen Geometrie.',
 'Full main378 four strips and native375 complete body compared. Checked every object,arrowhead and label of7.5.4,both uses of7.3,all hatted Gs and K[[t]],the exact inverse logarithmic derivative with constant terms,all quantifiers and diagram references in the converse,all composition circles and primes,the final unit identity and paragraph break,bibliography capitalization and both full plain titles,all dates/page numbers/punctuation,and the separate unreadable raised ink fragment. No prose underlining beyond the accepted bibliography title rule,and no author note. The following TeX macro block has no printed counterpart and is recorded separately as implementation scope.',
 witness='Native375 top/lower complete body,plus a close crop of the additional raised ink fragment after l est.')
r.commit()
