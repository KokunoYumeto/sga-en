#!/usr/bin/env python3
from review_helpers import Review,HERE
import json
r=Review();p=350
r.finding('346_350',17,'The first displayed expansion ends with three low dots and no additional stop.',
 'Main364 first strip and native361 top resolve exactly the three tail dots, followed by blank space. Retain the supplied absence of terminal punctuation.',
 'first display ending',witness=361)
r.finding('346_350',18,'The final Y_n factor has only two low tail dots; the Z_p and X_m tails each have three.',
 'Both scans resolve the three different tails. The current complete ellipsis denotes the same higher-degree terms of ch(psi); diplomatic retains the physical two-dot ending. The separate three constant-term errors are decided in ASTRA-V-CH-CONSTANTS-350.',
 'multiplicativity display, final factor',witness=361)
r.finding('346_350',19,'The first assertion prints i>=n, with a separate lower stroke below the sloping comparison sign.',
 'Native361 lower and the main third strip resolve the lower stroke, unlike the plain > at the statement end. In the universal symmetric-polynomial embedding X_i↦e_i(T1,...,Tn), the element becomes the sum of the n line elements L_j=(1,1+T_j). By6.2.1 and lambda-additivity, lambda_t(x)=product_(j=1)^n(1+L_j t), so coefficients vanish above n and the degree-n coefficient is product L_j=(1,1+sum T_j)=(1,1+a1). At n=1,lambda^1(L1)=L1 has scalar coordinate1 and is nonzero over K=Z, directly contradicting the printed endpoint. Retain current i>n, with no change of n or index.',
 'Proposition6.6.1(i)',witness=361)
r.finding('346_350',20,'There is no punctuation after the pair(1,1+a1) in assertion ii.',
 'Both main third strip and native361 lower show blank space after the closing parenthesis. The attached absence of a comma agrees.',
 'Proposition6.6.1(ii) ending',witness=361)
r.finding('346_350',21,'Assertion iii has no opening parenthesis before0, but a closing parenthesis after its ellipsis.',
 'The main/native images resolve the unmatched close. The sum of the lambda terms is an element of K×I(A); in the displayed positive-degree case its scalar coordinate is the alternating binomial sum0, and the second coordinate starts1-(n-1)!a_n. The existing current opening parenthesis gives exactly this ordered pair. The coefficient follows from ch(product_j(1-L_j))=product_j(1-exp T_j), whose degree-n part is(-1)^n product T_j; dividing by c_n=(-1)^(n-1)/(n-1)! yields-(n-1)!a_n.',
 'Proposition6.6.1(iii), ordered pair',witness=361)
r.finding('346_350',22,'Folio350 ends dans le cas;351 begins ou A est l anneau.',
 'The complete350 lower image and the directly viewed351 first strip establish the exact boundary. The attached marker agrees. The351 regional look does not mark that next page fully checked.',
 '350/351 boundary',witness=361)
r.own_finding('ASTRA-V-CH-CONSTANTS-350',p,
 'The multiplicativity display literally starts each of its three coefficient series with1+.',
 'Current removes the three1+ prefixes; diplomatic retains all three.',
 'Restore the zero constant term of each augmentation-ideal Chern character.',
 'Main second strip and native361 top confirm all three prefixes. On348, ch(phi)=eta(Log phi), with eta scaling homogeneous degree r by c_r=(-1)^(r-1)/(r-1)!, so ch(phi) has constant0. On349, the extension is ch(a,phi)=a+eta(Log phi), and the degree-n filtration for n>=1 has first coordinate0. Therefore the exact identity ch(phi*psi)=ch(phi)ch(psi) expands as c_pZ_p+...=(c_mX_m+...)(c_nY_n+...). In K=Z,A=Z[X,Y], wtX=wtY=1, phi=1+X,psi=1+Y,6.1.1 gives phi*psi=1-XY+higher, so the printed left side has degree-one component0 while the printed right side has X+Y. The exact comparison with unit pairs and the preceding source definitions is recorded in identification_350.json.',
 'three leading constants in the multiplicativity display',kind='misprint_in_print',witness=361)
