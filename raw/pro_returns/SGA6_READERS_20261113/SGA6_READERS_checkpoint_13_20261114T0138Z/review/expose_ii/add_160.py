"""Explicit image findings for the opening page of Exposé II."""
import re
from review_helpers import Review,ROOT
r=Review()
for n,printed,reason,region in [
(35,'Exposé II on its own line, underlined, without a final stop','The attached heading preserves the printed words and punctuation. The exposé name and title occupy separate lines.','exposé heading'),
(36,'EXISTENCE DE RÉSOLUTIONS GLOBALES, capitals and double underline','Two parallel rules run below the capital title. The acute on RÉSOLUTIONS is visible. Both attached layers match.','exposé title'),
(37,'par L. ILLUSIE, underlined','The surname is in capitals, and the entire author line has a rule below it. Both attached layers match.','author line')]:
    r.finding('156_160',n,printed,reason,region)
r.finding('156_160',38,'Proposition1.1 statement prose is underlined by word groups',
    'The complete statement on folio160 has separate rules beneath the lexical groups, while its formulas and category symbols carry their own typography. The exact word groups are preserved by the page-specific patch. Further ExposéII pages require their own direct comparison.',
    'Proposition1.1, beginning through formée des com-',verdict='not applied and now applied',
    change='Underline the directly observed folio160 word groups; no unreviewed-page decision.',witness=171)
sid='ASTRA-II-C-160'
reason='All forty category C occurrences on this page are typed C with a separate underline beneath the letter. Subscripts stay outside the rule. This preserves the same category and fiber objects while distinguishing their printed letter form from the plain D and K functor letters.'
r.own_finding(sid,160,'Forty underlined category C letters',r'\mathcal C',r'\underline{C}',reason,'All category letters, including subscripts in the displayed equalities',kind='font',witness=171)
r.patch(160,'both',r'\mathcal C',r'\underline{C}',sid,reason,40)
sid='ASTRA-II-SITE-160'
reason='The site S is underlined in the site declaration, the two S-category phrases, and S∈ob S. The object S in that membership statement and all fiber subscripts S remain plain. Native witness171 confirms the short rule beneath sous-S, faint in the main scan. The occurrence map preserves site and object separately.'
r.own_finding(sid,160,'Four underlined site S occurrences; ordinary object and subscript S',r'plain S throughout',r'underline only the four site occurrences',reason,'Opening paragraph and first proposition line',kind='font',witness=171)
for old,new in [(r'un site $S$, une $S$-catégorie',r'un site $\underline{S}$, une $\underline{S}$-catégorie'),(r'une sous-$S$-catégorie',r'une sous-$\underline{S}$-catégorie'),(r'Soit $S\in\Ob S$',r'Soit $S\in\Ob \underline{S}$')]:
    r.patch(160,'both',old,new,sid,reason)
sid='ASTRA-II-NUMBER-160'
reason='The introductory paragraph number1.0. is ordinary type, independently of the separately underlined proposition label. Preserve its printed weight.'
r.own_finding(sid,160,'Plain paragraph number1.0.',r'\textbf{1.0.}','1.0.',reason,'Opening paragraph number',kind='font')
r.patch(160,'both',r'\textbf{1.0.}','1.0.',sid,reason)
sid='ASTRA-II-ACYCLIC-160'
reason='The native witness shows a small crossed loop in the superscript in both occurrences. The sentence identifies this K^{−,∅} as the full thick subcategory of acyclic complexes inside K^−, and the displayed quotient uses that inclusion. Retain the existing varnothing transcription of the inspected crossed-loop mark.'
r.own_finding(sid,160,'K^{−,∅} with a crossed-loop superscript',r'\mathrm K^{-,\varnothing}',r'Retain \varnothing',reason,'Final quotient and following definition',kind='symbol',verdict='confirmed',witness=171)
sid='ASTRA-II-UNDERLINE-160'
reason='The word groups listed in this patch have visible rules in the complete page image. Math units, references, enumeration labels, the exact page boundary and all textual tokens remain identical; only the observed word-group underline commands are introduced.'
r.own_finding(sid,160,'Underlined statement prose by lexical group','Plain statement prose',r'\uline around inspected word groups',reason,'Entire Proposition1.1 on this folio',kind='underline')
old=(ROOT/'build/page_packets/160/diplomatic.tex').read_text()
for p in r.patches: old=old.replace(p['old'],p['new'])
start=old.index(r'\textbf{Proposition 1.1.}')
head,body=old[:start],old[start:]
def replace(a,b,n=1):
    global body
    assert body.count(a)==n,(a,body.count(a),n)
    body=body.replace(a,b)
def wrap(a,n=1):replace(a,r'\uline{'+a+'}',n)
wrap('Soit')
wrap('et supposons que')
wrap('est quasi-relevable dans')
wrap('étant considérée comme catégorie fibrée sur un site ponctuel',2)
wrap('tout objet de')
wrap('qui est de')
wrap('-type fini',2)
wrap('resp. de')
wrap('-présentation finie')
replace(' est de ',r' \uline{est de} ')
wrap('Alors')
wrap("est quasi-stable par noyau d'épimorphisme")
wrap('Soient')
replace(' et $n',r' \uline{et} $n')
replace('Si $E',r'\uline{Si} $E')
replace(' est $n$-',r' \uline{est} $n$-',2)
wrap('-pseudo-cohérent',3)
replace('(resp. $(n+1)',r'(\uline{resp.} $(n+1)')
wrap("En d'autres termes")
wrap('on a',2)
replace('(resp.\n',r'(\uline{resp.}'+'\n')
wrap('inclusions de sous-catégories strictement pleines de')
wrap("l'inclusion de droite étant d'ailleurs triviale")
wrap('Pour que')
wrap('soit pseudo-cohérent relativement à')
wrap("il faut et il suffit qu'il le soit relativement à")
wrap('autrement dit')
wrap('En outre')
wrap('le foncteur canonique')
replace('où $',r'\uline{où} $')
wrap('désigne la sous-catégorie épaisse de')
replace('formée des\ncom%',r'\uline{formée des'+'\ncom}%')
new=head+body
assert re.sub(r'\\uline\{([^{}]*)\}',lambda m:m.group(1),new)==old
r.patch(160,'both',old,new,sid,reason)
r.page(160,'Exposé II — EXISTENCE DE RÉSOLUTIONS GLOBALES','formée des com-',
    'All words, formulas and their indices compared. Witness171 examined at the opening paragraph and final quotient for site rules and the crossed-loop superscript.',witness=171)
r.commit()
