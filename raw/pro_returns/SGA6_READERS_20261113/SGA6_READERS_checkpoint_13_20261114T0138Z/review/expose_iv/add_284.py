#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=284
r.finding('281_285',16,'et l’homomorphisme canonique underlined as one lexical group on folio 284.',
 'The former split was caused by a displaced page marker. The whole phrase is now on 284 and both scans show one rule from et through canonique. The attached adjacent emphasis spans select the same letters; they are joined into the single observed underline span.',
 'first printed line',actual_page=284,witness=295,change='Render the complete phrase as one upright underline on 284; no text changes.')
r.finding('281_285',17,'(1 = cl(O_X)), et l’homomorphisme canonique (2.6.3.2)',
 'This formula starts the actual page; 283 ends at unité. The current markers preserve that boundary.', 'page start',witness=295)
for i,s,region in [(18,'et l’homomorphisme canonique','first line'),(19,'est un homomorphisme d’anneaux unifères','first assertion'),(20,'l’homomorphisme','second paragraph'),(21,'est un homomorphisme d’anneaux unifères','after the two pullback displays'),(23,'rang','2.8, augmentation paragraph')]:
 r.finding('281_285',i,s+' underlined','Both scans have a rule below the exact lexical group. The full stops and adjacent formulas remain outside the rules.',region,witness=295)
r.finding('281_285',22,'(et par suite aussi … via l’homomorphisme canonique K^•(X)_naïf → K^•(X) d’une structure…',
 'The native witness has no closer for the parenthesis opened before et par suite. The existing current closer after the canonical map closes only that parenthetical aside; the two algebra structures and comparison map are unchanged. Diplomatic correctly leaves the parenthesis open.',
 '2.8, paragraph following the i display',witness=295)
id='ASTRA-IV-O-284'
r.own_finding(id,p,'Six O letters individually underlined, all X/Y indices outside the rule.',r'\mathcal O',r'\underline{O}',
 'Both scans show one short rule beneath each structure-sheaf O, in the initial unit formula and the three ringed-topos pairs. Explicit local replacements preserve their observed glyphs.', 'all six structure-sheaf occurrences',kind='font',witness=295)
r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,'Six occurrence-specific structure-sheaf lower rules.',6)
id='ASTRA-IV-UNDERLINE-284'
r.own_finding(id,p,'Five lexical assertion groups, rang, and the two lexical portions of heading 2.8 underlined; numbering and formulas plain.',
 'Separate adjacent emph groups at the opening; other emph groups and fully bold heading.',
 'Use explicit upright word rules, joining the inspected opening phrase.',
 'The source rules stop before the two full stops and all mathematical units. The heading rule covers Augmentation de and vers independently.', 'opening continuation, assertion groups and 2.8 heading',witness=295)
r.patch(p,'both',"\\emph{et l'}%\n\\emph{homomorphisme canonique}",r"\uline{et l'homomorphisme canonique}",id,'One source underline spans the full first-line phrase.')
r.patch(p,'both',r"\emph{est un homomorphisme d'anneaux unifères}",r"\uline{est un homomorphisme d'anneaux unifères}",id,'Both observed assertion rules stop before the final stop.',2)
r.patch(p,'both',r"\emph{l'homomorphisme}",r"\uline{l'homomorphisme}",id,'Observed word rule.')
r.patch(p,'both',r'\emph{rang}',r'\uline{rang}',id,'Observed word rule.')
r.patch(p,'both',r'\textbf{2.8. Augmentation de \(K^{\bullet}\) vers \(H^0(\ ,\mathbb Z)\).}',r'2.8. \uline{Augmentation de} \(K^{\bullet}\) \uline{vers} \(H^0(\ ,\mathbb Z)\).',id,'Plain paragraph number and independent lexical rules in the heading.')
r.own_finding('ASTRA-IV-NOTATION-284',p,'Twenty raised K dots; four compact doubled/heavy diagonal integer Z glyphs without detached lower rules; terminal rg is lower-case.',
 'K^{\\bullet}, mathbb Z, and Rg macro.', 'Retain the inspected notation.',
 'All K superscripts and integer-coefficient occurrences were compared. The witness resolves the Z as the same compact heavy/doubled-diagonal form used earlier in IV, with no separately drawn lower line; the existing integer-symbol convention is retained locally.',
 '2.8 and earlier ring-homomorphism displays',kind='font',verdict='confirmed',witness=295)
r.page(p,'(1 = cl(O_X)), et l’homomorphisme canonique (2.6.3.2)','désigne le rang) :',
 'Complete prose and maps, twenty raised K marks, six O rules, four integer Z glyphs, two assertions of unitality, the missing printed parenthesis and ending diagram introduction compared. No author footnote.',witness='Native witness 295 opening and lower augmentation regions; witness_284_top.png and witness_284_lower.png')
r.commit()
