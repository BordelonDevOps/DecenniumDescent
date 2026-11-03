using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExecutionProfile { Laboratory, Release }
    public enum CommandKind { Move, Interact, AdvanceClock }
    public enum Outcome { Rejected, Committed, Duplicate }

    // DTOs are detached copies. No caller ever receives the owned simulation state.
    public sealed class ActorState
    {
        public string Id;
        public int X, Y, Tokens;
        public ActorState Copy() => (ActorState)MemberwiseClone();
    }
    public sealed class ObjectState
    {
        public string Id;
        public int X, Y;
        public bool Opened;
        public ObjectState Copy() => (ObjectState)MemberwiseClone();
    }
    public sealed class CommandReceipt
    {
        public string Principal, Id, Fingerprint;
        public long Revision;
        public CommandReceipt Copy() => (CommandReceipt)MemberwiseClone();
    }
    public sealed class Snapshot
    {
        public const int Schema = 1;
        public string ContentFingerprint;
        public bool TestOnly;
        public long Revision, Clock;
        public uint RandomState;
        public ActorState[] Actors;
        public ObjectState[] Objects;
        public CommandReceipt[] Receipts;
        public Snapshot Copy() => new Snapshot {
            ContentFingerprint = ContentFingerprint, TestOnly = TestOnly,
            Revision = Revision, Clock = Clock, RandomState = RandomState,
            Actors = Actors.Select(x => x.Copy()).ToArray(),
            Objects = Objects.Select(x => x.Copy()).ToArray(),
            Receipts = Receipts.Select(x => x.Copy()).ToArray()
        };
    }

    public sealed class Command
    {
        public string Id { get; }
        public string Actor { get; }
        public string Target { get; }
        public long ExpectedRevision { get; }
        public CommandKind Kind { get; }
        public int X { get; }
        public int Y { get; }
        public Command(string id, string actor, long revision, CommandKind kind,
            string target = "", int x = 0, int y = 0)
        { Id = id; Actor = actor; ExpectedRevision = revision; Kind = kind; Target = target; X = x; Y = y; }
        internal string Fingerprint => ((int)Kind).ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + Actor + "|" + Target + "|" + ExpectedRevision.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + X.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + Y.ToString(System.Globalization.CultureInfo.InvariantCulture);
    }

    // Constructed by the trusted local/host adapter, never from a claimed command identity.
    // Pass the current grant each time so revocation also applies to duplicate requests.
    public sealed class Authority
    {
        public string Principal { get; }
        public bool CanAdvanceClock { get; }
        private readonly HashSet<string> actors;
        public Authority(string principal, IEnumerable<string> controlledActors, bool canAdvanceClock = false)
        {
            if (!Validation.ValidId(principal) || controlledActors == null) throw new ArgumentException("Invalid authority.");
            Principal = principal; CanAdvanceClock = canAdvanceClock;
            actors = new HashSet<string>(controlledActors, StringComparer.Ordinal);
            if (actors.Any(x => !Validation.ValidId(x))) throw new ArgumentException("Invalid actor grant.");
        }
        public bool Controls(string actor) => actors.Contains(actor);
    }

    public interface ICommandPolicy
    {
        string ContentFingerprint { get; }
        bool TestOnly { get; }
        // Return null for success. Work on the detached candidate only.
        string Resolve(Snapshot candidate, Command command);
        string ValidateState(Snapshot candidate);
    }

    public sealed class CommandResult
    {
        public Outcome Outcome { get; }
        public string Code { get; }
        public long Revision { get; }
        internal CommandResult(Outcome outcome, string code, long revision)
        { Outcome = outcome; Code = code; Revision = revision; }
    }

    public static class Validation
    {
        public const int MaxReceipts = 1024;
        public static bool ValidId(string value)
        {
            if (string.IsNullOrEmpty(value) || value.Length > 96) return false;
            return value.All(c => (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                || (c >= '0' && c <= '9') || c == '_' || c == '-' || c == '.');
        }
        public static void Snapshot(Snapshot s)
        {
            if (s == null || !ValidId(s.ContentFingerprint) || s.Revision < 0 || s.Clock < 0 || s.RandomState == 0)
                throw new ArgumentException("Invalid snapshot header.");
            if (s.Actors == null || s.Objects == null || s.Receipts == null || s.Actors.Length == 0
                || s.Actors.Length > 64 || s.Objects.Length > 64 || s.Receipts.Length > MaxReceipts)
                throw new ArgumentException("Invalid snapshot counts.");
            if (s.Actors.Any(a => a == null || !ValidId(a.Id) || a.Tokens < 0)
                || s.Objects.Any(o => o == null || !ValidId(o.Id))) throw new ArgumentException("Invalid entity.");
            if (s.Actors.Select(a => a.Id).Concat(s.Objects.Select(o => o.Id)).Distinct(StringComparer.Ordinal).Count()
                != s.Actors.Length + s.Objects.Length) throw new ArgumentException("Duplicate entity ID.");
            if (s.Receipts.Any(r => r == null || !ValidId(r.Principal) || !ValidId(r.Id)
                || string.IsNullOrEmpty(r.Fingerprint) || r.Fingerprint.Length > 512
                || r.Fingerprint.Any(c => c < 32 || c > 126) || r.Revision < 1 || r.Revision > s.Revision))
                throw new ArgumentException("Invalid receipt.");
            if (s.Receipts.Select(r => r.Principal + "|" + r.Id).Distinct(StringComparer.Ordinal).Count() != s.Receipts.Length)
                throw new ArgumentException("Duplicate receipt.");
        }
    }

    // Single-threaded host owner. Network transport, cadence and production rules are outside this increment.
    public sealed class Simulation
    {
        private Snapshot state;
        private readonly ICommandPolicy policy;
        public Simulation(ICommandPolicy policy, Snapshot initial, ExecutionProfile profile)
        {
            this.policy = policy ?? throw new ArgumentNullException(nameof(policy));
            if (!Enum.IsDefined(typeof(ExecutionProfile), profile)) throw new ArgumentException("Invalid profile.");
            ValidateCandidate(initial);
            if (profile == ExecutionProfile.Release && (policy.TestOnly || initial.TestOnly))
                throw new InvalidOperationException("TEST_ONLY content is forbidden in release.");
            state = initial.Copy();
        }
        public Snapshot Capture() => state.Copy();
        private void ValidateCandidate(Snapshot candidate)
        {
            Validation.Snapshot(candidate);
            if (candidate.ContentFingerprint != policy.ContentFingerprint || candidate.TestOnly != policy.TestOnly)
                throw new ArgumentException("Content fingerprint or scope mismatch.");
            string error = policy.ValidateState(candidate);
            if (error != null) throw new ArgumentException(error);
        }
        public CommandResult Execute(Authority authority, Command command)
        {
            if (authority == null || command == null || !Validation.ValidId(command.Id)
                || !Validation.ValidId(command.Actor) || command.Target == null || command.Target.Length > 96
                || (command.Target.Length != 0 && !Validation.ValidId(command.Target)) || command.ExpectedRevision < 0
                || !Enum.IsDefined(typeof(CommandKind), command.Kind)) return Reject("InvalidCommand");
            if (!authority.Controls(command.Actor) || (command.Kind == CommandKind.AdvanceClock && !authority.CanAdvanceClock))
                return Reject("NotAuthorized");
            CommandReceipt previous = state.Receipts.FirstOrDefault(r => r.Principal == authority.Principal && r.Id == command.Id);
            if (previous != null)
                return previous.Fingerprint == command.Fingerprint
                    ? new CommandResult(Outcome.Duplicate, "AlreadyCommitted", previous.Revision) : Reject("CommandIdConflict");
            if (command.ExpectedRevision != state.Revision) return Reject("StaleRevision");
            if (!state.Actors.Any(a => a.Id == command.Actor)) return Reject("UnknownActor");
            if (state.Revision == long.MaxValue || state.Receipts.Length == Validation.MaxReceipts) return Reject("SessionCapacityReached");
            Snapshot candidate = state.Copy();
            string failure;
            try { failure = policy.Resolve(candidate, command); }
            catch (Exception ex) when (ex is ArgumentException || ex is OverflowException || ex is InvalidOperationException)
            { return Reject("PolicyFailure"); }
            if (failure != null) return Reject(failure);
            // Policy cannot rewrite command history, revision, identity or content scope.
            candidate.Revision = state.Revision + 1;
            candidate.Receipts = state.Receipts.Select(r => r.Copy()).Concat(new[] { new CommandReceipt {
                Principal = authority.Principal, Id = command.Id, Fingerprint = command.Fingerprint, Revision = candidate.Revision
            }}).ToArray();
            if (candidate.Clock < state.Clock) return Reject("ClockReversal");
            try { ValidateCandidate(candidate); }
            catch (ArgumentException) { return Reject("InvalidResult"); }
            state = candidate.Copy();
            return new CommandResult(Outcome.Committed, "Committed", state.Revision);
        }
        private CommandResult Reject(string reason) => new CommandResult(Outcome.Rejected, reason, state.Revision);
    }

    public static class RandomV1
    {
        public const string Algorithm = "xorshift32-v1";
        public static uint Next(ref uint state)
        {
            if (state == 0) throw new ArgumentException("RNG state cannot be zero.");
            unchecked { state ^= state << 13; state ^= state >> 17; state ^= state << 5; }
            return state;
        }
    }
}
