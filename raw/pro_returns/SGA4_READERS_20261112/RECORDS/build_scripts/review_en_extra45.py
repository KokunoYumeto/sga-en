"""Individually reviewed English consequences for 45 remaining agreed records.

The anchors are checked in the corrected projection of the current English
master. They retain the released vocabulary and mathematical spelling. Source
offsets are evidence, not instructions to patch a subsequently changed file.
"""
import json,re,sys
from pathlib import Path
from en_common import group,replace_spans
from en_extra import page_window,find_matches
ROOT=Path(__file__).resolve().parents[1]

# A French orthographic or inflectional repair has the same English realization
# on both sides at the identified occurrence. The literal English anchor records
# that realization; no English apparatus entry is created for these rows.
SAME={
31:("Indeed, by definition, a strict quotient", "The French plural ending in par définitions is an inflectional slip in the fixed phrase; both readings render by definition at this occurrence."),
41:("if $F$ is a sheaf of sets", "The French singular determiner un fixes the referent of faisceaux/faisceau; both render a sheaf of sets here."),
71:("Since the latter is cofinal", "The de/ce error occurs in the anaphor ce dernier for the preceding functor; both are represented by the latter in the released sentence."),
91:("a simple group $G_j$ in the class $j$", "The letter transposition calsse/classe has the same lexical realization class in this exact English sentence."),
105:("show that the latter is $\\Pi$-accessible", "The French infinitive and demonstrative misspellings montre/montrer and de/ce both map to the existing show that the latter construction."),
106:("preordered index sets", "The French des already specifies a plural; ensemble/ensembles d’indices both map to the released index sets."),
120:("$(\\ast)$ is an isomorphism", "The French un and singular subject determine one isomorphism; the extra final s has no separate English realization."),
134:("We must show that $y\\in U$", "The repaired French qu’on a y∈U and its missing-a printed form both express the displayed predicate through English that y∈U; English requires no counterpart of the French support verb a."),
198:("D. G. Quillen verified that", "The French past participle vérifiés/vérifié is rendered by the uninflected English past-tense verified."),
236:("possible to reconstruct $g$", "The erroneous acute accent in réconstituer leaves the English lexical rendering reconstruct unchanged."),
302:("are transformed by the equivalence $\\Phi$", "The omitted French s in tranformées is repaired in transformées; both realize the same English transformed at this occurrence."),
312:("category of left (\\resp right) $A'$-Modules", "The French plural des fixes Modules despite the dropped s; the released English already has plural Modules."),
318:("For every object $X$ of $C$", "The intrusive initial b in bobjet has the same English lexical realization object as objet."),
356:("category of left $\\Oo_S$-modules", "The French plural des fixes Modules despite the dropped s; both render the existing English modules."),
388:("all the preceding considerations carry over word for word", "The malformed infinitive transcrirent and corrected transcrire are realized by carry over in the released English construction."),
410:("morphisms satisfying one of the following conditions", "The French gender correction un/une has the same genderless English realization one of the following conditions."),
413:("normal crossings divisor", "The printed French singular croisement with plural normaux and the corrected croisements name the term rendered normal crossings divisor here."),
497:("addendum to Lemma", "The orthographic repair remord/remords in the parenthetical editorial addendum has the same released English realization addendum."),
}

