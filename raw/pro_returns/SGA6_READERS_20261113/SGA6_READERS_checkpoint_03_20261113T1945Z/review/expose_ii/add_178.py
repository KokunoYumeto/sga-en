"""Folio178: statement conclusion, proof and Stein definition."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('176_180',10,'équivalences de catégories : begins the page',
    'The preceding page has définit des; this folio begins with équivalences. Both attached markers match the directly compared boundary.',
    'First line',change='Retain the existing boundary.')
sid=r.finding('176_180',11,'relativement à la catégories des modules libres',
    'The singular article la governs the one category of finite free modules. Current removes the extraneous plural s from catégories; the indicated category and its modules remain unchanged.',
    'Continuation of Proposition2.3.2(d)',verdict='not applied and now applied',change='Current uses la catégorie; diplomatic preserves la catégories.')
r.patch(178,'current','à la catégories des modules libres','à la catégorie des modules libres',sid,'Restore agreement of the singular article and category noun.')
sid=r.finding('176_180',12,'Modules libres (resp.) facteurs directs de libres) de type fini',
    'The printed parenthesis closes after resp. and again after the alternative phrase. The matching alternative is Modules libres / facteurs directs de libres, both of finite type. Current removes the premature closer after resp. and retains the closer after libres; the two classes and Γ_S remain unchanged.',
    'Last proof sentence',verdict='not applied and now applied',change='Current removes only the premature closer after resp.; diplomatic keeps it.')
r.patch(178,'current','Modules libres (resp.) facteurs directs de libres)','Modules libres (resp. facteurs directs de libres)',sid,'Balance the one parenthetical alternative without changing either module class.')
r.finding('176_180',13,'The complete defined phrase de Stein is plain',
    'The words before and after the defined phrase are underlined, but both de and Stein lack a rule. The attached Stein is already plain. The full statement formatter below protects the complete phrase.',
    'Definition2.4.1',change='Retain plain de Stein inside the restored lexical statement rules.')
for n,letter in [(14,'A'),(15,'B')]:
    r.finding('176_180',n,'Only théorème is underlined in théorème '+letter,
        'The rule ends before the distinguishing letter. The attached emphasis span already has that precise boundary and will be rendered as an explicit word rule.',
        'Definition2.4.1, theorem '+letter+' label')
sid='ASTRA-II-C-178';reason='All nine category C letters in the proof are individually underlined. The two primes and every S/zero index lie outside the C rule.'
r.own_finding(sid,178,'Nine individually underlined C letters',r'\mathcal C',r'\underline{C}',reason,'Complete proof of2.3.2',kind='font')
r.patch(178,'both',r'\mathcal C',r'\underline{C}',sid,reason,9)
sid='ASTRA-II-SITE-178';reason='Three S letters denote the site/topos and are underlined: the proof phrase pour S le topos, the definition’s Soit S un topos, and On dit que S est de Stein. The final-object S and the underlying-space S in the proof are plain and stay unchanged.'
r.own_finding(sid,178,'Three underlined site/topos S letters','Plain S at three identified occurrences',r'\underline{S} at the three exact occurrences',reason,'Proof and Definition2.4.1',kind='font')
for old,new in [(r'pour $S$ le topos',r'pour $\underline{S}$ le topos'),(r'Soit $S$ un topos',r'Soit $\underline{S}$ un topos'),(r'On dit que $S$ est de Stein',r'On dit que $\underline{S}$ est de Stein')]:
    r.patch(178,'both',old,new,sid,reason)
sid='ASTRA-II-O-178';reason='All three structure-sheaf O letters in Definition2.4.1 and its two theorem clauses have individual rules.'
r.own_finding(sid,178,'Three underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'Definition2.4.1',kind='font')
r.patch(178,'both',r'\mathcal O',r'\underline{O}',sid,reason,3)
sid='ASTRA-II-UNDERLINE-178';reason='The entire proposition continuation and the Stein-definition words carry rules, except the plain defined phrase de Stein, the theorem letters A/B, mathematical units and references. The proof is plain apart from Preuve. This is the page178 continuation of checker176–180#7.'
r.own_finding(sid,178,'Underlined statement words with plain de Stein and theorem letters','Plain statement prose with two existing theorem emphasis groups',r'\uline on inspected word groups',reason,'Proposition continuation, proof heading and Definition2.4.1',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/178/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    new=old.replace(r'\emph{théorème}','théorème')
    first=new.index('\n')+1;first_end=new.index(r'\emph{Preuve.}')
    last=new.index('Soit ',new.index(r'\textbf{Définition 2.4.1.}'))
    protected=[r'de Stein',r'\(I 2\.15\.1 \(ii\)\)',r'\(I 3\.1\)',re.escape('«~théorème A~»'),re.escape('«~théorème B~»')]
    new=new[:last]+underline_statement(new[last:],protected)
    new=new[:first]+underline_statement(new[first:first_end])+new[first_end:]
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    for letter in ['A','B']:new=new.replace('«~théorème '+letter+'~»','«~'+r'\uline{théorème} '+letter+'~»')
    r.patch(178,layer,old,new,sid,reason)
r.page(178,'équivalences de catégories :','H^i(S,F)=0 pour i>0.',
    'The three equivalence arrows, full proposition continuation, complete proof with all references and both theorem clauses were compared. The plain de Stein phrase, theorem-label boundaries and all site/object S occurrences were inspected individually.')
r.commit()
