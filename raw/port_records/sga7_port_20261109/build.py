"""Write the batches that carry the French SGA 7 scan-check fixes into one translation (en7I, en7II, es7I, es7II):
per printed page, the translation's text of the page and its neighbours (segment.py), then the French fixes of that
page. English: the fixes of the corrected French (FIXLOG_<vol>_CURRENT.jsonl). Spanish (one source, two branches
\\sisi{original}{corregida}): the fixes of both French layers, paired: "both" when the same edit was made in the
diplomatic and the corrected French, otherwise "diplomatic only" or "corrected only". Page-marker fixes are left out.
Items already in the target's log (PORT_<TARGET>_LOG.jsonl) are left out, so a later run takes only new fixes.
usage: python -I build.py TARGET [ITEMS_PER_BATCH=120] [--max-kb=260] [--pages=A-B] [--tag=NAME]"""
import collections
import json
import pathlib
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
lo, hi = (int(v) for v in opts["pages"].split("-")) if "pages" in opts else (0, 10 ** 6)
t = S.load(name)
vol = t.vol
FRD = S.FR / ("sga7i" if vol == "7I" else "sga7ii")


def read_log(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


cur = read_log(S.FR / f"FIXLOG_{vol}_CURRENT.jsonl")
dip = read_log(S.FR / f"FIXLOG_{vol}.jsonl")
SKIP = {"marker", "dash_convention"}  # page markers; the price-dash convention of the publisher list (not exact edits)
items = []
if name.startswith("en"):
    for i, x in enumerate(cur):
        if x["kind"] not in SKIP:
            items.append(dict(id=f"C{i}", branch="corrected", cur=i, **{k: x[k] for k in ("file", "page", "kind", "old", "new")}))
else:
    free = collections.defaultdict(list)
    for j, x in enumerate(dip):
        free[(x["file"], x["page"], x["old"], x["new"])].append(j)
    for i, x in enumerate(cur):
        if x["kind"] in SKIP:
            continue
        js = free.get((x["file"], x["page"], x["old"], x["new"]))
        if js:
            j = js.pop(0)
            items.append(dict(id=f"B{i}", branch="both", cur=i, dip=j, **{k: x[k] for k in ("file", "page", "kind", "old", "new")}))
        else:
            items.append(dict(id=f"C{i}", branch="corrected", cur=i, **{k: x[k] for k in ("file", "page", "kind", "old", "new")}))
    paired = {it["dip"] for it in items if "dip" in it}
    for j, x in enumerate(dip):
        if x["kind"] in SKIP or j in paired:
            continue
        items.append(dict(id=f"D{j}", branch="diplomatic", dip=j, **{k: x[k] for k in ("file", "page", "kind", "old", "new")}))
LOG = HERE / f"PORT_{name.upper()}_LOG.jsonl"
done = {json.loads(l)["id"] for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()} if LOG.exists() else set()
items = [it for it in items if it["id"] not in done and lo <= int(it["page"]) <= hi]

fr_text = {}
for layer in ("current", "diplomatic"):
    for fn in S.FRFILES[vol]:
        fr_text[(layer, fn)] = (FRD / layer / fn).read_text(encoding="utf-8", errors="replace")


def fr_context(it, width=300):
    layer = "diplomatic" if it["branch"] == "diplomatic" else "current"
    txt = fr_text.get((layer, it["file"]), "")
    if it["new"].strip():
        k = txt.find(it["new"])
        if k >= 0:
            return txt[max(0, k - width):k + len(it["new"]) + width]
    return None


bypage = collections.defaultdict(list)
no_target = []
for it in items:
    p = int(it["page"])
    if t.window(p, 1):
        bypage[p].append(it)
    else:
        no_target.append(it["id"])
pages = sorted(bypage)


def page_text(p):
    return "".join(t.texts[f][a:b] for f, a, b in t.segs.get(p, []))


batches, curb, n, kb = [], [], 0, 0
shown_est = set()
for p in pages:
    add = sum(len(page_text(q).encode("utf-8")) for q in (p - 1, p, p + 1) if q not in shown_est) / 1024
    if curb and (n + len(bypage[p]) > per or kb + add > max_kb):
        batches.append(curb)
        curb, n, kb, shown_est = [], 0, 0, set()
        add = sum(len(page_text(q).encode("utf-8")) for q in (p - 1, p, p + 1)) / 1024
    curb.append(p)
    n += len(bypage[p])
    kb += add
    shown_est |= {p - 1, p, p + 1}
if curb:
    batches.append(curb)
LANG = "English" if name.startswith("en") else "Spanish"
out = HERE / f"batches_{TAG}"
out.mkdir(exist_ok=True)
index = []
for b, ps in enumerate(batches, 1):
    bname = f"{TAG}_{b:03d}"
    lines = [f"# {bname}: {sum(len(bypage[p]) for p in ps)} items on {len(ps)} printed pages of SGA {vol[0]} {vol[1:]}", ""]
    shown, ids = set(), []
    for p in ps:
        lines.append(f"=================== PAGE {p} ===================")
        for q in (p - 1, p, p + 1):
            if q in shown:
                lines.append(f"----- ({LANG} text of page {q}: shown above in this file) -----")
                continue
            shown.add(q)
            for f, a, e in t.segs.get(q, []):
                lines.append(f"----- {LANG}, file {t.rel(f)}, page {q} -----")
                lines.append(t.texts[f][a:e].rstrip("\n"))
        lines.append(f"----- French corrections on page {p} -----")
        for it in bypage[p]:
            ids.append(it["id"])
            head = f"[id {it['id']}] kind {it['kind']}; French file {it['file']}"
            if LANG == "Spanish":
                head += {"both": "; BRANCH: both", "corrected": "; BRANCH: corrected only",
                         "diplomatic": "; BRANCH: diplomatic only"}[it["branch"]]
            lines += [head, "OLD: " + it["old"], "NEW: " + it["new"]]
            ctx = fr_context(it)
            if ctx:
                lines.append(("FRENCH CONTEXT (diplomatic, after the fix): " if it["branch"] == "diplomatic" else
                              "FRENCH CONTEXT (corrected, after the fix): ") + ctx)
            lines.append("")
    (out / f"{bname}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    index.append(dict(batch=bname, items=len(ids), ids=ids, pages=[ps[0], ps[-1]]))
(out / "BATCHES.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
(out / "ITEMS.json").write_text(json.dumps({it["id"]: it for it in items}, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / f"no_target_{TAG}.json").write_text(json.dumps(no_target), encoding="utf-8")
sizes = [(out / f"{x['batch']}.txt").stat().st_size for x in index] or [0]
print(name, len(index), "batches;", sum(x["items"] for x in index), "items;", len(no_target), "without target text;",
      "branches", dict(collections.Counter(it["branch"] for it in items)),
      "| KB min/max/mean", min(sizes) // 1024, max(sizes) // 1024, sum(sizes) // max(1, len(sizes)) // 1024)
