"""Named paid feat chains and acquisition fields, not a use/runtime engine.

The source-bound parent class retains the earlier evidence unchanged. This
extension adds only the explicitly listed acquisition procedures.
"""
from copy import deepcopy
from feat_exact_01_composite_casting_model import CompositeCastingHistory


class RemainingOwnedChains(CompositeCastingHistory):
    IDS = {'curse_channeling', 'dark_binding', 'conjure_flora', 'verdant_bond',
           'trapcasting', 'lightning_affinity', 'stormcaller', 'voltyros_pact',
           'companion_training', 'berserker'}

    def actual_casting_routes(self):
        """Select a retained acquired route, not a spell label or a class name."""
        routes = []
        for spell in self.casting.qualifying():
            ability = spell.get('ability')
            if spell['kind'].startswith('wizard-'):
                ability = 'INT'
            if ability not in {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}:
                raise ValueError('Actual route lacks its source casting ability')
            route = {'grantId': spell['grantId'], 'ability': ability,
                     'sourceClass': spell.get('sourceClass')}
            if route not in routes:
                routes.append(route)
        return routes

    def acquire_named(self, sid, level, choice=None):
        if sid not in self.IDS:
            raise ValueError('Outside this finite named acquisition extension')
        qualified = self.prerequisite(sid)
        additions = {}
        if sid == 'stormcaller':
            if choice not in self.actual_casting_routes():
                raise ValueError('Permanently select an actual owned casting route')
            additions = {'fixedCastingRoute': deepcopy(choice),
                         'staticFieldUses': {'maximum': 1, 'current': 1},
                         'stormstepUses': {'maximum': 1, 'current': 1},
                         'activeFields': [], 'afterimage': None}
        elif sid == 'voltyros_pact':
            routes = self.actual_casting_routes()
            abilities = {route['ability'] for route in routes} if routes else {'INT'}
            if not isinstance(choice, dict) or set(choice) != {'ability'} or choice['ability'] not in abilities:
                raise ValueError('Choose one actual casting ability, or INT only when no casting source exists')
            additions = {'fixedAbility': choice['ability'], 'noCastingFallback': not routes,
                         'stormformUses': {'maximum': 1, 'current': 1},
                         'eyeActive': False, 'stationaryInterval': None}
        elif sid == 'conjure_flora':
            if choice not in self.actual_casting_routes():
                raise ValueError('Permanently select an actual owned casting route')
            additions = {'fixedCastingRoute': deepcopy(choice)}
        elif choice is not None:
            raise ValueError('No permanent acquisition menu exists for this named procedure')
        if sid == 'curse_channeling':
            additions = {'marks': [], 'markCapacity': 2 if sum(self.pay.current_classes.values()) >= 10 else 1}
        elif sid == 'dark_binding':
            additions = {'boundWeapon': None, 'bindingRitualCompleted': False}
        elif sid == 'conjure_flora':
            additions.update({'creationUses': {'maximum': 1, 'current': 1},
                              'plantCapacity': 2 if sum(self.pay.current_classes.values()) >= 10 else 1, 'activePlants': [],
                              'additionalCreationPending': False})
        elif sid == 'verdant_bond':
            additions = {'messageUses': {'maximum': 1, 'current': 1}, 'storedMessage': None}
        elif sid == 'lightning_affinity':
            additions = {'stormChargeCapacity': 2, 'stormCharges': [], 'primedRider': None}
        elif sid == 'berserker':
            additions = {'rageUses': {'maximum': 1, 'current': 1}, 'rageActive': False}
        # No companion, curse, field, plant, storm, damage or rest is created by payment.
        result = self.pay.commit(sid, self.first + ':' + str(level), choice=choice,
                                 prerequisites_met=qualified)
        if additions:
            self.initializations[sid] = additions
        return result

    def advance(self, level):
        super().advance(level)
        if 'conjure_flora' in self.initializations:
            self.initializations['conjure_flora']['plantCapacity'] = 2 if sum(self.pay.current_classes.values()) >= 10 else 1
        if 'curse_channeling' in self.initializations:
            self.initializations['curse_channeling']['markCapacity'] = 2 if level >= 10 else 1
