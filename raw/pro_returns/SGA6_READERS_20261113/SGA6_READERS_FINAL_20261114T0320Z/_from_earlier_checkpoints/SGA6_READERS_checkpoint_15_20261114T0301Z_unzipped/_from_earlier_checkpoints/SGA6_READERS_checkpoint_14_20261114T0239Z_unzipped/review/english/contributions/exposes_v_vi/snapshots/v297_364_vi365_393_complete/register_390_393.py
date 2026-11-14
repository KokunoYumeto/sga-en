#!/usr/bin/env python3
"""Close the assigned English VI range immediately before the sec.4 target."""
from pathlib import Path
import hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT,dump,build_records
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def units(p,layer):return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(p)/f'{layer}.tex').read_text())]
def variant(p,index,sid,mode,suffix='01'):
    c,d=units(p,'current')[index],units(p,'diplomatic')[index];assert c!=d
    if mode=='math':
        assert (c.startswith(r'\(') and d.startswith(r'\(')) or (c.startswith('$') and d.startswith('$'))
        c,d=(c[2:-2],d[2:-2]) if c.startswith(r'\(') else (c[1:-1],d[1:-1])
    return dict(id=f'EN-CONTRIB-VI-{p}-{suffix}',page=p,old=c,printed=d,source=sid,mode=mode)
variants=[
    variant(390,10,'ASTRA-VI-FLAG-D-390','math'),
    variant(390,12,'ASTRA-VI-FLAG-D-390','math','02'),
    dict(id='EN-CONTRIB-VI-390-03',page=390,old=r'\(\underline{E}_i\),',printed=r'\(\underline{E}_i\)',source='check/findings/findings_386_390.json#18',mode='text'),
    variant(391,3,'ASTRA-VI-PROJECTIVE-P-391','display'),
    variant(392,0,'ASTRA-VI-FLAG-OPERATORS-392','math'),
    dict(id='EN-CONTRIB-VI-392-02',page=392,old=r'\textbf{Theorem 3.3.}',printed=r'\textbf{Theorem 3.3}',source='check/findings/findings_391_395.json#9',mode='text'),
    dict(id='EN-CONTRIB-VI-392-03',page=392,old=r'\(\underline{A}\)-\uline{Modules locally free}',printed=r'\(A\)-\uline{Modules locally free}',source='ASTRA-VI-TOPOS-COEFFICIENT-RULE-392',mode='text')]
translated393=(HERE/'translations/393.tex').read_text();u393=units(393,'current')
translated393=re.sub(r'@@M(\d+)@@',lambda m:u393[int(m.group(1))],translated393)
for index,count in [(0,3),(1,4)]:
    c=translated393.split('\n\n')[index];assert c.count(r'\mathbf{Gl}')==count
    d=c.replace(r'\mathbf{Gl}',r'\underline{\underline{\operatorname{Gl}}}')
    variants.append(dict(id=f'EN-CONTRIB-VI-393-0{index+1}',page=393,old=c,printed=d,source='ASTRA-VI-GL-OPERATORS-393',mode='text',occurrence_count=count))
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
a=native.index(r'\sgaStableTarget{sga6.e06.sec.2.8}');b=native.index(r'\sgaStableTarget{sga6.e06.sec.3}',a)
native_block=re.search(r'(?:\\providecommand[^\n]*\n){9}',native[a:b]).group()
tf=HERE/'translations/390.tex';translated=tf.read_text()
if '@@CONTINUATION_BLOCK@@' in translated:
    translated=translated.replace('@@CONTINUATION_BLOCK@@\n','% SGA_NATIVE_CONTINUATION_389_390\n'+native_block)
    tf.write_text(translated)
