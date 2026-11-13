"""Folio168: proposition ending, coherent sheaves, and new theorem opening."""
from review_helpers import Review,ROOT
from source_emphasis import underline_words
r=Review()
obs={
15:('Folio168 starts with D^−(Coh(S))→D(Qcoh(S))','The complete word canonique is the last body word of167. Both attached markers already stand before the opening display delimiter on168.','Page opening'),
17:('est pleinement fidèle et a pour image essentielle is underlined','The lexical rule ends before the displayed-category notation. The attached emphasis span has that exact boundary.','First statement line after the display'),
20:('The corollary opening has lexical underlines','The words Soit, un schéma noethérien, the resp. alternative and Le foncteur canonique are underlined. S retains its separate plain form. The existing span contains those observed word groups.','Corollary2.2.2.1 opening'),
21:('The corollary conclusion has a lexical rule before D^b(S)_coh','The mathematical categories and the reference(I2.15) remain outside the rule. The attached boundary matches.','Corollary2.2.2.1 conclusion'),
22:('The opening statement of Proposition2.2.3 has underlined word groups','Every lexical group from Soit through sont équivalentes was inspected. The reference and final colon remain outside. The structure-sheaf O letters have their own underlines and are patched separately.','Proposition2.2.3 opening')}
for n,(printed,reason,region) in obs.items():r.finding('166_170',n,printed,reason,region)
r.finding('166_170',16,'canonique is underlined at the foot of167',
    'This inherited item is filed under168 but its word is printed at the end of167. That complete folio was directly compared and its emphasis rendering is already patched there.',
    'Folio167, final body word',actual_page=167,change='Retain the existing emphasis span; upright word-group rendering is patched on167.')
r.finding('166_170',18,'D^−(Qcoh(S)_coh has only one closing parenthesis',
    'The outer opening parenthesis after D^− is unclosed in print. Notations2.2.1 on167 defines D^−(Qcoh(S))_coh; current already restores that required close, while diplomatic retains its absence.',
    'Essential-image notation after the first display',change={'diplomatic':r'\mathrm D^{-}(\Qcoh(S)_{\coh}','current':r'\mathrm D^{-}(\Qcoh(S))_{\coh}'})
reason='The print reads tous before singular O_S-Module and singular est. Current already has the singular determiner tout; diplomatic retains the printed tous.'
r.finding('166_170',19,'tous O_S-Module quasi-cohérent est',reason,'Proof of Proposition2.2.2, final sentence',change='Retain diplomatic tous and current tout.')
r.source('fixes/FIXLOG_6_CURRENT.jsonl#348','tous O_S-Module',reason,'Same proof sentence',change='Retain the applied current correction tout.',page=168)
sid='ASTRA-II-C-168';reason='All four fibred-category C letters in the proof have individual underlines beneath C, with zero subscripts outside the rules. Preserve those inspected typed forms.'
r.own_finding(sid,168,'Four individually underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'Proof category definitions and their uses',kind='font')
r.patch(168,'both',r'\mathcal C',r'\underline{C}',sid,reason,4)
sid='ASTRA-II-O-168';reason='The five structure-sheaf O letters have individual underlines, three in the proof and two in Proposition2.2.3. Their subscript S stays outside the rule.'
r.own_finding(sid,168,'Five underlined O_S letters',r'\mathcal O',r'\underline{O}',reason,'Proof and Proposition2.2.3',kind='font')
r.patch(168,'both',r'\mathcal O',r'\underline{O}',sid,reason,5)
sid='ASTRA-II-SITE-168';reason='The first S in prenant pour S le site zariskien de S denotes the site and has an underline; the second is the scheme and remains plain. This exact occurrence map preserves the printed forms and their explicit site-of-scheme relation.'
r.own_finding(sid,168,'Underlined site S, plain scheme S',r'pour $S$ le site zariskien de $S$',r'pour $\underline{S}$ le site zariskien de $S$',reason,'First proof sentence',kind='font')
r.patch(168,'both',r'pour $S$ le site zariskien de $S$',r'pour $\underline{S}$ le site zariskien de $S$',sid,reason)
sid='ASTRA-II-UNDERLINE-168';reason='The five retained emphasis groups correspond to the directly inspected statement word groups and proof heading. Formula bytes and the current-only close-parenthesis and tout corrections remain independent of the formatter.'
r.own_finding(sid,168,'Five inspected emphasis groups',r'\emph groups',r'\uline word groups with formulas unchanged',reason,'Both statement portions and proof heading',kind='underline')
for layer in ['diplomatic','current']:
    old=(ROOT/f'build/page_packets/168/{layer}.tex').read_text()
    for p in r.patches:
        if p['layer'] in ['both',layer]:old=old.replace(p['old'],p['new'])
    new,stats=underline_words(old);assert stats['inspected_emphasis_groups']==5
    r.patch(168,layer,old,new,sid,reason)
r.page(168,'D^−(Coh(S))→D(Qcoh(S))','Les conditions suivantes sont équivalentes :',
    'Complete proof, corollary, its two displays and Proposition2.2.3 opening compared. The degree-n tensor exponents and subscript pairs were individually inspected.')
r.commit()
