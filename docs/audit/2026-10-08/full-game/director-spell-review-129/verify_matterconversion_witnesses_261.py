import copy,json,zipfile,hashlib,zlib
from pathlib import Path
from fractions import Fraction
B=Path(__file__).resolve().parent; O=B/'matter_conversion_witnesses_261'; checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def H(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def crc(b):return f'{zlib.crc32(b)&0xffffffff:08x}'
def ck(name,cond,detail=None):checks.append({'check':name,'passed':bool(cond),'detail':detail})
def apply_ops(state,ops):
 cur=copy.deepcopy(state)
 for op in ops:
  assert op['path']==''
  if op['op']=='test': assert cur==op['value']
  elif op['op']=='replace':cur=copy.deepcopy(op['value'])
  else:raise AssertionError(op)
 return cur
# Packet260 corrected manifest independently verifies its request member.
p260=B/'DD_Rank9_MatterConversion_MF210-B02_Supplement_260.zip'
with zipfile.ZipFile(p260) as z:
 man=json.loads(z.read('MANIFEST.json')); names=z.namelist()
 req=z.read('REQUEST.txt')
 ck('Packet260 archive contains 28 members including manifest',len(names)==28,len(names))
 ck('Packet260 manifest binds 27 non-self members',man.get('memberCountExcludingSelf')==27 and len(man['members'])==27,len(man['members']))
 reqm=next((m for m in man['members'] if m['path']=='REQUEST.txt'),None)
 ck('REQUEST.txt is listed with GPT-verified SHA-256',reqm is not None and reqm['sha256']==sha(req)=='c460c42d1f3ce15299938ee946bc68df4af944fd6b02b31c2c034968268d7a6f',None if reqm is None else reqm['sha256'])
 for m in man['members']:
  data=z.read(m['path']);ck('Packet260 member '+m['path'],len(data)==m['bytes'] and sha(data)==m['sha256'] and crc(data)==m['crc32'],{'bytes':len(data),'sha256':sha(data)})
# Prior Return247 archive binding and conditional-kernel reversibility.
ret=B/'rank9_materialforging2_return247_received/DD_Rank9_MaterialForging2_Director_Return247_HELD.zip';rb=ret.read_bytes()
rec=json.loads((B/'RANK9MATERIALFORGING2_RETURN247_INDEPENDENT_AUDIT.json').read_text(encoding='utf-8'))
ck('Return247 archive hash matches prior independent audit',sha(rb)==rec['archive']['sha256'] and len(rb)==rec['archive']['bytes'] and crc(rb)==rec['archive']['crc32'],{'bytes':len(rb),'sha256':sha(rb),'crc32':crc(rb)})
with zipfile.ZipFile(ret) as z:
 replay=json.loads(z.read('CASE_REPLAY.json')); kernels=[x for x in replay['cases'] if x['id'].startswith('MF210-M-')]
 ck('Seven Matter Conversion conditional kernels preserved',len(kernels)==7,[x['id'] for x in kernels])
 fwd=inv=0; kernel_fail=[]
 for meta in kernels:
  e=json.loads(z.read(meta['file']))['events'][0]
  ok=e['beforeSHA256']==H(e['before']) and e['afterSHA256']==H(e['after'])
  try:ok=ok and apply_ops(e['before'],e['forward'])==e['after'] and apply_ops(e['after'],e['inverse'])==e['before']
  except Exception:ok=False
  if not ok:kernel_fail.append(meta['id'])
  fwd+=len(e['forward']);inv+=len(e['inverse'])
 ck('Preserved kernels forward/inverse state hashes and operations pass',not kernel_fail and fwd==14 and inv==14,{'failed':kernel_fail,'forward':fwd,'inverse':inv})
# Verify each new full-state event chain and exact reversible root operations.
cases=[]
for cid,fn in [('MF259-M-W1','MF259-M-W1.json'),('MF259-M-W2','MF259-M-W2.json')]:
 c=json.loads((O/fn).read_text(encoding='utf-8'));cases.append(c);events=c['events'];errors=[];forward=reverse=0
 if len(events)!=15:errors.append('event-count')
 if c['initialState']!=events[0]['before'] or c['finalState']!=events[-1]['after']:errors.append('endpoint-binding')
 for i,e in enumerate(events):
  if e['beforeSHA256']!=H(e['before']) or e['afterSHA256']!=H(e['after']):errors.append(f'hash-{i}')
  if i and events[i-1]['after']!=e['before']:errors.append(f'continuity-{i}')
  try:
   if apply_ops(e['before'],e['forward'])!=e['after']:errors.append(f'forward-{i}')
   if apply_ops(e['after'],e['inverse'])!=e['before']:errors.append(f'inverse-{i}')
  except Exception:errors.append(f'patch-{i}')
  forward+=len(e['forward']);reverse+=len(e['inverse'])
  if e['after']['time']!=e['time'] or e['before']['time']>e['time']:errors.append(f'clock-{i}')
 ck(cid+' full-state hashes, continuity, forward and inverse replay',not errors,{'events':len(events),'forward':forward,'inverse':reverse,'errors':errors})
 ck(cid+' reports exactly 30 forward and 30 inverse ops',forward==30 and reverse==30,{'forward':forward,'inverse':reverse})
 st=c['finalState'];a=st['actors']['A'];b=st['actors']['B']
 ck(cid+' independent complete Wizard17 actors and legal learned/prepared focus route',a['id']=='A' and b['id']=='B' and a['id']!=b['id'] and a['profile']['class']=='Wizard' and b['profile']['class']=='Wizard' and a['profile']['classLevel']==17 and b['profile']['classLevel']==17 and 'matter-conversion' in a['profile']['learned'] and 'matter-conversion' in a['profile']['prepared'] and any(i.get('id')=='focus' for i in a['profile']['inventory']),True)
 ck(cid+' all scheduled starts and due ends processed',st['boundaryAudit']['processedStarts']=={'A':[0,6,12],'B':[1,7,13]} and st['boundaryAudit']['processedEnds']=={'A':[6,12],'B':[7,13]},st['boundaryAudit'])
 ck(cid+' spell cost and chronology preserve one 26-RP Action from 64 to 38',a['RP']==38 and a['resourceHistory']==[{'castId':('castMC259-W1' if cid.endswith('W1') else 'castMC259-W2'),'spell':'matter-conversion','time':(.1 if cid.endswith('W1') else 6.1),'cost':26,'action':'Action','firstFamily':True,'baseDissonance':0,'RefrainAdded':0,'componentMode':'arcane focus','focusId':'focus'}] and a['Dissonance']==0 and a['Refrain']==0,{'RP':a['RP'],'resourceHistory':a['resourceHistory'],'Dissonance':a['Dissonance'],'Refrain':a['Refrain']})
 ck(cid+' resolved terminal cast remains instantaneous ordinary matter',len(st['terminalCasts'])==1 and next(iter(st['terminalCasts'].values()))['status']=='resolved' and next(iter(st['terminalCasts'].values()))['ongoingEffect'] is None and next(iter(st['terminalCasts'].values()))['ordinaryPersistentMatter'],st['terminalCasts'])
# W1 semantics, material/economic conservation, custody and no repeat sale.
w1=cases[0];f=w1['finalState'];stone=f['items']['MC259-STONE-LOT-1'];mith=f['items']['MC259-MITHRIL-1'];eco=f['economy']
ck('W1 exact 1 lb stone→1 lb mithril mass, density, and geometry conserved',stone['massRationalLb']=='0/1' and mith['massRationalLb']=='1/1' and mith['geometryVolumeIn3']=='8/1' and mith['densityLbPerIn3']=='1/8' and f['conservationLedger']['massEquality']=='1/1 = 1/1 + 0/1 + 0/1' and mith['geometryInches']==[2,2,2],f['conservationLedger'])
ck('W1 station support, clearance, consent and range are within authorized fixture',f['scene']['station']['supportLimitLb']==100 and f['scene']['station']['clearanceInches']==6 and f['scene']['station']['BPermitsConversionAndAContinuedCustody'] and f['scene']['target']['rangeFeet']==5 and f['scene']['target']['within120Feet'],f['scene'])
ck('W1 finite one-use 250 gp quote settles before expiry',eco['quotes']['MC259-QUOTE-1']['settlementCount']==1 and eco['quotes']['MC259-QUOTE-1']['settledAtSeconds']<eco['quotes']['MC259-QUOTE-1']['validThroughSeconds'] and len(eco['transactions'])==1 and eco['transactions'][0]['amountGp']==250,eco)
ck('W1 coin reserve 300→50 and 250 payment remain 300 total in specified locations',eco['reserves']['MC259-GOLD-RESERVE-B']['valueGp']==50 and eco['coinLots']['MC259-PAYMENT-A-250GP']['valueGp']==250 and eco['coinLots']['MC259-PAYMENT-A-250GP']['location']=='MC259-TRAY-A' and eco['coinLots']['MC259-PAYMENT-A-250GP']['custodian']=='B' and eco['totalFixtureGoldPiecesAfter']==eco['totalFixtureGoldPiecesOpening']==300 and eco['profileCarriedGoldPiecesAfter']==eco['profileCarriedGoldPiecesOpening']==118 and eco['totalCoinPiecesAfter']==418,{'reserve':50,'payment':250,'total':eco['totalCoinPiecesAfter']})
ck('W1 output ownership passes to B; A payment not added to carried inventory',mith['owner']=='B' and mith['custodian']=='B-on-MC259-STATION-1' and 'MC259-PAYMENT-A-250GP' in f['items']['MC259-TRAY-A']['contents'] and f['items']['MC259-TRAY-A']['custodian']=='B',{'owner':mith['owner'],'custodian':mith['custodian'],'tray':f['items']['MC259-TRAY-A']})
ck('W1 repeat sale rejected without second action or payment',len(eco['settlementAttempts'])==1 and eco['settlementAttempts'][0]['result']=='rejected-already-settled' and eco['settlementAttempts'][0]['additionalPaymentGp']==0 and eco['settlementAttempts'][0]['additionalActionSpend'] is False,eco['settlementAttempts'])
# W2 rejection, release, conversion, support, damage and persistence.
w2=cases[1];f=w2['finalState'];panel=f['items']['MC259-PANEL-2'];glass=f['items']['MC259-GLASS-1'];attempt=f['preflightAttempts'][0]
ck('W2 reserved preflight rejects before payment with no expenditure',attempt['paidRP']==0 and attempt['ActionSpent'] is False and attempt['castingHistoryChanged'] is False and w2['events'][0]['before']['actors']['A']['RP']==w2['events'][0]['after']['actors']['A']['RP']==64 and w2['events'][0]['before']['actors']['A']['Action']==w2['events'][0]['after']['actors']['A']['Action']==1,attempt)
release_event=next(e for e in w2['events'] if e['id']=='W2:RESERVATION:RELEASE')
ck('W2 B releases reservation on its lawful first turn; revision advances and Action is recorded',release_event['before']['actors']['B']['regularStart']==1 and release_event['before']['actors']['B']['Action']==1 and release_event['after']['actors']['B']['Action']==0 and release_event['after']['items']['MC259-PANEL-2']['revision']==2 and release_event['after']['items']['MC259-PANEL-2']['reservationId'] is None,release_event['detail'])
commit_event=next(e for e in w2['events'] if e['id']=='W2:CAST:COMMIT')
ck('W2 new declaration uses post-release revision and exact ceramic allocation',commit_event['after']['pendingCasts']['castMC259-W2']['authorizationFrozen']['targetRevision']==2 and commit_event['after']['pendingCasts']['castMC259-W2']['authorizationFrozen']['inputAllocationId']=='MC259-CERAMIC-LOT-2',commit_event['after']['pendingCasts'])
ck('W2 143/32 lb material and 143/4 in3 remain exact with equal 1/8 density',glass['massRationalLb']=='143/32' and glass['geometryVolumeIn3']=='143/4' and glass['densityLbPerIn3']=='1/8' and f['conservationLedger']['massEquality']=='143/32 = 143/32 + 0/1 + 0/1',f['conservationLedger'])
ck('W2 physical body, ownership/custody, missing corner and four-point damage deficit persist',panel['id']=='MC259-PANEL-2' and panel['materialAllocationId']=='MC259-GLASS-1' and panel['owner']=='A' and panel['custodian']=='B' and panel['HP']==4 and panel['maxHP']==8 and panel['damageDeficit']==4 and panel['viewingResult']['notchRemainsOpen'] and panel['viewingResult']['visibleThroughIntactGlass'],panel)
ck('W2 authorized 20 lb support exceeds 143/32 lb panel; no unsupported structural claims',f['items']['MC259-FRAME-2']['staticPanelLoadLimitLb']==20 and Fraction(str(glass['massLb']))<20 and f['items']['MC259-FRAME-2']['pressureRated'] is False and f['items']['MC259-FRAME-2']['fluidSeal'] is False and f['items']['MC259-FRAME-2']['structuralBuildingFunction'] is False,{'loadLimitLb':20,'panelMassLb':glass['massLb']})
ck('W2 reservation cleared; no repair, sale, self-repair, magnification or special resistance',f['reservations']['MC259-RESERVATION-2']['status']=='cleared-after-conversion' and panel['HP']==4 and f['economy']['saleOrBuyer'] is None and glass['selfRepair'] is False and glass['opticalMagnification'] is False and glass['specialResistance'] is False,None)
ck('W2 ordinary output persists after A casting turn ends at t=12',f['time']==13.1 and f['persistenceObservations'][-1]['afterCasterTurnEnd']==12 and panel['ordinaryPersistentMatter'] and panel['ongoingSpellEffect'] is None,None)
# Scope and counts.
auth=json.loads((B/'MATTER_CONVERSION_DIRECTOR_FIXTURE_AUTHORIZATION_260.json').read_text(encoding='utf-8'))
ck('GPT authorization remains HOLD with fixture-only scope and no acceptance/application',auth['decision']=='HOLD' and auth['accepted'] is False and auth['applied'] is False and auth['authorizedNewScopedGameData'] is True,{'decision':auth['decision'],'accepted':auth['accepted'],'applied':auth['applied']})
fail=[x for x in checks if not x['passed']]
audit={'id':'MATTER-CONVERSION-MF210-B02-INDEPENDENT-AUDIT-261','checkedAtUtc':'2026-10-30T13:54:14Z','status':'PASS' if not fail else 'FAIL','authority':auth['authority'],'targetIds':['matter-conversion'],'blockerIds':['MF210-B02'],'acceptedIds':[],'appliedIds':[],'heldIds':['matter-conversion'],'caseIds':[c['id'] for c in cases],'checks':checks,'checkCount':len(checks),'passedChecks':sum(x['passed'] for x in checks),'failedChecks':len(fail),'failures':fail,'counts':{'newIntegratedCases':2,'newEvents':sum(len(c['events']) for c in cases),'newForwardOperations':sum(c['forwardOperations'] for c in cases),'newInverseOperations':sum(c['inverseOperations'] for c in cases),'preservedConditionalMatterKernels':7,'preservedKernelForwardOperations':14,'preservedKernelInverseOperations':14},'canonicalChanges':False,'githubChanges':False,'qualification':'Static authored fixtures and state replay only; no runtime, implementation, human-play, balance, cosmology, domain-closure, completion or release approval.'}
(O/'MATTER_CONVERSION_INDEPENDENT_AUDIT_261.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':audit['status'],'checks':audit['checkCount'],'passed':audit['passedChecks'],'failed':audit['failedChecks'],'counts':audit['counts'],'failures':fail},indent=2))
if fail:raise SystemExit(1)
