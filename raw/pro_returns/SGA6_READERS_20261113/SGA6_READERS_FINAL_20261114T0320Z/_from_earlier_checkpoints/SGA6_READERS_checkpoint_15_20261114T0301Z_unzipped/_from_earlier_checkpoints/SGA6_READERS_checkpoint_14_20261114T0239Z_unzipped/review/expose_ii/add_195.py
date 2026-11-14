"""Folio195: AppendixI opening and the first part of its Koszul lemma."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('191_195',29,'APPENDICE I / UN CONTRE-EXEMPLE DE VERDIER, with no stop after I',
 'The two capitalized title lines and the absence of a stop agree with the attached title. The author note is numerical1.',
 'Appendix title',change='Retain the title wording and punctuation; give its author note explicit label1.')
sid=r.finding('191_195',30,'The R in Rf_* has two horizontal lower rules',
 'The main scan shows two separate rules beneath R in paragraph0.2. Preserve these literal horizontal strokes, with the whole derived direct-image map unchanged.',
 'Paragraph0.2, derived direct-image functor',verdict='amended',change=r'Use \underline{\underline{R}}f_* in both layers.')
r.patch(195,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,'Preserve the two actual lower rules beneath the paragraph0.2 derived R.')
r.finding('191_195',31,'Page195 ends il existe n′≥n; page196 begins tel que',
 'Both boundary regions were inspected directly. The existing marker puts tel que and the transition map on196, exactly as printed.',
 'Final body line and following page opening',change='Retain the boundary before tel que.')
layout_reason='The first line of actual196 prints the transition H_i(f^{n′},A)→H_i(f^n,A) inline between tel que and soit nul. The attached display has the identical mathematical token sequence, the same two bounds from195, and the same final stop. The governing prompt accepts this layout variation, so there is no content correction to apply. This regional inspection does not mark196 fully checked.'
r.finding('191_195',32,'tel que H_i(f^{n′},A)→H_i(f^n,A) soit nul. is the opening line of196',layout_reason,
 'Actual196, first line only',verdict='layout observation accepted without content patch',change='Retain the existing mathematical tokens and punctuation; no layout-only patch.',actual_page=196)
r.source('fixes/MANUAL_6_findings/MANUAL_6_findings_191_195.json#1','The cited transition is on actual196 and has the attached token sequence',layout_reason,
 'Actual196, first line only',page=196,verdict='layout observation accepted without content patch',change='Close the stale195 replay as a layout-only observation; no content change.')
sid=r.finding('191_195',33,'All three system f letters on195 have an individual lower rule',
 'The definition f=(f_alpha), the equation f(x)=0, and the Koszul term H_i(f^n,A) each underline the same typed f. The native witness confirms all three. This decision is restricted to195; later appendix occurrences receive separate direct observations.',
 'Lemma1.1, three system symbols',verdict='not applied and now applied',change=r'On195 replace the three \mathbf f forms by \underline{f}.',witness=206)
r.patch(195,'both',r'\mathbf f',r'\underline{f}',sid,'Preserve the three directly observed individual f rules on195.',3)
sid='ASTRA-II-O-195';reason='The two structure-sheaf O letters in the introduction and the O_X in0.1 each carry one lower rule. The indices remain outside those rules.'
r.own_finding(sid,195,'Three underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'Introduction and paragraph0.1',kind='font')
r.patch(195,'both',r'\mathcal O',r'\underline{O}',sid,reason,3)
sid='ASTRA-II-PHI-195';reason='The inclusion functor in0.3 has a closed loop with a crossing stem, visible in the main scan and native witness. Preserve it as phi.'
r.own_finding(sid,195,'One closed-loop phi glyph',r'\varphi',r'\phi',reason,'Paragraph0.3',kind='symbol',witness=206)
r.patch(195,'both',r'\varphi',r'\phi',sid,reason)
sid='ASTRA-II-NOTES-195';reason='The title call and matching complete author note show a raised numerical1 inside baseline parentheses. The two dates and all wording of the note were compared.'
r.own_finding(sid,195,'Explicit numerical1 title note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Title and complete author note',kind='author_footnote',witness=206)
r.patch(195,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,reason)
sid='ASTRA-II-PARAGRAPHS-195';reason='The paragraph identifiers0.1.,0.2.,0.3. are plain typed numerals followed by stops. The statement-label convention for Lemme is retained separately.'
r.own_finding(sid,195,'Three plain numerical paragraph identifiers','Bold0.1.,0.2.,0.3.','Plain0.1.,0.2.,0.3.',reason,'Three introductory numbered paragraphs',kind='font')
for number in ('0.1.','0.2.','0.3.'):
 r.patch(195,'both',r'\textbf{'+number+'}',number,sid,reason)
sid='ASTRA-II-UNDERLINE-195';reason='Every lexical group in Lemma1.1 and its two listed conditions has a word rule, including i.e. The mathematical units and item labels remain independent; each system f has its separately observed rule. The preceding introductory prose is plain. Section-title styling follows the accepted heading convention.'
r.own_finding(sid,195,'Underlined lemma words and conditions','Plain lemma prose',r'\uline on exact inspected lexical groups',reason,'Lemma1.1 through the page ending',kind='underline',witness=206)
old=(ROOT/'build/page_packets/195/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
a=old.index('Soient ',old.index(r'\textbf{Lemme 1.1.}'))
new=old[:a]+underline_statement(old[a:])
r.patch(195,'both',old,new,sid,reason)
r.page(195,'APPENDICE I / UN CONTRE-EXEMPLE DE VERDIER','(ii) ... il existe n′≥n; note ends une question de celui-ci.',
 'The complete title and author note, all three introductory paragraphs, all functor maps, and the full printed lemma portion were compared. Native witness206 confirms the three underlined system f letters, closed phi and exact lemma word rules. Checker32 and its manual replay were inspected at the opening of actual196 and closed as layout-only observations without marking196 complete.',witness=206)
r.commit()
