"""Reconcile current candidate metadata and navigation after the authored pass.

Preserves prior artifacts. Does not mark exact review or whole-game work complete.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import re
import shutil
import subprocess
import sys
from build_advanced_craft_internal_candidates import read,dump,sha

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
PHASE='authored-candidate-awaiting-state-sequence-validation-and-exact-review'


def main():
    backup=A/'navigation-before-advanced-candidate-checkpoint';assert not backup.exists()
    ip=R/'data/director/advanced_craft_recipe_candidate_internal.json';pp=R/'data/crafting/advanced_craft_recipe_candidate_public.json'
    paths=[ip,pp,G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json',A/'ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json',A/'ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json',A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json',A/'ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json',A/'ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json']
    paths += [R/f"docs/director-only/{t.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md" for t in ['Enchanting','Rune Carving','Scribing','Tinkering']]
    saved=[]
    for p in paths:
        dst=backup/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);saved.append({'path':p.relative_to(G).as_posix(),'sha256':sha(p)})
    dump(backup/'MANIFEST.json',saved)
    d=read(ip);p=read(pp)
    d['status']=PHASE;d['publicProjectionComplete']=True;d['stateSequenceValidationComplete']=False
    d['publicCandidatePath']=pp.relative_to(R).as_posix()
    for c in d['cards']:c['status']=PHASE
    for h in d['enchantingHostModels'].values():h['status']='authored-existing-host-template-awaiting-exact-review'
    p['enchantingHostModels']=d['enchantingHostModels'];p['stateSequenceValidationComplete']=False
    dump(ip,d);dump(pp,p)
    for t in ['Enchanting','Rune Carving','Scribing','Tinkering']:
        path=R/f"docs/director-only/{t.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md"
        text=path.read_text(encoding='utf-8').replace('public projection, state-sequence validation and exact review pending.','public projection authored; state-sequence validation and exact review pending.')
        path.write_text(text,encoding='utf-8')
    ledger=read(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json');ledger['status']='Explicit public projection authored; envelope validation recorded separately';ledger['internalCandidateSha256']=sha(ip);dump(A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json',ledger)
    for name in ['ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json','ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json']:
        status=read(A/name);status['status']=PHASE
        for path in status['outputHashes']:status['outputHashes'][path]=sha(G/path)
        status['remainingWork']=['Finite behavior/state-sequence fixtures and semantic cross-check','Separate exact GPT review of all167 actual candidates and complete public envelope']
        dump(A/name,status)
    for script in ['validate_advanced_craft_internal_candidates.py','validate_advanced_craft_public_candidates.py']:
        result=subprocess.run([sys.executable,'-X','utf8',str(R/'tools'/script)],capture_output=True,text=True,encoding='utf-8')
        assert result.returncode==0,result.stdout+result.stderr
    iv=read(A/'ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json');pv=read(A/'ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json')
    progress=read(A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json');progress.update(status=PHASE,publicCardsAuthored=100,publicProjectionComplete=True,internalSourceAndManuscriptChecks=iv['checks'],publicEnvelopeChecks=pv['checks'],stateSequenceValidationComplete=False,exactReviewSubmitted=False,nextAction='Exercise all19 named worked boundaries and rejected alternatives, then submit the actual complete167 candidates/public envelope for separate exact GPT review.');dump(A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json',progress)
    now=datetime.now(timezone.utc).isoformat()
    receipt={'status':PHASE,'checkpointAtUtc':now,'internalCards':167,'publicCards':100,'internalBodyVariants':22,'publicBodyVariants':15,'existingHostTemplates':50,'sourceComponentOccurrences':758,'publicComponentMentions':343,'publicBookParagraphs':600,'sourceAndRegisterChecksReproduced':[5248,1623],'internalSourceManuscriptArithmeticChecks':iv['checks'],'publicEnvelopeChecks':pv['checks'],'checksPassed':iv['status']=='PASS' and pv['status']=='PASS','stateSequenceValidationComplete':False,'exactReviewSubmitted':False,'controllingEditorialCorrection':'ADV-EDIT-01','correctionReplyId':'a01ad150-d04b-4fb8-ae18-9ea476535a93','internalCandidateSha256':sha(ip),'publicCandidateSha256':sha(pp),'reviewedRecipes':520,'reviewedPublicRecipes':333,'newApprovals':0,'sourceInformationDeleted':0,'githubPushPerformed':False,'cosmologyReviewed':False,'nextAction':progress['nextAction']}
    dump(A/'ADVANCED_CRAFT_CANDIDATE_READINESS.json',receipt)
    start=G/'START_HERE.md';text=start.read_text(encoding='utf-8')
    summary='**Advanced crafting candidates written:** All167 internal recipe cards and100 public cards are authored. The [player guide](DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md) and [body catalogue](DescentReviewChanges/ReviewBible/docs/mechanics/ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md) are available to read. Source/manuscript/arithmetic and public-envelope checks pass; [the readiness record](docs/audit/2026-10-08/full-game/ADVANCED_CRAFT_CANDIDATE_READINESS.json) records their exact limits. GPT’s trap-spring correction ADV-EDIT-01 is applied beside preserved originals. Use-sequence checks and separate exact-card review remain next. No new recipe promotion: totals remain520/687 and public333/433.'
    text,n=re.subn(r'\*\*Advanced crafting source review complete:\*\*[^\n]+',summary,text,count=1);assert n==1
    text=text.replace('167 advanced-trade sources; availability and integration remain separate','All167 advanced drafts written; use-sequence checks and exact review remain. Availability and integration are separate')
    anchor='| Remaining recipes |';lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith(anchor):lines[i]='| Remaining recipes | Advanced candidates: [Enchanting](DescentReviewChanges/ReviewBible/docs/mechanics/ENCHANTING_CANDIDATE_RECIPE_CARDS.md), [Rune Carving](DescentReviewChanges/ReviewBible/docs/mechanics/RUNE_CARVING_CANDIDATE_RECIPE_CARDS.md), [Scribing](DescentReviewChanges/ReviewBible/docs/mechanics/SCRIBING_CANDIDATE_RECIPE_CARDS.md), [Tinkering](DescentReviewChanges/ReviewBible/docs/mechanics/TINKERING_CANDIDATE_RECIPE_CARDS.md). [Preserved source decisions](docs/audit/2026-10-08/full-game/GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md); exact review pending. |'
    start.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    handoff=A/'GPT_REVIEW_CONTINUATION_HANDOFF.md';ht=handoff.read_text(encoding='utf-8')
    update='**Current advanced-crafting work:** All167 internal and100 public operational candidates are authored, with22 internal/15 public body variants and50 existing host templates. The full final source verdict is preserved; its5248 source/1623 register checks reproduce. Current candidate checks pass:5770 internal source/manuscript/arithmetic and1725 public-envelope checks. The targeted ADV-EDIT-01 reply `a01ad150-d04b-4fb8-ae18-9ea476535a93` makes the trap spring replaceable while retaining original frame/discharge primaries; all11 affected cards are corrected. The notebook is idle after that completed clarification. No exact candidate package has yet been submitted. Next: actual finite use-sequence fixtures and semantic cross-check, then all167 complete candidates for exact GPT review. See [readiness](ADVANCED_CRAFT_CANDIDATE_READINESS.json). Counts remain520/687 and public333/433; no deletion, push or cosmology review.'
    ht,n=re.subn(r'\*\*Active advanced crafting review:\*\*[^\n]+',update,ht,count=1);assert n==1;handoff.write_text(ht,encoding='utf-8')
    obs=read(A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json');obs['observedAtUtc']=now;obs['historyBeforeAdvancedCandidateCheckpoint']={'currentRequest':obs['currentRequest']}
    obs['currentRequest']={'scope':'ADV-EDIT-01 targeted trap-spring clarification','status':'completed; applied beside preserved source files','turnId':'bc3f83a4-bf35-43c1-af2e-86bebf45a7dd','replyId':'a01ad150-d04b-4fb8-ae18-9ea476535a93','sourceVerdictPending':False,'exactReviewSubmitted':False,'notebookStatusAsObserved':'idle with full completed final reply via read_thread','browserTabId':'125745449','captureFile':'ADVANCED_TRAP_SPRING_FINAL_CAPTURE.json','integrationReceipt':'ADVANCED_TRAP_SPRING_INTEGRATION.json','resubmissionPerformed':False,'newAdvancedApprovals':0,'nextAction':progress['nextAction']}
    obs['advancedCandidateProgress']=receipt;obs['nextAction']=progress['nextAction'];obs['currentGoalTurnClassification']='progress:167 complete internal drafts and100 public projections authored; one targeted GPT ambiguity resolved and integrated; source and envelope checks pass; meaningful use-sequence/exact review remain.'
    dump(A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',obs)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
