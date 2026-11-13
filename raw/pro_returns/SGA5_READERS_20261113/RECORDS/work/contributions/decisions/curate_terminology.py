#!/usr/bin/env python3
"""Evidence inventory of technical vocabulary and its observed English forms.

This script changes no source text. Counts use the listed literal phrase forms,
case-insensitively, in body text before the indexes; source contexts are retained.
"""
from pathlib import Path
import argparse,bisect,csv,json,re
p=argparse.ArgumentParser();p.add_argument('--fr',default='work/sources/SGA5_FR/fr/sga5/current/s5.tex');p.add_argument('--en',default='work/contributions/english/EN_corrected_flat.tex');p.add_argument('--out',default='work/contributions/decisions');a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
F=Path(a.fr).read_text();E=Path(a.en).read_text()

# Each candidate English form is reported only when it actually occurs. The
# forms are search vocabulary, not an instruction to replace the author's text.
inventory=[
('préschéma|préschémas','prescheme|preschemes|pre-scheme|pre-schemes'),
('sous-préschéma|sous-préschémas','sub-prescheme|sub-preschemes|subprescheme|subpreschemes'),
('schéma|schémas','scheme|schemes'),
('faisceau|faisceaux','sheaf|sheaves'),
('faisceau constant|faisceaux constants','constant sheaf|constant sheaves'),
('localement constant|localement constante|localement constants|localement constantes','locally constant'),
('constant tordu|constante tordue|constants tordus|constantes tordues','twisted constant|twisted-constant|constant twisted'),
('faisceau constructible|faisceaux constructibles','constructible sheaf|constructible sheaves'),
('complexe dualisant|complexes dualisants','dualizing complex|dualizing complexes'),
('dualisant|dualisants','dualizing'),
('bidualisant|bidualisante|bidualisants|bidualisantes','bidualizing'),
('bidualité','biduality'),
('réflexif|réflexive|réflexifs|réflexives','reflexive'),
('dualité locale','local duality'),
('dimension quasi-injective','quasi-injective dimension'),
('dimension injective','injective dimension'),
('dimension cohomologique','cohomological dimension'),
('dimension topologique stricte','strict topological dimension'),
('tor-dimension','tor-dimension|tor dimension'),
('image directe|images directes','direct image|direct images|direct-image'),
('image inverse|images inverses','inverse image|inverse images|inverse-image|pullback|pull-back'),
('produit tensoriel|produits tensoriels','tensor product|tensor products|tensor-product'),
('produit tensoriel externe|produits tensoriels externes','external tensor product|external tensor products|external tensor-product'),
('somme directe|sommes directes','direct sum|direct sums'),
('produit fibré|produits fibrés','fibre product|fibre products|fiber product|fiber products'),
('fibre géométrique|fibres géométriques','geometric fibre|geometric fibres|geometric fiber|geometric fibers'),
('corps résiduel|corps résiduels','residue field|residue fields|residual field|residual fields'),
('caractéristique résiduelle|caractéristiques résiduelles','residual characteristic|residual characteristics|residue characteristic|residue characteristics'),
('limite inductive|limites inductives','inductive limit|inductive limits|direct limit|direct limits'),
('limite projective|limites projectives','projective limit|projective limits|inverse limit|inverse limits'),
('système projectif|systèmes projectifs','projective system|projective systems|inverse system|inverse systems'),
('système inductif|systèmes inductifs','inductive system|inductive systems|direct system|direct systems'),
('strictement local|strictement locale|strictement locaux|strictement locales','strictly local|strictly henselian|strict henselian'),
('localisé strict|localisés stricts|localisation stricte|localisations strictes','strict localization|strict localizations|strict localisation|strict localisations'),
('localement noethérien|localement noethérienne|localement noethériens|localement noethériennes','locally noetherian'),
('noethérien|noethérienne|noethériens|noethériennes','noetherian'),
('catégorie abélienne|catégories abéliennes','abelian category|abelian categories'),
('catégorie dérivée|catégories dérivées','derived category|derived categories'),
('catégorie triangulée|catégories triangulées','triangulated category|triangulated categories'),
('sous-catégorie pleine|sous-catégories pleines','full subcategory|full subcategories'),
('strictement pleine|strictement pleines','strictly full|strictly-full'),
('facteur direct|facteurs directs','direct factor|direct factors|direct summand|direct summands'),
('morphisme propre|morphismes propres','proper morphism|proper morphisms'),
('morphisme lisse|morphismes lisses','smooth morphism|smooth morphisms'),
('immersion fermée|immersions fermées','closed immersion|closed immersions|closed embedding|closed embeddings'),
('immersion ouverte|immersions ouvertes','open immersion|open immersions|open embedding|open embeddings'),
('épimorphisme|épimorphismes','epimorphism|epimorphisms'),
('monomorphisme|monomorphismes','monomorphism|monomorphisms'),
('noyau|noyaux','kernel|kernels'),
('conoyau|conoyaux','cokernel|cokernels|co-kernel|co-kernels'),
('endomorphisme|endomorphismes','endomorphism|endomorphisms'),
('automorphisme|automorphismes','automorphism|automorphisms'),
('morphisme de transition|morphismes de transition','transition morphism|transition morphisms|transition map|transition maps'),
('flèche|flèches','arrow|arrows|map|maps|morphism|morphisms'),
("flèche d'adjonction|flèches d'adjonction",'adjunction arrow|adjunction arrows|adjunction morphism|adjunction morphisms|adjunction map|adjunction maps'),
('isomorphisme canonique|isomorphismes canoniques','canonical isomorphism|canonical isomorphisms'),
('isomorphisme fonctoriel|isomorphismes fonctoriels','functorial isomorphism|functorial isomorphisms'),
('classe fondamentale|classes fondamentales','fundamental class|fundamental classes'),
('classe de Chern|classes de Chern','Chern class|Chern classes'),
('fibré vectoriel|fibrés vectoriels','vector bundle|vector bundles'),
('fibré projectif|fibrés projectifs','projective bundle|projective bundles'),
('sous-fibré|sous-fibrés','subbundle|subbundles|sub-bundle|sub-bundles'),
('puissance extérieure|puissances extérieures','exterior power|exterior powers'),
('algèbre extérieure|algèbres extérieures','exterior algebra|exterior algebras'),
('orientation|orientations','orientation|orientations'),
('supports propres','proper supports|compact supports'),
('cohomologie à supports propres','cohomology with proper supports|cohomology with compact supports|compactly supported cohomology|compact-support cohomology|compact support cohomology'),
('accouplement|accouplements','pairing|pairings|coupling|couplings'),
('cup-produit|cup-produits','cup-product|cup-products|cup product|cup products'),
('produit de Yoneda|produits de Yoneda','Yoneda product|Yoneda products'),
('changement de base|changements de base','base change|base changes|base-change'),
('correspondance cohomologique|correspondances cohomologiques','cohomological correspondence|cohomological correspondences'),
('correspondance équivariante|correspondances équivariantes','equivariant correspondence|equivariant correspondences'),
('terme local|termes locaux','local term|local terms'),
('formule des traces|formules des traces','trace formula|trace formulas'),
('formule de Lefschetz|formules de Lefschetz','Lefschetz formula|Lefschetz formulas'),
('diviseur|diviseurs','divisor|divisors'),
('croisements normaux','normal crossings|normal-crossings'),
('normalisé|normalisée|normalisés|normalisées','normalized|normalised'),
('normalisation','normalization|normalisation'),
('point fermé|points fermés','closed point|closed points'),
('point géométrique|points géométriques','geometric point|geometric points'),
('point fixe|points fixes','fixed point|fixed points|fixed-point'),
('multiplicité|multiplicités','multiplicity|multiplicities'),
('fonction caractéristique|fonctions caractéristiques','characteristic function|characteristic functions'),
('fonction centrale|fonctions centrales','class function|class functions|central function|central functions'),
('représentation régulière|représentations régulières','regular representation|regular representations'),
("représentation d'Artin|représentations d'Artin",'Artin representation|Artin representations'),
('représentation de Swan|représentations de Swan','Swan representation|Swan representations'),
('nombre de Lefschetz|nombres de Lefschetz','Lefschetz number|Lefschetz numbers'),
('nombre de Nielsen-Wecken|nombres de Nielsen-Wecken','Nielsen-Wecken number|Nielsen-Wecken numbers'),
('trace|traces','trace|traces'),
('cotrace|co-trace','cotrace|co-trace'),
('faisceau normal|faisceaux normaux','normal sheaf|normal sheaves'),
('faisceau conormal|faisceaux conormaux','conormal sheaf|conormal sheaves'),
('morphisme de Frobenius|morphismes de Frobenius','Frobenius morphism|Frobenius morphisms'),
('endomorphisme de Frobenius|endomorphismes de Frobenius','Frobenius endomorphism|Frobenius endomorphisms'),
('Frobenius géométrique','geometric Frobenius'),
('Frobenius arithmétique','arithmetic Frobenius'),
('dévissage|dévissages','dévissage|devissage'),
('fidèlement plat|fidèlement plate|fidèlement plats|fidèlement plates','faithfully flat'),
('module projectif|modules projectifs','projective module|projective modules'),
('module libre|modules libres','free module|free modules'),
('de type fini','of finite type|finitely generated|finite-type'),
('de présentation finie','of finite presentation|finitely presented|finite-presentation'),
('complexe parfait|complexes parfaits','perfect complex|perfect complexes'),
('pseudo-cohérent|pseudo-cohérente|pseudo-cohérents|pseudo-cohérentes','pseudo-coherent|pseudocoherent'),
('borné à droite|bornée à droite|bornés à droite|bornées à droite','bounded on the right|right bounded|right-bounded|bounded above'),
('borné à gauche|bornée à gauche|bornés à gauche|bornées à gauche','bounded on the left|left bounded|left-bounded|bounded below'),
('homotopie|homotopies','homotopy|homotopies'),
('acyclique|acycliques','acyclic'),
('quasi-isomorphisme|quasi-isomorphismes','quasi-isomorphism|quasi-isomorphisms'),
('rationalité','rationality'),
('anneau normal|anneaux normaux','normal ring|normal rings'),
('clôture normale','integral closure|normal closure'),
('sous-groupe distingué|sous-groupes distingués','normal subgroup|normal subgroups|distinguished subgroup|distinguished subgroups'),
('sommets','vertices|sums'),
('conjuguer|conjuguant','combine|combining|conjugate|conjugating'),
('ensemble des morphismes','set of morphisms|set of isomorphisms'),
]

