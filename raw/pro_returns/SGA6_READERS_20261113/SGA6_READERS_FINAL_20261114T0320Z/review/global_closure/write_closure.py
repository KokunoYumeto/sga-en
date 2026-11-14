#!/usr/bin/env python3
"""Close historical aliases from attributed source reviews; never edit source text."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'review/global_closure'
EVIDENCE = OUT / 'evidence'
EVIDENCE.mkdir(exist_ok=True)
GROUPS = json.loads((OUT / 'groups.json').read_text())
PENDING = json.loads((OUT / 'pending_inventory.json').read_text())
MARK = re.compile(r'%{10}\s+scan idx\s+\d+\s*\|\s*folio\s+(\d+)\s+%{10}')
FORMS = 'French diplomatic and corrected; English transfer follows the same established source decisions.'

def sha(s):
    return hashlib.sha256(s.encode() if isinstance(s, str) else s).hexdigest()

def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

cache = {}

def record(ref):
    if ref not in cache:
        path, number = ref.rsplit('#', 1)
        line = (ROOT / path).read_text().splitlines()[int(number) - 1]
        cache[ref] = dict(reference=ref, record_sha256=sha(line), record=json.loads(line))
    return cache[ref]['record']

def refs_by_source(path, pattern):
    rx = re.compile(pattern)
    return [f'{path}#{n}' for n, line in enumerate((ROOT / path).read_text().splitlines(), 1)
            if rx.search(json.loads(line).get('source_id', ''))]

def owner(p):
    for end, directory in [(77,'early'),(159,'expose_i'),(221,'expose_ii'),
                           (273,'expose_iii'),(296,'expose_iv'),(364,'expose_v'),
                           (415,'expose_vi'),(465,'expose_vii'),(497,'expose_viii'),
                           (518,'expose_ix'),(594,'expose_x'),(615,'expose_xii'),
                           (666,'xiii'),(700,'late')]:
        if p <= end:
            return directory
    raise ValueError(p)

def certificates(pages):
    answer = []
    for p in sorted(set(pages)):
        path = f'review/{owner(p)}/page_status.jsonl'
        matches = []
        for n, line in enumerate((ROOT / path).read_text().splitlines(), 1):
            d = json.loads(line)
            if d.get('page', d.get('folio')) == p:
                matches.append(f'{path}#{n}')
        assert matches, (p, path)
        answer.extend(matches)
        if p == 549:
            ap = 'review/expose_x_amendments/page_status.jsonl'
            for n, line in enumerate((ROOT / ap).read_text().splitlines(), 1):
                if json.loads(line).get('page') == p:
                    answer.append(f'{ap}#{n}')
    return answer

def images(pages):
    return '; '.join(f'scan/SGA6_scan_360dpi.pdf#page={p+14}; '
                     f'scan/SGA6_witness_300dpi.djvu#page={p+11}' for p in pages)

def attributed_images(refs, cert_refs):
    """Name only image sources actually asserted in the attributed records."""
    found = []
    for ref in refs + cert_refs:
        d = record(ref)
        value = d.get('image')
        if isinstance(value,str):
            found.extend(v.strip() for v in value.split(';') if v.strip())
    for ref in cert_refs:
        d=record(ref)
        p=d.get('page',d.get('folio'))
        if not isinstance(p,int):
            continue
        found.append(f'scan/SGA6_scan_360dpi.pdf#page={d.get("pdf_page",p+14)}')
        witness=d.get('witness_viewed')
        if isinstance(witness,int) and not isinstance(witness,bool):
            found.append(f'scan/SGA6_witness_300dpi.djvu#page={witness}')
        elif witness is True:
            found.append(f'scan/SGA6_witness_300dpi.djvu#page={p+11}')
        for wp in d.get('witness_pages',[]):
            found.append(f'scan/SGA6_witness_300dpi.djvu#page={wp}')
    return '; '.join(dict.fromkeys(found))

def spec(number, page, pages, refs, printed, verdict, reason, change=None,
         is_misprint=False, region='The exact scope documented by the attributed records',
         new_image_read=False, extra=None):
    return dict(group=number, page=page, actual_pages=list(pages), evidence_refs=refs,
                printed_reading=printed, verdict=verdict, reason=reason, change=change,
                is_misprint=is_misprint, region=region, new_image_read=new_image_read,
                extra=extra or {})

specs = {}

# The two records in these groups describe the same historical operation.
for number, page, ref in [(1,21,'review/early/decisions.jsonl#133'),
                          (2,21,'review/early/decisions.jsonl#134'),
                          (3,24,'review/early/decisions.jsonl#148')]:
    r = record(ref)
    specs[number] = spec(number,page,[page],[ref],r['printed_reading'],
        'confirmed as accepted heading transport',
        r['reason'] + ' This closes the paired historical FIXLOG alias by attribution to that exact scan decision. '
        'The map from the printed heading to the accepted heading is the identity on every word, accent, numeral and mathematical token; only the explicitly accepted heading rule is omitted.',
        'Retain the existing heading typography; no new text patch.',region=r['region'])

# Elision audit: preserve the recoverable present occurrences without inventing
# offsets for nineteen historically indistinguishable event records per log.
elisions = []
macro_inventory = []
baseline_text = {}
for layer in ['diplomatic', 'current']:
    path = f'fr/sga6/{layer}/main.tex'
    text = (ROOT / path).read_text()
    baseline_text[layer] = text
    marks = list(MARK.finditer(text))
    def page_at(pos):
        previous = [m for m in marks if m.start() <= pos]
        return int(previous[-1].group(1)) if previous else None
    for m in re.finditer(r"(?:[A-Za-zÀ-ÿ]+)'%\n\s*[A-Za-zÀ-ÿ]+", text):
        exact = m.group(0)
        elisions.append(dict(layer=layer,page=page_at(m.start()),source=path,
            source_sha256=sha(text),offset=m.start(),exact_source=exact,
            expanded_word=re.sub(r'%\n\s*','',exact),
            context=text[max(0,m.start()-45):m.end()+55]))
    all_defs = list(re.finditer(r'\\(?:providecommand|renewcommand|newcommand)\{\\([A-Za-z]+)\}[^\n]*',text))
    for g in GROUPS:
        if not 5 <= g['group'] <= 16:
            continue
        name = re.search(r'\{\\(\w+)\}',g['data']['new']).group(1)
        p = int(g['data']['page'])
        matches = [m for m in all_defs if m.group(1)==name and page_at(m.start())==p]
        assert len(matches)==1,(layer,g['group'],matches)
        m = matches[0]
        end = next((q.start() for q in all_defs if q.start()>m.start() and q.group(1)==name),len(text))
        uses = list(re.finditer(r'\\'+name+r'(?![A-Za-z])',text[m.end():end]))
        first = m.end()+uses[0].start() if uses else None
        macro_inventory.append(dict(group=g['group'],layer=layer,source=path,
            source_sha256=sha(text),historical_boundary_page=p,macro=name,
            exact_definition=m.group(0),offset=m.start(),use_count_until_next_definition=len(uses),
            first_use_page=page_at(first) if first is not None else None,
            first_use_context=text[first-45:first+110] if first is not None else None,
            next_definition_offset=end if end<len(text) else None,
            scan_claim='The command is unprinted implementation text; only its output occurrences have scan loci.'))
assert len(elisions)==30
assert {d['page'] for d in elisions}=={91,103,105,167,177,190,281,322,351,354,383,397,525,549,561}
for p in {d['page'] for d in elisions}:
    pair=[d for d in elisions if d['page']==p]
    assert len(pair)==2 and pair[0]['expanded_word']==pair[1]['expanded_word']
save(EVIDENCE/'elision_inventory.json',dict(
    historical_rows_per_log=19,current_recoverable_occurrences_per_layer=15,
    limitation='The nineteen identical event records provide no offsets or distinct words. No one-to-one reconstruction of those historical edits is asserted.',
    semantics='With ordinary TeX comment handling, % consumes the end of the line. Suppressing leading indentation on the next line yields the exact adjacent letter sequence after the apostrophe, with no inserted interword space.',
    occurrences=elisions))
save(EVIDENCE/'macro_inventory.json',macro_inventory)
elision_pages=sorted({d['page'] for d in elisions})
specs[4] = spec(4,None,elision_pages,[],
    'Apostrophe and following word are contiguous at the fifteen recoverable current source locations in each layer.',
    'resolved as implementation record; historical event offsets unavailable',
    'The original nineteen FIXLOG rows, repeated in the CURRENT log, have exactly identical payloads and no occurrence coordinates. '
    'The present source audit records fifteen apostrophe-%-newline occurrences in each layer, with the same reconstructed words in both. '
    'The TeX comment removes the endline before the following letters; the explicit map deletes only the comment/newline/indentation bytes and is the identity on all apostrophes and letters. '
    'Each recoverable source page has its attributed full comparison record; page549 also has its separate completed damaged-notation amendment. '
    'These facts settle the operation as a nonvariant spacing implementation record. They do not reconstruct a separate location for each of the nineteen old events; that historical metadata limitation is retained.',
    'No source-body or apparatus variant; retain the existing elision joining.',
    region='Unprinted line-end comments at the fifteen enumerated elisions',
    extra=dict(supplementary_evidence_packet='review/global_closure/evidence/elision_inventory.json',
               historical_event_locations_reconstructed=False))

# Macro renewals are adjudicated as implementation changes, with actual final
# definitions and uses recorded above. Later local case decisions take priority.
macro_pages={5:[84,90],6:[125,126],7:[146,147],8:[146,445],9:[159,160],
             10:[245,246],11:[245],12:[273,274],13:[273],14:[518],15:[536],16:[536,549]}
for number in range(5,17):
    entry=next(d for d in macro_inventory if d['group']==number and d['layer']=='current')
    p=entry['historical_boundary_page']; name=entry['macro']; refs=[]
    if number==10:
        refs=refs_by_source('review/expose_iii/decisions.jsonl',r'^check/findings/findings_231_235.json#(?:2|3)$')
    if number==12:
        refs=['review/expose_iv/own_findings.jsonl#1']
    reason=(f'The historical operation changes the definition mechanism for \\{name} from providecommand to renewcommand. '
        'The macro inventory gives the exact definitions in both attached layers, the next redefinition boundary, and the actual first use or the absence of uses. '
        'A providecommand leaves an existing definition unchanged; the recorded renewcommand assigns the stated replacement text at this exact boundary. ')
    if name=='Ob':
        reason+='The output spells the object-class label of the already bound category. Its notation map fixes every object and every morphism of that category; it changes no membership, fibre, functor or morphism. '
    elif name=='Im':
        reason+='Its operatorname expansion names the same image object of the displayed morphism, with the same inclusion into its codomain; the object and inclusion maps are unchanged. '
    else:
        reason+='Its operatorname expansion denotes the identity morphism of the same displayed object, acting as x↦x on sections, with the same domain and codomain. '
    if number in [10,12]:
        reason+='The old payload with capital Ob is superseded by the later, separately checked lower-case ob convention. The live definition is lower-case ob, as listed in the inventory; the original capital payload is not reapplied. '
    if entry['use_count_until_next_definition']==0:
        reason+='No use of this macro occurs before its next definition in the attached source, so this renewal has no intervening printed occurrence to certify. '
    else:
        reason+=f'The first surviving use is on folio{entry["first_use_page"]}; its existing source comparison is attributed, not represented as a fresh scan reading here. '
    specs[number]=spec(number,p,macro_pages[number],refs,entry['exact_definition'],
        'resolved; renewal retained with later case correction' if number in [10,12] else 'resolved as retained macro implementation',
        reason,'No new patch; retain the exact currently scoped macro definition.',
        region=f'Unprinted macro definition after historical folio{p}; output scope recorded separately',
        extra=dict(supplementary_evidence_packet='review/global_closure/evidence/macro_inventory.json',
                   macro=name,printed_macro_itself=False))

for number,operator in [(17,'parf.amp'),(18,'parf.dim')]:
    specs[number]=spec(number,'preamble',list(range(127,141)),
        ['review/expose_i/decisions.jsonl#971','review/expose_i/decisions.jsonl#1058',
         'review/expose_i/own_findings.jsonl#152','review/expose_i/own_findings.jsonl#153'],
        operator+' with a', 'confirmed as retained spelling implementation',
        f'The exact I134 spelling decision and I137 repeat establish {operator} with a, and the source macro already expands to that letter string. '
        'NOTE_6 expressly accepts this spelling transport. The internal perfamp/perfdim command name has no printed letters of its own. '
        'The local rules under the operators on127–128 remain occurrence-scoped as recorded; this spelling record neither adds nor removes such rules. '
        'The amplitude/dimension expression retains the same argument and the same integer bound; its notational map is the identity on that bound.',
        'Retain existing macro expansion; no new variant.')

specs[19]=spec(19,'macro',[142,143,144],
    [f'review/expose_i/own_findings.jsonl#{n}' for n in [206,207,208]],
    'One rule beneath Cart at each of the twelve occurrences, counts2,6,4.',
    'confirmed; one-rule expansion retained',
    'The exact local amendment establishes two Cart occurrences on142, six on143 and four on144. '
    'The active macro already expands to underline(operatorname Cart), so an extra local underline would render two rules. '
    'The previous local wrappers were explicitly withdrawn in the attributed decisions. This historical two-definition change is retained with that correction. '
    'The category of cartesian objects, its objects and arrows, and the separately ruled site subscript are unchanged by the single-rule notation map.',
    'No new patch; keep the one-rule Cart macro and the existing wrapper withdrawals.')

specs[20]=spec(20,'221-',[221,222,223,224,225],
    [f'review/expose_iii/decisions.jsonl#{n}' for n in [7,10,13,19,26,47]],
    'The explicitly observed capital Ob and lower-case ob occurrences are retained individually.',
    'confirmed with occurrence-scoped case decisions',
    'The I/II-to-III boundary macro uses lower-case ob. The complete222 source decision explicitly contrasts the lower-case occurrences in1.1(ii) and its proof with capital Ob in(i) and(iii);223 and225 have separately recorded lower-case forms. '
    'The old count3 is an implementation count, not a claim that every printed occurrence is lower-case. Explicit capital spellings are retained at their own source positions. '
    'Both spellings name the same bound object class in each membership expression; the identification fixes those objects and their category morphisms.',
    'Retain the reviewed local case forms; no new global substitution.')

iii_l_refs=[f'review/expose_iii/decisions.jsonl#{n}' for n in [88,91,94,98,101,107,110,113,117,120,129,138,141,144,268]]
specs[21]=spec(21,'221-273',list(range(221,274)),
    specs[20]['evidence_refs']+iii_l_refs+['review/expose_iii/own_findings.jsonl#25','review/expose_iii/own_findings.jsonl#26'],
    'Occurrence-specific Ob/ob; ordinary derived L, with the separately ruled category L(X) retained.',
    'confirmed with the completed III local exceptions',
    'The derived-L decisions on231–235 are individually attributed; the242–245 aggregate explicitly checks7,7,8,9 ordinary letters. '
    'The full III page certifications cover the remaining occurrences. The local category name L(X) on238–239 has its separate visible rule and is not overwritten by this derived-functor convention. '
    'For a flat replacement P of E, both printed derived-L notations denote the identical tensor complex P⊗F, with the identity chain map and the same map on its localized derived category. '
    'The lower-case object macro retains the explicit capital exceptions described in the preceding group. The historical count129 is preserved as event metadata, not inferred from a present global count.',
    'No new patch; retain every already reviewed local form.')

for number in [22,23]:
    specs[number]=spec(number,'236-240',list(range(236,241)),
        ['review/expose_iii/decisions.jsonl#185','review/expose_iii/decisions.jsonl#215'],
        'Ordinary typed R in the source derived-direct-image expressions236–240.',
        'resolved as recorded no-op' if number==22 else 'confirmed as historical scoped font transport',
        ('The first historical row has count0 and therefore records no replacement. ' if number==22 else
         'The second historical row records23 replacements; that event count does not assert the total number of R letters presently on these pages. ')+
        'The source decision on238 explicitly reads ordinary R in j′_*Rf_*(E); the complete236–240 page comparisons and the individually checked239 triangle retain the remaining ordinary forms. '
        'Choosing the same injective representative I of E, both font encodings denote the same complex f_*I; identity on f_*I and on its cohomology identifies the named derived functor without changing its arguments or degrees. '
        'No rule or font choice from another exposé is propagated into this scope.',
        'No new patch or mathematical variant.')

iv_refs=[f'review/expose_iv/decisions.jsonl#{n}' for n in [25,29,42,46,65]]
iv_refs += [f'review/expose_iv/own_findings.jsonl#{n}' for n in [10,12,17,18,23,29,32,35,36,37,42,44,46,50,51]]
specs[24]=spec(24,'Exposé IV',list(range(274,297)),iv_refs,
    'Raised round K dots; ordinary derived L; locally ruled parf, including the plain parf on279 and plain Parf on293.',
    'confirmed with completed occurrence-scoped IV refinements',
    'The aggregate nine raised K dots on278–280 and the later per-page glyph records establish the raised round mark. '
    'They also preserve the distinct lower K marks in the actual displays, rather than replacing all K annotations. '
    'The local279 correction explicitly bypasses the chapter underlined-parf macro for the plain occurrence in2.3(a);293 retains plain Parf. '
    'Thus the old scoped count160 is not reapplied as a blanket command. For every fixed category D, its font/dot transport fixes each generator [E] of k(D) and each triangle relation; it induces the identity homomorphism on that same Grothendieck group. '
    'For each derived tensor expression the chosen flat representative and its identity chain map remain unchanged. These explicit identifications concern only the same bound objects at the inspected occurrences.',
    'Retain the completed IV local renderings; no new patch.')

specs[25]=spec(25,'Exposé V',[299,301,306,307,308,309,310,311],
    [f'review/expose_v/decisions.jsonl#{n}' for n in [33,64,188]]+
    ['review/expose_v/own_findings.jsonl#32'],
    'Separate rules beneath Ab and fil at the individually inspected category names, without full stops at these occurrences.',
    'amended to occurrence-specific category rendering',
    'The historical macro change is superseded as an implementation prescription by the reviewed local expansion patches. '
    'The299 and301 occurrences are separately resolved;306–310 have counts3,1,1,3,1, and311 has three further names. '
    'The exact decisions deliberately avoid inferring an uninspected global spelling or punctuation from these observations. '
    'At each unchanged category name, the comparison fixes the underlying abelian group, every filtration subgroup and every filtration-preserving homomorphism. '
    'The source-specific word rules and punctuation therefore use the already recorded local forms.',
    'No new macro replacement; retain local patches and their exact counts.')

g_reason=('The exact aggregate finding306–310#14 records sixteen directly compared script G occurrences:308(6),309(2),310(1),311(3),313(1),344(1),345(1),347(1). '
    'The old nominal range306–313 contains thirteen actual G letters on308–313. The two later occurrences belong to344 final line and345 Ob(G), after the corrected page boundary. '
    'Section1.11 defines j:G→C by equipping a graded K-algebra B with its degree filtration, and Gr:C→G by the associated graded. '
    'Its epsilon_B:B→Gr(jB) sends a homogeneous b_n to its degree-n class, with inverse taking that class to b_n; these maps preserve addition, multiplication, grading and graded algebra homomorphisms. '
    'The old C_g encoding is replaced only where the actual printed glyph is the named script G; all separate C and C_o source letters remain as observed.')
specs[26]=spec(26,'306-313',list(range(306,314)),
    ['review/expose_v/decisions.jsonl#728'],
    'Thirteen script G occurrences on actual308–313.',
    'confirmed; actual occurrence scope clarified',g_reason,
    'Retain the thirteen verified G forms; no new patch.')
specs[28]=spec(28,'344-345',[344,345],
    ['review/expose_v/decisions.jsonl#728','review/expose_v/own_findings.jsonl#116','review/expose_v/own_findings.jsonl#119'],
    'Script G at344 final line and345 Ob(G).',
    'confirmed; corrected folio boundary retained',g_reason,
    'Retain the two verified G forms; no new patch.')

specs[27]=spec(27,'327-330',[327,328,329,330],
    ['review/expose_v/decisions.jsonl#489','review/expose_v/decisions.jsonl#539'],
    'Eight ruled unit1 numerals327–328; seven ruled Z and the two introducing F/F′ sheaf names on330.',
    'amended by the complete local rule inventory',
    'The old thirteen-replacement count is an event count. The completed scan decisions identify eight unit rules, including three earlier omissions on328, and seven Z plus two introducing F rules on330, including the earlier omitted first F. '
    'The final element F−F′ and all A,A^n,U_n on330 remain plain. Every unit annotation remains outside the rule; the prime of F′ also stays outside. '
    'The comparison fixes the same unit of the printed product, the same constant-sheaf sections n↦n, and the same sheaves F,F′ with identity section maps. '
    'The later independently justified fraction delimiters are unaffected by this graphical record.',
    'Retain the completed local additions and exceptions; no new patch.')

specs[29]=spec(29,370,[369,370],['review/expose_vi/decisions.jsonl#46'],
    'Folio369 ends at λ′≥λ;370 begins et un faisceau.',
    'confirmed as retained folio boundary',
    'The attributed source decision compares the end of369 and the beginning of370 in both images. The complete word group et un faisceau belongs to370. '
    'Moving only the unprinted marker before et leaves the ordered prose and mathematical tokens identical.',
    'Retain the already correct marker; no new patch.',region='369/370 boundary')

vi_refs=['review/expose_vi/decisions.jsonl#20','review/expose_vi/decisions.jsonl#38',
         'review/expose_vi/decisions.jsonl#268','review/expose_vi/decisions.jsonl#295']
specs[30]=spec(30,'Exposé VI',list(range(365,416)),vi_refs,
    'Raised round K dots; accepted NOTE_6 bold-S transport for the two printed S rules; occurrence-scoped Proj rules.',
    'confirmed with completed VI local refinements',
    'The366 source distinguishes the raised solid K dots from the small circles in numbered items. '
    'The368–370 S operators have two separately read lower rules, and NOTE_6 explicitly permits their bold S encoding; each ruled E argument has its own independent rule. '
    'The twenty-one underlined Proj_0 names on381–389 retain their exact local scope, including the separate plain geometric Proj(B) on382. '
    'The separately adjudicated missing K dot in389 prose is not silently converted into a diplomatic printed dot. '
    'For the fixed locally free sheaf E, the S notation map is identity on every symmetric power S^n(E), hence on ⊕_n S^n(E), multiplication and graded morphisms. '
    'For every fixed reviewed Grothendieck category the K glyph transport fixes [E] and the defining relations, inducing the identity group map. '
    'No VII or other exposé font policy is propagated here; the historical231-replacement count is retained solely as event metadata.',
    'Keep the completed local forms and separate paired source corrections; no new patch.')

specs[31]=spec(31,'380-389',list(range(380,390)),['review/expose_vi/decisions.jsonl#294'],
    'Script C, C_0 and C′ in all thirty named occurrences of VI§2.',
    'confirmed by the completed thirty-occurrence source decision',
    'The attributed aggregate explicitly completes the source comparison on380,383,384,386,387,388,389 and records the visible loops and C-shaped bowls. '
    'Section2.2 binds C to graded B-modules and degree-preserving B-linear maps, C_0 to its stated full subcategory, and C′ to O_S-modules. '
    'At each old G-encoded occurrence the corrected name retains exactly that bound object and those arrows: on C it sends M to M and each graded map u to u; on C_0 it restricts the same identity; on C′ it fixes each O_S-module and homomorphism. '
    'The first damaged380 letter uses the established definition and its repeated category list as documented by the source reviewer; no new recovered stroke is claimed here.',
    'Retain the thirty reviewed C forms; no new patch.')

specs[32]=spec(32,'381-389',list(range(381,390)),['review/expose_vi/decisions.jsonl#295'],
    'Twenty-one ruled Proj_0 names: fifteen on381–385, then386(1),387(1),389(4).',
    'confirmed with the geometric Proj exception retained',
    'The original log divides its twenty-one implementation replacements into ten explicit operatorname forms and eleven command forms in each layer. '
    'The completed aggregate source decision separately establishes all twenty-one printed rules, and retains the plain geometric Proj(B) on382. '
    'The active Projz expansion prints one rule under Proj and leaves the zero outside. The functor preserves the same sheaf on Proj(B): on D_+(f) its local module is the same degree-zero localization (M[f^−1])_0, and the comparison sends every localized section m/f^q to itself; these maps agree on overlaps. '
    'Thus the macro change identifies the same sheaf and sheaf maps without changing the scheme construction or adding a rule to its separate occurrence.',
    'Retain the twenty-one existing macro uses; no new patch.')

# Page-less Codex entries: the newer local decisions, not the old queue status,
# determine the final attributed disposition.
specs[33]=spec(33,89,[89],['review/expose_i/own_findings.jsonl#25'],
    'Three plain site-S occurrences in Proposition1.4.1; other site rules and object S remain occurrence-specific.',
    'global proposal rejected; local paired repair already established',
    'The old rejection reason claiming uniformly plain site S is superseded by the exact89 source decision. '
    'Three plain S letters in the proposition opening name the same site that is ruled in S∈ob S; current restores only those three site rules and diplomatic preserves them plain. '
    'Replacing every site name by calligraphic S was not the printed typography and is not adopted. '
    'The explicit comparison fixes the underlying site category and its arrows. For its fibred category p:C→S, it keeps p, each base object U, and the fibre C_U unchanged; the object binder S in the actual formula is not relabelled. '
    'This closure retains the existing local correction and its variant instead of the earlier global claim.',
    'No new patch; preserve ASTRA-I-S-089-PROP and the independently observed rules.',
    is_misprint=True,region='I Proposition1.4.1 opening and site/object notation')

specs[34]=spec(34,129,[129],
    [f'review/expose_i/decisions.jsonl#{n}' for n in [838,841,844,847]]+['review/expose_i/own_findings.jsonl#156'],
    'Left coefficient A′ in all four listed category occurrences; site/object S′ rule positions independently resolved.',
    'old uncertainty resolved; exact transcription repair accepted',
    'The four native-image decisions resolve the lowered A with a high prime in both corollary categories, the proof category and the final functor target. '
    'The earlier OCR-based rejection is therefore obsolete. The site glyph is the independently observed ruled S, while the proof final object S′ is plain; the proposed blanket calligraphic S is not adopted. '
    'For E′ with commuting left A′ and right A actions, E′⊗^L_A E inherits a′(e′⊗e)=(a′e′)⊗e on the same chosen flat tensor representative; the balancing relation (e′a)⊗e=e′⊗ae is respected by the commuting A′ action. '
    'This supplies the exact left-A′ target map without changing the printed site/final-object distinctions. Both layers already contain these scan-supported transcription repairs; no source misprint variant is created.',
    'No new patch; retain the four A′ repairs and the precise site rule map.',region='I Corollary4.19 and proof')

for number, page, ref, proof in [(35,411,'review/expose_vi/own_findings.jsonl#132','review/expose_vi/cohomology_index_411.json'),
                                 (36,415,'review/expose_vi/own_findings.jsonl#141','review/expose_vi/basis_product_415.json')]:
    r=record(ref)
    specs[number]=spec(number,page,[page],[ref],r['printed_reading'],
        'earlier Codex rejection reversed by completed source proof',
        r['reason']+' The historical page-less rejection is closed by this exact later source adjudication; its existing paired correction is retained and no second patch is applied.',
        r['change'],is_misprint=True,region=r['region'],
        extra=dict(proof_file=proof,proof_sha256=sha((ROOT/proof).read_bytes())))

specs[37]=spec(37,224,[224],['review/expose_iii/decisions.jsonl#75','review/expose_iii/own_findings.jsonl#10'],
    'The first base-change assertion has no(i); the next assertion is labelled(ii).',
    'rejected; author numbering retained',
    'The source decision reads both assertions in both scans and retains the unlabelled first assertion. '
    'The ordered-position map identifies the first assertion and the following(ii) without inserting an author label. '
    'Its base-change morphism is independently identified with EGAIII1.4.15.4 under u=i,v=g,v′=f,u′=i′,q=0. On affine pieces the exact map B⊗_A M→(B/IB)⊗_(A/I)M is b⊗m↦(b mod IB)⊗m, with inverse induced by the same representatives. '
    'That established map supplies no missing printed(i), so both bodies retain the source numbering.',
    'No patch or variant for the omitted first label.',region='III Lemma1.1.3 first two assertions')

for number,page,ref in [(38,254,'review/expose_iii/decisions.jsonl#370'),(40,272,'review/expose_iii/decisions.jsonl#562')]:
    r=record(ref)
    specs[number]=spec(number,page,[page],[ref],r['printed_reading'],
        'amended; exact local paired punctuation repair retained',
        r['reason']+' This resolves the earlier page-less queue through that precise local correction rather than reapplying its different delimiter proposal.',
        r['change'],is_misprint=True,region=r['region'])

specs[39]=spec(39,261,[261],['review/expose_iii/own_findings.jsonl#86'],
    "La condition a) (resp. a′), b), b′)) est de nature locale",
    'rejected; source delimiters are balanced',
    'The present bounded reinspection of the complete main261 image and native261 image directly confirms the two consecutive closing parentheses after b′. '
    'Parse a), a′), b), b′) as the four already defined item-label tokens. The opening parenthesis before resp. encloses the last three label tokens and their separators; its matching close is the final parenthesis after the b′) token. '
    'The exact decomposition is label(a)) + outer-open + resp. + label(a′)) + comma + label(b)) + comma + label(b′)) + outer-close. '
    'Deleting the final close would remove the match for the outer opening. No deletion is made, and the four labelled conditions, their order and their mathematical meaning are unchanged.',
    'Retain both consecutive closes; no patch or variant.',
    region='III Remarques5.2(i), first line',new_image_read=True,
    extra=dict(new_image_files=['review/expose_iii/images/p261.png','review/expose_iii/images/w261.png'],
               new_review_scope='Only the stated delimiter region; no new full-page certification.'))

assert set(specs)==set(range(1,41))
decisions=[]
packets=[]
for group in GROUPS:
    s=specs[group['group']]
    cs=certificates(s['actual_pages'])
    for ref in s['evidence_refs']+cs:
        record(ref)
    packet=dict(s)
    packet.update(historical_ids=group['ids'],historical_payload=group['data'],
                  page_certificate_refs=cs,
                  evidence_mode='bounded new delimiter inspection plus attributed completed page review' if s['new_image_read'] else 'attributed existing source review plus current implementation audit')
    packets.append(packet)
    for source_id in group['ids']:
        d=dict(source_id=source_id,page=s['page'],type='rejected_codex' if group['group']>=33 else 'fixlog',
            record_type='rejected_codex' if group['group']>=33 else 'fixlog',
            verdict=s['verdict'],printed_reading=s['printed_reading'],
            image=attributed_images(s['evidence_refs'],cs),region=s['region'],reason=s['reason'],change=s['change'],
            forms=FORMS,is_misprint=s['is_misprint'],
            correction_status='existing paired local correction retained' if s['is_misprint'] else 'no new source correction',
            evidence_mode=packet['evidence_mode'],new_image_read=s['new_image_read'],
            evidence_refs=s['evidence_refs'],page_certificate_refs=cs,
            evidence_packet=f'review/global_closure/evidence/group_{group["group"]:02d}.json',
            historical_record_group=group['group'],historical_aliases=[i for i in group['ids'] if i!=source_id],
            source_body_patch_added=False,**s['extra'])
        decisions.append(d)
    save(EVIDENCE/f'group_{group["group"]:02d}.json',packet)

# One deliberate override of the source-specific apparatus attribution. The
# accepted word correction and both French source bodies already are correct.
misprint_ref='review/late/decisions.jsonl#746'
misprint_evidence=['review/late/decisions.jsonl#178','review/late/decisions.jsonl#431']
for ref in [misprint_ref]+misprint_evidence:
    record(ref)
amendment=dict(source_id='fixes/MISPRINTS_6.json#665',page=688,type='misprint',record_type='misprint',
    kind='misprint_in_print',verdict='amended; source-specific apparatus attribution corrected',
    printed_reading='Sborik',image=images([688]),region='Bibliography entry[17], journal name',
    reason='Both mainPDF702 and nativeDjvu699 were directly re-viewed in the saved688 strips and print MAt. Sborik. '
    'This record concerns the missing n in Sborik only: diplomatic retains Sborik and current retains the established Sbornik. '
    'The previous MISPRINT665 decision copied the MAt./Mat. capitalization explanation from MISPRINT664 and pointed to checker46. '
    'Replace that attribution with the missing-letter explanation and checker47, matching the already correct FIXLOG2656 decision. '
    'MISPRINT664 remains the separate uppercase-A correction. No source-body text changes are required.',
    change={'diplomatic':'Sborik','current':'Sbornik','apparatus_only':True},correction='Sbornik',
    forms=FORMS,is_misprint=True,misprint=True,correction_status='existing paired word correction; apparatus metadata amended',
    related_finding='check/findings/findings_686_690.json#47',evidence_refs=misprint_evidence,
    supersedes=misprint_ref,supersedes_source_id='fixes/MISPRINTS_6.json#665',
    evidence_mode='direct bounded source reinspection plus attributed checker/FIXLOG agreement',
    new_image_read=True,new_image_files=['review/late/images/p688_1.png','review/late/images/w688_1.png'],
    new_review_scope='Bibliography entry17 only; no new full-page certification.',source_body_patch_added=False)
decisions.append(amendment)
save(EVIDENCE/'misprint_665_attribution.json',amendment)
save(EVIDENCE/'attributed_records.json',cache)

pending_ids={d['id'] for d in PENDING}
closure_ids={d['source_id'] for d in decisions[:-1]}
assert pending_ids==closure_ids,(pending_ids-closure_ids,closure_ids-pending_ids)
assert len(decisions)==108 and len(closure_ids)==107
assert len({d['source_id'] for d in decisions})==108
assert sum(d['record_type']=='fixlog' for d in decisions)==99
assert sum(d['record_type']=='rejected_codex' for d in decisions)==8
for d in decisions:
    assert not d['verdict'].startswith('pending')
    assert not d['source_body_patch_added']
    text=json.dumps(d,ensure_ascii=False)
    assert '/workspace/' not in text and '/mnt/' not in text
    assert not re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text)
(OUT/'decisions.jsonl').write_text(''.join(json.dumps(d,ensure_ascii=False)+'\n' for d in decisions))
save(OUT/'validation.json',dict(
    pending_rows=107,covered_pending_rows=107,fixlog_rows=99,rejected_codex_rows=8,
    separate_misprint_attribution_amendments=1,total_dispositions=108,unique_source_ids=108,
    unresolved_pending_source_ids=[],duplicate_source_ids_within_stream=[],
    source_body_patches_added=0,new_full_page_certifications=0,
    bounded_new_image_inspections=[dict(page=261,region='Remarques5.2(i) delimiter string'),dict(page=688,region='Bibliography17 Sborik')],
    attributed_record_count=len(cache),evidence_group_count=40,
    historical_limitation='Nineteen identical elision event rows per log lack individual offsets. Fifteen present occurrences per layer are inventoried; no one-to-one reconstruction is claimed.',
    deliberate_existing_source_id_override=dict(source_id='fixes/MISPRINTS_6.json#665',supersedes=misprint_ref),
    decisions_sha256=sha((OUT/'decisions.jsonl').read_bytes())))
(OUT/'HANDOFF.md').write_text('''# Historical closure handoff

The live stream `review/global_closure/decisions.jsonl` contains **108 attributed dispositions**: all **99** pending FIXLOG rows and **8** page-less rejected Codex rows from checkpoint11, plus the separately requested apparatus attribution amendment for **MISPRINT665**.

No source-body patch or new full-page certification is added. The complete French reviews, English seals and checkpoint inputs remain unchanged. Each closure points to exact existing source-decision records and page certifications; their literal JSON and hashes are retained in `evidence/attributed_records.json`. Forty group packets preserve every original historical payload and explain the disposition of each alias. Every pending canonical ID occurs exactly once in this stream.

## Material outcomes

- Codex241 and245 are closed by the already accepted VI411 total-cohomology and VI415 factor-count corrections, including their complete explicit proofs.
- Codex173 keeps the precise I89 local site-rule correction while rejecting blanket calligraphic normalization. Codex228 accepts the four scan-resolved A-prime transcription repairs and keeps the exact site/object glyph distinctions.
- Codex264 retains the unlabelled first assertion. Codex275 and282 use the already established local paired delimiter repairs. Codex278 retains the balanced label-plus-outer-parenthesis construction, newly re-viewed in both261 images.
- Global macros and scoped glyph records defer to the completed occurrence-specific decisions, including Cart's single rule, plain parf exceptions, Ab fil local expansions, the G/C definitions and the plain geometric Proj occurrence. Historical replacement counts are not presented as newly counted scan occurrences.
- The nineteen identical elision events in each old log have no individual offsets. Their operation is resolved, and all fifteen recoverable present occurrences in each layer are inventoried; a one-to-one reconstruction of the old events remains unavailable and is explicitly not asserted.
- MISPRINT665's copied MAt./Mat. explanation is replaced by its correct Sborik/Sbornik missing-n explanation, with checker686–690#47 and FIXLOG2656 as exact aliases. This intentionally supersedes `review/late/decisions.jsonl#746`; MISPRINT664 is unchanged. The source bodies already contain the proper paired readings.

`validation.json` records exact coverage and hashes. `write_closure.py` regenerates this evidence-only stream from the immutable source records and attached TeX, without editing either.
''')
print(json.dumps(json.loads((OUT/'validation.json').read_text()),ensure_ascii=False,indent=2))
