"""Independent semantic witnesses for the finite-cohomology English no-op rows."""
from pathlib import Path
import json,re,sys
sys.path.insert(0,'scripts')
from edition_tex import commands

W={}
def add(short,page,witness,explanation,classification='already conveyed in English'):
    ident='S45-SOL-'+short if short.isdigit() else short
    W[ident]=dict(page=str(page),witness=witness,explanation=explanation,classification=classification)

add('0982',234,'Speaking the language of derived categories has the advantage',
    'English already has the finite verb “has”; the French à/a error does not propagate.')
add('0985',234,'assuming that $X$ is smooth',
    'The scheme X remains an explicit math variable in the reduction to the smooth case.')
add('0987',234,'purely of relative dimension $n$',
    'The relative-dimension qualification and its variable n are both explicit.')
add('0988',234,r'K(n)[2 n]',
    'Both readings explicitly retain the coefficient complex, Tate twist n, and shift2n. The inserted isomorphism and pullback in the corrected formula are separately recorded by Sol0989.')
add('0991',235,r'($j:Y\hookrightarrow X$ a locally closed immersion and $\sF_1$ locally constant on $Y$)',
    'The parenthesis includes both the locally closed immersion and the sheaf on Y, with a closing parenthesis.')
add('0993',235,r'A variant of the argument of \ref{VII:1-6}',
    'English identifies the proof being varied and retains its reference1.6.')
add('0994',235,r'along a partition of $X$',
    'The partition is explicitly a partition of the scheme X.')
add('0995',236,'a finiteness theorem for vanishing-cycle sheaves',
    'The missing French word is already conveyed by the complete English finiteness statement.')
add('0997',236,'Let $X$ be a scheme of finite type',
    'The corollary begins with X explicitly introduced as a scheme.')
add('0998',239,r'with Galois group $G$, such that the inverse image $\sF_1$',
    'The English relative clause is grammatically correct and specifies the inverse-image sheaf on the covering.')
add('1000',240,r'for each $i$, there exists a dense open subset $U_i$',
    'Each projection index receives its own dense open subset, as required by the missing French phrase.')
add('1001',240,r'they hold over the union of the $\pr_i^{-1}(U_i)$',
    'The plural English pronoun correctly refers to the conclusions of the theorem.')
add('1003',240,'for the first, by the finiteness theorem',
    'The proof explicitly attributes the first term to the proper-morphism finiteness theorem.')
add('1004',240,r'with every base change in $S$',
    'English uses the ordinary lower-case term “base change” and retains the base S.')
add('1005',241,'finite, radicial, surjective base change',
    'All three properties of the base change are already stated in English.')
add('1006',241,r'V \ar@{^{(}->}[r]^j',
    'The inclusion V→X is explicitly labelled j in the English diagram.')
add('1007',241,r'The cohomology sheaves of $\Delta$',
    'The sentence concerns the cohomology sheaves of Delta, with the object explicitly identified.')
add('1009',242,r'acyclic at $x$ relative to $K$',
    'The definition includes both the point x and the coefficient complex K.')
add('1010',242,r"if it remains true after every base change $S' \to S$",
    'The universal condition explicitly requires persistence after every base change.')
add('1011',242,'We first deduce from the induction hypothesis that',
    'The induction hypothesis is explicitly the premise from which assertion(A) is deduced.')
add('1012',243,r'$X\xrightarrow u \dA_S^1 \to S$',
    'The factorization has the printed affine-line superscript1 and the arrow to S.')
add('1013',243,r'outside $T\subset X$ finite over $S$, $f$ is locally acyclic',
    'The lemma explicitly retains finiteness over S and local acyclicity of f outside T.')
add('1016',244,r'localized at $\eta$',
    'The geometric point is explicitly localized at the generic point eta.')
add('1017',244,r'endowed with an action of $\gal(\bar\eta/\eta)$',
    'The vanishing-cycle sheaves carry the specified Galois action.')
add('1018',244,r'Suppose that $X$ is of finite type over $S$',
    'The English hypothesis has the correct X and base S without the spurious French token.')
add('1019',244,r'$\eR^i\Psi_\eta(\sF)/\sG_i$',
    'The quotient formula is complete and its math delimiters close correctly.')
