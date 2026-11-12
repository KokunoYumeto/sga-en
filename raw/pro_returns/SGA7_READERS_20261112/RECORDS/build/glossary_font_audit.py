#!/usr/bin/env python3
"""Audit source font and mathematical-underline differences against English.

Font wrappers are significant here; the alignment normalizer is only a locator.
"""
import collections
import argparse
import difflib
import json
import re
from pathlib import Path

from english_variants import math_entries, balanced

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
OUT = ROOT / 'output' / 'records'
FONT = re.compile(r'\\(?:mathbb|mathcal|mathfrak|mathscr|mathbf|mathsf|mathit)\b')
COMP = json.loads((WORK / 'en_components.json').read_text())
CURRENT_EDITION = {(a['volume'], a['expose']): a for a in json.loads((WORK / 'en_variant_data.json').read_text())}
FINAL_COMPONENTS = {(a['volume'], a['component']): a for a in json.loads((WORK / 'en_final_components.json').read_text())} if (WORK / 'en_final_components.json').exists() else {}
OPERATIONS = []
REVIEWS = []


def clean_comments(t):
    return re.sub(r'(?<!\\)%[^\n]*', lambda m: ' ' * len(m[0]), t)


def applications(t, pattern):
    """Retain the actual argument of each font command, not just its count."""
    out=[]
    for m in pattern.finditer(t):
        q=m.end()
        while q<len(t) and t[q].isspace():q+=1
        if q==len(t):
            out.append((m[0],''));continue
        if t[q]=='{':
            level=1;end=q+1
            while end<len(t) and level:
                if t[end]=='\\':end+=2;continue
                if t[end]=='{':level+=1
                elif t[end]=='}':level-=1
                end+=1
            arg=t[q+1:end-1]
        elif t[q]=='\\':
            symbol=re.match(r'\\[A-Za-z]+|\\.',t[q:])
            arg=symbol[0]
        else:arg=t[q]
        out.append((m[0],re.sub(r'[\s{}]+','',arg)))
    return out


def discover():
    fonts, underlines, normalized_equal = [], [], []
    for vol, folder in [('7I', 'sga7i'), ('7II', 'sga7ii')]:
        for path in sorted((ROOT / 'sources/fr' / folder / 'current').glob('expose_*_body.tex')):
            ex = path.stem.split('_')[1]
            if ex == 'VI':
                continue
            ct = path.read_text()
            dt = (path.parent.parent / 'diplomatic' / path.name).read_text()
            cm, dm = math_entries(clean_comments(ct)), math_entries(clean_comments(dt))
            for mode in ('font', 'underline'):
                key = (lambda a: a['norm']) if mode == 'font' else (
                    lambda a: tuple(t for t in a['norm'] if t != '\\underline'))
                for b in difflib.SequenceMatcher(None, [key(a) for a in dm], [key(a) for a in cm], autojunk=False).get_matching_blocks():
                    for j in range(b.size):
                        old, new = dm[b.a+j], cm[b.b+j]
                        if mode=='font' and re.sub(r'\s+','',old['body'])!=re.sub(r'\s+','',new['body']):
                            page=re.findall(r'folio\s+(\S+)',ct[:new['start']])[-1]
                            tags=lambda t:re.findall(r'\\tag\*?\{([^{}]*)\}',t)
                            if applications(old['body'],FONT)!=applications(new['body'],FONT):category='font'
                            elif tags(old['body'])!=tags(new['body']):category='equation label'
                            elif old['body']==r'A^\natural_{\hat{\underline{O}}}':category='equivalent single-token brace group'
                            elif old['body']==r'\underline{G}_{m\,S}':category='math spacing only'
                            else:category='subscript or accent scope'
                            normalized_equal.append(dict(volume=vol,expose=ex,page=page,category=category,
                                                         printed=old['body'],corrected=new['body']))
                        pattern = FONT if mode == 'font' else re.compile(r'\\underline\b')
                        differs = applications(old['body'],pattern) != applications(new['body'],pattern)
                        if not differs:
                            continue
                        page = re.findall(r'folio\s+(\S+)', ct[:new['start']])[-1]
                        (fonts if mode == 'font' else underlines).append({
                            'volume': vol, 'expose': ex, 'page': page,
                            'printed': old['body'], 'corrected': new['body'],
                            'printed_start': old['start'], 'corrected_start': new['start'],
                            'source': f'fr/{folder}/{{diplomatic,current}}/{path.name}'})
    return fonts, underlines, normalized_equal


