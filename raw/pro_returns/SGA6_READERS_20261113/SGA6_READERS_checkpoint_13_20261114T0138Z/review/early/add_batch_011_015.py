"""Record the pp. 11–15 images personally compared in this review."""
from pathlib import Path
import json

R=Path(__file__).resolve().parents[2]
O=Path(__file__).resolve().parent
def load(n): return json.loads((O/n).read_text())
def save(n,a): (O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')

e={
1:['equation number (4.1)','The interdigit point is lost in this impression, as in earlier numbered references. Retain the restored stop under NOTE_6.'],
2:['exterior differential below (4.1)',"The denominator is visibly X in d_{X′/X}; the target is Ω¹_{X′/Y}. The differential into Ω¹_{X′/Y} is the universal Y-relative derivation d_{X′/Y}, restricted to J. Correct that index in the current layer."],
3:['heading 4.4.','A separate trailing point follows the second 4.'],
4:['et le complexe de chaines','The word has the ordinary dotted i and no circumflex; checked again in a 360 dpi crop. Retain chaines diplomatically and supply chaînes in current.'],
5:['§4.4, apparait comme quotient','The print reads apparait, with a dotted i. The corrected spelling requires apparaît.'],
6:['first line, non recollables / Voici','Voici follows on the same line without a paragraph indent. The stop after recollables is a weak or absent impression, retained under the documented faint-punctuation convention.'],
7:['display phi:C=A[T]→B','The phi is a closed handwritten oval crossed by a stroke. The attached phi command matches it.'],
8:['Soit J le noyau de phi','The same closed phi shape occurs in the following sentence.'],
9:['A(U)-algèbre commutative libre engendré','The printed participle ends é, with no additional e. Its noun algèbre is feminine; the preceding occurrence in the same sentence already prints engendrée.'],
10:["défini par l'homomorphisme naturelle",'The print has naturelle. The adjective modifying the masculine noun homomorphisme is naturel, already in current.'],
11:['complexe de chaines de longueur 1','The printed i is dotted with no circumflex. Keep the print diplomatically and restore chaînes in current.'],
12:['complexe cotangent relatif L de X sur Y','The rules underline the word groups complexe cotangent, relatif, de, and sur, with the mathematical symbols outside the rules. This is submitted to the volume-wide mixed text/formula underline convention.'],
13:['two subscripts naif in the following paragraph','Both subscripts are printed naif without the two dots. The corrected form is naïf; the same spelling decision applies to both occurrences.'],
14:['heading 4.5.','A trailing full stop is visible after 5.'],
15:['les sections qui précédent','The printed e accents are both acute; the verb form is précèdent. The attached current form already has the second accent grave.'],
16:['page 12 last line / page 13 first line','Page 12 ends corps; page 13 begins the complete word algébrique. The attached markers now split at that word boundary.'],
17:['page 13 first line','The print reads algébrique clos. The adverb modifying clos is algébriquement; this is still unapplied in current.'],
18:['page 13 last line / page 14 first line','Page 13 ends Atiyah-Hirzebruch; page 14 begins [1] un. Both attached markers are now correctly placed.'],
19:['page 14 first line','The print has homomorphisme groupes, without de. The current layer supplies the missing connecting word.'],
20:['paragraph after (5.2), Grauert [4]','The reference is visibly [4]. The bibliography on p. 19 was directly viewed: Grauert is entry [3], whereas [4] is Grothendieck, Classes de faisceaux / RRR. Current already supplies [3].'],
21:['diagram (5.3), left vertical label','The left f_* sits to the left of its arrow; the attached array now puts it on that side.'],
22:['Shih [7] et Atiyah','The reference is visibly [7]. Direct inspection of the p. 19 bibliography identifies W. Shih as entry [6]. The current layer already has [6].'],
23:['où les flêches horizontales','The accent over the first e is a circumflex. Retain flêches diplomatically and the corrected grave in current.'],
24:['first line, première flêche','The accent over flêche is visibly circumflex; première beside it has a grave. Both attached layers correctly distinguish printed and corrected accents.'],
25:['second line, cohomologie rationelle','The print has one n in rationelle. Current already has rationnelle.'],
26:["§6, l'existence a été signalé",'The participle visibly lacks a final e. Its subject existence is feminine; retain the attached current signalée.'],
27:['filtration paragraph, Filt_i K_dot(X)','The printed operator spells Filt with final t. The attached operatorname{Filt} restores it.'],
28:['dim supp.F≤i','There is a baseline point between supp and F. The attached transcription preserves it.'],
29:['formula (6.1), first two operators','Both operators spell Filt, including t. The attached layer already spells out both operators.'],
30:['formula (6.1), final operator','The last operator also spells Filt; the subscript is j−i.'],
31:['formula (6.1), Filt_j(K_dot(X)','A round opening parenthesis stands immediately after Filt_j and is never closed. The current layer removes that superfluous opening parenthesis.'],
32:['last body paragraph, équivalence rationelle','The second occurrence again has only one n; the attached current rationnelle is correct.']}
save('evidence_011_015.json',{'findings_011_015.json':e,'findings_006_010.json':{34:['page 10 last line / page 11 first display','Page 10 ends with de définir une théorie des classes de Chern; page 11 begins the display T_f∈K•(X). The attached folio-11 marker correctly precedes this display.']}})

patches=load('extra_patches.json')
def patch(p,old,new,idx,reason):
 patches.append({'page':p,'layer':'current','old':old,'new':new,'source_id':idx,'reason':reason,'kind':'misprint_correction'})
patch(11,r"d_{X'/X}:\underline J",r"d_{X'/Y}:\underline J",'fixes/MISPRINTS_6.json#45',e[2][1])
patch(11,'complexe de chaines',r'complexe de cha\^{\i}nes','fixes/MISPRINTS_6.json#46',e[4][1])
patch(11,'apparait comme quotient',r'appara\^{\i}t comme quotient','fixes/MISPRINTS_6.json#47',e[5][1])
patch(12,r"libre engendr\'e par $T(U)$",r"libre engendr\'ee par $T(U)$",'fixes/MISPRINTS_6.json#48',e[9][1])
patch(12,'complexe de chaines de longueur',r'complexe de cha\^{\i}nes de longueur','fixes/MISPRINTS_6.json#50',e[11][1])
patch(12,r'\mathrm{naif}',r'\text{na\"{\i}f}','fixes/MISPRINTS_6.json#51',e[13][1])
patch(13,r"alg\'ebrique clos de caract",r"alg\'ebriquement clos de caract",'fixes/MISPRINTS_6.json#53',e[17][1])
patch(12,r'Cel\`a est donc','Cela est donc','ASTRA-EARLY-0003','A grave accent is visibly printed on the final a of Celà. The demonstrative pronoun is Cela; retain Celà diplomatically and correct it in current.')
save('extra_patches.json',patches)

records=load('extra_decisions.json')
def rec(typ,p,idx,printed,region,reason,change,verdict='confirmed',**kw):
 records.append(dict(record_type=typ,page=p,source_id=idx,verdict=verdict,printed_reading=printed,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',12,'ASTRA-EARLY-0003','Celà est donc','paragraph before 4.5.','A grave accent is visible on the final a. The demonstrative pronoun Cela has no accent.',{'old':r'Cel\`a est donc','new':'Cela est donc'},'not applied and now applied',kind='misprint_correction')

# The source files use earlier folio boundaries; record the actual scan page.
hold={
4:(1,'introductif','introductive','The printed adjective is introductif; nature is feminine.'),
5:(1,'coéfficients','coefficients','The print has an acute over the first e; corrected spelling removes it.'),
6:(2,'débarasser','débarrasser','The printed single r is confirmed; current supplies the missing r.'),
7:(3,'sous-schémas fermé','sous-schéma fermé','The print has plural s after the singular article; current corrects agreement.'),
8:(3,'quasi-porjectifs','quasi-projectifs','The print transposes r and o.'),
9:(3,'coprs','corps','The print transposes p and r.'),
10:(4,'tranformant','transformant','The scan first word lacks s; its actual folio is 4.'),
11:(4,'j=i','j≤i','The print has equality. The coefficient identity gamma_i(x)=sum_{1≤j≤i} binomial(i−1,j−1)lambda^j(x) supplies the corrected range.'),
12:(6,'formule (2.2)','formule (1.2)','The scan prints (2.2); the paragraph extends the Riemann–Roch formula (1.2), so retain the HOLD correction in current. The actual folio is 6.'),
13:(6,'servie','servi',"The print has servie; the passé composé avait servi takes the uninflected participle here."),
14:(6,'cl•(E)=sum_i(−1)^i cl•(R^if_*(F))','cl•(F)=sum_i(−1)^i cl•(R^if_*(F))','The printed left variable E differs from the input F in every derived image; the current correction identifies the common input F.'),
15:(7,'K•(X)→K(Parf(Y))','K•(Y)→K(Parf(Y))','The paragraph constructs the map from locally free Y-modules to perfect complexes on Y; its source is K•(Y). The print has X.'),
16:(8,'sous-schémas; insersection','sous-schéma; intersection','Both printed spellings are directly visible; the current layer corrects the singular noun and the transposition.'),
17:(10,'définition ... adopté','définition ... adoptée','The printed participle lacks e; definition is feminine. The actual folio is 10.'),
18:(10,'question ... tiré','question ... tirée','The printed participle lacks e; question is feminine. The actual folio is 10.'),
19:(12,'homomorphisme naturelle','homomorphisme naturel','The printed adjective has lle; homomorphisme is masculine. The actual folio is 12.'),
20:(14,'homomorphisme groupes','homomorphisme de groupes','The printed line omits de. The actual folio is 14.'),
21:(15,'cohomologie rationelle','cohomologie rationnelle','The print has single n; the current layer supplies the second n.'),
22:(15,'existence ... signalé','existence ... signalée','The print lacks the feminine agreement e.'),
23:(15,'Filt_j(K_dot(X)','Filt_j K_dot(X)','The opening parenthesis after Filt_j has no close; current removes it.'),
24:(15,'équivalence rationelle','équivalence rationnelle','The second printed rationelle again has single n.')}
for n,(p,pr,cor,reason) in hold.items():
 rec('hold_difference',p,f'fr/codex/HOLD_VS_CORR.json#{n}',pr,'HOLD/CORR differing words at the stated folio',reason,{'diplomatic':pr,'corrected':cor},'amended' if n in (12,14,15) else 'confirmed')

rec('codex_reconciliation',8,'fixes/RECONCILE_CODEX_6.json#164','p3 défini par (2.1); p8 par la formule (2.1)','references to the construction of T_f','The record combines two locations. On p3, défini par (2.1) can refer to the displayed factorization used in the definition and is retained. On p8, the explicit word formule points to (2.1), but that display is the factorization X→X′→Y; the cotangent-class formula is (2.2). Correct only p8.',{'page3':'retain (2.1)','page8':'(2.1)→(2.2)'},'amended',codex_id='SGA-SRC-001468',related_pages=[3,8])
rec('codex_reconciliation',4,'fixes/RECONCILE_CODEX_6.json#169',r'cl(O_Z),) dont','page 4 first line','The comma is visibly inside the closing parenthesis. The proposal deletes source punctuation without repairing an incomplete formula or changing the mathematical reference; retain the printed parenthetical punctuation and confirm the prior non-application.','No change; rejected edit remains rejected.',codex_id='SGA-SRC-001473')
rec('codex_reconciliation',15,'fixes/RECONCILE_CODEX_6.json#193','des variantes du théorème ... valable','first body paragraph, final sentence','The singular adjective valable can modify the singular noun théorème. The scan supplies no omitted plural mark; retain the wording.','No change; rejected edit remains rejected.',codex_id='SGA-SRC-001497')

# Independently verified accepted Codex records, including their FIXLOG rows.
accepted={165:(6,336,'SGA-SRC-001469','formule (2.2)','formule (1.2)','The paragraph extends formula (1.2), the Riemann–Roch identity; (2.2) defines the cotangent class.'),166:(6,337,'SGA-SRC-001470','E on the left, F on the right','F on both sides','The print differs in its two input variables; current restores the common F.'),167:(7,338,'SGA-SRC-001471','K•(X)→K(Parf(Y))','K•(Y)→K(Parf(Y))','The displayed map sends locally free Y-modules to perfect Y-complexes.'),168:(8,339,'SGA-SRC-001472','cl(L_dot)','cl•(L_dot)','The source has no raised dot at this occurrence; the preceding definition names the class cl•.'),170:(4,335,'SGA-SRC-001474',"sommes d'expression","sommes d'expressions",'The plural sums refer to expressions of the displayed form; current supplies the plural s.'),189:(14,340,'SGA-SRC-001493','Grauert [4]','Grauert [3]',e[20][1]),190:(14,341,'SGA-SRC-001494','Shih [7]','Shih [6]',e[22][1])}
known={z['source_id'] for z in records}
logs=(R/'fixes/FIXLOG_6_CURRENT.jsonl').read_text().splitlines()
for idx,(p,line,cid,pr,cor,reason) in accepted.items():
 rec('codex_reconciliation',p,f'fixes/RECONCILE_CODEX_6.json#{idx}',pr,'accepted Codex correction',reason,{'diplomatic':pr,'corrected':cor},codex_id=cid)
 sid=f'fixes/FIXLOG_6_CURRENT.jsonl#{line}'
 if sid not in known and line not in (335,):
  z=json.loads(logs[line-1]); rec('fixlog',p,sid,pr,'corrected text',reason,{'old':z['old'],'new':z['new']})
save('extra_decisions.json',records)
pages=load('extra_pages.json')
begins={11:'T_f∈K•(X).',12:'essentiellement non recollables',13:'algébrique clos',14:'[1] un homomorphisme groupes',15:'la première flêche verticale'}
findings=json.loads((R/'check/findings/findings_011_015.json').read_text())
for p in range(11,16):
 pages.append({'page':p,'pdf_page':p+14,'fully_checked':True,'main_scan_viewed':'four overlapping horizontal strips','witness_viewed':False,'findings_count':sum(x['page']==p for x in findings),'begins':begins[p],'notes':'Main scan compared word by word and symbol by symbol; all displays and footnotes included. The p14 reference corrections were also checked against the p19 bibliography image.'})
save('extra_pages.json',pages)
