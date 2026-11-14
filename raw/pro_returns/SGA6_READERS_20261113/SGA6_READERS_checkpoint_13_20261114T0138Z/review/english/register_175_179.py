#!/usr/bin/env python3
"""Register soft-sheaf and Stein passages with their explicit original notes."""
from pathlib import Path
import hashlib,json,re
from reviewed_french import load_reviewed_pages
from verify_reviewed_english import split

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
chunk=(HERE/'EN_EXPOSE_II_P175_179.tex').read_text()
native=(HERE/'SGA6_EN_native_flattened_UNVERIFIED.tex').read_text()
prop=native.index(r'\sgaStableTarget{sga6.e02.prop.2-2-9}')
a=native.index('are fully faithful and have as essential image',prop)
lemma=native.index(r'\sgaStableTarget{sga6.e02.lem.2-4-3}',a)
b=native.index(r'\item Put $A=',lemma)
record=dict(id='EN-EXPOSE-II-175-179',page='175–179',
 place='Proposition2.2.9 continuation through Lemma2.4.3(b)',
 layer='both',old=native[a:b],new=chunk,
 status='accepted passage comparison; exact scanned French decisions supplied by early reviewer',
 source='build/page_packets/175–179/current.tex and diplomatic.tex; review/expose_ii/patches.jsonl',
 reason='Restores bounded D-b rather than inherited D-minus, the original D-plus domain/codomain of derived sections, each observed R letter and diagram label, original C-r regularity, complete soft-sheaf proof, the explicit post-checkpoint locator variant1.2.1/1.2, both theorem A/B word-rule scopes, all original examples and citations, source underlined ideal sheaf versus plain stalk maximal ideal, exact Nakayama comparison and all author calls/texts. The two source questions remain historical questions without a replacement assertion.')
note_start=native.index('Here ',b)
note_end=native.index('\n\n',note_start)+2
relocated=native[note_start:note_end]
assert 'enough closed points' in relocated and r'i^*:S\to s' in relocated
note_record=dict(id='EN-EXPOSE-II-NOTES179',page=179,
 place='Original179 author notes; inherited duplicate body paragraph after the180 lemma',
 layer='both',old=relocated,new='',
 status='accepted exact duplicate removal after restoring the original author-note layer',
 source='ASTRA-II-NOTE-179; reviewed original179 with its explicit calls1 and2',
 reason='The native English moved the two original179 notes into one later body paragraph and changed their displayed point map and ideal notation. Both complete notes are now translated at their directly observed calls with exact source math in EN-EXPOSE-II-175-179. Remove only that obsolete relocated paragraph, avoiding duplicated author content. This isolated cleanup does not claim that the surrounding180 body has been reviewed.')
path=HERE/'EN_TRANSLATION_PATCHES.jsonl';records=[json.loads(x) for x in path.read_text().splitlines()]
for rec in [record,note_record]:
 hits=[i for i,x in enumerate(records) if x['id']==rec['id']]
 if hits:records[hits[0]]=rec
 else:records.append(rec)
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))

variants=[]
def add(number,page,old,printed,source,reason,mode='text',region=''):
 variants.append(dict(id=f'EN-VAR-{number:03}',page=page,old=old,printed=printed,corrected=old,mode=mode,
  source=source,reason=reason,scope_start=f'%%%%%%%%%%  scan idx {page+13}  |  folio {page}',
  scope_end=f'%%%%%%%%%%  scan idx {page+14}  |  folio {page+1}' if page<179 else None,
  scan_image=f'scan/SGA6_scan_360dpi.pdf#page={page+14}; scan/SGA6_witness_300dpi.djvu#page={page+11}',
  scan_region=region))
add(122,175,r'F^i\in\Ob \underline{L}(S)',r'F^i\in\Ob \underline{L}(S))',
 'check/findings/findings_171_175.json#14; fixes/MISPRINTS_6.json#155',
 'The category expression L(S) has one opening parenthesis and is already closed. Current removes the unmatched second close after this expression; diplomatic retains it. The same component F^i and category membership remain.',
 mode='math',region='Proposition2.2.9(b), component membership')
add(123,177,'(I 4.8)','(4.8)',
 'check/findings/findings_176_180.json#8; fixes/MISPRINTS_6.json#165',
 'ExposéI Example4.8 on122 describes the perfect amplitude for this derived category of Modules using local direct factors of finite free Modules. The parallel statement II2.2.9 on175 explicitly cites I4.8. Current supplies the omitted exposé identifier; diplomatic retains4.8.',
 region='Proposition2.3.2(c), perfect-amplitude reference')
