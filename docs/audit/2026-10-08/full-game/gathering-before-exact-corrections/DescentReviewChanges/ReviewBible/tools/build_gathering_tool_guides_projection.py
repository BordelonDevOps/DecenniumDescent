"""Versioned GI integration and fail-closed player candidate projection.

Preserves the previous internal drafts. No source recipe is changed or approved.
Public component mentions are required assembly information, not donor dossiers.
Supplemental profiles require an exact matching public material authority.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, re, shutil
from build_gathering_tool_internal_draft import card_md, TRADE

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
STATUS='authored-candidate; joint-source reconciled; exact-review pending'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(G).as_posix()
def esc(v):return str(v).replace('|','\\|').replace('\n',' ')

AUXILIARY={
 'skinning.mundane-kit':{'name':"Mundane Skinner's-tools kit",'priceGp':5,'emptyWeightLb':5,'text':'One actual kit: knife 0.25 lb, sixteen-inch manual bone saw 1.5 lb, scraper 1 lb, fitted protective roll/case 2.25 lb. The knife and scraper may use the corresponding mundane body profiles when they actually match. The roll stores its implements, not unrecorded specimen cargo. This decomposition grants no separate free tools, retail valuations or enchantments.'},
 'skinning.harvesting-rack':{'name':'Mundane Harvesting Rack','priceGp':6,'emptyWeightLb':25,'maximumHP':5,'structuralAC':15,'surfaceInches':[48,30],'heightInches':30,'maximumSupportedLb':50,'packedInches':[50,8,6],'deployedInches':[50,32,30],'setupMinutes':5,'packingMinutes':5,'text':'Stable placement and two hands are required. Setup/packing is outside recipe hours unless already deployed. The supported-load limit includes everything supported. This is not a hoist, restraint or preserving station. A suitable existing station can serve instead. A tiered Curing rack remains its exact source object; this ordinary rack cannot replace an expensive consumed or retained source occurrence merely by sharing its name.'},
 'salvaging.salvage-table':{'name':'Mundane Salvage Table','priceGp':10,'emptyWeightLb':25,'maximumHP':20,'structuralAC':15,'surfaceInches':[48,30],'heightInches':30,'edgeThicknessInches':2,'maximumSupportedLb':100,'packedInches':[50,8,6],'deployedInches':[50,32,30],'setupMinutes':5,'packingMinutes':5,'text':'Stable placement and two hands are required. Setup/packing is outside recipe or dismantling hours unless already deployed. Every supported item counts toward the load. No tools, heat, storage, protection or bonus is supplied. A real compatible existing station may serve instead; ordinary field dismantling accepts a suitable stable surface without compulsory table ownership.'}
}

def bodies_md(bs,aux,internal=False):
 out=['# Gathering tools — '+('internal' if internal else 'player')+' candidate body catalogue','',
 '**Authored candidate; exact review pending.** Every profile describes one complete output, with one aggregate structural track. Recorded components, required original primary members, current condition and fit remain necessary. The mundane price/empty mass binds the body before its recipe transforms it. The finished output is magical; the same physical facts govern either audience.','']
 for key,b in bs.items():
  out += [f"## {b['trade']}: {b['family']}",'',f"**{b['baselinePriceGp']} gp; {b['baselineWeightLb']} lb empty; ordinary HP {b['ordinaryMaximumStructuralHP']} / structural AC {b['structuralAC']}; {b['equipmentGrade']} grade.**",'',b['operationalBodyText'],'',
   '**Original primary members:** '+', '.join(b['requiredOriginalPrimaryMembers'])+'.','',
   '**Permitted compatible subordinate replacements:** '+', '.join(b['permittedSubordinateReplacements'])+'.','',
   'Fixed dimensions; no automatic scaling. Two usable manipulating hands, actual compatible support and access are required. Capacity does not supply safe containment for hazardous material. A missing necessary member can disable a positive-HP body.','']
 for a in aux.values():
  out += [f"## {a['name']}",'',f"**{a['priceGp']} gp; {a['emptyWeightLb']} lb empty.**",'',a['text'],'']
  if 'maximumHP' in a:out += [f"Structural HP {a['maximumHP']} / AC {a['structuralAC']}; surface {a['surfaceInches'][0]} × {a['surfaceInches'][1]} inches at {a['heightInches']} inches; total supported load {a['maximumSupportedLb']} lb. Packed {' × '.join(map(str,a['packedInches']))} inches; deployed {' × '.join(map(str,a['deployedInches']))} inches. Setup and packing each {a['setupMinutes']} active minutes."+(' Bench edge is 2 inches thick.' if 'edgeThicknessInches' in a else ''),'']
 return '\n'.join(out)

def component_projection(c,materials):
 # A public formula authorizes its ingredient mention and assembly consumption,
 # not the entire embedded material object. Never infer visibility by its name.
 p={k:deepcopy(c[k]) for k in ['name','quantity','role','consumed']}
 matches=[(i,m) for i,m in enumerate(materials) if m['name'].casefold()==c['name'].casefold() and all(m.get(k)==c.get(k) for k in ['tier','value','weight'])]
 authority=None
 if len(matches)==1 and matches[0][1].get('visibility')=='public':
  i,m=matches[0];p['publicMaterialProfile']={k:deepcopy(m[k]) for k in ['name','tier','rarity','category','value','weight','properties'] if k in m}
  authority={'materialIndex':i,'visibility':'public','exactMatchFields':['name-casefold','tier','value','weight']}
 # Withheld metadata is retained in the full internal source and audit ledger.
 return p,authority

def public_card_md(c,b,full):
 # Reuse mechanical prose, replace its internal component and history envelope.
 text=card_md(full,b)
 text=text.replace('**Internal draft • public •','**Player candidate • public •')
 start=text.index('**Exact source components:**');end=text.index('**Creation work:**',start)
 table=['**Required component occurrences:** Whole-batch amounts. Each row is separate; consumed rows are spent and retained rows remain working capital. Detailed stock must match the actual formula before commitment. Public mentions do not disclose private donor or acquisition profiles.','','| Index | Ingredient | Quantity | Role | Consumed | Public material profile, when independently established |','|---:|---|---:|---|---|---|']
 for i,v in enumerate(c['sourceRecipe']['components']):
  profile=v.get('publicMaterialProfile');detail=(f"Tier {profile['tier']}; {profile['value']} gp and {profile['weight']} lb per source unit" if profile else 'Director verifies the exact required stock')
  table.append(f"| {i} | {esc(v['name'])} | {v['quantity']} | {v['role']} | {str(v['consumed']).lower()} | {detail} |")
 text=text[:start]+'\n'.join(table)+'\n\n'+text[end:]
 text=re.sub(r'\*\*Source tags and inactive history:\*\*.*?\n\n','',text,flags=re.S)
 text=text[:text.index('**Provenance and dependencies:**')]
 if c['recipeId'] in {'recipe-347','recipe-349','recipe-350','recipe-656','recipe-676'}:
  text+='**NEW omission completion:** The preserved source data carries one additional unit while the printed prose omits it. The operational card makes that allowance critical-success-only against real recorded ordinary reserve. The original text remains unchanged.\n\n'
 text+='**Use with:** the shared gathering guide, the '+c['sourceRecipe']['skill']+' field guide and the complete candidate body catalogue. This authored card awaits exact review.\n'
 return text

def main():
 ip=R/'data/director/gathering_tool_recipe_candidate_internal.json';pubp=R/'data/crafting/gathering_tool_recipe_candidate_public.json'
 assert not pubp.exists(),'Preserve/version the current projection before rebuilding.'
 d=read(ip);source=read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json');protected=read(A/'GATHERING_TOOL_PART2_SUBMISSION.json')['protectedFiles']
 assert all(sha(G/p)==h for p,h in protected.items())
 joint=A/'GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md';cap=read(A/'GATHERING_JOINT_SOURCE_RECONCILIATION_REPLY_CAPTURE.json')
 assert joint.read_text(encoding='utf-8').rstrip('\n')==cap['documentBody'] and cap['replyId']=='dab78a15-8340-4203-bb03-df03fa6a4956'
 archive=A/'gathering-before-joint-guide-integration';assert not archive.exists();archive.mkdir()
 old=[ip,R/'docs/director-only/GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md',A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json',A/'GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json']+[R/f'docs/director-only/{tr.upper()}_INTERNAL_RECIPE_CARDS.md' for tr in TRADE]
 manifest=[]
 for p in old:
  dst=archive/p.name;shutil.copy2(p,dst);manifest.append({'original':rel(p),'savedAs':dst.name,'sha256':sha(dst)})
 dump(archive/'MANIFEST.json',manifest)
 d['status']=STATUS;d['sourceJointReconciliation']={'file':rel(joint),'sha256':sha(joint),'turnId':cap['turnId'],'replyId':cap['replyId'],'corrections':['GI-11-C1','GI-12-C1'],'exactApproval':False}
 d['sharedOperationalGuide']='docs/director-only/GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md';d['auxiliaryModels']=deepcopy(AUXILIARY)
 for c in d['cards']:c['status']=STATUS
 dump(ip,d)
 appendix=R/'docs/director-only/GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md'
 appendix.write_text(appendix.read_text(encoding='utf-8')+'\n\n# Later controlling joint reconciliation\n\nThe original three verdicts above are preserved verbatim. GI-11-C1 corrects the Salvaging example only; GI-12-C1 corrects Skinning structural coverage only. Both take precedence over the historical wording.\n\n'+joint.read_text(encoding='utf-8'),encoding='utf-8')
 outputs=[ip,appendix]
 for tr in TRADE:
  cs=[c for c in d['cards'] if c['sourceRecipe']['skill']==tr];p=R/f'docs/director-only/{tr.upper()}_INTERNAL_RECIPE_CARDS.md'
  p.write_text(f'# {tr} — internal candidate recipe cards\n\n**{len(cs)} authored candidates; exact review pending.** Use the [operational guide](GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md) and [preserved source directions](GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md). Sources remain unchanged; GI corrections apply separately.\n\n'+'\n'.join(card_md(c,d['baseModels'][c['operational']['baseModelIds'][0]]) for c in cs),encoding='utf-8');outputs.append(p)
 internalguide=R/d['sharedOperationalGuide']
 internalguide.write_text('''# Gathering tools — internal operational guide

**All 128 authored candidates; exact review pending.** Read the shared and trade field procedures, which apply equally to the corresponding internal cards, then the additions below. The full historical evidence remains in the separate source-direction appendix. A source-authoring verdict does not approve a card or certify runtime/balance.

- [Shared procedure, creation and restoration](../mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md)
- [Mining procedure](../mechanics/MINING_CANDIDATE_GUIDE.md)
- [Skinning procedure](../mechanics/SKINNING_CANDIDATE_GUIDE.md)
- [Salvaging procedure](../mechanics/SALVAGING_CANDIDATE_GUIDE.md)
- [All seventeen internal bodies and auxiliary stations](GATHERING_TOOL_INTERNAL_BODY_CATALOGUE.md)
- [Mining cards](MINING_INTERNAL_RECIPE_CARDS.md), [Skinning cards](SKINNING_INTERNAL_RECIPE_CARDS.md), [Salvaging cards](SALVAGING_INTERNAL_RECIPE_CARDS.md)

## Complete internal effect coverage

Mining A: 320–344, +1 with no item reserve/preparation. B: 345–355, 656, 657, +2 and one preparation on Success or Critical Success, with one critical-only reserve unit. C: 356–358, 658, 659, +3, one preparation on Success or Critical Success and two critical-only reserve units. All thirteen B one-unit triggers are NEW omission completions; preserve the original fields and prose. The private Drill is manual compatible boring during already-exposed mineral extraction, with no prospecting/assay bonus.

Skinning A: 507–531, 677, 678, +1 with no item reserve/preparation. B: 532–541, 676, 679, +2, one preparation on Success or Critical Success and one critical-only reserve unit. C: 542–545, +3, one preparation on Success or Critical Success and two critical-only reserve units. All twelve B triggers are NEW omission completions. Two-extra effects still use only original real S when following Fishing; no retroactive reserve is supplied.

Salvaging groups: 433–445 = +1/25%; 446–455,668 = +1/35%; 456–461 = +2/45%; 462–466,669 = +2/55% with preparation; 467–469 = +3/65% with preparation; 470,670,671 = +3/75% with preparation. Every percentage replaces the baseline per eligible identity. No extraYield exists. The private Recovery Rig requires its full recorded geometry, support and additional five-minute mounting and five-minute dismounting.

## Precision component preparation

Tool-assisted dismantling still has binary DC10 success without natural shifts. A final total T≥20 separately qualifies Precision Critical Success, solely for an eligible printed preparation source. T<10 fails; 10≤T<20 succeeds without this preparation. No quantity, generic critical trigger, damaged-unit benefit, mishap or extra roll follows the precision label. Basic dismantling never receives this bridge. Ordinary construct-remains extraction gets only the compatible numerical item bonus.

The source must cover the entire declared exact identity pool, not just its eventual quality target. At precision success, follow the preregistered order to select one actually recovered compatible ordinary component up to 5 lb and 0.10 ft³, or a real predeclared bulk portion no larger than one source unit within those limits. Advance component preparation from Unprepared to Surface-cleaned/sorted once. The operation completes ten minutes of feasible nonhazardous superficial cleaning/sorting inside the existing hour. A capable worker with compatible Salvager's tools, both hands and a stable accessible surface can perform the mundane counterpart in ten active minutes without a roll. Record removed waste and retained matter; no extra reagent tax arises.

This is not chemical purification, repair, smelting or hazardous decontamination. Already prepared, incompatible or oversized indivisible material receives no benefit or substitute. Preparation changes neither yield, tier, rarity, value, HP, Freshness nor recipe progress. It is distinct from mineral dressing and hide/scale surface preparation.

## Corrected loss example and lineage

GI-11-C1 controls the old GT-V16C example: of an original 8 units, 2 are lost before admission and 1 during work. At a 75% ceiling, the 5 still present award 3.75 units and leave 1.25 unawarded. Thus 8 = 2 prior loss + 1 work loss + 3.75 awarded + 1.25 surviving unawarded. The 2.25 not awarded from the admitted 6 includes the 1 lost unit; it is not all residue in custody. Keep each actual disposition. Wrapping the surviving 1.25 with a new product gives it no ingredient entitlement.

Lawful manufacture using the awarded 3.75 may yield a real new product. Later 75% recovery at 0.01 precision gives at most 2.81 from its actual remaining material, not a share of the original 8. No unawarded residue enters that chain automatically.

## Components, visibility and exact-review gate

Preserve 580 occurrences: Mining193 (67 retained tools/126 consumed), Skinning192 (83/109), Salvaging195 (63/132). The twelve consumed tools remain consumed; ten catalyst occurrences allow at most one actual Masterwork return per batch, never all ten. Skinning has no catalysts. Keep both recipe-540 fang occurrences and both recipe-462 marrow occurrences. Recipe-671's soul circuit remains a material; its private matrixResearch remains preserved and inactive, with no additional ingredient, ritual, research permission or cosmological interpretation.

Preserve every exact component identity and physical divisibility. Mining/Salvaging source tool and discrete-part quantities are indivisible unless a genuine governing profile permits division; chemical/bulk precision is not inferred from monetary value. Skinning's reviewed oils, tanning solution and salts use 0.01 source units; whole fangs, tools and ordinary discrete parts do not.

Audience totals are 82 public, 6 restricted and 40 Director-only. Fifteen body models and the public auxiliary stations have public users; private Drill and Recovery Rig remain internal. All 492 public book paragraphs remain exact. Player projections retain formula ingredient mentions and required consumption but publish supplemental material profiles only under a matching public material authority. Missing or private metadata stays internally available, and does not establish acquisition rights. Review the entire projected JSON, cards and guides.

GI-12-C1 replaces the earlier Skinning structural count: each B5 body has 26 positive-HP P/flaw/current-HP inputs, 32 including zero. Mining156/192; Skinning130/160; Salvaging156/192; combined442/544. Outcomes and restoration transitions are separate dimensions. Exact review needs all 128 cards, 1,536 recipe/six-band/two-option cases with inapplicable choices labeled, 256 restoration quotations plus qualification, physical sequence cases and eight combined seams. These are authored-model checks, not evidence of runtime implementation or campaign balance.

Actual material access, anatomy, bills, special handling, origin and independent feature interactions remain genuine execution dependencies. Source directions are sufficient; there is no remaining preliminary source conference. Zero promotions occur here. Whole-game flow, authorized push and remote verification still precede careful cosmology review.
''',encoding='utf-8');outputs.append(internalguide)
 ib=R/'docs/director-only/GATHERING_TOOL_INTERNAL_BODY_CATALOGUE.md';ib.write_text(bodies_md(d['baseModels'],AUXILIARY,True),encoding='utf-8');outputs.append(ib)
 pcards=[];ledger=[]
 sourcekeys=['id','name','skill','skillLevel','difficulty','difficultyBand','craftingTime','rarity','quantity','tags','recipeFamily','outputType','effects','workRequirements','craftingCheck','discovery','economy','skillProgression','tier','visibility','knowledgeStatus','publicAvailability']
 for c in d['cards']:
  if c['visibility']!='public':continue
  r=c['sourceRecipe'];p={k:deepcopy(r[k]) for k in sourcekeys if k in r};p['components']=[]
  for i,comp in enumerate(r['components']):
   v,authority=component_projection(comp,source['materials']);p['components'].append(v)
   ledger.append({'recipeId':r['id'],'componentIndex':i,'assemblyFields':['name','quantity','role','consumed'],'assemblyAuthority':'public recipe component requirement; printed ingredient binding retained separately','supplementalAuthority':authority,'withheldSourceKeys':sorted(set(comp)-{'name','quantity','role','consumed'}),'sourcePreserved':True})
  assert not c['operational']['eligibleCatalystOccurrences'],'Inspect any newly public nested catalyst source before projection'
  pcards.append({'recipeId':c['recipeId'],'name':c['name'],'visibility':'public','status':STATUS,'sourceRecipe':p,'publicBookBinding':deepcopy(c['publicBookBinding']),'operational':deepcopy(c['operational'])})
 used={mid for c in pcards for mid in c['operational']['baseModelIds']};pbs={k:deepcopy(v) for k,v in d['baseModels'].items() if k in used}
 pub={'schemaVersion':1,'status':STATUS,'audience':'public-candidate','sharedCandidateRules':d['sharedCandidateRules'],'sharedOperationalGuide':'docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md','baseModels':pbs,'auxiliaryModels':deepcopy(AUXILIARY),'cards':pcards,'exactRecipeApproval':False,'runtimeImplemented':False,'balanceApproved':False,'projectionNote':'Formula mentions and consumption are retained; supplemental profiles require matching public authority. Original objects remain preserved internally. The book bindings are exact and separate from operational completion.'}
 dump(pubp,pub);outputs.append(pubp)
 pb=R/'docs/mechanics/GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md';pb.write_text(bodies_md(pbs,AUXILIARY),encoding='utf-8');outputs.append(pb)
 for tr in TRADE:
  cs=[c for c in pcards if c['sourceRecipe']['skill']==tr];full={c['recipeId']:c for c in d['cards']};p=R/f'docs/mechanics/{tr.upper()}_CANDIDATE_RECIPE_CARDS.md'
  p.write_text(f'# {tr} — player candidate recipe cards\n\n**{len(cs)} public candidates; exact review pending.** Use the [shared guide](GATHERING_TOOL_CANDIDATE_GUIDE.md), [{tr} guide]({tr.upper()}_CANDIDATE_GUIDE.md) and [body catalogue](GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md). Original book paragraphs remain distinct from new operational text.\n\n'+'\n'.join(public_card_md(c,pbs[c['operational']['baseModelIds'][0]],full[c['recipeId']]) for c in cs),encoding='utf-8');outputs.append(p)
 for name in ['GATHERING_TOOL','MINING','SKINNING','SALVAGING']:outputs.append(R/f'docs/mechanics/{name}_CANDIDATE_GUIDE.md')
 dump(A/'GATHERING_TOOL_PUBLIC_PROJECTION_LEDGER.json',{'status':'authored projection; exact-review pending','sourceSha256':sha(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'),'rows':ledger,'profilesPublished':sum(x['supplementalAuthority'] is not None for x in ledger),'profilesWithheld':sum(x['supplementalAuthority'] is None for x in ledger),'sourceDeleted':0})
 assert all(sha(G/p)==h for p,h in protected.items())
 report=read(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json');report.update(status=STATUS,updatedAtUtc=datetime.now(timezone.utc).isoformat(),sourceJointReconciliation=d['sourceJointReconciliation'],publicCards=82,publicBodies=15,publicParagraphs=492,auxiliaryModels=3,outputs={rel(p):sha(p) for p in outputs},openWork=['Validate complete guides/projection and meaningful arithmetic/physical sequences','Submit all128 complete candidates for separate exact GPT review'],previousVersionArchive=rel(archive/'MANIFEST.json'))
 dump(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json',report)
 dump(A/'GATHERING_JOINT_SOURCE_RECONCILIATION_INTEGRATION.json',{'status':'APPLIED source documentation corrections; no mechanics/source edits','source':d['sourceJointReconciliation'],'corrections':{'GI-11-C1':'Surviving residue1.25; loss1; prior loss2; awarded3.75','GI-12-C1':{'Mining':[156,192],'Skinning':[130,160],'Salvaging':[156,192],'total':[442,544]}},'protectedInputsUnchanged':82,'recipesApproved':0})
 print(json.dumps({'status':STATUS,'internalCards':128,'publicCards':len(pcards),'publicBodies':len(pbs),'publicBookParagraphs':sum(len(c['publicBookBinding']['paragraphs']) for c in pcards),'supplementalPublicProfiles':sum(x['supplementalAuthority'] is not None for x in ledger),'supplementalProfilesWithheld':sum(x['supplementalAuthority'] is None for x in ledger),'recipesApproved':0}))

if __name__=='__main__':main()
