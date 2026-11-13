"""Folio181: coefficient categories, a replayed font correction and functor syntax."""
from review_helpers import Review,ROOT,read
import json
r=Review()
r.finding('181_185',1,'où Lib(A) désigne begins the page',
    'The initial où and category name belong to the first printed line. Both attached markers already precede them.',
    'First printed line',change='Retain the existing boundary before où.')
r.finding('181_185',2,'A=Coh(S), B=Mod(S), with plain typed A and B',
    'All four A/B category letters in the declaration and inclusion map are plain typed capitals. The attached plain letters already match.',
    'Proof of Lemma2.4.4, first sentence')
r.finding('181_185',3,'The inline RΓ_S has a double-underlined R',
    'Both lower strokes are visible under the derived-functor letter. The cumulative middle replay preserves those two horizontal rules literally as underline{underline{R}}; retain that observed form.',
    'Proposition2.4.5(a), inline functor before final display',change='Retain the two literal lower rules supplied by the middle replay in both layers.')
sid=r.finding('181_185',4,'The final displayed RΓ_S has a double-underlined R',
    'The display has the same two horizontal lower rules as the inline functor. The middle replay already installs underline{underline{R}} at both the diplomatic equality and current colon. Retain those literal horizontal strokes rather than reverting that completed glyph correction.',
    'Final display',verdict='amended',change='Retain the literal double-underlined R installed by the cumulative middle replay; withdraw the redundant mathbb repair.')
r.source('fixes/REPLAY_MANUAL_6.json#4','Double-underlined R in the displayed RΓ_S=...',
    'The saved replay used an equals-sign anchor, but current had already replaced that sign with a colon. The cumulative middle replay now uses the actual colon anchor and supplies two literal lower rules in both layers. These horizontal rules agree with the page already inspected and with the root regional recheck.',
    'Final display',page=181,verdict='confirmed',change='Retain the middle replay mapping to underline{underline{R}} and the existing layer-specific equality/colon.')
reason='The print has an equals sign between the functor name RΓ_S and its domain. The preceding sentence introduces the fully faithful restriction of RΓ_S:D^+(S)→D^+(A); composing with the inclusion D^b(S)_coh→D^+(S) gives the displayed functor. A colon names that same functor and domain. Current already supplies the colon; diplomatic retains the equality.'
r.finding('181_185',5,'RΓ_S=D^b(S)_coh→D^+(A),',reason,'Final displayed functor',change='Retain the current colon and diplomatic equality, with double-marked R in both.')
for source in ['fixes/RECONCILE_CODEX_6.json#247','fixes/FIXLOG_6_CURRENT.jsonl#355']:
    r.source(source,'An equality between RΓ_S and the displayed domain',reason,'Final displayed functor',page=181,change='Retain the existing corrected colon and printed diplomatic equality.')
sid='ASTRA-II-C-181';reason='Both category C letters in the opening application of I2.7 have individual rules; the zero index stays outside.'
r.own_finding(sid,181,'Two individually underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'Opening proof continuation',kind='font')
r.patch(181,'both',r'\mathcal C',r'\underline{C}',sid,reason,2)
sid='ASTRA-II-O-181';reason='Both structure-sheaf O letters in the proof of2.4.4 are underlined individually, with their S indices outside.'
r.own_finding(sid,181,'Two underlined structure-sheaf O letters',r'\mathcal O',r'\underline{O}',reason,'Proof of2.4.4',kind='font')
r.patch(181,'both',r'\mathcal O',r'\underline{O}',sid,reason,2)
sid='ASTRA-II-PHI-181';reason='The inclusion functor is denoted by a closed-loop phi with a crossing stem. Use the phi form already preserved at the corresponding category-functor occurrences on166–167.'
r.own_finding(sid,181,'Closed-loop phi in the inclusion A→B',r'\varphi',r'\phi',reason,'First proof sentence of2.4.4',kind='font')
r.patch(181,'both',r'\varphi',r'\phi',sid,reason)
sid=r.finding('181_185',6,'The lemma and proposition words on181 are underlined',
    'Every lexical group of Lemma2.4.4 and Proposition2.4.5(a) was inspected. Mathematical units and numbered references remain independent. The two proof bodies are plain, and the Preuve heading has a rule without an added full stop. This record certifies181 only; subsequent pages receive separate observations.',
    'Lemma2.4.4 and Proposition2.4.5(a)',verdict='not applied and now applied',change='Restore the observed lexical rules and preserve the printed unstopped Preuve heading.')
for old,new in [
 ('Sous les hypothèses de (2.4.3), le foncteur canonique',r'\uline{Sous les hypothèses de} (2.4.3)\uline{, le foncteur canonique}'),
 (r'est pleinement fidèle et a pour image essentielle $\mathrm D^b(S)_{\coh}$ (I 2.15).',r'\uline{est pleinement fidèle et a pour image essentielle} $\mathrm D^b(S)_{\coh}$ (I 2.15).'),
 ('Avec les hypothèses et notations de (2.4.3), on a :',r'\uline{Avec les hypothèses et notations de} (2.4.3)\uline{, on a :}'),
 ('Les foncteurs canoniques',r'\uline{Les foncteurs canoniques}'),
 ('sont des équivalences de catégories. En outre le foncteur',r'\uline{sont des équivalences de catégories. En outre le foncteur}'),
 ('induit un foncteur pleinement fidèle',r'\uline{induit un foncteur pleinement fidèle}'),
 (r'\emph{Preuve}',r'\uline{Preuve}')]:
    r.patch(181,'both',old,new,sid,'Restore the directly observed statement word rules through exact lexical anchors, preserving the cumulative literal double-underlined R glyphs and all mathematical and reference tokens.')
r.page(181,'où Lib(A) désigne','RΓ_S=D^b(S)_coh→D^+(A),',
    'Every proof clause, category map, Ext expression, statement and final display was compared. The equals sign, both double-marked R forms and the closed phi were inspected directly; the stale current font replay is resolved.')
# Remove the superseded font patch before the ordinary idempotent commit.
# Its observed glyph is already supplied by review/middle/patches.jsonl.
p=ROOT/'review/expose_ii/patches.jsonl'
rows=[x for x in read('patches.jsonl') if x['source_id']!='check/findings/findings_181_185.json#4']
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
r.commit()
