# Frozen, source-bound builder for the Unravel Identity integration witness.
import json, pathlib, hashlib, zlib, copy, zipfile
W=pathlib.Path(r'C:\Github\DecenniumDescent-review-push-134')
B=W/'docs/audit/2026-10-08/full-game/director-spell-review-129'
Z241=B/'rank9_memorydenial6_current_source_241_prepared/DD_Rank9_MemoryDenial6_CurrentSource_241.zip'
ZRET=B/'rank9_memorydenial6_return241_received/DD_Rank9_MemoryDenial2_Director_Return241_HELD.zip'
def binding(path, raw):
    return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}'}
def local(rel):
    return binding(rel,(W/rel).read_bytes())
p251=json.loads((B/'UNRAVEL_IDENTITY_MD196_B02_WITNESS_PLAN_251.json').read_text(encoding='utf-8'))
pending=json.loads((B/'CURRENT36_PENDING_IDENTITY_AUDIT_250.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(Z241) as z:
    names={
      'druidClass':'data/public/class_playtests/druid.json',
      'mageClass':'data/public/class_playtests/mage.json',
      'wizardClass':'data/public/class_playtests/wizard.json',
      'formTempHP':'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md',
      'creatureLifecycle':'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md',
      'maximumHP':'docs/mechanics/MAXIMUM_HP_PLAYTEST.md',
      'bodyEquipment':'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',
      'characterCreation':'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
      'resonanceCanon':'docs/mechanics/RESONANCE_CANON.md',
      'spellIntegration':'docs/mechanics/SPELL_INTEGRATION_RULES.md',
      'catalog':'data/public/spell_playtests/catalog.json'}
    members={}
    for k,tail in names.items():
        hits=[n for n in z.namelist() if n.endswith(tail)]
        if len(hits)>1: hits=[n for n in hits if n.startswith('sources_current/')]
        if len(hits)!=1: raise RuntimeError(f'{k} member lookup has {len(hits)} hits for {tail}')
        members[k]=hits[0]
    sources={k:binding(v,z.read(members[k])) for k,v in members.items()}
    catalog=json.loads(z.read(members['catalog']).decode('utf-8'))
with zipfile.ZipFile(ZRET) as z:
    actorTemplate=binding('prior/ACTOR_PROFILES.json',z.read('prior/ACTOR_PROFILES.json'))
catalogPath='DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'
if local(catalogPath)['sha256']!=sources['catalog']['sha256']:
    raise RuntimeError('Current catalog differs from Packet241 bytes')
formReg=local('DescentReviewChanges/ReviewBible/data/playtest/druid_form_profiles.json')
S={x['id']:x for x in catalog['spells']}
def spell(sid,cls):
    s=S[sid]; a=s['classAccess'][cls]
    return {'id':sid,'name':s['name'],'class':cls,'rank':a['rank'],'minimumClassLevel':a['minimumClassLevel'],'baseRPCost':a['baseRpCost'],'catalogStatus':s['status'],'operationalEntryAvailable':bool(s.get('operational'))}
druidCantrips=['druidcraft','shape-water','mold-earth','gust']
druidPrepared=['shield','elemental-resistance','sanctuary','detect-poison','warding-bond','summon-fire-pet','burning-sands','elemental-bolt','protection-from-energy','summon-air-pet','resonance-well','conjure-shield-of-sparks','magic-circle','remove-curse','elemental-displacement','water-breathing','death-ward','polymorph','resurrection','mass-resurrection-denial']
wizardPrepared=['shield','protective-sphere','alarm-ward','elemental-resistance','sanctuary','detect-magic','binding-circle','purify-food-and-drink','arcane-lock','dispel-magic-lesser','protection-from-energy','barrier-of-faith','magic-circle','barrier-field','remove-curse','protection-from-scrying','resonance-anchor','alignment-sanctuary','speak-with-dead','slow','mind-blank','unravel-identity']
dc=[spell(s,'Druid') for s in druidCantrips]
dp=[spell(s,'Druid') for s in druidPrepared]
wp=[spell(s,'Wizard') for s in wizardPrepared]
for s in dc:
    if s['rank']!=0 or not s['operationalEntryAvailable']: raise RuntimeError(f'Invalid Druid cantrip: {s}')
for s in dp:
    if s['rank']>8 or s['minimumClassLevel']>15 or not s['operationalEntryAvailable']: raise RuntimeError(f'Invalid Druid prepared spell: {s}')
for s in wp:
    if s['minimumClassLevel']>17 or s['rank']>9: raise RuntimeError(f'Invalid Wizard prepared spell: {s}')
levels={1:6,2:2,3:2,4:2,5:3,6:3,7:3,8:3,9:4,10:4,11:4,12:4,13:5,14:5,15:5,16:5,17:6}
maxrank={1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4,9:5,10:5,11:6,12:6,13:7,14:7,15:8,16:8,17:9}
adds={1:['shield','protective-sphere','alarm-ward','elemental-resistance','sanctuary','dispel-resonance'],
2:['binding-circle','purify-food-and-drink'],3:['arcane-lock','dispel-magic-lesser'],4:['protection-from-energy','barrier-of-faith'],
5:['magic-circle','barrier-field','remove-curse'],6:['protection-from-scrying','resonance-anchor','alignment-sanctuary'],
7:['speak-with-dead','slow','water-breathing'],8:['summon-earth-pet','conjure-elemental-lance','burst-of-flamewind'],
15:['mind-blank'],17:['unravel-identity']}
school='mirror-image'; used={school}
for lv,ids in adds.items():
    for sid in ids:
        if sid in used: raise RuntimeError(f'duplicate spellbook member {sid}')
        used.add(sid)
fillers=[]
for s in catalog['spells']:
    a=s.get('classAccess',{}).get('Wizard')
    if a and a.get('rank',0)>0 and s.get('status')=='operational-playtest-draft' and s.get('operational'):
        fillers.append((a['rank'],s['id'],a['minimumClassLevel']))
fillers.sort()
for lv,count in levels.items():
    if len(adds.get(lv,[]))>count: raise RuntimeError(f'overfull book level {lv}')
    adds.setdefault(lv,[])
    while len(adds[lv])<count:
        poss=[(r,sid,m) for r,sid,m in fillers if r<=maxrank[lv] and m<=lv and sid not in used]
        if not poss: raise RuntimeError(f'no legal book fill at Wizard {lv}')
        _,sid,_=poss[0]; adds[lv].append(sid); used.add(sid)
book=[]
for lv,ids in adds.items():
    for sid in ids: book.append({'id':sid,'acquiredAtWizardLevel':lv,**spell(sid,'Wizard')})
schoolBonus={'id':school,'acquiredAtWizardLevel':1,'acquisition':'Illusion School bonus, additional to six starting spells',**spell(school,'Wizard')}
schoolBonusRecord=schoolBonus
if len(book)!=66 or len(book)+1!=67: raise RuntimeError(f'book count error {len(book)}')
# Detailed dependency rows enumerate all current Druid/Mage acquired capabilities/cards.
druidFeatures=[
('druid.base.druidic',1,'language/class feature','Unavailable while class-loss is active; acquired record remains.'),
('druid.base.spellcasting',1,'class engine','Druid prepared spells/casting unavailable; Druid RP contribution and levels stay fixed.'),
('druid.base.shapeshifting',1,'class engine','Unavailable; active form ends exactly once through proposed UI251-FORM-LOSS.'),
('druid.base.wolf-form-striker; druid.base.bear-form-tank; druid.base.hawk-form-scout; druid.base.boar-form-brawler; druid.base.panther-form-stealth',1,'five automatic Base forms','Unavailable; none active; no separate HP pools.'),
('druid.base.moon.combat-shapeshifting',2,'Moon Base feature','Unavailable; no active rider.'),
('druid.base.moon.circle-forms',2,'Moon Base feature','Unavailable; forms/attunements remain recorded, no new use.'),
('druid.arch.moon.primal-strike',6,'Moon Arch feature','Unavailable; no current attack rider.'),
('druid.hero.moon.beastlord-alpha-animal-hybrid; druid.hero.moon.mooncursed',10,'Moon Hero forms','Unavailable; neither is active.'),
('druid.arch.earth-warden-dire-bear; druid.arch.dire-wolf',11,'two forms attuned at long rest','Unavailable; Earth Warden ends; Dire Wolf remains an inactive acquisition.'),
('druid.hero.moon.elemental-shapeshifting',14,'Moon Hero feature; choose Earth','Unavailable; Earth option remains recorded, no use spent.'),
('Druid spell matrix and four cantrips',15,'20 prepared ranked spells, max rank8; four cantrips','Unavailable; no Druid spell used in this history.')
]
mageFeatures=[
('mage.base.spellcasting',1,'automatic engine','Mage casts unavailable during class loss; own14 RP contributes fixed4 to shared max46.'),
('mage.base.resonance-pool',1,'automatic shared-pool access','Ledger unavailable for Mage feature use; shared RP41/46 remains unchanged.'),
('mage.base.resonance-surge',1,'automatic 1/short rest','Unavailable; unspent use stays unspent.'),
('mage.base.fire.fire',2,'automatic Fire Focus','Unavailable; familiar’s creation-fixed identity/resistance is unaffected.'),
('mage.base.arcane-missile; mage.base.resonance-shield; mage.base.blink; mage.base.spell-precision',1,'four selected Base cards','Unavailable; no active effect.'),
('mage.base.elemental-affinity; mage.base.elemental-bolt',2,'two selected Base cards','Unavailable; no current rider.'),
('mage.arch.arcane-stability; mage.arch.elemental-surge',3,'two selected Arch cards','Unavailable; no active effect.'),
('mage.base.detect-magic',4,'selected concentration spell','Class maintenance is lost; DM-01 ends once at Unravel admission, no reactivation.'),
('mage.arch.conjure-elemental-familiar',5,'selected 1/LR class spell','Owner command is removed; same Fire familiar/HP/deadline persists; 4RP and spent use remain spent.')
]
def rows(items,cls):
    result=[]
    for ident,lv,kind,loss in items:
        result.append({'sourceId':ident,'class':cls,'classLevel':lv,'kind':kind,'duringUnravel':loss,'recovery':'Availability only; no restoration of ended effect or spent resource.'})
    return result
Ttarget={'id':'MD196-TARGET-HUMAN-DRUID15-MAGE5','qualification':'conditional static actor fixture, not campaign evidence','classLevels':{'Druid':15,'Mage':5},'levelSequence':[{'characterLevel':1,'class':'Druid','classLevel':1}]+[{'characterLevel':i,'class':'Mage','classLevel':i-1} for i in range(2,7)]+[{'characterLevel':i,'class':'Druid','classLevel':i-5} for i in range(7,21)],'entryAtCharacter2':{'INT':16,'WIS':14,'gates':'Mage INT13; Druid WIS13; both pass'},'finalScores':{'STR':10,'DEX':14,'CON':14,'INT':18,'WIS':20,'CHA':10},'ASIs':[{'characterLevel':5,'class':'Mage','classLevel':4,'choice':'INT+2'},{'characterLevel':9,'class':'Druid','classLevel':4,'choice':'WIS+2'},{'characterLevel':13,'class':'Druid','classLevel':8,'choice':'WIS+2'},{'characterLevel':17,'class':'Druid','classLevel':12,'choice':'WIS+2'}],'skills':{'Druid':['Nature','Perception'],'Mage entry':['Investigation'],'Human':['History'],'Nomadic Human':['Survival'],'City Guard Veteran':['Athletics','Insight']},'repertoire':{'druidCantrips':dc,'druidPrepared':dp,'druidPreparedCount':20,'druidPreparationCapacity':'Druid15 + WIS mod5 =20','druidMaxRank':8,'mageAutomatic':['mage.base.spellcasting','mage.base.resonance-pool','mage.base.resonance-surge'],'mageFocus':'Fire at Mage2, mage.base.fire.fire','mageSelected':['mage.base.arcane-missile','mage.base.resonance-shield','mage.base.blink','mage.base.spell-precision','mage.base.elemental-affinity','mage.base.elemental-bolt','mage.arch.arcane-stability','mage.arch.elemental-surge','mage.base.detect-magic','mage.arch.conjure-elemental-familiar'],'mageMaxRank':3,'mageOwnRP':14},'resources':{'PB':6,'HP':'138/138','sharedRP':'46/46','Dissonance':'0/12','DruidShifts':'6/6','Buffer':'35/35','FormSurge':'6/6','ElementalShapeshifting':'2/2','Familiar':'ready 1/LR'},'equipment':{'startingChoice':'Druid wealth; fixed roll2d4=8=80gp','items':[{'name':'wooden Druidic focus staff','qty':1,'cost':'5gp','weight':'4lb','custody':'right hand at root anatomy'},{'name':'common clothes','qty':1,'cost':'5sp','weight':'3lb','custody':'worn'}],'remainingCoin':'74gp 5sp','armor':'none','shield':'none','weapons':'none','rootAC':12,'EarthWardenAC':12,'meld':'staff/clothes inaccessible while melded; ownership unchanged; same items return at form end'}}
# Wizard actor: class sources and card progression; spells learned at exact legal levels.
wizCards=[
{'level':1,'ids':['wizard.base.arcane-recovery','wizard.base.arcane-insight','wizard.base.arcane-bolt','wizard.base.arcane-shield']},
{'level':2,'ids':['wizard.base.analyze-magic','wizard.base.spellbook-study']},
{'level':3,'ids':['wizard.arch.floating-preparation','wizard.arch.arcane-lock']},
{'level':4,'ids':['wizard.base.matrix-efficiency'],'ASI':'INT+2'},
{'level':5,'ids':['wizard.arch.dispel-magic']},
{'level':6,'ids':['wizard.arch.sigil-rewrite']},
{'level':7,'ids':['wizard.arch.spell-efficiency']},
{'level':8,'ids':['wizard.arch.improved-concentration'],'ASI':'INT+2'},
{'level':9,'ids':['wizard.arch.arcane-sight']},
{'level':10,'heroPath':'Spellbinder','ids':['wizard.hero.spellbinder.sigil-authority','wizard.hero.spellbinder.seal-magic']},
{'level':11,'ids':['wizard.arch.dimensional-pocket']},
{'level':12,'ids':['wizard.hero.spellbinder.knowledge-shield'],'ASI':'WIS+2'},
{'level':13,'ids':['wizard.arch.spell-tether']},
{'level':14,'ids':['wizard.hero.spellbinder.matrix-sharing']},
{'level':15,'ids':['wizard.base.spell-scribing']},
{'level':16,'ids':['wizard.hero.spellbinder.arcane-memory'],'ASI':'CHA+2'},
{'level':17,'ids':['wizard.base.minor-conjuration']}]
wizSpellbook=[]
for lv,ids in adds.items():
    for sid in ids: wizSpellbook.append({'id':sid,'level':lv,'rank':spell(sid,'Wizard')['rank']})
wizSpellbook.append({'id':school,'level':1,'rank':spell(school,'Wizard')['rank'],'reason':'Illusion specialization bonus'})
# Cast history includes two independent rank9/response fixtures and one remover.
events=[
{'event':'LONG-REST','time':'2026-10-30T10:00:00Z','after':{'HP':'138/138','RP':'46/46','Dissonance':'0/12','shifts':'6/6','buffer':'35/35','formSurge':'6/6','elementalUses':'2/2','concentration':None,'familiarUse':'ready'}},
{'event':'CAST-FIRE-FAMILIAR','time':'2026-10-30T10:01:00Z','action':'separate Mage Action; pay4RP; rank3 adds1 Dissonance; spend1/LR','after':{'RP':'42/46','Dissonance':'1/12','Familiar':'FAM-FIRE-01,14/14,AC18,Speed30,Fire resistance,expires 10:11:00Z','pendingCommand':None}},
{'event':'CAST-DETECT-MAGIC','time':'2026-10-30T10:02:00Z','action':'separate Mage Action; pay1RP; rank1 adds1 Dissonance; start concentration up to10min','after':{'RP':'41/46','Dissonance':'2/12','Refrain':'different spell breaks Refrain','NukeChain':'empty','concentration':'DM-01 ends no later than10:12:00Z'}},
{'event':'SHIFT-EARTH-WARDEN','time':'2026-10-30T10:03:03Z','action':'target regular turn N-1 Bonus Action; spend1 shift; clear remembered Refrain, not Dissonance','after':{'HP':'138/138','RP':'41/46','Dissonance':'2/12','shift':'5/6','buffer':'5/35','tempHP':'30 tied to FORM-EW-01','formDeadline':'10:13:03Z','AC':12,'formResistance':'nonmagical physical','naturalAttack':'PB+WIS,1d8+WIS slashing','canSpeak':True,'canCastSpells':False,'equipment':'staff/clothes melded'}},
{'event':'PREVIOUS-TARGET-END','time':'2026-10-30T10:03:06Z','action':'turn N-1 ends before the Unravel round; no idle-turn recovery asserted'},
{'event':'ADMIT-UNRAVEL','time':'2026-10-30T10:03:12Z','action':'separate Wizard17 Action,120ft,V/S/F; pay26RP; first distinct Wizard matrix family, no base Dissonance; automatic, no save, no concentration; persona: “I am Rowan Vale, a traveling herbalist.”','after':{'WizardCasterRP':'38/64','WizardDissonance':'0/13','TargetClassFeatures':'unavailable for one round','TargetFalseSelf':'active until first future target regular END','TargetIdentity':'unchanged','TargetHP':'138/138','TargetRP':'41/46','TargetDissonance':'2/12','form':'ended at admission under NEW UI251-FORM-LOSS; remove30 tempHP/resistance/attacks; root anatomy returned','concentration':'DM-01 ended terminally','familiar':'same FAM-FIRE-01,14/14,original10:11 deadline; owner command removed, no queued order','targetNextTurn':'not started; expiry is its next regular END'}},
{'event':'TARGET-TURN-START','time':'2026-10-30T10:03:14Z','action':'first target regular turn under Unravel; use ordinary Dodge, no spell/Weave ability. Familiar has no order, defensive movement/Dodge; no damage/control.'}
]
forks=[
{'id':'NATURAL-EXPIRY','actors':'shared target and Unravel caster','events':[{'event':'LET-THE-NOTE-FALL','time':'10:03:18Z','phase':'regular END cadence before expiry','effect':'Target used no spell/Weave; Dissonance2→1. RP and all resource ledgers unchanged.'},{'event':'UI-NATURAL-END','time':'10:03:18Z','phase':'first future target regular END','effect':'End class-loss and belief; restore capability availability only. Do not restore form/tempHP/resistance/natural attacks/DM or spent budgets. Familiar remains same and original deadline10:11:00Z.'}]},
{'id':'MINDBLANK-SUPPRESSION','separateActor':'Wizard17, rank8 Mind Blank in acquired spellbook and prepared set, initial RP64; cast Action/21RP/V-S-F at10:03:13Z after Unravel and before target turn. Result RP43/64; first distinct family Dissonance0.','events':[{'event':'MIND-BLANK-SUPPRESSES','time':'10:03:13Z','effect':'suppress both components while Mind Blank source effect is present; UI clock continues to original10:03:18Z and is not extended; ended form/DM are not recreated.'},{'event':'TARGET-TURN','time':'10:03:14Z','effect':'class availability resumes under suppression; target chooses ordinary Dodge/no spell; familiar continues defensive Dodge.'},{'event':'LET-THE-NOTE-FALL-AND-UI-EXPIRY','time':'10:03:18Z','effect':'Dissonance2→1; end original UI records at first future target END.'}],'qualification':'Mind Blank source is bound but its catalog duration field says Instantaneous; no temporary duration is invented. Director must confirm that the source effect record persists across this interval; otherwise this fork stays held.'},
{'id':'ARCH-DISPEL-REMOVAL','separateActor':'Wizard17 with wizard.arch.dispel-magic acquired at W5; pre-cast prepared Detect Magic at2RP, active concentration and perceivable aura; current RP62/64. After Unravel, Action/3RP at60ft; check d20 roll8 + INT5 + PB6 =19 vs DC10+rank9=19; success; RP59/64; Dispel recharge2.','events':[{'event':'ARCH-DISPEL-ENDS-UI','time':'10:03:13Z','effect':'end only the selected Unravel instance before target turn; restore class availability and end belief. Form/tempHP/resistance/natural attacks/DM remain ended; familiar source persists and command availability returns with no order.'},{'event':'TARGET-TURN-AND-LET-THE-NOTE-FALL','time':'10:03:14Z-10:03:18Z','effect':'target takes ordinary Dodge/no spell/Weave; Dissonance2→1 at end; no other budgets reset.'}],'qualification':'No Greater Dispel, no extra attempt, no refund. Perceivability relies on the exact observed Unravel instance and the remover’s already active Detect Magic aura; director to confirm.'}
]
# A structured plan derived from the already audited 251 plan, preserving authority while replacing incomplete witness content.
plan=copy.deepcopy(p251)
plan.update({'id':'UNRAVEL-IDENTITY-MD196-B02-INTEGRATED-WITNESS-252','recordedAtUtc':'2026-10-30T11:53:45+00:00','status':'INTEGRATED_SOURCE_BOUND_WITNESS_PREPARED_FOR_GPT_DIRECTOR_RECHECK','accepted':False,'applied':False})
plan['sourceAuthority']['supplementalLocalFormRegister']=formReg|{'status':'SUPPLEMENTAL_SOURCE_BOUND_FOR_THIS_WITNESS_NOT_PACKET241','relationship':'Earth Warden profile required by the Druid form overlay; does not itself establish class-loss callback.'}
plan['sourceAuthority']['packet241MemberBindings']=sources
plan['sourceAuthority']['return241ActorTemplate']=actorTemplate|{'use':'Origin template only; Wizard-specific equipment/capabilities are not inherited by target.'}
plan['qualifiedActors']={'target':Ttarget,'unravelCaster':{'id':'WITNESS-UNRAVEL-WIZARD17','qualification':'separate conditional Human Wizard17 Illusion caster; no target gear inherited','scores':{'STR':10,'DEX':14,'CON':14,'INT':20,'WIS':14,'CHA':13},'pointBuySpent':25,'ASIs':[{'level':4,'INT':'+2'},{'level':8,'INT':'+2'},{'level':12,'WIS':'+2'},{'level':16,'CHA':'+2'}],'school':'Illusion; spell attack12, spell save DC20, Dissonance limit13','selectedCards':wizCards,'automaticFeatures':['Arcane School Specialization','Spell Matrix System','Counterspell','Ritual Casting','Arcane Tradition: Illusion','School Mastery','Arcane Ward','Dual Cast','Overchannel','Arcane Feedback','Tethered Cast'],'spellbook':{'startingSix':adds[1],'schoolBonus':schoolBonusRecord,'levelUpAcquisitionSchedule':levels,'allLearnedEntries':wizSpellbook,'count':67},'preparedMatrices':wp,'preparedCount':22,'preparation':'Wizard17+INT modifier5=22; Matrix Efficiency acquired at W4 lowers study to45 minutes. Includes Mind Blank W15 and Unravel Identity W17.','maxRank':9,'PB':6,'RPMax':64,'HP':'104/104','hands':'Illusion focus left hand; right hand free; spellbook in satchel; no armor/weapon; AC12','archDispel':'wizard.arch.dispel-magic selected at W5; separate class card, not a prepared matrix.'},'mindBlankSuppressor':'Separate conditional Wizard17 fixture with Mind Blank prepared; 64RP before cast, pay21RP.','archDispelRemover':'Separate conditional Wizard17 fixture with W5 Arch Dispel and prepared Detect Magic; cast Detect Magic first for2RP, then Arch Dispel3RP.'}
plan['dependencyCallbackPlan']=rows(druidFeatures,'Druid')+rows(mageFeatures,'Mage')+[
{'source':'Human + Nomadic Human','duringUnravel':'Human +1 all scores, Common/Draconic, History and Nomadic Survival remain as independent ancestry/background records.','recovery':'none.'},
{'source':'Aethel City Guard Veteran background','duringUnravel':'Athletics, Insight, background feature and mundane training remain.','recovery':'none.'},
{'source':'Character-level ASIs','duringUnravel':'Mage4 INT at char5; Druid4/8/12 WIS at char9/13/17 remain; levels, HP/RP tables and PB are not reduced.','recovery':'none.'},
{'source':'Class-granted proficiencies','duringUnravel':'Nature/Perception from Druid, Investigation from Mage entry, and class saves/tool training remain recorded. No such check is used. Whether training is treated as a current class ability is explicitly for director confirmation.','recovery':'Do not infer loss or grant any bonus without ruling.'},
{'source':'Mundane functions/equipment/identity','duringUnravel':'Ordinary movement/speech as anatomy permits, mundane actions, coin/ownership, personal memory and objective identity remain. Equipment returns from form meld under existing procedure.','recovery':'none.'},
{'source':'NEW UI251-FORM-LOSS (spell-local only)','duringUnravel':'On successful admission only, end current Earth Warden form once; remove bound tempHP30, resistance/natural attacks and all form benefits; return root body and same equipment. Countered/admission-blocked Unravel does nothing.','recovery':'Class availability only; never recreate form, buffer, tempHP or Detect Magic. No global Druid/antimagic rule is asserted. Preserve HP138, RP41/46, shifts5/6, reserve5/35, Form Surge6/6, elemental uses2/2.'},
{'source':'Conjure Elemental Familiar + CREATURE_LIFECYCLE_PLAYTEST “At the table”','duringUnravel':'Same Fire familiar 14/14 AC18 with fixed resistance and original10:11 deadline persists; remove owner command permission, with no pending order. It defensively moves/Dodges; no damage/control.','recovery':'Owner permission returns only; same companion continues, no HP/time/use/order reset.'},
{'source':'Unravel Identity subjective-self component','duringUnravel':'Autonomous belief in “I am Rowan Vale, a traveling herbalist.” No forced behavior/allegiance, new skill/language/equipment, body or objective identity change.','recovery':'Belief ends with original one-round record; original memory and identity retained.'}]
plan['commonPrehistory']=events
plan['coverageAndReversibleEvidencePlan']={'commonHistory':'Exact time-stamped long-rest ledgers, separate paid Mage Actions, paid Bonus Action shift after casts, Refrain/Dissonance/Nuke Chain, familiar lifecycle, concentration and separate qualified Wizard17 Unravel casting. No spell cast while shifted; no invented rest/refill.','timeline':'Unravel admitted at10:03:12Z after target prior regular END10:03:06Z; target next START10:03:14Z and first future regular END10:03:18Z.','forks':forks,'stateAccounting':'At affected target END, Let the Note Fall removes1 Dissonance (2→1) because the target used no spell or Weave ability. No other current/max resources change.','preservation':'Existing Return241 cases remain byte-identical. Full forward/inverse operation list is below; inverses are audit-only and do not imply in-world recreation/refund.','statusBoundary':'No identity accepted/applied or canonical changes; Mind Blank and Arch Dispel forks are director rechecks.'}
plan['reversibleStateOperations']=[
{'id':'OP252-01','forward':'Initialize actor, pool and reserves from long rest.','inverse':'Restore pre-long-rest fixture for static audit only.'},
{'id':'OP252-02','forward':'Pay Conjure Familiar4RP; spend 1/LR; create source clocked Fire companion.','inverse':'Remove generated companion and restore pre-cast use/RP in static audit only.'},
{'id':'OP252-03','forward':'Pay Detect Magic1RP; start DM-01.','inverse':'End DM-01 and restore pre-cast RP/concentration snapshot for static audit.'},
{'id':'OP252-04','forward':'Pay one shift/Bonus Action; consume buffer30; create FORM-EW-01.','inverse':'Restore root anatomy, shift6, buffer35, no form temp HP; audit-only.'},
{'id':'OP252-05','forward':'Commit Wizard Action/RP26 and admit UI/belief; apply UI251-FORM-LOSS; terminally end DM-01.','inverse':'Restore exact pre-admission state for data replay only; not in-world healing/recovery.'},
{'id':'OP252-06','forward':'Select exactly one Natural End, Mind Blank Suppression or Arch Dispel branch and one Let-the-Note-Fall event.','inverse':'Reverse only branch changes to shared live-Unravel state; branch casters retain their separate costs in inverse snapshots.'}]
plan['directorQuestions']=[
'Confirm Druid15/Mage5 route, prepared repertoire, purchases, HP138, RP46 and the exact target values.',
'Confirm the newly bound supplemental Earth Warden profile agrees with the bound Druid form card and form interface.',
'Confirm spell-local NEW UI251-FORM-LOSS and terminal Detect Magic ending on successful Unravel admission.',
'Confirm familiar persistence, original HP/Fire resistance/deadline, command removal and default Dodge behavior.',
'Confirm one Dissonance vent at affected target END: 2→1 after a turn with no spell or Weave ability.',
'Confirm Wizard17 spellbook/preparation/acquisition; correct maximum RP is64, not68; confirm Arch Dispel acquisition and check.',
'Does Mind Blank source effect persist across its source time window and suppress both components before original Unravel END? Its catalog duration is Instantaneous; no temporary duration was invented.',
'Does the Arch Dispel remover perceive the actual rank9 Unravel record through the active Detect Magic aura/visible casting? It pays2RP Detect Magic and3RP Arch Dispel; roll8+11=19 against DC19.',
'Identify any remaining capability/proficiency callback or exact source defect before acceptance.'
]
plan['actorRecordBoundary']='Conditional static fixture only; no authenticated campaign or executed-play claim.'
# Ensure every required element is present and save.
out=B/'UNRAVEL_IDENTITY_MD196_B02_INTEGRATED_WITNESS_252.json'
out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'crc32':f'{zlib.crc32(out.read_bytes())&0xffffffff:08x}','spellbook':len(book)+1,'preparedWizard':len(wp),'preparedDruid':len(dp),'cantrips':len(dc),'pending':len(pending['pendingIds']),'formRegister':formReg},ensure_ascii=False,indent=2))
