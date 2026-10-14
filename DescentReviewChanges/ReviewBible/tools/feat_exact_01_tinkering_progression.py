"""Trade-XP replay over conditional, source-bound completed work orders.

The order's independent crafting legality is an explicit premise. This model
checks the supplied work/roll/material slice and XP accounting; it is not a
complete fabrication, product-body or campaign authentication engine.
"""
from copy import deepcopy
from feat_exact_01_training_prerequisite_model import proficiency_bonus
from validate_advanced_craft_worked_cases import creation_band


class TinkeringProgression:
    def __init__(self, actor_id, training, character_level, recipe_card, batch_capacity):
        if 'tools.tinker-s-tools' not in training['tools']:
            raise ValueError('Actual Tinkering primary-tool proficiency is required; kit ownership is insufficient')
        if recipe_card['status'] != 'reviewed-authored-operational-playtest':
            raise ValueError('A reviewed recipe card is required')
        if recipe_card['recipeId'] != 'recipe-591' or recipe_card['sourceRecipe']['skill'] != 'Tinkering':
            raise ValueError('This finite replay uses actual Field Stone Tool receipts only')
        if type(batch_capacity) is not int or batch_capacity < 1:
            raise ValueError('Positive source inventory capacity required')
        self.actor_id = actor_id; self.training = deepcopy(training); self.character_level = character_level
        self.card = deepcopy(recipe_card); self.level = 1; self.xp = 0; self.total_earned = 0
        self.completed_orders = {}; self.first_success_ids = set(); self.last_end = 0
        self.components = deepcopy(recipe_card['sourceRecipe']['components'])
        self.stock = {str(i): c['quantity'] * batch_capacity for i, c in enumerate(self.components)}
        self.advancements = []; self.traces = []

    def snapshot(self):
        return deepcopy(self.__dict__)

    def complete(self, order):
        if order['id'] in self.completed_orders:
            raise ValueError('A completion receipt cannot award trade XP twice')
        if order['actorId'] != self.actor_id or order['role'] != 'lead':
            raise ValueError('Only this trained lead receives this completion award')
        if order['recipeId'] != self.card['recipeId']:
            raise ValueError('Recipe identity differs from the bound whole card')
        work = self.card['operational']['work']; recipe = self.card['sourceRecipe']
        if order['station'] != recipe['workRequirements']['station'] or not set(recipe['workRequirements']['requiredTools']) <= set(order['physicalTools']):
            raise ValueError('Physical tools and the actual station are independent requirements')
        if order['startMinute'] < self.last_end or order['endMinute'] - order['startMinute'] != work['activeMinutes']:
            raise ValueError('A complete nonoverlapping source work interval is required')
        if not 1 <= recipe['skillLevel'] <= max(4, self.level) or recipe['discovery']['requiresFormula']:
            raise ValueError('This exact basic source recipe must be legally available')
        if order['componentOccurrences'] != self.components:
            raise ValueError('Preserve exact component occurrences; names alone cannot substitute')
        if any(self.stock[str(i)] < c['quantity'] for i, c in enumerate(self.components)):
            raise ValueError('Source ingredient lot exhausted')
        if order['chosenAbility'] != 'INT' or order['toolBonus'] != 0 or order['facilityBonus'] != 0 or order['assistantBonus'] != 0:
            raise ValueError('This finite ordinary workshop witness has no extra bonuses or assistants')
        modifier = (self.training['scores']['INT'] - 10) // 2 + proficiency_bonus(self.character_level)
        band = creation_band(order['naturalD20'], modifier, work['DC'])
        if band != 'Standard':
            raise ValueError('This source-qualified progression replay supplies Standard successful orders')
        before_level, before_xp = self.level, self.xp
        trivial = self.level >= recipe['skillProgression']['trivialAtSkillLevel']
        award = 0 if trivial else 2 if self.card['recipeId'] in self.first_success_ids else 4
        for i, component in enumerate(self.components):
            if component['consumed']:
                self.stock[str(i)] -= component['quantity']
        self.first_success_ids.add(self.card['recipeId']); self.last_end = order['endMinute']
        self.xp += award; self.total_earned += award
        while self.level < 20 and self.xp >= 10 + self.level:
            cost = 10 + self.level; self.xp -= cost
            self.advancements.append({'from': self.level, 'to': self.level + 1, 'spentXP': cost, 'order': order['id']})
            self.level += 1
        trace = {'order': deepcopy(order), 'sourceBand': band, 'modifier': modifier,
                 'beforeLevel': before_level, 'beforeXP': before_xp, 'trivial': trivial,
                 'xpAward': award, 'afterLevel': self.level, 'afterXP': self.xp,
                 'afterStock': deepcopy(self.stock),
                 'scope': 'Conditional legal completed work-order premise; no device activation, body instantiation or campaign authentication.'}
        self.completed_orders[order['id']] = deepcopy(trace); self.traces.append(trace)
        return deepcopy(trace)

    def prerequisite(self, contract):
        node = contract['requirements']
        if node != {'kind': 'trainedTradeLevel', 'trade': 'Tinkering', 'minimum': 5, 'notSkillCheckBonus': True}:
            raise ValueError('The controlling Tinker Adept contract changed')
        return self.level >= 5 and 'tools.tinker-s-tools' in self.training['tools']
