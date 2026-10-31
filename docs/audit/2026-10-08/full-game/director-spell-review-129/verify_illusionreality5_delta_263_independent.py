from __future__ import annotations
import copy, hashlib, json, zipfile, zlib
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_illusionreality5_delta_263_prepared'
ZIP=OUT/'DD_Rank9_SoulReflection_Delta_263.zip'
DELIVERY=OUT/'DD_Rank9_SoulReflection_Delta_263_DELIVERY.json'
AUDIT=OUT/'SOUL_REFLECTION_DELTA_263_INDEPENDENT_AUDIT.json'
SUBMISSION=OUT/'SOUL_REFLECTION_DELTA_263_SUBMISSION.json'
AUTH={'reviewedApplied':814,'pending':34,'acceptedUnapplied':0,'completeStandaloneProcedures':538,'scopedInterfaces':173}

def sha(b): return hashlib.sha256(b).hexdigest()
def crc(b): return f'{zlib.crc32(b)&0xffffffff:08x}'
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def safe(n):
 p=PurePosixPath(n)
 return bool(n) and '\\' not in n and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts)
def loadj(b): return json.loads(b.decode('utf-8-sig'))

def main():
 checks=[]
 def check(name,condition,detail=None): checks.append({'check':name,'passed':bool(condition),'detail':detail})
 archive=ZIP.read_bytes(); delivery=loadj(DELIVERY.read_bytes()); submission=loadj(SUBMISSION.read_bytes())
 expected=delivery['archive']
 check('ZIP size, SHA-256 and CRC32 match external delivery manifest',len(archive)==expected['bytes'] and sha(archive)==expected['sha256'] and crc(archive)==expected['crc32'],{'bytes':len(archive),'sha256':sha(archive),'crc32':crc(archive)})
 check('Delivery and submission bind the same target and current authority',delivery['authority']==AUTH and submission['authority']==AUTH and delivery['targetIds']==['soul-reflection'] and submission['targetIds']==['soul-reflection'])
 failures=[]; case_rows=[]
 with zipfile.ZipFile(ZIP) as z:
  names=z.namelist(); manifest_raw=z.read('MEMBER_MANIFEST.json'); manifest=loadj(manifest_raw)
  check('Archive member paths are unique and safe',len(names)==len(set(names)) and all(safe(n) for n in names))
  rows=manifest['members']; by_path={r['path']:r for r in rows}
  check('Internal manifest inventory count equals archive payload count',manifest['memberCountExcludingSelf']==len(rows)==len(names)-1,{'archiveMembers':len(names),'payloadMembers':len(rows)})
  check('External delivery manifest hash binds the internal manifest bytes',sha(manifest_raw)==delivery['memberManifestSha256'])
  for row in rows:
   n=row['path']
   if n not in names:
    failures.append({'member':n,'problem':'missing'}); continue
   b=z.read(n)
   if (len(b),sha(b),crc(b))!=(row['bytes'],row['sha256'],row['crc32']): failures.append({'member':n,'problem':'size/hash/CRC mismatch'})
  check('Every payload member matches its internal size/SHA/CRC binding',not failures,failures[:25])
  check('No unmanifested ZIP payload exists',set(names)==set(by_path)|{'MEMBER_MANIFEST.json'})
  # Verify the bound live files against their source bytes, including the current index and catalog.
  for logical,rec in loadj(z.read('sourceBindings/CURRENT_SOURCE_BINDINGS_263.json')).items():
   b=Path(ROOT/rec['path']).read_bytes()
   if (len(b),sha(b),crc(b))!=(rec['bytes'],rec['sha256'],rec['crc32']): failures.append({'source':logical,'problem':'current source differs from bound packet bytes'})
  check('All current authority, index, catalog, and accepted source bindings still match disk',not any('source' in f for f in failures),[f for f in failures if 'source' in f][:20])
  index=loadj(z.read('current/authored_review_index.json'))
  gas_entry=next(x for x in index['entries'] if x['id']=='gaseous-form')
  ray_entry=next(x for x in index['entries'] if x['id']=='ray-of-frost')
  catalog=loadj(z.read('current/catalog.json'))
  low=loadj(z.read('source/GASEOUS_FORM/candidate_low_rank_136.json'))
  gas=low['spells'][132]
  receipt=loadj(z.read('source/GASEOUS_FORM/LOW_RANK_136_EXACT_FULFILLMENT.json'))
  check('Gaseous Form resolves through exact current index pointer and complete reviewed envelope',gas_entry['procedureFile']=='candidate_low_rank_136.json' and gas_entry['procedurePointer']=='/spells/132/operationalCandidate' and gas['id']=='gaseous-form' and gas['reviewEvidence']['exactCandidateApproval'] is True)
  check('Gaseous Form envelope and exact fulfillment receipt share the reviewer reply',receipt['finalReplyId']==gas['reviewEvidence']['finalReplyId'] and receipt['status'].startswith('fulfilled'))
  ray=catalog['spells'][411]['operational']
  check('Ray of Frost source pointer binds 10-foot, one-d8 cold operation',ray_entry['procedurePointer']=='/spells/411/operational' and ray['rangeFeet']==10 and '1d8 cold damage' in ray['resolution'])
  prior=loadj(z.read('return246/members/MEMBER_MANIFEST.json'))
  old_bytes=z.read('return246/DD_Rank9_SoulReflection_Director_Return246_HELD.zip')
  old_delivery=loadj(z.read('return246/DD_Rank9_SoulReflection_Director_Return246_DELIVERY.json'))
  check('Return246 exact archive and member manifest are preserved and bound',sha(old_bytes)==old_delivery['archive']['sha256'] and prior['memberCountExcludingSelf']==len(prior['members']))
  prior_fail=[]
  with zipfile.ZipFile(__import__('io').BytesIO(old_bytes)) as pz:
   for r in prior['members']:
    b=pz.read(r['path'])
    if (len(b),sha(b),crc(b))!=(r['bytes'],r['sha256'],r['crc32']): prior_fail.append(r['path'])
  check('Return246 internal member hashes verify independently',not prior_fail,prior_fail[:15])
  profile=loadj(z.read('return246/members/prior/ACTOR_PROFILES.json'))['W17-IR207']
  check('W17 source-built actor retains non-campaign qualification and Gaseous Form preparation',profile['campaignExistenceVerified'] is False and 'gaseous-form' in profile['spellbook'] and 'gaseous-form' in profile['prepared'])
  for name in ['cases/FORM_SNAPSHOT_263.json','cases/COPIED_CONCENTRATION_263.json','cases/ORIGINAL_ZERO_263.json','cases/ORIGINAL_CARGO_263.json']:
   case=loadj(z.read(name)); events=case['events']; prior_after=case['initialState']; bad=[]
   if sha(canon(case['initialState']))!=case['initialSHA256']: bad.append('initial hash')
   times=[e['atSeconds'] for e in events]
   if times!=sorted(times): bad.append('nonmonotonic event times')
   for i,e in enumerate(events):
    if sha(canon(e['before']))!=e['beforeSHA256'] or sha(canon(e['after']))!=e['afterSHA256']: bad.append(f'event {i+1} state hash')
    if e['before']!=prior_after: bad.append(f'event {i+1} discontinuity')
    fwd=e['forward']; inv=e['inverse']
    if len(fwd)!=2 or len(inv)!=2 or fwd[0].get('op')!='test' or fwd[1].get('op')!='replace' or inv[0].get('op')!='test' or inv[1].get('op')!='replace': bad.append(f'event {i+1} operation shape')
    elif fwd[0].get('value')!=e['before'] or fwd[1].get('value')!=e['after'] or inv[0].get('value')!=e['after'] or inv[1].get('value')!=e['before']: bad.append(f'event {i+1} operation bindings')
    else:
     working=copy.deepcopy(e['before']); working=copy.deepcopy(fwd[1]['value'])
     if working!=e['after']: bad.append(f'event {i+1} forward replay')
     working=copy.deepcopy(inv[1]['value'])
     if working!=e['before']: bad.append(f'event {i+1} inverse replay')
    prior_after=e['after']
   if not events or prior_after!=case['finalState'] or sha(canon(case['finalState']))!=case['finalSHA256']: bad.append('final state binding')
   case_rows.append({'id':case['id'],'events':len(events),'forwardOperations':sum(len(e['forward']) for e in events),'inverseOperations':sum(len(e['inverse']) for e in events),'failures':bad})
  check('All four event cases have complete state chains, monotonic clocks, and reversible forward/inverse operations',all(not x['failures'] for x in case_rows),case_rows)
  form=loadj(z.read('cases/FORM_SNAPSHOT_263.json'))
  fstate=form['finalState']
  check('Changed-form trace preserves source deadline, same identity and no HP/RP reset',fstate['formRecords']['T']['endedAt']==8.0 and fstate['copiedForms']['R1']['endedAt']==8.0 and fstate['actors']['T']['hp']==104 and fstate['actors']['T']['rp']==59)
  conc=loadj(z.read('cases/COPIED_CONCENTRATION_263.json'))['finalState']
  check('Copied concentration trace records paid 5 RP, failed DC10 CON save, and retained HP100/RP59',conc['copiedConcentration']['R1']['status']=='ended-on-failed-save' and conc['copiedConcentration']['R1']['concentrationSave']['DC']==10 and conc['actors']['R1']['hp']==100 and conc['actors']['R1']['rp']==59)
  zero=loadj(z.read('cases/ORIGINAL_ZERO_263.json'))['finalState']
  check('Original-target zero trace resolves the 10-foot Ray of Frost and downstream actual death-save clock',zero['actors']['T']['hp']==0 and zero['actors']['T']['life']=='Downed' and zero['actors']['T']['deathSaves']=={'successes':1,'failures':0} and zero['spellRiders']['R1-RAYFROST-SLOW-263']['status']=='expired')
  cargo=loadj(z.read('cases/ORIGINAL_CARGO_263.json'))['finalState']; item=cargo['items']['T-map']; hist=cargo['cargoTrace']['events']
  check('Original T-map remains one owner-T item with exact suppression drop location through resume/end',item['owner']=='T' and item['custodian']=='ground' and item['position']==[15,0,0] and len([e for e in hist if e.get('item')=='T-map'])==4)
  beast_gap=loadj(z.read('source/ATTACHED_RECIPIENT_SOURCE_GAP_263.json'))
  check('Attached/no-phase source deficiency remains explicit and is not filled by a fixture',beast_gap['status']=='OPEN' and beast_gap['beastRows']==71 and beast_gap['rowsWithExplicitINTOrAbilityObject']==0)
  check('Packet does not accept/apply or modify canonical files',all(x['passed'] for x in checks) and not submission.get('acceptedIds') and not submission.get('appliedIds') and submission.get('canonicalChanges') is False)

 result={'id':'SOUL-REFLECTION-DELTA-263-INDEPENDENT-AUDIT','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','archive':{'path':ZIP.relative_to(ROOT).as_posix(),'bytes':len(archive),'sha256':sha(archive),'crc32':crc(archive)},
  'delivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':DELIVERY.stat().st_size,'sha256':sha(DELIVERY.read_bytes())},'authority':AUTH,
  'targetIds':['soul-reflection'],'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':sum(not x['passed'] for x in checks),'checks':checks,
  'caseCounts':case_rows,'acceptanceOrApplicationPerformed':False,'canonicalChanges':False,'githubChanges':False}
 AUDIT.write_bytes(enc(result))
 submission['independentAudit']={'path':AUDIT.relative_to(ROOT).as_posix(),'bytes':AUDIT.stat().st_size,'sha256':sha(AUDIT.read_bytes()),'status':result['status'],'checks':result['checkCount'],'failures':result['failedChecks']}
 submission['deliveryManifest']={'path':DELIVERY.relative_to(ROOT).as_posix(),'bytes':DELIVERY.stat().st_size,'sha256':sha(DELIVERY.read_bytes())}
 submission['status']='AUDITED_PREPARED_UNSENT' if result['status']=='PASS' else 'AUDIT_FAILED'
 SUBMISSION.write_bytes(enc(submission))
 print(json.dumps({'status':result['status'],'checks':result['checkCount'],'passed':result['passedChecks'],'failed':result['failedChecks'],'audit':str(AUDIT)},indent=2))
 if result['status']!='PASS': raise SystemExit(1)

if __name__=='__main__': main()
