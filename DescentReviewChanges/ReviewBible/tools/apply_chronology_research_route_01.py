"""Save the exact jointly confirmed route as a bounded provisional Director reference."""
from copy import deepcopy
from datetime import datetime,timezone
import re,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
    candidate=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_CANDIDATE.json'
    confirmation=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_CONFIRMATION_DOM.txt'
    target=R/'data/director/cosmology/chronology_research_route_reviewed_01.json'
    chapter=R/'docs/director-only/cosmology/CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md'
    receipt=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_APPLICATION_CHECK.json'
    assert all(not p.exists() for p in [target,chapter,receipt])
    assert info(candidate)['sha256']=='010af70d88ccd56c5f876b96afa3119392a4e4ae2fef8bdb5275cbe17d22c491'
    seen=confirmation.read_text(encoding='utf-8')
    assert '18747f4187e194eb86e2a92c314ceca7d702534d61b5e0532c7f748df874ef76' in seen and info(candidate)['sha256'] in seen
    assert all(f'LP{i:02d} — Confirmed' in seen for i in range(1,9))
    assert 'no remaining defect' in seen or 'not' in seen and 'remaining defect requiring an additional patch' in seen
    source_check=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_RETURN_SOURCE_CHECK_integrated.json'
    local_check=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_VALIDATION.json'
    assert json.loads(source_check.read_bytes())['failureCount']==0 and json.loads(local_check.read_bytes())['failureCount']==0
    original=json.loads(candidate.read_bytes());route=deepcopy(original['researchRoute'])
    before_status=route['status'];route['status']='Jointly reviewed and locally adopted NEW provisional Director/playtest route. Not recovered original lore; runtime, human balance and full-game approval remain open.'
    now=datetime.now(timezone.utc).isoformat()
    data={'id':'COSMOLOGY-CHRONOLOGY-RESEARCH-ROUTE-REVIEWED-01','recordedAtUtc':now,
      'authority':'Original manuscripts govern source reading subject to explicit owner corrections. Current souls/research operating model governs shared procedures. This package adopts only the jointly confirmed new route authorship.',
      'scope':'6route nodes, finite handouts,10qualification findings,3prediction tests, local12hour change cycle, finite alternate library and56interval worked schedule.',
      'status':'NEW provisional Director/playtest candidate; jointly confirmed by actual GPT Part3 and Codex.',
      'confirmedCandidate':info(candidate),'confirmation':info(confirmation),'confirmedPatch':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_LOCAL_PATCH_PROPOSAL.json'),
      'currentRoute':route,'statusLabelChangeOnly':{'before':before_status,'after':route['status']},
      'sourceBindings':json.loads((A/'cosmology-chronology-research-route-01/SOURCE_BINDINGS.json').read_bytes()),
      'validation':{'sourceFileLocationChecks':263,'exactPatchAndClockChecks':115,'failures':0,'sourceCheck':info(source_check),'localCheck':info(local_check),'runtimeMechanismRuns':0,'humanPlaytested':False},
      'relatedCurrentReferences':[
        info(R/'data/director/cosmology/souls_research_reviewed_01.json'),
        info(R/'data/director/cosmology/chronology_source_reviewed_01.json')],
      'notAdopted':['Any prospective710AE calendar anchor','Campaign frame before/during/after Proof War','Cosmological identity merges or recovered Equation formula','EPI01–17 mechanics','Pending spells','Whole Tier6–7 campaign/map/encounter-stat completion','Runtime/human balance/full-game/publication approval'],
      'preservedReturnHistory':[info(A/name) for name in ['COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Addendum_and_Evidence.zip','COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Revised_Addendum_and_Evidence.zip','COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Integrated_Addendum_and_Evidence.zip']],
      'historicalCasebooks':'All original identifiers and three return casebooks remain preserved in their immutable archives. Their route examples are nonoperative wherever superseded by this exact currentRoute. The current worked examples are the confirmed schedule, loan sequence, fixed fixture outcomes and task outcomes below.',
      'sourceInformationDeleted':0,'newProvisionalRouteAdopted':True,'campaignEpochChosen':False,'sourceDatesEdited':False,'fullCosmologyClosed':False,'published':False}
    target.write_bytes(encoded(data))
    lines=['# Chronology and Equation research route — reviewed candidate','',
      'This is the current **NEW provisional Director/playtest route**, jointly confirmed in Calibration Review Part3. Its new scenes, holdings and mechanics are authored game material, not recovered cosmological canon. Original sources remain intact. Explicit owner corrections control where stated.','',
      'Use [the souls/research operating reference](SOULS_RESEARCH_REVIEWED_01.md) for shared qualifications, language, taint, Hunt and death procedures. Use [the chronology source reference](CHRONOLOGY_SOURCE_REVIEWED_01.md) for the separate original-source comparison. This route selects no campaign epoch, corrects no87/710date, resolves no identity and activates no epilogue mechanic.','',
      'The precise current data is [chronology_research_route_reviewed_01.json](../../../data/director/cosmology/chronology_research_route_reviewed_01.json). Its application has263source/file/location checks and115exact-patch/clock checks; these do not constitute live playtesting or a complete Tier6–7 campaign.','',
      '## Route and evidence requirements','']
    def title(k):return re.sub(r'(?<!^)(?=[A-Z])',' ',k).replace('_',' ').capitalize()
    def emit(value,level=3):
        if isinstance(value,str):lines.extend([value,''])
        elif isinstance(value,(int,float,bool)) or value is None:lines.extend([str(value),''])
        elif isinstance(value,list):
            if all(isinstance(v,str) for v in value):lines.extend(['- '+v for v in value]+[''])
            else:
                for i,v in enumerate(value):
                    if isinstance(v,dict):lines.extend(['#'*min(level,6)+' '+str(v.get('id',v.get('name',f'Entry {i+1}'))),''])
                    emit(v,level+1)
        else:
            for k,v in value.items():
                if k in ['citations','sourceThemeCitations','nonoperativeHistory']:continue
                if isinstance(v,(dict,list)):
                    lines.extend(['#'*min(level,6)+' '+title(k),'']);emit(v,level+1)
                else:lines.extend(['**'+title(k)+':** '+str(v),''])
    emit(route['routeGate'])
    lines.extend(['## Bounded operational knowledge','']);emit(route['equationOperationalRelation'])
    lines.extend(['## The six scenes',''])
    for node in route['nodes']:
        lines.extend(['### '+node['id']+' — '+node['name'],''])
        # Omit duplicated older aliases from the readable chapter; the JSON aliases agree.
        emit({k:v for k,v in node.items() if k not in ['id','name','defaultQuestion','defaultDC','fixedOutcomes','result','schedule']},4)
    for heading,key in [('Finite handouts and provenance','handouts'),('Language and surviving text','languageAndReading'),('Physical fixture','mechanismFixture'),('Deterministic mechanism settings','mechanismSettings'),('Local heat observation','localChangeWindow'),('Ten qualification findings','qualificationFindings'),('Three prediction tests','predictionTests'),('Knowledge, exposure and Hunt','ktProgression'),('Shared task procedure','taskProcedure'),('Finite alternate library','alternateLibraries')]:
        lines.extend(['## '+heading,'']);emit(route[key])
    s=route['qualificationSchedule'];lines.extend(['## Complete Bard schedule',''])
    for k in ['character','clockPremises','safetyPremise','readiness','failedRetry','completion','limits']:lines.extend(['**'+title(k)+':** '+s[k],''])
    lines.extend(['Times such as28:00 mean04:00 on the following day. Every interval is actual elapsed time; between-phase descent remains a stated prerequisite from ordinary campaign play.','','| Phase / day | Start | End | Activity |','|---|---|---|---|'])
    for v in s['intervals']:lines.append('| '+v['phase']+' / '+str(v['day'])+' | '+v['start']+' | '+v['end']+' | '+v['activity'].replace('|','\\|')+' |')
    lines.extend(['','## Four borrowed-proficiency windows','']);emit(route['borrowedProficiencyFourWindowExample'])
    lines.extend(['## Preservation and remaining work','',
      'First, revised and integrated return archives, all source bindings, prior cases and the exact confirmed local patch remain preserved. Their superseded operating claims are history; the current route above governs this candidate. The full cosmology, broader deep-floor encounters, all17epilogue groups, runtime implementation, human playtesting and whole-game flow remain open.','',
      'Campaign frame relative to the Proof War remains an unanswered owner choice. No710AE prospective phase convention is adopted here. This application is local and unpublished.',''])
    chapter.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    saved=json.loads(target.read_bytes());same=deepcopy(saved['currentRoute']);same['status']=before_status;assert same==original['researchRoute']
    # The chapter's source path is relative to docs/director-only/cosmology.
    assert (chapter.parent/'../../../data/director/cosmology/chronology_research_route_reviewed_01.json').resolve()==target.resolve()
    receipt.write_bytes(encoded({'recordedAtUtc':now,'data':info(target),'chapter':info(chapter),'confirmedCandidate':info(candidate),'confirmation':info(confirmation),
      'sourceCheck':info(source_check),'localCheck':info(local_check),'sourceChecks':263,'patchAndClockChecks':115,'failureCount':0,
      'routeMatchesConfirmedCandidateExceptStatusLabel':True,'frozenSources':83,'nodes':6,'qualificationFindings':10,'predictionTests':3,'scheduleIntervals':56,
      'newProvisionalRouteAdopted':True,'sourceInformationDeleted':0,'campaignEpochChosen':False,'sourceDatesEdited':False,'runtimeMechanismRuns':0,'humanPlaytested':False,'wholeGameApproved':False,'published':False}))
    print(json.dumps({'application':info(receipt),'chapter':info(chapter),'data':info(target),'newProvisionalRouteAdopted':True,'wholeGameApproved':False}))

if __name__=='__main__':main()
