"""Folio174: proof, exact category rules and plain continuation exceptions."""
from review_helpers import Review,ROOT,underline_statement
r=Review()
reason9='The noun is printed singular between plural Les and canoniques and introduces the two displayed functors. Current already supplies the plural s; diplomatic preserves foncteur.'
r.finding('171_175',9,'Les foncteur canoniques',reason9,'Proposition2.2.9(a)',change='Retain the existing diplomatic singular and corrected plural.',witness=185)
reason10='The print has two closing parentheses after item c although no opening parenthesis precedes the item label. Current already retains the one label delimiter c); diplomatic preserves both printed closers.'
r.finding('171_175',10,'les assertions c)) résultent',reason10,'Last proof paragraph',change='Retain c)) diplomatically and the existing corrected c).',witness=185)
sid=r.finding('171_175',11,'Ceci achève la démonstration has no following full stop',
    'Both scans leave the complete closing sentence without a stop before the proposition. Diplomatic retains the absence; current supplies its sentence-ending full stop.',
    'End of proof of2.2.8',verdict='not applied and now applied',change='Insert the closing full stop in current only.',witness=185)
r.patch(174,'current','Ceci achève la démonstration\n','Ceci achève la démonstration.\n',sid,'Supply the missing final stop in the complete closing sentence.')
reason234='The condition reference is printed (1 1); the preceding application of(1.1), its condition(ii), and the following(1.1 a)) identify the same numbered proposition. NOTE_6 explicitly supplies missing stops between reference digits in both layers. The printed abbreviation non respée is retained. The separate c)) excess is removed only in current as recorded for checker#10.'
for source in ['fixes/RECONCILE_CODEX_6.json#234','fixes/FIXLOG_6.jsonl#373','fixes/FIXLOG_6_CURRENT.jsonl#350']:
    r.source(source,'(non respée) de (1 1), and c)) later in the proof',reason234,'Proof of2.2.8',page=174,change='Retain both-layer(1.1), retain non respée, and retain the corrected-only c) adjustment.',witness=185)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#351','les assertions c)) résultent',reason10,'Last proof paragraph',page=174,change='Retain the existing corrected c).',witness=185)
for source in ['fixes/RECONCILE_CODEX_6.json#235','fixes/FIXLOG_6_CURRENT.jsonl#352']:
    r.source(source,'Les foncteur canoniques',reason9,'Proposition2.2.9(a)',page=174,change='Retain the existing corrected foncteurs.',witness=185)
sid='ASTRA-II-L-174';reason='All twelve category L letters have individual rules: five L(S), two L(U), four standalone L, and the L in C_0=L. The native witness resolves the faint rules after Loclib(S) ou and relativement à. The generator L_i remains plain. This is the page174 continuation of checker171–175#8.'
r.own_finding(sid,174,'Twelve underlined category L letters','Plain category L',r'\underline{L} in the twelve observed positions',reason,'Proof and first final quotient display',kind='font',witness=185)
for old,new,count in [('L(S)',r'\underline{L}(S)',5),('L(U)',r'\underline{L}(U)',2),('$L$',r'$\underline{L}$',4),(r'\mathcal C_0=L',r'\mathcal C_0=\underline{L}',1)]:
    r.patch(174,'both',old,new,sid,reason,count)
sid='ASTRA-II-C-174';reason='All five category C letters are underlined individually; their zero and 1S indices remain outside the rules.'
r.own_finding(sid,174,'Five individually underlined C letters',r'\mathcal C',r'\underline{C}',reason,'Proof applications of1.1 and1.2',kind='font',witness=185)
r.patch(174,'both',r'\mathcal C',r'\underline{C}',sid,reason,5)
sid='ASTRA-II-SITE-174';reason='The S introduced as the Zariski site has an individual rule; the following scheme S and all other scheme/fiber S letters remain plain. The exact phrase identifies the single site occurrence.'
r.own_finding(sid,174,'Underlined S in pour S le site zariskien de S',r'pour $S$ le site',r'pour $\underline{S}$ le site',reason,'Proof application of1.1',kind='font',witness=185)
r.patch(174,'both',r'pour $S$ le site',r'pour $\underline{S}$ le site',sid,reason)
sid='ASTRA-II-O-174';reason='The sole sheaf O in the category of quasi-coherent finite-type modules has a rule under O alone.'
r.own_finding(sid,174,'One individually underlined structure-sheaf O',r'\mathcal O',r'\underline{O}',reason,'First proof paragraph',kind='font')
r.patch(174,'both',r'\mathcal O',r'\underline{O}',sid,reason)
sid='ASTRA-II-UNDERLINE-174';reason='The opening statement-continuation line is entirely plain in both scans. Proposition2.2.9 and Les foncteur(s) canoniques have lexical rules, whereas the isolated et between the two displays is plain. The witness confirms both plain exceptions. Preuve is underlined; the proof body remains plain.'
r.own_finding(sid,174,'Plain first line and final et; underlined proposition words','Plain proposition words and existing emphasis on Preuve',r'\uline only on the inspected proposition groups and proof heading',reason,'First line, proof heading and Proposition2.2.9',kind='underline',witness=185)
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/174/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    start=old.index('Les hypothèses',old.index(r'\textbf{Proposition 2.2.9.}'))
    new=old[:start]+underline_statement(old[start:],[r'\(2\.2\.8\)',r'(?m:^et$)'])
    new=new.replace(r'\emph{Preuve.}',r'\uline{Preuve.}')
    r.patch(174,layer,old,new,sid,reason)
r.page(174,'est pleinement fidèle et a pour image essentielle','K^{−,b}(Loclib(S))/K^{−,∅}(Loclib(S))→D(S)',
    'The complete proof and proposition opening were compared, including each restriction, reference, category letter and all quotient indices. The native witness resolves the first-line and final-et absence of underlining, the faint L rules, the missing reference stop, the doubled parenthesis and the missing closing sentence stop.',witness=185)
r.commit()
