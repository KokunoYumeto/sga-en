from pathlib import Path
import re,difflib,json
B=Path(__file__).parent

def arg(t,i):
 while t[i].isspace():i+=1
 assert t[i]=='{'; start=i+1; depth=1;i+=1
 while depth:
  if t[i]=='\\':i+=2;continue
  if t[i]=='{':depth+=1
  if t[i]=='}':depth-=1
  i+=1
 return t[start:i-1],i

def select(t,j=1):
 while r'\var{' in t:
  i=t.index(r'\var{');p=i+4;args=[]
  for _ in range(3):a,p=arg(t,p);args.append(a)
  t=t[:i]+args[j]+t[p:]
 return t

def norm(t):
 t=t.replace('\\,','').replace('\\!','').replace('\\;','').replace('\\:','').replace('\\big','').replace('\\Big','')
 t=re.sub(r'\\text(?:normal)?\{[^{}]*\}','TEXT',t)
 return re.sub(r'\s+','',t)
def maths(t):
 return [norm(x.group()) for x in re.finditer(r'(?<!\\)\$[^$]*?(?<!\\)\$|\\\[[\s\S]*?\\\]|\\begin\{(?:equation\*?|align\*?)\}[\s\S]*?\\end\{(?:equation\*?|align\*?)\}',t)]
def getpages(lang):
 f='sga4.5-6.tex' if lang=='fr' else 'sga4half_6_en.tex';s=re.split(r'\\PrintPage\{(\d+)\}\n',select((B/lang/f).read_text()))
 return {int(s[i]):s[i+1] for i in range(1,len(s),2)}
if __name__=='__main__':
 d=[];fr,en=getpages('fr'),getpages('en')
 for p in fr:
  f,e=maths(fr[p]),maths(en[p])
  for tag,a,b,c,k in difflib.SequenceMatcher(None,f,e,autojunk=False).get_opcodes():
   if tag!='equal':d.append(dict(page=p,fr=f[a:b],en=e[c:k]))
 (B/'math_differences.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
 for r in d:print(json.dumps(r,ensure_ascii=False))
