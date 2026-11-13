from pathlib import Path
import json,csv,re
BASE=Path(__file__).parent
SOURCE=BASE.parent.parent/'source'
SOL={r['id']:r for r in csv.DictReader((SOURCE/'check/SOL_FINDINGS.tsv').open(),delimiter='\t') if r['part']=='Sommes trig.'}
def append(name,obj):
 p=BASE/(name+'.jsonl')
 with p.open('a') as f:f.write(json.dumps(obj,ensure_ascii=False)+'\n')
def decide(num,reason,verdict='accepted',printed=None,old=None,new=None,corrected=None,region=None,en='pending alignment'):
 id=f'S45-SOL-{num:04}';r=SOL[id]
 row={'id':id,'printed_page':r['printed_page'],'pdf_page':int(r['pdf_page']),'verdict':verdict,'printed_reading':printed if printed is not None else r['scan_reading'],'image':f"scan/Number32.pdf#page={r['pdf_page']}",'region':region or r['where'],'change_made':new if new is not None else (r['fix_new'] or r['corrected'] or 'No text change'),'forms_affected':'none' if verdict=='rejected' else ('FR corrected and reading; EN where meaning changes' if r['kind']=='misprint_in_print' else 'FR all forms; EN where applicable'),'reason':reason,'kind':r['kind'],'fix_old':old if old is not None else r['fix_old'],'fix_new':new if new is not None else r['fix_new'],'corrected_reading':corrected if corrected is not None else r['corrected'],'codex_ids':[],'english_status':en}
 append('decisions',row)
 return row
def page(p,start_fr,start_en,notes='Full page read directly and compared against its complete TeX span; automatic overlap settled at the stated first word.'):
 append('pages',{'printed_page':str(p),'pdf_page':p+39,'checked_against_scan':True,'findings':sum(r['printed_page']==str(p) for r in SOL.values()),'start_fr':start_fr,'start_en':start_en,'reason':notes})
def own(num,p,place,printed,tex,change,kind,reason):
 id=f'S45-ASTRA-S-{num:04}'
 append('own_findings',{'id':id,'page':str(p),'place':place,'printed_reading':printed,'tex_reading':tex,'change':change,'kind':kind,'reason':reason,'image':f'scan/Number32.pdf#page={p+39}'})
 return id
def edit(p,id,lang,old,new,kind='transcription',context=None):
 append('edits',{'page':str(p),'source':id,'lang':lang,'old':old,'new':new,'kind':kind,'context':context})
def variant(p,id,old,new,reason,en_old=None,en_new=None,place=''):
 append('variants',{'id':id,'source':id,'page':str(p),'place':place,'printed':old,'corrected':new,'reason':reason,'kind':'misprint_in_print','english_applicable':en_old is not None,'en_printed':en_old,'en_corrected':en_new})
 edit(p,id,'fr',old,'\\var{'+old+'}{'+new+'}{'+id+'}',kind='variant')
 if en_old is not None:edit(p,id,'en',en_old,'\\var{'+en_old+'}{'+en_new+'}{'+id+'}',kind='variant')
