"""Source-bound training choices for Artisan, Craftsman and Versatile Artisan.

This is a finite acquisition projection. Recipe work, quality, time discounts,
formula access and actual inventory are governed by their separate procedures.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_training_prerequisite_model import materialize_training, normalize_name
from feat_exact_01_prodigy_choices import tool_projection


class TradeSelections:
    def __init__(self, actor, classes, equipment, skills, ancestry, backgrounds, contracts, trade_reference):
        if actor['priorFeatChoices']:
            raise ValueError('Record every feat through its actual paid history')
        self.actor = deepcopy(actor); self.contracts = contracts
        self.training = materialize_training(actor, classes, equipment, skills, ancestry, backgrounds)
        self.catalog, self.primary = tool_projection(equipment, trade_reference)
        self.by_trade = {trade: sid for sid, trade in self.primary.items()}
        self.artisan = {sid for sid, row in self.catalog.items() if row.get('group') == "Artisan's Tools"}
        for line in trade_reference.split('Existing equipment supplies', 1)[0].splitlines():
            if line.startswith('| ') and not line.startswith('| Trade |'):
                trade, ability, tool, artisan, injury = [s.strip() for s in line.strip('|').split('|')]
                if artisan == 'Yes':
                    sid = self.by_trade[trade]
                    if normalize_name(self.catalog[sid]['name']) != normalize_name(tool):
                        raise ValueError('Exact primary tool row mismatch')
                    self.artisan.add(sid)
        self.tools = set(self.training['tools'])
        self.trades = {self.primary[s]: {'level': 1, 'xp': 0} for s in self.tools if s in self.primary}
        self.pay = PaidChoices({name: row['asiClassLevels'] for name, row in classes.items()}, {},
                              deepcopy(actor['classLevels']), deepcopy(self.training['scores']), set(contracts))
        self.events = []

    def advance(self, level):
        first = self.actor['firstClass']
        if type(level) is not int or not self.pay.current_classes[first] <= level <= 20:
            raise ValueError('Invalid forward class level')
        self.actor['classLevels'][first] = level; self.pay.current_classes[first] = level

    def earn(self, level):
        first = self.actor['firstClass']; self.pay.earn_class_opportunity(first + ':' + str(level), first, level)

    def acquire(self, sid, level, selection):
        if sid not in {'artisan', 'craftsman', 'versatile_artisan'}:
            raise ValueError('Outside the three exact tool-choice procedures')
        if sid == 'versatile_artisan':
            if self.contracts[sid]['requirements'] != {'kind': 'actualProficiency', 'credential': 'at least one actual tool'}:
                raise ValueError('Controlling tool prerequisite changed')
            eligible = {trade: tool for trade, tool in self.by_trade.items() if tool not in self.tools}
            qualified = bool(self.tools)
        else:
            if self.contracts[sid]['requirements'] != {'kind': 'permanentAbility', 'ability': 'INT', 'minimum': 13}:
                raise ValueError('Controlling permanent INT prerequisite changed')
            eligible = {s: s for s in self.artisan - self.tools}
            qualified = self.pay.scores['INT'] >= 13
        if eligible:
            if selection not in eligible:
                raise ValueError('Choose one genuinely unowned credential from this exact feat menu')
            tool = eligible[selection]
        else:
            if selection is not None:
                raise ValueError('The actual menu is exhausted; no substitute or future choice credit')
            tool = None
        tools = set(self.tools); trades = deepcopy(self.trades)
        if tool is not None:
            tools.add(tool)
            if tool in self.primary:
                trades.setdefault(self.primary[tool], {'level': 1, 'xp': 0})
        grant = self.pay.commit(sid, self.actor['firstClass'] + ':' + str(level), choice=selection, prerequisites_met=qualified)
        self.tools = tools; self.trades = trades
        event = {'feat': sid, 'choice': selection, 'toolCredential': tool, 'state': 'resolved' if eligible else 'exhausted',
                 'payment': grant, 'futureChoiceCredit': False, 'physicalEquipmentGranted': [], 'expertiseGranted': [],
                 'recipeOrFormulaGranted': [], 'qualityRolled': False, 'creationWorkExecuted': False}
        self.events.append(event)
        return deepcopy(event)

    def snapshot(self):
        return {'actor': deepcopy(self.actor), 'payment': deepcopy(self.pay.__dict__),
                'tools': sorted(self.tools), 'trades': deepcopy(self.trades), 'events': deepcopy(self.events)}
