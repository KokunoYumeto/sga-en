"""One-shot direct collation records for the final two Exposé 0 folios."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_text())
def save(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
e={
1:['conclusion, p−1>dim.Y','The abbreviation dim is followed by a visible full stop. Both attached layers already retain it.'],
2:['conclusion, dimension inequality','The two occurrences dim.Y and dim.X each have a full stop immediately after dim. Both attached layers match.'],
3:['conclusion, projective-space dimension','The abbreviation in r>dim.X+1 has a full stop. Both attached layers match.'],
4:['N.B. label','The label is ordinary typed text without an underline. Both attached layers now preserve the plain label.'],
5:['N.B., comme dans R.R.R.2.16','Each R is followed by its own full stop. Both attached layers use the explicit abbreviation with all three stops.'],
6:['N.B., final R.R.R.','The third full stop of the abbreviation also ends the sentence; no additional stop follows. Both attached layers match.'],
7:['sentence immediately before formula(13)','This F lacks a check, although the preceding invocation of R.R. and formula(13) both have check F. The class used in the corollary is y·lambda_{−1}(check F); substituting its R.R. identity into the displayed calculation requires that same class. Restore the omitted check in current and retain plain F diplomatically.'],
8:['letter excerpt, final line','The typescript reads une variété obtenu. Variété is feminine and the participle modifies it; current must read obtenue. Preserve obtenu diplomatically.']}
save('evidence_076_080.json',{'findings_076_080.json':e})
patches=load('extra_patches.json')
def patch(p,layer,old,new,sid,reason,kind='misprint_correction',count=1):patches.append(dict(page=p,layer=layer,old=old,new=new,source_id=sid,reason=reason,kind=kind,expected_count=count))
patch(76,'current',r"\((Y',X',y\lambda_{-1}(F))\)",r"\((Y',X',y\lambda_{-1}(\check F))\)",'fixes/MISPRINTS_6.json#116',e[7][1])
patch(76,'current','une variété obtenu','une variété obtenue','fixes/MISPRINTS_6.json#117',e[8][1])
reason='The parenthetical copyist insertion after filtration≥p−1 has a raised opening star before dans and a lowered closing star after supports. The main scan displays both positions clearly, consistently with the explanatory copyist note on p71. Preserve the two observed heights in this exact occurrence.'
patch(76,'both',r'{*}dans \(K(Y)\) filtré par la codimension des supports{*}',r'\textsuperscript{*}dans \(K(Y)\) filtré par la codimension des supports\textsubscript{*}','ASTRA-EARLY-TYPE-019',reason,'interpolation_mark')
save('extra_patches.json',patches)
records=load('extra_decisions.json')
records.append(dict(record_type='typography_observation',page=76,source_id='ASTRA-EARLY-TYPE-019',verdict='not applied and now applied',printed_reading='raised opening star before dans; lowered closing star after supports',image='scan/SGA6_scan_360dpi.pdf#page=90',region='concluding paragraph, parenthetical copyist insertion',reason=reason,change={'old':r'{*}dans \(K(Y)\) filtré par la codimension des supports{*}','new':r'\textsuperscript{*}dans \(K(Y)\) filtré par la codimension des supports\textsubscript{*}'},forms='French diplomatic and corrected; English where notation is affected'))
save('extra_decisions.json',records)
pages=load('extra_pages.json')
pages.append(dict(page=76,pdf_page=90,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=False,findings_count=8,begins='De la formule(7)',notes='All prose, formulas(11)–(13), copyist stars, N.B., letter heading and opening lines directly compared. The page ends sous-variété non; the next folio starts singulière.'))
pages.append(dict(page=77,pdf_page=91,fully_checked=True,main_scan_viewed='four overlapping horizontal strips',witness_viewed=False,findings_count=0,begins='singulière. Dans ce deuxième cas',notes='Complete final letter excerpt directly compared, including formulas(9),(9bis), both underlined égalité spans, the two ellipses and p.c.c.J-P.S. All remaining page area was viewed and contains no further text. No new discrepancy was observed.'))
save('extra_pages.json',pages)
