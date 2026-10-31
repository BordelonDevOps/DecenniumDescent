from __future__ import annotations
import copy, hashlib, json, pathlib, zipfile, zlib
from datetime import datetime, timezone
import jsonpatch

ROOT = pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
AUDIT = ROOT / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
RECEIVED = AUDIT / 'rank9_defenseform8_return218_received'
ZIP = RECEIVED / 'DD_Rank9_DefenseForm5_Director_Return218.zip'
DELIVERY = RECEIVED / 'DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json'
SOURCE_ZIP = AUDIT / 'rank9_defenseform8_source_packet_218_refreshed/DD_Rank9_DefenseForm8_CurrentSource_218.zip'
OLD_RETURN = AUDIT / 'rank9_defenseform8_return186_received/DD_Rank9_DefenseForm8_Director_Return186.zip'
REPORT = AUDIT / 'RANK9_DEFENSEFORM8_RETURN218_INDEPENDENT_AUDIT.json'
AUTHORITY = {'reviewedApplied':808,'pending':40,'acceptedUnapplied':0,'completeStandaloneProcedures':532,'scopedInterfaces':173}
ACCEPTED = ['absolute-immunity','body-to-void']
HELD = ['elemental-shell','timeless-form','invulnerable-sphere']
BLOCKERS = {'elemental-shell':['DF218-B01','DF218-B02'],'timeless-form':['DF218-B03'],'invulnerable-sphere':['DF218-B04']}
checks=[]
def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def crc(b: bytes) -> str: return f'{zlib.crc32(b)&0xffffffff:08x}'
def canon(v) -> bytes: return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def add(name, ok, detail=None):
 checks.append({'check':name,'passed':bool(ok),**({'detail':detail} if detail is not None else {})})
def read_json(raw): return json.loads(raw.decode('utf-8-sig'))

