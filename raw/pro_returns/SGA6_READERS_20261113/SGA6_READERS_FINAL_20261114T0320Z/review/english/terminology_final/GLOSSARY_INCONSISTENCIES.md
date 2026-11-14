# SGA 6: English terminology and observed alternatives

## Scope and counts

This packet compares the 269 reviewed prefix inventory rows and 316 rows from the ten sealed contribution inventories, the supplied SGA 4, SGA 4½, SGA 5 and SGA 7 lexicons, and 26 additional source-linked lexical entries. It pairs all 234 printed index rows: 129 terminology rows and 105 notation rows. Two ditto rows are explicitly resolved to their preceding headwords, each retaining both definition references.

The deduplicated glossary contains **1346 rows** for **1296 French headword keys**. There are **46 admitted French headwords with multiple English renderings** in this inventory and **111 cross-volume decision rows** (110 retained differences and one resolved prior deviation). Case and TeX-encoding aliases are listed within an entry; formula-bearing source labels retain their literal notation.

Each row states its own count scope. Lexical count means English surface-form occurrences on a leaf co-attesting the complete French search phrase; first_place is the first such leaf in print order. Exact index labels instead count paired index rows. Macro/token rows count literal command uses in their declared folios. These quantities are not added as word totals or asserted as one-to-one semantic translation frequencies.

TeX formatting wrappers and accents are projected in a separate search view; mathematical operands are excluded from prose except simple Greek term prefixes and lexical text labels. Comments, macro definitions and structural labels are excluded. Original author notes, contents, indexes, bibliographic matter and original advertisements are included when present on those leaves. Phrases crossing original leaf boundaries are not joined for lexical counting.

Every input row and every printed index row has a disposition. This is not an assertion that an arbitrary phrase-extraction procedure has found every possible technical term in the volume. A phrase omitted from the glossary is not asserted absent from the book.

The first mechanically co-attesting leaf is not claimed to be the first semantically aligned translation token. Reviewed passage loci and exact index definition references are separate columns. Formula-bounded interval counts provide an additional check, with their entire bilingual intervals retained in `GLOSSARY_ATTESTATIONS.json`; shared intervals can still contain several words or constructions. The exclusions below prevent those coincidences from becoming unsupported terminology decisions.

## English corrections

Two English-only corrections replace **generalization** by **generization** at XIII 648(a) and 649. The French word is *générisation*. The local point relation is `s ∈ closure{t}`; on a common affine neighbourhood the prime inclusion `p_t ⊆ p_s` gives the localization map `A_{p_s} → A_{p_t}`. SGA 4, 4½ and 7 use **generization** for this relation. Ordinary *généralisation* elsewhere retains **generalization**. The exact patches are `EN-TERM-GENERIZATION-648` and `EN-TERM-GENERIZATION-649`; both English source forms receive them, with identical mathematical units and no French source variant.

The English assembly owner has accepted those patches. This packet computes its English lexical counts after applying them virtually to the captured input. `VIRTUAL_PATCH_APPLICATION.json` records the source hashes and exact assertions; this script changes no shared edition source.

## Multiple English renderings retained

### \text{réd}

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| \mathrm{red} | 20 | Exposé IX, printed p.502 | SGA6-TERM-0148 |
| \text{red} | 1 | Exposé XII, printed p.597 | SGA6-TERM-0149 |

retain the scoped lexical reduction labels. The macro form and the literal text form both denote the same reduction. On Spec(A) the identity of A/√0 commutes with A -> A/√0; the identities glue under localization. Roman and text-style red remain exactly the locally adopted English forms, with separate command/label counts.

Source loci: 502;597;599.

### application

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| application | 5 | Exposé 0, printed p.20 | SGA6-TERM-0208 |
| map | 91 | Exposé 0, printed p.2 | SGA6-TERM-0209 |

retain contextual wording. Application at20 and63 names the use of Chern-class theory in studying injection morphisms. Map at2 names the tangent map of the same smooth morphism, and at29 names the displayed function. The latter sends each displayed argument to the same displayed value; the former is the stated use of a result. The source passages and their formulas remain unchanged.

Source loci: 20,63;2,29.

### base

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| base | 88 | original leaf IX | SGA6-TERM-0224 |
| basis | 66 | original leaf VIII | SGA6-TERM-0225 |