# Complete local English spans, broad enough to distinguish nearby repeated
# symbols. These pairs preserve the exact authorial change, including omissions.
PAIRS={
29:(r"&\simeq \varprojlim_{C_{/C}} \Hom(X',Y)",r"&\simeq \varprojlim_{C_{/X}} \Hom(X',Y)"),
38:(r"$\Hhom(E,D)$ is also a $𝒰$-category",r"$\Hhom'(E,D)$ is also a $𝒰$-category"),
114:(r"\begin{enonce*}{Lemma 9.21.16}\etiquette[9.21.17]{I.lem9.21.17}",r"\begin{enonce*}{Lemma 9.21.17}\etiquette[9.21.17]{I.lem9.21.17}"),
146:(r"does not depend does not depend on the universe $𝒱$",r"does not depend on the universe $𝒱$"),
194:(r"it is itself the left adjoint of",r"it is itself the right adjoint of"),
195:("generalize functorial behavior to the case", "generalize this functorial behavior to the case"),
201:(r'''with the ``inclusion'' functor $j_{X!}:E_{/X}\rightarrow E$.''',r'''with the ``inclusion'' functor $j_{X!}:E_{/X}\rightarrow E$).'''),
215:(r"whose source lies in $E\in \widehat{E}$",r"whose source lies in $E\subset \widehat{E}$"),
247:(r"$C'$ the essential image of $f:\widehat{C}'\rightarrow \widehat{C}$",r"$C'$ the essential image of $f_{\ast}:\widehat{C}'\rightarrow \widehat{C}$"),
250:("complementation transforms infima and suprema and suprema into infima", "complementation transforms infima into suprema and suprema into infima"),
256:(r"\emph{support} of $G$ (\resp of $S$)",r"\emph{support} of $G$ (\resp of $s$)"),
259:(r"$g\circ i':\mathcal{F}\rightarrow E$ factors",r"$g\circ i':\mathcal{F}'\rightarrow E$ factors"),
262:(r"$Y$ an object of $A$, and a morphism from $X$ to $f(Y)$",r"$Y$ an object of $A$, and $u$ a morphism from $X$ to $f(Y)$"),
273:(r"arrow $f^{\ast}$ of $(\Esp)$ is a descent morphism",r"arrow $f$ of $(\Esp)$ is a descent morphism"),
284:(r"more generally, $\pi_0(\Top(X))$",r"more generally, $\pi_0(\Top(X/G))$"),
286:(r"canonical topology (), is homeomorphic",r"canonical topology (\hyperref[IV.exer7.8]{7.8}), is homeomorphic"),
308:(r"F\xrightarrow{\sim}\varprojlim_{\operatorname{Voix}(x)}",r"F\xrightarrow{\sim}\varprojlim_{\Vois(x)}"),
314:(r"A_∙(\Uu) \ZZ_∙(\Uu)\otimes_{\ZZ}A",r"A_∙(\Uu)\simeq \ZZ_∙(\Uu)\otimes_{\ZZ}A"),
323:(r"$R \hookrightarrow X$ be a covering target",r"$R \hookrightarrow X$ be a covering sieve"),
345:(r"denote by $\sheaf{\Delta}_n^c$ the standard semi-simplicial object",r"denote by $\sheaf{\Delta}_n$ the standard semi-simplicial object"),
361:(r"Taking the sheaf contains $\CC$ for $\mathfrak{F}$",r"Taking the constant sheaf $\CC$ for $\mathfrak{F}$"),
365:(r"the functor $P_{J}(\alpha)_{\ast}$",r"the functor $p_{J}(\alpha)_{\ast}$"),
373:(r"$H^n(X,\prod_{t\in T}F_t)=0$ for every $n$",r"$H^n(X,\prod_{t\in T}F_t)=0$ for every $n>0$"),
405:(r"morphisms $z\to x$, $z\to Y$ in $E_b$",r"morphisms $z\to x$, $z\to y$ in $E_b$"),
498:("for the Zarisky topology on a scheme", "for the Zariski topology on a scheme"),
499:[(r"The topos $F$ is identified with",r"The topos $\underleftarrow{F}$ is identified with"),
     (r"for every object $M$ of $F$ we have",r"for every object $M$ of $\underleftarrow{F}$ we have")],
500:(r"$\Hhom_{\cart/I^{\circ}}(I^{\circ},F')$ into $\Hom_{I^{\circ}}(I^{\circ},F')$",r"$\Hhom_{\cart/I^{\circ}}(I^{\circ},F')$ into $\Hhom_{I^{\circ}}(I^{\circ},F')$"),
}

def main():
    src=ROOT/'output/en/SGA4_EN_annotated_master.tex'
    text=src.read_text();edits=[]
    for m in re.finditer(r'\\SGA(?:quiet)?var\b',text):
        try:
            _,_,j,_=group(text,m.end());new,_,j,_=group(text,j);ident,_,j,_=group(text,j)
        except ValueError:continue
        if ident.startswith('EN-'):edits.append((m.start(),j,new))
    text=replace_spans(text,edits)
    mps=json.loads((ROOT/'sources/fixes/MISPRINTS_4.json').read_text())
    rows=[];failed=[]
    for num in sorted(set(SAME)|set(PAIRS)):
        r=mps[num-1];ident=f'MP{num:04d}'
        row=dict(id=ident,expose=r['expose'],page=r['page'],source='fixes/MISPRINTS_4.json#'+ident,
                 printed_french=r['print'],corrected_french=r['correct'],place=r['where'])
        w=page_window(text,r['expose'],r['page'],1)
        local=text[w[0]:w[1]] if w else ''
        if num in SAME:
            anchor,reason=SAME[num];hits=find_matches(anchor,local)
            row.update(assessment='no English impact',reason=reason,english_reading=anchor,
                       location_verified=bool(hits),hits=len(hits))
            if not hits:failed.append(ident)
        else:
            pairs=PAIRS[num];pairs=pairs if isinstance(pairs,list) else [pairs]
            ds=[]
            for old,new in pairs:
                oh=find_matches(old,local);nh=find_matches(new,local)
                hits=[(a,b,'printed') for a,b in oh]+[(a,b,'corrected') for a,b in nh]
                hits=[h for h in hits if not any(h[0]>=z[0] and h[1]<=z[1] and h[1]-h[0]<z[1]-z[0] for z in hits)]
                d=dict(printed=old,corrected=new,location_verified=len(hits)==1,hits=len(hits))
                if len(hits)==1:
                    a,b,state=hits[0];d.update(current_anchor=local[a:b],current_state=state,
                        context_before=local[max(0,a-90):a],context_after=local[b:b+90])
                else:failed.append(ident)
                ds.append(d)
            row.update(assessment='English-impact',reason='Exact local English phrase or formula carries the canonical accepted French delta; the checked source occurrence determines both diplomatic and corrected readings.',english_deltas=ds)
            if len(ds)==1:row['english_delta']=ds[0]
        rows.append(row)
    out=ROOT/'output/shared/EN_REVIEW_EXTRA45.json'
    out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print('Rows',len(rows),'no-impact',len(SAME),'impact',len(PAIRS),'failed',failed)

if __name__=='__main__':main()
