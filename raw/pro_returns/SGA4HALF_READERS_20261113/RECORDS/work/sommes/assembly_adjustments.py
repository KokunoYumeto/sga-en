from audit_helpers import *
# Extra repairs disclosed by comparing every later change in the two supplied trees.
own(50,205,'(4.17.3)–(4.17.5), continued p206',r'(T v)^\ast\sF(\psi), T v',r'(T v_0)^\ast\sF(\psi), T v_0', 'Restore the unindexed geometric morphism v after scalar extension.', 'transcription', 'The directly inspected p205 and p206 equations and prose print v without subscript after the original extension statement. Codex added subscripts not in the scan; preserve the earlier printed (T v_0) only in that extension statement.')
own(51,227,'Proof of 7.17, primed second factor',r"x_2'=\pr_2",r"x_2'=\pr_1",r"x_2'=\pr_2",'transcription','The scan distinguishes the unprimed projection pr1 from the primed projection pr2. A Codex change to the primed projection was an introduced error, independent of Sol0958 for the unprimed projection.')
own(52,228,'7.20 proof, fixed subspace cohomology',r'\h_c^{n-1}(V_a,\sF(\psi))',r'\h_c^{n-1}(V_a,\sF(\psi\sigma))',r'\h_c^{n-1}(V_a,\sF(\psi))','transcription','The enlarged p228 scan clearly prints F(psi) in this fixed-subspace occurrence. Retain the locally evident pullback abbreviation; an added sigma is not a required mathematical correction.')
# Exact bilingual boundary anchors resolved against the supplied translation.
updates={168:{'start_en':r'\chapter{Applications of the trace formula'},169:{'start_en':r'\section*{Notations}'},186:{'start_en':'More generally, given a finite filtration'},188:{'start_en':r'$\h_c^p(X,\sF)$'},189:{'start_en':r'\section{Sums in one variable}'},192:{'start_en':'would be the inverse image of an'},196:{'start_en':r'\section{Gauss and Jacobi sums}'},197:{'start_en':'\\begin{proof}[Proof]\nThe sheaf'},211:{'start_en':'Together with'},212:{'start_en':r'\item For $\fp$ prime'},214:{'start_en':'the product of $\\lambda_i$ is trivial'},220:{'start_fr':'On a encore\n\\begin{align*}', 'start_en':'We likewise have'},222:{'start_en':r'\item At $0$, the monodromy'}}
p=BASE/'pages.jsonl';rows=[json.loads(l) for l in p.read_text().splitlines()]
for r in rows:r.update(updates.get(int(r['printed_page']),{}))
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
# Repair an escaped-quote loss in the insertion journal, not a reading change.
p=BASE/'edits.jsonl';rows=[json.loads(l) for l in p.read_text().splitlines()]
for r in rows:
 if r['source']=='S45-ASTRA-S-0046':
  r['new']=r['new'].replace('(Inv. Math., à paraître) \\cite','(Inv. Math., à paraître)\'\' \\cite').replace('(Inv. Math., forthcoming) \\cite','(Inv. Math., forthcoming)\'\' \\cite')
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
