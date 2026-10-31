import copy,json,hashlib,zlib,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[5]
a=root/'docs/audit/2026-10-08/full-game/director-spell-review-129'
id='unravel-identity'
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
idxp=root/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
catp=root/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
oldp=root/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_reviewed_196/procedures/unravel-identity.json'
pkg=root/'DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9memorydenial6_unravel_reviewed_256'
old=rd(a/'authored_review_index.before_unravel_identity_256.json');new=rd(idxp);ops=rd(a/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_INDEX_OPERATIONS_256.json')
oldraw=(a/'authored_review_index.before_unravel_identity_256.json').read_bytes(); current=next(x for x in new['entries'] if x['id']==id); oldrow=next(x for x in old['entries'] if x['id']==id)
checks=[]
def ck(name,val): checks.append({'check':name,'passed':bool(val)})
ck('canonical counts 813/35',new['authoredCounts']=={'reviewed':813,'pending':35})
ck('standalone procedure count 537',new['representationCounts']['completeReviewedStandaloneProcedures']==537)
ck('scoped interfaces unchanged',new['representationCounts'].get('scopedInterfaces',173)==173)
ck('one spell entry changed',sum(a!=b for a,b in zip(old['entries'],new['entries']))==1 and len(old['entries'])==len(new['entries']))
ck('only accepted identity changed',current['id']==id and current['accepted'] and current['applied'])
ck('authored source status preserved',current['sourceStatus']==oldrow['sourceStatus']=='blocked-pending-operational-review')
ck('native catalog binding unchanged',bind(catp)['sha256']==rd(a/'CURRENT36_PENDING_IDENTITY_AUDIT_250.json')['catalogBinding']['sha256'])
pend={x['id'] for x in new['entries'] if x['authoredStatus']=='pending-authored-procedure'}; pa=rd(a/'CURRENT35_PENDING_IDENTITY_AUDIT_257.json')
ck('pending set exactly 35',len(pend)==35 and set(pa['pendingIds'])==pend and id not in pend)
ck('pending authority current',pa['authority']=={'reviewedApplied':813,'pending':35,'acceptedUnapplied':0,'completeStandaloneProcedures':537,'scopedInterfaces':173})
ck('queue and handoff current',rd(a/'CURRENT_SPELL_QUEUE_257.json')['currentAuthority']==pa['authority'] and rd(a/'CURRENT_HANDOFF_257.json')['currentAuthority']==pa['authority'])
ck('next GPT priority matter-conversion',rd(a/'CURRENT_SPELL_QUEUE_257.json')['next']['blocker']=='MF210-B02')
ck('application validation exists and passes',rd(a/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_APPLICATION_VALIDATION_256.json')['status']=='PASS')
ck('acceptance is exact GPT ACCEPT',rd(a/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_DIRECTOR_DECISION_256.json')['decision']=='EXACT_ACCEPT')
ck('MD196-B02 closed only',rd(a/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_APPLICATION_256.json')['closedBlockerIds']==['MD196-B02'])
ck('five qualifications remain',current['retainedQualificationIds']==['MD196-H01','MD196-H02','MD196-H03','MD196-H06','MD196-H08'])
proc=rd(pkg/'PROCEDURE_RECORD.json'); original=rd(oldp)
ck('accepted procedure text preserved',proc['procedure']==original['procedure'] and proc['accepted'] is True)
ck('runtime remains disabled',rd(pkg/'MODEL.json')['runtimeSelectionEnabled'] is False)
ck('no global suppression rule',rd(pkg/'MODEL.json')['sharedRequirements']['scope'].startswith('No global/shared'))
man=rd(pkg/'CANDIDATE_PACKAGE_MANIFEST.json')
ck('all package manifest hashes valid',all(len((root/f['path']).read_bytes())==f['bytes'] and sha((root/f['path']).read_bytes())==f['sha256'] for f in man['files']))
with zipfile.ZipFile(a/'DD_Rank9_MemoryDenial6_UnravelIdentity_IntegratedWitness_256.zip') as z:
 ck('accepted packet ZIP integrity',z.testzip() is None)
 ck('Packet256 witness/replay audits pass',rd(a/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_256_AUDIT.json')['checksPassed']==139 and rd(a/'UNRAVEL_IDENTITY_MD196_B02_FORWARD_INVERSE_REPLAY_256_AUDIT.json')['checksPassed']==164)
ck('index inverse exact',ops['inverseSemanticExact'] is True)
ck('backup matches before-index binding',sha(oldraw)==ops['before']['sha256'])
ck('application receipt targets only Unravel',rd(a/'RANK9_MEMORYDENIAL6_UNRAVEL_IDENTITY_APPLICATION_256.json')['appliedIds']==[id])
assert all(x['passed'] for x in checks),[x['check'] for x in checks if not x['passed']]
out={'id':'UNRAVEL-IDENTITY-APPLICATION-INDEPENDENT-VERIFICATION-256','status':'PASS','checksPassed':len(checks),'checkCount':len(checks),'checksFailed':0,'checks':checks,'indexAfter':bind(idxp),'catalogAfter':bind(catp),'pendingCount':len(pend),'next':rd(a/'CURRENT_SPELL_QUEUE_257.json')['next']}
(a/'UNRAVEL_IDENTITY_APPLICATION_INDEPENDENT_VERIFICATION_256.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))

