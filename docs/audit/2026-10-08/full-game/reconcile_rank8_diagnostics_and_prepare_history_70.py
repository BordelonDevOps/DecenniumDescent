"""Preserve an over-strict diagnostic, reconcile its scope, prepare one real question."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';P=A/'rank8-damage6-part5-correction-return-02'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 original=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_REVIEW_70.json';out=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_70.json'
 root=A/'rank8-damage6-cast-history-correction-02';archive=A/'DD_Rank8_Damage6_Cast_History_Correction_02.zip';prep=A/'RANK8_DAMAGE6_CAST_HISTORY_CORRECTION_02_PREPARATION.json';request=A/'GPT_PART5_RANK8_CAST_HISTORY_CORRECTION_13_REQUEST.txt';saved=A/Path(__file__).name
 assert not any(p.exists() for p in [out,root,archive,prep,request,saved])
 report=read(original);oldbytes=original.read_bytes();questions=read(P/'QUESTION_DISPOSITIONS.json');model=read(P/'MODEL.json')
 removed=[x for x in report['diagnosticChecks'] if x['check']=='New Pyre paragraph retained in QUESTION_DISPOSITIONS.json'];assert len(removed)==1 and removed[0]['passed'] is False
 report['originalUnmodifiedDiagnosticReport']=info(original)
 report['diagnosticScopeCorrection']={'preservedRejectedAssertion':removed[0],'reason':'The question disposition is a concise answer plus explicit local rule reference, not a full procedure rendering. Requiring the entire word-identical paragraph here was over-strict. Both actual answers contain the new scoped completion without contradiction, and both are exact full mirrors of MODEL. This is a local diagnostic correction, not a returned artifact defect. The original report/script remain unchanged.'}
 report['diagnosticChecks']=[x for x in report['diagnosticChecks'] if x not in removed]
 for i,phrases in [(7,['CON DC16 immediately','ends a failed hold immediately','before its creation still prevents the blast','no second cleanup ending']),(8,['held-concentration save','later recipient on failure','not an all-instantaneous-spells rule'])]:
  q=questions[i];ok=q==model['reviewQuestionDispositions02'][i] and 'RD8-PYRE-READY-BATCH-03' in q['localRuleIds'] and all(p in q['answer'] for p in phrases)
  assert ok,q['id'];report['diagnosticChecks'].append({'check':q['id']+' scoped linked answer and complete MODEL mirror','actual':ok,'expected':True,'passed':ok})
 report.update(id='RANK8-CORRECTION02-SEMANTIC-RECONCILIATION-70',recordedAtUtc=datetime.now(timezone.utc).isoformat(),diagnosticCheckCount=len(report['diagnosticChecks']),diagnosticFailures=sum(not x['passed'] for x in report['diagnosticChecks']))
 assert report['diagnosticCheckCount']==334 and report['diagnosticFailures']==1
 out.write_bytes(enc(report))
 text='''DECENNIUM DESCENT — RANK8 DAMAGE6 CAST-HISTORY QUALIFICATION CONFERENCE 13

PREPARED UNSENT. Submit only after the active Rank7 correction12 finishes; do not interrupt it. This note describes preparation history, not an actual submitted message.

The full Rank8 correction Return02 is attached unchanged under input/. Its archive is 17,408,791 bytes, SHA256 6678b1cbe5d02104b38b2cdb4eee4b1eec434dc7a05e60889ed7153ef2f730cb; MODEL is 1,753,895 bytes, SHA256 d58674925ea0711de915b713099c0cec55d687f7ceab86e41047563e4c0e9514. Read those actual bytes and the complete independent semantic reports, not a reconstructed summary. Local preservation passed1,060 checks.

The eight original findings are now independently reconciled at the supplied inputs: actual Ready concentration and the narrowly scoped created Pyre blast, complete screen geometry, both Greater Dispel captures, carrying/anchor/save state, forms and stage gates, legal movement, strain17 and actual Wall establishment. Preserve these corrections. Five procedures and all six shared clauses are exact; only the earlier agreed Pyre paragraph changed. The new local review has334 applicable diagnostics,333 passing and one remaining history qualification. One over-strict literal-paragraph check was explicitly withdrawn because Q08/Q09 correctly summarize/reference the complete procedure; original reports and that diagnostic are preserved, and both full answer mirrors were verified. That is not a GPT artifact defect.

ONE ADDITIONAL QUESTION — RD8-LOCAL70-01:
RD8-05-B /currentVectors/9/actorSheets/anchorCaster is a complete Wizard7 sheet. Its initialSetup states that at-1 it paid7RP for actual Dimensional Anchor,24→17, first prepared familyD0, with live concentration deadline59; previousSpell is Dimensional Anchor. Yet matrixFamiliesUsed is []. All eight independent branches reproduce this full supporting actor, for nine occurrences.

The actual Wizard PROTECTED DISSONANCE INTERFACE consumes the first-family exemption within an encounter; duplicate preparation cannot refresh it. Please bind whether the disclosed cast at-1 belongs to the current encounter. If so, record the actual dimensional-anchor family in all nine full sheets and affected mirrors. If the intended fixture contains an intervening legitimate encounter boundary, expressly identify it and its source authority while preserving the still-live spell lifetime and other history. Merely crossing a chosen time0 is not evidence of an encounter reset. Recommend the straightforward same-encounter spent-family record, avoiding an unneeded reset. Do not invent a new global encounter policy or a second first-cast exemption.

This omission predates Return02; it was newly noticed while checking the corrected complete Anchor metadata. It is not evidence that all eight prior corrections failed. Existing damage, RP and exile outcomes can remain exact. Supply one meaningful later same-family diagnostic proving correct nonrenewal (or source-qualified reset), without granting an Action or source not present. Keep any new case independent from the original main/branches.

Return full exact affected successor artifacts and complete source-linked disposition, with reversible full before/after operations from this exact Return02 MODEL and complete binding hashes. Preserve all prior history/receipts; alternatives must be clearly labeled and not cumulative. Reconcile every affected full mirror; do not fix only the narration or test expectation. If you disagree, explain the exact supplied encounter boundary and source instead of silently changing an input.

No new spell rule, generic Ready change, free Action, arbitrary encounter reset, implementation, balance or cosmology adoption is authorized. All six identities remain pending local cohort acceptance until this qualification is resolved. Applied525 reviewed/323 pending/249 standalone/173 interfaces and39 accepted-but-unapplied stay unchanged. The owner reserves implementation separately. Five external content/contest holds remain. Do not start a new cohort in this response.
'''
 request.write_text(text,encoding='utf-8');root.mkdir()
 files={'REQUEST.txt':request,'LOCAL_SEMANTIC_RECONCILIATION.json':out,'ORIGINAL_LOCAL_DIAGNOSTIC_REPORT.json':original,'LOCAL_DIAGNOSTICS.py':A/'audit_rank8_damage_corrections_02.py','PRESERVATION_RECEIPT.json':A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json','input/DD_Rank8_Damage_6_Part5_Correction_Return_02.zip':A/'DD_Rank8_Damage_6_Part5_Correction_Return_02.zip','sources/wizard.json':R/'data/public/class_playtests/wizard.json','sources/CLASS_PLAYTEST_RULES.md':R/'docs/mechanics/CLASS_PLAYTEST_RULES.md','sources/accepted_interface_registry_06.json':R/'data/director/spell_review/accepted_interface_registry_06.json'}
 manifest=[]
 for rel,source in files.items():
  target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes());b=info(target);manifest.append({'path':rel,'bytes':b['bytes'],'sha256':b['sha256'],'source':info(source)})
 (root/'MANIFEST.json').write_bytes(enc({'id':'RANK8-CAST-HISTORY-CORRECTION02-MANIFEST','status':'PREPARED_UNSENT','files':manifest}))
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for file in sorted(root.rglob('*')):
   if file.is_file():z.write(file,file.relative_to(root).as_posix())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==10
  for row in manifest:assert z.read(row['path'])==(root/row['path']).read_bytes()
 assert original.read_bytes()==oldbytes
 prep.write_bytes(enc({'id':'RANK8-CAST-HISTORY-CORRECTION02-PREPARATION','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','request':info(request),'archive':info(archive),'manifest':info(root/'MANIFEST.json'),'semanticReview':info(out),'questionCount':1,'findingId':'RD8-LOCAL70-01','sourceFiles':3,'fullOriginalReturnIncluded':True,'newAcceptedIdentities':0,'canonicalChanges':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'nextAction':'After completed Rank7 correction12, submit this full question and archive, then independently review actual reply.'}))
 saved.write_bytes(Path(__file__).read_bytes());print(json.dumps({'review':info(out),'archive':info(archive),'preparation':info(prep),'applicableDiagnostics':334,'failures':1,'questionCount':1,'sent':False}))
if __name__=='__main__':main()
