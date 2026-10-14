"""Preserve navigation, then record Fishing authoring without approving it."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import json, shutil, re
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,write


def main():
    paths=[GAME/'START_HERE.md',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',
        AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',
        ROOT/'data/playtest/game_development_coverage.json',
        AUDIT/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json']
    backup=AUDIT/'navigation-before-fishing-authoring'
    if not backup.exists():
        hashes={}
        for p in paths:
            rel=p.relative_to(GAME);dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest);hashes[str(rel).replace('\\','/')]=sha(p)
        dump(backup/'MANIFEST.json',hashes)
    oldcoverage=read(backup/'docs/audit/2026-10-08/full-game/FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json')
    cohorts=oldcoverage['cohortFiles']+['REMAINING_RANK3_SPELL_SOURCE_PREPARATION.json']
    ids=[];bindings=[];protected={}
    for name in cohorts:
        d=read(AUDIT/name);ids.extend(z['spellId'] for z in d['selectedSpells'])
        bindings.extend(d['currentBookBindings'])
        for p,h in d['protectedFiles'].items():
            assert p not in protected or protected[p]==h
            protected[p]=h
    assert len(ids)==len(set(ids))==137 and len(bindings)==141
    assert all(sha(GAME/p)==h for p,h in protected.items())
    prep=deepcopy(oldcoverage)
    prep.update({'distinctPreparedPendingSpellIds':137,'currentBookBindings':141,
        'allPendingMinClassRankZeroToThreeSourcesCovered':True,
        'prePushMechanicalQuestions':136,'postPushReceiptOnlyIds':['blink'],
        'protectedInputsUnchanged':len(protected),'cohortFiles':cohorts,
        'reviewApprovalsGranted':0,'packetsSent':0})
    dump(AUDIT/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json',prep)
    current=('**Current joint work:** GPT\'s complete [Fishing source verdict]({audit}GPT_FISHING_SOURCE_CONFERENCE.md) is preserved. '
        'It authorized authoring, not recipe approval. All 44 draft cards are written (28 public), with nine body models and separate audience files. '
        '[Preliminary validation]({audit}FISHING_PRELIMINARY_VALIDATION.json) passes 130 checks, 528 quality cases, 156 structural states and 76 repair quotes; '
        '63 protected inputs remain unchanged. Complete catch/retrieval scenario evidence and separate GPT exact-card review are next. Fishing approvals remain zero.')
    rank=('The [remaining rank-three spell audit]({audit}REMAINING_RANK3_SPELL_SOURCE_AUDIT.md) preserves 21 further source identities and 22 current-book placements. '
        'Twenty have pre-push mechanical questions; Blink is only a preserved receipt for the post-push cosmology review. '
        'Ten checks pass across 70 protected inputs. Across six unsent packets, 137 identities and 141 current-book bindings are now prepared: '
        '136 mechanical questions and one deferred receipt. Ordinary totals remain 276 operational and 572 unfinished; preparation grants no new approval.')
    for p in paths[:2]:
        s=p.read_text(encoding='utf-8');prefix='docs/audit/2026-10-08/full-game/' if p.name=='START_HERE.md' else ''
        s=re.sub(r'^\*\*Current joint request:\*\*.*$',current.format(audit=prefix),s,count=1,flags=re.M)
        if '**Current joint work:**' not in s:
            raise AssertionError('Current checkpoint heading not found')
        s=s.replace('Fishing is the active source conference; both parts were sent once and the complete Part B verdict remains pending. See FISHING_PART2_SUBMISSION.json.',
            'Fishing source review is complete; its full FI-D01–24 verdict is captured. All 44 draft cards are authored and preliminary source/projection/arithmetic checks pass; full scenario evidence and exact review remain pending.')
        s=s.replace('Fishing44 is next; no Fishing approval, deletion, push or cosmology review.',
            'Fishing44 is now authored from its separate source verdict; exact review remains pending. No Fishing approval, deletion, push or cosmology review.')
        s=s.replace('Fishing44 is in its source conference; no Fishing approval, deletion, push or cosmology review.',
            'Fishing44 is now authored; its exact review remains pending. No Fishing approval, deletion, push or cosmology review.')
        s=s.replace('A complete packet with 24 unresolved scenarios is prepared, unsent.',
            'The original prepared packet and 24 questions remain preserved; both source-conference parts were subsequently sent and the complete FI-D01–24 verdict is now captured.')
        if rank.format(audit=prefix) not in s:
            marker='**Owner-directed sequence:**' if p.name=='START_HERE.md' else '## Next prepared source evidence'
            s=s.replace(marker,rank.format(audit=prefix)+'\n\n'+marker,1)
        if p.name=='START_HERE.md' and '| [Fishing draft recipes]' not in s:
            target='| Ordinary spells |'
            row='| [Fishing draft recipes](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md) | All 44 authored from the completed source verdict; 28 public; preliminary checks pass | Catch/retrieval scenario validation and separate exact review; zero Fishing approvals |\n'
            s=s.replace(target,row+target,1)
        write(p,s)
    observation=read(paths[2]);capture=read(AUDIT/'FISHING_SOURCE_CONFERENCE_CAPTURE.json')
    observation['observedAtUtc']=datetime.now(timezone.utc).isoformat()
    observation['currentRequest'].update({'scope':'Fishing44 authored candidate; preparing separate exact-review evidence',
        'actualSourceVerdictPending':False,'replyId':capture['sourceReplyId'],
        'observedItemTypes':['userMessage','agentMessage'],'browserObservation':'Complete verdict downloaded and prefix-matched to actual completed reply; see capture manifest.',
        'sourceVerdictFile':'GPT_FISHING_SOURCE_CONFERENCE.md','sourceVerdictSha256':capture['sha256'],
        'exactReviewSubmitted':False})
    observation['latestCompletedSourceConference']={'turnId':capture['sourceTurnId'],'replyId':capture['sourceReplyId'],
        'file':'GPT_FISHING_SOURCE_CONFERENCE.md','captureEvidence':'FISHING_SOURCE_CONFERENCE_CAPTURE.json',
        'scope':'FI-D01..24 authoring permission only; zero exact approvals'}
    observation['previousCompletedAuthoringProgress']=deepcopy(observation['authoredProgress'])
    observation['authoredProgress']={'fishingCards':44,'publicCards':28,'checks':130,
        'qualityCases':528,'structuralStates':156,'repairQuotes':76,'protectedInputs':63,
        'currentReviewedRecipes':348,'newApprovals':0,'publicReviewed':223,'remainingRecipes':339,
        'exactReviewReady':False,'status':'complete draft; preliminary source/projection/arithmetic checks passed'}
    observation['independentProgress'].update({'focusedPendingSpellSourcesPrepared':137,
        'currentBookBindingsAcrossSixSpellPackets':141,'remainingRank3SourcesPrepared':21,
        'remainingRank3PrePushQuestions':20,'remainingRank3PostPushReceiptOnly':1,
        'remainingRank3Checks':10,'remainingRank3ProtectedInputs':70,
        'prePushSpellQuestionsAcrossSixPackets':136,'allPendingMinimumRankZeroToThreeSourcesPrepared':True})
    observation['currentGoalTurnClassification']='progress: complete Fishing source verdict captured;44 operational cards authored;130 preliminary checks pass;21 remaining rank3 sources linked with Blink deferred'
    observation['consecutiveBlockedGoalTurns']=0
    observation['threadStatus']='idle after completed source response; no exact request yet'
    observation['nextAction']='Complete Fishing reference scenarios, especially source-bound item eligibility, real opportunity chronology, unattended checks, bait exposure/expiry, secure retrieval and one recovery evaluation including zero. Fix and verify bounded helper before exact review; then prepare and send exact candidate, never infer approval from source verdict. Keep cosmology post verified push.'
    dump(paths[2],observation)
    coverage=read(paths[3]);byid={x['id']:x for x in coverage['aspects']}
    def append(area,key,value):
        arr=byid[area].setdefault(key,[])
        if value not in arr:arr.append(value)
    auditrel='docs/audit/2026-10-08/full-game/'
    rootrel='DescentReviewChanges/ReviewBible/'
    for area in ['DD-28','DD-29','DD-30','DD-38','DD-39','DD-40']:
        append(area,'reviewEvidence',auditrel+'GPT_FISHING_SOURCE_CONFERENCE.md')
        append(area,'draftEvidence',rootrel+'docs/mechanics/FISHING_RECIPE_PLAYTEST.md')
        append(area,'validationEvidence',auditrel+'FISHING_PRELIMINARY_VALIDATION.json')
        append(area,'openIssues','Fishing FI-D01..24 source conference is complete and all44 draft cards are authored.130 preliminary source/projection/arithmetic checks pass; full catching/chronology/harvest scenarios and separate exact review remain open. No Fishing promotions; totals348/687 unchanged.')
    append('DD-32','sourceEvidence',auditrel+'FISHING_HISTORICAL_TRANSPORT_BACKLOG.json')
    for area in ['DD-32','DD-39']:
        arr=byid[area].get('openIssues',[])
        byid[area]['openIssues']=[('FI-D06 resolves current recipes172/173/177 as Tackle and preserves three historical boat concepts in FISHING_HISTORICAL_TRANSPORT_BACKLOG.json. Separate transport statistics remain unauthored; these are not three new recipes.' if 'Fishing Boat names' in x else x) for x in arr]
    for area in ['DD-03','DD-11','DD-12','DD-18','DD-21','DD-23','DD-35']:
        append(area,'sourceEvidence',auditrel+'REMAINING_RANK3_SPELL_SOURCE_PREPARATION.json')
        append(area,'draftEvidence',auditrel+'REMAINING_RANK3_SPELL_SOURCE_AUDIT.md')
        append(area,'validationEvidence',auditrel+'REMAINING_RANK3_SPELL_SOURCE_STATUS.json')
    append('DD-12','openIssues','Six focused unsent cohorts now preserve137 unfinished min-rank0..3 source identities/141 book bindings:136 pre-push mechanical questions plus Blink receipt-only for post-push cosmology. The21 remainingrank3 sources pass10 preparation checks/70 protected files. No spell approval;276 operational/572 pending unchanged.')
    dump(paths[3],coverage)
    print(json.dumps({'navigationUpdated':4,'navigationOriginalsPreserved':5,
        'fishingDrafts':44,'fishingApprovals':0,'preparedSpellSources':137,
        'prePushSpellQuestions':136,'bookBindings':141,'protectedSpellInputs':len(protected)}))


if __name__=='__main__':main()
