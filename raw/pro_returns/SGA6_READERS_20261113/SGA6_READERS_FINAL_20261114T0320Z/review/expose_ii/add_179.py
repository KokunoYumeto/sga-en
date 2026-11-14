"""Folio179: ideal typography, a witnessed isomorphism sign and Stein lemma."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
for n,region in [(16,'The quotient F_s/m_sF_s'),(17,'The subsequent definition of the maximal ideal'),(18,'Author note2, maximal ideal of O_{S,s}')]:
    r.finding('176_180',n,'Plain typed m_s for the local-ring maximal ideal',
        'The m has no lower rule at this occurrence. The attached plain m already matches. The six sheaf-ideal occurrences are separately recorded with their observed rules.',region,witness=190)
sid=r.finding('176_180',19,'Six typed sheaf-ideal m letters have individual underlines',
    'The introduced ideal, both terms in the exact sequence, the subsequent quotient and its two global-section occurrences each have a rule under m alone. The native witness confirms this shape together with the plain local m. Replace each of these six fraktur letters with the observed underlined typed letter; indices and all maps remain unchanged.',
    'Remark2.4.1.1, six sheaf-ideal symbols',verdict='not applied and now applied',change='Use underlined m at these six occurrences in both layers.',witness=190)
r.patch(179,'both',r'\mathfrak m',r'\underline{m}',sid,'Represent the six directly observed typed m letters and their individual rules.',6)
for n,printed,region in [(20,'A new paragraph starts Le rédacteur ignore si','After the Nakayama argument'),(21,'A new paragraph starts Le rédacteur ignore également','Before the second editorial question')]:
    r.finding('176_180',n,printed,'The printed indentation marks the separate paragraph. Both attached layers already preserve that break.',region)
sid='ASTRA-II-ISO-179';reason='Both scans show a wave over a straight horizontal bar with plain ends, the printed simeq sign. The attached over-arrow form adds an arrowhead. The identified isomorphism is the evaluation map from global sections of the sheaf F/underlined-m_s F, concentrated at s, to its stalk F_s/m_sF_s. Restore the observed sign while retaining this same identified map and both arguments.'
r.own_finding(sid,179,'A wave over a straight bar in the global-sections/stalk identification',r'\xrightarrow{\sim}',r'\simeq',reason,'Comme on a H^0(S,F/m_sF) ... F_s/m_sF_s',kind='math',witness=190)
r.patch(179,'both',r'\xrightarrow{\sim}',r'\simeq',sid,reason)
sid='ASTRA-II-O-179';reason='All six structure-sheaf O letters have rules under O alone, including the two in author note2 and the local-ring subscripts S,s. No origin symbol is involved on this page.'
r.own_finding(sid,179,'Six underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'Remark, second author note and lemma hypothesis',kind='font',witness=190)
r.patch(179,'both',r'\mathcal O',r'\underline{O}',sid,reason,6)
sid='ASTRA-II-SITE-179';reason='Four site/topos S letters carry rules: the opening Si S, both targets S in author note1, and Soit S un topos in the lemma. The final-object S, module subscripts and all other inspected S letters are plain.'
r.own_finding(sid,179,'Four underlined site/topos S letters','Four exact plain S occurrences',r'\underline{S} at those occurrences',reason,'Opening remark, author note1 and lemma',kind='font',witness=190)
for old,new in [(r'Si $S$ a',r'Si $\underline{S}$ a'),(r'i_s:s\to S',r'i_s:s\to\underline{S}'),(r"d'un fermé de $S$",r"d'un fermé de $\underline{S}$"),(r'Soit $S$ un topos',r'Soit $\underline{S}$ un topos')]:
    r.patch(179,'both',old,new,sid,reason)
sid='ASTRA-II-NOTE-179';reason='The first call and its note label use raised numerical1 inside baseline parentheses; the second call and label use raised numerical2. Both complete author notes were compared, including all maps, ideals and ring symbols.'
r.own_finding(sid,179,'Parenthesized raised1 and raised2 at the respective calls and notes',r'Two \footnote commands',r'\SGAAuthorFootnote{1} and \SGAAuthorFootnote{2}',reason,'Remark2.4.1.1 and page foot',kind='other',witness=190)
r.patch(179,'both',r'\footnote{i.e. assez',r'\SGAAuthorFootnote{1}{i.e. assez',sid,reason)
r.patch(179,'both',r'\footnote{i.e. formé',r'\SGAAuthorFootnote{2}{i.e. formé',sid,reason)
sid='ASTRA-II-UNDERLINE-179';reason='All lexical groups in Lemma2.4.3 and items(a),(b) are underlined, including both resp. and stable in the second alternative of(a). Mathematical units, references and item labels remain outside. The preceding remark and examples are plain. These are the directly inspected page179 occurrences of checker176–180#7.'
r.own_finding(sid,179,'Underlined lemma and item words','Plain lemma prose',r'\uline on observed lexical groups',reason,'Lemma2.4.3 and items(a),(b)',kind='underline')
old=(ROOT/'build/page_packets/179/diplomatic.tex').read_text()
for p in r.patches:old=old.replace(p['old'],p['new'])
start=old.index('Soit ',old.index(r'\textbf{Lemme 2.4.3.}'))
new=old[:start]+underline_statement(old[start:],[r'\(2\.[14]\.1\)',r'\(2\.0\)',r'\(I 1\.2\)'])
r.patch(179,'both',old,new,sid,reason)
r.page(179,'Remarque2.4.1.1. Si S a assez de points fermés','sont des équivalences de catégories.; author note2 ends de O_{S,s}.',
    'The full remark, exact sequence, stalk argument, two editorial paragraphs, examples, lemma and both complete author notes were compared. Native witness190 resolves the isomorphism sign and sheaf/local ideal typography.',witness=190)
sid='ASTRA-II-TEX-DELIMITER-179';reason='Replacing the over-arrow command by the observed simeq sign concatenated its control word with the following F. A source space ends the command and preserves the same headless relation followed by F_s/m_sF_s. TeX consumes this token delimiter without introducing a new mathematical token.'
r.own_finding(sid,179,'The observed headless relation is followed by F_s/m_sF_s',r'\simeqF',r'\simeq F',reason,'Global-sections/stalk identification',kind='tex_syntax',witness=190)
r.patch(179,'both',r'\simeqF',r'\simeq F',sid,reason)
r.commit()
