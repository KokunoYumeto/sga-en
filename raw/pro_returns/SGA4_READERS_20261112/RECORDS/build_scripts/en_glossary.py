"""Build an auditable bilingual glossary from the supplied English text.

Counts are observed English occurrences on paired printed pages that also
contain the stated French term. No unobserved dictionary entries are emitted.
"""
from en_common import *
from build_en import page_markers
import collections

TERMS=r'''
faisceau|sheaf
faisceaux|sheaves
préfaisceau|presheaf;pre-sheaf
préfaisceaux|presheaves;pre-sheaves
faisceau associé|associated sheaf;sheafification
faisceau constant|constant sheaf
faisceau localement constant|locally constant sheaf
faisceau constructible|constructible sheaf
faisceau cohérent|coherent sheaf
faisceau quasi-cohérent|quasi-coherent sheaf;quasicoherent sheaf
faisceau abélien|abelian sheaf
faisceau de groupes|sheaf of groups;group sheaf
faisceau de modules|sheaf of modules;module sheaf
faisceau d'anneaux|sheaf of rings;ring sheaf
faisceau flasque|flasque sheaf;flabby sheaf
faisceau mou|soft sheaf
foncteur|functor
foncteurs|functors
foncteur exact|exact functor
exact à gauche|left exact;left-exact
exact à droite|right exact;right-exact
foncteur dérivé|derived functor
foncteurs dérivés|derived functors
foncteur adjoint|adjoint functor
adjoint à gauche|left adjoint
adjoint à droite|right adjoint
quasi-inverse|quasi-inverse;quasi inverse
pleinement fidèle|fully faithful
fidèle|faithful
essentiellement surjectif|essentially surjective
conservatif|conservative
représentable|representable
pro-représentable|pro-representable
ind-représentable|ind-representable
foncteur fibre|fiber functor;fibre functor
foncteurs fibres|fiber functors;fibre functors
foncteur d'oubli|forgetful functor
morphisme de foncteurs|morphism of functors;natural transformation
transformation naturelle|natural transformation
catégorie|category
catégories|categories
petite catégorie|small category
catégorie abélienne|abelian category
catégorie additive|additive category
catégorie dérivée|derived category
catégorie triangulée|triangulated category
catégorie opposée|opposite category
catégorie duale|dual category;opposite category
catégorie discrète|discrete category
catégorie filtrante|filtered category;filtering category
catégorie cofiltrante|cofiltered category;cofiltering category
catégorie fibrée|fibered category;fibred category
catégories fibrées|fibered categories;fibred categories
catégorie cofibrée|cofibered category;cofibred category
catégorie localisée|localized category;localization
catégorie quotient|quotient category
catégorie des ensembles|category of sets
catégorie des groupes|category of groups
catégorie des modules|category of modules
sous-catégorie pleine|full subcategory
objet|object
objets|objects
objet initial|initial object
objet final|final object;terminal object
objet nul|zero object
objet injectif|injective object
objet projectif|projective object
objet compact|compact object
objet cohérent|coherent object
sous-objet|subobject;sub-object
quotient|quotient
produit|product
produit fibré|fiber product;fibered product;fibre product
produits fibrés|fiber products;fibered products;fibre products
produit tensoriel|tensor product
produits tensoriels|tensor products
somme directe|direct sum
sommes directes|direct sums
somme amalgamée|amalgamated sum;pushout
somme|sum;coproduct
coproduit|coproduct
limite projective|projective limit;inverse limit
limites projectives|projective limits;inverse limits
limite inductive|inductive limit;direct limit;colimit
limites inductives|inductive limits;direct limits;colimits
limite inductive filtrante|filtered inductive limit;filtered direct limit;filtered colimit
limites inductives filtrantes|filtered inductive limits;filtered direct limits;filtered colimits
limites finies|finite limits
noyau|kernel
conoyau|cokernel
image directe|direct image;pushforward
images directes|direct images;pushforwards
image inverse|inverse image;pullback
images inverses|inverse images;pullbacks
image réciproque|inverse image;pullback
images réciproques|inverse images;pullbacks
monomorphisme|monomorphism
monomorphismes|monomorphisms
épimorphisme|epimorphism
épimorphismes|epimorphisms
épimorphisme strict|strict epimorphism
monomorphisme strict|strict monomorphism
isomorphisme|isomorphism
isomorphismes|isomorphisms
morphisme|morphism
morphismes|morphisms
flèche|arrow;map
flèches|arrows;maps
but|target;codomain
source|source;domain
section|section
rétraction|retraction
scindé|split
diagramme commutatif|commutative diagram
carré cartésien|cartesian square;Cartesian square;pullback square
cartésien|cartesian;Cartesian
cocartésien|cocartesian;cocartesian
équivalence|equivalence
relation d'équivalence|equivalence relation
relations d'équivalence|equivalence relations
ensemble|set
ensembles|sets
ensemble ordonné|ordered set;partially ordered set
partiellement ordonné|partially ordered
préordre|preorder;pre-order
cardinal|cardinal;cardinality
univers|universe
petit|small
crible|sieve
cribles|sieves
topologie|topology
topologies|topologies
prétopologie|pretopology;pre-topology
site|site
sites|sites
topos|topos;topoi
topologie canonique|canonical topology
topologie étale|étale topology;etale topology
topologie de Zariski|Zariski topology
topologie grossière|coarse topology;indiscrete topology
topologie discrète|discrete topology
recouvrement|covering;cover
recouvrements|coverings;covers
famille couvrante|covering family
familles couvrantes|covering families
hypercentre|hypercenter;hypercentre
hyperrecouvrement|hypercovering;hypercover
hyperrecouvrements|hypercoverings;hypercovers
point géométrique|geometric point
points géométriques|geometric points
localisation|localization;localisation
localisé strict|strict localization;strict localization
topos ponctuel|punctual topos;point topos
topos cohérent|coherent topos
topos local|local topos
topos annelé|ringed topos
topos fibré|fibered topos;fibred topos
recollement|gluing;glueing
descente|descent
descente effective|effective descent
descente cohomologique|cohomological descent
donnée de descente|descent datum
données de descente|descent data
descente universelle|universal descent
champ|stack
champs|stacks
gerbe|gerbe
gerbes|gerbes
torseur|torsor
torseurs|torsors
schéma|scheme
schémas|schemes
préschéma|prescheme;pre-scheme
préschémas|preschemes;pre-schemes
schéma affine|affine scheme
schéma noethérien|noetherian scheme;Noetherian scheme
schéma local|local scheme
anneau local|local ring
anneau hensélien|henselian ring;Henselian ring
strictement local|strictly local
hensélisé|henselization;henselisation
hensélisé strict|strict henselization;strict henselisation
corps résiduel|residue field
corps de fonctions|function field
corps des fractions|field of fractions;fraction field
corps algébriquement clos|algebraically closed field
séparablement clos|separably closed
purement inséparable|purely inseparable
séparable|separable
radiciel|radicial;purely inseparable
radicielle|radicial;purely inseparable
étale|étale;etale
étales|étale;etale
lisse|smooth
plat|flat
propre|proper
séparé|separated
quasi-séparé|quasi-separated;quasiseparated
quasi-compact|quasi-compact;quasicompact
quasi-projectif|quasi-projective;quasiprojective
projectif|projective
quasi-fini|quasi-finite;quasifinite
de type fini|of finite type
de présentation finie|of finite presentation
dimension relative|relative dimension
dimension cohomologique|cohomological dimension
dimension homologique|homological dimension
image fermée|closed image
immersion fermée|closed immersion
immersion ouverte|open immersion
immersion|immersion
support|support
supports|supports
support propre|proper support
supports propres|proper supports
cohomologie à supports propres|cohomology with proper supports;compactly supported cohomology
cohomologie à support propre|cohomology with proper support
cohomologie étale|étale cohomology;etale cohomology
cohomologie|cohomology
homologie|homology
complexe|complex
complexes|complexes
complexe borné|bounded complex
borné inférieurement|bounded below
borné supérieurement|bounded above
résolution injective|injective resolution
résolution projective|projective resolution
acyclique|acyclic
acyclicité|acyclicity
localement acyclique|locally acyclic
asphérique|aspherical
suite exacte|exact sequence
suites exactes|exact sequences
suite spectrale|spectral sequence
suites spectrales|spectral sequences
filtration|filtration
gradué|graded
bigradué|bigraded;bi-graded
différentielle|differential
homotopie|homotopy
quasi-isomorphisme|quasi-isomorphism
troncature|truncation
tronqué|truncated
dualité|duality
dual|dual
faisceau dualisant|dualizing sheaf;dualising sheaf
complexe dualisant|dualizing complex;dualising complex
formule de projection|projection formula
changement de base|base change;base-change
spécialisation|specialization;specialisation
générisation|generalization;generization;generisation
normalisation|normalization;normalisation
revêtement|covering;cover
revêtements|coverings;covers
revêtement galoisien|Galois covering;Galois cover
groupe fondamental|fundamental group
monodromie|monodromy
connexe|connected
connexité|connectedness
irréductible|irreducible
géométriquement unibranche|geometrically unibranch
diviseur|divisor
diviseurs|divisors
diviseur de Cartier|Cartier divisor
cycle|cycle
cycles|cycles
classe de Chern|Chern class
classes de Chern|Chern classes
classe fondamentale|fundamental class
trace|trace
produit cup|cup product
puissance symétrique|symmetric power
puissances symétriques|symmetric powers
objet simplicial|simplicial object
objet cosimplicial|cosimplicial object
cosquelette|coskeleton
squelette|skeleton
dégénérescence|degeneracy
augmentation|augmentation
complexe simple|simple complex;total complex
complexe total|total complex
double complexe|double complex
produit total|total product
limite homotopique|homotopy limit
fibré vectoriel|vector bundle
faisceau inversible|invertible sheaf;line bundle
invertible|invertible
unité|unit
racines de l'unité|roots of unity
torsion|torsion
sans torsion|torsion-free;torsion free
annulateur|annihilator
platitude|flatness
finitude|finiteness
localement constant constructible|locally constant constructible
dévisser|devissage;dévisser
dévissage|dévissage;devissage
'''

