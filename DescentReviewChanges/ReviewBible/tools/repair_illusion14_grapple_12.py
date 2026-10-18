"""Preserve and repair the overlapping Shadow Step grapple fixture; no spell-rule change."""
from datetime import datetime, timezone
from copy import deepcopy
import json, zipfile
from pathlib import Path
import sys
sys.path.insert(0, r'C:\Github\DecenniumDescent\DescentReviewChanges\ReviewBible\tools')
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    before_path = R/'data/director/spell_proposals/illusion_perception_14_current_11.json'
    out = R/'data/director/spell_proposals/illusion_perception_14_current_12.json'
    delta = A/'ILLUSION_PERCEPTION_14_GRAPPLE_DELTA_12.json'
    check = A/'ILLUSION_PERCEPTION_14_GRAPPLE_CHECK_12.json'
    root = A/'illusion-perception-14-conference-12'
    archive = A/'DD_Illusion_Perception_14_Conference_12.zip'
    req = A/'ILLUSION_PERCEPTION_14_CONFERENCE_12_REQUEST.txt'
    prep = A/'ILLUSION_PERCEPTION_14_CONFERENCE_12_PREPARATION.json'
    assert all(not p.exists() for p in [out, delta, check, root, archive, req, prep])
    old = json.loads(before_path.read_bytes()); d = deepcopy(old)
    i = next(i for i,e in enumerate(d['currentExamples']) if e['id']=='IN4-06-A')
    e = d['currentExamples'][i]; previous = deepcopy(e)
    assert e['initialState']['origin']==[0,0,0]
    assert e['initialState']['destination']==[45,0,0]
    assert e['expectedFinalState']['otherCreaturePosition']==[0,0,0]
    e['initialState']['geometry'] = 'Coordinates are occupied-body centers. Actual Medium caster and ordinary Medium grappler each have a 5x5ft footprint and measured height6ft (half-extents2.5,2.5,3). Supporting level floor is z=-3. Caster begins(0,0,0), grappler(0,5,0); their boundaries touch at y=2.5 without overlapping interiors, within the actual5ft grapple reach. Arrival(45,0,0) fits the caster and legal carried noncreature gear in real unoccupied supported space. Transparent glass occupies x20..20.25,y-10..10,z-3..10; it does not obscure the landing but would block an ordinary physical path. No relocation ward exists. The45ft destination is within both actual ranges; this spell-specific path exception remains proposed.'
    e['initialState']['grapplerPosition'] = [0,5,0]
    e['initialState']['bodyGeometry'] = {'casterHalfExtents':[2.5,2.5,3], 'grapplerHalfExtents':[2.5,2.5,3], 'supportFloorZ':-3, 'initialWholeBodyGap':0, 'finalWholeBodyGap':40, 'actualGrappleReach':5, 'measuredHeightIsFixtureInput':True}
    e['initialState']['grapple'] = 'Caster is in a preexisting ordinary Grappled relationship held by the distinct ordinary Medium body at(0,5,0), with actual reach5ft. Caster Speed0; no separate restraint or teleport prohibition. Both caster hands satisfy actual S/F. The grappler is an independent body and does not travel.'
    e['actionsAndResolution'][3] = 'Actual caster and lawful noncreature belongings arrive once at(45,0,0). Speed0 does not prohibit this teleport; no Speed is spent and no ordinary opportunity attack occurs. The distinct grappler stays at(0,5,0). After arrival, the nearest distance between their actual occupied boxes is40ft, exceeding its ordinary5ft grapple reach, so that relationship ends. Neither creature occupied the other creature’s body before or after the move.'
    e['expectedFinalState']['otherCreaturePosition'] = [0,5,0]
    e['expectedFinalState']['finalWholeBodyGap'] = 40
    e['expectedFinalState']['bodiesOverlap'] = False
    e['sourceRefs'].append({'path':'DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md','section':'Size and occupied space; actual Medium5x5 footprint; measured height remains fixture input.'})
    d['id'] = 'ILLUSION-PERCEPTION-14-CURRENT-12'
    d['recordedAtUtc'] = datetime.now(timezone.utc).isoformat()
    d['grappleFixtureRepair12'] = {'previousCompleteCandidate':info(before_path),'caseId':e['id'],'scope':'One complete current fixture repair only; all14 procedures,28 original scenarios,3 supplemental vectors and16 substantive questions remain unchanged. Exact prior case preserved in the separate delta. Actual GPT concurrence is pending.','adopted':False,'runtimeExecuted':False}
    change = {'pointer':f'/currentExamples/{i}','completeBefore':previous,'completeAfter':deepcopy(e),'reason':'The former expected state placed the independent grappler at the caster’s original coordinates. Give both real5x5 bodies distinct positions, exact support and whole-body distance; retain the45ft teleport and actual spell proposal.'}
    restored = deepcopy(d); restored['currentExamples'][i] = deepcopy(previous)
    restored['id'] = old['id']; restored['recordedAtUtc'] = old['recordedAtUtc']; del restored['grappleFixtureRepair12']
    assert restored==old
    checks = {'fullReverseEquality':restored==old,'all14ProceduresUnchanged':d['spells']==old['spells'],'allOriginalScenariosUnchanged':d['originalExamplesUnchanged']==old['originalExamplesUnchanged'],'all28CaseIdsPreserved':[v['id'] for v in d['currentExamples']]==[v['id'] for v in old['currentExamples']],'all3SupplementsUnchanged':d['supplementalVectors09']==old['supplementalVectors09'],'all16QuestionsUnchanged':d['conferenceDecisions10']==old['conferenceDecisions10'],'allOther27CasesUnchanged':all(x==y for j,(x,y) in enumerate(zip(d['currentExamples'],old['currentExamples'])) if j!=i),'initialFootprintsTouchWithoutInteriorOverlap':5==2.5+2.5,'finalNearestBodyGap':45-2.5-2.5==40,'grappleReachExceeded':40>5,'actualBodySupport':0-3==-3,'sourceDocumentExists':(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md').is_file()}
    assert all(checks.values()) and len(d['spells'])==14 and len(d['currentExamples'])==28 and len(d['conferenceDecisions10'])==16
    out.write_bytes(encoded(d)); delta.write_bytes(encoded({'previous':info(before_path),'current':info(out),'changes':[change],'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    check.write_bytes(encoded({'candidate':info(out),'delta':info(delta),'checks':checks,'scope':'Authored fixture consistency and preservation only. No runtime, human gameplay, balance or actual GPT acceptance.'}))
    oldroot=A/'illusion-perception-14-conference-11'; manifest_old=json.loads((oldroot/'MANIFEST.json').read_bytes()); paths={}
    for b in manifest_old['files']:
        p=G/b['path']; assert info(p)==b,b['path']; paths[p]=b
    for p in [before_path,out,delta,check,R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',R/'tools/repair_illusion14_grapple_12.py',oldroot/'MANIFEST.json',oldroot/'README.md']:
        paths[p]=info(p)
    root.mkdir()
    readme='''# Illusion/perception14 full semantic conference12

Current12 is the operative pending candidate. Read all14 complete procedures, actual source/access, sharedContractRouting10, all16 conferenceDecisions10, all28 currentExamples and3 supplementalVectors09, alongside the full supplied original/accepted sources. All28 original scenario texts and complete prior versions remain preserved. The previous conference README is included as history of the substantive questions, not as a competing Current11 authority.

Current12 repairs only IN4-06-A. A Medium5x5 caster at(0,0,0) and distinct Medium5x5 grappler at(0,5,0), both measured height6 and floorz-3, touch without overlapping. Caster teleports45ft to(45,0,0) under the explicit pending Shadow Step path exception. The grappler stays(0,5,0); the actual nearest whole-body gap40ft exceeds reach5. Full original/current case and reverse-equality checks are supplied. No other procedure, case, source proposition or design question changed. Current11 was prepared but never submitted.

Settle all16 substantive questions and give per-spell dispositions for all14 identities. Especially review Greater Phantom Steed carrying and suppression; original conditional Mind Maze mid-resolution premise versus real Ready; private Echofield recording; Spectral Army attack-target exception and later damage roots; armed Programmed Illusion/Detect Magic; True Seeing union and the Mental Prison bridge. Creation remains separate. Conditional source gaps are not runtime evidence. Accepted AC6/DE4 scopes and the five-entry Fate whitelist remain closed.

Return a downloadable REVIEW.json, VERDICT.md and complete exact Current12 pointer replacements if needed. No adoption, runtime, human gameplay, numerical balance, cosmology,75-domain closure, whole-game flow or release approval is requested. Ordinary480 reviewed/368 pending counts remain unchanged.
'''
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    manifest={'id':'ILLUSION-PERCEPTION-14-CONFERENCE-12','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(out),'files':list(paths.values()),'counts':{'spells':14,'originalScenarios':28,'currentCases':28,'supplements':3,'questions':16},'authoredCounts':{'reviewed':480,'pending':368},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    (root/'MANIFEST.json').write_bytes(encoded(manifest))
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']: z.write(root/name,name)
        for p,b in sorted(paths.items(),key=lambda x:x[1]['path']): z.write(p,'files/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p,b in paths.items(): assert z.read('files/'+b['path'])==p.read_bytes()
    b=info(archive)
    req.write_text(f'Please conduct the full illusion/perception14 semantic conference using {archive.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}). Read Current12 with all14 procedures,28 original/current cases,3 supplements and16 substantive questions plus full sources. It supersedes UNSENT11, changing only the overlapping Shadow Step grapple fixture: real Medium5x5 bodies touch initially at distinct centers(0,0,0)/(0,5,0), floorz-3; teleport45ft leaves40ft whole-body gap and ends reach5 grapple. Full before/after preservation supplied. Settle every procedure/question, including the substantive source-specific new authorship in README; provide downloadable full exact corrections at Current12 pointers if needed. Conditional source gaps stay explicit; accepted AC6/DE4 and Fate scopes remain closed. No adoption/runtime/human gameplay/balance/cosmology/domain closure;480/368 unchanged.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared UNSENT; companion/life10 conference remains actually active.','newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'checkCount':len(checks),'sources':len(paths),'preparation':info(prep)}))


if __name__=='__main__':main()