assert native_block in translated and native_block+'complete the induction' in translated
assert '\n\n' not in translated[:translated.index('complete the induction')]
assert not any(re.search(r'\\(?:provide|renew)command', (HERE/'source_packets'/str(p)/f'{layer}.tex').read_text()) for p in [389,390] for layer in ['current','diplomatic'])
extra=[dict(record_type='continuation_macro_boundary',page=389,next_page=390,placement_page=390,native_block=native_block,native_block_sha256=sha(native_block),reviewed_block='',reviewed_block_sha256=sha(''),decision='Retain all nine literal native continuation commands immediately before the source390 words complete the induction. The reviewed French389 and390 packets contain no corresponding continuation definitions. The command text is unchanged; native surrounding empty lines are not imported into the continuous source on/achève sentence. The390 page marker remains before its first source word, and no blank paragraph is created by the command block.')]
for p,paragraph,reason in [
    (389,False,'The printed389 on continues with390 achève; English we continues with complete the induction. The native nine-command transport block contains no paragraph break.'),
    (390,False,'The390 final et continues with391 pour tout i; English and continues with for every i, without an inserted comma or paragraph.'),
    (391,True,'The391 constant-rank reduction ends its paragraph before392 introduces the flag product.'),
    (392,True,'The392 constant-rank reduction ends its paragraph before393 begins the one-Module torsor construction.')]:
    f=(HERE/'source_packets'/str(p)/'current.tex').read_text();g=(HERE/'source_packets'/str(p+1)/'current.tex').read_text();e=(HERE/'translations'/f'{p}.tex').read_text();n=(HERE/'translations'/f'{p+1}.tex').read_text()
    assert e.endswith('\n\n')==paragraph,(p,repr(e[-30:]));assert not n.startswith('\n')
    extra.append(dict(record_type='manually_compared_source_folio_join',after=p,before=p+1,paragraph_break=paragraph,source_tail=f[-400:],source_head=g[:400],English_tail=e[-250:],English_head=n[:650] if p==389 else n[:250],source_page_sha256s={str(p):sha(f),str(p+1):sha(g)},reason=reason))
