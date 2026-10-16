"""Expose the three local arc proposals without treating them as reviewed rules."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_RECOVERY_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_DRAFT_01.json'
    delta=A/'EPILOGUE_CAMPAIGN_ARCS_DRAFT_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-campaign-arcs-draft-01'
    assert all(not p.exists() for p in [target,delta,preserved])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    root=A/'cosmology-epilogue-campaign-arcs-local-draft-01'
    draft=root/'ARCS_MODEL.json';cases=root/'CASEBOOK.json'
    prep=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_PREPARATION.json'
    refinement=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_REFINEMENT.json'
    validation=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION.json'
    assert read(validation)['failureCount']==0 and read(cases)['count']==13
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;pres.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    oldstart=originals[start].decode();line=next(x for x in oldstart.splitlines() if x.startswith('**Current joint review:**'))
    addition=' The [three later campaign arcs now have local review drafts](docs/audit/2026-10-08/full-game/cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json), with 13 authored situations; they are **unsubmitted and unadopted**.'
    newline=line.replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_RECOVERY_01.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_CAMPAIGN_ARCS_DRAFT_01.json')+addition
    start.write_text(oldstart.replace(line,newline,1),encoding='utf-8',newline='\n')
    oldguide=originals[guide].decode();anchor='First, revised and integrated return archives remain immutable.'
    paragraph='The **three later arcs now have concrete local proposals**, pending GPT review: [Rekindling Stars, Conclave of Untitled Songs and Devil’s Signature](../../../../../docs/audit/2026-10-08/full-game/cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json). They include finite scenes, three actor profiles, the Margin Kite sky-vessel and route, a complete fictional contract, and [13 worked situations](../../../../../docs/audit/2026-10-08/full-game/cosmology-epilogue-campaign-arcs-local-draft-01/CASEBOOK.json). [37 file/source/structure/selected-arithmetic checks](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_LOCAL_DRAFT_01_VALIDATION.json) pass; they do not establish semantic approval, balance or playtesting. The initial proposal is preserved beside its refinement. The current version has explicit on-site flight phases and a proposed real 50gp contract bond, rather than an annual obligation with cost-free immediate exit. All new rules remain **unsubmitted and unadopted**, with unresolved frame/placement and EPI-08–14 integration. Chrome now lists the same Part 3 at tab 125746286 (and older 125746280), but reading still times out; generation remains unverified and the request has not been resent.\n\n'
    assert oldguide.count(anchor)==1;guide.write_text(oldguide.replace(anchor,paragraph+anchor,1),encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [draft,cases,refinement]);row['validationEvidence'].append(validation.relative_to(G).as_posix())
    row['currentEvidenceAddenda'].append({'id':'epilogue-campaign-arcs-local-draft-01','recordedAtUtc':now,'arcs':3,'profiles':3,'authoredCases':13,'frozenSources':11,'selectedChecks':37,'failures':0,'newRulesAdopted':False,'submittedToGpt':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50']==[x for x in before['aspects'] if x['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied/110cases. EPI08–14 submitted/83sources;return unretrieved,Chrome3 Part3 tab286 readtimeout,generation unknown. EPI15–17 now concrete local unsubmitted/unadopted drafts:3arcs,3profiles,13cases,11sources,37narrow checks pass. Campaignframe/runtime/human/balance/fullgame/publication open;419/429ordinary spells. Laterwork local.'
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_RELIC_NULL_RECOVERY_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_CAMPAIGN_ARCS_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1;text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('EPI15–17 — local unsubmitted three-arc draft','cosmology-epilogue-campaign-arcs-local-draft-01/ARCS_MODEL.json'),('EPI15–17 —13 authored situations','cosmology-epilogue-campaign-arcs-local-draft-01/CASEBOOK.json'),('EPI15–17 — preserved refinement and real contract bond',refinement.name),('EPI15–17 —37 narrow draft checks',validation.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':anchor,'replacement':paragraph+anchor}];changes[1]['operations']=[{'old':line,'replacement':newline}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1200:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Unsubmitted local EPI15–17 draft only; no adoption.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(recordedAtUtc=now,tabId='125746286',otherObservedTabId='125746280',status='Return unretrieved;newly listed same-conversation tab286 also times out;generation unknown',consecutiveGoalTurnsWithObservationFailure=2,generationConfirmedLiveNow=False,generationConfirmedTerminal=False)
    state['cosmologyEpilogueCampaignArcsLocalDraft']={'status':'localunsubmitted/unadoptedproposal','model':info(draft),'casebook':info(cases),'initialPreparation':info(prep),'refinement':info(refinement),'validation':info(validation),'sourceCount':11,'authoredCases':13,'newRulesAdopted':False}
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
        'Check the pending user observation answer about Part3. Revalidate Chrome3 same conversation;currenthandle pantheonsTab286,lastinventoryalso280. Do not resend EPI08–14 or infer stopped generation from timeouts.',
        'When actual EPI08–14 return is accessible,download and run eight-file83-source verifier,then fullsemanticreview. Currentresponse remains unavailable;no ZIP downloaded.',
        'EPI15–17 localdraft is now concrete with13cases but unsubmitted/unadopted. Review sourcefidelity and allnew rules before jointconference. Currentrefinement supersedes initialdraft preservedunderhistory. Especially check sky-vessel crew/air/fuel/landing/cargo,localatmosphere andTransition eligibility,annualcontract50gpactualbond/agency andfiniteknowledgebenefit.',
        'Initialdraftpreparation has12cases and oldhashes; refinement/currentvalidation are the current13case evidence.37checks are only file/source/structure/selectedarithmetic,not semanticapproval.',
        'Consecutivebrowserobservationfailure turns=2,butthisturnmadeconcretelocalproposalprogress. Do notdeclare wholegoalcomplete orblockedwhilemeaningfulworkremains. No source deletions,epochchoice,runtime/human/balance/wholegame/publicationapproval.419/429ordinaryspells;latestGitHub18c6e3a.'
    ];state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))
if __name__=='__main__':main()
