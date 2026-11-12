"""Apply Sol's decisions to one translation of SGA 7 (as the EGA ports do): an "apply" edit is made when tr_old occurs
exactly once in the translation's text of folios PAGE-1..PAGE+1 (in tr_file, or, if that fails, in exactly one file of
the window), when it keeps the brace balance, the page markers, the label and link keys and the \\sisi branches, and
when it does not overlap another edit. Everything else goes to PORT_<TARGET>_LEFT.json. Every decision is logged in
PORT_<TARGET>_LOG.jsonl; ids already logged are skipped.
usage: python -I apply.py TARGET DECISIONS.json [...] [--dry]"""
import collections
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

name = sys.argv[1]
dry = "--dry" in sys.argv
paths = [a for a in sys.argv[2:] if not a.startswith("--")]
meta = {}
for f in [HERE / f"batches_{name}" / "ITEMS.json"] + sorted(HERE.glob(f"batches_{name}_*/ITEMS.json")):  # not en7II for en7I
    if not f.exists():
        continue
    meta.update(json.loads(f.read_text(encoding="utf-8")))
t = S.load(name)
LOG = HERE / f"PORT_{name.upper()}_LOG.jsonl"
LEFT = HERE / f"PORT_{name.upper()}_LEFT.json"
done = {json.loads(l)["id"] for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()} if LOG.exists() else set()
KEYS = re.compile(r"\\(?:label|SGARefTarget|SGARefLink|hyperref|ref|eqref|sref)\{([^}]*)\}")


def bal(s):
    s = s.replace(chr(92) * 2, "").replace(chr(92) + "{", "").replace(chr(92) + "}", "")
    return s.count("{") - s.count("}")


def occurrences(spans, f, s):
    hits = set()
    for g, a, b in spans:
        if g != f:
            continue
        k = t.texts[f].find(s, a)
        while k >= 0 and k + len(s) <= b:
            hits.add(k)
            k = t.texts[f].find(s, k + 1)
    return sorted(hits)


def bad(old, new):
    if not old or old == new:
        return "empty or unchanged"
    if bal(old) != bal(new):
        return "brace balance"
    if S.FRMARK.search(old) or S.FRMARK.search(new) or S.COUNTER.search(old) != S.COUNTER.search(new):
        return "page marker"
    if collections.Counter(KEYS.findall(old)) != collections.Counter(KEYS.findall(new)):
        return "label or link key"
    if old.count(chr(92) + "sisi") > new.count(chr(92) + "sisi"):
        return "removes a \\sisi"
    return None


stats = collections.Counter()
left = json.loads(LEFT.read_text(encoding="utf-8")) if LEFT.exists() else []
edits, logrecs = [], []
for path in paths:
    for d in json.load(open(path, encoding="utf-8")):
        i = str(d.get("id"))
        if i in done or i not in meta:
            stats["skipped"] += 1
            continue
        x = meta[i]
        page = int(x["page"])
        rec = dict(id=i, page=page, kind=x["kind"], branch=x["branch"], decision=d.get("decision"), note=d.get("note"),
                   batch=pathlib.Path(path).stem)
        if d.get("decision") == "apply":
            old = (d.get("tr_old") or "").replace("\r\n", "\n")
            new = (d.get("tr_new") or "").replace("\r\n", "\n")
            spans = t.window(page, 1)
            why = bad(old, new)
            hit = None
            if why is None:
                want = (d.get("tr_file") or "").replace(S.BS, "/")
                for f in {g for g, _, _ in spans}:
                    if t.rel(f) == want or f.name == want.rsplit("/", 1)[-1]:
                        occ = occurrences(spans, f, old)
                        if len(occ) == 1:
                            hit = (f, occ[0])
                if hit is None:
                    allhits = [(f, k) for f in {g for g, _, _ in spans} for k in occurrences(spans, f, old)]
                    if len(allhits) == 1:
                        hit = allhits[0]
                    else:
                        why = f"tr_old occurs {len(allhits)} times on pages {page - 1}-{page + 1}"
            if hit is not None and any(f == hit[0] and k < hit[1] + len(old) and hit[1] < k + len(o)
                                       for f, k, o, _, _ in edits):
                hit, why = None, "overlaps another edit"
            if hit is None:
                rec.update(outcome="left", why=why)
                left.append(dict(d, page=page, why=why))
            else:
                f, k = hit
                edits.append((f, k, old, new, i))
                rec.update(outcome="applied", tr_file=t.rel(f), tr_old=old, tr_new=new)
        else:
            rec["outcome"] = d.get("decision")
        stats[rec["outcome"]] += 1
        logrecs.append(rec)
changed = set()
if not dry:
    for f, k, old, new, i in sorted(edits, key=lambda e: (str(e[0]), -e[1])):
        assert t.texts[f][k:k + len(old)] == old
        t.texts[f] = t.texts[f][:k] + new + t.texts[f][k + len(old):]
        changed.add(f)
    for f in changed:   # keep the file's own line endings (the repositories store CRLF)
        crlf = b"\r\n" in f.read_bytes()
        f.write_text(t.texts[f], encoding="utf-8", newline="\r\n" if crlf else "")
    with open(LOG, "a", encoding="utf-8") as fh:
        for r in logrecs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    LEFT.write_text(json.dumps(left, ensure_ascii=False, indent=1), encoding="utf-8")
if "--why" in sys.argv:
    for r in logrecs:
        if r.get("outcome") == "left":
            print("  left", r["id"], r.get("why"))
print(("dry run " if dry else "") + ", ".join(f"{k} {v}" for k, v in sorted(stats.items())),
      "| files changed", len(changed))
