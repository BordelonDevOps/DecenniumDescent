"""Refresh the preserved Leatherworking preparation after actual Blacksmith review."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,zipfile,xml.etree.ElementTree as E
from prepare_cooking_exact_review import merge
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def write_new(p,s):
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    original=AUDIT/'CODEX_LEATHERWORKING_SOURCE_CONFERENCE.txt';old=original.read_text(encoding='utf-8')
    baseline=read(AUDIT/'LEATHERWORKING_REVIEW_BASELINE.json');assert len(baseline['files'])==36
    assert all(sha(GAME/p)==h for p,h in baseline['files'].items())
    manifest_path=ROOT/'docs/mechanics/BLACKSMITHING_REVIEW_STATUS.json';manifest=read(manifest_path)
    assert manifest['status'].startswith('REVIEWED') and all(sha(GAME/p)==h for p,h in manifest['artifactHashes'].items())
    validation=read(AUDIT/'BLACKSMITHING_CANDIDATE_VALIDATION.json');assert validation['status']=='PASS' and len(validation['checks'])==131
    evidence=read(AUDIT/'LEATHERWORKING_SOURCE_PREPARATION.json')
    source=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json');recipes=[r for r in source['recipes'] if r['skill']=='Leatherworking'];assert recipes==evidence['recipes'] and len(recipes)==44
    source_header='COMPLETE SOURCE RECORDS — COMMON plus recursive per-recipe overrides, arrays replace whole arrays'
    source_start=old.index(source_header);public_start=old.index('EXACT PUBLIC V5 PARAGRAPHS AND STRUCTURAL SOURCE AUDIT');equipment_start=old.index('COMPLETE SELECTED EQUIPMENT RECORDS AND EXPLICIT SOURCE CONFLICTS')
    packed=json.loads(old[source_start+len(source_header):public_start].strip());assert all(merge(packed['COMMON'],packed['recipeOverrides'][r['id']])==r for r in recipes)
    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx';assert sha(book)==evidence['bookSha256']
    with zipfile.ZipFile(book) as z:tree=E.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';paragraphs=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    assert len(evidence['publicBookBindings'])==30 and all(paragraphs[p['index']]==p['text'] for b in evidence['publicBookBindings'] for p in b['paragraphs'])
    interface=deepcopy(read(AUDIT/'LEATHERWORKING_INTERFACE_EVIDENCE.json'))
    interface['historicalPendingBlacksmithGuide']=interface.pop('pendingBlacksmithGuide')
    interface['historicalPendingBlacksmithGuide']['operative']=False
    interface['reviewedBlacksmithGuide']={'path':'DescentReviewChanges/ReviewBible/docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md','sha256':sha(ROOT/'docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md'),'exactReviewThreadId':manifest['exactReviewThreadId'],'exactReviewTurnId':manifest['exactReviewTurnId'],'exactReplyId':manifest['exactReplyId'],'status':manifest['status']}
    interface['historicalPreparationChecks']=interface.pop('checks')
    equipment=read(ROOT/'data/playtest/equipment_acquisition_candidate.json')['items'];eq={r['id']:r for r in equipment};assert all(eq[r['id']]==r for r in interface['completeEquipmentRecords'])
    questions=(AUDIT/'LEATHERWORKING_SOURCE_QUESTIONS.md').read_text(encoding='utf-8')
    start=questions.index('The current recipe index records ');end=questions.index('\n\n',start)
    questions=questions[:start]+'Blacksmithing exact review is now complete in this Part 2 chat: all four finite-repair requirements are implemented and validated. Its current full guide is supplied in Part A and controls this conference; any historical pending label below is superseded. Current operational counts are 218/687 reviewed, 469 remaining, public138/433 reviewed. These counts preserve prior authoring and approvals. Leatherworking still has no newly approved operational cards.'+questions[end:]
    questions=questions.replace('source conference — prepared, not sent','source conference — Part 2 current questions').replace("Blacksmithing's proposed defense-enhancement family","Blacksmithing's reviewed defense-enhancement family").replace('Blacksmithing gauntlet pair currently proposes','Blacksmithing gauntlet pair occupies').replace('confirm the final cross-trade relationship only after its exact review','define the cross-trade relationship consistently with its completed exact review')
    receipt='Codex to Calibration Review Part 2 — Blacksmithing completion receipt and Leatherworking source conference, Part A of 2.\n\nYour exact verdict (turn '+manifest['exactReviewTurnId']+', reply '+manifest['exactReplyId']+') authorized promotion after exact repairs and validation without another generic Blacksmithing conference. All BS-01–04 conditions are satisfied. The original submission and source records are preserved. All 43 cards are now REVIEWED for authored operational PLAYTEST only. Local validation passed 131 checks, including 20 timing cases, 4,116 durability states and 248 model-choice examples; 32 protected source/prior-rule files are unchanged. Public27 is an exact deep filtered derivation of internal43, with corrected common rules, permitted reviewed equipment, and no nested gated recipe/guidance leakage. Final artifact and evidence hashes were pinned before the index changed to218/687, public138/433. Source status/needsReview/legacy fields were never overwritten. These are local checks, distinct from your own 2,816 durability and12 timing cases. Runtime and balance remain false.\n\nThis Part A supplies the current reviewed cross-system rules and completed Blacksmithing guide. Part B will supply every one of the44 original Leatherworking recipes, all30 exact V5 public paragraph bindings,31 complete equipment records,11 cross-version AC conflicts and20 concrete scenarios. Please acknowledge receipt only and wait for Part B before the source/interface decisions. No unchanged Blacksmithing re-review is requested. Final joint flow review still precedes GitHub push; cosmology remains only after a successful push and verified remote commit.\n\n'
    context_start=old.index('EXISTING REVIEWED GUIDE: ');context_end=old.index('PENDING BLACKSMITHING GUIDE')
    context=old[context_start:context_end].strip()
    # Verify each quoted guide against its exact current file before transferring.
    for path,h in interface['reviewedGuideHashes'].items():assert sha(ROOT/path)==h
    receipt+='BLACKSMITHING FINAL HASH/STATUS MANIFEST\n'+compact(manifest)+'\n\n'
    receipt+='LOCAL TIMING CASE RESULTS\n'+compact([{'name':c['name'],'pass':c['pass']} for c in validation['part2Evidence']['timingCases']])+'\n\n'
    part_a=receipt+context+'\n\nCURRENT REVIEWED BLACKSMITHING GUIDE — SUPERSEDES HISTORICAL PENDING DRAFT\n'+(ROOT/'docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8')
    part_b='Codex to Calibration Review Part 2 — Leatherworking source conference, Part B of 2 (complete source/evidence and decision request). Part A supplied actual reviewed governing rules and completed Blacksmithing guide. Please now resolve all source/interface questions and twenty concrete scenarios below for all44 recipes. Give a concrete finite operational specification and distinguish existing authority from new authored completion. Preserve all original fields and both sides of conflicts. This is a source conference before exact card authoring, not a request to approve nonexistent completed cards. Do not infer effects or cosmology from names.\n\n'+questions+'\n\n'+old[source_start:equipment_start].strip()+'\n\nCOMPLETE SELECTED EQUIPMENT RECORDS AND EXPLICIT SOURCE CONFLICTS\n'+compact(interface)+'\n\n'+(AUDIT/'LEATHERWORKING_REVIEW_SCENARIOS.md').read_text(encoding='utf-8')
    outputs={'A_RULES':('CODEX_LEATHERWORKING_PART2_A_RULES.txt',part_a),'B_SOURCE':('CODEX_LEATHERWORKING_PART2_B_SOURCE.txt',part_b)}
    parts={}
    for key,(name,text) in outputs.items():
        p=AUDIT/name;write_new(p,text);parts[key]={'file':name,'sha256':sha(p),'characters':len(text),'sent':False}
    status={'status':'prepared for authorized existing Part 2; not yet sent','threadId':manifest['exactReviewThreadId'],'parts':parts,'originalPreparedPacketSha256':sha(original),'sourceOriginalsUnchanged':True,'sourceReconstructions':44,'publicBookBindings':30,'completeEquipmentRecords':31,'protectedSourceAndRuleFilesUnchanged':36,'reviewedBlacksmithArtifactsVerified':5,'sourceArmorConflicts':11,'scenarios':20,'recipesApproved':0,'currentRecipePassTotals':read(ROOT/'data/director/crafting_recipe_review_catalog.json')['totals'],'cosmology':'post-push only'}
    write_new(AUDIT/'LEATHERWORKING_PART2_SUBMISSION.json',json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    print(compact(status))
if __name__=='__main__':main()
