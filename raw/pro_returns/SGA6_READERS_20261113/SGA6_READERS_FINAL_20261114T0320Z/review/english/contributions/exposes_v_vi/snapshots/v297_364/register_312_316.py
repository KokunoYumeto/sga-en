#!/usr/bin/env python3
"""Record the complete English transfer of folios 312–316."""
from pathlib import Path
import json, sys, hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH, build_records, dump, ROOT
def units(page,layer):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
pairs=json.loads((HERE/'lexical_math_pairs.json').read_text())
pairs=[p for p in pairs if p['page']!=315]
fr=units(315,'current')[25]
assert fr.count(r'\text{pour }')==1 and fr.count(r'\text{si }')==1
pairs.append(dict(page=315,layer='both',French_literal_unit=fr,English_literal_unit=fr.replace(r'\text{pour }',r'\text{for }').replace(r'\text{si }',r'\text{if }'),expected_multiplicity=1,status='individually reviewed lexical translation only',scope='Complete final display defining the filtration image. Only pour/si become for/if; the inclusive bounds, exterior-power glyphs, module underlines, punctuation and every other literal character remain unchanged.'))
dump(HERE/'lexical_math_pairs.json',pairs)
c312,d312=units(312,'current')[35],units(312,'diplomatic')[35]
c316,d316=units(316,'current')[18],units(316,'diplomatic')[18]
assert c312!=d312 and c316!=d316
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=312]
proof=ROOT/'review/expose_v/identification_312.json'
batches.append(dict(expose='V',first=312,last=316,
    native_start='in \\hyperlink{sga6.e05.para.1-7}{1.7} that',
    native_end='\\(\\lambda\\)-rings.\n\\item If \\(A\\) is a ring',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French312–316 in both forms',
    reason='Complete manual reconstruction of universal-polynomial weights,the Todd example,Definition2.1,Examples2.2,Lemma2.2.1,and the first special case. Five native stable targets are retained in sequence; every formula,source typeface and page boundary is preserved,including the displayed continuation of the filtration definition across315/316.',
    variants=[
        dict(id='EN-CONTRIB-V-312-01',page=312,old=c312[2:-2],printed=d312[2:-2],mode='math',source='ASTRA-V-POINT-312'),
        dict(id='EN-CONTRIB-V-316-01',page=316,old=c316[2:-2],printed=d316[2:-2],mode='math',source='check/findings/findings_316_320.json#3')
    ],
    notes=[
        dict(page=312,source_id='ASTRA-V-FORMS-312;ASTRA-V-PLACEHOLDER-312;ASTRA-V-POINT-312',English_rendering='the full universal-polynomial construction and weight interval n through mn',decision='Restore the explicit coefficient names a_j^(i),the general factorization index i,and the upper weight mn omitted or narrowed in native English. Preserve all printed1..k index forms,the repeated source stops after the parenthesized resp. and etc.,and the exact underline around the universal-polynomial name. The separate leading dot before km has an explicit diplomatic/current branch and the exact supporting map packet is linked below.'),
        dict(page=313,source_id='check/findings/findings_311_315.json#16',English_rendering='Now consider',decision='The French maintement/maintenant spelling correction has the same English temporal adverb now in both forms.'),
        dict(page=313,source_id='ASTRA-V-PLACEHOLDER-313;ASTRA-V-FONT-313',English_rendering='all factorization maps,the full additive-example parenthesis,and the Todd character',decision='Restore the twelve source completion placeholders and the full equality of additive functors. The printed capital Phi has no added bar in the induced morphism; retain every source occurrence literally. Preserve plain Q in K=Q,reinforced Z below,and the plain1.16 label. Section refers here to the numbered sections1 and2,as in the earlier terminology record.'),
        dict(page=314,source_id='ASTRA-V-UNDERLINE-314;ASTRA-V-N-314;ASTRA-V-PRODUCT-314;review/expose_v_rendering/patches.jsonl',English_rendering='complete pre-lambda-ring definition and its morphism condition',decision='Preserve exact lexical rules while translating On appelle idiomatically as By a ... we mean. The term itself remains plain. Restore the literal summation with both i≥0 and upper infinity,the three plain N occurrences,the low multiplication stop,and source diagram label positions. The separate rendering stream supplies only the delimiter in i\\in N; no glyph is changed by that transport repair.'),
        dict(page=315,source_id='check/findings/findings_311_315.json#29',English_rendering='which will imply that it factors through',decision='French entrainera/entraînera has the same English verb construction in both forms; no artificial English accent variant is introduced.'),
        dict(page=315,source_id='ASTRA-V-UNDERLINE-315;review/expose_v/page_status.jsonl#page315',English_rendering='complete topos example and locally split exact-sequence lemma',decision='Preserve the locally-direct-summand hypotheses at every occurrence,the source capitalized Module terminology,and all underlined A/E occurrences separately from the printed plain A,E and E-double-prime occurrences. Exterior powers use the literal small wedge. The lemma leaves Let plain; only the source-supported lexical spans are underlined. The inclusive p≥n continuation remains inside the final display and continues onto316.'),
        dict(page=316,source_id='check/findings/findings_316_320.json#2;check/findings/findings_316_320.json#5',English_rendering='When;this is the case',decision='The French ou/où and c’èst/c’est accent repairs give identical English renderings in both forms. Their source glyph observations remain in the French audit.'),
        dict(page=316,source_id='ASTRA-V-WEDGE-316;ASTRA-V-ELLIPSES-316;ASTRA-V-PRODUCT-316',English_rendering='full f_p formula,additivity calculation,and inverse-image paragraph',decision='Restore the Gr^p subscript on the class map,all four low ellipses,the fourteen small exterior wedges,and the low product stop. Retain the exact K^bullet_naif symbols instead of native K-star. The ringed-topos target A! versus A-prime is explicitly branched with the verified structure map and module-pullback identification.'),
        dict(page=316,source_id='review/expose_v/page_status.jsonl#pages312-316',English_rendering='five source boundaries,five native stable targets,and no author notes',decision='Every prose clause and formula position was manually compared against the reviewed French. The itemize environment opens at316 and continues in the next batch; no unmatched environment is silently closed at the folio boundary. No original author note or native continuation macro block occurs in this batch.')
    ],
    extra_records=[dict(record_type='attributed_mathematical_identification',page=312,source_id='ASTRA-V-POINT-312',packet='review/expose_v/identification_312.json',packet_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),decision='The French audit proves the km endpoint by the graded elementary-symmetric injection and the coefficient identity Σq_J=d, d≤Σw_J≤md. This proof supports the explicit punctuation branch; the English author body retains the exact source mathematical statement.')],
    retained_proof_audits=[]))
dump(HERE/'batches.json',batches);build_records()

terms=HERE/'terms.tsv'
rows=[
    'polynôme universel\tuniversal polynomial\tV1.15,p312\tPreserve the source naming and its exact underline span.',
    'composante isobare\tisobaric component\tV1.15,pp312–313\tRetain the weight-qualified source term.',
    'facteur direct\tdirect summand\tV2.2,pp315–316\tUse the module-theoretic term consistently; preserve local and finite-type hypotheses.',
    'Module\tModule\tV2.2,pp315–316\tRetain the printed capital in these sheaf-module passages; mathematical A/E underlines are preserved separately.',
    'localement scindée\tlocally split\tV2.2.1,p315\tPreserve the local condition and its exact sequence.'
]
text=terms.read_text()
for row in rows:
    if row not in text:text+=row+'\n'
terms.write_text(text)
