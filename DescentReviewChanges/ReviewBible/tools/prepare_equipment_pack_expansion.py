"""Expand source packs for review. Proposed small-item weights remain unapproved."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'

def main():
    d=json.loads((ROOT/'data/playtest/equipment_source_catalog.json').read_text(encoding='utf-8'))
    byname={x['name']:x for x in d['records'] if x['category'] in ['Adventuring gear','Tools']}
    extra={'String (10 feet)':(1,0.02),'Little bag of sand':(1,1),'Small knife':(100,0.25),
           'Alms box':(100,1),'Incense (stick)':(10,0.02),'Censer':(500,1),'Vestments':(100,4)}
    weights={'Bell':0.02,'Candle':0.1,'Ink (1 ounce bottle)':0.1,'Ink pen':0.02,'Paper (one sheet)':0.02,
             'Parchment (one sheet)':0.02,'Perfume (vial)':0.1,'Sealing wax':0.1,'Soap':0.1}
    packs={
      'Burglar':(16,[('Backpack',1),('Ball bearings (bag of 1,000)',1),('String (10 feet)',1),('Bell',1),('Candle',5),('Crowbar',1),('Hammer',1),('Piton',10),('Lantern, hooded',1),('Oil (flask)',2),('Rations (1 day)',5),('Tinderbox',1),('Waterskin',1),('Rope, hempen (50 feet)',1)]),
      'Diplomat':(39,[('Chest',1),('Case, map or scroll',2),('Clothes, fine',1),('Ink (1 ounce bottle)',1),('Ink pen',1),('Lamp',1),('Oil (flask)',2),('Paper (one sheet)',5),('Perfume (vial)',1),('Sealing wax',1),('Soap',1)]),
      'Dungeoneer':(12,[('Backpack',1),('Crowbar',1),('Hammer',1),('Piton',10),('Torch',10),('Tinderbox',1),('Rations (1 day)',10),('Waterskin',1),('Rope, hempen (50 feet)',1)]),
      'Entertainer':(40,[('Backpack',1),('Bedroll',1),('Clothes, costume',2),('Candle',5),('Rations (1 day)',5),('Waterskin',1),('Disguise kit',1)]),
      'Explorer':(10,[('Backpack',1),('Bedroll',1),('Mess kit',1),('Tinderbox',1),('Torch',10),('Rations (1 day)',10),('Waterskin',1),('Rope, hempen (50 feet)',1)]),
      'Priest':(19,[('Backpack',1),('Blanket',1),('Candle',10),('Tinderbox',1),('Alms box',1),('Incense (stick)',2),('Censer',1),('Vestments',1),('Rations (1 day)',2),('Waterskin',1)]),
      'Scholar':(40,[('Backpack',1),('Book',1),('Ink (1 ounce bottle)',1),('Ink pen',1),('Parchment (one sheet)',10),('Little bag of sand',1),('Small knife',1)])}
    result=[]
    for n,(cost,items) in packs.items():
        rr=[]
        for name,qty in items:
            if name in extra: price,weight=extra[name];sid=None;status='new proposed accessory'
            else:
                x=byname[name];price=x['sourcePriceCp'];weight=x['sourceWeightLb'];sid=x['id'];status='source'
                if weight is None:weight=weights[name];status='source item; proposed missing weight'
            rr.append({'name':name,'quantity':qty,'catalogId':sid,'unitPriceCp':price,'unitWeightLb':weight,'status':status})
        result.append({'name':n+"'s Pack",'packagePriceGp':cost,'contents':rr,'proposedGrossWeightLb':round(sum(x['quantity']*x['unitWeightLb'] for x in rr),4),'individualRetailCp':round(sum(x['quantity']*x['unitPriceCp'] for x in rr),4),'containerPlacement':'Not assigned. A pack price grants contents, not capacity exemption or automatically legal placement.'})
    out={'status':'DRAFT for equipment review; no proposed weight approved yet','notice':'Source quantities/prices preserved; includes full waterskins. No extra pack-shell weight. Compare proposals against final GPT review before promoting.','packs':result}
    (AUDIT/'EQUIPMENT_PACK_EXPANSION_DRAFT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print([(x['name'],x['proposedGrossWeightLb'],x['individualRetailCp']/100,x['packagePriceGp']) for x in result])

if __name__=='__main__':main()
