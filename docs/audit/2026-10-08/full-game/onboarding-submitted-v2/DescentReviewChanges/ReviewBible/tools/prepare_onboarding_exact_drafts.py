"""Freeze complete current onboarding manuscripts and actual governing sources."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def main():
    archive=A/'DD_Onboarding_Exact_Drafts_Prepared_v1.zip';out=A/'ONBOARDING_EXACT_DRAFTS_PREPARATION.json'
    assert not archive.exists() and not out.exists(),'Preserve frozen handoff; use a new revision'
    evidence=read(A/'FIRST_BARD_WALKTHROUGH_PREPARATION.json')
    assert all(sha(G/p)==h for p,h in evidence['sourceHashes'].items())
    assert sha(G/evidence['manuscript'])==evidence['manuscriptSha256']
    manuscripts=[R/'docs/playtest'/n for n in ['SESSION_ZERO_PLAYTEST.md','NEWCOMER_PLAYER_GUIDE.md','NEWCOMER_DIRECTOR_GUIDE.md','RESONANCE_CHEATSHEET.md','FIRST_BARD_WALKTHROUGH.md']]
    files=set(manuscripts)|{G/p for p in evidence['sourceHashes']}
    files.update([G/'START_HERE.md',A/'FIRST_BARD_WALKTHROUGH_PREPARATION.json',A/'SESSION_ZERO_DRAFT_PREPARATION.json',A/'ONBOARDING_RULE_SUMMARY_RECONCILIATION.json',A/'ONBOARDING_EXACT_REVIEW_CASES.md',Path(__file__).resolve()])
    files.update(R/'docs/mechanics'/n for n in ['CONDITIONS_PLAYTEST.md','MAXIMUM_HP_PLAYTEST.md','CLASS_PLAYTEST_SESSION_LOG.md','BASE_CLASSES_START_HERE.md','CLASS_PLAYTEST_INDEX.md','ANCESTRY_BACKGROUND_REVIEW_STATUS.json','classes/oracle.md'])
    assert all(f.is_file() for f in files),[str(f) for f in files if not f.is_file()]
    readme='''# Complete onboarding manuscripts — prepared, unsent

The five actual player/Director manuscripts are under DescentReviewChanges/ReviewBible/docs/playtest/. Begin with FIRST_BARD_WALKTHROUGH.md, then SESSION_ZERO_PLAYTEST.md, NEWCOMER_PLAYER_GUIDE.md, NEWCOMER_DIRECTOR_GUIDE.md and RESONANCE_CHEATSHEET.md. START_HERE.md supplies the user reading path. The16 finite questions in docs/audit/2026-10-08/full-game/ONBOARDING_EXACT_REVIEW_CASES.md define the requested exact manuscript review.

Actual governing character, ancestry/background, equipment, Bard, Oracle, spell, Core, condition, timing, carrying, maximum-HP, rest and recovery sources are included. The full ordinary spell catalog and complete50 Bard cards preserve each selected original and operational record. FIRST_BARD_WALKTHROUGH_PREPARATION.json contains the complete selected source records, inventory, exact source hashes, numerical spot checks through existing calculators, and all seven resolved local walkthrough links. SESSION_ZERO_DRAFT_PREPARATION.json and ONBOARDING_RULE_SUMMARY_RECONCILIATION.json explain those drafts' scope. Those are preparation/evidence receipts, not review approvals.

All5 manuscripts require semantic teaching-flow review. No new unit-test suite or campaign/runtime simulation is claimed for these documentation changes. The body/inventory example's actual packing volume, campaign-specific social groups and declared synthetic enemy/ally premises remain expressly identified. No new lore or cosmology is inferred. Original sources and old onboarding revisions remain preserved in the repository.

This archive is frozen preparation, not a sent request. Check intervening source changes before dispatch. Do not interrupt the active advanced-crafting exact review. Its eventual result does not automatically approve these teaching manuscripts; their own narrow verdict remains needed. No new rules, class/card promotion, source deletion, GitHub push or cosmology review occurs here.
'''
    manifest={rel(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files,key=rel)}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README_ONBOARDING_REVIEW.md',readme.encode());z.writestr('FILE_MANIFEST.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
        for p in sorted(files,key=rel):z.write(p,rel(p))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(manifest)+2==len(set(z.namelist()))
        assert all(hashlib.sha256(z.read(p)).hexdigest()==v['sha256'] for p,v in manifest.items())
    obj={'status':'PASS complete-file preparation; UNSENT; exact manuscript review pending','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'manuscripts':[rel(p) for p in manuscripts],'reviewCases':16,'bundleFile':archive.name,'bundleSha256':sha(archive),'bundleBytes':archive.stat().st_size,'payloadFiles':len(manifest),'sourceAndDraftHashes':{p:v['sha256'] for p,v in manifest.items()},'sent':False,'newApprovals':0,'runtimeImplemented':False,'humanBalanceVerified':False,'cosmologyReviewed':False,'nextAction':'After the current advanced-crafting review completes, refresh any changed dependencies and submit the five actual manuscripts for their bounded exact teaching-flow review.'}
    out.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in obj.items() if k!='sourceAndDraftHashes'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
