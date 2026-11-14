#!/usr/bin/env python3
"""Record the coordinator's actual region readings; certify no whole pages.

Evidence: main scan regions personally read at 180–216 dpi, with native
300-dpi witness crops for the thin i strokes on folios 613 and 619.
"""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
new_decisions=[]
new_patches=[]

def decision(n,page,printed,change,reason,region,verdict='confirmed',witness=None):
    row=dict(source_id=f'fixes/REPLAY_MANUAL_6.json#{n}',page=page,
        type='replay',verdict=verdict,printed_reading=printed,
        image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}'+
          (f'; scan/SGA6_witness_300dpi.djvu#page={witness}' if witness else ''),
        region=region,change=change,forms='French layers and corresponding English transfer',
        reason=reason)
    new_decisions.append(row)
    return row

def patch(page,layer,old,new,n,count=1):
    row=next(x for x in new_decisions if x['source_id']==f'fixes/REPLAY_MANUAL_6.json#{n}')
    new_patches.append(dict(page=page,layer=layer,old=old,new=new,
        source_id=row['source_id'],expected_count=count,reason=row['reason']))

decision(3,165,r'\operatorname{Hom}_{A(S)}(.,\Gamma_S(F))',
    r'Current: \cdot becomes the printed baseline period; diplomatic already has it.',
    'The argument placeholder is a baseline period in both adjacent Hom expressions. The replay anchor missed the current layer because its second argument had separately changed from F to G. This decision changes only the placeholder and retains the separate F/G variant.',
    'Paragraph beginning D’autre part; pair of contravariant Hom functors',
    'not applied and now applied')
patch(165,'current',r'\operatorname{Hom}_{A(S)}(\cdot,\Gamma_S(G))',r'\operatorname{Hom}_{A(S)}(.,\Gamma_S(G))',3)

decision(4,181,r'R with two underlines in both RΓ_S expressions; final display has =',
    r'Both R glyphs are represented literally by \underline{\underline{R}} in each layer. The diplomatic = and corrected : are retained.',
    'Both visible R glyphs have two separate rules below the letter. The proposed mathbb substitution is amended to retain those two rules explicitly. The current replay anchor failed because = had already become :. The words induit un foncteur pleinement fidèle identify the displayed map as the restriction of RΓ_S along D^b(S)_coh→D^+(S); this supports the separately registered colon correction.',
    'Proposition2.4.5(a), last two RΓ_S occurrences; main216dpi crop', 'amended')
patch(181,'diplomatic',r'\mathbb R\Gamma_S',r'\underline{\underline{R}}\Gamma_S',4,2)
patch(181,'current',r'\mathbb R\Gamma_S',r'\underline{\underline{R}}\Gamma_S',4)
patch(181,'current','\n'+r'R\Gamma_S:\mathrm D^b','\n'+r'\underline{\underline{R}}\Gamma_S:\mathrm D^b',4)

decision(5,190,r'QE^n\simeq E^n',
    r'Current QE′{}^n\xrightarrow{\sim}E′{}^n becomes QE′{}^n\simeq E′{}^n; diplomatic already uses \simeq.',
    'The printed glyph is a tilde above a horizontal bar, with no arrowhead. The replay anchor was invalidated by the current layer’s independently introduced primes. This decision restores the glyph without deciding those primes.',
    'Paragraph beginning où E, just before d’où finalement', 'not applied and now applied')
patch(190,'current',r"QE'{}^n\xrightarrow{\sim} E'{}^n",r"QE'{}^n\simeq E'{}^n",5)

decision(6,223,r"H^n(i_*(E''))\simeq i_*H^n(E'')",
    r'Current uses \simeq with its separately corrected exponent m.',
    'The lower paragraph prints the isomorphism sign without an arrowhead. Reconciliation changed n to m in the current expression, so the replay anchor no longer matched; the sign change remains applicable at that expression.',
    'Final paragraph of Lemma1.1.1 proof, Comme H^n line; main216dpi lower crop', 'not applied and now applied')
patch(223,'current',r"H^m(i_*(E''))\xrightarrow{\sim}i_*H^m(E'')",r"H^m(i_*(E''))\simeq i_*H^m(E'')",6)

decision(7,252,r'g_\alpha^*(F)\simeq F_\alpha\otimes^{\mathrm L}_{Y_\alpha}\mathcal O_Y',
    r'Current second g_α^* expression uses \simeq; the separate corrected argument F_α is retained.',
    'Both isomorphism signs in the first paragraph have a tilde above a bar without an arrowhead. The first expression is already correct in both layers; this replay concerns the second expression, whose argument was separately corrected from F to F_α.',
    'First paragraph, on a g_α^*(F) line; main216dpi upper crop', 'not applied and now applied')
patch(252,'current',r'g_\alpha^*(F_\alpha)\xrightarrow{\sim}F_\alpha',r'g_\alpha^*(F_\alpha)\simeq F_\alpha',7)

decision(8,351,r'Enfin, Σ_{i=1}^n(−1)^iλ^i(x)=λ_{−1}(x)=∏_{i=1}^n(1−(1,1+T_i))=(−1)^n.∏_{i=1}^n(0,1+T_i).',
    'Keep the equation’s current display placement; no content patch for this replay.',
    'The main scan prints the whole equality after Enfin with its final full stop and the baseline multiplication dot after (−1)^n. The supplied display has the same equation tokens apart from the separately registered lower-bound correction. The requested inline/display move concerns layout, which NOTE_6 accepts; the changed lower bound also explains the failed exact anchor.',
    'Middle of page, equality after Enfin; main216dpi crop', 'reverted')

