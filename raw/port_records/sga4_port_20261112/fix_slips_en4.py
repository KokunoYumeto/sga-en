"""Correct two slips of the English SGA 4 (not fixes of the French): "algebraic separable" -> "separable algebraic"
(Exposé VIII, three places; the French reads "algébriques séparables") and "whence a" + "isomorphism" -> "whence an"
(Exposé XVIII, across two fragments). Each replacement must match exactly once; line endings (CRLF) are kept.
usage: python -I -B fix_slips_en4.py [--write]"""
import pathlib
import sys

ROOT = pathlib.Path("C:/Users/user/Documents/rights_cc0_20261025/sga-en/sources/native/SGA4/"
                    "SGA4_English_current_buildable_source_20260906/source")
NL = chr(13) + chr(10)
EDITS = [
    ("08/drafts/SGA4_VIII_LINES_1012_1556_English.texfrag",
     "\\emph{algebraic" + NL + "  separable} over $X$", "\\emph{separable" + NL + "  algebraic} over $X$"),
    ("08/drafts/SGA4_VIII_LINES_1012_1556_English.texfrag",
     "\\emph{algebraic separable} over $X$", "\\emph{separable algebraic} over $X$"),
    ("08/drafts/SGA4_VIII_LINES_1012_1556_English.texfrag",
     "geometric points algebraic" + NL + "separable over $X$", "geometric points separable" + NL + "algebraic over $X$"),
    ("18/drafts/SGA4_XVIII_LINES_856_1250_English.texfrag",
     "+Z_{\\Ll_{2}}$, whence a" + NL, "+Z_{\\Ll_{2}}$, whence an" + NL),
]
write = "--write" in sys.argv
texts = {}
for rel, old, new in EDITS:
    p = ROOT / rel
    t = texts.get(rel) or p.read_bytes().decode("utf-8")
    n = t.count(old)
    assert n == 1, (rel, old, n)
    texts[rel] = t.replace(old, new)
    print("ok", rel, repr(old[:40]))
nxt = (ROOT / "18/drafts/SGA4_XVIII_LINES_1251_1650_English.texfrag").read_bytes().decode("utf-8")
assert nxt.startswith("isomorphism ("), nxt[:40]
assert texts["18/drafts/SGA4_XVIII_LINES_856_1250_English.texfrag"].endswith("whence an" + NL)
if write:
    for rel, t in texts.items():
        (ROOT / rel).write_bytes(t.encode("utf-8"))
    print("written", len(texts), "files")
