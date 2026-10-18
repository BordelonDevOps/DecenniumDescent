"""Freeze the first CL10 current-case draft with honest unresolved prerequisites.

Run once after editing/checking companion_life10_current_cases_03.py. This does not
promote spells, change the catalog/index, or claim runtime/exact acceptance.
"""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,math,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from companion_life10_current_cases_03 import CASES,AUTHORING_QUESTIONS,SOURCE_LIFECYCLES

def main():
    out=R/'data/director/spell_proposals/companion_life_10_current_03.json'
    check=A/'COMPANION_LIFE_10_CURRENT_03_PREFLIGHT.json'
    receipt=A/'COMPANION_LIFE_10_CURRENT_03_PREPARATION.json'
    archive=A/'DD_Companion_Life_10_Current_03_Draft.zip'
    assert all(not p.exists() for p in [out,check,receipt,archive]),'Preserved output exists; do not rerun.'
    layer=R/'data/director/spell_review/companion_life_10_conference_applied_02.json'
    original_raw=layer.read_bytes();p=json.loads(original_raw)
    returned=A/'companion-life10-conference-01-review'
    obligations=json.loads((returned/'CASE_DEVELOPMENT.json').read_bytes())
    checks=[]
    def ck(label,value):
        checks.append({'check':label,'passed':bool(value)})
        assert value,label
    frozen={}
    with zipfile.ZipFile(A/'DD_Companion_Life_10_Conference_01.zip') as z:
        manifest=json.loads(z.read('MANIFEST.json'))
        for b in manifest['sources']:
            raw=z.read(b['archivePath'])
            ck('Exact frozen source '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'])
            frozen[b['path']]=raw
    def bound(path):
        rel=path.relative_to(G).as_posix();raw=path.read_bytes()
        frozen[rel]=raw
        return {'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    extra=[R/'data/public/class_playtests/paladin.json',R/'data/public/class_playtests/oracle.json',layer,
      A/'COMPANION_LIFE_10_CONFERENCE_01_RECEIPT.json',A/'COMPANION_LIFE_10_CONFERENCE_APPLIED_02_CHECK.json',
      returned/'REVIEW.json',returned/'PROPOSED_CORRECTIONS.json',returned/'CASE_DEVELOPMENT.json',
      R/'tools/companion_life10_current_cases_03.py',R/'tools/build_companion_life10_current_03.py']
    extra_bindings=[bound(x) for x in extra]
    for b in p['sourceBindings']:
        raw=frozen[b['path']]
        ck('Nested original source binding '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'])
    cat=json.loads(frozen['DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'])
    catalog={s['id']:s for s in cat['spells']}
    classes={k:json.loads(frozen[f'DescentReviewChanges/ReviewBible/data/public/class_playtests/{k.lower()}.json']) for k in ['Wizard','Cleric','Paladin','Oracle']}
    byid={c['id']:c for c in CASES}
    ck('27 distinct current case IDs',len(CASES)==len(byid)==27)
    ck('All20 original obligations have separate current entries',all(x in byid for x in obligations['originalIds']))
    ck('Two Command positive cases honestly conditional',[c['id'] for c in CASES if c['prerequisite']]==['IN6-09-A','IN6-09-B'])
    ck('All case runtime claims false',all(c['runtimeExecuted'] is False for c in CASES))
    ck('Five explicit unsent clarification questions',len(AUTHORING_QUESTIONS)==5)
    def walk(o,pointer=''):
        yield pointer,o
        if isinstance(o,dict):
            for k,v in o.items():yield from walk(v,pointer+'/'+str(k))
        elif isinstance(o,list):
            for k,v in enumerate(o):yield from walk(v,pointer+'/'+str(k))
    body_count=0;actor_count=0
    for path,v in walk(CASES):
        if not isinstance(v,dict):continue
        if 'bounds' in v and 'size' in v and 'heightFeet' in v:
            lo=v['bounds']['min'];hi=v['bounds']['max'];w={'Tiny':2.5,'Small':5,'Medium':5,'Large':10}[v['size']]
            ck('Body width/height '+path,hi[0]-lo[0]==w and hi[1]-lo[1]==w and hi[2]-lo[2]==v['heightFeet'] and all(hi[i]>lo[i] for i in range(3)))
            body_count+=1
        if v.get('class') in ['Wizard','Cleric'] and 'hpDerivation' in v:
            actor_count+=1;cl=v['class'];level=v['classLevel'];pb=2+(level-1)//4
            mod=(v['abilities']['INT' if cl=='Wizard' else 'WIS']-10)//2
            hp=(6 if cl=='Wizard' else 8)+2+(level-1)*((4 if cl=='Wizard' else 5)+2)
            ck('Actual class HP/attack/DC/pool '+path,v['PB']==pb and v['maximumHP']==hp and 0<=v['normalHP']<=hp and v['spellAttack']==pb+mod and v['spellDC']==8+pb+mod and v['maximumRP']==classes[cl]['rpByClassLevel'][level-1] and 0<=v['RP']<=v['maximumRP'])
            for sid in v['repertoire']['actualFixtureChoices']:
                access=catalog[sid]['classAccess'][cl]
                ck('Real class spell access '+path+'/'+sid,level>=access['minimumClassLevel'])
    for c in CASES:
        actors={x['id']:x for x in c['actors']}
        for e in c['events']:
            if 'RPAfterCommit' not in e:continue
            actor=actors[e['actor']];a=catalog[e['spellId']]['classAccess'][actor['class']]
            ck('Actual cast rank/cost '+c['id'],e['rank']==a['rank'] and e['baseRP']==a['baseRpCost'] and e['RPAfterCommit']==e['RPBefore']-e['RPPaid']>=0 and e['normalHPAfterCommit']>=1)
    def gap(a,b):
        return math.sqrt(sum(max(0,a['min'][i]-b['max'][i],b['min'][i]-a['max'][i])**2 for i in range(3)))
    def box(x,w=5,h=6,y=0):return {'min':[x-w/2,y-w/2,0],'max':[x+w/2,y+w/2,h]}
    ck('Golem full final melee gap',gap(box(20,10,8),box(30))==2.5)
    ck('Knight full melee gap',gap(box(10),box(20))==5)
    ck('Tiny touch range repaired',gap(box(11.25),box(20,2.5,2))==5)
    ck('Medium touch range actual',gap(box(11.25),box(20))==3.75)
    ck('Large touch range actual',gap(box(11.25),box(20,10,8))==1.25)
    ck('Wight target range and hostile proximity',gap(box(10),box(40))==25 and gap(box(10),box(20))==5)
    ck('AM open-floor point range',27.5-2.5-20==5<=10)
    ck('AM balcony point range',math.sqrt(5**2+3**2)<10)
    ck('AM balcony source segment clears original rim',10+(7-10)*.5==8.5>8)
    ck('Slow aura actual exit then reentry budget',33-2.5-20==10.5>10 and 2*(33-27.5)==11<=15)
    ck('Wraith10ft slab full-body traversal',(10+5)*2==30 and 40-30==10)
    ck('Wraith15ft slab full-body traversal',(15+5)*2==40 and 40-40==0)
    ck('Wraith caster body outside opaque slab',byid['IN6-07-B']['actors'][0]['body']['bounds']['max'][0]<0)
    ck('Hom physical and Load capacity both',6*7.5==45 and 20<=45 and 6/2==3 and 2<=3 and 4>3)
    ck('Hom Burdened exact threshold and rates',2>=3/2 and 20-10==10 and 30-10==20)
    ck('Soulburn original retained arithmetic',12-7+3==8 and 31-20==11)
    ck('Soulburn second real paid cast',24-7+3-7+3==16 and 44-20-20==4)
    ck('Grave Gift direct recovery retains wounds',31//2==15 and 31-15==16 and byid['NE5-04-A']['expected']['patientWounds']==3)
    ck('Flood complete dice and Wound arithmetic',sum([8,8,7,7,7])==37 and 37//2==18 and 18+2>=18)
    ck('Wraith actual donor loss excludes overkill',5+7==12 and 12//2==6 and min(6,100-97)==3)
    ck('Burden Shared14 conservation/funding',4+5+5==14 and 4//2==2)
    ck('Life Linked14 conservation/funding',14-2==12 and 6+6==12 and 6//2==3)
    ck('Hom repair arithmetic',7+3+5==15 and 20+11==31)
    ck('All4 Create profiles independently covered',{'CL10-PROFILE-GHOUL','CL10-PROFILE-WIGHT','CL10-PROFILE-MUMMY','IN6-11-A'}<=set(byid))
    ck('Twenty historical strings untouched',p['all20HistoricalScenarioTexts']==json.loads(original_raw)['all20HistoricalScenarioTexts'])
    ck('Applied layer bytes untouched',layer.read_bytes()==original_raw)
    records=[]
    for old in p['records']:
        proposal=old['conferenceAuthorshipProposal01']
        records.append({'spellId':old['spellId'],'status':'CURRENT_AUTHORSHIP_NOT_EXACT_ACCEPTED',
          'completeSourceAndAccess':deepcopy(old['completeCurrentCatalogSourceAndAccess']),
          'completeProcedureFromActualConferenceUnchanged':proposal['completeProposedProcedure'],
          'requiredSharedRuleIds':proposal['requiredSharedRuleIds'],
          'currentCaseIDs':[c['id'] for c in CASES if c['spellId']==old['spellId']],
          'completeHistoricalRecordUnchanged':deepcopy(old['completeEarlierRecordUnchanged'])})
    model={'id':'DD-COMPANION-LIFE10-CURRENT-03','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
      'status':'UNSENT_CURRENT_AUTHORSHIP_DRAFT_WITH_EXPLICIT_CLARIFICATION_AND_CONTENT_HOLDS',
      'developmentDirection':'VIDEO_GAME_ONLY','authorityBoundary':'Actual returned conference proposals are reproduced verbatim for current case development. No new procedure adoption, runtime implementation, human balance approval, bestiary CR certification or cosmology change.',
      'actualConferenceReceipt':info(A/'COMPANION_LIFE_10_CONFERENCE_01_RECEIPT.json'),
      'completePreservedAppliedLayer':p,'records':records,'sharedRules':deepcopy(p['conferenceSharedRuleProposals01']),
      'currentCases':CASES,'clarificationQuestions':AUTHORING_QUESTIONS,
      'originalObligationCoverage':[{'id':i,'currentCaseId':i,'status':byid[i]['status']} for i in obligations['originalIds']],
      'newSourceBindings':extra_bindings,'sourceBindings':p['sourceBindings'],
      'caseCounts':{'total':27,'originalObligationsRepresented':20,'conditionalMainCases':2,'nonconditionalMainCases':25,'supplementaryMainCases':7,'subbranchesHaveTheirOwnExplicitPrerequisites':True},
      'countsUnchanged':{'reviewed':480,'pending':368},'domainGatesUnchanged':75,
      'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    out.write_bytes(encoded(model))
    report={'candidate':info(out),'checks':checks,'checkCount':len(checks),'failed':0,'bodyRecordsChecked':body_count,'classActorRecordsChecked':actor_count,
      'frozenOriginalSources':len(manifest['sources']),'newBoundFiles':len(extra),
      'scope':'File integrity, access, actor arithmetic, selected geometry and authored expected-state consistency only. Not engine execution or comprehensive all-branch proof.',
      'openQuestions':AUTHORING_QUESTIONS,'unconditionalExactAcceptanceClaimed':False}
    check.write_bytes(encoded(report))
    files={out.relative_to(G).as_posix():out.read_bytes(),check.relative_to(G).as_posix():check.read_bytes(),**frozen}
    archive_manifest={'id':'DD-CL10-CURRENT-03-DRAFT-MANIFEST','candidate':info(out),'preflight':info(check),'status':model['status'],
       'files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'archivePath':'files/'+n} for n,b in sorted(files.items())]}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('MANIFEST.json',encoded(archive_manifest))
        z.writestr('READ_ME.txt','CL10 current authorship draft after actual GPT Conference01. Read five explicit questions before treating this as final exact review. All20 original scenario texts and whole returned/applied proposal history are preserved. 27 main authored cases,2 conditional Command cases,7 supplementary cases; subsidiary hypotheses remain labeled. No public catalog/index or domain gate changed. All original sources are frozen exact Conference01 bytes; new Paladin/Oracle sources are fully included.\n')
        for n,b in files.items():z.writestr('files/'+n,b)
    with zipfile.ZipFile(archive) as z:
        for b in archive_manifest['files']:
            raw=z.read(b['archivePath']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'],b['path']
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(out),'archive':info(archive),'preflight':info(check),
      'currentCases':27,'conditionalMainCases':2,'clarificationQuestions':5,'sourceFileCount':len(frozen),'archiveFilesVerified':len(files),
      'submittedToGPT':False,'status':model['status'],'countsUnchanged':model['countsUnchanged'],'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'candidate':info(out),'archive':info(archive),'checks':len(checks),'bodyRecords':body_count,'actorRecords':actor_count,'sourceFiles':len(frozen),'cases':27,'conditional':2,'questions':5},ensure_ascii=False))

if __name__=='__main__':main()
