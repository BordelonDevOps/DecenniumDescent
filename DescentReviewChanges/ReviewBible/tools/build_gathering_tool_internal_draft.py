"""Author all128 internal draft cards from preserved gathering source decisions.

This initial manuscript is deliberately unpromoted. Public guides/projection,
sequence validation and separate exact review remain required.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json
from gathering_tool_models import models,model_id

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
STATUS='internal-authored-draft; joint-source-reconciliation and exact-review pending'
TRADE={
 'Mining':{'prefix':'GT-M','ability':['Strength','Wisdom'],'credential':"Miner's tools",'checkFamily':'equipment.mining-task-enhancement','extraFamily':'equipment.mining-extra-recovery','qualityFamily':'equipment.mining-quality-step'},
 'Skinning':{'prefix':'GT-S','ability':['Dexterity','Wisdom'],'credential':"Skinner's tools",'checkFamily':'equipment.skinning-task-enhancement','extraFamily':'equipment.skinning-extra-recovery','qualityFamily':'equipment.skinning-quality-step'},
 'Salvaging':{'prefix':'GT-V','ability':['Intelligence','Wisdom'],'credential':"Salvager's tools",'checkFamily':'equipment.salvaging-task-enhancement','recoveryFamily':'equipment.salvaging-recovery-ceiling','qualityFamily':'equipment.salvaging-component-preparation'}
}
ROLES={
 'Mining Pick':'Exposed mineral detachment only; no prospecting or assay bonus.',
 'Gem Cutter':'Compatible mineral extraction; mineral assay only when actual scoring/examination is necessary; no prospecting bonus.',
 'Ore Extractor':'Supported manual mineral extraction only; no prospecting or assay bonus.',
 'Prospecting Tools':'Actual prospecting, mineral assay and necessary sampling/measurement/selection during mineral extraction.',
 'Mining Tool':'Actual screening/collecting mineral extraction; assay only when sorting/examination is necessary; no prospecting bonus.',
 'Drill':'Manual boring genuinely needed to free an already exposed compatible mineral piece; no prospecting or assay bonus.',
 'Skinning Knife':'Controlled cutting/separation of compatible animal parts with all other needed implements; no preservation bonus.',
 'Hide Scraper':'Hide or compatible scale/chitin backing separation; no preservation bonus.',
 'Scale Remover':'Actual lifting/removal of compatible scales or plates; no preservation bonus.',
 'Tanning Tools':'Supported hide/backing or compatible scaled-sheet extraction; separately, compatible hide/scale/chitin preservation.',
 'Preservation Kit':'Actual controlled receiving/separation of compatible parts during extraction, with missing cutting implements supplied; separately, compatible hide/scale/chitin preservation.',
 'Refiner':'Compatible loose component separation during lawful mundane dismantling; independently lawful ordinary construct-remains extraction may receive the numerical check bonus only.',
 'Salvaging Kit':'Actual compatible manual dismantling/separation with the complete kit; independently lawful ordinary construct-remains extraction may receive the numerical check bonus only.',
 'Separator':'Compatible accessible joint/assembly separation on real supported work; independently lawful ordinary construct-remains extraction may receive the numerical check bonus only.',
 'Extractor':'Manual extraction of accessible fitted ordinary components within actual force/fit limits; independently lawful ordinary construct-remains extraction may receive the numerical check bonus only.',
 'Salvage Tool':'Compatible manual unfastening, prying or separation of accessible ordinary components; independently lawful ordinary construct-remains extraction may receive the numerical check bonus only.',
 'Recovery Rig':'Actual manual recovery of compatible supported ordinary assemblies within the rig envelope; independently lawful ordinary construct-remains extraction may receive the numerical check bonus only.'
}
COMMON='''Register at most one magical candidate per physical family before commitment. The actual lead must directly operate it for at least one active minute in genuinely necessary compatible work, or throughout a genuinely shorter separately authorized task. Setup alone, token contact, an assistant's use and unused carried gear do not qualify. At qualifying work and the single resolution checkpoint, the complete item must be positive-HP, accessible, unsuppressed, unmelded and participating. Use current views for every registered candidate and the same physical histories for task admission and effects. Ordinary indispensable tools remain required even when unenchanted. Later suppression, repair or a new owner cannot rewrite a resolved claim. Pauses preserve the same unresolved claim; replacement leads require an accepted record and a genuinely feasible full lead workflow without reversing completed work. No late enchanted candidate or borrowed work interval.

These are durable magical nonartifact tools without attunement, charges, RP, concentration or a separate magic activation. Ordinary structural AC protects the object, not its bearer. Names, tags, donors, rarity, price and legacy effects grant no unprinted power, proficiency, formula, ingredient stock or acquisition permission. No Forge Dwarf artisan time/quality benefit applies. No tool imprint improves its creation, research, copying, identification, appraisal, repair or combat unless a separate exact rule expressly authorizes that task. Other actual class/spell/equipment effects retain their own predicates and stacking; these comparison families are not universal stacking rules.'''

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ratio(v):v=F(v);return {'numerator':v.numerator,'denominator':v.denominator}
def val(v):v=F(v);return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def esc(v):return str(v).replace('|','\\|').replace('\n',' ')

def effect(r):
 tr=r['skill'];m=r['mechanics'];t=TRADE[tr];bonus=m[{'Mining':'miningBonus','Skinning':'skinningBonus','Salvaging':'salvageBonus'}[tr]]
 text=f"This participating {r['recipeFamily']} offers +{bonus} in {t['checkFamily']}; apply the strongest independently eligible source once to the lead's permitted check. {ROLES[r['recipeFamily']]} "
 e={'checkBonus':bonus,'checkFamily':t['checkFamily'],'eligibleRole':ROLES[r['recipeFamily']],'qualityStep':m['qualityStep'],'qualityFamily':t['qualityFamily']}
 if tr in ('Mining','Skinning'):
  extra=m.get('extraYield',0);e.update(extraYield=extra,extraFamily=t['extraFamily'],extraTrigger='Core extraction Critical Success only',qualityTrigger='successful extraction, including Critical Success',coverage='actual selected ordinary extraction allocation, including proposed reserve')
  if extra:
   text+=f"On a Core extraction Critical Success, it offers up to {extra} distinct real ordinary reserve unit{'s' if extra!=1 else ''} in {t['extraFamily']}, independently compared. This supplements the one separately recorded damaged-baseline unit; it creates no matter or unique drop. A normal Success has no tool extra. "
  else:
   text+='This recipe grants no extra-recovery candidate; ordinary extraction critical benefits retain their own scope. '
  if m['qualityStep']:
   quality=('one compatible recovered ordinary mineral unit or predeclared real portion of at most 1 lb, Rough → Dressed' if tr=='Mining' else 'one compatible recovered ordinary hide/scale/chitin unit of at most 10 lb and 4 ft² actual treated surface, Unprepared → Surface-prepared')
   text+=f"On successful extraction, complete at most one preparation step on {quality}. Select the first eligible recovered unit in the preregistered order. The step completes 10 minutes of compatible superficial dry work within extraction; it grants no tier, value, freshness, HP or recipe-time improvement. If none qualifies, grant no substitute benefit. "
  else:text+='This recipe grants no preparation step. '
  if tr=='Skinning':text+='Only a Tanning Tools or Preservation Kit body may apply its check bonus to the separate eligible 30-minute preservation treatment; neither extra recovery nor preparation applies there. '
 else:
  p=m['recoveryPercent'];e.update(recoveryPercent=p,recoveryFamily=t['recoveryFamily'],qualityTrigger='tool-assisted dismantling total >=20 only',coverage='each exact component identity entire declared recovery pool')
  text+=f"On successful tool-assisted mundane dismantling, each fully covered exact component-identity pool uses the strongest eligible total recovery ceiling, including this source's {p}%, replacing the ordinary 25% rather than adding to it. Recover floor_to_unit(current eligible quantity × percentage / 100); unit 1 for indivisible parts, or 0.01 only for genuinely divisible bulk with that precision. No minimum one, remainder banking or later pass over residue. "
  if m['qualityStep']:text+='At total 20 or more on that route, prepare at most one actually recovered compatible mundane component of at most 5 lb and 0.10 ft³, or a preregistered bulk portion of at most one source unit within those limits. Follow the prior target order. This completes 10 minutes of nonhazardous superficial cleaning/sorting within the work, with no yield, tier, value, HP or freshness increase. '
  else:text+='This recipe grants no critical preparation step. '
  text+='Basic and tool-assisted dismantling succeed at DC 10 without natural-die shifts; the precision label changes no quantity and is not a generic critical. Percentage/preparation never apply to construct-remains extraction. '
 text+='Apply the shared candidate, work, physical-history and receipt requirements. A numerical allowance is not proof of actual materials or lawful receipt.'
 return e,text

def operation(r,b):
 tr=r['skill'];q=r['quantity'];w=r['workRequirements'];eff,text=effect(r);body=F(str(b['baselinePriceGp']));finished=F(str(r['economy']['recommendedMarketValue']))/q+body
 cats=[{'index':i,'component':deepcopy(c)} for i,c in enumerate(r['components']) if c['consumed'] and c['role']=='catalyst']
 return {'text':text,'baseModelIds':[b['id']],'effect':eff,'standardQuantity':q,'maximumOrderedBodyReserve':3*q//2,
  'work':{'abilityOptions':TRADE[tr]['ability'],'credential':TRADE[tr]['credential'],'artisan':False,'forgeDwarfEligible':False,'sourceActiveHours':w['activeWorkHours'],'includedStablePhaseHours':.25,'remainingHours':ratio(F(str(w['activeWorkHours']))-F(1,4)),'laterPhaseMaximumHours':8,'fieldCraftable':w['fieldCraftable'],'timeMode':w['timeMode'],'station':w['station'],'requiredTools':deepcopy(w['requiredTools']),'maximumAssistants':w['maximumAssistants'],'DC':r['craftingCheck']['targetDC'],'trivialAtSkillLevel':r['skillProgression']['trivialAtSkillLevel']},
  'outcomes':{'Standard':q,'ExceptionalYield':5*q//4,'MasterworkYield':3*q//2,'StructuralOptionQuantity':q,'ExceptionalStructuralPercent':25,'MasterworkStructuralPercent':50,'FlawedQuantity':q//2 if q>=2 else 1,'SingletonFlawedAddsPersistentFlaw':q==1,'Failed':0,'Mishap':0,'maximumMasterworkCatalystReturnUnits':min(1,len(cats))},
  'eligibleCatalystOccurrences':cats,'sourceProcessUnitReferenceGp':ratio(F(str(r['economy']['recommendedMarketValue']))/q),'finishedUnitReferenceGp':ratio(finished),
  'repair':{'trainedCredential':TRADE[tr]['credential'],'abilityOptions':TRADE[tr]['ability'],'functionalDC':10,'brokenDC':r['craftingCheck']['targetDC'],'functionalHours':'max(1, recorded maximumHP/10)','brokenHours':'max(8, recorded maximumHP/10)','functionalMaterialReferenceGp':ratio(body/4),'brokenMaterialReferenceGp':ratio(finished/4),'requiredOriginalPrimaryMembers':deepcopy(b['requiredOriginalPrimaryMembers']),'requiresOriginalCreationRecord':True,'terminalDismantlingRestorable':False,'formulaOrCreationLevelRequired':False,'restoresOnlyRecordedMaximumAndLegalFunction':True}}

def card_md(c,b):
 r=c['sourceRecipe'];o=c['operational'];w=o['work'];q=r['quantity'];rep=o['repair'];f=lambda v:val(F(v['numerator'],v['denominator']))
 lines=[f"## {r['name']} — {r['id']}",'',f"**Internal draft • {r['visibility']} • {r['skill']} level {r['skillLevel']} • tier {r['tier']} • DC {w['DC']} • {r['rarity']}**",'',
  '**Operational effect:** '+o['text'],'',f"**Complete body:** {b['baselinePriceGp']} gp; {b['baselineWeightLb']} lb empty; ordinary HP 5 / structural AC {b['structuralAC']}; Standard grade. "+b['operationalBodyText'],'',
  f"**Before creation:** Reserve {o['maximumOrderedBodyReserve']} actual complete, eligible mundane bodies in an exclusive fixed order before work. Validate all maximum-yield reserves before continuing and before the roll, even if a lower outcome would use fewer. They must have positive HP, no prior magical alteration and current physical/constituent history. A body cannot also be a toolkit, consumed component or another order's reserve. Lawful pre-roll replacement keeps its position; no post-roll choice or purchase. Transform the first resolved outputs; unused bodies remain ordinary stock.",'',
  '**Exact source components:** Each occurrence remains separate, including repeated IDs. Source quantities are for the whole printed batch, not each output.','',
  '| Index | Ingredient / exact source ID | Quantity | Tier | Unit gp | Unit lb | Role | Consumed |','|---:|---|---:|---:|---:|---:|---|---|']
 for i,x in enumerate(r['components']):lines.append(f"| {i} | {esc(x['name'])} / {esc(x['id'])} | {x['quantity']} | {x['tier']} | {x['value']} | {x['weight']} | {x['role']} | {str(x['consumed']).lower()} |")
 lines+=['',f"**Creation work:** {r['craftingTime']} = {w['sourceActiveHours']} actual active hours at {w['station']}, using {', '.join(w['requiredTools'])}. Choose {' or '.join(w['abilityOptions'])} and use {w['credential']} training under the crafting framework. The first 15 active minutes are included, leaving {f(w['remainingHours'])} hours in declared phases of at most eight hours. Only eligible actually incorporated inputs stabilize; untouched, returned or withdrawn stock keeps its true age and containment. Interruption loses unfinished-phase progress while spent materials and completed phases remain recorded.",'',
  f"**Access and assistance:** fieldCraftable={str(w['fieldCraftable']).lower()}; timeMode={w['timeMode']}. Both source restrictions and the actual station must be met. Expedition mode requires a fortified camp/research station; names do not waive false field flags. Maximum {w['maximumAssistants']} eligible creation assistants, each working all required hours; no time reduction or assistant XP. Ordinary tools/facilities grant +0. No artisan-only Forge Dwarf benefit. Active labor respects the two-work-Watch ceiling without duplicate credit for guard, travel, another task or beneficial rest.",'',
  '**Discovery and advancement:** '+json.dumps(r['discovery'],ensure_ascii=False)+f". Apply the framework's trained/untrained creation gates and legitimate formula access above level 4; ownership of a finished tool supplies none. Preserve trivialAtSkillLevel={w['trivialAtSkillLevel']} and the exact source progression. Item use, preparation, preservation and repair do not earn crafting XP through this recipe's per-success field.",'',
  f"**Manufacturing outcomes:** Standard {q}; Exceptional yield {o['outcomes']['ExceptionalYield']}; Masterwork yield {o['outcomes']['MasterworkYield']}; Flawed {o['outcomes']['FlawedQuantity']}; Failed/Mishap 0. Alternatively choose Q={q} bodies with the strongest 25%/50% structural improvement once for the batch after the check. HP 5 becomes 6/7; a single persistent flaw halves last to 2/3/3. Preserve current damage deficit. "+('Singleton Flawed establishes one flaw and can finish Broken.' if q==1 else 'Flawed yield reduction retains prior flaws but adds no singleton flaw, even if one output remains.')+' No outcome improves check bonus, reserve, percentage, preparation, capacity, grade or source permissions. Natural 1 is a crafting Mishap; natural 20 adds no extra band shift.','',
  '**Ingredients after resolution:** '+(f"Masterwork may retain one actual eligible catalyst unit total from source occurrence(s) {', '.join(str(x['index']) for x in o['eligibleCatalystOccurrences'])}; never all listed catalysts. " if o['eligibleCatalystOccurrences'] else 'No catalyst return exists for this recipe. ')+"Retained units keep actual identity, age and containment. Failed crafting returns 25% of consumed non-catalyst quantities with lawful exact-identity grouping and unit precision; no fractions of indivisible tools/vessels/parts or value conversion. Mishap/abandonment returns no consumed inputs. Nonconsumed tools and unused bodies remain except for real loss/damage; they are not extra recovery awards. The original material mass does not create duplicate complete bodies or get added once to every output.",'',
  f"**Restoration:** Actual trained {rep['trainedCredential']}, {' or '.join(rep['abilityOptions'])}, functional required tools and a suitable worksite. Functional DC 10; {rep['functionalHours']} hours; material reference {f(rep['functionalMaterialReferenceGp'])} gp. Broken DC {rep['brokenDC']}; {rep['brokenHours']} hours; {f(rep['brokenMaterialReferenceGp'])} gp. Require the original {', '.join(rep['requiredOriginalPrimaryMembers'])} and any additional irreplaceable members recorded at creation. Permitted subordinate replacements need real compatible stock; the target cannot supply missing repair tools. Core natural shifts collapse to success/failure. Success restores only recorded maximum/function; failure spends work/materials. No formula/creation-level gate, extra repair assistants, quality, XP, flaw removal, resource reset or reversal of terminal dismantling.",'',
  f"**Finished unit reference:** {f(o['finishedUnitReferenceGp'])} gp = original batch recommendedMarketValue / original Q + {b['baselinePriceGp']} gp mundane body. Retain exact fractions until one final actual purchase-ceiling/sale-floor copper rounding. Owned bodies need no repurchase; reusable source tools remain capital. Actual stock, operating costs, commissions and a willing buyer remain separate. No automatic artifact multiplier, quality resale multiplier or mundane salvage of a suppressed magical item.",'',
  '**Source effect, preserved unchanged:** '+r['effects'],'',
  '**Source tags and inactive history:** '+json.dumps({k:r[k] for k in ['tags','legacyName','legacyEffect','wholeCreatureUse','matrixResearch','directorGuidance'] if k in r},ensure_ascii=False), '']
 if c['publicBookBinding']:
  lines+=['**Complete original public V5 binding:**','','| Paragraph | Preserved text |','|---:|---|']+[f"| {p['index']} | {esc(p['text'])} |" for p in c['publicBookBinding']['paragraphs']]+['']
 lines+=['**Provenance and dependencies:** '+TRADE[r['skill']]['prefix']+'01–18 source directions; full original object and exact source index in the JSON. This card uses the shared candidate/work/physical-history rules and the complete trade procedures in the source-direction appendix. Material acquisition, special containment, true world records and the exact public projection remain separate requirements. This draft has no operational approval.','']
 return '\n'.join(lines)

def main():
 output=R/'data/director/gathering_tool_recipe_candidate_internal.json';assert not output.exists(),'Preserve prior draft; explicitly revise instead of overwriting.'
 evidence=read(A/'GATHERING_TOOL_SOURCE_PREPARATION.json');source=R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json';assert sha(source)==evidence['sourceSha256']
 recipes=[r for r in read(source)['recipes'] if r['skill'] in TRADE];assert recipes==evidence['recipes'] and len(recipes)==128
 protected=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')['protectedFiles'];assert all(sha(G/p)==h for p,h in protected.items())
 authorities={};verdicts={}
 for tr in TRADE:
  cap=read(A/(tr.upper()+'_SOURCE_CONFERENCE_CAPTURE.json'));p=A/cap['file'];assert sha(p)==cap['sha256'];authorities[tr]=cap;verdicts[tr]=p.read_text(encoding='utf-8')
 bs=models();bindings={b['recipeId']:b for b in evidence['publicBookBindings']};cards=[]
 for r in recipes:
  b=bs[model_id(r)];cards.append({'recipeId':r['id'],'name':r['name'],'visibility':r['visibility'],'status':STATUS,'sourceRecipeIndex':evidence['sourceIndices'][r['id']],'sourceRecipe':deepcopy(r),'publicBookBinding':deepcopy(bindings.get(r['id'])),'operational':operation(r,b)})
 guide='docs/director-only/GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md'
 obj={'schemaVersion':1,'status':STATUS,'audience':'director-internal','sourceSha256':sha(source),'sourceAuthorities':authorities,'sourceErratum':'docs/audit/2026-10-08/full-game/GPT_SKINNING_SOURCE_TALLY_ERRATUM.md','sharedCandidateRules':COMMON,'sharedSourceDirections':guide,'baseModels':bs,'cards':cards,'exactRecipeApproval':False,'runtimeImplemented':False,'balanceApproved':False,'cosmology':'post-verified-push only'}
 dump(output,obj)
 gp=R/guide;gp.write_text('# Gathering tools — internal source directions\n\n**Draft authoring appendix; not exact-card approval.** This preserves the complete three trade decisions, with the confirmed Skinning tally correction taking precedence over the two historical totals. It accompanies every draft card. A player-facing guide and exact projection still require authoring.\n\n## Shared current candidate requirements\n\n'+COMMON+'\n\n'+(A/'GPT_SKINNING_SOURCE_TALLY_ERRATUM.md').read_text(encoding='utf-8')+'\n\n'+'\n\n'.join(verdicts.values()),encoding='utf-8')
 outputs=[output,gp]
 for tr in TRADE:
  cs=[c for c in cards if c['sourceRecipe']['skill']==tr];p=R/f'docs/director-only/{tr.upper()}_INTERNAL_RECIPE_CARDS.md';assert not p.exists();p.write_text(f'# {tr} — internal draft recipe cards\n\n**{len(cs)} authored drafts; not selectable or reviewed.** Use the complete [shared source directions](GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md) alongside each card. Every original recipe object remains unchanged in the accompanying JSON. Public rules/projection and exact review remain required.\n\n'+'\n'.join(card_md(c,bs[c['operational']['baseModelIds'][0]]) for c in cs),encoding='utf-8');outputs.append(p)
 assert all(sha(G/p)==h for p,h in protected.items())
 report={'status':STATUS,'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'cards':128,'tradeCounts':{tr:sum(c['sourceRecipe']['skill']==tr for c in cards) for tr in TRADE},'visibilityCounts':{v:sum(c['visibility']==v for c in cards) for v in ['public','restricted','director-only']},'bodyModels':17,'publicBookBindings':len(bindings),'protectedInputsUnchanged':len(protected),'outputs':{str(p.relative_to(G)).replace('\\','/'):sha(p) for p in outputs},'sourceInformationDeleted':0,'recipesApproved':0,'currentReviewedRecipes':392,'remainingRecipes':295,'openWork':['Integrate actual GI-01–12 verdict','Author complete public/internal operational guides and recursive public projection','Validate every exact card, arithmetic and meaningful physical/cross-trade sequences','Submit complete128 exact candidates for separate GPT review'],'cosmology':'post-verified-push only'}
 dump(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json',report);print(json.dumps({k:report[k] for k in ['status','cards','tradeCounts','visibilityCounts','bodyModels','publicBookBindings','protectedInputsUnchanged','recipesApproved']}))

if __name__=='__main__':main()
