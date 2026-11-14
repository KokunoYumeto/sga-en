"""Folio177: soft-ring proposition, reference repairs and exact exceptions."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('176_180',6,'D’autre part begins the page',
    'Both the initial D and autre belong to the first printed line. The current marker before D already preserves the complete opening word.',
    'First line',change='Retain the existing marker before D.')
sid8=r.finding('176_180',8,'The amplitude reference is printed(4.8)',
    'The cited definition is Exemple4.8 of ExposéI, directly inspected at folio122(mainPDF136). It defines perfect amplitude for the same derived category of modules by the subcategory of direct factors of finite free modules. The directly compared parallel statement II2.2.9 on175 explicitly cites(I4.8). Current supplies the exposé identifier; the mathematical definition is unchanged.',
    'Proposition2.3.2(c), amplitude reference',verdict='not applied and now applied',change='Current changes(4.8) to(I4.8); diplomatic retains(4.8).')
r.patch(177,'current','(4.8)','(I 4.8)',sid8,'Identify the inspected definition in ExposéI4.8, folio122.')
sid9=r.finding('176_180',9,'The perfect-subcategory reference is printed(4.9)',
    'Notation4.9 in ExposéI, directly inspected at folio122(mainPDF136), names D(S)_parf for exactly the full subcategory of perfect objects used here. The parallel statement on175 explicitly cites(I4.9). Current supplies that exposé identifier without changing the specified subcategory.',
    'Proposition2.3.2(c), essential-image reference',verdict='not applied and now applied',change='Current changes(4.9) to(I4.9); diplomatic retains(4.9).')
r.patch(177,'current','(4.9)','(I 4.9)',sid9,'Identify the inspected notation in ExposéI4.9, folio122.')
sid='ASTRA-II-LOCLIB-177';reason='The native witness confirms a rule under Loclib alone in the first parenthetical alternative of item(a). All other Loclib occurrences on this page are plain. Preserve this one printed operator rule; its argument(S) remains outside.'
r.own_finding(sid,177,'Underlined Loclib in item(a)’s first resp. alternative',r'$\Lib(S)$ (resp. $\Loclib(S)$)',r'$\Lib(S)$ (resp. $\underline{\operatorname{Loclib}}(S)$)',reason,'First clause of item(a)',kind='font',witness=188)
r.patch(177,'both',r'$\Lib(S)$ (resp. $\Loclib(S)$)',r'$\Lib(S)$ (resp. $\underline{\operatorname{Loclib}}(S)$)',sid,reason)
sid='ASTRA-II-NOTE-177';reason='The call after(I1.2) and the author-note label are numerical1 raised inside baseline parentheses. The complete note reads Cette assertion vaut plus généralement pour S paracompact.'
r.own_finding(sid,177,'Parenthesized raised1 at call and note',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Item(a) and page foot',kind='other',witness=188)
r.patch(177,'both',r'\footnote{Cette assertion',r'\SGAAuthorFootnote{1}{Cette assertion',sid,reason)
sid=r.finding('176_180',7,'Statement words are underlined, with plain(resp. stable) in item(a)',
    'The full proposition statement on this folio was inspected. The native witness confirms that the second item(a) alternative(resp. stable) is plain, while the first resp. and its Loclib operator are underlined. The words resp. and pseudo-cohérent in item(b) are underlined. Numbered references, formulas and the author note remain independent. This decision certifies177 only; later pages are recorded separately.',
    'Proposition2.3.2, hypothesis and items(a)–(d)',verdict='not applied and now applied',change='Restore the inspected lexical rules and preserve the plain stable alternative.',witness=188)
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/177/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    start=old.index('Soit ',old.index(r'\textbf{Proposition 2.3.2.}'))
    note=r'\SGAAuthorFootnote{1}{Cette assertion vaut plus généralement pour $S$ paracompact.}'
    new=old[:start]+underline_statement(old[start:],[re.escape(note),r'\(resp\. stable\)',r'\(2\.0\)',r'\(I (?:1\.2|2\.15|4\.[89])\)',r'\(4\.[89]\)'])
    r.patch(177,layer,old,new,sid,'Restore the directly inspected statement rules while protecting the plain exception, all mathematical units and the author note.')
r.page(177,'D’autre part, si A est mou','En outre, il définit des; author note ends pour S paracompact.',
    'All prose and formulas were compared, including the two cohomological reference omissions, the baseline placeholder point in H^0(S,.) and the complete numerical author note. Witness188 resolves the mixed underlining within item(a). ExposéI folio122 was consulted only for the two cited reference regions, with no page-status claim for122.',witness=188)
r.commit()
