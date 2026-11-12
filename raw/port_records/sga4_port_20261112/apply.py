"""Check Sol's decisions for one translation of SGA 4 as the SGA 7 port applies them (sga7_port_20261109/apply.py): an
"apply" edit could be made when tr_old occurs exactly once in the translation's text of folios PAGE-1..PAGE+1 of its
exposé (in tr_file, or, if that fails, in exactly one file of the window), when it keeps the brace balance, the page
markers, the label and link keys and the \\sisi records, and when it does not overlap another edit; an "already" is
checked the same way (its tr_old once in the window).

With --write (the user approved the English port, brief of 12 Nov 2026 about 04:35 UTC) the edits that pass are made
(the files keep their CRLF line endings), every settled decision (applied, already found once, not applicable) is
logged in PORT_<TARGET>_LOG.jsonl, and everything else (a refused edit or quote, "unclear") goes to
PORT_<TARGET>_LEFT.json (by id; not logged, so a later round can send it again). Without --write it only reports and
writes CHECK_<decisions file stem>.json (every decision with its check outcome).
usage: python -I -B apply.py TARGET DECISIONS.json [...] [--write]"""
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
paths = [a for a in sys.argv[2:] if not a.startswith("--")]
write = "--write" in sys.argv
LOG = HERE / f"PORT_{name.upper()}_LOG.jsonl"
LEFT = HERE / f"PORT_{name.upper()}_LEFT.json"
done = {json.loads(l)["id"] for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()} if LOG.exists() else set()
left = json.loads(LEFT.read_text(encoding="utf-8")) if LEFT.exists() else {}
# corrections from the hand check (HANDFIX_<TARGET>.json: id -> fields that replace Sol's, with "why")
HF = HERE / f"HANDFIX_{name.upper()}.json"
handfix = json.loads(HF.read_text(encoding="utf-8")) if HF.exists() else {}
meta = {}
for f in sorted(HERE.glob(f"batches_{name}*/ITEMS.json")):
    meta.update(json.loads(f.read_text(encoding="utf-8")))
t = S.load(name)
KEYS = [re.compile(r"\\(?:hyperref|eqhyperref|pagehyperref)\[([^\]]*)\]"),
        re.compile(r"\\(?:hyperrefext|eqhyperrefext|neweqhyperrefext)\[[^\]]*\]\[([^\]]*)\]"),
        re.compile(r"\\etiquette(?:\[[^\]]*\])?\{([^}]*)\}"),
        re.compile(r"\\(?:label|ref|eqref|pageref|cite|refvb|refnoexpose|nderef)\{([^}]*)\}"),
        re.compile(r"\\MakeLinkTarget\*?\{([^}]*)\}")]


def keys(s):
    return collections.Counter(k for rx in KEYS for k in rx.findall(s))


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
    if len(S.MARK.findall(old)) != len(S.MARK.findall(new)):
        return "page marker"
    if keys(old) != keys(new):
        return "label or link key"
    if old.count(chr(92) + "sisi") > new.count(chr(92) + "sisi"):
        return "removes a \\sisi"
    return None


def locate(spans, d, old):
    want = (d.get("tr_file") or "").replace(S.BS, "/")
    for f in {g for g, _, _ in spans}:
        if t.rel(f) == want or f.name == want.rsplit("/", 1)[-1]:
            occ = occurrences(spans, f, old)
            if len(occ) == 1:
                return (f, occ[0]), None
    allhits = [(f, k) for f in {g for g, _, _ in spans} for k in occurrences(spans, f, old)]
    if len(allhits) == 1:
        return allhits[0], None
    return None, f"tr_old occurs {len(allhits)} times in the window"


stats = collections.Counter()
edits, logrecs = [], []
for path in paths:
    recs = []
    for d in json.load(open(path, encoding="utf-8")):
        i = str(d.get("id"))
        if i not in meta:
            stats["unknown id"] += 1
            continue
        if write and i in done:
            stats["already logged"] += 1
            continue
        x = meta[i]
        if i in handfix:
            d = dict(d, **{k: v for k, v in handfix[i].items() if k != "why"}, hand_check=handfix[i]["why"])
        spans = t.window(x["file"], int(x["page"]))
        rec = dict(id=i, expose=x["expose"], page=x["page"], kind=x["kind"], decision=d.get("decision"),
                   note=d.get("note"), tr_file=d.get("tr_file"), tr_old=d.get("tr_old"), tr_new=d.get("tr_new"))
        if d.get("hand_check"):
            rec["hand_check"] = d["hand_check"]
        dec = d.get("decision")
        if dec in ("apply", "already"):
            old = (d.get("tr_old") or "").replace("\r\n", "\n")
            new = (d.get("tr_new") or "").replace("\r\n", "\n")
            why = bad(old, new) if dec == "apply" else (None if old else "no tr_old")
            hit = None
            if why is None:
                hit, why = locate(spans, d, old)
            if dec == "apply" and hit is not None and any(f == hit[0] and k < hit[1] + len(old) and hit[1] < k + len(o)
                                                          for f, k, o, _, _ in edits):
                hit, why = None, "overlaps another edit"
            if hit is None:
                rec.update(check="refused", why=why)
            else:
                if dec == "apply":
                    edits.append((hit[0], hit[1], old, new, i))
                rec.update(check=("applied" if write else "would apply") if dec == "apply" else "already: found once",
                           at=f"{t.rel(hit[0])}:{t.texts[hit[0]].count(chr(10), 0, hit[1]) + 1}")
        else:
            rec["check"] = dec
        stats[rec["check"]] += 1
        rec["batch"] = pathlib.Path(path).stem.replace("decisions_", "")
        recs.append(rec)
        if rec["check"] in ("refused", "unclear"):
            left[i] = rec
        else:
            left.pop(i, None)
            logrecs.append(rec)
    out = HERE / f"CHECK_{pathlib.Path(path).stem}.json"
    out.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
changed = set()
if write:
    for f, k, old, new, i in sorted(edits, key=lambda e: (str(e[0]), -e[1])):
        assert t.texts[f][k:k + len(old)] == old
        t.texts[f] = t.texts[f][:k] + new + t.texts[f][k + len(old):]
        changed.add(f)
    for f in changed:   # keep the file's own line endings (the repository stores CRLF)
        crlf = bytes([13, 10]) in f.read_bytes()
        f.write_text(t.texts[f], encoding="utf-8", newline=chr(13) + chr(10) if crlf else "")
    with open(LOG, "a", encoding="utf-8") as fh:
        for r in logrecs:
            fh.write(json.dumps(r, ensure_ascii=False) + chr(10))
    LEFT.write_text(json.dumps(left, ensure_ascii=False, indent=1), encoding="utf-8")
print(("written: " if write else "dry run: ") + ", ".join(f"{k} {v}" for k, v in sorted(stats.items())),
      "| files changed", len(changed), "| left open", len(left))
