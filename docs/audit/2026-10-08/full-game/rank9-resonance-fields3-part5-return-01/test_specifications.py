#!/usr/bin/env python3
"""Independent finite numerical/state specifications, not game-engine integration.
No supplied project module is imported. Real source/perception/action predicates are
explicit inputs; these helpers do not establish production scheduler reachability.
"""
from pathlib import Path
from fractions import Fraction
import argparse, copy, json, math

ROOT=Path(__file__).resolve().parent
REPORT=[]
def check(name,inputs,actual,expected,scope='isolated numerical/state specification'):
 passed=actual==expected
 REPORT.append({'id':name,'scope':scope,'inputs':inputs,'actual':actual,'expected':expected,'passed':passed})
 if not passed:raise AssertionError(f'{name}: {actual!r} != {expected!r}')
def scale(parts,f=False,n=False):
 factor=Fraction(3,2) if f else Fraction(1)
 if n:factor*=Fraction(5,4)
 total=sum(parts.values());desired=int(total*factor)
 if total==0:return {k:0 for k in parts}
 quotas={k:Fraction(v*desired,total) for k,v in parts.items()}
 result={k:int(v) for k,v in quotas.items()}
 for k in sorted(quotas,key=lambda k:(-(quotas[k]-int(quotas[k])),k))[:desired-sum(result.values())]:result[k]+=1
 return result

def price(base,extras=0,principal=0,nexus=False,supreme=False,damp=False,influence=0):
 b,e=base,extras
 def deduct(x,y,n):
  bx=max(0,x-n);left=max(0,n-x);return bx,max(0,y-left)
 if nexus:b,e=deduct(b,e,2)
 if supreme:b,e=deduct(b,e,math.ceil((b+e)/2))
 d=2 if damp else 0;burden=max(0,influence)
 if influence<0:
  n=-influence;old=b+e;b,e=deduct(b,e,n);d=max(0,d-max(0,n-old))
 return {'base':b,'extra':e,'dampening':d,'burden':burden,'protectedPrincipal':principal,'total':b+e+d+burden+principal}

