"""Record the actual saved request; leave every submitted payload frozen."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, zipfile
G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
def load(p): return json.loads(p.read_text('utf-8-sig'))
def info(b): return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
p=load(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')
d=load(A/'EXPEDITION_INTEGRATED_V3_SAVED_REQUEST.json')
out=A/'EXPEDITION_INTEGRATED_V3_SUBMISSION.json'
assert not out.exists()
t=d['turns'][0]
assert t['id']=='999dd180-8e31-48be-ad59-58f8f65e1a1c'
message=t['items'][0]['content'][0]['text']
prompt=(A/'CODEX_EXPEDITION_INTEGRATED_V3_PROMPT.txt').read_text('utf-8-sig')
assert message==prompt.rstrip('\r\n')+'\n\n[User attached 1 file; file contents were not included]', 'Saved request differs from prepared prompt'
attachment=next(x for x in d['attachments'] if x['name']=='DD_Expedition_Transport_Social_58_Source_v3.zip')
archive=G/p['archive']['path']
ab=archive.read_bytes()
assert info(ab)=={k:p['archive'][k] for k in ['bytes','sha256']}
assert info(Path(attachment['path']).read_bytes())==info(ab)
stable=[]
with zipfile.ZipFile(archive) as z:
    manifest=json.loads(z.read('FILE_MANIFEST.json'))
    assert manifest==p['manifest'] and len(manifest)==304
    assert set(z.namelist())==set(manifest)|{'FILE_MANIFEST.json'}
    for rel,want in manifest.items():
        assert info(z.read(rel))==want, rel
        fp=G/rel
        if fp.exists():
            assert info(fp.read_bytes())==want, rel
            stable.append(rel)
        else:
            assert rel=='README_EXPEDITION_INTEGRATED_V3.md', rel
result={
 'status':'SUBMITTED; actual GPT source-authoring conference in progress; verdict pending',
 'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'threadId':d['thread']['id'],'threadTitle':d['thread']['title'],
 'savedUserMessageId':t['id'],
 'submittedAtUtc':datetime.fromtimestamp(t['startedAt'],timezone.utc).isoformat(),
 'archive':p['archive'],'payloadFiles':304,'currentRepositoryPayloadsVerified':len(stable),
 'attachmentReadbackBytesMatch':True,'savedPromptMatchesExceptFinalNewline':True,
 'questionCounts':p['questionCounts'],'questions':58,
 'originalV2PayloadsPreserved':194,'historicalCurrentPairs':len(p['historicalCurrentPairs']),
 'browserObservation':'Latest live response says archive and all 304 payload hashes match; Stop button present. Connector idle describes its synchronized snapshot and is not a final verdict.',
 'browserProof':{'path':'docs/audit/2026-10-08/full-game/EXPEDITION_INTEGRATED_V3_BROWSER.png',**info((A/'EXPEDITION_INTEGRATED_V3_BROWSER.png').read_bytes())},
 'historicalPreparationStatusPreserved':True,'allSubmittedPayloadsRemainFrozen':True,
 'newApprovals':0,'sourceInformationDeleted':0,'runtimeImplemented':False,
 'cosmologyReviewed':False,'gitPushPerformed':False,
 'next':'Read the complete source-authoring verdict, author the complete chapters/profiles/records/examples, then submit an exact candidate. Final whole-game flow agreement precedes authorized push; verified remote precedes cosmology.'
}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=False))
