from audit_support import *
reasons={
131:'PDF p.42 condition (i) explicitly uses a minus sign between barred X and Y. Restore that sign in all forms; setminus is a change of printed notation, although set-theoretically equivalent.',
132:'PDF p.42 definition of bon voisinage has existe des S-schémas. Codex still omits des; restore it in all forms.',
133:'PDF p.42 end of the good-neighbourhood paragraph has Spec(k), lowercase k, the field introduced earlier; Codex already agrees.',
134:'PDF p.42 last paragraph reads les fibres de u sont; Codex already agrees.',
135:'PDF p.43 final sentence prints sections hyperplanes with feminine adjective; Codex already agrees.',
136:'PDF p.44 first topological paragraph has application continue propre et séparée, with the final e visible; Codex already agrees.'}
decide('arcata',{n:('accepted',r) for n,r in reasons.items()})
starts={36:"d’obtenir en corollaire la",37:'satisfaisant aux conditions suivantes:',38:r'de $P$ un $\dP_S^1$-schéma',39:r'\section{Théorème de changement de base pour un morphisme propre.}',40:'Par passage à la limite'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated passage','reason':'Entire printed page directly compared, including both fibration diagrams and all references. Page38 starts mid-sentence at de P; page40 begins after the entire theorem (1.2).'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0013','page':'40','place':'Proposition (2.1), both Soient clauses','printed_reading':'Soient A ... et S=Spec(A). Soient f ... et X_0 ...','tex_reading':'Codex corrected changes both Soient to Soit under SGA45-CORR-0012','change':'Keep both printed plural forms in all French forms','kind':'editorial correction rejected','reason':'Each plural imperative introduces two coordinated objects: A and S, then f and X_0. The printed grammar is correct; neither change merits an apparatus entry.'}])
print('Arcata pp.36–40 recorded.')
