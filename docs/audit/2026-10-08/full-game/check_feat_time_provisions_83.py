"""Fresh isolated specification diagnostics. No project/downloaded Python imports.

This neither installs an engine nor changes the current feat candidate. The
recorded actor is the existing synthetic source-qualified acquisition slice;
environment and activity facts are explicit TEST_ONLY inputs, not campaign proof.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';I=R/'data/director/feat_candidates/exact_01'
ROOT=A/'feat335-time-provisions-cases-83';OUT=A/'FEAT335_TIME_PROVISIONS_CASES_83.json';CHECK=A/'FEAT335_TIME_PROVISIONS_CHECK_83.json';ZIP=A/'DD_Feat335_Time_Provisions_Cases_83.zip';SAVED=A/Path(__file__).name
for p in [ROOT,OUT,CHECK,ZIP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[];cases=[]
def ck(name,actual,expected=True):
 ok=actual==expected;checks.append({'check':name,'pass':ok,'actual':actual,'expected':expected})
 if not ok:raise AssertionError(name+': '+repr(actual)+' != '+repr(expected))
def case(id,title,before,inputs,actual,expected,sourceIds,limits='Isolated specification-state diagnostic; no world scheduler or game runtime executed.'):
 ck(id+' complete scoped outcome',actual,expected)
 cases.append({'id':id,'title':title,'initialState':deepcopy(before),'operationInputs':deepcopy(inputs),'computedFinalState':deepcopy(actual),'independentlySpecifiedExpectedFinalState':deepcopy(expected),'governingSources':sourceIds,'qualification':limits})
paths=[I/'candidate.json',I/'shared_rules.json',R/'data/public/feat_candidates/exact_01/candidate.json',A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json',A/'FEAT335_DEFERRED_ACQUISITION_STATE_CHECK.json',A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',A/'feat327-source-verdict/FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json',R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',R/'docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json',A/'EX58_X01_FULFILLMENT.json',A/'EX58_REVIEW_LABEL_NORMALIZATION.json',A/'ACTIVE_AUTHORING_CHECKPOINT_FULL_GAME_FRONTIER_82.json']
bindings=[info(p) for p in paths];cand=j(I/'candidate.json');shared=j(I/'shared_rules.json');public=j(R/'data/public/feat_candidates/exact_01/candidate.json')
records={r['id']:r for r in cand['records']};pp={r['id']:r for r in public['feats']};selected={k:records[k] for k in ['endurance','forager']}
for k,r in selected.items():
 ck(k+' full current public/internal text equality',pp[k]['operationalRules'],r['operationalRules'])
 ck(k+' remains source-authored not promoted',pp[k]['selectionEnabled'] is False and pp[k]['exactApproved'] is False and pp[k]['runtimeApproved'] is False)
ck('Endurance literal CON13 prerequisite',selected['endurance']['sourceObject']['prerequisite'],'Constitution 13+')
ck('Forager literal WIS13 prerequisite',selected['forager']['sourceObject']['prerequisite'],'Wisdom 13+')
for token in ['14lb','56pints','480-active-minute','one-completion/24-elapsed-hour']:
 ck('Forager exact quantity/time source '+token,token in selected['forager']['operationalRules'])
book=(R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md').read_text(encoding='utf-8');booklines=book.splitlines()
for token in ['2 lb of ration-equivalent edible food, 8 pints','1 pint of compatible lamp oil','0.25 lb of ordinary camp sundries','Donkey/mule 10','32, 24, 128, 40, 32, 40, 8, 16 and 12 pints/day','end of the second following canonical Watch']:
 ck('Exact EX58 input source '+token,token in book)
labels=j(A/'EX58_REVIEW_LABEL_NORMALIZATION.json');bk=info(R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md');expected=labels['currentEightCandidateFiles'][bk['path']]
ck('Full current EX58 book exact accepted bytes',(bk['bytes'],bk['sha256']),(expected['bytes'],expected['sha256']))
hist=j(A/'FEAT335_DEFERRED_ACQUISITION_STATE_CHECK.json')['histories'][6]
ck('Existing acquisition source is Endurance',hist['id'],'endurance')
actor=deepcopy(hist['before']);pay=actor['payment'];ck('Existing source slice Warrior8',pay['current_classes'],{'Warrior':8});ck('Existing source slice ability gates',pay['scores']['CON']>=13 and pay['scores']['WIS']>=13)
ck('Two distinct real class-scheduled opportunity levels',all(n in pay['class_schedules']['Warrior'] for n in [4,8]))
paid={'actorSource':bindings[4],'sourcePointer':'/histories/6/before','baseActor':actor,'declaredAvailableOpportunities':['Warrior:4','Warrior:8'],'paidGrants':[{'featId':'forager','opportunity':'Warrior:4','abilitySnapshot':deepcopy(pay['scores'])},{'featId':'endurance','opportunity':'Warrior:8','abilitySnapshot':deepcopy(pay['scores'])}],'scope':hist['before']['actor']['scope'],'notAuthenticatedCampaign':True}
case('FP83-01','Distinct paid prerequisites; no provisions or rest credit created',{'currentClassLevels':pay['current_classes'],'scores':pay['scores'],'available':['Warrior:4','Warrior:8'],'owned':[]},paid['paidGrants'],{'spent':['Warrior:4','Warrior:8'],'owned':['forager','endurance'],'foodLb':0,'waterPints':0,'foodWaterPending':0,'sleepPending':0},{'spent':['Warrior:4','Warrior:8'],'owned':['forager','endurance'],'foodLb':0,'waterPints':0,'foodWaterPending':0,'sleepPending':0},['GE-17','GD-09','FS-12','current acquisition assembly'],limits='New arithmetic/acquisition specification slice using the complete preserved synthetic Warrior8 fixture and actual class schedules. The production acquisition engine and complete character build are not executed or claimed.')

def forage(before,job):
 s=deepcopy(before)
 if not job['eligibleTerrain'] or not job['safeAccessibleCompatibleStocks']:raise ValueError('No qualifying source')
 if not job['actualPaidFeat'] or job['wisdom']<13:raise ValueError('No source-qualified feat')
 intervals=job['activeIntervals'];active=sum(b-a for a,b in intervals)
 if any(a<0 or b<=a for a,b in intervals) or any(a<intervals[i-1][1] for i,(a,b) in enumerate(intervals) if i):raise ValueError('Overlapping/invalid work')
 if active!=480:raise ValueError('Incomplete declared completion')
 end=intervals[-1][1]
 if s['lastCompletedMinute'] is not None and end-s['lastCompletedMinute']<1440:raise ValueError('Existing24hour allowance')
 used={((a//1440),w) for a,b in intervals for w in range((a%1440)//480,((b-1)%1440)//480+1)}
 if len(used)>2 or job.get('priorWorkWatchCount',0)+len(used)>2:raise ValueError('Third active work Watch')
 food,water=job['declaredFoodLb'],job['declaredWaterPints']
 if min(food,water)<0 or food>14 or water>56 or food>s['siteFoodLb'] or water>s['siteWaterPints']:raise ValueError('Absent or excess stock')
 if food>job['foodContainerCapacityLb'] or water>job['waterContainerCapacityPints']:raise ValueError('No real containers')
 s['siteFoodLb']-=food;s['siteWaterPints']-=water;s['holderFoodLb']+=food;s['holderWaterPints']+=water;s['lastCompletedMinute']=end
 return {'stock':s,'elapsedCompletionMinute':end,'activeMinutes':active,'elapsedSpanMinutes':end-intervals[0][0],'nonworkMinutes':end-intervals[0][0]-active,'nextCompletionAtOrAfterMinute':end+1440,'outputContentsLb':food+water,'outputContainersTareLb':job['containersTareLb'],'packedOutputLb':food+water+job['containersTareLb'],'oilCreatedPints':0,'sundriesCreatedLb':0,'abstractSupplyCreated':0,'workWatchSlots':sorted([list(x) for x in used])}
stock={'siteId':'TEST_ONLY-grain-and-spring-A','siteFoodLb':20,'siteWaterPints':80,'holderFoodLb':0,'holderWaterPints':0,'lastCompletedMinute':None}
job={'eligibleTerrain':True,'safeAccessibleCompatibleStocks':True,'actualPaidFeat':True,'wisdom':pay['scores']['WIS'],'activeIntervals':[[0,240],[270,510]],'declaredFoodLb':14,'declaredWaterPints':56,'foodContainerCapacityLb':14,'waterContainerCapacityPints':56,'containersTareLb':16,'containerEvidence':'TEST_ONLY already-owned measured containers:14empty4pint skins at1lb each plus a2lb food container with14lb capacity. No catalog profile or container granted by the feat.','incompatiblePause':'240–270minutes; no active work credit','priorWorkWatchCount':0}
f=forage(stock,job)
case('FP83-02','A genuine480active-minute forage completion with an incompatible30minute pause',stock,job,f,{'stock':{'siteId':'TEST_ONLY-grain-and-spring-A','siteFoodLb':6,'siteWaterPints':24,'holderFoodLb':14,'holderWaterPints':56,'lastCompletedMinute':510},'elapsedCompletionMinute':510,'activeMinutes':480,'elapsedSpanMinutes':510,'nonworkMinutes':30,'nextCompletionAtOrAfterMinute':1950,'outputContentsLb':70,'outputContainersTareLb':16,'packedOutputLb':86,'oilCreatedPints':0,'sundriesCreatedLb':0,'abstractSupplyCreated':0,'workWatchSlots':[[0,0],[0,1]]},['GE-17','EX58 FL-03','EX58 FL-04'],limits='Full bounded task/quantity case. Real site access, edible species-compatible grain, clean water, existing container dimensions, safe pause, paid feat and actor presence are explicit TEST_ONLY premises; the world engine does not authenticate them. The two touched canonical Watches are declared work slots; no third slot or elapsed Watch is added.')
for minute,eligible in [(1949,False),(1950,True),(1951,True)]:
 case('FP83-03-'+str(minute),'One completion per24elapsed hours, measured from actual previous completion',f['stock'],{'queriedCompletionMinute':minute,'queryOnly':True},{'elapsedSinceCompletion':minute-510,'eligible':minute-510>=1440,'stockChanged':False},{'elapsedSinceCompletion':minute-510,'eligible':eligible,'stockChanged':False},['GE-17'],limits='Pure boundary predicate; no second job is asserted to have been worked or completed.')
small={'siteId':'TEST_ONLY-small-site','siteFoodLb':4,'siteWaterPints':8,'holderFoodLb':0,'holderWaterPints':0,'lastCompletedMinute':None};sj={**job,'activeIntervals':[[0,480]],'declaredFoodLb':4,'declaredWaterPints':8}
sf=forage(small,sj)
case('FP83-04','Predeclared smaller guaranteed forage depletes a finite site',small,sj,{'siteFoodLb':sf['stock']['siteFoodLb'],'siteWaterPints':sf['stock']['siteWaterPints'],'holderFoodLb':sf['stock']['holderFoodLb'],'holderWaterPints':sf['stock']['holderWaterPints'],'contentsLb':sf['outputContentsLb']},{'siteFoodLb':0,'siteWaterPints':0,'holderFoodLb':4,'holderWaterPints':8,'contentsLb':12},['GE-17'])
def rejected(id,title,before,inputs,fn,sources):
 frozen=deepcopy(before)
 try:fn();raised=False
 except ValueError:raised=True
 case(id,title,before,inputs,{'rejected':raised,'originalStateUnchanged':before==frozen},{'rejected':True,'originalStateUnchanged':True},sources,limits='Invalid-input/commitment predicate only. Time/resources already represented by the input remain spent; this is not a claim that an attempted real activity rewinds time.')
empty={**sf['stock'],'lastCompletedMinute':None,'holderFoodLb':0,'holderWaterPints':0}
rejected('FP83-05','Another worker cannot recreate depleted source stocks',empty,sj,lambda:forage(empty,sj),['GE-17','EX58 FL-04'])
rejected('FP83-06','479active minutes do not yield the480minute guarantee',stock,{**job,'activeIntervals':[[0,479]]},lambda:forage(stock,{**job,'activeIntervals':[[0,479]]}),['GE-17','EX58 FL-03'])
allocation=[{'consumer':'feat holder','profile':'ordinary Medium person','foodLb':2,'waterPints':8},{'consumer':'companion person','profile':'ordinary Medium person','foodLb':2,'waterPints':8},{'consumer':'one actual donkey/mule','profile':'EX58 named mount diet','foodLb':10,'waterPints':24}]
case('FP83-07','The same finite output feeds two people and one mule using actual distinct demands',{'foodLb':14,'waterPints':56,'oilPints':0,'sundriesLb':0},{'actualConsumers':allocation,'grainCompatibleWithEveryRecipient':True},{'foodConsumedLb':sum(x['foodLb'] for x in allocation),'waterConsumedPints':sum(x['waterPints'] for x in allocation),'foodRemainingLb':14-sum(x['foodLb'] for x in allocation),'waterRemainingPints':56-sum(x['waterPints'] for x in allocation),'oilRemainingPints':0,'sundriesRemainingLb':0},{'foodConsumedLb':14,'waterConsumedPints':40,'foodRemainingLb':0,'waterRemainingPints':16,'oilRemainingPints':0,'sundriesRemainingLb':0},['GE-17','EX58 FL-04','EX58 named mount provisions'],limits='Species compatibility and an actual identified mule are TEST_ONLY premises. The literal10lb/24pint mount profile is used; generic Large-person4lb/16pints is not substituted. This validates diet arithmetic, not a new mount command, carrying or combat procedure.')
baskets=min(14//2,56//8,0//1,int(Fraction(0)/Fraction(1,4)))
case('FP83-08','Food/water output cannot pay an exact whole-Supply cost',{'foodLb':14,'waterPints':56,'oilPints':0,'sundriesLb':0},{'basketRequirement':{'foodLb':2,'waterPints':8,'oilPints':1,'sundriesLb':'1/4'},'exactProcedureRequiresWholeBasket':True},{'completePhysicalBaskets':baskets,'wholeSupplyCommitmentAllowed':baskets>=1,'createdOil':0,'createdSundries':0},{'completePhysicalBaskets':0,'wholeSupplyCommitmentAllowed':False,'createdOil':0,'createdSundries':0},['EX58 FL-04','GE-17'])

class Ledger:
 def __init__(self,minute=0,strain=0,operative=True,last_long=None):
  self.s={'minute':minute,'strain':strain,'foodWaterPending':0,'sleepPending':0,'operative':operative,'restDebt':False,'deadlineMinute':None,'assessedEvents':[],'unsupportedDayEndpoints':[],'lastBeneficialLongRestMinute':last_long,'longRestRewardEligibility':[],'events':[]}
 def snapshot(self):return deepcopy(self.s)
 def penalty(self,cause,event):
  s=self.s
  if event in s['assessedEvents']:raise ValueError('Repeated penalty event')
  field='foodWaterPending' if cause=='foodWater' else 'sleepPending';old=s[field]
  gain=old if s['operative'] else 1;s[field]=1-old if s['operative'] else 0;s['strain']+=gain;s['assessedEvents'].append(event)
  s['events'].append({'minute':s['minute'],'event':event,'cause':cause,'strainGain':gain,'pendingBefore':old,'pendingAfter':s[field]})
 def advance(self,t):
  s=self.s
  if t<s['minute']:raise ValueError('Clock rewind')
  due=s['deadlineMinute'];key='debt-due:'+str(due)
  if s['restDebt'] and due is not None and due<=t and key not in s['assessedEvents']:
   s['minute']=due;self.penalty('sleep',key)
  s['minute']=t
 def miss_rest(self,t):
  if t%480:raise ValueError('This fixture requires an exact canonical Watch endpoint')
  key='missed-rest:'+str(t)
  if key in self.s['assessedEvents']:raise ValueError('Repeated scheduled missed Rest')
  self.advance(t)
  if self.s['restDebt']:self.penalty('sleep',key)
  else:self.s['assessedEvents'].append(key)
  self.s['restDebt']=True;self.s['deadlineMinute']=t+960
  self.s['events'].append({'minute':t,'event':'debt-open-or-reset','deadlineMinute':t+960})
 def day(self,t,food_water,other):
  if t%1440:raise ValueError('Not a24hour endpoint')
  key='day:'+str(t)
  if key in self.s['assessedEvents']:raise ValueError('Repeated daily assessment')
  self.advance(t);s=self.s;s['assessedEvents'].append(key)
  if food_water:s['foodWaterPending']=0
  if not (food_water and other):s['unsupportedDayEndpoints'].append(t)
  if not other:
   if not s['operative'] and not food_water:s['foodWaterPending']=0
   s['strain']+=1;s['events'].append({'minute':t,'event':key,'cause':'independentMandatoryLogistics','strainGain':1})
  elif not food_water:self.penalty('foodWater','foodWater:'+str(t))
 def availability(self,t,operative):self.advance(t);self.s['operative']=operative;self.s['events'].append({'minute':t,'event':'availability','operative':operative})
 def rest(self,start,end,safe=True,uninterrupted=True):
  s=self.s
  if not safe or not uninterrupted or start<0 or end-start<480 or end<s['minute']:raise ValueError('Not a qualifying actual rest')
  if s['restDebt'] and s['deadlineMinute']==end:s['restDebt']=False;s['deadlineMinute']=None
  self.advance(end);s['restDebt']=False;s['deadlineMinute']=None;s['sleepPending']=0
  eligible=s['lastBeneficialLongRestMinute'] is None or end-s['lastBeneficialLongRestMinute']>=1440
  s['longRestRewardEligibility'].append({'endMinute':end,'eligible':eligible})
  if eligible:s['lastBeneficialLongRestMinute']=end
  s['events'].append({'minute':end,'event':'actual-safe-rest-complete','startMinute':start,'beneficialLongRestEligible':eligible,'resourceAmountsApplied':False})
def compact(s):return {k:s[k] for k in ['minute','strain','foodWaterPending','sleepPending','restDebt','deadlineMinute','unsupportedDayEndpoints']}
def ledger_case(id,title,l,before,events,expected):
 after=l.snapshot();case(id,title,before,events,compact(after),expected,['GD-09','FS-12','EX58 FL-03','EX58 FL-04'],limits='Complete state within the specified deprivation/rest slice; detailed transition trace and assessed-event identities are retained below. Actual scheduled Rest, activity exclusivity, provisions and safety are declared inputs. This is not a complete campaign scheduler or HP/RP recovery implementation.');cases[-1]['fullFinalScopedState']=after

l=Ledger();b=l.snapshot();l.day(1440,False,True);l.day(2880,False,True)
ledger_case('FP83-09','Two food/water-only unsupported days alternate omission and penalty',l,b,[{'minute':1440,'foodLbConsumed':2,'waterPintsConsumed':0,'otherSupportSatisfiedByActualDaylightAndSupplies':True},{'minute':2880,'foodLbConsumed':2,'waterPintsConsumed':0,'otherSupportSatisfiedByActualDaylightAndSupplies':True}],{'minute':2880,'strain':1,'foodWaterPending':0,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[1440,2880]})
l=Ledger();b=l.snapshot();l.day(1440,False,True);l.miss_rest(1440);l.advance(2400);l.miss_rest(2880);l.day(2880,False,True)
ledger_case('FP83-10','Food and sleep credits cannot cancel each other or clear debt',l,b,[{'minute':1440,'event':'foodWaterShortageAndMissed16to24Rest'},{'minute':2400,'event':'originalUnpaidDebtDeadline40h'},{'minute':2880,'event':'nextMissed40to48RestThenFoodWaterShortage'}],{'minute':2880,'strain':2,'foodWaterPending':0,'sleepPending':0,'restDebt':True,'deadlineMinute':3840,'unsupportedDayEndpoints':[1440,2880]})
ck('FP83-10 four distinct assessed deprivation events',len([e for e in l.s['events'] if e.get('cause') in ['foodWater','sleep']]),4)
l=Ledger();b=l.snapshot();l.miss_rest(1440);l.rest(1920,2400)
ledger_case('FP83-11','A real32to40hour safe Rest completes at the exact40hour debt deadline',l,b,[{'missedRestEndMinute':1440,'deadlineMinute':2400},{'safeRestStartMinute':1920,'safeRestEndMinute':2400}],{'minute':2400,'strain':0,'foodWaterPending':0,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[]})
ck('FP83-11 no unpaid due event introduced',any(e.get('cause')=='sleep' for e in l.s['events']),False)
l=Ledger(operative=False);b=l.snapshot();l.miss_rest(0);l.advance(960);l.availability(1200,True);l.miss_rest(1440);l.rest(1980,2460)
ledger_case('FP83-12','Late33to41hour Rest preserves the already incurred40hour penalty',l,b,[{'priorScheduledRestEndMinute':0,'initialFeatSuppressed':True},{'dueMinute':960},{'suppressionEndsMinute':1200},{'nextScheduledRestMissedMinute':1440},{'safeRestStartMinute':1980,'safeRestEndMinute':2460}],{'minute':2460,'strain':2,'foodWaterPending':0,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[]})
ck('FP83-12 due events retained at16h and40h',[e['minute'] for e in l.s['events'] if e.get('event','').startswith('debt-due:')],[960,2400])
l=Ledger(minute=2400,last_long=2400);b=l.snapshot();l.miss_rest(2880);l.rest(2880,3360)
ledger_case('FP83-13','Debt-clearing48to56hour Rest does not award a second beneficial Long Rest inside24hours',l,b,[{'priorActualSafeRest':'32–40hours','priorBeneficialLongRestMinute':2400,'prospectivelyDesignatedDay1Rest':'40–48hours','actualReplacement':'voluntary guard duty40–48hours'},{'missedRestEndMinute':2880,'deadlineMinute':3840},{'newActualSafeRest':'48–56hours'}],{'minute':3360,'strain':0,'foodWaterPending':0,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[]})
ck('FP83-13 resource reward ineligible',l.s['longRestRewardEligibility'],[{'endMinute':3360,'eligible':False}]);ck('FP83-13 prior reward identity unchanged',l.s['lastBeneficialLongRestMinute'],2400)
l=Ledger();b=l.snapshot();l.day(1440,False,True);l.availability(1800,False);l.day(2880,False,True);l.availability(3600,True);l.day(4320,False,True)
ledger_case('FP83-14','Suppression clears only the assessed unavailable cause credit and cannot rewrite prior days',l,b,[{'day24':'water-short operative'},{'hour30':'suppressed'},{'day48':'water-short unavailable'},{'hour60':'operative again'},{'day72':'water-short operative'}],{'minute':4320,'strain':1,'foodWaterPending':1,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[1440,2880,4320]})
l=Ledger();b=l.snapshot();l.day(1440,False,True);l.day(2880,False,False)
ledger_case('FP83-15','An independent necessary oil shortage bypasses Endurance without a second daily penalty',l,b,[{'day24':'water shortage only'},{'day48':'water shortage and declared six-hour mandatory lamp use; no alternative safe light; required oil absent'}],{'minute':2880,'strain':1,'foodWaterPending':1,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[1440,2880]})
l=Ledger(strain=2);b=l.snapshot();l.day(1440,False,True);l.day(2880,True,True)
ledger_case('FP83-16','Actually meeting the next day needs clears food credit without erasing earlier Strain or shortage history',l,b,[{'day24':'water shortage only'},{'day48':'actual2lb food and8pints water consumed; all other real needs met'}],{'minute':2880,'strain':2,'foodWaterPending':0,'sleepPending':0,'restDebt':False,'deadlineMinute':None,'unsupportedDayEndpoints':[1440]})
frozen=l.snapshot();rejected('FP83-17','Duplicate settlement cannot charge or consume twice',frozen,{'repeatDayEndpointMinute':2880},lambda:l.day(2880,True,True),['FS-12','EX58 FL-04']);ck('FP83-17 actual ledger unchanged after duplicate rejection',l.snapshot(),frozen)
rejected('FP83-18','Endurance does not authorize a third active work Watch',stock,{**job,'activeIntervals':[[960,1440]],'priorWorkWatchCount':2},lambda:forage(stock,{**job,'activeIntervals':[[960,1440]],'priorWorkWatchCount':2}),['GE-17','GD-09','EX58 FL-03'])
for bad in [{'eligibleTerrain':False},{'safeAccessibleCompatibleStocks':False},{'waterContainerCapacityPints':55},{'actualPaidFeat':False},{'wisdom':12}]:
 k=next(iter(bad));rejected('FP83-19-'+k,'Forage rejects the named absent operative predicate',stock,{**job,**bad},lambda bad=bad:forage(stock,{**job,**bad}),['GE-17'])
for label,safe,uninterrupted,duration in [('unsafe',False,True,480),('interrupted',True,False,480),('short',True,True,479)]:
 l=Ledger();l.miss_rest(1440);before=l.snapshot();rejected('FP83-20-'+label,'An unqualified rest cannot clear an actual debt',before,{'startMinute':1440,'endMinute':1440+duration,'safe':safe,'uninterrupted':uninterrupted},lambda l=l,duration=duration,safe=safe,uninterrupted=uninterrupted:l.rest(1440,1440+duration,safe,uninterrupted),['GD-09','EX58 FL-03']);ck('FP83-20-'+label+' actual ledger unchanged',l.snapshot(),before)

source_excerpts={'selectedFullFeatRecords':selected,'selectedFullSharedRule':next(x for x in shared['rules'] if x['id']=='FS-12'),'completeExistingAcquisitionHistory':hist,'currentAcquisitionAssemblyRows':[x for x in j(A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json')['entries'] if x['id'] in selected],'EX58ExactParagraphs':[{'line':i+1,'text':line} for i,line in enumerate(booklines) if (55<=i+1<=81) or ('Donkey/mule 10' in line)]}
report={'id':'FEAT335-TIME-PROVISIONS-83','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ISOLATED_SOURCE_BOUND_SPECIFICATION_DIAGNOSTICS_NOT_PARENT_ACCEPTANCE','scope':'FXC-06 subset: actual forage work time and finite stock, ordinary people and actual named mule diet, no abstract Supply creation, independent Endurance food/water and sleep causes, real debt deadlines, safe rest versus benefit eligibility, suppression and replay. No time-discount/repair completion claim.',
 'sourceBindings':bindings,'actorFixture':paid,'sources':source_excerpts,'cases':cases,'caseCount':len(cases),'topLevelCaseIds':[f'FP83-{i:02d}' for i in range(1,21)],
 'actualExecution':'Only this newly written self-contained standard-library specification diagnostic ran. No supplied project/downloaded module, gameplay engine, Unity process or campaign state ran.',
 'remainingFXC06':['Complete all source-qualified time-discount compositions and actual phase-credit precision.','Complete whole<=30minute rest repair versus partial tail of a longer order.','Validate full current actor/world activity and acquisition authentication in later implementation; fixture predicates are explicit here.'],
 'approvalBoundaries':{'newRulesSelected':0,'canonicalCandidateChanged':False,'featExactApproval':False,'full335CaseExecution':False,'worldEngineExecution':False,'humanGameplay':False,'balance':False,'wholeGameComplete':False},
 'sourceInformationDeleted':0}
for before in bindings:ck('Original source unchanged '+before['path'],info(G/before['path']),before)
payload={'REPORT.json':enc(report),'check_feat_time_provisions_83.py':Path(__file__).read_bytes(),'README.md':b'# Endurance and Forager source-bound specification cases\n\nThese finite cases exercise existing authored procedures and accepted EX58 interfaces. The full source files, current procedures, actor fixture and before/input/expected/actual state are preserved. TEST_ONLY environment and source-qualified acquisition slices are explicit; this is not a world simulation or complete character validation. FXC-06 remains partly open, including time discounts and repair. No canonical change or parent feat approval occurs.\n'}
for p in paths:payload['sources/'+p.relative_to(G).as_posix()]=p.read_bytes()
payload['MANIFEST.json']=enc({n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())})
ROOT.mkdir()
for n,b in payload.items():
 p=Path('\\\\?\\'+str((ROOT/n).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(payload.items()):z.writestr(n,b)
with zipfile.ZipFile(ZIP) as z:
 ck('Complete unique archive membership',len(z.namelist())==len(payload) and set(z.namelist())==set(payload))
 ck('Archive CRC',z.testzip() is None)
 for n,b in payload.items():ck('Full archive byte roundtrip '+n,z.read(n)==b)
OUT.write_bytes(enc(report));SAVED.write_bytes(Path(__file__).read_bytes());CHECK.write_bytes(enc({'report':info(OUT),'archive':info(ZIP),'checkCount':len(checks),'failures':0,'checks':checks,'scope':report['scope'],'runtimeTestsExecuted':0,'isolatedSpecificationDiagnosticExecuted':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'check':info(CHECK),'caseVariants':len(cases),'topLevelCases':20,'checks':len(checks),'failures':0}))
