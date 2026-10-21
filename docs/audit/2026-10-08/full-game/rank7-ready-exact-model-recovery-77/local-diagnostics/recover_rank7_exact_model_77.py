"""Recover the exact reported MODEL from locally preserved bytes; execute no downloaded code."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def at(d,p):
 for k in p.strip('/').split('/') if p else []:d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def setat(d,p,v):
 parent,key=p.rsplit('/',1);x=at(d,parent);x[int(key) if isinstance(x,list) else key]=v
root=A/'rank7-ready-exact-model-recovery-77';archive=A/'DD_Rank7_Exact_Model_Recovery_77.zip';receipt=A/'RANK7_EXACT_MODEL_RECOVERY_77.json';script=A/Path(__file__).name
assert not any(p.exists() for p in [root,archive,receipt,script])
oldp=A/'rank7-identity-casting5-part5-correction-return-02/MODEL.json';old=oldp.read_bytes();m=json.loads(old);new=deepcopy(m);checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
ck('Exact locally preserved Return02 MODEL',len(old)==12000315 and hashlib.sha256(old).hexdigest()=='fbdfd5c299d7a501d53eedad03df82211da312df783b06d68e1dae3de5fd0a36')
prefix='/currentVectors/2/independentBranches/0'
paths=[prefix+x+'/sourceLedger/hold/deadline' for x in ['/timeline/0/after','/timeline/1/before','/timeline/1/after','/timeline/2/before','/timeline/2/after','/expectedFinalState']]
ops=[]
for p in paths:
 ck('Actual old deadline '+p,at(new,p)==62);ops.append({'op':'replace','pointer':p,'beforeExists':True,'before':62,'after':61});setat(new,p,61)
raw=enc(new);reported='949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a'
ck('Reconstructed entire MODEL matches reported Return03 bytes and SHA256',len(raw)==12000315 and hashlib.sha256(raw).hexdigest()==reported)
reverse=deepcopy(new)
for op in reversed(ops):ck('Exact successor field '+op['pointer'],at(reverse,op['pointer'])==op['after']);setat(reverse,op['pointer'],op['before'])
ck('Full reversal restores every original byte',enc(reverse)==old)
b=at(new,prefix);before=b['timeline'][2]['before'];after=b['timeline'][2]['after'];mage=after['actors']['mage']
ck('Same named branch',b['id']=='RIC5-02-A-a')
ck('Actual unchanged55/61 cadence',(mage['regularStart'],mage['nextRegularStart'])==(55,61))
ck('Unchanged prep,Meta expiry,release sequence',[x['timeSeconds'] for x in b['timeline']]==[56.1,60.5,60.9])
ck('Real pre-expiry release',b['timeline'][2]['timeSeconds']<before['sourceLedger']['hold']['deadline'])
ck('Equality and later not pre-expiry',not 61<before['sourceLedger']['hold']['deadline'] and not 61.1<before['sourceLedger']['hold']['deadline'])
ck('No fabricated release START',b['timeline'][2]['regularStartsBeforeEvent']==[])
ck('Actual Reaction consumed',before['actors']['mage']['reaction'] is True and mage['reaction'] is False)
ck('No extra Action',before['actors']['mage']['action'] is False and mage['action'] is False)
ck('RP,Dissonance,Refrain,class uses unchanged',(mage['rp'],mage['dissonance'],mage['refrain'],mage['metaspellUses'])==(38,0,0,0))
ck('Original six damage retained',before['actors']['target']['hp']==80 and after['actors']['target']['hp']==74)
ck('Consumed hold and ended concentration',after['sourceLedger']['hold']['state']=='consumed' and mage['concentration'] is None)
ck('Exact final state mirror',b['expectedFinalState']==after)
ck('All other MODEL fields byte-equivalent after reverse',reverse==m)
originalArchive=A/'DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip'
ck('Exact complete previous archive',info(originalArchive)['sha256']=='d063125b1b570230afa9cef56714efc26d011dd9ca0dd56c064d5473c85b63a1')
localReview=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_74.json';review=json.loads(localReview.read_bytes())
ck('Prior one remaining deadline finding',review['diagnosticCheckCount']==554 and review['diagnosticFailures']==review['findingsCount']==1)
reportedNative=A/'GPT_PART5_RANK7_READY_DEADLINE_RETURN_03_NATIVE.json';missingNative=A/'GPT_PART5_RANK7_EXACT_RETURN_UNAVAILABLE_77_NATIVE.json'
sourcePaths=[localReview,A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json',reportedNative,missingNative,A/'GPT_PART5_RANK7_READY_DEADLINE_CORRECTION_14_REQUEST.txt',A/'RANK7_READY_DEADLINE_RETURN_03_AVAILABLE_75.json',A/'GPT_PART5_STATUS_SYNC_15_NATIVE.json']
request='''DECENNIUM DESCENT — EXACT RANK7 MODEL RECOVERY / BOUNDED ARTIFACT DELIVERY

Codex preserved your report that the exact116,652,484-byte Ready-deadline Return03 ZIP is unavailable in the current session. Its original identity/history remains preserved and is not replaced by a claim of download.

The supplied full recovered MODEL.json is12,000,315 bytes, SHA256949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a, EXACTLY matching the MODEL you reported in assistant b7cc95cd-bc1a-40c7-802a-b09859e01d9c. Codex reconstructed it from the complete preserved Return02 MODEL by the six expressly requested62-to61 deadline replacements only, then reversed all six and recovered every original byte. The full prior archive, source/state review, exact affected branch before/after, new check report, original request and actual completed replies are supplied. Downloaded code was not executed.

Please verify these actual bytes and deliver a newly identified RECOVERY return containing the complete current artifacts corresponding to this exact MODEL. Do not claim that a newly packaged ZIP has the original Return03 archive hash or that Codex downloaded the missing archive. Keep MODEL byte-identical; do not redo the five-spell authorship, reopen the reconciled original fixes, or alter any other MODEL values. Supply complete case/evidence/procedure/question/chapter mirrors and source-linked finding disposition, plus the genuine separate60.9/61/61.1 Ready-boundary diagnostic. Keep the diagnostic scheduler scope explicit: expiry of the hold does not invent a free Action/Reaction or pretend an isolated hold check implements the complete regular-START scheduler.

Use the six supplied operations as the incremental Return02 path. Any original-source or Return01 reconstruction path is an alternative, never cumulative. Preserve the original27+11 history and all source/access/prior case records. All exact prior bytes remain in the supplied original archive and locally; the new delivery can bind that input archive and its exact members instead of nesting it again or embedding duplicate117MB full-text replacement maps. Return the FULL current artifacts, not patch-only or summary-only cards. Include hashes/lengths and a clear manifest distinguishing current artifacts, retained original input, and newly authored recovery diagnostics. Split into separately hash-bound parts if necessary to keep each downloadable file below100MB without discarding information. Do not execute supplied project/downloaded Python as authority; independently inspect the small delta.

Current applied525/323/249/173 and45accepted-unapplied remain unchanged. Rank7 remains pending independent verification of this newly delivered complete artifact set. Owner implementation reservation,11 conditional branches and five whole positive-case holds remain. No canonical/index/registry/helper/runtime/cosmology changes, balance or release approval. This is a bounded recovery/delivery task, not another cohort. Identify any actual additional contradiction separately; do not silently change the exact recovered MODEL.
'''
members={'REQUEST.txt':request.encode(),'MODEL.json':raw,'EXACT_OPERATIONS_FROM_RETURN02.json':enc({'base':info(oldp),'targetBytes':len(raw),'targetSha256':reported,'operations':ops,'pathKind':'incremental; alternatives are not cumulative','serialization':'UTF-8 JSON indent2 ensure_ascii=False trailing LF; original key order'}),'COMPLETE_AFFECTED_BRANCH.json':enc({'pointer':prefix,'before':at(m,prefix),'after':b}),'LOCAL_RECOVERY_CHECK.json':enc({'checks':checks,'checkCount':len(checks),'failures':0,'scope':'Exact entire-model reconstruction, reversible preservation and bounded existing release arithmetic; not original ZIP recovery, artifact-mirror validation, scheduler/runtime testing or acceptance.'}),'input/'+originalArchive.name:originalArchive.read_bytes(),'local-diagnostics/'+Path(__file__).name:Path(__file__).read_bytes()}
for p in sourcePaths:members['evidence/'+p.name]=p.read_bytes()
for binding in review['sourceBindings']:
 p=G/binding['path'];assert info(p)==binding;members['sources/'+binding['path']]=p.read_bytes()
members['MANIFEST.json']=enc({'files':[{'path':n,'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for n,v in sorted(members.items())],'originalReturn03ArchiveRecovered':False,'exactReportedModelReconstructed':True,'newRuleAdoptions':0})
root.mkdir()
for n,v in members.items():
 p=Path('\\\\?\\'+str((root/n).resolve()));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v)
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,v in sorted(members.items()):z.writestr(n,v)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(members)
 for n,v in members.items():assert z.read(n)==v
ck('Original MODEL still untouched',oldp.read_bytes()==old)
script.write_bytes(Path(__file__).read_bytes())
receipt.write_bytes(enc({'id':'RANK7-EXACT-MODEL-RECOVERY-77','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'EXACT_REPORTED_MODEL_RECOVERED_COMPLETE_DELIVERY_PACKET_PREPARED_UNSENT','model':info(root/'MODEL.json'),'originalModel':info(oldp),'archive':info(archive),'manifest':info(root/'MANIFEST.json'),'operations':info(root/'EXACT_OPERATIONS_FROM_RETURN02.json'),'check':info(root/'LOCAL_RECOVERY_CHECK.json'),'request':info(root/'REQUEST.txt'),'reportedFinal':info(reportedNative),'actualUnavailableResponse':info(missingNative),'checks':len(checks),'allArchiveMembersCompared':True,'originalReturn03ZipRecovered':False,'completeReturn03ArtifactSetRecovered':False,'newAcceptedIdentities':0,'implementationApplied':False,'sourceInformationDeleted':0}))
print(json.dumps({'receipt':info(receipt),'archive':info(archive),'model':info(root/'MODEL.json'),'checks':len(checks),'members':len(members)}))
