"""Freeze the complete persistent20 semantic conference; no submission or adoption."""
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def bindings(v):
 if isinstance(v,dict):
  if all(k in v for k in ['path','bytes','sha256']):yield {k:v[k] for k in ['path','bytes','sha256']}
  for z in v.values():yield from bindings(z)
 elif isinstance(v,list):
  for z in v:yield from bindings(z)

def main():
 root=A/'persistent-damage-20-conference-06';zp=A/'DD_Persistent_Damage_20_Conference_06.zip';req=A/'PERSISTENT_DAMAGE_20_CONFERENCE_06_REQUEST.txt';prep=A/'PERSISTENT_DAMAGE_20_CONFERENCE_06_PREPARATION.json'
 assert not any(p.exists() for p in [root,zp,req,prep]);draft=R/'data/director/spell_proposals/persistent_damage_20_current_06.json';d=read(draft);paths={draft}
 for bind in d['sourceBindings']:
  p=G/bind['path'];assert info(p)==bind,bind['path'];paths.add(p)
 registry=read(R/'data/director/spell_review/accepted_interface_registry_04.json')
 for e in registry['entries']:
  for bind in bindings({'current':e['currentAuthoritativeSource'],'acceptance':e['acceptanceBasis']}):
   p=G/bind['path'];assert info(p)==bind,bind['path'];paths.add(p)
 names=['PERSISTENT_DAMAGE_20_SOURCE_CONVERGENCE_CHECK_01.json','PERSISTENT_DAMAGE_20_INTERFACE_FINDINGS_CHECK_02.json','PERSISTENT_DAMAGE_20_TRANSFER_CHECK_03.json','PERSISTENT_DAMAGE_20_ROOT_CHECK_04.json','PERSISTENT_DAMAGE_20_CURRENT_CHECK_01.json','PERSISTENT_DAMAGE_20_VECTOR_CHECK_02.json','PERSISTENT_DAMAGE_20_VECTOR_CHECK_03.json','PERSISTENT_DAMAGE_20_ADVERSARIAL_CHECK_04.json','PENDING_COHORTS_AFTER_DE4_07_CHECK.json','PERSISTENT_DAMAGE_20_CONFERENCE_CHECK_06.json']
 paths.update(A/n for n in names);paths.add(R/'tools/prepare_persistent_damage20_conference_06.py')
 root.mkdir();(root/'README.md').write_text('''# Persistent damage20 — full semantic conference06

Prepared UNSENT while actual next25 review is active. Ordinary authored counts remain480 reviewed/368 pending. No new acceptance, runtime execution, human gameplay, balance, cosmology or release approval is implied.

## Complete source review

Read MANIFEST.json, then the complete `files/DescentReviewChanges/ReviewBible/data/director/spell_proposals/persistent_damage_20_current_06.json`.

Read all20 `spells` (full source/access, procedure, remainingDecisions and damageRootProposal), `sharedRules`, `sharedContractRouting06`, all24 `conferenceDecisions06`,40 `currentExamples`,7 `currentSupplementalExamples` and8 `adversarialVectors04`. No source/scenario is represented by an identifier-only summary. Full previous drafts and all original40 texts remain preserved.

Current exact accepted interfaces control only their actual scope. The routed original shared contracts fill per-source context; current explicit spell/shared changes govern their local changes. Original status/example premises remain history, not competing current authority. A conflicting actual rule must be reported, not silently overridden. Some original hypothetical scenarios are deliberately limited composition/state-machine obligations; complete sourced supplements establish narrower actual encounters without pretending those hypothetical inputs exist in a current source.

## Material choices requiring concurrence

- Inferno Wave: real finite preexisting fuel, at most twelve actual clipped five-foot patches, short endpoints and real extinguishing. Current ground provenance stores actual caster/Null at ignition only for this finite patch; no global environmental ownership or automatic spread.
- Freezing Rain and Crystalline Growth: actual continuous contacted distance, genuine voluntary stopping and family exposure clocks; frame/input subdivision cannot manufacture or postpone exposure. Fixed crystal patch identities conserve HP and cleared state through suppression.
- Ice Storm: single mixed4d6+4d6 event and distinct one-minute magical terrain. P20-ICE-MIXED-04 is a separate proposed proportional aggregate flat-DR allocation option, deliberately not integrated before its own decision. Pending Meteor Spear cannot approve it by analogy.
- Wall of Fire: distinct crossing and nearby categories, each once per target/round across owners. Genuine teleport arrival can enter; teleport across without contact cannot. Each finite field and actual source origin remains separate.
- Vitriolic Sphere: one original future caster START, one private5d4 only when an operative due recipient exists, original save factor, suppressed opportunity consumed without replay. Caster death does not cancel the nonconcentration recipient rider.
- Storm Sphere: explicit new remote sphere origin, actual owner close-quarter rules and Bonus Action. The real Mage Undying Spellform/Arcane Ray/Ranger Beast supplement proves a lawful pulse while no independent Bonus Action is available; no invented unconscious-concentration exception or automatic bolt.
- Flame Typhoon: current perceived designated enemies,10ft horizontal inward force, actual support/collision and one family pulse. This is not secret hostility detection.
- Immolation: choiceA registers ordinary-extinguishable fire, with actual self/helper Action/full immersion clearing all eligible records including suppressed ones. Original one-record DEX task remains preserved. Accepted same-marker highest-expected-fire arbitration permits one winning group; all due groups consume ticks and keep their own permitted saves. Four future END ticks remain finite.
- Arcane Mortar: proposed three total shots rather than silently converting three rounds into unlimited fire. It is a100lb/AC16/HP30 object, using actual owner command and shared offensive activation; no creature/profile target waiver, supply refill, salvage or repair resurrection.
- Sonic Collapse: actual Shatter admission and one bounded section per structural whole, real preexisting weakness/durability and finite fallback debris. Extra integrity loss is not DamageDealt funding. Actual creature Falling remains separate; no world-scale recursive collapse by a generic name.
- Leeching Plague versus Enervation: separately proposed donor filters. Both exclude actual transfer branches with no-derived-healing/no-recovery flags before summing and flooring half. Complete Burden Shared and Life Linked vectors retain actual class access, costs and stages. A symbolic split alone is not a legal transfer or heal source.
- Aura of Dread, Blood Fog, Rift Spiral and Shadow of Moil: exact source predicates, ordinary knowledge/vision, true physical geometry, finite controllers and independent condition/damage components. The broad Moil resistance and cosmetic-only appearance are explicit decisions; non-damage HP costs remain outside damage resistance.
- Mass Decay: private lazy cast/ordinal2d6 caches, recipient-specific original roots, no earlier suppressed replay and no hidden timing/disclosure signal.
- Synaptic Static: original school-specific area and affected-roll categories, finite endings, earliest eligible one-die rider and actual Bane. The private original d6 stays fixed through a permitted d20 replacement. DE4 exact07 is now accepted/applied; no sixth presentation entry or hidden modifier disclosure follows from an otherwise permitted OVERT-ATTACK d20 view.
- Greater Phantasmal Killer: original4d6 is retained, with no invented fear or automatic rank upgrade to lower4d10. Complete accepted lower Phantasmal Killer and full pending True Seeing are included in `fullCounterparts06`. This greater source’s establishment-root mapping and independent damage/recognition separation still require their own decision. No approval of the entire True Seeing/illusion group is requested here.

## Requested result

Return substantive source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED for each procedure and all24 questions. Separate actual blockers from future runtime/balance work. For any required correction, provide complete replacement values at real Current06 JSON pointers, preserving historical text and scenario IDs. Supply downloadable REVIEW.json,VERDICT.md and PROPOSED_CORRECTIONS.json if needed. No exact acceptance of unseen future integration files is requested.

Registry04 and full underlying accepted sources/receipts are supplied. Exact accepted files may retain historical PENDING wording; the actual acceptance receipt and current index establish their scoped status. Keep settled AC6/DE4 closed and all75 domain gates distinct. The website/cosmology records and original source matter are not rewritten by this mechanics conference.
''',encoding='utf8',newline='\n')
 paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix());manifest={'id':'PERSISTENT-DAMAGE-20-CONFERENCE-06','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(draft),'files':[info(p) for p in paths],'readme':info(root/'README.md'),'counts':{'identities':20,'printedPlacements':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in d['spells']),'originalScenarioTexts':40,'currentOriginalVectors':40,'supplementalVectors':7,'adversarialVectors':8,'conferenceQuestions':24},'authoredCounts':{'reviewed':480,'pending':368},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0};(root/'MANIFEST.json').write_bytes(encoded(manifest))
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in ['README.md','MANIFEST.json']:z.write(root/n,n)
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for bind in manifest['files']:
   raw=z.read('files/'+bind['path']);assert len(raw)==bind['bytes'] and hashlib.sha256(raw).hexdigest()==bind['sha256']
 bind=info(zp);req.write_text(f'''Please conduct the full persistent-damage20 semantic conference using DD_Persistent_Damage_20_Conference_06.zip ({bind['bytes']} bytes;SHA256 {bind['sha256']}). Read README.md,MANIFEST.json and Current06:20 complete procedures/source-access/root mappings,40 original-case vectors,7 full-source supplements,8 adversarial cases,24 explicit decisions,complete accepted interfaces and full previous source history.

Please give source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED for all20 procedures and24 questions. Resolve the explicitly new fuel/structural bounds, recurring roots/clocks, ongoing-fire cure/arbitration, private delayed RNG, separate Ice Storm mixed-defense allocation, three-shot object mortar, transfer-healing exclusions and distinct donor predicates. DE4 exact07 is accepted/applied; current Fate and lower Phantasmal Killer are bound completely. True Seeing is included as a full pending counterpart, not approved by this conference. Current480/368 counts remain unchanged.

Return downloadable REVIEW.json,VERDICT.md and full exact pointer replacements if required. Preserve original scenario IDs and source text, actual class-school access and all history. Distinguish limited composition/conditional obligations from proved source-grounded fixtures and runtime. No new disclosure entry, global environment rule, cosmology, human balance or runtime/release approval. Keep settled AC6/DE4 closed; exact integration bytes will receive a later dedicated acceptance review.''',encoding='utf8',newline='\n')
 prep.write_bytes(encoded({'archive':bind,'candidate':info(draft),'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared UNSENT; await active next25 conference.','newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps(read(prep)))
if __name__=='__main__':main()
