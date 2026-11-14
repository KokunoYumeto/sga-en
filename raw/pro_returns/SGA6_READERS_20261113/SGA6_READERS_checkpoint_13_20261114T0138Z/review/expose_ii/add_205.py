"""Folio205: rigidity proposition, local proof scope and duplicate note labels."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('201_205',14,'The section f∈H^0(A,Hom(X_s,Y_s)) occurs in the running proposition text',
 'The attached text already places this formula inline, with the same mathematical tokens and final stop as the scan. The governing prompt accepts equivalent display layout; no further content correction arises from this observation.',
 'Proposition2.2, third printed line',verdict='layout observation accepted without further content patch',change='Retain the attached tokens, stop and paragraph boundary.')
r.finding('201_205',15,'The first limit reads lim and the second Lim with a capital L',
 'The two distinct capitalizations are visible in the main scan. The attached varinjlim in the first display and explicit Lim above the rightward arrow in the second already reproduce them. All indexing primes and zero subscripts were compared.',
 'Two limit displays in the proof',change='Retain both existing limit forms.')
sid=r.finding('201_205',16,'S′×V, ou V est un ouvert convexe de R^n',
 'The witness shows no accent on ou here, while the earlier où introducing S′ has its accent. This clause describes the named factor V of the immediately preceding chart; the relative connective où expresses that description. Preserve the unaccented diplomatic form and restore the accent in current.',
 'Proof, description of the target chart',verdict='confirmed; current correction now applied',change='Current alone: ou before V becomes où.',witness=216)
r.patch(205,'current',r"$S'\times V$, ou $V$ est",r"$S'\times V$, où $V$ est",sid,'Restore the accent on the relative connective in current only.')
sid=r.finding('201_205',17,'Both author calls and both matching note labels are raised numerical1 in parentheses',
 'Both original call/text pairs were read directly. Their exact association is Proposition2.2→the Douady attribution, and the later T.F.II3.3.1 call→the paracompact-neighborhood statement. Each pair has matching printed1 labels. Preserve those two observed pairs explicitly in both layers; the proposed sequential2 would replace an attested label by an editorial numbering convention, with no change to either identified note.',
 'Both calls and both complete author notes',verdict='amended; both printed label pairs retained explicitly',change='Use explicit SGAAuthorFootnote{1} for each of the two notes in both layers.',witness=216)
r.patch(205,'both',r'\footnote{',r'\SGAAuthorFootnote{1}{',sid,'Preserve both actual printed numerical1 call/text pairs.',2)
r.finding('201_205',18,'The body ends La proposition sera donc consé-',
 'The final printed body line has the first part consé- before the notes. Both source chunks already put consé% immediately before the following folio marker. Retain this exact split-word boundary.',
 'Final body line',change='Retain the existing consé% ending; do not repeat the marker repair.',witness=216)
reason='The proof begins Soit X′ un voisinage ouvert de x and contains no inserted quantifier. The map(2.1.1) is a morphism of sheaves on X_s; its stalk at x sends the germ of an S-morphism h to the germ of h restricted to X_s. The proof chooses X′ as a chart neighborhood of that point and subsequently uses X′_s. Thus the local point under consideration lies in X_s and the displayed restriction morphism specifies its role. Recording this stalk map supplies the proof-local scope without adding the absent sentence Soit x∈X_s to the transcription.'
r.source('fixes/RECONCILE_CODEX_6.json#260','Soit X′ un voisinage ouvert de x dans X, with no preceding quantifier for x',reason,
 'Actual205, opening of the proof',page=205,verdict='rejection confirmed with explicit local map',change='Retain the printed proof opening and document its pointwise restriction map.',witness=216)
sid='ASTRA-II-O-205';reason='The four O letters in the opening identification and its display each have one individual lower rule.'
r.own_finding(sid,205,'Four individually underlined O letters',r'\cO',r'\underline{O}',reason,'Opening paragraph and first display',kind='font')
r.patch(205,'both',r'\cO',r'\underline{O}',sid,reason,4)
sid='ASTRA-II-R-205';reason='The real-field R in Y=S×R and the two coordinate R letters in the proof each have two horizontal lower rules. The three exponents and products remain unchanged.'
r.own_finding(sid,205,'Three real-field R letters with double lower rules',r'\R',r'\underline{\underline{R}}',reason,'Opening identification and two local coordinate charts',kind='font',witness=216)
r.patch(205,'both',r'\R',r'\underline{\underline{R}}',sid,reason,3)
sid='ASTRA-II-UNDERLINE-205';reason='All lexical groups in Proposition2.2 carry word rules, including i.e., dont l’image par, coïncide avec, au-dessus de, and est mou. The reference(2.1.1) and the mathematical letters are independent. The following proof prose is plain apart from Preuve. The witness resolves each separate lower rule.'
r.own_finding(sid,205,'Underlined proposition word groups and Preuve','Plain proposition words and emphasized Preuve',r'Exact lexical uline groups',reason,'Complete proposition and proof label',kind='underline',witness=216)
t=(ROOT/'build/page_packets/205/diplomatic.tex').read_text()
a=t.index('Soient $X,Y$',t.index(r'\textbf{Proposition}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];new=underline_statement(old,protected=(r'\(2\.1\.1\)',))
r.patch(205,'both',old,new,sid,reason)
r.patch(205,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
r.page(205,'qui est un épimorphisme, comme on le constate aussitôt.','La proposition sera donc consé-; second author note ends voisinages paracompacts.',
 'Every word in the proposition and proof, all sheaf-Hom rules, both limit expressions, every prime and zero index, the literal unaccented ou, and both complete author notes were compared. The witness confirms the detailed proposition word rules and both repeated numerical1 labels. The local point scope of Codex260 is explicitly documented; no absent prose is inserted.',witness=216)
r.commit()
