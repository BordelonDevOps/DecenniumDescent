"""Author Fishing's 44 cards from FI-D01..24. Does not promote recipes.

Original source objects remain complete; operational additions are separate.
The shared guide is normative alongside each card, not a runtime implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json, re
from build_leatherworking_recipe_candidate import read, sha, write, dump, ratio, unr, fmt, public_projection

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
STATUS = 'authored-draft-required-exact-review-repairs'
AUTH = {'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'turnId':'d8e96231-9912-42c7-a691-7c4ba4b68821',
        'replyId':'78d78fa4-1292-4566-9f43-7149476da18e',
        'scope':'FI-D01..24 source/interface decisions; exact-card approval pending',
        'sha256':'f6b2325a6c23bd1652e0d9752bc2708754a34be2b95a5768f40b3152d5a22ad0'}
EXACT_AUTH={'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
    'turnId':'9d44c9d4-41c2-4550-99c7-4ad8f68b2cf6','replyId':'f0bf49fb-8bea-499f-8243-f3db5c302bbf',
    'sha256':'551587e17bd1c6552c374efb4c2cadf60e6efd7dda9f046e8c8bd620f66b8d7d',
    'scope':'FI-E01..11 required corrections; promotion conditional on completing all repairs and specified verification',
    'completionGateSatisfied':False}
CHECK_FAMILY = 'equipment.leather-task-enhancement'
RECOVERY_FAMILY = 'equipment.fishing-extra-recovery'
METHODS = {'Rod':['Rod','Line','Hook','Tackle','Lure','Bait','Rig'],
           'Net':['Net','Lure','Bait','Rig'], 'Trap':['Trap','Lure','Bait','Rig']}


def model_id(r):
    return 'fishing.' + ('bait-dose' if r['recipeFamily']=='Bait' else r['recipeFamily'].lower())


def models():
    rows = [
        ('Hook','Eyed 2-inch steel hook, 0.5-inch gape',.10,.02,5,19,'original hook body'),
        ('Line','Continuous 50-foot waxed-fiber line with end fittings',.20,.25,5,11,'original functional 50-foot span, including recovered severed sections'),
        ('Lure','3-inch wooden lure and attachment eye; no hook',.20,.05,5,15,'original core body'),
        ('Rod','6-foot wooden rod with grip and guides; no line or hook',.50,2,5,15,'original shaft'),
        ('Tackle','6 x 4 x 2-inch control board, winder, float, sinker and clips; no rod, line or hook',1,1,5,15,'original control board and winder'),
        ('Net','Dip-net: 6-foot handle, 2-foot hoop, 2-foot-deep bag, 0.5-inch mesh and bait clip',2,3,5,11,'original hoop, primary mesh and handle'),
        ('Trap','24 x 12 x 12-inch basket with funnel, service door, bait holder and 20-foot recovery cord',4,4,5,15,'original primary basket/frame and funnel'),
        ('Rig','6 x 4 x 4-inch perforated steel chum dispenser with lid, mount and 10-foot tether',2,1,5,19,'original canister and primary mounting'),
        ('Bait','Single 0.10-pound carrier dose and 0.01-pound wrapper; 2 x 1 x 1-inch packet',.02,.11,1,11,None)]
    result = {}
    for family,name,price,weight,hp,ac,original in rows:
        mid=model_id({'recipeFamily':family})
        result[mid]={'id':mid,'family':family,'name':name,'baselinePriceGp':price,
            'baselineWeightLb':weight,'ordinaryMaximumStructuralHP':hp,'structuralAC':ac,
            'grade':'Standard','fixedDimensions':True,'automaticLargeScaling':False,
            'repairable':family!='Bait','requiredOriginalAssembly':original,
            'methods':[k for k,v in METHODS.items() if family in v],
            'armorBonusCandidate':None,'provenance':'NEW FI-D02..05; original equipment unchanged'}
    result['fishing.bait-dose'].update({'carrierWeightLb':.10,'wrapperWeightLb':.01,
        'carrierPriceGp':.01,'wrapperPriceGp':.01,'wrapperHP':1,'wrapperAC':11,
        'storageUnprotectedHours':24,'receiptElapsedMinutes':60,'uses':1})
    return result


def affinities():
    s=(AUDIT/'GPT_FISHING_SOURCE_CONFERENCE.md').read_text(encoding='utf-8')
    section=s.split('## FI-D15',1)[1].split('## FI-D16',1)[0]
    rows=re.findall(r'^\| ([A-Za-z]+) \| (.+) \|$',section,re.M)
    result={tag:{'tag':tag,'intrinsicPredicate':predicate,
        'explicitApprovedAffinityAlsoQualifies':True,'authority':'NEW FI-D15'}
        for tag,predicate in rows if tag!='Affinity'}
    assert len(result)==14
    return result


def shared_profile(registry):
    return {'id':'fishing.shared.v1','sourceAuthority':AUTH,
        'classification':{'magical':True,'artifact':False,'attunementRequired':False,
            'charges':False,'resourceCost':0,'concentration':False,'spellActivationRequired':False},
        'affinityRegistry':registry,'methodCandidateFamilies':METHODS,
        'checkFamily':CHECK_FAMILY,'recoveryFamily':RECOVERY_FAMILY,
        'attempt':{'ability':'WIS','toolProficiency':'Fishing tackle','artisan':False,
            'setupActiveMinutes':5,'fishingMinutes':50,'checkAtMinute':55,
            'setupStartIndependentOfExposure':True,'firstExposureWithinSetupPhase':True,
            'preSetupReservationReceiptRequired':True,'preExposureCancellationPreservesWorkAndLosses':True,
            'separateSetupAndFishingWorkEvidence':True,
            'retrievalActiveMinutes':5,'attendedClosureMinutesAfterCheck':10,
            'ordinaryDCs':[12,15,18],'untrainedDisadvantage':True,
            'actualCanonicalCatchRollRequired':True,'canonicalRollBoundToOneAttempt':True,
            'declaredCatchProfileAndDCBoundToCoreResolution':True,'governingCredentialRequired':True,
            'expertiseReplacesPB':True,'trapPersonalTermsOnly':['WIS','Fishing PB or expertise'],
            'maximumUnresolvedDeploymentsPerLead':1,'maximumCatchLb':10,
            'leadHands':2,'trainedRodNetAssistantMaximum':1,'trainedRodNetAssistantBonus':1,
            'assistantMustWorkBeforeCheckMinutes':55,'trapAssistantBonus':0,
            'activeWorkActionSeconds':6,'activeWorkWatchCeiling':2,
            'criticalCatchMultiplier':1,'newCatchProcedureForEncounters':False},
        'trap':{'passiveSoakMinutes':50,'setterSnapshot':['WIS','Fishing PB or expertise'],
            'soakBeginsAfterCompletedSetup':True,
            'currentEquipmentAtCheck':True,'checkOnceWhenAbsent':True,
            'secureCaptureAtRetainedEntry':True,'usableInteriorInches':[22,10,10],
            'funnelInches':[4,4],'serviceOpeningInches':[8,8],
            'catchCapacityCubicFeet':1,'baitHolderLb':.10,'recoveryPathFeet':20},
        'net':{'reachFeet':6,'capacityCubicFeet':.5,'meshInches':.5,'combatRestraint':False},
        'rod':{'wholeLinePathFeet':50,'requires':['Rod','Line','Hook','compatible bait or artificial Lure']},
        'rig':{'usableInteriorInches':[5,3,3],'capacityPints':1,'capacityLb':1,
            'tetherFeet':10,'withinAssemblyBaitPointFeet':5,'extraMountMinutes':5,
            'extraRetrievalMinutes':5,'chumLb':1,'chumReferenceGp':.10,
            'oneFinishedBaitSubstitutionLb':.10,'remainingOrdinaryChumLb':.90,
            'actualLoadSupportMountAndFirstDispersalBound':True,
            'ordinaryChumPortionsSpentOnce':True,'wrapperExcludedFromChumMass':True,
            'currentBodyAndSupportRequiredForMagic':True,'spentAllotmentNeverRefilled':True,
            'claimClosureDoesNotRetrieveDispenser':True,
            'separateActualRetrievalWorkAndHandlingRequired':True,
            'unretrievedPhysicalLocationAndReservationPersist':True},
        'attraction':{'chooseSources':1,'waterPathFeet':30,'matchingWeight':2,
            'nonmatchingWeight':1,'stablePhysicalIdOrder':True,'drawsPerOpportunity':1,
            'outsideRegionExcluded':True,'originBoundToActualPresentationOrDispenser':True,
            'pathsBoundToOpportunityCandidateSet':True,'rodDeploymentPathIsSeparate':True,
            'compulsion':False,'redrawIfUnavailable':False},
        'ledger':{'checkpoint':['time','phase','sequence'],'expectedVersionRequired':True,
            'processHistoricalDueEventsFirst':True,'rejectReplayAndEarlierTransitions':True,
            'identities':['site','shared-stock','opportunity','creature','attempt','equipment','unit'],
            'oneExtraEvaluationPerCreatureIncludingZero':True,'separateLifeAndCustody':True,
            'automaticRenewal':False,'governingWorldRecordsRequired':True},
        'physicalEvidence':{'admissionBoundToAttemptAssemblyMethodAndCreature':True,
            'massAndGeometryBoundToApplicableCreatureProfile':True,
            'allIndispensableCurrentBodyStatesRequired':True,
            'allRegisteredMagicalCandidateViewsRequired':True,
            'ordinaryUnenchantedMembersRemainPhysicalRequirements':True,
            'admissionAndModifierUseSameCurrentBodyState':True,
            'attendedRetrievalRequiresLeadAndBothHands':True},
        'baitEvidence':{'actualDoseDebitRequired':True,'nullBaitIdHasNoFinishedBaitContribution':True,
            'receiptBindsPhysicalDoseRecipeAssemblyExposureExpiryAndSuppression':True,
            'presentationFormsBoundToRealItemsAndPortions':True,
            'ordinaryPortionRequiresInventoryAndUseEvidence':True,
            'oneOrdinaryPortionUsePerPhysicalIdentity':True,
            'storageHistoryFromActualCompletionRequired':True,'wrappingAndTransferNeverResetAge':True,
            'ordinarySwallowingPreservesValidReceipt':True},
        'recovery':{'inventoryAtCatch':False,'extraFromRealReservedUnitsOnly':True,
            'disjointBaselineReserveDamagedUniqueUnits':True,'categoryOrderBeforeCheck':True,
            'ordinaryMeatUnitLb':1,'ordinaryMeatTier':1,'ordinaryMeatValueGp':None,
            'baselineMassPrecisionLb':.01,'catchBonusOnHarvest':False,
            'actualDeathRemovalClocks':True,'partialHarvestForfeitsUnselected':True},
        'crafting':{'ability':'WIS','artisan':False,'forgeDwarfReduction':False,
            'firstStableIncludedActiveMinutes':15,'laterMaximumPhaseHours':8,
            'reserveMultiplier':ratio(F(3,2)),'sourceComponentsAllConsumed':True,
            'catalystReturnMaximum':0,'ordinaryToolFacilityBonus':0,
            'baitSingletonFlawedBecomesFailed':True,'baitDurabilityImprovement':False},
        'bodyQualification':{'actualOrderCreationInventoryReservationRequired':True,
            'fixedModelAndFamilyRequired':True,'exclusivePhysicalConstituents':True,
            'baitEligibleCarrierAndWrapperIdentitiesRequired':True,
            'consistentRecordedHPImprovementAndFlawRequired':True,
            'repairOriginalsFromCreationManifest':True,'repairRecipeAndModelBound':True,
            'arithmeticQuotationAloneQualifiesRepair':False},
        'baitContainer':{'priceGp':.10,'emptyWeightLb':.25,'hp':5,'structuralAC':15,
            'interiorInches':[5,3,3],'capacityPints':1,'capacityLb':1,
            'maximumPacketsByWeight':9,'actualPackingStillRequired':True,'preservation':False},
        'supply':{'unitsProduced':0,'foodCreditForRawCatch':0,
            'physicalPoolRouteExclusionPerWatch':['Fishing','Forage'],
            'disjointAuthoritativeStockException':True},
        'sourceInputsUntouched':True}


def operational(r,bs):
    m=r['mechanics'];q=r['quantity'];b=bs[model_id(r)];bait=r['recipeFamily']=='Bait'
    h=r['workRequirements']['activeWorkHours'];assert h is not None and h>=.25
    finished=F(str(r['economy']['recommendedMarketValue']))/q+F(str(b['baselinePriceGp']))
    text=(f"On one eligible ordinary provision catch check, this actual participating {r['recipeFamily']} "
        f"offers +{m['fishingBonus']} in {CHECK_FAMILY}; choose the strongest independently eligible modifier once. "
        f"It offers {m['extraYield']} in {RECOVERY_FAMILY}, separately compared at secure capture among sources "
        "that qualified at the check and still qualify. The first secure capture records one recovery evaluation "
        "for that physical creature, including zero; later recapture cannot raise it. Authorize only available "
        "disjoint real reserve units for later lawful harvesting, never immediate meat or extra creatures. "
        f"Its one selectable attraction affinity is {m['attracts']}; choose one source before one finite, "
        "weighted response allocation within 30 feet of connected water path. Local availability, perception, "
        "response and physical fit remain required. The three choices are independent; tags never combine automatically. ")
    text+=('Expose one whole eligible dose to spend its use and create one assembly-bound receipt lasting 60 elapsed minutes or until attempt closure. Ordinary dispersal/swallowing does not end the receipt. Failed or interrupted fishing gives no refund. Unexposed storage spoils after 24 accumulated unprotected hours from completion; unwrapping alone is not exposure. '
        if bait else 'The complete item must have positive structural HP, remain unsuppressed and unmelded, and actually participate in the registered method. It is reusable, but supplies no bait/chum or new opportunity. ')
    text+='Neither case grants a separate activation, RP, concentration, charges, proficiency, AC candidate, resistance, food credit or bonus on harvesting, repair, research, creation or combat.'
    return {'sharedProfileId':'fishing.shared.v1','text':text,'baseModelIds':[b['id']],
        'effect':{'fishingBonus':m['fishingBonus'],'extraYield':m['extraYield'],
            'attracts':m['attracts'],'checkFamily':CHECK_FAMILY,'recoveryFamily':RECOVERY_FAMILY,
            'armorBonusCandidate':None,'oneEvaluationIncludingZero':True},
        'eligibleMethods':b['methods'],'standardQuantity':q,'maximumBaseReserve':3*q//2,
        'outcomes':{'Standard':q,'ExceptionalYield':5*q//4,'MasterworkYield':3*q//2,
            'DurabilityOrLabelOptionQuantity':q,'FlawedQuantity':q//2 if q>=2 else (0 if bait else 1),
            'SingletonFlawedAddsPersistentFlaw':q==1 and not bait,
            'SingletonFlawedIsFailed':q==1 and bait,'Failed':0,'Mishap':0,
            'maximumEligibleCatalystReturnUnits':0,'baitLabelOnlyOption':bait,
            'bonusYieldAffinityOrUseImprovement':False},
        'work':{'sourceActiveWorkHours':h,'operationalActiveWorkHours':h,
            'includedFirstStablePhaseHours':.25,'remainingActiveWorkHours':h-.25,
            'maximumLaterPhaseHours':8,'forgeDwarfEligible':False,'requiredAbility':'WIS',
            'maximumAssistants':r['workRequirements']['maximumAssistants'],
            'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel'],
            'fieldCraftable':r['workRequirements']['fieldCraftable'],
            'timeMode':r['workRequirements']['timeMode']},
        'repair':None if bait else {'trainedFishingRequired':True,'ability':'WIS',
            'functionalDC':10,'brokenDC':r['craftingCheck']['targetDC'],
            'functionalMinimumHours':1,'brokenMinimumHours':8,
            'functionalMaterialsReferenceGp':ratio(F(str(b['baselinePriceGp']))/4),
            'brokenMaterialsReferenceGp':ratio(finished/4),
            'requiredOriginalAssembly':b['requiredOriginalAssembly'],'forgeDwarfEligible':False},
        'sourceProcessUnitReferenceGp':ratio(F(str(r['economy']['recommendedMarketValue']))/q),
        'finishedUnitReferenceGp':ratio(finished)}


def body_table(bs):
    return '\n'.join(['| Complete body | gp | lb | HP / structural AC | Methods |',
        '|---|---:|---:|---|---|']+[f"| {b['name']} | {b['baselinePriceGp']} | {b['baselineWeightLb']} | {b['ordinaryMaximumStructuralHP']} / {b['structuralAC']} | {', '.join(b['methods'])} |" for b in bs.values()])


def affinity_table(ds):
    return '\n'.join(['| Affinity | Intrinsic evidence (or explicit independently approved affinity) |',
        '|---|---|']+[f"| {tag} | {d['intrinsicPredicate']} |" for tag,d in ds.items()])


def method_note(family):
    common='All methods require actual prey/opportunity, access, receiving arrangements and the shared guide; maximum one unresolved deployment per lead.'
    notes={
        'Hook':'Mount to a complete Rod + continuous Line assembly with compatible ordinary bait, finished Bait or artificial Lure. Actual hook fit and 10-pound catch limit apply.',
        'Line':'Complete the Rod + Hook assembly and bait/Lure; the whole path, including depth/bends/elevation, is at most 50 feet. Joined extra lines do not extend it.',
        'Rod':'Supply separate continuous Line, Hook and bait/Lure. The actual lead uses two hands; this is no arcane focus. Whole line path is at most 50 feet and catch at most 10 pounds.',
        'Tackle':'Mount the control board to the Rod or stable support so it actually controls the admitted line. Supply separate Rod, Line, Hook and bait/Lure. This output is not the 1 gp / 4 lb tool kit or a boat.',
        'Lure':'Attach to a real admitted Rod, Net or Trap assembly. Rod may use this instead of ordinary bait; Trap still needs its own compatible bait. Stationary presentation must actually be receptive to prey.',
        'Net':'Use as a two-handed dip-net with supported access and a target within 6 feet. Catch must fit the hoop/mesh and both 10-pound / 0.5-cubic-foot limits. Unbaited visible prey may qualify; attraction needs actual compatible bait or attached Lure.',
        'Trap':'Supply actual anchor/support and compatible bait in its separate 0.10-pound holder. Catch must pass the 4 x 4-inch funnel and fit both 10-pound / 1-cubic-foot limits. Its one-shot unattended check is at minute 55; retrieval takes five active minutes and two capable hands along the 20-foot cord path.',
        'Rig':'Accessory only: bind to one Rod, Net or Trap assembly, within 5 feet of its bait/capture point, using actual support and at most 10 feet of tether. Load 1 pound compatible chum within both 1-pint / 1-pound capacity. One finished Bait can replace 0.10 pound, leaving 0.90 pound ordinary chum. Add five mounting and five retrieval minutes.',
        'Bait':'Place one whole dose in the actual admitted Rod, Net or Trap bait arrangement or compatible Rig chum. Only one receipt contributes to an assembly. A dose substituted into Rig chum does not also fill a Hook or Trap bait holder.'}
    return notes[family]+' '+common


def card_md(c,bs,ds,internal):
    r=c['sourceRecipe'];o=c['operational'];b=bs[model_id(r)];q=r['quantity'];w=r['workRequirements'];bait=r['recipeFamily']=='Bait'
    lines=[f"## {r['id']} — {r['name']}",'',f"**DRAFT; required exact-review corrections in progress.** {r['visibility']}; Fishing level {r['skillLevel']}; tier {r['tier']}; {r['rarity']}; crafting DC {r['craftingCheck']['targetDC']}; Standard quantity {q}.",'',
        '**Preserved source effect:** '+r['effects'],'','**Operational effect:** '+o['text'],'',
        affinity_table({r['mechanics']['attracts']:ds[r['mechanics']['attracts']]}),'',
        body_table({b['id']:b}),'','**Assembly and use:** '+method_note(r['recipeFamily']),'',
        '**Attempt:** Five setup minutes, fifty fishing minutes, one WIS/Fishing check at minute 55, then five active retrieval minutes. Each active six seconds uses an Action and the actual required hands. DC 12 / 15 / 18 is assigned to feasible site conditions before commitment, independently of this crafting DC. Untrained catching has disadvantage and no PB. One trained Rod/Net assistant earns +1 only after all 55 prior work minutes; Trap uses setter WIS/PB snapshot and current gear at its one due check, with no assistant. Rod/Net secure control must occur before closure ten elapsed minutes after the check. Real stock and one response allocation are required; failure spends the opportunity.','',
        f"**Reserve:** {o['maximumBaseReserve']} actual ordered "+('0.10-pound carrier blanks and 0.01-pound wrappers' if bait else 'complete Standard mundane bodies, never previously magically altered')+'. Reserve exclusively before work. Latest lawful age, condition and damage apply; missing/ineligible bodies pause before rolling. Transform first resolved N with no post-roll reordering or purchases; unused reserves remain actual ordinary stock. Source process materials are additional, not body mass.','',
        '**Source component occurrences:**','','| # | Component | Quantity | Tier | Role | Consumed | Unit lb | Unit gp | Properties |','|---|---|---:|---:|---|---|---:|---:|---|']
    for i,z in enumerate(r['components']):
        lines.append(f"| {i} | {z['name']} | {z['quantity']} | {z['tier']} | {z['role']} | {z['consumed']} | {z['weight']} | {z['value']} | {', '.join(z['properties'])} |")
    lines+=['','All listed occurrences are mandatory consumed process inputs once per batch. **No catalyst return.** Failed non-catalyst recovery is exactly the framework\'s 25% with actual divisibility and original ages; Mishap/abandonment return none. Role bait is not a finished Bait dose or an attempt\'s bait supply. Ordinary tools and reserved bodies are separate.','',
        f"**Work and access:** Source {r['craftingTime']}; {w['activeWorkHours']} actual active hours, including the first 15-minute stable incorporation phase; divide remaining {fmt(F(str(w['activeWorkHours']))-F(1,4))} hours into declared phases of at most eight hours. WIS and the actual non-artisan Fishing-tackle credential, toolkit, Knife, Bait container and {w['station']} are required. Source requiredTools: {', '.join(w['requiredTools'])}. fieldCraftable={str(w['fieldCraftable']).lower()}, timeMode={w['timeMode']}; both govern actual station access. Ordinary tools/facilities grant +0. No Forge Dwarf time or quality benefit. Maximum assistants {w['maximumAssistants']}, each working all actual hours; no time reduction. Untrained level 1–4 and higher formula gates follow the framework. Trade level is not added to the roll.",'',
        '**Discovery:** '+json.dumps(r['discovery'],ensure_ascii=False)+f". Preserve trivialAtSkillLevel={r['skillProgression']['trivialAtSkillLevel']} and source progression; do not regenerate level + 5. Actual incorporation stabilizes only eligible incorporated inputs, never already spoiled or untouched material. Interruption loses unfinished phase progress without refunding actual consumed inputs.",'',
        f"**Quality:** Standard {q}; Exceptional yield {o['outcomes']['ExceptionalYield']}; Masterwork yield {o['outcomes']['MasterworkYield']}; Flawed {o['outcomes']['FlawedQuantity']}. "+
        ('Singleton Flawed becomes Failed, with ordinary failed recovery and no magical dose. ' if bait and q==1 else '')+
        ('Alternatively retain Q doses with quality label only. No HP, storage life, receipt duration or extra-use improvement exists. Finished dose age begins at actual completion.' if bait else 'Alternatively retain Q bodies with strongest 25% / 50% structural improvement. Ordinary HP 5 becomes 6 / 7; one persistent flaw halves last to 2 / 3 / 3. Preserve damage deficit, so a positive-HP reserve can emerge Broken. '+('Singleton Flawed adds one persistent flaw.' if q==1 else 'Flawed keeps existing flaws but adds none, even when the resolved yield is one.'))+
        ' Failed/Mishap gives zero outputs. Bonuses, extra recovery, affinity, capacity, reach, grade and permission never improve.','']
    if bait:
        lines+=['**Consumption and repair:** One whole exposure spends one dose, with an assembly receipt lasting 60 elapsed minutes or attempt closure. Ordinary consumption/dispersal does not end the receipt; suppression must affect the assembly\'s bait magic. Storage reaches Spoiled directly after 24 accumulated unprotected hours from completion. Valid receipts keep their own clock; failed/abandoned attempts and transfer never refund a use. No Bait repair/reconstruction. Empty wrapper or residue has no magical use or source-value recovery; real residue mass and wrapper identity remain.','']
    else:
        rep=o['repair'];lines+=['**Repair:** Trained WIS + one Fishing PB/expertise, actual toolkit, Knife, Bait container and station. Functional DC 10, max(1 hour, recorded maximum HP / 10), material reference '+fmt(unr(rep['functionalMaterialsReferenceGp']))+' gp. Broken DC '+str(rep['brokenDC'])+', max(8 hours, recorded maximum HP / 10), material reference '+fmt(unr(rep['brokenMaterialsReferenceGp']))+' gp. Require '+rep['requiredOriginalAssembly']+' and all prerecorded additional irreplaceable constituents. Small subordinate fittings/patches may be replaced; missing primary assemblies cannot. Success restores recorded maximum HP; failure spends work/materials. No formula/creation-level gate, quality, XP, flaw removal, Forge Dwarf reduction or history/refill reset.','']
    lines+=['**Finished undamaged unit reference:** '+fmt(unr(o['finishedUnitReferenceGp']))+' gp = source Standard batch value / Q + '+str(b['baselinePriceGp'])+' gp body. Keep exact fractions until a real purchase (round up to copper) or sale (round down). No quality-yield divisor, double ingredient charge, guaranteed buyer or automatic artifact/rarity multiplier. Owned stock needs no repurchase; depleted/damaged/flawed sale price needs an actual quote.','',
        '**Capture and material boundary:** Check success is not death or harvested inventory. Record one physical creature and its first extra-recovery evaluation, including zero, with only actual disjoint reserve units. Release, recapture and transfer retain this history. Actual later lawful harvest uses existing source DC/time/tools, category-order/partial-forfeiture rules and death/removal ages. These catch bonuses do not aid extraction. No automatic ration, neutralized food, named ingredient or complete Supply Unit is produced. A shared physical pool cannot also yield overlapping Forage stock in the same Watch.','',
        '**Preserved tags:** '+', '.join(r['tags'])+'. Only mechanics.attracts selects attraction. Names, donors and optional metadata establish no unprinted traits or available ingredients.','']
    if c.get('publicBookBinding'):
        lines+=['**Complete public V5 binding:**','','| Paragraph | Preserved text |','|---:|---|']
        lines += [f"| {p['index']} | {p['text'].replace('|',chr(92)+'|')} |" for p in c['publicBookBinding']['paragraphs']]
        lines+=['']
    legacy={k:r[k] for k in ('legacyName','legacyEffect','wholeCreatureUse') if k in r}
    if legacy:lines+=['**Preserved inactive metadata:** '+json.dumps(legacy,ensure_ascii=False),'']
    if internal and 'directorGuidance' in r:
        lines+=['**Preserved optional Director guidance (inactive pending separate variant review):** '+json.dumps(r['directorGuidance'],ensure_ascii=False),'']
    lines+=['**Provenance:** Original V4 recipe index '+str(c['sourceRecipeIndex'])+'; full original object in the accompanying JSON. Operational additions: FI-D01–24. Source status/developed/needsReview flags do not approve this card.','']
    return '\n'.join(lines)


def main():
    assert not (ROOT/'docs/mechanics/FISHING_REVIEW_STATUS.json').exists(),'Already reviewed; do not overwrite.'
    baseline=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert all(sha(GAME/p)==h for p,h in baseline.items()),'Protected input changed'
    assert sha(AUDIT/'GPT_FISHING_SOURCE_CONFERENCE.md')==AUTH['sha256']
    assert sha(AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md')==EXACT_AUTH['sha256']
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    evidence=read(AUDIT/'FISHING_SOURCE_PREPARATION.json')
    recipes=[r for r in read(source)['recipes'] if r['skill']=='Fishing']
    assert recipes==evidence['recipes'] and len(recipes)==44
    bs=models();ds=affinities();bindings={z['recipeId']:z for z in evidence['publicBookBindings']}
    cards=[{'recipeId':r['id'],'name':r['name'],'visibility':r['visibility'],'status':STATUS,
        'sourceRecipeIndex':evidence['sourceIndices'][r['id']],'sourceRecipe':deepcopy(r),
        'publicBookBinding':deepcopy(bindings.get(r['id'])),'operational':operational(r,bs)} for r in recipes]
    public=[public_projection(c) for c in cards if c['visibility']=='public'];assert len(public)==28
    pbs={k:v for k,v in bs.items() if any(k in c['operational']['baseModelIds'] for c in public)}
    pds={k:v for k,v in ds.items() if any(c['operational']['effect']['attracts']==k for c in public)}
    assert len(pbs)==9 and len(pds)==13 and 'Cold' not in pds
    template=(ROOT/'tools/templates/fishing_rules.md').read_text(encoding='utf-8')
    files=[]
    for internal,cs,body,registry,base in [(True,cards,bs,ds,'director'),(False,public,pbs,pds,'playtest')]:
        folder='director-only' if internal else 'mechanics';prefix='INTERNAL' if internal else 'PUBLIC'
        guide=f'docs/{folder}/FISHING_'+('INTERNAL_GUIDE' if internal else 'RECIPE_PLAYTEST')+'.md'
        cardpath=f'docs/{folder}/FISHING_{prefix}_RECIPE_CARDS.md'
        jsonpath=f'data/{base}/fishing_recipe_candidate'+('_internal' if internal else '')+'.json'
        obj={'schemaVersion':1,'status':STATUS,'visibility':'director-internal' if internal else 'public',
            'sourceSha256':sha(source),'sourceAuthority':AUTH,'exactOperationalReviewAuthority':EXACT_AUTH,'sharedOperationalProfile':shared_profile(registry),
            'sharedGuide':guide,'baseModels':body,'cards':cs,'exactRecipeApproval':False,
            'runtimeImplemented':False,'balanceApproved':False,'cosmology':'post-push only'}
        dump(ROOT/jsonpath,obj)
        audience=('Internal: all 44 formulas (28 public, three restricted and thirteen Director-only), nine models and fourteen affinities.'
            if internal else 'Public: 28 formulas, nine models and thirteen operative affinities.')
        text=template.replace('{{AUDIENCE}}',audience).replace('{{BODY_TABLE}}',body_table(body)).replace('{{AFFINITY_TABLE}}',affinity_table(registry))
        for token,name in [('CRAFTING_LINK','CRAFTING_HARVEST_PLAYTEST.md'),('CORE_LINK','CORE_RESOLUTION_PLAYTEST.md'),('BODY_LINK','BODY_EQUIPMENT_PLAYTEST.md'),('EQUIPMENT_LINK','EQUIPMENT_ITEM_PROCEDURES.md')]:
            assert (ROOT/'docs/mechanics'/name).exists()
            text=text.replace('{{'+token+'}}',('../mechanics/' if internal else '')+name)
        assert '{{' not in text
        write(ROOT/guide,text)
        write(ROOT/cardpath,'# Fishing '+('internal' if internal else 'public')+' recipe cards\n\n**DRAFT; required exact-review corrections in progress.** '+audience+'\n\nEvery card uses the complete [shared guide]('+Path(guide).name+'). The JSON preserves full source objects.\n\n'+'\n'.join(card_md(c,body,registry,internal) for c in cs))
        files += [jsonpath,guide,cardpath]
    historical=[{'sourceRecipeId':r['id'],'legacyName':r['legacyName'],'legacyEffect':r['legacyEffect'],
        'currentName':r['name'],'currentBody':'fishing.tackle','status':'historical-transport-backlog',
        'newRecipe':False,'vehicleStatisticsApproved':False,'note':'Preserve the historical boat concept for separate transport work; current formula creates only the admitted Tackle board.'}
        for r in recipes if r['id'] in ['recipe-172','recipe-173','recipe-177']]
    dump(AUDIT/'FISHING_HISTORICAL_TRANSPORT_BACKLOG.json',{'status':'preserved historical concepts; no new recipes',
        'entries':historical,'sporefolkAdultReference':{'sourceRecipeId':'recipe-173',
        'literalReferencePreserved':True,'aquaticEcologyAvailabilityOrHarvestEstablished':False},'cosmology':'post-push only'})
    assert all(sha(GAME/p)==h for p,h in baseline.items()),'Protected input changed'
    dump(AUDIT/'FISHING_AUTHORING_STATUS.json',{'status':STATUS,'authoredCards':44,'publicCards':28,
        'restrictedCards':3,'directorOnlyCards':13,'internalBaseModels':9,'publicBaseModels':9,
        'internalAffinities':14,'publicAffinities':13,'protectedFilesUnchanged':len(baseline),
        'recipesApproved':0,'sourceVerdict':AUTH,'exactOperationalReviewAuthority':EXACT_AUTH,'currentReviewedRecipes':348,'remainingRecipes':339,
        'outputs':{p:sha(ROOT/p) for p in files},'sourceInformationDeleted':False,
        'cosmology':'post-push only','next':'complete FI-E01..11 repairs and exact artifact verification under the captured conditional authorization'})
    print(json.dumps({'cards':44,'public':28,'models':9,'internalAffinities':14,'publicAffinities':13,
        'protectedFilesUnchanged':len(baseline),'recipesApproved':0}))


if __name__=='__main__':
    main()
