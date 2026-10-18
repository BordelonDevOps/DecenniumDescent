"""Authored encounter inputs/expected results for GPT's CL10 conference decisions.

These are manuscript vectors, not an engine, an adopted bestiary, or runtime tests.
Kept separate from all historical scenario text and the immutable returned proposals.
"""
from copy import deepcopy

def body(ident, x, y=0, z=0, size='Medium', height=6, mass=180):
    width={'Tiny':2.5,'Small':5,'Medium':5,'Large':10}[size]
    return {'id':ident,'size':size,'centerXY':[x,y],'feetZ':z,
            'bounds':{'min':[x-width/2,y-width/2,z], 'max':[x+width/2,y+width/2,z+height]},
            'heightFeet':height,'massLb':mass,'orientation':'upright, world XYZ',
            'geometryRole':'authored actual encounter input, not a universal species height'}

def caster(ident, level, spells, school='Divination', cls='Wizard', hp=None, rp=None, x=0,y=0):
    pb=2+(level-1)//4; ability=18 if level>=4 else 16; modifier=(ability-10)//2
    maximum=(6 if cls=='Wizard' else 8)+2+(level-1)*((4 if cls=='Wizard' else 5)+2)
    pools={'Wizard':[4,6,10,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,80],
           'Cleric':[3,4,7,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,58]}
    result={'id':ident,'class':cls,'classLevel':level,'totalLevel':level,'PB':pb,
      'abilities':{'STR':10,'DEX':14,'CON':14,'INT':ability if cls=='Wizard' else 10,'WIS':ability if cls=='Cleric' else 10,'CHA':8},
      'abilityGeneration':'Recorded four-d6/drop-lowest arrays: 4,3,3,1 ->10; 6,4,4,1 ->14; 6,4,4,1 ->14; 6,5,5,1 ->16; 4,3,3,1 ->10; 3,3,2,1 ->8. Assign16 to casting ability,10 to the other mental ability. If attained, ASI4 gives casting ability+2. Later ASIs, if attained, use unrelated noncombat choices with no modifier to any tested event.',
      'spellAttack':pb+modifier,'spellDC':8+pb+modifier,'normalHP':maximum if hp is None else hp,'maximumHP':maximum,
      'hpDerivation':{'firstBase':6 if cls=='Wizard' else 8,'laterBase':4 if cls=='Wizard' else 5,'CONPerLevel':2,'levels':level},
      'RP':pools[cls][level-1] if rp is None else rp,'maximumRP':pools[cls][level-1],
      'body':body(ident,x,y),'AC':12,'walkSpeed':30,'temporaryHP':0,'Wounds':0,
      'repertoire':{'actualFixtureChoices':spells,'scope':'Known/learned and prepared for this proposed design encounter only; pending spells are not enabled in public playtests.'},
      'equipment':{'armor':None,'shield':None,'hands':'one ordinary focus held; other hand free for S','focus':{'id':ident+'-focus','massLb':1,'Load':0.1,'boundsFeet':[0.5,0.25,0.25],'permissions':'casting focus only, no attack/bonus/charge'}},
      'components':'audible V; free S hand; held class F; M/F uses focus alternative',
      'Dissonance':0,'previousCastName':None,'RefrainRun':0,'strainLimit':2+pb+modifier,
      'currentConditions':[],'concentration':None,'ReactionAvailable':True,
      'otherModifiers':'No defenses, price discounts, boosts, healing modifiers, injury, suppression, or unrelated acquired-feature activation unless separately stated.',
      'lifecycle':'living PC with death saves, not an HP-only monster',
      'sourceContext':'Complete actual class engine and current foundation/integration rules are bound by the candidate, not inferred from a spell name.'}
    if cls=='Wizard':
        result['specialization']=school
        result['repertoire'].update({'acquisition':'Each named ordinary spell selected as a legal level-up book addition at or after its rank gate; available additions suffice. One hour preparation after a beneficial long rest; no duplicates. Unlisted choices supply no test modifier.', 'matrixCapacity':level+modifier,'firstDistinctPreparedFamilyBaseDissonance':0})
        result['ConjurationCreationBonus']=level if school=='Conjuration' else 0
        result['FleshAscendantAcquired']=False
        result['heroPath']='Spellbinder, no modifying Hero card invoked' if level>=10 else None
        result['schoolPassive']='Divination failed-save reroll remains unused' if school=='Divination' else 'Only explicitly named school passive'
    else:
        result['InvocationPath']='Judgment; no Invocation or Rite used unless specified'
        result['Conviction']=5 if level>=9 else 3
        result['heroPath']='Saint' if level>=10 else None
        result['repertoire']['acquisition']='Actual ordinary Cleric repertoire choice under shared fallback, within class/rank/known capacity; no borrowed school or Wizard preparation exception.'
    return result

def cast(actor, spell, rank, time=0, round_no=1, rp_before=None, hp_cost=0, concentration=False):
    price=[0,2,3,5,7,10,13,17,21,26][rank]
    before=actor['RP'] if rp_before is None else rp_before
    return {'actor':actor['id'],'spellId':spell,'rank':rank,'school':'Necromancy' if spell!='create-homunculus' else 'Universal',
       'timeSeconds':time,'round':round_no,'activation':'Action on actual regular turn','RPBefore':before,'baseRP':price,'surcharge':0,'RPPaid':price,'RPAfterCommit':before-price,
       'normalHPCost':hp_cost,'normalHPAfterCommit':actor['normalHP']-hp_cost,
       'DissonanceBefore':0,'baseDissonance':0 if actor['class']=='Wizard' else (1 if rank<=5 else 2),'Refrain':0,'DissonanceAfter':0 if actor['class']=='Wizard' else (1 if rank<=5 else 2),
       'concentration':concentration,'durationStart':'successful establishment at this time',
       'checks':'Actual listed learned/prepared source, rank/access, Action, components, full geometry and affordable precommit pools. No unlisted counter, source modifier or interrupt in this branch.'}

def recipient(ident,x,y=0,hp=60,maximum=60,ac=12,lifecycle='HP-only living synthetic recipient'):
    return {'id':ident,'fixtureClassification':'Explicit synthetic encounter input; not a named class or approved bestiary creature','body':body(ident,x,y),
      'type':'Humanoid','normalHP':hp,'maximumHP':maximum,'temporaryHP':0,'AC':ac,'CONSaveBonus':2,
      'lifecycle':lifecycle,'Speed':30,'conditions':[],'Wounds':0,'defenses':[],'interceptors':[],
      'donorProvenance':'genuine noncreated living body; not a summon, copy or consumed animation',
      'anatomy':'connected head/torso, two arms/hands, two legs; no missing/harvested parts',
      'gear':[],'responses':'No protective, resurrection, control or other response unless separately supplied.'}

ENV={'plane':'same ordinary encounter plane, no cosmology inference','light':'bright, ordinary sight/hearing throughout open area',
 'ground':'continuous flat floor z=0, supports all named masses; open x/y extents at least[-100,100], ceiling z=30 unless overridden',
 'geometry':'Distances are shortest distances between actual body volumes; point-range uses nearest caster-body point. Bounds are actual occupied space; touching faces do not overlap interiors.',
 'LoE':'No opaque intervening objects, barriers or cover unless explicitly listed. Each selected source-target segment is in the described open region.',
 'time':'Each independent fixture begins at its own time0/round1. Within each round owner regular turn precedes its complete attached phase, then listed recipient turn. Next owner regular START is+6 seconds. No additional phases, refreshes or implicit actions.',
 'baseline':'No other actors, equipment bonuses, damage/healing modifiers, hidden suppressors, Fate disclosure grants or out-of-scope effects. Input prior states do not assert an unsupplied historical attack.'}

CASES=[]
def add(ident, spell, actors, events, expected, *, bodies=None, branches=None, condition=None, notes=None):
    CASES.append({'id':ident,'spellId':spell,'status':'CONDITIONAL_CONTENT_PREREQUISITE' if condition else 'AUTHORED_CURRENT_DESIGN_VECTOR',
      'runtimeExecuted':False,'authority':'Actual GPT conference proposal plus bound inherited interfaces; final exact review outstanding',
      'environment':deepcopy(ENV),'actors':actors,'bodyInputs':bodies or [],'events':events,'expected':expected,
      'independentBranches':branches or [],'prerequisite':condition,'notes':notes or []})

