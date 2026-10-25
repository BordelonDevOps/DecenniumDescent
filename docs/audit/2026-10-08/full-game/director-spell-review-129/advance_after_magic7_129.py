"""Fresh current navigation and exact applied context for the next authorized conference."""
from pathlib import Path
import json,hashlib,datetime,zipfile,copy
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-129';R=G/'DescentReviewChanges/ReviewBible';O=A/'spell-review-resume-116'
r=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
enc=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def save(p,o):p.write_bytes(enc(o))
idx=r(R/'data/public/spell_playtests/authored_review_index.json');assert idx['authoredCounts']=={'reviewed':623,'pending':225}
ids=r(D/'MAGIC7_EXACT_ACCEPTANCE_129.json')['acceptedIdentities'];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
counts={'reviewedApplied':623,'pending':225,'standalone':347,'scopedInterfaces':173,'acceptedUnapplied':0}
qp=O/'CURRENT_SPELL_QUEUE_129.json';q=r(qp)
for g in q['groups']:
 if g['group']=='magic-modifiers7':g.update({'previousPhase':g['currentPhase'],'currentPhase':'applied-authored-review-129-with-retained-holds','exactAcceptanceReceipt':str(D/'MAGIC7_EXACT_ACCEPTANCE_129.json'),'applicationReceipt':str(D/'MAGIC7_APPLICATION_129.json'),'applicationValidation':str(D/'MAGIC7_APPLICATION_VALIDATION_129.json')})
pending={e['id'] for e in idx['entries'] if e['authoredStatus']!='reviewed-authored-operational-playtest'}
groups=[g for g in q['groups'] if set(g['identities'])&pending]
flat=[sid for g in groups for sid in g['identities']];assert len(flat)==len(set(flat))==225 and set(flat)==pending
q['currentCounts']={'appliedReviewed':623,'indexPending':225,'acceptedUnapplied':0,'needsAcceptance':225,'submittedAwaitingReturn':0,'otherUnaccepted':225,'missingReturnArtifacts':0,'historicalMissingReturnReconstructionPending':8}
q['lastUpdatedAtUtc']=now;q['resumePriority']='Use Calibration review part6; Magic7 applied129; send prepared LifeMatter5 then continue all225 remaining until independently accepted and applied.'
q['directorConnectionStatus']='Magic7 Return03 independently accepted/applied; next LifeMatter5 prepared, not yet sent.'
for k in ['appliedAcceptedIdentities','acceptedIdentities']:
 if isinstance(q.get(k),list):q[k]=list(dict.fromkeys(q[k]+ids))
for k,n in [('latestAcceptanceReceipts','MAGIC7_EXACT_ACCEPTANCE_129.json'),('latestApplicationReceipts','MAGIC7_APPLICATION_129.json')]:
 if isinstance(q.get(k),list):q[k].append(str(D/n))
