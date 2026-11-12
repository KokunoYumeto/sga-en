"""Reproduce the individual textual judgements of the one-model records.

Inputs retain their ZIP-relative names. No scan claim is independently verified.
Explicit ID decisions are the review; locating candidate TeX is a separate step.
"""
from pathlib import Path
import csv, difflib, json, re, unicodedata

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'
OUT=ROOT/'output'/'records'
OUT.mkdir(parents=True,exist_ok=True)
PAGES=json.loads((SRC/'api_pass_20261111/PAGES.json').read_text())
DP={(str(x['tome']),x['page']) for x in json.loads((SRC/'api_pass_20261111/PAGES_FOR_APP_CHECK.json').read_text())}
EXPOSE_FILES={x['expose']:x['file'] for x in PAGES}

# The lexical/agreement records were read individually. These exceptions either
# propose a mathematical change, require external bibliographic verification,
# or impose an optional wording/notation change.
LANGUAGE_HOLDS={
 'OPUS':{5:'The coproduct description must be compared with its adjunction before reversing left and right.',102:'Both past and present verb forms are grammatical; the reported tense change needs the whole sentence.',161:'The supplied record establishes a spelling preference but gives no textual test of the author\'s intended accent.'},
 'SOL':{
 21:'The proposed reversal of the adjunction requires comparison with the coproduct formula and its Hom bijection.',
 40:'Deleting stricts changes a generating hypothesis; the supplied snippet does not establish the exact hypothesis used in the proof.',
 57:'The finiteness qualifier changes the theorem; equivalence of the two listed conditions needs proof from the surrounding statement.',
 67:'The phrase le cas is grammatically complete; ce cas supplies a stylistic preference rather than an established misprint.',
 97:'Changing pro-objets to ind-objets requires checking the variance and the displayed adjunction.',
 105:'Reversing exactitude à droite to à gauche requires checking the hypothesis and the argument, beyond this quoted phrase.',
 201:'The target category of the inverse-image assignment requires an explicit check of the domain/codomain convention used here.',
 233:'The distinction between the associated presheaf and sheaf functor requires the definition of the functor a in this argument.',
 253:'Adding an item label is structurally plausible, but the proposed absent printed label cannot be verified from this source record alone.',
 263:'The term sous-objets may refer to a specified object or subcategory; its replacement needs the full construction.',
 297:'Reordering the analytic cases requires matching all three cases with the preceding definition.',
 362:'Changing projective to inductive limit changes the complex; its universal construction needs independent checking.',
 389:'The reported spelling needs identification of the particular named theorem; the supplied record contains two competing names.',
 392:'The proposed repair changes both the article and the number of hyper-recouvrements; the intended category must be checked.',
 430:'The author-name correction requires a bibliographic authority beyond the quoted entry.',
 432:'The title\'s exact plural requires comparison with the cited publication.',
 433:'The publisher\'s exact spelling requires comparison with the cited edition.',
 446:'Replacing fermés by formés changes the description of the complexes and requires the construction of L.',
 448:'Removing the D qualification changes the objects described; the fibre construction needs independent verification.',
 449:'The sentence is incomplete, but the exact supplied subject/object Nous la is an editorial reconstruction.',
 455:'A morphism can be mentioned without asserting invertibility; the stronger conclusion requires the lemma\'s proof.',
 470:'Singularizing these isomorphisms requires identifying all isomorphisms referred to in the preceding sentence.',
 471:'A second name for the auxiliary scheme is plausible, but the proposed prime requires comparison with the whole factorization.',
 480:'The author-name correction requires a bibliographic authority beyond the quoted entry.',
 504:'The prefix pré changes the finiteness condition; the proof must be compared with condition (ii).',
 560:'Changing fibrées to fibres changes the category referred to and needs the surrounding fibre construction.',
 563:'Changing fibrés to fibres changes which topoi carry the induced maps and needs the localization definition.',
 592:'The prime on this arrow requires matching its endpoints and the preceding factorization.',
 622:'The cited book title needs verification against the publication.',
 623:'The exact article title needs verification against the publication.',
 629:'The number of the cited subassertion requires checking both parts of Proposition 4.1.',
 689:'The broken sentence establishes a lacuna, but it does not uniquely determine the proposed explanatory completion.',
 710:'The empty reference is an authorial lacuna; deleting it supplies no verified target and would conceal that lacuna.',
 715:'The exact title wording requires comparison with the cited article.',
 802:'The diagram may be induced from schemes; replacing its descriptive noun requires the intended level of the construction.',
 825:'The duplicated phrase may signal an unfinished construction; deleting it requires the complete sentence and its morphisms.',
 1023:'The base of all complexes in the prism requires an endpoint check of its functors.',
 1091:'Changing isomorphisme to morphisme enlarges the hypothesis materially and requires the proof of the Künneth criterion.',
 1236:'The third prime requires identifying the row\'s exact-sequence object throughout the diagram.',
 1240:'The cited book title needs verification against the publication.',
 }
}
REJECT={
 ('OPUS',11):'The change proobjets → pro-objets only inserts a hyphen in the same term; no malformed construction or change of meaning is exhibited.',
 ('OPUS',25):'The reference (2) already has a matched pair of parentheses and designates item 2; removing one parenthesis would impose a label style.',
 ('OPUS',131):'A semicolon separates the two displayed arguments just as the proposed comma does; the record supplies no syntax defect to repair.',
 ('OPUS',234):'The two expressions supply the same three listed arguments in the same order; replacing the first separator is a notation preference unsupported as a misprint.',
 ('OPUS',235):'The displayed arguments remain 0,x,x in the same order; replacing the first comma by a semicolon only enforces another separator convention.',
 ('SOL',67):'The phrase le cas is grammatically complete; the record supplies no uniquely required replacement by ce cas.',
 ('SOL',710):'Deleting the empty reference would hide a documented lacuna without recovering its target; retain it.',
}

