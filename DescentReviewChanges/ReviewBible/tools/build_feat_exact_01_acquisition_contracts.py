"""Normalize every exact printed prerequisite for auditable FXC-05 validation.

This is a source-based contract table, not a character builder or proof that
any real character owns the supplied prerequisites. All unknown grammar fails.
The one known weapon-bridge carry-forward issue remains explicitly pending.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
import re

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';V=A/'feat327-source-verdict'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def atom(kind,**kw):return {'kind':kind,**kw}
def all_of(*xs):return atom('all',requirements=list(xs))
def any_of(*xs):return atom('any',requirements=list(xs))
def ability(name,n):return atom('permanentAbility',ability=name,minimum=n)
def level(n):return atom('totalCharacterLevel',minimum=n)
def cls(name,n):return atom('classLevel',className=name,minimum=n)
def prof(name):return atom('actualProficiency',credential=name)
def feat(sid):return atom('ownedFeat',id=sid)
def receipt(name):return atom('actualEstablishedReceipt',receipt=name,doesNotCreateSource=True)
def weapon(category):return atom('actualWeaponProficiency',category=category,bridgeIssue='FEAT327-ACQ-01')
def lineage(name):return atom('actualLineageReceipt',lineage=name,noSilentAlias=True)
CAST=atom('actualSpellcastingRoute',grantsNoPoolRankOrClass=True)
def cast_rank(n):return atom('actualCastAccess',minimumRank=n,notJustCapacityOrRP=True)
def cast_school(name):return atom('actualCastAccess',school=name,notJustCapacityOrRP=True)
def spell(sid):return atom('actualCastAccess',spellId=sid,notJustCapacityOrRP=True)
def skill(name,n,governing):return atom('permanentSkillModifier',skill=name,minimum=n,ability=governing,
    requiresActualProficiency=True,contribution='abilityModifier + PB or replacing2PB Expertise',
    excludes=['equipment','temporary ability changes','situational feat bonuses','Help','advantage'])
def equipped(name):return atom('equippedMutation',name=name,requiresActualUnlockedSlot=True)
def mut_count(category,n):return atom('distinctEquippedMutations',category=category,minimum=n,requiresActualUnlockedSlots=True)

ABIL={'Strength':'STR','Dexterity':'DEX','Constitution':'CON','Intelligence':'INT','Wisdom':'WIS','Charisma':'CHA','Agility':'DEX'}
SKILLS={'Athletics':'STR','Insight':'WIS','Deception':'CHA','Investigation':'INT','Nature':'INT','Thievery':'DEX','Survival':'WIS','Arcana':'INT','Stealth':'DEX','Perception':'WIS'}
SPECIAL={
 'Spellcasting ability':CAST,
 'Animal Handling proficiency':prof('Animal Handling'),
 'Spellcasting ability, Level 3':all_of(CAST,level(3)),
 'Wisdom 17+, level 15+':all_of(ability('WIS',17),level(15)),
 'Spellcasting ability, proficiency with martial weapons':all_of(CAST,weapon('martial')),
 'Charisma 15+, Level 12':all_of(ability('CHA',15),level(12)),
 'Intelligence 14+, Soldier':all_of(ability('INT',14),cls('Soldier',1)),
 'Strength 16+, Level 9':all_of(ability('STR',16),level(9)),
 'Dexterity 14+, Melee':all_of(ability('DEX',14),weapon('melee')),
 'Proficiency with longbow or shortbow':any_of(weapon('longbow'),weapon('shortbow')),
 'Dexterity 15+, Level 10':all_of(ability('DEX',15),level(10)),
 'Ability to cast cantrips':atom('actualCastAccess',exactRank=0,notJustCapacityOrRP=True),
 'Strength 16+, 2H Weapon':all_of(ability('STR',16),weapon('Two-Handed-property')),
 'Athletics 4+, Strength 13+':all_of(skill('Athletics',4,'STR'),ability('STR',13)),
 'Insight 5+, Charisma 13+':all_of(skill('Insight',5,'WIS'),ability('CHA',13)),
 'Strength 14+, Melee':all_of(ability('STR',14),weapon('melee')),
 'Charisma 14+, Deception 4+':all_of(ability('CHA',14),skill('Deception',4,'CHA')),
 'Ability to cast dispel magic':spell('dispel-magic'),
 'Charisma 15+, worship a deity':all_of(ability('CHA',15),receipt('already-established deity worship')),
 'Dexterity 14+, Ranged':all_of(ability('DEX',14),weapon('ranged')),
 'Dragonborn or sorcerer with draconic bloodline':any_of(lineage('Dragonborn'),all_of(cls('Sorcerer',1),receipt('draconic bloodline with one recorded ancestry damage type'))),
 'Intelligence 12+, Level 4':all_of(ability('INT',12),level(4)),
 'Ability to cast at least one spell':CAST,
 'Constitution 15+, exposure to elemental plane':all_of(ability('CON',15),receipt('actual recorded elemental-plane exposure; literal only, no new cosmology')),
 'Ability to cast 3rd level spells':cast_rank(3),
 'Elf or half-elf':any_of(lineage('Elf'),lineage('Half-elf')),
 'Ability to cast enchantment spells':cast_school('Enchantment'),
 'Ability to cast evocation spells':cast_school('Evocation'),
 'Ability to cast find familiar':spell('find-familiar'),
 'Dexterity 14+, Charisma 13+':all_of(ability('DEX',14),ability('CHA',13)),
 'Trained in Medicine':prof('Medicine'),
 'Investigation 5+':skill('Investigation',5,'INT'),
 'Spell Focus feat':atom('ownedSupplementFeat',name='Spell Focus',source='SUP-05/newSpellFocus',notAddedToOriginal335=True),
 'Proficiency with medium armor':prof('medium armor'),
 'Nature 5+, Wisdom 13+':all_of(skill('Nature',5,'INT'),ability('WIS',13)),
 'Constitution 17+, level 10+':all_of(ability('CON',17),level(10)),
 'Alertness feat':feat('alertness'),'Athlete feat':feat('athlete'),'Climber feat':feat('climber'),
 'Charisma 13+ or Strength 15+':any_of(ability('CHA',13),ability('STR',15)),
 'Charisma 15+, level 6+':all_of(ability('CHA',15),level(6)),
 'Dexterity 15+, Thievery 5+':all_of(ability('DEX',15),skill('thieves tools',5,'DEX')),
 'Strength 13+, Weapon Proficiency':all_of(ability('STR',13),weapon('any actual profile')),
 'Martial Adept feat':feat('martialAdept'),
 'Survival 4+, Wisdom 13+':all_of(skill('Survival',4,'WIS'),ability('WIS',13)),
 'Spellcasting ability, Level 4':all_of(CAST,level(4)),
 'Proficiency with light armor':prof('light armor'),
 'Half-orc or orc':any_of(lineage('Half-orc'),lineage('Orc')),
 'Charisma 15+, ability to cast 5th level spells':all_of(ability('CHA',15),cast_rank(5)),
 'Half-elf, half-orc, or human':any_of(lineage('Half-elf'),lineage('Half-orc'),lineage('Human')),
 'Agility 15+, Melee Proficiency':all_of(ability('DEX',15),weapon('melee')),
 'Dexterity 15+, Level 7':all_of(ability('DEX',15),level(7)),
 'Arcana 5+, Intelligence 14+':all_of(skill('Arcana',5,'INT'),ability('INT',14)),
 'Shield Proficiency':prof('shields'),
 'Stealth 4+':skill('Stealth',4,'DEX'),
 'Spellcasting ability, Level 5':all_of(CAST,level(5)),
 'Arcana 4+, Intelligence 14+':all_of(skill('Arcana',4,'INT'),ability('INT',14)),
 'Dexterity 14+, Ranged Proficiency':all_of(ability('DEX',14),weapon('ranged')),
 'Constitution 13+, Wisdom 13+':all_of(ability('CON',13),ability('WIS',13)),
 'Intelligence 12+, Melee':all_of(ability('INT',12),weapon('melee')),
 'Wisdom 14+, Ranged':all_of(ability('WIS',14),weapon('ranged')),
 'Tinkering 5+':atom('trainedTradeLevel',trade='Tinkering',minimum=5,notSkillCheckBonus=True),
 'Perception 4+, Level 5':all_of(skill('Perception',4,'WIS'),level(5)),
 'Strength 14+, Level 8':all_of(ability('STR',14),level(8)),
 'Tool Proficiency':prof('at least one actual tool'),
 'Proficiency with chosen weapon':weapon('permanently chosen actual profile'),
 'Proficient, Level 6':all_of(weapon('permanently chosen actual profile'),level(6)),
 'Dexterity 15+, Whip':all_of(ability('DEX',15),weapon('whip')),
 'Nature 4+, Wisdom 13+':all_of(skill('Nature',4,'INT'),ability('WIS',13)),
 'Survival 4+':skill('Survival',4,'WIS'),
 'Intelligence 13+, proficiency in Knowledge (Monstrous Humanoids) or Survival':all_of(ability('INT',13),any_of(prof('legacy Knowledge (Monstrous Humanoids)'),prof('bounded INT(Nature) anatomy bridge'),prof('Survival'))),
 'Spellcasting ability, Intelligence 13+':all_of(CAST,ability('INT',13)),
 'Intelligence 15+, proficiency in Arcana':all_of(ability('INT',15),prof('Arcana')),
 'Power Attack or Combat Casting, spellcasting ability':all_of(any_of(feat('power_attack'),feat('combatCasting')),CAST),
 'Wisdom 13+, proficiency in Survival':all_of(ability('WIS',13),prof('Survival')),
 'Constitution 13+, level 4+':all_of(ability('CON',13),level(4)),
 'Intelligence 13+, proficiency in Engineering':all_of(ability('INT',13),prof('Engineering')),
 'Animal Companion feat or proficiency in Animal Handling':any_of(feat('animal_companion'),prof('Animal Handling')),
 'Spellcasting ability, proficiency in Nature':all_of(CAST,prof('Nature')),
 'Proficiency in Craft (Blacksmith), spellcasting ability or Engineering':all_of(prof('Smith tools / Blacksmithing'),any_of(CAST,prof('Engineering'))),
 'Spellcasting ability or proficiency in Arcana, level 6+':all_of(any_of(CAST,prof('Arcana')),level(6)),
 'Spellcasting ability, Charisma 13+':all_of(CAST,ability('CHA',13)),
 'Constitution 13+, level 6+':all_of(ability('CON',13),level(6)),
 'Curse Channeling or level 8+':any_of(feat('curse_channeling'),level(8)),
 'Forbidden Pact or spellcasting ability, level 3+':all_of(any_of(feat('forbidden_pact'),CAST),level(3)),
 'Proficiency in Survival, level 5+':all_of(prof('Survival'),level(5)),
 'Charisma 13+, level 3+':all_of(ability('CHA',13),level(3)),
 'Constitution 15+, Berserker feat or class rage ability':all_of(ability('CON',15),any_of(feat('berserker'),receipt('actual acquired class rage ability'))),
 'Precision Strike or level 8+':any_of(feat('precision_strike'),level(8)),
 'Dark Affinity or Hemocraft':any_of(feat('dark_affinity'),feat('hemocraft')),
 'Spellcasting ability or proficiency in Nature':any_of(CAST,prof('Nature')),
 'Proficiency in Craft (Blacksmith), Intelligence 13+':all_of(prof('Smith tools / Blacksmithing'),ability('INT',13)),
 'Spellcasting ability, Intelligence 15+':all_of(CAST,ability('INT',15)),
 'Proficiency in Religion or level 8+':any_of(prof('Religion'),level(8)),
 'Dexterity 13+ or Weapon Focus':any_of(ability('DEX',13),feat('weaponFocus')),
 'Intelligence 15+, Arcane Calculus or Temporal Theory':all_of(ability('INT',15),any_of(feat('arcane_calculus'),feat('temporal_theory'))),
 'Proficiency in Engineering':prof('Engineering'),
 'Favored Enemy (Dragon) or level 8+':any_of(feat('favored_enemy_dragon'),level(8)),
 'Lifeleech or spellcasting ability, level 8+':all_of(any_of(feat('lifeleech'),CAST),level(8)),
 'Spellcasting ability, level 8+':all_of(CAST,level(8)),
 'Spellcasting ability, proficiency in Nature or Spellcraft':all_of(CAST,any_of(prof('Nature'),prof('actual legacy Spellcraft; not Arcana alias'))),
 'Intelligence 15+, proficiency in Arcana, level 8+':all_of(ability('INT',15),prof('Arcana'),level(8)),
 'Conjure Flora or Verdant Bond':any_of(feat('conjure_flora'),feat('verdant_bond')),
 'Proficiency in Engineering or Disable Device':any_of(prof('Engineering'),prof('thieves tools mechanical disarm interface')),
 'Constitution 15+, Necrotic Affinity or Dark Fortitude':all_of(ability('CON',15),any_of(feat('necrotic_affinity'),feat('dark_fortitude'))),
 'Proficiency in Nature, spellcasting ability':all_of(prof('Nature'),CAST),
 'Stormcaller or Lightning Affinity, level 6+':all_of(any_of(feat('stormcaller'),feat('lightning_affinity')),level(6)),
}

MUTATIONS={
 'backlashEngine':equipped('Adrenal Backlash Core'),
 'bioStabilizer':equipped('Bloodthick Node'),
 'bornToHorrify':mut_count('Apex',1),
 'distortedDominance':mut_count('Aberrant',1),
 'evisceratorProtocol':all_of(equipped('Echo Knuckles'),equipped('Warpgrip Talons')),
 'evolutionUnderFire':mut_count('Apex',1),
 'hypermutationSpike':equipped('Butcherform Chassis'),
 'juggernautCore':equipped('Ossified Core'),
 'killChainAdaptation':mut_count('Combat',2),
 'livingFortress':mut_count('Vital',3),
 'synapticRot':any_of(equipped('Wailing Eye Cluster'),equipped('Viral Core Sacs')),
 'terrorEngine':equipped('Carrion Signal Gland')}

TRAINING={
 'athleticProdigy':{'Athletics':'snapshot-proficiency-or-expertise','Acrobatics':'snapshot-proficiency-or-expertise'},
 'charismatic':{'Persuasion':'snapshot-proficiency-or-expertise','Deception':'snapshot-proficiency-or-expertise'},
 'diplomat':{'Persuasion':'snapshot-proficiency-or-expertise','Insight':'snapshot-proficiency-or-expertise'},
 'naturalist':{'Nature':'snapshot-proficiency-or-expertise','Survival':'snapshot-proficiency-or-expertise'},
 'acrobatic':{'Acrobatics':'proficiency-only'},
 'ranger_training':{'Survival':'proficiency-only','Nature':'proficiency-only'}}

def parse(text):
    if text=='None':return atom('noPrintedPrerequisite')
    if text in SPECIAL:return SPECIAL[text]
    mt=re.fullmatch(r'(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma|Agility) (\d+)(?:\+| or higher)',text)
    if mt:return ability(ABIL[mt[1]],int(mt[2]))
    mt=re.fullmatch(r'(Strength|Intelligence) or (Dexterity|Wisdom|Charisma) (\d+)(?:\+| or higher)',text)
    if mt:return any_of(ability(ABIL[mt[1]],int(mt[3])),ability(ABIL[mt[2]],int(mt[3])))
    mt=re.fullmatch(r'Level (\d+)',text)
    if mt:return level(int(mt[1]))
    mt=re.fullmatch(r'(Gnome|Ogre|Goblin|Elf|Dwarf|Feykin|Umbrin|Orc|Troll|Human) heritage',text)
    if mt:return lineage(mt[1])
    raise ValueError('Unmapped exact printed prerequisite: '+repr(text))

def main():
    target=A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json'
    manuscript=A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.md'
    assert not target.exists() and not manuscript.exists(),'Do not overwrite emitted source evidence'
    source=read(V/'FEAT_327_AUTHORING_REGISTER.json');sd={x['featId']:x for x in source['records']}
    public=read(R/'data/public/feat_candidates/exact_01/candidate.json')
    hm=read(R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json')
    pairs={x['featId']:x['completeClassCounterpart'] for x in hm['originalWarriorCounterpartPairs']}
    assert set(pairs)==set(MUTATIONS)
    output=[]
    for i,p in enumerate(public['feats']):
        sid=p['id'];original=p['sourceObject'];printed=original.get('prerequisite')
        req=all_of(cls('Warrior',pairs[sid]['minimumClassLevel']),MUTATIONS[sid]) if sid in pairs else parse(printed)
        rule=p['unchangedReviewedRecord']['operationalRules'] if 'unchangedReviewedRecord' in p else p['operationalRules']
        row={'id':sid,'name':p['name'],'originalObject':original,'printedPrerequisitePresent':'prerequisite' in original,
             'printedPrerequisite':printed,'candidatePointer':f'/feats/{i}','requirements':req,
             'additionalUniversalAcquisitionGate':'One actual unspent class-scheduled ASI/feat opportunity or separately authorized feat grant; prerequisite success never creates a choice.',
             'actualClassScheduleRequired':True,'candidateSelectionEnabled':False,
             'acquisitionDoesNotGrantUseWithoutOngoingPredicates':True,'completeOperativeProcedure':rule,
             'requirementsStatus':'Source-derived finite validation contract; actual positive/negative actor histories still require testing.',
             'boundaryCasesValidated':False,'repeats':{'policy':'nonrepeatable','permanentChoice':True},
             'sourceDecision':sd[sid]['decision'] if sid in sd else 'Retain the entire already reviewed envelope without alteration.',
             'requiresLegacyOrContextReceiptWithoutCreatingIt':any(k in json.dumps(req) for k in ['actualEstablishedReceipt','actualLineageReceipt','Spellcraft','Sorcerer'])}
        if sid in {'abilityScoreImprovement','armorProficiency','resilient','weaponFocus'}:
            row['repeats']={'policy':{'abilityScoreImprovement':'each actual ASI opportunity, full legal allocation','armorProficiency':'different currently missing tier','resilient':'different save ability','weaponFocus':'different actual proficient weapon profile'}[sid],'permanentChoice':True}
        if sid in pairs:
            row['sharedPaidIdentity']={'featId':sid,'classCardId':pairs[sid]['id'],'samePaidIdentity':True,
                'classCardComparisonOnly':True,'completeClassCounterpart':pairs[sid],
                'acquisitionUsesEquippedState':'Existing slots/tier access required; active/use predicates remain in full source-directed procedure.'}
        if sid in TRAINING:row['fixedTrainingBranches']=TRAINING[sid]
        if sid in {'astral_projection','planar_binding'}:row['payloadAvailability']='null and unavailable even when prerequisite wrapper is legitimately acquired; no cosmology approval'
        if sid=='magicInitiate' or sid.startswith('magic_initiate_'):
            row['curriculumIdentity']='Generic and named Magic Initiate for the same curriculum share one acquisition entitlement. No duplicate charges under another name.'
        if 'bridgeIssue' in json.dumps(req):
            row['pendingExactIssue']='FEAT327-ACQ-01 sent to actual GPT; proposed generic weapon bridge not locally adopted. Per-feat explicit gates retain their own authority.'
        if 'unchangedReviewedRecord' in p:row['unchangedReviewedEnvelope']=p['unchangedReviewedRecord']
        output.append(row)
    assert len(output)==335 and len({x['id'] for x in output})==335
    names={x['id'] for x in output}
    def walk(x):
        if x['kind']=='ownedFeat':assert x['id'] in names,x
        for y in x.get('requirements',[]):walk(y)
    for x in output:walk(x['requirements'])
    result={'createdAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Complete prerequisite contract normalization; exhaustive legal-actor boundary testing pending.',
            'scope':'All335 original IDs including eight unchanged reviewed; final twelve Warrior overrides and six exploration training branches. Original strings never rewritten.',
            'sourceBindings':[info(p) for p in [Path(__file__),V/'FEAT_327_AUTHORING_REGISTER.json',V/'FEAT_SHARED_DIRECTIONS.json',V/'FEAT_SHARED_CONVENTION_DISPOSITIONS.json',
                R/'data/public/feat_candidates/exact_01/candidate.json',R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json']],
            'records':output,'counts':{'originalIds':335,'distinctPrintedPrerequisites':len({x['printedPrerequisite'] for x in output}),
                'sharedWarriorPaidIdentities':12,'explorationTrainingEntries':6,'unchangedReviewed':sum('unchangedReviewedEnvelope' in x for x in output),
                'recordsTouchingPendingWeaponBridge':sum('pendingExactIssue' in x for x in output)},
            'selectionEnabled':False,'allAcquisitionBoundariesValidated':False,'candidateReadyForSubmission':False,
            'doesNotProveActualCampaignReceiptsOrChoices':True,'pendingExactIssue':'FEAT327-ACQ-01'}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Feat prerequisite contracts','',result['scope'],'',result['status'],'',
           'This table is an audit aid. It does not grant feats or prove that a character has its prerequisites. FEAT327-ACQ-01 is a narrowly scoped pending GPT question about carrying forward generic weapon-proficiency bridges. Its proposed wording is not adopted here.','',
           '| Original identity | Exact printed prerequisite | Normalized requirement |','|---|---|---|']
    for x in output:
        normalized=json.dumps(x['requirements'],ensure_ascii=False,separators=(',',':'))
        lines.append(f"| `{x['id']}` | {x['printedPrerequisite']} | `{normalized}` |")
    lines+=['','The JSON companion retains every complete original object, full operative procedure, explicit current source decision, all twelve class counterpart cards, and all eight unchanged reviewed envelopes.','',
            '[Full source-bound contracts](FEAT_EXACT_01_ACQUISITION_CONTRACTS.json).','']
    manuscript.write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'contracts':info(target),'manuscript':info(manuscript),'counts':result['counts'],'actualActorTestsComplete':False}))

if __name__=='__main__':main()
