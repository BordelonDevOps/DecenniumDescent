"""Source-bound first-class training projections for feat prerequisites.

This is not a full character builder. Languages, class-card choices, equipment
possession and background feature effects are outside the projection and confer
no extra credential. It supports only the explicitly supplied source classes,
backgrounds, Human/Imperial skill choices and named training feat grants.
"""
from math import floor


def proficiency_bonus(total_level):
    if not 1 <= total_level <= 20:
        raise ValueError('Invalid total level')
    return 2+(total_level-1)//4


def normalize_name(value):
    return value.casefold().replace('’', "'").strip()


def weapon_profiles_for(first_class, equipment):
    """Finite mapping of the actual first-class source training rows.

    A weapon's physical possession and its most recent attack delivery are
    deliberately absent. Only actual profiled equipment can be returned.
    """
    simple = first_class in {'Bard', 'Paladin', 'Dragoon', 'Monk'}
    martial = first_class in {'Warrior', 'Paladin'}
    named = {
        'Bard': set(), 'Paladin': set(), 'Warrior': set(),
        'Dragoon': {'spear', 'glaive', 'trident'},
        'Monk': {'kama', 'nunchaku', 'quarterstaff'},
        'Thief': {'dagger', 'shortsword', 'crossbow, hand'},
        'Shaman': {'club', 'spear', 'quarterstaff'},
        'Soldier': {'repeating heavy crossbow'},
    }
    if first_class not in named:
        raise ValueError('First-class weapon row outside this finite projection')
    result = set()
    for sid, row in equipment.items():
        if 'weapons' not in row['category'].lower():
            continue
        category = row['category'].lower()
        properties = row['sourceFields'].get('Properties', '').lower()
        name = normalize_name(row['name'])
        if (simple and category.startswith('simple ')
                or martial and category.startswith('martial ')
                or name in named[first_class]
                or first_class == 'Thief' and 'thrown' in properties):
            result.add(sid)
        # Soldier's sidearm clause is not a grant of every martial weapon.
        # No unclassified weapon is silently relabeled as a sidearm.
        if first_class == 'Soldier' and row.get('sidearm') is True:
            result.add(sid)
    return result


