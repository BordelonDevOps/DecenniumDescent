using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>One explicitly authored TEST_ONLY world declaration. Entry never creates its actor.</summary>
    public sealed class PostRecoveryEncounterDefinition
    {
        public const string Actor = "TEST_ONLY.recovery-defender";
        public const string Club = "TEST_ONLY.recovery-defender-club";
        public const string Encounter = "TEST_ONLY.post-recovery-conflict";
        public const string Calendar = "TEST_ONLY.post-recovery-calendar";
        public const string Hero = "TEST_ONLY.actor";
        public const string Companion = "TEST_ONLY.companion";
        public const string PriorDefender = "TEST_ONLY.later-defender";
        public const string Controller = "TEST_ONLY.post-recovery-defender.v1";
        public const string Entitlement = "TEST_ONLY.post-recovery.initial-defender.v1";
        public const string Engagement = "TEST_ONLY.post-recovery.completed-approach.v1";
        public const string PlayerTie = "TEST_ONLY.post-recovery.hero-before-companion.v1";
        public const string DirectorTie = "TEST_ONLY.post-recovery.npc-first.v1";
        public const string Consent = "TEST_ONLY.post-recovery.companion-consent.v1";
        public const string Hold = "TEST_ONLY.post-recovery.defender-hold.v1";
        public bool CompanionConsents { get; }
        public bool DirectorAuthorizes { get; }
        public int DefenderX => 4;
        public int DefenderY => 4;
        public int FromX => 3;
        public int FromY => 2;
        public int ArrivalX => 3;
        public int ArrivalY => 3;
        public int CompanionX => 3;
        public int CompanionY => 4;

        public PostRecoveryEncounterDefinition(bool companionConsents = true, bool directorAuthorizes = true)
        { CompanionConsents = companionConsents; DirectorAuthorizes = directorAuthorizes; }

        public string Binding => string.Join("|", Actor, Club, Encounter, Calendar, Hero, Companion, PriorDefender,
            Controller, Entitlement, Engagement, PlayerTie, DirectorTie, CompanionConsents ? Consent : "",
            DirectorAuthorizes ? Hold : "", "26/26hp|10abilities|Warrior12,7,7|30speed|4,4|3,2-to-3,3|companion3,4");

        public bool Matches(WorldTraversalRecord edge) => edge != null && edge.ActorId == Hero && !edge.Running
            && edge.FromX == FromX && edge.FromY == FromY && edge.ToX == ArrivalX && edge.ToY == ArrivalY;

        public static bool IsParticipant(string actor) => actor == Hero || actor == Companion || actor == Actor;
        public static bool IsParty(string actor) => actor == Hero || actor == Companion;
        public static int TieOrder(string actor) => actor == Actor ? 0 : actor == Hero ? 1 : 2;
    }

    /// <summary>Actual completed travel, including a failed contact. Failure retains elapsed work and movement.</summary>
    public sealed class PostRecoveryContact
    {
        public long ApproachRevision { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public RuleTime RequestedUntil { get; }
        public string Failure { get; }
        public PostRecoveryContact(long approachRevision, long revision, string commandId, RuleTime at,
            RuleTime requestedUntil, string failure)
        {
            if (approachRevision < 1 || revision <= approachRevision || !Validation.ValidId(commandId)
                || requestedUntil < at || failure == null || failure != "" && !Validation.ValidId(failure))
                throw new ArgumentException("Invalid post-recovery contact.");
            ApproachRevision = approachRevision; Revision = revision; CommandId = commandId;
            At = at; RequestedUntil = requestedUntil; Failure = failure;
        }
    }

    /// <summary>Immutable admission evidence. Only the existing current interval ledgers are spendable.</summary>
    public sealed class PostRecoveryAdmission
    {
        public WorldScheduleRecord Epoch { get; }
        public string PreviousPartyEpochId { get; }
        public long PriorDefenderLocalStart { get; }
        public IReadOnlyList<LaterInitiativeDraw> Draws { get; }
        public IReadOnlyList<ReinforcementCarry> PartyCarried { get; }
        public WorldActivityIntervalRecord DefenderActivity { get; }
        public IReadOnlyList<string> InitialReactionActors { get; }

        public PostRecoveryAdmission(WorldScheduleRecord epoch, string previousPartyEpochId, long priorDefenderLocalStart,
            IEnumerable<LaterInitiativeDraw> draws, IEnumerable<ReinforcementCarry> partyCarried,
            WorldActivityIntervalRecord defenderActivity, IEnumerable<string> initialReactionActors)
        {
            var rolls = draws?.ToArray(); var carried = partyCarried?.ToArray(); var reactions = initialReactionActors?.ToArray();
            if (epoch == null || epoch.Id != PostRecoveryEncounterDefinition.Calendar || epoch.Order.Count != 3
                || !Validation.ValidId(previousPartyEpochId) || previousPartyEpochId == epoch.Id || priorDefenderLocalStart < 0
                || rolls == null || rolls.Length != 3 || rolls.Any(x => x == null)
                || !rolls.Select(x => x.ActorId).SequenceEqual(new[] { PostRecoveryEncounterDefinition.Hero,
                    PostRecoveryEncounterDefinition.Companion, PostRecoveryEncounterDefinition.Actor }.OrderBy(x => x, StringComparer.Ordinal))
                || rolls.Skip(1).Where((x,i) => rolls[i].RandomAfter != x.RandomBefore).Any()
                || !epoch.Order.SequenceEqual(rolls.OrderByDescending(x => x.Total)
                    .ThenBy(x => PostRecoveryEncounterDefinition.TieOrder(x.ActorId)).Select(x => x.ActorId))
                || carried == null || carried.Length != 2 || carried.Any(x => x == null)
                || !carried.Select(x => x.Interval.ActorId).OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(new[] { PostRecoveryEncounterDefinition.Hero, PostRecoveryEncounterDefinition.Companion })
                || defenderActivity == null || defenderActivity.ActorId != PostRecoveryEncounterDefinition.Actor
                || reactions == null || reactions.Any(x => !PostRecoveryEncounterDefinition.IsParticipant(x))
                || !reactions.SequenceEqual(reactions.Distinct(StringComparer.Ordinal).OrderBy(x => x, StringComparer.Ordinal)))
                throw new ArgumentException("Invalid post-recovery admission provenance.");
            Epoch = epoch; PreviousPartyEpochId = previousPartyEpochId; PriorDefenderLocalStart = priorDefenderLocalStart;
            Draws = Array.AsReadOnly(rolls); PartyCarried = Array.AsReadOnly(carried.OrderBy(x => x.Interval.ActorId, StringComparer.Ordinal).ToArray());
            DefenderActivity = defenderActivity; InitialReactionActors = Array.AsReadOnly(reactions);
        }

        public PostRecoveryAdmission At(long slot) => slot == Epoch.ProcessedSlot ? this : new PostRecoveryAdmission(
            Epoch.At(slot), PreviousPartyEpochId, PriorDefenderLocalStart, Draws, PartyCarried, DefenderActivity, InitialReactionActors);

        public WorldIntervalRecord CarriedInterval(string actor)
        {
            if (PostRecoveryEncounterDefinition.IsParty(actor)) return PartyCarried.Single(x => x.Interval.ActorId == actor).Interval;
            if (actor != PostRecoveryEncounterDefinition.Actor) throw new ArgumentException("Unknown admitted actor.");
            return new WorldIntervalRecord(actor, -1, DefenderActivity.MovementSpent,
                DefenderActivity.Action != WorldActionCommitment.None, DefenderActivity.DashPaid, InitialReactionActors.Contains(actor));
        }
    }

    public sealed class PostRecoveryEncounterRecord
    {
        public const int MaxContacts = 32;
        public PostRecoveryEncounterDefinition Definition { get; }
        public IReadOnlyList<PostRecoveryContact> Contacts { get; }
        public PostRecoveryAdmission Admission { get; }
        public PostRecoveryContact Entered => Contacts.SingleOrDefault(x => x.Failure == "");

        public PostRecoveryEncounterRecord(PostRecoveryEncounterDefinition definition,
            IEnumerable<PostRecoveryContact> contacts = null, PostRecoveryAdmission admission = null)
        {
            Definition = definition ?? throw new ArgumentNullException(nameof(definition));
            var rows = (contacts ?? Array.Empty<PostRecoveryContact>()).ToArray();
            if (rows.Length > MaxContacts || rows.Any(x => x == null)
                || rows.Skip(1).Where((x,i) => x.ApproachRevision <= rows[i].Revision || x.At < rows[i].At).Any()
                || rows.Count(x => x.Failure == "") > 1 || rows.Any(x => x.Failure == "" && x != rows.Last())
                || (admission != null) != rows.Any(x => x.Failure == "")
                || admission != null && (rows.Last().At != admission.Epoch.Origin || !definition.CompanionConsents || !definition.DirectorAuthorizes))
                throw new ArgumentException("Invalid post-recovery encounter history.");
            Contacts = Array.AsReadOnly(rows); Admission = admission;
        }

        public PostRecoveryEncounterRecord Append(PostRecoveryContact contact, PostRecoveryAdmission admission = null)
            => new PostRecoveryEncounterRecord(Definition, Contacts.Append(contact), admission ?? Admission);
        public PostRecoveryEncounterRecord At(long slot) => new PostRecoveryEncounterRecord(Definition, Contacts, Admission.At(slot));
    }

    public static partial class PostRecoveryProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.post-recovery-v1-";
        public const byte Marker = 16;
        public const string Approval = "cb561b81-6fb9-5530-8c08-7a4233e8be12";
        public static bool SelectedFingerprint(string value) => value != null && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal) || BishopProfile.SelectedFingerprint(value));
        public static bool Active(Snapshot state) => state.PostRecoveryEncounter?.Admission != null
            && state.Encounter?.Id == PostRecoveryEncounterDefinition.Encounter;
        public static bool OwnsCurrent(Snapshot state, string actor) => state.PostRecoveryEncounter?.Admission != null
            && PostRecoveryEncounterDefinition.IsParticipant(actor);
        public static bool IsEpoch(Snapshot state, string epoch) => epoch != null && state.PostRecoveryEncounter?.Admission?.Epoch.Id == epoch;
    }
}
