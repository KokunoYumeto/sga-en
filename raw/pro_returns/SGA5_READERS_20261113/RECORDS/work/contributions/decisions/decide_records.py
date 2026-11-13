#!/usr/bin/env python3
"""Reproduce the open-item inventory and exact source-based editorial patches.

Run from the directory containing work/sources, or pass --sources and --output.
Only relative archive member names appear in public records.
"""
from pathlib import Path
import argparse, collections, csv, hashlib, json, re

p=argparse.ArgumentParser()
p.add_argument('--sources',default='work/sources')
p.add_argument('--output',default='work/contributions/decisions')
args=p.parse_args()
src=Path(args.sources); out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
frpath='fr/sga5/current/s5.tex'
enpath='en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex'
F=(src/'SGA5_FR'/frpath).read_text()
D=(src/'SGA5_FR'/'fr/sga5/diplomatic/s5.tex').read_text()
E=(src/'SGA5_EN'/enpath).read_text()
originalE=E
patches=[]; decisions=[]

def note(item,page,readings,decision,reason,forms='all six',source=''):
    decisions.append(dict(item=item,page=str(page),readings=readings,decision=decision,reason=reason,forms=forms,source=source))

def patch(item,page,old,new,reason,forms='EN all',expected=1,language='EN'):
    global E,F
    text=E if language=='EN' else F
    actual=text.count(old)
    if actual!=expected:
        raise ValueError(f'{item}: expected {expected} exact occurrences, found {actual}; {old!r}')
    if not old or old==new: raise ValueError(item+': empty or unchanged patch')
    patches.append(dict(id=item,page=str(page),language=language,file=enpath if language=='EN' else frpath,
                        old=old,new=new,expected_count=expected,forms=forms,reason=reason,
                        source='port/SOL_NOTES_5.md' if item.startswith('SOL-EN-') else 'port/PORT_5_REPORT.md'))
    if language=='EN':E=text.replace(old,new)
    else:F=text.replace(old,new)

def solnum(n):return f'SOL-EN-{n:03d}'
def change(n,page,old,new,reason,expected=1):
    item=solnum(n);patch(item,page,old,new,reason,expected=expected)
    note(item,page,old+' -> '+new,'apply exact source-based translation repair',reason,'EN all','port/SOL_NOTES_5.md')

def retain(n,page,readings,reason,scan=False):
    note(solnum(n),page,readings,'needs the scan; keep recorded printed reading' if scan else 'retain source reading',reason,'all six' if scan else 'EN all','port/SOL_NOTES_5.md')

def scopechange(n,page,start,end,old,new,reason,expected=1):
    a=E.index(start);b=E.index(end,a+len(start));block=E[a:b]
    if block.count(old)!=expected:raise ValueError(f'{solnum(n)} scope occurrence count {block.count(old)}')
    change(n,page,block,block.replace(old,new),reason)

# French and English agree on the quotient morphism once its initial capital is
# corrected.  The equation q f' = (f'/G_x') q identifies the precise morphism.
patch('OPEN-H75',433,r"par $F'/G_{x'}$ l'endomorphisme",r"par $f'/G_{x'}$ l'endomorphisme",
      "The defining sentence descends f':X'->X' along q=p_1:X'->X'/G_{x'}; the quotient morphism satisfies q o f'=(f'/G_{x'}) o q. The pullback immediately below and formula (6.4.3) explicitly use this lowercase morphism. The printed capital is recorded by both French sources and their erratum comment.",
      forms='FR corrected apparatus; FR reading',language='FR')
note('OPEN-H75',433,"print: F'/G_{x'}; ported English: f'/G_{x'}",'correct F\' to f\' in the corrected French; retain ported corrected English; diplomatic forms retain F\'',patches[-1]['reason'],'FR and EN corrected; diplomatic variant retained','port/PORT_5_REPORT.md; fr/sga5/current/s5.tex')

change(1,17,r'\underline D_X=\underline D$',r'\underline D_K=\underline D$',
       'French I proof of Theorem 2.1 names the duality functor attached to K; its source reads D_K. Restore that named subscript in English.')
retain(2,18,r"\H^i(P'_{\ol{x}})=0",'The supplied ported English already has plain H in this expression; exact inspection confirms the proposed repair is present.')
change(3,19,'be a specialization morphism, and let','be a specialization morphism (SGA~A VIII~7.2), and let',
       'The corresponding French sentence explicitly cites SGAA VIII 7.2.')
patch(solnum(3),19,'be the corresponding specialization morphisms. There is a commutative square','be the corresponding specialization morphisms (SGA~A VIII~7.7). There is a commutative square',
      'The corresponding French sentence explicitly cites SGAA VIII 7.7.')
change(4,22,r'\begin{enumerate}[label=(\roman* bis)]'+'\n'+r'\item the analogue of (ii)',
       r'\begin{enumerate}[label=(\roman* bis),start=2]'+'\n'+r'\item the analogue of (ii)',
       'The French enumeration labels its two clauses (ii bis) and (iii bis); setting start=2 reproduces those labels exactly.')
oldnote=r'\footnote{\emph{Editorial note.} The printed source gives the intermediate term $\underline D_Y\R f_*\underline D_XF$ and cites Proposition~1.12(a)(i) for both successive arrows. This edition reproduces that chain. The mathematically coherent emendation is $\underline D_Y\R_!f\,\underline D_XF$ in the intermediate line, with Proposition~1.12(a)(ii) cited for the final arrow.}'
change(5,14,oldnote,'',
       'This is an added English editorial footnote. The source chain and its two references are retained. The properness assumption identifies Rf_* with R_!f; applying 1.12(a)(i) to F and then to D_X F yields the displayed intermediate and final terms. The proposed emendation in the added note is withdrawn and its full wording is retained in this decision record.')
change(6,70,'By purity, however,','By purity (4.3), however,','French p.70 explicitly gives the reference (4.3) before the displayed purity isomorphism.')
change(7,84,r"""(E,F) \arrow[d,"{(u_1\otimes^L_S E_2,\,v_1\otimes^L_S F_2)}"] & (E_1\otimes^L_S P_2,F_1\otimes^L_S Q_2) \arrow[l,"{(E_1\otimes^L_S u_2,\,F_1\otimes^L_S v_2)}"']""",
       r'(E,F) \arrow[r,"{(E_1\otimes^L_S u_2,\,F_1\otimes^L_S v_2)}"] \arrow[d,"{(u_1\otimes^L_S E_2,\,v_1\otimes^L_S F_2)}"] & (E_1\otimes^L_S P_2,F_1\otimes^L_S Q_2)',
       'French (2.4.1) places (E,F) at the upper right and points left to (E_1 tensor P_2,F_1 tensor Q_2). English interchanges the columns, so this same source-to-target arrow points right. Its source, target and label are preserved under that column permutation.')
