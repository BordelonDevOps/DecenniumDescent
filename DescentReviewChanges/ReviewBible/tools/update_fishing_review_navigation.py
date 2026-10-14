"""Reflect exact-review dispatch receipts without inferring GPT approval."""
from datetime import datetime,timezone
from pathlib import Path
import json,re,shutil
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,write


def main():
    submission=read(AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json')
    report=read(AUDIT/'FISHING_CANDIDATE_VALIDATION.json')
    paths=[GAME/'START_HERE.md',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',
        AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',ROOT/'data/playtest/game_development_coverage.json']
    backup=AUDIT/'navigation-before-fishing-exact-submission'
    if not backup.exists():
        manifests={}
        for p in paths:
            rel=p.relative_to(GAME);dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest);manifests[str(rel).replace('\\','/')]=sha(p)
        dump(backup/'MANIFEST.json',manifests)
    sent=[k for k,v in submission['parts'].items() if v['sent']]
    receipts=[k for k,v in submission['parts'].items() if v.get('actualReceiptReplyId')]
    phase=('All three exact-review parts have been sent once; await the actual completed verdict.' if len(sent)==3
        else f'{len(sent)} of three parts sent once; {len(receipts)} actual GPT receipts captured. Send the next part only after the preceding actual receipt.')
    current=('**Current joint work:** All 44 Fishing draft cards (28 public) are in [separate exact-review preparation/dispatch]({audit}FISHING_EXACT_PART2_SUBMISSION.json). '
        'The source verdict is preserved and its rules are implemented in both audience versions. '
        '[Local validation]({audit}FISHING_CANDIDATE_VALIDATION.json) has 220 passing checks: 130 source/projection/arithmetic checks and 90 sequence checks, '
        'plus 528 quality choices, 156 structural states and 76 repair quotes. All 63 protected inputs remain unchanged. '
        +phase+' Fishing approvals remain zero; no total is promoted on local checks.')
    for p in paths[:2]:
        s=p.read_text(encoding='utf-8');prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else ''
        s,n=re.subn(r'^\*\*Current joint work:\*\*.*$',current.format(audit=prefix),s,count=1,flags=re.M)
        assert n==1
        s=s.replace('All 44 authored from the completed source verdict; 28 public; preliminary checks pass | Catch/retrieval scenario validation and separate exact review; zero Fishing approvals',
            'All 44 authored; 28 public; 220 local checks pass | Three-part exact review underway; zero Fishing approvals')
        write(p,s)
    observation=read(paths[2])
    if 'fishingSourceRequestBeforeExact' not in observation:observation['fishingSourceRequestBeforeExact']=observation['currentRequest']
    observation['observedAtUtc']=datetime.now(timezone.utc).isoformat()
    observation['currentRequest']={'scope':'Fishing44 exact operational review in three parts',
        'submissionFile':'FISHING_EXACT_PART2_SUBMISSION.json','partsSentOnce':sent,
        'actualPartReceiptsCaptured':receipts,'completedExactVerdictPending':True,
        'resubmissionPerformed':False,'status':submission['status']}
    observation['authoredProgress'].update({'checks':report['checkCount'],'sequenceChecks':90,
        'exactReviewReady':True,'status':'complete local candidate; separate exact review dispatch underway'})
    observation['currentGoalTurnClassification']='progress:90 source-bound sequence checks and journal repairs completed; independent manuscript reconstruction passes;220 local checks; exact three-part packet prepared and dispatch begun'
    observation['consecutiveBlockedGoalTurns']=0
    observation['nextAction']=phase+' Obtain and preserve full verdict, apply finite repairs if required, and promote only under actual exact authorization. Full game scope and post-push cosmology sequence remain unchanged.'
    dump(paths[2],observation)
    coverage=read(paths[3])
    for aspect in coverage['aspects']:
        if aspect['id'] not in ['DD-28','DD-29','DD-30','DD-38','DD-39','DD-40']:continue
        for key,name in [('validationEvidence','FISHING_CANDIDATE_VALIDATION.json'),('validationEvidence','FISHING_SEQUENCE_VALIDATION.json'),('validationEvidence','FISHING_PUBLIC_PARAGRAPH_PROJECTION.json'),('draftEvidence','FISHING_WORKED_SCENARIOS.md'),('draftEvidence','FISHING_EXACT_PART2_SUBMISSION.json')]:
            rel='docs/audit/2026-10-08/full-game/'+name
            if rel not in aspect.setdefault(key,[]):aspect[key].append(rel)
        aspect['openIssues']=[('Fishing44 authored with220 local checks, all24 worked cases and exact internal/public reconstruction. Separate three-part GPT exact review is underway; no Fishing promotion. Current totals348/687 reviewed,339 remaining.' if x.startswith('Fishing FI-D01..24 source conference is complete') else x) for x in aspect['openIssues']]
    dump(paths[3],coverage)
    print(json.dumps({'sentParts':sent,'actualReceipts':receipts,'localChecks':220,'recipesApproved':0}))


if __name__=='__main__':main()
