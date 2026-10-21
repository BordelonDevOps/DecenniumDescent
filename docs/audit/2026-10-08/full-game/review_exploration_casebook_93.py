"""Record full semantic review of the original general-exploration feat cases.

Only independent standard-library fixture calculations run. This is not game
runtime, parent335 acceptance, acquisition execution or source-world proof.
"""
from pathlib import Path
from collections import defaultdict
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import json,hashlib,math,zipfile

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';I=R/'data/director/feat_candidates/exact_01'
ROOT=A/'feat335-exploration-casebook-93';OUT=A/'FEAT335_EXPLORATION_ORIGINAL_CASEBOOK_REVIEW_93.json';ZIP=A/'DD_Feat335_Exploration_Casebook_Review_93.zip';SAVED=A/Path(__file__).name
for p in (ROOT,OUT,ZIP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
checks=[]
def ck(name,ok):checks.append({'check':name,'pass':bool(ok)});assert ok,name
c=j(I/'candidate.json');e=j(I/'example_dispositions.json');fa=j(I/'additional_boundary_expectations.json');records={r['id']:r for r in c['records']}
selected=[r for r in c['records'] if r['cohort']=='general_exploration'];ids={r['id'] for r in selected};cases=[x for x in e['cases'] if x['featId'] in ids];boundaries=[x for x in fa['cases'] if x['featId'] in ids]
ck('31 complete selected feats and68 original case positions',len(selected)==31 and len(cases)==68)
ck('Three directly associated FA boundaries',{x['id'] for x in boundaries}=={'FA-03','FA-14','FA-15'})
notes={
'GE-01':[
'Acquisition while untrained grants PB once: DEX3+PB2=5. The source does not immediately turn its own grant into prior training.',
'Already-trained acquisition replaces PB2 by twice PB4: DEX3+4=7. Another Expertise representation remains the same one replacing contribution.',
'The original acrobat and acrobatic IDs and their source effects differ. No identity alias was granted by these cases.'],
'GE-02':[
'Choose Dexterity for the jumping Athletics check before rolling. DEX3+AthleticsPB2=5; Acrobatics Expertise is not the credential for this task.',
'The substitution changes the roll modifier only. Actual reach, paid approach/distance and an unoccupied supported landing remain separate premises.'],
'GE-03':[
'Actual language, observed manner and plausible bodily presentation support the impersonation check. Private passwords are neither perceived evidence nor a benefit of advantage.',
'A direct identity revelation that calls for no Deception/Performance check is outside this advantage predicate. This case creates no generic magical-scan immunity.'],
'GE-04':[
'Existing Animal Handling training at acquisition yields WIS2+2*PB3=8 on its eligible task.',
'The initial untrained branch remains ordinary proficiency. Only the later separate grant can supply whatever its own wording authorizes.',
'Skill quality cannot produce an animal, training, a control contract or an otherwise unavailable combat action. The hypothetical body must already exist.'],
'GE-05':[
'40gp is the recorded reference;20gp is a separate buyer offer. The result identifies the former without causing a sale or compelling a higher offer.',
'The declared ordinary magical-item DC20 applies absent a more specific DC. Actual complete unprotected operative properties are learned; a source-protected curse remains protected. No item or curse is authenticated by this hypothetical.'],
'GE-06':[
'STR15 satisfies the OR prerequisite independently of DEX12. Each skill reads its own pre-acquisition training snapshot.',
'Athletics STR2+2*PB3=8; Acrobatics DEX1+PB3=4; die12+4=16. Equal acquisition timing does not merge these skills.',
'Both already-trained skills obtain separate twice-PB grants; preexisting Expertise in either still contributes twice PB once.'],
'GE-07':[
'The legal Strength-based Intimidation task uses STR4+PB3=7. A weapon can be evidence of the display, not another proficiency term.',
'An imperceptible display supplies no operative communication to that guard. A successful real exchange resolves its predeclared attainable stakes, not an automatic condition.'],
'GE-08':[
'The bounded guarantee prevents accidental wrong choice of a still-valid previously traversed junction; a destroyed bridge remains an actual obstruction.',
'An unobserved teleport lacks an intervening traversed route. Existing map evidence survives where valid but does not identify a new geographical connection.'],
'GE-09':[
'Separate initial snapshots yield CHA3+2*PB2=7 Persuasion and CHA3+PB2=5 Deception.',
'Performance lies outside both named grants and is evaluated only from its actual other credentials.',
'Duplicate twice-PB Persuasion sources preserve both histories but give one replacingPB4 contribution: total7, not11.'],
'GE-10':[
'Current walking20 supplies climbing20. The shared spent-cost ledger retains10 already spent, leaving10 before any new terrain costs.',
'Advantage on a genuine climbing check does not supply a missing grip or adhesion. The slick-wall and unsupported-ceiling examples assume their stated real geometry.'],
'GE-11':[
'Actual levels8 and5 satisfy the comparison; a CR-only profile has no numeric character-level operand. The engine can evaluate a hidden real level without disclosing it.',
'Ordinary Intimidation already uses CHA3. The reverse substitution neither adds STR2 nor a secondCHA3 and supplies no proficiency.'],
'GE-12':[
'The source covers actual Charisma checks during direct noble interaction even when hostile. Attitude affects the real stakes, not the source breadth.',
'The fifteen-minute petition obtains only the announced tomorrow appointment and fee. Future waiting, access, security and the later request remain distinct.'],
'GE-13':[
'The explicitly adopted Deceiver exception permits a deliberate spoken lie after a genuine failed Zone of Truth save, while ordinary credibility still needs its actual social result. Save history, exposure and concentration are not erased.',
'Speaking falsely does not alter directly revealed memories or independently recorded facts. A distinct actual lie-triggered punishment retains its source trigger.'],
'GE-14':[
'CHA2+PB3=5 Persuasion, WIS3+2*PB3=9 Insight. Actual different governing abilities remain.',
'Sequential lawful purchases can make Persuasion already trained before the later Diplomat snapshot. Real opportunities and prerequisite checks are still required for both events.',
'An initiating Insight16 versus existing Deception16 leaves the existing state unchanged under Core opposed ties; Expertise changes the total, not that tie rule.'],
'GE-15':[
'Investigating the actual hinge for a secret door/trap meets the detection predicate. Detection does not execute disarm, safe touch or trigger suppression.',
'Dungeon Delver supplies active advantage only. A passive15 remains15; an independently acquired Observant would be evaluated separately.'],
'GE-16':[
'The actual2sp payer transfer is20cp; the5cp venue payment leaves15cp. Two paid active hours include the expressly allowed fifteen-minute information interaction, not an additional rest or job.',
'The real audience can offer only knowledge it holds. Successful engagement neither creates true facts nor refreshes unchanged attendees into a new information source.'],
'GE-17':[
'The corrected expected outcome makes the existing quantity explicit:14lb food plus56 one-pound pints is70lb before containers. It substitutes only the supported finite forage result, not a full seven-Supply basket.',
'A smaller amount must be declared before work and fit the actual separate stocks. At most4lb food and8pints water can be removed; another actor or container cannot replenish the same pool.'],
'GE-18':[
'Half the specific90-minute active inquiry is45 minutes. A separately scheduled meeting remains at its real calendar time.',
'The discount changes the actor work time only. False claims and unwilling contacts retain their actual truth and agency; no automatic disclosure follows.'],
'GE-19':[
'The explicitly authored Improved Athlete standing reach is STR16. The separately owned Athlete contributes max(0,STRmod3) once to the running baseline:19 feet. Ten supported approach feet plus19 airborne feet spend29 before other costs.',
'Derived climb/swim Speeds use current walking Speed, hence zero when walk is zero. Jump distance permission does not supply voluntary movement budget or a legal landing.'],
'GE-20':[
'DC18-total14 is deficit4 and receives this failed-check fall protection; total13 is deficit5 and does not. Last support and spent cost remain; the protected failure grants no traverse progress.',
'Breaking an anchor after a successful check is a separate loss of support. The failed-check exception does not suspend a body or override Falling.'],
'GE-21':[
'Ten elapsed days fits the30-day memory window. The actually perceived rune shape is recalled, but unknown language and an unobserved reverse side remain unknown.',
'An item recharge timestamp is not an astronomical event. If the region has no real sunrise schedule, this feat produces no invented solar/cosmology fact.'],
'GE-22':[
'PB3 caps the designated real contracts at3; it does not expand the owner-locked12-character expedition roster. Actual hirelings still require wages, consent, duties, time and command rules.',
'Danger expressly excluded by a contract removes the loyalty benefit and cannot force a compliance roll. A genuine amended agreement or refusal remains necessary.'],
'GE-23':[
'Nature INT1+2*PB2=5 and Survival WIS3+PB2=5 come from different training snapshots and abilities.',
'Expertise replaces normal PB; another credential or tool cannot add a second proficiency contribution to the same task.',
'Identification concerns available plant evidence. Neither a successful knowledge roll nor a name refills a depleted harvest pool.'],
'GE-24':[
'A predeclared50-to45gp concession produces the agreed45gp outcome on success. No second unprinted10percent reduction applies.',
'That purchase price is not a future repurchase promise. A genuine resale needs its own buyer, stock/demand, quote, title and settlement.'],
'GE-25':[
'Authorized passive Perception10+WIS3+PB2+5=20; the active modifier is WIS3+PB2=5. The passive feat bonus is not added to the active roll.',
'INT15 increased to16 gives mod3; authorized passive Investigation10+3+PB3+5=21. A task that requires active paid examination keeps that procedure.'],
'GE-26':[
'Ignore only the strategic ordinary terrain-rate penalty for the actually coordinated group. Its laden wagon remains the slowest limiting profile and must physically fit the route.',
'A separated scout is outside the leadership/communication predicate. Tactical terrain costs remain unchanged even while the leader owns the feat.'],
'GE-27':[
'Real natural partial obscurity supplies eligibility for a Hide attempt against that affected observer. Stealth still resolves against that observer passive DC with Core task degrees.',
'An observer with a clear angle or unaffected real sense is separately evaluated. Another observer losing sight does not erase this observer knowledge or perception.'],
'GE-28':[
'The die4 is a maximum discovery count, not matter creation. Only the two actual lots exist;7gp and0.5Load meet the explicit10gp/1Load ceilings.',
'Detection of a locked chest is neither opening nor ownership transfer. Unknown contents cannot be supplied by repeated unchanged scavenging rolls.'],
'GE-29':[
'The corrected example uses actual units: standard2lb/8pints becomes1lb/4pints, Large4lb/16pints becomes2lb/8pints. Strongest half reduction applies once rather than multiplying to quarters.',
'PB3 designates3 actual prepared companions for8 elapsed hours of the exact ordinary heat/cold-save advantage. Their food, water, breathing and required gear remain unchanged.'],
'GE-30':[
'The known/witnessed starting passage, nearby true trail and10-hour age qualify for the authored DC15 local examination. Successful trail direction supplies no flight mode or present-creature location.',
'Age16 hours adds5 and actual heavy intermingling adds5:DC25. Teleport has no intervening physical-passage trail and does not disclose the unknown arrival.'],
'GE-31':[
'Core difficult2+crawl1+squeeze1=4 movement cost per foot. Removing the terrain increment alone yields normal1+crawl1+squeeze1=3.',
'Terrain-only magical doubling is within the explicitly broad source completion. A separately imposed Restrained condition is a distinct cause with Speed0 and is retained.']}
ck('All31 authored review rationales present',set(notes)=={r['questionId'] for r in selected})
reviews=[]
by_question=defaultdict(list)
for x in cases:by_question[x['questionId']].append(x)
for q,rows in by_question.items():
 rows=sorted(rows,key=lambda x:int(x['sourcePointer'].rsplit('/',1)[1]));ck(q+' every original position individually reviewed',len(rows)==len(notes[q]))
 for x,note in zip(rows,notes[q]):
  idx=int(x['sourcePointer'].rsplit('/',1)[1]);r=records[x['featId']]
  ck(x['id']+' complete expected outcome matches current procedure case',x['completeExpectedOutcome']==r['workedCases'][idx])
  reviews.append({'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_EXACT_AUTHORED_PROCEDURE_AND_NAMED_SOURCE_SCOPE','reasoning':note,'qualification':'Source-based semantic adjudication of the full stated example. Hypothetical actors, grants, world geometry, items, knowledge and provider acts are conditional premises, not authenticated gameplay state. Numeric reference calculations are separately enumerated below.','canonicalApply':False,'runtimeExecuted':False})
boundary_notes={
'FA-03':'14+56=70lb; Large4lb/16pints is taken from the same finite stock. Only a Large holder with Survivalist halves its own need to2lb/8pints. No oil or sundry creation.',
'FA-14':'The actual10-minute inspection occupies part of the full30-minute appraisal. It neither creates a second roll nor refunds20 minutes.40gp reference is not20gp gross sale or settled net.',
'FA-15':'For confirmed knowing-holder false face100gp, liability=max(10gp,fees). Fees3gp leave7gp additional; fees12gp leave0 additional. The same fees are credited once; guilt and lawful collection are independent premises.'}
boundary_reviews=[{'id':x['id'],'completeOriginalBoundary':deepcopy(x),'reasoning':boundary_notes[x['id']],'reviewResult':'CONSISTENT_WITH_CURRENT_FS11_FS13_AND_EX58','runtimeExecuted':False} for x in boundaries]

# Actual numeric/state calculations. These are small reference projections of
# stated inputs, never a substitute for full game rule/admission execution.
calculations=[]
def calc(cid,links,inputs,actual,expected,scope):
 ck(cid+' expected projection',actual==expected)
 calculations.append({'id':cid,'originalCaseIds':links,'inputs':inputs,'calculatedResult':actual,'expectedResult':expected,'scope':scope,'runtimeExecuted':False})
def modifier(score):return (score-10)//2
def training(previous):return 2 if previous else 1
calc('GE93-N01',['GE-01-E01','GE-01-E02'],{'DEX':16,'PB':2,'beforeTrained':[False,True]},[modifier(16)+2*training(v) for v in [False,True]],[5,7],'Per-skill training snapshot and actual modifier only.')
calc('GE93-N02',['GE-02-E01'],{'DEX':16,'STR':12,'AthleticsPB':2,'AcrobaticsExpertise':True},modifier(16)+2,5,'Declared Dexterity Athletics uses actual Athletics credential.')
calc('GE93-N03',['GE-04-E01'],{'WIS':14,'PB':3,'previousAnimalHandling':True},modifier(14)+2*3,8,'Expertise replaces one normal PB.')
calc('GE93-N04',['GE-06-E01','GE-06-E02'],{'STR':15,'DEX':12,'PB':3,'previous':[True,False],'acrobaticsDie':12},[15>=15 or 12>=15,modifier(15)+6,modifier(12)+3,12+modifier(12)+3],[True,8,4,16],'Prerequisite OR and two independent actual skill totals.')
calc('GE93-N05',['GE-07-E01'],{'STRmodifier':4,'CHAmodifier':-1,'PB':3},4+3,7,'Legal chosen Strength Intimidation modifier only.')
calc('GE93-N06',['GE-09-E01','GE-09-E03'],{'CHA':16,'PB':2,'previousPersuasion':True,'previousDeception':False,'expertiseCopies':2},[modifier(16)+4,modifier(16)+2,modifier(16)+max(4,4)],[7,5,7],'One replacing proficiency contribution despite two retained grants.')
calc('GE93-N07',['GE-10-E01'],{'currentWalk':20,'spentMovementCost':10},max(0,20-10),10,'Derived current climb cap less the same spent cost; no terrain/body solver.')
calc('GE93-N08',['GE-11-E01'],{'speakerLevel':8,'targetLevels':[5,8,None],'CRonly':5},[level is not None and level<8 for level in [5,8,None]],[True,False,False],'Actual level comparison only; no CR conversion.')
calc('GE93-N09',['GE-11-E02'],{'CHAmodifier':3,'STRmodifier':2},3,3,'One chosen ability modifier; no invented proficiency.')
calc('GE93-N10',['GE-14-E01'],{'CHA':14,'WIS':16,'PB':3,'previous':[False,True]},[modifier(14)+3,modifier(16)+6],[5,9],'Separate task abilities and training snapshots.')
calc('GE93-N11',['GE-14-E02'],{'initialPersuasionProficiency':False,'lawfulOrder':['charismatic','diplomat']},[training(False),training(True)],[1,2],'Conditional granted-order snapshot, not execution of either acquisition or its opportunity.')
calc('GE93-N12',['GE-14-E03'],{'initiatorInsight':16,'existingDeception':16},16>16,False,'Strictly higher opposed total needed to change existing state.')
calc('GE93-N13',['GE-15-E02'],{'passive':15,'activeAdvantageSources':1},15,15,'No passive plus5 from active advantage.')
calc('GE93-N14',['GE-16-E01'],{'bookingSp':2,'cpPerSp':10,'venueCp':5,'activeMinutes':120,'includedTalkMinutes':15},{'netCp':2*10-5,'otherPerformanceMinutes':120-15},{'netCp':15,'otherPerformanceMinutes':105},'Arithmetic of the hypothetical paid booking; no employer, payment or rumor created.')
calc('GE93-N15',['GE-17-E01','FA-03'],{'people':7,'dailyFoodLb':2,'dailyWaterPints':8,'pintLb':1},{'foodLb':7*2,'waterPints':7*8,'cargoLbBeforeContainers':7*2+7*8},{'foodLb':14,'waterPints':56,'cargoLbBeforeContainers':70},'Actual standard quantities only; container capacities and lawful stock are required premises.')
stock={'foodLb':4,'waterPints':8};requested={'foodLb':4,'waterPints':8};remaining={k:stock[k]-requested[k] for k in stock}
calc('GE93-N16',['GE-17-E02'],{'initialStock':stock,'predeclaredRemoval':requested},{'removed':requested,'remaining':remaining,'secondMaximum':{k:min(v,requested[k]) for k,v in remaining.items()}},{'removed':{'foodLb':4,'waterPints':8},'remaining':{'foodLb':0,'waterPints':0},'secondMaximum':{'foodLb':0,'waterPints':0}},'One conditional completed lawful forage deduction and conservation; no harvest/access/scheduler engine.')
calc('GE93-N17',['GE-18-E01'],{'normalActiveMinutes':[90,91,120],'factor':'1/2'},[math.ceil(Fraction(v,2)) for v in [90,91,120]],[45,46,60],'Specific time and final upward minute rounding; appointment wait is outside the factor.')
calc('GE93-N18',['GE-19-E01'],{'STR':16,'approach':10},{'standing':16,'running':16+max(0,modifier(16)),'spent':10+16+max(0,modifier(16))},{'standing':16,'running':19,'spent':29},'Selected feat-local standing/running authored amounts; actual geometry still conditional.')
calc('GE93-N19',['GE-19-E02'],{'currentWalk':0,'spent':0},[max(0,0-0),0>0],[0,False],'No positive voluntary movement from a zero derived mode cap.')
def degree(die,bonus,dc):
 total=die+bonus;base=3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
 return max(0,min(3,base+(1 if die==20 else -1 if die==1 else 0)))
climbs=[{'die':10,'bonus':4,'dc':18},{'die':9,'bonus':4,'dc':18},{'die':1,'bonus':20,'dc':18},{'die':1,'bonus':30,'dc':18}]
climb_results=[{'degree':degree(x['die'],x['bonus'],x['dc']),'deficit':x['dc']-x['die']-x['bonus'],'failedCheckFallProtected':degree(x['die'],x['bonus'],x['dc'])<2 and x['dc']-x['die']-x['bonus']<5} for x in climbs]
calc('GE93-N20',['GE-20-E01'],{'actualClimbChecks':climbs},climb_results,[{'degree':1,'deficit':4,'failedCheckFallProtected':True},{'degree':1,'deficit':5,'failedCheckFallProtected':False},{'degree':1,'deficit':-3,'failedCheckFallProtected':True},{'degree':2,'deficit':-13,'failedCheckFallProtected':False}],'Separates actual task failure/natural shift from numerical deficit. Last-support, grip and collapse state are source premises, not computed geometry.')
calc('GE93-N21',['GE-21-E01'],{'elapsedDays':10,'memoryWindowDays':30},{'ageHours':10*24,'windowHours':30*24,'inside':10<30},{'ageHours':240,'windowHours':720,'inside':True},'Ages strictly inside the named memory window; no endpoint/calendar or perceptual fact invented.')
calc('GE93-N22',['GE-22-E01'],{'PB':3,'willingContracts':3,'existingRoster':12,'newPartyMember':1},{'designations':min(3,3),'rosterAfterProposedAddition':12+1,'withinCap':12+1<=12},{'designations':3,'rosterAfterProposedAddition':13,'withinCap':False},'Designation cap does not relax roster cap; provider contracts remain conditional.')
calc('GE93-N23',['GE-23-E01'],{'INT':12,'WIS':16,'PB':2,'previousNature':True,'previousSurvival':False},[modifier(12)+4,modifier(16)+2],[5,5],'Equal totals from distinct actual skills/abilities.')
calc('GE93-N24',['GE-24-E01'],{'openingQuoteGp':50,'announcedSuccessGp':45},{'finalGp':45,'concessionGp':50-45},{'finalGp':45,'concessionGp':5},'Uses actual agreed success quote; no multiplicative generic discount.')
calc('GE93-N25',['GE-25-E01'],{'WIS':16,'PB':2},{'passive':10+modifier(16)+2+5,'activeModifier':modifier(16)+2},{'passive':20,'activeModifier':5},'Passive-only plus5 distinguished from active modifier.')
calc('GE93-N26',['GE-25-E02'],{'INTbefore':15,'increase':1,'PB':3,'cap':20},{'INTafter':min(20,15+1),'passive':10+modifier(min(20,15+1))+3+5},{'INTafter':16,'passive':21},'Actual half-feat score change and authorized passive Investigation formula.')
calc('GE93-N27',['GE-26-E01'],{'walkerNormalMph':3,'ladenWagonNormalMph':2,'ordinaryTerrainFactor':'1/2','independentWeatherFactor':'3/4'},{'coordinatedRateWithFeat':str(min(Fraction(3),Fraction(2))*Fraction(3,4)),'withoutFeat':str(min(Fraction(3),Fraction(2))*Fraction(1,2)*Fraction(3,4))},{'coordinatedRateWithFeat':'3/2','withoutFeat':'3/4'},'Conditional numerical profiles illustrate removing only terrain; the example does not grant these speeds to any real wagon or route.')
calc('GE93-N28',['GE-27-E01','GE-27-E02'],{'stealthDie':10,'stealthModifier':5,'observerApassive':15,'AactualNaturalObscurity':True,'BclearSight':True},{'Adegree':degree(10,5,15),'AhideSucceeds':degree(10,5,15)>=2,'BfeatEligibility':False},{'Adegree':2,'AhideSucceeds':True,'BfeatEligibility':False},'Conditional per-observer roll/eligibility projection; no actual sensory engine or saved Hidden operation.')
calc('GE93-N29',['GE-28-E01'],{'die':4,'actualLots':[{'gp':3,'load':'1/5'},{'gp':4,'load':'3/10'}]}, {'lotCount':min(4,2),'gp':3+4,'load':str(Fraction(1,5)+Fraction(3,10)),'underCaps':7<=10 and Fraction(1,2)<=1},{'lotCount':2,'gp':7,'load':'1/2','underCaps':True},'Finite listed lots already meet both caps; no general tie/selection algorithm authored.')
calc('GE93-N30',['GE-29-E01','FA-03'],{'standard':[2,8],'large':[4,16],'overlappingFactors':['1/2','1/2']},{'factor':str(min(Fraction(1,2),Fraction(1,2))),'standard':[str(Fraction(v,2)) for v in [2,8]],'large':[str(Fraction(v,2)) for v in [4,16]]},{'factor':'1/2','standard':['1','4'],'large':['2','8']},'Exact personal requirements and strongest factor only.')
calc('GE93-N31',['GE-29-E02'],{'PB':3,'participatingCompanions':4,'elapsedHours':8},{'maximumDesignations':min(3,4),'durationMinutes':8*60},{'maximumDesignations':3,'durationMinutes':480},'Named prepared-companion cap and elapsed duration only; no automatic selection or actual climate/admission.')
calc('GE93-N32',['GE-30-E01','GE-30-E02'],{'trails':[{'ageHours':10,'heavilyIntermingled':False},{'ageHours':16,'heavilyIntermingled':True}]},[15+(5 if age>12 else 0)+(5 if mixed else 0) for age,mixed in [(10,False),(16,True)]],[15,25],'DC calculation for actual known trails strictly within lifetime; no trail creation, time-sampling or expiration-order policy.')
calc('GE93-N33',['GE-31-E01'],{'difficultTerrainCost':2,'crawlAdditional':1,'squeezeAdditional':1},{'ordinary':2+1+1,'withPersonalTerrainException':1+1+1},{'ordinary':4,'withPersonalTerrainException':3},'Only the terrain increment removed; distinct physical cost causes retained.')
calc('GE93-N34',['FA-14'],{'fullAppraisalMinutes':30,'includedInspectionMinutes':10,'referenceGp':40,'offerGp':20},{'remainingDistinctWorkMinutes':30-10,'totalMinutes':10+(30-10),'saleMinusReferenceGp':20-40},{'remainingDistinctWorkMinutes':20,'totalMinutes':30,'saleMinusReferenceGp':-20},'No second roll/time refund or compulsory sale follows the arithmetic.')
calc('GE93-N35',['FA-15'],{'falseFaceGp':100,'actualFeesGp':[3,12],'knowingLawfulFinding':True},[{'totalGp':max(100//10,s),'additionalFineGp':max(0,100//10-s)} for s in [3,12]],[{'totalGp':10,'additionalFineGp':7},{'totalGp':12,'additionalFineGp':0}],'Whole-gp exact inputs avoid rounding ambiguity; actual collection and knowledge finding remain separate.')

paths=[I/'candidate.json',I/'example_dispositions.json',I/'additional_boundary_expectations.json',I/'shared_rules.json',I/'fex_dispositions.json',R/'data/director/general_exploration_feat_operating_proposal_internal.json',R/'data/public/feat_candidates/exact_01/candidate.json',R/'docs/feats/exact-candidate-01/GENERAL_EXPLORATION.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',R/'data/public/spell_playtests/catalog.json',A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json',A/'FEAT335_TIME_PROVISIONS_CASES_83.json',A/'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json']
source_bytes={p.relative_to(G).as_posix():p.read_bytes() for p in paths};proposal=j(paths[5]);proposal_rows={r['id']:r for r in proposal['records']} if 'id' in proposal['records'][0] else {r['featId']:r for r in proposal['records']}
for x in cases:
 parts=x['sourcePointer'].split('/')[1:];value=proposal
 for part in parts:value=value[int(part)] if isinstance(value,list) else value[part]
 ck(x['id']+' complete original source text preserved',value==x['original'])
public=j(R/'data/public/feat_candidates/exact_01/candidate.json');pr={x['id']:x for x in public['feats']};manuscript=(R/'docs/feats/exact-candidate-01/GENERAL_EXPLORATION.md').read_text(encoding='utf-8-sig')
for r in selected:
 ck(r['id']+' full public procedure and cases agree',r['operationalRules']==pr[r['id']]['operationalRules'] and r['workedCases']==pr[r['id']]['workedCases'])
 ck(r['id']+' full chapter procedure and cases present',r['operationalRules'] in manuscript and all(s in manuscript for s in r['workedCases']))
ck('All660 expected outcomes already match full current feat case mirrors',all(x['completeExpectedOutcome']==records[x['featId']]['workedCases'][int(x['sourcePointer'].rsplit('/',1)[1])] for x in e['cases']))
linked={cid for n in calculations for cid in n['originalCaseIds']};catalog=j(R/'data/public/spell_playtests/catalog.json');zone=next(x for x in catalog['spells'] if x['id']=='zone-of-truth')
report={'id':'FEAT335-EXPLORATION-ORIGINAL-CASEBOOK-REVIEW-93','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'68_ORIGINAL_POSITIONS_AND3_BOUNDARIES_SEMANTICALLY_REVIEWED_WITH35_BOUNDED_REFERENCE_CALCULATIONS_PARENT_PENDING','scope':'All31 full general_exploration procedures, original source objects and68 original case positions read and compared with final shared/FEX directions, current public/chapter mirrors, Core movement/rolls, EX58 and exact Zone of Truth. Full original values and corrected expected outcomes remain preserved.','sourceBindings':[info(p) for p in paths],'completeSelectedRecords':selected,'completeRelatedAthleteRecord':records['athlete'],'completeZoneOfTruthCounterpart':zone,'originalCaseReviews':reviews,'additionalBoundaryReviews':boundary_reviews,'numericAndStateCalculations':calculations,'coverage':{'cohort':'general_exploration','fullFeatProcedures':31,'originalCasePositions':68,'additionalBoundaries':3,'boundedCalculations':35,'originalCasesWithNumericalProjection':sum(x['id'] in linked for x in cases),'additionalBoundariesWithNumericalProjection':sum(x['id'] in linked for x in boundaries),'originalTotalPositions':660,'otherOriginalPositionsOutsideThisReview':660-68,'additionalTotalPositions':28,'otherAdditionalPositionsOutsideThisReview':28-3},'reviewFindings':['No conflicting expected outcome identified among these68 full cases and3 boundaries under their stated conditional premises.','All660 selected expectations match their existing full current feat case mirrors; this is a complete fidelity check, not semantic review of the other592 positions.','Parent procedures still contain historical proposed/future-review language. The exact shared/FEX directions specify the selected authoring choices; whole-parent acceptance and implementation remain pending.','Actual world-specific prerequisites remain conditional: geometry, grips, stocks, authentic perceptions, contacts, items, contracts, payment and true levels are not supplied by prose or this script.','Current Zone of Truth restricts deliberate assertions across actual language-capable channels; the reviewed Deceiver example specifically concerns a spoken lie. It does not establish any new speech/sign/writing equivalence beyond the exact feat/source wording.'],'remainingScope':['Other592 original examples and25 additional boundaries are outside this completed cohort review. Earlier bounded diagnostics remain separate evidence and are not silently counted as full-casebook review.','Real full acquisition snapshots and native world/scheduler/persistence operations remain to be executed and reviewed in their correct later scope.','Tracker and Keen Mind examples are strictly inside their windows. This review does not newly resolve a boundary crossed during an examination or unseen world/cosmology information.','The original general_exploration cases do not exhaust all possible cross-feature compositions, runtime concerns or numerical balance.','Retain all existing parent335/copy/gadget/whole-positive-case holds and all remaining ordinary spell reviews.'],'checks':checks,'passed':len(checks),'failed':0,'newMechanicsAuthored':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproved':False,'cosmologyDecisions':0,'actuallySentToGpt':False}
payload=enc(report);script=Path(__file__).read_bytes()
ROOT.mkdir()
for rel,raw in source_bytes.items():
 p=ROOT/'sources'/rel;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw)
for p,raw in [(SAVED,script),(ROOT/Path(__file__).name,script),(OUT,payload),(ROOT/'REVIEW.json',payload)]:
 with p.open('xb') as f:f.write(raw)
readme='Complete source-preserving general-exploration casebook review93:31 full feat procedures,68 original case positions and3 FA boundaries. Every case has its own full original/expected text and semantic rationale.35 separate bounded reference calculations supplement that review; none is a game-runtime test. All source/case identities remain intact. Parent335 is pending. No canonical implementation or new mechanics. No supplied program needs execution.\n'
with (ROOT/'README.txt').open('xb') as f:f.write(readme.encode())
files=sorted(p for p in ROOT.rglob('*') if p.is_file());manifest={'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
with (ROOT/'MANIFEST.json').open('xb') as f:f.write(enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert all(len(z.read(x['path']))==x['bytes'] and sha(z.read(x['path']))==x['sha256'] for x in manifest['files'])
assert all((G/rel).read_bytes()==raw for rel,raw in source_bytes.items())
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'coverage':report['coverage'],'checks':len(checks),'failed':0,'archiveMembers':len(manifest['files'])+1},indent=2))
