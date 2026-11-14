"""Folio186: local immersion proof and the four author labels of section3."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
for n,region in [(1,'Displayed inclusion Qcoh(S)→Mod(S)'),(2,'The phrase encore noté phi'),(3,'Author note4')]:
    r.finding('186_190',n,'Closed-loop phi with a crossing stem',
        'The loop is closed at this occurrence. The attached phi form already matches the printed inclusion-functor letter.',region)
r.finding('186_190',4,'quasi-compact et quasi-séparé is underlined',
    'The complete standing-hypothesis phrase has word rules, while the surrounding paragraph is plain. The attached emphasis group has exactly this scope.',
    'First sentence of3.0')
for n in [5,6]:
    r.finding('186_190',n,'Author call(raised3) stands at the right of the inclusion display',
        'The printed call follows the displayed Mod(S) target. The attached mark/text pair already has that position and complete note text; it will receive the explicit observed label3.',
        'Section3.0 inclusion display and author note3')
for n,region in [(7,'Soit p un idéal premier'),(8,'Localization subscript on O_{Y,x}'),(9,'The equality p=0')]:
    r.finding('186_190',n,'A typed p with an individual underline',
        'The native witness confirms the lower rule at this precise occurrence. The attached underlined p matches all three printed local prime-ideal letters.',region,witness=197)
reason='The proof specifies the closed immersion f:X↪Y cut out by I. At the chosen point its ideal I_x is nonzero in the domain R=O_{Y,x}. Every prime P containing I_x is nonzero, and the chain(0)⊊P gives positive height. Thus the positive codimension is that of the closed subspace X=V(I) in Y. Current already changes the subject from printed Y to X, preserving the specified immersion and ideal.'
for source in ['fixes/RECONCILE_CODEX_6.json#252','fixes/FIXLOG_6_CURRENT.jsonl#359']:
    r.source(source,'Donc Y est de codimension>0 en x',reason,'End of the local immersion proof',page=186,change='Retain printed Y diplomatically and the existing corrected subject X.',witness=197)
sid='ASTRA-II-O-186';reason='All five structure-sheaf/local-ring O letters have individual rules: three in the immersion proof and two in author note3. Their indices remain outside.'
r.own_finding(sid,186,'Five underlined O letters',r'\mathcal O',r'\underline{O}',reason,'Proof and author note3',kind='font',witness=197)
r.patch(186,'both',r'\mathcal O',r'\underline{O}',sid,reason,5)
sid='ASTRA-II-NUMBER-186';reason='The paragraph label3.0 is typed in ordinary weight. Preserve this inspected paragraph number independently of the accepted statement-heading convention.'
r.own_finding(sid,186,'Plain paragraph label3.0',r'\textbf{3.0.}','3.0.',reason,'Beginning of section3.0',kind='font')
r.patch(186,'both',r'\textbf{3.0.}','3.0.',sid,reason)
sid='ASTRA-II-NOTES-186';reason='The four calls and note labels use numerical1,2,3,4 raised within baseline parentheses. Note1 follows normal, note2 belongs to the section title, note3 is attached to the inclusion display, and note4 follows étudier. All four note bodies were compared in full.'
r.own_finding(sid,186,'Parenthesized raised labels1,2,3,4',r'Automatic footnote commands',r'Explicit SGAAuthorFootnote/Mark/Text labels1–4',reason,'Four inspected author-note positions and page foot',kind='other')
for old,new in [(r'\footnote{Il suffit',r'\SGAAuthorFootnote{1}{Il suffit'),(r'\footnote{Ce numéro',r'\SGAAuthorFootnote{2}{Ce numéro'),(r'\text{\footnotemark}',r'\text{\SGAAuthorFootMark{3}}'),(r'\footnotetext{',r'\SGAAuthorFootText{3}{'),(r'\footnote{Nous omettrons',r'\SGAAuthorFootnote{4}{Nous omettrons')]:
    r.patch(186,'both',old,new,sid,reason)
sid='ASTRA-II-UNDERLINE-186';reason='All lexical groups of Lemma2.4.8.2 and Lemma3.1 are underlined. Mathematical units, the author note and references remain independent; (AB5) is plain. The proof is plain except Preuve, and only the standing-hypothesis phrase is underlined in3.0.'
r.own_finding(sid,186,'Underlined lemma words, proof heading and standing-hypothesis phrase','Plain statements with existing isolated emphasis',r'\uline on the inspected lexical groups',reason,'Both lemmas, proof heading and3.0',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/186/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    a=old.index('Soient ',old.index(r'\textbf{Lemme 2.4.8.2.}'));b=old.index(r'\emph{Preuve.}',a)
    c=old.index('La catégorie',old.index(r'\textbf{Lemme 3.1.}'))
    note=r'\SGAAuthorFootnote{1}{Il suffit que les anneaux locaux de $Y$ soient intègres.}'
    protected=[re.escape(note),r'\(AB 5\)',r'\(Tohoku 1\.10\.1\)']
    new=old[:c]+underline_statement(old[c:],protected)
    new=new[:a]+underline_statement(new[a:b],protected)+new[b:]
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}').replace(r'\emph{quasi-compact et quasi-séparé}',r'\uline{quasi-compact et quasi-séparé}')
    r.patch(186,layer,old,new,sid,reason)
r.page(186,'Lemme2.4.8.2.(cf.EGA IV18.10.3)','Qcoh(S) possède assez d’injectifs.; note4 ends de confusion à craindre.',
    'Every statement, local-ring argument, section heading, inclusion map and all four complete author notes were compared. Native witness197 confirms the three underlined local p letters and the printed codimension subject Y.',witness=197)
r.commit()