def convert(base,refund=0,explicit_unpriced=False,prohibited=False):
 if prohibited:return 0
 if explicit_unpriced:return 1
 if base is None:raise ValueError('Actual paid-base provenance is unknown, not intrinsic zero')
 if base==0:return 1
 net=max(0,base-refund)
 return 0 if net==0 else max(1,net//2)

def settle(ledger,origin,base,refund=0,explicit_unpriced=False,prohibited=False,living=True):
 if origin in ledger['receipts']:return {'repeat':True,'credit':0}
 value=convert(base,refund,explicit_unpriced,prohibited)
 credit=min(value,ledger['maximum']-ledger['rp']) if living else 0
 receipt={'value':value,'credit':credit,'lost':value-credit,'spent':True}
 ledger['receipts'][origin]=receipt;ledger['rp']+=credit
 return receipt

def body_intersects(foot,center,r):
 d=0
 for i in [0,1]:d+=max(0,abs(foot[i]-center[i])-2.5)**2
 d+=max(0,foot[2]-center[2],center[2]-(foot[2]+6))**2
 return d<r*r

def readiness(now,deadline,reaction=True,concentration=True,trigger=True,target=True):
 return now<deadline and all([reaction,concentration,trigger,target])

def case_get():
 data=json.loads((ROOT/'CASE_DISPOSITIONS.json').read_text());m={}
 for c in data['cases']:
  m[c['id']]=c
  for b in c['independentBranches']:m[b['id']]=b
 return m

def run():
 # Independent arithmetic, including correct single rational stage and typed remainder.
 vectors=[({'fire':29},True,False,{'fire':43}),({'fire':29},False,True,{'fire':36}),({'fire':21},True,True,{'fire':39}),({'fire':7},True,True,{'fire':13}),({'cold':9,'lightning':7},True,False,{'cold':14,'lightning':10}),({'cold':1,'fire':1},True,True,{'cold':2,'fire':1}),({'fire':0},True,True,{'fire':0}),({'cold':13},True,False,{'cold':19}),({'cold':11},True,False,{'cold':16}),({'force':18},False,True,{'force':22}),({'cold':5},True,False,{'cold':7})]
 for i,(p,f,n,e) in enumerate(vectors):check('MAGNITUDE-'+str(i),{'parts':p,'Furnace':f,'Supreme':n},scale(p,f,n),e)
 check('DEFENSE-FIRE-WARD',{'raw29':'Furnace then successful save and resistance'},(43//2)//2,10)
 check('DEFENSE-MIXED',{'amplifiedCold':14,'amplifiedLightning':10,'lightningResistance':True},14+10//2,19)
 check('FINISHER',{'native5':'Furnace then successfulCON'},int(Fraction(5)*Fraction(3,2))//2,3)
 check('BARRIER-POOL',{'actualPaidBase':2,'protectedX':2},int(Fraction(5*(2+2))*Fraction(5,4)),25)
 check('FAMILIAR',{'native5+17+4':26},int(Fraction(26)*Fraction(5,4)),32)
 for label,args,expect in [
  ('HALF26',{'base':26,'supreme':True},{'base':13,'extra':0,'dampening':0,'burden':0,'protectedPrincipal':0,'total':13}),
  ('HALF5',{'base':5,'supreme':True},{'base':2,'extra':0,'dampening':0,'burden':0,'protectedPrincipal':0,'total':2}),
  ('HALF1',{'base':1,'supreme':True},{'base':0,'extra':0,'dampening':0,'burden':0,'protectedPrincipal':0,'total':0}),
  ('PRINCIPAL',{'base':10,'extras':1,'principal':2,'nexus':True,'supreme':True,'damp':True,'influence':-1},{'base':2,'extra':1,'dampening':2,'burden':0,'protectedPrincipal':2,'total':7}),
  ('DAMP-LAST',{'base':1,'supreme':True,'damp':True},{'base':0,'extra':0,'dampening':2,'burden':0,'protectedPrincipal':0,'total':2}),
  ('INFLUENCE-EXHAUSTS-EXTRAS',{'base':0,'extras':1,'principal':4,'damp':True,'influence':-2},{'base':0,'extra':0,'dampening':1,'burden':0,'protectedPrincipal':4,'total':5}),
  ('BURDEN-LAST',{'base':5,'supreme':True,'influence':1},{'base':2,'extra':0,'dampening':0,'burden':1,'protectedPrincipal':0,'total':3}),
  ('OWN-RECAST',{'base':25},{'base':25,'extra':0,'dampening':0,'burden':0,'protectedPrincipal':0,'total':25}),
  ('NON-SPELL-FEE',{'base':1,'supreme':True},{'base':0,'extra':0,'dampening':0,'burden':0,'protectedPrincipal':0,'total':0})]:check('PRICE-'+label,args,price(**args),expect)
 for base,refund,value in [(26,0,13),(13,0,6),(5,0,2),(3,0,1),(2,0,1),(1,0,1),(0,0,1),(2,2,0),(5,3,1),(5,1,2),(5,9,0)]:check('CONVERT-'+str(base)+'-'+str(refund),{'actualBase':base,'actualBaseRefund':refund},convert(base,refund),value)
 check('CONVERT-INTRINSIC',{'explicitUnpricedActualMagic':True},convert(None,explicit_unpriced=True),1)
 check('CONVERT-SOURCE-PROHIBITED',{'sourceNoRPBody':True},convert(None,explicit_unpriced=True,prohibited=True),0)
 try:convert(None);unknown=False
 except ValueError:unknown=True
 check('CONVERT-UNKNOWN-IS-NOT-ZERO',{'missingPaidProvenance':True},unknown,True)
 l={'rp':63,'maximum':64,'receipts':{}}
 check('LEDGER-FIRST',{'initial':copy.deepcopy(l),'origin':'castA'},settle(l,'castA',5),{'value':2,'credit':1,'lost':1,'spent':True})
 snap=copy.deepcopy(l);check('LEDGER-DUPLICATE',{'origin':'castA'},settle(l,'castA',5),{'repeat':True,'credit':0});check('LEDGER-DUPLICATE-STATE',{},l,snap)
 l['rp']=60;check('LEDGER-NO-OVERFLOW-BANK',{'laterMissingRP':4},settle(l,'castA',5),{'repeat':True,'credit':0});check('LEDGER-NO-RECLAIM',{},l['rp'],60)
 check('LEDGER-NEW-REAL-ACTIVATION',{'origin':'castB'},settle(l,'castB',5),{'value':2,'credit':2,'lost':0,'spent':True})
 check('LEDGER-DEAD-OWNER',{},settle(l,'castC',2,living=False),{'value':1,'credit':0,'lost':1,'spent':True})
 check('LEDGER-REFUND-ZERO-NOT-INTRINSIC',{},settle(l,'castD',2,refund=2),{'value':0,'credit':0,'lost':0,'spent':True})
 for label,foot,center,r,expected in [('FURNACE25',[25,0,0],[0,0,3],30,True),('FURNACE41',[41,0,0],[0,0,3],30,False),('SING40',[40,0,0],[30,0,3],10,True),('SING55',[55,0,0],[30,0,3],10,False),('TANGENCY',[42.5,0,0],[30,0,3],10,False),('PARTIALINTERIOR',[42.49,0,0],[30,0,3],10,True),('SUPREMEPOSTBLINK',[45,10,0],[0,0,3],30,False)]:check('GEOMETRY-'+label,{'foot':foot,'center':center,'r':r},body_intersects(foot,center,r),expected)
 check('FIREBALL-LITERAL-RANGE',{'origin':[25,0,3],'center':[45,0,3],'range':20},math.dist([25,0,3],[45,0,3])<=20,True)
 check('FIREBALL-NO-DEFAULT150',{'distance':21,'actualRange':20},21<=20,False)
 check('BLINK-USEFUL-ENHANCEMENT',{'distanceSquared':1325,'native':30,'enhanced':37.5},30<math.sqrt(1325)<37.5,True)
 corners=[[38.5+x,y,z] for x in [-2.5,2.5] for y in [-2.5,2.5] for z in [0,6]]
 check('AM-FULL-RECIPIENT',{'center':[45,0,3],'radius':10,'bodyFoot':[38.5,0,0]},max(sum((p[i]-[45,0,3][i])**2 for i in range(3)) for p in corners),96.25)
 for time,result in [(6.9,True),(7,False),(7.1,False)]:check('READY-DEADLINE-'+str(time),{'now':time,'actualNextSTART':7},readiness(time,7),result)
 for flag in ['reaction','concentration','trigger','target']:
  kwargs={flag:False};check('READY-'+flag.upper(),kwargs,readiness(2.2,7,**kwargs),False)
 check('FIELD-DEADLINE-EQUALITY',{'established':0.1,'duration':60,'event':60.1},60.1<(0.1+60),False)
 check('CLASS-CONCENTRATION',{'faces':[12,8],'CON':2,'damage':22},max(12,8)+2>=max(10,22//2),True)
 check('GREATER-DISPEL',{'rank':9,'INT':4,'PB':6,'die':18},18+4+6>=10+2*9,True)
 check('INTEGRITY-OPPONENT-CHECK',{'nativeCheckDC':18,'oneSupreme':True},18+2,20)
 # Independent expected final-state values in all main cases and meaningful branches.
 c=case_get()
 outcomes={
  'RF9-AF-A':{'F':(104,38,0),'B':(104,59,0),'E':(61,64,0)},
  'RF9-AF-B':{'F':(104,38,0),'M':(104,42,2),'E':(47,64,0)},
  'RF9-RS-A':{'S':(104,41,0),'V':(104,64,0),'P':(76,64,0)},
  'RF9-RS-B':{'S':(104,41,0),'W':(104,60,2)},
  'RF9-NS-A':{'N':(82,38,0),'B':(95,62,0),'E':(68,64,0)},
  'RF9-NS-B':{'N':(104,38,0),'M':(104,49,2),'W':(104,62,0)},
  'RF9-COMBINED':{'N':(104,38,0),'F':(104,51,0),'S':(104,64,0),'B':(104,62,0),'P':(65,64,0),'E':(104,64,0),'T':(104,38,0)},
  'RF9-AF-A-save':{'E':(83,64,0)},'RF9-AF-A-ward':{'E':(83,64,0)},
  'RF9-AF-A-ready-out':{'B':(104,59,0),'E':(75,64,0)},'RF9-AF-A-ready-in':{'E':(61,64,0)},
  'RF9-AF-B-existing-cloud':{'Q':(92,43,0),'E':(34,64,0),'F':(104,38,0)},
  'RF9-AF-B-nonspell':{'M':(104,46,1),'E':(50,64,0)},
  'RF9-RS-A-zero':{'S':(104,40,0),'V':(104,64,0)},
  'RF9-RS-A-efficient':{'S':(104,40,0),'E':(104,64,0)},
  'RF9-RS-A-cap':{'S':(104,64,0)},
  'RF9-RS-B-dispel':{'S':(104,40,0),'D':(104,54,0)},
  'RF9-RS-B-true-suppression':{'S':(104,40,0),'V':(104,64,0),'E':(104,62,2),'A':(104,54,0)},
  'RF9-NS-A-own-recast':{'N':(104,13,3)},
  'RF9-NS-A-overlap':{'B':(104,51,0),'E':(104,62,0)},
  'RF9-NS-A-counter':{'N':(104,38,0),'E':(104,62,0)},
  'RF9-NS-A-prep-in-release-out':{'B':(104,62,0),'E':(75,64,0)},
  'RF9-NS-A-prep-out-release-in':{'B':(104,59,0),'E':(68,64,0)},
  'RF9-NS-A-protected-price':{'B':(104,52,13)},
  'RF9-NS-B-counterpulse':{'B':(104,64,0),'E':(104,59,0)},
  'RF9-NS-B-familiar':{'M':(104,48,1)},
  'RF9-COMBINED-consume-generators':{'S':(104,64,0),'N':(104,38,0),'F':(104,51,0)},
  'RF9-COMBINED-replay':{'S':(104,64,0),'P':(65,64,0)}
 }
 for cid,actors in outcomes.items():
  actual={a:tuple(c[cid]['finalState']['actors'][a][k] for k in ['hp','rp','D']) for a in actors}
  check('CASE-'+cid,{'expectedAt':'complete case final state','fields':['HP','RP','D']},actual,actors,'authored fixture numerical/state comparison, not engine execution')
 am=c['RF9-RS-B-true-suppression']['finalState'];check('AM-NO-RETROACTIVE-CONVERSION',{},'SuppressedBolt' in am['conversionReceipts'],False)
 check('AM-NEW-ACTIVATION-CONVERTS',{},am['conversionReceipts']['AbsorbedBolt']['credited'],1)
 check('AM-REAL-ENDING',{},(am['fields']['AM']['endedAt'],am['actors']['A']['concentration']),(2,None))
 sight=c['RF9-RS-B'];check('SIGHT-RECHARGE-PRESERVED',{},sight['timeline'][6]['after']['actors']['W']['recharge']['wizard.arch.arcane-sight'],1)
 check('SIGHT-THIRD-TURN-PAID',{},sight['finalState']['castRecords']['Sight2']['paidAt'],13.2)
 check('SIGHT-NO-EARLY-EFFICIENCY',{},sight['finalState']['castRecords']['Sight2']['nativeMatrixEfficiencyUsed'],False)
 nc=c['RF9-NS-A-own-recast']['finalState'];check('OWN-NEXUS-CLASS-EFFICIENCY',{},nc['castRecords']['Nexus2']['nativeMatrixEfficiencyUsed'],True)
 check('OWN-NEXUS-REAL-ENDING',{},(nc['fields']['Nexus1']['endedAt'],nc['fields']['Nexus2']['deadline']),(6.1,66.2))
 cost=c['RF9-NS-A-protected-price']['finalState'];check('PRICE-FULL-BUCKET-RECEIPT',{},cost['castRecords']['Barrier']['quote'],price(10,1,2,True,True,True,-1));check('BARRIER-NO-FALSE-BASE',{},cost['effects']['Barrier']['remainingPool'],25)
 co=c['RF9-COMBINED']['finalState'];check('COMBINED-TARGET-NO-ROOT',{},'Fire:E' in co['damageRootRecords'],False)
 check('COMBINED-TRUE-DEALER',{},co['damageRootRecords']['Fire:P']['dealer'],'B')
 check('COMBINED-PAID-NOT-NOMINAL',{},co['conversionReceipts']['Fire']['basis']['paidBase'],2)
 check('COMBINED-INCOMING-POINT-NOT-INSERTED',{},'NewSing' in co['fields'],False)
 check('COMBINED-CAPPED-POINT-CREDIT',{},(co['conversionReceipts']['NewSing']['credited'],co['conversionReceipts']['NewSing']['overflowOrDenied']),(11,2))
 gen=c['RF9-COMBINED-consume-generators']['finalState'];check('COMPLETE-GENERATOR-CAPTURE',{},[gen['fields'][x]['state'] for x in ['Sup','Fur']],['ended','ended'])
 integ=c['RF9-COMBINED-integrity']['finalState'];check('POSITIVE-INTEGRITY-ACTUAL-CAPTURE',{},sorted(integ['neutralizationReceipts']),['DispelBoth:Fur','DispelBoth:Sup']);check('POSITIVE-INTEGRITY-CHANGES-OUTCOME',{},(integ['neutralizationReceipts']['DispelBoth:Fur']['nativeDC'],integ['neutralizationReceipts']['DispelBoth:Fur']['integrity'],integ['neutralizationReceipts']['DispelBoth:Fur']['total'],integ['neutralizationReceipts']['DispelBoth:Fur']['success']),(28,2,29,False));check('POSITIVE-INTEGRITY-REAL-PRICE',{},integ['actors']['S']['rp'],59)
 for cid in ['RF9-AF-A-ready-out','RF9-AF-A-ready-in','RF9-NS-A-prep-in-release-out','RF9-NS-A-prep-out-release-in']:
  a=c[cid]['finalState']['actors']['B'];check('READY-REAL-REACTION-'+cid,{},(a['action'],a['reaction'],a['concentration'],a['ready']['state']),(False,False,None,'resolved'))
 cloud=c['RF9-AF-B-existing-cloud']['finalState'];check('CLOUD-ORIGINAL-DEADLINE',{},cloud['effects']['Cloud']['deadline'],59.1)
 check('CLOUD-NO-NEW-CAST-PER-PULSE',{},sorted(cloud['castRecords']),['Cloud','Fur'])
 check('FAMILIAR-NO-FREE-RESOURCE',{},c['RF9-NS-B-familiar']['finalState']['effects']['Fam']['RPGenerationAllowed'],False)
 check('NO-NEW-MAIN-HOLDS',{},sum(x['disposition']=='CONDITIONAL_EXTERNAL_PREMISE' for x in json.loads((ROOT/'CASE_DISPOSITIONS.json').read_text())['cases']),0)
 return {'classification':'isolated independent arithmetic, geometry, bounded event/ledger and authored fixture state diagnostics; not actual scheduler/engine/source-provider execution','testCount':len(REPORT),'failures':sum(not x['passed'] for x in REPORT),'tests':REPORT,'gameRuntimeExecuted':False,'humanPlaytests':0,'balanceApproved':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);a=ap.parse_args();r=run()
 if a.report:a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in r.items() if k!='tests'},indent=2))