def retrieval_view(t):
    # Preserve raw offsets while omitting layout-only markup from searches.
    idx_end=min([v for v in [t.find(r'\section*{Index terminologique}'),t.find(r'\section*{Terminological Index}')] if v>=0] or [len(t)])
    start=t.find(r'\begin{document}')+len(r'\begin{document}')
    t=t[:idx_end];chars=[];pos=[];i=start
    commands=re.compile(r'\\(?:emph|textbf|textit|textsc|uline|underline|noindent|textnormal|textrm)\b\s*\{?')
    while i<len(t):
        if t[i]=='%' and (i==0 or t[i-1]!='\\'):
            j=t.find('\n',i);i=len(t) if j<0 else j;continue
        m=commands.match(t,i)
        if m:i=m.end();continue
        if t[i] in '{}':i+=1;continue
        c=' ' if t[i].isspace() or t[i]=='~' else t[i]
        if c==' ' and chars and chars[-1]==' ':i+=1;continue
        chars.append(c);pos.append(i);i+=1
    return ''.join(chars),pos

FV,FP=retrieval_view(F);EV,EP=retrieval_view(E)
marks=[(m.start(),int(m.group(1))) for m in re.finditer(r'folio\s+(\d+)\s+%',F)]
mark_positions=[p for p,f in marks]
def folio(offset):
    i=bisect.bisect_right(mark_positions,offset)-1
    return marks[i][1] if i>=0 else None
