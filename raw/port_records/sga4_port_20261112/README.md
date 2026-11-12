# SGA 4: the French scan-check fixes into the translations (set up 12 Nov 2026)

The pattern of `sga7_port_20261109` (SGA 7), set up for SGA 4: the fixes that the scan check of 11 Nov made in the
French SGA 4 are carried into the translations by GPT-6.1 Sol (OpenAI API, reasoning effort high, Flex tier), batch by
batch, and every proposed edit is checked mechanically before anything is written.

**State: pilot only.** The pilot (20 fixes into the English, 12 Nov, $0.09) ran and was checked by hand: 20 of 20 decisions right (`PILOT_REVIEW.md`). Nothing
is applied to any translation and nothing is published; `apply.py` has writing switched off until the user approves
the port.

| File | What |
|---|---|
| `METHODOLOGY.md` | Sources of record, which fixes are final, the trees that carry SGA 4, the method, model provenance, cost |
| `PILOT_REVIEW.md` | The verdict on each pilot item and the recommendation |
| `final.py` → `FINAL_4.json` | Every French fix with its status: final, on a page of the in-app recheck, or not yet in the corrected layer |
| `segment.py` | The English SGA 4 cut into the printed pages of the French (page markers, fragment by fragment) |
| `pick_pilot.py` → `PILOT_IDS.json` | The 20 pilot fixes, drawn at random (seed 20261112) by kinds |
| `build.py` → `batches_<tag>/` | The batch text (English pages and French fixes) and `ITEMS.json` |
| `run.py` | Sends the batches to Sol, saves `answer_<batch>.md` and `decisions_<batch>.json`, writes the ledger row |
| `apply.py` → `CHECK_<decisions>.json` | Checks each decision (dry run only) |
| `compile.py` | Builds the English SGA 4 with XeLaTeX (for after an approval) |

Order: `final.py`, `pick_pilot.py`, `build.py en4 120 --max-kb=500 --tag=en4_pilot --ids=<PILOT_IDS>`,
`run.py en4 1 --tag=en4_pilot`, then the hand review.
