"""Independent adversarial probes of the submitted bounded helper.

These use the submitted Fixture class and a minimal source-derived mechanical
card table, NOT the full repository or its protected-input/hash validation suite.
Every world record is synthetic. 'accepted' reports helper behavior, not approval.
"""
from copy import deepcopy
from pathlib import Path
import json
import fishing_reference_submitted as ref
from fixture_submitted import Fixture
from audit_inputs import CARDS, BODY_GP

RESULTS=[]
def probe(name, fn):
    try:
        value=fn()
        RESULTS.append({'probe':name,'behavior':'accepted','details':value})
    except Exception as e:
        RESULTS.append({'probe':name,'behavior':'rejected','exception':type(e).__name__,'message':str(e)})

def capture_record(f):
    return f.records[f.records[f.check if f.method=='Trap' else f.capture]['captureEvidenceId']]

def rewrite_rolls(f, **changes):
    def walk(v):
        if isinstance(v,dict):
            if set(ref.CANONICAL)<=set(v):v.update(changes)
            for x in v.values():walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    walk(f.records)

def invalid_roll(field,value):
    f=Fixture();rewrite_rolls(f,**{field:value})
    f.records[f.commit]['attractionPhysicalId']=None
    f.records[f.resolution]['equipmentBonus']=0
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'descriptor':l.state['attempts'][f.aid]['canonicalRoll'],'recoveryEvaluated':f.creature in l.state['recoveries']}

for field,value in [('kind','attack'),('ability','DEX'),('proficiency','Survival'),('actualRoll',False),('automaticResult',True),('taskCategory','harvest')]:
    probe('Non-catch canonical descriptor '+field,lambda field=field,value=value:invalid_roll(field,value))

def ghost_bait():
    f=Fixture(bait=True)
    # Same registered physical dose, source-bound as a +3 Bait instead of +1.
    for r in f.records.values():
        if r['kind']=='assembly':r['itemRecipeIds'][f.bid]='recipe-198'
        elif r['kind']=='catch-roll':
            for v in r['items']:
                if v['physicalId']==f.bid:v['recipeId']='recipe-198'
    f.records[f.commit]['baitId']=None
    f.records[f.resolution]['equipmentBonus']=3
    l=f.run('check')
    return {'state':l.state['attempts'][f.aid]['state'],'baitUses':l.state['baitUses'],'eligibleExtra':l.state['attempts'][f.aid]['checkEligible'][f.bid],'scheduledExpiry':'bait:'+f.aid in l.state['due']}
probe('Registered Bait contributes without a journal debit',ghost_bait)

def missing_line(stage):
    f=Fixture();f.records[f.views[stage]['states']['A-item-641']]['currentHP']=0
    f.records[f.views[stage]['admission']]['apparatusStateIds']=[f.views[stage]['states']['A-item-164']]
    if stage=='check':f.records[f.resolution]['equipmentBonus']=1
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'sourceExtra':l.state['recoveries'][f.creature]['sourceExtra']}
probe('Broken indispensable Line omitted from check admission',lambda:missing_line('check'))
probe('Broken indispensable Line omitted from capture admission',lambda:missing_line('capture'))

def mismatched_mass():
    f=Fixture()
    for r in f.records.values():
        if r['kind']=='material-manifest':r['bodyMassLb']=12
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'manifestBodyLb':12,'admittedPreyLb':6}
probe('Twelve-pound body borrows a six-pound admission',mismatched_mass)

def omit_qualifying_item():
    f=Fixture()
    f.records[f.views['check']['view']]['items']=[v for v in f.records[f.views['check']['view']]['items'] if v['physicalId']!='A-item-641']
    f.records[f.resolution]['equipmentBonus']=1
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'acceptedBonus':1,'registeredFunctionalLineBonus':2}
probe('Omitted qualifying maximum item is silently ignored',omit_qualifying_item)

def late_trap_setup():
    f=Fixture(method='Trap')
    f.records[f.work]['intervals']=[{'startSeconds':3000,'endSeconds':3300,'hands':2,'actions':50}]
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'actualSetupInterval':[3000,3300],'acceptedSnapshotAt':300,'captureAt':3300}
probe('Trap set only during minutes 50-55 captures at minute 55',late_trap_setup)

