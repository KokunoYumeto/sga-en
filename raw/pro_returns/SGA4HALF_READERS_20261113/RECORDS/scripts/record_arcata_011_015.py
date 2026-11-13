from audit_support import *
decide('arcata',{
30:('accepted','PDF p.16 paragraph after triangle has the indexed structural map phi_U:U→X. The U is visible below phi; Codex already supplies it.'),
31:('accepted','PDF p.16 theorem (4.5) prints la réunion; Codex already agrees.'),
32:('accepted','PDF p.17 proof starts with capital X est affine; Codex already agrees.'),
33:('accepted','PDF p.17 Réciproquement paragraph prints M_U although phi has source V; its pullback is a module on V, so only corrected/reading use M_V.'),
34:('accepted',"PDF p.17 prints que ces identifications after M'''; the q is clear. Codex already supplies it."),
35:('accepted','PDF p.18 prints partial_0 partial_1 = partial_0 partial_0. With the coface arrows in the preceding diagram and right-to-left composition used throughout, inserting a unit in positions 0 then 1 equals inserting it twice at 0; the left composite must be partial_1 partial_0. Retain the printed order in diplomatic.'),
36:('accepted',"PDF p.18 right-adjoint diagram has exactly two primes on the kernel target M''. Three primes occur only in the input diagram. Codex already agrees."),
37:('accepted','PDF p.18 final line prints homomorphisme without any internal accent; Codex already agrees.'),
38:('accepted',"PDF p.19 prints v'∈V without prime on V. The arbitrary chosen basis vector belongs to V', while V is the invariant subspace constructed later; corrected/reading restore the prime."),
39:('accepted','PDF p.19 sentence after the cocycle identity prints non nul, with final l; Codex already agrees.'),
40:('accepted','PDF p.20 restriction-of-sieve paragraph reads constitué par; Codex already agrees.'),
41:('accepted','PDF p.20 restriction uses psi:W→V, matching the source W of the composite; capital W visible and already restored in Codex.'),
42:('accepted','PDF p.20 bottom (6.3) prints donné without a final e; Codex already agrees.')
})
starts={11:r'\subsubsection{}\label{I:1-4-3}',12:'\\begin{proof}\nNous ne traiterons',13:'\\[\\xymatrix{\n  B \\ar@<3pt>',14:'\\begin{align*}\n  k\'\\otimes_k',15:r'\subsection{Topologies de Grothendieck.}'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding labelled paragraph/display','reason':'Entire page directly compared, including every diagram arrow, index and prime; exact boundary differs from automatic overlap span. Stated Miller form conventions retained.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[{'id':'S45-ASTRA-A-0004','page':'4','place':'opening.tex, English lecture title','printed_reading':'Inputs of etale cohomology','tex_reading':'Inputs of étale cohomology','change':'Remove the added acute accent within the quoted English title in every form','kind':'accent','reason':'PDF p.9 plainly prints etale without accent; this is a quoted title, not an accented-capital convention.'}])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0033','page':'12','place':'Réciproquement paragraph','printed':r'M_U=\varphi^* M\prime','corrected':r'M_V=\varphi^* M\prime','kind':'symbol','reason':'The pullback along V→U lives on V.','en_printed':'same formula','en_corrected':'same formula'},
{'id':'S45-SOL-0035','page':'13','place':'coface identity','printed':r'\partial_0\partial_1','corrected':r'\partial_1\partial_0','kind':'formula','reason':'The usual coface relation for right-to-left composition requires the reversed left indices.','en_printed':'same formula','en_corrected':'same formula'},
{'id':'S45-SOL-0038','page':'14','place':'after proposition (5.2)','printed':r"v'\in V",'corrected':r"v'\in V'",'kind':'symbol','reason':"The arbitrary basis vector is in V', not necessarily its invariant subspace V.",'en_printed':'same formula','en_corrected':'same formula'}
])
print('Arcata pp.11–15 recorded.')
