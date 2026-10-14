"""FW06 finite paid initialization and capacity projection, not general feat use.

Environment and later event probes are expressly conditional. They do not
authenticate campaign events or implement combat, crafting, courses or rests.
"""
from copy import deepcopy
from feat_exact_01_remaining_owned_chains import RemainingOwnedChains
from feat_exact_01_acquisition_models import pb
from feat_exact_01_trade_selections import TradeSelections

IDS = frozenset({'runic_shield','spell_reservoir','mental_buffer','ritual_channeler',
    'quick_learner','core_infusion','master_smithing','dark_binding','temporal_theory',
    'arcane_momentum','lightning_affinity','curse_channeling','combat_reflexes',
    'frenzied_rage','energy_sink','endurance','spellweave','leadership','familiar_bond','empowered_summoning'})


def initial_state(sid, level):
    """Exact source initial fields; an allowance is not its eventual effect."""
    states = {
        'runic_shield': {'armed':True,'ward':None},
        'spell_reservoir': {'uses':{'maximum':1,'current':1,'recovery':'beneficial-owner-LR'},'claimedRestEvents':[]},
        'mental_buffer': {'uses':{'maximum':1,'current':1,'recovery':'beneficial-owner-LR'},'suppressedApplications':[]},
        'ritual_channeler': {'permissionOnly':True},
        'quick_learner': {'languageCategoryUsed':False,'toolCategoryUsed':False,'projects':[]},
        'core_infusion': {'rerollUses':{'maximum':1,'current':1,'recovery':'beneficial-owner-SR-or-LR'},'activeInfusion':None},
        'master_smithing': {'lastSuccessfulTemperCompletion':None,'ownedOutputProperties':{},'storedSpells':[]},
        'dark_binding': {'boundWeapon':None,'bindingRitualCompleted':False},
        'temporal_theory': {'tokenCapacity':2,'tokens':[],'activeEncounter':None,'spentTokenCount':0,'deferredFatigue':False},
        'arcane_momentum': {'maximum':3,'current':0,'qualifiedAttackIds':[],'activeEncounter':None,'declaredEnhancement':None},
        'lightning_affinity': {'stormChargeCapacity':2,'stormCharges':[],'primedRider':None},
        'curse_channeling': {'markCapacity':2 if level>=10 else 1,'marks':[],'dropEntitlementHistory':[]},
        'combat_reflexes': {'extraReactionAvailable':False,'extraReactionEpoch':None,'spentTriggerIds':[]},
        'frenzied_rage': {'rageInstances':{}},
        'energy_sink': {'uses':{'maximum':pb(level),'current':pb(level),'recovery':'beneficial-owner-LR'},'claimedCastRoots':[]},
        'endurance': {'foodWaterPending':0,'sleepPending':0},
        'spellweave': {'heldCapacity':1,'heldBuff':None},
        'leadership': {'designationCapacity':pb(level),'designatedContracts':[]},
        'familiar_bond': {'maximumHpContribution':level,'bodyCreated':False},
        'empowered_summoning': {'creationLineages':{},'bodyCreated':False},
    }
    if sid not in states: raise ValueError('Outside the20 exact FW06 identities')
    return deepcopy(states[sid])


