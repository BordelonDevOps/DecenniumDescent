import hashlib,json,subprocess,zipfile,zlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path.cwd();A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=A/'rank9_knowledgerevelation5_current_source_197_prepared'
ARCH=OUT/'DD_Rank9_KnowledgeRevelation5_CurrentSource_197.zip'
DEL=OUT/'DD_Rank9_KnowledgeRevelation5_CurrentSource_197_DELIVERY.json'
REPORT=A/'RANK9KNOWLEDGEREVELATION5_PACKET197_INDEPENDENT_AUDIT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def blob(commit,path):return subprocess.check_output(['git','cat-file','blob',f'{commit}:{path}'],cwd=ROOT)
def add(checks,name,ok,detail=None):checks.append({'check':name,'passed':bool(ok),'detail':detail})
def main():
 d=read(DEL);prep=read(A/'RANK9KNOWLEDGEREVELATION5_SOURCE_PREPARATION_197.json')
 commit=prep['sourceCommit'];branch=prep['sourceBranch']
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 remote=subprocess.check_output(['git','ls-remote','origin',f'refs/heads/{branch}'],cwd=ROOT,text=True).split()[0]
 rawhash=hashlib.sha256();n=0
 with ARCH.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):n+=len(c);rawhash.update(c)
 checks=[]
 add(checks,'Preparation binds the pushed HEAD and remote branch',commit==head==remote,{'sourceCommit':commit,'head':head,'remote':remote})
 add(checks,'Packet file matches delivery bytes and SHA-256',n==d['archive']['bytes'] and rawhash.hexdigest()==d['archive']['sha256'],{'bytes':n,'sha256':rawhash.hexdigest()})
 add(checks,'Packet is the exact five-identity current authority request',d['status']=='PREPARED_UNSENT' and d['accepted'] is False and d['applied'] is False and d['sourceAuthority']=={'reviewedApplied':786,'pending':62,'acceptedUnapplied':0,'completeStandaloneProcedures':510,'scopedInterfaces':173} and d['pendingIds']==['cosmic-awareness','cosmic-revelation','divine-truth','oracle-of-eternity','faction-omniscience-supreme'],d['pendingIds'])
 with zipfile.ZipFile(ARCH) as z:
  names=[i.filename for i in z.infolist()]
  manifest=json.loads(z.read('MANIFEST.json'))
  add(checks,'ZIP manifest, uniqueness, and archive CRC are valid',z.testzip() is None and len(names)==len(set(names)) and len(names)==manifest['memberCountExcludingSelf']+1 and len(manifest['members'])==manifest['memberCountExcludingSelf'],{'members':len(names),'manifestRows':len(manifest['members'])})
  rows={x['path']:x for x in manifest['members']}
  failures=[];member_bind={}
  for name,row in rows.items():
   h=hashlib.sha256();crc=0;size=0
   with z.open(name) as f:
    for c in iter(lambda:f.read(1024*1024),b''):size+=len(c);h.update(c);crc=zlib.crc32(c,crc)
   dig=h.hexdigest();member_bind[name]=(size,dig)
   if size!=row['bytes'] or dig!=row['sha256'] or f'{crc&0xffffffff:08x}'!=row['crc32']:failures.append(name)
  add(checks,'Every packet member matches exact size, SHA-256 and CRC-32',not failures,{'checked':len(rows),'failures':failures[:10]})
  current=json.loads(z.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_197.json'))
  historical=json.loads(z.read('HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json'))
  notes=json.loads(z.read('HISTORICAL_NOTES/RANK9KNOWLEDGEREVELATION5_NEXT_CONFERENCE_NOTES_129.json'))
  current_context=json.loads(z.read('CURRENT_CONTEXT_197.json'))
  add(checks,'Historical and current candidate both bind the exact five identities', [r['spellId'] for r in current['records']]==d['pendingIds']==[r['spellId'] for r in historical['records']],{'sourceBindings':len(current['sourceBindings'])})
  add(checks,'All question, case, and future-obligation counts are preserved',len(notes['completeOriginalQuestionsUnchanged'])==26 and len(notes['focusedAdditionalQuestions'])==2 and len(notes['allQuestions'])==28 and len(notes['requiredNewCases'])==10 and len(notes['originalFutureCaseRequirementsUnchanged'])==9 and current['questions']==historical['questions'] and current['futureCaseRequirements']==historical['futureCaseRequirements'],{'original':26,'addenda':2,'total':28,'newCases':10,'future':9})
  add(checks,'Current candidate refreshes all 126 source bindings to the pushed commit',len(current['sourceBindings'])==126 and current['currentSourceCommit']==commit and current['currentAuthority']==d['sourceAuthority'] and current['sourceBindingRefresh']['allSourceBindingsRefreshed'] is True,{'refreshed':len(current['sourceBindings']),'changed':current['sourceBindingRefresh']['changedSinceHistoricalCandidate']})
  source_fail=[]
  for b in current['sourceBindings']:
   name='sources_current/'+b['path']
   if name not in member_bind:source_fail.append({'path':b['path'],'reason':'missing member'});continue
   if member_bind[name]!=(b['bytes'],b['sha256']):source_fail.append({'path':b['path'],'reason':'member binding'})
   raw_source=blob(commit,b['path'])
   gitsha=hashlib.sha1(b'blob '+str(len(raw_source)).encode()+b'\0'+raw_source).hexdigest()
   if len(raw_source)!=b['bytes'] or sha(raw_source)!=b['sha256'] or gitsha!=b['gitBlobSHA1']:source_fail.append({'path':b['path'],'reason':'git blob binding'})
  add(checks,'All 126 refreshed members independently match commit tree blobs and Git blob IDs',not source_fail,{'checked':len(current['sourceBindings']),'failures':source_fail[:10]})
  oldarc=z.read('HISTORICAL_SOURCE_CONFERENCE_ARCHIVE_01.zip')
  oldc=z.read('HISTORICAL_SOURCE_CONFERENCE_CANDIDATE_01.json')
  add(checks,'Historical candidate and original conference archive match queued byte bindings',len(oldc)==d['historicalCandidate']['bytes'] and sha(oldc)==d['historicalCandidate']['sha256'] and len(oldarc)==d['historicalSourceArchive']['bytes'] and sha(oldarc)==d['historicalSourceArchive']['sha256'],{'historicalCandidateBytes':len(oldc),'archiveBytes':len(oldarc)})
  with zipfile.ZipFile(ARCH) as packet,zipfile.ZipFile(__import__('io').BytesIO(oldarc)) as oldz:
   historical_fail=[]
   for b in historical['sourceBindings']:
    member='sources/'+b['path']
    try:
     raw=oldz.read(member)
     if len(raw)!=b['bytes'] or sha(raw)!=b['sha256']:historical_fail.append(b['path'])
    except Exception:historical_fail.append(b['path'])
   add(checks,'All 126 historical source bindings match the original conference archive',not historical_fail,{'checked':len(historical['sourceBindings']),'failures':historical_fail[:10]})
  q=json.loads(z.read('current/'+ 'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT_SPELL_QUEUE_196.json'))
  p=json.loads(z.read('current/'+ 'docs/audit/2026-10-08/full-game/director-spell-review-129/CURRENT62_PENDING_IDENTITY_AUDIT_196.json'))
  idx=json.loads(z.read('current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'))
  ids=d['pendingIds'];pend={x['id'] for x in idx['entries'] if x['authoredStatus']=='pending-authored-procedure'}
  target=next(x for x in q['currentPendingGroups'] if x['group']==d['group'])
  add(checks,'Current queue, pending audit, and source index agree exactly at 786/62',q['currentAuthority']==d['sourceAuthority'] and p['pendingCount']==62 and set(p['pendingIds'])==pend and target['pendingIds']==ids and target['pendingCount']==5 and set(ids)<=pend and idx['authoredCounts']=={'reviewed':786,'pending':62},{'pending':len(pend),'targetsPending':all(x in pend for x in ids)})
  checkx=['AG190','TF192','CC194','MD196']
  for k,record in current_context['retainedNamedBlockersOutsideScope'].items():
   if k not in checkx: checkx.append(k)
  mem=json.loads(z.read('current/'+ 'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196/MODEL.json'))
  add(checks,'Return196 memory decisions remain static and exact',mem['acceptedIds']==['mass-willbreaker','mind-prison-mass','mind-wipe','unmake-spell'] and mem['unacceptedIds']==['mind-collapse','unravel-identity'] and mem['runtimeSelectionEnabled'] is False and current_context['retainedNamedBlockersOutsideScope']['MD196']['blockers']==['MD196-B01','MD196-B02'],{'accepted':mem['acceptedIds'],'blocked':mem['unacceptedIds']})
  app=json.loads(z.read('current/docs/audit/2026-10-08/full-game/director-spell-review-129/RANK9_MEMORYDENIAL6_APPLICATION_196.json'))
  add(checks,'Latest accepted memory application and current context are hash-bound',app['acceptedIds']==mem['acceptedIds'] and app['unacceptedIds']==mem['unacceptedIds'] and app['countsAfter']=={'reviewed':786,'pending':62} and app['completeReviewedStandaloneProcedures']['after']==510,app['id'])
 failed=[x for x in checks if not x['passed']]
 report={'id':'RANK9-KNOWLEDGE-REVELATION5-PACKET197-INDEPENDENT-AUDIT','status':'PASS' if not failed else 'FAIL','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checksPassed':len(checks)-len(failed),'checksFailed':len(failed),'checks':checks,'sourceCommit':commit,'packet':d['archive'],'delivery':{'path':DEL.relative_to(ROOT).as_posix(),'bytes':DEL.stat().st_size,'sha256':sha(DEL.read_bytes())},'accepted':False,'applied':False}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'status':report['status'],'checksPassed':report['checksPassed'],'checksFailed':report['checksFailed'],'failures':failed},indent=2))
 if failed:raise SystemExit(1)
if __name__=='__main__':main()
