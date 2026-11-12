"""Write the batches that carry the final French SGA 4 scan-check fixes into one translation (en4): per printed page,
the translation's text of the page and its neighbours (segment.py), then the French fixes of that page (FINAL_4.json,
made by final.py; only status "final"), each with OLD, NEW and the corrected French around the corrected place
(sga_scan_check_20261105/sga4/current). Items already in the target's log (PORT_<TARGET>_LOG.jsonl) are left out.
usage: python -I -B build.py TARGET [ITEMS_PER_BATCH=120] [--max-kb=260] [--ids=C1,A2,...] [--tag=NAME]"""
import collections
import difflib
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
name = args[0]
per = int(args[1]) if len(args) > 1 else 120
max_kb = int(opts.get("max-kb", 260))
TAG = opts.get("tag", name)
only = set(opts["ids"].split(",")) if "ids" in opts else None
t = S.load(name)
LANG = t.lang

items = [x for x in json.loads((HERE / "FINAL_4.json").read_text(encoding="utf-8")) if x["status"] == "final"]
LOG = HERE / f"PORT_{name.upper()}_LOG.jsonl"
done = {json.loads(l)["id"] for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()} if LOG.exists() else set()
items = [x for x in items if x["id"] not in done and (only is None or x["id"] in only)]
if only:
    missing = only - {x["id"] for x in items}
    assert not missing, f"ids not final or already logged: {sorted(missing)}"

# the corrected French, with the start of every printed page (the k-th marker outside comments is the k-th page)
pages = json.loads((S.PASS / "PAGES.json").read_text(encoding="utf-8"))
fr_text, fr_start = {}, {}
for d in S.DIRS:
    txt = (S.FR / "sga4" / "current" / d / f"{d}.tex").read_text(encoding="utf-8")
    fr_text[d] = txt
    pr = (S.PASS / "pristine" / "diplomatic" / d / f"{d}.tex").read_text(encoding="utf-8").split("\n")
    fp = [p for p in sorted((p for p in pages if p["file"] == d), key=lambda p: p["marker_line"])
          if S.MARK.search(S.code(pr[p["marker_line"] - 1]))]
    lines, off, marks = txt.split("\n"), 0, []
    for ln in lines:
        for m in S.MARK.finditer(S.code(ln)):
            marks.append(off)
        off += len(ln) + 1
    assert len(marks) == len(fp), (d, len(marks), len(fp))
    for p, k in zip(fp, marks):
        fr_start[(d, p["folio"])] = k


# where each fix was made in the text the scan check saw (pristine diplomatic): its neighbours pick the right
# occurrence of NEW in the corrected layer when NEW occurs more than once near the page
agreed = json.loads((S.PASS / "AGREED_FIXES.json").read_text(encoding="utf-8"))
manual = json.loads((S.FR / "REPLAY_MANUAL_4.json").read_text(encoding="utf-8"))
pristine = {d: (S.PASS / "pristine" / "diplomatic" / d / f"{d}.tex").read_text(encoding="utf-8") for d in S.DIRS}


def anchor(it):
    """(text before, text after) the fix in the pristine diplomatic text, or None."""
    if it["id"].startswith("A"):
        x = manual[int(it["id"][1:])]
        cands = [(x["start"], x["end"])]
    else:
        cands = [(a["start"], a["end"]) for a in agreed if a["file"] == it["file"] and int(a["page"]) == it["page"]
                 and a["old"] == it["old"] and a["new"] == it["new"]]
    if len(cands) != 1:
        return None
    s, e = cands[0]
    pt = pristine[it["file"]]
    return pt[max(0, s - 80):s], pt[e:e + 80]


