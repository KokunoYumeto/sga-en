#!/usr/bin/env python3
"""Adjudicate the two displaced VI Codex/HOLD records from their actual pages."""
from pathlib import Path
import shutil
from review_helpers import Review
r=Review()
why37=('Both complete primary/native390–391 pairs print X_1,...,X_n after reducing the preceding number of bundles to n=1, and print no rank-stratification paragraph. '
 'The actual forgetful morphism Flag(k^3)→P^2_k sends a complete quotient flag to its rank-one quotient. Over each such quotient its remaining choices are rank-one quotients of its two-dimensional kernel, so the fiber is P^1_k. Thus the first projective stage X_1 cannot already be the complete-flag scheme in this printed n=1 example. '
 'The construction needs a stopping-rank specification, but the print supplies no new binding for n. Splitting into rank strata, choosing a common rank bound, and rebinding a separate rank index lead to different added passages and different stopping-index conventions. The proposed HOLD paragraph is an expansion absent from both source images, and its exact added wording is not uniquely selected by them. Retain the source passage in both bodies; record the precise forgetful map and fiber counterexample rather than insert the proposed paragraph.')
for id in ['fr/codex/HOLD_VS_CORR.json#37','fixes/RECONCILE_CODEX_6.json:entries#224','fixes/RECONCILE_CODEX_6.json:entries#319']:
 r.source(id,'X_1,...,X_n; no inserted rank-stratification sentence',why37,'Construction ending390 and opening391',page=390,witness=401,
  verdict='confirmed',change='Retain the printed/current passage; confirm rejection of the expanded HOLD reconstruction.')
 r.decisions[-1].update(is_misprint=False,correction_status='Author indexing retained; no unique source-supported replacement',supplemental_images=['scan/SGA6_scan_360dpi.pdf#page=405','scan/SGA6_witness_300dpi.djvu#page=402'])
r.own_finding('ASTRA-VI-FLAG-STOPPING-390',390,'X_1,...,X_n after n=1','Same printed indexing','Retain both bodies and document the exact stopping-index problem.',why37,'Construction across390–391',kind='author_claim',verdict='confirmed',witness=401)
r.own[-1].update(is_misprint=False,correction_status='No unique source-supported replacement',supplemental_images=['scan/SGA6_scan_360dpi.pdf#page=405','scan/SGA6_witness_300dpi.djvu#page=402'])

printed=r'\sum_{i=1}^{n}c_i=\prod_{j=1}^{k}\left(\sum_{i=1}^{p_j}c_i^{(j)}\right)'
corrected=r'1+\sum_{i=1}^{n}c_i=\prod_{j=1}^{k}\left(1+\sum_{i=1}^{p_j}c_i^{(j)}\right)'
why38=('Both complete primary/native395 images print the displayed equality without either constant1, and the personally read396 top assigns weight i to c_i and c_i^(j). '
 'In Z[xi_1,...,xi_n][t], the coefficient of t^r in product_a(1+xi_a t) is the sum of monomials indexed by r-element subsets. Intersection with the declared disjoint blocks gives the exact bijection I↦(I∩B_1,...,I∩B_k), preserving each monomial and total cardinality. The empty subset contributes1 in every factor and in the total product. Consequently product_a(1+xi_a t)=product_j(1+sum_i sigma_i(block_j)t^i)=1+sum_r sigma_r(xi_1,...,xi_n)t^r. '
 'Apply the coefficientwise ring homomorphism to C=A[xi]/(sigma_r−c_r); its images are the stated c_r and c_i^(j). The n positive-degree coefficients give exactly c_r=sum_(a_1+...+a_k=r) product_j c_(a_j)^(j), with the empty-block coefficient1. The isobaric instruction selects these coefficient identities; its weights are formal bookkeeping and assert no grading on arbitrary A or specialized C. '
 'For A=Z,n=k=2,p_1=p_2=1,c_1=3,c_2=2, evaluation xi_1↦1,xi_2↦2 kills both defining relations and gives a unital C→Z. It sends the printed equality to5=2, while the corrected total equality gives6=6 and its coefficients give3=1+2,2=1·2. '
 'Adding1+ before the total sum and inside each block factor preserves every printed index and the isobaric instruction, and restores exactly the constants forced by the elementary-symmetric definitions. Diplomatic retains the original; current accepts this minimal part of the earlier Codex proposal. The formerly proposed extra terminal comma remains rejected because both scans omit it. Independent coefficient/context audit:independent_block_symmetric_audit_395.json, a text/math audit carrying no additional image claim; its separate source-context checks do not claim a proof of the lemma’s basis or ideal-generation assertions.')
for id in ['fr/codex/HOLD_VS_CORR.json#38','fixes/RECONCILE_CODEX_6.json:entries#216','fixes/RECONCILE_CODEX_6.json:entries#320']:
 r.source(id,printed,why38,'Lemme4.3(ii), final display and396 weight instruction',page=395,witness=406,
  verdict='amended',change=corrected+'; preserve the absence of terminal punctuation.')
 r.decisions[-1].update(is_misprint=True,correction_status='Previously rejected constant-term correction now accepted')
id='ASTRA-VI-BLOCK-SYMMETRIC-CONSTANTS-395'
r.own_finding(id,395,printed,printed,corrected,why38,'Lemme4.3(ii), final display',kind='misprint_in_print',witness=406)
r.own[-1].update(is_misprint=True,correction_status='accepted paired constant-term correction')
r.patch(395,'current',printed,corrected,id,why38)
shutil.copyfile(Path(__file__).parent.parent/'english/EN_INDEPENDENT_VI_BLOCK_SYMMETRIC_AUDIT_395.json',Path(__file__).parent/'independent_block_symmetric_audit_395.json')
r.commit()
