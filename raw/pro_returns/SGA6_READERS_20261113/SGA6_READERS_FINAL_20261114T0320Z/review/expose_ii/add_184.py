"""Folio184: two numerical notes, attribution and the stationary-submodule lemma."""
import re
from review_helpers import Review,ROOT,underline_statement
r=Review()
sid=r.finding('181_185',16,'J. Frish [5] in author note1',
    'The note omits c in Frish. The explicitly cited bibliography item[5], directly inspected at folio220(mainPDF234), spells Frisch, J. and names the analytic-functions paper. That exact citation identifies the same attribution; current supplies its missing c, while diplomatic preserves Frish.',
    'Author note1 to Proposition2.4.8',verdict='not applied and now applied',change='Current reads J. Frisch; diplomatic retains J. Frish.')
r.patch(184,'current','J. Frish [5]','J. Frisch [5]',sid,'Restore the surname spelling in the directly identified bibliography item[5].')
sid=r.finding('181_185',17,'un entier n_0 tel (E_n)_s=(E_{n_0})_s',
    'The printed clause has tel immediately followed by its equation. The conjunction que is missing from the declaration of the property of n_0. Current supplies only que; the integer, equality and bound n≥n_0 remain unchanged.',
    'First sentence of the lemma proof',verdict='not applied and now applied',change='Current inserts que after tel; diplomatic preserves the omission.')
r.patch(184,'current',r'$n_0$ tel $(E_n)_s',r'$n_0$ tel que $(E_n)_s',sid,'Supply the omitted conjunction before the defining equality.')
r.finding('181_185',18,'The filtration has three baseline dots',
    'The dots lie on the baseline between the two containment signs. Both attached layers already use ldots.',
    'Displayed finite filtration')
r.finding('181_185',19,'Both local prime-ideal p_i letters are plain typed p',
    'Neither occurrence carries a rule or fraktur shape. Both attached plain p letters match the printed quotient and following declaration.',
    'Sentence following the filtration')
sid='ASTRA-II-O-184';reason='All ten structure-sheaf/local-ring O letters carry individual underlines, in the proposition, proof, lemma and local filtration argument. The S,s and s indices remain outside their rules.'
r.own_finding(sid,184,'Ten individually underlined O letters',r'\mathcal O',r'\underline{O}',reason,'All ten sheaf and local-ring occurrences',kind='font')
r.patch(184,'both',r'\mathcal O',r'\underline{O}',sid,reason,10)
sid='ASTRA-II-NOTE-184';reason='The proposition-title call and first note use numerical1 raised inside baseline parentheses. The local-connectivity call and second note use numerical2 with the same geometry. Both complete author notes were read, including the attribution and reference[10].'
r.own_finding(sid,184,'Parenthesized raised1 and raised2 at their calls and notes',r'Two \footnote commands',r'\SGAAuthorFootnote{1} and \SGAAuthorFootnote{2}',reason,'Proposition title, connectivity clause and page foot',kind='other')
r.patch(184,'both',r'\footnote{Ce résultat',r'\SGAAuthorFootnote{1}{Ce résultat',sid,reason)
r.patch(184,'both',r'\footnote{Nous admettrons',r'\SGAAuthorFootnote{2}{Nous admettrons',sid,reason)
sid='ASTRA-II-UNDERLINE-184';reason='Every lexical group of Proposition2.4.8 and Lemma2.4.8.1 has a rule, including de Stein in this proposition and the real-analytic parenthetical example. Mathematical units, references and both author notes remain independent. Both proof bodies are plain except their Preuve headings. These are the page184 occurrences of checker181–185#6.'
r.own_finding(sid,184,'Underlined proposition and lemma words','Plain statement prose',r'\uline on inspected lexical groups',reason,'Proposition2.4.8, Lemma2.4.8.1 and proof headings',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/184/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    a=old.index('Soit ',old.index(r'\textbf{Proposition 2.4.8.}'));b=old.index(r'\emph{Preuve.}',a)
    c=old.index('Soit ',old.index(r'\textbf{Lemme 2.4.8.1.}'));d=old.index(r'\emph{Preuve.}',c)
    note=r"\SGAAuthorFootnote{2}{Nous admettrons que les notions de Géométrie analytique locale de [10] s'étendent aux espaces pseudo-analytiques complexes ; la réduction au cas habituel est en effet chaque fois immédiate.}"
    protected=[re.escape(note),r'\(2\.4\.[78]\)',r'\[15\]']
    new=old[:c]+underline_statement(old[c:d],protected)+old[d:]
    new=new[:a]+underline_statement(new[a:b],protected)+new[b:]
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    r.patch(184,layer,old,new,sid,reason)
r.page(184,'Proposition2.4.8.(raised1). Soit S','quitte à se loca-; author note2 ends chaque fois immédiate.',
    'Both full statements, both proof portions, the filtration, all local primes/rings and both numerical author notes were compared. Bibliography220 was consulted only at item[5] for the attribution spelling; no full-page status for220 is inferred.')
r.commit()