def add(vol, ex, page, prefix, corrected, printed, fr_id, reason):
    components = [a for a in COMP if a['volume'] == vol and a['component'].split('/')[-1].startswith(prefix)]
    assert len(components) == 1, prefix
    c = components[0]
    assert c['text'].count(corrected) == 1, (prefix, corrected, c['text'].count(corrected))
    assert balanced(printed), (prefix, 'braces')
    entry = dict(id=f'ED-EN-FONT-G{len(OPERATIONS):03d}', volume=vol, expose=ex,
                 component=c['component'], start=c['text'].index(corrected),
                 corrected=corrected, printed=printed,
                 source=f'{fr_id}; fr/{"sga7i" if vol=="7I" else "sga7ii"}/{{diplomatic,current}}/expose_{ex}_body.tex; folio {page}',
                 page=str(page), reason=reason)
    entry['source'] = entry['id'] + '; ' + entry['source']
    edition = CURRENT_EDITION.get((vol, ex), {})
    entry['prior_exact_printed_present'] = printed in edition.get('diplomatic', '')
    if (vol, c['component']) in FINAL_COMPONENTS:
        final = FINAL_COMPONENTS[(vol, c['component'])]
        entry['component_projection_check'] = dict(
            corrected_target_count=final['corrected'].count(corrected),
            printed_target_count=final['diplomatic'].count(printed),
            printed_target_baseline_count=final['corrected'].count(printed),
            corrected_target_remaining_in_printed=final['diplomatic'].count(corrected))
        check=entry['component_projection_check']
        check['verified']=(check['corrected_target_count']==1 and
                           check['printed_target_count']==check['printed_target_baseline_count']+1 and
                           check['corrected_target_remaining_in_printed']==0)
    OPERATIONS.append(entry)


def reviewed(fr_ids, status, reason):
    for fr_id in fr_ids.split():
        REVIEWS.append(dict(fr_id=fr_id, status=status, reason=reason))


def add_tag(vol,ex,page,current,printed):
    choices=[]
    for c in COMP:
        if (c['volume'],c['expose'])!=(vol,ex):continue
        for m in re.finditer(r'\\tag\*?\{',c['text']):
            t=c['text'];q=m.end();d=1
            while d and q<len(t):
                if t[q]=='\\':q+=2;continue
                if t[q]=='{':d+=1
                elif t[q]=='}':d-=1
                q+=1
            body=t[m.end():q-1]
            ref=re.fullmatch(r'\\SGARefTarget\{([^{}]+)\}\{([^{}]*)\}',body)
            value=ref[2] if ref else body
            if value==current:choices.append((c,t[m.start():q],ref))
    assert len(choices)==1,(vol,ex,current,[(c['component'],t) for c,t,r in choices])
    c,token,ref=choices[0]
    if printed is None:
        replacement=r'\notag'+(r'\SGARefAliasTarget{'+ref[1]+'}' if ref else '')
    elif ref:replacement=r'\tag{\SGARefTarget{'+ref[1]+'}{'+printed+'}}'
    else:replacement=r'\tag{'+printed+'}'
    add(vol,ex,page,c['component'].split('/')[-1],token,replacement,
        'complete normalized-equal formula audit',
        'The formula normalizer discards equation tags. Restore the supplied printed label'+
        ('; the unnumbered printed display uses notag, retaining any native cross-reference anchor.' if printed is None else
         ', retaining any native cross-reference anchor unchanged.'))
    OPERATIONS[-1]['id']=OPERATIONS[-1]['id'].replace('FONT','NORM')
    OPERATIONS[-1]['source']=OPERATIONS[-1]['source'].replace('ED-EN-FONT','ED-EN-NORM')


