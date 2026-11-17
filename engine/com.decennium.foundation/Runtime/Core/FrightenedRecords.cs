using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Chosen targets only. The host derives source, DC, relationship, timing,
    /// perception, saves, Action payment and recharge from actual shared state.</summary>
    public sealed class IntimidatingPresenceRequest
    {
        public ReadOnlyCollection<string> TargetIds { get; }
        internal string Fingerprint => string.Join(",", TargetIds);
        public IntimidatingPresenceRequest(IEnumerable<string> targetIds)
        {
            if (targetIds == null) throw new ArgumentNullException(nameof(targetIds));
            var ids = targetIds.Take(4).ToArray();
            if (ids.Length < 1 || ids.Length > 3 || ids.Any(x => !Validation.ValidId(x))
                || ids.Distinct(StringComparer.Ordinal).Count() != ids.Length)
                throw new ArgumentException("Intimidating Presence requires one to three distinct target identities.");
            TargetIds = Array.AsReadOnly(ids.OrderBy(x => x, StringComparer.Ordinal).ToArray());
        }
    }

    /// <summary>Shared named-ability recharge cursor. This record supplies neither feature
    /// ownership nor a reset producer; the source validates its maximum and actual cadence.</summary>
    public sealed class CharacterAbilityRechargeRecord
    {
        public string ActorId { get; }
        public string AbilityId { get; }
        public string EpochId { get; }
        public long LastLocalStart { get; }
        public RuleTime LastStartAt { get; }
        public int Remaining { get; }
        public CharacterAbilityRechargeRecord(string actor, string ability, string epoch, long lastLocalStart,
            RuleTime lastStartAt, int remaining)
        {
            if (!Validation.ValidId(actor) || !Validation.ValidId(ability) || !Validation.ValidId(epoch)
                || lastLocalStart < 0 || remaining < 0) throw new ArgumentException("Invalid named ability recharge cursor.");
            ActorId = actor; AbilityId = ability; EpochId = epoch; LastLocalStart = lastLocalStart;
            LastStartAt = lastStartAt; Remaining = remaining;
        }
    }

    /// <summary>Initial source-qualified Warrior ability choice. Feature ownership remains
    /// in CharacterFeatureGrants; this record does not grant a build or advancement.</summary>
    public sealed class WarriorAbilityChoiceRecord
    {
        public string ActorId { get; }
        public CharacterAbility Ability { get; }
        public string SourceRevision { get; }
        public string EntitlementId { get; }
        public long AcquiredRevision { get; }
        public WarriorAbilityChoiceRecord(string actor, CharacterAbility ability, string sourceRevision,
            string entitlementId, long acquiredRevision)
        {
            foreach (string value in new[] { actor, sourceRevision, entitlementId }) ConditionJournal.RequireId(value);
            if (ability != CharacterAbility.Strength && ability != CharacterAbility.Dexterity || acquiredRevision < 0)
                throw new ArgumentException("Invalid Warrior ability choice.");
            ActorId = actor; Ability = ability; SourceRevision = sourceRevision;
            EntitlementId = entitlementId; AcquiredRevision = acquiredRevision;
        }
    }

    public sealed class FrightenedUseRecord
    {
        public string Id { get; }
        public string CommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string SourceId { get; }
        public string SourceRevision { get; }
        public string EpochId { get; }
        public long LocalStart { get; }
        public RuleTime At { get; }
        public int Dc { get; }
        public ReadOnlyCollection<string> TargetIds { get; }
        public FrightenedUseRecord(string id, string commandId, long revision, string actor, string source,
            string sourceRevision, string epoch, long localStart, RuleTime at, int dc, IEnumerable<string> targets)
        {
            foreach (string value in new[] { id, commandId, actor, source, sourceRevision, epoch }) ConditionJournal.RequireId(value);
            if (revision < 1 || localStart < 0 || dc < 0) throw new ArgumentException("Invalid fear activation provenance.");
            var choice = new IntimidatingPresenceRequest(targets);
            Id = id; CommandId = commandId; Revision = revision; ActorId = actor; SourceId = source;
            SourceRevision = sourceRevision; EpochId = epoch; LocalStart = localStart; At = at; Dc = dc;
            TargetIds = choice.TargetIds;
        }
    }

    /// <summary>Actual save evidence in the shared RNG stream. Presence and suppression
    /// remain exclusively in the shared condition journal, not in this audit record.</summary>
    public sealed class FrightenedSaveRecord
    {
        public string Id { get; }
        public string UseId { get; }
        public string TargetId { get; }
        public string ApplicationId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public bool Repeat { get; }
        public int Dc { get; }
        public int Modifier { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public bool Success { get; }
        public bool AdmissionPrevented { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public FrightenedSaveRecord(string id, string useId, string target, string application, long revision,
            RuleTime at, bool repeat, int dc, int modifier, int first, int second, int natural,
            bool success, bool admissionPrevented, uint randomBefore, uint randomAfter, long wordsConsumed)
        {
            foreach (string value in new[] { id, useId, target }) ConditionJournal.RequireId(value);
            if (application == null || application != "" && !Validation.ValidId(application) || revision < 1 || dc < 0
                || first < 1 || first > 20 || second < 0 || second > 20 || natural < 1 || natural > 20
                || wordsConsumed < 1 || repeat && (application == "" || admissionPrevented)
                || success && admissionPrevented || !repeat && (application != "") != (!success && !admissionPrevented))
                throw new ArgumentException("Invalid fear saving-throw record.");
            Id = id; UseId = useId; TargetId = target; ApplicationId = application; Revision = revision;
            At = at; Repeat = repeat; Dc = dc; Modifier = modifier; First = first; Second = second; Natural = natural;
            Success = success; AdmissionPrevented = admissionPrevented; RandomBefore = randomBefore;
            RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
    }

    /// <summary>Captured source endpoints for one actual application. A future repeat
    /// only resolves while the journal still contains that present application.</summary>
    public sealed class FrightenedTimingRecord
    {
        public string ApplicationId { get; }
        public string UseId { get; }
        public string TargetId { get; }
        public string EpochId { get; }
        public long TargetLocalEnd { get; }
        public ConditionStamp RepeatAt { get; }
        public ConditionStamp FinalAt { get; }
        public FrightenedTimingRecord(string application, string use, string target, string epoch,
            long targetLocalEnd, ConditionStamp repeatAt, ConditionStamp finalAt)
        {
            foreach (string value in new[] { application, use, target, epoch }) ConditionJournal.RequireId(value);
            if (targetLocalEnd < 0 || finalAt.CompareTo(repeatAt) <= 0)
                throw new ArgumentException("Invalid fear source endpoints.");
            ApplicationId = application; UseId = use; TargetId = target; EpochId = epoch;
            TargetLocalEnd = targetLocalEnd; RepeatAt = repeatAt; FinalAt = finalAt;
        }
    }

    public static class FrightenedProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.frightened-v1-";
        public const byte Marker = 12;
        public const string Actor = "TEST_ONLY.later-defender";
        public const string SourceId = "warrior.base.intimidating-presence";
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string CardSha256 = "33598398ee903d4696f3acad393828496b567b6df69ae6c28873346a7b571c73";
        public const string WarriorEngineSha256 = "2fe08c7c9a299c3943c0bec763ab9691821d89c0a35af4bb77b75f05cba77a71";
        public const string ConditionSha256 = "246e82c831c231581742bc3b04b50065697f6a9039d0afcd3ef7d6a244d055d9";
        public const string Entitlement = "TEST_ONLY.frightened.initial-defender";
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal) || ClericSettlementProfile.SelectedFingerprint(value));
        public static bool ValidFixtureGrant(Snapshot state, CharacterFeatureGrantRecord grant)
            => state.ConnectedFrightened && (grant.ActorId == Actor || state.PostRecoveryEncounter != null
                && grant.ActorId == PostRecoveryEncounterDefinition.Actor) && grant.FeatureId == SourceId
                && grant.ClassName == "Warrior" && grant.ClassLevel == 2 && grant.MilestoneId == ""
                && grant.GrantedRevision == 0 && grant.Origin == CharacterFeatureGrantOrigin.TestOnlyFixtureEntitlement;

        internal static void Validate(Snapshot state)
        {
            bool selected = SelectedFingerprint(state.ContentFingerprint);
            if (state.ConnectedFrightened != selected || state.WarriorAbilityChoices == null || state.AbilityRecharges == null
                || state.FrightenedUses == null || state.FrightenedSaves == null || state.FrightenedTimings == null
                || state.WarriorAbilityChoices.Any(x => x == null) || state.AbilityRecharges.Any(x => x == null)
                || state.FrightenedUses.Any(x => x == null) || state.FrightenedSaves.Any(x => x == null) || state.FrightenedTimings.Any(x => x == null))
                throw new ArgumentException("Invalid Frightened envelope.");
            if (!selected) {
                if (state.WarriorAbilityChoices.Length + state.AbilityRecharges.Length + state.FrightenedUses.Length
                    + state.FrightenedSaves.Length + state.FrightenedTimings.Length != 0
                    || state.Conditions.Any(x => x.PolicyId == ConditionJournal.RelationshipPolicyId))
                    throw new ArgumentException("Frightened source state requires its explicit profile.");
                return;
            }
            var owners = state.PostRecoveryEncounter == null ? new[] { Actor }
                : new[] { Actor, PostRecoveryEncounterDefinition.Actor };
            bool choicesValid=state.WarriorAbilityChoices.Length==owners.Length
                && owners.All(owner=>state.WarriorAbilityChoices.Count(x=>x.ActorId==owner
                    && x.Ability==CharacterAbility.Strength && x.SourceRevision==SourceRevision && x.AcquiredRevision==0
                    && x.EntitlementId==(owner==Actor?Entitlement:PostRecoveryEncounterDefinition.Entitlement))==1);
            var choice = state.WarriorAbilityChoices.SingleOrDefault(x=>x.ActorId==Actor);
            if (!state.TestOnly || !state.ConnectedClericRepertoire || !state.ConnectedClericRp
                || state.SchemaVersion != Snapshot.SurpriseEntrySchema || !choicesValid || choice == null || choice.ActorId != Actor
                || choice.Ability != CharacterAbility.Strength || choice.SourceRevision != SourceRevision
                || choice.EntitlementId != Entitlement || choice.AcquiredRevision != 0
                || owners.Any(owner=>state.CharacterFeatureGrants.Count(x => x.ActorId==owner && ValidFixtureGrant(state, x)) != 1)
                || state.Characters.Single(x => x.ActorId == Actor).Levels.Count(x => x.ClassName == "Warrior") != 3
                || state.Conditions.Any(x => x.PolicyId != ConditionJournal.RelationshipPolicyId)
                || state.AbilityRecharges.Count(x=>x.AbilityId==SourceId) > owners.Length
                || state.AbilityRecharges.Any(x=>x.AbilityId!=SourceId&&(state.BishopEntry==null||x.AbilityId!=BishopProfile.Invocation)
                    &&(state.Consecration==null||x.AbilityId!=ConsecrationProfile.Consecrate)) || state.FrightenedUses.Length > 128
                || state.FrightenedSaves.Length > 768 || state.FrightenedTimings.Length > 384)
                throw new ArgumentException("Invalid bounded Frightened access or history.");
            if (state.FrightenedUses.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != state.FrightenedUses.Length
                || state.FrightenedSaves.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != state.FrightenedSaves.Length
                || state.FrightenedTimings.Select(x => x.ApplicationId).Distinct(StringComparer.Ordinal).Count() != state.FrightenedTimings.Length
                || state.FrightenedSaves.Select(x => x.UseId + "|" + x.TargetId + "|" + x.Repeat).Distinct(StringComparer.Ordinal).Count() != state.FrightenedSaves.Length)
                throw new ArgumentException("Duplicate Frightened history identity.");
            if (state.AbilityRecharges.Count(x=>x.AbilityId==SourceId) != state.FrightenedUses.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()
                || state.AbilityRecharges.Select(x=>x.ActorId+"|"+x.AbilityId).Distinct(StringComparer.Ordinal).Count()!=state.AbilityRecharges.Length
                || !state.FrightenedUses.Select(x => x.Revision).SequenceEqual(state.FrightenedUses.Select(x => x.Revision).OrderBy(x => x)))
                throw new ArgumentException("Missing recharge or unordered Frightened uses.");
            var lastUses = new System.Collections.Generic.Dictionary<string,FrightenedUseRecord>(StringComparer.Ordinal);
            foreach (var use in state.FrightenedUses) {
                lastUses.TryGetValue(use.ActorId,out var previousUse);
                var receipt = state.Receipts.SingleOrDefault(x => x.Revision == use.Revision);
                var command = receipt == null ? null : CommandHistory.Read(receipt);
                var epoch = WorldTiming.FindEpoch(state, use.EpochId);
                if (!owners.Contains(use.ActorId) || use.SourceId != SourceId || use.SourceRevision != SourceRevision || use.Dc != 10
                    || use.Id != "fear.use." + use.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)
                    || use.At > state.RuleClock || command?.Kind != CommandKind.UseIntimidatingPresence
                    || command.Actor != use.ActorId || command.Id != use.CommandId
                    || !command.IntimidatingPresence.TargetIds.SequenceEqual(use.TargetIds)
                    || epoch == null || !epoch.Order.Contains(use.ActorId) || epoch.LatestStart(use.ActorId, use.LocalStart) != use.LocalStart
                    || epoch.Id != (use.ActorId==Actor?state.Reinforcement?.Admission?.Phase.Epoch.Id:state.PostRecoveryEncounter?.Admission?.Epoch.Id)
                    || epoch.Start(use.LocalStart) > use.At || epoch.Start(use.LocalStart + 1) <= use.At
                    || !state.FrightenedSaves.Where(x => x.UseId == use.Id && !x.Repeat).Select(x => x.TargetId).SequenceEqual(use.TargetIds)
                    || previousUse != null && (previousUse.EpochId != use.EpochId
                        || use.LocalStart - previousUse.LocalStart < 3L * epoch.Order.Count))
                    throw new ArgumentException("Invalid paid Frightened use provenance.");
                var initial = state.FrightenedSaves.Where(x => x.UseId == use.Id && !x.Repeat).ToArray();
                for (int i = 1; i < initial.Length; i++) if (initial[i].RandomBefore != initial[i - 1].RandomAfter)
                    throw new ArgumentException("Noncontiguous initial fear saves.");
                lastUses[use.ActorId] = use;
            }
            foreach (var save in state.FrightenedSaves) {
                var use = state.FrightenedUses.SingleOrDefault(x => x.Id == save.UseId);
                var draw = DiceStream.Draw(save.RandomBefore, 20);
                if (use == null || !use.TargetIds.Contains(save.TargetId) || save.Dc != use.Dc || save.Revision > state.Revision
                    || save.Id != save.UseId + ".save." + save.TargetId + (save.Repeat ? ".repeat" : ".initial")
                    || save.First != draw.Value + 1 || save.Natural != save.First || save.Second != 0
                    || save.RandomAfter != draw.NextState || save.WordsConsumed != draw.WordsConsumed
                    || save.At < use.At || save.At > state.RuleClock || !save.Repeat && (save.Revision != use.Revision || save.At != use.At)
                    || save.Success != ((long)save.Natural + save.Modifier >= save.Dc)
                    || save.ApplicationId != "" && save.ApplicationId != save.UseId + "." + save.TargetId
                    || !save.Repeat && save.ApplicationId != "" && !state.FrightenedTimings.Any(x => x.ApplicationId == save.ApplicationId)
                    || save.Repeat && !state.FrightenedTimings.Any(x => x.ApplicationId == save.ApplicationId
                        && x.UseId == save.UseId && x.TargetId == save.TargetId && x.RepeatAt.Time == save.At))
                    throw new ArgumentException("Invalid Frightened save provenance.");
            }
            foreach (var timing in state.FrightenedTimings) {
                var use = state.FrightenedUses.SingleOrDefault(x => x.Id == timing.UseId);
                var epoch = WorldTiming.FindEpoch(state, timing.EpochId);
                var operation = state.Conditions.Single(x => x.Target == timing.TargetId).Operations
                    .SingleOrDefault(x => x.Kind == ConditionOperationKind.Apply && x.Application.Id == timing.ApplicationId);
                var a = operation?.Application;
                if (use == null || epoch == null || !epoch.Order.Contains(timing.TargetId)
                    || timing.EpochId != use.EpochId
                    || epoch.LatestStart(timing.TargetId, timing.TargetLocalEnd) != timing.TargetLocalEnd
                    || timing.TargetLocalEnd != NextTargetEnd(epoch, timing.TargetId, use.At)
                    || epoch.Start(timing.TargetLocalEnd + 1) != timing.RepeatAt.Time || timing.RepeatAt.Time <= use.At
                    || timing.RepeatAt.Phase != 0 || timing.FinalAt.Phase != 0
                    || !SixSecondsAfter(timing.FinalAt.Time, timing.RepeatAt.Time)
                    || a == null || a.Kind != "Frightened" || a.Owner != use.ActorId || a.Source != SourceId
                    || a.ApplyingDc != use.Dc || !a.Expires.HasValue || !a.Expires.Value.Equals(timing.FinalAt)
                    || !a.GenericCureAllowed || operation.At.Time != use.At || operation.At.Phase != 0 || a.Fear?.FearedEntityId != use.ActorId
                    || a.Fear.SourceUseId != use.Id || a.Fear.SourceRevision != SourceRevision
                    || !state.FrightenedSaves.Any(x => !x.Repeat && x.UseId == use.Id && x.TargetId == timing.TargetId
                        && x.ApplicationId == timing.ApplicationId && !x.Success && !x.AdmissionPrevented))
                    throw new ArgumentException("Invalid Frightened application endpoint or relationship.");
                if (state.RuleClock >= timing.RepeatAt.Time
                    && !state.FrightenedSaves.Any(x => x.Repeat && x.ApplicationId == timing.ApplicationId)
                    && !ClericSettlementProfile.CuredBeforeRepeat(state,timing))
                    throw new ArgumentException("Missing due Frightened repeat save.");
                if (state.RuleClock >= timing.FinalAt.Time
                    && !state.FrightenedSaves.Any(x => x.Repeat && x.ApplicationId == timing.ApplicationId && x.Success)
                    && state.Conditions.Single(x => x.Target == timing.TargetId).Now.Time < timing.FinalAt.Time
                    && !ClericSettlementProfile.CuredBeforeFinal(state,timing))
                    throw new ArgumentException("Missing due Frightened final ending.");
            }
            foreach (var journal in state.Conditions) {
                foreach (var operation in journal.Operations.Where(x => x.Kind == ConditionOperationKind.Apply && x.Application.Kind == "Frightened"))
                    if (!state.FrightenedTimings.Any(x => x.ApplicationId == operation.Application.Id && x.TargetId == journal.Target))
                        throw new ArgumentException("Unqualified Frightened application.");
                foreach (var operation in journal.Operations.Where(x => x.Kind == ConditionOperationKind.EndApplication
                    && state.FrightenedTimings.Any(t => t.ApplicationId == x.Subject && t.TargetId == journal.Target)))
                    if (!state.FrightenedSaves.Any(x => x.Repeat && x.Success && x.ApplicationId == operation.Subject
                        && x.TargetId == journal.Target && x.At == operation.At.Time && operation.Id == x.Id + ".end"
                        && operation.Reason == "source-repeat-success"))
                        throw new ArgumentException("Unqualified Frightened source ending.");
                // Old envelopes retain TAC-05's no-producer boundary. Wire108 must justify the actual paid Radiance cause.
                if (journal.Operations.Any(x => x.Kind == ConditionOperationKind.Cure && x.Subject == "Frightened"
                    && !ClericSettlementProfile.QualifiesCure(state,journal.Target,x)))
                    throw new ArgumentException("Frightened cure has no admitted gameplay producer.");
            }
            foreach (var recharge in state.AbilityRecharges.Where(x=>x.AbilityId==SourceId)) {
                lastUses.TryGetValue(recharge.ActorId,out var previousUse);
                var epoch = WorldTiming.FindEpoch(state, recharge.EpochId);
                if (!owners.Contains(recharge.ActorId) || recharge.AbilityId != SourceId || recharge.Remaining > 3 || epoch == null
                    || epoch.LatestStart(recharge.ActorId, recharge.LastLocalStart) != recharge.LastLocalStart
                    || epoch.Start(recharge.LastLocalStart) != recharge.LastStartAt || recharge.LastStartAt > state.RuleClock
                    || previousUse == null || previousUse.EpochId != recharge.EpochId || recharge.LastLocalStart < previousUse.LocalStart
                    || recharge.Remaining != Math.Max(0L, 3L - (recharge.LastLocalStart - previousUse.LocalStart) / epoch.Order.Count))
                    throw new ArgumentException("Invalid Frightened recharge cursor.");
            }
        }
        public static long NextTargetEnd(WorldScheduleRecord epoch, string target, RuleTime at)
        {
            long local = epoch.LatestStart(target, epoch.SlotAt(at));
            if (local < 0) local = Array.IndexOf(epoch.Order.ToArray(), target);
            if (epoch.Start(local + 1) <= at) local = checked(local + epoch.Order.Count);
            return local;
        }
        private static bool SixSecondsAfter(RuleTime later, RuleTime earlier)
            => (System.Numerics.BigInteger)later.Numerator * earlier.Denominator
                == ((System.Numerics.BigInteger)earlier.Numerator + 6 * (System.Numerics.BigInteger)earlier.Denominator) * later.Denominator;
    }
}
