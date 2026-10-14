"""Exercise real paid Gnome feat histories and all four gadget procedures."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_lineage_prerequisite_model import LineagePrerequisites
from feat_exact_01_gadget_use import GadgetUse, SID
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT_EXACT_01_GADGET_USE_CHECK.json'; notes = A / 'FEAT_EXACT_01_GADGET_USE_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R / 'tools/feat_exact_01_gadget_use.py',
        R / 'tools/feat_exact_01_lineage_prerequisite_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'data/playtest/ancestry_background_candidate.json', R / 'data/playtest/character_foundation.json',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', R / 'data/public/feat_candidates/exact_01/candidate.json',
        R / 'data/public/feat_candidates/exact_01/supplements.json', R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        R / 'docs/feats/exact-candidate-01/HERITAGE_MUTATION.md', R / 'docs/feats/exact-candidate-01/SUPPLEMENTS.md',
        R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md', R / 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md']
    bindings = [info(p) for p in paths]
    ancestry = read(paths[4]); classes = {x['class']: x for x in read(paths[5])['classes']}
    contracts = {x['id']: x for x in read(paths[6])['records']}
    gnome = next(x for x in ancestry['ancestries'] if x['name'] == 'Gnome')
    profiles = next(x['value'] for x in read(paths[8])['groups'] if x['id'] == 'SUP-08')
    candidate = next(x for x in read(paths[7])['feats'] if x['id'] == SID)
    world = {
        'evidenceMode': 'conditional-fixture', 'activeActor': 'maker', 'legalObjectSpaces': [0, 5],
        'actors': {key: {'position': pos, 'canAct': True, 'canWork': True, 'canHear': hear,
                        'actions': 1, 'interactions': 1, 'regularSerial': 1,
                        'freeHands': 2, 'willingToReceive': True}
                   for key, pos, hear in [('maker', 0, True), ('ally', 5, True), ('at30', 30, True),
                                          ('beyond30', 31, True), ('deaf', 0, False)]},
        'tools': {'tool-A': {'kind': 'tinkers-tools', 'usable': True, 'accessibleTo': ['maker'], 'position': 0}},
        'parts': {'parts-A': {'owner': 'maker', 'suitableMundaneParts': True, 'creditedCopper': 1000, 'position': 0}},
        'passages': {'doorway': {'ground': True, 'widthFeet': 5, 'position': 0}},
        'edges': {'shelf': {'mundane': True, 'thicknessInches': 2, 'position': 0}},
        'cargo': {'paperweight': {'weightLb': 5, 'creature': False, 'unattended': True,
                    'willinglyPresented': False, 'position': 0, 'attachedTo': None}},
        'bodies': {'walker': {'corporeal': True}, 'ghost': {'corporeal': False}},
        'unrelatedInventory': {'goldCoinsCopperValue': 5000, 'lampFuel': 3, 'classDevices': [],
                               'ancestralClockwork': ['separate-existing-ancestry-object'], 'purchasedSupplies': 4},
        'unrelatedHazards': {'rulesGasPresent': True, 'magicalDarknessPresent': True, 'suffocating': True}}
    checks = []; traces = []

    def check(label, condition):
        checks.append({'id': label, 'passed': bool(condition)})
        if not condition: raise AssertionError(label)

    def reject(label, model, operation):
        before = model.snapshot()
        try: operation()
        except ValueError as exc: checks.append({'id': label, 'passed': True, 'reason': str(exc)})
        else: check(label, False)
        check(label + '/no-partial-write', model.snapshot() == before)

    def make(variant=None, paid=True, base=None):
        base = base or gnome; variant = variant or base['variants'][0]
        actor = {'ancestryId': base['id'], 'variantId': variant['id'], 'classLevels': {'Warrior': 1},
            'abilityRolls': {k: [1, 4, 4, 4] for k in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']},
            'permanentScores': {k: 12 + variant['combinedAbilityBonuses'].get(k, 0)
                                for k in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']}, 'syntheticWitness': True}
        lineage = LineagePrerequisites(actor, ancestry, classes, contracts)
        lineage.advance(4); lineage.earn(4)
        m = GadgetUse(lineage, profiles, world)
        if paid: m.acquire('Warrior:4')
        return m

    def built(face, variant=None):
        m = make(variant); m.start('tool-A', 'parts-A'); m.advance(600)
        return m, m.complete(face, 0)

    def record(label, before, m, **extra):
        traces.append({'id': label, 'before': before, 'after': m.snapshot(), **extra})

    check('complete-source-procedure-equals-public', contracts[SID]['completeOperativeProcedure'] == candidate['operationalRules'])
    check('original-source-preserved', contracts[SID]['originalObject'] == candidate['sourceObject'])
    check('four-exact-profiles', [x['die'] for x in profiles] == [1, 2, 3, 4] and
          [x['id'] for x in profiles] == ['heritage-gadget.shaded-lamp', 'heritage-gadget.line-bell',
                                       'heritage-gadget.light-clamp', 'heritage-gadget.hand-fan'])
    check('all-current-Gnome-variants', {x['id'] for x in gnome['variants']} == {'tinker-gnome', 'arcanist-gnome', 'prankster-gnome'})
    for variant in gnome['variants']:
        m = make(variant, paid=False); before = m.snapshot(); m.acquire('Warrior:4')
        check(variant['id']+'/actual-paid-choice', m.lineage.pay.has(SID) and m.lineage.pay.opportunities['Warrior:4']['spent'])
        check(variant['id']+'/initial-no-inventory-or-proficiency-grant', m.world == before['world'] and not m.objects and m.next_start is None)
        m.lineage.advance(8); m.lineage.earn(8)
        reject(variant['id']+'/nonrepeatable', m, lambda: m.acquire('Warrior:8'))
        record(variant['id']+'/paid-acquisition', before, m)
        for face in range(1, 5):
            m = make(variant); before = m.snapshot(); m.start('tool-A', 'parts-A')
            check(variant['id']+str(face)+'/costs-before-d4', m.world['parts']['parts-A']['creditedCopper'] == 500 and
                  m.next_start == 86400 and not m.objects and 'face' not in m.work)
            m.advance(599); reject(variant['id']+str(face)+'/no-early-completion', m, lambda: m.complete(face, 0))
            m.advance(600); identity = m.complete(face, 0); obj = m.objects[identity]
            check(variant['id']+str(face)+'/exact-object', obj['profile'] == profiles[face-1]['id'] and
                  obj['expiresAt'] == 4200 and obj['size'] == 'Tiny' and obj['weightLb'] == 1 and
                  obj['armorClass'] == 10 and obj['hp'] == 1 and not obj['creatureTurn'])
            reject(variant['id']+str(face)+'/no-reroll-or-second-product', m, lambda: m.complete(5-face, 0))
            m.advance(4199); check(variant['id']+str(face)+'/live-before-hour', m.get_live(identity)['active'])
            m.advance(4200); check(variant['id']+str(face)+'/inert-at-hour', not obj['active'] and m.active is None and obj['creditedReclaimCopper'] == 0)
            check(variant['id']+str(face)+'/no-ancestry-reclaim-or-inventory-recharge', m.world['unrelatedInventory'] == world['unrelatedInventory'])
            record(variant['id']+'/'+str(face)+'/construction-expiry', before, m)

    human = next(x for x in ancestry['ancestries'] if x['name'] == 'Human')
    m = make(paid=False, base=human); reject('non-Gnome-no-invented-heritage', m, lambda: m.acquire('Warrior:4'))
    m = make(paid=False); reject('unpaid-does-not-build', m, lambda: m.start('tool-A', 'parts-A'))
    for label, change in [
        ('no-tools', lambda m: m.world['tools'].clear()),
        ('wrong-tools', lambda m: m.world['tools']['tool-A'].update(kind='smiths-tools')),
        ('broken-tools', lambda m: m.world['tools']['tool-A'].update(usable=False)),
        ('inaccessible-tools', lambda m: m.world['tools']['tool-A'].update(accessibleTo=[])),
        ('distant-tools', lambda m: m.world['tools']['tool-A'].update(position=10)),
        ('insufficient-parts', lambda m: m.world['parts']['parts-A'].update(creditedCopper=499)),
        ('coins-not-parts', lambda m: m.world['parts']['parts-A'].update(suitableMundaneParts=False)),
        ('not-owned', lambda m: m.world['parts']['parts-A'].update(owner='ally')),
        ('out-of-reach-parts', lambda m: m.world['parts']['parts-A'].update(position=10)),
        ('cannot-work', lambda m: m.world['actors']['maker'].update(canWork=False)),
        ('suppressed', lambda m: m.lineage.pay.suppress(SID))]:
        m = make(); change(m); reject('construction/'+label, m, lambda: m.start('tool-A', 'parts-A'))

    for second in [1, 599, 600]:
        m = make(); before = m.snapshot(); m.start('tool-A', 'parts-A'); m.advance(second); m.interrupt('explicit-work-interruption')
        check('interrupt/'+str(second)+'/costs-retained-no-product', m.world['parts']['parts-A']['creditedCopper'] == 500 and
              m.next_start == 86400 and not m.objects and m.work is None)
        reject('interrupt/'+str(second)+'/cannot-finish', m, lambda: m.complete(1, 0))
        m.advance(86399); reject('interrupt/'+str(second)+'/elapsed-not-calendar', m, lambda: m.start('tool-A', 'parts-A'))
        m.advance(86400); m.start('tool-A', 'parts-A'); m.advance(87000); m.complete(4, 0)
        check('interrupt/'+str(second)+'/next-real-attempt-pays-again', m.world['parts']['parts-A']['creditedCopper'] == 0 and m.next_start == 172800)
        record('interrupted-construction/'+str(second), before, m)
    m = make(); m.advance(86300); before = m.snapshot(); m.start('tool-A', 'parts-A'); m.advance(86900); identity = m.complete(1, 0)
    m.advance(90000); reject('midnight-does-not-reset-use', m, lambda: m.start('tool-A', 'parts-A'))
    # A genuine rest can occur on the shared clock; no reset operation exists on this elapsed-time allowance.
    m.advance(120000); m.events.append({'type': 'conditional-beneficial-rest-completed', 'at': 120000})
    reject('rest-does-not-reset-use', m, lambda: m.start('tool-A', 'parts-A'))
    m.advance(172699); reject('one-second-before-24-hours', m, lambda: m.start('tool-A', 'parts-A'))
    m.advance(172700); m.start('tool-A', 'parts-A')
    check('exact-24-hour-start-boundary', m.next_start == 259100 and not m.objects[identity]['active'])
    record('elapsed-clock-across-midnight-and-rest', before, m)

    m = make(); m.start('tool-A', 'parts-A'); m.advance(600)
    for face in [0, 5, True]: reject('invalid-d4/'+str(face), m, lambda f=face: m.complete(f, 0))
    reject('unreachable-output', m, lambda: m.complete(1, 10))
    m.world['tools']['tool-A']['usable'] = False
    reject('lost-tool-access-at-completion', m, lambda: m.complete(1, 0)); m.interrupt('tools-broke-before-completion')

    for face in range(1, 5):
        m, identity = built(face); before = m.snapshot(); expiry = m.objects[identity]['expiresAt']
        m.transfer(identity, 'maker', 'ally')
        check('handoff/'+str(face)+'/same-identity-expiry-and-allowance', len(m.objects) == 1 and
              m.objects[identity]['owner'] == m.objects[identity]['holder'] == 'ally' and
              m.objects[identity]['expiresAt'] == expiry and m.next_start == 86400 and
              m.world['actors']['ally']['freeHands'] == 1 and not m.world['actors']['maker']['interactions'])
        m.regular_start('ally', 2); m.transfer(identity, 'ally', 'maker')
        check('handoff/'+str(face)+'/return-conserves-hands', m.world['actors']['ally']['freeHands'] == 2 and
              m.world['actors']['maker']['freeHands'] == 1 and m.objects[identity]['expiresAt'] == expiry)
        m.advance(expiry); reject('handoff/'+str(face)+'/expired-object-unusable', m, lambda: m.get_live(identity))
        record('handoff/'+str(face), before, m)
        m, identity = built(face); before = m.snapshot(); m.damage(identity, 0)
        check('damage/'+str(face)+'/zero-no-destruction', m.get_live(identity)['hp'] == 1)
        m.damage(identity, 1)
        check('damage/'+str(face)+'/one-destroys-no-refund', m.objects[identity]['hp'] == 0 and not m.objects[identity]['active'] and
              m.world['parts']['parts-A']['creditedCopper'] == 500 and m.next_start == 86400)
        record('destruction/'+str(face), before, m)
        m, identity = built(face); before = m.snapshot(); m.dismantle(identity, 'maker')
        check('dismantle/'+str(face)+'/inert-zero-credit', not m.objects[identity]['active'] and m.objects[identity]['creditedReclaimCopper'] == 0)
        record('conditional-dismantling/'+str(face), before, m)

    m, identity = built(1); before = m.snapshot(); result = m.lamp(identity, 'maker', True)
    check('lamp/exact-light-no-fuel-or-ignition', result == {'brightFeet': 10, 'additionalDimFeet': 10,
          'penetratesMagicalDarkness': False, 'fuelGranted': 0, 'ignitesOtherObjects': False})
    reject('lamp/one-action-not-free-interaction', m, lambda: m.lamp(identity, 'maker', False))
    m.regular_start('maker', 2); m.lamp(identity, 'maker', False)
    check('lamp/action-extinguishes', not m.objects[identity]['lit'])
    m.regular_start('maker', 3); m.lamp(identity, 'maker', True); m.advance(4200)
    check('lamp/expiry-ends-light-without-touching-hazards', not m.objects[identity]['lit'] and m.world['unrelatedHazards'] == world['unrelatedHazards'])
    record('lamp/action-light-extinguish-expiry', before, m)

    m, identity = built(2); before = m.snapshot(); armed = m.arm_bell(identity, 'maker', 'doorway')
    check('bell/visible-five-foot-thread-no-hidden-DC', armed == {'threadFeet': 5, 'loadBearing': False, 'automaticHiddenDC': None})
    for body, passage, contact in [('ghost', 'doorway', True), ('walker', 'elsewhere', True), ('walker', 'doorway', False)]:
        check('bell/nontrigger/'+str((body, passage, contact)), m.cross_bell(identity, body, passage, contact) == {'rang': False} and m.objects[identity]['active'])
    result = m.cross_bell(identity, 'walker', 'doorway', True)
    check('bell/one-physical-crossing-only', result['heardBy'] == ['maker', 'ally', 'at30'] and not result['revealsIdentity'] and
          result['damage'] == 0 and not result['trips'] and not result['restrains'] and not m.objects[identity]['active'])
    reject('bell/no-second-trigger', m, lambda: m.cross_bell(identity, 'walker', 'doorway', True))
    record('bell/contact-and-hearing-boundaries', before, m, result=result)
    for field, value in [('widthFeet', 6), ('ground', False), ('position', 10)]:
        m, identity = built(2); m.world['passages']['doorway'][field] = value
        reject('bell/illegal-passage/'+field, m, lambda: m.arm_bell(identity, 'maker', 'doorway'))

    for ending in ['expired', 'destroyed', 'removed']:
        m, identity = built(3); before = m.snapshot(); result = m.clamp(identity, 'maker', 'shelf', 'paperweight')
        check('clamp/'+ending+'/five-lb-two-inch-boundary', m.objects[identity]['clampedObject'] == 'paperweight' and
              m.world['cargo']['paperweight']['attachedTo'] == identity and result ==
              {'supportsClimber': False, 'barsDoor': False, 'restrains': False, 'checkBonus': 0, 'extraHands': 0})
        if ending == 'expired': m.advance(4200)
        elif ending == 'destroyed': m.damage(identity, 1)
        else: m.regular_start('maker', 2); m.unclamp(identity, 'maker')
        check('clamp/'+ending+'/ordinary-fall-handoff', m.world['cargo']['paperweight']['attachedTo'] is None and
              len([x for x in m.events if x['type'] == 'ordinary-object-fall-required']) == 1)
        record('clamp/'+ending, before, m)
    for label, change in [('heavy', lambda m: m.world['cargo']['paperweight'].update(weightLb=6)),
                         ('creature', lambda m: m.world['cargo']['paperweight'].update(creature=True)),
                         ('unwilling-held-object', lambda m: m.world['cargo']['paperweight'].update(unattended=False)),
                         ('thick-edge', lambda m: m.world['edges']['shelf'].update(thicknessInches=3)),
                         ('nonmundane-edge', lambda m: m.world['edges']['shelf'].update(mundane=False)),
                         ('distant-edge', lambda m: m.world['edges']['shelf'].update(position=10))]:
        m, identity = built(3); change(m); reject('clamp/'+label, m, lambda: m.clamp(identity, 'maker', 'shelf', 'paperweight'))
    m, identity = built(3); m.world['cargo']['paperweight'].update(unattended=False, willinglyPresented=True)
    before = m.snapshot(); m.clamp(identity, 'maker', 'shelf', 'paperweight')
    check('clamp/willing-presentation-qualifies', m.world['cargo']['paperweight']['attachedTo'] == identity)
    record('clamp/willing-presentation', before, m)

    m, identity = built(4); reject('fan/must-actually-be-held', m, lambda: m.fan(identity, 'maker'))
    before = m.snapshot(); m.transfer(identity, 'maker', 'ally'); m.regular_start('ally', 2)
    result = m.fan(identity, 'ally'); reject('fan/sustaining-needs-another-action', m, lambda: m.fan(identity, 'ally'))
    m.extra_turn('ally'); check('fan/extra-turn-does-not-expire', m.objects[identity]['fan']['endAtRegularStart'] == 3)
    m.regular_start('maker', 2); check('fan/maker-turn-does-not-expire-users-fan', m.objects[identity]['fan'] is not None)
    m.regular_start('ally', 3); check('fan/next-regular-user-start-expires', m.objects[identity]['fan'] is None)
    m.fan(identity, 'ally'); check('fan/another-action-sustains', m.objects[identity]['fan']['endAtRegularStart'] == 4)
    check('fan/utility-only-no-hazard-cure', result['coneFeet'] == 5 and result['damage'] == result['creatureMovement'] == 0 and
          not any(result[k] for k in ['removesRulesGas', 'suffocationRelief', 'hazardImmunity', 'identifiesSubstance']) and
          m.world['unrelatedHazards'] == world['unrelatedHazards'])
    m.advance(4200); check('fan/lifetime-still-controls', m.objects[identity]['fan'] is None and not m.objects[identity]['active'])
    record('fan/held-action-and-regular-user-clock', before, m, result=result)

    for label, change in [('no-hand', lambda m: m.world['actors']['ally'].update(freeHands=0)),
                         ('unwilling', lambda m: m.world['actors']['ally'].update(willingToReceive=False)),
                         ('distant', lambda m: m.world['actors']['ally'].update(position=10)),
                         ('interaction-spent', lambda m: m.world['actors']['maker'].update(interactions=0))]:
        m, identity = built(1); change(m); reject('handoff/'+label, m, lambda: m.transfer(identity, 'maker', 'ally'))
    check('bound-sources-unchanged', bindings == [info(p) for p in paths])
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'four-gadget-construction-and-use-reference-pass',
        'checks': len(checks), 'results': checks, 'failures': [], 'sourceBindings': bindings,
        'cohort': [SID], 'completeOperativeContract': contracts[SID], 'completeProfiles': profiles,
        'conditionalWorldFixture': world, 'traces': traces,
        'counts': {'currentGnomeVariants': 3, 'gadgetProfiles': 4, 'constructionExpiryPairs': 12,
                   'recordedTraces': len(traces), 'newPartialPrerequisiteIdentities': 0},
        'limits': [
            'Source-qualified synthetic Gnome ancestry/ability/Warrior progression and actual paid feat opportunity; not a full character build or authenticated campaign.',
            'Tools, parts ownership/value/access, uninterrupted activity, turn receipts, hearing/contact, object presentation and unobstructed five-foot reach are conditional fixture facts. No inventory or physics engine authenticates them.',
            'Open d4 faces are supplied outcome witnesses; the model rejects choice/reroll/repeated completion but does not provide an RNG or verify an externally rolled die.',
            'The construction milestone is explicitly scheduled at ten minutes. Interruption events must be supplied when work/access fails; this is not an activity monitor.',
            'Ordinary resolved object damage is supplied; attacks, defenses and full object-damage resolution are not re-executed.',
            'Clamp release preserves a required ordinary-fall event. Its trajectory, impact damage and broader support/geometry remain separate.',
            'Dismantling is an explicitly supplied authorized physical event; its ordinary action/time procedure is not invented here.',
            'Fan user regular-start timing is exercised in initiative. Full virtual-marker and outside-initiative clock integration, line of sound/light occlusion and complete hand/cargo systems remain separate.',
            'No full acquisition audit, all-FXC04 closure, complete feat execution, actual GPT verdict, runtime promotion, human balance, publication or cosmology approval is claimed.'],
        'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8', newline='\n')
    notes.write_text('# Contraption Crafter: four temporary gadget procedures\n\n'
        f'{len(checks)} checks pass across {len(traces)} recorded histories. All three current Gnome variants pay an actual Warrior feat opportunity; '
        'all four d4 results receive construction/expiry histories. Parts and the use are committed at the start, interruption refunds neither, '
        'and the next attempt uses 24 elapsed hours rather than midnight or rest. Acquisition supplies no parts, tools or general tool proficiency.\n\n'
        'Lamp light, physical-contact bell, bounded clamp and held fan use their own Actions and limits. Handoffs retain the same identity and deadline; '
        'one damage destroys the HP1 object and spent parts provide no reclaim credit. Tinker Gnome clockwork, class devices, fuel and purchased supplies stay separate.\n\n'
        'Physical access, supplies, work, turns and resolved object damage are conditional fixtures. Clamp release retains an ordinary-fall event for later resolution; '
        'full physics, virtual clock integration and campaign authentication are not claimed. Candidate source rules and approval flags are unchanged.\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(checks), 'failures': 0, 'counts': report['counts'], 'report': info(output), 'notes': info(notes)}, indent=2))


if __name__ == '__main__':
    main()