# Independent syntactic/lexical conclusions for records classified mathematics.
OPUS_SIMPLE={3,12,16,20,21,28,31,33,48,49,60,62,63,65,72,73,82,83,89,90,91,92,107,108,109,110,113,115,117,118,119,127,132,133,134,141,146,152,153,154,157,166,167,173,187,212,224,228,229,230,238,244,245,247,254,257}
SOL_SIMPLE={3,7,8,20,30,37,60,63,87,112,113,123,124,125,129,136,144,146,157,
 162,169,172,174,180,185,189,200,214,226,236,245,252,254,256,260,264,269,277,
 303,304,305,306,308,309,310,311,312,325,328,336,
 348,353,372,373,374,375,376,381,382,383,385,386,393,404,434,438,439,441,461,475,
 486,487,488,489,497,498,499,500,506,524,526,536,541,543,546,550,564,565,566,
 576,580,582,585,594,605,612,613,614,616,617,630,632,639,646,658,666,667,679,
 681,682,691,693,698,703,705,709,716,731,732,736,741,742,744,748,749,760,
 765,766,767,770,771,774,775,777,778,779,780,782,783,784,786,794,799,800,811,
 823,850,852,870,871,873,940,979,989,1032,1035,1047,1100,1135,1136,1167,
 1212,1247,1249,1255,1267,1272,1288,1309,1310,1317,1319,1330,1332}

# Clear grammatical or delimiter repairs within human editorial records are
# accepted in judgment only. Their existing human apparatus remains intact.
EDITORIAL_SIMPLE={
 'OPUS':{204,205,210},
 'SOL':{14,44,101,346,347,349,355,357,360,364,388,586,654,659,660,665,686,717,
 721,724,725,726,727,728,862,880,887,914,915,920,922,923,983,1006,1039,1041,
 1078,1080,1088,1089,1090,1101,1111,1127,1131,1133,1147,1159,1170,1189,1293}
}

