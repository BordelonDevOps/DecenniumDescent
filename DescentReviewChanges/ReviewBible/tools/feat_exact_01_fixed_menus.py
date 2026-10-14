"""Permanent maneuver, metamagic and elemental acquisition menu reference slice.

No attack, spell activation, resource recharge or complete class build is
executed here. Actual-use predicates remain in the full source procedures.
"""
from copy import deepcopy
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains

ELEMENTS = ('acid', 'cold', 'fire', 'lightning', 'thunder')
METAMAGIC = ('Reach', 'Widen', 'Sculpt')
IDS = {'martialAdept', 'martial_adept_advanced', 'metamagicAdept', 'elementalAdept', 'elemental_mastery'}


class FixedMenus(RemainingOwnedChains):
    def acquire_menu(self, sid, level, choice):
        if sid not in IDS:
            raise ValueError('Outside the named acquisition-menu cohort')
        if not self.prerequisite(sid):
            raise ValueError('Actual current acquisition prerequisite not established')
        additions = {}
        if sid in {'martialAdept', 'martial_adept_advanced', 'metamagicAdept'}:
            if not isinstance(choice, list) or len(choice) != 2 or any(not isinstance(x, str) for x in choice) or len(set(choice)) != 2:
                raise ValueError('Exactly two distinct permanent menu identities required')
            menu = set(METAMAGIC) if sid == 'metamagicAdept' else {r['id'] for r in self.supplements['SUP-03']}
            if not set(choice) <= menu:
                raise ValueError('An imported class maneuver or unknown mode is not this feat menu')
            if sid == 'metamagicAdept':
                additions[sid] = {'modes': list(choice), 'sorceryPoints': {'maximum': 2, 'current': 2},
                    'classMetaspellGranted': False}
            elif sid == 'martialAdept':
                if 'feat_superiority' in self.initializations:
                    raise ValueError('Prior pool cannot be reinitialized')
                additions['feat_superiority'] = {'maneuvers': list(choice), 'maximum': 1, 'current': 1,
                    'dieSides': 6, 'sourceGrants': ['martialAdept']}
            else:
                prior = self.initializations.get('feat_superiority')
                if not prior or prior['sourceGrants'] != ['martialAdept'] or len(set(prior['maneuvers'])) != 2:
                    raise ValueError('Actual earlier parent choices and pool history required')
                if set(choice) & set(prior['maneuvers']):
                    raise ValueError('Advanced choices must exclude both prior maneuvers')
                if prior['maximum'] != 1 or prior['dieSides'] != 6 or prior['current'] not in (0, 1):
                    raise ValueError('Prior one-d6 resource history is invalid')
                additions['feat_superiority'] = {'maneuvers': prior['maneuvers'] + list(choice),
                    'maximum': 2, 'current': prior['current'] + 1, 'dieSides': 6,
                    'sourceGrants': ['martialAdept', 'martial_adept_advanced']}
        else:
            if not isinstance(choice, str) or choice not in ELEMENTS:
                raise ValueError('Permanently choose one of the five printed elemental types')
            additions[sid] = {'chosenDamageType': choice}
        grant = self.pay.commit(sid, self.first + ':' + str(level), choice=choice, prerequisites_met=True)
        self.initializations.update(deepcopy(additions))
        return grant
