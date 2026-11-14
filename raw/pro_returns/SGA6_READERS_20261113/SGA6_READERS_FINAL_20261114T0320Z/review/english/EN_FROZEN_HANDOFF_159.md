# English through159 snapshot handoff

The English source and records are stable for the next checkpoint copy.
Fresh reconstruction covers printed1–159 (Exposé0 and the complete ExposéI),
with38 accepted translation records and110 exact source variants. The current
comparison has5,013 literal mathematical units,33 approved paired nonidentical
occurrences and zero unexpected differences. Both ExposéI source branches pass
against their exact French references; each has15 approved lexical paired
occurrences and zero unexpected differences. The scoped glossary has171 rows.

The existing live PDFs still correspond to through150 and109 variants. All four
completed two passes, but their subsequent visual inspection found redundant
Cart rules142–144 and apparatus macro drift. Both source repairs are implemented.
The macro-state helper also passed the complete checkpoint04 through140 builds
and direct apparatus98 inspection. The through159 snapshot must be regenerated,
compiled and regionally inspected before claiming those repairs in its PDFs.

Commands from the snapshot work directory:

```sh
python review/english/build_english_candidates.py
python review/english/verify_reviewed_english.py
python review/english/verify_expose_i_forms.py
python review/english/compile_candidates.py
python review/english/make_alignment_hints.py
python review/english/refresh_work_summary.py
```

Required regional checks after this build: all twelve Cart occurrences142–144,
apparatus108 and110 with their body-time macro meanings, the new evaluation/trace
passage151–159 including the two157 tensor readings, and the final reading-form
margin warnings. The prior frozen handoffs and snapshots remain historical.
The inherited body beginning160 remains unreviewed English. Volume-wide front
matter, glossary decisions and full PDF inspection are unfinished.
