#!/usr/bin/env python3
"""Prepare exact final-pass typography amendments; frozen inputs stay untouched."""
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'review/global_conventions'
sys.path.insert(0,str(ROOT/'review/english'))
from reviewed_french import load_reviewed_pages
from source_typography import transport,braced,MATH,MARK,notes,note_labels

def sha(x):return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()
def save(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def jsonl(name,rows):(OUT/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
SCOPES=[('0',1,77,'early'),('I',78,159,'expose_i'),('II',160,221,'expose_ii'),
 ('III',222,273,'expose_iii'),('IV',274,296,'expose_iv'),('V',297,364,'expose_v'),
 ('VI',365,415,'expose_vi'),('VII',416,465,'expose_vii'),('VIII',466,497,'expose_viii'),
 ('IX',498,518,'expose_ix'),('X',519,594,'expose_x'),('XII',595,615,'expose_xii'),
 ('XIII',616,666,'xiii'),('XIV',667,690,'late'),('index',691,700,'late')]
def scope(p):return next(s for s in SCOPES if s[1]<=p<=s[2])
def marker(p):return f'%%%%%%%%%%  scan idx {p+13}  |  folio {p}  %%%%%%%%%%'
def joined(pages):return ''.join(marker(p)+pages[p] for p in sorted(pages))
def split(text):
 ms=list(MARK.finditer(text))
 return {int(m.group(1)):text[m.end():ms[i+1].start() if i+1<len(ms) else len(text)] for i,m in enumerate(ms)}

fresh={
 41:['review/early/page_041_s3.png'],43:['review/early/page_043_s2.png'],
 53:['review/early/page_053_s1.png'],54:['review/early/page_054_s3.png'],63:['review/early/page_063_s3.png'],
 616:['review/xiii/images/p616_1.png'],619:['review/xiii/images/p619_1.png'],
 621:['review/xiii/images/p621_1.png','review/xiii/images/p621_2.png'],
 639:['review/xiii/images/p639_1.png','review/xiii/images/p639_2.png'],
 643:['review/xiii/images/p643_2.png'],644:['review/xiii/images/p644_1.png'],
 645:['review/xiii/images/p645_1.png'],653:['review/xiii/images/p653_1.png'],658:['review/xiii/images/p658_2.png']}
fresh[605]=['review/expose_xii/images/p605_2.png']
attributed={}
def evidence(p):
 directory=scope(p)[3];refs=[]
 for name in ['page_status','own_findings','decisions']:
  path=ROOT/f'review/{directory}/{name}.jsonl'
  if not path.exists():continue
  for n,line in enumerate(path.read_text().splitlines(),1):
   d=json.loads(line)
   if d.get('page',d.get('folio'))!=p:continue
   if name!='page_status':
    if name=='decisions' and not d.get('source_id','').startswith(('check/','ASTRA-')):continue
    s=' '.join(str(d.get(k,'')) for k in ['kind','printed_reading','reason','change'])
    if not re.search(r'underlin|word.group|emph|plain.*number|paragraph.*number|defined.term',s,re.I):continue
   rel=str(path.relative_to(ROOT))+f'#{n}'
   attributed[rel]=dict(record_sha256=sha(line),record=d)
   refs.append(rel)
 return refs

allpatch=[];groups=[];counts=[];proofs={};raws={};finals={};exclusions=[]
for layer in ['diplomatic','current']:
 input_paths=[ROOT/f'fr/sga6/{layer}/main.tex']+sorted((ROOT/'review').glob('*/patches.jsonl'))
 input_paths+=sorted((ROOT/'build/page_packets').glob(f'*/{layer}.tex'))
 input_paths+=sorted((ROOT/'review').glob('*/new_pages.jsonl'))
 fingerprint=sha(''.join(str(p.relative_to(ROOT))+sha(p.read_bytes()) for p in input_paths))
 cached=OUT/f'loaded_{layer}.json'
 obj=json.loads(cached.read_text()) if cached.exists() else None
 if obj and obj['input_fingerprint']==fingerprint:
  pages={int(k):v for k,v in obj['pages'].items()};meta=obj['metadata']
 else:
  pages,meta=load_reviewed_pages(700,layer=layer,start=1)
  save(cached.name,dict(input_fingerprint=fingerprint,pages=pages,metadata=meta))
 raw=joined(pages);raws[layer]=raw
 final,changes,proof=transport(raw,{616,619,621,658},{43,639,643,644,645})
 assert len(changes)==387,(layer,len(changes))
 assert sum(len(c['plain_nested']) for c in changes)==6
 assert sum(len(c['plain_resp']) for c in changes)==8
 # Existing statement labels, including a separated statement number following
 # the author note on205, retain NOTE_6's expressly permitted label styling.
 bold=[]
 for m in re.finditer(r'\\textbf\{',final):
  b,z=braced(final,m.end()-1)
  if not re.fullmatch(r'\s*\d+(?:\.\d+)*\.?\s*',b):continue
  prev=[q for q in MARK.finditer(final,0,m.start())]
  p=int(prev[-1].group(1))
  if p==205 and b=='2.2.':continue
  replacement=r'\textnormal{3.2.}' if p==605 and b=='3.2.' else b
  bold.append(dict(start=m.start(),end=z,page=p,old=final[m.start():z],new=replacement,
                   kind='plain_paragraph_number'))
 assert len(bold)==77,(layer,len(bold))
 for c in reversed(bold):final=final[:c['start']]+c['new']+final[c['end']:]
 # Bold numeric wrappers never occur in a mathematical unit or author note.
 interim,_,_=transport(raw,{616,619,621,658},{43,639,643,644,645})
 before_units=[m.group() for m in MATH.finditer(interim)]
 after_units=[m.group() for m in MATH.finditer(final)]
 assert sum(u.count(r'\textbf{3.2.}') for u in before_units)==1
 assert [u.replace(r'\textbf{3.2.}',r'\textnormal{3.2.}') for u in before_units]==after_units
 proof['explicit_display_number_transport']=dict(page=605,old=r'\textbf{3.2.}',new=r'\textnormal{3.2.}',
    reason='Fresh main605 lower view shows an ordinary standalone paragraph label3.2 to the left of the formula. Only its font wrapper changes; the equality and every formula byte remain identical.')
 assert note_labels(raw)==note_labels(final)
 final_pages=split(final);finals[layer]=final
 assert set(final_pages)==set(pages)
 candidates=[]
 for number,c in enumerate(changes,1):
  kind='word_rules';p=c['page']
  oldparts=MARK.split(c['old']);newparts=MARK.split(c['new'])
  # re.split captures only each marker's folio number. All marker strings stay
  # literal, and the surrounding page fragments can be patched independently.
  assert len(oldparts)==len(newparts)
  local_pages=[p]+[int(x) for x in oldparts[1::2]]
  assert oldparts[1::2]==newparts[1::2]
  for pi,oldpart,newpart in zip(local_pages,oldparts[0::2],newparts[0::2]):
   if oldpart==newpart:continue
   assert oldpart
   candidates.append(dict(page=pi,layer=layer,old=oldpart,new=newpart,kind=kind,
       source_id=f'ASTRA-GLOBAL-WORD-RULES-{pi:03d}',reason='Render the exact previously inspected lexical emphasis span; preserve all mathematical units, author-note commands and explicit plain exclusions.'))
  groups.append(dict(layer=layer,group_index=number,**c))
  for field in ['plain_nested','plain_resp','plain_references']:
   for item in c[field]:exclusions.append(dict(layer=layer,group_index=number,kind=field,**item))
 for c in bold:
  candidates.append(dict(page=c['page'],layer=layer,old=c['old'],new=c['new'],
    kind='plain_paragraph_number',source_id=f'ASTRA-GLOBAL-PARAGRAPH-{c["page"]:03d}',
    reason='Remove only the bold wrapper of this independently numbered paragraph, under GLOBAL_ISSUES81; retain the same numeral and punctuation bytes. Statement-label styling is separately retained.'))
 # Coalesce identical local replacements; the count is checked at the precise
 # point where the patch is applied, not inferred from a chapter-wide regex.
 merged={}
 for c in candidates:
  key=(c['page'],c['old'],c['new'],c['kind'])
  if key not in merged:merged[key]=dict(c,expected_count=0)
  merged[key]['expected_count']+=1
 test=dict(pages)
 for c in merged.values():
  p=c['page'];n=test[p].count(c['old'])
  assert n==c['expected_count'],(layer,p,n,c['expected_count'],c['old'][:100])
  test[p]=test[p].replace(c['old'],c['new'],n)
  allpatch.append(c)
 assert test==final_pages,('Exact patch sequence differs from formatter result',layer)
 proofs[layer]=dict(**proof,source_sha256=sha(raw),final_sha256=sha(final),
    original_emph_commands=raw.count(r'\emph{'),top_level_groups=len(changes),
    nested_plain_exclusions=6,plain_resp_exclusions=8,plain_paragraph_number_wrappers=77,
    remaining_emph_commands=final.count(r'\emph{'),
    word_spans_added=sum(c['word_spans'] for c in changes),
    source_page_hashes={str(p):sha(pages[p]) for p in pages},
    final_page_hashes={str(p):sha(final_pages[p]) for p in final_pages})
 assert proofs[layer]['remaining_emph_commands']==0
 for label,a,b,directory in SCOPES:
  cs=[c for c in changes if a<=c['page']<=b]
  counts.append(dict(layer=layer,expose=label,start=a,end=b,
    input_emph_commands=sum(pages[p].count(r'\emph{') for p in range(a,b+1)),
    top_level_groups=len(cs),word_spans_added=sum(c['word_spans'] for c in cs),
    nested_plain_exclusions=sum(len(c['plain_nested']) for c in cs),
    plain_resp_exclusions=sum(len(c['plain_resp']) for c in cs),
    plain_reference_exclusions=sum(len(c['plain_references']) for c in cs),
    paragraph_numbers_restored=sum(a<=c['page']<=b for c in bold),
    existing_uline_commands=sum(pages[p].count(r'\uline{') for p in range(a,b+1)),
    final_uline_commands=sum(final_pages[p].count(r'\uline{') for p in range(a,b+1))))
 save(f'composed_{layer}_page_metadata.json',meta)
 (OUT/f'FR_{layer}_typography_proposed.tex').write_text(final)

# A same old/new/count at the same page is one both-layer patch. Branch-specific
# accepted source corrections keep their own layer and exact wording.
index={};patches=[]
for d in allpatch:
 key=tuple(d[k] for k in ['page','old','new','kind','expected_count'])
 if key in index:
  prev=patches[index[key]]
  assert prev['layer']!=d['layer'];prev['layer']='both'
 else:index[key]=len(patches);patches.append(d)
for n,p in enumerate(patches,1):p['patch_id']=f'ASTRA-GLOBAL-TYPO-P{n:04d}'
jsonl('post_review_patches.jsonl',patches)
save('typography_groups.json',groups)
save('plain_exclusions.json',exclusions)
save('typography_counts.json',counts)
save('transport_validation.json',proofs)

own=[]
for p in sorted({d['page'] for d in patches}):
 refs=evidence(p)
 word=[d for d in patches if d['page']==p and d['kind']=='word_rules']
 paragraph=[d for d in patches if d['page']==p and d['kind']=='plain_paragraph_number']
 shared=dict(page=p,record_type='own',kind='convention',verdict='not applied and now proposed in final pass',
  image=f'scan/SGA6_scan_360dpi.pdf#page={p+14}',
  evidence_mode='attributed completed source review; bounded reinspection recorded separately',
  evidence_refs=refs,new_image_files=fresh.get(p,[]),new_full_page_certification=False,
  forms='French diplomatic and corrected; source-linked typography transfer to English required.',
  is_misprint=False,source_body_content_changed=False,
  patch_stream='review/global_conventions/post_review_patches.jsonl')
 if word:
  row=dict(shared,source_id=f'ASTRA-GLOBAL-WORD-RULES-{p:03d}',
    printed_reading='Inspected lexical word-group rules, with mathematics and the explicitly listed defined terms, references and resp. occurrences outside them.',
    tex='Retained emph wrappers awaiting the delegated source-typography pass.',
    change='Replace only the mapped lexical wrappers by upright uline groups; preserve exact literal math and notes.',
    reason='The completed page review and its exact underline decisions supply the printed spans. The retained emphasis group boundaries are rendered rather than reselected. '
     'The nested XIII exclusions and plain numerical-reference/resp. occurrences are listed individually in plain_exclusions.json, with the fresh supporting regions recorded here. '
     'Cross-folio groups are divided only at their existing literal marker comments; no word, marker, mathematical command or note label is moved. '
     'The transport comparison is the identity on every mathematical token and every mathematical object/map that those tokens name. '
     'The in-math wrapper changes are the four separately confirmed lexical words in text commands on73–75 and the separately recorded ordinary paragraph label3.2 on605; every other byte of each mathematical unit is identical.',
    region='The exact emph groups and their source-located exclusions in typography_groups.json',
    patch_ids=[d['patch_id'] for d in word])
  own.append(row)
 if paragraph:
  own.append(dict(shared,source_id=f'ASTRA-GLOBAL-PARAGRAPH-{p:03d}',
    printed_reading='Ordinary typed standalone paragraph numbers; the same labels and terminal stops are retained.',
    tex='Bold wrappers around standalone numeric paragraph labels.',
    change='Remove only the listed textbf wrappers.',
    reason='GLOBAL_ISSUES81 and NOTE_6 defer these ordinary numbered paragraphs for a volume decision. The complete source page has already been read. '
     'This pass inventories every remaining pure numeric paragraph wrapper and restores ordinary weight. '
     'A statement label containing its label word remains under the expressly accepted NOTE_6 convention; the separated Proposition number2.2 on205 is also retained with that statement label. '
     'The mapping fixes every digit, full stop, item order and cross-reference target; it changes only the font wrapper.',
    region='Standalone numbered paragraphs listed in bold_item_paragraph_inventory.json',
    patch_ids=[d['patch_id'] for d in paragraph]))
jsonl('own_findings.jsonl',own)
save('attributed_typography_records.json',attributed)
save('fresh_region_evidence.json',dict(
    scope='Bounded typography reinspection only; existing complete page certificates stay unchanged.',
    images=fresh,
    observations=[
     '41: four parenthesized equation references have no rule, while the surrounding statement words and et do.',
     '43: both resp. abbreviations in Theorem2.3(i) are plain.',
     '53 and54: leading(2.22) and embedded(2.29) are plain.',
     '63: the locator2.2 after the ruled word théorème is plain.',
     '605: the standalone paragraph label3.2 at the left of the display has ordinary weight. The formula to its right is untouched.',
     '616 and619: defining m-régulier and(b)-faisceau are plain; the surrounding definition words are ruled.',
     '621: defining(b)-polynômes is plain; the theorem locator1.9 is plain; the parenthetical theorem title words are ruled.',
     '639: both resp. are plain; voir is ruled;4.1 is plain; Lemme is ruled and3.11 plain in print.',
     '643,644,645: their one,one,two statement resp. tokens are plain; other statement words are ruled.',
     '644: standalone4.4 is ordinary typed text.',
     '653: standalone6.1 is ordinary typed; the lemma phrase Sous les conditions de is ruled and its6.1 reference plain.',
     '658: the defining k-cycle phrase, intègre and degré are all plain inside the ruled definition; lemma6.10 reuses the same words with the visible statement rules.']))

summary=dict(status='exact final-pass typography proposals complete',
    patch_records=len(patches),layer_applications=sum(2 if p['layer']=='both' else 1 for p in patches),
    own_records=len(own),changed_pages=sorted({p['page'] for p in patches}),
    original_emph_commands_each_layer=393,top_level_emphasis_groups_each_layer=387,
    nested_plain_exclusions_each_layer=6,plain_resp_exclusions_each_layer=8,
    plain_paragraph_number_wrappers_each_layer=77,
    source_body_words_or_formulas_changed=False,author_note_labels_identical=True,
    author_note_body_typography_transports_recorded=True,
    new_full_page_certifications=0,
    integration_order='Explicit final pass after every ordinary review patch, in both French builder and reviewed_french loader.',
    frozen_inputs_modified=False,
    patch_sha256=sha((OUT/'post_review_patches.jsonl').read_bytes()))
save('TYPOGRAPHY_HANDOFF.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
