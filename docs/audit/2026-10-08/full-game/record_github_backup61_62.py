"""Record a verified preservation push and fresh GPT observation; apply no gameplay rules."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'

def read(p):
    return json.loads(p.read_bytes())

def enc(x):
    return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()

def binding(p):
    raw = p.read_bytes()
    return {'path': p.relative_to(G).as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def main():
    old = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_PLANAR_GATES_61.json'
    out = A / 'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_PLANAR_GATES_62.json'
    report = A / 'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_PLANAR_GATES_62_CHECK.json'
    preserved = A / 'navigation-before-github-planar-gates-62'
    script = A / Path(__file__).name
    assert not any(p.exists() for p in [out, report, preserved, script])
    checks = []

    def ck(label, ok):
        checks.append({'check': label, 'passed': bool(ok)})
        assert ok, label

    cp = read(old)
    ck('Exact checkpoint61', binding(old)['sha256'] == 'c83deb106ee3e2f0c92aa290cfc102f56d55fb561724d9454347760010061e22')
    pushpath = G / 'docs/audit/2026-10-20/github-snapshot-planar-gates61/PUSH_RECEIPT.json'
    push = read(pushpath)
    ck('Verified remote backup through61', push['commit'] == push['remoteMain'] and push['baseCommit'] == '0a9c7b2bc9adc0f6773f2cb64e2dbb3296843ccc' and push['worktreeClean'] and push['trackedEntriesDeleted'] == push['sourceInformationDeleted'] == 0)
    ck('Verified entire selected snapshot', push['expectedBlobsVerified'] > 28284 and push['priorTrackedEntriesPreserved'] == 28456)
    nativepath = A / 'GPT_PART5_RANK7_LIVE_AFTER_GITHUB_BACKUP_62_NATIVE.json'
    native = read(nativepath)
    ck('Fresh actual active Rank7 request', native['thread']['id'] == '6ad4a867-f330-83e9-829e-bf2bb41a6c09' and native['thread']['status']['type'] == 'active' and native['turns'][0]['id'] == '300380f5-c52b-471a-9eb5-f8251396eac2')
    ck('No completed Rank7 response claimed', not any(i['type'] == 'agentMessage' for i in native['turns'][0]['items']))
    protected = [old, R / 'data/public/spell_playtests/catalog.json', R / 'data/playtest/game_development_coverage.json']
    for key in ['currentWorkQueue', 'currentAuthoredIndex', 'currentAcceptedInterfaceRegistry', 'decisionLedger']:
        b = cp[key]
        ck('Current authority binding ' + key, binding(G / b['path']) == b)
        protected.append(G / b['path'])
    for b in cp['canonicalHelperBaselinesUnchanged']:
        ck('Canonical helper baseline ' + b['path'], binding(G / b['path']) == b)
        protected.append(G / b['path'])
    originals = {p: p.read_bytes() for p in protected}
    q = read(G / cp['currentWorkQueue']['path'])
    ck('Queue50 membership unchanged', len(q['groups']) == 46 and q['preparedOrActualReviewIdentityCount'] == 291 and q['originalSourceOrReceiptWorkCount'] == 32)
    ck('Membership and implementation unchanged', cp['authoredCounts'] == {'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied'] == 39 and not cp['implementationApplied'])
    navpaths = [G / 'START_HERE.md', R / 'docs/DEVELOPMENT_DIRECTION.md', G / 'REVIEW_MAP.html']
    for b in cp['navigation']:
        ck('Previous navigation binding ' + b['path'], binding(G / b['path']) == b)
    nav = {p:p.read_bytes() for p in navpaths}
    preserved.mkdir()
    for p, raw in nav.items():
        (preserved / p.name).write_bytes(raw)
    base = 'docs/audit/2026-10-08/full-game/'
    for p, prefix in [(navpaths[0], ''), (navpaths[1], '../../../')]:
        raw = nav[p]
        pos = raw.index(b'\n') + 1
        notice = ('\n**Current backup and review — 20 October 2026:** [Checkpoint 62](' + prefix + base + out.name + ') records the verified [GitHub backup through checkpoint 61](' + push['url'] + '). The complete Rank8 proposed return, eight local findings and unsent correction packet are preserved, together with full knowledge/revelation5 and planar/gates5 source conferences. GPT is still responding to Rank7IdentityCasting5. Applied counts remain 525 reviewed / 323 pending / 249 standalone, with 173 interfaces and 39 accepted-but-unapplied identities. Queue50 groups 291 identities and leaves 32 ungrouped. No canonical gameplay application or broad acceptance.\n').encode()
        p.write_bytes(raw[:pos] + notice + raw[pos:])
        ck('Previous navigation bytes retained ' + p.name, p.read_bytes().replace(notice, b'', 1) == raw)
    p = navpaths[2]
    raw = nav[p]
    pos = raw.index(b'</h1>') + len(b'</h1>')
    notice = ('<section class="sequence" aria-label="Verified development backup through checkpoint61"><p><strong>Checkpoint62: backup through61 verified.</strong> Rank8 remains unaccepted with eight local findings; knowledge/revelation5 and planar/gates5 packets remain undecided. GPT continues Rank7IdentityCasting5. No gameplay application. <a href="' + base + out.name + '">Current checkpoint</a> · <a href="' + push['url'] + '">Verified commit</a></p></section>').encode()
    p.write_bytes(raw[:pos] + notice + raw[pos:])
    ck('Previous review map bytes retained', p.read_bytes().replace(notice, b'', 1) == raw)
    cp.update(id='ACTIVE-AUTHORING-GITHUB-PLANAR-GATES-62', recordedAtUtc=datetime.now(timezone.utc).isoformat(), previousCheckpoint=binding(old), status='Verified preservation push through61; GPT remains active on Rank7IdentityCasting5. Rank8 bounded corrections and rank9 source conferences remain prepared, unsent and unapplied.', navigation=[binding(p) for p in navpaths], preservedNavigation=[binding(preserved / p.name) for p in navpaths], latestPreviouslyVerifiedGitHubBackup={'commit':push['commit'],'throughCheckpoint':61,'receipt':binding(pushpath),'url':push['url']}, previousGoalTurnClassification='progress: verified and pushed the complete selected preservation snapshot through61 with no tracked deletions; checked latest actual GPT status and retained all canonical authority.', laterLocalWork='This post-push receipt, fresh native status observation, checkpoint62 and navigation follow the verified backup through61.')
    cp['activeGptReviewAtLastVerifiedObservation']['nativeConfirmation'] = binding(nativepath)
    cp['activeGptReviewAtLastVerifiedObservation']['note'] = 'Fresh native observation after the verified push still shows the actual Rank7 user turn active without a completed assistant response. No interruption or additional message sent.'
    cp['lastUsageObservation'] = {'usedPercent':16,'remainingPercent':84,'stopAtRemainingPercent':20}
    out.write_bytes(enc(cp))
    script.write_bytes(Path(__file__).read_bytes())
    for p, raw in originals.items():
        ck('Protected authority unchanged ' + p.relative_to(G).as_posix(), p.read_bytes() == raw)
    report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':binding(out),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'implementationApplied':False,'scope':'Verified GitHub snapshot, exact current authority, observed GPT status and navigation preservation only; no semantic acceptance or runtime claim.'}))
    print(json.dumps({'checkpoint':binding(out),'report':binding(report),'checks':len(checks),'failures':0}))

if __name__ == '__main__':
    main()