def group_one():
    w= caster('W7',7,['summon-corpse-golem','soulburn-pact'])
    foe=recipient('foe',30)
    g=body('golem',10,size='Large',height=8,mass=600)
    add('IN4-07-A','summon-corpse-golem',[w,foe],[cast(w,'summon-corpse-golem',4,concentration=True),
      {'phase':'W7 round1 regular Bonus Action','command':'golem Slam foe','commandRangeGap':2.5,'commandSpent':1},
      {'phase':'round1 attached after whole W7 turn','move':{'from':[10,0,0],'to':[20,0,0],'distance':10,'rate':1,'cost':10,'Speed':20,'remaining':10,'sweptBounds':{'min':[5,-5,0],'max':[25,5,8]}},'attack':{'target':'foe','gapFeet':2.5,'roll':10,'modifier':7,'total':17,'AC':12,'advantage':False,'disadvantage':False,'critical':False,'dice':[6,7],'type':'bludgeoning','damage':13}}],
      {'casterRP':17,'golemBaseAndFinalMaxHP':60,'golemHP':60,'foeHP':47,'newWounds':0,'deadline':60,'dealer':'golem','statOwner':'W7','damageRoot':'CL10-golem-slam-1','Null':False,'ownerCommands':1,'ownerOffenses':1,'SlowAuraActivated':False,'secondOwnedOffenseAllowed':False},bodies=[g],notes=['Divination Wizard7 has neither Conjuration HP nor Hero Flesh Ascendant. Remainder of movement is unused. No foe is in melee reach before Golem movement, so no hostile reach exit occurs.'])
    w2=deepcopy(w); w2['RP']=17;w2['concentration']='same Golem created time0; ends60'
    add('IN4-07-B','summon-corpse-golem',[w2,recipient('selected-enemy',27.5)],[
      {'time':6,'round':2,'phase':'W7 regular turn','BonusAction':'command same Golem Slow Aura instead of Slam','Action':'unused','commandGap':12.5,'activationDC':15,'selectedKnownEnemyIDs':['selected-enemy']},
      {'time':6.5,'phase':'attached','auraOrigin':[20,0,4],'radius':10,'endpoint':'W7 next future regular START time12','initialEnemyClosestPoint':[25,0,4],'distance':5,'CONDie':7,'CONBonus':2,'CONTotal':9,'result':'failure; Speed30->15'},
      {'time':7,'phase':'enemy regular movement','routeCenters':[[27.5,0],[33,0],[27.5,0]],'segmentDistances':[5.5,5.5],'totalDistance':11,'maximumHalvedBudgetNeeded':15,'atOuterPose':{'boundsX':[30.5,35.5],'closestToAura':10.5,'auraApplies':False,'Speed':30},'afterReentry':{'Speed':15,'distanceSpent':11,'remaining':4,'saveRerolled':False},'opportunity':'Golem has no independent Reaction; no other threatening actor exists'}],
      {'savesThisActivation':1,'enemyFinalSpeedBefore12':15,'enemySpeedAt12':30,'hardGuardSpent':False,'lostActions':0,'ownerOffensesRound2':1,'golemSlamThisRound':False,'originalSourceExpiry':60},bodies=[body('golem',20,size='Large',height=8,mass=600)])
    s=caster('pact-W7',7,['soulburn-pact'],hp=31,rp=12)
    counter=caster('counter-W7',7,[],x=20,rp=12)
    add('IN4-10-A','soulburn-pact',[s],[cast(s,'soulburn-pact',4,hp_cost=20),{'resolve':'Choose3 actual RP recovery, missing capacity19; no recovery prohibition'}],
      {'RPSequence':[12,5,8],'HPSequence':[31,11,11],'temporaryHPUsed':0,'newWounds':0,'newSoulburnRestUse':False},branches=[
      {'name':'Independent countered branch, reset same original inputs','additionalActor':counter,'operation':{'source':'wizard.json /cards/17','activation':'available Reaction during pact commitment after costs','rangeGap':15,'perceivesVAndS':True,'RPSequence':[12,9],'rank':1,'DissonanceSequence':[0,0],'firstDistinctClassMatrix':True,'die':11,'INT':4,'PB':3,'checkTotal':18,'DC':18,'taskDegree':'Success','rechargeAfterResolution':2,'nextOwnRegularStarts':'2->1->0; no same-cast retry'},'expected':{'pactCasterRP':5,'pactCasterHP':11,'recovery':0,'countererRP':9}}])
    s2=caster('pact-W7',7,['soulburn-pact'],hp=44,rp=24)
    add('IN4-10-B','soulburn-pact',[s2],[cast(s2,'soulburn-pact',4,hp_cost=20),
      {'time':0,'resolve':'24RP->17->20;44HP->24'},
      {'time':6,'round':2,'activation':'new real Action same prepared Pact family, same actual pool','precommitRP':20,'precommitHP':24,'price':7,'DissonanceBefore':0,'repeatBaseDissonance':1,'Refrain':1,'DissonanceAfter':2,'commitRP':13,'commitHP':4,'recover':3,'finalRP':16,'noSoulburnNamedRestCap':True}],
      {'afterTwoLegalCasts':{'RP':16,'HP':4,'Dissonance':2},'thirdCastUnaffordableAt4HP':True},branches=[
      {'name':'Insufficient RP','initial':{'RP':6,'HP':31,'temporaryHP':30},'expected':{'commit':False,'RP':6,'HP':31,'Dissonance':0,'resourcesSpent':0}},
      {'name':'Insufficient normal HP','initial':{'RP':12,'HP':20,'temporaryHP':30},'expected':{'commit':False,'RP':12,'HP':20,'temporaryHP':30}},
      {'name':'Genuine limited Grand Reservoir comparator','actor':caster('reservoir-W20',20,['soulburn-pact'],hp=31,rp=0),
       'operation':{'acquiredSource':'Wizard20 automatic /cards/62','useBefore':'one available since beneficial long rest','preparedPact':True,'Action':'new regular Action','baseWaived':7,'surcharge':0,'HPStillPaid':20,'Dissonance':0,'recoveryChosen':0,'otherRefundFeature':None,'noOvercastFusionDualCast':True},
       'expected':{'RP':0,'HP':11,'ReservoirUseRemaining':0,'secondWaiverGranted':False},
       'boundary':'This zero-recovery comparator proves access/base-only limited waiver without claiming whether Soulburn positive recovery is forbidden by Reservoir’s another-RP-refund-feature clause. Positive-waiver recovery stays an explicit question for GPT; do not silently classify it as allowed.'}])
    k=caster('knight-W9',9,['summon-death-knight'],school='Conjuration')
    target=recipient('knight-foe',20)
    add('NE5-01-A','summon-death-knight',[k,target],[cast(k,'summon-death-knight',5,concentration=True),
       {'phase':'owner BA then actual attached phase','command':'Knight attack knight-foe','commandGap':5,'moveFeet':0,'attackGap':5,'d20':10,'attackModifier':8,'total':18,'targetAC':12,'critical':False,'advantage':False,'damageFaces':[6,7],'damageType':'necrotic','damage':13}],
      {'RP':22,'KnightMaxHP':89,'KnightHP':89,'creationBonus':9,'FleshAscendantBonus':0,'foeHP':47,'newWounds':0,'ownerCommands':1,'ownerOffenses':1,'secondStandardSkeletonAttackAllowed':False,'intrinsicSwordSalvage':0,'expiry':60},bodies=[body('Knight',10)],notes=['Conjuration at Wizard9 applies to this Wizard-created creature despite Necromancy spell school. School attack bonus does not apply, leaving+8. No actual second skeleton is needed to establish absence of a second allowance; no skeleton attack event is claimed.'])
    am=caster('AM-W9',9,['antimagic-field-lesser'],x=27.5)
    amcast=cast(am,'antimagic-field-lesser',5,time=7,round_no=2,concentration=True);amcast['school']='Abjuration';amcast['spellIdentityNote']='Use actual catalog ID supplied by accepted AC5 first spell when assembled; display name Antimagic Field (Lesser).'
    kb=deepcopy(k);kb['RP']=22;kb['concentration']='Knight source established0, ends60'
    add('NE5-01-B','summon-death-knight',[kb,am],[
       {'priorLawfulState':{'source':'Knight of A created time0, deadline60','KnightHP':59,'maximumHP':89,'damageBeforeFixture':30,'currentPose':[20,0,0],'poseAcquisition':'prior legal walk10 from summon10 in open region, already paid; no damage attack invented','lantern':{'id':'real-lantern-K','massLb':2,'Load':0.2,'boundsFeet':[1,1,1],'fuelMinutes':42,'condition':'undamaged','custody':'Knight right hand'}}},
       amcast,{'time':7,'AMPoint':[20,0,3],'pointToNearestCasterBody':5,'radius':10,'clearLoE':True,'KnightVolume':{'min':[17.5,-2.5,0],'max':[22.5,2.5,6]},'operation':'Any body intersection fully suppresses this Knight expression only under CL10 proposal','lanternDrop':{'min':[19.5,-0.5,0],'max':[20.5,0.5,1],'sameRegion':True,'supported':True}},
       {'time':13,'AMSourceEnds':'caster voluntarily ends concentration; no dispel/rescan','KnightReturn':'same saved pose, clear normal space; no displacement or automatic lantern pickup'}],
      {'KnightIdentity':'same','KnightHP':59,'maximumHP':89,'sourceExpiry':60,'absenceProvidesOccupancy':False,'lanternFuelAt13':'42 minutes minus six actual burning seconds; no refill','KnightGearAfterReturn':[],'AMCost':10,'AMRPAfter':22},bodies=[body('Knight-at-suppression',20)],branches=[
       {'name':'Occupied saved chamber; return pending until source expiry','environmentOverride':'Saved Knight body is inside an open-top 5x5 shaft x[17.5,22.5],y[-2.5,2.5], z[0,8]; solid walls surround horizontal sides, roof absent before lowering. AM caster is on a supported balcony at(27.5,0,10); sphere center(20,0,7) has clear diagonal LoE over wall height8 (segment from caster face25,0,10 crosses rimx22.5 atz8.5) and point distance sqrt34<10. The Knight is fully inside the shaft; field reaches it through open top.',
        'events':[{'time':8,'sourceInput':'A pre-existing mundane solid lift block is lowered by a previously established mechanism after Knight disappearance. This is explicit terrain input, not a spell-granted mover. Block occupies entire shaft x[17.5,22.5],y[-2.5,2.5],z[0,30]; side walls separate the region through z30. No six-foot body fits normally, squeezed, or at an adjacent candidate from the old body volume; an open pose atop the30ft block would require an impermissible farther search.'},{'time':13,'source':'AM ends, block remains','result':'normal fit and squeeze fail; no same-region adjacent fit through side walls or occupied block; no farther search; pending expression'},{'time':60,'source':'original absolute deadline','result':'source ends while still pending'},{'time':65,'sourceInput':'block removed','result':'no Knight return'}],
        'caveat':'This independent obstruction fixture starts with no real lantern/gear and with the block in its already-cleared upper storage position before lowering. It does not claim a lantern can survive crushing or teleport through the obstruction. The simple open-floor main case supplies the gear drop/return example.'}])
    donor=caster('gift-W9',9,['grave-gift'],hp=31)
    patient=recipient('patient',15,hp=0,maximum=40,lifecycle='living synthetic death-save-enabled ally, actual Dying')
    patient.update({'Wounds':3,'Critical':True,'willing':True,'deathSuccesses':1,'deathFailures':1,'conditions':['Prone','zero-HP Unconscious','zero-HP Incapacitated'],'independentInjury':'old left-hand injury unchanged','pose':'lying, bounds min[12.5,-2.5,0] max[17.5,2.5,1]; no new change of occupied footprint'});patient['body']['bounds']['max'][2]=1;patient['body']['heightFeet']=1;patient['body']['orientation']='prone'
    add('NE5-04-A','grave-gift',[donor,patient],[cast(donor,'grave-gift',5,hp_cost=15),{'targetGap':10,'LoE':'open','resolve':'willing living Dying0 ally; no broad HP block; direct set40'}],
       {'donorHP':16,'donorRP':22,'patientHP':40,'patientWounds':3,'Critical':True,'ProneRetained':True,'injuryRetained':True,'deathCountersCleared':True,'stableDeadline':None,'zeroHPUnconsciousRemoved':True,'ordinaryHealingDice':0,'ordinaryHealing39CeilingApplied':False,'RPRefund':0})
    gift2=caster('gift-W9',9,['grave-gift'],hp=2)
    patient2=deepcopy(patient);patient2['Wounds']=1;patient2['Critical']=False;patient2['deathFailures']=2
    blocker=caster('chill-W3',3,['chill-touch'],x=35)
    add('NE5-04-B','grave-gift',[gift2,patient2,blocker],[
      {'time':-1,'priorLawfulState':'Patient is alive Dying0, already has a successful real Chill Touch /catalog/spells/415/operational hit rider. Source-owner chill-W3, target’s first future regular END is time3. This fixture begins after that fully resolved source event; no invented melee hit against Unconscious is asserted. Exact blocked-HP rider and original endpoint are inputs, not a fresh cast or damage test.'},
      cast(gift2,'grave-gift',5,hp_cost=1),{'time':0,'targetGap':10,'resolve':'HP assignment blocked by still-operative Chill Touch; independently stabilize still-Dying target','privateD4':2,'StableDeadline':7200}],
      {'donorHP':1,'donorRP':22,'patientHP':0,'Stable':True,'deathSuccesses':0,'deathFailures':0,'deadline':7200,'newFateAdapter':False,'Wounds':1,'UnconsciousRetained':True,'ProneRetained':True},branches=[
      {'name':'Already Stable','initial':'same inputs except already Stable0 with deadline3500','expected':'preserve3500; no d4 draw; pay1HP/10RP'},
      {'name':'Donor1HP even with source-qualified would-die Ward','initial':'donor1HP, otherwise same legal state','expected':'unaffordable, no commitment/cost; cost is not a damage/death Ward trigger'},
      {'name':'Known actually dead recipient','initial':'recipient has actually died before target selection','expected':'ineligible; no cast/payment; this spell grants no resurrection'},
      {'name':'Countered after costs','initial':'same legal initial donor2/targetDying','operation':'Use independently sourced Wizard9 class Counterspell: actual available Reaction/3RP/recharge0,20ft clear range; d20=12+INT4+PB4=20 against rank5 DC20; success; source records as in IN4-10-A with rank5/DC20','expected':'donor1HP/22RP; patient stays Dying0 with original counters; no Stable d4'}])