decision(9,341,r"(n,x).(n',x')=(nn',nx'+n'x+x\cdot_N y) with no following full stop",
    'Remove the current layer’s terminal full stop in (5.5.2); retain the separate y→x′ correction.',
    'The multiplication line ends at its closing parenthesis; the next paragraph begins On considère. The diplomatic layer has already removed the extra point, but the current replay missed its changed final variable.',
    'Display(5.5.2), second line, right end; main216dpi upper crop', 'not applied and now applied')
patch(341,'current',r"(nn',nx'+n'x+x\cdot_N x').",r"(nn',nx'+n'x+x\cdot_N x')",9)

for n,where in [(14,'Definition1.5,(1.5.2)'),(15,'Proposition1.6(i)')]:
    decision(n,619,r'\sigma_1,\ldots,\sigma_i',
      'Already present in both supplied layers; no new patch.',
      'Both inspected scans show a dotted i as the final subscript. It matches the restriction F_i or F_{σ,i} in the same sentence. The literal corrected reading is already present in each supplied layer, so the old σ_1 endpoint cannot match.',
      where+'; main216dpi and witness300dpi middle/lower regions',witness=630)

decision(16,603,r'le sous-foncteur de \underline{\Isom}(L,M) formée',
    'Restore the first Isom underline in the current layer; retain its separate formée→formé correction.',
    'The first Isom is visibly underlined and its (L,M) arguments lie outside the rule. The second Isom below is also underlined. The diplomatic layer already preserves the first rule; the replay missed current formé because it searched formée.',
    'First three lines, continuation of the statement; main216dpi top crop', 'not applied and now applied')
patch(603,'current',r'de \(\Isom(L,M)\) formé',r'de \(\underline{\Isom}(L,M)\) formé',16)

decision(17,600,r'\Pic_{\coprod X_i\prime/S} in the lower Pic sequence; no index under coproduct',
    'Remove the added coproduct index in the current sequence, using its separately corrected X_i argument.',
    'The sequence uses a bare coproduct glyph followed by the indexed X. It has no additional i attached to the coproduct glyph. Diplomatic already has the requested form; the current layer’s prime removal made the original replay anchor absent.',
    'Pic sequence following X_0→coprod X_i→Y; main216dpi middle crop', 'not applied and now applied')
decision(18,600,r'\Pic_{\coprod X_i/S} in Si l’on sait; no index under coproduct',
    'Remove the added i on the two current coproduct glyphs (sequence and following sentence).',
    'The displayed sequence and the following sentence both have bare coproduct glyphs. The two matching current anchors explain the earlier ambiguous application. Each inspected occurrence loses only that extra coproduct index, and the separate prime correction remains intact.',
    'Pic sequence and following Si l’on sait sentence; main216dpi middle crop', 'not applied and now applied')
patch(600,'current',r'\Pic_{\coprod_iX_i/S}',r'\Pic_{\coprod X_i/S}',18,2)

decision(19,613,r'R^i(f_T)_*(F_T)',
    'Already present in both supplied layers; no new patch.',
    'The native300dpi witness resolves the thin superscript as a dotted i. The same i is quantified in pour tout i≥n. Both supplied layers already have that exponent, so the proposed old R^1 reading is absent.',
    'Lemma4.4, parenthesis defining S_n(T); main216dpi and witness300dpi middle crop',witness=624)

# These source records refer to the very same two R glyphs actually inspected.
font_decision=next(x for x in new_decisions if x['source_id'].endswith('#4'))
for source_id in ['check/findings/findings_181_185.json#3','check/findings/findings_181_185.json#4',
                  'fixes/FIXLOG_6.jsonl#895','fixes/FIXLOG_6.jsonl#896',
                  'fixes/FIXLOG_6_CURRENT.jsonl#1062']:
    r=font_decision.copy();r['source_id']=source_id;r['type']='finding' if source_id.startswith('check/') else 'fixlog';new_decisions.append(r)
r=font_decision.copy();r.update(source_id='ASTRA-CONVENTION-R181',type='convention',kind='convention');new_decisions.append(r)

def merge_file(name,rows):
    p=HERE/name
    prior=[json.loads(s) for s in p.read_text().splitlines() if s.strip()] if p.exists() else []
    ids={r['source_id'] for r in rows}
    kept=[r for r in prior if r.get('source_id') not in ids]
    p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in kept+rows))

if __name__=='__main__':
    # Check each patch against the actual original page packet, sequentially.
    pages={}
    for row in new_patches:
        for layer in ['diplomatic','current'] if row['layer']=='both' else [row['layer']]:
            key=(row['page'],layer)
            text=pages.setdefault(key,(ROOT/f'build/page_packets/{key[0]}/{layer}.tex').read_text())
            count=text.count(row['old'])
            assert count==row['expected_count'],(key,row['source_id'],count,row['expected_count'])
            pages[key]=text.replace(row['old'],row['new'])
    merge_file('decisions.jsonl',new_decisions)
    merge_file('patches.jsonl',new_patches)
    print(json.dumps({'region_decisions':len(new_decisions),'patches':len(new_patches),'whole_pages_certified':0}))
