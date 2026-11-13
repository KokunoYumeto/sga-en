"""Printed-folio correspondences from numbered structure and exact formula anchors."""
from pathlib import Path
import json,re,bisect,difflib,collections,csv
import prepare_english as p
OUT=Path(__file__).parent
FR=Path('work/sources/SGA5_FR/fr/sga5/current/s5.tex')
EXPOSES=[(1,'I'),(73,'III'),(138,'III B'),(204,'V'),(251,'VI'),(282,'VII'),(351,'VIII'),(372,'X'),(407,'XII'),(442,'XV'),(481,'Index')]

def group(s,i):
 assert s[i]=='{';lev=1;j=i+1
 while lev and j<len(s):
  if s[j]=='{' and s[j-1]!='\\':lev+=1
  elif s[j]=='}' and s[j-1]!='\\':lev-=1
  j+=1
 return s[i+1:j-1],j

def heads(s):
 out=[]
 clean=p.uncomment(s)
 rx=re.compile(r'\\(section|subsection|subsubsection|paragraph)(\*?)\{|\\begin\{statement\}\{')
 section=0;last=0
 for m in rx.finditer(clean):
  resets=list(re.finditer(r'\\setcounter\{section\}\{(\d+)\}',clean[last:m.start()]))
  if resets:section=int(resets[-1][1])
  title,end=group(s,m.end()-1);kind=m[1] or 'statement'
  last=end
  if kind=='section' and not m[2]:section+=1
  nm=re.search(r'(?<!\w)([A-D]\.\d+(?:\.\d+)*|\d+(?:\.\d+)*)',title)
  num=nm[1] if nm else (str(section) if kind=='section' and not m[2] else '')
  role=''
  for a,b in [('Corollaire','cor'),('Corollary','cor'),('Proposition','prop'),('Lemme','lem'),('Lemma','lem'),('Théorème','thm'),('Theorem','thm'),('Définition','def'),('Definition','def'),('Remarque','rem'),('Remark','rem'),('Example','ex'),('Exemple','ex')]:
   if a.lower() in title.lower():role=b;break
  out.append({'start':m.start(),'end':end,'title':title,'kind':kind,'number':num,'role':role})
 return out

