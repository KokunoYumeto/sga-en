#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=285
r.finding('281_285',24,'The page begins with the two-row augmentation diagram.',
 'The phrase désigne le rang) : is on 284 and the first diagram row is on 285; both attached markers now match.', 'page boundary',witness=296)
r.finding('281_285',25,'High opening star followed by On verra… in a new paragraph.',
 'The main scan and native crop show the paragraph start after the completed diagram. The attached paragraph break agrees with the source. The paired star heights are recorded separately.', 'paragraph after diagram',witness=296)
r.finding('281_285',26,'(V 3.9.1 et VI      ) que',
 'A visible untyped interval follows VI before the closer. Its content is blank; no missing numeral can be read or inferred from it. Retain the attached diplomatic spacing and current ordinary spacing as an explicit formatting variant with identical reference tokens V 3.9.1 and VI. Do not supply a conjectural reference.',
 'first line of starred paragraph',verdict='amended',change='Keep the observed blank in diplomatic and the existing compact spacing in current; no reference content is added.',witness=296)
reason=('Both scans print Deligne [5]. The directly inspected bibliography on 296 identifies [1] as Deligne, P., papiers secrets, followed by [2] Grauert, [3] Grothendieck and [V] Verdier. The reference target is therefore the named Deligne entry [1]. Current changes only the locator, while diplomatic preserves [5]; no new attribution or theorem wording is supplied. The 296 consultation is regional and does not mark that page fully checked.')
r.finding('281_285',27,'Deligne [5] a prouvé récemment',reason,'starred paragraph; bibliography entry [1] on 296',witness=296)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#392','Deligne [5]',reason,'starred paragraph',witness=296,change='Confirm current Deligne [1].')
r.source('fixes/RECONCILE_CODEX_6.json#288','Deligne [5]',reason,'starred paragraph',page=285,witness=296,change='Confirm current Deligne [1]; retain [5] diplomatically.')
for row in r.decisions:
 if row['source_id'] in ['check/findings/findings_281_285.json#27','fixes/MISPRINTS_6.json#246','fixes/FIXLOG_6_CURRENT.jsonl#392','fixes/RECONCILE_CODEX_6.json#288']:
  row['image']+='; scan/SGA6_scan_360dpi.pdf#page=310 (bibliography region only)'
r.finding('281_285',28,'The canonical K^•(X)_naïf → K^•(X) map occurs in the running sentence.',
 'The attached inline form agrees with the source. The mathematical sequence and punctuation are identical under the display/inline mapping; this is a recorded layout choice, not an additional content correction.',
 'starred paragraph, canonical comparison',witness=296,change='Retain the attached inline form; no content patch.')
f=r.finding('281_285',1,'Raised round K dots at every one of the 67 specified occurrences on 281–285 (7,15,13,20,12).',
 'Each page has now been compared in full. The round raised marks were checked against adjacent A′, X′ ticks and other punctuation in both scans. Retain the attached K^{\\bullet} mapping at these 67 inspected occurrences; this decision makes no inferred verdict for 286–296.',
 'all K superscripts on the five named pages',witness=292,change='Retain raised-dot K in the directly inspected five-page scope.')
for row in r.decisions:
 if row['source_id']==f:row['image']='scan/SGA6_scan_360dpi.pdf#pages=295-299; scan/SGA6_witness_300dpi.djvu#pages=292-296'
id='ASTRA-IV-O-285'
r.own_finding(id,p,'Two individual O rules in cases (i) and (iii), excluding the X indices.',r'\mathcal O_X',r'\underline{O}_X',
 'Native lower-page crop resolves each short horizontal rule beneath O.', 'last three numbered cases',kind='font',witness=296)
r.patch(p,'both',r'\mathcal O_X',r'\underline{O}_X',id,'Two directly observed structure-sheaf lower rules.',2)
id='ASTRA-IV-UNDERLINE-285'
r.own_finding(id,p,'Plain 2.9 with separate rules beneath Comparaison de and et; K symbols and terminal stop plain.',
 'The whole numbered heading is bold.', 'Use the two observed lexical rules.',
 'The native scan shows the rules ending before each K. The ensuing three cases and all their prose are plain.', '2.9 heading',witness=296)
r.patch(p,'both',r'\textbf{2.9. Comparaison de \(K^{\bullet}\) et \(K^{\bullet}_{\naif}\).}',r'2.9. \uline{Comparaison de} \(K^{\bullet}\) \uline{et} \(K^{\bullet}_{\naif}\).',id,'Observed lexical heading rules and plain paragraph number.')
id='ASTRA-IV-INTERPOLATION-285'
r.own_finding(id,p,'High opening star before On verra; low closing star after (XIV 1).',
 'Both stars are textsuperscript.', 'Keep the opening superscript and lower only the closing interpolation star.',
 'The native first-star crop places the opening mark above the text middle; the last-star crop places the closing mark beside and below the terminal stop. These paired marks bracket the added paragraph and have no corresponding bottom-of-page footnote. Preserve their different heights explicitly, as observed.',
 'two endpoints of starred paragraph',kind='interpolation_mark',witness=296)
r.patch(p,'both',r'(XIV 1).\textsuperscript{*}',r'(XIV 1).\textsubscript{*}',id,'The closing bracket star is visibly lowered in both scans.')
r.page(p,'Two-row diagram H^0(Y,Z) → K^•(Y)_naïf → K^•(Y) → H^0(Y,Z).','et A = O_X (II 2.4.5).',
 'Complete two-row diagram with ten headed arrows and four labels, twelve raised K dots, six integer Z glyphs, full starred paragraph, heading and all three cases compared. Both star heights and the blank after VI are recorded. Deligne locator verified against the bibliography region on 296 only. No author footnote.',witness='Native witness 296 diagram, first star, paragraph close and bottom cases; witness_285_diagram.png, witness_285_firststar.png, witness_285_stars.png, witness_285_bottom.png')
r.commit()
