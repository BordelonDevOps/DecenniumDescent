#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ConnectedExpeditionSession NewDeclaredGeometryExpedition() => ConnectedExpeditionSession.StartWithDeclaredGeometry(
            ClericInitialSelection.AuthoredExample(), ClericRepertoireSelection.AuthoredExample(),
            ClericMilestoneDeclaration.AuthoredExample(), BishopEntryRecord.Announced());

        private static void AddDeclaredGeometryCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac03_declared_geometry_strain_dash_queries_cross_actual_start", () => {
                const string hero = ConnectedExpeditionSession.Hero;
                foreach (bool resume in new[] { false, true }) {
                    var session = NewDeclaredGeometryExpedition(); var codec = new SnapshotCodec();
                    // Two genuine missed provisioning boundaries yield Strain4. No state injection.
                    ClericCommit(session, hero, CommandKind.AdvanceClock, x: 172804, y: 1);
                    var late = ShortRestCapture(session);
                    Require(ExpeditionStrainRules.Current(late, hero).Level == 4 && late.RuleClock == new RuleTime(172804),
                        "The real provisioning route did not reach the expected late Strain4 interval.");
                    string suffix = resume ? "resume" : "begin";
                    Command Move(CommandKind kind, string id, int dx = 0) => new Command("geometry.lock." + suffix + "." + id,
                        hero, ShortRestCapture(session).Revision, kind, kind == CommandKind.BeginWorldStep ? "run" : "", dx, 0);
                    var run = Move(CommandKind.BeginWorldStep, "paid", 1);
                    Require(session.QueryCastingCommand(ExpeditionSeat.Player, run).Admissible, "Initial strained run was unavailable.");
                    BishopCommit(session, run);
                    var paid = ShortRestCapture(session); var locked = paid.ExpeditionDashLocks.Single(x => x.ActorId == hero);
                    Require(!locked.InitiativeAnchored && locked.AppliedAt == late.RuleClock && locked.Deadline == late.RuleClock.AddSeconds(6),
                        "Paid ordinary run did not retain its actual six-second lock.");
                    if (resume) {
                        BishopCommit(session, Move(CommandKind.SuspendWorldStep, "suspend"));
                        var reuse = Move(CommandKind.ResumeWorldStep, "same-interval-reuse");
                        Require(session.QueryCastingCommand(ExpeditionSeat.Player, reuse).Admissible, "Already-paid same-interval reuse was locked.");
                        BishopCommit(session, reuse); BishopCommit(session, Move(CommandKind.SuspendWorldStep, "suspend-again"));
                        Require(ShortRestCapture(session).ExpeditionDashLocks.Single(x => x.ActorId == hero).AppliedAt == locked.AppliedAt,
                            "Same-interval resume repaid or moved the lock.");
                    } else {
                        int speed = checked((int)TestOnlyClubAttackPolicy.WalkingSpeed(paid, hero));
                        ClericCommit(session, hero, CommandKind.AdvanceClock, x: 15, y: speed);
                        Require(ShortRestCapture(session).WorldTraversals.Length == 0, "The actual run did not finish before the next Start.");
                    }
                    PostRecoveryAdvanceTo(session, new RuleTime(172806));
                    var fresh = ShortRestCapture(session); var interval = fresh.WorldIntervals.Single(x => x.ActorId == hero);
                    Require(interval.LastStart > late.WorldIntervals.Single(x => x.ActorId == hero).LastStart
                        && !interval.ActionSpent && !interval.DashPaid && ExpeditionStrainRules.DashLocked(fresh, hero),
                        "The control did not cross an actual refreshed Start while the paid lock remained active.");
                    BishopCheckpoint(session, directory, "geometry-lock-" + suffix);
                    var denied = Move(resume ? CommandKind.ResumeWorldStep : CommandKind.BeginWorldStep, "locked", resume ? 0 : -1);
                    var bytes = codec.Encode(ShortRestCapture(session)); var query = session.QueryCastingCommand(ExpeditionSeat.Player, denied);
                    File.WriteAllText(Path.Combine(directory, "geometry-lock-" + suffix + ".query.json"), System.Text.Json.JsonSerializer.Serialize(query));
                    Require(!query.Admissible && query.Code == "ExpeditionStrainDashLocked", "Run/resume query omitted the actual cross-Start Strain lock: " + query.Code);
                    Require(session.Submit(ExpeditionSeat.Player, denied).Response == ExpeditionResponse.Unavailable
                        && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Locked query/execution changed canonical state.");
                    PostRecoveryAdvanceTo(session, locked.Deadline);
                    var expiry = Move(resume ? CommandKind.ResumeWorldStep : CommandKind.BeginWorldStep, "expiry", resume ? 0 : -1);
                    Require(session.QueryCastingCommand(ExpeditionSeat.Player, expiry).Admissible, "Dash was not admitted at exact lock expiry.");
                    BishopCommit(session, expiry); BishopCheckpoint(session, directory, "geometry-lock-" + suffix + "-expired");
                }
            });
            cases.Add("tac03_declared_geometry_connected_weighted_interrupts_and_continue", () => RunDeclaredGeometryCampaign(directory));
            cases.Add("tac03_declared_geometry_paid_dash_suspend_authority_and_restore", () => {
                const string hero = ConnectedExpeditionSession.Hero;
                var session = NewDeclaredGeometryExpedition(); var codec = new SnapshotCodec(); var start = ShortRestCapture(session);
                var run = new Command("geometry.dash.begin", hero, start.Revision, CommandKind.BeginWorldStep, "run", 1, 0);
                Require(session.QueryCastingCommand(ExpeditionSeat.Player, run).Admissible, "Declared running was not exposed through ordinary legality.");
                BishopCommit(session, run); var paid = ShortRestCapture(session); var interval = paid.WorldIntervals.Single(x => x.ActorId == hero);
                Require(interval.DashPaid && interval.ActionSpent && interval.MovementSpent == default
                    && paid.RuleClock == start.RuleClock && paid.RandomState == start.RandomState, "Running did not pay its actual Action before travel.");
                var stable = codec.Encode(paid);
                Require(session.Submit(ExpeditionSeat.Player, run).Response == ExpeditionResponse.Duplicate
                    && stable.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Duplicate Dash repaid or refunded resources.");
                var suspend = new Command("geometry.dash.suspend", hero, paid.Revision, CommandKind.SuspendWorldStep);
                session.SetSeatEnabled(ExpeditionSeat.Player, false);
                Require(session.QueryCastingCommand(ExpeditionSeat.Player, suspend).Code == "NotAuthorized"
                    && session.Submit(ExpeditionSeat.Player, suspend).Response == ExpeditionResponse.NotAuthorized
                    && stable.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Revoked seat suspended another controller's movement.");
                session.SetSeatEnabled(ExpeditionSeat.Player, true); BishopCommit(session, suspend);
                BishopCheckpoint(session, directory, "geometry-paid-dash-suspended");
                var paused = ShortRestCapture(session);
                Require(paused.WorldTraversals.Single().Status == WorldTraversalStatus.Suspended
                    && paused.WorldIntervals.Single(x => x.ActorId == hero).DashPaid, "Saved suspension discarded the paid Dash.");
                BishopCommit(session, new Command("geometry.dash.resume", hero, paused.Revision, CommandKind.ResumeWorldStep));
                int speed = checked((int)TestOnlyClubAttackPolicy.WalkingSpeed(paused, hero));
                ClericCommit(session, hero, CommandKind.AdvanceClock, x: 15, y: speed);
                var after = ShortRestCapture(session); interval = after.WorldIntervals.Single(x => x.ActorId == hero);
                Require(after.WorldTraversals.Length == 0 && after.Actors.Single(x => x.Id == hero).X == 1
                    && interval.DashPaid && interval.ActionSpent && interval.MovementSpent == new RuleQuantity(5)
                    && after.RuleClock == new RuleTime(15, speed), "Resumed Dash changed actual cost, time or destination.");
                BishopCheckpoint(session, directory, "geometry-paid-dash-continued");
            });
            cases.Add("tac03_declared_geometry_genesis_and_verified_restore", () => {
                var session = NewDeclaredGeometryExpedition(); var state = ShortRestCapture(session); var codec = new SnapshotCodec();
                Require(state.WireSchemaVersion == 113 && state.SchemaVersion == Snapshot.SurpriseEntrySchema
                    && state.BishopEntry != null && state.PostRecoveryEncounter != null && state.ConnectedClericLongRest,
                    "Declared geometry lost its complete inherited composition.");
                Require(state.DeclaredGeometry != null && DeclaredGeometryProfile.HasExpectedLayout(state)
                    && state.ObservationMapWidth == 12 && state.ObservationMapHeight == 5, "Declared geometry was not selected.");
                var bytes = codec.Encode(state); var decoded = codec.Decode(bytes);
                Require(bytes.SequenceEqual(codec.Encode(decoded)) && bytes.SequenceEqual(codec.Encode(state.Copy())),
                    "Declared map clone or codec changed canonical state.");
                string path = Path.Combine(directory, "declared-geometry-genesis.ddsave"); session.Save(path); session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Verified restoration changed declared genesis.");
                var old = NewBishopExpedition(); var oldState = ShortRestCapture(old); var oldBytes = codec.Encode(oldState);
                Require(oldState.WireSchemaVersion == 112 && oldState.DeclaredGeometry == null
                    && oldState.ObservationMapWidth == 5 && oldBytes.SequenceEqual(codec.Encode(codec.Decode(oldBytes))),
                    "Existing Bishop geometry/encoding changed.");
                Throws<ArgumentException>(() => old.Restore(path));
                Require(oldBytes.SequenceEqual(codec.Encode(ShortRestCapture(old))), "Old-profile denial mutated its session.");
            });
            cases.Add("tac03_declared_geometry_support_cost_and_corner_controls", () => {
                var state = ShortRestCapture(NewDeclaredGeometryExpedition());
                Require(SharedDeclaredGeometry.SupportsAnchorAt(state, 11, 4) && !SharedDeclaredGeometry.SupportsAnchorAt(state, 12, 4)
                    && !SharedDeclaredGeometry.SupportsAnchorAt(state, -1, 4) && !SharedDeclaredGeometry.SupportsAnchorAt(state, int.MaxValue, 0),
                    "Declared bounds used the legacy extent or allowed invalid coordinates.");
                foreach (var cell in DeclaredGeometryProfile.Cells)
                    Require(!SharedDeclaredGeometry.SupportsAnchorAt(state, cell.X, cell.Y), "A blocker became a supported anchor.");
                Require(DeclaredGeometryProfile.TerrainCostAt(state, 5, 2) == 2 && DeclaredGeometryProfile.TerrainCostAt(state, 6, 2) == 3
                    && DeclaredGeometryProfile.TerrainCostAt(state, 5, 3) == 1, "Trusted destination costs changed.");
                var both = WorldSpatialQueries.Step(state, ConnectedExpeditionSession.Hero, 6, 0, 7, 1, true, true,
                    (x, y) => SharedDeclaredGeometry.SupportsAnchorAt(state, x, y));
                var one = WorldSpatialQueries.Step(state, ConnectedExpeditionSession.Hero, 5, 1, 6, 2, true, true,
                    (x, y) => SharedDeclaredGeometry.SupportsAnchorAt(state, x, y));
                Require(both == SpatialStepFailure.Blocked && one == SpatialStepFailure.None,
                    "Movement corner support was confused with ray corner intersection.");
                var missing = state.Copy(); missing.DeclaredGeometry = null;
                Require(!SharedDeclaredGeometry.SupportsAnchorAt(missing, 1, 1), "Missing selected binding fell back to legacy geometry.");
                Throws<ArgumentException>(() => DeclaredGeometryProfile.TerrainCostAt(missing, 1, 1));
                var old = ShortRestCapture(NewBishopExpedition());
                Require(!SharedDeclaredGeometry.SupportsAnchorAt(old, 5, 3) && SharedDeclaredGeometry.SupportsAnchorAt(old, 4, 3),
                    "Legacy floor expanded implicitly.");
            });
            cases.Add("tac03_declared_geometry_trusted_layout_and_terrain_rejection", () => {
                var state = ShortRestCapture(NewDeclaredGeometryExpedition()); var codec = new SnapshotCodec(); var before = codec.Encode(state);
                var width = state.Copy(); width.ObservationMapWidth = 13;
                Throws<ArgumentException>(() => codec.Encode(width));
                var cells = state.Copy(); cells.ObservationCells = cells.ObservationCells.Where(x => x.X != 6).ToArray();
                Throws<ArgumentException>(() => codec.Encode(cells));
                var binding = state.Copy(); binding.DeclaredGeometry = null;
                Throws<ArgumentException>(() => codec.Encode(binding));
                Throws<ArgumentException>(() => new DeclaredGeometryRecord(state.DeclaredGeometry.PredecessorFingerprint,
                    DeclaredGeometryProfile.DeclarationDigest, new[] { new DeclaredTerrainCell(5, 2, 1), new DeclaredTerrainCell(6, 2, 3) }));
                Require(before.SequenceEqual(codec.Encode(state)), "Forgery checks modified the original geometry state.");
            });
        }

        private static void RunDeclaredGeometryCampaign(string directory)
        {
            const string hero = ConnectedExpeditionSession.Hero, companion = ClericRpProfile.Actor, npc = PostRecoveryEncounterDefinition.Actor;
            var session = FundBishop(directory, expedition: NewDeclaredGeometryExpedition());
            int sequence = 0, acceptedOpportunities = 0, acceptedPress = 0;
            Command Make(CommandKind kind, string actor, string target = "", int x = 0, int y = 0, CombatRequest combat = null)
                => new Command("geometry.campaign." + (++sequence), actor, ShortRestCapture(session).Revision, kind, target, x, y, combat: combat);
            void Commit(Command command) => BishopCommit(session, command);
            void Step(int x, int y)
            {
                var state = ShortRestCapture(session);
                if (state.Actors.Single(a => a.Id == hero).X > 4) {
                    var bytes = new SnapshotCodec().Encode(state);
                    var options = session.DiscoverCastingCommands(ExpeditionSeat.Player, hero);
                    string beforeDiscovery = System.Text.Json.JsonSerializer.Serialize(options);
                    Require(bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))), "Acting hero discovery mutated state.");
                    string save = Path.Combine(directory, "geometry-acting-hero-discovery.ddsave"); session.Save(save); session.Restore(save);
                    string afterDiscovery = System.Text.Json.JsonSerializer.Serialize(session.DiscoverCastingCommands(ExpeditionSeat.Player, hero));
                    File.WriteAllText(Path.Combine(directory, "geometry-acting-hero-discovery.before.json"), beforeDiscovery);
                    File.WriteAllText(Path.Combine(directory, "geometry-acting-hero-discovery.after.json"), afterDiscovery);
                    Require(beforeDiscovery == afterDiscovery && bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                        "Acting hero discovery changed across actual restore.");
                    var chosen = options.SingleOrDefault(o => o.Command.Kind == CommandKind.TacticalStep && o.Command.X == x && o.Command.Y == y);
                    Require(chosen != null && chosen.Query.Admissible && chosen.Query.Costs.Single(c => c.Kind == "movement-feet").Amount == 10,
                        "Discovery did not offer the actual beyond-boundary Difficult destination and cost.");
                    sequence++; Commit(chosen.Command);
                } else Commit(Make(CommandKind.TacticalStep, hero, state.Encounter.CurrentTurnId, x, y));
                for (int pending = 0; pending < 16; pending++) {
                    state = ShortRestCapture(session);
                    var move = TestOnlyClubAttackPolicy.PendingMove(state);
                    if (move != null) {
                        BishopCheckpoint(session, directory, "geometry-pending-opportunity-" + sequence);
                        string reactor = move.Reactors[move.ResponseIndex]; bool accept = reactor == npc;
                        Commit(Make(CommandKind.RespondOpportunityAttack, reactor, move.Id,
                            combat: new CombatRequest(state.Encounter.CurrentTurnId, accept ? "TEST_ONLY.recovery-defender-club" : "", choice: accept)));
                        if (accept) acceptedOpportunities++;
                        continue;
                    }
                    var offer = TestOnlyClubAttackPolicy.CurrentPressOffer(state);
                    if (offer != null) {
                        BishopCheckpoint(session, directory, "geometry-pending-press-" + sequence);
                        Commit(Make(CommandKind.RespondPress, offer.ActorId, offer.Id,
                            combat: new CombatRequest(state.Encounter.CurrentTurnId, choice: true)));
                        acceptedPress++; continue;
                    }
                    return;
                }
                throw new Exception("Geometry interrupt chain did not finish.");
            }

            // Same paid approach and current inherited epoch as the accepted Bishop route.
            PostRecoveryStep(session, companion, 1, 0); PostRecoveryStep(session, companion, 1, 0); PostRecoveryStep(session, companion, 0, 1);
            PostRecoveryStep(session, hero, 1, 0); PostRecoveryStep(session, hero, 1, 0);
            var staged = ShortRestCapture(session); var epoch = staged.Reinforcement.Admission.Phase.Epoch;
            var duration = new RuleTime(30, TestOnlyClubAttackPolicy.WalkingSpeed(staged, hero));
            var earliest = new RuleTime(staged.RuleClock.Numerator * duration.Denominator + duration.Numerator * staged.RuleClock.Denominator,
                staged.RuleClock.Denominator * duration.Denominator);
            long slot = epoch.SlotAt(staged.RuleClock);
            while (epoch.Order[(int)(slot % epoch.Order.Count)] != "TEST_ONLY.later-defender" || epoch.Start(slot) < earliest) slot++;
            var arrival = epoch.Start(slot);
            PostRecoveryAdvanceTo(session, new RuleTime(arrival.Numerator * duration.Denominator - duration.Numerator * arrival.Denominator,
                arrival.Denominator * duration.Denominator));
            PostRecoveryStep(session, hero, 0, 1); BishopCheckpoint(session, directory, "geometry-entered");
            bool crossed = false, weighted = false; int deadEnds = 0;
            for (int turns = 0; turns < 120; turns++) {
                var state = ShortRestCapture(session); var encounter = state.Encounter;
                if (encounter == null) break;
                string actor = encounter.CurrentActor; var life = state.Lives.Single(x => x.ActorId == actor);
                var enemy = state.Lives.Single(x => x.ActorId == npc);
                if (life.Hp > 0 && !life.Dead) {
                    Commit(Make(CommandKind.SelectCombatStance, actor, combat: new CombatRequest(encounter.CurrentTurnId,
                        stance: (int)(actor == hero && weighted ? CombatStance.Aggressive : CombatStance.Guarded))));
                    if (enemy.Dead && deadEnds >= 3 && actor == hero) {
                        Commit(Make(CommandKind.EndFixedEncounter, hero, encounter.CurrentTurnId)); break;
                    }
                    if (actor == hero && !crossed) {
                        Step(4, 3); Step(5, 3); crossed = true;
                        BishopCheckpoint(session, directory, "geometry-tactical-beyond");
                    } else if (actor == hero && !weighted && state.Presses.Any(x => x.ActorId == npc && x.TargetId == hero)) {
                        var before = ShortRestCapture(session); Step(5, 2); var after = ShortRestCapture(session);
                        var move = after.TacticalMoves.Last(x => x.ActorId == hero && x.Kind == TacticalMoveKind.Ordinary);
                        Require(move.ToX == 5 && move.ToY == 2 && move.CostPaid == 10 && move.Status == TacticalMoveStatus.Completed
                            && after.WorldIntervals.Single(x => x.ActorId == hero).MovementSpent
                                - before.WorldIntervals.Single(x => x.ActorId == hero).MovementSpent == new RuleQuantity(10)
                            && before.RuleClock == after.RuleClock, "Tactical Difficult destination did not pay its actual ten-foot cost.");
                        Require(acceptedOpportunities > 0 && acceptedPress > 0 && !after.TacticalActors.Single(x => x.ActorId == npc).ReactionAvailable
                            && after.TacticalActors.Single(x => x.ActorId == npc).PressConsumed
                            && after.Actors.Single(x => x.Id == npc).X == 5 && after.Actors.Single(x => x.Id == npc).Y == 3,
                            "Actual attack-armed OA/Press did not follow through the paid movement parent.");
                        weighted = true; BishopCheckpoint(session, directory, "geometry-weighted-interrupt-complete");
                        var stable = new SnapshotCodec().Encode(ShortRestCapture(session));
                        var options = session.DiscoverCastingCommands(ExpeditionSeat.Player, hero);
                        var blocked = options.SingleOrDefault(o => o.Command.Kind == CommandKind.TacticalStep && o.Command.X == 6 && o.Command.Y == 1);
                        Require(blocked != null && !blocked.Query.Admissible && blocked.Query.Code == "BlockedTacticalStep",
                            "Acting hero discovery did not retain the declared blocked destination.");
                        Require(stable.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))), "Blocked discovery changed state.");
                        File.WriteAllText(Path.Combine(directory, "geometry-acting-hero-blocked.json"), System.Text.Json.JsonSerializer.Serialize(options));
                    } else if (actor == hero && weighted && !enemy.Dead) {
                        Commit(Make(CommandKind.AttackClub, hero, npc,
                            combat: new CombatRequest(encounter.CurrentTurnId, "TEST_ONLY.actor-club")));
                    } else if (actor == npc && !weighted) {
                        Commit(Make(CommandKind.AttackClub, npc, hero,
                            combat: new CombatRequest(encounter.CurrentTurnId, "TEST_ONLY.recovery-defender-club")));
                    } else if (actor == companion && !weighted && state.Lives.Single(x => x.ActorId == hero).Hp < 12
                        && state.ResonancePools.Single().Current >= 2) {
                        Commit(Make(CommandKind.UseHealingRite, companion, hero));
                    }
                }
                if (ShortRestCapture(session).Lives.Single(x => x.ActorId == npc).Dead) deadEnds++;
                PostRecoveryEnd(session);
            }
            var closed = ShortRestCapture(session);
            Require(crossed && weighted && closed.Encounter == null && closed.Lives.Single(x => x.ActorId == npc).Dead
                && closed.Lives.Where(x => x.ActorId == hero || x.ActorId == companion).All(x => x.Hp > 0 && !x.Dead),
                "Connected geometry route did not reach real opponent Dead closure with the party alive.");
            BishopCheckpoint(session, directory, "geometry-closed");

            void Walk(int dx, int dy, int multiplier, bool fractional)
            {
                // Settle actual time to the next hero Start in the current post-recovery epoch.
                // This gives an entire six-second interval for comparing real weighted expenditure.
                var waiting = ShortRestCapture(session); var currentEpoch = waiting.PostRecoveryEncounter.Admission.Epoch;
                long next = currentEpoch.SlotAt(waiting.RuleClock);
                while (currentEpoch.Order[(int)(next % currentEpoch.Order.Count)] != hero || currentEpoch.Start(next) <= waiting.RuleClock) next++;
                PostRecoveryAdvanceTo(session, currentEpoch.Start(next));
                var before = ShortRestCapture(session); int speed = checked((int)TestOnlyClubAttackPolicy.WalkingSpeed(before, hero));
                Require(speed > 0, "Connected ordinary geometry traversal lost walking capability.");
                Commit(Make(CommandKind.BeginWorldStep, hero, "walk", dx, dy));
                var started = ShortRestCapture(session);
                Require(started.WorldTraversals.Single(x => x.ActorId == hero).DistanceFeet == default,
                    "Starting geometry traversal spent a full edge immediately.");
                if (fractional) {
                    // One foot at destination terrain cost; old anchor remains authoritative only as an anchor.
                    ClericCommit(session, hero, CommandKind.AdvanceClock, x: 6 * multiplier, y: speed);
                    var partial = ShortRestCapture(session); var edge = partial.WorldTraversals.Single(x => x.ActorId == hero);
                    Require(edge.DistanceFeet == new RuleQuantity(1), "Weighted ordinary progress is not exact one-foot travel.");
                    Require(partial.WorldIntervals.Single(x => x.ActorId == hero).MovementSpent
                        - before.WorldIntervals.Single(x => x.ActorId == hero).MovementSpent == new RuleQuantity(multiplier),
                        "Partial ordinary travel did not pay its actual terrain cost.");
                    var point = WorldPositionResolver.Position(partial, hero);
                    Require(point.X.Denominator == 5 || point.Y.Denominator == 5, "Fractional physical position was rounded to an anchor.");
                    BishopCheckpoint(session, directory, "geometry-fractional-" + multiplier);
                    Commit(Make(CommandKind.SuspendWorldStep, hero));
                    var paused = new SnapshotCodec().Encode(ShortRestCapture(session));
                    BishopCheckpoint(session, directory, "geometry-paused-" + multiplier);
                    Require(paused.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))), "Paused restore reset progress or spending.");
                    Commit(Make(CommandKind.ResumeWorldStep, hero));
                    ClericCommit(session, hero, CommandKind.AdvanceClock, x: 24 * multiplier, y: speed);
                } else ClericCommit(session, hero, CommandKind.AdvanceClock, x: 30 * multiplier, y: speed);
                var after = ShortRestCapture(session);
                Require(!after.WorldTraversals.Any(x => x.ActorId == hero), "Weighted ordinary edge did not actually finish.");
                var priorActor = before.Actors.Single(x => x.Id == hero); var actor = after.Actors.Single(x => x.Id == hero);
                Require(actor.X == priorActor.X + dx && actor.Y == priorActor.Y + dy,
                    "Ordinary continuation changed the wrong position.");
                Require(after.WorldIntervals.Single(x => x.ActorId == hero).MovementSpent
                    - before.WorldIntervals.Single(x => x.ActorId == hero).MovementSpent == new RuleQuantity(5 * multiplier)
                    && after.RuleClock == new RuleTime(before.RuleClock.Numerator * speed + 30L * multiplier * before.RuleClock.Denominator,
                        before.RuleClock.Denominator * speed), "Ordinary destination terrain cost or elapsed time changed.");
            }
            Walk(-1, 0, 1, false); Walk(1, 0, 2, true); Walk(1, 0, 3, true); Walk(1, 0, 1, false);
            BishopCheckpoint(session, directory, "geometry-continued");
            var final = ShortRestCapture(session);
            File.WriteAllText(Path.Combine(directory, "geometry-connected-facts.json"), System.Text.Json.JsonSerializer.Serialize(new {
                scope = "Fresh finite campaign, real paid tactical crossing, weighted destination, actual OA/Press, Dead closure and weighted fractional ordinary travel",
                final.Revision, final.RuleClock, acceptedOpportunities, acceptedPress, final.TacticalMoves, final.PressOffers,
                final.WorldIntervals, final.WorldActivityIntervals, final.DeclaredGeometry
            }));
        }
    }
}
#endif
