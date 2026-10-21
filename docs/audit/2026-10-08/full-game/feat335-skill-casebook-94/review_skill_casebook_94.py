"""Full original skill-feat case review with bounded independent calculations."""
from pathlib import Path
from collections import defaultdict
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import json,hashlib,math,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';I=R/'data/director/feat_candidates/exact_01'
D=A/'feat335-ft84-derived-review-92/after/DescentReviewChanges/ReviewBible';P=A/'feat335-work-compositions84-part5-return-01'
ROOT=A/'feat335-skill-casebook-94';OUT=A/'FEAT335_SKILL_ORIGINAL_CASEBOOK_REVIEW_94.json';ZIP=A/'DD_Feat335_Skill_Casebook_Review_94.zip';SAVED=A/Path(__file__).name
for p in (ROOT,OUT,ZIP,SAVED):assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
checks=[]
def ck(name,ok):checks.append({'check':name,'pass':bool(ok)});assert ok,name
before=j(I/'candidate.json');derived=j(D/'data/director/feat_candidates/exact_01/candidate.json');e=j(I/'example_dispositions.json');records={r['id']:r for r in derived['records']};before_records={r['id']:r for r in before['records']}
selected=[r for r in derived['records'] if r['cohort']=='skill'];ids={r['id'] for r in selected};cases=[x for x in e['cases'] if x['featId'] in ids]
ck('25 skill procedures and50 original cases',len(selected)==25 and len(cases)==50)
ck('Only Spell Scribe has accepted FT84 procedure successor',[r['id'] for r in selected if r['operationalRules']!=before_records[r['id']]['operationalRules']]==['spell_scribe'])
notes={
'SF-01':[
'Original3+3=6 is ordinary Failure atDC15. Replacement1+3=4 is Critical Failure by margin, with the natural downgrade bounded at that floor. Commit the replacement once and then its actual falling consequence; no action replay or restoration of the old die.',
'Advantage selects4 from2/4, then the whole reroll selects8 from1/8. The effective natural result is8, not the unselected1: total11 is Failure. One LR use funds the replacement and cannot reroll itself.'],
'SF-02':[
'The actual Soldier1 and INT14 meet the named class/ability bridge. A legitimate observed planning Investigation check gets INT+onePB+2; its later crossbow attack is outside the tactics predicate.',
'A background or occupation called soldier is not an acquired Soldier class level. The example preserves distinct source identities and supplies no acquisition opportunity.'],
'SF-03':[
'Raw1 becomes effective2 before natural evaluation. AtDC20, effective2+2=4 remains Critical Failure by numerical margin. The inactive legacy never-fail-critically promise does not override the selected current effect.',
'Replace the raw face before disadvantage selection:1/17 becomes2/17 and selects2. A visually perceived calming posture can carry its narrow emotional signal to a deaf beast without granting heard speech or language.'],
'SF-04':[
'Derive climb20 from current walk20 after its real reduction; retain the10 already spent. Do not subtract the inherited reduction again or restart movement on changing mode.',
'The angle-only disadvantage exception still requires a supportable route. A real rope can supply support, while independent slickness remains; a featureless ceiling has no supplied adhesion.'],
'SF-05':[
'Insight16 cannot beat Deception16 in an initiating opposed contest. Neither an identical extra minute nor a new label supplies changed evidence for a retry.',
'A genuine current desire to end the conversation can be supported by observed behavior. An unknown future contact name is neither the stated surface result nor information created by success.'],
'SF-06':[
'Twice PB applies to the actual chosen already-trained History credential and its culture/custom scope. An Engineering structural task is a different credential and receives no such multiplier.',
'The originally untrained Religion branch is frozen at acquisition. A later separate grant follows its own rule; it does not retroactively rewrite this feat snapshot.'],
'SF-07':[
'Ten minutes can produce a real ally disguise, but the wearer-owned feat bonus remains with its owner. The owner must actually wear the qualifying disguise for their own identity-maintenance Deception check.',
'Clothing cannot change actual Large anatomy, doorway clearance or unknown credentials. Success on a plausible identity check does not resolve those independent obstacles.'],
'SF-08':[
'Observable6+4 minutes satisfy the10 active-minute map requirement; the5-minute obscured pause advances world time only. The named mapping/travel concurrency grants no unrelated work credit.',
'Preserve the map observations for the intact approach and mark the collapsed bridge segment unreliable. The map gives neither bridge-crossing permission nor an invented alternate path.'],
'SF-09':[
'A genuine living dying-to-Stable transition precedes the direct1HP offer. Positive recovery clears the obsolete Stable deadline and only zero-HP unconsciousness; other causes remain. The shared recipient LR epoch prevents another practitioner offering a second point.',
'A broad HP-gain prohibition blocks the1HP but not the recorded stabilization or its spent offer entitlement. Separately owned Field Medic requires its actual healer-kit event; its tempHP can apply when independently eligible but cannot wake Stable0.'],
'SF-10':[
'The extra shaving must exist in the searched frame and be discoverable by that real examination. It supplements ordinary forced-lock information without identifying an unsupported culprit.',
'The source requires one additional available physical clue, not guaranteed matter creation. A washed empty scene can truthfully have no further clue under the completed examination.'],
'SF-11':[
'Initiative12+DEX3+feat2-Concussion1=16. Its Skill catalog classification does not supply PB. Current FS03 governs distinct actual feat contributions despite the retained historical future-reference sentence.',
'An extra turn is not a new initiative roll. It neither adds2 to the saved total nor replaces original deadline markers.'],
'SF-12':[
'Recalling a studied ledger preserves what the document claimed. It does not authenticate whether the claimed payment happened.',
'A genuine quote/locate/compare task concerning understood studied text gets2. An unread sealed page supplies no memory or remote access; the inactive legacy5 is not added.'],
'SF-13':[
'DC18-total14 has deficit4 and receives protection only against failure-triggered picking traps; total13 has deficit5 and does not. The lock must be an actual lawful attempt; the2 bonus itself needs a preidentified complex lock.',
'Natural1+15=16 is ordinary Failure shifted to Critical Failure, but deficit2 still qualifies for the narrow failure-trigger protection. An independently satisfied touch trigger remains operative.'],
'SF-14':[
'The successful task returns evidence-supported approximate count, size and age, including uncertainty for intermixed prints. It does not infer exact identity or create obliterated tracks.',
'skill_feats1_master_tracker is explicitly the same master_tracker identity. Both saved representations retain one acquisition and a single2 contribution.'],
'SF-15':[
'Pay the actual authorized escape Action and LR use before replacing that one grapple check by ordinary success. A separate magical restraint survives; the feat provides no move, teleport or critical result.',
'A sealed cell with no eligible Grappled/Restrained escape check has no lawful activation predicate. No attempt or use is spent merely because escape is desired.'],
'SF-16':[
'The selected noncontact one-minute study expressly exempts the act of studying/recognizing from a gaze-only trigger. A distinct threshold crossing remains a real independent trigger and can interrupt the study.',
'An actual time-triggered mark retains its deadline during the minute. The feat neither pauses time nor credits a study that did not finish; no rune profile is generated by the example.'],
'SF-17':[
'Declared silent-debris mode halvesSpeed30 to15 for the interval. Difficult cost2 permits7.5 physical feet, or one complete5-foot tile when that representation requires whole tiles. Dash adds another reduced15 budget, not30.',
'Suppression is limited to careful footfall/debris sounds. Clear sight and an independently rattling carried chain remain evidence; no automatic Hidden state follows.'],
'SF-18':[
'An acknowledged porter bargain can satisfy the purposeful Persuasion predicate through a real understood channel. The2 bonus creates neither a porter nor waived wages or an automatic agreement.',
'Intimidation remains a distinct check even in a negotiation. Naming the threat hard negotiation does not change the actual skill into qualifying Persuasion.'],
'SF-19':[
'An actually authorized copy with separately classified40gp mundane and10gp rare inputs uses half120 minutes and three-quarters40gp, preserving rare10gp. This does not classify an ambiguous bill by absence or grant scroll production.',
'Wizard Spell Scribing supplies its own half factors only for a legal found Wizard spell copied into its actual spellbook. Strongest same-purpose factors apply once. Four indivisible sheets need3 and one still needs1. Mere Wizard ownership does not confer that cost rule on a different ritual-learning route; FT84 controls the separate written-ritual composition.'],
'SF-20':[
'Remove the actual motion disadvantage cause, leaving the independent darkness cause. One actual advantage then cancels remaining disadvantage normally; cause counts do not vote.',
'Fine-Motor Trauma is a numerical1 penalty under Core, not a disadvantage cause. The feat preserves that numerical penalty and the actual impairment.'],
'SF-21':[
'Passive15 meets a real accessible clueDC15 at normal pace. Arithmetic supplies no invisible clue, sense or authorization to replace a source-required active search.',
'Current blindness prevents the sight-dependent2 save bonus despite earlier knowledge of the floor plate. Remembered location can still inform a legal movement choice.'],
'SF-22':[
'An actually permitted fear-ending Wisdom save gets2 and retains binary save rules. Automatic duration expiry supplies no roll or new use opportunity.',
'An opposed Insight defense can qualify only when the real declared stake is coercive influence. An unrelated fixed-DC receipt Investigation is neither that contest nor a qualifying save.'],
'SF-23':[
'PB3 is a ceiling; only2 actual safe forage portions exist, so30-minute preparation affects2. Six-hour protection pauses existing spoilage age rather than rejuvenating stock or creating food.',
'Two cooks still share one recipient LR-family entitlement. The first qualifying consumption fixes its one-hour deadline; another portion neither adds a second1 nor refreshes it. Unsafe or poisoned material retains its hazard.'],
'SF-24':[
'The selected full replacement keeps personally owned eligible spell attacks as well as weapon attacks. Each distinct eligible50percent feat computes floor(0.5*native10)=5 independently; a separate1d6 rider is excluded from both bases, and no compounding occurs.',
'Huge-target paid advantage mode retains its slow qualification when disadvantage cancels the advantage. The actual hit and spent SR use precede the STR save. Failure evaluates half30=15 against the same pre-control30 as the independentminus10 result20; use15, not10. Success prevents this slow without refund.'],
'SF-25':[
'ActualCR1 yields ceil(10+1)=11. Successful briefing applies2 only to actual eligible understood participants against the named creature for its minute; same-feat sources remain a single2 contribution. Eligible self is an ally under FS05.',
'An actual nonhostileCR1/4 beast at200 feet meets the declared range/type predicate if its signal can be perceived. A successful paid DC15 call does not create a path through a sealed wall, teleport the creature or refund the spent attempt.']}
ck('Every skill question has two individual rationales',set(notes)=={r['questionId'] for r in selected} and all(len(n)==2 for n in notes.values()))
reviews=[]
for x in cases:
 idx=int(x['sourcePointer'].rsplit('/',1)[1]);r=records[x['featId']]
 ck(x['id']+' whole expected case matches accepted-derived manuscript data',x['completeExpectedOutcome']==r['workedCases'][idx])
 reviews.append({'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_EXACT_CURRENT_AUTHORING_AND_STATED_CONDITIONS','reasoning':notes[x['questionId']][idx],'qualification':'Full stated-case semantic review. Real acquisition, actors, physical sources, senses, targets, actions, gates and events remain conditional premises. Separately listed calculations execute only their bounded reference projection.','runtimeExecuted':False,'canonicalApplied':False})
