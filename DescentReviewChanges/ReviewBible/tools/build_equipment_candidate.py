"""Build the bounded equipment projection and starting-package reference."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
GUIDE='docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md'

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    if (ROOT/'docs/mechanics/EQUIPMENT_REVIEW_STATUS.json').exists():
        raise SystemExit('Reviewed equipment exists; use an explicit reviewed migration, not draft regeneration.')
    srcp=ROOT/'data/playtest/equipment_source_catalog.json';src=json.loads(srcp.read_text(encoding='utf-8'))
    physical_categories={'Armor and shields','Simple melee weapons','Simple ranged weapons','Martial melee weapons','Martial ranged weapons','Ammunition','Arcane focuses','Druidic focuses','Holy symbols','Alchemical containers','Adventuring gear','Tools'}
    exceptions={'Antitoxin (vial)', 'Perfume (vial)','Poison, basic (vial)','Candle','Sprig of mistletoe','Totem','Emblem','Sealing wax','Soap','Glass vial','Crystal vial','Vial','Ink (1 ounce bottle)'}
    unit_bundles={'Arrows (20)':20,'Blowgun needles (50)':50,'Crossbow bolts (20)':20,'Sling bullets (20)':20,'Spikes, iron (10)':10}
    # Actual source labels are verified below instead of guessed aliases silently succeeding.
    items=[]
    for source in src['records']:
        x=deepcopy(source)
        if x['category'] not in physical_categories or x['name']=='Unarmed strike':continue
        x['status']='authored-awaiting-exact-review'
        x['procedure']=GUIDE
        x['bundleSize']=unit_bundles.get(x['name'],1)
        x['operationalBundleWeightLb']=x['sourceWeightLb']
        x['weightProvenance']='source'
        if x['sourceWeightLb'] is None:
            x['operationalBundleWeightLb']=0.1 if x['name'] in exceptions else 0.02
            x['weightProvenance']='new small-item completion; source null preserved'
        x['unitWeightLb']=x['operationalBundleWeightLb']/x['bundleSize']
        x['unitPriceCp']=x['sourcePriceCp']/x['bundleSize'] if x['sourcePriceCp'] is not None else None
        x['tags']=[]
        if x['name'] in ['Dagger','Club','Light hammer','Handaxe','Crossbow, hand']:x['tags'].append('sidearm')
        x['largeSizingEligible']=x['category']=='Armor and shields' or 'weapons' in x['category']
        if x['name']=='Waterskin':x.update(emptyWeightLb=1,waterCapacityPints=4,sourceWeightIncludesContents=True)
        if x['name'] in ['Acid (vial)',"Alchemist's fire (flask)",'Holy water (flask)','Oil (flask)','Potion of healing']:
            x['sourceWeightIncludesContents']=True
        if x['name'] in ['Antitoxin (vial)','Ink (1 ounce bottle)','Perfume (vial)','Poison, basic (vial)']:
            x['operationalWeightIncludesContents']=True
        if x['name']=="Healer's kit":x.update(chargesWhenFull=10,weightPolicy='Fixed 3 lb regardless of remaining charges; no separate container mass',operationalWeightIncludesContents=True,chargeProcedure='EQUIPMENT_ITEM_PROCEDURES.md#medicine-and-alchemy')
        items.append(x)
    new=[
      ('Repeating heavy crossbow',100,20,'Martial ranged weapon','1d10 piercing; 80/320; Heavy, Two-handed, Ammunition, Repeating 5'),
      ('Kama',2,2,'Simple melee weapon','1d4 slashing; Light'),
      ('Nunchaku',2,2,'Simple melee weapon','1d4 bludgeoning; Light'),
      ('Religious implements',5,2,'Tool','Ordinary religious practice kit; no automatic consecrated focus'),
      ('Arcana tools',25,3,'Tool','Ordinary analysis implements'),
      ('Divination tools',15,2,'Tool','Ordinary cards/tokens; no future knowledge'),
      ('Survival tools',5,5,'Tool','Field knife, cord and repair implements; no free food'),
      ("Siege engineer's kit",50,15,'Tool','Measuring/assembly implements, not a siege engine'),
      ('Divination token',1,.1,'Focus','Oracle class focus'),
      ('Class token',5,.1,'Focus','Record one eligible casting class; no ancestry substitution'),
      ('String (10 feet)',.01,.02,'Accessory','Ordinary string'),
      ('Little bag of sand',.01,1,'Accessory','Ordinary sand; includes its bag'),
      ('Small knife',1,.25,'Accessory','Tool, not automatic dagger'),
      ('Alms box',1,1,'Accessory','Ordinary receptacle'),
      ('Incense block',.1,.02,'Accessory','Finite ordinary incense, no focus effect'),
      ('Censer',5,1,'Accessory','Ordinary incense burner'),
      ('Vestments',1,4,'Clothing','Ordinary religious clothing'),
      ('Journal',1,1,'Accessory','Also ledger/notebook'),
      ('Compass',5,.25,'Accessory','Ordinary direction, no check bonus'),
      ('Hooded cloak',1,2,'Clothing','Ordinary clothing'),
      ('Small document',None,.02,'Narrative accessory','One map, letter, rubbing, false paper or prophecy fragment; no automatic sale value'),
      ('Small narrative token',None,.1,'Narrative accessory','One trinket/insignia/charm/small relic; retain description, no automatic power or sale value'),
      ('Dried herb and flower collection',None,.5,'Ingredient bundle','Finite bundle; not automatic specific recipe ingredient or endless remedy material'),
      ('Broken manacle',None,3,'Narrative accessory','Unusable restraint fragment'),
      ('Celestial Emissary dim-light reliquary',5,2,'Source-specific accessory','Holy Symbol Reliquary physical profile; dim light 5 feet while in darkness; no further power'),
    ]
    for name,gp,weight,category,effect in new:
        items.append({'id':'new.'+slug(name),'name':name,'category':category,'status':'authored-awaiting-exact-review',
          'sourceLine':None,'sourceFields':None,'sourcePriceCp':None,'sourceWeightLb':None,'bundleSize':1,
          'unitPriceCp':gp*100 if gp is not None else None,'unitWeightLb':weight,'operationalBundleWeightLb':weight,
          'weightProvenance':'new conference completion','profile':effect,'procedure':GUIDE,'tags':[],
          'largeSizingEligible':'weapon' in category.lower()})
    names={}
    for x in items:names.setdefault(x['name'],[]).append(x)
    def find(name,category=None):
        choices=[x for x in names.get(name,[]) if category is None or x['category']==category]
        if len(choices)!=1:raise ValueError(('ambiguous/missing item',name,category,[x['id'] for x in choices]))
        return choices[0]
    def item(name,qty=1,**kw):
        x=find(name)
        if x['category']=='Ammunition':
            assert qty%x['bundleSize']==0, 'Starter kits grant complete retail ammunition bundles'
            return {'itemId':x['id'],'quantity':qty//x['bundleSize'],'grantedUnits':qty,**kw}
        return {'itemId':x['id'],'quantity':qty,**kw}
    def units(ref):return ref.get('grantedUnits',ref['quantity'])
    def describe(ref):
        x=byid[ref['itemId']]
        if 'grantedUnits' in ref:
            return str(ref['grantedUnits'])+' '+re.sub(r'\s*\(\d+\)','',x['name']).lower()
        return (str(ref['quantity'])+' × ' if ref['quantity']!=1 else '')+x['name']
    # All ammunition quantities below are individual projectiles, not retail bundles.
    ammo=[x for x in items if x['category']=='Ammunition']
    for x in ammo:
        m=re.search(r'\((\d+)\)',x['name'])
        if not m:raise ValueError(('unparsed ammunition bundle',x['name']))
        size=int(m[1]);x['bundleSize']=size;x['unitWeightLb']=x['operationalBundleWeightLb']/size;x['unitPriceCp']=x['sourcePriceCp']/size
    arrows=next(x['name'] for x in ammo if 'Arrows' in x['name'])
    bolts=next(x['name'] for x in ammo if 'bolts' in x['name'].lower())
    packs=json.loads((AUDIT/'EQUIPMENT_PACK_EXPANSION_DRAFT.json').read_text(encoding='utf-8'))['packs']
    packrecords=[]
    for p in packs:
        contents=[]
        for row in p['contents']:
            name='Incense block' if row['name']=='Incense (stick)' else row['name']
            contents.append(item(name,row['quantity']))
        packrecords.append({'id':'pack.'+slug(p['name'].replace("'s Pack",'')), 'name':p['name'],
            'priceCp':p['packagePriceGp']*100,'contents':contents,
            'status':'authored-awaiting-exact-review','placement':'Record actual legal container/attachment positions; no capacity waiver'})
    packby={x['id']:x for x in packrecords}; byid={x['id']:x for x in items}
    for p in packrecords:
        p['grossWeightLb']=round(sum(byid[x['itemId']]['unitWeightLb']*units(x) for x in p['contents']),5)
    # Structured actual choices, not duplicate grants or random default selections.
    classes={
      'Bard':(['Leather','Dagger','Flute'],'Entertainer'),
      'Cleric':(['Scale mail','Mace','Shield','Amulet'],'Priest'),
      'Crimson Agent':(['Leather','Shortsword',('Dagger',2),"Thieves' tools",'Class token'],'Burglar'),
      'Dragoon':(['Scale mail','Glaive',('Javelin',3),'Class token'],'Explorer'),
      'Druid':(['Leather'],'Explorer'),
      'Mage':(['Quarterstaff','Dagger','Wand'],'Scholar'),
      'Mirrorsage':(['Leather','Shortsword','Crossbow, hand',(bolts,20),'Mirror, steel'],'Explorer'),
      'Monk':(['Quarterstaff',('Dart',10),'Class token'],'Explorer'),
      'Oracle':(['Leather','Mace','Divination token'],'Priest'),
      'Paladin':(['Chain mail','Longsword','Shield',('Javelin',5),'Amulet'],'Priest'),
      'Ranger':(['Leather','Longbow',(arrows,20),'Shortsword','Totem'],'Explorer'),
      'Shaman':(['Leather','Spear','Totem','Herbalism kit'],'Explorer'),
      'Soldier':(['Chain mail','Repeating heavy crossbow',(bolts,20),'Dagger','Shield'],'Dungeoneer'),
      'Thief':(['Leather','Shortsword',('Dagger',2),"Thieves' tools",'Class token'],'Burglar'),
      'Tinker':(['Leather','Crossbow, light',(bolts,20),"Tinker's tools",'Class token'],'Explorer'),
      'Warrior':(['Hide','Greataxe',('Trident',2)],'Explorer'),
      'Wizard':(['Quarterstaff','Dagger','Wand','Spellbook'],'Scholar')}
    kitrecords=[]
    for cls,(kit,pack) in classes.items():
        contents=[]
        for entry in kit:
            name,qty=entry if isinstance(entry,tuple) else (entry,1)
            kw={'forClass':slug(cls)} if name=='Class token' else {}
            contents.append(item(name,qty,**kw))
        choices=[]
        if cls=='Druid':
            simple=[x for x in items if x['category'] in ['Simple melee weapons','Simple ranged weapons','Simple melee weapon']]
            choices=[{'id':'druid.first-weapon-or-shield','choose':1,'options':[item('Shield',material='wood')]+[{'itemId':x['id'],'quantity':1} for x in simple]},
                     {'id':'druid.melee-weapon','choose':1,'options':[item('Scimitar')]+[{'itemId':x['id'],'quantity':1} for x in simple if 'melee' in x['category']]},
                     {'id':'druid.focus','choose':1,'options':[{'itemId':x['id'],'quantity':1} for x in items if x['category']=='Druidic focuses']}]
        packid='pack.'+slug(pack)
        weight=sum(byid[x['itemId']]['unitWeightLb']*units(x) for x in contents)+packby[packid]['grossWeightLb']
        kitrecords.append({'class':cls,'contents':contents,'packId':packid,'choices':choices,
          'fixedWeightBeforeChoicesBackgroundSizingLb':round(weight,5),
          'source':'Player V6 lines 2407–2411' if cls=='Druid' else 'Player example line123 plus new completion' if cls=='Tinker' else 'new conference-authored kit',
          'notes':'No proficiency/feature/free refill grant. Wealth replaces this kit AND background physical items/money. Check actual carrying and fit. Repeating magazine starts empty.'})
    bg=json.loads((ROOT/'data/playtest/ancestry_background_candidate.json').read_text(encoding='utf-8'))['backgrounds']
    mappings={
      'aethel-city-guard-veteran':'Uniform insignia uses small narrative token unless an actual larger item is chosen; map uses small document; common clothes, manacles, pouch and coins use named catalog items.',
      'rift-scarred-survivor':'Trinket and luck amulet use small narrative tokens; map uses small document; traveler clothes and coins retain their named profiles.',
      'disgraced-noble-scion':'Fine clothes and signet ring retain normal profiles; letter uses small document; purse uses pouch. Source worn appearance alone does not invent mechanical damage.',
      'wildling-herbalist':'Herbalism kit; carved staff uses quarterstaff; one finite dried-herb/flower bundle; common clothes, pouch and coins.',
      'guild-artisan-dropout':'Select one actual artisan-tool item. Retain best-work sample description and choose its actual comparable profile, with no inferred hidden power. Letter, traveler clothes, pouch and coins use normal profiles.',
      'seeker-of-the-lost-pantheon':'Rubbing uses small document; myth book uses Book; select an ordinary holy-symbol profile; common clothes and coins. New candidate quantity completion: one incense block; no unlimited incense.',
      'marked-fugitive':'Broken manacle is a 3-lb unusable fragment; false papers use small documents; mark/scar is a body description, not extra carried inventory; mixed coins use actual denominations totaling10gp.',
      'expedition-cartographer':'Cartographer tools; new candidate quantity completion: three blank parchment sheets and three partially completed map documents; compass, traveler clothes, pouch and coins use normal profiles.',
      'arcane-academy-dropout':'Choose Spellbook OR one actual Arcane Focus. It retains normal equipment function but no free spells. Letter, common clothes, student robe=Robes, pouch and coins.',
      'cult-escapee':'Symbol uses small narrative token unless an actual holy symbol is explicitly chosen and fitted; disguise kit, journal, common clothes, pouch and coins use normal profiles.',
      'planar-merchant':'Small trinket keeps description but no inferred magic or automatic resale value; ledger=Journal; fine clothes, merchant scale, pouch and coins use normal profiles.',
      'battlefield-medic':'Full healer kit; bandana/token uses an appropriate small narrative accessory; journal, common clothes, pouch and coins.',
      'dimensional-refugee':'Record actual approximate size/weight of the strange device/artifact, with no functional or market/artifact mechanics before identification. Unusual clothing uses an actual comparable clothes profile; journal, pouch and coins retain normal profiles.',
      'relic-hunter':'Small authentic relic retains source description and small narrative-token profile without invented powers; reference book=Book; magnifying glass, traveler clothes, pouch and coins.',
      'corruption-survivor':'Holy-symbol option uses actual symbol profile with its normally permitted focus interface; charm option is narrative token. Purified-water vial is actual water in a real vial, not holy water. Journal, common clothes, pouch and coins.',
      'frontier-settler':'Select one actual ordinary mundane tool/weapon profile; no proficiency is gained. Map and community token retain ordinary accessory profiles; common clothes, pouch and coins.',
      'prophecy-bearer':'Prophecy document uses small document; birthmark/physical feature has no separate inventory weight. Symbolic item uses an appropriate actual ordinary profile with no invented power. Traveler clothes, pouch and coins.',
      'underworld-escapee':'Memento retains description and an appropriate narrative physical profile; disguise kit, common clothes, hooded cloak, pouch and coins use normal profiles.',
      'elemental-touched':'Descriptive elemental focus is an actual token/material/container, not automatic spellcasting F. Motif clothing uses an actual comparable clothes profile; journal, pouch and coins.',
      'celestial-emissary':'Choose actual holy symbol OR narrative celestial token; ceremonial clothes=Clothes costume; additional dim-light reliquary uses its exact source-specific profile; journal, pouch and coins.'}
    # Refuse an overlooked background instead of silently labeling all twenty complete.
    for b in bg:
        if b['id'] not in mappings:raise ValueError(('background mapping missing',b['id']))
    bgrows=[{'id':b['id'],'name':b['name'],'sourceEquipment':b['equipmentSource'],'physicalMapping':mappings[b['id']],
       'notes':'Preserve all description and every actual item. Make and record actual source choices/unspecified finite quantities at creation; no automatic spells/proficiency.'} for b in bg]
    out={'schemaVersion':'1.0','status':'AUTHORED EQUIPMENT CANDIDATE — exact manuscript review pending',
       'proceduralAuthority':GUIDE,'sourceCatalogSha256':hashlib.sha256(srcp.read_bytes()).hexdigest(),
       'conferenceTurnId':'2e6b4aa3-d9e7-4983-9ef3-a3ca4f3da037','cosmology':'deferred until successful authorized push and verified remote commit',
       'unitPolicy':'Source price/weight for printed retail bundle preserved. In ammunition references quantity counts retail bundles and grantedUnits is the explicit individual projectile count; use grantedUnits for derived per-projectile weight/value arithmetic. unitPriceCp/unitWeightLb do not guarantee fractional retail purchases. Other pack/kit references count actual named item units. A bag/kit/flask gross weight covers its actual contents once; healer-kit weight stays3lb regardless of charges.',
       'items':items,'packs':packrecords,'classKits':kitrecords,'backgrounds':bgrows,
       'openScope':['687 full recipe procedures','harvesting and preservation','vehicles and mounted combat','artifact and faction economy','runtime inventory execution','human balance'],
       'sourceReferenceOnlyCategories':[c for c in sorted({x['category'] for x in src['records']}) if c not in physical_categories]}
    dump(ROOT/'data/playtest/equipment_acquisition_candidate.json',out)
    md=['# Starting equipment and packs','', '**AUTHORED PLAYTEST CANDIDATE — exact manuscript review pending.** Use with the [equipment guide](EQUIPMENT_ACQUISITION_PLAYTEST.md) and [item procedures](EQUIPMENT_ITEM_PROCEDURES.md).','',
        'Choose the actual class and background packages, or the reviewed starting-wealth route. Wealth replaces both physical packages and all package money, without removing background training, standing or features. Fixed packages grant no proficiency or unselected feature. Record actual choices, quantities, fitted size, custody, ammunition and container placement. Check pounds and Load after every source is included.','',
        '## Class packages','', '| Class | Fixed contents and pack | Weight before choices, background and sizing |','|---|---|---:|']
    for k in kitrecords:
        desc=', '.join(describe(x) for x in k['contents'])
        if k['class']=='Druid':desc+='; wooden shield OR any simple weapon; scimitar OR any simple melee weapon; one druidic focus'
        desc+='; '+packby[k['packId']]['name']
        md.append(f"| {k['class']} | {desc} | {k['fixedWeightBeforeChoicesBackgroundSizingLb']:g} lb |")
    md += ['', 'The Druid package is preserved Player source; its choices add their actual weights to the fixed subtotal. The Tinker package completes the source example’s undefined basic supplies with Explorer’s Pack. Other kits are new conference decisions. Warrior’s two tridents replace the proposal’s unproficient handaxes. Staff means quarterstaff. Ammunition counts are individual units even when the source sells bundles.', '',
        'Soldier’s repeating crossbow magazine begins empty until actually loaded. Shield and crossbow may be used together only with the actual Shield Trained permission. Wizard’s book contains only its actual reviewed class spell entitlement. A selected Druid simple weapon supplies no missing proficiency or unlisted ammunition.', '',
        'Fixed Large-sized armor/shields/weapons are included without an added creation payment, at the guide’s doubled mass and later baseline value. A kit may exceed capacity or the Burdened threshold; legally store, transfer or carry it using actual resources. Do not silently delete items, create a porter or waive encumbrance.', '',
        '## Seven source packs','', 'A pack has exactly its listed contents and price. Gross weight includes its actual backpack/chest and full waterskin where named; there is no extra pack shell. Arrange real container/attachment positions within capacities. Source package price need not equal individual retail prices.','']
    for p in packrecords:
        md += ['### '+p['name'],'',f"**Price:** {p['priceCp']/100:g} gp. **Gross weight:** {p['grossWeightLb']:g} lb.",'',
          ', '.join(describe(x) for x in p['contents'])+'.','']
    md += ['Priest’s Pack contains two **blocks** of incense, preserving the source unit. Small-item weights and missing accessory profiles are new completions, not recovered book weights.','',
       '## Background equipment','', 'Every original equipment field is retained below. Existing named items keep their ordinary equipment function without granting training, spells, recipes, attunement or hidden properties. Record actual choices and finite quantities for descriptions such as “several”; a character sheet cannot leave carried quantities infinite or blank. Documents and oddities preserve their narrative information.','']
    for b in bgrows:
        md += ['### '+b['name'],'','**Preserved source package:** '+b['sourceEquipment'],'','**Physical mapping:** '+b['physicalMapping'],'']
    md += ['The Dimensional Refugee’s unusual object remains a possession with an actual recorded physical profile, not an automatically identified artifact. Celestial Emissary’s particular reliquary has only its source-specific dim-light procedure. No origin, cross-plane or cosmology ruling is made here.','']
    (ROOT/'docs/mechanics/EQUIPMENT_STARTING_PACKAGES.md').write_text('\n'.join(md),encoding='utf-8')
    print(json.dumps({'items':len(items),'newItems':len(new),'packs':len(packrecords),'classKits':len(kitrecords),'backgrounds':len(bgrows),'ammo':[(x['name'],x['bundleSize']) for x in ammo]}))

if __name__=='__main__':main()