def corpse(ident,x,y=0,death=-3600,missing=None,gear=None):
    b=body(ident,x,y); b['bounds']['max'][2]=1;b['heightFeet']=1;b['orientation']='prone'
    return {'id':ident,'body':b,'typeAtDeath':'Humanoid','deathTime':death,'realNonCreatedAllocation':ident+'-matter',
      'consumed':False,'connectedHeadTorso':True,'missingParts':missing or [],'gear':gear or [],
      'history':'Explicit physical input: genuinely dead ordinary humanoid, intact stated matter; not a copy, conjured donor or prior animation. No prior killing blow or biography is inferred.',
      'standingHeightIfSupported':6,'retainedNeeds':'No environmental immunity assigned. Long-term needs/behavior require separate supplied records; this immediate fixture does not claim work or survival outcomes.'}

def group_two():
    w=caster('flood-W9',9,['negative-energy-flood'])
    f=recipient('flood-target',20,hp=30,maximum=60,lifecycle='ordinary living monster: Core Wounds, then immediate actual death at0; no death-save chassis')
    f['gear']=[{'id':'pouch-F','massLb':1,'Load':0.1,'contents':['unique copper token F'],'fit':'belt on actual torso','boundsFeet':[0.5,0.5,0.5]}]
    damage={'CONSave':{'die':5,'bonus':2,'total':7,'DC':16,'success':False},'dice':[8,8,7,7,7],'rawAndResolved':37,'temporaryAbsorbed':0,'postTemp':37,'normalHPLost':30,'overkill':7,'instantDeath':False,'instantDeathComparison':'37-30=7<60','WoundSave':{'trigger':'drop and half-max, one save','DC':18,'die':18,'bonus':2,'total':20,'result':'success'},'finalHP':0,'lifeResult':'actual ordinary-monster death'}
    add('NE5-07-A','negative-energy-flood',[w,f],[cast(w,'negative-energy-flood',5),{'rangeGap':15,'LoE':'open','damage':damage,'dealer':'flood-W9','damageRoot':'F-original-target','Null':False,'immediateResponses':[]},
      {'afterRealDeathAndResponses':'same physical body falls prone at anchor20,0,0; usable connected head/torso and all limbs remain. Claim allocation once; no prior consumed flag. Form same body zombie at this actual prone pose; standing requires an actual later legal act.'}],
      {'casterRP':22,'casterDissonance':0,'zombieBaseAndFinalHP':20,'zombieMaxHP':20,'zombieAC':10,'pouchID':'pouch-F','pouchTokenPreserved':True,'bodyAnchor':[20,0,0],'initialProne':True,'allocationConsumed':True,'voluntaryCreationRoundActs':0,'absoluteExpiry':3600,'concentrationRequired':False,'AutoRaiseReservation':False,'newConjurationOrFleshBonus':0},notes=['Ordinary monster Wound processing is supplied explicitly; this is not an imported Ranger/no-Wounds lifecycle. No temporary HP from a Necromancy specialization: caster specialized Divination.'])
    living=deepcopy(f);living.update({'lifecycle':'living significant synthetic ally with death saves','maximumHP':80,'normalHP':30})
    warder=caster('ward-W7',7,['death-ward'],x=0,y=15)
    saint=caster('saint-C16',16,[],cls='Cleric',x=25)
    saint['acquiredCard']='Saint Resurrection selected at Cleric16, /cards/37; one unused long-rest use; Divine Rebirth not acquired'
    add('NE5-07-B','negative-energy-flood',[w,living],[cast(w,'negative-energy-flood',5),
      {'sameCONAndDamageAsA':True,'postTemp':37,'preHP':30,'maximumHP':80,'instantDeath':False,'WoundSave':{'DC':18,'die':18,'bonus':2,'result':'success'},'result':'living Dying0, Unconscious/Incapacitated/Prone; counters0/0; no actual corpse at claim checkpoint'}],
      {'zombieCreated':False,'laterDeathSaveDoesNotReplayClaim':True,'casterRP':22},branches=[
       {'name':'Real Death Ward floor, ordinary monster recipient of A','additionalActor':warder,'sourceSetup':{'time':-6,'activation':'warder regular Action','source':'catalog /spells/637/operational','rank':4,'RP':[24,17],'Dissonance':[0,0],'range':'body gaps sqrt(15^2+10^2)<60, open LoE','concentration':'warder, expires54 unless used','target':'flood-target','components':'V/S/F available'},
        'resolve':{'raw':37,'preHP':30,'maximumHP':60,'instantDeath':False,'floorResultHP':1,'wardConsumed':True,'halfMaxWoundStillRequired':True,'WoundDC':18,'CONRoll':18,'CONBonus':2,'WoundResult':'success'},'expected':{'alive':True,'corpse':False,'zombie':False,'warderConcentrationEnds':True}},
       {'name':'Actual readied Saint Resurrection after monster death of A','additionalActor':saint,'relationship':'target is saint’s actual allied willing identity; no soul/body/resurrection blocker; complete vital body remains',
        'ReadySetup':{'time':-1,'regularTurnStarted':-2,'nextRegularStart':4,'Action':'Ready one nonspell Resurrection Action for observable death of this allied target','concentrationRequiredByReady':False,'ReactionAvailable':True,'costAtSetup':0},
        'response':{'time':0,'trigger':'target actually dies from Flood packet; ordinary death completes, before Flood’s subsequent corpse claim','ReactionSpent':1,'touchGap':0,'sourceCard':'cleric /cards/37','RP':[45,35],'Conviction':[5,2],'onceLongRestUseSpent':True,'deadSeconds':0,'restoredHP':1,'S':3,'M':4,'temporaryHP':10,'tempExpiry':60,'DissonanceVented':0,'ventReason':'release occurs outside Saint’s regular turn, so own-turn vent predicate is false'},
        'expected':{'sameIdentityAlive':True,'HP':1,'temporaryHP':10,'zombie':False,'sourceCorpseClaimFails':True,'noFreeGenericInterrupt':True}},
       {'name':'Competing Auto-Raise','status':'CONDITIONAL_NOT_A_POSITIVE_CURRENT_VECTOR','missing':'actual standard-minion personal killing blow plus genuine pending checkpoint; Flood’s caster-dealt killing packet supplies neither','expected':'no invented standard-minion reservation'}])
    dw=caster('danse-W9',9,['danse-macabre'])
    corpses=[corpse('corpse-'+str(i+1),10+5*i,10,death=-(i+1)*3600,gear=[{'id':'token-'+str(i+1),'massLb':0.1,'Load':0.01,'custody':'fitted torso pouch included in this documented gross mass/Load'}]) for i in range(5)]
    dt=recipient('danse-foe',15,20)
    add('NE5-08-A','danse-macabre',[dw,dt],[cast(dw,'danse-macabre',5),
      {'selectionOrder':[c['id'] for c in corpses],'agesHours':[1,2,3,4,5],'maximumRangeUpperBound':35,'actualLoE':'five adjacent disjoint footprints y[7.5,12.5], caster0,0; open diagonal rays, no total cover','formation':'Each same prone anchor, HP20; no repaired matter; one common deadline3600'},
      {'time':6,'round':2,'phase':'owner BA then attached','command':'body2 stands and strikes danse-foe','standCost':10,'walkSpeed':20,'translation':0,'remaining':10,'attackBodyPose':[15,10,0],'targetPose':[15,20,0],'gapFeet':5,'d20':10,'modifier':8,'total':18,'targetAC':12,'damageFace':4,'damage':4,'type':'bludgeoning','critical':False,'targetHP':[60,56]}],
      {'RP':22,'members':5,'creationRoundVoluntaryActs':0,'creationBonus':0,'body2OnlyOffenseRound2':True,'otherFourAttack':False,'sharedOwnerOffenses':1,'separateWizardStandardCap':3,'allTokenIDsRetained':True,'expiry':3600},bodies=corpses)
    amended=deepcopy(corpses);amended[0]['missingParts']=['both legs below hip'];amended[1]['consumed']=True
    add('NE5-08-B','danse-macabre',[dw],[cast(dw,'danse-macabre',5),
      {'originalSelectionOrder':[c['id'] for c in amended],'hiddenConsumption':'corpse2 was earlier consumed; caster lacks that fact at legal commitment; no diagnostic/free reselect','resolutionInOrder':['corpse1 qualifies with head/torso/two arms but no legs','corpse2 fails','corpse3 qualifies','corpse4 qualifies','corpse5 qualifies'],'sixthCorpse':'corpse6 at(40,10) is visible but not selected and cannot substitute'}],
      {'RP':22,'newCohortIDs':['corpse-1','corpse-3','corpse-4','corpse-5'],'leglessBodyWalk':0,'legsRegrown':False,'sameMissingMatterRetained':True,'newCohortAtLeastOneEndsOldCohort':True,'standardMinionCap':3,'combinedOffensiveAllowance':1},bodies=amended,branches=[
      {'name':'All original selections secretly consumed','expected':'pay10; no new members, old cohort continues until its existing deadline; no replacement body choice'},
      {'name':'At3600','expected':'all remaining animations end at their own actual poses, real tokens persist, same consumed allocation flags remain; none becomes new fresh fuel'}])
    cw=caster('wraith-C11',11,['summon-soul-wraith'],cls='Cleric')
    wf=recipient('wraith-donor',20,hp=7,maximum=60,lifecycle='ordinary living monster, Core Wound save then actual death at0')
    wf['temporaryHP']=5
    add('IN6-07-A','summon-soul-wraith',[cw,wf],[cast(cw,'summon-soul-wraith',6,concentration=True),
      {'priorLawfulStateAtNextRound':'same Wraith is97/100 after a resolved3HP loss input; no attack invented; caster still concentrating, no bonus/max modifier'},
      {'time':6,'round':2,'ownerBonusAction':'command Wraith strike donor','attachedAttack':{'WraithCenter':[10,0],'donorCenter':[20,0],'gap':5,'d20':12,'modifier':8,'total':20,'targetAC':12,'critical':False,'dice':[8,9],'damage':17,'type':'necrotic','dealer':'Wraith','statOwner':'wraith-C11','Null':False},'damage':{'temporaryAbsorbed':5,'postTemp':12,'normalHPLost':7,'overkill':5,'instantDeath':False,'WoundSave':{'DC':10,'die':12,'bonus':2,'total':14,'result':'success'},'actualDeath':True,'responsesEndingWraith':[]},'lifetap':{'eligibleTerminalDamage':12,'base':6,'actualGain':3}}],
      {'casterRP':17,'casterDissonance':2,'WraithHP':100,'WraithMaxHP':100,'ownerHPGain':0,'ownerRPRecovery':0,'discardedHeal':3,'expiry':60,'oneOffense':True},bodies=[body('Wraith',10,height=6,mass=0)],notes=['Zero mass is an explicit fixture geometry/weight input for this generated manifestation only; no general Undead mass or carrying immunity is claimed. Any physical-load test must supply actual applicable Wraith capacity.'])
    add('IN6-07-B','summon-soul-wraith',[cw],[cast(cw,'summon-soul-wraith',6,concentration=True),
      {'formation':'Wraith feet(-2.5,0,0), body x[-5,0],y[-2.5,2.5],z[0,6]; caster at(-12.5,0) for this fixture. A slab x[0,10],y[-20,20],z[0,20] is ordinary opaque stone. Exit body x[10,15] was directly surveyed before this scene and remains unchanged; knowledge is input, not opaque vision. Initial summoning space is directly seen from caster; exit is known, not currently seen through stone.'},
      {'time':6,'round':2,'phase':'owner BA, actual Wraith attached phase','order':'Traverse to known open endpoint center12.5,0, feet0; no attack','realCargoOperation':'Before traversal, deposit the previously carried actual chest C at entry floor bounds x[-4.5,-3.5],y[2.55,3.55],z[0,1] through available ordinary interaction; gross20lb/2Load including contents. Wraith MediumSTR6 gives90lb/6Load, so this load is within both and below Burdened3. Proposed fixture has two usable gripping extremities and handles within0.05ft of the body face, with release/drop possible. This handling anatomy is an explicit pending local completion for GPT, not a granted attack or professional tool use. Chest’s acquisition is prior lawful cargo state, not free material creation.','route':{'startCenter':[-2.5,0,3],'endCenter':[12.5,0,3],'translation':15,'contactRate':2,'cost':30,'FlyBudget':40,'remaining':10,'fullEndpointBounds':{'min':[10,-2.5,0],'max':[15,2.5,6]}},'senses':'opaque slab blocks new sight/attack LoE throughout contact; no attack attempted'}],
      {'noCargoPhasing':True,'chestFinal':'same entry location, contents/condition unchanged','WraithEndsInOpenSpace':True,'movementSpent':30,'remaining':10,'oldRescueDamage':0,'sourceDeadline':60},bodies=[body('Wraith',-2.5,height=6,mass=0)],branches=[
       {'name':'Independent15-foot slab','geometry':'slab x[0,15], same actual5-foot-wide body; exit x[15,20], center17.5','distance':20,'rate':2,'cost':40,'remaining':0,'noTeleportOrShrunkBody':True},
       {'name':'Involuntary trapped-body input after real external event','input':'Explicit separate final scene state: Wraith body centered(5,0,3) inside opaque solid extending x[-20,30],y[-20,20],z[-20,30]; event has already completed. No normal or squeezed same-anchor space and no adjacent body fit in same unobstructed region; no assumed newly granted terrain-moving action. Actual source still concentrated at time12, expiry60.','operation':'At required completed-event placement checkpoint, local normalization fails; end manifestation, not far retreat and not1d10','expected':'same Wraith ceases at actual location; any real item there remains subject to current pending-item placement, never sent to entry chest location'}])

