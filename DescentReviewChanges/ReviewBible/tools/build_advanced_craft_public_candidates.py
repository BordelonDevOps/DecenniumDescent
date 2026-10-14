"""Explicit player projection of the 100 public advanced recipe candidates.

No runtime integration or exact promotion. All exclusions are recorded internally.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json
from build_advanced_craft_internal_candidates import read, dump, sha, val

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
STATUS='authored-player-candidate-awaiting-exact-review'
GUIDE='docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md'
BODY='docs/mechanics/ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md'
SOURCE_KEYS=['id','name','skill','skillLevel','difficulty','difficultyBand','craftingTime','rarity','quantity','tags','recipeFamily','outputType','effects','mechanics','workRequirements','craftingCheck','discovery','economy','skillProgression','tier','visibility','knowledgeStatus','publicAvailability']
BODY_TEXT={
 'EN-weapon':'One complete admitted actual weapon. Default longsword: ordinary 1d8 slashing, versatile1d10, its real proficiency/hands and existing equipment rules. Other listed existing weapon templates need full physical registration before work. The original working blade/head and structural tang/frame appropriate to that actual model are primary. No ammunition, sheath, second weapon or automatic proficiency. Preserve lawful source size/grade and their true reference values.',
 'EN-armor':'One complete admitted actual armor suit. Default chain shirt: ordinary AC13 + DEX (maximum2), with its real armor proficiency/donning requirements. Other listed suit templates retain their actual complete source properties. The principal original torso panels/mail assembly are primary. Structural AC19 is the object’s defense, not wearer AC. Shields and accessory pieces are not an armor suit.',
 'EN-wand':'One continuous hardwood conductor including grip, inscription and finish. The original inscribed rod is primary. One manipulating hand for its pulse; no ordinary weapon or class-focus permission, hidden compartment, fuel or battery.',
 'EN-staff':'One continuous hardwood inscribed rod including grip and finish. The original shaft is primary. One manipulating hand for its pulse; no automatic quarterstaff or class-focus profile. It does not fit a small container or become a necklace by renaming it.',
 'EN-charm':'One steel inscription face with its captive grip/loop. The original inscribed token is primary; a compatible minor grip/cord is subordinate. It can be carried in a lawful existing jewelry position but must actually be grasped with one manipulating hand to pulse. No passive wearing benefit or additional slot.',
 'RC-plate':'Original inscription plate0.8 lb plus captive feet/attachment strap0.2 lb, total1 lb. The original inscribed plate is primary; feet/strap may be replaced compatibly. No cargo or extra host body. Strapping it to gear does not merge HP or create armor. Use the guide’s actual ground placement, direct healing contact or one attuned wearing position.',
 'SC-book':'One 200-page bound book: original page block4 lb, covers/binding1 lb. Each page denotes one writable side. The original relevant inscription/page block is primary; covers/fastenings can be replaced when original content survives. Extra pages/smaller writing create no extra payload, research bonus or separate magical book. Two manipulating hands to open/turn pages unless actual stable support permits one-handed operation; supported reading remains within5 feet.',
 'SC-text':'One 40-page stitched notebook: original page block0.8 lb, covers/binding0.2 lb. Each page is one writable side. The original inscription/page block is primary; compatible covers/binding are subordinate. No supplied factual content or multiplied effects. Use the same actual two-hand/support/readability requirements as a book.',
 'SC-sheet':'One real paper sheet; no protective case or book. The original marked sheet is primary. Actual rolled dimensions come from that sheet; no extradimensional space or magical preservation. A separately supplied case has its own mass and capacity. A recipe’s consumed case remains its separate process input and is not returned for each output.',
 'TI-trap':'Frame3 lb, captive spring/actuation member2 lb, original working striker/discharge block2 lb, fittings/feet1 lb; total8 lb. Original frame and discharge block are primary. The spring, separate subordinate contacts, supports, catches, grip covers, fittings and feet are replaceable only with real compatible stock through actual repair. A missing/nonfunctional spring prevents discharge even at positive aggregate HP. Preserve the same dimensions/mass, primary identity and spent budgets. No loose saleable ammunition or Hunting Trap condition profile.',
 'TI-auto-tiny':'Original frame3 lb, original actuator2 lb, original logic/contact block1 lb, legs/grippers/fittings2 lb; total8 lb. Four ground-moving legs, two simple manipulators, no flight/climb/swim profile or storage chamber. Frame, actuator and logic block are primary; genuinely compatible limb/fitting restoration is subordinate. Carry at most5 lb in actual grippers, also subject to real shape, Load and movement. Occupied manipulators can prevent the attack/task. The B5/AC19 stock profile is replaced by the recipe’s fixed creature HP/AC after creation, not a second HP track.',
 'TI-auto-small':'Original frame10 lb, original actuator6 lb, original logic/contact block3 lb, legs/grippers/fittings6 lb; total25 lb. Four ground-moving legs and two simple manipulators; no storage chamber, flight, climbing/swimming mode or passenger seat. Frame, actuator and logic block are primary; compatible limbs/fittings are subordinate. At most20 lb actual gripper carriage with real geometry/Load; no humanoid item slots or automatic creature carriage. The B5/AC19 stock profile is replaced by printed creature statistics.',
 'TI-tool':'Manual driver/probe1.5 lb, indexed gauge1 lb, fitted handle/captive fittings0.5 lb; total3 lb. Original driver spine and gauge are primary. Two hands operate probe and stabilize actual work. This is one tool, not the complete Tinker toolkit, and has no cargo compartment.',
 'TI-device':'Frame2 lb, gauge1 lb, manual calibration/contact mechanism1 lb, grips/feet1 lb; total5 lb. Original frame, gauge and calibration mechanism are primary. Both hands operate it on a stable real bench. Jaws admit at most4 × 4 × 2 inches and2 lb. The hollow shape is not general cargo or safe fluid storage.',
 'TI-sensor':'Contact probe0.75 lb, comparator1 lb, handle/fittings0.25 lb; total2 lb. Original probe and comparator are primary; minor handle/fittings may be repaired compatibly. Both hands control probe/work. It compares actually exposed reachable properties with its finite dial; no remote detection, hidden compartments, mind-reading, passwords or automatic spell identification.'}


def component(c, materials):
    p={k:deepcopy(c[k]) for k in ['name','quantity','role','consumed']}
    matches=[(i,m) for i,m in enumerate(materials) if m['name'].casefold()==c['name'].casefold() and all(m.get(k)==c.get(k) for k in ['tier','value','weight'])]
    auth=None
    if len(matches)==1 and matches[0][1].get('visibility')=='public':
        i,m=matches[0];p['publicMaterialProfile']={k:deepcopy(m[k]) for k in ['name','tier','rarity','category','value','weight','properties'] if k in m}
        auth={'materialIndex':i,'visibility':'public','matchedFields':['name-casefold','tier','value','weight']}
    return p,auth


def render(c):
    s=c['sourceRecipe'];o=c['operational'];parts=[f"## {s['name']} — {s['id']}",'',f"**Player candidate; {s['skill']} level {s['skillLevel']}; DC {s['difficulty']}; exact review pending.**",'',
        'Use the [complete operating guide](ADVANCED_CRAFT_CANDIDATE_GUIDE.md) and [body catalogue](ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md).','']
    for p in o['paragraphs']:parts.extend(['**'+p['label']+'**','',p['text'],''])
    parts.extend(['**Six original public-book paragraphs, unchanged**',''])
    for p in c['publicBookBinding']['paragraphs']:parts.extend([f"Paragraph {p['index']}: {p['text']}",''])
    return '\n'.join(parts)


def build_projection(d,source):
    cards=[];ledger=[]
    for c in d['cards']:
        if c['visibility']!='public':
            ledger.append({'recipeId':c['recipeId'],'publicCardIncluded':False,'reason':'Original '+c['visibility']+' recipe remains internal; no recipe or body membership projected.'});continue
        s=c['sourceRecipe'];ps={k:deepcopy(s[k]) for k in SOURCE_KEYS if k in s};ps['components']=[];occ=[]
        for i,comp in enumerate(s['components']):
            pc,auth=component(comp,source['materials']);ps['components'].append(pc)
            old=c['operational']['componentOccurrences'][i]
            occ.append({k:deepcopy(old[k]) for k in ['index','retainedTool','consumedTool','masterworkCatalystEligible','failedRecoveryEligible','defaultFailurePrecision','precisionCondition','physicalIdentityMustRemainDistinct']})
            occ[-1]['componentMention']=deepcopy(pc)
            ledger.append({'recipeId':c['recipeId'],'componentIndex':i,'mentionIncluded':True,'supplementalAuthority':auth,
                           'withheldSourceKeys':[k for k in comp if k not in ['name','quantity','role','consumed']],
                           'supplementalProfileIncluded':auth is not None,'reason':'Formula authorizes mention/quantity/role/consumption; donor, acquisition, legacy and other embedded fields are withheld. Supplemental metadata needs one exact independent public material profile.'})
        o={k:deepcopy(c['operational'][k]) for k in ['profile','useBinding','bodyModelIds','standardQuantity','maximumOrderedBodyReserve','work','creation','references','creatureOutput','sourceStandardBatchReferenceGp','sourceProcessUnitReferenceGp','bodyVariants']}
        o['componentOccurrences']=occ;o['guide']=GUIDE;o['bodyGuide']=BODY;o['paragraphs']=[]
        for p in c['operational']['paragraphs']:
            if p['label']=='Internal source history':continue
            text=p['text']
            if p['label']=='Exact component occurrences':
                text='Required whole-batch occurrences; each row remains a separate physical quantity. Match the complete formula’s actual stock before committing; withheld metadata supplies neither free stock nor a substitution.\n\n'
                for i,pc in enumerate(ps['components']):
                    m=pc.get('publicMaterialProfile');extra=(f" Independently public profile: tier {m['tier']}, source unit {m['value']} gp / {m['weight']} lb." if m else ' Exact required stock must be verified with the Director.')
                    text+=f"- [{i}] {pc['name']}: quantity {pc['quantity']}; role {pc['role']}; consumed={str(pc['consumed']).lower()}.{extra}\n"
                text=text.rstrip()
            text=text.replace('max three active ordinary crafted automata separately from one 686.','at most three active ordinary crafted automata; class companion/deployable slots keep their separate source limits.')
            text=text.replace('The full 48-card Tinker interface register and TD-01–18 apply;','The Tinker class-interface procedures in the player guide apply;')
            text=text.replace('public guide','player guide')
            o['paragraphs'].append({'label':'Required component occurrences' if p['label']=='Exact component occurrences' else p['label'],'text':text})
        pc={'recipeId':c['recipeId'],'name':c['name'],'visibility':'public','status':STATUS,'sourceRecipe':ps,'publicBookBinding':deepcopy(c['publicBookBinding']),'operational':o}
        pc['manuscriptText']=render(pc);cards.append(pc)
    ids=sorted({bid for c in cards for bid in c['operational']['bodyModelIds']})
    assert ids==sorted(BODY_TEXT),ids
    bodies={}
    for bid in ids:
        b=d['bodyModels'][bid];src=b['sourceAuthoringProfile'];p={k:deepcopy(src[k]) for k in ['id','priceGp','massLb','HP','AC','dimensionsIn','material']}
        p['model']=b.get('operationalModelDescription',src['model']);p['primary']=b.get('operationalPrimaryRule',src['primary']);p['bodyText']=BODY_TEXT[bid];p['status']=STATUS
        bodies[bid]=p
    return cards,bodies,deepcopy(d['enchantingHostModels']),ledger


def body_markdown(bodies,hosts):
    lines=['# Advanced crafting — player body catalogue','','**Authored candidate; exact review pending.** These are complete ordinary bodies before transformation. The recipe adds its stated magic to the same actual physical identity. One aggregate structural track; creature output AC/HP supersedes the pre-animation chassis track. Prices are body references, not automatically available stock.','']
    for bid,b in bodies.items():
        lines.extend([f'## {bid}','',f"**{b['priceGp']} gp; {b['massLb']} lb; ordinary B{b['HP']}; structural AC {b['AC']}; {' × '.join(map(str,b['dimensionsIn']))} inches.**",'',b['bodyText'],'','**Original primary members and permitted restoration:** '+b['primary'],''])
    lines.extend(['## Actual stations and implements','','One active creator needs a stable clear surface at least24 × 18 inches and appropriately sized actual jigs for the selected complete weapon, suit or machine. A Resonance Circle needs one clear5-foot-square work bay and the genuine ordinary lens/stylus apparatus. A Slab supports the whole plate; a Scribe’s Desk permits real open-page preparation; a Tinker’s Workshop safely supports/fixtures each current assembly. These are actual admission requirements, not free stations or new automatic construction charges. Separate reserved storage can hold other bodies while work proceeds sequentially. Actual load can require stronger support. A portable sheet on a ledge does not satisfy the fixed facility flag.','','Keep each actual complete primary kit’s original price/mass. An included ordinary implement may satisfy a source-listed working requirement but is not a second physical tool, consumed tiered ingredient or complete output body. The player guide gives the narrow Runecarver working-lens correspondence. Actual light, safe access, hands, material preservation and hazardous containment remain necessary.','','## Existing weapon and suit host templates','','Choose one genuinely applicable source template before work and record its full physical state: actual size/grade, dimensions, dominant load-bearing material/AC, original magic-bearing working/structural members, real value/mass and damage history. Existing ordinary special weapon properties, ammunition, hands, proficiency and armor requirements remain. No shields, ammunition bundles, natural attacks, no-damage nets, prior magical hosts or unsupported special models.',''])
    for key,h in hosts.items():
        e=h['sourceEquipmentRecord'];lines.extend([f"### {e['name']} — {key}",'',f"Ordinary reference {val(h['ordinaryPriceGp'])} gp; {h['ordinaryWeightLb']} lb; B{h['baselineStructuralHP']}. Existing source properties: "+'; '.join(f'{k}: {v}' for k,v in e['sourceFields'].items())+'.',''])
    lines.extend(['Existing eligible Large sizing doubles ordinary price, weight and generic HP; Small/Medium/Tiny use their actual source sizing. Apply genuinely permitted grade and structural history afterward. Record the real physical model rather than infer dimensions or material from an ingredient name. The default longsword and chain shirt figures do not overwrite an admitted alternate host.',''])
    return '\n'.join(lines)


def main():
    dest=R/'data/crafting/advanced_craft_recipe_candidate_public.json';assert not dest.exists(),'Preserve/version an existing public candidate before rebuilding.'
    ip=R/'data/director/advanced_craft_recipe_candidate_internal.json';d=read(ip);source=read(R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')
    valid=read(A/'ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json');assert valid['status']=='PASS' and valid['candidateSha256']==sha(ip)
    assert len(d.get('controllingCorrections',[]))==1 and not d['openExactReviewIssues']
    cards,bodies,hosts,ledger=build_projection(d,source);assert len(cards)==100 and len(bodies)==15
    btext=body_markdown(bodies,hosts);(R/BODY).write_text(btext,encoding='utf-8')
    obj={'schemaVersion':1,'status':STATUS,'audience':'player-candidate','guide':GUIDE,'bodyGuide':BODY,
         'operatingGuideText':(R/GUIDE).read_text(encoding='utf-8'),'bodyGuideText':btext,'bodyModels':bodies,'enchantingHostModels':hosts,'cards':cards,
         'exactRecipeApproval':False,'runtimeImplemented':False,'balanceApproved':False,
         'sourcePreservation':'Original public-book paragraphs are preserved verbatim; active candidate wording completes their operating procedure. Source wording does not override that procedure.'}
    dump(dest,obj);outputs=[dest,R/GUIDE,R/BODY]
    for trade in ['Enchanting','Rune Carving','Scribing','Tinkering']:
        cs=[c for c in cards if c['sourceRecipe']['skill']==trade];p=R/f"docs/mechanics/{trade.upper().replace(' ','_')}_CANDIDATE_RECIPE_CARDS.md"
        assert not p.exists();p.write_text(f'# {trade} — player recipe candidates\n\n**{len(cs)} public candidate cards; exact review pending.** Use the complete operating guide and body catalogue.\n\n'+'\n'.join(c['manuscriptText'] for c in cs),encoding='utf-8');outputs.append(p)
    dump(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json',{'status':'Explicit draft projection; validation pending','internalCandidateSha256':sha(ip),'entries':ledger,'publicRecipes':100,'withheldRestrictedRecipes':7,'withheldDirectorRecipes':60,'publicBodies':15,'withheldBodyIds':sorted(set(d['bodyModels'])-set(bodies))})
    protected=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes'];assert all(sha(G/p)==h for p,h in protected.items())
    report={'status':STATUS,'createdAtUtc':datetime.now(timezone.utc).isoformat(),'publicRecipes':100,'publicBodies':15,'existingHostTemplates':len(hosts),'bookParagraphs':sum(len(c['publicBookBinding']['paragraphs']) for c in cards),
            'publicComponentMentions':sum(len(c['sourceRecipe']['components']) for c in cards),'independentlyPublicSupplementalProfiles':sum('publicMaterialProfile' in m for c in cards for m in c['sourceRecipe']['components']),
            'outputHashes':{p.relative_to(G).as_posix():sha(p) for p in outputs},'protectedSourceFilesUnchanged':len(protected),'newApprovals':0,
            'remainingWork':['Independent complete public-envelope and source-preservation validation','Finite behavior/state-sequence fixtures','Separate exact GPT review of all167 actual candidates']}
    dump(A/'ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json',report);print(json.dumps({k:v for k,v in report.items() if k!='outputHashes'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
