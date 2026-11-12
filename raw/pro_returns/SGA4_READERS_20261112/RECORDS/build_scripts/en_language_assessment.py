"""Individual English-impact review of canonical agreed misprint records.

A translation impact assessment does not re-adjudicate the accepted French
correction. No reader is changed by this script.
"""
from pathlib import Path
from collections import Counter
import json,re
ROOT=Path(__file__).resolve().parents[1]
# Each listed expression is the unchanged English rendering of the French
# spelling/agreement repair. Entries were read individually, not inferred from
# the source model's class or confidence.
NO_IMPACT={
19:'is called discrete',26:'the strongest of all',28:'a monomorphism',40:'cogenerating subcategories',
46:'first',54:'a U-category',55:'cofinal',63:'adjoint',64:'quasi-inverse',67:'strict epimorphisms',
72:'a small family of cofinal functors',73:'two full subcategories',78:'projective systems',
85:'ind-objects',88:'the cokernel',97:'represented by',99:'cardinal',118:'for every arrow',
132:'an element',141:'the set of g≤h is finite',145:'the category of sheaves',
154:'a family of base-changeable morphisms',157:'the canonical topology',158:'the topologies',
160:'on C',162:'for every bicovering family',163:'the usual notation',164:'the third and fourth isomorphisms',
168:'for every covering family',172:'whose existence is asserted',177:'for every arrow',
181:'up to very little',182:'other topoi',183:'the sheaf H',185:'given',186:'the groups',
187:'fundamental group',191:'the associated category',199:'a big sheaf',212:'reconstitutes',
220:'a family such that',234:'smooth',246:'such ordered sets',261:'an intersection',
271:'every locally closed subtopos',283:'enough points',291:'a U-sheaf of rings',292:'projective limits',
360:'constant coefficients',362:'is defined',368:'a left adjoint',370:'abelian categories',
376:'resolutions formed',377:'the category equipped with',385:'proof left to the reader',
386:'the functors',387:'one equips',402:'degeneracy',404:'the form that will be used',
422:'a generating family',436:'the object defined by',438:'a finite family of commutative diagrams',
473:'makes the functors continuous',476:'an equivalent category',510:'every integer',
527:'affine schemes',532:'an equivalence of categories',533:'an equivalence of categories',
569:'surjective',576:'used',588:'a system of hyperplanes',593:'true',
605:'applying to a morphism',611:'the base-change homomorphisms',612:'the corresponding point',
617:'around',634:'ind-L-finite',635:'example',637:'every closed subset',638:'along Y',
646:'quotients which are flat',679:'morphism',680:'given by',718:'the standard example',
719:'the following arrows',721:'a subadditive category',725:'resolves',733:'the categories',
737:'triangulated',741:'Let',749:'make it commute',750:'pathological',753:'the isomorphism',
755:'a family of points',759:'They allow',760:'bounded above',763:'the composite of the arrows',
764:'the functors',770:'commute with base change',788:'the sole hypothesis',791:'remain valid',
797:'every geometric point',798:'the simplicial homology',803:'between smooth schemes',
824:'smoothable morphisms',828:'prime to the residual characteristics',833:'the groups being affine',
834:'the relative cotangent complex of',847:'effective relative Cartier divisors',
858:'canonically isomorphic to k',894:'two compatibilities',896:'cover U',908:'along',
}
# These are English lexical deltas, rather than French-only spelling changes.
# They are translations of the accepted source readings, not yet location claims.
LEXICAL={
2:('where at least','or at least'),24:('epimorphic (respectively strictly epimorphic)','strictly epimorphic (respectively epimorphic)'),
53:('pro-represents','ind-represents'),57:('fortiori','a fortiori'),65:('an equivalent of categories','an equivalence of categories'),
137:('to a predecessor','has a predecessor'),147:('where','or'),155:('of what precedes','what precedes'),
173:('it is immediately','it is immediate'),174:('a sheaf','a functor'),189:('a right adjoint','a left adjoint'),
200:('a left adjoint','a right adjoint'),222:('of functor','the functor'),227:('finite infima arbitrary suprema','finite infima and arbitrary suprema'),
233:('universally finite','universally closed'),240:('right exact','left exact'),243:('three types','four types'),
258:('follows the','follows from'),272:('or','where'),274:('reduce a case','reduce to the case'),
282:('to a small conservative family','has a small conservative family'),296:('to the sequence','has the sequence'),
304:('contains F','is contained in F'),309:('has a map','to a map'),333:('injective Modules and injective Modules','injective Modules into injective Modules'),
344:('a covering isomorphism','a covering morphism'),374:('i is an isomorphism','it is an isomorphism'),
399:('which as B','which covers B'),411:('the case or','the case where'),415:('replace ... for the closed images','replace ... by the closed images'),
420:('perhaps omitted','may be omitted'),434:('are the final object','whose final object'),
444:('and necessary','it is necessary'),447:('sub-subobjects','its subobjects'),455:('also follows 4.10','also follows from 4.10'),
470:('also sufficient','also necessary'),477:('where again','or again'),482:('canonical isomorphism','up to canonical isomorphism'),
502:('in an equivalence manner','equivalently'),514:('in which is finite projective limits','in which the finite projective limits'),
518:('without Q_e(V)','in Q_e(V)'),524:('has F','to F'),540:('Then canonical homomorphism','Then the canonical homomorphism'),
581:('where','or'),582:('has field of fractions','with field of fractions'),584:('where','or'),585:('the bundle','the fibre'),
589:('not defined','not infinite'),613:('refrain itself repeating','refrain from repeating'),618:('mapping-cylinders','mapping-cylinder'),
636:('quasi-complete','quasi-compact'),639:('a contrary','on the contrary'),643:('an isomorph','an isomorphism'),
652:('satisfied X is noetherian','satisfied when X is noetherian'),656:('that for L_0 admits','that L_0 admits'),
661:('We the exact sequence','We have the exact sequence'),671:('affine space dimension 1','affine space of dimension 1'),
714:('According to XI 3.3 and there exists','According to XI 3.3, there exists'),
720:('and a functor','is a functor'),790:('that morphism','that the morphism'),842:('where inverse image','or inverse image'),
876:('the fibres X−U','the fibres of X−U'),878:('It is immediately','It is immediate'),897:('right adjoint','left adjoint'),
}
NAMES={129:('Academie Press','Academic Press'),143:('Academie Press','Academic Press'),
383:('Tohokû','Tôhoku'),586:('Hironaha','Hironaka'),587:('reel','reell'),
695:('Abyankhar','Abhyankar'),789:('Artin-Scheier','Artin-Schreier'),808:('mutadis mutandis','mutatis mutandis'),
927:('Abyankhar','Abhyankar'),930:('Résolution','Resolution')}
# An uncertain printed name cannot receive an invented diplomatic English form.
UNRESOLVED={130:'The canonical record explicitly cannot read the overtyped printed surname. Kuratowski is the corrected name; the exact diplomatic English surname remains unverified and needs the held scan decision.'}
NO_IMPACT.update({754:'hypotheses',827:'degree',859:'effective',860:'very ample',909:'birational',925:'equidimensional'})
LEXICAL.update({873:('each section S over k','each scheme S over k'),902:('reduced Z/n(-d)','reduced to Z/n(-d)'),906:('to the leaves to the reader','one leaves to the reader')})
NAMES.update({880:('Kunneth','Künneth'),881:('Kunneth','Künneth'),929:('Abyankhar','Abhyankar')})
PUNCT={1,27,151,171,190,232,268,270,306,340,354,367,433,460,507,567,651,783,799,801}
PUNCT.add(707)
REPETITION={30,152,325,432,670,861}

