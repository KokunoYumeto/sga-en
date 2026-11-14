#!/usr/bin/env python3
"""Source415 lower-endpoint correction with explicit basis maps."""
from pathlib import Path
import shutil
from review_helpers import Review
r=Review();id='ASTRA-VI-BASIS-PRODUCT-415'
why='The complete primary and native415 images both print the lower index0 and upper indexr. The preceding414 sentence defines r as the relative dimension of the actual flag tower and asserts that x-prime is a K(X)-basis element. The reviewed projective-bundle basis of1.13 transforms from1,xi,…,xi^q to1,(xi−1),…,(xi−1)^q by the triangular binomial matrix; its inverse is xi^j=sum_(m=0)^j binom(j,m)(xi−1)^m. Composing these exact module-basis maps through the3.1 projective tower produces the top basis monomial with sum of the stage relative dimensions=r factors. The printed r+1 assertion fails already for the identity flag tower over Spec(k):r=0,every line class is1,and the printed single factor is0,whereas the corrected empty product is the basis element1. On P^1 the explicit ring Z[delta]/(delta^2),delta=xi−1,also makes every two-factor product of line-class differences zero. Current changes the lower endpoint0→1 and retains the printed upper endpoint. The alternative endpoint edit0≤i≤r−1 is related exactly by j=i+1,xi_j=eta_(j−1),including r=0; the choice here claims no unique unseen author indexing intention. The source fixes the factor count. The top-coordinate map pi_top(x-prime·f^*(a))=a proves the following cancellation without assuming multiplication by x-prime injective on all K(X-prime). Full maps and counterexamples are in basis_product_415.json.'
r.own_finding(id,415,r"x'=\prod_{i=0}^{r}(\xi_i-1)",r"x'=\prod_{i=0}^{r}(\xi_i-1)",r'Current lower endpoint1; diplomatic0.',why,'First display, conclusion of6.9 proof',kind='misprint_in_print',witness=426)
r.own[-1].update(is_misprint=True,correction_status='accepted paired factor-count correction',proof_file='review/expose_vi/basis_product_415.json')
r.patch(415,'current',r"x'=\prod_{i=0}^{r}(\xi_i-1)",r"x'=\prod_{i=1}^{r}(\xi_i-1)",id,why)
shutil.copyfile(Path(__file__).parents[1]/'english/EN_INDEPENDENT_VI_BASIS_PRODUCT_AUDIT_415.json',Path(__file__).parent/'basis_product_415.json')
r.commit()