add('1020',244,r"uniformizers for $S$ are uniformizers for $S'$",
    'The English explicitly states that the same uniformizers work for S and S-prime.')
add('1023',245,'Let $f$ be one of the projections',
    'The English plural “projections” correctly expresses the family from which f is chosen.')
add('1024',245,r"$X\subset \dA_S^n\to \dA_S^1$. Let $X'$ be the ``localization''",
    'The affine-line formula closes before the following introduction of X-prime.')
add('1026',245,r"$X\times_{\dA_S^1} S'$ of $X$",
    'The localization is explicitly that of X, with X in math mode.')
add('1027',245,r"the inverse image of $\sF$ on $X'$",
    'The inverse-image sheaf is explicitly on X-prime.')
add('1029',246,r'$\sF$ be a sheaf of $A$-modules on $X$',
    'The sheaf symbol, coefficient ring, and scheme are all explicit.')
add('1030',246,'By passage to the limit, for each $i$',
    'The proof explicitly states the passage-to-the-limit argument before its indexed constructions.')
add('1032',247,'The long cohomology exact sequence deduced from',
    'The proof identifies the long cohomology exact sequence derived from the displayed short exact sequence.')
add('1033',247,r'$E_2^{p q} \sim \h^p(X_s,\sH^q)$',
    'The E2 term is related to H-p of the special fiber with coefficient sheaf H-q, including both exponents.')
add('1036',248,r'the strict henselization of $\dA_S^1$',
    'The English description correctly identifies the strict henselization.')
add('1038',248,'locally on $X$ and for every projection',
    'The argument retains the universal quantifier over projections.')
add('1041',248,'an isomorphism by the same invariance theorem',
    'The English conclusion explicitly invokes the same invariance theorem.')
add('1042',248,r'the $\eR^i f_\ast \sF$ are constructible',
    'The plural subject and predicate are grammatically correct in English.')
add('1043',248,r'their restrictions to the $Y_t$ ($t\in T$) are constructible',
    'English already uses plural restrictions and retains the indexed fibers.')
add('1044',249,r'applied to $X_s \to Y_s$',
    'The reference is explicitly applied to the morphism between the two special fibers.')
add('1045',250,r'a complex of sheaves of right $A$-modules',
    'English explicitly specifies right modules, without the French agreement error.')
add('1046',250,r'possible because $S$ has dimension $1$, shows that $K\iso D D K$',
    'The dimensional reason and resulting biduality isomorphism are both explicitly present.')
add('1049',251,r'The mapping cylinder $\Delta$',
    'The mapping cylinder is explicitly named Delta in the trait case.')
add('1050',252,'takes up certain parts of the late',
    'The introduction refers to certain parts of the earlier SGA5 material; the French agreement repair has no omitted English meaning.')
add('1051',252,r'For every specialization arrow $i:t\to S(s)$',
    'The universal quantifier, specialization arrow, and its source and target are explicit.')
add('1052',252,r'if $\bar S$ denotes the normalization',
    'The normalized scheme has the required overbar.')
add('1054',252,r'integral, with closed point radicial over $s$)',
    'The parenthesis remains open through the radicial closed-point qualification and then closes.')
add('1055',253,r"the coskeleton of $\bar S\to S'$",
    'The simplicial scheme is the coskeleton of the specified normalization morphism.')
add('1057',253,r'On the other hand, for $n>0$',
    'The secondary induction assertion is explicitly restricted to positive n.')
add('1058',253,r'$\h^i C(\bar S_n,s)=0$ for $i\leqslant N$',
    'The vanishing statement includes the cohomological exponent i, the simplicial index n, and the induction bound N.')
add('1060',254,r'Then, for every constructible $F\in\ob\eD^b(S,A^\circ)$',
    'The corollary explicitly quantifies over every constructible complex F in the stated category.')
add('1061',255,r'and $\eR f_\ast E$ is constructible',
    'Constructibility of the derived direct image appears as an explicit additional conclusion.')
add('1064',255,r'the fundamental class $\cl(D_i)$',
    'The canonical isomorphism is explicitly identified using the fundamental class of D-i.')
