"""Enumerate proposed per-row work; this does not prove current runtime admission safety."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
inventory=json.loads((HERE/'API_CONSUMERS.json').read_text(encoding='utf-8'))
groups={
 'shared-origin':(
  'AbilityCheckRules ActorLifeRules CharacterRuleFacts PlaytestDamageDice ActorLifeRecords ActorLifeCodec',
  'Introduce/validate disjoint source-qualified origin for shared ability/life/AC/check paths. Retain real character level/PB API; absent creature PB is unavailable. For untrained checks only, no proficiency entry contributes zero. Never synthesize a character.',
  'Creature target/observer/life checks with no class record; missing/both/forged origin rejection; genuine untrained modifier; generic affected-PB Bleeding unsupported before cost/RNG.'),
 'mixed-character-shared':(
  'SharedCharacterAdvancement CharacterAdvancementRecords',
  'Generalize shared AC/armor-strength-speed and ordinary save contributions. Preserve character-only levels, HP growth, class grants, owner PB, training and equipment entitlement. Register the exact new epoch for existing owned recharge without resetting at admission.',
  'AC10 despite DEX+2; no fabricated PB; ordinary CON+2/WIS0; actual party source bonus retained; fake creature loadout/grant rejected before lookup; no duplicate recharge.'),
 'target-combat':(
  'TestOnlyClubAttackPolicy SharedWorldRangedCombat SharedOverwatchExecution SharedFrightened SharedHuntingTrap SharedPeriodicRider SharedSanctuary SharedSpellEffects',
  'Generalize actual target/attacker ability, AC and life facts where the actor may be the creature. Source-owner class/attack DC PB remains the genuine trained owner PB; creature own attack+3 is independent. Route creature save checks through untrained contributions, not character lookup. Preserve explicit source/target/roster gates for unselected producers.',
  'Incoming attacks/target saves and typed defenses; Sanctuary creature WIS0; source-owner DC unchanged; fixed Bleed versus unsupported generic affected-PB application; held weapon/Overwatch/fear source ownership cannot be acquired by Wraith.'),
 'owned-class':(
  'ConnectedCastingView SharedBishopEntry SharedClericSettlement SharedDivineInvocation SharedResonance SharedSpellCasting SharedSpellRepertoire ClericSettlementValidation ResonanceRecords',
  'Retain actual Cleric character owner, earned levels/cards, caster PB, repertoire, Dissonance formula and finite pools. Generalize allowed recipient living/type/AC/save facts separately. Explicitly register the new admitted epoch without broadening source grants or casting contexts.',
  'Creature cannot cast or gain class/recharge resources; source-owner formulas unchanged; eligible party Rite/Invocation/casting in new epoch; Ferry living-recipient rejection before cost/RNG; target-side legal effects reach shared creature state.'),
 'shared-observer-session':(
  'ConnectedExpeditionView SharedObservationActions SharedCompanionStabilization SharedRetreat LaterEncounterRecords',
  'Use the proper actor origin for shared displayed life, perception/initiative/saves and supported target interactions. Preserve exact party, retreat-profile and trained-worker/source permissions. New epoch/seat/closure uses its own records; old classifiers remain versioned.',
  'Creature own WIS0/DEX+2, filtered facts and ordinary permissions; no hidden source/type leakage; early creature-specific unsupported paths return before character access; authentic old context results unchanged.'),
 'old-fixture-character':(
  'PeriodicRiderFixture PlaytestCharacterBuild PlaytestCharacters RangedAttackResolution SharedLaterEncounter SharedPostRecoveryEncounter SharedWorldDefinitions PostRecoveryEncounterValidation RangedCombatRecords RangedCombatCodec',
  'Retain exact old character fixture/build/weapon-source producers and their actual proficiency inputs. New genesis must use a separate creature origin/source-attack path; never reuse human defender construction or a forged ranged PB. Validators must allow the new union only in its selected version while validating each old record against its real owner.',
  'Authentic old saves/views/continuations; reject creature ID substituted into an old character producer/record; genuine new actor has no class/club/ranged PB; strict new genesis union validation.'),
 'party-work-source':(
  'SharedConsumeDecay SharedCraftingConsequences SharedExpeditionEpisodeClose SharedExpeditionRouteMappingWork SharedExpeditionRouteReconnaissance SharedFishingTrap SharedFleshWarden SharedFormulaResearch SharedHarvest SharedHarvestPreservationTreatment SharedHavenSale SharedManufacturing SharedMining SharedMiningAssay SharedOrdinaryReceptacle SharedProspecting SharedRecipe347 SharedSupplyCache SharedTemporaryCampConstruction SharedToolRepair SharedWoundTreatment FleshWardenRecords',
  'Retain real party/worker/source-owner selection, trained skill rank, equipment/work/ingredient/custody and supported profile gates. Creature origin alone grants none. Verify each user-reachable entry point rejects an unsupported creature owner before character-only numeric lookup; generalize a legal creature target independently when the existing source actually admits it.',
  'Wrong creature worker/caster/source attempts leave state, reservations, Action and RNG unchanged without throwing; genuine party work outputs and historical record validation stay exact; no generic physiology or free skill grant.'),
 'character-work-wire':(
  'ExpeditionRouteMappingWorkRecord FishingTrapRecords HarvestPreservationRecords HarvestRecords MiningAssayRecords MiningRecords ProspectingRecords RouteReconnaissanceRecords TemporaryCampConstructionRecords ExpeditionRouteMappingWorkCodec ExpeditionRouteReconnaissanceCodec FishingTrapCodec HarvestCodec HarvestPreservationTreatmentCodec MiningAssayCodec MiningCodec ProspectingCodec TemporaryCampConstructionCodec',
  'Preserve serialized historical trained-worker contribution fields and validate their actual source producer/owner. A stored zero proficiency contribution does not create a creature PB. No new creature worker, source or record migration is admitted by this contract.',
  'Old bytes and worker-derived checks unchanged; forged owner/proficiency/history rejected; creature requests fail before creating these records.'),
 'fear-source-wire':(
  'FrightenedRecords',
  'Keep old Warrior Intimidating Presence grants, ability choice and caster DC source owner. Integrate lawful affected-creature ability/life and exact new epoch for existing carried/repeat effects without granting Wraith a Warrior source.',
  'Real target WIS and condition timing; no copied fear source; causal grant/owner and original deadline checks across new epoch.'),
}
lookup={}
for group,(names,work,control) in groups.items():
 for name in names.split():
  assert name not in lookup,name
  lookup[name]=(group,work,control)
rows=[]
for kind in ['numeric','proficiency']:
 for row in inventory['searches'][kind]['rows']:
  name=Path(row['path']).stem
  assert name in lookup,('Unassigned consumer',name)
  group,work,control=lookup[name]
  for hit in row['hits']:
   rows.append(dict(inventory=kind,path=row['path'],line=hit['line'],text=hit['text'],category=group,requiredDisposition=work,requiredControl=control,status='PROPOSED_IMPLEMENTATION_WORK_NOT_EXECUTED'))
assert len(rows)==inventory['searches']['numeric']['matchedLines']+inventory['searches']['proficiency']['matchedLines']
extra=dict(id='generic-affected-creature-PB-Bleeding',source='DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md#bleeding',requiredDisposition='Application Unsupported unless a separately reviewed source supplies magnitude; no creature PB0, no inferred PB and no immunity claim.',requiredControl='No cost/RNG/condition record on generic application; source-specific fixed magnitude remains a separately qualified source.')
result=dict(status='COMPLETE_ENUMERATION_OF_PROPOSED_NUMERIC_AND_PB_WORK',generatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),inventorySha256=hashlib.sha256((HERE/'API_CONSUMERS.json').read_bytes()).hexdigest(),files=len({r['path'] for r in rows}),inventoryRows=len(rows),uniqueSourceLines=len({(r['path'],r['line']) for r in rows}),sourceOnlySupplement=extra,rows=rows,limits='Every matched numeric/PB line is assigned. Categories prescribe work and controls; they do not establish that existing gates already suffice. Implementation must inspect indirect calls, reconcile actual changed/unchanged boundaries and execute controls. Other inventory families remain governed by the complete contract.')
(HERE/'CONSUMER_DISPOSITIONS.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps({k:v for k,v in result.items() if k not in ['rows','sourceOnlySupplement']}))
