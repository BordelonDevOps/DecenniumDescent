from __future__ import annotations
import copy, hashlib, json, pathlib, zipfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
ARCHIVE = HERE / 'rank9_materialforging2_return247_received' / 'DD_Rank9_MaterialForging2_Director_Return247_HELD.zip'
OUT = HERE / 'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_254.json'
AUDIT = HERE / 'ETERNAL_FORGE_MF210_B01_SUPPLEMENT_254_INDEPENDENT_AUDIT.json'

def canon(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def sha(v): return hashlib.sha256(canon(v)).hexdigest()
def file_sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ptr(parts): return '/' + '/'.join(str(x).replace('~', '~0').replace('/', '~1') for x in parts)

def diff(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        out=[]
        for k in sorted(a.keys()-b.keys()):
            p=ptr(path+(k,)); out += [{'op':'test','path':p,'value':a[k]},{'op':'remove','path':p}]
        for k in sorted(b.keys()-a.keys()): out.append({'op':'add','path':ptr(path+(k,)),'value':b[k]})
        for k in sorted(a.keys()&b.keys()): out += diff(a[k],b[k],path+(k,))
        return out
    if a == b: return []
    p=ptr(path); return [{'op':'test','path':p,'value':a},{'op':'replace','path':p,'value':b}]

def local_binding(path):
    p=REPO/path; data=p.read_bytes(); return {'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def zip_binding(member):
    with zipfile.ZipFile(ARCHIVE) as z: data=z.read(member)
    return {'path':ARCHIVE.relative_to(REPO).as_posix(),'packetMember':member,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

with zipfile.ZipFile(ARCHIVE) as z:
    source_case=json.loads(z.read('cases/MF210-F02.json'))
base=copy.deepcopy(source_case['events'][-1]['after'])
assert source_case['events'][-1]['id']=='MF210-F02:6' and base['time']==12.1
a0=base['actors']['A']; i0=base['items']['bracelet-1']
assert (a0['RP'],i0['id'],i0['recipe'],i0['HP'],i0['charges'],i0['imprintRoot']['id'])==(38,'bracelet-1','recipe-241',5,0,'castF2')
assert i0['custodian']=='A-wrist' and i0['worn'] is True and sha(base)==source_case['events'][-1]['afterSHA256']

state=copy.deepcopy(base); events=[]
def event(eid,kind,end,desc,mutate):
    before=copy.deepcopy(state); mutate(state); state['time']=end
    if eid not in state['processedEvents']: state['processedEvents'].append(eid)
    after=copy.deepcopy(state)
    events.append({'id':eid,'kind':kind,'timeStartSeconds':before['time'],'timeEndSeconds':end,'description':desc,
        'beforeSHA256':sha(before),'afterSHA256':sha(after),'forward':diff(before,after),'inverse':diff(after,before)})

def init_fixture(s):
    # Construct a fresh minimal actor rather than copying the prior-case Wizard.
    b={'id':'B','positionFeet':[5,0,0],'HP':10,'maxHP':10,'RP':0,'maxRP':0,'Dissonance':0,'Refrain':0,
        'lastSpell':None,'usedPreparedFamilies':[],'regularStart':None,'nextRegularStart':18.2,
        'regularStartsProcessed':[],'Action':0,'Reaction':1,'BonusAction':0,'freeInteraction':0,
        'movementRemaining':30,'recharge':{},'ready':None,'concentration':None,
        'hands':{'left':None,'right':None},'worn':[],'resourceHistory':[],'resourceCredits':[],
        'deathSaves':{'applicable':False,'success':0,'failure':0},'conditions':[],'turnCast':False,
        'conscious':True,'incapacitated':False,
        'profile':{'id':'MF210-W2-RECEIVER-01','status':'authored static noncasting fixture',
        'fixtureQualification':'No class progression, spellbook, spellcasting, or prior-case actor history is asserted.',
        'class':None,'classLevel':None,'size':'Medium','AC':12,'ACDerivation':'unarmored 10 + DEX 2; no armor or shield',
        'HP':10,'maxHP':10,'abilities':{'DEX':14},
        'modifiers':{'DEX':2},'proficiencyBonus':0,'skills':[],'stealthProficiency':False,
        'body':{'size':'Medium','dimensionsFeet':[5,5,6],'hands':2,'wrists':['left','right'],
            'wristAnatomy':'two ordinary compatible wrists; recipe-241 Bracelet fit is an explicit local fixture input',
            'rightWristPointFeet':[2.5,0,3],'orientation':'facing A at the bounded handoff point',
            'walkFeet':30},'spellcasting':False,'learned':[],'prepared':[],'inventory':[]}}
    s['actors']['B']=b
    s['scene']['BoccupiedBoxFeet']=[[2.5,-2.5,0],[7.5,2.5,6]]; s['scene']['BpositionFeet']=[5,0,0]
    s['scene']['w2Geometry']={'authorship':'new bounded local fixture; no global dimensions claimed','Afeet':[0,0,0],
        'Bfeet':[5,0,0],'BoccupiedBoxFeet':[[2.5,-2.5,0],[7.5,2.5,6]],'Bfacing':'toward A',
        'BRightWristPointFeet':[2.5,0,3],'braceletWristPoint':[2.5,0,3],'handoffPointFeet':[2.5,0,3],
        'AtoBraceletFeet':3.905,'lineOfEffect':'unblocked',
        'adjacentOpaqueHideCover':{'pointFeet':[2.5,2.5,0],'blocksClearViewOfB':True,'blocksLineOfEffectToBracelet':False},'noTravel':True}
    s['scene']['restSite']={'id':'MF210-W2-RETUNE-REST-SITE-01','fixtureLocation':'safe enclosed resting room at the bounded W2 site',
        'safeAndPermitted':True,'hostileInterruption':False,'hazardDuringRest':False}
    s['supplement']={'id':'MF247-F-W2','status':'local noncanonical fixture; GPT review required',
        'campaignClock':{'campaignId':'MF210-W2-CLOCK-01','epochD0Seconds':0,'epochDesignation':'06:00',
            'secondsPerDawn':86400,'dawns':[{'index':1,'timeSeconds':86400,'identity':'MF210-W2-CLOCK-01:jewelcrafting-dawn:1'},
                {'index':2,'timeSeconds':172800,'identity':'MF210-W2-CLOCK-01:jewelcrafting-dawn:2'}]},
        'receiver':{'actorId':'B','profileId':'MF210-W2-RECEIVER-01','status':'authored noncanonical noncasting fixture',
            'classProgression':None,'spellbook':None,'spellcasting':False,'HP':10,'maxHP':10,'AC':12,'size':'Medium',
            'bodyDimensionsFeet':[5,5,6],'wristAnatomy':'two ordinary wrists; explicit fixture fit for recipe-241 Bracelet',
            'rightWristPointFeet':[2.5,0,3],'occupiedPositionFeet':[[2.5,-2.5,0],[7.5,2.5,6]],'facing':'toward A',
            'DEX':14,'DEXModifier':2,'StealthProficiency':False,'StealthProficiencyBonus':0,'otherStealthBonuses':[],
            'hands':{'left':'empty','right':'empty'},'positionFeet':[5,0,0],'movementFeet':30,'conscious':True,'incapacitated':False,
            'consents':['receive','wear','object-damage test'],'rightWristOpen':True,'otherJewelry':[],
            'competingEquipmentEffects':[],'castsInWitness':False},
        'initiativeEpisodes':[],'rests':[],'dawnEvents':[],'custodyHistory':[],'objectDamageEvents':[],
        'chargeTransactions':[],'spellEvents':[],'imprintEndings':[],'newCreations':[],'timelineGaps':[],'noncanonical':True}
event('MF247-F-W2-E01-RECEIVER-ENTRY','authored-receiver-fixture-entry',12.2,
    'Add a distinct source-derived receiver after exact MF210-F02:6; import no prior actor-B history.',init_fixture)

def start_a18(s):
    a=s['actors']['A']; a.update({'regularStart':18,'nextRegularStart':24,'regularStartsProcessed':[18],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
    s['supplement']['initiativeEpisodes'].append({'id':'MF210-W2-TRANSFER','startSeconds':18,'endSeconds':24.3,
        'initiativeRolls':{'A':{'d20':16,'DEX':2,'total':18},'B':{'d20':9,'DEX':2,'total':11}},'order':['A','B'],'newEncounter':True})
event('MF247-F-W2-E02-A-START-18','regular-turn-start',18,'A begins the authored transfer encounter, ordered before B.',start_a18)

def doff(s):
    a=s['actors']['A']; it=s['items']['bracelet-1']; a['Action']=0; a['worn'].remove('bracelet-1'); a['hands']['right']='bracelet-1'
    it['revision']+=1; it['custodian']='A-right-hand'; it['worn']=False; it['positionBoxFeet']=[2.5,0,3]
    s['supplement']['custodyHistory'].append({'timeSeconds':18.1,'from':'A-wrist','to':'A-right-hand','itemId':'bracelet-1','owner':'A',
        'consent':True,'cost':'A Action','positionBeforeFeet':[2.5,0,3],'positionAfterFeet':[2.5,0,3]})
event('MF247-F-W2-E03-A-DOFF','source-one-Action-doff',18.1,'A spends one Action to doff bracelet-1; owner and 0/1 charge history remain.',doff)

def handoff(s):
    a=s['actors']['A']; b=s['actors']['B']; it=s['items']['bracelet-1']
    b.update({'regularStart':18.2,'nextRegularStart':24.2,'regularStartsProcessed':[18.2],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
    assert a['hands']['right']=='bracelet-1' and b['hands']['right'] is None
    a['hands']['right']=None; b['hands']['right']='bracelet-1'; b['freeInteraction']=0
    it['revision']+=1; it['custodian']='B-right-hand'
    s['supplement']['custodyHistory'].append({'timeSeconds':18.2,'from':'A-right-hand','to':'B-right-hand','itemId':'bracelet-1','owner':'A',
        'consent':True,'cost':'B free object interaction','positionBeforeFeet':[2.5,0,3],'positionAfterFeet':[2.5,0,3],
        'receiverRightHandPointFeet':[2.5,0,3]})
event('MF247-F-W2-E04-B-HANDOFF','consensual-free-interaction-handoff',18.2,'B receives the same physical bracelet by consensual free interaction; no charge reset.',handoff)

def start_a24(s):
    a=s['actors']['A']; a.update({'regularStart':24,'nextRegularStart':30,'regularStartsProcessed':a['regularStartsProcessed']+[24],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
event('MF247-F-W2-E05-A-START-24','regular-turn-start',24,'A receives the next regular turn.',start_a24)

def don(s):
    b=s['actors']['B']; it=s['items']['bracelet-1']
    b.update({'regularStart':24.2,'nextRegularStart':30.2,'regularStartsProcessed':b['regularStartsProcessed']+[24.2],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
    b['Action']=0; b['hands']['right']=None; b['worn'].append('bracelet-1')
    it['revision']+=1; it['custodian']='B-right-wrist'; it['worn']=True
    s['supplement']['custodyHistory'].append({'timeSeconds':24.2,'from':'B-right-hand','to':'B-right-wrist','itemId':'bracelet-1','owner':'A',
        'consent':True,'rightWristOpen':True,'cost':'B Action to don','positionBeforeFeet':[2.5,0,3],
        'positionAfterFeet':[2.5,0,3],'receiverRightWristPointFeet':[2.5,0,3]})
event('MF247-F-W2-E06-B-DON','source-one-Action-don',24.2,'B spends one Action to don the bracelet on an open wrist; charges remain 0/1.',don)

def rest(s):
    a=s['actors']['A']; a['RP']=59; a['Dissonance']=0; a['concentration']=None; a['ready']=None
    s['supplement']['initiativeEpisodes'][-1]['endSeconds']=24.3; s['supplement']['initiativeEpisodes'][-1]['closedNormally']=True
    s['supplement']['rests'].append({'id':'MF210-W2-RETUNE-REST-01','actor':'A','startSeconds':24.3,'endSeconds':3624.3,'durationSeconds':3600,'beneficial':True,
        'uninterrupted':True,'beneficialShortRestsSinceLongRest':1,'maximum':2,'formula':'max(0, floor(maxRP/4 + 0.5) + casting modifier)',
        'arithmetic':{'maxRP':64,'roundedQuarter':16,'INTModifier':5,'recovery':21,'before':38,'after':59},
        'location':'MF210-W2-RETUNE-REST-SITE-01; safe enclosed resting room in the bounded W2 fixture, with no hostile interruption or hazard during the interval',
        'safeAndPermittedCircumstances':True,'completionId':'MF210-W2-RETUNE-REST-01-COMPLETE',
        'overlappingActiveWork':False,'automaticHPRecovery':False,'ArcaneRecoveryUsed':False,'ArcaneRecoveryAcquired':False,
        'HPRecovery':0,'DissonanceBefore':0,'DissonanceAfter':0,'DissonanceCleared':True,'RefrainBefore':a['Refrain'],
        'RefrainReset':False,'rememberedSpellNameReset':False,'preparedFamilyHistoryReset':False})
    s['supplement']['timelineGaps'].append({'fromSeconds':3624.3,'toSeconds':86398,'mode':'out of initiative','noActorTurnsOrRelocation':True,
        'noTimedEffectsOrConcentration':True,'noOmittedDawnBefore86400':True,'noOtherRestBenefit':True})
event('MF247-F-W2-E07-ONE-HOUR-RETUNE','completed-one-hour-short-rest',3624.3,
    'A completes safe, permitted, uninterrupted Retune rest MF210-W2-RETUNE-REST-01; shared formula restores 21 RP (38 to 59), clearing Dissonance while preserving Refrain and spell-family history. No overlapping work, automatic HP recovery, or Arcane Recovery occurs.',rest)

def advance_field(s): pass
event('MF247-F-W2-E08-ADVANCE-TO-DAWN1','out-of-initiative-clock-advance',86398,
    'Advance to two seconds before fixed dawn 1; no unrecorded action, relocation, damage, repair, rest or timed effect occurs.',advance_field)

def lesser_antimagic(s):
    a=s['actors']['A']; a.update({'regularStart':86398,'nextRegularStart':86404,'regularStartsProcessed':[86398],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False,'usedPreparedFamilies':[]})
    a['Action']=0; a['RP']-=10; a['lastSpell']='antimagic-field-lesser'; a['Dissonance']=0; a['turnCast']=True
    a['usedPreparedFamilies']=['antimagic-field-lesser']
    a['resourceHistory'].append({'castId':'amfW2','spell':'antimagic-field-lesser','time':86398,'cost':10,'action':'Action','firstFamily':True,'baseDissonance':0,'RefrainAdded':0})
    a['concentration']={'castId':'amfW2','spell':'antimagic-field-lesser','startsAtSeconds':86398,'expiresAtSeconds':86458,
        'maximumDurationSeconds':60,'centerFeet':[2.5,0,3],'radiusFeet':10,'lineOfEffect':'unblocked','concentration':True}
    s['terminalCasts']['amfW2']={'caster':'A','spell':'antimagic-field-lesser','rank':5,'paidRP':10,'paidAction':'Action',
        'components':'V/S/F','status':'resolved','origin':[0,0,0],'authorizationFrozen':{'profile':'antimagic-field-lesser#procedure','centerFeet':[2.5,0,3],'radiusFeet':10,'durationSeconds':60}}
    s['supplement']['spellEvents'].append({'castId':'amfW2','caster':'A','spell':'antimagic-field-lesser','rank':5,'timeSeconds':86398,
        'costRP':10,'action':'Action','target':'bracelet-1 and castF2 root intersect the field','centerFeet':[2.5,0,3],
        'rangeFeet':3.905,'radiusFeet':10,'expiresAtSeconds':86458})
    s['supplement']['activeEffects']={'amfW2':{'status':'active','centerFeet':[2.5,0,3],'radiusFeet':10,'expiresAtSeconds':86458,'suppresses':'castF2'}}
    s['supplement']['initiativeEpisodes'].append({'id':'MF210-W2-SUPPRESSION','startSeconds':86398,'endSeconds':86398.2,
        'initiativeOrder':['A','B'],'Ainitiative':18,'Binitiative':11,'closedAfterCast':True})
event('MF247-F-W2-E09-PAID-ANTIMAGIC-CAST','actual-paid-lesser-antimagic-cast',86398,
    'A spends 10 RP and one Action on prepared Lesser Antimagic; the fixed 10-foot field is centered on the bracelet, within 10 feet, and lasts 60 seconds.',lesser_antimagic)

def field_intersection(s):
    it=s['items']['bracelet-1']; it['revision']+=1; it['imprintRoot']['suppressed']=True
    s['supplement']['activeEffects']['amfW2']['status']='suppressing-castF2'
event('MF247-F-W2-E10-APPLY-FIELD','field-intersects-and-suppresses-imprint',86398.1,
    'The field intersects the worn bracelet; its physical body, custody, HP, ownership, root identity and zero-charge ledger remain.',field_intersection)

def dawn1(s):
    it=s['items']['bracelet-1']; it['revision']+=1
    it['processedDawns'].append('MF210-W2-CLOCK-01:jewelcrafting-dawn:1')
    s['supplement']['dawnEvents'].append({'index':1,'timeSeconds':86400,'identity':'MF210-W2-CLOCK-01:jewelcrafting-dawn:1',
        'itemId':'bracelet-1','eligible':False,'reason':'castF2 suppressed by active amfW2','chargesBefore':0,'chargesAfter':0,'processedOnce':True})
event('MF247-F-W2-E11-SUPPRESSED-DAWN1','process-ineligible-dawn-once',86400,
    'Dawn 1 is processed while suppressed. The charge stays 0 and no future refill is banked.',dawn1)

def resume(s):
    it=s['items']['bracelet-1']; a=s['actors']['A']; it['revision']+=1; it['imprintRoot']['suppressed']=False
    a['concentration']=None; s['supplement']['activeEffects']['amfW2']['status']='ended-at-deadline'
    s['supplement']['activeEffects']['amfW2']['endedAtSeconds']=86458
    s['supplement']['timelineGaps'].append({'fromSeconds':86458,'toSeconds':86460,'noCatchUpRecharge':True})
event('MF247-F-W2-E12-FIELD-EXPIRES-NO-CATCHUP','concentration-deadline-resumption',86458,
    'The 60-second field ends at its exact deadline. The still-live root resumes; the processed dawn is not replayed.',resume)

def sunder_start(s):
    a=s['actors']['A']; b=s['actors']['B'];
    a.update({'regularStart':86460,'nextRegularStart':86466,'regularStartsProcessed':[86460],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
    b.update({'regularStart':86460.2,'nextRegularStart':86466.2,'regularStartsProcessed':[86460.2],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
    s['supplement']['initiativeEpisodes'].append({'id':'MF210-W2-SUNDER','startSeconds':86460,'endSeconds':86460.2,
        'initiativeOrder':['A','B'],'Ainitiative':18,'Binitiative':11})
    a['freeInteraction']=0; a['hands']['right']='dagger'
    for x in a['profile']['inventory']:
        if x['id']=='dagger': x['custody']='right hand'
    s['supplement']['objectDamageEvents'].append({'id':'sunderW2','attacker':'A','target':'bracelet-1','timeSeconds':86460.1,
        'weapon':'dagger','ownerConsent':True,'draw':'one free interaction from belt','attackAction':True,'attacksConsumed':1})
event('MF247-F-W2-E13-SUNDER-START-DRAW','object-damage-turn-start-and-draw',86460,
    'A begins a fresh turn and draws the source-listed dagger with one free interaction; the item is in 5-foot reach.',sunder_start)

def sunder_hit(s):
    a=s['actors']['A']; b=s['actors']['B']; it=s['items']['bracelet-1']; a['Action']=0
    it['revision']+=1; it['HP']=2; it['damageDeficit']=3; it['functionalState']='positive-HP-damaged'
    s['rolls'].append({'id':'sunderW2','kind':'weapon-attack-against-worn-object','attacker':'A','target':'bracelet-1','weapon':'dagger',
        'd20':11,'DEX':2,'PB':6,'proficient':True,'attackTotal':19,'targetAC':19,'ACRule':'max(material AC 19, wearer AC 12)',
        'hit':True,'damageDie':'1d4 piercing','dieResult':1,'damageAbility':2,'damageTotal':3,'critical':False,'wearerDamage':0})
    s['supplement']['objectDamageEvents'][0].update({'wearerAC':12,'itemHPBefore':5,'itemHPAfter':2,'wearerHPBefore':b['HP'],
        'wearerHPAfter':b['HP'],'chargeLedgerPreserved':0,'castF2Preserved':True})
event('MF247-F-W2-E14-SUNDER-HIT','actual-sunder-object-damage',86460.1,
    'One legal dagger Sunder attack hits AC 19 for 3 piercing damage. Only bracelet HP changes 5 to 2; wearer HP, charges and root remain.',sunder_hit)

def close_sunder(s):
    s['supplement']['initiativeEpisodes'][-1]['endSeconds']=86460.2
    s['supplement']['initiativeEpisodes'][-1]['closedNormally']=True
event('MF247-F-W2-E15-CLOSE-SUNDER','close-object-test-encounter',86460.2,'Close the bounded Sunder encounter after one attack.',close_sunder)

def advance_dawn2(s):
    s['supplement']['timelineGaps'].append({'fromSeconds':86460.2,'toSeconds':172800,'mode':'out of initiative',
        'noActionsDamageRepairOrRelocation':True,'noCatchUpBeforeDawn2':True})
event('MF247-F-W2-E16-ADVANCE-TO-DAWN2','out-of-initiative-clock-advance',172800,
    'Advance the same fixed campaign clock to dawn 2; no intervening item event occurs.',advance_dawn2)

def dawn2(s):
    it=s['items']['bracelet-1']; assert it['HP']==2 and it['charges']==0 and it['complete'] and it['imprintRoot']['active'] and not it['imprintRoot']['suppressed']
    it['revision']+=1; it['processedDawns'].append('MF210-W2-CLOCK-01:jewelcrafting-dawn:2'); it['charges']=1
    s['supplement']['dawnEvents'].append({'index':2,'timeSeconds':172800,'identity':'MF210-W2-CLOCK-01:jewelcrafting-dawn:2',
        'itemId':'bracelet-1','eligible':True,'reason':'complete, HP 2, unsuppressed','chargesBefore':0,'chargesAfter':1,'processedOnce':True})
event('MF247-F-W2-E17-ELIGIBLE-DAWN2','eligible-dawn-refill-once',172800,
    'Dawn 2 refills the complete, positive-HP, unsuppressed item once from 0 to maximum 1.',dawn2)

def hide_and_spend(s):
    b=s['actors']['B']; it=s['items']['bracelet-1']
    b.update({'regularStart':172800.2,'nextRegularStart':172806.2,'regularStartsProcessed':[172800.2],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False})
    assert it['custodian']=='B-right-wrist' and it['charges']==1 and not b['conditions']
    it['revision']+=1; it['charges']=0; b['Action']=0
    s['rolls'].append({'id':'hideW2','kind':'DEX-Stealth','actor':'B','action':'Hide',
        'eligibleBecause':'adjacent opaque cover prevents clear view by A','observer':'A','observerPassiveDC':19,
        'observerPassiveDCDerivation':'10 + WIS modifier 3 + Perception proficiency 6','chargeDeclaredBeforeRoll':True,
        'chargeDebitedBeforeDice':True,'itemId':'bracelet-1','advantageSource':'recipe-241','diceInputs':[8,15],
        'selectedDie':15,'DEX':2,'proficiencyAdded':0,'flatFamilyBonus':1,'total':18,'result':'Failure; B remains perceivable to A'})
    s['supplement']['chargeTransactions'].append({'id':'bracelet-1-hideW2','timeSeconds':172800.2,'itemId':'bracelet-1',
        'actor':'B','rollId':'hideW2','before':1,'after':0,'declaredBeforeRoll':True,'advantageApplied':True})
    s['supplement']['currentEncounter']={'id':'MF210-W2-ENDING-AND-RECREATION','startSeconds':172800.1,
        'initiativeOrder':['B','A'],'Ainitiative':12,'Binitiative':18,'newEncounter':True}
event('MF247-F-W2-E18-B-HIDE-CHARGE','real-hide-check-with-pre-roll-charge',172800.2,
    'After refill, B spends the charge immediately before a real Hide DEX(Stealth) check with advantage; it fails against A’s passive DC, so A can still perceive the item.',hide_and_spend)

def a_start_for_dispel(s):
    a=s['actors']['A']; a.update({'regularStart':172800.4,'nextRegularStart':172806.4,'regularStartsProcessed':[172800.4],
        'Action':1,'Reaction':1,'BonusAction':1,'freeInteraction':1,'movementRemaining':30,'turnCast':False,'usedPreparedFamilies':[]})
    s['supplement']['initiativeEpisodes'].append({'id':'MF210-W2-ENDING-AND-RECREATION','startSeconds':172800.1,
        'endSeconds':172806.6,'initiativeOrder':['B','A'],'Ainitiative':12,'Binitiative':18,'newEncounter':True})
event('MF247-F-W2-E19-A-START-FOR-DISPEL','regular-turn-start',172800.4,
    'A receives an Action after B’s failed Hide check; the center is perceived, unobstructed and within Greater Dispel’s 30-foot range.',a_start_for_dispel)

def greater_dispel(s):
    a=s['actors']['A']; it=s['items']['bracelet-1']; assert a['Action']==1 and a['RP']==49 and it['imprintRoot']['active']
    a['Action']=0; a['RP']-=10; a['lastSpell']='greater-dispel'; a['Dissonance']=0
    a['usedPreparedFamilies'].append('greater-dispel')
    a['resourceHistory'].append({'castId':'greaterDispelW2','spell':'greater-dispel','time':172800.5,'cost':10,
        'action':'Action','firstFamily':True,'baseDissonance':0,'RefrainAdded':0})
    check={'caster':'A','target':'ongoing Until-dispelled spell application castF2','perceivedCenterFeet':[2.5,0,3],
        'centerPerceived':True,'centerDistanceFeet':3.905,'maximumRangeFeet':30,'radiusFeet':30,
        'centerLineOfEffect':'unblocked','alliesIncludedInCaptureRule':True,
        'immutableCapturedApplications':['castF2'],'noOtherEligibleApplicationsInVolume':True,
        'targetGeneratingRank':9,'d20':17,'INT':5,'PB':6,'total':28,'DC':28,
        'DCFormula':'10 + 2 × generating rank 9','degree':'Success','castF2NotSuppressed':True}
    s['rolls'].append({'id':'dispelW2','kind':'Greater Dispel rank-check','source':'greater-dispel#procedure',**check})
    it['revision']+=1; it['imprintRoot']['active']=False; it['imprintRoot']['suppressed']=False
    it['imprintRoot']['endReason']='actual-successful-dispel'; it['imprintRoot']['endedAtSeconds']=172800.5
    s['terminalCasts']['greaterDispelW2']={'caster':'A','spell':'greater-dispel','rank':5,'paidRP':10,
        'paidAction':'Action','components':'V/S/F','status':'resolved','origin':[0,0,0],
        'authorizationFrozen':{'centerFeet':[2.5,0,3],'capturedApplications':['castF2']}}
    s['supplement']['spellEvents'].append({'castId':'greaterDispelW2','caster':'A','spell':'greater-dispel',
        'rank':5,'timeSeconds':172800.5,'costRP':10,'action':'Action','centerFeet':[2.5,0,3],
        'targetEffect':'castF2','immutableCapturedApplications':['castF2'],'check':check})
    s['supplement']['imprintEndings'].append({'rootId':'castF2','physicalItemId':'bracelet-1','eventId':'greaterDispelW2',
        'timeSeconds':172800.5,'procedure':'AC5:/spells/2/procedure; castF2 application scope /0/spellLocalNEW/permanence and /dispel','reason':'actual-successful-dispel',
        'physicalBodyPreserved':True,'owner':'A','custodian':it['custodian'],'HP':it['HP'],'charges':it['charges']})
event('MF247-F-W2-E20-PAID-GREATER-DISPEL','paid-Greater-Dispel-ends-castF2',172800.5,
    'A spends 10 RP and one Action on prepared Greater Dispel. Its unsuppressed 30-foot capture contains only the perceived Until-dispelled castF2 application; the actual check 17+INT 5+PB 6=28 meets DC28. Only the imprint ends.',greater_dispel)

def b_next_turn(s):
    b=s['actors']['B']; b.update({'regularStart':172806.2,'nextRegularStart':172812.2,
        'regularStartsProcessed':b['regularStartsProcessed']+[172806.2],'Action':1,'Reaction':1,'BonusAction':1,
        'freeInteraction':1,'movementRemaining':30,'turnCast':False})
event('MF247-F-W2-E21-B-NEXT-TURN','regular-turn-start-no-action',172806.2,
    'B receives the next regular turn; no action or item interaction occurs before A’s next slot.',b_next_turn)

def a_next_turn(s):
    a=s['actors']['A']; a.update({'regularStart':172806.4,'nextRegularStart':172812.4,
        'regularStartsProcessed':a['regularStartsProcessed']+[172806.4],'Action':1,'Reaction':1,'BonusAction':1,
        'freeInteraction':1,'movementRemaining':30,'turnCast':False})
event('MF247-F-W2-E22-A-NEXT-TURN','regular-turn-start-and-recharge-tick',172806.4,
    'A receives a new Action next round; no unspent class Dispel Magic recharge is part of this trace.',a_next_turn)

def second_forge(s):
    a=s['actors']['A']; assert a['Action']==1 and a['RP']==39 and not s['items']['bracelet-1']['imprintRoot']['active']
    assert a['hands']['left']=='focus' and a['hands']['right']=='dagger'
    a['freeInteraction']=0; a['hands']['right']=None
    for x in a['profile']['inventory']:
        if x['id']=='dagger': x['custody']='belt'
    a['Action']=0; a['RP']-=26; a['lastSpell']='eternal-forge'; a['Dissonance']=0
    a['usedPreparedFamilies'].append('eternal-forge')
    a['resourceHistory'].append({'castId':'castF3','spell':'eternal-forge','time':172806.5,'cost':26,
        'action':'Action','firstFamily':True,'baseDissonance':0,'RefrainAdded':0})
    s['terminalCasts']['castF3']={'caster':'A','spell':'eternal-forge','rank':9,'paidRP':26,'paidAction':'Action',
        'components':'V/S/F','status':'resolved','origin':[0,0,0],
        'authorizationFrozen':{'profile':'recipe-241','quantity':1,'complete':True}}
    s['items']['bracelet-2']={'id':'bracelet-2','revision':1,'owner':'A','custodian':'A-floor-within-5ft',
        'model':'jewelcrafting.bracelet','recipe':'recipe-241','massLb':{'n':1,'d':10},'AC':19,'maxHP':5,'HP':5,
        'damageDeficit':0,'charges':1,'maximumCharges':1,'processedDawns':[],'complete':True,'worn':False,'melded':False,
        'imprintRoot':{'id':'castF3','rank':9,'active':True,'suppressed':False},'referenceGP':{'n':166,'d':3},
        'provenance':['castF3'],'reservedBy':None,'positionBoxFeet':[0,3,0],
        'geometryAuthorship':'new local output placement within F02 recipe-241 fixture envelope'}
    s['supplement']['spellEvents'].append({'castId':'castF3','caster':'A','spell':'eternal-forge','rank':9,
        'timeSeconds':172806.5,'costRP':26,'action':'Action','handUse':'focus in left hand; dagger stowed with free interaction',
        'authorization':{'profile':'recipe-241','quantity':1,'complete':True},'newItemId':'bracelet-2','newRootId':'castF3'})
    s['supplement']['newCreations'].append({'itemId':'bracelet-2','rootId':'castF3','createdBy':'A','createdAtSeconds':172806.5,
        'chargesInitializedOnce':True,'initialCharges':1,'oldItemUnaffected':'bracelet-1'})
event('MF247-F-W2-E23-SECOND-PAID-FORGE','distinct-paid-Eternal-Forge-creation',172806.5,
    'A stows the dagger with a free interaction, then spends one Action and 26 RP on a separately paid Eternal Forge cast, creating bracelet-2/castF3 with one initial charge.',second_forge)

def close_final(s):
    s['supplement']['initiativeEpisodes'][-1]['endSeconds']=172806.6
    s['supplement']['initiativeEpisodes'][-1]['closedNormally']=True
    s['supplement']['currentEncounter']=None
    s['supplement']['status']='W2_TRACE_BUILT_PENDING_DIRECTOR_REVIEW'
event('MF247-F-W2-E24-CLOSE','close-final-encounter',172806.6,
    'Close the final encounter without additional actions; preserve both physical item and root histories.',close_final)

expected={'timeSeconds':state['time'],'actorARP':state['actors']['A']['RP'],'actorBRP':state['actors']['B']['RP'],
    'bracelet1':{'id':'bracelet-1','owner':'A','custodian':'B-right-wrist','HP':2,'charges':0,'maximumCharges':1,
        'processedDawns':['MF210-W2-CLOCK-01:jewelcrafting-dawn:1','MF210-W2-CLOCK-01:jewelcrafting-dawn:2'],
        'root':'castF2','rootActive':False,'endReason':'actual-successful-dispel'},
    'bracelet2':{'id':'bracelet-2','owner':'A','custodian':'A-floor-within-5ft','HP':5,'charges':1,'root':'castF3','rootActive':True}}
branch={'id':'MF247-F-W2-SUPPRESSED-DAWN-NO-CATCHUP','description':'Integrated continuation from MF210-F02:6 through transfer, lifecycle, removal and distinct paid creation.',
    'baseStateSHA256':sha(base),'events':events,'finalStateSHA256':sha(state),'expectedFinal':expected}

bindings=[zip_binding('cases/MF210-F02.json'),zip_binding('cases/MF210-F-greater-dispel.json'),
    zip_binding('PROCEDURES.json'),zip_binding('SOURCE_BINDINGS.json'),
    local_binding('DescentReviewChanges/ReviewBible/docs/mechanics/JEWELCRAFTING_RECIPE_PLAYTEST.md'),
    local_binding('DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md'),
    local_binding('DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md'),
    local_binding('DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md'),
    local_binding('DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md'),
    local_binding('DescentReviewChanges/ReviewBible/data/public/class_playtests/wizard.json'),
    local_binding('DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json'),
    local_binding('DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_01.json'),
    local_binding('docs/audit/2026-10-08/full-game/director-spell-review-129/ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_253.json')]

packet={'id':'ETERNAL-FORGE-MF210-B01-WITNESS-SUPPLEMENT-254','recordedAtUtc':'2026-10-30T00:00:00Z',
    'status':'DRAFT_WITH_FORWARD_INVERSE_REPLAY_AND_LOCAL_CONSISTENCY_AUDIT_DIRECTOR_REVIEW_REQUIRED',
    'authority':{'reviewedApplied':811,'pending':37,'acceptedUnapplied':0},
    'sourceDecision':{'destination':'GPT director - Calibration review part 6',
        'status':'MF247-F-W1_COMPLETE_COMPONENT_WITNESS; MF247-F-W2_OPEN',
    'summary':'This is a noncanonical lifecycle continuation from exact MF210-F02:6. Per the director ruling, prepared Greater Dispel targets the separately maintained rank-9 Until-dispelled Forge application castF2, while preserving the permanent physical bracelet and its full lifecycle ledger.'},
    'componentW1':{'id':'MF247-F-W1','status':'COMPLETE_COMPONENT_WITNESS','packet':'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_253.json',
        'sha256':file_sha(HERE/'ETERNAL_FORGE_MF210_B01_WITNESS_SUPPLEMENT_253.json')},
    'priorCase':{'caseId':'MF210-F02','endEventId':'MF210-F02:6','timeSeconds':12.1,'endSnapshotSHA256':sha(base),
        'sourceArchive':{'path':ARCHIVE.relative_to(REPO).as_posix(),'bytes':ARCHIVE.stat().st_size,'sha256':file_sha(ARCHIVE)},
        'sourceMember':'cases/MF210-F02.json','endState':base,
        'endpoint':{'item':'bracelet-1','recipe':'recipe-241','root':'castF2','HP':5,'charges':'0/1','wornBy':'A','owner':'A','custodian':'A-wrist','actorA_RP':38}},
    'witnessCases':[{'id':branch['id'],'status':'local integrated W2 branch pending GPT review',
        'timeline':{'fromSeconds':12.1,'toSeconds':state['time'],'fixedEpochD0Seconds':0,'dawns':[86400,172800]},
        'eventIds':[e['id'] for e in events],'summary':'Transfer and don preserve charge 0; dawn 1 is ineligible under Lesser Antimagic and is not replayed; the resumed positive-HP bracelet is Sunder-damaged, refills once at dawn 2, spends that charge on a real Hide check, loses only castF2 to paid Greater Dispel, and remains physically present while a separate paid cast creates bracelet-2/castF3.'}],
    'sourceBindings':bindings,'acceptedIds':[],'appliedIds':[],'canonicalChanges':False,'applicationChanges':False,'githubChanges':False,
    'eventReplay':{'method':'Reversible JSON-Patch event stream from exact MF210-F02:6 state; each event has before/after SHA-256 and inverse operations.',
        'baseStateSHA256':sha(base),'branches':[branch]},
    'remainingForDirector':['Review the exact Greater Dispel envelope, one-hour Retune record, noncasting receiver fixture, integrated timeline, and forward/inverse replay.',
        'If W2 meets all requirements, mark the integrated Eternal Forge witness complete and accept Eternal Forge / MF210-B01; otherwise list exact remaining corrections.',
        'After adjudicating Eternal Forge, identify the remaining pending identities and authority counts, with exact IDs.']}
OUT.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
audit={'id':'ETERNAL-FORGE-MF210-B01-SUPPLEMENT-254-INDEPENDENT-AUDIT',
    'status':'BUILT_PENDING_STANDALONE_VERIFIER_AND_GPT_DIRECTOR_REVIEW','packetPath':OUT.relative_to(REPO).as_posix(),
    'packetBytes':OUT.stat().st_size,'packetSHA256':file_sha(OUT),'sourceBaseSHA256':sha(base),'eventCount':len(events),
    'forwardOperationCount':sum(len(e['forward']) for e in events),'inverseOperationCount':sum(len(e['inverse']) for e in events),
    'finalStateSHA256':sha(state),'sourceBindings':bindings,
    'checksPending':['standalone forward/inverse replay','source hash reproduction','resource/charge/identity assertions','GPT semantic review'],
    'canonicalChanges':False,'applicationChanges':False,'authority':packet['authority']}
AUDIT.write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'packetBytes':OUT.stat().st_size,'packetSHA256':file_sha(OUT),'events':len(events),
    'forwardOps':audit['forwardOperationCount'],'inverseOps':audit['inverseOperationCount'],'finalStateSHA256':sha(state)},indent=2))
