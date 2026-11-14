#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=316
r.finding('316_320',1,'The page begins with F^p∧^n(E)=∧^n(E), et si p<0,F^p∧^n(E)=0. Ceci définit… in running text.',
 'The complete main first strip and native top crop resolve the continuous sentence at the left margin. The315 half was directly inspected through its final comma. The attached closure on315 and running-text continuation on316 preserve exactly the printed formula tokens and punctuation; this is a scoped layout/TeX implementation decision.',
 '315/316 boundary and first sentence',verdict='scoped implementation confirmed; no content error',witness=327)
r.finding('316_320',2,'Dans le cas ou is printed without a grave accent.',
 'Both scans resolve the plain u. The construction is the relative phrase Dans le cas où followed by the stated local direct-summand condition. Preserve printed ou diplomatically and restore the accent in the corrected layer.',
 'paragraph before the equality in K',verdict='not applied and now applied',change={'diplomatic':'Dans le cas ou','current':'Dans le cas où'},witness=327)
r.patch(p,'current','Dans le cas ou','Dans le cas où','check/findings/findings_316_320.json#2','Restore the relative-adverb accent only in the corrected layer.')
r.finding('316_320',3,'The target pair of f is printed (T′,A!), with a tall tapering stroke and a separate low dot after A.',
 'The native lower crop and witness_316_Amark.png resolve a mark taller than the nearby primes and with a lower dot. The declared target immediately above is (T′,A′), and the displayed inverse-image map immediately below has source K_naif(T′,A′). The ringed-topos morphism therefore uses the same A′, with structure map f⁻¹A′→A and module pullback A⊗_{f⁻¹A′}f⁻¹E′. This explicit identification supports the corrected prime while the diplomatic layer retains the printed exclamation-shaped mark. The underline lies only under A.',
 'f:(T,A)→(T′,A!)',witness=327)
r.finding('316_320',4,'The316 list item begins with a short typed hyphen before Soit X un schéma.',
 'The native lower crop resolves the hyphen and its following space. The attached label=- agrees at this first item. The second listed item on317 is outside the current full-page scope and will be checked there.',
 'first special-case item on316',verdict='316 item confirmed;317 item separately scoped',witness=327)
r.finding('316_320',5,'A small grave-like tick rises above the e in c’èst; it is smaller and lighter than the ordinary accent in pré on the same line.',
 'The main tight crop main_316_cest.png and native witness_316_cest.png both retain the small upper mark. Its reduced size and slight contact with the letter are recorded physically; the scans do not document an erasure. Keep the attached diplomatic c’èst to preserve this visible mark. The corrected phrase c’est uses the pronoun c’ and verb est, leaving the sentence’s demonstrative reference unchanged.',
 'first special-case item, c’èst ce cas',verdict='visible source mark retained; paired lexical correction confirmed',witness=327)
r.finding('316_320',6,'All twenty-four specified letter rules on316 are present: eighteen E occurrences and six A occurrences; primes and the exclamation-shaped mark lie outside.',
 'Both scans were read occurrence by occurrence. The fourteen exterior-power arguments are underlined, as are E″ after sections données and all three letters in E′,E,E″. The six A letters in the three unprimed/three primed-or-exclamation topos pairs are underlined. The λ-class arguments and both tensor subscripts A remain plain. The320 portion of this multi-page finding will be separately checked on320.',
 'twenty-four inspected Module/ring letters on316',verdict='316 occurrences confirmed and applied;320 separately scoped',change='Apply exact local A/E rules on316.',witness=327)
id='check/findings/findings_316_320.json#6'
for old,new,count in [
 (r'\Lambda^n(E)',r'\Lambda^n(\underline{E})',10),
 (r"\Lambda^{n-p}(E')",r"\Lambda^{n-p}(\underline{E}')",1),
 (r"\Lambda^p(E'')",r"\Lambda^p(\underline{E}'')",1),
 (r"\Lambda^p(E')",r"\Lambda^p(\underline{E}')",1),
 (r"\Lambda^q(E'')",r"\Lambda^q(\underline{E}'')",1),
 (r"de \(E''\)",r"de \(\underline{E}''\)",1),
 (r"\(E',E,E''\)",r"\(\underline{E}',\underline{E},\underline{E}''\)",1),
 (r'(T,A)',r'(T,\underline{A})',3),
]:r.patch(p,'both',old,new,id,'Preserve the exact inspected letter rule and its plain neighbouring marks.',count=count)
r.patch(p,'diplomatic',r"(T',A')",r"(T',\underline{A}')",id,'Preserve the two diplomatic A-prime letter rules.',count=2)
r.patch(p,'current',r"(T',A')",r"(T',\underline{A}')",id,'Preserve all three corrected A-prime letter rules.',count=3)
r.patch(p,'diplomatic',r"(T',A!)",r"(T',\underline{A}!)",id,'Preserve the diplomatic A rule with the separate observed exclamation-shaped mark.')
r.own_finding('ASTRA-V-WEDGE-316',p,'All fourteen exterior-power signs on316 are small unadorned wedges, matching the eight inspected on315.',
 r'\wedge replaces the fourteen \Lambda commands on316.',
 'Restore the fourteen observed small wedge forms.',
 'The main first/middle strips and native top crop resolve each sign, from the first filtration sentence through the final class-of-graded equality. The wedge products of individual x sections already use the same small wedge glyph and remain unchanged. The notation identification sends each elementary exterior tensor to itself in the same alternating quotient; it changes no exterior degree or Module argument.',
 'all fourteen exterior-power operators',kind='symbol',witness=327)
