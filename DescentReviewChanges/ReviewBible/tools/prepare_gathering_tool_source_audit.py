"""Joint source evidence for Mining, Skinning and Salvaging tool interfaces.

No tool effects, quality steps or missing yield clauses are approved here.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,re,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
TRADES=('Mining','Skinning','Salvaging')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(x):return {'numerator':x.numerator,'denominator':x.denominator}
def create(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    target=AUDIT/'GATHERING_TOOL_SOURCE_PREPARATION.json';notes=AUDIT/'GATHERING_TOOL_SOURCE_AUDIT.md'
    assert not target.exists() and not notes.exists(),'Inspect existing evidence first.'
    paths={'mechanicalV4':ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json','internalV4':GAME/'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json','v2':GAME/'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json','publicRuntime':GAME/'src/data/crafting-recipes.json'}
    hashes={k:sha(p) for k,p in paths.items()};source=read(paths['mechanicalV4']);rs=[r for r in source['recipes'] if r['skill'] in TRADES]
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';ps=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    checks=[]
    def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
    check('128 unique Mining43 Skinning43 Salvaging42 records',len(rs)==128 and Counter(r['skill'] for r in rs)=={'Mining':43,'Skinning':43,'Salvaging':42} and len({r['id'] for r in rs})==128)
    check('82public6restricted40Director-only boundary',Counter(r['visibility'] for r in rs)=={'public':82,'restricted':6,'director-only':40})
    bindings=[];omissions=[];struct=[];gated_absent=True;bonuses_ok=True;quality_ok=True;percent_ok=True
    for r in rs:
        hits=[i for i,p in enumerate(ps) if p.startswith('Formula ID: '+r['id']+' ')]
        if r['visibility']=='public':
            assert len(hits)==1,(r['id'],hits)
            i=hits[0];bindings.append({'recipeId':r['id'],'effectMatches':ps[i-4]=='Effect. '+r['effects'],'paragraphs':[{'index':j,'text':ps[j]} for j in range(i-5,i+1)]})
        else:gated_absent &= not hits
        m=r['mechanics'];bonus_field={'Mining':'miningBonus','Skinning':'skinningBonus','Salvaging':'salvageBonus'}[r['skill']]
        bonuses_ok &= r['effects'].startswith(f"Grants +{m[bonus_field]} to {r['skill']} checks")
        quality_ok &= bool(m['qualityStep'])==('one quality step' in r['effects'])
        if r['skill']=='Salvaging':percent_ok &= f"up to {m['recoveryPercent']}%" in r['effects']
        if m.get('extraYield',0)>0 and f"{m['extraYield']} additional" not in r['effects']:
            omissions.append({'recipeId':r['id'],'trade':r['skill'],'visibility':r['visibility'],'field':'mechanics.extraYield','numericValue':m['extraYield'],'preservedEffect':r['effects'],'resultItemField':r['resultItem']['mechanics'].get('extraYield'),'disposition':'Unresolved; no numeric yield adopted or discarded by this source audit.'})
        consumed=[c for c in r['components'] if c['consumed']]
        mass=sum((F(str(c['weight']))*c['quantity'] for c in consumed),F(0))
        struct.append({'recipeId':r['id'],'trade':r['skill'],'family':r['recipeFamily'],'quantity':r['quantity'],'maximumYield':3*r['quantity']//2,'sourceConsumedMassLb':ratio(mass),'sourceUnitReferenceGp':ratio(F(r['economy']['recommendedMarketValue'],r['quantity'])),'sourceWorkRequirements':r['workRequirements'],'abilityOptions':r['craftingCheck']['abilityOptions'],'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel'],'mechanics':m})
    check('All82 public effects exactly match actual book paragraphs',len(bindings)==82 and all(b['effectMatches'] for b in bindings))
    check('All46 gated formulas absent from public V5',gated_absent)
    check('Every128 trade bonus is printed exactly',bonuses_ok)
    check('Quality-step flag matches printed clause for all128',quality_ok)
    check('All42 Salvaging recovery percentages printed exactly',percent_ok)
    check('Exactly25 positive extraYield1 omissions preserved',len(omissions)==25 and all(o['numericValue']==1 and o['resultItemField']==1 and o['trade'] in ('Mining','Skinning') for o in omissions))
    check('All resultItem mechanics match primary source',all(r['resultItem']['mechanics']==r['mechanics'] for r in rs))
    components=[{'recipeId':r['id'],'trade':r['skill'],'componentIndex':i,'sourceComponent':c} for r in rs for i,c in enumerate(r['components'])]
    tools=[c for c in components if c['sourceComponent']['role']=='tool'];used_tools=[c for c in tools if c['sourceComponent']['consumed']];reusable=[c for c in tools if not c['sourceComponent']['consumed']];catalysts=[c for c in components if c['sourceComponent']['role']=='catalyst']
    check('580 component occurrences,213 reusable tool rows,12 consumed tool rows',len(components)==580 and len(reusable)==213 and len(used_tools)==12)
    check('Ten real consumed catalyst rows retained',len(catalysts)==10 and all(c['sourceComponent']['consumed'] for c in catalysts))
    check('All source work-hour values present',all(r['workRequirements']['activeWorkHours'] is not None for r in rs))
    check('54true74false field flags preserved',Counter(r['workRequirements']['fieldCraftable'] for r in rs)=={True:54,False:74})
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
    check('All128 identities in both historical sources',all(all(r['id'] in versions[v] for r in rs) for v in ('internalV4','v2')))
    check('Public runtime contains exact82 public identities',{r['id'] for r in versions['publicRuntime'].values() if r['skill'] in TRADES}=={r['id'] for r in rs if r['visibility']=='public'})
    check('Only128 absentV2 visibility fields differ across3380 fields',len(comparisons)==3380 and len(diff)==128 and all(d['version']=='v2' and d['field']=='visibility' and not d['otherFieldPresent'] for d in diff))
    protected=read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files']
    check('All42 protected source and reviewed-rule files unchanged',len(protected)==42 and all(sha(GAME/p)==h for p,h in protected.items()))
    check('All four compared source files unchanged',all(sha(paths[k])==h for k,h in hashes.items()))
    assert all(c['pass'] for c in checks),[c['name'] for c in checks if not c['pass']]
    guide=ROOT/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md';paras=guide.read_text(encoding='utf-8').split('\n\n')
    needles=['**Completion:** the Director records a finite harvest manifest','Roll base yield once for the remains','Use the core four-degree check for extraction','**New basic dismantling procedure:**','Track condition separately from material tier and rarity']
    boundary=[]
    for needle in needles:
        matched=[p for p in paras if p.startswith(needle)];assert len(matched)==1,needle
        boundary.append({'file':guide.relative_to(GAME).as_posix(),'sha256':sha(guide),'exactParagraph':matched[0]})
    out={'status':'PASS — internal source preparation only, unsent, no effect decision','trades':list(TRADES),'sourceSha256':hashes['mechanicalV4'],'bookSha256':sha(book),'sourceIndices':{r['id']:source['recipes'].index(r) for r in rs},'counts':dict(Counter(r['visibility'] for r in rs)),'tradeSummaries':{trade:{'recipes':sum(r['skill']==trade for r in rs),'families':dict(Counter(r['recipeFamily'] for r in rs if r['skill']==trade)),'visibility':dict(Counter(r['visibility'] for r in rs if r['skill']==trade)),'extraYieldOmissions':sum(o['trade']==trade for o in omissions)} for trade in TRADES},'recipes':rs,'publicBookBindings':bindings,'structuralAudit':struct,'extraYieldOmissions':omissions,'componentOccurrences':len(components),'reusableToolOccurrences':reusable,'consumedToolOccurrences':used_tools,'catalystOccurrences':catalysts,'reviewedBoundaryEvidence':boundary,'versionAudit':{'sourcePaths':{k:p.relative_to(GAME).as_posix() for k,p in paths.items()},'sourceHashes':hashes,'fields':fields,'comparisons':comparisons,'differences':diff,'fieldComparisons':len(comparisons),'matchingFields':sum(c['equal'] for c in comparisons),'interpretation':'Source variants agree except absent V2 visibility; agreement does not resolve the25 data/prose yield omissions or establish runtime parity.'},'checks':checks,'recipesApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only'}
    create(target,json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    text='''# Gathering-tool source audit — internal preparation

This evidence preserves **128 complete formulas**: Mining43, Skinning43 and Salvaging42; **82 public / six restricted / forty Director-only**. All82 public effects match exact V5 paragraphs. Eighteen checks pass across3,380 source-field comparisons. The only cross-version differences are128 absent V2 visibility fields. No formula effect or numeric conflict is resolved or approved here.

The **25 positive extraYield:1 data/prose omissions** are retained separately with both values and complete source text. Their presence across variants proves the discrepancy is stable, not whether the number should operate. The existing eleven Leatherworking AC conflicts have their own source disposition; that does not automatically settle these yield fields.

The128 formulas contain580 component occurrences:213 reusable tool rows,12 explicitly consumed tool rows and10 consumed catalyst rows. Preserve every occurrence, original quantity/tier/value and consumed flag. A costly high-tier tool input cannot silently become a cheap ordinary kit, and consumed=true cannot be corrected from its role name alone. Independently required credentials, facilities and actual tools remain distinct from process inputs. All work-hour values exist;54 field flags are true and74 false.

## Existing boundaries supplied for the eventual conference

The reviewed harvest procedure begins with a finite manifest: identities, tier, weight, value, total units, damaged recoverable allocation, anatomy and preservation. Base yield is rolled once. Partial selection forfeits unselected ordinary categories. Its four-degree extraction check can preserve one already-recorded damaged ordinary unit on Critical Success; it does not create an exceptional drop or exceed the original anatomy.

The reviewed basic dismantling route uses predeclared physically remaining mundane components,25% recovery and binary success at DC10. It irreversibly dismantles the item, and supplies no automatic magical/unique-item salvage profile or critical-success benefit. Consequently a Salvaging recipe's printed critical-success quality clause needs a specific compatible procedure; it cannot borrow another subsystem's critical rule silently.

Preservation condition (Fresh/Degraded/Spoiled), material tier, rarity, equipment grade, crafting outcome and a recipe's undefined “quality step” are different fields. No source name or common word proves they are interchangeable.

## Decisions required from GPT

- Resolve each of the25 unprinted extraYield1 fields explicitly, retaining source prose and data. If active, define trigger, cap, shared physical identity, frequency and interaction with printed extraYield2 critical clauses and the existing one-damaged-unit preservation rule.
- Define “quality step” separately for mineral harvest, hide/scale harvest and recovered mundane components. Preserve tier/access/rarity/value unless an explicit new rule changes a specific property; do not disguise an unbounded transmutation or multiplication of value as bookkeeping.
- Define actual eligible trade-check tasks: creation, identification, extraction, preservation, refining, dismantling, repair and research are not automatically one interchangeable roll. State which source bonus applies where and which real actor/tool use qualifies.
- Give complete finite body profiles for all seventeen named families, physical unit definitions, size/weight/value, material/HP, required stock or complete-body reservations, tool credential versus enchantment, and compatible use. A Tool/Kit/Rig name is not a free duplicate of an existing complete tool set or an equipment-grade upgrade.
- Resolve several enchanted tools, multiple workers, class/task modifiers and simultaneous body/gear use on one attempt. Give finite bonus/yield/quality arbitration without a universal strongest-modifier rule or repeated activation by transfer.
- Keep gatherable nodes/remains finite and previously manifested. No repeated failed/partial attempt, processing of already-recovered parts, recapture, item trade, repair, suppression or alternate worker may refresh the same anatomy/material allocation.
- For Salvaging, define percentages per actual remaining component identity and permitted unit precision, fractions/remainders, the quoted “up to” cap, failed work, critical-success procedure, and the relationship with the existing25% route. Do not add percentages or apply them to sale value. Magical/unique items still need actual salvage profiles.
- Address nested physical items and assemblies, contained supplies, unique embedded components, spent ammunition/charges, quality variants, source whole-creature references and catalysts. Recovery cannot include both an intact subassembly and its already-counted components.
- State whether quality improvement and extra yield require the tool at completion, the whole attempt, a selected phase or another explicit boundary. Cover damaged functional/Broken tools, suppression, meld, swapping and interruptions without reroll or duplicate claims.
- Preserve actual crafting abilities, primary credentials, station/access modes, field flags, assistants, phases, preservation and source triviality. Classify creation work against already reviewed artisan/non-artisan rules before applying Forge Dwarf; do not assume all crafted objects qualify.
- Decide explicit quality, persistent flaw, repair/reconstruction and value rules for these real bodies. Do not infer a charge, yield, quality-step, price or gear-grade increase from the generic structural-HP improvement option.

The [complete evidence](GATHERING_TOOL_SOURCE_PREPARATION.json) retains all128 originals,82 book bindings,25 omissions,225 tool occurrences,10 catalysts, all comparison differences and exact reviewed boundary paragraphs. It is unsent. Leatherworking's exact-card review remains active. No original information, worksite, body part, inventory resource or cosmology was changed by this audit.
'''
    create(notes,text)
    print(json.dumps({'status':'PASS','recipes':128,'publicBookBindings':82,'checks':len(checks),'sourceFieldComparisons':len(comparisons),'yieldOmissions':dict(Counter(x['trade'] for x in omissions)),'components':580,'reusableTools':213,'consumedTools':12,'catalysts':10,'recipesApproved':0}))
if __name__=='__main__':main()
