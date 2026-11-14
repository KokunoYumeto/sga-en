"""Folio175: statement continuation, repeated numerical author note and proof."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
r.finding('171_175',12,'The proof repeats author call(raised1) after(3.7)',
    'A second numerical1 call appears after the proof reference, referring to the same author note as the statement call. Both attached layers already repeat it; explicit label preservation is patched separately.',
    'First line of proof of2.2.9')
r.finding('171_175',13,'The R of RΓ_S is double-underlined',
    'The two lower strokes are visible under the derived-functor R. The attached mathbb R already represents this form.',
    'Remark2.2.10(a), derived global-section functor')
reason='The printed F^i∈ob L(S)) has a second closing parenthesis after the completed category expression. Its matching opener is the single parenthesis of L(S). Current already removes the unmatched extra closer; diplomatic retains it.'
r.finding('171_175',14,'F^i∈ob L(S)) pour i>m',reason,'Proposition2.2.9(b)',change='Retain the diplomatic extra closer and the existing corrected L(S).')
for source in ['fixes/RECONCILE_CODEX_6.json#236','fixes/FIXLOG_6_CURRENT.jsonl#353']:
    r.source(source,'F^i∈ob L(S))',reason,'Proposition2.2.9(b)',page=175,change='Retain the existing corrected removal of one unmatched closing parenthesis.')
r.finding('171_175',15,'The body ends dont l’image essentielle est',
    'The article la is absent from the end of this printed page; the footnote follows separately. Both attached layers already end the body with est.',
    'Last body line and folio176 boundary',change='Retain the existing boundary before la.')
sid='ASTRA-II-L-175';reason='Four category L letters carry individual rules: the two terms of the first quotient, the term F^i∈ob L(S), and L(S)=Lib(S). This completes the directly inspected page175 continuation of checker171–175#8.'
r.own_finding(sid,175,'Four individually underlined category L letters','L(S)',r'\underline{L}(S)',reason,'First display, item(b), and remark(a)',kind='font')
r.patch(175,'both','L(S)',r'\underline{L}(S)',sid,reason,4)
sid='ASTRA-II-O-175';reason='The single structure-sheaf O in the affine-scheme remark has a rule under its letter alone.'
r.own_finding(sid,175,'One underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'Opening of Remark2.2.10(a)',kind='font')
r.patch(175,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-NOTE-175';reason='The statement call, repeated proof call and footnote label all have the numerical1 raised within baseline parentheses. The complete note reads Le §3 est indépendant du reste de l’exposé. Preserve one explicit author label and its repeat independently of editorial numbering.'
r.own_finding(sid,175,'Three occurrences of parenthesized raised1',r'\footnote and \footnotemark[\value{footnote}]',r'\SGAAuthorFootnote{1} and \SGAAuthorFootMark{1}',reason,'Statement after(3.7), proof after(3.7), and page foot',kind='other')
r.patch(175,'both',r'\footnote{Le \S~3',r'\SGAAuthorFootnote{1}{Le \S~3',sid,reason)
r.patch(175,'both',r'\footnotemark[\value{footnote}]',r'\SGAAuthorFootMark{1}',sid,reason)
sid='ASTRA-II-UNDERLINE-175';reason='Every lexical group of the statement continuation and item(b) carries a rule, including the quoted dimension description. Mathematical units, numbered references, author note and item controls remain independent. The proof and remark are plain except the Preuve heading.'
r.own_finding(sid,175,'Underlined statement words and Preuve heading','Plain statement prose',r'\uline on the inspected groups',reason,'Statement continuation through item(b), and proof heading',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/175/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    start=old.index('\n')+1;end=old.index(r'\emph{Preuve.}')
    note=r"\SGAAuthorFootnote{1}{Le \S~3 est indépendant du reste de l'exposé.}"
    new=old[:start]+underline_statement(old[start:end],[re.escape(note),r'\(I (?:2\.15|4\.[89])\)',r'\(3\.7\)'])+old[end:]
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    r.patch(175,layer,old,new,sid,reason)
r.page(175,'sont pleinement fidèles et ont pour image essentielle','dont l’image essentielle est; author note ends du reste de l’exposé.',
    'Every statement and proof clause, quotient term, interval, final derived functor and complete numerical author note was compared. Both numerical calls were individually inspected.')
r.commit()
