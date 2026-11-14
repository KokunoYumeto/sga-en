#!/usr/bin/env python3
from review_helpers import Review,read
r=Review();p=358
r.finding('356_360',8,'Folio358 starts ce q[blank]i montre que;the preceding equality display remains on357.',
 'Full main371/372 boundary strips and native368/369 show the display ending357 and the sentence beginning358. The attached marker is exact.',
 '357/358 boundary',witness=369)
r.finding('356_360',9,'The opening word is q[one blank cell]i,with no visible u.',
 'Main first strip and native369 top show one empty cell. The sentence concludes the already displayed composite identity u inverse composed with Gr(tilde-c)=Id;restoring qui supplies the missing relative-pronoun letter while leaving that exact map and equality untouched.',
 'opening ce q i',verdict='not applied and now applied',change='Current restores ce qui;diplomatic retains the explicit blank cell.',witness=369)
r.patch(p,'current',r'q\hphantom{u}i','qui','check/findings/findings_356_360.json#9','Restore the single visibly absent lexical letter.')
r.finding('356_360',10,'The opening identity label is Id with capital I and lowercase d,unruled.',
 'Native369 top resolves both plain upright letters. The attached Id control expands to operatorname{Id},as confirmed in the source macro declarations. It denotes the identity on Gr of the named augmented ring:the preceding map fixes each class of gamma^i(x),and these classes generate the associated graded algebra.',
 'opening composite identity',witness=369)
rules_reason=('Main four strips and native top/lower resolve every source rule endpoint.6.12 has eight groups:Si;est de caracteristique nulle;et;une;algebre;de filtration discrete;alors la classe de Chern completee;est un isomorphisme.6.13 has twelve:Soit;une;algebre graduee;et;une;algebre;augmentee;on appelle theorie de Chern de;a valeurs dans;tout;homomorphisme;compatible avec les augmentations.6.14 has nine:Le foncteur defini en;est representable;Si;est;de caracteristique nulle;et;de filtration discrete;il est represente;par le gradue associe a. Every mathematical letter,algebra-name wedge,prefix K-lambda or lambda,number and punctuation outside these spans is plain. The source line-break hyphen in homomorphisme introduces no lexical hyphen. The6.11 body on356 was directly checked and is unruled.')
r.finding('356_360',11,'The three statements have eight,twelve,and nine lexical rule groups respectively.',
 rules_reason,'6.12,6.13 and6.14 bodies',verdict='not applied and now applied',
 change='Restore the29 lexical groups,removing the old emph wrapper around the mathematical names.',witness=369)
r.finding('356_360',12,'Hom_lambda(wedge,Ch(A)) is inline at the next source line start,plain and followed by a full stop.',
 'Both scans show ordinary text line spacing and the final stop. The attached inline formula has the same mathematical tokens and punctuation. No further content correction follows from the former display layout.',
 'end of the functor-definition paragraph',verdict='formatting decision; tokens and punctuation confirmed',
 change='Retain the attached inline Hom formula and its final full stop.',witness=369)
close_reason=('Both scans show only one closing parenthesis in R_(k,a)(c^i(x),which closes the argument of c^i but leaves the outer R application open. The evaluated polynomial map is R_(k,a):the coefficient list(c^1(x),...,c^k(x))↦c^k(ax),as defined by the scalar-operation coefficient map6.1. Closing that outer application adds exactly the omitted delimiter without changing its inputs,the scalar a or its value. Retain the existing current close and the diplomatic omission.')
r.finding('356_360',13,'Relationiii has only one closing parenthesis after c^i(x).',
 close_reason,'scalar-operation polynomial relationiii',witness=369)
r.source('fixes/FIXLOG_6_CURRENT.jsonl#419','Missing outer R application close in relationiii.',close_reason,'relationiii',page=p,witness=369)
r.source('fixes/RECONCILE_CODEX_6.json#306','Missing outer R application close in relationiii.',close_reason,'relationiii',page=p,witness=369)
r.finding('356_360',14,'The last relation ends with a comma after the algebra-name wedge.',
 'The native lower crop resolves the descending comma tail,matching the earlier commas and longer than the full stops in the same relation reference. The attached comma agrees.',
 'relationiv final punctuation',witness=369)
r.own_finding('ASTRA-V-UNDERLINE-358',p,
 'The three statement bodies have29 lexical rule groups and plain mathematical names.',
 '29 explicit lexical uline groups.',
 'Restore the observed rules and remove mathematics from the inherited emph span.',
 rules_reason,'Corollary6.12,Definition6.13,Proposition6.14',witness=369)
