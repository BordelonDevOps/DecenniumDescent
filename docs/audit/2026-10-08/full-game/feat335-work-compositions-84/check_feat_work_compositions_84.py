"""Source-bound specification diagnostics; no project or downloaded module imports.

All actual access, paid feat/class ownership and worksite facts are explicit
conditional fixture inputs. This is not a complete character or world engine.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
from math import ceil
import hashlib, json, re, zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G/'DescentReviewChanges/ReviewBible'
A = G/'docs/audit/2026-10-08/full-game'
I = R/'data/director/feat_candidates/exact_01'
ROOT = A/'feat335-work-compositions-84'
OUT = A/'FEAT335_WORK_COMPOSITIONS_84.json'
CHECK = A/'FEAT335_WORK_COMPOSITIONS_CHECK_84.json'
ZIP = A/'DD_Feat335_Work_Compositions_84.zip'
SAVED = A/Path(__file__).name
for p in (ROOT, OUT, CHECK, ZIP, SAVED):
    assert not p.exists(), str(p)

def j(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
def info(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
checks=[]; cases=[]
def ck(label, actual, expected=True):
    ok=actual==expected
    checks.append({'check':label,'pass':ok,'actual':actual,'expected':expected})
    if not ok: raise AssertionError(label+': '+repr(actual)+' != '+repr(expected))
def case(cid,title,inputs,actual,expected,sources,limit='Conditional specification arithmetic/state only. Ownership, prerequisites, actual access, tools, bodies, safety and source eligibility are supplied premises, not authenticated campaign state.'):
    ck(cid+' '+title,actual,expected)
    cases.append({'id':cid,'title':title,'inputs':deepcopy(inputs),'computed':deepcopy(actual),'expected':deepcopy(expected),'sources':sources,'qualification':limit})
def rejects(cid,title,inputs,fn,sources):
    try: fn(); actual=False
    except ValueError: actual=True
    case(cid,title,inputs,{'rejected':actual},{'rejected':True},sources)

paths=[I/'candidate.json', I/'shared_rules.json', R/'data/public/feat_candidates/exact_01/candidate.json',
       R/'docs/feats/exact-candidate-01/CRAFTING.md',
       R/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md',
       R/'docs/director-only/ADVANCED_CRAFT_INTERNAL_OPERATIONAL_GUIDE.md',
       R/'data/crafting/advanced_craft_recipe_candidate_public.json',
       R/'docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md',
       R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',
       R/'data/public/class_playtests/wizard.json',
       R/'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md',
       A/'feat327-source-verdict/FEAT_EXACT_CANDIDATE_ACCEPTANCE_CONTRACT.md',
       A/'feat327-source-verdict/FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json',
       A/'FEAT335_COMPLETE_ACQUISITION_ASSEMBLY_AFTER_FLORA.json',
       A/'FEAT335_TIME_PROVISIONS_CASES_83.json',
       A/'ACTIVE_AUTHORING_CHECKPOINT_FEAT_TIME_PROVISIONS_83.json']
bindings=[info(p) for p in paths]
candidate=j(paths[0]); records={r['id']:r for r in candidate['records']}
public={r['id']:r for r in j(paths[2])['feats']}
ids=['craftsman','diligent_researcher','spell_scribe','tinker_adept','combat_engineering','master_smithing','quick_learner','quick_ritualist','ritual_channeler','ritual_caster','gossip','battleReady','contraption_crafter','trapsetter']
selected={k:records[k] for k in ids}
for k,r in selected.items():
    ck(k+' exact public/internal procedure',r['operationalRules'],public[k]['operationalRules'])
    ck(k+' no parent exact or runtime promotion',not r['selectionEnabled'] and not r['exactApproved'] and not r['runtimeApproved'])
shared=j(paths[1]); cards={c['recipeId']:c for c in j(paths[6])['cards']}
en=cards['recipe-121']; craft=paths[4].read_text(encoding='utf-8'); advanced=paths[5].read_text(encoding='utf-8'); equipment=paths[8].read_text(encoding='utf-8'); wizard=j(paths[9])
ck('Actual selected EN source hours',en['sourceRecipe']['workRequirements']['activeWorkHours'],4)
ck('Actual selected EN assistant cap',en['sourceRecipe']['workRequirements']['maximumAssistants'],0)
ck('Actual selected EN field flag',en['sourceRecipe']['workRequirements']['fieldCraftable'],False)
ck('Actual selected EN minimum research source',en['sourceRecipe']['discovery']['minimumResearchHours'],0)
for token in ['first `min(15 minutes, adjusted total active time)`','rounded upward once to a whole minute','An interruption loses unfinished creation-phase progress only']:
    ck('Advanced exact source '+token,token in advanced)
for token in ['| Light armor | 1 minute | 1 minute |','| Heavy armor | 10 minutes | 5 minutes |','One actual assisting creature halves doff time only']:
    ck('Equipment exact source '+token,token in equipment)
for token in ['2 hours and 50 gp','1 hour and 25 gp','Matrix Efficiency reduces this to 45 minutes']:
    ck('Wizard exact source '+token,token in json.dumps(wizard))
fa13=next(c for c in j(paths[12])['cases'] if c['id']=='FA-13')
ck('Source-authored partial repair example retained','twenty-minute partial repair restoring2HP may restore5withPB3' in fa13['completeExpectedOutcome'])

# Manufacturing: existing 8-hour source example and the complete actual EN card.
def manufacturing(base,craftsman=False,forge=False):
    factors=[F(1)] + ([F(1,2)] if craftsman else []) + ([F(3,4)] if forge else [])
    return ceil(F(base)*min(factors))
for base,label,expected in [(480,'source-worked-8h',[480,240,360,240]),(240,'actual-recipe-121',[240,120,180,120])]:
    for n,(cm,fd) in enumerate([(False,False),(True,False),(False,True),(True,True)]):
        actual=manufacturing(base,cm,fd)
        case('WC84-01-'+label+'-'+str(n),'Strongest applicable manufacturing factor once',{'baseMinutes':base,'eligibleCraftsman':cm,'eligibleForgeDwarf':fd,'paidPrerequisitesAndSite':True},{'activeMinutes':actual,'independentCuringWaitMinutes':1440,'beneficialLongRestMinutes':480},{'activeMinutes':expected[n],'independentCuringWaitMinutes':1440,'beneficialLongRestMinutes':480},['craftsman','FS-14','AC-05','recipe-121' if base==240 else 'craftsman current worked case'],limit='Work requirement only; no output, quality, XP, new ingredient or full character is simulated. The 24-hour independent curing wait is the feat source worked-case fixture, not an added EN recipe requirement. The actual EN source card is retained in full.')
for cm,ce in [(False,True),(True,False),(True,True)]:
    minutes=ceil(F(60)*min([F(1)]+([F(1,2)] if cm else [])+([F(1,2)] if ce else [])))
    case('WC84-02-'+str(int(cm))+str(int(ce)),'Two eligible field construction discounts remain one half',{'fallbackBarricadeBaseMinutes':60,'hasCraftsman':cm,'hasCombatEngineeringPermission':True,'eligibleCombatEngineeringTime':ce,'planksLb':20,'hardwareReferenceGp':2},{'activeMinutes':minutes,'planksLbRequired':20,'hardwareReferenceGpRequired':2,'completionDC':12,'qualityOrXPGranted':False},{'activeMinutes':30,'planksLbRequired':20,'hardwareReferenceGpRequired':2,'completionDC':12,'qualityOrXPGranted':False},['combat_engineering','craftsman','FS-14'])

def remaining_work(old_remaining,old_factor,new_factor):
    if old_remaining<0 or not 0<new_factor<=old_factor<=1:raise ValueError('Invalid actual work conversion')
    return ceil(F(old_remaining)*new_factor/old_factor)
case('WC84-03','Mid-order acquisition changes only remaining work',{'originalRequiredMinutes':480,'completedCreditedMinutes':240,'completedPhasesPreserved':True,'newPaidCraftsmanAcquiredAtBoundary':True},{'remainingMinutes':remaining_work(240,F(1),F(1,2)),'actualTotalIfCompleted':240+remaining_work(240,F(1),F(1,2))},{'remainingMinutes':120,'actualTotalIfCompleted':360},['craftsman','FS-14'])
case('WC84-04','A stronger new factor replaces the earlier factor on remaining work',{'originalBaseMinutes':480,'oldForgeRequired':360,'completedCreditedOldMinutes':180,'oldFactor':'3/4','newFactor':'1/2','newPaidCraftsmanAcquiredAtBoundary':True},{'remainingMinutes':remaining_work(180,F(3,4),F(1,2)),'actualTotalIfCompleted':180+remaining_work(180,F(3,4),F(1,2))},{'remainingMinutes':120,'actualTotalIfCompleted':300},['craftsman','FS-14'],limit='Algebraic normalization of the source remaining-unworked requirement at a completed phase boundary; no repeated acquisition event or automatic rest/work schedule is asserted.')

# The EN order retains its actual stable incorporation phase and every lost minute.
phase_plan=[15,105]
attempts=[{'phase':0,'actualMinutes':10,'completed':False},{'phase':0,'actualMinutes':15,'completed':True},{'phase':1,'actualMinutes':30,'completed':False},{'phase':1,'actualMinutes':105,'completed':True}]
credited=0;elapsed=0;next_phase=0;trace=[]
for a in attempts:
    if a['phase']!=next_phase:raise ValueError('Out-of-order fixture')
    elapsed+=a['actualMinutes']
    if a['completed']:
        assert a['actualMinutes']==phase_plan[next_phase]
        credited+=phase_plan[next_phase];next_phase+=1
    trace.append({'elapsedActiveMinutes':elapsed,'creditedMinutes':credited,'nextPhase':next_phase})
case('WC84-05','Interrupted EN creation retains complete phases, real losses and minimum incorporation',{'actualRecipeId':'recipe-121','eligibleCraftsman':True,'phaseMinutes':phase_plan,'attempts':attempts,'actualIngredientsBodiesStationAndEligibility':'explicit conditional premises, not created by this case'},{'requiredCredit':120,'trace':trace,'elapsedActiveMinutes':elapsed,'creditedMinutes':credited,'extraOutputOrInputRefundGranted':False},{'requiredCredit':120,'trace':[{'elapsedActiveMinutes':10,'creditedMinutes':0,'nextPhase':0},{'elapsedActiveMinutes':25,'creditedMinutes':15,'nextPhase':1},{'elapsedActiveMinutes':55,'creditedMinutes':15,'nextPhase':1},{'elapsedActiveMinutes':160,'creditedMinutes':120,'nextPhase':2}],'elapsedActiveMinutes':160,'creditedMinutes':120,'extraOutputOrInputRefundGranted':False},['AC-05','recipe-121','craftsman','FS-14'])

# Research requirements and genuinely excluded activities retain separate ledgers.
for factors,expected,label in [([],480,'none'),([F(1,2)],240,'researcher'),([F(1,2),F(1,2)],240,'two-authorized-same-purpose-halves')]:
    base=max(8,en['sourceRecipe']['discovery']['minimumResearchHours'])*60
    case('WC84-06-'+label,'Formula research uses its actual minimum before eligible reduction',{'actualRecipeId':'recipe-121','sourceMinimumHours':0,'frameworkMinimumHours':8,'eligibleRelevantEvidenceAndFacility':True,'factors':[str(x) for x in factors]},{'requiredActiveMinutes':ceil(F(base)*min([F(1)]+factors)),'actualRecipeDC':en['sourceRecipe']['craftingCheck']['targetDC'],'newFormulaOrRetryGranted':False},{'requiredActiveMinutes':expected,'actualRecipeDC':8,'newFormulaOrRetryGranted':False},['Diligent Researcher','FS-14','CRAFTING_HARVEST_PLAYTEST research'],limit='Third variant is the exact current Diligent Researcher worked-case comparison to an independently authorized second half-time source; it does not create such a feat/item. Actual research results and campaign evidence are not executed.')
for activity,minutes in [('ordinary-language-course',19200),('ordinary-craft-formula-copy',60),('repair-source-worked-case',120),('Master-Smithing-fixed-temper',480),('Combat-Engineering-fixed-kill-zone-preparation',10)]:
    case('WC84-07-'+activity,'A different or explicitly excluded procedure is not retimed as ordinary creation/research',{'activity':activity,'actualRequiredMinutes':minutes,'claimedDiscounts':['Craftsman','Forge Dwarf','Diligent Researcher']},{'requiredMinutes':minutes,'discountApplied':False},{'requiredMinutes':minutes,'discountApplied':False},['craftsman','diligent_researcher','master_smithing','combat_engineering'],limit='Source classification adjudication, not execution of a general category classifier. Each procedure remains conditional on its full source authority. Contraption Crafter is expressly left unselected below rather than excluded merely for printing a duration.')

# Exact copied-spell arithmetic, including current Wizard's separate class price.
def copy_bill(minutes,divisible,indivisible,aggregate_cp,rare,unique,time_factors,material_factors,classified=True):
    if not classified:raise ValueError('Unclassified special inputs')
    tf=min([F(1)]+time_factors);mf=min([F(1)]+material_factors)
    return {'activeMinutes':ceil(F(minutes)*tf),'divisibleUnits':str(F(divisible)*mf),'indivisibleUnits':ceil(F(indivisible)*mf),'mundaneAggregateCp':ceil(F(aggregate_cp)*mf),'rareUnits':rare,'uniqueUnits':unique}
case('WC84-08','Spell Scribe preserves the source mixed bill',{'sourceWorkedCaseMinutes':120,'mundaneCp':4000,'separateRareCp':1000,'featMaterialFactor':'3/4'}, {'activeMinutes':ceil(F(120,2)),'mundaneCp':ceil(F(4000)*F(3,4)),'rareCp':1000,'totalCp':ceil(F(4000)*F(3,4))+1000}, {'activeMinutes':60,'mundaneCp':3000,'rareCp':1000,'totalCp':4000}, ['spell_scribe current full worked case','FS-14'])
case('WC84-09','Exact final-minute, indivisible-unit and aggregate-copper rounding',{'minutes':121,'divisibleMundaneUnits':6,'indivisibleMundaneUnits':1,'mundaneAggregateCp':1001,'rareUnits':3,'uniqueUnits':1},copy_bill(121,6,1,1001,3,1,[F(1,2)],[F(3,4)]),{'activeMinutes':61,'divisibleUnits':'9/2','indivisibleUnits':1,'mundaneAggregateCp':751,'rareUnits':3,'uniqueUnits':1},['spell_scribe'])
ck('Four mundane indivisible sheets become three',copy_bill(120,0,4,0,0,0,[F(1,2)],[F(3,4)])['indivisibleUnits'],3)
for feat in [False,True]:
    times=[F(1,2)]+([F(1,2)] if feat else [])
    materials=[F(1,2)]+([F(3,4)] if feat else [])
    case('WC84-10-'+str(feat),'Actual Wizard rank2 class scribing remains120minutes and50gp',{'actualFoundWizardSpellRank':2,'withinActualLegalRank':True,'legibleAccessibleSource':True,'baselineMinutesPerRank':120,'baselineCpPerRank':5000,'WizardSpellScribing':True,'SpellScribeFeat':feat},{'minutes':ceil(F(240)*min(times)),'cp':ceil(F(10000)*min(materials))},{'minutes':120,'cp':5000},['current Wizard SPELL ACQUISITION BY SCRIBING','spell_scribe'],limit='Actual class-defined copying time and ordinary class bill comparison. This does not classify an independently ambiguous rare-ink bill or execute acquisition/rank validation.')
rejects('WC84-11','An unclassified special-ink bill cannot be assumed mundane',{'classificationAvailable':False},lambda:copy_bill(120,1,1,1000,0,0,[F(1,2)],[F(3,4)],False),['spell_scribe'])
case('WC84-12','Wizard preparation and reconstruction remain separate',{'MatrixEfficiencyOwned':True,'SpellScribeOwned':True,'reconstructionRank':2},{'matrixMinutes':45,'memoryReconstructionMinutes':480,'memoryMaterialsCp':20000,'ordinaryFormulaCopyMinutes':60,'ordinaryFormulaCopyCp':10},{'matrixMinutes':45,'memoryReconstructionMinutes':480,'memoryMaterialsCp':20000,'ordinaryFormulaCopyMinutes':60,'ordinaryFormulaCopyCp':10},['Wizard SPELLBOOK LOSS and MATRIX','spell_scribe','CRAFTING_HARVEST_PLAYTEST'],limit='Exact source classification/numeric adjudication only; no spellbook reconstructed and no class RP or matrices are created.')

# Ritual formula is an explicit exception with a protected base-plus-minimum.
def ritual(base,added,quick=False,channeler=False,physical_assistants=1,wait=0):
    if min(base,added,physical_assistants,wait)<0:raise ValueError('Invalid ritual state')
    if channeler and physical_assistants<1:raise ValueError('Not a group ritual')
    a=min(added,max(300,ceil(F(added,2)))) if quick else added
    previous=base+a
    total=min(previous,max(base+300,ceil(F(previous)*F(3,4)))) if channeler else previous
    return {'activeSeconds':total,'addedAfterQuickSeconds':a,'passiveWaitingSeconds':wait,'elapsedSeconds':total+wait}
expected_ritual={120:[126,126,126,126],300:[306,306,306,306],600:[606,306,455,306],601:[607,307,456,306],1800:[1806,906,1355,680]}
for added,values in expected_ritual.items():
    for n,(qr,rc) in enumerate([(False,False),(True,False),(False,True),(True,True)]):
        expa=added if not qr else {120:120,300:300,600:300,601:301,1800:900}[added]
        case('WC84-13-'+str(added)+'-'+str(n),'Ordered ritual composition retains base, floor and non-worsening rule',{'baseSeconds':6,'sourceAdditionalSeconds':added,'QuickRitualist':qr,'RitualChanneler':rc,'actualQualifiedPhysicalAssistants':1,'separatePassiveWaitSeconds':600},ritual(6,added,qr,rc,1,600),{'activeSeconds':values[n],'addedAfterQuickSeconds':expa,'passiveWaitingSeconds':600,'elapsedSeconds':values[n]+600},['quick_ritualist','ritual_channeler','FS-14'],limit='600-second addition is the current standard ritual route. Other additions and passive wait are explicit source-formula boundary inputs, not newly admitted ritual spells. No overlay, spell acquisition, full cast, output or cost waiver is implemented.')
for qr in [False,True]:
    case('WC84-14-'+str(qr),'Long printed base labor survives group adjustment',{'baseSeconds':3600,'addedSeconds':600,'quick':qr,'channeler':True},ritual(3600,600,qr,True),{'activeSeconds':3900,'addedAfterQuickSeconds':300 if qr else 600,'passiveWaitingSeconds':0,'elapsedSeconds':3900},['quick_ritualist','ritual_channeler'])
rejects('WC84-15','A feat-owning lead alone is not a group',{'leadOwnsRitualChanneler':True,'physicalAssistants':0},lambda:ritual(6,600,False,True,0),['ritual_channeler'])
case('WC84-16','Extra holders cannot multiply helper discount or become extra bodies',{'actualLead':1,'actualAssistants':2,'featHoldersAmongAssistants':2,'sourceNoOtherAssistantCap':True},{'timeSeconds':ritual(6,1800,True,True,2)['activeSeconds'],'ordinaryContributionCount':min(2,2+2),'physicalPeople':3,'grantedCheckBonus':0},{'timeSeconds':680,'ordinaryContributionCount':2,'physicalPeople':3,'grantedCheckBonus':0},['ritual_channeler'])

# Actual source category times and the explicit armor/helper composition.
for base,expected in [(90,45),(120,60),(121,61)]:
    case('WC84-17-'+str(base),'Gossip shortens actual inquiries, not calendar appointments',{'localInquiryMinutes':base,'separateAppointmentWaitMinutes':1440,'willingActualContacts':True},{'activeMinutes':ceil(F(base,2)),'appointmentWaitMinutes':1440,'extraCheckOrTruthGranted':False},{'activeMinutes':expected,'appointmentWaitMinutes':1440,'extraCheckOrTruthGranted':False},['gossip'])
def armor(seconds,feat,helper,doff=True):
    return ceil(F(seconds)*(F(1,2) if feat else 1)*(F(1,2) if helper and doff else 1))
for seconds,label,values in [(60,'light-doff',[60,30,30,15]),(300,'heavy-doff',[300,150,150,75])]:
    for n,(feat,helper) in enumerate([(False,False),(True,False),(False,True),(True,True)]):
        case('WC84-18-'+label+'-'+str(n),'Armor/helper explicit multiplication overrides generic strongest-factor comparison',{'ordinarySeconds':seconds,'BattleReady':feat,'oneActualHelper':helper,'operation':'doff'}, {'requiredSeconds':armor(seconds,feat,helper)},{'requiredSeconds':values[n]},['battleReady','EQUIPMENT_ACQUISITION don/doff'])
case('WC84-19','Helpers do not further reduce donning or shield Actions',{'mediumDonSeconds':300,'BattleReady':True,'extraHelpers':2,'shieldActualCost':'1Action'},{'mediumDonSeconds':armor(300,True,True,False),'lightDoffWithHelpersSeconds':armor(60,True,True),'shieldActions':1,'minimumCompleteSixSecondIntervalsFor15sDoff':ceil(F(15,6))},{'mediumDonSeconds':150,'lightDoffWithHelpersSeconds':15,'shieldActions':1,'minimumCompleteSixSecondIntervalsFor15sDoff':3},['battleReady','EQUIPMENT_ACQUISITION don/doff'],limit='The three-interval result is an arithmetic lower bound requiring three actually available Actions/intervals; no combat actor receives extra Actions or a completed doff from elapsed time alone.')

# Entire authorized repair, successful HP restoration and preserved finite stock.
def repair(state,request):
    s=deepcopy(state); q=request
    if q['id'] in s['completedRepairs']:raise ValueError('Replayed completion')
    if not all(q[k] for k in ['authorizedProcedure','actualBody','complexMechanism','tradeLevelAtLeast5','actualToolsAndSafeAccess']):raise ValueError('Absent source authorization')
    if not 0<=s['currentHP']<=s['maximumHP'] or min(q['totalActiveMinutes'],q['insideRestMinutes'],q['baseRestoredHP'],q['PB'],q['materialCp'])<0:raise ValueError('Invalid state')
    if s['materialsCp']<q['materialCp']:raise ValueError('Missing materials')
    s['materialsCp']-=q['materialCp'];s['elapsedActiveMinutes']+=q['totalActiveMinutes'];s['completedRepairs'].append(q['id'])
    eligible=0<q['totalActiveMinutes']<=30 and q['insideRestMinutes']==q['totalActiveMinutes'] and q['ownerRestEligibleApartFromThisRepair']
    base=min(s['maximumHP']-s['currentHP'],q['baseRestoredHP']) if q['success'] else 0
    bonus=min(q['PB'],max(0,s['maximumHP']-s['currentHP']-base)) if eligible and q['success'] else 0
    s['currentHP']+=base+bonus
    return {'state':s,'entireRepairRestException':eligible,'baseHPActuallyRestored':base,'featExtraHP':bonus}
initial={'bodyId':'TEST_ONLY-FA13-actual-device','currentHP':2,'maximumHP':10,'chargesRemaining':1,'chargesSpent':2,'serviceRemaining':4,'serviceSpent':1,'fuelRemaining':3,'fuelSpent':1,'materialsCp':100,'elapsedActiveMinutes':0,'completedRepairs':[]}
request={'id':'repair-A','authorizedProcedure':True,'actualBody':True,'complexMechanism':True,'tradeLevelAtLeast5':True,'actualToolsAndSafeAccess':True,'totalActiveMinutes':20,'insideRestMinutes':20,'baseRestoredHP':2,'PB':3,'materialCp':20,'ownerRestEligibleApartFromThisRepair':True,'success':True}
def repaircase(cid,title,before,q,expectedhp,bonus,exception,base):
    expected=deepcopy(before);expected['currentHP']=expectedhp;expected['materialsCp']-=q['materialCp'];expected['elapsedActiveMinutes']+=q['totalActiveMinutes'];expected['completedRepairs'].append(q['id'])
    result=repair(before,q)
    case(cid,title,{'before':before,'request':q},result,{'state':expected,'entireRepairRestException':exception,'baseHPActuallyRestored':base,'featExtraHP':bonus},['tinker_adept','FS-14','FA-13'],limit='FA-13 independently-authorized 20-minute partial repair supplies the positive source case. Other durations, body budget values and20cp material payment are explicit TEST_ONLY boundary inputs, not a new repair recipe or actual campaign character. Successful repair outcome and rest eligibility APART FROM this repair are premises; the actual entire-job exception is evaluated here. insideRestMinutes identifies work in the proposed rest window, not an award of beneficial rest. No repair roll or rest reward engine ran; an overlong job gets no assertion of a legal beneficial rest.')
    return result
positive=repaircase('WC84-20','Whole20-minute partial repair restores2+PB3 currentHP',initial,request,7,3,True,2)
repaircase('WC84-21','Exactly30minutes is eligible',initial,{**request,'totalActiveMinutes':30,'insideRestMinutes':30},7,3,True,2)
repaircase('WC84-22','31minute whole repair has no rest exception',initial,{**request,'totalActiveMinutes':31,'insideRestMinutes':30},4,0,False,2)
repaircase('WC84-23','Last20minutes of8hour reconstruction earns no rest bonus',initial,{**request,'totalActiveMinutes':480},4,0,False,2)
repaircase('WC84-24','Failed repair spends work/material but restores noHP',initial,{**request,'success':False},2,0,True,0)
repaircase('WC84-25','Full base restoration has no bonus headroom',initial,{**request,'baseRestoredHP':8},10,0,True,8)
repaircase('WC84-26','PB bonus stops at actual maximum', {**initial,'currentHP':7}, request,10,1,True,2)
repaircase('WC84-27','An observer resting nearby grants no owner rest exception',initial,{**request,'ownerRestEligibleApartFromThisRepair':False},4,0,False,2)
rejects('WC84-28','Duplicate completion cannot create HP or refund stock',{'before':positive['state'],'request':request},lambda:repair(positive['state'],request),['tinker_adept','FS-14'])
for field in ['authorizedProcedure','actualBody','complexMechanism','tradeLevelAtLeast5','actualToolsAndSafeAccess']:
    rejects('WC84-29-'+field,'A missing governing repair predicate stays missing',{'request':{**request,field:False}},lambda field=field:repair(initial,{**request,field:False}),['tinker_adept','FS-14'])

# Preserve an explicit finite follow-through list; arithmetic does not decide scope.
questions=[
 {'id':'FT84-Q01','subject':'Spell Scribe and the Ritual Caster learning route','exactSourceIssue':'Ritual Caster calls its eight-hour-per-rank route spell learning/copying and expressly excludes ordinary research reductions. Spell Scribe applies to an otherwise authorized spell/scroll copying procedure. Neither text expressly selects the interaction for an available complete written ritual versus teacher-led learning, nor itemizes the ten-gp practice/writing bill.','request':'In the later parent feat exact review, select the source-qualified written-copy versus teaching predicate and any material classification; preserve the full learning/recording requirements and rare/unique boundaries. Do not treat an unitemized bill as wholly mundane or universally forbid an otherwise qualifying copy.','disposition':'UNSELECTED; no canonical or local candidate rule added'},
 {'id':'FT84-Q02','subject':'Research phase-credit precision','exactSourceIssue':'Diligent Researcher requires each actual project\'s phase-credit precision and an existing final fractional phase. Manufacturing has explicit first incorporation plus at-most-eight-hour phases; language teaching has15-minute phases. The ordinary eight-hour Translate/Decipher and generic formula-research passages inspected do not expressly assign teaching\'s15-minute phase clock to every research task.','request':'Bind the exact existing per-project phase rule in the full candidate or explicitly complete only an actual missing one during parent review; do not silently import manufacturing incorporation or teaching phases into all research.','disposition':'UNSELECTED; no new universal research phase clock'},
 {'id':'FT84-Q03','subject':'Craftsman and feat-granted Contraption construction','exactSourceIssue':'Craftsman reduces eligible personally led creation, including non-artisan creation, and refers to recipe creation phases. Contraption Crafter grants an actual ten-minute uninterrupted construction using committed parts, but does not expressly say that it is creation-time-discounted or exempt. Master Smithing temper and Combat Engineering kill-zone preparation explicitly exclude creation discounts; their exclusions do not automatically govern another feat.','request':'Resolve the exact construction category and remaining uninterrupted-work requirement without granting a recipe, extra gadget, reset use or free parts. Check the separately authored Trapsetter and other closed construction processes under the same actual-source predicate; do not infer a blanket exclusion merely from a printed fixed duration.','disposition':'UNSELECTED; no discount or exemption selected'},
]
time_mentions=[]
for r in candidate['records']:
    clauses=[s for s in re.split(r'(?<=[.!?])\s+',r['operationalRules'] or '') if re.search(r'(half|halve|discount|25%).*(time|labor|hour|minute)|(time|labor|hour|minute).*(half|halve|discount|25%)',s,re.I)]
    if clauses:time_mentions.append({'featId':r['id'],'fullMatchingClauses':clauses,'fullRecordPreservedInSource':True})
report={'id':'FEAT335-WORK-COMPOSITIONS-84','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS_ISOLATED_SPECIFICATION_CASES_WITH_EXPLICIT_OPEN_INTERFACE_DISPOSITIONS',
 'sourceBindings':bindings,'fullSelectedFeatRecords':selected,'fullSharedRules':[x for x in shared['rules'] if x['id'] in ['FS-03','FS-14']],
 'fullActualRecipe121':en,'fullSourceFA13':fa13,'all327ProcedureTimeMentionScan':time_mentions,
 'cases':cases,'caseCount':len(cases),'topLevelCaseCount':29,'openDispositions':questions,
 'scope':'Manufacturing strongest-factor and remaining-work arithmetic, actual EN first-phase losses, fixed-procedure exclusions, research requirement arithmetic, spell copying bills, ritual composition matrix, Gossip, explicit Battle Ready/helper exception and whole authorized rest-repair HP/budget state. This does not finish FXC-06 or all335 feat review.',
 'actualExecution':'Only this new self-contained Python standard-library diagnostic ran. No project/downloaded Python imports, game application, Unity process, complete campaign scheduler, full character acquisition or owned-world action ran.',
 'approvalBoundaries':{'newRuleAdoptions':0,'canonicalCandidateChanged':False,'parentFeatExactApproval':False,'full335Execution':False,'runtimeTesting':False,'humanTesting':False,'balance':False,'wholeGameComplete':False},
 'nextAction':'Confer on the three explicitly unselected source-interface dispositions within later full feat review, complete any exact resulting cases and reconcile all FXC gates. Keep current GPT Resonance Fields3 generation uninterrupted.',
 'sourceInformationDeleted':0}
for row in bindings:ck('Exact original source retained '+row['path'],info(G/row['path']),row)
payload={'REPORT.json':enc(report),'check_feat_work_compositions_84.py':Path(__file__).read_bytes(),
 'README.md':b'# Work and repair specification evidence\n\nSource-bound conditional specification cases preserve full input files and actual procedure texts. They do not authenticate a campaign actor or implement a game runtime. Manufacturing, copying, rituals, armor and repairs retain separate source contracts. Three source-interface dispositions remain explicitly unselected for the parent feat review. No canonical rule, selection flag, spell index or exact feat approval is changed.\n'}
for p in paths:payload['sources/'+p.relative_to(G).as_posix()]=p.read_bytes()
payload['MANIFEST.json']=enc({n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())})
ROOT.mkdir()
for n,b in payload.items():
    p=Path('\\\\?\\'+str((ROOT/n).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,b in sorted(payload.items()):z.writestr(n,b)
with zipfile.ZipFile(ZIP) as z:
    ck('Archive exact membership',set(z.namelist())==set(payload) and len(z.namelist())==len(payload))
    ck('Archive CRC',z.testzip() is None)
    for n,b in payload.items():ck('Archive roundtrip '+n,z.read(n)==b)
OUT.write_bytes(enc(report));SAVED.write_bytes(Path(__file__).read_bytes())
CHECK.write_bytes(enc({'report':info(OUT),'archive':info(ZIP),'checkCount':len(checks),'failures':0,'checks':checks,'isolatedSpecificationExecuted':True,'runtimeTestsExecuted':0,'newRuleAdoptions':0,'openSourceDispositions':len(questions),'sourceInformationDeleted':0}))
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'check':info(CHECK),'cases':len(cases),'checks':len(checks),'failures':0,'unselectedDispositions':len(questions)}))
