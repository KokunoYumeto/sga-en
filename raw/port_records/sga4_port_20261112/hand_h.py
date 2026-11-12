"""Show the by-hand fixes (REPLAY_MANUAL_4 "by hand", ids H…) for settling: the fix (OLD -> NEW), both readings of the
scan, the corrected French where the fix belongs (anchored by the text around the fix in the text the scan check saw),
and the English lines of the page window that look most like the passage.
usage: python -I -B hand_h.py [IDS,...] [--all] (default: the H fixes whose page is not in the in-app recheck)"""
import difflib
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
import pathlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

F = json.load(open(HERE / "FINAL_4.json", encoding="utf-8"))
M = json.load(open(S.FR / "REPLAY_MANUAL_4.json", encoding="utf-8"))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
want = set(args[0].split(",")) if args else None
H = [x for x in F if x["id"].startswith("H") and (want is None and ("--all" in sys.argv or not x["page_in_app_check"])
                                                   or want is not None and x["id"] in want)]
bh = [x for x in M if x.get("status") == "by hand"]
t = S.load("en4")
pr = {}
cur = {}


def norm(s):
    return re.sub(r"\s+", " ", s)


for x in H:
    m = M[int(x["id"][1:])]
    assert m["old"] == x["old"] and m["new"] == x["new"], x["id"]
    d = x["file"]
    if d not in pr:
        pr[d] = (S.PASS / "pristine" / "diplomatic" / d / f"{d}.tex").read_text(encoding="utf-8")
        cur[d] = (S.FR / "sga4" / "current" / d / f"{d}.tex").read_text(encoding="utf-8")
    p, c = pr[d], cur[d]
    s, e = m["start"], m["end"]
    before, after = p[max(0, s - 70):s], p[e:e + 70]
    print(f"===== {x['id']}  {x['expose']} p. {x['page']}  {x['kind']}  | where: {m.get('where','')[:90]}")
    print("OLD:", x["old"][:300])
    print("NEW:", x["new"][:300])
    for who, rs in m.get("readings", {}).items():
        for r in rs[:1]:
            print(f"  {who}: scan «{str(r.get('scan',''))[:160]}» note: {str(r.get('note',''))[:200]}")
    # the corrected French: the longest piece of the text before the fix that occurs once in the corrected layer
    k = -1
    for L in (60, 45, 30, 20):
        b = before[-L:]
        if c.count(b) == 1:
            k = c.index(b) + len(b)
            break
    if k < 0:
        for L in (60, 45, 30, 20):
            a = after[:L]
            if c.count(a) == 1:
                k = c.index(a) - len(x["old"])
                break
    if k >= 0:
        print("  FR current:", norm(c[max(0, k - 120):k + len(x["old"]) + 160]))
    else:
        print("  FR current: anchor not found; FR seen:", norm(before[-100:] + "[[" + x["old"] + "]]" + after[:100]))
    # English: lines of the window most like OLD and its neighbourhood
    spans = t.window(d, x["page"])
    target = norm(before[-40:] + x["old"] + after[:40])
    cands = []
    for f, a0, b0 in spans:
        txt = t.texts[f][a0:b0]
        lines = txt.split("\n")
        for i in range(len(lines)):
            chunk = " ".join(lines[i:i + 3])
            r = difflib.SequenceMatcher(None, target, norm(chunk)).ratio()
            cands.append((r, f, a0, i, chunk))
    cands.sort(key=lambda z: -z[0])
    seen = set()
    for r, f, a0, i, chunk in cands[:2]:
        line_no = t.texts[f][:a0].count("\n") + i + 1
        if (f, i) in seen:
            continue
        seen.add((f, i))
        print(f"  EN {t.rel(f).split('/')[-1]}:{line_no} ({r:.2f}): {norm(chunk)[:330]}")
