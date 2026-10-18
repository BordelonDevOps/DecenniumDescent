"""Successor handoff with checkpoint22 and full agreed-copy progress evidence."""
from copy import deepcopy
from pathlib import Path
from datetime import datetime,timezone
import json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded


def main():
    root=A/'gpt-continuation05-handoff-02';out=A/'GPT_CONTINUATION_05_HANDOFF_02.json'
    prep=A/'GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json';request=A/'GPT_CONTINUATION_05_HANDOFF_02_REQUEST.txt'
    zp=A/'DD_Continuation_05_Handoff_02.zip'
    assert not any(p.exists() for p in [root,out,prep,request,zp])
    old=A/'GPT_CONTINUATION_05_HANDOFF_01.json';before=json.loads(old.read_bytes());handoff=deepcopy(before)
    bindings={}
    def bind(p):b=info(p);bindings[b['path']]=b;return b
    # Prior context01 is frozen in its original archive. Mutable navigation is
    # rebound here as explicitly new context02, never passed off as old bytes.
    for b in before['sources']:bind(G/b['path'])
    newpaths=[old,A/'GPT_CONTINUATION_05_HANDOFF_01_PREPARATION.json',
        A/'GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json',A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_RELEASE_CONTINUATION_22.json',
        A/'COPY_RELEASE_CONTINUATION_22_CHECK.json',R/'data/director/spell_review/remaining_work_queue_17.json',
        A/'FEAT335_COPY_RELEASE_01_PROGRESS.json',A/'FEAT335_COPY_RELEASE_01_PREPARATION.json',
        A/'FEAT335_COPY_RELEASE_01_GPT_UPDATE.txt',A/'DD_Feat335_Copy_Release_Integration_01.zip',Path(__file__)]
    for p in newpaths:bind(p)
    queue=R/'data/director/spell_review/remaining_work_queue_17.json'
    handoff.update(id='GPT-CONTINUATION-05-HANDOFF-02',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        previousHandoff=info(old),currentCheckpoint=info(A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_RELEASE_CONTINUATION_22.json'),
        queue={'grouped':142,'groups':19,'ungrouped':181,'source':info(queue)},
        actualCollaborationStatus=info(A/'GPT_REVIEW_PART4_LENGTH_LIMIT_01_STATUS.json'),
        boundedAgreedRuleProgress={'progress':info(A/'FEAT335_COPY_RELEASE_01_PROGRESS.json'),
            'completeArchiveIncludedInThisHandoff':info(A/'DD_Feat335_Copy_Release_Integration_01.zip'),
            'status':'136 finite checks/19 conditional histories; seven direct-Action profiles integrated with paid acquisition, actual existing RP, cadence and concentration. Ready concentration only. No new rules selected.',
            'deferredReview':'Do not replace the Illusion conference with this progress update. Full Shaman/Mirrorsage, recipient effects and Ready transactions remain open. COPY-READY-ALLOWANCE-01 is a queued source question.'},
        sources=list(bindings.values()),newChatCreated=False,newRuleAdoptions=0)
    handoff['continuationRules']=[s.replace('Latest verified observation49used/51remaining.','Latest verified observation50used/50remaining.') for s in handoff['continuationRules']]
    handoff['latestWorkNotYetPushed']=['Part4 length-limit diagnosis and continuation handoffs','Copy release implementation/evidence','Queue17/checkpoint22']
    checks=[];root.mkdir()
    out.write_bytes(encoded(handoff));raw=handoff['fullUserObjective']['exactText'].encode('utf8')
    (root/'OWNER_OBJECTIVE.txt').write_bytes(raw)
    for b in bindings.values():
        p=G/b['path'];assert info(p)==b
        dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
        assert dst.read_bytes()==p.read_bytes();checks.append({'source':b,'preservedExactly':True})
    conferences=handoff['firstConference']['archivesToUploadAlongsideThisHandoff']
    for b in conferences:
        assert info(G/b['path'])==b
        with zipfile.ZipFile(G/b['path']) as z:assert z.testzip() is None
    (root/'MANIFEST.json').write_bytes(encoded({'handoff':info(out),'sources':list(bindings.values()),'separateConferenceArchives':conferences,'ownerObjective':handoff['fullUserObjective'],'checks':checks,'failures':0}))
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(out,'HANDOFF.json')
        for p in root.rglob('*'):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None and z.read('HANDOFF.json')==out.read_bytes()
        assert z.read('OWNER_OBJECTIVE.txt')==raw
        for b in bindings.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
    original=(A/'GPT_CONTINUATION_05_HANDOFF_01_REQUEST.txt').read_text('utf8')
    revised=original.replace('DD_Continuation_05_Handoff_01.zip','DD_Continuation_05_Handoff_02.zip').replace('currently51percent','latest observation50percent')
    revised+='Context02 carries the current queue17/checkpoint22 and a complete nested DD_Feat335_Copy_Release_Integration_01.zip:136 passing finite checks/19 conditional histories implementing previously accepted CRS-01..03, with no new rules. Read its progress limitations, but finish the full Illusion14 conference first; CompanionExact05 remains next. Ready allowance timing, actual Shaman/Mirrorsage providers and recipient effects are still open. This progress is not full feat or runtime approval.\n'
    request.write_text(revised,encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':info(zp),'handoff':info(out),'manifest':info(root/'MANIFEST.json'),'request':info(request),
        'separateArchives':conferences,'sourceCount':len(bindings),'allArchivedBytesVerified':True,
        'supersedesForNextSubmissionOnly':info(A/'GPT_CONTINUATION_05_HANDOFF_01_PREPARATION.json'),
        'status':'Prepared UNSENT; continuation authorization still pending; no new chat created.',
        'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'archive':info(zp),'handoff':info(out),'sources':len(bindings),'newChatCreated':False}))


if __name__=='__main__':main()
