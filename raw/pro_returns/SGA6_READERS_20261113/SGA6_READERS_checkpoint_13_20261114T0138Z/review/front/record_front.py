#!/usr/bin/env python3
"""Record the coordinator's direct visual collation of the front matter.

Evidence images were actually viewed before these decisions were entered.
This script reproduces the records and exact patches; it performs no OCR verdicts.
"""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
rows=[]
patches=[]

def decision(id,page,where,printed,corrected,reason,region,kind='misprint',status='confirmed',source_id=None):
    pdf={'V':7,'VII':9,'VIII':10,'IX':11,'XI':13,'XII':14}.get(page)
    witness={'V':5,'VII':7,'VIII':8,'IX':9,'XI':10,'XII':11}.get(page)
    rows.append({'source_id':source_id or id,'id':id,'type':kind,'page':page,'where':where,'verdict':status,
      'printed_reading':printed,'correction':corrected,
      'image':f'scan/SGA6_scan_360dpi.pdf#page={pdf}; scan/SGA6_witness_300dpi.djvu#page={witness}',
      'region':region,'change':corrected,'forms':'FR diplomatic preserves print; FR corrected/apparatus and reading use correction' if kind=='misprint' else 'all FR forms; EN where applicable',
      'reason':reason})

def patch(id,layer,old,new,reason):
    patches.append({'source_id':id,'page':'front','layer':layer,'old':old,'new':new,'reason':reason})

decision('ASTRA-FM-001','V','Preface, second paragraph','régigé','rédigé',
 'The main scan and witness both print régigé; the verb is rédiger. Keep the inherited diplomatic reading and the existing corrected reading.',
 'second paragraph, line containing «n’a pas été régigé»')
decision('ASTRA-FM-002','VII','Introduction, second paragraph, last line','extrêment','extrêmement',
 'The witness clearly shows extrêment, with the medial me absent. The corrected adverb is extrêmement. Existing layer difference is justified.',
 'second paragraph, last line')
decision('ASTRA-FM-003','VII','Introduction, third paragraph','coéfficients','coefficients',
 'Both scans show the acute accent in coéfficients. The French noun coefficients has no acute accent. Existing layer difference is justified.',
 'third paragraph, line with «coéfficients discrets»')
for suffix,place in [('a','third paragraph, first occurrence'),('b','third paragraph, occurrence before «notamment»')]:
    decision('ASTRA-FM-004'+suffix,'VII',place,'Algèbrique','Algébrique',
      'The printed grave accent is visible in the witness; correct the accent in algébrique. The diplomatic layer retains the printed accent.',
      place)
decision('ASTRA-FM-005','VIII','Introduction, first paragraph','Algèbrique','Algébrique',
 'The grave accent is clear in both scans in «Géométrie Algèbrique». This occurrence was left unchanged in the attached current layer; correct the spelling.',
 'first paragraph, line before «parvenir à une démonstration»',status='not applied and now applied')
patch('ASTRA-FM-005','current','aussi en Géométrie Algèbrique pour parvenir','aussi en Géométrie Algébrique pour parvenir','Correct the scan-confirmed grave accent.')
decision('ASTRA-FM-006','VIII','Introduction, second paragraph','inflence','influence',
 'Both scans print inflence, missing u in influence. Both attached layers retain it; add u only in the corrected layer.',
 'second paragraph, line with «une inflence évidente»',status='not applied and now applied')
patch('ASTRA-FM-006','current','une inflence évidente','une influence évidente','Correct the missing u in the printed word.')
decision('ASTRA-FM-007','VIII','Introduction, end of second paragraph','exposés cites','exposés cités',
 'The scan and witness show cites without an acute accent. The past participle modifying exposés is cités.',
 'second paragraph, last two lines',status='not applied and now applied')
patch('ASTRA-FM-007','current','les exposés cites de Serre','les exposés cités de Serre','Restore the acute accent in the past participle.')
decision('ASTRA-FM-008','VIII','Introduction, Serre reference','Lectures Notes in Mathematics','Lecture Notes in Mathematics',
 'Both scans print Lectures Notes. The series title is printed as Lecture Notes in Mathematics on the original title page (main PDF3; witness1). Remove the spurious s in the corrected reference.',
 'second paragraph, parenthesis beginning «Lectures Notes»',status='not applied and now applied')
patch('ASTRA-FM-008','current','(Lectures Notes in Mathematics','(Lecture Notes in Mathematics','Use the series title as printed on the volume title page.')
decision('ASTRA-FM-009','XI','Contents, Exposé VI title','Fibre Projectif','Fibré Projectif',
 'The contents page visibly prints Fibre without an accent; the term is fibré projectif and the corrected layer already supplies the accent. Retain the printed title diplomatically.',
 'last contents entry, title line')
for id,page,old,new,region in [
 ('ASTRA-FM-010','IX',r"de l'anneau $K^\circ$",r"de l'anneau $K^{\bullet}$",'second paragraph, line mentioning VI 1.1'),
 ('ASTRA-FM-011','XI',r'Le $K^\circ$',r'Le $K^{\bullet}$','Exposé VI contents title'),
 ('ASTRA-FM-012','XII',r'Calcul du $K^\circ$',r'Calcul du $K^{\bullet}$','Exposé VII contents title')]:
    decision(id,page,region,r'K^{\bullet}',r'K^{\bullet}',
      'The exponent is a solid raised dot in the main scan and witness. The attached front matter encodes an open circle. Use a raised-dot glyph in both layers, preserving the printed distinction.',
      region,kind='own_finding',status='amended')
    patch(id,'both',old,new,'Replace an open-circle transcription by the solid raised dot visible in the print.')
