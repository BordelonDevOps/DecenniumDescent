#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedClericLongRest;

        internal TestOnlySharedWorldPolicy EnableConnectedClericLongRest(ClericInitialSelection initial,
            ClericRepertoireSelection repertoire, ClericMilestoneDeclaration declaration)
        {
            EnableConnectedClericCasting(initial,repertoire,declaration);
            EnableDailyProvisioning(new TestOnlyDailyProvisioningProfile());
            EnableRestDebt(new TestOnlyRestDebtProfile(sites:new[] {
                new TestOnlyRestSiteFact(ClericLongRestProfile.SiteId,ClericLongRestProfile.X,ClericLongRestProfile.Y,true,true)
            }));
            // Reuse recovery records and current timing, without selecting the older profile's
            // base-vessel or unlinked-carrying exceptions.
            strainRecoveryProfile = new TestOnlyExpeditionStrainRecoveryProfile(new[] { ClericLongRestProfile.SiteId });
            connectedClericLongRest = true;
            ContentFingerprint = ClericLongRestProfile.FingerprintPrefix + RetreatHash(string.Join("|",ContentFingerprint,
                ClericLongRestProfile.ApprovalResponse,ClericLongRestProfile.SiteId,
                "earned-cleric2-only|stationary1,3|post-closure|safe-secure-one-occupant|positive-hp|no-active-concentration",
                "passive-shelter|ambient-light|no-fee|no-provisions|fixed-two-member-obligations-from0",
                "full28800|positive-damage-including-temp-interrupts|invalidations-before-completion-and-debt",
                "beneficial86400|hp-positive-gap-then-restrictions|rp-max|unavailable-conviction-to-max-no-numeric-gain",
                "wound-adjusted-half-expended-hd|dissonance-clear|refrain-retained|two-short-rest-epoch",
                "completion-endings-even-when-capped|current-secure-point-choice-and-continuation|no-legacy-physical-exceptions",
                TestOnlyExpeditionStrainRecoveryProfile.SourceRevision,TestOnlyExpeditionStrainRecoveryProfile.StrainBlob,
                TestOnlyExpeditionStrainRecoveryProfile.ExpeditionBookBlob));
            return this;
        }

        private void InitializeClericLongRest(Snapshot s)
        {
            if (!connectedClericLongRest) return;
            s.ConnectedClericLongRest = true;
            s.ClericLongRests = Array.Empty<ClericLongRestRecord>();
            s.ClericLongRestSettlements = Array.Empty<ClericLongRestSettlementRecord>();
            s.ConvictionBalance = null;
        }

        private string ClericLongRestAccess(Snapshot s, ClericLongRestRecord active)
            => ClericLongRestAccessConstraintV1(s, active)?.NativeCode;

        private NativeCommandConstraintV1 ClericLongRestAccessConstraintV1(Snapshot s, ClericLongRestRecord active)
        {
            const string actor = ClericRpProfile.Actor;
            if (!s.ConnectedClericLongRest || s.ConvictionCapacity?.PoolAcquiredRevision == 0
                || s.ClericInvocationPath == null) return new NativeCommandConstraintV1("LongRestRequiresEarnedCleric2", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 49);
            if (s.InventoryCombat || s.ClericObjective == null
                || !s.ClosedEncounters.Any(x => x.Encounter.Id == s.ClericMilestone.LaterEncounterId))
                return new NativeCommandConstraintV1("LongRestRequiresSettledEncounterClosure", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 52);
            var body = s.Actors.Single(x => x.Id == actor);
            if (body.X != ClericLongRestProfile.X || body.Y != ClericLongRestProfile.Y
                || !WorldWalkable(s,body.X,body.Y) || s.WorldTraversals.Any(x => x.ActorId == actor))
                return new NativeCommandConstraintV1("LongRestRequiresStationaryBerthAccess", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 56);
            if (s.Actors.Any(x => x.Id != actor && x.X == body.X && x.Y == body.Y)) return new NativeCommandConstraintV1("LongRestBerthOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 57);
            var life = s.Lives.Single(x => x.ActorId == actor);
            var conditions = View(s,actor);
            if (life.Dead || life.Hp <= 0 || life.Stable || life.StableUntil.HasValue
                || conditions.Has(ConditionKind.Unconscious) || conditions.Has(ConditionKind.Petrified)
                || ExpeditionStrainRules.Current(s,actor).Level >= 6) return new NativeCommandConstraintV1("LongRestBodyUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 62);
            if (s.SpellEffects.Any(x => x.CasterId == actor && x.Present && x.RequiresConcentration))
                return new NativeCommandConstraintV1("LongRestRequiresConcentrationEnded", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 64);
            var end = active?.DueAt ?? s.RuleClock.AddSeconds(ClericLongRestProfile.DurationSeconds);
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == actor && x.JobId != active?.Id
                    && x.Start < end && x.End > s.RuleClock)
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == actor && x.Id != active?.Id)
                || s.ExpeditionAssignments.Any(x => x.WorkerId == actor && x.Open)
                || s.RouteTravels.Any(x => x.TravelerId == actor && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused)))
                return new NativeCommandConstraintV1("LongRestActorOccupied", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 71);
            if (s.CharacterHitDice.Any(x => x.ActorId == actor && x.Spent)) return new NativeCommandConstraintV1("LongRestSpentDicePathUnsupported", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 72);
            return null;
        }

        private string AssessClericLongRest(Snapshot s, Command c)
            => ClericLongRestConstraintV1(s, c)?.NativeCode;

        private NativeCommandConstraintV1 ClericLongRestConstraintV1(Snapshot s, Command c)
        {
            if (!s.ConnectedClericLongRest || c.Actor != ClericRpProfile.Actor) return new NativeCommandConstraintV1("LongRestUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 78);
            if (c.X != 0 || c.Y != 0 || c.Inventory != null || c.Combat != null || c.Advancement != null
                || c.Ranged != null || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null
                || c.DefensiveFormation != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null || c.RouteMappingWork != null
                || c.IntimidatingPresence != null || c.HealingRite != null || c.SpellCast != null
                || c.Guidance != null || c.SanctuaryResponse != null) return new NativeCommandConstraintV1("UnexpectedLongRestPayload", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 84);
            var active = ClericLongRestProfile.Active(s);
            if (c.Kind == CommandKind.InterruptLongRest)
                return active == null || c.Target != active.Id ? new NativeCommandConstraintV1("NoMatchingActiveLongRest", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 87) : null;
            if (c.Kind != CommandKind.BeginLongRest || c.Target != ClericLongRestProfile.SiteId) return new NativeCommandConstraintV1("LongRestSiteUnavailable", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 88);
            if (active != null) return new NativeCommandConstraintV1("LongRestAlreadyActive", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 89);
            if (PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s)
                || s.ManufacturingAdvance != null) return new NativeCommandConstraintV1("LongRestPendingChoice", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 91);
            if (s.ClericLongRests.Length >= ClericLongRestProfile.MaxAttempts) return new NativeCommandConstraintV1("LongRestHistoryCapacityReached", "engine/com.decennium.foundation/Laboratory/Model/SharedClericLongRest.cs", 92);
            return ClericLongRestAccessConstraintV1(s,null);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverClericLongRest(Snapshot s, string actor)
        {
            if (!s.ConnectedClericLongRest || actor != ClericRpProfile.Actor) yield break;
            var active = ClericLongRestProfile.Active(s);
            var option = new Command("option." + s.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".long-rest",
                actor,s.Revision,active == null ? CommandKind.BeginLongRest : CommandKind.InterruptLongRest,
                active?.Id ?? ClericLongRestProfile.SiteId);
            if (AssessClericLongRest(s,option) == null) yield return option;
        }

        private string ResolveClericLongRest(Snapshot s, Command c)
        {
            string failure = AssessClericLongRest(s,c);
            if (failure != null) return failure;
            if (c.Kind == CommandKind.InterruptLongRest) {
                InterruptClericLongRest(s,ClericLongRestProfile.Active(s),c.Id,ClericLongRestInterruption.Explicit,c.Id);
                return null;
            }
            var rest = new ClericLongRestRecord(s.ClericLongRests.Length,c.Id,s.Revision+1,s.RuleClock);
            s.Work = s.Work.Reserve(rest.Id,new[] {
                new WorkerInterval(ClericLongRestProfile.OccupancyId(rest.Id),rest.Id,rest.ActorId,rest.StartedAt,rest.DueAt)
            },Array.Empty<ResourceReservation>());
            s.RestIntervals = s.RestIntervals.Append(new RestIntervalRecord(rest.Id,rest.ActorId,rest.SiteId,
                rest.StartedAt,rest.DueAt,null,RestIntervalStatus.Active,s.Revision+1)).ToArray();
            s.ClericLongRests = s.ClericLongRests.Append(rest).ToArray();
            return null;
        }

        private static void InterruptClericLongRest(Snapshot s, ClericLongRestRecord rest, string commandId,
            ClericLongRestInterruption reason, string cause)
        {
            if (rest == null) return;
            if (!Validation.ValidId(commandId)) throw new ArgumentException("Rest interruption requires its actual command.");
            s.Work = s.Work.CancelFutureWork(rest.Id,s.RuleClock);
            var ended = new ClericLongRestRecord(rest.Sequence,rest.StartCommandId,rest.StartRevision,rest.StartedAt,
                ClericLongRestOutcome.Interrupted,reason,ClericLongRestBenefit.NotCompleted,
                commandId,s.Revision+1,s.RuleClock,cause);
            s.ClericLongRests = s.ClericLongRests.Select(x => x.Id == rest.Id ? ended : x).ToArray();
            s.RestIntervals = s.RestIntervals.Select(x => x.Id == rest.Id
                ? new RestIntervalRecord(x.Id,x.ActorId,x.SiteId,x.StartedAt,x.ScheduledEnd,s.RuleClock,
                    RestIntervalStatus.Interrupted,s.Revision+1,allowLongRestBoundaryInterruption:true) : x).ToArray();
        }

        internal static void InterruptClericLongRestForDamage(Snapshot s, string actor, long resolvedDamage,
            string commandId, string cause)
        {
            if (actor != ClericRpProfile.Actor || !ClericLongRestProfile.DamageInterrupts(resolvedDamage)) return;
            InterruptClericLongRest(s,ClericLongRestProfile.Active(s),commandId,ClericLongRestInterruption.Damage,cause);
        }

        private void ReconcileClericLongRestAccess(Snapshot s, Command command)
        {
            var active = ClericLongRestProfile.Active(s);
            if (active == null) return;
            string failure = ClericLongRestAccess(s,active);
            if (failure == null) return;
            var reason = s.InventoryCombat ? ClericLongRestInterruption.Encounter
                : failure == "LongRestBodyUnsupported" ? ClericLongRestInterruption.BodyIneligible : ClericLongRestInterruption.AccessLost;
            InterruptClericLongRest(s,active,command.Id,reason,command.Id);
        }

        // Called only after due world events and provisioning have been applied. Invalidated
        // participants are interrupted before the shared debt processor can credit completion.
        private string ProcessClericLongRestBoundary(Snapshot s, Command command)
        {
            if (!s.ConnectedClericLongRest) return null;
            ReconcileClericLongRestAccess(s,command);
            string failure = ProcessRestDebtBoundary(s);
            if (failure != null) return failure;
            ClampExpeditionStrainLife(s);
            failure = OpenStrainRecoveryOffers(s,command);
            if (failure != null) return failure;
            var rest = ClericLongRestProfile.Active(s);
            if (rest == null || rest.DueAt != s.RuleClock) return null;
            return CompleteClericLongRest(s,rest,command);
        }

        private string CompleteClericLongRest(Snapshot s, ClericLongRestRecord rest, Command command)
        {
            var shared = s.RestIntervals.Single(x => x.Id == rest.Id);
            if (shared.Status != RestIntervalStatus.Completed || shared.EndedAt != s.RuleClock)
                return "LongRestSharedCompletionMissing";
            var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.RestIntervalId == rest.Id);
            var prior = s.ClericLongRestSettlements.LastOrDefault(x => x.Benefit == ClericLongRestBenefit.Eligible);
            bool eligible = benefit != null;
            var status = eligible ? ClericLongRestBenefit.Eligible
                : prior != null && s.RuleClock < prior.At.AddSeconds(ClericLongRestProfile.BenefitCadenceSeconds)
                    ? ClericLongRestBenefit.CadenceLimited : ClericLongRestBenefit.RestDebtOwed;
            var before = s.Lives.Single(x => x.ActorId == rest.ActorId);
            var life = ActorLifeRules.ReadForResolution(s,before);
            if (life.Dead || life.Hp <= 0) return "LongRestTerminalEligibilityWasNotReconciled";
            var pool = s.ResonancePools.Single(x => x.ActorId == rest.ActorId);
            var casting = s.CastingStrain.Single(x => x.ActorId == rest.ActorId);
            long requested = eligible ? ClericLongRestProfile.HealingRequest(life.Hp,life.MaximumHp) : 0;
            long potential = View(s,rest.ActorId).HealingPotential(requested);
            var healed = eligible ? PlaytestLife.Heal(life,potential) : life;
            // The selected companion has no specific-duration temporary-HP producer. Generic
            // completion endings apply even when this actual completed rest is benefit-capped.
            var after = new LifeState(healed.MaximumHp,healed.Hp,0,healed.Wounds,healed.Stable,healed.Dead,
                healed.DeathSuccesses,healed.DeathFailures,healed.UsesDeathSaves,lastDeathTurn:healed.LastDeathTurn,
                stableUntil:healed.StableUntil);
            int? convictionBefore = s.ConvictionBalance?.Current;
            int? convictionAfter = eligible ? s.ConvictionCapacity.Maximum : convictionBefore;
            var settled = new ClericLongRestSettlementRecord(rest.Id,command.Id,s.Revision+1,s.RuleClock,status,
                benefit?.Id ?? "",prior?.BeneficialRestId ?? "",BishopProfile.CapacityRevisionBefore(s,s.Revision+1),
                life.Hp,life.MaximumHp,requested,potential,after.Hp,life.TemporaryHp,after.TemporaryHp,
                life.Wounds.Count,0,eligible ? ClericLongRestProfile.HitDiceAllowance(0,life.Wounds.Count) : 0,0,
                pool.Current,pool.Maximum,eligible ? pool.Maximum : pool.Current,convictionBefore,convictionAfter,
                casting.Dissonance,eligible ? 0 : casting.Dissonance,casting.LastSpellId,casting.Refrain,casting.LastCastRevision,s.BishopEntry!=null);
            TestOnlyClubAttackPolicy.ApplyLife(s,before,after);
            if (eligible) {
                s.ResonancePools = s.ResonancePools.Select(x => x.ActorId == rest.ActorId
                    ? new ResonancePoolRecord(x.ActorId,x.Maximum,x.Maximum,x.InitialFunding) : x).ToArray();
                s.CastingStrain = s.CastingStrain.Select(x => x.ActorId == rest.ActorId
                    ? new CastingStrainRecord(x.ActorId,0,x.LastSpellId,x.Refrain,x.LastCastRevision) : x).ToArray();
                s.ConvictionBalance = new ConvictionBalanceRecord(s.ConvictionBalance?.FundingRestId ?? rest.Id,
                    s.ConvictionBalance?.FundingRevision ?? s.Revision+1,s.ConvictionCapacity.Maximum);
            }
            var ended = new ClericLongRestRecord(rest.Sequence,rest.StartCommandId,rest.StartRevision,rest.StartedAt,
                ClericLongRestOutcome.Completed,ClericLongRestInterruption.None,status,command.Id,s.Revision+1,s.RuleClock,command.Id);
            s.ClericLongRests = s.ClericLongRests.Select(x => x.Id == rest.Id ? ended : x).ToArray();
            s.ClericLongRestSettlements = s.ClericLongRestSettlements.Append(settled).ToArray();
            return null;
        }
    }
}
#endif
