"""Record complete source preparation, preserving all existing authorities and history."""
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json
from record_rank9_memory_denial_conference_57 import G,R,A,read,encoded,info

def main():
    now=datetime.now(timezone.utc).isoformat()
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_IMPACT_EXILE_64.json'
    outcp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ILLUSION_REALITY_65.json'
    oldq=R/'data/director/spell_review/remaining_work_queue_52.json'
    outq=oldq.with_name('remaining_work_queue_53.json')
    pp=A/'RANK9_ILLUSION_REALITY_5_SOURCE_CONFERENCE_01_PREPARATION.json'
    checkp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ILLUSION_REALITY_65_CHECK.json'
    keep=A/'navigation-before-rank9-illusion-reality-65'
    browserp=A/'GPT_PART5_RANK7_BROWSER_STATUS_65.json'
    assert not any(p.exists() for p in [outcp,outq,checkp,keep,browserp])
    cp,q0,prep=map(read,[previous,oldq,pp]);q=deepcopy(q0)
    candidate=read(G/prep['candidate']['path']);sc=read(G/prep['check']['path']);checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    protected_paths=[previous,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    protected_paths += [G/cp[k]['path'] for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
    protected_paths += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected={p:p.read_bytes() for p in protected_paths}
    ck('Exact preceding checkpoint64',info(previous)['sha256']=='08c89d32cb3dce7f1666da2fc56540b0d74d7f9ce192ea6c3611d66c12d9492e')
    ck('Exact Queue52 binding',info(oldq)==cp['currentWorkQueue'])
    ck('Full packet artifact bindings',all(info(G/prep[k]['path'])==prep[k] for k in ['candidate','archive','manifest','check','request']))
    ck('Five complete source-only identities',prep['status']=='PREPARED_UNSENT' and prep['identityCount']==5 and prep['placementCount']==5 and prep['sourceCount']==157 and prep['questionCount']==31 and prep['riskCounts']=={'C':5} and sc['checkCount']==485 and sc['failures']==0 and not candidate['currentVectors'] and candidate['newRuleAdoptions']==candidate['cosmologyDecisions']==0)
    ck('Thirteen complete applied counterparts and four full pending archives',len(candidate['completeAppliedCounterparts'])==13 and len(candidate['pendingComparisonsNotAuthority'])==4 and all('completeConferenceArchive' in x for x in candidate['pendingComparisonsNotAuthority']))
    ck('All31 choices unselected',len(candidate['questions'])==31 and all(not x['decisionSelected'] for x in candidate['questions']))
    ck('All eight complete Illusion14 artifacts bound',all(any(b['path'].endswith('illusion-perception14-exact-13/'+n) for b in candidate['sourceBindings']) for n in ['SPELLS_MODEL.json','CASEBOOK.json','REGISTER.json','SOURCE_HASHES.json','PLAYER_CHAPTER.md','LOCAL_REVIEW_NOTES.md','EVIDENCE_MANIFEST.json','DIRECTOR_REVIEW.md']))
    rank8=candidate['unacceptedRank8DamageComparison']
    ck('Unaccepted Rank8 return/findings/corrections fully bound',all(info(G/b['path'])==b for k,b in rank8.items() if k!='qualification') and len(rank8)==9)
    ids=[r['spellId'] for r in candidate['records']]
    ck('Five previously ungrouped identities',len(set(ids))==5 and all(next(r for r in q['rows'] if r['id']==sid)['currentGroup'] is None for sid in ids))
    group={'group':'rank9-illusion-reality5','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':5,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'sourceCount':157,'placementCount':5,'questionCount':31,'riskCounts':{'C':5},'currentCaseCount':0,'latestObservedStatus':'Five complete sources preserve belief-based rank6-or-lower imitation,battlefield two-roll attacks,ambiguous50percent attack/spell miss chance,substantive one-minute partial reality,and a forced three-round self-reflection fight.31 choices remain unselected; no mechanical/cosmological adoption.'}
    q['groups'].append(group)
    for old,row in zip(q0['rows'],q['rows']):
        if row['id'] in ids:
            row.update(currentGroup=group['group'],currentPhase=group['phase'],semanticAcceptanceClaimed=False,sourceConferencePreparation=info(pp),nextAction='Confer on31 source-local belief,copy,RNG,physical profile,agency and lifecycle questions. Supply full useful procedures and positive cases using complete accepted perception/body/control evidence; no generic harmless-image substitute or invented soul/plane facts.')
        else:ck('Unaffected complete queue row retained '+row['id'],row==old)
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q['previousSummaryBefore65']={'limitations':q0['limitations'],'preparedOrActualReviewIdentityCount':q0['preparedOrActualReviewIdentityCount'],'originalSourceOrReceiptWorkCount':q0['originalSourceOrReceiptWorkCount']}
    q.update(id='REMAINING-WORK-QUEUE-53',recordedAtUtc=now,previousQueue=info(oldq),preparedOrActualReviewIdentityCount=305,originalSourceOrReceiptWorkCount=18,pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),latestSourceConference=info(pp))
    q['sourceBindings'].extend([info(pp),prep['candidate'],prep['archive'],prep['check']])
    q['limitations']='Current through checkpoint65: applied525/323/249 and173 interfaces unchanged;39 accepted-but-unapplied. Rank8Damage6 retains8 local findings and an unsent correction packet. Visible Rank7 browser still shows Stop2045; fresh native reads returned Too many requests,so prior native64 is retained as historical verification.49 groups cover305 pending identities;18 rank9 identities remain ungrouped. Illusion/reality5 preserves157 full sources,5 placements,31 unselected questions and485 preservation checks. No semantic acceptance,runtime or cosmology adoption. Backup through61 is verified; owner implementation reservation and separate completion gates remain.'
    ck('323 pending across49 groups;305 grouped and18 ungrouped',len(q['rows'])==323 and len(q['groups'])==49 and sum(r['currentGroup'] is not None for r in q['rows'])==305 and sum(r['currentGroup'] is None for r in q['rows'])==18)
    ck('39 accepted but unapplied unchanged',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    ck('Remaining ungrouped all rank9',all(min(a['rank'] for a in r['completeCurrentSourceAndAccess']['classAccess'].values())==9 for r in q['rows'] if r['currentGroup'] is None))
    ck('Every earlier group unchanged',q['groups'][:-1]==q0['groups'])
    ck('Prior native evidence retained with exact bytes',info(G/cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']['path'])==cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation'])
    browser={'recordedAtUtc':now,'threadId':'6ad4a867-f330-83e9-829e-bf2bb41a6c09','title':'Calibration Review Part 5','tabId':'125747318','visibleStopControl':2045,'visibleComposerControl':2040,'visibleLatestWork':'Rank7IdentityCasting5 source inspection lists Cast Echo,Meta Surge,Erase from Reality,Sequester and Simulacrum; no completed final response observed.','messageSent':False,'interrupted':False,'freshNativeRead':{'tool':'read_thread','result':'Too many requests','isError':True},'qualification':'Fresh browser observation of visible generation control; not proof of backend progress or completion. Native64 remains the latest successful native observation. Unity Development Setup could not load during preceding pertinent-information check.'}
    browserp.write_bytes(encoded(browser))
    for b in cp['navigation']:ck('Previous navigation binding '+b['path'],info(G/b['path'])==b)
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths};base='docs/audit/2026-10-08/full-game/'
    keep.mkdir()
    for p,raw in nav.items():(keep/p.name).write_bytes(raw)
    outq.write_bytes(encoded(q))
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest source preparation — 20 October 2026:** [Checkpoint65]('+prefix+base+outcp.name+') and [Queue53]('+prefix+outq.relative_to(G).as_posix()+') add five rank9 illusion/reality identities:157 full source artifacts,5 placements,31 unselected questions and485 preservation checks.305 pending identities are grouped;18 remain ungrouped. GPT visibly shows Rank7 generation; native status reads are temporarily limited. Rank8 awaits8 bounded corrections. Applied525/323/249 and39 accepted-but-unapplied stay unchanged. Backup is verified through61; no gameplay or cosmology application.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current rank9 illusion and reality preparation"><p><strong>Checkpoint65: five rank9 illusion/reality sources prepared.</strong>157 full sources,5 placements,31 unselected questions;485 preservation checks. Queue53:305 grouped pending identities,18 ungrouped. Rank7 generation remains visible; native reads are temporarily limited. Rank8 corrections remain queued. No gameplay or cosmology adoption. <a href="'+base+outcp.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('Full original review map retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-RANK9-ILLUSION-REALITY-65',recordedAtUtc=now,previousCheckpoint=info(previous),currentWorkQueue=info(outq),preparedGroupCount=49,groupedPendingIdentities=305,ungroupedPendingIdentities=18,rank9IllusionReality5SourceConference=info(pp),status='Five complete rank9 illusion/reality sources prepared without selections; visible Rank7 generation persists,native observation temporarily limited; Rank8 corrections unsent.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],lastUsageObservation={'usedPercent':19,'remainingPercent':81,'stopAtRemainingPercent':20},previousGoalTurnClassification='Verified wait: specific Rank7 browser showed live Stop control; native observation failed transiently. This turn makes progress with five full source preparations,31 questions,485 checks and queue/navigation reconciliation.',laterLocalWork='Checkpoints62-65,summon-hosts5,impact-exile4,illusion-reality5,Queue53 and current navigation follow verified GitHub backup through61.',nextAction='Inspect actual Rank7 final when available; do not interrupt or infer termination from a rate-limit error. Preserve/verify the full return,then deliver prepared Rank8 bounded corrections. Continue18 ungrouped rank9 sources and full pending conferences. Preserve owner implementation reservation; stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['latestBrowserStatus']=info(browserp)
    cp['activeGptReviewAtLastVerifiedObservation']['note']='Current browser observation shows Stop2045 without a completed final. Native confirmation remains prior64; fresh reads returned Too many requests. This transient failure is not terminal. No interruption or new message.'
    cp['queueObservationSupersession']='Queue53 preserves every earlier group and changes only five previously ungrouped identities into source-only preparation. Existing Rank8 correction status and exact accepted counts remain intact.'
    outcp.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    checkp.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(outcp),'queue':info(outq),'checks':checks,'checkCount':len(checks),'failures':0,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':'Full source/history/queue/navigation preservation only; no semantic acceptance,engine runtime or cosmology adoption.'}))
    print(json.dumps({'checkpoint':info(outcp),'queue':info(outq),'checks':len(checks),'check':info(checkp)}))

if __name__=='__main__':main()