class DeferredAcquisitionStates(RemainingOwnedChains):
    def __init__(self,*args):
        super().__init__(*args)
        self.training_imports = []
        self.environment = {'mode':'conditional-fixture-only','normalHP':7,'maximumHP':31,
            'currentRP':0,'maximumRP':0,'strain':2,'restDebt':{'openedAtWatch':3,'deadlineWatch':5},
            'assessedEvents':['conditional-old-shortage'],'ordinaryReactionAvailable':False,
            'activeConditions':['conditional-preexisting-control'],'inventory':[],
            'followers':[],'summons':[],'familiar':None,'courseCredit':0,
            'previousEncounters':['conditional-old-encounter']}
        self.event_history = []

    def acquire_artisan_training(self, level, trade_reference):
        trade = TradeSelections(self.actor,self.classes,self.equipment,self.skills,self.ancestry,
            self.backgrounds,self.contracts,trade_reference)
        trade.pay = self.pay  # Same actual payments; no fabricated prior entitlement.
        trade.tools.update(self.training_projection['tools'])
        event = trade.acquire('artisan',level,'tools.smith-s-tools')
        self.training_imports.append(deepcopy(event))
        self.training_projection['tools'].add(event['toolCredential'])
        return event

    def _project_existing_familiar(self):
        body = self.environment['familiar']
        if body is None or body.get('spellId') != 'find-familiar':return
        level = sum(self.pay.current_classes.values())
        body.setdefault('featMaximumContributions',{})['familiar_bond'] = level
        body['maximumHP'] = body['nativeMaximumHP']+sum(body['featMaximumContributions'].values())
        body['currentHP'] = min(body['currentHP'],body['maximumHP'])

    def advance(self,level):
        super().advance(level)
        for event in getattr(self,'training_imports',[]):
            self.training_projection['tools'].add(event['toolCredential'])
        total = sum(self.pay.current_classes.values())
        if 'energy_sink' in self.initializations:
            uses = self.initializations['energy_sink']['uses']
            uses['maximum'] = pb(total);uses['current'] = min(uses['current'],uses['maximum'])
        if 'leadership' in self.initializations:self.initializations['leadership']['designationCapacity'] = pb(total)
        if 'familiar_bond' in self.initializations:
            self.initializations['familiar_bond']['maximumHpContribution'] = total
            self._project_existing_familiar()

    def acquire_deferred(self,sid,level,choice=None):
        if sid not in IDS:raise ValueError('Outside the20 FW06 acquisition identities')
        if choice is not None:raise ValueError('This identity has no permanent purchase menu; later choices require their actual events')
        # Actual retained feat alternatives short-circuit before conditional external branches.
        qualified = self.prerequisite(sid)
        state = initial_state(sid,sum(self.pay.current_classes.values()))
        grant = self.pay.commit(sid,self.first+':'+str(level),prerequisites_met=qualified)
        self.initializations[sid] = state
        if sid == 'familiar_bond':self._project_existing_familiar()
        return grant

    def conditional_next_encounter(self,identity,living=True):
        """Only Runic Shield activation shape; all encounter legality is a premise."""
        if identity in self.environment['previousEncounters']:
            return False
        self.environment['previousEncounters'].append(identity)
        state = self.initializations.get('runic_shield')
        if not state or not state['armed'] or not living:return False
        state['ward'] = {'points':15,'encounter':identity};state['armed'] = False
        self.event_history.append({'kind':'conditional-runic-first-encounter','id':identity})
        return True

    def conditional_runic_rest(self,identity,beneficial):
        """Rest receipt supplied, not a simulation of rest qualification/recovery."""
        if not beneficial or any(x.get('kind')=='conditional-runic-rest' and x['id']==identity for x in self.event_history):return False
        state = self.initializations.get('runic_shield')
        if state is None:return False
        state.update(ward=None,armed=True)
        self.event_history.append({'kind':'conditional-runic-rest','id':identity})
        return True

    def conditional_familiar_arrival(self,body,genuinely_new_creation):
        """Actual identity/new-vs-return distinction is an explicit test premise."""
        self.environment['familiar'] = deepcopy(body)
        if not self.pay.has('familiar_bond'):return
        self._project_existing_familiar()
        if genuinely_new_creation and body.get('spellId')=='find-familiar':
            self.environment['familiar']['currentHP'] = self.environment['familiar']['maximumHP']

    def snapshot(self):
        return {**super().snapshot(),'paidTrainingImports':deepcopy(self.training_imports),
                'conditionalEnvironment':deepcopy(self.environment),'conditionalEventHistory':deepcopy(self.event_history)}
