"""Finite numeric prerequisite model; not a character builder or feat runtime.

Only the numeric part of a source contract and an already earned opportunity
are assessed here. Selection choices, repeatability, payload availability and
ongoing use conditions remain separate gates.
"""

NUMERIC_KINDS = frozenset({
    'permanentAbility', 'totalCharacterLevel', 'noPrintedPrerequisite',
    'all', 'any',
})


def is_numeric_tree(node):
    kind = node.get('kind')
    if kind not in NUMERIC_KINDS:
        return False
    if kind in {'all', 'any'}:
        children = node.get('requirements')
        return isinstance(children, list) and bool(children) and all(
            is_numeric_tree(child) for child in children)
    return True


def meets_numeric_prerequisite(node, permanent_scores, class_levels):
    """Read permanent scores and actual class levels, never temporary bonuses."""
    if not is_numeric_tree(node):
        raise ValueError('Unsupported or empty numeric prerequisite tree')
    if set(permanent_scores) != {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}:
        raise ValueError('Six recorded permanent abilities required')
    if any(type(score) is not int for score in permanent_scores.values()):
        raise ValueError('Permanent abilities must be integers')
    if not class_levels or any(type(n) is not int or n < 1 for n in class_levels.values()):
        raise ValueError('Positive attained class levels required')
    if not 1 <= sum(class_levels.values()) <= 20:
        raise ValueError('Total character level outside the foundation range')

    def resolve(part):
        kind = part['kind']
        if kind == 'noPrintedPrerequisite':
            return True
        if kind == 'permanentAbility':
            return permanent_scores[part['ability']] >= part['minimum']
        if kind == 'totalCharacterLevel':
            return sum(class_levels.values()) >= part['minimum']
        if kind == 'all':
            return all(resolve(child) for child in part['requirements'])
        if kind == 'any':
            return any(resolve(child) for child in part['requirements'])
        raise ValueError('Unsupported numeric atom')

    return resolve(node)


def numeric_and_opportunity_gate(node, paid_choices, opportunity):
    """Necessary gates only. True does not authorize a complete acquisition."""
    numeric = meets_numeric_prerequisite(
        node, paid_choices.scores, paid_choices.current_classes)
    receipt = paid_choices.opportunities.get(opportunity)
    return bool(numeric and receipt is not None and not receipt['spent'])
