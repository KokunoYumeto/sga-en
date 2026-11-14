"""Folio172: factoriality statement and doubled-origin proof."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('171_175',6,'Only Preuve is underlined in Preuve de 2.2.7.',
    'The rule stops after the word Preuve. The attached emphasis boundary already excludes de and the reference.',
    'Proof heading')
r.finding('171_175',7,'En particulier (EGA IV 21.11.1) : begins its own paragraph',
    'The line is plain and separated from the preceding underlined proposition. Both attached layers already preserve the paragraph break.',
    'Transition from proposition to corollary')
sid='ASTRA-II-O-172';reason='The three structure-sheaf O letters in the final paragraph have individual underlines; the ordinary origin O and its O_1,O_2 labels remain plain.'
r.own_finding(sid,172,'Three underlined sheaf O letters; origin O labels plain',r'\mathcal O',r'\underline{O}',reason,'Last paragraph, sections and restriction map',kind='font')
r.patch(172,'both',r'\mathcal O',r'\underline{O}',sid,reason,3)
sid='ASTRA-II-E-172';reason='All six affine-plane E letters, including the one in the structure-sheaf subscript, have the printed double lower strokes. The attached mathbb E represents these double-marked letters; the ordinary S and origin O labels are separately retained. No mathematical object or map changes.'
r.own_finding(sid,172,'Six double-marked E letters naming the affine plane',r'\mathbb E',r'Retain \mathbb E',reason,'Doubled-origin example',kind='font',verdict='confirmed')
sid='ASTRA-II-UNDERLINE-172';reason='Proposition2.2.7 and Corollary2.2.7.1 have rules under every lexical group, with their mathematical symbols and reference(2.2.5) outside. The two remarks, proof body and En particulier transition are plain. Only Preuve is underlined in its heading. These are the page172 occurrences of the scope noted in checker171–175#5.'
r.own_finding(sid,172,'Underlined proposition and corollary words; plain remarks and proof body','Plain statement prose',r'\uline on inspected lexical groups',reason,'Proposition, corollary and proof heading',kind='underline')
old=(ROOT/'build/page_packets/172/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
new=old
intervals=[]
for label,startword,endmark in [(r'\textbf{Proposition 2.2.7.}','Soit ','En particulier'),(r'\textbf{Corollaire 2.2.7.1.}','Tout ',r'\emph{Preuve}')]:
    start=new.index(startword,new.index(label));end=new.index(endmark,start);intervals.append((start,end))
for start,end in reversed(intervals):new=new[:start]+underline_statement(new[start:end],[r'\(2\.2\.5\)'])+new[end:]
new=new.replace(r'\emph{Preuve}',r'\uline{Preuve}')
r.patch(172,'both',old,new,sid,reason)
r.page(172,'puisque U′ est affine','donc tout faisceau',
    'All proof and remark prose, the factoriality proposition and regular corollary, the projection and restriction maps, and every affine-plane/sheaf/origin letter were individually compared.')
r.commit()
