"""Submitted Fixture class; imports adapted to local mechanical test records.
No fixture or input record asserts actual game-world facts.
"""
from copy import deepcopy
import fishing_reference_submitted as ref
from audit_inputs import CARDS

class Fixture:
    def __init__(self,method='Rod',numbers=None,prefix='A',start=0,creature='fish-A',lead='angler-A',bait=False):
        self.records={};self.p=prefix;self.method=method;self.start=start;self.creature=creature;self.lead=lead
        self.aid=prefix+'-attempt';self.cp0=[start,0,0];self.cpc=[start+3300,0,0];self.cpl=[start+3600,1,0]
        self.numbers=numbers if numbers is not None else ([179,641,164,160] if method=='Rod' else [166,160] if method=='Net' else [161,160])
        if bait:self.numbers=self.numbers+[162]
        self.gear={prefix+'-item-'+str(n):'recipe-'+str(n) for n in self.numbers}
        self.bid=prefix+'-item-162' if bait else None
        self.roll={'id':prefix+'-roll','kind':'ability-check','actor':lead,'ability':'WIS','proficiency':'Fishing tackle','actualRoll':True,'automaticResult':False,'taskCategory':'ordinary-provision-catch'}
        self.manifest=self.add('manifest-initial','material-manifest',self.cp0,physicalId=creature,bodyMassLb=6,
            baseline=[self.unit('base',1)],extraReserve=[self.unit('extra1',1),self.unit('extra2',1),self.unit('extra3',1)],
            damagedBaseline=[self.unit('damaged',1)],unique=[self.unit('unique',.1,'exceptional-organ')],resourcePolicy='permitted')
        self.profile=self.add('prey','ordinary-prey-profile',self.cp0,physicalId=creature,approvedAffinities=['Water','Unholy'],captureProcedure='ordinary-provision')
        self.path=self.add('response-path','response-path',self.cp0,physicalId=creature,unobstructedWaterPathFeet=20,responseDisposition='receptive')
        self.response=self.add('response','response-candidates',self.cp0,opportunityId=prefix+'-opportunity',candidates=[{'physicalId':creature,'profileEvidenceId':self.profile,'responseEvidenceId':self.path}])
        self.allocation=self.add('allocation','stock-allocation',self.cp0,sharedStockId='shared-pond',partitionId='whole-pool')
        self.opportunity=self.add('opportunity','opportunity',self.cp0,opportunityId=prefix+'-opportunity',candidateCreatureIds=[creature],
            sharedStockId='shared-pond',allocationPartitionId='whole-pool',allocationEvidenceId=self.allocation,watchId='Watch-1',disposition='available-stock',manifestByCreatureId={creature:self.manifest})
        self.order=self.add('order','recovery-order',[start+3200,0,0],attemptId=self.aid,unitIds=[creature+'-extra1',creature+'-extra2',creature+'-extra3'])
        self.views={}
        for label,cp in [('deploy',self.cp0),('check',self.cpc),('capture',self.cpl)]:self.views[label]=self.make_view(label,cp)
        bait_id=None
        if bait:bait_id=self.add('unused-dose','unused-bait',self.cp0,physicalId=self.bid,unprotectedHours=23,condition='eligible')
        self.commit=self.add('commit','fishing-transition',self.cp0,operation='commit',attemptId=self.aid,lead=lead,
            opportunityEvidenceId=self.opportunity,assemblyEvidenceId=self.views['deploy']['assembly'],
            canonicalRoll=self.roll,checkCheckpoint=self.cpc,equipmentEvidenceId=self.views['deploy']['view'],
            attractionPhysicalId=next((i for i in self.gear if CARDS[self.gear[i]]['sourceRecipe']['recipeFamily']=='Lure'),None),
            responseEvidenceId=self.response,responseDraw=1,baitId=self.bid,
            **({'baitEvidenceId':bait_id,'baitExpiryCheckpoint':[start+3600,0,0]} if bait else {}))
        intervals=[{'startSeconds':start,'endSeconds':start+(300 if method=='Trap' else 3300),'hands':2,'actions':50 if method=='Trap' else 550}]
        self.work=self.add('work','work-record',self.cpc,worker=lead,intervals=intervals)
        self.config=self.add('setter','trap-configuration',[start+300,0,0],attemptId=self.aid,setter=lead,personalContributions={'WIS':2,'Fishing':2})
        extra=ref.effect_candidates(self.world(),self.views['check']['view'],CARDS)
        self.resolution=self.add('resolution','catch-resolution',self.cpc,attemptId=self.aid,canonicalRoll=self.roll,physicalId=creature,
            degree='Success',workEvidenceId=self.work,setterConfigurationEvidenceId=self.config,
            personalContributions={'WIS':2,'Fishing':2},assistantBonus=0,
            admissionEvidenceId=self.views['check']['admission'],equipmentEvidenceId=self.views['check']['view'],equipmentBonus=extra['bonus'])
        self.check=self.add('check-event','fishing-transition',self.cpc,operation='check',attemptId=self.aid,dueId='check:'+self.aid,
            catchResolutionEvidenceId=self.resolution,closureCheckpoint=[start+3900,0,0])
        if method=='Trap':
            capture=self.make_capture('trap-secure',self.cpc,self.views['check'])
            self.records[self.check]['captureEvidenceId']=capture
        else:
            capture=self.make_capture('landed',self.cpl,self.views['capture'])
            self.capture=self.add('capture-event','fishing-transition',self.cpl,operation='capture',attemptId=self.aid,captureEvidenceId=capture)
        self.expire=self.add('expiry','fishing-transition',[start+3600,0,0],operation='expire-bait',attemptId=self.aid,dueId='bait:'+self.aid)
        disp=self.add('disposition','actual-disposition',[start+3601,0,0],attemptId=self.aid,physicalId=creature,reason='retrieved',location='actual-bank',elevationFeet=0)
        self.close=self.add('close','fishing-transition',[start+3601,0,0],operation='close',attemptId=self.aid,dispositionEvidenceId=disp)

    def unit(self,name,mass,material='ordinary-fish-meat'):
        return {'id':self.creature+'-'+name,'massLb':mass,'material':material,'category':material,'state':'available'}

    def add(self,key,kind,cp,**kw):
        key=self.p+'-'+key
        assert key not in self.records,key
        self.records[key]={'id':key,'kind':kind,'checkpoint':list(cp),'authority':'synthetic FI-D01..24 fixture, not campaign content',
            'citations':['GPT_FISHING_SOURCE_CONFERENCE.md FI-D01..24; synthetic local facts explicitly assumed'],'fixture':True,**deepcopy(kw)}
        return key

    def world(self):return ref.WorldEvidence(self.records,test_fixture=True)

    def make_view(self,label,cp):
        views=[];states={};primary=[]
        required={'Rod':{'Rod','Line','Hook'},'Net':{'Net'},'Trap':{'Trap'}}[self.method]
        for item,rid in self.gear.items():
            fam=CARDS[rid]['sourceRecipe']['recipeFamily']
            kw={'physicalId':item,'currentHP':5,'complete':True,'suppressed':False,'melded':False}
            if fam=='Bait':kw.update({'currentHP':1,'receiptAttemptId':self.aid,'exposedAt':self.cp0,'expiresAt':[self.start+3600,0,0],'assemblyBaitSuppressed':False})
            state=self.add(label+'-state-'+item,'item-state',cp,**kw);states[item]=state
            if fam in required:primary.append(state)
            views.append({'physicalId':item,'recipeId':rid,'roll':deepcopy(self.roll),'stateEvidenceId':state})
        admission=self.add(label+'-admission','physical-admission',cp,method=self.method,disposition='admitted',
            preyMassLb=6,handlingLimitLb=10,wholeLinePathFeet=48,reachFeet=5,preyVolumeCubicFeet=.2,recoveryPathFeet=15,apparatusStateIds=primary)
        ordinary_lot=self.p+'-ordinary-bait-lot'
        presentation=self.add(label+'-presentation','bait-presentation',cp,attemptId=self.aid,
            sourcePhysicalIds=[ordinary_lot],ordinaryBaitLotIds=[ordinary_lot],forms=['ordinary-bait'])
        assembly=self.add(label+'-assembly','assembly',cp,attemptId=self.aid,lead=self.lead,method=self.method,
            participatingItemIds=list(self.gear),itemRecipeIds=self.gear,
            itemFamilyById={i:CARDS[rid]['sourceRecipe']['recipeFamily'] for i,rid in self.gear.items()},
            presentationEvidenceId=presentation,admissionEvidenceId=admission)
        view=self.add(label+'-view','catch-roll',cp,roll=self.roll,assemblyEvidenceId=assembly,items=views)
        return {'view':view,'assembly':assembly,'admission':admission,'states':states}

    def make_capture(self,label,cp,view):
        manifest=deepcopy(self.records[self.manifest]);manifest.pop('id');manifest.pop('kind');manifest.pop('checkpoint')
        current=self.add(label+'-manifest','material-manifest',cp,**manifest)
        work=self.add(label+'-work','work-record',cp,worker=self.lead,intervals=[{'startSeconds':self.start+3300,'endSeconds':cp[0],'hands':2,'actions':(cp[0]-self.start-3300)//6}])
        return self.add(label,'secure-capture',cp,physicalId=self.creature,attemptId=self.aid,manifestEvidenceId=current,
            admissionEvidenceId=view['admission'],equipmentEvidenceId=view['view'],recoveryOrderEvidenceId=self.order,
            retrievalWorkEvidenceId=work,lifeState='alive',location='Trap interior' if self.method=='Trap' else 'supported landing tub',elevationFeet=3)

    def run(self,through='capture'):
        ledger=ref.FishingLedger(CARDS);world=self.world()
        ledger.apply(world,self.commit,0)
        if through=='commit':return ledger
        ledger.apply(world,self.check,1)
        if through=='check' or self.method=='Trap':return ledger
        if self.bid:ledger.apply(world,self.expire,ledger.state['version'])
        ledger.apply(world,self.capture,ledger.state['version'])
        if through=='close':ledger.apply(world,self.close,ledger.state['version'])
        return ledger
