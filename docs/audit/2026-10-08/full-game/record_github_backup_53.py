"""Record the verified backup and current GPT observation; preserve gameplay authority."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
    raw=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    now=datetime.now(timezone.utc).isoformat()
    old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_WARD_CONTROL_52.json'
    output=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_BACKUP_53.json'
    check=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_BACKUP_53_CHECK.json'
    keep=A/'navigation-before-github-backup-53'
    native=A/'GPT_PART5_LIVE_AT_GITHUB_BACKUP_53_NATIVE.json'
    receipt=G/'docs/audit/2026-10-20/github-snapshot-ward-control52/PUSH_RECEIPT.json'
    assert not any(p.exists() for p in [output,check,keep])
    cp=read(old);push=read(receipt);live=read(native);checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    ck('Expected exact previous checkpoint',info(old)['sha256']=='eb38ed80e943bfa888bf949d3b25d992557dfca6f07bec1a4c149ff32894ddfd')
    ck('Verified remote backup and complete prior tree retention',push['commit']==push['remoteMain']=='867da46cfddbbdb26d7d63c228316a8e6014e971' and push['worktreeClean'] and push['expectedBlobsVerified']==27682 and push['priorTrackedEntriesPreserved']==27452 and push['trackedEntriesDeleted']==push['sourceInformationDeleted']==0)
    ck('Existing rank8 conference still active without completed response',live['thread']['status']['type']=='active' and live['turns'][0]['id']=='e642823a-1f56-42e5-b786-8d1e3f5a85f3' and not any(i['type']=='agentMessage' for i in live['turns'][0]['items']))
    protected=[old,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
        b=cp[k];ck('Exact current binding '+k,info(G/b['path'])==b);protected.append(G/b['path'])
    for b in cp['canonicalHelperBaselinesUnchanged']:
        ck('Original helper binding '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
    originals={p:p.read_bytes() for p in protected}
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in navpaths}
    for b in cp['navigation']:ck('Preceding navigation exact '+b['path'],info(G/b['path'])==b)
    keep.mkdir()
    for p,raw in nav.items():(keep/p.name).write_bytes(raw)
    base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Latest verified backup — 20 October 2026:** [Checkpoint 53]('+prefix+base+output.name+') records [GitHub commit 867da46]('+push['url']+') through checkpoint 52. The complete preparation-only Ready successor, owner ledger02, Unity direction reconciliation and three new rank9 conferences are preserved. All 27,682 expected file contents matched; all 27,452 prior tracked entries were retained. GPT is still reviewing Rank8Damage6. Applied 525 reviewed / 323 pending / 249 standalone, 173 interfaces and 39 accepted-but-unapplied identities remain unchanged. Queue43 retains 255 grouped and 68 ungrouped pending identities.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Navigation previous bytes retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    notice=('<section class="sequence" aria-label="Current verified GitHub backup"><p><strong>Checkpoint53: GitHub backup through52 verified.</strong>Ready successor and all three new rank9 source conferences preserved; no gameplay application. GPT continues Rank8Damage6. <a href="'+base+output.name+'">Current checkpoint</a> · <a href="'+push['url']+'">Verified commit</a></p></section>').encode()
    p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Full prior domain map retained',p.read_bytes().replace(notice,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-GITHUB-BACKUP-53',recordedAtUtc=now,previousCheckpoint=info(old),
        status='Verified GitHub backup through52; latest pertinent owner discussions remain reconciled; actual Rank8Damage6 conference is still responding.',
        navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],
        latestPreviouslyVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':52,'receipt':info(receipt),'url':push['url']},
        lastUsageObservation={'usedPercent':8,'remainingPercent':92,'stopAtRemainingPercent':20},
        previousGoalTurnClassification='progress: checked actual GPT discussions, verified current decision bindings and backed up complete preserved progress through52 without mechanic application.',
        laterLocalWork='Only this post-push checkpoint, its fresh GPT observation, verification/navigation and push receipt follow the verified backup through52.',
        nextAction='Retrieve the active Rank8Damage6 conference when complete, then confer on Rank7IdentityCasting5. Continue full prepared conferences and68 ungrouped rank9 identities with owner implementation reservation and source fidelity. Stop at20 percent remaining.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation']=info(native)
    output.write_bytes(enc(cp))
    for p,raw in originals.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    ck('No membership or implementation changes',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
    check.write_bytes(enc({'recordedAtUtc':now,'checkpoint':info(output),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'implementationApplied':False,'scope':'Backup receipt and navigation/source preservation; no new engine tests or authored acceptance.'}))
    print(json.dumps({'checkpoint':info(output),'verification':info(check),'checks':len(checks),'failures':0}))

if __name__=='__main__':main()
