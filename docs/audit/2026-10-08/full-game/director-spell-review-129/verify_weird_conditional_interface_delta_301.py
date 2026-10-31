from __future__ import annotations
import hashlib,io,json,pathlib,zipfile,zlib
ROOT=pathlib.Path.cwd(); OUT=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129/rank9_weird_conditional_interface_delta_301'
ZIP=OUT/'DD_Rank9_Weird_ConditionalInterface_Completion_301.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def h(x):return sha(canon(x))
def apply(s,ops):
 cur=s
 for o in ops:
  assert o['path']==''
  if o['op']=='test':assert cur==o['value']
  elif o['op']=='replace':cur=o['value']
  else:raise AssertionError(o)
 return cur
def replay(events,start,end):
 cur=start
 for e in events:
  assert cur==e['before'] and h(cur)==e['beforeSHA256'],e['id']
  assert apply(cur,e['forward'])==e['after'] and h(e['after'])==e['afterSHA256'],e['id']
  assert apply(e['after'],e['inverse'])==cur,e['id']
  cur=e['after']
 assert cur==end
 for e in reversed(events):
  assert cur==e['after'];cur=apply(cur,e['inverse']);assert cur==e['before']
 assert cur==start
 return h(cur)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 names=z.namelist();assert len(names)==35 and len(names)==len(set(names))
 manifest=json.loads(z.read('DELIVERY_MANIFEST_301.json')); rows={x['path']:x for x in manifest['files']}
 assert len(rows)==34 and manifest['fileCountExcludingManifest']==34
 assert set(rows)==set(names)-{'DELIVERY_MANIFEST_301.json'}
 for n,r in rows.items():
  b=z.read(n);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and f'{zlib.crc32(b)&0xffffffff:08x}'==r['crc32'],n
 # Fresh replay all source payload cases preserved in the package.
 cases=sorted(n for n in names if n.startswith('preserved/cases/RANK9PSYCHICFEAR7-180-WEIRD') and n.endswith('.json'))
 assert len(cases)==18
 event_total=0;case_data={};case_sha={}
 for n in cases:
  raw=z.read(n);d=json.loads(raw);cur=d['initialState']
  for e in d['events']:
   assert cur==e['before'] and h(cur)==e['beforeSHA256'],e['id']
   assert apply(cur,e['forward'])==e['after'] and h(e['after'])==e['afterSHA256'],e['id']
   assert apply(e['after'],e['inverse'])==cur,e['id'];cur=e['after']
  assert cur==d['finalState']
  for e in reversed(d['events']):cur=apply(cur,e['inverse']);assert cur==e['before'],e['id']
  assert cur==d['initialState'];event_total+=len(d['events']);case_data[n.split('preserved/',1)[1]]=d;case_sha[n.split('preserved/',1)[1]]=sha(raw)
 assert event_total==1054
 # Fresh trace verification, independent of builder assertions.
 w1=json.loads(z.read('WCI-01_PROVIDERLESS_GAMEPLAY_ACTIVATION_DENIAL_301.json'))
 srcA='cases/RANK9PSYCHICFEAR7-180-WEIRD-A.json';caseA=case_data[srcA]
 assert w1['result']['decision']=='DENY' and w1['result']['payment']==0 and w1['result']['stateMutation'] is False
 assert w1['before']==w1['after'] and w1['beforeSHA256']==w1['afterSHA256']
 assert len(w1['history'])==len(caseA['events'])+1 and w1['history'][1:]==caseA['events']
 replay(w1['history'],caseA['initialState'],caseA['finalState'])
 w2=json.loads(z.read('WCI-02_CONDITIONAL_START_END_LIFECYCLE_TRACE_301.json'))
 fork2=caseA['events'][2]['after'];hist2=w2['history']
 assert w2['source']['caseSHA256']==case_sha[srcA] and w2['source']['forkStateSHA256']==h(fork2)
 assert len(w2['conditionalInputs'])==2 and len(hist2)==83 and hist2[:2]==w2['conditionalInputs']
 replay(hist2,fork2,caseA['finalState'])
 assert caseA['finalState']['time']==60.21 and w2['assertions']['originalExpiryStillAt60_21'] is True
 assert w2['assertions']['noAdditionalWeirdPacketOrFamilyOpportunity'] is True and w2['assertions']['noAddedRegularEndWISSave'] is True
 w3=json.loads(z.read('WCI-03_UNCONSCIOUS_RECIPIENT_BOUNDARY_TRACE_301.json'))
 src03='cases/RANK9PSYCHICFEAR7-180-WEIRD-B__external-help-wake-with-custody-retained.json';c03=case_data[src03];fork3=c03['events'][2]['after'];sched=w3['sharedSubsequentSchedule']
 assert w3['source']['caseSHA256']==case_sha[src03] and w3['source']['forkStateSHA256']==h(fork3)
 assert len(w3['branches'])==2 and {b['policy'] for b in w3['branches']}=={'deny','permit-as-hypothetical-input'}
 for b in w3['branches']:
  be=[b['inputEvent'],b['recipientActivationEvent']]
  assert be[0]['before']==be[0]['after']==fork3 and be[1]['before']==be[1]['after']==fork3
  assert be[1]['detail']['decision']=='DENY_PRECOMMIT' and be[1]['detail']['payment']==0
  replay(be+sched,fork3,c03['finalState'])
 assert any(e['time']==14.2 and 'wake' in e['kind'].lower() for e in sched)
 assert any(e['time']==60.21 and 'absolute expiry' in e['kind'] for e in sched)
 assert w3['assertions']['noActionBonusActionReactionSpeechOrMovementGranted'] is True
 assert w3['coverageLabel']=='null-concentration/unspent-recipient baseline preservation; not a demonstrated historical spent-resource or previously ended-concentration case.'
 assert w3['wakingCheckpoint']['recipientConditions']==['Prone'] and w3['wakingCheckpoint']['recipientConcentration'] is None
 assert w3['wakingCheckpoint']['recipientRP']==68 and w3['wakingCheckpoint']['casterRP']==42 and w3['wakingCheckpoint']['casterPaidRP']==26
 assert w3['expiryCheckpoint']['recipientConditions']==['Prone'] and w3['expiryCheckpoint']['recipientConcentration'] is None
 assert w3['expiryCheckpoint']['recipientRP']==68 and w3['expiryCheckpoint']['casterRP']==42 and w3['expiryCheckpoint']['casterPaidRP']==26
 clarification=json.loads(z.read('WCI03_PRESERVED_BASELINE_CLARIFICATION_301.json'))
 assert clarification['status'].startswith('PF301 unchanged')
 w4=json.loads(z.read('WCI-04_ATTACHED_PHASE_DEDUPLICATION_TRACE_301.json'))
 src04='cases/RANK9PSYCHICFEAR7-180-WEIRD-B__incapacitated-familiar-attached-phase.json';c04=case_data[src04];fork4=c04['events'][9]['after']
 assert w4['source']['caseSHA256']==case_sha[src04] and w4['source']['forkStateSHA256']==h(fork4)
 replay(w4['history'],fork4,c04['finalState'])
 opp=c04['finalState']['spellOpportunityHistory'];wins=[x for x in opp if x.get('family')=='weird' and x.get('target')=='F' and x.get('won') is True]
 assert sorted(x['numberedRound'] for x in wins)==[0,1]
 # Verify current authority is still only prepared, not accepted/applied.
 authority=json.loads(z.read('CURRENT_AUTHORITY_301.json'))
 assert authority['authority']=={'reviewedApplied':821,'pending':27,'acceptedUnapplied':0,'completeStandaloneProcedures':545,'scopedInterfaces':173}
 assert authority['weirdIndexStatus']['accepted'] is False and authority['weirdIndexStatus']['applied'] is False and authority['applicationPerformed'] is False
 source_map=json.loads(z.read('SOURCE_MAP_301.json'))
 corrected_request=json.loads(z.read('request/WEIRD_PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_301.json'))
 assert corrected_request['recordedAtUtc']=='2026-10-31T02:42:35Z'
 assert sha(z.read('request/WEIRD_PF182_B02_REQUEST_301_TIMESTAMP_CORRECTION.json'))==source_map['timestampCorrection']['sha256']
 idx=ROOT.joinpath(*source_map['currentIndex']['path'].split('/')).read_bytes();cat=ROOT.joinpath(*source_map['currentCatalog']['path'].split('/')).read_bytes()
 assert len(idx)==source_map['currentIndex']['bytes'] and sha(idx)==source_map['currentIndex']['sha256']
 assert len(cat)==source_map['currentCatalog']['bytes'] and sha(cat)==source_map['currentCatalog']['sha256']
 inner=zipfile.ZipFile(io.BytesIO(z.read('authority/DD_CurrentSpellAuthority_300.zip')))
 assert inner.testzip() is None
 irow=next(x for x in inner.namelist() if x.endswith('authored_review_index.json'))
 crow=next(x for x in inner.namelist() if x.endswith('catalog.json'))
 assert inner.read(irow)==idx and inner.read(crow)==cat
 print(json.dumps({'status':'PASS','outerBytes':ZIP.stat().st_size,'outerSHA256':sha(ZIP.read_bytes()),'members':len(names),'payloadBindings':len(rows),'freshSourceCases':18,'freshSourceEvents':event_total,'WCI01':'PASS','WCI02':'PASS','WCI03_branches':2,'WCI03_sharedScheduleEvents':len(sched),'WCI04':'PASS','currentAuthority':'821/27/0','canonicalIndexUnchanged':True,'catalogUnchanged':True,'accepted':False,'applied':False},indent=2))
