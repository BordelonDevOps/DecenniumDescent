"""Execute source-qualified mixed casting prerequisite histories, not feat use."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from feat_exact_01_casting_credential_model import CastingSources
from feat_exact_01_composite_casting_model import CompositeCastingHistory

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def serial(value):
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(type(value).__name__)


def main():
    report_path = A / 'FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_CHECK.json'
    notes_path = A / 'FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_NOTES.md'
    assert not report_path.exists() and not notes_path.exists(), 'Preserve existing evidence; do not overwrite'
    paths = [Path(__file__), R / 'tools/feat_exact_01_composite_casting_model.py',
        R / 'tools/feat_exact_01_casting_credential_model.py', R / 'tools/feat_exact_01_training_prerequisite_model.py',
        R / 'tools/feat_exact_01_initiate_acquisition_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/class_playtests/wizard.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json', A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', A / 'FEAT_EXACT_01_LINEAGE_PREREQUISITE_CHECK.json',
        A / 'FEAT327_ACQ_03_FINITE_FULFILLMENT.json', R / 'data/public/spell_playtests/authored_review_index.json',
        R / 'data/public/spell_playtests/catalog.json', A / 'GPT_HEALING_FINAL_CLOSURE.md']
    bindings = [info(path) for path in paths]
    foundation = read(paths[6]); classes = {x['class']: x for x in foundation['classes']}
    skills = {skill: ability for ability, group in foundation['skillAbilities'].items() for skill in group}
    ancestry = read(paths[7]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[8])['records']}
    wizard = read(paths[9]); dependencies = read(paths[10])['spells']
    supplements = {x['id']: x['value'] for x in read(paths[11])['groups']}
    contracts = {x['id']: x for x in read(paths[13])['records']}
    base_actor = read(paths[14])['actorSourceProjection']; previous = read(paths[15])
    review_index = read(paths[17]); catalog = read(paths[18])
    # One additional current reviewed payload supplies an actual high-rank witness.
    # This is a report-local binding; it does not edit the frozen feat dependencies.
    entry = next(x for x in review_index['entries'] if x['id'] == 'stitch-fate')
    assert entry['authoredStatus'] == 'reviewed-authored-operational-playtest'
    assert entry['procedureFile'] == 'catalog.json' and entry['wholeCardPointer'] == '/spells/280'
    assert info(paths[18])['sha256'] == review_index['sourceCatalogSha256']
    card = catalog['spells'][280]
    assert card['id'] == 'stitch-fate' and card['classAccess']['Wizard']['rank'] == 8
    assert 'docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_CLOSURE.md' in card['operational']['reviewEvidence']
    dependencies = deepcopy(dependencies)
    dependencies['stitch-fate'] = {'id': card['id'], 'originalCatalogRecord': deepcopy(card),
        'authoredIndexEntry': deepcopy(entry), 'completeCurrentProcedureCard': deepcopy(card),
        'binding': {'file': paths[18].relative_to(G).as_posix(), 'bytes': info(paths[18])['bytes'],
                    'sha256': info(paths[18])['sha256'], 'pointer': entry['wholeCardPointer']},
        'grantsNoAccessByItself': True,
        'scope': 'Additional current catalog witness retained only in this report; original source quotations remain inside the whole card.'}
    sources = CastingSources(G, dependencies, supplements, wizard)
    results = []; cases = []; seen = set(); observed = {}

    def check(label, truth, kind='mixed-prerequisite'):
        results.append({'id': label, 'kind': kind, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def reject(label, operation, h=None):
        before = h.snapshot() if h else None
        try:
            operation()
        except (ValueError, KeyError) as exc:
            results.append({'id': label, 'kind': 'rejection', 'passed': True, 'reason': str(exc)})
        else:
            check(label, False, 'rejection')
        if h:
            check(label + '/atomic', h.snapshot() == before, 'history-integrity')

    human = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
    imperial = next(x for x in human['variants'] if x['id'] == 'imperial-human')

    def actor(first='Warrior', nature=False, academy=False, smith=True, scores=None):
        a = deepcopy(base_actor); a['firstClass'] = first; a['classLevels'] = {first: 1}
        if first == 'Warrior':
            a['selectedClassSkills'] = ['Nature' if nature else 'Animal Handling', 'Athletics']
        elif first == 'Monk':
            a['selectedClassSkills'] = ['Athletics', 'Insight']
            a['classToolChoices'] = ['tools.smith-s-tools' if smith else 'tools.carpenter-s-tools']
        elif first == 'Bard':
            a['selectedClassSkills'] = ['Engineering', 'Nature', 'Investigation']
            a['classToolChoices'] = ['tools.flute', 'tools.drum', 'tools.lute']
        elif first == 'Wizard':
            a['selectedClassSkills'] = ['Insight', 'Investigation']
            a['scope'] = 'Explicit Wizard class-level, ability and repertoire subset only; starting training, class-card selections and complete book history are not projected.'
        else:
            raise ValueError(first)
        if academy:
            a['background'] = 'arcane-academy-dropout'; a['backgroundToolChoice'] = None
            a['backgroundDuplicateSkillChoice'] = None
        for ability, score in (scores or {}).items():
            bonus = imperial['combinedAbilityBonuses'][ability]
            dice = next(d for d in product(range(1, 7), repeat=4) if sum(d) - min(d) + bonus == score)
            a['abilityRolls'][ability] = list(dice); a['permanentScores'][ability] = score
        return a

    def history(first='Warrior', **kwargs):
        return CompositeCastingHistory(actor(first, **kwargs), classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)

    def initiate(level=8, **kwargs):
        h = history(**kwargs); h.advance(4); h.earn(4); h.initiate(); h.advance(level)
        return h

    def wizard_history(level=8, known=None, book=None, prepared=None, scores=None):
        h = history('Wizard', scores=scores); h.advance(level)
        h.wizard(['friends', 'arcane-ray'] if known is None else known,
                 ['find-familiar'] if book is None else book,
                 [] if prepared is None else prepared)
        return h

    def case(label, h, expectations, gate=None):
        assert label not in seen; seen.add(label)
        level = h.actor['classLevels'][h.first]; opportunity = h.first + ':' + str(level)
        scheduled = level in classes[h.first]['asiClassLevels']
        if scheduled and opportunity not in h.pay.opportunities:
            h.earn(level)
        before = h.snapshot(); rows = []
        for sid, expected in expectations.items():
            actual = h.prerequisite(sid)
            check(label + '/' + sid, actual == expected)
            expected_gate = expected if gate is None else expected and gate
            got_gate = h.gate(sid, opportunity)
            check(label + '/' + sid + '/earned-unspent', got_gate == expected_gate, 'opportunity-gate')
            rows.append({'id': sid, 'printedPrerequisite': contracts[sid]['printedPrerequisite'],
                         'expected': expected, 'observed': actual, 'expectedGate': expected_gate, 'observedGate': got_gate})
            observed.setdefault(sid, set()).add(actual)
        check(label + '/no-query-state-change', before == h.snapshot(), 'history-integrity')
        cases.append({'id': label, 'history': before, 'opportunity': opportunity,
                      'qualifyingSpellWitnesses': h.casting.qualifying(), 'expectations': rows})

    simple = [sid for sid, c in contracts.items() if c['requirements']['kind'] == 'actualSpellcastingRoute']
    check('printed-simple-casting-sources', all(contracts[s]['printedPrerequisite'] in {'Spellcasting ability', 'Ability to cast at least one spell'} for s in simple), 'source-data')
    case('retained-paid-Initiate-generic', initiate(), dict.fromkeys(simple, True))
    no_cast = history(); no_cast.advance(8)
    case('no-personal-route', no_cast, dict.fromkeys(simple, False))
    for sid, minimum in [('arcaneResonance', 3), ('metamagicAdept', 4), ('spellPenetration', 5), ('spell_reflection', 8)]:
        for level in dict.fromkeys([minimum - 1, minimum, 8]):
            case(sid + '/level' + str(level), wizard_history(level), {sid: level >= minimum}, gate=level in classes['Wizard']['asiClassLevels'])
    for sid, ability, minimum in [('arcane_adaptation', 'INT', 13), ('mimicry', 'INT', 15), ('curse_weaving', 'CHA', 13)]:
        for score in [minimum - 1, minimum]:
            h = initiate(scores={ability: score})
            h.actor['temporaryBonuses'] = {ability: 99}
            case(sid + '/permanent' + str(score), h, {sid: score >= minimum})
        case(sid + '/score-without-route', no_cast, {sid: False})
    case('Warrior-martial-and-casting', initiate(), {'battleMage': True, 'eldritch_combat': True})
    case('Warrior-martial-without-casting', no_cast, {'battleMage': False, 'eldritch_combat': False})
    monk = history('Monk'); monk.advance(4); monk.earn(4); monk.acquire_parent('forbidden_pact', 4, {'sigil': 'hex'}); monk.advance(8)
    case('Monk-Pact-no-martial-profile', monk, {'battleMage': False, 'eldritch_combat': False})
    case('Initiate-exact-cantrip-name-school', initiate(), {'cantrip_mastery': True, 'familiar_bond': True, 'enchantment_focus': True, 'evocation_focus': True, 'dispel_mastery': False, 'elemental_mastery': False, 'heighten_spell': False})
    case('Wizard-exact-ritual-not-cantrip', wizard_history(8, known=[]), {'cantrip_mastery': False, 'familiar_bond': True})
    case('Pact-no-assigned-school-or-familiar', monk, {'cantrip_mastery': True, 'familiar_bond': False, 'enchantment_focus': False, 'evocation_focus': False})
    for prepared in [[], ['dispel-magic']]:
        h = wizard_history(8, known=[], book=['dispel-magic'], prepared=prepared)
        h.casting.use_state['rp'] = 0
        case('Wizard-Dispel-' + ('prepared' if prepared else 'unprepared'), h,
             dict.fromkeys(['dispel_mastery', 'elemental_mastery', 'heighten_spell'], bool(prepared)))
    for score, prep in [(15, True), (14, True), (15, False)]:
        h = wizard_history(16, known=[], book=['stitch-fate'], prepared=['stitch-fate'] if prep else [], scores={'CHA': score})
        case('rank8-CHA' + str(score) + '-prepared' + str(prep), h, {'planar_binding': score >= 15 and prep})
    h = wizard_history(16, known=[], book=['dispel-magic'], prepared=['dispel-magic'])
    case('rank3-with-high-maximum-is-not-rank5', h, {'planar_binding': False})
    check('deferred-Planar-payload-not-activated', 'null and unavailable' in contracts['planar_binding']['payloadAvailability'] and contracts['planar_binding']['candidateSelectionEnabled'] is False, 'source-data')
    for nature, cast in [(True, True), (True, False), (False, True), (False, False)]:
        h = initiate(nature=nature) if cast else history(nature=nature)
        h.advance(8)
        case('Nature' + str(nature) + '-casting' + str(cast), h, {
            'conjure_flora': nature and cast, 'verdant_bond': nature and cast,
            'stormcaller': nature and cast, 'lightning_affinity': nature or cast})
    h = initiate(academy=True)
    case('Arcana-is-not-legacy-Spellcraft', h, {'stormcaller': False})
    case('Smith-with-paid-Pact', monk, {'core_infusion': True})
    engineer = history('Monk'); engineer.advance(4); engineer.earn(4)
    engineer.acquire_parent('skill_expert', 4, {'newSkill': 'Engineering', 'expertiseSkill': 'Engineering'}); engineer.advance(8)
    case('Smith-and-paid-Engineering-without-casting', engineer, {'core_infusion': True})
    h = history('Monk'); h.advance(8)
    case('Smith-without-either-alternative', h, {'core_infusion': False})
    h = history('Monk', smith=False); h.advance(4); h.earn(4); h.acquire_parent('forbidden_pact', 4, {'sigil': 'hex'}); h.advance(8)
    case('Pact-without-Smith', h, {'core_infusion': False})
    h = history('Bard'); h.advance(8)
    case('Engineering-without-Smith', h, {'core_infusion': False})
    for alternative in ['actual-casting', 'actual-Arcana', 'neither']:
        for level in [5, 6, 8]:
            h = initiate(level) if alternative == 'actual-casting' else history(academy=alternative == 'actual-Arcana')
            h.advance(level)
            case('Curse/' + alternative + '/level' + str(level), h, {'curse_channeling': alternative != 'neither' and level >= 6}, gate=level == 8)
    for parent in ['power_attack', 'combatCasting']:
        h = initiate(); h.earn(8); h.acquire_parent(parent, 8); h.advance(12)
        case('Momentum-paid-' + parent, h, {'arcane_momentum': True})
        h.remove_personal_routes()
        case('Momentum-' + parent + '-without-retained-casting', h, {'arcane_momentum': False})
    case('Momentum-casting-alone', initiate(), {'arcane_momentum': False})
    h = history(); h.advance(4); h.earn(4); h.acquire_parent('power_attack', 4); h.advance(8)
    case('Momentum-power-alone', h, {'arcane_momentum': False})
    case('Echo-casting-alternative', initiate(), {'eldritch_echo': True})
    case('Echo-neither', no_cast, {'eldritch_echo': False})
    case('Echo-under-level', wizard_history(2), {'eldritch_echo': False}, gate=False)
    h = history(); h.advance(4); h.earn(4); h.acquire_parent('forbidden_pact', 4, {'sigil': 'hex'}); h.advance(8); h.remove_personal_routes()
    case('Echo-retained-paid-parent-after-route-loss', h, {'eldritch_echo': True})
    case('Soul-Cage-casting-alternative', initiate(), {'soul_cage': True})
    case('Soul-Cage-neither', no_cast, {'soul_cage': False})
    case('Soul-Cage-under-level', initiate(7), {'soul_cage': False}, gate=False)
    h = initiate(); h.earn(8); h.acquire_parent('lifeleech', 8); h.advance(12); h.remove_personal_routes()
    case('Soul-Cage-retained-paid-Lifeleech-after-route-loss', h, {'soul_cage': True})
    check('Lifeleech-acquisition-no-reserve-refill', h.initializations['lifeleech']['recoveryReserveCurrent'] == 0, 'source-initialization')
    focus = initiate(); focus.earn(8); focus.spell_focus(8, 'Evocation'); focus.advance(12)
    case('Greater-Focus-real-paid-fixed-school', focus, {'greater_spell_focus': True})
    focus.remove_personal_routes()
    case('Greater-Focus-retains-parent-after-route-loss', focus, {'greater_spell_focus': True})
    check('Greater-Focus-fixed-school-history', focus.pay.grants[-1]['choice'] == 'Evocation', 'paid-history')
    h = initiate(); h.earn(8); h.acquire_parent('evocation_focus', 8); h.advance(12)
    case('Evocation-Focus-is-not-supplement-Spell-Focus', h, {'greater_spell_focus': False})
    case('Greater-Focus-casting-alone', initiate(), {'greater_spell_focus': False})
    h = initiate(4)
    case('spent-Initiate-opportunity-cannot-pay-another-feat', h, {'arcaneFocus': True}, gate=False)
    h = initiate(); h.earn(8); h.acquire_parent('combatCasting', 8)
    case('spent-parent-opportunity-cannot-pay-child', h, {'arcane_momentum': True}, gate=False)
    before = h.snapshot()
    reject('duplicate-paid-Combat-Casting', lambda: h.acquire_parent('combatCasting', 8), h)
    reject('no-invented-off-schedule-opportunity', lambda: h.earn(7), h)
    no_pact = history(scores={'CHA': 12}); no_pact.advance(4); no_pact.earn(4)
    reject('Pact-requires-its-own-permanent-CHA', lambda: no_pact.acquire_parent('forbidden_pact', 4, {'sigil': 'hex'}), no_pact)
    reject('Wizard-repertoire-is-not-a-training-projection', lambda: wizard_history().prerequisite('core_infusion'))
    # Derive the covered set from current contracts rather than from fixture names.
    def contains(node):
        return node['kind'] in {'actualSpellcastingRoute', 'actualCastAccess'} or any(contains(c) for c in node.get('requirements', []))
    cohort = {sid for sid, contract in contracts.items() if contains(contract['requirements'])} | {'greater_spell_focus'}
    check('exact-cohort34', len(cohort) == 34 and set(observed) == cohort, 'coverage')
    check('positive-and-negative-each-identity', all(observed[sid] == {False, True} for sid in cohort), 'coverage')
    prior_remaining = {x['id'] for x in previous['remaining']}
    check('cohort-disjoint-from-earlier292', len(prior_remaining) == 43 and cohort <= prior_remaining, 'coverage')
    remaining = [contracts[sid] for sid in contracts if sid in prior_remaining - cohort]
    check('nine-remain-in-this-partial-predicate-ledger', len(remaining) == 9, 'coverage')
    additional = [{'path': filename, 'bytes': size, 'sha256': digest} for filename, (size, digest, _) in sources.cache.items() if filename not in {b['path'] for b in bindings}]
    for bound in bindings + additional:
        check('unchanged/' + bound['path'], info(G / bound['path']) == bound, 'source-integrity')
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'passed-finite-combined-casting-and-owned-supplement-prerequisite-projections',
        'sourceBindings': bindings + additional, 'cohort': sorted(cohort), 'completeSourceContracts': [contracts[sid] for sid in contracts if sid in cohort],
        'completeParentContracts': [contracts[sid] for sid in ['magicInitiate', 'power_attack', 'combatCasting', 'lifeleech', 'forbidden_pact', 'evocation_focus', 'skill_expert']],
        'completeSpellFocusSupplement': supplements['SUP-05']['newSpellFocus'],
        'additionalSourceQualifiedPayload': dependencies['stitch-fate'],
        'counts': {'newPartialPrerequisiteIdentities': 34, 'cumulativePartialPrerequisiteIdentities': 326,
            'remainingCredentialDependentIdentities': 9, 'recordedCases': len(cases),
            'prerequisiteComparisons': sum(len(c['expectations']) for c in cases), 'newlyClosedFullFeatAcquisitions': 0},
        'cases': cases, 'checks': len(results), 'checkKinds': dict(Counter(x['kind'] for x in results)), 'failures': [], 'results': results,
        'remaining': [{'id': c['id'], 'name': c['name'], 'printedPrerequisite': c['printedPrerequisite'], 'requirements': c['requirements']} for c in remaining],
        'scope': 'Actual current casting trees combined with permanent scores, source class levels, actual training and paid parent ownership, plus a separate earned-unspent opportunity gate. Expectations are explicit finite source cases. Target feats are not purchased merely because these necessary gates pass.',
        'limits': [
            'These are conditional authored histories. Source bindings authenticate files, not real campaign rolls, levels, grant removal, study or awards.',
            'Wizard witnesses are explicit legal repertoire/ability/class-level subsets, not complete characters or book/class-card acquisition histories. Training queries on that slice raise rather than interpreting omitted training as absent.',
            'The current rank8 Stitch Fate source supplies the positive minimum-rank5 witness. This is not an exact-rank5 boundary witness; no new rank5 spell or pending payload is authored. Actual prepared rank3 and an unprepared high-rank book entry supply negatives.',
            'Planar Binding receives an external prerequisite projection only. Its null spell payload stays unavailable, original objects and selection flags stay unchanged, and no cosmology is reviewed.',
            'Current Nature supplies the Stormcaller alternative; no positive legacy Spellcraft character is supplied or invented. Arcana is not silently aliased to it.',
            'Paid Lifeleech history initializes zero recovery reserve; its later rest/capacity/healing/death procedures are not executed by this acquisition predicate pass.',
            'The34 new identities extend disjoint partial prerequisite bookkeeping only. They do not establish34 complete target acquisitions, all choices, use procedures, every boundary, exact-candidate approval, runtime correctness or human balance.',
        ],
        'allCohortCompleteAcquisitionsValidated': False, 'candidateReadyForSubmission': False,
        'newRulesAdopted': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False}
    with report_path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, default=serial); stream.write('\n')
    notes = f'''# Combined casting prerequisites

{len(results)} checks pass across {len(cases)} explicit source-qualified histories/snapshots. All 33 casting-bearing prerequisite trees and Greater Spell Focus have positive and negative finite cases, with their actual earned, unspent opportunity gate assessed separately.

The combined rules preserve independent requirements and alternatives: martial training is not inferred from spell access; Core Infusion still needs smith's tools; Arcana can satisfy Curse Channeling's alternative without casting; Nature can satisfy Lightning Affinity; Arcana is not legacy Spellcraft. Paid parent histories support Arcane Momentum, Eldritch Echo, Soul Cage and Greater Spell Focus without granting unpaid parents or erasing independent requirements.

Magic Initiate retains its classless source placements. Actual prepared Wizard Dispel Magic supplies rank3; unprepared ordinary entries do not. The reviewed rank8 Stitch Fate supplies a minimum-rank5 witness, while Planar Binding's own payload remains null and unusable. No exact-rank5 positive boundary or spell activation is claimed.

The disjoint partial-prerequisite ledger now covers 326 identities and leaves 9: {', '.join(c['id'] for c in remaining)}. These are necessary-gate projections, not 326 complete acquisitions. Required choices, use/resource procedures, broader character histories, remaining legacy/context credentials and the complete exact candidate review remain outstanding.

All bound source bytes remain unchanged. No game rule, approval flag, historical source, runtime selection or cosmology changed.
'''
    with notes_path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(notes)
    print(json.dumps({'report': info(report_path), 'notes': info(notes_path), 'checks': len(results), 'cases': len(cases), 'failures': 0, 'newPartialIdentities': 34, 'remaining': len(remaining)}, indent=2))


if __name__ == '__main__':
    main()
