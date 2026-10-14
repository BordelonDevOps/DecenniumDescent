"""Record the real attachment-bearing request; never resend on a click timeout."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 p=A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json';assert not p.exists()
 prep=read(A/'ADVANCED_CRAFT_JOINT_DISPATCH_PREPARATION.json');cap=read(A/'ADVANCED_CRAFT_JOINT_REQUEST_CAPTURE.json');turn=cap['turns'][0]
 assert turn['id']=='6b7737b0-b71b-4bfc-8627-4705e81fc26c'
 user=next(i for i in turn['items'] if i['type']=='userMessage');text='\n'.join(x['text'] for x in user['content'] if x['type']=='text')
 prompt=(A/prep['promptFile']).read_text(encoding='utf-8')
 assert text.split('\n\n[User attached',1)[0].rstrip()==prompt.rstrip() and '[User attached 1 file;' in text
 assert any(x['name']==prep['bundleFile'] for x in cap['attachments'])
 assert sha(A/prep['bundleFile'])==prep['bundleSha256'] and all(sha(G/n)==h for n,h in prep['currentFileHashes'].items())
 record={'status':'Sent once; actual attachment-bearing source request confirmed; verdict pending','threadId':cap['thread']['id'],'turnId':turn['id'],'observedAtUtc':datetime.now(timezone.utc).isoformat(),'bundleFile':prep['bundleFile'],'bundleSha256':prep['bundleSha256'],'bundleBytes':prep['bundleBytes'],'payloadFiles':prep['payloadFiles'],'promptFile':prep['promptFile'],'promptSha256':prep['promptSha256'],'actualPromptMatches':True,'currentUserMessageAttachedFileCount':1,'actualBundleNamePresent':True,'threadAttachmentListIncludesEarlierFiles':True,'requestCapture':'ADVANCED_CRAFT_JOINT_REQUEST_CAPTURE.json','clickTimedOutButSubmissionConfirmed':True,'resubmissionPerformed':False,'sourceVerdictPending':True,'recipesReviewed':520,'recipesPending':167,'newAdvancedApprovals':0,'currentFileHashes':prep['currentFileHashes'],'cosmology':'post-verified-push only'}
 dump(p,record)
 prep.update({'sent':True,'actualTurnId':turn['id'],'submissionFile':p.name});dump(A/'ADVANCED_CRAFT_JOINT_DISPATCH_PREPARATION.json',prep)
 op=A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';obs=read(op);obs['currentRequest']={'scope':'Advanced167 complete-source conference with current Tinker and pending feat comparisons','submissionFile':p.name,'requestCapture':record['requestCapture'],'actualLastObservedTurn':turn['id'],'actualUserPromptMatches':True,'actualAttachedFileCount':1,'bundleFile':prep['bundleFile'],'bundleSha256':prep['bundleSha256'],'sourceVerdictPending':True,'notebookStatusAsObserved':cap['thread']['status']['type'],'resubmissionPerformed':False,'newAdvancedApprovals':0,'browserTabId':'125745441','nextAction':'Capture actual complete source verdict; no resend while active'}
 obs['nextAction']='Read the complete advanced167 source-authoring verdict and integrate finite directions; do not resend the confirmed attachment-bearing request.';obs['observedAtUtc']=record['observedAtUtc'];dump(op,obs)
 note='**Active advanced crafting review:** The complete138-file archive for all167 advanced formulas is submitted once in Calibration Review Part2 (turn `'+turn['id']+'`). The actual request matches the saved prompt and confirms one current attachment. Await its source-authoring verdict before building exact cards; no new advanced recipe is approved. Gathering remains reviewed128, bringing totals520/687 and public333/433.\n\n'
 for fp in [G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md']:
  s=fp.read_text(encoding='utf-8');i=s.index('\n\n')+2;fp.write_text(s[:i]+note+s[i:],encoding='utf-8')
 print(json.dumps({k:record[k] for k in ['status','turnId','payloadFiles','actualPromptMatches','currentUserMessageAttachedFileCount','newAdvancedApprovals']}))
if __name__=='__main__':main()
