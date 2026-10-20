"""Record the verified proposed Ready successor and next actual GPT conference."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
from collections import Counter
import hashlib
import json

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'


def read(p): return json.loads(p.read_bytes())
def encoded(d): return (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode()
def info(p):
    raw = p.read_bytes()
    return {'path':p.relative_to(G).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def main():
    now = datetime.now(timezone.utc).isoformat()
    oldcp = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEFENSE_FORM_50.json'
    cpfile = A / 'ACTIVE_AUTHORING_CHECKPOINT_READY_SUCCESSOR_RANK8_REVIEW_51.json'
    oldq = R / 'data/director/spell_review/remaining_work_queue_41.json'
    qfile = oldq.with_name('remaining_work_queue_42.json')
    oldledger = A / 'PERTINENT_GPT_DECISIONS_2026_10_20_01.json'
    ledgerfile = oldledger.with_name('PERTINENT_GPT_DECISIONS_2026_10_20_02.json')
    receiptfile = A / 'COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json'
    nativefile = A / 'GPT_PART5_RANK8_DAMAGE_CONFERENCE_09_CONFIRMED_NATIVE.json'
    requestfile = A / 'GPT_PART5_RANK8_DAMAGE_CONFERENCE_09_REQUEST.txt'
    outcheck = A / 'ACTIVE_AUTHORING_CHECKPOINT_READY_SUCCESSOR_RANK8_REVIEW_51_CHECK.json'
    keep = A / 'navigation-before-ready-successor-rank8-review-51'
    assert not any(p.exists() for p in [cpfile,qfile,ledgerfile,outcheck,keep])
    cp, q, ledger, receipt, native = map(read,[oldcp,oldq,oldledger,receiptfile,nativefile])
    q0 = deepcopy(q)
    checks = []
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)}); assert ok,label
    turn = next(t for t in native['turns'] if any(i.get('type')=='userMessage'
        and i.get('content',[{}])[0].get('text','').rstrip('\n')==requestfile.read_text(encoding='utf-8').rstrip('\n') for i in t['items']))
    ck('Actual request is active in the designated GPT chat', native['thread']['id']=='6ad4a867-f330-83e9-829e-bf2bb41a6c09' and native['thread']['status']['type']=='active')
    ck('Verified Ready successor with no application',receipt['checkCount']==751 and receipt['failures']==0
        and not receipt['implementationApplied'] and not receipt['downloadedCodeExecuted']
        and info(G/receipt['archive']['path'])==receipt['archive'])
    protected_paths = [oldcp,oldq,oldledger,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
    protected_paths += [G/cp[k]['path'] for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry']]
    protected_paths += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
    protected = {p:p.read_bytes() for p in protected_paths}
    root = G/receipt['extractedRoot']
    ledger.update(id='PERTINENT-GPT-DECISIONS-2026-10-20-02',recordedAtUtc=now,previousLedger=info(oldledger))
    choice = next(d for d in ledger['mechanicalDecisions'] if d['id']=='COPY-READY-PREPARATION-ONLY')
    choice.update(status='owner-delegated-gpt-selection-exact-successor-locally-verified-unapplied',
        selectedPolicy='COPY-READY-ALLOWANCE-02',exactSelectedPolicy=info(root/'POLICY_SELECTION.json'),
        localPreflight=info(receiptfile),actualGptAssistant='b8ed94a4-df57-42af-9750-40f992afbbd0',
        currentIntegrationHandoff=info(root/'CODEX_HANDOFF.md'))
    ledger['readySuccessorCompleted']={'archive':receipt['archive'],'receipt':info(receiptfile),
        'nativeReturn':receipt['nativeEvidence'],'jsonProposalOperations':30,'alternativeOriginalFeatOperations':26,
        'fullHandoffReplacement':1,'scope':'Proposed authoring successor only; alternative paths must not both be applied. Full Ready remains unimplemented.'}
    ledger['nextActualConference']={'request':info(requestfile),'native':info(nativefile),'userTurn':turn['id'],'group':'rank8-damage6'}
    ledgerfile.write_bytes(encoded(ledger))
    for group in q['groups']:
        if group['group']=='rank8-damage6':
            group.update(phase='actual-source-conference-review-in-progress',
                actualReviewRequest=info(requestfile),actualNativeConfirmation=info(nativefile),
                actualUserTurn=turn['id'],latestObservedStatus='Full six-spell conference requested and verified active in Calibration Review Part 5 after Ready successor receipt.')
        elif group['group']=='rank7-identity-casting5':
            group.update(phase='source-conference-delivered-awaiting-review',
                deliveryAcknowledgment=receipt['nativeEvidence'],
                latestObservedStatus='Actual GPT final identifies this complete conference as already delivered and next after Rank8Damage6; no semantic review claimed.')
    phases={g['group']:g['phase'] for g in q['groups']}
    for old,row in zip(q0['rows'],q['rows']):
        if row['currentGroup'] in ['rank8-damage6','rank7-identity-casting5']:
            row['currentPhase']=phases[row['currentGroup']]
            row['nextAction']='Retrieve and independently review the full actual GPT conference return; no canonical application under the owner reservation.'
        ck('Complete source/index/history retained '+row['id'],all(old[k]==row[k] for k in ['completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']))
    q.update(id='REMAINING-WORK-QUEUE-42',recordedAtUtc=now,previousQueue=info(oldq),
        pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),
        latestOwnerDecisionLedger=info(ledgerfile),latestReadySuccessorPreflight=info(receiptfile))
    q['sourceBindings'].extend([info(ledgerfile),info(receiptfile),receipt['archive'],info(nativefile),info(requestfile)])
    q['limitations']+=' Current checkpoint51: preparation-only Ready successor is locally verified and unapplied; rank8-damage6 is in actual GPT conference, rank7-identity-casting5 is delivered awaiting review. Older unsent/active-Ready wording is historical. No spell membership changes.'
    ck('Membership unchanged',len(q['rows'])==323 and len(q['groups'])==39 and
        sum(r['currentGroup'] is not None for r in q['rows'])==249 and
        sum(r['currentGroup'] is None for r in q['rows'])==74)
    ck('Accepted but unapplied remains39',sum(r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied'] for r in q['rows'])==39)
    qfile.write_bytes(encoded(q))
    paths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']
    nav={p:p.read_bytes() for p in paths}; keep.mkdir(); base='docs/audit/2026-10-08/full-game/'
    for p,raw in nav.items(): (keep/p.name).write_bytes(raw)
    for p,prefix in [(paths[0],''),(paths[1],'../../../')]:
        raw=nav[p];pos=raw.index(b'\n')+1
        notice=('\n**Current review — 20 October 2026:** [Checkpoint 51]('+prefix+base+cpfile.name+') records the completed preparation-only copied-feat Ready proposal: 751 local preservation/reconstruction/case-data checks passed; no rule implementation. [Current owner decisions]('+prefix+base+ledgerfile.name+') and the exact handoff supersede the older both-round accounting. GPT is now reviewing the six rank8 damage spells; rank7 identity/casting follows. [Queue 42]('+prefix+qfile.relative_to(G).as_posix()+') retains 525 reviewed / 323 pending / 249 standalone, 39 accepted but unapplied, and 74 ungrouped rank9 identities. GitHub backup remains through checkpoint 48.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]);ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
    p=paths[2];raw=nav[p];pos=raw.index(b'</h1>')+len(b'</h1>')
    banner=('<section class="sequence" aria-label="Current Ready and rank8 review"><p><strong>Checkpoint 51: preparation-only Ready proposal locally verified.</strong> 751 preservation, exact reconstruction and case-data checks passed; full Ready is still unimplemented. GPT is reviewing six rank8 damage spells. Applied counts and all 39 accepted-but-unapplied identities remain unchanged. <a href="'+base+cpfile.name+'">Current checkpoint</a> · <a href="'+base+ledgerfile.name+'">Current owner decisions</a></p></section>').encode()
    p.write_bytes(raw[:pos]+banner+raw[pos:]);ck('All original domain navigation retained',p.read_bytes().replace(banner,b'',1)==raw)
    cp.update(id='ACTIVE-AUTHORING-READY-SUCCESSOR-RANK8-REVIEW-51',recordedAtUtc=now,
        previousCheckpoint=info(oldcp),decisionLedger=info(ledgerfile),currentWorkQueue=info(qfile),
        status='Preparation-only Ready exact proposed successor locally verified; full Rank8Damage6 conference active in actual GPT chat.',
        completedReadySuccessor={'archive':receipt['archive'],'localReceipt':info(receiptfile),'policy':info(root/'POLICY_SELECTION.json'),'handoff':info(root/'CODEX_HANDOFF.md'),'implementationApplied':False},
        activeGptReviewAtLastVerifiedObservation={'threadId':native['thread']['id'],'title':native['thread']['title'],
            'userTurn':turn['id'],'nativeConfirmation':info(nativefile),'scope':'Complete Rank8Damage6 source conference; Rank7IdentityCasting5 follows.','sent':True,'completedResponseReceived':False},
        navigation=[info(p) for p in paths],preservedNavigation=[info(keep/p.name) for p in paths],
        previousGoalTurnClassification='progress: verified and preserved exact Ready successor; advanced actual GPT conference and supersession references.',
        laterLocalWork='Checkpoints49–51, queues40–42, death/recovery7, defense/form8, the Ready successor and local preflight, newer owner ledger, navigation and GPT request09 follow the last GitHub backup through48.',
        nextAction='Retrieve and independently verify the live Rank8Damage6 conference. Continue Rank7IdentityCasting5 and remaining prepared/ungrouped sources, retaining source fidelity and the owner implementation reservation. Stop at20 percent remaining.')
    cpfile.write_bytes(encoded(cp))
    for p,raw in protected.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==raw)
    outcheck.write_bytes(encoded({'recordedAtUtc':now,'checkpoint':info(cpfile),'queue':info(qfile),'ledger':info(ledgerfile),
        'checks':checks,'checkCount':len(checks),'failures':0,'implementationApplied':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cpfile),'queue':info(qfile),'ledger':info(ledgerfile),'check':info(outcheck),'checks':len(checks)}))


if __name__=='__main__':main()