def text_only(s):
    s=uncomment(s)
    s=re.sub(r'\\SGApage\{[^}]*\}\{[^}]*\}\{[^}]*\}',' ',s)
    s=re.sub(r'\\(?:hyperref|eqhyperref)\[[^]]*\]\{([^{}]*)\}',r'\1',s)
    s=re.sub(r'\\[A-Za-z@]+(?:\[[^]]*\])?',' ',s)
    s=re.sub(r'[{}$]',' ',s)
    return re.sub(r'\s+',' ',s)

def pattern(phrase):
    return re.compile(r'(?<!\w)'+re.escape(phrase).replace(r'\ ',r'\s+')+r'(?!\w)',re.I)

def selected_sisi(s):
    edits=[]
    for m in active_matches(r'\\sisi\b',s):
        if any(a<=m.start()<b for a,b,_ in edits):continue
        try:
            _,_,j,_=group(s,m.end());value,_,j,_=group(s,j)
        except ValueError:continue
        edits.append((m.start(),j,selected_sisi(value)))
    return replace_spans(s,edits)

def corpus_pages():
    french={};english={}
    for d in DIRS:
        text,markers=french_marker_map(d)
        edits=[(a,a+len(r'\pageoriginale'),r'\SGApage{'+str(p['tome'])+'}{'+p['expose']+'}{'+str(p['folio'])+'}') for a,ln,p in markers]
        text=selected_sisi(replace_spans(text,edits))
        mm=list(re.finditer(r'\\SGApage\{[^}]*\}\{[^}]*\}\{(\d+)\}',text))
        for i,m in enumerate(mm):
            b=mm[i+1].start() if i+1<len(mm) else len(text)
            french[(d,int(m.group(1)))]=text_only(text[m.end():b])
    s=selected_sisi(page_markers(RELEASE.read_text()))
    for f in fragment_blocks(s):
        t=f['text'];mm=list(re.finditer(r'\\SGApage\{[^}]*\}\{[^}]*\}\{(\d+)\}',t))
        previous=max([p for d,p in english if d==f['file']],default=None)
        bounds=[(0,previous)]+[(m.end(),int(m.group(1))) for m in mm]
        for i,(a,page) in enumerate(bounds):
            b=mm[i].start() if i<len(mm) else len(t)
            if page is not None:
                english.setdefault((f['file'],page),'')
                english[(f['file'],page)]+=' '+text_only(t[a:b])
    return french,english