retain source constructions. For a basis (b_i) of a module M, the coordinate map R^(I) -> M sends e_i to b_i and has the inverse given by the stated coefficients. For the base S of X/S, the structural morphism is the given X -> S. The local words retain these specified data; no replacement of either map or any assertion about unrelated constructions is made.

Source loci: 25;297;365.

### changement de base

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| base change | 45 | Exposé II, printed p.171 | SGA6-TERM-0275 |
| base-change | 5 | Exposé III, printed p.224 | SGA6-TERM-0276 |

retain noun and attributive spelling. Base change and base-change qualify the same cartesian diagram. The comparison map and both projections are literally retained; the hyphen occurs before an English noun such as arrow. Its removal or insertion is not needed to identify any mathematical map.

Source loci: 171;224;416.

### complété

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| completed | 1 | Exposé II, printed p.218 | SGA6-TERM-0337 |
| completion | 2 | Exposé 0, printed p.33 | SGA6-TERM-0338 |

retain grammatical constructions. Completion names the inverse-limit object and completed qualifies that same construction in its local sentence. For a displayed filtration F^n A, the comparison with the completed object is a -> (a mod F^n A)_n; each quoted context retains its original filtration and transition maps.

Source loci: 33;218;401.

### composante neutre

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| identity component | 1 | Exposé XII, printed p.598 | SGA6-TERM-0343 |
| neutral component | 1 | Exposé X, printed p.537 | SGA6-TERM-0344 |

retain equivalent local group labels. Neutral component at537 is Pic^0_{X/k}; identity component at598 is the component of Ker(f_s^*) containing its identity. In each passage both English labels denote the connected component containing the given identity section. The identification is the identity on that component, preserving its inclusion in the same group and the group law. The reference glossaries use identity component; neutral component is retained with this explicit local identification.

Source loci: 537;598.

### conoyau

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| cokernel | 10 | Exposé I, printed p.115 | SGA6-TERM-0356 |
| cokernels | 2 | Exposé II, printed p.163 | SGA6-TERM-0357 |

retain collective plural. At163 the source stable par noyau, conoyau et extension is rendered stable under kernels, cokernels and extensions. For each displayed map u:M -> N, the cokernel is the same quotient N/im(u) and the same quotient homomorphism N -> N/im(u); the English plural refers to the collection of those quotients.

Source loci: 115;163.

### corps des fractions

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| Field of fractions | 1 | Exposé IX, printed p.502 | SGA6-TERM-0370 |
| fraction field | 4 | Exposé X, printed p.588 | SGA6-TERM-0371 |

retain equivalent field names. Fraction field and field of fractions refer to the localization of the same integral domain A at the nonzero elements of A. The comparison sends a/b to a/b; its identical inverse preserves addition, multiplication and A -> Frac(A). The terminology choice does not change the domain or a field extension.

Source loci: 502;588.

### de plus

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| also | 28 | Exposé 0, printed p.4 | SGA6-TERM-0416 |
| In addition | 13 | Exposé 0, printed p.7 | SGA6-TERM-0417 |

retain ordinary sentence wording. Also and in addition attach the additional assertion stated in the French sentence. They introduce no new object or mathematical map; all displayed assumptions and conclusions are retained.

Source loci: 4;7.

### de présentation finie

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| finitely presented | 1 | Exposé VII, printed p.443 | SGA6-TERM-0418 |
| of finite presentation | 86 | Exposé I, printed p.78 | SGA6-TERM-0419 |

retain adjective and noun phrase. The graded Module on443 is finitely presented, and the corresponding source says de présentation finie comme Module gradué. The same presentation by finitely many generators and relations is retained. Of finite presentation elsewhere leaves that same local presentation condition in noun-phrase form.

Source loci: 78;443.

### de type fini

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| finite-type | 1 | Exposé XIII, printed p.648 | SGA6-TERM-0424 |
| of finite type | 377 | Exposé 0, printed p.7 | SGA6-TERM-0425 |

retain grammatical placement. At648 the finite-type A-subalgebras B_alpha are the same subalgebras generated by finitely many elements; the transition inclusions B_alpha -> B_beta and colimit B remain literal. Of finite type is retained in the other sentence constructions.

Source loci: 7;648.

### facteur direct

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| direct factor | 10 | Exposé I, printed p.89 | SGA6-TERM-0536 |
| direct summand | 8 | Exposé V, printed p.315 | SGA6-TERM-0537 |

