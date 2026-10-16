"""Preserve and audit GPT's first Banishment return; do not adopt its rules."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def main():
    out = A / 'banishment-current-review-01-return'
    audit = A / 'BANISHMENT_CURRENT_REVIEW_01_LOCAL_AUDIT.json'
    request = A / 'BANISHMENT_REPAIR_02_REQUEST.txt'
    assert not audit.exists() and not request.exists()
    inputs = read(A / 'banishment-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    model = read(out / 'SPELL_MODEL.json')
    cases = read(out / 'CASEBOOK.json')['cases']
    sources = read(out / 'SOURCE_HASHES.json')
    manifest = read(out / 'EVIDENCE_MANIFEST.json')
    checks = []

    def check(label, ok):
        checks.append({'check': label, 'pass': bool(ok)})

    check('49 returned bindings equal the frozen input bindings', sources['bindings'] == inputs['sourceBindings'] and len(sources['bindings']) == 49)
    for b in sources['bindings']:
        raw = (G / b['path']).read_bytes()
        check('source length and SHA256: ' + b['path'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    for b in manifest['files']:
        raw = (out / b['name']).read_bytes()
        check('output length and SHA256: ' + b['name'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    check('complete ordinary source/access object preserved', model['sourceAndAccess'] == inputs['sourceCard'])
    check('all thirty requested case IDs exactly once', [c['id'] for c in cases] == [f'BAN-C{i:02}' for i in range(1, 31)])
    for original in inputs['originalAuthoredExamples'] + inputs['additionalReviewScenarios']:
        returned = next(c for c in cases if c['id'] == original['id'])
        check(original['id'] + ' historical scenario preserved', returned['historicalSourceScenario'] == original)
    check('all ten review question IDs', [q['id'] for q in model['questionDispositions']] == [f'BAN-{i:02}' for i in range(1, 11)])
    findings = [
        {
            'id': 'BAN-R02-01', 'severity': 'adoption-blocking',
            'location': 'SPELL_MODEL.json /procedure/closure/placement and /blockers; Player and Director closure sections',
            'finding': 'The search ends at 120 ft and the last-resort exception ignores transport prevention only. No terminal outcome exists if there is no physically fitting candidate in that volume. Ordinary collapse/filled space or a larger created visitor can cause this without erasing a plane. If the otherwise-physically-legal set is empty, ignoring blockers cannot produce a legal space. Calling the module complete is therefore unsupported.',
            'requiredCorrection': 'Supply a finite, fully specified physical-exhaustion branch with a valid terminal state for every extant body/object, or explicitly revise the admitted state space so this case is provably impossible. Do not turn it into indefinite exile, deletion, overlap/crushing, implicit resize, an unbounded search, a hidden future ruling or invented named cosmology. Specify 3D ring origin, footprint/orientation, tie order and multi-entity placement when earlier ejections consume later bodies\' only fitting spaces. Include concrete physical-exhaustion and blocker-only fallback examples.'
        },
        {
            'id': 'BAN-R02-02', 'severity': 'adoption-blocking',
            'location': 'SPELL_MODEL.json BAN-07 and /procedure/castAndSave; PLAYER_CHAPTER.md Voluntary restrictions; Paladin /cards/41, /cards/43, /cards/130',
            'finding': 'Verdict Absolute forbids voluntary teleportation/invisibility, but does not contain No Escape\'s extradimensional-travel clause. The proposal classifies Banishment as non-teleport planar displacement to exclude Reign of Ashes, while also treating Verdict Absolute as blocking willing admission. Those two readings are inconsistent. Willing admission that rolls and fails instead of electing failure also needs an explicit voluntariness predicate.',
            'requiredCorrection': 'Keep the three exact cards distinct. Under the proposed non-teleport classification, explain why Verdict Absolute does or does not apply without importing No Escape\'s extra clause. Compare willing election, genuinely unwilling failed save, and willing but rolled failure for each relevant restriction. Clearly label the Banishment-only transport classification as NEW authorship; do not redefine all planar travel.'
        },
        {
            'id': 'BAN-R02-03', 'severity': 'requires-consistent-text',
            'location': 'CASEBOOK.json BAN-C10; SPELL_MODEL.json /procedure/escape/primaryEscape, /procedure/closure/trigger and /cellEnd',
            'finding': 'BAN-C10 says the cell closes/ejects remaining objects if no other occupants, whereas the model ends the primary branch on escape and closes any remaining contents. The empty-cell case is excluded by the closure trigger\'s any-real-body/object condition even though the cell should cease as well.',
            'requiredCorrection': 'State one lifecycle: primary escape ends the application, immediately settles every remaining secondary body/object once under the complete closure procedure, and destroys even an empty ephemeral cell. If another rule is intended, specify its finite lifetime explicitly. Add an actual primary escape with a secondary body and cargo still inside.'
        },
        {
            'id': 'BAN-R02-04', 'severity': 'evidence-correction',
            'location': 'CASEBOOK.json BAN-C01 and BAN-C02; all thirty /sourceRefs',
            'finding': 'BAN-C01 places establishment/deadline in costLedger and RP30/7/23 in clockLedger; BAN-C02 also places rpSpent in clockLedger. All thirty sourceRefs arrays are empty. These are authored evidence/schema defects, not runtime failures.',
            'requiredCorrection': 'Correct ledger fields and populate sourceRefs with bound source path and exact object pointer or section as applicable, distinguishing NEW proposal clauses from existing authority. Keep historicalSourceScenario records unchanged.'
        },
        {
            'id': 'BAN-R02-05', 'severity': 'incomplete-authored-examples',
            'location': 'CASEBOOK.json especially BAN-C10, BAN-C11, BAN-C13, BAN-C17, BAN-C23, BAN-C24, BAN-C26, BAN-C29, BAN-C30',
            'finding': 'Several requested current adjudications still use placeholder permissions, unspecified paid costs, unnamed source rerolls/transformations and no actual terminal coordinates. C17 explicitly promised numeric outcomes in its historical requirement but still only says to follow actual Counterspell/reroll rules. C29 and C30 leave the actual casts\' RP ledgers empty. A conditional visitor fixture is not evidence that any supplied source can target a previously unknown cell.',
            'requiredCorrection': 'Make each applicable fixture concrete with legal class/repertoire, actual costs/action/command state, rolls/DC where relevant, elapsed times, exact body/arrival geometry and terminal identities. For a source permission not established in the 49 files, label the fixture conditional rather than invent an ability. Use the actual current Faction Portal, Spectral Steed, Water Pet and Counterspell records for concrete escape/creation/counter examples. Distinguish conditional interface coverage from demonstrated current legal states. Avoid asserting that a Medium-to-Large change cannot fit a cell until actual dimensions show it.'
        }
    ]
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'REPAIR REQUIRED; first GPT return preserved, not jointly accepted or adopted',
        'archive': info(A / 'DD_Banishment_Current_Review_01_Return.zip'),
        'actualBrowserResponse': info(A / 'BANISHMENT_CURRENT_REVIEW_01_RETURN_ACTUAL_DOM.txt'),
        'sourceAndPreservationChecks': checks,
        'checkCount': len(checks), 'failureCount': sum(not c['pass'] for c in checks),
        'semanticFindingCount': len(findings), 'findings': findings,
        'caseCount': 30, 'emptySourceRefsCount': sum(not c['sourceRefs'] for c in cases),
        'newRulesAdopted': False, 'sourceInformationDeleted': 0,
        'runtimeTestsExecuted': 0, 'humanPlaytested': False,
        'ordinarySpellCountsUnchanged': {'reviewed': 434, 'pending': 414, 'total': 848},
    }
    audit.write_bytes(encoded(result))
    assert result['failureCount'] == 0, result['failureCount']
    lines = [
        'Continue the dedicated ordinary Banishment conference in this same Part 4 chat. Codex downloaded and preserved your exact DD_Banishment_Current_Review_01_Return.zip: 33,775 bytes, SHA-256 2057a8ace9e7102dfac550abec4daa3f0640399828be5dcb8dc3fe6016632d47.',
        f'Local verification passed {len(checks)} source/output/preservation checks: all 49 source files still match, the complete ordinary source/access card is unchanged, all historical BAN-C01..28 scenario records are preserved, and BAN-C01..30 plus BAN-01..10 are present. This is structural verification, not approval of semantic completeness or runtime execution.',
        'I have NOT accepted or adopted Banishment yet. The first return has five repair findings. Please read them against the same full 49-source input and your actual first-return files; make a complete replacement candidate rather than a prose-only reply.'
    ]
    for f in findings:
        lines.extend(['', f['id'] + ' — ' + f['location'], f['finding'], 'Required repair: ' + f['requiredCorrection']])
    lines.extend([
        '',
        'Exact Paladin authorities already in your input: /cards/41 No Escape says cannot voluntarily teleport, become invisible or enter extradimensional travel; /cards/43 Verdict Absolute says cannot voluntarily teleport or become invisible; /cards/130 Reign of Ashes says cannot benefit from Dash or teleportation. Preserve these differences.',
        'Retain all 30 original case IDs and their historicalSourceScenario evidence exactly. Add numbered repair examples BAN-X01 onward for the physical-exhaustion branch, blocker-only last resort, exact Paladin branches and primary escape leaving a secondary body/cargo. Cite current source paths/pointers in each example. Keep conditional external-visitor cases explicitly conditional unless a current actual source proves the route.',
        'Return DD_Banishment_Repair_02_Return.zip with exactly the same eight roots: REGISTER.json, SPELL_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_REVIEW.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json. Include explicit dispositions for BAN-R02-01..05, exact source hashes and output sizes/hashes. Preserve all source/access metadata. Clearly mark every NEW scoped rule, including any replacement of your closure design. Do not silently broaden AC4 or class rules. Cleric Banish Unholy stays separate.',
        'No ordinary-spell adoption, named-cosmology, soul/origin, era, numerical-balance, runtime, human-playtest, whole-game or publication approval is implied. If a complete finite procedure is not possible under the chosen design, replace that design explicitly instead of declaring unresolved geometry complete.'
    ])
    request.write_text('\n\n'.join(lines) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'audit': info(audit), 'request': info(request), 'checks': len(checks), 'failureCount': result['failureCount'], 'semanticFindings': len(findings)}))


if __name__ == '__main__':
    main()
