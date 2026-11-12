"""Carry the final French SGA 4 scan-check fixes into one translation with OpenAI GPT-6.1 Sol (effort high, Flex tier),
batch by batch, at most CONCURRENCY at a time; answers in answer_<batch>.md and decisions_<batch>.json; each decisions
file is dry-run with apply.py. When the run ends, one row for it goes into the compute-cost ledger
(compute_cost_ledger/LEDGER.jsonl, id "sga4-port-<tag>"). The prompt is that of the SGA 7 ports
(sga7_port_20261109/run.py), adapted to SGA 4 and to the English edition's \\sisi records.
usage: python -I -B run.py TARGET [CONCURRENCY=1] [--only=BATCH,BATCH] [--tag=NAME] [--effort=high] [--work="..."]
The API key is read from the user's note at run time by enr_pilot (never printed or stored)."""
import datetime
import json
import os
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\user\Documents\enriques_api_pilot_20261106")
import enr_pilot as P  # noqa: E402

LEDGER = r"C:\Users\user\Documents\compute_cost_ledger\LEDGER.jsonl"
COMMON = r"""
The French SGA 4 (Théorie des topos et cohomologie étale des schémas, Séminaire de Géométrie Algébrique du Bois-Marie
1963-1964, by M. Artin, A. Grothendieck and J.-L. Verdier; Lecture Notes in Mathematics 269, 270 and 305, 1972-1973)
is the LaTeX edition distributed by Fabrice Orgogozo. It was checked page by page against the printed original, and
every correction is an exact edit OLD -> NEW of the French LaTeX. The {LANG} edition is a translation of the same
LaTeX edition, made before these corrections; it keeps the edition's macros, its \pageoriginale page markers and its
\sisi{A}{B} records (A the printed reading, B the reading the edition's editors corrected it to; the {LANG} edition
prints B).

Your batch is below, between BEGIN BATCH and END BATCH. It has one block per printed page: "=== EXPOSÉ <exposé>,
PAGE <page> ===", then the {LANG} text of that page and of its neighbours ("----- {LANG}, file <file>, page <p> -----";
a page of the {LANG} runs from the line of its \pageoriginale marker, which stands after the first word or two of the
printed page; where a file's page breaks are not marked, the whole file is shown), then the French corrections of that
page: "[id X]" with the kind of the correction, OLD, NEW and FRENCH CONTEXT (the corrected French around the
corrected place).

For each id decide:
- "apply": the {LANG} has the error that the French fix corrects. Give an exact {LANG} edit: "tr_file" (as named in
  the block), "tr_old" (an exact substring of that {LANG} text, long enough to occur only once in the {LANG} pages of
  the block) and "tr_new" (the corrected {LANG}). Carry over the meaning of the fix: a corrected formula, index, sign,
  symbol, reference number, number or letter; a missing or wrong word or phrase (translated, never pasted in French); a
  missing or wrong parenthesis, bracket or punctuation mark that belongs to the mathematics or the meaning; a font
  (italic, bold, script letters) that the mathematics depends on.
- "already": the {LANG} already says what the corrected French says.
- "not_applicable": the fix concerns only the French: spelling, accents, French grammar (agreement, tense, a wrong
  French word that the translation renders correctly anyway), French punctuation or spacing, a line or page break, or
  another layout choice of the French that the {LANG} does not follow.
- "unclear": you cannot find the passage or are not sure; say why in "note".

Rules:
- Mathematics must end up identical to the corrected French: same symbols, letters, indices, references and numbering.
- A fix inside a \sisi{A}{B} of the French: make it in the same argument of the matching \sisi of the {LANG}; if the
  {LANG} has no such \sisi, a fix of the printed reading A alone is "not_applicable", and a fix of B (or of both) is
  made in the {LANG} text that the {LANG} prints there.
- Keep the {LANG} edition's conventions, macros, spelling and typography.
- Never change \pageoriginale markers, the keys of \etiquette, \label, \hyperref, \hyperrefext, \eqhyperref, \ref or
  \cite, or file structure.
- If one {LANG} edit covers several ids, put it in the first and give the others "already" with note "covered by <id>".
  No two "apply" edits may overlap.
- Use LF line breaks (\n) in tr_old and tr_new, exactly as in the {LANG} text shown.

Answer with one fenced block ```json containing one JSON list, one object per id, in the batch's order:
  {"id": "X", "decision": "apply"|"already"|"not_applicable"|"unclear", "tr_file": ..., "tr_old": ..., "tr_new": ...,
   "note": "..."}
("tr_file" and "tr_old" for "apply" and "already", "tr_new" only for "apply"; "note" short, and only where useful).
Every id of the batch gets exactly one object. For "already", "tr_old" is the exact {LANG} text (occurring once in the
{LANG} pages of the block) that already says what the corrected French says, so that the decision can be checked.
After the block, one line each: any place where the {LANG} translation itself is wrong in a way the French fix does
not cover (do not fix those). Nothing else.
"""
PROMPTS = {"en": "You carry corrections from the French SGA 4 into the English SGA 4.\n" + COMMON.replace("{LANG}", "English")}


def prompt(target):
    return PROMPTS[target[:2]]


def submit(target, tag, name, effort="high"):
    text = open(os.path.join(HERE, f"batches_{tag}", name + ".txt"), encoding="utf-8").read()
    body = {"model": "gpt-6.1-sol", "input": prompt(target) + "\nBEGIN BATCH\n" + text + "\nEND BATCH\n",
            "reasoning": {"effort": effort}, "max_output_tokens": 128000, "background": True, "service_tier": "flex"}
    code, r = P.call("POST", P.API, body)
    return code, r.get("id"), r.get("error")


