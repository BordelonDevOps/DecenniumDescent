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
        private static ConnectedExpeditionSession NewRepertoireExpedition() => ConnectedExpeditionSession.StartWithClericRepertoire(
            ClericInitialSelection.AuthoredExample(), ClericRepertoireSelection.AuthoredExample());
        private static void RequireInitialRepertoire(Snapshot s)
        {
            Require(s.WireSchemaVersion == 106 && s.SchemaVersion == 90 && s.TestOnly && s.ConnectedClericRepertoire
                && s.KnownSpells.Select(x => x.SpellId).OrderBy(x => x, StringComparer.Ordinal).SequenceEqual(ClericRepertoireProfile.InitialSpells)
                && s.KnownSpells.All(x => x.ActorId == ClericRpProfile.Actor && x.ClassName == "Cleric" && x.MatchesSource()
                    && x.Origin == SpellAcquisitionOrigin.InitialClassRepertoire && x.AcquiredRevision == 0 && x.ClassLevel == 1
                    && x.LevelOrdinal == 1 && x.EntitlementId == ClericRepertoireProfile.InitialEntitlement)
                && s.KnownSpells.Count(x => x.Rank == 0) == 3 && s.KnownSpells.Count(x => x.Rank == 1) == 2,
                "Five exact initial spells must remain owned with source-bound construction provenance.");
        }
        private static void DenyRepertoireCommands(ConnectedExpeditionSession session)
        {
            var codec = new SnapshotCodec(); var state = ShortRestCapture(session); var before = codec.Encode(state);
            var simulation = (Simulation)typeof(ConnectedExpeditionSession).GetField("simulation", BindingFlags.Instance | BindingFlags.NonPublic).GetValue(session);
            var grant = new Authority("TEST_ONLY.host", new[] { ClericRpProfile.Actor }, inventoryOwners: new[] { ClericRpProfile.Actor });
            foreach (var kind in new[] { CommandKind.CastKnownSpell, CommandKind.AcquireEarnedSpell }) {
                foreach (string spell in kind == CommandKind.CastKnownSpell
                    ? ClericRepertoireProfile.InitialSpells.Append(ClericRepertoireProfile.FutureChoice) : new[] { ClericRepertoireProfile.FutureChoice }) {
                    var command = new Command("repertoire.deny." + spell, ClericRpProfile.Actor, state.Revision, kind, spell);
                    string code = kind == CommandKind.CastKnownSpell ? "OrdinarySpellcastingUnsupported" : "ClericEarnedAdvancementUnavailable";
                    var query = simulation.QueryCommand(grant, command);
                    Require(!query.Admissible && query.Code == code && query.Costs.Count == 0, "Unsupported capability query must not quote executable costs.");
                    var result = simulation.Execute(grant, command);
                    Require(result.Outcome == Outcome.Rejected && result.Code == code, "Typed engine request must reach the capability denial.");
                    Require(session.Submit(ExpeditionSeat.Player, command).Response == ExpeditionResponse.Unavailable,
                        "Session must forward well-formed unsupported requests to the engine.");
                    Require(before.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Denial mutated complete canonical state.");
                }
            }
        }

        private static void AddConnectedClericRepertoireCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("tac07_cleric_initial_repertoire_source_and_detached_earned_contract", () =>
            {
                var session = NewRepertoireExpedition(); var initial = ShortRestCapture(session); RequireInitialRepertoire(initial);
                Require(SpellSourceCatalog.Definitions.Count == 6 && SpellSourceCatalog.Definitions.All(x => !x.CastingSupported)
                    && SpellSourceCatalog.Get("detect-magic").Placements.Count == 2
                    && SpellSourceCatalog.Get("spare-the-dying").Placements.Count == 2
                    && SpellSourceCatalog.Get("detect-magic").AccessFor("Bard").School == "Universal"
                    && SpellSourceCatalog.Get("detect-magic").AccessFor("Cleric").School == "Divination",
                    "Global identity must preserve alternate placement and per-class source bindings.");
                Require(ClericRepertoireProfile.AssessChoice("flare-spark", 1) == "SpellClassAccessDenied"
                    && ClericRepertoireProfile.AssessChoice("dispel-magic-lesser", 2) == "SpellClassLevelDenied"
                    && ClericRepertoireProfile.AssessChoice("light", 1) == "SpellSourceAdmissionUnsupported",
                    "Negative source controls must retain their different reasons.");
                var choices = ClericRepertoireProfile.InitialSpells.ToArray();
                Throws<ArgumentException>(() => new ClericRepertoireSelection(null));
                Throws<ArgumentException>(() => new ClericRepertoireSelection(choices.Take(4)));
                Throws<ArgumentException>(() => new ClericRepertoireSelection(choices.Append("detect-magic")));
                foreach (string replacement in new[] { "guidance", "light", "flare-spark", "dispel-magic-lesser", "unknown",
                    "cleric.base.healing-rite", "spare-the-dying.universal", "detect-magic" }) {
                    var invalid = choices.ToArray(); invalid[0] = replacement;
                    Throws<ArgumentException>(() => new ClericRepertoireSelection(invalid));
                }
                var selection = new ClericRepertoireSelection(choices.Reverse()); choices[0] = "unknown";
                Require(selection.SpellIds.SequenceEqual(ClericRepertoireProfile.InitialSpells), "Selection must copy and normalize caller input.");
                Throws<ArgumentNullException>(() => ConnectedExpeditionSession.StartWithClericRepertoire(null, selection));
                Throws<ArgumentNullException>(() => ConnectedExpeditionSession.StartWithClericRepertoire(ClericInitialSelection.AuthoredExample(), null));
                DenyRepertoireCommands(session);

                // Detached mechanical settlement inputs only: this is not lawful connected campaign advancement/history.
                var settle = typeof(TestOnlySharedWorldPolicy).GetMethod("SettleClericEarnedRepertoire", BindingFlags.Static | BindingFlags.NonPublic);
                var staged = initial.Copy(); staged.Revision = 10;
                string actor = ClericRpProfile.Actor; var character = staged.Characters.Single(x => x.ActorId == actor);
                staged.Characters = staged.Characters.Select(x => x.ActorId != actor ? x : new ActorCharacterRecord(actor,
                    character.ProfileId, character.Abilities, character.Levels.Append(new CharacterLevelFact("Cleric", 5)))).ToArray();
                var advancement = new CharacterAdvancementRecord(actor, "TEST_ONLY.detached-milestone", 11, 1, 2, "Cleric", 2, 5,
                    HitPointGainMethod.FixedAverage, 8, 13, 8, 8, new[] { "cleric.base.judging-light", "cleric.base.conviction-pool" });
                staged.CharacterMilestones = new[] { new CharacterMilestoneRecord(advancement.MilestoneId, actor, 9, 11) };
                staged.CharacterAdvancements = new[] { advancement };
                void Settle(Snapshot candidate, string id = "detect-magic") => settle.Invoke(null, new object[] { candidate, actor, id, advancement });
                foreach (string spell in new[] { "guidance", "light", "flare-spark", "dispel-magic-lesser", "unknown" }) {
                    var denied = staged.Copy(); var owned = denied.KnownSpells;
                    Throws<TargetInvocationException>(() => Settle(denied, spell));
                    Require(ReferenceEquals(owned, denied.KnownSpells), "Invalid earned choice must not mutate ownership.");
                }
                foreach (int invalid in Enumerable.Range(0, 4)) {
                    var denied = staged.Copy(); var owned = denied.KnownSpells;
                    if (invalid == 0) denied.CharacterMilestones = Array.Empty<CharacterMilestoneRecord>();
                    if (invalid == 1) denied.CharacterMilestones = new[] { new CharacterMilestoneRecord(advancement.MilestoneId, actor, 9) };
                    if (invalid == 2) denied.Characters = initial.Characters;
                    if (invalid == 3) denied.CharacterAdvancements = Array.Empty<CharacterAdvancementRecord>();
                    Throws<TargetInvocationException>(() => Settle(denied));
                    Require(ReferenceEquals(owned, denied.KnownSpells), "Unsettled milestone or class must reject unchanged.");
                }
                uint rng = staged.RandomState; var clock = staged.RuleClock; var pools = staged.ResonancePools; var lives = staged.Lives;
                Settle(staged); var earned = staged.KnownSpells.Last();
                Require(staged.KnownSpells.Length == 6 && earned.SpellId == "detect-magic" && earned.ClassLevel == 2 && earned.Rank == 1
                    && earned.Origin == SpellAcquisitionOrigin.EarnedClassLevel && earned.MilestoneId == advancement.MilestoneId
                    && earned.AcquiredRevision == 11 && staged.Revision == 10 && staged.RandomState == rng && staged.RuleClock == clock
                    && ReferenceEquals(pools, staged.ResonancePools) && ReferenceEquals(lives, staged.Lives),
                    "Detached settlement must add only the exact earned provenance; no implicit resource/time/RNG changes.");
                var settled = staged.KnownSpells; Throws<TargetInvocationException>(() => Settle(staged));
                Require(ReferenceEquals(settled, staged.KnownSpells), "One level entitlement cannot settle twice.");
                Throws<ArgumentException>(() => new SnapshotCodec().Encode(staged));
                RequireInitialRepertoire(ShortRestCapture(session));
            });

            cases.Add("tac07_cleric_repertoire_connected_payment_restore_and_denials", () =>
            {
                const string hero = ConnectedExpeditionSession.Hero, ally = ClericRpProfile.Actor;
                var session = ClericInjuredArrival(NewRepertoireExpedition()); var codec = new SnapshotCodec();
                RequireInitialRepertoire(ShortRestCapture(session)); DenyRepertoireCommands(session);
                ClericGuard(session, ally); ClericCommit(session, ally, CommandKind.UseHealingRite, ally);
                var paid = ShortRestCapture(session); RequireInitialRepertoire(paid);
                Require(paid.HealingRites.Single().ActualGain > 0 && paid.ResonancePools.Single().Current == 1
                    && paid.AlchemyDoses.Length == 6, "Connected route must retain actual injury/healing, RP payment and prepared doses.");
                string path = Path.Combine(directory, "repertoire-paid.ddsave"); session.Save(path);
                session = NewRepertoireExpedition(); session.Restore(path);
                Require(codec.Encode(paid).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Repertoire save/restore changed paid state.");
                DenyRepertoireCommands(session);
                ClericEnd(session, ally);
                ClericGuard(session, hero);
                ClericCommit(session, hero, CommandKind.TacticalStep, session.View(ExpeditionSeat.Player).TurnId, y: 2);
                ClericEnd(session, hero); ClericDefender(session); ClericGuard(session, ally); ClericEnd(session, ally);
                for (int round = 0; ; round++) {
                    Require(round < 24, "Connected encounter failed to conclude.");
                    ClericGuard(session, hero);
                    if (ShortRestCapture(session).Lives.Single(x => x.ActorId == "TEST_ONLY.later-defender").Dead) break;
                    ClericCommit(session, hero, CommandKind.AttackClub, "TEST_ONLY.later-defender",
                        combat: new CombatRequest(session.View(ExpeditionSeat.Player).TurnId, "TEST_ONLY.actor-club"));
                    ClericEnd(session, hero); ClericDefender(session); ClericGuard(session, ally); ClericEnd(session, ally);
                }
                ClericCommit(session, hero, CommandKind.EndFixedEncounter, session.View(ExpeditionSeat.Player).TurnId);
                ClericCommit(session, hero, CommandKind.BeginWorldStep, "walk", y: -1);
                ClericCommit(session, hero, CommandKind.AdvanceClock, x: 6, y: 1);
                var continued = ShortRestCapture(session); RequireInitialRepertoire(continued); DenyRepertoireCommands(session);
                session.Save(path); session.Restore(path);
                Require(!continued.InventoryCombat && continued.ResonancePools.Single().Current == 1 && continued.AlchemyDoses.Length == 6
                    && codec.Encode(continued).SequenceEqual(codec.Encode(ShortRestCapture(session))), "Paid continuation/replay must preserve ownership and resources.");
            });

            cases.Add("tac07_cleric_repertoire_forgery_legacy_and_authority_boundaries", () =>
            {
                var session = NewRepertoireExpedition(); var initial = ShortRestCapture(session); var codec = new SnapshotCodec();
                var legacy = NewClericExpedition(); var old = ShortRestCapture(legacy); var before = codec.Encode(initial);
                string oldPath = Path.Combine(directory, "repertoire-authentic105.ddsave"), newPath = Path.Combine(directory, "repertoire-initial106.ddsave");
                legacy.Save(oldPath); session.Save(newPath);
                legacy.Restore(oldPath);
                Require(old.WireSchemaVersion == 105 && old.KnownSpells.Length == 0 && !old.ConnectedClericRepertoire
                    && codec.Encode(old).SequenceEqual(codec.Encode(ShortRestCapture(legacy))), "Old105 cannot gain implicit knowledge.");
                Throws<ArgumentException>(() => session.Restore(oldPath)); Throws<ArgumentException>(() => legacy.Restore(newPath));
                Require(before.SequenceEqual(codec.Encode(ShortRestCapture(session))) && codec.Encode(old).SequenceEqual(codec.Encode(ShortRestCapture(legacy))),
                    "Cross-profile restore must be atomic.");
                var known = initial.KnownSpells[0];
                void Reject(Snapshot s) => Throws<ArgumentException>(() => codec.Encode(s));
                foreach (int control in Enumerable.Range(0, 13)) {
                    var s = initial.Copy();
                    if (control == 0) s.KnownSpells = s.KnownSpells.Take(4).ToArray();
                    if (control == 1) s.KnownSpells = s.KnownSpells.Append(known).ToArray();
                    if (control == 2) s.KnownSpells = s.KnownSpells.Append(KnownSpellRecord.FromSource(ClericRpProfile.Actor, "detect-magic",
                        SpellAcquisitionOrigin.EarnedClassLevel, 2, 2, ClericRepertoireProfile.EarnedEntitlement, "forged.milestone", 1)).ToArray();
                    if (control == 3) s.TestOnly = false;
                    if (control == 4) s.ConnectedClericRepertoire = false;
                    if (control >= 5) s.KnownSpells[0] = new KnownSpellRecord(control == 5 ? ConnectedExpeditionSession.Hero : known.ActorId,
                        control == 6 ? "Bard" : known.ClassName, known.SpellId, control == 7 ? new string('0', 40) : known.SourceRevision,
                        control == 8 ? new string('0', 64) : known.WholeCardSha256, control == 9 ? new string('0', 64) : known.ProcedureSha256,
                        control == 10 ? "Universal" : known.School, control == 12 ? 1 : known.Rank, known.Origin, known.ClassLevel, known.LevelOrdinal,
                        control == 11 ? "forged.entitlement" : known.EntitlementId, known.MilestoneId, known.AcquiredRevision);
                    Reject(s);
                }
                var bad = old.Copy(); bad.KnownSpells = initial.KnownSpells; Reject(bad);
                bad = initial.Copy(); var spare = bad.KnownSpells.Single(x => x.SpellId == "spare-the-dying");
                bad.KnownSpells = bad.KnownSpells.Select(x => x != spare ? x : new KnownSpellRecord(spare.ActorId, spare.ClassName,
                    spare.SpellId, spare.SourceRevision, spare.WholeCardSha256, spare.ProcedureSha256, "Universal", spare.Rank,
                    spare.Origin, spare.ClassLevel, spare.LevelOrdinal, spare.EntitlementId, spare.MilestoneId, spare.AcquiredRevision)).ToArray();
                Reject(bad);
                var command = new Command("repertoire.authority", ClericRpProfile.Actor, 0, CommandKind.CastKnownSpell, "guidance");
                session.SetSeatEnabled(ExpeditionSeat.Player, false);
                Require(session.Submit(ExpeditionSeat.Player, command).Response == ExpeditionResponse.NotAuthorized, "Revoked seat must not reach capability state.");
                session.SetSeatEnabled(ExpeditionSeat.Player, true);
                Require(session.Submit(ExpeditionSeat.FirstOpponent, command).Response == ExpeditionResponse.NotAuthorized
                    && session.Submit(ExpeditionSeat.Player, new Command("repertoire.stale", ClericRpProfile.Actor, 1,
                        CommandKind.AcquireEarnedSpell, "detect-magic")).Response == ExpeditionResponse.StaleRevision
                    && before.SequenceEqual(codec.Encode(ShortRestCapture(session))), "Authority and expected revision must precede denial without mutation.");
                var own = session.View(ExpeditionSeat.Player).Actors.Single(x => x.Position.Id == ClericRpProfile.Actor).Repertoire;
                Require(own.KnownSpells.Count == 5 && !own.FutureChoiceOwned && own.KnownSpells.All(x => !x.CastingSupported)
                    && session.View(ExpeditionSeat.FirstOpponent).Actors.All(x => x.Repertoire == null), "Only owning seat may see spell knowledge/provenance.");
            });
        }
    }
}
#endif
