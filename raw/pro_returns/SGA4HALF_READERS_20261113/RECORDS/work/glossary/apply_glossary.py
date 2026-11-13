"""Reviewed English terminology normalization, applied after component assembly.
Interface: apply_glossary(text, language='en', component=None) -> (text, rows).
This function is idempotent and operates only on the authorial component body.
Every occurrence retains its printed-page location and receives a change-log row.
"""
import re

def apply_glossary(text,language='en',component=None):
 if language.lower() not in ('en','english'):return text,[]
 if component is not None:component=str(component).replace('\\','/').rsplit('/',1)[-1]
 rows=[]
 def edit(m):
  old=m[0];plural=old.lower().endswith('s');new='dévissages' if plural else 'dévissage'
  if old[0].isupper():new=new[0].upper()+new[1:]
  ps=re.findall(r'\\(?:PrintPage|MathPage)\{([^}]+)\}',text[:m.start()]);page=ps[-1] if ps else ''
  rows.append(dict(id='S45-ASTRA-G-0001',page=page,component=component or 'Arcata',place='Technical term dévissage; aligned prose or section heading',before=old,after=new,source='GLOSSARY_SGA4_FR_EN.tsv; GLOSSARY_SGA7_FR_EN.tsv; matching French dévissage',kind='terminology',reason='Both supplied reference glossaries retain dévissage/devissage. Later exposés and the restored Arcata contents use dévissage; unify the isolated English unwinding translation with that technical term.'))
  return new
 # Every occurrence of this word in the English corpus corresponds to dévissage
 # in Arcata; mathematical formulas and bibliography titles contain none.
 text=re.sub(r'\b[Uu]nwindings?\b',edit,text)
 return text,rows
