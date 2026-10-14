"""Apply only completed GEX-01/GEX-02 authority, preserving the submitted bytes.

Prepared from the review's visible proposed patch. Execution requires the full
completed final response. That response supplies the required wording directly.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, zipfile

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(G).as_posix()

SHARED_OLD="An ordinary permitted unranked extraction can be attempted untrained with no tool PB and disadvantage. Dismantling and restoration require the actual trade credential."
SHARED_NEW="The ordinary Mining prospecting and mineral-assay procedures, and otherwise permitted unranked extraction, can be attempted untrained with no relevant tool PB and disadvantage. Dismantling and restoration require the actual trade credential."
MINING_OLD="Prospecting and assay use Core task degrees and natural shifts."
MINING_NEW=("For these ordinary Mining information tasks, an untrained lead uses WIS with no Miner's-tools proficiency contribution and disadvantage. "
 "No recipe-level or formula gate applies to these unranked tasks. The actual required implements, lawful access, physical suitability and the candidate's genuine qualifying operation remain necessary. "
 "Other advantage/disadvantage sources use Core arbitration; this does not add another die for each disadvantage source.\n\n"+MINING_OLD)
SUPPLY_OLD="Skinning's actual oils, tanning solution and salts use source-unit precision of 0.01; other materials require their governing physical precision."
SUPPLY_NEW=("Skinning's actual oils, tanning solution and salts use source-unit precision of 0.01. "
 "For Salvaging recipe creation, Purification agent and Stabilizer are likewise divisible accounting lots to 0.01 of their own exact source unit. "
 "On Failed creation, recover 25% per exact consumed non-catalyst identity and floor to that identity's allowed precision. "
 "Vessels and consumed-tool source units remain indivisible; other ingredients require their own governing physical precision. "
 "This is creation-failure recovery, not the finished tool's dismantling recovery percentage.")
INTERNAL_OLD="Skinning's reviewed oils, tanning solution and salts use 0.01 source units; whole fangs, tools and ordinary discrete parts do not."
INTERNAL_NEW=("Skinning's reviewed oils, tanning solution and salts use 0.01 source units. "
 "For Salvaging recipe creation, GT-V11 also explicitly binds Purification agent and Stabilizer as divisible accounting lots to 0.01 of their own exact source unit. "
 "Failed creation returns 25% per exact consumed non-catalyst identity, floored at that permitted precision, not the finished tool's dismantling percentage. "
 "Vessels, consumed tools, whole fangs and other discrete ingredient units remain indivisible unless their own actual governing profile permits division. "
 "Every returned quantity retains its identity, age, condition and required compatible containment; it is not money or new stock.")
REPLACEMENTS={
 'docs/mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md':[(SHARED_OLD,SHARED_NEW),(SUPPLY_OLD,SUPPLY_NEW)],
 'docs/mechanics/MINING_CANDIDATE_GUIDE.md':[(MINING_OLD,MINING_NEW)],
 'docs/director-only/GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md':[(INTERNAL_OLD,INTERNAL_NEW)],
 'tools/build_gathering_tool_guides_projection.py':[(INTERNAL_OLD,INTERNAL_NEW)],
}

def main():
 cap=read(A/'GATHERING_128_EXACT_VERDICT_CAPTURE.json')
 assert cap['completedFinalResponseCaptured'] and cap['turnId']=='a7bd2e52-b70c-4cba-85bc-7c73251f174c'
 vp=A/'GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md'
 assert sha(vp)==cap['verdictSha256']
 verdict=vp.read_text(encoding='utf-8')
 assert 'Only GEX-01 and GEX-02 prevent promotion' in verdict
 assert 'No additional generic source conference or full128-card resubmission is required' in verdict
 for exact in [SHARED_NEW,MINING_NEW.split('\n\n')[0],SUPPLY_NEW]:assert exact in verdict
 submission=read(A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json')
 assert sha(A/submission['bundleFile'])==submission['bundleSha256']
 assert all(sha(G/p)==h for p,h in submission['artifactHashes'].items())
 assert all(sha(G/p)==h for p,h in submission['protectedFiles'].items())
 plans={}
 for name,pairs in REPLACEMENTS.items():
  p=R/name;old=p.read_bytes().decode('utf-8');new=old
  with zipfile.ZipFile(A/submission['bundleFile']) as z:assert z.read(rel(p))==p.read_bytes(),name
  for search,replacement in pairs:
   assert new.count(search)==1,(name,search)
   new=new.replace(search,replacement,1)
  plans[p]=new
 archive=A/'gathering-before-exact-corrections';assert not archive.exists();archive.mkdir()
 saved=set(plans)|{A/n for n in ['GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json','GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json','GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json','GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json','GATHERING_TOOL_WORKED_CASE_VALIDATION.json']}
 manifest={}
 for p in saved:
  dst=archive/rel(p);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
  assert sha(dst)==sha(p);manifest[rel(p)]=sha(p)
 dump(archive/'MANIFEST.json',manifest)
 for p,new in plans.items():p.write_bytes(new.encode('utf-8'))
 status=read(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json')
 for p in plans:
  if rel(p) in status['outputs']:status['outputs'][rel(p)]=sha(p)
 status.update({'status':'GEX-01/GEX-02 applied; completion validation pending; unpromoted','exactReviewSubmitted':True,'exactReviewCompleted':True,'recipesApproved':0,'exactReviewAuthority':{'file':vp.name,'sha256':sha(vp),'turnId':cap['turnId'],'replyId':cap['replyId']},'next':'Rerun current-bound existing suites and required GEX regressions before authorized promotion'})
 dump(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json',status)
 receipt={'status':'GEX-01/GEX-02 text applied; validation pending; zero promotions','appliedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':status['exactReviewAuthority'],'corrections':['GEX-01','GEX-02'],'changes':{rel(p):{'beforeSha256':manifest[rel(p)],'afterSha256':sha(p),'binding':'Exact public replacement wording from completed final response; equivalent GT-V11 internal/generation carry-through'} for p in plans},'archive':rel(archive),'originalSourceObjectsChanged':False,'cardsChanged':False,'protectedInputsUnchanged':len(submission['protectedFiles']),'recipesApproved':0,'reviewerDownloadAvailable':False,'authorityIsCompleteCapturedFinalResponse':True}
 dump(A/'GATHERING_128_EXACT_CORRECTIONS_APPLIED.json',receipt)
 print(json.dumps(receipt))

if __name__=='__main__':main()
