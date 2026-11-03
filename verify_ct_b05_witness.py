"""Independent serialized-evidence verifier; does not import or run the builder."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,unicodedata,zlib,subprocess
R=Path(__file__).resolve().parent
A='docs/audit/2026-10-08/full-game/director-spell-review-129/'
O=A+'collapse_timeline_b05_witness_2026-11-03/'
def read(p):return json.loads((R/p).read_bytes())
def norm(o):
 if isinstance(o,str):return unicodedata.normalize('NFC',o)
 if isinstance(o,list):return [norm(x) for x in o]
 if isinstance(o,dict):return {norm(k):norm(v) for k,v in o.items()}
 return o
def hashstate(s):return hashlib.sha256(json.dumps(norm(s),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
checks=[]
def check(label,value):
 checks.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
def replay(s,ops):
 result=deepcopy(s)
 for o in ops:
  pp=o['path'].split('/')[1:];parts=[x.replace('~1','/').replace('~0','~') for x in pp]
  parent=result
  for p in parts[:-1]:parent=parent[p]
  leaf=parts[-1]
  assert (leaf in parent)==o['beforeExists'],o['path']
  if o['beforeExists']:assert parent[leaf]==o['before'],o['path']
  if o['afterExists']:parent[leaf]=deepcopy(o['after'])
  else:del parent[leaf]
 return result
def binding(b):
 raw=(R/b['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=b['sha256']:
  raw=subprocess.check_output(['git','show',W['sourceCommit']+':'+b['path']],cwd=R)
 check('raw-source:'+b['path'],hashlib.sha256(raw).hexdigest()==b['sha256'] and len(raw)==b['bytes'])
 if 'crc32' in b:check('crc:'+b['path'],f'{zlib.crc32(raw):08x}'==b['crc32'].lower())
def byid(branch,name):return next(e for e in branch['events'] if e['id']==name)
def clear(a,b):return any(min(a[k][1],b[k][1])<=max(a[k][0],b[k][0]) for k in 'xyz')
W=read(O+'CT_B05_P04_TESTONLY_WITNESS_PACKET_01.json');P=read(W['proposal']['path']);S=P['proposedTestOnlyInputSpecification']
binding(W['proposal']);binding(W['ownerAuthorization'])
owner=read(W['ownerAuthorization']['path'])
check('actual-user-authorization-without-invented-verbatim-adoption',owner['ownerInstructionExact']=='then get it done' and owner['adoptedProposalSHA256']==W['proposal']['sha256'])
for b in W['sourceBindings']:binding(b)
parent=read(W['sourceParent']['path'])['events'][2]['after'];check('exact-parent',hashstate(parent)==W['sourceParent']['stateSHA256'])
paid=W['commonPaidRoot'];check('paid-root-hash',hashstate(paid)==W['commonPaidRootSHA256'])
check('paid-root-resources',paid['actors']['T']['RP']==38 and paid['actors']['W']['RP']==38 and paid['actors']['T']['budget']['Action']==0)
check('paid-root-two-casts',len(paid['casts'])==2 and len(paid['actors']['T']['resourceHistory'])==1 and len(paid['actors']['W']['resourceHistory'])==1)
check('no-pending-cast-after-resolution',paid['ctTestOnly']['pendingCast'] is None and paid['ctTestOnly']['resolvedCT'])
forwardCount=inverseCount=0
for n,b in enumerate(W['branches']):
 check('branch-name:'+str(n),b['id']==S['newBranchIds'][n])
 current=deepcopy(parent);last=-1;seen=set()
 for i,e in enumerate(b['events']):
  check(f'{n}:{i}:unique-time-order',e['id'] not in seen and e['atMs']>=last);seen.add(e['id']);last=e['atMs']
  check(f'{n}:{i}:before',current==e['beforeState'] and hashstate(current)==e['beforeStateSHA256'])
  current=replay(current,e['forward']);forwardCount+=len(e['forward'])
  check(f'{n}:{i}:after',current==e['afterState'] and hashstate(current)==e['afterStateSHA256'] and current['world']['nowMs']==e['atMs'])
 check(f'{n}:terminal',current==b['finalState'] and hashstate(current)==b['finalStateSHA256'])
 for i,e in enumerate(reversed(b['events'])):
  current=replay(current,e['inverse']);inverseCount+=len(e['inverse']);check(f'{n}:reverse:{i}',current==e['beforeState'])
 check(f'{n}:restored',current==parent)
 events=b['events'];commit=byid(b,'CT-B05-COMMIT')['afterState'];response=byid(b,'CT-B05-W-COUNTER-DECLINE')
 check(f'{n}:commit-before-response',response['beforeState']==commit and commit['actors']['T']['seenFamilies']==['collapse-timeline'] and commit['actors']['T']['lastSpell']=='collapse-timeline' and commit['actors']['T']['spellsThisTurn']==1)
 check(f'{n}:decline-no-cost',response['afterState']['actors']==response['beforeState']['actors'])
 check(f'{n}:same-paid-root',b['events'][b['commonPrefixEventCount']-1]['afterState']==paid)
 for who,starts,ends in [('W',[0,6000],[1900,7900]),('T',[2000,8000],[3900])]:
  a=b['finalState']['actors'][who];check(f'{n}:{who}:marker-histories',a['regularStarts']==starts and a['regularEnds']==ends)
  check(f'{n}:{who}:terminal-resource',a['RP']==38 and a['Dissonance']==0 and a['Refrain']==0 and a['spellsThisTurn']==0 and a['budget']['Reaction']==1)
 check(f'{n}:T-END-preserves-cast-flag',byid(b,'T-END-3900')['afterState']['actors']['T']['spellsThisTurn']==1)
 check(f'{n}:W-END-preserves-cast-flag',byid(b,'W-END-1900')['afterState']['actors']['W']['spellsThisTurn']==1)
 f=b['finalState'];check(f'{n}:deadline-original',f['obligations'][next(iter(f['obligations']))]['deadlineMs']==34560000100)
 check(f'{n}:six-second-advance',f['world']['nowMs']-paid['world']['nowMs']==6000)
 check(f'{n}:body-and-movement',f['actors']['W']['position']==[15,5,0] and f['actors']['W']['budget']['movement']==0)
 check(f'{n}:two-casts-only',len(f['casts'])==2)
 check(f'{n}:ArcaneWard-no-HP-change',f['actors']['W']['hp']==parent['actors']['W']['hp'] and f['actors']['W']['resistances']==parent['actors']['W']['resistances'])
 book=f['items']['book-W'];ob=f['obligations'][next(iter(f['obligations']))]
 if n==0:
  check('compatible-fulfillment',book['position']==[15,0,0] and book['custodian']=='cache' and book['owner']=='W' and ob['status']=='fulfilled' and ob['fulfilledAtMs']==6001 and f['actors']['W']['budget']['interaction']==0)
  check('compatible-support-contact',book['occupiedBoundsFt']['z'][0]==f['items']['CT-B05-SUPPORT-01']['topZ'])
 else:
  check('incompatible-no-placement',book['custodian']=='W' and book['position']==[15,1.5,2.5] and ob['status']=='pending' and f['actors']['W']['budget']['interaction']==1)
  u=f['ctTestOnly']['unavailableLedger']['CT-B05-SUPPORT-01']
  check('finite-no-recovery-contract',u['fromMs']==4000 and u['unavailableThroughMs']==34560000100 and u['availableAgainAtMs']==34560000101 and u['returnNotExecutedWithinHorizon'])
  check('intact-plate-custody',f['items']['CT-B05-SUPPORT-01']['custodian']=='CT-B05-UNAVAILABLE-LEDGER' and not f['items']['CT-B05-SUPPORT-01']['destroyed'])
 check(f'{n}:no-guarantee-promotion',ob['guaranteeProved'] is False and f['ctTestOnly']['guaranteeProved'] is False)
 for e in events:
  st=e['afterState']
  if 'ctTestOnly' not in st:continue
  actor=st['actors'];items=st['items']
  check(f'{n}:{e["id"]}:body-nonoverlap',clear(actor['W']['occupiedBoundsFt'],actor['T']['occupiedBoundsFt']))
  for who in ['W','T']:check(f'{n}:{e["id"]}:{who}:gate-clear',clear(actor[who]['occupiedBoundsFt'],items['gate']['occupiedBoundsFt']))
  for obs in [actor['T']['occupiedBoundsFt'],items['CT-B05-FOCUS-T-01']['occupiedBoundsFt'],items['gate']['occupiedBoundsFt']]:
   check(f'{n}:{e["id"]}:book-clear',clear(items['book-W']['occupiedBoundsFt'],obs))
  if e['id'].startswith('W-MOVE-'):
   for kind in ['body','book']:
    before=e['beforeState']['actors']['W']['occupiedBoundsFt'] if kind=='body' else e['beforeState']['items']['book-W']['occupiedBoundsFt']
    after=actor['W']['occupiedBoundsFt'] if kind=='body' else items['book-W']['occupiedBoundsFt']
    sweep={k:[min(before[k][0],after[k][0]),max(before[k][1],after[k][1])] for k in 'xyz'}
    for obs in [actor['T']['occupiedBoundsFt'],items['CT-B05-FOCUS-T-01']['occupiedBoundsFt'],items['gate']['occupiedBoundsFt']]:check(f'{n}:{e["id"]}:{kind}:continuous-clear',clear(sweep,obs))
sel=W['selection'];check('atomic-selected-settlement',replay(paid,sel['forward'])==sel['afterState'])
rollback=replay(sel['afterState'],sel['inverse']);check('rollback-to-paid-root',rollback==paid and rollback['actors']['T']['RP']==38)
retry=sel['sameKeyRetry'];check('receipt-first-retry',retry['beforeState']==retry['afterState']==sel['afterState'] and retry['beforeSHA256']==retry['afterSHA256'] and retry['receipt']['newOperations']==0)
filter=sel['filteredCandidate'];check('incompatible-filter-no-refund',filter['paidRootBeforeSHA256']==filter['paidRootAfterSHA256']==W['commonPaidRootSHA256'] and filter['refundRP']==0 and not filter['candidateApplied'])
for e in reversed(W['branches'][0]['events'][:W['branches'][0]['commonPrefixEventCount']]):rollback=replay(rollback,e['inverse'])
check('full-atomic-inverse-exact-parent',rollback==parent==W['fullAudit']['restoredState'])
check('all-non-effects',W['limits']=={'runtimeExecuted':False,'campaignEvent':False,'witnessesSealed':False,'guaranteeProved':False,'blockersClosed':[],'retainedOpenBlockers':['TF192-B05','TF192-B02'],'nativeAuthorityCreated':False,'EPExceptionalOperationsImported':False,'queueChangedByWitness':False})
raw=(R/(O+'CT_B05_P04_TESTONLY_WITNESS_PACKET_01.json')).read_bytes()
report={'id':'CT-B05-P04-INDEPENDENT-VERIFIER-01','status':'PASS','method':'Separate verifier implementation, same assistant/session; not an independent human or external auditor. Replayed serialized patches without importing builder.',
        'witnessSHA256':hashlib.sha256(raw).hexdigest(),'checksPassed':len(checks),'checksFailed':0,
        'recordedEvents':sum(len(b['events']) for b in W['branches']),'forwardOperations':forwardCount,'inverseOperations':inverseCount,
        'atomicSettlementOperations':len(sel['forward']),'sourceParentRestored':True,'checks':checks}
(R/(O+'VALIDATION_CT_B05_P04_01.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
