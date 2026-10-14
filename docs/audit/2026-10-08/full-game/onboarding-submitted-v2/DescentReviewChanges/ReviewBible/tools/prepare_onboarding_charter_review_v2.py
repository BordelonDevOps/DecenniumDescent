"""Freeze the six teaching/charter manuscripts and the completed recipe receipt."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 zpath=A/'DD_Onboarding_and_Design_Charter_Exact_Review_v2.zip';out=A/'ONBOARDING_CHARTER_EXACT_PREPARATION.json';assert not zpath.exists() and not out.exists()
 prior=read(A/'ONBOARDING_EXACT_DRAFTS_PREPARATION.json');assert sha(A/prior['bundleFile'])==prior['bundleSha256']
 changes={n:{'preparedSha256':h,'currentSha256':sha(G/n)} for n,h in prior['sourceAndDraftHashes'].items() if sha(G/n)!=h}
 assert set(changes)=={'START_HERE.md'},changes
 receipt=read(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json');assert receipt['aggregateReviewedRecipes']==687
 assert all(sha(G/n)==h for n,h in receipt['finalArtifactHashes'].items())
 files={G/n for n in prior['sourceAndDraftHashes']}
 additions=[A/'DESIGN_CHARTER_CANDIDATE.md',R/'docs/mechanics/DESIGN_DOCTRINE.md',R/'docs/mechanics/GAMEPLAY_LOOP_CANON.md',G/'docs/reference/Player_Rulebook_v6_source_text.txt',G/'docs/canon/CANON_MANIFEST.json',A/'EXPEDITION_HAVEN_FLOW_SOURCE_AUDIT.md',A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json',A/'ADVANCED_167_EXACT_COMPLETION_VALIDATION.json',A/'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json',R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json',R/'tools/validate_advanced_exact_corrections.py',R/'tools/finalize_advanced_exact_review.py',Path(__file__).resolve()]
 files.update(additions);files.update(G/n for n in receipt['finalArtifactHashes'])
 files.update(A/'advanced167-exact-reviewer-files'/n for n in ['AEX_167_Exact_Review_Verdict.md','AEX_167_CORRECTIONS.json','AEX_167_FOCUSED_REGRESSIONS.json'])
 cases=A/'ONBOARDING_CHARTER_EXACT_REVIEW_SCOPE.md'
 cases.write_text('''# Onboarding and design charter — exact review scope

Review six complete actual manuscripts: FIRST_BARD_WALKTHROUGH.md, SESSION_ZERO_PLAYTEST.md, NEWCOMER_PLAYER_GUIDE.md, NEWCOMER_DIRECTOR_GUIDE.md, RESONANCE_CHEATSHEET.md and DESIGN_CHARTER_CANDIDATE.md. The first five retain the prepared v1 bytes. The charter was separately grounded in the owner-locked doctrine and actual loop/character sources. This is their first exact notebook review, not a new generic source-authoring conference.

Apply all16 NW-01–16 cases in ONBOARDING_EXACT_REVIEW_CASES.md, plus these four:

| ID | Required manuscript check |
|---|---|
| NW-17 | Does the charter faithfully synthesize the owner-locked doctrine and actual expedition/extraction/Haven/Opening loop, while treating provisional calibration targets and unsettled flow details accurately? Identify exact contradictions, not new setting inventions. |
| NW-18 | Do the charter and teaching path preserve actual Base/Arch/Hero schedules, milestone versus optional-XP choice, consequences and spent-resource continuity without promising unearned grants or guaranteed survival? |
| NW-19 | Are session length, table agreements, tone and safety presented as practical table choices? Does any teaching text confuse human usability/balance evidence with reference checks or claim the whole campaign is finished? |
| NW-20 | Can these six texts form a coherent entry path under their stated playtest scope? Return finite corrections and exact acceptance conditions. DD-01 final whole-game consistency remains open even if this charter synthesis is accepted. |

The completed advanced-recipe files/receipts are continuity evidence: AEX-01–07 fulfilled under the existing conditional authority,167 advanced and100 public promoted,aggregate687/687 and433/433. The three original reports bind the prepromotion corrected bytes; final receipt proves review-label-only normalization and supplies final hashes.33 focused cases are authored adjudications/reference calculations,not live advanced runtime tests. The navigation receipt accounts for the three protected catalog/navigation files updated only after promotion,with their prior bytes preserved. No fresh all-source crafting conference is requested.

Give one bounded exact six-manuscript verdict: inspected files; KEEP or named correction with exact affected section/replacement; disposition for all20 cases; whether corrected documents can be accepted under finite conditions without another generic review. Preserve source/card data and all existing original approvals. Do not silently promote pending spells,feats or classes. Actual human teaching/balance,remaining systems/final whole-game flow,GitHub push and post-push cosmology are separate. The original Player extract and canon registry are supplied as source evidence; defer cosmology/deep-setting/seasonal interpretation entirely.
''',encoding='utf-8')
 files.add(cases)
 manifest={rel(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files,key=rel)}
 readme='''# Exact teaching and charter review — complete files v2

Read docs/audit/2026-10-08/full-game/ONBOARDING_CHARTER_EXACT_REVIEW_SCOPE.md first, then all six named manuscripts and the original16-case file. Actual governing sources and complete selected Bard/ancestry/background/equipment/spell evidence are included. FIRST_BARD_WALKTHROUGH_PREPARATION.json records exact selected objects and worked checks. Use source-specific fields,not outside RPG assumptions.

All five onboarding manuscripts and their v1 governing dependencies remain byte-identical. Only START_HERE.md changed since v1,to record all687 recipe reviews. The added source-grounded charter and its actual doctrine/loop/introduction/foundation basis require their own teaching/synthesis verdict. Current recipe correction evidence is included for continuity and independent hash verification,not as a request to reopen the completed source conference. Preserved historical/pending labels in original evidence do not override current receipts.

FILE_MANIFEST.json supplies exact bytes/hashes for every payload. Existing source evidence remains historical and immutable. No source deletion,publication,GitHub push,cosmology interpretation or runtime/balance certification is requested.
'''
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.writestr('README_REVIEW.md',readme.encode());z.writestr('FILE_MANIFEST.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
  for p in sorted(files,key=rel):z.write(p,rel(p))
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None and len(z.namelist())==len(manifest)+2==len(set(z.namelist()))
  assert all(sha(G/n)==m['sha256']==hashlib.sha256(z.read(n)).hexdigest() for n,m in manifest.items())
 obj={'status':'PASS complete current file preparation; UNSENT','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'bundleFile':zpath.name,'bundleSha256':sha(zpath),'bundleBytes':zpath.stat().st_size,'payloadFiles':len(manifest),'manuscripts':prior['manuscripts']+[rel(A/'DESIGN_CHARTER_CANDIDATE.md')],'reviewCases':20,'sourceAndDraftHashes':{n:m['sha256'] for n,m in manifest.items()},'changedSinceV1':changes,'sent':False,'newOnboardingApprovals':0,'advancedRecipesReviewed':167,'aggregateReviewedRecipes':687,'publicReviewedRecipes':433,'runtimeImplemented':False,'humanBalanceVerified':False,'cosmologyReviewed':False}
 dump(out,obj);print(json.dumps({k:v for k,v in obj.items() if k!='sourceAndDraftHashes'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
