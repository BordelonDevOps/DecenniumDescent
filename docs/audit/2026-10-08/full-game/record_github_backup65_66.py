"""Record a verified source-preservation push; apply no gameplay changes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def binding(p):
    raw=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
    old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ILLUSION_REALITY_65.json'
    out=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_ILLUSION_REALITY_66.json'
    report=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_ILLUSION_REALITY_66_CHECK.json'
    preserved=A/'navigation-before-github-illusion-reality-66'
    script=A/Path(__file__).name
    assert not any(p.exists() for p in [out,report,preserved,script])
    checks=[]
    def ck(label,ok):checks.append({'check':label,'passed':bool(ok)});assert ok,label
    cp=read(old)
    ck('Exact checkpoint65',binding(old)['sha256']=='1d4650e44d0733de215bdb5bf0867d034b30ff741c996a2b35b462d2663403d1')
    pushpath=G/'docs/audit/2026-10-20/github-snapshot-illusion-reality65/PUSH_RECEIPT.json';push=read(pushpath)
    ck('Verified remote backup through65',push['commit']==push['remoteMain'] and push['baseCommit']=='111a098b52763862ac4c98f7803e8c1d556668e2' and push['worktreeClean'] and push['trackedEntriesDeleted']==push['sourceInformationDeleted']==0)
    ck('Verified entire selected snapshot and prior entries',push['expectedBlobsVerified']>28645 and push['priorTrackedEntriesPreserved']==28826)
    protected=[old,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    for key in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
        b=cp[key];ck('Current authority binding '+key,binding(G/b['path'])==b);protected.append(G/b['path'])
    for b in cp['canonicalHelperBaselinesUnchanged']:
        ck('Canonical helper baseline '+b['path'],binding(G/b['path'])==b);protected.append(G/b['path'])
    for key in ['nativeConfirmation','latestBrowserStatus']:
        b=cp['activeGptReviewAtLastVerifiedObservation'][key];ck('Prior actual GPT evidence preserved '+key,binding(G/b['path'])==b)
    originals={p:p.read_bytes() for p in protected};q=read(G/cp['currentWorkQueue']['path'])
    ck('Queue53 membership unchanged',len(q['groups'])==49 and q['preparedOrActualReviewIdentityCount']==305 and q['originalSourceOrReceiptWorkCount']==18)
    ck('Membership and implementation unchanged',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
    navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    for b in cp['navigation']:ck('Previous navigation binding '+b['path'],binding(G/b['path'])==b)
    nav={p:p.read_bytes() for p in navpaths};preserved.mkdir()
    for p,raw in nav.items():(preserved/p.name).write_bytes(raw)
    base='docs/audit/2026-10-08/full-game/'
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Current backup and review — 20 October 2026:** [Checkpoint66]('+prefix+base+out.name+') records the verified [GitHub backup through checkpoint65]('+push['url']+'). Complete summon-hosts5,impact-exile4 and illusion-reality5 source conferences are preserved. Applied525/323/249,173 interfaces and39 accepted-but-unapplied remain unchanged. Queue53 groups305 pending identities and leaves18 ungrouped. Rank8 corrections remain queued; latest successful native Rank7 evidence is64,with visible generation at65 and transient native read limits. No canonical gameplay or cosmology application.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous navigation bytes retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=navpaths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    notice=('<section class="sequence" aria-label="Verified development backup through checkpoint65"><p><strong>Checkpoint66: backup through65 verified.</strong> Three full rank9 source packets are preserved. Queue53:305 grouped pending identities,18 ungrouped. Rank8 corrections and Rank7 response remain pending. No gameplay application. <a href="'+base+out.name+'">Current checkpoint</a> · <a href="'+push['url']+'">Verified commit</a></p></section>').encode()
    p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Previous review map bytes retained',p.read_bytes().replace(notice,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-GITHUB-ILLUSION-REALITY-66',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=binding(old),status='Verified preservation push through65. Three source conferences remain undecided; Rank8 corrections remain unsent. No canonical gameplay or cosmology application.',navigation=[binding(p) for p in navpaths],preservedNavigation=[binding(preserved/p.name) for p in navpaths],latestPreviouslyVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':65,'receipt':binding(pushpath),'url':push['url']},previousGoalTurnClassification='progress: full illusion/reality5 preparation and checkpoint65. Current turn verifies and pushes the selected preservation snapshot through65 with no tracked deletions.',laterLocalWork='This post-push receipt,checkpoint66 and navigation follow the verified backup through65.')
    cp['activeGptReviewAtLastVerifiedObservation']['note']='Prior native64 and browser65 observations remain exact. Another fresh native read during backup66 returned Too many requests; it does not prove termination. No interruption or new message was sent. No new final response is claimed.'
    cp['lastUsageObservation']={'usedPercent':20,'remainingPercent':80,'stopAtRemainingPercent':20}
    out.write_bytes(enc(cp));script.write_bytes(Path(__file__).read_bytes())
    for p,raw in originals.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':binding(out),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'implementationApplied':False,'scope':'Verified GitHub snapshot,current authority and navigation preservation only; no new GPT verdict,semantic acceptance or runtime claim.'}))
    print(json.dumps({'checkpoint':binding(out),'report':binding(report),'checks':len(checks),'failures':0}))
if __name__=='__main__':main()
