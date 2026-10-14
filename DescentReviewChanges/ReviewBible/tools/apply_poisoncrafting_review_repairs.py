"""Apply the five finite corrections in the actual Poisoncrafting exact review."""
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TURN='f8cd1339-42dc-413b-b3cb-b071aa52b12e'
REPLY='d151511f-1830-4828-8134-98c91c482444'

def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def replace_once(s,old,new):
    assert s.count(old)==1, (old[:90],s.count(old))
    return s.replace(old,new,1)

def main():
    log=AUDIT/'POISONCRAFTING_EXACT_REPAIRS_APPLIED.json'
    assert not log.exists(), 'Repairs already recorded; inspect final state.'
    review=(AUDIT/'GPT_POISONCRAFTING_EXACT_REVIEW.txt').read_text(encoding='utf-8')
    assert 'After applying the five items above' in review and 'all 41 cards' in review
    paths=[ROOT/'docs/mechanics/POISONCRAFTING_RECIPE_PLAYTEST.md',ROOT/'docs/mechanics/POISONCRAFTING_PUBLIC_RECIPE_CARDS.md',ROOT/'docs/director-only/POISONCRAFTING_INTERNAL_RECIPE_CARDS.md',ROOT/'data/playtest/poisoncrafting_recipe_candidate.json',ROOT/'data/director/poisoncrafting_recipe_candidate_internal.json']
    before={}
    for p in paths:
        backup=AUDIT/('POISONCRAFTING_BEFORE_EXACT_REPAIRS_'+p.name)
        assert not backup.exists()
        backup.write_bytes(p.read_bytes())
        before[str(p.relative_to(GAME))]=hashlib.sha256(p.read_bytes()).hexdigest()
    guide=paths[0].read_text(encoding='utf-8')
    guide=replace_once(guide,'All actual source-specific anatomical restrictions still apply. Creature type alone supplies no invented immunity. A living/active creature must be a legal target of the actual delivery and effect; a Dead body receives no active creature-condition record. Inhaled delivery specifically requires actual ambient-gas breathing. Injury and contact have the distinct physical eligibility below rather than a universal breathing requirement.',
      'Every actual source-specific anatomical restriction still applies. Creature type alone supplies no invented immunity or ineligibility. A creature must be a legal target of the actual delivery and effect. A Dead body receives no active creature-condition record. Inhaled delivery separately requires actual ambient-gas breathing; injury and contact use their own physical eligibility rules.')
    fear='A legal same-recipe/same-owner/same-target refresh of an existing Frightened record extends only that record\'s legal expiry. It retains the record\'s original fixed `fearLocus`; the later exposure does not move it. If the prior record has ended, a later failed exposure that actually establishes a new Frightened record records the new exposure point as its new `fearLocus`. A successful later save, condition immunity, or another result that fails to establish/refresh Frightened does not alter the locus.'
    guide=replace_once(guide,'For this exact-review draft, refreshing an existing Frightened record retains that record\'s original fixed fear locus; it extends the existing relationship rather than choosing a new source. Once that record ends, a later real application records its new actual exposure locus. This finite refresh clarification is submitted for exact review.',fear)
    clean='**Contact-poison cleaning — NEW.** A small object for this procedure is one handheld object whose entire coated region the cleaner can directly access while remaining in one space. Cleaning that object takes one Action. Any other eligible coated object, and a full five-foot-square coated surface patch, requires one uninterrupted active minute. In initiative, one designated cleaner must spend an Action on each of ten consecutive regular turns and at least 60 elapsed seconds must pass. If the tenth Action occurs before 60 seconds, maintain the required access until the 60-second point; no eleventh Action is required. Interruption before completion does not end the charge: the remaining single coating record and its original expiry continue. Cleaning produces only inert waste and never recoverable poison. Ordinary contact/barrier rules still apply to the cleaner during the procedure. Runoff, cloth and rinse water never become extra poison doses.'
    guide=replace_once(guide,'Cleaning destroys the charge into inert waste. One Action and actual wiping/washing access cleans one small object. One uninterrupted active minute cleans the full patch. For this exact-review draft, a larger eligible coated object also uses that one-minute procedure: one designated cleaner, ten consecutive regular-turn Actions and at least 60 seconds, with required access through resolution and no eleventh Action. A partial/interrupted cleaning does not create recoverable active stock or complete the cleanse. This timing/large-object completion is explicitly submitted for exact review. Runoff, cloth and rinse water never become extra poison doses.',clean)
    slow='All active `poisoncraft.slowed` records together contribute at most one ×1/2 multiplier to each applicable movement speed. A distinct independently lawful effect that expressly halves the same movement speed contributes its own multiplier unless that effect says otherwise; two such independent ×1/2 sources therefore produce ×1/4. Speed 0 remains 0. A rule that increases movement cost rather than actually halving Speed remains a movement-cost rule and is not converted into another ×1/2 multiplier. Each individual modifier source is applied at most once to a final movement mode; a movement mode dynamically derived from another already-modified mode inherits that result and does not receive the same source\'s multiplier a second time merely because the modifier nominally covers both modes.'
    guide=replace_once(guide,'Other independently applicable movement modifiers retain their reviewed scopes; this permission does not create an additional universal modifier rule.','\n\n**Slowed composition — NEW.** '+slow)
    auto='**Venom Master — automatic failure.** If a legitimate crafted injury-poison exposure requires its initial CON save and an applicable rule causes that save to automatically fail, that is a failed initial poison save for Venom Master. No physical d20 roll is required. This does not apply when explicit whole-poison-effect/toxin immunity prevents the application itself, because in that case no legitimate initial poison save is required. An unnecessary die rolled despite such immunity cannot trigger Venom Master. This remains after the qualifying critical hit and cannot retroactively penalize the triggering poison save.'
    guide=replace_once(guide,'For exact review, the treatment of a legitimate source-mandated automatic CON failure is explicitly queried alongside the requirement that an unnecessary die for a wholly immune application cannot trigger this feature.','\n\n'+auto)
    paths[0].write_text(guide,encoding='utf-8')
    texts={p:p.read_text(encoding='utf-8') for p in paths[1:3]}
    for p in paths[3:]:
        x=json.loads(p.read_text(encoding='utf-8'))
        x['pendingBindings']=[]
        x['thiefIntegration']['venomMaster'].update(automaticRequiredInitialSaveFailureCountsAsFailure=True,physicalDieRollRequired=False,wholeApplicationImmunityMeansNoQualifyingSave=True)
        for c in x['cards']:
            o=c['operational'];e=o['effect'];profile=e['conditionProfile'];old=o['text']
            e.update(creatureTypeAloneCreatesImmunity=False,creatureTypeAloneCreatesIneligibility=False,deadBodyReceivesActiveConditionRecord=False)
            if e['condition']=='frightened':
                profile.update(fearLocus='actual exposure point when the record is first established',sameIdentityRefreshRetainsOriginalLocus=True,newRecordUsesNewExposureLocus=True)
                profile['text']+=' '+fear
                o['text']+=' '+fear
            if e['condition']=='slowed':
                profile.update(distinctIndependentSpeedHalvingsCompose=True,distinctHalvingComposition='multiplicative',sameModifierSourceAppliedAtMostOncePerFinalMovementMode=True,derivedModeDoesNotReapplyInheritedModifierSource=True,movementCostRulesRemainSeparate=True,hardZeroRemainsZero=True)
                profile['text']+=' '+slow
                o['text']+=' '+slow
            if c['sourceMechanics']['delivery']=='contact':
                o['delivery'].update(singleActionCleaningEligibility='handheld object whose entire coated region is directly accessible while cleaner remains in one space',largeObjectOrPatchCleaningRegularTurnActions=10,largeObjectOrPatchCleaningMinimumElapsedSeconds=60,largeObjectOrPatchCleaningRequiresConsecutiveRegularTurns=True,largeObjectOrPatchCleaningRequiresContinuousAccess=True,eleventhActionRequired=False,interruptionLeavesChargePresent=True,interruptionPreservesOriginalChargeExpiry=True,ordinaryContactAndBarrierRulesApplyDuringCleaning=True)
            if p==paths[4] and old!=o['text']:
                for md,s in texts.items():
                    if md==paths[1] and c['visibility']!='public':continue
                    # Identical source effects can produce identical operational paragraphs.
                    # Replace the exact paragraph inside this card's unique section only.
                    begin=s.index('## '+c['recipeId']+' — ')
                    end=s.find('\n## recipe-',begin+1)
                    if end<0:end=len(s)
                    segment=replace_once(s[begin:end],'**Operational effect:** '+old,'**Operational effect:** '+o['text'])
                    texts[md]=s[:begin]+segment+s[end:]
        dump(p,x)
    for p,s in texts.items():p.write_text(s,encoding='utf-8')
    repairs=[
      'Retain the original fixed fear locus when an existing same-identity Frightened record refreshes; only an actually established new record records a new locus.',
      'Define handheld/single-space cleaning eligibility; encode ten consecutive regular Actions AND 60 seconds for other objects/patches, original charge/expiry on interruption, and ordinary cleaner exposure rules.',
      'Count a legitimate required initial CON save that automatically fails for Venom Master; a physical die is unnecessary and whole-application immunity supplies no qualifying save.',
      'Compose distinct lawful speed halvings multiplicatively, retain one Poisoncraft Slowed multiplier, and never reapply a modifier inherited by a derived movement mode; movement cost stays separate.',
      'Remove living-type eligibility; creature type alone supplies no poison immunity or ineligibility, while actual delivery anatomy, breathing and Dead-body restrictions remain.'
    ]
    dump(log,{'exactReviewTurnId':TURN,'exactReplyId':REPLY,'repairs':repairs,'beforeHashes':before,'sourceInformationDeleted':0,'pendingBindingsCleared':True})
    print(json.dumps({'repairsApplied':len(repairs),'artifactsUpdated':len(paths),'sourceInformationDeleted':0}))

if __name__=='__main__':main()