save(qp,q)
hp=D/'CURRENT_HANDOFF_129.json';h=r(hp);h['status']='MAGIC7_APPLIED_LIFEMATTER5_READY_ALL225_REQUIRED';h['currentCounts']=counts;h['lastUpdatedAtUtc']=now;h['appliedThisTurn']['Magic7']=ids;h['applicationReceipts'].append(str(D/'MAGIC7_APPLICATION_129.json'))
h['director'].update({'activeRequestStatus':'MAGIC7_COMPLETE_ACCEPTED_APPLIED_NEXT_LIFEMATTER5_UNSENT','scope':'LifeMatter5 next; preserve closed Magic7 exact Return03.'})
h['next']='Send LifeMatter5 with exact current applied context, independently review its whole return, apply immediately after acceptance, then Information8/Eye1 and all remaining source conferences.'
h['resumePriority']=q['resumePriority'];h['directorConnectionStatus']=q['directorConnectionStatus'];h['magic7Application129']=r(D/'MAGIC7_APPLICATION_VALIDATION_129.json');h['material8ReconstructionPacket']=str(D/'MATERIAL8_RECONSTRUCTION_PACKET_129.json');save(hp,h)
cp=A/'ACTIVE_AUTHORING_CHECKPOINT_ORDINARY_SPELL_REVIEW_129.json';c=r(cp);c.update({'status':h['status'],'currentCounts':counts,'newApplied':7,'lastUpdatedAtUtc':now,'magic7Application129':h['magic7Application129'],'next':h['next']});c['director']=h['director'];save(cp,c)
p=G/'START_HERE.md';s=p.read_text(encoding='utf-8-sig');mark='The checkpoint entries below preserve earlier states; checkpoint129 and the Part6 direction above control current work.';tail=s[s.index(mark):]
header='# Active ordinary spell review129 — Calibration review part6\n\nMagic7 exact Return03 is independently accepted and applied. Current authored coverage: **623 applied /225 pending /347 standalone /173 scoped interfaces /0 accepted-unapplied**. Seven native procedures,39 access rows,14 main cases,26 branches and839 events are preserved with7,649 data checks and225 final source/phase/preservation checks passing. Two non-operative historical-file locator corrections are recorded in the exact acceptance receipt; all79 original Return02 members are preserved. Runtime, human-play, balance, cosmology and release holds remain.\n\nContinue until all225 remaining pending identities are independently accepted and applied. User selected Calibration review part6 (6adc506d-8770-83ea-b64c-0345d9b9b682). LifeMatter5 is the next prepared packet. Read docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_HANDOFF_129.json and spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json. Do not reopen335 feats or completed spell cohorts. Thirty additional rank8/rank9 packets and the Material8 fresh-reconstruction packet are prepared.\n\n'
p.write_text(header+tail,encoding='utf-8')
files={}
for n in ['DD_Magic7_Corrected_Return03_129.zip','MAGIC7_EXACT_ACCEPTANCE_129.json','MAGIC7_APPLICATION_129.json','MAGIC7_APPLICATION_VALIDATION_129.json','MAGIC7_RETURN03_INDEPENDENT_DATA_AUDIT_129.json','MAGIC7_RETURN03_FINAL_INDEPENDENT_CHECKS_129.json','MAGIC7_INDEX_OPERATIONS_129.json']:files['accepted/'+n]=(D/n).read_bytes()
for n in ['MODEL.json','PROCEDURES.json','SHARED_RULES.json','OPERATIVE_TEXT.md','HOLD_REGISTER.json','NATIVE_AND_ACCESS_RECORDS.json','ACTOR_TEMPLATES.json']:files['accepted/magic7/'+n]=(D/'magic7_return03_received'/n).read_bytes()
files['current/authored_review_index.json']=(R/'data/public/spell_playtests/authored_review_index.json').read_bytes();files['current/CURRENT_SPELL_QUEUE_129.json']=qp.read_bytes();files['current/APPLICATION_CHECKPOINT_129.json']=cp.read_bytes()
files['README.md']=b'# Magic7 applied context129\n\nAuthoritative current state:623 applied/225 pending/347 standalone/173 scoped interfaces/0 accepted-unapplied. Complete exact Return03 archive plus independent acceptance/application and current index are supplied. Two prior-member locator-only errata are authoritatively resolved by the acceptance receipt; the old bytes exist under history/return02. No rule or case was changed locally. Closed335 feats and all completed spells remain closed. Retained content/runtime/human/balance/cosmology/release holds remain.\n\nLifeMatter5 conference127 is the next pending authoring packet. Its historical610/238/334 labels and Transport/Magic pending labels are superseded by this exact application context and Transport6 applied context128. Preserve its complete nested original sources,20 questions,10 original scenarios and all case obligations. Do not run supplied or historical programs.\n'
files['MANIFEST.json']=enc({'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in files.items()]})
out=D/'DD_Magic7_Applied_Context_129.zip';assert not out.exists()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in files.items():z.writestr(n,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)
 for b in json.loads(z.read('MANIFEST.json'))['files']:assert sha(z.read(b['path']))==b['sha256'] and len(z.read(b['path']))==b['bytes']
receipt={'id':'MAGIC7-APPLIED-CONTEXT-129','archive':bind(out),'members':len(files),'bindings':len(files)-1,'status':'PREPARED_NOT_SENT','currentCounts':counts,'pendingGroups':len(groups),'pendingExactlyOnce':True};save(D/'MAGIC7_APPLIED_CONTEXT_PACKET_129.json',receipt);print(json.dumps(receipt,indent=2))
