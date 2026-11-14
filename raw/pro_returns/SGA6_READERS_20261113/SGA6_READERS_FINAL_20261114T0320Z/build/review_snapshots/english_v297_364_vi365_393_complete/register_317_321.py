#!/usr/bin/env python3
"""Record the complete English transfer of folios 317–321."""
from pathlib import Path
import json, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH, build_records, dump
def units(page,layer):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
def variant(page,index,source,mode,suffix='01'):
    c,d=units(page,'current')[index],units(page,'diplomatic')[index]
    assert c!=d
    if mode=='math':c,d=c[2:-2],d[2:-2]
    return dict(id=f'EN-CONTRIB-V-{page}-{suffix}',page=page,old=c,printed=d,mode=mode,source=source)
batches=json.loads((HERE/'batches.json').read_text());batches=[b for b in batches if b['first']!=317]
batches.append(dict(expose='V',first=317,last=321,
    native_start='\\(\\lambda\\)-rings.\n\\item If \\(A\\) is a ring',
    native_end='which are checked by \\hyperlink{sga6.e05.thm.1-10}{1.10} on the elements',
    source='review/expose_v/FROZEN_HANDOFF.md; reviewed French317–321 in both forms',
    reason='Complete reconstruction of the representation-ring example,the formal-series multiplication and operations,Definition2.4,and Examples2.5 through the two diagrams. All ten native stable targets remain in order,including the nonprinting2.4.3 target although the source second formula has no printed number. Every unit symbol,nested functor argument,bound,and map label is transferred literally.',
    variants=[
        variant(317,28,'check/findings/findings_316_320.json#11','display'),
        variant(318,2,'check/findings/findings_316_320.json#12','text'),
        variant(318,8,'check/findings/findings_316_320.json#13','text','02'),
        variant(320,21,'check/findings/findings_316_320.json#26','math'),
        variant(321,21,'check/findings/findings_321_325.json#4','display')
    ],
    notes=[
        dict(page=317,source_id='check/findings/findings_316_320.json#8;check/findings/findings_316_320.json#9',English_rendering='a Z-bilinear morphism of functors;by means of the element',decision='The redundant French de and omitted definite article produce the same idiomatic English adjective and definite-noun constructions in both forms. The exact operation specified by1+XYt and2.3.1 is unchanged; no artificial English grammar errors are introduced.'),
        dict(page=317,source_id='review/expose_v/page_status.jsonl#page317;check/findings/findings_316_320.json#11',English_rendering='lambda-rings continuation,representation example,and multiplication definition',decision='The top continuation is lambda-rings without an added pre-prefix. Preserve the printed plain A in(T,A),lowercase modules in this item,plain2.3 label,and the capital identity command at its observed label position. Its surplus colon is explicitly branched in the complete diagram. Elementary is retained here because it is actually present in this source paragraph.'),
        dict(page=318,source_id='check/findings/findings_316_320.json#12;check/findings/findings_316_320.json#13;check/findings/findings_316_320.json#16',English_rendering='the independent universal pair,P_2,and composed with itself',decision='The repeated-X versus independent-Y pair and lowercase-p versus capital-P name each have separate literal branches. The French lui même/lui-même compound spelling renders identically as itself. Restore the source standalone P_2 reference,all reinforced Z occurrences,and both underlined unit symbols. The folio ends with we before shall choose on319.'),
        dict(page=319,source_id='review/expose_v/page_status.jsonl#page319',English_rendering='full nested-functor construction,filtration,and coefficient definition',decision='Retain the literal Ghat^u∘Ghat^t object,all floor brackets,low ellipses and both underlined units. Preserve the original plain1 in the generic series but the underlined1 in its defining operation. The separate Q_{2,2} reference before the next-page display is restored. No mathematical token is inferred from the shortened native prose.'),
        dict(page=320,source_id='check/findings/findings_316_320.json#26;review/expose_v/page_status.jsonl#page320',English_rendering='full exterior-power motivation and lambda-ring definition',decision='Restore underlined E/F,the exact composite Ghat^u(lambda_t)(lambda_u(E)),all source semicolons,and the complete definition underline groups. The two operations identities retain the single printed2.4.2 label and no added2.4.3 number; the native nonprinting stable target remains beside the corresponding formula. The i.j/i,j separator has an explicit branch,retaining the reinforced N in both forms.'),
        dict(page=321,source_id='check/findings/findings_321_325.json#4;review/expose_v/page_status.jsonl#page321',English_rendering='terminology paragraph and full first two examples through their diagrams',decision='Retain all five lambda tokens in the terminology explanation,all underlined units,low product stop in the final inline unit identity,and the binomial-product low ellipsis. The missing parenthesis in the product vertex is explicitly branched with its exact lambda_u×lambda_u target identification. Both lower horizontal diagram labels retain their source placement.'),
        dict(page=321,source_id='review/expose_v/page_status.jsonl#pages317-321',English_rendering='five exact folio boundaries,ten native stable targets,and no author notes',decision='Every prose clause,formula and its placement was manually compared with the reviewed French. The first page closes the preceding itemize;321 opens an enumerate that continues onto322. No author-note call/text or native continuation macro block occurs in this batch.')
    ],retained_proof_audits=[]))
dump(HERE/'batches.json',batches);build_records()
