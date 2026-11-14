#!/usr/bin/env python3
from review_helpers import Review
r=Review();p=297
r.finding('296_300',8,'Exposé V with one lower rule and no stop; GENERALITES SUR LES λ-ANNEAUX in capitals with two lower rules.',
 'Both the main top strip and native title crop show the separate title lines and the double rule beneath the main title. The attached explicit underlines match; the accepted capital-accent convention supplies É without changing the source wording.',
 'exposé heading',witness=308)
r.finding('296_300',9,'par P. BERTHELOT, with the full line underlined.',
 'The native title crop confirms the capital surname, punctuation after P and single rule beneath the complete author line. The attached form agrees.',
 'author line',witness=308)
r.finding('296_300',10,'le point de vue fonctoriel adopté ici à l’avantage…',
 'The grave accent is visible in both scans. The sentence’s subject is le point de vue fonctoriel adopté ici; its finite verb is a in the construction a l’avantage de réduire. The diplomatic layer keeps the printed accented form, and current receives the unaccented verb.',
 'second introductory paragraph',verdict='confirmed; current correction now applied',witness=308,
 change='Current only: adopté ici à l’avantage→adopté ici a l’avantage.')
r.patch(p,'current',"adopté ici à l'avantage","adopté ici a l'avantage",'check/findings/findings_296_300.json#10','Correct the finite verb avoir, preserving the source accent diplomatically.')
r.own_finding('ASTRA-V-FONT-297',p,'Both category letters are handwritten looping script C; the base-ring K and paragraph number 1.1. are ordinary typed characters.',
 r'\mathcal C in both occurrences; ordinary K and 1.1.',
 'Retain the two script category forms and remove bold weight from the paragraph number.',
 'The native lower crop resolves the looping C with no detached lower rule in both positions. The paragraph number has the same ordinary typed weight as the prose; no body phrase is underlined. The section-title rule remains covered by the accepted section-title convention.',
 'definition of the category and paragraph number',kind='font',witness=308)
r.patch(p,'both',r'\textbf{1.1.}',r'1.1.','ASTRA-V-FONT-297','Preserve the plain typed paragraph number.')
r.page(p,'Exposé V; GENERALITES SUR LES λ-ANNEAUX; par P. BERTHELOT','à valeurs dans la catégorie des groupes',
 'Complete title, author line, both introductory paragraphs, their quotation marks and punctuation, λ symbols and superscript i, section heading and beginning of the filtered-algebra definition compared. Both script C letters are retained locally. The printed à/finite a variant is explicit. No author note.',
 witness='Native witness308 title, introductory prose and category regions; witness_297_title.png, witness_297_intro.png and witness_297_category.png')
r.commit()
