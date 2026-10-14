"""Apply the verified nine TEX edits and five navigation notes, preserving originals."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, shutil
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game';D=A/'teaching-nine-exact-reviewer-files'
B=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\teaching-tex-reproduction')
F=B/'frozen';W=B/'working';N=B/'nested-originals';BACK=A/'teaching-before-tex-fulfillment'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def h(p):return sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':h(p)}
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

assert not BACK.exists(), 'One-use application already started'
c=load(D/'TEX_EXACT_CORRECTIONS.json');ops=c['operations'];groups={x['path'] for x in ops}
check=load(A/'TEACHING_TEX_LOCAL_EXACT_AMENDMENTS.json');assert check['checks']==621 and not check['failed']
assert not load(A/'teaching-tex-local-source/TEACHING_READ_ONLY_AUDIT.json')['failedChecks']
assert not load(A/'TEACHING_TEX_LOCAL_FOCUSED_REFERENCES.json')['failed']
mf=load(F/'FILE_MANIFEST.json')
for rel in load(A/'TEACHING_TEX_LOCAL_PREPARATION.json')['liveDiskPayloadsUnchanged']:
    assert h(G/rel)==mf[rel]['sha256'],rel
for op in ops:assert h(G/op['path'])==op['beforeFileSha256'],op['id']
nav=load(A/'CHARACTER_CREATION_NAVIGATION_CANDIDATE_RECEIPT.json')
assert h(G/nav['original'])==nav['originalSha256']
q=load(A/'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json')
dispositions=load(D/'TEX_TE_01_29_DISPOSITIONS.json')
assert len(dispositions['cases'])==29 and not dispositions['unresolvedSourceQuestions']
assert [x['submittedQuestion'] for x in dispositions['cases']]==q['questions']
assert len({x['id'] for x in dispositions['cases']})==29
cases=load(D/'TEX_FINITE_ACCEPTANCE_CASES.json');assert len(cases['cases'])==16
assert all(x['runtimeExecuted'] is False for x in cases['cases'])
paths=groups|set(q['candidateFiles'])|{nav['original'],c['administrativeFulfillment']['coverageJsonPath'],'DescentReviewChanges/ReviewBible/docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md',c['administrativeFulfillment']['advancedStatusPath'],'START_HERE.md','docs/audit/2026-10-08/full-game/GPT_REVIEW_CONTINUATION_HANDOFF.md'}
originals={}
for rel in sorted(paths):
    src=G/rel;dest=BACK/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest);originals[rel]=rec(src)
for rel in sorted(groups):
    src=W/rel;assert h(src)==check['changedCurrentFiles'][rel]['correctedBeforeLabelsSha256']
    (G/rel).write_bytes(src.read_bytes());assert h(G/rel)==h(src)
# Keep LF in the governing chapter and never import the candidate banner.
src=BACK/nav['original'];before=src.read_bytes();assert b'\r\n' not in before
text=before.decode('utf-8')
for change in nav['changes']:
    assert text.count(change['old'])==1
    text=text.replace(change['old'],change['proposedReplacement'],1)
after=text.encode('utf-8');(G/nav['original']).write_bytes(after)
reverse=text
for change in reversed(nav['changes']):
    assert reverse.count(change['proposedReplacement'])==1
    reverse=reverse.replace(change['proposedReplacement'],change['old'],1)
assert reverse.encode('utf-8')==before and nav['candidateBanner'] not in text
erratum=G/c['erratumRepositoryPath'];assert not erratum.exists();shutil.copy2(D/c['erratumArtifact'],erratum)
unchanged=[]
for rel in load(A/'TEACHING_TEX_LOCAL_PREPARATION.json')['liveDiskPayloadsUnchanged']:
    if rel not in groups|{nav['original']}:
        assert h(G/rel)==mf[rel]['sha256'],rel;unchanged.append(rel)
assert h(G/q['candidateFiles'][-1])=='633d8fca919c5ad02733c9944a1892e30895e75a2551e9c841f6742f269e3d68'
proofs=D/'corrected-manuscript-proofs'
for src in proofs.rglob('*.md'):
    rel=src.relative_to(proofs);assert h(G/rel)==h(src),rel
receipt={'reviewId':'TEX-EXACT-2026-10-11','createdAt':datetime.now(timezone.utc).isoformat(),'status':'All nine operative replacements and five navigation notes applied; labels/admin pending', 'authority':{'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','replyId':'cb2e5a59-d467-4439-903f-1af7c37c7838','verdict':rec(D/'TEX_NINE_TEACHING_EXACT_VERDICT.md'),'archive':rec(A/'DD_Teaching_9_Exact_Verdict_and_Evidence.zip')},'originalBackup':BACK.relative_to(G).as_posix(),'originals':originals,'operativeEdits':ops,'preLabelArtifacts':{rel:rec(G/rel) for rel in q['candidateFiles']},'correctedCurrentFiles':{rel:rec(G/rel) for rel in sorted(groups)},'navigation':{'original':nav['original'],'beforeSha256':nav['originalSha256'],'after':rec(G/nav['original']),'reversesToOriginalBytes':True,'lineEndings':'LF','changes':nav['changes'],'mechanicsChanged':False},'erratum':rec(erratum),'unchangedSubmittedLivePayloads':unchanged,'questionDispositions':dispositions,'finiteAuthoredAcceptanceCases':cases,'validation':{'sourceChecks':2262,'exactAmendmentChecks':621,'focusedReferenceChecks':67,'originalLinks':158,'correctedLinks':162,'failed':0,'pdf':'Unchanged reviewed original; no regeneration or newly claimed render checks','fullIntegratedDeviceValidatorRun':False},'sourceInformationDeleted':0,'runtimeApproved':False,'balanceApproved':False,'humanTrialsPerformed':False,'wholeGameFlowComplete':False,'githubPushed':False,'cosmologyReviewed':False}
save(A/'TEACHING_TEX_PRELABEL_FULFILLMENT.json',receipt)
print(json.dumps({'operativeEdits':9,'existingFilesCorrected':7,'navigationNotes':5,'unchangedOtherSubmittedLivePayloads':len(unchanged),'originalFilesBackedUp':len(originals),'pdfUnchanged':True,'labelsAdminPending':True}))
