"""Freeze the next full illusion conference without interrupting active next25 review."""
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
 root=A/'illusion-perception-14-conference-11';zp=A/'DD_Illusion_Perception_14_Conference_11.zip';req=A/'ILLUSION_PERCEPTION_14_CONFERENCE_11_REQUEST.txt';prep=A/'ILLUSION_PERCEPTION_14_CONFERENCE_11_PREPARATION.json';assert not any(p.exists() for p in [root,zp,req,prep]);draft=R/'data/director/spell_proposals/illusion_perception_14_current_11.json';d=read(draft);paths={draft}
 for bind in d['sourceBindings']:
  p=G/bind['path'];assert info(p)==bind,bind['path'];paths.add(p)
 def bindings(v):
  if isinstance(v,dict):
   if all(k in v for k in ['path','bytes','sha256']):yield {k:v[k] for k in ['path','bytes','sha256']}
   for z in v.values():yield from bindings(z)
  elif isinstance(v,list):
   for z in v:yield from bindings(z)
 registry=read(R/'data/director/spell_review/accepted_interface_registry_04.json')
 for e in registry['entries']:
  for bind in bindings({'current':e['currentAuthoritativeSource'],'acceptance':e['acceptanceBasis']}):
   p=G/bind['path'];assert info(p)==bind,bind['path'];paths.add(p)
 names=['ILLUSION_PERCEPTION_15_SOURCE_CHECK_01.json','ILLUSION_PERCEPTION_14_CURRENT_CHECK_01.json','ILLUSION_PERCEPTION_14_STEED_CHECK_02.json','ILLUSION_PERCEPTION_14_FIXTURE_CHECK_03.json','ILLUSION_PERCEPTION_14_CURRENT03_POINTER_CHECK.json','PENDING_COHORTS_AFTER_DE4_07_CHECK.json','ILLUSION_PERCEPTION_14_SOCIAL_PROGRAM_CHECK_05.json','ILLUSION_PERCEPTION_14_MOVEMENT_CHECK_06.json','ILLUSION_PERCEPTION_14_CONTROL_VISIBILITY_CHECK_07.json','ILLUSION_PERCEPTION_14_RNG_ROOTS_CHECK_08.json','ILLUSION_PERCEPTION_14_COUNTERPART_CHECK_09.json','ILLUSION_PERCEPTION_14_CONFERENCE_CHECK_10.json','ILLUSION_PERCEPTION_14_BINDING_CHECK_11.json']
 paths.update(A/n for n in names);paths.update(R/'tools'/n for n in ['prepare_illusion_perception14_social_program_05.py','prepare_illusion_perception14_movement_06.py','prepare_illusion_perception14_control_visibility_07.py','prepare_illusion_perception14_rng_roots_08.py','prepare_illusion_perception14_counterparts_09.py','prepare_illusion_perception14_conference_10.py','prepare_illusion_perception14_binding_11.py'])
 root.mkdir();text='''# Illusion/perception14 — full semantic conference11

This packet is prepared and UNSENT. Do not interrupt the active next25 review. None of these14 identities is newly accepted. Ordinary counts remain480 reviewed/368 pending; accepted AC6/DE4 scope remains closed.

## Read order

1. MANIFEST.json binds every complete current file and the candidate.
2. `files/DescentReviewChanges/ReviewBible/data/director/spell_proposals/illusion_perception_14_current_11.json` is the current candidate. Read all14 `spells[].procedure` values, complete source/access records, `sharedContractRouting10`, `conferenceDecisions10`, all28 `currentExamples` and3 `supplementalVectors09`.
3. `sharedContractRouting10` routes each source identity to its full preserved original shared proposal and only named applicable keys. Source-specific current procedure changes control their explicit local exceptions. Old shared clauses about other cards supply no powers to this cohort. Original example/status blocks are history; actual Wizard engine11 and current fixtures supply first-distinct-matrixD0 without waiving Refrain or extra hooks.
4. Every original source record, procedure and all28 original scenario texts remain unchanged in history. `originalExamplesUnchanged` and each current case’s `originalTextUnchanged` preserve identities and wording. Complete earlier drafts are included; they are not competing current authorities.
5. Registry04 and the actual full sources/acceptance records behind its entries are supplied for scoped comparison. These accepted predicates are not a new global extension. Their historical tabletop wording remains evidence under the current video-game-only direction.

Current11 changes only three frozen guide-copy locations to exactly match Registry04. All procedures,28cases,3supplements and16questions are unchanged from Current10; its complete file and prepared packet remain preserved. Registry04/full current source authority controls these comparisons.

## Explicit decisions, not silent corrections

The16 conference questions address all14 procedures, their shared routing and the excluded Creation source. Current changes preserve old text and distinguish inherited facts from new scoped authorship:

- Greater Invisibility and Echofield retain the Core observer-known Invisible exception. Reality Fracture renders no silhouette for a baseline visually unperceived body, even when its location is known.
- Greater Phantom Steed proposes Small/Medium riderbody3/6Load only for this35Load mount, keeping350lb physical weight separate. The old205lb→20.5Load example is preserved; current baseline is9.5Load and an added-cargo branch shows the17.5Load Burdened threshold. Full-source suppression ending remains a separate explicit choice with real Lesser Antimagic and actual40ft Falling:next-same-slot-END descent,2d6=7,not immediate falling or5e dice.
- Mind Maze’s old mid-attack-resolution premise is not proven by ordinary Ready. Current case has a real paid Ready after the completed observable attack, plus a preserved conditional state-machine obligation. IP14-COMMIT-INTERRUPT-03 asks for an actual source or agreement on that limited evidence; no generic interrupt was invented.
- Echofield NEW08 fixes digital buffer/event ordering and private uniform choices; no empty-set draws, source-generated sound feedback, public hidden buffer or sixth DE4 disclosure entry.
- Spectral Army NEW08 proposes the caster as dealer for each distinct later discharge, recipient-specific roots and current Null at root creation. NEW09 narrows apparent targets to real ordinary weapon/unarmed Attack Action attacks; creature-only spells/class/profile targets and opportunity triggers retain their predicates. The full earlier broader companion clause is preserved. Actual Ray of FrostN31 is the counterexample.
- Programmed Illusion NEW09 does not automatically make an armed, visually/audibly absent anchor a perceived target for Detect Magic. N30 uses its actual30ft/active-perceived source predicate and later broad-school Action; no dormant-magic or secret-script disclosure is granted.
- True Seeing’s union/extent and Mental Prison bridge remain material choices. N29 binds the complete real pending Mental Prison record and shared proposal:entry28 and exit24 are two events leaving48HP from100,not one52-damage Wound event. This does not approve the separate Mental Prison cohort.

Some original branches deliberately remain conditional where the independent source is not supplied:one-hour suppression, extra turns, postcommit light/barrier events and an actual magical-darkness source. Current cases name those limits and add concrete valid counterparts; do not count them as fully proven encounter reachability. All numbers, structure and source/pointer checks are authored-file evidence only. No game runtime or human gameplay test was run.

## Requested response

Return source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED for every procedure and each of16 questions. Identify actual blockers and provide complete exact proposed replacements at real Current11 pointers, preserving history and scenario IDs. Supply downloadable REVIEW.json,VERDICT.md and PROPOSED_CORRECTIONS.json if needed. Do not re-open accepted AC6/DE4; do not approve unseen future final integration files.

Creation’s full original record is preserved separately in the candidate and source audit. Its permanent stock/material/food/sale/recipe semantics require a separate economy/crafting conference. All75 domain gates, cosmology boundaries, runtime/gameplay/balance and release gates remain distinct. No source information has been deleted.
'''
 (root/'README.md').write_text(text,encoding='utf8',newline='\n');paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix());manifest={'id':'ILLUSION-PERCEPTION-14-CONFERENCE-11','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(draft),'files':[info(p) for p in paths],'readme':info(root/'README.md'),'counts':{'identities':14,'printedPlacements':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in d['spells']),'originalScenarioTexts':28,'currentOriginalVectors':28,'supplementalVectors':3,'conferenceQuestions':16},'authoredCounts':{'reviewed':480,'pending':368},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 (root/'MANIFEST.json').write_bytes(encoded(manifest))
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in ['README.md','MANIFEST.json']:z.write(root/n,n)
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for bind in manifest['files']:
   raw=z.read('files/'+bind['path']);assert len(raw)==bind['bytes'] and hashlib.sha256(raw).hexdigest()==bind['sha256']
 bind=info(zp);message=f'''Please conduct the complete illusion/perception14 semantic source conference using DD_Illusion_Perception_14_Conference_11.zip ({bind['bytes']} bytes;SHA256 {bind['sha256']}). Read README.md,MANIFEST.json and Current11. It supplies14 full currentprocedures with actualsource/access,28 preservedoriginalscenario texts and28currentvectors,3 fullsourcecounterpart supplements,per-source sharedcontract routing and16 explicit questions. Creation remains separately preserved for economy/crafting; no acceptance is requested for it or the full Mental Prison cohort.

Please give substantive source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED for all14 procedures and16 questions. In particular settle mountLoad and suppressionending; MindMaze originalmid-resolution reachability versus realReady; privateEchofield ordering/visibility; SpectralArmy apparentattack-target and delayed-root mappings; ProgrammedIllusion detector eligibility; TrueSeeing union and MentalPrisonexit bridge. All older text/records are preserved. Conditional independent-source branches are explicitly limited rather than presented as executed encounters. Current realcounterparts include Darkvision,Silence,LesserAntimagic,AlterSelf,MinorIllusion,DetectMagic,RayofFrost,Ready,Help and actualWizardcasting.

Return downloadable REVIEW.json,VERDICT.md and any exact full pointer replacements. Preserve scenario IDs/class-schoolaccess and distinguish these new choices from accepted scopes. Keep settledAC6/DE4 closed; no hidden-information/Fate whitelist expansion, globalrule or cosmologypermission by analogy. No runtime/human gameplay/balance/release approval. Ordinary480/368 counts remain unchanged until actual final exact acceptance and application.'''
 req.write_text(message,encoding='utf8',newline='\n');prep.write_bytes(encoded({'archive':bind,'candidate':info(draft),'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared UNSENT; await active next25 conference, do not interrupt.','newRuleAdoptions':0,'runtimeTestsExecuted':0}));print(json.dumps(read(prep)))
if __name__=='__main__':main()
