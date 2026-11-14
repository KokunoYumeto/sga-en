"""Folio277: exact/dense subsets, local underline exceptions and proof."""
from review_helpers import Review, ROOT, underline_statement
r=Review()
r.finding('276_280',1,'277 begins Il résulte aussitôt',
 'The complete Il résulte opening lies on277, after the preceding displayed homomorphism and author note. Both attached layers now place Il below the277 marker and retain its separating whitespace.',
 'Top boundary',change='Retain the corrected marker position.')
r.finding('276_280',2,'The canonical k(A)→k(D_A^b(C)) map completes the running sentence with a stop',
 'The attached layers already reproduce the same symbols, parentheses and final stop inline. The permitted display-layout convention gives no further content change at this locus.',
 'Opening sentence',verdict='layout observation accepted without further content patch',change='Retain the existing map and punctuation.',witness=288)
sid='ASTRA-IV-O-277';reason='The two structure-sheaf O letters in remark1.6.1 each have one individual lower rule; their S subscripts remain outside the rule. The surrounding category letters A and C remain plain.'
r.own_finding(sid,277,'Two singly underlined O_S letters',r'\mathcal O_S',r'\underline{O}_S',reason,'Remark1.6.1, the two module categories',kind='font',witness=288)
r.patch(277,'both',r'\mathcal O_S',r'\underline{O}_S',sid,reason,2)
sid='ASTRA-IV-UNDERLINE-277';reason='Definition1.7 and lemma1.8 have lexical lower rules, with two exact exceptions in the definition: the first defining word exact and the defining word dense are plain. The earlier sous-ensemble in est un sous-ensemble remains underlined, and the later repeated sous-ensemble exact de is fully underlined. The cf. is underlined while its EGAIII3.1.1 locator is plain. The proof label has a rule; remark and proof prose remain plain. These scopes were resolved from the native witness, not inferred from the inherited emph spans.'
r.own_finding(sid,277,'Definition and lemma word groups with two plain defining-word exceptions','Plain statements with emph sous-ensemble exact and emph dense',r'Exact lexical uline groups, retaining the observed plain exact/dense',reason,'Definition1.7, lemma1.8 and proof label',kind='underline',witness=288)
t=(ROOT/'build/page_packets/277/diplomatic.tex').read_text()
a=t.index('Soient ',t.index(r'\textbf{Définition 1.7.}'));b=t.index('\n\n'+r'\textbf{Lemme 1.8.}',a)
old=t[a:b];plain=old.replace(r'\emph{sous-ensemble exact}','sous-ensemble exact').replace(r'\emph{dense}','dense')
new=underline_statement(plain,protected=(r'(?<=sous-ensemble )exact(?= \(cf\.)',r'(?<=est )dense(?= dans)',r'EGA III 3\.1\.1'))
r.patch(277,'both',old,new,sid,reason)
a=t.index('Soient ',t.index(r'\textbf{Lemme 1.8.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(277,'both',old,underline_statement(old),sid,reason)
r.patch(277,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
r.page(277,'Il résulte aussitôt de(1.4) que varphi est inverse de l’homomorphisme canonique','k(C)_i=k(C)_0. Soit alors x∈k(C);',
 'Every word, formula, superscript and subscript was compared with both layers. The opening varphi has the same curled form as276. Both definition triangles and all three resp. forms, the two exact underline exceptions, each index threshold i≥1/i≥0, C_{i−1}, and k(C)_{i+1} were checked. The final punctuation is a semicolon. Native witness288 resolves the structure-sheaf rules and exact statement emphasis; no author note is present.',witness=288)
r.commit()
