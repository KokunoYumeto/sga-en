"""Record directly viewed pp.31–35 and native witness42 detail."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['after (1.22bis), la composante','The article la lies outside the underline; the rule begins at composante. The attached split matches.'],
2:['formula (1.26), target','One large hat spans A⊗Q, including the tensor product and Q. This was also directly viewed in native witness42. The attached widehat{A⊗Q} preserves the scope.'],
3:['formula (1.26), connecting rule','Both the primary image and native witness42 show a horizontal rule with a clean right end and no arrowhead. Preserve the headless rule diplomatically; current supplies the arrow for the stated homomorphism ch.'],
4:['homomorphisme d’anneaux augnentés','The printed word has n in place of the first m. The corrected word is augmentés; current still needs this correction.'],
5:['défini sans ambiguité','The printed i has one dot and no diaeresis, also visible in native witness42. Current already has ambiguïté; NOTE_6 accepts the regularized diaeresis.'],
6:['endomorphisme additif de widehat(A⊗Q)','The hand-drawn hat extends over all three elements A, tensor sign and Q. The attached widehat scope is correct.'],
7:['isomorphisme ... sur l’anneau widehat(A⊗Q)','The hat again spans A⊗Q; in the nearby source ring A-tilde⊗Q, tilde covers A alone. The attached target matches.'],
8:['additive homomorphism from 1+Ahat-plus','The left hat covers A alone, while the target hat spans A⊗Q inside parentheses and the plus lies outside. The attached scopes match.'],
9:['formula (1.28), ending','There is no terminal stop after x^i. The attached formula correctly runs into on a alors.'],
10:['line following (1.28)','The first letter is lowercase o in on a alors; the attached text matches.'],
11:['Proposition1.3, parenthesis before Si l’on pose','The parenthetical on a N^i=0 pour i>q is plain; the rule resumes at Si l’on pose. The attached emphasis boundary matches.'],
12:['Proposition1.3, second finite sum','The upper limit is visibly n. The proposition defines N with rankq and components throughN^q; Proposition1.2 gives λ^i(N)=0 for i>q. No n is defined here. Correct the upper bound to q in current.'],
13:['six Todd symbols p32 and formula(1.30bis) p33','The glyph has a looped top stroke and descending curved stem; the sentence expressly identifies it as the initial of Todd. It is script T. Replace the six mathcal C occurrences on inspected p32 and the one on inspected p33 by mathcal T; later occurrences remain for direct inspection.'],
14:['p33 before formula(1.32)','No colon follows en posant. The attached text omits it.'],
15:['formula(1.32), ending','No terminal full stop follows the closing parenthesis. The attached display matches.'],
16:['notre anneau A en est un complèté','The first e has a grave and the last an acute. Correct the first to acute, complété, in current.'],
17:['Theorem1.4, est un polynôme, isobare','The word polynôme and its following comma lie outside the underline; est un and isobare de have rules. The attached split matches this.'],
18:['p33 last line, de N^p dans N. On','The word de is plain; dans has an underline; the final On is plain. The attached boundaries and position of On match.'],
19:['boundary pp33/34','The final word of p33 is On; p34 begins fait opérer. Both attached markers are correctly placed.'],
20:['p34 first words','The underline starts at fait, after the plain On ending p33. The attached emph begins at fait.'],
21:['p34 first sentence after N^(p)','There is no comma between N^(p) and the following donc sur. The attached comma removal is confirmed.'],
22:['proof, quotient λ^p(N,1)','The quotient is inline, followed by est une série on the same printed line. The attached text is now inline with the same formula and punctuation; the layout choice adds no content variant.'],
23:['proof, ℓ^p(N) opening','The expression follows l’élément in the running text. The attached inline opening now matches, with its mathematical parentheses assessed separately.'],
24:['proof, ℓ^p(N) closing','The comma and où maintenant immediately follow the inline K(G) expression. The attached inline closing matches.'],
25:['proof, E_G((Λ(N^(p))^alt)','The print leaves the inner grouping around Λ(N^(p)) unclosed before alt. Current adds the missing close so that alt applies to Λ(N^(p)), as in the complete displayed expression(1.33).'],
26:['boundary pp34/35','Page34 ends s’identifie; p35 starts au sous-anneau. The attached marker correctly precedes au.'],
27:['p35 first paragraph, ℓ^p(N)λ_{−1}(N) identity','The identity is inline, followed by Comme on est on the same printed line. The attached inline formula now matches the mathematical and punctuation tokens; no new layout edit is made.']}
save('evidence_031_035.json',{'findings_031_035.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind,count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(31,'current',"d'anneaux augnentés","d'anneaux augmentés",'fixes/MISPRINTS_6.json#67',e[4][1],'misprint_correction')
patch(32,'current',r'\sum_{i=0}^{n}(-1)^i\lambda^i(N)',r'\sum_{i=0}^{q}(-1)^i\lambda^i(N)','fixes/MISPRINTS_6.json#69',e[12][1],'misprint_correction')
patch(33,'current','un complèté','un complété','fixes/MISPRINTS_6.json#70',e[16][1],'misprint_correction')
patch(32,'both',r'\mathcal C',r'\mathcal T','check/findings/findings_031_035.json#13',e[13][1],'symbol',6)
patch(33,'both',r'\mathcal C',r'\mathcal T','check/findings/findings_031_035.json#13',e[13][1],'symbol')
patch(31,'both','être tel que les\n','être tel que les com%\n','ASTRA-EARLY-0010','The last printed line ends com-; put this syllable before the marker with percent to join the complete word across it.','marker')
patch(32,'both',r'composantes de $\ch(x)$',r'posantes de $\ch(x)$','ASTRA-EARLY-0010','The first printed line begins posantes, completing com- from p31.','marker')
patch(34,'current',r'(\S 2, théorème 1.3)',r'(\S 2, théorème 1.1)','ASTRA-EARLY-0011','The cited representation-ring result in §2 is Theorem1.1 on p26 with its corollary p27. Proposition1.3 on p32 concerns the Chern/Todd identity and is in §3.','misprint_correction')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',31,'ASTRA-EARLY-0010','p31 com- / p32 posantes','folio boundary','The complete word composantes crosses the printed page boundary. The attached marker places the complete word underp32. Split it as com% before the marker and posantes after, preserving the rendered word.',{'page31':'les com%','page32':'posantes'},'not applied and now applied',related_pages=[31,32])
rec('own_finding',34,'ASTRA-EARLY-0011','(§2, théorème1.3)','last sentence of the proof portion on p34','The scan clearly prints1.3. The result in §2 identifying the representation ring is Theorem1.1 (p26) and its corollary (p27), both directly viewed. The result numbered1.3 is a proposition in §3 concerning ch(λ_{−1}(N)) (p32). Restore the reference1.1 in current.',{'old':'théorème1.3','new':'théorème1.1'},'not applied and now applied',related_pages=[26,27,32,34])
save('extra_decisions.json',records)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_031_035.json').read_text())
beg={31:'La formule (1.22)',32:'posantes de ch(x)',33:'ce qui équivaut à',34:'fait opérer',35:'au sous-anneau'}
for p in range(31,36):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p==31,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='Body, displays and note on p35 fully compared. Native witness42 additionally read for the p31 wide-hat scope, headless rule and dotted i.'))
save('extra_pages.json',pages)
over=load('record_overrides.json');over['check/findings/findings_031_035.json#13']={'related_pages':[32,33],'change':'Inspected p32 six occurrences and p33 one occurrence: mathcal C→mathcal T in both layers. Later listed pages not yet certified.'};save('record_overrides.json',over)
