"""Finite paid skill/tool/language choice and Cultural Expert snapshot checks."""
from copy import deepcopy
from datetime import datetime, timezone
from itertools import combinations, product
import json
from pathlib import Path
from feat_exact_01_training_language_choices import TrainingLanguageChoices
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    target = A / 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_CHECK.json'
    notes = A / 'FEAT_EXACT_01_TRAINING_LANGUAGE_CHOICES_NOTES.md'
    assert not target.exists() and not notes.exists()
    paths = [Path(__file__), R / 'tools/feat_exact_01_training_language_choices.py',
        R / 'tools/feat_exact_01_prodigy_choices.py', R / 'tools/feat_exact_01_acquisition_models.py',
        R / 'tools/feat_exact_01_training_prerequisite_model.py', R / 'tools/validate_feat_exact_01_composite_casting.py',
        R / 'data/playtest/character_foundation.json', R / 'data/playtest/ancestry_background_candidate.json',
        R / 'data/playtest/equipment_source_catalog.json', R / 'data/playtest/language_communication_candidate_public.json',
        R / 'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md', R / 'docs/mechanics/CRAFTING_TRADE_REFERENCE.md',
        A / 'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json', A / 'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
        R / 'data/public/feat_candidates/exact_01/candidate.json', R / 'data/public/feat_candidates/exact_01/shared_rules.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[6]); classes = {x['class']: x for x in foundation['classes']}
    skills = {s: a for a, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[7]); backgrounds = {x['id']: x for x in ancestry['backgrounds']}
    equipment = {x['id']: x for x in read(paths[8])['records']}; language = read(paths[9])
    trade = paths[11].read_text(encoding='utf-8'); contracts = {x['id']: x for x in read(paths[12])['records']}
    actor = deepcopy(read(paths[13])['actorSourceProjection'])
    actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
    modes = language['rules']['permanentModeConvention']['ordinaryModes']
    available = [{'language': sid, 'evidenceMode': 'conditional_fixture', 'modes': modes,
        'admission': 'ordinary-contact', 'contactPremise': 'Explicit conditional admitted ordinary contact before acquisition; not an actual campaign record.'}
        for sid in ['common', 'dwarvish', 'elvish', 'orcish', 'gnomish', 'goblin', 'giant', 'trollish']]
    available += [{'language': sid, 'evidenceMode': 'conditional_fixture', 'modes': actual_modes,
        'admission': 'source-qualified-contact', 'contactPremise': 'Explicit conditional separately admitted existing source-qualified contact; no new canon or secret access is authored.'}
        for sid, actual_modes in [('draconic', modes), ('runic', ['reading', 'writing'])]]
    results = []; traces = []

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def capture(label, h, conditional=None):
        traces.append({'id': label, 'after': h.snapshot(),
            'conditionalPremisesBeyondBaseSlice': conditional or [],
            'scope': 'Actual source-derived Human/Imperial/Warrior training/payment slice with explicitly conditional language contact; not authenticated campaign or full build.'})

    def reject(label, h, call):
        before = h.snapshot()
        try:
            call()
        except (ValueError, KeyError) as error:
            check(label, True); results[-1]['rejection'] = str(error)
        else:
            check(label, False)
        check(label + '/atomic', h.snapshot() == before)

    def history(int_score=None, dice_tool=False):
        a = deepcopy(actor)
        if dice_tool:
            a['backgroundToolChoice'] = 'tools.dragonchess-set'
        if int_score is not None:
            human = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
            variant = next(x for x in human['variants'] if x['id'] == 'imperial-human')
            bonus = variant['combinedAbilityBonuses']['INT']
            a['abilityRolls']['INT'] = list(next(d for d in product(range(1, 7), repeat=4) if sum(d) - min(d) + bonus == int_score))
            a['permanentScores']['INT'] = int_score
        h = TrainingLanguageChoices(a, classes, equipment, skills, ancestry, backgrounds, contracts,
            language, available, ['dwarvish', 'elvish', 'orcish'], trade)
        h.advance(4); h.earn(4); return h

    def skill(sid): return {'kind': 'skill', 'id': sid}
    def tool(sid): return {'kind': 'tool', 'id': sid}

    baseline = history(); missing_skills = sorted(s for s in skills if baseline.skill_factor(s) == 0)
    all_tools = sorted(baseline.tool_catalog); missing_tools = sorted(set(all_tools) - baseline.tools)
    # All eight ordered skill/tool type patterns; every currently eligible skill
    # and all42 profiled tools also receive an individual legal acquisition.
    for pattern in product(['skill', 'tool'], repeat=3):
        h = history(); si = ti = 0; selected = []
        for kind in pattern:
            if kind == 'skill': selected.append(skill(missing_skills[si])); si += 1
            else: selected.append(tool(missing_tools[ti])); ti += 1
        event = h.acquire_skilled(4, selected)
        check('Skilled/pattern/' + str(pattern), len(event['orderedChoices']) == 3 and all(x['state'] == 'resolved' for x in event['orderedChoices']))
        check('Skilled/no-free-extras/' + str(pattern), h.pay.scores == baseline.pay.scores and h.actor['physicalInventory'] == [] and all(h.skill_factor(s) <= 1 for s in skills))
        capture('Skilled/pattern/' + str(pattern), h)
    for sid in missing_skills:
        h = history(); h.acquire_skilled(4, [skill(sid), tool('tools.tinker-s-tools'), tool('tools.flute')])
        check('Skilled/actual-skill/' + sid, h.skill_factor(sid) == 1 and h.trades == {'Tinkering': {'level': 1, 'xp': 0}})
        capture('Skilled/skill/' + sid, h)
    primary_seen = set()
    for sid in all_tools:
        h = history(dice_tool=sid == 'tools.dice-set'); before = h.snapshot()
        h.acquire_skilled(4, [tool(sid), skill('Investigation'), skill('Stealth')])
        check('Skilled/actual-tool/' + sid, h.tools - set(before['tools']) == {sid})
        expected = {h.primary[sid]: {'level': 1, 'xp': 0}} if sid in h.primary else {}
        if sid in h.primary: primary_seen.add(h.primary[sid])
        check('Skilled/mapped-trade-only/' + sid, h.trades == expected and h.actor['physicalInventory'] == [])
        capture('Skilled/tool/' + sid, h)
    check('all42tools-and16primary-mappings', len(all_tools) == 42 and len(primary_seen) == 16)
    for bad in [None, [], [skill('Investigation')], [skill('Investigation')] * 3,
        [skill('Athletics'), tool('tools.flute'), skill('Stealth')], [skill('Spellcraft'), skill('Stealth'), tool('tools.flute')],
        [tool('simple-melee-weapons.dagger'), skill('Stealth'), skill('Investigation')],
        [tool('tools.dice-set'), skill('Stealth'), skill('Investigation')],
        [None, skill('Stealth'), skill('Investigation')], [skill('Stealth'), skill('Investigation'), {'kind': 'expertise', 'id': 'Athletics'}]]:
        h = history(); reject('Skilled/invalid/' + str(bad), h, lambda: h.acquire_skilled(4, bad))
    h = history(); h.trades['Tinkering'] = {'level': 7, 'xp': 3}
    h.acquire_skilled(4, [tool('tools.tinker-s-tools'), skill('Investigation'), skill('Stealth')])
    check('Skilled/preserve-higher-existing-lawful-trade', h.trades['Tinkering'] == {'level': 7, 'xp': 3})
    capture('Skilled/preserve-trade', h, ['Existing legitimate Tinkering7/3XP is conditional prior training; the feat supplies no complete history for it.'])
    h = history(); h.acquire_skilled(4, [skill('Investigation'), skill('Stealth'), tool('tools.flute')]); h.advance(8); h.earn(8)
    reject('Skilled/nonrepeatable', h, lambda: h.acquire_skilled(8, [skill('Medicine'), skill('Survival'), tool('tools.tinker-s-tools')]))
    h.skill_sources['Investigation']['conditional-later-independent-training'] = 1
    check('Skilled/later-duplicate-retains-choice', h.pay.grants[0]['choice'][0] == skill('Investigation') and h.skill_factor('Investigation') == 1)
    capture('Skilled/later-duplicate', h, ['Later independently lawful duplicate skill grant is conditional; no respec rule is created.'])
    for left in [0, 1, 2]:
        h = history(); h.skill_sources = {s: {'conditional-existing-training': 1} for s in skills}; h.tools = set(all_tools)
        remaining = missing_skills[:left]
        for s in remaining: del h.skill_sources[s]
        event = h.acquire_skilled(4, [skill(s) for s in remaining] + [None] * (3 - left))
        check('Skilled/exhaustion/' + str(left), sum(x['state'] == 'exhausted' for x in event['orderedChoices']) == 3 - left and not event['futureChoiceCredit'])
        capture('Skilled/exhaustion/' + str(left), h, ['Conditional saturation of eligible proficiencies; not a complete earned Warrior history.'])

    pairs = list(combinations(missing_skills, 2))
    for pair in pairs:
        h = history(); initial = deepcopy(h.skill_sources); h.acquire_jack(4, list(pair))
        check('Jack/untrained-not-proficiency/' + str(pair), h.skill_sources == initial and all(h.skill_factor(s) == 0 and h.task_pb_contribution(s) == 1 for s in pair))
        check('Jack/no-trade-or-item/' + str(pair), h.trades == {} and h.actor['physicalInventory'] == [])
        capture('Jack/pair/' + str(pair), h)
    h = history(); h.acquire_jack(4, ['Investigation', 'Stealth'])
    for level, expected in [(4, 1), (5, 1), (9, 2), (13, 2), (17, 3), (20, 3)]:
        h.advance(level); check('Jack/floor-current-PB/' + str(level), h.task_pb_contribution('Investigation') == expected)
    check('Jack/strongest-contribution-no-addition', h.task_pb_contribution('Investigation', other_untrained=4) == 4)
    h = history(); h.acquire_jack(4, ['Investigation', 'Stealth']); h.advance(8); h.earn(8)
    h.acquire_skilled(8, [skill('Investigation'), skill('Medicine'), tool('tools.flute')])
    check('Jack/separate-paid-full-training-overrides-half', h.skill_factor('Investigation') == 1 and h.task_pb_contribution('Investigation') == 3 and h.half_skill_choices == ['Investigation', 'Stealth'])
    del h.skill_sources['Investigation']['skilled']
    # A lawful source-removal premise changes credential state only; it is not a
    # feat-provided retraining/removal procedure or refunded feat opportunity.
    if not h.skill_sources['Investigation']: del h.skill_sources['Investigation']
    check('Jack/same-half-choice-resumes-on-actual-loss', h.task_pb_contribution('Investigation') == 1 and len(h.pay.grants) == 2)
    capture('Jack/paid-training-and-conditional-loss', h, ['Separately lawful loss of the later proficiency is conditional; no removal rule or payment refund authored.'])
    for bad in [None, [], ['Investigation'], ['Investigation', 'Investigation'], ['Athletics', 'Investigation'], ['tools.flute', 'Investigation'], ['Spellcraft', 'Investigation'], [None, 'Investigation']]:
        h = history(); reject('Jack/invalid/' + str(bad), h, lambda: h.acquire_jack(4, bad))
    h = history(); h.acquire_jack(4, ['Investigation', 'Stealth']); h.advance(8); h.earn(8)
    reject('Jack/nonrepeatable-no-retarget', h, lambda: h.acquire_jack(8, ['Medicine', 'Survival']))
    for left in [0, 1]:
        h = history(); h.skill_sources = {s: {'conditional-training': 1} for s in skills}
        if left: del h.skill_sources['Investigation']
        e = h.acquire_jack(4, (['Investigation'] if left else []) + [None] * (2 - left))
        check('Jack/exhaustion/' + str(left), len(h.half_skill_choices) == left and not e['futureChoiceCredit'])
        capture('Jack/exhaustion/' + str(left), h, ['Conditional complete/near-complete training snapshot.'])

    available_new = sorted(baseline.languages.eligible()); language_cases = 0
    for feat in ['linguist', 'polyglot']:
        for selected in combinations(available_new, 3):
            h = history(); before = h.snapshot(); event = h.acquire_languages(feat, 4, list(selected)); language_cases += 1
            check(feat + '/three-distinct/' + str(selected), set(h.languages.known) - set(before['languages']['known']) == set(selected))
            check(feat + '/actual-modes-only/' + str(selected), all(h.languages.known[s] == h.languages.attested_modes(s) for s in selected))
            check(feat + '/no-ability-fee-credit/' + str(selected), h.pay.scores == before['payment']['scores'] and event['newCourseCredit'] == 0 and not event['futureChoiceCredit'])
            check(feat + '/exact-family-anchors/' + str(selected), h.language_anchors[feat] == list(selected))
            capture(feat + '/languages/' + str(selected), h)
        for bad in [None, [], ['gnomish'], ['gnomish', 'gnomish', 'goblin'], ['elvish', 'goblin', 'giant'],
            ['the-voice', 'goblin', 'giant'], ['Mycelian', 'goblin', 'giant'], [None, 'goblin', 'giant']]:
            h = history(); reject(feat + '/invalid/' + str(bad), h, lambda: h.acquire_languages(feat, 4, bad))
        h = history(); h.languages.add('gnomish', {'speaking', 'spokenComprehension'}, 'conditional narrower prior competency')
        event = h.acquire_languages(feat, 4, ['gnomish', 'goblin', 'runic'])
        check(feat + '/complete-only-missing-modes', event['orderedChoices'][0]['newModes'] == ['reading', 'writing'])
        check(feat + '/written-only-Runic', h.languages.known['runic'] == {'reading', 'writing'})
        capture(feat + '/partial-modes', h, ['Existing narrower Gnomish grant is an explicit conditional premise.'])
        h.advance(8); h.earn(8)
        reject(feat + '/nonrepeatable', h, lambda: h.acquire_languages(feat, 8, ['giant', 'trollish', 'draconic']))
        for left in [0, 1, 2]:
            h = history(); retain = available_new[:left]
            for row in available:
                if row['language'] not in retain: h.languages.add(row['language'], row['modes'], 'conditional-prior-complete-knowledge')
            e = h.acquire_languages(feat, 4, retain + [None] * (3 - left))
            check(feat + '/exhaustion/' + str(left), len(h.language_anchors[feat]) == left and not e['futureChoiceCredit'])
            capture(feat + '/exhaustion/' + str(left), h, ['Conditional known-language saturation within the genuine available list.'])
    h = history(); h.acquire_languages('polyglot', 4, ['gnomish', 'goblin', 'runic']); h.advance(8); h.earn(8)
    h.acquire_languages('linguist', 8, ['giant', 'trollish', 'draconic'])
    check('Polyglot/other-feat-does-not-expand-anchors', h.language_anchors['polyglot'] == ['gnomish', 'goblin', 'runic'] and h.language_anchors['linguist'] == ['giant', 'trollish', 'draconic'])
    capture('Polyglot4-Linguist8', h)

    # Existing canon is an opaque conditional premise; no culture history,
    # deity, plane or new ordinary skill is authored by these boundary records.
    def culture(h, separate=False):
        record = {'id': 'conditional-existing-culture-01', 'evidenceMode': 'conditional_fixture',
            'existingCulturePremise': 'This fixture assumes an already named culture and legitimately available knowledge; it authors no setting facts.',
            'sourceRef': 'conditional-record:existing-culture-01',
            'separateLoreCredential': {'id': 'conditional-existing-lore-01', 'recordRef': 'conditional-record:existing-lore-01'} if separate else None}
        h.admit_conditional_culture_record(record); return record['id']

    for selected in ['History', 'Religion']:
        h = history(); original_factor = h.skill_factor(selected)
        h.acquire_cultural(4, skill(selected))
        check('Cultural/' + selected + '/fixed-branch', h.cultural['branch'] == ('expertise-in-cultural-context' if original_factor else 'proficiency'))
        check('Cultural/' + selected + '/context-scope', h.cultural_factor(selected, cultural_context=True) == (2 if original_factor else 1) and h.cultural_factor(selected, cultural_context=False) == 1)
        if not original_factor:
            h.skill_sources[selected]['conditional-later-proficiency'] = 1
            check('Cultural/later-proficiency-not-retroactive-Expertise', h.cultural_factor(selected, cultural_context=True) == 1)
        h.skill_sources[selected]['conditional-other-Expertise'] = 2
        check('Cultural/' + selected + '/no4PB', h.cultural_factor(selected, cultural_context=True) == 2)
        capture('Cultural/' + selected, h, ['Later independent proficiency/Expertise receipts are conditional boundary premises, not new training procedures.'])
    for separate in [False, True]:
        for prior_factor in [0, 1, 2]:
            h = history(); cid = culture(h, separate); selected = 'conditional-existing-lore-01' if separate else 'History'
            if separate:
                if prior_factor: h.lore_sources[selected] = {'conditional-prior-credential': prior_factor}
            else:
                h.skill_sources.pop('History')
                if prior_factor: h.subject_sources[cid] = {'conditional-prior-bounded-History': prior_factor}
            before_catalog = deepcopy(h.skill_catalog); h.acquire_cultural(4, {'kind': 'culture', 'id': cid})
            expected = 2 if prior_factor else 1
            check('Cultural/conditional-branch/' + str((separate, prior_factor)), h.cultural_factor(selected, cid, True) == expected)
            check('Cultural/no21st-ordinary-skill/' + str((separate, prior_factor)), h.skill_catalog == before_catalog and len(h.skill_catalog) == 20)
            if not separate:
                check('Cultural/bounded-not-general-History/' + str(prior_factor), h.skill_factor('History') == 0 and h.cultural_factor('History', 'different-culture', True) == 0)
            capture('Cultural/conditional/' + str((separate, prior_factor)), h,
                ['Opaque existing culture/credential and prior proficiency state are conditional evidence only; no complete earned character or setting/cosmology content is asserted.'])
    h = history(); cid = culture(h); h.acquire_cultural(4, {'kind': 'culture', 'id': cid})
    check('Cultural/general-History-qualifies-for-bounded-Expertise', h.cultural_factor('History', cid, True) == 2 and h.cultural_factor('History', 'different-culture', True) == 1)
    h.advance(8); h.earn(8); reject('Cultural/nonrepeatable', h, lambda: h.acquire_cultural(8, skill('Religion')))
    for bad in [None, skill('Arcana'), {'kind': 'culture', 'id': 'new-unrecorded-culture'}, {'kind': 'lore', 'id': 'unrecorded-Lore'}]:
        h = history(); reject('Cultural/invalid/' + str(bad), h, lambda: h.acquire_cultural(4, bad))
    h = history(); reject('Cultural/no-unsupported-admission', h, lambda: h.admit_conditional_culture_record({'id': 'invented'}))

    # Permanent INT requirements are checked with actual ancestry-adjusted rolls.
    for feat, minimum in [('jack_of_all_trades', 12), ('cultural_expert', 12), ('linguist', 14), ('polyglot', 14)]:
        for score in [minimum - 1, minimum]:
            h = history(int_score=score)
            call = (lambda: h.acquire_jack(4, ['Investigation', 'Stealth'])) if feat == 'jack_of_all_trades' else (
                (lambda: h.acquire_cultural(4, skill('Religion'))) if feat == 'cultural_expert' else
                (lambda: h.acquire_languages(feat, 4, ['gnomish', 'goblin', 'giant'])))
            if score < minimum:
                h.actor['temporaryIntelligenceBonus'] = 10
                reject(feat + '/below-permanent-gate', h, call)
            else:
                call(); check(feat + '/exact-permanent-gate', h.pay.has(feat))
            capture(feat + '/INT' + str(score), h)
    for bound in bindings:
        check('unchanged/' + bound['path'], info(G / bound['path']) == bound)
    limits = [
        'Actual Human/Imperial/Warrior fixed training and feat opportunities are projected. All language-contact lists and prior saturation/removal/extra credential states are explicitly conditional, not campaign authentication or complete builds.',
        'Skilled exercises all8 ordered skill/tool category patterns, every untrained skill in the base source slice and all42 profiled tools/16 primary trades. It does not claim every combination or a complete training history for every ordinary skill.',
        'Jack of All Trades checks half-PB selection and later independent proficiency arbitration; it creates no trained credential or trade.',
        'Language choices use reviewed ordinary/contact and explicitly admitted Draconic/Runic modes. Missing secret/special-language entitlements remain unestablished; rejection in this slice is not a universal prohibition. Polyglot recognition/translation play is not executed here.',
        'Cultural Expert uses actual History/Religion training examples plus opaque conditional existing culture/Lore records. These records establish no real canon, society, deity, cosmology or actual campaign knowledge. Broader knowledge-access adjudication remains in the source.',
        'This pass covers permanent selections and bounded resulting training contributions, not all feat use, all335 acquisitions, full original660 cases, exact candidate approval, software implementation or human balance.']
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'passed-five-training-language-acquisition-slices',
        'checks': len(results), 'failures': [], 'results': results, 'sourceBindings': bindings,
        'cohort': ['skilled', 'jack_of_all_trades', 'cultural_expert', 'linguist', 'polyglot'],
        'completeProcedures': {sid: contracts[sid]['completeOperativeProcedure'] for sid in ['skilled', 'jack_of_all_trades', 'cultural_expert', 'linguist', 'polyglot']},
        'traces': traces, 'limits': limits, 'counts': {'identities': 5, 'toolProfiles': len(all_tools),
            'primaryTrades': len(primary_seen), 'baseSliceUntrainedSkills': len(missing_skills), 'jackPairs': len(pairs),
            'languageTriples': language_cases, 'recordedTraces': len(traces), 'newPartialPrerequisiteIdentities': 0},
        'sourceInformationDeleted': False, 'newRulesAdopted': False, 'campaignRecordsAuthenticated': 0,
        'fullCandidateApproved': False, 'cosmologyReviewed': False}
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=serial); f.write('\n')
    with notes.open('x', encoding='utf-8', newline='\n') as f:
        f.write('# Skill, tool and language selections\n\n')
        f.write(f'{len(results)} checks pass across{len(traces)} captured histories for Skilled, Jack of All Trades, Cultural Expert, Linguist and Polyglot. The evidence distinguishes actual proficiency, half-PB, contextual Expertise, subject-only History and attested language modes.\n\n')
        for limit in limits: f.write('- ' + limit + '\n')
    print(json.dumps({'report': info(target), 'notes': info(notes), 'checks': len(results), 'traces': len(traces),
        'counts': report['counts'], 'failures': 0}, indent=2))


if __name__ == '__main__':
    main()