calcs=[]
def calc(cid,case_ids,inputs,actual,expected,scope):
 ck(cid+' expected result',actual==expected);calcs.append({'id':cid,'originalCaseIds':case_ids,'inputs':inputs,'calculatedResult':actual,'expectedResult':expected,'scope':scope,'runtimeExecuted':False})
def degree(face,bonus,dc):
 total=face+bonus;d=3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
 return max(0,min(3,d+(1 if face==20 else -1 if face==1 else 0)))
calc('SF94-N01',['SF-01-E01'],{'DC':15,'modifier':3,'oldFace':3,'replacement':1},[3+3,degree(3,3,15),1+3,degree(1,3,15)],[6,1,4,0],'Full chosen-face task outcomes, not a falling engine.')
calc('SF94-N02',['SF-01-E02'],{'oldFaces':[2,4],'newFaces':[1,8],'advantage':True,'modifier':3,'DC':15},[max(2,4)+3,degree(max(2,4),3,15),max(1,8)+3,degree(max(1,8),3,15)],[7,1,11,1],'Replace both original dice and evaluate the selected natural result.')
calc('SF94-N03',['SF-02-E01'],{'conditionalDie':8,'INTmodifier':2,'PB':2,'tacticsFeat':2},8+2+2+2,14,'Illustrative legal planning task formula with explicit new fixture die/PB; not an added attack modifier.')
calc('SF94-N04',['SF-03-E01'],{'rawFace':1,'effectiveFace':2,'bonus':2,'DC':20},[2+2,degree(2,2,20)],[4,0],'Effective natural2 has no natural1 downgrade but retains critical margin failure.')
calc('SF94-N05',['SF-03-E02'],{'rawFaces':[1,17],'disadvantage':True},min(2 if f==1 else f for f in [1,17]),2,'Replacement occurs before disadvantage selection; raw history remains in inputs.')
calc('SF94-N06',['SF-04-E01'],{'originalWalk':30,'actualReduction':10,'spentCost':10},{'walk':30-10,'derivedClimb':30-10,'remaining':max(0,30-10-10)},{'walk':20,'derivedClimb':20,'remaining':10},'One inherited penalty, one spent movement ledger; support/access are assumed.')
calc('SF94-N07',['SF-05-E01'],{'Insight':16,'Deception':16},16>16,False,'Opposed initiating tie gives no new result.')
calc('SF94-N08',['SF-06-E01','SF-06-E02'],{'conditionalPB':3,'initialHistoryTrained':True,'initialReligionTrained':False},{'qualifiedHistoryContribution':2*3,'initialReligionContribution':3,'afterLaterDuplicateReligionContributionFromThisFeat':3},{'qualifiedHistoryContribution':6,'initialReligionContribution':3,'afterLaterDuplicateReligionContributionFromThisFeat':3},'Per-acquisition branch contribution; independent later source effects are outside this projection.')
calc('SF94-N09',['SF-07-E01'],{'qualifyingPreparedDisguise':True,'wearerOwnsFeat':[False,True]},[2 if owner else 0 for owner in [False,True]],[0,2],'Conditional wearer entitlement only; no disguise fabrication or inspection engine.')
calc('SF94-N10',['SF-08-E01'],{'segments':[{'elapsedMinutes':6,'observable':True},{'elapsedMinutes':5,'observable':False},{'elapsedMinutes':4,'observable':True}]},{'worldMinutes':6+5+4,'creditedMappingMinutes':6+4},{'worldMinutes':15,'creditedMappingMinutes':10},'Named concurrent mapping time with uncredited obscured interval.')
def recovery_projection(blocked):
 s={'normalHP':0,'stable':True,'stableDeadlineSeconds':10800,'recipientEpoch':'LR7','surgeonOfferSpent':True,'independentUnconsciousCause':False}
 if not blocked:s.update(normalHP=1,stable=False,stableDeadlineSeconds=None)
 return s
