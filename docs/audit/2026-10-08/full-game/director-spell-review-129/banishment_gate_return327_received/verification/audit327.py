import json, hashlib, pathlib, zipfile, zlib, copy, math
R=pathlib.Path(__file__).resolve().parent; S=R/'source'; P=R/'payload'; P.mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def binding(b,path=None):
 d={'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
 if path:d={'path':path,**d}
 return d
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
checks=[]
def check(id,ok,detail=None):
 checks.append({'id':id,'pass':bool(ok),**({'detail':detail} if detail is not None else {})})
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(a.read_bytes())
zpath=R.parent/'upload/DD_Rank9_BanishmentGate_CurrentSource_327.zip'; zb=zpath.read_bytes(); zm=read(S/'MANIFEST.json')
check('input-zip-sha256',sha(zb)=='0ff68b54ce84b1ad51604149ee37520b53284dfdf9a0b9dfa6a3eeec30a6db22')
with zipfile.ZipFile(zpath) as z:
 check('input-zip-crc',z.testzip() is None)
 check('input-exact-allowlist',set(z.namelist())=={'MANIFEST.json'}|{m['path'] for m in zm['members']} and len(z.namelist())==27)
 for m in zm['members']:
  b=z.read(m['path']); check('input-member:'+m['path'],all(binding(b)[k]==m[k] for k in ('bytes','sha256','crc32')))
  check('extraction:'+m['path'],b==(S/m['path']).read_bytes())
for f in S.rglob('*'):
 if f.is_file():cp(f,P/'evidence/packet327'/f.relative_to(S))
prior=read(S/'prior/PlanarGates5_Return200_DELIVERY.json'); rows={m['path']:m for m in prior['members']}
case_reports=[]; eventtotal=forwardtotal=inversetotal=clockmarkers=0
def replay(state,ops):
 for op in ops:
  if op['path']!='':raise ValueError('Unsupported non-root patch: '+str(op['path']))
  if op['op']=='test':
   if state!=op['value']:raise ValueError('Root test mismatch')
  elif op['op']=='replace':state=copy.deepcopy(op['value'])
  else:raise ValueError('Unsupported operation '+op['op'])
 return state
for f in sorted((S/'prior/cases').glob('*.json')):
 c=read(f); cid=c['id']; matches=[m for m in rows.values() if m['path'].endswith('/'+f.name)]
 check(cid+':sealed-case-bytes',len(matches)==1 and all(binding(f.read_bytes())[k]==matches[0][k] for k in ('bytes','sha256','crc32')))
 check(cid+':initial-hash',sha(canon(c['initial']))==c['initialSHA256']); check(cid+':final-hash',sha(canon(c['final']))==c['finalSHA256'])
 state=copy.deepcopy(c['initial']); lasttime=-math.inf; events=[]
 for i,e in enumerate(c['events']):
  pre=cid+':event:'+str(i); check(pre+':chain',state==e['before']);check(pre+':before-hash',sha(canon(e['before']))==e['beforeSHA256']);check(pre+':after-hash',sha(canon(e['after']))==e['afterSHA256'])
  check(pre+':time-order',e['time']>=lasttime);lasttime=e['time']
  state=replay(state,e['forward']);check(pre+':forward',state==e['after']);check(pre+':inverse',replay(copy.deepcopy(state),e['inverse'])==e['before'])
  forwardtotal+=len(e['forward']);inversetotal+=len(e['inverse']);eventtotal+=1
  if e['kind'] in ('START','END'):clockmarkers+=1
  events.append({'index':i,'id':e['id'],'time':e['time'],'kind':e['kind'],'source':e['source'],'narrative':e['narrative'],'beforeSHA256':e['beforeSHA256'],'afterSHA256':e['afterSHA256'],'forwardOperationCount':len(e['forward']),'inverseOperationCount':len(e['inverse'])})
 check(cid+':final-chain',state==c['final'])
 for e in reversed(c['events']):state=replay(state,e['inverse'])
 check(cid+':full-reverse',state==c['initial'])
 final=c['final']; clocks=[]
 for aid,a in final['actors'].items():
  sched=a.get('regularSchedule')
  if not sched:continue
  start,period,offset=sched['firstStart'],sched['period'],sched['endOffset'];t=final['time']
  starts=[];ends=[];n=0
  while start+n*period<=t+1e-8:
   st=start+n*period;starts.append(st)
   if st+offset<=t+1e-8:ends.append(st+offset)
   n+=1
  check(cid+':scheduled-starts:'+aid,sched['starts']==starts,{'actual':sched['starts'],'expected':starts})
  check(cid+':scheduled-ends:'+aid,sched['ends']==ends,{'actual':sched['ends'],'expected':ends})
  check(cid+':next-start:'+aid,abs(sched['nextStart']-(start+n*period))<1e-8)
  check(cid+':next-end:'+aid,abs(sched['nextEnd']-(start+len(ends)*period+offset))<1e-8)
  clocks.append({'actorId':aid,'starts':sched['starts'],'ends':sched['ends'],'nextStart':sched['nextStart'],'nextEnd':sched['nextEnd'],'budgetHistory':sched['budgetHistory'],'recharge':a.get('recharge'),'action':a.get('action'),'bonusAction':a.get('bonusAction'),'reaction':a.get('reaction'),'movement':a.get('movement'),'RP':a.get('RP'),'Dissonance':a.get('Dissonance'),'magicThisTurn':a.get('magicThisTurn'),'resourceHistory':a.get('resourceHistory'),'spellHistory':a.get('spellHistory'),'concentration':a.get('concentration')})
 case_reports.append({'id':cid,'statusPreserved':c['status'],'eventCount':len(events),'forwardOperationCount':sum(x['forwardOperationCount'] for x in events),'inverseOperationCount':sum(x['inverseOperationCount'] for x in events),'replay':'PASS','wholeRequiredCaseComplete':False,'initialSHA256':c['initialSHA256'],'finalSHA256':c['finalSHA256'],'events':events,'finalActorClocksAndResources':clocks,'qualification':'Exact authored states replayed; numeric success does not establish missing positive branch premises, acquisition or campaign facts.'})
for f in (S/'prior/procedures').glob('*.json'):
 matches=[m for m in rows.values() if m['path'].endswith('/'+f.name)];check('prior-procedure-seal',len(matches)==1 and sha(f.read_bytes())==matches[0]['sha256'])
idx=read(S/'authority/authored_review_index_selected.json');cat=read(S/'authority/catalog_selected.json');live=read(R.parent/'faction_omniscience_return326/source/authority/current/authored_review_index.json')
livebytes=(R.parent/'faction_omniscience_return326/source/authority/current/authored_review_index.json').read_bytes();check('full-live-index-sha',sha(livebytes)==zm['inputBindings']['authoredReviewIndexSha256'])
liveentries=live.get('spells',live.get('entries',[]))
for row in idx['entries']:check('current-index-row:'+row['id'],row==next(x for x in liveentries if x['id']==row['id']))
with zipfile.ZipFile(R.parent/'upload/DD_Rank9_TimeFate6_CurrentSource_282.zip') as z:
 b=z.read('sources_current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'); check('full-catalog-current-sha',sha(b)==zm['inputBindings']['catalogSha256']); fullcat=json.loads(b)
 for row in cat['spells']:check('current-catalog-row:'+row['id'],row==next(x for x in fullcat['spells'] if x['id']==row['id']))
 corepaths=[x for x in z.namelist() if x.endswith('/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')]
 corebinding=[]
 for name in corepaths:
  b=z.read(name);corebinding.append({'externalArchive':'DD_Rank9_TimeFate6_CurrentSource_282.zip','member':name,**binding(b),'matchesPacket327CurrentHash':sha(b)==zm['inputBindings']['coreSourceSha256']})
champ=next(x for x in idx['entries'] if x['id']=='faction-champion');norm=[]
for fn,key in [('AC5_REVIEWED_SPELLS.json','completeEnvelopeBinding'),('AC5_EXACT_ACCEPTANCE_05_RECEIPT.json','authoredAcceptanceReceipt')]:
 b=(S/'current_sources'/fn).read_bytes();lf=b.replace(b'\r\n',b'\n');expected=champ[key]
 check('AC5-LF-index-bound:'+fn,len(lf)==expected['bytes'] and sha(lf)==expected['sha256']);check('AC5-normalization-structural:'+fn,json.loads(b)==json.loads(lf))
 out=P/'evidence/index-bound'/fn;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(lf)
 norm.append({'input':'evidence/packet327/current_sources/'+fn,'inputBinding':binding(b),'operation':'CRLF -> LF only; originals preserved','output':str(out.relative_to(P)),'outputBinding':binding(lf),'indexedBinding':expected,'result':'EXACT_INDEX_BOUND'})
receipt=read(S/'current_sources/AC5_EXACT_ACCEPTANCE_05_RECEIPT.json');check('AC5-acceptance-applied',receipt['status']=='exact-authored-acceptance-applied' and 'faction-champion' in receipt['acceptedSpellIds'])
model=read(S/'current_sources/AC5_REVIEWED_SPELLS.json');check('AC5-profile-source-preserved',model['spells'][14]['id']=='faction-champion' and 'AC5-PROFILE-FACTION-CHAMPION-01' in model['profiles'])
prior326=read(S/'prior/Return326_HELD_DELIVERY.json');ba=(S/'prior/Return326_HELD.zip').read_bytes();expected326=prior326['archive'];check('Return326-archive-binding',all(binding(ba)[k]==expected326[k] for k in ('bytes','sha256','crc32')))
with zipfile.ZipFile(S/'prior/Return326_HELD.zip') as z:
 check('Return326-crc',z.testzip() is None)
 for m in prior326['members']:check('Return326-member:'+m['path'],all(binding(z.read(m['path']))[k]==m[k] for k in ('bytes','sha256','crc32')))
pending=read(S/'authority/CURRENT25_PENDING_IDENTITY_AUDIT_327.json');queue=read(S/'authority/CURRENT_SPELL_QUEUE_327.json');check('pending25',len(pending['pendingIds'])==25 and len(set(pending['pendingIds']))==25 and 'banishment-gate' in pending['pendingIds'])
check('queue-exact25',set(queue['continuingPriorityOrder']+queue['separatelyRetainedHolds'])==set(pending['pendingIds']))
counts={'preservedCases':len(case_reports),'mainCases':2,'branches':7,'events':eventtotal,'forwardOperations':forwardtotal,'inverseOperations':inversetotal,'fullReverseTraversals':len(case_reports),'regularClockMarkers':clockmarkers,'wholeRequiredMainCasesComplete':0,'ruleOnlyBranchRecords':7,'ac5AcceptedExampleRecords':5,'ac5ExamplesWithNewFullStateReplay':0,'targetQuestionDispositions':10,'targetFutureObligations':5}
write(P/'REPLAY_RESULTS.json',{'id':'PG327-REPLAY','status':'PASS' if all(x['pass'] for x in checks if ':event:' in x['id']) else 'FAIL','counts':counts,'stateHashSerialization':prior['stateHashSerialization'],'cases':case_reports})
write(P/'SOURCE_BINDINGS.json',{'packet':binding(zb,zpath.name),'packetManifest':'evidence/packet327/MANIFEST.json','AC5Normalization':norm,'currentIndexVerified':binding(livebytes),'currentCatalogVerifiedSha256':zm['inputBindings']['catalogSha256'],'coreSourceExternalCheck':corebinding,'scope':'Exact packet payloads, current selected index/catalog rows and accepted AC5 envelope/receipt verified. Case embedded profile hash references are preserved; not a new full acquisition audit of absent class-source files. Historical metadata is not current authority.'})
report={'id':'PG327-DATA-INTEGRITY','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checkCount':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'counts':counts,'checks':checks}
write(P/'DATA_INTEGRITY_CHECK.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2));print('FAILURES',json.dumps([x for x in checks if not x['pass']],indent=2))
