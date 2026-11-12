r"""English anchors inspected against their canonical accepted MP records."""
from en_common import *

PAIRS=[
('MP0005','I',12,
 r'One immediately verifies that $\varprojlim_I F\prime$ (\resp $\varinjlim_I F\prime$) is isomorphic',
 r'One immediately verifies that $\varprojlim_I F$ (\resp $\varinjlim_I F$) is isomorphic'),
('MP0009','I',24,
 r'For every object $Y$ of $C$, this gives a morphism of functors',
 r'For every object $Y$ of $C\prime$, this gives a morphism of functors'),
('MP0012','I',34,
 r'C/H \ar[r]^{u/H}\ar[d]_{J_H}',r'C/H \ar[r]^{u/H}\ar[d]_{j_H}'),
('MP0020','I',43,
 r'let us prove that $u$ is an isomorphism',r"let us prove that $u'$ is an isomorphism"),
('MP0021','I',43,
 "fiber category $E_X$. Then two arrows from $X'$ to $Y'$ lie\n  over the same arrow $\\id_X$ of $E$, and hence are identical,\n  so $E_X$ is ordered.",
 "fiber category $E'_X$. Then two arrows from $X'$ to $Y'$ lie\n  over the same arrow $\\id_X$ of $E$, and hence are identical,\n  so $E'_X$ is ordered."),
('MP0029','I',50,r'\varprojlim_{C_{/C}} \Hom',r'\varprojlim_{C_{/X}} \Hom'),
('MP0044','I',63,r'Then $I$ is filtered: indeed,',r"Then $I'$ is filtered: indeed,"),
('MP0045','I',64,r"preordered set $OB\,I'$",r"preordered set $\Ob\,I'$"),
('MP0047','I',65,r'with source $x$ and target $y$ has',r'with source $x$ and target $e$ has'),
('MP0050','I',66,r'This indeed gives a finite subdiagram of $E$.',r'This indeed gives a finite subdiagram of $I$.'),
('MP0060','I',87,r'We may already suppose that $g$, hence $\Ind(f)$, is fully faithful.',r'We may already suppose that $f$, hence $\Ind(f)$, is fully faithful.'),
('MP0075','I',106,r'consisting of those $y\in A$ such that $y\leq x$',r'consisting of those $y\in C$ such that $y\leq x$'),
('MP0076','I',106,r'that $L$ is injective and that the order',r'that $L_\circ$ is injective and that the order'),
('MP0084','I',117,r'for the sum of the $X(\alpha)$ in $\Ind(C)$ to be universal,',r'for the sum of the $X(\alpha)$ in $\Pro(C)$ to be universal,'),
('MP0087','I',131,r"where $C$ is a fixed small generating subcategory of $C$",r"where $C'$ is a fixed small generating subcategory of $C$"),
('MP0090','I',134,r'the hypotheses on $E$ in \hyperref[I.cor8.12.7]{8.12.7}',r'the hypotheses on $C$ in \hyperref[I.cor8.12.7]{8.12.7}'),
('MP0092','I',135,r'projective system $(X_i)_{i\in I}$ in $E$,',r'projective system $(X_i)_{i\in I}$ in $C$,'),
('MP0093','I',138,
 r"let $C'_1$ be a small generating subcategory of $C$, and $\Pi$ a cardinal such that the $Y'\in \Ob C'$ are",
 r"let $C'_1$ be a small generating subcategory of $C'$, and $\Pi$ a cardinal such that the $Y'\in \Ob C'_1$ are"),
('MP0096','I',145,r'then so is $\varprojlim X_j$.',r'then so is $\varinjlim X_j$.'),
('MP0098','I',146,r'the set of strict subobjects of $E$ is small',r'the set of strict subobjects of $X$ is small'),
('MP0100','I',146,r'Indeed, let $I$ be an ordered set large relative to $I$,',r'Indeed, let $I$ be an ordered set large relative to $\Pi$,'),
('MP0107','I',161,r'moreover that, for every $a\in\ob B$,',r'moreover that, for every $\alpha\in\ob B$,'),
('MP0108','I',166,r'Consider the composite $X(\alpha_i)\rightarrow X(\alpha)',r'Consider the composite $X(\alpha)_i\rightarrow X(\alpha)'),
('MP0109','I',166,r'factors through some $f^\ast(X(\alpha)_j)$',r'factors through some $f^\ast(X(\beta)_j)$'),
('MP0115','I',171,r'the cartesian sections of $E$ over $F$.',r'the cartesian sections of $E$ over $B$.'),
('MP0127','I',180,r'and the fiber products $A_i\times_AA_j$ are representable.',r'and the fiber products $A_i\times_BA_j$ are representable.'),
('MP0139','I',212,r'(x_{n+1}\in x_n\in x_{n+1}\in\ldots)\mapsto',r'(x_{n+1}\in x_n\in x_{n-1}\in\ldots)\mapsto'),
('MP0142','I',217,r"$M_{g'}$ of upper bounds of $g$ are not isomorphic.",r"$M_{g'}$ of upper bounds of $g'$ are not isomorphic."),
('MP0149','II',243,r'Q_2 \ar[r]^{V_2}',r'Q_2 \ar[r]^{v_2}'),
]

def records():
    result=[]
    for ident,exp,page,a,b in PAIRS:
        # Prime control words are made explicit in these two text anchors.
        a=a.replace(r'\prime',"'");b=b.replace(r'\prime',"'")
        result.append(dict(id=ident,source=ident,file=next(k for k,v in EXPOSE.items() if v==exp),page=page,printed=a,corrected=b,kind='agreed misprint',place='canonical MP place; inspected English context',manual=True))
    return result

if __name__=='__main__':
    (RECORDS/'EN_MANUAL_PAIRS.json').write_text(json.dumps(records(),ensure_ascii=False,indent=2)+'\n')
    print(len(records()),'reviewed English anchors')
