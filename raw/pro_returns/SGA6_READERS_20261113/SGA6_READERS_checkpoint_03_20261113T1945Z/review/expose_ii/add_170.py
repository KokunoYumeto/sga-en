"""Folio170: full proof comparison, punctuation witness and structure sheaf."""
from review_helpers import Review
r=Review()
r.finding('166_170',32,'F | S_{f_{ij}} est begins the page',
    'The restriction and the verb est are on the first printed line; the preceding page ends Le faisceau. Both attached markers already preserve this boundary.',
    'First printed line',change='Retain the existing page boundary.')
r.finding('166_170',33,'(EGA I 9.4.9 et IV 1.7.7), on peut',
    'The main image has a faint speck above the comma; the native witness has a clean comma at precisely the same position. Both attached layers already have the observed comma.',
    'Proof of (ii)⇒(iii), citation before on peut',witness=181)
r.finding('166_170',34,'No punctuation follows the second line of the Im(u_i) display',
    'The final tensor power ends the display without a stop in both scans. Both attached layers already retain this absence.',
    'Two-line image formula',witness=181)
sid='ASTRA-II-O-170';reason='Both structure-sheaf O letters in the two morphism displays carry a rule under the letter alone; the S subscripts and r_i powers are independently typed.'
r.own_finding(sid,170,'Two underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'First and second morphism displays',kind='font',witness=181)
r.patch(170,'both',r'\mathcal O',r'\underline{O}',sid,reason,2)
r.page(170,'F | S_{f_{ij}} est','F un Idéal quasi-',
    'All proof prose, section and tensor indices, two morphisms and the two-line image equality directly compared. No lexical emphasis span occurs on this proof page. The witness was inspected at the citation comma and both image-formula lines.',witness=181)
r.commit()
