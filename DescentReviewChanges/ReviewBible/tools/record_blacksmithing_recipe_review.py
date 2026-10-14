"""Record the actual Part 2 finite-repair approval, with evidence before indexing."""
from pathlib import Path
from collections import Counter
import hashlib,json,shutil,subprocess,sys
from build_blacksmithing_recipe_candidate import EXACT_THREAD,EXACT_TURN,EXACT_REPLY

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
BACKUP=AUDIT/'blacksmithing-before-part2-promotion'
LABEL='REVIEWED — authored operational PLAYTEST Blacksmithing recipe set'
FILES=['docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md','docs/mechanics/BLACKSMITHING_PUBLIC_RECIPE_CARDS.md','docs/director-only/BLACKSMITHING_INTERNAL_RECIPE_CARDS.md','data/playtest/blacksmithing_recipe_candidate.json','data/director/blacksmithing_recipe_candidate_internal.json']
REPAIRS=[
 'BS-01: exact anchored outside windows, trigger-bound entry guards, actual host-turn budgets, exit lockout and expenditure-before-mitigation state procedure.',
 'BS-02: physical identity and latest lawful completion HP; functional means at least 1 current HP; singleton Flawed can produce a Broken dormant imprint.',
 'BS-03: all sixteen defensive cards state exact suit/shield/accessory eligibility; resistance stays separate; melded items give no active wearing benefits.',
 'BS-04: original revision preserved, actual Part 2 verdict pinned, fresh source/behavior/projection checks passed, public route proven and final hashes recorded before index promotion.']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def relative(p):return p.relative_to(GAME).as_posix()
def backup(p):
    q=BACKUP/p.relative_to(GAME);assert not q.exists(),q
    q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
