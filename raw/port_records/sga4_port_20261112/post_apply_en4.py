"""One edit after apply.py that its link-key check does not allow: fix C733 (XVIII, p. 482). The corrected French reads
"généralisée en 2.17" (the print's number, no link); Sol changed the shown number from 2.14 to 2.17 and kept the link to
Theorem 2.14, which the English translator had added. A "2.17" that links to 2.14 is wrong, so the link goes and the
text reads "generalized in 2.17.", as the French. Must match exactly once; CRLF kept.
usage: python -I -B post_apply_en4.py [--write]"""
import pathlib
import sys

F = pathlib.Path("C:/Users/user/Documents/rights_cc0_20261025/sga-en/sources/native/SGA4/"
                 "SGA4_English_current_buildable_source_20260906/source/18/drafts/SGA4_XVIII_LINES_44_450_English.texfrag")
OLD = "generalized in \\hyperref[XVIII.thm2.14]{2.17}."
NEW = "generalized in 2.17."
t = F.read_bytes().decode("utf-8")
assert t.count(OLD) == 1, t.count(OLD)
print("ok C733")
if "--write" in sys.argv:
    F.write_bytes(t.replace(OLD, NEW).encode("utf-8"))
    print("written")
