from __future__ import annotations
import copy,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
FULL=ROOT/'docs/audit/2026-10-08/full-game'
AUDIT=FULL/'director-spell-review-129'
ARCHIVE=FULL/'DD_Rank8_Planar_5_Source_Conference_02.zip'
CANDIDATE=ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/rank8_planar_5_source_conference_02.json'
PREP=FULL/'RANK8_PLANAR_5_SOURCE_CONFERENCE_02_PREPARATION.json'
CHECK=FULL/'RANK8_PLANAR_5_SOURCE_CONFERENCE_02_CHECK.json'
VERIFY=AUDIT/'PLANAR5_PACKET_INDEPENDENT_VERIFICATION_165.json'
QUEUE=AUDIT/'CURRENT_SPELL_QUEUE_165.json'
HANDOFF=AUDIT/'CURRENT_HANDOFF_165.json'
RECEIPT=AUDIT/'PLANAR5_GPT_SUBMISSION_165.json'
IDS=['demiplane','maze','planar-seal','seal-of-banishment','gloom-bind']
RAW_URL='https://raw.githubusercontent.com/BordelonDevOps/DecenniumDescent/codex/ordinary-spell-review-complete/docs/audit/2026-10-08/full-game/DD_Rank8_Planar_5_Source_Conference_02.zip'
CHAT_URL='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
COMMIT='8fca38e3bfb895fce999557dba914fed9d3ec875'
MESSAGE='''GPT — please review the exact fresh Rank8 Planar5 Conference02 packet attached and published on the current GitHub branch.

ZIP: https://raw.githubusercontent.com/BordelonDevOps/DecenniumDescent/codex/ordinary-spell-review-complete/docs/audit/2026-10-08/full-game/DD_Rank8_Planar_5_Source_Conference_02.zip
Size: 22,486,077 bytes
SHA-256: 1c0ea7395a9cc04b81d26b5174dc5a178204bfecc3c77cc2321d469952ad3425
Branch commit: 8fca38e3bfb895fce999557dba914fed9d3ec875

Use current authority 730 applied-reviewed / 118 pending / 0 accepted-unapplied. Review only demiplane, maze, planar-seal, seal-of-banishment, and gloom-bind. Resolve the 24 preserved questions and return source-faithful complete procedures, all question and case dispositions, a complete hold register, and your independent semantic failure check. Keep all source, access, content, lifecycle, information, structure, runtime, balance, cosmology, and release holds explicit. Conference01 is historical 525/323 context only. Do not edit canonical files or revisit completed/applied cohorts. If the packet passes, state accepted=true and applied=false only for the exact IDs accepted; otherwise leave all unaccepted and unapplied and list exact blockers. Keep runtime, human-play, balance, cosmology, and release qualifications explicit.'''
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 prep=read(PREP); check=read(CHECK); verification=read(VERIFY)
 assert prep['status']=='PREPARED_UNSENT' and check['failures']==0 and verification['status']=='PASS' and verification['failures']==0
 assert bind(ARCHIVE)==prep['archive'] and bind(CANDIDATE)==prep['candidate']
 assert not RECEIPT.exists(),f'Receipt exists; inspect before retry: {RECEIPT}'
 now=datetime.now(timezone.utc).isoformat()
 receipt={'id':'PLANAR5-GPT-SUBMISSION-165','sentAtUtc':now,'destination':{'conversationTitle':'Calibration review part 6','url':CHAT_URL},'attachment':{'name':ARCHIVE.name,**bind(ARCHIVE)},'publicRawUrl':RAW_URL,'branch':{'name':'codex/ordinary-spell-review-complete','commit':COMMIT},'message':MESSAGE,'messageSha256':hashlib.sha256(MESSAGE.encode('utf-8')).hexdigest(),'reviewIds':IDS,'authority':{'reviewedApplied':730,'pending':118,'acceptedUnapplied':0,'completeReviewedStandaloneProcedures':454,'scopedInterfaces':173},'packetCheck':bind(CHECK),'independentVerification':bind(VERIFY),'submissionStateObserved':'ChatGPT accepted attachment and message; response showed Working / responding. No director decision received yet.'}
 write(RECEIPT,receipt)
 queue=read(QUEUE)
 queue['recordedAtUtc']=now;queue['packetStatus']='SUBMITTED_AWAITING_DIRECTOR_RETURN'
 queue['currentPendingGroups'][0]['status']='SUBMITTED_AWAITING_DIRECTOR_RETURN'
 queue['currentPendingGroups'][0]['submissionReceipt']=bind(RECEIPT)
 queue['next']['status']='SUBMITTED_AWAITING_DIRECTOR_RETURN'
 queue['sourceConferencePrepared']['status']='submitted-awaiting-director-return'
 queue['sourceConferencePrepared']['submissionReceipt']=bind(RECEIPT)
 queue['nextPreparedRequest']=queue['sourceConferencePrepared']
 queue['directorSubmission']={'status':'submitted-awaiting-director-return','conversation':CHAT_URL,'receipt':bind(RECEIPT),'archive':bind(ARCHIVE),'reviewIds':IDS}
 queue['currentSubmission']=bind(RECEIPT)
 write(QUEUE,queue)
 handoff=read(HANDOFF)
 handoff['recordedAtUtc']=now;handoff['status']='PLANAR5_SUBMITTED_AWAITING_DIRECTOR_RETURN'
 handoff['currentQueueBinding']=bind(QUEUE);handoff['currentSubmissionBinding']=bind(RECEIPT)
 handoff['nextPreparedRequest']={'status':'submitted-awaiting-director-return','conversation':CHAT_URL,'receipt':bind(RECEIPT),'archive':bind(ARCHIVE),'candidate':bind(CANDIDATE),'reviewIds':IDS}
 handoff['directorSubmission']=handoff['nextPreparedRequest']
 write(HANDOFF,handoff)
 print(json.dumps({'status':'RECORDED_SUBMITTED_AWAITING_DIRECTOR_RETURN','receipt':bind(RECEIPT),'queue':bind(QUEUE),'handoff':bind(HANDOFF)},indent=2))
if __name__=='__main__':main()
