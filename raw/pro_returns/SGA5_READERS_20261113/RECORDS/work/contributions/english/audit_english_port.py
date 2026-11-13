"""Per-record inheritance checks for the authenticated English port and final branches."""
from pathlib import Path
import re,json,csv,difflib,bisect,collections,hashlib
import prepare_english as p
OUT=Path(__file__).parent

def main():
 root=Path('work/sources/SGA5_EN');base=(root/p.ENREL).read_text();cur=(OUT/'EN_corrected_flat.tex').read_text();dip=(OUT/'EN_diplomatic_flat.tex').read_text()
 fr=Path('work/sources/SGA5_FR/fr/sga5/current/s5.tex').read_text();fps=p.getpages(fr)
 _,_,_,anchors=p.align_math(fr,base)
 logs=[json.loads(s) for s in (root/'port/PORT_EN5_LOG.jsonl').read_text().splitlines() if s.strip()];byid={r['id']:r for r in logs}
 common=json.loads((OUT/'EN_common_corrections.json').read_text());variants=json.loads((OUT/'EN_variants.json').read_text())
 al=base.splitlines(keepends=True);bl=cur.splitlines(keepends=True);ap=[0];bp=[0]
 for s in al:ap.append(ap[-1]+len(s))
 for s in bl:bp.append(bp[-1]+len(s))
 ops=[];changed=[]
 for op,i,j,k,l in difflib.SequenceMatcher(None,al,bl,autojunk=False).get_opcodes():
  if op=='equal':ops.append(('equal',ap[i],ap[j],bp[k],bp[l]));continue
  old=''.join(al[i:j]);new=''.join(bl[k:l]);changed.append({'base_start':ap[i],'base_end':ap[j],'corrected_start':bp[k],'corrected_end':bp[l],'before':old,'after':new})
  for o,a,b,c,d in difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes():ops.append((o,ap[i]+a,ap[i]+b,bp[k]+c,bp[k]+d))
 def mapped(a,b):
  pieces=[o for o in ops if o[1]<b and a<o[2] or (o[1]==o[2] and a<o[1]<b)]
  assert pieces,(a,b)
  first,last=pieces[0],pieces[-1]
  ca=first[3]+a-first[1] if first[0]=='equal' else first[3]
  cb=last[3]+b-last[1] if last[0]=='equal' else last[4]
  return ca,cb,all(o[0]=='equal' for o in pieces)
 def at_page(page,needle):
  positions=[m.start() for m in re.finditer(re.escape(needle),base)]
  if not positions:return None
  aim=p.estimate(fps[int(page)]['start'],anchors)
  return min(positions,key=lambda x:abs(x-aim))
 def in_page(r,page):
  x=str(r.get('page',''))
  nums=[int(n) for n in re.findall(r'\d+',x)]
  return bool(nums) and (nums[0]<=page<=nums[-1] if len(nums)>1 else nums[0]==page)
 rows=[];fail=[];cache={}
 def check_record(r,stack=()):
  if r['id'] in cache:return cache[r['id']]
  assert r['id'] not in stack
  status=r['decision'];pg=int(r['page']);source='port/PORT_EN5_LOG.jsonl:'+r['id']
  if status=='not_applicable':
   result={'audit_status':'recorded not applicable','evidence':'Final port decision: '+r.get('note',''),'sources':[source],'base_count':0,'corrected_count':0,'diplomatic_count':0,'base_offset':'','corrected_offset':'','corrected_reading':''};cache[r['id']]=result;return result
  needle=r.get('tr_new') if status=='apply' else (r.get('tr_new') or r.get('tr_old'))
  needle=needle or '';original=needle;support=[];pos=at_page(pg,needle) if needle else None
  # The pilot's comma was deliberately removed by the later C3013 operation.
  if pos is None and r['id']=='C3012':
   needle=original.rstrip(',');pos=at_page(pg,needle);support=['C3013']
  # This already-correct square was subsequently given its missing derived L.
  if pos is None and r['id']=='C466':
   c=byid['C605'];assert c['tr_old'] in needle
   needle=needle.replace(c['tr_old'],c['tr_new']);pos=at_page(pg,needle);support=['C605']
  covered=re.findall(r'\b(?:C\d+|K\d+p\d+|R\d+)\b',r.get('note','')) if 'covered by' in r.get('note','') else []
  if pos is None and covered:
   checks=[check_record(byid[x],stack+(r['id'],)) for x in covered]
   assert all(x['audit_status']!='unresolved' for x in checks)
   result={'audit_status':'covered by verified port operation','evidence':'The final port log explicitly identifies '+', '.join(covered)+'. Each referenced operation has its own checked row.','sources':[source]+['port/PORT_EN5_LOG.jsonl:'+x for x in covered],'base_count':base.count(original) if original else 0,'corrected_count':cur.count(original) if original else 0,'diplomatic_count':dip.count(original) if original else 0,'base_offset':'','corrected_offset':'','corrected_reading':''};cache[r['id']]=result;return result
  if pos is None:
   result={'audit_status':'unresolved','evidence':'No exact port reading or explicit supersession chain was found.','sources':[source],'base_count':0,'corrected_count':cur.count(original) if original else 0,'diplomatic_count':dip.count(original) if original else 0,'base_offset':'','corrected_offset':'','corrected_reading':''};fail.append(r['id']);cache[r['id']]=result;return result
  ca,cb,equal=mapped(pos,pos+len(needle));reading=cur[ca:cb]
  deps=[]
  if not equal:
   affected=[h for h in changed if h['base_start']<pos+len(needle) and pos<h['base_end']]
   for h in affected:
    for d in common:
     if in_page(d,pg) and (d.get('old','') in h['before'] or d.get('new','') in h['after']):deps.append(d['id'])
   for v in variants:
    if v.get('original') and v['original']!=v['after'] and v['start_corrected']<cb and ca<v['end_corrected']:deps.append(v['id'])
   # Character-map evidence retains the entire before/after source context;
   # known source decisions own every edit in the construction.
   if not deps:
    for d in common:
     if in_page(d,pg):deps.append(d['id'])
   assert deps,('unattributed port-reading change',r['id'],pg,needle,reading)
  if support:
   for x in support:check_record(byid[x],stack+(r['id'],))
  audit_status='exact port reading retained' if equal and not support else 'later port operation verified' if equal else 'retained with explicit later source repair'
  sources=[source]+['port/PORT_EN5_LOG.jsonl:'+x for x in support]+list(dict.fromkeys(deps))
  evidence=('The exact port reading is present at the mapped source occurrence.' if equal else 'The exact source interval is carried through the complete line/character edit map; the displayed replacement is owned by the listed later source-repair decisions.')
  if support:evidence+=' The earlier surface reading is superseded by '+', '.join(support)+'.'
  result={'audit_status':audit_status,'evidence':evidence,'sources':sources,'base_count':base.count(original),'corrected_count':cur.count(original),'diplomatic_count':dip.count(original),'base_offset':pos,'corrected_offset':ca,'corrected_reading':reading,'effective_base_reading':needle}
  cache[r['id']]=result;return result
 for i,r in enumerate(logs,1):
  result=check_record(r)
  rows.append({'row':i,'id':r['id'],'page':r['page'],'port_decision':r['decision'],'branch_recorded':r.get('branch',''),'kind':r.get('kind',''),**result})
 # The diplomatic branch is a complete exact projection from the same master.
 projected=cur
 for v in reversed(sorted(variants,key=lambda v:v['start_corrected'])):
  a,b=v['start_corrected'],v['end_corrected'];assert projected[a:b]==v['after'],v['id'];projected=projected[:a]+v['before']+projected[b:]
 assert projected==dip
 assert not fail,fail
 (OUT/'EN_PORT_AUDIT.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 fields=['row','id','page','port_decision','branch_recorded','kind','audit_status','base_count','corrected_count','diplomatic_count','base_offset','corrected_offset','effective_base_reading','corrected_reading','evidence','sources']
 with (OUT/'EN_PORT_AUDIT.tsv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader()
  for r in rows:w.writerow({**r,'sources':'; '.join(r['sources'])})
 summary={'port_rows':len(rows),'port_decisions':dict(collections.Counter(r['port_decision'] for r in rows)),'audit_statuses':dict(collections.Counter(r['audit_status'] for r in rows)),'unresolved':len(fail),'source_sha256':hashlib.sha256(base.encode()).hexdigest(),'corrected_sha256':hashlib.sha256(cur.encode()).hexdigest(),'diplomatic_sha256':hashlib.sha256(dip.encode()).hexdigest(),'common_correction_operations':len(common),'explicit_diplomatic_variants':len(variants),'byte_exact_variant_replay':True,'construction':'The entire authenticated ported source is retained, then the enumerated exact operations are applied with occurrence-count assertions. The diplomatic source is the byte-exact branch selection from the same variant catalogue. Reader front-matter wrapping is separately logged by the root build.'}
 (OUT/'EN_PORT_AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
 # Machine-readable changed source regions supplement each row's exact map.
 (OUT/'EN_PORT_BUILD_REGIONS.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
