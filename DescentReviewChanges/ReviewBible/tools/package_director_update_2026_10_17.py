"""Package the owner's requested latest-change handoff to the actual GPT Director."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p): return json.loads(p.read_bytes())

def main():
    out=A/'director-latest-changes-2026-10-17'
    archive=A/'DD_Director_Latest_Changes_2026_10_17.zip'
    preparation=A/'DIRECTOR_LATEST_CHANGES_2026_10_17_PREPARATION.json'
    request=A/'DIRECTOR_LATEST_CHANGES_2026_10_17_REQUEST.txt'
    assert not any(p.exists() for p in [out,archive,preparation,request])
    rec=read(A/'AC6_EXACT_ACCEPTANCE_06_RECEIPT.json')
    check=read(A/'AC6_EXACT_ACCEPTANCE_06_APPLICATION_CHECK.json')
    index=read(R/'data/public/spell_playtests/authored_review_index.json')
    assert index['authoredCounts']=={'reviewed':465,'pending':383}
    assert check['checkCount']==1367 and check['failureCount']==0
    for b in rec['acceptedArtifactBindings']: assert info(G/b['path'])==b
    for c in rec['canonicalCopies']:
        assert info(G/c['source']['path'])==c['source']
        assert info(G/c['destination']['path'])==c['destination']
        assert (G/c['source']['path']).read_bytes()==(G/c['destination']['path']).read_bytes()
    paths=[G/b['path'] for b in rec['acceptedArtifactBindings']]
    paths += [G/c['destination']['path'] for c in rec['canonicalCopies']]
    paths += [A/n for n in ['DD_AC6_Semantic_Current_06.zip','DD_AC6_Semantic_Current_06_Review.zip','ac6-exact-acceptance-06/REVIEW.json','ac6-exact-acceptance-06/VERDICT.md','AC6_EXACT_ACCEPTANCE_06_ACTUAL_NATIVE.json','AC6_EXACT_ACCEPTANCE_06_RECEIPT.json','AC6_EXACT_ACCEPTANCE_06_APPLICATION_CHECK.json','AC6_EXACT_ACCEPTANCE_06_OPERATIONS.json','source-before-ac6-exact-acceptance-06/PRESERVATION_MANIFEST.json','source-before-ac6-exact-acceptance-06/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json','DE4_DIGITAL_FIXTURES_CHECK_04.json','DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json']]
    paths += [R/n for n in ['data/public/spell_playtests/authored_review_index.json','docs/mechanics/ABJURATION_CONJURATION_RANK6_REVIEW_STATUS.json','tools/apply_ac6_exact_acceptance_06.py','data/director/spell_proposals/divination_enchantment_rank4_current_04.json','data/director/spell_proposals/divination_enchantment_rank4_current_03.json','tools/prepare_de4_digital_fixtures_04.py','data/director/spell_review/accepted_interface_registry_02.json','data/director/spell_review/ordinary_spell_inventory_01.json','data/director/spell_review/damage_control_25_semantic_delta_01.json','docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md','docs/DEVELOPMENT_DIRECTION.md']]
    paths += [G/'docs/audit/2026-10-17/github-snapshot-stop/PUSH_RECEIPT.json']
    paths=sorted(set(paths),key=lambda p:p.relative_to(G).as_posix())
    for p in paths: assert p.is_file(),p
    summary='''# Latest changes for GPT Director — 17 October 2026

The owner explicitly asked Codex to push the latest changes to GPT. This packet updates the Director notebook with the actual current local files. Development is video-game-only.

## Completed since GitHub c1e2b7d

The exact AC6 Current06 acceptance was independently bound to the downloaded review ZIP, the exact submitted input ZIP, all eight accepted payloads, all 103 frozen/current source files, all 14 source/access records, 16 placements, 55 current case identities, 51 original scenario identities and 22 unchanged original texts. The accepted model, casebook and both manuscripts were copied byte-for-byte into their canonical destinations. The authored index now records **465 reviewed / 383 pending**, with 189 complete standalone procedures. All 1,367 application checks passed. This is authored video-game rules integration, not runtime or gameplay approval.

The exact acceptance wrapper, application receipt/check/operations, original index preservation copy, current index, status record and application script are included. The complete prior submission ZIP supplies the unchanged frozen evidence; no settled semantic re-review is requested. Historical candidate wording inside accepted payloads remains verbatim; current status is supplied by the separate receipt and index.

## Pending work, explicitly not accepted

DE4 Current04 is included as the latest saved draft, alongside Current03, its preparation script and 331-check report. The fixture changes cover real Field Repair and legal Phantasmal Killer class-access/Null-root/timing branches. A source-reference defect was identified after that draft: N25's new Wizard engine/7 citation must be corrected to the relevant engine/9 school-specialization and engine/11 protected-dissonance entries, and N24 needs engine/9 for its Abjuration specialization. This correction has NOT yet been written. The existing report verifies pointer resolution but does not prove that this wrong-but-resolving pointer supports the claim. All 15 procedures remain pending joint review. The Fate guard remains an unadopted proposal.

The 49-entry registry02, inventory01 and next25 semantic delta are included only as existing preparation context. They have NOT yet been refreshed for AC6 adoption. Inventory01's historical 451/397 counts and pending-AC6 statement are stale; the current authored index and AC6 application receipt control. START_HERE, review map, coverage ledger and the active authoring checkpoint also still await the corresponding navigation update. Do not infer approval from these drafts or stale navigation.

## Requested Director response

Verify the manifest and the current applied index/copies against the accepted AC6 bindings. Acknowledge the updated 465/383 accounting, or identify a concrete mismatch. Keep AC6 semantic review closed unless the exact files reveal a concrete contradiction. Confirm your current next priorities and the narrow unresolved decisions requiring conference before DE4/next25; do not approve unseen or incomplete dependencies. No new global rule, Fate guard, runtime execution, human playtesting, numerical balance, cosmology canon, whole-game completion or release approval is requested.

The GitHub backup at c1e2b7d predates this AC6 application. This handoff is to GPT, not another GitHub push. Full source history remains preserved.
'''
    out.mkdir()
    (out/'LATEST_CHANGES.md').write_text(summary,encoding='utf8',newline='\n')
    manifest={'id':'DIRECTOR-LATEST-CHANGES-2026-10-17','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'ownerInstruction':'Ok. push to GPT your latest changes','destinationThreadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','destinationTitle':'Review Continuation Part 4','authoredCounts':index['authoredCounts'],'ac6Applied':True,'de4Applied':False,'newRulesBeyondAcceptedAc6':False,'files':[info(p) for p in paths],'summary':info(out/'LATEST_CHANGES.md'),'sourceInformationDeleted':0,'runtimeTestsExecuted':0}
    (out/'MANIFEST.json').write_bytes(encoded(manifest))
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(out/'LATEST_CHANGES.md','LATEST_CHANGES.md')
        z.write(out/'MANIFEST.json','MANIFEST.json')
        for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for b in manifest['files']:
            raw=z.read('files/'+b['path'])
            assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
        assert z.read('LATEST_CHANGES.md')==(out/'LATEST_CHANGES.md').read_bytes()
    b=info(archive)
    text=f'''The owner asked: "push to GPT your latest changes." Attached is the latest actual local state, DD_Director_Latest_Changes_2026_10_17.zip ({b['bytes']} bytes; SHA-256 {b['sha256']}).

Read LATEST_CHANGES.md first, then MANIFEST.json. AC6 Current06 is now locally integrated with all eight accepted files byte-identical and 1,367 application checks passing. The authoritative current index is 465 reviewed / 383 pending (189 complete standalone procedures). The exact accepted submission, recovered acceptance, current copies, before/after index evidence and application records are included.

DE4 Current04 and its check report are included as PENDING drafts only. The README identifies the unfinished Wizard source-reference correction and the unadopted Fate guard. Registry02/inventory01/next25 delta are preparation context; registry/inventory/navigation have not yet been refreshed after AC6, so the current index and receipt control the count.

Please verify receipt of this exact archive and the applied AC6 bindings/counts, then give your next priorities and any consequential unresolved decisions requiring our conference. Do not repeat the accepted AC6 semantic review absent a concrete mismatch, and do not approve the pending DE4/Fate guard from this status handoff. Preserve the video-game-only direction and separate authored acceptance from implementation, gameplay, balance, canon and release gates.
'''
    request.write_text(text,encoding='utf8',newline='\n')
    preparation.write_bytes(encoded({'id':manifest['id'],'archive':b,'manifest':info(out/'MANIFEST.json'),'summary':info(out/'LATEST_CHANGES.md'),'request':info(request),'fileCount':len(paths),'memberCount':len(paths)+2,'allMemberBytesVerified':True,'authoredCounts':index['authoredCounts'],'newRuleAdoptionsFromPackaging':0,'sourceInformationDeleted':0}))
    print(json.dumps(read(preparation)))

if __name__=='__main__':main()
