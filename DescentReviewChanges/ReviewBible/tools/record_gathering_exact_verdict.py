"""Bind the complete connector final response, without relying on failed downloads."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 p=A/'GATHERING_128_EXACT_FINAL_THREAD_CAPTURE.json';d=read(p);t=d['turns'][0]
 assert t['id']=='a7bd2e52-b70c-4cba-85bc-7c73251f174c' and t['status']=='completed'
 a=next(i for i in t['items'] if i['type']=='agentMessage')
 assert a['id']=='af756084-996a-4143-a34a-baf1da9bcce3'
 v=A/'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md'
 assert v.read_text(encoding='utf-8').rstrip('\n')==a['text'].rstrip('\n')
 assert a['text'].endswith('then careful cosmology review.') and len(a['text'])<20000
 assert 'No additional generic source conference or full128-card resubmission is required solely for those changes.' in a['text']
 cap={'threadId':d['thread']['id'],'turnId':t['id'],'replyId':a['id'],'completedFinalResponseCaptured':True,'capturedAtUtc':datetime.now(timezone.utc).isoformat(),'characters':len(a['text']),'completeConnectorTextMatchesSavedVerdict':True,'verdictFile':v.name,'verdictSha256':sha(v),'threadCaptureFile':p.name,'threadCaptureSha256':sha(p),'reviewerFileDownloadStatus':'Browser download event timed out and no matching local download found; complete final response is independently captured and is controlling authority','noReplyTruncationObserved':True,'conditions':['GEX-01','GEX-02'],'promotionConditional':True,'recipesPromoted':0}
 dump(A/'GATHERING_128_EXACT_VERDICT_CAPTURE.json',cap)
 scopes={}
 for code,next_code,trade in [('GEX-01','4. GEX-02','Mining'),('GEX-02','5. Public component','Salvaging')]:
  block=a['text'].split('## '+('3. GEX-01' if code=='GEX-01' else '4. GEX-02'),1)[1].split('## '+next_code,1)[0]
  affected=block.split('### Affected recipes',1)[1].split('### Exact replacement wording',1)[0]
  ids=list(dict.fromkeys(re.findall(r'recipe-\d+',affected)))
  scopes[code]={'affectedRecipeIds':ids,'trade':trade}
 assert len(scopes['GEX-01']['affectedRecipeIds'])==26 and len(scopes['GEX-02']['affectedRecipeIds'])==29
 scope={'provenance':'Local structured extraction of completed final response, not downloaded reviewer summary','authority':cap,'all128Covered':True,'promotionAfterConditionsAuthorized':True,'archiveSha256':read(A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json')['bundleSha256'],'namedCorrections':scopes,'recipesPromoted':0}
 dump(A/'GATHERING_128_EXACT_VERDICT_SCOPE.json',scope)
 print(json.dumps({'status':'Complete final response captured','replyId':a['id'],'characters':len(a['text']),'verdictSha256':sha(v),'conditionalCorrections':list(scopes),'recipesPromoted':0}))
if __name__=='__main__':main()
