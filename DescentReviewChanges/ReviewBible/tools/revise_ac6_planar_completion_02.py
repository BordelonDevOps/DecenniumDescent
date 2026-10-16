"""Preserve draft01 and make geometry/healing examples explicit in draft02."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(p):
    return json.loads(p.read_bytes())


def main():
    previous = R / 'data/director/spell_proposals/ac6_planar_completion_draft_01.json'
    output = R / 'data/director/spell_proposals/ac6_planar_completion_draft_02.json'
    report = A / 'AC6_PLANAR_COMPLETION_LOCAL_REVIEW_02.json'
    assert not output.exists() and not report.exists()
    old = read(previous); draft = deepcopy(old)
    draft.update(id='DD-AC6-PLANAR-COMPLETION-DRAFT-02', recordedAtUtc=datetime.now(timezone.utc).isoformat(), previousCompleteDraft=info(previous))
    portal = draft['spells'][2]['modes']['Conjuration8']
    old_geometry = 'Both openings need actual unoccupied clear physical volume at formation and suitable real destination support for the declared initial users; the spell creates no floor, breathing protection or environmental immunity.'
    new_geometry = 'Both openings initially need actual unoccupied clear physical aperture volume and a front-side receiving region at least10feet wide,15feet high and5feet deep. A larger traveler needs additional actual receiving clearance at transit. An unsupported but otherwise empty fitting destination is permitted; the spell creates no floor, flight, breathing protection or environmental immunity. A traveler arriving without real support immediately follows its actual Falling/other movement rules.'
    assert portal['openings'].count(old_geometry) == 1
    portal['openings'] = portal['openings'].replace(old_geometry, new_geometry)
    portal['transit'] += ' NEW receiving placement: before a particular transit commits, declare the receiving whole-body footprint/pose on the exit\'s front side, with the nearest edge of that footprint no more than5feet from the exit plane and every body point on the receiving side. It must be a real perceived or personally known location through the actual opening view, fit the current whole body/group and obey the declared exit orientation; it is not a remote retarget beyond the receiving space. Hidden/intervening occupancy is checked after a valid commitment and can defeat that paid movement without a substitute. All bodies retain their actual anatomy, dimensions, load and gear; no slot is reserved against other travelers. The five-foot minimum setup clearance alone does not prove that a Large or larger body fits.'
    cases = {x['id']: x for x in draft['workedExamples']}
    cases['PB-D03']['proposedAdjudication'] = 'While the wall is suppressed, a qualifying Large creature with an actual10foot width and10foot height stands through its thickness. Use wall coordinates x=-15..15,z=0..15 and5foot panels, with the body intersecting x=-5..5,z=0..10: four panels are occupied, not two. At resumption these four remain pending without crushing or teleportation. Each resumes only when its qualifying body intersections clear, retaining the same deadline. Other clear unsuppressed panels remain operative.'
    cases['GA-D03']['proposedAdjudication'] = 'A qualifying Null damage root takes the ally from10HP to0 at t100. Same Large body remains NullDisabled0, occupying its real space; no corpse/cargo drop or replaced creature appears. At t110, a Cleric1 with the actually selected Healing Rite, WIS+3, S1 and3current RP takes its real Action from20feet away with ordinary perception/line of effect and no healing blockers or other bonuses. GA-HEAL-01 expressly makes this extant ally a legal living-ally target. Healing Rite spends2RP (3to1) and rolls1d8=4, plusM3, restoring7HP on the same body and ending Disabled. This is a class technique, not an ordinary spell cast. Source expiry remains t3600 and no command or offense allowance is refreshed.'
    draft['workedExamples'].append({'id': 'NX-D11', 'spellId': 'alignment-nexus', 'title': 'A fitting unsupported arrival is real travel',
        'proposedAdjudication': 'The caster actually knows a clear receiving balcony that later loses its floor while both openings remain geometrically unobstructed. A traveler deliberately declares a fitting visible whole-body arrival in that unsupported space and completes an otherwise legal transit. It arrives and immediately follows the actual Falling rule; Nexus supplies no floor, Hover, safe-place retarget or automatic return. A Large traveler whose receiving footprint needs10feet depth cannot rely on the initial5foot minimum clearance as proof that it fits.',
        'evidenceKind': 'Unadopted authored conditional example; no runtime or human test.', 'sourceRefs': [{'path': output.relative_to(G).as_posix(), 'pointer': '/spells/2/modes/Conjuration8/openings', 'authority': 'NEW local proposal, not accepted rule'}, {'path': output.relative_to(G).as_posix(), 'pointer': '/spells/2/modes/Conjuration8/transit', 'authority': 'NEW local proposal, not accepted rule'}]})

    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    catalog = read(catalog_path)
    ac4_path = R / 'data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json'
    ac4 = read(ac4_path)
    def cat_ref(ident):
        i = next(i for i, x in enumerate(catalog['spells']) if x['id'] == ident)
        return {'path': catalog_path.relative_to(G).as_posix(), 'pointer': f'/spells/{i}/operational', 'authority': 'Current reviewed comparison, within its own scope'}
    def ac4_ref(ident):
        i = next(i for i, x in enumerate(ac4['spells']) if x['spellId'] == ident)
        return {'path': ac4_path.relative_to(G).as_posix(), 'pointer': f'/spells/{i}/procedure', 'authority': 'Accepted AC4 procedure, within its own scope'}
    null_ref = {'path': 'DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md', 'section': '### Recipient lifecycles for qualifying Null damage', 'authority': 'Accepted Null lifecycle rules'}
    for x in draft['workedExamples']:
        for ref in x['sourceRefs']:
            if ref['path'] == previous.relative_to(G).as_posix():
                ref['path'] = output.relative_to(G).as_posix()
        if x['id'] == 'PB-D01': x['sourceRefs'].append(cat_ref('planar-ally-minor'))
        if x['id'] in ['PB-D04', 'NX-D06']: x['sourceRefs'].append(ac4_ref('dimensional-anchor'))
        if x['id'] == 'PB-D05': x['sourceRefs'].append({'path': 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/banishment_exact_model_04.json', 'pointer': '/procedure/closure', 'authority': 'Accepted ordinary Banishment terminal-return exception only'})
        if x['id'] in ['GA-D03', 'GA-D04']: x['sourceRefs'].extend([null_ref, {'path': output.relative_to(G).as_posix(), 'pointer': '/greaterPlanarAllyProfile', 'authority': 'NEW scoped profile/healing proposal'}])
        if x['id'] == 'GA-D03': x['sourceRefs'].append({'path': 'DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json', 'pointer': '/cards/12', 'authority': 'Actual Cleric Healing Rite'})
        if x['id'] == 'NX-D02': x['sourceRefs'].append(ac4_ref('alignment-lock'))
        if x['id'] == 'NX-D04': x['sourceRefs'].append(cat_ref('fate-coin'))
        if x['id'] == 'NX-D11': x['sourceRefs'].append({'path': 'DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md', 'section': '## Movement and geometry', 'authority': 'Actual current Falling rules; no new damage formula authored here'})
    paths = {G / b['path'] for b in old['sourceBindings']}
    paths.update([previous, A / 'AC6_PLANAR_COMPLETION_CHECK_01.json', Path(__file__).resolve()])
    for x in draft['workedExamples']:
        paths.update(G / ref['path'] for ref in x['sourceRefs'] if ref['path'] != output.relative_to(G).as_posix())
    bindings = [info(p) for p in sorted(paths)]
    draft['sourceBindings'] = bindings
    checks = []
    def ck(name, value):
        checks.append({'check': name, 'pass': bool(value)}); assert value, name
    ck('all source/access and historical receipts preserved', all(x['completeSourceAndAccess'] == old['spells'][i]['completeSourceAndAccess'] and x['historicalDeferredReceipt'] == old['spells'][i]['historicalDeferredReceipt'] for i, x in enumerate(draft['spells'])))
    ck('all previous example identities plus new arrival case', {x['id'] for x in old['workedExamples']} | {'NX-D11'} == {x['id'] for x in draft['workedExamples']} and len(draft['workedExamples']) == 23)
    ck('actual Healing Rite identity', read(R / 'data/public/class_playtests/cleric.json')['cards'][12]['id'] == 'cleric.base.healing-rite')
    for example in draft['workedExamples']:
        for ref in example['sourceRefs']:
            if 'pointer' in ref:
                source = draft if ref['path'] == output.relative_to(G).as_posix() else read(G / ref['path'])
                ck(example['id'] + ' exact pointer ' + ref['pointer'], bool(at(source, ref['pointer'])))
            else:
                ck(example['id'] + ' section ' + ref['section'], ref['section'] in (G / ref['path']).read_text(encoding='utf8'))
    output.write_bytes(encoded(draft))
    ck('all existing sources unchanged', all(info(G / b['path']) == b for b in bindings))
    findings = [
        {'id': 'PD-LOCAL-01', 'finding': 'A10x10 profile crossing a panel plane occupies four5x5panels, not an unspecified two.', 'change': 'PB-D03 now gives actual wall/body coordinates and four-panel outcome.'},
        {'id': 'PD-LOCAL-02', 'finding': 'The generic healing example did not identify an actual source, cost, range or roll.', 'change': 'GA-D03 now uses the exact Cleric1 Healing Rite card12, Action2RP,20foot legal range,1d8=4+3=7 healing, and the explicit unadopted profile extension.'},
        {'id': 'PD-LOCAL-03', 'finding': 'Initial five-foot receiving clearance could be confused with whole-body arrival legality.', 'change': 'Each transit declares a complete current receiving footprint/pose; large bodies require actual additional clearance, with hidden paid failure and no substitute.'},
        {'id': 'PD-LOCAL-04', 'finding': 'The first draft required support at portal setup despite supplying no actual safety guarantee.', 'change': 'Fitting unsupported arrival is explicitly allowed and invokes real Falling; new NX-D11 demonstrates the consequence without free floor/flight/rescue.'},
        {'id': 'PD-LOCAL-05', 'finding': 'Several integration examples only cited their draft and source receipt.', 'change': 'Added exact current Banishment, AC4, Minor Ally, Fate Coin, Healing Rite, Null and Falling references where operative.'},
    ]
    report.write_bytes(encoded({'recordedAtUtc': draft['recordedAtUtc'], 'previousDraft': info(previous), 'currentDraft': info(output), 'findings': findings, 'checkCount': len(checks), 'failureCount': 0, 'checks': checks,
        'scope': 'Local source and authored geometry/example review; all new procedures remain unadopted and unsent. The five joint design decisions, active AC5 dependencies, CR certification, runtime and human balance are not resolved by these checks.', 'sourceInformationDeleted': 0, 'newSpellAdoptions': 0}))
    print(json.dumps({'draft': info(output), 'review': info(report), 'sourceFiles': len(bindings), 'examples': len(draft['workedExamples']), 'localFindingsAddressed': len(findings), 'checks': len(checks), 'failures': 0}))


if __name__ == '__main__':
    main()
