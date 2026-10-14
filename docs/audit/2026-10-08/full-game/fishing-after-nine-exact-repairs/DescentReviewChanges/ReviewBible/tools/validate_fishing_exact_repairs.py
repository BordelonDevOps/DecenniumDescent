"""Finite FI-E regressions. Partial reports never authorize promotion.

Synthetic campaign records test relationship validation; they do not certify
actual stock, behavior, custody, or world facts. Historical reports are retained.
"""
from copy import deepcopy
import json
import fishing_reference as ref
from validate_fishing_sequences import Fixture,CARDS
from fishing_crafting_fixtures import CraftFixture,MODELS
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump


class Checks:
    def __init__(self):self.rows=[];self.fixtures={}
    def check(self,issue,name,condition):
        self.rows.append({'issue':issue,'name':name,'pass':bool(condition)})
        assert condition,name
    def reject(self,issue,name,fn,ledger=None):
        before=deepcopy(ledger.state) if ledger else None
        try:fn()
        except ValueError:
            self.check(issue,name,ledger is None or ledger.state==before);return
        self.check(issue,name,False)
    def keep(self,name,fixture):self.fixtures[name]=deepcopy(fixture.records)


def response_region(c):
    issue='FI-E07'
    x=Fixture();x.records[x.path]['unobstructedWaterPathFeet']=30
    ledger=x.run()
    c.check(issue,'30-foot attraction path and separate 48-foot Rod path capture normally',
        ledger.state['attempts'][x.aid]['state']=='captured' and
        ledger.state['attempts'][x.aid]['response']['weights']==[(x.creature,2)])
    c.keep('e07-thirty-foot-response-forty-eight-foot-Rod',x)
    x=Fixture();x.records[x.path]['unobstructedWaterPathFeet']=31
    r=ref.weighted_response(x.world(),x.response,'Unholy',None)
    c.check(issue,'31-foot candidate excluded completely',r=={'physicalId':None,'weights':[],'draw':None})
    c.reject(issue,'cannot draw an excluded 31-foot creature',lambda:ref.weighted_response(x.world(),x.response,'Unholy',1))
    c.reject(issue,'journal cannot capture out-of-region candidate',lambda:x.run('commit'))
    x.records[x.commit]['responseDraw']=None
    c.reject(issue,'known-empty attraction allocation cannot commit as available stock',lambda:x.run('commit'))
    x.records[x.opportunity]['disposition']='exploratory'
    c.check(issue,'exploratory empty allocation records no replacement',x.run('commit').state['attempts'][x.aid]['selectedCreatureId'] is None)

    x=Fixture();entries=[]
    for letter,aff in [('A',['Unholy']),('B',[]),('C',['Unholy','Water'])]:
        creature='fish-'+letter
        profile=x.add('e07-profile-'+letter,'ordinary-prey-profile',x.cp0,physicalId=creature,
            approvedAffinities=aff,captureProcedure='ordinary-provision')
        path=x.add('e07-path-'+letter,'response-path',x.cp0,physicalId=creature,
            unobstructedWaterPathFeet=30,responseDisposition='receptive',
            originEvidenceId=x.origin,opportunityId=x.records[x.opportunity]['opportunityId'])
        entries.append({'physicalId':creature,'profileEvidenceId':profile,'responseEvidenceId':path})
    x.records[x.response]['candidates']=list(reversed(entries))
    x.records[x.opportunity]['candidateCreatureIds']=[e['physicalId'] for e in entries]
    results=[ref.weighted_response(x.world(),x.response,'Unholy',i) for i in range(1,6)]
    c.check(issue,'stable 2/1/2 distribution includes receptive nonmatch once',
        [r['physicalId'] for r in results]==['fish-A','fish-A','fish-B','fish-C','fish-C'] and
        all(r['weights']==[('fish-A',2),('fish-B',1),('fish-C',2)] for r in results))
    c.reject(issue,'one draw must lie in finite pool',lambda:ref.weighted_response(x.world(),x.response,'Unholy',6))
    x.records[entries[0]['responseEvidenceId']]['unobstructedWaterPathFeet']=31
    c.check(issue,'out-of-region matching candidate cannot retain weight one',
        ref.weighted_response(x.world(),x.response,'Unholy',1)['weights']==[('fish-B',1),('fish-C',2)])
    c.keep('e07-finite-weighted-region',x)
    x.records[entries[1]['responseEvidenceId']]['responseDisposition']='rejected'
    c.reject(issue,'rejection is never compelled into receptive response',lambda:ref.weighted_response(x.world(),x.response,'Unholy',1))

    for field,value in [('originEvidenceId','another-origin'),('opportunityId','another-opportunity')]:
        x=Fixture();x.records[x.path][field]=value
        c.reject(issue,'path must bind actual '+field,lambda:x.run('commit'))
    for field,value in [('pointId','another-bait-point'),('attemptId','another-attempt'),('assemblyEvidenceId','another-assembly')]:
        x=Fixture();x.records[x.origin][field]=value
        c.reject(issue,'origin must bind actual '+field,lambda:x.run('commit'))
    x=Fixture();x.records[x.opportunity]['candidateCreatureIds'].append('unrecorded-fish')
    c.reject(issue,'direct selector requires entire opportunity candidate set',lambda:ref.weighted_response(x.world(),x.response,'Unholy',1))
    x=Fixture();x.records[x.response]['attractionPhysicalId']='A-item-179'
    c.reject(issue,'journal rejects different committed attraction source',lambda:x.run('commit'))
    x=Fixture();x.records[x.response]['allocationProcedure']='ordinary-visible-response'
    c.reject(issue,'ordinary response cannot enlarge selected-attraction allocation',lambda:x.run('commit'))

    x=Fixture(method='Net',numbers=[166]);x.records[x.path]['unobstructedWaterPathFeet']=31
    c.check(issue,'separately recorded ordinary visible Net has no attraction weighting',
        x.run().state['attempts'][x.aid]['response']['weights']==[(x.creature,1)])
    x=Fixture();ledger=x.run('commit')
    c.reject(issue,'one opportunity cannot redraw by replaying commitment',lambda:ledger.apply(x.world(),x.commit,ledger.state['version']),ledger)
    resolution=x.records[x.resolution];resolution['physicalId']='replacement-fish'
    c.reject(issue,'unavailable original fish cannot be replaced at check',lambda:ledger.apply(x.world(),x.check,ledger.state['version']),ledger)

    # Point identity only here. FI-E05 supplies the separate load/work checks.
    x=Fixture(numbers=[179,641,164,642]);x.select_attraction('A-item-642')
    assembly=x.records[x.views['deploy']['assembly']]
    deployment=x.add('e07-rig-deployment','rig-deployment',x.cp0,attemptId=x.aid,
        dispenserPhysicalId='A-item-642',dispenserPointId='A-rig-point')
    assembly['rigDeploymentEvidenceId']=deployment
    x.records[x.origin].update({'pointKind':'rig-dispenser','pointId':'A-rig-point'})
    c.check(issue,'Rig response selector uses recorded dispenser point',
        ref.weighted_response(x.world(),x.response,'Water',1)['physicalId']==x.creature)
    x.records[x.origin]['pointId']='A-bait-point'
    c.reject(issue,'Rig selector cannot borrow another bait point',lambda:ref.weighted_response(x.world(),x.response,'Water',1))


def catch_admission(c):
    issue='FI-E01'
    invalid=[('kind','attack'),('ability','DEX'),('proficiency','Survival'),
        ('automaticResult',True),('actualRoll',False),('taskCategory','harvest')]
    for field,value in invalid:
        x=Fixture();roll=deepcopy(x.roll);roll[field]=value
        for record in x.records.values():
            if 'canonicalRoll' in record:record['canonicalRoll']=deepcopy(roll)
            if record['kind']=='catch-roll':
                record['roll']=deepcopy(roll)
                for item in record['items']:item['roll']=deepcopy(roll)
        x.records[x.resolution]['equipmentBonus']=0;x.sync_core()
        x.select_attraction(None)
        c.check(issue,'unrelated selector still returns zero for '+field,
            ref.effect_candidates(x.world(),x.views['check']['view'],CARDS)['bonus']==0)
        ledger=ref.FishingLedger(CARDS)
        c.reject(issue,'journal atomically rejects '+field+' despite claimed Success',
            lambda:ledger.apply(x.world(),x.commit,0),ledger)

    x=Fixture();ledger=x.run('close')
    y=Fixture(prefix='B',start=4000,creature='fish-B',lead='angler-B')
    for record in y.records.values():
        if 'canonicalRoll' in record:record['canonicalRoll']['id']=x.roll['id']
        if record['kind']=='catch-roll':
            record['roll']['id']=x.roll['id']
            for item in record['items']:item['roll']['id']=x.roll['id']
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    c.reject(issue,'closed prior attempt still owns its canonical roll ID',
        lambda:ledger.apply(both,y.commit,ledger.state['version']),ledger)
    c.check(issue,'roll registry persists original attempt binding',ledger.state['rollAttempts']=={x.roll['id']:x.aid})

    for method in ('Rod','Net','Trap'):
        for training,term in [('trained',2),('untrained',0),('expertise',4)]:
            x=Fixture(method=method)
            x.records[x.credential]['training']=training
            x.records[x.resolution]['personalContributions']['Fishing']=term
            x.records[x.config]['personalContributions']['Fishing']=term
            x.records[x.core]['untrainedDisadvantageApplied']=training=='untrained'
            x.sync_core()
            ledger=x.run()
            c.check(issue,method+' '+training+' uses actual credential and single proficiency term',
                ledger.state['attempts'][x.aid]['state']=='captured')
            c.keep('e01-'+method.lower()+'-'+training,x)
            if training=='untrained':
                x.records[x.core]['untrainedDisadvantageApplied']=False
                c.reject(issue,method+' untrained result cannot omit disadvantage source',lambda:x.run())
            if training=='expertise':
                x.records[x.resolution]['personalContributions']['Fishing']=6
                x.records[x.config]['personalContributions']['Fishing']=6;x.sync_core()
                c.reject(issue,method+' expertise replaces rather than adds another PB',lambda:x.run())

    for dc in (12,15,18):
        x=Fixture();x.records[x.catch_profile]['dc']=dc;x.records[x.resolution]['dc']=dc;x.sync_core()
        c.check(issue,'predeclared ordinary DC '+str(dc)+' binds Core resolution',x.run().state['attempts'][x.aid]['catchDC']==dc)
    x=Fixture();x.records[x.catch_profile]['dc']=21
    c.reject(issue,'nonordinary DC needs independently reviewed override',lambda:x.run('commit'))
    override=x.add('reviewed-override','reviewed-catch-dc',x.setup_start,catchProfileEvidenceId=x.catch_profile,
        dc=21,method='Rod',reviewStatus='reviewed')
    x.records[x.catch_profile]['reviewedOverrideEvidenceId']=override
    x.records[x.resolution]['dc']=21;x.sync_core()
    c.check(issue,'separately reviewed override retains its own declared DC',x.run().state['attempts'][x.aid]['catchDC']==21)
    x.records[override]['dc']=24
    c.reject(issue,'override for another DC cannot qualify profile',lambda:x.run('commit'))

    x=Fixture();ledger=x.run('commit');x.records[x.resolution]['dc']=15;x.sync_core()
    c.reject(issue,'matching resolution and Core cannot change committed DC',lambda:ledger.apply(x.world(),x.check,1),ledger)
    x=Fixture();x.records[x.core]['degree']='Critical Success'
    c.reject(issue,'degree label must agree with separately resolved Core evidence',lambda:x.run())
    x=Fixture();x.records[x.core]['equipmentBonus']=99
    c.reject(issue,'Core equipment amount must agree with catch record',lambda:x.run())
    x=Fixture();x.records[x.credential]['actor']='another-angler'
    c.reject(issue,'another actor credential cannot grant proficiency',lambda:x.run())
    x=Fixture();x.records[x.credential]['proficiency']='Survival'
    c.reject(issue,'different credential cannot grant Fishing PB',lambda:x.run())
    x=Fixture();x.records[x.credential]['checkpoint']=[3301,0,0]
    c.reject(issue,'future credential cannot justify earlier catch',lambda:x.run())
    x=Fixture(method='Trap')
    for key in (x.resolution,x.config):x.records[key]['personalContributions']['arbitrary-buff']=30
    x.sync_core()
    c.reject(issue,'matching Trap dictionaries cannot introduce extra personal terms',lambda:x.run())
    x=Fixture(method='Trap');x.records[x.config]['credentialEvidenceId']='replacement-credential'
    c.reject(issue,'Trap cannot replace configured setter credential',lambda:x.run())
    x=Fixture();bonus=x.add('legal-bonus','catch-personal-bonus',x.cpc,actor=x.lead,
        rollId=x.roll['id'],approvedTaskCategory='ordinary-provision-catch',value=1)
    x.records[x.core]['otherBonusEvidenceIds']=[bonus]
    c.check(issue,'ordinary independent bonus has actual governing evidence',x.run().state['attempts'][x.aid]['state']=='captured')
    x.records[bonus]['rollId']='another-roll'
    c.reject(issue,'personal bonus evidence must belong to this actual roll',lambda:x.run())
    x=Fixture(method='Trap');x.records[x.core]['otherBonusEvidenceIds']=['future-buff']
    c.reject(issue,'unattended Trap cannot import later personal bonus',lambda:x.run())


