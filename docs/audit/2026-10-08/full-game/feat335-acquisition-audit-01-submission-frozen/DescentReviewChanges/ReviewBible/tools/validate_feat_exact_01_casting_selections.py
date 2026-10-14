"""Source-bound eleven-feat permanent casting/route selection evidence."""
from copy import deepcopy
from datetime import datetime, timezone
from itertools import product
import json
from pathlib import Path
from feat_exact_01_casting_selections import CastingSelections, MENTAL, ELEMENTS, COHORT
from feat_exact_01_casting_credential_model import CastingSources
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    target = A / 'FEAT_EXACT_01_CASTING_SELECTIONS_CHECK.json'
    notes = A / 'FEAT_EXACT_01_CASTING_SELECTIONS_NOTES.md'
    assert not target.exists() and not notes.exists()
    paths = {'foundation': R / 'data/playtest/character_foundation.json',
        'ancestry': R / 'data/playtest/ancestry_background_candidate.json',
        'equipment': R / 'data/playtest/equipment_source_catalog.json',
        'wizard': R / 'data/public/class_playtests/wizard.json',
        'dependencies': R / 'data/public/feat_candidates/exact_01/spell_dependencies.json',
        'supplements': R / 'data/public/feat_candidates/exact_01/supplements.json',
        'shared': R / 'data/public/feat_candidates/exact_01/shared_rules.json',
        'contracts': A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        'actor': A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        'coreProposal': R / 'data/director/magic_core_feat_operating_proposal_internal.json',
        'sourceVerdict': A / 'feat327-source-verdict/FEAT_SUPPLEMENT_DIRECTIONS.json',
        'currentPublic': R / 'data/public/feat_candidates/exact_01/candidate.json',
        'currentInternal': R / 'data/director/feat_candidates/exact_01/candidate.json',
        'ACQ03': A / 'FEAT327_ACQ_03_GPT_ADDENDUM.md'}
    bound_paths = list(paths.values()) + [Path(__file__)] + [R / 'tools' / n for n in [
        'feat_exact_01_casting_selections.py', 'feat_exact_01_remaining_owned_chains.py',
        'feat_exact_01_composite_casting_model.py', 'feat_exact_01_casting_credential_model.py',
        'feat_exact_01_initiate_acquisition_model.py', 'feat_exact_01_training_prerequisite_model.py',
        'feat_exact_01_acquisition_models.py', 'validate_feat_exact_01_composite_casting.py']]
    bindings = [info(p) for p in bound_paths]
    foundation = read(paths['foundation']); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths['ancestry']); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths['equipment'])['records']}
    supplements = {x['id']: x['value'] for x in read(paths['supplements'])['groups']}
    dependencies = read(paths['dependencies'])['spells']
    sources = CastingSources(G, dependencies, supplements, read(paths['wizard']))
    contracts = {x['id']: x for x in read(paths['contracts'])['records']}
    core = read(paths['coreProposal']); actor_source = read(paths['actor'])['actorSourceProjection']
    results = []; traces = []; placement_checks = []; cohort_seen = set()

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth: raise AssertionError(label)

    def capture(label, h, premise=None):
        traces.append({'id': label, 'state': h.snapshot(), 'conditionalPremises': premise or [],
            'scope': 'Actual source-qualified acquisition slice, not full class/feat use or authenticated campaign.'})

    def reject(label, h, call):
        before = h.snapshot()
        try: call()
        except (ValueError, KeyError) as error:
            check(label, True); results[-1]['rejection'] = str(error)
        else: check(label, False)
        check(label + '/atomic', h.snapshot() == before)

    def history(first='Warrior', level=4, scores=None, earned=True):
        actor = deepcopy(actor_source)
        actor.update(firstClass=first, classLevels={first: 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
        human = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
        variant = next(x for x in human['variants'] if x['id'] == 'imperial-human')
        for ability, score in (scores or {}).items():
            bonus = variant['combinedAbilityBonuses'][ability]
            actor['abilityRolls'][ability] = list(next(d for d in product(range(1, 7), repeat=4) if sum(d) - min(d) + bonus == score))
            actor['permanentScores'][ability] = score
        if first == 'Wizard':
            actor['selectedClassSkills'] = ['Insight', 'Investigation']
            actor['scope'] = 'Explicit class-level/ability/repertoire subset, not a complete Wizard build or learned-book history.'
        h = CastingSelections(actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources)
        h.configure_choice_sources(core); h.advance(level)
        if earned: h.earn(level)
        return h

    def wizard(level=8):
        h = history('Wizard', level); h.wizard(['friends', 'arcane-ray'], ['dispel-magic'], ['dispel-magic']); return h

    def initiate(level=8):
        h = history(); h.initiate(); h.advance(level); h.earn(level); return h

    def acquire(h, sid, level, choice):
        before_scores = deepcopy(h.pay.scores); before_classes = deepcopy(h.pay.current_classes)
        before_resources = deepcopy(h.casting.use_state)
        h.acquire_casting_selection(sid, level, choice); cohort_seen.add(sid)
        check(sid + '/scores-and-classes-unchanged/' + str(choice), h.pay.scores == before_scores and h.pay.current_classes == before_classes)
        check(sid + '/no-RP-created/' + str(choice), h.casting.use_state['rp'] == before_resources['rp'])

    # These choices do not create spells. Ritual acquisition also creates no
    # book, formula or learned ritual; its learning/casting work remains separate.
    for sid, options, level in [('arcane_pulse', MENTAL, 8), ('hemocraft', ('INT', 'CHA'), 4), ('ritual_caster', ('INT', 'WIS'), 4)]:
        for ability in options:
            h = history(level=level); acquire(h, sid, level, {'ability': ability})
            check(sid + '/fixed-ability/' + ability, h.initializations[sid]['fixedAbility'] == ability and not h.casting.qualifying())
            if sid == 'hemocraft':
                check('Hemocraft/empty-start/' + ability, h.initializations[sid]['recoveryReserve']['current'] == 0 and h.initializations[sid]['bleedRecords'] == [])
            if sid == 'ritual_caster':
                check('Ritual/no-free-book-or-formula/' + ability, h.initializations[sid]['learnedRituals'] == [] and h.initializations[sid]['actualBookRef'] is None)
            next_level = 12 if level == 8 else 8; h.advance(next_level); h.earn(next_level)
            reject(sid + '/nonrepeatable/' + ability, h, lambda: h.acquire_casting_selection(sid, next_level, {'ability': options[-1]}))
            capture(sid + '/' + ability, h)
    h = history(level=4); reject('Pulse/below7', h, lambda: h.acquire_casting_selection('arcane_pulse', 4, {'ability': 'INT'}))
    for ability in ['STR', 'DEX', 'CON', None]:
        h = history(level=8); reject('Pulse/bad-ability/' + str(ability), h, lambda: h.acquire_casting_selection('arcane_pulse', 8, {'ability': ability}))
    for chosen, scores, valid in [('INT', {'INT': 12, 'WIS': 13}, False), ('WIS', {'INT': 13, 'WIS': 12}, False),
        ('INT', {'INT': 13, 'WIS': 12}, True), ('WIS', {'INT': 12, 'WIS': 13}, True)]:
        h = history(scores=scores)
        if valid: acquire(h, 'ritual_caster', 4, {'ability': chosen})
        else: reject('Ritual/selected-ability-must-qualify/' + chosen, h, lambda: h.acquire_casting_selection('ritual_caster', 4, {'ability': chosen}))
        capture('Ritual/qualifying-choice/' + str((chosen, scores)), h)
    h = history(scores={'INT': 12, 'CHA': 13}); acquire(h, 'hemocraft', 4, {'ability': 'INT'})
    check('Hemocraft/literal-either-stat-menu-distinct-from-OR-gate', h.initializations['hemocraft']['fixedAbility'] == 'INT' and h.pay.scores['INT'] == 12)
    capture('Hemocraft/CHA-gate-INT-choice', h)
    h = history(scores={'INT': 12, 'CHA': 12}); reject('Hemocraft/neither-ability-gate', h, lambda: h.acquire_casting_selection('hemocraft', 4, {'ability': 'INT'}))
    for element in ELEMENTS:
        h = history(level=8); acquire(h, 'elemental_affinity', 8, {'damageType': element})
        check('Affinity/no-spell-route/' + element, not h.casting.qualifying()); capture('Affinity/' + element, h)
    h = history(); reject('Affinity/below5', h, lambda: h.acquire_casting_selection('elemental_affinity', 4, {'damageType': 'fire'}))
    for element in ['force', 'necrotic', 'all', None]:
        h = history(level=8); reject('Affinity/unsupported/' + str(element), h, lambda: h.acquire_casting_selection('elemental_affinity', 8, {'damageType': element}))

    # Fixed ordinary payloads and source-authored supplemental grant. No fake
    # Magehand/Read Surface Thoughts alias or unrestricted class repertoire.
    for sid, spell, rank, school in [('telekinetic', 'mage-hand', 0, 'Universal'),
        ('telepathic', 'proposal_feat_detect_thoughts', 2, 'Divination')]:
        for ability in MENTAL:
            h = history(); acquire(h, sid, 4, {'ability': ability}); routes = h.casting.qualifying()
            check(sid + '/exact-personal-route/' + ability, len(routes) == 1 and (routes[0]['spellId'], routes[0]['rank'], routes[0]['school'], routes[0]['ability']) == (spell, rank, school, ability))
            if sid == 'telekinetic':
                check('Telekinetic/exact-waiver-only/' + ability, routes[0]['waivedComponents'] == ['V', 'S'] and not h.casting.use_state['renewableCharges'])
            else:
                charge = h.casting.use_state['renewableCharges'][sid + '/Warrior:4'][spell]
                check('Telepathic/one-own-charge/' + ability, (charge['maximum'], charge['current']) == (1, 1) and h.initializations[sid]['activeCommunicationChannel'] is None)
                charge['current'] = 0
                check('Telepathic/depletion-keeps-credential/' + ability, h.prerequisite('elementalAdept'))
            h.advance(8); h.earn(8)
            reject(sid + '/nonrepeatable/' + ability, h, lambda: h.acquire_casting_selection(sid, 8, {'ability': 'CHA'}))
            capture(sid + '/' + ability, h, ['Any recorded zero charge is an explicit conditional earlier lawful expenditure, not a cast simulated here.'])

    touched_cases = 0
    for sid, label, primary in [('feyTouched', 'Fey Touched', 'misty-step'), ('shadow_touched', 'Shadow Touched', 'invisibility')]:
        pool = core['currentChoicePools'][label]['choices']; check(sid + '/full32-source-menu', len(pool) == 32)
        for row in pool:
            # Every class-placement provenance is resolved against its actual
            # current payload; three paid histories cover each identity/school.
            for source_class in row['sourceRows']:
                selection = {'spellId': row['id'], 'school': row['school'], 'sourceClass': source_class}
                route = history().touched_route(sid, selection)
                check(sid + '/placement/' + str(selection), (route['rank'], route['school']) == (1, row['school']))
                placement_checks.append({'feat': sid, 'selection': selection, 'route': route})
            source_class = sorted(row['sourceRows'])[0]
            for ability in MENTAL:
                selected = {'spellId': row['id'], 'school': row['school'], 'sourceClass': source_class}
                h = history(); acquire(h, sid, 4, {'ability': ability, 'rank1': selected}); touched_cases += 1
                routes = h.casting.qualifying(); charge = h.casting.use_state['renewableCharges'][sid + '/Warrior:4']
                check(sid + '/two-exact-entitlements/' + str((selected, ability)), len(routes) == 2 and {r['spellId'] for r in routes} == {primary, row['id']} and all(r['ability'] == ability for r in routes))
                check(sid + '/separate-initial-charges/' + str((selected, ability)), set(charge) == {primary, row['id']} and all(c['current'] == c['maximum'] == 1 for c in charge.values()))
                charge[primary]['current'] = 0
                check(sid + '/independent-charge-state/' + str((selected, ability)), charge[row['id']]['current'] == 1 and h.prerequisite('elementalAdept'))
                check(sid + '/no-ordinary-class-learning/' + str((selected, ability)), not h.casting.book and not h.casting.known and not h.casting.prepared and h.pay.current_classes == {'Warrior': 4})
                h.advance(8)
                check(sid + '/growth-does-not-refill/' + str((selected, ability)), charge[primary]['current'] == 0)
                capture(sid + '/' + str((selected, ability)), h, ['Primary charge is conditionally already spent; no cast/action/strain/refund behavior is executed by this acquisition pass.'])
        valid = {'spellId': pool[0]['id'], 'school': pool[0]['school'], 'sourceClass': sorted(pool[0]['sourceRows'])[0]}
        for changed in [{'school': 'Universal'}, {'sourceClass': 'Warrior'}, {'spellId': 'missing-spell'}, {'rank': 1}]:
            h = history(); bad = {**valid, **changed}
            reject(sid + '/invalid-placement/' + str(changed), h, lambda: h.acquire_casting_selection(sid, 4, {'ability': 'INT', 'rank1': bad}))
        h = history(); acquire(h, sid, 4, {'ability': 'INT', 'rank1': valid}); h.advance(8); h.earn(8)
        reject(sid + '/nonrepeatable', h, lambda: h.acquire_casting_selection(sid, 8, {'ability': 'CHA', 'rank1': valid}))

    pact_choices = [{'sigil': 'hex'}, {'sigil': 'shadowstep'}] + [{'sigil': 'energyResistance', 'damageType': t} for t in ELEMENTS]
    for choice in pact_choices:
        h = history(); acquire(h, 'forbidden_pact', 4, choice); routes = h.casting.qualifying()
        check('Pact/one-CHA-rank0-absent-school/' + str(choice), len(routes) == 1 and routes[0]['spellId'] == 'feat-supplement.eldritch-blast' and routes[0]['rank'] == 0 and routes[0]['ability'] == 'CHA' and 'school' not in routes[0])
        state = h.initializations['forbidden_pact']
        check('Pact/fixed-sigil-not-other-feat/' + str(choice), state['sigil'] == choice['sigil'] and len(h.pay.grants) == 1 and not h.pay.has('dark_affinity') and not h.pay.has('curse_channeling'))
        check('Pact/no-ranked-repertoire/' + str(choice), not any(r['rank'] > 0 for r in routes) and state['spentSubstitutionEncounterIds'] == [])
        h.advance(8); h.earn(8)
        reject('Pact/nonrepeatable/' + str(choice), h, lambda: h.acquire_casting_selection('forbidden_pact', 8, {'sigil': 'hex'}))
        capture('Pact/' + str(choice), h)
    for choice in [{'sigil': 'energyResistance'}, {'sigil': 'energyResistance', 'damageType': 'force'}, {'sigil': 'hex', 'damageType': 'fire'}, {'sigil': 'invented'}]:
        h = history(); reject('Pact/invalid/' + str(choice), h, lambda: h.acquire_casting_selection('forbidden_pact', 4, choice))

    for create, label in [(lambda: initiate(), 'paid-Initiate'), (lambda: wizard(), 'Wizard'),
        (lambda: history(), 'Pact')]:
        h = create()
        if label == 'Pact':
            h.acquire_casting_selection('forbidden_pact', 4, {'sigil': 'hex'}); h.advance(8); h.earn(8)
        candidates = sorted({r['spellId'] for r in h.casting.qualifying() if r['rank'] == 0})
        for cantrip in candidates:
            case = create()
            if label == 'Pact':
                case.acquire_casting_selection('forbidden_pact', 4, {'sigil': 'hex'}); case.advance(8); case.earn(8)
            prior = deepcopy(case.casting.snapshot()); acquire(case, 'cantrip_mastery', 8, {'spellId': cantrip})
            check('Cantrip/fixed-owned-mode/' + label + '/' + cantrip, case.initializations['cantrip_mastery']['fixedSpellId'] == cantrip and case.casting.snapshot() == prior)
            capture('Cantrip/' + label + '/' + cantrip, case)
    for sid in ['magehand', 'unknown-cantrip', 'dispel-magic', 'find-familiar']:
        h = wizard(); reject('Cantrip/not-actual-known-rank0/' + sid, h, lambda: h.acquire_casting_selection('cantrip_mastery', 8, {'spellId': sid}))
    h = history(level=8); reject('Cantrip/no-grant', h, lambda: h.acquire_casting_selection('cantrip_mastery', 8, {'spellId': 'arcane-ray'}))

    for create, label in [(lambda: initiate(), 'Initiate-INT'), (lambda: wizard(), 'Wizard-INT')]:
        h = create(); provider = h.providers()[0]; acquire(h, 'soul_cage', 8, {'provider': provider})
        check('SoulCage/actual-fixed-provider/' + label, h.initializations['soul_cage']['fixedProvider'] == provider)
        check('SoulCage/no-crystal-or-charges-created/' + label, h.initializations['soul_cage']['actualBlackCrystalRef'] is None and h.initializations['sharedSoulCharges']['current'] == 0)
        capture('SoulCage/' + label, h)
    h = history(); h.acquire_casting_selection('forbidden_pact', 4, {'sigil': 'shadowstep'}); h.advance(8); h.earn(8)
    acquire(h, 'soul_cage', 8, {'provider': h.providers()[0]})
    check('SoulCage/actual-Pact-CHA-provider', h.initializations['soul_cage']['fixedProvider']['ability'] == 'CHA'); capture('SoulCage/Pact-CHA', h)
    # A real separately paid Lifeleech parent does not invent a missing DC source.
    h = initiate(); h.acquire_parent('lifeleech', 8); h.advance(12); h.earn(12)
    h.initializations['sharedSoulCharges'] = {'maximum': 3, 'current': 2, 'evaluatedDeathEvents': ['conditional-previous-death'], 'bodyEpochEntitlements': ['conditional-body-epoch']}
    saved = deepcopy(h.initializations['sharedSoulCharges']); provider = h.providers()[0]
    acquire(h, 'soul_cage', 12, {'provider': provider})
    check('SoulCage/preserves-existing-shared-charge-history', h.initializations['sharedSoulCharges'] == saved)
    capture('SoulCage/Lifeleech-shared-pool', h, ['Two legitimate previously collected charges and their event/body records are conditional prior resource facts; no death/capture executed here.'])
    h = initiate(); h.acquire_parent('lifeleech', 8); h.advance(12); h.earn(12); old_provider = h.providers()[0]
    h.remove_personal_routes()
    check('SoulCage/printed-owned-parent-OR-retained', h.prerequisite('soul_cage') and not h.providers())
    reject('SoulCage/mandatory-provider-not-invented', h, lambda: h.acquire_casting_selection('soul_cage', 12, {'provider': old_provider}))
    capture('SoulCage/removed-route-missing-mandatory-choice', h,
        ['Prior spell-grant removal is a conditional separately lawful event, not a removal rule provided by a feat. ACQ03 explicitly controls required acquisition selections as well as printed predicates.'])
    h = wizard(); bad = {**h.providers()[0], 'ability': 'CHA'}
    reject('SoulCage/cannot-substitute-higher-ability', h, lambda: h.acquire_casting_selection('soul_cage', 8, {'provider': bad}))
    check('eleven-identities-covered', cohort_seen == COHORT)
    # Bind every actual complete spell file consulted by the resolver, including
    # payload descendants outside the immutable feat-dependency envelope.
    for rel, (size, digest, _) in sources.cache.items():
        bound = info(G / rel); check('current-spell-source/' + rel, bound['bytes'] == size and bound['sha256'] == digest)
        if bound not in bindings: bindings.append(bound)
    for bound in bindings: check('unchanged/' + bound['path'], info(G / bound['path']) == bound)
    limits = [
        'This pass establishes named permanent selections and initial grants only, not complete eleven-feat use, damage/healing/resource timing, all335 acquisitions or CRPG implementation.',
        'The Human/Imperial/Warrior and paid-Initiate slices retain actual class opportunities and source training. Wizard spellbook/repertoire witnesses are declared legal source-bound subsets, not full class builds or learning histories.',
        'All64 preserved Touched identity/school menu entries are exercised with all3 abilities. Every listed source-class placement is independently resolved. Source class labels bind rank/school/payload and do not grant that class or impose its learning gates on this expressly classless feat route.',
        'New supplemental Detect Thoughts, Misty Step feat access and Eldritch Blast are bound to actual source-authoring directions, not inserted into ordinary class catalogs or promoted to runtime selection.',
        'Known Cantrip Mastery modes and Soul Cage providers use actual retained source witnesses. This does not claim every class/ancestry casting engine or every possible cantrip; future use/repertoire changes retain the full governing procedure.',
        'Conditional prior expenditures, shared Soul Charges and lawful grant removal are labeled premises, not authenticated campaign events or newly authored retraining/death procedures.',
        'Ritual Caster receives no free book or ritual. Its real learning/casting labor, materials, concentration and cost rules remain separate. No pact, soul, Feywild, Shadowfell or other cosmology content is reviewed or authored.']
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-eleven-casting-selection-slices',
        'sourceBindings': bindings, 'checks': len(results), 'failures': [], 'results': results,
        'cohort': sorted(COHORT), 'traces': traces, 'touchedPlacementEvidence': placement_checks,
        'completeProcedures': {sid: contracts[sid]['completeOperativeProcedure'] for sid in COHORT}, 'limits': limits,
        'counts': {'identities': 11, 'touchedMenuEntries': 64, 'touchedAbilityHistories': touched_cases,
            'touchedSourcePlacements': len(placement_checks), 'pactChoiceBranches': len(pact_choices),
            'recordedTraces': len(traces), 'newPartialPrerequisiteIdentities': 0},
        'sourceInformationDeleted': False, 'newRulesAdopted': False, 'fullCandidateApproved': False,
        'campaignRecordsAuthenticated': 0, 'cosmologyReviewed': False}
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=serial); f.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as f:
        f.write('# Permanent feat casting selections\n\n')
        f.write(f'{len(results)} checks pass across{len(traces)} recorded histories for11 identities. Fey/Shadow Touched cover64 identity/school entries,192 ability histories and{len(placement_checks)} source-class placement checks. Forbidden Pact covers all7 nested branches.\n\n')
        for limit in limits: f.write('- ' + limit + '\n')
    print(json.dumps({'report': info(target), 'notes': info(notes), 'checks': len(results), 'traces': len(traces),
        'counts': report['counts'], 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
