using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    public static partial class OrdinaryMagicProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.ordinary-magic-v1-";
        public const string Approval = "07b5b8fe-e82f-5d53-b4ed-42087afbd942";
        public const string RepresentationApproval = "8bd7afb5-3691-50e2-ac9a-1faaa9179ccf";
        public const string ContractHash = "bf565dfce8661dae67df214a8b5fd736c845ad06074622ad758f82fa9faf239d";
        public const byte Marker = 21;
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
            || ConnectedWorkControlProfile.SelectedFingerprint(value));
        public static bool IsPredecessor(string value) => value != null && value.StartsWith(ConsecrationProfile.FingerprintPrefix, StringComparison.Ordinal)
            && CreatureActorRecord.Hex(value.Substring(ConsecrationProfile.FingerprintPrefix.Length), 64);
        public static string BindFingerprint(string predecessor)
        {
            if (!IsPredecessor(predecessor)) throw new ArgumentException("Ordinary magic requires its qualified Consecration predecessor.");
            using (var hash = SHA256.Create()) return FingerprintPrefix + string.Concat(hash.ComputeHash(Encoding.UTF8.GetBytes(
                string.Join("|", predecessor, Approval, ContractHash, RepresentationApproval,
                    "CAL01-05|actual-origin|one-settlement|six-consumers|no-bootstrap-casting|admission-only-carry")))
                .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
        internal static void RequireEvent(long ordinal, string cause, long revision)
        {
            if (ordinal < 1 || revision < 1 || !Validation.ValidId(cause)) throw new ArgumentException("Invalid magical event provenance.");
        }
        internal static void RequireOrigin(SpellTurnIdentity origin)
        {
            if (origin == null || origin.IsCarried || origin.ActorId != ClericRpProfile.Actor)
                throw new ArgumentException("Magical activity requires its real originating Start.");
        }
        public static bool SameOrigin(SpellTurnIdentity left, SpellTurnIdentity right)
            => left == null ? right == null : left.SameAs(right);
        public static bool SupportedEpoch(Snapshot s, string epoch) => epoch != null
            && (epoch == s.Reinforcement?.Admission?.Phase.Epoch.Id || PostRecoveryProfile.IsEpoch(s, epoch) || FerryWraithProfile.IsEpoch(s, epoch));

        /// <summary>Pure calendar assessment only. Producer preflight retains Action, source,
        /// condition, component, work and authority checks. Paid cure factories may call this
        /// after expenditure without falsely requiring a second unspent Action.</summary>
        public static string ContextFailure(Snapshot s, string actor)
        {
            if (s.OrdinaryMagic == null || actor != ClericRpProfile.Actor) return "OrdinaryMagicalActivityUnsupported";
            var current = s.OrdinaryMagic.Current;
            var epoch = WorldTiming.ForActor(s, actor);
            if (current?.Origin == null || epoch == null || !SupportedEpoch(s, epoch.Id)) return "MagicalAllowanceUnavailable";
            if (current.ContextEpoch != epoch.Id || current.InInitiative != s.InventoryCombat) return "MagicalContextBoundaryPending";
            var interval = s.WorldIntervals.SingleOrDefault(x => x.ActorId == actor);
            if (interval == null || interval.LastStart != (current.Origin.EpochId == epoch.Id ? current.Origin.GlobalStart : -1))
                return "MagicalAllowanceBoundaryPending";
            long slot = epoch.SlotAt(s.RuleClock);
            if (slot != epoch.ProcessedSlot) return "MagicalContextBoundaryPending";
            if (s.InventoryCombat) {
                if (s.Encounter == null || WorldTiming.ForEncounter(s)?.Id != epoch.Id || s.Encounter.CurrentActor != actor
                    || s.InventoryTurnActor != actor || current.Origin.EpochId != epoch.Id || current.Origin.LocalStart != slot)
                    return "WrongRegularTurn";
            } else {
                string encounter = FerryWraithProfile.IsEpoch(s, epoch.Id) ? FerryWraithProfile.Encounter
                    : PostRecoveryProfile.IsEpoch(s, epoch.Id) ? PostRecoveryEncounterDefinition.Encounter : s.Reinforcement.Definition.EncounterId;
                if (s.Encounter != null || !s.ClosedEncounters.Any(x => x.Encounter.Id == encounter
                    || epoch.Id == s.Reinforcement?.Admission?.Phase.Epoch.Id && s.Reengagement?.IsSegment(x.Encounter.Id) == true))
                    return "MagicalActivityContextUnsupported";
            }
            if (!current.Consumed && current.Deadline <= s.RuleClock) return "MagicalAccountingBoundaryPending";
            return null;
        }
        public static MagicalActivityContextRecord Activity(Snapshot s, string command)
            => s.OrdinaryMagic?.Activities.SingleOrDefault(x => x.CommandId == command);
        public static bool ValidActivity(Snapshot s, string command, SpellTurnIdentity origin, RuleTime at)
        {
            var row = Activity(s, command);
            return row != null && row.At == at && row.Origin.SameAs(origin);
        }
        public static bool ValidActivityContext(Snapshot s, string command, string originEpoch, long local, long global, RuleTime at)
        {
            var row = Activity(s, command);
            return row != null && row.At == at && row.Origin.EpochId == originEpoch
                && row.Origin.LocalStart == local && row.Origin.GlobalStart == global;
        }
        public static bool IsSkippedStart(Snapshot s, WorldScheduleRecord epoch, long local)
        {
            var phase = s.Reinforcement?.Admission?.Phase;
            var exit = s.Retreat?.SuccessfulExit;
            return local >= 0 && phase != null && exit != null && epoch.Id == phase.Epoch.Id
                && phase.GlobalTurn(local) == exit.EndTurn + 1 && epoch.LatestStart(ClericRpProfile.Actor, local) == local;
        }
        public static long FirstOwnerStart(WorldScheduleRecord epoch) => epoch.Order.ToList().IndexOf(ClericRpProfile.Actor);
        public static long NextOwnerStart(Snapshot s, WorldScheduleRecord epoch, RuleTime at)
        {
            long local = epoch.LatestStart(ClericRpProfile.Actor, epoch.SlotAt(at));
            long next = local < 0 ? FirstOwnerStart(epoch) : checked(local + epoch.Order.Count);
            return next;
        }
        public static SpellTurnIdentity OriginAt(Snapshot s, WorldScheduleRecord epoch, long local)
            => new SpellTurnIdentity(ClericRpProfile.Actor, epoch.Id, local, WorldTiming.TurnOrdinal(s, epoch.Id, local));

        public static void ValidateRecharge(Snapshot s, string command, CharacterAbilityRechargeRecord recharge)
        {
            var use = Activity(s, command);
            if (use == null || recharge.ActorId != use.Origin.ActorId) throw new ArgumentException("Recharge lacks its paid context.");
            var epochs = new[] { s.Reinforcement?.Admission?.Phase.Epoch, s.PostRecoveryEncounter?.Admission?.Epoch,
                s.FerryWraith?.Admission?.Epoch }.Where(x => x != null).ToArray();
            int first = Array.FindIndex(epochs, x => x.Id == use.ContextEpoch);
            if (first < 0) throw new ArgumentException("Recharge has no actual application context.");
            var cursorEpoch = WorldTiming.FindEpoch(s, use.Origin.EpochId);
            long cursor = use.Origin.LocalStart, ticks = 0;
            for (int i = first; i < epochs.Length; i++) {
                var epoch = epochs[i];
                RuleTime until = i + 1 < epochs.Length ? epochs[i + 1].Origin : s.RuleClock;
                long last = epoch.LatestStart(ClericRpProfile.Actor, Math.Min(epoch.ProcessedSlot, epoch.SlotAt(until)));
                if (i + 1 < epochs.Length && last >= 0 && epoch.Start(last) == until) last -= epoch.Order.Count;
                if (IsSkippedStart(s, epoch, last)) last -= epoch.Order.Count;
                long after = i == first ? epoch.LatestStart(ClericRpProfile.Actor, epoch.SlotAt(use.At)) : -1;
                long count = ConsecrationProfile.CountRechargeStarts(s, epoch, ClericRpProfile.Actor, after, last);
                if (count == 0) continue;
                ticks = checked(ticks + count); cursorEpoch = epoch; cursor = last;
            }
            if (recharge.EpochId != cursorEpoch.Id || recharge.LastLocalStart != cursor
                || recharge.LastStartAt != cursorEpoch.Start(cursor) || recharge.Remaining != Math.Max(0L, 3L - ticks))
                throw new ArgumentException("Recharge differs from actual post-use owner Starts.");
        }
    }
}
