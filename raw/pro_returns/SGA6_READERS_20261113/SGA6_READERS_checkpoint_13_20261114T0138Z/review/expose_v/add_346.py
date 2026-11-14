#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=346
qreason=('The canonical map of1.11 is q_A:1+sum a_n t^n↦1+sum[a_n]_n, where[a_n]_n lies in Gr^nA. '
 'Its target is the degree product, as defined on308–309. The inclusion into the augmented ring is phi↦(0,phi). '
 'For A=K[T] with its degree filtration, q_A(1+sum_(n>=1)T^n t^n)=1+sum_(n>=1)T^n, an element of the completed product. '
 'With K=Z its infinitely many nonzero graded coefficients cannot lie in the direct sum: every element of the direct sum has finite degree support. '
 'The next display explicitly writes the same completion hat. Retain the source omission diplomatically and its supplied restoration in current.')
for n,where in ((1,'first inline canonical morphism'),(2,'second inline canonical morphism'),(4,'first displayed target')):
 r.finding('346_350',n,'A low period follows Gr at this occurrence; in the first and displayed occurrences it is covered by the completion hat.',
  'Main360 upper/second strips and native357 top resolve the period and hat endpoints. The supplied placeholder is correct; its physical low form is restored by the separate occurrence-counted patch.',
  where,witness=357)
r.finding('346_350',3,'The second inline Gr expression has no completion hat; the preceding expression and the following display have it.',
 qreason,'second inline canonical morphism',witness=357)
id5=r.finding('346_350',5,'There is a blank after foncteurs sur and before the colon.',
 'Native357 top and the main second strip show no category ink in this space. In1.11, j:G→C gives the degree filtration and epsilon:Id_G→Gr∘j identifies each homogeneous component with its associated graded class. Lemma1.12 sends u:I→H on G to u_Gr∘q on C and is bijective. Applied here to H=G-hat^u∘i∘(K×I), it produces precisely the displayed descended morphism on G. Insert only that category letter in the corrected layer; retain the observed blank diplomatically.',
 'prose between the two displays',verdict='not applied and now applied',change='Diplomatic blank; corrected script G.',witness=357)
r.patch(p,'current',r'foncteurs sur\qquad:',r'foncteurs sur \(\mathcal G\) :',id5,'Name the exact domain category of the descended natural transformation.')
r.finding('346_350',6,'Only a typed prime stands above the second displayed arrow; no gamma is visible before it.',
 'Both main and native357 top show a blank to the left of the prime. The first display labels the morphism gamma-prime; the second is its unique descent through q by1.12, with the j-th coordinate of gamma-prime^i given immediately afterwards by Q-double-prime_(i,j). The exact relation is descended_gamma-prime_Gr(A)∘q_A=H(q)_A∘gamma-prime_A. Thus restoring gamma before this same prime preserves the named transformation and its coefficients.',
 'second displayed arrow label',witness=357)
for id in ('fixes/FIXLOG_6.jsonl#342','fixes/FIXLOG_6_CURRENT.jsonl#307'):
 r.source(id,'No printed id glyph occurs on this folio; the supplied TeX footer renews the local id macro.',
  'This row is an implementation decision, not a scan glyph claim. Retain the scoped renewal so the local operator definition takes effect when already defined. Actual usage glyphs remain subject to their own later image checks.',
  'nonprinted local macro block after the page body',page=p,verdict='scoped implementation retained',change='Retain the existing renewal; no printed text changed.',witness=357)
r.own_finding('ASTRA-V-LOW-MARKS-346',p,
 'Three Gr placeholders and five standalone hatted placeholders are low periods. Both ellipses in gamma-prime^i(1+X1+...+Xn+...) are also low.',
 r'Use \mathord{.} at the eight placeholders and \ldots at the two ellipses.',
 'Restore the inspected low glyphs without changing hat scopes or coefficient indices.',
 'The native upper crop resolves all three Gr periods, both displayed single placeholders and the two polynomial-series ellipses; the upper/lower overlap and lower crop resolve the remaining three prose placeholders. The existing multiplication period in6.1.4 is already low and is retained.',
 'canonical maps, descended map, universal-series argument and final paragraphs',kind='symbol',witness=357)
