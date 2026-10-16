"""Keep the active AC6 review and complete DE4 preparation discoverable without adoption."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat();previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC5_ACCEPTED_AC6_SUBMITTED_03.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DE4_CURRENT_AUDIT_01.json';delta=A/'DE4_CURRENT_AUDIT_01_NAVIGATION_DELTA.json';keep=A/'navigation-before-de4-current-audit-01'
    assert not any(p.exists() for p in [checkpoint,delta,keep])
    audit=A/'DE4_CURRENT_SOURCE_INTERFACE_AUDIT_01.json';check=A/'DE4_CURRENT_SOURCE_INTERFACE_CHECK_01.json';amend=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json';amendcheck=A/'DE4_FATE_GUARD_AMENDMENT_CHECK_02.json'
    assert read(check)['failureCount']==read(amendcheck)['failureCount']==0
    live=A/'AC6_FULL_CURRENT_REVIEW_03_LIVE_AT_DE4_AUDIT.txt';assert 'button "Stop"' in live.read_text(encoding='utf8')
    start=G/'START_HERE.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';saved=[];raw={}
    for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        b=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);raw[p]=b;saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=raw[start].decode();assert text.count(previous.relative_to(G).as_posix())==1;text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
    marker='**Prepared disease-interface audit:**';assert text.count(marker)==1
    paragraph='**Next fifteen-spell group:** The [current Divination/Enchantment rank-four source audit](docs/audit/2026-10-08/full-game/DE4_CURRENT_SOURCE_INTERFACE_AUDIT_01.json) preserves all 15 drafts and 30 original examples, compares 44 current spell records and binds 61 source files including all 17 public class files. Sixteen current issues and 30 required worked examples cover rerolls, information protection, temporary ability scores, faction/alignment readings, mental control, damage and Null Veil. [352 preservation/reference checks](docs/audit/2026-10-08/full-game/DE4_CURRENT_SOURCE_INTERFACE_CHECK_01.json) passed. The [explicit Fate Reversal guard amendment draft](docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json) inventories reversible proposed changes across nine active files, preserving four historical source records; [its follow-up checks](docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_CHECK_02.json) passed. These preparations are unsent and unadopted. Complete the current procedures/examples and refresh any accepted AC6 dependencies before their joint review.\n\n'
    text=text.replace(marker,paragraph+marker,1);start.write_text(text,encoding='utf8',newline='\n')
    cov=json.loads(raw[ledger]);prior=deepcopy(cov)
    for ident in ['DD-11','DD-12']:
        row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row);row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [audit,check,amend,amendcheck])
        row.setdefault('currentEvidenceAddenda',[]).append({'id':'de4-current-audit-01','recordedAtUtc':now,'status':'Current15-spell source/interface audit and nine-file proposed reroll-guard amendment prepared. Actual AC6 review still live; no additional adoption.','de4Identities':15,'de4OriginalExamples':30,'currentComparisons':44,'sourceFiles':61,'currentIssues':16,'requiredNewExamples':30,'auditChecks':352,'guardBaseChecks':236,'guardFollowupChecks':25,'newRuleAdoptions':0})
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
    assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in prior['aspects'] if x['id'] not in ['DD-11','DD-12']]
    ledger.write_bytes(encoded(cov))
    code=raw[builder].decode();tail=' + read(A / "AC5_ACCEPTED_AC6_SUBMITTED_03_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "DE4_CURRENT_AUDIT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    rows=[('DE4 — current fifteen-spell source/interface audit',audit.name),('DE4 — exact source and current reference checks',check.name),('DE4 — proposed three-spell reroll guard across nine active files',amend.name),('DE4 — preserved Director feat sources and reversible amendment',amendcheck.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(row)+',\n' for row in rows),1)
    scope='451 reviewed /397 pending ordinary spells. AC5 is jointly accepted and integrated. Actual GPT Part4 is still reviewing the full14-identity AC6 packet103 sources51 current cases. The next15 DE4 source/interface audit is prepared with61 sources44 comparisons16 issues30 new case requirements; explicit nine-file Fate Reversal guard amendment remains unsent/unadopted. Full75-area development and final whole-game flow remain open.'
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':0,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress: actual AC5 exact acceptance/applied16 spells and submitted full AC6 review',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Current DE4 source audit and explicit reroll-guard amendment drafted only. Existing451 reviewed membership unchanged.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(lastSuccessfulObservation=info(live),generationConfirmedLiveAtObservation=True,status='Same AC6 submission still visibly active: Stop control and live analysis with system thinking notice. No terminal return yet. Do not resend/restart solely for an unchanged observation or timeout.')
    state['de4CurrentPreparation']={'audit':info(audit),'auditCheck':info(check),'sourceManifest':info(A/'de4-current-source-interface-01/SOURCE_MANIFEST.json'),'identities':15,'originalExamples':30,'currentCounterparts':44,'sourceFiles':61,'issues':16,'futureExamples':30,'guardAmendment':info(amend),'guardCheck':info(amendcheck),'guardPreviousDraft':info(A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_01.json'),'status':'Unsent/unadopted. Complete current15 procedures and30 required finite examples; refresh AC6 after actual acceptance. Guard proposal still requires final current design-note/metadata integration and actual joint approval.'}
    state['safeNextActions'].insert(3,'DE4 preparation is ready for current procedure work:15 original full drafts/30 historical texts,61 sources44 current comparisons16 issues30 explicit new case requirements. Nine-file Fate Reversal guard amendment02 preserves4 historical records and inventories202 catalog bindings. Do not apply before actual joint review. Refresh accepted AC6 dependencies before submitting.')
    state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Prepared current DE4 source/interface audit and concrete reversible nine-file reroll-guard proposal while actual AC6 GPT generation remains live.','evidence':info(audit),'activeReviewObservation':info(live)}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(checkpoint),'links':build['existingDistinctLinks'],'missingLinks':0,'newSpellAdoptions':0,'currentOrdinarySpells':state['currentOrdinarySpellCounts'],'activeReviewUserTurn':state['activeGptReview']['userTurnId']}))

if __name__=='__main__':main()
