"""Folio185: normalized-space map, ideal tildes, restrictions and exact type."""
from review_helpers import Review
r=Review()
r.finding('181_185',20,'liser begins the page after loca- on184',
    'The printed word localiser is divided exactly at loca/liser. Both attached layers already split the TeX word at that boundary.',
    'First printed line',change='Retain the existing loca/liser marker.')
observations={
21:('The local prime ideal p_i has a plain typed p','This is the p_i whose stalk is realized by the coherent ideal introduced next; the attached plain p already matches.','First parenthetical(resp. p_i)'),
22:('The coherent ideal has an underlined p_i','The rule covers p alone. The attached underlined p already preserves the sheaf-ideal form.','First sentence, Idéaux cohérents'),
23:('Three baseline dots in the filtration','The three stops sit at baseline between the containment signs. Both attached layers already use ldots.','Displayed filtration'),
24:('The denominator ideal p_i has an underlined p','The same coherent ideal occurs in O_S/p_i, with its rule visible. Both attached layers match.','Quotient F_i/F_{i+1}'),
25:('Comme O_s est intègre continues the same paragraph','The sentence follows the preceding stalk equality without a new indentation. Both attached layers match.','Transition to reduction'),
26:('réduit alone is underlined at the end of the reduction sentence','The existing emphasis span has exactly that one word; the earlier ordinary réduit in donc en particulier réduit is plain.','quitte à se localiser en s'),
29:('A wide tilde covers the whole product E_n·tilde O_S','The outer tilde is present in the definition of the ideal on the normalized space, as in the display and later restriction. Both attached layers already include it.','Sentence following the p_* display'),
30:('The structural sheaf is O with subscript tilde S','The tilde is over the subscript S at this occurrence; the other algebra occurrences carry the tilde over O. The attached placement already matches.','l’Idéal de O_{tilde S}'),
32:('normal alone is underlined in the reduction clause','The later ordinary normal in S étant normal is plain. The existing emphasis selects the correct first occurrence.','ce qui nous ramène au cas où S est normal'),
33:('Comme(E_n)_s=0 continues the same paragraph','The sentence follows maintenant. without a new paragraph. Both attached layers preserve that continuation.','Transition to the closed immersion'),
34:('étale alone is underlined after définie par E_n est','The two later occurrences of étale are plain. The attached emphasis group has precisely the observed scope.','First étale assertion'),
35:('The page ends Il reste donc à établir le','No further words or colon occur after le on this page. The attached layers already end at the printed word.','Last body line')}
for n,(printed,reason,region) in observations.items():
    r.finding('181_185',n,printed,reason,region,witness=196 if n in [29,30,32,33,34] else None)
sid=r.finding('181_185',27,'On sait(loc. cit.) que S est le spectre analytique',
    'The preceding sentence introduces the normalization tilde S. The finite algebra tilde O_S is its normalization algebra, and the next displayed identity uses the specified projection p:tilde S→S. Its relative analytic spectrum is the domain tilde S of p. Current supplies the missing tilde on this domain label; diplomatic retains the printed S.',
    'Sentence identifying the finite-algebra spectrum',verdict='not applied and now applied',change='Current restores tilde S in the spectrum sentence; diplomatic retains plain S.')
r.patch(185,'current',r'que $S$ est le spectre analytique',r'que $\widetilde S$ est le spectre analytique',sid,'Identify the relative analytic spectrum with the explicitly defined normalization and its projection p.')
sid=r.finding('181_185',28,'(10 II §3 Prop.8), with no square brackets around10',
    'The same work is cited on this page as[10] in IV§3, IV§4 and II§3; the present citation specifies Proposition8 of that last section. Current restores the bibliography-number brackets, identifying the same reference without changing its section or proposition.',
    'Citation immediately before the p_* display',verdict='not applied and now applied',change='Current writes([10] II §3 Prop.8); diplomatic retains the unbracketed10.',witness=196)
r.patch(185,'current',r'(10 II \S3 Prop.8)',r'([10] II \S3 Prop.8)',sid,'Use the same explicit bibliography identifier[10] as the surrounding citations of this work.')
reason31='The introduced open neighborhood is V in tilde S, and the ideal with the outer tilde is a sheaf on tilde S. Its restriction map is the inverse image along V↪tilde S, giving the displayed ideal restricted to V. The earlier U is the open neighborhood on S. The source projection p:tilde S→S relates these neighborhoods. Current already uses the named V in this restriction; diplomatic retains printed U.'
r.finding('181_185',31,'The ideal on tilde S is printed with restriction |U',reason31,
    'V-neighborhood clause',change='Retain the existing current |V and diplomatic |U.',witness=196)
for source in ['fixes/RECONCILE_CODEX_6.json#251','fixes/FIXLOG_6_CURRENT.jsonl#358']:
    r.source(source,'The restriction in the V clause is printed |U',reason31,'V-neighborhood clause',page=185,change='Retain the existing corrected |V.',witness=196)
sid='ASTRA-II-O-185';reason='All eighteen structure-sheaf/algebra O letters have individual underlines. This includes the O under each normalization tilde and the single O with tilde S as its subscript. The existing inner/outer tildes, indices and baseline restrictions remain exactly placed.'
r.own_finding(sid,185,'Eighteen individually underlined O letters',r'\mathcal O',r'\underline{O}',reason,'Entire proof page',kind='font',witness=196)
r.patch(185,'both',r'\mathcal O',r'\underline{O}',sid,reason,18)
sid='ASTRA-II-POINT-185';reason='The proof has explicitly reduced O_{S,s} to an integral local analytic ring. Its stalk is that of the local analytic model in Definition2.4.7 and is henselian. A finite algebra over a henselian local ring decomposes into local factors; its integral-closure algebra here is a domain, so exactly one factor occurs. Consequently the normalization has a unique point tilde s over s, with p(tilde s)=s. This exact lift supports the printed reuse of the label s in the V-neighborhood clause. Preserve that label without inserting an inverse-image expression.'
r.own_finding(sid,185,'un voisinage ouvert V de s dans tilde S','The same printed point label s', 'Retain s using the specified unique lift p(tilde s)=s',reason,'V-neighborhood clause after reduction to an integral local ring',kind='other',verdict='confirmed',witness=196)
sid='ASTRA-II-UNDERLINE-185';reason='The proof has exactly three separately emphasized words: réduit in the reduction sentence, normal in the normalization reduction, and the first étale in the immersion argument. Their existing emphasis spans are exact; the corresponding later plain words remain unchanged.'
r.own_finding(sid,185,'Three isolated underlined words',r'\emph{réduit}, \emph{normal}, \emph{étale}',r'\uline on exactly those three words',reason,'Three proof reductions/assertions',kind='underline',witness=196)
for word in ['réduit','normal','étale']:
    r.patch(185,'both',r'\emph{'+word+'}',r'\uline{'+word+'}',sid,reason)
r.page(185,'liser au voisinage de s','Il reste donc à établir le',
    'The complete proof, filtration, local/sheaf ideal forms, normalization algebra, all inner and outer tildes, p_* identity, open restrictions, local point identification and every occurrence of the three emphasized words were compared. Native witness196 resolves the nested tilde positions and the V-neighborhood clause.',witness=196)
r.commit()