def group_three():
    cmd=caster('command-W11',11,['command-undeath'])
    add('IN6-09-A','command-undeath',[cmd],[],{'positiveBindingClaimed':False,'approvedCR2UndeadInvented':False},
      condition='Complete operative authoritative exact-CR2 Undead profile is absent from the bound26 source-only bestiary records. Requires actual full statistics/type/CR/approval/lifecycle/schedule, not inferred CR from the four newly authored Create Undead profiles.',
      branches=[{'name':'Actually unrated Ghast is not a known legal CR2 target','target':{'body':body('unrated-Ghast',20),'profile':'complete new Create Undead Ghast,50HP/AC14; CR unassigned'},'operation':'known missing eligibility rejected at preflight','expected':{'RPUnchanged':40,'ActionNotCommitted':True,'noSave':True,'noControl':True,'noPublicHiddenDiagnostic':True}},
        {'name':'Historical positive obligation retained','status':'conditional only','prerequisites':'real CR2 Undead, actual WIS and hard-admission ledger, class/access13RP/60ft, original schedule and body history','expected':'only when supplied may the chosen failed-save/no-immunity control rule be demonstrated'}])
    add('IN6-09-B','command-undeath',[cmd],[],{'positiveReplacementOrCommandClaimed':False,'noSyntheticCRGranted':True},
      condition='Same missing exact-CR2 operative profile also prevents a real two-slot replacement/command fixture. Original positive text remains unchanged and explicitly conditional.',
      notes=['Future case must bind two old relation IDs and a declared replacement; saved new target leaves both old relations while13RP stays spent. Successful later binding requires its own genuinely unspent hard guard. Independent target keeps its actual old initiative; companion keeps original owner phase. Issuance-round command and execution-round offensive ledgers both apply; deadline is earliest future opportunity, binder nextSTART, issue+6, with expiry first. These are adopted-for-authoring proposed obligations, not executed positive evidence.'])
    cr=caster('creator-C11',11,['create-undead'],cls='Cleric')
    cg=corpse('Ghast-corpse',10,0,death=-90000,missing=['left hand'],gear=[{'id':'old-coat','massLb':2,'Load':0.2,'fit':'ordinary soft mundane coat, not armor; no AC bonus','condition':'torn left sleeve'}])
    ally=recipient('cone-ally',20,-2.5); foe=recipient('cone-enemy',20,2.5)
    add('IN6-11-A','create-undead',[cr,ally,foe],[cast(cr,'create-undead',6),
      {'select':'same corpse -> Ghast, old corpse usable despite25hour age','bodyState':'same anchor prone at10,0; retained left-hand absence and torn coat; HP50 AC14; no Conjuration/Flesh bonus; no creation-round action'},
      {'time':6,'round':2,'phase':'real creator BA and attached phase','command':'stand then exhale toward+x','standCost':15,'Speed':30,'movementAfter':0,'headOutlet':[12.5,0,5],'cone':'15foot cone along+x; cross-section radius equals forward distance/2 (base diameter15), capped at x27.5; actual 3D volume and clear origin LoE','recipients':['cone-ally','cone-enemy'],'intersectionWitnesses':{'cone-ally':[18,-1,5],'cone-enemy':[18,1,5]},'sharedDice':[3,4],'poison':7,'DC':16,'CON':{'cone-ally':{'die':15,'bonus':2,'total':17,'success':True,'damage':3},'cone-enemy':{'die':5,'bonus':2,'total':7,'success':False,'damage':7}},'meleeActionThisPhase':False}],
      {'casterRP':17,'casterDissonance':2,'GhastHP':50,'leftHandRestored':False,'allyHP':57,'enemyHP':53,'newWounds':0,'Poisoned':False,'toxinStock':0,'offenses':1,'CRAssigned':False,'permanentBody':True},bodies=[cg],notes=['Cone witnesses lie5.5ft forward and1ft radial from mouth, inside radius2.75 and within each actual5x5x6 body. The two recipient footprints touch at y0 without overlapping interiors. Cone width convention must match inherited combat geometry; not a new all-spell cone definition.'])
    oldghoul={'id':'old-Ghoul','body':body('old-Ghoul',10,10),'profile':'Create Undead Ghoul, original creator-C11','HP':35,'maximumHP':40,'authority':'old-authority-1','consumedAllocation':'old-ghoul-matter','gear':[],'birthRound':-2,'spentRound1Opportunity':False}
    oldwight={'id':'old-Wight','body':body('old-Wight',20,10),'profile':'Create Undead Wight, original creator-C11','HP':45,'maximumHP':45,'authority':'old-authority-2','consumedAllocation':'old-wight-matter','gear':[],'birthRound':-1,'spentRound1Opportunity':False}
    mummycorpse=corpse('Mummy-corpse',10,-10)
    add('IN6-11-B','create-undead',[cr],[{'priorLawfulState':[oldghoul,oldwight],'earlierCreationCosts':'each earlier real rank6 cast paid13 in separate earlier scenes; present30RP is documented current pool after a later genuine replenishment. No free current cast or initial approval is inferred; body/authority inputs are prior lawful state, not freshly executed events.'},
      {'beforeCommit':'choose Mummy and predeclare release only old-authority-1'},cast(cr,'create-undead',6),
      {'successfulFormation':'same corpse permanent Mummy70HP AC16; release old Ghoul authority only, preserve old-Ghoul35HP/body/consumed flag','schedule':'creator round1 at0; released Ghoul gets first independent slot immediately after former creator’s next regular slot at6, not current round1 attached phase; stable body-ID tie. New Mummy cannot voluntarily act round1. Wight remains creator-controlled.'}],
      {'realBodies':3,'liveAuthorityRelations':2,'controlledIDs':['old-Wight','Mummy-corpse'],'independentID':'old-Ghoul','GhoulHP':35,'casterRP':17,'newMummyHP':70,'newMummyAC':16,'newCRAssignments':0,'freeImmediateGhoulActions':0},bodies=[mummycorpse],branches=[
       {'name':'New creation hidden failure','expected':'13RP spent; old two authorities and both old bodies unchanged; no substitute corpse or automatic new command'},
       {'name':'Independent behavior/work beyond release','status':'CONDITIONAL_CONTENT_PREREQUISITE','missing':'actual retained physiological needs, NPC goals and qualified work/roster inputs; no perpetual labor, hostility, loyalty or no-breath claim'}])
    hom=caster('hom-W11',11,['create-homunculus'])
    h=body('Hom',5,size='Tiny',height=2,mass=8)
    parcel={'id':'parcel-H','massLb':20,'Load':2,'boundsFeet':[1,1,1],'contents':'documented mundane material, inclusive gross mass/Load; no creature, weapon or activated consumable','initialBounds':{'min':[6.3,-0.5,0],'max':[7.3,0.5,1]},'handling':'small hands grip supplied exterior handles; nearest grip0.05ft from body’s east face, actually reachable, no tool/expertise'}
    add('TU6-12-A','create-homunculus',[hom],[cast(hom,'create-homunculus',6),
      {'time':0,'round':1,'phase':'actual creator BA after creation, then attached','command':'pick up adjacent unattended handled parcel-H','taskInteractions':1,'movement':0,'channel':'spoken, clearly heard/perceived5ft body-center separation, open LoE, same plane','capacity':{'physical':45,'load':3,'grossCarriedLb':20,'grossCarriedLoad':2,'ownBodyNotCargo':8},'Burdened':True,'adjustedWalk':10,'adjustedFly':20},
      {'time':6,'round':2,'phase':'creator BA then attached','command':'carry parcel to marked floor position15,0 and set it down','FlyCenterRoute':[[5,0,1],[15,0,1]],'distance':10,'rate':1,'cost':10,'availableBeforeDrop':20,'remainingBeforeDrop':10,'sweptBody':{'min':[3.75,-1.25,0],'max':[16.25,1.25,2]},'sweptParcel':'held in front at x-body-east-face+0.05 to+1.05; open whole route, no barrier or other body','endItemBounds':{'min':[16.3,-0.5,0],'max':[17.3,0.5,1]},'taskInteractions':1,'actualSupervisionDistanceLessThan60':True}],
      {'casterRP':27,'homHP':20,'homMaxHP':20,'parcelRealAndUnchanged':True,'physicalLimitPass':True,'LoadLimitPass':True,'round1Commands':1,'round2Commands':1,'attacksOrHelp':0,'trainedWorkAward':0},bodies=[h],branches=[
       {'name':'Second20lb2Load parcel before delivery','expected':'total40lb passes45 but4Load fails3; one bundle label cannot change total; no routine carrying of both'},
       {'name':'Outside supervised task loses channel','initial':'same extant Hom, creator gives actual spoken instruction at distance15 to sort known mundane objects, one interaction per6seconds','timeline':[{'time':6,'state':'supervision present','completedInteractions':1},{'time':7,'input':'creator walks20ft behind an opaque wall, same real body movement/time; LoE supervision lost','completedAdditionalInteractions':0},{'time':12,'state':'still occluded','productiveSteps':0},{'time':18,'input':'creator actually returns to clear channel and restates instruction; clock resumed prospectively','instantCatchup':0},{'time':24,'state':'six genuinely supervised seconds completed','newInteractions':1}],'expected':'body waits/defends during loss; no deleted body, remote shop, simultaneous Watch or created proficiency'}])
    add('TU6-12-B','create-homunculus',[hom],[{'priorLawfulState':'same Divination Wizard11 creation paid13, currentRP27, original Hom7/20 after resolved13HP loss input. Current Homcenter5 and creator0 have body-edge gap1.25, within actual ordinary5ft touch reach; no intervening barrier.'},
       {'time':6,'round':2,'Action':'original creator maintenance','source':'new explicit Homunculus maintenance, not spell','RPBefore':27,'RPPaid':2,'RPAfter':25,'dice':[3,5],'gain':8,'HP':[7,15],'DissonanceBefore':0,'DissonanceAfter':0,'sameSourceAndBody':True}],
      {'HP':15,'maximumHP':20,'CounterspellTrigger':False,'RefrainReset':False,'cargoRefilled':False,'livingAllyPermissionInferred':False},bodies=[h],branches=[
       {'name':'NullDisabled0 extant body','input':'Actual independently established qualifying NullDisabled0 on this same source with all own ending predicates false; packet construction is not asserted here','operation':'same original-creator Action touch2RP, dice3,5','expected':'same body8/20, clear disabled0 only, same real gear/fuel/command history'},
       {'name':'Ordinary0 already ended body','input':'Hom’s ordinary0 destruction already resolved; its real lantern L remains at current floor position with fuel17minutes and existing cracked pane','operation':'attempt maintenance at remains','expected':'no eligible Hom body; no repair/cost; old lantern unchanged. New actual13RP creation is a new identity and does not retrieve or restore lantern'},
       {'name':'Actual Conjuration qualification','actor':caster('hom-conj-W11',11,['create-homunculus'],school='Conjuration'),'operation':'real new Action rank6 Universal cast40->27RP, first prepared familyD0; fit Tiny2.5square at5,0 with2ft height, clear components/range/LoE; no Flesh Ascendant','expected':'new Construct max/current20+11=31; actual spell remains Universal; no class or school alias'}])