add('1068',256,'with the analogous formulas in integral cohomology',
    'English retains the comparison with the analogous integral-cohomology formulas.')
add('1072',257,'The canonical arrow',
    'The arrow introducing equation(2.2.2) is explicitly described as canonical.')
add('1073',257,r'at a geometric point $x$ of $X$',
    'The fiber calculation specifies both the geometric point x and its scheme X.')
add('1074',257,r"and that the fiber of \eqref{VII:eq:5-2-2-2} at $x$ identifies",
    'The second fiber identification retains the conjunction, point x, and equation reference2.2.2.')
add('1075',257,r"If $s'' \xrightarrow{u'} s' \xrightarrow u s$ are specialization arrows",
    'The two composable maps are explicitly identified as specialization arrows.')
add('1077',258,r'for every specialization $u:t\to S(s)$',
    'The universal specialization condition appears explicitly.')
add('1079',259,r'Let $x$ be a geometric point of $X$,',
    'The geometric point x is introduced on X with the correct following punctuation.')
add('1080',259,r'let $t\to S(s)$ be a specialization',
    'The map from t to the strict localization is explicitly a specialization.')
add('1081',259,'is an isomorphism. We may assume that $A$ is constant.',
    'The desired isomorphism and the subsequent reduction to constant A are distinct, complete sentences.')
add('1083',259,r'(\eR {f_{(x)}}_\ast (E|X(x)))_z',
    'The fiber subscript z applies to the derived direct image of the restricted complex.')
add('1084',259,r'\eR\Gamma(Y(y)_t,(E_x)|Y(y)_t)',
    'The displayed derived-section term includes the indicated restricted constant coefficient E-x on Y(y)-t.')
add('1088',260,'complex of finite tor-dimension',
    'The defining hypothesis requires a complex with finite Tor dimension.')
add('1090',261,r'The hypothesis implies that \eqref{VII:eq:5-2-10-1} is an isomorphism',
    'The final step explicitly attributes the isomorphism to the hypothesis and retains the equation target.')
add('S45-ASTRA-V-0001',236,r'Let $X$ be a scheme of finite type over a separably closed $k$, and let $\sF$ be a constructible sheaf',
    'The English introduces both X and F correctly. Retaining French plural Soient requires no change to the English construction.',
    'French grammar decision; English meaning already correct')
add('S45-ASTRA-V-0016',256,r'when $S=\spec(\dC)$',
    'The substantive complex-base case is explicitly present. The recorded unbreakable-box choice is French typography and does not require an English textual alteration.',
    'French layout decision; English meaning already correct')
add('S45-ASTRA-V-0017',261,Path('work/finitude_verdier/bibliography_261_en.tex').read_text(),
    'All four printed bibliographic entries are restored in their original order, with the English heading and “forthcoming” for the unpublished final entry.',
    'complete restored bibliography verified')

def normalize(s):return re.sub(r'\s+',' ',s).strip()
def resolve(s,corrected):
    for row in reversed(commands(s,'var',3,True)):
        s=s[:row['start']]+row['args'][int(corrected)]+s[row['end']:]
    return s

if __name__=='__main__':
    text=Path('work/finitude_verdier/en/sga4half_7_en.tex').read_text()
    chunks=re.split(r'\\PrintPage\{([^}]+)\}',text)
    pages=dict(zip(chunks[1::2],chunks[2::2]))
    cohort=[r for r in json.loads(Path('work/finitude_verdier/coverage_noops_en.json').read_text()) if str(r['page']).isdigit() and 233<=int(r['page'])<=261]
    assert set(W)=={r['id'] for r in cohort},('missing witnesses',sorted({r['id'] for r in cohort}-set(W)))
    for sid,r in W.items():
        for mode in [False,True]:
            assert normalize(r['witness']) in normalize(resolve(pages[r['page']],mode)),(sid,r['page'],mode,r['witness'])
    path=Path('work/finitude_verdier/coverage_witnesses_en_233_261.json')
    path.write_text(json.dumps(W,ensure_ascii=False,indent=2)+'\n')
    print('Saved',len(W),'independent English witnesses, each verified in both readings.')
