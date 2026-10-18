"""Freeze the consolidated next25 manuscript and its complete conference evidence."""
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 root=A/'damage-control-25-conference-06';zp=A/'DD_Damage_Control_25_Conference_06.zip';req=A/'DAMAGE_CONTROL_25_CONFERENCE_06_REQUEST.txt';prep=A/'DAMAGE_CONTROL_25_CONFERENCE_06_PREPARATION.json'
 assert not any(p.exists() for p in [root,zp,req,prep])
 draft=R/'data/director/spell_proposals/damage_control_25_current_06.json';d=read(draft);paths={draft}
 for b in d['sourceBindings']:
  p=G/b['path'];assert info(p)==b,b['path'];paths.add(p)
 reg=read(R/'data/director/spell_review/accepted_interface_registry_03.json');used={x['id'] for s in d['spells'] for x in s['inheritedInterfaces']}
 def bindings(x):
  if isinstance(x,dict):
   if all(k in x for k in ['path','bytes','sha256']):yield {k:x[k] for k in ['path','bytes','sha256']}
   for v in x.values():yield from bindings(v)
  elif isinstance(x,list):
   for v in x:yield from bindings(v)
 for e in reg['entries']:
  if e['id'] in used:
   for b in bindings({'current':e['currentAuthoritativeSource'],'acceptance':e['acceptanceBasis']}):
    p=G/b['path'];assert info(p)==b,b['path'];paths.add(p)
 paths.update(A/n for n in ['DAMAGE_CONTROL_25_DIGITAL_AUTHORING_CHECK_01.json','DAMAGE_CONTROL_25_HISTORY_RECONCILIATION_02.json','DAMAGE_CONTROL_25_HISTORY_RECONCILIATION_CHECK_02.json','DAMAGE_CONTROL_25_CASE_MIGRATION_CHECK_03.json','DAMAGE_CONTROL_25_CONFERENCE_OPTIONS_CHECK_04.json','DAMAGE_CONTROL_25_HIGH_RANK_CHECK_05.json','DAMAGE_CONTROL_25_NAMED_LIFECYCLE_CHECK_06.json','ACTIVE_AUTHORING_CHECKPOINT_DE4_CONFERENCE_NEXT25_02.json','DE4_DIGITAL_CONFERENCE_05_SUBMISSION_RECEIPT.json'])
 paths.update(R/'tools'/n for n in ['author_damage_control_25_digital_02.py','reconcile_damage_control_25_history_02.py','migrate_damage_control_25_cases_03.py','complete_next25_conference_options_04.py','complete_next25_high_rank_vectors_05.py','complete_next25_named_lifecycle_06.py'])
 paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix())
 summary='''# Next25 damage/control — full source conference 06

This is a pending25-identity/26-placement authored cohort. Nothing in this archive promotes a spell or changes the accepted465/383 count. AC6 remains closed. This packet is independent preparation while the Director completes DE4; it does not infer or preempt DE4 acceptance.

## Read order and precedence

1. MANIFEST.json gives every exact file and hash.
2. `files/DescentReviewChanges/ReviewBible/data/director/spell_proposals/damage_control_25_current_06.json` is the CURRENT candidate. Its25 complete `spells` embed all source records and actual class access. For18 restored spells, `procedure.completeText` is the entire older authored proposal, with explicit narrow digital/current extensions where identified. The seven high-rank records use their structured procedure plus `sharedRules`. These are all unaccepted choices.
3. Every one of the six original full proposal files is supplied, preserving18 complete older authored procedures, shared proposals and36 original examples. Earlier Current01's shorter alternatives remain in `previousStructuredAlternative01` and complete earlier draft files as history. They do NOT replace current restored procedures.
4. `currentDigitalVectors` maps all36 original scenarios to explicit source-linked casting/expected states. `highRankCurrentVectors05` adds15 casting/branch examples for the seven new cards. `currentCases` retains10 additional cases (seven raw arithmetic plus three cross cases). `mixedDefenseOptionVectors04` supplies three separate unadopted option vectors. These sets overlap in purpose and must not be summed into a claim of independent full game tests. No game runtime executed.
5. Registry03 and semantic delta02 identify current accepted interfaces, including Ready, actual Globe rank/origin, both Nexus schools, damage/Null/zero, companion and clocks. Full authoritative files and exact acceptance evidence for used registry entries are included. The old physical-dice/two-spell Fate wording in unchanged accepted files is historical/current pre-DE4 adoption; use the separately reviewed DE4 disposition only after it actually arrives and is integrated.

## Director conference decisions

Please give a substantive disposition for all25 procedures plus each of the nine `conferenceDecisions`, using AGREE, AGREE_WITH_SCOPED_AUTHORSHIP or CHANGE_REQUIRED with exact pointers and replacement text. Preserve all original scenarios and class-school access. Do not repeat already supplied class/header arithmetic as a substitute for the source-specific choices.

- **ICE:** Freezing Sphere has a full existing proposal: original exposed water top1ft, conserved actual water/ice lot, exclusions/clearance, actual support,5x5 section fallbackAC12/HP20/load500lb, fire melt fraction, shared contaminants/custody/source lifetime and elapsed thaw. Review this whole proposal, not the obsolete assumption that it has no physical rules. Remaining concrete questions are deterministic clearance routing without invented tunnels, geometry/support after partial melting/breakage, split/HP rounding without material or HP duplication, and slip regular-cycle/extra-turn timing. Provide a bounded complete engine behavior; do not turn it into generic worldwide material physics or remove the original promise to freeze water.
- **MIXED DEFENSE:** `mixedDefenseConferenceOption04` proposes exact rational proportional allocation with largest fractional remainder and canonical-type tie-break, ONLY for Meteor Spear. It preserves ordinary class flatDR before resistance and actual Warrior Spinal Plating after resistance. Three vectors use actual Warrior Brutal Fortitude, Adaptive Tissue and Spinal sources. This option is explicitly NOT integrated into Meteor's procedure yet. Decide it, or replace with another complete deterministic scoped allocation. Do not silently grant multiple flat defenses or stage stacking.
- **MENTAL BOMB:** restored trigger after a perceived hostile within20ft completes an Action/BA/Reaction; INT;20ft sphere of perceived enemies; finite next-elected legal Reaction debt, real chosen entitlement including special reactions, no charge for the prevented operation, earliest existing debt retained, no rewind of completed trigger. Do not reinstate obsolete Current01 damage-only trigger/WIS/refresh-cancel alternative without an explicit new source decision.
- **PHANTOM SWARM:** restored20ft all-creature sphere, WIS,5d6psychic,30ft real movement budget away from fixed original center. Current finite original START/owner phase/no-schedule expiry and source-plane clauses are new proposals parallel to DE4, not automatic inheritance of a pending rule.
- **HORRID ALIAS:** same identity and two placements remain; Action/range30/instantaneous/V,S,F metadata only is proposed from the two explicit same-effect historical Abi-Dalzim rows. Review alias mapping, cube orientation/range, CON half and actual class-school access separately.
- **GEOMETRY:** preserve Meteor60x5x5 prism, Cone diameter=d at axiald, Sunbeam60x5 cylinder, Destructive Wave self60 sphere, other specified source shapes; review digital closed-body/LoE/snapshot predicates and seven new high-rank choices without a generic shape substitution.
- **CHAIN:** primary has real60ft range, up to three independently selected/perceived secondary recipients within30ft of actual primary, full shared10d8, independent defenses. New primary-operative-payload prerequisite versus mere immunity/damage reduction and primary as authorized arc origin need an explicit decision. Caster remains damage dealer. No random Chain Arc or recursive arcs.
- **OTHER VALUES:** review all original NEW choices and seven new high-rank completions; examples include Blight10d8 plant branch, Destructive Wave10d6 thunder OR radiant, Solar/Sunbeam actual visual rider gates, separate Illusion repeat-save/control behavior, Wail self inclusion and hard guard, Elemental independent10d10 pools and bounded type selection, high-rank blindness endpoints. Do not infer immunity, souls, sunlight, objects, planes or resources from titles.
- **LANCE RECIPIENT:** Current06 supplies a specific correction to the prior ambiguous after-damage body phrase. Push rechecks the original existing creature; living unconscious0HP is eligible. A truly ended creature identity does not silently retarget its corpse/object. No new death rule. HR04-B branchB explicitly isolates an already-known actual death result. The new HR04-C supplies the actual Ranger16 Beast source (HP36, AC14, save+5, acquired card and paid bond), compares ordinary42fire death/corpse with Null Disabled0 preserving the same animal/bond, and tests the proposed20ft push only for the continuing creature. The earlier composition vector remains preserved and is no longer the only death comparison.

The source bindings, ordinary casting examples and direct numeric/geometry checks passed as recorded. Legal input fixtures do not prove engine execution or a full character build/acquisition event; body/defense/knowledge premises are stated. Keep semantic agreement, final rebound-file acceptance, implementation, runtime execution, gameplay, numerical balance, cosmology and release separate. No information was deleted. Please identify actual blocking cases or necessary exact source repairs, and give the candidate hash reviewed. Do not accept unseen later integration files.
'''
 root.mkdir();(root/'README.md').write_text(summary,encoding='utf8',newline='\n')
 manifest={'id':'DAMAGE-CONTROL-25-CONFERENCE-06','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(draft),'files':[info(p) for p in paths],'readme':info(root/'README.md'),'counts':{'identities':25,'placements':26,'restoredOriginalProcedures':18,'newHighRankProcedures':7,'originalScenariosPreserved':36,'currentOriginalScenarioVectors':36,'highRankSupplementalVectors':15,'otherCurrentCases':10,'separateMixedOptionVectors':3,'boundCurrentCandidateSources':46},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 (root/'MANIFEST.json').write_bytes(encoded(manifest))
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(root/'README.md','README.md');z.write(root/'MANIFEST.json','MANIFEST.json')
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for b in manifest['files']:
   raw=z.read('files/'+b['path']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
 b=info(zp)
 message=f'''Next25's consolidated full source conference is ready. Attached DD_Damage_Control_25_Conference_06.zip ({b['bytes']} bytes; SHA-256 {b['sha256']}). Please read README.md and MANIFEST.json, then Current06. It supplies25 identities/26 placements,18 restored complete historical authored proposals and all36 original scenarios, seven new high-rank proposals with15 supplemental casting vectors, current accepted-interface sources, and explicit scoped options. All earlier alternatives/history remain preserved; Current01 alternatives are not governing choices. No new spell acceptance or runtime execution is claimed.

Please review every complete procedure and the nine conference decisions: actual ice physical behavior; Meteor mixed-defense allocation; Mental Bomb reaction debt; Phantom Swarm finite movement; Horrid metadata alias; source-specific geometry; Chain Lightning primary/arc locus; all other original/new values; and Lance creature identity after damage. The README gives concrete unresolved edges and exact current field names. Return source-linked AGREE / AGREE_WITH_SCOPED_AUTHORSHIP / CHANGE_REQUIRED with precise pointers and replacement text. Keep settled AC6 closed. Apply DE4 only to the extent of your actual completed disposition, never as inferred acceptance of unseen final files. Separate semantic agreement from final exact adoption and every runtime/gameplay/balance/canon/release gate. The owner asks continued substantive development until20% allowance remains.'''
 req.write_text(message,encoding='utf8',newline='\n');prep.write_bytes(encoded({'archive':b,'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared; not yet submitted. Do not interrupt the active DE4 conference.'}));print(json.dumps(read(prep)))

if __name__=='__main__':main()
