#!/usr/bin/env python3
"""Context-reviewed English diplomatic reconstructions and non-counterparts."""
import json
import re
from english_stage import WORK,ROOT,SRC
from english_variants import op_entry


NO_COUNTERPART={
 '7I:C575':'The phrase is present in both source layers; the differential on this page is the separately recorded reference 4.3/14.3.4, not this restored phrase.',
 '7I:C730':'French biridifié/rigidifié is a French spelling slip; the English technical term rigidified is unchanged.',
 '7I:C769':'The English expresses the Hom set directly and does not call its elements either isomorphisms or homomorphisms; the isomorphism classes of cocartesian functors are a different, correct phrase.',
 '7I:C802':'The English recasts the parenthesis as a separate sentence; no corresponding missing parenthesis exists.',
 '7I:C813':'The English construction from the category of biextensions expresses the functor domain in both readings; the French preposition correction does not require a different English rendering.',
 '7I:C836':'The released sentence has no enclosing parenthesis corresponding to this French missing delimiter.',
 '7I:C857':'Handled as a corrected-English repair with an attested printed I-prime, not by adding a second prime to the release.',
 '7I:C881':'The English recasts the French parenthesis as a colon and complete clause.',
 '7I:C909':'The English expression has a different, balanced grouping; the French missing outer parenthesis has no direct counterpart in that grouping.',
 '7I:C922':'The English colon construction has no enclosing French parenthesis to retain.',
 '7I:C936':'French où/ou does not change the released English equivalent-to-define construction.',
 '7I:C1025':'The printed mathematical symbols agree after ignoring the damaged TeX dollar placement; dollar delimiters are transcription syntax and are not printed glyphs.',
 '7II:C522':'The English dim expression is written without the outer parenthesis used in French; its inner cohomology parentheses remain intact.',
 '7II:C574':'The released English says just used instead of printing either numerical reference; no differing English reference exists.',
 '7II:C584':'The same formula is handled with C582 and the full-source formula collation.',
 '7II:C628':'French fibre/fibré does not change the English word fiber.',
 '7II:C642':'The English refers to the chosen extension without repeating its French symbol; no symbol exists at this locus to vary.',
 '7II:C672':'The English proof-reduction sentence expresses the same implication for both French formulations.',
 '7II:C745':'The English uses a simple see reference without the French nested parenthesis; no corresponding extra opening parenthesis exists.',
 '7II:C749':'The English tensor product has no structure-ring subscript at this locus; adding a square elsewhere would corrupt the formula.',
 '7II:C750':'The two references are stated jointly before the two calculations in English; both correct references are already present.',
 '7II:C751':'The English explanation is a separate sentence without the French enclosing parenthesis.',
 '7II:C822':'The English uses the equivalent pullback expression without a tensor product over k or K at this locus.',
 '7II:C884':'Both authoritative French layers put the reference outside underlining; this is a shared transcription repair, not a printed variant.',
 '7II:C885':'Both authoritative source layers separate math from underline; the released English shares that presentation.',
 '7II:C887':'Both authoritative source layers separate references and punctuation from underline; no diplomatic/current distinction occurs here.',
}