def crafting_qualification(c):
    issue='FI-E10'
    x=CraftFixture(band='Masterwork');out=x.output()
    c.check(issue,'seven complete actual Trap bodies produce seven Masterwork outputs',
        len(out['selected'])==7 and [z['physicalId'] for z in out['selected']]==x.state_ids)
    c.keep('e10-seven-real-Trap-reserves',x)
    c.reject(issue,'unbound reserve labels cannot qualify production',lambda:ref.ordered_output(x.recipe,'Masterwork',x.reserves()))
    x=CraftFixture();x.records['body-0']['complete']=False
    c.reject(issue,'incomplete correct-family body cannot qualify reserve',x.output)
    x=CraftFixture();hook=CraftFixture('recipe-164')
    for i in range(7):
        source_i=min(i,len(hook.state_ids)-1)
        for prefix in ('body','creation','inventory','reservation'):
            encoded=json.dumps(hook.records[f'{prefix}-{source_i}'])
            for name in ('body','creation','inventory','reservation'):
                encoded=encoded.replace(f'{name}-{source_i}',f'{name}-{i}')
            x.records[f'{prefix}-{i}']=json.loads(encoded)
        x.records[f'body-{i}']['complete']=False
    c.reject(issue,'seven incomplete Hook bodies cannot substitute for Trap bodies',x.output)
    for i in range(7):x.records[f'body-{i}']['complete']=True
    c.reject(issue,'complete Hook bodies still have wrong admitted family',x.output)
    x=CraftFixture();inv=x.records['inventory-0'];inv['constituents'].pop()
    c.reject(issue,'missing actual original Trap primary pauses reserve',x.output)
    x=CraftFixture();x.records['inventory-1']['constituents'][0]['physicalId']='body-0-basket-frame'
    x.records['creation-1']['primaryConstituents']['basket-frame']=['body-0-basket-frame']
    c.reject(issue,'two reserve bodies cannot share one original frame',x.output)
    for field,value in [('orderId','another-order'),('physicalId','another-body'),('state','released')]:
        x=CraftFixture();x.records['reservation-0'][field]=value
        c.reject(issue,'actual reservation must retain '+field,x.output)
    x=CraftFixture();x.records['inventory-0']['reservedForOrderId']='another-order'
    c.reject(issue,'inventory cannot be reserved for another order',x.output)
    x=CraftFixture();x.records['inventory-0']['availability']='unavailable'
    c.reject(issue,'stale availability cannot qualify body stock',x.output)
    x=CraftFixture();x.state_ids.reverse()
    c.reject(issue,'post-outcome reserve reordering rejected',x.output)
    x=CraftFixture();x.records[x.quality_id]['band']='Masterwork'
    c.reject(issue,'actual quality record must match claimed result',x.output)
    x=CraftFixture();x.records['creation-0']['bodyProfile']['baselineWeightLb']=.02
    c.reject(issue,'fixed body profile cannot shrink a Trap to Hook weight',x.output)
    x=CraftFixture();x.records['body-0']['priorMagicalAlteration']=True
    c.reject(issue,'previously altered reserve cannot be freshly enchanted',x.output)
    x=CraftFixture();x.records['body-0']['currentHP']=1;x.outcome('Exceptional','property')
    out=x.output()
    c.check(issue,'damaged 1/5 reserve retains four-point damage deficit at 2/6',
        (out['selected'][0]['currentHP'],out['selected'][0]['maximumHP'])==(2,6))
    x=CraftFixture();x.records['body-6']['currentHP']=0
    c.reject(issue,'Broken unused maximum reserve still pauses completion',x.output)
    for packaged in (False,True):
        x=CraftFixture('recipe-171','Masterwork',packaged=packaged)
        c.check(issue,('exclusive package' if packaged else 'separate identities')+' provides four real Bait blanks',
            len(x.output()['selected'])==4)
        c.keep('e10-bait-'+('package' if packaged else 'separate'),x)
        for role in ('carrier','wrapper'):
            x=CraftFixture('recipe-171','Masterwork',packaged=packaged)
            parts=x.records['inventory-0']['constituents']
            if packaged:parts[0][role+'Condition']='destroyed'
            else:next(z for z in parts if z['physicalId'].endswith(role))['materialCondition']='destroyed'
            c.reject(issue,('packaged ' if packaged else 'separate ')+role+' destroyed cannot qualify Bait',x.output)
    x=CraftFixture('recipe-171');x.records['inventory-0']['constituents'][0]['condition']='destroyed'
    c.reject(issue,'destroyed material identity cannot be restored by eligible label',x.output)
    x=CraftFixture('recipe-171');x.records['inventory-0']['constituents'][0]['massLb']=.09
    c.reject(issue,'Bait carrier requires actual full tenth pound',x.output)
    c.reject(issue,'unmodified B5 at 1/1 cannot be normalized into healed 5/5',lambda:ref.structural_hp(5,1,1))
    x=CraftFixture();x.records['body-0'].update({'maximumHP':1,'currentHP':1})
    c.reject(issue,'contradictory HP record fails bound reserve qualification',x.output)
    x=CraftFixture();x.records['body-0']['durabilityPercent']=50;x.records['body-0']['maximumHP']=7
    c.reject(issue,'strongest improvement cannot change without actual body history',x.output)

    for rid in ['recipe-179','recipe-641','recipe-163','recipe-642']:
        x=CraftFixture(rid,repair=True);x.records['body-0']['currentHP']=0
        q=x.quote()
        c.check(issue,rid+' Broken qualification binds actual recipe and model',
            q['recipeId']==rid and q['bodyModelId']==x.model['id'] and q['successHP']==5 and not q['repairCompleted'])
    x=CraftFixture('recipe-179',repair=True);x.records['body-0']['currentHP']=1
    q=x.quote()
    c.check(issue,'qualified Rod functional cost uses its own .50gp body',str(q['materialReferenceGp'])=='1/8' and str(q['purchaseGp'])=='13/100')
    x.records['creation-0']['bodyProfile']['baselinePriceGp']=.10
    c.reject(issue,'Hook price cannot enter actual Rod repair through altered profile',x.quote)
    x=CraftFixture('recipe-179',repair=True);x.records['inventory-0']['constituents']=[]
    c.reject(issue,'arbitrary clip cannot replace actual required original shaft',x.quote)
    x=CraftFixture('recipe-179',repair=True);x.records['creation-0']['additionalIrreplaceableConstituentIds']=['original-inlay']
    c.reject(issue,'separately recorded irreplaceable original also remains required',x.quote)
    x.records['inventory-0']['constituents'].append({'physicalId':'original-inlay','originalBodyId':'body-0','condition':'intact'})
    c.check(issue,'recovered additional original qualifies only with actual inventory record','original-inlay' in x.quote()['requiredOriginalIds'])
    x=CraftFixture('recipe-179',repair=True)
    x.records['creation-0']['primaryConstituents']={'clip':['clip-only']}
    x.records['inventory-0']['constituents']=[{'physicalId':'clip-only','originalBodyId':'body-0','condition':'intact'}]
    c.reject(issue,'fabricated primary list contradicts modeled original assembly',x.quote)
    x=CraftFixture('recipe-179',repair=True);x.records['body-0']['recipeId']='recipe-164'
    c.reject(issue,'repair recipe cannot differ from creation recipe',x.quote)
    x=CraftFixture('recipe-179',repair=True);x.records['creation-0']['recipeId']='recipe-164';x.records['body-0']['recipeId']='recipe-164'
    c.reject(issue,'matching changed recipe labels still cannot mix Hook with Rod body',x.quote)
    x=CraftFixture('recipe-179',repair=True);x.records['body-0'].update({'flawed':True,'maximumHP':2,'currentHP':0})
    x.records['creation-0']['persistentFlaw']=True;q=x.quote()
    c.check(issue,'repair preserves persistent flaw and restores only flawed maximum',q['persistentFlaw'] and q['successHP']==2)
    x.records['body-0'].update({'flawed':False,'maximumHP':5})
    c.reject(issue,'a later state cannot erase the original persistent flaw',x.quote)
    x=CraftFixture('recipe-641',repair=True);x.records['body-0']['currentHP']=0;x.records['body-0']['complete']=False
    part=x.records['inventory-0']['constituents'][0];ident=part['physicalId']
    part['condition']='broken';part['recoveredOriginalSections']=[
        {'physicalId':'recovered-first','originalConstituentId':ident,'startFeet':0,'endFeet':23,'condition':'damaged'},
        {'physicalId':'recovered-second','originalConstituentId':ident,'startFeet':23,'endFeet':50,'condition':'damaged'}]
    c.check(issue,'recovered original Line sections admit splice repair without new span',x.quote()['successHP']==5)
    c.keep('e10-recovered-original-Line-splice',x)
    part['recoveredOriginalSections'][1]['startFeet']=24
    c.reject(issue,'missing original Line foot prevents repair',x.quote)
    part['recoveredOriginalSections'][1]['startFeet']=22
    c.reject(issue,'overlap cannot duplicate original Line material',x.quote)
    part['recoveredOriginalSections'][1]['startFeet']=23
    part['recoveredOriginalSections'][1]['originalConstituentId']='replacement-span'
    c.reject(issue,'replacement Line section cannot stand for missing original span',x.quote)
    x=CraftFixture('recipe-171',repair=True)
    c.reject(issue,'actual Bait body still has no repair route',x.quote)


