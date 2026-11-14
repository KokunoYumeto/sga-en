#!/usr/bin/env python3
"""Attribute the completed convention decisions without editing frozen inputs."""
from pathlib import Path
import csv, hashlib, json, re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'review/global_conventions'

def sha(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()

def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

evidence = {}

def attribute(ref):
    if ref in evidence:
        return ref
    path, sep, suffix = ref.rpartition('#')
    if sep and suffix.isdigit() and path.endswith('.jsonl'):
        line = (ROOT / path).read_text().splitlines()[int(suffix)-1]
        evidence[ref] = {'record_sha256': sha(line), 'record': json.loads(line)}
    else:
        p = ROOT / ref
        data = p.read_bytes()
        evidence[ref] = {'file_sha256': sha(data)}
        if p.suffix == '.json':
            evidence[ref]['record'] = json.loads(data)
    return ref

def row(key, scope, reading, disposition, reason, refs, change='Retain the completed occurrence-specific repairs; no new mathematical patch.'):
    return {
        'source_id': key, 'record_type': 'convention', 'scope': scope,
        'verdict': disposition, 'printed_reading': reading, 'change': change,
        'forms': 'French diplomatic and corrected; mapped English typography with the same distinctions.',
        'reason': reason, 'evidence_refs': [attribute(x) for x in refs],
        'evidence_mode': 'Explicit attribution to completed direct source observations; fresh bounded views are separately listed.',
        'new_full_page_certification': False,
    }

rows = [
 row('conventions/GLOBAL_ISSUES_SGA.md#76', 'Volume; occurrence-specific dots and page boundaries',
     'Exact source page openings; raised typed Gr dots; accepted quote, joint-name and epsilon glyph transports.',
     'closed by the completed page decisions and NOTE_6 accepted transports',
     'The old OCR relocation count146 describes an earlier operation. The final page-boundary records, including the individually located690 break, govern the actual markers. The exact marker/prose comparison preserves the ordered author text; it does not repeat the OCR pass. NOTE_6 expressly accepts guillemets, joint-name en dashes, and epsilon/varepsilon renderings of the typed epsilon. Its accepted glyph transport also covers the ordinary Q used for the same bound rational coefficient field: the field identification fixes every rational number and its operations. The reviewed local rules on Q, such as the individually underlined coefficient on XIV669, remain visible. Raised Gr marks stay superscripts; the lower dots in XIV complexes and the completion placeholders of V retain their independently read positions. No volume-wide replacement of dots, primes or coefficient letters is applied.',
     ['conventions/NOTE_6.txt', 'review/late/decisions.jsonl#242', 'review/late/decisions.jsonl#258',
      'review/global_closure/evidence/group_29.json', 'review/late/own_findings.jsonl#73', 'review/late/HANDOFF.md']),
 row('conventions/GLOBAL_ISSUES_SGA.md#81', 'I category/site letters; all ordinary item and paragraph labels',
     'Underlined typed category C in the inspected I occurrences; ordinary item letters and standalone paragraph numbers.',
     'closed; existing category/item repairs retained and remaining paragraph wrappers supplied in the final pass',
     'I96–100 directly establishes a single rule under the category C, with primes and indices outside. The site symbol has its own independent rule; the object S in a fibre subscript remains as observed. In I89 the current category/site repairs refer to exactly the already bound category and site: the identification fixes each object, morphism and fibre, while the diplomatic branch retains the locally plain letters. The composed body has no remaining pure bold item-letter wrappers. Of78 pure numeric bold groups,77 are ordinary paragraph labels and receive exact local wrapper removal. The2.2. group on205 belongs to a Proposition label separated by an original note and retains NOTE_6 accepted statement-label styling. The source605 label3.2 is an ordinary paragraph label beside a display, confirmed by the new bounded view; only its text wrapper changes.',
     ['review/expose_i/own_findings.jsonl#21', 'review/expose_i/own_findings.jsonl#25',
      'review/expose_i/own_findings.jsonl#43', 'review/expose_i/own_findings.jsonl#44',
      'review/expose_i/own_findings.jsonl#45', 'review/expose_i/own_findings.jsonl#46',
      'review/expose_i/own_findings.jsonl#47', 'review/global_conventions/bold_item_paragraph_inventory.json',
      'review/global_conventions/fresh_region_evidence.json'],
     'Apply only the77 exact numeric-wrapper repairs per branch in post_review_patches.jsonl; preserve statement labels.'),
 row('conventions/GLOBAL_ISSUES_SGA.md#82', 'II160–221; especially163,167,173–175',
     'Statement word rules, plain defining descriptions, and22 individually underlined category L letters on173–175.',
     'closed by the completed II local applications',
     'The recorded source groups on163 exclude the defined descriptions quasi-compact and engendré par ses sections. The167 proposition groups and the173 lemma groups already have explicit uline wrappers. Category L counts are6 on173,12 on174 and4 on175; the generating invertible sheaves L_i remain plain. Each category-letter transport fixes the same objects and maps of L(S), L(U), or the explicitly named subcategory; it does not replace the separate sheaf generators. The composed II body has0 emph groups and770 uline commands. This count verifies that the deferred II implementation is already present; no duplicate wrappers are added by the final pass.',
     ['review/expose_ii/own_findings.jsonl#15', 'review/expose_ii/own_findings.jsonl#26',
      'review/expose_ii/decisions.jsonl#168', 'review/expose_ii/own_findings.jsonl#40',
      'review/expose_ii/own_findings.jsonl#41', 'review/expose_ii/own_findings.jsonl#46',
      'review/global_conventions/typography_counts.json']),
 row('conventions/GLOBAL_ISSUES_SGA.md#84', 'III222–273',
     'Local capital Ob/lowercase ob; source triangles with their observed vertices, arrows and marks.',
     'closed by occurrence-specific III decisions',
     'The III macro is lowercase ob, with the directly observed capital Ob exceptions retained explicitly. The222 source contrasts1.1(ii) and its proof with the capital forms in(i) and(iii); both spellings name the same bound object class through the identity on objects and arrows. The223 source triangle has E-double-prime above E-prime→E, with a transverse tick on the upper-to-left edge; applying i_* sends each vertex and edge to the second displayed triangle. The230 triangle is E→F→G→E with G above and no printed[1], and its next triangle applies f_* to those same vertices and arrows. The239 source has a curved tail at the upper Rf_*(E-double-prime) vertex, separately retained. No shift or linear presentation is inserted in the diplomatic triangle. The derived tensor L is ordinary at its individually observed occurrences, while the category L(X) rule on238–239 remains independent.',
     ['review/global_closure/evidence/group_20.json', 'review/global_closure/evidence/group_21.json',
      'review/expose_iii/decisions.jsonl#29', 'review/expose_iii/decisions.jsonl#32',
      'review/expose_iii/decisions.jsonl#303', 'review/expose_iii/decisions.jsonl#306',
      'review/expose_iii/decisions.jsonl#215']),
 row('conventions/GLOBAL_ISSUES_SGA.md#86', 'IV274–296',
     'Raised round K dots, with lower coherent-group dots and actual primes preserved locally.',
     'closed by the complete IV occurrence audit',
     'The old K-prime replacement is retained only as implemented through the direct source decisions. The9 upper marks on278–280 and later per-page glyph records establish the raised round K form. The lower K marks in the same pages remain lower. For a fixed bound category D, the notational transport fixes each generator[E] and each triangle relation in k(D), hence induces the identity on that same group. The chapter parf macro is overridden at the plain source occurrences279 and293; the source distinction between the full finite-amplitude category and the full perfect category on279 is preserved, with the identity-on-objects inclusion inducing its displayed K map. No new group identification is inferred from the dot shape.',
     ['review/global_closure/evidence/group_24.json', 'review/expose_iv/own_findings.jsonl#12',
      'review/expose_iv/own_findings.jsonl#44']),
 row('conventions/GLOBAL_ISSUES_SGA.md#87', 'V297–364',
     'Baseline series dots; individually ruled Ab and fil with the locally printed punctuation; script category letters.',
     'closed with the global Abfil punctuation prescription replaced by observed local forms',
     'The299 first category name has Ab.fil. with two separate word rules and stops outside; the second299 occurrence, the301 Hom subscript, and all9 occurrences306–310 have separately ruled Ab fil without stops. The later311 forms have their own direct decisions. Thus a macro that forced two stops everywhere would erase the observed punctuation. At each unchanged category name the identity fixes the abelian group, its filtration subgroups and every filtration-preserving homomorphism. Each baseline ellipsis denotes the same ordered intermediate terms of the written sequence; only its source height is restored. Script C and the16 named graded-category G occurrences retain their direct local forms; their exact relation is j:G→C by the degree filtration and Gr:C→G, with epsilon_B sending homogeneous b_n to its degree-n class and inverse taking that class to b_n.',
     ['review/expose_v/decisions.jsonl#30', 'review/expose_v/decisions.jsonl#33',
      'review/expose_v/decisions.jsonl#64', 'review/expose_v/decisions.jsonl#188',
      'review/global_closure/evidence/group_25.json', 'review/global_closure/evidence/group_26.json',
      'review/expose_v/decisions.jsonl#728', 'review/expose_v/own_findings.jsonl#8',
      'review/expose_v/own_findings.jsonl#11', 'review/expose_v/own_findings.jsonl#12',
      'review/expose_v/own_findings.jsonl#14', 'review/expose_v/own_findings.jsonl#15']),
 row('conventions/GLOBAL_ISSUES_SGA.md#88', 'V309–316,344–347,356–360',
     'Small exterior wedges; ordinary-atom wedge names of the augmented lambda-ring; baseline completion arguments under the hat.',
     'closed; the earlier keep-Lambda proposal is superseded by the direct two-scan glyph decisions',
     'The complete315–316 comparison reads8+14 small unadorned exterior wedges. The associated notation map sends every elementary exterior tensor to itself in the same alternating quotient, fixing degree and Module argument. On356–360 the actual counts10,7,15,6,8 read the same unadorned wedge shape as an ordinary-atom algebra name. That rendering names the same augmented lambda-ring: the comparison is the identity on its elements, multiplication, augmentation and every lambda operation, and therefore on its filtration quotients and universal coefficient maps. It adds no exterior-power operation. Completion-placeholder dots on309–313 remain at the baseline under their original hats; each represents the same unspecified functor argument and preserves the printed Hom sources, targets and compositions. All A/E rules and script G letters are occurrence-scoped; the16 G letters are independently closed through347.',
     ['review/expose_v/decisions.jsonl#286', 'review/expose_v/own_findings.jsonl#43',
      'review/expose_v/own_findings.jsonl#151', 'review/expose_v/own_findings.jsonl#154',
      'review/expose_v/own_findings.jsonl#157', 'review/expose_v/own_findings.jsonl#158',
      'review/expose_v/own_findings.jsonl#161', 'review/expose_v/own_findings.jsonl#26',
      'review/expose_v/own_findings.jsonl#30', 'review/expose_v/own_findings.jsonl#33',
      'review/expose_v/own_findings.jsonl#35', 'review/expose_v/own_findings.jsonl#37',
      'review/expose_v/decisions.jsonl#728']),
]

aux = [
 row('ASTRA-CONVENTION-STATEMENTS', 'All reviewed exposés; remaining0,VII,X,XIII emphasis groups',
     'Upright lexical word-group rules, with independently printed mathematical rules and local plain defined terms.',
     'closed;483 exact final-pass records ready for integration',
     'The387 outer groups per branch are the retained source-reviewed emph spans. No new lexical span is selected outside those endpoints. The6 nested defining terms,8 plain resp. tokens and20 diplomatic/21 current numerical locators are individually enumerated. Existing uline spans remain unchanged. Edge punctuation and punctuation-only segments are outside the new lexical rules; internal punctuation remains in its retained word group. Cross-folio groups preserve every literal page-marker comment and the ordered text. Four lexical text wrappers inside mathematical displays73–75 and the ordinary paragraph label on605 are explicitly recorded; every other mathematical-unit byte is identical. The111 original note labels are unchanged; the already observed pre-lambda-ring rule in note21 is the sole author-note body wrapper transport.',
     ['review/global_conventions/transport_validation.json', 'review/global_conventions/typography_groups.json',
      'review/global_conventions/plain_exclusions.json', 'review/global_conventions/fresh_region_evidence.json',
      'review/early/FROZEN_HANDOFF.md', 'review/xiii/HANDOFF.md'],
     'Apply post_review_patches.jsonl only after all ordinary review patches. Map the listed wrappers into existing English translations.'),
 row('ASTRA-CONVENTION-SYMBOL-RULES', 'I,II,VI,VII,X,XII,XIII and locally elsewhere',
     'Single, double and wavy rules retained at their individual symbols; indices and primes outside the rules.',
     'closed by the existing local symbol decisions',
     'The final lexical formatter does not select or transform mathematical font commands. I category C and site S, II category L and VI script C use their source-specific forms. VI§2 identifies C with graded B-modules and degree-preserving maps, C_0 with its named full subcategory and C-prime with O_S-modules; each corrected category glyph fixes those bound objects and maps. X536–537 retains the wavy Picard-functor rule literally in both forms and the straight scheme rules separately. The functor-to-scheme relation is the recorded natural representability identification on T-points, not a claim of mathematical nonrelation. XIII650 similarly retains plain Pic for the representing scheme P, using h_P≅Pic^tau and its K-fibre. Simple primes are outside their observed letter rules; existing explicit symbol rules remain independent of statement prose.',
     ['review/global_closure/evidence/group_31.json', 'review/expose_x/decisions.jsonl#78',
      'review/expose_x/decisions.jsonl#82', 'review/expose_x/decisions.jsonl#83',
      'review/expose_x/decisions.jsonl#84', 'review/xiii/decisions.jsonl#114']),
 row('ASTRA-CONVENTION-DERIVED-SYM-P', 'III,IV,VI,VII; occurrence-scoped',
     'Ordinary derived letters where printed; literal double rules and declared current representations at the specified occurrences.',
     'closed by the existing scoped decisions',
     'Ordinary L and R in III–IV remain ordinary; the category L(X) rule is separate. For a fixed flat representative P of E the derived tensor spelling denotes the same P⊗F, compared by its identity chain map. For a fixed injective representative I the derived-image spelling denotes the same f_*I and identity on cohomology. VI384/385 and the listed VII letters preserve double rules diplomatically and use their declared double-struck current form. VI retains NOTE_6 accepted bold-S transport, while the VII double-rule S occurrences preserve literal diplomatic strokes and the declared bold current form. Their exact object is ⊕Sym^n(E), with the same symmetric-product multiplication. Double-rule projective P is literal diplomatically and bold in current at its recorded occurrences: identity of the graded symmetric algebra induces identity on each degree-zero standard affine chart, then on the glued projective bundle. VII437 single-rule Rees-algebra S stays singly ruled, with no propagation from the symmetric-algebra convention.',
     ['review/global_closure/evidence/group_21.json', 'review/global_closure/evidence/group_22.json',
      'review/global_closure/evidence/group_30.json', 'review/expose_vi/own_findings.jsonl#49',
      'review/expose_vii/own_findings.jsonl#23', 'review/expose_vii/own_findings.jsonl#32',
      'review/expose_vii/own_findings.jsonl#55', 'review/expose_vii/own_findings.jsonl#58',
      'review/expose_vii/own_findings.jsonl#59']),
 row('ASTRA-CONVENTION-O-XIII-XIV', 'XIII616–666 and XIV667–690',
     'Ordinary typed body O in XIII; separately ruled O in its616 note and at the individually observed XIV occurrences.',
     'closed by the existing O repairs; no final mathematical-font replacement',
     'The complete XIII source comparison supplies ordinary body O, with the separately observed underlined footnote occurrence on616. XIV keeps its directly observed plain or singly ruled O forms by occurrence. A font transport at a fixed structure sheaf preserves each ring O_X(U), every restriction homomorphism and the same sheaf/module maps; it does not change the sheaf. Braces around O in the composed TeX protect lexical separation from preceding control words such as otimes. The final convention formatter leaves every such mathematical token unchanged.',
     ['review/xiii/own_findings.jsonl#2', 'review/xiii/own_findings.jsonl#3',
      'review/xiii/own_findings.jsonl#4', 'review/xiii/own_findings.jsonl#5',
      'review/xiii/HANDOFF.md', 'review/late/decisions.jsonl#18',
      'review/global_conventions/transport_validation.json']),
 row('ASTRA-CONVENTION-XIV-DOTS-PHI-CLASS', 'XIV667–690',
     'Lower complex L dots; raised K/Gr/g dots; typed cohomological asterisks; straight phi; locally looped c-ell and typed cl.',
     'closed by the complete XIV local audit',
     'The L complex dots667–669 are baseline marks, with upper primes independently retained. The cohomological degree and Tate-twist placeholders are typed asterisks, whereas the K/Gr/g marks are round raised dots. Each fixed complex or graded family is unchanged component by component, and every displayed differential or graded map keeps its source and target. The straight-stroke phi follows the individual source glyph observations. The looped ell in the class name is rendered as c followed by ell at its named occurrences, while the typed cl in677(4.7) remains typed cl; in each occurrence the class map sends the identical sheaf or cycle to its already bound class. The source-context identification in669 Gr(Y) fixes each graded piece and preserves the printed omission of its dot. Every substantive missing-star or missing-dot correction remains separately registered as a variant.',
     ['review/late/decisions.jsonl#242', 'review/late/decisions.jsonl#11',
      'review/late/decisions.jsonl#94', 'review/late/decisions.jsonl#95',
      'review/late/decisions.jsonl#103', 'review/late/own_findings.jsonl#6',
      'review/late/own_findings.jsonl#8', 'review/late/decisions.jsonl#48',
      'review/late/decisions.jsonl#59', 'review/late/decisions.jsonl#258']),
 row('ASTRA-CONVENTION-NUMERO-MACROS', 'Local abbreviation and macro scopes throughout the volume',
     'Raised-o numero forms; source-derived scoped expansions of Cart, parf.amp, parf.dim, Projz and Gro.',
     'closed by the existing macro and individual spelling records',
     'The n° sign preserves the source raised o and the local punctuation; duplicate stops are adjudicated separately. Cart has one rule at each of its12 source occurrences142–144, so extra wrappers were withdrawn. parf.amp and parf.dim preserve the exact a spelling and the same amplitude/dimension bound. Projz has a rule under Proj and its0 outside; on D_+(f) its sheaf map fixes each section m/f^q of (M[f^−1])_0 and agrees on overlaps. Gro expands locally to Gr with a raised bullet in French from the536 continuation block. Native English had an earlier circle expansion; its sealed X transfer therefore preserves the source continuation block and explicitly renews Gro to the reviewed bullet expansion before the537 use. Formula command/argument bytes stay unchanged; the macro-state evidence is separately retained in the English boundary packet.',
     ['review/late/decisions.jsonl#5', 'review/late/decisions.jsonl#7',
      'review/late/decisions.jsonl#25', 'review/global_closure/evidence/group_17.json',
      'review/global_closure/evidence/group_18.json', 'review/global_closure/evidence/group_19.json',
      'review/global_closure/evidence/group_32.json',
      'review/english/contributions/exposes_viii_x/batches.json']),
]

allrows = rows + aux
save('convention_decisions.json', allrows)
(OUT / 'convention_decisions.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False)+'\n' for x in allrows))
save('convention_evidence.json', evidence)
with (OUT / 'CONVENTIONS_DECIDED.tsv').open('w', newline='') as stream:
    fields = ['source_id','scope','verdict','printed_reading','change','reason','forms','evidence_refs']
    writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t', extrasaction='ignore')
    writer.writeheader()
    for r in allrows:
        writer.writerow({**r, 'evidence_refs': '; '.join(r['evidence_refs'])})

counts = json.loads((OUT / 'typography_counts.json').read_text())
current = [x for x in counts if x['layer']=='current']
table = ['| Exposé | Folios | Existing word-rule commands | Added rule spans | Plain paragraph labels restored |',
         '|---|---:|---:|---:|---:|']
for x in current:
    table.append(f"| {x['expose']} | {x['start']}–{x['end']} | {x['existing_uline_commands']} | {x['word_spans_added']} | {x['paragraph_numbers_restored']} |")

policy = '''# Conventions source et composition finale

Les décisions portent sur des occurrences déjà comparées aux images. Les nouvelles vues de cette passe sont des contrôles typographiques bornés, décrits dans `fresh_region_evidence.json`. Elles n'ajoutent aucun certificat de page entière. Les sept entrées demandées de `GLOBAL_ISSUES_SGA.md` ont chacune une disposition dans `CONVENTIONS_DECIDED.tsv`, avec les observations attribuées et leur empreinte dans `convention_evidence.json`.

## Règles lexicales et étiquettes

La composition rend les groupes de mots soulignés en caractères droits avec `\\uline`. Les formules gardent leur propre typographie, y compris les règles individuelles sous les lettres, les doubles règles et les primes hors des règles. Les termes définis laissés sans règle dans le texte source conservent cette absence de règle ; leur réemploi peut être souligné à un autre endroit. Les six exclusions emboîtées de XIII sont énumérées, ainsi que les huit `resp.` sans règle et les références numériques. Les deux `resp` soulignés de X567 restent soulignés.

Les points terminaux et les segments ne contenant que de la ponctuation sont placés hors des nouvelles règles lexicales. La ponctuation interne demeure dans le groupe de mots déjà délimité. La passe n'ajoute aucun groupe lexical hors des anciens points d'entrée et de sortie des `emph`. Les règles `uline` déjà explicites restent intactes. Le style gras des étiquettes d'énoncés et l'absence de règle sous les sous-titres suivent l'exception explicite de NOTE_6. Les simples numéros de paragraphe ont, en revanche, leur graisse ordinaire :77 groupes par forme sont corrigés, avec conservation du numéro2.2 de la Proposition de205, séparé de son nom par une note de l'auteur.

Les groupes qui traversent les frontières44/45,60/61,61/62,631/632,647/648 et665/666 gardent leurs mots et commentaires de page dans l'ordre exact. Le découpage en patches sert seulement à appliquer les mêmes groupes aux pages déjà composées.

## Portée par exposé

''' + '\n'.join(table) + '''

Les nombres sont des comptes de commandes, non des nombres de théorèmes ou de traits physiques. Le détail diplomatique, notamment658 groupes supplémentaires dans XIII contre659 en corrigé, figure dans `typography_counts.json`. II ne reçoit aucune nouvelle règle : son traitement local a déjà installé770 commandes, avec les22 lettres de catégorie L observées sur173–175.

## Notation mathématique

Le tableau des conventions conserve une notation explicite pour chaque distinction effectivement observée, à sa portée d'auteur. Il ne transporte pas une convention d'un exposé dans un autre. Dans I, la catégorie C et le site S ont leurs règles séparées, tandis que le S objet dans un indice de fibre demeure à son propre emplacement. Dans VI§2, les catégories C, C_0 et C′ sont les lettres scriptes directement lues. Dans V, la catégorie graduée G et la catégorie filtrée C sont reliées par les foncteurs de filtration par le degré et de gradué associé ; l'isomorphisme d'un objet gradué B avec Gr(jB) envoie chaque élément homogène à sa classe de même degré. Ces identifications sont consignées avec les décisions, sans effacer les lettres distinctes.

Les points hauts K et Gr gardent leur position haute ; les points bas des groupes cohérents et des complexes L de XIV667–669 gardent la position basse. Les astérisques de la cohomologie et des torsions de Tate dans XIV restent des astérisques. Les points de l'argument non spécifié sous les chapeaux de V309–313 sont à la ligne de base. Les séries conservent les points à la hauteur lue. Les véritables primes restent des primes.

Les puissances extérieures de V315–316 emploient le petit coin vu dans les deux scans. Le nom de l'anneau sur356–360 emploie le même dessin comme atome ordinaire ; l'identification avec le nom Lambda de l'ancien TeX fixe l'anneau, son augmentation et toutes ses opérations lambda. Cette lecture graphique n'ajoute aucune opération extérieure au nom de l'anneau.

Les lettres dérivées ordinaires de III–IV restent ordinaires. Les doubles règles dérivées observées dans VI–VII sont littérales diplomatiquement et ont la représentation double-barrée déclarée dans la forme corrigée. Le S d'algèbre symétrique de VI conserve le transport gras autorisé par NOTE_6 ; les occurrences VII ont leur propre décision diplomatique à deux règles et corrigée grasse. Le S d'algèbre de Rees de VII437 garde sa règle simple. Les P à deux règles sont reproduits littéralement diplomatiquement et en gras dans le corrigé là où la décision locale le prévoit. L'identité de l'algèbre symétrique induit l'identité des cartes affines de degré zéro et du fibré projectif recollé.

Les règles des foncteurs Hom, Isom, Pic et Proj sont indépendantes des règles lexicales. Le Pic ondulé de X536–537 est conservé littéralement dans les deux formes ; le Pic à règle droite des schémas voisins garde sa règle droite. La relation au schéma représentant est l'identification naturelle des points T avec les classes du foncteur. XIII650 conserve le Pic sans règle employé pour le schéma représentant et sa fibre K, par la même identification de représentabilité.

Le O du corps de XIII est ordinaire ; sa note616 et les occurrences XIV qui présentent une règle gardent leurs règles locales. Les accolades de protection autour de O évitent de fusionner une lettre avec le nom d'une commande TeX précédente. Le phi de XIV suit le trait droit observé. Les occurrences c-ell manuscrites et le cl tapé de677(4.7) suivent leurs observations propres. Les formes n° gardent le o élevé et la ponctuation locale. Les macros Cart, parf.amp, parf.dim, Projz et Gro ont leurs expansions et portées consignées ; le transfert anglais conserve les réinitialisations nécessaires à ses anciens blocs de macros.

Les guillemets, tirets des noms composés, glyphes epsilon et les transports de lettres double-barrées expressément admis par NOTE_6 restent des conventions déclarées de composition. Les règles et lettres ordinaires signalées comme exceptions par les revues locales demeurent telles quelles. La passe finale ne modifie aucune commande de police mathématique.

## Contrôle et application

`post_review_patches.jsonl` doit être appliqué après tous les patches ordinaires, aux deux branches françaises entièrement composées. Ses483 entrées produisent930 applications de branche. Les ancres exactes et leurs comptes sont vérifiés. Les387 groupes extérieurs par branche proviennent des393 commandes emph, avec six groupes définis emboîtés.

La comparaison conserve les111 étiquettes de notes d'auteur. La seule transformation de corps de note concerne le groupe pré-lambda-anneau de21, déjà observé et enregistré ; le contenu et sa formule restent identiques. Quatre mots lexicaux dans des commandes text de formules sur73–75 changent de wrapper, et le numéro3.2 à gauche du display605 devient ordinaire. Tous les autres octets des22 412 unités mathématiques diplomatiques et22 415 unités corrigées sont identiques. L'échantillon `render_sample/typography_sample.pdf`, compilé sans diagnostic puis regardé, vérifie les termes définis, les resp., les références et le numéro ordinaire. Le rendu du livre complet relève du compilateur final.

Les fichiers figés ne sont pas modifiés. Les pages `loaded_*.json` sont les bases exactes avant cette passe ; elles doivent rester disponibles pour reproduire les ancres même après l'ajout de la passe au chargeur partagé.
'''
(OUT / 'CONVENTIONS_SGA6.md').write_text(policy)

exclusions = json.loads((OUT / 'plain_exclusions.json').read_text())
cur_ex = [r for r in exclusions if r['layer']=='current']
ex_table = ['| Folio | Current group | Kind | Exact source content to keep plain |', '|---:|---:|---|---|']
for r in cur_ex:
    content = r.get('plain', r.get('text','')).replace('|','\\|')
    ex_table.append(f"| {r['page']} | {r['group_index']} | {r['kind']} | `{content}` |")
english = '''# English typography transfer handoff

This is an occurrence map for the already sealed translations. It does not authorize changing their mathematical content or their source-boundary macro packets. Apply the mapped wrapper edits in aggregate output, keeping the immutable contribution bases and their original verification hashes.

## Authoritative inputs

- `typography_groups.json`:774 records,387 for each French branch, giving the exact original outer group and its proposed wrapper-only result. Filter by `layer`, then map the source group to its existing translated counterpart.
- `plain_exclusions.json`: the complete local exclusions. Current has6 nested terms,8 plain resp. tokens and21 plain numerical locators; diplomatic has20 locators because the accepted current-only phrase on644 cites3.8.
- `transport_validation.json`: all source/final page hashes, exact notes and math comparisons.
- `typography_counts.json`: per-exposé rule counts and standalone paragraph wrappers.
- `post_review_patches.jsonl`: exact French final-pass anchors; do not apply French prose strings directly to English.

## Scope and punctuation

No new lexical emphasis scope was added outside the existing387 outer emph groups. Four independently source-confirmed lexical words inside mathematical text commands on73–75 retain their existing emphasis scope and change wrapper only. The new final pass does not wrap an already explicit uline group. Existing plain exclusions from earlier local source patches remain plain; this list supplements them rather than replacing them.

Keep full mathematical units literal and outside prose-rule wrappers, retaining any independent symbol rules inside those units. Preserve original notes, note labels, stable targets, and folio marker comments. Keep the same translated words and formula order at all six cross-folio outer groups:44/45,60/61,61/62,631/632,647/648,665/666.

For each mapped lexical piece, the French pass excludes leading/trailing spaces and edge punctuation `.,;:!?()[]«»~`. A piece containing only punctuation remains plain. Internal punctuation is retained inside the previously delimited lexical group. In particular terminal stops and isolated parentheses adjoining mathematical units remain outside the new rule. Do not strip, add, move or reinterpret punctuation bytes in the translated text. Already explicit uline groups retain their local punctuation and source decisions.

Only the six listed nested defining phrases are plain at those definition occurrences. Their reuse elsewhere, such as m-regular in the following616 lemma and special positive k-cycle in658 Lemma6.10, keeps its observed rule. The protection mechanism must therefore be keyed to these exact source groups and their translated anchors. Likewise protect only the eight listed resp. occurrences: the two source X567 resp tokens, groups214 and217, are explicitly ruled and must remain ruled. Other already explicit ruled resp. groups, including I and II, stay intact.

## Complete new plain-exclusion mapping

''' + '\n'.join(ex_table) + '''

For the defining terms the expected English concepts are m-regular; (b)-sheaf; (b)-polynomials; special positive k-cycle of dimension r; integral; degree. Use the exact already adopted translated phrase, preserving all its literal mathematical tokens and the frozen glossary choice.

## Labels and notes

The77 ordinary standalone numeric paragraph labels per branch lose only their bold wrappers. The source2052.2 belongs to a Proposition label divided by the original author note and remains under NOTE_6 accepted statement-label typography. The source6053.2 is an ordinary paragraph label beside a display, so its English counterpart must use ordinary text weight without changing the display equality. Existing statement labels may retain accepted bold styling; no new rule is required under their numbers.

All111 author-note labels are identical in the French transport. One note body, folio21, has the already source-observed lexical wrapper transport: emph around pre-lambda-ring becomes separate ruled lexical pieces on each side of the literal lambda math. Preserve its note command, original label and every translated word. Other note bodies remain outside this final wrapper pass.

The four lexical mathematical text commands are73 dans,74 avec,75 d'où,75 pour tout. Their translated text wrappers follow the already accepted source observations; every other math-unit byte is unchanged by this convention pass. Source605's paragraph-label wrapper is the additional explicitly documented display-side exception.

## Required aggregate checks

Record the source group index, exact English before/after anchor, occurrence count and hashes for each mapped amendment. Verify no nested/doubled uline wrapper is introduced; all plain defining terms, resp. tokens, locators and existing plain exceptions remain unruled; the two567 resp tokens remain ruled; the111 author-note labels and mathematical contents are preserved. Update the old0/I-only `EN_FONT_RENDERING_RECORD` basis to the actual per-exposé source coverage and these exact mappings. This handoff supplies attributed evidence; it does not claim the English aggregate has already passed those checks.
'''
(OUT / 'EN_TYPOGRAPHY_HANDOFF.md').write_text(english)

render = {'source': 'review/global_conventions/render_sample/typography_sample.tex',
          'pdf': 'review/global_conventions/render_sample/typography_sample.pdf',
          'image': 'review/global_conventions/render_sample/sample-1.png',
          'compile_exit_code': 0, 'diagnostics': [], 'pages': 1,
          'visually_viewed': True,
          'observation': 'The plain defining phrases, plain resp. and numeric references remain visibly unruled; reused terms and the two567 resp tokens have rules. Mathematical symbols remain outside the lexical rules. The3.2 label has ordinary weight. No clipping or overfull text is visible.',
          'scope': 'Representative typography sample; no complete-reader rendering certification.'}
save('render_sample/render_validation.json', render)

core = json.loads((OUT / 'TYPOGRAPHY_HANDOFF.json').read_text())
proof = json.loads((OUT / 'transport_validation.json').read_text())
validation = {
 'required_global_items': [76,81,82,84,86,87,88],
 'required_global_items_closed': len(rows), 'additional_convention_rows': len(aux),
 'attributed_evidence_files_or_records': len(evidence),
 'patch_sha256': sha((OUT/'post_review_patches.jsonl').read_bytes()),
 'patch_count': core['patch_records'], 'branch_applications': core['layer_applications'],
 'existing_own_records': core['own_records'],
 'full_page_certificates_added': 0,
 'source_math_changes': 'Only the four declared lexical text wrappers and the605 numeric-label text wrapper; all other math bytes equal.',
 'author_note_labels_identical': all(x['author_note_labels_identical'] for x in proof.values()),
 'render_sample_verified': True,
 'frozen_files_changed': False,
 'english_application_status': 'Exact handoff supplied; aggregate mapping/rendering owned by english_audit_build.',
}
assert validation['patch_sha256']=='daa85e9b4ddc6221571bc248383035cef5b346b6d312c4bdab9247c7b824fdc7'
save('HANDOFF_VALIDATION.json',validation)

handoff = '''# Final convention handoff

The convention package is coherent and ready for integration. Required GLOBAL_ISSUES76,81,82,84,86,87,88 are closed in `CONVENTIONS_DECIDED.tsv` and `convention_decisions.jsonl`; six supplementary rows cover the remaining NOTE_6 notation and typography scopes. Exact attributed observations are copied with hashes in `convention_evidence.json`. No new full-page certification is claimed.

Apply `post_review_patches.jsonl` as an explicit **final** pass after every ordinary review patch, in both French builder and shared reviewed-French loader. The stable stream has483 records,930 branch applications and189 local own-finding rows. Its SHA256 is `daa85e9b4ddc6221571bc248383035cef5b346b6d312c4bdab9247c7b824fdc7`. Both exact branches replay against the saved fully composed inputs. The final pass adds1,212 diplomatic/1,213 current lexical spans and restores77 standalone numeric labels in each branch.

The111 author-note labels are unchanged. The only author-note body wrapper change is the already read21 pre-lambda-ring phrase. The four lexical math-text words on73–75 and the605 display-side paragraph-label wrapper are explicit exceptions; all other bytes in22,412 diplomatic/22,415 current mathematical units are identical. The representative one-page PDF compiled without diagnostics and was viewed; the complete book still receives its normal final compile/render verification.

Use `CONVENTIONS_SGA6.md` for the reader README policy. `EN_TYPOGRAPHY_HANDOFF.md` gives the exact application/exclusion guidance requested by the English owner, including punctuation, all35 current plain exclusions and the special ruled567 tokens. No new lexical scope has been added outside the retained emphasis endpoints. Existing explicit rules and source-local mathematical font choices are not rewritten.

The core patch stream and its pre-final-pass loaded snapshots must stay stable. Later root integration can mark applications in separate build reports. Frozen source reviews, prior checkpoints and sealed English contributions are untouched.
'''
(OUT/'HANDOFF.md').write_text(handoff)

selected = [p for p in OUT.rglob('*') if p.is_file() and p.suffix in {'.json','.jsonl','.tsv','.md','.py','.tex','.pdf','.png'} and '__pycache__' not in p.parts and p.name!='MANIFEST.json']
save('MANIFEST.json', [{'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size, 'sha256':sha(p.read_bytes())} for p in sorted(selected)])
print(json.dumps(validation, ensure_ascii=False))
