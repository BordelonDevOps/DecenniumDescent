"""One-shot full stated-case review of MX01-20; arithmetic projections, not runtime."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib, json, zipfile

G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
I=R/'data/director/feat_candidates/exact_01'; D=A/'feat335-ft84-derived-review-92/after/DescentReviewChanges/ReviewBible'
ROOT=A/'feat335-magic-extended-part01-102'; OUT=A/'FEAT335_MAGIC_EXTENDED_PART01_CASEBOOK_REVIEW_102.json'; ZIP=A/'DD_Feat335_Magic_Extended_Part01_102.zip'; SAVED=A/Path(__file__).name
for p in (ROOT,OUT,ZIP,SAVED): assert not p.exists(),str(p)
def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes(); return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(name,result):
 checks.append({'check':name,'pass':bool(result)}); assert result,name

current=j(I/'candidate.json'); originals={r['id']:r for r in current['records']}
selected=[r for r in j(D/'data/director/feat_candidates/exact_01/candidate.json')['records'] if r['cohort']=='magic_extended'][:20]
records={r['id']:r for r in selected}; cases=[r for r in j(I/'example_dispositions.json')['cases'] if r['featId'] in records]; boundaries=[r for r in j(I/'additional_boundary_expectations.json')['cases'] if r['featId'] in records]
proposal_path=R/'data/director/magic_extended_feat_operating_proposal_internal.json'; proposal=j(proposal_path)
ck('Exact MX01-20,40 originals,2 boundaries',len(selected)==20 and [r['questionId'] for r in selected]==['MX-'+str(i).zfill(2) for i in range(1,21)] and len(cases)==40 and {r['id'] for r in boundaries}=={'FA-04','FA-16'})
public={r['id']:r for r in j(R/'data/public/feat_candidates/exact_01/candidate.json')['feats']}; dpublic={r['id']:r for r in j(D/'data/public/feat_candidates/exact_01/candidate.json')['feats']}
chapter_path=R/'docs/feats/exact-candidate-01/MAGIC_EXTENDED.md'; chapter=chapter_path.read_text(encoding='utf-8-sig')
for r in selected:
 fid=r['id']; src=proposal['records'][int(r['questionId'][-2:])-1]
 ck(fid+' unchanged full derived record',r==originals[fid])
 ck(fid+' complete original object',r['sourceObject']==src['sourceObject']==r['sourceDirection']['originalSourceObject'])
 ck(fid+' original question preserved',r['originalQuestion']==src['originalQuestion'])
 ck(fid+' exact proposal hash',r['sourceDirection']['sourceFileSha256']==info(proposal_path)['sha256'])
 ck(fid+' full current/public/derived procedure and cases',all(r[k]==public[fid][k]==dpublic[fid][k] for k in ('operationalRules','workedCases','payloadOperational')))
 ck(fid+' complete manuscript procedure',r['operationalRules'] in chapter)
 ck(fid+' source records still inactive',not r['selectionEnabled'] and not r['exactApproved'] and not r['runtimeApproved'])
for case in cases:
 ix=int(case['questionId'][-2:])-1; ci=int(case['id'][-2:])-1
 ck(case['id']+' full original source position',proposal['records'][ix]['workedCases'][ci]==case['original'])
 ck(case['id']+' current exact expectation',records[case['featId']]['workedCases'][ci]==case['completeExpectedOutcome'])

notes={
'MX-01':[
'With the actual non-feat AC already resolved to14 and only Arcane Armor eligible, the qualifying on-cast Reaction faces15. Its historical stronger-same-stat caveat does not override final FS03: another distinct eligible flat feat adds; duplicate Arcane Armor does not. Casting/continuing-concentration trigger and an actual attack/save against the holder are necessary.',
'An ordinary attack during concentration has no qualifying Reaction trigger and gets no modifier. Counterspell is the countering caster\'s task check, so neither this feat\'s AC nor save bonus changes that check. No general5% resistance is restored.'],
'MX-02':[
'One actual prepared Wizard-rank2 matrix may become another already owned/book-eligible Wizard-rank2 matrix on a beneficial Short Rest. Capacity and other matrices stay fixed; ongoing lawful effect/concentration retains its original deadline. This is one feat exchange per rest across classes, separate from Wizard\'s own acquired substitution feature.',
'A second-class rank2 record does not prove Wizard book, school, level or preparation eligibility. No new spell/list/capacity or free rest appears; the printed INT15 acquisition condition remains even though not repeated in the operational paragraph.'],
'MX-03':[
'Warrior7 without another actual pool has0RP; the3RP Action cannot commit. Legal feat acquisition and a permanently selected DC ability do not supply spellcasting or RP.',
'One native3d6 result11 gives11 on failed STR save and floor(11/2)=5 on success before defenses. A failed target pushes only over actual free-body clearance, at most10ft; a3ft clearance limits to3, not through the wall. The technique is magical but not a spell, and self has no away-from-self direction.'],
'MX-04':[
'For completed personal rank3 with5 actual unrefunded paidRP, min(3,5,headroom,5) returns3. A separately lawful earlier4RP refund leaves only1 recoverable. The same expense cannot fund Arcane Resonance again; earlier-refund permission is a premise, not granted by this example.',
'A charge/free-price cast with0 personally paidRP returns0 despite rank3. Declining computed0 spends no LR use; independent actual surcharge, if any, must have its own payment receipt. Countered casts, copied casts and Ready release do not open another refund.'],
'MX-05':[
'The supplied PB3/headroom2 arithmetic permits N2 and costs4 normalHP. Actual total-level9 acquisition, actual PB, pool and available BA remain required separately; the example is not proof of a legal level/PB character build. Pay before restoration and resolve Wound/death/concentration; surviving capacity caps the award.',
'At4 normalHP the4HP cost fails the leave-at-least1 preflight even with20tempHP; no BA/use is spent. TempHP, resistance, transfer or a floor cannot fund this cost. Fatal Wound consequences can still kill a payer whose immediate HP payment left positiveHP.'],
'MX-06':[
'For an actual rank2 spell, legal DC mode costs4 normalHP and raises14 to15 for every directly generated save of this same cast, including valid repeats. Existing concentration faces cost damage before displacement; use/payment remains committed if interruption or cost consequences abort the cast.',
'A flat-only damage formula supplies no native die for die mode. DC mode is useful only where the source has an actual saving throw; it invents none. Added die selects one native immediate packet, or one true shared area roll, before critical/save/defense. Rank0 pays0HP but still spends the finite use.'],
'MX-07':[
'Given an actually sourced mandatory later-turn Action upkeep costing2RP, one available BA and the finite SR use can replace that Action once while still paying2RP. Concentration and the original deadline persist; the quoted upkeep is a conditional premise, not a newly authored spell.',
'Optional summoned offense is not required maintenance by name. This supplies no extra command or offense budget and compresses neither initial casting, Ready setup nor a ritual. Exact combined mandatory-upkeep payloads retain their one printed occurrence.'],
'MX-08':[
'Add2 only to an actual CON concentration save, including legally held Ready or qualifying nonspell concentration. A separate eligible flat feat adds under FS03, class bonuses compare in their own family, and advantage/disadvantage cancels normally. One damage packet is not split into saves per type.',
'Incapacitation\'s automatic concentration loss creates no save to improve. Wound, death, unrelatedCON and special non-CON checks do not acquire this bonus, and the feat grants no zeroHP permission.'],
'MX-09':[
'Against actual rank3, Counterspell taskDC=10+2*3=16. Existing ability+PB5 plus selected active feat2 gives7; task degrees and natural shifts still govern. The historical+4 description is preserved inactive, and no source/save access is granted.',
'Mystic Focus modifies spell attacks, not this task. The hypothetical alternative+1counter-saveDC applies only to a separately operative source actually using such a save; it cannot create a save or penetration check for ordinary/Mage/Wizard Counterspell.'],
'MX-10':[
'Actual ordinary Dispel Magic selects one individually perceptible eligible rank2 ongoing effect within60ft/LoE and ends it automatically. No random selection, check or+1roll is created; other two effects remain subject only to real ending dependencies.',
'Generating rank5 lies beyond ordinary rank0-3 scope. ExtraRP, the feat or a second target from a separately adopted Dispel Mastery cannot permit it or invent a harder check. Permanent items/class engines remain outside this spell.'],
'MX-11':[
'After a completed rank1-3 initial payload, native11 yields a snapshotted5 for the next future regular start. Recheck original recipients, fixed origin/area and concentration, then fresh original save/attack and defenses. A half-success branch on5 becomes2. This is not a new cast, proc, critical-dice roll, target rescan or refund.',
'Summoned bodyHP, attacks and turns are outside the finite numerical component menu. Echoes cannot create bodies/resources/action grants/copy chains. Ready preparation waits for actual release; flat bonus uses the original family and bounded deadline, and invalid echoes expire without refund.'],
'MX-12':[
'An eligible ranked actual quoted stage2 becomes1 before final Influence. Commit both the numbered-round claim and one PB-limited use with the cast, even if later countered. Discounts, printed independent costs and armor/strain precede this stage as specified; it is not a new base-rank price.',
'A free route with only1 independentRP cost cannot reduce and spends no use. Genuine0 remains0 without inventing1RP; extra turns do not reset the round claim, and PB maximum growth adds no current uses.'],
'MX-13':[
'A successful real save against an original meaningful hostile spell can qualify even after5 positive damage. Complete its consequences first, then actual Reaction/use and headroom permit at most1RP; repeat ticks of that cast do not repeat the award.',
'A legal missed hostile spell attack can satisfy no-damage, but friendly/harmless/self/farming events cannot. TempHP absorption is actual damage; full prevention can qualify only if the source\'s no-resource flags permit it. Failed nondamaging control qualifies only when the survivor can actually react.'],
'MX-14':[
'After a real failed displacement-determining save and before consequences, the available LR use changes it to the source\'s success result without an Action/Reaction. Its ordinary advantage can cancel disadvantage; success may still retain separately specified damage.',
'A save-less automatic displacement has no eligible roll or failure to replace. The feat grants neither general immunity nor destination knowledge/cosmology and does not override explicit no-replacement rules.'],
'MX-15':[
'An earlier ranked cast in the same genuine actual turn blocks Flash Cast even for rank0. Preflight fails before BA/use spend. Earlier/later on-turn Reaction casts count; extra Actions are not new turns.',
'A committed rank2 Flash Cast can coexist with a legal Action cantrip, but bars on-turn ranked Counterspell even if Flash Cast was countered. Costs/components/concentration/history remain ordinary; a genuine later extra turn changes the turn prohibition only, not LR uses or regular budgets. Paid feat-copy casts are casts under FS08; secondary echo/Ready release is not.'],
'MX-16':[
'At the next numbered boundary restore prior temporary permutations, apply C\'s single baseline swap A,B,C to A,C,B, then new Future Echo permutations. C gains no present-round turn; all retained slots and preexisting virtual deadlines remain. Incapacitation alone does not remove C.',
'Three actual same-school Divination casts refresh the one-hour+2 deadline and queue only one move for this boundary. Wrong-school access is not Divination by identity union. A departed participant without a slot loses the pending move; repeated callbacks cannot repeat a swap.'],
'MX-17':[
'Only a real source whose illusion globally ends from an attack/interaction supports this delay. It stays nonphysical until the current actual turn end (canonical six-second window outside initiative), and independent concentration/expiry/dispel ending still wins. No such source is authenticated by this conditional example.',
'Silent Image physical passage gives direct proof immediately, with no saving throw or restored belief. Current Silent Image and Minor Illusion do not globally end from ordinary interaction, so this feat usually does not trigger. Investigation remains the source\'s actual Action check.'],
'MX-18':[
'A finite nonconcentration60-second duration extends to66 once, not72 or an extra20%. Earlier discharge/destruction still ends it. Ready extends the payload at release, not its held deadline.',
'A source with a fixed total3 pulses remains3 regardless of extra duration. A genuinely duration-driven tick may occur if naturally reached; the feat supplies no fixed count, stock, charge, concentration extension or separate resurrection window.'],
'MX-19':[
'A directly printed repeated spellWISsave gains2. A distinct eligible save feat adds, ordinary family comparisons remain, and CON13 is only an acquisition gate.',
'Concentration after spell damage is a shared-rules consequence; only Concentrated Will\'s own scope supplies its2. Magical Fortitude adds nothing to that concentration, Wound or ordinary death save, or to a magical nonspell technique merely by name.'],
'MX-20':[
'Two owners against the same livingRP4 recipient in one numbered round share one Mana Burn claim: first actual failed native-damage save removes1 to3; second removes0. The recipient claim survives resource changes and callback retries; it never transfersRP to the caster.',
'Damage immunity does not erase the failed save governing a native damage component, so a surviving actual pool can lose1. NoRP means no substitute loss from charges/RC/slots; a zeroRP pool still consumes the claim, preventing later same-round farming after refill. Copy/echo/reflection gives no fresh proc.']}
reviews=[]
for c in cases:
 reviews.append({'id':c['id'],'featId':c['featId'],'completeOriginalDisposition':c,'reviewResult':'CONSISTENT_UNDER_EXACT_STATED_PREMISES_AND_CURRENT_SHARED_RULES','reasoning':notes[c['questionId']][int(c['id'][-2:])-1],'qualification':'Full stated-case semantic review, not actual-world acquisition/source authentication, full engine execution or balance approval. Unspecified lawful source/geometry/resource premises remain conditional.','runtimeExecuted':False,'canonicalApplied':False})
boundary_notes={
'FA-04':'Two distinct eligible feat2 values add4; class1/2 in one comparison family yields2; total6 plus actual ability/PB once. Real acquisition and source-specific concentration predicates remain necessary.',
'FA-16':'Actual Mage3RPmax8/current7 has headroom1; Dragoon8max7 and Warrior7max0 are verified against current full class tables. Mage3 alone does not satisfy Arcane Recall\'s total-level10 prerequisite. This boundary is capacity arithmetic unless an independently legal total-level10 acquisition/cast/refund history is also supplied; no multiclass RP law or levels are invented.'}
boundary_reviews=[{'id':b['id'],'completeOriginalDisposition':b,'reviewResult':'CONSISTENT_CAPACITY_OR_FAMILY_BOUNDARY_WITH_ACQUISITION_QUALIFICATION','reasoning':boundary_notes[b['id']],'runtimeExecuted':False} for b in boundaries]

calcs=[]
def calc(key,ids,inputs,actual,expected,scope):
 ck(key+' bounded expected result',actual==expected)
 calcs.append({'id':key,'originalCaseIds':ids,'inputs':inputs,'calculatedResult':actual,'expectedResult':expected,'scope':scope+' TEST_ONLY conditional projection, not an executed game engine or campaign event.','runtimeExecuted':False})
def mids(i):return ['MX-'+str(i).zfill(2)+'-E01','MX-'+str(i).zfill(2)+'-E02']
calc('MX102-N01',mids(1),{'resolvedNonFeatAC':14,'armor':1,'otherDistinctEligibleFeat':2},[14+1,14+1+2,14],[15,17,14],'Qualifying Reaction / distinct added feat / unrelated attack branches; duplicate Armor never adds twice.')
matrix=['TEST_ONLY_A_rank2','TEST_ONLY_C_rank1']; after=matrix.copy();after[0]='TEST_ONLY_B_rank2'
calc('MX102-N02',mids(2),{'prepared':matrix,'BAlreadyWizardBookEligible':True,'otherClassOnly':False},[after,len(after)==len(matrix),False],[['TEST_ONLY_B_rank2','TEST_ONLY_C_rank1'],True,False],'One beneficial-rest matrix replacement. Existing effect record and deadline are retained, not recreated; symbols assert no catalog grant.')
roll=sum([2,4,5]);calc('MX102-N03',mids(3),{'faces':[2,4,5],'cost':3,'warriorPool':0,'freeBodyClearanceFeet':3},[0>=3,roll,roll//2,min(10,3)],[False,11,5,3],'Explicit actual free-body clearance, not a guessed wall-to-center distance. No generic geometry runtime.')
calc('MX102-N04',mids(4),{'rank':3,'paid':5,'headroom':8,'previousRefund':4,'freePaid':0},[min(3,5,8,5),min(3,5,8,5-4),min(3,5,8,0)],[3,1,0],'Separate original receipt cases; earlier refund must have an actual lawful source, not supplied here.')
calc('MX102-N05',mids(5),{'PBParameter':3,'headroom':2,'HP':9,'temp':20,'maxHP':30,'N':2},[min(3,2),9-2*2,20,2,4-2*2>=1],[2,5,20,2,False],'Nonlethal branch with no half-max Wound; actual acquisition/PB/source legality remains separate from example arithmetic.')
cost=6;wound_due=2*cost>=12; wound_total=1+0-3;fatal=wound_due and wound_total<max(10,cost//2)
calc('MX102-N06',['MX-05-E01','MX-06-E01'],{'beforeHP':12,'maxHP':12,'preWounds':3,'cost':6,'woundD20':1,'CON':0},[12-cost,wound_due,wound_total,fatal,0 if fatal else 3],[6,True,-2,True,0],'Actual6 normal-HP cost leaves6 but half-max triggers one fatal failed Wound at3 existing Wounds. No RP award/dependent unfinished cast survives actual death; no survival replacement is stipulated.')
calc('MX102-N07',mids(6),{'rank':2,'DC':14,'HP':15,'nativeDiceFaces':[2,3],'addedDie':4},[2*2,15-4,14+1,sum([2,3,4]),2*len([2,3,4]),0>0],[4,11,15,9,6,False],'DC and added-die alternatives are separate branches. Flat-only damage has0 native dice; actual critical doubles3 dice to6, not this already rolled total.')
calc('MX102-N08',['MX-06-E02'],{'rank0':0,'useBefore':1},[2*0,1-1],[0,0],'Legal cantrip option still consumes finite SR use despite0HP cost; no free repeated use.')
calc('MX102-N09',mids(7),{'Action':1,'BA':1,'RP':5,'requiredUpkeepRP':2,'uses':1},[1,1-1,5-2,1-1,False],[1,0,3,0,False],'One actual mandatory-upkeep Action is replaced by BA; optional attack command remains ineligible. No source spell or extra budget invented.')
calc('MX102-N10',mids(8)+['FA-04'],{'distinctFeats':[2,2],'oneClassFamily':[1,2],'CON':2,'PBIfProficient':3,'advantageD20':[3,11],'DC':15},[sum([2,2])+max([1,2]),max([3,11])+2+3+sum([2,2])+max([1,2]),False],[6,22,False],'Conditional qualifying actualCONsave; incapacity branch has no roll, not an automatic success.')
def task_success(face,mod,dc):
 total=face+mod; degree=3 if total>=dc+10 else 2 if total>=dc else 0 if total<=dc-10 else 1
 degree=max(0,min(3,degree+(1 if face==20 else -1 if face==1 else 0)))
 return degree>=2
calc('MX102-N11',mids(9),{'triggerRank':3,'abilityPlusPB':5,'feat':2,'ordinaryFace':9},[10+2*3,5+2,task_success(9,7,16),task_success(1,15,16),task_success(20,-7,16)],[16,7,True,False,True],'Actual task natural shifts: natural1 total16 degrades success; natural20 total13 improves failure. Mystic Focus contributes0 to task.')
calc('MX102-N12',mids(10),{'effects':[2,3,5],'selectedRank':2,'ceiling':3},[0<=2<=3,0<=5<=3,0,2],[True,False,0,2],'One individually perceptible otherwise legal effect ends automatically;0rolls,2other effects remain absent an actual ending dependency.')
calc('MX102-N13',mids(11),{'native':11,'originalRecipients':['A','B'],'stillLegal':['A'],'freshASaveSuccess':True},[11//2,(11//2)//2,['A'],0],[5,2,['A'],0],'A gets fresh native half-success2 before defenses; B no longer legal gets no echo. Summon HP/body duplication count0.')
calc('MX102-N14',mids(12),{'preInfluencePrices':[2,1,0],'usesBefore':3},[max(1,2-1),1,0,3-1,3,3],[1,1,0,2,3,3],'Only price2 genuinely reduces and spends; no unspecified Influence factor invented. Independent stage1/0 cases keep uses.')
def sink(saved,damage,hostile,able,headroom,spent=False,no_resource=False):return int((saved or damage==0) and hostile and able and headroom>0 and not spent and not no_resource)
calc('MX102-N15',mids(13),{'saveSuccessWithDamage':5,'tempAbsorbed':5,'normalHpLost':0},[sink(True,5,True,True,2),sink(False,0,True,True,2),sink(False,0,False,True,2),sink(False,5,True,True,2),sink(False,0,True,False,2),sink(False,0,True,True,2,True),sink(False,0,True,True,2,False,True)],[1,1,0,0,0,0,0],'Saved damage;miss;friendly;temp-only damage;incapacitated control;already used cast;source no-resource branches. Each1requires actualReaction/use and only1RP restoration.')
calc('MX102-N16',mids(14),{'actualEligibleSave':True,'failed':True,'uses':1,'saveLess':True},[1-1,True,False],[0,True,False],'Post-failure replacement preserves actual source success payload; no-save branch creates no opportunity and spends nothing.')
calc('MX102-N17',mids(15),{'earlierRankedCasts':1,'flashRank0':True,'rankedFlashCommitted':True},[1==0,False,True,False],[False,False,True,False],'Earlier ranked cast rejects Flash including cantrip; after rank2 Flash a legal Action cantrip allowed, on-turn rankedCounterspell barred. Listed secondFalse is new-use available after consuming this LR use.')
order=['A','B','C'];idx=order.index('C');order[idx-1],order[idx]=order[idx],order[idx-1]
calc('MX102-N18',mids(16),{'baseline':['A','B','C'],'CQueuedCasts':3},[order,len(set(order)),min(1,3),0],[['A','C','B'],3,1,0],'One baseline advance at boundary;3slots conserved,0new turns. Restore temporary permutation before this operation.')
calc('MX102-N19',mids(17),{'sourceEndsGloballyOnHit':True,'currentTurnEnd':42,'parentExpiry':40,'silentImagePhysicalInteraction':True},[min(42,40),False,0],[40,False,0],'Independent earlier expiry40 defeats deferred42; SilentImage is already known without a new save and does not globally end on passage.')
calc('MX102-N20',mids(18),{'durationSeconds':60,'dischargeAt':32,'fixedPulseCount':3},[60+6,min(60+6,32),3],[66,32,3],'Finite original duration extension; independent discharge and fixed-count pulses conserved. No concentration-duration extension.')
calc('MX102-N21',mids(19),{'directSpellSaveBonus':2,'distinctEligibleFeat':2,'ordinaryConcentrationFromDamage':True},[2+2,0,2],[4,0,2],'Direct spell save may add4; MagicalFortitude contributes0 to ordinary concentration, ConcentratedWill separately2 if owned/eligible.')
rp=4; consumed=False; losses=[]
for owner in ['A','B']:
 loss=0 if consumed else min(1,rp);rp-=loss;consumed=True;losses.append(loss)
calc('MX102-N22',mids(20),{'targetRP':4,'qualifyingOwners':['A','B'],'sameRound':True},[losses,rp,True],[ [1,0],3,True],'One recipient-wide claim. Immunity does not undo native-damage failed-save qualification; RP-less branch has nopool and no transfer.')
zero_rp=0; first_loss=min(1,zero_rp); zero_claim=True; later_refill=2;later_loss=0 if zero_claim else min(1,later_refill)
calc('MX102-N23',['MX-20-E01','MX-20-E02'],{'zeroRPBefore':0,'laterLawfulRefill':2},[first_loss,zero_claim,later_refill-later_loss],[0,True,2],'ZeroRP realpool consumes claim; independently lawful later refill is not removed again this same numbered round.')
classes={n:j(R/('data/public/class_playtests/'+n+'.json')) for n in ['mage','dragoon','warrior','wizard']}
mage_max=classes['mage']['rpByClassLevel'][2];dragoon_max=classes['dragoon']['rpByClassLevel'][7];warrior_max=classes['warrior']['rpByClassLevel'][6]
calc('MX102-N24',['FA-16'],{'MageClassLevel':3,'MageCurrentRP':7,'DragoonClassLevel':8,'WarriorClassLevel':7},[mage_max,min(5,max(0,mage_max-7)),dragoon_max,warrior_max,warrior_max>=3],[8,1,7,0,False],'Actual class tables. Capacity-only boundary, not standaloneMage3 eligibility for level10 ArcaneRecall, not an invented multiclass pool formula.')

catalog=j(R/'data/public/spell_playtests/catalog.json'); deps=[s for s in catalog['spells'] if s['id'] in {'counterspell','dispel-magic','future-echo','minor-illusion','silent-image'}]
ck('Five exact named dependency records retained',len(deps)==5 and all(s['operational'] for s in deps))
ck('All40 originals have individually authored notes',len(reviews)==40 and len({r['id'] for r in reviews})==40)
linked={i for c in calcs for i in c['originalCaseIds']};ck('All40 original positions and2 boundaries linked to bounded projections',linked=={c['id'] for c in cases}|{b['id'] for b in boundaries})
paths=[I/'candidate.json',I/'example_dispositions.json',I/'additional_boundary_expectations.json',I/'shared_rules.json',I/'supplements.json',I/'fex_dispositions.json',proposal_path,R/'data/public/feat_candidates/exact_01/candidate.json',D/'data/director/feat_candidates/exact_01/candidate.json',D/'data/public/feat_candidates/exact_01/candidate.json',chapter_path,D/'docs/feats/exact-candidate-01/MAGIC_EXTENDED.md',R/'docs/feats/exact-candidate-01/source-audit/MAGIC_EXTENDED.md',R/'data/public/spell_playtests/catalog.json']
paths += [R/('docs/mechanics/'+n+'.md') for n in ['CORE_RESOLUTION_PLAYTEST','COMBAT_ACTION_PLAYTEST','CONDITIONS_PLAYTEST','MAXIMUM_HP_PLAYTEST','BODY_EQUIPMENT_PLAYTEST','SPELL_INTEGRATION_RULES','CLASS_PLAYTEST_RULES','HEALING_DEATH_PLAYTEST']]
paths += [R/('data/public/class_playtests/'+n+'.json') for n in classes]
paths += [A/'FEAT335_FT84_DERIVED_MIRROR_RECONCILIATION_92.json',A/'FEAT335_MAGIC_CORE_ORIGINAL_CASEBOOK_REVIEW_100.json']
source_data={p:p.read_bytes() for p in paths};ck('Unique existing full source paths',len(paths)==len(set(paths)) and all(source_data.values()))
report={'id':'FEAT335-MAGIC-EXTENDED-PART01-102','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'MX01_20_COMPLETE_STATED_CASE_REVIEW_COHORT_AND_PARENT_REMAIN_PENDING','scope':'First20 of58 extended-magic procedures;40 of116 original examples plusFA04/16. Full final cohort remains required. No new mechanics or source promotion.','sourceBindings':[info(p) for p in paths],'completeSelectedRecords':selected,'completeOriginalProposalRecords':proposal['records'][:20],'completeOriginalSharedProposal':proposal['sharedProposal'],'completeControllingSharedRules':j(I/'shared_rules.json'),'completeNamedSpellDependencies':deps,'completeClassDependencies':classes,'originalCaseReviews':reviews,'additionalBoundaryReviews':boundary_reviews,'numericAndStateCalculations':calcs,'coverage':{'cohort':'magic_extended','part':'MX01-MX20','fullFeatRecords':20,'cohortTotalRecords':58,'originalCasePositions':40,'cohortTotalOriginalCases':116,'additionalBoundaries':2,'boundedCalculations':len(calcs)},'reviewFindings':['FS03 later distinct-feat addition controls over Arcane Armor historical stronger-same-stat example caveat. All original bytes preserved; no generic strongest-feat rule restored.','FA16 exact source pools are8/7/0. It is a capacity boundary, not proof Mage3 owns level10 Arcane Recall; actual total-level acquisition and actual pool calculation remain mandatory.','Arcane Transfusion PB3 example is arithmetic under supplied parameters, not authenticated acquisition/level/PB evidence. Cost damage bypasses tempHP but retains Wound/concentration/death consequences, including fatal Wound before RP restoration.','Counterspell remains a task with natural shifts and active+2; ordinary DispelMagic automatic rank0-3 ending has no check.','Ready preparation/release, extra actual turns, global rounds, fixed original duration markers, and current FutureEcho restoration remain distinct.','Echo secondary results are not casts; EnergySink, ManaBurn and paid-cast refunds preserve source/cast/recipient causal claims. No actual world witness or runtime implementation is supplied.'],'remainingScope':['Complete remaining38 extended-magic records/76 originals and its5 additional boundaries, then22 heritage/mutation records44 originals4 boundaries.','Parent335 full assembly and actual acquisition/copy/mental-predicate obligations, whole joint review, runtime, gameplay, balance, cosmology and release remain open.','BestiaryRecoveryPart01 is separately dispatched; no bestiary result accepted by this feat review.'],'checks':checks,'passed':len(checks),'failed':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0,'newMechanicsAuthored':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'actuallySentToGpt':False}
ROOT.mkdir(); put(SAVED,Path(__file__).read_bytes());put(OUT,enc(report));put(ROOT/'REVIEW.json',enc(report));put(ROOT/'review_magic_extended_part01_102.py',Path(__file__).read_bytes())
for p,b in source_data.items():put(ROOT/'sources'/p.relative_to(G),b)
put(ROOT/'README.txt',b'Complete bounded stated-case review MX01-20. All source files are retained under sources/. Original and final source records remain distinct. Review.json records individual notes and conditional arithmetic; no runtime implementation or whole-cohort acceptance. Do not run supplied scripts.\n')
members=sorted(p for p in ROOT.rglob('*') if p.is_file()); manifest={'id':'MX102-MANIFEST','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in members]};put(ROOT/'MANIFEST.json',enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(manifest['files'])+1
 for row in manifest['files']:
  b=z.read(row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
 assert all(p.read_bytes()==b for p,b in source_data.items())
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'coverage':report['coverage'],'passed':len(checks),'failed':0,'fullSourceFiles':len(paths),'archiveMembers':len(manifest['files'])+1},indent=2))
