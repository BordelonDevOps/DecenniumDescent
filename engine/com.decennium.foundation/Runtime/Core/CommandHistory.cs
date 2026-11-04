using System;
using System.Globalization;

namespace Decennium.Foundation
{
    /// <summary>Strict reconstruction of an existing receipt payload. This supplies no authority,
    /// source eligibility or state validation; callers still replay through their selected policy.</summary>
    public static class CommandHistory
    {
        public static Command Read(CommandReceipt receipt)
        {
            if (receipt == null || !Validation.ValidId(receipt.Id) || !Validation.ValidId(receipt.Principal)
                || receipt.Revision < 1 || string.IsNullOrEmpty(receipt.Fingerprint) || receipt.Fingerprint.Length > 512)
                throw new ArgumentException("Invalid command receipt.");
            var p = receipt.Fingerprint.Split('|');
            if (p.Length != 6 && p.Length != 10 && p.Length != 12 && p.Length != 13) throw new ArgumentException("Invalid receipt fields.");
            int Int(string value) => int.TryParse(value, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out int n)
                ? n : throw new ArgumentException("Invalid receipt integer.");
            long Long(string value) => long.TryParse(value, NumberStyles.None, CultureInfo.InvariantCulture, out long n)
                ? n : throw new ArgumentException("Invalid receipt quantity.");
            var kind = (CommandKind)Int(p[0]);
            if (!Enum.IsDefined(typeof(CommandKind), kind) || !Validation.ValidId(p[1]) || p[2] != "" && !Validation.ValidId(p[2]))
                throw new ArgumentException("Invalid receipt identity or command kind.");
            InventoryRequest inventory = null; CombatRequest combat = null;
            if (p.Length == 10) {
                if (p[6] != "inventory-v1") throw new ArgumentException("Unknown inventory receipt version.");
                var q = p[7].Split('/'); if (q.Length != 2) throw new ArgumentException("Invalid receipt fraction.");
                inventory = new InventoryRequest(new RuleQuantity(Long(q[0]), Long(q[1])), p[8], (HandlingKind)Int(p[9]));
            }
            if (p.Length >= 12) {
                if (p[6] != (p.Length == 12 ? "combat-v1" : "combat-v2") || p.Length == 13 && p[12] != "1"
                    || p[11] != "0" && p[11] != "1") throw new ArgumentException("Invalid combat receipt version or flag.");
                combat = new CombatRequest(p[7], p[8], Int(p[9]), (AttackKnockoutMode)Int(p[10]), p[11] == "1",
                    p.Length == 13 ? PressHitInstruction.KeepExisting : PressHitInstruction.ArmOrReplace);
            }
            var command = new Command(receipt.Id, p[1], receipt.Revision - 1, kind, p[2], Int(p[4]), Int(p[5]), inventory, combat);
            // Includes expected revision and exact canonical numeric representation, versions and fields.
            if (!command.MatchesReceipt(receipt)) throw new ArgumentException("Noncanonical or inconsistent command receipt.");
            return command;
        }
    }
}
