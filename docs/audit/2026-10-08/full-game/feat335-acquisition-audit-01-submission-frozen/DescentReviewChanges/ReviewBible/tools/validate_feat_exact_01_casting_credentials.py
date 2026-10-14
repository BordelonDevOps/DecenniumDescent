"""Execute ACQ-03 A-H and finite controls with source-qualified synthetic routes."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_numeric_prerequisite_model import meets_numeric_prerequisite
from feat_exact_01_casting_credential_model import CastingSources, CastingCredentials, school_state

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; A = G / 'docs/audit/2026-10-08/full-game'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def info(p):
    b = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def serial(value):
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(type(value).__name__)


def main():
    output = A / 'FEAT327_ACQ_03_CASTING_CREDENTIAL_CHECK.json'
    notes_path = A / 'FEAT327_ACQ_03_CASTING_CREDENTIAL_NOTES.md'
    assert not output.exists() and not notes_path.exists(), 'Refusing to overwrite prior evidence'
    paths = [Path(__file__), R / 'tools/feat_exact_01_casting_credential_model.py',
        R / 'tools/feat_exact_01_initiate_acquisition_model.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/feat_exact_01_numeric_prerequisite_model.py', R / 'tools/feat_exact_01_training_prerequisite_model.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/public/class_playtests/wizard.json',
        R / 'data/public/feat_candidates/exact_01/spell_dependencies.json', R / 'data/public/feat_candidates/exact_01/supplements.json',
        R / 'data/public/feat_candidates/exact_01/shared_rules.json', A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', A / 'FEAT327_ACQ_03_GPT_RESPONSE.json',
        A / 'FEAT327_ACQ_03_INDEPENDENT_DESCENDANT_CHECK.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[6]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: ability for ability, rows in foundation['skillAbilities'].items() for s in rows}
    ancestry = read(paths[7]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[8])['records']}
    wizard = read(paths[9]); dependencies = read(paths[10])['spells']
    supplements = {x['id']: x['value'] for x in read(paths[11])['groups']}
    contracts = {x['id']: x for x in read(paths[13])['records']}
    actor = read(paths[14])['actorSourceProjection']
    sources = CastingSources(G, dependencies, supplements, wizard)
    results = []; traces = []

    def check(label, truth, kind='bounded-snapshot'):
        results.append({'id': label, 'kind': kind, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def reject(label, operation):
        try:
            operation()
        except (ValueError, KeyError) as exc:
            results.append({'id': label, 'kind': 'rejection', 'passed': True, 'reason': str(exc)})
        else:
            check(label, False, 'rejection')

    def new_initiate(cantrips=None):
        c = InitiateAcquisitions(deepcopy(actor), classes, equipment, skills, ancestry, backgrounds,
                                contracts, supplements['SUP-04'], dependencies)
        c.advance(4); c.earn(4)
        c.acquire('magicInitiate', 4, {'curriculum': 'Wizard', 'cantrips': cantrips or ['friends', 'arcane-ray'], 'rank1': 'find-familiar'})
        c.pay.valid_feat_ids.add(supplements['SUP-05']['newSpellFocus']['id'])
        return c

    generic = contracts['arcaneFocus']['requirements']
    cantrip = contracts['cantrip_mastery']['requirements']
    def access(**kwargs):
        return {'kind': 'actualCastAccess', 'castingPrerequisitePolicyRef': 'FEAT327-ACQ-03', **kwargs}

    def evaluate(label, c, queries):
        before = c.snapshot(); observed = {}
        for name, (node, expected) in queries.items():
            observed[name] = c.matches(node)
            check(label + '/' + name, observed[name] == expected)
        check(label + '/all-state-unchanged', c.snapshot() == before)
        traces.append({'id': label, 'input': before, 'expectedAndObserved': {name: {'node': node, 'expected': expected, 'observed': observed[name]} for name, (node, expected) in queries.items()}, 'qualifyingWitnesses': c.qualifying()})

    def clone(c):
        other = CastingCredentials(sources); other.__dict__.update(c.snapshot()); return other

    check('actual-Wizard-ritual-source', 'automatic at Wizard 2' in wizard['engine'][13] and 'without being prepared' in wizard['engine'][13], 'source-data')
    check('actual-Wizard-book-loss-source', 'Losing the spellbook does not erase matrices currently prepared in memory' in wizard['engine'][8], 'source-data')
    check('source-school-not-authored-for-blast', 'school' not in supplements['SUP-07']['eldritchBlast'], 'source-data')
    check('separate-paid-focus-source', supplements['SUP-05']['newSpellFocus']['id'] == 'proposal_spell_focus' and 'Not repeatable' in supplements['SUP-05']['newSpellFocus']['effect'], 'source-data')
    init = new_initiate(); a = CastingCredentials(sources, 1); a.import_initiate(init, 1)
    evaluate('A-paid-Warrior-Initiate', a, {
        'generic': (generic, True), 'cantrips': (cantrip, True), 'Enchantment': (access(school='Enchantment'), True),
        'Evocation': (access(school='Evocation'), True), 'Universal-rank1': (access(school='Universal', exactRank=1), True),
        'Find-Familiar': (access(spellId='find-familiar'), True), 'no-Dispel': (access(spellId='dispel-magic'), False),
        'no-rank3': (access(minimumRank=3), False), 'no-rank5': (access(minimumRank=5), False),
        'no-field-union': (access(school='Universal', exactRank=0), False),
    })
    check('A-source-class-is-not-Wizard-level-grant', init.snapshot()['actor']['classLevels'] == {'Warrior': 4} and init.rp == {'maximum': 0, 'current': 0}, 'paid-history')
    check('A-exact-three-supported-schools', a.supported_schools() == {'Enchantment', 'Evocation', 'Universal'})
    b = clone(a)
    for charge in b.use_state['renewableCharges'].values():
        charge['current'] = 0
    evaluate('B-conditional-prior-renewable-spend', b, {'Find-Familiar': (access(spellId='find-familiar'), True), 'rank1': (access(exactRank=1), True)})
    check('B-no-refill', all(x['current'] == 0 for x in b.use_state['renewableCharges'].values()))
    c = CastingCredentials(sources, 1)
    c.wizard_snapshot(5, ['friends', 'arcane-ray', 'mage-hand'], ['dispel-magic', 'find-familiar'], ['find-familiar'], 1)
    evaluate('C-Wizard-unprepared-Dispel', c, {'generic': (generic, True), 'cantrip': (cantrip, True),
        'Dispel': (access(spellId='dispel-magic'), False), 'rank3': (access(minimumRank=3), False), 'Abjuration': (access(school='Abjuration'), False)})
    d = CastingCredentials(sources, 1)
    d.wizard_snapshot(5, ['friends', 'arcane-ray', 'mage-hand'], ['dispel-magic', 'find-familiar'], ['dispel-magic'], 1)
    d.use_state['rp'] = 0
    evaluate('D-prepared-Dispel-RP0', d, {'generic': (generic, True), 'Dispel': (access(spellId='dispel-magic'), True),
        'rank3': (access(minimumRank=3), True), 'Abjuration': (access(school='Abjuration'), True),
        'no-rank5': (access(minimumRank=5), False), 'no-school-union': (access(spellId='dispel-magic', school='Universal'), False)})
    e = CastingCredentials(sources, 1); e.wizard_snapshot(2, [], ['find-familiar', 'charm-person'], [], 1)
    evaluate('E-actual-automatic-ritual', e, {'generic': (generic, True), 'Find-Familiar': (access(spellId='find-familiar', school='Universal', exactRank=1), True),
        'no-tag-spread': (access(spellId='charm-person'), False), 'not-a-cantrip': (cantrip, False)})
    first = CastingCredentials(sources, 1); first.wizard_snapshot(1, [], ['find-familiar'], [], 1)
    evaluate('E-no-unacquired-level2-ritual', first, {'no-route': (generic, False)})
    f = clone(b); f.use_state['temporaryBlocks'] = ['missing-components', 'no-hands', 'no-voice', 'unconscious', 'temporary-prohibition', 'suppressed']
    evaluate('F-retained-despite-temporary-blocks', f, {'generic': (generic, True), 'Find-Familiar': (access(spellId='find-familiar'), True)})
    removed = clone(f); removed.moment = 2
    for grant in removed.grants.values():
        grant['removedAt'] = 2
    evaluate('F-conditional-lawful-grant-removal', removed, {'generic': (generic, False), 'Find-Familiar': (access(spellId='find-familiar'), False)})
    init.advance(8); init.earn(8); a.acquire_spell_focus(init.pay, 'Warrior:8', 'Evocation')
    before_choice = deepcopy(init.pay.grants[-1]); retained_focus = clone(removed)
    check('F-later-loss-retains-paid-Focus-choice', init.pay.has('proposal_spell_focus') and init.pay.grants[-1] == before_choice and before_choice['choice'] == 'Evocation', 'paid-history')
    init.advance(12); init.earn(12); before_pay = deepcopy(init.pay.__dict__)
    reject('F-no-new-Focus-school-from-removed-route', lambda: retained_focus.acquire_spell_focus(init.pay, 'Warrior:12', 'Evocation'))
    check('F-rejected-selection-no-payment-change', before_pay == init.pay.__dict__, 'paid-history')
    reject('F-nonrepeatable-Focus-with-retained-route', lambda: a.acquire_spell_focus(init.pay, 'Warrior:12', 'Universal'))
    check('F-nonrepeatable-no-payment-change', before_pay == init.pay.__dict__, 'paid-history')
    pact_pay = PaidChoices({n: x['asiClassLevels'] for n, x in classes.items()}, {}, {'Warrior': 4}, deepcopy(actor['permanentScores']), set(contracts) | {'proposal_spell_focus'})
    pact_pay.earn_class_opportunity('Warrior:4', 'Warrior', 4)
    pact_qualified = meets_numeric_prerequisite(contracts['forbidden_pact']['requirements'], pact_pay.scores, pact_pay.current_classes)
    pact_pay.commit('forbidden_pact', 'Warrior:4', choice={'sigil': 'hex'}, prerequisites_met=pact_qualified)
    g = CastingCredentials(sources, 1); g.import_forbidden_pact(pact_pay, 1, 'hex')
    evaluate('G-paid-school-unassigned-Blast', g, {'generic': (generic, True), 'cantrip': (cantrip, True),
        'no-Enchantment': (access(school='Enchantment'), False), 'no-Evocation': (access(school='Evocation'), False),
        'no-Universal': (access(school='Universal'), False), 'no-rank1': (access(minimumRank=1), False)})
    check('G-source-school-presence-stays-absent', school_state(g.qualifying()[0]) == {'presence': 'absent'})
    pact_pay.current_classes['Warrior'] = 8; pact_pay.earn_class_opportunity('Warrior:8', 'Warrior', 8)
    before_pay = deepcopy(pact_pay.__dict__)
    reject('G-generic-without-supported-school-does-not-buy-Focus', lambda: g.acquire_spell_focus(pact_pay, 'Warrior:8', 'Evocation'))
    check('G-failed-Focus-no-spend', before_pay == pact_pay.__dict__, 'paid-history')
    other = clone(removed); other.grants.update(deepcopy(g.grants)); other.routes.extend(deepcopy(g.routes))
    evaluate('F-independent-retained-route-survives', other, {'generic': (generic, True), 'lost-Find-not-recreated': (access(spellId='find-familiar'), False)})
    h_init = new_initiate(['mage-hand', 'friends']); h = CastingCredentials(sources, 1); h.import_initiate(h_init, 1)
    evaluate('H-reviewed-Mage-Hand-actual-grant', h, {'Mage-Hand': (access(spellId='mage-hand', exactRank=0), True)})
    check('H-original-blocked-live-disabled-remain', dependencies['mage-hand']['originalCatalogRecord']['status'] == 'blocked-pending-operational-review' and dependencies['mage-hand']['completeCurrentProcedureCard']['selectionEnabled'] is False, 'source-data')
    empty = CastingCredentials(sources, 1)
    empty.use_state.update({'rp': 999, 'claimedMaxRank': 9, 'ownedScrolls': ['dispel-magic'], 'claimedBook': ['dispel-magic'], 'classLabel': 'Wizard'})
    sources.ordinary('mage-hand', 'Wizard')
    evaluate('control-catalog-item-pool-label-not-grant', empty, {'generic': (generic, False), 'Dispel': (access(spellId='dispel-magic'), False)})
    future = clone(a)
    for grant in future.grants.values():
        grant['acquiredAt'] = 2
    evaluate('control-prospective-grant-no-bootstrap', future, {'generic': (generic, False)})
    future.moment = 2
    evaluate('control-established-later-snapshot', future, {'generic': (generic, True)})
    substitution = clone(c); before = substitution.snapshot()
    reject('control-future-or-incomplete-substitution', lambda: substitution.substitute('find-familiar', 'dispel-magic', 9))
    check('control-incomplete-substitution-atomic', substitution.snapshot() == before)
    substitution.substitute('find-familiar', 'dispel-magic', 10)
    evaluate('control-completed-source-substitution', substitution, {'Dispel': (access(spellId='dispel-magic'), True), 'independent-Find-ritual': (access(spellId='find-familiar'), True)})
    lost_prepared = clone(d); lost_prepared.book_present = False
    evaluate('control-lost-book-surviving-matrix', lost_prepared, {'Dispel': (access(spellId='dispel-magic'), True), 'unprepared-Find-no-book': (access(spellId='find-familiar'), False)})
    lost_unprepared = clone(c); lost_unprepared.book_present = False
    evaluate('control-lost-unprepared-entry', lost_unprepared, {'Dispel': (access(spellId='dispel-magic'), False)})
    heighten = clone(a); heighten.use_state.update({'claimedRpSpent': 26, 'claimedHeightenRank': 9})
    evaluate('control-price-does-not-change-grant-rank', heighten, {'rank3': (access(minimumRank=3), False), 'rank5': (access(minimumRank=5), False)})
    check('control-null-and-absent-distinct', school_state({}) == {'presence': 'absent'} and school_state({'school': None}) == {'presence': 'null', 'value': None}, 'field-presence')
    for sid in ['astral-projection', 'planar-binding']:
        reject('control-null-pending-payload/' + sid, lambda s=sid: sources.ordinary(s, 'Wizard'))
    reject('control-unsupported-class-version', lambda: sources.ordinary('dispel-magic', 'Warrior'))
    broken_deps = deepcopy(dependencies); broken_deps['mage-hand']['binding']['sha256'] = '0' * 64
    invalid_sources = CastingSources(G, broken_deps, supplements, wizard)
    reject('control-favorable-label-does-not-fix-bad-binding', lambda: invalid_sources.ordinary('mage-hand', 'Wizard'))
    bad_wizard = CastingCredentials(sources, 1)
    reject('control-real-class-rank-gate', lambda: bad_wizard.wizard_snapshot(2, [], ['dispel-magic'], ['dispel-magic'], 1))
    bound_payloads = []
    for filename, (size, digest, _) in sources.cache.items():
        bound_payloads.append({'path': filename, 'bytes': size, 'sha256': digest})
    for bound in bindings + bound_payloads:
        check('unchanged/' + bound['path'], info(G / bound['path']) == bound, 'source-integrity')
    report = {'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-finite-ACQ03-casting-credential-acceptance',
        'sourceBindings': bindings + bound_payloads, 'counts': {'namedAcceptanceGroups': 8, 'recordedSnapshotTraces': len(traces),
            'newlyClosedFullFeatAcquisitions': 0, 'remainingCredentialDependentIdentities': 43},
        'checks': len(results), 'checkKinds': dict(Counter(x['kind'] for x in results)), 'failures': [], 'results': results,
        'traces': traces, 'sourceQualifiedInitiateHistory': init.snapshot(), 'sourceQualifiedForbiddenPactHistory': deepcopy(pact_pay.__dict__),
        'completeWizardEngine': wizard['engine'], 'completeRelevantFeatContracts': [contracts[s] for s in ['magicInitiate', 'forbidden_pact', 'greater_spell_focus']],
        'completeSpellFocusSupplement': supplements['SUP-05']['newSpellFocus'], 'completeBlastProfile': supplements['SUP-07']['eldritchBlast'],
        'completeRitualOverlay': supplements['SUP-05']['newRitualTagOverlay'],
        'completeSelectedSpellEvidence': {s: dependencies[s] for s in ['friends', 'arcane-ray', 'find-familiar', 'dispel-magic', 'mage-hand', 'charm-person']},
        'scope': 'ACQ-03 named synthetic acquisition-snapshot expectations and finite controls. Real paid Magic Initiate, Forbidden Pact and separate Spell Focus histories are generated from bound source inputs. Wizard examples are explicit lawful repertoire subsets, not complete class-card/book builds. Credential evaluation makes no cast and preserves all supplied resources/use blocks.',
        'limits': ['Source files and payload versions are authenticated locally; campaign rolls, ancestry, levels, prior charge spends, lawful grant removals and completed study are authored conditional premises, not authenticated real events.',
            'A depleted renewable charge is supplied as prior state; no earlier spell cast, expenditure, rest or refill is simulated.',
            'Wizard known/book/prepared subsets use actual rank/class gates, actual automatic Ritual Casting and exact overlay. Full acquisition histories for every book entry/class card, every prepared matrix and every ordinary class remain outside this finite bridge test.',
            'The absent-school positive is actual Eldritch Blast. The explicit-null field-presence check is a small classification control, not a newly authored/null-school spell payload.',
            'Grant removal is a stated authorized-removal premise. This model does not create a retraining or source-expiry procedure, authenticate it, or turn a renewable charge into a nonrenewable permission.',
            'Temporary blocks remain real prohibitions on actual use. Passing the casting credential does not by itself authorize selecting a feat while unconscious or otherwise violating a transaction rule.',
            'Actual attack/cast/component/payment/target/strain rules and all noncasting prerequisite branches remain separate. The33 annotated identities are not33 complete acquisitions; the43 remaining-identity ledger is unchanged by this narrow bridge fulfillment.'],
        'finiteBehavioralAcceptanceComplete': True, 'onlyThisNamedIssueClosed': True,
        'all335ActualAcquisitionBoundaryCasesExecuted': False, 'candidateReadyForSubmission': False,
        'candidateExactApproved': False, 'runtimeImplemented': False, 'sourceInformationDeleted': False, 'cosmologyReviewed': False}
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, default=serial); stream.write('\n')
    notes = f'''# ACQ-03 casting prerequisite acceptance\n\n{len(results)} checks pass across the eight named acceptance groups and additional finite controls. The full report records{len(traces)} snapshots with exact source witnesses.\n\nPaid Magic Initiate supplies personal spell credentials without Wizard levels or an RP pool. A spent renewable charge and temporary casting blocks preserve the retained credential, while a genuinely removed grant no longer supports a new acquisition. Evaluation neither spends nor restores resources.\n\nWizard's ordinary unprepared book entry does not qualify. Actually prepared Dispel Magic qualifies at RP0; the exact acquired Wizard2 ritual route permits unprepared Find Familiar. Future study does not anticipate a prepared change, and a lost book preserves only the routes its source actually retains.\n\nActual Eldritch Blast has no school: it supports generic/cantrip predicates, but cannot alone pay for a Spell Focus acquisition with a fictitious school choice. A separate paid Spell Focus fixes a genuinely supported school and retains that historical selection after supporting-grant loss.\n\nReviewed Mage Hand is accepted only with its exact current source binding and an actual personal grant, despite its preserved blocked original and disabled live-selection flag. Unfinished/null payloads, bad bindings, item ownership, RP capacity and future grants do not supply positive witnesses.\n\nThese are source-qualified synthetic acquisition snapshots, not complete characters, actual casts or campaign authentication. Only ACQ-03's finite bridge acceptance is fulfilled. The33 casting-node annotations do not close33 full acquisitions;43 other credential-dependent identities and the complete candidate's selection/use work remain.\n'''
    with notes_path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(notes)
    print(json.dumps({'report': info(output), 'notes': info(notes_path), 'checks': len(results), 'traces': len(traces), 'failures': 0, 'onlyThisNamedIssueClosed': True}, indent=2))


if __name__ == '__main__':
    main()
