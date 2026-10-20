"""Explicit conditional scenarios; never authenticated campaign events."""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import json
from core_playtest_rules import LifeState
from form_temphp_playtest_rules import BufferLedger
from transformation_spell_playtest_rules import ConcentrationLedger
from feat335_copy_capture import CopyAcquisition,CopyCaptures
from feat335_copy_source_components import CopySourceComponents
from feat_exact_01_casting_credential_model import CastingSources
from feat335_copy_payloads import CopyPayloadWorld,CopyPayloadReleases

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'


def read(p):return json.loads(p.read_bytes())


class CopyPayloadFixtures:
    def __init__(self):
        self.paths=[R/'data/playtest/character_foundation.json',R/'data/playtest/ancestry_background_candidate.json',
            R/'data/playtest/equipment_source_catalog.json',R/'data/public/feat_candidates/exact_01/supplements.json',
            R/'data/public/feat_candidates/exact_01/spell_dependencies.json',R/'data/public/class_playtests/wizard.json',
            A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',A/'FEAT_EXACT_01_INITIATE_ACQUISITION_CHECK.json',
            A/'FEAT335_COPY_SOURCE_COMPONENTS_CHECK.json']
        f,ancestry,equipment,sm,deps,wizard,contracts,prior,self.source_report=[read(p) for p in self.paths]
        self.classes={x['class']:x for x in f['classes']};self.skills={s:a for a,ss in f['skillAbilities'].items() for s in ss}
        self.ancestry=ancestry;self.equipment={x['id']:x for x in equipment['records']};self.backgrounds={x['id']:x for x in ancestry['backgrounds']}
        self.contracts={x['id']:x for x in contracts['records']};self.supplements={x['id']:x['value'] for x in sm['groups']}
        self.sources=CastingSources(G,deps['spells'],self.supplements,wizard);self.actor=prior['actorSourceProjection']
        for dep in deps['spells'].values():
            p=G/dep['binding']['file']
            if p not in self.paths:self.paths.append(p)

    def acquisition(self):
        actor=deepcopy(self.actor);actor.update(firstClass='Wizard',classLevels={'Wizard':1},selectedClassSkills=['Insight','Investigation'])
        h=CopyAcquisition(actor,self.classes,self.equipment,self.skills,self.ancestry,self.backgrounds,self.contracts,self.supplements,self.sources)
        h.advance(4);h.wizard(['arcane-ray','friends'],['find-familiar'],['find-familiar'])
        for sid,level in [('eldritch_echo',4),('mimicry',8),('arcane_adaptation',12)]:
            h.advance(level);h.earn(level);h.acquire_copy(sid,level)
        return h

    @staticmethod
    def actor_state(ident):
        return {'id':ident,'life':LifeState(40,30),'creature':True,'living':True,'willing':True,'ordinaryAC':12,
            'speedBeforeControl':30,'coreSpeedZero':False,'ordinaryReactionAllowed':True,'magicAllowed':True,
            'conscious':True,'canAct':True,'verbalAvailable':True,'somaticAvailable':True,
            'position':[0,0,0],'regularStartPhase':Fraction(0),'regularEndPhase':Fraction(1,4),
            'inProgressRegularEnd':None,'incomingAttackRollMode':'normal','dexSaveRollMode':'normal',
            'wisSaveRollMode':'normal','dexSaveModifier':0,'wisSaveModifier':0,
            'damageImmunities':set(),'damageResistances':set(),'flatDamageReduction':0,
            'healingReductions':[],'healingSystemicFactors':[],'hpGainProhibited':False,'copyHindranceImmune':False,
            'unsupportedInterceptors':[]}

    def make(self,owner='owner',world=None,concentration=None):
        h=self.acquisition();witnesses=CopySourceComponents(self.sources)
        for row in self.source_report['histories']:
            if row['id'].startswith('all-seven/'):
                for event,s in row['state'].items():witnesses.witness(event,s['spellId'],s['sourceRoute']['sourceClass'],s['sourceClassLevel'],s['premises'],s['outcome'])
        if world is None:
            actors={n:self.actor_state(n) for n in [owner,'target','target2','target3','target4']}
            world=CopyPayloadWorld(actors,BufferLedger())
        if owner not in world.actors:world.actors[owner]=self.actor_state(owner)
        for target in world.actors:
            world.observations[(owner,target)]={'distanceFeet':20,'perceived':True,'lineOfEffect':True,
                'areas':{'area':{'distanceFeet':5,'lineOfEffect':True}}}
        world.actors[owner]['regularStartPhase']=Fraction(0)
        world.actors[owner]['regularEndPhase']=Fraction(1,4)
        world.actors[owner]['inProgressRegularEnd']=Fraction(25,4)
        world.actors['target']['regularEndPhase']=Fraction(9,4)
        return CopyPayloadReleases(CopyCaptures(h,witnesses),owner,
            {'owner':owner,'source':'Wizard/class-engine','rp':44,'maxRP':44},
            {'dissonance':0,'previousSpell':None,'refrain':0,'classRecords':{}},
            concentration or ConcentrationLedger(),world)

    @staticmethod
    def capture(m,profile,event='capture',sid='mimicry',adapt=False,source=None):
        geo=dict(actualCaptureWindow=True,conscious=True,actualFeatAvailable=True,sourceCreatureDistance=30,
            resolvedComponentDistance=30,sourcePerceived=True,effectPerceived=True,lineOfEffect=True,
            usedAgainstOwner=False,sourceLawfulRange=True,actualReactionLegal=True)
        return m.captures.capture(event,sid,source or 'source-'+profile,profile,'Wizard/class-engine',geo,adapt=adapt)

    @staticmethod
    def start(m):
        m.captures.start_regular('turn1',1,1,actual_new_regular_start=True)
        m.world.advance(Fraction(61,10),[m])

    @staticmethod
    def frame(m):
        return dict(turn=m.captures.current_turn,round=m.captures.current_round,actions=1,conscious=True,canAct=True,
            verbal=True,somatic=True,magicAllowed=True,knownLegalSelection=True,unmodifiedPrice=True,ordinaryActionAllowed=True)

    @staticmethod
    def selection(profile,targets=None):
        if profile=='step':return dict(destination=[10,0,0],distanceFeet=10,visible=True,fitting=True,unoccupied=True,lineOfEffect=True,teleportAllowed=True)
        selection={'targets':targets or ['target']}
        if profile=='burst':selection['area']=dict(id='area',distanceFeet=20,knownPoint=True,lineOfEffect=True)
        if profile=='boon':selection['statistic']='AC'
        return selection

    def declare(self,m,profile,event='cast',cap='capture',selection=None):
        return m.declare(event,cap,permission='pending',grant_id='Wizard/class-engine',frame=self.frame(m),selection=selection or self.selection(profile))

    @staticmethod
    def core(critical=False,wound=None,injury=None,con=0):
        return dict(constitutionSaveModifier=con,woundNatural=wound,injuryD6=injury,critical=critical)
