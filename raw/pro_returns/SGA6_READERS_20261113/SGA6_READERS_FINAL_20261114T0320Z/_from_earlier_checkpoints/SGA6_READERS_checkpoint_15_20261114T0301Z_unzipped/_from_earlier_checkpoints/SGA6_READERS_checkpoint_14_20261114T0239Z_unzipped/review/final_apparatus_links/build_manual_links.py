#!/usr/bin/env python3
"""Record the individually inspected contextual links of the French apparatus.

The mapping is explicit, rather than inferred from a short punctuation or
wrapper substring. Each row seals the two exact alternatives and the selected
already adjudicated source records. No source decision is created here.
"""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from fr_source_links import load_decisions

# M:n denotes the exact one-based MISPRINTS_6 record, not a finding-list index.
MAPPING={
13:('M:4','The complete formula closes ch_Y before the equals sign; the reviewed closing parenthesis is rendered by the existing bigl/bigr pair.'),
18:('M:9','The correction is tranformant to transformant. The added linefeed is an ordinary TeX interword space at the same boundary; it adds no second textual correction.'),
25:('M:20','The final e of servie is removed, giving the source-adjudicated servi.'),
37:('M:27','The minimal insertion e is the feminine ending of adoptee in its exact surrounding accented word.'),
40:('M:31','The minimal insertion e is the feminine ending of tiree in its exact surrounding accented word.'),
51:('M:52','The accent in the second syllable of precedent changes from acute to grave, as adjudicated for the complete verb.'),
53:('M:54','The missing word de is inserted at the recorded location.'),
59:('M:60','The minimal insertion e completes the adjudicated feminine agreement signalee.'),
60:('M:61','The full formula removes the extra opening parenthesis immediately after Filt_j.'),
61:('M:62','This occurrence is equivalence rationelle, the later page15 spelling error. The earlier cohomologie rationelle belongs to record59 and FRV0058; its candidate alias is excluded here.'),
66:('M:43','The complete bibliographic word loses the printed French acute accent: Differential.'),
69:('M:34','The lambda formula receives its adjudicated closing parenthesis in (1.10).'),
84:('M:71','The complete E_G exterior-power expression receives the reviewed missing closing parenthesis.'),
91:('M:72','The index condition in equation (2.8) is i>1, replacing the printed i>=1.'),
96:('M:76','The exact L occurrence gains the missing category underline.'),
110:('M:87 ASTRA-EARLY-0016','This full math unit combines the two independently recorded changes: removal of the extra outer close and D to Y.'),
123:('M:102','The displayed summation lower index replaces phi by 1.'),
152:('M:125','First plain C on89; the added rule belongs to this C, not the adjacent site-S correction.'),
155:('M:126','The C following strictement pleine gains its reviewed missing rule; site-S records are excluded.'),
156:('M:127','The C following quasi-relevable gains its reviewed missing rule; site-S records are excluded.'),
158:('M:119','First of the two plain category-C occurrences on93 covered by the same explicitly located register record.'),
159:('M:119','Second of the two plain category-C occurrences on93 covered by the same explicitly located register record.'),
164:('M:129','The complete pseudocoherence parenthesis carries the source-adjudicated n-pseudocoherent/resp. pseudocoherent text; later word rules preserve that text.'),
168:('ASTRA-I-RADICAL-109','The complete underlined span removes the recorded nilpotence-only disjunct. The independent source proof is in the selected decision.'),
180:('M:145','The first missing closing parenthesis after Tr(D(C)) is record145; the later separate occurrence is record146.'),
182:('M:147','This C_0 receives its missing category rule.'),
183:('M:148','The quotient separator is the recorded slash in the complete math unit.'),
189:('M:137 ASTRA-I-INDEX-142','The exact object-membership formula changes X in ob C_X to X in ob S. The source record and independent index decision jointly identify this expression.'),
198:('M:159','The missing semicolon is inserted at the exact source punctuation boundary.'),
201:('M:162','The source sentence receives its missing final full stop after O_S.'),
226:('ASTRA-II-PAREN-189','First extra closing parenthesis after a deduite de reference is removed.'),
227:('ASTRA-II-PAREN-189','Second extra closing parenthesis after a deduite de reference is removed.'),
252:('M:202','The structure-sheaf O_Y receives the missing single rule.'),
271:('check/findings/findings_256_260.json#20','This locator is in the proof phrase appliquer(4.8) avec Y=S,F=O_S. The separate Corollary4.9.1 occurrence belongs to finding14 and FRV0270; it is excluded here.'),
276:('M:226','The source abbreviation rep. becomes resp.; the enclosing word-rule command preserves both alternatives literally.'),
280:('M:229','The extra closing parenthesis in Z-prime^p(E)) is removed.'),
287:('M:238','The complete EGAIII6 and IV3.1.0 references receive their adjudicated parenthesis placement.'),
294:('M:244','The reference receives the missing parenthesis at the inspected source location.'),
300:('M:248','The missing resp. parenthesis is closed after K^bullet(Y), as located in the body context.'),
313:('M:258 M:259','The complete formula contains two distinct missing-parenthesis repairs; both register sources are retained.'),
368:('M:322 M:323 M:324','The full aligned display combines the printed stop/comma, two/three dots and duplicated low product-dot repairs.'),
370:('M:325','The duplicated low placeholder dot is removed; mathord{.} transports the retained typed baseline dot.'),
374:('M:297','The complete Gr expression gains the recorded completion hat.'),
380:('M:302','Equation6.5.2 changes its two typed dots to the reviewed three-dot ellipsis.'),
381:('M:303','Equation6.5.3 changes its two typed dots to the reviewed three-dot ellipsis.'),
383:('M:304 ASTRA-V-CH-CONSTANTS-350','This complete display combines the final two-dot repair and the three independently proved removals of 1+ from the Chern-character expressions.'),
386:('ASTRA-V-TWO-DOT-351','The exactly located two-dot source ellipsis is corrected to three dots.'),
396:('M:337','The complete Ch(Gr wedge) expression loses its extra outer close.'),
403:('M:344','The diagram target Ch(Gr wedge) loses the recorded extra close.'),
408:('M:346 M:347','The full derivative expression removes its extra denominator close and changes dt to the independently recorded du.'),
424:('M:317','The missing est is inserted in the source sentence.'),
425:('ASTRA-VI-SYZYGY-372','Z_(r+1) changes to Z_r by the exact resolution argument in the source decision. Braces group the same changed index.'),
426:('ASTRA-VI-ALGEBRA-RULE-372','The entire first B to underlined B correction after est isomorphe comme belongs to this algebra-rule decision, including both wrapper braces. The page-wide GLYPHS decision explicitly preserves this exception plain and is excluded as a source for its closing brace.'),
439:('ASTRA-VI-ADJOINT-TARGET-382','The target M changes to tilde M; the common category rules are separately preserved by the382 glyph decision.'),
448:('ASTRA-VI-PROJECTIVE-P-385 ASTRA-VI-PROJECTIVE-ARG-RULE-385','The complete X=Proj expression combines the projective-P double-rule/bold transport and the missing E rule, each explicitly sourced.'),
449:('M:355','The printed baseline L dot becomes a superscript bullet; both alternatives retain the common L rule.'),
450:('ASTRA-VI-DERIVED-R-386','Both total-derived R occurrences transport their two printed rules to mathbb. The exact functor identification is recorded in the source decision.'),
459:('M:359','The comma missing after E_i is inserted.'),
469:('ASTRA-VI-GL-OPERATORS-393','The two Gl operators in this math unit transport the printed double rule to bold, with the same functor of automorphisms.'),
470:('ASTRA-VI-GL-OPERATORS-393','The two Gl operators in this second math unit use the same separately proved double-rule/bold transport.'),
484:('ASTRA-VI-FLAG-LAST-INDEX-397','The final flag index changes F_m to F_n; the common underlines remain unchanged.'),
485:('ASTRA-VI-FLAG-NOTATION-REFERENCE-397','This digit is in notation de3.5 to4.5, identifying the canonical quotients and kernels. The separate basis/corollary3.4 to4.4 decision belongs to FRV0495 and is explicitly excluded here.'),
521:('M:369','The source punctuation isomorphisme.: loses the extra full stop.'),
536:('M:382','The verb permet becomes permettent by the explicitly recorded agreement correction.'),
539:('M:384','The printed circumflex in c-est is removed.'),
550:('M:396','The missing par is inserted at the recorded source boundary.'),
596:('ASTRA-VII-0084','The missing localement is inserted before libres.'),
673:('ASTRA-VIII-0064','All projective-P operators within this full math unit transport their printed double rule to bold.'),
674:('ASTRA-VIII-0064','All projective-P operators within this next full math unit use the same independently recorded transport.'),
698:('ASTRA-IX-NONZERO-LOCALIZATION-503','The missing non nuls qualification is the source-adjudicated localization correction.'),
724:('M:541','The dimension expression receives its missing close after f-inverse(Supp F).'),
736:('M:526','The exact underlined N is replaced by the recorded lower-case n.'),
740:('M:517','The O subscript is placed on the correct Mod symbol, as the complete source expression requires.'),
742:('M:519','The extra closing parenthesis in Gl(n)) is removed.'),
745:('ASTRA-X-0093','The complete first-pivot correction c=c_(h,1,lambda) to c=c_(2,h,lambda) belongs to ASTRA-X-0093, including deletion of the old ,1. Checker556_560#17 concerns a later clearing clause and is excluded from this full variant.'),
768:('ASTRA-X-REF-580-POSTFREEZE M:501','This combined minimal pair15) to14 contains the7.15 to7.14 locator correction and deletion of an extra closing parenthesis. The reference amendment explicitly leaves the parenthesis to its separate record501; both sources are required.'),
773:('M:493','This bar belongs to the localization B_i=A_{i,m_i}, identified by a to a/1 in the localization of bar A_i. The following k_i residue-field formula is record494/FIXLOG507 and is excluded from this occurrence.'),
779:('M:531','The printed reference receives its missing close.'),
781:('ASTRA-X-0124 M:533','This complete span combines de type fini to noetherien and the independent missing-parenthesis correction.'),
786:('M:573','This occurrence is sur S_i to S_2; record571 concerns the separate X_i expression.'),
825:('M:585','The module base changes O_Y to O_X.'),
859:('ASTRA-XIII-0030','The current span inserts the full reference sous les hypotheses de3.8. The source decision includes the printed-context proof and explicit P1-to-point counterexample; later word rules only surround the same insertion.'),
872:('M:614','The complete formula removes the printed duplicate et a_q^(q); the later rule around et carries the same retained word.'),
876:('M:626','The missing I is inserted. The global word-rule decision supplies only the wrapper and is excluded as the source of this content change.'),
877:('M:627','The missing feminine e completes engendree in the exact source sentence.'),
882:('M:632','The module base changes O_Y to O_X at this independently located occurrence.'),
889:('M:673 ASTRA-XIII-0067','The complete reference removes the genuinely printed duplicated journal/year/pages text and corrects the independent terminal103 to104.'),
920:('M:651','The duplicated full stop in Cf.. is removed.'),
940:('M:698 M:699','The full expression corrects both independently recorded Q-ell indices.'),
957:('M:664','The bibliographic abbreviation MAt. becomes Mat.; neighbouring record665 concerns Sborik and is excluded.'),
}

