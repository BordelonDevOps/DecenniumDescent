using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    public sealed class ConsecrateRequest
    {
        public int X { get; }
        public int Y { get; }
        public ConsecrateRequest(int x, int y) { X = x; Y = y; }
        internal string Fingerprint => X.ToString(CultureInfo.InvariantCulture) + "|" + Y.ToString(CultureInfo.InvariantCulture);
    }

    public enum ConsecrationEnd { Active, Expiry, Replacement }

    /// <summary>A paid fixed terrain application. The original deadline never follows a later actor epoch.</summary>
    public sealed class ConsecrationZone
    {
        public string CommandId { get; }
        public long Revision { get; }
        public string OwnerId { get; }
        public string SourceId => ConsecrationProfile.Consecrate;
        public string SourceRevision => ClericRpProfile.SourceRevision;
        public string AreaId => ConsecrationProfile.Area;
        public int X { get; }
        public int Y { get; }
        public RuleTime At { get; }
        public bool InInitiative { get; }
        public string EpochId { get; }
        public long LocalStart { get; }
        public RuleTime ExpiresAt { get; }
        public int RpBefore { get; }
        public int RpAfter => RpBefore - 2;
        public ConsecrationEnd End { get; }
        public long EndRevision { get; }
        public RuleTime EndAt { get; }
        public ConsecrationZone(string command, long revision, string owner, int x, int y, RuleTime at,
            bool initiative, string epoch, long localStart, RuleTime expiresAt, int rpBefore,
            ConsecrationEnd end = ConsecrationEnd.Active, long endRevision = 0, RuleTime endAt = default)
        {
            if (!Validation.ValidId(command) || revision < 1 || owner != ClericRpProfile.Actor
                || x < 0 || y < 0 || !Validation.ValidId(epoch) || localStart < 0 || expiresAt <= at
                || rpBefore < 2 || !Enum.IsDefined(typeof(ConsecrationEnd), end)
                || !initiative && expiresAt != at.AddSeconds(18)
                || end == ConsecrationEnd.Active && (endRevision != 0 || endAt != default)
                || end != ConsecrationEnd.Active && (endRevision <= revision || endAt < at)
                || end == ConsecrationEnd.Expiry && endAt != expiresAt
                || end == ConsecrationEnd.Replacement && endAt >= expiresAt)
                throw new ArgumentException("Invalid paid Consecration application.");
            CommandId = command; Revision = revision; OwnerId = owner; X = x; Y = y; At = at;
            InInitiative = initiative; EpochId = epoch; LocalStart = localStart; ExpiresAt = expiresAt;
            RpBefore = rpBefore; End = end; EndRevision = endRevision; EndAt = endAt;
        }
        public bool Present(RuleTime at) => at >= At && at < ExpiresAt
            && (End == ConsecrationEnd.Active || at < EndAt);
        public bool PresentAtRevision(RuleTime at, long revision) => revision > Revision && at >= At && at < ExpiresAt
            && (End == ConsecrationEnd.Active || at < EndAt || at == EndAt && revision < EndRevision);
        public ConsecrationZone Finish(ConsecrationEnd cause, long revision, RuleTime at)
        {
            if (End != ConsecrationEnd.Active || cause == ConsecrationEnd.Active)
                throw new InvalidOperationException("Only a live zone can end once.");
            return new ConsecrationZone(CommandId, Revision, OwnerId, X, Y, At, InInitiative,
                EpochId, LocalStart, ExpiresAt, RpBefore, cause, revision, at);
        }
    }

    /// <summary>The separately capped Ground rider, never part of the base Rite or a recursive trigger.</summary>
    public sealed class ConsecratedGroundHealing
    {
        public string RiteCommandId { get; }
        public string ZoneCommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public string OwnerId { get; }
        public string TargetId { get; }
        public RuleQuantity TargetX { get; }
        public RuleQuantity TargetY { get; }
        public long HpBefore { get; }
        public long Potential { get; }
        public long HpAfter { get; }
        public long ActualGain => HpAfter - HpBefore;
        public ConsecratedGroundHealing(string rite, string zone, long revision, RuleTime at, string owner,
            string target, RuleQuantity x, RuleQuantity y, long before, long potential, long after)
        {
            if (!Validation.ValidId(rite) || !Validation.ValidId(zone) || revision < 1
                || owner != ClericRpProfile.Actor || !Validation.ValidId(target) || before < 1
                || potential < 0 || potential > 1 || after < before || after - before > potential)
                throw new ArgumentException("Invalid Consecrated Ground healing.");
            RiteCommandId = rite; ZoneCommandId = zone; Revision = revision; At = at;
            OwnerId = owner; TargetId = target; TargetX = x; TargetY = y;
            HpBefore = before; Potential = potential; HpAfter = after;
        }
    }

    public sealed class ConsecrationAttackContribution
    {
        public string AttackId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public string AttackerId { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public bool Undead { get; }
        public string TypeSource => Undead ? FerryWraithProfile.SourceRevision : ConsecrationProfile.RosterSource;
        public string ZoneCommandId { get; }
        public string Disposition => !Undead ? "KnownNonUndead" : ZoneCommandId == "" ? "NoQualifyingZone" : "UndeadInsideZone";
        public int Contribution => ZoneCommandId == "" ? 0 : -1;
        public int TotalModifier { get; }
        public ConsecrationAttackContribution(string attack, long revision, RuleTime at, string actor,
            RuleQuantity x, RuleQuantity y, bool undead, string zone, int totalModifier)
        {
            if (!Validation.ValidId(attack) || revision < 1 || !Validation.ValidId(actor) || zone == null
                || zone != "" && (!undead || !Validation.ValidId(zone))
                || undead != (actor == FerryWraithProfile.Actor)
                || !undead && !ConsecrationProfile.HumanoidActors.Contains(actor))
                throw new ArgumentException("Invalid Consecration attack contribution.");
            AttackId=attack; Revision=revision; At=at; AttackerId=actor; X=x; Y=y;
            Undead=undead; ZoneCommandId=zone; TotalModifier=totalModifier;
        }
    }

    public sealed class ConsecrationRecord
    {
        public const int MaxZones = 128, MaxHealing = 128, MaxAttacks = 256;
        public string PredecessorFingerprint { get; }
        public string RosterSource => ConsecrationProfile.RosterSource;
        public IReadOnlyList<string> HumanoidActors { get; }
        public IReadOnlyList<ConsecrationZone> Zones { get; }
        public IReadOnlyList<ConsecratedGroundHealing> Healing { get; }
        public IReadOnlyList<ConsecrationAttackContribution> Attacks { get; }
        public ConsecrationRecord(string predecessor, IEnumerable<string> humanoidActors,
            IEnumerable<ConsecrationZone> zones = null, IEnumerable<ConsecratedGroundHealing> healing = null,
            IEnumerable<ConsecrationAttackContribution> attacks = null)
        {
            var actors = humanoidActors?.ToArray();
            var applications = (zones ?? Array.Empty<ConsecrationZone>()).ToArray();
            var gains = (healing ?? Array.Empty<ConsecratedGroundHealing>()).ToArray();
            var rolls = (attacks ?? Array.Empty<ConsecrationAttackContribution>()).ToArray();
            if (!ConsecrationProfile.IsPredecessor(predecessor) || actors == null
                || !actors.SequenceEqual(ConsecrationProfile.HumanoidActors)
                || applications.Length > MaxZones || gains.Length > MaxHealing || rolls.Length > MaxAttacks
                || applications.Any(x => x == null) || gains.Any(x => x == null)
                || rolls.Any(x => x == null) || rolls.Select(x => x.AttackId).Distinct().Count() != rolls.Length
                || applications.Select(x => x.CommandId).Distinct().Count() != applications.Length
                || gains.Select(x => x.RiteCommandId).Distinct().Count() != gains.Length
                || applications.Count(x => x.End == ConsecrationEnd.Active) > 1
                || applications.Skip(1).Where((x,i) => x.Revision <= applications[i].Revision).Any()
                || gains.Skip(1).Where((x,i) => x.Revision <= gains[i].Revision).Any())
                throw new ArgumentException("Invalid Consecration source or history.");
            PredecessorFingerprint = predecessor; HumanoidActors = Array.AsReadOnly(actors);
            Zones = Array.AsReadOnly(applications); Healing = Array.AsReadOnly(gains);
            Attacks = Array.AsReadOnly(rolls);
        }
        public ConsecrationRecord WithZones(IEnumerable<ConsecrationZone> zones)
            => new ConsecrationRecord(PredecessorFingerprint, HumanoidActors, zones, Healing, Attacks);
        public ConsecrationRecord WithHealing(IEnumerable<ConsecratedGroundHealing> healing)
            => new ConsecrationRecord(PredecessorFingerprint, HumanoidActors, Zones, healing, Attacks);
        public ConsecrationRecord WithAttacks(IEnumerable<ConsecrationAttackContribution> attacks)
            => new ConsecrationRecord(PredecessorFingerprint, HumanoidActors, Zones, Healing, attacks);
    }

    public static class ConsecrationProfile
    {
        public const string Consecrate = "cleric.base.consecrate", Ground = "cleric.base.consecrated-ground";
        public const string FingerprintPrefix = "TEST_ONLY.consecration-v1-";
        public const string Area = "TEST_ONLY.declared-geometry", RosterSource = "TEST_ONLY.consecration-roster.v1";
        public const byte Marker = 20;
        public static IReadOnlyList<string> HumanoidActors { get; } = Array.AsReadOnly(new[] {
            "TEST_ONLY.actor", "TEST_ONLY.companion", "TEST_ONLY.haven-copper-buyer",
            "TEST_ONLY.later-defender", "TEST_ONLY.recovery-defender", "TEST_ONLY.third-combatant" });
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
            || OrdinaryMagicProfile.SelectedFingerprint(value));
        public static bool IsPredecessor(string value) => value != null && value.StartsWith(FerryWraithProfile.FingerprintPrefix, StringComparison.Ordinal)
            && CreatureActorRecord.Hex(value.Substring(FerryWraithProfile.FingerprintPrefix.Length), 64);
        public static string BindFingerprint(string predecessor)
        {
            if (!IsPredecessor(predecessor)) throw new ArgumentException("Consecration requires its Ferry predecessor.");
            string binding = string.Join("|", predecessor, ClericRpProfile.SourceRevision, Consecrate, Ground,
                "CG-GEO-01|CG-GROUND-01|CG-TIME-01|CG-ORDER-01|CG-STACK-01|CG-CONTEXT-01",
                "action2RP|radius15-range30|original-third-start-or-18s|recharge3|base-ground-radiance-aura",
                RosterSource, string.Join(",", HumanoidActors), "complete-Humanoid|living-recipient|no-racial-mechanics");
            using (var hash = SHA256.Create()) return FingerprintPrefix + string.Concat(hash.ComputeHash(Encoding.UTF8.GetBytes(binding))
                .Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
        public static long AfterGround(Snapshot s, HealingRiteRecord rite)
        {
            if (rite == null) throw new ArgumentNullException(nameof(rite));
            var ground = s.Consecration?.Healing.SingleOrDefault(x => x.RiteCommandId == rite.CommandId);
            if (ground == null) return rite.HpAfter;
            var zone = s.Consecration.Zones.SingleOrDefault(x => x.CommandId == ground.ZoneCommandId);
            if (!s.HealingRites.Contains(rite) || rite.ActualGain <= 0 || ground.Revision != rite.Revision
                || ground.At != rite.At || ground.OwnerId != rite.ActorId || ground.TargetId != rite.TargetId
                || ground.HpBefore != rite.HpAfter || zone == null || zone.OwnerId != rite.ActorId
                || !zone.PresentAtRevision(rite.At,rite.Revision)
                || !s.Consecration.HumanoidActors.Contains(rite.TargetId)
                || !s.CharacterFeatureGrants.Any(x => x.ActorId == rite.ActorId && x.FeatureId == Ground
                    && ClericRpProfile.ValidInitialGrant(s,x)))
                throw new ArgumentException("Unqualified intermediate Ground predecessor.");
            var dx = ground.TargetX >= new RuleQuantity(zone.X) ? ground.TargetX-new RuleQuantity(zone.X) : new RuleQuantity(zone.X)-ground.TargetX;
            var dy = ground.TargetY >= new RuleQuantity(zone.Y) ? ground.TargetY-new RuleQuantity(zone.Y) : new RuleQuantity(zone.Y)-ground.TargetY;
            if (dx > new RuleQuantity(3) || dy > new RuleQuantity(3)) throw new ArgumentException("Ground predecessor is outside its fixed terrain.");
            return ground.HpAfter;
        }

        internal static void Validate(Snapshot s)
        {
            if ((s.Consecration != null) != SelectedFingerprint(s.ContentFingerprint))
                throw new ArgumentException("Consecration envelope mismatch.");
            if (s.Consecration == null) {
                if (s.RadianceUses.Any(x => x.PreRadianceHp() != x.BaseHpAfter))
                    throw new ArgumentException("Intermediate Rite healing requires its explicit profile.");
                return;
            }
            var record = s.Consecration;
            if (!s.TestOnly || s.FerryWraith == null || (s.OrdinaryMagic?.PredecessorFingerprint ?? s.ContentFingerprint) != BindFingerprint(record.PredecessorFingerprint)
                || record.PredecessorFingerprint != FerryWraithProfile.BindFingerprint(s.FerryWraith.PredecessorFingerprint,
                    s.FerryWraith.CompanionConsents, s.FerryWraith.DirectorAuthorizes)
                || !s.Actors.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal).SequenceEqual(
                    HumanoidActors.Append(FerryWraithProfile.Actor).OrderBy(x => x, StringComparer.Ordinal)))
                throw new ArgumentException("Unqualified Consecration genesis.");
            foreach (var zone in record.Zones) {
                var receipt = s.Receipts.SingleOrDefault(x => x.Revision == zone.Revision);
                var command = receipt == null ? null : CommandHistory.Read(receipt);
                var epoch = WorldTiming.FindEpoch(s, zone.EpochId);
                if (command?.Kind != CommandKind.UseConsecrate || command.Id != zone.CommandId || command.Actor != zone.OwnerId
                    || command.GetConsecrateRequest() == null || command.GetConsecrateRequest().X != zone.X || command.GetConsecrateRequest().Y != zone.Y
                    || zone.Revision > s.Revision || zone.At > s.RuleClock || epoch == null
                    || !DeclaredGeometryProfile.SupportsAnchorAt(s,zone.X,zone.Y)
                    || !s.CharacterFeatureGrants.Any(x=>x.ActorId==zone.OwnerId && x.FeatureId==Consecrate
                        && ClericRpProfile.ValidInitialGrant(s,x))
                    || epoch.LatestStart(zone.OwnerId, zone.LocalStart) != zone.LocalStart || epoch.Start(zone.LocalStart) > zone.At
                    || (s.OrdinaryMagic==null ? zone.At >= epoch.Start(checked(zone.LocalStart+1))
                        : !OrdinaryMagicProfile.ValidActivityContext(s,zone.CommandId,zone.EpochId,zone.LocalStart,
                            WorldTiming.TurnOrdinal(s,zone.EpochId,zone.LocalStart),zone.At)
                            || OrdinaryMagicProfile.Activity(s,zone.CommandId).InInitiative!=zone.InInitiative)
                    || zone.RpBefore != ClericLongRestProfile.RpBefore(s,zone.Revision)
                    || zone.InInitiative && zone.ExpiresAt != epoch.Start(checked(zone.LocalStart + 3L * epoch.Order.Count))
                    || zone.End == ConsecrationEnd.Active && zone.ExpiresAt <= s.RuleClock
                    || zone.End != ConsecrationEnd.Active && (zone.EndRevision > s.Revision || zone.EndAt > s.RuleClock)
                    || zone.End == ConsecrationEnd.Replacement && !record.Zones.Any(x => x.OwnerId == zone.OwnerId
                        && x.Revision == zone.EndRevision && x.At == zone.EndAt))
                    throw new ArgumentException("Unqualified Consecration use or endpoint.");
            }
            if(s.Receipts.Count(x=>CommandHistory.Read(x).Kind==CommandKind.UseConsecrate)!=record.Zones.Count)
                throw new ArgumentException("Missing paid Consecration application history.");
            foreach (var ground in record.Healing) {
                var rite = s.HealingRites.SingleOrDefault(x => x.CommandId == ground.RiteCommandId);
                var zone = record.Zones.SingleOrDefault(x => x.CommandId == ground.ZoneCommandId);
                if (rite == null || zone == null || rite.ActualGain <= 0 || rite.Revision != ground.Revision
                    || rite.At != ground.At || rite.ActorId != ground.OwnerId || rite.TargetId != ground.TargetId
                    || rite.HpAfter != ground.HpBefore || zone.OwnerId != ground.OwnerId || !zone.PresentAtRevision(ground.At,ground.Revision)
                    || !HumanoidActors.Contains(ground.TargetId))
                    throw new ArgumentException("Unqualified Ground healing predecessor.");
                if(AfterGround(s,rite)!=ground.HpAfter)
                    throw new ArgumentException("Ground result is not its qualified historical predecessor.");
            }
            var attacks=s.MeleeAttacks.Select(x => (x.Id,x.Revision,x.At,x.AttackerId,x.Attack))
                .Concat(s.RangedAttacks.Select(x => (x.Id,x.Revision,x.At,x.AttackerId,x.Attack))).ToArray();
            if(record.Attacks.Count!=attacks.Length) throw new ArgumentException("Missing Consecration attack disposition.");
            foreach(var audit in record.Attacks) {
                var matches=attacks.Where(x => x.Id==audit.AttackId).ToArray();
                if(matches.Length!=1 || matches[0].Revision!=audit.Revision || matches[0].At!=audit.At
                    || matches[0].AttackerId!=audit.AttackerId || matches[0].Attack.Modifier!=audit.TotalModifier)
                    throw new ArgumentException("Unbound Consecration attack disposition.");
                if(audit.ZoneCommandId!="") {
                    var zone=record.Zones.SingleOrDefault(x => x.CommandId==audit.ZoneCommandId);
                    if(zone==null || !zone.PresentAtRevision(audit.At,audit.Revision))
                        throw new ArgumentException("Unqualified Consecration attack zone.");
                    var dx=audit.X>=new RuleQuantity(zone.X)?audit.X-new RuleQuantity(zone.X):new RuleQuantity(zone.X)-audit.X;
                    var dy=audit.Y>=new RuleQuantity(zone.Y)?audit.Y-new RuleQuantity(zone.Y):new RuleQuantity(zone.Y)-audit.Y;
                    if(dx>new RuleQuantity(3) || dy>new RuleQuantity(3))
                        throw new ArgumentException("Consecration attack is outside its fixed zone.");
                }
            }
            var recharge = s.AbilityRecharges.Where(x => x.AbilityId == Consecrate).ToArray();
            if (recharge.Length != (record.Zones.Count == 0 ? 0 : 1)
                || recharge.Any(x => x.ActorId != ClericRpProfile.Actor))
                throw new ArgumentException("Missing Consecrate recharge provenance.");
            if (recharge.Length != 0) ValidateRecharge(s,record.Zones.Last(),recharge[0]);
            // Exact payment and historical sensory/position facts are independently replayed.
        }
        private static void ValidateRecharge(Snapshot s, ConsecrationZone last, CharacterAbilityRechargeRecord recharge)
        {
            if(s.OrdinaryMagic!=null) { OrdinaryMagicProfile.ValidateRecharge(s,last.CommandId,recharge); return; }
            var epochs = new[] { s.Reinforcement?.Admission?.Phase.Epoch, s.PostRecoveryEncounter?.Admission?.Epoch,
                s.FerryWraith?.Admission?.Epoch }.Where(x => x != null).ToArray();
            int first = Array.FindIndex(epochs,x => x.Id == last.EpochId);
            if (first < 0) throw new ArgumentException("Consecrate recharge has no source schedule.");
            long ticks = 0, cursor = last.LocalStart;
            var current = epochs[first];
            for (int i=first; i<epochs.Length; i++) {
                var epoch = epochs[i];
                RuleTime until = i+1 < epochs.Length ? epochs[i+1].Origin : s.RuleClock;
                long latest = epoch.LatestStart(last.OwnerId,epoch.SlotAt(until));
                // The new schedule owns the boundary itself. Historical schedules continue virtual
                // duration markers, but those must never recharge the transferred ability.
                if (i+1 < epochs.Length && latest >= 0 && epoch.Start(latest) == until) latest -= epoch.Order.Count;
                if(IsSkippedRechargeStart(s,epoch,last.OwnerId,latest))latest-=epoch.Order.Count;
                long after=i==first?last.LocalStart:-1;
                long count=CountRechargeStarts(s,epoch,last.OwnerId,after,latest);
                if(count==0)continue;
                ticks = checked(ticks + count);
                current = epoch; cursor = latest;
            }
            if (recharge.EpochId != current.Id || recharge.LastLocalStart != cursor
                || recharge.LastStartAt != current.Start(cursor) || recharge.LastStartAt > s.RuleClock
                || recharge.Remaining != Math.Max(0L,3L-ticks))
                throw new ArgumentException("Invalid Consecrate source recharge cursor.");
        }
        public static long CountRechargeStarts(Snapshot s,WorldScheduleRecord epoch,string actor,long after,long through)
        {
            int owner=epoch.Order.ToList().IndexOf(actor);
            if(owner<0)throw new ArgumentException("Consecrate recharge actor is outside its source schedule.");
            if(through<owner || through<=after)return 0;
            long first=after<owner?owner:checked(after+epoch.Order.Count-(after-owner)%epoch.Order.Count);
            long last=epoch.LatestStart(actor,through);
            if(last<first)return 0;
            long count=(last-first)/epoch.Order.Count+1;
            var phase=s.Reinforcement?.Admission?.Phase;var exit=s.Retreat?.SuccessfulExit;
            if(phase!=null && exit!=null && epoch.Id==phase.Epoch.Id) {
                long skipped=exit.EndTurn+1L-phase.FirstTurn;
                if(skipped>=first && skipped<=last && IsSkippedRechargeStart(s,epoch,actor,skipped))count--;
            }
            return count;
        }
        private static bool IsSkippedRechargeStart(Snapshot s,WorldScheduleRecord epoch,string actor,long local)
        {
            var phase=s.Reinforcement?.Admission?.Phase;var exit=s.Retreat?.SuccessfulExit;
            return local>=0 && phase!=null && exit!=null && epoch.Id==phase.Epoch.Id
                && phase.GlobalTurn(local)==exit.EndTurn+1 && epoch.LatestStart(actor,local)==local;
        }
    }
}
