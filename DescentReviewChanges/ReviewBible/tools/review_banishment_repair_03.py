"""Preserve and independently audit the completed GPT Banishment Repair03."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest
from review_banishment_repair_02 import at


def read(path):
    return json.loads(path.read_bytes())


def main():
    out = A / 'banishment-repair-03-return'
    target = A / 'BANISHMENT_REPAIR_03_LOCAL_AUDIT.json'
    request = A / 'BANISHMENT_REPAIR_04_REQUEST.txt'
    assert not target.exists() and not request.exists()
    inputs = read(A / 'banishment-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    model = read(out / 'SPELL_MODEL.json')
    register = read(out / 'REGISTER.json')
    cases = read(out / 'CASEBOOK.json')['cases']
    prior = read(A / 'banishment-repair-02-return/CASEBOOK.json')['cases']
    sources = read(out / 'SOURCE_HASHES.json')
    manifest = read(out / 'EVIDENCE_MANIFEST.json')
    checks = []

    def check(label, ok):
        checks.append({'check': label, 'pass': bool(ok)})

    check('exact eight root files', {p.name for p in out.iterdir()} == {
        'REGISTER.json', 'SPELL_MODEL.json', 'PLAYER_CHAPTER.md',
        'DIRECTOR_REVIEW.md', 'CASEBOOK.json', 'SOURCE_HASHES.json',
        'VERDICT.md', 'EVIDENCE_MANIFEST.json'})
    check('original49source bindings exact', sources['bindings'] == inputs['sourceBindings'])
    for b in sources['bindings']:
        raw = (G / b['path']).read_bytes()
        check('current source: ' + b['path'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    for b in manifest['files']:
        raw = (out / b['name']).read_bytes()
        check('output: ' + b['name'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    check('ordinary source/access object exact', model['sourceAndAccess'] == inputs['sourceCard'])
    check('register/model access agree', register['spell']['accessRows'] == model['procedure']['access'])
    check('all34previous case IDs retained in order', [c['id'] for c in cases[:34]] == [c['id'] for c in prior])
    check('one new mandatory reversion example', len(cases) == 35 and cases[-1]['id'] == 'BAN-X05')
    for original in inputs['originalAuthoredExamples'] + inputs['additionalReviewScenarios']:
        check('historical evidence: ' + original['id'], next(c for c in cases if c['id'] == original['id'])['historicalSourceScenario'] == original)
    check('ten original review IDs', [q['id'] for q in model['questionDispositions']] == [f'BAN-{i:02}' for i in range(1, 11)])
    check('four repair dispositions', [q['id'] for q in model['repairDispositions']] == [f'BAN-R03-{i:02}' for i in range(1, 5)])
    check('register/model original dispositions agree', register['questionDispositions'] == model['questionDispositions'])
    check('register/model repair dispositions agree', register['repairDispositions'] == model['repairDispositions'])
    refs = []
    sections = []
    for c in cases:
        check(c['id'] + ' nonempty sourceRefs', bool(c['sourceRefs']))
        for ref in c['sourceRefs']:
            path = out / ref['path'] if ref['path'] == 'SPELL_MODEL.json' else G / ref['path']
            entry = {'caseId': c['id'], **ref}
            if ref['pointer'].startswith('section:'):
                sections.append(entry)
                continue
            try:
                value = at(read(path), ref['pointer'])
                ok = value is not None
                entry['resolvedIdentity'] = ({k: value[k] for k in ('id', 'name') if k in value}
                                             if isinstance(value, dict) else None)
            except (KeyError, IndexError, ValueError, FileNotFoundError):
                ok = False
            refs.append(entry)
            check(c['id'] + ' JSON reference ' + ref['path'] + ref['pointer'], ok)

    findings = [
        {
            'id': 'BAN-R04-01', 'severity': 'source-regression',
            'location': 'CASEBOOK.json BAN-C17 actionsAndResolution/sourceRefs',
            'finding': 'The Oracle reroll now says once/day and cites /cards/14, which resolves to Mystery Surge, not Spiral-Touched Boon I. The operative Oracle /cards/31 is 1/long rest and requires using the new result. This is a semantic reference failure despite a structurally resolvable pointer.',
            'requiredCorrection': 'Restore /cards/31 and exact 1/long rest/current result timing. Preserve the old once/day wording only inside the historical source object. Keep the revised Wizard class Counterspell fixture: /cards/17 really costs3RP and uses INT+PB vs10+2*rank; add its actual2-round recharge to the ledger rather than reverting to ordinary5RP Counterspell.'
        },
        {
            'id': 'BAN-R04-02', 'severity': 'stale-operative-language',
            'location': 'CASEBOOK.json BAN-C27 actionsAndResolution; SPELL_MODEL.json /cosmologyBoundary',
            'finding': 'C27 still instructs preserve corpse identity/package reservation and release ended summon berth, although Repair03 removes reservations. The active top-level cosmologyBoundary still names BAN-CELL-01 instead of BAN-CELL-03.',
            'requiredCorrection': 'Replace current C27 reservation instructions with extant corpse/cargo identity tracking and absence of the expired summon. Update the current cell ID. Preserve superseded wording only in explicit historical material. Scan operative prose semantically, not only for old rule-ID strings.'
        },
        {
            'id': 'BAN-R04-03', 'severity': 'example-geometry',
            'location': 'CASEBOOK.json BAN-C13, BAN-C24 and BAN-C30',
            'finding': 'C13 calls origin ordinary open terrain yet says its old5x5 anchor cannot contain the new10x10 anatomy. A fixed spatial anchor is not a5x5 container: on clear open terrain the new10x10 footprint can fit at the same center. C24 places the Pet against the east cell boundary but claims no expansion is required for5ft clearance. C30 still omits an actual Water Pet preflight square and says after ordinary positioning without position/cost.',
            'requiredCorrection': 'C13 should return the Large body at the same anchor on its stated open terrain, or explicitly supply real terrain obstructing that footprint before selecting adjacent placement. In C24 remove the false clearance assertion and define post-admission expanded bounds if expansion is selected. In C30 give the Pet square that is already visible/fitting/unoccupied at preflight, before the new concentration ends the Steed, plus any real movement/cost. Prior legal Steed admission may have expanded the cell; document the resulting bounds rather than implying a future expansion.'
        },
        {
            'id': 'BAN-R04-04', 'severity': 'scope-and-operability',
            'location': 'SPELL_MODEL.json /procedure/closure/placementConflictState and /fallingAndSupport; Player/Director placement conflict paragraphs; BAN-X01/BAN-X05',
            'finding': 'The accepted body source supplies an unresolved physical conflict at the same spatial anchor until obstruction removal or legal relocation. It does not define occupiedFootprint=null or categorically forbid every action/reaction/effect requiring position, perception, range or reach. Those are new authored consequences, not an already accepted canonical record. The model categorical prohibition is also stronger than the chapters saying normally. It can prevent the independently legal relocation invoked as a way out and creates de facto untargetability without a stated targeting procedure.',
            'requiredCorrection': 'Keep finite ending and mandatory anatomy preservation. Explicitly distinguish inherited placement order from any NEW Banishment-only conflict-state semantics. Define a usable fixed-anchor spatial reference for effects that require location without granting legal movement, wall passage, overlap or automatic immunity. Apply each actual effect prerequisite instead of a blanket null-footprint failure. If proposing different semantics, label them NEW and explain the interaction. Supply two actual-source adjudications: obstruction physically removed, and one current legal relocation source resolving a conflict (or explain exactly why a stated source fails). State how perception/LoE, terrain/support, ongoing attached effects and real clocks are evaluated; do not change the global body rule silently.'
        }
    ]
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Repair03 preserved; finite ending and real familiar escape materially improved; further bounded correction required before adoption.',
        'archive': info(A / 'DD_Banishment_Repair_03_Return.zip'),
        'actualBrowserResponse': info(A / 'BANISHMENT_REPAIR_03_RETURN_ACTUAL_DOM.txt'),
        'checks': checks, 'checkCount': len(checks),
        'failureCount': sum(not c['pass'] for c in checks),
        'resolvedJsonReferences': refs, 'resolvedJsonReferenceCount': len(refs),
        'descriptiveSectionReferences': sections, 'sourceReferenceCount': len(refs) + len(sections),
        'semanticFindings': findings, 'semanticFindingCount': len(findings),
        'independentSemanticReadScope': 'Complete operative model, Player and Director chapters, register, all35current case adjudications and every JSON source reference identity; exact body-placement, Oracle31, Wizard17 and Mage21/engine authorities. Structural validation is not semantic approval.',
        'sourceInformationDeleted': 0, 'newRulesAdopted': False,
        'runtimeTestsExecuted': 0, 'humanPlaytested': False,
        'countsUnchanged': {'reviewed': 434, 'pending': 414, 'total': 848},
    }
    assert result['failureCount'] == 0
    target.write_bytes(encoded(result))
    body = (R / 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md').read_text(encoding='utf8')
    placement = body.split('## Placement and involuntary endings\n', 1)[1].split('\n## Body weight and conditions', 1)[0]
    text = [
        'Continue the same ordinary Banishment review with bounded Repair04. I preserved DD_Banishment_Repair_03_Return.zip exactly:44,092bytes,SHA256 e8cd1eff7ee8f8d727db37abf5972d5c4a6b70a3ba1158e6ada087f6200dca85. No Banishment rule has been adopted.',
        f'Independent structural verification: {len(checks)}checks,0failures;49frozen sources/output hashes, original source/access,34prior case IDs plusBAN-X05, and28historical scenario objects preserved. {len(refs)}JSON pointers resolve and{len(sections)}references are descriptive section references. I also read all35current adjudications and the complete model/chapters/register. A resolving pointer is not necessarily the right source.',
        'The finite plane-return design and actual nonconcentration Mage familiar escape are useful corrections. Keep them and the exact Paladin distinction. Four bounded issues remain:',
    ]
    for f in findings:
        text += [f['id'] + ' — ' + f['location'], f['finding'], 'Required resolution: ' + f['requiredCorrection']]
    text += [
        'Exact accepted body placement source (already one of the49inputs):', placement,
        'Oracle /cards/31 operative identity: oracle.supplement.spiral-touched.spiral-touched-boon-i; frequency Reroll1/long rest; effect +3initiative;1/long rest reroll one failed save and use the new result. /cards/14 is Mystery Surge, a different feature.',
        'For the conflict-state discussion, the same frozen input contains actual Dimensional Door in accepted AC4 /spells/12, and actual ordinary Polymorph catalog /spells/735/operational. Use exact existing source predicates if either is relevant; do not invent a generic teleport or discard origin-plane blockers. Distinguish logical spatial reference from a legal occupied footprint and prove the selected procedure is runnable.',
        'Return DD_Banishment_Repair_04_Return.zip with the same8root files. Preserve all49source bindings, original source/access and28historicalSourceScenario objects exactly. Retain all35current case IDs; add cases only for the requested conflict-resolution evidence. Include BAN-R04-01..04 dispositions. Update all current model/register/chapter/case wording consistently and verify complete file hashes. No runtime/human/balance/canon/soul/origin/era/whole-game/publication approval. Cleric Banish Unholy remains separate. Please evaluate the precise issue and correct it directly; do not reopen the accepted AC4module or return to protected berths.'
    ]
    request.write_text('\n\n'.join(text) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'audit': info(target), 'request': info(request), 'checks': len(checks), 'failures': 0, 'semanticFindings': len(findings)}))


if __name__ == '__main__':
    main()
