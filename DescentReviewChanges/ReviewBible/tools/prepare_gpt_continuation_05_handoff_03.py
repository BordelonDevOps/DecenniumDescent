"""Current unsent handoff through checkpoint26; preserve earlier handoffs intact."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    root = A/'gpt-continuation05-handoff-03'; out = A/'GPT_CONTINUATION_05_HANDOFF_03.json'
    prep = A/'GPT_CONTINUATION_05_HANDOFF_03_PREPARATION.json'; request = A/'GPT_CONTINUATION_05_HANDOFF_03_REQUEST.txt'
    zp = A/'DD_Continuation_05_Handoff_03.zip'
    assert not any(p.exists() for p in [root, out, prep, request, zp])
    old = A/'GPT_CONTINUATION_05_HANDOFF_02.json'; before = read(old); handoff = deepcopy(before)
    bindings = {}; rebindings = []
    def bind(p):
        b = info(p); bindings[b['path']] = b; return b
    allowed = {'START_HERE.md', 'DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md',
               'DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json'}
    for b in before['sources']:
        current = bind(G/b['path'])
        if current != b:
            assert b['path'] in allowed
            rebindings.append({'priorContext02Binding': b, 'currentContext03Binding': current,
                'qualification': 'Explicit current navigation/coverage context; prior bytes remain frozen in Handoff02, never represented as unchanged.'})
    queue = R/'data/director/spell_review/remaining_work_queue_19.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_IDENTITY_CASTING_26.json'
    push = G/'docs/audit/2026-10-18/github-snapshot-classes-rank8/PUSH_RECEIPT.json'
    paths = [old, A/'GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json', queue, checkpoint,
        A/'RANK7_IDENTITY_CASTING_26_CHECK.json', push, Path(__file__),
        A/'FEAT335_COPY_PAYLOADS_01_PROGRESS.json', A/'FEAT335_COPY_PAYLOADS_01_PREPARATION.json',
        A/'FEAT335_COPY_PAYLOADS_01_GPT_UPDATE.txt', A/'DD_Feat335_Copy_Payloads_01.zip',
        A/'FEAT335_COPY_CLASSES_01_PROGRESS.json', A/'FEAT335_COPY_CLASSES_01_PREPARATION.json',
        A/'FEAT335_COPY_CLASSES_01_GPT_UPDATE.txt', A/'DD_Feat335_Copy_Classes_01.zip',
        A/'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_PREPARATION.json', A/'DD_Rank8_Damage_6_Source_Conference_01.zip',
        A/'RANK7_IDENTITY_CASTING_5_SOURCE_CONFERENCE_01_PREPARATION.json', A/'DD_Rank7_Identity_Casting_5_Source_Conference_01.zip']
    for p in paths: bind(p)
    q = read(queue); cp = read(checkpoint); receipt = read(push)
    assert cp['currentWorkQueue'] == info(queue)
    assert q['preparedOrActualReviewIdentityCount'] == 153 and q['originalSourceOrReceiptWorkCount'] == 170 and len(q['groups']) == 21
    assert receipt['commit'] == receipt['remoteMain'] == '7142a4f7e9c6088dbd1c92bd2ea3bde3891f42a9'
    assert receipt['trackedEntriesDeleted'] == 0
    objective = Path(r'C:\Users\cbord\.codex\attachments\3b824f9b-a950-43b8-99e9-61e7ebf125b1\goal-objective.md').read_text('utf8')
    assert objective == handoff['fullUserObjective']['exactText']
    handoff.update(id='GPT-CONTINUATION-05-HANDOFF-03', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        previousHandoff=info(old), currentCheckpoint=info(checkpoint),
        queue={'grouped': 153, 'groups': 21, 'ungrouped': 170, 'source': info(queue)},
        verifiedBackup=info(push), currentBackupCommit=receipt['commit'], explicitMutableSourceRebindings=rebindings,
        previousProgressContext02Unchanged=deepcopy(before['boundedAgreedRuleProgress']),
        boundedAgreedRuleProgress={
            'commitment': {'progress': info(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json'), 'fullArchive': info(A/'DD_Feat335_Copy_Release_Integration_01.zip'), 'checks': 136, 'conditionalHistories': 19},
            'recipientEffects': {'progress': info(A/'FEAT335_COPY_PAYLOADS_01_PROGRESS.json'), 'fullArchive': info(A/'DD_Feat335_Copy_Payloads_01.zip'), 'checks': 115, 'conditionalHistories': 27},
            'classProviders': {'progress': info(A/'FEAT335_COPY_CLASSES_01_PROGRESS.json'), 'fullArchive': info(A/'DD_Feat335_Copy_Classes_01.zip'), 'checks': 205, 'conditionalHistories': 22},
            'status': 'Agreed scoped rules implemented in finite evaluators; no new rule adoption. All three complete archives are nested in this handoff and have not been sent/reviewed as updates.',
            'scope': 'Seven declared direct-Action copy profiles, actual recipient health/buff/movement effects and actual Shaman/Mirrorsage provider/resource/concentration/allowance integrations. Conditional histories are not broad runtime or whole-feat approval.',
            'remaining': 'COPY-READY-ALLOWANCE-01 requires actual GPT. Full class Mirror capture/Echo payload/cadence, general ordinary concentration/world clocks/geometry/interceptors and runtime remain open. Earlier release/payload reports keep their narrower historical coverage; later class integration does not rewrite them.',
            'deferredReview': 'Read the current status to stay informed, but finish Illusion14 first, then separately supplied CompanionExact05/CR2 evidence. Do not silently accept unseen or unreviewed work.'},
        laterFullSourceConferencesIncluded=[
            {'preparation': info(A/'RANK8_DAMAGE_6_SOURCE_CONFERENCE_01_PREPARATION.json'), 'fullArchive': info(A/'DD_Rank8_Damage_6_Source_Conference_01.zip'),
             'scope': 'Six identities/six placements;20 unselected questions,51 full sources,240 source-preservation checks;4B/2C. No operational procedures/cases/rules adopted.'},
            {'preparation': info(A/'RANK7_IDENTITY_CASTING_5_SOURCE_CONFERENCE_01_PREPARATION.json'), 'fullArchive': info(A/'DD_Rank7_Identity_Casting_5_Source_Conference_01.zip'),
             'scope': 'Five identities/six placements;24 unselected questions,68 full sources,277 source-preservation checks;all5C. Actual Fate Echo acceptance/full DI7 cases and real Mage/feat metamagic evidence included. No procedures/cases/rules adopted.'}],
        sources=list(bindings.values()), newChatCreated=False, newRuleAdoptions=0,
        latestWorkNotYetPushed=['Rank7 identity/casting5 full source conference and queue19/checkpoint26', 'Continuation handoff03'],
        currentProgressQualification='Use checkpoint26/queue19 and this context03 for current status. Older handoffs/checkpoints/requests inside full sources are history; their stale counts, push IDs and open-coverage labels do not replace current statements.')
    handoff['continuationRules'] = [s.replace('Latest verified observation50used/50remaining.', 'Latest verified observation55used/45remaining.') for s in handoff['continuationRules']]
    conferences = handoff['firstConference']['archivesToUploadAlongsideThisHandoff']
    for b in conferences:
        assert info(G/b['path']) == b
        with zipfile.ZipFile(G/b['path']) as z: assert z.testzip() is None
    nested = [b for b in bindings.values() if b['path'].endswith('.zip')]
    for b in nested:
        with zipfile.ZipFile(G/b['path']) as z: assert z.testzip() is None
    root.mkdir(); out.write_bytes(encoded(handoff)); raw = objective.encode('utf8'); (root/'OWNER_OBJECTIVE.txt').write_bytes(raw)
    checks = []
    for b in bindings.values():
        p = G/b['path']; assert info(p) == b
        dst = root/'sources'/b['path']; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(p.read_bytes())
        assert dst.read_bytes() == p.read_bytes(); checks.append({'source': b, 'preservedExactly': True})
    (root/'MANIFEST.json').write_bytes(encoded({'handoff': info(out), 'sources': list(bindings.values()), 'separateConferenceArchives': conferences,
        'nestedFullArchives': nested, 'ownerObjective': handoff['fullUserObjective'], 'checks': checks, 'failures': 0}))
    with zipfile.ZipFile(zp, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(out, 'HANDOFF.json')
        for p in root.rglob('*'):
            if p.is_file(): z.write(p, p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None and z.read('HANDOFF.json') == out.read_bytes() and z.read('OWNER_OBJECTIVE.txt') == raw
        for b in bindings.values(): assert z.read('sources/'+b['path']) == (G/b['path']).read_bytes()
    request.write_text('Continue our Decennium Descent video-game-only review in Calibration Review Part5 within Dungeon Crawler. Part4 reached its conversation-length limit and remains preserved. Read HANDOFF.json and OWNER_OBJECTIVE.txt from DD_Continuation_05_Handoff_03.zip, then complete the interrupted full Illusion/Perception14 Current12 conference using the other two attached full archives. The original full request is preserved; current context is525reviewed/323pending/249standalone and173 scoped interfaces. Review all14 procedures,28 original/current scenarios,3 supplements and16 explicit decisions; no earlier Illusion final exists. Return complete exact-pointer repairs, question/case dispositions, holds and downloadable source/hash evidence. Do not accept other cohorts from their status metadata. CompanionExact05 and expanded CR2 evidence are next, separately.\n\nCurrent progress: queue19/checkpoint26 has153 identities in21 active/prepared groups and170 ungrouped. Commit7142a4f7e9c6088dbd1c92bd2ea3bde3891f42a9 is verified through checkpoint25,25264 expected blobs and no prior tracked files deleted. This handoff includes the complete three copied-feat integration archives:136 commitment,115 recipient and205 class-provider checks; actual Shaman/Mirrorsage integration is now included, but full Ready/class Echo/world/runtime remain open. COPY-READY-ALLOWANCE-01 is queued for actual discussion. It also includes complete Rank8Damage6 and Rank7IdentityCasting5 source conferences,44 unselected questions in total; neither is adopted. Read these progress summaries to remain informed without replacing the priority Illusion review.\n\nPreserve all original sources/access/history and distinguish source review, conditional evaluator checks, engine/runtime, human gameplay, balance, cosmology and75-domain/release gates. Owner wants ongoing mutual updates and development to review completion or20percent allowance remaining; latest observation45percent. If a file is inaccessible, identify it concretely before deciding. This context03 supersedes older handoffs only for the next submission, and creates no new acceptance.\n', encoding='utf8', newline='\n')
    prep.write_bytes(encoded({'archive': info(zp), 'handoff': info(out), 'manifest': info(root/'MANIFEST.json'), 'request': info(request),
        'separateArchives': conferences, 'sourceCount': len(bindings), 'nestedFullArchiveCount': len(nested), 'allArchivedBytesVerified': True,
        'supersedesForNextSubmissionOnly': info(A/'GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json'),
        'status': 'Prepared UNSENT; continuation authorization still pending; no new chat created.', 'newRuleAdoptions': 0, 'sourceInformationDeleted': 0}))
    print(json.dumps({'archive': info(zp), 'handoff': info(out), 'sources': len(bindings), 'fullNestedArchives': len(nested), 'newChatCreated': False}))


if __name__ == '__main__': main()
