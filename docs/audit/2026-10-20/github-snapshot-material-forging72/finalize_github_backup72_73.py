"""Verify the snapshot plus its separate verification-record commit; no history rewrite."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,hashlib
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
H=W.parent/'audit_tools';spec=importlib.util.spec_from_file_location('backup72_delivery',H/'deliver_progress_2026_10_20_material_forging72.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def main():
 final=b.git('rev-parse','HEAD').decode().strip();snapshot=b.git('rev-parse','HEAD^').decode().strip();remote=b.git('ls-remote','origin','refs/heads/main').decode().split()[0]
 assert final==remote and b.git('rev-parse','HEAD^^').decode().strip()==b.BASE
 assert b.git('status','--porcelain=v1','-z')==b''
 report=b.REPORT+'/STAGED_VERIFICATION.json'
 assert b.git('diff-tree','--no-commit-id','--name-only','-r','HEAD','-z').decode().strip('\0')==report
 expected=json.loads((b.W/'expected-staged-blobs.json').read_bytes());tree=b.h.oldtree(final);prior=b.h.oldtree(b.BASE);snap=b.h.oldtree(snapshot)
 assert all(tree.get(n,{}).get('oid')==oid for n,oid in expected.items())
 assert set(prior)<=set(tree) and set(tree)-set(prior)-set(expected)=={report}
 assert tree[report]['oid']==b.h.p.blob(b.lp(b.D/report).read_bytes())
 assert set(snap)<=set(tree) and set(tree)-set(snap)=={report}
 assert all(tree[n]['oid']==v['oid'] for n,v in snap.items())
 verification=json.loads(b.lp(b.D/report).read_bytes())
 assert verification['stagedBlobMismatches']==verification['deletedEntries']==0
 assert verification['expectedBlobsVerified']==len(expected) and verification['priorTrackedEntriesRetained']==len(prior)
 receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'sourceRoot':str(b.G),'deliveryRoot':str(b.D),
  'baseCommit':b.BASE,'snapshotCommit':snapshot,'verificationRecordCommit':final,'commit':final,'remoteMain':remote,
  'url':f'https://github.com/BordelonDevOps/DecenniumDescent/commit/{final}',
  'worktreeClean':True,'expectedBlobsVerified':len(expected),'totalCommitEntries':len(tree),'priorTrackedEntriesPreserved':len(prior),
  'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'authoredCounts':{'reviewed':525,'pending':323},
  'developmentContinues':True,'wholeGameCompleted':False,'scope':b.SCOPE,
  'verificationRecordFollowup':'Snapshot commit was already pushed when its generated verification record was found untracked. A second ordinary commit adds only that exact record. Both commits verified against the full expected snapshot; no amend,force push or history rewrite.',
  'receiptVerifier':Path(__file__).name}
 raw=b.jsraw(receipt);b.write_new(b.W/'push-receipt.json',raw);b.write_new(b.G/b.REPORT/'PUSH_RECEIPT.json',raw)
 b.write_new(b.G/b.REPORT/Path(__file__).name,Path(__file__).read_bytes());print(json.dumps(receipt))
if __name__=='__main__':main()
