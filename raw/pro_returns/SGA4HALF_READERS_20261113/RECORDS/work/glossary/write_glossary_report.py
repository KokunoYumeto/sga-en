"""Write the reviewed glossary report from reproducible final-body counts."""
from pathlib import Path
import csv,json,re

B=Path(__file__).parent
status=json.loads((B/'STATUS.json').read_text())
multi=json.loads((B/'multiple_renderings.json').read_text())
patches=json.loads((B/'GLOSSARY_PATCHES.json').read_text())
policies={
 'application':'Retain the distinction between application of a result and a map or mapping. A matching page can contain both senses.',
 'base':'Retain base schemes and topological bases versus a basis of a vector space or module.',
 'caractéristique résiduelle':'Retain the conventional synonyms residual characteristic and residue characteristic.',
 'changement de base':'Retain noun versus attributive hyphenation; both denote base change.',
 'cohomologie à support propre':'Retain proper-support and compact-support terminology in the algebraic and comparison contexts. Compactly supported is an adjectival form of the latter.',
 'corps de nombres':'Retain singular and plural wording required by the sentence. The surface counts are not a one-to-one alignment of grammatical number.',
 'de plus':'Retain discourse alternatives; this is not a mathematical distinction.',
 'de présentation finie':'Retain adjective versus prepositional construction.',
 'entier':'Retain the noun integer and the adjective integral, including integrality of elements or rings.',
 'fermé':'Retain adjective versus explicitly named closed subset.',
 'fibre':'Retain British/American spelling already present in the supplied English.',
 'fibre géométrique':'Retain British/American spelling.',
 'fibre spéciale':'Retain British/American spelling.',
 'fibres':'Retain British/American spelling.',
 'flèche':'Retain arrow in categorical language and map when describing the associated mapping.',
 'flèche de spécialisation':'Retain specialization arrow and specialization map, the two source-attested descriptions of this construction.',
 'flèches':'Retain categorical arrows versus maps according to the surrounding description.',
 'foncteur':'Retain singular/plural English as the sentence requires. This broad page-level co-attestation does not establish that a singular French token was translated by a plural English token.',
 'foncteur dérivé cohomologique':'Retain the base phrase and its explicit right-hand qualification. The shorter phrase is also a substring of the longer; these are overlapping counts, not disjoint translation choices.',
 'homomorphisme':'Retain map where the homomorphism has already been specified; retain homomorphism where its algebraic structure is stated.',
 'image réciproque':'Retain ordinary versus attributive hyphenation.',
 'limite projective':'Retain inverse limit and projective limit, which both supplied reference traditions recognize.',
 'lisse':'Retain smooth for schemes and morphisms and the established English sheaf term lisse in the Rapport; see the five-context review above.',
 'lisses':'Retain smooth and lisse with the same scheme/sheaf qualification as lisse. English adjectives do not inflect for number.',
 'morphisme':'Retain morphism and its contextual abbreviation map.',
 "n'est pas":'Retain syntactic alternatives. The bare negation is not a competing technical term.',
 'nombre premier':'Retain the expanded prime number and the noun prime.',
 'ouvert':'Retain adjectival open and the explicit open subset or open subscheme appropriate to the object.',
 'partie':'Retain part in ordinary discourse and subset in set-theoretic statements.',
 'plongement':'Retain embedding and immersion according to the category and stated hypotheses; no global equivalence of all embedding notions is asserted.',
 'premier':'Retain the ordinal first and the distinct arithmetic adjective prime.',
 'relèvement':'Retain the conventional noun forms lift and lifting.',
 'sur':'Retain on and over according to grammatical and mathematical context.',
 'type fini':'Retain finite type for the geometric property and finitely generated when stating the corresponding algebraic condition.',
 'unité':'Retain identity for a group identity or identity transformation and unit in the relevant algebraic construction.',
 'variété':'Retain algebraic variety versus topological or differentiable manifold.',
 'voisinage':'Retain British/American spelling.',
 'voisinage étale':'Retain British/American spelling.',
 'à support propre':'Retain the same contextual proper/compact support terminology as the longer cohomology entry.',
 'étale':'Retain the unaccented etale in the original English lecture title quoted on p. 4; the surrounding translation uses étale. Do not silently respell an authorial title.'
}
assert not(set(multi)-set(policies)), 'A newly observed multiple rendering needs review: '+repr(set(multi)-set(policies))

