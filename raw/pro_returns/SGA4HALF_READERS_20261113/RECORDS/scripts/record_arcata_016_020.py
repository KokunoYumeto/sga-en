from audit_support import *
decide('arcata',{
43:('accepted','PDF p.21 local-section compatibility line reads on ait; Codex already agrees.'),
44:('accepted','PDF p.21 sheaf condition has pour toute section donnée; Codex already agrees.'),
45:('accepted','PDF p.21 exactness definition prints tout s ... telle. The masculine quantifier tout requires tel; retain telle diplomatically. English such that is unaffected.'),
46:('accepted','PDF p.21 example (6.4)a reads La topologie de Grothendieck; Codex already agrees.'),
47:('accepted',"PDF p.22 cohomology paragraph prints d'un faisceau abélien in the singular; Codex already agrees."),
48:('accepted','PDF p.22 derived-functor sentence reads on note; Codex already agrees.'),
49:('accepted','PDF p.22 explicitly prints a centred dot in the variable argument of H^i(X,•). Restore that displayed notation; the dash is not a macro rendering the same sign.'),
50:('accepted','PDF p.22 visibly numbers both Cohomologie and the following torsor paragraph (6.5). Keep the duplicate label surface in diplomatic and use (6.6) in corrected/reading, preserving the stable label I:1-6-6.',{'codex_ids':['SGA45-CORR-0006']}),
51:('accepted','PDF p.23 definition (1.1)c has underlined r at all three locations, with no descender. Restore r using the existing Fraktur alphabet; p is a different letter.'),
52:('accepted','PDF p.24 example (1.2)b prints analytisé; it refers to the analytification morphism, not the property analyticité.'),
53:('accepted','PDF p.24 analytic morphism has target S^an, matching f:X→S; Codex already agrees.'),
54:('accepted with a corrected reading','PDF p.24 Sorite (1.3) has four items. Its b) is exactly the composition assertion. Supplied Codex incorrectly places the word (composition) before the original c), while still omitting b). Insert the complete b) and remove that misplaced label from c).',{'fix_old':'  \\item (composition) Si $f:X\\to S$ et $g:Y\\to S$','fix_new':'  \\item (composition) Le composé de deux morphismes étales est un morphisme étale.\n  \\item Si $f:X\\to S$ et $g:Y\\to S$','change_made':'Restore all four items a–d; remove the misplaced composition label from item c.'}),
55:('accepted','PDF p.24 (1.4) reads et on note; the pronoun is visible and absent in Codex diplomatic.'),
56:('accepted','PDF p.24 last sentence of (1.4) has muni de la topologie étale; Codex already agrees.'),
57:('accepted','PDF p.25 first reference is I.6.5, repeating the source torsor paragraph number. In corrected/reading it must follow the renumbered I.6.6; diplomatic retains I.6.5.'),
58:('accepted','PDF p.25 first paragraph clearly has point base choisi; Codex already agrees.'),
59:('accepted','PDF p.25 multiplicative-group paragraph prints asterisks on O_U, H^0(X,O_X), and k. Restore these three authorial signs in all forms; changing asterisk to cross is a notation change rather than a macro for the same sign.'),
60:('rejected','PDF p.25 indeed prints the unqualified references (4.2)(i) and (4.5). The preceding descent discussion and the words pleine fidélité determine their chapter-I targets; the retained labels already target those results. Adding I is editorial expansion, not a securely established misprint, so preserve the printed reference surfaces.'),
61:('accepted','PDF p.25 proof (2.3)b visibly reads i.e. isomorphes à O_X; the word must be restored in all forms.'),
62:('rejected','PDF p.25 final line prints (4.2)(ii) and (4.5). As in S45-SOL-0060, the intended earlier descent results are unambiguous and correctly linked; no proven misprint requires an added chapter prefix.')
})
starts={16:'contravariant $\\sF$',17:'topologie fpqc (fidèlement plate quasi-compacte)',18:r'\section{Topologie étale.}',19:r'\subsubsection{Exemples:}\label{I:2-1-2}',20:r'De plus $\h^1(X,\dZ/n)$'}
append_jsonl(ROOT/'work/arcata/pages.jsonl',[{'printed_page':str(p),'pdf_page':INDEX[str(p)]['pdf_page'],'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL),'start_fr':a,'start_en':'Corresponding translated phrase/display','reason':'Full page checked visually against diplomatic TeX. Page starts independently settled; notably p17 begins topologie fpqc, and p20 begins De plus. Miller sheaf conventions retained.'} for p,a in starts.items()])
append_jsonl(ROOT/'work/arcata/variants.jsonl',[
{'id':'S45-SOL-0045','page':'16','place':'definition of exactness','printed':'telle que','corrected':'tel que','kind':'word','reason':'Agreement with masculine tout s.','english_applicability':'No English change.'},
{'id':'SGA45-CORR-0006','sources':['SGA45-CORR-0006','S45-SOL-0050'],'page':'17','place':'torsor paragraph number','printed':'6.5','corrected':'6.6','kind':'number','reason':'Duplicated paragraph number; the next number is 6.6.','en_printed':'6.5','en_corrected':'6.6'},
{'id':'S45-SOL-0057','page':'20','place':'reference to torsors','printed':'I.6.5','corrected':'I.6.6','kind':'reference','reason':'Reference follows the corrected torsor paragraph number.','en_printed':'I.6.5','en_corrected':'I.6.6'}
])
append_jsonl(ROOT/'work/arcata/own_findings.jsonl',[
{'id':'S45-ASTRA-A-0005','page':'14','place':'multiplicative groups in Hilbert 90 paragraph','printed_reading':r"k'^*",'tex_reading':r"{k'}^\times",'change':'Restore asterisk for the group of units consistently on this page, all forms','kind':'symbol','reason':'PDF p.19 prints asterisks throughout. This is an explicit reversal of the rendition’s sign substitution, preserving the author’s notation.'},
{'id':'S45-ASTRA-A-0006','page':'19','place':'Sorite (1.3), Codex restoration','printed_reading':'b) composition assertion; c) two étale morphisms','tex_reading':'(composition) attached to the two-morphisms item; whole b) absent','change':'Restore b) and remove the misplaced label from c)','kind':'missing','reason':'Direct scan establishes all four lettered items. Codex’s insertion of a label alone repaired the wrong locus; see S45-SOL-0054.'}
])
print('Arcata pp.16–20 recorded.')
