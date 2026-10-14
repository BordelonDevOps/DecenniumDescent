"""Permanent feat casting selections and initial grants, not a casting runtime.

Uses complete current source procedures and exact spell placements. Temporary
use impediments do not remove acquired credentials; missing required source
choices still prevent a completed acquisition under ACQ03.
"""
from copy import deepcopy
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains

MENTAL = ('INT', 'WIS', 'CHA')
ELEMENTS = ('acid', 'cold', 'fire', 'lightning', 'thunder')
COHORT = {'arcane_pulse', 'cantrip_mastery', 'elemental_affinity', 'feyTouched', 'shadow_touched',
    'ritual_caster', 'telekinetic', 'telepathic', 'forbidden_pact', 'hemocraft', 'soul_cage'}


class CastingSelections(RemainingOwnedChains):
    def configure_choice_sources(self, core_proposal):
        self.touched_pools = {sid: deepcopy(core_proposal['currentChoicePools'][label]['choices'])
            for sid, label in [('feyTouched', 'Fey Touched'), ('shadow_touched', 'Shadow Touched')]}
        self.misty_step = deepcopy(core_proposal['mistyStepOriginalSupplement'])

    def providers(self):
        return self.actual_casting_routes()

    def touched_route(self, sid, selection):
        if not isinstance(selection, dict) or set(selection) != {'spellId', 'school', 'sourceClass'}:
            raise ValueError('Exact spell, rank1 school and actual source placement required')
        rows = [r for r in self.touched_pools[sid] if r['id'] == selection['spellId'] and r['school'] == selection['school']
            and selection['sourceClass'] in r['sourceRows']]
        if len(rows) != 1 or rows[0]['rank'] != 1 or rows[0]['authoredStatus'] != 'reviewed-authored-operational-playtest':
            raise ValueError('Not an available exact reviewed rank1 placement in this feat pool')
        row = rows[0]; route = self.sources.ordinary(selection['spellId'], selection['sourceClass'])
        if route['rank'] != 1 or route.get('school') != selection['school'] or route['placement'] != row['sourceRows'][selection['sourceClass']]:
            raise ValueError('Source row and current whole-payload placement differ')
        return route

    def acquire_casting_selection(self, sid, level, choice):
        if sid not in COHORT or not isinstance(choice, dict):
            raise ValueError('Named feat and exact acquisition fields required')
        if not self.prerequisite(sid):
            raise ValueError('Printed current acquisition predicate not established')
        additions = {}; routes = []; charges = {}
        ability_feats = {'arcane_pulse', 'feyTouched', 'shadow_touched', 'ritual_caster', 'telekinetic', 'telepathic', 'hemocraft'}
        if sid in ability_feats:
            allowed = ('INT', 'WIS') if sid == 'ritual_caster' else ('INT', 'CHA') if sid == 'hemocraft' else MENTAL
            expected = {'ability', 'rank1'} if sid in {'feyTouched', 'shadow_touched'} else {'ability'}
            if set(choice) != expected or choice.get('ability') not in allowed:
                raise ValueError('Exactly the source-permitted permanent ability and choices required')
            ability = choice['ability']
            if sid == 'ritual_caster' and self.pay.scores[ability] < 13:
                raise ValueError('Ritual Caster specifically chooses a qualifying INT/WIS ability')
            additions[sid] = {'fixedAbility': ability}
            if sid in {'feyTouched', 'shadow_touched'}:
                selected = self.touched_route(sid, choice['rank1'])
                if sid == 'feyTouched':
                    primary = {'spellId': self.misty_step['id'], 'rank': 2, 'school': 'Conjuration',
                        'sourceClass': None, 'supplement': 'MF-13 explicit feat route to preserved Misty Step profile',
                        'completeProfile': deepcopy(self.misty_step)}
                else:
                    primary = self.sources.ordinary('invisibility', 'Wizard')
                    if (primary['rank'], primary['school']) != (2, 'Illusion'):
                        raise ValueError('Actual Invisibility rank2 Illusion required')
                routes = [{**r, 'ability': ability, 'entitlement': 'feat-charge-only'} for r in [primary, selected]]
                charges = {r['spellId']: {'maximum': 1, 'current': 1, 'recovery': 'beneficial-owner-LR'} for r in routes}
                additions[sid]['rank1Selection'] = deepcopy(choice['rank1'])
            elif sid == 'telekinetic':
                route = self.sources.ordinary('mage-hand', 'Wizard')
                if route['rank'] != 0 or route.get('school') != 'Universal':
                    raise ValueError('Exact ordinary Universal Mage Hand, not Magehand, required')
                routes = [{**route, 'ability': ability, 'entitlement': 'feat-cantrip', 'waivedComponents': ['V', 'S']}]
            elif sid == 'telepathic':
                supplemental = self.supplements['SUP-05']['newDetectThoughts']
                if supplemental['completeProcedureInFeat'] != sid or supplemental['ordinaryClassAccess']:
                    raise ValueError('Complete authored feat-only Detect Thoughts source required')
                routes = [{'spellId': supplemental['id'], 'rank': supplemental['rank'], 'school': supplemental['school'],
                    'sourceClass': None, 'supplement': 'SUP-05/newDetectThoughts', 'ability': ability,
                    'completeControllingProcedure': self.contracts[sid]['completeOperativeProcedure'], 'entitlement': 'feat-charge-only'}]
                charges = {supplemental['id']: {'maximum': 1, 'current': 1, 'recovery': 'beneficial-owner-LR'}}
                additions[sid]['activeCommunicationChannel'] = None
            elif sid == 'hemocraft':
                additions[sid].update(bleedRecords=[], recoveryReserve={'current': 0, 'lastBeneficialRestSnapshot': None})
            elif sid == 'ritual_caster':
                additions[sid].update(learnedRituals=[], actualBookRef=None)
        elif sid == 'elemental_affinity':
            if set(choice) != {'damageType'} or choice['damageType'] not in ELEMENTS:
                raise ValueError('One of five permanent printed elements required')
            additions[sid] = {'chosenDamageType': choice['damageType']}
        elif sid == 'cantrip_mastery':
            if set(choice) != {'spellId'}:
                raise ValueError('One exact already-known rank0 identity required')
            modes = [r for r in self.casting.qualifying() if r['spellId'] == choice['spellId'] and r['rank'] == 0]
            if not modes:
                raise ValueError('No actually retained known rank0 mode for that exact identity')
            additions[sid] = {'fixedSpellId': choice['spellId'], 'rank': 0, 'acquisitionModes': modes,
                'newSpellGrant': False}
        elif sid == 'forbidden_pact':
            sigils = {r['id']: r for r in self.supplements['SUP-07']['pactSigils']}
            sigil = choice.get('sigil')
            expected = {'sigil', 'damageType'} if sigil == 'energyResistance' else {'sigil'}
            if sigil not in sigils or set(choice) != expected:
                raise ValueError('One actual permanent sigil and all required nested choices')
            if sigil == 'energyResistance' and choice['damageType'] not in ELEMENTS:
                raise ValueError('Energy Resistance needs one of the five actual damage types')
            additions[sid] = {'sigil': sigil, 'spentSubstitutionEncounterIds': []}
            if sigil == 'energyResistance': additions[sid]['chosenDamageResistance'] = choice['damageType']
            else: additions[sid]['sigilAllowance'] = {'maximum': 1, 'current': 1, 'recovery': 'beneficial-owner-SR-or-LR'}
            routes = [{**self.sources.blast(), 'ability': 'CHA', 'entitlement': 'feat-cantrip'}]
        elif sid == 'soul_cage':
            if set(choice) != {'provider'} or choice['provider'] not in self.providers():
                raise ValueError('Mandatory retained actual casting provider cannot be invented from Lifeleech ownership')
            additions[sid] = {'fixedProvider': deepcopy(choice['provider']), 'actualBlackCrystalRef': None}
            prior = self.initializations.get('sharedSoulCharges')
            if prior is None:
                additions['sharedSoulCharges'] = {'maximum': 3, 'current': 0, 'evaluatedDeathEvents': [], 'bodyEpochEntitlements': []}
            elif prior.get('maximum') != 3 or not 0 <= prior.get('current', -1) <= 3:
                raise ValueError('Existing shared charge state must be valid; no acquisition refill')
        else:
            raise ValueError('Unhandled acquisition')
        # Validate everything before committing the one real earned opportunity.
        grant = self.pay.commit(sid, self.first + ':' + str(level), choice=choice, prerequisites_met=True)
        self.initializations.update(deepcopy(additions))
        if routes:
            gid = sid + '/' + grant['opportunity']
            self.casting.grants[gid] = {'source': 'actual-paid-feat-complete-controlling-procedure',
                'acquiredAt': self.casting.moment, 'payment': deepcopy(grant)}
            self.casting.routes.extend({**deepcopy(r), 'grantId': gid, 'kind': 'personal-feat'} for r in routes)
            if charges:
                self.casting.use_state['renewableCharges'][gid] = deepcopy(charges)
        return grant
