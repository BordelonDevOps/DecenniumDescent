import json,hashlib,re
from pathlib import Path
A=Path('C:/Github/DecenniumDescent/docs/audit/2026-10-08/full-game')
sources=["C:\\Users\\cbord\\AppData\\Local\\Temp\\codex-file-preview-cajv1T\\Pasted text (4).txt","C:\\Users\\cbord\\AppData\\Local\\Temp\\codex-file-preview-mo7PYz\\Pasted text (3).txt","C:\\Users\\cbord\\AppData\\Local\\Temp\\codex-file-preview-i7RGLq\\Pasted text (2).txt","C:\\Users\\cbord\\AppData\\Local\\Temp\\codex-file-preview-YWr8O9\\Pasted text(20261009-204313).txt"]
ledger=[]
for src in sources:
 p=Path(src); raw=p.read_bytes(); s=raw.decode('utf-8-sig'); n=int(re.match(r'PART (\d) OF 4',s).group(1)); planned=(A/f'CODEX_ENCHANTMENT_RANK1_TRANSFER_PART{n}.md').read_text(encoding='utf-8')
 assert s.rstrip()==planned.rstrip(),n
 dst=A/f'CODEX_ENCHANTMENT_RANK1_DELIVERED_PART{n}.txt'; assert not dst.exists();dst.write_bytes(raw)
 ledger.append({'part':n,'path':str(dst),'sha256':hashlib.sha256(raw).hexdigest(),'matchesPlannedIgnoringFinalWhitespace':True,'characters':len(s)})
ledger.sort(key=lambda x:x['part'])
combined=''.join(Path(x['path']).read_text(encoding='utf-8-sig').split('\n',1)[1] for x in ledger)
assert combined.rstrip()==(A/'CODEX_ENCHANTMENT_RANK1_EXACT_REVIEW_COMPACT.md').read_text(encoding='utf-8').rstrip()
p=A/'ENCHANTMENT_RANK1_EXACT_SUBMISSION.json'; d=json.loads(p.read_text(encoding='utf-8')); d.update(status='exact candidate submitted; actual browser user turn and four delivered attachments verified; review pending',dispatch={'method':'Chrome visible composer, four ordered pasted-text attachments','turnId':'c3d6ad40-d199-4f8b-9a3c-3d2e03fd12a3','conversationId':'6a7a0fa2-eee0-83ea-92e9-6723a9f67ede','attachments':ledger,'compactPacketPath':str(A/'CODEX_ENCHANTMENT_RANK1_EXACT_REVIEW_COMPACT.md'),'compactPacketSha256':hashlib.sha256((A/'CODEX_ENCHANTMENT_RANK1_EXACT_REVIEW_COMPACT.md').read_bytes()).hexdigest(),'verification':'Four delivered attachments match planned packet, ignoring only final trailing whitespace. Shared-field reconstruction locally matches every candidate spell field.','failedTransportNotes':'Earlier connector acknowledgement did not produce a visible message. Single-use loopback preview was not readable in browser. No browser permissions changed. Direct paste succeeded.'}); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':d['status'],'parts':ledger},ensure_ascii=False,indent=2))