retain direct-factor and direct-summand wording. In the quoted module contexts, a splitting i:P -> F and r:F -> P with r i = 1 gives F ≃ P ⊕ ker(r) by (p,k) -> i(p)+k, with inverse f -> (r(f),f-i r(f)). This exact isomorphism identifies the direct factor and direct summand named in those passages; no local-freeness claim is added. The same local split exact sequence is retained at468.

Source loci: 89;109;315;468.

### fermé

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| closed | 97 | Exposé 0, printed p.3 | SGA6-TERM-0580 |
| closed subset | 13 | Exposé II, printed p.176 | SGA6-TERM-0581 |

retain adjective and subset noun. Closed qualifies the given immersion or subset. Closed subset makes the source noun un fermé explicit, retaining the same subset Z and inclusion Z -> X. No scheme structure is inserted by this lexical choice.

Source loci: 3;176.

### fibre

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| fiber | 22 | Exposé I, printed p.142 | SGA6-TERM-0584 |
| fibre | 7 | Exposé I, printed p.84 | SGA6-TERM-0585 |
| stalk | 3 | Exposé III, printed p.267 | SGA6-TERM-0586 |

retain stalk and fibre/fiber with exact local objects. On267 the source expressly calls O_{X,x} the anneau local fibre and separately forms P_x ⊗_{O_{X,x}} k(x); stalk names that stated local ring. On381–382 the stated stalk map is a localization, and the comparison bar(f)^* M -> tilde(M) is checked on those stalks. The stalk-to-residue-fibre map is m -> m⊗1. On84 and142 the category fibre has the same objects over S and arrows over 1_S; fibre and fiber identify these data by the identity functor. The orthographic variants are retained. No blanket replacement of stalk by geometric fibre is made.

Source loci: 84;142;267;381;382.

### fibres

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| fibers | 55 | Exposé I, printed p.157 | SGA6-TERM-0589 |
| fibres | 6 | Exposé 0, printed p.2 | SGA6-TERM-0590 |

retain spelling aliases. Fibres and fibers retain the same locally specified inverse-image spaces or category fibres. Their identity maps preserve the structural projections or the arrows over 1_S, respectively. The supplied SGA4½ and SGA7 reports retain both spellings.

Source loci: 2;157.

### flèche

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| arrow | 126 | Exposé 0, printed p.15 | SGA6-TERM-0624 |
| map | 3 | Exposé II, printed p.219 | SGA6-TERM-0625 |

retain arrow and the specified identity map. The genuine map alternative on568 is flèche identique: it is the identity q -> q of the same displayed object, so identity arrow and identity map have identical action and composition. Other page-level matches with morphism or plural arrows were rejected as unpaired co-occurrences.

Source loci: 15;568.

### flèches

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| arrows | 50 | Exposé 0, printed p.14 | SGA6-TERM-0629 |
| maps | 3 | Exposé V, printed p.362 | SGA6-TERM-0630 |

retain local map/arrow wording. At362 the source names the displayed functions as arrows of its diagrams. Calling them maps preserves their exact sources, targets and formulas. No change to those functions is proposed.

Source loci: 14;362.

### foncteur

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| functor | 305 | original leaf XII | SGA6-TERM-0631 |
| functors | 61 | Exposé 0, printed p.42 | SGA6-TERM-0632 |

retain attested singular and collective plural. The source homomorphisme de foncteur at385 is translated homomorphism of functors. Both displayed functors and the components beta_E of the same natural transformation are unchanged; for u:E -> F, the same naturality square is retained. This English plural identifies the two functors already displayed, without changing the transformation.

Source loci: 385.

### image directe

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| direct image | 9 | Exposé 0, printed p.1 | SGA6-TERM-0741 |
| direct-image | 7 | Exposé 0, printed p.6 | SGA6-TERM-0742 |

retain noun and attributive spelling. Direct image and direct-image functor name the same f_* in each local context. On381 it sends an O_Y-Module M to the same sheaf f_*M with the f_*O_Y-module structure. Hyphenation introduces no additional operation.

Source loci: 1;6;381.

### image inverse

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| inverse image | 24 | Exposé 0, printed p.41 | SGA6-TERM-0744 |
| inverse-image | 12 | Exposé I, printed p.84 | SGA6-TERM-0745 |
| pullback | 4 | Exposé XIII, printed p.632 | SGA6-TERM-0746 |