def find(view,positions,forms):
    result=[]
    for form in forms:
        pat=r'(?<![\w-])'+re.escape(form).replace(r'\ ',r'\s+')+r'(?![\w-])'
        found=list(re.finditer(pat,view,re.I))
        if found:
            result.append({'form':form,'count':len(found),'first_offset':positions[found[0].start()],'first_excerpt':view[max(0,found[0].start()-70):found[0].end()+100]})
    return result
rows=[]
for i,(fr,en) in enumerate(inventory,1):
    fs=fr.split('|');es=en.split('|');fobs=find(FV,FP,fs);eobs=find(EV,EP,es)
    if not fobs and not eobs:continue
    first=min((r['first_offset'] for r in fobs),default=None)
    rows.append({'id':f'BODY-TERM-{i:03d}','French_term':fs[0],'French_search_forms':fs,'English_search_forms':es,'French_observed_forms':fobs,'English_observed_forms':eobs,'French_body_count':sum(r['count'] for r in fobs),'English_body_count':sum(r['count'] for r in eobs),'first_French_folio':folio(first) if first is not None else None,'first_French_offset':first,'multiple_English_spellings_or_inflections':len(eobs)>1,'status':'Observed lexical inventory; inflections and contextual translation alternatives require source-paragraph review before any editorial change.'})
