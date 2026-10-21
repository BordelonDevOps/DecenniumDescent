"""Record a completed GPT return without mistaking its claims for local validation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
name='GPT_PART5_RANK7_READY_DEADLINE_RETURN_03_NATIVE.json'
out=A/'RANK7_READY_DEADLINE_RETURN_03_AVAILABLE_75.json'
assert not out.exists() and not (A/name).exists() and not (A/Path(__file__).name).exists()
data=json.loads((W/name).read_bytes());turn=data['turns'][0]
assert turn['id']=='0a9e0b92-ece2-4815-84d4-3b2baf6f4712'
reply=next(i for i in turn['items'] if i['type']=='agentMessage')
assert reply['id']=='b7cc95cd-bc1a-40c7-802a-b09859e01d9c'
assert '116,652,484' in reply['text'] and 'ab898f5bcf51351b3aa93c92c2d5949a34e25e54e43570093a76ed75dda6a403' in reply['text']
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(A/name).write_bytes((W/name).read_bytes())
receipt={'id':'RANK7-READY-DEADLINE-RETURN03-AVAILABLE-75','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkpointBeforeFinal':info(A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_ACCEPTANCE_UNITY_INTAKE_75.json'),'actualFinal':info(A/name),'actualAssistant':'b7cc95cd-bc1a-40c7-802a-b09859e01d9c','status':'COMPLETE_GPT_REPLY_PRESERVED; FULL_ARCHIVE_DOWNLOAD_AND_LOCAL_VALIDATION_PENDING','reportedArchive':{'name':'DD_Rank7_Identity_Casting_5_Part5_Ready_Deadline_Return_03.zip','bytes':116652484,'sha256':'ab898f5bcf51351b3aa93c92c2d5949a34e25e54e43570093a76ed75dda6a403'},'reportedModel':{'bytes':12000315,'sha256':'949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a'},'reportedCorrection':'Six scalar deadlines62 to61; complete case/state mirrors; boundary60.9-valid,61-and61.1-expired with once-only cleanup. All other model values claimed unchanged.','reportedVerificationNotLocallyReproduced':{'manifestFiles':93,'archiveMembers':94,'incrementalOperations':6,'alternativeOperations':44,'completeArtifactReplacements':17,'authorSourceAndStateChecks':703,'authorFreshExtractionChecks':797,'authorIsolatedTests':172},'localDownloadAttempt':'Review text accessible through native read. Browser control lost attachment and timed out while restoring the completed conversation; no archive download action completed. No downloaded archive falsely accepted.','historicalCountInGptReply':39,'actualCurrentAcceptedButUnapplied':45,'countExplanation':'Six Rank8 successors were independently accepted locally after the Rank7 request was sent; reply repeats historical39. Inform GPT on next successful conference. Rank7 adds no accepted identities yet.','newAcceptedIdentities':0,'implementationApplied':False,'runtimeTestsExecuted':0,'downloadedCodeExecuted':False,'sourceInformationDeleted':0,'nextAction':'Recover the full original116,652,484-byte archive through the authorized browser and compare hash. Inspect/reconstruct as data only; never execute downloaded Python. Preserve all original sources and perform exact six-field and boundary semantic review before accepting.'}
out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
print(json.dumps({'receipt':info(out),'native':info(A/name),'acceptedButUnapplied':45,'rank7Acceptance':False}))