def cell(s):return str(s).replace('|','\\|').replace('\n',' ')
out=['# English terminology: observed variation and decisions','',
 '## Scope and count definition','',
 f"The inventory reads all {status['pages']['fr']} French and {status['pages']['en']} English printed-page units (III–IV and 1–312) from the finalized annotated components. It selects the corrected side of every variant and applies the documented English terminology patch before counting. Restored authorial introductions, summaries, contents, and headings are included. Editorial front matter and apparatus are excluded. Local bibliography entries retain original publication titles and are excluded from prose-term counts; their translated headings are retained.",'',
 f"`GLOSSARY_SGA4HALF_FR_EN.tsv` contains {status['glossary_rows']} rows: {status['term_rows']} term/rendering rows for {status['unique_french_terms']} distinct normalized French expressions, plus {status['notation_rows']} unchanged named mathematical commands. There are {len(multi)} French expressions with more than one attested English rendering. The lexicon combines the supplied SGA 4 and SGA 7 pairs with reviewed definitions and technical vocabulary from SGA 4½.",'',
 'A term count is the number of exact English surface-form occurrences on an aligned printed page that also contains the French expression. Case is ignored; TeX accents and ordinary spaces are normalized. These are paired-page lexical attestations, following the counting convention documented in the supplied SGA 4 glossary. They are not independently established one-to-one translation-token counts. A page can contain several mathematical constructions or senses; nested terms and longer qualified expressions can overlap. The counts must therefore not be added as a total word count, nor used to infer that each French token received each listed English rendering. Singular and plural French expressions remain separate unless the supplied expression itself includes them. The table below preserves every observed multiple rendering in this inventory, including ordinary discourse entries inherited from the reference glossaries.','',
 '`GLOSSARY_ATTESTATIONS.tsv` records every counted English occurrence with its printed page and surrounding normalized text. `GLOSSARY_SOURCE_CENSUS.json` retains every French and English emphasis span, including long statements and expressions containing formulas. `GLOSSARY_CANDIDATES.tsv` gives the reviewed disposition of residual short emphasized expressions; they are not silently promoted to glossary equivalences. `unequal_emphasis_sequences.json` records the four unequal short-emphasis sequences and is discussed below.','',
 '## Editorial policy','',
 'The existing English is authoritative unless the source context establishes a plain slip. British/American spelling, grammatical number, noun/adjective constructions, and legitimate mathematical synonyms are retained. Thus fibre/fiber and neighbourhood/neighborhood remain, as do inverse/projective limit and the context-sensitive proper/compact support terminology. Capitalization at the start of a sentence or heading is not treated as a separate rendering. This follows the preservation policy in the supplied SGA 4 and SGA 7 inconsistency reports.','',
 '### Corrections applied to the English terminology','',
 '`S45-ASTRA-G-0001` replaces seven Arcata noun or heading occurrences of unwinding/unwindings with dévissage/dévissages. Both supplied reference glossaries retain dévissage (with the unaccented devissage variant in SGA 7); the restored Arcata contents and later exposés already use the technical term. The French and mathematical notation are unchanged. These are translation corrections in all three English forms, not misprints of the French print, so they receive English change-log rows and no print-variant apparatus entry.','',
 '| Printed page | Before | After | Finding |','|---|---|---|---|']
