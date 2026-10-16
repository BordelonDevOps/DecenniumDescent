from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,re
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
now=datetime.now(timezone.utc).isoformat()
check=A/'VIDEO_GAME_ONLY_01_APPLICATION_CHECK.json';checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json'
assert not check.exists() and not checkpoint.exists()
previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_SEMANTIC_CURRENT_06_SUBMITTED.json'
keep=A/'navigation-before-video-game-only-01';manifest=keep/'PRESERVATION_MANIFEST.json';saved=read(manifest)
ledger=R/'data/playtest/game_development_coverage.json';cov=read(ledger);direction=cov['developmentDirection'];oldcov=read(keep/ledger.relative_to(G))
start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';directive=R/'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md'
attachment=Path(r'C:\Users\cbord\.codex\attachments\648011ef-dacb-416d-914d-45e18bcc1793\Pasted text.txt')
protocol=R/'docs/mechanics/SPELL_REVIEW_PROTOCOL.md';registry=R/'data/director/spell_review/accepted_interface_registry_02.json';inventory=R/'data/director/spell_review/ordinary_spell_inventory_01.json';semantic=R/'data/director/spell_review/damage_control_25_semantic_delta_01.json';index=R/'data/public/spell_playtests/authored_review_index.json'
delta=A/'VIDEO_GAME_ONLY_01_NAVIGATION_DELTA.json';build=read(A/'REVIEW_MAP_BUILD.json')
assert not build['missingLinks'] and build['sha256']==info(G/'REVIEW_MAP.html')['sha256']
assert directive.read_bytes()==attachment.read_bytes()
for item in saved:
 assert hashlib.sha256((G/item['preservedCopy']).read_bytes()).hexdigest()==item['sha256']
for change in read(delta)['changes']:
 assert info(G/change['after']['path'])==change['after']
assert len(cov['aspects'])==75 and read(index)['authoredCounts']=={'reviewed':451,'pending':397} and len(read(registry)['entries'])==49
for row,old in zip(cov['aspects'],oldcov['aspects']):
 assert row['id']==old['id']
 for k in ['status','closure','humanEvidence','completionClass','reviewEvidence','sourceEvidence','validationEvidence','draftEvidence']:
  assert row[k]==old[k],(row['id'],k)
# Reverify source bindings from the frozen accelerated-review source manifest and exact accepted registry.
protected=[protocol,registry,inventory,semantic,index,A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json',A/'DD_AC6_Semantic_Current_06.zip',R/'data/director/spell_proposals/divination_enchantment_rank4_current_03.json',A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json']
known={'SPELL_REVIEW_PROTOCOL.md':'9c23553beb4656b7df526ab387cbf8da42efd0044f80a053235046e79e8ba360','accepted_interface_registry_02.json':'b241873b8eb0b33030293b0f4807486a961ce92911de0eb7fdde6f77cc12c456','ordinary_spell_inventory_01.json':'79f217c989eb26f177782aae674a7065307ef97c7d7d32cf13eafacd73517588','damage_control_25_semantic_delta_01.json':'feccac44f06106d948fca0af3fd6c6356c406212ffa35b2a096a00c733428a6d','DD_AC6_Semantic_Current_06.zip':'4693842bf52da2062d27e22d30d08dff450dbdf563c36b7399db4ca34909872f','divination_enchantment_rank4_current_03.json':'17c1a727dd7a8f959818875d9029e1873b31e9d1ca324a78688eb333f8cd8f3e','DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json':'427f290d5738c7faa2ac955141c8c86f75c84ec9a79c32b7fadce45bafd500d1'}
for p in protected:
 if p.name in known:assert info(p)['sha256']==known[p.name],p
checked_links=0
for p in [guide,start]:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#')[0]).resolve()
  assert q==checkpoint.resolve() or q.exists(),(p.name,target)
  checked_links+=1
application={'recordedAtUtc':now,'direction':direction,'attachmentBytes':attachment.stat().st_size,'attachmentSha256':hashlib.sha256(attachment.read_bytes()).hexdigest(),'directive':info(directive),'verbatimCopy':True,'navigationFilesPreserved':len(saved),'protectedFiles': [info(p) for p in protected],'areasRetained':75,'digitalScopesUpdated':[r['id'] for r in cov['aspects'] if 'priorDirectionScope' in r],'domainClosureAndEvidenceUnchanged':True,'ordinarySpellCounts':read(index)['authoredCounts'],'registryEntries':49,'guideAndStartPageLocalLinksVerified':checked_links,'reviewMapExistingLinks':build['existingDistinctLinks'],'reviewMapMissingLinks':[],'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsRun':False,'scope':'Direction/navigation/preservation checks only; no mechanic implementation or gameplay validation.','validationRepair':'Initial validation encountered the link to this not-yet-written successor checkpoint. Completed finalization without rerunning the applied mutation script; validated all links after writing checkpoint.'}
check.write_bytes(encoded(application))
state=read(previous)
scope=build['notebookReview']
state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',developmentDirection=direction,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),applicationCheck=info(check),newRuleAdoptions=0,newRuleAdoptionScope='Owner direction and navigation only; no source mechanic, accepted cohort, cosmology canon or domain closure changed.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
state['activeGptReview'].update(userTurnId='b5b34710-2b90-4e7a-b644-a27f19a0fec8',status='Current06 was submitted once. Later notebook discussion describes AC6 as completed; exact acceptance artifact remains unrecovered and unverified. Do not resend or adopt from a later summary.',generationConfirmedLiveAtObservation=False,returnReceived=False,newRulesAdopted=False)
state['acceleratedReview']={'protocol':info(protocol),'registry':info(registry),'inventory':info(inventory),'next25SemanticDelta':info(semantic),'preflight':info(A/'accelerated-review-01/PREFLIGHT.json'),'supersession':'Video-game-only directive controls conflicting tabletop requirements and future acceptance wording.'}
state['safeNextActions']=['Follow the video-game-only directive and active guide; do not resume tabletop chapter/worksheet/GM publication work from historical checkpoint prose.','Recover and verify AC6 exact Current06 acceptance artifact before local adoption; no resubmission merely because older browser messages are unavailable.','Correct DE4 two identified fixture errors as deterministic digital test vectors while preserving originals. Do not adopt the pending Fate guard amendment without substantive conference.','Continue the prepared25-spell semantic delta with accepted-interface inheritance, actual automated preflight and narrowly authored engine decisions; no repeated review of settled scopes.','Preserve all75 domain identities; pursue their digital scope, final actual-GPT whole-game flow and verified delivery. Source/canon and implementation/gameplay/balance/release gates remain separate.']
state.setdefault('preservationManifests',[]).append(info(manifest));checkpoint.write_bytes(encoded(state))
for p in [guide,start]:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if '://' not in target and not target.startswith('#'):assert (p.parent/target.split('#')[0]).exists(),target
assert 'Active direction — video game only' in start.read_text(encoding='utf8')
assert 'Video game only:' in (G/'REVIEW_MAP.html').read_text(encoding='utf8')
print(json.dumps({'directive':info(directive),'guide':info(guide),'checkpoint':info(checkpoint),'preservedFiles':len(saved),'areas':75,'updatedScopes':len(application['digitalScopesUpdated']),'localMarkdownLinks':checked_links,'reviewMapLinks':build['existingDistinctLinks'],'missingLinks':0,'newRuleAdoptions':0}))
