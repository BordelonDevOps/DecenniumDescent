"""Source-only Fishing reconciliation, preserving every formula and access gate."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,re,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(x):return {'numerator':x.numerator,'denominator':x.denominator}
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    target=AUDIT/'FISHING_SOURCE_PREPARATION.json';notes=AUDIT/'FISHING_SOURCE_AUDIT.md'
    assert not target.exists() and not notes.exists(),'Inspect existing source evidence rather than overwrite.'
    paths={'mechanicalV4':ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json','internalV4':GAME/'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json','v2':GAME/'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json','publicRuntime':GAME/'src/data/crafting-recipes.json'}
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';eqpath=ROOT/'data/playtest/equipment_acquisition_candidate.json'
    source=read(paths['mechanicalV4']);rs=[r for r in source['recipes'] if r['skill']=='Fishing'];hashes={k:sha(p) for k,p in paths.items()}
    protected=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    checks=[]
    def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
    check('All44 unique Fishing identities preserved',len(rs)==44 and {r['id'] for r in rs}=={f'recipe-{i}' for i in [*range(160,200),*range(640,644)]})
    check('Visibility28public3restricted13Director-only',Counter(r['visibility'] for r in rs)=={'public':28,'restricted':3,'director-only':13})
    bindings=[];gated_absent=True;prose_exact=True;struct=[]
    for r in rs:
        hits=[i for i,p in enumerate(ps) if p.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];bindings.append({'recipeId':r['id'],'effectMatches':ps[i-4]=='Effect. '+r['effects'],'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:gated_absent &= not hits
        m=r['mechanics'];match=re.fullmatch(r'Grants \+(\d+) to Fishing checks\. On a successful catch, gain (\d+) additional units? of usable meat or material; tagged bait preferentially attracts (.+)-aligned creatures\.',r['effects'])
        prose_exact &= bool(match) and int(match[1])==m['fishingBonus'] and int(match[2])==m['extraYield'] and match[3]==m['attracts'].lower() and m['attracts']==m['tag']
        mass=sum((F(str(c['weight']))*c['quantity'] for c in r['components'] if c['consumed']),F(0))
        struct.append({'recipeId':r['id'],'family':r['recipeFamily'],'quantity':r['quantity'],'maximumYield':3*r['quantity']//2,'sourceConsumedMassLb':ratio(mass),'sourceRecordedConsumedWeightLb':r['economy']['consumedWeight'],'sourceUnitReferenceGp':ratio(F(r['economy']['recommendedMarketValue'],r['quantity'])),'workRequirements':r['workRequirements'],'craftingAbilityOptions':r['craftingCheck']['abilityOptions'],'mechanics':m,'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel']})
    check('All28 public effect paragraphs exactly match V5',len(bindings)==28 and all(b['effectMatches'] for b in bindings))
    check('All16 gated Fishing formulas absent from public V5',gated_absent)
    check('All44 source bonuses extraYield and attraction tags match prose',prose_exact)
    check('Every resultItem duplicates its exact source mechanics',all(r['resultItem']['mechanics']==r['mechanics'] for r in rs))
    comps=[c for r in rs for c in r['components']]
    check('All212 component occurrences are consumed with no catalyst/tool role',len(comps)==212 and all(c['consumed'] and c['role'] not in ('catalyst','tool') for c in comps))
    check('Source component roles independently counted',Counter(c['role'] for c in comps)=={'bait':80,'material':56,'substrate':35,'stabilizer':22,'ingredient':18,'binder':1})
    check('Nine finite source family identities retained',Counter(r['recipeFamily'] for r in rs)=={'Line':9,'Lure':7,'Bait':6,'Net':6,'Trap':5,'Hook':5,'Tackle':3,'Rod':2,'Rig':1})
    check('All source work hours present',all(r['workRequirements']['activeWorkHours'] is not None for r in rs))
    check('Nineteen field flags true and25false retained',Counter(r['workRequirements']['fieldCraftable'] for r in rs)=={True:19,False:25})
    check('WIS Fishing creation tools and station exact',all(r['craftingCheck']['abilityOptions']==['Wisdom'] and r['workRequirements']['station']=='Shoreline, dock, or fishing station' and r['workRequirements']['requiredTools']==['Fishing tackle','Knife','Bait container'] for r in rs))
    versions={}
    for version,p in paths.items():
        d=read(p);versions[version]={r['id']:r for r in (d if isinstance(d,list) else d['recipes'])}
    fields=['name','effects','mechanics','quantity','components','workRequirements','craftingCheck','economy','visibility','discovery'];comparisons=[];diff=[]
    for r in rs:
      for version,rows in versions.items():
        if version=='mechanicalV4' or r['id'] not in rows:continue
        other=rows[r['id']]
        for field in fields:
            same=(field in r)==(field in other) and r.get(field)==other.get(field)
            comparisons.append({'recipeId':r['id'],'version':version,'field':field,'equal':same})
            if not same:diff.append({'recipeId':r['id'],'version':version,'field':field,'currentFieldPresent':field in r,'currentValue':r.get(field),'otherFieldPresent':field in other,'otherValue':other.get(field)})
    check('All44 identities exist in both historical variants',all(all(r['id'] in versions[v] for r in rs) for v in ('internalV4','v2')))
    check('Public runtime source has exact28public Fishing identities',{r['id'] for r in versions['publicRuntime'].values() if r['skill']=='Fishing'}=={r['id'] for r in rs if r['visibility']=='public'})
    check('Only44 missing V2 visibility fields differ among1160comparisons',len(comparisons)==1160 and len(diff)==44 and all(d['version']=='v2' and d['field']=='visibility' and not d['otherFieldPresent'] for d in diff))
    check('All42 protected source and rule files unchanged',len(protected)==42 and all(sha(GAME/p)==h for p,h in protected.items()))
    check('All four compared source files unchanged',all(sha(paths[k])==h for k,h in hashes.items()))
    assert all(c['pass'] for c in checks),[c['name'] for c in checks if not c['pass']]
    eq=read(eqpath)['items'];search=[z for z in eq if re.search('fish|tackle|net|rod|bait|hook|rope|bucket|boat|line|knife|sack',z['name'],re.I)]
    selected=[z for z in search if z['name'] not in ('Rod','Signet ring')];assert len(selected)==9
    excluded=[{'reason':'Name match only: arcane-focus Rod is not automatically a Fishing rod; Signet ring is unrelated substring. Record retained for provenance.','record':z} for z in search if z not in selected]
    out={'status':'PASS — source preparation only; not sent; no Fishing operation approved','sourceSha256':sha(paths['mechanicalV4']),'bookSha256':sha(book),'equipmentSha256':sha(eqpath),'sourceIndices':{r['id']:source['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'families':dict(Counter(r['recipeFamily'] for r in rs)),'tags':dict(Counter(r['mechanics']['tag'] for r in rs)),'recipes':rs,'publicBookBindings':bindings,'structuralAudit':struct,'componentOccurrences':len(comps),'componentRoleCounts':dict(Counter(c['role'] for c in comps)),'fieldFlagCounts':{'true':19,'false':25},'completeEquipmentReferenceRecords':selected,'equipmentReferenceScope':'Existing comparison references only. Net weapon, grapple, rope and block-and-tackle powers do not automatically belong to Fishing outputs; no model whitelist approved.','excludedNameSearchMatches':excluded,'versionAudit':{'sourcePaths':{k:p.relative_to(GAME).as_posix() for k,p in paths.items()},'sourceHashes':hashes,'fields':fields,'comparisons':comparisons,'differences':diff,'fieldComparisons':len(comparisons),'matchingFields':sum(c['equal'] for c in comparisons),'interpretation':'Only absent V2 visibility fields differ; current access boundaries control. Source projection agreement is not live runtime parity.'},'checks':checks,'recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only'}
    create(target,json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    text='''# Fishing source audit — internal preparation

All **44 Fishing formulas** are preserved: 28 public, three restricted and thirteen Director-only. All 28 public effects match the actual V5 paragraphs. Seventeen source checks pass, including 1,160 field comparisons across available source versions; only the 44 V2 records' absent visibility fields differ. No Fishing output or procedure is approved by this audit, and this evidence has not been sent to GPT.

The source contains nine families: Line9, Lure7, Bait6, Net6, Trap5, Hook5, Tackle3, Rod2 and Rig1. Every current effect grants a Fishing-check bonus, an additional usable meat/material unit count after a successful catch, and preferential attraction to its tag. All three printed quantities/tags agree with the numerical fields. That agreement does not establish a playable catch or attraction procedure.

There are **212 consumed component occurrences**, including 80 with role bait; none is a catalyst or nonconsumed tool. Recipe ingredients labeled bait remain distinct from a finished Bait output or bait supplied during a later fishing attempt. Preserve all three physical roles. Actual Fishing tackle, Knife and Bait container are separate work requirements. All source active-hour values exist. Preserve the 19 true and 25 false fieldCraftable flags and their actual station/time-mode conditions.

## Consequential questions for GPT

- Define an actual Fishing attempt: eligible sites/catches, WIS and real tool proficiency, DC, duration, finite opportunities, assistance, maximum simultaneous deployments, fishing watches, interruption, success/failure and retrieval. Crafting these outputs is separate from catching fish; recipe DC/time/quantity is not automatically a fishing-attempt DC/time/catch.
- Define each complete body and output unit for all nine families. Separate consumable bait, reusable lure/hook/line/rod/tackle/net/trap and the Rig using actual source authority or explicitly new decisions. Give mass, price, size, durability, reach/length, fittings, compatible assemblies, load/catch limits and required additional equipment. An arcane-focus Rod, combat Net or Grappling hook grants no implicit Fishing properties.
- Determine exactly when a bonus applies and how several enchanted pieces in one tackle assembly combine. Distinguish assembling, setting, attracting, catching, landing, restraining, killing, processing and harvesting. A fishing bonus is not automatically a combat attack, save, animal-control, stealth or harvesting bonus.
- Preserve all +1/+2/+3 additional-unit values while assigning a finite lawful meaning to a meat/material unit. Specify eligible catch identity, available quantity, mass, donor anatomy, current condition, tier, spoilage, harvesting costs, and whether the effect increases recovery, catches additional available specimens, or does something explicitly different. Do not invent extra unique organs, repeat-catch recovery or a valuable catalog material from an unnamed unit.
- Give preferential attraction a bounded mechanical operation, not an assumed compulsion/summon or guaranteed rare encounter. Record actual local availability and relevant creature/tag eligibility. Names such as Unholy or Psychic require no origin, deity, soul, alignment or cosmology decision at this stage. Attraction, threat and catch eligibility must remain separate.
- Define bait expenditure and remaining-use state for every family, including failed attempts, early retrieval, interrupted work, combat, suppression, item breakage, loss and transfer. Packaging and donor ingredients do not grant unlimited finished bait or hidden recharges.
- Address unattended traps, several anglers, overlapping bait, repeated checks at one depleted site, escaped/live/released catches and catch records shared with harvesting. No physical catch can be counted twice or recycled for new output by release and recapture.
- Honor the reviewed classification: Fishing tackle is a particular non-artisan tool proficiency, so the artisan-only Forge Dwarf creation benefit is not automatically available. Any proposed exception needs a new explicit decision. Keep workshop/Haven/legacy access even where a station string mentions shoreline; a false field flag is not overridden by being near water.
- Specify legal quality options for consumables and durable pieces separately. The reviewed default structural HP improvement does not increase bonus, catch yield, attraction range, charges or market grade. Source quality labels cannot by themselves create those powers. Preserve latest physical damage and actual complete-body/stock conservation.
- Give actual repair/reconstruction and pricing rules only after body classification. Distinguish consumed bait from recoverable durable identity, preserve any persistent flaw, and prevent repair from replenishing consumed fishing resources or refreshing a catch site.
- Keep all original and legacy fields, all 28 exact public bindings and all 16 gated formulas. The existing bestiary/crafting crosslink audit recognizes recipe-173 as one literal source reference; that narrow name match does not establish ingredient availability or a complete ecological link.

The [complete source evidence](FISHING_SOURCE_PREPARATION.json) includes every original record, all paragraphs, comparison differences, component occurrences and nine equipment references. Leatherworking's exact review remains the active joint request. This Fishing preparation does not interrupt it, grant source availability, approve runtime behavior, or undertake the deferred cosmology review.
'''
    create(notes,text)
    print(json.dumps({'status':'PASS','recipes':44,'publicBookBindings':28,'checks':len(checks),'fieldComparisons':len(comparisons),'missingV2Visibility':len(diff),'components':len(comps),'equipmentReferences':len(selected),'recipesApproved':0}))
if __name__=='__main__':main()
