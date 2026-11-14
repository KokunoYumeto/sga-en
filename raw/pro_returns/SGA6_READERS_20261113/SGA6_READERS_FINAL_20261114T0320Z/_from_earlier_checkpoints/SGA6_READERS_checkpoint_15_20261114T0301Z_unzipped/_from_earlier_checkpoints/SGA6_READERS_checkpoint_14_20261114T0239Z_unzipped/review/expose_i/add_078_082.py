#!/usr/bin/env python3
from review_helpers import Review
r=Review()
r.finding('076_080',9,'Two title lines, then par L. ILLUSIE; no Exposé I prefix',
    'The whole title page has no printed exposé-number prefix above or within the two title lines. The attached title already omits the added words.', 'Entire title block')
r.finding('076_080',10,'GÉNÉRALITÉS SUR LES CONDITIONS DE FINITUDE DANS LES / CATÉGORIES DÉRIVÉES, capitals and double underlines',
    'Each capitalized title line carries two visible parallel rules. The supplied title preserves their letter case, accents and rules.', 'Two title lines')
r.finding('076_080',11,'par L. ILLUSIE, single underline',
    'The author name is in capitals and the line has one rule. Both layers have exactly this author form.', 'Author line')
r.finding('076_080',12,'L_n→L_{n−1}→...→L_0→F→0, with three baseline dots',
    'The three typed dots lie below the arrows’ shafts. Both layers already use ldots.', 'First display')
r.finding('076_080',13,'le troisième l’est aussi. On généralise aisément',
    'On généralise follows on the same printed line and continues the same paragraph; the attached prose now joins it.', 'Main paragraph, third-party pseudo-coherence sentence')
r.finding('076_080',14,'en tant que Module. La notion de complexe pseudo-cohérent',
    'La is at the end of the same printed line as Module, and notion starts the next line without a paragraph indentation. Retain the joined source paragraph.', 'Middle paragraph, after en tant que Module')
r.finding('076_080',15,'0→L_n→...→L_0→F→0, with three baseline dots',
    'The typed dots are on the baseline below the arrows. Both attached layers use ldots.', 'First display')
r.finding('076_080',16,'On a évidemment D(X)_parf⊂D(X)_coh, mais l’inclusion est',
    'The source prints the inclusion inline and the attached layers already do so. This is an accepted layout choice; the formula and following comma are retained without a content correction.', 'Middle paragraph, after tensoriel dérivés',
    verdict='amended',change='Retain the existing inline formula; classify the move as accepted layout.')
r.finding('076_080',17,'Triangle R→L→F→R followed by a comma to the right of F',
    'The comma is clearly visible outside the triangle to the right of F, and the three arrowheads agree with the supplied diagram. Retain the current comma.', 'Triangle in lower half')
r.finding('081_085',1,'commode - et utile',
    'The punctuation is one short typed hyphen, matching the glyph in s’avère-t-il above. The attached source already uses one hyphen.', 'First paragraph, line starting commode')
r.finding('081_085',2,'notamment dans l’Exp. II - d’axiomatiser',
    'The closing parenthetical dash is the same single typed hyphen as its opening counterpart. Retain the one-hyphen source form.', 'First paragraph, same line')
r.finding('081_085',3,'sont donnés dans l’Exp. II. On montre en particulier',
    'The first printed line continues after the period; there is no paragraph indentation before On montre. The joined attached text agrees.', 'First body line')
r.finding('081_085',4,'A titre d’illustration - et pour',
    'The dash after illustration is a single short hyphen. The supplied source retains that glyph; the initial capital accent is accepted by NOTE_6.', 'First paragraph, illustration clause')
r.finding('081_085',5,'des notions introduites - on donne en appendice',
    'A single short typed hyphen closes the clause, and both layers already contain one hyphen.', 'First paragraph, notions introduites clause')

for p,count in [(78,3),(79,8),(80,2),(81,1),(82,2)]:
    id=f'ASTRA-I-O-{p:03d}'
    reason='Every structure-sheaf O on this personally compared page is a plain typed capital with one underline; none has a script outline. Preserve the visible underline at these exact occurrences without redefining a macro elsewhere.'
    r.own_finding(id,p,'underlined O_X',r'\mathcal O_X',r'\underline{O}_X',reason,'All structure-sheaf O occurrences')
    r.patch(p,'both',r'\mathcal O',r'\underline{O}',id,reason,count)
for p,count,words in [(79,3,'pseudo-cohérent (twice), complexe'),(80,4,'finie, parfaits, complexe, parfait'),(81,1,'globalement'),(82,3,'pseudo-cohérent, resp. parfait, relativement à')]:
    id=f'ASTRA-I-TERMS-{p:03d}'
    reason='The named word groups are upright type with underlines in the scanned page. Replace the italic emphasis command by an underline command only at those observed groups.'
    r.own_finding(id,p,'Underlined '+words,r'\emph{...}',r'\uline{...}',reason,'Defined/emphasized words')
    r.patch(p,'both',r'\emph{',r'\uline{',id,reason,count)
r.own_finding('ASTRA-I-CONVENTION-078-082',78,'Underlined plain O and upright underlined defined words',
    'Script O and italic defined words', 'Use explicit underline commands at the observed occurrences on78–82.',
    'The scan distinguishes the structure-sheaf letter by a rule and introduces the named terms with upright underlining. The mapping of each source occurrence to its printed glyph is listed in the page-specific patch records. D(X) remains plain D through the existing Db macro.',
    'ExposéI introduction, pages78–82',kind='convention',verdict='amended')
for p,b,e in [(78,'GÉNÉRALITÉS SUR LES CONDITIONS DE FINITUDE','localement une suite exacte'),(79,'L_n→L_{n−1}→...','tout O_X-Module'),(80,'cohérent F admet localement','localement bornée est parfait.'),(81,'Pseudo-cohérence et perfection','De tels critères'),(82,'sont donnés dans l’Exp. II.','F est parfait rel. à p')]:
    r.page(p,b,e,'Structure-sheaf and emphasis glyphs recorded as explicit local conventions.')
r.commit()
