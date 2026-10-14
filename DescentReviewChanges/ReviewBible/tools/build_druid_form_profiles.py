"""Build the 26 source-qualified form profiles; no source card is changed."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

# Exact basic attack expressions; qualified riders remain in full sourceProcedure.
ATTACKS={
'wolf-form-striker':('1d8+WIS','piercing'),
'bear-form-tank':('2d6+WIS+1','slashing'),
'hawk-form-scout':('1d4+WIS','slashing'),
'boar-form-brawler':('1d6+WIS','piercing'),
'panther-form-stealth':('2d4+WIS','slashing'),
'dire-wolf':('2d6+WIS','piercing'),
'earth-warden-dire-bear':('1d8+WIS','slashing'),
'sky-serpent':('2d8+WIS','lightning'),
'ironhorn-ram':('1d8+WIS','bludgeoning'),
'shadow-lynx':('2d4+WIS','slashing'),
'blight-elk':('2d8+WIS','piercing'),
'tanglemaw':('2d6+WIS','piercing'),
'beastlord-alpha-animal-hybrid':('2d6+WIS','piercing'),
'mooncursed':('2d6+WIS','piercing'),
'elemental-shapeshifting':('2d8+WIS','chosen-element'),
'tempest-raptor':('2d6+WIS','lightning'),
'thunderhorn-stag':('1d8+WIS','piercing'),
'snow-leopard':('2d6+WIS','cold'),
'frost-wyrmling':('1d8+WIS','cold'),
'carrion-rat-king':('1d8+WIS piercing + 2d6 poison','mixed'),
'insect-broodmother':('1d8+WIS','piercing'),
'master-of-vermin':('S d6+WIS','piercing'),
'charbear':('2d8+WIS','fire'),
'blazewood-stag':('1d8+WIS','piercing')}
MOVES={'wolf-form-striker':{'walk':40},'hawk-form-scout':{'walk':10,'fly':60},
       'panther-form-stealth':{'walk':40},'dire-wolf':{'walk':40},
       'sky-serpent':{'walk':30,'fly':80},'tempest-raptor':{'walk':30,'fly':60},
       'insect-broodmother':{'walk':30,'climb':30}}
AC={'bear-form-tank':('floor',14),'ironhorn-ram':('floor',17),
    'frost-wyrmling':('add',2),'insect-broodmother':('add',3),'elemental-shapeshifting':('fixed',16)}
# Special IDs share one opportunity for their printed modes. A None action is
# an expressly attached rider/entry/crit event, never a new free attack.
SPECIALS={
'dire-wolf':{'howl':('action','surge')},
'earth-warden-dire-bear':{'slam':('action','recharge2')},
'sky-serpent':{'wet':(None,'surge')},
'shadow-lynx':{'blink':('reaction','surge')},
'beastlord-alpha-animal-hybrid':{'howl':('action','surge')},
'mooncursed':{'howl':('action','surge')},
'tempest-raptor':{'wet':(None,'surge')},
'thunderhorn-stag':{'step':('action','surge')},
'frost-wyrmling':{'breath':('action','short-rest'),'ignore-cold-resistance':(None,'surge')},
'carrion-rat-king':{'summon':('action','surge')},
'insect-broodmother':{'spawn':(None,'surge'),'negate-critical':(None,'surge')},
'charbear':{'smoke':('action','surge')},
'blazewood-stag':{'blast':('action','long-rest')}}

def main():
    registry=json.loads((ROOT/'data/playtest/form_temphp_bindings.json').read_text(encoding='utf-8'))
    path=ROOT/'data/playtest/druid_form_profiles.json'
    previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    profiles={}
    for row in registry['bindings']:
        src=row['sourceProcedure']; ident=row['bindingId']; slug=ident.split('.')[-1]
        if not ident.startswith('druid.') or slug not in ATTACKS:continue
        assert src['sourceKind']=='form'
        dice,kind=ATTACKS[slug]; mode,n=AC.get(slug,('normal',0))
        old=previous.get('profiles',{}).get(ident,{})
        if old:assert old['sourceSha256']==row['sourceSha256'],'Review changed source before rebuilding'
        profiles[ident]={
            'sourceId':ident,'sourceSha256':row['sourceSha256'],'sourceProcedure':src,
            'minimumLevel':src['minimumClassLevel'],'circle':src['path'],
            'archAttunement':src['band']=='Arch','canSpeak':src['band']!='Base',
            'size':'Tiny' if slug=='hawk-form-scout' else 'Medium',
            'mayLarge':src['band']=='Hero' or slug in ('bear-form-tank','earth-warden-dire-bear'),
            'movement':MOVES.get(slug,{'walk':30}),'hover':slug=='sky-serpent',
            'ac':{'mode':mode,'amount':n},
            'attack':{'identity':['formAttack','naturalAttack'],'countPerAction':1,'rangeFeet':5,
                      'attack':'PB+WIS','damage':dice,'damageType':kind,
                      'intrinsicallyMagical':slug=='shadow-lynx'},
            'entryBuffer':20 if slug=='bear-form-tank' else 30 if slug=='earth-warden-dire-bear' else 0,
            'specials':{k:{'action':v[0],'payment':v[1]} for k,v in SPECIALS.get(slug,{}).items()},
            'normalSensesRetained':True,'handBasedEquipmentUse':False,
            'integrationStatus':old.get('integrationStatus','DRAFT; implementation review pending'),
            'riderResolution':'Apply exact sourceProcedure through canonical condition/combat engines; not an unrestricted proc list.'}
    assert len(profiles)==26
    out={k:v for k,v in previous.items() if k!='profiles'}
    out.setdefault('status','DRAFT; 26 profiles, implementation review pending')
    out['profiles']=profiles
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Built26 exact-source form profiles; no original source changes.')
if __name__=='__main__':main()