add(124,177,'(I 4.9)','(4.9)',
 'check/findings/findings_176_180.json#9; fixes/MISPRINTS_6.json#166',
 'ExposéI Notation4.9 on122 names D(S)_parf for the full subcategory of perfect objects used here. The parallel statement on175 has the explicit I4.9 locator. Current supplies the omitted exposé identifier without changing the indicated subcategory.',
 region='Proposition2.3.2(c), perfect-subcategory reference')
add(125,178,'free Modules (resp. direct factors of free Modules) of finite type',
 'free Modules (resp.) direct factors of free Modules) of finite type',
 'check/findings/findings_176_180.json#12; fixes/MISPRINTS_6.json#168',
 'The printed alternative closes immediately after resp. and again after the phrase giving the alternative. Current removes only the premature first close. The functor Gamma_S and both specified kinds of Modules remain unchanged.',
 region='Final proof sentence concerning Gamma_S')
add(126,178,'Assertion c) follows from (1.2 b),c),d))',
 'Assertion c) follows from (1.2.1 b),c),d))',
 'ASTRA-II-REF-178-POST05; review/expose_ii_amendments/reference_178_identification.json',
 'Both scans print the extra .1. The actual Proposition1.2(b,c,d) on161–163 supplies the bounded representative, canonical fully faithful functor and actual quasi-isomorphism used here. The printed C_0=Lib wording is retained. The recorded specialization first takes P=Loclib and identifies C_(1S) with P by the identity on modules and maps. For a degree-i term choose a finite-free complement Q and add the contractible disk Q→Q in degrees i−1,i. Its projection pi and inclusion j satisfy pi j=id and dh+hd=id−j pi, with h^i=id_Q. Descending through i=n,...,m+1 gives the stated free higher terms, and the composite F→G→E is the required quasi-isomorphism. This exact construction supports the locator repair without silently identifying the two printed categories.',
 region='Proof of2.3.2(c), citation of the globalization proposition')
path=HERE/'EN_VARIANTS.jsonl';rows=[json.loads(x) for x in path.read_text().splitlines()]
ids={v['id'] for v in variants};rows=[x for x in rows if x['id'] not in ids]+variants
rows.sort(key=lambda x:int(x['id'].rsplit('-',1)[1]))
path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

current,ref=load_reviewed_pages(179)
diplomatic,dref=load_reviewed_pages(179,'diplomatic')
ledger=[]
patch_sources=['review/expose_ii/patches.jsonl','review/expose_ii_amendments/patches.jsonl']
for raw in '\n'.join((ROOT/p).read_text() for p in patch_sources).splitlines():
 if not raw.strip():continue
 p=json.loads(raw)
 if not 175<=p['page']<=179:continue
 ledger.append(dict(page=p['page'],source_id=p['source_id'],layer=p['layer'],
  decision='transferred in faithful English; source punctuation/reference variants are explicitly branched',
  patch_record_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_reason=p['reason'],
  expected_source_count=p.get('expected_count',1)))
for layer,reading,french,reference in [('current','corrected',current,ref),('diplomatic','printed',diplomatic,dref)]:
 text=chunk
 for v in variants:
  a=text.index(v['scope_start']);b=text.index(v['scope_end'],a) if v.get('scope_end') else len(text)
  section=text[a:b];assert section.count(v['old'])==1,(v['id'],section.count(v['old']))
  text=text[:a]+section.replace(v['old'],v[reading],1)+text[b:]
 en=split(text)
 for page in range(175,180):
  counts={}
  for token in [r'\underline{C}',r'\underline{S}',r'\underline{O}',r'\underline{L}',
                r'\underline{m}',r'\underline{\underline{R}}',r'\mathbb R',
                r'\underline{\operatorname{Loclib}}',r'\varnothing',
                r'\SGAAuthorFootnote{1}',r'\SGAAuthorFootnote{2}',r'\SGAAuthorFootMark{1}']:
   counts[token]=dict(French=french[page].count(token),English=en[page].count(token))
   assert counts[token]['French']==counts[token]['English'],(layer,page,token,counts[token])
  ledger.append(dict(page=page,layer=layer,source_id='exact reviewed page glyph inventory',
   decision='literal command multiplicities agree in both materialized branches',
   source=reference['bases'][page-1],counts=counts))
