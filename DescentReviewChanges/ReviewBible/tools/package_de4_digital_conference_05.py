"""Freeze the complete pending DE4 cohort and exact proposed amendment for GPT."""
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 root=A/'de4-digital-review-05';zpath=A/'DD_DE4_Digital_Conference_05.zip';req=A/'DE4_DIGITAL_CONFERENCE_05_REQUEST.txt';prep=A/'DE4_DIGITAL_CONFERENCE_05_PREPARATION.json'
 assert not any(p.exists() for p in [root,zpath,req,prep])
 draft=R/'data/director/spell_proposals/divination_enchantment_rank4_current_05.json';d=read(draft);guard=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_03.json';g=read(guard)
 paths={draft,guard}
 for b in d['sourceBindings']+g['sourceBindings']:
  p=G/b['path'];assert info(p)==b,b['path'];paths.add(p)
 for row in read(A/'de4-digital-conference-05/PRESERVATION_MANIFEST.json'):
  for key in ['source','preservedCopy','proposedCopy']:paths.add(G/row[key]['path'])
 paths.update(A/n for n in ['de4-digital-conference-05/PRESERVATION_MANIFEST.json','DE4_DIGITAL_CONFERENCE_CHECK_05.json','DE4_SOURCE_REFERENCE_CHECK_04A.json','DE4_DIGITAL_FIXTURES_CHECK_04.json','AC6_REGISTRY_INVENTORY_REFRESH_03_CHECK.json','AC6_APPLIED_DE4_04A_NAVIGATION_CHECK.json','ACTIVE_AUTHORING_CHECKPOINT_AC6_APPLIED_DE4_04A.json','AC6_EXACT_ACCEPTANCE_06_APPLICATION_CHECK.json','DIRECTOR_LATEST_CHANGES_2026_10_17_VERIFIED_NATIVE.json'])
 paths.update(R/n for n in ['tools/prepare_de4_digital_conference_05.py','tools/correct_de4_source_references_04a.py','tools/prepare_de4_digital_fixtures_04.py','data/director/spell_review/accepted_interface_registry_03.json','data/director/spell_review/ordinary_spell_inventory_02.json','docs/DEVELOPMENT_DIRECTION.md','data/playtest/game_development_coverage.json'])
 paths.add(G/'START_HERE.md');paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix())
 summary="""# DE4 complete pending digital cohort — conference 05

Thank you for the completed AC6 handoff verification. AC6 remains closed and unchanged. Registry03 now indexes 78 accepted interfaces (49 unchanged plus 29 scoped AC6 entries); inventory02, START_HERE, development direction, review map and coverage checkpoint now say 465 reviewed / 383 pending. The narrow DE4 Wizard evidence repair is complete: N24 engine/9, N25 engine/9 and engine/11. No DE4 identity is accepted yet.

## Read these current candidates

- `files/DescentReviewChanges/ReviewBible/data/director/spell_proposals/divination_enchantment_rank4_current_05.json`: all 15 complete pending procedures, all 30 original texts, all 30 preceding current cases, and four added current vectors N31–N34. The 82 bound source files are supplied in full. Original/historical fields are evidence; `procedure`, `sharedRules` and `currentExamples` are the proposed current rules/cases.
- `files/docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_DRAFT_03.json`: exact unadopted transformations for nine active files. It extends the common guard to Fate Reversal and explicitly converts physical-dice restrictions to engine RNG under the owner's directive. Exact current before copies and proposed text copies are included. Proposed copies still have pre-application dependency metadata: they are reviewable text transformations, NOT a claim of already rebound live adoption.
- `files/docs/audit/2026-10-08/full-game/DE4_DIGITAL_CONFERENCE_CHECK_05.json`: 363 passed checks of preservation, exact source bindings, pointers, proposed reversible changes and direct vector arithmetic. No game runtime executed. The earlier 331 fixture checks and 306 evidence-repair checks have their own narrower scopes.

## Conference decisions requested

1. **DE4-GUARD-01 and DE4-RNG-05:** Explicitly decide the three-spell common lineage, legal commitment, per-source spend, whole-d20 versus one-component replacement, shared damage pool, independent class rerolls, stable simultaneous ordering, and hidden RNG protection. Digital conversion is owner-directed. The proposal intentionally requires an existing source-specific gameplay-visibility grant and does not expose hidden rolls merely because the engine knows them. If this leaves a material original source without a usable presentation policy, identify the exact source/event and recommend a bounded decision; do not quietly approve an undefined visibility policy. The in-world Coin remains a physical item; the random die is an engine operation. N31/32 test shared component/hidden cases, N34 retains an accepted Nexus modifier snapshot.
2. **DE4-SEAL-LOCI-02:** Decide actual body/expression locus, pending operator suppression versus a paid operative attempt against a protected generating event, same physical Coin custody, and the explicit same-family exemption. Seal's proposed school predicate has no rank ceiling. Current05 now compares accepted AC6 Globe and both actual Nexus schools. N33 distinguishes rank4 outside/inside Globe origin, Divination6 local insight suppression, and Conjuration8 remaining outside Seal's school predicate. Do not rewrite accepted AC6.
3. **DE4-ORDER-DELIVERY-02 / DE4-COMPULSION-EXPIRY-03:** Decide same-plane new mental orders versus already-delivered instructions; source-plane fixed Compulsion direction; finite original latest opportunity, expiry after the one eligibility check, actual attached phase versus expiry-only bookkeeping, and disabled/no-schedule companions. N24 retains real Tinker protected vent and Field Repair with no manufactured action, command, recharge or retry.
4. Review the remaining complete DE4 procedures against supplied sources: genuine class access, score/stat timing, Mass Pacify's deliberate attack-only scope, faction/alignment/information boundaries, all regular/attached END save bridges, and Phantasmal Killer's separate school/Null-root/exposure branches. State exact remaining defects and minimal corrections, retaining all original scenario obligations. No tabletop convenience redesign.

## Response format

Please inspect the actual archive/manifest and return a source-linked decision record for these points and the full pending cohort. For each use AGREE, AGREE_WITH_SCOPED_AUTHORSHIP, or CHANGE_REQUIRED; cite precise current JSON pointers/case IDs and replacement text for a required correction. Distinguish agreement on an authored proposal from final exact adoption with rebound dependency metadata. If no semantic blocker remains, identify the exact candidate hashes you reviewed and any remaining mechanical integration requirements. Do not infer acceptance of unseen final files.

N31 is an isolated RNG-composition vector with a declared already eligible shared 3d6 event; it is not a new damage spell or claim of class acquisition. N33 likewise tests existing lawful parents; it does not claim to execute their setup costs. Report if fuller real-source end-to-end vectors are needed for a specific behavior.

The old AC6 pending-source audit and old two-spell/physical-dice wording are retained as history. Current05's acceptedAC6DependencyRefresh05 and current proposed digital contract control this review. No source information has been deleted. Authored acceptance, runtime implementation/execution, human gameplay, numerical balance, canon and release remain separate. Latest GitHub backup c1e2b7d predates these local changes. The owner requests continued work until 20% account allowance remains; this is a work stop rule, not a new design constraint.
"""
 root.mkdir();(root/'README.md').write_text(summary,encoding='utf8',newline='\n')
 manifest={'id':'DE4-DIGITAL-CONFERENCE-05','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'currentCandidate':info(draft),'proposedAmendment':info(guard),'files':[info(p) for p in paths],'readme':info(root/'README.md'),'counts':{'pendingCohortIdentities':15,'currentCases':34,'preservedOriginalTexts':30,'currentSourceBindings':82},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
 (root/'MANIFEST.json').write_bytes(encoded(manifest))
 with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(root/'README.md','README.md');z.write(root/'MANIFEST.json','MANIFEST.json')
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for b in manifest['files']:
   raw=z.read('files/'+b['path']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
 b=info(zpath)
 text=f'''The owner asks us to keep focused development going until 20% allowance remains. Thank you for verifying the previous handoff. I completed registry03 (78 entries), inventory02, current navigation and the Wizard source-reference repair. AC6 remains closed at 465 reviewed / 383 pending.

Attached is DD_DE4_Digital_Conference_05.zip ({b['bytes']} bytes; SHA-256 {b['sha256']}). Read README.md and MANIFEST.json, then the complete DE4 Current05 and exact unadopted Fate amendment03. All 15 procedures, 30 original texts, 34 current cases, 82 bound sources, accepted AC6 interfaces, and nine before/proposed text representations are supplied. 363 local checks passed; no game runtime or live rule adoption is claimed.

Please now perform the substantive full-cohort conference you identified: (1) three-spell Fate guard plus explicit engine RNG/player-information mapping, (2) Seal Vision loci/paid block/same-family exemption with accepted Globe/Nexus, (3) control delivery and finite Compulsion opportunities, and (4) remaining individual DE4 procedures and cases. Give explicit source-linked dispositions and exact minimal corrections where needed. Keep settled AC6 closed absent a concrete contradiction. Proposed amendment copies are exact text proposals with current pre-adoption dependency metadata; distinguish semantic agreement from final rebound-file acceptance. The README states the boundaries and two composition-only vectors honestly. Do not approve hidden RNG exposure, undefined source visibility or unseen final files. Preserve the video-game-only direction.

I will refresh/develop next25's source-linked exceptions while you review this packet.'''
 req.write_text(text,encoding='utf8',newline='\n');prep.write_bytes(encoded({'archive':b,'manifest':info(root/'MANIFEST.json'),'request':info(req),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared; submission not yet claimed'}));print(json.dumps(read(prep)))

if __name__=='__main__':main()
