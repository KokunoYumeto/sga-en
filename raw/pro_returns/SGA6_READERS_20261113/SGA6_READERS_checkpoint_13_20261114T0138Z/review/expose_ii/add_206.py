"""Folio206: cut-off lemma, exact word rules, and a separate author-claim issue."""
import json,re
from review_helpers import Review,ROOT,HERE,underline_statement
r=Review()
r.finding('206_210',1,'The page begins quence du lemme suivant :',
 'The preceding complete page ends consé-. Both attached sources already split the word as consé% before the206 marker and quence after it.',
 'Opening printed line',change='Retain the already-correct split-word marker.')
r.finding('206_210',2,'The lemma conclusion prints s×U without braces around s',
 'This occurrence omits the braces that appear in the hypotheses and proof. The map j_s:U→S×U, u↦(s,u), has image {s}×U; the printed s×U denotes this same fibre image under j_s. This explicit parametrization supports retaining the abbreviated occurrence rather than inserting unprinted braces. All other printed braces remain present.',
 'Lemma2.2.1, conclusion before the two conditions',verdict='retained with explicit fibre parametrization',change='Retain the printed s×U in both layers.',witness=217)
sid='ASTRA-II-R-206';reason='The R letters for the two Euclidean coordinate spaces in the lemma each carry two horizontal lower rules. Their m and n exponents remain unchanged.'
r.own_finding(sid,206,'Two R letters with double lower rules',r'\R',r'\underline{\underline{R}}',reason,'Opening lemma hypotheses',kind='font',witness=217)
r.patch(206,'both',r'\R',r'\underline{\underline{R}}',sid,reason,2)
sid='ASTRA-II-O-206';reason='The two structure-sheaf O letters in the corollary and the three in its author note each have one individual lower rule.'
r.own_finding(sid,206,'Five individually underlined O letters',r'\cO',r'\underline{O}',reason,'Corollary2.3 and its complete author note',kind='font',witness=217)
r.patch(206,'both',r'\cO',r'\underline{O}',sid,reason,5)
sid='ASTRA-II-NOTE-206';reason='The corollary call after mous and its complete author note use a raised numerical1 within baseline parentheses. The note itself is plain prose, including its final reference(2.5).'
r.own_finding(sid,206,'One explicit numerical1 author note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Corollary call and complete author note',kind='author_footnote',witness=217)
r.patch(206,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,reason)
sid='ASTRA-II-UNDERLINE-206';reason='The lexical groups throughout Lemma2.2.1 and its two conditions are underlined, while all three resp. abbreviations are plain. Corollary2.3 likewise underlines its lexical groups, leaving references(2.2),(2.1.1), mathematical units, and the author note independent. The proof has only its Preuve label underlined. All exceptions were inspected in the native witness.'
r.own_finding(sid,206,'Lemma and corollary word rules; plain resp. and references','Unformatted statement prose',r'Exact lexical uline groups',reason,'Complete lemma, corollary and proof label',kind='underline',witness=217)
t=(ROOT/'build/page_packets/206/diplomatic.tex').read_text()
for p in r.patches:t=t.replace(p['old'],p['new'])
a=t.index('Soient ',t.index(r'\textbf{Lemme 2.2.1.}'));b=t.index(r'\begin{itemize}',a)
old=t[a:b];new=underline_statement(old,protected=(r'resp\.',))
r.patch(206,'both',old,new,sid,reason)
for label in ('i','ii'):
 prefix=r'\item[('+label+')] '
 a=t.index(prefix)+len(prefix);b=t.index('\n',a)
 old=t[a:b];r.patch(206,'both',old,underline_statement(old),sid,reason)
