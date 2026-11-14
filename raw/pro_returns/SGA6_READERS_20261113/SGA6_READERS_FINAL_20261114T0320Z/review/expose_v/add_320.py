#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=320
r.finding('316_320',22,'The page begins with the displayed Q₂,₂(X₁,X₂,X₃,X₄)=X₁X₃−X₄, followed by a full stop.',
 'The main first strip and native top crop show the full formula below the running header. The preceding319 page ends with the introducing colon. The attached marker now places the complete formula on320.',
 'page boundary319/320',witness=331)
r.finding('316_320',23,'The definition underlines eight lexical groups, with the λ signs, K, displayed map, connecting hyphens and final2.3 plain.',
 'The native lower crop resolves the endpoints of the rules: Un pré; anneau; sera appelé un; anneau si l’homomorphisme de groupes abéliens; est un; homomorphisme; pour la structure de pré; anneau sur le deuxième membre définie en. In particular the rules under the two pré groups end beneath the é, before the connecting hyphen; amend the proposal’s inclusion of those hyphens. The accepted bold-label convention covers Définition2.4.',
 'Définition2.4 statement',verdict='observed lexical rules applied with exact hyphen scope',change='Underline the eight explicitly observed lexical groups only.',witness=331)
old=r"Un pré-\(\lambda\)-anneau \(K\) sera appelé un \(\lambda\)-anneau si l'homomorphisme de groupes abéliens \(\lambda_t:K\longrightarrow1+K[[t]]^+\) est un \(\lambda\)-homomorphisme pour la structure de pré-\(\lambda\)-anneau sur le deuxième membre définie en 2.3."
new=r"\uline{Un pré}-\(\lambda\)-\uline{anneau} \(K\) \uline{sera appelé un} \(\lambda\)-\uline{anneau si l'homomorphisme de groupes abéliens} \(\lambda_t:K\longrightarrow1+K[[t]]^+\) \uline{est un} \(\lambda\)-\uline{homomorphisme} \uline{pour la structure de pré}-\(\lambda\)-\uline{anneau sur le deuxième membre définie en} 2.3."
r.patch(p,'both',old,new,'check/findings/findings_316_320.json#23','Restore the eight directly inspected lexical rules, with the two pré hyphens outside.')
r.finding('316_320',24,'Cela signifie donc qu’on a les relations begins a new indented paragraph.',
 'The native lower crop shows the paragraph separation and the following universal quantifier. The attached break agrees without any changed mathematical token.',
 'paragraph after Définition2.4',verdict='formatting observed; no content error',witness=331)
r.finding('316_320',25,'En termes des applications λ^i begins a new indented paragraph after2.4.1.',
 'The native lower crop directly shows its spacing and indentation. The attached paragraph break agrees; the full stop at the end of2.4.1 remains.',
 'paragraph after2.4.1',verdict='formatting observed; no content error',witness=331)
r.finding('316_320',26,'The separator in i.j is a baseline full stop, while the following N has a visibly doubled left vertical stroke.',
 'The native tight crop witness_320_ijN.png resolves the stop separately from the following j descender and the later comma. The preceding319 definition labels Q_{i,j} by the separately chosen operation index i and coefficient index j. Under successive coefficient extraction [u^i] and [t^j], the identity λ_u(λ_t(x))=Ĝ(λ_t)(λ_u(x)) gives λ^j(λ^i(x))=Q_{i,j}(λ¹(x),…,λ^{ij}(x)) for the pair (i,j)∈N×N. Thus a comma expresses the two independent indices in this exact displayed family; retain the stop diplomatically and restore the comma currently. Retain the inspected double-stem N in both layers.',
 'quantifier line before2.4.2',verdict='not applied and now applied',change={'diplomatic':r'i.j\in\mathbb N','current':r'i,j\in\mathbb N'},witness=331)
