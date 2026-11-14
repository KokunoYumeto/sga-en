"""Folio189: exact statement rules, explicit author label, paired parentheses."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('186_190',25,'Closed-loop phi in display(3.0)',
 'The circular loop and crossing stem agree with the attached phi form. The full domain and codomain were compared.',
 'Proposition3.5 display(3.0)',witness=200)
for i,region in [(26,'Display(3.5.1)'),(27,'Display(3.5.2)')]:
 r.finding('186_190',i,'The R in RQ(E) has two horizontal lower rules',
 'Both actual glyphs have two separate horizontal strokes below R. Preserve these literal rules independently of the plain derived-functor letters with superscript degrees in the proof and footnote.',
 region,verdict='amended',change=r'Use \underline{\underline{R}} for these two observed RQ occurrences.',witness=200)
r.finding('186_190',28,'Preuve de is underlined; the following reference(3.5.1) and stop are plain',
 'The attached emphasis scope already separates these units. The output helper is changed to a literal word rule with the same lexical scope.',
 'Final proof heading',change=r'Retain the scope and typeset \uline{Preuve de} (3.5.1).',witness=200)
r.finding('186_190',29,'The tilde is over Γ alone, with S below Γ',
 'The base of the tilde is Γ and the lower S is outside its scope. The attached widetilde{Γ}_S matches.',
 'Affine-case coherer formula',witness=200)
sid='ASTRA-II-UNDERLINE-189';reason='The proposition words are underlined, except the word de between its two category expressions, which is plain in both scans. Each numbered adjunction assertion underlines pour, la flèche d’adjonction, déduite de, and est un isomorphisme; its numerical references and delimiters stay plain. The two Preuve headings and the final Preuve de are underlined. Proof prose and the author note are plain.'
r.own_finding(sid,189,'Exact proposition, adjunction-assertion and proof-heading word rules','Plain statements and italic emphasis',r'\uline on inspected groups, leaving category-joining de plain',reason,'Proposition3.5, assertions3.5.1/2 and proof headings',witness=200)
old=(ROOT/'build/page_packets/189/diplomatic.tex').read_text();new=old
a=new.index('Si $S$',new.index(r'\textbf{Proposition 3.5.}'));b=new.index(r'\emph{Preuve.}',a)
span=underline_statement(new[a:b],[r'\\begin\{equation\}.*?\\end\{equation\}'])
assert span.count(r'\uline{de}')==1
span=span.replace(r'\uline{de}',r'de')
new=new[:a]+span+new[b:]
a=new.index(r'\begin{enumerate}');b=new.index(r'\end{enumerate}',a)
span=new[a:b]
for word in ['pour','la flèche d\'adjonction','déduite de','est un isomorphisme']:
 assert span.count(word)==2,(word,span.count(word))
 span=span.replace(word,r'\uline{'+word+'}')
new=new[:a]+span+new[b:]
new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}').replace(r'\emph{Preuve de}',r'\uline{Preuve de}')
r.patch(189,'both',old,new,sid,reason)
sid='ASTRA-II-PAREN-189';reason='Each printed parenthetical has three opening parentheses and four closing parentheses. Removing the final unmatched closing delimiter balances the existing reference without changing its tokens or the adjunction maps E→RQ(E) and RQ(E)→E. Diplomatic retains all printed delimiters.'
r.own_finding(sid,189,'Both déduite de references contain an extra closing parenthesis',r'(3.3 b) (ii)) ) and (3.3 b)(ii)) )','Current removes one unmatched closing parenthesis in each reference',reason,'Parentheticals below both adjunction displays',kind='misprint_in_print',witness=200)
r.patch(189,'current','(3.3 b) (ii)) )','(3.3 b) (ii))',sid,reason)
r.patch(189,'current','(3.3 b)(ii)) )','(3.3 b)(ii))',sid,reason)
sid='ASTRA-II-NOTES-189';reason='The call after dévissage immédiat and the footnote label both show a raised numerical1 within baseline parentheses. Its spectral sequence has plain R letters with degree indices and a typed star in the abutment.'
r.own_finding(sid,189,'Explicit numerical1 author note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Final proof opening and complete author note',kind='author_footnote',witness=200)
r.patch(189,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,reason)
sid='ASTRA-II-R-189';reason='The R letters in the two adjunction displays have two horizontal lower rules in both scans. The plain R letters with degree superscripts elsewhere on the page are untouched.'
r.own_finding(sid,189,'Two literal double-underlined R letters',r'\mathbb R',r'\underline{\underline{R}}',reason,'The two adjunction displays',kind='font',witness=200)
r.patch(189,'both',r'\mathbb R',r'\underline{\underline{R}}',sid,reason,2)
r.page(189,'Preuve. Comme f est quasi-compact et quasi-séparé','les inclusions f_i:U_i→S sont des morphismes affines,; author note ends R*Q(E).',
 'All proof prose, references, two adjunction assertions, the entire proposition, affine formula and full author note were compared. Witness200 confirms the plain de between category expressions, the two extra closing delimiters, the literal double lower rules on two R letters and the raised author label1. The final thus d’ailleurs continuation begins on190.',witness=200)
r.commit()
