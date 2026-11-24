#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddConnectedFleshWardenCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac06_flesh_warden_connected_real_healing_and_rest_replacement", () =>
            {
                const string hero = FleshWardenProfile.Actor;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                var session = ShortRestArrival(ConnectedExpeditionSession.StartWithFleshWarden(), true);
                var codec = new SnapshotCodec();
                Snapshot Capture() => ShortRestCapture(session);
                ActorLifeRecord Hero() => Capture().Lives.Single(x => x.ActorId == hero);
                void Commit(string id, CommandKind kind, string target = "", int x = 0, int y = 0)
                {
                    var command=new Command(id, hero, session.View(player).Revision, kind, target, x, y);
                    if(ShortRestBerth.IsCommand(kind))AssertPureUtility(session,command);
                    CommitVialRoute(session,command);
                }
                string FileAt(string label) => Path.Combine(directory, "flesh-connected-" + label + ".ddsave");
                var arrival = Capture();
                var dose = arrival.AlchemyDoses.Single(x => x.Id == VialId);
                Require(Hero().Hp > 26 && Hero().MaximumHp == 32 && dose.Spent && dose.ActualHealing > 0
                    && arrival.FleshWarden.Applications.Single().Present && !arrival.InventoryCombat,
                    "Real later combat and finite tactical healing must create HP above the old capacity before replacement.");
                Commit("flesh.replace", CommandKind.BeginMutationShortRest, FleshWardenProfile.SpinalBuffer);
                session.Save(FileAt("pending")); session.Restore(FileAt("pending"));
                var pending = Capture();
                Commit("flesh.before-end", CommandKind.AdvanceClock, x: 3599, y: 1);
                Require(Hero().MaximumHp == 32 && Hero().Hp == arrival.Lives.Single(x => x.ActorId == hero).Hp,
                    "A replacement choice must not change equipment before the entire hour.");
                Commit("flesh.end", CommandKind.AdvanceClock, x: 1, y: 1);
                var split = Capture(); session.Save(FileAt("split"));
                session.Restore(FileAt("pending")); Commit("flesh.whole", CommandKind.AdvanceClock, x: 3600, y: 1);
                var whole = Capture();
                var change = whole.FleshWarden.Choices.Last().Change;
                Require(Hero().MaximumHp == 26 && Hero().Hp == 26 && change.HpBefore > 26
                    && change.CapacityClamp == change.HpBefore - 26 && change.Healing == 0 && change.Damage == 0
                    && whole.FleshWarden.EquippedMutationId == FleshWardenProfile.SpinalBuffer
                    && !whole.FleshWarden.Applications.Single().Present
                    && whole.FleshWarden.Applications.Single().Id == pending.FleshWarden.ApplicationId
                    && whole.RandomState == pending.RandomState && whole.RandomState == split.RandomState
                    && whole.RuleClock == split.RuleClock && whole.Lives.Zip(split.Lives, (a,b) => a.SameAs(b)).All(x => x)
                    && whole.ConsumeDecay.End == TemporaryHpEnd.Expired && Hero().TemporaryHp == 0,
                    "Replacement must preserve the actual effect identity, clamp only excess HP, and leave independent expiry deterministic.");
                Commit("flesh.continue", CommandKind.BeginWorldStep, "walk", y: -1);
                Commit("flesh.continue-paid", CommandKind.AdvanceClock, x: 6, y: 1);
                session.Save(FileAt("continued")); session.Restore(FileAt("continued"));
                var continued = Capture();
                var replay = ConnectedExpeditionSession.StartWithFleshWarden();
                foreach (var receipt in continued.Receipts) {
                    if (receipt.Principal == "TEST_ONLY.tac10-later-defender.v1")
                        Require(replay.AdvanceAutomaticDefender().Response == ExpeditionResponse.Committed, "Automatic defender replay failed.");
                    else CommitVialRoute(replay, CommandHistory.Read(receipt));
                }
                Require(codec.Encode(continued).SequenceEqual(codec.Encode(ShortRestCapture(replay)))
                    && continued.Actors.Single(x => x.Id == hero).Y == 0,
                    "Capacity application/removal must survive restore and direct replay through paid continuation.");
            });

            cases.Add("tac06_flesh_warden_choice_interruption_identity_authority_and_forgery", () =>
            {
                const string hero = FleshWardenProfile.Actor;
                const ExpeditionSeat player = ExpeditionSeat.Player;
                var session = ConnectedExpeditionSession.StartWithFleshWarden();
                var codec = new SnapshotCodec();
                var policy = (TestOnlySharedWorldPolicy)typeof(ConnectedExpeditionSession).GetField("policy", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session);
                Snapshot Capture() => ShortRestCapture(session);
                void Commit(string id, CommandKind kind, string target = "", int x = 0, int y = 0)
                {
                    var command=new Command(id, hero, session.View(player).Revision, kind, target, x, y);
                    if(ShortRestBerth.IsCommand(kind))AssertPureUtility(session,command);
                    CommitVialRoute(session,command);
                }
                Command Begin(string id, string target = FleshWardenProfile.FleshWarden)
                    => new Command(id, hero, session.View(player).Revision, CommandKind.BeginMutationShortRest, target);
                void Deny(Command c, ExpeditionResponse expected = ExpeditionResponse.Unavailable, ExpeditionSeat seat = player)
                {
                    var bytes = codec.Encode(Capture());
                    Require(session.Submit(seat, c).Response == expected && bytes.SequenceEqual(codec.Encode(Capture())), "Mutation denial/retry changed state: " + c.Id);
                }
                void Reject(Snapshot forged)
                {
                    bool rejected = false;
                    try { codec.Encode(forged); } catch (ArgumentException) { rejected = true; }
                    Require(rejected || policy.ValidateState(forged) != null, "Forged mutation state was accepted.");
                }
                var initial = Capture();
                Require(initial.WireSchemaVersion == 104 && initial.SchemaVersion == 90 && initial.CharacterHitDice.Length == 0
                    && initial.CharacterFeatureGrants.Count(x => FleshWardenProfile.ValidFixtureGrant(initial, x)) == 2
                    && initial.FleshWarden.EquippedMutationId == FleshWardenProfile.SpinalBuffer
                    && initial.FleshWarden.Applications.Count == 0 && session.View(ExpeditionSeat.FirstOpponent).FleshWarden == null,
                    "Only the exact fixture grants may bypass the unrelated Hit Dice ledger; a foreign seat must not see the loadout.");
                var forged = initial.Copy(); forged.CharacterFeatureGrants = forged.CharacterFeatureGrants.Take(1).ToArray(); Reject(forged);
                forged = initial.Copy(); forged.FleshWarden = new FleshWardenRecord(new MutationQualificationRecord(hero, "wrong-source", MutationTier.Basic, MutationTree.Vital),
                    1, FleshWardenProfile.SpinalBuffer, "", Array.Empty<MutationRestChoiceRecord>(), Array.Empty<MutationCapacityApplicationRecord>()); Reject(forged);
                forged = initial.Copy(); forged.ConnectedFleshWarden = false; Reject(forged);
                forged = ShortRestCapture(ConnectedExpeditionSession.StartWithShortRest()); forged.CharacterFeatureGrants = initial.CharacterFeatureGrants; Reject(forged);
                Commit("flesh.berth", CommandKind.BeginWorldStep, "walk", y: 1);
                Commit("flesh.berth-paid", CommandKind.AdvanceClock, x: 6, y: 1);
                Deny(Begin("flesh.unknown", "warrior.unknown"));
                Deny(new Command("flesh.dice", hero, Capture().Revision, CommandKind.BeginMutationShortRest, FleshWardenProfile.FleshWarden, 1));
                Deny(new Command("flesh.foreign", ConnectedExpeditionSession.Companion, Capture().Revision, CommandKind.BeginMutationShortRest, FleshWardenProfile.FleshWarden));
                Deny(new Command("flesh.stale", hero, Capture().Revision-1, CommandKind.BeginMutationShortRest, FleshWardenProfile.FleshWarden), ExpeditionResponse.StaleRevision);
                var begin = Begin("flesh.interrupted"); AssertPureUtility(session,begin);CommitVialRoute(session, begin);
                Deny(begin, ExpeditionResponse.Duplicate);
                session.SetSeatEnabled(player, false); Deny(begin, ExpeditionResponse.NotAuthorized); session.SetSeatEnabled(player, true);
                Deny(new Command(begin.Id, hero, begin.ExpectedRevision, begin.Kind, FleshWardenProfile.SpinalBuffer), ExpeditionResponse.CommandIdConflict);
                Commit("flesh.partial", CommandKind.AdvanceClock, x: 17, y: 1);
                var pending = Capture();
                var active = ShortRestBerth.Active(pending);
                Commit("flesh.interrupt", CommandKind.InterruptShortRest, active.Id);
                Require(Capture().FleshWarden.Choices.Single().Change == null && Capture().FleshWarden.Applications.Count == 0
                    && ShortRestBerth.BenefitsUsed(Capture()) == 0 && Capture().Lives.Single(x => x.ActorId == hero).MaximumHp == 26,
                    "Interrupted choice cannot apply capacity or spend a benefit.");
                var restart=Begin("flesh.restart");AssertPureUtility(session,restart);CommitVialRoute(session,restart);
                string path = Path.Combine(directory, "flesh-choice-pending.ddsave"); session.Save(path); session.Restore(path);
                Commit("flesh.restart-before", CommandKind.AdvanceClock, x: 3599, y: 1);
                Require(Capture().FleshWarden.ApplicationId == "", "Restart cannot retain the interrupted attempt's progress.");
                Commit("flesh.restart-end", CommandKind.AdvanceClock, x: 1, y: 1);
                var applied = Capture(); var effect = applied.FleshWarden.Applications.Single();
                var sameCommand=Begin("flesh.same");AssertPureUtility(session,sameCommand);CommitVialRoute(session,sameCommand); Commit("flesh.same-hour", CommandKind.AdvanceClock, x: 3600, y: 1);
                var same = Capture();
                Require(same.FleshWarden.ApplicationId == effect.Id && same.FleshWarden.Applications.Single().StartedAt == effect.StartedAt
                    && same.Lives.Single(x => x.ActorId == hero).Hp == 26 && same.Lives.Single(x => x.ActorId == hero).MaximumHp == 32
                    && ShortRestBerth.BenefitsUsed(same) == 2 && same.FleshWarden.Choices.Last().Change.CapacityClamp == 0,
                    "Same-card completion must spend its benefit without refreshing or duplicating the source or healing.");
                var third = Begin("flesh.third", FleshWardenProfile.SpinalBuffer);
                Require(policy.Resolve(same.Copy(), third) == "MutationRestCadenceUnsupported"
                    && session.View(player).FleshWarden.PlanUnavailableReason == "MutationRestCadenceUnsupported", "Cadence exclusion must be explicit.");
                Deny(third);
                Commit("flesh.plain-third", CommandKind.BeginShortRest, ShortRestBerth.Id);
                Commit("flesh.plain-third-hour", CommandKind.AdvanceClock, x: 3600, y: 1);
                Require(Capture().ShortRests.Last().Benefit == ShortRestBenefit.Ineligible && Capture().FleshWarden.ApplicationId == effect.Id,
                    "An ordinary ineligible rest preserves the equipped mutation.");
                forged = applied.Copy();
                forged.FleshWarden = new FleshWardenRecord(applied.FleshWarden.Qualification, 1, FleshWardenProfile.FleshWarden, effect.Id,
                    applied.FleshWarden.Choices, new[] { new MutationCapacityApplicationRecord(effect.Id, effect.SourceId, effect.SourceRevision,
                        ConnectedExpeditionSession.Companion, hero, 3, effect.StartRestId, effect.StartedAt) }); Reject(forged);
                forged = applied.Copy();
                forged.FleshWarden = new FleshWardenRecord(applied.FleshWarden.Qualification, 1, FleshWardenProfile.FleshWarden, effect.Id,
                    applied.FleshWarden.Choices, new[] { new MutationCapacityApplicationRecord(effect.Id, effect.SourceId, effect.SourceRevision,
                        hero, hero, 4, effect.StartRestId, effect.StartedAt) }); Reject(forged);
                forged = applied.Copy(); forged.ShortRests = Array.Empty<ShortRestRecord>(); Reject(forged);
            });

            cases.Add("tac06_flesh_warden_shared_capacity_life_temp_and_strain_boundaries", () =>
            {
                const string hero = FleshWardenProfile.Actor;
                var initial = ShortRestCapture(ConnectedExpeditionSession.StartWithFleshWarden());
                var apply = typeof(TestOnlySharedWorldPolicy).GetMethod("ApplyMutationCapacity", BindingFlags.Static | BindingFlags.NonPublic);
                var effect = new MutationCapacityApplicationRecord("detached.flesh", FleshWardenProfile.FleshWarden, FleshWardenProfile.SourceRevision,
                    hero, hero, 3, "detached.rest", default);
                MutationCapacityChangeRecord Change(Snapshot s, bool equip)
                    => (MutationCapacityChangeRecord)apply.Invoke(null, new object[] { s, equip ? new[] { effect } : Array.Empty<MutationCapacityApplicationRecord>(),
                        equip ? FleshWardenProfile.SpinalBuffer : FleshWardenProfile.FleshWarden, equip ? "" : effect.Id, equip ? effect.Id : "" });
                foreach (string condition in new[] { "living", "dying", "stable", "dead" }) {
                    var s = initial.Copy();
                    var before = new ActorLifeRecord(hero, 26, condition == "living" ? 18 : 0, 3, new[] { (int)Injury.Concussion, (int)Injury.OffensiveTrauma, (int)Injury.MobilityTrauma },
                        condition == "stable", condition == "dead", true, condition == "dying" ? 1 : 0, condition == "dying" ? 2 : condition == "dead" ? 3 : 0, condition == "stable" ? new RuleTime(900) : (RuleTime?)null,
                        7, true, new[] { "TEST_ONLY.actor-club" });
                    s.Lives = s.Lives.Select(x => x.ActorId == hero ? before : x).ToArray();
                    var grant = new ConsumeDecayRecord("detached.decay", 1, default, 3, true); s.ConsumeDecay = grant;
                    uint rng = s.RandomState; var events = s.LifeEvents;
                    var raised = Change(s, true);
                    var effective = ActorLifeRules.ReadForResolution(s, s.Lives.Single(x => x.ActorId == hero));
                    Require(effective.HealingCeiling == 31 && effective.Dead == (condition == "dead"),
                        "Critical ceiling must use the raised effective capacity without reviving a corpse.");
                    if (condition == "living") Require(PlaytestLife.Heal(effective, 100).Hp == 31, "Actual Critical healing must stop at effective maximum minus one.");
                    if (condition == "stable") Require(PlaytestLife.StableRecoveryAt(effective, new RuleTime(900)).Hp == 1,
                        "Stable recovery must retain its independent lawful endpoint under the new capacity.");
                    var lowered = Change(s, false); var after = s.Lives.Single(x => x.ActorId == hero);
                    Require(after.SameAs(before) && raised.Healing == 0 && lowered.Damage == 0 && lowered.CapacityClamp == 0
                        && ReferenceEquals(grant, s.ConsumeDecay) && s.ConsumeDecay.Deadline == new RuleTime(3600)
                        && s.RandomState == rng && ReferenceEquals(events, s.LifeEvents),
                        "Detached shared capacity operation changed independent life or temporary-grant facts: " + condition);
                }
                var excess = initial.Copy();
                var temp = new ConsumeDecayRecord("detached.excess-decay", 1, default, 3, true); excess.ConsumeDecay = temp;
                excess.Lives = excess.Lives.Select(x => x.ActorId == hero ? new ActorLifeRecord(hero, 32, 30, 3, x.LinkedInjuries,
                    x.Stable, x.Dead, x.UsesDeathSaves, x.DeathSuccesses, x.DeathFailures, x.StableUntil, x.LastDeathTurn, x.Prone, x.HeldItems) : x).ToArray();
                var clamp = Change(excess, false);
                Require(clamp.CapacityClamp == 4 && clamp.Damage == 0 && clamp.Healing == 0 && ReferenceEquals(temp, excess.ConsumeDecay)
                    && excess.Lives.Single(x => x.ActorId == hero).TemporaryHp == 3, "An actual detached capacity clamp must leave temporary HP independent.");
                var strained = initial.Copy();
                strained.ExpeditionStrainGains = Enumerable.Range(0, 4).Select(i => new ExpeditionStrainGainRecord("detached.gain."+i,
                    "detached.point."+i, ExpeditionStrainCauseKind.DailyProvisioning, "detached.day", i, hero,
                    TestOnlyDailyProvisioningProfile.SourceId, TestOnlyDailyProvisioningProfile.TrackId, default, 1, i, 1, 1, true, true,
                    ExpeditionStrainEndpoint.None)).ToArray();
                strained.Lives = strained.Lives.Select(x => x.ActorId == hero ? new ActorLifeRecord(hero, 26, 18, 0, x.LinkedInjuries,
                    x.Stable, x.Dead, x.UsesDeathSaves, x.DeathSuccesses, x.DeathFailures, x.StableUntil, x.LastDeathTurn, x.Prone, x.HeldItems) : x).ToArray();
                var gained = Change(strained, true);
                var resolved = ActorLifeRules.ReadForResolution(strained, strained.Lives.Single(x => x.ActorId == hero));
                Require(gained.MaximumBefore == 26 && gained.EffectiveBefore == 19 && gained.MaximumAfter == 32
                    && gained.EffectiveAfter == 24 && resolved.MaximumHp == 24 && resolved.Hp == 18,
                    "Shared Expedition Strain must apply once to pre-systemic capacity, with no healing.");
                var removed = Change(strained, false);
                Require(removed.MaximumAfter == 26 && removed.EffectiveAfter == 19 && removed.HpAfter == 18,
                    "Capacity removal must preserve independent systemic projection.");
            });
        }
    }
}
#endif
