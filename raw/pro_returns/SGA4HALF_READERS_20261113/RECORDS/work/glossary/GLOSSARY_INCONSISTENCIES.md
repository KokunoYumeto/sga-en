# English terminology: observed variation and decisions

## Scope and count definition

The inventory reads all 314 French and 314 English printed-page units (III–IV and 1–312) from the finalized annotated components. It selects the corrected side of every variant and applies the documented English terminology patch before counting. Restored authorial introductions, summaries, contents, and headings are included. Editorial front matter and apparatus are excluded. Local bibliography entries retain original publication titles and are excluded from prose-term counts; their translated headings are retained.

`GLOSSARY_SGA4HALF_FR_EN.tsv` contains 877 rows: 800 term/rendering rows for 757 distinct normalized French expressions, plus 77 unchanged named mathematical commands. There are 40 French expressions with more than one attested English rendering. The lexicon combines the supplied SGA 4 and SGA 7 pairs with reviewed definitions and technical vocabulary from SGA 4½.

A term count is the number of exact English surface-form occurrences on an aligned printed page that also contains the French expression. Case is ignored; TeX accents and ordinary spaces are normalized. These are paired-page lexical attestations, following the counting convention documented in the supplied SGA 4 glossary. They are not independently established one-to-one translation-token counts. A page can contain several mathematical constructions or senses; nested terms and longer qualified expressions can overlap. The counts must therefore not be added as a total word count, nor used to infer that each French token received each listed English rendering. Singular and plural French expressions remain separate unless the supplied expression itself includes them. The table below preserves every observed multiple rendering in this inventory, including ordinary discourse entries inherited from the reference glossaries.

`GLOSSARY_ATTESTATIONS.tsv` records every counted English occurrence with its printed page and surrounding normalized text. `GLOSSARY_SOURCE_CENSUS.json` retains every French and English emphasis span, including long statements and expressions containing formulas. `GLOSSARY_CANDIDATES.tsv` gives the reviewed disposition of residual short emphasized expressions; they are not silently promoted to glossary equivalences. `unequal_emphasis_sequences.json` records the four unequal short-emphasis sequences and is discussed below.

## Editorial policy

The existing English is authoritative unless the source context establishes a plain slip. British/American spelling, grammatical number, noun/adjective constructions, and legitimate mathematical synonyms are retained. Thus fibre/fiber and neighbourhood/neighborhood remain, as do inverse/projective limit and the context-sensitive proper/compact support terminology. Capitalization at the start of a sentence or heading is not treated as a separate rendering. This follows the preservation policy in the supplied SGA 4 and SGA 7 inconsistency reports.

### Corrections applied to the English terminology

`S45-ASTRA-G-0001` replaces seven Arcata noun or heading occurrences of unwinding/unwindings with dévissage/dévissages. Both supplied reference glossaries retain dévissage (with the unaccented devissage variant in SGA 7); the restored Arcata contents and later exposés already use the technical term. The French and mathematical notation are unchanged. These are translation corrections in all three English forms, not misprints of the French print, so they receive English change-log rows and no print-variant apparatus entry.

| Printed page | Before | After | Finding |
|---|---|---|---|
| 27 | unwindings | dévissages | S45-ASTRA-G-0001 |
| 27 | unwindings | dévissages | S45-ASTRA-G-0001 |
| 35 | unwinding | dévissage | S45-ASTRA-G-0001 |
| 36 | Unwindings | Dévissages | S45-ASTRA-G-0001 |
| 40 | unwinding | dévissage | S45-ASTRA-G-0001 |
| 51 | Unwindings | Dévissages | S45-ASTRA-G-0001 |
| 70 | unwinding | dévissage | S45-ASTRA-G-0001 |

The heading is printed on p. 36 and was rechecked directly on that scan. The two verbal uses of unwound on p. 37 translate dévisser/dévisse in descriptions of successive reductions of a proper morphism and projective space. Their verbal explanation is retained; the noun replacement is deliberately not extended to those sentences.

