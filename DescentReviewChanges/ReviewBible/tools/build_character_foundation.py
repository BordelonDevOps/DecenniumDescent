"""Build the source-linked 17-class foundation from the recorded GPT conference."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME/'docs/audit/2026-10-08/full-game'
EVIDENCE = json.loads((AUDIT/'CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json').read_text(encoding='utf-8'))
SOURCE_CLASSES = {x['class']:x for x in EVIDENCE['classes']}

SKILLS = {
    'STR':['Athletics'], 'DEX':['Acrobatics','Sleight of Hand','Stealth'],
    'INT':['Arcana','Engineering','History','Investigation','Nature','Religion'],
    'WIS':['Animal Handling','Insight','Medicine','Perception','Survival'],
    'CHA':['Deception','Intimidation','Performance','Persuasion','Reputation']}
ALL_SKILLS = [skill for skills in SKILLS.values() for skill in skills]

# Class, HD, saves, tier, wealth dice/multiplier, class skill choice/list, multiclass gate.
ROWS = [
 ('Bard',8,'DEX CHA','hybrid',5,10,3,ALL_SKILLS,'CHA'),
 ('Cleric',8,'WIS CHA','full',5,10,2,'History|Insight|Medicine|Persuasion|Religion','WIS'),
 ('Crimson Agent',8,'DEX INT','hybrid',4,10,4,'Acrobatics|Athletics|Deception|Insight|Intimidation|Investigation|Perception|Sleight of Hand|Stealth','DEX CON'),
 ('Dragoon',10,'STR DEX','minor',5,10,2,'Athletics|Acrobatics|Perception|Survival','STR DEX'),
 ('Druid',8,'INT WIS','full',2,10,2,'Arcana|Animal Handling|Insight|Medicine|Nature|Perception|Religion|Survival','WIS'),
 ('Mage',6,'INT WIS','full',4,10,2,'Arcana|History|Insight|Investigation|Medicine|Religion','INT'),
 ('Mirrorsage',8,'INT CHA','hybrid',4,10,3,'Arcana|History|Insight|Investigation|Nature|Perception','INT CHA'),
 ('Monk',8,'STR DEX','minor',5,1,2,'Acrobatics|Athletics|History|Insight|Religion|Stealth','DEX WIS'),
 ('Oracle',6,'WIS CHA','none',3,10,4,'Arcana|History|Insight|Medicine|Persuasion|Religion','WIS CHA'),
 ('Paladin',10,'WIS CHA','half',5,10,2,'Athletics|Insight|Intimidation|Medicine|Persuasion|Religion','STR CHA'),
 ('Ranger',8,'STR DEX','half',5,10,3,'Animal Handling|Athletics|Insight|Investigation|Nature|Perception|Stealth|Survival','DEX WIS'),
 ('Shaman',8,'WIS CON','hybrid',2,10,4,'Animal Handling|Insight|Medicine|Nature|Perception|Religion|Survival','WIS CON'),
 ('Soldier',10,'STR CON','none',5,10,2,'Athletics|Intimidation|Perception|Survival','STR CON'),
 ('Thief',8,'DEX INT','minor',4,10,4,'Acrobatics|Athletics|Deception|Insight|Intimidation|Investigation|Perception|Performance|Persuasion|Sleight of Hand|Stealth','DEX'),
 ('Tinker',8,'INT DEX','minor',4,10,2,'Arcana|Engineering|History|Investigation|Medicine|Nature|Perception','INT DEX'),
 ('Warrior',12,'STR CON','none',2,10,2,'Animal Handling|Athletics|Intimidation|Nature|Perception|Survival','STR CON'),
 ('Wizard',6,'INT WIS','full',4,10,2,'Arcana|History|Insight|Investigation|Medicine|Religion','INT'),
]
PROFICIENCIES = {
 'Bard':('Light','Simple weapons; musical instruments used as improvised weapons','Three musical instruments'),
 'Cleric':('Light; Medium; Shields','Simple weapons; one existing mundane deity-favored weapon selected and recorded at creation','Religious implements'),
 'Crimson Agent':('Light','Simple weapons; actual Finesse-property or Thrown-property weapons',"Poisoner's kit; thieves' tools"),
 'Dragoon':('Light; Medium','Simple weapons; spears; glaives; tridents',"Leatherworker's tools"),
 'Druid':('Light; Medium; Shields — no metal armor or shields','Clubs; daggers; darts; javelins; maces; quarterstaffs; scimitars; sickles; slings; spears','Herbalism kit'),
 'Mage':('None','Daggers; darts; slings; quarterstaffs; light crossbows',"Arcana tools; scribe's supplies"),
 'Mirrorsage':('Light','Simple weapons; shortswords; hand crossbows',"Calligrapher's supplies"),
 'Monk':('None','Simple weapons; kama; nunchaku; staff',"One artisan's tool"),
 'Oracle':('Light','Simple weapons; symbolic/relic weapons only with an actual defined weapon profile','Divination tools'),
 'Paladin':('Light; Medium; Heavy; Shields','Simple weapons; Martial weapons','None'),
 'Ranger':('Light; Medium — no plate','Longbows; shortbows; spears; daggers; shortswords; scimitars','Survival tools; herbalism kit'),
 'Shaman':('Light','Clubs; spears; staves',"Alchemist's supplies; herbalism kit"),
 'Soldier':('Light; Medium; Heavy; Shields','Repeating heavy crossbows; actual equipment explicitly classified as a sidearm',"Carpenter's tools; siege engineer's kit"),
 'Thief':('Light','Daggers; shortswords; hand crossbows; actual Thrown-property weapons',"Thieves' tools; poisoner's kit"),
 'Tinker':('Light','Simple weapons; shortbows; crossbows',"Tinker's tools; alchemist's supplies"),
 'Warrior':('Medium; Heavy','Martial weapons','None'),
 'Wizard':('None','Daggers; darts; slings; quarterstaffs; light crossbows',"Arcana tools; scribe's supplies"),
}
MC_PROFICIENCIES = {
 'Bard':'Light armor; one skill of your choice; one musical instrument',
 'Cleric':'Light armor; medium armor; shields',
 'Crimson Agent':"Light armor; one skill from this class's list",
 'Dragoon':'Medium armor; shields; martial weapons',
 'Druid':'Light armor; medium armor; shields — no metal armor or shields',
 'Mage':"One skill from this class's list",
 'Mirrorsage':"One skill from this class's list",
 'Monk':'Simple weapons; shortswords',
 'Oracle':"Light armor; one skill from this class's list",
 'Paladin':'Light armor; medium armor; shields; simple weapons; martial weapons',
 'Ranger':"Light armor; medium armor; shields; simple weapons; martial weapons; one skill from this class's list",
 'Shaman':"Light armor; shields; one skill from this class's list",
 'Soldier':'Light armor; medium armor; heavy armor; shields; simple weapons; martial weapons',
 'Thief':"Light armor; one skill from this class's list; thieves' tools",
 'Tinker':"Light armor; one skill from this class's list; tinker's tools",
 'Warrior':'Light armor; medium armor; shields; simple weapons; martial weapons',
 'Wizard':"One skill from this class's list",
}

profiles=[]
for name,hd,saves,tier,dice,mult,count,skill_list,gate in ROWS:
    source=SOURCE_CLASSES[name]
    armor,weapons,tools=PROFICIENCIES[name]
    profile={'class':name,'slug':source['slug'],'hitDie':hd,'fixedLaterLevelHpBase':hd//2+1,
             'savingThrowProficiencies':saves.split(),'weaveTier':tier,
             'armor':armor,'weapons':weapons,'tools':tools,
             'skillChoices':count,'skillOptions':skill_list if isinstance(skill_list,list) else skill_list.split('|'),
             'startingWealth':{'diceCount':dice,'dieSides':4,'multiplierGp':mult},
             'multiclassPrerequisites':{ability:13 for ability in gate.split()},
             'multiclassProficiencies':MC_PROFICIENCIES[name],
             'rpByClassLevel':source['rpByClassLevel'],
             'asiClassLevels':source['asiClassLevels'],
             'classCandidatePath':source['activeCandidatePath'],
             'classCandidateSha256':source['activeCandidateSha256'],
             'sourceChassisLines':[x['line'] for x in source['detailedBookChassis']],
             'sourceComparison':'docs/audit/2026-10-08/full-game/CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json'}
    profiles.append(profile)

obj={'schemaVersion':'1.0','version':'0.1-playtest',
     'status':'REVIEWED CHARACTER FOUNDATION — authored operational PLAYTEST candidate',
     'reviewTurnId':'93aa40e3-89e9-46cd-bd22-d70cb3e244e1',
     'exactReviewTurnId':'d1bc9c3b-6f5a-4aed-a6ad-d39d5cdd933f',
     'proceduralAuthority':'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md; the class data accompanies this guide and is not a complete character runtime schema.',
     'authorityOrder':['Reviewed active class contract','Detailed class entry','Classes Table fallback','Companion only for actual gaps'],
     'sourceEvidenceSha256':hashlib.sha256((AUDIT/'CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json').read_bytes()).hexdigest(),
     'sourceBookSha256':EVIDENCE['playerSegments'][0]['sha256'],
     'skillAbilities':SKILLS,'pointBuy':{'budget':27,'minimum':8,'maximum':15,'costs':{str(k):v for k,v in zip(range(8,16),[0,1,2,3,4,5,7,9])},'status':'provisional-optional-companion-derived'},
     'standardArray':[15,14,13,12,10,8],
     'xpThresholds':[0,300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000],
     'classes':profiles,
     'unclosedScope':['Complete ancestry traits/ASI reconciliation','Complete background packages/features','Equipment records/prices/weights/carrying','Remaining feats and spells','Separate prestige-class mechanics','Live companion parity','Human balance','Final authored flow and GitHub delivery'],
     'cosmology':'Deferred until after successful authorized GitHub push and remote commit verification'}
out=ROOT/'data/playtest/character_foundation.json'
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Character foundation tables\n',
       '**REVIEWED CHARACTER FOUNDATION — authored operational PLAYTEST candidate.** Use with [creation and advancement](CHARACTER_CREATION_PLAYTEST.md). This table resolves starting class statistics; complete ancestry/background/equipment and live companion parity remain open.\n',
       '## Starting class, Hit Dice, skills and wealth\n',
       'Saving throws and full starting skills apply to the first character class. Later new classes use the separate multiclass table. Wealth replaces class/background starting equipment; it is not added to those packages.\n',
       '| Class | HD / later fixed base | Saves | Starting skills | Starting wealth | ASI class levels |',
       '|---|---|---|---|---|---|']
for p in profiles:
    w=p['startingWealth'];wealth=f"{w['diceCount']}d4"+(f" × {w['multiplierGp']}" if w['multiplierGp']!=1 else '')+' gp'
    guide='BARD_PLAYTEST_v0_1.md' if p['class']=='Bard' else f"classes/{p['slug']}.md"
    lines.append(f"| [{p['class']}]({guide}) | d{p['hitDie']} / {p['fixedLaterLevelHpBase']} | {', '.join(p['savingThrowProficiencies'])} | Choose {p['skillChoices']} | {wealth} | {' / '.join(map(str,p['asiClassLevels']))} |")
lines.extend(['','Add CON modifier to the HP base for each attained level, minimum 1 per level. Only the first **character** level uses the maximum die value. Mirrorsage d8, Oracle d6 and Ranger d8 retain their previously reviewed detailed-book resolutions. Monk wealth has no ×10 multiplier.','',
              '## Class skill lists','', '| Class | Choose | Eligible skills |','|---|---:|---|'])
for p in profiles:
    lines.append(f"| {p['class']} | {p['skillChoices']} | {', '.join(p['skillOptions'])} |")
lines.extend(['','**New completions:** concrete Crimson Agent, Ranger, Thief and Warrior lists replace companion placeholders. Oracle starting Spellcraft becomes Arcana here only; Tinker adds Engineering as an option, with no extra selection. Druid uses its explicit book list.','',
              '## First-class armor, weapons and tools','',
              '| Class | Armor | Weapons | Tools |','|---|---|---|---|'])
for p in profiles:lines.append(f"| {p['class']} | {p['armor']} | {p['weapons']} | {p['tools']} |")
lines.extend(['','A named weapon, kit, relic, focus, kama, nunchaku or other implement still requires an actual equipment record for its statistics and use. Proficiency does not grant ownership or create an item profile.','',
 'Bard instruments use the ordinary improvised-weapon procedure without an invented die or extra attack. The Cleric favored weapon is one already-existing mundane record chosen and recorded at creation, with no free later change. Ranger’s dagger/shortsword/scimitar definition is a new bounded interpretation of “dual-wielded blades”; it does not remove normal wielding requirements or grant a second attack.','',
 'Soldier sidearms must be explicitly classified in actual equipment records; the equipment pass still has to supply those bindings. Warrior mutation-tagged gear is a bonus-eligibility hook, not a proficiency category. Mage/Wizard Wand, Staff, Arcane Staff, Spell Focus and Spellblade source labels grant no weapon statistics or magical powers by themselves. Druid retains its nonmetal restriction. Monk’s Unarmored Flow follows its own card.','',
 'A legitimate tool check adds proficiency once if trained; skill plus tool training does not add PB twice. Arcana tools, religious implements, divination tools and survival tools remain source-preserved proficiency labels, with actual equipment procedures still required.','',
 '## Multiclass entry','',
 'On taking a new Base class, meet the listed scores for every existing class and the new one. These are not requirements for creating a first-level single-class character. Use only the new class’s proficiency row below; no extra starting saves, full starting skill list, equipment, wealth or background.','',
 '| New class | Minimum scores | Proficiencies gained once on entry |','|---|---|---|'])
for p in profiles:
    gate=', '.join(f'{k} {v}' for k,v in p['multiclassPrerequisites'].items())
    lines.append(f"| {p['class']} | {gate} | {p['multiclassProficiencies']} |")
lines.extend(['','These deliberately preserve the book’s separate multiclass rows even where they are broader than a detailed first-class chassis: for example, Dragoon entry grants shields and martial weapons, and Soldier entry grants simple/martial weapons. They are not merged back into first-class starting lists. Paladin’s starting Martial Proficiency card cannot bypass the multiclass table to grant heavy armor.','',
 '## Ability-check skills','', '| Ability | Skills |','|---|---|'])
for ability,skills in SKILLS.items():lines.append(f"| {ability} | {', '.join(skills)} |")
lines.extend(['','There are 20 basic skills; CON has no default skill. A Director can call for another appropriate ability with a skill when circumstances justify it. Use the reviewed [core task procedure](CORE_RESOLUTION_PLAYTEST.md); attacks and ordinary saves remain distinct.','',
 '## Evidence and status','',
 '[Data](../../data/playtest/character_foundation.json) · [Complete source comparison](../../../../docs/audit/2026-10-08/full-game/CHARACTER_FOUNDATION_SOURCE_EVIDENCE.json) · [GPT conference](../../../../docs/audit/2026-10-08/full-game/GPT_CHARACTER_FOUNDATION_CONFERENCE.md). Original books, companion entries and current class cards remain unchanged. The disagreements are resolved only for this provisional candidate. Cosmology remains deferred until after verified GitHub delivery.',''])
(ROOT/'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'profiles':len(profiles),'skills':len(ALL_SKILLS),'data':str(out)},indent=2))