# These are independently identified ambiguous scan/notation questions.
OPUS_REASONS={
 4:'The change from script K to plain K requires a verified identification of the presheaf and the underlined printed glyph.',
 6:'The intended scope of the subscript in phi_i(Y) requires checking the definition of the family phi_i.',
 18:'The proposed Si repairs a possible missing antecedent, but the full grammatical clause must establish that exact insertion.',
 19:'The record reports a typographical distinction between plain and underlined d; the symbol identity requires the surrounding cardinal convention.',
 22:'The glyph alpha versus membership is a scan-dependent reading; preserve the agreed source pending that comparison.',
 23:'The omitted paragraph number is not supplied by the sentence; 6 remains a conjectured target.',
 24:'The reported Greek glyph and the Latin f require the scan to identify the printed symbol precisely.',
 27:'Restoring lambda changes both the pullback and its codomain; the projection\'s exact source must be checked.',
 29:'The subscript A/a requires identifying the inclusion functor in all three formulas, not just regularizing its letter case.',
 45:'The reference is present but the proposed new displayed number needs identification of the intended equation.',
 61:'The prime distinguishes two ordered sets; the antecedent of this quantified set requires verification.',
 64:'Replacing objects by arrows changes the described action of g*; the definition of S must settle it.',
 66:'The proposed reference is plausible but must be compared with the stated definition and its label.',
 67:'The arrow label needs the definitions and endpoints of i and j in the gluing diagram.',
 68:'The record explicitly allows loss of faint strokes in the scan; no diagram completion is certified.',
 74:'Reversing both arrows requires the constructed map of relations and the adjunction; the snippet alone does not verify that construction.',
 76:'The product index may be a bound index or the indexing object; the formula defining Pi must settle the capital.',
 78:'The claimed replacement cross-reference requires comparison with both numbered adjunction formulas.',
 79:'Changing the ring subscript requires the module structures on both arguments of Hom.',
 80:'The missing first argument Y requires checking the internal-Hom adjunction used in the chain.',
 81:'The second internal-Hom argument must be traced through the chain before replacing M by N.',
 84:'The script/plain U distinction needs the local notational identification and the printed glyph.',
 85:'The arrow-style change requires establishing a misprint rather than a printed notation convention.',
 87:'Replacing two projective limits by inductive limits requires the homological construction of this complex.',
 88:'The source of both edge morphisms requires its Čech-cohomology definition and the degree conventions.',
 94:'This record bundles a tuple permutation and glyph repairs; each component needs a separate exact placement and definition check.',
 95:'Three independent proposed repairs are bundled; their index and morphism identifications require the full diagram.',
 96:'The identification of the handwritten script glyph with lambda is expressly a scan reading.',
 97:'The record bundles several handwritten-glyph readings and diagram changes; those readings cannot be certified without the scan.',
 99:'The presentation suggests indices 0 and 1, but the two diagram terms must be matched with its arrows before replacement.',
 106:'The proposed corrected field and quoted TeX put G on different operators; that ambiguity prevents an exact repair.',
 111:'The proposed star is described as presumptive; the notation for the three direct-image complexes must settle it.',
 112:'The equality/membership mark in the coproduct index requires checking the printed glyph and the indexing convention.',
 114:'The record combines a missing clause and two variable changes; the absent clause cannot be reconstructed from this snippet.',
 126:'The record offers two alternative index repairs and hence does not determine one exact corrected reading.',
 128:'The target topos must be matched with the preceding morphism before changing F double-prime to E double-prime.',
 129:'The change of family index requires tracking the corresponding transition maps.',
 136:'Parentheses around the slice index may group an indexed family; the supplied snippet does not uniquely establish a misprint.',
 138:'The labels require matching all endpoints with the definition of gamma; the record alone does not prove the diagram.',
 144:'Replacing an equals sign by a colon requires the local convention for defining a named arrow.',
 147:'The proposed renaming runs through an entire proof; every bound occurrence and antecedent must be tracked.',
 148:'The abutment requires checking the site and the sheaf in the spectral-sequence construction.',
 149:'The two field letters may encode an implicit identification; the record does not determine which occurrence to replace.',
 150:'Both the sheaf and its base change; the direct-image morphism and its source/target must be checked together.',
 151:'The sentence ends at de and supplies no unique missing reference or completion.',
 155:'The two replacements depend on the ambient sets of T_i and the surjectivity argument, which need explicit checking.',
 162:'The record offers 0 or O as the printed glyph; that printed reading cannot be fixed without the scan.',
 170:'The cohomology coefficient must be traced through the chosen Godement resolution.',
 174:'The connecting morphism must be checked against the named delta-functor before changing R to T.',
 176:'The proposed lower-case h requires the exact base-change square and functor types in both occurrences.',
 177:'Naming the ring A is plausible, but the record combines that insertion with an unclosed parenthesis without a unique complete repair.',
 180:'The record explicitly cannot distinguish an omitted mu from a faint lost stroke; retain the printed blank.',
 181:'The star count requires comparison with the two numbered conditions and their stated equivalence.',
 183:'The record explicitly describes the printed case as unclear; the scan must resolve it.',
 184:'The record explicitly allows a lost handwritten membership sign; the printed reading remains unverified.',
 185:'The supposed blank may be a lost handwritten membership sign; the printed reading remains unverified.',
 186:'The supposed missing membership sign needs a scan check before a diplomatic variant can be specified.',
 196:'The symmetric-group letter may be a font/handwriting issue; the scan must establish the exact printed glyph.',
 201:'The degree k must be checked against all symmetric powers in the paragraph before inserting two exponents.',
 207:'The proposed replacement requires tracking the object being reduced throughout the dévissage.',
 213:'The d/alpha reading concerns a handwritten symbol whose exact printed identity needs verification.',
 214:'The record explicitly calls the replacement probable; the structural morphism and pullback need an identification.',
 215:'The plus signs specify derived-functor domains; the source and target categories must be checked.',
 222:'The record combines several bar insertions; the compactified schemes and their maps must be tracked separately.',
 223:'The printed index only looks lowercase according to the record; the scan must resolve it.',
 225:'The case of the base subscript needs verification against the printed symbols and the base-scheme convention.',
 226:'Swapping whole proof paragraphs requires proving which case each argument establishes; no paraphrased replacement is accepted.',
 227:'The record proposes an isomorphism sign while reporting that TeX inserts equality; the exact relation is unresolved.',
 231:'Disjoint supports motivate a zero object, but the reported script O/zero reading still requires the exact printed glyph.',
 232:'The functor F and the object assignment script F must be identified throughout the coherence formula.',
 233:'The target cross-reference requires comparison with the additive-functor compatibility definitions.',
 236:'The truncation bound changes the complex; the degrees and the displayed comparison require independent verification.',
 237:'The index i/1 reading requires the chosen family of local equations and the printed symbol.',
 239:'The preimage map depends on the compactification; the two morphisms must be identified.',
 240:'The direct-image functor depends on the compactification and must be checked against the defined domain.',
 241:'The record proposes multiple bar insertions across the page, requiring a tracked occurrence list.',
 242:'The bundled bar and modulus-index insertions require a separate type check for every diagram entry.',
 243:'The omitted stars require checking which derived direct-image functors the sentence defines.',
 249:'The prime distinguishes maps in the argument; the exact surjectivity claim must identify the map.',
 250:'The record describes A_alpha as presumptive, so the omitted index is not determined.',
 251:'Replacing the cohomological star by 2 requires verifying the purity degree and the meaning of the displayed graded notation.',
 258:'The year requires an external bibliographic authority; the source record alone does not establish it.'
}

