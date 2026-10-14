"""One-use authoring of source-qualified, explicitly partial training examples.

Expected results below are authored cases, not outputs of the prerequisite model.
No game rule or operative candidate is changed by this script.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
OUT = A/'FEAT_EXACT_01_TRAINING_PREREQUISITE_FIXTURES.json'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()}

foundation = read(R/'data/playtest/character_foundation.json')
classes = {x['class']: x for x in foundation['classes']}
ancestry = read(R/'data/playtest/ancestry_background_candidate.json')
human = next(x for x in ancestry['ancestries'] if x['id'] == 'human')
imperial = next(x for x in human['variants'] if x['id'] == 'imperial-human')
contracts = {x['id']: x for x in read(A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json')['records']}

# Each tuple is a separately authored, literal cohort specification.
# (feat, first class, preferred starting skill, class level)
PLANS = [
 ('animal_companion','Bard','Animal Handling',4), ('battlefield_tactician','Soldier',None,4),
 ('bleeding_edge','Bard',None,4), ('bowyer','Warrior',None,4),
 ('cavalry','Bard','Animal Handling',4), ('cleaving_momentum','Warrior',None,4),
 ('climb_anywhere','Bard','Athletics',4), ('cold_reader','Bard','Insight',4),
 ('crippling_strike','Bard',None,4), ('disarming_blow','Bard',None,4),
 ('disguise_expert','Bard','Deception',4), ('double_tap','Bard',None,4),
 ('field_medic','Bard','Medicine',4), ('forensic_investigator','Bard','Investigation',4),
 ('heavily_armored','Warrior',None,4), ('herbalist','Bard','Nature',4),
 ('lock_savant','Thief',None,4), ('lunge','Bard',None,4),
 ('master_tracker','Bard','Survival',4), ('medium_armor_master','Warrior',None,4),
 ('moderately_armored','Bard',None,4), ('riposte','Bard',None,4),
 ('runic_scholar','Bard','Arcana',4), ('savage_momentum','Bard',None,4),
 ('shield_expert','Paladin',None,4), ('silent_movement','Bard','Stealth',4),
 ('spell_scribe','Bard','Arcana',4), ('sure_shot','Bard',None,4),
 ('tactical_flanker','Bard',None,4), ('target_mark','Bard',None,4),
 ('trap_sense','Bard','Perception',8), ('versatile_artisan','Bard',None,4),
 ('weaponFocus','Warrior',None,4), ('weapon_mastery','Warrior',None,8),
 ('whip_control','Warrior',None,4), ('wilderness_chef','Bard','Nature',4),
 ('wilderness_walker','Bard','Survival',4), ('anatomy_lore','Bard','Nature',4),
 ('arcane_calculus','Bard','Arcana',4), ('beast_lore','Bard','Survival',4),
 ('combat_engineering','Bard','Engineering',4), ('favored_enemy_dragon','Bard','Survival',8),
 ('master_smithing','Monk',None,4), ('necrotic_affinity','Bard','Religion',4),
 ('primal_instinct','Bard','Survival',4), ('siege_savant','Bard','Engineering',4),
 ('temporal_theory','Bard','Arcana',8), ('trapsetter','Bard','Engineering',4),
]

def score(actor, ability, value):
    base = value-imperial['combinedAbilityBonuses'][ability]
    dice = next((list(d) for d in product(range(1,7), repeat=4) if sum(d)-min(d) == base), None)
    assert dice is not None, (ability, value)
    actor['abilityRolls'][ability] = dice
    actor['permanentScores'][ability] = value

def actor(first='Bard', preferred=None, level=4, avoid=(), academy=False):
    background_skills = {'Arcana','History'} if academy else {'History','Performance'}
    existing = background_skills | {'Reputation','Persuasion'}
    selected = [] if preferred is None else [preferred]
    assert not set(selected) & (existing | set(avoid))
    for name in classes[first]['skillOptions']:
        if name not in selected and name not in existing and name not in avoid:
            selected.append(name)
        if len(selected) == classes[first]['skillChoices']:
            break
    assert len(selected) == classes[first]['skillChoices']
    result = {
        'scope': 'Synthetic first-class training/ability/paid-opportunity slice; not a complete character or authenticated campaign record.',
        'ancestry':'human','variant':'imperial-human','ancestrySkillChoice':'Reputation',
        'background':'arcane-academy-dropout' if academy else 'disgraced-noble-scion',
        'backgroundDuplicateSkillChoice':None if academy else 'Performance',
        'backgroundToolChoice':None if academy else 'tools.dice-set',
        'firstClass':first,'classLevels':{first:level},'selectedClassSkills':selected,
        'classToolChoices':['tools.drum','tools.flute','tools.lute'] if first=='Bard' else ['tools.smith-s-tools'] if first=='Monk' else [],
        'abilityRolls':{},'permanentScores':{},
        'priorFeatChoices':[{'featId':'alert','classLevel':4}] if level>=8 else [],
        'targetClassOpportunity':level,
        'physicalInventory':[], 'temporaryBonuses':{}, 'situationalBonuses':{},
    }
    for key in ['STR','DEX','CON','INT','WIS','CHA']:
        score(result,key,16)
    return result

def atoms(node):
    return [node] if 'requirements' not in node else [v for child in node['requirements'] for v in atoms(child)]

cases=[]
def add(sid,label,who,expected,reason):
    cases.append({'id':sid+'/'+label,'featId':sid,'actor':deepcopy(who),
                  'expectedPrerequisite':expected,'reason':reason})

primary={}
for sid,first,skill,level in PLANS:
    who=actor(first,skill,level)
    if sid in {'weaponFocus','weapon_mastery'}:
        who['weaponChoice']='martial-melee-weapons.longsword'
    primary[sid]=deepcopy(who)
    add(sid,'source-training',who,True,'Actual first-class/ancestry/background training and permanent scores at an earned class opportunity.')
    for node in atoms(contracts[sid]['requirements']):
        if node['kind']=='permanentAbility':
            changed=deepcopy(who);score(changed,node['ability'],node['minimum']-1)
            changed['temporaryBonuses']={node['ability']:20}
            add(sid,'below-'+node['ability'],changed,False,'Temporary ability increases cannot repair a deficient permanent prerequisite.')
        if node['kind']=='totalCharacterLevel' and sid!='necrotic_affinity':
            changed=deepcopy(who);changed['classLevels'][first]=4;changed['priorFeatChoices']=[];changed['targetClassOpportunity']=4
            add(sid,'before-required-level',changed,False,'A real class-four choice does not waive the printed total-level requirement.')

# Independently authored missing-training examples, with complete legal starting choices.
missing_skills={
 'animal_companion':['Animal Handling'],'cavalry':['Animal Handling'],'field_medic':['Medicine'],
 'anatomy_lore':['Nature','Survival'],'arcane_calculus':['Arcana'],'beast_lore':['Survival'],
 'combat_engineering':['Engineering'],'favored_enemy_dragon':['Survival'],'primal_instinct':['Survival'],
 'siege_savant':['Engineering'],'temporal_theory':['Arcana'],'trapsetter':['Engineering'],
 'necrotic_affinity':['Religion'],
}
for sid,avoid in missing_skills.items():
    who=actor(level=primary[sid]['targetClassOpportunity'],avoid=avoid)
    add(sid,'missing-training',who,False,'The selected source grants supply neither required training nor an alternative qualifying branch.')

for sid,first in [('heavily_armored','Bard'),('medium_armor_master','Bard'),('moderately_armored','Warrior'),
                  ('shield_expert','Warrior'),('battlefield_tactician','Bard'),('whip_control','Bard')]:
    add(sid,'wrong-source-training',actor(first),False,'The actual first-class row lacks this credential; later multiclass grants cannot be imported.')
add('master_smithing','different-artisan-tool',dict(actor('Monk'),classToolChoices=['tools.carpenter-s-tools']),False,'An actual different artisan tool is not Smith tools.')
add('versatile_artisan','no-tool-grant',actor('Paladin',academy=True),False,'This first class/background has no tool grant; physical possession would not supply training.')
for sid in ['double_tap','sure_shot','target_mark','cleaving_momentum','bowyer']:
    who=actor('Shaman');who['physicalInventory']=['simple-melee-weapons.spear']
    add(sid,'shaman-versatile-thrown',who,False,'Club/spear/staff training supplies no actual ranged/bow/Two-Handed profile; thrown and Versatile are separate properties.')
for sid in ['weaponFocus','weapon_mastery']:
    who=actor('Bard',level=primary[sid]['targetClassOpportunity']);who['weaponChoice']='martial-melee-weapons.whip'
    add(sid,'untrained-chosen-profile',who,False,'Owning an actual Whip profile is distinct from being proficient with it.')
    who['physicalInventory']=['martial-melee-weapons.whip']
    add(sid,'possessed-but-untrained',who,False,'Physical possession does not create profile proficiency.')
    who=deepcopy(primary[sid]);who['weaponChoice']='all martial weapons'
    add(sid,'umbrella-is-not-profile',who,False,'The permanent choice must be an actual defined weapon profile.')

# Every alternate current-source OR arm is exercised separately.
add('bowyer','shortbow-only',actor('Bard'),True,'Simple training gives Shortbow; it does not grant Longbow.')
add('anatomy_lore','survival-only',actor('Bard','Survival',avoid=['Nature']),True,'Actual Survival is an independent printed alternative to the bounded Nature bridge.')
add('necrotic_affinity','level-eight-without-religion',actor('Bard',level=8,avoid=['Religion']),True,'Printed level-eight OR branch requires no Religion proficiency.')
add('trapsetter','thieves-tools-only',actor('Thief'),True,'Actual Thief tools training supports the explicit mechanical disarm bridge without Engineering.')
add('cleaving_momentum','longsword-held-full-martial-training',dict(actor('Paladin'),physicalInventory=['martial-melee-weapons.longsword']),True,'Actual Greatsword proficiency exists despite currently holding only a Versatile longsword.')
add('cleaving_momentum','simple-two-handed-shortbow',actor('Bard'),True,'The acquisition gate says Two-Handed property, not melee; use-time attack conditions remain separate.')

NUMERICAL = {
 'climb_anywhere':('Athletics','STR',4), 'cold_reader':('Insight','WIS',5),
 'disguise_expert':('Deception','CHA',4), 'forensic_investigator':('Investigation','INT',5),
 'herbalist':('Nature','INT',5), 'lock_savant':('thieves tools','DEX',5),
 'master_tracker':('Survival','WIS',4), 'runic_scholar':('Arcana','INT',5),
 'silent_movement':('Stealth','DEX',4), 'spell_scribe':('Arcana','INT',4),
 'trap_sense':('Perception','WIS',4), 'wilderness_chef':('Nature','INT',4),
 'wilderness_walker':('Survival','WIS',4),
}
for sid,(skill,ability,minimum) in NUMERICAL.items():
    level=8 if sid=='trap_sense' else 4
    pb=3 if level==8 else 2
    for delta in [-1,0,1]:
        who=actor('Thief' if skill=='thieves tools' else 'Bard',None if skill=='thieves tools' else skill,level)
        value=10+2*(minimum+delta-pb)
        # Lock Savant's DEX15 is independently required; DEX15 still has +2.
        if sid=='lock_savant' and delta==-1:value=15
        score(who,ability,value)
        if delta==-1:
            who['situationalBonuses']={'equipment':10,'Help':True,'advantage':True,'featBonus':10}
        add(sid,'modifier-'+str(minimum+delta),who,delta>=0,'Permanent ability modifier plus one actual PB; equipment, Help, advantage and situational bonuses are excluded.')
    who=actor('Bard',level=level,avoid=[] if skill=='thieves tools' else [skill])
    score(who,ability,18)
    add(sid,'high-ability-without-training',who,False,'A high ability score does not satisfy the explicit actual-proficiency requirement.')
    if skill!='thieves tools':
        who=actor('Bard',skill,8)
        known=set(who['selectedClassSkills'])|{'History','Performance','Reputation','Persuasion'}
        new_skill=next(name for name in foundation['skillAbilities'] if name not in known)
        who['priorFeatChoices']=[{'featId':'skill_expert','classLevel':4,'newSkill':new_skill,'expertiseSkill':skill}]
        # Keep separately required abilities satisfied, while deriving Expertise from a real prior feat.
        score(who,ability,14)
        add(sid,'prior-paid-expertise',who,True,'Actual Skill Expert at class four replaces PB with 2PB; no extra ability increase or tool Expertise is inferred.')

# Separate arithmetic/branch probes are validated without claiming full feat use.
special={
 'expertiseNewSkill':actor('Bard',level=8,avoid=['Nature']),
 'expertiseThenNaturalist':actor('Bard','Nature',12),
 'lockAtLevelEight':actor('Thief',level=8),
}
special['expertiseNewSkill']['priorFeatChoices']=[{'featId':'skill_expert','classLevel':4,'newSkill':'Nature','expertiseSkill':'Nature'}]
special['expertiseThenNaturalist']['priorFeatChoices']=[{'featId':'skill_expert','classLevel':4,'newSkill':'Medicine','expertiseSkill':'Nature'}, {'featId':'naturalist','classLevel':8}]
score(special['lockAtLevelEight'],'DEX',15)
add('lock_savant','dex-fifteen-pb-three',special['lockAtLevelEight'],True,'DEX15 contributes +2 and actual level-eight PB contributes +3; no tool Expertise is needed.')

source_paths=[R/'tools/build_feat_exact_01_training_fixtures.py',
 A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',R/'data/playtest/character_foundation.json',
 R/'data/playtest/ancestry_background_candidate.json',R/'data/playtest/equipment_source_catalog.json',
 R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'data/director/feat_candidates/exact_01/shared_rules.json',
 R/'data/public/feat_candidates/exact_01/candidate.json',A/'FEAT327_ACQ_01_INDEPENDENT_CHECK.json',
 A/'FEAT327_ACQ_02_INDEPENDENT_FULFILLMENT.json']
source_paths += [G/classes[name]['classCandidatePath'] for name in sorted({x['actor']['firstClass'] for x in cases})]
payload={
 'status':'authored-source-qualified-training-slices-awaiting-validation',
 'scope':'48 prerequisite trees plus earned/unspent class feat payment. Not complete feat acquisitions, class-card builds, ability allocations, initial resource states, full payload/use procedures, legacy receipts or human roll/award authentication.',
 'sourceBindings':[info(p) for p in source_paths],
 'cohortIds':[x[0] for x in PLANS],
 'completeContracts':[contracts[x[0]] for x in PLANS],
 'firstClassSources':{name:classes[name] for name in sorted({x['actor']['firstClass'] for x in cases})},
 'priorTrainingFeatSources':{name:contracts[name] for name in ['skill_expert','naturalist','alert']},
 'cases':cases,'specialTrainingCases':special,
 'unprofiledGrantLimit':'Soldier repeating-heavy-crossbow/sidearm and siege-engineer training are not relabeled as ordinary catalog weapons/tools. The Soldier example only tests its actual class credential. Missing catalog profiles do not prove absence of those source grants.',
 'unmodeledLegacyBranch':'Anatomy Lore legacy Knowledge (Monstrous Humanoids) positive receipt is not supplied; current Nature and Survival alternatives are exercised.',
 'candidateSelectionEnabled':False,'completeAcquisitionsValidated':False,'candidateReadyForSubmission':False,
}
assert len(PLANS)==48 and len(set(payload['cohortIds']))==48
with OUT.open('x',encoding='utf-8',newline='\n') as stream:
    json.dump(payload,stream,ensure_ascii=False,indent=2);stream.write('\n')
print(json.dumps({'fixture':info(OUT),'cohort':48,'cases':len(cases)},indent=2))
