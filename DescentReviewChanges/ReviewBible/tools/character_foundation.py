"""Reference calculations for the authored character foundation, not the live UI.

This module never changes a character save, grants a card or refreshes a resource.
Its input profiles are the separately reviewed character_foundation.json data.
"""
from math import ceil

ABILITIES = ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA')


def integer(value, label):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f'{label} must be an integer')
    return value


def ability_modifier(score):
    return (integer(score, 'Ability score') - 10) // 2


def proficiency_bonus(total_level):
    integer(total_level, 'Character level')
    if not 1 <= total_level <= 20:
        raise ValueError('Character level must be 1–20')
    return 2 + (total_level - 1) // 4


def point_buy_cost(scores):
    if len(scores) != 6:
        raise ValueError('Assign six pre-ancestry ability scores')
    costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
    for score in scores:
        integer(score, 'Point-buy score')
        if score not in costs:
            raise ValueError('Point-buy scores must be 8–15 before ancestry')
    cost = sum(costs[x] for x in scores)
    if cost > 27:
        raise ValueError('Point buy exceeds 27 points')
    return cost


def validate_class_levels(profiles, class_levels, acquisition_order):
    if not class_levels or set(class_levels) != set(acquisition_order):
        raise ValueError('Record every held class in acquisition order')
    if len(acquisition_order) != len(set(acquisition_order)):
        raise ValueError('Acquisition order cannot contain duplicates')
    for name, level in class_levels.items():
        if name not in profiles:
            raise ValueError(f'Unknown Base class: {name}')
        integer(level, 'Class level')
        if not 1 <= level <= 20:
            raise ValueError('Held class levels must be 1–20')
    total = sum(class_levels.values())
    proficiency_bonus(total)
    return total


def merged_rp(profiles, class_levels, acquisition_order):
    validate_class_levels(profiles, class_levels, acquisition_order)
    tier_order = {'none': 0, 'minor': 1, 'hybrid': 2, 'half': 3, 'full': 4}
    rows = []
    for acquired, name in enumerate(acquisition_order):
        profile = profiles[name]
        tier = profile['weaveTier']
        if tier == 'none':
            continue
        level = class_levels[name]
        rows.append({'class': name, 'level': level, 'tier': tier,
                     'pool': profile['rpByClassLevel'][level - 1], 'acquired': acquired})
    rows.sort(key=lambda row: (-tier_order[row['tier']], -row['level'],
                              -row['pool'], row['acquired']))
    if not rows:
        return {'maximum': 0, 'primary': None, 'secondary': None, 'secondaryBonus': 0,
                'noncontributingWeaveClasses': []}
    bonus = ceil(rows[1]['pool'] / 4) if len(rows) > 1 else 0
    return {'maximum': rows[0]['pool'] + bonus, 'primary': rows[0],
            'secondary': rows[1] if len(rows) > 1 else None, 'secondaryBonus': bonus,
            'noncontributingWeaveClasses': rows[2:]}


def base_maximum_hp(profiles, gained_levels, constitution_score):
    """Each chronological row is {class, base}; base is a recorded roll/fixed value."""
    if not 1 <= len(gained_levels) <= 20:
        raise ValueError('Record 1–20 chronological gained levels')
    modifier = ability_modifier(constitution_score)
    contributions = []
    hit_dice = {}
    for i, record in enumerate(gained_levels):
        name = record['class']
        if name not in profiles:
            raise ValueError(f'Unknown Base class: {name}')
        die = profiles[name]['hitDie']
        base = integer(record['base'], 'Recorded HP die value')
        if not 1 <= base <= die or (i == 0 and base != die):
            raise ValueError('First character level uses maximum; later bases must fit their class die')
        contributions.append(max(1, base + modifier))
        hit_dice[str(die)] = hit_dice.get(str(die), 0) + 1
    return {'baseMaximum': sum(contributions), 'contributions': contributions,
            'hitDiceBySize': hit_dice}


def new_class_prerequisite_failures(profiles, held_classes, new_class, scores):
    if new_class not in profiles or any(name not in profiles for name in held_classes):
        raise ValueError('Unknown Base class')
    if not held_classes or new_class in held_classes:
        return []  # The new-class entry test is not a recurring retention test.
    if set(scores) != set(ABILITIES):
        raise ValueError('Supply all six current ability scores')
    for score in scores.values():
        integer(score, 'Ability score')
    failures = []
    for name in dict.fromkeys([*held_classes, new_class]):
        for ability, required in profiles[name]['multiclassPrerequisites'].items():
            if scores[ability] < required:
                failures.append({'class': name, 'ability': ability, 'required': required,
                                 'actual': scores[ability]})
    return failures


def clamp_after_capacity_change(current, new_maximum):
    """A capacity change alone never fills a newly available resource or heals."""
    integer(current, 'Current resource')
    integer(new_maximum, 'Resource maximum')
    if current < 0 or new_maximum < 0:
        raise ValueError('Resources cannot be negative')
    return min(current, new_maximum)
