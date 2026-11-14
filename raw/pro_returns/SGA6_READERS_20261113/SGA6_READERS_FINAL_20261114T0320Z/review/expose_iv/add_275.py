"""Folio275: lemmas1.3–1.4 and additive functions on an exact subcategory."""
from review_helpers import Review, ROOT, underline_statement
r=Review()
sid=r.finding('271_275',23,'The lexical statements of lemma1.2 on274 and lemmas1.3–1.4 on275 are underlined by word group',
 'The complete statements on both pages have now been inspected. Every lexical group named by the checker is underlined, including the four resp. occurrences in lemma1.4. Mathematical formulas, item labels and the locators([V]I2.1)/(1.1) retain their independent glyphs and plain references. The exact inspected groups are supplied by the274 and275 underline patches; no claim is made about further IV pages from this two-page observation.',
 'Folio274 lemma1.2; folio275 lemmas1.3–1.4',change='Render the inspected lexical groups with occurrence-specific uline patches.',witness=285)
r.decisions[-1]['image']+='; scan/SGA6_scan_360dpi.pdf#page=289; scan/SGA6_witness_300dpi.djvu#page=286'
r.finding('271_275',24,'275 begins with the coproduct isomorphism, after remarquer qu’on a on274',
 'The adjacent main pages confirm that remarquer qu’on a is above the274 folio. Both attached layers now begin275 directly with the display.',
 'Top boundary',change='Retain the corrected marker position.')
r.finding('271_275',25,'The defined word abélienne in1.5 is underlined',
 'The lower rule spans this single word; the surrounding definition prose is plain. The attached emph grouping is correct.',
 '1.5, first sentence',change='Render the existing correct span with uline.')
sid='ASTRA-IV-ACYCLIC-275'
r.own_finding(sid,275,'A crossed-loop marker in both K^{b,∅}(A) occurrences',r'\emptyset','Retain the printed acyclic-subcategory marker.',
 'The native witness shows a loop crossed by a diagonal stem in the prose definition and the quotient display. The text itself defines this category as the full subcategory of acyclic bounded complexes. The inclusion K^{b,∅}(A)→K^b(A) and its quotient are precisely the two displayed categories; the existing emptyset command records that marker without a new mathematical substitution.',
 '1.5, acyclic subcategory and display1.5.1',kind='symbol',verdict='retained',witness=286)
sid='ASTRA-IV-UNDERLINE-275';reason='Lemmas1.3 and1.4 have lexical lower rules throughout their statements, including all four resp. occurrences of1.4. Their formulas and references remain independent. Both Preuve labels and the defined words abélienne/additive in1.5 have lower rules; the number1.5 and all remaining definition prose are plain. Existing statement-label typography follows the accepted convention.'
r.own_finding(sid,275,'Two lemma word-group statements, two proof labels, two defined words, plain1.5','Plain statements, emph words and bold1.5',r'Exact lexical uline groups and plain1.5',reason,'Two lemmas and definition1.5',kind='underline',witness=286)
t=(ROOT/'build/page_packets/275/diplomatic.tex').read_text()
for num in ('1.3','1.4'):
    a=t.index('Soient ',t.index(r'\textbf{Lemme '+num+'.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
    old=t[a:b];r.patch(275,'both',old,underline_statement(old,protected=(r'\(1\.1\)',)),sid,reason)
r.patch(275,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason,2)
for word in ('abélienne','additive'):
    r.patch(275,'both',r'\emph{'+word+'}',r'\uline{'+word+'}',sid,reason)
r.patch(275,'both',r'\textbf{1.5.}','1.5.',sid,reason)
r.page(275,'Coproduct over i≥0 of L[2ni] ≃ L ⊕ (coproduct over i≥0 of L[2ni])[2n],','(1.5.1) cl_A:ob A → k(K^b(A)/K^{b,∅}(A))',
 'Every word, formula, symbol and punctuation mark was compared with both layers. The opening isomorphism is headless; both coproduct lower bounds are i≥0. All three sums on the page have no supplied summation index. The first lemma1.4 equality has no final punctuation; the second is enclosed by the printed resp. parenthesis with its final stop. The formula1.5.1 ends without punctuation and continues the sentence on276. Category A/C and lowercase ob/cl remain plain. Native witness286 resolves the exact statement groups, four resp. rules and the two crossed-loop acyclic markers.',witness=286)
r.commit()