def clean(s):
    return re.sub(r'\s+',' ',s).strip()

def words(s):
    return re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)?",s,flags=re.UNICODE)

def textual_reason(x):
    """Retain the explicit grammatical observation checked in the record."""
    note=clean(x['note'])
    clauses=re.split(r'(?<=[.!?])\s+',note)
    basis=[]
    for c in clauses:
        if any(k in c.lower() for k in ('the tex','le tex','la tex','tex keeps','tex retains','tex silently','tex corrects','the edition','l’édition','l\'édition','\\sisi','scan','witness','témoin')):
            continue
        basis.append(c)
    observed=' '.join(basis)
    if not observed:
        observed=f'The local spelling or delimiter pair is {clean(x["scan"])} → {clean(x["corrected"])}.'
    return f'Textual check at {x["where"]}: {observed}'

def unresolved_reason(x):
    n=x['note'].lower(); target=clean(x['corrected'])
    if any(w in n for w in ('not clear','not fully clear','faint','lost','look','look-alike','peu net','scan','printed glyph','handwritten')):
        return f'The proposed reading {target} involves a printed glyph or a missing stroke at {x["where"]}; the textual record does not independently establish that glyph.'
    if any(w in n for w in ('reference','référence','renvoi','numbered','numéro')):
        return f'The proposed reference {target} at {x["where"]} needs comparison with the statement actually invoked; that target has not been independently established here.'
    if any(w in n for w in ('blank','incomplete','lacune','laissé','omitted clause','entire clause','missing reference')):
        return f'The record documents a lacuna at {x["where"]}; it does not uniquely establish the proposed completion {target}.'
    if any(w in n for w in ('arrow','flèche','morphism','morphisme','adjunction','adjonction','direction','contravariant')):
        return f'The replacement {target} at {x["where"]} requires a complete check of the maps, their endpoints and the composition convention; this identification is not independently verified.'
    if any(w in n for w in ('index','indice','prime','bar','tilde','hat','underline','case','capital','superscript','exponent','exposant')):
        return f'The replacement {target} at {x["where"]} identifies a particular indexed object or symbol; that identification is not independently established by the quoted local expression.'
    return f'The proposed reading {target} at {x["where"]} changes a substantive mathematical assertion or bibliographic identification; no independent derivation of this exact replacement is established in this review.'