def build_manual(components,candidates):
    cmap={(c['volume'],c['component']):c for c in components}
    candidates={(x['volume']+':'+x['id']):x for x in candidates}
    overrides={};decisions=[]
    def add(key,replacements=None,*,target=None,printed=None,component=None,reason='Context checked against the actual diplomatic and current source readings.'):
        x=candidates[key];p=x['port'];f=x['fr_fix'];v=x['volume']
        component=component or p.get('tr_file')
        if target is None:target=p.get('tr_new') if p.get('decision')=='apply' else p.get('tr_old')
        if printed is None:
            printed=target
            for a,b in replacements or []:
                assert a in printed,(key,a)
                printed=printed.replace(a,b)
        t=cmap[(v,component)]['text'];assert t.count(target)==1,(key,t.count(target))
        a=t.index(target)
        overrides[key]=op_entry(v,component,a,a+len(target),target,printed,p.get('source','OPEN_ITEMS_DECIDED.tsv')+'#'+x['id']+'; '+str(f.get('id','')),f['page'],f['kind'],'context-reviewed reconstruction')
        decisions.append({'item':'EN-RECON-'+key,'page':v+':'+str(f['page']),'decision':'Use the explicitly reconstructed diplomatic reading.','reason':reason,'source':overrides[key]['source'],'corrected':target,'printed':printed})

    add('7I:C527',[("T_p(A'_K)","T_p(A'_k)")],reason='The diplomatic source has lower-case k, not the K-prime that occurred in an earlier corrected transcription.')
    add('7I:C731',[(r'j(xy)',r'j(f(xy))'),(r'j(x)j(y)',r'j(f(x)f(y))')])
    add('7I:C756',[(r'\underline\Psi_{L_\bullet}(A)',r'\underline\Psi_L(A)')])
    add('7I:C770',[(r'\underline\Psi_{L_\bullet}',r'\underline\Psi_L')])
    add('7I:C772',[(r"L'_\bullet]",r"L']")])
    add('7I:C783',[(r' and \SGARefLink{sga7.sga7i.eviii.n1-5}{1.5}, respectively', '')])
    add('7I:C844',[(r'V^\perp/',r'V/')],reason='The actual diplomatic source already reads 2 lambda; only the missing orthogonal-complement superscripts are variants.')
    target=r'$K_t$ is unipotent (SGA 3, XVII, 1.1), then $K_s$ is unipotent as well.'
    add('7I:C851',target=target,printed=target.replace('XVII, 1.1)','VII, 1.1'))
    NO_COUNTERPART['7I:C1035']='Covered together with the missing parenthesis by the unique C851 locus; no duplicate entry.'
    add('7I:C878',[(r"\'{e}tale",'connected')])
    add('7I:C880',[('$G$ plainly','$X$ plainly')])
    add('7I:C892',[(r'\mathcal A\times',r'A\times')])
    add('7I:C894',[(r'group by $\underline M$',r'group by $M$')])
    add('7I:C904',[(r'A^{\natural}',r'A')])
    add('7I:C924',[(r"of $A'_K$",r'of $A_K$')])
    add('7I:C927',[(r'u_\ell^{A_K}',r'\varphi^t')])
    add('7I:C979',[(r'\mathcal E(B)',r'(B)')])
    add('7II:C512',[('Koszul','Kozul')])
    # C519 concerns the complete filtration passage, not merely its opening.
    x=candidates['7II:C519'];c=cmap[('7II',x['port']['tr_file'])]['text']
    start=c.index(x['port']['tr_old']);end=c.index(r'\end{equation}',c.index(r'\tag{1.3.6}',start))+len(r'\end{equation}')
    target=c[start:end]
    add('7II:C519',target=target,printed=target.replace(r'\underline O_H',r'\underline O_Y'))
    add('7II:C534',[(r'\operatorname{char}',r'\operatorname{card}')])
    add('7II:C570',target=r'\arrow[rr, "\sigma-1"] \arrow[d]',printed=r'\arrow[rr, dash, "\sigma-1"] \arrow[d]',reason='Restore only the printed rule; the inherited editorial explanation is extracted separately.')
    add('7II:C581',target=r'\subsubsection*{2.4.7.}',printed=r'\subsubsection*{2.4.6.}',reason='Restore the actual printed number, omitting the inherited explanatory parenthesis from the body.')
    x=candidates['7II:C582'];target=x['port']['tr_new'].split('\nThe source prints')[0]
    printed=target.replace(r'\tag{2.4.7.1}',r'\tag{2.4.6.1}').replace(r'\mathbb H^n(X^*_{s(x)},K) \arrow[r] \arrow[d]',r'\mathbb H^n(X_{s(x)},K) \arrow[r] \arrow[d]')
    add('7II:C582',target=target,printed=printed,reason='Restore the printed repeated tag and missing star, without reintroducing translator commentary.')
    add('7II:C617',[(r'\overline B^*',r'{}_1\overline B^*')])
    add('7II:C621',[(r'\partial T_0',r'\partial T')])
    add('7II:C646',[(r'\xi\prod',r'\xi:\prod')])
    x=candidates['7II:C653'];c=cmap[('7II',x['port']['tr_file'])]['text'];start=c.index(x['port']['tr_old']);end=c.index(r'\item',start)+len(r'\item');target=c[start:end]
    add('7II:C653',target=target,printed=target[:-len(r'\item')]+r'\item[(1)]',reason='The print labels the first enumerated clause (1); no letter in the section heading is altered.')
    add('7II:C685',target=candidates['7II:C685']['port']['tr_old'],replacements=[('presented in $n$ variables','of dimension $n$')],reason='The released variables formulation encodes dimension n minus one. The printed dimension n is a materially different claim, so the diplomatic translation states it explicitly.')
    add('7II:C692',[(r'$\mathcal Y\to',r'$Y\to')])
    add('7II:C819',[(r'X_1^{W_1}',r'X_1^{W}')],reason='The diplomatic source already uses upper-case W; its missing subscript 1 is the actual printed variant.')
    add('7II:C889',[(r'\pi_U',r'\pi')],reason='The diplomatic arrow label is pi without U. The label-side apostrophe repaired in the scan pass is not the printed/corrected distinction.')
    add('7II:C900',[(r'/p\right)',r'\right.')],reason='The source lacks the denominator p and uses a null closing delimiter. The other field-letter variant is collated independently from the complete formula.')
    target=candidates['7II:C901']['port']['tr_new'];printed=candidates['7II:C901']['port']['tr_old'].replace('1-q^it','1-q^if')
    add('7II:C901',target=target,printed=printed,reason='The actual printed product has f instead of t as well as the missing inverse; the printed zeta quotient is also reversed.')
    for key,reason in NO_COUNTERPART.items():
        if key in candidates:
            x=candidates[key];decisions.append({'item':'EN-NO-VARIANT-'+key,'page':x['volume']+':'+str(x['fr_fix']['page']),'decision':'No additional English variant for this item.','reason':reason,'source':x['port'].get('source','fixes/FIXLOG_'+x['volume']+'_CURRENT.jsonl')})
    return overrides,NO_COUNTERPART,decisions


if __name__=='__main__':
    cs=json.loads((WORK/'en_components.json').read_text());xs=json.loads((WORK/'en_candidates.json').read_text())
    ops,no,decs=build_manual(cs,xs)
    (WORK/'en_manual_operations.json').write_text(json.dumps(list(ops.values()),ensure_ascii=False,indent=1))
    (WORK/'en_manual_decisions.json').write_text(json.dumps(decs,ensure_ascii=False,indent=1))
    print('manual',len(ops),'no-counterpart',len(no))
