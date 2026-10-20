"""Record completed backup, preserved Rank8 return and observed next GPT review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_MEMORY_DENIAL_57.json'
    out=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK8_RETURN_58.json'
    report=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK8_RETURN_58_CHECK.json'
    keep=A/'navigation-before-github-rank8-return-58'
    assert not any(p.exists() for p in [out,report,keep])
    cp=read(old);checks=[]
    def ck(label,ok):checks.append({'check':label,'passed':bool(ok)});assert ok,label
    ck('Exact previous checkpoint',info(old)['sha256']=='a28473d87363a97d3ea76b8c7a3733c39d1154dbc41964d02ce0febb48e6c0e4')
    pushpath=G/'docs/audit/2026-10-20/github-snapshot-memory-denial57/PUSH_RECEIPT.json'
    push=read(pushpath)
    ck('Verified push through57',push['commit']==push['remoteMain']=='0a9c7b2bc9adc0f6773f2cb64e2dbb3296843ccc' and push['worktreeClean'] and push['expectedBlobsVerified']==28284 and push['priorTrackedEntriesPreserved']==27845 and push['trackedEntriesDeleted']==push['sourceInformationDeleted']==0)
    receiptpath=A/'RANK8_DAMAGE6_PART5_RETURN_01_LOCAL_PREFLIGHT.json';receipt=read(receiptpath)
    ck('559 exact local checks',receipt['checkCount']==559 and receipt['failures']==0 and receipt['forwardAndReverseOperations']==37 and not receipt['implementationApplied'])
    for key in ['archive','model','nativeFinal']:ck('Exact received binding '+key,info(G/receipt[key]['path'])==receipt[key])
    nativepath=A/'GPT_PART5_RANK7_IDENTITY_CONFERENCE_10_NATIVE.json'
    browserpath=A/'GPT_PART5_RANK7_IDENTITY_CONFERENCE_10_BROWSER_OBSERVATION.json'
    requestpath=A/'GPT_PART5_RANK7_IDENTITY_CONFERENCE_10_REQUEST.txt'
    browser=read(browserpath);native=read(nativepath)
    ck('Actual request observed in browser',browser['observedRequestText'].strip()==requestpath.read_text(encoding='utf-8').strip())
    ck('Observed active reply',browser['visibleStatus']=='ChatGPT is responding' and native['thread']['status']['type']=='active')
    protected=[old,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
        b=cp[k];ck('Current binding '+k,info(G/b['path'])==b);protected.append(G/b['path'])
    for b in cp['canonicalHelperBaselinesUnchanged']:
        ck('Helper baseline '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
    originals={p:p.read_bytes() for p in protected}
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths}
    for b in cp['navigation']:ck('Previous navigation exact '+b['path'],info(G/b['path'])==b)
    keep.mkdir()
    for p,b in nav.items():(keep/p.name).write_bytes(b)
    base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        b=nav[p];pos=b.index(b'\n')+1
        notice=('\n**Current review and backup — 20 October 2026:** [Checkpoint 58]('+prefix+base+out.name+') records verified [GitHub backup through checkpoint57]('+push['url']+'). GPT returned the six Rank8Damage6 procedures and 12 main/41 branch cases; the complete archive, 51 original sources, 11 context files and 37 reversible operations passed 559 independent preservation/reconstruction checks. Full local semantic review remains pending. GPT is now responding to the separate Rank7IdentityCasting5 request. Applied 525 reviewed / 323 pending / 249 standalone, 173 interfaces and 39 accepted-but-unapplied identities remain unchanged. Queue47 retains 281 grouped and42 ungrouped pending identities. No gameplay application.\n').encode()
        p.write_bytes(b[:pos]+notice+b[pos:]);ck('Previous navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==b)
    p=navpaths[2];b=nav[p];pos=b.index(b'</h1>')+len(b'</h1>')
    notice=('<section class="sequence" aria-label="Current GitHub backup and GPT review"><p><strong>Checkpoint58: backup through57 verified; Rank8 return preserved.</strong>Six procedures and12 main/41 branch cases received;559 local integrity/replay checks passed; semantic review pending. GPT is responding to Rank7IdentityCasting5. No gameplay application. <a href="'+base+out.name+'">Current checkpoint</a> · <a href="'+push['url']+'">Verified commit</a></p></section>').encode()
    p.write_bytes(b[:pos]+notice+b[pos:]);ck('Prior map retained',p.read_bytes().replace(notice,b'',1)==b)
    cp.update(id='ACTIVE-AUTHORING-GITHUB-RANK8-RETURN-58',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=info(old),status='Verified backup through57; Rank8Damage6 return preserved and exact-replayed, semantic review pending; GPT responding to Rank7IdentityCasting5.',navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],latestPreviouslyVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':57,'receipt':info(pushpath),'url':push['url']},lastUsageObservation={'usedPercent':12,'remainingPercent':88,'stopAtRemainingPercent':20},previousGoalTurnClassification='progress: preserved and independently exact-verified the complete Rank8 return; dispatched and observed the next Rank7 source conference; recorded verified GitHub backup through57.',laterLocalWork='This Rank8 inbound archive/extraction/receipt, next Rank7 request/evidence, post-push checkpoint and navigation follow verified backup through57.',nextAction='Complete independent substantive review of all Rank8 procedures, questions,12 main and41 branch cases; record findings before any accepted aggregate change. Receive active Rank7IdentityCasting5 return. Continue42 ungrouped rank9 identities and full prepared conferences. Preserve owner implementation reservation; stop at20 percent remaining.')
    cp['completedRank8Damage6Return']={'archive':receipt['archive'],'model':receipt['model'],'localPreflight':info(receiptpath),'nativeFinal':receipt['nativeFinal'],'assistantTurn':'5cc8c83d-ec06-41b4-b4e7-e1c1b06ab85f','localSemanticReview':'PENDING: six full procedures and six shared clauses read; full question/case/source semantic disposition not yet complete.','acceptedAggregateIncrement':0,'implementationApplied':False}
    cp['activeGptReviewAtLastVerifiedObservation']={'threadId':browser['threadId'],'title':browser['title'],'userTurn':None,'request':info(requestpath),'nativeConfirmation':info(nativepath),'browserObservation':info(browserpath),'dispatch':info(A/'GPT_PART5_RANK7_IDENTITY_CONFERENCE_10_DISPATCH.json'),'scope':'Full Rank7IdentityCasting5 conference; five identities,68 sources,24 questions.','sent':True,'completedResponseReceived':False,'note':'Browser visibly confirms exact new request and responding state. Native reader is active but exposes only last completed Rank8 turn; its old UUID is not the new request UUID.'}
    cp['queueObservationSupersession']='Queue47 is retained byte-for-byte; its older active Rank8 status is historical. This checkpoint records the received return and active Rank7 request without changing membership.'
    out.write_bytes(enc(cp))
    for p,b in originals.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
    ck('Membership and implementation unchanged',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
    report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':info(out),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'implementationApplied':False,'scope':'Backup receipt, inbound verification bindings, observed GPT dispatch and preserved navigation. No authored acceptance or runtime test claim.'}))
    print(json.dumps({'checkpoint':info(out),'report':info(report),'checks':len(checks),'failures':0}))

if __name__=='__main__':main()