def move_capture(fixture,checkpoint,intervals=None):
    """Move the synthetic receiving checkpoint and all its contemporaneous views."""
    old=fixture.cpl
    for record in fixture.records.values():
        if record['checkpoint']==old:record['checkpoint']=list(checkpoint)
    fixture.cpl=list(checkpoint)
    placement=fixture.records[fixture.records[fixture.capture]['captureEvidenceId']]
    if intervals is not None:fixture.records[placement['retrievalWorkEvidenceId']]['intervals']=deepcopy(intervals)


def attempt_clocks(c):
    issue='FI-E02'
    x=Fixture(bait=True);ledger=x.run();a=ledger.state['attempts'][x.aid]
    c.check(issue,'dry setup0 exposure5 check55 secure60 expiry65 use distinct clocks',
        a['startedAt'][0]==0 and a['committedAt'][0]==300 and a['checkAt'][0]==3300 and
        x.records[a['captureEvidenceId']]['checkpoint'][0]==3600 and ledger.state['due']['bait:'+x.aid]['at'][0]==3900)
    c.check(issue,'attended closure remains minute65 with its own ordered checkpoint',ledger.state['due']['closure:'+x.aid]['at']==tuple(x.closure))
    c.keep('e02-dry-setup-five-minute-exposure',x)
    for method in ('Rod','Net','Trap'):
        x=Fixture(method=method)
        c.check(issue,method+' completes distinct setup and fishing/soak phases',x.run().state['attempts'][x.aid]['state']=='captured')
        x.records[x.setup_work]['intervals']=[{'startSeconds':3000,'endSeconds':3300,'hands':2,'actions':50}]
        ledger=x.run('commit')
        c.reject(issue,method+' cannot move setup to minutes50–55',lambda:ledger.apply(x.world(),x.check,1),ledger)
    x=Fixture(method='Trap');x.records[x.soak]['startSeconds']=0
    c.reject(issue,'Trap soak cannot absorb its separate setup phase',lambda:x.run())
    x=Fixture(method='Trap');x.records[x.soak]['disposition']='interrupted-deployment'
    c.reject(issue,'interrupted Trap soak cannot claim continuous fifty minutes',lambda:x.run())
    x=Fixture();x.records[x.work]['intervals'][0]['startSeconds']=0
    c.reject(issue,'fishing phase cannot count setup again',lambda:x.run())
    x=Fixture();x.records[x.commit]['checkCheckpoint']=[3600,0,0]
    c.reject(issue,'later exposure cannot restart the check clock',lambda:x.run('commit'))
    x=Fixture(bait=True);x.records[x.commit]['baitExpiryCheckpoint']=[3600,0,0]
    c.reject(issue,'receipt cannot expire sixty minutes from dry setup instead of exposure',lambda:x.run('commit'))
    x=Fixture(exposure_offset=301)
    c.reject(issue,'first deployment cannot slide beyond the fixed setup phase',lambda:x.run('commit'))

    x=Fixture(bait=True);cp=[120,0,0]
    work=x.add('cancel-work','work-record',cp,attemptId=x.aid,worker=x.lead,phase='setup',
        intervals=[{'startSeconds':0,'endSeconds':120,'hands':2,'actions':20}])
    resources=x.records[x.reservation]['reservedResourceIds']
    disposition=x.add('cancel-disposition','fishing-reservation-disposition',cp,
        reservationEvidenceId=x.reservation,attemptId=x.aid,lead=x.lead,status='cancelled-before-exposure',
        releasedOpportunityId=x.records[x.opportunity]['opportunityId'],releasedUnspentResourceIds=resources,spentOrDestroyedResourceIds=[])
    cancel=x.add('cancel','fishing-transition',cp,operation='cancel-setup',attemptId=x.aid,lead=x.lead,
        reservationEvidenceId=x.reservation,reservationDispositionEvidenceId=disposition,workEvidenceId=work)
    ledger=ref.FishingLedger(CARDS);ledger.apply(x.world(),cancel,0)
    record=ledger.state['preExposureCancellations'][x.aid]
    c.check(issue,'pre-exposure cancellation preserves120seconds and releases only unspent reservations',
        record['workedSeconds']==120 and x.bid in record['releasedUnspentResourceIds'] and
        not ledger.state['opportunities'] and not ledger.state['baitUses'] and not ledger.state['due'] and record['inventoryCreated']==[])
    c.reject(issue,'cancelled reservation cannot later be committed',lambda:ledger.apply(x.world(),x.commit,1),ledger)
    c.keep('e02-cancelled-before-exposure',x)
    broken=x.bid;x.records[disposition]['releasedUnspentResourceIds']=[r for r in resources if r!=broken]
    x.records[disposition]['spentOrDestroyedResourceIds']=[broken]
    ledger=ref.FishingLedger(CARDS);ledger.apply(x.world(),cancel,0)
    c.check(issue,'pre-exposure material damage is preserved without reconstructing an unused dose',
        ledger.state['preExposureCancellations'][x.aid]['spentOrDestroyedResourceIds']==[broken] and
        broken not in ledger.state['preExposureCancellations'][x.aid]['releasedUnspentResourceIds'])
    x.records[disposition]['releasedUnspentResourceIds'].append(broken)
    c.reject(issue,'cancellation cannot both lose and release the same material',lambda:ref.FishingLedger(CARDS).apply(x.world(),cancel,0))

    x=Fixture(bait=True);ledger=x.run('commit');cp=[600,0,0]
    x.records[x.close]['checkpoint']=cp
    disp=x.records[x.records[x.close]['dispositionEvidenceId']];disp['checkpoint']=cp;disp['reason']='abandoned'
    ledger.apply(x.world(),x.close,1)
    c.check(issue,'postcommit interruption keeps spent opportunity and bait',
        ledger.state['opportunities']==[x.records[x.opportunity]['opportunityId']] and ledger.state['baitUses']==[x.bid] and
        ledger.state['reservationHistory'][x.reservation]['outcome']=='committed' and ledger.state['attempts'][x.aid]['state']=='closed')
    c.reject(issue,'abandoned attempt cannot claim its original later catch check',lambda:ledger.apply(x.world(),x.check,2),ledger)

    for expiry_first in (True,False):
        x=Fixture(bait=True,bait_number=198,exposure_offset=0)
        x.expiry=[3600,0 if expiry_first else 1,0]
        x.records[x.expire]['checkpoint']=list(x.expiry)
        x.records[x.commit]['baitExpiryCheckpoint']=list(x.expiry)
        x.records[x.bait_exposure]['expiresAt']=list(x.expiry)
        for v in x.views.values():x.records[v['states'][x.bid]]['expiresAt']=list(x.expiry)
        move_capture(x,[3600,1 if expiry_first else 0,0])
        ledger=x.run()
        c.check(issue,('expiry before capture' if expiry_first else 'capture before expiry')+' at same timestamp respects authoritative phases',
            ledger.state['recoveries'][x.creature]['sourceExtra']==(2 if expiry_first else 3))
        c.keep('e02-same-time-'+('expiry-first' if expiry_first else 'capture-first'),x)
    x=Fixture(numbers=[179,641,164,642]);ledger=x.run('commit')
    c.check(issue,'separate Rig mounting precedes main setup without changing its clock',
        ledger.state['attempts'][x.aid]['startedAt'][0]==0 and x.records[next(iter(x.records[x.reservation]['rigMountWorkByPhysicalId'].values()))]['intervals'][0]['endSeconds']==0)
    mount=x.records[next(iter(x.records[x.reservation]['rigMountWorkByPhysicalId'].values()))]
    mount['intervals']=[{'startSeconds':0,'endSeconds':300,'hands':2,'actions':50}]
    c.reject(issue,'Rig mounting cannot reuse the main five-minute setup',lambda:x.run('commit'))


