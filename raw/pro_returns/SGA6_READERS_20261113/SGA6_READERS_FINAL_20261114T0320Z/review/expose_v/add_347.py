#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=347
r.finding('346_350',7,'The category in Ob(G) is a single handwritten script G with a connected descending tail.',
 'Main361 upper strip and native358 top resolve the loop and connected descender. This is the graded K-algebra category already named in1.11, and the supplied mathcal G agrees. The sixteen historical occurrences have now each received a direct page check.',
 'Definition6.2, Ob argument',witness=358)
r.finding('346_350',8,'The words les relations are followed by a typed colon.',
 'Main first/second strips and native358 top clearly show both vertically arranged dots. The attached colon agrees.',
 'sentence before6.2.1',witness=358)
r.finding('306_310',14,
 'All sixteen listed historical category occurrences have a handwritten script G with a connected descender: actual308(6),309(2),310(1),311(3),313(1),344(1),345(1),347(1).',
 'Every listed occurrence was directly compared during its saved full-page scan check. The old queue assigns two letters to345; the corrected page boundary places the first at344 final line and the second at345 Ob(G). The final347 native crop resolves the same connected tail. Retain the already applied mathcal G forms. The exact mathematical relation to the category C is j:G→C assigning the degree filtration and Gr:C→G, with epsilon_B:B→Gr(jB) mapping each homogeneous b_n to its class and inverse taking that class to b_n, as printed in1.11. No categorical nonrelation is asserted.',
 'all sixteen actual occurrences enumerated above',verdict='confirmed for all listed occurrences; aggregate complete',
 change='Retain all sixteen occurrence-verified mathcal G forms.',witness=319)
for row in r.decisions:
 if row['source_id']=='check/findings/findings_306_310.json#14':
  row['image']='; '.join(f'scan/SGA6_scan_360dpi.pdf#page={x+14}; scan/SGA6_witness_300dpi.djvu#page={x+11}' for x in (308,309,310,311,313,344,345,347))
r.own_finding('ASTRA-V-UNDERLINE-347',p,
 'Definition6.2 underlines thirteen lexical word groups, including anneau de Chern; its mathematics,6.1 reference and the two hyphens following the displayed scalar/type symbols are plain.',
 'Use thirteen explicit uline groups in the inspected definition body, preserving its mathematical tokens.',
 'Restore the ruled definition statement without carrying a rule through the intervening math or hyphens.',
 'The main first strip and native358 top resolve each rule separately: Le foncteur defini en;sur la categorie des;algebres;graduees;a valeurs dans la categorie des;algebres;est appele;anneau de Chern;sa valeur pour;est notee;ou;s il;y a des risques de confusion. The surrounding prose and both6.2.1 formulas are unruled. The label word uses the accepted bold-label representation.',
 'complete Definition6.2 body',witness=358)
t=(HERE/'page_347_diplomatic.tex').read_text()
old=t.split(r'\textbf{Définition 6.2.} ',1)[1].split('\n\nDes formules',1)[0]
new=(r'\uline{Le foncteur défini en} 6.1 \uline{sur la catégorie des} \(K\)-\uline{algèbres} '
 r'\uline{graduées}, \uline{à valeurs dans la catégorie des} \(K\)-\(\lambda\)-\uline{algèbres}, '
 r'\uline{est appelé} \uline{anneau de Chern}; \uline{sa valeur pour} \(A\in\operatorname{Ob}(\mathcal G)\) '
 r'\uline{est notée} \(\Ch(A)\) (\uline{ou}, \uline{s\'il} \uline{y a des risques de confusion}, \(\Ch_K(A)\)).')
# The apostrophe above is literal prose, not a TeX accent control.
new=new.replace(r"s\'il","s'il")
r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-347','Preserve the thirteen directly observed word rules and all existing mathematical tokens.')
r.page(p,'Definition6.2','est un lambda-homomorphisme).',
 'Full main361 four strips and native358 top/lower compared. Checked the thirteen definition word rules, plain6.1 reference, one script G, Ch and Ch_K, all four references before the colon,6.2.1 pairs and its low product period, first-row absence of punctuation and second-row comma, lambda exponent i and bound i>=2, bibliography[1], all prose words and references3.9/3.10/6.7, both raised K dots, completion hat on A, and the final parenthesis/stop. No author note.',
 witness='Native358 top/lower: witness_347_top.png and witness_347_lower.png.')
r.commit()
