"""Pick the pilot: about 20 final fixes (FINAL_4.json), at random with a fixed seed, by groups of kinds, at most two per
exposé, none whose page window touches the seven English fragments that Codex edited after the repository build
(23-28 Sep; SOURCE_OF_RECORD_AUDIT_20261110/evidence/en_sga4_codexworking_vs_repo.txt), since the repository copy of
those is not the newest English. Writes PILOT_IDS.json.
usage: python -I -B pick_pilot.py [--seed=20261112]"""
import collections
import json
import pathlib
import random
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import segment as S  # noqa: E402

opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
seed = int(opts.get("seed", 20261112))
CODEX_NEWER = {"SGA4_I_LINES_1347_1496_English.texfrag", "SGA4_I_LINES_1497_1738_English.texfrag",
               "SGA4_I_LINES_1739_1946_English.texfrag", "SGA4_I_LINES_4271_4625_English.texfrag",
               "SGA4_I_LINES_4854_5078_English.texfrag", "SGA4_I_LINES_5805_5940_English.texfrag",
               "SGA4_VBIS_LINES_3453_3612_English.texfrag"}
GROUPS = [("mathematics", r"formula|symbol|number|font", 8), ("words", r"word|missing|extra", 8),
          ("punctuation or accent", r"^(punctuation|accent)$", 2)]
t = S.load("en4")
fin = [x for x in json.loads((HERE / "FINAL_4.json").read_text(encoding="utf-8")) if x["status"] == "final"]
ok = []
for x in fin:
    w = t.window(x["file"], x["page"])
    if w and not any(p.name in CODEX_NEWER for p, _, _ in w):
        ok.append(x)
rng = random.Random(seed)
picked, per_exp = [], collections.Counter()
cs = [x for x in ok if x["id"].startswith("C")]
for label, rx, n in GROUPS:
    pool = [x for x in cs if re.search(rx, x["kind"])]
    rng.shuffle(pool)
    got = 0
    for x in pool:
        if got == n:
            break
        if per_exp[x["expose"]] >= 2 or x in picked:
            continue
        picked.append(dict(x, group=label))
        per_exp[x["expose"]] += 1
        got += 1
pool = [x for x in ok if x["id"].startswith("A")]
rng.shuffle(pool)
for x in pool[:2]:
    picked.append(dict(x, group="already in the corrected layer before the pass"))
(HERE / "PILOT_IDS.json").write_text(json.dumps(dict(
    seed=seed, candidates=len(ok), final=len(fin), excluded_codex_newer=len(fin) - len(ok),
    ids=[x["id"] for x in picked], items=picked), ensure_ascii=False, indent=1), encoding="utf-8")
print(len(fin), "final;", len(ok), "candidates outside the Codex-newer fragments; picked", len(picked))
for x in picked:
    print(f"{x['id']:6s} {x['expose']:5s} p.{x['page']:<4d} {x['kind']:18s} {x['group'][:12]:12s} "
          f"{x['old'][:60]!r} -> {x['new'][:60]!r}")
print(",".join(x["id"] for x in picked))