r.patch(206,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
a=t.index('Sous les hypothèses',t.index(r'\textbf{Corollaire 2.3.}'))
n=t.index(r'\SGAAuthorFootnote{1}{',a);z=t.index('}. Pour tout fermé',n)+1
old=t[a:];new=underline_statement(t[a:n],protected=(r'\(2\.2\)',))+t[n:z]+underline_statement(t[z:],protected=(r'\(2\.1\.1\)',))
r.patch(206,'both',old,new,sid,reason)
issue={
 'record_type':'author_claim_issue','source_id':'ASTRA-II-AUTHOR-CLAIM-206','page':206,
 'source_reading_status':'decided and retained','textual_change':'None; no replacement theorem proposed.',
 'image':'scan/SGA6_scan_360dpi.pdf#page=220; scan/SGA6_witness_300dpi.djvu#page=217',
 'region':'Corollary2.3, general Hom-sheaf softness and displayed restriction map',
 'printed_passage':'Sous les hypothèses de (2.2), les faisceaux i_s^{-1}Hom(X,Y), Hom(X_s,Y_s) sont mous. ... Pour tout fermé A de X_s, l’application H^0(X_s,i_s^{-1}Hom(X,Y)) → H^0(A,Hom(X_s,Y_s)) déduite de (2.1.1) est surjective. Each Hom here has its printed underline.',
 'definition_evidence':[
  {'page':200,'region':'§1.1, parenthetical conclusion of the mixed-variety definition','printed_passage':'Si S est réduit à un point, une variété mixte de classe C^r au-dessus de S n’est autre qu’une variété de classe C^r au sens usuel.'},
  {'page':204,'region':'§2.0, final sentence','printed_passage':'Les variétes mixtes dont il sera question seront supposées de classe C^r, avec r≥1 (éventuellement r=∞).'},
  {'page':204,'region':'§2.1, definition of the Hom sheaf','printed_passage':'Hom-underlined(X,Y)(U)=Hom(U,Y), pour U ouvert de X.'},
  {'page':205,'region':'Proposition2.2 hypotheses','printed_passage':'Soient X,Y des S-variétés mixtes, et s∈S. On suppose que la fibre X_s est paracompacte et que s admet un système fondamental de voisinages paracompacts.'}
 ],
 'allowed_example':'Take S={s}, r=∞, X=R² and Y=S¹ with their C∞ structure sheaves. Local charts of S¹ are open intervals, so §1.1 includes Y. The fibre X_s=R² is paracompact, and {s} is a paracompact fundamental neighborhood basis. Let A=S¹⊂R² and W={z:1/2<|z|<3/2}. The smooth map h:W→S¹, h(z)=z/|z|, defines a morphism of ringed spaces by pullback φ↦φ∘h and hence a section [h]_A of the printed target sheaf on closed A.',
 'exact_restriction_map':'Here i_s is the identity. The displayed map becomes q:C∞(R²,S¹)→H^0(A,Hom-underlined(R²,S¹)), g↦[g]_A. The sheaf definition on204 identifies its domain with all global smooth maps.',
 'obstruction':'A preimage g of [h]_A would satisfy g|_A=h|_A=id_{S¹}. For the inclusion i:S¹→R² this gives g∘i=id_{S¹}. On fundamental groups, i_* factors through π_1(R²)=0, since the explicit contraction H_t(z)=(1−t)z contracts R². Thus g_*∘i_*=0, whereas (id_{S¹})_*=id_Z on π_1(S¹)=Z. These two induced maps cannot agree. Consequently [h]_A has no preimage under q.',
 'scope':'The obstruction concerns the arbitrary-Y Hom claim and the displayed general restriction assertion. It supplies no replacement theorem. The source statement remains transcribed in both layers; its source reading is fully decided. The proof’s local target-chart inclusions on205 do not identify all the unrestricted H^0 sets: composition with Y′→Y identifies the germs that locally factor through Y′, and does not supply the impossible global extension above.'
}
(HERE/'author_claim_issue_206.json').write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
r.own_finding(issue['source_id'],206,issue['printed_passage'],'Attached general Hom-sheaf claim is faithful','Retain the printed statement; record the separate explicit author-claim obstruction without a textual emendation.',
 issue['allowed_example']+' '+issue['exact_restriction_map']+' '+issue['obstruction']+' See review/expose_ii/author_claim_issue_206.json for definition passages and precise scope.',
 issue['region'],kind='author_claim_issue',verdict='source reading decided and retained; author claim contradicted by the recorded map',witness=217)
r.page(206,'quence du lemme suivant :','déduite de(2.1.1) est surjective.; author note ends(2.5) ci-dessous.',
 'All lemma hypotheses and conditions, the cut-off construction and both formulas, every corollary word and symbol, and the complete author note were compared. Native witness217 resolves the exact statement word rules, three plain resp. occurrences, and numerical1 note. The source reading of the general Hom assertion is decided and retained; a separate author-claim issue records the explicit circle-to-plane restriction obstruction without inventing replacement text.',witness=217)
r.commit()