change(8,88,'the sums of this square','the vertices of this square','French reads "les sommets de ce carré"; restore the corresponding English term "vertices".')
change(9,95,r'A_{X_2}\xrightarrow{\sim}f_2^!A_{Y_2}',r'A_{X_2}\xrightarrow{\sim}f_2^*A_{Y_2}',
       'French p.95 explicitly writes the canonical inverse-image identification A_X2 -> f_2^* A_Y2.')
retain(10,96,r'printed and corrected French: f_{2*}(4)\circ(2); proposed: (f_{2*}(4)\circ(2))^{-1}',
       'Both supplied French layers retain the un-inverted second path in the description following 3.5. The English follows that recorded reading. The added inverse is a new mathematical proposal; preserve both readings in the unresolved apparatus until the print and full diagram are rechecked.',scan=True)
change(11,98,r"g'_*d'^!\xrightarrow{\sim}d^!f_*",r"g'_*c'^!\xrightarrow{\sim}d^!f_*",'French p.98 explicitly labels this base-change isomorphism with c\' in its source.')
change(12,101,r"E''=C'\times_{X'}D'",r"E''=C'\times_XD'",'French p.101 defines this fibre product over X.')
change(13,115,r'p_{12}^*p_{12,2}^!L_2\to p_{23}^*p_{23,2}^*L_2',r'p_{12}^*p_{12,2}^!L_2\to p_{23}^!p_{23,2}^*L_2','French p.115 writes p_23^! in the target of the base-change arrow.')
change(14,127,r'\cl^d_{X/S}(Y)\in',r'\cl_{X/S}(Y)\in','French formula (6.8.1) writes cl_X/S(Y), without an extra superscript d.')
change(15,127,r'\Hom(\Lambda^d N_{Y/X},\Omega^d_{X/S}\otimes\cO_Y),&',r'\uHom(\Lambda^d N_{Y/X},\Omega^d_{X/S}\otimes\cO_Y),&','French (6.8.2) underlines Hom. The existing English macro uHom reproduces the underline at this exact occurrence.')
change(16,143,r'(Du)_z\in\Hom((DM)_y,(DM)_x)',r'(Du)_z\in\Hom((DM)_y,(DL)_x)','French p.143 explicitly has (DL)_x as the second argument, agreeing with the displayed dual correspondence Du.')
retain(17,144,r'printed and corrected French: (\{y\}\times Y,B); proposed: (\{x\}\times Y,B)',
       'The supplied French source retains y in this pair. The English accurately carries it. Keep that recorded printed reading and expose the suggested x alongside it for scan review.',scan=True)
change(18,148,r"h_*a'_*a'{}^!(DL_x\lten_{\Lambda}M_y)"+'\n'+r' \xrightarrow{\sim} a_*a^!(DL\lten_{\Lambda}M),',
       r"h_*a'_*a'{}^!(DL_x\lten_SM_y)"+'\n'+r' \xrightarrow{\sim} a_*a^!(DL\lten_SM),','Both French canonical isomorphisms use the external tensor product over S. Restore those explicit subscripts in the English.')
patch(solnum(18),148,r"h_*b'_*b'{}^!(L_x\lten_{\Lambda}DM_y)"+'\n'+r' \xrightarrow{\sim} b_*b^!(L\lten_{\Lambda}DM),',
      r"h_*b'_*b'{}^!(L_x\lten_SDM_y)"+'\n'+r' \xrightarrow{\sim} b_*b^!(L\lten_SDM),','French p.148 explicitly gives S at both tensor products in the second canonical isomorphism.')
change(19,151,r'f:T-Z\hookrightarrow T',r'f:T-Y\hookrightarrow T','French p.151 defines f as the inclusion T-Y -> T.')
change(20,152,r"E'=(P\lten_{\Lambda}Q)|T'-(X'\cup Y')"+'\n'+r"   =(P'\lten_{\Lambda}Q')|T'-(X'\cup Y').",
       r"E'=(P\otimes_SQ)|T'-(X'\cup Y')"+'\n'+r"   =(P'\otimes_SQ')|T'-(X'\cup Y').",'French p.152 gives ordinary external tensors over S at both occurrences in this definition.')