r.patch(p,'current',r'\(i.j\in\mathbb N\)',r'\(i,j\in\mathbb N\)','check/findings/findings_316_320.json#26','Restore the comma between the independently indexed i and j in the corrected layer.')
r.finding('316_320',27,'The first line of2.4.2 ends with the two closing parentheses after λ^i(y), with no following comma.',
 'Both lower scans resolve the terminal parentheses and the blank space after them. The attached deletion agrees.',
 'first line of2.4.2',witness=331)
r.finding('316_320',28,'The second line of2.4.2 ends with the two closing parentheses after λ^{ij}(x), with no following full stop.',
 'Both lower scans resolve the terminal parentheses and clear margin. The attached deletion agrees.',
 'second line of2.4.2',witness=331)
r.finding('316_320',29,'A single number2.4.2 lies at the left of the two relations; there is no2.4.3.',
 'The main final strip and native lower crop show the one shared number between the lines. The attached single tag plus notag preserves the number and both formulas; its vertical placement is an accepted layout choice.',
 'equation number beside the final two lines',witness=331)
r.finding('316_320',6,'The twenty-four letter rules on316 and all four E/F rules on320 are now individually checked; the surrounding primes, class arguments and A-Modules letters remain as separately observed.',
 'The316 occurrences are recorded in their exact local patches. On320 the two letters after pour tous A-Modules and the two letters in au cas où E et F have short individual rules. Every E/F inside the intervening λ-class display is plain, and both A letters in A-Modules are plain. The complete316 and320 images support this bounded decision without a global font substitution.',
 'twenty-four316 and four320 Module/ring letter rules',verdict='confirmed and applied at all inspected316/320 occurrences',change='Keep the316 local patches and apply the four320 letter rules under ASTRA-V-MODULE-RULES-320.',witness=327)
for row in r.decisions:
 if row['source_id']=='check/findings/findings_316_320.json#6':
  row['image']='scan/SGA6_scan_360dpi.pdf#page=330; scan/SGA6_witness_300dpi.djvu#page=327; scan/SGA6_scan_360dpi.pdf#page=334; scan/SGA6_witness_300dpi.djvu#page=331'
r.own_finding('ASTRA-V-MODULE-RULES-320',p,'Exactly four E/F letters in the two prose statements are underlined; all λ-class arguments and both A letters are plain.',
 r'\underline{E},\underline{F} after A-Modules; \underline{E} et \underline{F} in the invertibility clause.',
 'Restore the four directly inspected letter rules.',
 'The native top crop separates each short rule from its following comma or neighbouring word. These are the same two Modules used in the displayed λ-identities, whose plain class letters remain unchanged; no underline is extended into those class formulas.',
 'first paragraph’s Module names and subsequent invertibility clause',witness=331)
r.patch(p,'both',r'\(E,F\)',r'\(\underline{E},\underline{F}\)','ASTRA-V-MODULE-RULES-320','Preserve the first two inspected Module letter rules.')
r.patch(p,'both',r'\(E\) et \(F\)',r'\(\underline{E}\) et \(\underline{F}\)','ASTRA-V-MODULE-RULES-320','Preserve the second two inspected Module letter rules.')
r.page(p,'Q_{2,2}(X_1,X_2,X_3,X_4)=X_1X_3-X_4.','Q_{i,j}(λ¹(x),…,λ^{ij}(x))',
 'Entire opening Q polynomial and stop, every reference in the explanatory paragraphs, four independent Module rules and all plain class arguments, full λ_t/λ_u identities with superscript u on the first G, all semicolons, exact definition word rules and plain connecting hyphens, universal quantifier, complete2.4.1 with G lacking a superscript u as printed, period separator i.j and doubled-stem N, both complete2.4.2 relations with their indices and baseline ellipses, sole shared number, and absence of terminal punctuation compared. No author note.',
 witness='Native witness331 top/lower and tight i.j/N crops; witness_320_top.png, witness_320_lower.png and witness_320_ijN.png')
r.commit()
