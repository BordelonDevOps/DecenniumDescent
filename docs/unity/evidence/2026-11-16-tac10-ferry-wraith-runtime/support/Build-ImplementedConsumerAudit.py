"""Bind each approved numeric/PB inventory row to its implemented source disposition.

This is static audit evidence, not a substitute for executed gameplay or final review.
"""
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PACKET = HERE.parent
BASE = 'e7f7ac179170e491f2e628f46de4441165551f12'
CURRENT = 'c8ffee78d5047131317ff923c8e3a575b6c51f3a'
INVENTORY = PACKET.parent / '2026-11-16-tac10-undead-amended-contract/CONSUMER_DISPOSITIONS.json'

# File-specific conclusions from inspection of the producer, consumer and admission paths.
NOTES = '''
AbilityCheckRules.cs|Snapshot checks route through CharacterStateFacts.DeriveCheck and ActorNumericFacts. Overloads explicitly accepting ActorCharacterRecord or CharacterRuleFacts remain character-only. No proficiency entry gives rank0 contribution0; this is not a creature PB value.
ActorLifeRules.cs|The inventoried rows are the earlier TestOnlyActorLifePolicy genesis/character validator. That policy constructs only its fixed character roster. Shared life settlement uses ActorLifeRecord and does not synthesize a class for Ferry.
CharacterRuleFacts.cs|Real character class/level/PB formulas remain unchanged. CharacterStateFacts now holds disjoint ActorNumericFacts plus optional real character; generic check/injury operations use Numeric. Character and Rules require a real character and remain unavailable for the creature.
PlaytestDamageDice.cs|PrototypeArmor.UnarmoredBaseAc(int dexterity) accepts a DEX score and derives its modifier internally; there is no CharacterRuleFacts overload. Shared ArmorClass branches to printed creature AC before calling the character unarmored formula. Damage settlement receives the resolved CON modifier rather than inventing a class.
ActorLifeRecords.cs|Origin validation now requires exactly one character-or-creature origin per actor and one shared life record. Creature origins are restricted to selected Ferry. The character-only maximum-HP formula remains on the character branch.
ActorLifeCodec.cs|The historical character array retains its exact old field layout and level encoding. Creature data is appended separately by FerryWraithCodec; no dummy character or old-wire insertion occurs. Shared life records remain separate from both origins.
ConnectedCastingView.cs|Casting projection computes class level/PB only for the actual owned Cleric actor and repertoire; Ferry receives no casting projection or class facts.
SharedBishopEntry.cs|Entry entitlement and milestone conditions bind the existing Cleric character. These checks remain class-specific and do not make creature origin an eligible Bishop candidate.
SharedClericSettlement.cs|Healing Rite/Radiance ownership is checked before class formulas. Existing Cleric resource entitlement remains exact; only the registered Ferry epoch extends the owned turn context.
SharedDivineInvocation.cs|AssessDivineInvocation first requires ClericRpProfile.Actor, earned Bishop, the valid feature grant and Radiance ownership; only then reads the actual character to derive the pool. New epoch is read from WorldTiming for the already-owned use; no creature Invocation grant.
SharedResonance.cs|Pool, grounding and class formulas remain owned-Cleric operations. LivingRecipient rejects the printed nonliving Ferry source. Own-turn recognition adds the exact Ferry epoch and preserves the old contexts; this is not arbitrary encounter eligibility.
SharedSpellCasting.cs|Caster class/PB/DC formulas retain actual repertoire, feature ownership and selected spell gates. CurrentCastingTurn/End processing explicitly recognize the Ferry epoch. Sanctuary source continuation preserves the full creature feature payload; target-save numerics remain separate from caster ownership.
SharedSpellRepertoire.cs|Known-spell capacity/selection remains attached to the real Cleric character and its earned level. The creature acquires no repertoire.
ClericSettlementValidation.cs|Historical owned Rite/Radiance records accept the registered Ferry epoch with its exact first-turn origin. Existing class/source/actor validation remains; no universal epoch allowance or class conversion.
ResonanceRecords.cs|Stored resonance maximum remains derived from the actual Cleric level and validated grant; the creature has no resonance pool.
ConnectedExpeditionView.cs|The inventoried Cleric level lookup is tied to the owned Cleric actor. Ferry display and command availability use its separate actor/seat. Corrected host projection and five-path evidence compare populated four-seat views.
SharedCompanionStabilization.cs|The medicine check uses shared numeric/injury facts, after actual actor/target, current-turn, dying-target, hand, Action and stationary-access checks. It does not derive target PB or grant the creature hands.
SharedObservationActions.cs|Hide/Search and passive perception use CharacterStateFacts generic checks, which now consume ActorNumericFacts. Real training records remain separate; an untrained creature receives only its ability/injury modifiers.
SharedRetreat.cs|The retained authored retreat lead's task uses shared numeric/injury facts after AssessRetreatInstruction. This adds no Ferry retreat source or roster entitlement.
LaterEncounterRecords.cs|WorldTiming explicitly resolves the selected Ferry epoch/participants and preserves prior epoch identity. Old LaterDefender character profile validation remains fixed to that character; shared calendar registration is not a class grant.
PeriodicRiderFixture.cs|Earlier explicit fixture character facts remain in its own selected source factory. Ferry registration does not reuse that factory to assign levels or generic Bleeding magnitude.
SharedLaterEncounter.cs|Old later-defender genesis still creates its real character. Shared initiative now takes DEX through Numeric; closure recognizes the exact Ferry record. Old character construction is not run for Ferry.
SharedPostRecoveryEncounter.cs|Recovery-defender character genesis remains unchanged. Advancing the historical recovery calendar skips actors whose current owner is Ferry, preventing duplicate Ends/Starts and preserving inherited intervals.
SharedWorldDefinitions.cs|Configured world actors are authored real characters. Worker rosters derive from that original configuration, not the later appended Ferry actor. No creature is inserted into class/training/work definitions.
PostRecoveryEncounterValidation.cs|Old defender source validation stays character-specific. Current participant ownership switches only after actual Ferry admission; earlier records cannot claim the new epoch and the old closed encounter remains valid.
RangedCombatRecords.cs|The explicit ranged actor profile retains real ability/level facts and its old schema validation. Ferry Claw has a distinct printed source and does not become a ranged-profile character.
PlaytestCharacterBuild.cs|Character creation accepts class/level selections explicitly. This is not a generic actor factory and is not used for source-creature initialization.
PlaytestCharacters.cs|Character HP/level/PB formulas remain explicit character utilities. ActorNumericFacts refuses to call the PB formula for a creature; printed source HP and AC bypass these character formulas.
RangedAttackResolution.cs|These overloads accept explicit ranged character facts/modifiers. Shared target derivation was changed at the shared caller; printed Claw uses its own source path rather than this character ranged source.
RangedCombatCodec.cs|Historical ranged-character profile serialization remains byte-stable; creature source serialization is an additive separate record.
SharedCharacterAdvancement.cs|Shared AC checks creature origin first and returns printed AC. Save proficiency remains from actual initial loadout/class entry, otherwise no proficiency entry contributes0. Equipment-strength penalty requires actual worn chainmail, absent from Ferry genesis. Level, feature and HP advancement remain real-character operations. Named Invocation recharge transfers only to the registered new epoch without granting a fresh use.
CharacterAdvancementRecords.cs|Most rows validate actual character growth/loadout/feature ownership. The shared BonusAction ledger membership now uses Actors, so nonclass actors may carry the ordinary ledger without acquiring a character feature. No level/PB record is synthesized.
SharedConsumeDecay.cs|Resolve binds the fixed ConsumeDecaySite actor/source and current context before the character-level row. Ferry receives no Consume Decay entitlement.
SharedCraftingConsequences.cs|The selected occurred mishap binds the authored LeadId/target. Its damage/check character is the actual work lead; Ferry is not an authored work participant. Selected typed combat defenses do not invent a new crafting producer.
SharedExpeditionEpisodeClose.cs|Award admission explicitly requires each charter member to have a Character record as well as Actor/Life/Condition state. Existing character awards cannot become creature advancement.
SharedExpeditionRouteMappingWork.cs|RouteMappingWorkSelected enumerates its earlier schemas and excludes Ferry114. Worker checks/results remain associated with that selected lead/assistant source. Shared skill calculation itself now uses numeric facts; no new creature route-work source is introduced.
SharedExpeditionRouteReconnaissance.cs|RouteReconnaissanceSelected accepts the explicit reconnaissance or daily-provisioning schemas, excluding Ferry114. The existing actual lead/cohort and source result records remain intact.
SharedFishingTrap.cs|Genesis changes apply only to the selected real setter. Actual operations use profile.SetterId or existing owned jobs/handovers; continuing labor requires at least two available hands. Ferry has no granted hands, training or trap job.
SharedFleshWarden.cs|Mutation capacity and base-HP formulas bind FleshWardenProfile.Actor and its actual growth. There is no arbitrary creature recipient or new class entitlement.
SharedFormulaResearch.cs|ResearchAccess requires research.WorkerId, actual trade qualification, tools and access before the Rules/PB lookup at completion. Generic creature research remains unsupported.
SharedHarvest.cs|HarvestAccess checks IsHarvestWorker against the configured worker roster before checks or consequences. The later appended Ferry is absent from that roster and has no harvest source/manifest. Character-only accident CON and stored proficiency remain confined to the admitted workers.
SharedHarvestPreservationTreatment.cs|The ordinary branch requires selected preservation schemas, a scheduled TestOnlyPolicy.ActorId worker and actual cooking training; BloodSpecimen has its separately bound producer. No new Ferry treatment source is selected.
SharedHavenSale.cs|The inventoried row creates the fixed real buyer character in trusted genesis. It is not a shared target calculation and does not create character facts for Ferry.
SharedManufacturing.cs|ManufacturingAccess requires TestOnlyPolicy.CompanionId and the actual trade/formula/tool/access source before Rules/PB completion. Ferry is not an admitted manufacturer.
SharedMining.cs|IsMiningWorker checks the selected assignment WorkerIds or original worldConfiguration actor roster. Ferry is appended separately and is not eligible. Character training/profile and stored check results remain for the admitted work participants.
SharedMiningAssay.cs|Both assay paths use IsMiningWorker and actual source/tool/hand gates before deriving/checking results; no generic creature assay producer exists. Serialized proficiency is the actual worker result, not inferred Ferry PB.
SharedOrdinaryReceptacle.cs|The actual lock OwnerId and physical credential ownership/usable hand gate precede PickCheckModifier. Ferry owns no authored ordinary lock or tool and receives no lock-picking entitlement.
SharedProspecting.cs|IsProspectingWorker uses the explicit prospecting fixture roster, checked by ProspectingAccess before the shared check and stored result. No Ferry worker or training is added.
SharedRecipe347.cs|Recipe347Access explicitly requires TestOnlyPolicy.CompanionId, actual Mining trade/tools and two hands. The Rules/PB completion row remains a real-character source calculation.
SharedSupplyCache.cs|PickCheckModifier deliberately uses a real character; callers require the cache's actual owner and physical tools/hand source. Ferry receives neither the authored cache ownership nor generic tool proficiency.
SharedTemporaryCampConstruction.cs|Assessment requires the configured LeadId and actual trained crew/source. Completion uses the source-bound lead's historical character. Ferry has no camp-construction source, roster membership or training.
SharedToolRepair.cs|RepairAccess checks IsRepairWorker and selected training before Rules/PB, with actual tools and usable-hand gates. The original configured roster excludes Ferry; no inferred repair proficiency.
SharedWoundTreatment.cs|The source fixes WoundTreatmentStation.Healer/Patient and binds both reservations. The healer's medicine check uses shared numeric facts; no new creature treatment entitlement or target source is authored.
FleshWardenRecords.cs|The maximum-HP validator is for the fixed real Flesh Warden character and actual mutation capacity. Printed creature HP remains separate.
SharedFrightened.cs|Feature source remains an actually owned Warrior/later-defender choice with real PB. Target WIS is now ActorNumericFacts; source feature ownership and target numeric origin are not conflated.
SharedHuntingTrap.cs|Setter/puller sources remain admitted real characters. Target DEX/CON uses ActorNumericFacts; selected Ferry damage uses the single typed piercing boundary. No trap source or hands are granted to Ferry.
SharedOverwatchExecution.cs|Source owner/PB and actual ability choices remain character-specific. Target saves use ActorNumericFacts and selected damage uses one typed piercing boundary. Source magnitude is not affected-creature generic PB.
SharedPeriodicRider.cs|Fixed authored applications and ResolveOverwatchRider -> ApplyOverwatchBleed are admitted source-specific periodic producers. The latter requires the selected shooter/target and original calendar; its source-owner PB supplies the DC. Target CON uses ActorNumericFacts and selected damage records the typed boundary. Neither producer supplies generic affected-creature-PB Bleeding; that unsourced application remains Unsupported.
SharedSanctuary.cs|Actual attacking actor WIS uses ActorNumericFacts. Creature regular/OA continuations retain FeatureId and full source payload; owner casting DC remains the original Cleric source. No class/PB is inferred for the source creature.
SharedSpellEffects.cs|Concentration target CON uses ActorNumericFacts and actual save proficiency. Owning spell/source and condition journals remain unchanged.
SharedWorldRangedCombat.cs|Weapon/Suppression/Overwatch owners retain actual character proficiency and features. Target AC/DEX/CON now route through the disjoint source facts; selected damage pays the one typed boundary. Public Ferry Dash and Claw/seal requests have explicit source/party/context gates.
TestOnlyClubAttackPolicy.cs|Printed source Claw is validated before ordinary weapon resolution: +3 and d4 fire, critical2d4, no STR/PB inference or creature fallback unarmed/club attack. Target AC/CON uses source facts. Pending knockout finishes the retained effective damage and prior rolls without reapplying defenses or rerolling damage.
FrightenedRecords.cs|The inventoried class lookup validates the fixed old Warrior source owner and actual choice/grant. Ferry receives no Intimidating Presence; its target save is handled separately by SharedFrightened.
'''
NOTES = dict(line.split('|', 1) for line in NOTES.strip().splitlines())

