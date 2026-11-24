#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy : ICommandAssessmentFactsPolicyV1
    {
        // Incremental implementation inventory, not the final INT-05 operation catalog.
        bool ICommandAssessmentFactsPolicyV1.SupportsAssessment(CommandKind kind)
            => kind == CommandKind.CastKnownSpell || kind == CommandKind.AcquireEarnedSpell
                || kind == CommandKind.UseIntimidatingPresence
                || connectedClericCasting && (kind == CommandKind.EndSpellConcentration
                || kind == CommandKind.GroundCastingStrain || kind == CommandKind.FocusDetectedAura)
                || ClericLongRestProfile.IsCommand(kind) || kind == CommandKind.UseHealingRite
                || kind == CommandKind.UseDivineInvocation || kind == CommandKind.UseConsecrate
                || ShortRestBerth.IsCommand(kind) || kind == CommandKind.ConsumeDecay
                || WoundTreatmentStation.IsCommand(kind) || kind == CommandKind.StabilizeCompanion
                || kind == CommandKind.Hide || kind == CommandKind.Search || kind == CommandKind.CancelExplorationHide
                || kind == CommandKind.CancelExplorationSearch
                || kind == CommandKind.ResolveExpeditionStrainRecovery
                || kind == CommandKind.StartHavenAppraisal || kind == CommandKind.StartExpeditionBill
                || kind == CommandKind.AcceptNextCharter || kind == CommandKind.StartCharterAttempt
                || kind == CommandKind.ObserveCharterApproach
                || TestOnlyFillingPolicy.IsWaterFillCommand(kind)
                || kind==CommandKind.StartMining || kind==CommandKind.PauseMining || kind==CommandKind.ResumeMining
                || ManufacturingCommand(kind) || FormulaCommand(kind)
                || kind == CommandKind.CloseExpeditionEpisode
                || kind == CommandKind.StartNextCharterPlan
                || kind == CommandKind.AwardCharacterMilestone || kind == CommandKind.AdvanceCharacterLevel;
        bool ICommandAssessmentFactsPolicyV1.RequiresVerifiedAssessment(CommandKind kind)
            => kind == CommandKind.StartNextCharterPlan && verifiedPlanningPassage;

        NativeCommandAssessmentV1 ICommandAssessmentFactsPolicyV1.AssessFacts(NativeReadContextV1 context,
            Snapshot current, Authority authority, Command command)
        {
            if (((ICommandAssessmentFactsPolicyV1)this).RequiresVerifiedAssessment(command.Kind))
                throw new InvalidOperationException("This operation requires its owning verified checkpoint.");
            return AssessInitialFactsV1(context,current,command);
        }

        private NativeCommandAssessmentV1 AssessInitialFactsV1(NativeReadContextV1 context,
            Snapshot current, Command command, PlanningPassage? passage = null)
        {
            using var conditions = ConditionResolutionScope.EnterRead(context, current);
            if(command.Kind==CommandKind.StartNextCharterPlan && nextCharterPlanProfile!=null
                && (!passage.HasValue || !passage.Value.Covers(current,nextCharterPlanProfile.Terms,current.Revision)))
                return NativeCommandAssessmentV1.VerificationUnavailableAt(current.Revision);
            if (!((ICommandAssessmentFactsPolicyV1)this).SupportsAssessment(command.Kind))
                throw new InvalidOperationException("Native assessment extraction is incomplete for this operation.");
            var failure = WorldOpeningConstraintV1(current, command);
            // Native long-rest requests return before the active-rest interruption gate,
            // Sanctuary, Guidance and physical checks. Preserve this early branch exactly.
            if (ClericLongRestProfile.IsCommand(command.Kind))
                return InitialAssessmentV1(current, failure ?? ClericLongRestConstraintV1(current, command));
            failure = failure ?? ActiveLongRestInterruptionV1(current, command);
            if (failure == null && current.ConnectedClericCasting && PendingSanctuary(current) != null)
                failure = NonSanctuaryResponseConstraintV1(command);
            failure = failure ?? GuidanceChoiceConstraintV1(current, command)
                ?? SpellCastingProfile.PhysicalConstraintV1(current, command)
                ?? SelectedInitialConstraintV1(current, command, passage);
            return InitialAssessmentV1(current, failure);
        }

        private NativeCommandConstraintV1 SelectedInitialConstraintV1(Snapshot current, Command command, PlanningPassage? passage = null)
        {
            switch (command.Kind) {
                case CommandKind.CastKnownSpell: return current.ConnectedClericCasting
                    ? SpellCastConstraintV1(current, command) : ClericRepertoireProfile.CommandConstraintV1(current, command);
                case CommandKind.AcquireEarnedSpell: return ClericRepertoireProfile.CommandConstraintV1(current, command);
                case CommandKind.UseIntimidatingPresence: return IntimidatingPresenceConstraintV1(current, command);
                case CommandKind.UseConsecrate: return ConsecrateConstraintV1(current, command);
                case CommandKind.UseDivineInvocation: return DivineInvocationConstraintV1(current, command);
                case CommandKind.UseHealingRite: return HealingRiteConstraintV1(current, command);
                case CommandKind.BeginShortRest:
                case CommandKind.InterruptShortRest:
                case CommandKind.BeginMutationShortRest:
                    return ClassRecoveryConstraintV1(current, command) ?? ShortRestConstraintV1(current, command);
                case CommandKind.ConsumeDecay:
                    return ActiveShortRestInterruptionV1(current, command) ?? ConsumeDecayConstraintV1(current, command);
                case CommandKind.StartWoundTreatment:
                case CommandKind.InterruptWoundTreatment:
                    return ActiveShortRestInterruptionV1(current, command) ?? WoundTreatmentConstraintV1(current, command);
                case CommandKind.StabilizeCompanion:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? CompanionStabilizationConstraintV1(current, command);
                case CommandKind.StartHavenAppraisal:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? AssessHavenAppraisalConstraintV1(current, command, out _, out _);
                case CommandKind.StartExpeditionBill:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? AssessExpeditionBillConstraintV1(current, command, out _, out _);
                case CommandKind.StartWaterFill:
                case CommandKind.PauseWaterFill:
                case CommandKind.ResumeWaterFill:
                case CommandKind.CancelWaterFill:
                    return WaterFillBranchConstraintV1(current,command);
                case CommandKind.StartMining:
                case CommandKind.PauseMining:
                case CommandKind.ResumeMining:
                    return BeforeWorkBranchConstraintV1(current,command) ?? (IsMiningCommand(command)
                        ?AssessMiningCommandConstraintV1(current,command,out _):UnimplementedBranchConstraintV1(current,command));
                case CommandKind.StartManufacturing:
                case CommandKind.PauseManufacturing:
                case CommandKind.ResumeManufacturing:
                case CommandKind.CancelManufacturing:
                case CommandKind.ResolveManufacturingQuality:
                case CommandKind.UseAlchemyDose:
                    return BeforeWorkBranchConstraintV1(current,command) ?? ManufacturingInitialConstraintV1(current,command);
                case CommandKind.StartFormulaResearch:
                case CommandKind.StartFormulaCopy:
                case CommandKind.PauseFormulaWork:
                case CommandKind.ResumeFormulaWork:
                case CommandKind.CancelFormulaWork:
                    return BeforeWorkBranchConstraintV1(current,command)
                        ?? (connectedCombat!=null && PendingCalendarChoice(current)
                            ? new NativeCommandConstraintV1("TacticalChoicePending", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1036)
                            : FormulaWorkConstraintV1(current,command,out _,out _,out _,out _));
                case CommandKind.CloseExpeditionEpisode:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? ExpeditionCloseConstraintV1(current, command, out _, false);
                case CommandKind.StartNextCharterPlan:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? AssessNextCharterPlanCommandConstraintV1(current, command, out _, out _, out _, passage);
                case CommandKind.AcceptNextCharter:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? AssessNextCharterAgreementCommandConstraintV1(current, command, out _, out _);
                case CommandKind.StartCharterAttempt:
                case CommandKind.ObserveCharterApproach:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? AssessCharterAttemptConstraintV1(current, command, out _, out _);
                case CommandKind.ResolveExpeditionStrainRecovery:
                    return ActiveShortRestInterruptionV1(current, command) ?? WoundTreatmentOuterConstraintV1(current, command)
                        ?? SearchActivityConstraintV1(current, command) ?? HideActivityConstraintV1(current, command)
                        ?? RetreatHostileAttackConstraintV1(current, command) ?? PendingRecoveryChoiceConstraintV1(current, command)
                        ?? StrainRecoveryInitialConstraintV1(current, command);
                case CommandKind.AwardCharacterMilestone:
                case CommandKind.AdvanceCharacterLevel:
                    return BeforeStabilizationBranchConstraintV1(current, command)
                        ?? HavenMealServingConstraintV1(current, command) ?? RouteTravelOuterConstraintV1(current, command)
                        ?? (IsClericAdvancement(current, command) ? ClericAdvancementConstraintV1(current, command)
                            : CharacterAdvancementRules.InitialConstraintV1(current, command));
                case CommandKind.Hide:
                case CommandKind.Search:
                case CommandKind.CancelExplorationHide:
                case CommandKind.CancelExplorationSearch:
                    return ObservationBranchConstraintV1(current, command);
                default: return CastingUtilityConstraintV1(current, command);
            }
        }

        private NativeCommandConstraintV1 ObservationBranchConstraintV1(Snapshot current, Command command)
        {
            var failure = ActiveShortRestInterruptionV1(current, command) ?? WoundTreatmentOuterConstraintV1(current, command)
                ?? SearchActivityConstraintV1(current, command) ?? HideActivityConstraintV1(current, command);
            if (failure != null) return failure;
            if (command.Kind == CommandKind.CancelExplorationHide)
                return current.ExplorationHide == null ? new NativeCommandConstraintV1("OrdinaryHideUnavailable",
                    "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 918)
                    : CancelExplorationHideConstraintV1(current, command);
            if (current.ExplorationHide != null && !current.InventoryCombat && command.Kind == CommandKind.Hide)
                return ExplorationHideConstraintV1(current, command, out _, out _, out _);
            if(current.ExplorationSearch==null && command.Kind==CommandKind.CancelExplorationSearch)
                return BeforeWorkBranchConstraintV1(current,command) ?? UnimplementedBranchConstraintV1(current,command);
            if (current.ExplorationSearch != null && command.Kind == CommandKind.CancelExplorationSearch)
                return CancelExplorationSearchConstraintV1(current, command);
            if (current.ExplorationSearch != null && !current.InventoryCombat && command.Kind == CommandKind.Search)
                return ExplorationSearchConstraintV1(current, command, out _);
            failure = RetreatHostileAttackConstraintV1(current, command) ?? PendingRecoveryChoiceConstraintV1(current, command)
                ?? HavenCareActorConstraintV1(current, command) ?? MoraleRestingActorConstraintV1(current, command)
                ?? RestingActorConstraintV1(current, command) ?? HavenMealServingConstraintV1(current, command)
                ?? RouteTravelOuterConstraintV1(current, command) ?? ObservationActionConstraintV1(current, command, out _);
            if(failure!=null)return failure;
            if(command.Kind==CommandKind.Search) {
                failure=SearchRequestConstraintV1(current,command,out var cell);
                return failure ?? SearchCandidateConstraintV1(current,command,cell,out _);
            }
            return HideConstraintV1(current, command, out _, out _, out _, out _, out _, out _);
        }

        // Used only for stabilization, advancement, appraisal, billing and charter assent/attempts. Intervening native
        // dispatches and transition-only guards cannot match these kinds; this is not a universal prefix.
        private NativeCommandConstraintV1 BeforeStabilizationBranchConstraintV1(Snapshot current, Command command)
            => ActiveShortRestInterruptionV1(current, command) ?? WoundTreatmentOuterConstraintV1(current, command)
                ?? SearchActivityConstraintV1(current, command) ?? HideActivityConstraintV1(current, command)
                ?? RetreatHostileAttackConstraintV1(current, command) ?? PendingRecoveryChoiceConstraintV1(current, command)
                ?? HavenCareActorConstraintV1(current, command) ?? MoraleRestingActorConstraintV1(current, command)
                ?? RestingActorConstraintV1(current, command);

        private static NativeCommandAssessmentV1 InitialAssessmentV1(Snapshot current, NativeCommandConstraintV1 failure)
        {
            // Initial admission does not certify the shared post-resolution tail or
            // candidate validation. Those stages must not be predicted by running them here.
            return new NativeCommandAssessmentV1(current.Revision, failure == null, null, failure);
        }

        private NativeCommandConstraintV1 RouteTravelOuterConstraintV1(Snapshot s, Command c)
        {
            var openRoute = routeTravelFixture == null ? null : OpenRouteTravel(s, c.Actor);
            var attachedRoutePosition = routeMotionFixture == null ? null : RouteSpatial(s, c.Actor);
            if (openRoute?.Status == ExpeditionRouteTravelStatus.Paused && attachedRoutePosition != null
                && !attachedRoutePosition.Detached
                && (attachedRoutePosition.X.Denominator != 1 || attachedRoutePosition.Y.Denominator != 1)
                && c.Kind != CommandKind.BeginWorldStep && c.Kind != CommandKind.AdvanceClock
                && c.Kind != CommandKind.DispatchConditionEvent && c.Kind != CommandKind.BeginFixedEncounter)
                return new NativeCommandConstraintV1("RouteTravelerMustDetachBeforeStationaryAction", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 975);
            if (openRoute?.Status == ExpeditionRouteTravelStatus.Moving
                && c.Kind != CommandKind.AdvanceClock && c.Kind != CommandKind.DispatchConditionEvent
                && c.Kind != CommandKind.BeginFixedEncounter) return new NativeCommandConstraintV1("RouteTravelMustPauseFirst", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 978);
            return null;
        }

        private static NativeCommandConstraintV1 WoundTreatmentOuterConstraintV1(Snapshot s, Command c)
        {
            if (s.ConnectedWoundTreatment && WoundTreatmentStation.IsStationId(c.Target)) return new NativeCommandConstraintV1("WoundTreatmentStockSealed", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 909);
            if (WoundTreatmentStation.Active(s) != null && (c.Actor == WoundTreatmentStation.Healer || c.Actor == WoundTreatmentStation.Patient)
                && c.Kind != CommandKind.AdvanceClock)
                return new NativeCommandConstraintV1("WoundTreatmentParticipantOccupied", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 912);
            return null;
        }

        private static NativeCommandConstraintV1 ClassRecoveryConstraintV1(Snapshot s, Command c)
            => s.ConnectedClericRp && ShortRestBerth.IsCommand(c.Kind)
                ? new NativeCommandConstraintV1("ClassRecoveryUnsupported",
                    "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 896) : null;

        private static NativeCommandConstraintV1 ActiveShortRestInterruptionV1(Snapshot s, Command c)
            => ShortRestBerth.Active(s) != null && c.Actor == ShortRestBerth.Actor
                && c.Kind != CommandKind.AdvanceClock && c.Kind != CommandKind.BeginFixedEncounter
                && c.Kind != CommandKind.EnterInventoryCombat
                    ? new NativeCommandConstraintV1("ShortRestRequiresInterruption",
                        "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 906) : null;

        // Exact shared prefix for selected mining, formula and manufacturing commands; earlier dispatch families are excluded.
        private NativeCommandConstraintV1 BeforeWorkBranchConstraintV1(Snapshot s, Command c)
            => BeforeStabilizationBranchConstraintV1(s,c) ?? HavenMealServingConstraintV1(s,c)
                ?? RouteTravelOuterConstraintV1(s,c) ?? OffCalendarWorkConstraintV1(s,c)
                ?? contentManifest?.CommandConstraintV1(s,c) ?? Recipe347WorkWatchConstraintV1(s,c)
                ?? (ManufacturingChoicePending(s) && c.Kind!=CommandKind.ResolveManufacturingQuality
                    && c.Kind!=CommandKind.ResolveRecipe347Quality ? new NativeCommandConstraintV1("ManufacturingChoicePending",
                    "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1003) : null);

        private NativeCommandConstraintV1 OffCalendarWorkConstraintV1(Snapshot s, Command c)
        {
            if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c) && !IsConnectedRecipe4Check(s, c)) {
                var activity = ActivityInterval(s, c.Actor);
                if (activity.Action == WorldActionCommitment.Dash
                    || activity.Action == WorldActionCommitment.ActiveLabor && !CanContinueActivityLabor(s, c.Actor))
                    return new NativeCommandConstraintV1("OffCalendarActionAlreadySpent", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 990);
            }
            return null;
        }

        private NativeCommandConstraintV1 OrdinaryManagementConstraintV1(Snapshot s,Command c)
        {
            // None of these procedures may authorize access using a stale integer grid anchor.
            if (s.WorldTraversals.Any(x => x.ActorId == c.Actor || c.Inventory?.Destination == x.ActorId)) return new NativeCommandConstraintV1("TraversalRequiresStationaryInteraction", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1124);
            bool release = c.Kind == CommandKind.PauseCrop || c.Kind == CommandKind.PauseWaterFill || c.Kind == CommandKind.CancelWaterFill || c.Kind == CommandKind.InterruptIntake || c.Kind == CommandKind.SetCropConditions;
            if (!release && !CapableWorker(s, c.Actor)) return new NativeCommandConstraintV1("WorkerCannotPerformTask", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1126);
            if ((c.Kind == CommandKind.StartWaterFill || c.Kind == CommandKind.ResumeWaterFill) && AvailableHands(s, c.Actor) < 2) return new NativeCommandConstraintV1("TwoHandsRequired", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1127);
            return null;
        }

        private static NativeCommandConstraintV1 SharedUnimplementedConstraintV1(Command c)
            => c.Combat!=null
                ?new NativeCommandConstraintV1("SharedCombatHandoffNotImplemented", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1060)
                :new NativeCommandConstraintV1("SharedCommandNotImplemented", "engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs", 1122);

        private NativeCommandConstraintV1 UnimplementedBranchConstraintV1(Snapshot s,Command c)
            => connectedCombat!=null && s.InventoryCombat ? UnimplementedCalendarConstraintV1(s,c)
                : SharedUnimplementedConstraintV1(c);

        private NativeCommandConstraintV1 WaterFillBranchConstraintV1(Snapshot s,Command c)
        {
            var failure=BeforeWorkBranchConstraintV1(s,c);
            if(failure!=null)return failure;
            if(connectedCombat!=null && s.InventoryCombat)return UnimplementedCalendarConstraintV1(s,c);
            if(c.Combat!=null)return SharedUnimplementedConstraintV1(c);
            return OrdinaryManagementConstraintV1(s,c) ?? inventory.AssessWaterFillConstraintV1(s,c,out _);
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
