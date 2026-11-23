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
        private static void OrdinaryMagicNextLate(ConnectedExpeditionSession session, string id)
        {
            var state = ShortRestCapture(session); var epoch = WorldTiming.ForActor(state, ClericRpProfile.Actor);
            long next = epoch.LatestStart(ClericRpProfile.Actor, epoch.ProcessedSlot) + epoch.Order.Count;
            OrdinaryMagicAdvance(session, epoch.Start(next).AddSeconds(3), id);
        }
        private static void AddOrdinaryMagicConsumerCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac01_ordinary_magic_genuine_bishop_consumers_and_long_rest", () => {
                const string actor = ClericRpProfile.Actor, hero = ConnectedExpeditionSession.Hero;
                var session = FundBishop(directory, expedition: NewOrdinaryMagicExpedition());
                Snapshot State() => ShortRestCapture(session);
                var funded = State(); var codec = new SnapshotCodec();
                Require(!funded.InventoryCombat && funded.ResonancePools.Single().Current == 7
                    && funded.ClericLongRestSettlements.Length == 2 && funded.OrdinaryMagic.ZeroIdleRanges.Sum(x => x.Count) > 4800
                    && funded.OrdinaryMagic.Settlements.Count < 2048 && funded.CastingTurnEnds.Length == 0,
                    "Genuine long rests lost funding or expanded harmless intervals into legacy End rows.");
                var historicalEnd = funded.OrdinaryMagic.Settlements.First(x => x.Reason == MagicalSettlementReason.OutsideDeadline
                    && x.MagicalActivity && x.Before == 0 && x.After == 0);
                var historicalActivity = funded.OrdinaryMagic.Activities.Single(x => x.Origin.SameAs(historicalEnd.Origin));
                Require(historicalActivity.At < historicalEnd.At, "Missing genuine temporal ordering forgery witness.");
                var reordered = funded.Copy(); var calendar = funded.OrdinaryMagic;
                var reversedActivity = new MagicalActivityContextRecord(historicalEnd.Ordinal, historicalActivity.CommandId,
                    historicalActivity.Revision, historicalActivity.At, historicalActivity.Origin, historicalActivity.SegmentOrdinal,
                    historicalActivity.ContextEpoch, historicalActivity.InInitiative, true, historicalActivity.Kind);
                var reversedEnd = new MagicalSettlementRecord(historicalActivity.Ordinal, historicalEnd.Origin, historicalEnd.SegmentOrdinal,
                    historicalEnd.ContextEpoch, historicalEnd.CauseId, historicalEnd.Revision, historicalEnd.At, historicalEnd.Reason,
                    historicalEnd.IdleEligible, false, false, historicalEnd.Proficiency, 0, 0);
                reordered.OrdinaryMagic = calendar.With(calendar.NextOrdinal, calendar.Current,
                    activities: calendar.Activities.Select(x => x.Ordinal == historicalActivity.Ordinal ? reversedActivity : x),
                    settlements: calendar.Settlements.Select(x => x.Ordinal == historicalEnd.Ordinal ? reversedEnd : x));
                Throws<ArgumentException>(() => codec.Encode(reordered));
                File.WriteAllText(Path.Combine(directory, "chronology-forgery-scope.txt"),
                    "Detached swap of genuine earlier zero-strain magic and later settlement ordinals rejects despite preserved row counts, contiguous ordinals and numeric outcomes. No forged save was adopted.");
                void Paid(Command command) {
                    var before = codec.Encode(State());
                    Require(session.QueryCastingCommand(ExpeditionSeat.Player, command).Admissible
                        && before.SequenceEqual(codec.Encode(State())), "Late consumer query was unavailable or impure: " + command.Kind);
                    BishopCommit(session, command);
                    var activity = State().OrdinaryMagic.Activities.Single(x => x.CommandId == command.Id);
                    var epoch = WorldTiming.FindEpoch(State(), activity.Origin.EpochId);
                    Require(!activity.InInitiative && activity.At == epoch.Start(activity.Origin.LocalStart).AddSeconds(3)
                        && !activity.ConsumedAtUse, "Late consumer was attributed to a virtual short End or another allowance.");
                }
                OrdinaryMagicNextLate(session, "oma.consumers.consecrate-time");
                var at = State(); var body = at.Actors.Single(x => x.Id == actor);
                Paid(new Command("oma.consumers.consecrate", actor, at.Revision, CommandKind.UseConsecrate,
                    consecrate: new ConsecrateRequest(body.X, body.Y)));
                var zone = State().Consecration.Zones.Single();
                Require(State().ResonancePools.Single().Current == 5 && zone.ExpiresAt == zone.At.AddSeconds(18)
                    && State().AbilityRecharges.Single(x => x.AbilityId == ConsecrationProfile.Consecrate).Remaining == 3,
                    "Late Consecrate changed actual cost, captured lifetime or recharge.");
                BishopCheckpoint(session, directory, "ordinary-late-consecrate");
                OrdinaryMagicNextLate(session, "oma.consumers.invocation-time");
                at = State();
                Paid(new Command("oma.consumers.invocation", actor, at.Revision, CommandKind.UseDivineInvocation,
                    divineInvocation: new DivineInvocationRequest(new[] { hero, actor })));
                Require(State().ResonancePools.Single().Current == 2 && State().ConvictionBalance.Current == 3
                    && State().BishopEntry.Invocations.Single().Turn.SameAs(State().OrdinaryMagic.Current.Origin),
                    "Late Invocation lost its actual source payment or stable interval.");
                BishopCheckpoint(session, directory, "ordinary-late-invocation");
                OrdinaryMagicNextLate(session, "oma.consumers.guidance-time");
                Paid(new Command("oma.consumers.guidance", actor, State().Revision, CommandKind.CastKnownSpell, hero,
                    spellCast: new SpellCastRequest("guidance", willingTarget: true)));
                OrdinaryMagicNextLate(session, "oma.consumers.detect-time");
                Paid(new Command("oma.consumers.detect", actor, State().Revision, CommandKind.CastKnownSpell, actor,
                    spellCast: new SpellCastRequest("detect-magic", SpellCastingProfile.FocusId)));
                var detected = State(); var views = session.View(ExpeditionSeat.Player);
                var target = views.Actors.Single(x => x.Position.Id == hero).Position;
                var aura = views.Actors.Single(x => x.Position.Id == actor).Casting.Auras.Single(x => x.X == target.X && x.Y == target.Y);
                Require(detected.ResonancePools.Single().Current == 0 && detected.Consecration.Zones.Single().End == ConsecrationEnd.Expiry
                    && detected.Consecration.Zones.Single().EndAt == zone.ExpiresAt
                    && detected.AbilityRecharges.Single(x => x.AbilityId == ConsecrationProfile.Consecrate).Remaining == 0,
                    "Captured terrain expiry or actual Start recharge moved with late activity.");
                OrdinaryMagicNextLate(session, "oma.consumers.focus-time");
                var focusBefore = State();
                Paid(new Command("oma.consumers.focus", actor, focusBefore.Revision, CommandKind.FocusDetectedAura, aura.ObservationId));
                Require(State().SpellCasts.Length == focusBefore.SpellCasts.Length && State().RandomState == focusBefore.RandomState
                    && State().DetectMagicFocuses.Single().ObservationId == aura.ObservationId,
                    "Paid focus invented a spell cast or RNG.");
                BishopCheckpoint(session, directory, "ordinary-late-focus");
                OrdinaryMagicNextLate(session, "oma.consumers.ground-time");
                var groundBefore = State(); var groundOrigin = groundBefore.OrdinaryMagic.Current.Origin;
                Require(groundBefore.CastingStrain.Single().Dissonance > 0, "The genuine cast sequence did not produce meaningful Grounding strain.");
                Paid(new Command("oma.consumers.ground", actor, groundBefore.Revision, CommandKind.GroundCastingStrain));
                OrdinaryMagicAdvance(session, groundBefore.OrdinaryMagic.Current.Deadline, "oma.consumers.ground-end");
                var end = State().OrdinaryMagic.Settlements.Single(x => x.Origin.SameAs(groundOrigin));
                Require(end.Grounding && !end.MagicalActivity && end.After == Math.Max(0, end.Before - 2)
                    && State().SpellEffects.Any(x => x.Present && x.SpellId == "detect-magic"),
                    "Passive concentration prevented exclusive Grounding reduction.");
                BishopCheckpoint(session, directory, "ordinary-consumers-continued");
                File.WriteAllText(Path.Combine(directory, "ordinary-consumer-facts.json"), System.Text.Json.JsonSerializer.Serialize(new {
                    scope = "Fresh genuine acquire/combat/earn/long-rest/manage/prepare prefix, late Consecrate/Invocation/spell/focus/Grounding, captured expiry/recharge, continued outside play",
                    State().Revision, State().RuleClock, State().OrdinaryMagic, State().CastingStrain, State().AbilityRecharges
                }));
            });
        }
    }
}
#endif