delivery = json.loads(DELIVERY.read_text(encoding='utf-8-sig'))
archive_raw = ZIP.read_bytes()
archive_sha = sha(archive_raw)
add('Outer archive size/SHA-256/CRC match the external delivery record',len(archive_raw)==delivery['archive']['bytes']==72072047 and archive_sha==delivery['archive']['sha256']=='09e592f58e66975933f3feb8fe8779c215d5a70d5f00623a23da6ede351d8875' and crc(archive_raw)==delivery['archive']['crc32'])
add('External delivery identifies the exact group return and leaves it unapplied',delivery['id']=='RANK9-DEFENSEFORM5-RETURN218-DELIVERY' and delivery['applied'] is False and delivery['noCanonicalChanges'] is True and delivery['noGitHubChanges'] is True)
with zipfile.ZipFile(ZIP) as z:
 names=z.namelist(); name_set=set(names)
 add('ZIP CRC scan passes and member names are unique',z.testzip() is None and len(names)==len(name_set)==delivery['memberCount']==115)
 unsafe=[n for n in names if n.startswith(('/','\\')) or '..' in pathlib.PurePosixPath(n.replace('\\','/')).parts or any(part.startswith('.') for part in n.replace('\\','/').split('/'))]
 add('Archive has no traversal, hidden, or absolute paths',not unsafe,unsafe[:10])
 allow=set(delivery['allowlist']); rows={r['path']:r for r in delivery['members']}
 add('External allowlist and delivery member inventory exactly equal archive names',allow==name_set and set(rows)==name_set and len(rows)==len(delivery['members'])==115)
 member_errors=[]
 for n in names:
  raw=z.read(n); row=rows.get(n,{})
  if (len(raw),sha(raw),crc(raw))!=(row.get('bytes'),row.get('sha256'),row.get('crc32')) or z.getinfo(n).CRC!=(zlib.crc32(raw)&0xffffffff): member_errors.append(n)
 add('Every archive member independently matches delivered bytes/SHA/CRC and central-directory CRC',not member_errors,member_errors[:10])
 internal=read_json(z.read('MEMBER_MANIFEST.json')); imap={r['path']:r for r in internal['members']}
 add('Internal manifest covers exactly all 114 payload members',internal['payloadMemberCount']==114 and set(imap)==name_set-{'MEMBER_MANIFEST.json'} and len(imap)==114)
 internal_errors=[]
 for n,row in imap.items():
  raw=z.read(n)
  if (len(raw),sha(raw),crc(raw))!=(row.get('bytes'),row.get('sha256'),row.get('crc32')): internal_errors.append(n)
 add('Every payload member matches the internal self-excluding manifest',not internal_errors,internal_errors[:10])
 decision=read_json(z.read('DIRECTOR_DECISION.json'))
 auth=read_json(z.read('AUTHORITY.json'))
 counts=read_json(z.read('COUNTS.json'))
 add('Delivery, director decision, and authority records agree on 808/40/0 and 532/173',delivery['authority']==AUTHORITY and decision['sourceAuthority']==AUTHORITY and auth['authority']==AUTHORITY and all(internal['authority'][k]==AUTHORITY[k] for k in ('reviewedApplied','pending','acceptedUnapplied')))
 add('Exactly Absolute Immunity and Body to Void are accepted, with no application',delivery['acceptedIds']==decision['acceptedIds']==ACCEPTED and delivery['applied'] is False and decision['applied'] is False and auth['acceptedIds']==ACCEPTED and auth['applied'] is False and auth['canonicalFilesChanged'] is False and auth['GitHubChanged'] is False)
 add('Exactly the other three Defense/Form8 identities remain held',delivery['heldIds']==decision['heldIds']==HELD and counts['heldIdentities']==3 and counts['acceptedIdentities']==2)
 disposition_errors=[]
 per={x['spellId']:x for x in delivery['perIdentity']}; dper={x['spellId']:x for x in decision['perIdentity']}
 proc=read_json(z.read('PROCEDURES.json')); procmap={x['spellId']:x for x in proc['spells']}
 for sid in ACCEPTED+HELD:
  a=per.get(sid,{}); b=dper.get(sid,{}); p=procmap.get(sid,{})
  if (a.get('accepted'),a.get('applied'),a.get('blockerIds'),a.get('procedure'))!=(b.get('accepted'),b.get('applied'),b.get('blockerIds'),b.get('procedure')): disposition_errors.append((sid,'decision/delivery mismatch'))
  if a.get('accepted') is not (sid in ACCEPTED) or a.get('applied') is not False or p.get('accepted') is not (sid in ACCEPTED) or p.get('applied') is not False: disposition_errors.append((sid,'procedure disposition mismatch'))
  if sid in HELD and a.get('blockerIds')!=BLOCKERS[sid]: disposition_errors.append((sid,'exact blocker mismatch'))
  pp=a.get('procedure')
  if pp not in name_set: disposition_errors.append((sid,'procedure member missing'))
  else:
   pd=read_json(z.read(pp))
   if pd.get('spellId')!=sid or pd.get('accepted') is not (sid in ACCEPTED) or pd.get('applied') is not False: disposition_errors.append((sid,'procedure file mismatch'))
 add('Five identity decisions, procedure dispositions, per-identity blocker IDs, and procedure files agree',not disposition_errors,disposition_errors[:12])
 blockers=read_json(z.read('BLOCKER_REASSESSMENT.json'))['records']
 blocker_map={x.get('currentId'):x for x in blockers if x.get('currentId')}
 add('Four held blockers map to the prior exact source blockers',all(blocker_map[h]['decision']=='RETAIN_EXACT_SOURCE_DEPENDENCY' for h in sum(BLOCKERS.values(),[])) and {blocker_map[h]['currentId'] for h in sum(BLOCKERS.values(),[])}==set(sum(BLOCKERS.values(),[])))
 package_checks=delivery['packageChecks']
 add('Director package audit reports exactly 470 passing checks and no failures',package_checks['count']==470 and not package_checks['failed'] and len(package_checks['results'])==470 and all(x['pass'] for x in package_checks['results']))
 semantic=read_json(z.read('INDEPENDENT_SEMANTIC_FAILURE_CHECK.json'))
 add('All 33 independent semantic assertions pass',semantic['assertionCount']==33 and len(semantic['assertions'])==33 and all(x['pass'] for x in semantic['assertions']))
 baseline=read_json(z.read('BASELINE_DATA_CHECK.json')); added=read_json(z.read('ADDED_DATA_INTEGRITY_CHECK.json'))
 add('Return186 baseline evidence is reused without replay: 19,517 checks and 69 cases remain unchanged',baseline['targetCaseCount']==69 and baseline['targetEvents']==1496 and baseline['checks']==19517 and baseline['failures']==[] and len(baseline['results'])==19517 and all(x['pass'] for x in baseline['results']) and added['baselineReusedWithoutReplay'] is True and added['newAndPackagingDataCheckCount']==2335 and added['failures']==[] and len(added['results'])==2335 and all(x['pass'] for x in added['results']))
# Reopen for deep case and source audits after the initial ZIP context closed.
z=zipfile.ZipFile(ZIP)
# Verify historical identity of all 69 preserved cases against Return186's archived casebook.
preserved=read_json(z.read('PRESERVED_CASE_INDEX.json'))['cases']; old_zip=zipfile.ZipFile(OLD_RETURN)
oldbook=read_json(old_zip.read('CASEBOOK.json')); old_cases={x['id']:x for x in oldbook['cases']}
preserve_errors=[]
for row in preserved:
 obj=read_json(z.read(row['path']))
 if len(z.read(row['path']))!=row['bytes'] or sha(z.read(row['path']))!=row['sha256'] or row['id'] not in old_cases or obj!=old_cases[row['id']]: preserve_errors.append(row['id'])
