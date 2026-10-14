"""Three acquired SUP-07 sigils in a conditional straight-line test world.

This executes sigil allowances, movement, mark use and passive packet defense.
It does not execute Forbidden Pact's HP substitution, Eldritch Blast, generic
spellcasting, full damage-to-life resolution, rest eligibility or setting lore.
"""
from copy import deepcopy
from core_playtest_rules import attack_roll
from feat_exact_01_acquisition_models import pb
from feat335_copy_source_components import integer, dice


class PactSigils:
    def __init__(self, acquired, world):
        if not acquired.pay.has('forbidden_pact'):
            raise ValueError('Actual paid Forbidden Pact required')
        self.acquired = acquired
        self.state = acquired.initializations['forbidden_pact']
        paid = next(x for x in acquired.pay.grants if x['identity'] == 'forbidden_pact')
        if paid['choice']['sigil'] != self.state['sigil']:
            raise ValueError('Retained permanent sigil must match the payment record')
        if self.state['sigil'] == 'energyResistance' and paid['choice']['damageType'] != self.state['chosenDamageResistance']:
            raise ValueError('Permanent resistance type must match the payment record')
        self.world = deepcopy(world); self.events = {}; self.rests = set()
        self.turn = None; self.regular_ordinal = 0; self.turn_ids = set()
        self.actions = 0; self.bonus_actions = 0; self.mark = None
        expected = {'shadowstep', 'hex', 'energyResistance'}
        if self.state['sigil'] not in expected: raise ValueError('No invented sigil')
        self.sigil_source = deepcopy(next(x for x in acquired.supplements['SUP-07']['pactSigils'] if x['id'] == self.state['sigil']))

    def snapshot(self):
        return {'acquisition': self.acquired.snapshot(), 'world': deepcopy(self.world),
                'events': deepcopy(self.events), 'rests': sorted(self.rests),
                'turn': deepcopy(self.turn), 'regularOrdinal': self.regular_ordinal,
                'turnIds': sorted(self.turn_ids), 'actions': self.actions,
                'bonusActions': self.bonus_actions, 'mark': deepcopy(self.mark)}

    def operative(self):
        return self.acquired.pay.has('forbidden_pact') and 'forbidden_pact' not in self.acquired.pay.suppressed

    def start(self, turn, *, regular, actual_turn_grant):
        if actual_turn_grant is not True or type(regular) is not bool or not turn or turn in self.turn_ids or self.turn is not None:
            raise ValueError('One actual new owned turn required')
        self.turn_ids.add(turn); self.turn = {'id': turn, 'regular': regular}
        self.actions = 1; self.bonus_actions = 1
        if regular:
            self.regular_ordinal += 1
            if self.mark and self.regular_ordinal >= self.mark['expiresAtRegularStart']:
                self.mark['active'] = False

    def end(self, turn):
        if self.turn is None or self.turn['id'] != turn: raise ValueError('Current owned turn required')
        self.turn = None; self.actions = 0; self.bonus_actions = 0

    def owner(self): return self.world['actors']['owner']

    def line(self, start, end):
        return not any(min(start, end) < wall < max(start, end) for wall in self.world['walls'])

    def gate(self, event, sigil):
        if not event or event in self.events or self.state['sigil'] != sigil or not self.operative():
            raise ValueError('New event from the actual unsuppressed selected sigil required')
        if not self.turn or not self.owner()['canAct'] or self.bonus_actions < 1 or self.state['sigilAllowance']['current'] < 1:
            raise ValueError('Actual action-capable owned turn, Bonus Action and sigil use required')

    def shadowstep(self, event, destination):
        self.gate(event, 'shadowstep')
        integer(destination, 'straight-line destination', -10000, 10000)
        owner = self.owner(); old = owner['position']; offsets = owner['footprintOffsets']
        if not offsets or len(offsets) != len(set(offsets)) or 0 not in offsets:
            raise ValueError('Actual complete fixed body footprint required')
        origin_cells = [old + x for x in offsets]; dest_cells = [destination + x for x in offsets]
        if abs(destination - old) > 15 or not owner['teleportAllowed'] or not self.line(old, destination):
            raise ValueError('Actual teleport distance, permission and line of effect required')
        if not all(self.world['light'].get(x) in {'dim', 'dark'} for x in origin_cells + dest_cells):
            raise ValueError('Whole origin and destination footprints must be dim or dark')
        occupied = {a['position'] + x for who, a in self.world['actors'].items() if who != 'owner' for x in a['footprintOffsets']}
        if not all(x in self.world['visibleCells'] and x in self.world['fittingCells'] and x not in occupied for x in dest_cells):
            raise ValueError('Actual visible fitting unoccupied destination footprint required')
        self.bonus_actions -= 1; self.state['sigilAllowance']['current'] -= 1
        owner['position'] = destination
        self.events[event] = {'sigil': 'shadowstep', 'from': old, 'to': destination,
            'originFootprint': origin_cells, 'destinationFootprint': dest_cells,
            'bonusActionSpent': 1, 'useSpent': 1, 'newFeatGranted': False,
            'scope': 'Legal immediate sigil movement; no generic teleport engine or spell cast.'}
        return deepcopy(self.events[event])

    def hex(self, event, target):
        self.gate(event, 'hex'); victim = self.world['actors'].get(target)
        if not victim or target == 'owner' or not victim['hostile'] or not victim['perceived']:
            raise ValueError('Actual perceived hostile creature required')
        if abs(victim['position'] - self.owner()['position']) > 30 or not self.line(self.owner()['position'], victim['position']):
            raise ValueError('Hex requires actual30ft range and line of effect')
        self.bonus_actions -= 1; self.state['sigilAllowance']['current'] -= 1
        self.mark = {'sourceEvent': event, 'target': target, 'active': True,
                     'expiresAtRegularStart': self.regular_ordinal + 1}
        self.events[event] = {'sigil': 'hex', 'mark': deepcopy(self.mark),
            'bonusActionSpent': 1, 'useSpent': 1, 'curseClassification': False,
            'newCurseChannelingGrant': False}
        return deepcopy(self.events[event])

    def weapon_attack(self, event, target, natural, native_dice, hex_dice):
        if not event or event in self.events or not self.turn or self.actions < 1 or not self.owner()['canAct']:
            raise ValueError('One actual owned ordinary Attack Action required')
        victim = self.world['actors'].get(target); weapon = self.world['weapon']
        profile = self.acquired.equipment.get(weapon['profile'])
        if not victim or not victim['perceived'] or abs(victim['position'] - self.owner()['position']) > 5 or not self.line(self.owner()['position'], victim['position']):
            raise ValueError('Actual perceived reachable weapon recipient required')
        if weapon['heldBy'] != 'owner' or weapon['profile'] != 'martial-melee-weapons.longsword' or weapon['hands'] != 1 or profile['sourceFields']['Damage'] != '1d8 slashing':
            raise ValueError('This finite attack uses an actually held one-handed source longsword')
        trained = weapon['profile'] in self.acquired.training_projection['weapons']
        strength = (self.acquired.pay.scores['STR'] - 10) // 2
        result = attack_roll(natural, strength + (pb(sum(self.acquired.pay.current_classes.values())) if trained else 0), victim['armorClass'])
        eligible_hex = bool(result['hit'] and self.operative() and self.mark and self.mark['active'] and self.mark['target'] == target)
        count = 2 if result['critical'] else 1
        if result['hit']:
            native = max(0, dice(native_dice, count, 8) + strength)
        else:
            if native_dice: raise ValueError('A miss has no native damage dice')
            native = 0
        if eligible_hex:
            addition = dice(hex_dice, count, 4)
        else:
            if hex_dice: raise ValueError('No Hex die without this actual qualifying weapon hit')
            addition = 0
        # The complete roll inputs are validated before changing action/mark state.
        self.actions -= 1
        if eligible_hex: self.mark['active'] = False
        self.events[event] = {'kind': 'actual-personal-direct-weapon-attack', 'target': target,
            'attack': result, 'sourceWeapon': weapon['profile'], 'ActionSpent': 1,
            'nativeSlashing': native, 'nativeNecrotic': addition, 'hexConsumed': eligible_hex,
            'damageAppliedToLife': False, 'newCastOrCurseOrDropReward': False}
        return deepcopy(self.events[event])

    def resist_packet(self, event, damage_type, native_amount, other_resistances=()):
        if self.state['sigil'] != 'energyResistance' or not event or event in self.events:
            raise ValueError('One incoming packet and actual selected resistance sigil required')
        integer(native_amount, 'incoming native component')
        own = self.operative() and damage_type == self.state['chosenDamageResistance']
        resistant = own or damage_type in other_resistances
        amount = native_amount // 2 if resistant else native_amount
        self.events[event] = {'kind': 'conditional-incoming-typed-packet', 'type': damage_type,
            'native': native_amount, 'resistanceAppliedOnce': bool(resistant), 'ownSigilOperative': own,
            'afterResistanceStageOnly': amount, 'damageAppliedToLife': False, 'newImmunity': False,
            'otherDefenseCompositionExecuted': False,
            'absorption': 0, 'chargesCreated': 0}
        return deepcopy(self.events[event])

    def rest(self, event, *, kind, beneficial):
        if not event or kind not in {'SR', 'LR'} or type(beneficial) is not bool:
            raise ValueError('Actual supported rest completion required')
        if not beneficial or event in self.rests: return False
        self.rests.add(event)
        if self.state['sigil'] in {'shadowstep', 'hex'}:
            self.state['sigilAllowance']['current'] = self.state['sigilAllowance']['maximum']
        return True
