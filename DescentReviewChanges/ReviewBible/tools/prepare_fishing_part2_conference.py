"""Current Fishing source conference after the fulfilled Jewelcrafting review."""
from pathlib import Path
import json,hashlib
from prepare_combat_feat_source_audit import section
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(d):return json.dumps(d,ensure_ascii=False,separators=(',',':'))
def write(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    dest=AUDIT/'FISHING_PART2_SUBMISSION.json';assert not dest.exists()
    original=AUDIT/'CODEX_FISHING_SOURCE_EVIDENCE_PREPARED.txt';old_status=read(AUDIT/'FISHING_SOURCE_PACKET_STATUS.json')
    assert sha(original)==old_status['packetSha256']=='193ad24ca70aec126cd023104eb6ce6cae1565cec69876ba6825543e8f56e084'
    prep=read(AUDIT/'FISHING_SOURCE_PREPARATION.json');source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    recipes=[r for r in read(source)['recipes'] if r['skill']=='Fishing']
    assert len(recipes)==44 and recipes==prep['recipes'] and sha(source)==prep['sourceSha256']
    protected={source.relative_to(GAME).as_posix():sha(source),original.relative_to(GAME).as_posix():sha(original)}
    manifests=[]
    for name in ('ALCHEMY','HERBALISM','COOKING','POISONCRAFTING','BLACKSMITHING','LEATHERWORKING','TAILORING','JEWELCRAFTING'):
        p=ROOT/f'docs/mechanics/{name}_REVIEW_STATUS.json';m=read(p)
        assert m['status'].startswith('REVIEWED') and all(sha(GAME/q)==h for q,h in m['artifactHashes'].items())
        manifests.append(m);protected[p.relative_to(GAME).as_posix()]=sha(p);protected.update(m['artifactHashes'])
    refs={
      'CRAFTING_HARVEST_PLAYTEST.md':None,'CRAFTING_TRADE_REFERENCE.md':None,
      'EQUIPMENT_ACQUISITION_PLAYTEST.md':None,'BODY_EQUIPMENT_PLAYTEST.md':None,
      'LEATHERWORKING_RECIPE_PLAYTEST.md':None,'TAILORING_RECIPE_PLAYTEST.md':None,'JEWELCRAFTING_RECIPE_PLAYTEST.md':None,
      'COOKING_RECIPE_PLAYTEST.md':['Food mass and the food ledger','Containers and capacity','Cooking, stabilization and storage','Whole-creature Masterwork traits'],
      'CORE_RESOLUTION_PLAYTEST.md':['Which rule applies','Rolls'],
      'COMBAT_ACTION_PLAYTEST.md':['Encounter and action resources','Time and event ordering — NEW'],
      'CONTROL_STATES_PLAYTEST.md':['Records, clocks and precedence','Compulsion, action denial and initiative'],
      'CREATURE_LIFECYCLE_PLAYTEST.md':['At the table','Different kinds of creature life','Stats and ownership'],
      'GAMEPLAY_LOOP_CANON.md':['5. Opening clock and Watches','6. Route procedure','Resource Team','Team check procedure','Supply Units','15. Harvesting and salvage']}
    excerpts=[]
    for name,heads in refs.items():
        p=ROOT/'docs/mechanics'/name;t=p.read_text(encoding='utf-8');protected[p.relative_to(GAME).as_posix()]=sha(p)
        for h in heads or [None]:
            text=section(t,h) if h else t
            excerpts.append({'file':p.relative_to(GAME).as_posix(),'heading':h,'sha256':sha(p),'exactText':text,'scope':'Existing source procedure; later reviewed Core/crafting/equipment/body rules control conflicts. The full travel/Supply domain has not completed its operational audit.' if name=='GAMEPLAY_LOOP_CANON.md' else 'Existing operational guide, only its stated reviewed scope.'})
    receipt=read(AUDIT/'JEWELCRAFTING_EXACT_REPAIRS_APPLIED.json');validation=read(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json')
    assert receipt['status'].startswith('PASS') and validation['recipesApproved']==43 and validation['checkCount']==131 and validation['protectedFilesUnchanged']==54
    cover='''Codex to Calibration Review Part 2: FISHING source/interface conference in TWO parts. Please acknowledge PART A receipt only and wait for PART B before giving decisions.

Your Jewelcrafting exact verdict turn3074a6c4-b718-4241-ae05-f6b3ed1238b0/reply872837f3-e844-4e3f-9a79-068060b62213 has been implemented within JC-ER01..03. We preserved the submitted15-file revision and all20 files in your downloaded evidence archive. All19 archive member hashes verified; your reconstructed internal/public manuscripts exactly match the preserved submitted bytes. JC-ER01 now requires campaign/epoch/time/scheduler-order/preceding-dawn checkpoints and rejects unresolved dawns or earlier transitions. JC-ER02 binds both trade views to one actual roll ID and consistent roll descriptors, preserving item-specific current-event premises and protected older helpers. JC-ER03 derives recipe268 DC19/body2gp/finished4509gp and positively checks8h,1127.25gp reconstruction; both original-constituent negatives now use that same source-bound profile. Corrected local131 checks,69 predicate cases,486 structural states and86 values pass;54 protected inputs unchanged. Complete public cards,guide andJSON reconstruct exactly. All43 cards are now promoted under your finite authorization. No unchanged-card resubmission is requested.

Current recipe progress348/687 reviewed,339remaining;public223/433. Fishing44 is wholly pending:28public,3restricted,13Director-only. Part A provides exact current rule dependencies, final repair evidence and the corrected bounded helper. Part B supplies44 complete original records,28 V5 book bindings,212 consumed component occurrences,nine equipment references,three legacy boat transitions,one literal bestiary reference and24 concrete scenarios. Earlier pending/unsent/Leatherworking-active wording in the preserved prepared packet is historical; this cover supplies current logistics.

After Part B, provide finite FI-D authoring decisions covering all FI-01..24 scenarios and every clause. Clearly distinguish preserved rules from NEW completions. Set a usable finite fishing attempt, site/opportunity/creature identity and depletion ledger; nine complete equipment/consumable bodies; actual user/assembly/hands/deployment/setting/retrieval limits; bonus/extra-yield/attraction eligibility and combination; meat/material unit identity,mass and availability; consumable bait states and clocks; suppression,Broken,meld,custody,release/recapture; creation,quality,actual non-artisan tools,field flags,repair and value. The Fishing ability is WIS and tackle is a non-artisan tool credential; an artisan-only Forge Dwarf benefit is not automatically admitted. Existing Forage/Supply and harvest source procedures are supplied with their actual scope, not blanket domain approval. Resolve their interface explicitly without silent duplicate production or inventing a new ecology from item names.

Do not import external game rules. Legacy Fishing Boat names/effects remain preserved and need an explicit later transport disposition; current Tackle does not silently become a boat. No ingredient/creature availability, automatic summon/charm/control, fresh anatomy, extra unique organs or unknown market price follows from a donor/affinity name. Preserve every source and all visibility/nested guidance gates. Souls,Unholy,aligned and similar names authorize no cosmology decision. Cosmology stays after the successful authorized GitHub push and verified remote commit. No deletion or push has occurred; whole-game final flow,human balance,availability and companion runtime remain open.

Please return the eventual completed source verdict in full and, if lengthy, also as a verbatim UTF-8 Markdown download. Source decisions permit authoring, not exact operational-card promotion; a separate exact review follows.
'''
    partA=cover+'\nFULFILLED JEWELCRAFTING REPAIR RECEIPT\n'+compact(receipt)
    partA+='\nCORRECTED BOUNDED REFERENCE — NOT COMPANION RUNTIME\n'+(ROOT/'tools/jewelcrafting_reference.py').read_text(encoding='utf-8')
    partA+='\nLOCAL CORRECTED VALIDATION CASES\n'+compact({k:validation[k] for k in ('status','checkCount','checks','crossTradeSourceFixtures','structuralStates','protectedFilesUnchanged','artifactHashes')})
    partA+='\nEXACT CURRENT GOVERNING DEPENDENCIES\n'+compact(excerpts)
    partA+='\nCURRENT VERIFIED LAST-TRADE REVIEW MANIFESTS\n'+compact(manifests[-3:])+'\nEND PART A. Acknowledge receipt only; await Part B.'
    partB='''Codex: PART B completes the FISHING SOURCE/INTERFACE conference. Both parts are now available. Please resolve every FI-01..24 scenario through finite FI-D authoring decisions using the full originals and current dependencies. Current reviewed totals348/687,public223/433. Fishing44 remains unapproved. The following preparation is preserved verbatim; its unsent/Leatherworking-active logistics are historical and superseded by this cover and Part A. No source developed flag grants operational approval. Please give source authoring decisions, then we will author and return exact cards for separate review. Cosmology stays post-push only.

'''+original.read_text(encoding='utf-8')+'\n\nEND COMPLETE FISHING SOURCE CONFERENCE. All44 full sources and24 scenarios are supplied. Zero Fishing approvals. Return a full finite disposition and a verbatim UTF-8 Markdown download if long.'
    assert all(sha(GAME/p)==h for p,h in protected.items())
    status={'status':'Prepared current two-part Fishing source conference; not sent','threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','sourceRecipes':44,'public':28,'restricted':3,'directorOnly':13,'sourceScenarios':24,'currentGuideExcerpts':len(excerpts),'protectedFiles':protected,'sourceInformationDeleted':0,'recipesApproved':0,'currentReviewedTotal':348,'remaining':339,'publicReviewed':223,'parts':{},'cosmology':'post-push only'}
    for label,t in [('A_CURRENT_RULES',partA),('B_COMPLETE_SOURCES',partB)]:
        p=AUDIT/f'CODEX_FISHING_PART2_{label}.txt';write(p,t);status['parts'][label]={'file':p.name,'characters':len(t),'sha256':sha(p),'sent':False}
    write(dest,json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(compact({'parts':status['parts'],'protectedFiles':len(protected),'currentGuideExcerpts':len(excerpts),'sourceRecordsExact':len(recipes)}))
if __name__=='__main__':main()
