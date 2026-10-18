"""Preserve Current03 and correct local fixture completeness before GPT submission."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile,math
from apply_di7_ap_as_01 import G,R,A,info,encoded
from companion_life10_current_cases_03 import caster

def main():
    old=R/'data/director/spell_proposals/companion_life_10_current_03.json'
    out=R/'data/director/spell_proposals/companion_life_10_current_04.json'
    delta=A/'COMPANION_LIFE_10_CURRENT_04_LOCAL_DELTAS.json'
    check=A/'COMPANION_LIFE_10_CURRENT_04_PREFLIGHT.json'
    prep=A/'COMPANION_LIFE_10_CURRENT_04_PREPARATION.json'
    archive=A/'DD_Companion_Life_10_Current_04_Draft.zip'
    assert all(not f.exists() for f in [out,delta,check,prep,archive])
    before=old.read_bytes();d=json.loads(before);prior=deepcopy(d);changes=[];checks=[]
    def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
    def replace_case(cid,mutate,reason):
        i=next(i for i,c in enumerate(d['currentCases']) if c['id']==cid);was=deepcopy(d['currentCases'][i]);mutate(d['currentCases'][i]);changes.append({'caseId':cid,'pointer':f'/currentCases/{i}','reason':reason,'completeBefore':was,'completeAfter':deepcopy(d['currentCases'][i])})
    def armor(c):
        gear=c['bodyInputs'][0]['gear'];gear.append({'id':'actual-padded-Ghast','source':'data/playtest/equipment_acquisition_candidate.json /items/0','catalogId':'armor-and-shields.padded','massLb':8,'Load':0.8,'custody':'worn on same actual torso; correct Medium fit retained','condition':'scuffed but not Broken; cosmetic old damage not repaired','ACFormula':'11+DEXmodifier','DEXModifier':1,'wornAC':12,'armorProficiency':False})
        c['events'][1]['bodyState']='Same anchor prone at10,0; retained left-hand absence, real worn padded armor and torn coat. BaseHP50, baseAC14; actual compatible worn armor replaces AC with11+DEX1=12. No Conjuration/Flesh bonus; no creation-round action.'
        c['events'][2]['actualArmorInterface']={'wornAC':12,'baseAC':14,'totalRealGearLb':10,'totalLoad':1,'burdenThreshold':7,'Burdened':False,'nonproficiency':'STR/DEX checks, saves and attacks have disadvantage; spell RP+1 and concentration disadvantage if such operations occur. This chosen CON-save exhalation is a magical nonspell native Action, no STR/DEX attack roll or spell cast, so those penalties do not change its pool/DC or create a new RP price. Padded Stealth disadvantage remains.','actualMissingHand':'left hand stays absent, head/oral outlet remains usable'}
        c['expected'].update({'GhastBaseAC':14,'GhastActualWornAC':12,'realArmorID':'actual-padded-Ghast','armorDuplicated':False,'armorRepaired':False})
    replace_case('IN6-11-A',armor,'Original obligation explicitly includes real armor. Current03 supplied only a nonarmor coat. Bind the actual reviewed padded armor, retained fit/condition, lower worn AC and real nonproficiency rather than silently dropping that obligation.')
    def counter(c):
        b=c['independentBranches'][3];a=caster('gift-counter-W9',9,[],x=20,y=15)
        b['additionalActor']=a
        b['operation']={'source':'wizard.json /cards/17 automatic Counterspell at2, rank1 class matrix','activation':'actual available Reaction at Gift cast beginning after Gift costs; counterer perceives V/S in open bright room','rangeGapFeet':math.sqrt(15**2+10**2),'rangeLimit':60,'RPBefore':32,'RPPaid':3,'RPAfter':29,'DissonanceBefore':0,'firstDistinctPreparedClassFamilyBase':0,'Refrain':0,'DissonanceAfter':0,'INT':4,'PB':4,'d20':12,'checkTotal':20,'DC':20,'degree':'Success','rechargeBefore':0,'rechargeAfter':2,'counteredSpellRank':5,'noCounterpulseOrFeedback':True,'noRetrySamePendingCast':True}
        b['expected']='Gift donor remains1HP/22RP after paid cost; recipient remains original Dying0 with original counters and no new Stable d4; counterer29RP/recharge2.'
    replace_case('NE5-04-B',counter,'Supply a complete actual counterer body/build/pool and geometric range for the countered branch; the Current03 shorthand named Wizard9 but omitted that actual actor.')
    def readiness(c):
        c['events'][2]['originalCommand']={'sourceOwner':'original-source-W11','time':6.05,'round':2,'activation':'one actual regular-turn Bonus Action','instruction':'defensive movement0 and Dodge at the next real attached opportunity','perceivedBody':True,'samePlane':True,'rangeGapUpperBound':16.25,'clearLoEAndAudibleChannel':True,'commandAllowanceBefore':1,'commandAllowanceAfter':0,'offensiveAllowanceSpent':False,'legalBeforeField':True}
        c['events'][2]['release']='At6.1, after audible command has completed at6.05, AM caster spends its actual Reaction before owner ends6.25/attached6.5; select point now; no second price/cadence or Counterspell window.'
        c['expected']['sourceClock']='AM starts at actual release6.1, deadline66.1, voluntarily ends13; original summon clocks remain independent.'
    replace_case('CL10-SUPPRESSION-BRANCHES',readiness,'Specify the actual originally legal paid command before the readied field release, instead of calling an unspecified order source-qualified.')
    for case in d['currentCases']:
        questions=[]
        if case['id']=='IN4-10-B':questions=['CL10-C03-Q01']
        if case['id']=='IN6-07-B':questions=['CL10-C03-Q02','CL10-C03-Q04']
        if case['id']=='IN6-11-A':questions=['CL10-C03-Q03']
        if case['spellId']=='command-undeath':questions=['CL10-C03-Q05']
        if questions:case['unresolvedProposalQuestions']=questions
    # The exact before/after records include the final added qualification fields.
    for change in changes:change['completeAfter']=deepcopy(next(c for c in d['currentCases'] if c['id']==change['caseId']))
    changedids={x['caseId'] for x in changes}
    qualificationids={c['id'] for c in d['currentCases'] if c.get('unresolvedProposalQuestions')}
    for oldc,newc in zip(prior['currentCases'],d['currentCases']):
        if oldc['id'] not in changedids:
            stripped=deepcopy(newc);stripped.pop('unresolvedProposalQuestions',None)
            ck('Unchanged case except explicit qualification '+oldc['id'],oldc==stripped)
    ck('All10 full conference procedures unchanged',d['records']==prior['records'])
    ck('Shared rules unchanged',d['sharedRules']==prior['sharedRules'])
    ck('Complete old applied layer unchanged',d['completePreservedAppliedLayer']==prior['completePreservedAppliedLayer'])
    ck('Same27 current identities',[c['id'] for c in d['currentCases']]==[c['id'] for c in prior['currentCases']])
    ck('Padded real AC and mass',11+1==12 and 8+2==10 and 0.8+0.2==1<7)
    ck('Counter range/affordability/check',math.sqrt(15**2+10**2)<60 and 32-3==29 and 12+4+4==10+2*5)
    ck('Ready true ordered phases',5<6.05<6.1<6.25<6.5<11<13 and 6.1+60==66.1)
    ck('Current03 preserved exact',old.read_bytes()==before)
    source_bytes={}
    with zipfile.ZipFile(A/'DD_Companion_Life_10_Current_03_Draft.zip') as z:
        m=json.loads(z.read('MANIFEST.json'))
        for b in m['files']:
            raw=z.read(b['archivePath']);ck('Frozen03 exact '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']);source_bytes[b['path']]=raw
    equipment=json.loads(source_bytes['DescentReviewChanges/ReviewBible/data/playtest/equipment_acquisition_candidate.json'])['items'][0]
    ck('Real padded item source',equipment['id']=='armor-and-shields.padded' and equipment['unitWeightLb']==8 and equipment['sourceFields']['Armor Class (AC)']=='11 + Dex modifier')
    d['id']='DD-COMPANION-LIFE10-CURRENT-04';d['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
    d['previousCandidate']=info(old)
    d['caseCounts'].pop('nonconditionalMainCases')
    d['caseCounts']['mainEntriesWithoutWholeCaseCRHold']=25
    d['caseCounts']['fullyApprovedCurrentCases']=0
    d['caseCounts']['clarificationDependentMainIDs']=sorted(qualificationids)
    d['localAuthorship04']={'scope':'Three local fixture repairs plus explicit routing to five already recorded questions; unchanged procedures/shared rules/history. Not a final exact candidate.', 'sourceInformationDeleted':0,'newRuleAdoptions':0}
    delta.write_bytes(encoded({'original':info(old),'changes':changes,'questionRoutingAddedTo':sorted(qualificationids),'allOtherCaseContentUnchanged':True,'proceduresAndSharedRulesUnchanged':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    d['localDelta']=info(delta);out.write_bytes(encoded(d))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'failed':0,'prior335CheckScope':'The original report is retained. Its unchanged structures/arithmetic still apply; these additional checks address new corrections only. Neither report executes the game or certifies every branch.','threeCompleteRepairs':info(delta),'openQuestions':5,'wholeCaseCRHolds':2,'runtimeTestsExecuted':0,'fullyApprovedCurrentCases':0}))
    for f in [out,delta,check,R/'tools/repair_companion_life10_current_04.py']:
        source_bytes[f.relative_to(G).as_posix()]=f.read_bytes()
    m={'id':'DD-CL10-CURRENT-04-DRAFT-MANIFEST','candidate':info(out),'preflight':info(check),'supersedesUnsent03':True,'files':[{'path':n,'archivePath':'files/'+n,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for n,raw in sorted(source_bytes.items())]}
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        z.writestr('MANIFEST.json',encoded(m));z.writestr('READ_ME.txt','Current04 supersedes the unsent Current03 draft. Read five explicit clarification questions and27 authored cases (two whole-case exactCR2 holds; additional scoped question qualifications). This is a current authorship conference draft, not final exact approval. Three complete local before/after repairs preserve original real-armor obligation, actual counterer and legal pre-suppression Ready command. All prior procedures, sources and20 original texts remain exact. No adoption or runtime claim.\n')
        for n,raw in source_bytes.items():z.writestr('files/'+n,raw)
    with zipfile.ZipFile(archive) as z:
        for b in m['files']:assert hashlib.sha256(z.read(b['archivePath'])).hexdigest()==b['sha256']
    prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(out),'archive':info(archive),'localDelta':info(delta),'preflight':info(check),'archiveFilesVerified':len(m['files']),'status':'UNSENT_CURRENT_AUTHORSHIP_CONFERENCE_DRAFT','mainCases':27,'wholeCaseCRHolds':2,'questions':5,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'candidate':info(out),'archive':info(archive),'checks':len(checks),'archiveFiles':len(m['files']),'changes':3}))

if __name__=='__main__':main()