def infer_segments(x):
    """Suggest exact lexical pairs; never apply them here."""
    a,b=x['scan'],x['corrected']
    out=[]
    if len(a)<200 and len(b)<200 and not any(k in a+b for k in ('...', '…','(twice)','same','with a','first ','sans ','no ')):
        out.append({'printed':a,'corrected':b,'method':'record-pair'})
    # A single corrected word can be aligned to a misspelling inside the scan.
    if re.fullmatch(r"[\wÀ-ÿ'’-]+",b):
        aw=words(a)
        candidates=[(difflib.SequenceMatcher(None,w.casefold(),b.casefold()).ratio(),w) for w in aw if w.casefold()!=b.casefold()]
        candidates.sort(reverse=True)
        if candidates and candidates[0][0]>=.48 and (len(candidates)==1 or candidates[0][0]>candidates[1][0]):
            out.insert(0,{'printed':candidates[0][1],'corrected':b,'method':'lexical-alignment'})
    return out

def main():
    judged=[]; edits=[]
    decisions_path=ROOT/'build_scripts'/'one_model_review.json'
    extra=json.loads(decisions_path.read_text()) if decisions_path.exists() else {}
    for model in ('OPUS','SOL'):
        records=json.loads((SRC/f'api_pass_20261111/{model}_ONLY_MISPRINTS.json').read_text())
        for n,x in enumerate(records,1):
            ident=f'OM-{model}-{n:04d}'
            cls=x['class']; verdict='possible-not-verified'
            specific=extra.get(ident)
            if (model,n) in REJECT:
                verdict='reject'; reason=REJECT[(model,n)]
            elif n in LANGUAGE_HOLDS.get(model,{}):
                reason=LANGUAGE_HOLDS[model][n]
            elif cls=='language':
                verdict='accept'
                reason=textual_reason(x)
            elif (model=='OPUS' and n in OPUS_SIMPLE) or (model=='SOL' and n in SOL_SIMPLE):
                verdict='accept'
                reason=textual_reason(x)
            elif cls=='recorded by the editors' and n in EDITORIAL_SIMPLE[model]:
                verdict='accept'
                reason=textual_reason(x)+' Preserve the human editorial entry unchanged.'
            elif cls=='recorded by the editors':
                reason=f'This finding intersects Orgogozo\'s \\sisi material at {x["where"]}; preserve that human entry unchanged. '+unresolved_reason(x)
            elif model=='OPUS':
                reason=OPUS_REASONS.get(n,f'The proposed reading {clean(x["corrected"])} at {x["where"]} needs the exact local definitions and printed symbol; no unique repair is certified by this record.')
            else:
                reason=unresolved_reason(x)
            if specific:
                verdict=specific['verdict']; reason=specific['reason']
            file=EXPOSE_FILES[x['expose']]
            held=(str(x['tome']),x['page']) in DP
            application='preserve-human-apparatus' if cls=='recorded by the editors' else ('hold-disputed-page' if held else ('accepted-candidate' if verdict=='accept' else 'not-applied'))
            row={'id':ident,'model':model,'page':f't{x["tome"]} {x["expose"]} p.{x["page"]}','reading':x['scan'],'verdict':verdict,'reason':reason,'corrected_reading':x['corrected'],'place':x['where'],'class':cls,'application':application}
            judged.append(row)
            if verdict=='accept' and cls!='recorded by the editors':
                edit={'id':ident,'model':model,'tome':str(x['tome']),'page':x['page'],'expose':x['expose'],'file':file,'printed':x['scan'],'corrected':x['corrected'],'tex':x['tex'],'place':x['where'],'reason':reason,'on_disputed_page':held,'application':application,'segments':specific.get('segments',infer_segments(x)) if specific else infer_segments(x),'source':f'api_pass_20261111/{model}_ONLY_MISPRINTS.json'}
                if specific:
                    for key in ('duplicate_group','evidence'):
                        if key in specific:edit[key]=specific[key]
                edits.append(edit)
    with (OUT/'ONE_MODEL_MISPRINTS_JUDGED.tsv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(judged[0]),delimiter='\t',lineterminator='\n');w.writeheader()
        # One physical TSV line per finding; TeX backslashes remain literal.
        for row in judged:
            w.writerow({k:clean(v) for k,v in row.items()})
    (OUT/'one_model_edits.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
    from collections import Counter
    print('Rows:',len(judged),'Verdicts:',dict(Counter(x['verdict'] for x in judged)))
    print('Accepted candidates:',len(edits),'undisputed:',sum(not x['on_disputed_page'] for x in edits))

if __name__=='__main__':main()