calc('SF94-N11',['SF-09-E01','SF-09-E02'],{'genuineStabilizationAlreadyCompleted':True,'recipientEpoch':'LR7','savedDeadline':10800,'broadHPGainBlocked':[False,True]},[recovery_projection(False),recovery_projection(True)],[{'normalHP':1,'stable':False,'stableDeadlineSeconds':None,'recipientEpoch':'LR7','surgeonOfferSpent':True,'independentUnconsciousCause':False},{'normalHP':0,'stable':True,'stableDeadlineSeconds':10800,'recipientEpoch':'LR7','surgeonOfferSpent':True,'independentUnconsciousCause':False}],'Post-stabilization conditional offer projection only, not actual Medicine/kit/scheduler execution. The hypothetical deadline is already saved.')
calc('SF94-N12',['SF-09-E02'],{'normalHP':0,'separatelyOwnedFieldMedic':True,'actualKitStabilization':True,'PB':3},{'normalHP':0,'offeredTempHP':3,'wokenByTempHP':False},{'normalHP':0,'offeredTempHP':3,'wokenByTempHP':False},'Separate genuine kit-triggered Field Medic offer; no ordinary healing or awakening from temporary HP.')
calc('SF94-N13',['SF-11-E01'],{'die':12,'DEXmodifier':3,'feat':2,'Concussion':-1},12+3+2-1,16,'Actual initiative arithmetic with numeric injury retained.')
lock_inputs=[{'face':10,'modifier':4,'dc':18},{'face':9,'modifier':4,'dc':18},{'face':1,'modifier':15,'dc':18}]
lock_results=[{'total':x['face']+x['modifier'],'degree':degree(x['face'],x['modifier'],x['dc']),'deficit':x['dc']-x['face']-x['modifier'],'failureTriggerProtected':degree(x['face'],x['modifier'],x['dc'])<2 and x['dc']-x['face']-x['modifier']<5} for x in lock_inputs]
calc('SF94-N14',['SF-13-E01','SF-13-E02'],{'checks':lock_inputs},lock_results,[{'total':14,'degree':1,'deficit':4,'failureTriggerProtected':True},{'total':13,'degree':1,'deficit':5,'failureTriggerProtected':False},{'total':16,'degree':0,'deficit':2,'failureTriggerProtected':True}],'Only the actual failed-lock trigger predicate; no disarm/touch-trigger suppression.')
aliases={'skill_feats1_master_tracker':'master_tracker'};identities={aliases.get(x,x) for x in ['master_tracker','skill_feats1_master_tracker']}
calc('SF94-N15',['SF-14-E02'],{'savedRepresentations':['master_tracker','skill_feats1_master_tracker']},{'canonicalIds':sorted(identities),'bonus':2*len(identities)},{'canonicalIds':['master_tracker'],'bonus':2},'Only the explicitly authorized alias is normalized.')
calc('SF94-N16',['SF-15-E01'],{'realHoldingEffects':['grapple-A','magic-restraint-B'],'permittedEscapeTarget':'grapple-A','paidAction':1,'paidFeatUse':1},[x for x in ['grapple-A','magic-restraint-B'] if x!='grapple-A'],['magic-restraint-B'],'Conditional allowed single-effect escape success; no permission/grant or movement generated.')
calc('SF94-N17',['SF-16-E02'],{'studyStartSeconds':0,'continuousStudySeconds':60,'independentTriggerSeconds':30},30<0+60,True,'Independent actual deadline occurs before study completion; does not infer what the rune does.')
calc('SF94-N18',['SF-17-E01'],{'normalSpeed':30,'silentFactor':'1/2','terrainCost':2,'tileFeet':5},{'silentSpeed':15,'distanceWithoutDash':str(Fraction(15,2)),'wholeTilesWithoutDash':int(Fraction(15,2)//5),'oneDashCap':2*15,'distanceWithDash':str(Fraction(30,2))},{'silentSpeed':15,'distanceWithoutDash':'15/2','wholeTilesWithoutDash':1,'oneDashCap':30,'distanceWithDash':'15'},'Exact movement-cost arithmetic; no rounding off-grid physical distance or refund by mode switch.')
calc('SF94-N19',['SF-18-E01','SF-18-E02'],{'declaredSkill':['Persuasion','Intimidation'],'realFormalExchange':True},[2 if s=='Persuasion' else 0 for s in ['Persuasion','Intimidation']],[2,0],'Conditional bonus classification preserves actual skill and channel requirements.')
calc('SF94-N20',['SF-19-E01'],{'authorizedCopyMinutes':120,'classifiedMundaneGp':40,'separateRareGp':10},{'minutes':math.ceil(Fraction(120,2)),'mundaneGp':str(Fraction(40)*Fraction(3,4)),'rareGp':10},{'minutes':60,'mundaneGp':'30','rareGp':10},'Named independently authorized copying task with actual classified quantities. No bill classification or production access inferred.')
calc('SF94-N21',['SF-19-E02'],{'timeFactors':['1/2','1/2'],'eligibleMaterialFactors':['3/4','1/2'],'indivisibleMundaneSheets':[4,1]},{'timeFactor':str(min(Fraction(1,2),Fraction(1,2))),'eligibleMaterialFactor':str(min(Fraction(3,4),Fraction(1,2))),'spellScribeSheets':[math.ceil(Fraction(v)*Fraction(3,4)) for v in [4,1]]},{'timeFactor':'1/2','eligibleMaterialFactor':'1/2','spellScribeSheets':[3,1]},'Wizard factors apply only when its actual legal found-Wizard-spell/spellbook procedure covers the same category. Sheet illustration uses the separately stated Spell Scribe three-quarter factor.')
calc('SF94-N22',['SF-19-E01'],{'classifiedAggregateMundanePurchaseCp':1249,'factor':'3/4'},{'exactCp':str(Fraction(1249)*Fraction(3,4)),'finalPurchaseCp':math.ceil(Fraction(1249)*Fraction(3,4))},{'exactCp':'3747/4','finalPurchaseCp':937},'One genuine indivisible final purchase is rounded up once; no intermediate discounts or phantom refunds.')
calc('SF94-N23',['SF-19-E02'],{'actualRankOneWrittenRitualRoute':True,'baseMinutes':480,'SpellScribeOwned':True,'unclassifiedRealBillCp':1000},{'activeMinutes':math.ceil(Fraction(480,2)),'claimedMaterialDiscountCp':0,'undiscountedBillCp':1000},{'activeMinutes':240,'claimedMaterialDiscountCp':0,'undiscountedBillCp':1000},'Existing accepted FT84-Q01 scoped comparison: independent time benefit survives unitemized material classification; actual genuine materials and all learning gates remain required.')
remaining_causes={'motion','darkness'}-{'motion'}
calc('SF94-N24',['SF-20-E01'],{'disadvantageCauses':['motion','darkness'],'removed':['motion'],'separateAdvantage':True},{'remaining':sorted(remaining_causes),'withoutAdvantage':'disadvantage' if remaining_causes else 'normal','withAdvantage':'normal' if remaining_causes else 'advantage'},{'remaining':['darkness'],'withoutAdvantage':'disadvantage','withAdvantage':'normal'},'Cause-specific removal then ordinary single advantage/disadvantage cancellation.')
calc('SF94-N25',['SF-20-E02'],{'FineMotorNumericPenalty':-1,'eligibleDisadvantageCauses':[]},-1,-1,'A numeric injury is preserved rather than reclassified as disadvantage.')
calc('SF94-N26',['SF-21-E01','SF-21-E02'],{'passive':15,'detectionDC':15,'actualAccessibleClue':True,'currentlyBlinded':True},{'meetsAccessibleDC':15>=15,'currentSightBonus':0},{'meetsAccessibleDC':True,'currentSightBonus':0},'Arithmetic/admitted-sight projection only; prior knowledge is not current sight.')
calc('SF94-N27',['SF-22-E01'],{'actualFearSaveDie':1,'ordinarySaveModifier':15,'featBonus':2,'DC':18},{'total':1+15+2,'success':1+15+2>=18},{'total':18,'success':True},'Binary actual saving throw; natural1 supplies no task downgrade.')
calc('SF94-N28',['SF-23-E01'],{'PB':3,'actualSafeForagedPortions':2,'prepMinutes':30},{'preparedPortions':min(3,2),'newPortionsCreated':0,'prepMinutes':30},{'preparedPortions':2,'newPortionsCreated':0,'prepMinutes':30},'Conditional finite portion ceiling after real safe forage; no inventory/yield engine.')
calc('SF94-N29',['SF-23-E01'],{'priorSpoilageAgeHours':2,'protectedHours':6,'elapsedSinceCompletionHours':7},2+max(0,7-6),3,'Unbreached nonstacking six-hour pause preserves prior age; hypothetical same clean stored portion.')
calc('SF94-N30',['SF-23-E02'],{'firstQualifyingConsumptionMinute':10,'secondCookConsumptionMinute':20,'durationMinutes':60,'recipientEpoch':'LR7'},{'unchangedDeadlineMinute':10+60,'maximumOneUseBonus':1},{'unchangedDeadlineMinute':70,'maximumOneUseBonus':1},'Recipient-family first-offer deadline; a second actual consumption does not refresh it.')
calc('SF94-N31',['SF-24-E01'],{'nativeAfterCritical':[10,11],'twoSeparatelyEligibleFactors':['1/2','1/2'],'externalRiderExcludedFromBase':4},[{'native':n,'increments':[math.floor(Fraction(n,2)),math.floor(Fraction(n,2))],'beforeDefensesWithSeparateRider':n+2*math.floor(Fraction(n,2))+4} for n in [10,11]],[{'native':10,'increments':[5,5],'beforeDefensesWithSeparateRider':24},{'native':11,'increments':[5,5],'beforeDefensesWithSeparateRider':25}],'Each separate eligible feat floors its own increment from the same actual native base; external4 is never compounded.')
calc('SF94-N32',['SF-24-E02'],{'preControlSpeed':30,'hostileHalf':'1/2','hostileFlatPenalty':10},{'halfCandidate':15,'flatCandidate':20,'selected':min(15,20)},{'halfCandidate':15,'flatCandidate':20,'selected':15},'Strongest hostile reduction from one pre-control base, with both source histories/deadlines retained.')
calc('SF94-N33',['SF-25-E01','SF-25-E02'],{'actualCRs':['1','1/4'],'sameFeatBriefingBonuses':[2,2]}, {'readDCs':[math.ceil(10+Fraction(v)) for v in ['1','1/4']],'sameFeatBonus':max(2,2)},{'readDCs':[11,11],'sameFeatBonus':2},'CR arithmetic and same-source overlap; no unknown CR or creature generated.')
calc('SF94-N34',['SF-25-E02'],{'callSeconds':0,'taskMaximumSeconds':60,'overallMaximumSeconds':600,'hypotheticalLegalArrivalSeconds':[60,590]},[min(arrival+60,600) for arrival in [60,590]],[120,600],'Conditional feasible arrivals only; actual movement/route/agency remain unexecuted. A sealed route supplies no arrival.')

paths=[I/'candidate.json',I/'example_dispositions.json',I/'shared_rules.json',I/'fex_dispositions.json',R/'data/director/skill_feat_operating_proposal_internal.json',D/'data/director/feat_candidates/exact_01/candidate.json',D/'data/public/feat_candidates/exact_01/candidate.json',D/'docs/feats/exact-candidate-01/SKILL.md',P/'SELECTED_PROCEDURES.json',P/'QUESTION_DISPOSITIONS.json',A/'FEAT335_WORK_COMPOSITIONS_INDEPENDENT_SEMANTIC_REVIEW_88.json',A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md',R/'docs/mechanics/HEALING_DEATH_PLAYTEST.md',R/'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md',R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',R/'data/public/class_playtests/wizard.json',A/'FEAT335_HEALING_COMPOSITIONS_89.json',A/'FEAT335_RESOLUTION_CASES_85.json',A/'FEAT335_TIME_PROVISIONS_CASES_83.json']
source_bytes={p.relative_to(G).as_posix():p.read_bytes() for p in paths};proposal=j(R/'data/director/skill_feat_operating_proposal_internal.json')
for x in cases:
 value=proposal
 for part in x['sourcePointer'].split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
 ck(x['id']+' original source exact',value==x['original'])
public=j(D/'data/public/feat_candidates/exact_01/candidate.json');pr={r['id']:r for r in public['feats']};chapter=(D/'docs/feats/exact-candidate-01/SKILL.md').read_text(encoding='utf-8-sig')
for r in selected:
 ck(r['id']+' complete derived public mirror exact',r['operationalRules']==pr[r['id']]['operationalRules'] and r['workedCases']==pr[r['id']]['workedCases'])
 ck(r['id']+' whole derived chapter procedure/examples present',r['operationalRules'] in chapter and all(s in chapter for s in r['workedCases']))
selected_scribe=next(x for x in j(P/'SELECTED_PROCEDURES.json')['procedures'] if x['id']=='spell_scribe')
ck('Exact previously accepted complete Spell Scribe successor',records['spell_scribe']['operationalRules']==selected_scribe['after'] and before_records['spell_scribe']['operationalRules']==selected_scribe['before'])
ck('No original skill case changed by FT84',all(records[r['id']]['workedCases']==before_records[r['id']]['workedCases'] for r in selected))
field_medic=next(r for r in before['unchangedReviewedFeats'] if r['id']=='field_medic');wizard=j(R/'data/public/class_playtests/wizard.json');scribing=next(x for x in wizard['cards'] if x['id']=='wizard.base.spell-scribing');linked={x for r in calcs for x in r['originalCaseIds']}
report={'id':'FEAT335-SKILL-ORIGINAL-CASEBOOK-REVIEW-94','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'25_FULL_PROCEDURES_AND50_ORIGINAL_POSITIONS_REVIEWED_WITH34_BOUNDED_CALCULATIONS_PARENT_PENDING','scope':'Full skill-cohort authored semantic review against exact current source/shared directions and the independently accepted FT84 Spell Scribe successor in isolated candidate92. Original50 positions and their full corrected expected outcomes remain intact.','sourceBindings':[info(p) for p in paths],'completeSelectedRecords':selected,'originalSpellScribeRecord':before_records['spell_scribe'],'completeReviewedFieldMedicCounterpart':field_medic,'completeWizardScribingCounterpart':scribing,'originalCaseReviews':reviews,'additionalBoundaryReviews':[],'numericAndStateCalculations':calcs,'coverage':{'cohort':'skill','fullFeatProcedures':25,'originalCasePositions':50,'additionalBoundaries':0,'boundedCalculations':34,'originalCasesWithNumericalProjection':sum(x['id'] in linked for x in cases)},'reviewFindings':['No conflicting expected outcome identified among the50 complete original cases under their exact qualified procedures.','The original two Spell Scribe examples remain valid. The second is conditional on an actually eligible Wizard spellbook copying route; it does not make every Wizard-owned ritual-learning transaction a Wizard-class copy. The accepted FT84 written-ritual half-time/bill separation is carried forward exactly.','Anatomy Lore uses the selected complete corrections: eligible spell attacks remain allowed, percentage feats compute independent native-base increments, and hostile slows use strongest-result arbitration.','Field Surgeon has a genuine stabilization trigger and recipient LR-family offer lock. Field Medic requires its own actual kit-source event, and temporary HP does not wake a living Stable0 recipient.','Historical descriptions/legacy effects and future-proposal phrases remain preserved as evidence; exact current effect/shared/FEX/FT84 text defines the reviewed candidate.'],'remainingScope':['Actual acquisition histories, legal class options, creature/body/route records, channels, tasks and native event permissions remain conditional premises rather than runtime fixtures.','No complete game scheduler, world model, save/reload pipeline, rune resolver, tracking engine or finite production engine is executed here.','The full parent335 exact submission, remaining original cohorts and FA boundaries, copied-feat/native/gadget integrations and all earlier holds remain.','This review adds no new mechanic, stronger information claim, lore or cosmology. No human gameplay or numerical balance approval.'],'checks':checks,'passed':len(checks),'failed':0,'newMechanicsAuthored':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproved':False,'cosmologyDecisions':0,'actuallySentToGpt':False}
payload=enc(report);script=Path(__file__).read_bytes();ROOT.mkdir()
for rel,raw in source_bytes.items():
 target=ROOT/'sources'/rel;target.parent.mkdir(parents=True,exist_ok=True)
 with target.open('xb') as f:f.write(raw)
for p,b in [(SAVED,script),(ROOT/Path(__file__).name,script),(OUT,payload),(ROOT/'REVIEW.json',payload)]:
 with p.open('xb') as f:f.write(b)
with (ROOT/'README.txt').open('xb') as f:f.write(b'Full skill-cohort casebook review94:25 complete procedures,50 original positions and34 bounded reference calculations. Complete source/expected values and individual semantic rationales are preserved. FT84 Spell Scribe successor is from the isolated derived92 candidate and remains unapplied. This is not runtime execution or parent335 acceptance. No supplied program needs execution.\n')
files=sorted(p for p in ROOT.rglob('*') if p.is_file());manifest={'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
with (ROOT/'MANIFEST.json').open('xb') as f:f.write(enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert all(len(z.read(x['path']))==x['bytes'] and sha(z.read(x['path']))==x['sha256'] for x in manifest['files'])
assert all((G/rel).read_bytes()==b for rel,b in source_bytes.items())
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'coverage':report['coverage'],'checks':len(checks),'failed':0,'archiveMembers':len(manifest['files'])+1},indent=2))