def wrong_retrieval_worker():
    f=Fixture();p=capture_record(f)
    f.records[p['retrievalWorkEvidenceId']]['worker']='unrelated-helper'
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'lead':f.lead,'creditedRetriever':'unrelated-helper'}
probe('Attended capture accepts a different workers retrieval minutes',wrong_retrieval_worker)

def unloaded_rig():
    f=Fixture(numbers=[179,183,164,160,642]);l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'sourceExtra':l.state['recoveries'][f.creature]['sourceExtra'],'rigChumLoadRecords':0,'extraRigWorkRecords':0}
probe('Rig grants +2 with no load or extra-work evidence',unloaded_rig)

def false_presentation():
    f=Fixture(numbers=[179,183,164])
    for view in f.views.values():
        a=f.records[view['assembly']];p=f.records[a['presentationEvidenceId']]
        p.update(forms=['Lure'],sourcePhysicalIds=['A-item-179'],ordinaryBaitLotIds=[])
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'declaredLureSourceIsActually':'Rod179'}
probe('Rod is relabeled as a Lure in presentation.forms',false_presentation)

def reused_roll():
    a=Fixture();l=a.run('close')
    b=Fixture(prefix='B',start=4000,creature='fish-B',lead=a.lead)
    rewrite_rolls(b,id=a.roll['id'])
    w=ref.WorldEvidence({**a.records,**b.records},test_fixture=True)
    for key in (b.commit,b.check,b.capture):l.apply(w,key,l.state['version'])
    return {'capturedBodies':len(l.state['recoveries']),'rollIds':[x['checkId'] for x in l.state['attempts'].values()]}
probe('Same canonical roll ID funds two different catches',reused_roll)

def trap_close_without_retrieval():
    f=Fixture(method='Trap');l=f.run()
    l.apply(f.world(),f.close,l.state['version'])
    return {'state':l.state['attempts'][f.aid]['state'],'equipmentReservations':l.state['equipmentReservations'],'retrievalWorkSeconds':0}
probe('Trap closes as retrieved without five retrieval work minutes',trap_close_without_retrieval)

def failed_trap_frees_lead():
    f=Fixture(method='Trap');f.records[f.resolution]['degree']='Failure';l=f.run('check')
    d=f.add('failed-disposition','actual-disposition',[3301,0,0],attemptId=f.aid,physicalId=f.creature,reason='failed',location='still-deployed pond',elevationFeet=-1)
    e=f.add('failed-close','fishing-transition',[3301,0,0],operation='close',attemptId=f.aid,dispositionEvidenceId=d)
    l.apply(f.world(),e,l.state['version'])
    b=Fixture(method='Trap',prefix='B',start=3302,creature='fish-B',lead=f.lead)
    w=ref.WorldEvidence({**f.records,**b.records},test_fixture=True)
    l.apply(w,b.commit,l.state['version'])
    return {'oldTrapLocation':l.state['attempts'][f.aid]['disposition']['location'],'secondDeploymentState':l.state['attempts'][b.aid]['state']}
probe('Failed still-deployed Trap frees lead for another deployment',failed_trap_frees_lead)

def handover_cancels_check():
    f=Fixture(method='Trap');l=f.run('commit')
    d=f.add('handover-disposition','actual-disposition',[600,0,0],attemptId=f.aid,physicalId=f.creature,reason='lawful-handover',location='still-deployed pond',elevationFeet=-1,recipient='angler-B')
    e=f.add('handover-event','fishing-transition',[600,0,0],operation='close',attemptId=f.aid,dispositionEvidenceId=d)
    l.apply(f.world(),e,l.state['version'])
    return {'state':l.state['attempts'][f.aid]['state'],'due':l.state['due'],'successorRecordExists':False}
probe('Pending Trap handover deletes its scheduled check',handover_cancels_check)

def outside_attraction():
    f=Fixture();f.records[f.path]['unobstructedWaterPathFeet']=31
    l=f.run()
    return {'state':l.state['attempts'][f.aid]['state'],'response':l.state['attempts'][f.aid]['response']}
probe('Outside 30-foot response region remains selectable',outside_attraction)

