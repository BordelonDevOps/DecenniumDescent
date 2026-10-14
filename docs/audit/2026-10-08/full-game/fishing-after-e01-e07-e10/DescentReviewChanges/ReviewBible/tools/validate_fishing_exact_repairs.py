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
    override=x.add('reviewed-override','reviewed-catch-dc',x.cp0,catchProfileEvidenceId=x.catch_profile,
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


def main():
    c=Checks();response_region(c);catch_admission(c);crafting_qualification(c)
    baseline=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert len(baseline)==63 and all(sha(GAME/p)==h for p,h in baseline.items())
    fixtures=AUDIT/'FISHING_EXACT_REPAIR_FIXTURES.json'
    dump(fixtures,{'status':'synthetic regression records, not campaign content','fixtures':c.fixtures})
    inputs=[ROOT/'tools/fishing_reference.py',ROOT/'tools/validate_fishing_sequences.py',
        ROOT/'tools/validate_fishing_exact_repairs.py',ROOT/'tools/fishing_crafting_fixtures.py',
        ROOT/'tools/build_fishing_recipe_candidate.py',ROOT/'tools/templates/fishing_rules.md',
        AUDIT/'FISHING_EXACT_REPAIR_WORKED_CASES.md',
        AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md',fixtures]
    inputs.extend(ROOT/p for p in read(AUDIT/'FISHING_AUTHORING_STATUS.json')['outputs'])
    report={'status':'partial FI-E regression evidence; full promotion gate remains open',
        'authority':'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md','authorityReplyId':'f0bf49fb-8bea-499f-8243-f3db5c302bbf',
        'checks':c.rows,'checkCount':len(c.rows),'coveredIssues':['FI-E01','FI-E07','FI-E10'],
        'inputHashes':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in inputs},
        'protectedInputsUnchanged':63,'recipesPromoted':0,
        'limits':'Bounded helper regressions only; all FI-E01..11 requirements and artifact agreement still required.'}
    dump(AUDIT/'FISHING_EXACT_REPAIR_VALIDATION.json',report)
    print(json.dumps({k:report[k] for k in ['status','checkCount','coveredIssues','protectedInputsUnchanged','recipesPromoted']}))


if __name__=='__main__':main()
