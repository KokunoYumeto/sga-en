"""Folio220: bibliography entries1–13, all printed punctuation and boundaries."""
from review_helpers import Review
r=Review()
r.finding('216_220',24,'BIBLIOGRAPHIE in capitals with a lower rule',
 'The heading is at the top of220, not219 as its earlier marker-keyed record indicates. Its capitals are already restored. The section-title convention expressly accepts subsection typography without reproducing the title rule.',
 'Top heading',change='Retain the existing capitalized section title and its accepted heading typography.',actual_page=220)
r.finding('216_220',25,'220 starts with BIBLIOGRAPHIE, followed by entry[1]',
 'The entire heading and the first bibliography item belong after the220 marker; both attached layers already place them there.',
 'Top boundary',change='Retain the current marker placement.')
r.finding('216_220',26,'220 ends at the stop after entry[13]; entry[14] starts221',
 'Directly inspected adjacent folios show the complete Kiehl entry ending220 and the label[14] with Lang at the top of221. The attached marker already precedes the whole item14.',
 'Bottom boundary and adjacent folio top',change='Retain the current221 marker position.')
r.finding('216_220',27,'Verdier, J-L., without a stop after J',
 'The first bibliography entry prints a hyphen immediately after J. The attached text preserves that exact punctuation; the distinct J.-L. form in entry18 on221 is also printed.',
 'Bibliography entry1',change='Retain J-L. at this occurrence.')
for index,printed,region in [(28,'1963-64','Entry4, seminar year'),(30,'2974-2976','Entry5, page range'),(31,'1959-60','Entry8, seminar year'),(32,'1959-60','Entry10, seminar year'),(33,'1964-65','Entry11, seminar year'),(34,'6499-6502','Entry12, page range'),(35,'256-273','Entry13, page range')]:
    r.finding('216_220',index,printed+' with a typed hyphen',
      'The directly inspected range uses the short typed hyphen and the attached source already retains a single TeX hyphen. No other range or joint-name convention is changed.',
      region,change='Retain the existing single hyphen.',witness=231)
r.finding('216_220',29,'Fonctions analyliques sur un ensemble semi-analytique',
 'The witness clearly shows l after analy in the first adjective, while the later semi-analytique has t. The diplomatic layer already keeps analyliques and the corrected layer supplies analytiques; preserve that explicit source variant.',
 'Bibliography entry5, Frisch title',change='Retain the existing diplomatic analyliques / corrected analytiques variant.',witness=231)
r.page(220,'BIBLIOGRAPHIE; [1] Artin, M., Grothendieck, A., et Verdier, J-L.','[13] Kiehl, R., Theorem A und Theorem B in der nichtarchimedischen Funktionentheorie, Invent. math.2, p.256-273(1967).',
 'Every word, author initial, accent, date, range and punctuation mark in entries1–13 was compared with both layers. The printed Frisch spelling, the title analyliques, Italian varietà, unpunctuated H. before Funzioni, literal T.F without a final abbreviation stop, and the raised o in n°20 are preserved. Joint-name dashes and the section-title rule follow the expressly accepted conventions. There are no author notes or further source words below entry13. Native witness231 resolves the title misspelling and thin punctuation.',witness=231)
r.commit()
