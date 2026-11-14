"""Folio202: coefficient field glyphs, exact sequences and author notes."""
from review_helpers import Review
r=Review()
r.finding('201_205',5,'The numerical1 call follows the first exact-sequence display and its stop',
 'The display ends →0. followed by a raised1 in parentheses. There is no call after canonique. The attached split mark/text placement already agrees; its literal label is recorded below.',
 'First exact sequence and first complete author note',change='Retain the existing call position and assign its observed explicit label1.',witness=213)
for i,region in [(6,'First Hom placeholder in the sentence applying the functor'),(7,'Parenthetical complex-coefficient Hom placeholder')]:
 r.finding('201_205',i,'The empty Hom argument is a baseline typed stop followed by a comma',
  'Both main and native witness show the stop at baseline, with the following comma independent. The attached (.,F) tokens already reproduce this printed placeholder.',
  region,change='Retain the existing baseline point and comma.',witness=213)
reason='The sentence prints identifications(1.2.2.1) et(1.2.4.1). The two identification maps were read on201 and202: in the real case and complex case respectively, h↦h∘d^n_{X/S}(E) identifies the appropriate Hom group with Diff^n(E,F) or Diff^n_C(E,F). The complex identification is numbered(1.2.3.1), while(1.2.4.1) is the principal-parts exact sequence to which Hom is applied. These explicit composition maps support the existing corrected second reference(1.2.3.1), preserving the printed(1.2.4.1) diplomatically.'
r.finding('201_205',8,'The second identification reference is printed(1.2.4.1)',reason,
 'Sentence preceding formula(1.2.4.2)',change='Retain diplomatic(1.2.4.1) and existing current(1.2.3.1).',witness=213)
for sid in ['fixes/RECONCILE_CODEX_6.json#259','fixes/FIXLOG_6_CURRENT.jsonl#364']:
 r.source(sid,'The second identification reference is(1.2.4.1)',reason,'Sentence preceding formula(1.2.4.2)',page=202,change='Retain the existing current-only reference correction.',witness=213)
sid='ASTRA-II-O-202';reason='All twenty-three O letters, including the second author note, have one individual lower rule. The display and inline indices remain outside the rule.'
r.own_finding(sid,202,'Twenty-three singly underlined O letters',r'\cO',r'\underline{O}',reason,'Complete body and second author note',kind='font',witness=213)
r.patch(202,'both',r'\cO',r'\underline{O}',sid,reason,23)
sid='ASTRA-II-C-202';reason='Each of the fifteen coefficient-field C letters has two horizontal lower rules. The main image and witness distinguish those rules clearly, including all four Diff subscripts. The latter receive explicit script braces so the complete double-rule glyph remains one subscript field.'
r.own_finding(sid,202,'Fifteen field C letters with two horizontal lower rules',r'\mathbb C',r'\underline{\underline{C}}',reason,'Complex coefficient expressions and four Diff subscripts',kind='font',witness=213)
r.patch(202,'both',r'_\mathbb C',r'_{\underline{\underline{C}}}',sid,reason,4)
r.patch(202,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason,11)
sid='ASTRA-II-NOTES-202';reason='The first note has raised numerical1 in baseline parentheses and is called after the display stop. The second has raised numerical2 and is called after O_X in D’où, en tensorisant. Both complete notes were compared; preserve their actual labels and call positions.'
r.own_finding(sid,202,'Explicit numerical author notes1 and2',r'\footnotemark, \footnotetext and \footnote',r'Explicit SGAAuthorFootMark/Text{1} and SGAAuthorFootnote{2}',reason,'Two note calls and both complete footnotes',kind='author_footnote',witness=213)
r.patch(202,'both',r'\footnotemark',r'\SGAAuthorFootMark{1}',sid,reason)
r.patch(202,'both',r'\footnotetext{',r'\SGAAuthorFootText{1}{',sid,reason)
r.patch(202,'both',r'\footnote{',r'\SGAAuthorFootnote{2}{',sid,reason)
sid='ASTRA-II-PARAGRAPHS-202';reason='The paragraph identifiers1.2.3. and1.2.4. use plain typed numerals and their printed final stops.'
r.own_finding(sid,202,'Plain1.2.3. and1.2.4.','Bold identifiers','Plain identifiers with their original stops',reason,'Two paragraph openings',kind='font',witness=213)
for num in ('1.2.3.','1.2.4.'):
 r.patch(202,'both',r'\textbf{'+num+'}',num,sid,reason)
r.page(202,'dans F d’ordre ≤n.','The parenthetical complex-coefficient sequence ends with a stop; note2 ends P^{n−1}_{X/S}.',
 'Every word, all four displayed formulas, each Hom placeholder, all tensor subscripts, the sigma_n label on the real row, the unlabelled complex-row arrow, and both complete notes were compared. The numbered complex bijection has an arrowhead. Native witness213 confirms literal double lower rules on all coefficient C letters, both author labels, and the printed second identification reference. No lexical emphasis occurs on this page.',witness=213)
r.commit()
