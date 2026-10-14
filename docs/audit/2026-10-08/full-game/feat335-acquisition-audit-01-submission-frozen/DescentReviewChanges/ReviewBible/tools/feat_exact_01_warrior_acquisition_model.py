"""Warrior mutation-feat qualification, separate from attacks and feat effects.

The caller supplies source-bound mutation profiles and the specifically
reviewed Advanced tier-cap scope. No class engine, equipment slot or active
mutation is granted by testing a prerequisite.
"""
from collections import Counter
from dataclasses import dataclass, field


def mutation_slots(warrior_level):
    return sum(warrior_level >= milestone for milestone in (1, 5, 13, 20))


def loadout_errors(warrior_level, equipped, profiles, advanced_scope):
    if advanced_scope not in {'global', 'per-tree'}:
        raise ValueError('An explicit Advanced tier-cap ruling is required')
    errors = []
    if len(equipped) != len(set(equipped)):
        errors.append('same mutation equipped twice')
    if len(equipped) > mutation_slots(warrior_level):
        errors.append('not enough unlocked mutation slots')
    if any(identity not in profiles for identity in equipped):
        return errors + ['unrecognized normal mutation profile']
    chosen = [profiles[identity] for identity in equipped]
    if any(card['minimumClassLevel'] > warrior_level for card in chosen):
        errors.append('mutation tier or card class gate not reached')
    if sum(card['tier'] == 'Apex' for card in chosen) > 1:
        errors.append('more than one Apex equipped')
    advanced = [card for card in chosen if card['tier'] == 'Advanced']
    if advanced_scope == 'global' and len(advanced) > 2:
        errors.append('more than two Advanced equipped globally')
    if advanced_scope == 'per-tree' and any(n > 2 for n in Counter(card['tree'] for card in advanced).values()):
        errors.append('more than two Advanced equipped in one tree')
    return errors


def mutation_prerequisites_met(node, classes, equipped, profiles, advanced_scope):
    warrior_level = classes.get('Warrior', 0)
    if loadout_errors(warrior_level, equipped, profiles, advanced_scope):
        return False
    chosen = [profiles[identity] for identity in equipped]

    def resolve(part):
        kind = part['kind']
        if kind == 'classLevel':
            return classes.get(part['className'], 0) >= part['minimum']
        if kind == 'equippedMutation':
            return any(card['name'] == part['name'] for card in chosen)
        if kind == 'distinctEquippedMutations':
            category = part['category']
            return sum(card['tier'] == category if category == 'Apex'
                       else card['tree'] == category for card in chosen) >= part['minimum']
        if kind == 'all':
            return bool(part['requirements']) and all(resolve(child) for child in part['requirements'])
        if kind == 'any':
            return bool(part['requirements']) and any(resolve(child) for child in part['requirements'])
        raise ValueError('Not a mutation-feat acquisition atom')

    return resolve(node)


def mutation_component_ready(feat_id, equipped, active, profiles):
    """Only the ongoing mutation component, after lawful activation is proved.

    Does not establish action, target, attack/save, hostile cause, healing,
    finite-use, timing, survival or damage predicates for an actual feat event.
    """
    if len(active) != len(set(active)) or not set(active) <= set(equipped):
        raise ValueError('Active mutations must be distinct equipped profiles')
    cards = [profiles[identity] for identity in active]
    names = {card['name'] for card in cards}
    exact = {
        'backlashEngine': 'Adrenal Backlash Core',
        'hypermutationSpike': 'Butcherform Chassis',
        'juggernautCore': 'Ossified Core',
        'terrorEngine': 'Carrion Signal Gland',
    }
    if feat_id in exact:
        return exact[feat_id] in names
    if feat_id == 'bioStabilizer':
        return 'Bloodthick Node' in names and len(cards) >= 2
    if feat_id in {'bornToHorrify', 'evolutionUnderFire'}:
        return any(card['tier'] == 'Apex' for card in cards)
    if feat_id == 'distortedDominance':
        return any(card['tree'] == 'Aberrant' for card in cards)
    if feat_id == 'evisceratorProtocol':
        return {'Echo Knuckles', 'Warpgrip Talons'} <= names
    if feat_id == 'killChainAdaptation':
        return sum(card['tree'] == 'Combat' for card in cards) >= 2
    if feat_id == 'livingFortress':
        return sum(card['tree'] == 'Vital' for card in cards) >= 3
    if feat_id == 'synapticRot':
        return bool({'Wailing Eye Cluster', 'Viral Core Sacs'} & names)
    raise ValueError('Unknown shared Warrior feat identity')


