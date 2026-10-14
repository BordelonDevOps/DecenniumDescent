"""Preserve all Tailoring sources and public-book bindings; grants no approval."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,re,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ratio(n):return {'numerator':n.numerator,'denominator':n.denominator}
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    paths=[AUDIT/'TAILORING_SOURCE_PREPARATION.json',AUDIT/'TAILORING_SOURCE_AUDIT.md']
    assert not any(p.exists() for p in paths),'Inspect existing evidence instead of overwriting.'
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';src=read(source);rs=[r for r in src['recipes'] if r['skill']=='Tailoring']
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';equipment=ROOT/'data/playtest/equipment_acquisition_candidate.json'
    protected=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files'];before={str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in (source,book,equipment)}
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    checks=[]
    def check(name,value):checks.append({'name':name,'pass':bool(value)})
    check('All 43 distinct Tailoring identities accounted',len(rs)==43 and {r['id'] for r in rs}=={f'recipe-{i}' for i in [*range(546,585),*range(680,684)]})
    check('Original visibility is 29 public / four restricted / ten Director-only',Counter(r['visibility'] for r in rs)=={'public':29,'restricted':4,'director-only':10})
    bindings=[];gated_absent=True;effects_match=True;struct=[];numeric=True
    for r in rs:
        hits=[i for i,p in enumerate(ps) if p.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];effects_match &= ps[i-4]=='Effect. '+r['effects']
            bindings.append({'recipeId':r['id'],'effectMatches':ps[i-4]=='Effect. '+r['effects'],'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:gated_absent &= not hits
        m=r['mechanics']
        if m['type']=='container':
            match=re.fullmatch(r'Creates a fitted container holding (\d+) pounds without counting against normal encumbrance; \+(\d+) to checks to conceal or organize its contents\.',r['effects'])
            numeric &= bool(match) and int(match[1])==m['capacityPounds'] and int(match[2])==m['bonus']
        else:
            match=re.fullmatch(r'Creates a tailored (.+) granting \+(\d+) to a related social, stealth, or environmental check(?: and resistance to (\w+) damage)?\.',r['effects'])
            numeric &= bool(match) and int(match[2])==m['skillBonus'] and match[3]==m['resistance']
        mass=sum((Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed']),Fraction(0))
        struct.append({'recipeId':r['id'],'quantity':r['quantity'],'maximumYield':3*r['quantity']//2,'sourceConsumedMassLb':ratio(mass),'sourceUnitReferenceGp':ratio(Fraction(r['economy']['recommendedMarketValue'],r['quantity'])),'componentRoles':dict(Counter(c['role'] for c in r['components'])),'sourceWorkHours':r['workRequirements']['activeWorkHours'],'sourceTimeMode':r['workRequirements']['timeMode'],'sourceFieldCraftable':r['workRequirements']['fieldCraftable']})
    check('All 29 public effects exactly match real V5 paragraphs',len(bindings)==29 and effects_match)
    check('No gated Tailoring formula appears in the public book',gated_absent)
    check('Five containers and 38 garment effects retain exact numerical prose',Counter(r['mechanics']['type'] for r in rs)=={'container':5,'garment':38} and numeric)
    check('All 43 resultItem mechanics equal current recipe mechanics',all(r['resultItem']['mechanics']==r['mechanics'] for r in rs))
    components=[c for r in rs for c in r['components']]
    check('190 occurrences preserve 165 consumed inputs and 25 reusable tools',len(components)==190 and sum(c['consumed'] for c in components)==165 and all(c['consumed']==(c['role']!='tool') for c in components))
    check('All 25 nonconsumed tools retain their actual rows; no source catalyst exists',sum(c['role']=='tool' for c in components)==25 and all(c['role']!='catalyst' for c in components))
    check('All source fieldCraftable flags stay false',all(r['workRequirements']['fieldCraftable'] is False for r in rs))
    check('Only recipe 584 has null source active hours',[r['id'] for r in rs if r['workRequirements']['activeWorkHours'] is None]==['recipe-584'])
    check('No source armor bonus field exists to infer AC from a garment',all('armorBonus' not in r['mechanics'] for r in rs))
    check('Seven printed resistance records retained',sum(bool(r['mechanics'].get('resistance')) for r in rs)==7)
    equip=read(equipment)['items'];selected=[r for r in equip if re.search(r'clothes|rope|sack|pouch|bag|backpack|blanket|bedroll|tent|climber|weaver|tailor|disguise',r['name'],re.I)]
    check('Original source, book and equipment bytes unchanged',all(sha(GAME/p)==h for p,h in before.items()))
    check('All 42 current source/rule baseline files unchanged',len(protected)==42 and all(sha(GAME/p)==h for p,h in protected.items()))
    assert all(c['pass'] for c in checks),[c['name'] for c in checks if not c['pass']]
    out={'status':'Source preparation only; not sent to GPT; no operational cards approved','sourceSha256':sha(source),'bookSha256':sha(book),'equipmentSha256':sha(equipment),'sourceIndices':{r['id']:src['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'effectTypes':dict(Counter(r['mechanics']['type'] for r in rs)),'families':dict(Counter(r['recipeFamily'] for r in rs)),'recipes':rs,'publicBookBindings':bindings,'structuralAudit':struct,'completeEquipmentReferenceRecords':selected,'componentOccurrences':len(components),'sourceComponentRoles':dict(Counter(c['role'] for c in components)),'checks':checks,'sourceOriginalsChanged':0,'recipesApproved':0,'cosmology':'Deferred until authorized push and verified remote commit.'}
    create(paths[0],json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    notes='# Tailoring source audit — internal preparation\n\nContains restricted and Director-only formula evidence. This is a source audit, not a reviewed gameplay supplement or a public export.\n\nAll 43 original records (546–584, 680–683) are retained intact: 29 public, four restricted and ten Director-only. Every public effect matches its actual V5 paragraph. The source has five containers and 38 garments across nine families. Fourteen checks pass; all 42 protected current source/rule files are unchanged. Nothing has been sent to GPT or approved for this new operational pass.\n\n## Questions requiring joint review\n\n- Complete Bag bodies need finite physical capacity, volume, closure, price, weight, structure and fit. Source relief is 10/30/40/50 lb; it must interact explicitly with Leatherworking, printed Inventory Load, nesting, suppression, breakage and melding. Leatherworking’s pending conference is a dependency, not established authority.\n- Define exact social, stealth and environmental check eligibility for each garment family, actor and task. No source says universal skill, saving-throw, attack, AC, Speed or environmental-immunity bonus. Establish combination with other garments and Leatherworking on the same check.\n- Define one complete output body and actual benefit slots for Cloak, Gloves pair, Hat, Garment, Robe, Cord, Veil and Mantle. Gloves interact with Blacksmithing’s reviewed Gauntlets slot; Hats with the Helm slot. Clothing, coats, robes, cloaks and armor require explicit layer/slot compatibility rather than unlimited worn bonuses.\n- Recipe-680 is named Climbing Cord but its current effect type is garment and its printed benefit is a related social/stealth/environmental check bonus. A rope length, carrying capacity, harness function, climbing proficiency or new action cannot be supplied solely by its name. Resolve that physical-use binding explicitly.\n- Recipe-681’s Veilcloth needs a concrete wearable veil profile. Recipe-682’s Shadow Cloak grants no invisibility, darkness or acid resistance. Recipe-683’s Living Mantle grants poison-damage resistance, not immunity to Poisoned or donor abilities.\n- Seven garments have printed resistance, including one bludgeoning resistance. Give actual-wearing, functional, suppression and meld predicates without inventing an AC bonus, damage scope limitation or automatic climate immunity.\n- Tiny component bills do not automatically fund multiple complete bodies. Specify supplemental bodies or sufficient separately quantified stock, ordered maximum-yield reserves, current HP snapshot, legal replacements, flaws, durability and exact return/recovery at every outcome. Preserve every ingredient occurrence.\n- The 190 component occurrences comprise 165 consumed inputs and 25 nonconsumed tools (Needle, Scissors and Measuring tools). Preserve every exact tool occurrence, source tier and price, including tier-10 54,000-gp tool references. Reuse is not duplication, consumption or ingredient recovery. Resolve how these source tool rows relate to required Needles/Shears and the kit/station without silently substituting a cheap ordinary tool for a specified profile. No source catalyst exists, so Masterwork cannot return an ingredient by relabeling it.\n- All fieldCraftable flags are false; contradictory field timeMode labels remain preserved. Recipe-584 has null hours and a one-year label; any 1,920-hour overlay must be separately identified under the reviewed framework. Confirm artisan Forge Dwarf work/phase effects without extending them to repair.\n- Establish trained repair/reconstruction, recoverable-body conditions, finite materials and prices, failure and suppression behavior. Preserve source batch reference, divide by source Q once, then separately account for actual supplemental bodies. Titles do not grant equipment grade or artifact classification.\n\n[Complete source, paragraph bindings and audit evidence](TAILORING_SOURCE_PREPARATION.json). Original legacy names/effects, source statuses, needsReview flags, access and optional guidance remain unchanged. No source deletion, runtime change, approval or cosmology review occurred.\n'
    create(paths[1],notes)
    print(json.dumps({'status':'PASS','recipes':43,'publicBindings':29,'checks':len(checks),'componentOccurrences':len(components),'equipmentReferences':len(selected),'recipesApproved':0}))
if __name__=='__main__':main()