def supplements():
    cr=caster('profiles-C11',11,['create-undead'],cls='Cleric')
    for profile,hp,ac,speed,faces,damage_type in [('Ghoul',40,13,40,[3,4],'slashing'),('Wight',45,15,30,[5,6],'necrotic'),('Mummy',70,16,20,[6,7],'bludgeoning')]:
        ranged=profile=='Wight'; foe=recipient(profile+'-foe',40 if ranged else 20)
        actors=[cr,foe]
        if ranged: actors.append(recipient('conscious-hostile-threat',20))
        events=[cast(cr,'create-undead',6),{'formation':{'profile':profile,'corpse':corpse(profile+'-corpse',10),'sameProneAnchor':True,'baseAndFinalHP':hp,'AC':ac,'noCreationRoundActs':True}},
          {'time':6,'round':2,'phase':'creator actual BA then attached','command':'stand and make exactly one native '+profile+' attack','standCost':speed/2,'Speed':speed,'translation':0,'attack':{'target':foe['id'],'bodyGap':25 if ranged else 5,'range':60 if ranged else 5,'d20s':[17,8] if ranged else [12],'selectedDie':8 if ranged else 12,'modifier':8,'total':16 if ranged else 20,'AC':12,'advantage':False,'disadvantage':ranged,'critical':False,'faces':faces,'damageType':damage_type,'damage':sum(faces),'noSpellCast':True}}]
        if ranged:events[-1]['closeQuarters']='Conscious non-Incapacitated hostile at20 sees Wight10 and is within actual body gap5; disadvantage applies despite attacked target at40.'
        if profile=='Ghoul':events[-1]['rider']={'positivePostDefensePreTemp':7,'DC':16,'CONDie':5,'CONBonus':2,'total':7,'Speed':[30,20],'targetFutureTurn':{'start':7,'end':8},'expiry':8,'hardGuardSpent':False}
        add('CL10-PROFILE-'+profile.upper(),'create-undead',actors,events,{'casterRP':17,'casterDissonance':2,'profileHP':hp,'targetHP':60-sum(faces),'ownerOffenses':1,'automaticCR':None,'extraCurseOrDisease':False,'extraSpellCadence':False},bodies=[body(profile,10)],notes=['Ghast’s full ally-inclusive cone is IN6-11-A. No extra physical damage weapon or imported monster ability.'])
    am=caster('suppression-W9',9,['antimagic-field-lesser'],x=27.5)
    amevent=cast(am,'antimagic-field-lesser',5,time=5,round_no=1,concentration=True);amevent['school']='Abjuration'
    amevent['activation']='Ready spell on caster actual regular Action at5; next caster regular START11; V/S/F, price/cadence once now; held concentration starts5'
    amevent['trigger']='Hear the named original creator issue its actual spoken command to the target after creator regular START6; release immediately after that observable completed command, before later attached phase6.5'
    add('CL10-SUPPRESSION-BRANCHES','shared-companion-lifecycle',[am],[
      {'independentFixtures':'Each named branch is a separate encounter state, never seven creatures sharing one space simultaneously. Each original source was actually established at time0 by its source-qualified creator; remaining3HP and current source/gear pose are prior lawful state inputs; no fresh creation or free casting is claimed by this suppression event.'},amevent,
      {'time':6.1,'release':'actual available Reaction; legal point selected now, no second spell cast/price/counter window','point':[20,0,3],'radius':10,'pointRangeFromCasterBody':5,'LoE':'open','targetBody':'Medium5x5x6 at20,0,0; substitute actual Large10x10x8 Golem or Tiny2.5x2.5x2 Hom, all intersect sphere','creator':'original separate creator body at0,0 is outside field; its spoken command was actually legal when issued before the field appeared','expiry':66.1},
      {'time':6.5,'input':'Issued command reaches its genuine original-owner attached opportunity while expression/control suppressed or ended; command is spent/lost. No new Bonus Action or phase created.'},
      {'time':13,'operation':'AM owner ends concentration; original source clocks unchanged'}],
      {'newGlobalSummonRule':False,'branchesReviewedAsSeparateProposedLifecycles':True},branches=[
      {'body':'Golem','originalExpiry':60,'expectedAt7':'body and creating application end; actual real2lb lantern deposited current floor, never copied','expectedAt13':'no return'},
      {'body':'Wraith','originalExpiry':60,'expectedAt7':'manifestation and creating application end; actual cargo settles locally','expectedAt13':'no return'},
      {'body':'Homunculus','originalExpiry':None,'expectedAt7':'persistent source/body ends; actual cargo settles locally','expectedAt13':'no return'},
      {'body':'Knight','originalExpiry':60,'expectedAt7':'body absent with saved current pose20,0,0; real gear drops; HP3 and original60 deadline retained','expectedAt13':'same body3HP returns only if saved-pose suppression cleared and local fit succeeds; no gear pickup; occupied/expiry alternatives NE5-01-B'},
      {'body':'Flood zombie','originalExpiry':3600,'expectedAt7':'same consumed physical body inert, real gear/support/gravity unchanged','expectedAt13':'same3HP animation resumes, old queued order not replayed, original3600 deadline'},
      {'body':'Danse member','originalExpiry':3600,'expectedAt7':'same physical consumed member inert; does not end outside cohort members','expectedAt13':'same3HP member animation, no old order replay, original3600 deadline'},
      {'body':'Create Undead Ghoul','originalExpiry':None,'expectedAt7':'permanent flesh remains3HP; authority suppressed, underlying independent agency; native magical slowing rider unavailable but ordinary physical body survives','schedule':'next independent slot after original creator’s next scheduled occurrence, e.g. creator regular START12; no immediate7 turn; if an actual opportunity already spent that numbered round, no duplicate. Reacquisition at13 retires independent slot prospectively into next genuinely available attached phase. No particular autonomous behavior or work is claimed.'},
      {'body':'Command Undeath target','status':'CONDITIONAL_CONTENT_PREREQUISITE','missing':'actual CR2 full profile and true successful old binding','expectedRuleOnly':'physical body remains; only authority suppresses, original actual schedule retained, no queued-order replay'}])
    nd=caster('null-W3',3,['chill-touch'],x=11.25)
    nd['nullState']='Existing documented active unsuppressed Null Veil at each damage-root creation; no new exposure field or cosmology rule authored.'
    add('CL10-NULL-ZERO-BRANCHES','shared-companion-lifecycle',[nd],[
      {'independentFixtures':'One actual target at20,0,feet0 per separate fixture: Golem60max, Knight80max, Wraith100max, Hom20max, Flood20max, Danse20max, CreateGhoul40max; each current3HP from explicit prior lawful state, real extant source and actor ancestry as named; other original creator at0,10. No target is prone or incapacitated before first attack.'},
      {'time':0,'source':'catalog415 Chill Touch, Wizard Evocation rank0; direct known cantrip, no matrix slot','Action':'actual W3 regular Action; V/S, free hand; base0RP, D0+0 first-name','targetGaps':{'Medium':3.75,'Large':1.25,'Tiny':5},'attack':{'d20':18,'INT':3,'PB':2,'total':23,'targetACAtMost':18,'critical':False,'d8':6,'damage':'necrotic6'},'rootDealer':'null-W3','nullNonlethal':True,'sourceOwnerOfTargetIsNotDealer':True,'result':'same bodyHP0 NullDisabled0; no new Wound/death/Stable/corpse. Independent Chill Touch broad HP block ends at first future original-owner regular END5.5.'},
      {'time':6,'round':2,'Action':'new real Chill Touch, same available components/range','RP':0,'baseDissonance':0,'Refrain':1,'DissonanceAfter':1,'attack':{'d20':18,'modifier':5,'total':23,'d8':6,'critical':False},'newRootNullFlag':True,'result':'same disabled0 body, no fresh corpse/death or reset; new independent broad HP block ends at creator next regular END11.5'}],
      {'allSevenNamedBodyBranches':'same identity/body/gear and original source lifetime; no claimed universal living-ally healing permission','FateAdaptersAdded':0},branches=[
      {'name':'Ordinary damage comparator from same initial3HP state','change':'dealer has no active Veil at root creation; all other cast/attack inputs same','expected':'Golem/Knight/Wraith/Hom end at ordinary0; Flood/Danse/Create leave same consumed remains; no fresh reusable corpse'},
      {'name':'Independent source end','operation':'original creator ends concentration on finite Golem/Knight/Wraith at its real regular turn17, or respective60 deadline expires','expected':'NullDisabled does not prevent ending; no reappearance'},
      {'name':'Actual Hom repair after HP-block expiry','actor':caster('hom-owner-W11',11,['create-homunculus'],x=10,y=5,rp=27),'target':'same Hom20max at20,0; creator moves5ft along+x on actual regular turn17 to15,5, leaving actual touch gap<=5; owner was original creator in this branch','operation':'Chill blocks both expired by11.5; creator Action touch2RP, dice3,5','expected':'RP25, same extant Hom8HP, clearDisabled only; no reset of items/commands/source; no organic Healing Rite invoked'},
      {'name':'Consumed animation healing restriction','operation':'attempt generic Cleric Healing Rite on disabled Flood/Danse/Create','expected':'no scoped living-ally eligibility supplied by CL10, so this source cannot be used as an unearned repair'}])