r.patch(p,'current',r'1+\frac{(-1)^',r'\frac{(-1)^','ASTRA-V-CH-CONSTANTS-350','Remove precisely the three extra unit terms from the augmentation-ideal character equality.',count=3)
r.own_finding('ASTRA-V-CH-MODULUS-350',p,
 'The opening congruence has modulus completed A^(>=n+1), without a rational scalar-extension subscript.',
 r'Current \widehat A_{\mathbb Q}^{\ge n+1}; diplomatic \widehat A^{\ge n+1}.',
 'Restore the actual target filtration of the character defined on348.',
 'Both scans clearly omit Q at this occurrence. The map ch is valued in the degree completion of A_Q=A tensor_ZQ, and eta scales degree r by the rational c_r. For K=Z,A=Z[Y] with wtY=3,n=1,phi=1+Y,a1=0, the degree-three component of ch(phi)-ch(1+a1) is Y/2. The coefficient map [Y]:completed Q[Y]→Q sends the integral completed subgroup to Z and this difference to1/2, so it is not in completed A^(>=2). It is in the rational completed degree>=2 subgroup, exactly the target filtration of ch. The packet records the scalar-extension and homogeneous projection maps.',
 'opening congruence, modulus',kind='misprint_in_print',witness=361)
r.patch(p,'current',r'\mathrm{mod.}\ \widehat A^{\ge n+1}',r'\mathrm{mod.}\ \widehat A_{\mathbb Q}^{\ge n+1}','ASTRA-V-CH-MODULUS-350','Restore the exact rational completed filtration target of ch.')
r.own_finding('ASTRA-V-UNDERLINE-350',p,
 'Proposition6.6.1 has six lexical rule groups:Soit;un element de la forme;Alors;pour;les termes non ecrits;etant de degre.',
 'Use six explicit uline groups, including pour inside its display text.',
 'Restore the inspected word rules, retaining all mathematics independently.',
 'Main third/fourth strips and native361 lower show each rule. Item labels, formulas, comparison signs and n remain plain; the proof continuation and6.6 prose are plain.',
 'Proposition6.6.1 statement',witness=361)
for old,new in (
 (r'\textbf{Proposition 6.6.1.} Soit',r'\textbf{Proposition 6.6.1.} \uline{Soit}'),
 ('un élément de la forme',r'\uline{un élément de la forme}'),
 ('Alors :',r'\uline{Alors} :'),
 (r'\text{pour }',r'\text{\uline{pour} }'),
 ('les termes non écrits',r'\uline{les termes non écrits}'),
 ('étant de degré',r'\uline{étant de degré}')):
 r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-350','Preserve this directly observed lexical rule.')
r.own_finding('ASTRA-V-FORMS-350',p,
 'The6.6 paragraph number is ordinary type; the polynomial index N has a reinforced left stem and the tensor coefficient Q has an inner stroke. All complete series ellipses are low.',
 r'Use plain6.6., retain \mathbb N and \mathbb Q, and use \ldots for six diplomatic/seven corrected complete ellipses.',
 'Preserve the occurrence-specific paragraph, number-letter and ellipsis forms.',
 'The native N tight crop and nearest-neighbour zoom resolve the additional left stroke; native top resolves the inner Q stroke. Main/native complete views resolve every ellipsis, including the separately paired two-dot final factor. The existing three product periods in the middle display are already low.',
 '6.6 label, universal ring and all complete ellipses',kind='convention',witness=361)