def main():
    data=json.loads((ROOT/'records/FR_SOURCE_LINK_CANDIDATES.json').read_text())
    variants={r['variant_id']:r for r in data['variants']}
    _,_,decisions=load_decisions()
    rows=[]
    for n,(sources,reason) in sorted(MAPPING.items()):
        vid=f'FRV{n:04d}';v=variants[vid]
        ids=[('fixes/MISPRINTS_6.json#'+s[2:]) if s.startswith('M:') else s for s in sources.split()]
        for sid in ids:
            d=decisions[sid]
            assert str(d['page'])==str(v['page']),(vid,sid,d['page'],v['page'])
            assert d.get('image') and d.get('reason') and not d['verdict'].startswith(('pending','reverted')),(vid,sid)
        rows.append(dict(variant_id=vid,page=v['page'],printed=v['printed'],corrected=v['corrected'],
             sha256_printed=hashlib.sha256(v['printed'].encode()).hexdigest(),sha256_corrected=hashlib.sha256(v['corrected'].encode()).hexdigest(),
             source_ids=ids,method='Individually inspected full-variant/source-record correspondence; supersedes short-substring candidate aliases.',reason=reason))
    uncovered={v['variant_id'] for v in variants.values() if v['uncovered_edits']}
    assert uncovered <= {r['variant_id'] for r in rows},uncovered-{r['variant_id'] for r in rows}
    (ROOT/'review/final_apparatus_links/manual_links.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    print(json.dumps({'manual_variants':len(rows),'uncovered_candidates_addressed':len(uncovered)}))

if __name__=='__main__':main()
