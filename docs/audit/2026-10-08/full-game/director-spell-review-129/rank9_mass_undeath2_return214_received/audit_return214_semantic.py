from __future__ import annotations
import json, pathlib, hashlib, zipfile, zlib, gc
BASE=pathlib.Path(r'docs/audit/2026-10-08/full-game/director-spell-review-129')
REC=BASE/'rank9_mass_undeath2_return214_received'
EX=REC/'extracted'
DELTA=REC/'DD_Rank9_MassUndeath2_Director_Return214_DELTA.zip'
DM=REC/'DD_Rank9_MassUndeath2_Director_Return214_DELTA_DELIVERY.json'
ORIG_DM=REC/'DD_Rank9_MassUndeath2_Director_Return214_DELIVERY.json'
PRIOR=BASE/'rank9_mass_undeath2_return213_received/DD_Rank9_MassUndeath2_Director_Return213_HELD.zip'
SOURCE=pathlib.Path(r'docs/audit/2026-10-08/full-game/DD_Rank9_Mass_Undeath_2_Source_Conference_02.zip')
INDEX=pathlib.Path(r'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
CAT=pathlib.Path(r'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')
checks=[]
def add(name,ok,detail=None): checks.append({'check':name,'passed':bool(ok),'detail':detail})
def filehash(p):
 h=hashlib.sha256(); c=0; n=0
 with p.open('rb') as f:
  while True:
   b=f.read(1024*1024)
   if not b: break
   h.update(b); c=zlib.crc32(b,c); n+=len(b)
 return {'bytes':n,'sha256':h.hexdigest(),'crc32':f'{c&0xffffffff:08x}'}
def memberhash(z,name):
 h=hashlib.sha256(); c=0; n=0
 with z.open(name) as f:
  while True:
   b=f.read(1024*1024)
   if not b: break
   h.update(b); c=zlib.crc32(b,c); n+=len(b)
 return {'bytes':n,'sha256':h.hexdigest(),'crc32':f'{c&0xffffffff:08x}'}
def canon_hash(v):
 raw=json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
 return hashlib.sha256(raw).hexdigest()
# Transport and exact member bindings.
dm=json.loads(DM.read_text(encoding='utf-8')); orig_dm=json.loads(ORIG_DM.read_text(encoding='utf-8'))
delta_h=filehash(DELTA); add('delta outer binding exact',delta_h['bytes']==73870874 and delta_h['sha256']=='897c2cc997fd10f242d8e4b53389adf2f12ac52e1a910954355862f62c756faf' and delta_h['crc32']=='5a23a20a',delta_h)
add('delta delivery manifest bound to archive',dm.get('sha256')==delta_h['sha256'] and dm.get('bytes')==delta_h['bytes'] and dm.get('crc32')==delta_h['crc32'])
add('original delivery manifest byte binding',filehash(ORIG_DM)['sha256']=='7bca56ad0716d82bd4af00d633809139209544c83527b581fdb26c2cd56f2607' and orig_dm.get('sha256')=='b784f3568f9806a902ff565f0d739ebc6642e80293175066cdc3e89c3ecc2114')
with zipfile.ZipFile(DELTA) as z:
 bad=z.testzip(); names=z.namelist(); allowed=dm.get('allowlist',[]); members=dm.get('members',[])
 add('delta ZIP CRC integrity',bad is None,bad)
 add('exact unique allowlist',len(names)==len(set(names)) and set(names)==set(allowed) and len(names)==40,{'actual':len(names),'allowlist':len(allowed)})
 member_results=[]
 for item in members:
  got=memberhash(z,item['path']); ok=got['bytes']==item['bytes'] and got['sha256']==item['sha256'] and got['crc32']==item['crc32']; member_results.append(ok)
 add('all 40 archive members match byte/hash/CRC allowlist',all(member_results),{'passed':sum(member_results),'total':len(member_results)})
# External prior and source conference bindings.
ph=filehash(PRIOR); ext=dm.get('externalRequiredMembers',[]); external=next((x for x in ext if x.get('path')=='prior/Return213.zip'),{})
add('external Return213 binding exact local archive',ph['bytes']==370069024 and ph['sha256']=='b041264b058179841418c12233a5a34d78aaf7850a23513ac55237ec12d3bd07' and ph['crc32']=='dab10b6f' and external.get('bytes')==ph['bytes'] and external.get('sha256')==ph['sha256'] and external.get('crc32')==ph['crc32'])
sh=filehash(SOURCE); add('Source Conference 02 archive exact',sh['bytes']==291977874 and sh['sha256']=='4af12a5cd32fc8cbdab98e204ef21965d11d1a3fa178bbcff64ddc64deac779d')
source_map=json.loads((EX/'RULE_SOURCE_MAP.json').read_text(encoding='utf-8'))
source_entries=[v for group in source_map['rules'].values() for v in group]
with zipfile.ZipFile(SOURCE) as sz:
 source_results=[]
 for ent in source_entries:
  p=pathlib.Path(ent['path']); local=filehash(p)
  member='sources/'+ent['path']; archived=memberhash(sz,member)
  source_results.append(local['bytes']==ent['bytes'] and local['sha256']==ent['sha256'] and archived['bytes']==ent['bytes'] and archived['sha256']==ent['sha256'])
 add('all RULE_SOURCE_MAP sources match local and conference archive',all(source_results),{'passed':sum(source_results),'total':len(source_results)})
 # Exact specifically cited rule bindings from user request.
 needed={
  'DescentReviewChanges/ReviewBible/data/director/cosmology/epilogue_relic_null_reviewed_01.json':(180794,'ca4145e988da1aab10184328e11de5de0f529aa4b907df9891f46bffc9f8a637'),
  'DescentReviewChanges/ReviewBible/docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md':(59823,'8ff5422a3adc8aeec5a6b70ae79608def0cc924f0ae7487040c99da2f6ca3980'),
  'DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_DEATH_PLAYTEST.md':(23410,'8d68794687b97da70aaff9953f9724e31e9fa3c8568fd4c2f9e8fd05d34c93f7'),
  'DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md':(67451,'55f486de8d38a6734f8f0f2f62066401504f5b1311ebe66693175876b3f7aa6d')}
 needed_results=[]
 for p,(n,h) in needed.items():
  a=filehash(pathlib.Path(p)); b=memberhash(sz,'sources/'+p); needed_results.append(a['bytes']==n and a['sha256']==h and b['bytes']==n and b['sha256']==h)
 add('four named rule sources match user-supplied byte bindings',all(needed_results),{'passed':sum(needed_results),'total':len(needed_results)})
# Independently verify every reversible case trace against snapshot hashes and exact full-state root patches.
def verify_case(doc, name):
 events=doc['events']; prev=doc['initialState']; before_total=None; event_ops=0
 for i,e in enumerate(events):
  b=e['before']; a=e['after']
  if i==0 and b!=doc['initialState']: return False, 'first-before'
  if i and b!=prev: return False, f'continuity:{i}'
  if canon_hash(b)!=e['beforeSHA256'] or canon_hash(a)!=e['afterSHA256']: return False, f'hash:{i}'
  f=e['forward']; inv=e['inverse']; event_ops+=len(f)+len(inv)
  if len(f)!=2 or len(inv)!=2: return False, f'op-count:{i}'
  if f[0].get('op')!='test' or f[0].get('path')!='' or f[0].get('value')!=b: return False, f'fwd-test:{i}'
  if f[1].get('op')!='replace' or f[1].get('path')!='' or f[1].get('value')!=a: return False, f'fwd-apply:{i}'
  if inv[0].get('op')!='test' or inv[0].get('path')!='' or inv[0].get('value')!=a: return False, f'inv-test:{i}'
  if inv[1].get('op')!='replace' or inv[1].get('path')!='' or inv[1].get('value')!=b: return False, f'inv-apply:{i}'
  prev=a
 if prev!=doc['finalState']: return False,'final-state'
 return True,event_ops
new_files=sorted((EX/'cases').glob('*.json'))
new_ids=[]; total_events=0; total_ops=0; new_ok=[]
for p in new_files:
 d=json.loads(p.read_text(encoding='utf-8')); new_ids.append(d.get('id')); ok,info=verify_case(d,d.get('id')); new_ok.append(ok); total_events+=len(d['events']); total_ops+=info if ok else 0; del d; gc.collect()
add('all 13 new case traces replay and invert exactly',len(new_files)==13 and all(new_ok),{'cases':len(new_files),'passed':sum(new_ok),'events':total_events,'operations':total_ops})
prior_ids=[]; prior_ok=[]; prior_events=0; prior_ops=0
with zipfile.ZipFile(PRIOR) as pz:
 prior_case_names=sorted(n for n in pz.namelist() if n.startswith('cases/') and n.endswith('.json'))
 for name in prior_case_names:
  d=json.loads(pz.read(name).decode('utf-8')); prior_ids.append(d.get('id')); ok,info=verify_case(d,d.get('id')); prior_ok.append(ok); prior_events+=len(d['events']); prior_ops+=info if ok else 0; del d; gc.collect()
add('all preserved Return213 case traces replay and invert exactly',len(prior_case_names)==17 and all(prior_ok),{'cases':len(prior_case_names),'passed':sum(prior_ok),'events':prior_events,'operations':prior_ops})
add('aggregate case/event/operation counts match decision',len(set(new_ids+prior_ids))==30 and prior_events+total_events==847 and prior_ops+total_ops==3388,{'distinctCases':len(set(new_ids+prior_ids)),'events':prior_events+total_events,'ops':prior_ops+total_ops})
# Exact decision and no-application state.
dec=json.loads((EX/'DIRECTOR_DECISION_214.json').read_text(encoding='utf-8'))
accepted=['field-of-endless-dead','plague-of-undeath']
add('director exact acceptance and unapplied state',dec.get('accepted') is True and dec.get('applied') is False and dec.get('acceptedIds')==accepted and dec.get('appliedIds')==[] and dec.get('heldTargetIds')==[])
add('Return214 independent machine reports pass',all(json.loads((EX/f).read_text(encoding='utf-8')).get('passed') is True for f in ['SOURCE_VERIFICATION_214.json','ACTOR_ACCESS_CHECK_214.json','DATA_INTEGRITY_CHECK_214.json','SEMANTIC_NUMERICAL_CHECK_214.json','INDEPENDENT_SEMANTIC_FAILURE_CHECK_214.json']))
# Reassess semantics from actual state histories rather than supplied statuses alone.
null_ok=[]
for fid,fn in [('field-of-endless-dead','FE214-NULL-HISTORY.json'),('plague-of-undeath','PU214-NULL-HISTORY.json')]:
 d=json.loads((EX/'cases'/fn).read_text(encoding='utf-8'))
 init=d['initialState']; nf=init['nullField']; actor=init['actors']['B']; events=d['events']
 save_event=next(e for e in events if e['time']==-590); nf_after=save_event['after']['nullField']['B']; save=nf_after['hourlySaves'][-1]
 exit_event=next(e for e in events if e['time']==-588); ve=exit_event['after']['actors']['B']['nullVeil']
 root_event=next(e for e in events if e['time']==1.2); root=root_event['after']['roots']['NULL-B-ROOT']; veil=root_event['after']['actors']['B']['nullVeil']; body=root_event['after']['bodies']['D00']
 ok=(nf['fieldId']=='NULL-FIELD-QUIET-WELL-1' and nf['centerXY']==[0,0] and nf['radiusFeet']==7.5 and nf['zMin']==0 and nf['zMax']==10 and actor['profile']['classLevel']==17 and actor['profile']['saves']['WIS']==9 and save['d20']==4 and save['DC']==15 and save['total']==13 and save['total']==save['d20']+save['WIS'] and save['success'] is False and save['alive'] is True and nf_after['inside'] is True and nf_after['accumulatedSeconds']==0 and exit_event['after']['nullField']['B']['inside'] is False and exit_event['after']['nullField']['B']['accumulatedSeconds']==2 and ve['active'] and not ve['suppressed'] and root['dealer']=='B' and root['recipient']=='F/D00' and root['damage']==24 and root['recipientHPbefore']==20 and root['normalHPafter']==0 and root['nullNonlethal'] and root['snapshotVeil']['active'] and not root['snapshotVeil']['suppressed'] and veil['active'] and not veil['suppressed'] and 'NullDisabled' in body['animation']['conditions'] and 'Incapacitated' in body['animation']['conditions'] and actor['nullVeil'] is None)
 null_ok.append(ok); del d; gc.collect()
add('Null exposure/save/unsuppressed same-dealer root verified in both spells',all(null_ok),{'passed':sum(null_ok),'total':len(null_ok),'keyFacts':'exact field; WIS9, d20=4, 13<15; residual 2s after exit; same B dealer, minion recipient'})
# Exact held external boundaries and lifecycle branches.
reass=json.loads((EX/'BLOCKER_REASSESSMENT_214.json').read_text(encoding='utf-8'))
conditional={x['id'] for x in reass.get('conditionalBoundaries',[])}
add('only two stated missing external boundaries retained conditionally',conditional=={'MU214-C01-CONSUMED-REMAINS-RESURRECTION','MU214-C02-CONSTRUCTED-CORPSE'})
# Case evidence requirements must be present for both identities.
case_text={p.stem:p.read_text(encoding='utf-8') for p in new_files}
required_labels={
 'FE214-NULL-HISTORY':['exact60minute due WIS save fails','same B creates actual Null root'],
 'PU214-NULL-HISTORY':['exact60minute due WIS save fails','same B creates actual Null root'],
 'FE214-DENIAL-RESURRECTION':['A pays animation source; Denial is not an animation blocker','same U returns at1HP'],
 'PU214-DENIAL-RESURRECTION':['A pays animation source; Denial is not an animation blocker','same U returns at1HP'],
 'FE214-ORDER-INCAPACITY':[''], 'FE214-ORDER-DEATH':[''],
 'PU214-ORDER-INCAPACITY':[''], 'PU214-ORDER-DEATH':[''],
 'FE214-MIRROR-CONTROL':[''], 'PU214-MIRROR-CONTROL':[''],
 'FE214-SUPPRESSED-FORMATION':[''], 'PU214-SUPPRESSED-FORMATION':[''],
 'PU214-DAMAGE-CONCENTRATION':['']}
label_check=[]
for p in new_files:
 d=json.loads(p.read_text(encoding='utf-8')); labels=[e['label'] for e in d['events']]
 if d['id'] in required_labels:
  for token in required_labels[d['id']]:
   if token: label_check.append(any(token in l for l in labels))
# Both original spell clauses should be present and seven inherited identities remain untouched.
add('required Null and Denial histories have explicit event witnesses',all(label_check),{'passed':sum(label_check),'total':len(label_check)})
add('seven inherited pending holds and prior source questions retained',len(dec.get('retainedInheritedHeldIds',[]))==7 and dec.get('counts',{}).get('originalQuestions')==24 and dec.get('counts',{}).get('selectedDispositions')==24)
# The queue baseline and exact pending identities remain as submitted.
idx=json.loads(INDEX.read_text(encoding='utf-8')); cat=json.loads(CAT.read_text(encoding='utf-8'))
entries=idx['entries']; byid={x['id']:x for x in entries};
add('current review index remains at submitted 804/44 baseline and both exact targets pending',idx.get('authoredCounts',{}).get('reviewed')==804 and idx.get('authoredCounts',{}).get('pending')==44 and all(byid[x]['authoredStatus']=='pending-authored-procedure' for x in accepted))
add('catalog remains unchanged at its source-bound exact hash',filehash(CAT)['bytes']==5085187 and filehash(CAT)['sha256']=='773fb0b3b0fdb501858ded33c02d90dc4db3009bd1b9f7112c244d998218f05b')
# Reconfirm accepted procedure native snapshots equal current exact catalog entries.
cat_byid={x.get('id'):x for x in cat['spells']}
procedures=json.loads((EX/'PROCEDURES_214.json').read_text(encoding='utf-8'))
native_ok=[]
for proc in procedures:
 sid=proc['id']; native=proc['nativeCardUnchanged']; entry=byid[sid]
 native_ok.append(entry['wholeCardPointer']==f"/spells/{cat['spells'].index(cat_byid[sid])}" and native['id']==sid and native['status']==cat_byid[sid]['status'] and native['classAccess']==cat_byid[sid]['classAccess'] and native['operational'] is None and entry['sourceStatus']==native['status'])
add('accepted procedure preserves each pending native card and all three access routes',all(native_ok),{'passed':sum(native_ok),'total':len(native_ok)})
report={'id':'RETURN214-DELTA-SEMANTIC-INDEPENDENT-AUDIT','status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','acceptedIds':accepted,'applied':False,'authorityBeforeApplication':{'reviewedApplied':804,'pending':44,'acceptedUnapplied':0,'completeStandaloneProcedures':528,'scopedInterfaces':173},'counts':{'sourceRuleBindings':len(source_entries),'newCases':len(new_files),'preservedCases':len(prior_case_names),'newEvents':total_events,'preservedEvents':prior_events,'events':total_events+prior_events,'operations':total_ops+prior_ops},'checks':checks}
out=REC/'RETURN214_SEMANTIC_INDEPENDENT_AUDIT.json'; out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'checkCount':len(checks),'passed':sum(c['passed'] for c in checks),'failed':[c for c in checks if not c['passed']],'counts':report['counts'],'report':str(out)},indent=2))