def main():
    audit=json.loads((ROOT/'output/records/EN_SOURCE_AUDIT.json').read_text())
    ids=sorted({int(r['id'][2:]) for r in audit if r.get('status')=='requires English-language assessment' and re.fullmatch(r'MP\d{4}',r.get('id',''))})
    # Preserve the original reviewed scope when the English audit is rebuilt.
    scope=ROOT/'work_fr/en_assessment_ids.json'
    if scope.exists():ids=sorted(json.loads(scope.read_text()))
    records=json.loads((ROOT/'sources/fixes/MISPRINTS_4.json').read_text())
    disputed={(str(x['tome']),int(x['page'])) for x in json.loads((ROOT/'sources/api_pass_20261111/PAGES_FOR_APP_CHECK.json').read_text())}
    out=[]
    for n in ids:
        r=records[n-1];ident=f'MP{n:04d}'
        row={'id':ident,'expose':r['expose'],'page':r['page'],'source':f'fixes/MISPRINTS_4.json#{ident}',
             'printed_french':r['print'],'corrected_french':r['correct'],'place':r['where'],
             'held_disputed_page':(str(r['tome']),int(r['page'])) in disputed}
        if n in NO_IMPACT:
            row.update(assessment='no-impact',reason=f'The French spelling/agreement repair leaves the English rendering “{NO_IMPACT[n]}” unchanged; it adds no mathematical argument, qualifier, reference or variable.',english_reading=NO_IMPACT[n])
            if n==824:row['reason']='The French typo limifiables is repaired to lissifiables; the released English already names the same factorization as “smoothable morphisms” (XVIII p.483), which remains the term in both English forms.'
            if n==759:row['reason']='The plural French verb permettent and its antecedent résolutions already identify a plural subject; English “They allow” expresses that subject in both forms, without the French masculine/feminine distinction.'
            if n==770:row['reason']='The French number repair changement→changements leaves the English construction “commute with base change” unchanged.'
        elif n in UNRESOLVED:
            row.update(assessment='unresolved',reason=UNRESOLVED[n])
        else:
            row['assessment']='English-impact'
            if n in LEXICAL:
                a,b=LEXICAL[n]
                row.update(reason=f'The accepted French substitution changes the English words/construction: “{a}” → “{b}”; retain that distinction at the recorded occurrence.',english_delta={'printed':a,'corrected':b,'location_verified':False})
            elif n in NAMES:
                a,b=NAMES[n]
                row.update(reason=f'The name, retained title word or Latin phrase is carried into English verbatim: “{a}” → “{b}”.',english_delta={'printed':a,'corrected':b,'location_verified':False})
            elif n in PUNCT:
                row['reason']='The record changes a displayed delimiter or sentence punctuation at '+r['where']+'; its literal printed/corrected punctuation remains relevant in the English occurrence and requires an exact local anchor.'
            elif n in REPETITION:
                row['reason']='The record removes an explicitly repeated word, clause or mathematical label at '+r['where']+'; a diplomatic English occurrence must preserve the corresponding repeated material, with the corrected occurrence removing it.'
            else:
                row['reason']='The accepted reading changes an explicit mathematical symbol, argument, label, reference, or missing content at '+r['where']+'; that same recorded delta carries into the English text, beyond French spelling or agreement.'
        out.append(row)
    (ROOT/'output/records/EN_MISPRINT_LANGUAGE_ASSESSMENT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(len(out),dict(Counter(r['assessment'] for r in out)))
    print('No impact:',','.join(r['id'] for r in out if r['assessment']=='no-impact'))

if __name__=='__main__':main()
