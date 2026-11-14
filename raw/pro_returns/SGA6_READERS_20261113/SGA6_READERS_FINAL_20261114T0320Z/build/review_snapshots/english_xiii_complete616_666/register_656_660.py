from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from contribution import make_chunk
make_chunk('XIII',656,660)
b=json.loads((H/'batches.json').read_text());b=[x for x in b if x['first']!=656]
u=lambda p:json.loads((H/'source_packets'/str(p)/'units.json').read_text())
v=[]
def add(p,old,printed,s,mode='text'):v.append(dict(id=f'EN-CONTRIB-XIII-{len(v)+35:03}',page=p,old=old,printed=printed,source=s,mode=mode))
add(656,u(656)[21],u(656)[21].replace('{O}_P','{O}_X'),'ASTRA-XIII-0046')
add(657,u(657)[3],u(657)[3].replace('F_q(-1))','F_q(-1)'),'fixes/MISPRINTS_6.json#613')
add(657,u(657)[28],u(657)[28].replace('^{(r-q+1)}','^{(r-q)}'),'ASTRA-XIII-0047')
add(657,u(657)[29]+' and '+u(657)[30],u(657)[29]+' and $a_q^{(q)}$ and '+u(657)[30],'fixes/MISPRINTS_6.json#614')
add(657,u(657)[32],u(657)[32].replace('F(-1)','F(-1'),'fixes/MISPRINTS_6.json#615')
add(660,u(660)[19],u(660)[19].replace('{O}_Z(-Z)','{O}_X(-Z)').replace('{O}_{X_n}','{O}_X'),'ASTRA-XIII-0048')
end=r'\sgaStableTarget{sga6.e13.cor.6-14}'
s=(H.parents[1]/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text();assert s.count(end)==1
b.append(dict(expose='XIII',first=656,last=660,native_start=b[-1]['native_end'],native_end=end,source='Both exact reviewed French656–660 packets and frozen XIII source/proof decisions.',reason='Restore full6.5–6.8 proofs, precise polynomial argument/index families, complete positive-cycle definition and degree bounds, and the double-divisor example. The current double-divisor correction identifies I/I² as its kernel and O_Y/I² as its middle term, while all printed subscripts remain diplomatic.',variants=v,notes=[dict(page=657,topic='Polynomial-family indexing',decision='ASTRA-XIII0047 transfers only the approved r−q→r−q+1 superscript correction. The defining A_i^(q) family has q+1 coefficient slots; the displayed c_(q−1),...,c_r list has r−q+2 slots. All source arguments and stated index ranges remain literal.'),dict(page=660,topic='Exact double-divisor sequence',decision='ASTRA-XIII0048 is a complete-unit current branch with both repaired subscripts: the quotient map O_Y/I²→O_Y/I has kernel I/I²≅O_Z(−Z), I=O_Y(−Z). The printed O_X(−Z) and O_X are both retained diplomatically. The distinct Cartier sequence0→O_Y(−Z)→O_Y→O_Z→0 is related via these quotient ideals, as documented in the source audit, and is not substituted for the author’s double-divisor calculation.'),dict(page=660,topic='Consequential prose retained',decision='ASTRA-XIII0049 restores d’où que in both French layers; the English hence renders this same consequence in both forms, with no invented English variant.'),dict(page=658,topic='Nested defined terms',decision='Retain the exact nested emphasis boundaries for special positive k-cycle, integral and degree in the raw contribution. Their observed plain/ruled treatment awaits the separately assigned global convention amendment and will not alter the literal mathematical source bases.'),dict(page=657,topic='Proof completion',decision='The full induction defining A_0,...,A_r and its explicit F_q-for-F specialization are present; no native proof abbreviation is retained.')]))
(H/'batches.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
