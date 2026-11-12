# English font, underline, and normalization audit

## Scope and method

This audit checks distinctions that token normalization can hide. It removes percent-comments before locating mathematical expressions, aligns the complete French diplomatic and corrected formula sequences, and then compares their original TeX with whitespace alone ignored. Font application is checked with its argument, so equal counts of font commands cannot hide a change in their scope. A separate pass locates mathematical underline differences while ignoring only the underline command for alignment. Original-English Exposé VI is excluded from transfer because both editions already take its complete variants directly from the same paired French-package witnesses.

The English formula normalizer drops blackboard, calligraphic, fraktur, and several other font wrappers, braces, equation tags, and some spacing. It **retains mathematical underline commands**. Consequently the underline check also tests the correspondence between underlined French notation and a calligraphic symbol chosen consistently in the released translation.

## Complete audit of normalized-equal formula pairs

Exactly **31** source formula pairs compare equal under the normalizer but differ after whitespace removal. Their complete source readings are retained in `EN_FONT_UNDERLINE_AUDIT.json`.

| Difference class | Pairs |
| --- | --- |
| equation label | 12 |
| equivalent single-token brace group | 1 |
| font | 12 |
| math spacing only | 1 |
| subscript or accent scope | 5 |

The two cases without a change of mathematical content are a redundant brace group around the single superscript token `\natural`, and a thin space inside the multiplicative-group subscript. The latter does change printed spacing and remains a French typographic apparatus entry. No phi/varphi, epsilon/varepsilon, arrow, or inequality-alias difference occurs among these paired sources. Every equation-label change and every change in subscript or accent scope has an explicit English reconstruction. Unnumbered printed displays use `\notag`; an existing English cross-reference anchor is retained without displaying an invented equation number.

The five scope differences are the comma inside `H_{s,}` on XIX331; the twist absorbed into `O_{Delta(1)}` on XVIII277 and `O_{X(1)}` on XVIII294; and two occurrences of the closure bar over `Q_ell` together on XVIII326. These follow the designated source layers; they are not claims of a new inspection of the physical print.

## Mixed font and symbol changes

All **36** French apparatus entries outside Exposé VI that change a blackboard, calligraphic, fraktur, bold, sans-serif, script, or italic math-font application were reviewed. There are **0 unreviewed entries** in that mechanical scope. This includes changes where a symbol or mathematical expression changes at the same time as its font. Existing complete reconstructions are identified separately; moved ambient-space phrases and wholly inserted Galois numerators are not misclassified as isolated font errors.

## Exact English operations

The audit supplies **43** native English operations. Each corrected string and its offset is asserted against the unchanged native release component. The printed branch alone changes. The final column records whether the exact proposed printed passage is already present in the latest reconstructed diplomatic text read by this run; it must be refreshed after integration.

The stricter component-level count check passes for **43 of 43** operations: each corrected target is unique in its assigned component, its diplomatic target adds exactly one occurrence relative to the corrected baseline, and the corrected target disappears from that diplomatic component. Existing duplicate equation labels are therefore accounted for explicitly.

