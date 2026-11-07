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
        private static ConditionFixtureEvent CCApply(string id, string kind, string target = TestOnlyPolicy.ActorId,
            ConditionStamp? expires = null, ConditionStamp at = default, bool? inherited = null)
            => new ConditionFixtureEvent(target, ConditionOperation.Apply("event." + id, at, CJApp(id, kind, expires, inherited: inherited), kind == "Unconscious" ? id + ".prone" : ""));
        private static ConditionFixtureEvent CCGrant(string id, string target, ConditionStamp? expires, params string[] kinds)
            => new ConditionFixtureEvent(target, ConditionOperation.Grant("event." + id, default, new ConditionImmunityData(id, "owner", "ward", kinds, expires, "ward-end")));
        private static TestOnlyClubAttackPolicy CCPolicy(ConditionFixtureEvent[] events = null, uint seed = 1, long actorHp = 26, long companionHp = 26, bool prone = false, AdditionalTacticalActor third = null)
            => new TestOnlyClubAttackPolicy(seed: seed, actorHp: actorHp, companionHp: companionHp, actorProne: prone,
                actorBaseWalkingSpeed: 30, companionBaseWalkingSpeed: 30, tactical: new TacticalCombatFixture(third), conditions: new ConditionCombatFixture(events ?? Array.Empty<ConditionFixtureEvent>()));
        private static Command CCCommand(Simulation s, string id, string target = TestOnlyPolicy.ActorId)
            => new Command("condition." + (s.Capture().Revision + 1), target, s.Capture().Revision, CommandKind.DispatchConditionEvent, "event." + id);
        private static void CCDispatch(Simulation s, string id, string target = TestOnlyPolicy.ActorId) => CommitTac(s, CCCommand(s, id, target));
        private static ConditionLedger CCState(Simulation s, string actor = TestOnlyPolicy.ActorId) => TestOnlyClubAttackPolicy.ConditionsFor(s.Capture(), actor);
        private static void AddConditionCombatCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TacticalCombatFixture.Host(); var codec = new SnapshotCodec();
            cases.Add("condition_combat_schema12_is_explicit_and_release_excluded", () => {
                var p = CCPolicy(); var s = Clubs(p);
                Require(s.Capture().SchemaVersion == 12 && s.Capture().Conditions.Length == 2 && TacticalPolicy().Initial().SchemaVersion == 11, "Condition profile not explicitly selected.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s, p))), "Initial condition host cannot restore.");
                Throws<InvalidOperationException>(() => new Simulation(p, p.Initial(), ExecutionProfile.Release));
                Throws<ArgumentException>(() => new TestOnlyClubAttackPolicy(conditions: new ConditionCombatFixture()));
                Throws<ArgumentException>(() => CCApply("bad", "Blinded", expires: CJAt(1, 20)));
                Throws<ArgumentException>(() => CCApply("bad", "Blinded", at: CJAt(0, 10)));
            });
            cases.Add("condition_combat_pre_route_schema_reads_keep_their_original_journal_clock", () => {
                var snapshot = CCPolicy().Initial();
                var journal = snapshot.Conditions.Single(x => x.Target == TestOnlyPolicy.ActorId);
                RuleTime savedJournalTime = journal.Now.Time;
                snapshot.RuleClock = snapshot.RuleClock.AddSeconds(1);
                var ledger = TestOnlyClubAttackPolicy.ConditionsFor(snapshot, TestOnlyPolicy.ActorId);
                Require(snapshot.SchemaVersion == Snapshot.ConditionSchema && ledger.Now.Time == savedJournalTime
                    && ledger.Now.Time != snapshot.RuleClock,
                    "A pre-schema52 condition read projected sparse-journal time and changed historical behavior.");
            });
            cases.Add("condition_combat_world_authority_and_retry_revocation_precede_duplicate", () => {
                var p = CCPolicy(new[] { CCApply("blind", "Blinded") }); var s = Clubs(p); var c = CCCommand(s, "blind");
                var noWorld = new Authority("TEST_ONLY.host", new[] { TestOnlyPolicy.ActorId });
                RejectUnchanged(s, noWorld, c, "NotAuthorized"); CommitTac(s, c); byte[] bytes = Bytes(s);
                Require(s.Execute(host, c).Outcome == Outcome.Duplicate && bytes.SequenceEqual(Bytes(s)), "Duplicate repeated condition.");
                RejectUnchanged(s, noWorld, c, "NotAuthorized");
                s = RestoreClub(s, p); Require(s.Execute(host, c).Outcome == Outcome.Duplicate, "Restored condition receipt lost.");
                RejectUnchanged(s, host, CCCommand(s, "blind"), "ConditionEventAlreadyResolved");
            });
            cases.Add("condition_combat_fixed_events_bind_target_time_and_payload", () => {
                var s = Clubs(CCPolicy(new[] { CCApply("future", "Blinded", at: CJAt(1)) }));
                RejectUnchanged(s, host, CCCommand(s, "missing"), "UnknownConditionEvent");
                RejectUnchanged(s, host, CCCommand(s, "future", TestOnlyPolicy.CompanionId), "UnknownConditionEvent");
                RejectUnchanged(s, host, CCCommand(s, "future"), "WrongConditionEventTime");
                var c = CCCommand(s, "future"); RejectUnchanged(s, host, new Command(c.Id, c.Actor, c.ExpectedRevision, c.Kind, c.Target, 1), "InvalidConditionEvent");
                AdvanceI(s, 1); CCDispatch(s, "future"); Require(CCState(s).View().Has(ConditionKind.Blinded), "Fixed event did not apply at its marker.");
            });
            cases.Add("condition_combat_positive_hp_sleep_drops_once_without_dying", () => {
                var p = CCPolicy(new[] { CCApply("sleep", "Unconscious", expires: CJAt(1)) }); var s = Clubs(p); CCDispatch(s, "sleep");
                var l = Life(s); Require(l.Hp == 26 && !l.Stable && !l.Dead && l.StableUntil == null && l.Prone && l.HeldItems.Count == 0, "External sleep altered life or omitted onset.");
                var club = s.Capture().Clubs.Single(x => x.Id == TestOnlyClubAttackPolicy.ActorClub);
                Require(club.HeldBy == "" && club.OwnerId == TestOnlyPolicy.ActorId && club.CustodianId == TestOnlyPolicy.ActorId, "Drop lost ownership/custody.");
                s = RestoreClub(s, p); AdvanceI(s, 2);
                Require(!CCState(s).View().Has(ConditionKind.Unconscious) && Life(s).Prone && Life(s).HeldItems.Count == 0 && s.Capture().LifeEvents.Length == 0, "Sleep expiry stood, retrieved or ran death saves.");
            });
            cases.Add("condition_combat_sleep_blocks_choices_but_not_turn_progress", () => {
                var s = Clubs(CCPolicy(new[] { CCApply("sleep", "Unconscious") })); CCDispatch(s, "sleep"); BeginEncounter(s);
                RejectUnchanged(s, host, Tac(s, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive), "ActorUnaware");
                RejectUnchanged(s, host, Tac(s, CommandKind.TacticalStep, x: 0, y: 1), "ActorUnaware");
                CommitTac(s, Tac(s, CommandKind.EndRegularTurn)); Require(s.Capture().Encounter.CurrentActor == TestOnlyPolicy.CompanionId, "Unaware turn could not finish.");
            });
            cases.Add("condition_combat_incapacitated_allows_locomotion_and_standing", () => {
                var p = CCPolicy(new[] { CCApply("incap", "Incapacitated") }, prone: true); var s = Tactical(p); CCDispatch(s, "incap");
                CommitTac(s, Tac(s, CommandKind.StandFromProne)); TacStep(s, 0, 1);
                Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent == 20 && !Life(s).Prone, "Incapacitated silently prohibited independent movement.");
                RejectUnchanged(s, host, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId), "ConditionPreventsAction");
                RejectUnchanged(s, host, Tac(s, CommandKind.Disengage), "ConditionPreventsAction");
                Require(Resources(s).ReactionAvailable, "Condition spent reaction resource.");
            });
            cases.Add("condition_combat_action_restrictions_do_not_waive_stance_choice", () => {
                foreach (string kind in new[] { "Incapacitated", "Dazed" }) {
                    var p = CCPolicy(new[] { CCApply("restriction", kind) }); var s = Clubs(p); BeginEncounter(s);
                    if (kind == "Dazed") CommitTac(s, Tac(s, CommandKind.Disengage));
                    CCDispatch(s, "restriction");
                    RejectUnchanged(s, host, Tac(s, CommandKind.EndRegularTurn), "StanceRequired");
                    CommitTac(s, Tac(s, CommandKind.SelectCombatStance, stance: (int)CombatStance.Guarded));
                    CommitTac(s, Tac(s, CommandKind.EndRegularTurn));
                    Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s, p))), "Restricted stance choice did not persist.");
                }
            });
            cases.Add("condition_combat_dazed_respects_prior_movement_and_forbids_dash", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("daze", "Dazed") })); TacStep(s, 0, 1); CCDispatch(s, "daze");
                RejectUnchanged(s, host, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId), "ConditionPreventsAction");
                RejectUnchanged(s, host, Tac(s, CommandKind.EncounterDash), "ConditionPreventsDash"); TacStep(s, 1, 1);
                Require(TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent == 10, "Dazed movement mode stopped legal movement.");
            });
            cases.Add("condition_combat_dazed_after_action_blocks_movement_not_reaction", () => {
                var p = CCPolicy(new[] { CCApply("daze", "Dazed") }); var s = Tactical(p); CommitTac(s, Tac(s, CommandKind.Disengage)); CCDispatch(s, "daze");
                RejectUnchanged(s, host, Tac(s, CommandKind.TacticalStep, x: 0, y: 1), "ConditionPreventsMovement");
                Require(Resources(s).ReactionAvailable && CCState(s).View().Clauses.Has(ConditionClause.Dazed), "Dazed consumed reaction.");
                s = RestoreClub(s, p); RejectUnchanged(s, host, Tac(s, CommandKind.TacticalStep, x: 0, y: 1), "ConditionPreventsMovement");
            });
            cases.Add("condition_combat_dazed_reactor_can_take_ordinary_oa", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("daze", "Dazed", TestOnlyPolicy.CompanionId) }, seed: SeedForDeath(16)));
                CCDispatch(s, "daze", TestOnlyPolicy.CompanionId); TacStep(s, 0, 1); TacStep(s, 0, 2); AnswerOpportunity(s, true);
                Require(s.Capture().MeleeAttacks.Single().Opportunity && !Resources(s, TestOnlyPolicy.CompanionId).ReactionAvailable, "Dazed removed its permitted Reaction.");
            });
            cases.Add("condition_combat_restrained_zero_speed_keeps_action_permission", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("bind", "Restrained") }, seed: SeedForDeath(16))); CCDispatch(s, "bind");
                RejectUnchanged(s, host, Tac(s, CommandKind.TacticalStep, x: 0, y: 1), "ZeroSpeedCannotMove");
                CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId));
                Require(s.Capture().MeleeAttacks.Single().Attack.Second != 0 && TestOnlyClubAttackPolicy.WalkingSpeed(s.Capture(), TestOnlyPolicy.ActorId) == 0, "Restrained failed to constrain speed/attack.");
            });
            cases.Add("condition_combat_blinded_attack_has_disadvantage", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("blind", "Blinded") }, seed: SeedForDeath(16))); CCDispatch(s, "blind");
                CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId)); var a = s.Capture().MeleeAttacks.Single().Attack;
                Require(a.Second != 0 && a.Selected == Math.Min(a.First, a.Second), "Blinded attack did not use disadvantage.");
            });
            cases.Add("condition_combat_target_advantage_cancels_poison_disadvantage", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("poison", "Poisoned"), CCApply("blind", "Blinded", TestOnlyPolicy.CompanionId) }));
                CCDispatch(s, "poison"); CCDispatch(s, "blind", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId));
                Require(s.Capture().MeleeAttacks.Single().Attack.Second == 0, "Condition advantage/disadvantage did not cancel.");
            });
            cases.Add("condition_combat_paralysis_critical_if_hit_without_automatic_hit", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("paralyze", "Paralyzed", TestOnlyPolicy.CompanionId) }, seed: SeedForDeath(16)));
                CCDispatch(s, "paralyze", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackClub, TestOnlyPolicy.CompanionId, weapon: TestOnlyClubAttackPolicy.ActorClub));
                var attack = s.Capture().MeleeAttacks.Single(); Require(attack.Attack.Hit && attack.Attack.Critical && attack.Damage.Dice.Count == 2, "Paralyzed adjacent hit did not become critical.");
            });
            cases.Add("condition_combat_petrified_damage_halves_before_life_resolution", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("stone", "Petrified", TestOnlyPolicy.CompanionId) }, seed: SeedForDeath(16)));
                CCDispatch(s, "stone", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId));
                Require(s.Capture().MeleeAttacks.Single().Damage.Total == 1 && Life(s, TestOnlyPolicy.CompanionId).Hp == 25, "Petrified failed to halve3 before life resolution.");
            });
            cases.Add("condition_combat_stone_pending_knockout_preserves_resolved_damage", () => {
                var p = CCPolicy(new[] { CCApply("stone", "Petrified", TestOnlyPolicy.CompanionId) }, seed: SeedForDeath(16), companionHp: 1); var s = Tactical(p);
                CCDispatch(s, "stone", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId, knockout: AttackKnockoutMode.AskIfEligible));
                var pending = s.Capture().MeleeAttacks.Single(); Require(pending.Pending && pending.Damage.Total == 1, "Pending stone damage wrong.");
                s = RestoreClub(s, p); CommitTac(s, Tac(s, CommandKind.ResolveKnockout, pending.Id, choice: true));
                Require(Life(s, TestOnlyPolicy.CompanionId).Stable && s.Capture().MeleeAttacks.Single().Damage.Total == 1, "Continuation halved twice or lost damage.");
            });
            cases.Add("condition_combat_invisible_known_location_does_not_restore_oa_sight", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("invis", "Invisible") })); CCDispatch(s, "invis"); TacStep(s, 0, 1); TacStep(s, 0, 2);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()) == null && Body(s).Y == 2 && Resources(s, TestOnlyPolicy.CompanionId).ReactionAvailable, "Known location incorrectly supplied OA sight.");
            });
            cases.Add("condition_combat_blinded_reactor_cannot_offer_oa", () => {
                var s = Tactical(CCPolicy(new[] { CCApply("blind", "Blinded", TestOnlyPolicy.CompanionId) })); CCDispatch(s, "blind", TestOnlyPolicy.CompanionId); TacStep(s, 0, 1); TacStep(s, 0, 2);
                Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()) == null && Resources(s, TestOnlyPolicy.CompanionId).ReactionAvailable, "Blind reactor attacked unseen movement.");
            });
            cases.Add("condition_combat_residual_stun_keeps_component_absent_but_blocks_body_attack", () => {
                var p = CCPolicy(new[] { CCGrant("ward", TestOnlyPolicy.ActorId, null, "Incapacitated"), CCApply("stun", "Stunned") }); var s = Tactical(p);
                CCDispatch(s, "ward"); CCDispatch(s, "stun"); Require(!CCState(s).View().Has(ConditionKind.Incapacitated), "Host recreated prevented component.");
                RejectUnchanged(s, host, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId), "ConditionPreventsPhysicalAttack");
                Require(Resources(s).ReactionAvailable && Life(s).HeldItems.Count == 1, "Body restriction spent resources or dropped weapon.");
            });
            cases.Add("condition_combat_suppressed_prone_changes_effects_without_standing", () => {
                var p = CCPolicy(new[] { CCGrant("ward", TestOnlyPolicy.ActorId, CJAt(1), "Prone") }, prone: true); var s = Tactical(p); CCDispatch(s, "ward");
                TacStep(s, 0, 1); Require(Life(s).Prone && TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent == 5 && !CCState(s).View().Has(ConditionKind.Prone), "Suppressed Prone stood body or retained crawl cost.");
                CommitTac(s, Tac(s, CommandKind.StandFromProne)); Require(!Life(s).Prone && TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent == 20, "Suppressed physical posture received free stand.");
                CommitTac(s, Tac(s, CommandKind.EndRegularTurn)); s = RestoreClub(s, p); Require(!Life(s).Prone && !CCState(s).View().Has(ConditionKind.Prone), "Immunity expiry repeated fall after standing.");
            });
            cases.Add("condition_combat_prone_immunity_rejects_voluntary_drop", () => {
                var s = Tactical(CCPolicy(new[] { CCGrant("ward", TestOnlyPolicy.ActorId, null, "Prone") })); CCDispatch(s, "ward");
                RejectUnchanged(s, host, Tac(s, CommandKind.DropProne), "PronePrevented"); Require(!Life(s).Prone, "Prevented drop changed posture.");
            });
            cases.Add("condition_combat_zero_hp_prone_immunity_prevents_fall_not_incapacity", () => {
                var p = CCPolicy(new[] { CCGrant("ward", TestOnlyPolicy.CompanionId, null, "Prone", "Unconscious", "Incapacitated") }, seed: SeedForDeath(16), companionHp: 1); var s = Tactical(p);
                CCDispatch(s, "ward", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId, knockout: AttackKnockoutMode.KnockOutIfEligible));
                var l = Life(s, TestOnlyPolicy.CompanionId); Require(l.Hp == 0 && l.Stable && !l.Prone && l.HeldItems.Count == 0, "Immunity changed zeroHP or failed distinct drop/fall.");
                CommitTac(s, Tac(s, CommandKind.EndRegularTurn)); RejectUnchanged(s, host, Tac(s, CommandKind.TacticalStep, x: 1, y: 1), "ActorCannotAct");
                s = RestoreClub(s, p); Require(Life(s, TestOnlyPolicy.CompanionId).Hp == 0 && !Life(s, TestOnlyPolicy.CompanionId).Prone, "Restore required every zeroHP body to be prone.");
            });
            cases.Add("condition_combat_external_sleep_survives_separate_zero_hp_cause", () => {
                var p = CCPolicy(new[] { CCApply("sleep", "Unconscious", TestOnlyPolicy.CompanionId) }, seed: SeedForDeath(16), companionHp: 1); var s = Tactical(p);
                CCDispatch(s, "sleep", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId, knockout: AttackKnockoutMode.KnockOutIfEligible));
                var l = Life(s, TestOnlyPolicy.CompanionId); Require(l.Stable && CCState(s, TestOnlyPolicy.CompanionId).View().Has(ConditionKind.Unconscious), "Independent unconscious state lost on zeroHP.");
                // Full recovery interval cannot be advanced while encounter remains active. The exact
                // saved independent cause is checked here; existing helper tests cover recovery arithmetic.
                s = RestoreClub(s, p); Require(CCState(s, TestOnlyPolicy.CompanionId).View().Has(ConditionKind.Unconscious), "Saved zeroHP replaced external sleep.");
            });
            cases.Add("condition_combat_fractional_absolute_expiry_precedes_incoming_decision", () => {
                var p = CCPolicy(new[] { CCApply("sleep", "Unconscious", TestOnlyPolicy.CompanionId, new ConditionStamp(new RuleTime(1, 3))) }); var s = Tactical(p);
                CCDispatch(s, "sleep", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.EndRegularTurn));
                Require(!CCState(s, TestOnlyPolicy.CompanionId).View().Has(ConditionKind.Unconscious) && Life(s, TestOnlyPolicy.CompanionId).Prone, "Absolute expiry missed before incoming turn.");
                Require(CCState(s, TestOnlyPolicy.CompanionId).Applications.Single(x => x.Id == "sleep").EndedAt.Value.Time == new RuleTime(1, 3), "Fractional deadline rounded to slot.");
                CommitTac(s, Tac(s, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s, p))), "Exact clock replay changed condition state.");
            });
            cases.Add("condition_combat_restore_rejects_missing_journal_or_forged_world_consequence", () => {
                var p = CCPolicy(new[] { CCApply("sleep", "Unconscious") }); var s = Clubs(p); CCDispatch(s, "sleep"); var v = s.Capture();
                v.Conditions = p.Initial().Conditions; Throws<ArgumentException>(() => new Simulation(p, v, ExecutionProfile.Laboratory));
                v = s.Capture(); var initial = p.Initial(); v.Clubs = initial.Clubs; v.Lives = initial.Lives;
                Throws<ArgumentException>(() => new Simulation(p, v, ExecutionProfile.Laboratory));
                v = s.Capture(); v.Conditions = Array.Empty<ConditionJournal>(); Throws<ArgumentException>(() => codec.Encode(v));
            });
            cases.Add("condition_combat_pending_knockout_blocks_external_injection", () => {
                var p = CCPolicy(new[] { CCApply("blind", "Blinded") }, seed: SeedForDeath(16), companionHp: 1); var s = Tactical(p);
                CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId, knockout: AttackKnockoutMode.AskIfEligible));
                RejectUnchanged(s, host, CCCommand(s, "blind"), "KnockoutChoicePending");
            });
            cases.Add("condition_combat_event_invalidates_oa_without_spending_reaction", () => {
                var p = CCPolicy(new[] { CCApply("blind", "Blinded", TestOnlyPolicy.CompanionId) }); var s = Tactical(p);
                TacStep(s, 0, 1); TacStep(s, 0, 2); var oldResponse = Opportunity(s, true); var c = CCCommand(s, "blind", TestOnlyPolicy.CompanionId);
                CommitTac(s, c); Require(TestOnlyClubAttackPolicy.PendingMove(s.Capture()) == null && Body(s).Y == 2 && Resources(s, TestOnlyPolicy.CompanionId).ReactionAvailable
                    && s.Capture().MeleeAttacks.Length == 0, "Invalidating OA spent a reaction or stopped legal departure.");
                RejectUnchanged(s, host, oldResponse, "StaleRevision"); s = RestoreClub(s, p); byte[] bytes = Bytes(s);
                Require(s.Execute(host, c).Outcome == Outcome.Duplicate && bytes.SequenceEqual(Bytes(s)), "Event retry repeated continuation consequences.");
            });
            cases.Add("condition_combat_event_stops_unpaid_step_preserving_prior_spending", () => {
                var p = CCPolicy(new[] { CCApply("stun", "Stunned") }); var s = Tactical(p); TacStep(s, 0, 1); TacStep(s, 0, 2); CCDispatch(s, "stun");
                var move = s.Capture().TacticalMoves.Last(); Require(move.Status == TacticalMoveStatus.Interrupted && move.CostPaid == 0 && Body(s).Y == 1
                    && TestOnlyClubAttackPolicy.WalkingLedger(s.Capture()).Spent == 5 && Resources(s, TestOnlyPolicy.CompanionId).ReactionAvailable, "Condition interruption charged untraveled step or discarded prior movement.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s, p))), "Interrupted movement replay diverged.");
            });
            cases.Add("condition_combat_event_skips_current_oa_preserving_captured_order", () => {
                var p = CCPolicy(new[] { CCApply("blind", "Blinded", TestOnlyPolicy.CompanionId) }, third: new AdditionalTacticalActor(0, 1, 30)); var s = Tactical(p);
                TacStep(s, 1, 1); TacStep(s, 2, 2); CCDispatch(s, "blind", TestOnlyPolicy.CompanionId);
                var move = TestOnlyClubAttackPolicy.PendingMove(s.Capture()); Require(move.ResponseIndex == 1 && move.Reactors.SequenceEqual(new[] { TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id }), "Captured OA ordering changed.");
                s = RestoreClub(s, p); AnswerOpportunity(s, false); Require(Body(s).X == 2 && Resources(s, TestOnlyPolicy.CompanionId).ReactionAvailable, "Remaining captured reactor failed to finish.");
            });
            cases.Add("condition_combat_unaccepted_press_invalidation_preserves_entitlement", () => {
                var p = CCPolicy(new[] { CCApply("stun", "Stunned", at: CJAt(3)) }, seed: SeedForDeath(16)); var s = Tactical(p);
                CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId)); TacEnd(s); TacStep(s, 2, 0); AnswerOpportunity(s, false);
                CCDispatch(s, "stun"); Require(TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture()) == null && s.Capture().PressOffers.Single().Status == PressOfferStatus.Invalidated
                    && !Resources(s).PressConsumed && Body(s, TestOnlyPolicy.CompanionId).X == 2 && Body(s).X == 0, "Invalidated unpaid Press consumed entitlement or reversed retreat.");
                s = RestoreClub(s, p);
            });
            cases.Add("condition_combat_accepted_press_interruption_keeps_paid_entitlement", () => {
                var p = CCPolicy(new[] { CCApply("stun", "Stunned", at: CJAt(2)) }, seed: SeedForDeath(16), third: new AdditionalTacticalActor(0, 1, 30)); var s = Tactical(p);
                TacStep(s, 1, 1); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId)); TacEnd(s); TacStep(s, 2, 0); AnswerOpportunity(s, false);
                TacStep(s, 3, 0); AnswerOpportunity(s, false); CommitTac(s, PressChoice(s, true)); CCDispatch(s, "stun");
                Require(Resources(s).PressConsumed && s.Capture().TacticalMoves.Last().Status == TacticalMoveStatus.Interrupted && s.Capture().TacticalMoves.Last().CostPaid == 0
                    && Body(s).X == 1 && Body(s).Y == 1 && Resources(s, AdditionalTacticalActor.Id).ReactionAvailable, "Interrupted accepted follow refunded entitlement or spent untraveled movement.");
                s = RestoreClub(s, p);
            });
            cases.Add("condition_combat_offturn_dazed_press_ignores_previous_turn_action", () => {
                var p = CCPolicy(new[] { CCApply("daze", "Dazed", at: CJAt(3)) }, seed: SeedForDeath(16)); var s = Tactical(p);
                CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId)); TacEnd(s); TacStep(s, 2, 0); AnswerOpportunity(s, false); CCDispatch(s, "daze");
                Require(TestOnlyClubAttackPolicy.CurrentPressOffer(s.Capture()) != null, "Previous own-turn Action incorrectly prevented offturn movement.");
                CommitTac(s, PressChoice(s, true)); Require(Body(s).X == 1 && Resources(s).PressConsumed, "Dazed offturn Press did not resolve.");
            });
            cases.Add("condition_combat_natural_twenty_recovery_keeps_independent_sleep", () => {
                var p = CCPolicy(new[] { CCApply("sleep", "Unconscious", TestOnlyPolicy.CompanionId) }, seed: TacticalSeed(16, 16, 20, 20), companionHp: 1); var s = Tactical(p);
                CCDispatch(s, "sleep", TestOnlyPolicy.CompanionId); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId));
                CommitTac(s, Tac(s, CommandKind.EndRegularTurn));
                Require(Life(s, TestOnlyPolicy.CompanionId).Hp == 1 && CCState(s, TestOnlyPolicy.CompanionId).View().Has(ConditionKind.Unconscious), "Natural20 incorrectly removed external sleep.");
                RejectUnchanged(s, host, Tac(s, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive), "ActorUnaware");
                s = RestoreClub(s, p);
            });
            cases.Add("condition_combat_injected_events_preserve_response_receipt_capacity", () => {
                var events = Enumerable.Range(0, 30).Select(i => new ConditionFixtureEvent(TestOnlyPolicy.ActorId,
                    ConditionOperation.Cure("event.noop" + i, CJAt(479), "Blinded"))).ToArray();
                var p = CCPolicy(events); var raw = p.Initial();
                // Build valid prehistory once; Simulation still replays and verifies it in full.
                for (int i = 0; i < 479; i++) {
                    var c = new Command("setup." + i, TestOnlyPolicy.ActorId, i, CommandKind.AdvanceClock, x: 1, y: 1);
                    Require(p.Resolve(raw, c) == null, "Clock setup failed."); raw.Revision++;
                    var receipt = new CommandReceipt { Principal = host.Principal, Id = c.Id, Revision = raw.Revision,
                        Fingerprint = ((int)c.Kind).ToString(System.Globalization.CultureInfo.InvariantCulture) + "|" + c.Actor + "||" + i.ToString(System.Globalization.CultureInfo.InvariantCulture) + "|1|1" };
                    Require(c.MatchesReceipt(receipt), "Setup receipt differs from real command.");
                    raw.Receipts = raw.Receipts.Concat(new[] { receipt }).ToArray();
                }
                var s = new Simulation(p, raw, ExecutionProfile.Laboratory); BeginEncounter(s); Stance(s, CombatStance.Aggressive);
                TacStep(s, 0, 1); TacStep(s, 0, 2);
                for (int i = 0; i < 20; i++) CCDispatch(s, "noop" + i);
                Require(s.Capture().Revision == 503 && TestOnlyClubAttackPolicy.PendingMove(s.Capture()) != null, "Expected pending choice at reserved boundary.");
                RejectUnchanged(s, host, CCCommand(s, "noop20"), "ContinuationCapacityReached");
                AnswerOpportunity(s, false); Require(Body(s).Y == 2 && TestOnlyClubAttackPolicy.PendingMove(s.Capture()) == null, "Injected events stranded controller response.");
                Require(Bytes(s).SequenceEqual(Bytes(RestoreClub(s, p))), "Capacity-bound continuation cannot restore.");
            });
            cases.Add("condition_combat_save_store_keeps_journal_and_world_atomic", () => {
                var p = CCPolicy(new[] { CCApply("sleep", "Unconscious") }); var s = Clubs(p); var store = new FileSaveStore(); string path = Path.Combine(directory, "condition-host.bin");
                store.Save(path, s.Capture()); CCDispatch(s, "sleep"); store.Save(path, s.Capture());
                var restored = new Simulation(p, store.Load(path), ExecutionProfile.Laboratory);
                Require(Life(restored).HeldItems.Count == 0 && Life(restored).Prone && CCState(restored).View().Has(ConditionKind.Unconscious), "Saved journal/world split.");
                Require(store.Load(path + ".bak").Conditions.All(x => x.Operations.Count == 0), "Previous good state did not survive.");
                Throws<InvalidDataException>(() => store.Save(path, TacticalPolicy().Initial()));
            });
            cases.Add("condition_combat_aggregate_journals_cross_old_limit_and_roundtrip_on_disk", () => {
                var v = CCPolicy(third: new AdditionalTacticalActor(1, 1, 30)).Initial(); string Long(string text) => text.PadRight(96, 'x');
                var ops = Enumerable.Range(0, 512).Select(i => ConditionOperation.Grant(Long("op" + i), default,
                    new ConditionImmunityData(Long("grant" + i), Long("owner"), Long("source"), Enumerable.Range(0, 14).Select(k => Long("kind" + k)), CJAt(1), Long("end")))).ToArray();
                v.Conditions = v.Actors.Select(a => new ConditionJournal(Long("policy"), a.Id, operations: ops)).ToArray(); var bytes = codec.Encode(v);
                Require(bytes.Length > SnapshotCodec.MaxBytes && bytes.Length < SnapshotCodec.ConditionMaxBytes && bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))), "Aggregate condition envelope failed.");
                string path = Path.Combine(directory, "maximum-condition-host.bin"); var store = new FileSaveStore(); store.Save(path, v);
                Require(bytes.SequenceEqual(codec.Encode(store.Load(path))), "File store retained old2MiB limit.");
                // Structural codec maximum is not an admitted gameplay history.
            });
        }
    }
}
#endif
