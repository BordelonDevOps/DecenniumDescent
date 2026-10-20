"""Record actual GPT return and dispatch without adopting gameplay proposals."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'

def read(p): return json.loads(p.read_bytes())
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def binding(p):
    raw = p.read_bytes()
    return {'path':p.relative_to(G).as_posix(), 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    old = A / 'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_ILLUSION_REALITY_66.json'
    out = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK7_RETURN_RANK8_DISPATCH_67.json'
    report = A / 'ACTIVE_AUTHORING_CHECKPOINT_RANK7_RETURN_RANK8_DISPATCH_67_CHECK.json'
    queueout = R / 'data/director/spell_review/remaining_work_queue_54.json'
    preserved = A / 'navigation-before-rank7-return-rank8-dispatch-67'
    script = A / Path(__file__).name
    assert not any(p.exists() for p in [out, report, queueout, preserved, script])
    checks = []
    def ck(label, ok):
        checks.append({'check':label, 'passed':bool(ok)})
        assert ok, label
    cp = read(old)
    ck('Exact checkpoint66', binding(old)['sha256'] == '702a76906eaf6add7cfba33012b167c5e976fb3193547febd6d3573f473c3886')
    protected = [old, R/'data/public/spell_playtests/catalog.json', R/'data/playtest/game_development_coverage.json']
    for key in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
        b = cp[key]; ck('Current authority binding ' + key, binding(G/b['path']) == b); protected.append(G/b['path'])
    for b in cp['canonicalHelperBaselinesUnchanged']:
        ck('Canonical helper binding ' + b['path'], binding(G/b['path']) == b); protected.append(G/b['path'])
    originals = {p:p.read_bytes() for p in protected}
    qpath = G / cp['currentWorkQueue']['path']; previous = read(qpath); q = copy.deepcopy(previous)
    ck('Original queue53 counts', len(q['groups']) == 49 and q['preparedOrActualReviewIdentityCount'] == 305 and q['originalSourceOrReceiptWorkCount'] == 18)
    preflightpath = A/'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_LOCAL_PREFLIGHT.json'; preflight = read(preflightpath)
    ck('Rank7 independent preservation checks', preflight['checkCount'] == 577 and preflight['failures'] == 0 and all(c['passed'] for c in preflight['checks']))
    for key in ['archive','model','nativeFinal']:
        b = preflight[key]; ck('Rank7 verified artifact ' + key, binding(G/b['path']) == b)
    nativepath = A/'GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_DISPATCH_NATIVE.json'; native = read(nativepath)
    textpath = A/'GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_DISPATCH_TEXT.txt'
    user = native['turns'][0]['items'][0]
    ck('Actual submitted user turn', user['id'] == '939b0d09-faf6-4c89-baa6-759aa484eb2e' and user['type'] == 'userMessage')
    submitted = user['content'][0]['text'].split('\n\n[User attached')[0]
    ck('Actual submitted text equals saved request', submitted == textpath.read_text(encoding='utf-8').rstrip('\n'))
    ck('Actual native GPT response active', native['thread']['status']['type'] == 'active')
    zipfile = A/'DD_Rank8_Damage6_Local_Corrections_01.zip'
    ck('Submitted archive exact original bytes', len(native['attachments']) == 1 and native['attachments'][0]['name'] == zipfile.name and Path(native['attachments'][0]['path']).read_bytes() == zipfile.read_bytes())
    ck('Submitted archive expected binding', binding(zipfile)['sha256'] == 'c8264a558ae3e6f6581f3f1d32dc1b4ac4866908cec7c732d23028590a1003ac' and binding(zipfile)['bytes'] == 5204994)
    dispatch = {'threadId':native['thread']['id'], 'title':native['thread']['title'], 'userTurn':user['id'], 'request':binding(textpath), 'fullPreparedRequest':binding(A/'GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_REQUEST.txt'), 'archive':binding(zipfile), 'nativeConfirmation':binding(nativepath), 'sent':True, 'completedResponseReceived':False, 'scope':'Bounded full correction conference for eight independent local Rank8Damage6 findings.', 'latestObservedStatus':'Actual submitted text and archive verified; native thread active. No corrected successor received at this observation.', 'attachmentBytesIndependentlyVerified':True}
    received = {'archive':preflight['archive'], 'model':preflight['model'], 'nativeFinal':preflight['nativeFinal'], 'localPreflight':binding(preflightpath), 'assistantTurn':'9b85bf4a-deeb-4a01-8d53-9a9a8eac6dbd', 'status':'FULL_PROPOSED_RETURN_PRESERVED_PENDING_LOCAL_SEMANTIC_REVIEW', 'sourceFiles':68, 'laterContextFiles':10, 'exactOperationsForwardAndReverse':27, 'preservationChecks':577, 'mainCases':10, 'independentBranches':39, 'conditionalBranches':11, 'newAcceptedIdentities':0, 'implementationApplied':False, 'nativeTextLimit':preflight['nativeFinalLimit']}
    for group in q['groups']:
        if group['group'] not in ('rank7-identity-casting5','rank8-damage6'): continue
        group['priorObservationBefore67'] = {k:copy.deepcopy(group[k]) for k in ('phase','latestObservedStatus')}
        if group['group'] == 'rank7-identity-casting5':
            group.update(phase='returned-proposed-conference-pending-local-semantic-review', latestObservedStatus='Completed final received and full archive independently preserved with577 checks; five identities not yet locally accepted.', completedReturn=received, newAcceptedIdentities=0, returnedProposedMainCases=10, returnedProposedBranches=39)
        else:
            group.update(phase='bounded-correction-conference-actually-sent', latestObservedStatus='Full eight-finding correction request and exact archive submitted in actual user turn939b0d09-faf6-4c89-baa6-759aa484eb2e; native GPT is responding.', actualCorrectionDispatch=dispatch)
    for row in q['rows']:
        if row.get('currentGroup') not in ('rank7-identity-casting5','rank8-damage6'): continue
        row['previousObservationBefore67'] = {k:copy.deepcopy(row[k]) for k in ('currentPhase','nextAction')}
        if row['currentGroup'] == 'rank7-identity-casting5':
            row.update(currentPhase='returned-proposed-conference-pending-local-semantic-review', nextAction='Independently review all full proposed Rank7 procedures and10 main/39 branch cases; preserve actual source boundaries and no canonical application.')
        else:
            row.update(currentPhase='bounded-correction-conference-actually-sent', nextAction='Retrieve the actual full bounded Rank8 correction response when complete; independently reconcile all eight findings and complete mirrors before semantic acceptance.')
        ck('Acceptance remains false ' + row['id'], not row['semanticAcceptanceClaimed'])
    q.update(id='REMAINING-WORK-QUEUE-54', recordedAtUtc=datetime.now(timezone.utc).isoformat(), previousQueue=binding(qpath), currentRank7Return=received, currentRank8ActualCorrectionDispatch=dispatch)
    q['latestActualReviewEvidence'] += [binding(preflightpath),binding(nativepath),binding(A/'GPT_PERTINENT_RECHECK_67.json')]
    ck('All queue identities and source rows retained', len(q['rows']) == len(previous['rows']) and [r['id'] for r in q['rows']] == [r['id'] for r in previous['rows']] and all(r['completeCurrentSourceAndAccess'] == p['completeCurrentSourceAndAccess'] and r['currentIndexEntryUnchanged'] == p['currentIndexEntryUnchanged'] for r,p in zip(q['rows'],previous['rows'])))
    ck('Group membership and all unrelated group records unchanged', all(g == p if g['group'] not in ('rank7-identity-casting5','rank8-damage6') else g['identities'] == p['identities'] and g['candidate'] == p['candidate'] for g,p in zip(q['groups'],previous['groups'])))
    ck('Counts and original source bindings unchanged', q['ordinarySpellCounts'] == previous['ordinarySpellCounts'] and q['sourceBindings'] == previous['sourceBindings'])
    queueout.write_bytes(enc(q))
    navpaths = [G/'START_HERE.md', R/'docs/DEVELOPMENT_DIRECTION.md', G/'REVIEW_MAP.html']
    for b in cp['navigation']: ck('Previous navigation binding ' + b['path'], binding(G/b['path']) == b)
    nav = {p:p.read_bytes() for p in navpaths}; preserved.mkdir()
    for p,raw in nav.items(): (preserved/p.name).write_bytes(raw)
    base = 'docs/audit/2026-10-08/full-game/'
    for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
        raw = nav[p]; pos = raw.index(b'\n')+1
        notice = ('\n**Current GPT review — 20 October 2026:** [Checkpoint67]('+prefix+base+out.name+') records the complete Rank7 identity/casting5 return, independently preserved with577 checks and awaiting local semantic review. The eight-finding Rank8 correction request and complete archive are actually sent; GPT is responding. Queue54 retains305 grouped and18 ungrouped pending identities. Applied525/323/249,173 interfaces and39 accepted-but-unapplied remain unchanged. Owner implementation reservation retained. The verified GitHub backup still extends through checkpoint65.\n').encode()
        p.write_bytes(raw[:pos]+notice+raw[pos:]); ck('Original navigation retained ' + p.name,p.read_bytes().replace(notice,b'',1) == raw)
    p = navpaths[2]; raw = nav[p]; pos = raw.index(b'</h1>')+len(b'</h1>')
    notice = ('<section class="sequence" aria-label="Current GPT return and correction dispatch"><p><strong>Checkpoint67: Rank7 return preserved; Rank8 corrections sent.</strong> Rank7 semantic review remains pending. Queue54 retains305 grouped and18 ungrouped identities. Applied counts and39 accepted-but-unapplied remain unchanged. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode()
    p.write_bytes(raw[:pos]+notice+raw[pos:]); ck('Original review map retained',p.read_bytes().replace(notice,b'',1) == raw)
    cp['previousGptObservationBefore67'] = copy.deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
    cp.update(id='ACTIVE-AUTHORING-RANK7-RETURN-RANK8-DISPATCH-67',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=binding(old),status='Full Rank7 return preserved with577 checks; Rank8 bounded corrections actually submitted. Local semantic review and reserved implementation remain separate.', currentWorkQueue=binding(queueout),completedRank7IdentityCasting5Return=received,activeGptReviewAtLastVerifiedObservation=dispatch,pertinentRecheck=binding(A/'GPT_PERTINENT_RECHECK_67.json'),navigation=[binding(p) for p in navpaths],preservedNavigation=[binding(preserved/p.name) for p in navpaths],queueObservationSupersession='Queue54 changes only review observations for eleven existing identities; all49 groups,305 grouped and18 ungrouped identities remain. Rank7 is received; Rank8 corrections are actually sent.',nextAction='Continue independent full Rank7 semantic review while GPT handles the eight Rank8 findings. Then continue remaining18 ungrouped rank9 source preparation, including Elemental Convergence/Fusion. Preserve owner implementation reservation and stop at20 percent remaining.',previousGoalTurnClassification='progress: verified and recorded GitHub source backup through65. Current67 preserves full Rank7 final and dispatches complete Rank8 correction conference.',laterLocalWork='Checkpoint66 and this Rank7 intake,Rank8 dispatch,Queue54 and checkpoint67 are local work after the verified backup through65.',lastUsageObservation={'usedPercent':21,'remainingPercent':79,'stopAtRemainingPercent':20})
    cp['completedRank8Damage6Return']['actualCorrectionDispatch'] = dispatch
    ck('No applied or accepted-count increment',cp['authoredCounts'] == {'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied'] == 39 and not cp['implementationApplied'])
    out.write_bytes(enc(cp)); script.write_bytes(Path(__file__).read_bytes())
    for p,raw in originals.items(): ck('Protected authority unchanged ' + p.relative_to(G).as_posix(),p.read_bytes() == raw)
    report.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpoint':binding(out),'queue':binding(queueout),'checks':checks,'checkCount':len(checks),'failures':0,'scope':'Actual full return preservation, native dispatch/attachment evidence and queue/navigation continuity only; no new semantic acceptance or runtime/implementation claim.','sourceInformationDeleted':0,'implementationApplied':False}))
    print(json.dumps({'checkpoint':binding(out),'queue':binding(queueout),'report':binding(report),'checks':len(checks),'failures':0}))

if __name__ == '__main__': main()
