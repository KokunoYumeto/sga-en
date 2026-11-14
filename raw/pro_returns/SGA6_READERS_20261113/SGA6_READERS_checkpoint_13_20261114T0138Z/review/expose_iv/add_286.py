#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=286
for i,s,region in [(1,'munit','2.10, assertion'),(2,'d’une structure de','2.10, assertion'),(3,'module','2.10, assertion'),(4,'covariant','2.11'),(5,'propres','2.11')]:
 r.finding('286_290',i,s+' underlined','Both scans have the exact lexical rule; the formula, hyphen before module, and terminal punctuation remain independent.',region,witness=297)
r.finding('286_290',6,'Ordinary upright L above the tensor symbol, with A below.',
 'The native upper crop resolves a single-stroke L with ordinary foot, no added lower rule or duplicated stem. Retain the attached plain derived-tensor L.', 'first display',witness=297)
r.finding('286_290',7,'parf underlined in D(X), while both coh suffixes remain plain.',
 'The lower rule belongs exactly to parf in the first factor. The attached explicit uparf matches.', 'first display',witness=297)
r.finding('286_290',8,'Grâce,à l’associativité',
 'A comma with the same descending tail as the surrounding typed commas stands after Grâce in both scans. The prepositional phrase Grâce à has no intervening syntactic boundary; current removes only that stray comma. Diplomatic preserves it.', 'sentence after (2.10.1)',witness=297)
id='ASTRA-IV-O-286'
r.own_finding(id,p,'Three O letters carry individual short lower rules; X/Y indices remain outside.',r'\mathcal O',r'\underline{O}',
 'The first ringed topos and both endpoints of f have clearly resolved O rules in the native upper crop.', '2.10, all structure-sheaf letters',kind='font',witness=297)
r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,'Three locally observed O rules.',3)
id='ASTRA-IV-UNDERLINE-286'
r.own_finding(id,p,'Plain 2.10, 2.11 and 2.11.1; lexical heading and five body word rules.',
 'Whole headings/paragraph number bold; five emph spans.', 'Use the observed word rules and plain numbering.',
 'All heading formulas and periods are outside the rules. The lower paragraph is plain throughout, including both Rf_* occurrences.', 'headings and five emphasized words/groups',witness=297)
for s in ['munit',"d'une structure de",'module','covariant','propres']:
 r.patch(p,'both',r'\emph{'+s+'}',r'\uline{'+s+'}',id,'Observed upright word rule.')
for old,new in [
 (r'\textbf{2.10. Accouplement entre \(K^{\bullet}\) et \(K_{\bullet}\).}',r'2.10. \uline{Accouplement entre} \(K^{\bullet}\) \uline{et} \(K_{\bullet}\).'),
 (r'\textbf{2.11. Loi covariante sur \(K_{\bullet}\) et formule de projection.}',r'2.11. \uline{Loi covariante sur} \(K_{\bullet}\) \uline{et formule de projection}.'),
 (r'\textbf{2.11.1.}',r'2.11.1.')]:r.patch(p,'both',old,new,id,'Observed heading rules and plain paragraph number.')
r.own_finding('ASTRA-IV-NOTATION-286',p,'Seven raised K dots, two plain R letters in Rf_*, and one underlined parf.',
 'Raised-dot K, plain R, explicit uparf.', 'Retain these inspected forms.',
 'Both native crops distinguish the upper K marks from the lower K dots; the R letters have no detached lower rules. The source A below the tensor sign is retained as printed.',
 'all notation on the page',kind='symbol',verdict='confirmed',witness=297)
r.page(p,'2.10. Accouplement entre K^• et K_•.','(2.11.1.1) f_* : K_•(X) → K_•(Y)',
 'Complete prose, hypotheses as printed, every reference, both displayed pairings and the derived/direct-image maps compared. Seven raised K marks and all lower dots checked. The final display has no terminal punctuation. Broad K-dot finding #9 will be completed after the remaining pages in its scope.',witness='Native witness 297 upper and lower formula regions; witness_286_top.png and witness_286_lower.png')
r.commit()
