#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit fixed roster encounter in the supplied arena. The schema29 Soldier build
    /// schedules its companion ally alongside the hostile actor. This supplies test facts, not
    /// enemy content or AI.</summary>
    public sealed class SharedCombatFixture
    {
        public long EnemyHp { get; }
        public long EnemyMaximumHp { get; }
        public uint Seed { get; }
        public SharedCombatFixture(long enemyHp=26,uint seed=1,long enemyMaximumHp=26)
        {if(enemyHp<1||enemyMaximumHp<enemyHp||enemyMaximumHp>26||seed==0)throw new ArgumentException("Invalid connected combat fixture.");EnemyHp=enemyHp;EnemyMaximumHp=enemyMaximumHp;Seed=seed;}
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        /// <summary>Opts this TEST_ONLY shared simulation into schema56's persisted Dodge Action.</summary>
        public TestOnlySharedWorldPolicy EnableDodgeAction()
        {
            if(initializationStarted)throw new InvalidOperationException("Dodge content must be selected before Initial().");
            if(dodgeActionEnabled)return this;
            dodgeActionEnabled=true;
            using(var hash=SHA256.Create())ContentFingerprint="TEST_ONLY.dodge-v1-"+string.Concat(hash.ComputeHash(
                Encoding.UTF8.GetBytes(ContentFingerprint+"|source-dodge-until-next-regular-start|schema56"))
                .Select(x=>x.ToString("x2",System.Globalization.CultureInfo.InvariantCulture)));
            return this;
        }
        /// <summary>Opts a connected TEST_ONLY calendar into the persisted nonspell Ready Action
        /// slice. Named-target five-foot club/unarmed attacks use schema58 and the shared reaction queue.</summary>
        public TestOnlySharedWorldPolicy EnableReadyAction()
        {
            if(initializationStarted)throw new InvalidOperationException("Ready Action content must be selected before Initial().");
            if(readyActionEnabled)return this;
            if(connectedCombat==null)throw new InvalidOperationException("Ready Action requires the connected tactical calendar fixture.");
            readyActionEnabled=true;
            using(var hash=SHA256.Create())ContentFingerprint="TEST_ONLY.ready-action-v1-"+string.Concat(hash.ComputeHash(
                Encoding.UTF8.GetBytes(ContentFingerprint+"|named-target-enters-five-foot-reach|club-or-unarmed|shared-post-step-order|exact-shared-clock-own-start-expiry|schema58"))
                .Select(x=>x.ToString("x2",System.Globalization.CultureInfo.InvariantCulture)));
            return this;
        }
        /// <summary>Opts this TEST_ONLY shared world into explicit planar observation content.
        /// Call before Initial(); the map, per-actor ranges and records are part of schema51 saves.</summary>
        public TestOnlySharedWorldPolicy EnableObservation(ObservationFixture fixture)
            => EnableObservation(fixture, ObservationAlgorithmVersion.ExactPathIntervalsV2);

        /// <summary>Selects the explicit observation procedure used by saved schema51 histories.
        /// LegacySampledV1 is retained for replaying authentic saves created before exact intervals.</summary>
        public TestOnlySharedWorldPolicy EnableObservation(ObservationFixture fixture,
            ObservationAlgorithmVersion algorithmVersion)
        {
            if (fixture == null) throw new ArgumentNullException(nameof(fixture));
            if (algorithmVersion != ObservationAlgorithmVersion.LegacySampledV1
                && algorithmVersion != ObservationAlgorithmVersion.ExactPathIntervalsV2)
                throw new ArgumentOutOfRangeException(nameof(algorithmVersion));
            if (initializationStarted) throw new InvalidOperationException("Observation content must be selected before Initial().");
            if (observationFixture != null) throw new InvalidOperationException("Observation content is already selected.");
            if (routeTravelFixture != null) throw new InvalidOperationException("RouteObservationIntegrationUnsupported");
            observationFixture = fixture;
            observationAlgorithmVersion = algorithmVersion;
            ContentFingerprint = ObservationFixture.BindFingerprint(ContentFingerprint, fixture, algorithmVersion);
            return this;
        }

        /// <summary>Opts this TEST_ONLY fixture into the saved site-aware assignment increment.
        /// Call before Initial(); the selected schema and content fingerprint are part of the save scope.</summary>
        public TestOnlySharedWorldPolicy EnableExpeditionAssignments()
        {
            if (expeditionAssignmentsEnabled) return this;
            if (!PhysicalFishingEnabled && miningFixture==null && !cacheExcavationEnabled)
                throw new InvalidOperationException("Expedition assignments require an enabled physical Trap or mining procedure.");
            expeditionAssignmentsEnabled = true;
            using (var hash = System.Security.Cryptography.SHA256.Create())
                ContentFingerprint = "TEST_ONLY.site-assignment-v1-" + string.Concat(hash.ComputeHash(
                    System.Text.Encoding.UTF8.GetBytes(ContentFingerprint + "|site-aware-work-assignment-v1"))
                    .Select(x => x.ToString("x2", System.Globalization.CultureInfo.InvariantCulture)));
            return this;
        }

        /// <summary>Opts the finite TEST_ONLY cache fixture into one shallow buried-site procedure.
        /// Requires an actual portable kit so the shovel is present as equipment state.</summary>
        public TestOnlySharedWorldPolicy EnableBuriedCacheExcavation()
        {
            if (initializationStarted) throw new InvalidOperationException("Cache excavation must be selected before Initial().");
            if (cacheExcavationEnabled) return this;
            if (portableKit == null || supplyCache == null || !supplyCache.HasTools || supplyCache.HasKey)
                throw new InvalidOperationException("Buried-cache excavation requires the portable-kit cache fixture and actual thieves' tools.");
            if (contentManifest != null)
            {
                var shovel = contentManifest.ResolveRuntime("adventuring-gear.shovel");
                if (shovel == null || shovel.SemanticId != "adventuring-gear.shovel"
                    || !contentManifest.Supports(shovel, ContentOperation.PortableEquipment)
                    || !contentManifest.Supports(shovel, ContentOperation.PortableInteraction))
                    throw new InvalidOperationException("Buried-cache excavation requires the source-resolved shovel content profile.");
            }
            cacheExcavationEnabled = true;
            if (!expeditionAssignmentsEnabled) EnableExpeditionAssignments();
            using (var hash = System.Security.Cryptography.SHA256.Create())
                ContentFingerprint = "TEST_ONLY.buried-cache-v1-" + string.Concat(hash.ComputeHash(
                    System.Text.Encoding.UTF8.GetBytes(ContentFingerprint + "|one-authored-safe-cache|shovel|300-active-seconds|retain-progress"))
                    .Select(x => x.ToString("x2", System.Globalization.CultureInfo.InvariantCulture)));
            return this;
        }

        /// <summary>Opts this TEST_ONLY site-assignment profile into fixed-origin off-calendar
        /// six-second activity accounting. The companion remains outside tactical initiative.</summary>
        public TestOnlySharedWorldPolicy EnableOffCalendarActivity()
        {
            if (offCalendarActivityEnabled) return this;
            if (!expeditionAssignmentsEnabled)
                throw new InvalidOperationException("Off-calendar activity requires the persisted site-assignment profile.");
            offCalendarActivityEnabled = true;
            using (var hash = System.Security.Cryptography.SHA256.Create())
                ContentFingerprint = "TEST_ONLY.world-activity-v1-" + string.Concat(hash.ComputeHash(
                    System.Text.Encoding.UTF8.GetBytes(ContentFingerprint + "|off-calendar-activity-v1|origin-six-second-buckets|shared-action-work-exclusion"))
                    .Select(x => x.ToString("x2", System.Globalization.CultureInfo.InvariantCulture)));
            return this;
        }

        public static TestOnlySharedWorldPolicy WithFishingTrap(SharedFishingTrapFixture fishingTrap,uint seed=1)
        {
            if(fishingTrap==null)throw new ArgumentNullException(nameof(fishingTrap));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed));
            policy.fishingTrap=fishingTrap;policy.fishingTrapProfiles=new[]{fishingTrap};
            policy.ContentFingerprint=FishingTrapFingerprint(policy.ContentFingerprint,fishingTrap);
            return policy;
        }
        public static TestOnlySharedWorldPolicy WithFishingTrapAndRepair(SharedFishingTrapFixture fishingTrap,
            SharedRepairFixture repair, SharedCraftingFixture crafting = null, uint seed = 1, int walkingSpeed = 30)
        {
            if (fishingTrap == null || repair == null) throw new ArgumentNullException(fishingTrap == null ? nameof(fishingTrap) : nameof(repair));
            var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed), null,
                crafting ?? new SharedCraftingFixture(toolHp: 0), repair, walkingSpeed);
            policy.fishingTrap = fishingTrap; policy.fishingTrapProfiles = new[] { fishingTrap };
            policy.ContentFingerprint = FishingTrapFingerprint(policy.ContentFingerprint, fishingTrap);
            return policy.EnableExpeditionAssignments();
        }
        /// <summary>Physical schema38 witness with multiple independently supplied world Trap profiles.
        /// Distinct opportunities may reference one physical creature at the same site; response allocation remains single-body.</summary>
        public static TestOnlySharedWorldPolicy WithFishingTraps(System.Collections.Generic.IEnumerable<SharedFishingTrapFixture> profiles,uint seed=1)
        {
            if(profiles==null)throw new ArgumentNullException(nameof(profiles));
            var rows=profiles.OrderBy(x=>x?.TrapIdentity,StringComparer.Ordinal).ToArray();
            if(rows.Length<2||rows.Any(x=>x==null)||rows.SelectMany(x=>new[]{x.TrapIdentity,x.OpportunityIdentity,
                x.BaitLotIdentity,x.SupportIdentity,x.ReceiverIdentity,x.ReceiverSupportIdentity,x.StockVersionIdentity})
                    .Distinct(StringComparer.Ordinal).Count()!=rows.Length*7
                ||rows.GroupBy(x=>x.CreatureIdentity,StringComparer.Ordinal).Any(g=>g.Select(x=>x.SiteIdentity).Distinct(StringComparer.Ordinal).Count()!=1)
                ||rows.GroupBy(x=>x.SetterId,StringComparer.Ordinal).Any(g=>g.Select(x=>x.ProficiencyRank).Distinct().Count()!=1))
                throw new ArgumentException("Multiple Trap profiles require distinct physical operation identities, shared candidate bodies confined to one site, and a consistent fishing-tackle rank per setter.",nameof(profiles));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed));
            policy.fishingTrapProfiles=rows;policy.fishingTrap=rows[0];
            policy.ContentFingerprint=FishingTrapSetFingerprint(policy.ContentFingerprint,rows);
            return policy;
        }
        /// <summary>Historical schema35 authority used only to verify old save replay. New sessions
        /// must use schema37, which requires actual stock and physical equipment records.</summary>
        public static TestOnlySharedWorldPolicy WithLegacyFishingTrap(SharedFishingTrapFixture fishingTrap,uint seed=1)
        {
            if(fishingTrap==null)throw new ArgumentNullException(nameof(fishingTrap));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed));
            policy.fishingTrap=fishingTrap;policy.fishingTrapProfiles=new[]{fishingTrap};policy.fishingTrapLegacy=true;
            policy.ContentFingerprint=LegacyFishingTrapFingerprint(policy.ContentFingerprint,fishingTrap);
            return policy;
        }
        /// <summary>Historical schema36 authority used to verify the bait/timing-only save projection.</summary>
        public static TestOnlySharedWorldPolicy WithBaitOnlyFishingTrap(SharedFishingTrapFixture fishingTrap,uint seed=1)
        {
            if(fishingTrap==null)throw new ArgumentNullException(nameof(fishingTrap));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed:seed));
            policy.fishingTrap=fishingTrap;policy.fishingTrapProfiles=new[]{fishingTrap};policy.fishingTrapBaitOnly=true;
            policy.ContentFingerprint=BaitOnlyFishingTrapFingerprint(policy.ContentFingerprint,fishingTrap);
            return policy;
        }
        public TestOnlySharedWorldPolicy(RepeatingCrossbowFixture rangedCombat,SharedCombatFixture combat,int walkingSpeed=30,
            ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain)
            :this(combat,walkingSpeed,conditions,terrain)
        {
            if(combat==null||rangedCombat==null)throw new ArgumentException("Repeating crossbow combat requires its connected encounter and explicit shooter fixture.");
            this.rangedCombat=rangedCombat;ContentFingerprint=RepeatingCrossbowFixture.BindFingerprint(ContentFingerprint,rangedCombat);
        }
        private static void SyncCalendarBodies(Snapshot s)
        {
            foreach(var interval in s.WorldIntervals) {
                int start=checked((int)interval.LastStart);var before=s.TacticalActors.Single(x=>x.ActorId==interval.ActorId);
                if(before.LastRegularStart!=start){SoldierTacticalFeatures.ExpireStartMarker(s,interval.ActorId,start,s.Revision+1);s.TacticalActors=s.TacticalActors.Select(x=>x.ActorId==interval.ActorId?new ActorTacticalRecord(x.ActorId,start,interval.ReactionAvailable):x).ToArray();CharacterAdvancementRules.RegularStart(s,interval.ActorId,start);TestOnlySharedWorldPolicy.OverwatchRegularStart(s,interval.ActorId,start,s.Revision+1);}
                s.ActorMovement=s.ActorMovement.Select(x=>x.ActorId==interval.ActorId?new ActorMovementRecord(x.ActorId,x.BaseWalkingSpeed,start):x).ToArray();
            }
        }
        private static void ObserveCalendar(Snapshot s)
        {
            var e=s.Encounter;if(e==null)return;int slot=checked((int)s.WorldSchedule.ProcessedSlot);
            if(slot!=e.TurnOrdinal)s.Encounter=new FixedEncounterRecord(e.Id,e.Origin,e.Order,e.StartRevisions.Concat(new[]{s.Revision+1}),e.ObservedOrdinals.Concat(new[]{slot}));
            if(s.InventoryCombat)s.InventoryTurnActor=s.Encounter.CurrentActor;
        }
        private static void PauseParticipantWork(Snapshot s,string actor)
        {
            PauseFishingTrapForActor(s,actor);
            foreach(var job in s.FormulaWork.Where(x=>x.WorkerId==actor&&x.Status==FormulaWorkStatus.Working).ToArray())PauseFormula(s,job);
            foreach(var crop in s.Crops.Where(x=>x.Tasks.Any(t=>t.WorkerId==actor&&t.Status==CropWorkStatus.Working)).ToArray())CampGreens.Pause(s,crop.Id,actor);
            foreach(var fill in s.WaterFills.Where(x=>x.WorkerId==actor&&x.Status==WaterFillStatus.Working).ToArray())WaterFilling.Pause(s,fill);
            foreach(var intake in s.Intakes.Where(x=>x.ActorId==actor&&x.Status==IntakeStatus.Working).ToArray())OrdinaryInventory.Interrupt(s,intake,IntakeStatus.CombatInterrupted);
            foreach(var attempt in s.SupplyCacheAttempts.Where(x=>x.ActorId==actor&&x.Status==SupplyCacheAttemptStatus.Working).ToArray())InterruptSupplyCacheAttempt(s,attempt);
            foreach(var attempt in s.HarvestAttempts.Where(x=>x.WorkerId==actor&&x.Status==HarvestAttemptStatus.Working).ToArray())PauseHarvest(s,attempt);
        }
        private string EnterCalendarCombat(Snapshot s,Command c)
        {
            if(c.Inventory!=null||c.Combat!=null||c.Target!=""||c.X!=0||c.Y!=0||!s.WorldSchedule.Order.Contains(c.Actor))return "InvalidSharedCombatEntry";
            if(s.InventoryCombat)return "AlreadyInTacticalControl";
            if(s.WorldTraversals.Length!=0)return "OffGridCombatEntryUnsupported";
            if(s.WorldSchedule.ProcessedSlot>=int.MaxValue)return "CombatCalendarCapacityReached";
            if(routeMotionFixture!=null&&s.RouteTravelSpatial.Any(x=>!x.Detached
                &&(x.X.Denominator!=1||x.Y.Denominator!=1)))return "OffGridCombatEntryUnsupported";
            if(routeTravelFixture!=null)
                foreach(var travel in s.RouteTravels.Where(x=>x.Status==ExpeditionRouteTravelStatus.Moving).ToArray())
                    SetRouteTravel(s,travel.With(travel.NominalEffort,ExpeditionRouteTravelStatus.Paused));
            if(routeMotionFixture!=null)
                foreach(var spatial in s.RouteTravelSpatial.Where(x=>!x.Detached).ToArray())
                    SetRouteSpatial(s,spatial.With(spatial.X,spatial.Y,true));
            if(s.Encounter==null)s.Encounter=new FixedEncounterRecord("world.fixed-conflict",s.WorldSchedule.Origin,s.WorldSchedule.Order,new[]{s.Revision+1},new[]{(int)s.WorldSchedule.ProcessedSlot});
            foreach(string actor in s.WorldSchedule.Order)PauseParticipantWork(s,actor);
            // Starts have already been processed by shared advancement. Do not replay one here.
            s.InventoryCombat=true;s.InventoryTurnActor=s.Encounter.CurrentActor;s.InventoryInteractions=Interval(s,s.Encounter.CurrentActor).Interactions;
            PauseIncompatibleCacheExcavation(s);
            PauseIncompatibleRemedies(s);PauseIncompatibleRepairs(s);PauseIncompatibleManufacturing(s);
            PauseIncompatibleHarvesting(s);return null;
        }
        internal static bool PendingCalendarChoice(Snapshot s)=>s.MeleeAttacks.Any(x=>x.Pending)||TestOnlyClubAttackPolicy.PendingMove(s)!=null
            ||TestOnlyClubAttackPolicy.CurrentPressOffer(s)!=null||s.OverwatchOffers.Any(x=>x.Status==OverwatchOfferStatus.Pending)
            ||s.ReadyOccurrences.Any(x=>x.Status==ReadyOccurrenceStatus.Pending)
            ||s.OverwatchRiderChoices.Any(x=>x.Status==OverwatchRiderChoiceStatus.Pending)||PendingCommandStepOffer(s)!=null
            ||s.InventoryCombat&&s.HuntingTrapTriggers.Any(x=>x.Status==HuntingTrapTriggerStatus.Pending)
            ||s.DefensiveFormations.Any(x=>x.Active&&x.Shifts.Any(y=>y.Status==DefensiveFormationShiftStatus.AwaitingResponse
                ||y.Status==DefensiveFormationShiftStatus.Moving));
        private static bool ResolvedConflict(Snapshot s)=>s.Lives.Single(x=>x.ActorId==AdditionalTacticalActor.Id).Dead;
        private string ResolveCalendarCombat(Snapshot s,Command c)
        {
            if(c.Kind==CommandKind.AdvanceClock)return "TacticalDecisionClockPaused";
            var formationResponse=PendingDefensiveFormationShift(s);
            if(formationResponse!=null) {
                if(c.Kind!=CommandKind.RespondDefensiveFormation)return "DefensiveFormationChoicePending";
                string formationError=ResolveDefensiveFormationResponse(s,c);
                if(formationError==null) {
                    string formationTriggerError=QueueCompletedMovementOverwatch(s);if(formationTriggerError!=null)return formationTriggerError;
                    NormalizePendingOverwatchOffers(s);NormalizePendingReadyOccurrences(s);FinishDefensiveFormationContinuation(s,c.Id);
                }
                return formationError;
            }
            if(c.Kind==CommandKind.RespondDefensiveFormation)return "NoPendingDefensiveFormationChoice";
            var commandStep=PendingCommandStepOffer(s);
            if(commandStep!=null) {
                if(c.Kind!=CommandKind.RespondCommandStep)return "CommandStepChoicePending";
                string stepError=ResolveCommandStepResponse(s,c);
                if(stepError==null){string queued=QueueCompletedMovementOverwatch(s);if(queued!=null)return queued;NormalizePendingOverwatchOffers(s);NormalizePendingReadyOccurrences(s);}
                return stepError;
            }
            if(c.Kind==CommandKind.RespondCommandStep)return "NoPendingCommandStepChoice";
            if(c.Kind==CommandKind.OfferCommandStep)return ResolveCommandStepOffer(s,c);
            var riderChoice=s.OverwatchRiderChoices.SingleOrDefault(x=>x.Status==OverwatchRiderChoiceStatus.Pending);
            if(riderChoice!=null) {
                if(c.Kind!=CommandKind.ResolveOverwatchRider)return "OverwatchRiderChoicePending";
                string riderError=ResolveOverwatchRiderChoice(s,c);if(riderError!=null)return riderError;
                NormalizePendingReadyOccurrences(s);ResolveOrderedHuntingTrapTrigger(s);
                bodies.ContinueTacticalFlow(s);string queueError=QueueCompletedMovementOverwatch(s);if(queueError!=null)return queueError;
                NormalizePendingOverwatchOffers(s);NormalizePendingReadyOccurrences(s);
                FinishDefensiveFormationContinuation(s,c.Id);
                return null;
            }
            var pendingMove=TestOnlyClubAttackPolicy.PendingMove(s);
            if(pendingMove==null) {
                var postStep=NextPostStepChoice(s);
                if(postStep==PostStepChoiceKind.Ready) {
                    if(c.Kind!=CommandKind.RespondReady)return "ReadyActionChoicePending";
                    string readyError=ResolveReadyResponse(s,c);if(readyError!=null)return readyError;
                    NormalizePendingReadyOccurrences(s);ResolveOrderedHuntingTrapTrigger(s);
                    if(!s.MeleeAttacks.Any(x=>x.Pending)) {
                        bodies.ContinueTacticalFlow(s);string queueError=QueueCompletedMovementOverwatch(s);if(queueError!=null)return queueError;
                        NormalizePendingOverwatchOffers(s);NormalizePendingReadyOccurrences(s);
                        ResolveOrderedHuntingTrapTrigger(s);FinishDefensiveFormationContinuation(s,c.Id);
                    }
                    return null;
                }
                if(postStep==PostStepChoiceKind.Overwatch) {
                    if(c.Kind!=CommandKind.RespondOverwatch)return "OverwatchChoicePending";
                    string responseError=ResolveOverwatchResponse(s,c);if(responseError!=null)return responseError;
                    NormalizePendingReadyOccurrences(s);ResolveOrderedHuntingTrapTrigger(s);
                    if(!s.OverwatchRiderChoices.Any(x=>x.Status==OverwatchRiderChoiceStatus.Pending)) {
                        bodies.ContinueTacticalFlow(s);string queueError=QueueCompletedMovementOverwatch(s);if(queueError!=null)return queueError;
                        NormalizePendingOverwatchOffers(s);NormalizePendingReadyOccurrences(s);
                        ResolveOrderedHuntingTrapTrigger(s);
                        FinishDefensiveFormationContinuation(s,c.Id);
                    }
                    return null;
                }
                if(postStep==PostStepChoiceKind.Press&&c.Kind==CommandKind.RespondOverwatch)return "EarlierPostStepChoicePending";
            } else if(c.Kind==CommandKind.RespondOverwatch)return "OpportunityChoicePending";
            if(c.Kind==CommandKind.RespondReady)return "NoPendingReadyChoice";
            if(c.Kind==CommandKind.RespondOverwatch)return "NoPendingOverwatchChoice";
            if(c.Kind==CommandKind.ResolveOverwatchRider)return "NoPendingOverwatchRiderChoice";
            if(HasMovingDefensiveFormation(s)&&c.Kind!=CommandKind.RespondOpportunityAttack&&c.Kind!=CommandKind.RespondPress
                &&c.Kind!=CommandKind.ResolveKnockout)return "DefensiveFormationContinuationPending";
            if(c.Kind==CommandKind.TacticalAssessment)return ResolveTacticalAssessment(s,c);
            if(c.Kind==CommandKind.ActivateDefensiveFormation)return ResolveDefensiveFormation(s,c);
            if(c.Kind==CommandKind.SuppressionFire) {
                string error=ResolveSuppressionFire(s,c);if(error==null)NormalizePendingOverwatchOffers(s);return error;
            }
            if(c.Kind==CommandKind.AttackRepeatingCrossbow||c.Kind==CommandKind.ReloadRepeatingCrossbow
                ||c.Kind==CommandKind.WarningShot||c.Kind==CommandKind.CoveringFire) {
                string error=ResolveRepeatingCrossbow(s,c);if(error==null)NormalizePendingOverwatchOffers(s);return error;
            }
            if(c.Kind==CommandKind.DispatchConditionEvent) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                string error=bodies.Resolve(s,c);if(error==null){PauseIncompatibleWork(s);NormalizePendingOverwatchOffers(s);}return error;
            }
            if(c.Kind==CommandKind.EndRegularTurn||c.Kind==CommandKind.EndFixedEncounter) {
                if(c.Inventory!=null||c.Combat!=null||c.X!=0||c.Y!=0||c.Actor!=s.Encounter.CurrentActor||c.Target!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                bool exit=c.Kind==CommandKind.EndFixedEncounter;
                if(exit&&!ResolvedConflict(s))return "ConflictNotResolved";
                if(TestOnlyClubAttackPolicy.Aware(s,c.Actor)&&!TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
                if(s.WorldSchedule.ProcessedSlot>=int.MaxValue-1)return "CombatCalendarCapacityReached";
                ExpireOverwatchSnares(s,c.Actor,s.Encounter.TurnOrdinal,s.Revision+1);
                CharacterAdvancementRules.EndRegularTurn(s,c.Actor,s.Encounter.TurnOrdinal);
                string timeFailure=AdvanceTo(s,s.WorldSchedule.Start(s.WorldSchedule.ProcessedSlot+1),exit,c);
                if(timeFailure!=null)return timeFailure;
                if(s.ManufacturingAdvance!=null)return null;
                s.InventoryInteractions=Interval(s,s.Encounter.CurrentActor).Interactions;
                // Time and consequences are committed even if the exit predicate no longer holds.
                if(exit&&ResolvedConflict(s)&&!PendingCalendarChoice(s)){s.InventoryCombat=false;s.InventoryTurnActor="";s.InventoryInteractions=0;CharacterAdvancementRules.TacticalExit(s);}
                return null;
            }
            if(!s.WorldSchedule.Order.Contains(c.Actor))return "ActorOutsideEncounter";
            if(c.Kind==CommandKind.SelectCombatStance&&c.Combat?.Stance==(int)CombatStance.Mobile)return "SharedMobileDistanceNotImplemented";
            if((c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.AttackUnarmed)&&!s.WorldSchedule.Order.Contains(c.Target))return "TargetOutsideEncounter";
            if(c.Kind==CommandKind.EncounterDash) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                if(c.Inventory!=null||c.Combat!=null||c.X!=0||c.Y!=0||c.Actor!=s.Encounter.CurrentActor||c.Target!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
                if(Interval(s,c.Actor).ActionSpent)return "ActionAlreadySpent";
                return PayRun(s,c.Actor);
            }
            if(c.Kind==CommandKind.ActivateTacticalReposition) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                return CharacterAdvancementRules.ActivateTacticalReposition(s,c);
            }
            if(c.Kind==CommandKind.DesignateOverwatch) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                return ResolveOverwatchDesignation(s,c);
            }
            if(c.Kind==CommandKind.Ready)return ResolveReadyDeclaration(s,c);
            if(c.Kind==CommandKind.CurePeriodicRider)return ResolvePeriodicMedicine(s,c);
            if((c.Kind==CommandKind.HandleInventory||c.Kind==CommandKind.HandleVessel)&&s.SchemaVersion>=Snapshot.SupplyCacheSchema) {
                if(PendingCalendarChoice(s))return "TacticalChoicePending";
                if(c.Actor!=s.Encounter.CurrentActor)return "WrongRegularTurn";
                if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
                if(AvailableHands(s,c.Actor)<1)return "HandlingHandRequired";
                var interval=Interval(s,c.Actor);
                if(s.InventoryInteractions!=interval.Interactions)return "TacticalInteractionLedgerMismatch";
                if(interval.Interactions>=2)return "InteractionBudgetUnavailable";
                if(interval.Interactions==1&&interval.ActionSpent)return "ActionAlreadySpent";
                if(interval.Interactions==1&&!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
                string handling=inventory.Resolve(s,c);if(handling!=null)return handling;
                var spent=Interval(s,c.Actor).SpendInteraction();SetInterval(s,spent);s.InventoryInteractions=spent.Interactions;
                PauseIncompatibleWork(s);return null;
            }
            if((c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.AttackUnarmed)&&AttackingFromActiveOverwatchZone(s,c.Actor,c.Target))
                return "OverwatchAttackTriggerNotImplemented";
            bool action=c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.AttackUnarmed||c.Kind==CommandKind.Disengage||c.Kind==CommandKind.Dodge;
            string failure=bodies.Resolve(s,c);if(failure!=null)return failure;
            string triggerError=QueueCompletedMovementOverwatch(s);if(triggerError!=null)return triggerError;
            NormalizePendingOverwatchOffers(s);
            FinishDefensiveFormationContinuation(s,c.Id);
            if(action)SetInterval(s,Interval(s,c.Actor).PayAction());
            PauseIncompatibleWork(s);return null;
        }
    }
}
#endif