def physical_bindings(c):
    issue='FI-E03'
    for label in ('check','capture'):
        x=Fixture();sid=x.views[label]['states']['A-item-641'];x.records[sid]['currentHP']=0
        x.records[x.views[label]['admission']]['apparatusStateIds'].remove(sid)
        if label=='check':x.records[x.resolution]['equipmentBonus']=1;x.sync_core()
        ledger=x.run('commit' if label=='check' else 'check')
        event=x.check if label=='check' else x.capture
        c.reject(issue,label+' cannot omit Broken indispensable Line',lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)
    x=Fixture();x.records[x.manifest]['bodyMassLb']=12
    c.reject(issue,'twelve-pound manifest cannot borrow six-pound admission',lambda:x.run('commit'))
    for label in ('deploy','check','capture'):
        for field,value in [('physicalId','another-fish'),('attemptId','another-attempt'),('preyMassLb',5),
                ('preyVolumeCubicFeet',.1),('preyGeometry',{'lengthInches':1})]:
            x=Fixture();x.records[x.views[label]['admission']][field]=value
            c.reject(issue,label+' binds actual creature/admission '+field,lambda:x.run())
    x=Fixture();view=x.records[x.views['check']['view']]
    view['items']=[i for i in view['items'] if i['physicalId']!='A-item-641']
    x.records[x.resolution]['equipmentBonus']=1;x.sync_core()
    c.reject(issue,'missing strongest registered candidate is not proof of ineligibility',lambda:x.run())
    x=Fixture();view=x.records[x.views['capture']['view']];view['items'].pop()
    c.reject(issue,'missing weaker registered candidate also fails complete current coverage',lambda:x.run())
    x=Fixture();state=x.records[x.views['check']['states']['A-item-641']]
    other=deepcopy(state);other.pop('id');other.pop('kind');other.pop('checkpoint');other['currentHP']=0
    sid=x.add('conflicting-line-state','item-state',x.cpc,**other)
    next(i for i in x.records[x.views['check']['view']]['items'] if i['physicalId']=='A-item-641')['stateEvidenceId']=sid
    x.records[x.resolution]['equipmentBonus']=1;x.sync_core()
    c.reject(issue,'physical and magic views cannot cherry-pick contradictory current states',lambda:x.run())
    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]
    x.records[cap['retrievalWorkEvidenceId']]['worker']='assistant'
    c.reject(issue,'assistant work cannot substitute for lead retrieval',lambda:x.run())
    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]
    x.records[cap['retrievalWorkEvidenceId']]['intervals'][0]['hands']=1
    c.reject(issue,'lead still needs both actual retrieval hands',lambda:x.run())
    x=Fixture()
    for view in x.views.values():
        for sid in view['states'].values():x.records[sid]['suppressed']=True
    x.select_attraction(None);x.records[x.resolution]['equipmentBonus']=0;x.sync_core()
    ledger=x.run()
    c.check(issue,'suppressed complete apparatus remains physically usable with zero magic',
        ledger.state['attempts'][x.aid]['state']=='captured' and ledger.state['recoveries'][x.creature]['sourceExtra']==0)
    c.keep('e03-suppressed-functional-apparatus',x)
    x=Fixture();x.records[x.views['capture']['states']['A-item-641']]['suppressed']=True
    c.check(issue,'weaker still-qualified source supplies recovery after strongest suppression',x.run().state['recoveries'][x.creature]['sourceExtra']==1)
    x=Fixture();intervals=[{'startSeconds':3300,'endSeconds':3420,'hands':2,'actions':20},
        {'startSeconds':3480,'endSeconds':3660,'hands':2,'actions':30}]
    move_capture(x,[3660,0,0],intervals)
    c.check(issue,'interrupted retrieval retains five actual minutes before closure',x.run().state['attempts'][x.aid]['state']=='captured')
    c.keep('e03-interrupted-timely-retrieval',x)
    x=Fixture();ordinary='A-item-641'
    x.gear[ordinary]=None;x.records[x.reservation]['itemRecipeIds'][ordinary]=None
    for view in x.views.values():
        assembly=x.records[view['assembly']];assembly['itemRecipeIds'][ordinary]=None
        x.records[view['view']]['items']=[i for i in x.records[view['view']]['items'] if i['physicalId']!=ordinary]
    x.records[x.resolution]['equipmentBonus']=1;x.sync_core()
    c.check(issue,'ordinary unenchanted Line remains indispensable while producing no magic',x.run().state['recoveries'][x.creature]['sourceExtra']==1)
    x.records[x.views['check']['states'][ordinary]]['currentHP']=0
    c.reject(issue,'ordinary unenchanted indispensable Line must still function',lambda:x.run())


def bait_expenditure(c):
    issue='FI-E04'
    x=Fixture(bait=True,bait_number=198);x.records[x.commit]['baitId']=None
    ledger=ref.FishingLedger(CARDS)
    c.reject(issue,'undeclared +3 Bait cannot contribute without journal expenditure',lambda:ledger.apply(x.world(),x.commit,0),ledger)
    x=Fixture(numbers=[179,641,164,160,198]);ledger=x.run()
    c.check(issue,'registered but unexposed Bait supplies no contribution or receipt',
        not ledger.state['baitUses'] and ledger.state['recoveries'][x.creature]['sourceExtra']==2 and
        'bait:'+x.aid not in ledger.state['due'])
    x=Fixture(bait=True,bait_number=198);ledger=x.run('close')
    debit=ledger.state['baitDebits'][x.bid]
    c.check(issue,'one actual dose debit binds physical source recipe assembly exposure expiry and age',
        ledger.state['baitUses']==[x.bid] and debit['recipeId']=='recipe-198' and debit['assemblyId']==x.assembly_id and
        debit['exposureEvidenceId']==x.bait_exposure and debit['unprotectedAgeSecondsAtExposure']==82800 and
        debit['expiresAt'][0]-debit['exposedAt'][0]==3600)
    c.keep('e04-source-bound-consumed-dose',x)
    x=Fixture(bait=True);ledger=x.run('commit')
    exposure=x.records[x.bait_exposure];exposure['checkpoint']=[301,0,0];exposure['expiresAt']=[3901,0,0]
    x.records[x.bait_use]['checkpoint']=[301,0,0]
    for view in x.views.values():
        x.records[view['states'][x.bid]]['exposedAt']=[301,0,0]
        x.records[view['states'][x.bid]]['expiresAt']=[3901,0,0]
    c.reject(issue,'later matching receipt views cannot rewrite the original journal debit clock',lambda:ledger.apply(x.world(),x.check,1),ledger)
    x=Fixture(bait=True,bait_number=198)
    presentation=x.records[x.records[x.views['deploy']['assembly']]['presentationEvidenceId']]
    presentation['sources']=[s for s in presentation['sources'] if s['form']=='Lure']
    presentation['sourcePhysicalIds']=[s['physicalId'] for s in presentation['sources']]
    presentation['forms']=[s['form'] for s in presentation['sources']];presentation['ordinaryBaitLotIds']=[]
    c.reject(issue,'exposed dose cannot borrow an assembly while absent from its physical presentation',lambda:x.run('commit'))
    x=Fixture(bait=True,bait_number=198);ledger=x.run('close')
    y=Fixture(prefix='B',start=4000,creature='fish-B',lead='angler-B',bait=True,bait_number=198)
    y.records=json.loads(json.dumps(y.records).replace(y.bid,x.bid))
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    c.reject(issue,'closed attempt never refunds a consumed dose to another assembly',lambda:ledger.apply(both,y.commit,ledger.state['version']),ledger)
    for key,field,value in [('exposure','recipeId','recipe-162'),('exposure','assemblyId','another-assembly'),
            ('exposure','physicalId','another-dose'),('use','physicalId','another-dose'),('use','carrierLb',.05),
            ('use','purpose','crafting-process-input')]:
        x=Fixture(bait=True,bait_number=198);x.records[x.bait_exposure if key=='exposure' else x.bait_use][field]=value
        c.reject(issue,'receipt/debit must bind '+key+' '+field,lambda:x.run('commit'))
    for field,value in [('receiptAttemptId','another-attempt'),('exposureEvidenceId','copied-receipt'),('expiresAt',[9999,0,0])]:
        x=Fixture(bait=True);x.records[x.views['capture']['states'][x.bid]][field]=value
        c.reject(issue,'current Bait view cannot substitute '+field,lambda:x.run())
    x=Fixture(bait=True,bait_number=198)
    state=x.records[x.views['capture']['states'][x.bid]]
    state.update({'currentHP':0,'complete':False,'participatingAttemptId':None})
    c.check(issue,'ordinary swallowing preserves valid attempt receipt after carrier is gone',x.run().state['recoveries'][x.creature]['sourceExtra']==3)
    c.keep('e04-swallowed-dose-receipt-survives',x)
    x=Fixture(bait=True,bait_number=198)
    state=x.records[x.views['capture']['states'][x.bid]];state['assemblyBaitSuppressed']=True
    x.records[state['baitEffectStateEvidenceId']]['suppressed']=True
    c.check(issue,'actual assembly bait suppression removes only that receipt benefit',x.run().state['recoveries'][x.creature]['sourceExtra']==2)
    x.records[state['baitEffectStateEvidenceId']]['assemblyId']='nearby-unrelated-object'
    c.reject(issue,'nearby object suppression cannot stand in for assembly bait scope',lambda:x.run())
    x=Fixture(bait=True,bait_number=198,exposure_offset=0);ledger=x.run()
    c.check(issue,'expired receipt grants no current bonus or recovery despite original valid debit',
        x.bid not in ref.effect_candidates(x.world(),x.views['capture']['view'],CARDS)['eligibleIds'] and
        ledger.state['recoveries'][x.creature]['sourceExtra']==2 and x.bid in ledger.state['baitDebits'])

    x=Fixture();presentation=x.records[x.records[x.views['deploy']['assembly']]['presentationEvidenceId']]
    lure=next(s for s in presentation['sources'] if s['form']=='Lure')
    old=lure['physicalId'];lure['physicalId']='A-item-179'
    presentation['sourcePhysicalIds']=[s['physicalId'] for s in presentation['sources']]
    x.records[lure['useEvidenceId']]['physicalId']='A-item-179'
    c.reject(issue,'Rod cannot acquire Lure form through a matching presentation list',lambda:x.run('commit'))
    for field,value in [('stockClass','consumed-recipe-bait-component'),('state','consumed'),
            ('materialCondition','Spoiled'),('massLb',.09),('physicalId','another-portion')]:
        x=Fixture();x.records['A-ordinary-stock'][field]=value
        c.reject(issue,'ordinary portion requires actual eligible inventory '+field,lambda:x.run('commit'))
    x=Fixture();x.records['A-ordinary-use']['locationKind']='rig-chum'
    c.reject(issue,'Rig chum cannot also stand in for Rod hook bait location',lambda:x.run('commit'))
    x=Fixture();x.records['A-ordinary-use']['locationId']='another-hook'
    c.reject(issue,'ordinary portion must occupy this actual presentation point',lambda:x.run('commit'))
    x=Fixture();ledger=x.run('close')
    y=Fixture(prefix='B',start=4000,creature='fish-B',lead='angler-B')
    y.records=json.loads(json.dumps(y.records).replace('B-ordinary-bait-lot','A-ordinary-bait-lot'))
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    c.reject(issue,'one ordinary portion cannot be exposed again for another attempt',lambda:ledger.apply(both,y.commit,ledger.state['version']),ledger)

    x=Fixture(bait=True);cp=x.cp0;completed=x.records[x.bait_completion]['checkpoint']
    stages=[(completed,[cp[0]-7200,0,0],'wrapped','original-holder'),
        ([cp[0]-7200,0,0],[cp[0]-3600,0,0],'unwrapped','original-holder'),
        ([cp[0]-3600,0,0],[cp[0]-1800,0,0],'rewrapped','original-holder'),
        ([cp[0]-1800,0,0],cp,'wrapped','new-holder')]
    x.records[x.bait_storage]['intervals']=[{'start':a,'end':b,'preservationEvidenceId':None,'storageForm':form,'holderId':holder} for a,b,form,holder in stages]
    dose,age=ref.unused_bait_qualification(x.world(),x.records[x.commit]['baitEvidenceId'],cp)
    c.check(issue,'unwrap rewrap and transfer retain all23 accumulated unprotected hours',age==82800 and dose['quantity']==1)
    c.check(issue,'unwrapping before exposure creates no prior journal debit',x.run('commit').state['baitUses']==[x.bid])
    c.keep('e04-unwrapped-rewrapped-transferred-age',x)
    x.records[x.records[x.commit]['baitEvidenceId']]['unprotectedHours']=0
    c.reject(issue,'transfer cannot reset dose age while retaining its original history',lambda:x.run('commit'))
    x=Fixture(bait=True);start=[x.cp0[0]-86400,0,0]
    x.records[x.bait_completion]['checkpoint']=start;x.records[x.bait_storage]['intervals'][0]['start']=start
    x.records[x.records[x.commit]['baitEvidenceId']]['unprotectedHours']=24
    c.reject(issue,'24 accumulated unprotected hours spoils even a freshly rewrapped dose',lambda:x.run('commit'))
    x=Fixture(bait=True);x.records[x.bait_storage]['intervals'][0]['start'][0]+=60
    c.reject(issue,'missing minute of storage history cannot disappear from age',lambda:x.run('commit'))
    x=Fixture(bait=True);x.records[x.bait_completion]['physicalId']='another-dose'
    c.reject(issue,'fresh completion of another physical dose cannot reset this one',lambda:x.run('commit'))
    x=Fixture(bait=True);x.records[x.records[x.commit]['baitEvidenceId']]['condition']='destroyed'
    c.reject(issue,'destroyed unused dose cannot create a receipt',lambda:x.run('commit'))
    x=Fixture(bait=True);end=[x.cp0[0]-82800,0,0];start=[x.cp0[0]-90000,0,0]
    x.records[x.bait_completion]['checkpoint']=start
    preservation=x.add('compatible-storage','compatible-bait-preservation',start,physicalId=x.bid,
        recipeId=x.gear[x.bid],effectiveUntil=end,existingProcedureRef='synthetic independently governed compatible preservation premise; no new game method',disposition='compatible-active')
    x.records[x.bait_storage]['intervals']=[{'start':start,'end':end,'preservationEvidenceId':preservation},
        {'start':end,'end':x.cp0,'preservationEvidenceId':None}]
    c.check(issue,'actually compatible protected interval changes only accumulated unprotected age',
        x.run('commit').state['baitDebits'][x.bid]['unprotectedAgeSecondsAtExposure']==82800)
    x.records[preservation]['physicalId']='another-dose'
    c.reject(issue,'another dose preservation cannot protect this physical bait history',lambda:x.run('commit'))