retain inverse image and pullback in their defined loci. On381 f^{-1} is expressly the sheaf-of-sets inverse image, and bar(f)^*M = f^{-1}M ⊗_{f^{-1}A} O_Y is the module inverse image. On632 pullback names L′ = g^*L′_alpha for the displayed base-change projection g:X_{Z′} -> X_{Z′_alpha}; the identity on g^{-1}L′_alpha ⊗_{g^{-1}O} O identifies the two labels there. The functor symbols, coefficient rings and base-change morphisms remain literal.

Source loci: 84;381;632.

### image réciproque

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| inverse image | 13 | Exposé 0, printed p.39 | SGA6-TERM-0747 |
| inverse-image | 2 | Exposé 0, printed p.72 | SGA6-TERM-0748 |

retain source inverse-image wording. For the bundle/sheaf construction on51, the same f^*E = f^{-1}E ⊗_{f^{-1}O_Y} O_X is used. Inverse image and attributive inverse-image preserve that exact object and action on arrows.

Source loci: 51;72.

### images directes

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| direct images | 1 | Exposé VII, printed p.443 | SGA6-TERM-0750 |
| direct-image | 1 | Exposé IV, printed p.287 | SGA6-TERM-0751 |

retain plural noun and attributive form. Direct images is the plural noun; direct-image qualifies the same named functor in the analytic projection formula on287. The exact Rf_* terms and the projection-formula arrow are unchanged.

Source loci: 287;443.

### intègre

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| an integral domain | 10 | Exposé 0, printed p.35 | SGA6-TERM-0773 |
| integral | 116 | Exposé 0, printed p.35 | SGA6-TERM-0774 |

retain local ring and scheme wording. An integral domain names the same ring A in the ring passages, with the identity A -> A. Integral qualifies the source scheme in the scheme passages, retaining its structure sheaf and structural morphism. No source ring or scheme is replaced, and the nested phrase integral in integral domain is counted as an explicitly overlapping lexical occurrence.

Source loci: 35;47;649.

### limite inductive

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| direct limit | 1 | Exposé XIV, printed p.686 | SGA6-TERM-0797 |
| inductive limit | 15 | Exposé II, printed p.163 | SGA6-TERM-0798 |

retain inductive/direct-limit names. For the fixed diagram (A_i,u_ij), the comparison from the object called inductive limit to that called direct limit is the unique map sending each canonical image j_i(a) to the same j_i(a). The reverse map has the same property; uniqueness of the colimit factorization makes their composites identities. On686 this applies to the stated system of Chow rings; its transition maps remain the given restriction maps.

Source loci: 163;686.

### limite projective

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| inverse limit | 1 | Exposé XIV, printed p.685 | SGA6-TERM-0800 |
| projective limit | 5 | Exposé II, printed p.218 | SGA6-TERM-0801 |

retain projective/inverse-limit names. For the stated restriction system A_K, both labels name compatible families (a_K) satisfying the same transition equalities. The comparison sends (a_K) to (a_K), with itself as inverse, and commutes with every projection. The source author claim about cohomology and this limit on685 is retained without adding an equality.

Source loci: 218;685.

### n'est pas

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| is not | 52 | Exposé 0, printed p.1 | SGA6-TERM-0881 |
| not | 89 | Exposé 0, printed p.1 | SGA6-TERM-0882 |

retain local negation syntax. Is not and the shorter not preserve the same negated predicate. The short word also occurs inside is not, so these lexical counts overlap and do not establish two translations of each source token.

Source loci: 1.

### nombre premier

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| prime | 8 | Exposé X, printed p.532 | SGA6-TERM-0892 |
| prime number | 3 | Exposé X, printed p.532 | SGA6-TERM-0893 |

retain full and abbreviated noun. Prime and prime number name the same integer p in the displayed binomial divisibility argument. The identification is p -> p in Z and leaves every divisibility statement unchanged. The shorter phrase also occurs inside prime number, so its lexical count overlaps that longer entry.

Source loci: 532.

### noyau

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| kernel | 54 | Exposé 0, printed p.4 | SGA6-TERM-0903 |
| kernels | 32 | Exposé I, printed p.86 | SGA6-TERM-0904 |

retain collective plural. Kernel and kernels name ker(u) for each same map u. Its inclusion ker(u) -> domain(u) is unchanged; the plural in stability assertions ranges over those maps.

Source loci: 86;163.