r.patch(p,'both',r'\textbf{6.6.}',r'6.6.','ASTRA-V-FORMS-350','Preserve the ordinary numbered paragraph.')
r.patch(p,'diplomatic',r'\cdots',r'\ldots','ASTRA-V-FORMS-350','Preserve six complete low diplomatic ellipses.',count=6)
r.patch(p,'current',r'\cdots',r'\ldots','ASTRA-V-FORMS-350','Preserve seven complete low corrected ellipses.',count=7)
packet={
 'record_type':'exact_identification','page':p,
 'source_ids':['ASTRA-V-CH-CONSTANTS-350','ASTRA-V-CH-MODULUS-350'],
 'image':['scan/SGA6_scan_360dpi.pdf#page=364','scan/SGA6_witness_300dpi.djvu#page=361'],
 'preceding_source_definitions':{
  '348_6.3.1':'The natural group homomorphism ch:I(A)=1+completed A^+→completed A_Q^+ is determined on the universal weight-one element by ch(1+X)=exp(X)-1.',
  '348_eta':'eta(sum_(r>=1)a_r t^r)=sum_(r>=1)((-1)^(r-1)/(r-1)!) a_r t^r; t records homogeneous degree.',
  '348_6.3.2':'ch(phi)=eta(Log phi). Log(phi) and eta(Log phi) both have constant0.',
  '345_unit_and_rank':'Ch(A)=K×I(A), with additive zero(0,1), multiplicative unit(1,1), augmentation/rank pi(a,phi)=a, ideal inclusion i(phi)=(0,phi), and scalar inclusion j(a)=(a,1).',
  '345_multiplication':'(a,phi)(b,psi)=(ab,phi^b psi^a(phi*psi)). In particular i(phi)i(psi)=i(phi*psi), while(1,phi)(1,psi)=(1,phi psi(phi*psi)).',
  '349_6.3.3':'The extended character is ch(a,phi)=a+eta(Log phi). Thus ch(i(phi))=eta(Log phi), whereas ch(1,phi)=1+eta(Log phi).',
  '349_6.5.1':'For n>=1 the degree-n subgroup is the image u↦(0,1+u), with u in product_(r>=n)A^r. The phi/psi of6.5(i),(ii) are in this rank-zero ideal.'},
 'three_constants':{
  'printed':'1+c_p Z_p+...=(1+c_m X_m+...)(1+c_n Y_n+...), with the final diplomatic tail printed as two dots.',
  'corrected':'c_p Z_p+...=(c_m X_m+...)(c_n Y_n+...), c_r=(-1)^(r-1)/(r-1)!; only the three1+ prefixes are removed by this decision.',
  'map':'Apply the same ring homomorphism ch to i(phi)i(psi)=i(phi*psi). Every resulting series has scalar/constant0; this directly gives the corrected equality.',
  'unit_comparison':'Applying ch to the rank-one pairs instead would give(1+ch(phi))(1+ch(psi))=1+ch(phi)+ch(psi)+ch(phi*psi), using their exact product(1,phi psi(phi*psi)). Hence the three printed prefixes cannot be justified by changing the rank convention alone.',
  'counterexample':'K=Z,A=Z[X,Y],wtX=wtY=1,m=n=1,phi=1+X,psi=1+Y. Formula6.1.1 gives phi*psi=(1+X+Y)/((1+X)(1+Y))=1-XY+terms of degree>=3. The printed left side has degree-one coefficient0, while its right side has X+Y. Under [X]:Q[[X,Y]]→Q these coefficients are0 and1.',
  'leading_coefficient':'The corrected identity gives p=m+n and c_(m+n) Z_(m+n)=c_m c_n X_mY_n, hence Z_(m+n)=-(m+n-1)!/((m-1)!(n-1)!) X_mY_n, exactly6.5.3. Torsion-free universal coefficients embed into their rational extension; equality then descends and specializes by the independent-coefficient evaluation map.'},
 'rational_modulus':{
  'printed':'ch(phi) congruent ch(1+a_n) mod completed A^(>=n+1).',
  'corrected':'The modulus is completed A_Q^(>=n+1).',
  'scalar_extension':'iota_r:A^r→A^r tensor_ZQ sends a↦a tensor1; its product over r>=n+1 maps the integral degree tail into the rational degree tail.',
  'filtration_map':'Log(phi)-Log(1+a_n) has no homogeneous components through n. Applying eta preserves each degree and multiplies it by c_r in Q, so its image lies in product_(r>=n+1)(A^r tensor_ZQ).',
  'counterexample':'K=Z,A=Z[Y],wtY=3,n=1,phi=1+Y,a1=0. The degree-three component is eta(Y)=Y/2. The coordinate projection coefficient_Y sends the image of the integral completion to Z, but sends this difference to1/2. Thus the printed integral modulus fails, while the corrected rational degree>=2 modulus holds.',
  'scope':'Only the opening modulus gains Q; all degree bounds and the printed character map remain unchanged.'},
 'disposition':'Diplomatic retains both source readings. Current makes the exact three constant removals and one rational-target restoration; no new statement or hypothesis is introduced.'
}
(HERE/'identification_350.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
r.page(p,'donc ch(phi) congruent ch(1+a_n)','dans le cas',
 'Full main364 four strips and native361 top/lower compared. Checked the initial integral modulus and omitted rational subscript, first display with no extra stop, all sum bounds, reinforced N/Q with tight native N view, three erroneous1+ prefixes and mixed two/three-dot endings, all products/factorials, ordinary6.6 and its wavy projection arrow, six proposition word rules, literal i>=n versus final >n, ii lack of punctuation, iii sum from0 to n and missing opening pair parenthesis, and exact350/351 boundary. No author note.',
 witness='Native361 top/lower; witness_350_N.png and nearest-neighbour zoom. Main351 first strip consulted only for boundary/proof setup.')
r.commit()
