"""Corpus glossary with literal counts, exact first-occurrence offsets and source references."""
from pathlib import Path
import re,json,csv,bisect,collections
import prepare_english as p
from editorial_note_relocation import mask_editorial_note
OUT=Path(__file__).parent
DEC=Path('work/contributions/decisions')

def view(s,start,end):
 # Search view only: remove TeX command names and grouping, retain their
 # textual arguments, and map every remaining character to its source offset.
 clean=p.uncomment(s)
 masked=list(clean[start:end])
 for m in re.finditer(r'\\(?:[A-Za-z@]+|.)',clean[start:end],re.S):
  for j in range(m.start(),m.end()):masked[j]=' '
 chars=[];positions=[];space=False
 for j,c in enumerate(masked):
  if c in '{}':continue
  if c.isspace() or c=='~':
   if not space:chars.append(' ');positions.append(start+j)
   space=True
  else:chars.append(c);positions.append(start+j);space=False
 return ''.join(chars),positions

def hits(v,positions,term):
 pattern=r'(?<![\w-])'+re.escape(term).replace(r'\ ',r'\s+')+r'(?![\w-])'
 return [(positions[m.start()],m[0]) for m in re.finditer(pattern,v,re.I)]

def main():
 en=(OUT/'EN_corrected_flat.tex').read_text();fr=Path('work/sources/SGA5_FR/fr/sga5/current/s5.tex').read_text()
 ea=en.index(r'\phantomsection\addcontentsline{toc}{section}{Exposé I ---');eb=en.index(r'\section*{Terminological Index}')
 fps=p.getpages(fr);fa=fps[1]['start'];fb=fps[481]['start']
 ev,ep=view(mask_editorial_note(en),ea,eb);fv,fp=view(fr,fa,fb)
 folios=list(fps);fstarts=[x['start'] for x in fps.values()]
 def ffolio(pos):return folios[max(0,bisect.bisect_right(fstarts,pos)-1)]
 align=json.loads((OUT/'EN_ALIGNMENT.json').read_text());astarts=[r['position_corrected'] for r in align]
 headings=[r for r in align if 'anchor' in r and ('section' in r['kind'] or 'statement' in r['kind'] or r['kind'] in ['expose','index'])]
 hstarts=[r['position_corrected'] for r in headings]
 def place(pos):
  j=max(0,bisect.bisect_right(astarts,pos)-1);prev=align[j];nxt=align[min(j+1,len(align)-1)]
  page=str(prev['folio']) if prev['folio']==nxt['folio'] or prev['position_corrected']==pos else str(prev['folio'])+'–'+str(nxt['folio'])
  h=headings[max(0,bisect.bisect_right(hstarts,pos)-1)]
  anchor=re.sub(r'\s+',' ',h['anchor'])
  return f"{p.expose(prev['folio'])}; {anchor}; printed folio {page}"
 inventory=json.loads((DEC/'body_terminology_inventory.json').read_text())
 additions=[
  ('fibre',['fibre','fibres'],['fibre','fibres','fiber','fibers']),
  ('AR-nul',['AR-nul','AR-nuls'],['AR-null','AR-zero']),
  ('voisinage',['voisinage','voisinages'],['neighbourhood','neighbourhoods','neighborhood','neighborhoods']),
  ('annulé',['annulé','annulée','annulés','annulées'],['annihilated','killed']),
  ('formule',['formule','formules'],['formula','formulae','formulas']),
  ('catégorie fibrée',['catégorie fibrée','catégories fibrées'],['fibred category','fibred categories']),
  ('catégorie cofibrée',['catégorie cofibrée','catégories cofibrées'],['cofibred category','cofibred categories']),
  ('flasque',['flasque','flasques'],['flasque','flabby']),
  ('quasi-compact',['quasi-compact','quasi-compacte','quasi-compacts','quasi-compactes'],['quasi-compact','quasicompact']),
 ]
 for i,(term,fs,es) in enumerate(additions,1):inventory.append({'id':f'BODY-EXTRA-{i:03d}','French_term':term,'French_search_forms':fs,'English_search_forms':es})
 additions_path=OUT/'GLOSSARY_ADDITIONS.json'
 audited_additions=json.loads(additions_path.read_text()) if additions_path.exists() else []
 inventory.extend(audited_additions)
 coordinate_path=OUT/'GLOSSARY_COORDINATED_CATEGORY_EVIDENCE.json'
 coordinate=json.loads(coordinate_path.read_text()) if coordinate_path.exists() else None
 if coordinate:
  inventory=[coordinate if r['id']==coordinate['id'] else r for r in inventory]
 for r in inventory:
  if r['French_term']=='produit fibré':r['English_search_forms']+=['fibred product','fibred products','fibre products']
  if r['French_term']=='borné à gauche':r['English_search_forms']+=['left-bounded','bounded on the left']
  if r['French_term']=='fonction centrale':r['English_search_forms']+=['class function','class functions']
  if coordinate and r['French_term']=='catégorie fibrée':
   r['French_search_forms']+=['catégories fibrées et cofibrées','catégories fibrées ou cofibrées','catégorie fibrée et cofibrée']
   r['English_search_forms']+=['fibred and cofibred category','fibred and cofibred categories','fibred or cofibred categories']
 rows=[];families=[];occurrences=[]
 for term in inventory:
  focc=sorted(set(q for form in term['French_search_forms'] for q in hits(fv,fp,form)))
  if not focc:continue
  observed=[]
  for form in dict.fromkeys(term['English_search_forms']):
   occ=hits(ev,ep,form)
   if not occ:continue
   observed.append({'form':form,'count':len(occ),'first_place':place(occ[0][0]),'first_offset':occ[0][0],'case_forms':dict(collections.Counter(q[1] for q in occ))})
   rid=term['id']+'-'+str(len(observed)).zfill(2)
   rows.append({'French term or notation':term['French_term'],'English rendering':form,'count':len(occ),'first place':place(occ[0][0]),'kind':'body term','count scope':'literal English phrase in exposés, including their bibliographies; command names and indexes excluded','French count':len(focc),'first French place':f'{p.expose(ffolio(focc[0][0]))}; printed folio {ffolio(focc[0][0])}','references':'','source id':rid,'source':'fr/sga5/current/s5.tex;en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex;EN_ALIGNMENT.tsv'})
   occurrences.append({'id':rid,'French_term':term['French_term'],'English_rendering':form,'count':len(occ),'positions_corrected':[x[0] for x in occ],'first_context':en[max(ea,occ[0][0]-100):occ[0][0]+len(form)+150]})
  if observed:families.append({'id':term['id'],'French_term':term['French_term'],'English_forms':observed,'French_count':len(focc),'first_French_folio':ffolio(focc[0][0])})
 pairs=json.loads((DEC/'index_glossary_pairs.json').read_text())
 for pair in pairs:
  label=pair['English_rendering'];poss=[m.start() for m in re.finditer(re.escape(label),en[ea:])]
  poss=[ea+x for x in poss]
  assert poss,(pair['id'],label)
  rows.append({'French term or notation':pair['French_term_or_notation'],'English rendering':label,'count':len(poss),'first place':place(poss[0]),'kind':'index '+pair['kind'],'count scope':'exact complete index-label TeX string in exposés and indexes; aliases not combined','French count':fr[fa:].count(pair['French_term_or_notation']),'first French place':f"Index; printed folio {pair['index_folio']}",'references':pair['English_references'],'source id':pair['id'],'source':'fr/sga5/current/s5.tex:Index;en/ported_source/sources/native/SGA5/SGA5_English_sync_workpass.tex:Index'})
 fields=['French term or notation','English rendering','count','first place','kind','count scope','French count','first French place','references','source id','source']
 with (OUT/'GLOSSARY_SGA5_FR_EN.tsv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
 (OUT/'GLOSSARY_FAMILIES.json').write_text(json.dumps(families,ensure_ascii=False,indent=2))
 (OUT/'GLOSSARY_OCCURRENCES.json').write_text(json.dumps(occurrences,ensure_ascii=False,indent=2))
 corrected=json.loads((OUT/'EN_common_corrections.json').read_text());fixes=[r for r in corrected if r['id'].startswith('GLOSSARY-')]
 def esc(s):return s.replace('|',r'\|').replace('\n',' ')
 lines=['# English terminology and variations','',
  'The glossary combines all 108 paired entries of the printed terminology and notation indexes with an independently counted body vocabulary. Each index pair is checked against its exposé/section references. Body rows state the literal English phrase counted; inflections have separate rows. The complete list of multiple observed forms in this audited vocabulary appears below, including ordinary plurals so that no observed variation is hidden.','',
  'Counts cover the corrected English from Exposé I through Exposé XV, including the exposés’ bibliographies. TeX command names, comments, front matter, indexes, and the inherited English editorial footnote relocated to the unresolved appendix are excluded from body-term counts. Thus a diagram command such as `\\arrow` contributes no occurrence of the English word “arrow”. Formatting wrappers and whitespace are ignored only in the search view, with every occurrence mapped back to its exact source offset. Nested terms have independent counts: “tensor product” can also occur within “external tensor product”. The counts measure the stated English phrase, including its uses outside the French headword’s immediate contexts; they are not asserted to be word-alignment frequencies. Index rows instead count their complete exact TeX label string and explicitly say so.','',
  'A first place is an English heading and a printed-folio anchor or bounding range. A range records the two exact neighbouring folio anchors; no interpolated folio is claimed. `GLOSSARY_OCCURRENCES.json` retains all English source offsets and first-occurrence context, and `EN_ALIGNMENT.tsv` supplies the folio evidence.','',
  '## Spelling repairs applied in all English forms','',
  '| Decision | Earlier spelling | Current spelling | Replacements | Source place and reason |','|---|---|---|---:|---|']
 for r in fixes:lines.append('| '+esc(r['id'])+' | `'+esc(r['old'])+'` | `'+esc(r['new'])+'` | '+str(r['applied_count'])+' | '+esc(str(r['page'])+'; '+r['reason'])+' |')
 lines+=['','## Source-based translation repairs','',
  '| French term | Earlier English | Reading retained | Place / decision | Reason |','|---|---|---|---|---|']
 for r in json.loads((DEC/'SOL_glossary_variants.json').read_text()):
  lines.append('| '+esc(r['French_term'])+' | '+esc(r['earlier_English'])+' | '+esc(r['selected_English'])+' | '+esc(str(r['folio'])+'; '+r['source_id'])+' | '+esc(r['disposition'])+' |')
 lines+=['','The internal-derived-Hom audit extends the cited SOL repairs to the complete Exposé III / III B corpus. Its 433 one-to-one formula occurrences carry the exact French token, its scoped expansion, both French formula contexts and the English context. The two plain `R Hom_{Λ[G]}(Q,Q)` factors on pp. 201–202 are retained. The source’s corrected internal-Hom forms are supplied in the remaining matched places, with the two printed missing underlines on pp. 93 and 126 retained diplomatically. See `EN_INTERNAL_HOM_AUDIT.tsv`.','',
  '## Every observed multiple form in the audited body vocabulary','',
  '| French term | English forms and counts | First places | Disposition |','|---|---|---|---|']
 dispositions={
  'image directe':'Retain noun and adjective syntax: direct image / direct-image. The formula and its f_* or f_! notation remain explicit at each place.',
  'image inverse':'Retain the ported noun, adjective and pullback wording. The cited f^* construction determines the morphism at each place; the literal phrase totals are kept separate.',
  'produit tensoriel':'Retain tensor product as a noun and tensor-product in compounds; every ordinary or derived tensor symbol remains as stated.',
  'produit tensoriel externe':'Retain the grammatical noun/compound forms and plural inflection.',
  'produit fibré':'Retain fibre product and fibred product; the source explicitly gives each product over its indicated base, such as X ×_S Y. No base or product morphism is changed.',
  'changement de base':'Retain base change as a noun and base-change in compounds; the corresponding Cartesian square or cited base-change morphism is preserved.',
  'flèche':'Retain arrow, map and morphism in their supplied contexts. Their corpus totals include uses translating other French words; the row does not identify all those uses with flèche.',
  "flèche d'adjonction":'Retain the phrasing attached to the displayed adjunction arrow, for example f^*f_* → 1 or 1 → f_*f^*. No unit/counit direction is changed.',
  'de présentation finie':'Retain predicative of finite presentation and adjectival finitely presented in their given module/morphism contexts.',
  'de type fini':'Retain predicative of finite type and adjectival finite-type; no hypotheses are altered.',
  'borné à droite':'Retain the source’s phrases for complexes with components vanishing above a bound. The corresponding D^- notation and degree conventions are unchanged.',
  'borné à gauche':'Retain the source’s phrases for complexes with components vanishing below a bound. The corresponding D^+ notation and degree conventions are unchanged.',
  'sommets':'The specific mistranslation sums of this square is repaired to vertices. Other sums refer to the separately stated addition operations and are not altered.',
  'conjuguer':'The two source deductions combining formulas are repaired. Conjugation expressions in their group/action contexts are retained; the literal forms are counted separately.',
  'annulé':'Retain annihilated and killed with the stated annihilating integer or ideal; the assertion that its multiplication action is zero remains the same.',
  'formule':'Retain singular formula and the supplied plural spellings formulae / formulas, including titles and bibliographic wording.',
 }
 multi=[r for r in families if len(r['English_forms'])>1]
 for r in multi:
  forms='; '.join(x['form']+' ('+str(x['count'])+')' for x in r['English_forms'])
  places='; '.join(x['form']+': '+x['first_place'] for x in r['English_forms'])
  disp=dispositions.get(r['French_term'],'Retain the attested singular/plural forms and contextual wording, with separate literal counts.')
  lines.append('| '+esc(r['French_term'])+' | '+esc(forms)+' | '+esc(places)+' | '+esc(disp)+' |')
 lines+=['','## Index and notation checks','',
  'All 56 terminology entries and 52 notation entries have a paired English entry in the same order. Their references agree after the stated translation of “déf.” and “n°” labels, including the source corrections from XIV to XV and the rationality-theorem section correction. The glossary retains the exact supplied corrected French index labels in its French column and the corrected English labels in its English column. The exact TeX records the author’s ordinary Hom, internal Hom, derived Hom, Γ^G and underlined Γ^G at the specified source places. The 32 scanned RΓ sites have their separate decisions and are not counted as lexical inconsistencies.','',
  f'Catalogue totals: {len(rows)} rows; {len(families)} body term families; 108 verified index pairs; {len(multi)} body families with more than one observed English form. The body family inventory and all occurrence counts are reproducible by `build_glossary.py`.','']
 if audited_additions:
  lines+=['## Final coverage audit additions','',
   'The original 303-row glossary was checked against every paired index entry and every observed form in its 117 body families. Thirteen further phrase families were then added from exact paired passages. Their shared formulas, section references, source offsets and unmodified bilingual contexts are retained in `GLOSSARY_ADDITIONS.json`. The single literal “pullback” occurrence in the inherited p.43 editorial footnote was excluded when that complete note was relocated to the apparatus, as recorded by EN-INHERITED-0046-P43. No authorial-body change accompanies the glossary additions.','',
   '| French phrase | Attested English search forms | Exact paired locus |','|---|---|---|']
  for r in audited_additions:
   obs=next(x for x in families if x['id']==r['id'])
   lines.append('| '+esc(r['French_term'])+' | '+esc('; '.join(x['form']+' ('+str(x['count'])+')' for x in obs['English_forms']))+' | '+esc(r['paired_evidence']['alignment_basis'])+' |')
  lines+=['',
   'The earlier cofibred-category candidate had no occurrence of the contiguous French search phrase. Inspection recovered the exact coordinated phrases “catégories fibrées et cofibrées”, “catégories fibrées ou cofibrées” and “catégorie fibrée et cofibrée”, with their paired English wording. These complete strings are now explicit search forms; the cofibred family and coordinated alternatives in the fibred family are counted. `GLOSSARY_COORDINATED_CATEGORY_EVIDENCE.json` records the paired passage.','',
   'The other ten initially excluded curated phrase families have zero literal occurrences for all their listed French and English forms in the declared body scope. The audit records each tested form and zero count; it does not infer a missing body term from an unattested candidate. The full 108-entry index remains covered separately. See `GLOSSARY_COVERAGE_AUDIT.json` and `GLOSSARY_COVERAGE_AUDIT.md`.','']
 (OUT/'GLOSSARY_INCONSISTENCIES.md').write_text('\n'.join(lines))
 summary={'rows':len(rows),'body_term_families':len(families),'body_rendering_rows':len(rows)-108,'index_pairs':108,'multiple_form_families':len(multi),'lexical_repair_operations':len(fixes),'lexical_replacements':sum(r['applied_count'] for r in fixes)}
 (OUT/'GLOSSARY_SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))

if __name__=='__main__':main()