change(21,154,"X' & W' \\arrow[l,\"s'_1\"']", "X' \\arrow[d,\"f\"'] & W' \\arrow[l,\"s'_1\"']",'French p.154 includes the vertical morphism f:X\'->X in the diagram of Lemma 3.5; restore its arrow and label.')
change(22,156,r"X' & A'_{i'} \arrow[l]",r"X' \arrow[d] & A'_{i'} \arrow[l]",'French p.156 includes the left vertical arrow X\'->X in each of these two squares.')
patch(solnum(22),156,r"X' & B'_{j'} \arrow[l]",r"X' \arrow[d] & B'_{j'} \arrow[l]",'French p.156 includes the left vertical arrow X\'->X in the second square.')
old=r'''Z-(X\cup Y) \arrow[r,hook,"i'"] \arrow[d,"j"'] & Z-Y \arrow[d,"j"]\\
Z-X \arrow[r,hook,"i"'] \arrow[d,"m"'] & Z \arrow[d,"m"]\\
Y-z \arrow[r,hook,"i_1"'] & Y .'''
new=r'''Z-(X\cup Y) \arrow[r,hook,"i'"] \arrow[d,hook,"j'"'] & Z-Y \arrow[d,hook,"j"]\\
Z-X \arrow[r,hook,"i"'] & Z\\
Y-z \arrow[r,hook,"i_1"'] \arrow[u,hook,"m'"'] & Y \arrow[u,hook,"m"] .'''
change(23,158,old,new,'Copy the exact French diagram at p.158: the upper-left inclusion is j\'; the lower inclusions m\' and m run upward from Y-z and Y.')
change(24,158,r"i^*Rj_*i'_!L\xrightarrow{\sim}Rj_*(i'^*i'_!L)=Rj_*L",r"i^*Rj_*i'_!L\xrightarrow{\sim}Rj'_*(i'^*i'_!L)=Rj'_*L",'French p.158 explicitly primes the two right-hand j symbols in this base-change identification.')
change(25,160,r'''Y \arrow[r] & Y(\bar s)\\
Y(\bar z) \arrow[u] \arrow[r,"a"'] & \bar\eta \arrow[u,"b"']''',r'''Y & Y(\bar s) \arrow[l]\\
Y(\bar z) \arrow[u] & \bar\eta \arrow[l,"a"'] \arrow[u,"b"']''','Copy the source and target of both horizontal arrows in the French p.160 square: Y(sbar)->Y and etabar->Y(zbar).')
retain(26,160,r'recorded print: localization at \bar z; proposed: at \bar s','Both French layers retain the reference to the localization at zbar in this sentence. Retain that reading with the suggested sbar in the unresolved notes for review against the scan.',scan=True)
change(27,160,r"D=f^{-1}(z)(\simeq\mathbb P^1_S)",r"D=f^{-1}(z)(\simeq\mathbb P^1_s)",'The French source explicitly records its earlier scan-confirmed transcription repair (FIX#58): this exceptional divisor is printed P^1_s with lowercase s.')
retain(28,161,r"recorded print: RΓ(B'\cup D,i'_!(E')|B'-(B'\cup D)); proposed: RΓ(B'-D,i'_!(E')|B'-D)",'Both French layers preserve the printed union and nested set difference in this display. Keep the source reading, and record the proposed correction for scan review.',scan=True)
retain(29,170,r'recorded print: \uHom_A^\bullet(E,E)\to A; proposed target: A_\natural','French p.170 explicitly retains A in this sentence, while the nearby constructions use A_natural. Preserve the recorded reading and show the proposed target in the unresolved apparatus.',scan=True)
change(31,171,r'\RHom_A(E,F)\lten_{A^e}E \arrow',r'\RHom_A(E,F)\lten_AE \arrow','The French upper-left object of (5.9.1) has the outer tensor subscript A. The enveloping-algebra subscript stays on the scalar-extension factors.')
patch(solnum(31),171,r'\RHom_B(B\lten_AE,F\lten_{A^e}B^e)\lten_{B^e}(B\lten_AE) \arrow',r'\RHom_B(B\lten_AE,F\lten_{A^e}B^e)\lten_B(B\lten_AE) \arrow','The French lower-left object of (5.9.1) has the outer tensor subscript B.')
change(32,171,r'\in\ob D^b((B^e)^\circ)',r'\in\ob D^b(B^\circ)','French p.171 writes D^b(B^circ). Its correction history explicitly confirms this reading: taking Hom over the left B action retains the target\'s right B action, expressed by the action (h.b)(e)=h(e)b.')
retain(33,171,'recorded print: 5.3.6; proposed: 5.3.5','Both French layers cite 5.3.6 after (5.9.1). Keep the printed reference and record 5.3.5 as an unresolved alternative requiring the source page.',scan=True)
retain(35,171,'D^b((B^e)^circ) -> D^b(B^circ)','Duplicate of SOL-EN-032; the exact same occurrence is repaired once under that identifier.')
retain(36,171,'outer tensors A^e,B^e -> A,B','Duplicate of SOL-EN-031; the two exact occurrences are repaired once under that identifier.')
change(37,171,r'and $(F\lten_{A^e}B^e)\lten_B(B\lten_AG)\in\ob D^+(B)$',r'and $(F\lten_{A^e}B^e)\lten_AG\in\ob D^+(B)$','Restore the literal expression in the French hypothesis preceding (5.9.2). The longer expression remains in the diagram where the French also gives it.')
change(38,173,r'\Tr_A(f_g)=\Tr_A(gf)',r'\Tr_A(fg)=\Tr_A(gf)','French p.173 reads the product fg in this cyclic trace identity.')
change(39,173,r'({}_BE,{}^BP_A)',r'({}_BE,{}_BP_A)','French p.173 puts B in a left subscript of P, in the stated bimodule notation.')
change(40,175,'of the triangle\n\\[\n\\begin{tikzcd}[column sep=huge,row sep=large]','of the triangle\n\\[\n(*)\\qquad\n\\begin{tikzcd}[column sep=huge,row sep=large]','The French labels this triangle (*) and refers to its commutativity by that label.')
change(41,175,r'\RHom_B(E,B\otimes_KM)\lten_{B^e}E\longrightarrow M\lten_K(B\lten_{B^e}B)',r'\RHom_B(E,B\otimes_KM)\lten_BE\longrightarrow M\lten_K(B\lten_{B^e}B)','French p.175 puts B on the outer evaluation tensor, retaining B^e inside the target.')
change(42,177,'to conjugate 5.10.6 and 5.10.9','to combine 5.10.6 and 5.10.9','Here French conjuguer joins the two named results in a deduction; the English verb combine retains that use.')
# Occurrence audit: every one of the 69 RHom tokens in this bounded English
# passage has its underlined counterpart in the French passage.  Seven plain
# Hom tokens in the French remain plain at their separately matched sites.
a=E.index('Traces and extension of scalars'); b=E.index('\\subsection*{6.',a)
block=E[a:b];assert block.count(r'\RHom')==69
change(34,'171-182',block,block.replace(r'\RHom',r'\uRHom'),'The complete matched French passage III B 5.9-5.13 has 69 uRHom and no plain RHom; the English has 69 plain RHom in the corresponding sequence. Restore the underline token at each of these 69 exact matched occurrences. The plain Hom occurrences are audited separately.')
retain(30,'171-172','RHom -> uRHom','Covered once by the 69-occurrence passage repair SOL-EN-034, including the text and (5.9.1).')
a=E.index('Traces and restriction of scalars');b=E.index('\\subsubsection*{5.11',a)
block=E[a:b];n=block.count(r'\Hom');assert n==32
patch(solnum(34),'173-177',block,block.replace(r'\Hom',r'\uHom'),'All 32 plain Hom occurrences in English III B 5.10 correspond to underlined Hom in the French passage. Preserve the seven plain Hom occurrences subsequently used in 5.11-5.13.')
patch(solnum(34),182,r'{}_{(\psi)}B=\Hom_B(B,{}_{(\psi)}B)',r'{}_{(\psi)}B=\uHom_B(B,{}_{(\psi)}B)','French p.182 underlines Hom at this specific twisted scalar-restriction diagram node.')
patch(solnum(34),182,r'\Hom_A(B,{}_{(\varphi)}A)\otimes_AB',r'\uHom_A(B,{}_{(\varphi)}A)\otimes_AB','French p.182 underlines Hom at the second node of the same diagram.')