def transfer_supplements():
    cw=caster('transfer-C11',11,['summon-soul-wraith'],cls='Cleric')
    target=recipient('original-donor',20)
    pal={'id':'martyr-P9','class':'Paladin','classLevel':9,'totalLevel':9,'PB':4,'S':2,'M':4,
      'abilities':{'STR':14,'DEX':10,'CON':14,'INT':8,'WIS':10,'CHA':18},'HP':76,'maximumHP':76,'hpDerivation':'10+2 +8*(6+2)=76','RP':14,'maximumRP':14,
      'body':body('martyr-P9',25,5),'Oath':'Martyr King, sworn at3, unbroken','aura':'Conscious radius15 at9; up to3 allies chosen actual regular START; Aura of Crown+1 saves, no chosen Crown redirection on this root','additionalDailyAura':'fear/charm save+1, not weapon DR','acquired':'automatic chosen-Oath Burden Shared at9 /cards/136','ReactionAvailable':True,'roundRedirectionUsed':False,'Dissonance':0,'previousCastName':None,'strainLimit':10,'equipment':'unarmored, free hand and ordinary focus; spoken components available; no source benefit other than stated'}
    r1=recipient('willing-recipient-1',20,5);r2=recipient('willing-recipient-2',25,0)
    add('CL10-WRAITH-BURDEN-SHARED','summon-soul-wraith',[cw,target,pal,r1,r2],[cast(cw,'summon-soul-wraith',6,concentration=True),
      {'priorState':'Wraith90/100 at10,0 with creator concentration active;3 allied donor bodies chosen in Paladin’s aura at its real regular START5; all explicitly accept their named amounts and all are genuine noncreated living bodies'},
      {'time':6.5,'round':2,'command':'creator real BA at6, attached Wraith attack original-donor','attack':{'gap':5,'die':12,'modifier':8,'total':20,'AC':12,'critical':False,'dice':[7,7],'rawNecrotic':14,'dealer':'Wraith','Null':False}},
      {'reaction':'Paladin Burden Shared after target defenses, before tempHP','source':'paladin /cards/136','RP':[14,9],'rank':3,'Dissonance':[0,1],'Refrain':0,'transferAmount':10,'cap':13,'branches':[{'id':'original-donor','damage':4,'eligibleFunding':4},{'id':'willing-recipient-1','damage':5,'eligibleFunding':0,'flags':['no-derived-healing','no-redirect','no-reflection','no-resource']},{'id':'willing-recipient-2','damage':5,'eligibleFunding':0,'flags':['no-derived-healing','no-redirect','no-reflection','no-resource']}],'otherReactions':[],'sharedPaladinRedirectionSpent':True}],
      {'originalHP':56,'recipient1HP':55,'recipient2HP':55,'PaladinHP':76,'actualDamageConserved':14,'eligibleWraithDamage':4,'lifetap':2,'WraithHP':92,'newWounds':0,'PaladinSelfAbsorptionRider':False,'originalParentCountedAgain':False},bodies=[body('Wraith',10,height=6,mass=0)],notes=['Paladin is not a transferred recipient; self-absorption healing cannot be manufactured. This is a separate actual proposed encounter, not an allowed farming strategy.'])
    ora={'id':'life-O6','class':'Oracle','classLevel':6,'totalLevel':6,'PB':3,'S':2,'M':4,
      'abilities':{'STR':10,'DEX':14,'CON':14,'INT':8,'WIS':10,'CHA':18},'HP':38,'maximumHP':38,'hpDerivation':'6+2+5*(4+2)=38','body':body('life-O6',20,10),'RC':5,'RCMax':5,'RP':None,
      'Mystery':'Life at1','Curse':'Burning Blood at1, boons I/II actually acquired; no optional ignition; necrotic transferred damage is not a slashing/piercing wound or direct weapon hit','selectedTierI':'Overflowing Light, inactive','selectedTierII':'Life Linked at6, /cards/174','LifeBloomWard':'actual automatic /cards/169; no placed bloom, self first necrotic reduction cannot apply a second defense stage to transferred damage','ReactionAvailable':True,'roundLifeLinkTransferUsed':False,'conditions':[],'noOtherActiveEffects':True}
    add('CL10-WRAITH-LIFE-LINKED','summon-soul-wraith',[cw,target,ora],[cast(cw,'summon-soul-wraith',6,concentration=True),
      {'time':-1,'OracleRegularStart':-2,'nextStarts':[4,10],'Action':'Life Linked original-donor, willing living ally','range':'body gap5<=five actual5ft tiles(25ft), same plane, perceived/clear LoE','RC':[5,3],'duration':'2round ally buff until Oracle second future regular START10','concentration':False,'WeaveDissonance':False},
      {'priorState':'same Wraith90/100 at10,0; concentration from0; Oracle/target stay within25ft'},
      {'time':6.5,'round':2,'command':'actual creator BA at6 then attached Wraith attack','attack':{'gap':5,'d20':12,'modifier':8,'total':20,'AC':12,'critical':False,'dice':[7,7],'rawNecrotic':14},'firstNecroticReduction':2,'postDefense':12,'OracleReactionTransfer':6,'split':[6,6],'OracleBranchFlags':['no-redirect','no-second-mitigation','no-recovery','no-retaliation','no-resource','no-copy'],'noSecondBloomSelfReduction':True}],
      {'originalHP':54,'OracleHP':32,'OracleRC':3,'WraithEligibleTerminalDamage':6,'lifetap':3,'WraithHP':93,'OracleLifeProphecyTriggered':False,'newWounds':0,'rootConservation':'14=2 prevented+6 original+6 transferred','linkStillEnds':10},bodies=[body('Wraith',10,height=6,mass=0)])

