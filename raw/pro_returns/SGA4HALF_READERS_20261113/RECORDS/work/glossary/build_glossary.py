"""Count technical vocabulary in the corrected bilingual masters.
The inventory combines supplied SGA4/SGA7 term pairs with separately reviewed
SGA4HALF definitions. Counts are exact English surface-form occurrences on
aligned printed pages that also attest the French expression. They are not
lemmatized token counts; case is ignored. Formula/label/citation syntax is not
counted as prose. Named mathematical commands are counted separately.
"""
from pathlib import Path
import re,csv,json,unicodedata,collections,bisect,sys,hashlib
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[2];B=Path(__file__).parent
sys.path.insert(0,str(ROOT/'work/sommes'))
from compare_math import arg,select
from apply_glossary import apply_glossary
SOURCES=[
 ('Introduction','arcata','sga4.5-intro.tex','sga4half_intro_en.tex'),
 ('Ariane','arcata','ariane.tex','ariane_en.tex'),
 ('Arcata','arcata','sga4.5-1.tex','sga4half_1_en.tex'),
 ('Rapport','rapport_cycle','sga4.5-2.tex','sga4half_2_en.tex'),
 ('Fonctions L','rapport_cycle','sga4.5-3.tex','sga4half_3_en.tex'),
 ('Cycle','rapport_cycle','sga4.5-4.tex','sga4half_4_en.tex'),
 ('Dualité','rapport_cycle','sga4.5-5.tex','sga4half_5_en.tex'),
 ('Sommes trigonométriques','sommes','sga4.5-6.tex','sga4half_6_en.tex'),
 ('Finitude','finitude_verdier','sga4.5-7.tex','sga4half_7_en.tex'),
 ('Catégories dérivées','finitude_verdier','sga4.5-8.tex','sga4half_8_en.tex'),
 ('Erratum','finitude_verdier','sga4.5-erratum.tex','sga4half_erratum_en.tex')]


def choose_macro(t,name,nargs,selected):
 tok='\\'+name
 start=0
 while True:
  m=re.search(re.escape(tok)+r'(?=\s*\{)',t[start:])
  if not m:break
  i=start+m.start();p=start+m.end();aa=[]
  for _ in range(nargs):a,p=arg(t,p);aa.append(a)
  t=t[:i]+aa[selected]+t[p:];start=i
 return t


def accents(t):
 marks={"'":'\u0301','`':'\u0300','^':'\u0302','"':'\u0308','~':'\u0303'}
 t=re.sub(r'\\([\'`^"~])\{?([A-Za-z])\}?',lambda m:unicodedata.normalize('NFC',m[2]+marks[m[1]]),t)
 t=re.sub(r'\\c\s*\{?([Cc])\}?',lambda m:'Ç' if m[1]=='C' else 'ç',t)
 for a,b in [(r'\oe','œ'),(r'\OE','Œ'),(r'\ae','æ'),(r'\AA','Å')]:t=t.replace(a,b)
 return t

