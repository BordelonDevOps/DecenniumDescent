"""Package current complete rules and bounded acquisition evidence for GPT."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile
from record_feat_exact_01_acq03_fulfillment import read, info, write_new

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
PREFIX = 'FEAT335_ACQUISITION_AUDIT_01'


def main():
    prep = A / (PREFIX + '_PREPARATION.json')
    packet = A / 'DD_FEAT335_Acquisition_Audit_01.zip'
    root = A / 'feat335-acquisition-audit-01-input'
    assert not prep.exists() and not packet.exists() and not root.exists()
    checkpoint_path = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_WEAPON_PROFILE_CHOICES.json'
    checkpoint = read(checkpoint_path)
    assert info(G / checkpoint['coverageLedger']['path']) == checkpoint['coverageLedger']
    current = R / 'data/public/feat_candidates/exact_01'
    internal = R / 'data/director/feat_candidates/exact_01'
    contract_path = A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    contract = read(contract_path); public = read(current / 'candidate.json')
    records = contract['records']; candidates = {x['id']: (i, x) for i, x in enumerate(public['feats'])}
    assert len(records) == len(candidates) == 335 and {x['id'] for x in records} == set(candidates)
    mismatches = []; unchanged_reviewed = 0
    for i, row in enumerate(records):
        pi, candidate = candidates[row['id']]
        if 'unchangedReviewedRecord' in candidate:
            operative = candidate['unchangedReviewedRecord']['operationalRules']
            unchanged_reviewed += 1
            operative_pointer = f'/feats/{pi}/unchangedReviewedRecord/operationalRules'
        else:
            operative = candidate['operationalRules']
            operative_pointer = f'/feats/{pi}/operationalRules'
        if row['completeOperativeProcedure'] != operative:
            mismatches.append({'id': row['id'], 'contractPointer': f'/records/{i}/completeOperativeProcedure',
                               'publicPointer': operative_pointer})
    assert unchanged_reviewed == 8
    assert not mismatches, mismatches
    partial_path = A / 'FEAT_EXACT_01_PARTIAL_PREREQUISITE_COVERAGE_INDEX.json'
    partial = read(partial_path)
    reports = {G / x['report']['path'] for x in partial['cohorts']}
    reports.update(A / name for name in [
        'FEAT_EXACT_01_ACQUISITION_HISTORY_AFTER_ACQ01_CHECK.json',
        'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', 'FEAT_EXACT_01_PRODIGY_CHOICES_CHECK.json',
        'FEAT_EXACT_01_TRADE_SELECTIONS_CHECK.json', 'FEAT_EXACT_01_HALF_FEAT_CHOICES_CHECK.json',
        'FEAT_EXACT_01_FIXED_MENUS_CHECK.json', 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_CHECK.json',
        'FEAT_EXACT_01_CASTING_SELECTIONS_CHECK.json', 'FEAT_EXACT_01_WEAPON_PROFILE_CHOICES_CHECK.json',
        'FEAT327_ACQ_05_LIFECYCLE_CHECK.json'])
    payloads = {Path(__file__), checkpoint_path, partial_path, contract_path}
    payloads.update(current.glob('*.json')); payloads.update(internal.glob('*.json'))
    payloads.update((R / 'data/public/class_playtests').glob('*.json'))
    payloads.update((R / 'docs/feats/exact-candidate-01').glob('*.md'))
    payloads.update(A / name for name in [
        'FEAT327_ACQ_01_GPT_ADDENDUM.md', 'FEAT327_ACQ_01_DERIVED_FULFILLMENT.json',
        'feat327-acq02-source/FEAT327_ACQ_02_ADDENDUM.md', 'FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json',
        'FEAT327_ACQ_03_GPT_ADDENDUM.md', 'FEAT327_ACQ_03_FINITE_FULFILLMENT.json',
        'feat327-acq04-source/FEAT327_ACQ04_CONTROLLING_ADDENDUM.md',
        'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json', 'FEAT327_ACQ_04_FINITE_FULFILLMENT.json',
        'feat327-acq05-source/FEAT327_ACQ05_CONTROLLING_ADDENDUM.md', 'FEAT327_ACQ_05_FINITE_FULFILLMENT.json',
        'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md'])
    payloads.update(R / ('docs/mechanics/' + name) for name in [
        'CHARACTER_CREATION_PLAYTEST.md', 'CHARACTER_FOUNDATION_TABLES.md',
        'CORE_RESOLUTION_PLAYTEST.md', 'COMBAT_ACTION_PLAYTEST.md',
        'ANCESTRY_BACKGROUND_PLAYTEST.md', 'EQUIPMENT_ACQUISITION_PLAYTEST.md', 'MAXIMUM_HP_PLAYTEST.md'])
    # Evidence remains in its actual historical revision. A newer source binding
    # is NOT silently substituted into an earlier executed report.
    summaries = []; historical_bindings = []
    for path in sorted(reports):
        data = read(path); assert not data.get('failures') and not data.get('failureCount', 0)
        payloads.add(path)
        note = path.with_name(path.name.replace('_CHECK.json', '_NOTES.md'))
        if note.exists(): payloads.add(note)
        summary = {k: deepcopy(data[k]) for k in [
            'createdAtUtc', 'recordedAtUtc', 'status', 'scope', 'checks', 'counts', 'cohort', 'menus',
            'limits', 'remaining', 'all335ActualAcquisitionBoundaryCasesExecuted',
            'doesNotAuthenticatePrerequisiteReceipts', 'fullFeatCandidateApproved', 'candidateReadyForSubmission'] if k in data}
        summary['report'] = info(path); summary['reportIncludedComplete'] = True
        summaries.append(summary)
        for binding in data.get('sourceBindings', []):
            if not isinstance(binding, dict) or 'path' not in binding: continue
            source = (G / binding['path']).resolve()
            assert source.is_relative_to(G.resolve()) and source.is_file(), binding
            payloads.add(source)
            actual = info(source)
            if actual != binding:
                historical_bindings.append({'report': info(path), 'recordedHistoricalBinding': binding,
                    'currentIncludedFile': actual,
                    'meaning': 'Report remains an earlier revision; do not claim it executed against these newer bytes. Consult named addenda/fulfillments.'})
    payloads.update((R / 'tools').glob('feat_exact_01_*.py'))
    payloads.update((R / 'tools').glob('validate_feat_exact_01_*.py'))
    assert all(p.is_file() for p in payloads), [str(p) for p in payloads if not p.is_file()]
    root.mkdir()
    request = '''FEAT335-ACQUISITION-AUDIT-01 — exhaustive acquisition/initial-state review

We are continuing the owner's complete CRPG system specification, retaining the twelve-character expedition, parallel activities and host permissions. Software conversion and human balance testing are later. Actual final joint whole-game flow agreement precedes the already-authorized commit/push, verified remote, careful cosmology review and preservation-based cleanup. Do not reopen completed crafting/language/onboarding/EX58 or ACQ01–05 absent a concrete mismatch.

ACQ05 is fulfilled locally: seven replacements in five files, 272 independent descendant checks and 206 lifecycle checks across all20 named groups/71 traces. The preserved original and old completion-first model remain historical. Subsequent paid-selection passes cover Prodigy; three trade feats; eight half-feats; five fixed martial/metamagic/elemental menus; five skill/tool/language menus; eleven casting choices; and Weapon Focus/Mastery. The latest weapon pass has591 checks/47 histories, all40 reviewed equipment profiles, one actual Monk unarmed Focus witness and two explicitly conditional Troll Claws witnesses. These are limited local reports, not your approval or335 complete acquisitions.

Please inspect the attached current full335 acquisition contracts, complete public/internal candidates, shared rules, full supplements, exact spell dependencies, class/ancestry/equipment sources and complete local reports. PACKAGE_MANIFEST.json binds every byte. START_HERE.json indexes report scopes and historical source-binding differences; those differences must not be mistaken for executed checks against newer source revisions. The 335-row source index supplies navigation, not semantic acceptance. Compare the COMPLETE operative procedures, not keyword hits or only normalized prerequisite trees.

Requested deliverable: one finite, row-by-row acquisition/initial-state audit covering all335 exact IDs. This is a targeted readiness audit of FXC05 and acquisition portions of FXC04, not the final assembled full-feat verdict and not a new generic source-authoring conference.

For EACH ID identify: (a) actual printed/operative acquisition predicates and repeatability; (b) every mandatory permanent selection and fixed snapshot branch, with its real menu/source; (c) initial finite allowances, pools/reserves/empty containers, shared parent-pool behavior, capacity-only changes, ownership without body/item/stock, and any acquisition that must not initialize until a later event; (d) deferred/unavailable or external-source-conditional branches; (e) which attached evidence actually covers each obligation and what remains untested or unestablished. A feat with no new selection/resource still needs an explicit source-based disposition, not omission. Shared-rule-backed groups may avoid redundant work but must enumerate their exact members and per-feat exceptions. Keep use-time costs, clocks, damage and real physical premises distinct from acquisition.

Return machine-readable rows plus a concise finite remaining-work list grouped by actual missing obligation. Do not infer full acquisition completion by adding partial coverage counts. Do not demand actual campaign records merely to exercise already-approved conditional interfaces; equally do not promote a fixture to a real credential. Identify contradictions in the new local models if any. Proposed tests should cover real distinct boundaries and interactions, not repeat thousands of tautological checks. Preserve source permissions rather than reducing the menu to the easiest supported witness.

One concrete classification question needs your source comparison: Weapon Focus expressly admits a specific unarmed profile with an actual proficiency receipt. Weapon Mastery names an actual proficient weapon profile and a specific genuine natural weapon, rejecting umbrella labels. The retained source table places Unarmed strike under Simple melee weapons; reviewed equipment says unarmed is an attack option rather than an inventory object, and the40 physical equipment profiles exclude it. The local pass proves Monk's Simple-training route only for specific unarmed Focus; it leaves specific-unarmed Mastery outside the slice, not illegal. Determine the exact current disposition for a specific proficient ordinary/Monk unarmed profile under Mastery, and whether Troll Claws' express natural-weapon/unarmed wording plus an actual existing training grant establishes exact-profile proficiency or still needs a separate external credential. Do not import outside-game defaults. Cite actual clauses; if a genuinely NEW minimal completion is required, give exact guarded changes, not silent interpretation. Keep unprovided genuine natural profiles as source-qualified possibilities, not a blanket ban or a free proficiency grant.

Likewise check the distinction that Focus explicitly requires ongoing operative proficiency, while Mastery specifies proficiency at acquisition and its own profile/level use predicates. Do not add an ongoing gate absent a controlling clause. Preserve the level6 gate and actual earned opportunities, nonrepeatable Mastery, broadest critical range, natural19 needingAC, and natural20 automatic hit.

Prefer KEEP where complete source already controls. If an ambiguity is found elsewhere, cite the exact current identity/field and propose only its necessary completion. Any new authoring is distinct from your audit conclusions, and no broader candidate promotion follows. Return full source-linked JSON/Markdown and any actual reproduction checker/results in a downloadable ZIP. Mark calculations you actually executed separately from authored expectations. Keep all original objects, historical evidence, status/selection flags, the two null deferred payloads, and every unrelated source unchanged. No cosmology interpretation, deletion, runtime selection, full-game approval or extra owner confirmation is requested.
'''
    request_path = root / 'REQUEST.txt'
    request_path.write_text(request, encoding='utf-8', newline='\n')
    row_index = []
    for i, row in enumerate(records):
        pi, candidate = candidates[row['id']]
        row_index.append({'id': row['id'], 'name': row['name'],
            'contract': {'path': contract_path.relative_to(G).as_posix(), 'pointer': f'/records/{i}'},
            'public': {'path': (current / 'candidate.json').relative_to(G).as_posix(), 'pointer': f'/feats/{pi}'},
            'semanticAcquisitionAuditStatus': 'requested-not-yet-performed',
            'fullAcquisitionProvenByIndex': False})
    index_path = root / 'ALL335_SOURCE_INDEX.json'
    write_new(index_path, {'status': 'literal-navigation-index-only', 'count': len(row_index), 'records': row_index})
    start_path = root / 'START_HERE.json'
    write_new(start_path, {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'reviewId': PREFIX,
        'purpose': 'Exhaustive acquisition/initial-state audit; not final whole-feat review or promotion.',
        'request': info(request_path), 'sourceIndex': info(index_path), 'currentCheckpoint': info(checkpoint_path),
        'currentContractPublicFullTextParity': {'recordsCompared': 335, 'mismatches': []},
        'evidenceReports': summaries, 'historicalBindingsWhoseCurrentBytesDiffer': historical_bindings,
        'sourceBindingDifferencePolicy': 'Preserve old report bytes and actual measured current files separately; no rerun/current-version claim follows.',
        'completeAcquisitionClaimed': False, 'newRuleAdoptions': 0, 'sourceInformationDeleted': False})
    payloads.update({request_path, index_path, start_path})
    manifest = {p.relative_to(G).as_posix(): info(p) for p in sorted(payloads)}
    with zipfile.ZipFile(packet, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(payloads): z.write(p, p.relative_to(G).as_posix())
        z.writestr('PACKAGE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None and len(z.namelist()) == len(manifest) + 1
        for name, bound in manifest.items():
            raw = z.read(name)
            assert len(raw) == bound['bytes'] and sha256(raw).hexdigest() == bound['sha256']
    assert all(info(G / name) == bound for name, bound in manifest.items())
    write_new(prep, {'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'prepared-and-byte-verified-not-yet-submitted', 'id': PREFIX,
        'request': info(request_path), 'startHere': info(start_path), 'sourceIndex': info(index_path),
        'archive': info(packet), 'payloads': len(manifest), 'completeReportsIncluded': len(reports),
        'currentFullProcedurePairsCompared': 335, 'historicalBindingDifferencesRecorded': len(historical_bindings),
        'sourceInformationDeleted': False, 'newRuleAdoptions': 0, 'fullCandidateApproved': False})
    print(json.dumps({'preparation': info(prep), 'archive': info(packet), 'payloads': len(manifest),
        'reports': len(reports), 'historicalBindingDifferences': len(historical_bindings)}, indent=2))


if __name__ == '__main__':
    main()
