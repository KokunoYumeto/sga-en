"""Direct folio163 review, with folio164 comparison of its continued C′_S."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('161_165',7,'Proof part d) starts a separate paragraph',
    'The print starts d) at the left margin on a new line with paragraph separation. Both attached layers already preserve that break.',
    'Opening proof, transition from c) to d)')
r.finding('161_165',8,'EGA 0_I 5.2.3, without a comma after I',
    'There is no comma between the chapter indicator and 5.2.3. Both attached layers match the printed citation.',
    'Lemma2.1.1 reference')
sid=r.finding('161_165',9,'The newly introduced C′_S has no underline',
    'Native witness174 confirms that this one C′ lacks a rule. The same category is the domain of Γ_S and of the exact-sequence hypotheses on the directly compared following folio164, where C′ is individually underlined throughout. Its inclusion C′_S→C_S is the one explicitly specified in the definition, and each subsequent occurrence denotes this same subcategory. Diplomatic retains plain C′ here; current uses the underlined C form consistently for that identified category.',
    'Lemma2.1.2, introduced subcategory after S∈ob S',verdict='amended',
    change='Keep plain C′_S diplomatically; current changes this occurrence to underlined C′_S.',witness=174)
r.patch(163,'current',r"$C'_S$",r"$\underline{C}'_S$",sid,'The printed plain C′ and the underlined C′ on164 name the same explicitly included subcategory; current preserves one form for that category.')
sid='ASTRA-II-C-163';reason='The five other category C letters have visible individual underlines, including C_{1S} in the opening quotient and C,C_0,C_S,C_{0S} in Lemma2.1.2. The separately adjudicated plain C′ occurrence is excluded from this replacement.'
r.own_finding(sid,163,'Five underlined C letters; separately observed plain C′',r'\mathcal C',r'\underline{C}',reason,'All five mathcal C occurrences',kind='font',witness=174)
r.patch(163,'both',r'\mathcal C',r'\underline{C}',sid,reason,5)
sid='ASTRA-II-SITE-163';reason='The three topos pairs (S,A), the three ob S membership targets, and the S-category adjective all carry site-S underlines. These seven exact occurrences are changed together; all fiber indices and the objects in covering arrows stay unchanged.'
r.own_finding(sid,163,'Seven underlined site S occurrences',r'plain site S',r'\underline{S} at the seven observed occurrences',reason,'Notation paragraph and both lemma statements',kind='font',witness=174)
for old,new,count in [(r'$(S,A)$',r'$(\underline{S},A)$',3),(r'\in\Ob S',r'\in\Ob \underline{S}',3),(r'$S$-catégorie',r'$\underline{S}$-catégorie',1)]:
    r.patch(163,'both',old,new,sid,reason,count)
sid='ASTRA-II-OBJECT-S-163';reason='The object S in On suppose que S est quasi-compact has a short rule in both scans. The immediately preceding declaration S∈ob S and the covering arrows S_i→S identify it with the same plain object S. Preserve this isolated printed rule diplomatically; current uses plain object S consistently while the site S remains underlined. No object or morphism is changed.'
r.own_finding(sid,163,'An underlined object S in On suppose que S est quasi-compact','Plain S in both attached layers',{'diplomatic':r'On suppose que $\underline{S}$ est quasi-compact','current':r'On suppose que $S$ est quasi-compact'},reason,'Lemma2.1.1 second sentence',kind='font',witness=174)
r.patch(163,'diplomatic',r'On suppose que $S$ est quasi-compact',r'On suppose que $\underline{S}$ est quasi-compact',sid,reason)
sid='ASTRA-II-UNDERLINE-163';reason='The two lemma statements have lexical underlining, except the defined descriptions quasi-compact and engendré par ses sections, which are plain. Both omissions of a rule were directly inspected; the former was also checked in the native witness. The proof paragraphs and notation prose remain plain. Removing the new lexical wrappers recovers the original tokens exactly.'
r.own_finding(sid,163,'Underlined lemma prose with two plain defined descriptions','Plain lemma prose',r'\uline on observed groups, excluding quasi-compact and engendré par ses sections',reason,'Lemma2.1.1 and opening of Lemma2.1.2',kind='underline',witness=174)
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/163/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    label=old.index(r'\textbf{Lemme 2.1.1}')
    start=old.index('Soient ',label);end=old.index(r'\end{enumerate}',start)+len(r'\end{enumerate}')
    first=underline_statement(old[start:end],[r'quasi-compact',r'engendré par ses sections'])
    second_label=old.index(r'\textbf{Lemme 2.1.2.}',end)
    second_start=old.index('Soient ',second_label)
    second=underline_statement(old[second_start:],[r'\(I 1\.3 d\)\)'])
    new=old[:start]+first+old[end:second_start]+second
    r.patch(163,layer,old,new,sid,reason)
r.page(163,'c) Compte tenu de (1.2 a))','On suppose que',
    'Every word, formula and reference compared, including the plain defined descriptions. Native witness174 checked the lemma wording and the un-underlined C′. The continuing category on164 was independently viewed before the current-form decision.',witness=174)
r.commit()