def fr_context(it, width=300):
    """The corrected French around the fix: NEW between the starts of pages page-1 and page+2; where NEW occurs more
    than once there, the occurrence with the same neighbours as the fix in the text the scan check saw."""
    d, f, txt = it["file"], it["page"], fr_text[it["file"]]
    a = fr_start.get((d, f - 1), fr_start.get((d, f), 0))
    nxt = [v for (dd, g), v in fr_start.items() if dd == d and g > f + 1]
    b = min(nxt) if nxt else len(txt)
    a = txt.rfind("\n", 0, a) + 1
    if not it["new"].strip():
        return None, 0
    hits = [a + m.start() for m in re.finditer(re.escape(it["new"]), txt[a:b])]
    if not hits:
        return None, 0
    n_hits = len(hits)
    if n_hits > 1:
        an = anchor(it)
        if an:   # the occurrence whose neighbours look most like those of the fix (a \sisi may wrap it now)
            before, after = an
            L = len(it["new"])

            def score(k):
                return (difflib.SequenceMatcher(None, before[-60:], txt[max(0, k - 60):k]).ratio()
                        + difflib.SequenceMatcher(None, after[:60], txt[k + L:k + L + 60]).ratio())
            hits.sort(key=score, reverse=True)
            if score(hits[0]) - score(hits[1]) > 0.3:
                n_hits = 1
    k = hits[0]
    return txt[max(0, k - width):k + len(it["new"]) + width], n_hits


bypage = collections.defaultdict(list)
no_target = []
for it in items:
    if t.window(it["file"], it["page"]):
        bypage[(it["file"], it["page"])].append(it)
    else:
        no_target.append(it["id"])
order = {d: i for i, d in enumerate(S.DIRS)}
keys = sorted(bypage, key=lambda k: (order[k[0]], k[1]))


def page_bytes(d, q):
    return sum(len(t.texts[f][a:b].encode("utf-8")) for f, a, b in t.segs.get((d, q), []))


batches, curb, n, kb = [], [], 0, 0
for k in keys:
    add = sum(page_bytes(k[0], q) for q in (k[1] - 1, k[1], k[1] + 1)) / 1024
    if curb and (n + len(bypage[k]) > per or kb + add > max_kb):
        batches.append(curb)
        curb, n, kb = [], 0, 0
    curb.append(k)
    n += len(bypage[k])
    kb += add
if curb:
    batches.append(curb)
out = HERE / f"batches_{TAG}"
out.mkdir(exist_ok=True)
index = []
EXP = {p["file"]: p["expose"] for p in pages}
for b, ks in enumerate(batches, 1):
    bname = f"{TAG}_{b:03d}"
    lines = [f"# {bname}: {sum(len(bypage[k]) for k in ks)} items on {len(ks)} printed pages of SGA 4", ""]
    shown, ids = set(), []
    for d, p in ks:
        lines.append(f"=================== EXPOSÉ {EXP[d]}, PAGE {p} ===================")
        for q in (p - 1, p, p + 1):
            for f, a, e in t.segs.get((d, q), []):
                if (f, a, e) in shown:
                    lines.append(f"----- ({LANG} text of page {q}, file {t.rel(f)}: shown above in this file) -----")
                    continue
                shown.add((f, a, e))
                whole = " (the whole file: its page breaks are not marked)" if f in t.unaligned else ""
                lines.append(f"----- {LANG}, file {t.rel(f)}, page {q}{whole} -----")
                lines.append(t.texts[f][a:e].rstrip("\n"))
        lines.append(f"----- French corrections on page {p} -----")
        for it in bypage[(d, p)]:
            ids.append(it["id"])
            lines += [f"[id {it['id']}] kind {it['kind']}; French file {d}/{d}.tex",
                      "OLD: " + it["old"], "NEW: " + it["new"]]
            ctx, nh = fr_context(it)
            if ctx:
                lines.append("FRENCH CONTEXT (corrected, after the fix): " + ctx)
            it["fr_hits"] = nh
            lines.append("")
    (out / f"{bname}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    index.append(dict(batch=bname, items=len(ids), ids=ids, pages=[f"{d}:{p}" for d, p in ks]))
(out / "BATCHES.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
(out / "ITEMS.json").write_text(json.dumps({it["id"]: it for it in items}, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / f"no_target_{TAG}.json").write_text(json.dumps(no_target), encoding="utf-8")
sizes = [(out / f"{x['batch']}.txt").stat().st_size for x in index] or [0]
print(name, len(index), "batches;", sum(x["items"] for x in index), "items;", len(no_target), "without target text;",
      "French context found for", sum(1 for it in items if it.get("fr_hits")), "| KB min/max/mean",
      min(sizes) // 1024, max(sizes) // 1024, sum(sizes) // max(1, len(sizes)) // 1024)