add('All 69 preserved case objects are unchanged from the prior Return186 casebook',len(preserved)==69 and not preserve_errors,preserve_errors[:10])
case_index=read_json(z.read('CASE_INDEX.json'))
dispositions=read_json(z.read('CASE_DISPOSITIONS.json'))['cases']; new_ids={x['id'] for x in dispositions if x.get('new') is True}
case_map={x['id']:x for x in case_index['cases']}
new_errors=[]; replay_cases=events=forward=inverse=0
for cid in sorted(new_ids):
 row=case_map.get(cid); case=read_json(z.read(row['path'])) if row and row['path'] in name_set else None
 if not row or not case or case['id']!=cid or row['events']!=len(case['events']): new_errors.append((cid,'missing/index mismatch')); continue
 state=case['initialState']
 if sha(canon(state))!=case['initialSHA256']: new_errors.append((cid,'initial hash')); continue
 try:
  for ev in case['events']:
   before,after=ev['beforeState'],ev['afterState']
   if state!=before or sha(canon(before))!=ev['beforeSHA256'] or sha(canon(after))!=ev['afterSHA256']: raise AssertionError('event hash/state')
   f=jsonpatch.JsonPatch(ev['forward']).apply(before,in_place=False)
   if f!=after: raise AssertionError('forward replay')
   back=jsonpatch.JsonPatch(ev['inverse']).apply(after,in_place=False)
   if back!=before: raise AssertionError('inverse replay')
   forward+=len(ev['forward']); inverse+=len(ev['inverse']); events+=1; state=after
  if state!=case['finalState'] or sha(canon(state))!=case['finalSHA256']: raise AssertionError('final hash/state')
  replay_cases+=1
 except Exception as e: new_errors.append((cid,str(e)))
add('Three added cases independently replay forward/inverse with exact state hashes',len(new_ids)==3 and replay_cases==3 and not new_errors,{'caseIds':sorted(new_ids),'cases':replay_cases,'events':events,'forwardOperations':forward,'inverseOperations':inverse,'errors':new_errors[:10]})
add('Case index totals reconcile to 72 cases, 1,568 events and 3 added traces',len(case_index['cases'])==72 and case_index['caseCount']==72 and case_index['preservedCases']==69 and case_index['newCases']==3 and case_index['events']==1568 and events==72 and case_index['events']==baseline['targetEvents']+events)
# Verify the nested 218 source packet matches the exact locally prepared source packet.
source_bind=delivery['sourcePacketBinding']; source_inner=z.read('source/DD_Rank9_DefenseForm8_CurrentSource_218.zip')
add('Embedded source packet is byte-exact to the locally prepared authority-808 packet',source_bind['bytes']==len(source_inner)==SOURCE_ZIP.stat().st_size and source_bind['sha256']==sha(source_inner)==sha(SOURCE_ZIP.read_bytes()) and source_inner==SOURCE_ZIP.read_bytes())
reconciliation=read_json(z.read('source/CANDIDATE_BINDING_RECONCILIATION_218.json'))
local_reconciliation=json.loads((AUDIT/'CURRENT_CANDIDATE_BINDING_RECONCILIATION_218.json').read_text(encoding='utf-8-sig'))
add('Candidate serialization reconciliation is unchanged and records zero structural differences',reconciliation==local_reconciliation and reconciliation['jsonStructuralEquality'] is True and reconciliation['fieldDifferences']==0)
source_check=read_json(z.read('SOURCE_CHECK.json'))
add('Source check covers 87 refreshed bindings and stays at current authority',len(source_check['bindings'])==87 and source_check['authority']==AUTHORITY and source_check['failures']==0 if isinstance(source_check.get('failures'),int) else len(source_check['bindings'])==87 and source_check['authority']==AUTHORITY)

status='PASS' if all(c['passed'] for c in checks) else 'FAIL'
report={'id':'RANK9-DEFENSEFORM8-RETURN218-INDEPENDENT-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':status,'checksPassed':sum(c['passed'] for c in checks),'checksFailed':sum(not c['passed'] for c in checks),'archive':{'path':ZIP.relative_to(ROOT).as_posix(),'bytes':len(archive_raw),'sha256':archive_sha,'crc32':crc(archive_raw)},'deliveryManifest':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':DELIVERY.stat().st_size,'sha256':sha(DELIVERY.read_bytes())},'acceptedIds':ACCEPTED,'heldIds':HELD,'blockerIds':BLOCKERS,'authority':AUTHORITY,'preservedCasesVerified':len(preserved)-len(preserve_errors),'newCasesReplayed':replay_cases,'checks':checks}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
old_zip.close()
