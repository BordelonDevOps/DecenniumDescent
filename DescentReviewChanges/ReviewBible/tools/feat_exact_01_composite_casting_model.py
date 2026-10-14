"""Finite combined feat prerequisites, grounded in explicit paid source slices.

This is neither a complete character builder nor a casting/use engine. The
Wizard slice intentionally has no training projection: training predicates on
that slice raise, rather than treating omitted class grants as absent.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices
from feat_exact_01_initiate_acquisition_model import InitiateAcquisitions
from feat_exact_01_training_prerequisite_model import materialize_training, meets_training_prerequisite
from feat_exact_01_casting_credential_model import CastingCredentials


class CompositeCastingHistory:
    def __init__(self, actor, classes, equipment, skills, ancestry, backgrounds, contracts, supplements, sources):
        self.actor = deepcopy(actor)
        self.classes = classes; self.equipment = equipment; self.skills = skills
        self.ancestry = ancestry; self.backgrounds = backgrounds; self.contracts = contracts
        self.supplements = supplements; self.sources = sources
        self.first = actor['firstClass']; self.initializations = {}
        if actor['priorFeatChoices'] or set(actor['classLevels']) != {self.first}:
            raise ValueError('Supply one actual first class and earn all feat history here')
        if self.first == 'Wizard':
            if actor['ancestry'] != 'human' or actor['variant'] != 'imperial-human':
                raise ValueError('Wizard ability witness uses the actual Human/Imperial source')
            h = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
            variant = next(x for x in h['variants'] if x['id'] == 'imperial-human')
            rolls = actor['abilityRolls']
            if set(rolls) != {'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'}:
                raise ValueError('Six actual ability-roll premises required')
            if any(len(d) != 4 or any(type(n) is not int or not 1 <= n <= 6 for n in d) for d in rolls.values()):
                raise ValueError('Invalid four-d6/drop-lowest premise')
            scores = {a: sum(d) - min(d) + variant['combinedAbilityBonuses'][a] for a, d in rolls.items()}
            if scores != actor['permanentScores']:
                raise ValueError('Ability snapshot differs from rolls and ancestry')
            if type(actor['classLevels']['Wizard']) is not int or not 1 <= actor['classLevels']['Wizard'] <= 20:
                raise ValueError('Invalid attained Wizard level')
            self.training_projection = None
        else:
            self.training_projection = materialize_training(actor, classes, equipment, skills, ancestry, backgrounds)
            scores = self.training_projection['scores']
        self.pay = PaidChoices({n: c['asiClassLevels'] for n, c in classes.items()}, {},
                               deepcopy(actor['classLevels']), deepcopy(scores), set(contracts) | {'proposal_spell_focus'})
        self.casting = CastingCredentials(sources, sum(actor['classLevels'].values()))

    def snapshot(self):
        return {'actor': deepcopy(self.actor), 'payment': deepcopy(self.pay.__dict__),
                'training': deepcopy(self.training_projection), 'casting': self.casting.snapshot(),
                'initializations': deepcopy(self.initializations)}

    def advance(self, level):
        if type(level) is not int or not self.actor['classLevels'][self.first] <= level <= 20:
            raise ValueError('Attained class levels must move forward')
        self.actor['classLevels'] = {self.first: level}; self.pay.current_classes = {self.first: level}
        self.casting.moment = level
        if self.training_projection is not None:
            self.training_projection = materialize_training(self.actor, self.classes, self.equipment, self.skills, self.ancestry, self.backgrounds)

    def earn(self, level):
        self.pay.earn_class_opportunity(self.first + ':' + str(level), self.first, level)

    def prerequisite(self, sid):
        def resolve(node):
            kind = node['kind']
            if kind == 'all':
                return bool(node['requirements']) and all(resolve(c) for c in node['requirements'])
            if kind == 'any':
                return bool(node['requirements']) and any(resolve(c) for c in node['requirements'])
            if kind in {'actualSpellcastingRoute', 'actualCastAccess'}:
                return self.casting.matches(node)
            if kind == 'ownedFeat':
                return self.pay.has(node['id'])
            if kind == 'ownedSupplementFeat':
                if node['source'] != 'SUP-05/newSpellFocus' or node['name'] != 'Spell Focus':
                    raise ValueError('Unmodeled supplemental ownership source')
                return self.pay.has(self.sources.focus['id'])
            if kind == 'totalCharacterLevel':
                return sum(self.pay.current_classes.values()) >= node['minimum']
            if kind == 'permanentAbility':
                return self.pay.scores[node['ability']] >= node['minimum']
            if kind == 'noPrintedPrerequisite':
                return True
            if kind == 'actualProficiency' and node['credential'] == 'actual legacy Spellcraft; not Arcana alias':
                # These current-source actors supply no actual legacy Spellcraft history.
                return False
            if self.training_projection is None:
                raise ValueError('Wizard training is outside this repertoire/ability slice')
            return meets_training_prerequisite(node, self.actor, self.training_projection, self.equipment, self.skills)
        return resolve(self.contracts[sid]['requirements'])

    def gate(self, sid, opportunity):
        op = self.pay.opportunities.get(opportunity)
        return bool(self.prerequisite(sid) and op is not None and not op['spent'])

    def initiate(self):
        if self.first != 'Warrior' or self.pay.grants:
            raise ValueError('This finite Initiate import starts with an unpaid Warrior slice')
        level = self.actor['classLevels']['Warrior']
        original = self.pay.opportunities.get('Warrior:' + str(level))
        if original is None or original['spent']:
            raise ValueError('Earn the actual Initiate opportunity first')
        paid = InitiateAcquisitions(self.actor, self.classes, self.equipment, self.skills, self.ancestry,
                                   self.backgrounds, self.contracts, self.supplements['SUP-04'], self.sources.dependencies)
        paid.earn(level)
        paid.acquire('magicInitiate', level, {'curriculum': 'Wizard', 'cantrips': ['friends', 'arcane-ray'], 'rank1': 'find-familiar'})
        self.casting.import_initiate(paid, level)
        self.pay = paid.pay
        self.pay.valid_feat_ids.add(self.sources.focus['id'])

    def wizard(self, known, book, prepared):
        if self.first != 'Wizard':
            raise ValueError('A real supplied Wizard class level is required')
        self.casting.wizard_snapshot(self.actor['classLevels']['Wizard'], known, book, prepared,
                                     self.casting.moment, self.pay.scores['INT'])

    def acquire_parent(self, sid, level, choice=None):
        if sid not in {'power_attack', 'combatCasting', 'lifeleech', 'forbidden_pact', 'evocation_focus', 'skill_expert'}:
            raise ValueError('Outside the explicitly supplied parent/alternative acquisition cohort')
        qualified = self.prerequisite(sid)
        next_actor = deepcopy(self.actor); next_training = self.training_projection
        if sid == 'skill_expert':
            if not isinstance(choice, dict) or set(choice) != {'newSkill', 'expertiseSkill'}:
                raise ValueError('Actual ordered skill and Expertise choices required')
            next_actor['priorFeatChoices'].append({'featId': sid, **choice})
            next_training = materialize_training(next_actor, self.classes, self.equipment, self.skills, self.ancestry, self.backgrounds)
        elif sid == 'forbidden_pact':
            if choice != {'sigil': 'hex'} or 'hex' not in {s['id'] for s in self.supplements['SUP-07']['pactSigils']}:
                raise ValueError('This finite source witness uses the actual permanently selected Hex sigil')
        elif choice is not None:
            raise ValueError('This parent has no permanent acquisition menu in this projection')
        record = self.pay.commit(sid, self.first + ':' + str(level), choice=choice, prerequisites_met=qualified)
        self.actor = next_actor; self.training_projection = next_training
        if sid == 'forbidden_pact':
            self.casting.import_forbidden_pact(self.pay, self.casting.moment, 'hex')
        if sid == 'lifeleech':
            self.initializations[sid] = {'recoveryReserveCurrent': 0, 'noLongRestSimulated': True,
                                        'scope': 'Acquisition initializes zero reserve; rest capacity/use and death collection are not executed.'}
        return record

    def spell_focus(self, level, school):
        return self.casting.acquire_spell_focus(self.pay, self.first + ':' + str(level), school)

    def remove_personal_routes(self):
        # Explicit conditional lawful-removal premise, not an invented retraining mechanic.
        for grant in self.casting.grants.values():
            grant['removedAt'] = self.casting.moment