def materialize_training(actor, classes, equipment, skill_abilities, ancestry, backgrounds):
    first = classes[actor['firstClass']]
    if any(type(value) is not int or not 1 <= value <= 20 for value in actor['classLevels'].values()):
        raise ValueError('Invalid attained class level')
    if actor['classLevels'].get(actor['firstClass'], 0) < 1:
        raise ValueError('The recorded first class must be attained')
    if set(actor['classLevels']) != {actor['firstClass']}:
        raise ValueError('This projection supports a single first class, not inferred multiclass grants')
    selected = actor['selectedClassSkills']
    if len(selected) != first['skillChoices'] or len(set(selected)) != len(selected):
        raise ValueError('Wrong number of distinct starting class skill choices')
    if not set(selected) <= set(first['skillOptions']):
        raise ValueError('Starting skill outside the actual first-class list')
    if actor['ancestry'] != 'human' or actor['variant'] != 'imperial-human':
        raise ValueError('Unmodeled ancestry or variant')
    human = next(row for row in ancestry['ancestries'] if row['id'] == 'human')
    imperial = next(row for row in human['variants'] if row['id'] == 'imperial-human')
    if actor['ancestrySkillChoice'] != 'Reputation':
        raise ValueError('This finite witness fixes Human Versatility to Reputation')
    if set(actor['abilityRolls']) != {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}:
        raise ValueError('Six source-generated abilities required')
    if any(len(dice) != 4 or any(type(die) is not int or not 1 <= die <= 6 for die in dice)
           for dice in actor['abilityRolls'].values()):
        raise ValueError('Invalid four-d6/drop-lowest witness')
    scores = {key: sum(dice)-min(dice)+imperial['combinedAbilityBonuses'][key]
              for key, dice in actor['abilityRolls'].items()}
    if scores != actor['permanentScores']:
        raise ValueError('Permanent ability snapshot does not match generation and ancestry')
    skills = {'Reputation': 1, 'Persuasion': 1}
    receipts = [{'credential': 'Reputation', 'source': 'human/Versatility', 'choice': True},
                {'credential': 'Persuasion', 'source': 'imperial-human/Social Intuition', 'choice': False}]
    background = backgrounds[actor['background']]
    if actor['background'] == 'disgraced-noble-scion':
        if background['skillsSource'] != 'History, Persuasion' or actor['backgroundDuplicateSkillChoice'] != 'Performance':
            raise ValueError('Unexpected noble background skill procedure')
        skills.update({'History': 1, 'Performance': 1})
        receipts.extend([{'credential': 'History', 'source': 'disgraced-noble-scion'},
                         {'credential': 'Performance', 'source': 'fixed Persuasion duplicate replacement',
                          'authority': 'CHARACTER_CREATION_PLAYTEST duplicate fixed skill rule'}])
    elif actor['background'] == 'arcane-academy-dropout':
        if background['skillsSource'] != 'Arcana, History':
            raise ValueError('Unexpected academy background skills')
        skills.update({'Arcana': 1, 'History': 1})
        receipts.extend({'credential': name, 'source': 'arcane-academy-dropout'} for name in ['Arcana', 'History'])
    else:
        raise ValueError('Unmodeled background')
    if set(selected) & set(skills):
        raise ValueError('Selectable class grant must choose a different eligible skill')
    for name in selected:
        skills[name] = 1
        receipts.append({'credential': name, 'source': actor['firstClass']+'/first-class-skill-choice'})

    tools = set()
    choices = actor['classToolChoices']
    if actor['firstClass'] == 'Bard':
        if len(choices) != 3 or len(set(choices)) != 3 or any(equipment[sid].get('group') != 'Musical Instruments' for sid in choices):
            raise ValueError('Bard requires three distinct actual musical instruments')
        tools.update(choices)
    elif actor['firstClass'] == 'Monk':
        if len(choices) != 1 or equipment[choices[0]].get('group') != "Artisan's Tools":
            raise ValueError('Monk requires one actual artisan tool choice')
        tools.update(choices)
    else:
        if choices:
            raise ValueError('This fixed source tool row does not authorize an extra choice')
        fixed = {
            'Warrior': [], 'Paladin': [],
            'Dragoon': ["Leatherworker's tools"],
            'Thief': ["Thieves' tools", "Poisoner's kit"],
            'Shaman': ["Alchemist's supplies", 'Herbalism kit'],
            'Soldier': ["Carpenter's tools"],
        }[actor['firstClass']]
        for name in fixed:
            matches = [sid for sid, item in equipment.items() if normalize_name(item['name']) == normalize_name(name)
                       and item['category'] == 'Tools']
            if len(matches) != 1:
                raise ValueError('Actual fixed tool profile missing or ambiguous: '+name)
            tools.add(matches[0])
    if actor['background'] == 'disgraced-noble-scion':
        sid = actor['backgroundToolChoice']
        if sid not in equipment or equipment[sid].get('group') != 'Gaming Sets':
            raise ValueError('Actual noble gaming-set choice required')
        tools.add(sid)
    elif actor['backgroundToolChoice'] is not None:
        raise ValueError('Academy background supplies no tool choice')

    # These two actual feat procedures are sufficient for this finite cohort.
    # Their paid class opportunities are validated by the caller before use.
    seen_grants = set()
    for grant in actor['priorFeatChoices']:
        sid = grant['featId']
        if sid in seen_grants:
            raise ValueError('A prior nonrepeatable feat cannot be purchased twice')
        seen_grants.add(sid)
        if sid in {'alert', 'alertness', 'lucky'}:
            continue
        if sid == 'skill_expert':
            new_skill, expertise = grant['newSkill'], grant['expertiseSkill']
            if new_skill not in skill_abilities or new_skill in skills:
                raise ValueError('Skill Expert requires a new actual skill, not a tool')
            skills[new_skill] = 1
            if expertise not in skill_abilities or skills.get(expertise, 0) != 1:
                raise ValueError('Expertise must choose a now-proficient skill without Expertise')
            skills[expertise] = 2
            receipts.append({'credential': expertise, 'source': 'skill_expert', 'contribution': 'replacing 2PB'})
        elif sid == 'naturalist':
            if scores['WIS'] < 13:
                raise ValueError('Naturalist permanent Wisdom13 required')
            for name in ['Nature', 'Survival']:
                skills[name] = 2 if skills.get(name, 0) else 1
            receipts.append({'credential': 'Nature and Survival', 'source': 'naturalist', 'fixedSnapshot': True})
        else:
            raise ValueError('Prior feat not modeled as a source of this training')

    armor = {token.strip().lower() for token in first['armor'].split(';')}
    return {'scores': scores, 'skills': skills, 'tools': tools, 'armor': armor,
            'weapons': weapon_profiles_for(actor['firstClass'], equipment),
            'receipts': receipts, 'totalLevel': sum(actor['classLevels'].values())}


