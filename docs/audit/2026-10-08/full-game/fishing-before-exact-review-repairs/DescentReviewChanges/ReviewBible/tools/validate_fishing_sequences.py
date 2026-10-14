"""Source-bound, synthetic campaign fixtures for FI-D01..24 interfaces.

No synthetic creature or site is promoted to game content. Documentary world
premises are explicitly fixtures. The helper's real-world verification limits
and the separate exact-review gate remain in the output.
"""
from copy import deepcopy
from fractions import Fraction as F
import json,re
import fishing_reference as ref
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,write

CARDS={c['recipeId']:c for c in read(ROOT/'data/director/fishing_recipe_candidate_internal.json')['cards']}


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


def main():
    checks=[];saved={}
    def check(case,name,condition):
        checks.append({'case':case,'name':name,'pass':bool(condition)})
        assert condition,name
    def reject(case,name,fn,ledger=None):
        before=deepcopy(ledger.state) if ledger else None
        try:fn()
        except ValueError:
            check(case,name,ledger is None or ledger.state==before);return
        check(case,name,False)
    def keep(name,fixture):saved[name]=deepcopy(fixture.records)
    f=Fixture();l=f.run();keep('ordinary-source-bound-Rod',f)
    check('FI-01','one successful source-bound ordinary catch has no inventory',l.state['attempts'][f.aid]['state']=='captured' and l.state['recoveries'][f.creature]['inventoryCreated']==[])
    check('FI-07','four actual pieces select +2 and two real extra units',ref.effect_candidates(f.world(),f.views['check']['view'],CARDS)['bonus']==2 and len(l.state['recoveries'][f.creature]['authorizedUnitIds'])==2)
    check('FI-10','living capture remains living',l.state['recoveries'][f.creature]['lifeStateAtCapture']=='alive')
    for field,value in [('id','other-roll'),('actor','other-angler'),('kind','saving-throw'),('ability','DEX'),('proficiency','Survival'),('actualRoll',False),('automaticResult',True),('taskCategory','harvest')]:
        x=Fixture();x.records[x.views['check']['view']]['items'][0]['roll'][field]=value
        reject('FI-07','reject mismatched per-item '+field,lambda x=x:ref.effect_candidates(x.world(),x.views['check']['view'],CARDS))
    for n,statefield in [(641,'suppressed'),(160,'melded')]:
        x=Fixture();x.records[x.views['check']['states']['A-item-'+str(n)]][statefield]=True
        out=ref.effect_candidates(x.world(),x.views['check']['view'],CARDS)
        check('FI-16',statefield+' removes only actual item bonus',out['bonus']==(1 if n==641 else 2))
    x=Fixture();x.records[x.views['capture']['states']['A-item-641']]['suppressed']=True
    check('FI-07','weaker still-qualified source supplies secure-capture recovery',x.run().state['recoveries'][x.creature]['sourceExtra']==1)
    x=Fixture();x.records[x.views['check']['states']['A-item-641']]['suppressed']=True;x.records[x.resolution]['equipmentBonus']=1
    check('FI-07','later recovered stronger item cannot increase prior-check entitlement',x.run().state['recoveries'][x.creature]['sourceExtra']==1)
    for field,value in [('automaticResult',True),('actualRoll',False),('taskCategory','harvest'),('kind','attack')]:
        x=Fixture();v=x.records[x.views['check']['view']];v['roll'][field]=value
        for i in v['items']:i['roll'][field]=value
        check('FI-01','no catch modifier on '+field,ref.effect_candidates(x.world(),x.views['check']['view'],CARDS)['bonus']==0)
    x=Fixture();x.records[x.views['deploy']['admission']]['wholeLinePathFeet']=51
    reject('FI-03','51-foot Rod path rejected',lambda:x.run('commit'))
    x=Fixture();x.records[x.views['deploy']['admission']]['preyMassLb']=12
    reject('FI-03','12-pound prey rejected',lambda:x.run('commit'))
    x=Fixture(numbers=[179,160])
    reject('FI-03','Rod and Lure alone lack required Line and Hook',lambda:x.run('commit'))
    x=Fixture();assembly=x.records[x.views['deploy']['assembly']]
    x.records[assembly['presentationEvidenceId']]['forms']=[]
    reject('FI-03','Rod requires real bait or Lure presentation',lambda:x.run('commit'))
    x=Fixture(method='Trap');assembly=x.records[x.views['deploy']['assembly']]
    x.records[assembly['presentationEvidenceId']]['forms']=['Lure']
    reject('FI-05','Lure cannot replace actual Trap bait',lambda:x.run('commit'))
    x=Fixture(method='Net',numbers=[166]);assembly=x.records[x.views['deploy']['assembly']]
    x.records[assembly['presentationEvidenceId']]['forms']=[]
    check('FI-04','unbaited Net can attempt real visible admitted prey',x.run().state['attempts'][x.aid]['state']=='captured')
    x.records[x.commit]['attractionPhysicalId']='A-item-166'
    reject('FI-14','unbaited Net cannot invent an attraction presentation',lambda:x.run('commit'))
    x=Fixture();assistant_work=x.add('assistant-work','work-record',x.cpc,worker='helper',intervals=[{'startSeconds':0,'endSeconds':3300,'hands':2,'actions':550}])
    assistant=x.add('assistant','fishing-assistant',x.cpc,worker='helper',attemptId=x.aid,trainedCredential='Fishing tackle',workEvidenceId=assistant_work)
    x.records[x.resolution].update({'assistantBonus':1,'assistantEvidenceId':assistant})
    check('FI-07','trained assistant completing all55 minutes can grant +1',x.run().state['attempts'][x.aid]['state']=='captured')
    x.records[assistant_work]['intervals'][0]['startSeconds']=3000
    reject('FI-07','late assistance does not qualify earlier check',lambda:x.run())
    x=Fixture();x.records[x.resolution]['assistantBonus']=2
    reject('FI-07','two assistants cannot grant +2',lambda:x.run())
    x=Fixture();x.records[x.resolution]['degree']='Critical Success'
    check('FI-01','Critical Success creates no additional specimen or reserve',len(x.run().state['recoveries'])==1 and len(x.run().state['recoveries'][x.creature]['authorizedUnitIds'])==2)
    x=Fixture();x.records[x.resolution]['equipmentBonus']=99
    reject('FI-07','resolved roll must use actual strongest recipe bonus',lambda:x.run())
    x=Fixture(method='Net');check('FI-04','source Net can capture one admitted fish',x.run().state['attempts'][x.aid]['state']=='captured');keep('ordinary-Net',x)
    for field,value in [('reachFeet',7),('preyVolumeCubicFeet',.6),('disposition','rejected-by-mesh')]:
        x=Fixture(method='Net');x.records[x.views['deploy']['admission']][field]=value
        reject('FI-04','Net rejects '+field,lambda x=x:x.run('commit'))
    x=Fixture(method='Trap');l=x.run();keep('one-shot-Trap',x)
    check('FI-05','Trap captures at minute55 with five setup work minutes',l.state['checkpoint'][0]==3300 and l.state['attempts'][x.aid]['state']=='captured')
    reject('FI-05','duplicate Trap check rejected atomically',lambda:l.apply(x.world(),x.check,l.state['version']),l)
    x=Fixture(method='Trap');x.records[x.resolution]['personalContributions']['WIS']=8
    reject('FI-05','later personal buff cannot replace setter snapshot',lambda:x.run())
    x=Fixture(method='Trap');x.records[x.resolution]['assistantBonus']=1
    reject('FI-05','Trap receives no generic assistant bonus',lambda:x.run())
    x=Fixture(method='Trap');l=x.run('commit')
    late=x.add('late-repair','state-transition',[5400,0,0],attemptId=x.aid)
    event=x.add('late-repair-event','fishing-transition',[5400,0,0],operation='checkpoint',attemptId=x.aid,stateEvidenceId=late)
    reject('FI-05','late repaired state cannot bypass historical minute55 check',lambda:l.apply(x.world(),event,l.state['version']),l)
    generic=deepcopy(x.records[event]);generic['checkpoint']=x.cpc;generic['dueId']='check:'+x.aid;x.records[event]=generic
    reject('FI-08','generic checkpoint cannot consume check due event',lambda:l.apply(x.world(),event,l.state['version']),l)
    x=Fixture(method='Trap');l=x.run('commit')
    failure=x.add('broken-history','no-catch-resolution',x.cpc,attemptId=x.aid,reason='assembly-inoperable',historicalCause='primary Trap body Broken before due check; no real containment')
    no=x.add('no-check','fishing-transition',x.cpc,operation='no-check',attemptId=x.aid,dueId='check:'+x.aid,noCatchEvidenceId=failure)
    l.apply(x.world(),no,l.state['version'])
    check('FI-16','Broken unattended apparatus resolves once without fabricated dice/catch',l.state['attempts'][x.aid]['state']=='no-catch' and not l.state['recoveries'])
    x=Fixture();l=x.run('commit');other=Fixture(prefix='B',start=1,creature=x.creature,lead='angler-B')
    both=ref.WorldEvidence({**x.records,**other.records},test_fixture=True)
    reject('FI-08','simultaneous real creature double-reservation rejected',lambda:l.apply(both,other.commit,l.state['version']),l)
    reject('FI-08','duplicate opportunity callback rejected',lambda:l.apply(x.world(),x.commit,l.state['version']),l)
    reject('FI-08','stale ledger version rejected',lambda:l.apply(x.world(),x.check,0),l)
    other=Fixture(prefix='B',start=1,creature='fish-B',lead='angler-B')
    # Change one whole physical apparatus ID, preserving its recorded identity.
    old='B-item-641';new='A-item-641'
    for rec in other.records.values():
        if rec.get('physicalId')==old:rec['physicalId']=new
        if rec['kind']=='assembly':
            rec['participatingItemIds']=[new if v==old else v for v in rec['participatingItemIds']]
            rec['itemRecipeIds'][new]=rec['itemRecipeIds'].pop(old)
            rec['itemFamilyById'][new]=rec['itemFamilyById'].pop(old)
        if rec['kind']=='catch-roll':
            for item in rec['items']:
                if item['physicalId']==old:item['physicalId']=new
    both=ref.WorldEvidence({**x.records,**other.records},test_fixture=True)
    reject('FI-08','apparatus cannot serve two concurrent attempts',lambda:l.apply(both,other.commit,l.state['version']),l)
    x=Fixture();l=x.run('commit');other=Fixture(prefix='B',start=1,creature='fish-B',lead='angler-B')
    both=ref.WorldEvidence({**x.records,**other.records},test_fixture=True);l.apply(both,other.commit,l.state['version'])
    check('FI-08','distinct prey/opportunity/equipment allow two anglers',len(l.state['attempts'])==2)
    x=Fixture();l=x.run('commit');other=Fixture(prefix='B',start=1,creature='fish-B',lead=x.lead)
    both=ref.WorldEvidence({**x.records,**other.records},test_fixture=True)
    reject('FI-05','same lead cannot deploy again while unresolved',lambda:l.apply(both,other.commit,l.state['version']),l)
    x=Fixture(bait=True);l=x.run();keep('bait-expiry-before-secure-capture',x)
    check('FI-02','dose consumed once and receipt expires before later same-time capture',l.state['baitUses']==[x.bid] and not l.state['attempts'][x.aid]['receiptActive'])
    x=Fixture(bait=True);x.records[x.p+'-unused-dose']['unprotectedHours']=24
    reject('FI-02','Spoiled stored dose cannot expose',lambda:x.run('commit'))
    x=Fixture(bait=True);l=x.run('check')
    reject('FI-02','capture cannot skip earlier same-time bait expiry',lambda:l.apply(x.world(),x.capture,l.state['version']),l)
    x=Fixture(bait=True);x.records[x.resolution]['degree']='Failure';l=x.run('check')
    check('FI-02','failed catch still spends opportunity and dose',l.state['baitUses']==[x.bid] and len(l.state['opportunities'])==1 and not l.state['recoveries'])
    x=Fixture(bait=True);l=x.run('commit')
    disposition=x.add('abandon-disposition','actual-disposition',[60,0,0],attemptId=x.aid,physicalId=x.creature,reason='abandoned',location='actual pond',elevationFeet=-1)
    event=x.add('abandon-event','fishing-transition',[60,0,0],operation='close',attemptId=x.aid,dispositionEvidenceId=disposition)
    l.apply(x.world(),event,l.state['version'])
    check('FI-02','early abandonment cancels future rolls without refunding spent bait/opportunity',l.state['baitUses']==[x.bid] and len(l.state['opportunities'])==1 and not l.state['due'])
    reject('FI-08','new callback cannot reopen abandoned opportunity',lambda:l.apply(x.world(),x.check,l.state['version']),l)
    x=Fixture();l=x.run('check')
    cap=x.records[x.records[x.capture]['captureEvidenceId']];work=x.records[cap['retrievalWorkEvidenceId']];work['intervals'][0]['startSeconds']=3400
    reject('FI-12','less than five actual retrieval minutes rejected',lambda:l.apply(x.world(),x.capture,l.state['version']),l)
    x=Fixture();l=x.run('check');cap=x.records[x.records[x.capture]['captureEvidenceId']]
    x.records[cap['retrievalWorkEvidenceId']]['intervals'][0]['hands']=1
    reject('FI-12','missing second actual retrieval hand rejected',lambda:l.apply(x.world(),x.capture,l.state['version']),l)
    x=Fixture();l=x.run('check');x.records[x.views['capture']['states']['A-item-641']]['currentHP']=0
    reject('FI-12','Broken Line cannot secure a catch',lambda:l.apply(x.world(),x.capture,l.state['version']),l)
    x=Fixture();l=x.run('check');x.records[x.views['capture']['states']['A-item-179']]['melded']=True
    reject('FI-16','melded indispensable Rod cannot secure a catch',lambda:l.apply(x.world(),x.capture,l.state['version']),l)
    x=Fixture();x.records[x.records[x.capture]['captureEvidenceId']]['location']=''
    reject('FI-12','secure capture needs actual receiving location',lambda:x.run())
    x=Fixture();l=x.run('check')
    disp=x.add('deadline-disposition','actual-disposition',[3900,0,0],attemptId=x.aid,physicalId=x.creature,reason='deadline',location='actual water',elevationFeet=-2)
    end=x.add('deadline','fishing-transition',[3900,0,0],operation='close',attemptId=x.aid,dueId='closure:'+x.aid,dispositionEvidenceId=disp)
    l.apply(x.world(),end,l.state['version'])
    check('FI-12','deadline closes without catch inventory or recovery',not l.state['recoveries'] and l.state['attempts'][x.aid]['state']=='closed')
    reject('FI-12','late capture cannot reopen deadline',lambda:l.apply(x.world(),x.capture,l.state['version']),l)
    for op in ['known-empty','impossible-access']:
        x=Fixture();x.records[x.opportunity]['disposition']=op
        reject('FI-13','precommit '+op+' spends nothing',lambda x=x:x.run('commit'))
    x=Fixture(bait=True);x.records[x.opportunity]['disposition']='exploratory';x.records[x.opportunity]['candidateCreatureIds']=[];x.records[x.response]['candidates']=[];x.records[x.commit]['responseDraw']=None
    l=x.run('commit');check('FI-13','actual empty exploratory opportunity can spend bait without inventing fish',l.state['baitUses']==[x.bid] and l.state['attempts'][x.aid]['selectedCreatureId'] is None)
    failure=x.add('empty-history','no-catch-resolution',x.cpc,attemptId=x.aid,reason='empty',historicalCause='finite exploratory stock contains no eligible creature')
    no=x.add('empty-no-check','fishing-transition',x.cpc,operation='no-check',attemptId=x.aid,dueId='check:'+x.aid,noCatchEvidenceId=failure)
    l.apply(x.world(),no,l.state['version']);check('FI-13','empty due opportunity produces no roll/recovery',l.state['attempts'][x.aid]['checkId'] is None and not l.state['recoveries'])
    x=Fixture();x.records[x.profile]['approvedAffinities']=[]
    r=ref.weighted_response(x.world(),x.response,'Unholy',1)
    check('FI-13','nonmatching real prey has ordinary weight one',r['weights']==[(x.creature,1)] and x.run().state['recoveries'][x.creature]['sourceExtra']==2)
    x=Fixture();entries=[]
    for letter,aff in [('A',['Unholy']),('B',[]),('C',['Unholy','Water'])]:
        creature='fish-'+letter;profile=x.add('weighted-profile-'+letter,'ordinary-prey-profile',x.cp0,physicalId=creature,approvedAffinities=aff,captureProcedure='ordinary-provision')
        path=x.add('weighted-path-'+letter,'response-path',x.cp0,physicalId=creature,unobstructedWaterPathFeet=20,responseDisposition='receptive')
        entries.append({'physicalId':creature,'profileEvidenceId':profile,'responseEvidenceId':path})
    x.records[x.response]['candidates']=list(reversed(entries))
    check('FI-14','stable weighted outcomes 2/1/2 with one draw',[ref.weighted_response(x.world(),x.response,'Unholy',i)['physicalId'] for i in range(1,6)]==['fish-A','fish-A','fish-B','fish-C','fish-C'])
    reject('FI-14','out-of-pool draw rejected',lambda:ref.weighted_response(x.world(),x.response,'Unholy',6))
    x.records[entries[0]['responseEvidenceId']]['unobstructedWaterPathFeet']=31
    check('FI-14','outside 30-foot preference gives no doubled weight',ref.weighted_response(x.world(),x.response,'Unholy',1)['weights'][0]==('fish-A',1))
    x.records[entries[1]['responseEvidenceId']]['responseDisposition']='rejected'
    reject('FI-14','hostile/rejecting candidate is not forced receptive',lambda:ref.weighted_response(x.world(),x.response,'Unholy',1))
    x=Fixture();x.records[x.profile]['captureProcedure']='combat-encounter'
    reject('FI-14','resisting encounter creature needs its own procedure',lambda:x.run('commit'))
    x=Fixture();x.records[x.profile]['approvedAffinities']=[];x.records[x.profile]['poisonImmune']=True
    check('FI-15','poison immunity alone gives no Poison preference',ref.weighted_response(x.world(),x.response,'Poison',1)['weights'][0][1]==1)
    x.records[x.profile]['approvedAffinities']=['Poison']
    check('FI-15','approved Poison affinity still works on immune prey',ref.weighted_response(x.world(),x.response,'Poison',1)['weights'][0][1]==2)
    x=Fixture();m=x.records[x.manifest];m['bodyMassLb']=.4;m['baseline']=[x.unit('base',.4)];m['extraReserve']=[];m['damagedBaseline']=[];m['unique']=[]
    x.records[x.order]['unitIds']=[]
    cap=x.records[x.records[x.capture]['captureEvidenceId']];cur=x.records[cap['manifestEvidenceId']]
    for key in ['bodyMassLb','baseline','extraReserve','damagedBaseline','unique']:cur[key]=deepcopy(m[key])
    l=x.run();check('FI-09','small fish retains source E but authorizes zero extra units',l.state['recoveries'][x.creature]['sourceExtra']==2 and l.state['recoveries'][x.creature]['authorizedUnitIds']==[])
    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']];cur=x.records[cap['manifestEvidenceId']]
    cur['extraReserve'].append(x.unit('invented',.1,'other-material'))
    reject('FI-09','new anatomical unit at capture rejected',lambda:x.run())
    x=Fixture();x.records[x.order]['checkpoint']=[3300,0,1]
    reject('FI-11','post-roll category order rejected',lambda:x.run())
    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']];x.records[cap['manifestEvidenceId']]['resourcePolicy']='summoned-no-resources'
    check('FI-10','origin prohibition preserves no-resource policy',x.run().state['recoveries'][x.creature]['authorizedUnitIds']==[])
    # Every enchanted piece is suppressed, while the complete physical assembly
    # still captures normally; first evaluation must explicitly persist zero.
    x=Fixture()
    for label in ['deploy','check','capture']:
        for state in x.views[label]['states'].values():x.records[state]['suppressed']=True
    x.records[x.commit]['attractionPhysicalId']=None;x.records[x.resolution]['equipmentBonus']=0
    l=x.run('close');first=deepcopy(l.state['recoveries'][x.creature]);check('FI-10','ordinary physical catch explicitly records zero',first['sourceExtra']==0 and first['evaluatedIncludingZero'])
    y=Fixture(prefix='B',start=4000,creature=x.creature,lead='angler-B')
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    for key in [y.commit,y.check,y.capture]:l.apply(both,key,l.state['version'])
    check('FI-10','new justified recapture cannot upgrade first zero evaluation',l.state['recoveries'][x.creature]==first)
    keep('zero-then-stronger-recapture',y)
    x=Fixture();cp=[7200,0,0]
    x.records[x.manifest]['baseline'].append(x.unit('scales',.2,'ordinary-scales'))
    capture_manifest=x.records[x.records[x.capture]['captureEvidenceId']]['manifestEvidenceId']
    x.records[capture_manifest]['baseline'].append(x.unit('scales',.2,'ordinary-scales'))
    l=x.run()
    manifest=deepcopy(x.records[x.manifest]);manifest.pop('id');manifest.pop('kind');manifest.pop('checkpoint')
    # A real separate scale portion uses part of the original fixture's body
    # mass; it is not also in the meat or Fishing extra reserve.
    mid=x.add('harvest-manifest','material-manifest',cp,**manifest)
    prerequisite=x.add('extraction-authority','lawful-extraction',cp,physicalId=x.creature,
        deathOrRemovalTime=4000,governingProcedure='CRAFTING_HARVEST_PLAYTEST.md; independently resolved lawful extraction, actual access/tools/DC/time assumed by this synthetic fixture')
    choice=x.add('harvest-choice','harvest-category-choice',[6000,0,0],physicalId=x.creature,categories=['ordinary-fish-meat'])
    event=x.add('harvest-event','resolved-ordinary-harvest',cp,physicalId=x.creature,
        lawfulExtractionEvidenceId=prerequisite,manifestEvidenceId=mid,choiceEvidenceId=choice,
        degree='Critical Success',damagedBaselineUnitId=x.creature+'-damaged')
    recovery=l.state['recoveries'][x.creature];h=ref.resolve_ordinary_harvest_units(x.world(),event,recovery,{})
    check('FI-11','baseline, two Fishing units and separate critical damaged unit remain distinct',h[x.creature]['authorizedExtractedUnitIds']==[x.creature+'-'+k for k in ['base','extra1','extra2','damaged']])
    check('FI-11','partial choice forfeits unselected scale unit and grants no unique organ',h[x.creature]['forfeitedUnselectedOrdinaryUnitIds']==[x.creature+'-scales'] and h[x.creature]['uniqueDropsAuthorized']==[])
    check('FI-23','harvest boundary preserves age and creates no serving or Supply Unit',h[x.creature]['deathOrRemovalTime']==4000 and h[x.creature]['foodServingCredit']==0 and h[x.creature]['completeSupplyUnits']==0)
    reject('FI-10','new harvester cannot reset ordinary body resolution',lambda:ref.resolve_ordinary_harvest_units(x.world(),event,recovery,h))
    x.records[event]['damagedBaselineUnitId']=x.creature+'-extra1'
    reject('FI-11','critical harvesting cannot duplicate a Fishing reserve unit',lambda:ref.resolve_ordinary_harvest_units(x.world(),event,recovery,{}))
    x.records[event]['degree']='Failure';x.records[event]['damagedBaselineUnitId']=None
    h=ref.resolve_ordinary_harvest_units(x.world(),event,recovery,{})
    check('FI-11','failed extraction yields no units',h[x.creature]['authorizedExtractedUnitIds']==[])
    reject('FI-11','failed harvest does not reopen through another worker',lambda:ref.resolve_ordinary_harvest_units(x.world(),event,recovery,h))
    keep('partial-critical-failed-harvest-boundary',x)
    x=Fixture();l=ref.FishingLedger(CARDS)
    route=x.add('forage-route','production-route',[-1,1,0],route='Forage',sharedStockId='shared-pond',allocationPartitionId='whole-pool',watchId='Watch-1')
    route_event=x.add('forage-event','fishing-transition',[-1,1,0],operation='forage-route',routeEvidenceId=route)
    l.apply(x.world(),route_event,0)
    reject('FI-23','same pool/watch cannot also produce Fishing after Forage',lambda:l.apply(x.world(),x.commit,l.state['version']),l)
    x.records[x.opportunity]['allocationPartitionId']='documented-disjoint-fish';x.records[x.allocation]['partitionId']='documented-disjoint-fish'
    l.apply(x.world(),x.commit,l.state['version']);check('FI-23','authoritative disjoint physical stock partition is allowed',len(l.state['attempts'])==1)
    for f in saved.values():
        assert all(v['fixture'] and v['citations'] for v in f.values())
    preliminary=read(AUDIT/'FISHING_PRELIMINARY_VALIDATION.json')
    assert all(c['pass'] for c in preliminary['checks'])
    baseline=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    check('FI-24','63 protected input hashes unchanged',all(sha(GAME/p)==h for p,h in baseline.items()))
    outputs=read(AUDIT/'FISHING_AUTHORING_STATUS.json')['outputs']
    check('FI-24','six exact candidate artifacts unchanged during sequence work',all(sha(ROOT/p)==h for p,h in outputs.items()))
    dump(AUDIT/'FISHING_SEQUENCE_FIXTURES.json',{'status':'synthetic test evidence, not game content','fixtures':saved})
    result={'status':'bounded sequence checks passed; exact review preparation ongoing','checks':checks,
        'preliminaryChecks':len(preliminary['checks']),'qualityCases':len(preliminary['qualityCases']),
        'structuralCases':len(preliminary['structuralCases']),'repairQuotes':len(preliminary['repairQuotes']),
        'syntheticFixtureSets':len(saved),'recipesApproved':0,'runtimeImplemented':False,
        'worldFactsAuthenticated':False,'fullScenarioReadThroughStillRequired':True,
        'remainingBeforeDispatch':['review all 24 written cases against exact artifacts','final helper audit for missing cross-links/timing/placement','complete exact-review packet and audience reconstruction evidence'],
        'sourceInformationDeleted':False,'cosmology':'post-push only'}
    dump(AUDIT/'FISHING_SEQUENCE_VALIDATION.json',result)
    print(json.dumps({'sequenceChecks':len(checks),'preliminaryChecks':len(preliminary['checks']),
        'fixtureSets':len(saved),'recipesApproved':0,'runtimeImplemented':False}))


if __name__=='__main__':main()
