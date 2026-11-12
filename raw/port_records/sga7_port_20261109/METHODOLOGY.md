# Methodology: sga7_port_20261109

## Model provenance, 10-12 November 2026

- Merge of Codex's later English SGA 7 I components (MERGE_CODEX_EN7I.md; pushed to sga-en as b5ff265): Claude Opus 5.5 subagent, high effort. The components themselves: OpenAI Codex sessions (September).
- Port rounds 1-4: GPT-6.1 Sol (OpenAI API, reasoning effort high, Flex tier) for the translations of the fixes; scripts by Claude Opus 5.5.
- Round 5 (12 Nov): no model call. Claude Opus 5.5 (subagent) chose and checked every edit by hand; most edits are Sol's own decisions of rounds 1-4 that apply.py could not make.

## Round 5: the leftovers, by hand (12 Nov 2026)

Rounds 1-4 left 20 items in PORT_<TARGET>_LEFT.json (en7I 2, en7II 2, es7I 8, es7II 8). Their decisions were right; apply.py refused them for one of four reasons, and none needed a new model call:

- **No page window.** The terminal publisher catalogue (French pp. 525-528) is no longer input by the readers (sga-en a5ec69b, sga-es dcdcf00), so segment.py finds no segment for those pages: en7I C1002, C1003; es7I C1000-C1005. Sol's edits go into the catalogue files directly.
- **Two occurrences in the window.** en7II C151 (Cor. 1.3.2 (i) and (ii) of XV): the edit goes to (ii), where the French fix is; es7II B174 is unique now that B176 is applied.
- **Overlap with an edit of the same batch** that is now applied: es7II B447 (after B446), D580 (after B474).
- **A \sisi that the French fix collapses** (both French layers now read the same): es7II D4, D721, D742, D762, C884, as for D654 and D665 on 10 Nov.
- **tr_old off by a blank line:** en7II C77 (the \mathfrak X, \mathfrak D edit of XIV 1.4.1-1.4.2); make_hand_r5 asserts that the edit equals Sol's apart from that line.
- es7I D654 and D665 were applied by hand on 10 Nov; round 5 only checks that they are in place.

Fourteen catalogue fixes beyond the 20 went in with them, so that both catalogues follow the corrected French: en7I C1000, C1001, C1004, C1005 (Sol had judged them not applicable to the English, while the English catalogue keeps titles in their original language and Sol applied C1002 and C1003 there), and the fixes of p. 526, which no round could send (no target text in the window): en7I C1012, C1013, C574, C601, C602; es7I C1012, C1013 (as \sisi{print}{corrected}), B574, B601, B602.

Tools: apply_hand.py applies HAND_R5.json (built by a script from the LEFT lists and the hand entries) with the checks of apply.py (tr_old exactly once in the named file, brace balance, page markers, label and link keys, overlaps, \sisi removal only where the entry says "collapse"). Each edit is logged in PORT_<TARGET>_LOG.jsonl with batch "hand_r5"; the LEFT lists before round 5 are kept as PORT_<TARGET>_LEFT_before_r5.json and the LEFT lists are now empty.

Result: all six builds compile (en7I 289 pages, en7II 266, es7I 322 in both editions, es7II 277 in both editions). Pushed: sga-en 07aadf2 (7 I), 202e743 (7 II); sga-es 0a91119 (7 I), c42c103 (7 II). No release was cut.

Still open: 19 decisions of rounds 1-4 were "unclear" (en7I C82, C874, C713; en7II C8, C17, C138, C475, C508; es7I B80, B82, D130, C874; es7II B0, B8, D517, C508, C574, C822, C823). Most come from page windows that did not hold the passage; they need a round with the right pages. In XV Cor. 1.3.2 (i) the English underlines "$S$-" where the French does not; no French fix covers it.
