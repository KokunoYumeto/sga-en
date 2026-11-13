"""Source-anchored, content-preserving layout repairs for the full readers.

Apply to prepared body text after prepare_body(). This module does not edit any
shared source. Its caller receives the modified string and a replay log.
"""
import re

PARAGRAPHS = {
    'fr': [
        ('I', '21', r'Soient $U\to X$ un morphisme étale et', "d'où le résultat."),
        ('II', '105', r"En effet, $F h^{-1}$ n'a pas de point fixe sur $V$", r'applique \eqref{II:eq:5-12-1}.'),
        ('III', '127', r'On a', r'la suite exacte longue'),
        ('IV', '137', r"Pour $A$ un corps, et $X_i$ une famille finie d'espaces", r'$\h^*\left(\prod X_i,A\right) = \bigotimes \h^*(X_i,A)$.'),
        ('V', '158', r'Soit $X$ une courbe projective et lisse sur $k$ algébriquement clos.', "identifie chaque facteur au dual de l'autre."),
        ('V', '161', r'fait de $\pic_D^0(\bar X)$ un', r'réciproque par $f_0$.'),
        ('VI', '198', r'Si $M=A^I$, $I$ un ensemble fini', r"projectif d'équation $\sum x_i=0$ de $P$."),
        ('VI', '210', r'Si $\varepsilon$ est une unité totalement positive', r'$E_\fm\subset F^\ast$ des unités totalement positives $\equiv 1\pmod\fm$.'),
        ('VI', '222', r'La fibre de $\eR^i \pi_! \sF(\psi\sigma)$ en $a$ est', 'nous fournit donc le'),
    ],
    'en': [
        ('IV', '142', r'Since $\eR g^! \sF=g^*\sF(N)[2N]$, the transitivity formula', r'\cite[XVIII 3.17]{sga4}}.'),
        ('IV', '152', r'Let $f$ be an endomorphism of $X$ proper and smooth', 'each counted with its multiplicity.'),
        ('V', '158', r'We reduce to checking that, for $f$ finite,', 'follows from \\ref{V:1-3}, and the assertion follows.'),
        ('VI', '180', r'Poincaré duality pairs $\h_c^i(X,\sF)$', 'satisfy'),
        ('VI', '197', r'If $\chi$ is nontrivial, \ref{VI:4-2}(iii)', '{S45-SOL-0805}$.'),
    ],
}

def page_range(body,page):
    # Markers may have been relocated to just after headings, but the actual
    # paragraphs below remain wholly on the designated printed source page.
    pattern=r'\\(?:PrintPage|MathPage)\{'+re.escape(page)+r'\}'
    hits=list(re.finditer(pattern,body))
    assert len(hits)==1,('printed page marker count',page,len(hits))
    a=hits[0].end()
    next_marker=re.search(r'\\(?:PrintPage|MathPage)\{[^}]+\}',body[a:])
    b=a+next_marker.start() if next_marker else len(body)
    return a,b

