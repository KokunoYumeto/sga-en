"""Which SGA 4 French scan-check fixes are final, for the port into the translations.

The French source of record of the port is the scan-check working copy of SGA 4 (sga_scan_check_20261105/sga4), as
the working copies sga7i/sga7ii were for SGA 7: its corrected layer `current` carries the fixes of the API pass of
11 Nov 2026 (FIXLOG_4_CURRENT.jsonl, replayed from FIXLOG_4.jsonl on the diplomatic layer). A fix is FINAL when
  1. it is in the corrected layer: a FIXLOG_4_CURRENT row whose NEW text is in the file now (the file's hash is also
     compared with the one the pass wrote, APPLY_STATE.json), or a fix of FIXLOG_4 that the corrected layer already had
     (REPLAY_MANUAL_4.json, status "already there"); and
  2. its printed page is not waiting for the in-app recheck (sga4_api_pass_20261111/PAGES_FOR_APP_CHECK.json): the
     recheck can still change those pages.
Not final: the fixes on the pages of the recheck, and the 56 fixes still to be replayed by hand on the corrected layer
(REPLAY_MANUAL_4.json, status "by hand").

Ids: C<i> = row i of FIXLOG_4_CURRENT.jsonl; A<j> = entry j of REPLAY_MANUAL_4.json ("already there"); H<j> = entry j
("by hand"). Writes FINAL_4.json (every fix with its status) and prints the counts.
usage: python -I -B final.py"""
import collections
import hashlib
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
FR = pathlib.Path(r"C:\Users\user\Documents\sga_scan_check_20261105")
PASS = FR / "sga4_api_pass_20261111"


def jl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


cur = jl(FR / "FIXLOG_4_CURRENT.jsonl")
manual = json.loads((FR / "REPLAY_MANUAL_4.json").read_text(encoding="utf-8"))
pages = json.loads((PASS / "PAGES.json").read_text(encoding="utf-8"))
app = json.loads((PASS / "PAGES_FOR_APP_CHECK.json").read_text(encoding="utf-8"))
state = json.loads((PASS / "APPLY_STATE.json").read_text(encoding="utf-8"))
app_pages = {(str(a["file"]), int(a["page"])) for a in app}
page_of = {(str(p["file"]), int(p["folio"])): p for p in pages}

texts, same_as_pass = {}, {}
for d in sorted({p["file"] for p in pages}):
    f = FR / "sga4" / "current" / d / f"{d}.tex"
    raw = f.read_bytes()
    texts[d] = raw.decode("utf-8").replace("\r\n", "\n")
    same_as_pass[d] = hashlib.sha256(raw).hexdigest().upper() == state["files"].get(f"current/{d}/{d}.tex")

out, counts = [], collections.Counter()


def entry(i, src, x, d, page, in_current):
    pg = page_of.get((d, page))
    on_app = (d, page) in app_pages
    status = "final" if in_current and not on_app else ("app_check" if in_current else "not_in_current")
    rec = dict(id=i, source=src, file=d, page=page, expose=pg["expose"] if pg else None,
               counter=pg["counter"] if pg else None, kind=x.get("kind") or "/".join(x.get("kinds") or []),
               old=x["old"], new=x["new"], status=status, page_in_app_check=on_app)
    counts[(src, status)] += 1
    out.append(rec)


for i, x in enumerate(cur):
    d = x["file"].split("/")[0]
    entry(f"C{i}", "FIXLOG_4_CURRENT", x, d, int(x["page"]), x["new"] in texts[d])
for j, x in enumerate(manual):
    d = str(x["file"])
    if x.get("status") == "already there":
        entry(f"A{j}", "already there", x, d, int(x["page"]), x["new"] in texts[d])
    else:
        entry(f"H{j}", "by hand", x, d, int(x["page"]), False)
(HERE / "FINAL_4.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("corrected-layer files unchanged since the pass wrote them:", sum(same_as_pass.values()), "of", len(same_as_pass),
      [d for d, v in same_as_pass.items() if not v])
for k, v in sorted(counts.items()):
    print(f"{k[0]:18s} {k[1]:15s} {v}")
fin = [r for r in out if r["status"] == "final"]
print("FINAL:", len(fin), "fixes on", len({(r['file'], r['page']) for r in fin}), "pages; by exposé:",
      dict(collections.Counter(r["expose"] for r in fin)))
