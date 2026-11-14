"""Folio169: exact statement groups, omitted list separator and sheaf O."""
from review_helpers import Review,ROOT
from source_emphasis import underline_words
r=Review()
obs={
23:('Les ouverts, pour, et, forment une base de la topologie de are underlined','The formulas and final S remain independently typed. The existing emphasis boundary follows the observed lexical groups.','Condition(i)'),
24:('Ceux des and qui sont affines recouvrent are underlined','The S_f formula and final S remain outside lexical rules. The attached grouping matches.','Condition(i′)'),
26:('Pour tout and on a are underlined','The formula between the two lexical groups is independently typed. The attached emphasis span preserves their scope.','Condition(iii) introduction'),
27:('somme, non directe, de sous-faisceaux de are underlined','The final F and outer closing parenthesis and stop remain outside the lexical span. The existing grouping matches under the accepted punctuation convention.','Parenthetical explanation of the sum'),
30:('The lexical groups of Lemma2.2.3.1 are underlined','Soient, un schéma, un, Module inversible, L’immersion canonique and est affine carry rules. The mathematical units and terminal stop remain independently typed.','Lemma2.2.3.1 statement')}
for n,(printed,reason,region) in obs.items():r.finding('166_170',n,printed,reason,region)
sid=r.finding('166_170',25,'The lexical words of(ii) are underlined, but both resp. alternatives are plain',
    'Both printed resp. words are outside the lexical rules. The attached broad emphasis span would underline them. Split the exact span to retain the inspected plain alternatives, leaving all text and math tokens unchanged.',
    'Condition(ii)',verdict='amended',change='Split the existing emphasis into three word groups and leave both resp. alternatives outside.')
a=r"\emph{Pour tout $\mathcal O_S$-Module $F$ quasi-cohérent et de type fini, il existe une famille $(r_i)_{i\in I}$ (resp. $(n_i)_{i\in I}$) d'entiers $\ge0$ (resp. $>0$), et un épimorphisme}"
b=r"\emph{Pour tout $\mathcal O_S$-Module $F$ quasi-cohérent et de type fini, il existe une famille $(r_i)_{i\in I}$} (resp. $(n_i)_{i\in I}$) \emph{d'entiers} $\ge0$ (resp. $>0$), \emph{et un épimorphisme}"
r.patch(169,'both',a,b,sid,'Preserve both directly observed plain resp. alternatives within the otherwise underlined item.')
sid=r.finding('166_170',28,'Même condition que, mais, étant un Idéal quasi-cohérent de are underlined; (iii) is plain',
    'The referenced item number is outside the rule between the two lexical groups. Split the existing span at that reference, keeping every text and mathematical token.',
    'Condition(iii′)',verdict='amended',change='Leave the reference(iii) outside the two lexical underline groups.')
r.patch(169,'both',r'\emph{Même condition que (iii), mais $F$ étant un Idéal quasi-cohérent de}',r'\emph{Même condition que} (iii), \emph{mais $F$ étant un Idéal quasi-cohérent de}',sid,'The item reference(iii) is printed without a rule.')
r.finding('166_170',29,'The final O_S in(iii′) has no following full stop',
    'The item ends without a stop in print. Diplomatic already preserves its absence; current already supplies the sentence-ending stop consistently with the surrounding complete items.',
    'End of condition(iii′)',change='Retain the existing diplomatic absence and current full stop.')
sid=r.finding('166_170',31,'No comma follows Module inversible before f∈Γ(X,L)',
    'The Soient declaration introduces X, the invertible module L, and the section f∈Γ(X,L). The missing separator runs the third object into the description of L. Current supplies one comma to delimit the section declaration; the three objects and all their relations remain unchanged.',
    'Lemma2.2.3.1 variable list',verdict='not applied and now applied',change='Current inserts a comma after inversible; diplomatic retains the printed absence.')
r.patch(169,'current',r'inversible $f\in\Gamma(X,L)$',r'inversible, $f\in\Gamma(X,L)$',sid,'Separate the section f from the preceding description of the invertible module L in the declaration list.')
sid='ASTRA-II-O-169';reason='All five structure-sheaf O letters are individually underlined, in the statement, its coproduct and the affine-open lemma/proof. Their scheme subscripts remain outside the rules.'
r.own_finding(sid,169,'Five underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'All five O occurrences',kind='font')
r.patch(169,'both',r'\mathcal O',r'\underline{O}',sid,reason,5)
sid='ASTRA-II-UNDERLINE-169';reason='After the two exact span amendments, twelve emphasis groups represent the observed statement words and two proof headings. The two resp. alternatives, the reference(iii), all formulas and the final mathematical symbols remain outside lexical rules. The formatter verifies the unchanged math units.'
r.own_finding(sid,169,'Twelve inspected lexical emphasis groups after splitting the plain exceptions',r'\emph groups',r'\uline word groups with math preserved',reason,'All statements and proof headings',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/169/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    new,stats=underline_words(old);assert stats['inspected_emphasis_groups']==12
    r.patch(169,layer,old,new,sid,reason)
r.page(169,'(i) Les ouverts S_f','Le faisceau',
    'All five conditions, coproduct and sum, the affine-open lemma, both proof openings and the final indexed covering argument directly compared.')
r.commit()
