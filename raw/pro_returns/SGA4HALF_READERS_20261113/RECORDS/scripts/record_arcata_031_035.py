from audit_support import *
reasons={
107:'PDF p.36 proof (2.2) prints égal without final e; Codex already agrees.',
108:'PDF p.36 reduced-norm bracket prints se descend without final e; Codex already agrees.',
109:'PDF p.37 first paragraph uses lowercase d in delta+Nd; Codex already agrees.',
110:'PDF p.37 second paragraph prints le cas général; Codex already agrees.',
111:'PDF p.37 extension is transcendante pure; Codex already agrees.',
112:'PDF p.37 introduces s=[K:k(X)], also used in sn and sd; Codex already agrees.',
113:'PDF p.37 prints une base with final e; Codex already agrees.',
114:'PDF p.37 norm-polynomial argument visibly has X_{ij}, although the introduced variables are U_{ij}. Keep X diplomatically and repair to U in corrected/reading in both languages.',
115:'PDF p.37 visibly prints the norm subscript K/k. The finite extension is K/k(X); use that subscript only in corrected/reading. This agrees with Codex SGA45-CORR-0011B, the append-only alias correcting its historical identifier collision.',
116:'PDF p.37 says polynôme homogène; Codex already restores homogène.',
117:'PDF p.37 introductory paragraph of §3 has groupes de cohomologie; Codex already agrees.',
118:'PDF p.38 first paragraph has eta as the second subscript of G_m; Codex already agrees.',
119:'PDF p.38 first paragraph includes de X after K(X). The words are still absent in Codex and must be restored in all forms.',
120:'PDF p.38 first paragraph prints point fermé without extra e; Codex already agrees.',
121:'PDF p.38 divisor sheaf before the sequence has i_{x*}, a direct image, not subscript x_I; Codex already agrees.',
122:'PDF p.38 divisor sequence is labelled (*); Codex restores it while keeping Miller’s stable label.',
123:'PDF p.38 proof (3.2) prints point fermé without extra e; Codex already agrees.',
124:'PDF p.38 last proof sentence uses the noun transcendance; Codex already agrees.',
125:'PDF p.39 proof (3.4) explicitly names the closed point x. Codex still omits x in this phrase; restore it in every form.',
126:'PDF p.39 higher-direct-image expression has a visible equals sign; Codex already restores it.',
127:'PDF p.39 proof (3.4) prints le spectre; Codex already agrees.',
128:'PDF p.40 Kummer proof prints plural égalités; Codex already agrees.',
129:'PDF p.40 second low-degree exact sequence contains two Pic(X) terms connected by multiplication by n. Codex restores both terms and arrows; retain them in every form.',
130:'PDF p.40 final paragraph begins Un dévissage; Codex already agrees.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={31:r'\begin{propositiondotdash}\label{I:3-2-2}',32:r'$f(\underline{T})=0$ devient un système',33:r'\h^0(X,\dG_m) &= k^*',34:r'\h^q(X, j_* \dG_{m,\eta}) = \h^q(\eta,\dG_{m,\eta})',35:r'\begin{corollarydash}\label{I:3-3-5}'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage or formula','reason':'All words, mathematical expressions and diagram terms compared directly with the scan. Exact page starts corrected against printed lines rather than automatic slices.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0114','page':'32','place':'norm polynomial argument','printed':'X_{i j}','corrected':'U_{i j}','kind':'symbol','reason':'The variables introduced in the previous sentence are U_{ij}.','en_printed':'X_{i j}','en_corrected':'U_{i j}'},
{'id':'SGA45-CORR-0011B','sources':['SGA45-CORR-0011B','S45-SOL-0115'],'page':'32','place':'norm subscript','printed':'N_{K/k}','corrected':'N_{K/k(X)}','kind':'formula','reason':'Only K/k(X) is the indicated finite extension.','en_printed':'N_{K/k}','en_corrected':'N_{K/k(X)}'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0011','page':'28','place':'(1.2), closure and Galois group','printed_reading':r'Soient $\bar K$ une clôture algébrique de $K$ et $G=\gal(\bar K/K)$','tex_reading':'Codex corrected changes Soient to Soit (SGA45-CORR-0011, first historical row)','change':'Keep Soient in all forms','kind':'editorial correction rejected','reason':'Two objects are introduced, the closure and the Galois group; their different grammatical descriptions do not make the plural imperative erroneous.'},
{'id':'S45-ASTRA-A-0012','page':'27','place':'Codex proper-name correction SGA45-CORR-0010','printed_reading':'Künneth','tex_reading':'Codex calls Kunneth the diplomatic reading and Künneth a correction','change':'Classify the umlaut restoration as transcription repair in all forms, linked to S45-ASTRA-A-0010','kind':'editorial classification','reason':'The enlarged scan displays the umlaut; there is no difference between the print and the corrected spelling, so no apparatus variant is warranted.'}])
print('Arcata pp.31–35 recorded.')
