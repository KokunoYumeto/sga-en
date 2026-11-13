"""Exact witnesses selected after reading the final French page contexts."""
from pathlib import Path
import json
import check_coverage as c
W=Path(__file__).parent
existing={}
for finding in c.D:
 sid=finding['id'];page=int(finding['printed_page'])
 if any(op['id']==sid and op['lang']=='fr' for op in c.OPS):continue
 witness=finding.get('change_made','').replace(r'\n','\n')
 if len(witness)>6 and all(c.literal_evidence('fr',page,witness,mode) for mode in [0,1]):
  existing[sid]=dict(page=page,witness=witness,classification='inherited French reading already matches scan',explanation='The literal scan repair is already present in the inherited diplomatic source and survives both selected readings.')
out={}
def add(sid,page,witness,explanation,classification='inherited French reading already matches scan'):
 if isinstance(sid,int):sid=f'S45-SOL-{sid:04d}'
 evidence=witness if isinstance(witness,list) else [dict(page=page,witness=witness)]
 for e in evidence:
  for mode in [0,1]:assert c.literal_evidence('fr',e.get('page',page),e['witness'],mode),(sid,e)
 out[sid]=dict(page=page,evidence=evidence,classification=classification,explanation=explanation)
add(1093,262,[dict(page=262,witness=r'\PrintPage{262}\chapter{Catégories dérivées}'),dict(page=263,witness=r'\PrintPage{263}\begin{center}\textbf{Sommaire}'),dict(page=264,witness=r'\PrintPage{264}\section{Catégories triangulées: définitions et exemples}')],'The three observed source-page boundaries separate title, contents, and first chapter.','page-boundary restoration')
add(1104,266,r'Le triangle $(X,X,0,\operatorname{id}_X,0,0)$ est distingué.','The identity has its X subscript; braces around a one-token subscript do not change the printed symbol.')
add(1144,281,r'$S_Y$','The Y subscript is already present, including both readings of the adjacent omission variant1145.')
add(1166,288,r'Considérons pour un objet $X$ de $\cA$','The object is X in the existing French text.')
add(1199,300,r'\section{Les foncteurs dérivés}\label{VIII:4}','The printed chapter text is retained; the allowed Miller section numbering is not a printed-text correction.','rejected proposal; existing equivalent heading retained')
add(1206,301,[dict(page=302,witness=r"\PrintPage{302}foncteur $\%$ (resp. $\%'$)")],'The302 boundary is placed before the actual percent-shaped functor glyph.','page-boundary restoration')
add(1217,304,r'\begin{theorem}\label{VIII:4-2-3}','The theorem target remains explicit and unchanged. Miller numbering is retained rather than introducing a speculative printed correction.','rejected proposal; theorem target retained')
add(1225,305,r"Alors le théorème \ref{VIII:4-2-3} s'applique",'The existing reference still resolves to the explicit theorem target.','rejected proposal; reference target retained')
add('S45-ASTRA-V-0001',236,r'Soient $X$ un schéma de type fini sur $k$ séparablement clos et $\sF$ un faisceau','The plural verb governs both X and F, so it is retained.','rejected Codex proposal; printed wording retained')
add('S45-ASTRA-V-0002',234,'grosso modo','The source expression is preserved; only the English translation needed repair.','French source unchanged; English-only translation repair')
add('S45-ASTRA-V-0003',244,r'en dimension de $X_\eta<n$','The French explicitly speaks of dimension; the English omission was repaired.','French source unchanged; English-only translation repair')
add('S45-ASTRA-V-0013',257,"Il découle de l'hypothèse d'acyclicité locale que la flèche canonique",'The French has the local-acyclicity argument without the extra English qualification.','French source unchanged; English-only translation repair')
add('S45-ASTRA-V-0014',259,r"L'hypothèse d'acyclicité sur $q$ entra\^ine donc que la restriction",'The French directly states the implication; the English rhetorical addition was removed.','French source unchanged; English-only translation repair')
add('S45-ASTRA-V-0015',261,"L'hypothèse implique que",'The French does not contain the added English qualification.','French source unchanged; English-only translation repair')
add('S45-ASTRA-V-0016',256,r'dans le \mbox{cas} $S=\spec(\dC)$','The box changes only permitted line breaking and retains every printed word.','permitted layout retained')
add('S45-ASTRA-V-0017',261,(W/'bibliography_261_fr.tex').read_text(),'All four restored bibliography entries are present as the reviewed complete block.','restored source block')
add('S45-ASTRA-V-0018',263,(W/'contents_263_fr.tex').read_text(),'The entire restored original contents, including all local page numbers, is present.','restored source block')
add('S45-ASTRA-V-0020',272,r'0 \ar[r] & X^\bullet \ar[r] & Y^\bullet \ar[r] & Z^\bullet \ar[r] & 0','The sequence arrows remain unlabelled, as printed.','rejected Codex proposal; unlabelled arrows retained')
add('S45-ASTRA-V-0028',290,r'Un tel morphisme $\delta$ est unique et vérifie','The final printed delta notation is retained; the stray subscript is separately a variant under1172.','rejected Codex proposal; printed notation retained')
add('S45-ASTRA-V-0029',295,r'(S=0 \to X^\bullet \to Y^\bullet \to Z^\bullet \to 0)','The short exact sequence retains its printed unlabelled maps.','rejected Codex proposal; unlabelled arrows retained')
add('S45-ASTRA-V-0031',298,r'\varinjlim_{(\mathsf{Qis}/X^\bullet)^\circ} \hom_{\eK(\cA)}(-,Y^\bullet) \ar[dl]^-\sim','The existing down-left arrow already connects to the next-line limit, as required by the scan.')
(W/'coverage_witnesses_fr_manual.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(W/'coverage_witnesses_fr_existing.json').write_text(json.dumps(existing,ensure_ascii=False,indent=2))
print('Recorded',len(out),'manually selected and',len(existing),'literal-match French witnesses')