### nul

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| vanishing | 3 | Exposé V, printed p.301 | SGA6-TERM-0905 |
| zero | 54 | original leaf VIII | SGA6-TERM-0906 |

retain zero and vanishing syntax. Zero names the displayed zero element. Vanishing on/for states that the same specified function or graded component takes that zero value at the stated arguments. The function, arguments and zero map are retained, so no nonzero value or new bound is introduced.

Source loci: 23;301;452.

### ouvert

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| open | 196 | Exposé 0, printed p.7 | SGA6-TERM-0926 |
| open set | 6 | Exposé I, printed p.140 | SGA6-TERM-0927 |
| open subscheme | 3 | Exposé X, printed p.561 | SGA6-TERM-0928 |
| open subset | 87 | Exposé 0, printed p.46 | SGA6-TERM-0929 |

retain explicit local open-object names. Open subset and open set retain the same U ⊆ X with inclusion j:U -> X. Where the source scheme context supplies an open subscheme, its sheaf is O_X|_U and its morphism is that same open immersion j. Adjectival open leaves the local object specified by the rest of the sentence unchanged.

Source loci: 46;140;561.

### partie

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| part | 23 | original leaf IX | SGA6-TERM-0940 |
| subset | 30 | Exposé 0, printed p.38 | SGA6-TERM-0941 |

retain contextual noun. Part names the indicated portion of the exposition. Subset names the specified collection P of elements of the displayed set X, with its inclusion P -> X unchanged. The passage, rather than a page-wide word match, fixes the wording.

Source loci: IX;38.

### premier

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| first | 47 | original leaf VIII | SGA6-TERM-0985 |
| prime | 17 | Exposé 0, printed p.4 | SGA6-TERM-0986 |

retain ordinal and algebraic phrases. First retains the stated order of the exposition or sequence. Prime retains the specified prime number or prime ideal in the local formula. No integer, ideal, order relation or morphism is altered.

Source loci: VIII;4;532.

### produit fibré

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| fiber product | 2 | Exposé II, printed p.209 | SGA6-TERM-0996 |
| fibre product | 1 | Exposé VI, printed p.414 | SGA6-TERM-0997 |

retain spelling aliases. Fiber product and fibre product name the same X ×_S Y with the same two projections. The comparison is the unique map whose composites are those projections; the inverse satisfies the same property, so uniqueness makes the composites identities.

Source loci: 209;414.

### produit tensoriel

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| tensor product | 29 | Exposé 0, printed p.3 | SGA6-TERM-0998 |
| tensor-product | 1 | Exposé VII, printed p.433 | SGA6-TERM-0999 |

retain noun and attributive spelling. Tensor product and attributive tensor-product retain the exact coefficient ring and module factors. Their identification sends each pure tensor m⊗n to itself; the balanced relations are unchanged.

Source loci: 3;433.

### relèvement

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| lift | 1 | Exposé XII, printed p.606 | SGA6-TERM-1062 |
| lifting | 1 | Exposé II, printed p.163 | SGA6-TERM-1063 |

retain lift and lifting syntax. Lift names the stated arrow or object together with its projection, and lifting names its construction. In the fixed source diagram the same relation p∘l=u is retained; no different l or p is selected.

Source loci: 163;606.

### schéma des drapeaux

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| flag scheme | 5 | Exposé VI, printed p.390 | SGA6-TERM-1105 |
| scheme of flags | 4 | Exposé IX, printed p.510 | SGA6-TERM-1106 |

retain flag-scheme aliases. Flag scheme and scheme of flags represent the same explicitly specified flag functor: a test S-scheme T is sent to the chains in E_T with the prescribed locally free quotient ranks. The comparison sends each chain to itself; it is natural under pullback, has itself as inverse, and therefore induces the representing-scheme isomorphism preserving the universal flags.

Source loci: 390;510;515.

### semi-continuité

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| semi-continuity | 4 | Exposé III, printed p.259 | SGA6-TERM-1130 |
| semicontinuity | 2 | Exposé I, printed p.83 | SGA6-TERM-1131 |

retain hyphenation aliases. Semi-continuity and semicontinuity retain the same stated function, such as t -> h^0(F_{t,i}(-1)) on620. The sets defined by its inequalities and the topology on the base are identical. No upper/lower direction or semicontinuity theorem is changed.

Source loci: 83;273;586;620.