ledger.extend([
 dict(page=175,source_id='ASTRA-II-NOTE-175',decision='Restore one numerical1 author note and its repeated proof call; the second call does not duplicate the note text.'),
 dict(page=175,source_id='reviewed Proposition2.2.9 and Remark2.2.10',decision='The first essential image and proof use D-b, the derived section functor has source D-plus(S) and target D-plus(A), and its displayed R has two lower rules. Restore those exact source qualifications instead of inherited unbounded or D-minus alternatives.'),
 dict(page=176,source_id='reviewed176 diagrams',decision='Both derived R letters have doubled vertical stems and retain mathbb R, independently of the preceding175 double-lower-rule R. All diagram targets, Gamma labels, terminal commas and parentheses match the source.'),
 dict(page=176,source_id='check/findings/findings_176_180.json#4; fixes/MISPRINTS_6.json#164',
  decision='English unchanged: both the malformed French cohomologique and corrected cohomologie refer to bounded cohomology in the same complex statement. No artificial English adjective error is introduced.'),
 dict(page=177,source_id='reviewed examples and Proposition2.3.2',decision='Restore the source C^r regularity, not inherited C-infinity. Only the first Loclib operator has its observed underline; the later occurrences stay plain. The parenthetical resp. stable is plain. Keep baseline H^0(S,.) slot and the exact separate functor displays.'),
 dict(page=177,source_id='ASTRA-II-NOTE-177',decision='Return the full paracompact extension assertion to the original numerical1 author-note layer before the body full stop.'),
 dict(page=178,source_id='check/findings/findings_176_180.json#11; fixes/MISPRINTS_6.json#167',
  decision='English unchanged: the printed singular article already selects the one category of free modules; French catégorie plural-ending repair has no separate English reading.'),
 dict(page=178,source_id='reviewed proof and Definition2.4.1',decision='Restore the entire proof, including the variable-open fiber category and all C indices, and the original three-row plain-arrow display. Stein remains plain in its definition, and only theorem is underlined in each quoted theorem A/B label; A/B and quotation marks remain independently plain.'),
 dict(page=178,source_id='ASTRA-II-REF-178-POST05',
  decision='Apply the separately saved post-checkpoint locator amendment after the frozenII patch stream. Keep printed C_0=Lib in both English forms; the exact Loclib application and contractible-disk chain maps are documented in the source identification packet and variant126.',
  identification_packet_sha256=hashlib.sha256((ROOT/'review/expose_ii_amendments/reference_178_identification.json').read_bytes()).hexdigest()),
 dict(page=179,source_id='ASTRA-II-NOTE-179',decision='Restore numerical1 and2 with full original note text, exact i_s:s→underlined S, the underlined ideal sheaf and plain local maximal ideal, and original ring subscript S,s. Delete only the separately recorded obsolete later body paragraph.'),
 dict(page=179,source_id='reviewed Remark2.4.1.1 and Examples2.4.2',decision='The Nakayama comparison stays inline with its source headless isomorphism; all exact ideal occurrences remain. Both historical editor questions retain separate paragraphs. Citations[3],[3],[13] are restored at their original examples.'),
])
for v in variants:ledger.append(dict(page=v['page'],source_id=v['source'],decision='explicit English printed/corrected variant',English_variant=v['id'],printed=v['printed'],corrected=v['corrected']))
(HERE/'EN_EXPOSE_II_TRANSFER_175_179.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in ledger))
path=HERE/'EN_AUTHOR_NOTE_MARKS.tsv'
notes=[x for x in path.read_text().splitlines() if not any(x.startswith(str(p)+'\t') for p in [175,177,179])]
notes.extend([
 '175\tStatement and repeated proof call after3.7\traised numerical1 inside baseline parentheses\t2\tASTRA-II-NOTE-175\tearly reviewer direct scan comparison, main PDF189\tSGAAuthorFootnote{1}; SGAAuthorFootMark{1}\tOne original text with two explicit calls.',
 '177\tProposition2.3.2(a), before final stop\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-177\tearly reviewer direct scan comparison, main PDF191 and witness188\tSGAAuthorFootnote{1}\tFull paracompact assertion retained as an author note.',
 '179\tAfter enough closed points\traised numerical1 inside baseline parentheses\t1\tASTRA-II-NOTE-179\tearly reviewer direct scan comparison, main PDF193 and witness190\tSGAAuthorFootnote{1}\tExact original point morphism and full SGA4 citation.',
 '179\tAfter the point defining the Ideal\traised numerical2 inside baseline parentheses\t1\tASTRA-II-NOTE-179\tearly reviewer direct scan comparison, main PDF193 and witness190\tSGAAuthorFootnote{2}\tFull ideal/fiber definition; the two original notes are not merged.'
])
path.write_text('\n'.join(notes)+'\n')
pat=re.escape(r'\sgaStableTarget{')+r'([^}]+)\}'
ot=set(re.findall(pat,record['old']));nt=set(re.findall(pat,chunk))
assert ot and ot==nt,dict(missing=sorted(ot-nt),extra=sorted(nt-ot))
print(json.dumps(dict(passage=record['id'],variants=sorted(ids),transfer_rows=len(ledger),
 stable_targets=len(ot),additional_exact_duplicate_removal=note_record['id']),ensure_ascii=False))
