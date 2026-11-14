"""One-shot direct collation record for pp.71–75, including copyist marks."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['bibliography heading','A colon follows the underlined heading. Both attached layers include the colon; the subsection style is accepted.'],
2:['bibliographic reference[1]','The print clearly has topologischen. The adjective before plural Methoden without an article takes the ending-e, as Neue does. Correct to Neue topologische Methoden in current while retaining the printed title spelling diplomatically.'],
3:['Rappel de notations heading and unmarked footnote','A normal-height star precedes the heading, with no call after notations. The note text at the foot starts directly with Les passages, without a label. The leading star opens the copyist interpolation closed on p73. Keep that star, remove the invented automatic heading call, and set the note with the explicit unmarked label.'],
4:['copyist note, astériques','The printed word lacks s after i: astériques. Correct it to astérisques in current. The two illustrative stars have separate raised and lowered positions, recorded under finding21.'],
5:['opening bracketed explanation, R.R.R.','All three full stops are visible in R.R.R. Both attached layers now use the literal abbreviation with stops.'],
6:['boundary pp71/72','Page71 ends sous- and p72 begins variété. The attached sous-% preserves the original compound hyphen and prevents an inserted space across the marker.'],
7:['classes de cylces','The letters are cylces, with l before c. Correct to cycles in current.'],
8:['rationnelle -cf. Chow','A short hyphen immediately precedes cf., with a space before the hyphen. Both attached layers now preserve the literal punctuation.'],
9:['Si E est un fibré paragraph','An indented paragraph begins after the preceding sentence ending codimension i. Both attached paragraph breaks match.'],
10:['fibré à fibre vectoriel','The print says vectoriel with no final-le. The adjective modifies feminine fibre; current must read vectorielle, as the later occurrence on the same page does.'],
11:['Lorsque y est le fibré tangent paragraph','A new indented paragraph follows Ce sont des éléments de A(X)⊗Q. Both attached layers match.'],
12:['Le premier est homogène paragraph','This paragraph is indented after the f-star map display. Both attached paragraph breaks match.'],
13:['dim.X−dim.Y','Both abbreviations have an explicit full stop. The attached dim.X and dim.Y match.'],
14:['On définit également paragraph','A new indented paragraph follows the degree statement. Both attached layers match.'],
15:['Si F est un faisceau paragraph','An indented paragraph follows the upper/lower-shriek map display. Both attached paragraph breaks match.'],
16:['boundary pp72/73','Page72 ends l’opération d’image réciproque. Page73 begins Si G est un faisceau cohérent. Both attached markers now precede Si G.'],
17:['theorem label','The entire label is typed in capitals. Both attached labels now retain capitals, with the accepted accented-capital and joint-name typography.'],
18:['formula(1), dans','The word dans is visibly underlined. Both attached layers include emphasis on this word.'],
19:['Lemma1 label','The label is typed LEMME1 in capitals. Both attached layers match.'],
20:['de R.R.R. On va','The abbreviation has three full stops; the last also closes the sentence. Both attached layers now preserve it literally.'],
21:['copyist interpolation marks on pp71,73,75','P71 heading has a normal-height opening star. Its footnote illustrates a raised opening star and lowered closing star. P73 has a lowered closing star after the definition of f_!, then three parenthesized interpolations (application régulière, abrégée, En fait...) each with a raised opener and lowered closer. P75 Dans la formule(7) has a normal-height opener and lowered closer before the bracket. Preserve these observed heights explicitly; all listed locations were directly viewed.'],
22:['Lemma2 label','The label is typed LEMME2 in capitals. Both attached layers match.'],
23:['formula(4), avec','The word avec is underlined. Both attached layers preserve its emphasis.'],
24:['Corollary label','COROLLAIRE is typed in capitals. Both attached labels match.'],
25:['Lemma3 label','LEMME3 is typed in capitals. Both attached labels match.'],
26:['Lemma3, u arrow','The arrow is plain and has no vertical tail bar. Both attached longrightarrow commands preserve the printed arrow type.'],
27:['between(u,v_0) and v_0∈P','No comma stands between these two expressions. Both attached layers omit the formerly added comma. The index-zero/o shape follows NOTE_6.'],
28:['blow-up diagram, lower arrow','The j label is above the bottom arrow; g is left of the left upward arrow and f is right of the right upward arrow. All attached positions now match.'],
29:['Lemma4 label','LEMME4 is typed in capitals. Both attached labels match.'],
30:['formula(8), d’où','The word is underlined. Both attached layers preserve the emphasis.'],
31:['formula(9), pour tout','These two words are underlined. Both attached layers preserve their emphasis.'],
32:['Pour simplifier l’écriture paragraph','The bracketed paragraph begins indented after the displayed formulas. Both attached paragraph breaks match.'],
33:['La formule(7) paragraph','A new indented paragraph follows(6bis). Both attached layers preserve it.'],
34:['KÜnneth on pp70 and75','The U-umlaut form is visibly taller than the adjacent lowercase n, with the same tall form on p70. Native witnesses81 and86 confirm the matching letter forms. Preserve KÜnneth in the diplomatic text on both pages and Künneth in current; no assumption about the typewriter keyboard is required. P75 already has these two readings; p70 receives the parallel diplomatic patch.'],
35:['En fait,(9) bracketed paragraph','This final bracketed comment begins on a new indented line after xi=C^1(L). Both attached paragraph breaks match.']}
save('evidence_071_075.json',{'findings_071_075.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(71,'current','Neue topologischen Methoden','Neue topologische Methoden','fixes/MISPRINTS_6.json#111',e[2][1])
patch(71,'current','astériques','astérisques','fixes/MISPRINTS_6.json#112',e[4][1])
patch(72,'current','cylces','cycles','fixes/MISPRINTS_6.json#113',e[7][1])
patch(72,'current','fibre vectoriel,','fibre vectorielle,','fixes/MISPRINTS_6.json#114',e[10][1])
patch(71,'both',r'\subsection*{* Rappel de notations\footnotemark}',r'\subsection*{* Rappel de notations}','check/findings/findings_071_075.json#3',e[3][1],'author_note_label')
patch(71,'both',r'\footnotetext{Les passages',r'\SGAAuthorFootText{unmarked}{Les passages','ASTRA-EARLY-NOTE-071-1',e[3][1],'author_note_label')
patch(71,'both',r'*\dots*',r'\textsuperscript{*}\dots\textsubscript{*}','check/findings/findings_071_075.json#21',e[21][1],'interpolation_mark')
patch(73,'both',r'\quad*',r'\quad\textsubscript{*}','check/findings/findings_071_075.json#21',e[21][1],'interpolation_mark')
patch(73,'both','(* ',r'(\textsuperscript{*} ','check/findings/findings_071_075.json#21',e[21][1],'interpolation_mark',3)
patch(73,'both',' *)',r' \textsubscript{*})','check/findings/findings_071_075.json#21',e[21][1],'interpolation_mark',3)
patch(75,'both','.{*}]',r'.\textsubscript{*}]','check/findings/findings_071_075.json#21',e[21][1],'interpolation_mark')
patch(75,'both',r'\footnotemark',r'\text{\SGAAuthorFootMark{*}}','ASTRA-EARLY-NOTE-075-1','The call after mod.(1−L) in formula(7) is a baseline parenthesized star, followed by a full stop. Preserve that explicit call in the display.','author_note_label')
patch(75,'both',r'\footnotetext{Cette formule',r'\SGAAuthorFootText{*}{Cette formule','ASTRA-EARLY-NOTE-075-2','The author-note label at the foot is the same baseline parenthesized star as the call after(7). Preserve its explicit mark.','author_note_label')
patch(70,'diplomatic','Künneth','KÜnneth','ASTRA-EARLY-TYPE-016',e[34][1],'printed_case')
patch(72,'both',r'\mathcal O',r'\underline{O}','ASTRA-EARLY-TYPE-017','The opening O_Y and both O letters in the Tor expression are underlined typed letters. Preserve the three observed forms explicitly.','font',3)
patch(75,'both',r'\mathcal O',r'\underline{O}','ASTRA-EARLY-TYPE-018','The base-ring O_X(v) and both O letters in the arguments of Tor in(6bis) are visibly underlined. Preserve all three forms explicitly.','font',3)
proof='The print names the derived functors R^pf_* immediately after the operation G↦f_*(G), but then calls the underlying functor f. The explicitly defined sheaf functor is f_*:Coh(Y)→Coh(X), G↦f_*(G); its p-th right derived functor is R^pf_*. Supply the omitted lower star in this one functor name, preserving the morphism f and the distinct K-group map f_! elsewhere.'
patch(73,'current',r'du foncteur \(f\) ainsi défini',r'du foncteur \(f_*\) ainsi défini','ASTRA-EARLY-0022',proof)
save('extra_patches.json',patches)
records=load('extra_decisions.json')
def rec(typ,p,sid,pr,region,reason,change,verdict='confirmed',**kw):records.append(dict(record_type=typ,page=p,source_id=sid,verdict=verdict,printed_reading=pr,image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',region=region,reason=reason,change=change,forms='French diplomatic and corrected; English where meaning or notation is affected',**kw))
rec('own_finding',73,'ASTRA-EARLY-0022','du foncteur f ainsi défini','first paragraph',proof,{'old':r'du foncteur \(f\) ainsi défini','new':r'du foncteur \(f_*\) ainsi défini'},'not applied and now applied')
rec('typography_observation',70,'ASTRA-EARLY-TYPE-016','KÜnneth','first sentence',e[34][1],{'diplomatic':'KÜnneth','current':'Künneth'},'not applied and now applied',witness_image='scan/SGA6_witness_300dpi.djvu#page=81',related_pages=[70,75])
rec('typography_observation',72,'ASTRA-EARLY-TYPE-017','three underlined O letters','first paragraph and Tor expression','The three structure-sheaf letters have explicit underlines. Replace the mathcal O forms on this inspected page only.',{'old':r'\mathcal O','new':r'\underline{O}','count':3},'not applied and now applied')
rec('typography_observation',75,'ASTRA-EARLY-TYPE-018','three underlined O letters','formula(6bis)','The three structure-sheaf letters, including the base-ring superscript, have explicit underlines. Replace those mathcal O forms only.',{'old':r'\mathcal O','new':r'\underline{O}','count':3},'not applied and now applied')
rec('typography_observation',71,'ASTRA-EARLY-NOTE-071-1','unmarked copyist note','foot of page',e[3][1], 'Remove the spurious heading footnote call and use SGAAuthorFootText{unmarked}.','not applied and now applied')
rec('typography_observation',75,'ASTRA-EARLY-NOTE-075-1','(*)','call at end of formula(7)','A central star enclosed in baseline parentheses stands after mod.(1−L), before the full stop.','Use SGAAuthorFootMark{*} at the displayed location.','not applied and now applied')
rec('typography_observation',75,'ASTRA-EARLY-NOTE-075-2','(*)','author-note label','The footnote label has the same central star within baseline parentheses. The complete note, citing VII4.1, was directly compared.','Use SGAAuthorFootText{*}.','not applied and now applied')
save('extra_decisions.json',records)
overrides=load('record_overrides.json')
overrides['check/findings/findings_071_075.json#3']={'verdict':'amended','change':'Keep the normal-height opening interpolation star; remove the invented footnotemark after the heading and render the note without a label.','reason':e[3][1]}
overrides['check/findings/findings_071_075.json#21']={'related_pages':[71,73,75],'change':'Explicit superscript/subscript star forms in all directly inspected interpolation locations; the two normal-height openers are retained.'}
overrides['check/findings/findings_071_075.json#34']={'related_pages':[70,75],'change':'Diplomatic KÜnneth on both inspected pages; corrected Künneth. P75 already differs; p70 receives an occurrence-specific diplomatic patch.'}
save('record_overrides.json',overrides)
pages=load('extra_pages.json');f=json.loads((R/'check/findings/findings_071_075.json').read_text())
for row in pages:
 if row['page']==70:row['witness_viewed']=True;row['notes']+=' Native witness81 first-line crop subsequently inspected for the tall U-umlaut form.'
beg={71:'Références bibliographiques',72:'variété Y de X',73:'Si G est un faisceau',74:'LEMME2',75:'LEMME4'}
for p in range(71,76):pages.append(dict(page=p,pdf_page=p+14,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=p==75,findings_count=sum(z['page']==p for z in f),begins=beg[p],notes='All prose, displays, p74 diagram, author/copyist notes and interpolation marks directly compared. Native witness86 was used for the tall U-umlaut form on p75. HOLD35 is nominally packet75 but actually ExposéI1.1.5 and has been referred to the ExposéI reviewer.'))
save('extra_pages.json',pages)
