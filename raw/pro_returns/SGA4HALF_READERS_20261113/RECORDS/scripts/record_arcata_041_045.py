from audit_support import *
reasons={
137:'PDF p.46 explicitly includes the comparison theorem EGA III,4.1, the completion-to-inverse-limit map and its bijectivity before the idempotent map. Codex already restores the whole paragraph; retain it and its citation key in all forms.',
138:'PDF p.46 says X_n et X_0 ont même espace topologique; Codex already agrees.',
139:'PDF p.47 completion paragraph reads le long de X_0; Codex already agrees.',
140:'PDF p.47 local-finite-presentation paragraph has un système; Codex already agrees.',
141:'PDF p.47 Artin approximation paragraph introduces barred xi over the completion, distinguished from xi over A; Codex already agrees.',
142:'PDF p.48 proof (3.3) attaches the subscript U to the constant sheaf Z/n; Codex already restores it.',
143:'PDF p.48 image description says le plus petit; Codex already agrees.',
144:'PDF p.49 Godement paragraph places the geometric point over lowercase x; Codex already agrees.',
145:'PDF p.49 Godement paragraph has the normal grave accent in où; Codex already agrees.',
146:'PDF p.50 proof (3.7) places p_{i*} below the product sign. The expression must instead apply each direct-image functor to C_i, as in (3.2)(ii) on p.43. Preserve the subscript diplomatically and correct the product of direct images only in corrected/reading.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={41:r'$\Gamma(X,\sO_X)$ pour la topologie',42:r'\operatorname{Rev.et}(X) \to \operatorname{Rev.et}(X_0)',43:r"à $X_0'$.",44:r'sur $\cC$ à valeurs',45:r'\begin{propositiondotdash}\label{I:4-3-7}'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage or display','reason':'Entire page compared with the scan, including restored comparison theorem and all canonical maps. Page43 starts with the final words à X_0-prime, and page44 starts inside definition (3.4).'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0146','page':'45','place':'proof (3.7), form of objects of E','printed':r'\prod_{p_{i*}} C_i','corrected':r'\prod p_{i*} C_i','kind':'formula','reason':'The product is of the direct images p_{i*}C_i, as in (3.2)(ii).','en_printed':r'\prod_{p_{i*}} C_i','en_corrected':r'\prod p_{i*} C_i'}])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0014','page':'41','place':'Proposition (2.2), both Soient clauses','printed_reading':'Soient A ... et S=Spec(A). Soient f ... et X_0 ...','tex_reading':'Codex corrected changes both Soient to Soit under SGA45-CORR-0013','change':'Keep both printed plural forms in all French forms','kind':'editorial correction rejected','reason':'As in (2.1), each plural imperative introduces two coordinated objects. The printed construction is grammatical.'}])
print('Arcata pp.41–45 recorded.')