### sur

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| On | 994 | original leaf V | SGA6-TERM-1213 |
| Over | 548 | Exposé 0, printed p.1 | SGA6-TERM-1214 |

retain local preposition. On and over keep the object and structural relation explicitly stated in each sentence. Every named X -> S, sheaf on X, and arrow is unchanged; no mathematical identification is inferred from the preposition alone.

Source loci: 1;V.

### système projectif

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| inverse system | 3 | Exposé XIII, printed p.631 | SGA6-TERM-1227 |
| projective system | 4 | Exposé II, printed p.213 | SGA6-TERM-1228 |

retain inverse/projective-system names. Both names keep the same indexed objects and transition arrows u_ji:A_j -> A_i for i≤j. The comparison is the identity natural transformation on that exact diagram; its inverse is identical. The corresponding limit projections therefore agree.

Source loci: 213;631;638.

### topos

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| Topoi | 30 | original leaf VII | SGA6-TERM-1252 |
| Topos | 80 | original leaf VII | SGA6-TERM-1253 |

retain grammatical number. Topos and topoi retain the same specified category or listed categories. The plural is ordinary English number; no category, functor or topology is replaced.

Source loci: VII;83.

### type fini

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| finite type | 416 | Exposé 0, printed p.7 | SGA6-TERM-1284 |
| finitely generated | 1 | Exposé XIII, printed p.650 | SGA6-TERM-1285 |

retain the exact finite-generation formulation. On650 the Néron–Severi groups are finitely generated: for a stated finite generating family (g_i), the epimorphism Z^n -> G sends e_i to g_i. In module contexts the corresponding map is A^n -> M; in algebra contexts the defining map is A[T_1,...,T_n] -> B. Finite type and finitely generated retain the source category and this exact presentation map in each cited passage.

Source loci: 7;648;650.

### unité

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| identity | 4 | Exposé I, printed p.89 | SGA6-TERM-1292 |
| unit | 29 | Exposé 0, printed p.21 | SGA6-TERM-1293 |

retain unit/identity labels. The unit in a ring is the same element 1 satisfying 1a=a1=a. The identity matrix on557 is the same diagonal matrix with entries1 and off-diagonal entries0, acting identically on the stated module. The local labels preserve those elements and operations.

Source loci: 21;89;557.

### variété

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| manifold | 2 | Exposé II, printed p.177 | SGA6-TERM-1301 |
| variety | 48 | Exposé 0, printed p.25 | SGA6-TERM-1302 |

retain the source-specified local geometry. On177 manifold of class C^r retains the source C^r charts and their transition maps; the identity on the charted space preserves the sheaf of C^r functions used there. Algebraic variety on25 retains the same algebraic variety and structure sheaf. Mixed variety in II retains the explicit source definition; no general replacement of one local structure by another is made.

Source loci: 25;177;199.

### voisinage

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| neighborhood | 69 | Exposé II, printed p.205 | SGA6-TERM-1310 |
| neighbourhood | 21 | Exposé I, printed p.118 | SGA6-TERM-1311 |

retain spelling aliases. Neighborhood and neighbourhood retain the same open U containing the specified point or closed subset and the same inclusion U -> X. The reference volumes themselves retain both spellings; no open set is changed.

Source loci: 118;205.

### éclatement

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| blow-up | 1 | Exposé X, printed p.589 | SGA6-TERM-1315 |
| blowup | 1 | Exposé XIII, printed p.664 | SGA6-TERM-1316 |

retain blow-up spelling aliases. For the same ideal I, blow-up and blowup retain Proj(⊕_{n≥0} I^n) and its structural map to X. The identity on each graded piece I^n induces the identity of that Proj and preserves the exceptional ideal and projection.

Source loci: 589;664.

### éclaté

| English rendering | Count | First co-attesting place | Entry |
|---|---:|---|---|
| blow-up | 2 | Exposé 0, printed p.9 | SGA6-TERM-1317 |
| blown-up | 3 | original leaf XII | SGA6-TERM-1318 |

retain noun and participial phrase. Blow-up names the constructed scheme and blown-up qualifies scheme in the title. Both preserve the same Proj of the source Rees algebra and its structural morphism. No blow-up center is changed.

Source loci: 9;416;588.

## Source-scoped notation expansions