for r in patches:out.append('| '+ ' | '.join(cell(r[k]) for k in ['page','before','after','id'])+' |')
out += ['',
 'The heading is printed on p. 36 and was rechecked directly on that scan. The two verbal uses of unwound on p. 37 translate dévisser/dévisse in descriptions of successive reductions of a proper morphism and projective space. Their verbal explanation is retained; the noun replacement is deliberately not extended to those sentences.','',
 'Two further local terminology repairs are already in the Sommes component and its English change log: `S45-ASTRA-S-0070` changes conjugation class to conjugacy class on p. 181, matching the surrounding lemma and proof; `S45-ASTRA-S-0072` changes projective system to inverse system in the second of two parallel phrases on p. 199, where the same sentence had used both English names for parallel French occurrences of système projectif. The latter is a local consistency repair, not a claim that projective system is an incorrect mathematical term.','',
 '### Five retained uses of lisse','',
 'All five English occurrences are in the Rapport and concern adic sheaves. None describes a scheme or a morphism. The word is explicitly defined in terms of the locally constant finite-level sheaves, then used for the associated representation category and restrictions of constructible sheaves. Smooth remains the ordinary rendering for geometric objects, and is also used in some joint scheme/sheaf phrasing. The supplied reference glossaries favor smooth; they do not make the established English sheaf term lisse a semantic error.','',
 '| Printed page | Occurrence | Context and decision |','|---|---|---|',
 '| 82 | First | Definition: the adic sheaf is lisse when its finite-level sheaves are locally constant. Retain. |',
 '| 82 | Second | Comparison with the terminology of SGA 5, quoting the just-defined property. Retain. |',
 '| 83 | First | Equivalence between lisse adic sheaves and finite-type modules with continuous fundamental-group action. Retain. |',
 '| 83 | Second | A finite stratification on which the restrictions of a constructible adic sheaf are lisse. Retain. |',
 '| 88 | Only occurrence | Reduction to a smooth curve with a lisse sheaf. Retain the distinction in this sentence. |','',
 'The exact singular French entry lisse co-attests three of these occurrences; the plural lisses entry includes the two on p. 83 and overlaps the singular entry on p. 88, where both French forms occur. Thus their two glossary counts of three must not be added to infer six physical English occurrences. Locally constant is indexed under localement constant(s). It is not entered as an interchangeable rendering of lisse: such words often occur on the same page because a theorem has a smooth scheme and a locally constant sheaf, which does not establish a translation equivalence.','',
 f'## All {len(multi)} multiple renderings in the final glossary','',
 '| French expression | English renderings and counts | First witnesses, in the same order | Decision |','|---|---|---|---|']
for fr,rs in multi.items():
 out.append('| '+' | '.join(cell(x) for x in [fr,'; '.join(r['english_rendering']+' ('+str(r['count'])+')' for r in rs),'; '.join(r['first_place'] for r in rs),policies[fr]])+' |')
out += ['',
 '## Emphasis review and limitations of the inventory','',
 'The complete emphasis census is retained separately so that long statements, proper titles, formulas, and partial phrases do not have to be turned into artificial dictionary entries. The short residual expressions are all reviewed in `GLOSSARY_CANDIDATES.tsv`. A formula-dependent prefix such as an object followed by -torsor, -acyclic, or -flat is covered by the corresponding lexical term and by the mathematical notation inventory. Noun phrases prefixed by an article are indexed under their unprefixed term. Full sentences and proof headings are documented without being asserted to name a new concept.','',
 'The four unequal short-emphasis sequences require no speculative pairing: on p. 18 a bibliographic title has two emphasized French occurrences and one English occurrence; on p. 24 only the English emphasizes the same bibliographic title; on p. 38 the English emphasizes Lefschetz pencil, already indexed against pinceau de Lefschetz; on p. 230 the English adds three grammatical emphases in the discussion of the word “the.” These typography differences do not justify vocabulary replacements. The raw spans remain available in the census.','',
 'A missing row means that this lexicon and paired-page procedure did not establish an attested pair. It does not establish the absence of a word or concept from the volume. This restriction is especially relevant to formula-dependent wording and reordered long phrases. The glossary is a reproducible lexical inventory; the scan decisions and the separate bilingual mathematical review remain the authority for the text.','',
 '## Notation','',
 'Named mathematical commands are counted separately, with the same retained command on both sides. In particular, the Miller distinctions between sheaf and ordinary Hom, Ext, and derived Hom conventions are not silently homogenized. The notation decisions supplied for SGA 4 and SGA 7 were read as records of those editions; a volume-specific replacement is not imported into SGA 4½ without evidence from its own print. Such content decisions belong to the scan check and misprint register.','',
 '## Reproducibility and sources','',
 'Run `python3 work/glossary/build_glossary.py`, then `python3 work/glossary/write_glossary_report.py`, after the component builders. The first script reads the finalized French/English components, applies `apply_glossary.py` in memory, selects corrected variants, and writes the counts and occurrence evidence. The second checks that every multiple rendering and every residual short-emphasis candidate has an explicit reviewed policy before writing this report. `STATUS.json` records the input hashes and numerical totals. The assembly uses the same idempotent `apply_glossary(text, language, component)` function and records each actual replacement in `GLOSSARY_CHANGES_APPLIED.json`.','',
 'Source records: `en/glossaries/GLOSSARY_SGA4_FR_EN.tsv`, `en/glossaries/GLOSSARY_SGA4_INCONSISTENCIES.md`, `en/glossaries/GLOSSARY_SGA7_FR_EN.tsv`, `en/glossaries/GLOSSARY_SGA7_INCONSISTENCIES.md`, and the supplied notation-decision records. The text and page references are to Deligne, P. (1977), *Cohomologie étale* (SGA 4½; Lecture Notes in Mathematics 569), with the collaborators credited in the readers. All paths in the evidence are project- or source-relative.','']