r.patch(p,'both',r'\,\cdot\,',r'\,\mathord{.}\,','ASTRA-V-LOW-MARKS-346','Preserve three low Gr placeholders.',count=3)
r.patch(p,'both',r'\widehat{\cdot}',r'\widehat{\mathord{.}}','ASTRA-V-LOW-MARKS-346','Preserve five low hatted placeholders.',count=5)
r.patch(p,'both',r'\dots',r'\ldots','ASTRA-V-LOW-MARKS-346','Preserve the two low universal-series ellipses.',count=2)
r.own_finding('ASTRA-V-COEFFICIENT-AGREEMENT-346',p,
 'The sentence whose subject is le j-ieme coefficient ends et sera notee Q-double-prime_(i,j).',
 'Diplomatic notée; corrected noté.',
 'Correct the final participle agreement with the masculine subject coefficient.',
 'The main second strip and native357 top resolve the final e after noté. Both coordinated predicates est la composante isobare and sera noté have le j-ième coefficient as their subject. The coefficient identification remains Q-double-prime_(i,j)=[weight j]Q-prime_(i,j); only the prose ending changes.',
 'paragraph defining Q-double-prime_(i,j)',kind='misprint_in_print',witness=357)
r.patch(p,'current',r"et sera notée \(Q''_{i,j}\)",r"et sera noté \(Q''_{i,j}\)",'ASTRA-V-COEFFICIENT-AGREEMENT-346','Repair only the coefficient-subject agreement.')
packet={
 'record_type':'exact_identification','page':p,
 'source_ids':['check/findings/findings_346_350.json#3',id5,'check/findings/findings_346_350.json#6'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=360','scan/SGA6_witness_300dpi.djvu#page=357'],
 'canonical_map':'q_A(1+sum_(n>=1)a_n t^n)=1+sum_(n>=1)[a_n]_n in1+product_(n>=1)Gr^nA.',
 'ring_inclusion':'I(Gr A)→K×I(Gr A),phi↦(0,phi), identifies the displayed augmentation ideal.',
 'completion_example':'For K=Z,A=Z[T] with F^n=(T^n), f=1+sum_(n>=1)T^n t^n is allowed. Its q image has nonzero T^n component in every degree. The natural inclusion direct_sum Gr^nA→product Gr^nA has finite-support image, so this q image is outside that image.',
 'category_identification':'j:G→C assigns the degree filtration. epsilon_B:B→Gr(jB) sends b_n to its degree-n class, and its inverse takes that homogeneous class to b_n. This natural componentwise isomorphism is the1.11 identification used in1.12.',
 'descent':'For H=G-hat^u∘i∘(K×I) on G,1.12 identifies Nat(I,H) with Nat(G-hat,H∘Gr) by u↦u_Gr∘q. Therefore the descended arrow is a morphism on G, and its gamma-prime label represents the same unique transformation after this exact identification.',
 'coefficient_relation':'For each i,j, Q-double-prime_(i,j) is the weight-j component of Q-prime_(i,j), as printed below the arrow.',
 'source_disposition':'Diplomatic retains the omitted hat, empty category slot and bare prime. Current retains the supplied hat/gamma restoration and now fills the category slot with script G.'
}
(HERE/'identification_346.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'On le munit','On en tire aussitot le resultat.',
 'Full main360 four strips and native357 top/lower compared. Checked every word, all G completion hats and t/u/g indices, the unchanged source g without an added triangle, both canonical inline maps, all three Gr dots and missing-hat variant, blank category slot, bare-prime arrow, two lower ellipses, Q single/double primes and i,j indices, literal notee agreement,6.1.4 lower bound p>=1 with no upper limit, every gamma prime, product period and punctuation, both3.7.2 references and the final sentence. No author note or ruled lexical body span. The nonprinted macro row is explicitly recorded as implementation only.',
 witness='Native357 top/lower: witness_346_top.png and witness_346_lower.png.')
r.commit()
