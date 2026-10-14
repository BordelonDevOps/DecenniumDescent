"""Author source-bound synthetic Warrior acquisition witnesses; no rule edits."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


paths = [R/'data/public/class_playtests/warrior.json',
         R/'data/playtest/character_foundation.json',
         R/'data/playtest/ancestry_background_candidate.json',
         A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
         R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
         R/'data/director/feat_candidates/exact_01/shared_rules.json', Path(__file__)]
warrior, foundation, ancestry, contracts = map(read, paths[:4])
cards = {card['id']: card for card in warrior['cards']}
records = {record['id']: record for record in contracts['records'] if 'sharedPaidIdentity' in record}
assert len(records) == 12
profiles = {}
for card in warrior['cards']:
    if card['sourceKind'] != 'mutation':
        continue
    match = re.fullmatch(r'Warrior (\d+); (Basic|Advanced|Apex) (Vital|Combat|Aberrant)(?:; maximum one Apex equipped)?', card['prerequisite'])
    assert match, card['id']
    profiles[card['id']] = {**deepcopy(card), 'tier': match[2], 'tree': match[3]}

# Explicit authored history, checked separately against every attained source
# schedule row. No class/card ID is inferred from a feat's display name.
choices = {
    1: ['warrior.base.serum-injection', 'warrior.base.brutal-strike',
        'warrior.base.survival-instinct', 'warrior.base.combat-instinct'],
    2: ['warrior.base.physical-conditioning', 'warrior.base.brutality-sense'],
    3: ['warrior.arch.mutation-efficiency', 'warrior.arch.mutation-overload'],
    4: ['warrior.arch.brutal-fortitude'],
    5: ['warrior.arch.overpressure-response'],
    6: ['warrior.arch.crushing-advance'],
    7: ['warrior.arch.pain-conversion'],
    8: ['warrior.arch.adaptive-tissue'],
    9: ['warrior.arch.brutality-momentum'],
    10: ['warrior.hero.wardborn.guardian-tissue', 'warrior.hero.wardborn.bulwark-mutation-tree'],
    11: ['warrior.base.intimidating-presence'],
    12: ['warrior.hero.wardborn.mutated-guard'],
    13: ['warrior.base.mutation-surge'],
    14: ['warrior.hero.wardborn.guardian-pulse'],
    15: ['warrior.arch.serum-cocktail'],
    16: ['warrior.hero.wardborn.warding-mutation'],
    17: ['warrior.arch.brutality-unleashed'],
    18: ['warrior.hero.wardborn.stabilizing-injection'],
    19: ['warrior.arch.survival-adaptation'],
    20: [],
}
progression = []
for level in range(1, 21):
    automatic = [card['id'] for card in warrior['cards'] if card['acquisition'] == 'automatic'
                 and card['minimumClassLevel'] == level and card['path'] in (None, 'Wardborn')]
    progression.append({'class': 'Warrior', 'classLevel': level, 'totalLevel': level,
                        'selectedCards': choices[level], 'automaticCards': automatic,
                        'heroPath': 'Wardborn' if level >= 10 else None,
                        'ordinaryFeatOpportunity': level in warrior['asiClassLevels']})

human = next(row for row in ancestry['ancestries'] if row['id'] == 'human')
imperial = next(row for row in human['variants'] if row['id'] == 'imperial-human')
base_scores = {'STR': 15, 'DEX': 14, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8}
scores = {key: value+imperial['combinedAbilityBonuses'][key] for key, value in base_scores.items()}

def mutation(suffix):
    identity = 'warrior.supplement.'+suffix
    assert identity in profiles
    return identity


# Level columns are an example ordinary milestone after earlier choices are
# spent, not a claim no authorized retained opportunity could be used earlier.
templates = {
    'backlashEngine': (8, ['adrenal-backlash-core']),
    'bioStabilizer': (4, ['bloodthick-node']),
    'bornToHorrify': (16, ['mythic-carapace']),
    'distortedDominance': (4, ['bone-lure-growth']),
    'evisceratorProtocol': (8, ['echo-knuckles', 'warpgrip-talons']),
    'evolutionUnderFire': (16, ['mythic-carapace']),
    'hypermutationSpike': (16, ['butcherform-chassis']),
    'juggernautCore': (8, ['ossified-core']),
    'killChainAdaptation': (8, ['brute-knuckles', 'splinter-bone-fangs']),
    'livingFortress': (16, ['ironhide-graft', 'bloodthick-node', 'spinal-buffer']),
    'synapticRot': (8, ['wailing-eye-cluster']),
    'terrorEngine': (8, ['carrion-signal-gland']),
}
assert set(templates) == set(records)
fixtures = []
for sid, (level, names) in templates.items():
    equipped = [mutation(name) for name in names]
    slots_needed = [1, 5, 13, 20][len(equipped)-1]
    equipped_at = max(slots_needed, max(profiles[x]['minimumClassLevel'] for x in equipped))
    assert equipped_at < level
    prior_milestones = [n for n in warrior['asiClassLevels'] if n < level]
    prior_ids = ['alert', 'alertness', 'lucky']
    assert len(prior_milestones) <= len(prior_ids)
    record = records[sid]
    fixtures.append({
        'id': 'WACQ-'+sid, 'synthetic': True, 'featId': sid,
        'classCardAlias': record['sharedPaidIdentity']['classCardId'],
        'requirements': record['requirements'],
        'completeOperativeProcedure': record['completeOperativeProcedure'],
        'completeOriginalObject': record['originalObject'],
        'completeClassCounterpart': record['sharedPaidIdentity']['completeClassCounterpart'],
        'abilityMethod': 'standard-array', 'baseScores': base_scores,
        'ancestry': 'human', 'variant': 'imperial-human',
        'appliedAbilityBonuses': imperial['combinedAbilityBonuses'], 'permanentScores': scores,
        'chosenWarriorAbility': 'STR', 'classLevels': {'Warrior': level},
        'classProgression': progression[:level],
        'earlierFeatChoices': [{'classLevel': n, 'featId': prior}
                               for n, prior in zip(prior_milestones, prior_ids)],
        'equipmentReceipt': {
            'event': 'synthetic completed qualifying long rest',
            'atWarriorClassLevel': equipped_at,
            'equippedAfter': equipped,
            'allDormantAtAcquisition': True,
            'clockAndSupportAreSuppliedScenarioPremises': True,
            'note': 'The rest is an authored scenario premise, not an authenticated campaign event. '
                    'Its completion is earlier than the feat milestone; mutation names do not create slots.',
        },
        'acquisitionOpportunity': {'identity': f'Warrior:{level}', 'class': 'Warrior',
                                   'classLevel': level, 'unspent': True},
        'expectedPrerequisitesMet': True,
        'expectedPaidIdentity': sid,
        'expectedNewMutationSlots': 0,
        'expectedNewClassSelections': 0,
        'expectedFeatLimitedUseAtFirstAcquisition': {'longRest': 1} if sid == 'hypermutationSpike' else {},
        'scope': 'Complete named mutation/class prerequisite and one paid identity for a synthetic acquisition. '
                 'Full sheet, real campaign advancement/rest receipts and all use-time feat triggers are separate.',
    })

target = A/'FEAT_EXACT_01_WARRIOR_ACQUISITION_FIXTURES.json'
assert not target.exists()
result = {
    'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
    'status': 'authored-source-qualified-fixtures-awaiting-validation',
    'sourceBindings': [info(path) for path in paths],
    'ordinaryMutationProfiles': profiles,
    'completeClassSelectionHistoryThrough20': progression,
    'fixtures': fixtures,
    'pendingNarrowRuling': 'FEAT327-ACQ-02: global versus per-tree Advanced tier ceiling; '
                          'the12 positive fixtures fit both interpretations and use at most one Apex.',
    'sourceInformationDeleted': False, 'selectionEnabled': False,
    'candidateReadyForSubmission': False,
}
with target.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(result, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps({'fixtureFile': info(target), 'feats': len(fixtures),
                  'normalMutationProfiles': len(profiles), 'classHistoryLevels': len(progression)}, indent=2))
