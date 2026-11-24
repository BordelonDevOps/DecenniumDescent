#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private ClericMilestoneDeclaration clericMilestoneDeclaration;
        internal TestOnlySharedWorldPolicy EnableConnectedClericSettlement(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration)
        {
            if (declaration == null) throw new ArgumentNullException(nameof(declaration));
            EnableConnectedFrightened(initial,repertoire);
            clericMilestoneDeclaration = declaration;
            ContentFingerprint = ClericSettlementProfile.FingerprintPrefix + RetreatHash(string.Join("|",ContentFingerprint,
                declaration.Binding,declaration.Digest,ClericSettlementProfile.RadianceCardSha256,
                "review-dbb657df-4133-556e-bccc-a389145b7916|earned-cleric2|retained-own-slot|no-conviction-balance"));
            return this;
        }

        private void InitializeClericSettlement(Snapshot state)
        {
            if (clericMilestoneDeclaration == null) return;
            state.ConnectedClericSettlement = true;
            state.ClericMilestone = clericMilestoneDeclaration;
            state.ConvictionCapacity = new ConvictionCapacityRecord(ClericRpProfile.Actor,ClericRpProfile.SourceRevision,"",0);
        }

        private static void RecordClericObjectiveCompletion(Snapshot state, ClosedEncounterRecord closed)
        {
            if (!state.ConnectedClericSettlement || state.ClericObjective != null) return;
            var declaration = state.ClericMilestone; var first = state.LaterEncounter.FirstExit; var batch = state.ConnectedBatch;
            if (closed.Encounter.Id != declaration.LaterEncounterId || first?.Encounter.Id != declaration.FirstEncounterId
                || batch?.Disposition != ConnectedSpecimenDisposition.Consumed || batch.SettlementRevision <= first.ClosedRevision
                || batch.SettlementRevision >= closed.ClosedRevision || state.InventoryCombat
                || state.Lives.Single(x => x.ActorId == declaration.ActorId).Dead
                || !state.ManufacturingOrders.Any(x => x.Id == batch.OrderId && x.RecipeId == declaration.RecipeId
                    && x.Status == ManufacturingStatus.Complete)) return;
            state.ClericObjective = new ClericObjectiveCompletion(declaration.Digest,first.Reason,first.ClosedRevision,
                batch.OrderId,batch.SettlementRevision,closed.Reason,closed.ClosedRevision,closed.ClosedAt);
        }

        private static bool IsClericAdvancement(Snapshot s, Command c)
            => s.ConnectedClericSettlement && c.Actor == ClericRpProfile.Actor;

        private string AssessClericAdvancement(Snapshot s, Command c)
            => ClericAdvancementConstraintV1(s,c)?.NativeCode;

        private NativeCommandConstraintV1 ClericAdvancementConstraintV1(Snapshot s, Command c)
        {
            if (!IsClericAdvancement(s,c)) return new NativeCommandConstraintV1("UnsupportedAdvancementPath", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 50);
            if (c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null || c.Ranged != null
                || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null || c.DefensiveFormation != null
                || c.ExpeditionAssignment != null || c.HarvestSelection != null || c.MiningSelection != null
                || c.ProspectingExposure != null || c.RouteMappingWork != null || c.IntimidatingPresence != null || c.HealingRite != null)
                return new NativeCommandConstraintV1("InvalidAdvancementCommand", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 55);
            if (c.Target == BishopProfile.Milestone) return BishopAdvancementConstraintV1(s,c);
            if (c.Target != s.ClericMilestone.MilestoneId) return new NativeCommandConstraintV1("UndeclaredMilestone", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 57);
            if (s.ClericObjective == null) return new NativeCommandConstraintV1("MilestoneObjectiveIncomplete", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 58);
            if (c.Kind == CommandKind.AwardCharacterMilestone) {
                if (c.Advancement != null) return new NativeCommandConstraintV1("InvalidMilestoneAward", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 60);
                if (s.CharacterMilestones.Any(x => x.ActorId == c.Actor && x.MilestoneId == c.Target)) return new NativeCommandConstraintV1("MilestoneAlreadyAwarded", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 61);
                return s.CharacterMilestones.Length >= 256 ? new NativeCommandConstraintV1("MilestoneCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 62) : null;
            }
            if (c.Kind != CommandKind.AdvanceCharacterLevel || c.Advancement == null) return new NativeCommandConstraintV1("CharacterAdvancementCommandNotImplemented", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 64);
            var milestone = s.CharacterMilestones.SingleOrDefault(x => x.ActorId == c.Actor && x.MilestoneId == c.Target);
            if (milestone == null) return new NativeCommandConstraintV1("MilestoneNotAvailable", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 66);
            if (milestone.ConsumedRevision != 0) return new NativeCommandConstraintV1("MilestoneAlreadyConsumed", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 67);
            if (s.InventoryCombat) return new NativeCommandConstraintV1("TacticalControlActive", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 68);
            if (PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s)) return new NativeCommandConstraintV1("TacticalChoicePending", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 69);
            if (s.ManufacturingAdvance != null) return new NativeCommandConstraintV1("ManufacturingChoicePending", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 70);
            if (CharacterAdvancementRules.Busy(s,c.Actor) || OrdinaryInventory.Busy(s,c.Actor)) return new NativeCommandConstraintV1("CharacterBusy", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 71);
            var character = s.Characters.Single(x => x.ActorId == c.Actor);
            if (character.ProfileId != ClericRpProfile.CharacterProfile || character.Levels.Count != 1
                || character.Levels[0].ClassName != "Cleric" || character.Levels[0].BaseHp != 8
                || !character.Abilities.SequenceEqual(new[] {10,10,10,10,14,10})) return new NativeCommandConstraintV1("UnsupportedAdvancementPath", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 75);
            if (!ClericSettlementProfile.ValidChoices(c.Advancement)) return new NativeCommandConstraintV1("ClericSettlementChoiceUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 76);
            var row = ClassAdvancementScheduleCatalog.Get("Cleric",2);
            if (row == null || row.RequiredSelections != 2 || row.MinimumActiveSelections != 0 || row.HasAsiOrFeatOpportunity != false
                || !row.Bands.SequenceEqual(new[] {"Base"},StringComparer.Ordinal)) return new NativeCommandConstraintV1("ClassScheduleNeedsBinding", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 79);
            var candidates = ClassAdvancementOptionCatalog.Candidates(row);
            foreach (string feature in c.Advancement.FeatureIds) {
                var option = ClassAdvancementOptionCatalog.Get("Cleric",feature);
                if (option == null || !candidates.Contains(option) || option.HasPathConstraint || option.HasDeclaredPrerequisite)
                    return new NativeCommandConstraintV1("FeatureOutsideClassSchedule", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 84);
            }
            if (s.CharacterFeatureGrants.Any(x => x.ActorId == c.Actor && (ClericSettlementProfile.SelectedCards.Contains(x.FeatureId)
                || x.FeatureId == ClericSettlementProfile.Attunement || x.FeatureId == ClericSettlementProfile.Radiance))) return new NativeCommandConstraintV1("FeatureAlreadyOwned", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 87);
            if (s.ClericInvocationPath != null || s.CharacterAdvancements.Any(x => x.ActorId == c.Actor)) return new NativeCommandConstraintV1("UnsupportedAdvancementPath", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 88);
            if (s.CharacterAdvancements.Length >= 128 || s.CharacterFeatureGrants.Length + 4 > 256 || s.CharacterHitDice.Length >= 1280)
                return new NativeCommandConstraintV1("AdvancementCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 90);
            var dice = s.CharacterHitDice.Where(x => x.ActorId == c.Actor).ToArray();
            if (dice.Length != 1 || dice[0].LevelOrdinal != 1 || dice[0].ClassName != "Cleric" || dice[0].DieSize != 8)
                return new NativeCommandConstraintV1("HitDieLedgerMismatch", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 93);
            var life = s.Lives.Single(x => x.ActorId == c.Actor);
            if (life.MaximumHp != 8) return new NativeCommandConstraintV1("AdvancementHealthBasisMismatch", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 95);
            var pool = s.ResonancePools.SingleOrDefault(x => x.ActorId == c.Actor);
            if (pool == null || pool.Maximum != DeriveResonanceMaximum(character)) return new NativeCommandConstraintV1("ResonancePoolUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 97);
            if (s.ConvictionCapacity?.PoolAcquiredRevision != 0) return new NativeCommandConstraintV1("ConvictionCapacityUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 98);
            if (ClericRepertoireProfile.ValidateInitialChoices(s.KnownSpells.Select(x => x.SpellId)) != null
                || s.KnownSpells.Any(x => !x.MatchesSource() || x.ActorId != c.Actor || x.ClassName != "Cleric"
                    || x.Origin != SpellAcquisitionOrigin.InitialClassRepertoire || x.ClassLevel != 1 || x.LevelOrdinal != 1
                    || x.EntitlementId != ClericRepertoireProfile.InitialEntitlement || x.MilestoneId != "" || x.AcquiredRevision != 0)
                || s.InitialClassSelections.Count(x => ClericRpProfile.ValidInitialSelection(s,x)) != 1
                || s.CharacterFeatureGrants.Count(x => ClericRpProfile.ValidInitialGrant(s,x)) != 4)
                return new NativeCommandConstraintV1("ClericEarnedRepertoireChoiceUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedClericSettlement.cs", 105);
            return null;
        }

        private string ResolveClericAdvancement(Snapshot s, Command c)
        {
            string failure = AssessClericAdvancement(s,c); if (failure != null) return failure;
            if(c.Target==BishopProfile.Milestone){SettleBishopAdvancement(s,c);return null;}
            long revision = checked(s.Revision + 1);
            if (c.Kind == CommandKind.AwardCharacterMilestone) {
                s.CharacterMilestones = s.CharacterMilestones.Append(new CharacterMilestoneRecord(c.Target,c.Actor,revision)).ToArray();
                return null;
            }
            var prior = s.Characters.Single(x => x.ActorId == c.Actor);
            var levels = prior.Levels.Append(new CharacterLevelFact("Cleric",5)).ToArray();
            var character = new ActorCharacterRecord(c.Actor,prior.ProfileId,prior.Abilities,levels);
            long maximum = PlaytestCharacters.BaseMaximumHp(levels.Select(x => new CharacterLevelRecord(x.ClassName,x.BaseHp)).ToArray(),
                prior.Abilities[(int)CharacterAbility.Constitution]).BaseMaximum;
            var life = s.Lives.Single(x => x.ActorId == c.Actor);
            long current = PlaytestCharacters.ClampAfterCapacityChange(life.Hp,maximum);
            var advancement = new CharacterAdvancementRecord(c.Actor,c.Target,revision,1,2,"Cleric",2,5,HitPointGainMethod.FixedAverage,
                life.MaximumHp,maximum,life.Hp,current,ClericSettlementProfile.SelectedCards.ToArray());
            s.Characters = s.Characters.Select(x => x.ActorId == c.Actor ? character : x).ToArray();
            s.Lives = s.Lives.Select(x => x.ActorId != c.Actor ? x : new ActorLifeRecord(x.ActorId,maximum,current,x.TemporaryHp,x.LinkedInjuries,
                x.Stable,x.Dead,x.UsesDeathSaves,x.DeathSuccesses,x.DeathFailures,x.StableUntil,x.LastDeathTurn,x.Prone,x.HeldItems)).ToArray();
            s.CharacterHitDice = s.CharacterHitDice.Append(new CharacterHitDieRecord(c.Actor,2,"Cleric",8,false)).ToArray();
            s.CharacterFeatureGrants = s.CharacterFeatureGrants.Concat(ClericSettlementProfile.SelectedCards.Select(id =>
                new CharacterFeatureGrantRecord(c.Actor,id,"Cleric",2,c.Target,revision))).Concat(
                new[] {ClericSettlementProfile.Attunement,ClericSettlementProfile.Radiance}.Select(id =>
                new CharacterFeatureGrantRecord(c.Actor,id,"Cleric",2,c.Target,revision,CharacterFeatureGrantOrigin.EarnedAutomaticClassFeature))).ToArray();
            s.ClericInvocationPath = new ClericInvocationPathRecord(c.Actor,c.Advancement.InvocationPath,ClericRpProfile.SourceRevision,c.Target,revision);
            s.ResonancePools = s.ResonancePools.Select(x => x.ActorId == c.Actor ? x.ReconcileCapacity(DeriveResonanceMaximum(character)) : x).ToArray();
            s.ConvictionCapacity = new ConvictionCapacityRecord(c.Actor,ClericRpProfile.SourceRevision,c.Target,revision);
            s.CharacterMilestones = s.CharacterMilestones.Select(x => x.ActorId == c.Actor && x.MilestoneId == c.Target ? x.Consume(revision) : x).ToArray();
            s.CharacterAdvancements = s.CharacterAdvancements.Append(advancement).ToArray();
            SettleClericEarnedRepertoire(s,c.Actor,c.Advancement.EarnedSpell,advancement);
            return null;
        }

        private IEnumerable<Command> DiscoverClericAdvancement(Snapshot s, string actor)
        {
            if (!s.ConnectedClericSettlement || actor != ClericRpProfile.Actor || s.ClericObjective == null) yield break;
            string id = "option." + s.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".cleric";
            var command = s.CharacterMilestones.Any(x => x.ActorId == actor)
                ? new Command(id,actor,s.Revision,CommandKind.AdvanceCharacterLevel,s.ClericMilestone.MilestoneId,
                    advancement:new CharacterAdvancementRequest(ClericSettlementProfile.SelectedCards.ToArray(),
                        ClericSettlementProfile.Radiance,ClericRepertoireProfile.FutureChoice))
                : new Command(id,actor,s.Revision,CommandKind.AwardCharacterMilestone,s.ClericMilestone.MilestoneId);
            if (AssessClericAdvancement(s,command) == null) yield return command;
            foreach(var option in DiscoverBishopAdvancement(s,actor))yield return option;
        }
    }
}
#endif