Two further local terminology repairs are already in the Sommes component and its English change log: `S45-ASTRA-S-0070` changes conjugation class to conjugacy class on p. 181, matching the surrounding lemma and proof; `S45-ASTRA-S-0072` changes projective system to inverse system in the second of two parallel phrases on p. 199, where the same sentence had used both English names for parallel French occurrences of système projectif. The latter is a local consistency repair, not a claim that projective system is an incorrect mathematical term.

### Five retained uses of lisse

All five English occurrences are in the Rapport and concern adic sheaves. None describes a scheme or a morphism. The word is explicitly defined in terms of the locally constant finite-level sheaves, then used for the associated representation category and restrictions of constructible sheaves. Smooth remains the ordinary rendering for geometric objects, and is also used in some joint scheme/sheaf phrasing. The supplied reference glossaries favor smooth; they do not make the established English sheaf term lisse a semantic error.

| Printed page | Occurrence | Context and decision |
|---|---|---|
| 82 | First | Definition: the adic sheaf is lisse when its finite-level sheaves are locally constant. Retain. |
| 82 | Second | Comparison with the terminology of SGA 5, quoting the just-defined property. Retain. |
| 83 | First | Equivalence between lisse adic sheaves and finite-type modules with continuous fundamental-group action. Retain. |
| 83 | Second | A finite stratification on which the restrictions of a constructible adic sheaf are lisse. Retain. |
| 88 | Only occurrence | Reduction to a smooth curve with a lisse sheaf. Retain the distinction in this sentence. |

The exact singular French entry lisse co-attests three of these occurrences; the plural lisses entry includes the two on p. 83 and overlaps the singular entry on p. 88, where both French forms occur. Thus their two glossary counts of three must not be added to infer six physical English occurrences. Locally constant is indexed under localement constant(s). It is not entered as an interchangeable rendering of lisse: such words often occur on the same page because a theorem has a smooth scheme and a locally constant sheaf, which does not establish a translation equivalence.

## All 40 multiple renderings in the final glossary

