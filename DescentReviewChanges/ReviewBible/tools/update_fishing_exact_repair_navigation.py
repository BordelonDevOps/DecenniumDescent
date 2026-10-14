"""Record partial repair evidence without promoting the Fishing candidate."""
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import json,re,shutil
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,write,EXACT_AUTH


def main():
    assert not (ROOT/'docs/mechanics/FISHING_REVIEW_STATUS.json').exists(), 'Partial-repair navigation is historical after promotion; use the completed review manifest'
    report=read(AUDIT/'FISHING_EXACT_REPAIR_VALIDATION.json')
    source=read(AUDIT/'FISHING_REPAIRED_SOURCE_VALIDATION.json')
    status=read(AUDIT/'FISHING_AUTHORING_STATUS.json')
    protected=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert all(sha(GAME/p)==h for p,h in protected.items())
    assert all(sha(GAME/p)==h for p,h in report['inputHashes'].items())
    archives={}
    for name in ['fishing-exact-submission-original','fishing-before-exact-review-repairs','fishing-after-e01-e07-e10','fishing-after-six-exact-repairs','fishing-after-seven-exact-repairs','fishing-after-eight-exact-repairs','fishing-after-nine-exact-repairs']:
        manifest=read(AUDIT/name/'MANIFEST.json')
        assert all(sha(AUDIT/name/p)==h for p,h in manifest.items()),name
        archives[name]=len(manifest)
    now=datetime.now(timezone.utc).isoformat()
    coverage_path=ROOT/'data/playtest/game_development_coverage.json'
    latest=AUDIT/'FISHING_EXACT_PART2_C_LATEST_OBSERVATION.json'
    backup=AUDIT/'navigation-before-fishing-repair-progress'
    if not backup.exists():
        hashes={}
        for p in [coverage_path,latest]:
            target=backup/p.relative_to(GAME);target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,target);hashes[str(p.relative_to(GAME)).replace('\\','/')]=sha(p)
        dump(backup/'MANIFEST.json',hashes)
    covered=report['coveredIssues'];counts=Counter(x['issue'] for x in report['checks'])
    covered_text=', '.join(covered)
    remaining=[f'FI-E{i:02}' for i in range(1,12) if f'FI-E{i:02}' not in covered]
    progress=read(AUDIT/'FISHING_EXACT_REPAIR_PROGRESS.json')
    progress.update({'status':'partial repair implementation; full FI-E01..11 gate remains open',
        'updatedAtUtc':now,'implementedAreas':covered,'focusedChecksPassed':report['checkCount'],
        'sourceProjectionArithmeticChecksPassed':len(source['checks']),
        'validationFile':'FISHING_EXACT_REPAIR_VALIDATION.json',
        'sourceValidationFile':'FISHING_REPAIRED_SOURCE_VALIDATION.json',
        'workedCasesFile':'FISHING_EXACT_REPAIR_WORKED_CASES.md',
        'currentArtifactHashes':status['outputs'],'recipesPromoted':0,'fullCompletionGateSatisfied':False,
        'preservedArchiveFileCounts':archives})
    for repair in progress['repairs']:
        if repair['id'] in covered:
            repair.update({'status':'implemented and focused regressions pass; full-candidate integration gate pending',
                'checksPassed':counts[repair['id']],'validation':'FISHING_EXACT_REPAIR_VALIDATION.json',
                'workedCases':'FISHING_EXACT_REPAIR_WORKED_CASES.md'})
    dump(AUDIT/'FISHING_EXACT_REPAIR_PROGRESS.json',progress)
    statement=('**Current joint work:** GPT returned the [Fishing exact verdict]({prefix}GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md) with eleven required corrections. '
        f'{len(covered)} of eleven correction areas ({covered_text}) are implemented in the current draft. '
        f'[Focused verification]({{prefix}}FISHING_EXACT_REPAIR_VALIDATION.json) passes {report["checkCount"]} checks; '
        '[source/projection/arithmetic verification]({prefix}FISHING_REPAIRED_SOURCE_VALIDATION.json) passes 130 checks, retaining 528 quality cases, 156 structural states and 76 arithmetic quotations. '
        'All 63 protected inputs and the original submissions are preserved. The [remaining repairs and full integration gate]({prefix}FISHING_EXACT_REPAIR_PROGRESS.json) are still open. '
        'Fishing promotion remains zero; totals stay 348/687 reviewed, 339 remaining.')
    for p in [GAME/'START_HERE.md',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md']:
        text=p.read_text(encoding='utf-8');prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else ''
        text,n=re.subn(r'^\*\*Current joint work:\*\*.*$',statement.format(prefix=prefix),text,count=1,flags=re.M)
        assert n==1
        if p.name=='START_HERE.md':
            text=text.replace('Fishing44 exact review, then 128 gathering-tool','Fishing44 required repairs, then 128 gathering-tool')
            line=('| Fishing | [Draft public guide](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_RECIPE_PLAYTEST.md), '
                '[public cards](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md), '
                '[repair progress](docs/audit/2026-10-08/full-game/FISHING_EXACT_REPAIR_PROGRESS.json). '
                f'{len(covered)} of eleven required correction areas implemented; remaining repairs and complete verification precede promotion. |')
            text,n=re.subn(r'^\| Fishing \|.*$',line,text,count=1,flags=re.M);assert n==1
        else:
            text=text.replace('All 44 draft cards are authored and preliminary source/projection/arithmetic checks pass; full scenario evidence and exact review remain pending.',
                'All 44 draft cards are authored. The actual exact verdict now requires FI-E01..11 repairs; current implementation and evidence are recorded above. Historical submitted validation remains preserved.')
        write(p,text)
    prior=read(latest)
    latest_value={'notebookId':EXACT_AUTH['threadId'],'notebookTitle':'Calibration Review Part 2',
        'threadStatus':{'type':'idle'},'actualTurnId':EXACT_AUTH['turnId'],'reportedTurnStatus':'completed',
        'observedItemTypes':['userMessage','agentMessage'],'completedAgentMessages':[{'id':EXACT_AUTH['replyId']}],
        'observedAtUtc':now,'verdictFile':'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md','verdictSha256':EXACT_AUTH['sha256'],
        'note':'Actual completed agent reply confirmed again through read_thread; conditional FI-E01..11 authorization, not completed repairs.',
        'priorObservationArchivedAt':'navigation-before-fishing-repair-progress/docs/audit/2026-10-08/full-game/FISHING_EXACT_PART2_C_LATEST_OBSERVATION.json'}
    dump(latest,latest_value)
    observation=read(AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json')
    observation['observedAtUtc']=now
    observation['currentRequest'].update({'completedExactVerdictPending':False,
        'status':f'Exact verdict captured; {len(covered)} required correction areas implemented; remaining repairs and full integration verification open',
        'actualVerdictReplyId':EXACT_AUTH['replyId'],'verdictFile':'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md',
        'repairProgressFile':'FISHING_EXACT_REPAIR_PROGRESS.json','notebookStatusAsObserved':'idle'})
    observation['latestCompletedExactReview']={**EXACT_AUTH,'file':'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md'}
    observation['authoredProgress'].update({'historicalSubmittedChecks':220,'historicalSubmittedSequenceChecks':90,
        'checks':130+report['checkCount'],'sourceProjectionArithmeticChecks':130,
        'focusedRepairChecks':report['checkCount'],'implementedRepairAreas':covered,
        'sequenceChecks':None,'fullOriginalSequenceRevalidationPending':True,'exactReviewReady':False,
        'status':'Partial exact-review repairs implemented and regenerated; full completion gate pending'})
    observation['currentGoalTurnClassification']=f'progress: {covered_text} implemented with{report["checkCount"]} focused checks;130 source/projection/arithmetic checks; current six artifacts regenerated; originals preserved'
    observation['consecutiveBlockedGoalTurns']=0
    observation['nextAction']='Complete remaining '+', '.join(remaining)+', and promote only when every requirement of the actual conditional verdict is satisfied. No further generic exact review is required. Whole-game completion, authorized push, remote verification, then cosmology remain the owner-directed sequence.'
    dump(AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',observation)
    coverage=read(coverage_path)
    for aspect in coverage['aspects']:
        if aspect['id'] not in ['DD-28','DD-29','DD-30','DD-38','DD-39','DD-40']:continue
        for name in ['GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md','FISHING_EXACT_REPAIR_PROGRESS.json','FISHING_EXACT_REPAIR_VALIDATION.json','FISHING_REPAIRED_SOURCE_VALIDATION.json','FISHING_EXACT_REPAIR_WORKED_CASES.md']:
            rel='docs/audit/2026-10-08/full-game/'+name
            key='draftEvidence' if 'WORKED' in name else 'validationEvidence'
            if rel not in aspect.setdefault(key,[]):aspect[key].append(rel)
        aspect['openIssues']=[(f'Fishing44 exact verdict requires FI-E01..11. {len(covered)} areas implemented ({covered_text});{report["checkCount"]} focused checks and130 source/projection/arithmetic checks pass. Remaining repairs and full completion gate open; zero promotion. Current totals348/687 reviewed,339 remaining.' if x.startswith(('Fishing44 authored with220','Fishing44 exact verdict requires')) else x) for x in aspect['openIssues']]
    dump(coverage_path,coverage)
    submission=read(AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json')
    submission.update({'status':'actual exact verdict captured; FI-E01..11 repairs required; partial implementation in progress',
        'actualExactVerdictReplyId':EXACT_AUTH['replyId'],'actualExactVerdictFile':'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md'})
    dump(AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json',submission)
    assert all(sha(GAME/p)==h for p,h in protected.items())
    dump(AUDIT/'FISHING_REPAIR_NAVIGATION_RECEIPT.json',{'status':'current navigation updated without promotion',
        'implementedAreas':covered,'focusedChecks':report['checkCount'],'protectedInputsUnchanged':63,
        'preservedArchiveFileCounts':archives,'recipesPromoted':0,'cosmology':'post-push only'})
    print(json.dumps({'implementedAreas':covered,'focusedChecks':report['checkCount'],'protectedInputsUnchanged':63,'preservedArchives':archives,'recipesPromoted':0}))


if __name__=='__main__':main()
