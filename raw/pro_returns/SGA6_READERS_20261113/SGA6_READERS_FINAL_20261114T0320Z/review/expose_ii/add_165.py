"""Folio165: natural Hom map, replayed point, and lemma typography."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
obs={
15:('Hom in the opening paragraph has an individual underline','The rule covers the sheaf-Hom operator only. Both attached underlined Hom commands match.','First paragraph'),
16:('The placeholder in Hom_{A_S}(.,G) is a baseline stop','The dot sits at the baseline, and both attached layers already use a literal full stop.','Hom functor applied to(*)'),
21:('Plain A and B name the abelian categories','Both names are ordinary typed capitals. Both attached layers already retain their plain forms.','Lemma2.1.3 opening'),
22:('Plain A→B in the functor declaration','The two category letters have no individual underlines or script forms. Both attached declarations match.','φ:A→B'),
23:('Plain A in M∈ob A','The category letter is ordinary type in the membership condition. Both attached layers match.','Lemma2.1.3 a)'),
24:('Plain A in the first L∈ob A','The category letter has the same ordinary form as in the declaration. Both attached layers match.','Condition(i)'),
25:('Plain A and B as the two Ext subscripts','The typed subscript capitals are ordinary letters, and both attached Ext expressions match.','Condition(i), Ext display'),
26:('Plain A in the final L∈ob A','The final category letter is ordinary type. The final line is wholly on165.','Condition(ii), final line'),
27:('Closed phi in φ:A→B','The drawn glyph is a loop crossed by a stroke, represented by the existing phi command.','Functor declaration'),
28:('Closed phi in induite par φ','The same loop-and-stroke glyph is used in the parenthesis. Both attached phi commands match.','Condition(i) parenthesis'),
29:('Two closed phi glyphs in the Ext display','Both drawn functor symbols have the closed-loop form. Both attached phi commands match.','Ext_B arguments')}
for n,(printed,reason,region) in obs.items():r.finding('161_165',n,printed,reason,region)
sid=r.finding('161_165',17,'Hom_{A(S)}(.,Γ_S(F)) uses a baseline placeholder stop',
    'The diplomatic layer already preserves the baseline stop. The current layer corrected F to G but left cdot at this placeholder, so the original replay anchor containing F no longer matched. Change only the placeholder in the existing Γ_S(G) expression.',
    'Functor applied to(**)',verdict='not applied and now applied',change='Current Hom_{A(S)}(cdot,Γ_S(G))→Hom_{A(S)}(.,Γ_S(G)).')
r.patch(165,'current',r'\operatorname{Hom}_{A(S)}(\cdot,\Gamma_S(G))',r'\operatorname{Hom}_{A(S)}(.,\Gamma_S(G))',sid,'The inspected placeholder is a baseline stop; retain the independently established G correction.')
r.source('fixes/REPLAY_MANUAL_6.json#3','Baseline stop before Γ_S(F) in print',
    'The failed replay retained the old F anchor, while current had already changed that variable to G. The point is now restored at its exact current occurrence without reversing the variable correction.',
    'Functor applied to(**)',verdict='not applied and now applied',change='Place the baseline-stop correction in Hom_{A(S)}(.,Γ_S(G)).',page=165)
reason='The functor applied to the A(S)-module presentation(**) is Hom_{A(S)}(−,Γ_S(G)): it is compared with Hom_{A_S}(−,G) applied to(*). The two right-hand bottom terms explicitly have Γ_S(G) as their second argument. Thus Γ_S(G), already in current, is the required fixed second argument; diplomatic retains Γ_S(F).'
r.finding('161_165',18,'The print writes Γ_S(F) as the second argument',reason,'Functor applied to(**)',change='Retain diplomatic F and the already-corrected current G.')
r.source('fixes/FIXLOG_6_CURRENT.jsonl#347','Γ_S(F)',reason,'Functor applied to(**)',change='Retain current Γ_S(G).',page=165)
reason='Applying Hom_{A(S)}(−,Γ_S(G)) to the displayed sequence(**) gives the left term Hom_{A(S)}(Γ_S(F),Γ_S(G)). The vertical comparison sends an A_S-linear sheaf map F→G to its section map Γ_S(F)→Γ_S(G). Restore those two section functors in the bottom-left term in current; the upper sheaf Hom(F,G) remains unchanged.'
sid=r.finding('161_165',19,'The first bottom Hom has arguments(F,G)',reason,'Bottom-left nonzero diagram term',verdict='not applied and now applied',change='Current Hom_{A(S)}(F,G)→Hom_{A(S)}(Γ_S(F),Γ_S(G)).')
r.patch(165,'current',r'\operatorname{Hom}_{A(S)}(F,G) \arrow[r]',r'\operatorname{Hom}_{A(S)}(\Gamma_S(F),\Gamma_S(G)) \arrow[r]',sid,reason)
reason='No punctuation separates the two finite clauses ending isomorphismes and beginning il en est donc. A semicolon marks that clause boundary in current while retaining the two claims and their order exactly. Diplomatic retains the printed absence.'
sid=r.finding('161_165',20,'des isomorphismes il en est donc, with no separator',reason,'First sentence after the diagram',verdict='not applied and now applied',change='Current inserts a semicolon after isomorphismes.')
r.patch(165,'current','des isomorphismes il en est donc','des isomorphismes ; il en est donc',sid,reason)
sid='ASTRA-II-C-165';reason='All seven category C letters in the proof have individual rules beneath C. Their primes and S or0S subscripts lie outside the rules. The later lemma uses the independently inspected plain A,B category notation.'
r.own_finding(sid,165,'Seven underlined C letters; plain A,B in the new lemma',r'\mathcal C',r'\underline{C}',reason,'Proof category symbols',kind='font')
r.patch(165,'both',r'\mathcal C',r'\underline{C}',sid,reason,7)
sid='ASTRA-II-UNDERLINE-165';reason='All lexical groups of Lemma2.1.3 on this folio, including induite par in parentheses, have visible underlines. Mathematical letters and formulas retain their independent typography. The preceding proof body is plain. The literal token-identity assertion checks the added wrappers.'
r.own_finding(sid,165,'Underlined lemma word groups','Plain lemma prose',r'\uline on the inspected statement groups',reason,'Lemma2.1.3 opening through the final line',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/165/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    label=old.index(r'\textbf{Lemme 2.1.3.}');start=old.index('Soient ',label)
    new=old[:start]+underline_statement(old[start:])
    r.patch(165,layer,old,new,sid,reason)
r.page(165,'d’où la première assertion.','(ii) pour tout L∈ob A, la flèche canonique',
    'Complete proof, both tagged sequences, every diagram node and arrow, all category letters, phi glyphs and the partial lemma statement directly compared. The manual replay point is explicitly placed after the variable correction.')
r.commit()
