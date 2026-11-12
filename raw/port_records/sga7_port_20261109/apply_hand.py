"""Apply hand-made edits (round 5, 12 Nov 2026) to the translations of SGA 7: the leftovers of rounds 1-4
(PORT_<TARGET>_LEFT.json) whose decision was right but whose edit apply.py could not make (the passage outside the
page window, two occurrences in the window, an overlap with an edit since made, or a \\sisi that the French fix
collapses), and the catalogue fixes of the terminal publisher matter (outside the readers).

Every edit names its file (relative to the target's root, so files that the reader no longer inputs can be edited),
and is made only when tr_old occurs exactly once in that file, the brace balance is kept, no page marker, label or
link key changes, and no two edits overlap. A \\sisi may disappear only where the entry says "collapse": true (both
French layers now read the same). "verify": true only checks that an earlier hand edit is in place (tr_new present,
tr_old absent). Applied and verified entries are logged in PORT_<TARGET>_LOG.jsonl with batch "hand_r5" and
removed from PORT_<TARGET>_LEFT.json (the file before is kept as PORT_<TARGET>_LEFT_before_r5.json).
usage: python -I -B apply_hand.py HAND_R5.json [--dry]"""
import collections
import json
import pathlib
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

dry = "--dry" in sys.argv
entries = json.loads(pathlib.Path([a for a in sys.argv[1:] if not a.startswith("--")][0]).read_text(encoding="utf-8"))
KEYS = re.compile(r"\\(?:label|SGARefTarget|SGARefLink|hyperref|ref|eqref|sref)\{([^}]*)\}")


def bal(s):
    s = s.replace(chr(92) * 2, "").replace(chr(92) + "{", "").replace(chr(92) + "}", "")
    return s.count("{") - s.count("}")


def bad(e):
    old, new = e["tr_old"], e["tr_new"]
    if not old or old == new:
        return "empty or unchanged"
    if bal(old) != bal(new):
        return "brace balance"
    if S.FRMARK.search(old) or S.FRMARK.search(new) or len(S.COUNTER.findall(old)) != len(S.COUNTER.findall(new)):
        return "page marker"
    if collections.Counter(KEYS.findall(old)) != collections.Counter(KEYS.findall(new)):
        return "label or link key"
    if old.count(chr(92) + "sisi") > new.count(chr(92) + "sisi") and not e.get("collapse"):
        return "removes a \\sisi"
    return None


def meta_of(target):
    m = {}
    for f in [HERE / f"batches_{target}" / "ITEMS.json"] + sorted(HERE.glob(f"batches_{target}_*/ITEMS.json")):
        if f.exists():
            m.update(json.loads(f.read_text(encoding="utf-8")))
    return m


texts, crlf, problems, done = {}, {}, [], collections.defaultdict(list)
for e in entries:
    root = S.TARGETS[e["target"]]["root"]
    p = root / e["tr_file"]
    if p not in texts:
        raw = p.read_bytes()
        crlf[p] = b"\r\n" in raw
        texts[p] = raw.decode("utf-8").replace("\r\n", "\n")
    t = texts[p]
    if e.get("verify"):
        ok = t.count(e["tr_new"]) >= 1 and t.count(e["tr_old"]) == 0
        print(("verified " if ok else "NOT IN PLACE ") + e["target"], e["id"])
        if ok:
            done[e["target"]].append((e, None))
        else:
            problems.append((e["id"], "earlier hand edit not in place"))
        continue
    why = bad(e)
    n = t.count(e["tr_old"])
    if why is None and n != 1:
        why = f"tr_old occurs {n} times in {e['tr_file']}"
    if why:
        problems.append((e["id"], why))
        print("REFUSED", e["target"], e["id"], why)
        continue
    k = t.find(e["tr_old"])
    e["_pos"] = (p, k)
    done[e["target"]].append((e, p))
# overlaps
spans = collections.defaultdict(list)
for tgt, lst in done.items():
    for e, p in lst:
        if p is not None:
            k = e["_pos"][1]
            spans[p].append((k, k + len(e["tr_old"]), e["id"]))
for p, sp in spans.items():
    sp.sort()
    for a, b in zip(sp, sp[1:]):
        if b[0] < a[1]:
            problems.append((b[2], f"overlaps {a[2]}"))
if problems:
    print("PROBLEMS, nothing written:", problems)
    sys.exit(1)
for tgt, lst in done.items():
    for e, p in lst:
        if p is not None:
            print(("would apply " if dry else "apply ") + tgt, e["id"], "in", e["tr_file"])
if dry:
    print("dry run: nothing written")
    sys.exit(0)
for p in spans:
    t = texts[p]
    for tgt, lst in done.items():
        for e, q in sorted([x for x in lst if x[1] == p], key=lambda x: -x[0]["_pos"][1]):
            k = e["_pos"][1]
            assert t[k:k + len(e["tr_old"])] == e["tr_old"]
            t = t[:k] + e["tr_new"] + t[k + len(e["tr_old"]):]
    p.write_bytes((t.replace("\n", "\r\n") if crlf[p] else t).encode("utf-8"))
for tgt, lst in done.items():
    meta = meta_of(tgt)
    log = HERE / f"PORT_{tgt.upper()}_LOG.jsonl"
    left_p = HERE / f"PORT_{tgt.upper()}_LEFT.json"
    with open(log, "a", encoding="utf-8") as fh:
        for e, p in lst:
            x = meta.get(e["id"], {})
            rec = dict(id=e["id"], page=int(x.get("page", e.get("page", 0))), kind=x.get("kind"), branch=x.get("branch"),
                       decision="apply", note=e.get("note"), batch="hand_r5",
                       outcome="applied" if p is not None else "verified", why="hand: " + e["why"],
                       decision_from=e.get("decision_from"))
            if p is not None:
                rec.update(tr_file=e["tr_file"], tr_old=e["tr_old"], tr_new=e["tr_new"])
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if left_p.exists():
        before = HERE / f"PORT_{tgt.upper()}_LEFT_before_r5.json"
        if not before.exists():
            shutil.copyfile(left_p, before)
        ids = {e["id"] for e, _ in lst}
        left = [d for d in json.loads(left_p.read_text(encoding="utf-8")) if d["id"] not in ids]
        left_p.write_text(json.dumps(left, ensure_ascii=False, indent=1), encoding="utf-8")
        print(tgt, "left now", len(left))
print("written:", ", ".join(f"{t} {len(l)}" for t, l in done.items()))