def main():
    fr,en=corpus_pages();rows=[];evidence=[]
    from glossary_source_spans import main as source_span_terms
    observed=source_span_terms()
    vocabulary=collections.defaultdict(set)
    labels={}
    for line in TERMS.strip().splitlines():
        term,renderings=line.split('|')
        labels.setdefault(term.casefold(),term)
        vocabulary[term.casefold()].update(renderings.split(';'))
    for term,renderings in observed.items():
        labels.setdefault(term.casefold(),term)
        vocabulary[term.casefold()].update(renderings)
    for termkey,renderings in vocabulary.items():
        term=labels[termkey]
        fpat=pattern(term)
        # Search a spelling once, then split counts by the actual case in the
        # English source. Cartesian and cartesian never count the same hit.
        searches={r.casefold():r for r in sorted(renderings)}
        for rendering in searches.values():
            epat=pattern(rendering);counts=collections.Counter();first={};examples=collections.defaultdict(list)
            for key,ft in fr.items():
                if not fpat.search(ft):continue
                et=en.get(key,'');matches=list(epat.finditer(et))
                for m in matches:
                    place=EXPOSE[key[0]]+' p. '+str(key[1])
                    actual=re.sub(r'\s+',' ',m.group())
                    first.setdefault(actual,place);counts[actual]+=1
                    if len(examples[actual])<3:examples[actual].append(place+': '+et[max(0,m.start()-55):m.end()+70])
            for actual,count in counts.items():
                rows.append(dict(french_term_or_notation=term,english_rendering=actual,count=count,first_place=first[actual],method='paired-page attestation; exact English case'))
                evidence.append(dict(french_term=term,english_rendering=actual,count=count,examples=' | '.join(examples[actual])))
    # Stable named notation is retained verbatim in the existing translation.
    baseline=RELEASE.read_text();frags=fragment_blocks(baseline)
    notation=collections.defaultdict(lambda:[0,''])
    for f in frags:
        place=EXPOSE[f['file']]+'; '+f['name']
        for m in active_matches(r'\\(?:[A-Z][a-z]|Hhom|Eext|Hom|Ext|Tor|Spec|varinjlim|varprojlim|bigdot|PP|ZZ|QQ|NN|RR|CC)\b',f['text']):
            name=m.group();notation[name][0]+=1
            if not notation[name][1]:notation[name][1]=place
    for name,(count,place) in sorted(notation.items()):rows.append(dict(french_term_or_notation=name,english_rendering=name,count=count,first_place=place,method='unchanged named TeX notation'))
    rows.sort(key=lambda r:(r['french_term_or_notation'].casefold(),r['english_rendering']))
    write_tsv(RECORDS/'GLOSSARY_SGA4_FR_EN.tsv',rows,['french_term_or_notation','english_rendering','count','first_place','method'])
    write_tsv(RECORDS/'GLOSSARY_EVIDENCE.tsv',evidence,['french_term','english_rendering','count','examples'])
    groups=collections.defaultdict(list)
    for r in rows:
        if r['method'].startswith('paired-page'):groups[r['french_term_or_notation']].append(r)
    inconsistent={k:v for k,v in groups.items() if len(v)>1}
    out=['# Observed glossary variation','',
    'This report enumerates every multiple rendering in the glossary. The vocabulary combines '+
    'the source terminology in `build_scripts/en_glossary.py` with an enumeration of all emphasized '+
    'source spans in the 271 supplied translation fragments. `GLOSSARY_SOURCE_CENSUS.json` retains '+
    'every French emphasis span; `GLOSSARY_SOURCE_SPANS.tsv` records raw French and English spans, '+
    'their source fragment, the exact index pairing, and each typography projection. '+
    'Twenty-three unequal emphasis sequences have explicit reviewed maps. Long mathematical '+
    'statements remain in that evidence inventory; their content is not shortened into a term. '+
    'Entries are counted only when '+
    'the French phrase and the English rendering occur on paired printed pages. Counts are '+
    'English occurrences on those paired pages, not an inferred one-to-one word alignment. '+
    'English case is counted exactly: Cartesian and cartesian have disjoint occurrence counts. '+
    'The selected corrected sides of the original human sisi records are counted once. '+
    'The glossary also counts unchanged named TeX notation. `GLOSSARY_EVIDENCE.tsv` gives examples.', '',
    'Terminology has been left as in the released English. The records below identify variation; '+
    'a matching page may contain a different construction, and the evidence does not justify '+
    'replacing a valid technical rendering merely to reduce the number of forms.', '',
    f'Glossary rows: {len(rows)}. French terms with observed alternative renderings: {len(inconsistent)}.','']
    for term,rr in sorted(inconsistent.items()):
        out+=['## '+term,'','| English rendering | Count | First place |','|---|---:|---|']
        for r in rr:out.append('| '+r['english_rendering']+' | '+str(r['count'])+' | '+r['first_place']+' |')
        out.append('')
    (RECORDS/'GLOSSARY_INCONSISTENCIES.md').write_text('\n'.join(out)+'\n')
    print(json.dumps({'glossary_rows':len(rows),'terms':len(groups),'multiple_renderings':len(inconsistent),'notation':len(notation)}))

if __name__=='__main__':main()
