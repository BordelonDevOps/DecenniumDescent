"""Fresh current navigation and byte-exact applied context after one-ID validated application."""
from pathlib import Path
import json,hashlib,datetime,zipfile
G=Path(r'C:\Github\DecenniumDescent');D=Path(__file__).parent;A=D.parent;R=G/'DescentReviewChanges/ReviewBible';O=A/'spell-review-resume-116'
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
enc=lambda x:(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
def write(p,x):p.write_bytes(enc(x))
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat();v=rd(D/'DISINTEGRATE_APPLICATION_VALIDATION_129.json');assert v['passed']
idx=rd(R/'data/public/spell_playtests/authored_review_index.json');assert idx['authoredCounts']=={'reviewed':628,'pending':220}
ap=D/'DISINTEGRATE_EXACT_ACCEPTANCE_129.json';rp=D/'DISINTEGRATE_APPLICATION_129.json';q=rd(O/'CURRENT_SPELL_QUEUE_129.json');assert q['currentCounts']['indexPending']==221
q['currentCounts'].update(appliedReviewed=628,indexPending=220,acceptedUnapplied=0,needsAcceptance=220,submittedAwaitingReturn=9,otherUnaccepted=211)
q['appliedAcceptedIdentities']=sorted(set(q['appliedAcceptedIdentities'])|{'disintegrate'});q['acceptedIdentities']=['disintegrate'];q['latestAcceptanceReceipts'].append(str(ap));q['latestApplicationReceipts'].append(str(rp));q['lastUpdatedAtUtc']=now
q['nextSuggestedGroups']=['information8','eye-judgement1','planar-travel6','rank7-perception5','ward7','manifestation7','soul-contact6','vitality-matter10']
for g in q['groups']:
 if g['group']=='life-matter5':g.update(currentPhase='all-five-applied-exact-receipts-129',appliedIdentities=['awaken','bone-cage','contagion','disintegrate','telekinesis'],pendingIdentities=[],latestApplicationReceipt=str(rp),latestExactAcceptanceReceipt=str(ap))
q['director']['scope']='All five LifeMatter identities applied under separate exact four-ID Return01 and one-ID Return02 receipts. Continue pending Information8/EyeJudgement1 and all220.'
q['resumePriority']='Apply exact accepted Information8/EyeJudgement1 next, then all220 remaining. Disintegrate is applied; do not redo LifeMatter or closed cohorts.'
q['directorConnectionStatus']='Same Part6 backing task received exact next9 request. Official Library yielded finalReturn02 independently despite delayed read_thread progress. Use actual returned files/receipts rather than stale tool-progress text.'
inventory=rd(D/'CURRENT221_PACKET_INVENTORY_129.json');inventory.update(id='CURRENT220-PACKET-INVENTORY-129',recordedAtUtc=now,counts=idx['authoredCounts'],priorInventory='CURRENT221_PACKET_INVENTORY_129.json',currentIndexSha256=v['index']['sha256'])
inventory['groups']=[g for g in inventory['groups'] if g['group']!='life-matter5']
inventory['groupsCount']=len(inventory['groups'])
pending={e['id'] for e in idx['entries'] if e['authoredStatus']!='reviewed-authored-operational-playtest'};listed=[s for g in inventory['groups'] for s in g['identities']]
assert len(listed)==len(set(listed))==220 and set(listed)==pending
inventory['pendingExactlyOnce']=True;inventory['scope']='Current220 pending identities mapped exactly once across42 verified source packet groups. LifeMatter5 fully applied under separate exact receipts; original packet inventories remain immutable history.'
inp=D/'CURRENT220_PACKET_INVENTORY_129.json';assert not inp.exists();write(inp,inventory);q['currentPacketInventory']=str(inp);write(O/'CURRENT_SPELL_QUEUE_129.json',q)
for p in [D/'CURRENT_HANDOFF_129.json',A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_129.json']:
 j=rd(p);j.update(currentCounts={'reviewedApplied':628,'pending':220,'standalone':352,'scopedInterfaces':173,'acceptedUnapplied':0},status='PART6_LIFEMATTER5_ALL_APPLIED_INFORMATION8_EYE1_PENDING_ALL220_REQUIRED',lastUpdatedAtUtc=now,disintegrateApplication129=v,next=q['resumePriority'],director=q['director'],currentPacketInventory=str(inp),future41LibraryUploads=str(D/'NEXT41_SOURCE_LIBRARY_UPLOADS_129.json'))
 if 'resumePriority' in j:j['resumePriority']=q['resumePriority']
 if 'appliedThisTurn' in j:j['appliedThisTurn']['Disintegrate']=['disintegrate']
 if 'applicationReceipts' in j:j['applicationReceipts'].append(str(rp))
 if 'newApplied' in j:j['newApplied']=12
 write(p,j)
start=G/'START_HERE.md';old=start.read_text(encoding='utf-8-sig');marker='The checkpoint entries below preserve earlier states; checkpoint129 and the Part6 direction above control current work.';assert marker in old
prefix='# Active ordinary spell review129 — Calibration review part6\n\nAll five LifeMatter identities are independently accepted and applied: four exact Return01 procedures plus corrected Disintegrate Return02. Current authored coverage: **628 applied /220 pending /352 standalone /173 scoped interfaces /0 accepted-unapplied**. The latest one-ID application preserves all847 unrelated index entries and all148 corrected-return evidence files byte for byte. Original Return01 remains complete in its preserved history. No runtime, human-play, balance, cosmology or release approval follows.\n\nContinue until all220 remaining identities are independently accepted and applied. Use Calibration review part6 (6adc506d-8770-83ea-b64c-0345d9b9b682), confirmed backing task01a16c9a-4007-70c7-84b3-95bedbad20e5 on durable. Information8 and EyeJudgement1 full sources and exact request are delivered; continue those conferences. Official Library delivery can advance before read_thread progress updates. Six later source packets covering41 identities are uploaded and referenced by NEXT41_SOURCE_LIBRARY_UPLOADS_129.json; their director request is not yet sent. Read director-spell-review-129/CURRENT_HANDOFF_129.json, CURRENT220_PACKET_INVENTORY_129.json and spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json under docs/audit/2026-10-08/full-game. Do not reopen feats or completed spell cohorts.\n\n'
start.write_text(prefix+old[old.index(marker):],encoding='utf-8')
packet=D/'DD_Disintegrate_Applied_Context_129.zip';assert not packet.exists();payload={}
for p in [ap,rp,D/'DISINTEGRATE_APPLICATION_VALIDATION_129.json',D/'DISINTEGRATE_INDEX_OPERATIONS_129.json',D/'DISINTEGRATE_RETURN02_FINAL_INDEPENDENT_REVIEW_129.json',D/'LIFEMATTER5_RETURN02_INDEPENDENT_DATA_AUDIT_129.json',D/'LIFEMATTER5_RETURN02_CAST_SOURCE_AUDIT_129.json',D/'LIFEMATTER5_RETURN02_ACTOR_CARD_AUDIT_129.json',D/'LIFEMATTER5_RETURN02_BOOK_AUDIT_129.json',D/'LIFEMATTER5_RETURN02_LIBRARY_DELIVERY_129.json',D/'DD_LifeMatter5_Director_Return02_130_DELIVERY.json',R/'data/public/spell_playtests/authored_review_index.json',O/'CURRENT_SPELL_QUEUE_129.json',inp,D/'INFORMATION8_EYE1_LIBRARY_UPLOAD_129.json',D/'NEXT41_SOURCE_LIBRARY_UPLOADS_129.json',D/'LIFEMATTER4_CONTEXT_AND_NEXT9_DELIVERY_129.json',R/'docs/spells/candidates/DISINTEGRATE_REVIEWED_129.md',D/'DD_LifeMatter5_Director_Return02_130.zip']:payload[p.name]=p.read_bytes()
payload['README.md']=b'Current628applied/220pending/352standalone/173scoped/0accepted-unapplied. Disintegrate exact corrected Return02 is now independently accepted and applied; the four previous LifeMatter selections remain unchanged. Complete148-member Return02 ZIP and all acceptance/application/current-index/queue/verification data are included. Return02 nests exact previous applied context and fullReturn01. Only exact receipts control acceptance; historical proposed/pending labels remain preserved. Continue Information8/EyeJudgement1 and all220; no closed cohort reopened. Runtime/human/balance/cosmology/release holds remain.\n'
payload['MANIFEST.json']=enc({'id':'DISINTEGRATE-APPLIED-CONTEXT-129','recordedAtUtc':now,'currentCounts':idx['authoredCounts'],'appliedIds':['disintegrate'],'files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}for n,b in payload.items()]})
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in payload.items():z.writestr(n,b)
with zipfile.ZipFile(packet) as z:
 assert z.testzip() is None
 for n,b in payload.items():assert z.read(n)==b
result={'id':'DISINTEGRATE-APPLIED-CONTEXT-PACKET-129','archive':bind(packet),'members':len(payload),'currentCounts':idx['authoredCounts'],'appliedIds':['disintegrate'],'sent':False,'completeReturn02Preserved':True};write(D/'DISINTEGRATE_APPLIED_CONTEXT_PACKET_129.json',result);print(json.dumps(result,indent=2))
