#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=317
r.finding('316_320',7,'Page317 starts λ-anneaux., followed by the hyphen item Soit A un anneau.',
 'The main first strip and native top crop resolve the continuation word and its full stop before the second list item. The fully inspected316 ends at des. The attached boundary agrees.',
 'page start',witness=328)
r.finding('316_320',8,'The source prints un morphisme de at line end, followed by Z-bilinéaire de foncteurs.',
 'Both scans resolve the extra de between morphisme and its adjective. The displayed operation β_K:Ĝ(K)×Ĝ(K)→Ĝ(K) is specified by β(1+Xt,1+Yt)=1+XYt in2.3.1; Z-bilinéaire qualifies that operation. Removing the intervening de restores the adjective construction without changing this map or its arguments.',
 'multiplication-definition paragraph',verdict='not applied and now applied',change={'diplomatic':r'un morphisme de \(\mathbb Z\)-bilinéaire','current':r'un morphisme \(\mathbb Z\)-bilinéaire'},witness=328)
r.patch(p,'current',r'un morphisme de \(\mathbb Z\)-bilinéaire',r'un morphisme \(\mathbb Z\)-bilinéaire','check/findings/findings_316_320.json#8','Remove the printed surplus preposition in the corrected adjective construction.')
r.finding('316_320',9,'The source prints par élément1+XYt, without an article.',
 'Both scans resolve the adjacent words par élément. The sentence singles out the explicit element1+XYt of Ĝ(Z[X,Y]); the following cet élément and equation2.3.1 refer to exactly that same series. Restore the missing definite article in the corrected layer while keeping the printed omission diplomatically.',
 'multiplication-definition paragraph',verdict='not applied and now applied',change={'diplomatic':'par élément','current':'par l’élément'},witness=328)
r.patch(p,'current',r'par élément \(1+XYt\)',r"par l'élément \(1+XYt\)",'check/findings/findings_316_320.json#9','Restore the definite article referring to the explicitly specified universal series.')
r.finding('316_320',10,'The label Id stands above the bottom rightward arrow of the second square, near its arrowhead.',
 'The native lower crop and tight witness_317_Id.png resolve the capital I and lowercase d above the shaft. The attached upper-side label agrees. Its precise horizontal placement is a layout observation, with no additional mathematical token change.',
 'second square, lower arrow',witness=328)
r.finding('316_320',11,'The identity label is printed Id: with two vertically aligned points after d.',
 'The tight native crop resolves both points, separate from the arrowhead below. The arrow is Id_Ĝ:Ĝ→Ĝ, α↦α, in the commutativity square; the colon supplies no further argument or defined expression. The attached diplomatic Id: and corrected Id preserve the printed punctuation and its deletion respectively.',
 'second square, identity label',witness=328)
r.own_finding('ASTRA-V-ID-317',p,'The identity label uses a capital I and lowercase d, without an underline.',
 r'\id expands to \operatorname{Id} at this inspected usage.',
 'Retain the scoped capitalized identity-operator definition.',
 'The native identity crop directly verifies this first literal id-macro use after the Exposé V reset. This supplies usage-page evidence for the implementation records at296; those records themselves made no claim that Id was printed on296. The separately adjudicated colon is punctuation, and the identity map remains α↦α on Ĝ.',
 'second square, bottom arrow label',kind='font',verdict='confirmed',witness=328)
r.own[-1]['related_sources']=['fixes/FIXLOG_6.jsonl#339','fixes/FIXLOG_6_CURRENT.jsonl#304']
r.own_finding('ASTRA-V-FONT-317',p,'The number2.3. is plain; all A letters in the ring/representation example, including (T,A), are plain. Both integer-ring Z letters have the reinforced diagonal form.',
 r'Render2.3. without bold; retain the local plain A forms and \mathbb Z.',
 'Restore the inspected plain paragraph number and retain the other local forms.',
 'The native top crop resolves the ordinary number, the unruled A in every example position, and the doubled-diagonal Z in bilinéaire and Z[X,Y]. Every hatted G on this page was checked in the two native crops; all surrounding running prose is plain.',
 'second list item and2.3',kind='font',witness=328)
r.patch(p,'both',r'\textbf{2.3.}','2.3.','ASTRA-V-FONT-317','Preserve the observed plain paragraph number.')
r.finding('316_320',4,'Both special-case items use short typed hyphens: Soit X un schéma on316 and Soit A un anneau on317.',
 'The complete pages316 and317 have now been compared in both scans. Each native crop resolves the short hyphen before Soit. The attached label=- reproduces both observed list markers.',
 'the two special-case items across316/317',verdict='confirmed at both inspected items',change='Retain the existing explicit hyphen list label.',witness=327)
for row in r.decisions:
 if row['source_id'] in ['check/findings/findings_316_320.json#4','fixes/FIXLOG_6.jsonl#1396','fixes/FIXLOG_6_CURRENT.jsonl#1521']:
  row['image']='scan/SGA6_scan_360dpi.pdf#page=330; scan/SGA6_witness_300dpi.djvu#page=327; scan/SGA6_scan_360dpi.pdf#page=331; scan/SGA6_witness_300dpi.djvu#page=328'
r.page(p,'λ-anneaux.','the second square’s final Ĝ followed by a comma',
 'Complete representation example and its lowercase modules,2.3 statement, all hats and doubled Z forms, both printed grammar slips, exact product bounds i=1…n and degree condition k<n, circle operation and2.3.1 punctuation, all eight headed square arrows, every node, capitalized identity label and its colon, and the final comma compared. No author note.',
 witness='Native witness328 top/lower and tight identity crop; witness_317_top.png, witness_317_lower.png, witness_317_Id.png')
r.commit()
