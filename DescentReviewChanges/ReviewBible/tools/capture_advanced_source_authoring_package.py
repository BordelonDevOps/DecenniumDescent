"""Preserve and verify a completed reviewer download without executing its files."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, shutil, zipfile

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--package',required=True);args=parser.parse_args()
    downloaded=Path(args.package).resolve();assert downloaded.is_file()
    thread_file=A/'ADVANCED_CRAFT_JOINT_FINAL_THREAD_CAPTURE_PARTIAL.json';thread=read(thread_file)
    assert thread['thread']['id']=='6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b'
    turn=next(t for t in thread['turns'] if t['id']=='6b7737b0-b71b-4bfc-8627-4705e81fc26c')
    assert turn['status']=='completed'
    answers=[i for i in turn['items'] if i['type']=='agentMessage'];assert answers
    answer=answers[-1];assert answer['id']=='af2a24f6-c967-4aa5-a28e-5c2e9de13cb6'
    final_text=answer.get('text')
    if final_text is None:
        blocks=answer['content'];assert not any(x.get('truncated',False) for x in blocks)
        final_text='\n'.join(x['text'] for x in blocks if x['type']=='text')
    assert final_text and '167' in final_text
    assert answer.get('truncated') is True and len(final_text)==20000
    tail_file=A/'ADVANCED_CRAFT_FINAL_BROWSER_SECTIONS_6_7.txt'
    tail=tail_file.read_text(encoding='utf-8')
    assert tail.startswith('6. Tinkering and the 18 class-device interfaces')
    assert 'verified remote commit remains before careful cosmology review.' in tail
    assert '## 6. Tinkering and the 18 class-device interfaces' in final_text
    final_text=('Capture note: sections1–5 and introduction retain connector Markdown. Sections6–7 are the complete rendered browser text from the same final reply; mathematical presentation can repeat visual and accessible forms. This is a content-complete composed capture, not a byte-identical export of the final-message Markdown. The exact downloaded verdict is the operative source-authoring authority.\n\n'+final_text.split('## 6. Tinkering and the 18 class-device interfaces',1)[0]+tail)
    submission=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')
    assert all(sha(G/p)==h for p,h in submission['currentFileHashes'].items())
    dest=A/'advanced167-source-authoring-reviewer-files'
    copy=A/'DD_Advanced_167_Source_Authoring_Decisions.zip'
    capture=A/'ADVANCED_CRAFT_SOURCE_VERDICT_CAPTURE.json'
    verdict=A/'GPT_ADVANCED_167_SOURCE_AUTHORING_VERDICT.md'
    reply=A/'GPT_ADVANCED_167_SOURCE_AUTHORING_REPLY.md'
    assert not any(p.exists() for p in [dest,copy,capture,verdict,reply]), 'Do not overwrite prior captures'
    with zipfile.ZipFile(downloaded) as z:
        names=z.namelist();assert len(names)==len(set(names))==13 and z.testzip() is None
        assert all(Path(n).name==n and '/' not in n and '\\' not in n and n not in ['.','..'] for n in names)
        manifest=json.loads(z.read('FILE_MANIFEST_AUTHORING.json'))
        assert set(manifest)|{'FILE_MANIFEST_AUTHORING.json'}==set(names)
        assert all(len(z.read(n))==m['bytes'] and hashlib.sha256(z.read(n)).hexdigest()==m['sha256'] for n,m in manifest.items())
        assert 'DD_Advanced_167_Source_Authoring_Verdict.md' in names
        assert 'ADVANCED_167_AUTHORING_REGISTER.json' in names and 'CASE_68_DISPOSITION_INDEX.json' in names
        payload={n:z.read(n) for n in names}
    assert sha(downloaded)=='f868ca4cc85cad004fb6c8ecc69d3095bf8e7d244f4bf7c4918729ff874007ce'
    assert payload['DD_Advanced_167_Source_Authoring_Verdict.md']==Path('C:/Users/cbord/Downloads/DD_Advanced_167_Source_Authoring_Verdict.md').read_bytes()
    # All validation above is read-only; only now preserve exact downloaded bytes.
    shutil.copy2(downloaded,copy);dest.mkdir()
    for n,b in payload.items():(dest/n).write_bytes(b)
    verdict.write_bytes(payload['DD_Advanced_167_Source_Authoring_Verdict.md'])
    reply.write_text(final_text,encoding='utf-8')
    result={'status':'complete final reply and reviewer source-authoring package captured; not exact-card approval',
            'capturedAtUtc':datetime.now(timezone.utc).isoformat(),'threadId':thread['thread']['id'],'turnId':turn['id'],'replyId':answer['id'],
            'threadCaptureFile':thread_file.name,'threadCaptureSha256':sha(thread_file),'finalReplyFile':reply.name,'finalReplySha256':sha(reply),
            'downloadedPackagePath':str(downloaded),'packageFile':copy.name,'packageSha256':sha(copy),'packageBytes':copy.stat().st_size,
            'reviewerFilesDirectory':dest.name,'reviewerManifestVerified':True,'reviewerPayloadFiles':13,
            'finalReplyCaptureMethod':'Connector original first20000 characters preserved with truncated flag; complete browser sections6–7 captured separately and composed at section boundary. Final UI message id matched connector id.',
            'browserTailFile':tail_file.name,'browserTailSha256':sha(tail_file),'browserFinalMessageCharacters':26392,
            'interimLiveDraftIsNotAuthority':True,'interimLivePackageNotUsed':'DD_Advanced_167_Source_Authoring_Package.zip; earlier live159558-byte verdict and27-model draft superseded by actual final171095-byte verdict and22 defaults/variants',
            'verdictFile':verdict.name,'verdictSha256':sha(verdict),'verdictBytes':verdict.stat().st_size,
            'reviewedInputBundle':submission['bundleFile'],'reviewedInputBundleSha256':submission['bundleSha256'],
            'allSubmittedFilesUnchanged':True,'submittedFiles':len(submission['currentFileHashes']),
            'capturedFiles':{n:sha(dest/n) for n in names},'newAdvancedRecipeApprovals':0,
            'sourceInformationDeleted':0,'githubPushPerformed':False,'cosmologyReviewed':False,
            'nextAction':'Read complete verdict and all structured authoring data; reconcile against source records, then author167 exact candidates and submit their complete operational package for review.'}
    dump(capture,result)
    print(json.dumps({k:result[k] for k in ['status','replyId','packageFile','packageSha256','verdictBytes','verdictSha256','submittedFiles','newAdvancedRecipeApprovals']}))

if __name__=='__main__':main()
