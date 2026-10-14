"""Separate paid class-skill declaration and outcome for Versatile Mastery.

This finite interface uses an actual Action task and the foundation's normal
skill ability. It does not rule on other task timings or authorized variants.
"""
from copy import deepcopy
from core_playtest_rules import task_check
from feat335_borrowed_transactions import BorrowedTransactions


class BorrowedSkillTransactions(BorrowedTransactions):
    def declare_skill(self, event, declaration):
        if not isinstance(declaration, dict) or set(declaration) != {'skill', 'ability', 'dc', 'actualCheckAction'}:
            raise ValueError('Exact task declaration required; no roll/outcome keys')
        choice = self.preflight(event, 'skill')
        skill = declaration['skill']; ability = declaration['ability']; dc = declaration['dc']
        if choice != skill or choice in self.menu or skill not in self.acquired.skills:
            raise ValueError('Prepared actual donor class skill must match this task')
        if declaration['actualCheckAction'] is not True or self.actions < 1:
            raise ValueError('Actual legal task and its own Action required')
        if ability != self.acquired.skills[skill]:
            raise ValueError('This finite interface requires the normal sourced skill ability')
        if type(dc) is not int or dc < 0:
            raise ValueError('Actual task DC required before commitment')
        own_factor = self.acquired.training_projection['skills'].get(skill, 0)
        if own_factor not in {0, 1, 2}:
            raise ValueError('Actual own training contribution required')
        factor = max(1, own_factor)
        modifier = self.mod(ability) + factor * self.proficiency()
        provenance = self.commit(event, choice, None, 'action')
        self.pending = {'event': event, 'type': 'borrowed-skill', 'skill': skill, 'ability': ability,
            'dc': dc, 'modifier': modifier, 'ownTrainingFactor': own_factor,
            'borrowedTrainingFactor': 1, 'effectiveTrainingFactor': factor,
            'provenance': provenance, 'paidBeforeRolls': True}
        self.events[event]['status'] = 'committed-awaiting-rolls'
        return deepcopy(self.pending)

    def resolve_skill(self, event, natural):
        p = self.pending
        if not p or p['event'] != event or p['type'] != 'borrowed-skill':
            raise ValueError('Actual unresolved paid class-skill check required')
        result = task_check(natural, p['modifier'], p['dc'])
        self.events[event].update(status='resolved', result=deepcopy(result))
        self.pending = None
        return result

    def borrowed_skill(self, event, skill, natural, ability, dc, *, actual_check_action):
        # Compatibility for older named examples. Direct declare/resolve calls
        # demonstrate that payment itself requires no roll or known result.
        self.declare_skill(event, {'skill': skill, 'ability': ability, 'dc': dc,
                                  'actualCheckAction': actual_check_action})
        return self.resolve_skill(event, natural)