| French expression | English renderings and counts | First witnesses, in the same order | Decision |
|---|---|---|---|
| application | application (7); map (62); mapping (3) | Ariane; printed p. 2; Arcata; printed p. 18; Cycle; printed p. 135 | Retain the distinction between application of a result and a map or mapping. A matching page can contain both senses. |
| base | base (80); basis (9) | Ariane; printed p. 1; Arcata; printed p. 29 | Retain base schemes and topological bases versus a basis of a vector space or module. |
| caractéristique résiduelle | residual characteristic (1); residue characteristic (2) | Finitude; printed p. 247; Arcata; printed p. 59 | Retain the conventional synonyms residual characteristic and residue characteristic. |
| changement de base | Base change (57); base-change (9) | Ariane; printed p. 1; Rapport; printed p. 88 | Retain noun versus attributive hyphenation; both denote base change. |
| cohomologie à support propre | cohomology with compact support (1); cohomology with proper support (11); compactly supported cohomology (2) | Sommes trigonométriques; printed p. 184; Arcata; printed p. 5; Arcata; printed p. 66 | Retain proper-support and compact-support terminology in the algebraic and comparison contexts. Compactly supported is an adjectival form of the latter. |
| corps de nombres | number field (10); number fields (2) | Sommes trigonométriques; printed p. 177; Sommes trigonométriques; printed p. 211 | Retain singular and plural wording required by the sentence. The surface counts are not a one-to-one alignment of grammatical number. |
| de plus | also (13); In addition (15) | Ariane; printed p. 2; Arcata; printed p. 37 | Retain discourse alternatives; this is not a mathematical distinction. |
| de présentation finie | finitely presented (1); of finite presentation (6) | Rapport; printed p. 93; Arcata; printed p. 10 | Retain adjective versus prepositional construction. |
| entier | integer (40); integral (4) | Arcata; printed p. 21; Arcata; printed p. 24 | Retain the noun integer and the adjective integral, including integrality of elements or rings. |
| fermé | closed (63); closed subset (4) | Arcata; printed p. 9; Arcata; printed p. 37 | Retain adjective versus explicitly named closed subset. |
| fibre | fiber (33); fibre (35) | Rapport; printed p. 80; Arcata; printed p. 22 | Retain British/American spelling already present in the supplied English. |
| fibre géométrique | geometric fiber (2); geometric fibre (2) | Cycle; printed p. 146; Arcata; printed p. 60 | Retain British/American spelling. |
| fibre spéciale | special fiber (2); special fibre (6) | Dualité; printed p. 156; Arcata; printed p. 39 | Retain British/American spelling. |
| fibres | fibers (9); fibres (20) | Rapport; printed p. 84; Arcata; printed p. 5 | Retain British/American spelling. |
| flèche | arrow (35); map (6) | Rapport; printed p. 96; Arcata; printed p. 54 | Retain arrow in categorical language and map when describing the associated mapping. |
| flèche de spécialisation | specialization arrow (3); specialization map (3) | Finitude; printed p. 252; Arcata; printed p. 54 | Retain specialization arrow and specialization map, the two source-attested descriptions of this construction. |
| flèches | arrows (23); maps (9) | Rapport; printed p. 92; Arcata; printed p. 13 | Retain categorical arrows versus maps according to the surrounding description. |
| foncteur | functor (198); functors (50) | Arcata; printed p. 9; Arcata; printed p. 17 | Retain singular/plural English as the sentence requires. This broad page-level co-attestation does not establish that a singular French token was translated by a plural English token. |
| foncteur dérivé cohomologique | cohomological derived functor (7); right cohomological derived functor (4) | Catégories dérivées; printed p. 302; Catégories dérivées; printed p. 302 | Retain the base phrase and its explicit right-hand qualification. The shorter phrase is also a substring of the longer; these are overlapping counts, not disjoint translation choices. |
| homomorphisme | homomorphism (40); map (15) | Arcata; printed p. 13; Arcata; printed p. 28 | Retain map where the homomorphism has already been specified; retain homomorphism where its algebraic structure is stated. |
| image réciproque | inverse image (28); inverse-image (1) | Arcata; printed p. 23; Catégories dérivées; printed p. 311 | Retain ordinary versus attributive hyphenation. |
| limite projective | inverse limit (4); projective limit (4) | Rapport; printed p. 98; Arcata; printed p. 54 | Retain inverse limit and projective limit, which both supplied reference traditions recognize. |
| lisse | lisse (3); Smooth (101) | Rapport; printed p. 82; Arcata; printed p. 5 | Retain smooth for schemes and morphisms and the established English sheaf term lisse in the Rapport; see the five-context review above. |
| lisses | lisse (3); smooth (38) | Rapport; printed p. 83; Ariane; printed p. 1 | Retain smooth and lisse with the same scheme/sheaf qualification as lisse. English adjectives do not inflect for number. |
| morphisme | map (48); Morphism (250) | Arcata; printed p. 18; Ariane; printed p. 1 | Retain morphism and its contextual abbreviation map. |
| n'est pas | is not (14); not (22) | Arcata; printed p. 6; Arcata; printed p. 6 | Retain syntactic alternatives. The bare negation is not a competing technical term. |
| nombre premier | prime (11); prime number (6) | Arcata; printed p. 46; Rapport; printed p. 77 | Retain the expanded prime number and the noun prime. |
| ouvert | open (78); open subscheme (12); open subset (24) | Arcata; printed p. 6; Rapport; printed p. 100; Arcata; printed p. 6 | Retain adjectival open and the explicit open subset or open subscheme appropriate to the object. |
| partie | part (19); subset (9) | Ariane; printed p. 3; Arcata; printed p. 9 | Retain part in ordinary discourse and subset in set-theoretic statements. |
| plongement | embedding (5); immersion (13) | Sommes trigonométriques; printed p. 200; Arcata; printed p. 64 | Retain embedding and immersion according to the category and stated hypotheses; no global equivalence of all embedding notions is asserted. |
| premier | first (11); prime (36) | Introduction; printed p. III; Arcata; printed p. 18 | Retain the ordinal first and the distinct arithmetic adjective prime. |
| relèvement | lift (1); lifting (1) | Sommes trigonométriques; printed p. 216; Sommes trigonométriques; printed p. 216 | Retain the conventional noun forms lift and lifting. |
| sur | On (608); Over (307) | Introduction; printed p. III; Ariane; printed p. 2 | Retain on and over according to grammatical and mathematical context. |
| type fini | finite type (96); finitely generated (5) | Ariane; printed p. 2; Arcata; printed p. 10 | Retain finite type for the geometric property and finitely generated when stating the corresponding algebraic condition. |
| unité | identity (2); unit (1) | Rapport; printed p. 90; Sommes trigonométriques; printed p. 210 | Retain identity for a group identity or identity transformation and unit in the relevant algebraic construction. |
| variété | manifold (3); variety (13) | Arcata; printed p. 66; Arcata; printed p. 24 | Retain algebraic variety versus topological or differentiable manifold. |
| voisinage | neighborhood (4); neighbourhood (9) | Fonctions L; printed p. 121; Arcata; printed p. 18 | Retain British/American spelling. |
| voisinage étale | étale neighborhood (1); étale neighbourhood (2) | Finitude; printed p. 246; Arcata; printed p. 22 | Retain British/American spelling. |
| à support propre | with compact support (1); with proper support (15) | Sommes trigonométriques; printed p. 184; Arcata; printed p. 5 | Retain the same contextual proper/compact support terminology as the longer cohomology entry. |
| étale | etale (1); étale (129) | Arcata; printed p. 4; Ariane; printed p. 1 | Retain the unaccented etale in the original English lecture title quoted on p. 4; the surrounding translation uses étale. Do not silently respell an authorial title. |