def meets_training_prerequisite(node, actor, training, equipment, skill_abilities):
    def proficiency(credential):
        if credential in skill_abilities:
            return training['skills'].get(credential, 0) >= 1
        if credential in {'light armor', 'medium armor', 'shields'}:
            return credential.removesuffix(' armor') in training['armor']
        if credential == 'at least one actual tool':
            return bool(training['tools'])
        if credential == 'Smith tools / Blacksmithing':
            return 'tools.smith-s-tools' in training['tools']
        if credential == 'thieves tools mechanical disarm interface':
            return 'tools.thieves-tools' in training['tools']
        if credential == 'bounded INT(Nature) anatomy bridge':
            return training['skills'].get('Nature', 0) >= 1
        if credential == 'legacy Knowledge (Monstrous Humanoids)':
            # No legacy character receipt is supplied by these current-source witnesses.
            return False
        raise ValueError('Unmodeled credential: '+credential)

    def weapon(category):
        candidates = training['weapons']
        if category == 'permanently chosen actual profile':
            chosen = actor.get('weaponChoice')
            return chosen in candidates and chosen in equipment
        for sid in candidates:
            row = equipment[sid]
            classification = row['category'].lower()
            properties = row['sourceFields'].get('Properties', '').lower()
            if (category == 'any actual profile'
                    or category == 'melee' and classification.endswith('melee weapons')
                    or category == 'ranged' and classification.endswith('ranged weapons')
                    or category == 'martial' and classification.startswith('martial ')
                    or category == 'Two-Handed-property' and 'two-handed' in properties
                    or category in {'longbow', 'shortbow', 'whip'} and row['name'].lower() == category):
                return True
        return False

    kind = node['kind']
    if kind == 'all':
        return bool(node['requirements']) and all(meets_training_prerequisite(child, actor, training, equipment, skill_abilities)
                                                for child in node['requirements'])
    if kind == 'any':
        return bool(node['requirements']) and any(meets_training_prerequisite(child, actor, training, equipment, skill_abilities)
                                                for child in node['requirements'])
    if kind == 'permanentAbility':
        return training['scores'][node['ability']] >= node['minimum']
    if kind == 'totalCharacterLevel':
        return training['totalLevel'] >= node['minimum']
    if kind == 'classLevel':
        return actor['classLevels'].get(node['className'], 0) >= node['minimum']
    if kind == 'actualProficiency':
        return proficiency(node['credential'])
    if kind == 'actualWeaponProficiency':
        return weapon(node['category'])
    if kind == 'permanentSkillModifier':
        if node['skill'] == 'thieves tools':
            factor = int('tools.thieves-tools' in training['tools'])
            ability = 'DEX'  # Only the explicit FS-02/printed Thievery acquisition bridge.
        else:
            factor = training['skills'].get(node['skill'], 0)
            ability = skill_abilities[node['skill']]
        if node['ability'] != ability:
            raise ValueError('Governing ability differs from the current skill/explicit tool bridge')
        if factor not in {1, 2}:
            return False
        modifier = floor((training['scores'][ability]-10)/2)+proficiency_bonus(training['totalLevel'])*factor
        return modifier >= node['minimum']
    if kind == 'noPrintedPrerequisite':
        return True
    raise ValueError('Outside this training prerequisite cohort: '+kind)
