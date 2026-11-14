#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=306
r.finding('306_310',1,'The page starts with (1+X^{(j)}t)_{j=1,..,k}, followed by the ambient functor value and un élément θ… .',
 'Both scans show the whole family expression at the top of this page, after élément on 305. The attached marker already precedes the family, as recorded by the preceding checker batch.',
 'page start',witness=317)
reason='The native top crop shows two full stops between the two commas in j=1,..,k. The diplomatic layer already has exactly two stops. The current three-dot ellipsis supplies the standard index-list abbreviation, with the identical endpoints 1 and k.'
r.finding('306_310',2,'j=1,..,k with two stops.',reason,'subscript of the first family',witness=317,change='Retain the existing two-stop diplomatic / three-stop current distinction.')
r.source('fixes/FIXLOG_6.jsonl#1331','j=1,..,k with two stops.',reason,'subscript of the first family',witness=317,page=p,change='Retain the applied diplomatic two-stop reading.')
r.finding('306_310',3,'Le lecteur se convaincra… begins a new paragraph.',
 'The main and native top images show the indented paragraph after conditions i) and ii). The attached layout already agrees, without changing words or mathematical tokens.',
 'after the two conditions',verdict='formatting observed; no content error',witness=317)
r.finding('306_310',4,'(cf. 1.3,ex.2) ends the three-relation line without a full stop.',
 'The native relations crop shows a bare closing parenthesis. The attached punctuation agrees; placing the reference on a separate TeX line changes only layout.',
 'three relations in 1.8',witness=317)
r.finding('306_310',5,'The 306 portion of Lemme 1.9 underlines Soit, un foncteur sur, and alors l’homomorphisme canonique.',
 'The main lower strips and native relations crop show exactly those lexical rules, with the formulas and semicolon/colon outside them. This saved decision is limited to the inspected 306 passage; the listed 307–310 statement passages are checked separately as those pages are read. No script infers their verdicts from 306.',
 'Lemme 1.9 on page 306',verdict='confirmed for inspected 306 portion',witness=317,change='Render the three inspected lexical spans locally.')
r.finding('306_310',6,'The three Ab fil occurrences on 306 each have separate rules under Ab and fil and no stops.',
 'The native relations crop resolves one category target and the two Hom subscripts. Replace just those three inspected occurrences by explicit forms. The source’s macro-wide proposal is not applied; the other named pages are decided individually when read.',
 'category target and two Hom subscripts',verdict='confirmed locally; scope amended',witness=317,change='At the three page-306 occurrences only, use separately underlined Ab and fil.')
r.patch(p,'both',r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}','check/findings/findings_306_310.json#6','Preserve the three observed category-name rules locally.',count=3)
r.patch(p,'both',r"\textbf{Lemme 1.9.} Soit \(H:\mathcal C_0\to\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}\) un foncteur sur \(\mathcal C_0\)~; alors l'homomorphisme canonique~:",r"\textbf{Lemme 1.9.} \uline{Soit} \(H:\mathcal C_0\to\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}\) \uline{un foncteur sur} \(\mathcal C_0\)~; \uline{alors l'homomorphisme canonique}~:",'check/findings/findings_306_310.json#5','Preserve the inspected lemma word rules with independent formulas and punctuation.')
r.own_finding('ASTRA-V-FONT-306',p,'Plain paragraph number 1.8.; handwritten script C throughout; capital I and lowercase d in Id with a script C₀ subscript.',
 r'1.8.; \mathcal C; \operatorname{Id}_{\mathcal C_0}.',
 'Remove bold weight from 1.8.; retain the inspected category and Id forms.',
 'The native top and relations crops resolve the plain paragraph number, every looping script category letter and its subscript, and the actual Id glyph. The three relations have the printed g subscripts and composition-circle order. This Id observation concerns the literal occurrence on 306; it does not infer other usage pages from the unprinted macro-reset records at 296.',
 'paragraph 1.8 and its relation line',kind='font',witness=317)
r.patch(p,'both',r'\textbf{1.8.}','1.8.','ASTRA-V-FONT-306','Preserve the ordinary typed paragraph number.')
r.page(p,'(1+X^{(j)}t)_{j=1,..,k}…','Hom_{Ab fil}(Ĝ,H∘g)→Hom_{Ab fil}(Ĝ∘i,H)',
 'Complete first family expression, both quantifiers and all multivariable indices, condition i) without a stop and ii) with a stop, all prose, i and g displays with final commas, the three functor relations and reference, and the lemma’s first part and final Hom display compared. No author note.',
 witness='Native witness317 top and relations crops; witness_306_top.png and witness_306_relations.png')
r.commit()
