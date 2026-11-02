import copy,hashlib,json,zlib,subprocess
from pathlib import Path
def locate_repository():
 for base in [Path.cwd(), *Path(__file__).resolve().parents]:
  for candidate in [base, base/'decay_repo']:
   if (candidate/'DescentReviewChanges').is_dir(): return candidate
 raise RuntimeError('Repository not found')
ROOT=locate_repository()
A=Path('docs/audit/2026-10-08/full-game/director-spell-review-129');O=A/'summon_avatar_of_decay_static_closure_487';C=Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9decay_static_reviewed_487');I=Path('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
def read(p):return json.loads((ROOT/p).read_bytes())
checks=[]
def ck(name,ok):
 checks.append({'check':name,'pass':bool(ok)})
 if not ok:raise AssertionError(name)
def binding(p):
 b=(ROOT/p).read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def check_binding(b):
 if isinstance(b,dict):
  if {'path','bytes','sha256'}<=b.keys() and (ROOT/b['path']).is_file():
   # Explicit historical index binding is to the preapplication tree.
   if b['path']==str(I) and b['sha256']=='0c69755ec80df390b4e8676bfdd81db63f9429f6faf1f23d74bbd99c0856684b':return
   actual=binding(b['path']);ck('binding '+b['path'],all(actual[k]==b[k] for k in ['bytes','sha256']))
  for v in b.values():check_binding(v)
 elif isinstance(b,list):
  for v in b:check_binding(v)
index=read(I);old=json.loads(Path(__file__).with_name('index_before.json').read_bytes() if Path(__file__).with_name('index_before.json').exists() else subprocess.check_output(['git','show','c6d6a3a0e084008fc260dc6096c2b01fd77e67d6:'+str(I)],cwd=ROOT));q=read(A/'CURRENT_SPELL_QUEUE_479.json');oq=read(A/'CURRENT_SPELL_QUEUE_478.json');m=read(C/'MODEL.json');cov=read(C/'CASE_COVERAGE.json');accept=read(O/'DIRECTOR_ACCEPTANCE_487.json');app=read(O/'APPLICATION_487.json')
ck('exact single changed row',[n for n,(x,y) in enumerate(zip(old['entries'],index['entries'])) if x!=y]==[670]);ck('all 848 identities conserved',len(index['entries'])==len(old['entries'])==848)
ck('only counts and one row changed',{k:v for k,v in index.items() if k not in ['authoredCounts','representationCounts','entries']}=={k:v for k,v in old.items() if k not in ['authoredCounts','representationCounts','entries']})
ck('833 to 834',index['authoredCounts']=={'reviewed':834,'pending':14});ck('standalone plus one',index['representationCounts']=={**old['representationCounts'],'completeReviewedStandaloneProcedures':558})
ck('pending enumerates exact rows',set(q['remainingPendingIds'])=={e['id'] for e in index['entries'] if e['authoredStatus']=='pending-authored-procedure'})
ck('pending next order exact',q['continuingPriorityOrder']==oq['continuingPriorityOrder'][1:] and q['nextIdentity']=='reverse-gravity-field')
ck('acceptance and application only Decay',accept['acceptedIds']==app['acceptedIds']==app['appliedIds']==['summon-avatar-of-decay'] and accept['appliedIds']==[])
ck('accepted unapplied zero after application',q['currentAuthority']=={'reviewedApplied':834,'pending':14,'acceptedUnapplied':0,'completeStandaloneProcedures':558,'scopedInterfaces':173})
ck('12 qualifications exact',m['sharedRequirements']['qualifications']==read(A/'rank9_summon_avatar_of_decay_return333_received/payload/evidence/RETURN285_QUALIFICATIONS.json')['qualifications'])
ck('retained procedure semantically exact',m['spells'][0]['sourceProcedureRecord']==read(A/'rank9_summon_avatar_of_decay_return333_received/payload/input/05_RETURN285_AVATAR_PROCEDURE.json'))
ck('native card exact blocked/null',m['spells'][0]['nativeCard']==read(I.parent/'catalog.json')['spells'][670] and m['spells'][0]['nativeCard']['operational'] is None)
ck('no runtime promotion',not m['runtimeSelectionEnabled'] and not q['runtimeSelectionEnabled'])
ck('13 historical cases untouched',cov['historicalCases']==read(A/'rank9_summon_avatar_of_decay_return333_received/payload/PRESERVED_OUTCOMES.json')['exactCaseBindings'] and not cov['historicalCasesReplayed'])
ck('four residuals exact scope',[x['id'] for x in cov['residuals']]==['SH333-R01','SH333-R02','SH333-R03','SH333-R04'] and cov['openStaticIntegrations']==[])
ck('R02 source qualification retained',not accept['R02ActualProviderQualified'] and 'abstract' in m['sharedRequirements']['R02ReviewOnlyRevision'])
ck('no new witness seal',not accept['newEvidenceSealIssued'])
for p in [O/'DIRECTOR_ACCEPTANCE_487.json',O/'APPLICATION_487.json',O/'IDENTITY_RECONCILIATION_487.json',C/'MODEL.json',C/'CASE_COVERAGE.json',C/'CANDIDATE_PACKAGE_MANIFEST.json',A/'CURRENT_SPELL_QUEUE_479.json',A/'CURRENT_HANDOFF_479.json',A/'CURRENT14_PENDING_IDENTITY_AUDIT_479.json']:
 check_binding(read(p))
report={'id':'DECAY-APPLICATION-VALIDATION-487','status':'PASS','checksPassed':len(checks),'failures':0,'checks':checks,'appliedIds':['summon-avatar-of-decay'],'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','indexAfter':binding(I),'authorityAfter':q['currentAuthority'],'historicalReplaysPerformed':False,'publicationNotYetAsserted':True}
(ROOT/O/'APPLICATION_VALIDATION_487.json').write_text(json.dumps(report,indent=2)+'\n')
if Path(__file__).with_name('publish_paths.json').exists():
 paths=json.loads(Path(__file__).with_name('publish_paths.json').read_bytes());paths.append(str(O/'APPLICATION_VALIDATION_487.json'));Path(__file__).with_name('publish_paths.json').write_text(json.dumps(sorted(set(paths)),indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'index':binding(I),'authority':q['currentAuthority']},indent=2))