def run(write_operations=True):
    fonts, underlines, normalized_equal = discover()
    # Twelve font-only mathematical differences that compare equal after the
    # normalizer drops font wrappers. Each native target is independently located.
    add('7I','IX',403,'150_',r'A_n=\mathcal A\times_{\widehat S}S_n',r'A_n=A\times_{\widehat S}S_n',
        'F7I-IX-078.2','The printed ordinary A is distinct from the corrected calligraphic formal scheme. Port C892 already records the corrected target; font-erasing token transfer cannot reconstruct its printed font.')
    add('7I','IX',445,'165_',r'\mathbb Z_S\subset\mathbb Q_S',r'\mathbb Z_S\subset Q_S',
        'F7I-IX-125.1','Restore the plain printed Q only in the terminal containing sheaf.')
    add('7I','IX',452,'167_',r'(U\otimes\mathbb Q_\ell)^I\simeq U^I',r'(U\otimes Q_\ell)^I\simeq U^I',
        'F7I-IX-131.1','Only the lower-row coefficient in diagram11.3.7 has plain Q in the printed source.')
    add('7I','IX',515,'184_',r'where $G_K$ itself is of one of these types.',r'where $\mathbb G_K$ itself is of one of these types.',
        'F7I-IX-197.2','The printed blackboard G is erroneous at this one occurrence of the general group G_K, distinct from the surrounding multiplicative and additive groups.')
    add('7II','XVIII',320,'131_',r'H^{n-1}(X\cap H_s,\mathbb Q_\ell)',r'H^{n-1}(X\cap H_s,Q_\ell)',
        'F7II-XVIII-103.4','The coefficient Q lacks its blackboard typeface in the printed local-system description.')
    add('7II','XVIII',327,'133_',r'Thus a $\mathbb Q_\ell$-subspace $M$ of $E$',r'Thus a $Q_\ell$-subspace $M$ of $E$',
        'F7II-XVIII-110.10','Restore the plain Q in the final invariant-subspace argument; equivalent module/subspace phrasing is retained from the English release.')
    add('7II','XVII',247,'106_',r'A=\mathbb Z[[X_1,\ldots,X_a]]',r'A=Z[[X_1,\ldots,X_a]]',
        'F7II-XVII-042.5','The coefficient ring is printed with ordinary Z.')
    add('7II','XVI',202,'085_',r'$\mathbb E_S^{n+1}$ defined by an equation',r'$E_S^{n+1}$ defined by an equation',
        'F7II-XVI-004.2','Only Case1 has ordinary E in print. The accompanying X_s/X correction is independent and must be preserved.')
    add('7II','XXII',416,'169_',r'converges in $\mathbb Q_p(\xi_p)$',r'converges in $Q_p(\xi_p)$',
        'F7II-XXII-034.1','The parenthetical convergence remark has plain Q; the preceding field in4.1.4 is blackboard Q in both witnesses.')
    add('7II','XXII',416,'169_',r'\in\mathbb Q_p[[X]],',r'\in Q_p[[X]],',
        'F7II-XXII-035.1','Restore plain Q in4.1.6 only; its target is located uniquely by the series-ring expression.')
    add('7II','XXII',418,'171_',r'\tau\in\operatorname{Gal}(K/\mathbb Q_p(\xi_p))',r'\tau\in\operatorname{Gal}(K/Q_p(\xi_p))',
        'F7II-XXII-039.1','Restore plain Q in the tagged definition4.4.1, not in the adjacent verbal field definition.')
    add('7II','XX',362,'146_',r'$\mathbb Q_\ell$-homologous to zero',r'$Q_\ell$-homologous to zero',
        'F7II-XX-040.6','The closing quadric example prints ordinary Q. The English lexical rendering is retained; the font distinction alone is reconstructed.')
    # Mixed semantic/font differences: a changed symbol can be reconstructed
    # correctly while its font wrapper is still lost by ordinary token transfer.
    add('7I','VIII',264,'108_',r'and to $M=\mathbb Z/n\mathbb Z$',r'and to $\mathbb Z=\mathbb Z/n\mathbb Z$',
        'F7I-VIII-033.2','The printed left side is blackboard Z, not ordinary Z; preserve the complete mistaken symbol when reversing M.')
    add('7I','VIII',302,'122_',r'\mathrm{Hom}\bigl(\Phi\otimes\Psi,(\mathbb Q/\mathbb Z)_k\bigr)',
        r'\mathrm{Hom}\bigl(\Phi\otimes\Psi,Q/\mathbb Z\bigr)',
        'F7I-VIII-067.2','The print omits the grouping and constant-sheaf subscript and also prints ordinary Q. This complete target supersedes a partial delimiter/subscript reversal that retained the corrected font.')
    add('7I','IX',493,'180_',r'let $\underline R$ be the sheaf of sections of $R$',r'let $\mathbb R$ be the sheaf of sections of $R$',
        'F7I-IX-176.1','The printed symbol is blackboard R, not merely an un-underlined R. Both the formula and port token-transfer candidates dropped the underline but lost this printed font.')
    add('7II','X',2,'001_',r'$\underline{O}_{Z_o}$',r'$O_{\mathbb Z_o}$',
        'F7II-X-002.2 F7II-X-002.4','Restore both the missing O underline and the erroneous blackboard Z subscript in the printed statement.')
    add('7II','XI',48,'013_',r'\longrightarrow H^q\bigl(\mathbb P(\underline E),\mathbb Z/\ell^m\bigr)',
        r'\longrightarrow H^q(Y,\mathbb Z/\ell^m)',
        'F7II-XI-013.1','Replacing the entire target projective space by printed Y must remove both the blackboard P and the underlined E argument, leaving no unattached font wrapper. The integrated literal target uses ordinary parentheses; no new delimiter-sizing convention is imposed.')
    add('7II','XIV',160,'062_','H^*(U^*,V)\n \\xrightarrow[(4.18.1)]',
        'H^*(U^*,\\mathbb C)\n \\xrightarrow[(4.18.1)]',
        'F7II-XIV-053.1','The erroneous printed coefficient is blackboard C. Ordinary C would not reproduce the recorded printed symbol.')
    add('7II','XVII',215,'091_',r'A pencil $D=\{H_t\}_{t\in D}$',r'A pencil $D=\{H_t\}_{t\in\mathbb P}$',
        'F7II-XVII-004.1','The definition prints the blackboard projective-space symbol P as index set, not an ordinary variable P. The earlier notation paragraph is a separate occurrence.')
    add('7II','XVIII',295,'121_',r'\longrightarrow H^p(\mathbb P^1,R^n\rho_*\mathbb Q_\ell)',
        r'\longrightarrow H^p(\mathbb P^1,\mathbb R^1\rho_*\mathbb Q_\ell)',
        'F7II-XVIII-060.7','The printed target has blackboard R and degree1; reversing only the degree would leave its font correction unrecorded.')
    add('7II','XX',361,'146_','\\geq\n\\dim_{\\mathbb Q}', '\\geq\n\\dim_Q',
        'F7II-XX-038.4','Only the right-hand dimension operator has ordinary Q as its printed scalar field. Other degree/twist corrections within5.1.1 remain separately applicable.')
    add('7II','XXII',435,'182_',r'\longrightarrow\mathcal O_V\longrightarrow0,',
        r'\longrightarrow\mathcal O_V\longrightarrow\mathcal O,',
        'F7II-XXII-069.1','The printed terminal object of6.2.2 is calligraphic O, not ordinary O and not zero.')
    add('7II','XXII',435,'182_','\\mathcal O_V \\arrow[r] \\arrow[d,"\\mathfrak F_q"\'] &\n0\\\\',
        '\\mathcal O_V \\arrow[r] \\arrow[d,"\\mathfrak F_q"\'] &\n\\mathcal O\\\\',
        'F7II-XXII-070.1','The printed upper-right endpoint in6.2.3 is calligraphic O.')
    add('7II','XXII',435,'182_','\\mathcal O_V \\arrow[r] &\n0 .',
        '\\mathcal O_V \\arrow[r] &\n\\mathcal O .',
        'F7II-XXII-070.2','The printed lower-right endpoint in6.2.3 is calligraphic O.')
    add('7II','XXII',437,'183_',r'f(X)^{q-1}\cdot \mathfrak F_q',r'f(X)^{q-1}\cdot f_q',
        'F7II-XXII-076.2','The printed operator is lowercase ordinary f_q. Retaining mathfrak while changing its letter would produce an unattested fraktur f.')
    # The source underline is translated systematically by calligraphic Y.
    add('7II','XVII',218,'092_',r'$\mathcal Y\to\check{\mathbb P}^{r}$ makes',r'$Y\to\check{\mathbb P}^{r}$ makes',
        'F7II-XVII-008.1','The release renders the underlined incidence scheme as calligraphic Y. At the one printed omission of its underline, diplomatic English must likewise use plain Y; the surrounding occurrences retain calligraphic Y.')
    # Complete residual audit of raw-different but normalized-equal formulas.
    # No phi/varphi, epsilon/varepsilon, arrow, or inequality alias difference
    # occurs in the source pairs. Tags and binding scopes do occur.
    for args in [('7I','IX',452,'11.3.4','11,3.4'),
                 ('7I','IX',471,'12.3.3','12.2.3'),
                 ('7I','IX',471,'12.3.4','12.2.4'),
                 ('7I','IX',472,'12.3.8',None),
                 ('7II','XII',76,'3.3.1','3.2.1'),
                 ('7II','XVIII',309,'5.8.7.3',None),
                 ('7II','XVII',244,"5.2.6$'$",'5.2.6'),
                 ('7II','XV',181,'2.1.7.1','2.1 7.1'),
                 ('7II','XXII',422,'4.5.14','5.4.14'),
                 ('7II','XXII',423,'4.5.23','4.5.2.3'),
                 ('7II','XXII',425,'4.5.33','4.5.23'),
                 ('7II','XXII',428,'5.0.4','5.0.7')]:
        add_tag(*args)
    add('7II','XIX',331,'135_','$H^{2n}(H_s,\\mathbb Q_\\ell)$, and that this image equals',
        '$H^{2n}(H_{s,}\\mathbb Q_\\ell)$, and that this image equals',
        'normalized-equal subscript-scope audit',
        'The designated diplomatic source places the comma inside the subscript s, whereas current places it between the cohomology arguments. Reconstruct that supplied source distinction without claiming an independent physical-scan judgment.')
    c=next(c for c in COMP if c['volume']=='7II' and c['component'].split('/')[-1].startswith('115_'))
    old='''\\begin{aligned}
c_1(\\underline N_{\\widetilde\\Delta/\\widetilde X})^2
&=g^*\\!\\left(c_1(\\xi_\\Delta)^2\\right)'''
    new='''\\begin{aligned}
c_1(\\underline N_{\\widetilde\\Delta/\\widetilde X})^2
&=\\left(g^*c_1(\\underline{\\mathcal O}_{\\Delta(1)})
 -(\\rho i)^*c_1(\\xi_{\\mathbb P^1})\\right)^2\\\\
&=g^*\\!\\left(c_1(\\xi_\\Delta)^2\\right)'''
    add('7II','XVIII',277,'115_',old,new,'normalized-equal subscript-scope audit',
        'The release omits the intermediate expansion containing the printed O_{Delta(1)} error. Restore that intermediate row only in diplomatic English; leave the following xi_Delta expansion as printed, rather than transplanting the error into a different term.')
    add('7II','XVIII',294,'121_',r'first Chern class of $\underline{\mathcal O}_X(1)$',
        r'first Chern class of $\underline{\mathcal O}_{X(1)}$',
        'normalized-equal subscript-scope audit',
        'The printed twist (1) is incorrectly enclosed in the X subscript. Braces are significant for this binding, although discarded by the alignment normalizer.')
    add('7II','XVIII',326,'133_',r'$\bar E=E\otimes_{\mathbb Q_\ell}\bar{\mathbb Q}_\ell$',
        r'$\bar E=E\otimes_{\mathbb Q_\ell}\overline{\mathbb Q_\ell}$',
        'normalized-equal accent-scope audit',
        'The printed closure bar covers Q_ell together, whereas current places ell outside the bar. The wide overline displays the supplied printed scope explicitly.')
    add('7II','XVIII',326,'133_',r'$\bar{\mathbb Q}_\ell$-linear subspace',
        r'$\overline{\mathbb Q_\ell}$-linear subspace',
        'normalized-equal accent-scope audit',
        'The second occurrence in the coefficient-field description has the same printed bar scope over Q_ell.')
    for op in OPERATIONS[38:]:
        op['id']=op['id'].replace('FONT','NORM')
        op['source']=op['source'].replace('ED-EN-FONT','ED-EN-NORM')
    reviewed('F7II-XII-005.6','covered','G101 reconstructs the whole affine-space section statement, including blackboard E; this is not an isolated font replacement.')
    reviewed('F7II-XVII-034.1','covered','G141 explicitly restores the final O_{mathbb P} in the Euler sequence.')
    reviewed('F7I-IX-179.2','covered','G075 removes the whole mathcal E in the printed empty (B) term, including its font macro.')
    reviewed('F7II-XX-020.3','covered','ED-7II-1018-EN reconstructs the full omitted equality and explicitly retains plain Q in its printed denominator.')
    reviewed('F7II-XVIII-108.4','covered','The inserted target cohomology term is removed as a whole in E196; its blackboard coefficient is part of that added term, not a separate typeface change.')
    reviewed('F7II-XVI-008.1','contextual check','The source replaces base T by P^1_k; the full symbol replacement removes the projective-space typography. It is not a font-only variant.')
    reviewed('F7II-XXI-023.3 F7II-XXI-023.4 F7II-XXI-025.3','contextual check','These are missing Galois-group numerators, restored or omitted as entire overlined finite-field symbols. They do not change the font of a retained symbol.')
    reviewed('F7II-XXI-026.1 F7II-XXI-026.2','no distinct English reading','The projective ambient space is moved within the same French sentence. Its symbol and assertion are unchanged.')
    for op in OPERATIONS:
        for fr_id in re.findall(r'F7I{1,2}-[A-Z]+-\d+\.\d+', op['source']):
            REVIEWS.append({'fr_id':fr_id, 'status':'exact English reconstruction', 'operation':op['id'],
                            'reason':op['reason']})
    fr_register=json.loads((OUT/'FR_APPARATUS.json').read_text())
    fr_font_entries=[a for a in fr_register if a['expose']!='VI' and
                     applications(a['before'],FONT)!=applications(a['after'],FONT)]
    reviewed_ids={a['fr_id'] for a in REVIEWS}
    unreviewed=[a['id'] for a in fr_font_entries if a['id'] not in reviewed_ids]
    assert not unreviewed,('Unreviewed mixed font entries',unreviewed)
    underline_coverage=[]
    bases={0:'Existing formula and manual dual-group reconstruction on folio404.',
           1:'Existing port and formula operations remove the underline from the second twisted-constant module.',
           2:'Existing port and formula operations cover the representability statement overS.',
           3:'Existing port and formula operations cover the formal-smoothness statement overS.',
           4:'Existing port and formula operations cover the groupE overS.',
           5:'Existing port and formula operations cover u_ell.',
           6:'Existing complete-formula operation removes the two erroneous underlines on the right side.',
           7:'Existing port and formula operations cover the special-fibre symbolX_o^lambda.',
           8:'Existing port and formula operations cover the second free moduleE-prime.',
           9:'Existing port and formula operations retain the completion hat and remove its inner underline.',
           10:'ED-EN-FONT-G014 restores the printed blackboardR, repairing the plainR left by the earlier transfer.',
           11:'Existing port and formula operations cover R_{underline O}.',
           12:'Existing port and formula operations cover the second toric-part symbol.',
           13:'Existing formula operation covers the second module in the pair.',
           14:'ED-EN-FONT-G025 confirms the already reconstructed calligraphicY-to-plainY correspondence.',
           15:'ED-EN-FORMULA-G233.',16:'ED-EN-FORMULA-G235.',17:'ED-EN-FORMULA-E236.',
           18:'ED-EN-FONT-G015 restores both plainO and the blackboardZ subscript.'}
    assert len(underlines)==len(bases),'New mathematical-underline candidate requires context review.'
    for i,a in enumerate(underlines):
        underline_coverage.append({**a,'review_basis':bases[i]})
    if write_operations:
        (WORK / 'en_font_resolutions_glossary.json').write_text(json.dumps(OPERATIONS, ensure_ascii=False, indent=2)+'\n')
    (WORK / 'glossary_font_math_candidates.json').write_text(json.dumps(fonts, ensure_ascii=False, indent=2)+'\n')
    (WORK / 'glossary_underline_math_candidates.json').write_text(json.dumps(underlines, ensure_ascii=False, indent=2)+'\n')
    audit={'font_only_candidates':fonts, 'mathematical_underline_candidates':underlines,
           'mathematical_underline_coverage':underline_coverage,
           'complete_normalized_equal_raw_different_pairs':normalized_equal,
           'normalized_equal_categories':dict(collections.Counter(a['category'] for a in normalized_equal)),
           'font_apparatus_entries_reviewed':len(fr_font_entries),
           'unreviewed_font_apparatus_entries':unreviewed,
           'reviewed_mixed_font_changes':REVIEWS, 'operations':OPERATIONS,
           'exact_component_projection_checks_passed':sum(o.get('component_projection_check',{}).get('verified',False) for o in OPERATIONS),
           'scope':'All paired source math expressions equal under the English formula normalizer, plus all French apparatus differences changing the application or argument of mathbb/mathcal/mathfrak/mathscr/mathbf/mathsf/mathit outside original-English VI. Percent comments are excluded. Mathematical underline candidates use a second pass ignoring only underline for locating the counterpart.',
           'limits':'Ordinary upright-versus-italic math typography (mathrm/operatorname), text emphasis and prose-underlining spans are not automatically recased to French typography. Font styling consistently chosen by the released translation is retained. Source Expose VI is shared directly, so its font differences are already carried by source identity.'}
    (OUT / 'EN_FONT_UNDERLINE_AUDIT.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
    def cell(t):return str(t).replace('|','\\|').replace('\n',' ')
    def table(headers,rows):
        return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+
                         ['| '+' | '.join(cell(c) for c in row)+' |' for row in rows])
    categories=collections.Counter(a['category'] for a in normalized_equal)
    note=['# English font, underline, and normalization audit',
          '## Scope and method',
          'This audit checks distinctions that token normalization can hide. It removes percent-comments '
          'before locating mathematical expressions, aligns the complete French diplomatic and corrected '
          'formula sequences, and then compares their original TeX with whitespace alone ignored. '
          'Font application is checked with its argument, so equal counts of font commands cannot hide '
          'a change in their scope. A separate pass locates mathematical underline differences while '
          'ignoring only the underline command for alignment. Original-English Exposé VI is excluded '
          'from transfer because both editions already take its complete variants directly from the same '
          'paired French-package witnesses.',
          'The English formula normalizer drops blackboard, calligraphic, fraktur, and several other font '
          'wrappers, braces, equation tags, and some spacing. It **retains mathematical underline commands**. '
          'Consequently the underline check also tests the correspondence between underlined French '
          'notation and a calligraphic symbol chosen consistently in the released translation.',
          '## Complete audit of normalized-equal formula pairs',
          f'Exactly **{len(normalized_equal)}** source formula pairs compare equal under the normalizer '
          'but differ after whitespace removal. Their complete source readings are retained in '
          '`EN_FONT_UNDERLINE_AUDIT.json`.',
          table(['Difference class','Pairs'],sorted(categories.items())),
          'The two cases without a change of mathematical content are a redundant brace group around the single superscript token '
          '`\\natural`, and a thin space inside the multiplicative-group subscript. The latter does change printed spacing and remains a French typographic apparatus entry. No phi/varphi, '
          'epsilon/varepsilon, arrow, or inequality-alias difference occurs among these paired sources. '
          'Every equation-label change and every change in subscript or accent scope has an explicit '
          'English reconstruction. Unnumbered printed displays use `\\notag`; an existing English '
          'cross-reference anchor is retained without displaying an invented equation number.',
          'The five scope differences are the comma inside `H_{s,}` on XIX331; the twist absorbed into '
          '`O_{Delta(1)}` on XVIII277 and `O_{X(1)}` on XVIII294; and two occurrences of the closure bar '
          'over `Q_ell` together on XVIII326. These follow the designated source layers; they are not '
          'claims of a new inspection of the physical print.',
          '## Mixed font and symbol changes',
          f'All **{len(fr_font_entries)}** French apparatus entries outside Exposé VI that change a '
          'blackboard, calligraphic, fraktur, bold, sans-serif, script, or italic math-font application '
          'were reviewed. There are **0 unreviewed entries** in that mechanical scope. This includes '
          'changes where a symbol or mathematical expression changes at the same time as its font. '
          'Existing complete reconstructions are identified separately; moved ambient-space phrases '
          'and wholly inserted Galois numerators are not misclassified as isolated font errors.',
          '## Exact English operations',
          f'The audit supplies **{len(OPERATIONS)}** native English operations. Each corrected string '
          'and its offset is asserted against the unchanged native release component. The printed '
          'branch alone changes. The final column records whether the exact proposed printed passage '
          'is already present in the latest reconstructed diplomatic text read by this run; it must '
          'be refreshed after integration.',
          f"The stricter component-level count check passes for **{audit['exact_component_projection_checks_passed']} of {len(OPERATIONS)}** operations: "
          'each corrected target is unique in its assigned component, its diplomatic target adds exactly one '
          'occurrence relative to the corrected baseline, and the corrected target disappears from that '
          'diplomatic component. Existing duplicate equation labels are therefore accounted for explicitly.',
          table(['Operation','Exposé / folio','Corrected English span','Printed English span','Exact printed span present'],
                [[o['id'],o['volume']+' '+o['expose']+' / '+o['page'],
                  '`'+o['corrected'].replace('`','')+'`','`'+o['printed'].replace('`','')+'`',
                  'yes' if o['prior_exact_printed_present'] else 'awaiting integration or overlapping reconstruction'] for o in OPERATIONS]),
          '## Mathematical underline check',
          f'The independent underline pass finds **{len(underlines)}** pairs. The following records '
          'identify their exact contextual treatment. Font-family repairs are included above when '
          'merely removing an underline would lose the printed glyph.',
          table(['Exposé / folio','French printed','French corrected','English treatment'],
                [[a['volume']+' '+a['expose']+' / '+a['page'],'`'+a['printed']+'`',
                  '`'+a['corrected']+'`',a['review_basis']] for a in underline_coverage]),
          '## Limits and reproduction',
          audit['limits'],
          'Run `python build/glossary_font_audit.py --reports-only` after the English reconstruction to refresh the '
          'presence checks without rewriting the stable reconstruction-input ledger. The complete machine record includes all raw source pairs, the mixed-change '
          'review, exact native strings and offsets, and each reconstruction reason. Ordinary authorial '
          'prose emphasis and font choices consistently adopted by the translation are outside a '
          'mechanical reversal to French typography. No unverified general rule is applied to them.']
    (OUT/'EN_FONT_UNDERLINE_AUDIT.md').write_text('\n\n'.join(note)+'\n')
    print(json.dumps({'pure_font_candidates':len(fonts),'math_underline_candidates':len(underlines),
                      'exact_reviewed_operations':len(OPERATIONS),
                      'already_exact_in_prior_diplomatic':sum(o['prior_exact_printed_present'] for o in OPERATIONS)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--reports-only',action='store_true',help='Refresh audit records without rewriting the reconstruction-input ledger.')
    run(write_operations=not parser.parse_args().reports_only)