(out/'body_terminology_inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (out/'body_terminology_inventory.tsv').open('w',newline='') as f:
    names=['id','French_term','French_search_forms','English_observed_forms','French_body_count','English_body_count','first_French_folio','status'];w=csv.DictWriter(f,fieldnames=names,delimiter='\t');w.writeheader()
    for r in rows:w.writerow({k:('|'.join(r[k]) if k=='French_search_forms' else '; '.join(x['form']+' ['+str(x['count'])+']' for x in r[k]) if k=='English_observed_forms' else r[k]) for k in names})

sol_variants=[
 {'French_term':'sommets','earlier_English':'sums','selected_English':'vertices','folio':88,'source_id':'SOL-EN-008','disposition':'repair exact phrase the sums of this square to the vertices of this square'},
 {'French_term':'conjuguer; en conjuguant','earlier_English':'conjugate; conjugating','selected_English':'combine; combining','folio':'177,202','source_id':'SOL-EN-042; SOL-EN-061','disposition':'repair the two deductions combining named formulas; preserve conjugation in its other mathematical contexts'},
 {'French_term':'ensemble des morphismes','earlier_English':'set of isomorphisms','selected_English':'set of morphisms','folio':216,'source_id':'SOL-EN-063','disposition':'restore the exact source definition of Homprime_AR(X,Y)'},
 {'French_term':'sous-groupe distingué','earlier_English':'distinguished subgroup','selected_English':'normal subgroup','folio':440,'source_id':'SOL-EN-082','disposition':'render the subgroup property gH_1g^{-1}=H_1, whose quotient H/H_1 is used in the passage'},
 {'French_term':'clôture normale de Z_ell dans Omega','earlier_English':'normal closure','selected_English':'integral closure','folio':470,'source_id':'SOL-EN-083','disposition':'the coefficient ring consists of a in Omega satisfying a monic polynomial with coefficients in Z_ell; translate the term for that same ring'},
 {'French_term':'faisceau normal','earlier_English':'normal sheaf','selected_English':'normal sheaf','folio':299,'source_id':'REVIEW-5-01','disposition':'retain the recorded print; conormal sheaf is only the unresolved alternative associated with the handwritten co'},
 {'French_term':'SGA A; SGAA','earlier_English':'SGA A; SGAA','selected_English':'SGA A; SGAA','folio':'1,19','source_id':'SOL-EN-088','disposition':'authorial alias explicitly identified as SGA4 in the introduction; keep the cited notation'},
 {'French_term':'Hom with an underline','earlier_English':'plain Hom at the specified 34 occurrences; plain RHom at 69+7 occurrences','selected_English':'uHom or uRHom at those exact occurrences','folio':'171-182,201-202','source_id':'SOL-EN-034; SOL-EN-060','disposition':'copy the exact French underline assignment; seven later plain Hom and two plain RHom factors retain their matched source forms'},
]
(out/'SOL_glossary_variants.json').write_text(json.dumps(sol_variants,ensure_ascii=False,indent=2)+'\n')
summary={'curated_phrase_families':len(inventory),'observed_rows':len(rows),'rows_with_French_body_evidence':sum(bool(r['French_observed_forms']) for r in rows),'rows_with_English_body_evidence':sum(bool(r['English_observed_forms']) for r in rows),'exact_SOL_terminology_dispositions':len(sol_variants),'count_definition':'Case-insensitive occurrences of the explicitly listed literal phrase forms in text before the indexes, with emphasis wrappers and repeated whitespace omitted only in the search view. Counts can overlap between nested phrases; no source text is changed.','next_step':'Use the exact 108 index pairs as the glossary core, this body inventory for additional observed terms, and aligned paragraph evidence to distinguish contextual alternatives from slips.'}
(out/'body_terminology_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
