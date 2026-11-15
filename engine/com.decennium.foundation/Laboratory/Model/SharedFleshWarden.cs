#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedFleshWarden;

        internal TestOnlySharedWorldPolicy EnableConnectedFleshWarden()
        {
            EnableConnectedShortRest();
            connectedFleshWarden = true;
            ContentFingerprint = FleshWardenProfile.FingerprintPrefix + RetreatHash(string.Join("|", ContentFingerprint,
                FleshWardenProfile.SourceRevision, FleshWardenProfile.FleshWarden, FleshWardenProfile.SpinalBuffer,
                "fixture-entitlements|basic-vital|actual-warrior3|automatic-slot1|initial-dormant-spinal-buffer|immutable-rest-choice|two-benefits|capacity-only"));
            return this;
        }

        private void InitializeFleshWarden(Snapshot state)
        {
            if (!connectedFleshWarden) return;
            state.ConnectedFleshWarden = true;
            state.FleshWarden = new FleshWardenRecord(new MutationQualificationRecord(FleshWardenProfile.Actor,
                FleshWardenProfile.SourceRevision, MutationTier.Basic, MutationTree.Vital), 1, FleshWardenProfile.SpinalBuffer, "",
                Array.Empty<MutationRestChoiceRecord>(), Array.Empty<MutationCapacityApplicationRecord>());
            state.CharacterFeatureGrants = state.CharacterFeatureGrants.Concat(new[] { FleshWardenProfile.FleshWarden, FleshWardenProfile.SpinalBuffer }
                .Select(id => new CharacterFeatureGrantRecord(FleshWardenProfile.Actor, id, "Warrior", 1, "", 0,
                    CharacterFeatureGrantOrigin.TestOnlyFixtureEntitlement))).ToArray();
        }

        private static string MutationRestAccess(Snapshot state, string mutation)
        {
            if (!state.ConnectedFleshWarden) return "MutationRestUnavailable";
            if (!FleshWardenProfile.IsMutation(mutation)) return "UnsupportedMutationRestSelection";
            if (!FleshWardenProfile.HasEntitlements(state)) return "MutationRestQualificationUnavailable";
            if (ShortRestBerth.BenefitsUsed(state) >= ShortRestBerth.InitialBenefits) return "MutationRestCadenceUnsupported";
            return null;
        }

        private static void AddMutationRestChoice(Snapshot state, ShortRestRecord rest, string mutation)
        {
            var old = state.FleshWarden;
            state.FleshWarden = new FleshWardenRecord(old.Qualification, old.SlotOrdinal, old.EquippedMutationId, old.ApplicationId,
                old.Choices.Append(new MutationRestChoiceRecord(rest.Id, mutation)), old.Applications);
        }

        private static void CompleteMutationRest(Snapshot state, ShortRestRecord rest)
        {
            var choice = FleshWardenProfile.Choice(state, rest.Id);
            if (choice == null || rest.Outcome != ShortRestOutcome.Completed) return;
            var old = state.FleshWarden;
            var character = CharacterRuleFacts.ForActor(state, FleshWardenProfile.Actor).Source;
            int warriorLevel = character.Levels.Count(x => x.ClassName == "Warrior");
            var applications = old.Applications.ToArray();
            string application = old.ApplicationId;
            if (old.EquippedMutationId != choice.MutationId) {
                if (old.EquippedMutationId == FleshWardenProfile.FleshWarden)
                    applications = applications.Select(x => x.Id == application ? x.End(rest) : x).ToArray();
                application = choice.MutationId == FleshWardenProfile.FleshWarden ? FleshWardenProfile.ApplicationIdentity(rest.Id) : "";
                if (application != "") applications = applications.Append(new MutationCapacityApplicationRecord(application,
                    FleshWardenProfile.FleshWarden, FleshWardenProfile.SourceRevision, character.ActorId, character.ActorId,
                    warriorLevel, rest.Id, rest.EndedAt.Value)).ToArray();
            }
            var change = ApplyMutationCapacity(state, applications, old.EquippedMutationId, old.ApplicationId, application);
            state.FleshWarden = new FleshWardenRecord(old.Qualification, old.SlotOrdinal, choice.MutationId, application,
                old.Choices.Select(x => x.RestId == rest.Id ? new MutationRestChoiceRecord(x.RestId, x.MutationId, change) : x), applications);
        }

        /// <summary>Shared capacity operation used by completed choices and detached boundary controls.
        /// The life record retains pre-systemic capacity; its effective resolution applies Strain once.</summary>
        internal static MutationCapacityChangeRecord ApplyMutationCapacity(Snapshot state, MutationCapacityApplicationRecord[] applications,
            string previousMutation, string previousApplication, string application)
        {
            const string actor = FleshWardenProfile.Actor;
            var character = CharacterRuleFacts.ForActor(state, actor).Source;
            long baseMaximum = PlaytestCharacters.BaseMaximumHp(character.Levels.Select(x => new CharacterLevelRecord(x.ClassName, x.BaseHp)).ToArray(),
                character.Abilities[(int)CharacterAbility.Constitution]).BaseMaximum;
            var sourceRecords = applications.Select(x => new MaximumHpApplication(x.Id, x.OwnerId, x.TargetId,
                new MaximumHpMagnitude(MaximumHpSource.FleshWarden, warriorLevel: x.WarriorLevel), new EffectClockMarker(x.StartedAt),
                present: x.Present, endedReason: x.Present ? null : "completed-mutation-replacement")).ToArray();
            var before = state.Lives.Single(x => x.ActorId == actor);
            var effectiveBefore = ActorLifeRules.ReadForResolution(state, before);
            var recomputed = PlaytestMaximumHp.Recompute(effectiveBefore, baseMaximum, sourceRecords, actor,
                new EffectClockMarker(state.RuleClock), expedition: ExpeditionStrainRules.Current(state, actor).Level);
            long preSystemic = checked((long)recomputed.Calculation.PreSystemicMaximum);
            var after = recomputed.State;
            state.Lives = state.Lives.Select(x => x.ActorId != actor ? x : new ActorLifeRecord(actor, preSystemic, after.Hp,
                x.TemporaryHp, x.LinkedInjuries, x.Stable, x.Dead, x.UsesDeathSaves, x.DeathSuccesses, x.DeathFailures,
                x.StableUntil, x.LastDeathTurn, x.Prone, x.HeldItems)).ToArray();
            return new MutationCapacityChangeRecord(previousMutation, previousApplication, application, baseMaximum,
                before.MaximumHp, preSystemic, effectiveBefore.MaximumHp, after.MaximumHp, before.Hp, after.Hp);
        }
    }
}
#endif
