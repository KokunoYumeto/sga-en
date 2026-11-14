#!/usr/bin/env python3
"""Register the manually compared VII447–451 translation."""
from pathlib import Path
import json,sys,hashlib,re
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT
def units(page,layer='current'):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
variants=[]
def add(n,page,index,source,mode='text',related=None):
    c,d=units(page),units(page,'diplomatic')
    entry=dict(id=f'EN-CONTRIB-VII-{n:03}',page=page,old=c[index],printed=d[index],mode=mode,source=source)
    if related:entry['related_sources']=related
    variants.append(entry)
add(51,447,27,'ASTRA-VII-0095','display',['check/findings/findings_446_450.json#9'])
for n,index in [(52,6),(53,9),(55,28),(56,29)]:add(n,449,index,'ASTRA-VII-0097')
add(54,449,17,'ASTRA-VII-0098')
for n,index in [(57,4),(58,5),(59,7),(60,9),(62,19),(63,23)]:add(n,451,index,'ASTRA-VII-0102')
add(61,451,17,'fixes/MISPRINTS_6.json#439')
variants.sort(key=lambda x:x['id'])
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
fr=(HERE/'source_packets/447/current.tex').read_text()
macro_pattern=re.compile(r'\\providecommand\{\\Q\}.*?\\providecommand\{\\cO\}\{\\mathcal O\}',re.S)
frblock=macro_pattern.search(fr).group()
pos=native.index(r'\sgaStableTarget{sga6.e07.remark-3-8}')
nativeblock=list(macro_pattern.finditer(native[:pos]))[-1].group()
assert frblock==nativeblock
config=dict(expose='VII',first=447,last=451,
  native_start=r"Therefore coherent modules on \(X'\) with support in \(Y'\) are perfect.",
  native_end=r"Now \(\lambda^p(\xi,p^*(i_*(y)))-\lambda^p(1,p^*(i_*(y)))\) is divisible by \(1-\xi\).",
  source='review/expose_vii/HANDOFF.md and final_audit.json; exact reviewed French447–451',
  reason='Restores the complete perfect-support and finite-filtration proof, all source sheaf/class distinctions, the precise section and conormal construction, and every step of the lambda-operation reduction and Jouanolou lemma. The corrected counit triangle has a single complete display branch carrying its separate source direction and glyph audits. The ambiguous ideal sentence remains with the exact conormal-map audit.',
  variants=variants,retained_proof_audits=['ASTRA-VII-0099'],notes=[
    dict(page=447,source_id='ASTRA-VII-0095 and complete supported-class proof',decision='Restore the source comparison of Grothendieck groups on Y-prime, the local perfectness argument, every step of the finite J-adic filtration and support calculation. The complete triangle is atomic variant051: its three corrected arrows come from the explicit counit evaluation and mapping cone in ASTRA-VII-0095, while its L/R glyph pair is separately sourced to checker446450#9. Both author bodies keep the cyclic convention and no new shift label. The exact concluding class x−f*f_*x and support argument follow the source.'),
    dict(page=447,source_id='native and reviewed continuation macro packet',decision='Retain the complete13-definition continuation block at its original boundary before Remark3.8. The native and reviewed command block are byte-identical, so the one preserved copy represents both inputs; no renewal or changed expansion is needed.',native_and_French_macro_sha256=hashlib.sha256(frblock.encode()).hexdigest(),macro_tokens=re.findall(r'\\providecommand\{(\\[A-Za-z]+)\}',frblock)),
    dict(page=448,source_id='complete Remark3.8 and Lemma4.1',decision='Restore the full additive/multiplicative/lambda description, rational qualifier and original author parenthesis, all statement word-group rules, both congruence lines and the complete exterior-power calculation. The source noet-with-diaeresis-hérien spelling and corrected noethérien both render noetherian; no artificial English accent error is introduced. Preserve every class symbol plain and each separately ruled sheaf letter exactly.'),
    dict(page=449,source_id='ASTRA-VII-0099 and complete section/conormal construction',decision='Restore the quotient by the last r coordinates, full graded coordinate algebra, I/I² expression and source phrase corresponding ideal without replacing it by conormal. The exact quotient/basis maps and ambiguity are attributed separately to ASTRA-VII-0099. Preserve the complete iterated projective-space alternative; the native English had incorrectly reduced it to a single P1. All five P glyphs are covered by four exact unit branches052/053/055/056; the subscript p/P is independent054. Restore the exact theorem statement, source mod.-torsion underlines and all quantifiers.'),
    dict(page=450,source_id='complete lambda reduction and self-intersection identities',decision='Restore both full3.4 computations with their literal inline references rather than invented equation tags, the entire V5.4.2 formula, exact z=j^*(u-prime) and u-prime=j_*(z-prime), the three-term sheaf sequence and printed j_*(1)=1−J-prime. Preserve all native target IDs at the corresponding actual expressions. Both source branches are identical on this page, so no formula variant is fabricated.'),
    dict(page=451,source_id='complete descent and Jouanolou lemma',decision='Restore both successive projective sections, the author’s punctuation after4.1., every descent stage, the full lemma with precisely the printed hypothesis on s composed with i, and the attribution J.P.Jouanolou. Restore the complete projection calculation and both final congruence lines. The inherited native additional hypothesis and for s is absent from the source and is removed in both forms. The O_p(−1) source variant is061 with its explicit multiplication-by-coordinate sheaf map; all other eight P occurrences are covered by the six complete-unit branches057–060/062/063. Source mod. torsion remains literal English mathematical terminology.')
  ])
p=HERE/'batches.json';a=json.loads(p.read_text());a=[x for x in a if x['first']!=447];a.append(config);a.sort(key=lambda x:x['first']);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print('Registered VII447–451:13 complete-unit variant groups; native/reviewed boundary macros identical.')