## Emphasis review and limitations of the inventory

The complete emphasis census is retained separately so that long statements, proper titles, formulas, and partial phrases do not have to be turned into artificial dictionary entries. The short residual expressions are all reviewed in `GLOSSARY_CANDIDATES.tsv`. A formula-dependent prefix such as an object followed by -torsor, -acyclic, or -flat is covered by the corresponding lexical term and by the mathematical notation inventory. Noun phrases prefixed by an article are indexed under their unprefixed term. Full sentences and proof headings are documented without being asserted to name a new concept.

The four unequal short-emphasis sequences require no speculative pairing: on p. 18 a bibliographic title has two emphasized French occurrences and one English occurrence; on p. 24 only the English emphasizes the same bibliographic title; on p. 38 the English emphasizes Lefschetz pencil, already indexed against pinceau de Lefschetz; on p. 230 the English adds three grammatical emphases in the discussion of the word “the.” These typography differences do not justify vocabulary replacements. The raw spans remain available in the census.

A missing row means that this lexicon and paired-page procedure did not establish an attested pair. It does not establish the absence of a word or concept from the volume. This restriction is especially relevant to formula-dependent wording and reordered long phrases. The glossary is a reproducible lexical inventory; the scan decisions and the separate bilingual mathematical review remain the authority for the text.

## Notation

Named mathematical commands are counted separately, with the same retained command on both sides. In particular, the Miller distinctions between sheaf and ordinary Hom, Ext, and derived Hom conventions are not silently homogenized. The notation decisions supplied for SGA 4 and SGA 7 were read as records of those editions; a volume-specific replacement is not imported into SGA 4½ without evidence from its own print. Such content decisions belong to the scan check and misprint register.

## Reproducibility and sources

Run `python3 work/glossary/build_glossary.py`, then `python3 work/glossary/write_glossary_report.py`, after the component builders. The first script reads the finalized French/English components, applies `apply_glossary.py` in memory, selects corrected variants, and writes the counts and occurrence evidence. The second checks that every multiple rendering and every residual short-emphasis candidate has an explicit reviewed policy before writing this report. `STATUS.json` records the input hashes and numerical totals. The assembly uses the same idempotent `apply_glossary(text, language, component)` function and records each actual replacement in `GLOSSARY_CHANGES_APPLIED.json`.

Source records: `en/glossaries/GLOSSARY_SGA4_FR_EN.tsv`, `en/glossaries/GLOSSARY_SGA4_INCONSISTENCIES.md`, `en/glossaries/GLOSSARY_SGA7_FR_EN.tsv`, `en/glossaries/GLOSSARY_SGA7_INCONSISTENCIES.md`, and the supplied notation-decision records. The text and page references are to Deligne, P. (1977), *Cohomologie étale* (SGA 4½; Lecture Notes in Mathematics 569), with the collaborators credited in the readers. All paths in the evidence are project- or source-relative.
