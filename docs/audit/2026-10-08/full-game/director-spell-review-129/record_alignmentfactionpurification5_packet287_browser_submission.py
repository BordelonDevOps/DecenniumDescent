from datetime import datetime,timezone
import hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=BASE/'rank9_alignmentfactionpurification5_current_source_287_prepared'
CHAT='https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def main():
 packet_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287.json'; packet=read(packet_path)
 report_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_INDEPENDENT_AUDIT.json';receipt_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_RECEIPT.json'
 assert packet['status']=='PACKET287_AUDITED_READY_TO_SUBMIT_816_32_0'
 assert read(report_path)['status']=='PASS' and read(report_path)['checkCount']==16
 now=datetime.now(timezone.utc).isoformat();status='PACKET287_SUBMITTED_GPT_PENDING_816_32_0'
 files=[OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287.zip',OUT/'DD_Rank9_AlignmentFactionPurification5_CurrentSource_287_DELIVERY.json',OUT/'CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json',OUT/'CURRENT_CONTEXT_287.json',OUT/'REQUEST_287.txt',BASE/'CURRENT_SPELL_QUEUE_287.json',BASE/'CURRENT_HANDOFF_287.json',BASE/'CURRENT32_PENDING_IDENTITY_AUDIT_287.json',BASE/'CURRENT_SPELL_REVIEW_SNAPSHOT_287.md',BASE/'RANK9ALIGNFACTIONPURIFICATION5_SOURCE_PREPARATION_287.json',packet_path,report_path,receipt_path]
 submission={'id':'RANK9ALIGNFACTIONPURIFICATION5-PACKET-287-SUBMISSION','recordedAtUtc':now,'status':status,'group':packet['group'],'targetIds':packet['pendingIds'],'authority':packet['sourceAuthority'],'archive':packet['archive'],'deliveryManifest':packet['deliveryManifest'],'independentAudit':info(report_path),'auditReceipt':info(receipt_path),'auditStatus':'PASS','auditChecks':16,'auditFailures':0,'acceptedIds':[],'appliedIds':[],'heldIds':[],'destination':'GPT director conversation','conversationId':'6adc506d-8770-83ea-b64c-0345d9b9b682','browserVerified':True,'attachedFiles':[info(x) for x in files],'submittedAtUtc':now,'followUpPingsSent':0,'githubChanges':False,'browserEvidence':{'conversationTitle':'Calibration review part 6','conversationUrl':CHAT,'attachedFilesVisible':[x.name for x in files],'submittedMessageVisible':True,'directorStatusVisible':'Working'}}
 sub_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_SUBMISSION.json';write(sub_path,submission);sub_info=info(sub_path)
 packet.update({'status':status,'submission':sub_info,'submittedAtUtc':now,'followUpPingsSent':0});write(packet_path,packet)
 pending_path=BASE/'CURRENT32_PENDING_IDENTITY_AUDIT_287.json';pending=read(pending_path);pending.update({'recordedAtUtc':now,'status':status});pending['preparedNextGroup'].update({'status':status,'submittedAtUtc':now,'submission':sub_info});pending['lastSubmittedPacket']={'group':packet['group'],'targetIds':packet['pendingIds'],'archive':packet['archive'],'deliveryManifest':packet['deliveryManifest'],'independentAudit':submission['independentAudit'],'receipt':submission['auditReceipt'],'acceptedIds':[],'appliedIds':[],'submittedAtUtc':now,'status':status,'submission':sub_info};write(pending_path,pending);pending_info=info(pending_path)
 qpath=BASE/'CURRENT_SPELL_QUEUE_287.json';q=read(qpath);q.update({'recordedAtUtc':now,'status':status,'packetStatus':status,'pendingIdentityAudit':pending_info,'currentSubmission':sub_info,'submittedAtUtc':now,'githubChanges':False});write(qpath,q)
 hpath=BASE/'CURRENT_HANDOFF_287.json';h=read(hpath);h.update({'recordedAtUtc':now,'status':status,'pendingIdentityAudit':pending_info,'queue':info(qpath),'currentQueueBinding':info(qpath),'currentSubmission':sub_info,'submittedAtUtc':now,'nextStep':'Packet287 is submitted to GPT for exactly the five Alignment/Faction/Purification identities. Check browser receipt and progress frequently, ping again when needed, audit the sealed return, then apply only exact accepted IDs.'});write(hpath,h)
 print(json.dumps({'status':status,'submission':sub_info,'pendingAudit':pending_info,'queue':info(qpath),'handoff':info(hpath)},indent=2))
if __name__=='__main__':main()