@dataclass
class BasicMutationActivation:
    """Finite Basic-mutation sequence for an able-to-act synthetic Warrior.

    Starts immediately after a supplied qualifying long rest with Stonecore
    doses. The witness must not own Mutation Adaptation; other activation
    routes, serum effects, damage, restrictions on acting and encounters are
    outside this deliberately small projection.
    """
    level: int
    equipped: list
    profiles: dict
    owned_cards: set
    advanced_scope: str
    turn: int = 1
    strain: int = 0
    active_until: dict = field(default_factory=dict)
    spent_bonus_turns: set = field(default_factory=set)
    apex_used_this_encounter: bool = False
    apex_until: int | None = None
    doses: list = field(init=False)

    def __post_init__(self):
        if loadout_errors(self.level, self.equipped, self.profiles, self.advanced_scope):
            raise ValueError('Illegal mutation equipment')
        if 'warrior.base.mutation-adaptation' in self.owned_cards:
            raise ValueError('This witness does not model modified Strain generation')
        self.doses = ['warrior.supplement.stonecore'] * (4 if self.level >= 20 else 3 if self.level >= 11 else 2)

    @property
    def ordinary_limit(self):
        return 2 if 'warrior.arch.mutation-efficiency' in self.owned_cards else 1

    @property
    def active(self):
        if self.apex_until is not None and self.turn < self.apex_until:
            return list(self.equipped)
        return list(self.active_until)

    def inject_basic(self, mutation_id, end_active=None):
        if 'warrior.base.serum-injection' not in self.owned_cards:
            raise ValueError('Serum Injection was not acquired')
        if mutation_id not in self.equipped or self.profiles[mutation_id]['tier'] != 'Basic':
            raise ValueError('Only equipped Basic mutation injections are in this projection')
        if not self.doses or self.strain >= 3 or self.turn in self.spent_bonus_turns:
            raise ValueError('Dose, Strain or actual Bonus Action unavailable')
        if self.apex_until is not None and self.turn < self.apex_until:
            raise ValueError('Concurrent Apex/serum duration arbitration is outside this projection')
        prospective = dict(self.active_until)
        prospective[mutation_id] = self.turn+3
        if len(prospective) > self.ordinary_limit:
            if end_active not in self.active_until or end_active == mutation_id:
                raise ValueError('Must choose an existing active mutation to end')
            del prospective[end_active]
        self.active_until = prospective
        self.doses.pop()
        self.strain += 1
        self.spent_bonus_turns.add(self.turn)

    def activate_apex_form(self):
        if self.level < 20 or 'warrior.supplement.apex-form' not in self.owned_cards:
            raise ValueError('Actual Warrior20 automatic Apex Form required')
        if self.apex_used_this_encounter or self.turn in self.spent_bonus_turns:
            raise ValueError('Apex Form use or Bonus Action unavailable')
        if self.active_until:
            raise ValueError('This finite witness starts Apex Form with dormant mutations')
        self.apex_until = self.turn+3
        self.apex_used_this_encounter = True
        self.spent_bonus_turns.add(self.turn)

    def next_regular_turn(self):
        self.turn += 1
        self.active_until = {identity: expiry for identity, expiry in self.active_until.items()
                             if expiry > self.turn}
        if self.apex_until is not None and self.turn >= self.apex_until:
            self.apex_until = None
