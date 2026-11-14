#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=290
r.finding('286_290',9,'Twenty-four raised round K marks on 286–289: 7, 3, 4 and 10 respectively; no K mark on 290.',
 'Every occurrence on these five fully compared pages has been inspected. The round raised marks match K^{\\bullet}; the actual narrow prime of the tag (2.12.3′) and its reference on 289 remains distinct and unchanged. This confirms the proposed mapping only in the observed 286–290 scope, without extending it to later pages.',
 'all K notation on 286–290',verdict='confirmed',change='Confirm the attached K^{\\bullet} forms in this scope; retain genuine prime in (2.12.3′).',witness=297)
r.finding('286_290',17,'The first line is the section 3 heading, with author-note call (raised 1).',
 'The main page begins at the heading; the preceding sentence ends on the fully compared 289. The attached page marker already follows that sentence.',
 'page start',witness=301)
r.finding('286_290',18,'The final body words are La flèche de changement de base.',
 'Both scans end the body line after base, without est; the attached marker places est on 291. The numerical author note below the rule is part of 290.',
 'page end',witness=301)
r.finding('286_290',19,'on vérifié facilement',
 'The accent on final é is plainly visible in both scans. The subject on and the finite construction qu’on a require vérifie here; the diplomatic layer preserves the printed participial spelling and the current layer supplies the finite verb.',
 'proof after (III 3.7.1)',witness=301)
r.own_finding('ASTRA-IV-NOTATION-290',p,'Proposition label underlined; its number and statement body plain. Preuve underlined. Headed arrow with centered tilde in (*); plain R and L letters.',
 r'\uline{Preuve}; \xrightarrow{\sim}; ordinary R and L.',
 'Replace only the inspected lexical emphasis helper; retain the proposition label convention and the mathematical symbols.',
 'The complete statement has no rules beneath its prose. The native heading and proof crops confirm the two leftward and two downward arrows in the square, the tilde-labelled rightward arrow in (*), and ordinary R/L letters. The source punctuation, boundedness superscripts b/−/+, and final display stops or comma agree.',
 'section heading, proposition, square and complete proof',kind='symbol',witness=301)
r.patch(p,'both',r'\emph{Preuve}',r'\uline{Preuve}','ASTRA-IV-NOTATION-290','Preserve the observed rule beneath Preuve, with colon outside it.')
r.own_finding('ASTRA-IV-FOOTNOTE-290',p,'Raised digit 1 within baseline parentheses in both the heading call and the footnote label.',
 r'\SGAAuthorFootnote{1}{Les résultats de ce numéro ne seront pas utilisés dans les Exp.\ V à VIII.}',
 'Use the explicit observed numerical label in both French layers.',
 'Both the native heading crop and lower proof/note crop show the same parenthesized raised digit. The note text agrees word for word, including V à VIII and final stop.',
 'heading call and note below the rule',kind='author_note',witness=301)
r.patch(p,'both',r'\protect\footnote{Les résultats de ce numéro ne seront pas utilisés dans les Exp.\ V à VIII.}',r'\protect\SGAAuthorFootnote{1}{Les résultats de ce numéro ne seront pas utilisés dans les Exp.\ V à VIII.}','ASTRA-IV-FOOTNOTE-290','Preserve the actual raised numerical call and label rather than inherited automatic numbering.')
r.page(p,'3. Compléments sur les groupes de Grothendieck des schémas (raised 1)','Body: La flèche de changement de base; note: les Exp. V à VIII.',
 'Complete proposition, all four diagram arrows and their labels, two hypotheses, base-change display, full proof and Hom adjunction, boundedness symbols, author note and boundary compared. The statement body is plain; no invented underlining. The source vérifié spelling is retained diplomatically and corrected in current.',
 witness='Native witness 301 heading and proof/note regions; witness_290_heading.png and witness_290_proof.png')
r.commit()