def prose(t):
 t=select(t,1);t=choose_macro(t,'PrintCite',2,0);t=choose_macro(t,'texorpdfstring',2,0)
 t=re.sub(r'(?<!\\)%[^\n]*','',t)
 t=re.sub(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',r' ZZPAGE\1ZZ ',t)
 t=re.sub(r'\\chaptermark\{[^}]*\}','',t)
 # Bibliographic entries retain original publication languages and are not
 # translated terminology; only the translated Bibliography heading is counted.
 bib_heading=r'\\section\*\{(?:Bibliographie|Bibliography)\}|\\begin\{center\}\\textbf\{(?:Bibliographie|Bibliography)\.\}\\end\{center\}|\\textbf\{\\underline\{Bibliographie\.\}\}'
 t=re.sub('('+bib_heading+r')[\s\S]*',lambda m:m[1]+' '+' '.join(re.findall(r'ZZPAGE[^\s{}]*?ZZ',m[0])),t)
 t=t.replace(r'$\ell$', 'ℓ').replace(r'$\ell^n$', 'ℓⁿ')
 t=re.sub(r'\\(?:label|ref|eqref)\{[^}]*\}',' ',t)
 t=re.sub(r'\\cite(?:\[[^\]]*\])?\{[^}]*\}',' ',t)
 t=re.sub(r'\\hyperref\[[^\]]*\]','',t)
 t=re.sub(r'\\hyperlink\{[^}]*\}','',t)
 def math_words(m):
  s=m[0];parts=[]
  # Retain prose within formula annotations and page markers inside displays.
  for q in re.finditer(r'ZZPAGE[^\s{}]*?ZZ|\\text(?:normal)?\{',s):
   if q[0].startswith('ZZPAGE'):parts.append((q.start(),q[0]))
   else:
    try:a,e=arg(s,q.end()-1);parts.append((q.start(),a))
    except (AssertionError,IndexError):pass
  return ' '+' '.join(x for _,x in sorted(parts))+' '
 t=re.sub(r'\\\[[\s\S]*?\\\]|\\begin\{(?:equation\*?|align\*?|alignat\*?|gather\*?)\}[\s\S]*?\\end\{(?:equation\*?|align\*?|alignat\*?|gather\*?)\}',math_words,t)
 t=re.sub(r'(?<!\\)\$[^$]*?(?<!\\)\$',math_words,t)
 t=accents(t)
 t=re.sub(r'\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?',' ',t)
 t=re.sub(r'\\(?:setcounter|addtocounter)\{[^}]*\}\{[^}]*\}',' ',t)
 t=re.sub(r'\\[A-Za-z@]+\*?',' ',t)
 t=t.replace('~',' ').replace('{','').replace('}','').replace('\\',' ').replace('’',"'")
 t=t.replace('``','"').replace("''",'"').replace('--','-').replace('–','-').replace('‑','-')
 t=re.sub(r'\s+',' ',t).strip()
 return t

def getpages(t):
 a=re.split(r'ZZPAGE([^\s{}]*?)ZZ',t)
 return {a[i]:a[i+1] for i in range(1,len(a),2)}

@lru_cache(maxsize=8192)
def termnorm(s):return re.sub(r'\s+',' ',accents(s).replace('’',"'").replace('--','-').replace('–','-')).strip().casefold()
@lru_cache(maxsize=4096)
def rx(s):return re.compile(r'(?<![\wÀ-ÿ])'+re.escape(termnorm(s))+r'(?![\wÀ-ÿ])')
def termfind(t,s):return list(rx(s).finditer(termnorm(t)))

raw={};pages={};parts={};glossary_patches=[];input_hashes=[]
for part,owner,ff,ef in SOURCES:
 for L,F in [('fr',ff),('en',ef)]:
  p=ROOT/'work'/owner/L/F
  if not p.exists():raise SystemExit('Missing finalized component '+str(p.relative_to(ROOT)))
  t=p.read_text()
  input_hashes.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(t.encode()).hexdigest()))
  if L=='en':t,patches=apply_glossary(t,language='en',component=F);glossary_patches.extend(patches)
  raw[L,part]=select(t,1)
  pp=getpages(prose(t))
  for n,body in pp.items():
   if (L,n) in pages:raise ValueError(('duplicate page',L,n))
   pages[L,n]=body;parts[n]=part
(B/'GLOSSARY_PATCHES.json').write_text(json.dumps(glossary_patches,ensure_ascii=False,indent=2))

catalogue={}
for fn in ['GLOSSARY_SGA4_FR_EN.tsv','GLOSSARY_SGA7_FR_EN.tsv']:
 with (ROOT/'source/en/glossaries'/fn).open() as f:
  for r in csv.DictReader(f,delimiter='\t'):
   fr=r.get('french_term_or_notation',r.get('french',''));en=r.get('english_rendering',r.get('english',''))
   # Commands, isolated variable names and corrupted overlong glossary excerpts
   # are not imported as terminology. Mathematical notation is inventoried below.
   if '\\' in fr or '\\' in en or len(fr)<3 or len(fr)>100 or len(en)>130 or fr.startswith(('=','(')):continue
   key=(termnorm(fr),termnorm(en))
   catalogue.setdefault(key,dict(fr=fr,en=en,sources=set()))['sources'].add(fn)

custom=B/'reviewed_pairs.json'
if custom.exists():
 for r in json.loads(custom.read_text()):
  key=(termnorm(r['fr']),termnorm(r['en']))
  catalogue.setdefault(key,dict(fr=r['fr'],en=r['en'],sources=set()))['sources'].add(r.get('source','SGA4HALF reviewed pair'))

# Discover emphasis-aligned pairs for human review; do not silently add them.
def emphasis_spans(t):
 out=[]
 for m in re.finditer(r'\\emph\{',t):
  try:a,e=arg(t,m.end()-1)
  except (AssertionError,IndexError):continue
  projected=prose('\\PrintPage{x}'+a);projected=getpages(projected).get('x','').strip()
  out.append(dict(tex=a,prose=projected))
 return out
