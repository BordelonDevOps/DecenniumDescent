from datetime import datetime,timezone
import hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def info(p):
 b=p.read_bytes()
 return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 packet_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287.json'
 report_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_INDEPENDENT_AUDIT.json'
 receipt_path=BASE/'RANK9ALIGNFACTIONPURIFICATION5_PACKET_287_RECEIPT.json'
 packet=read(packet_path); report=read(report_path); receipt=read(receipt_path)
 assert packet['status']=='PREPARED_UNAUDITED_UNSENT' and report['status']=='PASS' and report['checkCount']==16 and receipt['auditStatus']=='PASS'
 now=datetime.now(timezone.utc).isoformat()
 report_info=info(report_path); receipt_info=info(receipt_path)
 status='PACKET287_AUDITED_READY_TO_SUBMIT_816_32_0'
 packet.update({'status':status,'independentAudit':report_info,'auditReceipt':receipt_info,'auditStatus':'PASS','auditChecks':16,'auditFailures':0})
 write(packet_path,packet)
 qpath=BASE/'CURRENT_SPELL_QUEUE_287.json'; queue=read(qpath)
 queue.update({'recordedAtUtc':now,'status':status,'packetStatus':status,'currentPacketAudit':report_info,'currentPacketAuditReceipt':receipt_info,'githubChanges':False})
 queue['nextPreparedRequest'].update({'status':status,'independentAudit':report_info,'auditReceipt':receipt_info,'auditStatus':'PASS','auditChecks':16})
 write(qpath,queue)
 hpath=BASE/'CURRENT_HANDOFF_287.json'; handoff=read(hpath)
 handoff.update({'recordedAtUtc':now,'status':status,'currentPacketAudit':report_info,'currentPacketAuditReceipt':receipt_info,'currentQueueBinding':info(qpath),'queue':info(qpath),'nextPreparedRequest':queue['nextPreparedRequest'],'resumePriority':'Packet287 passed independent 16/16 audit. Submit only this five-identity packet to GPT, monitor and ping the Director for progress, then audit the sealed return before deciding or applying any exact accepted IDs.'})
 write(hpath,handoff)
 print(json.dumps({'status':status,'packet':info(packet_path),'audit':report_info,'receipt':receipt_info,'queue':info(qpath),'handoff':info(hpath)},indent=2))
if __name__=='__main__': main()
