"""Flatten one annotated source per language and select the six reader forms."""
from pathlib import Path
import json,re,hashlib,importlib.util
from edition_catalog import *
from edition_tex import prepare_body,preamble
from reader_frontmatter import frontmatter

OUT=ROOT/'deliverables';WORK=ROOT/'work/build'
WORK.mkdir(parents=True,exist_ok=True)
FILENAMES={
 'fr':[(0,0,'SGA4HALF_FR_diplomatique'),(1,0,'SGA4HALF_FR_corrige_apparat'),(2,0,'SGA4HALF_FR_texte_de_lecture'),(1,1,'SGA4HALF_FR_annotated_master')],
 'en':[(0,0,'SGA4HALF_EN_diplomatic'),(1,0,'SGA4HALF_EN_corrected_apparatus'),(2,0,'SGA4HALF_EN_reading'),(1,1,'SGA4HALF_EN_annotated_master')],
}

def conditional_frontmatter(lang):
    return r'\ifcase\EditionMode'+'\n'+frontmatter(lang,0)+'\n'+r'\or'+'\n'+frontmatter(lang,1)+'\n'+r'\or'+'\n'+frontmatter(lang,2)+'\n'+r'\fi'+'\n'

def sanitize_note(lang):
    p=ROOT/('source/fr/codex_dip/sga4.5-note.tex' if lang=='fr' else 'source/en/sources/components/sga4half_note_en.tex')
    s=p.read_text()
    s=re.sub(r'\\section\*\{[^}]*\}',r'\\section*{'+('Note du compositeur Daniel Miller' if lang=='fr' else 'Daniel Miller’s typesetter’s note')+'}',s,count=1)
    # The provided source already redacts the address; retain that redaction.
    s=re.sub(r'[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','[address omitted]',s)
    return r'\ifnum\EditionMode=2\relax\else'+'\n'+s+'\n'+r'\clearpage\fi'+'\n'

summary={};glossary_changes=[];layout_changes=[]
glossary_module=ROOT/'work/glossary/apply_glossary.py'
apply_glossary=None
if glossary_module.exists():
    spec=importlib.util.spec_from_file_location('edition_glossary',glossary_module)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    apply_glossary=module.apply_glossary
for lang in ['fr','en']:
    dest=OUT/lang.upper();dest.mkdir(parents=True,exist_ok=True)
    chunks=[];component_hashes={}
    for c in COMPONENTS:
        source=component_path(c,lang)
        component_hashes[source.relative_to(ROOT).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
        text=source.read_text()
        if apply_glossary:
            text,changes=apply_glossary(text,language=lang,component=c['key']);glossary_changes.extend(changes)
        # Optional, reviewed terminology corrections are applied in a separate,
        # source-anchored stage, never by silently changing the source component.
        patchfile=ROOT/'work/common/glossary_patches.json'
        if lang=='en' and patchfile.exists():
            patches=json.loads(patchfile.read_text())
            if isinstance(patches,dict):patches=patches.get('patches',[])
            for patch in patches:
                if patch.get('component') not in [c['key'],c['en']]:continue
                old,new=patch['old'],patch['new'];expected=patch.get('count',1)
                assert text.count(old)==expected,('glossary count',patch)
                text=text.replace(old,new)
        if c['key']=='erratum' and r'\label{ErratumSGA4}' not in text:
            m=re.search(r'\\chapter\*?\{[^}]+\}',text)
            if m:text=text[:m.end()]+r'\label{ErratumSGA4}'+text[m.end():]
        chunks.append('% BEGIN COMPONENT '+c['key']+'\n'+text+'\n% END COMPONENT '+c['key']+'\n')
        if c['key']=='introduction':chunks.append('% BEGIN ORIGINAL GENERAL CONTENTS\n'+(ROOT/f'work/common/general_contents_{lang}.tex').read_text()+'\n% END ORIGINAL GENERAL CONTENTS\n')
    raw='\n'.join(chunks)
    prepared=prepare_body(raw,lang)
    prepared['input_component_sha256']=component_hashes
    layout_module=ROOT/'work/rapport_cycle/layout_repairs.py'
    if layout_module.exists():
        spec=importlib.util.spec_from_file_location('edition_layout',layout_module)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        prepared['body'],changes=module.apply_layout_repairs(prepared['body'],lang)
        prepared['layout_repairs']=changes;layout_changes.extend(changes)
    assert not prepared['unresolved_citations'],prepared['unresolved_citations']
    assert not re.search(r'\\(?:input|include)\{',prepared['body'])
    (WORK/f'prepared_body_{lang}.tex').write_text(prepared['body'])
    (WORK/f'apparatus_{lang}.tex').write_text(prepared['apparatus'])
    (WORK/f'prepare_report_{lang}.json').write_text(json.dumps({k:v for k,v in prepared.items() if k not in ['body','apparatus']},ensure_ascii=False,indent=2))
    header=preamble(lang,1).replace(r'\providecommand\EditionMode{1}',r'\providecommand\EditionMode{@MODE@}')
    template=header+'\n'+r'\providecommand\EditionIsMaster{@MASTER@}'+'\n'+r'\begin{document}'+'\n'+r'\hypersetup{pageanchor=false}'+'\n'+conditional_frontmatter(lang)+sanitize_note(lang)+r'\clearpage\pagenumbering{arabic}\hypersetup{pageanchor=true}'+'\n'+prepared['body']+'\n'+prepared['apparatus']+'\n'+r'\end{document}'+'\n'
    (WORK/f'master_template_{lang}.tex').write_text(template)
    for mode,master,name in FILENAMES[lang]:
        content=template.replace('@MODE@',str(mode)).replace('@MASTER@',str(master))
        p=dest/(name+'.tex');p.write_text(content)
        summary[name]=dict(language=lang,mode=mode,master=bool(master),tex=p.relative_to(ROOT).as_posix(),
                           sha256=hashlib.sha256(p.read_bytes()).hexdigest(),variant_occurrences=len(prepared['entries']),
                           single_source_template_sha256=hashlib.sha256(template.encode()).hexdigest())
        summary[name]['input_component_sha256']=component_hashes
(WORK/'ASSEMBLY_VALIDATION.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
(WORK/'GLOSSARY_CHANGES_APPLIED.json').write_text(json.dumps(glossary_changes,ensure_ascii=False,indent=2))
(WORK/'LAYOUT_CHANGES_APPLIED.json').write_text(json.dumps(layout_changes,ensure_ascii=False,indent=2))
print(json.dumps({k:{a:v[a] for a in ['mode','master','variant_occurrences']} for k,v in summary.items()},indent=2))
