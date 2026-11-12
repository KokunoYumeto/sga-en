"""Audit the eight generated sources' credits, rights and editorial coverage.

This is a source/content audit. PDF rendering and the complete body/fix audits
are recorded separately. No paths from the execution environment enter the
audit output.
"""
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / 'output/records'
spec = importlib.util.spec_from_file_location('editorial_render', ROOT / 'build/editorial_decisions.py')
editorial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editorial)

HUMANS = [
    'Alexander Grothendieck', 'Michèle Raynaud', 'Michel Raynaud', 'Pierre Deligne',
    'Nicholas Katz', 'Michel Demazure', 'Michael Artin', 'Jean-Louis Verdier',
    'Luc Illusie', 'Bas Edixhoven', 'Yves Laszlo', 'L. Bayle', 'N. Borne',
    'O. Brinon', 'J. Buresi', 'M. Chardin', 'F. Ducrot', 'P. Graftiaux',
    'F. Han', 'P. Karwasz', 'L. Koelblen', 'D. Madore', 'S. Morel', 'D. Naie',
    'B. Osserman', 'J. Riou', 'V. Sécherre', 'C. Sabbah', 'Jacob C. Reinhold',
    'Philippe Gille', 'Patrick Polo', 'Fabrice Orgogozo', 'Daniel Miller',
]
MANDATORY = ['AI-transcribed', 'AI-translated', 'AI-produced corrections',
             'GPT-6 Astra (OpenAI, ChatGPT Pro mode)']
RIGHTS_EN = (
    "The rights in the original work belong to its author or the author's representatives or heirs. "
    'Where we hold rights, in the AI-produced transcription, translation, corrections and typesetting, '
    'they are dedicated to the public domain under CC0 1.0. This edition is published for educational, '
    'non-profit purposes, and we claim no rights we do not hold. If you hold rights in this work and '
    'object to its publication here, please open a GitHub issue and we will take it down.')
RIGHTS_FR = (
    'Les droits sur l’œuvre originale appartiennent à son auteur ou aux représentants ou héritiers de celui-ci. '
    'Dans la mesure où nous détenons des droits sur la transcription, la traduction, les corrections et la '
    'composition produites par l’intelligence artificielle, nous les dédions au domaine public sous CC0 1.0. '
    'Cette édition est publiée à des fins éducatives et non lucratives, et nous ne revendiquons aucun droit '
    'que nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez à sa publication '
    'ici, veuillez ouvrir un ticket GitHub et nous la retirerons.')

attr = (ROOT / 'sources/en/repo/ATTRIBUTION.md').read_text()
readme = (ROOT / 'sources/en/repo/README.md').read_text()
production = readme[readme.index("Jacob C. Reinhold's English translation"):readme.index('\n## Status')].strip()
source_authority = (ROOT / 'sources/en/repo/SOURCE_AUTHORITY.md').read_text()
numbering = source_authority[source_authority.index('SGA 7 I is complete'):source_authority.index('\n- Published volume:')].strip()
expected = {
    'entire_ATTRIBUTION_wording': editorial.prose_to_tex(attr),
    'README_production_history': editorial.prose_to_tex(production),
    'SGA7I_source_authority': editorial.prose_to_tex(numbering),
}
for volume in ('sga7i', 'sga7ii'):
    expected[volume + '_entire_corpus_README'] = editorial.prose_to_tex(
        (ROOT / 'sources/codex_french_corpus_aug2026' / volume / 'README.md').read_text())
inherited = (ROOT / 'sources/en/evidence/supplemental_working_decisions/sga7i/INHERITED_ENGLISH_PROVENANCE_AND_ADVERSE_USE.md').read_text()
expected['inherited_lineage_caution'] = editorial.prose_to_tex(
    inherited[inherited.index('That service identity'):inherited.index('## Source-alignment findings')].strip())
expected['inherited_adverse_use_disposition'] = editorial.prose_to_tex(
    inherited[inherited.index('This witness is retained unchanged'):].strip())

readers = []
exceptions = []
for p in sorted((ROOT / 'output').glob('*/*.tex')):
    t = p.read_text()
    front = t[t.index(r'\begin{document}'):t.index(r'\tableofcontents')]
    language = p.parent.name
    checks = {key: value in front for key, value in expected.items()}
    checks.update(
        complete_frontmatter_fragment=(ROOT / f'work/frontmatter_{language}.tex').read_text() in front,
        all_33_recorded_human_names=all(name in front for name in HUMANS),
        all_mandatory_AI_and_build_wording=all(word in front for word in MANDATORY),
        rights_statement_exact=editorial.tex(RIGHTS_EN if language == 'en' else RIGHTS_FR) in front,
        both_volume_bibliographic_identity=all(s in front for s in
            ['Alexander Grothendieck', 'D. S. Rim', 'Pierre Deligne', 'Nicholas Katz',
             'Lecture Notes in Mathematics 288', '1972', 'Lecture Notes in Mathematics 340', '1973']),
        inherited_witness_hash_and_size=all(s in front for s in
            ['278,864', 'CFCB4C17081E16F963DCBC3FA04A43C4D4065477CB37BD931233840D287AA2E9']),
        no_prohibited_AI_wording=('AI-' + 'assisted') not in t,
    )
    bad_toc = len(re.findall(r"\\SGAtoc\{Expos'e", t))
    if bad_toc:
        exceptions.append({'file': str(p.relative_to(ROOT / 'output')),
                           'issue': 'Generated English TOC titles use an apostrophe in place of the accented e.',
                           'occurrences': bad_toc})
    for check, ok in checks.items():
        if not ok:
            exceptions.append({'file': str(p.relative_to(ROOT / 'output')), 'issue': check})
    readers.append({'file': str(p.relative_to(ROOT / 'output')),
                    'sha256': hashlib.sha256(t.encode()).hexdigest(), 'checks': checks})