def rig_retrieval_event(x,*,checkpoint=None,work_start=None):
    cp=checkpoint or [x.start+3901,0,0];start=x.start+3601 if work_start is None else work_start
    ident=x.rig['physicalId']
    work=x.add('rig-retrieval-work','work-record',cp,attemptId=x.aid,physicalId=ident,worker=x.lead,phase='rig-retrieval',
        intervals=[{'startSeconds':start,'endSeconds':start+300,'hands':2,'actions':50}])
    admission=x.add('rig-retrieval-admission','rig-handling-admission',cp,attemptId=x.aid,dispenserPhysicalId=ident,
        worker=x.lead,disposition='admitted',pathDisposition='admitted',handledMassLb=1.5,handlingCapacityLb=10,
        receivingLocationId=x.p+'-rig-rack')
    disposition=x.add('rig-retrieval-disposition','rig-disposition',cp,attemptId=x.aid,dispenserPhysicalId=ident,
        reason='retrieved',locationId=x.p+'-rig-rack',elevationFeet=2,workEvidenceId=work,handlingEvidenceId=admission)
    event=x.add('rig-retrieval-event','fishing-transition',cp,attemptId=x.aid,operation='reconcile-rig',rigDispositionEvidenceId=disposition)
    return event,work,admission,disposition


def bait_into_rig(x):
    """One real dose replaces .10 lb chum; Rod retains its separate actual Lure."""
    for key in (x.bait_exposure,x.bait_use):
        x.records[key].update({'locationKind':'rig-chum','locationId':x.p+'-rig-point'})
    x.records[x.rig['stock']]['massLb']=.9
    x.records[x.rig['load']].update({'finishedBaitPhysicalId':x.bid,'finishedBaitExposureEvidenceId':x.bait_exposure,'finishedBaitCarrierLb':.1})
    x.records[x.rig['deployment']].update({'finishedBaitPhysicalId':x.bid,'finishedBaitExposureEvidenceId':x.bait_exposure})
    x.records[x.rig['use']]['finishedBaitPhysicalId']=x.bid
    for view in x.views.values():
        presentation=x.records[x.records[view['assembly']]['presentationEvidenceId']]
        presentation['sources']=[s for s in presentation['sources'] if s['form']!='finished-Bait']
        presentation['sourcePhysicalIds']=[s['physicalId'] for s in presentation['sources']]
        presentation['forms']=[s['form'] for s in presentation['sources']]
        presentation['ordinaryBaitLotIds']=[s['physicalId'] for s in presentation['sources'] if s['form']=='ordinary-bait']


def rig_operations(c):
    issue='FI-E05';numbers=[179,182,164,160,642]
    x=Fixture(numbers=numbers);x.select_attraction(x.rig['physicalId']);ledger=x.run('close')
    a=ledger.state['attempts'][x.aid]
    c.check(issue,'fully bound Rig alone supplies strongest +2 catch and recovery',
        x.records[x.resolution]['equipmentBonus']==2 and ledger.state['recoveries'][x.creature]['sourceExtra']==2 and
        a['attractionPhysicalId']==x.rig['physicalId'] and len(ledger.state['chumUseIds'])==1)
    c.check(issue,'closing catch leaves deployed Rig in actual location with handling still due',
        a['state']=='closed' and a['rigHandling']['state']=='deployed' and a['rigHandling']['locationId']==x.p+'-rig-point' and
        ledger.state['equipmentReservations'].get(x.rig['physicalId'])==x.aid and a['rigHandling']['inventoryCreated']==[])
    c.keep('e05-complete-Rig-deployment',x)
    prior=deepcopy(ledger.state['recoveries']);event,work,admission,disposition=rig_retrieval_event(x)
    ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'own five-minute Rig retrieval reconciles actual receiving disposition without new catch',
        ledger.state['attempts'][x.aid]['rigHandling']['state']=='retrieved' and
        ledger.state['attempts'][x.aid]['rigHandling']['locationId']==x.p+'-rig-rack' and
        x.rig['physicalId'] not in ledger.state['equipmentReservations'] and ledger.state['recoveries']==prior and
        len(ledger.state['chumUseIds'])==1)
    c.reject(issue,'Rig retrieval cannot be replayed for another body or inventory entry',lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)
    c.keep('e05-separate-Rig-retrieval',x)
    for field,value in [('loadEvidenceId',None),('supportEvidenceId',None),('mountWorkEvidenceId',None)]:
        x=Fixture(numbers=numbers);x.records[x.rig['deployment']][field]=value
        c.reject(issue,'Rig requires actual '+field,lambda:x.run('commit'))
    for field,value in [('massLb',.9),('state','already-spent'),('materialCondition','Spoiled')]:
        x=Fixture(numbers=numbers);x.records[x.rig['stock']][field]=value
        c.reject(issue,'ordinary chum stock rejects '+field,lambda:x.run('commit'))
    for field,value in [('occupiedVolumePints',1.1),('totalMassLb',.9),('wrapperMassIncludedLb',.01),('compatibility','incompatible')]:
        x=Fixture(numbers=numbers);x.records[x.rig['load']][field]=value
        c.reject(issue,'Rig load rejects '+field,lambda:x.run('commit'))
    for field,value in [('tetherPathFeet',11),('distanceToAssemblyPointFeet',6),('supportPhysicalId',None),
            ('disposition','unsupported'),('assemblyPointId','another-hook')]:
        x=Fixture(numbers=numbers);x.records[x.rig['supports']['deploy']][field]=value
        c.reject(issue,'Rig deployment rejects '+field,lambda:x.run('commit'))
    x=Fixture(numbers=numbers);x.records[x.rig['use']]['disposition']='not-opened'
    c.reject(issue,'unopened chum cannot claim committed dispersal benefits',lambda:x.run('commit'))
    x=Fixture(numbers=numbers);portion='A-ordinary-bait-lot'
    x.records[x.rig['stock']]['physicalId']=portion;x.records[x.rig['use']]['ordinaryPortionIds']=[portion]
    c.reject(issue,'one actual portion cannot fill both hook and Rig',lambda:x.run('commit'))
    x=Fixture(numbers=numbers);ledger=x.run('close')
    y=Fixture(numbers=numbers,prefix='B',start=4000,lead='angler-B',creature='fish-B')
    y.records=json.loads(json.dumps(y.records).replace(y.rig['portionId'],x.rig['portionId']))
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    c.reject(issue,'spent chum cannot fill a later Rig deployment',lambda:ledger.apply(both,y.commit,ledger.state['version']),ledger)
    y=Fixture(prefix='C',start=4000,lead='angler-C',creature='fish-C')
    y.records=json.loads(json.dumps(y.records).replace('C-ordinary-bait-lot',x.rig['portionId']))
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    c.reject(issue,'Rig residue cannot return as usable ordinary bait',lambda:ledger.apply(both,y.commit,ledger.state['version']),ledger)

    x=Fixture(numbers=numbers,bait=True,bait_number=198);bait_into_rig(x);ledger=x.run()
    c.check(issue,'one finished dose replaces .10 lb while .90 lb ordinary chum and separate Lure remain',
        ledger.state['baitUses']==[x.bid] and len(ledger.state['chumUses'])==1 and
        ledger.state['attempts'][x.aid]['rigBinding']['load']['wrapperMassIncludedLb']==0)
    c.keep('e05-finished-Bait-substitution',x)
    x.records[x.rig['stock']]['massLb']=.8
    c.reject(issue,'finished Bait does not replace the remaining nine tenths pound',lambda:x.run('commit'))
    x=Fixture(numbers=numbers,bait=True,bait_number=198);bait_into_rig(x)
    presentation=x.records[x.records[x.views['deploy']['assembly']]['presentationEvidenceId']]
    presentation['sources'].append({'physicalId':x.bid,'form':'finished-Bait','useEvidenceId':x.bait_exposure})
    presentation['forms']=[s['form'] for s in presentation['sources']];presentation['sourcePhysicalIds']=[s['physicalId'] for s in presentation['sources']]
    c.reject(issue,'same finished dose cannot also occupy the hook while in Rig chum',lambda:x.run('commit'))

    for mode in ('suppressed','broken'):
        x=Fixture(numbers=numbers)
        for label in ('check','capture'):
            body=x.records[x.views[label]['states'][x.rig['physicalId']]]
            if mode=='suppressed':body['suppressed']=True
            else:
                body['currentHP']=0;x.records[x.rig['states'][label]]['disposition']='spilled'
        x.records[x.resolution]['equipmentBonus']=1;x.sync_core();ledger=x.run()
        c.check(issue,mode+' Rig loses benefits while body location and original spent allotment persist',
            ledger.state['recoveries'][x.creature]['sourceExtra']==1 and len(ledger.state['chumUseIds'])==1 and
            ledger.state['attempts'][x.aid]['rigHandling']['locationId']==x.p+'-rig-point')
        c.keep('e05-'+mode+'-Rig',x)
    x=Fixture(numbers=numbers)
    for label in x.views:x.records[x.views[label]['states'][x.rig['physicalId']]]['suppressed']=True
    x.records[x.resolution]['equipmentBonus']=1;x.sync_core();ledger=x.run()
    c.check(issue,'suppressed but functional Rig can deploy with actual load and no magic',
        ledger.state['recoveries'][x.creature]['sourceExtra']==1 and len(ledger.state['chumUseIds'])==1)
    x=Fixture(numbers=numbers);x.records[x.views['deploy']['states'][x.rig['physicalId']]]['currentHP']=0
    x.records[x.rig['states']['deploy']]['disposition']='spilled'
    c.reject(issue,'already Broken dispenser cannot claim a functional initial deployment',lambda:x.run('commit'))
    x=Fixture(numbers=numbers);x.records[x.views['check']['states'][x.rig['physicalId']]]['currentHP']=0
    x.records[x.rig['states']['check']]['disposition']='spilled';x.records[x.resolution]['equipmentBonus']=1;x.sync_core()
    c.reject(issue,'repairing an emptied spilled Rig cannot invent a fresh chum allotment',lambda:x.run())
    x=Fixture(numbers=numbers);x.records[x.views['check']['states'][x.rig['physicalId']]]['suppressed']=True
    x.records[x.resolution]['equipmentBonus']=1;x.sync_core();ledger=x.run()
    c.check(issue,'later restored Rig magic cannot enlarge prior-check recovery or refill chum',
        ledger.state['recoveries'][x.creature]['sourceExtra']==1 and len(ledger.state['chumUseIds'])==1)

    for fault in ('missing-work','borrowed-catch-work','one-hand','wrong-body','insufficient-capacity'):
        x=Fixture(numbers=numbers);ledger=x.run('close')
        event,work,admission,disposition=rig_retrieval_event(x,work_start=3300 if fault=='borrowed-catch-work' else None)
        if fault=='missing-work':x.records[disposition]['workEvidenceId']=None
        if fault=='one-hand':x.records[work]['intervals'][0]['hands']=1
        if fault=='wrong-body':x.records[work]['physicalId']='another-Rig'
        if fault=='insufficient-capacity':x.records[admission]['handlingCapacityLb']=1
        c.reject(issue,'Rig retrieval rejects '+fault,lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)
    x=Fixture(numbers=numbers);ledger=x.run('close');cp=[3700,0,0]
    disposition=x.add('abandon-Rig','rig-disposition',cp,attemptId=x.aid,dispenserPhysicalId=x.rig['physicalId'],
        reason='abandoned',locationId=x.p+'-rig-point',elevationFeet=-2)
    event=x.add('abandon-Rig-event','fishing-transition',cp,attemptId=x.aid,operation='reconcile-rig',rigDispositionEvidenceId=disposition)
    ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'express Rig abandonment preserves location and spent chum without carried inventory',
        ledger.state['attempts'][x.aid]['rigHandling']['state']=='abandoned' and
        ledger.state['attempts'][x.aid]['rigHandling']['inventoryCreated']==[] and len(ledger.state['chumUseIds'])==1)