group_one()
group_two()
group_three()
supplements()
transfer_supplements()

# Explicit shared prior-source inputs, separately instantiated per lifecycle branch.
SOURCE_LIFECYCLES=[
 {'label':'Golem','spell':'summon-corpse-golem','rank':4,'maxHP':60,'duration':60,'size':'Large','height':8,'mass':600},
 {'label':'Knight','spell':'summon-death-knight','rank':5,'maxHP':80,'duration':60,'size':'Medium','height':6,'mass':180},
 {'label':'Wraith','spell':'summon-soul-wraith','rank':6,'maxHP':100,'duration':60,'size':'Medium','height':6,'mass':0},
 {'label':'Homunculus','spell':'create-homunculus','rank':6,'maxHP':20,'duration':None,'size':'Tiny','height':2,'mass':8},
 {'label':'Flood zombie','spell':'negative-energy-flood','rank':5,'maxHP':20,'duration':3600,'size':'Medium','height':6,'mass':180},
 {'label':'Danse member','spell':'danse-macabre','rank':5,'maxHP':20,'duration':3600,'size':'Medium','height':6,'mass':180},
 {'label':'Create Undead Ghoul','spell':'create-undead','rank':6,'maxHP':40,'duration':None,'size':'Medium','height':6,'mass':180},
]
for case in CASES:
    if case['id']=='IN6-07-B':
        case['actors'][0]['body']=body('wraith-C11',-12.5)
    if case['id']=='CL10-WRAITH-LIFE-LINKED':
        case['events'][0],case['events'][1]=case['events'][1],case['events'][0]
    if case['id'] in ['CL10-SUPPRESSION-BRANCHES','CL10-NULL-ZERO-BRANCHES']:
        owner=caster('original-source-W11',11,[s['spell'] for s in SOURCE_LIFECYCLES],x=0,y=10 if case['id']=='CL10-NULL-ZERO-BRANCHES' else 0)
        case['actors'].append(owner)
        case['independentPriorSourceInstances']=[]
        for row in SOURCE_LIFECYCLES:
            price=[0,2,3,5,7,10,13][row['rank']]
            formed=-19 if case['id']=='CL10-NULL-ZERO-BRANCHES' else 0
            case['independentPriorSourceInstances'].append({**deepcopy(row),'actualBody':body(row['label'],20,size=row['size'],height=row['height'],mass=row['mass']),
              'creator':'original-source-W11','createdAt':formed,'sourceExpiry':None if row['duration'] is None else formed+row['duration'],
              'originalCasting':'actual source-qualified Wizard11 Action at indicated prior time, listed spell learned/prepared, available V/S/F, declared legal body/target/matter under that exact procedure; first prepared familyD0; no surcharge/discount; created/formed exactly once',
              'creatorRPAtThatCast':[40,40-price],'initialHP':row['maxHP'],'currentHP':3,'lossBeforeFixture':row['maxHP']-3,
              'historyBoundary':'These are explicit prior lawful body/source inputs, not a claimed replay/test of unsupplied attacks. Consumed animations retain real connected head/torso, no missing parts and consumed allocation; finite manifestations create no reusable corpse. No generic approval of a bestiary profile.',
              'currentFlags':'no resistance/temporaryHP/Wound/armor/max modifier; no gear except where branch expressly gives real lantern; no Conjuration or Flesh Ascendant',
              'ownerMarkers':'Null fixture START -1,5,11,17 and END -.5,5.5,11.5,17.5; suppression fixture START0,6,12,18, END+.25 and attached+.5',
              'atMostOneBodyFromThisTablePerIndependentFixture':True})
        if case['id']=='CL10-SUPPRESSION-BRANCHES':
            for branch in case['independentBranches']:
                if 'expectedAt7' in branch:branch['expectedAt6_1']=branch.pop('expectedAt7')
        else:
            case['independentBranches'][1]['operation']='Original creator ends concentration on finite Golem/Knight/Wraith at its real regular turn17, or source’s actual formation-19 plus60 deadline41 expires.'

