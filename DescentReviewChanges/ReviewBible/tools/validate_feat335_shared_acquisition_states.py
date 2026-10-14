"""Missing finite AA12/14 order histories; unchanged AA13 evidence is reused."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat335_shared_acquisition_states import SharedAcquisitionStates, BLAST, SHARED_BLAST
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'


def main():
    output = A/'FEAT335_SHARED_ACQUISITION_STATE_CHECK.json'
    assert not output.exists(), 'Existing evidence is immutable'
    paths = [R/'data/playtest/character_foundation.json', R/'data/playtest/ancestry_background_candidate.json',
        R/'data/playtest/equipment_source_catalog.json', R/'data/public/feat_candidates/exact_01/supplements.json',
        R/'data/public/feat_candidates/exact_01/spell_dependencies.json', R/'data/public/class_playtests/wizard.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R/'data/public/feat_candidates/exact_01/candidate.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',
        A/'feat335-acquisition-audit-01-verdict/ACCEPTANCE_EXPECTATIONS.json',
        A/'feat335-acquisition-audit-01-verdict/FINITE_REMAINING_WORK.json',
        Path(__file__), R/'tools/feat335_shared_acquisition_states.py',
        *[R/'tools'/n for n in ['feat_exact_01_casting_selections.py', 'feat_exact_01_remaining_owned_chains.py',
            'feat_exact_01_composite_casting_model.py', 'feat_exact_01_casting_credential_model.py',
            'feat_exact_01_acquisition_models.py', 'feat_exact_01_initiate_acquisition_model.py',
            'feat_exact_01_training_prerequisite_model.py']]]
    bindings = [info(p) for p in paths]
    foundation, ancestry, equipment_doc, supplement_doc, dep_doc, wizard, contract_doc, initiate_report = [read(p) for p in paths[:8]]
    classes = {x['class']: x for x in foundation['classes']}
    skills = {s:a for a, group in foundation['skillAbilities'].items() for s in group}
    equipment = {x['id']:x for x in equipment_doc['records']}
    backgrounds = {x['id']:x for x in ancestry['backgrounds']}
    contracts = {x['id']:x for x in contract_doc['records']}
    supplements = {x['id']:x['value'] for x in supplement_doc['groups']}
    sources = CastingSources(G, dep_doc['spells'], supplements, wizard)
    public = {x['id']:x for x in read(paths[8])['feats']}
    checks = []; histories = []

    def check(label, actual, expected=True):
        entry = {'id': label, 'actual': deepcopy(actual), 'expected': deepcopy(expected), 'passed': actual == expected}
        checks.append(entry)
        assert entry['passed'], label

    def rejected(label, h, action, reason):
        before = h.snapshot()
        try: action()
        except ValueError as error: check(label+'/reason', reason in str(error))
        else: check(label+'/rejects', False)
        check(label+'/atomic', h.snapshot(), before)

    def new(casting=True):
        actor = deepcopy(initiate_report['actorSourceProjection'])
        actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Nature', 'Athletics'])
        h = SharedAcquisitionStates(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        if casting:
            h.advance(4); h.earn(4); h.initiate()
        return h

    def op(h, level):
        h.advance(level); h.earn(level)

    def soul(h, sid, level):
        return h.acquire_soul_source(sid, level, {'provider': h.providers()[0]} if sid == 'soul_cage' else None)

    def record(label, start, h, **extra):
        histories.append({'id':label, 'before':start, 'after':h.snapshot(), **extra})

    for sid in ['lifeleech', 'soul_cage', 'forbidden_pact', 'eldritch_echo']:
        p = public[sid].get('unchangedReviewedRecord', public[sid])
        check(sid+'/complete-procedure-join', contracts[sid]['completeOperativeProcedure'], p['operationalRules'])
    check('exact-blast-source-ability', supplements['SUP-07']['eldritchBlast']['castingAbility'],
          'CHA; both feat grants share this one source ability/identity, not two selectable histories.')
    check('no-blast-school-inference', 'school' not in supplements['SUP-07']['eldritchBlast'])
    check('duplicate-blast-no-replay-source', 'Duplicate grant creates no duplicate spell, price waiver, resource pool, known-spell count or separate Refrain.' in supplements['SUP-07']['eldritchBlast']['grant'])

    for order in [('soul_cage', 'lifeleech'), ('lifeleech', 'soul_cage')]:
        for remaining in [0, 1, 2, 3]:
            h = new(); start = h.snapshot(); op(h, 8)
            first, second = order; tag = first+'-then-'+second+'/'+str(remaining)
            casting_before = h.casting.snapshot()
            first_grant = soul(h, first, 8)
            pool = h.initializations['sharedSoulCharges']
            check(tag+'/first-owner-creates-zero-only', pool, {'maximum':3, 'current':0, 'evaluatedDeathEvents':[], 'bodyEpochEntitlements':[]})
            check(tag+'/first-acquisition-is-no-cast', h.casting.snapshot(), casting_before)
            # Explicit conditional prior spent/capture journals test retention only.
            pool.update(current=remaining,
                evaluatedDeathEvents=[{'event':'conditional-death-A', 'alreadyEvaluated':True}],
                bodyEpochEntitlements=[{'body':'conditional-body-A', 'epoch':2, 'consumed':True}])
            pool['conditionalImportProvenance'] = 'Given source-valid persistent state; no actual death or collection simulated'
            before_pool = deepcopy(pool)
            if first == 'soul_cage':
                h.initializations['soul_cage']['actualBlackCrystalRef'] = 'conditional-existing-crystal-ref'
            else:
                h.initializations['lifeleech']['recoveryReserveCurrent'] = 5
                h.initializations['lifeleech']['noLongRestSimulated'] = True
                h.initializations['lifeleech']['conditionalPriorReserve'] = 'Given spent reserve; no rest simulated'
            first_state = deepcopy(h.initializations[first])
            op(h, 12); second_grant = soul(h, second, 12)
            check(tag+'/same-owner-pool-object', h.initializations['sharedSoulCharges'] is pool)
            check(tag+'/whole-pool-journals-retained', h.initializations['sharedSoulCharges'], before_pool)
            check(tag+'/first-source-state-retained', h.initializations[first], first_state)
            check(tag+'/distinct-earned-payments', [first_grant['opportunity'], second_grant['opportunity']], ['Warrior:8', 'Warrior:12'])
            check(tag+'/Lifeleech-reserve-separate', 'sharedSoulCharges' not in h.initializations['lifeleech'])
            if second == 'lifeleech':
                check(tag+'/new-Lifeleech-empty-not-level-full', h.initializations[second]['recoveryReserveCurrent'], 0)
            else: check(tag+'/new-Cage-no-crystal', h.initializations[second]['actualBlackCrystalRef'], None)
            retained = deepcopy(h.initializations); op(h, 16)
            rejected(tag+'/no-repeat-or-reinitialization', h, lambda: soul(h, second, 16), 'Nonrepeatable identity already acquired')
            check(tag+'/level-increase-does-not-refill', h.initializations, retained)
            record(tag, start, h, conditionalPriorJournal=True, noDeathRestCaptureOrItemCreation=True)

    h = new(False); start = h.snapshot(); op(h, 8)
    rejected('Lifeleech-cannot-bootstrap-casting', h, lambda: h.acquire_soul_source('lifeleech', 8), 'Prerequisites not established')
    rejected('Cage-no-provider-no-free-pool', h, lambda: h.acquire_soul_source('soul_cage', 8, {'provider':{'ability':'INT'}}), 'Printed current acquisition predicate not established')
    record('missing-real-casting-credential', start, h)
    for invalid in [{'maximum':3,'current':4,'evaluatedDeathEvents':[],'bodyEpochEntitlements':[]},
                    {'maximum':3,'current':True,'evaluatedDeathEvents':[],'bodyEpochEntitlements':[]},
                    {'maximum':3,'current':2,'evaluatedDeathEvents':None,'bodyEpochEntitlements':[]}]:
        h = new(); op(h, 8); soul(h, 'soul_cage', 8); op(h, 12)
        h.initializations['sharedSoulCharges'] = deepcopy(invalid)
        rejected('invalid-import/'+str(invalid), h, lambda: h.acquire_soul_source('lifeleech', 12), 'valid existing shared Soul Charge pool')

    for order in [('forbidden_pact', 'eldritch_echo'), ('eldritch_echo', 'forbidden_pact')]:
        # Pact can be the first casting source; Echo-first uses genuinely paid Initiate.
        for sigil in ['hex', 'shadowstep', 'energyResistance']:
            first, second = order
            h = new(casting=first == 'eldritch_echo'); start = h.snapshot()
            first_level = 8 if first == 'eldritch_echo' else 4
            second_level = first_level+4
            tag = first+'-then-'+second+'/'+sigil
            pact_choice = {'sigil':sigil, **({'damageType':'cold'} if sigil == 'energyResistance' else {})}
            op(h, first_level)
            initial_use = deepcopy(h.casting.use_state)
            first_grant = h.acquire_blast_source(first, first_level, pact_choice if first == 'forbidden_pact' else None)
            routes = [r for r in h.casting.qualifying() if r['spellId'] == BLAST]
            check(tag+'/first-one-exact-blast', len(routes), 1)
            check(tag+'/first-no-RP-strain-history-change', h.casting.use_state, initial_use)
            check(tag+'/no-class-or-repertoire-grant', [h.pay.current_classes, h.casting.known, h.casting.book, h.casting.prepared, h.casting.wizard_level],
                  [{'Warrior':first_level}, set(), set(), set(), 0])
            check(tag+'/one-CHA-rank0-unassigned-school', routes[0]['rank'] == 0 and routes[0]['ability'] == 'CHA' and 'school' not in routes[0] and 'sourceClass' not in routes[0])
            first_acquired = h.casting.grants[SHARED_BLAST]['acquiredAt']
            h.casting.use_state.update(rp=0, conditionalPriorDissonance=3,
                conditionalPriorRefrain={BLAST:2}, conditionalCastRoots=['conditional-old-blast-root'])
            if first == 'forbidden_pact':
                h.initializations[first]['spentSubstitutionEncounterIds'] = ['conditional-previous-encounter']
                if 'sigilAllowance' in h.initializations[first]: h.initializations[first]['sigilAllowance']['current'] = 0
            else:
                h.initializations[first]['captureUses']['current'] = 0
                h.initializations['pendingFeatCopy'] = {'sourceEvent':'conditional-old-copy', 'profile':'strike', 'expires':'conditional-next-turn'}
            first_state = deepcopy(h.initializations)
            use_before = deepcopy(h.casting.use_state)
            source_routes_before = deepcopy([r for r in h.casting.routes if r['spellId'] != BLAST])
            op(h, second_level)
            second_grant = h.acquire_blast_source(second, second_level, pact_choice if second == 'forbidden_pact' else None)
            check(tag+'/second-no-RP-or-strain-reset', h.casting.use_state, use_before)
            check(tag+'/original-grant-state-preserved', {k:h.initializations[k] for k in first_state}, first_state)
            check(tag+'/other-spell-routes-preserved', [r for r in h.casting.routes if r['spellId'] != BLAST], source_routes_before)
            blast_routes = [r for r in h.casting.qualifying() if r['spellId'] == BLAST]
            check(tag+'/second-does-not-duplicate-route-or-spell', len(blast_routes), 1)
            check(tag+'/same-source-ability-payload', blast_routes[0], routes[0])
            check(tag+'/first-acquired-time-not-replayed', h.casting.grants[SHARED_BLAST]['acquiredAt'], first_acquired)
            check(tag+'/both-paid-source-journals-retained', [x['identity'] for x in h.casting.grants[SHARED_BLAST]['paidSources']], list(order))
            check(tag+'/different-paid-opportunities', [first_grant['opportunity'], second_grant['opportunity']],
                  ['Warrior:'+str(first_level), 'Warrior:'+str(second_level)])
            check(tag+'/no-RP-class-source-created', h.pay.current_classes, {'Warrior':second_level})
            if second == 'eldritch_echo':
                check(tag+'/new-capture-allowance-full-no-capture', [h.initializations[second]['captureUses']['current'],h.initializations['pendingFeatCopy']], [1,None])
            op(h, 16)
            rejected(tag+'/duplicate-acquisition-no-replay', h,
                lambda: h.acquire_blast_source(second, 16, pact_choice if second == 'forbidden_pact' else None), 'Nonrepeatable identity already acquired')
            record(tag, start, h, conditionalPriorJournal=True, noCastCaptureReleaseRestOrEncounterCreated=True)

    h = new(False); start = h.snapshot(); op(h, 4)
    rejected('Echo-cannot-bootstrap-with-own-future-blast', h, lambda: h.acquire_blast_source('eldritch_echo', 4), 'Prerequisites not established')
    record('Echo-missing-parent-and-casting', start, h)
    h = new(False); start = h.snapshot(); op(h, 4)
    h.acquire_blast_source('forbidden_pact', 4, {'sigil':'hex'})
    rejected('Pact-and-Echo-cannot-share-payment', h, lambda: h.acquire_blast_source('eldritch_echo', 4), 'No unspent earned opportunity')
    record('shared-identity-does-not-share-payment', start, h)

    check('source-bindings-unchanged-during-run', [info(p) for p in paths], bindings)
    result = {'recordedAtUtc':datetime.now(timezone.utc).isoformat(), 'status':'pass', 'checks':len(checks),
        'failures':[], 'acceptanceGroups':['AA-12','AA-14'], 'historyCount':len(histories),
        'sourceBindings':bindings, 'results':checks, 'histories':histories,
        'scope':'Paid, source-qualified shared-owner acquisition orders only. Prior charge/strain/death/cast/body state is conditional fixture input; no actual use/death/rest/campaign proof.',
        'remainingFW05':'Bind already-existing AA13 Hemo-empty/Life-Drinker-full and spent-plus-new-superiority evidence into assembly; do not demand redundant executions.',
        'limits':['No individual blast-source removal/reacquisition model; this evidence covers retained-source acquisition orders.',
                  'No feat runtime, player balance, full335 assembly approval or cosmology review.'],
        'newGameRules':0, 'sourceInformationDeleted':0, 'fullFeatCandidateApproved':False}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8')
    print(json.dumps({'checks':len(checks),'histories':len(histories),'report':info(output)}))


if __name__ == '__main__':
    main()
