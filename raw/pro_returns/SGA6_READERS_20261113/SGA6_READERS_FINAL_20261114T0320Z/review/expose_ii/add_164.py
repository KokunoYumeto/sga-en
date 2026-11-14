"""Direct folio164 statement, spectral sequence, and author-note review."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
observations={
10:('The page begins with H^1(S,F)=0 pour tout F∈ob C′_S.','The entire display belongs below the folio164 marker. Both attached layers already place the opening display delimiter there.','Page opening'),
11:('Hom has an individual underline in the hypothesis','The rule covers Hom only and leaves its arguments outside. Both attached underlined Hom expressions match.','Lemma2.1.2 a), Hom(G,E)'),
12:('The sheaf Ext is typed and underlined','A visible rule lies under the three letters Ext. The E in the arguments is the surviving corrected uppercase letter. Both attached underlined Ext commands preserve this reading.','Spectral-sequence E_2 term'),
13:('The abutment is Ext with a raised typed asterisk','The mark has the crossed strokes of the typed star; it is not a degree letter. Both attached layers already use the asterisk.','Spectral-sequence abutment'),
14:('Hom is underlined in H^1(S,Hom(G,E))','The individual Hom rule is visible; the arguments and the Ext^1 on the right remain outside it. Both attached layers match.','Final isomorphism')}
for n,(printed,reason,region) in observations.items():r.finding('161_165',n,printed,reason,region)
sid='ASTRA-II-C-164';reason='All eleven category C letters have individual underlines. This includes the repeated C′_S defined on163; its prime remains outside the C rule.'
r.own_finding(sid,164,'Eleven individually underlined C letters',r'\mathcal C',r'\underline{C}',reason,'All category symbols',kind='font')
r.patch(164,'both',r'\mathcal C',r'\underline{C}',sid,reason,11)
sid='ASTRA-II-SITE-164';reason='The first two S letters in the author note denote the site/topos and are visibly underlined. Its last S denotes the final object and is plain. Only the two exact S est occurrences receive underlines.'
r.own_finding(sid,164,'Two underlined site S letters and a plain final-object S','All three standalone S letters plain',r'Underline the two S est occurrences only',reason,'Author note',kind='font')
r.patch(164,'both',r'$S$ est',r'$\underline{S}$ est',sid,reason,2)
sid='ASTRA-II-NOTE-164';reason='The call after filtrantes and its footnote label both show a raised numerical1 inside baseline parentheses. Preserve this explicit author label independently of editorial apparatus numbering. The full note was compared.'
r.own_finding(sid,164,'Parenthesized raised1 at call and note label',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'After limites inductives filtrantes and at the foot of the page',kind='other')
r.patch(164,'both',r'\footnote{hypothèse',r'\SGAAuthorFootnote{1}{hypothèse',sid,reason)
sid='ASTRA-II-UNDERLINE-164';reason='The complete statement prose carries word-group rules, including pour tout within the first display. The displayed mathematics, the reference(I1.2), and the author note are independently typed and stay outside the lexical wrappers. Preuve is underlined and the proof body remains plain.'
r.own_finding(sid,164,'Underlined statement groups, including pour tout','Plain statement prose and pour tout',r'\uline on the inspected lexical groups',reason,'Complete statement and proof heading',kind='underline')
old=(ROOT/'build/page_packets/164/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
start=old.index('\n')+1;end=old.index(r'\emph{Preuve.}')
statement=old[start:end]
# The explicit author-note command and both of its balanced arguments form a
# protected interval. This note contains math and must not acquire prose rules.
mark=statement.index(r'\SGAAuthorFootnote{1}')
brace=mark+len(r'\SGAAuthorFootnote{1}')
depth=1;j=brace+1
while depth:
    if statement[j]=='{' and statement[j-1]!='\\':depth+=1
    if statement[j]=='}' and statement[j-1]!='\\':depth-=1
    j+=1
note=statement[mark:j]
new_statement=underline_statement(statement,[re.escape(note),r'\(I 1\.2\)'])
assert new_statement.count(r'\text{pour tout }')==1
new_statement=new_statement.replace(r'\text{pour tout }',r'\text{\uline{pour tout} }')
new=old[:start]+new_statement+old[end:]
new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
r.patch(164,'both',old,new,sid,reason)
r.page(164,'H^1(S,F)=0 pour tout F∈ob C′_S.','H^1(S,Hom(G,E))≃Ext^1(G,E),',
    'All statement clauses, displays, spectral-sequence marks and the complete numeric author note directly compared. The page ends after the displayed isomorphism; its explanatory sentence starts on165.')
r.commit()