def apply_layout_repairs(body,lang):
    logs=[]
    # Split two nonnumbered chains at equality signs. Every mathematical token
    # remains in its original order; only alignment and display boundaries vary.
    patterns=[
        ('99',r'\\\[\s*(\\tr\\left\(F\^\*,\s*\\h_c\^\*\(X,\\sG\)\\right\).*?)\s*\\\]'),
        ('103',r'\\\[\s*(\|H\|\\cdot\s*\\tr_\\Lambda\(F,P_H\).*?)\s*\\\]'),
    ]
    for page,pattern in patterns:
        found=list(re.finditer(pattern,body,re.S));assert len(found)==1,(lang,page,'display match',len(found))
        m=found[0];formula=m[1]
        terms=re.split(r'\s*=\s*',formula)
        assert len(terms)==5,(lang,page,'equality count',len(terms))
        # Two compact aligned lines retain the five-term chain in reading order.
        new='\\begin{align*}\n  '+terms[0]+' &= '+terms[1]+' = '+terms[2]+' \\\\\n  &= '+terms[3]+' = '+terms[4]+'\n\\end{align*}'
        # Verify that no content token was altered beyond whitespace/alignment.
        canonical=lambda s: re.sub(r'\s+','',s)
        rebuilt=' = '.join(terms)
        assert canonical(formula)==canonical(rebuilt)
        body=body[:m.start()]+new+body[m.end():]
        logs.append(dict(language=lang,part='II',page=page,kind='display_lines',reason='Two-line equality chain; no mathematics or numbering changed.'))
    if lang=='fr':
        a,b=page_range(body,'87');chunk=body[a:b]
        formula=r'$(x_1,\dotsc,x_n)\mapsto \left(f(x_n),x_1,\dotsc,x_{n-1}\right)$'
        assert chunk.count(formula)==1
        new='\n'+r'\['+formula[1:-1]+r'\]'+'\n'
        chunk=chunk.replace(formula,new)
        body=body[:a]+chunk+body[b:]
        logs.append(dict(language=lang,part='II',page='87',kind='inline_to_display',reason='Keep the complete cyclic map together without stretched theorem prose; all content tokens unchanged.'))
    # The trace sum is indivisible enough that inline reflow leaves conspicuous
    # word spacing. Display its existing complete variant, retaining the comma.
    a,b=page_range(body,'176');chunk=body[a:b]
    tail='{S45-SOL-0697}$,';assert chunk.count(tail)==1
    y=chunk.index(tail)+len(tail);x=chunk.rfind('$',0,y-len(tail))
    fragment=chunk[x:y];assert fragment.startswith(r'$\var')
    new='\n'+r'\['+fragment[1:-2]+r'\text{,}\]'+'\n'
    body=body[:a+x]+new+body[a+y:]
    logs.append(dict(language=lang,part='VI',page='176',kind='inline_to_display',reason='Display the unchanged complete trace-sum variant and its comma; all readings and the occurrence identifier are preserved.'))
    for part,page,start,end in PARAGRAPHS[lang]:
        a,b=page_range(body,page);chunk=body[a:b]
        # The short p127 start is anchored additionally by the exact formula.
        if lang=='fr' and page=='127':
            pattern=r'On a\s*\$\\h_c\^\*\(\\dA\^1,\\pi_\*\\dZ/2\)'
            hits=list(re.finditer(pattern,chunk));assert len(hits)==1,(page,len(hits));x=hits[0].start()
        else:
            assert chunk.count(start)==1,(lang,page,'paragraph start',chunk.count(start))
            x=chunk.index(start)
        assert chunk[x:].count(end)==1,(lang,page,'paragraph end',chunk[x:].count(end))
        y=chunk.index(end,x)+len(end)
        old=chunk[x:y]
        stretch='4em' if (lang,page) in {('fr','87'),('fr','105'),('fr','161'),('fr','176'),('en','176')} else '2em'
        replacement=r'\begingroup'+'\n'+r'\emergencystretch='+stretch+r'\relax'+'\n'+old+r'\par'+'\n'+r'\endgroup'
        body=body[:a+x]+replacement+body[a+y:]
        logs.append(dict(language=lang,part=part,page=page,kind='paragraph_breaks',emergency_stretch=stretch,reason='Local final-pass line-breaking flexibility; no source text, math, font, variant, or marker changed.'))
    # The corrected twists and apparatus marks widen this existing small
    # three-column product diagram. Use the next standard size, locally.
    a,b=page_range(body,'149');chunk=body[a:b]
    pattern=r'\\small\s*(\\\[\\xymatrix@=0\.5cm\{.*?\}\\\])\s*\\normalsize'
    hits=list(re.finditer(pattern,chunk,re.S));assert len(hits)==1,(lang,'149',len(hits))
    m=hits[0];diagram=m[1].replace(r'\xymatrix@=0.5cm{',r'\xymatrix@=0.5cm@C=0.4cm{',1)
    replacement=r'\begingroup'+'\n'+r'\footnotesize'+'\n'+diagram+'\n'+r'\endgroup'
    body=body[:a+m.start()]+replacement+body[a+m.end():]
    logs.append(dict(language=lang,part='IV',page='149',kind='diagram_font',font='footnotesize',column_separation='0.4cm',reason='Locally size the complete product diagram and slightly reduce column spacing; retain every node, arrow, label and variant.'))
    # Both exact-sequence diagrams share one small-font scope. This also keeps
    # their geometry identical between diplomatic and corrected forms.
    a,b=page_range(body,'267');chunk=body[a:b]
    prop=chunk.index(r'\label{VIII:1-1-2}');x=chunk.index(r'\[\xymatrix{',prop)
    end=chunk.index(r'\end{proposition}',x);y=chunk.rfind(r'\]',x,end)+2
    original=chunk[x:y];assert original.count(r'\[\xymatrix{')==2
    replacement=r'\begingroup'+'\n'+r'\small'+'\n'+original+'\n'+r'\endgroup'
    body=body[:a+x]+replacement+body[a+y:]
    logs.append(dict(language=lang,part='VIII',page='267',kind='diagram_font',font='small',reason='One local scope for the two complete long exact sequences; all arrows and labels retained.'))
    return body,logs

if __name__=='__main__':
    from pathlib import Path
    import json
    folder=Path('work/rapport_cycle/layout_review')
    records=[]
    for lang in ['fr','en']:
        s=(folder/f'baseline_{lang}.tex').read_text()
        s,log=apply_layout_repairs(s,lang)
        # This local trial is separate from the assembled, shared readers.
        (folder/f'layout_trial_{lang}.tex').write_text(s)
        records.extend(log)
    (folder/'repairs_applied.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(records,ensure_ascii=False,indent=2))
