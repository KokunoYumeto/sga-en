# Final SGA 6 terminology handoff

Status: complete and stable for final assembly. The shared English builder owns the edition sources and receives this packet without any pending terminology repair.

## Deliverables

- `GLOSSARY_SGA6_FR_EN.tsv` — 1078945 bytes; SHA256 `77442fd8bbbb08df59d239c0c232ddcd57445ca7875ec93a0bf0e41adce523ea`.
- `CROSS_VOLUME_TERMS.tsv` — 77578 bytes; SHA256 `f201416f2f001a99d9f23aa9a974c4875a2e7ce875670d736cf060502a3e3bc8`.
- `GLOSSARY_INCONSISTENCIES.md` — 34359 bytes; SHA256 `65f5b00ef52514f3112acaf7790052ef02d54209364764ddfc46bafbdf79b594`.

## Coverage and decisions

The glossary has 1346 rows for 1296 distinct French headword keys. It records 46 admitted headwords with multiple English renderings and 111 cross-volume decisions: 110 retained differences and one resolved prior deviation.

Every one of the 5,134 declared TSV input rows and 26 additional reviewed entries has an explicit disposition. All 234 printed index rows are paired and assigned exactly once, including both ditto rows. Their original definition references and mathematical units are retained. Thirty-four complete reference formula labels receive a separate literal-token census.

The two exact generalization → generization repairs on 648–649 are already applied in the live English source. All 720 live French and English printed-leaf search views agree with this packet’s captured, explicitly patched inventory. The notation ledger records 20 literal red-macro invocations separately from the three literal labels on 545 and one on 597.

Each row states its own count scope. Lexical count means English surface-form occurrences on a leaf co-attesting the complete French search phrase; first_place is the first such leaf in print order. Exact index labels instead count paired index rows. Macro/token rows count literal command uses in their declared folios. These quantities are not added as word totals or asserted as one-to-one semantic translation frequencies.

Every input row and every printed index row has a disposition. This is not an assertion that an arbitrary phrase-extraction procedure has found every possible technical term in the volume. A phrase omitted from the glossary is not asserted absent from the book.

## Reproduction and verification

Captured inputs and their hashes are in INPUT_MANIFEST.json, SUPPLEMENTAL_INPUT_MANIFEST.json and FINAL_MACRO_INPUT_MANIFEST.json. Rebuild in this order: make_terminology_patches.py, lexical_inventory.py, index_inventory.py, finalize_glossary.py, verify_glossary.py, close_packet.py. The input preparation script refuses to overwrite a captured input with changed bytes.

FINAL_VERIFICATION.json records the successful row census, deduplication, exact index assignment, command counts, cross-volume alias equality, applied patch scopes, live corpus comparison and privacy checks. MANIFEST.json lists every packet file except itself, SEAL_RECEIPT.json and Python caches; SEAL_RECEIPT.json gives the manifest digest. No edition source or immutable contribution seal was edited.
