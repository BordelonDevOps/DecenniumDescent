"""Reference access and ordinary-cast pricing, not a combat/effect simulator."""
import math


class SpellRuleError(ValueError):
    pass


def integer(value, label, minimum, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum or (maximum is not None and value > maximum):
        raise SpellRuleError(f'Invalid {label}')
    return value


def access_for(spell, class_name, class_level, *, require_operational=True):
    integer(class_level, 'class level', 1, 20)
    if require_operational and spell['status'] != 'operational-playtest-draft':
        raise SpellRuleError('Spell is not operational in this packet')
    access = spell['classAccess'].get(class_name)
    if access is None:
        raise SpellRuleError('Class has no ordinary access to this spell')
    if class_level < access['minimumClassLevel']:
        raise SpellRuleError('Class-level spell gate is not met')
    return access


def quote_cast(spell, class_name, class_level, *, available_spell_ids, rp, max_rp,
               dissonance, proficiency, casting_modifier, previous_spell_id=None,
               previous_refrain=0, traumatic_casting=False):
    """Price one already-target-legal cast. Does not consume actions or apply class cadence hooks.

    available_spell_ids must be the character's actually known/prepared repertoire, not all
    catalog options. The caller verifies components, targets, concentration choice and action.
    Traumatic casting must be granted by an explicit Lich/Necromancer feature, never inferred.
    """
    access = access_for(spell, class_name, class_level)
    if spell['id'] not in available_spell_ids:
        raise SpellRuleError('Spell is not currently known/prepared')
    integer(max_rp, 'maximum RP', 0)
    integer(rp, 'RP', 0, max_rp)
    integer(dissonance, 'Dissonance', 0)
    integer(proficiency, 'proficiency', 2, 6)
    integer(casting_modifier, 'casting modifier', -5, 10)
    integer(previous_refrain, 'Refrain', 0, 3)
    rank = access['rank']
    limit = max(4, 2 + proficiency + max(0, casting_modifier))
    state = 3 if dissonance >= limit+6 else 2 if dissonance >= limit+3 else 1 if dissonance >= limit else 0
    if rank > 0 and state == 3 and not traumatic_casting:
        raise SpellRuleError('Fractured: ordinary ranked casting is blocked')
    surcharge = state if rank > 0 else 0
    cost = access['baseRpCost'] + spell['additionalRpCost'] + surcharge
    if rp < cost:
        raise SpellRuleError('Insufficient RP')
    refrain = min(3, previous_refrain+1) if previous_spell_id == spell['id'] else 0
    base_d = 0 if rank == 0 else 1 if rank <= 5 else 2
    return {'spellId':spell['id'], 'rank':rank, 'cost':cost, 'baseRpCost':access['baseRpCost'],
            'additionalRpCost':spell['additionalRpCost'], 'surcharge':surcharge,
            'rpAfterPayment':rp-cost, 'limit':limit, 'refrain':refrain,
            'dissonanceAddedBeforeClassInterface':base_d+refrain,
            'dissonanceBeforeClassInterface':dissonance+base_d+refrain,
            'trauma':rank*state if traumatic_casting and rank > 0 and state else 0}


def retune_amount(max_rp, casting_modifier):
    integer(max_rp, 'maximum RP', 0)
    integer(casting_modifier, 'casting modifier', -5, 10)
    # Explicit halves-up interpretation matches positive-number JS Math.round.
    return max(0, math.floor(max_rp/4 + 0.5) + casting_modifier)
