"""Local archive/text verifier; executes none of the downloaded code."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import json,zipfile,hashlib,stat
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
archive=A/'DD_Part5_Copied_Feat_Integration_Review_01.zip'
root=A/'copied-feat-integration-part5-return-01'
receipt=A/'COPIED_FEAT_PART5_RETURN_01_LOCAL_PREFLIGHT.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def bind(p):
    b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':digest(b)}
def main():
    assert not receipt.exists() and (not root.exists() or not any(root.iterdir()))
    checks=[]
    def ck(label,test):
        checks.append({'check':label,'passed':bool(test)});assert test,label
    with zipfile.ZipFile(archive) as z:
        ck('Exact final archive',archive.stat().st_size==36867306 and digest(archive.read_bytes())=='006c3705fa56717b4aa6b4a7fcf08e658e91a1568bbbf2b3cb8a471df42dd064')
        ck('CRC',z.testzip() is None);names=z.namelist()
        ck('Unique52 safe regular members',len(names)==len(set(names))==52 and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n and not stat.S_ISLNK(z.getinfo(n).external_attr>>16) for n in names))
        manifest=json.loads(z.read('MANIFEST.json'))
        ck('Complete51 member manifest',manifest['fileCount']==len(manifest['files'])==51 and {x['path'] for x in manifest['files']}==set(names)-{'MANIFEST.json'})
        for b in manifest['files']:
            raw=z.read(b['path']);ck('Full manifest bytes '+b['path'],len(raw)==b['bytes'] and digest(raw)==b['sha256'])
        inputs=json.loads(z.read('INPUT_BINDINGS.json'))['inputs'];ck('Seven complete prior archives',len(inputs)==7)
        for b in inputs:
            raw=z.read(b['path']);local=A/PurePosixPath(b['path']).name
            ck('Input exactly equals local '+local.name,local.exists() and local.read_bytes()==raw and len(raw)==b['bytes'] and digest(raw)==b['sha256'])
        bindings=json.loads(z.read('CODE_BINDINGS.json'));operations=json.loads(z.read('CODE_OPERATIONS.json'))
        ck('Four files eleven operations no ruleJSON change',bindings['fileCount']==len(bindings['files'])==4 and operations['operationCount']==len(operations['operations'])==11 and operations['ruleJsonOperationCount']==0)
        for b in bindings['files']:
            before=z.read('baseline/'+b['path']);after=z.read('proposed/'+b['path'])
            ck('Live baseline exact '+b['path'],(G/b['path']).read_bytes()==before and len(before)==b['before']['bytes'] and digest(before)==b['before']['sha256'])
            ck('Proposed exact '+b['path'],len(after)==b['after']['bytes'] and digest(after)==b['after']['sha256'])
            ops=[o for o in operations['operations'] if o['path']==b['path']];ck('Exact operation count '+b['path'],len(ops)==b['operations'])
            current=before
            for o in ops:
                old=o['before'].encode();new=o['after'].encode();ck('Unique before '+o['id'],o['kind']=='replace-exact-text' and current.count(old)==1);current=current.replace(old,new,1)
            ck('Full forward bytes '+b['path'],current==after)
            for o in reversed(ops):
                old=o['before'].encode();new=o['after'].encode();ck('Unique reverse '+o['id'],current.count(new)==1);current=current.replace(new,old,1)
            ck('Full reverse bytes '+b['path'],current==before)
        payload=z.read('proposed/DescentReviewChanges/ReviewBible/tools/feat335_copy_payloads.py').decode()
        ck('Inactive reducer guards still present',"any(r.next_healing for r in actor['healingReductions'])" in payload and "any(r.next_healing for r in world.actors[eligible[0]]['healingReductions'])" in payload)
        ck('Buffer expiry return still discarded','self.buffers.expire(marker);self.projection()' in payload)
        root.mkdir(exist_ok=True)
        for n in names:
            dst=root/PurePosixPath(n);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(z.read(n))
        r={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'archive-and-exact-change-integrity-verified-substantive-followup-required','archive':bind(archive),'actualGptFinal':bind(A/'GPT_PART5_COPIED_FEAT_FINAL_01_NATIVE.json'),'verificationScript':bind(Path(__file__)),'extractedRoot':root.relative_to(G).as_posix(),'memberCount':52,'manifestBoundFiles':51,'priorArchivesExactlyMatchLocal':7,'liveBaselinesExactlyMatch':4,'exactOperationsReplayedAndReversed':11,'checks':checks,'checkCount':len(checks),'failures':0,'gptFinalFindingCount':5,'independentLocalDiagnosticGroups':6,
            'openFollowup':[{'id':'LOCAL-INACTIVE-MEND-REDUCER','evidence':bind(A/'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json'),'finding':'Both absent and suppressed next-healing records were independently reproduced as erroneous rejection. Both final proposed payload guards retain unfiltered any(next_healing); disposition/correction remains required.'},
                {'id':'LOCAL-SHARED-BUFFER-EXPIRY','evidence':bind(A/'COPIED_FEAT_PART5_LOCAL_DEFECT_REPRODUCTION_02.json'),'finding':'Final proposed CopyPayloadWorld.advance still discards BufferLedger.expire return instructions. The independently reproduced Oracle expiry instruction loss is not resolved by native-concentration preflight.'}],
            'additionalGptFindingsForLocalReview':['CFI-05 extra-turn ID reused as regular start','CFI-03 native concentration divergence guard'],
            'limits':['Complete archive/input/baseline/forward/reverse integrity only;not semantic acceptance of every proposed code change.','No downloaded scripts or proposed code executed. GPT456existing assertions/47tests/880checks remain its reported results.','Full Ready,positive linked Shaman Step,printed nonteleport Step and next-attack/next-save Boon remain required. Rejecting an unsupported path is not completion of its printed benefit.','Full68-history/source-member/profile semantic comparisons remain to be inspected independently.'],
            'implementationApplied':False,'newRuleAdoptions':0,'sourceInformationDeleted':0,'ownerImplementationReservationRetained':True}
        with receipt.open('x',encoding='utf8',newline='\n') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
        print(json.dumps({'receipt':bind(receipt),'checks':len(checks),'failures':0,'openLocalDefectGroups':2}))
if __name__=='__main__':main()
