#!/usr/bin/env python3
"""Close the Adams appendix and preserve both next-exposé macro blocks."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def english(s):return s.replace(r'\text{$(k-1)$-ième coefficient de }',r'\text{$(k-1)$-st coefficient of }')
def variant(p,index,sid,mode,suffix='01'):
    c,d=english(units(p,'current')[index]),english(units(p,'diplomatic')[index]);assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-V-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
variants=[variant(362,4,'check/findings/findings_361_365.json#7','display'),
          dict(id='EN-CONTRIB-V-362-02',page=362,old=r'\uline{if the} \(\psi^k\) \uline{satisfy these identities}',printed=r'\uline{if the} \(\psi^t\) \uline{satisfy these identities}',source='check/findings/findings_361_365.json#9',mode='text'),
          variant(362,17,'check/findings/findings_361_365.json#12','math','03'),
          variant(363,13,'ASTRA-V-COEFFICIENT-363','display'),
          variant(363,15,'check/findings/findings_361_365.json#19','display','02')]
variants[0]['related_sources']=['check/findings/findings_361_365.json#6']
variants[3]['related_sources']=['check/findings/findings_361_365.json#16']
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text());pairs=[p for p in pairs if p['page']!=363]
for layer in ['current','diplomatic']:
    f=units(363,layer)[13];e=english(f);assert f!=e
    pairs.append(dict(page=363,layer=layer,French_literal_unit=f,English_literal_unit=e,expected_multiplicity=1,status='individually reviewed lexical translation only',scope='The complete coefficient display: ième coefficient de becomes st coefficient of. The internal $(k-1)$ token,sign,slash grouping,Phi superscripts,and all remaining syntax are unchanged within each source branch.'))
dump(HERE/'lexical_math_pairs.json',pairs)
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e05.bibliography}');b=native.index(r'\sgaStableTarget{sga6.e06.expose}',a)
native_block=re.search(r'(?:\\providecommand[^\n]*\n){20}',native[a:b]).group()
fr364=(HERE/'source_packets/364/current.tex').read_text()
reviewed_block=fr364[fr364.index('% Exposé VI projective-bundle macro additions'):].strip('\n')+'\n'
assert len(re.findall(r'\\(?:provide|renew)command',reviewed_block))==20
tf=HERE/'translations/364.tex';translated=tf.read_text()
if '@@CONTINUATION_BLOCKS@@' in translated:
    translated=translated.replace('@@CONTINUATION_BLOCKS@@','% SGA_NATIVE_CONTINUATION_364\n'+native_block+'\n% SGA_REVIEWED_FRENCH_CONTINUATION_364\n'+reviewed_block)
    tf.write_text(translated)
assert native_block in translated and reviewed_block in translated
assert translated.index(native_block)<translated.index(reviewed_block)
extra=[dict(record_type='continuation_macro_boundary',page=364,next_page=365,source_id='fixes/FIXLOG_6.jsonl#343;fixes/FIXLOG_6_CURRENT.jsonl#308',native_block=native_block,reviewed_block=reviewed_block,native_block_sha256=sha(native_block),reviewed_block_sha256=sha(reviewed_block),decision='Preserve all20 native definitions and all20 reviewed next-exposé definitions after the actual second bibliography item. The reviewed id renewal follows the native provide. No printed id glyph is asserted on364;subsequent usage decisions remain occurrence-specific.')]
dest=HERE/'attributed_source_audits';dest.mkdir(exist_ok=True)
for p,sid,name in [(362,'check/findings/findings_361_365.json#7;check/findings/findings_361_365.json#12','identification_362.json'),(363,'check/findings/findings_361_365.json#19;ASTRA-V-COEFFICIENT-363;ASTRA-V-UNIT-363','identification_363.json')]:
    rel='review/expose_v/'+name;raw=(ROOT/rel).read_bytes();(dest/name).write_bytes(raw)
    extra.append(dict(record_type='attributed_source_audit_packet',page=p,source_id=sid,source_packet=rel,contribution_copy='review/english/contributions/exposes_v_vi/attributed_source_audits/'+name,packet_sha256=hashlib.sha256(raw).hexdigest(),decision='Exact frozen source proof packet: formal u-derivation,unit inversion,the signed logarithmic coefficient map,and the lower-arrow route are retained separately from the translated author body.'))
for p,paragraph,reason in [
    (361,False,'The361 last word The continues with362 operations psi^k,matching Les / opérations at the exact source marker.'),
    (362,False,'The362 definition ends is and continues with363 a group homomorphism.'),
    (363,True,'The364 opening Now,if K is a lambda-ring is the independently recorded new indented paragraph.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=362]
batches.append(dict(expose='V',first=362,last=364,native_start=r'By \hyperlink{sga6.e05.para.7-3}{7.3}, the operations',native_end=r'\sgaStableTarget{sga6.e06.expose}',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French362–364 in both forms',
    reason='Complete reconstruction of7.4(ii),both directions of7.5,all four exact diagrams and coefficient calculations,the complete bibliography and both20-command continuation macro blocks. Seven native stable targets remain in source order.',variants=variants,
    notes=[
        dict(page=362,source_id='check/findings/findings_361_365.json#5;check/findings/findings_361_365.json#6;check/findings/findings_361_365.json#7;check/findings/findings_361_365.json#8',English_rendering='complete elementary-series Adams calculation',decision='Restore the hatted functor and the underlined coefficient-ring unit. The first full display branches both the printed dt/current du and the surplus closing parenthesis. In R=Ghat(Z[X]),a=1+Xt,the source unit is represented by1+t,the line-element series is1_R+a u,and D_u sends it to a. Its quotient expansion gives a^(circle k)=1+X^k t and exactly7.4.1. The source algebra operations and formal variable remain distinct by this explicit map.'),
        dict(page=362,source_id='check/findings/findings_361_365.json#9;check/findings/findings_361_365.json#10;check/findings/findings_361_365.json#12;check/findings/findings_361_365.json#13;check/findings/findings_361_365.json#14',English_rendering='full7.5 statement,unit proof and7.5.2 square',decision='Preserve all14 lexical rule groups with mathematical arguments plain;the isolated psi^t exponent is explicitly branched to psi^k. Restore the source semicolons,inline unit computation,and separate psi^k(1) display. The slash grouping is separately branched:the displayed geometric series multiplied by1+t is1,and its t-coefficient is−1 rather than the ungrouped expression’s+1. Restore every Phi label in7.5.2,the left-side circle,the above-arrow lower labels,and final comma,which inherited English had changed.'),
        dict(page=363,source_id='ASTRA-V-COEFFICIENT-363;check/findings/findings_361_365.json#16',English_rendering='full logarithmic coefficient definition and elementary multiplicativity calculation',decision='Restore Phi^k=the composite of Dlog and(-1)^(k−1) times coefficient extraction. The parenthetical coefficient series and missing Phi superscript have one complete-display branch with both source IDs. Dlog(1+Xt)=X/(1+Xt) has coefficient(-1)^(k−1)X^k;the displayed signed series has coefficientX^k. At k=2 the unsigned source value is−X². Only the lexical coefficient words are translated inside the unit.'),
        dict(page=363,source_id='check/findings/findings_361_365.json#19;check/findings/findings_361_365.json#20;ASTRA-V-UNIT-363;check/findings/findings_361_365.json#22;check/findings/findings_361_365.json#24',English_rendering='full7.5.3 diagram,consecutive calculations,and both final compositions',decision='Restore superscript t/u functors,all kk-prime indices,and the actual lower Phi^k arrow,which points right in diplomatic and left currently. Its map has domain Ghat^t(K),codomainK,and sends1+X^(k-prime)t toX^(kk-prime),agreeing with the left vertical route. Keep the plain1 in the u-series:the scalar unit map sends n to(1+t)^n in the represented t-series ring. The two calculation displays have no inserted and then;both following composition formulas are complete inline source formulas in separate paragraphs.'),
        dict(page=364,source_id='ASTRA-V-LOG-DERIVATIVE-364;check/findings/findings_361_365.json#27;check/findings/findings_361_365.json#28',English_rendering='complete two-part proof conclusion and unit integration',decision='Restore all quantifiers and the full7.5.4 square with above-arrow lower lambda label. Under the explicitly recorded Q-algebra convention,Dlog inverse sends sum g_j t^j to exp(sum g_j t^(j+1)/(j+1)),with integral constant0 and exponential constant1. Equality of every Phi coefficient therefore gives equality of the series;the source’s two diagram tests and final unit argument are retained verbatim in mathematical content.'),
        dict(page=364,source_id='check/findings/findings_361_365.json#29;check/findings/findings_361_365.json#30;check/findings/findings_361_365.json#31;ASTRA-V-INK-364',English_rendering='BIBLIOGRAPHY and both complete source entries',decision='Keep the all-capital heading and plain French/German titles with the exact supplied journal,volume,date,and page details;remove the inherited unprinted emphasis. The independently recorded small raised ink fragment after l est establishes no additional readable token and is retained as an attributed evidence note,without inventing an author-note call or cause.'),
        dict(page=364,source_id='fixes/FIXLOG_6.jsonl#343;fixes/FIXLOG_6_CURRENT.jsonl#308',English_rendering='both complete20-command next-exposé macro blocks',decision='The literal native provide block and reviewed block,including its scoped id renewal,remain after the second bibliography item and before the VI target. Exact texts and hashes are in the continuation record. The local capital Id on361 remains an independent literal command.'),
        dict(page=364,source_id='review/expose_v/page_status.jsonl#pages362-364',English_rendering='three complete source pages and seven native targets',decision='Every prose clause,formula,reference,underline group and placement was manually compared with both reviewed French forms. The three joins are explicit. This closes ExposéV through its bibliography and continuation block;there are no original author notes in these three pages and no newly claimed image or PDF review.')
    ],extra_records=extra,retained_proof_audits=['ASTRA-V-UNIT-363','ASTRA-V-LOG-DERIVATIVE-364']))
dump(HERE/'batches.json',batches);build_records()