AUTHORING_QUESTIONS=[
 {'id':'CL10-C03-Q01','scope':'Soulburn Pact / Grand Reservoir','question':'Does Grand Reservoir’s cannot-combine-with-another-RP-refund-feature restriction prohibit Soulburn’s own0..3 recovery on that waived cast? The supplied zero-recovery waiver comparator avoids silently granting a profitable combination. Please supply the exact positive/blocked ruling before we claim a positive waived-recovery case.','status':'UNSENT_NEW_TEXT_INTERPRETATION'},
 {'id':'CL10-C03-Q02','scope':'Soul Wraith real cargo fixture','question':'Confirm two usable gripping extremities as a narrow new body-profile completion for legal mundane pickup/drop, or supply a source-compatible alternative for the required actual chest-deposition case. No extra weapon, skill or professional task is inferred. The current case labels this new premise and does not claim it inherited.','status':'UNSENT_SCOPED_COMPLETION'},
 {'id':'CL10-C03-Q03','scope':'Ghast15ft cone','question':'Confirm the case-local15ft axial cone with circular cross-section diameter equal to forward distance, origin actual head outlet and volume intersection. The inherited DI7 formula is scoped to another spell; no global shape import is asserted. Both case witnesses are well inside this explicitly proposed cone.','status':'UNSENT_GEOMETRIC_COMPLETION'},
 {'id':'CL10-C03-Q04','scope':'Soul Wraith physical weight','question':'Current geometry fixtures explicitly use0lb for the generated manifestation but do not assert that value is printed or grant carrying immunity. Choose an explicit bounded profile mass (or leave weight-dependent operations conditional) before treating physical-load cases as fully qualified. STR6/Medium ordinary cargo capacities remain independently sourced.','status':'UNSENT_PROFILE_COMPLETION'},
 {'id':'CL10-C03-Q05','scope':'Command Undeath / bestiary content','question':'The frozen26-record bestiary has no full operative authoritative exactCR2 Undead. Both original positive Command cases remain conditional. Confirm the next content-authoring boundary: develop a distinct source-based complete NPC profile in a separate review, or keep these two positive cases open. Do not assignCR2 to an unrated Create Undead body merely to satisfy the tests.','status':'CONTENT_PREREQUISITE_NOT_AN_ADOPTED_PROFILE'}
]