for old,new in (
 (r'Si \(K\) est de caractéristique nulle, et \(\Lambda\) une \(K\)-\(\lambda\)-algèbre de filtration discrète, alors la classe de Chern complétée :',r'\uline{Si} \(K\) \uline{est de caractéristique nulle}, \uline{et} \(\Lambda\) \uline{une} \(K\)-\(\lambda\)-\uline{algèbre} \uline{de filtration discrète}, \uline{alors la classe de Chern complétée} :'),
 ('\nest un isomorphisme.\n','\n'+r'\uline{est un isomorphisme}.'+'\n'),
 (r'Soit \(A\) une \(K\)-algèbre graduée, et \(\Lambda\) une \(K\)-\(\lambda\)-algèbre augmentée~; on appelle \emph{théorie de Chern de \(\Lambda\) à valeurs dans \(A\)} tout \(\lambda\)-homomorphisme : \(\Lambda\longrightarrow \Ch(A)\), compatible avec les augmentations.',r'\uline{Soit} \(A\) \uline{une} \(K\)-\uline{algèbre graduée}, \uline{et} \(\Lambda\) \uline{une} \(K\)-\(\lambda\)-\uline{algèbre} \uline{augmentée}~; \uline{on appelle théorie de Chern de} \(\Lambda\) \uline{à valeurs dans} \(A\) \uline{tout} \(\lambda\)-\uline{homomorphisme} : \(\Lambda\longrightarrow \Ch(A)\), \uline{compatible avec les augmentations}.'),
 (r'Le foncteur défini en 6.13 est représentable. Si \(K\) est de caractéristique nulle, et \(\Lambda\) de filtration discrète, il est représenté par le gradué associé à \(\Lambda\).',r'\uline{Le foncteur défini en} 6.13 \uline{est représentable}. \uline{Si} \(K\) \uline{est} \uline{de caractéristique nulle}, \uline{et} \(\Lambda\) \uline{de filtration discrète}, \uline{il est représenté} \uline{par le gradué associé à} \(\Lambda\).')):
 r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-358','Preserve the exact lexical rule endpoints and plain mathematical tokens.')
wedge_reason=('All15 actual358 algebra-name signs are the same small unadorned wedges,individually checked in the statements,arrows,Hom expression,generator condition and each of the four relations. The ordinary-atom wedge is an occurrence-specific rendering of the named augmented ring. The map between this notation and the attached Lambda name is the identity on the underlying ring,its augmentation and its operations,and hence on the coefficient evaluation and Hom data.')
aggregate=next(x for x in read('decisions.jsonl') if x['source_id']=='check/findings/findings_356_360.json#2').copy()
aggregate.update(verdict='actual356–358 scope decided;359–360 pending',
 printed_reading='Ten actual356,seven actual357,and15 actual358 algebra-name signs are small serifless wedges.',
 change=r'Use the occurrence-scoped \mathord{\wedge} replacements on356–358 only;359–360 await direct comparison.',
 region='all actual356–358 algebra-name glyphs')
aggregate['reason']+=' '+wedge_reason
aggregate['image']+='; scan/SGA6_scan_360dpi.pdf#page=372; scan/SGA6_witness_300dpi.djvu#page=369'
r.decisions.append(aggregate)
r.own_finding('ASTRA-V-WEDGE-358',p,
 'All15 algebra-name signs are small unadorned wedges.',r'Use15 \mathord{\wedge} glyphs.',
 'Preserve each inspected ordinary-atom shape and unchanged named algebra.',
 wedge_reason,'all algebra-name occurrences',kind='symbol',witness=369)
r.patch(p,'both',r'\Lambda',r'\mathord{\wedge}','ASTRA-V-WEDGE-358','Preserve all15 local algebra-name glyphs.',count=15)
r.page(p,'ce q[blank]i montre que u inverse composed Gr(tilde-c)=Id.','relationiv:pour j,k>=1,x in Fil^1 wedge,',
 'Full main372 four strips and native369 top/lower compared. Checked the opening blank cell and capital Id,the exact357/358 marker,all29 lexical rule groups and their plain mathematical gaps,the arrow and Hom parentheses,all15 unadorned algebra-name wedges,generator indices and degree assignment,every k/i/j sum bound,P and Q double-primes,R scalar parameter a,missing source outer close and existing current repair,three semicolons and the final comma with its visible tail,every prose word and other punctuation. No author note.',
 witness='Native369 top/lower complete body;blank u cell,Id capitalization,29 rule groups,15 wedges,and all relation punctuation resolved.')
r.commit()
