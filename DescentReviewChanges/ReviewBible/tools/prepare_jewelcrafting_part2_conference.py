"""Fresh source conference with completed Tailoring/Leatherworking dependencies."""
from pathlib import Path
import json,hashlib
from prepare_combat_feat_source_audit import section

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def compact(d):return json.dumps(d,ensure_ascii=False,separators=(',',':'))

def main():
    dest=AUDIT/'JEWELCRAFTING_PART2_SUBMISSION.json';assert not dest.exists()
    source=ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    prep=read(AUDIT/'JEWELCRAFTING_SOURCE_PREPARATION.json')
    recipes=[r for r in read(source)['recipes'] if r['skill']=='Jewelcrafting']
    assert recipes==prep['recipes'] and len(recipes)==43 and sha(source)==prep['sourceSha256']
    original=AUDIT/'CODEX_JEWELCRAFTING_SOURCE_EVIDENCE_PREPARED.txt'
    assert sha(original)=='a9612a2f040eff88d49fe09ce3837d0d19939f0cad3806b205c169cb89930951'
    protected={source.relative_to(GAME).as_posix():sha(source),original.relative_to(GAME).as_posix():sha(original)}
    manifests=[]
    for name in ['ALCHEMY','HERBALISM','COOKING','POISONCRAFTING','BLACKSMITHING','LEATHERWORKING','TAILORING']:
        p=ROOT/f'docs/mechanics/{name}_REVIEW_STATUS.json';m=read(p)
        assert m['status'].startswith('REVIEWED') and all(sha(GAME/q)==h for q,h in m['artifactHashes'].items())
        manifests.append(m);protected[p.relative_to(GAME).as_posix()]=sha(p);protected.update(m['artifactHashes'])
    refs={
      'CRAFTING_HARVEST_PLAYTEST.md':None,'EQUIPMENT_ACQUISITION_PLAYTEST.md':None,
      'BODY_EQUIPMENT_PLAYTEST.md':None,'LEATHERWORKING_RECIPE_PLAYTEST.md':None,'TAILORING_RECIPE_PLAYTEST.md':None,
      'CORE_RESOLUTION_PLAYTEST.md':['Which rule applies','Rolls'],
      'COMBAT_ACTION_PLAYTEST.md':['Encounter and action resources','Time and event ordering — NEW'],
      'CONTROL_STATES_PLAYTEST.md':['Records, clocks and precedence','Compulsion, action denial and initiative'],
      'CONDITIONS_PLAYTEST.md':['Incapacitated','Poisoned','Unconscious']}
    excerpts=[]
    for name,heads in refs.items():
        p=ROOT/'docs/mechanics'/name;t=p.read_text(encoding='utf-8');protected[p.relative_to(GAME).as_posix()]=sha(p)
        for h in heads or [None]:excerpts.append({'file':p.relative_to(GAME).as_posix(),'heading':h,'sha256':sha(p),'exactText':section(t,h) if h else t})
    receipt=read(AUDIT/'TAILORING_EXACT_REPAIRS_APPLIED.json');validation=read(AUDIT/'TAILORING_CANDIDATE_VALIDATION.json')
    assert receipt['status'].startswith('PASS') and validation['recipesApproved']==43 and validation['checkCount']==157
    cover="""Codex to Calibration Review Part 2: next source/interface conference, JEWELCRAFTING, in TWO parts. Acknowledge PART A receipt only and wait for PART B before authoring decisions.

Your Tailoring exact verdict (turn b6984844-5544-4ff0-9624-50bab432dbb2, reply54b2b40e-cce6-48c4-8aa6-51ea7c535f0c) is implemented within TA-ER01..04. Item-specific task qualification now precedes strongest-value comparison, all designations are checked before filtering, Leatherworking containers route to their actual operator, source-valid fixtures replace the invalid combinations, and both guides/all card repair paragraphs require the actual Weaver toolkit. Local157 checks and558 durability states pass;53 protected inputs unchanged. Complete public JSON envelope equality and exact public manuscript paragraph reconstruction pass. All43 Tailoring cards are operationally promoted under your conditional authorization. Submitted files and your downloaded reviewer archive remain separate internal evidence. No unchanged-card resubmission is requested.

Current operational recipe pass:305/687 reviewed,382remaining;public197/433. No Jewelcrafting recipe is approved. Part A supplies exact current reviewed dependency text and final Tailoring evidence. Part B supplies all43 Jewelcrafting original records,26 exact public bindings,10 complete equipment references,source-version comparison,all11 catalyst rows and24 detailed source scenarios. All earlier draft/pending counts in the preserved preparation describe its historical preparation time; this cover is the current state. Keep the original source objects unchanged.

After Part B, give finite numbered JC-D authoring decisions that cover every JC-01..24 scenario:14 tag predicates for checks/saves, passive+1/+2/+3 scope and charge timing, finite slots/bodies, dawn-event identity and persistent charge ledgers, suppression/Broken/meld/transfer, creation/quality/catalysts, actual tools/repair and value. Explicitly distinguish preserved rules from NEW completions. Attach exact mechanical dependencies if an issue cannot be settled from these supplied texts; do not claim access to local file paths. Human balance and availability remain separate. Sources saying souls/spirit/Unholy or naming donors do not authorize cosmology changes. Defer cosmology until after successful authorized GitHub push and remote verification. Whole-game final flow review is still later; no push or deletion has occurred.
"""
    partA=cover+'\nFINAL TAILORING REPAIR RECEIPT\n'+compact(receipt)+'\nFINAL TAILORING SOURCE-BOUND VALIDATION CASES\n'+compact({k:validation[k] for k in ['status','checkCount','checks','durabilityStates','sourceBoundFixtures','repairProcedureContract','nestedFixturePremises']})
    partA+='\nCORRECTED BOUNDED TAILORING HELPER (not companion runtime)\n'+(ROOT/'tools/tailoring_reference.py').read_text(encoding='utf-8')
    partA+='\nEXACT CURRENT RULE DEPENDENCIES (each retains its stated scope)\n'+compact(excerpts)
    partA+='\nCURRENT VERIFIED REVIEW MANIFESTS\n'+compact(manifests[-2:])+'\nEND PART A. Please acknowledge receipt only; Part B follows.'
    old=original.read_text(encoding='utf-8')
    body=old[old.index('Lossless source format:'):]
    partB="""Codex: PART B completes the JEWELCRAFTING SOURCE/INTERFACE conference. Both parts are now available. Please give finite JC-D authoring decisions with explicit NEW completions and resolve the24 scenarios below. Current totals305/687,public197/433;Jewelcrafting43 allpending. The source-preparation audit below remains preserved historical evidence; its 'unsent'/'Leatherworking pending' logistics are superseded by this cover and Part A. Do not treat source developed flags as exact-card approval. Authoring follows your decisions, then a separate exact-card review. Cosmology remains post-push only.

"""+body+'\n\nEND COMPLETE SOURCE CONFERENCE. All source records retained; zero Jewelcrafting approvals.'
    assert all(sha(GAME/p)==h for p,h in protected.items())
    status={'status':'Prepared two-part source conference; not sent','threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','sourceRecipes':43,'public':26,'restricted':1,'directorOnly':16,'sourceScenarios':24,'currentGuideExcerpts':len(excerpts),'protectedFiles':protected,'sourceInformationDeleted':0,'recipesApproved':0,'currentReviewedTotal':305,'remaining':382,'publicReviewed':197,'parts':{},'cosmology':'post-push only'}
    for label,t in [('A_CURRENT_RULES',partA),('B_COMPLETE_SOURCES',partB)]:
        p=AUDIT/f'CODEX_JEWELCRAFTING_PART2_{label}.txt';assert not p.exists();write(p,t)
        status['parts'][label]={'file':p.name,'characters':len(t),'sha256':sha(p),'sent':False}
    write(dest,json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(compact({'parts':status['parts'],'protectedFiles':len(protected),'currentGuideExcerpts':len(excerpts),'sourceRecordsExact':len(recipes)}))
if __name__=='__main__':main()