def emphasized(t):return [s['prose'] for s in emphasis_spans(t) if 2<len(s['prose'])<90]
review=[];census=[];unequal=[]
for p in parts:
 # Read emphasis within actual TeX printed-page pieces.
 for part,owner,ff,ef in SOURCES:
  if part!=parts[p]:continue
  pair=[]
  for L in ['fr','en']:
   ss=re.split(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',raw[L,part]);dd={ss[i]:ss[i+1] for i in range(1,len(ss),2)}
   for index,span in enumerate(emphasis_spans(dd.get(p,'')),1):
    census.append(dict(part=part,page=p,language=L,index=index,**span))
   pair.append(emphasized(dd.get(p,'')))
  if len(pair[0])==len(pair[1]):
   for f,e in zip(*pair):
    if (termnorm(f),termnorm(e)) not in catalogue:review.append(dict(page=p,fr=f,en=e))
  else:unequal.append(dict(part=part,page=p,fr=pair[0],en=pair[1]))
(B/'emphasis_pairs_for_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
(B/'GLOSSARY_SOURCE_CENSUS.json').write_text(json.dumps(census,ensure_ascii=False,indent=2))
(B/'unequal_emphasis_sequences.json').write_text(json.dumps(unequal,ensure_ascii=False,indent=2))

rows=[];attest=[]
order=['III','IV']+[str(x) for x in range(1,313)]
for (fr,en),r in catalogue.items():
 hits=[];fr_total=0
 for p in order:
  f=pages.get(('fr',p),'');e=pages.get(('en',p),'')
  fm=termfind(f,fr);em=termfind(e,en)
  fr_total+=len(fm)
  if fm and em:
   for m in em:hits.append((p,m,termnorm(e)))
 if not hits:continue
 p=hits[0][0]
 rows.append(dict(french_term_or_notation=r['fr'],english_rendering=r['en'],count=len(hits),first_place=parts[p]+'; printed p. '+p,method='exact English surface form on an aligned page attesting French expression; case ignored',reference='; '.join(sorted(r['sources']))))
 for p,m,t in hits:attest.append(dict(fr=r['fr'],en=r['en'],page=p,context=t[max(0,m.start()-100):m.end()+100]))

# Authorial named mathematical symbols/operators, in the retained Miller system.
commands=set()
for (L,part),t in raw.items():
 if L=='fr':
  commands.update(re.findall(r'\\(?:[cdefgs][A-Z]|dmu|aut|br|cl|cosp|dv|Div|ext|Ext|gal|gl|gr|h|hh|Hom|hom|im|ob|pgl|pic|res|rHom|rhom|sh|spe|spec|swan|tor|Tor|tr|an|const|et|iso|lotimes|kloos|pr|varinjlim|varprojlim)\b',t))
for cmd in sorted(commands):
 n=0;first=None
 for part,owner,ff,ef in SOURCES:
  t=raw['en',part]
  for m in re.finditer(re.escape(cmd)+r'(?![A-Za-z])',t):
   ps=re.findall(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',t[:m.start()]);p=ps[-1] if ps else None
   if p:
    n+=1
    if first is None:first=part+'; printed p. '+p
 if n:rows.append(dict(french_term_or_notation=cmd,english_rendering=cmd,count=n,first_place=first,method='unchanged named mathematical command; corrected text; exact command occurrences',reference='Miller notation retained unless the print requires a distinction'))

rows.sort(key=lambda r:(termnorm(r['french_term_or_notation']),termnorm(r['english_rendering'])))
with (B/'GLOSSARY_SGA4HALF_FR_EN.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['french_term_or_notation','english_rendering','count','first_place','method','reference'],delimiter='\t');w.writeheader();w.writerows(rows)
(B/'attestations.json').write_text(json.dumps(attest,ensure_ascii=False,indent=2))
with (B/'GLOSSARY_ATTESTATIONS.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['fr','en','page','context'],delimiter='\t');w.writeheader();w.writerows(attest)
byfr=collections.defaultdict(list)
for r in rows:
 if not r['french_term_or_notation'].startswith('\\'):byfr[termnorm(r['french_term_or_notation'])].append(r)
mult={k:v for k,v in byfr.items() if len(v)>1}
(B/'multiple_renderings.json').write_text(json.dumps(mult,ensure_ascii=False,indent=2))
summary=dict(pages={L:len([p for l,p in pages if l==L]) for L in ['fr','en']},glossary_rows=len(rows),term_rows=sum(not r['french_term_or_notation'].startswith('\\') for r in rows),notation_rows=sum(r['french_term_or_notation'].startswith('\\') for r in rows),multi_rendering_terms=len(mult),reviewed_emphasis_candidates=len(review))
summary.update(unique_french_terms=len(byfr),english_attestations=len(attest),emphasis_spans=len(census),input_hashes=input_hashes)
(B/'STATUS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary))
