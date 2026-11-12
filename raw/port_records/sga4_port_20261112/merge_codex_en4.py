"""Merge Codex's seven English SGA 4 fragments of 23-28 Sep 2026 (sga4_english_reader_clean_r8_20260730, never
published) into sga-en sources/native/SGA4. Every hunk was checked against the corrected French
(sga_scan_check_20261105/sga4/current) before this merge (METHODOLOGY.md, "Merge of Codex's seven English files"): each is Codex's correction, and the
repository has no later fix in these files (each file's only commit is 656e043, the 6 Sep text). The repository keeps
its own master file (tomes/SGA4_English_translation_workpass.tex: title and credits pages, rights statement). The
merged files keep the repository's CRLF line endings.
usage: python -I -B merge_codex_en4.py [--write]"""
import hashlib
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
CODEX = pathlib.Path(r"C:\Users\user\Documents\interlanguage_parts\03_projects\language_management\english_germanic"
                     r"\03_working_translations\sga4_english_reader_clean_r8_20260730\source")
REPO = pathlib.Path(r"C:\Users\user\Documents\rights_cc0_20261025\sga-en\sources\native\SGA4"
                    r"\SGA4_English_current_buildable_source_20260906\source")
FILES = ["01/drafts/SGA4_I_LINES_1347_1496_English.texfrag", "01/drafts/SGA4_I_LINES_1497_1738_English.texfrag",
         "01/drafts/SGA4_I_LINES_1739_1946_English.texfrag", "01/drafts/SGA4_I_LINES_4271_4625_English.texfrag",
         "01/drafts/SGA4_I_LINES_4854_5078_English.texfrag", "01/drafts/SGA4_I_LINES_5805_5940_English.texfrag",
         "05bis/drafts/SGA4_VBIS_LINES_3453_3612_English.texfrag"]
write = "--write" in sys.argv
for f in FILES:
    c, r = CODEX / f, REPO / f
    cb, rb = c.read_bytes(), r.read_bytes()
    ct = cb.decode("utf-8").replace("\r\n", "\n")
    crlf = b"\r\n" in rb
    out = (ct.replace("\n", "\r\n") if crlf else ct).encode("utf-8")
    print(f, "codex sha256", hashlib.sha256(cb).hexdigest()[:16], "| repo before", hashlib.sha256(rb).hexdigest()[:16],
          "| merged", hashlib.sha256(out).hexdigest()[:16], "| CRLF" if crlf else "| LF")
    if write:
        r.write_bytes(out)