change(43,184,r'f_{1!}L_1\lten_{S,A}f_{2!}L_2',r'f_{1*}L_1\lten_{S,A}f_{2*}L_2','French (6.2.1) writes direct-image stars on both f_1 and f_2.')
change(44,184,r'f^!M_1\lten_{S,A}f^!M_2',r'f_1^!M_1\lten_{S,A}f_2^!M_2','French (6.2.2) explicitly indexes the two extraordinary inverse-image functors by 1 and 2.')
change(45,185,r't_A^! = KA_T',r't^!A = KA_T','French (6.3.1) applies t^! to A; preserve that literal operand position.')
retain(46,185,r'recorded print: E_2=KA_{X_1}; proposed: F_1=KA_{X_1}','The supplied corrected French also reads E_2 here. The proposed substitution is preserved as an unresolved reading for scan review; the English keeps the French source.',scan=True)
change(47,187,r'by applying $i^cc^!$',r'by applying $i_*^ci^{c!}$','French p.187 explicitly applies i_*^c i^{c!} in the sentence before (6.5.7).')
change(48,187,r'\delta^*c_*^c\RHom_A(c_1^*L,c_2^!L)',r'\delta^*c_*\RHom_A(c_1^*L,c_2^!L)','French (6.5.7) has c_* with no superscript c at this occurrence.')
change(49,188,r'\langle u,v\rangle_A=\Tr_A(\bar vu)=\Tr_A(u\bar v)',r'\langle u,v\rangle_A=\Tr_A(vu)=\Tr_A(uv)','French (6.6.4) writes the unbarred v in both products.')
retain(50,191,r'recorded print: D_c({}_AX)=D_c({}_{A[G]}X); proposed left side: D_c(G,{}_AX)','Both French layers preserve the left side without G. Retain it and record the proposed equivariant argument for scan review.',scan=True)
change(51,194,r'f_*M_n\in\Ob D_{\mathrm{ctf}}',r'f_*L_n\in\Ob D_{\mathrm{ctf}}','The corrected French p.194 writes L_n in this hypothesis; the printed M_n is retained through the diplomatic projection.')
retain(52,195,r'recorded print: F^n\Lambda_X=0 for n>=1; proposed bound: n>=2','Both French layers preserve the bound n>=1 alongside the separate F^1 definition. Retain the recorded printed bound and expose the suggested n>=2 for scan review.',scan=True)
retain(53,195,r'recorded print target: c_2^!(\Lambda_{X-U,X}); proposed: c_2^!(\Lambda_{U,X})','Both French layers retain the first target in the degree-one graded correspondence. Preserve that reading and show the alternative for scan review.',scan=True)
change(54,195,r'\underline c_{X-U,U}=j_*\underline c_{X-U}',r'\underline c_{X-U,X}=j_*\underline c_{X-U}','French (6.14.4) has X as the second subscript of the left correspondence.')
retain(55,195,'underline c, underline c_{U,X}, etc., to specify the base ring','The English sentence follows the exact French wording and symbols. Any added coefficient subscript requires an editorial reconstruction; keep the text and record the observation without such an addition.')
retain(56,197,'recorded print: every point x of G; proposed: every point x of C','The supplied French also reads "pour tout point x de G". Preserve it and show C as an alternative for review against the page.',scan=True)
retain(57,197,r'recorded print: f_*M; proposed: f_*L','Both French layers retain f_*M in Proposition 6.19. Keep the recorded reading and preserve the proposed L alongside it in the unresolved apparatus.',scan=True)
change(58,198,'be a proper $G$-morphism','be a proper $G$-$S$-morphism','French Proposition 6.21 explicitly says G-S-morphisme propre.')
retain(59,199,'diagram labels (1)-(5), (A), (B)','The supplied ported English diagram already contains all five arrow labels and the two phantom square labels; the suggestion is already satisfied.')
a=E.index('\\begin{statement}{Lemma 6.23.3}');b=E.index('\\subsection*{6.24}',a);block=E[a:b]
new=block.replace(r'\delta^*\RHom',r'\delta^*\uRHom')
new=new.replace(r'\RHom_{\Lambda[G]}(P,K_Y\lten P)',r'\uRHom_{\Lambda[G]}(P,K_Y\lten P)')
new=new.replace(r'\RHom_{\Lambda[G]}(P\lten Q,K_Y\lten P\lten Q)',r'\uRHom_{\Lambda[G]}(P\lten Q,K_Y\lten P\lten Q)')
new=new.replace(r'\RHom_{\Lambda[G]}(Q,Q)\xrightarrow{\Tr_{\Lambda}}',r'\uRHom_{\Lambda[G]}(Q,Q)\xrightarrow{\Tr_{\Lambda}}')
assert new.count(r'\uRHom')==7 and new.count(r'\RHom')==2
change(60,'201-202',block,new,'The French passage underlines Hom at these seven specific occurrences and keeps the two R Hom(Q,Q) factors in diagrams (*) and (**) plain. The English repair reproduces that exact occurrence-level assignment.')
change(61,202,'by conjugating 6.23.1 with the Lefschetz formula','by combining 6.23.1 with the Lefschetz formula','French en conjuguant links two named formulas in a deduction; combine is the matching English use, consistent with SOL-EN-042.')
retain(62,206,r'recorded French: \uHom_A(M,\Hom_C(X,Y)); proposed outer symbol: \Hom_A','French p.206 has the underlined outer Hom in the supplied source, as does the ported English. Preserve this explicit source notation and record the proposed plain reading for scan review.',scan=True)
change(63,216,'the set of isomorphisms from $X$ to $Y$ in $P\'_{AR}$','the set of morphisms from $X$ to $Y$ in $P\'_{AR}$','The French definition of Hom\'_AR(X,Y) says ensemble des morphismes; restore the corresponding English noun.')
retain(64,224,'reference to diagram (D); no detached label on the diagram','The French source likewise calls the following diagram (D) in the preceding sentence and has no detached label in its TeX diagram. The English preserves the same identifying text; retain without adding a new label.')
retain(65,233,r'p^n_{\mathrm{AR}}','The ported English already uses lowercase p at this occurrence after Definition 5.1.3; the proposed change is already present.')
retain(66,'245-246',r'Properties of \mathbb{E}(X)','The supplied ported English heading already uses mathbb E, matching the French heading; no second edit is needed.')

