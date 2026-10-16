"""Package the exact current review for the owner's actual Part 4 notebook."""
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def main():
    root=A/'part4-relic-null-handoff-01'
    archive=A/'DD_Part4_Relic_Null_Revision_Handoff_01.zip'
    receipt=A/'PART4_RELIC_NULL_HANDOFF_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    root.mkdir()
    mapping={
      'ORIGINAL_REVIEW_INPUT.zip':A/'DD_Cosmology_Epilogue_Relic_Null_01.zip',
      'ORIGINAL_GPT_RETURN.zip':A/'DD_Cosmology_Epilogue_Relic_Null_01_Return_01.zip',
      'SEMANTIC_REVIEW.json':A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.json',
      'SEMANTIC_REVIEW.md':A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.md',
      'REVISION_REQUEST.txt':A/'COSMOLOGY_EPILOGUE_RELIC_NULL_02_REVISION_REQUEST.txt',
      'RETURN_SOURCE_CHECK.json':A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_RETURN_SOURCE_CHECK_01.json',
      'context/ACTIVE_CHECKPOINT.json':A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_RECOVERY_01.json',
      'context/CURRENT_COSMOLOGY_READ_FIRST.md':R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md',
      'context/SOULS_RESEARCH_APPLICATION_CHECK.json':A/'COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json',
      'context/CHRONOLOGY_ROUTE_APPLICATION_CHECK.json':A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_APPLICATION_CHECK.json',
      'context/EPI01_07_APPLICATION_CHECK.json':A/'COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json',
    }
    life=R/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md'
    mapping['additional_sources/'+life.relative_to(G).as_posix()]=life
    frozen=[{'packagePath':n,**info(p)} for n,p in mapping.items()]
    for n,p in mapping.items():
        out=root/n;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(p.read_bytes())
    (root/'ADDITIONAL_SOURCE_BINDINGS.json').write_bytes(encoded([info(life)]))
    handoff='''# Current Decennium Descent handoff to Review Continuation Part 4

Your opening response used an older checkpoint. Do not restart Operational Souls / Death Jurisdiction. The bounded souls/research/Hunt module, chronology research route, and EPI-01–07 character module were subsequently reviewed with actual Part3 and applied locally. The three application receipts and current reader guide are included. Their scope remains provisional authored tabletop rules, not cosmological identity, runtime, human balance or whole-game approval.

Current task: revise the actual completed EPI-08–14 return in response to RNX-01–14. Codex recovered your original exact 70,386-byte ZIP, SHA256 24eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699. All 234 independent frozen source/file/citation checks pass. All eight original return files remain unchanged. The semantic audit requires14 corrections and28 follow-up scenarios; no EPI08–14 rules have been adopted.

Read ORIGINAL_REVIEW_INPUT.zip for the original83 frozen sources and exact request. Read ORIGINAL_GPT_RETURN.zip for your complete candidate,47 cases,source hashes and verdict. Read SEMANTIC_REVIEW and REVISION_REQUEST for the actual findings. The line saying the request is prepared-only describes its saved local creation state; this upload now submits it to you.

Additional source: CREATURE_LIFECYCLE_PLAYTEST.md is supplied under additional_sources at its actual project-relative path, with exact binding. Your corrected SOURCE_HASHES must retain all83 original frozen bindings and add this one current binding (84 total), rather than claiming it was in the old packet. Context files and application receipts are handoff evidence, not another set of source rules. The old83 include current Combat Action, Body Equipment, Language Communication and Healing/Death references. The only current drift among the83 is the reader guide's added workflow/navigation text; original source and adopted rule payloads remain unchanged.

Two follow-up observations from Codex's actual source read: COMBAT_ACTION_PLAYTEST already preserves original virtual turn markers and absolute outside-initiative deadlines through initiative changes; RNX-04 can use that existing rule. LANGUAGE_COMMUNICATION_PLAYTEST distinguishes physical sound suppression from the full Silenced condition and requires the actual caster's audible V. Use these current rules, not an invented replacement engine.

Codex has not implemented its RNX recommendations. Treat them as proposals to discuss/correct, not pre-approved mechanics. For flora, portable finite planting trays are one possible NEW way to preserve a brief visit while permitting later identification/harvest; if you choose this, author exact stock identities, retrieval time, dimensions, mass, hand/carry and return eligibility, with no copied plants or hidden access extension. You may propose a better complete solution with source reasoning.

Return a complete corrected DD_Cosmology_Epilogue_Relic_Null_02_Return.zip containing exactly the eight named root files in REVISION_REQUEST. Include all47 earlier case IDs (corrected where necessary; old versions remain in the original ZIP) and28 RNX scenarios with initial state, real actions, rolls/DCs, one elapsed timeline, stock/custody and final state. Keep a clear RNX disposition and changed-field map. Complete both playable chapters and all actor/scene dependencies, not only an amendment list. The manifest lists the other seven exact output hashes and byte counts. Report the final ZIP hash and size in your chat reply.

Preserve original manuscripts and explicit owner corrections, unresolved Heartcell/other identities, the after-Infinite-Yield premise and the unanswered campaign era. No historical information may be deleted. Do not claim approval of the separate later-arcs, consumable or environment drafts: those remain unsubmitted/unadopted. Ordinary spells remain419 reviewed/429 pending; trade recipes687 reviewed is a separate catalog. The owner authorized actual GPT collaboration, but final joint whole-game flow, runtime, human testing, balance and publication are still open. Latest verified GitHub backup is18c6e3a; subsequent work is local.

The previous Part3 displayed a usage-limit alert; exact archive access has now succeeded. This is a new actual Part4 conversation, not a reason to reauthor already-adopted modules or retry old base64 exports.
'''
    (root/'HANDOFF.md').write_text(handoff,encoding='utf-8',newline='\n')
    files=[]
    for p in sorted(root.rglob('*')):
        if p.is_file():
            b=p.read_bytes();files.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':files,'sources':frozen,'originalFrozenSources':83,'additionalCurrentSources':1,'rulesAdopted':False}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with ZipFile(archive) as z:
        for f in files:
            b=z.read(f['path']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
    assert frozen==[{'packagePath':n,**info(p)} for n,p in mapping.items()]
    record={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'manifest':info(root/'PACKAGE_MANIFEST.json'),
       'destinationTitle':'Review Continuation Part 4','destinationThreadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8',
       'url':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1acef-455c-83ea-bc33-56e4adaec9c8',
       'browserId':'3','tabId':'125746308','originalSources':83,'additionalSources':1,'revisionFindings':14,'originalCases':47,'requestedAdditionalCases':28,
       'sourceFilesUnchanged':True,'submitted':False,'creationTimeStatus':'Prepared; a separate actual submission receipt is required.','newRulesAdopted':False}
    receipt.write_bytes(encoded(record));print(json.dumps({'preparation':info(receipt),'archive':info(archive),'files':len(files)+1,'checks':len(files),'failures':0}))

if __name__=='__main__':main()
