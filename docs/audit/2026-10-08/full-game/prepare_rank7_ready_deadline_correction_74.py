"""Complete bounded follow-up with preserved return, sources and local evidence; unsent."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
W=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\audit_work')
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
root=A/'rank7-identity-casting5-ready-deadline-correction-02'
archive=A/'DD_Rank7_Identity_Casting5_Ready_Deadline_Correction_02.zip'
prep=A/'RANK7_IDENTITY_CASTING5_READY_DEADLINE_CORRECTION_02_PREPARATION.json'
requestpath=A/'GPT_PART5_RANK7_READY_DEADLINE_CORRECTION_14_REQUEST.txt'
scripts=['audit_rank7_identity_corrections_02_74.py','reconcile_rank7_cadence_diagnostics_74.py',Path(__file__).name]
assert not any(p.exists() for p in [root,archive,prep,requestpath]+[A/n for n in scripts])
reportpath=A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_74.json'
report=json.loads(reportpath.read_bytes());original=A/'DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip'
assert info(original)['sha256']=='d063125b1b570230afa9cef56714efc26d011dd9ca0dd56c064d5473c85b63a1'
assert report['diagnosticCheckCount']==554 and report['diagnosticFailures']==report['findingsCount']==1
request='''DECENNIUM DESCENT — RANK7 IDENTITY/CASTING5 READY DEADLINE CORRECTION CONFERENCE14

PREPARED LOCALLY, NOT SENT. Submit only after the currently active separate Rank8 cast-history response finishes. This packet is neither an actual dispatch nor acceptance/implementation.

All three original Rank7 correction groups have now been independently reconciled: legal Adept acquisition replacing the level12 CHA increase, eight real Action debits and complete propagation, and successful Erase casting/family history with the later17RP, D2+Refrain1 continuation. The full Return02 archive passed1057 independent preservation/source/mirror/reversible reconstruction checks. Current semantic reconciliation has554 applicable diagnostics,553 passes and ONE bounded remaining state correction. All121 events and44 ordinary Action commitments were independently classified. Nine initially overstrict local START-sequence diagnostics were withdrawn with precise evidence, not treated as GPT defects. Both reports are preserved in this packet.

Please read this complete request, LOCAL_SEMANTIC_RECONCILIATION.json and the complete unchanged input/DD_Rank7_Identity_Casting_5_Part5_Correction_Return_02.zip. The archive is64,667,556 bytes, SHA256 d063125b1b570230afa9cef56714efc26d011dd9ca0dd56c064d5473c85b63a1. Its full MODEL is12,000,315 bytes, SHA256 fbdfd5c299d7a501d53eedad03df82211da312df783b06d68e1dae3de5fd0a36. Every previous source, full original history, corrected case, procedure and shared decision is present. Do not reconstruct from chat summaries or run supplied local diagnostics as authority. Identify any exact missing file.

RIC5-LOCAL74-01: RIC5-02-A-a correctly changed the fixture to actual Mage START55/nextSTART61, preparation56.1, Meta Surge expiry60.5 and release60.9. However sourceLedger.hold.deadline still equals62 in SIX current complete states: timeline0 after; timeline1 before and after; timeline2 before and after; expectedFinalState. Their MODEL prefix is /currentVectors/2/independentBranches/0. The full same case also appears in CASE_DISPOSITIONS/cases and evidence/worked_cases. COMBAT_ACTION_PLAYTEST.md:99 says generic Ready expires at the next regular own-turn start. The actual state deadline is therefore61.

Correct this remaining current deadline field and every affected complete mirror to61. The amended60.9 release remains legal; do not move it again or extend Ready. Preserve its spent Action, one actual Reaction,38RP/D0/zero class uses and six damage/target74HP. Preserve all three original correction groups, the two other additional cadence repairs, all five spell procedures, five shared rules,24 decisions and11 original conditional branch qualifications. Historical input/baseline files must retain their original62 bytes and be explicitly historical. Do not promote the candidate or change canonical files.

Provide a separate meaningful boundary diagnostic with the actual55/61 cadence: release60.9 is before expiry; a hypothetical trigger at61 or61.1 cannot release the hold. The stale time<62 field would otherwise give the wrong boundary predicate. This is a data-authoring inconsistency and a diagnostic of the stored value; neither side has run a production Ready scheduler. Retain consumption/cleanup exactly once; do not add a free Action, cast-history update, extra metamagic payment, new clock or global rule.

Return the complete corrected successor MODEL, all full case/evidence/chapter mirrors, source-linked finding disposition, exact complete before/after objects and reversible operations from the exact bound Return02 MODEL. Keep complete baseline and historical input bytes. If providing an alternative original-source reconstruction path, identify it as an ALTERNATIVE, never cumulative. Preserve the original eleven-plus27 operation history and all previous reports. Reconcile current documentary/specification mirrors without rewriting historical artifacts. Use full state objects, not summary-only replacement snippets. Document any additional real contradiction separately with its exact source and pointer.

This is a bounded fixture correction. Applied525 reviewed/323 pending/249 standalone/173 interfaces and39 accepted-but-unapplied remain unchanged. Rank7 and Rank8 each await their own independent acceptance. Owner implementation reservation remains in force. No canonical catalog/index/registry/helper/runtime changes, cosmology, balance approval, whole-game closure or release approval. Do not start another cohort in this response.
'''
request+='\nEXACT DEADLINE LOCATIONS:\n'+json.dumps(report['findings'][0]['evidence']['locations'],indent=2)+'\n'
members={'REQUEST.txt':request.encode(),'LOCAL_SEMANTIC_RECONCILIATION.json':reportpath.read_bytes(),
 'ORIGINAL_LOCAL_DIAGNOSTIC_REPORT.json':(A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_SEMANTIC_REVIEW_74.json').read_bytes(),
 'PRIOR_PRESERVATION_RECEIPT.json':(A/'RANK7_IDENTITY_CASTING5_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json').read_bytes(),
 'input/'+original.name:original.read_bytes()}
for name in scripts[:2]:members['local-diagnostics/'+name]=(W/name).read_bytes()
for binding in report['sourceBindings']:
 p=G/binding['path'];assert info(p)==binding;members['sources/'+binding['path']]=p.read_bytes()
manifest={'status':'PREPARED_NOT_SENT_NOT_ACCEPTED_NOT_APPLIED','files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(members.items())]}
members['MANIFEST.json']=enc(manifest)
root.mkdir()
for n,b in members.items():
 p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(members.items()):z.writestr(n,b)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None and set(z.namelist())==set(members)
 for n,b in members.items():assert z.read(n)==b
requestpath.write_bytes(members['REQUEST.txt'])
for n in scripts:(A/n).write_bytes((W/n).read_bytes())
result={'id':'RANK7-IDENTITY-CASTING5-READY-DEADLINE-CORRECTION-02-PREPARATION','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_NOT_SENT',
 'archive':info(archive),'request':info(requestpath),'semanticReview':info(reportpath),'originalReturn':info(original),'manifest':info(root/'MANIFEST.json'),
 'manifestFiles':len(members)-1,'allArchiveBytesReopenedAndCompared':True,'findings':1,'diagnosticChecks':554,'diagnosticFailures':1,'sent':False,'implementationApplied':False,'newAcceptedIdentities':0,'sourceInformationDeleted':0}
prep.write_bytes(enc(result));print(json.dumps({'preparation':info(prep),'archive':info(archive),'files':len(members),'sent':False}))
