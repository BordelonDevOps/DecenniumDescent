"""Bind every printed ancestry spell grant to its source and actual catalog identity."""
import json
from pathlib import Path
from build_ancestry_background_candidate import slug

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'

def main():
    if (ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json').exists():
        raise SystemExit('Reviewed reference already exists. Preserve it and prepare a separately versioned revision instead of overwriting approved data.')
    evidence=json.loads((AUDIT/'ANCESTRY_BACKGROUND_SOURCE_EVIDENCE.json').read_text(encoding='utf-8'))
    catalog=json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))['spells']
    by_name={s['name'].casefold():s for s in catalog}
    owners={owner['name']:owner for a in evidence['ancestries'] for owner in [a]+a['variants']}
    # owner, source trait, ability, spell:level:recharge:school/rank for new grants
    source_rows=[
      ('River Amphibian','Water Manipulation','WIS',[('Shape Water',1,'at-will'),('Create or Destroy Water',3,'day'),('Water Breathing',5,'day')]),
      ('Umbrin','Umbrin Magic','CHA',[('Dancing Lights',1,'at-will'),('Faerie Fire',3,'day'),('Darkness',5,'day')]),
      ('Cavern Mystic','Earth Communion','WIS',[('Detect Magic',1,'long-rest'),('Speak with Plants',1,'long-rest')]),
      ('Flame Drakari','Fire Affinity','CON',[('Produce Flame',1,'at-will'),('Burning Hands',3,'day')]),
      ('Frost Drakari','Ice Affinity','CON',[('Ray of Frost',1,'at-will'),('Ice Knife',3,'day')]),
      ('Storm Drakari','Lightning Affinity','CON',[('Shocking Grasp',1,'at-will'),('Thunderwave',3,'day')]),
      ('Stone Drakari','Earth Affinity','CON',[('Mold Earth',1,'at-will'),('Earth Tremor',3,'day')]),
      ('Gale Drakari','Air Affinity','CON',[('Gust',1,'at-will'),('Feather Fall',3,'day')]),
      ('Wave Drakari','Water Affinity','CON',[('Shape Water',1,'at-will'),('Create or Destroy Water',3,'day')]),
      ('Twilight Elf','Twilight Magic','CHA',[('Minor Illusion',1,'at-will'),('Disguise Self',3,'day'),('Misty Step',5,'day')]),
      ('Feykin','Fey Magic','CHA',[('Druidcraft',1,'at-will'),('Charm Person',3,'long-rest'),('Misty Step',5,'long-rest')]),
      ('Summer Fey','Touch of Summer','CHA',[('Thorn Whip',1,'at-will'),('Goodberry',3,'day')]),
      ('Winter Fey','Touch of Winter','CHA',[('Ray of Frost',1,'at-will'),('Ice Knife',3,'day')]),
      ('Twilight Fey','Touch of Twilight','CHA',[('Minor Illusion',1,'at-will'),('Sleep',3,'day')]),
      ('Arcanist Gnome','Natural Illusionist','INT',[('Minor Illusion',1,'at-will')]),
      ('Prankster Gnome','Minor Illusion','INT',[('Minor Illusion',1,'at-will')]),
      ('Shaman Orc','Spirit Guide','WIS',[('Guidance',1,'at-will'),('Speak with Animals',3,'day'),('Augury',5,'day')]),
      ('Blood Troll','Blood Magic','CHA',[('Blood Manipulation',1,'at-will'),('False Life',3,'day'),('Vampiric Touch',5,'day')]),
    ]
    supplemental={
      'Create or Destroy Water':('Transmutation',1),'Faerie Fire':('Evocation',1),'Darkness':('Evocation',2),
      'Speak with Plants':('Divination',3),'Produce Flame':('Evocation',0),'Misty Step':('Conjuration',2),
      'Thorn Whip':('Transmutation',0),'Goodberry':('Transmutation',1),'Speak with Animals':('Divination',1),'Blood Manipulation':('Transmutation',0)}
    modes={'Dancing Lights':'Evocation','Detect Magic':'Divination','Feather Fall':'Illusion','Charm Person':'Enchantment'}
    result={'status':'candidate-pending-notebook-review','sourceSha256':evidence['sourceSha256'],
            'grantRoute':'Proposed explicit ancestry route; does not add ordinary class access or an RP pool.',
            'grants':[],'choiceGrants':[],'modifiers':[]}
    for owner,trait,ability,spells in source_rows:
        t=next(t for t in owners[owner]['traits'] if t['name']==trait)
        for name,level,recharge in spells:
            assert name.casefold() in t['text'].casefold(),(name,t)
            entry=by_name.get(name.casefold())
            if entry:
                school=modes.get(name,entry['schools'][0]);ranks={v['rank'] for v in entry['classAccess'].values() if v['school']==school}
                assert len(ranks)==1,(name,ranks)
                rank=ranks.pop();identity=entry['id'];state=entry['status'];identity_type='existing-catalog'
            else:
                school,rank=supplemental[name];identity=slug(name);state='missing-catalog-identity-proposed-supplement';identity_type='new-ancestry-supplement-proposal'
            row={'id':slug(owner)+'--'+identity,'owner':owner,'trait':trait,'sourceLine':t['sourceLine'],
                 'spellId':identity,'spellName':name,'identityType':identity_type,'currentEffectStatus':state,
                 'minimumCharacterLevel':level,'castingAbility':ability,'proposedSchool':school,'rank':rank,
                 'uses':None if recharge=='at-will' else 1,'recharge':recharge}
            if owner=='Cavern Mystic':row['sourceRestriction']='Magic affecting earth/stone only' if name=='Detect Magic' else 'Fungi only'
            result['grants'].append(row)
    wizard_options=[{'spellId':s['id'],'school':s['classAccess']['Wizard']['school'],'currentEffectStatus':s['status']} for s in catalog if s['classAccess'].get('Wizard',{}).get('rank')==0]
    for owner,trait in [('High Elf','Cantrip'),('Lichborn','Arcane Knowledge')]:
        t=next(t for t in owners[owner]['traits'] if t['name']==trait)
        result['choiceGrants'].append({'id':slug(owner)+'--wizard-cantrip-choice','owner':owner,'trait':trait,'sourceLine':t['sourceLine'],
          'choose':1,'minimumCharacterLevel':1,'castingAbility':'INT','rank':0,'recharge':'at-will','options':wizard_options})
    t=next(t for t in owners['Obsidian Highborn']['traits'] if t['name']=='Enhanced Umbrin Magic')
    result['modifiers'].append({'owner':'Obsidian Highborn','trait':t['name'],'sourceLine':t['sourceLine'],'affectedGrantIds':['umbrin--faerie-fire','umbrin--darkness'],'replaceUses':2,'recharge':'day','doesNotBypassLevelGate':True})
    unique={r['spellId']:r for r in result['grants']}
    summary={'fixedGrantRows':len(result['grants']),'choiceGrants':len(result['choiceGrants']),'namedSpellDependencies':len(unique),
             'existingOperational':sum(x['currentEffectStatus']=='operational-playtest-draft' for x in unique.values()),
             'existingUnfinished':sum(x['currentEffectStatus']=='blocked-pending-operational-review' for x in unique.values()),
             'missingNamedSpells':sum(x['identityType']=='new-ancestry-supplement-proposal' for x in unique.values()),
             'wizardCantripChoices':len(wizard_options)}
    assert summary['existingUnfinished']==7 and summary['missingNamedSpells']==10,summary
    result['coverage']=summary
    (ROOT/'data/playtest/ancestry_spell_grants_candidate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (AUDIT/'ANCESTRY_SPELL_DEPENDENCY_AUDIT.json').write_text(json.dumps({'status':'source bindings validated; mechanical approval pending',**summary,'dependencies':list(unique.values())},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))

if __name__=='__main__':main()
