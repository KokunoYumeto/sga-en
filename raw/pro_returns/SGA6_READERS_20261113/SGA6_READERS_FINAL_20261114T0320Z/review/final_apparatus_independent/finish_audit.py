#!/usr/bin/env python3
"""Package the completed occurrence audit without editing production inputs."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SNAP = HERE / "input_snapshot"


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def readable_spacing(text):
    # These are newly written audit sentences, never source or variant bytes.
    return re.sub(r"\b(All|all|The|the|every|remaining|observed|captured|giving|comprise|and|on|page|for|in|exact|both|after|before|under|counts|record|finding|reference|from|de|to)(?=\d)", r"\1 ", text)


CASES = {
    "FRV0061": dict(
        issue="wrong occurrence of the same spelling correction",
        wrong_source_ids=["check/findings/findings_011_015.json#25"],
        required_source_ids=["fixes/MISPRINTS_6.json#62"],
        equivalent_source_ids=["check/findings/findings_011_015.json#32"],
        note="This occurrence is équivalence rationelle in the last body paragraph. Finding25/M59 concern the earlier cohomologie rationelle in FRV0058. The complete sentence location, rather than the identical word pair, selects finding32/M62.",
        discovery="Independent confirmation of a coordinator-flagged ambiguous pair."),
    "FRV0271": dict(
        issue="wrong occurrence of the same reference-digit correction",
        wrong_source_ids=["check/findings/findings_256_260.json#14"],
        required_source_ids=["check/findings/findings_256_260.json#20"],
        equivalent_source_ids=[],
        note="The variant occurs in the proof phrase appliquer (4.8) avec Y=S,F=O_S. Finding20 identifies that substitution in4.9: f!O_S=K_X and RHom(E,f!O_S)=D_X(E). Finding14 concerns the earlier corollary and its E=O_X evaluation map; it belongs to FRV0270.",
        discovery="Independent occurrence check."),
    "FRV0426": dict(
        issue="one wrapper component linked to a different mathematical-letter occurrence",
        wrong_source_ids=["ASTRA-VI-GLYPHS-372"],
        required_source_ids=["ASTRA-VI-ALGEBRA-RULE-372"],
        equivalent_source_ids=[],
        note="The two inserted wrapper pieces enclose the first B after est isomorphe comme. ALGEBRA-RULE-372 supplies that complete B-to-underlined-B correction and the identity algebra action b·[l]=[bl]. The page-wide GLYPHS-372 patch expressly preserves that first B plain and adds a closing brace at another B. Its short B-plus-text-command match cannot source this closing brace.",
        discovery="Independent component-scope check."),
    "FRV0485": dict(
        issue="notation locator linked to a different basis locator on the same page",
        wrong_source_ids=["ASTRA-VI-FLAG-BASIS-REFERENCE-397"],
        required_source_ids=["ASTRA-VI-FLAG-NOTATION-REFERENCE-397"],
        equivalent_source_ids=[],
        note="The phrase is notation de3.5, corrected to4.5, which defines the canonical quotients and kernels and their classes xi_i. BASIS-REFERENCE-397 identifies the distinct corollary3.4-to4.4 basis assertion at FRV0495. The shared character pair3-to4 does not identify the same reference.",
        discovery="Coordinator/early-reviewer finding independently confirmed; already corrected in the initial84-row manual snapshot."),
    "FRV0745": dict(
        issue="two parts of one pivot-index correction split across different source occurrences",
        wrong_source_ids=["check/findings/findings_556_560.json#17"],
        required_source_ids=["ASTRA-X-0093"],
        equivalent_source_ids=[],
        note="The complete first-pivot expression is c=c_{h,1,lambda}, corrected to c=c_{2,h,lambda} under s'=sc. ASTRA-X-0093 explicitly supplies that change. Finding17 concerns the later left/right clearing clause, whose left c_{i,1,lambda} changes to c_{1,i,lambda}; it does not supply deletion of ,1 in this first-pivot occurrence. Both character pieces therefore belong to0093.",
        discovery="Independent compound-source check beyond the initial weak-context list."),
    "FRV0768": dict(
        issue="missing separately adjudicated component source in a compound variant",
        wrong_source_ids=[],
        required_source_ids=["ASTRA-X-REF-580-POSTFREEZE", "fixes/MISPRINTS_6.json#501"],
        equivalent_source_ids=["check/findings/findings_576_580.json#17"],
        note="The minimal pair15)-to14 combines the locator7.15-to7.14 with deletion of the excess closing parenthesis. The reference amendment explicitly reserves the parenthesis as a separate source correction. M501/finding17 count the earlier closed parenthesis and the single opening before cf., leaving one excess closer. The reference amendment supplies the exact cycle-specialization map; both records are required for this combined alternative.",
        discovery="Independent review of a ten-character-context match and the source's explicit scope exclusion."),
    "FRV0773": dict(
        issue="localization bar linked to the following residue-field bar",
        wrong_source_ids=["fixes/FIXLOG_6_CURRENT.jsonl#507"],
        required_source_ids=["fixes/MISPRINTS_6.json#493"],
        equivalent_source_ids=["check/findings/findings_581_585.json#12"],
        note="This formula is B_i=(bar A_i)_{m_i}, whose localization map sends a to a/1. M493/finding12 identify precisely that occurrence. FIXLOG507/M494/finding13 concern the following residue field k_i=bar A_i/m_i and its localization-induced residue isomorphism; that separate correction belongs to FRV0774.",
        discovery="Independent occurrence check."),
}


GROUP_NOTES = [
    "The two inserted e endings belong separately to adopté/M27 and tiré/M31; the exact words select the two existing manual links.",
    "M51 expressly locates both naif subscripts: comme un élément de and de préférence à. One record covers both occurrences.",
    "The first cohomologie occurrence uses finding25/M59; the later équivalence occurrence requires finding32/M62. FRV0061 is corrected explicitly.",
    "The first bare citation has the exact FIXLOG342 anchor dans[6])est faite par Kleiman. The later C-07 citation is finding5. Both target FGA entry5 but occupy separately located phrases.",
    "ASTRA-I-S-089-PROP expressly enumerates these three site-S occurrences and preserves the plain object S. Its scope covers all three variants.",
    "The three category-C occurrences use the existing manual M125/M126/M127 links in order. The site-S source listed by the candidate diagnostic is excluded from all three effective links.",
    "M119 expressly covers the first two plain category-C occurrences in Lemma1.4.2. Both existing manual links use it; the candidate site-S record is excluded.",
    "FRV0180 closes the middle Tr(D(C)) clause under M145; FRV0181 closes the final Tr(K^b(C_0)) clause under finding35. The separate positions are preserved.",
    "Finding8 supplies the exposé identifier for amplitude definition4.8; finding9 supplies it for perfect-subcategory notation4.9. Each exact reference has its own source.",
    "ASTRA-II-PAREN-189 expressly counts the excess closer in each of the two adjunction parentheticals, so it covers both removals.",
    "The corollary and proof have distinct substitutions and source records. FRV0270 remains finding14; FRV0271 now uses finding20.",
    "Finding10 and M238 are explicit aliases for the same citation containing two missing closes. Their reason identifies both insertion positions, after III6 and after the IV3.1.0 citation.",
    "M252 expressly covers the second display tag and both following references. Its beta map and alpha-tensor-beta comparison identify the common3.2.3.1 target in all three places.",
    "ASTRA-V-POLYNOMES-361 explicitly locates the opening polynomial paragraph and the last sentence of7.3, covering both bare-o spellings.",
    "The Gl source enumerates all seven double-rule group-scheme occurrences and thirteen single-rule group-sheaf occurrences. Both unary representation-ring units are in its double-rule scope.",
    "The same explicit seven-occurrence Gl inventory includes both factors in each of these two product representation-ring units; no single-rule occurrence is substituted.",
    "The394 flag-operator record covers all D_pi operators on the folio, including the two complete identical units in this group.",
    "The notation reference and basis reference have distinct effective links after the FRV0485 override; FRV0495 retains its basis source.",
    "The397 projective-operator record covers all nine P letters, including each of these four identical P(E) units.",
    "The397 D/G record counts four D letters, including the two D(F) units and the two diagram D letters.",
    "The same nine-P inventory expressly includes the P subscript and diagram as well as these three K(P(E)) units.",
    "The398 D/G record counts seven D letters and covers both D(E) units in this group.",
    "The same seven-D inventory covers all four K(D(E)) units in this group.",
    "FLAG-SPLITTING-REFERENCES-398 expressly corrects both3.5 and3.7 to4.5 and4.7, identifying the kernel construction and the invertible-factor classes separately within one source record.",
    "DOUBLE-OPERATORS-399 counts five G letters and includes both G_S^{n,r} units here.",
    "DOUBLE-OPERATORS-400 counts nine G letters and includes both K(G_S^{n,r}) units here.",
    "VII0023 records four S(E) double-rule occurrences on425. Its exact count and symmetric-algebra construction cover these three identical units and the fourth nonidentical unit.",
    "VII0029 records six S occurrences on428. The three S(E_0) units lie within that explicit occurrence count.",
    "The same six-S record covers both S(E) units; it does not alter the separately observed E/E_0 rules.",
    "VII0055 has explicit L count2 despite its terse first-occurrence region label; VII0056 has R count3. The actual patches cover both identical L/R units. No second L correction is inferred from the label alone.",
    "VII0072 and0073 record two L and two R glyphs respectively. Their patches and counts cover both Lf*(Ri*M) units.",
    "VII0076 records four projective P letters and includes both identical P_X^{d-1} units.",
    "VIII0087 records eight symmetric-algebra S letters on494, including these two identical units and the remaining displayed occurrences.",
    "Bibliography entry3 and entry5 use separate FIXLOG556 and557 records. Each doubled stop remains attached to its own author-initial occurrence.",
    "The I4.7 and I4.8 index entries use separate findings2 and3, respectively. Each missing opening parenthesis is located by its own index locator.",
]


EXTRA_EXPLICIT = {
    "FRV0077": "The lower i on x is the sole changed index; the independent lower summation bound is preserved.",
    "FRV0119": "M97 expressly corrects both E_i indices in the author-note unit to the already bound E_j family; xi_i remains unchanged.",
    "FRV0120": "The sole delta supplies the K rule. The separately discussed G(A) target is byte-identical in both alternatives.",
    "FRV0138": "Only astériques changes to astérisques. The separately adjudicated raised/lowered author-note stars are identical in both alternatives.",
    "FRV0160": "The complete display changes only the v_i expression to the finite composite recorded by COMPOSITION-094; the separate u'_i formula is unchanged.",
    "FRV0212": "Only the spurious .1 in the locator is removed. The source's separately discussed C_0=Lib wording does not enter this variant.",
    "FRV0360": "COEFFICIENT-PARAMETER-336 expressly covers the displayed first R_(n,a) occurrence; the changed parameter is epsilon(a).",
    "FRV0361": "The same336 record expressly includes the following prose R_(n,a) occurrence, so the second use has direct scope support.",
    "FRV0393": "Only the prime placement in the first universal-element relation changes. The separately recorded final augmentation/filtration issue is absent from this alternative.",
    "FRV0657": "This2. insertion is the first diff piece of the one reference1.5.1-to2.1.1, explicitly sourced to FIXLOG460; the paired deletion is FRV0658.",
    "FRV0658": "This.5 deletion is the second diff piece of the same reference1.5.1-to2.1.1. The exact adjacent source locator confirms the shared FIXLOG460 attribution.",
    "FRV0792": "The whole diagram differs only by the prime on X_i. The replay's separate coproduct-index removal is already common to both alternatives and is not an apparatus delta.",
}


def main():
    mechanics = read(HERE / "MECHANICAL_VALIDATION.json")
    assert mechanics["mechanical_passed"] == 970 and not mechanics["failed"]
    all_rows = read(HERE / "all_970_mechanical_audit.json")
    byid = {r["variant_id"]: r for r in all_rows}
    decisions = read(HERE / "resolved_decisions.json")
    decisions.update(read(HERE / "additional_resolved_decisions.json"))
    original = read(SNAP / "records/FR_APPARATUS_SOURCE_LINKS.json")["variants"]
    manual_rows = [json.loads(s) for s in (HERE / "manual_links_at_validation.jsonl").read_text().splitlines()]
    manual = {r["variant_id"]: r for r in manual_rows}
    contexts = read(HERE / "diplomatic_variant_contexts.json")
    current_contexts = read(HERE / "current_variant_contexts.json")
    repeats = read(HERE / "repeated_full_variant_pairs.json")
    assert len(repeats) == len(GROUP_NOTES) == 35

    discrepancies = []
    for vid, data in CASES.items():
        base = byid[vid]
        assert base["effective_source_ids"] == data["required_source_ids"], (vid, base["effective_source_ids"])
        discrepancies.append(dict(
            variant_id=vid, page=base["page"], issue=data["issue"], discovery=data["discovery"],
            printed=base["printed"], corrected=base["corrected"],
            sha256_printed=base["sha256_printed"], sha256_corrected=base["sha256_corrected"],
            captured_report_source_ids=base["cached_source_ids"], wrong_source_ids=data["wrong_source_ids"],
            required_source_ids=data["required_source_ids"], equivalent_source_ids=data["equivalent_source_ids"],
            exact_diplomatic_context=contexts[vid], exact_current_context=current_contexts[vid],
            occurrence_reason=readable_spacing(data["note"]), source_decisions=[decisions[s] for s in data["required_source_ids"]],
            status="resolved in the observed 90-row manual stream; regeneration checked separately",
            text_change=False, source_decision_change=False,
        ))
    write("DISCREPANCIES.json", discrepancies)

    group_audit = []
    for i, (group, note) in enumerate(zip(repeats, GROUP_NOTES), 1):
        group_audit.append(dict(group_number=i, page=group["page"], variant_ids=group["ids"],
            exact_printed=group["printed"], exact_corrected=group["corrected"],
            diagnostic_candidate_sources=group["selected_sources"],
            effective_links={vid: byid[vid]["effective_source_ids"] for vid in group["ids"]},
            source_contexts={vid: contexts[vid] for vid in group["ids"]},
            verdict="supported after the explicit listed manual corrections", occurrence_reason=readable_spacing(note)))
    write("REPEATED_PAIR_AUDIT.json", group_audit)

    reviewed = {r["variant_id"] for r in all_rows if r["risk_flags"] or len(r["effective_source_ids"]) > 1}
    supplemental = set()
    for variant in original:
        for component in variant["component_proofs"]:
            corr = component["selected_correspondence"]
            is_component = corr.get("proof") != "one exact source-pair replacement reconstructs this whole branch variant"
            if (is_component and corr.get("literal_context_characters", 10000) < 15) or len(corr["source_pair_printed"]) <= 5:
                supplemental.add(variant["variant_id"])
    reviewed |= supplemental | set(EXTRA_EXPLICIT)
    group_for_id = {vid: g for g in group_audit for vid in g["variant_ids"]}
    semantic = []
    for vid in sorted(reviewed):
        item = byid[vid]
        sources = [decisions[sid] for sid in item["effective_source_ids"]]
        note = (CASES[vid]["note"] if vid in CASES else EXTRA_EXPLICIT.get(vid) or
                group_for_id.get(vid, {}).get("occurrence_reason") or
                ("The manual whole-alternative link was independently compared with the exact body context, literal delta, and resolved source region/reading. " + manual[vid]["reason"] if vid in manual else
                 "The exact source region and printed reading below were compared with this variant's complete alternative and neighboring sentence. The selected source covers this occurrence and its recorded delta; a matching character pair alone was not used as the occurrence justification."))
        semantic.append(dict(variant_id=vid, page=item["page"], verdict="supported with effective source IDs",
            risk_flags=item["risk_flags"] + (["additional_compound_source_check"] if len(item["effective_source_ids"]) > 1 else []) +
                       (["extended_short_context_check"] if vid in supplemental else []) +
                       (["explicit_separate_scope_check"] if vid in EXTRA_EXPLICIT else []),
            effective_source_ids=item["effective_source_ids"], printed=item["printed"], corrected=item["corrected"],
            exact_diplomatic_context=contexts[vid], exact_current_context=current_contexts[vid],
            occurrence_reason=readable_spacing(note), attributed_source_decisions=sources,
            new_scan_inspection_claim=False,
            basis="Independent attribution audit of already resolved source evidence; no new full-page collation or mathematical theorem is claimed."))
    write("OCCURRENCE_AUDIT.json", semantic)

    expected = [{k: r[k] for k in ("variant_id", "page", "printed", "corrected", "sha256_printed", "sha256_corrected", "effective_source_ids")} for r in all_rows]
    write("EXPECTED_REGENERATED_LINKS.json", expected)

    code_dir = HERE / "code_at_handoff"
    code_dir.mkdir(exist_ok=True)
    code_changes = []
    for name in ("fr_readable_apparatus.py", "fr_source_links.py"):
        source = ROOT / "scripts" / name
        target = code_dir / name
        shutil.copy2(source, target)
        old = (SNAP / "scripts" / name).read_text()
        new = target.read_text()
        diff = "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                    fromfile="input_snapshot/scripts/" + name, tofile="code_at_handoff/" + name))
        (HERE / (name + ".diff")).write_text(diff)
        code_changes.append(dict(path="scripts/" + name, original_sha256=sha(old), final_sha256=sha(new),
             comparison="Only source-error classification supplement transport changed after capture; literal candidate selection and manual precedence are unchanged."))

    code_audit = dict(
        code_versions=code_changes,
        observed_guards=["Exact ordered970 ID/page/printed/corrected match against the candidate cache.",
                         "Exact manual alternative bytes and SHA-256 match before manual precedence.",
                         "Resolved source has image, reason, accepted verdict, and matching folio.",
                         "Every automatic character edit has a selected literal proof."],
        occurrence_limitation="Whole replacement uniqueness is tested inside the minimal variant, not across source occurrences on the folio. Literal-component matching measures local character context and can select a hunk from another occurrence. The first-match score and source-ID tie break do not establish occurrence identity.",
        compound_limitation="A single character-diff component may combine edits from two independently adjudicated source issues, as the5)-to4 component in FRV0768. A full-pair source string can reconstruct both while its reason expressly authorizes only one. Source scope must therefore be checked in addition to literal reconstruction.",
        context_serialization="For a component, common_left_literal/common_right_literal store the printed-branch strings; their length is the minimum of two branch-specific matching lengths. The auditor checked each branch against its own source-pair context, without assuming the two neighboring branch strings are identical.",
        resolution="The seven explicit manual whole-alternative links retain the same exact variant alternatives and choose the correct occurrence sources. No builder or source decision was changed by this audit.",
        recommendation="Retain the occurrence-specific manual links and their exact hashes. Future regeneration with changed alternatives should fail the existing assertions and require renewed occurrence review rather than accepting a short-pair match as sufficient provenance.",
    )
    write("CODE_AUDIT.json", code_audit)
    summary = dict(variants=970, exact_text_and_hash_checks_passed=970, body_location_checks_passed=1940,
        automatic_components_checked=1238, original_manual_links=83, initial_manual_snapshot_links=84,
        final_manual_links=len(manual), final_manual_sha256=mechanics["latest_manual_sha256"],
        targeted_occurrence_variants=len(semantic), remaining_variants_mechanical_and_resolved_provenance_checks=970-len(semantic),
        repeated_whole_pair_groups=35, repeated_whole_pair_variants=79,
        under_six_literal_context_variants=41, ambiguous_short_pair_variants=48,
        captured_report_issues=7, issues_already_overridden_at_initial_manual_capture=1,
        additional_overrides_during_audit=6, unresolved_identified_issues=0,
        fresh_scan_views=0, mathematical_recollation=False,
        source_text_changed=False, source_decisions_changed=False, sealed_inputs_changed=False,
        regenerated_output_status="Use verify_regenerated.py after the coordinator rebuild; this package verifies the observed 90-row manual stream against the captured 970 alternatives.")
    regenerated_path = HERE / "REGENERATED_VALIDATION.json"
    if regenerated_path.exists():
        regenerated = read(regenerated_path)
        assert regenerated["status"] == "passed" and not regenerated["errors"]
        summary["regenerated_output_status"] = "Passed: the observed regenerated report and variants retain all 970 exact alternatives and all expected effective source IDs."
        summary["regenerated_validation"] = "REGENERATED_VALIDATION.json"
        summary["regenerated_observed_files"] = regenerated["observed_files"]
    write("AUDIT.json", summary)

    lines = ["# Independent audit of French apparatus provenance\n",
        "The captured apparatus contains **970 exact alternatives**. All970 pass the independent ID, folio, text, SHA-256, TSV, resolved-source, and literal-correspondence checks; both body locations pass, giving1,940 location checks. The audit identified seven occurrence-attribution or compound-source issues. All seven are resolved in the observed90-row manual-link stream. The French alternatives and the underlying source decisions were not changed.\n",
        "## Seven resolved issues\n",
        "| Variant | Folio | Captured-report issue | Effective source |\n|---|---:|---|---|\n"]
    for row in discrepancies:
        lines.append(f"| {row['variant_id']} | {row['page']} | {row['issue']} | " + "; ".join("`" + s + "`" for s in row["required_source_ids"]) + " |\n")
    lines += ["\nThe397 notation/basis mismatch had already been identified by the coordinator and early reviewer and was present as an override in the initial manual snapshot. The other six required additional overrides during this audit. Complete exact alternatives, contexts, source reasons and the original versus corrected source lists are in `DISCREPANCIES.json`.\n",
        "## Scope and evidence\n",
        f"The occurrence pass covers **{len(semantic)} distinct alternatives**. It includes all41 variants with an automatically selected literal context shorter than six characters, all48 variants with multiple short-pair candidate sources, all35 repeated complete-pair groups (79 variants), every manual whole-alternative link, compound-source alternatives, the additional short-context/tiny-pair cases, and the listed explicit source-scope exclusions. `OCCURRENCE_AUDIT.json` retains an individual row with exact neighboring text and the attributed source records for each reviewed alternative.\n",
        f"The remaining{970-len(semantic)} alternatives received the exact-text, hash, location, character-edit and resolved-provenance checks. This is a provenance-selection audit of existing reviewed evidence. It does not claim a fresh scan collation or a new mathematical proof for each of the970 source corrections. No new source image was certified.\n",
        "The repeated-pair checks confirm the two page12 naif subscripts under M51; distinguish the two page17 citations; confirm M252's explicit coverage of the display tag and both later references on293; and retain the counted page-wide operator records where their scope really covers multiple occurrences. The page89 and93 category-C manual links remain distinct from the adjacent site-S records. Full group-by-group reasons appear in `REPEATED_PAIR_AUDIT.json`.\n",
        "## Literal and positional checks\n",
        "The saved French bodies were captured after the49 numeric-heading font declarations had been added, whereas the970 cached offsets preceded that supplement. The auditor inverted only those exact49 declarations in each branch **in memory**. All970 offsets then matched in both branches. No source file was rewritten; `context_alignment.json` records the body hashes and the98 exact inversions.\n",
        "The captured automatic proofs comprise803 whole-pair reconstructions and435 literal-component correspondences. All were independently replayed. Each character delta is covered. The manual stream is checked against the same exact alternatives and hashes. The source records retain accepted dispositions, matching folios, scan references and their own reasons. The TSV alternatives and source lists match the captured JSON exactly.\n",
        "## Code assessment\n",
        "The existing builder's exact cache/manual assertions are effective safeguards. Its automatic scores establish literal correspondence, but a minimal3-to4 or one-brace hunk can come from another occurrence on the same page. A compound diff can also merge two independent changes into one character component. The seven explicit whole-alternative overrides address these observed cases without broadening source scope.\n",
        "The component report stores the printed neighboring literal strings and a context length common to two separate branch comparisons. The independent validator checks each branch against its own source-pair strings; it does not assume neighboring text is identical between branches. The later code changes observed during this audit only add explicit source-error classification supplements; the literal-selection and manual-precedence logic is unchanged. `CODE_AUDIT.json` and the two saved code diffs document this.\n",
        "## Handoff\n",
        "`EXPECTED_REGENERATED_LINKS.json` fixes all970 alternatives and their effective source IDs. Run `python review/final_apparatus_independent/verify_regenerated.py` after rebuilding the French apparatus. That read-only check compares the regenerated report and variants with this exact expectation and writes only its audit result here. The original capture remains unchanged under `input_snapshot/`.\n",
        "No French source text, source decision, frozen review, contribution, or checkpoint was modified by the audit.\n"]
    if regenerated_path.exists():
        lines += ["\n## Regenerated output verified\n",
                  "The coordinator's rebuilt report and variants have now passed `verify_regenerated.py`: all970 exact alternatives, hashes, folios and effective source lists match the sealed expectation, with90 manual links and zero unresolved entries. `REGENERATED_VALIDATION.json` records the exact observed file hashes.\n"]
    document = readable_spacing("\n".join(lines))
    document = re.sub(r"(?m)(^\|.*\|)\n\n(?=\|)", r"\1\n", document)
    document = document.replace("The 397 notation/basis", "The page 397 notation/basis").replace("minimal3-to4", "minimal 3 → 4")
    (HERE / "AUDIT.md").write_text(document)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
