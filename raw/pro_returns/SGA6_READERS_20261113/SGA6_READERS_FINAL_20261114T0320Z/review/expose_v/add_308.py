#!/usr/bin/env python3
from review_helpers import Review,HERE
r=Review();p=308
r.finding('306_310',8,'sa valeur sur l’élément… begins the page.',
 'The main first strip and native top crop begin with sa, while 307 ends associe. The attached marker already stands before sa, preserving the space and complete phrase across the boundary.',
 'page start',witness=319)
for n,printed,region in [(9,'Le théorème résulte… begins a new paragraph.','after conditions i) and ii)'),(12,'Soit B… begins a new paragraph.','after the canonical isomorphism ε'),(13,'Par ailleurs… begins a new paragraph.','before the final filtered-group map')]:
 r.finding('306_310',n,printed,
  'Both main and native crops confirm the indentation and break. The attached layout already agrees, with unchanged words, symbols and punctuation; no new content patch is introduced.',
  region,verdict='formatting observed; no content error',witness=319)
r.finding('306_310',10,'The final series is 1+…+a_nt^n+… with baseline dots, followed by a comma.',
 'The native lower crop resolves both three-dot groups below the plus-sign midline and the final comma. The attached ldots groups and comma agree.',
 'last printed line',witness=319)
r.finding('306_310',14,'Six handwritten script G letters with connected descenders occur in 1.11 and its continuation on 308.',
 'The native lower crop resolves the long connected descending stroke at all six positions: the category name, the source of j, target of Gr, Id subscript, Ob argument and final category-arrow source. The adjacent script C letters lack that descending stroke. The text explicitly relates these categories by j:G→C, Gr:C→G and ε:Id_G→Gr∘j. The attached six mathcal G forms preserve the observed letters. This decision covers the inspected 308 occurrences; the other listed usage pages will receive their own direct checks.',
 'six script category letters on 308',verdict='confirmed for inspected 308 scope',witness=319,change='Retain the six already applied mathcal G forms locally.')
r.own_finding('ASTRA-V-UNDERLINE-308',p,'The theorem continuation underlines its lexical words, with formulas, references 1.4 and 1.5, parentheses and punctuation outside the rules.',
 r'\uline word spans through avec des notations analogues à celles de 1.4 et 1.5.',
 'Render the inspected theorem-continuation word rules.',
 'The native top crop resolves the separate rules beneath sa valeur sur l’élément, de, est injective, son image est le sous-groupe de, formé des éléments, tels que, avec des notations analogues à celles de, and et. The two displayed conditions are plain mathematical formulas; the proof and paragraph 1.11 are plain prose. This checks the 308 portion named in checker306_310#5.',
 'opening theorem continuation',witness=319)
t=(HERE/'page_308_current.tex').read_text();old=t.split('\n',1)[1].split('\n\\[',1)[0]
new=r"\uline{sa valeur sur l'élément} \(1+Xt\) \uline{de} \(\Ghat\circ i(K[X])\), \uline{est injective}; \uline{son image est le sous-groupe de} \(H(K[X])\) \uline{formé des éléments} \(\theta\) \uline{tels que} (\uline{avec des notations analogues à celles de} 1.4 \uline{et} 1.5)~:"
r.patch(p,'both',old,new,'ASTRA-V-UNDERLINE-308','Preserve the exact observed lexical-rule endpoints.')
r.own_finding('ASTRA-V-ABFIL-308',p,'Ab and fil are separately underlined in the target of the graded-algebra functor.',
 r'\mathcal G\to\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}',
 'Render this one inspected category-name occurrence explicitly.',
 'The native lower crop shows a rule beneath Ab and another beneath fil, ending before the sentence stop. This is the 308 occurrence listed in checker306_310#6; no macro-wide replacement is made.',
 'end of Soit B… paragraph',witness=319)
r.patch(p,'both',r'\Abfil',r'\underline{\mathrm{Ab}}\,\underline{\mathrm{fil}}','ASTRA-V-ABFIL-308','Preserve this observed category-name rule.')
r.own_finding('ASTRA-V-FONT-308',p,'Plain paragraph number 1.11.; capitalized Id with script G subscript; a headed tilde-labelled arrow for ε; hats over B and Gr A.',
 r'1.11.; \operatorname{Id}_{\mathcal G}; \xrightarrow{\sim}; \widehat B; \widehat{\operatorname{Gr}A}.',
 'Remove bold weight from 1.11.; retain the other inspected forms.',
 'The native lower crop resolves the plain numeral weight, I/d capitalization, the separate tilde above the isomorphism arrow, and the completion hats (the second spans Gr A). The infinite product has lower bound i=0 and upper ∞. The first condition ends with a semicolon and the second with a full stop; the later cf.1.7 reference has no final stop.',
 '1.11 and its completion notation',kind='font',witness=319)
r.patch(p,'both',r'\textbf{1.11.}','1.11.','ASTRA-V-FONT-308','Preserve the ordinary typed paragraph number.')
r.page(p,'sa valeur sur l’élément…','en associant à la série 1+…+a_nt^n+…,',
 'Complete theorem continuation and both conditions, the proof and convention paragraphs, all of 1.11, the six script G occurrences and adjacent script C forms, ε arrow, product bounds, completion hats, category-name rules and final comma compared. Checker306_310#11 concerns actual309 and is reserved for that page. No author note.',
 witness='Native witness319 top and lower crops; witness_308_top.png and witness_308_lower.png')
r.commit()
