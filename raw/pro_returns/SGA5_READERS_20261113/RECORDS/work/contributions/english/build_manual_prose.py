from pathlib import Path
import json,re
out=Path(__file__).parent
s=(out/'EN_corrected_flat.tex').read_text()
vs=[]
def add(pg,after,before,src='fr/sga5/diplomatic/s5.tex;fr/sga5/current/s5.tex',reason='Translate the distinct printed and corrected source readings at this place.'):
 if after not in s:raise ValueError((pg,after))
 vs.append({'page':pg,'after':after,'before':before,'source':src,'reason':reason})
add(34,'and in particular satisfies conditions (ii) and (iii) of 1.7.','and in particular satisfies conditions (ii) and (ii) of 1.7.')
add(45,'the duality isomorphism (SGAA~XVIII~3.1.10):','the duality isomorphism (SGAA~3.1.10):')
add(89,r'\subsection*{3.1}',r'\subsection*{3.L}')
add(181,'The traces 5.13.2 coincide','The traces 5.14.2 coincide')
add(199,'The arrows (1) and (3) are given','where (1) and (3) are given')
add(211,'is filtering (SGA 4 I 2.7).','is filtering (SGA 4 1 2.7).')
add(234,'the canonical functors','the canonical functions')
add(247,'from the generalities of A.1','from the generalities of A 1')
anchor='\\[\n\\mathcal E_r^{(n)}(X)=\\bigl(\\mathcal E_r^{p,q}(X)\\bigr)_{p+q=n}.\n\\]'
duplicate='\\[\nE^{(n)}_r(X)=\\bigl(E_r^{p,q}(X)\\bigr)_{p+q=n}\n\\]\nis canonically endowed with the structure of a graded \\((\\gr^\\bullet(S),\\mathcal D)\\)-module. The same holds by passage to the limit for\n'
add(248,anchor,duplicate+anchor,reason='The French diplomatic source repeats the E_r display and its explanatory sentence at the folio boundary; the corrected source removes that repetition.')
add(267,'Then, as in (1.3.3), one sees','Then, as in (1.3.2), one sees')
add(268,'As in (1.3.4), one defines','As in (1.3.3), one defines')
add(268,'Paragraph (1.3.4) adapts','Paragraph (1.3.3) adapts')
add(269,r'with the functor \(G\longrightarrow\cHom(F,G)\) (1.3.3)',r'with the functor \(G\longrightarrow\cHom(F,G)\) (1.3.2)')
add(270,'This allows one, as in (1.4.5),','This allows one, as in (1.4.6),')
add(271,'noetherian object (V 1.3).','noetherian object (5 1.3).')
add(293,'so by Corollary (2.2.6) the inverse-image homomorphism','so (2.2.5), the inverse-image homomorphism')
add(317,'By (SGA 4, Exposé V bis, 2.5.5 and 2.5.6),','By (SGA),')
a='Let $X$ be a projective smooth connected $k$-scheme of dimension $n$, and let $Y$ be a smooth hyperplane section of $X$, defined by a section of an ample $\\mathcal O_X$-module $L$. Let $p$ be the canonical morphism from $X$ to $k$ and $p_*$ the corresponding Gysin morphism.'
b='Let $X$ be a proper smooth connected $k$-scheme of dimension $n$, and let $Y$ be a smooth closed subscheme of dimension $n-1$ of $X$, thus defined by a section of an invertible $\\mathcal O_X$-module $L$. Let $p$ be the canonical morphism from $X$ to $k$ and $p$ the corresponding Gysin morphism.'
add(323,a,b,reason='The printed Corollary 7.4 has the proper/closed-subscheme/invertible hypotheses and p for the Gysin morphism; the corrected source records the projective/hyperplane/ample version and p_*.')
add(329,r'Using moreover the identity $c_{d-1}(\check F)=(-1)^{d-1}c_{d-1}(F)$, the lemma follows',r'The lemma follows',reason='The corrected source supplies this explicit identity in the proof; the diplomatic source has no corresponding clause.')
add(345,r'when $X$ is replaced by $X\times\mathbb P^1$',r'when is replaced by $X\times\mathbb P^1$')
add(345,r'it is immediate (cf. $(D_1)$) that',r'it is immediate (cf. $(D_1)$ that')
add(367,r'\emph{Proof of Proposition 8.1.}',r'\emph{Proof of Proposition 5.2.}')
add(382,'one can use the isomorphisms (3.8.1).','one can use the isomorphisms (4.3.4).')
add(384,r"for the map $s:C'\to C'$ (Lemma 4.1)",r"for the map $s:C'\to C'$ (Lemma 5.1)")
add(390,'where the first member of (5.2)','where the first member of (6.2)')
add(390,'On the other hand, by Proposition 3.2,','On the other hand, by Proposition 3.3.1,')
add(393,'Comparison with (5.2.1) gives','Comparison with (6.2.1) gives')
add(396,'satisfying conditions i), ii) of 6.1.','satisfying conditions i), ii) of 7.1.')
add(401,'as in 6.1, and let $F$ be a complex of sheaves','as in 7.1, and let $F$ be a complex of sheaves')
add(426,'the classical Lefschetz formula (cf. III, 4.8 and 4.10).','the classical Lefschetz formula (cf. ).')
add(433,r"let $G_{x'}$ be the stabilizer of the point $x'$",r"let $G_{x'}$ be the stabilization of the point $x'$",reason='The printed French noun is stabilisation; the corrected noun is stabilisateur. The diplomatic English retains the literal erroneous noun.')
add(441,r'and let $F$ be a sheaf of $\Lambda$-modules on $X$.',r'and a sheaf of $\Lambda$-modules on $X$.')
# The indices retain the source print's XIV where the corrected source supplies XV.
for m in re.finditer(r'\\sgaindexentry\{([^\n]*)\}\{([^\n]*XV[^\n]*)\}',s):
 a=m[0];b=a.replace('XV','XIV')
 if 'rationality of' in a:
  b=b.replace('XIV 3 no. 2','XIV 2 no. 2')
 pg=484 if m.start()>s.index('Index of Notation') else (481 if 'Frobenius correspondence' in a else 482)
 add(pg,a,b)
(out/'manual_prose_variants.json').write_text(json.dumps(vs,ensure_ascii=False,indent=2))
print('manual prose variants',len(vs))
