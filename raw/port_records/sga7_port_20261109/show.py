"""Show Sol's decisions of a batch beside the French fixes: python -I show.py TARGET BATCH [DECISION ...] [--n=40]"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
target, batch, kinds = args[0], args[1], set(args[2:]) or {"apply"}
meta = {}
for f in [HERE / f"batches_{target}" / "ITEMS.json"] + sorted(HERE.glob(f"batches_{target}_*/ITEMS.json")):
    if f.exists():
        meta.update(json.loads(f.read_text(encoding="utf-8")))
ds = json.loads((HERE / f"decisions_{batch}.json").read_text(encoding="utf-8"))
for d in [d for d in ds if d.get("decision") in kinds][:int(opts.get("n", 40))]:
    x = meta.get(str(d["id"]), {})
    print(f"--- {d['id']} p.{x.get('page')} {x.get('kind')} {x.get('branch')} [{d.get('decision')}] {d.get('note') or ''}")
    print("   FR  ", repr(x.get("old"))[:160], "->", repr(x.get("new"))[:160])
    print("   TR  ", repr(d.get("tr_old"))[:160], "->", repr(d.get("tr_new"))[:160])
