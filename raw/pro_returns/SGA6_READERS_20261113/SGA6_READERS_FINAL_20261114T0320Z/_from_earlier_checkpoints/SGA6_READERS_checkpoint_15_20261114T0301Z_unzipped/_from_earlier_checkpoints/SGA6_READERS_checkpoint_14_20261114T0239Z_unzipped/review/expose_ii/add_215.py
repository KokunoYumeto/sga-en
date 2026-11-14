"""Folio215: finiteness theorem, order sequence and Hilbert-complex notation."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
sid=r.finding('211_215',11,'The derived R has two horizontal lower rules',
 'The main region enlarged to ten pixels per PDF point and the native witness show two separate rules below the typed R. Preserve those literal lower strokes at the theorem’s derived direct-image symbol.',
 'Theorem3.2.1, derived direct image',verdict='amended',change=r'Use \underline{\underline{R}} in both layers.',witness=226)
r.patch(215,'both',r'\mathbb{R}',r'\underline{\underline{R}}',sid,'Preserve the two directly inspected horizontal rules beneath the derived R.')
r.finding('211_215',12,'The shifted complex and que nous noterons expression are inline in the proof',
 'The attached text now has the same mathematical token sequence, comma and final stop inline. The governing prompt accepts display layout variation, so this observation requires no further content patch.',
 'Proof, paragraph beginning Pour chaque r',verdict='layout observation accepted without further content patch',change='Retain the attached shifted-complex expressions and punctuation.')
r.finding('211_215',13,'le complexe de faisceaux associés à, with plural associés',
 'Both the opening continuation and the later proof phrase use the plural associés referring to the associated sheaves. The attached plural is already correct.',
 'Proof, sentence defining the section-sheaf complex',change='Retain the existing plural associés.',witness=226)
sid='ASTRA-II-ORDER-215';reason='The order symbol n in the theorem has its own lower rule, independently of the preceding lexical rule under d’ordre. The definition on203 names this sequence underline n=(n_i); the proof here uses its components n_j in m_i=sum_{j<i}n_j. Preserve the directly printed sequence glyph.'
r.own_finding(sid,215,'Individually underlined order sequence n','Plain n in d’ordre',r'\underline{n}',reason,'Theorem3.2.1, elliptic order',kind='symbol',witness=226)
r.patch(215,'both',"d'ordre $n$ de fibrés",r"d'ordre $\underline{n}$ de fibrés",sid,reason)
sid='ASTRA-II-O-215';reason='The theorem’s structure-sheaf O has one individual lower rule, with S outside it.'
r.own_finding(sid,215,'One singly underlined O_S',r'\cO_S',r'\underline{O}_S',reason,'Theorem3.2.1, module category',kind='font',witness=226)
r.patch(215,'both',r'\cO',r'\underline{O}',sid,reason)
sid='ASTRA-II-FIELDS-215';reason='The coefficient C in the theorem and all three integer Z letters in the proof have two horizontal lower rules. Their surrounding indices and quantifiers remain unchanged.'
r.own_finding(sid,215,'One C and three Z letters with double lower rules',r'\mathbb C and \Z',r'\underline{\underline{C}} and \underline{\underline{Z}}',reason,'Theorem module category, two proof parameters and final assertion',kind='font',witness=226)
r.patch(215,'both',r'\mathbb C',r'\underline{\underline{C}}',sid,reason)
r.patch(215,'both',r'\Z',r'\underline{\underline{Z}}',sid,reason,3)
sid='ASTRA-II-PHI-215';reason='The phi in phi_{r−m_i}d^i has a closed loop crossed by a stem; its full nested subscript remains unchanged.'
r.own_finding(sid,215,'One closed-loop phi glyph',r'\varphi',r'\phi',reason,'Definition of the Hilbert-bundle complex near the end',kind='symbol',witness=226)
r.patch(215,'both',r'\varphi',r'\phi',sid,reason)
sid='ASTRA-II-UNDERLINE-215';reason='The theorem’s lexical groups are underlined, including its parenthetical explanation, while references(1.2.5) and(2.5) remain plain. The comma after isomorphe is printed and retained. The proof prose is plain apart from Preuve. In the final assertion(a), Pour and le morphisme canonique each have word rules, with the parameter r∈Z independent.'
r.own_finding(sid,215,'Theorem lexical rules, Preuve label and final assertion words','Plain statement prose and emph proof label',r'Exact lexical uline groups',reason,'Theorem3.2.1 and final assertion(a)',kind='underline',witness=226)
t=(ROOT/'build/page_packets/215/diplomatic.tex').read_text()
for p in r.patches:t=t.replace(p['old'],p['new'])
a=t.index('Soient ',t.index(r'\textbf{Théorème 3.2.1.}'));b=t.index('\n\n'+r'\emph{Preuve.}',a)
old=t[a:b];r.patch(215,'both',old,underline_statement(old,protected=(r'\(1\.2\.5\)',r'\(2\.5\)')),sid,reason)
r.patch(215,'both',r'\emph{Preuve.}',r'\uline{Preuve.}',sid,reason)
a=t.index('(a) Pour ')+len('(a) ');old=t[a:]
r.patch(215,'both',old,underline_statement(old),sid,reason)
r.page(215,'induisant sur les faisceaux de sections le morphisme de faisceaux associés à u_r.','(a) Pour r∈Z, le morphisme canonique',
 'Every theorem and proof word, all raised complex dots, the independently underlined order sequence, the sum bound j<i, each r−m_i shift, the projective-limit formula, and all individual C′/F sheaf rules were compared. The prime remains outside each C rule and the complex dot remains outside the F rule. Native witness226 and the enlarged main R region resolve the literal glyph constructions and exact theorem lexical extents. The final assertion begins here and continues beyond the marker.',witness=226)
r.commit()
