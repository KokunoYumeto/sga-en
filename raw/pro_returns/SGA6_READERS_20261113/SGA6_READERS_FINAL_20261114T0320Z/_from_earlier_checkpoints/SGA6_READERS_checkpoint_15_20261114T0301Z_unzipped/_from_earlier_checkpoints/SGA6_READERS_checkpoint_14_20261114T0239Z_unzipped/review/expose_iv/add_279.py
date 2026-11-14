"""Folio279: the four K groups and the actual local parfait font exception."""
from review_helpers import Review, ROOT, underline_statement
import re
r=Review()
r.finding('276_280',8,'Definition2.2 has one rule under parf; remark2.3(a) has plain parf',
 'The native witness resolves the two occurrences separately. The definition’s existing uparf correctly prints one rule. The later raw parf macro is redefined at the chapter start to underline, so merely retaining that token would lose the actually plain occurrence; the latter is repaired explicitly by ASTRA-IV-PARF-279.',
 'Definition2.2 and the local-index display of remark2.3(a)',verdict='confirmed and supplemented',change='Retain uparf in the definition and print the later occurrence explicitly plain.',witness=290)
sid='ASTRA-IV-PARF-279';reason='The final displayed subscript parf is plainly unruled in both scans, while the definition’s finite-perfect-amplitude subscript above is ruled. The inclusion of the full finite-amplitude category into the full perfect category is the identity on each object and morphism and induces K^•(_A X)→K^•_loc(_A X). The local record preserves the source’s notation for these related categories. Since the chapter macro parf currently inserts a rule, use an explicit upright plain word only at this occurrence.'
r.own_finding(sid,279,'Plain parf in K^•_loc(_A X)=k(D(_A X)_parf)',r'D({}_A X)_{\parf}',r'D({}_A X)_{\mathrm{parf}}',reason,'Remark2.3(a), final display',kind='font',witness=290)
r.patch(279,'both',r'D({}_A X)_{\parf}',r'D({}_A X)_{\mathrm{parf}}',sid,reason)
sid='ASTRA-IV-AUTHOR-NOTE-279';reason='The call after the ambient module category and its bottom note both show raised numerical1 inside baseline parentheses. The following sentence stop lies outside the call; the note prose is plain.'
r.own_finding(sid,279,'Explicit numerical author-note label1',r'\footnote',r'\SGAAuthorFootnote{1}',reason,'Definition2.2, ambient category and bottom note',kind='author_note_label',witness=290)
r.patch(279,'both',r'\footnote{On se permettra',r'\SGAAuthorFootnote{1}{On se permettra',sid,reason)
sid='ASTRA-IV-UNDERLINE-279';reason='The complete lexical statement of definition2.2 is underlined, including all resp. phrases. Its two references(1.1)/(1.5.2), all formulas and the author note remain independent and plain except for their own mathematical glyph rules. The opening continuation and remark2.3(a) prose are plain; named labels retain the accepted statement convention.'
r.own_finding(sid,279,'Definition2.2 word groups; plain opening, remark and note','Plain definition statement',r'Exact lexical uline groups',reason,'Definition2.2',kind='underline',witness=290)
t=(ROOT/'build/page_packets/279/diplomatic.tex').read_text()
for p in r.patches:t=t.replace(p['old'],p['new'])
a=t.index('Soit ',t.index(r'\textbf{Définition 2.2.}'));b=t.index('\n\n'+r'\textbf{Remarques 2.3.}',a)
old=t[a:b];n0=old.index(r'\SGAAuthorFootnote{1}');n1=old.index('}. Nous dirons',n0)+1;note=old[n0:n1]
r.patch(279,'both',old,underline_statement(old,protected=(r'\(1\.1\)',r'\(1\.5\.2\)',re.escape(note))),sid,reason)
r.page(279,'Les deux dernières catégories sont des sous-catégories pleines de la catégorie Mod(_A X)','mais d’une manière générale se prêtent moins bien au calcul des intersections.',
 'Every body and author-note word, six raised K dots and the corresponding low dots, four naive/derived definitions, all left A subscripts, loc/loc b placements and two parf forms were compared with both layers. The first remark formula has no punctuation before its parenthetical explanation; the final display ends with a stop. The only source font repair beyond lexical rules is the explicitly plain parf occurrence whose inherited macro would otherwise underline it. Native witness290 resolves dots, both parf forms and the note geometry.',witness=290)
r.commit()
