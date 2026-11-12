"""Compact view of Sol's "apply" edits for the hand check: per id, the French fix as a minimal diff of OLD -> NEW with
the corrected French around it, and the English edit as a minimal diff of tr_old -> tr_new with the English around it
(the text before the edit is applied). Also lists "not_applicable" decisions on fixes of kinds that touch mathematics.
usage: python -I -B review.py DECISIONS.json [...] [--na] [--width=50]"""
import difflib
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
W = int(opts.get("width", 50))
paths = [a for a in sys.argv[1:] if not a.startswith("--")]
meta = {}
for f in sorted(HERE.glob("batches_en4*/ITEMS.json")):
    meta.update(json.loads(f.read_text(encoding="utf-8")))
t = S.load("en4")
TOK = re.compile(r"\\[A-Za-z]+|\\.|\s+|[A-Za-z]+|[0-9]+|.", re.S)


def one(s):
    return re.sub(r"\s+", " ", s)


def mdiff(a, b):
    """Minimal token diff: 'pre[-x-]{+y+}post' segments, joined by ' ... '."""
    ta, tb = TOK.findall(a), TOK.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        pre = "".join(ta[max(0, i1 - 6):i1])
        post = "".join(ta[i2:i2 + 6])
        out.append(f"{one(pre)}[-{one(''.join(ta[i1:i2]))}-]{{+{one(''.join(tb[j1:j2]))}+}}{one(post)}")
    return " ... ".join(out) if out else "(no change)"


def en_context(d, x):
    spans = t.window(x["file"], int(x["page"]))
    old = (d.get("tr_old") or "").replace("\r\n", "\n")
    for f, a, b in spans:
        k = t.texts[f].find(old, a)
        if 0 <= k and k + len(old) <= b:
            return f, k
    return None, -1


def strip_acc(w):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", w) if unicodedata.category(c) != "Mn").lower()


def trivial(a, b):
    """True when OLD -> NEW changes only accents, spacing, punctuation, or a French word ending (agreement)."""
    ta, tb = TOK.findall(a), TOK.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        xa, xb = "".join(ta[i1:i2]), "".join(tb[j1:j2])
        if not (xa + xb).strip() or re.fullmatch(r"[\s,;:.!?«»'’~-]*", xa + xb):
            continue
        ua, ub = strip_acc(xa.strip()), strip_acc(xb.strip())
        if ua == ub:
            continue
        if ua.isalpha() and ub.isalpha() and len(ua) > 2 and len(ub) > 2:
            k = 0
            while k < min(len(ua), len(ub)) and ua[k] == ub[k]:
                k += 1
            if k >= max(len(ua), len(ub)) - 3 and k >= 3:
                continue
        return False
    return True


na_kinds = ("formula", "symbol", "number", "missing", "extra", "reference")
for p in paths:
    for d in json.load(open(p, encoding="utf-8")):
        i = d["id"]
        x = meta.get(i)
        if x is None:
            continue
        dec = d.get("decision")
        if dec == "apply":
            f, k = en_context(d, x)
            old = d["tr_old"].replace("\r\n", "\n")
            if f is None:
                print(f"[{i}] {x['expose']} p.{x['page']} {x['kind']}: EN tr_old NOT FOUND in the window")
                continue
            line = t.texts[f].count("\n", 0, k) + 1
            pre = one(t.texts[f][max(0, k - W):k])
            post = one(t.texts[f][k + len(old):k + len(old) + W])
            print(f"[{i}] {x['expose']} p.{x['page']} {x['kind']}")
            print(f"  FR: {mdiff(x['old'], x['new'])}")
            print(f"  EN {f.name[5:-16]}:{line}: …{pre}⟨{mdiff(old, d['tr_new'].replace(chr(13) + chr(10), chr(10)))}⟩{post}…")
            if d.get("note"):
                print(f"  note: {one(d['note'])[:160]}")
        elif dec == "not_applicable" and "--na" in sys.argv and not trivial(x["old"], x["new"]):
            print(f"[{i}] N/A {x['expose']} p.{x['page']} {x['kind']}: FR {mdiff(x['old'], x['new'])} | {one(d.get('note') or '')[:140]}")
        elif dec == "already" and "--already" in sys.argv:
            print(f"[{i}] ALR {x['expose']} p.{x['page']} {x['kind']}: FR {mdiff(x['old'], x['new'])} | EN «{one(d.get('tr_old') or '')[:150]}»")