retain(67,308,r'h=f\circ g:\prod_i{}_XD_i\to S','The supplied ported English already includes the base X on this fibre product and on the definition of D immediately before it.')
change(68,311,r'A^\bullet(D)\otimes_{A^\bullet(X)}Q(X,g^*L)\to Q(D,g^*L)',r'A^\bullet(D)\otimes_{A^\bullet(X)}Q(X,f^*L)\to Q(D,g^*f^*L)','The corrected French gives f^*L over X and g^*f^*L over D in this second canonical morphism. The corresponding printed reading is retained through the diplomatic projection.')
change(69,314,'\\end{tikzcd}\n\\]\nIt is known that diagram $(D_1)$','\\end{tikzcd}\n\\]\n\\[\n(D_1)\\qquad\\qquad\\qquad\\qquad(D_2)\n\\]\nIt is known that diagram $(D_1)$','The French supplies the detached labels (D_1) and (D_2) directly below the pair of diagrams; restore those labels in the same order.')
change(70,341,'In fact, we shall prove the stronger statement $b_0=0$.','In fact, we shall show (which is equivalent by 9.1.1) that one even has $b_0=0$.','Restore the French parenthetical reference and equivalence assertion; the supplied English had omitted this clause.')
change(71,341,r'Since $X\times0$ is linearly equivalent to $X\times1$ in $X\times\mathbb P^1$, one has',r'Since $X\times0$ is linearly equivalent to $X\times1$ in $X\times\mathbb P^1$, one has the equality $f_1^*u_*(1)=f_1^*(X\times1)$, whence, since $\widehat N\cap f_1^{-1}(X\times1)=\emptyset$,','Restore the two omitted formulas and the connecting words from the French proof immediately before (9.4.6).')
change(72,365,r'\mathbf L\Phi_{X^\bullet}:D^-({}_A\cC)\longrightarrow D^-(\Ab).',r'\mathbf L^{-}\Phi_{X^\bullet}:D^-({}_A\cC)\longrightarrow D^-(\Ab).','The French displayed definition includes a superscript minus on its derived-functor symbol, also present in the next English sentence. Preserve the English macro vocabulary while restoring the missing superscript.')
retain(73,371,'recorded print: cf. SGA 3 I 4.7.2).; proposed: balanced punctuation','Both supplied French layers contain the unmatched closing parenthesis at the same point. Retain the recorded punctuation and register the balanced alternative for inspection of the printed page.',scan=True)
change(74,373,'and, for $g,h\\in G$, the diagram','b) For $g,h\\in G$, the diagram','French p.373 explicitly labels this second equivariance condition b); restore the label omitted by the English.')
retain(75,375,'recorded print: Weil formula 6.1 and local invariants in no. 5; proposed: formula 5.2 and local invariants in no. 6','Both French layers retain the two recorded references. Keep them in the translated body and preserve the suggested renumbering in the unresolved notes for scan review.',scan=True)
retain(76,379,'recorded print: defined in 4.1; proposed: defined in 3.4','French Proposition 3.6 explicitly says defini dans 4.1. Retain that source reference, with the suggested 3.4 recorded for inspection of the printed page.',scan=True)
retain(77,380,'recorded print: (4.3.1); proposed: (3.7.1)','Both French layers give (4.3.1) in the sentence after (3.7.2). Preserve that reference and expose the alternative in the unresolved apparatus.',scan=True)
change(78,391,r'\mathcal F(G,\mathbb Z_\ell)\xrightarrow{\lambda_n^*}\mathcal F(G,\mathbb Z/\ell^n\mathbb Z).',r'\mathcal F(G,\mathbb Z_\ell)\xrightarrow{\lambda_n^\natural}\mathcal F(G,\mathbb Z/\ell^n\mathbb Z).','The French labels this map on class functions with lambda_n^natural. Copy the superscript at this exact occurrence, leaving the two subsequent module-class maps lambda_n^* unchanged.')
patch(solnum(78),391,r'\lambda_n^*(\operatorname{tr}(\mu_\nu(S_1)))=\lambda_n^*(\sigma_2).',r'\lambda_n^\natural(\operatorname{tr}(\mu_\nu(S_1)))=\lambda_n^\natural(\sigma_2).','The French puts natural on both class-function reduction maps in this equation; the adjacent lambda_n^* inside tr and before mu_nu(S_1) is retained exactly as the French gives it.')
retain(79,393,r'\sum_{y\prime\in Y\prime}\nu_{y\prime}(g)','The ported English already gives nu at this Lefschetz-sum occurrence and in (5.2.2). No further v-to-nu edit remains.')
retain(80,393,'v_yprime(g) -> nu_yprime(g)','Duplicate of SOL-EN-079; the supplied port already contains the proposed nu at that exact place.')
retain(81,404,r'\RG_!V(F) -> compact-support subscript with V','The malformed token RG_!V(F) is absent from the supplied ported English. The p.404 compact-support formula is already written with its support marker and base V grouped as in the ported source; no second repair is applied.')
change(82,440,'largest distinguished subgroup of $H$','largest normal subgroup of $H$','The French sous-groupe distingue denotes here H_1 with gH_1g^{-1}=H_1 for every g in H, and the following quotient H/H_1 is the group used by the passage. Render the same subgroup property by the English term normal.')
change(83,470,'the normal closure\nof $\\mathbb Z_\\ell$ in $\\Omega$','the integral closure\nof $\\mathbb Z_\\ell$ in $\\Omega$','The French footnote calls for the normal closure of the valuation ring inside the coefficient field. The ring meant is {a in Omega : a satisfies a monic polynomial with coefficients in Z_ell}; integral closure is the English term for this same ring. The translated noun is repaired without altering the coefficient object or the French wording.')
patch(solnum(84),472,r'avec $F$ annulé par $\ell^{\nu+1}$',r'avec $F_\nu$ annulé par $\ell^{\nu+1}$','The scan prints bare F in this clause (scans/page_472_s3.png, x465-680,y45-110). In the immediately preceding sentence, the torsion sheaf F_nu and h_{F_nu}:h^*F_nu->F_nu enter formula (3)_nu. This sentence applies that formula for each component of the system F=(F_nu); the annihilation hypothesis therefore belongs to that same component F_nu. The corrected branch supplies the missing index and the diplomatic branch preserves F.',forms='FR corrected apparatus; FR reading',language='FR')
patch(solnum(84),472,r'with $F$ annihilated by $\ell^{\nu+1}$',r'with $F_\nu$ annihilated by $\ell^{\nu+1}$','Carry the scan-confirmed French editorial correction SOL-EN-084 into the corrected English; retain the scan reading F in the diplomatic English.',forms='EN corrected apparatus; EN reading')
note(solnum(84),472,r'printed: F; corrected: F_\nu','correct the missing component index in both corrected languages; preserve the scanned F in both diplomatic forms','The preceding formula (3)_nu is defined for the torsion component F_nu and its endomorphism h_{F_nu}. Applying it to each component of F=(F_nu) requires the same indexed annihilation hypothesis. The printed bare F is directly visible in scans/page_472_s3.png, x465-680,y45-110.','FR and EN corrected; diplomatic variant retained','port/SOL_NOTES_5.md; scans/page_472_s3.png')
change(85,475,'In view of the remark, this gives','In view of Remark 2, this gives','The French explicitly cites remarque 2 in this sentence; restore the omitted numeral in the English.')
retain(86,475,r'recorded print: endomorphism of K\prime; proposed: endomorphism of K\prime_\nu','The supplied French also says Kprime without the index nu in this sentence. Preserve that recorded reading, while retaining the indexed alternative for scan review.',scan=True)
retain(87,18,r'\H^i(P_{\ol{x}})=0','The supplied ported English already uses plain H in the unprimed expression, as it does in SOL-EN-002 for the primed expression.')
retain(88,19,'SGA A, Expose IX, 2.13; proposed replacement: SGA 4','The French introductory paragraph explicitly defines SGA A as the earlier seminar SGA 4. The citation SGAA IX 2.13 follows that authorial alias. Keep the alias, whose referent is already identified, rather than replace the printed citation notation.')
retain(89,'173-174,182',r'\Hom_A,\Hom_B -> \uHom_A,\uHom_B','Covered by SOL-EN-034: the 32 exact Hom occurrences in III B 5.10 and the two matched diagram nodes on p.182 have been repaired; the seven later plain Hom occurrences matching the French remain plain.')