ledger = list(csv.DictReader((RECORDS / 'OPEN_ITEMS_DECIDED.tsv').open(), delimiter='\t'))
data = json.loads((RECORDS / 'editorial_decisions.json').read_text())
notes = data['unresolved_notes']
required_named = ['ED-MANUAL-7I-334', 'ED-7I-356', 'ED-7II-627', 'ED-7II-1018',
                  'ED-en7I-C82', 'ED-en7I-C713', 'ED-en7I-C874', 'ED-en7II-C8',
                  'ED-en7II-C17', 'ED-en7II-C138', 'ED-en7II-C475', 'ED-en7II-C508',
                  'ED-XV-1.3.2-i']
missing_required = sorted(set(required_named) - {r['item'] for r in ledger})
incomplete_rows = [r['item'] for r in ledger if not all(r[k].strip() for k in
                   ['item', 'page', 'readings', 'decision', 'reason', 'forms_affected', 'source', 'status'])]
scan_ids = {r['item'] for r in ledger if r['status'] == 'needs the scan'}
scan_notes = {r['id'] for r in notes if r['status'] == 'needs the scan'}
note_checks = []
for language in ('fr', 'en'):
    fragment = (ROOT / f'work/unresolved_{language}.tex').read_text()
    master = ROOT / ('output/fr/SGA7_FR_master_annote.tex' if language == 'fr'
                     else 'output/en/SGA7_EN_annotated_master.tex')
    t = master.read_text()
    for note in notes:
        retained = editorial.tex(('Retained/source reading: ' if language == 'en'
                                   else 'Lecture de la source conservée : ') + note['printed'])
        alternative = editorial.tex(('Alternative: ' if language == 'en'
                                      else 'Alternative : ') + note['alternative'])
        i = t.index(r'\subsection*{' + editorial.tex(note['id'] + ' — ' + note['page']) + '}')
        conditional = t.rfind(r'\ifnum\SGAform=1', 0, i) > t.rfind(r'\fi', 0, i)
        row = {'id': note['id'], 'language': language, 'status': note['status'],
               'retained_reading_in_fragment': retained in fragment,
               'alternative_in_fragment': alternative in fragment,
               'retained_reading_in_master': retained in t,
               'alternative_in_master': alternative in t,
               'inside_apparatus_form_conditional': conditional}
        note_checks.append(row)
        if not all(row[k] for k in row if k not in ('id', 'language', 'status')):
            exceptions.append({'issue': 'unresolved note presentation', **row})

inventory = list(csv.DictReader((RECORDS / 'FRONT_MATTER_INVENTORY.tsv').open(), delimiter='\t'))
privacy = {'email_matches': [], 'environment_path_matches': []}
email = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]{1,100}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63})+")
local = re.compile(r'/(?:Users|home|root|workspace|tmp|opt|usr|var|mnt|private)/|(?<![A-Za-z])[A-Za-z]:\\(?:Users|Windows|Program Files|Documents|Temp)\\')
for p in sorted((ROOT / 'output').rglob('*')):
    if not p.is_file() or p.suffix not in ('.tex', '.md', '.json', '.tsv', '.log', '.txt') or p.name == 'FRONT_MATTER_AUDIT.json':
        continue
    t = p.read_text(errors='replace')
    counts = {'email_matches': sum(bool(email.search(line)) for line in t.splitlines() if '@' in line),
              'environment_path_matches': len(local.findall(t))}
    for category, count in counts.items():
        if count:
            finding = {'file': str(p.relative_to(ROOT / 'output')), 'occurrences': count}
            privacy[category].append(finding)
            exceptions.append({'issue': category, **finding})

result = {
    'scope': 'Credits, front matter, unresolved-note presentation, named-item completeness, and text-output privacy; body reconstruction and PDF visual checks are separate audits.',
    'reader_and_master_count': len(readers), 'reader_checks': readers,
    'recorded_human_credit_names_count': len(HUMANS), 'recorded_human_credit_names': HUMANS,
    'source_wording_rule': 'All ATTRIBUTION and corpus README prose is present; Markdown link markup and whitespace are converted to TeX without changing their human-credit wording.',
    'decision_count': len(ledger), 'unique_decision_count': len({r['item'] for r in ledger}),
    'named_required_items_count': len(required_named), 'missing_named_items': missing_required,
    'incomplete_decision_rows': incomplete_rows,
    'decision_status_counts': dict(Counter(r['status'] for r in ledger)),
    'unresolved_notes_count': len(notes), 'scan_dependent_decision_count': len(scan_ids),
    'scan_dependent_note_count': len(scan_notes), 'other_retained_note_count': len(notes) - len(scan_notes),
    'scan_decisions_without_both_readings_note': sorted(scan_ids - scan_notes),
    'note_presentation_checks': note_checks,
    'missing_printed_front_matter': [r for r in inventory if r['status'].startswith('not transcribed')],
    'front_matter_inventory_source': 'FRONT_MATTER_INVENTORY.tsv',
    'privacy': privacy, 'exceptions': exceptions,
}
(RECORDS / 'FRONT_MATTER_AUDIT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['reader_and_master_count', 'decision_count',
      'unresolved_notes_count', 'scan_dependent_decision_count', 'other_retained_note_count', 'exceptions']},
      ensure_ascii=False, indent=2))
