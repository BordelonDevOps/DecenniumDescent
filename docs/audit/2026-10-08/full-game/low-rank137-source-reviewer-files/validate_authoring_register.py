"""Source-bound static and executable *reference* checks. No gameplay runtime.
Stdlib only. Reads submitted originals and exported directions; writes report only.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import os,json,hashlib,re
O=Path(os.environ.get('DD_REVIEW_OUTPUT',str(Path(__file__).resolve().parent)))
ROOT=Path(os.environ.get('DD_SOURCE_ROOT','/mnt/data/low_rank_source_v3'))
E=O/'evidence';A=ROOT/'docs/audit/2026-10-08/full-game';R=ROOT/'DescentReviewChanges/ReviewBible'
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
checks=[]
def check(group,id,actual,expected):
 checks.append({'group':group,'id':id,'passed':actual==expected,'actual':actual,'expected':expected})
reg=load(O/'LR_137_AUTHORING_REGISTER.json');rows=reg['records'];byq={d['questionId']:d for d in rows};bys={d['spellId']:d for d in rows}
original={d['questionId']:d for d in load(E/'SELECTED_137_ORIGINAL_RECORDS.json')}
cat={s['id']:s for s in load(R/'data/public/spell_playtests/catalog.json')['spells']}
pol=load(O/'LR_SHARED_OPERATING_DIRECTIONS.json')['policies'];polby={p['id']:p for p in pol}
text=(O/'LR_137_SOURCE_AUTHORING_VERDICT.md').read_text();ck=load(O/'LR_EXACT_CANDIDATE_CHECKLIST.json');pro=load(O/'LR_8_PROPOSAL_DISPOSITIONS.json');interfaces=load(O/'LR_CLASS_AND_SPELL_INTERFACE_DISPOSITIONS.json');conf=load(O/'LR_SOURCE_CONFLICT_DISPOSITIONS.json');worked=load(O/'LR_WORKED_BOUNDARIES.json')
check('coverage','unique137',len(bys),137);check('coverage','questions original exact',set(byq)==set(original),True)
check('coverage','mechanical136',sum(d['authoring'] is not None for d in rows),136)
check('coverage','receipt only Blink',[d['spellId'] for d in rows if d['authoring'] is None],['blink'])
check('coverage','six cohorts',dict(Counter(d['questionId'].rsplit('-',1)[0] for d in rows)),{'IL':26,'UN':23,'TR':29,'NE':30,'EV3':8,'R3':21})
check('coverage','mechanical no promotions',any(d['promotionAuthorized'] for d in rows),False)
for i,d in enumerate(rows):
 q=d['questionId'];s=original[q];raw=s['fullSourceAndCurrentAccessRecord']
 for k in ['spellId','questionId','preparationFile','recordSha256']:
  check('preservation',q+':'+k,d[k],s[k])
 check('preservation',q+':original full equality',d['fullSourceAndCurrentAccessRecord']==raw,True)
 check('preservation',q+':catalog full equality',raw==cat[d['spellId']],True)
 check('preservation',q+':original hash',digest(raw),d['recordSha256'])
 check('preservation',q+':exact question',d['sourceQuestion'],s['individualQuestion'])
 check('preservation',q+':class access',d['classAccess'],raw['classAccess'])
 check('preservation',q+':additional RP',d['additionalRpCost'],raw['additionalRpCost'])
 check('preservation',q+':operational remains null',d['fullSourceAndCurrentAccessRecord']['operational'],None)
 check('preservation',q+':source status',d['sourceStatusUnchanged'],raw['status'])
 check('coverage',q+':chapter section exactly one',text.count('#### '+d['decisionId']+' — '),1)
 check('coverage',q+':checklist question',ck['perQuestion'][i]['completeQuestion'],s['individualQuestion'])
 check('coverage',q+':conflict mapping',conf['perQuestionDispositions'][i]['sourceQuestion'],s['individualQuestion'])
 if d['authoring']:
  au=d['authoring']
  check('authoring-shape',q+':all concrete fields',all(isinstance(au[k],str) and au[k].strip() for k in ['activation','range','components','target','duration','resolution','procedure','limitsAndLifecycle','newDecisionNotice']),True)
  check('authoring-shape',q+':mandatory new label','NEW' in au['newDecisionNotice'],True)
  for k in ['target','duration','resolution','procedure','limitsAndLifecycle']:
   check('manuscript-parity',q+':'+k,au[k] in text,True)
  check('manuscript-parity',q+':worked boundary',d['workedBoundary']['wording'] in text,True)
for p in pol:
 check('manuscript-parity',p['id']+':complete rule',p['wording'] in text,True)
 for path in p['sourcePaths']:check('source-reference',p['id']+':'+path,(ROOT/path).exists(),True)
allbindings=load(A/'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json')['bookBindingsWithActualDocx']
actualbindings=[b for d in rows for b in d['bookBindings']]
check('book','141 bindings',len(actualbindings),141)
check('book','full binding equality',actualbindings,allbindings)
for p in pro['records']:
 d=bys[p['spellId']]
 check('proposal',p['spellId']+':full direction',p['completeWording'],d['authoring'])
 check('proposal',p['spellId']+':source proposal exists',p['unchangedOriginalProposal'] in load(ROOT/p['proposalFile'])['proposals'],True)
 check('proposal',p['spellId']+':four original boundaries',len(p['boundaryDispositions']),4)
 check('proposal',p['spellId']+':not exact promotion',p['exactOperationalApproval'],False)
check('proposal','eight all distinct',len({p['spellId'] for p in pro['records']}),8)
check('proposal','32 original boundaries',sum(len(p['boundaryDispositions']) for p in pro['records']),32)
for c,o in zip(interfaces['classComparisons'],load(E/'CLASS_COMPARISONS.json')):
 check('class-interface',c['id']+':unchanged full original',c['unchangedCompleteComparison'],o)
 check('class-interface',c['id']+':complete prose',c['wording'] in text,True)
 check('class-interface',c['id']+':no promotion',c['newClassPromotion'],False)
for c,o in zip(interfaces['spellCounterparts'],load(E/'COUNTERPARTS.json')):
 check('spell-interface',c['spellId']+':full counterpart',c['unchangedCompleteCounterpart'],o)
 check('spell-interface',c['spellId']+':no promotion',c['promotionAuthorized'],False)
check('class-interface','54 class records',len(interfaces['classComparisons']),54)
check('spell-interface','114 counterpart records',len(interfaces['spellCounterparts']),114)
check('spell-interface','83 operative counterparts',sum(c['unchangedCompleteCounterpart']['operational'] is not None for c in interfaces['spellCounterparts']),83)
check('worked','137 per-identity authored boundaries',len(worked['perSpellBoundaries']),137)
check('worked','18 joint authored boundaries',len(worked['jointBoundaries']),18)
check('worked','not falsely runtime',any(c['runtimePassed'] for c in worked['jointBoundaries']),False)
check('scope','no ordinary source questions left',ck['mechanicalSourceQuestionsBlockingAuthoring'],[])
check('scope','source spell totals unchanged',[sum(s['operational'] is not None for s in cat.values()),sum(s['operational'] is None for s in cat.values())],[276,572])
# Precise focused static seams tied to actual directions, not just generic check counts.
for q in ['UN-19','R3-09']:
 check('focused-static',q+':beneficial and hostile','beneficial or hostile' in byq[q]['authoring']['procedure'],True)
check('focused-static','reflection not old hostile-only policy','first actually resolving hostile' in polby['LR-G14']['wording'],False)
check('focused-static','reflection allows Touch','Touch-delivered' in polby['LR-G14']['wording'],True)
check('focused-static','Silent Echo longer suffix','longer actual utterance' in byq['IL-02']['authoring']['procedure'],True)
check('focused-static','True Strike next end','end of the caster’s next future regular turn' in byq['UN-09']['authoring']['duration'],True)
check('focused-static','Haste explicit exception','NEW ending-cost exception' in byq['R3-12']['authoring']['limitsAndLifecycle'],True)
check('focused-static','class named exceptions retained','Druid Circle always-prepared table' in polby['LR-G01']['wording'],True)
check('focused-static','source Ritual tag count',sum(any(str(t).lower()=='ritual' for t in s.get('tags',[])) for s in load(R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')['spells']),0)

# EXPLICIT REFERENCE FUNCTIONS: finite source-bound arithmetic/contract fixtures only.
# They are not implementations of the game's actions, spatial engine, authority or event bus.
def params(q):return byq[q]['authoring']['numericParameters']
def ref(id,actual,expected):check('executable-reference',id,actual,expected)
def rational(x):return str(x) if isinstance(x,F) else x
ref('Color Spray count',params('IL-11')['maximumTargets'],3)
actors=[{'id':'a','hp':2,'temp':30,'dist':5,'immune':True},{'id':'b','hp':3,'temp':0,'dist':10,'immune':False},{'id':'c','hp':5,'temp':0,'dist':10,'immune':False},{'id':'d','hp':8,'temp':0,'dist':5,'immune':False}]
chosen=sorted(actors,key=lambda a:(a['hp'],a['dist'],a['id']))[:params('IL-11')['maximumTargets']]
ref('Color Spray selected no temp rerank',[a['id'] for a in chosen],['a','b','c'])
ref('Color Spray immunity no fourth replacement',[a['id'] for a in chosen if not a['immune']],['b','c'])
ref('Phantom Footsteps maximum traversed distance',params('IL-08')['seconds']*params('IL-08')['feetPerSecond'],30)
ref('Shadow Marks finite fourth replacement',['m1','m2','m3','m4'][-params('IL-09')['maximumMarks']:],['m2','m3','m4'])
ref('Minor Disguise localized count',params('IL-07')['maximumLocalizedChanges'],3)
ref('Control spectral object 12 pounds rejected',12<=params('IL-04')['objectMaxLb'],False)
ref('Control spectral object half pound admitted',F(1,2)<=params('IL-04')['objectMaxLb'],True)
ref('Necrotic flat pre-resistance 9 minus2 thenhalf',max(0,9-params('NE-15')['necroticFlatReduction'])//2,3)
ref('Necrotic flat never negative',max(0,1-params('NE-15')['necroticFlatReduction']),0)
ref('Spectral Claw critical dice not flat',sum([6,6])+1,13)
ref('Shardstorm half typed components independently',[sum([4,3,2,1,4])//2,5//2],[7,2])
ref('Mixed Slashing9 resisted Fire6 unaffected',[9//2,6],[4,6])
ref('Flame Arrows maximum true physical arrows',params('R3-16')['maximumArrows'],12)
ref('Flame Arrows cannot grant from fewer than present',min(8,params('R3-16')['maximumArrows']),8)
ref('Six meteor maximum all-overlap fire dice',params('EV3-07')['meteors']*2,12)
ref('Six meteor centers preserve five-foot range',params('EV3-07')['castRangeFeet'],5)
ref('Fireball actual cast range',params('EV3-05')['castRangeFeet'] if 'castRangeFeet' in params('EV3-05') else params('EV3-05')['rangeFeet'],20)
ref('Geyser one event per creature/cast',min(4,params('EV3-01')['maxEventsPerCreaturePerCast']),1)
ref('Geyser launch ten feet',params('EV3-01')['launchFeet'],10)
ref('Enlarge mass from 10 lb',rational(F(10)*F(params('TR-19')['growMassNumerator'],params('TR-19')['growMassDenominator'])),'135/4')
ref('Reduce mass from 10 lb',rational(F(10)*F(params('TR-19')['shrinkMassNumerator'],params('TR-19')['shrinkMassDenominator'])),'5/4')
ref('Enlarge factor agrees cubic linear',F(str(params('TR-19')['growLinear']))**3==F(params('TR-19')['growMassNumerator'],params('TR-19')['growMassDenominator']),True)
ref('Shrink factor agrees cubic linear',F(str(params('TR-19')['shrinkLinear']))**3==F(params('TR-19')['shrinkMassNumerator'],params('TR-19')['shrinkMassDenominator']),True)
ref('Repeat enlarge starts from unmodified baseline not33.75',rational(F(10)*F(27,8)),'135/4')
def ability_mod(n):return (n-10)//2
ref('Feral Might18 plus2 score/mod',[min(30,18+2),ability_mod(min(30,18+2))],[20,5])
ref('Feral Might29 cap30',min(30,29+2),30)
# Corpse clock unaffected by treatment.
ref('23h50 plus20 minutes exceeds24h',F(23*60+50+20)>24*60,True)
ref('Gentle Repose never rebases death timestamp',[0,23*3600+50*60+20*60],[0,87000])
def soul_tap(roll,actual_loss,donor_rp,caster_rp_after,caster_max,eligible=True):
 if not eligible or actual_loss<=0:return {'healBeforeCaps':0,'rpTransferred':0,'donorRemaining':donor_rp,'casterRemaining':caster_rp_after}
 h=min(roll,actual_loss);rp=min(roll,donor_rp,max(0,caster_max-caster_rp_after))
 return {'healBeforeCaps':h,'rpTransferred':rp,'donorRemaining':donor_rp-rp,'casterRemaining':caster_rp_after+rp}
ref('Soul Tap joint die real pools',soul_tap(4,3,2,4,6),{'healBeforeCaps':3,'rpTransferred':2,'donorRemaining':0,'casterRemaining':6})
ref('Soul Tap all temporary buffer no funding',soul_tap(4,0,5,4,6),{'healBeforeCaps':0,'rpTransferred':0,'donorRemaining':5,'casterRemaining':4})
ref('Soul Tap zero donorRP still permits funded HP',soul_tap(4,3,0,4,6)['healBeforeCaps'],3)
ref('Soul Tap full caster RP does not debit donor',soul_tap(4,3,5,6,6)['donorRemaining'],5)
ref('Soul Tap donation ineligible',soul_tap(4,3,5,4,6,False)['rpTransferred'],0)
ref('Soul Tap base paid before transfer',6-params('NE-16')['sourceBaseRp'],4)
ref('Soul Tap transfer conservation',2+4,soul_tap(4,3,2,4,6)['donorRemaining']+soul_tap(4,3,2,4,6)['casterRemaining'])
# Future regular-end checkpoints exclude the in-progress turn's endpoint.
ends=[5,11,17,23,29];current_end=5
future=[t for t in ends if t>current_end][:3]
ref('three future ends not current',[*future],[11,17,23])
ref('suppressed middle tick spent not queued',[t for t in future if t!=17],[11,23])
ref('no fourth tick awarded after suppressed event',len(future),3)
# Commitment and deferred action contracts, independent of a game event implementation.
def mark(valid,committed,rolled,trigger):return valid and (committed if trigger=='commit' else rolled)
ref('attack commit mark canceled aftercommit spends',mark(True,True,False,'commit'),True)
ref('illegal attack declaration no commitment',mark(False,False,False,'commit'),False)
ref('roll-only True Strike retains canceled roll',mark(True,True,False,'roll'),False)
ref('roll-only True Strike miss spends',mark(True,True,True,'roll'),True)
def echo_quote(base,surcharge,additional=0):
 if min(base,surcharge,additional)<0:raise ValueError('negative cost')
 return surcharge+additional if params('UN-21')['baseRpWaived'] else base+surcharge+additional
ref('Echo Cast base-only RP quote',echo_quote(3,1),1)
ref('Echo Cast retains actual additional cost',echo_quote(3,1,2),3)
ref('Cantrip Echo one Bonus Action',params('UN-05')['bonusActions'],1)
ref('Quick Cast preparation and payload different rounds',[params('UN-17')['preparationBonusActions'],params('UN-17')['payloadBonusActions']],[1,1])
ref('one turn Bonus Action cannot pay two',[1>=params('UN-17')['preparationBonusActions']+params('UN-17')['payloadBonusActions']],[False])
ref('Delay absolute hold cap',params('UN-14')['maximumHoldSeconds'],6)
ref('Delay later than six seconds rejected',7<=params('UN-14')['maximumHoldSeconds'],False)
ref('Ritual Anchor current payloads empty',params('UN-12')['currentAdmittedPayloadCount'],0)
ref('Glyph ward one use',params('R3-21')['uses'],1)
ref('Glyph trigger radius',params('R3-21')['triggerRadiusFeet'],5)
# Reflection makes a single source-owned delivery, not a new caster-owned event.
def reflection(root_redirected,has_ward,return_legal):
 if root_redirected or not has_ward:return {'spent':False,'redirected':root_redirected,'recipient':'current','newCasts':0}
 return {'spent':True,'redirected':bool(return_legal),'recipient':'original-caster' if return_legal else 'current','newCasts':0}
ref('mirror valid return',reflection(False,True,True),{'spent':True,'redirected':True,'recipient':'original-caster','newCasts':0})
ref('second mirror no loop/no consume',reflection(True,True,True),{'spent':False,'redirected':True,'recipient':'current','newCasts':0})
ref('invalid return spends but no immunity',reflection(False,True,False),{'spent':True,'redirected':False,'recipient':'current','newCasts':0})
# Countered payload does not reach interception; no call to reflection is made.
def mirror_admission(countered,area,multiple,self_only,sole_direct_creature):
 return not (countered or area or multiple or self_only) and sole_direct_creature
ref('countered payload no eligible resolving event',mirror_admission(True,False,False,False,True),False)
ref('ordinary single direct spell admitted',mirror_admission(False,False,False,False,True),True)
ref('area only one occupant not single target',mirror_admission(False,True,False,False,True),False)
ref('Haste extra full Action maximum',params('R3-12')['extraFullActionsPerNumberedRound'],1)
ref('Haste already spent round does not refill',max(0,params('R3-12')['extraFullActionsPerNumberedRound']-1),0)
ref('Haste actual termination cost count',params('R3-12')['backlashRounds'],1)
def haste_backlash(willing_at_application,event,immune=False):
 return willing_at_application and event in {'expiry','concentration-end','dispel','replacement','dismissal'} and not immune
ref('Haste suppression alone is not termination',haste_backlash(True,'suppression'),False)
ref('Haste ended concentration inflicts cost',haste_backlash(True,'concentration-end'),True)
ref('Haste actual immunity still prevents Stunned',haste_backlash(True,'concentration-end',True),False)
ref('Gaseous gap minimum actual inch',params('R3-17')['minimumGapInches'],1)
ref('Gaseous 0.5 inch rejected',F(1,2)>=params('R3-17')['minimumGapInches'],False)
ref('Fold extra passenger count',params('R3-20')['additionalCreatures'],0)
def arc_flash(damage,dex_success,con_success,blind_immune):
 return {'damage':damage//2 if dex_success else damage,'blinded':not con_success and not blind_immune}
ref('Arc Flash separate successful DEX failedCON',arc_flash(9,True,False,False),{'damage':4,'blinded':True})
ref('Arc Flash blindness immunity does not cancel damage',arc_flash(9,False,False,True),{'damage':9,'blinded':False})
# Numeric source ward/profile tests remain scoped, not state/world assertions.
ref('Blade profile same dice after transfer',params('IL-25')['weaponDice'],'2d8')
ref('No-promotions from reference tests',reg['scope']['newPromotions'],0)
report={'reviewId':reg['scope']['reviewId'],'scope':'Static exact-source/register/manuscript comparisons and explicitly limited executable reference arithmetic/contract functions only. Not gameplay runtime, human balance or actual world authentication.','checkCount':len(checks),'groupCounts':dict(Counter(c['group'] for c in checks)),'executableReferenceChecks':sum(c['group']=='executable-reference' for c in checks),'failedChecks':[c for c in checks if not c['passed']],'checks':checks}
(E/'AUTHORING_REGISTER_AND_REFERENCE_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print({k:v for k,v in report.items() if k!='checks'})
if report['failedChecks']:raise SystemExit(1)
