"""How well do the page windows (folios p-1..p+1) of each target hold the place of a French fix? For every fix whose
old or new text has a formula that also occurs somewhere in the target (normalized), count whether it occurs inside
the window. usage: python -I check_windows.py [TARGET ...]"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import segment as S  # noqa: E402

for name in sys.argv[1:] or list(S.TARGETS):
    t = S.load(name)
    log = S.FR / f"FIXLOG_{t.vol}_CURRENT.jsonl"
    fixes = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
    whole = {p: S.norm(x) for p, x in t.texts.items()}
    inwin = anywhere = tried = 0
    misses = []
    for x in fixes:
        if x["kind"] == "marker":
            continue
        cands = [S.norm(m.group(0)) for s in (x["old"], x["new"]) for m in S.MATH.finditer(s)]
        cands = [c for c in cands if len(c) >= 6]
        if not cands:
            continue
        tried += 1
        hit_any = [c for c in cands if any(c in w for w in whole.values())]
        if not hit_any:
            continue
        anywhere += 1
        win = "".join(S.norm(t.texts[p][a:b]) for p, a, b in t.window(int(x["page"]), 1))
        if any(c in win for c in hit_any):
            inwin += 1
        else:
            win2 = "".join(S.norm(t.texts[p][a:b]) for p, a, b in t.window(int(x["page"]), 3))
            misses.append((x["page"], hit_any[0][:40], any(c in win2 for c in hit_any)))
    print(f"{name}: fixes with formulas {tried}; found in the target {anywhere}; inside p-1..p+1 {inwin}; "
          f"misses {len(misses)} (of them within p-3..p+3: {sum(1 for m in misses if m[2])})")
    for m in misses[:8]:
        print("   ", m)