These choices are recorded by the English assembly owner in `EN_MACRO_EXPANSION_DECISIONS.json` and `EN_AGGREGATE_MACRO_TRANSPORTS.jsonl`. The glossary cites those records without duplicating their body patches.

| Source notation | English rendering | Uses in declared scope | Decision |
|---|---|---:|---|
| `\operatorname{Gl}` | `\operatorname{Gl}` | 13 | EN-AGG-MACRO-GL-393 |
| `\text{réd}` | `\mathrm{red}` | 20 | EN-AGG-MACRO-RED-502 |
| `\operatorname{long}` | `\operatorname{length}` | 2 | EN-AGG-MACRO-LENGTH-520 |
| `\mathbb Z_\ell` | `\mathbb Z_\ell` | 14 | EN-AGG-MACRO-ZELL_QELL-681 |
| `\mathbb Q_\ell` | `\mathbb Q_\ell` | 5 | EN-AGG-MACRO-ZELL_QELL-681 |
| `\text{naïf}` | `\text{naive}` | 4 | EN-AGG-MACRO-NAIF-698 |

The reduction count is20 literal `\red` invocations. Three literal `\mathrm{red}` labels on545 and one `\text{réd}` / `\text{red}` pair on597 are counted separately in `LITERAL_NOTATION_CHOICES.json`; the earlier metadata figure30 was an arithmetic error corrected by the English assembly owner. Both metadata snapshots and the clarification are retained.


Each exact identity proof and all counted folios are in `NOTATION_EXPANSION_CHOICES.json`. In particular, the naïf/naive identity sends every class [E] to [E] in each stated exact category and preserves every short-exact-sequence relation; the Gl/GL comparison fixes every invertible matrix. The red/réd identity fixes A/√0, and long/length fixes the same module and its composition-series quotients.

The seven SGA 4 notation records retain their original volume scopes in `REFERENCE_NOTATION_DECISIONS.json`. Their labels do not identify an SGA 6 occurrence to rewrite. The local SGA 6 source glyph decisions are preserved.

## Rejected candidate inferences and inventory qualifications

The full input-pair disposition is in `LEXICON_DISPOSITIONS.json`. Examples checked in their bilingual intervals include:

- **entier → integral:** on339 the integer n and an integral-domain assertion are separate French phrases.
- **homomorphisme → map:** on457,531,547 map translates application, while homomorphism is separately retained.
- **immersion → embedding:** on251 the two English words belong to separate source clauses.
- **flèche → morphism:** on360 the vertical arrow and the resulting morphism are separately named.
- **recouvrement → cover:** on169 cover translates the verb recouvrent; the noun recouvrement is covering.
- Singular/plural page coincidences such as faisceau/sheaves, fibre/fibres and trace/traces are excluded when the local plural translates a separate French plural. Genuine collective plurals, including stable under kernels/cokernels and homomorphism of functors, have explicit local decisions.
- Punctuation, Roman reference numerals and single-letter prose matches are not promoted to mathematical notation. Exact named TeX tokens, complete printed notation-index labels and the separately checked macro expansions have their own count scopes.

A number of provisional contribution headwords were lemma forms, condensed labels or phrases interrupted by a source qualifier. Their zero literal attestations are retained in the audit rather than assigned invented counts. Exact source plurals or fuller labels were added where inspected, including résolutions injectives, tores déployés, épimorphismes effectifs and complexe de Modules parfait. The candidate classe fondamentale at674 has no such literal source/English phrase there; the separately attested classe d’homologie fondamentale / fundamental homology class is indexed at15.

## Cross-volume choices

`CROSS_VOLUME_TERMS.tsv` lists every admitted headword whose rendering set differs from at least one supplied glossary for that exact headword, the source-scoped Gl/GL notation choice, and the resolved prior generalization/generization deviation. Every volume’s original rendering and row reference are retained. `CROSS_VOLUME_DECISIONS.tsv` is an identical audit alias. Grammatical inflection, ordinary synonyms and spelling alternatives are preserved when the local object, diagram or formula is unchanged, with the explicit maps given above. The two source-proved generization slips are corrected.

## Reproducibility

Run `make_terminology_patches.py`, `lexical_inventory.py`, `index_inventory.py`, and `finalize_glossary.py` in this directory after verifying the captured manifests. `prepare_inputs.py` creates the initial immutable input copy and refuses to overwrite it with changed shared inputs. All outputs are local to this review packet; shared edition sources, sealed contributions and their manifests remain unchanged.
