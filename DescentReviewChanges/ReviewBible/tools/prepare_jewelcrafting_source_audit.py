"""Source-only Jewelcrafting audit; no accessory, charge or cosmology rules authored."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,re,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(x):return {'numerator':x.numerator,'denominator':x.denominator}
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    target=AUDIT/'JEWELCRAFTING_SOURCE_PREPARATION.json';notes=AUDIT/'JEWELCRAFTING_SOURCE_AUDIT.md'
    assert not target.exists() and not notes.exists(),'Existing evidence must be inspected before replacement.'
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';src=read(source);rs=[r for r in src['recipes'] if r['skill']=='Jewelcrafting']
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';equipment=ROOT/'data/playtest/equipment_acquisition_candidate.json'
    before={p.relative_to(GAME).as_posix():sha(p) for p in (source,book,equipment)};protected=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    bindings=[];struct=[];catalysts=[];printed=True;gated_absent=True
    checks=[]
    def check(name,value):checks.append({'name':name,'pass':bool(value)})
    check('All 43 unique Jewelcrafting identities accounted',len(rs)==43 and {r['id'] for r in rs}=={f'recipe-{i}' for i in [*range(241,280),*range(648,652)]})
    check('Visibility remains26 public / one restricted / sixteen Director-only',Counter(r['visibility'] for r in rs)=={'public':26,'restricted':1,'director-only':16})
    for r in rs:
        hits=[i for i,p in enumerate(ps) if p.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];bindings.append({'recipeId':r['id'],'effectMatches':ps[i-4]=='Effect. '+r['effects'],'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:gated_absent &= not hits
        m=r['mechanics'];match=re.fullmatch(r'While worn, grants \+(\d+) to one (.+)-related check or save\. It has (\d+) charges?; expend one to gain advantage on such a roll\. Charges return at dawn\.',r['effects'])
        printed &= bool(match) and int(match[1])==m['bonus'] and match[2]==m['tag'].lower() and int(match[3])==m['charges'] and m['type']=='worn_accessory'
        for i,c in enumerate(r['components']):
            if c['role']=='catalyst':catalysts.append({'recipeId':r['id'],'componentIndex':i,'sourceComponent':c})
        mass=sum((Fraction(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed']),Fraction(0))
        struct.append({'recipeId':r['id'],'quantity':r['quantity'],'maximumYield':3*r['quantity']//2,'sourceConsumedMassLb':ratio(mass),'sourceUnitReferenceGp':ratio(Fraction(r['economy']['recommendedMarketValue'],r['quantity'])),'sourceWorkHours':r['workRequirements']['activeWorkHours'],'sourceTimeMode':r['workRequirements']['timeMode'],'sourceFieldCraftable':r['workRequirements']['fieldCraftable'],'componentRoles':dict(Counter(c['role'] for c in r['components'])),'sourceMaximumCharges':m['charges'],'sourceBonus':m['bonus'],'operativeTag':m['tag']})
    check('All26 public effects match actual V5 paragraphs',len(bindings)==26 and all(b['effectMatches'] for b in bindings))
    check('No gated Jewelcrafting formula appears in public V5',gated_absent)
    check('All43 current effects exactly match tag, bonus, charge and dawn fields',printed)
    check('Every resultItem mechanics object equals current source mechanics',all(r['resultItem']['mechanics']==r['mechanics'] for r in rs))
    components=[c for r in rs for c in r['components']]
    check('All200 source component occurrences are consumed',len(components)==200 and all(c['consumed'] for c in components))
    check('All11 catalyst occurrences retained individually',len(catalysts)==11 and all(z['sourceComponent']['consumed'] for z in catalysts))
    check('No ingredient row is silently treated as a nonconsumed tool',all(c['role']!='tool' for c in components))
    check('All43 fieldCraftable flags false; all actual source hours present',all(r['workRequirements']['fieldCraftable'] is False and r['workRequirements']['activeWorkHours'] is not None for r in rs))
    check('Source charges cover1 through6 without inferred charge improvements',Counter(r['mechanics']['charges'] for r in rs)=={1:15,2:9,3:7,4:5,5:6,6:1})
    check('Every source uses Dexterity or Intelligence and Jeweler facilities',all(r['craftingCheck']['abilityOptions']==['Dexterity','Intelligence'] and r['workRequirements']['station']=="Jeweler's Bench" and r['workRequirements']['requiredTools']==["Jeweler's tools",'Fine files','Magnifying lens'] for r in rs))
    check('Original source, book and equipment files unchanged',all(sha(GAME/p)==h for p,h in before.items()))
    check('All42 current source/rule baseline files unchanged',len(protected)==42 and all(sha(GAME/p)==h for p,h in protected.items()))
    assert all(c['pass'] for c in checks),[c['name'] for c in checks if not c['pass']]
    eq=read(equipment)['items'];matches=[r for r in eq if re.search(r'jewel|gem|ring|amulet|necklace|pendant|crown|tiara|earring|bracelet|brooch|focus|crystal|holy symbol|component pouch|clothes',r['name'],re.I)]
    reference_ids={'arcane-focuses.crystal','holy-symbols.amulet','adventuring-gear.component-pouch','adventuring-gear.signet-ring','adventuring-gear.magnifying-glass','tools.jeweler-s-tools'}
    selected=[r for r in eq if r['id'] in reference_ids or r['id'].startswith('adventuring-gear.clothes-')]
    assert len(selected)==10
    excluded=[r for r in matches if r not in selected]
    out={'status':'Source preparation only; not sent and no operational approval','sourceSha256':sha(source),'bookSha256':sha(book),'equipmentSha256':sha(equipment),'sourceIndices':{r['id']:src['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'families':dict(Counter(r['recipeFamily'] for r in rs)),'operativeTags':dict(Counter(r['mechanics']['tag'] for r in rs)),'recipes':rs,'publicBookBindings':bindings,'structuralAudit':struct,'catalystOccurrences':catalysts,'componentOccurrences':len(components),'componentRoleCounts':dict(Counter(c['role'] for c in components)),'completeEquipmentReferenceRecords':selected,'checks':checks,'sourceInformationDeleted':0,'recipesApproved':0,'cosmology':'Do not derive metaphysical definitions from tags or donor names; careful cosmology review remains after authorized successful push and verified remote commit.'}
    out['equipmentReferenceScope']='Existing comparison records only, not a legal base-model whitelist, enchantment permission or grant of any focus/symbol power. Exact bindings await joint review.'
    out['excludedNameSearchMatches']=[{'reason':'Name-search match only; not selected as a relevant Jewelcrafting body/tool reference. Original equipment record preserved.','sourceEquipmentRecord':r} for r in excluded]
    create(target,json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    text='# Jewelcrafting source audit — internal preparation\n\nThis internal evidence contains restricted and Director-only formulas. It is not a public rule supplement. All43 original records (241–279,648–651) are preserved:26 public, one restricted, sixteen Director-only. All26 public effects match actual V5 paragraphs. Fourteen checks pass with all42 protected source/rule files unchanged. No Jewelcrafting rule has been approved or installed.\n\n## Questions for the source conference\n\n- All43 effects say “while worn” and “+1/+2/+3 to one [tag]-related check or save.” Define what “one” selects or limits, the eligible actor, exact check/save scopes for all14 tags, and timing. Do not infer an unlimited universal bonus, an attack bonus, resistance or a proficiency.\n- Each item grants a finite source maximum of1–6 charges; spending one gives advantage on such a roll. Define declaration timing relative to dice/results, Action/Reaction costs if any, already-present advantage/disadvantage, copied/repeated rolls, interruption and legal refunds. Bonus eligibility and charge spending must remain distinct.\n- Define dawn recharge using the already reviewed campaign time procedure, physical item identity, the actually recorded maximum and one legitimate recharge event. Address underground use, rest, travel, transfer, suppression, breakage, rebuilding and unspent charges without inventing cosmology, planar travel or repeated dawn farming.\n- Resolve active wearing slots and complete bodies for Bracelet, Earring, Crown, Amulet, Ring, Tiara, Necklace, Brooch, Gem and Pendant. Define whether an Earring output is one piece or one matched pair. A loose Gem needs a legal mounted/worn state; carrying it or setting it in a weapon is not automatically “worn.”\n- Account for actual anatomical compatibility, hands, fitting, don/doff and the existing Helm/Gauntlets slots. Wearing numerous rings, bracelets, amulets or brooches must not silently establish unlimited simultaneous bonuses or charge pools.\n- Define combination on one roll with another jewel and existing class/spell/equipment bonuses, including Leatherworking and Tailoring only after their actual decisions. A save can genuinely involve more than one tag; do not grant multiple independent roll events merely to use more charges.\n- Resolve physical identity, required supplemental bodies or stock, reserved order, damaged inputs, latest completion HP, return/recovery, mass, ordinary value and finished-item reference. Source materials and tiny bills do not automatically fund unlimited complete jewelry bodies.\n- The source contains200 consumed component occurrences, including11 actual catalyst rows. Preserve every occurrence and quantity; Masterwork returns at most the framework’s one eligible actual unit. A component’s name, gem category or donor identity cannot relabel its role.\n- Give an explicit quality menu for this charged item family. The source quality labels mention charges, but the reviewed framework defaults only to structural HP and explicitly excludes charge increases. Any replacement charge/property option needs its own precise review; decide the permitted improvement, persistent flaw, maximum/current charge state, recharge and repair interaction. Numerical balance remains separately unapproved.\n- All43 fieldCraftable flags are false despite ten field timeMode labels. All source work-hour values exist. Preserve actual DEX/INT choices, Jeweler’s-tools proficiency, Jeweler’s Bench, Fine files, Magnifying lens, assistants and phase/integration rules.\n- Define trained repair/reconstruction, recoverable-body conditions, DCs, active time, materials and failed work. Repair must not teach a formula, duplicate jewels, refresh spent charges or erase a persistent flaw without explicit reviewed authority.\n- Source charges, bonus and operative tag agree with exact effect prose. Current/legacy names, secondary tags and whole-creature metadata remain preserved evidence; they grant no donor powers, sentience, origin, deity, resistance or other unprinted effect. In particular, Unholy, Vitality, Arcane and donor-name wording require bounded mechanical eligibility without undertaking the deferred cosmology review.\n\n[Complete original records, public paragraph bindings, catalyst rows and checks](JEWELCRAFTING_SOURCE_PREPARATION.json). This evidence is not sent to GPT yet. Leatherworking’s source/interface conference is complete; its44 authored cards are now in exact review. Do not interrupt that active review or treat its pending exact verdict as approval.\n'
    create(notes,text)
    print(json.dumps({'status':'PASS','recipes':43,'publicBindings':26,'checks':len(checks),'componentOccurrences':len(components),'catalystOccurrences':len(catalysts),'equipmentReferences':len(selected),'recipesApproved':0}))
if __name__=='__main__':main()
