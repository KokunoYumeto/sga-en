# English typography transfer handoff

This is an occurrence map for the already sealed translations. It does not authorize changing their mathematical content or their source-boundary macro packets. Apply the mapped wrapper edits in aggregate output, keeping the immutable contribution bases and their original verification hashes.

## Authoritative inputs

- `typography_groups.json`:774 records,387 for each French branch, giving the exact original outer group and its proposed wrapper-only result. Filter by `layer`, then map the source group to its existing translated counterpart.
- `plain_exclusions.json`: the complete local exclusions. Current has6 nested terms,8 plain resp. tokens and21 plain numerical locators; diplomatic has20 locators because the accepted current-only phrase on644 cites3.8.
- `transport_validation.json`: all source/final page hashes, exact notes and math comparisons.
- `typography_counts.json`: per-exposé rule counts and standalone paragraph wrappers.
- `post_review_patches.jsonl`: exact French final-pass anchors; do not apply French prose strings directly to English.

## Scope and punctuation

No new lexical emphasis scope was added outside the existing387 outer emph groups. Four independently source-confirmed lexical words inside mathematical text commands on73–75 retain their existing emphasis scope and change wrapper only. The new final pass does not wrap an already explicit uline group. Existing plain exclusions from earlier local source patches remain plain; this list supplements them rather than replacing them.

Keep full mathematical units literal and outside prose-rule wrappers, retaining any independent symbol rules inside those units. Preserve original notes, note labels, stable targets, and folio marker comments. Keep the same translated words and formula order at all six cross-folio outer groups:44/45,60/61,61/62,631/632,647/648,665/666.

For each mapped lexical piece, the French pass excludes leading/trailing spaces and edge punctuation `.,;:!?()[]«»~`. A piece containing only punctuation remains plain. Internal punctuation is retained inside the previously delimited lexical group. In particular terminal stops and isolated parentheses adjoining mathematical units remain outside the new rule. Do not strip, add, move or reinterpret punctuation bytes in the translated text. Already explicit uline groups retain their local punctuation and source decisions.

Only the six listed nested defining phrases are plain at those definition occurrences. Their reuse elsewhere, such as m-regular in the following616 lemma and special positive k-cycle in658 Lemma6.10, keeps its observed rule. The protection mechanism must therefore be keyed to these exact source groups and their translated anchors. Likewise protect only the eight listed resp. occurrences: the two source X567 resp tokens, groups214 and217, are explicitly ruled and must remain ruled. Other already explicit ruled resp. groups, including I and II, stay intact.

## Complete new plain-exclusion mapping

| Folio | Current group | Kind | Exact source content to keep plain |
|---:|---:|---|---|
| 41 | 62 | plain_references | `2.5` |
| 41 | 62 | plain_references | `2.7` |
| 41 | 62 | plain_references | `2.8` |
| 41 | 62 | plain_references | `2.9` |
| 43 | 70 | plain_resp | `resp.` |
| 43 | 70 | plain_resp | `resp.` |
| 53 | 103 | plain_references | `2.22` |
| 54 | 109 | plain_references | `2.29` |
| 63 | 134 | plain_references | `2.2` |
| 616 | 246 | plain_nested | `$m$-r\'egulier` |
| 619 | 258 | plain_nested | `\((b)\)-faisceau` |
| 621 | 271 | plain_nested | `\((b)\)-polynômes` |
| 621 | 272 | plain_references | `1.9` |
| 639 | 321 | plain_resp | `resp.` |
| 639 | 321 | plain_resp | `resp.` |
| 639 | 321 | plain_references | `4.1` |
| 643 | 328 | plain_resp | `resp.` |
| 644 | 329 | plain_resp | `resp.` |
| 644 | 329 | plain_references | `3.8` |
| 645 | 331 | plain_resp | `resp.` |
| 645 | 332 | plain_resp | `resp.` |
| 653 | 348 | plain_references | `6.1` |
| 653 | 349 | plain_references | `1.9` |
| 653 | 350 | plain_references | `6.1` |
| 654 | 352 | plain_references | `6.1` |
| 654 | 352 | plain_references | `1.9` |
| 655 | 356 | plain_references | `6.1` |
| 656 | 360 | plain_references | `6.1` |
| 657 | 361 | plain_references | `6.1` |
| 658 | 369 | plain_nested | `$k$-cycle positif sp\'ecial de dimension $r$` |
| 658 | 369 | plain_nested | `int\`egre` |
| 658 | 369 | plain_nested | `degr\'e` |
| 660 | 374 | plain_references | `6.1` |
| 662 | 378 | plain_references | `4.6` |
| 664 | 383 | plain_references | `7.1` |

For the defining terms the expected English concepts are m-regular; (b)-sheaf; (b)-polynomials; special positive k-cycle of dimension r; integral; degree. Use the exact already adopted translated phrase, preserving all its literal mathematical tokens and the frozen glossary choice.

## Labels and notes

The77 ordinary standalone numeric paragraph labels per branch lose only their bold wrappers. The source2052.2 belongs to a Proposition label divided by the original author note and remains under NOTE_6 accepted statement-label typography. The source6053.2 is an ordinary paragraph label beside a display, so its English counterpart must use ordinary text weight without changing the display equality. Existing statement labels may retain accepted bold styling; no new rule is required under their numbers.

All111 author-note labels are identical in the French transport. One note body, folio21, has the already source-observed lexical wrapper transport: emph around pre-lambda-ring becomes separate ruled lexical pieces on each side of the literal lambda math. Preserve its note command, original label and every translated word. Other note bodies remain outside this final wrapper pass.

The four lexical mathematical text commands are73 dans,74 avec,75 d'où,75 pour tout. Their translated text wrappers follow the already accepted source observations; every other math-unit byte is unchanged by this convention pass. Source605's paragraph-label wrapper is the additional explicitly documented display-side exception.

## Required aggregate checks

Record the source group index, exact English before/after anchor, occurrence count and hashes for each mapped amendment. Verify no nested/doubled uline wrapper is introduced; all plain defining terms, resp. tokens, locators and existing plain exceptions remain unruled; the two567 resp tokens remain ruled; the111 author-note labels and mathematical contents are preserved. Update the old0/I-only `EN_FONT_RENDERING_RECORD` basis to the actual per-exposé source coverage and these exact mappings. This handoff supplies attributed evidence; it does not claim the English aggregate has already passed those checks.