def add_harvest(f,recovery,cp=7200,death=4000):
    captured=f.records[recovery['manifestEvidenceId']]
    data={k:deepcopy(v) for k,v in captured.items() if k not in ('id','kind','checkpoint')}
    mid=f.add('probe-harvest-manifest','material-manifest',[cp,0,0],**data)
    legal=f.add('probe-harvest-legal','lawful-extraction',[cp,0,0],physicalId=f.creature,deathOrRemovalTime=death)
    choice=f.add('probe-harvest-choice','harvest-category-choice',[cp-1,0,0],physicalId=f.creature,categories=['ordinary-fish-meat'])
    event=f.add('probe-harvest','resolved-ordinary-harvest',[cp,0,0],physicalId=f.creature,lawfulExtractionEvidenceId=legal,manifestEvidenceId=mid,choiceEvidenceId=choice,degree='Success')
    return event,mid

def origin_laundering():
    f=Fixture();f.records[f.manifest]['resourcePolicy']='summoned-no-resources'
    l=f.run();r=l.state['recoveries'][f.creature]
    event,_=add_harvest(f,r)
    h=ref.resolve_ordinary_harvest_units(f.world(),event,r,{})
    return {'initialPolicy':f.records[f.manifest]['resourcePolicy'],'authorizedExtra':r['authorizedUnitIds'],'extracted':h[f.creature]['authorizedExtractedUnitIds']}
probe('Initial no-resource origin disappears in later permitted snapshots',origin_laundering)

def lost_reserve_restored():
    f=Fixture();f.records[f.manifest]['extraReserve'][0]['state']='lost'
    l=f.run()
    return {'initialState':'lost','authorizedExtra':l.state['recoveries'][f.creature]['authorizedUnitIds']}
probe('Lost initial reserve becomes available again without a transition',lost_reserve_restored)

def lost_baseline_restored():
    f=Fixture();capture_record(f)
    f.records[capture_record(f)['manifestEvidenceId']]['baseline'][0]['state']='lost'
    l=f.run();r=l.state['recoveries'][f.creature];event,mid=add_harvest(f,r)
    f.records[mid]['baseline'][0]['state']='available'
    h=ref.resolve_ordinary_harvest_units(f.world(),event,r,{})
    return {'capturedState':'lost','extracted':h[f.creature]['authorizedExtractedUnitIds']}
probe('Lost captured baseline is restored by a later manifest',lost_baseline_restored)

def early_harvest():
    f=Fixture();l=f.run();r=l.state['recoveries'][f.creature]
    event,_=add_harvest(f,r,cp=2000,death=1800)
    h=ref.resolve_ordinary_harvest_units(f.world(),event,r,{})
    return {'captureAt':3600,'harvestAt':2000,'extracted':h[f.creature]['authorizedExtractedUnitIds']}
probe('Harvest predates the capture record authorizing it',early_harvest)

def future_death():
    f=Fixture();l=f.run();r=l.state['recoveries'][f.creature]
    event,_=add_harvest(f,r,cp=7200,death=10000)
    h=ref.resolve_ordinary_harvest_units(f.world(),event,r,{})
    return {'harvestAt':7200,'deathOrRemovalAt':h[f.creature]['deathOrRemovalTime']}
probe('Harvest carries a future death or removal clock',future_death)

def rename_partition():
    f=Fixture();l=ref.FishingLedger(CARDS)
    route=f.add('probe-forage','production-route',[-1,1,0],route='Forage',sharedStockId='shared-pond',allocationPartitionId='whole-pool',watchId='Watch-1')
    e=f.add('probe-forage-event','fishing-transition',[-1,1,0],operation='forage-route',routeEvidenceId=route)
    l.apply(f.world(),e,0)
    f.records[f.opportunity]['allocationPartitionId']='new-name'
    f.records[f.allocation]['partitionId']='new-name'
    l.apply(f.world(),f.commit,l.state['version'])
    return {'routes':[[list(k),v] for k,v in l.state['poolRoutes'].items()],'disjointMemberSetsPresent':False}
probe('Partition renaming bypasses whole-pool Forage exclusion',rename_partition)

def future_profile():
    f=Fixture();f.records[f.profile]['checkpoint']=[10000,0,0];l=f.run('commit')
    return {'committedAt':0,'profileEffectiveCheckpoint':10000,'response':l.state['attempts'][f.aid]['response']}
probe('Future prey profile is used by earlier response allocation',future_profile)

