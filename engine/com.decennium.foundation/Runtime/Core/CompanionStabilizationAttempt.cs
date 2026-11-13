using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Resolved Medicine evidence. The shared life record remains authoritative for recovery.</summary>
    public sealed class CompanionStabilizationAttempt
    {
        public const int DC = 10;
        public string CommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string PatientId { get; }
        public int TurnOrdinal { get; }
        public RuleTime At { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public long Total => (long)Natural + Modifier;
        public bool ActionSpent => true;
        public bool Succeeded => RecoveryDie != 0;
        public int RecoveryDie { get; }
        public RuleTime? RecoveryAt => Succeeded ? At.AddSeconds(RecoveryDie * 3600L) : (RuleTime?)null;
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public CompanionStabilizationAttempt(string commandId, long revision, string actorId, string patientId, int turnOrdinal,
            RuleTime at, int first, int second, int natural, int modifier, int recoveryDie, uint randomBefore, uint randomAfter,
            long wordsConsumed)
        {
            if (!Validation.ValidId(commandId) || revision < 1 || actorId != ConnectedVialRules.CarrierId
                || patientId != ConnectedVialRules.CompanionRecipientId || turnOrdinal < 0 || at.Numerator < 0
                || first < 1 || first > 20 || second < 0 || second > 20 || natural != first && natural != second
                || natural < 1 || recoveryDie < 0 || recoveryDie > 4 || randomBefore == 0 || randomAfter == 0
                || wordsConsumed < (second == 0 ? 1 : 2) + (recoveryDie == 0 ? 0 : 1))
                throw new ArgumentException("Invalid companion stabilization attempt.");
            CommandId = commandId;
            Revision = revision;
            ActorId = actorId;
            PatientId = patientId;
            TurnOrdinal = turnOrdinal;
            At = at;
            First = first;
            Second = second;
            Natural = natural;
            Modifier = modifier;
            RecoveryDie = recoveryDie;
            RandomBefore = randomBefore;
            RandomAfter = randomAfter;
            WordsConsumed = wordsConsumed;
        }

        internal static void Validate(Snapshot state)
        {
            var attempts = state.CompanionStabilizations;
            if (attempts == null || attempts.Length > Validation.MaxReceipts
                || !state.ConnectedCompanionStabilization && attempts.Length != 0 || attempts.Any(x => x == null))
                throw new ArgumentException("Invalid companion stabilization history.");
            if (!state.ConnectedCompanionStabilization) return;

            long previous = 0;
            foreach (var attempt in attempts) {
                if (attempt.Revision <= previous || attempt.Revision > state.Revision || attempt.At > state.RuleClock)
                    throw new ArgumentException("Invalid companion stabilization revision.");
                var encounter = EncounterHistory.AtRevision(state, attempt.Revision);
                if (encounter == null || encounter.Id != state.Reinforcement?.Definition.EncounterId)
                    throw new ArgumentException("Companion stabilization requires the selected encounter.");
                int start = encounter.StartRevisions.Count - 1;
                while (start >= 0 && encounter.StartRevisions[start] >= attempt.Revision) start--;
                if (start < 0 || encounter.ObservedOrdinals[start] != attempt.TurnOrdinal
                    || !EncounterHistory.MatchesTurn(encounter, attempt.TurnOrdinal, attempt.ActorId)
                    || encounter.StartAt(attempt.TurnOrdinal) != attempt.At)
                    throw new ArgumentException("Companion stabilization has no owning regular turn.");
                var receipt = state.Receipts.SingleOrDefault(x => x.Revision == attempt.Revision);
                var command = new Command(attempt.CommandId, attempt.ActorId, attempt.Revision - 1,
                    CommandKind.StabilizeCompanion, attempt.PatientId);
                if (receipt?.Principal != "TEST_ONLY.host" || !command.MatchesReceipt(receipt))
                    throw new ArgumentException("Companion stabilization requires its exact command receipt.");
                previous = attempt.Revision;
            }
            string kind = ((int)CommandKind.StabilizeCompanion).ToString(System.Globalization.CultureInfo.InvariantCulture) + "|";
            int count = state.Receipts.Count(x => x.Fingerprint.StartsWith(kind, StringComparison.Ordinal));
            if (count != attempts.Length) throw new ArgumentException("Missing companion stabilization evidence.");
        }
    }
}