| Operation | Exposé / folio | Corrected English span | Printed English span | Exact printed span present |
| --- | --- | --- | --- | --- |
| ED-EN-FONT-G000 | 7I IX / 403 | `A_n=\mathcal A\times_{\widehat S}S_n` | `A_n=A\times_{\widehat S}S_n` | yes |
| ED-EN-FONT-G001 | 7I IX / 445 | `\mathbb Z_S\subset\mathbb Q_S` | `\mathbb Z_S\subset Q_S` | yes |
| ED-EN-FONT-G002 | 7I IX / 452 | `(U\otimes\mathbb Q_\ell)^I\simeq U^I` | `(U\otimes Q_\ell)^I\simeq U^I` | yes |
| ED-EN-FONT-G003 | 7I IX / 515 | `where $G_K$ itself is of one of these types.` | `where $\mathbb G_K$ itself is of one of these types.` | yes |
| ED-EN-FONT-G004 | 7II XVIII / 320 | `H^{n-1}(X\cap H_s,\mathbb Q_\ell)` | `H^{n-1}(X\cap H_s,Q_\ell)` | yes |
| ED-EN-FONT-G005 | 7II XVIII / 327 | `Thus a $\mathbb Q_\ell$-subspace $M$ of $E$` | `Thus a $Q_\ell$-subspace $M$ of $E$` | yes |
| ED-EN-FONT-G006 | 7II XVII / 247 | `A=\mathbb Z[[X_1,\ldots,X_a]]` | `A=Z[[X_1,\ldots,X_a]]` | yes |
| ED-EN-FONT-G007 | 7II XVI / 202 | `$\mathbb E_S^{n+1}$ defined by an equation` | `$E_S^{n+1}$ defined by an equation` | yes |
| ED-EN-FONT-G008 | 7II XXII / 416 | `converges in $\mathbb Q_p(\xi_p)$` | `converges in $Q_p(\xi_p)$` | yes |
| ED-EN-FONT-G009 | 7II XXII / 416 | `\in\mathbb Q_p[[X]],` | `\in Q_p[[X]],` | yes |
| ED-EN-FONT-G010 | 7II XXII / 418 | `\tau\in\operatorname{Gal}(K/\mathbb Q_p(\xi_p))` | `\tau\in\operatorname{Gal}(K/Q_p(\xi_p))` | yes |
| ED-EN-FONT-G011 | 7II XX / 362 | `$\mathbb Q_\ell$-homologous to zero` | `$Q_\ell$-homologous to zero` | yes |
| ED-EN-FONT-G012 | 7I VIII / 264 | `and to $M=\mathbb Z/n\mathbb Z$` | `and to $\mathbb Z=\mathbb Z/n\mathbb Z$` | yes |
| ED-EN-FONT-G013 | 7I VIII / 302 | `\mathrm{Hom}\bigl(\Phi\otimes\Psi,(\mathbb Q/\mathbb Z)_k\bigr)` | `\mathrm{Hom}\bigl(\Phi\otimes\Psi,Q/\mathbb Z\bigr)` | yes |
| ED-EN-FONT-G014 | 7I IX / 493 | `let $\underline R$ be the sheaf of sections of $R$` | `let $\mathbb R$ be the sheaf of sections of $R$` | yes |
| ED-EN-FONT-G015 | 7II X / 2 | `$\underline{O}_{Z_o}$` | `$O_{\mathbb Z_o}$` | yes |
| ED-EN-FONT-G016 | 7II XI / 48 | `\longrightarrow H^q\bigl(\mathbb P(\underline E),\mathbb Z/\ell^m\bigr)` | `\longrightarrow H^q(Y,\mathbb Z/\ell^m)` | yes |
| ED-EN-FONT-G017 | 7II XIV / 160 | `H^*(U^*,V)  \xrightarrow[(4.18.1)]` | `H^*(U^*,\mathbb C)  \xrightarrow[(4.18.1)]` | yes |
| ED-EN-FONT-G018 | 7II XVII / 215 | `A pencil $D=\{H_t\}_{t\in D}$` | `A pencil $D=\{H_t\}_{t\in\mathbb P}$` | yes |
| ED-EN-FONT-G019 | 7II XVIII / 295 | `\longrightarrow H^p(\mathbb P^1,R^n\rho_*\mathbb Q_\ell)` | `\longrightarrow H^p(\mathbb P^1,\mathbb R^1\rho_*\mathbb Q_\ell)` | yes |
| ED-EN-FONT-G020 | 7II XX / 361 | `\geq \dim_{\mathbb Q}` | `\geq \dim_Q` | yes |
| ED-EN-FONT-G021 | 7II XXII / 435 | `\longrightarrow\mathcal O_V\longrightarrow0,` | `\longrightarrow\mathcal O_V\longrightarrow\mathcal O,` | yes |
| ED-EN-FONT-G022 | 7II XXII / 435 | `\mathcal O_V \arrow[r] \arrow[d,"\mathfrak F_q"'] & 0\\` | `\mathcal O_V \arrow[r] \arrow[d,"\mathfrak F_q"'] & \mathcal O\\` | yes |
| ED-EN-FONT-G023 | 7II XXII / 435 | `\mathcal O_V \arrow[r] & 0 .` | `\mathcal O_V \arrow[r] & \mathcal O .` | yes |
| ED-EN-FONT-G024 | 7II XXII / 437 | `f(X)^{q-1}\cdot \mathfrak F_q` | `f(X)^{q-1}\cdot f_q` | yes |
| ED-EN-FONT-G025 | 7II XVII / 218 | `$\mathcal Y\to\check{\mathbb P}^{r}$ makes` | `$Y\to\check{\mathbb P}^{r}$ makes` | yes |
| ED-EN-NORM-G026 | 7I IX / 452 | `\tag{\SGARefTarget{sga7.sga7i.eix.n11-3-4}{11.3.4}}` | `\tag{\SGARefTarget{sga7.sga7i.eix.n11-3-4}{11,3.4}}` | yes |
| ED-EN-NORM-G027 | 7I IX / 471 | `\tag{\SGARefTarget{sga7.sga7i.eix.n12-3-3}{12.3.3}}` | `\tag{\SGARefTarget{sga7.sga7i.eix.n12-3-3}{12.2.3}}` | yes |
| ED-EN-NORM-G028 | 7I IX / 471 | `\tag{\SGARefTarget{sga7.sga7i.eix.n12-3-4}{12.3.4}}` | `\tag{\SGARefTarget{sga7.sga7i.eix.n12-3-4}{12.2.4}}` | yes |
| ED-EN-NORM-G029 | 7I IX / 472 | `\tag{\SGARefTarget{sga7.sga7i.eix.n12-3-8}{12.3.8}}` | `\notag\SGARefAliasTarget{sga7.sga7i.eix.n12-3-8}` | yes |
| ED-EN-NORM-G030 | 7II XII / 76 | `\tag{3.3.1}` | `\tag{3.2.1}` | yes |
| ED-EN-NORM-G031 | 7II XVIII / 309 | `\tag{5.8.7.3}` | `\notag` | yes |
| ED-EN-NORM-G032 | 7II XVII / 244 | `\tag{5.2.6$'$}` | `\tag{5.2.6}` | yes |
| ED-EN-NORM-G033 | 7II XV / 181 | `\tag{2.1.7.1}` | `\tag{2.1 7.1}` | yes |
| ED-EN-NORM-G034 | 7II XXII / 422 | `\tag{4.5.14}` | `\tag{5.4.14}` | yes |
| ED-EN-NORM-G035 | 7II XXII / 423 | `\tag{4.5.23}` | `\tag{4.5.2.3}` | yes |
| ED-EN-NORM-G036 | 7II XXII / 425 | `\tag{4.5.33}` | `\tag{4.5.23}` | yes |
| ED-EN-NORM-G037 | 7II XXII / 428 | `\tag{5.0.4}` | `\tag{5.0.7}` | yes |
| ED-EN-NORM-G038 | 7II XIX / 331 | `$H^{2n}(H_s,\mathbb Q_\ell)$, and that this image equals` | `$H^{2n}(H_{s,}\mathbb Q_\ell)$, and that this image equals` | yes |
| ED-EN-NORM-G039 | 7II XVIII / 277 | `\begin{aligned} c_1(\underline N_{\widetilde\Delta/\widetilde X})^2 &=g^*\!\left(c_1(\xi_\Delta)^2\right)` | `\begin{aligned} c_1(\underline N_{\widetilde\Delta/\widetilde X})^2 &=\left(g^*c_1(\underline{\mathcal O}_{\Delta(1)})  -(\rho i)^*c_1(\xi_{\mathbb P^1})\right)^2\\ &=g^*\!\left(c_1(\xi_\Delta)^2\right)` | yes |
| ED-EN-NORM-G040 | 7II XVIII / 294 | `first Chern class of $\underline{\mathcal O}_X(1)$` | `first Chern class of $\underline{\mathcal O}_{X(1)}$` | yes |
| ED-EN-NORM-G041 | 7II XVIII / 326 | `$\bar E=E\otimes_{\mathbb Q_\ell}\bar{\mathbb Q}_\ell$` | `$\bar E=E\otimes_{\mathbb Q_\ell}\overline{\mathbb Q_\ell}$` | yes |
| ED-EN-NORM-G042 | 7II XVIII / 326 | `$\bar{\mathbb Q}_\ell$-linear subspace` | `$\overline{\mathbb Q_\ell}$-linear subspace` | yes |

