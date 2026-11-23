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
        private static ConnectedExpeditionSession NewOrdinaryMagicExpedition() => ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(
            ClericInitialSelection.AuthoredExample(), ClericRepertoireSelection.AuthoredExample(),
            ClericMilestoneDeclaration.AuthoredExample(), BishopEntryRecord.Announced());
        private static void OrdinaryMagicAdvance(ConnectedExpeditionSession session, RuleTime until, string id)
        {
            var state = ShortRestCapture(session); var now = state.RuleClock;
            Require(until > now, "Ordinary magic advancement requires a future absolute target.");
            var elapsed = new RuleTime(checked(until.Numerator * now.Denominator - now.Numerator * until.Denominator),
                checked(until.Denominator * now.Denominator));
            BishopCommit(session, new Command(id, ConnectedExpeditionSession.Hero, state.Revision,
                CommandKind.AdvanceClock, x: checked((int)elapsed.Numerator), y: checked((int)elapsed.Denominator)));
        }

        private static void AddOrdinaryMagicCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac01_ordinary_magic_fresh_profile_and_save_boundary", () => {
                var session = NewOrdinaryMagicExpedition();
                var state = ShortRestCapture(session);
                Require(state.WireSchemaVersion == 116 && state.OrdinaryMagic != null && state.OrdinaryMagic.Current == null
                    && state.OrdinaryMagic.Activities.Count == 0 && state.OrdinaryMagic.Settlements.Count == 0,
                    "Fresh ordinary-magic profile invented an allowance or activity.");
                BishopCheckpoint(session, directory, "ordinary-magic-genesis");
                var old = NewConsecrationExpedition();
                var codec = new SnapshotCodec(); var oldBytes = codec.Encode(ShortRestCapture(old));
                bool rejected = false;
                try { old.Restore(Path.Combine(directory, "ordinary-magic-genesis.ddsave")); }
                catch (Exception e) when (e is ArgumentException || e is InvalidDataException) { rejected = true; }
                Require(rejected && oldBytes.SequenceEqual(codec.Encode(ShortRestCapture(old))), "A115 session adopted116 state or changed after rejection.");
            });
            cases.Add("tac01_ordinary_magic_genuine_c1_late_rite_and_settlement", () => {
                var session = EarnClericObjective(false, directory, NewOrdinaryMagicExpedition());
                var before = ShortRestCapture(session);
                Require(!before.InventoryCombat && before.Characters.Single(x => x.ActorId == ClericRpProfile.Actor).Levels.Count == 1
                    && before.ResonancePools.Single().Current == 3 && before.HealingRites.Length == 0
                    && before.Lives.Single(x => x.ActorId == ConnectedExpeditionSession.Hero).Hp == 9,
                    "The retained genuine pre-advancement Rite route changed.");
                // Delete a genuine zero-effect tactical End and forge apparent openness.
                // This must fail independent causal validation, before complete receipt replay.
                var original = before.OrdinaryMagic; var allowance = original.Current;
                Require(allowance.Consumed && before.CastingStrain.Single().Dissonance == 0, "Missing genuine zero-End forgery witness.");
                var forged = before.Copy();
                var reopened = new MagicalAllowanceRecord(allowance.Origin, allowance.OriginAt, allowance.Deadline,
                    allowance.ContextEpoch, allowance.InInitiative, false, allowance.SegmentOrdinal);
                var segments = original.Segments.Select(x => x.Ordinal != allowance.SegmentOrdinal ? x
                    : new MagicalSegmentRecord(x.Ordinal, x.Origin, x.ContextEpoch, x.InInitiative, false, x.CauseId, x.Revision,
                        x.At, x.Closed, x.CloseCauseId, x.CloseRevision, x.CloseAt));
                forged.OrdinaryMagic = original.With(original.NextOrdinal, reopened, segments: segments,
                    settlements: original.Settlements.Where(x => !x.Origin.SameAs(allowance.Origin)));
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(forged));
                File.WriteAllText(Path.Combine(directory, "zero-end-forgery-scope.txt"),
                    "Detached deletion of genuine zero-End coverage rejects during encoding; no forged campaign save was produced or adopted.");
                var remainder = NewOrdinaryMagicExpedition();
                string remainderPath = Path.Combine(directory, "c1-consumed-before.ddsave"); session.Save(remainderPath); remainder.Restore(remainderPath);
                var deniedGround = new Command("oma.c1.consumed-ground", ClericRpProfile.Actor, before.Revision, CommandKind.GroundCastingStrain);
                var remainderBytes = new SnapshotCodec().Encode(ShortRestCapture(remainder));
                Require(!remainder.QueryCastingCommand(ExpeditionSeat.Player, deniedGround).Admissible
                    && remainder.Submit(ExpeditionSeat.Player, deniedGround).Response == ExpeditionResponse.Unavailable
                    && remainderBytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(remainder))),
                    "Zero-effect consumed opportunity allowed paid Grounding or mutated rejection.");
                BishopCommit(remainder, new Command("oma.c1.remainder-rite", ClericRpProfile.Actor, before.Revision,
                    CommandKind.UseHealingRite, ConnectedExpeditionSession.Hero));
                var remainderPaid = ShortRestCapture(remainder);
                Require(remainderPaid.OrdinaryMagic.Activities.Last().ConsumedAtUse
                    && remainderPaid.OrdinaryMagic.Activities.Last().Origin.SameAs(allowance.Origin)
                    && remainderPaid.OrdinaryMagic.Settlements.Count == original.Settlements.Count,
                    "Lawful remainder magic reopened or rewrote the consumed opportunity.");
                OrdinaryMagicAdvance(remainder, allowance.Deadline, "oma.c1.remainder-boundary");
                Require(ShortRestCapture(remainder).OrdinaryMagic.Settlements.Count(x => x.Origin.SameAs(allowance.Origin)) == 1,
                    "Remainder magic produced a second settlement.");
                BishopCheckpoint(remainder, directory, "c1-remainder-after");
                var epoch = WorldTiming.ForActor(before, ClericRpProfile.Actor);
                long next = epoch.LatestStart(ClericRpProfile.Actor, epoch.ProcessedSlot) + epoch.Order.Count;
                var late = epoch.Start(next).AddSeconds(3);
                OrdinaryMagicAdvance(session, late, "oma.c1.late");
                var ready = ShortRestCapture(session); var origin = ready.OrdinaryMagic.Current.Origin;
                Require(ready.RuleClock == late && !ready.OrdinaryMagic.Current.Consumed && origin.LocalStart == next
                    && !ready.WorldIntervals.Single(x => x.ActorId == ClericRpProfile.Actor).ActionSpent,
                    "Late outside access invented a refresh or inherited a consumed opportunity.");
                BishopCheckpoint(session, directory, "c1-open-late-interval");
                var codec = new SnapshotCodec(); var unchanged = codec.Encode(ShortRestCapture(session));
                var unowned = new Command("oma.c1.unowned-cure", ClericRpProfile.Actor, ready.Revision, CommandKind.UseHealingRite,
                    ConnectedExpeditionSession.Hero, healingRite: new HealingRiteRequest(RadianceCurePreference.Frightened));
                Require(!session.QueryCastingCommand(ExpeditionSeat.Player, unowned).Admissible
                    && session.Submit(ExpeditionSeat.Player, unowned).Response == ExpeditionResponse.Unavailable
                    && unchanged.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Unowned Radiance cure did not reject atomically.");
                var rite = new Command("oma.c1.rite", ClericRpProfile.Actor, ready.Revision, CommandKind.UseHealingRite, ConnectedExpeditionSession.Hero);
                Require(session.QueryCastingCommand(ExpeditionSeat.Player, rite).Admissible, "Genuine C1 late base Rite was not discoverable/admissible.");
                BishopCommit(session, rite);
                var paid = ShortRestCapture(session);
                var use = paid.HealingRites.Single(x => x.CommandId == rite.Id);
                Require(paid.ResonancePools.Single().Current == 1 && use.ActualGain > 0 && use.TurnOrdinal == origin.GlobalStart
                    && paid.RadianceUses.Length == 0 && paid.CastingActivities.Single(x => x.CommandId == rite.Id).Turn.SameAs(origin)
                    && paid.OrdinaryMagic.Activities.Single(x => x.CommandId == rite.Id).Origin.SameAs(origin),
                    "Late Rite lost payment/origin or fabricated a passive rider.");
                BishopCheckpoint(session, directory, "c1-paid-late-rite");
                var paidBytes = codec.Encode(ShortRestCapture(session));
                Require(session.Submit(ExpeditionSeat.Player, rite).Response == ExpeditionResponse.Duplicate
                    && paidBytes.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Restored late Rite retry changed the campaign.");
                OrdinaryMagicAdvance(session, epoch.Start(next).AddSeconds(6), "oma.c1.settle");
                var after = ShortRestCapture(session);
                var end = after.OrdinaryMagic.Settlements.Single(x => x.Origin.SameAs(origin));
                Require(end.Reason == MagicalSettlementReason.OutsideDeadline && end.MagicalActivity && end.Before == 0 && end.After == 0
                    && !after.OrdinaryMagic.Current.Consumed && !after.OrdinaryMagic.Current.Origin.SameAs(origin)
                    && after.CastingTurnEnds.Length == 0, "Outside magic was settled twice or as a retroactive short End.");
                BishopCheckpoint(session, directory, "c1-after-settlement");
                OrdinaryMagicAdvance(session, after.RuleClock.AddSeconds(60), "oma.c1.zero-range");
                var sparse = ShortRestCapture(session); var calendar = sparse.OrdinaryMagic;
                var range = calendar.ZeroIdleRanges.Last(x => x.Count > 1);
                var sparseEpoch = WorldTiming.FindEpoch(sparse, range.EpochId);
                var shortened = new MagicalZeroIdleRange(range.Ordinal, range.EpochId,
                    range.FirstLocalStart + sparseEpoch.Order.Count, range.LastLocalStart, range.Count - 1,
                    range.CauseId, range.Revision, range.Through);
                var missing = sparse.Copy();
                missing.OrdinaryMagic = calendar.With(calendar.NextOrdinal, calendar.Current,
                    ranges: calendar.ZeroIdleRanges.Select(x => x.Ordinal == range.Ordinal ? shortened : x));
                Throws<ArgumentException>(() => codec.Encode(missing));
                missing.OrdinaryMagic = calendar.With(calendar.NextOrdinal, calendar.Current,
                    ranges: calendar.ZeroIdleRanges.Where(x => x.Ordinal != range.Ordinal));
                Throws<ArgumentException>(() => codec.Encode(missing));
                missing.OrdinaryMagic = calendar.With(calendar.NextOrdinal, calendar.Current,
                    settlements: calendar.Settlements.Where(x => x.Ordinal != end.Ordinal));
                Throws<ArgumentException>(() => codec.Encode(missing));
                var closure = calendar.Transitions.First(x => x.FromEpoch == x.ToEpoch);
                Require(closure.AdmissionCarry == null, "Mode change invented a duplicate historical budget claim.");
                Throws<ArgumentException>(() => new MagicalTransitionRecord(closure.Ordinal, closure.CauseId, closure.Revision,
                    closure.At, closure.Origin, closure.FromEpoch, closure.ToEpoch, closure.FromInitiative, closure.ToInitiative,
                    closure.Consumed, new ReinforcementCarry(sparse.WorldIntervals.Single(x => x.ActorId == ClericRpProfile.Actor), true)));
                BishopCheckpoint(session, directory, "c1-sparse-covered");
                File.WriteAllText(Path.Combine(directory, "coverage-forgery-scope.txt"),
                    "Detached missing/shortened range, historical outside zero settlement, and invented mode-change budget claims reject. No forged save is adopted.");
            });
            cases.Add("tac01_ordinary_magic_consumed_strain_sparse_partition_regression", () => {
                const string hero = ConnectedExpeditionSession.Hero, actor = ClericRpProfile.Actor;
                var session = EarnClericObjective(false, directory, NewOrdinaryMagicExpedition(), beforeClosure: active => {
                    for (int i = 0; i < 4; i++) {
                        ClericEnd(active, hero); ClericDefender(active); ClericGuard(active, actor);
                        BishopCommit(active, new Command("oma.sparse.guidance." + i, actor, ShortRestCapture(active).Revision,
                            CommandKind.CastKnownSpell, actor, spellCast: new SpellCastRequest("guidance", willingTarget: true)));
                        ClericEnd(active, actor); ClericGuard(active, hero);
                    }
                });
                var closed = ShortRestCapture(session); var current = closed.OrdinaryMagic.Current;
                Require(!closed.InventoryCombat && current.Consumed && closed.CastingStrain.Single().Dissonance == 6,
                    "The genuine repeated casts did not retain nonzero strain after actual closure.");
                string path = Path.Combine(directory, "consumed-strain-closure.ddsave"); session.Save(path);
                var partitioned = NewOrdinaryMagicExpedition(); partitioned.Restore(path);
                var grounded = NewOrdinaryMagicExpedition(); grounded.Restore(path);
                OrdinaryMagicAdvance(grounded, current.OriginAt.AddSeconds(9), "oma.ground.late");
                var groundBefore = ShortRestCapture(grounded); var groundOrigin = groundBefore.OrdinaryMagic.Current.Origin;
                Require(groundBefore.CastingStrain.Single().Dissonance == 6, "The outside short slot End reduced strain early.");
                var ground = new Command("oma.ground.pay", actor, groundBefore.Revision, CommandKind.GroundCastingStrain);
                Require(grounded.QueryCastingCommand(ExpeditionSeat.Player, ground).Admissible, "Late Grounding was unavailable.");
                BishopCommit(grounded, ground);
                Require(ShortRestCapture(grounded).CastingStrain.Single().Dissonance == 6
                    && ShortRestCapture(grounded).WorldIntervals.Single(x => x.ActorId == actor).ActionSpent,
                    "Grounding omitted payment or reduced strain before settlement.");
                OrdinaryMagicAdvance(grounded, current.OriginAt.AddSeconds(12), "oma.ground.settle");
                var groundAfter = ShortRestCapture(grounded); var groundEnd = groundAfter.OrdinaryMagic.Settlements.Single(x => x.Origin.SameAs(groundOrigin));
                Require(groundEnd.Grounding && !groundEnd.MagicalActivity && groundEnd.Before == 6 && groundEnd.After == 4
                    && groundAfter.CastingStrain.Single().Refrain == groundBefore.CastingStrain.Single().Refrain,
                    "Grounding stacked idle decay or changed Refrain.");
                BishopCheckpoint(grounded, directory, "grounded-late-after");
                var target = current.OriginAt.AddSeconds(24);
                OrdinaryMagicAdvance(session, target, "oma.sparse.whole");
                for (int i = 1; i <= 4; i++) OrdinaryMagicAdvance(partitioned, current.OriginAt.AddSeconds(6 * i), "oma.sparse.part." + i);
                var whole = ShortRestCapture(session); var parts = ShortRestCapture(partitioned);
                string Mechanical(Snapshot s) => string.Join(";", s.OrdinaryMagic.Settlements.Select(x =>
                    x.Origin.Binding + "|" + x.At + "|" + x.Reason + "|" + x.Before + "|" + x.After));
                Require(whole.RuleClock == target && parts.RuleClock == target && whole.CastingStrain.Single().Dissonance == 3
                    && parts.CastingStrain.Single().Dissonance == 3 && whole.RandomState == parts.RandomState
                    && whole.OrdinaryMagic.Current.Origin.SameAs(parts.OrdinaryMagic.Current.Origin)
                    && Mechanical(whole) == Mechanical(parts), "Consumed nonzero strain lost future accounting under sparse advancement.");
                BishopCheckpoint(session, directory, "sparse-whole-after");
                BishopCheckpoint(partitioned, directory, "sparse-partitioned-after");
                File.WriteAllText(Path.Combine(directory, "partition-comparison-scope.txt"),
                    "Compared actual strain, origin, clock, RNG and ordered settlement mechanics. Different advancing commands retain different receipt/revision histories; raw full-save equality is not claimed.");
            });
            AddOrdinaryMagicConsumerCases(cases, directory);
        }
    }
}
#endif