def write(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def main():
    manifest=ROOT/'docs/mechanics/BLACKSMITHING_REVIEW_STATUS.json'
    assert not manifest.exists(),'Promotion already exists; inspect it rather than rerunning.'
    # Validate the actual corrected files again after final validator edits.
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/validate_blacksmithing_recipe_candidate.py')],check=True)
    report_path=AUDIT/'BLACKSMITHING_CANDIDATE_VALIDATION.json';report=read(report_path)
    assert report['status']=='PASS' and len(report['checks'])==131 and len(report['part2Evidence']['timingCases'])==20
    verdict=AUDIT/'GPT_BLACKSMITHING_PART2_EXACT_REVIEW.txt'
    assert 'sufficient for promotion without another generic Blacksmithing conference' in verdict.read_text(encoding='utf-8')
    paths=[ROOT/p for p in FILES]
    mutable=paths+[report_path,ROOT/'data/playtest/game_development_coverage.json',GAME/'START_HERE.md',AUDIT/'REVIEW_STATUS.md',AUDIT/'BLACKSMITHING_PART2_SUBMISSION.json',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',ROOT/'data/director/crafting_recipe_review_catalog.json',ROOT/'data/playtest/crafting_recipe_review_catalog_public.json',ROOT/'docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md',AUDIT/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json']
    for p in mutable:backup(p)
    dump(BACKUP/'MANIFEST.json',{'purpose':'Corrected and validated state before review-status and index promotion','files':{relative(p):sha(p) for p in mutable}})
    repairs_path=AUDIT/'BLACKSMITHING_PART2_REPAIRS_APPLIED.json'
    dump(repairs_path,{'status':'PASS; exact finite repairs implemented and validated before promotion','exactReviewThreadId':EXACT_THREAD,'exactReviewTurnId':EXACT_TURN,'exactReplyId':EXACT_REPLY,'repairs':REPAIRS,'correctedPrePromotionArtifactHashes':{relative(p):sha(p) for p in paths},'validationSha256BeforePromotion':sha(report_path),'verdictSha256':sha(verdict),'checks':131,'localTimingCases':20,'localDurabilityStates':4116,'modelChoiceExamples':248,'sourceInformationDeleted':0,'originalSubmittedRevisionBackup':'docs/audit/2026-10-08/full-game/blacksmithing-before-part2-repairs','correctedPrePromotionBackup':relative(BACKUP)})
    for p in paths[:3]:
        s=p.read_text(encoding='utf-8').replace('**Exact review finite repairs applied; validation pending.**','**'+LABEL+'.**')
        s=s.replace('BS-01 through BS-03 are applied; BS-04 validation must pass before promotion.','All four exact-review requirements are satisfied; 131 local checks pass, including 20 timing cases. Runtime implementation and human balance approval remain separate.')
        s=s.replace('## Scope and remaining exact review','## Reviewed scope and remaining integration').replace('This supplement implements the source conference and all eight focused interface decisions. The complete cards and machine projections still need exact review and source-fidelity checks.','This supplement implements the source conference, all eight focused interface decisions and the completed Part 2 exact review. All four finite-repair requirements are satisfied; the 43 cards and their projections pass 131 local checks.')
        write(p,s)
    for p in paths[3:]:
        x=read(p);x['status']=LABEL;x['sharedOperationalProfile']['status']='reviewed-authored-operational-playtest'
        for c in x['cards']:c['status']='reviewed-authored-operational-playtest'
        dump(p,x)
    # Status labels changed; ensure the promoted bytes still conform.
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/validate_blacksmithing_recipe_candidate.py')],check=True)
    report=read(report_path);assert report['status']=='PASS'
    refs=[verdict,AUDIT/'GPT_BLACKSMITHING_SOURCE_CONFERENCE.txt',AUDIT/'GPT_BLACKSMITHING_INTERFACE_REVIEW.txt']
    dump(manifest,{'status':LABEL,'exactReviewThreadId':EXACT_THREAD,'exactReviewTurnId':EXACT_TURN,'exactReplyId':EXACT_REPLY,'sourceConferenceTurnId':'5869023f-1971-470c-9a61-27c9e5b04668','interfaceTurnId':'a184686d-59a2-4c32-8cca-797b936060d5','repairsApplied':REPAIRS,'coverage':{'recipes':43,'public':27,'restricted':4,'directorOnly':12,'baseModels':40,'weaponEffects':27,'defensiveEffects':16,'elementalRiders':10},'validationChecks':len(report['checks']),'localTimingCases':20,'localDurabilityStates':4116,'modelChoiceExamples':248,'protectedSourceAndPriorRuleArtifactsUnchanged':32,'artifactHashes':{relative(p):sha(p) for p in paths},'replyHashes':{p.name:sha(p) for p in refs},'validationEvidence':relative(report_path),'validationSha256':sha(report_path),'repairEvidence':relative(repairs_path),'repairEvidenceSha256':sha(repairs_path),'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,'aggregateReviewedRecipes':218,'remainingRecipeEffects':469,'cosmology':'Deferred until successful authorized GitHub push and verified remote commit.'})
    # Index promotion is deliberately last, after the manifest pins all evidence.
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/build_crafting_recipe_review_catalog.py')],check=True)
    totals=read(AUDIT/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json')['totals']
    assert totals['reviewed']==218 and totals['publicReviewed']==138 and totals['unreviewed']==469
    summary='All 43 Blacksmithing recipes completed exact review in Calibration Review Part 2. All four finite-repair requirements are satisfied: exact rider timing, live completion damage state, explicit defensive eligibility and fresh validation/public filtering. **131 local checks pass**, including 20 timing cases, 4,116 durability states and 248 model-choice examples. All 43 source recipes, 38 referenced equipment records and 32 protected source/prior-rule files remain unchanged. Visibility is 27 public / 4 restricted / 12 Director-only.\n\nCurrent operational-pass recipe totals: **218 of 687 reviewed; 469 remain**. Public totals: **138 of 433 reviewed; 295 remain**. These are current-pass counts, preserving prior authoring and owner approvals. Human balance, material availability, runtime/companion parity and whole-game flow remain open. No source deletion or GitHub push occurred; cosmology remains strictly post-push.\n'
    wrapper='# Blacksmithing exact review completed in Part 2\n\nActual notebook: [Calibration Review Part 2](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/'+EXACT_THREAD+'). Turn `'+EXACT_TURN+'`; reply `'+EXACT_REPLY+'`. The [captured verdict](GPT_BLACKSMITHING_PART2_EXACT_REVIEW.txt) explicitly permits promotion after exact implementation and successful validation without a new generic conference. The [repair evidence](BLACKSMITHING_PART2_REPAIRS_APPLIED.json) records corrected hashes and validation before promotion. The [final manifest](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/BLACKSMITHING_REVIEW_STATUS.json) pins final artifacts and evidence.\n\n'+summary+'\n'+''.join('- '+x+'\n' for x in REPAIRS)
    write(AUDIT/'GPT_BLACKSMITHING_PART2_EXACT_REVIEW.md',wrapper)
    write(AUDIT/'BLACKSMITHING_REVIEW_CHECKPOINT.md','# Blacksmithing completed\n\n'+summary)
    p=AUDIT/'BLACKSMITHING_PART2_SUBMISSION.json';x=read(p)
    x.update(status='COMPLETED; four finite-repair requirements satisfied and 43 cards promoted',reviewStatus=relative(manifest),repairEvidence=relative(repairs_path),validationChecks=131)
    x['textParts']['C_EXACT']['status']='Completed exact verdict; finite repairs applied, validated and promoted'
    dump(p,x)
    p=ROOT/'data/playtest/game_development_coverage.json';x=read(p)
    for aspect in x['aspects']:
        if aspect['id'] not in ('DD-29','DD-30','DD-54','DD-63'):continue
        note={'DD-29':'Blacksmithing adds 43 reviewed operational recipes after four finite-repair requirements; current total 218/687, 469 remain. Leatherworking source conference is next.',
              'DD-30':'Blacksmithing preserves actual bases, source batch values and exact repair references; 248 model-choice examples verified. Finite buyers and balance remain open.',
              'DD-54':'Blacksmithing public27 is proven an exact filtered derivation of internal43, with permitted equipment and no nested gated formula/guidance leakage. Public reviewed count138/433.',
              'DD-63':'Blacksmithing authored state specification and 20 timing-reference cases are complete; companion/live runtime parity remains unimplemented.'}[aspect['id']]
        aspect.setdefault('completedScopes',[]).append(note)
        for k,v in [('reviewEvidence','docs/audit/2026-10-08/full-game/GPT_BLACKSMITHING_PART2_EXACT_REVIEW.md'),('validationEvidence','docs/audit/2026-10-08/full-game/BLACKSMITHING_CANDIDATE_VALIDATION.json'),('draftEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md')]:
            if v not in aspect.setdefault(k,[]):aspect[k].append(v)
    dump(p,x)
    p=GAME/'START_HERE.md';s=p.read_text(encoding='utf-8')
    start=s.index('The latest completed recipe review covers ');end=s.index('\n\n',start)
    s=s[:start]+'The latest completed recipe review covers [all 43 Blacksmithing formulas](DescentReviewChanges/ReviewBible/docs/mechanics/BLACKSMITHING_RECIPE_PLAYTEST.md), including [27 public cards](DescentReviewChanges/ReviewBible/docs/mechanics/BLACKSMITHING_PUBLIC_RECIPE_CARDS.md). Calibration Review Part 2 approved the authored scope after four finite-repair requirements; all are satisfied and 131 checks pass. The [recipe index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md) records **218 of 687 recipe effects reviewed in this operational manuscript pass; 469 remain** (138 of 433 public formulas reviewed). Original source information remains preserved. Leatherworking is the next source conference. No deletion, GitHub push or cosmology review occurred.'+s[end:]
    s=s.replace('512 other recipe effects','469 other recipe effects').replace('The other 512 recipe effects remain open.','The other 469 recipe effects remain open.')
    s=s.replace('Blacksmithing\'s exact verdict and the GPT continuation remain prerequisites.','Blacksmithing’s exact review is now complete in the owner-created Part 2 continuation.')
    s=s.replace('Alchemy, Herbalism, Cooking and Poisoncrafting now account for 175 reviewed effects; the remaining 512 stay in the recipe queue.','Alchemy, Herbalism, Cooking, Poisoncrafting and Blacksmithing now account for 218 reviewed effects; the remaining 469 stay in the recipe queue.')
    anchor='| Ordinary spells |';assert s.count(anchor)==1
    s=s.replace(anchor,'| [Blacksmithing recipes](DescentReviewChanges/ReviewBible/docs/mechanics/BLACKSMITHING_PUBLIC_RECIPE_CARDS.md) | All 43 formulas reviewed; 27 public, 16 separately gated; 131 checks pass | Material availability, wider interactions, runtime and balance |\n'+anchor)
    write(p,s)
    p=AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md';s=p.read_text(encoding='utf-8');start=s.index('## Live Part 2 checkpoint');end=s.index('## Human objective',start)
    s=s[:start]+'## Live Part 2 checkpoint\n\n'+summary+'\nThe original handoff and Parts A–C were successfully received. The completed exact verdict is turn `'+EXACT_TURN+'`, reply `'+EXACT_REPLY+'`. See [captured review and promotion evidence](GPT_BLACKSMITHING_PART2_EXACT_REVIEW.md). Historical handoff counts below describe the preserved pre-promotion checkpoint; current counts above control. Leatherworking remains the next source conference.\n\n'+s[end:]
    s=s.replace('the complete handoff and pending review evidence are being transferred.','the complete handoff and Blacksmithing review evidence have been received and reviewed.')
    write(p,s)
    p=AUDIT/'REVIEW_STATUS.md';write(p,p.read_text(encoding='utf-8')+'\n\n## Blacksmithing completed in Calibration Review Part 2\n\n'+summary)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/build_game_coverage.py')],check=True)
    print(json.dumps({'status':LABEL,'checks':131,'reviewedRecipes':218,'remainingRecipes':469,'publicReviewed':138}))

if __name__=='__main__':main()