## Mathematical underline check

The independent underline pass finds **19** pairs. The following records identify their exact contextual treatment. Font-family repairs are included above when merely removing an underline would lose the printed glyph.

| Exposé / folio | French printed | French corrected | English treatment |
| --- | --- | --- | --- |
| 7I IX / 404 | `M` | `\underline{M}` | Existing formula and manual dual-group reconstruction on folio404. |
| 7I IX / 418 | `M'` | `\underline{M}'` | Existing port and formula operations remove the underline from the second twisted-constant module. |
| 7I IX / 478 | `S` | `\underline{S}` | Existing port and formula operations cover the representability statement overS. |
| 7I IX / 478 | `S` | `\underline{S}` | Existing port and formula operations cover the formal-smoothness statement overS. |
| 7I IX / 480 | `S` | `\underline{S}` | Existing port and formula operations cover the groupE overS. |
| 7I IX / 481 | `u_\ell` | `\underline{u}_\ell` | Existing port and formula operations cover u_ell. |
| 7I IX / 482 | `\underline{X}^\lambda = X \times_{S} \underline{S}^\lambda` | `\underline{X}^\lambda = \underline{X} \times_{\underline{S}} \underline{S}^\lambda` | Existing complete-formula operation removes the two erroneous underlines on the right side. |
| 7I IX / 482 | `X_o^\lambda` | `\underline{X}_o^\lambda` | Existing port and formula operations cover the special-fibre symbolX_o^lambda. |
| 7I IX / 488 | `E'_s` | `\underline{E}'_s` | Existing port and formula operations cover the second free moduleE-prime. |
| 7I IX / 488 | `\hat{E}_s` | `\hat{\underline{E}}_s` | Existing port and formula operations retain the completion hat and remove its inner underline. |
| 7I IX / 493 | `\mathbb{R}` | `\underline{R}` | ED-EN-FONT-G014 restores the printed blackboardR, repairing the plainR left by the earlier transfer. |
| 7I IX / 504 | `R_{\underline{O}}` | `\underline{R}_{\underline{O}}` | Existing port and formula operations cover R_{underline O}. |
| 7I IX / 505 | `R'{}^{t}_{U}` | `\underline{R}'{}^{t}_{U}` | Existing port and formula operations cover the second toric-part symbol. |
| 7I IX / 512 | `(\underline{M},M')` | `(\underline{M},\underline{M}')` | Existing formula operation covers the second module in the pair. |
| 7II XVII / 218 | `Y \longrightarrow \check{\mathbb{P}}^r` | `\underline{Y} \longrightarrow \check{\mathbb{P}}^r` | ED-EN-FONT-G025 confirms the already reconstructed calligraphicY-to-plainY correspondence. |
| 7II XXI / 386 | `H^i_c (X,\underline{G})` | `\underline{H}^i_c (X,\underline{G})` | ED-EN-FORMULA-G233. |
| 7II XXI / 391 | `H_c^i(X,G)^\vee` | `\underline{H}_c^i(X,G)^\vee` | ED-EN-FORMULA-G235. |
| 7II XXI / 393 | `H^i_c(X,\underline{G})` | `\underline{H}^i_c(X,\underline{G})` | ED-EN-FORMULA-E236. |
| 7II X / 2 | `O_{\mathbb{Z}_o}` | `\underline{O}_{Z_o}` | ED-EN-FONT-G015 restores both plainO and the blackboardZ subscript. |

## Limits and reproduction

Ordinary upright-versus-italic math typography (mathrm/operatorname), text emphasis and prose-underlining spans are not automatically recased to French typography. Font styling consistently chosen by the released translation is retained. Source Expose VI is shared directly, so its font differences are already carried by source identity.

Run `python build/glossary_font_audit.py --reports-only` after the English reconstruction to refresh the presence checks without rewriting the stable reconstruction-input ledger. The complete machine record includes all raw source pairs, the mixed-change review, exact native strings and offsets, and each reconstruction reason. Ordinary authorial prose emphasis and font choices consistently adopted by the translation are outside a mechanical reversal to French typography. No unverified general rule is applied to them.
