"""Direct comparison of folio161, including its two partial statements."""
import re
from review_helpers import Review,ROOT
r=Review()
r.finding('161_165',1,'The page begins plexes acycliques',
    'The word complexes is divided com-/plexes at the printed boundary. Both attached markers already preserve com% before the marker and plexes after it.',
    'First word and preceding folio boundary',change='Retain the attached exact split-word boundary.')
r.finding('161_165',2,'Three baseline dots between L^0 and L^m',
    'The ellipsis consists of three low typed stops below arrow height. Both attached ldots forms match.',
    'First proof display')
sid=r.finding('161_165',3,'On a donc un suite exacte',
    'The masculine article un is printed before feminine suite. Correct only the article to une in current and preserve un diplomatically.',
    'Proof b), immediately before the short exact sequence',verdict='not applied and now applied',change='Current un suite exacte→une suite exacte.',witness=172)
r.patch(161,'current','On a donc un suite exacte','On a donc une suite exacte',sid,'Suite is feminine; the printed article has the wrong gender.')
r.finding('161_165',4,'The continued proposition and the opening of Proposition1.2 have underlined word groups',
    'The complete folio was inspected. Its statement groups are underlined, but Si after the first displayed category is plain in both scans and is preserved plain. The page-specific patch records the exact observed groups; later folios are not certified by this item.',
    'Opening continuation and final two lines',verdict='not applied and now applied',change='Apply the inspected lexical underline groups on folio161 only.',witness=172)
sid='ASTRA-II-C-161';reason='Each of the twenty-eight category C letters represented by mathcal C has a separate underline, including those inside D and K and the pseudo-coherence labels. Preserve the observed typed C form, leaving indices outside its rule.'
r.own_finding(sid,161,'Twenty-eight individually underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'All category occurrences',kind='font')
r.patch(161,'both',r'\mathcal C',r'\underline{C}',sid,reason,28)
sid='ASTRA-II-UNDERLINE-161';reason='Only the inspected statement word groups and the proof heading are wrapped in underline commands. Si in the second printed line is visibly plain in the main scan and native witness and stays plain. The proof body stays plain. Removing the newly added wrappers recovers every original textual and mathematical token exactly.'
r.own_finding(sid,161,'Statement word-group rules, with plain Si; underlined Preuve heading','Plain statement prose and italic Preuve',r'\uline on exact inspected groups',reason,'Opening statement, proof heading and Proposition1.2 opening',kind='underline',witness=172)
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/161/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    a=old.index(r'\end{enumerate}')
    top,rest=old[:a],old[a:]
    def topwrap(term,n=1):
        global top
        assert top.count(term)==n,(term,top.count(term),n)
        top=top.replace(term,r'\uline{'+term+'}')
    for term in ['plexes acycliques','est pleinement fidèle et a pour image essentielle','est relevable dans',r'i.e.\ si les objets de','sont projectifs','la catégorie','est réduite aux objets nuls','et par suite le foncteur','est pleinement fidèle','et a pour image essentielle']:
        # The final two groups occur once outside the already wrapped longer group.
        if term=='est pleinement fidèle':
            assert top.count('est pleinement fidèle (')==1
            top=top.replace('est pleinement fidèle (',r'\uline{est pleinement fidèle} (')
        elif term=='et a pour image essentielle':
            assert top.count('(et a pour image essentielle ')==1
            top=top.replace('(et a pour image essentielle ',r'(\uline{et a pour image essentielle} ')
        else:topwrap(term)
    assert rest.count(r'\emph{Preuve.}')==1
    rest=rest.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    pos=rest.index(r'\textbf{Proposition 1.2.}')
    proof,tail=rest[:pos],rest[pos:]
    for term in ['Supposons','localement relevable dans',"localement stable par noyau d'épimorphisme"]:
        assert tail.count(term)==1
        tail=tail.replace(term,r'\uline{'+term+'}')
    assert tail.count(' et localement')==0
    tail=tail.replace(' et '+r'\uline{localement',r' \uline{et} \uline{localement')
    assert tail.count('et faisons les \nhypo%')==1
    tail=tail.replace('et faisons les \nhypo%',r'\uline{et faisons les '+'\nhypo}%')
    new=top+proof+tail
    assert re.sub(r'\\uline\{([^{}]*)\}',lambda m:m.group(1),new)==old.replace(r'\emph{Preuve.}','Preuve.')
    r.patch(161,layer,old,new,sid,reason)
sid='ASTRA-II-INK-161'
r.own_finding(sid,161,'E par E′′, with irregular extra strokes near par','E par E′′','Retain the complete word par without a new punctuation token.',
    'The native witness resolves all three letters of par. A short irregular line before it and a curved stroke beneath its last part do not replace a letter or form the regular straight rule used for lexical underlining elsewhere on the page. The printed sentence remains Quitte à remplacer E par E′′; the same replacement is stated by the following reduction to E′′.',
    'Proof b), Quitte à remplacer',kind='other',verdict='confirmed',witness=172)
r.page(161,'plexes acycliques','et faisons les hypo-',
    'All words, formulas and proof references compared; witness172 inspected at the opening statement and the replacement sentence. Plain Si and the exact com-/plexes and hypo-/thèses folio splits are retained.',witness=172)
r.commit()
