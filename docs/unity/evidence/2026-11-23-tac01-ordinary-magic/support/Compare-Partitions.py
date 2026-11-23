"""Compare the complete detached gameplay projection, expanding only zero-idle compression.
Original checksum-validated saves and receipt histories remain untouched. Numeric revision
normalization is restricted to new command provenance; origin admission IDs stay intact.
"""
import copy,json,sys,hashlib
from pathlib import Path
from fractions import Fraction

def qty(v):return Fraction(v['Numerator'],v['Denominator'])
def time(v):return {'Numerator':v.numerator,'Denominator':v.denominator}
def normalize(raw,base):
 s=copy.deepcopy(raw);commands={r['Id'] for r in s['Receipts'] if r['Revision']>base};s.pop('Receipts');s.pop('Revision')
 def provenance(value):
  if isinstance(value,list):return [provenance(x) for x in value]
  if not isinstance(value,dict):return value
  result={}
  for k,v in value.items():
   if k in ('CauseId','CloseCauseId','EndCauseId','CommandId') and isinstance(v,str) and v in commands:v='<partition-advance>'
   if k in ('Revision','CloseRevision','EndRevision','AppliedRevision') and isinstance(v,int) and v>base:v='<after-branch>'
   result[k]=provenance(v)
  return result
 s=provenance(s);calendar=s['OrdinaryMagic'];rawcal=raw['OrdinaryMagic'];events=[]
 def event(kind,row):
  row=copy.deepcopy(row);row.pop('Ordinal',None);row.pop('SegmentOrdinal',None)
  # Commands are provenance, not gameplay. Zero-range expansion has no individual command row.
  for k in ('CauseId','Revision','CloseCauseId','CloseRevision'):row.pop(k,None)
  return {'kind':kind,'record':row}
 for key,kind in [('Segments','segment'),('Activities','activity'),('Settlements','settlement'),('Transitions','transition')]:
  for row in calendar[key]:events.append((row['Ordinal'],0,event(kind,row)))
 epochs={raw['WorldSchedule']['Id']:raw['WorldSchedule']}
 if raw.get('Reinforcement',{}).get('Admission'):e=raw['Reinforcement']['Admission']['Phase']['Epoch'];epochs[e['Id']]=e
 for profile in ('PostRecoveryEncounter','FerryWraith'):
  if raw.get(profile) and raw[profile].get('Admission'):e=raw[profile]['Admission']['Epoch'];epochs[e['Id']]=e
 for r in rawcal['ZeroIdleRanges']:
  e=epochs[r['EpochId']];count=len(e['Order']);start=qty(e['Origin'])
  origins=[x['Origin'] for x in rawcal['Segments'] if x['Origin'] and x['Origin']['EpochId']==r['EpochId']]
  offsets={o['GlobalStart']-o['LocalStart'] for o in origins};assert len(offsets)==1
  offset=offsets.pop();slots=list(range(r['FirstLocalStart'],r['LastLocalStart']+1,count));assert len(slots)==r['Count']
  assert time(start+Fraction(slots[-1]*6,count)+6)==r['Through']
  for i,slot in enumerate(slots):
   at=start+Fraction(slot*6,count);actor='TEST_ONLY.companion';assert e['Order'][slot%count]==actor
   origin={'ActorId':actor,'EpochId':e['Id'],'LocalStart':slot,'GlobalStart':slot+offset,'CarriedAdmissionRevision':0,'IsCarried':False,'Binding':f"{actor}|{e['Id']}|{slot}|{slot+offset}|0"}
   segment={'Origin':origin,'ContextEpoch':e['Id'],'InInitiative':False,'ConsumedAtOpen':False,'At':time(at),'Closed':True,'CloseAt':time(at+6)}
   settlement={'Origin':origin,'ContextEpoch':e['Id'],'At':time(at+6),'Reason':1,'IdleEligible':True,'MagicalActivity':False,'Grounding':False,'Proficiency':2,'Before':0,'After':0,'Reduction':1}
   events.extend([(r['Ordinal'],i*2,event('segment',segment)),(r['Ordinal'],i*2+1,event('settlement',settlement))])
 events.sort(key=lambda x:(x[0],x[1]))
 current=calendar['Current'];selected=next(x for x in calendar['Segments'] if x['Ordinal']==current['SegmentOrdinal']);current.pop('SegmentOrdinal')
 s['OrdinaryMagic']={k:v for k,v in calendar.items() if k not in ('NextOrdinal','Current','Segments','Activities','Settlements','ZeroIdleRanges','Transitions')}
 s['OrdinaryMagic'].update({'Current':current,'CurrentSegment':event('segment',selected)['record'],'OrderedEvents':[x[2] for x in events]})
 # Every calendar property was either retained, referenced, or expanded above.
 # All remaining policy/profile metadata is preserved unchanged.
 return s

def differences(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  if a.keys()!=b.keys():return [path+':keys']
  return [p for k in a for p in differences(a[k],b[k],path+'/'+k)]
 if isinstance(a,list):
  if len(a)!=len(b):return [path+f':length {len(a)} != {len(b)}']
  return [p for i,(x,y) in enumerate(zip(a,b)) for p in differences(x,y,path+'/'+str(i))]
 return [] if a==b else [path]

root=Path(sys.argv[1]);rows=[]
for name,left,right,base in [('nonzero-24-seconds','sparse-whole-after.json','sparse-partitioned-after.json',240),('eight-hours','eight-hour-whole.ddsave.json','eight-hour-parts.ddsave.json',241)]:
 a=json.loads((root/left).read_text());b=json.loads((root/right).read_text());na=normalize(a,base);nb=normalize(b,base);diff=differences(na,nb)
 for side,v in [('whole',na),('parts',nb)]: (root/(name+'.'+side+'.normalized.json')).write_text(json.dumps(v,indent=2)+'\n')
 rows.append({'name':name,'status':'PASS' if not diff else 'FAIL','completeSnapshotTopLevelFields':len(a),'mechanicalEvents':len(na['OrdinaryMagic']['OrderedEvents']),'wholeRevision':a['Revision'],'partsRevision':b['Revision'],'randomEqual':a['RandomState']==b['RandomState'],'differences':diff,'leftSha256':hashlib.sha256((root/left).read_bytes()).hexdigest(),'rightSha256':hashlib.sha256((root/right).read_bytes()).hexdigest()})
result={'status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL','normalization':'Only command/revision provenance and explicit expansion of equivalent zero-idle ranges. Full canonical gameplay structure, exact quantities, RNG and ordered mechanical events retained. Raw histories preserved. ResourceLot/Reservation legacy integral Quantity accessors omitted by serializer; exact Amount/Consumed/Released/Remaining remain.','cases':rows}
(root/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['status']=='PASS'
