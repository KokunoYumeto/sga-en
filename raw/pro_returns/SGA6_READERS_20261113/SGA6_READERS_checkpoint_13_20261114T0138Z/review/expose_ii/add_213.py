"""Folio213: projective-system continuation and parameterized operators."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('211_215',4,'The page begins(3.0.2)); then item(ii)',
 'Both preceding and current complete pages were compared. The attached source puts the marker before the reference and closing parenthesis, followed by the entire second item, exactly matching the print.',
 'First two printed lines',change='Retain the existing boundary before(3.0.2)).')
r.finding('211_215',5,'V une variété compacte, E et F des fibrés vectoriels complexes',
 'The named bundles occur as E et F, with no additional et before E. The attached correction already reproduces this exact conjunction placement.',
 'Lemma3.1.4 hypotheses',change='Retain the attached E et F wording.',witness=224)
r.finding('211_215',6,'Pour u∈Diff^n_C(pr_2^*E,pr_2^*F), l’application ... is inline',
 'The attached inline version has the same membership formula and following comma as the scan. Under the governing layout convention this observation needs no further content patch.',
 'Lemma3.1.4, second sentence',verdict='layout observation accepted without further content patch',change='Retain the already-matching tokens and comma.')
r.finding('211_215',7,'montrer que pour, with no comma after que',
 'The proof line visibly runs que pour without intervening punctuation. The attached text already removes the extra comma.',
 'Proof, sentence reducing to sections of G',change='Retain the attached que pour.')
r.finding('211_215',8,'The numerical1 call follows the final displayed membership formula and its stop',
 'The source has no note call after soit. The final display ends with a stop and then the raised1 call. The existing split mark/text position agrees; the explicit label is supplied below.',
 'Paragraph3.1.5 final display and author note',change='Retain call placement after the stop and preserve numerical1 explicitly.',witness=224)
sid=r.finding('211_215',9,'(loc.cit) has no stop after cit',
 'The main and native witness show cit immediately followed by the close parenthesis. The same abbreviation at the opening of211 prints its final stop. Preserve this omitted-stop reading diplomatically and complete the abbreviation in current.',
 'Parenthetical explanation after item(ii)',verdict='confirmed; current correction now applied',change='Current alone: (loc.cit) becomes (loc.cit.).',witness=224)
r.patch(213,'current','(loc.cit)~:','(loc.cit.)~:',sid,'Supply the omitted abbreviation stop in current only.')
sid='ASTRA-II-C-213';reason='The five Diff coefficient subscripts and the coefficient letter in the author note have two horizontal lower rules. All six were compared; brace the complete changed Diff subscript glyph explicitly.'
r.own_finding(sid,213,'Six field C letters with double lower rules',r'\mathbb C',r'\underline{\underline{C}}',reason,'Item(ii), lemma and author note',kind='font',witness=224)
r.patch(213,'both',r'_\mathbb C',r'_{\underline{\underline{C}}}',sid,reason,5)
r.patch(213,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
sid='ASTRA-II-N-213';reason='The sole natural-number N in the lemma carries two distinct lower rules.'
r.own_finding(sid,213,'One N with double lower rules',r'\N',r'\underline{\underline{N}}',reason,'Lemma3.1.4 hypotheses',kind='font',witness=224)
r.patch(213,'both',r'\N',r'\underline{\underline{N}}',sid,reason)
sid='ASTRA-II-PHI-213';reason='All four phi occurrences in item(ii) have closed loops crossed by stems; the projective-limit arrow is separately leftward and retained.'
r.own_finding(sid,213,'Four closed-loop phi glyphs',r'\varphi',r'\phi',reason,'Opening item(ii)',kind='symbol',witness=224)
r.patch(213,'both',r'\varphi',r'\phi',sid,reason,4)
sid='ASTRA-II-NOTE-213';reason='The final displayed call and complete note both use raised numerical1 within baseline parentheses. The coefficient C has its independent double lower rule.'
r.own_finding(sid,213,'Explicit numerical1 split author note',r'\footnotemark and \footnotetext',r'\SGAAuthorFootMark{1} and \SGAAuthorFootText{1}',reason,'Last display and sole author note',kind='author_footnote',witness=224)
r.patch(213,'both',r'\footnotemark',r'\SGAAuthorFootMark{1}',sid,reason)
r.patch(213,'both',r'\footnotetext{',r'\SGAAuthorFootText{1}{',sid,reason)
sid='ASTRA-II-PARAGRAPH-213';reason='The identifier3.1.5. has plain typed numerals and its final stop.'
r.own_finding(sid,213,'Plain3.1.5.',r'\textbf{3.1.5.}','3.1.5.',reason,'Final numbered paragraph',kind='font')
r.patch(213,'both',r'\textbf{3.1.5.}','3.1.5.',sid,reason)
sid='ASTRA-II-UNDERLINE-213';reason='Every lexical group in Lemma3.1.4 has a lower rule, including the et between E and F. Mathematical units remain independent. Only the Preuve label is underlined in the following proof; the opening item and explanatory parenthesis are plain.'
r.own_finding(sid,213,'Complete lemma lexical rules and Preuve label','Plain lemma prose and emph proof label',r'Lexical uline groups',reason,'Lemma3.1.4 and proof label',kind='underline',witness=224)
t=(ROOT/'build/page_packets/213/diplomatic.tex').read_text()
for p in r.patches:
 if p['layer']=='both':t=t.replace(p['old'],p['new'])
a=t.index('Soient ',t.index(r'\textbf{Lemme 3.1.4.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(213,'both',old,underline_statement(old),sid,reason)
r.patch(213,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
r.page(213,'(3.0.2));','u∈Diff^n(pr_2^*E,pr_2^*F). followed by note1; note ends pour abréger.',
 'Every word, both opening item delimiters, the leftward projective-limit arrow, all pullback stars and parameter subscripts, each comma/stop and the complete author note were compared. Native witness224 confirms the omitted abbreviation stop, four closed phi glyphs, field-letter rules, conjunction placement and exact lemma lexical extents.',witness=224)
r.commit()