def finish(target, name, r):
    text = "".join(c.get("text", "") for o in r.get("output", []) if o.get("type") == "message"
                   for c in o.get("content", []))
    open(os.path.join(HERE, f"answer_{name}.md"), "w", encoding="utf-8").write(text)
    m = re.search(r"```json\s*\n(.*?)```", text, re.S)
    ok = False
    if m:
        try:
            lst = json.loads(m.group(1))
            json.dump(lst, open(os.path.join(HERE, f"decisions_{name}.json"), "w", encoding="utf-8"), ensure_ascii=False,
                      indent=1)
            ok = True
        except ValueError as e:
            print(name, "JSON error", e, flush=True)
    u = r.get("usage") or {}
    usd = (u.get("input_tokens", 0) * 1 + u.get("output_tokens", 0) * 5) / 1e6      # Flex: $1 / $5 per million
    dry = ""
    if ok:
        res = subprocess.run([sys.executable, "-I", "-B", os.path.join(HERE, "apply.py"), target,
                              os.path.join(HERE, f"decisions_{name}.json")], capture_output=True, text=True,
                             encoding="utf-8")
        dry = (res.stdout.strip().splitlines() or [res.stderr.strip()[-300:]])[-1]
    return ok, round(usd, 4), dry, u


def ledger(target, tag, st, effort, work, t0):
    done = [v for v in st.values() if v.get("tokens")]
    tin = sum(v["tokens"][0] or 0 for v in done)
    tout = sum(v["tokens"][1] or 0 for v in done)
    rsn = sum(v.get("reasoning") or 0 for v in done)
    usd = round(tin / 1e6 + tout * 5 / 1e6, 4)
    row = {"id": f"sga4-port-{tag}", "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
           "project": "SGA 4 French scan-check fixes into the translations (sga4_port_20261112)",
           "work": work or f"{tag}: {len(st)} request(s) into {target}",
           "method": "Responses API, Flex tier, background, sga4_port_20261112/run.py", "model": "GPT-6.1 Sol (OpenAI)",
           "effort": effort, "tier": "flex", "requests": len(st), "input_tokens": tin, "output_tokens": tout,
           "reasoning_tokens": rsn, "usd_batch_price": usd, "list_price_usd": round(2 * usd, 4),
           "key": "OpenAI project key (Untitled 1936.md)",
           "basis": "measured: usage of each answer; price 1.0/5.0 per million (Flex)",
           "wall_minutes": round((time.time() - t0) / 60, 1),
           "result": "; ".join(f"{n}: {v.get('status')} {v.get('dry', '')}" for n, v in st.items())}
    with open(LEDGER, "ab") as fh:    # the ledger's newer rows end in CRLF
        fh.write(json.dumps(row, ensure_ascii=False).encode("utf-8") + b"\r\n")
    print("ledger row", row["id"], f"${usd}", flush=True)


def run(target, conc, tag, only=None, effort="high", work=None):
    t0 = time.time()
    sp = os.path.join(HERE, f"state_{tag}.json")
    st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    index = json.load(open(os.path.join(HERE, f"batches_{tag}", "BATCHES.json"), encoding="utf-8"))
    todo = [b["batch"] for b in index if not os.path.exists(os.path.join(HERE, f"decisions_{b['batch']}.json"))
            and (only is None or b["batch"] in only)]
    flying = {n: v["id"] for n, v in st.items() if v.get("status") == "submitted" and n in todo}
    queue = [n for n in todo if n not in flying]
    while queue or flying:
        while queue and len(flying) < conc:
            n = queue.pop(0)
            code, rid, err = submit(target, tag, n, effort)
            if code >= 300 or not rid:
                print(n, "submit failed", code, json.dumps(err)[:200], flush=True)
                time.sleep(60)
                queue.append(n)
                continue
            flying[n] = rid
            st[n] = {"status": "submitted", "id": rid, "t": time.time(), "tries": st.get(n, {}).get("tries", 0) + 1}
            json.dump(st, open(sp, "w", encoding="utf-8"), indent=1)
            print(n, "submitted", flush=True)
        time.sleep(45)
        for n, rid in list(flying.items()):
            code, r = P.call("GET", f"{P.API}/{rid}")
            s = r.get("status")
            if s in ("queued", "in_progress"):
                continue
            del flying[n]
            if s == "completed":
                ok, usd, dry, u = finish(target, n, r)
                st[n].update(status="done" if ok else "bad_answer", usd=usd, dry=dry,
                             tokens=[u.get("input_tokens"), u.get("output_tokens")],
                             reasoning=(u.get("output_tokens_details") or {}).get("reasoning_tokens"),
                             minutes=round((time.time() - st[n]["t"]) / 60, 1))
                print(n, st[n]["status"], f"${usd}", st[n]["minutes"], "min |", dry, flush=True)
            else:
                st[n].update(status=s)
                print(n, s, json.dumps(r.get("error"))[:200], flush=True)
                if st[n]["tries"] < 3:
                    queue.append(n)
            json.dump(st, open(sp, "w", encoding="utf-8"), indent=1)
    cost = sum(v.get("usd") or 0 for v in st.values())
    print(tag, "done; cost", f"${cost:.4f}", flush=True)
    ledger(target, tag, st, effort, work, t0)


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    o = dict(x[2:].split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    run(a[0], int(a[1]) if len(a) > 1 else 1, o.get("tag", a[0]), o["only"].split(",") if "only" in o else None,
        o.get("effort", "high"), o.get("work"))