# The six supplied review rows retain stable identifiers independent of their
# historical mix of decision/status fields.
review_source='fixes/REVIEW_5_OPEN.jsonl'
note('REVIEW-5-01',299,'recorded print: faisceau normal; handwritten alternative: faisceau conormal','needs the scan; retain normal in both source branches','The source records classify the thin added co as a reader annotation and preserve normal. N=J/J^2 and its dual occur explicitly in the same statement; replacing the noun is not required to recover its displayed formula. The printed-page image is outside the supplied range, so the handwritten insertion cannot be independently classified here.','all six; unresolved note in corrected apparatus',review_source)
note('REVIEW-5-02','417,420','printed: ring A in five places; corrected: R','retain all five recorded corrections','GLOBAL-99 and HANDFIX_5 give the completed all-five decision. The proof uses the valuation ring R of Proposition 4.6, and K=Frac(R) supplies the fraction field used in its last stage. The original A is retained in the diplomatic branch.','all six',review_source+'; conventions/GLOBAL_ISSUES_SGA.md, item 99')
note('REVIEW-5-03','414,416,423','Card in XII section 4; card on 69,393,401','retain the existing occurrence-level capitalization','All ten XII section-4 instances were already written operatorname{Card}; the conventions report checked lower-case card outside that section. No global macro replacement is warranted.','all six',review_source+'; reports/CONVENTIONS_5_REPORT.md')
note('REVIEW-5-04','408-432','H_{n,Uprime,Xprime}, H_{m,Uprime,Xprime}, H_{Uprime,Xprime}(ell) -> script H','retain the completed 45-occurrence convention in each French layer and its English counterparts','GLOBAL-97 and the conventions report record the scan check and all 45 applications per French layer. The cohomology H and the Galois-group H are explicitly excluded and retain their existing readings.','all six',review_source+'; conventions/GLOBAL_ISSUES_SGA.md, item 97')
note('REVIEW-5-05',435,'print repeats p.434 on p.435; transcribed folios jump 434 to 436','retain the body once; print an editorial notice at the folio jump','GLOBAL-100 identifies p.435 as a duplicate physical printing of p.434. Retain the established body and folio sequence, with an explicit notice accounting for the skipped folio.','all six',review_source+'; conventions/GLOBAL_ISSUES_SGA.md, item 100')
note('REVIEW-5-06','429,432','typed isomorphism sign approx; source macro simeq','retain the explicitly recorded simeq convention','GLOBAL-78 and GLOBAL-96c explicitly adopt this rendering for the recorded isomorphism sign, and the conventions pass restored the three itemized approx occurrences to simeq. The arrow signs on p.9 and approxeq on p.357 keep their separately recorded forms.','all six',review_source+'; conventions/GLOBAL_ISSUES_SGA.md, items 78 and 96c')

# Port report: the retrospective section 9 closes several earlier section-8
# items.  Its closed status is preserved instead of reopening completed work.
port_source='port/PORT_5_REPORT.md'
note('PORT-LEFT','all','PORT_EN5_LEFT.json: empty array','closed; no items to decide','The supplied JSON has zero entries.','EN all','port/PORT_EN5_LEFT.json')
note('PORT-UNCLEAR-REFUSED','all','PORT_EN5_LOG.jsonl: 1856 entries; no unclear or refused decisions','closed; no items to decide','Exact decision inventory is apply 707, already 138, not_applicable 1011. The 1856 item identifiers cover ITEMS_5.json exactly.','EN all','port/PORT_EN5_LOG.jsonl; port/ITEMS_5.json')
note('PORT-RAW-R20',331,'raw batch R20: unclear; final port log R20: already','closed by the hand-checked final decision','The raw batch decision questioned how to render the brackets in (8.5.4). HANDFIX_EN5 and the final PORT_EN5_LOG record the item as already; the English uses the relevant square brackets. The historical unclear entry is retained in the source audit, with its later disposition.','EN all','port/decisions/decisions_en5_full_017.json; port/HANDFIX_EN5.json; port/PORT_EN5_LOG.jsonl')
note('PORT-REPORT-8.1','all','working-tree publication pending in section 8; published commits recorded in section 9.6','closed by the later source record','Section 9.6 records sga-en d11a0c6 and sga-es e1fec10. The attached ported English is the base specified by the user; no repository publication action is part of the reader build.','source provenance',port_source)
note('PORT-REPORT-8.2',433,"F'/G_xprime versus f'/G_xprime",'decided by OPEN-H75','The exact corrected/diplomatic branches and quotient-morphism reason are recorded under OPEN-H75.','all six',port_source)
note('PORT-REPORT-8.3',420,'Spanish short proof versus full French proof of u(fprime_R) nonzero; C3106 and K55','closed by section 9.1; preserve the full proof in the English','The later report states that the full French proof was restored in the Spanish and both pending edits applied. The supplied English already keeps the full argument; no English paragraph is to be dropped.','EN all; Spanish outside these six readers',port_source)
note('PORT-REPORT-8.4','various','13 missing Spanish diplomatic edits; French diplomatic-only fixes','closed for the 13 Spanish edits; carry French diplomatic readings through the reader projection','Section 9.2 records all 13 Spanish edits placed. The current task derives English diplomatic branches from the French recorded printed/corrected differences, including differences absent from the earlier corrected-only port.','all six; Spanish outside these six readers',port_source)
note('PORT-REPORT-8.5-HEADINGS','VI 2.2.3; X 3.1,3.3,3.4; XII 4','added descriptive headings versus French numbered headings','closed by section 9.3; retain the supplied ported headings','The report records removal of the added headings, including English X 3.4. Keep the headings of the supplied ported source; do not regenerate the discarded titles.','EN all',port_source)
note('PORT-REPORT-8.5-DIAGRAM','V A.3','English repeated diagram d_3 has epi labels; report says French omitted them','retain both epi labels in the repeated English diagram','Direct inspection of both supplied French layers shows text{epi} labels on both horizontal arrows in the repeated proof diagram. The English labels reproduce those sources. The report sentence describing their absence does not match the attached final files.','EN all',port_source+'; fr/sga5/current/s5.tex; fr/sga5/diplomatic/s5.tex')
note('PORT-REPORT-8.6','various','SOL_NOTES_5.md: 89 English observations and 18 Spanish observations','English observations decided individually as SOL-EN-001 through SOL-EN-089','The English notes are matched to source paragraphs and each has an explicit disposition. The Spanish-only observations concern source files outside the supplied French and English reader task; their status is recorded separately without editing an unavailable Spanish text.','EN all',port_source+'; port/SOL_NOTES_5.md')
note('PORT-REPORT-8.7','not applicable','Flex refusal; Batch API completed the port','closed as an operational provenance record','The later report and complete 1856-entry port log give the completed English results. The API scheduling history does not imply a pending textual edit.','provenance only',port_source)
note('REPLAY-R9',184,'reworded corrected sentence versus printed (ou ...), dont on deduit de (loc. cit.)','closed by the later conventions pass; retain the restored printed sentence','REPLAY_MANUAL_5 still carries the earlier open status, but CONVENTIONS_5_REPORT Part 1 explicitly restores the printed sentence, including de (loc. cit.), and the supplied final current layer contains it. No second edit is required.','all six','fixes/REPLAY_MANUAL_5.json, R9; reports/CONVENTIONS_5_REPORT.md')

