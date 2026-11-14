"""Folio278: exercise hint, a justified retained C-index and K notation."""
from review_helpers import Review, HERE
import json
r=Review()
r.finding('276_280',3,'278 starts on peut écrire after the semicolon on277',
 'Both adjacent folios have been read: on belongs at the top of278, and the preceding page ends after the semicolon. The supplied markers already preserve that boundary and the space in on peut.',
 'Top boundary',change='Retain the corrected marker placement.')
reason='Instantiate lemma1.8’s preceding dense-set construction with C_0=Ob A, using the exercise’s stated density and the stability of A under finite sums, subobjects and quotients. Let A_0=A and A_i be the full extension category of pairs of A_{i−1} objects. Zero belongs to A_0, and 0→E→E→0→0 gives A_{i−1}⊂A_i. Intersecting an extension with a subobject gives ends E′∩U and im(E′→V); taking a quotient gives ends im(U→E″) and E″/im(U). These ends remain in A_{i−1}, so each A_i remains stable under subobjects and quotients; finite direct sums preserve the same extension sequences. In the C_i recursion, a middle third term is an A_i extension, while an outer third term is a subobject or quotient in A_{i−1}⊂A_i. Conversely an A_i extension is a middle term of such a short exact sequence. Induction gives C_i=Ob A_i via the identity of objects in C, and the full subcategory on C_i is A_i with the identity on morphisms. Thus printed C_{i−1} gives exactly the same recursion in this exercise; the proposed replacement is not forced. The coordinator independently checked this identification.'
r.finding('276_280',4,'extensions de deux objets de C_{i−1}',reason,
 'Exercise1.9 Hint, recursive construction',verdict='amended; printed label retained with explicit identification',
 change='Retain C_{i−1} in both layers; do not introduce the proposed A_{i−1} emendation.',witness=289)
r.finding('276_280',5,'The lowercase direct limit has a rightward lower arrow and no index',
 'The witness leaves the space beneath the arrow empty; the only i at the limit expression is the subscript of A_i. The attached unindexed limit is faithful.',
 'Hint, final homomorphism',change='Retain the existing unindexed direct limit.',witness=289)
r.finding('276_280',7,'parf in D(_A X) has one lower rule',
 'The four notation rows show this rule only under parf; coh, Loclib and Coh remain plain. The actual uparf definition expands to one underline of upright parf with an invisible spacing rule, so the attached occurrence has exactly the observed construction.',
 '2.1, second notation row',change='Retain the existing uparf occurrence.',witness=289)
sid='fixes/RECONCILE_CODEX_6.json#286'
r.source(sid,'dans le cas non respé',
 'Both scans plainly retain the final accented é in the author’s abbreviation. It refers to the primary triangulated branch of lemma1.8: by lemma1.2, cl(E′)−cl(E″)=cl(E′⊕E″[1]), so the second object can be chosen0 there. This exact identity identifies the branch without replacing the author’s abbreviation by resp. The proposed expansion/punctuation normalization is unnecessary.',
 'Opening proof continuation',verdict='rejection confirmed with explicit branch identity',change='Retain non respé in both layers.',witness=289,page=278)
sid='ASTRA-IV-K-DOTS-278'
r.own_finding(sid,278,'The heading has a low dot on its first K and a raised round dot on its second K',r'K_{\bullet} and K^{\bullet}','Retain the two dot levels.',
 'The raised mark is round and sits at cap height, while the nearby apostrophe of d’un is a vertical tick. The first K has the low dot. The current heading already reproduces these two independently observed forms. The broad checker276_280#6 also names279–280 and is completed with those inspections.',
 'Section2 heading',kind='symbol',verdict='retained',witness=289)
sid='ASTRA-IV-UNDERLINE-278';reason='The entire exercise1.9 statement and its hint prose are plain. Only Hint has a lexical lower rule; its colon is outside the rule. The section heading retains accepted heading typography, while the number2.1 and all four notation descriptions are plain.'
r.own_finding(sid,278,'Underlined Hint, plain exercise and plain2.1','Emph Hint and bold2.1',r'uline Hint and plain2.1',reason,'Hint and notation paragraph',kind='underline',witness=289)
r.patch(278,'both',r'\emph{Hint}',r'\uline{Hint}',sid,reason)
r.patch(278,'both',r'\textbf{2.1.}','2.1.',sid,reason)
packet={'record_type':'exact_identification','source_id':'check/findings/findings_276_280.json#4','related_source_id':'fixes/MISPRINTS_6.json#233','page':278,
 'source_reading_status':'decided and retained','printed_reading':'C_{i−1}',
 'image':'scan/SGA6_scan_360dpi.pdf#page=291; scan/SGA6_witness_300dpi.djvu#page=289',
 'source_definitions':{'277':'Lemma1.8: C_0=C′; C_i contains the terms of short exact sequences with two terms in C_{i−1}, in the abelian branch.','278':'Exercise1.9: A is a full subcategory of abelian C, stable under finite sums, subobjects and quotients, with Ob A dense in Ob C; the hint starts A=A_0.'},
 'comparison':reason,
 'explicit_maps':{'object_sets':'id:C_i→Ob A_i, E↦E, with inverse E↦E.','full_categories':'The full subcategory of C on C_i→A_i is the identity on objects and each Hom_C(E,F).'},
 'textual_change':'None; both layers retain C_{i−1}. No replacement theorem is proposed.'}
(HERE/'identification_278.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(278,'on peut écrire, comme on le voit facilement, x=cl(E′)−cl(E″)','Coh(_A X)=catégorie des A-Modules à gauche cohérents…(I3.1).',
 'Every word, symbol and formula was compared with both layers. The author’s non respé abbreviation, the printed C_{i−1}, the barred element arrow E↦cl_C(E), unindexed direct limit, low/raised K dots, the four left-module category subscripts, and the sole parf rule were read in the witness. The exercise is plain rather than sharing the lemma underlining pattern. The exact C_i/Ob A_i identification is saved separately and supports retaining the printed label; no mathematical replacement is inserted.',witness=289)
r.commit()