decision('ASTRA-FM-013','XII','Contents, Exposé IX title',r'Quelques Calculs de Groupes K.',r'Quelques Calculs de Groupes $K$.',
 'The witness shows the dot on the baseline after K, aligned with terminal punctuation, with no subscript attached to K. The attached front matter adds a lower degree dot. Transcribe the printed full stop.',
 'Exposé IX contents title',kind='own_finding',status='amended')
patch('ASTRA-FM-013','both',r'Quelques Calculs de Groupes $K_\bullet$'+"\\\\",r'Quelques Calculs de Groupes $K$.'+"\\\\",'Transcribe the visible baseline full stop, removing the unsupported subscript dot.')
for id,title,page in [('ASTRA-FM-014','Préface','V'),('ASTRA-FM-015','Introduction','VII'),('ASTRA-FM-016','Table des matières','XI')]:
    decision(id,page,'heading',title+' (underlined)',title+' (underlined)',
      'The heading word has a single printed underline. Preserve that visible emphasis in the diplomatic and corrected headings.',
      'top heading',kind='convention',status='amended')
    patch(id,'both','\\section*{'+title+'}','\\section*{\\underline{'+title+'}}','Keep the printed single underline on this front-matter heading.')

# Bind every applicable HOLD row to directly inspected front matter.
holds=json.loads((ROOT/'fr/codex/HOLD_VS_CORR.json').read_text())
for i,h in enumerate(holds,1):
    if h['corr_lines'][0]>=170:
        continue
    s='\n'.join(h['corr'])
    linked=[]
    for needle,ids in [('rédigé',['ASTRA-FM-001']),('extrêmement',['ASTRA-FM-002']),('coéfficients',['ASTRA-FM-003']),('coefficients',['ASTRA-FM-003','ASTRA-FM-004a','ASTRA-FM-004b']),('Fibré',['ASTRA-FM-009'])]:
        if needle in s:
            linked.extend(ids)
    if linked:
        rows.append({'source_id':f'fr/codex/HOLD_VS_CORR.json#{i}','type':'hold_difference','page':'front',
          'verdict':'confirmed','printed_reading':'See '+', '.join(dict.fromkeys(linked)),
          'image':'scan/SGA6_scan_360dpi.pdf#pages=7,9,13; scan/SGA6_witness_300dpi.djvu#pages=5,7,10',
          'region':'the word-level locations in the linked decisions','change':'Retain the corrected readings and the separate diplomatic spellings.',
          'forms':'FR corrected and reading','reason':'The front-matter difference is an attested printed spelling corrected by '+', '.join(dict.fromkeys(linked))+'.'})

HERE.mkdir(exist_ok=True)
def jsonl(name,data):
    (HERE/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
jsonl('decisions.jsonl',rows)
jsonl('patches.jsonl',patches)
page_rows=[]
for pdf,folio,witness in [(1,'cover',None),(3,'I',1),(4,'II',2),(5,'III',3),(6,'IV',4),(7,'V',5),(8,'VI',6),(9,'VII',7),(10,'VIII',8),(11,'IX',9),(12,'X',None),(13,'XI',10),(14,'XII',11)]:
    blank=pdf in [6,8,12]
    # Cover/title/colophon have been read but are only complete after the
    # independent transcription file is produced and compared.
    complete=pdf in [1,3,4,5,6,7,8,9,10,11,12,13,14]
    page_rows.append({'page':folio,'pdf_page':pdf,'witness_page':witness,'checked':complete,
      'status':'fully compared' if complete and not blank else 'blank page inspected' if blank else 'image read; transcription integration pending',
      'image':f'scan/SGA6_scan_360dpi.pdf#page={pdf}',
      'region':'whole printed text, with overlapping strips at 194.4 dpi; witness at 300 dpi where cited',
      'reason':'Blank verso: visible marks are show-through from the reverse.' if blank else 'Direct visual comparison with both French source layers; page breaks and listed differences recorded.',
      'starts':{1:'Lecture Notes in Mathematics',3:'Lecture Notes in Mathematics',4:'AMS Subject Classifications (1970)',5:'SEMINAIRE DE GEOMETRIE ALGEBRIQUE DU BOIS MARIE',7:'PREFACE',9:'INTRODUCTION',10:'plexe du théorème de Riemann-Roch',11:"d'un morphisme projectif d'espaces analytiques complexes",13:'TABLE DES MATIERES',14:'EXPOSE VII'}.get(pdf,'')})
page_rows.insert(1,{'page':'cover-verso','pdf_page':2,'witness_page':None,'checked':False,'status':'partly obscured; unresolved',
 'image':'scan/SGA6_scan_360dpi.pdf#page=2','region':'whole page; upper publisher notice covered by a physical library label',
 'reason':'The witness starts at the title page and supplies no inside-cover counterpart. Do not invent the obscured words.'})
jsonl('page_status.jsonl',page_rows)
print(json.dumps({'decisions':len(rows),'patches':len(patches),'fully_compared_front_pages':sum(p['checked'] for p in page_rows)},ensure_ascii=False))