def trap_disposition_event(x, reason, cp, *, captured=False, receiver='holder-B', worker='retriever-C', key='handling'):
    ident=next(i for i,rid in x.gear.items() if CARDS[rid]['sourceRecipe']['recipeFamily']=='Trap')
    capture=x.records[x.check]['captureEvidenceId'] if captured else None
    location=x.add(key+'-state','trap-disposition-state',cp,attemptId=x.aid,trapPhysicalId=ident,
        apparatusLocationId=x.p+('-receiving-rack' if reason=='retrieved' else '-trap-site'),
        apparatusElevationFeet=0 if reason=='retrieved' else -3,
        apparatusDisposition=reason if reason in ('retrieved','abandoned') else 'deployed',
        captureEvidenceId=capture,catchPhysicalId=x.creature if captured else None,
        catchLocationId=('actual-receiving-tub' if reason=='retrieved' else 'actual-Trap-interior') if captured else None,
        catchElevationFeet=0 if captured else None,lifeState='alive' if captured else None,
        custody=('escaped' if reason=='escaped' else 'contained') if captured else None)
    disposition=x.add(key+'-disposition','actual-disposition',cp,attemptId=x.aid,physicalId=x.creature,
        reason=reason,trapStateEvidenceId=location)
    if reason=='retrieved':
        work=x.add(key+'-work','work-record',cp,attemptId=x.aid,physicalId=ident,worker=worker,phase='trap-retrieval',
            intervals=[{'startSeconds':cp[0]-300,'endSeconds':cp[0],'hands':2,'actions':50}])
        load=x.add(key+'-load','trap-handling-load',cp,attemptId=x.aid,trapPhysicalId=ident,
            trapStateEvidenceId=location,catchPhysicalId=x.creature if captured else None,
            apparatusMassLb=4.05,otherContentsMassLb=.1,catchMassLb=6 if captured else 0,catchTransported=captured,
            catchProfileEvidenceId=x.profile if captured else None)
        admission=x.add(key+'-admission','trap-handling-admission',cp,attemptId=x.aid,trapPhysicalId=ident,
            worker=worker,disposition='admitted',pathDisposition='admitted',recoveryPathFeet=15,
            loadEvidenceId=load,trapStateEvidenceId=location,handledMassLb=10.15 if captured else 4.15,handlingCapacityLb=20)
        x.records[disposition].update({'retrievalWorkEvidenceId':work,'handlingEvidenceId':admission})
    if reason=='lawful-handover':
        handover=x.add(key+'-handover','trap-handover',cp,attemptId=x.aid,trapPhysicalId=ident,
            fromActor=x.lead,toActor=receiver,opportunityId=x.records[x.opportunity]['opportunityId'],
            selectedCreatureId=x.creature,canonicalRollId=x.roll['id'],disposition='lawful-accepted',
            trapStateEvidenceId=location,setterConfigurationEvidenceId=x.config)
        x.records[disposition]['handoverEvidenceId']=handover
    event=x.add(key+'-event','fishing-transition',cp,operation='close',attemptId=x.aid,dispositionEvidenceId=disposition)
    return event


