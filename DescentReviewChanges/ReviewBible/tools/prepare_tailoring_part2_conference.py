"""Preserve prepared source evidence and add the actual completed dependency context."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def main():
    status_path=AUDIT/'TAILORING_PART2_SUBMISSION.json';assert not status_path.exists()
    original=read(AUDIT/'TAILORING_SOURCE_PACKET_STATUS.json');packet=AUDIT/original['packetFile'];assert sha(packet)==original['packetSha256']
    leather=read(ROOT/'docs/mechanics/LEATHERWORKING_REVIEW_STATUS.json')
    assert leather['status'].startswith('REVIEWED') and all(sha(GAME/p)==h for p,h in leather['artifactHashes'].items())
    report=read(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json');assert report['status']=='PASS' and sha(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json')==leather['validationSha256']
    sources=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes'];evidence=read(AUDIT/'TAILORING_SOURCE_PREPARATION.json')
    assert evidence['recipes']==[r for r in sources if r['skill']=='Tailoring']
    guides=['BODY_EQUIPMENT_PLAYTEST.md','CRAFTING_HARVEST_PLAYTEST.md','CRAFTING_TRADE_REFERENCE.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','BLACKSMITHING_RECIPE_PLAYTEST.md']
    context=[ROOT/'docs/mechanics'/p for p in guides]+[ROOT/'docs/director-only/LEATHERWORKING_INTERNAL_GUIDE.md']
    protected=dict(read(AUDIT/'LEATHERWORKING_PART2_REVIEW_BASELINE.json')['files'])
    assert all(sha(GAME/p)==h for p,h in protected.items())
    for p in context+[GAME/p for p in leather['artifactHashes']]+[ROOT/'docs/mechanics/LEATHERWORKING_REVIEW_STATUS.json',ROOT/'tools/leatherworking_reference.py',AUDIT/'TAILORING_SOURCE_PREPARATION.json',AUDIT/'TAILORING_SOURCE_VERSION_AUDIT.json',packet]:protected[p.relative_to(GAME).as_posix()]=sha(p)
    dump(AUDIT/'TAILORING_PART2_REVIEW_BASELINE.json',{'scope':'Protected original sources and completed prior rules, including final reviewed Leatherworking; no new Tailoring approval','files':protected})
    cover='''Codex to Calibration Review Part 2: TAILORING SOURCE/INTERFACE CONFERENCE, in TWO parts.

First, your completed Leatherworking exact verdict (turn2a3db078-0ab3-411a-a9d2-aeb19da8765e/reply1f8a8f86-3d64-4665-8d7f-cd315727a240) is captured. Both finite evidence repairs are implemented. LW-ER01 documents the already-eligible suit-grade contract, uses None for the unselected suit under explicit alternative-formula legality, and separately tests selected Crude/no-positive, zero-recipe and positive-recipe cases. LW-ER02 identifies the Tiny transformed140-lb body, existing1.5 casualty Load,15lb/1.5Load melded cargo, no other equipment and inactive relief:155lb/3Load, with handling/anatomy still required. All91 local checks and52 cases pass;2,832 durability and1,065 burden states pass;42 protected files remain unchanged. Exact manuscript public projection has570 references and reconstructs exactly. These are local evidence, not checks attributed to you. Only evidence and operational review-status/provenance labels changed; all source records, bodies and effect rules are preserved. Under your express finite-repair authorization, all44 Leatherworking cards are now reviewed authored operational PLAYTEST. Totals262/687 reviewed,425remaining;public168/433. No runtime/balance/whole-game/publication approval, deletion or push. Cosmology remains strictly after successful authorized GitHub push and verified remote commit.

Please acknowledge PART A only, and wait for PART B before the Tailoring decision. This part supplies the completed exact verdict, fulfilled-repair evidence, final manifest and complete current reviewed governing guides. Part B supplies all43 full source records,29 exact public V5 bindings,20 equipment references, full version evidence and20 unresolved Tailoring scenarios, losslessly factored.

The preserved Tailoring evidence was prepared before Leatherworking completed. Its statements that Leatherworking is pending and its earlier262/218-style counters are historical preparation context, superseded by this cover and the actual reviewed rules below. Do not erase the older packet or treat its open questions as decisions. Tailoring has no authored operational-card approval yet. This conference requests explicit source/interface directions sufficient to author all43 finite cards; exact manuscript review follows authoring.
'''
    a='\n\n'.join([cover,'COMPLETED LEATHERWORKING EXACT VERDICT\n'+(AUDIT/'GPT_LEATHERWORKING_EXACT_VERDICT.md').read_text(encoding='utf-8'),'LOCAL FULFILLED-REPAIR RECEIPT\n'+(AUDIT/'LEATHERWORKING_EXACT_REPAIRS_APPLIED.json').read_text(encoding='utf-8'),'FINAL LEATHERWORKING REVIEW MANIFEST\n'+json.dumps(leather,ensure_ascii=False),*[p.relative_to(GAME).as_posix()+' — COMPLETE CURRENT GUIDE\n'+p.read_text(encoding='utf-8') for p in context],'END PART A. Acknowledge receipt only; complete source evidence follows in Part B.'])
    b='''Codex: PART B completes the Tailoring source/interface conference. Part A supplied the now-reviewed Leatherworking rules and complete current dependencies. Please now give numbered finite decisions for authoring all43 Tailoring cards; do not mark source direction as exact-card approval.

Resolve all20 scenarios and every nine-family body/slot/effect binding, including five Bag containers and38 garments; source relief versus actual capacity, cross-trade stacking and nesting; exact social/stealth/environmental task domains and actual actor; seven printed resistances including bludgeoning; Gloves/Gauntlets, Hat/Helm and armor/robe/cloak/coat layers; Climbing Cord, Veilcloth and Living Mantle physical identities; complete output bodies or quantified supplemental stock; ordered maximum-yield reserves/latest damage/flaw; source25 reusable tools versus165 consumed components, including high-tier tool values, no catalysts; workstation/field flags, year-null584, quality/Forge Dwarf, mundane-base versus finished-unit reconstruction prices and all source preservation. Do not invent powers solely from names/tags, donor traits or cosmology. Decide finite missing body values and declare them as new playtest overlays, not recovered source facts.

The following prepared packet is copied EXACTLY, including its historical pre-conference notices. The present cover supersedes only those timing/status notices. Its full original sources, unresolved questions, preserved version differences and public bindings remain evidence. Current totals262/687 reviewed,425remaining;public168/433. No Tailoring cards are approved yet. Final game flow and delivery remain later; cosmology is post-push only.

BEGIN UNMODIFIED PRESERVED SOURCE PACKET
'''+packet.read_text(encoding='utf-8')+'\nEND PART B. Please deliver the complete Tailoring source/interface authoring directions with any unresolved conflicts explicitly identified.\n'
    status={'status':'prepared-not-sent','threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','scope':'source/interface direction only; exact-card review follows authoring','parts':{},'protectedFiles':len(protected),'sourceRecipes':43,'publicBookBindings':29,'sourcePacketSha256':sha(packet),'reviewedTotal':262,'remaining':425,'recipesApproved':0,'cosmology':'post-push only'}
    for label,text in [('A_REVIEWED_CONTEXT',a),('B_FULL_SOURCE',b)]:
        p=AUDIT/f'CODEX_TAILORING_PART2_{label}.txt';assert not p.exists();write(p,text);status['parts'][label]={'file':p.name,'characters':len(text),'sha256':sha(p),'sent':False}
    dump(status_path,status);print(json.dumps(status))
if __name__=='__main__':main()
