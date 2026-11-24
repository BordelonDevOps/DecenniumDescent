#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy : ICommandAssessmentFactsPolicyV1
    {
        // Incremental implementation inventory, not the final INT-05 operation catalog.
        bool ICommandAssessmentFactsPolicyV1.SupportsAssessment(CommandKind kind)
            => connectedClericCasting && (kind == CommandKind.EndSpellConcentration
                || kind == CommandKind.GroundCastingStrain || kind == CommandKind.FocusDetectedAura);
        bool ICommandAssessmentFactsPolicyV1.RequiresVerifiedAssessment(CommandKind kind)
            => kind == CommandKind.StartNextCharterPlan && verifiedPlanningPassage;

        NativeCommandAssessmentV1 ICommandAssessmentFactsPolicyV1.AssessFacts(NativeReadContextV1 context,
            Snapshot current, Authority authority, Command command)
        {
            using var conditions = ConditionResolutionScope.EnterRead(context, current);
            if (((ICommandAssessmentFactsPolicyV1)this).RequiresVerifiedAssessment(command.Kind))
                throw new InvalidOperationException("This operation requires its owning verified checkpoint.");
            if (!((ICommandAssessmentFactsPolicyV1)this).SupportsAssessment(command.Kind))
                throw new InvalidOperationException("Native assessment extraction is incomplete for this operation.");
            var failure = WorldOpeningConstraintV1(current, command)
                ?? ActiveLongRestInterruptionV1(current, command);
            if (failure == null && current.ConnectedClericCasting && PendingSanctuary(current) != null)
                failure = NonSanctuaryResponseConstraintV1(command);
            failure = failure ?? GuidanceChoiceConstraintV1(current, command)
                ?? SpellCastingProfile.PhysicalConstraintV1(current, command)
                ?? CastingUtilityConstraintV1(current, command);
            // Initial utility admission does not certify the shared post-resolution tail or
            // candidate validation. Those stages must not be predicted by running them here.
            return new NativeCommandAssessmentV1(current.Revision, failure == null, null, failure);
        }

        private NativeCommandConstraintV1 WorldOpeningConstraintV1(Snapshot s, Command c)
        {
            const string source = "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs";
            if (!s.Actors.Any(a => a.Id == c.Actor)) return new NativeCommandConstraintV1("UnknownWorldActor", source, 866);
            if(s.FerryWraith!=null&&c.Kind==CommandKind.EncounterDash) {
                if(!FerryWraithProfile.DashPayloadValid(c))return new NativeCommandConstraintV1("InvalidFerryDashPayload", source, 868);
                if(!s.InventoryCombat||!FerryWraithProfile.Active(s)
                    ||c.Actor!=FerryWraithProfile.Hero&&c.Actor!=FerryWraithProfile.Companion)
                    return new NativeCommandConstraintV1("FerryDashRequiresPartyCombat", source, 870);
                if(c.Actor!=s.Encounter.CurrentActor||c.Target!=s.Encounter.CurrentTurnId)
                    return new NativeCommandConstraintV1("WrongRegularTurn", source, 871);
            }
            if(s.FerryWraith!=null&&IsOffCalendarActivity(s,c.Actor)
                &&ActivityInterval(s,c.Actor).Action==WorldActionCommitment.SealTear&&StartsOrResumesActivityWork(c))
                return new NativeCommandConstraintV1("OffCalendarActionAlreadySpent", source, 875);
            return null;
        }

        private static NativeCommandConstraintV1 ActiveLongRestInterruptionV1(Snapshot s, Command c)
            => ClericLongRestProfile.Active(s) != null && c.Actor == ClericRpProfile.Actor
                && c.Kind != CommandKind.AdvanceClock && c.Kind != CommandKind.BeginFixedEncounter
                && c.Kind != CommandKind.EnterInventoryCombat
                    ? new NativeCommandConstraintV1("LongRestRequiresInterruption",
                        "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 879) : null;

        private static NativeCommandConstraintV1 NonSanctuaryResponseConstraintV1(Command c)
            => c.Kind != CommandKind.RespondSanctuary
                ? new NativeCommandConstraintV1("SanctuaryChoicePending",
                    "engine/com.decennium.foundation/Laboratory/Model/SharedSanctuary.cs", 91) : null;

        private static NativeCommandConstraintV1 CastingUtilitySelectionConstraintV1(Snapshot s, Command c)
            => !s.ConnectedClericCasting || c.Actor != ClericRpProfile.Actor
                ? new NativeCommandConstraintV1("OrdinarySpellcastingUnsupported",
                    "engine/com.decennium.foundation/Laboratory/Model/SharedSpellCasting.cs", 360) : null;

        private NativeCommandConstraintV1 EndConcentrationConstraintV1(Snapshot s, Command c)
        {
            const string source = "engine/com.decennium.foundation/Laboratory/Model/SharedSpellCasting.cs";
            if(PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s))
                return new NativeCommandConstraintV1("TacticalChoicePending", source, 362);
            return s.SpellEffects.Any(x=>x.Id==c.Target&&x.CasterId==c.Actor&&x.Present&&x.RequiresConcentration)
                ? null : new NativeCommandConstraintV1("ConcentrationUnavailable", source, 364);
        }
    }
}
#endif