def trap_lifecycle(c):
    issue='FI-E06'
    x=Fixture(method='Trap');x.records[x.resolution]['degree']='Failure';x.sync_core();ledger=x.run()
    close=trap_disposition_event(x,'failed',[3350,0,0]);ledger.apply(x.world(),close,ledger.state['version'])
    a=ledger.state['attempts'][x.aid]
    c.check(issue,'failed claim closes while deployed Trap keeps allowance and gear reservation',
        a['state']=='closed' and not a['deploymentReconciled'] and a['responsibleActor']==x.lead and
        all(ledger.state['equipmentReservations'][g]==x.aid for g in x.gear))
    y=Fixture(prefix='second',start=3700,creature='fish-B')
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    c.reject(issue,'failed unretrieved Trap blocks another deployment by holder',lambda:ledger.apply(both,y.commit,ledger.state['version']),ledger)
    retrieve=trap_disposition_event(x,'retrieved',[3700,0,0],key='later-retrieval')
    ledger.apply(x.world(),retrieve,ledger.state['version'])
    c.check(issue,'actual empty Trap retrieval frees allowance without inventing selected prey or inventory',
        ledger.state['attempts'][x.aid]['deploymentReconciled'] and
        ledger.state['attempts'][x.aid]['trapHandling']['inventoryCreated']==[] and
        ledger.state['attempts'][x.aid]['creatureDisposition'] is None and not ledger.state['equipmentReservations'])
    both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    ledger.apply(both,y.commit,ledger.state['version'])
    c.check(issue,'holder can commit another actual opportunity after physical retrieval',y.aid in ledger.state['attempts'])
    c.keep('e06-failed-claim-and-later-actual-retrieval',x)

    x=Fixture(method='Trap',bait=True);ledger=x.run('commit')
    due=deepcopy(ledger.state['due']);before=deepcopy(ledger.state['attempts'][x.aid])
    handover=trap_disposition_event(x,'lawful-handover',[600,0,0]);ledger.apply(x.world(),handover,ledger.state['version'])
    a=ledger.state['attempts'][x.aid]
    c.check(issue,'pending handover retains original setter roll prey opportunity receipt and every scheduled event',
        a['responsibleActor']=='holder-B' and a['lead']==x.lead and a['state']=='committed' and
        a['canonicalRoll']==before['canonicalRoll'] and a['selectedCreatureId']==before['selectedCreatureId'] and
        a['opportunityId']==before['opportunityId'] and a['receiptActive'] and ledger.state['due']==due)
    y=Fixture(prefix='old-setter-new',start=700,creature='fish-B');both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    ledger.apply(both,y.commit,ledger.state['version'])
    c.check(issue,'lawful handover frees original setter while new holder keeps allowance',
        ledger.state['attempts'][y.aid]['responsibleActor']==x.lead and ref.FishingLedger._allowance_occupied(ledger.state,'holder-B'))
    ledger.apply(both,x.check,ledger.state['version'])
    c.check(issue,'handed-over Trap resolves original one-shot check using original setter and current gear',
        ledger.state['attempts'][x.aid]['state']=='captured' and ledger.state['attempts'][x.aid]['checkId']==x.roll['id'] and
        ledger.state['attempts'][x.aid]['setterBinding']['configuration']['personalContributions']=={'WIS':2,'Fishing':2})
    c.reject(issue,'handover never grants a second check',lambda:ledger.apply(both,x.check,ledger.state['version']),ledger)
    c.keep('e06-pending-handover-retains-one-original-check',x)

    x=Fixture(method='Trap');y=Fixture(prefix='occupied',start=100,lead='holder-B',creature='fish-B')
    handover=trap_disposition_event(x,'lawful-handover',[700,0,0]);both=ref.WorldEvidence({**x.records,**y.records},test_fixture=True)
    ledger=ref.FishingLedger(CARDS);ledger.apply(both,x.commit,0);ledger.apply(both,y.commit,1)
    c.reject(issue,'handover to occupied holder fails atomically with pending checks unchanged',lambda:ledger.apply(both,handover,2),ledger)
    for field,value in [('setterConfigurationEvidenceId','different-configuration'),('opportunityId','fresh-opportunity'),
            ('selectedCreatureId','replacement-fish'),('canonicalRollId','new-roll'),('fromActor','wrong-holder'),
            ('toActor',''),('disposition','not-accepted')]:
        x=Fixture(method='Trap');ledger=x.run('commit');event=trap_disposition_event(x,'lawful-handover',[600,0,0])
        disp=x.records[x.records[event]['dispositionEvidenceId']];x.records[disp['handoverEvidenceId']][field]=value
        c.reject(issue,'handover binds actual '+field,lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)
    x=Fixture(method='Trap');ledger=x.run('commit');event=trap_disposition_event(x,'lawful-handover',[600,0,0])
    ledger.apply(x.world(),event,ledger.state['version'])
    x.records[x.config]['personalContributions']['WIS']=4;x.records[x.credential]['wisModifier']=4
    x.records[x.resolution]['personalContributions']['WIS']=4;x.sync_core()
    c.reject(issue,'later matching dictionaries cannot rewrite original setter snapshot',lambda:ledger.apply(x.world(),x.check,ledger.state['version']),ledger)

    x=Fixture(method='Trap',bait=True);ledger=x.run('commit');spent=deepcopy(ledger.state['baitDebits'])
    event=trap_disposition_event(x,'abandoned',[600,0,0]);ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'express abandonment cancels pending check keeps actual location and refunds no bait or opportunity',
        not ledger.state['due'] and ledger.state['baitDebits']==spent and len(ledger.state['opportunities'])==1 and
        ledger.state['attempts'][x.aid]['trapHandling']['locationId']==x.p+'-trap-site' and
        ledger.state['attempts'][x.aid]['deploymentReconciled'])
    c.reject(issue,'abandoned deployment cannot resolve cancelled check',lambda:ledger.apply(x.world(),x.check,ledger.state['version']),ledger)
    x=Fixture(method='Trap');ledger=x.run();recovery=deepcopy(ledger.state['recoveries'])
    event=trap_disposition_event(x,'abandoned',[3400,0,0],captured=True);ledger.apply(x.world(),event,ledger.state['version'])
    animal=ledger.state['attempts'][x.aid]['creatureDisposition']
    c.check(issue,'abandoning captured Trap preserves living animal location identity and recovery history',
        animal['catchPhysicalId']==x.creature and animal['lifeState']=='alive' and animal['catchLocationId']=='actual-Trap-interior' and
        ledger.state['recoveries']==recovery)
    c.keep('e06-abandoned-Trap-retains-existing-animal',x)

    x=Fixture(method='Trap');ledger=x.run();event=trap_disposition_event(x,'retrieved',[3601,0,0],captured=True)
    ledger.apply(x.world(),event,ledger.state['version']);a=ledger.state['attempts'][x.aid]
    c.check(issue,'capable different retriever moves actual Trap and living catch after five minutes',
        a['deploymentReconciled'] and a['creatureDisposition']['catchLocationId']=='actual-receiving-tub' and
        a['trapHandling']['locationId']==x.p+'-receiving-rack' and a['trapHandling']['inventoryCreated']==[])
    c.keep('e06-capable-retriever-and-real-receiving-locations',x)
    c.reject(issue,'already retrieved Trap cannot be retrieved again',lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)
    for target,field,value in [('disposition','retrievalWorkEvidenceId',None),('disposition','handlingEvidenceId',None),
            ('work','worker',''),('work','physicalId','other-Trap'),('work','phase','setup'),
            ('span','hands',1),('span','startSeconds',3500),('admission','recoveryPathFeet',21),
            ('admission','pathDisposition','blocked'),('admission','handlingCapacityLb',5),
            ('admission','handledMassLb',4.15),('load','catchMassLb',0),
            ('location','apparatusLocationId',''),('location','catchLocationId',''),
            ('location','captureEvidenceId','another-capture')]:
        x=Fixture(method='Trap');ledger=x.run();event=trap_disposition_event(x,'retrieved',[3601,0,0],captured=True)
        disp=x.records[x.records[event]['dispositionEvidenceId']];work=x.records[disp['retrievalWorkEvidenceId']]
        adm=x.records[disp['handlingEvidenceId']]
        records={'disposition':disp,'work':work,'span':work['intervals'][0],'admission':adm,
            'load':x.records[adm['loadEvidenceId']],'location':x.records[disp['trapStateEvidenceId']]}
        records[target][field]=value
        c.reject(issue,'retrieved Trap requires actual '+target+' '+field,lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)

    x=Fixture(method='Trap');ledger=x.run('commit');event=trap_disposition_event(x,'failed',[600,0,0])
    c.reject(issue,'bare failed claim cannot cancel still-pending Trap check',lambda:ledger.apply(x.world(),event,ledger.state['version']),ledger)
    x=Fixture(method='Trap');ledger=x.run();event=trap_disposition_event(x,'finished',[3350,0,0],captured=True)
    ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'finished captured claim retains unresolved physical deployment and animal reservation',
        not ledger.state['attempts'][x.aid]['deploymentReconciled'] and ledger.state['creatureReservations'][x.creature]==x.aid)
    x=Fixture(method='Trap',numbers=[161,160,642]);ledger=x.run()
    event=trap_disposition_event(x,'retrieved',[3601,0,0],captured=True);ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'Trap retrieval does not silently retrieve attached Rig or refund its allotment',
        ledger.state['attempts'][x.aid]['rigHandling']['state']=='deployed' and
        ledger.state['equipmentReservations'][x.rig['physicalId']]==x.aid and len(ledger.state['chumUseIds'])==1)

    x=Fixture(method='Trap');ledger=x.run('commit');event=trap_disposition_event(x,'retrieved',[900,0,0])
    ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'early physical retrieval cancels pending check without capturing selected prey',
        not ledger.state['due'] and not ledger.state['recoveries'] and ledger.state['attempts'][x.aid]['deploymentReconciled'])
    x=Fixture(method='Trap');ledger=x.run();event=trap_disposition_event(x,'retrieved',[3601,0,0],captured=True)
    disp=x.records[x.records[event]['dispositionEvidenceId']];adm=x.records[disp['handlingEvidenceId']]
    loc=x.records[disp['trapStateEvidenceId']];load=x.records[adm['loadEvidenceId']]
    loc.update({'custody':'escaped','catchLocationId':'actual-water-location'})
    load.update({'catchTransported':False,'catchMassLb':0});adm['handledMassLb']=4.15
    ledger.apply(x.world(),event,ledger.state['version'])
    c.check(issue,'retrieving apparatus after escape preserves actual fish location without carrying it',
        ledger.state['attempts'][x.aid]['creatureDisposition']['catchLocationId']=='actual-water-location' and
        ledger.state['attempts'][x.aid]['creatureDisposition']['custody']=='escaped')
    x=Fixture(method='Trap');ledger=x.run('commit');event=trap_disposition_event(x,'lawful-handover',[600,0,0])
    ledger.apply(x.world(),event,ledger.state['version'])
    for key in x.views['check']['states'].values():x.records[key]['suppressed']=True
    x.records[x.resolution]['equipmentBonus']=0;x.sync_core();ledger.apply(x.world(),x.check,ledger.state['version'])
    c.check(issue,'handover keeps setter snapshot but uses then-current suppressed equipment',
        ledger.state['attempts'][x.aid]['checkEligible']=={} and ledger.state['recoveries'][x.creature]['sourceExtra']==0)


def material_successor_fixture(x, prior, key, cp):
    values=deepcopy(x.records[prior])
    for field in ('id','kind','checkpoint','transitionEvidenceIds'):values.pop(field,None)
    values['previousManifestEvidenceId']=prior
    return x.add(key,'material-manifest',cp,**values)


def material_transition_fixture(x, prior, current, *, lifecycle=None, allowed=False):
    before={u['id']:u for g in ref.MATERIAL_GROUPS for u in x.records[prior][g]}
    changes=[]
    for g in ref.MATERIAL_GROUPS:
        for u in x.records[current][g]:
            if u!=before[u['id']]:changes.append({'unitId':u['id'],'fromUnit':deepcopy(before[u['id']]),
                'toUnit':deepcopy(u),'lifecycleEvidenceId':lifecycle})
    ident=x.add('transition-'+current,'material-state-transition',x.records[current]['checkpoint'],
        physicalId=x.creature,fromManifestEvidenceId=prior,toManifestEvidenceId=current,
        unitChanges=changes,governingProcedure='Synthetic actual loss or separately governed condition treatment; no campaign permission granted',
        conditionChangeDisposition='lawful-under-governing-procedure' if allowed else None)
    x.records[current]['transitionEvidenceIds']=[ident]
    return ident


def harvest_fixture(x, *, cp=None):
    cp=cp or [7200,0,0]
    cap=x.records[x.check if x.method=='Trap' else x.capture]['captureEvidenceId']
    mid=material_successor_fixture(x,x.records[cap]['manifestEvidenceId'],'harvest-manifest',cp)
    lifecycle=x.add('harvest-lifecycle','material-lifecycle',[4000,0,0],physicalId=x.creature,
        eventKind='death',deathOrRemovalTime=4000,priorDeathOrRemovalTime=None,
        unitIds=[u['id'] for g in ref.MATERIAL_GROUPS for u in x.records[mid][g]],
        governingProcedure='Synthetic separately resolved lawful death; actual campaign authority is external')
    prerequisite=x.add('harvest-lawful','lawful-extraction',cp,physicalId=x.creature,deathOrRemovalTime=4000,
        lifecycleEvidenceId=lifecycle,governingProcedure='Independently resolved harvesting with actual access, tools and work')
    choice=x.add('harvest-choice','harvest-category-choice',[cp[0]-100,0,0],physicalId=x.creature,categories=['ordinary-fish-meat'])
    event=x.add('harvest','resolved-ordinary-harvest',cp,physicalId=x.creature,lawfulExtractionEvidenceId=prerequisite,
        manifestEvidenceId=mid,choiceEvidenceId=choice,degree='Success',damagedBaselineUnitId=None)
    return {'event':event,'manifest':mid,'lifecycle':lifecycle,'prerequisite':prerequisite,'choice':choice,'capture':cap}


