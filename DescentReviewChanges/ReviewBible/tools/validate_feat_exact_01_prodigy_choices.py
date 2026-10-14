"""Record finite paid Prodigy selections and explicitly conditional edge cases."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from feat_exact_01_prodigy_choices import ProdigyAcquisition, LanguageChoices
from validate_feat_exact_01_composite_casting import read, info, serial

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    output = A / 'FEAT_EXACT_01_PRODIGY_CHOICES_CHECK.json'
    notes = A / 'FEAT_EXACT_01_PRODIGY_CHOICES_NOTES.md'
    assert not output.exists() and not notes.exists()
    paths = [Path(__file__), R/'tools/feat_exact_01_prodigy_choices.py',
             R/'tools/feat_exact_01_acquisition_models.py', R/'tools/feat_exact_01_training_prerequisite_model.py',
             R/'tools/validate_feat_exact_01_composite_casting.py', R/'data/playtest/character_foundation.json',
             R/'data/playtest/ancestry_background_candidate.json', R/'data/playtest/equipment_source_catalog.json',
             R/'data/playtest/language_communication_candidate_public.json',
             R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md', R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
             R/'docs/mechanics/CRAFTING_TRADE_REFERENCE.md', A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
             A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json', R/'data/public/feat_candidates/exact_01/candidate.json',
             R/'data/public/feat_candidates/exact_01/shared_rules.json']
    bindings = [info(p) for p in paths]
    foundation = read(paths[5]); classes = {c['class']: c for c in foundation['classes']}
    skills = {s: ability for ability, group in foundation['skillAbilities'].items() for s in group}
    ancestry = read(paths[6]); backgrounds = {b['id']: b for b in ancestry['backgrounds']}
    equipment = {r['id']: r for r in read(paths[7])['records']}; language = read(paths[8])
    trade = paths[11].read_text(encoding='utf-8'); contracts = {r['id']: r for r in read(paths[12])['records']}
    actor = deepcopy(read(paths[13])['actorSourceProjection'])
    actor.update(firstClass='Warrior', classLevels={'Warrior': 1}, selectedClassSkills=['Animal Handling', 'Athletics'])
    results = []; traces = []
    modes = language['rules']['permanentModeConvention']['ordinaryModes']
    available = [{'language': sid, 'evidenceMode': 'conditional_fixture', 'modes': modes,
                  'admission': 'ordinary-contact',
                  'contactPremise': 'Conditional world provides this admitted ordinary population-language contact before choice; no real campaign asserted.'}
                 for sid in ['common', 'dwarvish', 'elvish', 'orcish', 'gnomish', 'goblin', 'giant', 'trollish']]

    def check(label, truth):
        results.append({'id': label, 'passed': bool(truth)})
        if not truth:
            raise AssertionError(label)

    def history(custom=None, options=None, starting=None):
        h = ProdigyAcquisition(custom or actor, classes, equipment, skills, ancestry, backgrounds, contracts,
                               language, available if options is None else options,
                               ['dwarvish', 'elvish', 'orcish'] if starting is None else starting, trade)
        h.advance(4); h.earn(4)
        return h

    def choices(**changes):
        return {'skill': 'Investigation', 'tool': 'tools.tinker-s-tools', 'language': 'gnomish',
                'expertise': 'Investigation', **changes}

    def remember(label, before, h, scope='Source-qualified Human/Imperial/Warrior training and paid-opportunity slice with explicitly conditional language contact premises'):
        traces.append({'id': label, 'scope': scope, 'before': before, 'after': h.snapshot()})

    def reject(label, h, choice, sid='prodigy', level=4):
        before = h.snapshot(); original_choice = deepcopy(choice)
        try:
            h.acquire(sid, level, choice)
        except (ValueError, KeyError) as error:
            results.append({'id': label, 'passed': True, 'reason': str(error)})
        else:
            check(label, False)
        check(label + '/atomic-rejection', h.snapshot() == before and choice == original_choice)
        traces.append({'id': label, 'scope': 'Rejected acquisition command', 'before': before, 'choice': choice,
                       'unchangedAfter': h.snapshot()})

    h = history(); before = h.snapshot(); event = h.acquire('prodigy', 4, choices())
    check('ordered-four-part-acquisition', [x['part'] for x in event['orderedChoices']] == ['skill', 'tool', 'language', 'expertise'])
    check('new-skill-can-receive-expertise', h.skill_factor('Investigation') == 2 and h.skill_modifier('Investigation') == 7)
    check('actual-single-Warrior4-payment', len(h.pay.grants) == 1 and h.pay.opportunities['Warrior:4']['spent'])
    check('source-primary-trade-one-zero', h.trades == {'Tinkering': {'level': 1, 'xp': 0}})
    check('real-starting-plus-feat-language-count', set(h.languages.known) == {'common', 'dwarvish', 'elvish', 'orcish', 'gnomish'})
    check('permanent-full-modes-and-shared-script', h.languages.known['gnomish'] == set(modes) and 'dwarvish-script' in h.languages.scripts)
    check('no-ability-increase-or-physical-inventory', h.pay.scores == before['payment']['scores'] and h.actor['physicalInventory'] == [])
    check('no-study-fee-or-banked-choice', event['newCourseCredit'] == 0 and event['newPhysicalItems'] == [] and not event['futureChoiceCredit'])
    remember('complete-first-Prodi-selection', before, h)

    # Every actual tool profile, including all sixteen primary trade bindings.
    primary_seen = set(); tool_ids = sorted(h.tool_catalog)
    for tool in tool_ids:
        a = deepcopy(actor)
        if tool == 'tools.dice-set':
            a['backgroundToolChoice'] = 'tools.dragonchess-set'
        case = history(a); old = case.snapshot(); case.acquire('prodigy', 4, choices(tool=tool))
        delta = case.tools - set(old['tools'])
        check(tool + '/one-new-proficiency', delta == {tool})
        primary = case.primary.get(tool)
        if primary:
            primary_seen.add(primary)
            check(tool + '/actual-primary-trade-only', case.trades == {primary: {'level': 1, 'xp': 0}})
        else:
            check(tool + '/no-invented-trade', not case.trades)
        check(tool + '/proficiency-not-kit-ownership', case.actor['physicalInventory'] == [] and case.pay.scores == old['payment']['scores'])
        remember('tool-choice/' + tool, old, case)
    check('all16-source-primary-trades-exercised', len(primary_seen) == 16)
    check('all42-actual-profiled-tool-options-exercised', len(tool_ids) == 42)

    baseline = history()
    for skill in sorted(set(skills) - set(baseline.skill_sources)):
        case = history(); old = case.snapshot(); case.acquire('prodigy', 4, choices(skill=skill, expertise=skill))
        check('new-skill/' + skill, case.skill_factor(skill) == 2 and case.skill_modifier(skill) == 7)
        remember('new-skill/' + skill, old, case)
    for skill in sorted(baseline.skill_sources):
        case = history(); old = case.snapshot(); case.acquire('prodigy', 4, choices(expertise=skill))
        check('existing-skill/' + skill, case.skill_factor(skill) == 2 and case.skill_factor('Investigation') == 1)
        remember('existing-skill/' + skill, old, case)

    for level, expected_modifier in [(4, 7), (5, 9), (8, 9), (9, 11), (12, 11), (13, 13), (16, 13), (17, 15), (20, 15)]:
        h.advance(level)
        check('Expertise-2PB-at-level-' + str(level), h.skill_modifier('Investigation') == expected_modifier)
    check('level-growth-does-not-reinitialize-trade-or-give-languages', h.trades['Tinkering'] == {'level': 1, 'xp': 0} and len(h.languages.known) == 5)
    h.earn(8); reject('nonrepeatable-at-new-opportunity', h, choices(skill='Stealth', tool='tools.flute', language='goblin', expertise='Stealth'), level=8)
    fresh = history(); fresh.acquire('prodigy', 4, choices())
    reject('same-opportunity-cannot-buy-another-feat', fresh, {'skill': 'Stealth', 'expertise': 'Stealth'}, sid='skill_expert')
    fresh.advance(8); fresh.earn(8)
    reject('second-Expertise-source-cannot-select-existing-expert', fresh, {'skill': 'Stealth', 'expertise': 'Investigation'}, sid='skill_expert', level=8)
    old = fresh.snapshot(); fresh.acquire('skill_expert', 8, {'skill': 'Stealth', 'expertise': 'Stealth'})
    check('separately-paid-skill-expert-keeps-two-distinct-experts', fresh.skill_modifier('Investigation') == 9 and fresh.skill_modifier('Stealth') == 9 and len(fresh.pay.grants) == 2)
    remember('Prodigy4-SkillExpert8', old, fresh)
    reverse = history(); reverse.acquire('skill_expert', 4, {'skill': 'Investigation', 'expertise': 'Investigation'})
    reverse.advance(8); reverse.earn(8)
    reject('Prodigy-after-SkillExpert-cannot-redouble', reverse, choices(skill='Stealth', expertise='Investigation'), level=8)
    old = reverse.snapshot(); reverse.acquire('prodigy', 8, choices(skill='Stealth', expertise='Stealth'))
    check('SkillExpert4-Prodigy8-preserves-actual-separate-payments', [g['opportunity'] for g in reverse.pay.grants] == ['Warrior:4', 'Warrior:8'])
    remember('SkillExpert4-Prodigy8', old, reverse)

    for label, value in {
        'existing-skill': choices(skill='Athletics'), 'invented-skill': choices(skill='Spellcraft'),
        'known-tool': choices(tool='tools.dice-set'), 'invented-tool': choices(tool='supertools'),
        'weapon-not-tool': choices(tool='simple-melee-weapons.dagger'), 'language-fully-known': choices(language='elvish'),
        'unsupported-language': choices(language='draconic'), 'ungranted-secret-language': choices(language='the-voice'),
        'alias-label-not-resolved-identity': choices(language='Mycelian'), 'unknown-expertise': choices(expertise='Stealth'),
        'tool-not-skill-expertise': choices(expertise='tools.tinker-s-tools'),
        'unspent-skill-slot': choices(skill=None), 'unspent-tool-slot': choices(tool=None),
        'unspent-language-slot': choices(language=None), 'unspent-expertise-slot': choices(expertise=None),
        'unprinted-ability-field': {**choices(), 'abilityIncrease': 'INT'},
    }.items():
        reject(label, history(), value)
    for field in choices():
        c = choices(); del c[field]; reject('missing-choice-field/' + field, history(), c)
    unpaid = history(); unpaid.pay.opportunities.clear(); reject('no-earned-opportunity', unpaid, choices())
    bad_lineage = history(); bad_lineage.actor['ancestry'] = 'elf'; reject('cosmetic-ancestry-does-not-qualify', bad_lineage, choices())

    # Language permutations use actual reviewed IDs, with declared world/contact
    # premises; they do not assert an authenticated campaign or secret grant.
    for sid in ['goblin', 'giant', 'trollish', 'gnomish']:
        case = history(); old = case.snapshot(); case.acquire('prodigy', 4, choices(language=sid))
        check('language-option/' + sid, case.languages.known[sid] == set(modes))
        if sid == 'trollish':
            check('Trollish-does-not-grant-Giant', 'giant' not in case.languages.known)
        remember('language-option/' + sid, old, case)
    for sid, granted_modes in [('draconic', modes), ('runic', ['reading', 'writing'])]:
        extra = {'language': sid, 'modes': granted_modes, 'admission': 'source-qualified-contact',
                 'contactPremise': 'Explicitly conditional admitted contact grants this option and its exact modes; no actual lore/source entitlement is asserted.',
                 'evidenceMode': 'conditional_fixture'}
        case = history(options=available+[extra]); old = case.snapshot(); case.acquire('prodigy', 4, choices(language=sid))
        check('conditional-special/' + sid, case.languages.known[sid] == set(granted_modes))
        remember('conditional-special/' + sid, old, case, 'Conditional allowed-contact fixture only; no new campaign entitlement, class or cosmology')
    for label, row in {
        'no-contact': {'language': 'gnomish', 'modes': modes, 'admission': 'ordinary-contact', 'evidenceMode': 'conditional_fixture'},
        'exotic-as-ordinary': {'language': 'draconic', 'modes': modes, 'admission': 'ordinary-contact', 'evidenceMode': 'conditional_fixture', 'contactPremise': 'conditional'},
        'Runic-invented-speech': {'language': 'runic', 'modes': modes, 'admission': 'source-qualified-contact', 'evidenceMode': 'conditional_fixture', 'contactPremise': 'conditional'},
        'fixture-mislabeled-campaign': {'language': 'gnomish', 'modes': modes, 'admission': 'ordinary-contact', 'evidenceMode': 'campaign_record', 'contactPremise': 'conditional'},
    }.items():
        try:
            LanguageChoices(language, [row])
        except ValueError as error:
            results.append({'id': label, 'passed': True, 'reason': str(error)})
        else:
            check(label, False)
    case = history(); case.languages.add('gnomish', {'speaking', 'spokenComprehension'}, 'conditional prior narrower grant premise')
    old = case.snapshot(); event = case.acquire('prodigy', 4, choices())
    check('existing-language-genuine-missing-modes', event['orderedChoices'][2]['newModes'] == ['reading', 'writing'])
    remember('complete-real-missing-modes', old, case, 'Conditional prior narrower competency premise; no complete source history claimed')
    lang = LanguageChoices(language, available)
    lang.add('orcish', {'speaking'}, 'conditional fixed source A'); lang.add('orcish', {'reading', 'writing'}, 'conditional fixed source B')
    check('fixed-duplicate-unions-modes-preserves-provenance', len(lang.known) == 1 and len(lang.receipts) == 2 and lang.known['orcish'] == {'speaking', 'reading', 'writing'})
    check('shared-script-does-not-create-language-semantics', 'dwarvish-script' in lang.scripts and 'gnomish' not in lang.known)
    try:
        history(starting=['dwarvish', 'dwarvish', 'orcish'])
    except ValueError:
        check('starting-choice-duplicate-rejected', True)
    else:
        check('starting-choice-duplicate-rejected', False)
    a = deepcopy(actor); a.update(background='arcane-academy-dropout', backgroundToolChoice=None)
    academy = history(a, starting=['dwarvish', 'elvish', 'orcish', 'goblin'])
    old = academy.snapshot(); academy.acquire('prodigy', 4, choices())
    check('Academy-two-real-language-choices-plus-feat', len(academy.languages.known) == 6)
    remember('Academy-source-choice-count', old, academy)

    # Exhaustion is an explicitly conditional state boundary, not an assertion
    # that the five paid Warrior opportunities can purchase every proficiency.
    for part in ['skill', 'tool', 'language', 'all']:
        case = history(); c = choices()
        if part in {'skill', 'all'}:
            case.skill_sources = {s: {'conditional-complete-training-premise': 1 if part == 'skill' else 2} for s in skills}
            c['skill'] = None
            c['expertise'] = 'Investigation' if part == 'skill' else None
        if part in {'tool', 'all'}:
            case.tools = set(case.tool_catalog); case.trades = {t: {'level': 5, 'xp': 7} for t in case.primary.values()}
            c['tool'] = None
        if part in {'language', 'all'}:
            for row in available:
                case.languages.add(row['language'], row['modes'], 'conditional all-options-already-known premise')
            c['language'] = None
        old = case.snapshot(); event = case.acquire('prodigy', 4, c)
        check(part + '/exhausted-slot-no-banked-credit', not event['futureChoiceCredit'] and case.pay.opportunities['Warrior:4']['spent'])
        if part == 'all':
            check('all-exhausted-still-spends-one-choice-no-extra-benefit', all(x['state'] == 'exhausted' for x in event['orderedChoices']) and case.trades == old['trades'] and case.tools == set(old['tools']) and case.pay.scores == old['payment']['scores'])
        remember('conditional-exhaustion/' + part, old, case, 'Conditional saturation boundary only; not a lawful full character acquisition history')
    case = history(); case.trades['Tinkering'] = {'level': 5, 'xp': 7}; case.tools.add('tools.tinker-s-tools')
    old = case.snapshot(); case.acquire('prodigy', 4, choices(tool='tools.flute'))
    check('existing-trade-retains-level-and-XP', case.trades == {'Tinkering': {'level': 5, 'xp': 7}})
    remember('conditional-existing-trade-preservation', old, case, 'Conditional prior earned trade state; no full crafting history simulated')

    # Bind to the unchanged actual candidate, not only a hand-written model.
    candidate = read(paths[14]); current_prodigy = candidate['feats'][213]
    check('candidate-identity-guard', current_prodigy['id'] == 'prodigy')
    check('all-source-inputs-byte-unchanged', [info(p) for p in paths] == bindings)
    check('candidate-selection-stays-disabled', contracts['prodigy']['candidateSelectionEnabled'] is False)
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'finite-paid-Prodigy-choices-validated-not-runtime',
              'sourceBindings': bindings, 'checks': len(results), 'failures': [], 'results': results,
              'counts': {'sourceToolProfiles': len(tool_ids), 'primaryTrades': len(primary_seen), 'recordedTraces': len(traces),
                         'newPartialPrerequisiteIdentities': 0},
              'fullSourceProcedure': contracts['prodigy']['completeOperativeProcedure'],
              'actorSourceProjection': actor, 'conditionalWorldAdmissionPremises': available,
              'toolProjection': baseline.tool_catalog, 'primaryToolBindings': baseline.primary, 'traces': traces,
              'limits': ['Finite actual Human/Imperial/Warrior first-class training, generated abilities, earned ASI and ordered feat choices; not a complete class build.',
                         'All language contact and saturation/partial-mode/prior-trade states are explicitly conditional; no campaign history authenticated.',
                         'Half-elf/Half-orc external-lineage predicates remain separately covered in the earlier lineage report; this pass creates neither option.',
                         'Restricted language sources outside supplied ordinary/contact premises remain unestablished; no cosmology interpreted.',
                         'No full game use engine, 335 complete acquisitions, 660 original examples, exact candidate approval, balance or software implementation claimed.'],
              'originalSourcesDeleted': False, 'fullFeatCandidateApproved': False, 'runtimeImplemented': False}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=serial)+'\n', encoding='utf-8', newline='\n')
    notes.write_text('# Prodigy ordered-choice evidence\n\n'
                    f'{len(results)} finite checks passed, with {len(traces)} recorded traces. '
                    'The actual Human/Imperial Warrior slice spends one real scheduled feat opportunity, resolves skill/tool/language before Expertise, '
                    'and can apply Expertise to its newly learned skill. All 42 actual profiled tool choices and all 16 primary-trade bindings are exercised. '
                    'Primary tools initialize only their actual trade at level 1/zero XP; proficiency creates no kit or supplies.\n\n'
                    'The pass also covers separately paid Skill Expert order, duplicate/repeated/unpaid rejection, PB scaling, ordinary and conditional special language modes, '
                    'source starting-language counts, and exhausted slots without substitute or future credit. '
                    'Contact premises, prior narrower language grants, saturated training and prior trade histories are expressly conditional—not authenticated campaign facts or complete builds.\n\n'
                    'This adds acquisition-choice evidence for an already counted identity. It adds no new feat, changes no rule or source flag, '
                    'and does not complete all feat acquisitions/use, original examples, exact GPT review or runtime implementation.\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks': len(results), 'failures': 0, 'counts': report['counts'], 'report': info(output), 'notes': info(notes)}, indent=2))


if __name__ == '__main__':
    main()