r.patch(p,'both',r'\Lambda',r'\wedge','ASTRA-V-WEDGE-316','Preserve the fourteen inspected exterior-power glyphs.',count=14)
r.own_finding('ASTRA-V-ELLIPSES-316',p,'All four ellipsis groups in the defining formula for f_p are three baseline stops.',
 r'\ldots replaces the four \cdots commands in this formula.',
 'Restore the observed baseline ellipsis height.',
 'The native top crop resolves the two source-factor groups and two target-factor groups. They sit on the letter baseline, above the locally low-set wedge strokes, and each has three points. The ordered factors and their primed indices remain identical.',
 'en posant f_p formula',kind='symbol',witness=327)
r.patch(p,'both',r'\cdots',r'\ldots','ASTRA-V-ELLIPSES-316','Preserve the four inspected baseline three-dot groups.',count=4)
r.own_finding('ASTRA-V-PRODUCT-316',p,'The dot between λ^(n−p)(E′) and λ^p(E″) is a baseline stop.',
 r'\lambda^{n-p}(E\prime)\mathbin{.}\lambda^p(E\prime\prime) (with the original prime syntax retained).',
 'Restore the low multiplication dot in the equality in K.',
 'The native top crop places this dot at the baseline, matching the immediately following comma rather than the equality midline. It denotes the ring multiplication m_K:K×K→K, (a,b)↦ab, on the two displayed λ-classes. The exact operation, summation bounds0≤p≤n and plain class arguments are retained.',
 'last sum in the equality in K',kind='symbol',witness=327)
r.patch(p,'both',r"\lambda^{n-p}(E')\cdot\lambda^p(E'')",r"\lambda^{n-p}(E')\mathbin{.}\lambda^p(E'')",'ASTRA-V-PRODUCT-316','Preserve the inspected low multiplication dot.')
r.finding('311_315',31,'The eighteen315 letter rules and the316 continuation have now all been directly inspected; local A/E exceptions and prime boundaries are preserved.',
 'The315 replacements record its five A and thirteen E forms; checker316_320#6 records the independently inspected twenty-four316 forms. Both full pages have been compared in both scans. No replacement is extended to an uninspected use.',
 '315 specified occurrences and316 continuation',verdict='confirmed and applied at the inspected315/316 occurrences',change='Use the occurrence-specific315 patches and316 continuation patches.',witness=326)
r.finding('311_315',32,'There are eight small exterior wedges on315 and fourteen on316, all directly inspected.',
 'The complete two-page proof has now been compared in both scans. Every exterior-power sign has two sloping strokes without capital-Lambda serifs. The exact local patches preserve these22 signs and their unchanged exterior degrees/arguments; later uses in356–360 remain outside this decision.',
 'all22 exterior-power signs on315/316',verdict='confirmed and applied on315/316 only',change='Use the eight315 and fourteen316 wedge replacements.',witness=326)
for row in r.decisions:
 if row['source_id'] in ['check/findings/findings_311_315.json#31','check/findings/findings_311_315.json#32']:
  row['image']='scan/SGA6_scan_360dpi.pdf#page=329; scan/SGA6_witness_300dpi.djvu#page=326; scan/SGA6_scan_360dpi.pdf#page=330; scan/SGA6_witness_300dpi.djvu#page=327'
r.page(p,'F^p∧^n(E)=∧^n(E), et si p<0,F^p∧^n(E)=0.','pour la théorie générale des',
 'Complete filtration continuation, all14 exterior-power glyphs and24 A/E rules, full f_p formula including every prime and index, four baseline ellipses, headless local decomposition sign, direct-sum index p+q=n, both sums0…n and low class-product dot, all topos-pair forms and pullback stars, K raised dots and naif subscripts, relative ou, exclamation-shaped A mark, the small e accent, first list hyphen, and final page words compared. No author note.',
 witness='Native witness327 top/lower, A-mark and c’est crops, plus main tight c’est crop; witness_316_top.png, witness_316_lower.png, witness_316_Amark.png, witness_316_cest.png, main_316_cest.png')
r.commit()