WIRE_PRODUCERS = {
    'ExpeditionRouteMappingWork': 'SharedExpeditionRouteMappingWork.cs',
    'ExpeditionRouteReconnaissance': 'SharedExpeditionRouteReconnaissance.cs',
    'RouteReconnaissance': 'SharedExpeditionRouteReconnaissance.cs',
    'FishingTrap': 'SharedFishingTrap.cs', 'HarvestPreservation': 'SharedHarvestPreservationTreatment.cs',
    'HarvestPreservationTreatment': 'SharedHarvestPreservationTreatment.cs', 'Harvest': 'SharedHarvest.cs',
    'MiningAssay': 'SharedMiningAssay.cs', 'Mining': 'SharedMining.cs', 'Prospecting': 'SharedProspecting.cs',
    'TemporaryCampConstruction': 'SharedTemporaryCampConstruction.cs',
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(path, revision):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', revision + ':' + path])


def main():
    proposal = json.loads(INVENTORY.read_text(encoding='utf-8-sig'))
    cache, rows = {}, []
    for index, row in enumerate(proposal['rows'], 1):
        path = row['path']
        if path not in cache:
            oldraw, newraw = git(path, BASE), git(path, CURRENT)
            assert newraw == (ROOT / path).read_bytes(), 'Audit source changed: ' + path
            old, new = oldraw.decode('utf-8-sig').splitlines(), newraw.decode('utf-8-sig').splitlines()
            cache[path] = (oldraw, newraw, old, new, difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes())
        oldraw, newraw, old, new, opcodes = cache[path]
        line = row['line'] - 1
        assert old[line].strip() == row['text'].strip(), (path, row['line'])
        opcode = next(op for op in opcodes if op[1] <= line < op[2])
        kind, a, b, c, d = opcode
        start, end = (c + line - a, c + line - a + 1) if kind == 'equal' else (c, d)
        filename = Path(path).name
        if row['category'] == 'character-work-wire':
            stem = re.sub(r'(Records?|Codec)\.cs$', '', filename)
            producer = WIRE_PRODUCERS[stem]
            note = ('Retain the historical work record/codec and its actual stored check/proficiency fields; no shared actor lookup or new creature PB default is added here. Producer: '
                    + producer + '. ' + NOTES[producer] + ' Strict command replay, not field shape alone, authenticates the stored result.')
        else:
            note = NOTES[filename]
        rows.append(dict(id='consumer-' + str(index).zfill(3), inventory=row['inventory'], path=path,
                         baselineLine=row['line'], baselineText=row['text'], category=row['category'],
                         baselineFileSha256=sha(oldraw), currentFileSha256=sha(newraw), fileChanged=oldraw != newraw,
                         mapping=kind, currentStartLine=start+1, currentEndLine=end,
                         currentText=new[start:end], disposition=note,
                         status='STATIC_DISPOSITION_RECORDED_REQUIRES_FINAL_REVIEW'))
    assert len(rows) == 332 and len(cache) == 81
    assert len({(r['path'], r['baselineLine']) for r in rows}) == 329
    indirect_notes = {
        'ActorNumericFacts.cs': 'New shared numeric boundary: exactly one character/creature origin, printed creature facts, nullable unknown PB; rank0 contribution0, positive-rank creature proficiency unavailable. RequireCharacter never fabricates levels.',
        'ClubAttackRecords.cs': 'ArmorClass is an already-resolved attack-roll field; it does not derive or grant target character facts. Exact roll identity remains persisted.',
        'CreatureActorRecords.cs': 'New immutable source-qualified printed creature facts, including AC/HP/abilities/type/defenses; no class, level or PB field.',
        'ClubAttackCodec.cs': 'Retains the existing resolved attack-roll AC field without re-derivation; selected creature source/payload is authenticated by the additive source record and full replay.',
        'FerryWraithCodec.cs': 'Additive114 creature/source/epoch/seal/typed-damage data; historical character and work layouts remain unchanged. Printed AC is serialized as source data, not synthesized from DEX.',
    }
    indirect = []
    pattern = re.compile(r'\b(?:CharacterStateFacts|CharacterRuleFacts|ActorNumericFacts|AbilityCheckRules|PassivePerception|SaveProficiencyBonus|ArmorClass)\b')
    for part in ('Laboratory/Model', 'Runtime/Core', 'Runtime/Persistence'):
        for source in sorted((ROOT / 'engine/com.decennium.foundation' / part).glob('*.cs')):
            path = source.relative_to(ROOT).as_posix()
            if path in cache:
                continue
            hits = [dict(line=i, text=text.strip()) for i, text in enumerate(source.read_text(encoding='utf-8-sig').splitlines(), 1) if pattern.search(text)]
            if hits:
                assert source.name in indirect_notes, 'New unclassified indirect consumer: ' + path
                assert source.read_bytes() == git(path, CURRENT)
                indirect.append(dict(path=path, sha256=sha(source.read_bytes()), matches=hits, disposition=indirect_notes[source.name]))
    assert len(indirect) == 5
    output = dict(status='COMPLETE_STATIC_ROW_RECONCILIATION_PENDING_FINAL_REVIEW', baselineCommit=BASE,
                  runtimeCommit=CURRENT, inventorySha256=sha(INVENTORY.read_bytes()), collectorSha256=sha(Path(__file__).read_bytes()),
                  inventoryRows=len(rows), uniqueSourceLines=329, files=len(cache),
                  changedFiles=sum(a != b for a,b,*_ in cache.values()), rows=rows, indirect=indirect,
                  sourceOnlySupplement=proposal['sourceOnlySupplement'],
                  indirectCallChains=[
                      'AbilityCheckRules/Hide/Search/passive perception -> CharacterStateFacts.DeriveCheck -> ActorNumericFacts; optional real Character/Rules remains class-only.',
                      'Shared target AC/save/initiative/injury -> ActorNumericFacts; source attack/PB/class/gear eligibility remains on its exact existing source.',
                      'Ordinary work assessment -> selected fixed/configured worker roster, source/gear/hands/training -> actual character result -> unchanged work record/codec -> strict full command replay.',
                      'Owned Cleric/Bishop grant -> exact WorldTiming Ferry epoch -> shared costs/conditions/recharge -> existing source record validation; admission grants no resource or recharge reset.',
                      'Source attack -> one typed damage boundary -> shared LifeState -> retained pending knockout Finish; no reroll or second resistance pass.',
                      'Ferry trusted genesis -> CreatureActorRecord plus shared actor/life/condition/movement -> additive114 codec; no Character/training/PB/work/equipment entry.',
                  ],
                  limits='Static source/disposition audit only. Execution is qualified by the retained focused cases, five paths, original corrected regression and authentic compatibility. Source-only unsupported PB application control and any remaining acceptance-boundary witnesses must be separately retained; no module acceptance is asserted.')
    (PACKET / 'CONSUMER_AUDIT.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: output[k] for k in ('status','runtimeCommit','inventoryRows','uniqueSourceLines','files','changedFiles')}))


if __name__ == '__main__':
    main()