global_source='conventions/GLOBAL_ISSUES_SGA.md'
def globalnote(item,page,readings,decision,reason,forms='all six'):
    note('GLOBAL-'+item,page,readings,decision,reason,forms,global_source)
globalnote('75','1-5 and I','added SGA5 heading prefix; Preuve. versus Preuve :; set of primes bold n versus double-struck L','retain completed pilot repairs and recorded heading typesetting','The final layers have no added SGA5 heading prefix, retain the scoped proof labels and use mathbb{L} for the indicated prime set on the cited later occurrences. The source explicitly accepts its run-in label and heading typesetting; no extra replacement is introduced.')
globalnote('77-SGA5','volume','macro-dependent glyphs and exposé-specific conventions','retain the recorded scoped macros and inspect their rendered occurrences','The record warns that isolated checker fragments omit macro definitions. The reader projection must evaluate those definitions at each occurrence; a macro-definition difference alone is not an apparatus entry. The specific remaining R Gamma question is decided under GLOBAL-98a.')
globalnote('78','volume','typist glyph alternatives and established TeX renderings','retain the explicitly recorded glyph convention','The source authorizes this rendering convention. This build adds no blanket conversion of letters or operators; unresolved occurrence-specific cases are listed separately.')
globalnote('80','XII 4.7; V 4.2.2','Codex replacement proof and added hypotheses versus source proof and hypotheses','retain the recorded rejection of these reconstructions','The reconciliation record has already rejected the replacement proof of XII 4.7 and added hypotheses of V 4.2.2. The six readers keep the supplied full proof and existing hypotheses, and retain the 49 accepted reconciliation changes.')
globalnote('83','138-202','statement underlining; scoped plain R and R Hom with Hom underlined','retain the final occurrence-level emphasis and macro scopes','The final French layers include the statement emphasis from the page checks and end the III/III B macro scope at Exposé V. English Hom underlines missing from the port are restored at the exact matched occurrences under SOL-EN-034 and SOL-EN-060; plain Hom counterparts are retained.')
globalnote('85-LABELS','Exposé V','printed DEFINITION 1.1. - and related labels; existing bold mixed-case labels','needs the scan; retain the established source typesetting','The record gives example print labels but no complete per-label mapping, and the relevant scans are absent. Preserve the final source label forms; retain the stated printed alternatives as unresolved typography notes rather than infer one replacement across the exposé.')
globalnote('85-ARROWS','197-199','lower horizontal arrow labels above in the record of the print; below in the TeX','needs the scan; preserve each source arrow and its label','The positional observation is volume-wide and was not itemized. The arrow sources, targets and labels are retained exactly; moving labels by a global rule would require the unavailable pages and a per-diagram check.')
globalnote('89a','Exposé VII','printed capital statement labels with variable stops/dashes; existing bold mixed case','needs the scan; retain the established labels','The source gives several different punctuation patterns, including one label without stop or dash. There is no complete per-label placement record, so no uniform replacement is justified from the attached text.')
globalnote('89b','281-295','plain R in most recorded places; double-struck R in Rp_*, R_!p, Rf_* in proof 1.2','retain the completed itemized readings; needs the scan for any additional occurrence','The page checks applied occurrence-level font fixes, and the record explicitly identifies exceptions. Preserve those final occurrences and their macro scope; do not infer the unexamined ones from a single global definition.')
globalnote('89c','288-289','recorded typed P and E; existing mathbb P and mathbb E, 21 places','needs the scan; keep the established source renderings','The global note did not itemize the 21 sites. The unavailable pages are needed to map each claimed font reading to the exact occurrence. Preserve both stated readings in the unresolved notes.')
globalnote('89d','289-310','A^* versus printed A^bullet','retain the completed bullet restoration','The later conventions report restores seven occurrences on p.289 and two on p.310, retaining the corrected indices and bases. The supplied final Exposé VII has no A^* occurrence.')
globalnote('89e','Exposé VII','Module versus -module','retain the checked occurrence-level capitalization; needs the scan for unitemized sites','The source explicitly prohibits a blind pass and records capitalization page by page. Retain those final forms and list the general pending observation without changing unexamined prose.')
globalnote('89f','Exposé VII, including 295','typed plain O; hand-drawn script O_C; existing mathcal O','needs the scan; retain each final source occurrence','The supplied global note describes more than one glyph and gives no complete occurrence list. A new blanket replacement would discard that recorded variation. The final sources are retained and both glyph readings are exposed for later page inspection.')
globalnote('89g','285,289,330','tensor sign with two underlines; source double-underlined otimes','retain the explicitly recorded tensor rendering','The final French writes mathbin{underline{underline{otimes}}} at the recorded occurrences; GLOBAL-98 explicitly treats that double underline as part of the adopted notation. The reader macro set must reproduce the same printed sign.')
globalnote('89h','286-288','printed small p in A_p, mu_p, O_p(1); corrected capital P','retain all 13 recorded correction items together','The register identifies 13 small-p items in these pages; the current layer consistently uses the scheme P and the diplomatic layer preserves p. The exact map is p:P->S, with A_P and mu_P in D(P), and the displayed adjunction sends mu_P^{-1}[-2]->A_P to mu_S^{-1}[-2]->Rp_*A_P. This fixes the object denoted by each corrected subscript without altering the projection p.')
globalnote('VIII-Ob','351-371','ob from the original macro; printed Ob','retain completed scoped Ob definition','GLOBAL-96a and the conventions report record the scoped operatorname{Ob} definition. The report counts 19 uses in VIII; the earlier global estimate of 20 is superseded by that completed occurrence count.')
globalnote('VIII-CATEGORIES','351-371','typed plain C,D,A,B; source script cC,cD,cA,cB','needs the scan; retain the existing scoped category symbols','The unnumbered note identifies a glyph question without an occurrence-level list and points to the general convention. Preserve the final text; record the plain and script renderings for inspection rather than redefine four category macros globally.')
globalnote('VIII-QUOTES','351-371','straight printed quotes; guillemets in TeX; six pairs cited','retain the individually recorded quotation changes; needs the scan for remaining pairs','The note says the two pairs on pp.354-355 were itemized. Preserve the final source quotation marks at those sites and elsewhere; the missing images prevent a new blanket six-pair transcription.')
globalnote('VII-SET-DIFFERENCE','301 and Exposé VII','dotted minus in X dot-minus Y and Xprime dot-minus Yprime; other set differences','retain the two itemized dotted-minus occurrences; needs the scan for the rest','The final source explicitly writes mathbin{dot{-}} in both p.301 complements. Other occurrences were not inspected in the supplied note, so retain their existing symbols and expose the pending alternative.')
globalnote('96a','VIII and X','ob versus Ob','retain scoped Ob in VIII and X','The completed conventions pass explicitly set and ended the local definitions in both layers, with 19 uses in VIII and 16 diplomatic/17 corrected uses in X.')
globalnote('96b','X, 372-405','EP versus double-struck EP','retain the scoped double-struck EP rule','The conventions report records 26 uses covered in Exposé X and preserves the independent p.111 occurrence in III.')
globalnote('96c','9,357,429,432 and volume','simeq; xrightarrow{approx}; approxeq','retain the recorded occurrence exceptions','This duplicates REVIEW-5-06. The established convention keeps simeq for the specified typewriter isomorphism sign, with the explicit p.9 and p.357 exceptions preserved.')
globalnote('96d','69,393,401,414,416,423','Card in XII section 4; card elsewhere','retain the completed case-sensitive readings','This duplicates REVIEW-5-03; ten Card occurrences and the separately checked lower-case card occurrences remain unchanged.')
globalnote('96e','374-405','plain derived R at itemized sites; two remaining double-struck RG on 391,392','retain the recorded occurrence-level readings','The conventions report confirms the p.392 scan and the two remaining RG symbols. Preserve those two forms and the plain replacements from the page checks.')
globalnote('97','408-432','script H at 45 places; plain cohomology and Galois H','retain the completed 45-occurrence script-H convention','This duplicates REVIEW-5-04. The original H exclusions in the source record are kept.')
globalnote('98-FROBENIUS','441-480','single-underlined fr/Fr in XII 7.3; double-underlined in XV; three plain exceptions','retain the completed local definitions and explicit exceptions','The conventions pass records the scan-supported scopes and the plain occurrences on pp.443,456,460; it also records the six underlined Omega^1 on p.447. These completed changes are carried through without extending the rule to additional occurrences.')
globalnote('98a','457-474','32 target R Gamma occurrences: double-underlined upright R in the scan; diplomatic formerly double-struck, corrected plain upright','use each scan decision; diplomatic double underline; corrected plain upright R','The independent scan audit inspected every target and records its image region in PLACES_98_DECIDED.tsv. All 32 targets have the double underline, including the lower p.460 node; the separately printed plain R on p.461 is outside the 32 targets. The corrected branch keeps the source edition convention for derived functors.','all six; 32 occurrence variants')
globalnote('98b',441,r'retained in both branches: \underline{\operatorname{\mathbb{F}r}}_{Y/S}; unresolved alternative: \underline{\operatorname{Fr}}_{Y/S}','needs the scan; retain the supplied printed glyph in both branches','GLOBAL-98 expressly leaves this occurrence open against the general glyph convention of item 78. MISPRINTS_5 entry 572 records the underlined double-struck F but qualifies its glyph treatment. The p.441 scan is unavailable. Under the rule for unresolved readings outside the supplied scans, preserve that recorded printed glyph in all six readers and place the upright alternative in the nonvariant unresolved notes. The relative Frobenius morphism Y->Y^{(p/S)} and all other symbols of the display are unchanged.')
globalnote('99','417,420','five occurrences A -> R','retain the completed all-five correction','This duplicates REVIEW-5-02. The final current source corrects all five; the diplomatic keeps their printed A.')
globalnote('100',435,'duplicate printing of p.434','retain the established folio jump and add an explanatory notice','This duplicates REVIEW-5-05. The folio sequence 434,436 is deliberate and the underlying text is present once.')