def material_recovery(c):
    issue='FI-E08'
    x=Fixture();x.records[x.manifest]['resourcePolicy']='summoned-no-resources'
    c.reject(issue,'later permitted capture cannot erase initial summoned no-resource origin',lambda:x.run())
    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]['manifestEvidenceId']
    for key in (x.manifest,cap):x.records[key]['resourcePolicy']='summoned-no-resources'
    ledger=x.run();recovery=ledger.state['recoveries'][x.creature];h=harvest_fixture(x)
    result=ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{})[x.creature]
    c.check(issue,'preserved no-resource origin allows no Fishing reserve or baseline harvest',
        recovery['originRestrictions']==['summoned-no-resources'] and not recovery['authorizedUnitIds'] and not result['authorizedExtractedUnitIds'])
    x.records[h['manifest']].update({'resourcePolicy':'permitted','accessPermission':'permitted'})
    c.reject(issue,'harvest permission cannot launder captured origin prohibition',lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    x.records[h['manifest']]['originRestrictions']=['summoned-no-resources']
    c.check(issue,'current access permission is separate from preserved origin prohibition',
        ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{})[x.creature]['authorizedExtractedUnitIds']==[])
    c.keep('e08-origin-restrictions-survive-access-permission',x)

    for state in sorted(ref.IRREVERSIBLE_MATERIAL_STATES):
        x=Fixture();x.records[x.manifest]['extraReserve'][0]['state']=state
        c.reject(issue,'initial '+state+' reserve cannot reappear at capture',lambda:x.run())
        x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]['manifestEvidenceId']
        x.records[cap]['baseline'][0]['state']=state;material_transition_fixture(x,x.manifest,cap)
        ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
        x.records[h['manifest']]['baseline'][0]['state']='available';material_transition_fixture(x,cap,h['manifest'],allowed=True)
        c.reject(issue,'captured '+state+' baseline cannot return even under a new available label',
            lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))

    x=Fixture();ledger=x.run();recovery=ledger.state['recoveries'][x.creature];h=harvest_fixture(x)
    x.records[h['manifest']]['extraReserve'][0]['massLb']=.75
    c.reject(issue,'changed remaining mass needs its governing real-loss transition',lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    material_transition_fixture(x,recovery['manifestEvidenceId'],h['manifest'])
    result=ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{})[x.creature]
    c.check(issue,'authorized one-pound portion can lose mass and extract at most remaining three quarters',
        result['authorizedExtractedMassLbByUnitId'][x.creature+'-extra1']==.75 and
        result['authorizedExtractedMassLbByUnitId'][x.creature+'-extra2']==1 and result['inventoryCreated']==[])
    c.keep('e08-post-capture-real-three-quarter-pound-remainder',x)
    restored=material_successor_fixture(x,h['manifest'],'repacked-manifest',[7300,0,0]);x.records[restored]['extraReserve'][0]['massLb']=1
    material_transition_fixture(x,h['manifest'],restored)
    c.reject(issue,'repackaging cannot restore lost quarter pound',lambda:ref.material_history_to(x.world(),recovery['manifestSnapshot'],x.records[restored]))
    x=Fixture();x.records[x.manifest]['extraReserve'][0]['massLb']=.75
    c.reject(issue,'new initial meat reserve still requires a whole real pound',lambda:x.run('commit'))
    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]['manifestEvidenceId']
    x.records[cap]['extraReserve'][0]['massLb']=.75;material_transition_fixture(x,x.manifest,cap)
    c.check(issue,'loss before first capture does not create a new fractional meat entitlement',
        x.creature+'-extra1' not in x.run().state['recoveries'][x.creature]['authorizedUnitIds'])

    x=Fixture();ledger=x.run();h=harvest_fixture(x,cp=[3000,0,0]);recovery=ledger.state['recoveries'][x.creature]
    c.reject(issue,'harvest cannot precede capture that authorizes recovery',lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    for target,field,value in [('prerequisite','deathOrRemovalTime',8000),('lifecycle','deathOrRemovalTime',8000),
            ('lifecycle','checkpoint',[8000,0,0]),('lifecycle','physicalId','another-donor'),
            ('lifecycle','unitIds',[]),('lifecycle','governingProcedure','')]:
        x=Fixture();ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
        x.records[h[target]][field]=value
        c.reject(issue,'extraction requires historical lifecycle '+target+' '+field,
            lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))

    x=Fixture();ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
    for g in ref.MATERIAL_GROUPS:
        for unit in x.records[h['manifest']][g]:unit['deathOrRemovalTime']=4000
    material_transition_fixture(x,recovery['manifestEvidenceId'],h['manifest'],lifecycle=h['lifecycle'])
    c.check(issue,'actual death clocks survive into extraction',
        ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{})[x.creature]['deathOrRemovalTime']==4000)
    later=x.add('later-clock','material-lifecycle',[4500,0,0],physicalId=x.creature,eventKind='death',deathOrRemovalTime=4500,
        priorDeathOrRemovalTime=None,unitIds=x.records[h['lifecycle']]['unitIds'],governingProcedure='Synthetic replacement claim')
    x.records[h['prerequisite']].update({'lifecycleEvidenceId':later,'deathOrRemovalTime':4500})
    c.reject(issue,'replacement time cannot reset established clock',lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    x.records[later].update({'eventKind':'documented-clock-correction','priorDeathOrRemovalTime':4000,
        'governingProcedure':'Synthetic explicit correction of an erroneous historical clock, not sale or repackaging'})
    corrected=ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{})[x.creature]
    c.check(issue,'actual governing clock correction preserves earlier timestamp in history',
        corrected['priorCorrectedClocksByUnitId'][x.creature+'-base']==4000 and corrected['deathOrRemovalTime']==4500)

    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]['manifestEvidenceId']
    for key in (x.manifest,cap):x.records[key]['baseline'][0]['state']='damaged'
    ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
    x.records[h['manifest']]['baseline'][0]['state']='available'
    transition=material_transition_fixture(x,cap,h['manifest'])
    c.reject(issue,'available label without separately lawful condition procedure cannot restore damaged material',
        lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    x.records[transition]['conditionChangeDisposition']='lawful-under-governing-procedure'
    before=deepcopy(recovery);result=ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{})[x.creature]
    c.check(issue,'separately governed lawful condition change preserves unit identity and first Fishing evaluation',
        x.creature+'-base' in result['authorizedExtractedUnitIds'] and recovery==before)

    x=Fixture();cap=x.records[x.records[x.capture]['captureEvidenceId']]['manifestEvidenceId']
    for key in (x.manifest,cap):x.records[key]['baseline'].append(x.unit('scales',.2,'ordinary-scales'))
    ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
    x.records[h['event']].update({'degree':'Critical Success','damagedBaselineUnitId':x.creature+'-damaged'})
    history=ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{});result=history[x.creature]
    c.check(issue,'partial critical harvest uses distinct damaged baseline and forfeits unselected scales',
        result['authorizedExtractedUnitIds']==[x.creature+'-'+k for k in ('base','extra1','extra2','damaged')] and
        result['forfeitedUnselectedOrdinaryUnitIds']==[x.creature+'-scales'] and result['uniqueDropsAuthorized']==[])
    c.reject(issue,'new harvester cannot reopen already resolved or forfeited ordinary body',
        lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,history))
    x.records[h['event']]['damagedBaselineUnitId']=x.creature+'-extra1'
    c.reject(issue,'critical recovery cannot duplicate Fishing reserve as damaged baseline',
        lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    x=Fixture()
    for view in x.views.values():
        for key in view['states'].values():x.records[key]['suppressed']=True
    x.select_attraction(None);x.records[x.resolution]['equipmentBonus']=0;x.sync_core();ledger=x.run()
    c.check(issue,'living zero-source capture permanently records first evaluation and creates no meat inventory',
        ledger.state['recoveries'][x.creature]['evaluatedIncludingZero'] and ledger.state['recoveries'][x.creature]['sourceExtra']==0 and
        ledger.state['recoveries'][x.creature]['inventoryCreated']==[] and ledger.state['recoveries'][x.creature]['lifeStateAtCapture']=='alive')
    x=Fixture();ledger=x.run('commit');x.records[x.manifest]['resourcePolicy']='summoned-no-resources'
    ledger.apply(x.world(),x.check,ledger.state['version'])
    c.reject(issue,'historical initial manifest cannot be rewritten after commitment',lambda:ledger.apply(x.world(),x.capture,ledger.state['version']),ledger)
    x=Fixture();ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
    x.records[recovery['manifestEvidenceId']]['baseline'][0]['state']='lost'
    c.reject(issue,'later rewrite of captured manifest cannot replace its saved snapshot',lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))
    x=Fixture();ledger=x.run();h=harvest_fixture(x);recovery=ledger.state['recoveries'][x.creature]
    x.records[h['manifest']]['baseline']=[]
    c.reject(issue,'lost material identity must remain a tombstone instead of disappearing from history',lambda:ref.resolve_ordinary_harvest_units(x.world(),h['event'],recovery,{}))


def main():
    c=Checks();response_region(c);catch_admission(c);crafting_qualification(c);attempt_clocks(c);physical_bindings(c);bait_expenditure(c);rig_operations(c);trap_lifecycle(c);material_recovery(c)
    baseline=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert len(baseline)==63 and all(sha(GAME/p)==h for p,h in baseline.items())
    fixtures=AUDIT/'FISHING_EXACT_REPAIR_FIXTURES.json'
    dump(fixtures,{'status':'synthetic regression records, not campaign content','fixtures':c.fixtures})
    inputs=[ROOT/'tools/fishing_reference.py',ROOT/'tools/validate_fishing_sequences.py',
        ROOT/'tools/validate_fishing_recipe_candidate.py',
        ROOT/'tools/validate_fishing_exact_repairs.py',ROOT/'tools/fishing_crafting_fixtures.py',
        ROOT/'tools/build_fishing_recipe_candidate.py',ROOT/'tools/templates/fishing_rules.md',
        AUDIT/'FISHING_EXACT_REPAIR_WORKED_CASES.md',
        AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md',fixtures]
    inputs.extend(ROOT/p for p in read(AUDIT/'FISHING_AUTHORING_STATUS.json')['outputs'])
    report={'status':'partial FI-E regression evidence; full promotion gate remains open',
        'authority':'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md','authorityReplyId':'f0bf49fb-8bea-499f-8243-f3db5c302bbf',
        'checks':c.rows,'checkCount':len(c.rows),'coveredIssues':['FI-E01','FI-E02','FI-E03','FI-E04','FI-E05','FI-E06','FI-E07','FI-E08','FI-E10'],
        'inputHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in inputs},
        'protectedInputsUnchanged':63,'recipesPromoted':0,
        'limits':'Bounded helper regressions only; all FI-E01..11 requirements and artifact agreement still required.'}
    dump(AUDIT/'FISHING_EXACT_REPAIR_VALIDATION.json',report)
    print(json.dumps({k:report[k] for k in ['status','checkCount','coveredIssues','protectedInputsUnchanged','recipesPromoted']}))


if __name__=='__main__':main()
