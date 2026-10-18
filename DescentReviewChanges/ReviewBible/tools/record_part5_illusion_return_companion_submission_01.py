"""Preserve actual Part5 exchanges and verify downloaded bytes; no rule adoption."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded

W = Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
TID = '6ad4a867-f330-83e9-829e-bf2bb41a6c09'


def read(p):
    return json.loads(p.read_bytes())


def main():
    now = datetime.now(timezone.utc).isoformat()
    receipt = A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json'
    submission = A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01.json'
    root = A/'illusion-perception14-part5-return-01'
    archive = A/'DD_Illusion_Perception_14_Part5_Return_01.zip'
    copies = {
        A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_NATIVE.json': W/'illusion14-part5-return01-native.json',
        A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01_NATIVE.json': W/'companion-exact05-part5-submitted-native01.json',
        A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01_REQUEST.txt': W/'companion-exact05-part5-submitted-request01.txt',
        A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01_UI.txt': W/'companion-exact05-part5-delivered01-ui.txt',
    }
    assert not any(p.exists() for p in [receipt, submission, root, archive, *copies])
    downloaded = Path(r'C:\Users\cbord\Downloads')/archive.name
    raw = downloaded.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert len(raw) == 228141 and sha == '018b3f0e5e932ae427d7a55b1e19ba5bd5b4500d100b4f05c73f15ab4a386590'
    native = read(W/'illusion14-part5-return01-native.json')
    assert native['thread']['id'] == TID
    finals = [i for t in native['turns'] for i in t['items'] if i.get('type') == 'agentMessage' and i.get('id') == '1329ce3a-137c-4789-928c-b0eda39df21e']
    assert len(finals) == 1 and sha in finals[0]['text']
    with zipfile.ZipFile(downloaded) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == 10 and z.testzip() is None
        assert all(len(PurePosixPath(n).parts) == 1 and not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n for n in names)
        payloads = {n:z.read(n) for n in names}
    manifest = json.loads(payloads['MANIFEST.json'])
    assert len(manifest['files']) == 9 and {b['path'] for b in manifest['files']} == set(names)-{'MANIFEST.json'}
    for b in manifest['files']:
        data = payloads[b['path']]
        assert len(data) == b['bytes'] and hashlib.sha256(data).hexdigest() == b['sha256']
    review = json.loads(payloads['REVIEW.json'])
    ops = json.loads(payloads['POINTER_OPERATIONS.json'])
    declaration = json.loads(payloads['SUCCESSOR_DECLARATION.json'])
    assert info(G/ops['baseCandidate']['path']) == ops['baseCandidate'] == declaration['baseCurrent12']
    assert review['verdict']['repairedPayload'] == 'SEMANTICALLY_ACCEPTED_FOR_INTEGRATION' and len(ops['operations']) == 2
    sent = read(W/'companion-exact05-part5-submitted-native01.json')
    uid = 'e7643d79-8ef1-4c64-b216-89a20101d269'
    assert sent['thread']['id'] == TID
    turn = next(t for t in sent['turns'] if t['id'] == uid)
    request = (W/'companion-exact05-part5-submitted-request01.txt').read_text('utf8').rstrip()
    assert turn['items'][0]['content'][0]['text'] == request+'\n\n[User attached 2 files; file contents were not included]'
    ui = (W/'companion-exact05-part5-delivered01-ui.txt').read_text('utf8')
    assert 'button "Stop"' in ui and 'Companion/Life10 Exact05' in ui
    attached = {a['name'] for a in sent['attachments']}
    inputs = []
    for name, size, digest, count in [
        ('DD_Companion_Life_10_Exact_05.zip',17707929,'be5a37d3032cd2e0b9e9486821045f0e467ac4977418a266a703407eb037d7ba',181),
        ('DD_Command_Undeath_Content_Evidence_01.zip',9436211,'315927825af947c8c3ca744b447009ab2be170a29343719c7de580b52f259d59',191),
    ]:
        b = info(A/name)
        assert name in attached and b['bytes'] == size and b['sha256'] == digest
        with zipfile.ZipFile(A/name) as z:
            assert z.testzip() is None and len(z.namelist()) == count
        inputs.append(b)
    for dst, src in copies.items():
        dst.write_bytes(src.read_bytes())
    root.mkdir()
    archive.write_bytes(raw)
    for name, data in payloads.items():
        (root/name).write_bytes(data)
    receipt.write_bytes(encoded({
        'id':'ILLUSION-PERCEPTION14-PART5-RETURN01','recordedAtUtc':now,
        'actualChat':'Calibration Review Part 5','actualThreadId':TID,
        'actualUserMessageId':'49c773ce-baf8-44ed-9658-595d5a7e5b10','actualAssistantMessageId':finals[0]['id'],
        'actualNativeFinal':info(A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_NATIVE.json'),
        'actualSubmission':info(A/'GPT_CONTINUATION_05_ACTUAL_START_01.json'),
        'returnedArchive':info(archive),'returnedFiles':[info(root/n) for n in names],
        'manifestPayloadsVerified':9,'manifestSelfHashConvention':manifest['note'],
        'verdict':review['verdict'],'exactBaseCandidate':ops['baseCandidate'],
        'procedureRepairs':declaration['procedureRepairs'],'acceptedIdentitiesForIntegration':14,
        'caseRewrites':0,'holdsUnchanged':review['holds'],
        'correctionsApplied':False,'authoredCountsUnchanged':{'reviewed':525,'pending':323},
        'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,
        'scope':'Actual semantic return verified and preserved. Local replay, source/case verification and clean canonical integration remain. The return accepts the exact repaired payload, not unseen future artifacts.'
    }))
    submission.write_bytes(encoded({
        'id':'COMPANION-LIFE10-EXACT05-PART5-ACTUAL-SUBMISSION01','recordedAtUtc':now,
        'status':'ACTUALLY_DELIVERED; LIVE_REVIEW_AT_CAPTURE; NO_FINAL_IN_THIS_RECEIPT',
        'chat':{'title':'Calibration Review Part 5','threadId':TID,'url':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/'+TID},
        'actualUserTurn':uid,'actualUserTurnTimestamp':turn['startedAt'],
        'request':info(A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01_REQUEST.txt'),
        'nativeReadEvidence':info(A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01_NATIVE.json'),
        'uiEvidence':info(A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01_UI.txt'),
        'actualCurrentAttachments':inputs,'attachmentScope':'Native attachment inventory contains all five conversation attachments; the exact current user turn states two attachments and both expected names are present.',
        'priorReviewReceipt':info(receipt),'preparation':info(A/'COMPANION_LIFE_10_EXACT_05_PREPARATION.json'),
        'contentHolds':['IN6-09-A','IN6-09-B'],'reviewRequested':'Eight exact files; ten complete procedures; six shared and four scoped rules;20 original scenarios;27 cases;38 independent branches;expanded native CR2 evidence.',
        'summaryOnlyUpdate':'Rank8Ward5 preparation and checkpoint32/queue25; full ward packet not yet delivered.',
        'localProofScreenshot':str(W/'companion-exact05-part5-delivered01.png'),
        'authorizationBasis':'Standing owner instructions explicitly authorize continued GPT collaboration, file audit and sharing current development with GPT.',
        'semanticAcceptanceClaimed':False,'sourceInformationDeleted':0,'wholeGameComplete':False
    }))
    print(json.dumps({'returnReceipt':info(receipt),'submissionReceipt':info(submission),'returnedManifestPayloadsVerified':9,'procedureOperationsPendingReplay':2}))


if __name__ == '__main__':
    main()
