"""Record the confirmed attachment-bearing exact request without resending."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    dest=A/'ADVANCED_CRAFT_EXACT_SUBMISSION.json';assert not dest.exists()
    prep=read(A/'ADVANCED_CRAFT_EXACT_REVIEW_PREPARATION.json');cap=read(A/'ADVANCED_CRAFT_EXACT_REQUEST_CAPTURE.json')
    turn=cap['turns'][0];assert turn['id']=='dbffb1f2-10d4-4454-a983-2e3850f654eb'
    msg=next(x for x in turn['items'] if x['type']=='userMessage')
    text='\n'.join(x['text'] for x in msg['content'] if x['type']=='text')
    prompt=A/'CODEX_ADVANCED_CRAFT_EXACT_REVIEW_PROMPT.txt'
    assert text.split('\n\n[User attached',1)[0].rstrip()==prompt.read_text(encoding='utf-8').rstrip()
    assert '[User attached 1 file;' in text and any(x['name']==prep['bundleFile'] for x in cap['attachments'])
    assert sha(A/prep['bundleFile'])==prep['bundleSha256']
    assert all(sha(G/p)==h for p,h in prep['currentFileHashes'].items())
    rec={**prep,'status':'Sent once; complete exact-candidate review pending','sent':True,'threadId':cap['thread']['id'],'turnId':turn['id'],'observedAtUtc':datetime.now(timezone.utc).isoformat(),'actualPromptMatches':True,'currentUserMessageAttachedFileCount':1,'actualBundleNamePresent':True,'promptFile':prompt.name,'promptSha256':sha(prompt),'requestCapture':'ADVANCED_CRAFT_EXACT_REQUEST_CAPTURE.json','clickTimedOutButSubmissionConfirmed':True,'resubmissionPerformed':False,'exactVerdictPending':True,'recipesReviewed':520,'publicRecipesReviewed':333}
    dump(dest,rec)
    backup=A/'advanced167-before-exact-submission-checkpoint';assert not backup.exists();backup.mkdir()
    note='**Advanced crafting exact review submitted:** All167 internal cards,100 public versions, complete guides/body catalogues and37 authored worked sequences are now with GPT in Calibration Review Part2 (turn `'+turn['id']+'`). Local source/manuscript/public-envelope and numeric checks pass; GPT’s exact semantic verdict remains pending. Trap-spring correction ADV-EDIT-01 and the TD-08 one-device/two-Dissonance transcription correction are included. See the [submission receipt](docs/audit/2026-10-08/full-game/ADVANCED_CRAFT_EXACT_SUBMISSION.json) and [player guide](DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md). Counts remain520/687 reviewed and public333/433; no new approvals, deletion, push or cosmology review.'
    for file in [G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md']:
        shutil.copy2(file,backup/file.name);s=file.read_text(encoding='utf-8');parts=s.split('\n\n',2);n=note
        if file.parent==A:n=n.replace('docs/audit/2026-10-08/full-game/ADVANCED_CRAFT_EXACT_SUBMISSION.json','ADVANCED_CRAFT_EXACT_SUBMISSION.json').replace('DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md','../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md')
        s=parts[0]+'\n\n'+n+'\n\n'+parts[2]
        s=s.replace('All167 advanced drafts written; use-sequence checks and exact review remain.','All167 advanced drafts and37 worked sequences submitted; exact semantic verdict pending.')
        file.write_text(s,encoding='utf-8')
    for name in ['ADVANCED_CRAFT_CANDIDATE_READINESS.json','ADVANCED_CRAFT_AUTHORING_PROGRESS.json']:
        file=A/name;shutil.copy2(file,backup/name);obj=read(file)
        obj.update({'status':'exact-authored-operational-review-submitted-verdict-pending','exactReviewSubmitted':True,'exactReviewTurnId':turn['id'],'exactSubmissionFile':dest.name,'nextAction':'Capture the completed exact verdict, inspect its complete artifacts and implement genuine named corrections. Do not resend this request.'})
        dump(file,obj)
    file=A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';shutil.copy2(file,backup/file.name);obs=read(file)
    obs['currentRequest']={'scope':'All167 actual advanced candidates,100 complete public envelopes and37 qualitative sequences','submissionFile':dest.name,'actualLastObservedTurn':turn['id'],'actualUserPromptMatches':True,'actualAttachedFileCount':1,'bundleFile':prep['bundleFile'],'bundleSha256':prep['bundleSha256'],'exactVerdictPending':True,'browserTabId':'125745449','resubmissionPerformed':False,'nextAction':'Read the completed exact-candidate verdict; do not resend on browser timeouts.'}
    obs['advancedCandidateProgress']=read(A/'ADVANCED_CRAFT_CANDIDATE_READINESS.json')
    obs['nextAction']='Capture complete advanced exact review; independent remaining-work preparation may continue while GPT reviews.'
    obs['observedAtUtc']=rec['observedAtUtc'];dump(file,obs)
    print(json.dumps({k:rec[k] for k in ['status','turnId','actualPromptMatches','payloadFiles','bundleSha256','newApprovals']}))
if __name__=='__main__':main()
