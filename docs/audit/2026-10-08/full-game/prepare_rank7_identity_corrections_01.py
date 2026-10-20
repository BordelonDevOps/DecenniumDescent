"""Preserve a complete bounded correction packet without dispatch or adoption."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 root=A/'rank7-identity-casting5-local-corrections-01';archive=A/'DD_Rank7_Identity_Casting5_Local_Corrections_01.zip'
 prep=A/'RANK7_IDENTITY_CASTING5_LOCAL_CORRECTIONS_01_PREPARATION.json'
 req=A/'GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_REQUEST.txt'
 audit=A/'audit_rank7_identity_semantics_01.py';script=A/Path(__file__).name
 assert not any(p.exists() for p in [root,archive,prep,req,audit,script])
 reportpath=A/'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json';report=json.loads(reportpath.read_bytes())
 original=A/'DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip'
 assert info(original)['sha256']=='cdc2b871521cdb2c33bb2b23932d5fcb25dcb486e794e826c637d48d10beb5b7'
 assert report['diagnosticCheckCount']==314 and report['diagnosticFailures']==11 and report['findingsCount']==3
 request='''DE CENNIUM DESCENT — RANK7 IDENTITY/CASTING5 BOUNDED CORRECTION CONFERENCE 12

Prepared locally; NOT DISPATCHED. Submit after the active Rank8 correction response finishes. This preparation status must not be confused with an actual GPT submission.

Please read the complete original returned archive under input/ and this entire request. The original return is preserved byte-for-byte as input/DD_Rank7_Identity_Casting_5_Part5_Conference_Return_01.zip, 14,578,890 bytes, SHA256 cdc2b871521cdb2c33bb2b23932d5fcb25dcb486e794e826c637d48d10beb5b7. Its full MODEL is 11,968,546 bytes, SHA256 2cd09a244b6f49a6aa1240ed295470bcbdaff8df038bb51092756849a47ef2f5. It contains all complete sources, later contexts, five procedures, 24 decisions, 10 main examples and39 independent branches. Do not reconstruct from chat summaries or execute supplied local code as authority. If a necessary file cannot be accessed, name the exact missing file.

Independent source/manifest/reversible reconstruction previously passed577 checks. The new local semantic review performed314 fixture/source/arithmetic/state diagnostics:303 passed and11 failed. These11 failures fall into THREE corrections below. They are authored-example diagnostics, not engine tests. No spell in this group is locally accepted or implemented yet. All five remain tier C.

1. METAMAGIC ADEPT ACQUISITION: RIC5-02-B-a claims an actually acquired Adept Sculpt mode, conditional on operational feat availability. Its complete Wizard13 actor spends class4 on INT+2, class8 on STR+2, class12 on CHA+2 and expressly says no extra feat. CHARACTER_CREATION_PLAYTEST.md:45 requires an ASI OR an eligible feat at4/8/12/16/19; none remains available at13. Conditional availability does not supply an additional milestone. Bind actual chosen feat modes, acquisition milestone and source in a coherent actor. Reconcile generated scores and downstream stats if replacing an ASI. No free invented feat. The negative RIC5-02-B-b branch also says genuine both-provider acquisition despite inheriting a full all-ASI history; either bind lawful ownership or retain an explicit conditional provider predicate without pretending the actor has a complete legal acquisition. The Meta Surge waiver selection itself is not reopened.

2. ACTION LEDGERS: Eight successful Action events retain action=true after their event. They explicitly define that boolean as the REMAINING underlying ledger, and regular START is materialized BEFORE the event. Correct the debit and every subsequent state until the next actual refresh. Exact events (zero-based): RIC5-01-B timeline3 enemy Fireball; RIC5-02-A timeline2 Mage repeated Ray; RIC5-04-A timeline3 enemy Ray; RIC5-04-B timeline3 carrier putting down the body; RIC5-05-B timeline5 creator dismissal and timeline7 creator new Simulacrum; RIC5-02-B-a timeline1 Wizard Fireball; RIC5-04-B-b timeline0 caster Lesser Antimagic. All eight currently have true both before and after. Audit the cadence-normalization logic and all main/branch mirrors for the same bug. Legal rejected declarations remain unspent; composite Cast Echo children and Reaction-only release do not acquire extra Action costs. The new local diagnostics intentionally expose these eight states rather than merely repeat the narrative.

3. SUCCESSFUL ERASE CAST HISTORY: RIC5-03-B-a pays17RP and spends the Action, and the valid subject receives Erase protection. The wall excludes only one observer. Nevertheless caster.lastSpell stays null and preparedFamiliesUsed stays empty in the completed event and final state. Record the actual Erase commitment and used first-prepared family. Keep zero base Dissonance for this genuine first prepared cast, actual observer exclusion, and subject protection. This is not an illegal/refunded casting attempt.

The exact case pointers, complete evidence, class sources and all diagnostic outcomes are in LOCAL_SEMANTIC_REVIEW.json. The independently written diagnostic script is included for transparency; it is not a production engine. Full current class, advancement, resolution, body and registry sources are separately supplied under sources/ with hashes in MANIFEST.json. Original history is preserved inside the unchanged return archive.

Return complete corrected MODEL, case dispositions, actor accounting, procedures, player/Director chapters, specifications, source/reference bindings and all affected mirrors. Include findings dispositions with exact source explanations for any disagreement. Do not fix just a narrative summary or change only the local test expectations. Show meaningful failing-then-corrected finite state evidence for acquisition, regular-START refresh followed by Action debit, and Erase's next repeated cast respecting its spent history.

Supply complete before/after operations beginning at the exact returned MODEL above, complete baseline/successor bytes, hashes, and forward/reverse reconstruction evidence. If you also retain an alternative original source-candidate path, clearly identify its exact baseline and its prerequisite operations. Alternatives must not be applied cumulatively. Preserve all original bytes and reports. Reconcile every affected full mirror; do not erase an unchanged historical example just because its successor is corrected.

Retain all11 genuine conditional branch qualifications and the five independent Companion/Control content/contest holds. No new global rule, simplified tabletop substitute, class grant, generic free Action, generic copy restriction or cosmology is authorized by these fixture corrections. Cast Echo's native interrupt and long-cast completions, Meta Surge's explicitly selected provider waiver, Erase's bounded mask, Sequester's clocks, and Simulacrum's finite resource/lifecycle procedures remain scoped proposed authorship. Any newly discovered contradiction should be stated separately with exact evidence.

Applied525 reviewed /323 pending /249 standalone /173 interfaces and39 accepted-but-unapplied remain unchanged. The owner reserves the separate implementation instruction. No canonical index/catalog/registry/helper edits, runtime implementation, balance approval, cosmology adoption, whole-game completion or release approval is implied. Rank8 corrections remain a separate conference and must be completed before this one is submitted.
'''.replace('DE CENNIUM','DECENNIUM')
 request+='\nFULL LOCAL FINDINGS (verbatim structured evidence):\n'+json.dumps(report['findings'],ensure_ascii=False,indent=2)+'\n'
 members={'REQUEST.txt':request.encode('utf-8'),'LOCAL_SEMANTIC_REVIEW.json':reportpath.read_bytes(),
   'LOCAL_DIAGNOSTICS.py':(W/'audit_rank7_identity_semantics_01.py').read_bytes(),
   'input/'+original.name:original.read_bytes(),
   'PRIOR_PRESERVATION_RECEIPT.json':(A/'RANK7_IDENTITY_CASTING5_PART5_RETURN_01_LOCAL_PREFLIGHT.json').read_bytes()}
 for binding in report['sourceBindings']:
  path=G/binding['path'];assert info(path)==binding;members['sources/'+binding['path']]=path.read_bytes()
 manifest={'status':'PREPARED_NOT_SENT_NOT_ACCEPTED_NOT_APPLIED','files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(members.items())]}
 members['MANIFEST.json']=enc(manifest)
 root.mkdir()
 for n,b in members.items():
  path=root/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in sorted(members.items()):z.writestr(n,b)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  assert set(z.namelist())==set(members)
  for n,b in members.items():assert z.read(n)==b
 req.write_bytes(members['REQUEST.txt']);audit.write_bytes(members['LOCAL_DIAGNOSTICS.py']);script.write_bytes(Path(__file__).read_bytes())
 result={'id':'RANK7-IDENTITY-CASTING5-LOCAL-CORRECTIONS-01-PREPARATION','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'status':'PREPARED_NOT_SENT','archive':info(archive),'request':info(req),'semanticReview':info(reportpath),
  'originalReturn':info(original),'manifest':info(root/'MANIFEST.json'),'manifestFiles':len(members)-1,
  'allArchiveBytesReopenedAndCompared':True,'findings':3,'diagnosticChecks':314,'diagnosticFailures':11,
  'sent':False,'implementationApplied':False,'newAcceptedIdentities':0,'sourceInformationDeleted':0}
 prep.write_bytes(enc(result));print(json.dumps({'preparation':info(prep),'archive':info(archive),'files':len(members),'sent':False}))
if __name__=='__main__':main()