extra.append(dict(record_type='assigned_contribution_boundary',page=393,next_page=394,next_native_target='sga6.e06.sec.4',next_contributor='review/english/contributions/expose_vi_394_415',decision='This contribution ends after the complete source393 final sentence referring to3.2 and1.14, with a paragraph break. Its exact native replacement ends immediately before the sec.4 stable target, which belongs to the separate394–415 contribution. No394 prose, formula or target is consumed. The415/416 native and reviewed continuation blocks remain assigned to that contributor.'))
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=390]
batches.append(dict(expose='VI',first=390,last=393,native_start=r'\providecommand{\Sym}{\operatorname{Sym}}',native_end=r'\sgaStableTarget{sga6.e06.sec.4}',
    source='review/expose_vi/HANDOFF.md; reviewed French390–393 in both forms',
    reason='Restore the exact induction continuation, the full three results of section3 and their complete proofs, including every torsor, action and representation-ring formula. Preserve the native nine-command continuation block without an invented paragraph. Four native stable targets remain in their original order. This closes the assigned range immediately before section4 on394.',variants=variants,
    notes=[
        dict(page=390,source_id='check/findings/findings_386_390.json#13;ASTRA-VI-FLAG-D-390;check/findings/findings_386_390.json#17;check/findings/findings_386_390.json#18;check/findings/findings_386_390.json#19;ASTRA-VI-WORD-RULES-390',English_rendering='exact induction conclusion and Proposition3.1',decision='Keep the source389/390 word boundary, both complete coefficient sums and their commas, without inserting the native extra multiplier formula into the prose. Restore every ruled word group, the inline product with three baseline stops and its actual n endpoints, and the parenthetical two definitions of K. The three flag D occurrences are branched through identity on each complete quotient flag and its pullbacks. The missing comma before X is separately branched. Keep the source final and and its continuous391 opening.'),
        dict(page=390,source_id='ASTRA-VI-FLAG-STOPPING-390;fr/codex/HOLD_VS_CORR.json#37;fixes/RECONCILE_CODEX_6.json:entries#224;fixes/RECONCILE_CODEX_6.json:entries#319',English_rendering='complete source flag construction with X1,...,Xn after n=1',decision='Retain the printed indexing in both bodies and remove the inherited English rank-stratification paragraph, which is absent from the source. The source audit gives the exact forgetful map Flag(k^3)→P^2 taking a complete quotient flag to its rank-one quotient; the remaining choices form P^1 of the two-dimensional kernel. Thus this first stage does not yet supply the printed complete flag in the n=1 example. The evidence fixes the source reading but supplies no unique added stopping-rank passage. This precise issue remains in the separate attributed author-argument record, with no replacement theorem.'),
        dict(page=391,source_id='ASTRA-VI-PROJECTIVE-P-391;check/findings/findings_391_395.json#2;check/findings/findings_391_395.json#3;ASTRA-VI-WORD-RULES-391;ASTRA-VI-GLYPHS-391',English_rendering='complete projective recursion and Theorem3.2 proof opening',decision='Restore the actual k-indexed display and its semicolon, preserving the preceding i-indexed prose. The projective-P convention is explicit: each quotient E_T→L maps to itself, and id_E induces id on its symmetric algebra and Proj charts. Restore the separate reduction paragraph, the theorem reference V2.4, the inline lambda_t map and the full hat over K(S)[[t]] with plus outside. Keep the exact class elements E,F plain and their sheaf antecedents ruled, related by E↦cl(E) and lambda^i(cl(E))=cl(wedge^i E). Restore both polynomial identities and all repeated K groups in the finite disjoint-cover argument.'),
        dict(page=391,source_id='fixes/FIXLOG_6_CURRENT.jsonl#420;check/findings/findings_391_395.json#4',English_rendering='Since S is a quasi-compact scheme',decision='The source substantival phrase un quasi-compact is retained by translating its article and making its already declared scheme referent explicit in English. The same S was introduced as a scheme in Theorem3.2; no new hypothesis or French correction is supplied. This phrase has the same rendering in both English forms.'),
        dict(page=392,source_id='ASTRA-VI-FLAG-OPERATORS-392;check/findings/findings_391_395.json#8;check/findings/findings_391_395.json#9;ASTRA-VI-TOPOS-COEFFICIENT-RULE-392;ASTRA-VI-WORD-RULES-392',English_rendering='complete splitting argument and Theorem3.3',decision='Restore the inline flag product, the two universal identities with their actual semicolon and final comma, and the printed S under the full hat. The two flag operators are branched under identity on their quotient-flag functors. Preserve the source theorem stop omission diplomatically; the one plain A coefficient is separately branched through restriction of scalars along id_A, which leaves the module and its action identical. Keep of bounded rank on T unruled and every other inspected statement word group in its source scope. Restore the full reduction through each K^bullet of the disjoint opens; these two K^bullet expressions are retained literally rather than changed to K.'),
        dict(page=392,source_id='fixes/FIXLOG_6_CURRENT.jsonl#421',English_rendering='sums of classes of invertible sheaves',decision='The French classe/classes agreement repair has the same English plural rendering in both forms. The exact source class map is [E]=sum_j[L_j/L_(j−1)] on the complete flag, with the already specified multiple quotient sheaves. No English agreement error or different number of class summands is introduced.'),
        dict(page=393,source_id='ASTRA-VI-GL-OPERATORS-393;check/findings/findings_391_395.json#17;ASTRA-VI-GLYPHS-393;check/findings/findings_391_395.json#16',English_rendering='full one- and two-Module torsor/representation argument',decision='Restore every omitted associated Module, the complete two-factor torsor formula, both standard/trivial actions, the induced lambda-homomorphism and the last polynomial-relation sentence. Preserve all thirteen singly ruled group-sheaf operators and their separately ruled A arguments. The seven group-scheme Gl occurrences have two exact paragraph branches, covering3 and4 named occurrences respectively: on each object U the evaluation is the same invertible matrices Gl_n(A(U))=GL_n(A(U)), with identical multiplication and restriction maps, and the contracted-product map sends [p,v] to p(v). Keep all standard representations, ranks and group products unchanged. Restore the separate final paragraph and the complete reference to[5] and alternative3.2/1.14 argument.'),
        dict(page=393,source_id='review/expose_vi/page_status.jsonl#pages390-393',English_rendering='four complete source pages and four native stable targets',decision='All prose, formula placement, local rules, punctuation and nine branch records were manually compared with both reviewed French forms. All four joins are explicit, and the contribution stops at the authorized native sec.4 boundary. These pages contain no original author note. Source images and author-claim verification remain attributed to the frozen French review; no new full-page image or English PDF inspection is claimed.')
    ],extra_records=extra,retained_proof_audits=['ASTRA-VI-FLAG-STOPPING-390']))
dump(HERE/'batches.json',batches);build_records()