# The Spanish-only observations are inventoried separately, without copying
# non-public filesystem locations or importing another language into the books.
sol_text=(src/'SGA5_EN'/'port/SOL_NOTES_5.md').read_text()
spanish=[];section=''
for line_no,line in enumerate(sol_text.splitlines(),1):
    if line.startswith('## '): section=line[3:]
    elif line.strip() and not line.startswith('#') and section.startswith('answer_es5_'):
        spanish.append({'item':f'SOL-ES-{len(spanish)+1:03d}','source_section':section,'source_line':line_no,'observation':line})
for row in spanish:
    note(row['item'],'Spanish source',row['observation'],'outside the requested French and English reader scope','This observation names a Spanish source not included among the six requested readers. Its related French/English reading is governed by the explicit language-specific decisions above; no Spanish text is supplied or edited here.','no requested reader','port/SOL_NOTES_5.md, '+row['source_section'])

# Final open-glyph disposition. The diplomatic source already has this
# printed form; both corrected branches now retain it pending the scan.
for language in ['FR','EN']:
    patch('GLOBAL-98b',441,r'\Fr_{Y/S}:Y\longrightarrow Y^{(p/S)}',r'\underline{\operatorname{\mathbb{F}r}}_{Y/S}:Y\longrightarrow Y^{(p/S)}',
          'Retain the recorded single-underlined double-struck F in the p.441 relative Frobenius display. GLOBAL-98b remains open, and its page is outside the supplied scans. Both branches preserve the supplied print under rule 3; the upright Fr is recorded as an unresolved alternative without a counted variant.',
          forms=language+' corrected apparatus; '+language+' reading',language=language)
    patches[-1]['source']='conventions/GLOBAL_ISSUES_SGA.md, item 98b; fixes/MISPRINTS_5.json, entry 572'

# Further inspected decisions are appended above the export marker.
note('EN-INHERITED-0046-P43',43,
     r'supplied diplomatic: i\prime\prime^*\underline{D}_{x}i\prime\prime^*\R^{!}j(F); supplied corrected: i\prime^*\underline{D}_{\ol{x}}i\prime\prime^*\R^{!}j(F); unresolved subscript alternative: \ol{\{x\}}',
     'needs the scan; preserve the supplied body readings and relocate the inherited English editorial note to the corrected apparatus only',
     r'The ported English contains an explicitly editorial footnote qualifying the first pullback stroke and the duality subscript in I 4.6. MISPRINTS_5 entries 54 and 55 record those two questions independently; entry 55 records the closure-subscript alternative alongside the factorization through i\prime\prime:closure{x}->Y. Page 43 is outside the supplied scans. The complete inherited note and its qualifications are preserved through an exact reversible wrapper extraction, while the frozen mathematical bodies and the 30 shared unresolved notes remain unchanged.',
     'EN corrected apparatus: inherited note relocated; all supplied mathematical body readings retained',
     'en/evidence/controls/standalone/sga5/controls/REMOVED_READER_PROSE_SGA5_001_002.texfrag:SGA5-READER-PROSE-002; en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex; fixes/MISPRINTS_5.json, entries 54 and 55')
# EXPORT
if __name__=='__main__':
    (out/'open_item_patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2)+'\n')
    (out/'decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
    with (out/'OPEN_ITEMS_DECIDED.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['item','page','readings','decision','reason','forms','source'],delimiter='\t');w.writeheader();w.writerows(decisions)
    print(json.dumps({'decisions':len(decisions),'patch_operations':len(patches),'EN_patch_operations':sum(x['language']=='EN' for x in patches),'FR_patch_operations':sum(x['language']=='FR' for x in patches)}))