def body_reserve_bad_model():
    r=CARDS['recipe-163']['sourceRecipe']
    reserves=[{'id':'b'+str(i),'modelId':'fishing.hook','weightLb':.02,'complete':False,
        'inventoryEvidenceRef':'fixture-inventory','reservationEvidenceRef':'fixture-reservation','ownerOrderId':'order',
        'state':'available-reserved','grade':'Standard','priorMagicalAlteration':False,
        'originalConstituentIds':['same-original-hook'],'currentHP':5,'maximumHP':5,'durabilityPercent':0,'flawed':False} for i in range(7)]
    out=ref.ordered_output(r,'Masterwork',reserves)
    return {'recipeFamily':'Trap','acceptedReserveModels':[z['modelId'] for z in out['selected']],'allShareOneOriginalConstituent':True}
probe('Trap order accepts incomplete Hook bodies sharing a constituent',body_reserve_bad_model)

def repair_wrong_body():
    r=CARDS['recipe-179']['sourceRecipe'];body={'id':'fishing.hook','family':'Hook','baselinePriceGp':.1}
    quote=ref.repair_quote(r,body,1,5,['clip'],['clip'])
    return {'rodRepairMaterials':str(quote['materialReferenceGp']),'correctRodMaterials':'1/8','originalRequired':['clip']}
probe('Rod repair accepts Hook pricing and only a listed clip',repair_wrong_body)

def invalid_hp():
    return ref.structural_hp(5,1,1)
probe('Inconsistent B5 maximum is silently normalized as full health',invalid_hp)

def destroyed_bait_blank():
    r=CARDS['recipe-162']['sourceRecipe']
    z={'id':'blank','inventoryEvidenceRef':'inventory','reservationEvidenceRef':'reservation','ownerOrderId':'order','state':'available-reserved','grade':'Standard','priorMagicalAlteration':False,'carrierLb':.1,'wrapperLb':.01,'materialCondition':'destroyed'}
    out=ref.ordered_output(r,'Standard',[z])
    return {'quantity':out['outcome']['quantity'],'selectedCondition':out['selected'][0]['materialCondition']}
probe('Destroyed Bait carrier is accepted because it is not Spoiled',destroyed_bait_blank)

def post_capture_partial_mass_loss():
    f=Fixture();l=f.run();r=l.state['recoveries'][f.creature]
    event,mid=add_harvest(f,r)
    f.records[mid]['extraReserve'][0]['massLb']=.75
    h=ref.resolve_ordinary_harvest_units(f.world(),event,r,{})
    return {'originallyAuthorizedMassLb':1,'remainingMassLb':.75,'harvest':h[f.creature]}
probe('VALID post-capture loss reduces a previously whole authorized meat portion',post_capture_partial_mass_loss)

def distinct_setup_and_exposure_clocks():
    f=Fixture(bait=True)
    # Source-permitted timeline: dry setup begins at 0, first actual deployment
    # and Bait exposure occur at 300, catch check at 3300, retrieval at 3600,
    # receipt expiry at 3900. This changes no source duration or bonus.
    for r in f.records.values():
        if r['checkpoint']==[0,0,0] and r['kind'] not in ('material-manifest','ordinary-prey-profile','stock-allocation'):
            r['checkpoint']=[300,0,0]
        if r['kind']=='item-state' and r.get('physicalId')==f.bid:
            r['exposedAt']=[300,0,0];r['expiresAt']=[3900,0,0]
    f.records[f.commit]['attemptStartCheckpoint']=[0,0,0]
    f.records[f.commit]['baitExpiryCheckpoint']=[3900,0,0]
    ledger=ref.FishingLedger(CARDS)
    ledger.apply(f.world(),f.commit,0)
    return {'committed':True,'attemptStart':0,'exposure':300,'check':3300,'baitExpiry':3900}
probe('VALID source timeline separates setup start from exposure at minute 5',distinct_setup_and_exposure_clocks)

# Positive and rejection controls: these are independent smoke checks, not the
# submitted 220-check repository validation suite.
for method in ('Rod','Net','Trap'):
    probe('CONTROL ordinary '+method,lambda method=method:Fixture(method=method).run().state['attempts']['A-attempt']['state'])
def control_broken():
    f=Fixture();f.records[f.views['capture']['states']['A-item-641']]['currentHP']=0
    return f.run().state
probe('CONTROL correctly linked Broken Line is rejected',control_broken)

out={'scope':'Independent targeted probes, minimal source-register mechanical records; no repository/hash-suite rerun',
     'probeCount':len(RESULTS),'results':RESULTS}
Path(__file__).with_name('adversarial_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
for r in RESULTS:print(r['behavior'].upper(),r['probe'],json.dumps(r.get('details',r.get('message')),default=str))
