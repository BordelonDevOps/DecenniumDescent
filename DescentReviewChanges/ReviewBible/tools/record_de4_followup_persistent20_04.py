"""Record the actual pending conference and new independent evidence without adoption."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    cp = A/'ACTIVE_AUTHORING_CHECKPOINT_DE4_FOLLOWUP_PERSISTENT20_04.json'
    delta = A/'DE4_FOLLOWUP_PERSISTENT20_04_NAVIGATION_DELTA.json'
    report = A/'DE4_FOLLOWUP_PERSISTENT20_04_NAVIGATION_CHECK.json'
    keep = A/'navigation-before-de4-followup-persistent20-04'
    assert not any(p.exists() for p in [cp, delta, report, keep])
    now = datetime.now(timezone.utc).isoformat()
    prev = A/'ACTIVE_AUTHORING_CHECKPOINT_NEXT25_READY_PERSISTENT20_03.json'
    oldcp = read(prev)
    start = G/'START_HERE.md'; guide = R/'docs/DEVELOPMENT_DIRECTION.md'
    builder = R/'tools/build_review_map.py'; ledger = R/'data/playtest/game_development_coverage.json'
    mapfile = G/'REVIEW_MAP.html'; buildfile = A/'REVIEW_MAP_BUILD.json'
    raw = {p:p.read_bytes() for p in [start, guide, builder, ledger, mapfile, buildfile]}
    saved = []
    for p,b in raw.items():
        q = keep/p.relative_to(G); q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(b)
        saved.append({'source':info(p), 'preservedCopy':info(q)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    submitted = read(A/'DE4_REVIEW_FOLLOWUP_06_SUBMITTED_NATIVE.json')
    payload = json.loads(next(x['text'] for x in submitted['content'] if x['type']=='text'))
    turn = next(x for x in payload['turns'] if x['id']=='c4aa146a-0678-4bf1-ba82-e00c3b1a3d09')
    assert any('DD_DE4_Review_Followup_06.zip' in str(x) for x in turn['items'])
    text = raw[start].decode('utf8').replace(prev.relative_to(G).as_posix(), cp.relative_to(G).as_posix())
    changes = {
      '**Current GPT conference:**': '**Current GPT conference:** The [recovered final DE4 Conference05 review](docs/audit/2026-10-08/full-game/DE4_DIGITAL_CONFERENCE_05_FINAL_RECEIPT.json) is preserved and verified, including its complete report and corrections. It required four focused corrections before final exact review. GPT now has the [Current06 follow-up](docs/audit/2026-10-08/full-game/DE4_REVIEW_FOLLOWUP_06_PREPARATION.json), with [actual submission evidence](docs/audit/2026-10-08/full-game/DE4_REVIEW_FOLLOWUP_06_SUBMITTED_NATIVE.json). All 19 proposed operations, 37 current cases, 30 original texts and 88 source bindings are preserved. The remaining narrow decisions concern source-specific RNG disclosure, empty Burning Hands cones, private Confusion draws and accurate historical attribution. The nine proposed Fate representations still require final metadata rebinding and exact acceptance; no live rules or counts changed. Continue the active Review Continuation Part 4 review without duplicating the upload.',
      '**Preserved fifteen-spell proposal:**': '**Preserved fifteen-spell proposal:** [DE4 Current06](DescentReviewChanges/ReviewBible/data/director/spell_proposals/divination_enchantment_rank4_current_06.json) and [Fate amendment04](docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_DRAFT_04.json) incorporate the final review as pending authorship. The [390-check preflight](docs/audit/2026-10-08/full-game/DE4_REVIEW_REVISION_CHECK_06.json) confirms preservation and exact correction bindings. Current05, amendment03, the interim evidence and recovered final report remain separate historical records. New N35–N37 cases cover compelled attacks under Mass Pacify, Stable/death-save/summon-expiry ordering and hidden-occupancy-safe damage-pool generation.',
    }
    for marker, replacement in changes.items():
        begin=text.index(marker); end=text.index('\n\n',begin); text=text[:begin]+replacement+text[end:]
    marker='**Prepared disease-interface audit:**'; pos=text.index(marker)
    added='**Persistent spell development:** The source audit preserves all 20 earlier procedures and 40 original cases. [Interface findings](DescentReviewChanges/ReviewBible/data/director/spell_review/persistent_damage_20_interface_findings_02.json) identify actual ongoing-fire/cure conflicts and provide the real Mage Undying Spellform case. [Transfer vectors](DescentReviewChanges/ReviewBible/data/director/spell_review/persistent_damage_20_transfer_vectors_03.json) use actual Burden Shared and Life Linked rules; [damage-root options](DescentReviewChanges/ReviewBible/data/director/spell_review/persistent_damage_20_root_proposal_04.json) remain explicit new source-specific proposals. These evidence files are in the current GPT handoff for awareness, not approval. The [remaining authorship map](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_spell_authoring_map_03.json) separates the active 15, next 25, persistent 20 and preserved later work so complete earlier proposals are reused.\n\n'
    text=text[:pos]+added+text[pos:]; start.write_text(text,encoding='utf8',newline='\n')
    gt=raw[guide].decode('utf8').replace(prev.name,cp.name)
    oldline=next(x for x in gt.splitlines() if x.startswith('- DE4 Current05'))
    gt=gt.replace(oldline,'- The recovered final DE4 Conference05 review is preserved. Current06/Fate04 incorporate its 19 operations and add three cases, giving 37 current cases, 30 original texts and 88 sources. The actual GPT follow-up is active. Its narrow unresolved changes remain pending; nine proposed representations still need final metadata rebinding and exact acceptance. No live rule changed.')
    gt=gt.replace('Latest observed weekly allowance was94% remaining','Latest observed weekly allowance was90% remaining')
    gt=gt.replace('- Continue the full75-domain objective','- Persistent20 findings02, transfer vectors03 and root options04 are provided to GPT for awareness only. All 20 earlier procedures and 40 original cases remain preserved. Real ongoing-fire, Undying Spellform and no-recovery transfer rules control the proposed compositions; no general root or information rule is silently expanded.\n- Continue the full75-domain objective')
    guide.write_text(gt,encoding='utf8',newline='\n')
    cov=read(ledger); before=deepcopy(cov)
    evidence=[A/'DE4_REVIEW_REVISION_CHECK_06.json',A/'DE4_DIGITAL_CONFERENCE_05_FINAL_RECEIPT.json',A/'DE4_REVIEW_FOLLOWUP_06_PREPARATION.json',A/'PERSISTENT_DAMAGE_20_TRANSFER_CHECK_03.json',A/'PERSISTENT_DAMAGE_20_ROOT_CHECK_04.json']
    for row in cov['aspects']:
        if row['id'] in ['DD-11','DD-12']:
            row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'de4-followup-persistent20-04','recordedAtUtc':now,'reviewed':465,'pending':383,'de4CurrentCases':37,'de4SourceBindings':88,'de4FollowupSubmitted':True,'persistent20EvidenceProvidedForAwarenessOnly':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'fullDomainClosureChanged':False})
    for b,a in zip(before['aspects'],cov['aspects']):
        assert all(b[k]==a[k] for k in ['status','closure','humanEvidence','completionClass'])
        if b['id'] not in ['DD-11','DD-12']: assert b==a
    ledger.write_bytes(encoded(cov))
    code=raw[builder].decode('utf8')
    tail=' + read(A / "NEXT25_READY_PERSISTENT20_03_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "DE4_FOLLOWUP_PERSISTENT20_04_NAVIGATION_DELTA.json")["changes"]\n')
    code=code.replace('    pending = [\n','    pending = [\n        ("DE4 Current06 — narrow follow-up submitted", "DE4_REVIEW_FOLLOWUP_06_PREPARATION.json"),\n        ("DE4 Conference05 — verified final report", "DE4_DIGITAL_CONFERENCE_05_FINAL_RECEIPT.json"),\n        ("Persistent20 — source-specific root options pending", "PERSISTENT_DAMAGE_20_ROOT_CHECK_04.json"),\n',1)
    scope='Video-game-only75-domain development.465 reviewed/383 pending;78 accepted interfaces. AC6 applied. DE4 final Conference05 review recovered; Current06/Fate04 narrow actual GPT follow-up active,37 cases88sources. Next25 Current06 packet ready/unsent. Persistent20 full source history, interface conflicts, transfer vectors and source-specific root proposals pending. No runtime, balance, canon or release closure; stop at20percent allowance remaining.'
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(vals)==1; code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    compile(code,str(builder),'exec'); builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next({**x['source'],'preservedCopy':x['preservedCopy']['path']} for x in saved if x['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]],'sourceInformationDeleted':0,'newRuleAdoptions':0,'all75DomainGatesUnchanged':True}))
    current={'id':'ACTIVE-AUTHORING-DE4-FOLLOWUP-PERSISTENT20-04','recordedAtUtc':now,'status':scope,'previousCheckpoint':info(prev),'historyPolicy':oldcp['historyPolicy'],'counts':oldcp['counts'],'activeGptReview':{'threadId':payload['thread']['id'],'threadTitle':payload['thread']['title'],'userTurnId':turn['id'],'archive':info(A/'DD_DE4_Review_Followup_06.zip'),'nativeEvidence':info(A/'DE4_REVIEW_FOLLOWUP_06_SUBMITTED_NATIVE.json'),'actualMessage':info(A/'DE4_REVIEW_FOLLOWUP_06_ACTUAL_MESSAGE.txt'),'reviewStatus':'Submitted narrow semantic follow-up; no acceptance inferred.'},'de4':{'draft':info(R/'data/director/spell_proposals/divination_enchantment_rank4_current_06.json'),'guard':info(A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_04.json'),'check':info(A/'DE4_REVIEW_REVISION_CHECK_06.json'),'priorFinalReview':info(A/'DE4_DIGITAL_CONFERENCE_05_FINAL_RECEIPT.json'),'adopted':False},'next25':oldcp['next25'],'persistent20':{'sourceAudit':info(R/'data/director/spell_review/persistent_damage_20_source_convergence_01.json'),'interfaceFindings':info(R/'data/director/spell_review/persistent_damage_20_interface_findings_02.json'),'transferVectors':info(R/'data/director/spell_review/persistent_damage_20_transfer_vectors_03.json'),'rootOptions':info(R/'data/director/spell_review/persistent_damage_20_root_proposal_04.json'),'providedToGptForAwarenessOnly':True,'semanticReviewRequested':False,'adopted':False},'remainingAuthorshipMap':info(R/'data/director/spell_review/remaining_spell_authoring_map_03.json'),'lastUsageObservation':{'weeklyUsedPercent':10,'weeklyRemainingPercent':90,'shortWindowReported':False},'usageStop':oldcp['usageStop'],'latestVerifiedGitHubBackup':oldcp['latestVerifiedGitHubBackup'],'coverageLedger':info(ledger),'navigationDelta':info(delta),'preservedNavigation':info(keep/'PRESERVATION_MANIFEST.json'),'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'wholeGameFlowConfirmed':False,'releaseApproved':False}
    cp.write_bytes(encoded(current))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode==0,(run.stdout[-2000:],run.stderr[-2000:])
    build=read(buildfile); assert not build['missingLinks']
    current['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]}; cp.write_bytes(encoded(current))
    report.write_bytes(encoded({'checkpoint':info(cp),'delta':info(delta),'savedNavigationFiles':len(saved),'all75DomainGatesUnchanged':True,'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[],'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps(read(report)))

if __name__=='__main__': main()
