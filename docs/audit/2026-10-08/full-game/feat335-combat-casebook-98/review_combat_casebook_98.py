"""One-shot full combat-feat casebook review; no game runtime or imported code."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import json,hashlib,math,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';I=R/'data/director/feat_candidates/exact_01';D=A/'feat335-ft84-derived-review-92/after/DescentReviewChanges/ReviewBible'
ROOT=A/'feat335-combat-casebook-98';OUT=A/'FEAT335_COMBAT_ORIGINAL_CASEBOOK_REVIEW_98.json';ZIP=A/'DD_Feat335_Combat_Casebook_Review_98.zip';SAVED=A/Path(__file__).name
for p in [ROOT,OUT,ZIP,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(p,b):
 with p.open('xb') as f:f.write(b)
checks=[]
def ck(n,ok):checks.append({'check':n,'pass':bool(ok)});assert ok,n
candidate=j(I/'candidate.json');selected=[r for r in candidate['records'] if r['cohort']=='combat'];records={r['id']:r for r in selected}
cases=[x for x in j(I/'example_dispositions.json')['cases'] if x['featId'] in records];boundaries=[x for x in j(I/'additional_boundary_expectations.json')['cases'] if x['featId'] in records]
ck('47 full procedures94 originals2 boundaries',len(selected)==47 and len(cases)==94 and len(boundaries)==2)
notes={
'CF-01':[
'The actual direct piercing event resolves against AC17 and deals4 before creating the later minus1 layer. Natural or unarmored defense is eligible; positive tempHP absorption can qualify, but zero prevented damage or copied/periodic origins do not.',
'Two actual owners retain two deadline records but supply one minus1 family. Expiry of the earlier record cannot delete the still-live later record or permanently alter an armor item.'],
'CF-02':[
'The current replacement explicitly admits the commander among three distinct willing hearing/understanding recipients. The Action and SR use pay once; each actual mover, including the commander, spends their own available Reaction and separate half-current-Speed movement budget. The original terrain example remains preserved and valid within that conditional movement scope.',
'Recipient order is fixed. A hazard-induced Incapacitated state before recipient2 resolves prevents its Reaction, with no replacement selection or commander refund. Recipient3 still independently checks current range, hearing, willingness, position and capability.'],
'CF-03':[
'One added base weapon die from a2d6 expression is1d6, so the actual critical doubles three dice to6d6. Flat modifiers are not doubled, and the old percent wording does not add another multiplier.',
'Activation on original turn4 selects future regular starts5and6 and ends at6. A skipped turn retains its virtual marker and an extra turn adds no regular expiry marker. This operating rage still does not satisfy Frenzied Rage acquisition by name.'],
'CF-04':[
'The actual application snapshots PB3 into MedicineDC13. A legal adjacent Action/usable hand/injury-access check totaling13 ends only the chosen owner record; no kit charge is invented and another owner record remains.',
'Competition occurs only at identical due target regular-start markers. A stronger expected-damage group wins, but the losing Bleeding Edge still consumes each due tick: two losses leave one of its three ticks, not a banked retry.'],
'CF-05':[
'PB3 plus CON2 supplies5 prevention against the whole resolved direct event after passives and before tempHP. Mixed components consume that one allowance in stable order; it does not subtract5 from every component or reduce attached conditions.',
'The actual outward5ft and return5ft are two positional displacements. Returning to the same square does not clear displacement history, so Brace remains unavailable until its next original regular-start reset.'],
'CF-06':[
'The actually complete route requires10 movement cost for the occupied difficult square plus5 for the exit. From20 it leaves5. The guard lacking a Reaction permits passage, but does not erase other threats, hazards or the feat claim.',
'The special legal entry attack resolves before crossing. A hit leaves the rogue in the last legal outside space, commits the10-point attempted entry cost and the once-turn allowance, and retains actual damage and other consequences.'],
'CF-07':[
'After the qualifying continuous same-turn voluntary approach and actual melee hit, normal damage resolves before the save. On failure a wall can limit push to0 while independently eligible Prone still applies; no new size ceiling is imported.',
'Teleport and carried movement do not supply the required personal continuous10ft straight approach. Meeting the geometric endpoint alone cannot activate the rider.'],
'CF-08':[
'A real two-handed melee attack causing a genuine hostile positive-to-zero transition after floors qualifies even if the victim survives dying. The legal acquired feat, own turn, different reachable target and still-available Bonus Action are separate gates.',
'The follow-up consumes the same finite Bonus Action wallet. Its own drop grants no second Bonus Action or recursive free attack, and an off-turn trigger cannot be banked.'],
'CF-09':[
'The ray is an actual ranged spell attack, so the feat removes only the nearby seeing non-Incapacitated hostile cause of disadvantage. It creates no generic ranged-attack opportunity penalty for everyone else.',
'The long-range cause remains after proximity is removed. All surviving advantage/disadvantage still cancel normally, and separate movement or casting opportunity triggers retain their own source scope.'],
'CF-10':[
'Conscious surprise prevention removes the current surprise prohibition without restoring a spent Reaction or missed turn. The plus1AC is tied to the encounter numbered round1, including an actual extra turn in that same round.',
'A round3 entrant has no personal first-round AC reset. The independently conscious surprise protection still works, retaining the underlying surprise schedule if consciousness changes.'],
'CF-11':[
'A legal own-turn weapon attack may miss and still fund its post-attack slide. The separate5-cost budget pays the real ground/path and suppresses opportunity attacks only from the declared target; it grants neither an attack nor broader immunity.',
'One complete difficult5ft tile costs10, exceeding the separate5-point budget. Ordinary movement cannot be silently pooled into that feature operation, and Speed0 remains disqualifying.'],
'CF-12':[
'A thrown dagger is a melee-class weapon with Finesse even though the actual attack is ranged. Its hit can apply the literal branch, lowering30/40 modes to20/30 absent stronger control; no positive-damage gate is added.',
'Two owners preserve separate expiries for one minus10 identity layer. Final shared FS04 evaluates other hostile slows against the same pre-control Speed and selects the lowest result; the individual draft phrase cannot authorize additive slow stacking.'],
'CF-13':[
'With otherwise-currentAC17, floor15percent is2, producing19. The stance occupies the normal stance choice and computes before percentage-AC additions; no round-up or percent-on-percent bonus appears.',
'A forced push is allowed and retains the AC record. During the current restricted turn the holder still cannot voluntarily teleport, while source-permitted off-turn Reaction movement is a distinct window.'],
'CF-14':[
'Payment removes one actual base die before critical doubling. A one-die sword therefore has zero base sword dice left on the critical; independent legal riders and flats remain, and no spent rider die substitutes for payment.',
'A real non-droppable bond can prevent the later drop but does not refund the already forgone die. The procedure does not sever a curse/bond, damage the object or manufacture another damage die.'],
'CF-15':[
'An actual ranged-weapon Attack Action trigger and legal same-turn Bonus Action supply two separate bow attacks with two real arrows. The second omits positiveDEX3; no thrown-melee classification shortcut or loading bypass is supplied.',
'A negativeDEX modifier remains on the second damage expression. A weapon permitted only one shot in its source interval cannot make an illegal second shot merely because the Bonus Action exists.'],
'CF-16':[
'Drawing a genuinely sheathed1d6 weapon with real draw permission and declaring before the roll adds one base die, so a critical doubles two dice to4d6. The feat does not supply a hand, interaction or attack.',
'The declaration spends the encounter use even on a miss. A new weapon, resheathing, initiative exit or new turn within the same continuous fight does not restore it.'],
'CF-17':[
'Before damage,2times10 is less than21 and2times11 is not. TemporaryHP is excluded from the predicate, and this hidden adjudication does not disclose targetHP to the attacker.',
'A natural19 in the expanded range still requires total at leastAC. Total18 against20 misses; only natural20 retains the ordinary automatic-hit rule.'],
'CF-18':[
'Opposed17 beats14 with no task-degree or natural shift. The actual owner next attack compares against16 instead of18, and declaration consumes the mark even if that attack misses.',
'An ally cannot spend the owner-specific next-attack record. Its intervening attack gets no Feint reduction and leaves the owner mark available until its original deadline or replacement.'],
'CF-19':[
'The initiator adds4 to12 for16; the initial defender stays15 because the escape penalty applies only to an actual later Escape Action. The real hand, reach, size and attack replacement remain required.',
'On the selected hold escape18 becomes14 and maintenance13 becomes17. These are the two expressly different sides; another grappler adds neither a second minus4 nor an extra maintaining bonus to this contest.'],
'CF-20':[
'A5ft sword receives10ft reach for one declared melee weapon attack, then returns to5. This never grants movement, an additional attack, persistent threatened space or grapple reach.',
'A10ft weapon can make one15ft attack but restores10ft reach afterward. Movement from15to20 is entirely outside that ordinary threat boundary, so the old lunge cannot supply an opportunity trigger.'],
'CF-21':[
'Dash adds its ordinary Speed contribution to the movement cap. A failed legal Large-guard save plus an actual side destination clearing the whole route permits passage, using real costs and ordinary opportunity triggers.',
'No clearing destination means the special passage stays blocked even after failed save. The attempted first step is paid; the guard is not teleported through a wall and a second Dash does not reopen the same creature challenge.'],
'CF-22':[
'The STR-based melee weapon trade pays minus2 on the actual roll and adds floor19times20percent=3 on a hit for22. It cannot be combined with Precision Strike on that attack.',
'Power Attack and the independently eligible Giant Slayer each compute floor20times20percent=4 from the same native20. Their increments total8 for28; no compounded28.8, combined rounding shortcut or external-rider base is imported.'],
'CF-23':[
'The explicit NEW useful completion ignores half cover supplied solely by actual allied bodies in the shot path. It removes that cause of the2AC comparison while preserving real target and line legality.',
'A stone wall remains a separate actual half-cover cause even with an adjacent ally. This feat removes neither terrain cover nor hostile-body/three-quarters/total cover and invents no general shooting-into-melee disadvantage.'],
'CF-24':[
'Actual Thrown ranged use doubles20 normal to40 while long60 stays fixed, with plus1attack. Melee stabbing with that weapon does not receive the thrown-only benefits.',
'The hypothetical actual40/60 profile caps doubled normal80 at60, retaining a hard maximum60. A profile with no long-range interval gains no invented extension.'],
'CF-25':[
'The enemy is already Prone before the attack damage, so one eligible direct hit gets flatPB4. A critical does not double it to8 or apply it to every native component.',
'Bull Rush applies its Prone rider after normal damage. That newly created condition cannot retroactively qualify Punishing Blow on the same hit; a later separately legal attack can check the new state.'],
'CF-26':[
'One1d8 native weapon plus one added base die becomes4d8 on an actual critical. The feature grants no new attack and does not double flat modifiers.',
'Unseen-target disadvantage cancels the one-attack advantage, but the declared extra die on a hit and attacks-against vulnerability remain. Misses and canceled advantage do not refund the chosen downside.'],
'CF-27':[
'The seen adjacent attacker actually misses while Dodge applies and the defender has usableSpeed30. A real available attack-capable Reaction can pay one legal counterattack in reach, subject to the regular-interval and causal-root caps.',
'A parry using the only Reaction leaves none for Riposte. Reducing a hit to zero damage is also not turning it into a miss; neither a zero-damage hit nor defensive-only extra Reaction establishes eligibility.'],
'CF-28':[
'Consecutive hits have prior counts0,1,2. AtPB3 the owner may spend the actual-turn allowance for1 on hit2 or retain it for2 on hit3, never both. Nonattack actions do not reset the actual encounter chain.',
'The missed off-turn melee attack is part of the real sequence and breaks the chain. The next hit begins count1 with no prior-hit bonus; its own turn identity cannot recreate the lost chain.'],
'CF-29':[
'A chosen shield contributes its actual2 plus own enhancement1; failed save suppresses all3 and any dependent featAC through target-next-original-start. It does not break the body or suppress unrelated traits.',
'Each selected rider needs its own unspent native base die before critical doubling. A one-die weapon cannot fund both; an actual two-die weapon can pay two distinct dice if every other predicate is met.'],
'CF-30':[
'With actual shield proficiency, STR3+PB3 attacks at6, damage1d4+3 and optional stunDC8+3+3=14. The hit-stage SR stun payment and later CON save do not create another Bonus Action.',
'A stun beginning after the enemy regular turn can block interim Reactions but expires at that enemy next regular start before voluntary decisions. Immunity and the shared hard-denial ledger still apply; this is not a whole next-turn theft.'],
'CF-31':[
'The successful DEX save ordinarily gives12/2=6. Actual shield interposition and an available paid Reaction change that save damage to0 before damage, leaving independently attached conditions unchanged.',
'A failed save does not qualify and keeps the source failure damage. Physical interposition/origin and shield usability remain actual gates, not universal immunity to areas.'],
'CF-32':[
'An actual worn chain suit supplies at least2 eligible physical contribution points, so a legal ranged-class weapon attack comparesAC16 at14. The target actualAC and armor item are not permanently edited.',
'Leather base11 minus10 contributes only1 removable point;DEX5 remains, comparing16 at15. Ordinary half cover can instead fund the two-point combined budget. Magical barrier/enhancement and total-cover target denial remain.'],
'CF-33':[
'The two different conscious willing allies must actually threaten and perceive the target from opposite sides of its whole occupied footprint. The chosen owner funds one1d6 rider, doubled to2d6 on a real critical, without granting generic flanking advantage.',
'Three owners do not place three dice on one hit. Choose one funding owner before rolling and spend only its actual-turn allowance; all geometry and native-damage requirements still apply.'],
'CF-34':[
'The replacement case expressly admits a held usable melee weapon reach5 for activation and the owner as an allied recipient. The first owner attack consumes that mark entitlement even on miss. Stowing does not change the original activation or create another attack; the preserved original miss-then-hit example remains consistent.',
'Two marks give one family plus1 on the same first attack. That event consumes all applicable unspent first-attack entitlements for the actual attacker identity across those marks, so neither can be saved for a later hit.'],
'CF-35':[
'The source push5 grows once to10; an actual wall5ft away limits displacement to5. Bull Rush own Prone remains independent, without duplicate application or obstacle bypass.',
'The actual opposed Shove success is not a saving throw failure. Its push can increase to10, but contest margin7 supplies no fail-by5 save or extra Prone entitlement.'],
'CF-36':[
'PB3 limits three distinct independently legal targets inside the actual radius and normal-range shots. Three arrows and the SR use commit at declaration; each target receives its own attack/damage, not one area save or a multiplied Attack Action.',
'A later total-cover target is skipped while its committed arrow/use remain spent and no replacement is selected. Other independently legal shots can finish; Extra Attack and Double Tap do not enlarge the special Volley Action.'],
'CF-37':[
'A normallySTR longsword may useDEX4 for its attack while retainingSTR1 for damage. This attack-only substitution does not grant Finesse, weapon proficiency, lighter weight or STR-qualified Power Attack.',
'A real Finesse dagger independently permits its ownDEX damage choice. The feat does not create that property or replace a spell casting ability; an attack-modifier-based DC instead follows the actual selected attack ability.'],
'CF-38':[
'Chosen-proficient longsword natural19 totals21 and meetsAC20, producing one critical. Total18 misses despite the same natural19; acquisition choice and actual weapon type remain fixed.',
'Compare thresholds19,19and an independently applicable18 and choose18. Never add range steps to manufacture17; a critical still doubles eligible dice only once.'],
'CF-39':[
'The actual proficient whip reaches10ft and the Large target is within the one-size category limit. Opposed weapon18 beatsAcrobatics15, causing eligible Prone without damage or any hit/critical trigger.',
'An opposed tie preserves the held sword and spends the substituted Attack Action attack. It supplies no damage/on-hit resource, and Lunge cannot extend a nonattack weapon check.'],
'CF-40':[
'Actual opposite adjacent conscious melee threats establish the feat-only surrounded predicate. Native19 supplies floor1.9=1 derived cleave to one other reachable perceived hostile; recipient defenses remain and no second attack or recursive proc is created.',
'An Incapacitated surrounding creature no longer threatens for this predicate. The continuous plus1AC ends immediately and future cleave is unavailable until the real geometry/capability is restored.'],
'CF-41':[
'A real prepared Action-time Touch rank1 spell can append after the qualifying Attack Action sequence and actual hit, subject to the separate owner-regular interval and regular-creature-turn embedded limits. RP/components/route/target/concentration/Dissonance remain paid and the spell performs its own attack/save.',
'The distinct SR mode may follow a legal opportunity melee-weapon hit off-turn if both casting caps and causal permissions allow it. A one-minute Touch spell is ineligible because this completion admits only Action-time casts; it cannot compress longer, BA or Reaction casts.'],
'CF-42':[
'Actual CR7 gives observationDC10+ceil7=17. A real successful read supplies one available fact and the owner plus three actual briefed understanding recipients receive the individual Dragon breath-save plus1 through encounter end. No sealed origin, type or inferred ancestry is created.',
'The real acid-pool surcharge can be ignored during the source pursuit window, but hazard damage/saves and impassability remain. The terrain benefit is not acid resistance or unrestricted movement.'],
'CF-43':[
'For actual Berserker melee-weapon damage, the same plus2 is replaced by3, not added to5. A genuine hostile positive-to-zero can supply one own-turn free attack, but its descendant drop cannot spawn another attack in that causal root; actual acquisition remains separate from an operating rage name.',
'Three allowed time extensions contribute18seconds to the same rage use; a fourth contributes0. Original non-time endings, including actual Incapacitated where specified, still terminate it despite an extended time endpoint.'],
'CF-44':[
'The broad own direct native27 against actual Large adds floor5.4=5 for32 before defenses. Independent eligible percentages use the same base and their own floors; a copied/periodic or companion-owned packet cannot acquire it.',
'At separation15 with own reach5, a legal maximum5ft step leaves10 outside reach, so the Reaction cannot start. The Huge attacker reach15 is not borrowed. No attack roll or recursive Giant Slayer percentage belongs to the derived1d6 reaction packet.'],
'CF-45':[
'Resolved12 against targetHP3/temp4 yields only7 actual damage, with5 overkill excluded. The critical recovery base is floor7/2=3 and the distinct genuine drop recovery follows it, sharing the same finite reserve, ordinary limits and source-qualified meaningful-hostile history.',
'At level8, only2 current reserve and10missingHP cap the legal base8 recovery to2. Reserve reaches0 and later critical recovery cannot heal until the actual beneficialLR refill; blocked/fullHP events spend0 but bank no future recovery.'],
'CF-46':[
'Ordinary Precision Strike pays minus2 and adds floor21/2=10 for31 before defenses. Its once-turn trade excludes Power Attack on that same attack and does not compute from unrelated riders.',
'Grappled is an ownership-independent target alternative. Declared critical mode spends the SR use and turn claim with no minus2 or plus50percent; a hit doubles eligible dice once, while a miss spends without damage. Current predicate and critical immunity remain checked at resolution.'],
'CF-47':[
'Current self-ally scope admits the conscious holder to the fear aura; no hearing/common-language gate is added to that aura. Actual Dragon attacks receive plus2AC, whereas a merely dragonkin tag cannot satisfy the narrower Dragon predicate.',
'An actual visible Dragon ranged breath attack qualifies for the pre-roll disadvantage Reaction. A save breath instead permits a personal whole-save advantaged reroll after initial success or failure but before consequences; both modes share one SR use and actual Reaction. Non-breath ranged attacks and no-roll payloads gain no invented eligible branch.']}
ck('47 pairs of individually authored case rationales',set(notes)=={r['questionId'] for r in selected} and all(len(v)==2 and all(v) for v in notes.values()))
proposal=j(R/'data/director/combat_feat_operating_proposal_internal.json');reviews=[]
for x in cases:
 idx=int(x['sourcePointer'].rsplit('/',1)[1]);value=proposal
 for part in x['sourcePointer'].split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
 ck(x['id']+' exact complete original source case',value==x['original'])
 ck(x['id']+' exact complete current expected case',x['completeExpectedOutcome']==records[x['featId']]['workedCases'][idx])
 reviews.append({'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_CURRENT_AUTHORING_AND_EXPLICIT_CONDITIONS','reasoning':notes[x['questionId']][idx],'qualification':'Full stated-case semantic review; actual lawful acquisition, source tags, geometry, world records, actor/event budgets and causal provenance remain premises, not authenticated by these illustrations.','runtimeExecuted':False,'canonicalApplied':False})
bn={'FA-07':'The commander is one actual recipient identity and must spend their own available Reaction for movement; the other recipients own their independent wallets. No self-target creates another body, turn, Action or Reaction.','FA-08':'The exact correction includes ranged attack-roll breaths, excludes non-breath ranged attacks, and keeps saving-throw breaths in the separate personal reroll branch. No attack/save is fabricated and both branches share one actual SR use.'}
boundary_reviews=[{'id':x['id'],'featId':x['featId'],'completeOriginalDisposition':deepcopy(x),'reviewResult':'CONSISTENT_WITH_CURRENT_AUTHORING_AND_EXPLICIT_CONDITIONS','reasoning':bn[x['id']],'runtimeExecuted':False,'canonicalApplied':False} for x in boundaries]
public={r['id']:r for r in j(R/'data/public/feat_candidates/exact_01/candidate.json')['feats']};derived={r['id']:r for r in j(D/'data/director/feat_candidates/exact_01/candidate.json')['records']};dp={r['id']:r for r in j(D/'data/public/feat_candidates/exact_01/candidate.json')['feats']}
chapter=(R/'docs/feats/exact-candidate-01/COMBAT.md').read_text(encoding='utf-8-sig')
for r in selected:
 ck(r['id']+' complete FT84-derived record unchanged',r==derived[r['id']])
 ck(r['id']+' complete public procedures/cases match',all(r[k]==p[r['id']][k] for p in [public,dp] for k in ['operationalRules','workedCases']))
 ck(r['id']+' complete chapter procedures/cases',r['operationalRules'] in chapter and all(s in chapter for s in r['workedCases']))
changed=[x['id'] for x in cases if x['original']!=x['completeExpectedOutcome']]
ck('Exactly four earlier authored case replacements preserved',changed==['CF-02-E01','CF-34-E01','CF-47-E01','CF-47-E02'])
calcs=[]
def C(n,refs,inputs,actual,expected,scope):
 cid='CF98-N'+str(n).zfill(2);ck(cid+' expected result',actual==expected);calcs.append({'id':cid,'originalCaseIds':refs,'inputs':inputs,'calculatedResult':actual,'expectedResult':expected,'scope':scope,'runtimeExecuted':False})
C(1,['CF-01-E01'],{'originalAC':17,'positiveDirectPiercing':4},{'triggerComparisonAC':17,'laterComparisonAC':17-1},{'triggerComparisonAC':17,'laterComparisonAC':16},'Actual source-qualified damage event completes before the feat layer applies.')
C(2,['CF-01-E02'],{'baselineAC':17,'twoIndependentExpirySeconds':[10,20],'querySeconds':[9,10,19,20]},[17-int(any(t<end for end in [10,20])) for t in [9,10,19,20]],[16,16,16,17],'End-exclusive independent source records for the same minus1 comparison family; illustrative original deadlines, not new clock rules.')
C(3,['CF-02-E01','CF-02-E02','FA-07'],{'orderedRecipients':['commander','ally2','ally3'],'speeds':[30,30,20],'reactionsBefore':[1,1,1],'incapacitatedAtResolution':[False,True,False]},{'budgets':[s//2 if not inc else 0 for s,inc in zip([30,30,20],[False,True,False])],'reactionsAfter':[0,1,0],'commanderActionUsed':1,'commanderSRUseSpent':1},{'budgets':[15,0,10],'reactionsAfter':[0,1,0],'commanderActionUsed':1,'commanderSRUseSpent':1},'All other actual hearing/understanding/range/willingness/path predicates supplied; recipient2 cannot spend a Reaction, no replacement or refund.')
C(4,['CF-02-E01'],{'actualSpeed':30,'difficultTilePhysicalFeet':5,'costPerFoot':2},{'separateBudget':30//2,'completeTiles':(30//2)//(5*2),'completeGridDistance':((30//2)//(5*2))*5},{'separateBudget':15,'completeTiles':1,'completeGridDistance':5},'Preserved original case terrain arithmetic; continuous geometry may differ, this fixture explicitly requires complete grid tiles.')
C(5,['CF-03-E01'],{'nativeGreatswordD6Count':2,'extraBaseD6':1,'criticalDiceFactor':2},(2+1)*2,6,'Actual added weapon die, not entire2d6 expression; flats remain separately unchanged.')
C(6,['CF-03-E02'],{'activationOwnRegularNumber':4,'futureOriginalStarts':[5,6],'extraTurnBetween':True,'regular5Skipped':True},[4+n for n in [1,2]],[5,6],'Existing virtual marker6 remains the second future regular start; extra turn and skipped activity do not insert/remove markers.')
C(7,['CF-04-E01'],{'applicationPB':3,'MedicineTotal':13,'existingOwnerRecords':['A','B'],'selectedOwner':'A'},{'snapshottedDC':10+3,'success':13>=10+3,'remainingOwners':[x for x in ['A','B'] if x!='A']},{'snapshottedDC':13,'success':True,'remainingOwners':['B']},'Already-legal adjacent Medicine Action ends selected record only; no kit expenditure supplied.')
bleed_trace=[];remaining=3
for marker,stronger_due in [(1,True),(2,True),(3,False)]:
 winner='stronger2d4' if stronger_due and Fraction(10,2)>Fraction(5,2) else 'edge1d4';remaining-=1
 bleed_trace.append({'futureRegularStart':marker,'winner':winner,'edgeTicksRemaining':remaining})
C(8,['CF-04-E02'],{'edgeInitialTicks':3,'edgeExpectedDamage':'5/2','strongerExpectedDamage':5,'strongerDueStarts':[1,2]},bleed_trace,[{'futureRegularStart':1,'winner':'stronger2d4','edgeTicksRemaining':2},{'futureRegularStart':2,'winner':'stronger2d4','edgeTicksRemaining':1},{'futureRegularStart':3,'winner':'edge1d4','edgeTicksRemaining':0}],'Both groups due at identical target markers; later independent sources/ending methods are not simulated.')
def reduce_components(values,allowance):
 result=[]
 for v in values:
  paid=min(v,allowance);result.append(v-paid);allowance-=paid
 return result
C(9,['CF-05-E01'],{'stableResolvedComponents':[3,5],'PB':3,'CON':2},{'afterPrevention':reduce_components([3,5],max(0,3+2)),'totalAfter':sum(reduce_components([3,5],max(0,3+2)))},{'afterPrevention':[0,3],'totalAfter':3},'One whole direct event, after passive defenses and before real tempHP; not five prevention per component.')
C(10,['CF-05-E02'],{'actualPositionSegmentsFeet':[5,-5]},{'netPosition':sum([5,-5]),'traveledDisplacement':sum(abs(x) for x in [5,-5]),'eligibleNoDisplacement':not any(x!=0 for x in [5,-5])},{'netPosition':0,'traveledDisplacement':10,'eligibleNoDisplacement':False},'Same endpoint cannot erase actual displacement receipts.')
C(11,['CF-06-E01','CF-06-E02'],{'remainingMovementCost':20,'occupiedEntryCost':10,'legalExitCost':5},{'noReactionPassRemaining':20-10-5,'specialHitFailRemaining':20-10},{'noReactionPassRemaining':5,'specialHitFailRemaining':10},'Complete legal route and committed use assumed; special hit stops before entry and still pays first attempted step.')
C(12,['CF-07-E01'],{'PB':3,'STR':3,'saveTotal':9,'specifiedPush':5,'wallAvailableDistance':0,'proneEligible':True},{'saveDC':8+3+3,'failed':9<8+3+3,'actualPushFeet':min(5,0),'prone':9<8+3+3},{'saveDC':14,'failed':True,'actualPushFeet':0,'prone':True},'Already-eligible continuous personal approach and post-damage living target; blocked push does not cancel independent Prone.')
C(13,['CF-08-E01','CF-08-E02'],{'genuineHostileDropAfterFloor':True,'ownTurn':True,'initialBonusActions':1,'followupAlsoDrops':True},{'followupAttacks':min(1,1),'bonusActionsAfter':1-1,'furtherBonusActionAttacks':min(1,1-1)},{'followupAttacks':1,'bonusActionsAfter':0,'furtherBonusActionAttacks':0},'Actual legal two-hand attacks and target reach required; drop creates no new wallet or recursive action grant.')
def adv_state(advantages,disadvantages):return 0 if advantages and disadvantages else 1 if advantages else -1 if disadvantages else 0
C(14,['CF-09-E01','CF-09-E02'],{'disadvantageCausesBefore':[['proximity'],['proximity','longRange']]},[adv_state([], [c for c in causes if c!='proximity']) for causes in [['proximity'],['proximity','longRange']]],[0,-1],'Only the named proximity cause removed;0 ordinary and minus1 disadvantage, no new opportunity trigger.')
C(15,['CF-10-E01','CF-10-E02'],{'baselineAC':16,'numberedRounds':[1,1,3],'middleEventIsExtraTurn':True},[16+int(r==1) for r in [1,1,3]],[17,17,16],'Encounter-wide round identity; surprise and resource availability are separately sourced.')
C(16,['CF-11-E01','CF-11-E02'],{'slideBudget':5,'tileDistance':5,'terrainCostFactors':[1,2]},[5*f<=5 for f in [1,2]],[True,False],'Separate movement-cost budget with actual nonzero Speed and legal endpoint; attack target immunity does not cover other foes.')
C(17,['CF-12-E01','CF-12-E02'],{'preControlSpeeds':[30,40],'duplicateCripplingOwners':2,'independentHalfSpeedAlsoConsidered':True},{'cripplingAlone':[max(0,s-10) for s in [30,40]],'withHalfSpeed':[min(max(0,s-10),s//2) for s in [30,40]]},{'cripplingAlone':[20,30],'withHalfSpeed':[15,20]},'Final FS04 strongest adverse result from same pre-control values, not double subtraction or subtract-then-half. Preserves already spent movement.')
C(18,['CF-13-E01'],{'otherwiseCurrentACs':[17,19],'latterIncludesStillUnspentGuard2':True},{'bonuses':[math.floor(Fraction(b*15,100)) for b in [17,19]],'totals':[b+math.floor(Fraction(b*15,100)) for b in [17,19]]},{'bonuses':[2,2],'totals':[19,21]},'Real flat base before all percentageAC; losing conditional Guard recomputes base17/total19, not percent compounding.')
C(19,['CF-14-E01','CF-29-E02'],{'baseDiceCounts':[1,2],'distinctPaidDice':[1,2],'criticalFactor':2},[max(0,n-p)*2 for n,p in [(1,1),(2,2)]],[0,0],'Base-die payment precedes critical doubling. A single existing die cannot be spent by two riders; separate flat/rider components remain.')
C(20,['CF-15-E01','CF-15-E02'],{'actualSecondBowDie':4,'abilityModifiers':[3,-1],'arrowsBefore':10},{'secondDamages':[max(0,4+min(m,0)) for m in [3,-1]],'arrowsAfterTwoLegalShots':10-2},{'secondDamages':[4,3],'arrowsAfterTwoLegalShots':8},'Only if weapon loading/cadence/hands permit both shots; no invented ammo refund or restoring feature.')
C(21,['CF-16-E01'],{'nativeD6Count':1,'DrawCutAddedBaseD6':1,'criticalFactor':2},(1+1)*2,4,'Actual pre-roll draw declaration and real sheath/draw permission; a miss still spends the encounter use.')
C(22,['CF-17-E01','CF-17-E02'],{'HP':[10,11],'maximum':21,'tempHP':10,'keptNaturalFace':19,'attackTotal':18,'AC':20},{'belowHalf':[2*h<21 for h in [10,11]],'natural19Hits':18>=20},{'belowHalf':[True,False],'natural19Hits':False},'Pre-damage hidden predicate and actual AC comparison; no retroactive critical from damage loweringHP.')
C(23,['CF-18-E01','CF-18-E02'],{'Deception':17,'Insight':14,'baselineTargetAC':18,'ownerAttackTotal':13},{'contestSuccess':17>14,'ownerComparisonAC':18-2,'ownerAttackHits':13>=18-2,'allyComparisonAC':18},{'contestSuccess':True,'ownerComparisonAC':16,'ownerAttackHits':False,'allyComparisonAC':18},'Owner attack declaration consumes even on miss; ally cannot consume or benefit from owner mark.')
C(24,['CF-19-E01','CF-19-E02'],{'initiation':12,'initialDefense':15,'escape':18,'maintenance':13},{'initialTotals':[12+4,15],'initialSuccess':12+4>15,'escapeTotals':[18-4,13+4],'escapeSuccess':18-4>13+4},{'initialTotals':[16,15],'initialSuccess':True,'escapeTotals':[14,17],'escapeSuccess':False},'Two distinct sides only during selected Escape contest; ties preserve existing hold, no additional grappler penalty.')
C(25,['CF-20-E01','CF-20-E02'],{'ordinaryReaches':[5,10],'lungeIncrement':5,'laterMovement':[15,20]},{'oneAttackReaches':[v+5 for v in [5,10]],'restoredReaches':[5,10],'laterLeaves10ftReach':15<=10 and 20>10},{'oneAttackReaches':[10,15],'restoredReaches':[5,10],'laterLeaves10ftReach':False},'Attack-scoped reach ends before later movement; no persistent threat or separate maneuver extension.')
C(26,['CF-21-E01','CF-21-E02'],{'Speed':30,'legalDashCounts':[1,2],'alreadySpent':15},{'caps':[(1+n)*30 for n in [1,2]],'remaining':[(1+n)*30-15 for n in [1,2]],'sameCreatureChallengesPerActualTurn':len({'guard','guard'})},{'caps':[60,90],'remaining':[45,75],'sameCreatureChallengesPerActualTurn':1},'Dash cap math does not authorize additional Dash costs. One real challenged creature receipt remains spent despite additional Dashes; failed/no-space passage remains blocked.')
C(27,['CF-22-E01','CF-22-E02'],{'nativeDamageAmounts':[19,20],'independentEligiblePercentages':[20,20]},{'single19':19+(19*20)//100,'two20':20+sum((20*p)//100 for p in [20,20])},{'single19':22,'two20':28},'Power Attack alone19; independent Power Attack/Giant Slayer20 fixture, each floored from same native base. Precision Strike trade is excluded.')
C(28,['CF-23-E01','CF-23-E02'],{'baselineAC':16,'coverCauses':[['alliedBodyHalf'],['alliedBodyHalf','wallHalf']]},[16+(2 if any(c!='alliedBodyHalf' for c in cs) else 0) for cs in [['alliedBodyHalf'],['alliedBodyHalf','wallHalf']]],[16,18],'Only actual allied-body half cover is ignored; wall remains and no universal adjacent-ally disadvantage is added.')
C(29,['CF-24-E01','CF-24-E02'],{'actualThrownRanges':[[20,60],[40,60]]},[[min(normal*2,long),long] for normal,long in [(20,60),(40,60)]],[[40,60],[60,60]],'Actual ranged Thrown use only; no change to long range, melee use or missing interval.')
C(30,['CF-25-E01','CF-25-E02'],{'PB':4,'targetProneBeforeDamage':[True,False],'secondTargetBecomesProneAfterDamage':True,'critical':True},[4 if prone else 0 for prone in [True,False]],[4,0],'Flat once per native hit, never critical doubled or retroactive from after-damage Bull Rush.')
C(31,['CF-26-E01','CF-26-E02'],{'nativeD8Count':1,'additionalBaseD8':1,'critical':True,'unseenTargetDisadvantage':True},{'criticalD8Count':(1+1)*2,'netAttackAdvantage':adv_state(['reckless'],['unseen']),'attacksAgainstAdvantagePersists':True},{'criticalD8Count':4,'netAttackAdvantage':0,'attacksAgainstAdvantagePersists':True},'Countervailing disadvantage cancels only roll advantage; declared extra die and downside persist under their exact durations.')
C(32,['CF-27-E01','CF-27-E02'],{'reactionWalletsAfterDefense':[1,0],'qualifiedDodgeOrParryMiss':True},[min(1,w) for w in [1,0]],[1,0],'Other reach/weapon/capability/regular-interval and causal-root checks assumed. A defensive-only grant is not an attack-capable wallet.')
def momentum_choose(chosen_hit):
 count=0;used=False;bonuses=[]
 for hit_number in [1,2,3]:
  prior=count;count+=1;bonus=min(3,prior) if hit_number==chosen_hit and prior>0 and not used else 0
  if bonus:used=True
  bonuses.append(bonus)
 return bonuses
C(33,['CF-28-E01'],{'threeSameTargetHits':True,'PB':3,'oneActualTurn':True},{'chooseHit2':momentum_choose(2),'chooseHit3':momentum_choose(3)},{'chooseHit2':[0,1,0],'chooseHit3':[0,0,2]},'Distinct selection branches within one real actual turn; no multiple bonus spending.')
count=2;momentum_trace=[]
for hit in [False,True]:
 prior=count if hit else 0;count=count+1 if hit else 0;momentum_trace.append({'hit':hit,'priorEligibleHits':prior,'chainAfter':count})
C(34,['CF-28-E02'],{'priorChain':2,'eventSequence':['missedOpportunityAttack','nextMeleeHit']},momentum_trace,[{'hit':False,'priorEligibleHits':0,'chainAfter':0},{'hit':True,'priorEligibleHits':0,'chainAfter':1}],'The actual off-turn attack participates in chain history; changing turn does not repair a broken sequence.')
C(35,['CF-29-E01'],{'otherwiseAC':14,'shieldPhysical':2,'shieldEnhancement':1,'actualDependentShieldExpert':1},{'before':14+2+1+1,'chosenShieldContributionSuppressed':2+1,'dependentFeatSuppressed':1,'after':14},{'before':18,'chosenShieldContributionSuppressed':3,'dependentFeatSuppressed':1,'after':14},'Conditional additionally owned Shield Expert explicitly requires shield contribution. Other independent AC and item traits remain outside the suppression.')
C(36,['CF-30-E01'],{'STR':3,'PB':3,'actualShieldProficiency':True,'bashDie':3},{'attackModifier':3+3,'normalDamage':3+3,'stunDC':8+3+3},{'attackModifier':6,'normalDamage':6,'stunDC':14},'Actual Attack Action/BA/usable shield/hand and optional hit-stage SR expenditure remain independent prerequisites.')
C(37,['CF-30-E02'],{'applySecond':1,'targetNextOriginalRegularStartSecond':6,'queries':[5,6]},[1<=t<6 for t in [5,6]],[True,False],'Stunned expires at target start before voluntary decisions; this calculation does not bypass immunity/hard-denial admission.')
C(38,['CF-31-E01','CF-31-E02'],{'failureFire':12,'successfulDEXHalfDamage':True,'interpositionAndReaction':True},{'ordinarySuccess':12//2,'featSuccess':0,'failedSave':12},{'ordinarySuccess':6,'featSuccess':0,'failedSave':12},'Only successful-save damage becomes0. Nondamage outcomes, physical line/origin and shield availability remain real.')
def sure_shot(actual_ac,suit_base,ordinary_cover=0):
 removable_cover=min(2,ordinary_cover);removable_suit=min(2-removable_cover,max(0,suit_base-10));return actual_ac-removable_cover-removable_suit
C(39,['CF-32-E01','CF-32-E02'],{'profiles':[{'AC':16,'suitBase':16,'cover':0},{'AC':16,'suitBase':11,'cover':0},{'AC':18,'suitBase':11,'cover':2}]},[sure_shot(16,16),sure_shot(16,11),sure_shot(18,11,2)],[14,15,16],'One combined two-point budget, ordinary cover first then physical suit contribution. DEX/magical enhancements/barriers/shields excluded; total cover still untargetable.')
def crosses_open_rect(p,q,box):
 lo=Fraction(0);hi=Fraction(1)
 for a,b,mn,mx in zip(p,q,box[:2],box[2:]):
  delta=b-a
  if delta==0:
   if not mn<a<mx:return False
  else:
   x,y=sorted([Fraction(mn-a,delta),Fraction(mx-a,delta)]);lo=max(lo,x);hi=min(hi,y)
 return lo<hi
geometry_fixtures=[{'p':[-10,0],'q':[10,0],'box':[-5,-5,5,5]},{'p':[-15,5],'q':[15,5],'box':[-10,-10,10,10]},{'p':[-15,-5],'q':[-15,5],'box':[-10,-10,10,10]},{'p':[-15,5],'q':[-5,15],'box':[-10,-10,10,10]}]
C(40,['CF-33-E01','CF-40-E01'],{'coordinateUnits':'half-feet; axis-aligned occupied footprints','fixtures':geometry_fixtures,'allOtherThreatPerceptionAndCapabilityPredicates':True},[crosses_open_rect(x['p'],x['q'],x['box']) for x in geometry_fixtures],[True,True,False,False],'Bounded planar center-segment geometry: opposite Medium and Large footprints qualify; same side and corner-only touch do not. No elevation, unseen bodies or generic flanking advantage implemented.')
C(41,['CF-33-E01','CF-33-E02'],{'actualFundingOwnersAvailable':3,'chosenFundingOwnerCount':1,'nativeRiderD6':1,'criticalDiceFactor':2},{'riderD6Count':1*2,'ownerClaimsSpent':1},{'riderD6Count':2,'ownerClaimsSpent':1},'One family rider per actual hit; other owners retain their claims, no three-die stacking.')
mark_receipts={'markA':set(),'markB':set()};mark_trace=[]
for attacker,result in [('owner','miss'),('owner','hit')]:
 eligible=[m for m,used in mark_receipts.items() if attacker not in used]
 for m in eligible:mark_receipts[m].add(attacker)
 mark_trace.append({'attacker':attacker,'result':result,'bonus':int(bool(eligible)),'claimsConsumed':eligible})
C(42,['CF-34-E01','CF-34-E02'],{'twoActiveActualMarks':True,'allianceAndActivationRangeLegal':True,'orderedAttacks':['ownerMiss','ownerHit']},mark_trace,[{'attacker':'owner','result':'miss','bonus':1,'claimsConsumed':['markA','markB']},{'attacker':'owner','result':'hit','bonus':0,'claimsConsumed':[]}],'Self-ally and all-applicable first-attack consumption, not a per-turn bonus. Stowing weapon and alliance churn do not clear receipts.')
C(43,['CF-35-E01','CF-35-E02'],{'originalPushFeet':5,'featAddedFeet':5,'wallDistance':5,'ordinaryShoveContestMargin':7},{'specifiedDistance':5+5,'actualWallLimitedDistance':min(5+5,5),'shoveGrantsSaveMarginProne':False},{'specifiedDistance':10,'actualWallLimitedDistance':5,'shoveGrantsSaveMarginProne':False},'Direct actual source pushes only; ordinary opposed contest has no numerical saving-throw failure margin.')
volley_targets=[{'id':'A','xy':[25,0],'laterLegal':True,'face':15,'AC':16},{'id':'B','xy':[30,5],'laterLegal':False,'face':None,'AC':16},{'id':'C','xy':[35,0],'laterLegal':True,'face':3,'AC':16}]
shots=[{'id':t['id'],'attackTotal':t['face']+5,'hit':t['face']+5>=t['AC']} for t in volley_targets if t['laterLegal']]
C(44,['CF-36-E01','CF-36-E02'],{'PB':3,'point':[30,0],'areaRadius':10,'bowNormalRange':80,'shooter':[0,0],'arrowsBefore':10,'attackModifier':5,'lockedTargets':volley_targets},{'initialRangeGeometryLegal':all((t['xy'][0]-30)**2+t['xy'][1]**2<=10**2 and t['xy'][0]**2+t['xy'][1]**2<=80**2 for t in volley_targets),'arrowsAfterCommit':10-len(volley_targets),'shots':shots},{'initialRangeGeometryLegal':True,'arrowsAfterCommit':7,'shots':[{'id':'A','attackTotal':20,'hit':True},{'id':'C','attackTotal':8,'hit':False}]},'All targets initially perceived/line legal, adequate real bow cadence and paid special Action/SR use; B later gains total cover, so no B roll/replacement/refund. Independent hit damage remains its native source.')
C(45,['CF-37-E01','CF-37-E02'],{'STR':1,'DEX':4,'PB':3,'longswordDie':4,'daggerDie':3},{'longswordAttackModifier':4+3,'longswordDamage':4+1,'actualFinesseDaggerDamage':3+4,'attackAbilityDC':8+3+4,'STRFixedBullRushDC':8+3+1},{'longswordAttackModifier':7,'longswordDamage':5,'actualFinesseDaggerDamage':7,'attackAbilityDC':15,'STRFixedBullRushDC':12},'Source attack-only DEX substitution, plus separate genuine dagger Finesse; no spell ability substitution or granted proficiency.')
C(46,['CF-38-E01','CF-38-E02'],{'naturalFace':19,'totals':[21,18],'AC':20,'applicableThresholds':[19,19,18]},{'critResults':[19>=19 and total>=20 for total in [21,18]],'broadestThreshold':min(19,19,18)},{'critResults':[True,False],'broadestThreshold':18},'Compare actual ranges rather than sum expansions; natural19 still requires hit.')
C(47,['CF-39-E01','CF-39-E02'],{'actualWhipReach':10,'targetDistance':10,'weaponCheck':18,'opposingChecks':[15,18]},{'inReach':10<=10,'contestSuccess':[18>d for d in [15,18]],'damage':0},{'inReach':True,'contestSuccess':[True,False],'damage':0},'Target size/body and real control mode required; opposed check is not attack/hit/critical, ties preserve state.')
C(48,['CF-40-E01','CF-40-E02'],{'otherwiseAC':17,'oppositeHostilesActive':[True,False],'nativeWeaponDamage':19},{'ACs':[17+int(ok) for ok in [True,False]],'legalCleaveAmounts':[(19*10)//100 if ok else 0 for ok in [True,False]]},{'ACs':[18,17],'legalCleaveAmounts':[1,0]},'Second state loses a real surrounding melee threat; one derived packet only, before its actual recipient defenses and no recursive proc.')
def append_eligibility(action_time,rank,touch,self_only,hit_target,ordinary_mode):
 return action_time and (touch or self_only) and (not touch or hit_target) and (not ordinary_mode or rank in [0,1])
C(49,['CF-41-E01','CF-41-E02'],{'fixtures':[{'ActionTime':True,'rank':1,'Touch':True,'hitTarget':True,'ordinary':True},{'ActionTime':True,'rank':5,'Touch':True,'hitTarget':True,'ordinary':False},{'ActionTime':False,'rank':1,'Touch':True,'hitTarget':True,'ordinary':False}]},[append_eligibility(True,1,True,False,True,True),append_eligibility(True,5,True,False,True,False),append_eligibility(False,1,True,False,True,False)],[True,True,False],'Partial admission projection only: second fixture assumes independently legitimate rank5 access, paid SR mode and all source costs; no actual spell, access or cast is created.')
C(50,['CF-41-E01'],{'initialRP':10,'independentlyQuotedActualSpellPrice':3,'swordAttackHits':True,'actualSpellAttackFace':6,'spellAttackModifier':5,'targetAC':14},{'RPAfterCommit':10-3,'spellAttackTotal':6+5,'spellAttackHits':6+5>=14},{'RPAfterCommit':7,'spellAttackTotal':11,'spellAttackHits':False},'Synthetic legal already-quoted spell operation, not a new spell price. Sword hit does not substitute for the actual independent spell roll; all ordinary cast/history/component requirements remain.')
C(51,['CF-42-E01'],{'actualCRs':['7','7/2',None]},[10+math.ceil(Fraction(c)) if c is not None else 15 for c in ['7','7/2',None]],[17,14,15],'Exact observed creature CR retained; no-CR fallback is15, not guessed type or sealed origin.')
C(52,['CF-42-E02'],{'actualPoolPathFeet':10,'difficultCostFactor':2,'pursuitBenefitActive':True},{'ordinaryMovementCost':10*2,'featureMovementCost':10,'hazardDamageWaived':False},{'ordinaryMovementCost':20,'featureMovementCost':10,'hazardDamageWaived':False},'Only actual source lair difficulty surcharge in its limited pursuit window, not acid immunity or passage through solid terrain.')
C(53,['CF-43-E01','CF-43-E02'],{'actualBerserkerFlat':2,'replacementFlat':3,'extensionOffers':4,'maximumExtensions':3,'secondsPerOriginalRound':6},{'operativeFlat':3,'extensionAccepted':[i<3 for i in range(4)],'totalAddedSeconds':min(4,3)*6},{'operativeFlat':3,'extensionAccepted':[True,True,True,False],'totalAddedSeconds':18},'Own qualifying current rage and genuine drop receipts assumed; causal attack-chain prohibition and non-time endings remain independent.')
C(54,['CF-44-E01','CF-44-E02'],{'actualLargeNativeDamage':27,'distanceFromHugeAttacker':15,'ownReach':5,'separateStepBudget':5,'terrainCostFactor':1},{'percentBonus':27*20//100,'totalBeforeDefense':27+27*20//100,'bestPostStepDistance':15-5,'canBeginReaction':15-5<=5},{'percentBonus':5,'totalBeforeDefense':32,'bestPostStepDistance':10,'canBeginReaction':False},'Straight unobstructed best-case approach still cannot enter OWN reach; attacker15ft reach does not transfer.')
def recover(raw,hp,maximum,reserve):
 gain=max(0,min(raw,maximum-hp,reserve));return hp+gain,reserve-gain,gain
actual_damage=min(12,4)+min(max(0,12-4),3);self_hp=10;reserve=16;life_trace=[]
for label,raw in [('critical',actual_damage//2),('drop',8)]:
 before={'HP':self_hp,'reserve':reserve};self_hp,reserve,gain=recover(raw,self_hp,30,reserve);life_trace.append({'event':label,'base':raw,'before':before,'actualRestored':gain,'after':{'HP':self_hp,'reserve':reserve}})
C(55,['CF-45-E01'],{'victimHP':3,'victimTempHP':4,'resolvedIncoming':12,'victimEffectiveMaximum':20,'victimPriorWounds':0,'actualWoundSaveTotal':15,'livingOwnerLevel':8,'ownerInitialHP':10,'ownerMaximumHP':30,'ownerInitialReserve':16,'genuineMeaningfulHostileAndRewardEligibleOrigin':True},{'actualDamage':actual_damage,'overkill':12-actual_damage,'lifeTrace':life_trace},{'actualDamage':7,'overkill':5,'lifeTrace':[{'event':'critical','base':3,'before':{'HP':10,'reserve':16},'actualRestored':3,'after':{'HP':13,'reserve':13}},{'event':'drop','base':8,'before':{'HP':13,'reserve':13},'actualRestored':8,'after':{'HP':21,'reserve':5}}]},'Damage/healing reference projection under explicit no-block/no-modifier/no-Critical-cap fixture. Victim survives actual Core processing at0; this does not authenticate a campaign or implement all lethal-state transitions.')
C(56,['CF-45-E02'],{'level':8,'HP':20,'maximumHP':30,'currentReserve':2,'dropHealingBase':8},list(recover(8,20,30,2)),[22,0,2],'Actual restoredHP spends only2 reserve; no stored surplus or recovery before a real beneficialLR.')
C(57,['CF-46-E01','CF-46-E02'],{'nativeOrdinaryDamage':21,'ordinaryPenalty':-2,'criticalModeOriginalD8Count':1,'criticalModeUseDeclared':True},{'ordinaryBonus':21*50//100,'ordinaryTotal':21+21*50//100,'criticalModeD8Count':1*2,'criticalModeFeatPercentBonus':0,'criticalModeAttackPenalty':0},{'ordinaryBonus':10,'ordinaryTotal':31,'criticalModeD8Count':2,'criticalModeFeatPercentBonus':0,'criticalModeAttackPenalty':0},'Modes replace each other and both exclude Power Attack trade; miss spends the real declared SR/turn claim.')
C(58,['CF-47-E01'],{'otherwiseAC':17,'actualAttackerTypes':['Dragon','dragonkin'],'consciousOwnerAtAuraDistance':0,'auraRadius':30},{'ACs':[17+(2 if t=='Dragon' else 0) for t in ['Dragon','dragonkin']],'ownerInAura':0<=30},{'ACs':[19,17],'ownerInAura':True},'Exact creature facts required; own fear-save aura needs consciousness/line, no invented hearing/language gate.')
C(59,['CF-47-E02','FA-08'],{'seenActualDragon':True,'attackKinds':['rangedBreath','rangedNonBreath','meleeNonBreath'],'ordinaryAdvantageFaces':[17,5]},[kind in ['rangedBreath','meleeNonBreath'] for kind in ['rangedBreath','rangedNonBreath','meleeNonBreath']],[True,False,True],'Legal pre-roll paid attack branch; saving-throw/no-roll payloads are different branches, not coerced into attacks.')
C(60,['CF-47-E02','FA-08'],{'saveDC':15,'saveModifier':2,'initialFace':16,'replacementAdvantageFaces':[3,6],'ReactionBefore':1,'SRUsesBefore':1},{'initialTotal':16+2,'initialSuccess':16+2>=15,'mandatoryReplacementTotal':max(3,6)+2,'replacementSuccess':max(3,6)+2>=15,'ReactionAfter':0,'SRUsesAfter':0},{'initialTotal':18,'initialSuccess':True,'mandatoryReplacementTotal':8,'replacementSuccess':False,'ReactionAfter':0,'SRUsesAfter':0},'Explicit source exception permits reroll after initial SUCCESS or failure; replacement can worsen it and must stand. Other allies retain their own results.')
# Check actual-turn allowance distinction without treating extra Actions as extra turns.
claims=set();cadence=[]
for turn,event in [('regular-A','attack1'),('regular-A','extraActionAttack'),('actual-extra-A','attack'),('regular-A','replayedAttack')]:
 key=('armor_crusher','owner',turn);allowed=key not in claims
 if allowed:claims.add(key)
 cadence.append(allowed)
C(61,['CF-01-E01','CF-28-E01'],{'qualifiedUnqualifiedOncePerTurnFeature':True,'actualTurnEventSequence':[['regular-A','attack1'],['regular-A','extraActionAttack'],['actual-extra-A','attack'],['regular-A','replayedAttack']]},cadence,[True,False,True,False],'Final FS06 supersedes older submitted regular-only rule for unqualified once-per-turn. It grants no extra turn; own-regular/embedded-cast and duration markers remain separate.')
def apportioned_increment(amounts,percent):
 total=sum(amounts);inc=total*percent//100
 if not total:return [0 for _ in amounts]
 exact=[Fraction(inc*v,total) for v in amounts];out=[math.floor(v) for v in exact];left=inc-sum(out)
 order=sorted(range(len(amounts)),key=lambda k:(-(exact[k]-out[k]),k))
 for k in order[:left]:out[k]+=1
 return out
C(62,['CF-22-E02','CF-44-E01','CF-46-E01'],{'nativeTypedAmounts':[7,6],'independentlyEligibleGiantSlayerPercent':20,'independentlyEligiblePrecisionStrikePercent':50,'PowerAttackNotChosen':True},{'giantIncrement':apportioned_increment([7,6],20),'precisionIncrement':apportioned_increment([7,6],50),'totalBeforeDefense':13+(13*20//100)+(13*50//100)},{'giantIncrement':[1,1],'precisionIncrement':[3,3],'totalBeforeDefense':21},'Separate floored increments from same eligible native packet, then proportional largest remainder. This legal independent pair does not combine the mutually exclusive Power/Precision trades.')
linked={ref for c in calcs for ref in c['originalCaseIds']};ck('All bounded calculations link actual reviewed cases',linked<={x['id'] for x in cases+boundaries})
paths=[I/'candidate.json',I/'example_dispositions.json',I/'additional_boundary_expectations.json',I/'shared_rules.json',I/'fex_dispositions.json',R/'data/director/combat_feat_operating_proposal_internal.json',R/'data/public/feat_candidates/exact_01/candidate.json',D/'data/director/feat_candidates/exact_01/candidate.json',D/'data/public/feat_candidates/exact_01/candidate.json',R/'docs/feats/exact-candidate-01/COMBAT.md',R/'docs/feats/exact-candidate-01/source-audit/COMBAT.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CONDITIONS_PLAYTEST.md',R/'docs/mechanics/CONDITION_RECOVERY_PLAYTEST.md',R/'docs/mechanics/MAXIMUM_HP_PLAYTEST.md',R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',A/'FEAT335_HEALING_COMPOSITIONS_89.json',A/'FEAT335_RESOLUTION_CASES_85.json',A/'FEAT335_PHYSICAL_SOCIAL_COMPOSITIONS_91.json']
source_bytes={p.relative_to(G).as_posix():p.read_bytes() for p in paths}
report={'id':'FEAT335-COMBAT-ORIGINAL-CASEBOOK-REVIEW-98','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'47_FULL_PROCEDURES94_ORIGINAL_POSITIONS2_BOUNDARIES_REVIEWED_WITH62_BOUNDED_CALCULATIONS_PARENT_PENDING','scope':'Complete combat-cohort stated-case semantic review including all94 original positions andFA07/08. Preserves four earlier exact expectation replacements and full original sources; no canonical integration or new mechanics.','sourceBindings':[info(p) for p in paths],'completeSelectedRecords':selected,'originalCaseReviews':reviews,'additionalBoundaryReviews':boundary_reviews,'numericAndStateCalculations':calcs,'coverage':{'cohort':'combat','fullFeatProcedures':47,'originalCasePositions':94,'additionalBoundaries':2,'boundedCalculations':len(calcs),'originalCasesWithNumericalProjection':sum(x['id'] in linked for x in cases),'additionalCasesWithNumericalProjection':sum(x['id'] in linked for x in boundaries)},'preservedEarlierReplacedExpectations':changed,'reviewFindings':['All94 complete current outcomes and2 boundaries are consistent under their explicit actual-source predicates; synthetic numeric examples do not establish real acquisition, campaign actors or available events.','Four historical examples retain both original and current exact versions: commander self-recipient, own Target Mark, and two Slayer Resolve cases. Current breath Reaction includes ranged breath attacks; saving-throw branch may reroll even an initially successful save.','Final FS06 actual-turn cadence overrides the preserved original combat sharedProposal regular-only restriction for unqualified once-per-turn; expressly own-regular and Eldritch embedded-cast limits stay separate. Extra Actions and replayed event identities create no additional claim.','Final FS04 hostile-slow arbitration compares against same pre-control Speed and chooses the lowest surviving result. Crippling minus10 does not compound with another minus10 or an independently stronger half-Speed.','Pre-critical base-die payment cannot spend a single die twice. Each separately eligible percentage uses its own floor from the same eligible native base; Power Attack and Precision Strike remain mutually exclusive on an attack.','Riposte, Frenzied Rage and Eldritch Combat retain actual finite action/Reaction and causal-root gates. Volley is a special Action with locked targets and committed arrows, not an Attack Action or shared-damage area.','Center-segment tests cover only admitted planar example footprints with real opposing threats. Actual three-dimensional geometry, physical body/range/sight, target identity and world tags remain external predicates.','Life Drinker numeric7 actual damage from12againstHP3/temp4 excludes overkill and shares a finite personal reserve across critical-then-drop healing. Source causal flags, survival, broad blockers and anti-farm eligibility remain required.'],'remainingScope':['After registering this cohort338 other ordinary positions and16 additional boundaries remain; full parent335 finite tables, acquisition/world evidence, source dependency carriage, copy chains, all mirrors and joint submission are still pending.','No complete runtime engine, actor scheduler, arbitrary geometry, casting-route execution or actual campaign has been run. Calculations are bounded reference projections against exact sourced procedures.','Actual Dragon/dragonkin/CR/blood/body facts remain source-owned. No bestiary retyping, sealed-content review, cosmology or new lineage is authorized here.','No human playtesting, numerical balance, whole-game or release approval.'],'checks':checks,'passed':len(checks),'failed':0,'newMechanicsAuthored':0,'canonicalApplied':False,'parent335Accepted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproved':False,'cosmologyDecisions':0,'actuallySentToGpt':False}
payload=enc(report);script=Path(__file__).read_bytes();ROOT.mkdir()
for rel,b in source_bytes.items():
 p=ROOT/'sources'/rel;p.parent.mkdir(parents=True,exist_ok=True);put(p,b)
for p,b in [(SAVED,script),(ROOT/Path(__file__).name,script),(OUT,payload),(ROOT/'REVIEW.json',payload)]:put(p,b)
put(ROOT/'README.txt',b'Full combat casebook98:47 complete procedures,94 original positions,2 FA boundaries,62 bounded reference calculations. Full originals and four prior expectation replacements preserved. Unapplied; no runtime, parent335, balance, cosmology or publication approval. No supplied program needs execution.\n')
files=sorted(p for p in ROOT.rglob('*') if p.is_file());manifest={'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]};put(ROOT/'MANIFEST.json',enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(p for p in ROOT.rglob('*') if p.is_file()):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 assert all(len(z.read(x['path']))==x['bytes'] and sha(z.read(x['path']))==x['sha256'] for x in manifest['files'])
assert all((G/rel).read_bytes()==b for rel,b in source_bytes.items())
print(json.dumps({'report':info(OUT),'archive':info(ZIP),'coverage':report['coverage'],'checks':len(checks),'failed':0,'fullSourceFiles':len(paths),'archiveMembers':len(manifest['files'])+1},indent=2))
