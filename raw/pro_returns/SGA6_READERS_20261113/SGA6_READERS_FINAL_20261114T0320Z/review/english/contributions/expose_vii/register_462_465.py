#!/usr/bin/env python3
"""Register the final manually compared VII462–465 translation."""
from pathlib import Path
import json,sys,re,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from contribution import MATH,ROOT
def units(page,layer='current'):
    return [m.group() for m in MATH.finditer((HERE/'source_packets'/str(page)/f'{layer}.tex').read_text())]
variants=[]
def add(n,page,old,printed,source,mode='text'):
    variants.append(dict(id=f'EN-CONTRIB-VII-{n:03}',page=page,old=old,printed=printed,mode=mode,source=source))
add(78,462,'Taking (4.8.1) into account, we therefore obtain:','Taking (4.6.1) into account, we therefore obtain:','fixes/MISPRINTS_6.json#419')
add(79,465,r'the exact sequence (IV\qquad):',r'the exact sequence (IV\qquad:','fixes/MISPRINTS_6.json#423')
c,d=units(465),units(465,'diplomatic')
add(80,465,'Consequently, '+c[41]+' can be expressed','Consequently, '+d[41]+' can be expressed','fixes/MISPRINTS_6.json#424')
add(81,465,c[46],d[46],'fixes/MISPRINTS_6.json#425')
native=(ROOT/'review/english/SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
fr=(HERE/'source_packets/465/current.tex').read_text()
pattern=re.compile(r'\\providecommand\{\\etale\}.*?\\providecommand\{\\Ch\}\{\\operatorname\{Ch\}\}',re.S)
frblock=pattern.search(fr).group();end=native.index(r'\sgaStableTarget{sga6.e08.expose}');nativeblock=list(pattern.finditer(native[:end]))[-1].group();assert frblock==nativeblock
config=dict(expose='VII',first=462,last=465,
  native_start=r'\hyperlink{sga6.e07.eq.4-6-1}{(4.6.1)}, we get',
  native_end=r'\sgaStableTarget{sga6.e08.expose}',
  source='review/expose_vii/HANDOFF.md and final_audit.json; exact reviewed French462–465, plus the430 postfreeze note amendment already transferred',
  reason='Completes the graded-kernel and surjectivity proofs, all quotient-class bars and ordered pairs, the complete topological-filtration argument and bibliography. Blank source locators and the unresolved integral-lift strength remain with their exact independent audits; only the source-authorized locator, closing parenthesis and final supported class receive variants.',
  variants=variants,retained_proof_audits=['ASTRA-VII-0136','ASTRA-VII-0137'],notes=[
    dict(page=462,source_id='complete quotient-class and filtration proof',decision='Restore every composite/grouping and the exact class bars on z and1−L, the full difference z−g^*(z-prime)lambda_(−1)(F) in Fil^k, and the final VI5.11 argument with all rational coefficients. Native English had changed bars into primes and the difference into an equality; both source forms are now literal. The first opening locator is printed4.8.1 in both forms, whereas the later printed4.6.1/current4.8.1 is explicit078. Only the text phrase by3.4 within its complete display is translated by an exact lexical pair.'),
    dict(page=463,source_id='complete filtered-surjectivity argument',decision='Restore the entire decomposition x-prime=f^*f_*x-prime+j_*y-prime, exact degree-k product filtration and homomorphism labelv, gamma^k(x-prime_1), the ordered pair in the gamma-star formula, and both final filtration degrees. Native English had replaced several k degrees by1 and omitted the second tuple component; all are restored literally in both forms. French entraine/entraîne renders implies unchanged.'),
    dict(page=464,source_id='ASTRA-VII-0136 and complete topological-filtration introduction',decision='Restore i^gr/i_gr in the source order, the raised bullet on c(N), the explicit lambda filtration subscript, all topological-support definitions, the N.B. parenthesis and full noetherian-induction setup. Preserve all three unfinished source locators and their exact blank spacing/delimiters; native English had suppliedIV2.12 or omitted blanks. The retained source packet provides candidate maps without filling the missing literal references. French intégres/intègres and montrons la/montrons-la render integral and prove it unchanged. Soir/Soit is the single-letter error in the variable-introduction syntax J the Ideal of O_X followed by defining Z; English renders Let in both, with the French source typo explicitly retained in this ledger rather than inventing an English evening statement.'),
    dict(page=465,source_id='ASTRA-VII-0137 and final supported-class correction',decision='Restore the complete regular-sequence construction, exact restriction J|U, codimension formula, localization sequence and all ensuing integral/rational classes. Preserve the source integral x lift and y∈j_*K(Z-prime) without adding Q or a denominator-clearing hypothesis; the stronger lift remains separately audited as unresolved in ASTRA-VII-0137. The blankIV locator remains blank, with only its closing parenthesis changed in079. Final x→y statements are explicit080/081 with the source localization and support proof. Restore the full final k+1 bound. Bibliography heading capitals and the complete plain Cartan–Eilenberg title follow the reviewed source.'),
    dict(page=465,source_id='native and reviewed pre-VIII continuation macros',decision='Retain both etale and Ch definitions at their actual465/466 boundary. The complete native and reviewed command blocks are byte-identical, so one preserved copy represents both exact inputs. The final replacement span ends immediately before sga6.e08.expose, leaving the VIII contributor’s start intact.',native_and_French_macro_sha256=hashlib.sha256(frblock.encode()).hexdigest(),macro_tokens=[r'\etale',r'\Ch'])
  ])
p=HERE/'batches.json';a=json.loads(p.read_text());a=[x for x in a if x['first']!=462];a.append(config);a.sort(key=lambda x:x['first']);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print('Registered VII462–465:4 source-variant groups; complete50-folio exposé and boundary macros.')