def make():
 fr=FR.read_text();en=(OUT/'EN_corrected_flat.tex').read_text();fc,ec,direct,anchors=p.align_math(fr,en)
 fp=p.getpages(fr);fstarts=[v['start'] for v in fp.values()];folios=list(fp)
 def ffolio(x):return folios[max(0,bisect.bisect_right(fstarts,x)-1)]
 fa,ea=heads(fr),heads(en)
 for h in fa:h['folio']=ffolio(h['start']);h['expose']=p.expose(h['folio'])
 ens=[]
 for m in re.finditer(r'\\phantomsection\\addcontentsline\{toc\}\{section\}\{Exposé (I|III B|III|V|VI|VII|VIII|X|XII|XV) ---',en):
  ex=m[1];pg=next(pg for pg,e in EXPOSES if e==ex);ens.append({'position':m.start(),'folio':pg,'kind':'expose','confidence':'explicit exposé correspondence','source':f'fr/sga5/current/s5.tex:folio{pg}','anchor':f'Exposé {ex}'})
 for name,pg in [('Terminological Index',481),('Index of Notation',483)]:
  needle=r'\section*{'+name+'}';pos=en.index(needle);ens.append({'position':pos,'folio':pg,'kind':'index','confidence':'explicit index correspondence','source':f'fr/sga5/current/s5.tex:folio{pg}','anchor':name})
 ens.sort(key=lambda x:x['position']);estarts=[x['position'] for x in ens]
 am=[a for a,b in anchors];bm=[b for a,b in anchors]
 records=[];unmatched=[]
 # Exact bilingual heading matches supplement the numeric parser, including
 # French run-in bold headings represented as English statement headings.
 manual_specs=[
 ('Definition and formal properties','Définition et propriétés formelles des complexes dualisants',3),
 ('Scholium 1.12.1',r'\textbf{Scholie :}',13),
 ('3.1.2. Dévissage',r'\textbf{3.1.2. Dévissage de faisceaux constructibles.}',22),
 ('3.1.6. Cohomological',r'\textbf{3.1.6. Finitude cohomologique.}',25),
 ('Bibliography','BIBLIOGRAPHIE',54),('Appendix','APPENDICE',55),('Bibliography','BIBLIOGRAPHIE',72),
 ('Contents','SOMMAIRE.',75),
 ('Notation and recalls','1. Notations et rappels de formules de Künneth.',76),
 ('Functoriality of','2. Fonctorialité de',81),
 ('Cohomological Correspondences','3. Correspondances cohomologiques.',89),
 ('Pairings of Correspondences','4. Accouplements de correspondances. Formule de Lefschetz.',99),
 ('Bibliography','BIBLIOGRAPHIE.',136),
 ('Exposé III B',r'Exposé III B\\CALCULS DE TERMES LOCAUX',138),
 ('Introduction','Cet exposé, rédigé en janvier 1977',138),
 ('Summary','Sommaire.',139),
 ('I. Correspondences in General Position','I. - Correspondances en position générale entre courbes.',140),
 ('II. Equivariant','II. Correspondances équivariantes.',162),
 ('Bibliography','BIBLIOGRAPHIE.',203),
 ('Exposé V.',r'EXPOSÉ V\\SYSTÈMES PROJECTIFS $J$-ADIQUES',204),
 ("Appendix: Shih's theorem",'Appendice: le théorème de SHIH.',243),
 ('Functoriality.','Fonctorialité.',244),
 ('Exposé VI','EXPOSÉ VI',251),('Remark',r'\begin{statement}{Remarque}',260),
 ('Exposé VII','EXPOSÉ VII',282),('Exposé VIII','Exposé VIII',351),
 ('Lemma',r'\begin{statement}{Lemme}',367),
 ('Exposé X ---','Exposé X',372),('References','Références',406),
 ('Exposé XII','Exposé XII',407),
 ('d) The case of a sheaf',r'd) Le cas du faisceau $F$ qui ne se ramifie pas',437),
 ('Exposé XV','EXPOSÉ XV',442),
 ('2. Effect on cohomology',r'n\textsuperscript{o} 2. Effet sur la cohomologie.',456),
 ('3. Behavior of products',r'n\textsuperscript{o} 3. Comportement des produits.',458),
 ('Terminological Index','Index terminologique',481),('Index of Notation','Index des notations',483)]
 manual={}
 for eprefix,fneedle,pg in manual_specs:
  part=fp[pg];assert fneedle in part['text'],('French heading absent',pg,fneedle)
  fpos=part['start']+part['text'].index(fneedle)
  options=[h for h in ea if h['title'].startswith(eprefix)]
  assert options,('English heading absent',pg,eprefix)
  aim=p.estimate(fpos,anchors);h=min(options,key=lambda h:abs(h['start']-aim))
  assert h['start'] not in manual,('Manual heading selected twice',h)
  manual[h['start']]={'position':h['start'],'folio':pg,'kind':'explicit_'+h['kind'],'confidence':'exact bilingual heading or run-in label correspondence','anchor':h['title'],'fr_anchor':fneedle,'fr_position':fpos,'source':'fr/sga5/current/s5.tex;fr/sga5/diplomatic/s5.tex'}
 for h in ea:
  if h['start']<ens[0]['position']:continue
  if h['start'] in manual:records.append(manual[h['start']]);continue
  ei=bisect.bisect_right(estarts,h['start'])-1;ex=p.expose(ens[max(0,ei)]['folio'])
  ai=bisect.bisect_left(bm,h['start']);lo=anchors[max(0,ai-1)][0];hi=anchors[min(len(anchors)-1,ai)][0]
  candidates=[f for f in fa if f['expose']==ex and (f['number']==h['number']) and (f['role']==h['role']) and f['kind']==h['kind']]
  if not candidates and h['number']:candidates=[f for f in fa if f['expose']==ex and f['number']==h['number'] and f['role']==h['role']]
  local=[f for f in candidates if lo-250<=f['start']<=hi+250]
  if local:candidates=local
  if candidates and h['number']:
   f=min(candidates,key=lambda f:min(abs(f['start']-lo),abs(f['start']-hi)))
   # Require the structural match to lie in the neighboring formula window.
   if f['start']<lo-2000 or f['start']>hi+2000:
    unmatched.append(h);continue
   records.append({'position':h['start'],'folio':f['folio'],'kind':'numbered_'+h['kind'],'confidence':'matched numbered structure within exact formula-anchor window','anchor':h['title'],'fr_anchor':f['title'],'source':'fr/sga5/current/s5.tex','fr_position':f['start']})
  else:
   # Unnumbered source headings are resolved only when the neighboring source paragraphs lie on one folio.
   p0,p1=ffolio(lo),ffolio(hi)
   if p0==p1:
    records.append({'position':h['start'],'folio':p0,'kind':'bounded_'+h['kind'],'confidence':'heading bounded by exact formula anchors on a single printed folio','anchor':h['title'],'source':'fr/sga5/current/s5.tex'})
   else:unmatched.append(h)
 # Each printed folio may additionally be identified at the beginning of its first matched English paragraph.
 # A paragraph is eligible only when its first matched formula also begins a French paragraph on that folio.
 byfolio={}
 emstarts=[m['start'] for m in ec]
 # Group depth is computed from TeX control sequences, so escaped braces
 # do not masquerade as grouping and paragraph markers never split a macro.
 depth=0;depth_at={0:0}
 for m in re.finditer(r'\\(?:[A-Za-z@]+|.)|[{}]',p.uncomment(en),re.S):
  if m[0]=='{':depth+=1
  elif m[0]=='}':depth-=1
  depth_at[m.end()]=depth
 depth_keys=sorted(depth_at)
 def safe_position(pos):
  j=bisect.bisect_right(emstarts,pos)-1
  if j>=0 and ec[j]['start']<pos<ec[j]['end']:return False
  return depth_at[depth_keys[max(0,bisect.bisect_right(depth_keys,pos)-1)]]==0
 for fpos,epos in anchors:
  pg=ffolio(fpos)
  if pg in byfolio:continue
  fs=fr.rfind('\n\n',0,fpos)+2;es=en.rfind('\n\n',0,epos)+2
  if es<ens[0]['position'] or ffolio(fs)!=pg:continue
  if not safe_position(es):continue
  # A formula at the paragraph start, or a short preceding sentence without another formula, anchors this paragraph.
  if fpos-fs<=750 and epos-es<=750 and '\\begin{tikz' not in en[es:epos]:
   # Do not insert in a math environment or an enclosing grouped macro.
   st=en[es:epos]
   if st.count('$')%2 or st.count(r'\[')>st.count(r'\]'):continue
   byfolio[pg]={'position':es,'folio':pg,'kind':'paragraph','confidence':'corresponding paragraph containing exact formula anchor','source':'fr/sga5/current/s5.tex','fr_position':fs,'formula_fr':fr[fpos:min(fpos+90,len(fr))],'formula_en':en[epos:min(epos+90,len(en))]}
 # Keep all section anchors; paragraph markers are restricted to monotonically ordered folios.
 allrecs=ens+records+list(byfolio.values())
 represented={r['folio'] for r in allrecs}
 # Where a printed page starts within a paragraph, the first exact formula
 # correspondence supplies a narrower, explicitly labelled anchor.
 for fpos,epos in anchors:
  pg=ffolio(fpos)
  if pg in represented or not safe_position(epos):continue
  allrecs.append({'position':epos,'folio':pg,'kind':'formula','confidence':'exact corresponding formula occurrence on the stated French folio','source':'fr/sga5/current/s5.tex','fr_position':fpos,'formula_fr':fr[fpos:min(fpos+90,len(fr))],'formula_en':en[epos:min(epos+90,len(en))]});represented.add(pg)
 # The two index continuation pages are aligned by the exact bilingual entry
 # pair already verified against their identical exposé/section references.
 pairs=json.loads(Path('work/contributions/decisions/index_glossary_pairs.json').read_text())
 for pg in [482,484]:
  pair=next(r for r in pairs if r['index_folio']==pg)
  needle=r'\sgaindexentry{'+pair['English_rendering']+'}{'+pair['English_references']+'}'
  assert en.count(needle)==1,(pg,needle,en.count(needle))
  allrecs.append({'position':en.index(needle),'folio':pg,'kind':'index_entry','confidence':'exact bilingual index entry with verified identical reference','source':'fr/sga5/current/s5.tex;en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex','anchor':pair['English_rendering'],'fr_anchor':pair['French_term_or_notation'],'fr_position':pair['FR_char_offset']})
 allrecs.sort(key=lambda x:(x['position'],x['folio']))
 result=[];prev=0;seenpos=set();rejected=[]
 for r in allrecs:
  if r['position'] in seenpos:continue
  if r['folio']<prev:
   rejected.append({**r,'reason':'would reverse printed-folio order'});continue
  if result and r['folio']==prev and r['kind']=='paragraph':continue
  result.append(r);seenpos.add(r['position']);prev=r['folio']
 # English offsets for diplomatic text are computed from the exact annotated variants.
 variants=json.loads((OUT/'EN_variants.json').read_text());variants.sort(key=lambda v:v['start_corrected'])
 for r in result:
  delta=0;inside=False
  for v in variants:
   a,b=v['start_corrected'],v['end_corrected']
   if b<=r['position']:delta+=len(v['before'])-len(v['after'])
   elif a<r['position']<b:inside=True;break
  r['position_corrected']=r.pop('position');r['position_diplomatic']=r['position_corrected']+delta
  if inside:r['in_variant']=True
 (OUT/'EN_ALIGNMENT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 (OUT/'EN_ALIGNMENT_UNPLACED.json').write_text(json.dumps({'unmatched_headings':unmatched,'nonmonotone_rejected':rejected},ensure_ascii=False,indent=2))
 with (OUT/'EN_ALIGNMENT.tsv').open('w') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n')
  w.writerow(['folio','expose','kind','English corrected source offset','English diplomatic source offset','English anchor','French anchor','confidence','source'])
  for r in result:w.writerow([r['folio'],p.expose(r['folio']),r['kind'],r['position_corrected'],r['position_diplomatic'],r.get('anchor',r.get('formula_en','')),r.get('fr_anchor',r.get('formula_fr','')),r['confidence'],r['source']])
 (OUT/'EN_ALIGNMENT_SUMMARY.json').write_text(json.dumps({'formula_anchors':len(anchors),'markers':len(result),'distinct_folios':len(set(r['folio'] for r in result)),'kind_counts':dict(collections.Counter(r['kind'] for r in result)),'unmatched_headings':len(unmatched),'nonmonotone_rejected':len(rejected)},indent=2))
 print(json.dumps({'anchors':len(anchors),'markers':len(result),'folios':len(set(r['folio'] for r in result)),'unmatched':len(unmatched),'rejected':len(rejected)}))
if __name__=='__main__':
 import csv
 make()
