#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static void AddCommandHistoryCases(Dictionary<string, Action> cases)
        {
            CommandReceipt Receipt(string fingerprint, long revision = 1) => new CommandReceipt {
                Principal = "TEST_ONLY.host", Id = "history.test", Revision = revision, Fingerprint = fingerprint };
            string Header(CommandKind kind, string target = "", long revision = 0) => ((int)kind).ToString(System.Globalization.CultureInfo.InvariantCulture)
                + "|" + TestOnlyPolicy.ActorId + "|" + target + "|" + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + "|0|0";
            cases.Add("command_history_reads_actual_mixed_inventory_receipts", () => {
                var s = Inventory(); string portion = Portion(s, Q(1)); Eat(s, Q(1,3), portion); AdvanceI(s, 300);
                foreach (var receipt in s.Capture().Receipts) {
                    var c = CommandHistory.Read(receipt); Require(c.MatchesReceipt(receipt), "Existing committed payload changed.");
                }
                var copy = new Simulation(new TestOnlyInventoryPolicy(), new TestOnlyInventoryPolicy().Initial(), ExecutionProfile.Laboratory);
                foreach (var receipt in s.Capture().Receipts) Require(copy.Execute(TestOnlyInventoryPolicy.Host(), CommandHistory.Read(receipt)).Outcome == Outcome.Committed, "Mixed history failed ordinary command path.");
                Require(Bytes(s).SequenceEqual(Bytes(copy)), "Reconstructed mixed history changed state.");
            });
            cases.Add("command_history_reads_both_canonical_combat_versions", () => {
                foreach (var choice in new[] { PressHitInstruction.ArmOrReplace, PressHitInstruction.KeepExisting }) {
                    var s = Tactical(); CommitTac(s, Tac(s, CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId, press: choice));
                    var receipt = s.Capture().Receipts.Last(); var c = CommandHistory.Read(receipt);
                    Require(c.Combat.PressInstruction == choice && c.MatchesReceipt(receipt), "Combat choice lost on reconstruction.");
                }
            });
            cases.Add("command_history_rejects_noncanonical_quantities_and_integers", () => {
                string prefix = Header(CommandKind.PortionInventory, TestOnlyInventoryPolicy.FoodId) + "|inventory-v1|";
                foreach (string q in new[] { "2/4", "01/2", "1/02", "+1/2", "-1/2", "1/0", "0/2", "1 /2", "1/2/3", "9223372036854775808/1" })
                    Throws<ArgumentException>(() => CommandHistory.Read(Receipt(prefix + q + "||0")));
                foreach (string text in new[] { "01|actor||0|0|0", "+1|actor||0|0|0", "1|actor||00|0|0", "1|actor||0|-0|0", "1|actor||0| 0|0", "1|actor||0|2147483648|0" })
                    Throws<ArgumentException>(() => CommandHistory.Read(Receipt(text)));
            });
            cases.Add("command_history_rejects_unknown_tags_flags_and_trailing_fields", () => {
                string header = Header(CommandKind.AttackUnarmed, TestOnlyPolicy.CompanionId);
                foreach (string suffix in new[] { "|combat-v3|turn||0|0|0", "|combat-v1|turn||0|0|2", "|combat-v2|turn||0|0|0|0", "|combat-v1|turn||0|0|0|1",
                    "|combat-v2|turn||0|0|0|1|extra", "|inventory-v2|1/1||0", "|inventory-v1|1/1||99", "|combat-v1|turn||6|0|0", "|combat-v1|turn||0|9|0" })
                    Throws<ArgumentException>(() => CommandHistory.Read(Receipt(header + suffix)));
            });
            cases.Add("command_history_requires_matching_revision_and_bounded_identities", () => {
                Throws<ArgumentException>(() => CommandHistory.Read(null));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(Header(CommandKind.Move), 0)));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(Header(CommandKind.Move), 2)));
                foreach (string field in new[] { "", "bad id", new string('a',97) }) {
                    var r = Receipt(Header(CommandKind.Move)); r.Principal = field; Throws<ArgumentException>(() => CommandHistory.Read(r));
                    r = Receipt(Header(CommandKind.Move)); r.Id = field; Throws<ArgumentException>(() => CommandHistory.Read(r));
                }
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt(new string('x',513))));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt("999|actor||0|0|0")));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt("1|bad actor||0|0|0")));
                Throws<ArgumentException>(() => CommandHistory.Read(Receipt("1|actor|bad target|0|0|0")));
            });
            cases.Add("command_history_reconstruction_does_not_authorize_execution", () => {
                var s = Tactical(); var r = s.Capture().Receipts.Last(); var command = CommandHistory.Read(r);
                RejectUnchanged(s, new Authority(r.Principal, Array.Empty<string>()), command, "NotAuthorized");
                var other = Clubs(); RejectUnchanged(other, TacticalCombatFixture.Host(), command, "StaleRevision");
            });
        }
    }
}
#endif