candidate_policies={
 '-torseur':('covered','Formula-dependent prefix; torseur/torsor is indexed separately.'),
 'le groupe de Brauer':('covered','The leading article is not part of the term; groupe de Brauer/Brauer group is indexed.'),
 'Corps locaux':('title','Original publication title, retained in its original language.'),
 'Cohomologie galoisienne':('title','Original publication title, retained in its original language.'),
 'Preuve transcendante.':('heading','Proof heading, not a newly defined mathematical concept.'),
 '-faisceaux':('covered','Formula-dependent prefix; faisceau/sheaf and its plural are indexed separately.'),
 'On utilise les notations du , et ℓ est un nombre premier .':('sentence','Full statement with formula/reference slots; its mathematical terms are indexed separately.'),
 'définir':('discourse','Emphasis on the act of defining; not a technical noun.'),
 'Pour abréger, nous dirons projectif pour projectif de type fini':('sentence','An authorial abbreviation convention; projectif and type fini are indexed.'),
 'Noyau de':('covered','Heading with an omitted formula; noyau/kernel is indexed.'),
 'Surjectivité de':('covered','Heading with an omitted formula; surjectivité/surjectivity is indexed.'),
 'locales':('modifier','Ordinary inflected modifier; not a new term by itself.'),
 'localement acyclique en , rel.':('covered','Definition with point and sheaf formula slots; localement acyclique/locally acyclic is indexed.'),
 'localement acyclique, rel.':('covered','Definition with a relative coefficient formula slot; localement acyclique/locally acyclic is indexed.'),
 'universellement localement acyclique, rel.':('covered','Definition with a relative coefficient formula slot; the complete lexical term is indexed.'),
 'est gradué':('covered','Predicative form of gradué/graded, already indexed.'),
 'mais les isomorphismes ne sont pas, en général, uniquement déterminés':('sentence','Emphasized qualification in a mathematical statement, not a separate term.'),
 'objet libre à gauche sur':('covered','Definition with quotient-category formula slot; libre à gauche/free on the left is indexed.'),
 '-libre à gauche':('covered','Formula-dependent alternate placement of the free-on-the-left adjective; raw notation retained in the census.'),
 'objet libre à droite sur':('covered','Definition with quotient-category formula slot; libre à droite/free on the right is indexed.'),
 '-libre à droite':('covered','Formula-dependent alternate placement of the free-on-the-right adjective; raw notation retained in the census.'),
 'Ce foncteur est essentiellement surjectif.':('sentence','Full sentence; foncteur and essentiellement surjectif are separately indexed.'),
 '-ème hyper-ext':('covered','Ordinal formula slot; hyper-ext/hyper-Ext is separately indexed.'),
 '-acyclique':('covered','Formula-dependent prefix; acyclique/acyclic is indexed separately.'),
 '-plat':('covered','Formula-dependent prefix; plat/flat is indexed separately.')
}
candidates=json.loads((B/'emphasis_pairs_for_review.json').read_text())
for r in candidates:
 assert r['fr'] in candidate_policies, 'Unreviewed emphasis candidate: '+repr(r)
 r['status'],r['reason']=candidate_policies[r['fr']]
with (B/'GLOSSARY_CANDIDATES.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['page','fr','en','status','reason'],delimiter='\t');w.writeheader();w.writerows(candidates)
(B/'GLOSSARY_INCONSISTENCIES.md').write_text('\n'.join(out))
print(json.dumps(dict(report='GLOSSARY_INCONSISTENCIES.md',multiple_renderings=len(multi),reviewed_candidates=len(candidates),documented_glossary_changes=len(patches))))
