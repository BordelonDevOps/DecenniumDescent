# Observation schema 51 code review packet

> Historical packet: this generated source bundle predates the final schema51 endpoint-placement repair and the 2026-11-06 partial-traversal acceptance. It was not submitted as a complete source packet for the excerpt-limited GPT review. Do not use the embedded source or validation counts as the current checkout; see `README.md` and `SOURCE_BINDINGS.json` for the current test evidence. Retained as historical review context only.

This packet contains the exact uncommitted C# files for an implementation review. Checkout: branch `Engine`, HEAD `4df6738972ccba92cc7cf2495a3b0bf2547b596e`; the observation work is not committed or pushed. Please review only the code included here; do not claim access to the live local checkout or its omitted files.

The accepted design consensus is recorded in `docs/unity/OBSERVATION_RULE_DECISIONS.md`. Pinned source snapshots: `COMBAT_ACTION_PLAYTEST.md` at revision `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4`, sections Cover/sight/Hide/Search; `CONDITIONS_PLAYTEST.md` at the same revision, Invisible; `CORE_RESOLUTION_PLAYTEST.md` at the same revision, task degrees. These sources specify distinct sight/location/effect facts, observer-specific Hide/Search, and Invisible reveal behavior. The geometry profile, current-location lifetime, initiative integration and traversal sampling are explicitly provisional implementation completions, not source text.

The implementation adds schema51 observation content and per-observer knowledge/audit. Existing actor positions and traversal, condition journals, shared RNG, Action intervals, command receipts, clock, inventory and persistence remain authorities. Map geometry and sight/search profiles are explicit fingerprinted TEST_ONLY fixtures. Exploration Hide/Search costs, hearing/light/special senses, Investigation traces, production geometry and general suspected-space attacks are outside this slice.

Validation already run against the current checkout: focused observation case PASS 1/1; full C# 9 warnings-as-errors suite PASS 1,172/1,172; static package checks PASS 18 with 237 assets / 237 unique GUIDs; `git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --check` PASS. The complete final trace was replayed twice from identical initial bytes and produced identical final bytes. A malformed Search-cell snapshot regression initially failed because persisted Search coordinates were not checked against map bounds; `ObservationValidation` was amended and the regression now passes. Unity import/build/runtime was not run.

Review focus: identify concrete correctness defects, especially rational geometry/closed-cell boundaries and endpoint handling; partial traversal visibility changes; current/last-known knowledge transitions; Invisible episode identity and modifier de-duplication; Hide/Search Action, RNG, and audit; attack/Overwatch integration; strict schema51 validation/codec determinism; and missing high-value regressions. Distinguish confirmed defects from untested suggestions. Do not re-open settled design decisions unless code contradicts them.

## `engine/com.decennium.foundation/Runtime/Core/ObservationRecords.cs`

```csharp
using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum ObservationEvidenceKind { None, DirectSight, Search, AttackEvidence }
    public enum ObservationActionKind { Hide, Search }
    public enum ObservationDieSelection { None, Normal, Advantage, Disadvantage }
    public enum ObservationTaskDegree { None, CriticalFailure, Failure, Success, CriticalSuccess }
    public enum ObservationActionOutcome { NoEligibleObservers, HideAttempted, SearchNoFinding, SearchFound }

    /// <summary>Persisted authored map cell; all geometry channels remain independent.</summary>
    public sealed class ObservationMapCellRecord
    {
        public int X { get; }
        public int Y { get; }
        public bool BlocksSight { get; }
        public bool BlocksEffect { get; }
        public bool BlocksMovement { get; }
        public bool Solid { get; }
        public ObservationMapCellRecord(int x, int y, bool blocksSight, bool blocksEffect, bool blocksMovement, bool solid)
        {
            if (x < 0 || y < 0 || !blocksSight && !blocksEffect && !blocksMovement && !solid || solid && !blocksMovement)
                throw new ArgumentException("Invalid observation cell channels.");
            X = x; Y = y; BlocksSight = blocksSight; BlocksEffect = blocksEffect; BlocksMovement = blocksMovement; Solid = solid;
        }
        public bool SameAs(ObservationMapCellRecord x) => x != null && X == x.X && Y == x.Y
            && BlocksSight == x.BlocksSight && BlocksEffect == x.BlocksEffect && BlocksMovement == x.BlocksMovement && Solid == x.Solid;
    }

    /// <summary>Explicit observer ranges loaded from fingerprinted TEST_ONLY content.</summary>
    public sealed class ObservationProfileRecord
    {
        public string ActorId { get; }
        public long SightRangeFeet { get; }
        public long SearchRangeFeet { get; }
        public ObservationProfileRecord(string actorId, long sightRangeFeet, long searchRangeFeet)
        {
            if (!Validation.ValidId(actorId) || sightRangeFeet < 0 || searchRangeFeet < 0)
                throw new ArgumentException("Invalid observation profile.");
            ActorId = actorId; SightRangeFeet = sightRangeFeet; SearchRangeFeet = searchRangeFeet;
        }
        public bool SameAs(ObservationProfileRecord x) => x != null && ActorId == x.ActorId
            && SightRangeFeet == x.SightRangeFeet && SearchRangeFeet == x.SearchRangeFeet;
    }

    /// <summary>Auditable tactical Hide or candidate-space Search check. For an unsuccessful Search,
    /// TargetId is deliberately empty so the observer receives no hidden identity from the record.</summary>
    public sealed class ObservationActionRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public ObservationActionKind Kind { get; }
        public ObservationActionOutcome Outcome { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public int Modifier { get; }
        public long Total { get; }
        public ObservationDieSelection Selection { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public ObservationActionRecord(string id, string actorId, string targetId, ObservationActionKind kind,
            ObservationActionOutcome outcome, RuleTime at, long revision, RuleQuantity x, RuleQuantity y,
            int first, int second, int natural, int modifier, long total, ObservationDieSelection selection,
            uint randomBefore, uint randomAfter, long wordsConsumed)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || targetId == null
                || targetId != "" && !Validation.ValidId(targetId) || !Enum.IsDefined(typeof(ObservationActionKind), kind)
                || !Enum.IsDefined(typeof(ObservationActionOutcome), outcome) || !Enum.IsDefined(typeof(ObservationDieSelection), selection)
                || revision < 1 || x.Numerator < 0 || y.Numerator < 0 || randomBefore == 0 || randomAfter == 0 || wordsConsumed < 0)
                throw new ArgumentException("Invalid observation action record.");
            bool noRoll = selection == ObservationDieSelection.None;
            if (noRoll)
            {
                if (first != 0 || second != 0 || natural != 0 || modifier != 0 || total != 0
                    || randomBefore != randomAfter || wordsConsumed != 0
                    || outcome != ObservationActionOutcome.NoEligibleObservers && outcome != ObservationActionOutcome.SearchNoFinding)
                    throw new ArgumentException("Invalid unrolled observation action.");
            }
            else
            {
                if (!Enum.IsDefined(typeof(ObservationDieSelection), selection) || first < 1 || first > 20
                    || (selection == ObservationDieSelection.Normal) != (second == 0)
                    || second < 0 || second > 20 || selection != ObservationDieSelection.Normal && second == 0
                    || natural != (selection == ObservationDieSelection.Advantage ? Math.Max(first, second)
                        : selection == ObservationDieSelection.Disadvantage ? Math.Min(first, second) : first)
                    || total != (long)natural + modifier
                    || wordsConsumed != (selection == ObservationDieSelection.Normal ? 1 : 2))
                    throw new ArgumentException("Invalid observation die audit.");
            }
            if (kind == ObservationActionKind.Hide && (targetId != ""
                    || outcome != ObservationActionOutcome.HideAttempted && outcome != ObservationActionOutcome.NoEligibleObservers)
                || kind == ObservationActionKind.Search && (outcome == ObservationActionOutcome.SearchFound) != (targetId != "")
                || kind == ObservationActionKind.Search && outcome != ObservationActionOutcome.SearchFound
                    && outcome != ObservationActionOutcome.SearchNoFinding)
                throw new ArgumentException("Observation action outcome does not match its kind.");
            if (kind == ObservationActionKind.Search && (x.Denominator != 1 || y.Denominator != 1))
                throw new ArgumentException("Search must name one authored grid cell.");
            Id = id; ActorId = actorId; TargetId = targetId; Kind = kind; Outcome = outcome; At = at; Revision = revision;
            X = x; Y = y; First = first; Second = second; Natural = natural; Modifier = modifier; Total = total;
            Selection = selection; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
        public bool SameAs(ObservationActionRecord x) => x != null && Id == x.Id && ActorId == x.ActorId && TargetId == x.TargetId
            && Kind == x.Kind && Outcome == x.Outcome && At == x.At && Revision == x.Revision && X == x.X && Y == x.Y
            && First == x.First && Second == x.Second && Natural == x.Natural && Modifier == x.Modifier && Total == x.Total
            && Selection == x.Selection && RandomBefore == x.RandomBefore && RandomAfter == x.RandomAfter && WordsConsumed == x.WordsConsumed;
    }

    /// <summary>One observer's result against a single shared Hide roll.</summary>
    public sealed class ObservationHideResultRecord
    {
        public string AttemptId { get; }
        public string ObserverId { get; }
        public RuleQuantity ObserverX { get; }
        public RuleQuantity ObserverY { get; }
        public int Dc { get; }
        public ObservationTaskDegree Degree { get; }
        public bool HiddenEstablished { get; }
        public ObservationHideResultRecord(string attemptId, string observerId, RuleQuantity observerX, RuleQuantity observerY,
            int dc, ObservationTaskDegree degree, bool hiddenEstablished)
        {
            if (!Validation.ValidId(attemptId) || !Validation.ValidId(observerId) || dc < 0
                || degree < ObservationTaskDegree.CriticalFailure || degree > ObservationTaskDegree.CriticalSuccess
                || hiddenEstablished != (degree >= ObservationTaskDegree.Success))
                throw new ArgumentException("Invalid observer-specific Hide result.");
            AttemptId = attemptId; ObserverId = observerId; ObserverX = observerX; ObserverY = observerY;
            Dc = dc; Degree = degree; HiddenEstablished = hiddenEstablished;
        }
        public bool SameAs(ObservationHideResultRecord x) => x != null && AttemptId == x.AttemptId && ObserverId == x.ObserverId
            && ObserverX == x.ObserverX && ObserverY == x.ObserverY && Dc == x.Dc && Degree == x.Degree
            && HiddenEstablished == x.HiddenEstablished;
    }

    /// <summary>Per-observer current and last-known location knowledge. This is never a shared
    /// world-visibility flag: each row belongs to exactly one observer/target pair.</summary>
    public sealed class ObserverKnowledgeRecord
    {
        public string ObserverId { get; }
        public string TargetId { get; }
        public bool HasLastKnownLocation { get; }
        public bool CurrentLocationKnown { get; }
        public RuleQuantity LastKnownX { get; }
        public RuleQuantity LastKnownY { get; }
        public ObservationEvidenceKind Evidence { get; }
        public RuleTime EvidenceAt { get; }
        public long EvidenceRevision { get; }
        public string HiddenAttemptId { get; }
        public string RevealedInvisibleEpisodeId { get; }
        public ObserverKnowledgeRecord(string observerId, string targetId, bool hasLastKnownLocation, bool currentLocationKnown,
            RuleQuantity lastKnownX, RuleQuantity lastKnownY, ObservationEvidenceKind evidence, RuleTime evidenceAt,
            long evidenceRevision, string hiddenAttemptId = "", string revealedInvisibleEpisodeId = "")
        {
            if (!Validation.ValidId(observerId) || !Validation.ValidId(targetId) || observerId == targetId
                || !Enum.IsDefined(typeof(ObservationEvidenceKind), evidence) || evidenceRevision < 0
                || hiddenAttemptId == null || hiddenAttemptId != "" && !Validation.ValidId(hiddenAttemptId)
                || revealedInvisibleEpisodeId == null || revealedInvisibleEpisodeId != "" && !Validation.ValidId(revealedInvisibleEpisodeId)
                || currentLocationKnown && (!hasLastKnownLocation || evidence == ObservationEvidenceKind.None || hiddenAttemptId != "")
                || !hasLastKnownLocation && (lastKnownX != default || lastKnownY != default || currentLocationKnown || evidence != ObservationEvidenceKind.None)
                || hasLastKnownLocation && evidence == ObservationEvidenceKind.None)
                throw new ArgumentException("Invalid observer knowledge record.");
            ObserverId = observerId; TargetId = targetId; HasLastKnownLocation = hasLastKnownLocation;
            CurrentLocationKnown = currentLocationKnown; LastKnownX = lastKnownX; LastKnownY = lastKnownY;
            Evidence = evidence; EvidenceAt = evidenceAt; EvidenceRevision = evidenceRevision;
            HiddenAttemptId = hiddenAttemptId; RevealedInvisibleEpisodeId = revealedInvisibleEpisodeId;
        }
        public bool SameAs(ObserverKnowledgeRecord x) => x != null && ObserverId == x.ObserverId && TargetId == x.TargetId
            && HasLastKnownLocation == x.HasLastKnownLocation && CurrentLocationKnown == x.CurrentLocationKnown
            && LastKnownX == x.LastKnownX && LastKnownY == x.LastKnownY && Evidence == x.Evidence
            && EvidenceAt == x.EvidenceAt && EvidenceRevision == x.EvidenceRevision
            && HiddenAttemptId == x.HiddenAttemptId && RevealedInvisibleEpisodeId == x.RevealedInvisibleEpisodeId;
    }

    public static class ObservationValidation
    {
        public const int MaxCells = 4096, MaxProfiles = Snapshot.MaxActors, MaxAttempts = 512, MaxHideResults = 4096,
            MaxKnowledgePairs = Snapshot.MaxActors * (Snapshot.MaxActors - 1);

        public static void Validate(Snapshot s)
        {
            if (s.ObservationCells == null || s.ObservationProfiles == null || s.ObservationActions == null
                || s.ObservationHideResults == null || s.ObserverKnowledge == null
                || s.ObservationCells.Length > MaxCells || s.ObservationProfiles.Length > MaxProfiles
                || s.ObservationActions.Length > MaxAttempts || s.ObservationHideResults.Length > MaxHideResults
                || s.ObserverKnowledge.Length > MaxKnowledgePairs || s.ObservationCells.Any(x => x == null)
                || s.ObservationProfiles.Any(x => x == null) || s.ObservationActions.Any(x => x == null)
                || s.ObservationHideResults.Any(x => x == null) || s.ObserverKnowledge.Any(x => x == null))
                throw new ArgumentException("Invalid observation collections.");
            if (s.SchemaVersion < Snapshot.ObservationSchema)
            {
                if (s.ObservationMapWidth != 0 || s.ObservationMapHeight != 0 || s.ObservationCells.Length != 0
                    || s.ObservationProfiles.Length != 0 || s.ObservationActions.Length != 0
                    || s.ObservationHideResults.Length != 0 || s.ObserverKnowledge.Length != 0)
                    throw new ArgumentException("Observation state requires schema51.");
                return;
            }
            if (s.ObservationMapWidth < 1 || s.ObservationMapWidth > 64 || s.ObservationMapHeight < 1 || s.ObservationMapHeight > 64
                || s.ObservationCells.Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != s.ObservationCells.Length
                || s.ObservationCells.Any(x => x.X >= s.ObservationMapWidth || x.Y >= s.ObservationMapHeight)
                || !s.Actors.Select(x => x.Id).OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(s.ObservationProfiles.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal))
                || s.ObservationCells.Any(x => x.Solid && s.Actors.Any(a => a.X == x.X && a.Y == x.Y)
                    || x.Solid && s.Objects.Any(o => o.X == x.X && o.Y == x.Y))
                || s.Actors.Any(x => x.X < 0 || x.X >= s.ObservationMapWidth || x.Y < 0 || x.Y >= s.ObservationMapHeight)
                || s.Objects.Any(x => x.X < 0 || x.X >= s.ObservationMapWidth || x.Y < 0 || x.Y >= s.ObservationMapHeight)
                || s.WorldTraversals.Any(x => x.FromX < 0 || x.FromX >= s.ObservationMapWidth || x.ToX < 0 || x.ToX >= s.ObservationMapWidth
                    || x.FromY < 0 || x.FromY >= s.ObservationMapHeight || x.ToY < 0 || x.ToY >= s.ObservationMapHeight
                    || s.ObservationCells.Any(c => c.Solid && (c.X == x.FromX && c.Y == x.FromY || c.X == x.ToX && c.Y == x.ToY))))
                throw new ArgumentException("Invalid authored observation map or occupied cell.");
            if (s.ObservationActions.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ObservationActions.Length
                || s.ObserverKnowledge.Select(x => x.ObserverId + "|" + x.TargetId).Distinct(StringComparer.Ordinal).Count() != s.ObserverKnowledge.Length
                || s.ObservationHideResults.Select(x => x.AttemptId + "|" + x.ObserverId).Distinct(StringComparer.Ordinal).Count() != s.ObservationHideResults.Length)
                throw new ArgumentException("Duplicate observation identity.");
            foreach (var action in s.ObservationActions)
            {
                if (!s.Actors.Any(x => x.Id == action.ActorId) || action.TargetId != "" && !s.Actors.Any(x => x.Id == action.TargetId)
                    || action.TargetId == action.ActorId || action.At > s.RuleClock || action.Revision > s.Revision
                    || !WithinMap(action.X, s.ObservationMapWidth) || !WithinMap(action.Y, s.ObservationMapHeight))
                    throw new ArgumentException("Observation action references invalid state.");
            }
            foreach (var result in s.ObservationHideResults)
            {
                var attempt = s.ObservationActions.SingleOrDefault(x => x.Id == result.AttemptId);
                if (attempt == null || attempt.Kind != ObservationActionKind.Hide || attempt.Outcome != ObservationActionOutcome.HideAttempted
                    || attempt.ActorId == result.ObserverId || !s.Actors.Any(x => x.Id == result.ObserverId)
                    || !WithinMap(result.ObserverX, s.ObservationMapWidth) || !WithinMap(result.ObserverY, s.ObservationMapHeight))
                    throw new ArgumentException("Hide result references an invalid observer or attempt.");
            }
            foreach (var knowledge in s.ObserverKnowledge)
            {
                if (!s.Actors.Any(x => x.Id == knowledge.ObserverId) || !s.Actors.Any(x => x.Id == knowledge.TargetId)
                    || knowledge.EvidenceAt > s.RuleClock || knowledge.EvidenceRevision > s.Revision
                    || knowledge.HasLastKnownLocation && (!WithinMap(knowledge.LastKnownX, s.ObservationMapWidth)
                        || !WithinMap(knowledge.LastKnownY, s.ObservationMapHeight)))
                    throw new ArgumentException("Observer knowledge references invalid state.");
                if (knowledge.HiddenAttemptId != "")
                {
                    var attempt = s.ObservationActions.SingleOrDefault(x => x.Id == knowledge.HiddenAttemptId);
                    if (attempt == null || attempt.Kind != ObservationActionKind.Hide || attempt.ActorId != knowledge.TargetId
                        || !s.ObservationHideResults.Any(x => x.AttemptId == attempt.Id && x.ObserverId == knowledge.ObserverId && x.HiddenEstablished))
                        throw new ArgumentException("Hidden state has no successful observer-specific Hide result.");
                }
                if (knowledge.RevealedInvisibleEpisodeId != "")
                {
                    var journal = s.Conditions.SingleOrDefault(x => x.Target == knowledge.TargetId);
                    if (journal == null || !journal.Operations.Any(x => x.Application != null
                        && x.Application.Id == knowledge.RevealedInvisibleEpisodeId && x.Application.Kind == "Invisible"))
                        throw new ArgumentException("Invisible revelation latch has no matching condition episode source.");
                }
                if (knowledge.CurrentLocationKnown)
                {
                    var actual = Position(s, knowledge.TargetId);
                    if (actual.X != knowledge.LastKnownX || actual.Y != knowledge.LastKnownY)
                        throw new ArgumentException("Current location knowledge disagrees with actual position.");
                }
            }
        }

        private static bool WithinMap(RuleQuantity coordinate, int extent)
            => coordinate.Numerator >= 0 && (BigInteger)coordinate.Numerator < (BigInteger)extent * coordinate.Denominator;

        private static (RuleQuantity X, RuleQuantity Y) Position(Snapshot s, string actorId)
        {
            var actor = s.Actors.Single(x => x.Id == actorId);
            var edge = s.WorldTraversals?.SingleOrDefault(x => x.ActorId == actorId);
            if (edge == null) return (new RuleQuantity(actor.X), new RuleQuantity(actor.Y));
            RuleQuantity Fraction(int origin, int direction)
            {
                BigInteger n = (BigInteger)origin * 5 * edge.DistanceFeet.Denominator + (BigInteger)direction * edge.DistanceFeet.Numerator;
                return RuleQuantity.FromFraction(n, (BigInteger)5 * edge.DistanceFeet.Denominator);
            }
            int dx = Math.Sign(edge.ToX - edge.FromX), dy = Math.Sign(edge.ToY - edge.FromY);
            return (Fraction(edge.FromX, dx), Fraction(edge.FromY, dy));
        }
    }
}

```

## `engine/com.decennium.foundation/Runtime/Persistence/ObservationCodec.cs`

```csharp
using System;
using System.IO;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Schema51 append-only encoding for per-observer knowledge and tactical check audits.</summary>
    internal static class ObservationCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);

        internal static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            writer.Write(snapshot.ObservationMapWidth); writer.Write(snapshot.ObservationMapHeight);
            writer.Write(snapshot.ObservationCells.Length);
            foreach (var x in snapshot.ObservationCells)
            {
                writer.Write(x.X); writer.Write(x.Y); writer.Write(x.BlocksSight); writer.Write(x.BlocksEffect);
                writer.Write(x.BlocksMovement); writer.Write(x.Solid);
            }
            writer.Write(snapshot.ObservationProfiles.Length);
            foreach (var x in snapshot.ObservationProfiles)
            { WriteText(writer, x.ActorId); writer.Write(x.SightRangeFeet); writer.Write(x.SearchRangeFeet); }
            writer.Write(snapshot.ObservationActions.Length);
            foreach (var x in snapshot.ObservationActions)
            {
                WriteText(writer, x.Id); WriteText(writer, x.ActorId); WriteText(writer, x.TargetId);
                writer.Write((int)x.Kind); writer.Write((int)x.Outcome); WriteTime(writer, x.At); writer.Write(x.Revision);
                WriteQuantity(writer, x.X); WriteQuantity(writer, x.Y);
                writer.Write(x.First); writer.Write(x.Second); writer.Write(x.Natural); writer.Write(x.Modifier); writer.Write(x.Total);
                writer.Write((int)x.Selection); writer.Write(x.RandomBefore); writer.Write(x.RandomAfter); writer.Write(x.WordsConsumed);
            }
            writer.Write(snapshot.ObservationHideResults.Length);
            foreach (var x in snapshot.ObservationHideResults)
            {
                WriteText(writer, x.AttemptId); WriteText(writer, x.ObserverId);
                WriteQuantity(writer, x.ObserverX); WriteQuantity(writer, x.ObserverY); writer.Write(x.Dc);
                writer.Write((int)x.Degree); writer.Write(x.HiddenEstablished);
            }
            writer.Write(snapshot.ObserverKnowledge.Length);
            foreach (var x in snapshot.ObserverKnowledge)
            {
                WriteText(writer, x.ObserverId); WriteText(writer, x.TargetId); writer.Write(x.HasLastKnownLocation);
                writer.Write(x.CurrentLocationKnown); WriteQuantity(writer, x.LastKnownX); WriteQuantity(writer, x.LastKnownY);
                writer.Write((int)x.Evidence); WriteTime(writer, x.EvidenceAt); writer.Write(x.EvidenceRevision);
                WriteText(writer, x.HiddenAttemptId); WriteText(writer, x.RevealedInvisibleEpisodeId);
            }
        }

        internal static void Read(BinaryReader reader, Snapshot snapshot)
        {
            snapshot.ObservationMapWidth = reader.ReadInt32(); snapshot.ObservationMapHeight = reader.ReadInt32();
            snapshot.ObservationCells = new ObservationMapCellRecord[ReadCount(reader, ObservationValidation.MaxCells)];
            for (int i = 0; i < snapshot.ObservationCells.Length; i++)
                snapshot.ObservationCells[i] = new ObservationMapCellRecord(reader.ReadInt32(), reader.ReadInt32(),
                    ReadBool(reader), ReadBool(reader), ReadBool(reader), ReadBool(reader));
            snapshot.ObservationProfiles = new ObservationProfileRecord[ReadCount(reader, ObservationValidation.MaxProfiles)];
            for (int i = 0; i < snapshot.ObservationProfiles.Length; i++)
                snapshot.ObservationProfiles[i] = new ObservationProfileRecord(ReadText(reader), reader.ReadInt64(), reader.ReadInt64());
            snapshot.ObservationActions = new ObservationActionRecord[ReadCount(reader, ObservationValidation.MaxAttempts)];
            for (int i = 0; i < snapshot.ObservationActions.Length; i++)
                snapshot.ObservationActions[i] = new ObservationActionRecord(ReadText(reader), ReadText(reader), ReadText(reader),
                    (ObservationActionKind)reader.ReadInt32(), (ObservationActionOutcome)reader.ReadInt32(), ReadTime(reader), reader.ReadInt64(),
                    ReadQuantity(reader), ReadQuantity(reader), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(),
                    reader.ReadInt32(), reader.ReadInt64(), (ObservationDieSelection)reader.ReadInt32(), reader.ReadUInt32(),
                    reader.ReadUInt32(), reader.ReadInt64());
            snapshot.ObservationHideResults = new ObservationHideResultRecord[ReadCount(reader, ObservationValidation.MaxHideResults)];
            for (int i = 0; i < snapshot.ObservationHideResults.Length; i++)
                snapshot.ObservationHideResults[i] = new ObservationHideResultRecord(ReadText(reader), ReadText(reader),
                    ReadQuantity(reader), ReadQuantity(reader), reader.ReadInt32(),
                    (ObservationTaskDegree)reader.ReadInt32(), ReadBool(reader));
            snapshot.ObserverKnowledge = new ObserverKnowledgeRecord[ReadCount(reader, ObservationValidation.MaxKnowledgePairs)];
            for (int i = 0; i < snapshot.ObserverKnowledge.Length; i++)
                snapshot.ObserverKnowledge[i] = new ObserverKnowledgeRecord(ReadText(reader), ReadText(reader), ReadBool(reader), ReadBool(reader),
                    ReadQuantity(reader), ReadQuantity(reader), (ObservationEvidenceKind)reader.ReadInt32(), ReadTime(reader), reader.ReadInt64(),
                    ReadText(reader), ReadText(reader));
        }

        private static void WriteQuantity(BinaryWriter writer, RuleQuantity value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader reader) => new RuleQuantity(reader.ReadInt64(), reader.ReadInt64());
        private static void WriteTime(BinaryWriter writer, RuleTime value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }
        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
        private static void WriteText(BinaryWriter writer, string value)
        {
            byte[] bytes = Utf8.GetBytes(value);
            if (bytes.Length > 512) throw new InvalidDataException("Observation identity exceeds the save bound.");
            writer.Write(bytes.Length); writer.Write(bytes);
        }
        private static string ReadText(BinaryReader reader)
        {
            int length = ReadCount(reader, 512); byte[] bytes = reader.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException();
            return Utf8.GetString(bytes);
        }
        private static int ReadCount(BinaryReader reader, int maximum)
        { int value = reader.ReadInt32(); if (value < 0 || value > maximum) throw new InvalidDataException("Invalid observation collection length."); return value; }
        private static bool ReadBool(BinaryReader reader)
        { byte value = reader.ReadByte(); if (value > 1) throw new InvalidDataException("Invalid observation boolean."); return value == 1; }
    }
}

```

## `engine/com.decennium.foundation/Laboratory/Model/ObservationGeometry.cs`

```csharp
#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit cell channels. Solid cells reject actor/object placement; each query channel
    /// remains independent so opaque cover does not silently imply blocked effect or movement.</summary>
    public sealed class ObservationGridCell
    {
        public int X { get; }
        public int Y { get; }
        public bool BlocksSight { get; }
        public bool BlocksEffect { get; }
        public bool BlocksMovement { get; }
        public bool Solid { get; }
        public ObservationGridCell(int x, int y, bool blocksSight, bool blocksEffect, bool blocksMovement, bool solid = false)
        {
            if (!blocksSight && !blocksEffect && !blocksMovement && !solid || solid && !blocksMovement)
                throw new ArgumentException("Observation cell must declare a blocker channel; solid cells must block movement.");
            X = x; Y = y; BlocksSight = blocksSight; BlocksEffect = blocksEffect; BlocksMovement = blocksMovement; Solid = solid;
        }
        internal string Key => string.Join(",", new[] { X.ToString(CultureInfo.InvariantCulture), Y.ToString(CultureInfo.InvariantCulture),
            BlocksSight ? "1" : "0", BlocksEffect ? "1" : "0", BlocksMovement ? "1" : "0", Solid ? "1" : "0" });
    }

    /// <summary>Explicit per-actor TEST_ONLY sight and candidate-search reach. These values are
    /// fixture facts, not universal Decennium sensory ranges.</summary>
    public sealed class ObservationSightProfile
    {
        public string ActorId { get; }
        public long SightRangeFeet { get; }
        public long SearchRangeFeet { get; }
        public ObservationSightProfile(string actorId, long sightRangeFeet, long searchRangeFeet)
        {
            if (!Validation.ValidId(actorId) || sightRangeFeet < 0 || searchRangeFeet < 0)
                throw new ArgumentException("Invalid authored observation profile.");
            ActorId = actorId; SightRangeFeet = sightRangeFeet; SearchRangeFeet = searchRangeFeet;
        }
        internal string Key => ActorId + "|" + SightRangeFeet.ToString(CultureInfo.InvariantCulture) + "|" + SearchRangeFeet.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Immutable, content-fingerprinted planar map for the TEST_ONLY shared-world host.</summary>
    public sealed class ObservationFixture
    {
        private readonly ObservationGridCell[] cells;
        private readonly ObservationSightProfile[] profiles;
        public int Width { get; }
        public int Height { get; }
        public IReadOnlyList<ObservationGridCell> Cells => Array.AsReadOnly(cells);
        public IReadOnlyList<ObservationSightProfile> Profiles => Array.AsReadOnly(profiles);
        public ObservationFixture(int width, int height, IEnumerable<ObservationGridCell> cells,
            IEnumerable<ObservationSightProfile> profiles)
        {
            if (width < 1 || width > 64 || height < 1 || height > 64 || cells == null || profiles == null)
                throw new ArgumentException("Invalid authored observation map.");
            this.cells = cells.ToArray(); this.profiles = profiles.ToArray();
            if (this.cells.Any(x => x == null) || this.profiles.Any(x => x == null)
                || this.cells.Any(x => x.X < 0 || x.X >= width || x.Y < 0 || x.Y >= height)
                || this.cells.Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != this.cells.Length
                || this.profiles.Select(x => x.ActorId).Distinct(StringComparer.Ordinal).Count() != this.profiles.Length
                || this.profiles.Length < 2 || this.profiles.Length > Snapshot.MaxActors)
                throw new ArgumentException("Invalid or duplicate observation fixture rows.");
            Width = width; Height = height;
            this.cells = this.cells.OrderBy(x => x.X).ThenBy(x => x.Y).ToArray();
            this.profiles = this.profiles.OrderBy(x => x.ActorId, StringComparer.Ordinal).ToArray();
        }
        public bool InBounds(int x, int y) => x >= 0 && x < Width && y >= 0 && y < Height;
        public ObservationSightProfile Profile(string actorId) => profiles.SingleOrDefault(x => x.ActorId == actorId);
        public ObservationGridCell Cell(int x, int y) => cells.SingleOrDefault(c => c.X == x && c.Y == y);
        internal bool SolidAt(int x, int y) => Cell(x, y)?.Solid == true;
        internal bool Blocks(int x, int y, ObservationChannel channel)
        {
            var cell = Cell(x, y);
            if (cell == null) return false;
            return channel == ObservationChannel.Sight ? cell.BlocksSight
                : channel == ObservationChannel.Effect ? cell.BlocksEffect : cell.BlocksMovement;
        }
        internal string Key => "observation-map-v1|" + Width.ToString(CultureInfo.InvariantCulture) + "x" + Height.ToString(CultureInfo.InvariantCulture)
            + "|cells=" + string.Join(";", cells.Select(x => x.Key)) + "|profiles=" + string.Join(";", profiles.Select(x => x.Key))
            + "|cell-centres|chebyshev-5ft|supercover-closed-cell-corner-blocks|channels-independent";
        internal static string BindFingerprint(string prior, ObservationFixture fixture)
        {
            using (var sha = SHA256.Create())
                return "TEST_ONLY.observation-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior + "|" + fixture.Key))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
        internal string ValidateSnapshot(Snapshot s)
        {
            if (s.Actors.Any(a => !InBounds(a.X, a.Y) || SolidAt(a.X, a.Y))
                || s.Objects.Any(o => !InBounds(o.X, o.Y) || SolidAt(o.X, o.Y))
                || !s.Actors.Select(a => a.Id).OrderBy(x => x, StringComparer.Ordinal)
                    .SequenceEqual(profiles.Select(x => x.ActorId).OrderBy(x => x, StringComparer.Ordinal)))
                return "ObservationMapPlacementOrProfileMismatch";
            if (s.ObservationMapWidth != Width || s.ObservationMapHeight != Height
                || s.ObservationCells.Length != cells.Length || s.ObservationProfiles.Length != profiles.Length
                || s.ObservationCells.OrderBy(x => x.X).ThenBy(x => x.Y)
                    .Zip(cells, (a, b) => a.X == b.X && a.Y == b.Y && a.BlocksSight == b.BlocksSight
                        && a.BlocksEffect == b.BlocksEffect && a.BlocksMovement == b.BlocksMovement && a.Solid == b.Solid).Any(x => !x)
                || s.ObservationProfiles.OrderBy(x => x.ActorId, StringComparer.Ordinal)
                    .Zip(profiles, (a, b) => a.ActorId == b.ActorId && a.SightRangeFeet == b.SightRangeFeet
                        && a.SearchRangeFeet == b.SearchRangeFeet).Any(x => !x)) return "ObservationContentMismatch";
            if (s.WorldTraversals.Any(x => !InBounds(x.FromX, x.FromY) || !InBounds(x.ToX, x.ToY)
                || SolidAt(x.FromX, x.FromY) || SolidAt(x.ToX, x.ToY))) return "ObservationTraversalOutsideAuthoredMap";
            return null;
        }
        internal void Initialize(Snapshot s)
        {
            s.ObservationMapWidth = Width; s.ObservationMapHeight = Height;
            s.ObservationCells = cells.Select(x => new ObservationMapCellRecord(x.X, x.Y,
                x.BlocksSight, x.BlocksEffect, x.BlocksMovement, x.Solid)).ToArray();
            s.ObservationProfiles = profiles.Select(x => new ObservationProfileRecord(x.ActorId,
                x.SightRangeFeet, x.SearchRangeFeet)).ToArray();
        }
    }

    internal enum ObservationChannel { Sight, Effect, Movement }

    /// <summary>Exact rational point in authored grid-cell coordinates. Actor anchors are integer
    /// cell centres; active world movement offsets them by the persisted exact partial distance.</summary>
    internal readonly struct ObservationPoint
    {
        internal RuleQuantity X { get; }
        internal RuleQuantity Y { get; }
        internal ObservationPoint(RuleQuantity x, RuleQuantity y) { X = x; Y = y; }
    }

    /// <summary>Deterministic planar visibility, line-of-effect and movement-channel queries.</summary>
    public static class ObservationGeometry
    {
        private readonly struct Fraction : IComparable<Fraction>, IEquatable<Fraction>
        {
            internal readonly BigInteger N, D;
            internal Fraction(BigInteger n, BigInteger d)
            {
                if (d == 0) throw new DivideByZeroException();
                if (d < 0) { n = -n; d = -d; }
                var gcd = BigInteger.GreatestCommonDivisor(BigInteger.Abs(n), d);
                N = n / gcd; D = d / gcd;
            }
            internal Fraction(long n) { N = n; D = 1; }
            internal static Fraction From(RuleQuantity value) => new Fraction(value.Numerator, value.Denominator);
            public int CompareTo(Fraction other) => (N * other.D).CompareTo(other.N * D);
            public bool Equals(Fraction other) => N == other.N && D == other.D;
            public override bool Equals(object obj) => obj is Fraction other && Equals(other);
            public override int GetHashCode() => unchecked(N.GetHashCode() * 397 ^ D.GetHashCode());
            public static Fraction operator +(Fraction a, Fraction b) => new Fraction(a.N * b.D + b.N * a.D, a.D * b.D);
            public static Fraction operator -(Fraction a, Fraction b) => new Fraction(a.N * b.D - b.N * a.D, a.D * b.D);
            public static Fraction operator -(Fraction value) => new Fraction(-value.N, value.D);
            public static Fraction operator *(Fraction a, Fraction b) => new Fraction(a.N * b.N, a.D * b.D);
            public static Fraction operator /(Fraction a, Fraction b) => new Fraction(a.N * b.D, a.D * b.N);
            public static bool operator <(Fraction a, Fraction b) => a.CompareTo(b) < 0;
            public static bool operator >(Fraction a, Fraction b) => a.CompareTo(b) > 0;
            public static bool operator <=(Fraction a, Fraction b) => a.CompareTo(b) <= 0;
            public static bool operator >=(Fraction a, Fraction b) => a.CompareTo(b) >= 0;
            internal static Fraction Abs(Fraction x) => x.N < 0 ? new Fraction(-x.N, x.D) : x;
            internal RuleQuantity NonnegativeQuantity() => RuleQuantity.FromFraction(N, D);
        }

        private readonly struct Point
        {
            internal readonly Fraction X, Y;
            internal Point(Fraction x, Fraction y) { X = x; Y = y; }
            internal static Point From(ObservationPoint p) => new Point(Fraction.From(p.X), Fraction.From(p.Y));
            internal static Point Cell(int x, int y) => new Point(new Fraction(x), new Fraction(y));
            internal static Point Lerp(Point a, Point b, Fraction t) => new Point(a.X + (b.X - a.X) * t, a.Y + (b.Y - a.Y) * t);
        }

        internal static ObservationPoint Position(Snapshot s, string actorId)
        {
            var actor = s.Actors.Single(a => a.Id == actorId);
            var edge = s.WorldTraversals.SingleOrDefault(x => x.ActorId == actorId);
            if (edge == null) return new ObservationPoint(new RuleQuantity(actor.X), new RuleQuantity(actor.Y));
            int dx = Math.Sign(edge.ToX - edge.FromX), dy = Math.Sign(edge.ToY - edge.FromY);
            RuleQuantity Coordinate(int origin, int direction)
            {
                BigInteger numerator = (BigInteger)origin * 5 * edge.DistanceFeet.Denominator
                    + (BigInteger)direction * edge.DistanceFeet.Numerator;
                return RuleQuantity.FromFraction(numerator, (BigInteger)5 * edge.DistanceFeet.Denominator);
            }
            return new ObservationPoint(Coordinate(edge.FromX, dx), Coordinate(edge.FromY, dy));
        }

        public static bool CanSee(Snapshot s, ObservationFixture fixture, string observerId, string targetId)
            => CanSeeAt(fixture, Profile(fixture, observerId), Point.From(Position(s, observerId)), Point.From(Position(s, targetId)));

        public static bool CanSee(Snapshot s, string observerId, string targetId)
        {
            if (s == null || s.ObservationMapWidth < 1) return false;
            return GeometricSight(s, observerId, Position(s, observerId), Position(s, targetId));
        }

        internal static bool GeometricSight(Snapshot s, string observerId, ObservationPoint observerPosition, ObservationPoint targetPosition)
        {
            var profile = s.ObservationProfiles.SingleOrDefault(x => x.ActorId == observerId);
            if (profile == null) return false;
            Point from = Point.From(observerPosition), to = Point.From(targetPosition);
            Fraction range = new Fraction(profile.SightRangeFeet, 5);
            return Fraction.Abs(to.X - from.X) <= range && Fraction.Abs(to.Y - from.Y) <= range
                && ClearLine(s, from, to, ObservationChannel.Sight);
        }

        public static bool LineOfEffectClear(Snapshot s, ObservationFixture fixture, string sourceId, string targetId)
            => ClearLine(fixture, Point.From(Position(s, sourceId)), Point.From(Position(s, targetId)), ObservationChannel.Effect);

        public static bool LineOfEffectClear(Snapshot s, string sourceId, string targetId)
            => s != null && s.ObservationMapWidth > 0
                && ClearLine(s, Point.From(Position(s, sourceId)), Point.From(Position(s, targetId)), ObservationChannel.Effect);

        public static bool Walkable(ObservationFixture fixture, int x, int y)
            => fixture != null && fixture.InBounds(x, y) && !fixture.Blocks(x, y, ObservationChannel.Movement);

        public static bool Walkable(Snapshot s, int x, int y)
            => s != null && x >= 0 && x < s.ObservationMapWidth && y >= 0 && y < s.ObservationMapHeight
                && !s.ObservationCells.Any(c => c.X == x && c.Y == y && c.BlocksMovement);

        internal static bool ClearLine(ObservationFixture fixture, ObservationPoint from, ObservationPoint to, ObservationChannel channel)
            => ClearLine(fixture, Point.From(from), Point.From(to), channel);

        private static bool CanSeeAt(ObservationFixture fixture, ObservationSightProfile profile, Point from, Point to)
        {
            if (fixture == null || profile == null) return false;
            Fraction rangeCells = new Fraction(profile.SightRangeFeet, 5);
            if (Fraction.Abs(to.X - from.X) > rangeCells || Fraction.Abs(to.Y - from.Y) > rangeCells) return false;
            return ClearLine(fixture, from, to, ObservationChannel.Sight);
        }

        private static bool ClearLine(ObservationFixture fixture, Point from, Point to, ObservationChannel channel)
        {
            if (fixture == null) return false;
            foreach (var cell in fixture.Cells)
            {
                if (!fixture.Blocks(cell.X, cell.Y, channel)) continue;
                var minX = new Fraction(2L * cell.X - 1, 2); var maxX = new Fraction(2L * cell.X + 1, 2);
                var minY = new Fraction(2L * cell.Y - 1, 2); var maxY = new Fraction(2L * cell.Y + 1, 2);
                if (SegmentIntersects(from, to, minX, maxX, minY, maxY)) return false;
            }
            return true;
        }

        private static bool ClearLine(Snapshot s, Point from, Point to, ObservationChannel channel)
        {
            foreach (var cell in s.ObservationCells)
            {
                bool blocks = channel == ObservationChannel.Sight ? cell.BlocksSight
                    : channel == ObservationChannel.Effect ? cell.BlocksEffect : cell.BlocksMovement;
                if (!blocks) continue;
                var minX = new Fraction(2L * cell.X - 1, 2); var maxX = new Fraction(2L * cell.X + 1, 2);
                var minY = new Fraction(2L * cell.Y - 1, 2); var maxY = new Fraction(2L * cell.Y + 1, 2);
                if (SegmentIntersects(from, to, minX, maxX, minY, maxY)) return false;
            }
            return true;
        }

        private static bool SegmentIntersects(Point a, Point b, Fraction minX, Fraction maxX, Fraction minY, Fraction maxY)
        {
            Fraction enter = new Fraction(0), exit = new Fraction(1);
            if (!ClipAxis(a.X, b.X - a.X, minX, maxX, ref enter, ref exit)
                || !ClipAxis(a.Y, b.Y - a.Y, minY, maxY, ref enter, ref exit)) return false;
            return enter <= exit && exit >= new Fraction(0) && enter <= new Fraction(1);
        }

        private static bool ClipAxis(Fraction origin, Fraction delta, Fraction minimum, Fraction maximum,
            ref Fraction enter, ref Fraction exit)
        {
            if (delta.N == 0) return origin >= minimum && origin <= maximum;
            Fraction a = (minimum - origin) / delta, b = (maximum - origin) / delta;
            if (a > b) { var temp = a; a = b; b = temp; }
            if (a > enter) enter = a;
            if (b < exit) exit = b;
            return enter <= exit;
        }

        /// <summary>Returns exact path parameters at which sight can change along one straight cell
        /// edge. Between consecutive values, blocker-cell supercover and Chebyshev range are stable.</summary>
        internal static IReadOnlyList<RuleQuantity> VisibilityBreakpoints(ObservationFixture fixture,
            ObservationPoint fixedPosition, int fromX, int fromY, int toX, int toY, long rangeFeet)
            => VisibilityBreakpointsCore(fixture.Cells.Where(x => x.BlocksSight).Select(x => (X: x.X, Y: x.Y)),
                fixedPosition, fromX, fromY, toX, toY, rangeFeet);

        internal static IReadOnlyList<RuleQuantity> VisibilityBreakpoints(Snapshot s, ObservationPoint fixedPosition,
            int fromX, int fromY, int toX, int toY, long rangeFeet)
            => VisibilityBreakpointsCore(s.ObservationCells.Where(x => x.BlocksSight).Select(x => (X: x.X, Y: x.Y)),
                fixedPosition, fromX, fromY, toX, toY, rangeFeet);

        private static IReadOnlyList<RuleQuantity> VisibilityBreakpointsCore(IEnumerable<(int X, int Y)> blockers,
            ObservationPoint fixedPosition, int fromX, int fromY, int toX, int toY, long rangeFeet)
        {
            var values = new List<Fraction> { new Fraction(0), new Fraction(1) };
            Point fixedPoint = Point.From(fixedPosition);
            Point start = Point.Cell(fromX, fromY), end = Point.Cell(toX, toY);
            Fraction dx = end.X - start.X, dy = end.Y - start.Y;
            Fraction range = new Fraction(rangeFeet, 5);
            if (dx.N != 0)
            {
                AddParameter(values, (fixedPoint.X - range - start.X) / dx);
                AddParameter(values, (fixedPoint.X + range - start.X) / dx);
            }
            if (dy.N != 0)
            {
                AddParameter(values, (fixedPoint.Y - range - start.Y) / dy);
                AddParameter(values, (fixedPoint.Y + range - start.Y) / dy);
            }
            foreach (var cell in blockers)
            {
                for (int sx = -1; sx <= 1; sx += 2)
                    for (int sy = -1; sy <= 1; sy += 2)
                    {
                        var corner = new Point(new Fraction(2L * cell.X + sx, 2), new Fraction(2L * cell.Y + sy, 2));
                        Fraction vx = corner.X - fixedPoint.X, vy = corner.Y - fixedPoint.Y;
                        Fraction wx = start.X - fixedPoint.X, wy = start.Y - fixedPoint.Y;
                        Fraction denominator = dx * vy - dy * vx;
                        Fraction numerator = -(wx * vy - wy * vx);
                        if (denominator.N != 0) AddParameter(values, numerator / denominator);
                        else if (numerator.N == 0)
                        {
                            Fraction lengthSquared = dx * dx + dy * dy;
                            if (lengthSquared.N != 0)
                                AddParameter(values, ((corner.X - start.X) * dx + (corner.Y - start.Y) * dy) / lengthSquared);
                        }
                    }
            }
            values.Sort();
            var unique = new List<Fraction>();
            foreach (var value in values) if (unique.Count == 0 || !unique[unique.Count - 1].Equals(value)) unique.Add(value);
            return Array.AsReadOnly(unique.Select(x => x.NonnegativeQuantity()).ToArray());
        }

        private static void AddParameter(List<Fraction> values, Fraction value)
        { if (value >= new Fraction(0) && value <= new Fraction(1)) values.Add(value); }

        internal static IReadOnlyList<RuleQuantity> ObservationSamples(ObservationFixture fixture,
            ObservationPoint fixedPosition, int fromX, int fromY, int toX, int toY, long rangeFeet)
            => ObservationSamples(VisibilityBreakpoints(fixture, fixedPosition, fromX, fromY, toX, toY, rangeFeet));

        internal static IReadOnlyList<RuleQuantity> ObservationSamples(Snapshot s, ObservationPoint fixedPosition,
            int fromX, int fromY, int toX, int toY, long rangeFeet)
            => ObservationSamples(VisibilityBreakpoints(s, fixedPosition, fromX, fromY, toX, toY, rangeFeet));

        internal static IReadOnlyList<RuleQuantity> ObservationSamples(Snapshot s, ObservationPoint fixedPosition,
            int fromX, int fromY, int toX, int toY, long rangeFeet, RuleQuantity minimum, RuleQuantity maximum)
        {
            if (minimum > maximum || maximum > new RuleQuantity(1)) throw new ArgumentException("Invalid visibility interval.");
            var boundaries = new List<RuleQuantity> { minimum, maximum };
            boundaries.AddRange(VisibilityBreakpoints(s, fixedPosition, fromX, fromY, toX, toY, rangeFeet)
                .Where(x => x > minimum && x < maximum));
            return ObservationSamples(Array.AsReadOnly(boundaries.Distinct().OrderBy(x => x).ToArray()));
        }

        private static IReadOnlyList<RuleQuantity> ObservationSamples(IReadOnlyList<RuleQuantity> values)
        {
            var breaks = values.ToArray();
            var samples = new List<RuleQuantity>(breaks);
            for (int i = 0; i + 1 < breaks.Length; i++)
                samples.Add(RuleQuantity.FromFraction((BigInteger)breaks[i].Numerator * breaks[i + 1].Denominator
                    + (BigInteger)breaks[i + 1].Numerator * breaks[i].Denominator,
                    (BigInteger)2 * breaks[i].Denominator * breaks[i + 1].Denominator));
            return Array.AsReadOnly(samples.OrderBy(x => x).ToArray());
        }

        internal static ObservationPoint AtEdge(int fromX, int fromY, int toX, int toY, RuleQuantity parameter)
        {
            int dx = Math.Sign(toX - fromX), dy = Math.Sign(toY - fromY);
            RuleQuantity Coordinate(int origin, int direction)
            {
                BigInteger numerator = (BigInteger)origin * parameter.Denominator + (BigInteger)direction * parameter.Numerator;
                return RuleQuantity.FromFraction(numerator, parameter.Denominator);
            }
            return new ObservationPoint(Coordinate(fromX, dx), Coordinate(fromY, dy));
        }

        internal static RuleTime AtTime(RuleTime start, RuleTime end, RuleQuantity fraction)
        {
            BigInteger deltaN = (BigInteger)end.Numerator * start.Denominator - (BigInteger)start.Numerator * end.Denominator;
            BigInteger deltaD = (BigInteger)end.Denominator * start.Denominator;
            BigInteger n = (BigInteger)start.Numerator * deltaD * fraction.Denominator
                + deltaN * fraction.Numerator * start.Denominator;
            BigInteger d = (BigInteger)start.Denominator * deltaD * fraction.Denominator;
            return RuleTime.FromFraction(n, d);
        }

        private static ObservationSightProfile Profile(ObservationFixture fixture, string actorId)
            => fixture?.Profile(actorId);
    }
}
#endif

```

## `engine/com.decennium.foundation/Laboratory/Model/ObservationRules.cs`

```csharp
#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    internal sealed class ObservationMovementSegment
    {
        internal WorldTraversalRecord Edge { get; }
        internal RuleQuantity FromDistance { get; }
        internal RuleQuantity ToDistance { get; }
        internal ObservationMovementSegment(WorldTraversalRecord edge, RuleQuantity fromDistance, RuleQuantity toDistance)
        { Edge = edge; FromDistance = fromDistance; ToDistance = toDistance; }
    }

    /// <summary>A per-observer view record. This projection deliberately has no hidden actor entries.</summary>
    public sealed class ObservationKnownLocation
    {
        public string ActorId { get; }
        public RuleQuantity X { get; }
        public RuleQuantity Y { get; }
        public ObservationEvidenceKind Evidence { get; }
        public RuleTime EvidenceAt { get; }
        internal ObservationKnownLocation(string actorId, RuleQuantity x, RuleQuantity y,
            ObservationEvidenceKind evidence, RuleTime evidenceAt)
        { ActorId = actorId; X = x; Y = y; Evidence = evidence; EvidenceAt = evidenceAt; }
    }

    /// <summary>
    /// Schema51 TEST_ONLY observation state. Geometry is fixture-authored; condition journals remain
    /// authoritative for sensory conditions and Invisible application episodes. This class stores only
    /// observer-specific knowledge and projects no information to an observer who has not acquired it.
    /// </summary>
    public static class ObservationRules
    {
        public static void Initialize(Snapshot s, ObservationFixture fixture)
        {
            if (s == null || fixture == null || s.SchemaVersion < Snapshot.ObservationSchema)
                throw new ArgumentException("Schema51 observation content is required.");
            s.ObserverKnowledge = Array.Empty<ObserverKnowledgeRecord>();
            foreach (var observer in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                foreach (var target in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                    if (observer.Id != target.Id && DirectSightAt(s, observer.Id, target.Id,
                        ObservationGeometry.Position(s, observer.Id), ObservationGeometry.Position(s, target.Id)))
                        Set(s, NewKnowledge(s, observer.Id, target.Id, true, ObservationGeometry.Position(s, target.Id),
                            ObservationEvidenceKind.DirectSight, s.RuleClock, 0));
        }

        /// <summary>Refreshes endpoint visibility and invalidates stale locations after unseen movement.</summary>
        public static void Refresh(Snapshot s, RuleTime at, long revision)
        {
            if (s == null || s.SchemaVersion < Snapshot.ObservationSchema) return;
            foreach (var observer in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                foreach (var target in s.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
                {
                    if (observer.Id == target.Id) continue;
                    var prior = Knowledge(s, observer.Id, target.Id);
                    var targetPosition = ObservationGeometry.Position(s, target.Id);
                    string episode = CurrentInvisibleEpisodeId(s, target.Id);
                    if (DirectSightAt(s, observer.Id, target.Id, ObservationGeometry.Position(s, observer.Id), targetPosition))
                    {
                        if (prior == null || !prior.CurrentLocationKnown || prior.LastKnownX != targetPosition.X
                            || prior.LastKnownY != targetPosition.Y || prior.Evidence != ObservationEvidenceKind.DirectSight
                            || prior.HiddenAttemptId != "" || prior.RevealedInvisibleEpisodeId != episode)
                            Set(s, NewKnowledge(s, observer.Id, target.Id, true, targetPosition,
                                ObservationEvidenceKind.DirectSight, at, revision, revealedEpisode: episode));
                    }
                    else if (prior != null)
                    {
                        bool stillAtLastKnown = prior.CurrentLocationKnown && prior.LastKnownX == targetPosition.X
                            && prior.LastKnownY == targetPosition.Y;
                        bool current = prior.CurrentLocationKnown && stillAtLastKnown;
                        string revealed = episode == "" ? "" : prior.RevealedInvisibleEpisodeId;
                        if (current != prior.CurrentLocationKnown || revealed != prior.RevealedInvisibleEpisodeId)
                            Set(s, Copy(prior, currentLocationKnown: current, revealedEpisode: revealed));
                    }
                }
        }

        /// <summary>Returns only the current/last-known entries available to one observer.</summary>
        public static IReadOnlyList<ObservationKnownLocation> KnownLocations(Snapshot s, string observerId)
        {
            if (s == null || !Validation.ValidId(observerId) || !s.Actors.Any(x => x.Id == observerId))
                throw new ArgumentException("A current observer is required.");
            var known = new List<ObservationKnownLocation>();
            foreach (var target in s.Actors.Where(x => x.Id != observerId).OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                var point = ObservationGeometry.Position(s, target.Id);
                var row = Knowledge(s, observerId, target.Id);
                if (CanSee(s, observerId, target.Id))
                    known.Add(new ObservationKnownLocation(target.Id, point.X, point.Y,
                        ObservationEvidenceKind.DirectSight, row?.EvidenceAt ?? s.RuleClock));
                else if (row != null && row.CurrentLocationKnown && row.LastKnownX == point.X && row.LastKnownY == point.Y
                    && !HiddenTo(s, observerId, target.Id))
                    known.Add(new ObservationKnownLocation(target.Id, row.LastKnownX, row.LastKnownY, row.Evidence, row.EvidenceAt));
            }
            return Array.AsReadOnly(known.ToArray());
        }

        public static bool CanSee(Snapshot s, string observerId, string targetId)
        {
            if (s == null || s.SchemaVersion < Snapshot.ObservationSchema || observerId == targetId) return false;
            if (!DirectSightAt(s, observerId, targetId, ObservationGeometry.Position(s, observerId), ObservationGeometry.Position(s, targetId)))
                return false;
            return !HiddenTo(s, observerId, targetId);
        }

        /// <summary>Known location is separate from sight, but successful Hide suppresses stale knowledge.</summary>
        public static bool LocationKnown(Snapshot s, string observerId, string targetId)
        {
            if (CanSee(s, observerId, targetId)) return true;
            var row = Knowledge(s, observerId, targetId);
            if (row == null || !row.CurrentLocationKnown || HiddenTo(s, observerId, targetId)) return false;
            var actual = ObservationGeometry.Position(s, targetId);
            return row.LastKnownX == actual.X && row.LastKnownY == actual.Y;
        }

        public static bool HiddenTo(Snapshot s, string observerId, string targetId)
        {
            if (s == null || s.SchemaVersion < Snapshot.ObservationSchema || observerId == targetId) return false;
            var row = Knowledge(s, observerId, targetId);
            if (row == null || row.HiddenAttemptId == "") return false;
            return !DirectSightAt(s, observerId, targetId, ObservationGeometry.Position(s, observerId), ObservationGeometry.Position(s, targetId));
        }

        /// <summary>True only for the Invisible episode explicitly disclosed to this observer.</summary>
        public static bool InvisibleRevealed(Snapshot s, string observerId, string targetId)
        {
            string episode = CurrentInvisibleEpisodeId(s, targetId);
            if (episode == "") return false;
            return Knowledge(s, observerId, targetId)?.RevealedInvisibleEpisodeId == episode;
        }

        internal static string CurrentInvisibleEpisodeId(Snapshot s, string targetId)
        {
            if (s.SchemaVersion < Snapshot.ConditionSchema || !s.Conditions.Any(x => x.Target == targetId)) return "";
            var ledger = TestOnlyClubAttackPolicy.ConditionsFor(s, targetId);
            var currentIds = new HashSet<string>(ledger.View().Sources(ConditionKind.Invisible), StringComparer.Ordinal);
            if (currentIds.Count == 0) return "";
            var all = ledger.Applications.Where(x => x.Application.Kind == ConditionKind.Invisible).ToArray();
            var connected = new HashSet<string>(currentIds, StringComparer.Ordinal);
            var starts = all.Where(x => currentIds.Contains(x.Id)).Select(x => x.Application.Starts).ToArray();
            var ends = all.Where(x => currentIds.Contains(x.Id)).Select(EndOf).ToArray();
            var earliest = starts.Min(); var latest = ends.Max();
            bool changed;
            do
            {
                changed = false;
                foreach (var instance in all)
                {
                    if (connected.Contains(instance.Id)) continue;
                    var start = instance.Application.Starts; var end = EndOf(instance);
                    if (start.CompareTo(latest) <= 0 && end.CompareTo(earliest) >= 0)
                    {
                        connected.Add(instance.Id); starts = starts.Concat(new[] { start }).ToArray();
                        ends = ends.Concat(new[] { end }).ToArray(); earliest = starts.Min(); latest = ends.Max(); changed = true;
                    }
                }
            } while (changed);
            return all.Where(x => connected.Contains(x.Id)).OrderBy(x => x.Application.Starts)
                .ThenBy(x => x.Id, StringComparer.Ordinal).First().Id;
        }

        private static EffectClockMarker EndOf(ConditionInstance instance)
        {
            var ends = new[] { instance.EndedAt, instance.Application.Expires }.Where(x => x.HasValue)
                .Select(x => x.Value).ToArray();
            return ends.Length == 0 ? new EffectClockMarker(new RuleTime(long.MaxValue), int.MaxValue) : ends.Min();
        }

        internal static bool DirectSightAt(Snapshot s, string observerId, string targetId,
            ObservationPoint observerPosition, ObservationPoint targetPosition)
        {
            if (s.SchemaVersion < Snapshot.ConditionSchema || !s.Actors.Any(x => x.Id == observerId)
                || !s.Actors.Any(x => x.Id == targetId) || !ActorLifeRules.CanAct(s, observerId)) return false;
            var observer = TestOnlyClubAttackPolicy.ConditionsFor(s, observerId).View();
            var target = TestOnlyClubAttackPolicy.ConditionsFor(s, targetId).View();
            return !observer.Unaware && !observer.BlocksSight && !target.Has(ConditionKind.Invisible)
                && ObservationGeometry.GeometricSight(s, observerId, observerPosition, targetPosition);
        }

        /// <summary>Checks sight with only the target's Invisible component lifted. Used to avoid
        /// counting the same known Invisible episode as both condition disadvantage and generic unseen.</summary>
        internal static bool InvisibleIsOnlySightBlocker(Snapshot s, string observerId, string targetId)
        {
            if (!TestOnlyClubAttackPolicy.ConditionsFor(s, targetId).View().Has(ConditionKind.Invisible)
                || !ActorLifeRules.CanAct(s, observerId)) return false;
            var observer = TestOnlyClubAttackPolicy.ConditionsFor(s, observerId).View();
            return !observer.Unaware && !observer.BlocksSight
                && ObservationGeometry.GeometricSight(s, observerId, ObservationGeometry.Position(s, observerId),
                    ObservationGeometry.Position(s, targetId));
        }

        internal static void DiscloseLocation(Snapshot s, string observerId, string targetId,
            ObservationEvidenceKind evidence, RuleTime at, long revision)
        {
            if (evidence != ObservationEvidenceKind.Search && evidence != ObservationEvidenceKind.AttackEvidence)
                throw new ArgumentOutOfRangeException(nameof(evidence));
            var position = ObservationGeometry.Position(s, targetId);
            string episode = CurrentInvisibleEpisodeId(s, targetId);
            var prior = Knowledge(s, observerId, targetId);
            Set(s, NewKnowledge(s, observerId, targetId, true, position, evidence, at, revision,
                revealedEpisode: episode == "" ? prior?.RevealedInvisibleEpisodeId ?? "" : episode));
        }

        internal static void ApplyHide(Snapshot s, string observerId, string targetId, string attemptId,
            RuleTime at, long revision)
        {
            var prior = Knowledge(s, observerId, targetId);
            string episode = CurrentInvisibleEpisodeId(s, targetId);
            if (prior == null)
                prior = NewKnowledge(s, observerId, targetId, false, default, ObservationEvidenceKind.None, at, revision);
            Set(s, Copy(prior, currentLocationKnown: false, hiddenAttemptId: attemptId,
                revealedEpisode: episode == "" ? prior.RevealedInvisibleEpisodeId : episode));
        }

        internal static void ProcessWorldTraversalSegments(Snapshot s, IReadOnlyList<ObservationMovementSegment> segments,
            RuleTime start, RuleTime end, long revision)
        {
            if (segments == null || segments.Count == 0 || s.SchemaVersion < Snapshot.ObservationSchema) return;
            var moving = new HashSet<string>(segments.Select(x => x.Edge.ActorId), StringComparer.Ordinal);
            foreach (var segment in segments.OrderBy(x => x.Edge.ActorId, StringComparer.Ordinal))
            {
                string mover = segment.Edge.ActorId;
                RuleQuantity minimum = segment.FromDistance.Scale(1, 5), maximum = segment.ToDistance.Scale(1, 5);
                if (maximum <= minimum) continue;
                foreach (var other in s.Actors.Where(x => x.Id != mover && !moving.Contains(x.Id)).OrderBy(x => x.Id, StringComparer.Ordinal))
                {
                    var fixedPoint = ObservationGeometry.Position(s, other.Id);
                    RecordPathSight(s, segment, mover, other.Id, true, fixedPoint, minimum, maximum, start, end, revision);
                    RecordPathSight(s, segment, mover, other.Id, false, fixedPoint, minimum, maximum, start, end, revision);
                }
            }
        }

        private static void RecordPathSight(Snapshot s, ObservationMovementSegment segment, string mover, string other,
            bool moverIsTarget, ObservationPoint fixedPoint, RuleQuantity minimum, RuleQuantity maximum,
            RuleTime start, RuleTime end, long revision)
        {
            string observer = moverIsTarget ? other : mover;
            string target = moverIsTarget ? mover : other;
            long range = s.ObservationProfiles.Single(x => x.ActorId == observer).SightRangeFeet;
            var samples = ObservationGeometry.ObservationSamples(s, fixedPoint, segment.Edge.FromX, segment.Edge.FromY,
                segment.Edge.ToX, segment.Edge.ToY, range, minimum, maximum);
            ObservationPoint lastVisible = default;
            RuleQuantity lastParameter = default;
            bool found = false;
            foreach (var sample in samples)
            {
                var movingPoint = ObservationGeometry.AtEdge(segment.Edge.FromX, segment.Edge.FromY,
                    segment.Edge.ToX, segment.Edge.ToY, sample);
                var observerPoint = moverIsTarget ? fixedPoint : movingPoint;
                var targetPoint = moverIsTarget ? movingPoint : fixedPoint;
                if (DirectSightAt(s, observer, target, observerPoint, targetPoint))
                { found = true; lastVisible = targetPoint; lastParameter = sample; }
            }
            if (!found) return;
            RuleQuantity subsegment = FractionBetween(lastParameter, minimum, maximum);
            RuleTime evidenceAt = ObservationGeometry.AtTime(start, end, subsegment);
            var actualTarget = ObservationGeometry.Position(s, target);
            bool stillCurrent = lastVisible.X == actualTarget.X && lastVisible.Y == actualTarget.Y;
            var prior = Knowledge(s, observer, target);
            string episode = CurrentInvisibleEpisodeId(s, target);
            Set(s, NewKnowledge(s, observer, target, stillCurrent, lastVisible,
                ObservationEvidenceKind.DirectSight, evidenceAt, revision,
                revealedEpisode: episode == "" ? prior?.RevealedInvisibleEpisodeId ?? "" : episode));
        }

        private static RuleQuantity FractionBetween(RuleQuantity point, RuleQuantity start, RuleQuantity end)
        {
            var numerator = (System.Numerics.BigInteger)point.Numerator * start.Denominator
                - (System.Numerics.BigInteger)start.Numerator * point.Denominator;
            numerator *= end.Denominator;
            var denominator = (System.Numerics.BigInteger)point.Denominator
                * ((System.Numerics.BigInteger)end.Numerator * start.Denominator
                    - (System.Numerics.BigInteger)start.Numerator * end.Denominator);
            return RuleQuantity.FromFraction(numerator, denominator);
        }

        private static ObserverKnowledgeRecord NewKnowledge(Snapshot s, string observer, string target,
            bool current, ObservationPoint point, ObservationEvidenceKind evidence, RuleTime at, long revision,
            string hiddenAttempt = "", string revealedEpisode = "")
            => new ObserverKnowledgeRecord(observer, target, evidence != ObservationEvidenceKind.None,
                current, point.X, point.Y, evidence, at, revision, hiddenAttempt, revealedEpisode);

        private static ObserverKnowledgeRecord Copy(ObserverKnowledgeRecord prior, bool? currentLocationKnown = null,
            string hiddenAttemptId = null, string revealedEpisode = null)
            => new ObserverKnowledgeRecord(prior.ObserverId, prior.TargetId, prior.HasLastKnownLocation,
                currentLocationKnown ?? prior.CurrentLocationKnown, prior.LastKnownX, prior.LastKnownY, prior.Evidence,
                prior.EvidenceAt, prior.EvidenceRevision, hiddenAttemptId ?? prior.HiddenAttemptId,
                revealedEpisode ?? prior.RevealedInvisibleEpisodeId);

        private static ObserverKnowledgeRecord Knowledge(Snapshot s, string observer, string target)
            => s.ObserverKnowledge.SingleOrDefault(x => x.ObserverId == observer && x.TargetId == target);

        private static void Set(Snapshot s, ObserverKnowledgeRecord value)
        {
            var prior = Knowledge(s, value.ObserverId, value.TargetId);
            if (prior == null)
            {
                if (s.ObserverKnowledge.Length >= ObservationValidation.MaxKnowledgePairs)
                    throw new InvalidOperationException("Observation knowledge capacity reached.");
                s.ObserverKnowledge = s.ObserverKnowledge.Concat(new[] { value }).OrderBy(x => x.ObserverId, StringComparer.Ordinal)
                    .ThenBy(x => x.TargetId, StringComparer.Ordinal).ToArray();
            }
            else s.ObserverKnowledge = s.ObserverKnowledge.Select(x => x.ObserverId == value.ObserverId && x.TargetId == value.TargetId ? value : x).ToArray();
        }
    }
}
#endif

```

## `engine/com.decennium.foundation/Laboratory/Model/SharedObservationActions.cs`

```csharp
#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        public string Resolve(Snapshot s, Command c)
        {
            string error = ResolveCore(s, c);
            if (error == null && s.SchemaVersion >= Snapshot.ObservationSchema)
                ObservationRules.Refresh(s, s.RuleClock, s.Revision + 1);
            return error;
        }

        private string ResolveObservationAction(Snapshot s, Command c)
        {
            if (observationFixture == null || s.SchemaVersion < Snapshot.ObservationSchema)
                return "ObservationActionNotImplemented";
            if (s.Encounter == null || !s.InventoryCombat) return "ObservationActionRequiresTacticalCombat";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (c.Actor != s.Encounter.CurrentActor || c.Target != s.Encounter.CurrentTurnId)
                return "WrongRegularTurn";
            if (c.Inventory != null || c.Combat != null || c.Advancement != null || c.Ranged != null
                || c.SuppressionFire != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
                || c.MiningSelection != null || c.ProspectingExposure != null || c.OverwatchRider != OverwatchRider.None)
                return "InvalidObservationActionPayload";
            if (!ActorLifeRules.CanAct(s, c.Actor)) return "ActorCannotAct";
            if (!Permissions(s, c.Actor).Action) return "ConditionPreventsAction";
            var interval = Interval(s, c.Actor);
            if (interval.ActionSpent) return "ActionAlreadySpent";
            if (s.ObservationActions.Length >= ObservationValidation.MaxAttempts) return "ObservationHistoryCapacityReached";

            string failure = c.Kind == CommandKind.Hide ? ResolveHide(s, c) : ResolveSearch(s, c);
            if (failure != null) return failure;
            SetInterval(s, interval.PayAction());
            PauseIncompatibleWork(s);
            return null;
        }

        private string ResolveHide(Snapshot s, Command c)
        {
            if (c.Target != s.Encounter.CurrentTurnId || c.X != 0 || c.Y != 0) return "InvalidHideRequest";
            var actor = s.Actors.Single(x => x.Id == c.Actor);
            var position = ObservationGeometry.Position(s, actor.Id);
            if (!IsGridCell(position.X) || !IsGridCell(position.Y)) return "HideRequiresAuthoredGridCell";

            var observers = s.Actors.Where(x => x.Id != actor.Id && ActorLifeRules.CanAct(s, x.Id)
                    && !TestOnlyClubAttackPolicy.ConditionsFor(s, x.Id).View().Unaware
                    && WithinRange(ObservationGeometry.Position(s, x.Id), position,
                        s.ObservationProfiles.Single(p => p.ActorId == x.Id).SightRangeFeet))
                .OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (observers.Any(x => ObservationRules.DirectSightAt(s, x.Id, actor.Id,
                    ObservationGeometry.Position(s, x.Id), position))) return "HideWhileClearlyObserved";
            if (s.ObservationHideResults.Length + observers.Length > ObservationValidation.MaxHideResults)
                return "ObservationHideHistoryCapacityReached";
            if (s.ObserverKnowledge.Length + observers.Count(x => !s.ObserverKnowledge.Any(k => k.ObserverId == x.Id && k.TargetId == actor.Id))
                > ObservationValidation.MaxKnowledgePairs) return "ObservationKnowledgeCapacityReached";

            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".hide";
            RuleTime at = s.RuleClock;
            if (observers.Length == 0)
            {
                s.ObservationActions = s.ObservationActions.Concat(new[] { new ObservationActionRecord(attemptId, actor.Id, "",
                    ObservationActionKind.Hide, ObservationActionOutcome.NoEligibleObservers, at, revision, position.X, position.Y,
                    0, 0, 0, 0, 0, ObservationDieSelection.None, s.RandomState, s.RandomState, 0) }).ToArray();
                return null;
            }

            var character = s.Characters.Single(x => x.ActorId == actor.Id);
            var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == actor.Id && x.SkillId == "stealth");
            int modifier = AbilityCheckRules.Derive(character, training, 1)
                .TotalWithInjury(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == actor.Id)));
            int disadvantage = TestOnlyClubAttackPolicy.ConditionsFor(s, actor.Id).View().Has(ConditionKind.Poisoned) ? 1 : 0;
            var selection = PlaytestDice.Selection(0, disadvantage);
            var observerFacts = observers.Select(observer => new
            {
                Actor = observer,
                Position = ObservationGeometry.Position(s, observer.Id),
                Dc = PassivePerception(s, observer.Id)
            }).ToArray();
            var prior = s.ObservationActions.Where(x => x.ActorId == actor.Id && x.Kind == ObservationActionKind.Hide)
                .OrderByDescending(x => x.Revision).FirstOrDefault();
            if (prior != null && prior.Outcome == ObservationActionOutcome.HideAttempted
                && prior.X == position.X && prior.Y == position.Y && prior.Modifier == modifier
                && prior.Selection == DieSelection(selection))
            {
                var priorResults = s.ObservationHideResults.Where(x => x.AttemptId == prior.Id)
                    .OrderBy(x => x.ObserverId, StringComparer.Ordinal).ToArray();
                bool unchanged = priorResults.Length == observerFacts.Length
                    && observerFacts.OrderBy(x => x.Actor.Id, StringComparer.Ordinal).Select((x, i) =>
                        priorResults[i].ObserverId == x.Actor.Id && priorResults[i].Dc == x.Dc
                            && priorResults[i].ObserverX == x.Position.X && priorResults[i].ObserverY == x.Position.Y).All(x => x);
                if (unchanged && priorResults.Any(x => !x.HiddenEstablished)) return "HideAttemptUnchanged";
            }
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var action = new ObservationActionRecord(attemptId, actor.Id, "", ObservationActionKind.Hide,
                ObservationActionOutcome.HideAttempted, at, revision, position.X, position.Y, roll.First,
                roll.Second ?? 0, roll.Natural, modifier, roll.Natural + (long)modifier, DieSelection(roll.Selection),
                before, roll.NextRandomState, roll.WordsConsumed);
            var results = observerFacts.Select(fact =>
            {
                var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, fact.Dc);
                var degree = ObservationDegree(check.Degree);
                return new ObservationHideResultRecord(attemptId, fact.Actor.Id, fact.Position.X, fact.Position.Y,
                    fact.Dc, degree, check.Success);
            }).ToArray();
            s.ObservationActions = s.ObservationActions.Concat(new[] { action }).ToArray();
            s.ObservationHideResults = s.ObservationHideResults.Concat(results).ToArray();
            s.RandomState = roll.NextRandomState;
            foreach (var result in results.Where(x => x.HiddenEstablished))
                ObservationRules.ApplyHide(s, result.ObserverId, actor.Id, attemptId, at, revision);
            return null;
        }

        private string ResolveSearch(Snapshot s, Command c)
        {
            if (c.Target != s.Encounter.CurrentTurnId || c.X < 0 || c.Y < 0
                || c.X >= s.ObservationMapWidth || c.Y >= s.ObservationMapHeight) return "InvalidSearchRequest";
            var profile = s.ObservationProfiles.Single(x => x.ActorId == c.Actor);
            var searcher = ObservationGeometry.Position(s, c.Actor);
            var candidateCell = new ObservationPoint(new RuleQuantity(c.X), new RuleQuantity(c.Y));
            if (!WithinRange(searcher, candidateCell, profile.SearchRangeFeet)) return "SearchCellOutOfRange";
            var targets = s.Actors.Where(x => x.Id != c.Actor && s.WorldSchedule.Order.Contains(x.Id)
                    && ObservationRules.HiddenTo(s, c.Actor, x.Id))
                .Where(x =>
                {
                    var point = ObservationGeometry.Position(s, x.Id);
                    return IsGridCell(point.X) && IsGridCell(point.Y) && point.X == candidateCell.X && point.Y == candidateCell.Y;
                }).OrderBy(x => x.Id, StringComparer.Ordinal).ToArray();
            if (targets.Length > 1) return "SearchCandidateAmbiguous";
            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".search";
            RuleTime at = s.RuleClock;
            if (targets.Length == 0)
            {
                s.ObservationActions = s.ObservationActions.Concat(new[] { new ObservationActionRecord(attemptId, c.Actor, "",
                    ObservationActionKind.Search, ObservationActionOutcome.SearchNoFinding, at, revision, candidateCell.X, candidateCell.Y,
                    0, 0, 0, 0, 0, ObservationDieSelection.None, s.RandomState, s.RandomState, 0) }).ToArray();
                return null;
            }

            var target = targets[0];
            var knowledge = s.ObserverKnowledge.Single(x => x.ObserverId == c.Actor && x.TargetId == target.Id);
            var hide = s.ObservationActions.Single(x => x.Id == knowledge.HiddenAttemptId && x.Kind == ObservationActionKind.Hide);
            int dc = checked((int)hide.Total);
            var character = s.Characters.Single(x => x.ActorId == c.Actor);
            var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == c.Actor && x.SkillId == "perception");
            int modifier = AbilityCheckRules.Derive(character, training, 4)
                .TotalWithInjury(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == c.Actor)), perception: true);
            int disadvantage = TestOnlyClubAttackPolicy.ConditionsFor(s, c.Actor).View().Has(ConditionKind.Poisoned) ? 1 : 0;
            uint before = s.RandomState;
            var roll = PlaytestDice.RollD20(before, disadvantageSources: disadvantage);
            var check = PlaytestRolls.TaskCheck(roll.Natural, modifier, dc);
            bool found = check.Success;
            var action = new ObservationActionRecord(attemptId, c.Actor, found ? target.Id : "", ObservationActionKind.Search,
                found ? ObservationActionOutcome.SearchFound : ObservationActionOutcome.SearchNoFinding, at, revision,
                candidateCell.X, candidateCell.Y, roll.First, roll.Second ?? 0, roll.Natural, modifier,
                roll.Natural + (long)modifier, DieSelection(roll.Selection), before, roll.NextRandomState, roll.WordsConsumed);
            s.ObservationActions = s.ObservationActions.Concat(new[] { action }).ToArray();
            s.RandomState = roll.NextRandomState;
            if (found) ObservationRules.DiscloseLocation(s, c.Actor, target.Id, ObservationEvidenceKind.Search, at, revision);
            return null;
        }

        private static bool IsGridCell(RuleQuantity x) => x.Denominator == 1;
        private static ObservationDieSelection DieSelection(D20Selection selection)
            => selection == D20Selection.Normal ? ObservationDieSelection.Normal
                : selection == D20Selection.Advantage ? ObservationDieSelection.Advantage : ObservationDieSelection.Disadvantage;
        private static ObservationTaskDegree ObservationDegree(TaskDegree degree)
            => degree == TaskDegree.CriticalSuccess ? ObservationTaskDegree.CriticalSuccess
                : degree == TaskDegree.Success ? ObservationTaskDegree.Success
                : degree == TaskDegree.Failure ? ObservationTaskDegree.Failure : ObservationTaskDegree.CriticalFailure;

        private static int PassivePerception(Snapshot s, string actor)
        {
            var character = s.Characters.Single(x => x.ActorId == actor);
            var training = s.SkillTraining.SingleOrDefault(x => x.ActorId == actor && x.SkillId == "perception");
            var check = AbilityCheckRules.Derive(character, training, 4);
            return checked(10 + check.Total);
        }

        private static bool WithinRange(ObservationPoint a, ObservationPoint b, long rangeFeet)
        {
            BigInteger dx = BigInteger.Abs((BigInteger)a.X.Numerator * b.X.Denominator
                - (BigInteger)b.X.Numerator * a.X.Denominator);
            BigInteger dxDenominator = (BigInteger)a.X.Denominator * b.X.Denominator;
            BigInteger dy = BigInteger.Abs((BigInteger)a.Y.Numerator * b.Y.Denominator
                - (BigInteger)b.Y.Numerator * a.Y.Denominator);
            BigInteger dyDenominator = (BigInteger)a.Y.Denominator * b.Y.Denominator;
            BigInteger limit = (BigInteger)rangeFeet;
            return dx * 5 <= limit * dxDenominator && dy * 5 <= limit * dyDenominator;
        }
    }
}
#endif

```

## `engine/com.decennium.foundation/Tests/EditMode/ObservationCases.cs`

```csharp
#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ObservationFixture ObservationCoverFixture()
            => new ObservationFixture(8, 8,
                new[] { new ObservationGridCell(2, 0, blocksSight: true, blocksEffect: false, blocksMovement: true) },
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 5, 5),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                });

        private static uint ObservationHideSearchSeed(Snapshot initial)
        {
            var hider = initial.Characters.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
            var hiderSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == hider.ActorId && x.SkillId == "stealth");
            int hideModifier = AbilityCheckRules.Derive(hider, hiderSkill, 1)
                .TotalWithInjury(ActorLifeRules.Read(initial.Lives.Single(x => x.ActorId == hider.ActorId)));
            var observer = initial.Characters.Single(x => x.ActorId == AdditionalTacticalActor.Id);
            var observerSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == observer.ActorId && x.SkillId == "perception");
            int hideDc = checked(10 + AbilityCheckRules.Derive(observer, observerSkill, 4).Total);
            var searcher = initial.Characters.Single(x => x.ActorId == AdditionalTacticalActor.Id);
            var searchSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == searcher.ActorId && x.SkillId == "perception");
            int searchModifier = AbilityCheckRules.Derive(searcher, searchSkill, 4)
                .TotalWithInjury(ActorLifeRules.Read(initial.Lives.Single(x => x.ActorId == searcher.ActorId)), perception: true);
            for (uint seed = 1; seed < 1000000; seed++)
            {
                var hide = PlaytestDice.RollD20(seed);
                var hideCheck = PlaytestRolls.TaskCheck(hide.Natural, hideModifier, hideDc);
                if (!hideCheck.Success) continue;
                var search = PlaytestDice.RollD20(hide.NextRandomState);
                if (PlaytestRolls.TaskCheck(search.Natural, searchModifier, checked((int)hideCheck.Total)).Success) return seed;
            }
            throw new Exception("No deterministic Hide/Search seed was found.");
        }

        private static Command ObservationCommand(Simulation simulation, CommandKind kind, string actor = null, int x = 0, int y = 0)
        {
            var s = simulation.Capture();
            actor = actor ?? s.Encounter.CurrentActor;
            return new Command("observation.command." + (s.Revision + 1), actor, s.Revision, kind,
                s.Encounter.CurrentTurnId, x, y);
        }

        private static byte[] RunObservationTrace(TestOnlySharedWorldPolicy policy, Simulation simulation)
        {
            var hero = TestOnlyPolicy.ActorId;
            var enemy = AdditionalTacticalActor.Id;
            var host = TestOnlySharedWorldPolicy.Host();
            var initial = simulation.Capture();
            Require(initial.SchemaVersion == Snapshot.ObservationSchema
                && !ObservationRules.LocationKnown(initial, hero, enemy)
                && !ObservationRules.LocationKnown(initial, enemy, hero)
                && !ObservationRules.CanSee(initial, hero, enemy)
                && ObservationGeometry.LineOfEffectClear(initial, hero, enemy),
                "A sight-only blocker did not preserve location secrecy independently of line of effect.");

            WorldCommit(simulation, new Command("observation.begin", hero, initial.Revision, CommandKind.BeginFixedEncounter));
            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
            RejectUnchanged(simulation, host,
                Tac(simulation, CommandKind.AttackClub, enemy, weapon: TestOnlyClubAttackPolicy.ActorClub), "TargetLocationUnknown");
            RejectUnchanged(simulation, host, ObservationCommand(simulation, CommandKind.Search, hero, 7, 7), "SearchCellOutOfRange");

            var hide = ObservationCommand(simulation, CommandKind.Hide, hero);
            WorldCommit(simulation, hide);
            var hidden = simulation.Capture();
            var hideAction = hidden.ObservationActions.Single(x => x.Kind == ObservationActionKind.Hide);
            Require(hideAction.Outcome == ObservationActionOutcome.HideAttempted
                && hidden.ObservationHideResults.Length == 1 && hidden.ObservationHideResults[0].HiddenEstablished
                && ObservationRules.HiddenTo(hidden, enemy, hero) && !ObservationRules.LocationKnown(hidden, enemy, hero)
                && !ObservationRules.LocationKnown(hidden, hero, enemy),
                "Hide did not create observer-specific hidden state and preserve information boundaries.");
            byte[] afterHide = Bytes(simulation);
            Require(simulation.Execute(host, hide).Outcome == Outcome.Duplicate && afterHide.SequenceEqual(Bytes(simulation)),
                "Duplicate Hide replay consumed another Action or random draw.");
            simulation = new Simulation(policy, new SnapshotCodec().Decode(afterHide), ExecutionProfile.Laboratory);
            WorldCommit(simulation, Tac(simulation, CommandKind.EndRegularTurn));

            var search = ObservationCommand(simulation, CommandKind.Search, enemy, 0, 0);
            WorldCommit(simulation, search);
            var found = simulation.Capture();
            var searchAction = found.ObservationActions.Single(x => x.Kind == ObservationActionKind.Search);
            Require(searchAction.Outcome == ObservationActionOutcome.SearchFound && searchAction.TargetId == hero
                && !ObservationRules.HiddenTo(found, enemy, hero) && ObservationRules.LocationKnown(found, enemy, hero)
                && !ObservationRules.LocationKnown(found, hero, enemy)
                && ObservationRules.KnownLocations(found, enemy).Any(x => x.ActorId == hero)
                && !ObservationRules.KnownLocations(found, hero).Any(x => x.ActorId == enemy),
                "Search did not disclose the found location only to its searcher.");

            var invalid = simulation.Capture();
            invalid.ObservationActions = invalid.ObservationActions.Select(x => x.Id == searchAction.Id
                ? new ObservationActionRecord(x.Id, x.ActorId, x.TargetId, x.Kind, x.Outcome, x.At, x.Revision,
                    new RuleQuantity(invalid.ObservationMapWidth), x.Y, x.First, x.Second, x.Natural, x.Modifier,
                    x.Total, x.Selection, x.RandomBefore, x.RandomAfter, x.WordsConsumed)
                : x).ToArray();
            Throws<ArgumentException>(() => ObservationValidation.Validate(invalid));
            Throws<ArgumentException>(() => new Simulation(policy, invalid, ExecutionProfile.Laboratory));

            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, actor: enemy, stance: (int)CombatStance.Aggressive));
            WorldCommit(simulation, Tac(simulation, CommandKind.EndRegularTurn, actor: enemy));
            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
            RejectUnchanged(simulation, host,
                Tac(simulation, CommandKind.AttackClub, enemy, weapon: TestOnlyClubAttackPolicy.ActorClub), "TargetLocationUnknown");

            byte[] saved = Bytes(simulation);
            var restored = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
            Require(saved.SequenceEqual(Bytes(restored)) && restored.Capture().RandomState == simulation.Capture().RandomState,
                "Observation knowledge, action audit or RNG changed across save/restore.");
            return saved;
        }

        private static void AddObservationCases(Dictionary<string, Action> cases)
        {
            cases.Add("observation_shared_hide_search_save_replay_and_observer_isolation", () => {
                var fixture = ObservationCoverFixture();
                var seedProbe = new TestOnlySharedWorldPolicy(new SharedCombatFixture(), conditions: null).EnableObservation(fixture);
                var seed = ObservationHideSearchSeed(seedProbe.Initial());
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed)).EnableObservation(fixture);
                var simulation = World(policy);
                byte[] initial = Bytes(simulation);
                byte[] firstRun = RunObservationTrace(policy, simulation);
                var replay = new Simulation(policy, new SnapshotCodec().Decode(initial), ExecutionProfile.Laboratory);
                byte[] replayed = RunObservationTrace(policy, replay);
                Require(firstRun.SequenceEqual(replayed), "Replaying the complete observation command trace changed the final bytes.");
            });
        }
    }
}
#endif

```

## `engine/com.decennium.foundation/Laboratory/Model/ConditionCombatPolicy.cs` lines 25–49

```csharp
            bool ownTurn = s.Encounter?.CurrentActor == actor;
            long spent = ownTurn ? s.ActorMovement.Single(x => x.ActorId == actor).Spent
                + s.TacticalMoves.Where(x => x.ActorId == actor && x.TurnOrdinal == s.Encounter.TurnOrdinal && EncounterHistory.InCurrent(s,x.Revision) && x.Kind == TacticalMoveKind.Press && x.Status == TacticalMoveStatus.Completed).Sum(x => x.CostPaid) : 0;
            if(ownTurn&&s.WorldSchedule!=null&&s.WorldIntervals.Single(x=>x.ActorId==actor).MovementSpent!=default)spent=Math.Max(1,spent);
            return PlaytestConditions.Permissions(CombatConditions(s, actor), ownTurn && ActionSpent(s) ? 1 : 0, spent);
        }
        private static bool EffectiveProne(Snapshot s, string actor) => WithConditions(s)
            ? ConditionsFor(s, actor).View().Has(ConditionKind.Prone) : s.Lives.Single(x => x.ActorId == actor).Prone;
        internal static bool CanSee(Snapshot s, string observer, string target)
        {
            if (s.SchemaVersion >= Snapshot.ObservationSchema) return ObservationRules.CanSee(s, observer, target);
            bool conditionSight = !WithConditions(s)
                || Aware(s, observer) && !ConditionsFor(s, observer).View().BlocksSight
                    && !ConditionsFor(s, target).View().Has(ConditionKind.Invisible);
            return conditionSight;
        }
        internal static bool DamageConditionCapacity(Snapshot s, string target)
        {
            if (!WithConditions(s)) return true;
            var journal = s.Conditions.Single(x => x.Target == target);
            return journal.Operations.Count < ConditionJournal.MaxOperations && ConditionsFor(s, target).Applications.Count < ConditionLedger.MaxApplications;
        }
        private static void CommitCondition(Snapshot s, ConditionHistoryTransition result)
        {
            var ledger = result.State.Ledger; string actor = ledger.Target;
```

## `engine/com.decennium.foundation/Laboratory/Model/TestOnlyClubAttackPolicy.cs` lines 190–275

```csharp
            if(c.Kind==CommandKind.EncounterDash)return encounter.Resolve(s,c);
            if(!HasStance(s))return "StanceRequired";
            return Attack(s,c);
        }
        private static CombatDamageRoll DamageRecord(int[] dice,long total,long diceWords,uint seed,RolledDamage result)
            =>new CombatDamageRoll(dice,total,diceWords,seed,result.NextRandomState,result.WordsConsumed,result.WoundRoll?.Natural??0,result.InjuryD6??0,result.StableD4??0);
        private static string Attack(Snapshot s,Command c,bool opportunity=false)
        {
            string physical=PhysicalAttackFailure(s,c.Actor);if(physical!=null)return physical;
            var request=c.Combat;
            if(request.Stance!=0||request.Choice||s.SchemaVersion<Snapshot.TacticalMovementSchema&&request.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidAttackRequest";
            if(s.MeleeAttacks.Length==128)return "AttackHistoryCapacityReached";
            bool unarmed=c.Kind==CommandKind.AttackUnarmed;
            if(unarmed&&(s.SchemaVersion<Snapshot.TacticalMovementSchema||request.WeaponId!=""))return "InvalidUnarmedRequest";
            var weapon=s.Clubs.SingleOrDefault(w=>w.Id==request.WeaponId);
            var attacker=s.Lives.Single(l=>l.ActorId==c.Actor);
            if(!unarmed&&(weapon==null||weapon.ProfileId!=ClubProfile||weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor||!attacker.HeldItems.Contains(weapon.Id)))return "ClubNotHeld";
            var target=s.Lives.SingleOrDefault(l=>l.ActorId==c.Target);
            if(target==null||target.ActorId==c.Actor||target.Dead)return "InvalidLivingTarget";
            if(!DamageConditionCapacity(s,c.Target))return "ConditionHistoryCapacityReached";
            var a=s.Actors.Single(x=>x.Id==c.Actor);var t=s.Actors.Single(x=>x.Id==c.Target);
            if(s.SchemaVersion>=Snapshot.ObservationSchema&&!ObservationRules.LocationKnown(s,c.Actor,c.Target))return "TargetLocationUnknown";
            if(s.SchemaVersion>=Snapshot.ObservationSchema&&!ObservationGeometry.LineOfEffectClear(s,c.Actor,c.Target))return "BlockedLineOfEffect";
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(a.X,a.Y),new CombatCell(t.X,t.Y))>5)return "TargetOutOfReach";
            bool attackerInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,c.Target,c.Actor);
            bool targetInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,c.Actor,c.Target);
            var modifiers=PlaytestConditions.Attack(CombatConditions(s,c.Actor),CombatConditions(s,c.Target),
                attackerInvisibleLocationKnown:attackerInvisibleKnown,targetInvisibleLocationKnown:targetInvisibleKnown);
            var incomingEffects=SoldierTacticalFeatures.ForAttack(s,c.Actor,c.Target);
            bool advantage=modifiers.AdvantagePresent,disadvantage=modifiers.DisadvantagePresent||incomingEffects.WarningShot;
            int modifier=checked((attacker.LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0)-incomingEffects.CoveringFirePenalty
                +incomingEffects.TacticalAssessmentBonus); // STR10, explicitly no Club proficiency grant.
            var defense=ActiveStance(s,c.Target);int dexterity=s.Characters.Single(x=>x.ActorId==c.Target).Abilities[1];
            int ac=checked(CharacterAdvancementRules.ArmorClass(s,c.Target,dexterity)+(defense?.Kind==CombatStance.Aggressive?-2:defense?.Kind==CombatStance.Guarded?1:0)
                +CharacterAdvancementRules.DefensivePositioningBonus(s,c.Target));
            string attackId="attack."+N(s.Revision+1);
            string captureFailure=SoldierTacticalFeatures.CaptureAndConsume(s,attackId,c.Actor,c.Target,"",out _);if(captureFailure!=null)return captureFailure;
            uint before=s.RandomState;var roll=PlaytestDice.RollD20(before,advantage?1:0,disadvantage?1:0);
            var hit=PlaytestRolls.AttackRoll(roll.Natural,modifier,ac);bool critical=hit.Hit&&(hit.Critical||modifiers.CriticalIfHit);
            var attack=new CombatAttackRoll(roll.First,roll.Second??0,roll.Natural,modifier,ac,hit.Hit,critical,before,roll.NextRandomState,roll.WordsConsumed);
            uint next=roll.NextRandomState;CombatDamageRoll damage;bool pending=false;
            if(hit.Hit) {
                var dice=new int[unarmed?0:critical?2:1];long words=0;
                for(int i=0;i<dice.Length;i++){var d=DiceStream.Draw(next,4);dice[i]=d.Value+1;next=d.NextState;words=checked(words+d.WordsConsumed);}
                int flat=ActiveStance(s,c.Actor)?.Kind==CombatStance.Aggressive?2:0;
                long total=unarmed?PrototypeUnarmed.Damage(10,flat):dice.Sum()+flat;
                total=CharacterAdvancementRules.ReduceIncomingDamage(s,c.Target,total);
                if(WithConditions(s)&&ConditionsFor(s,c.Target).View().Has(ConditionKind.Petrified))total=PlaytestConditions.PetrifiedDamage(total);
                var targetCharacter=s.Characters.Single(x=>x.ActorId==c.Target);
                int constitutionSave=checked(PlaytestCharacters.AbilityModifier(targetCharacter.Abilities[2])
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,c.Target,"CON"));
                var result=PlaytestDamageDice.Resolve(ActorLifeRules.Read(target),total,s.RuleClock,next,constitutionSaveModifier:constitutionSave,
                    critical:critical,melee:true,knockout:(KnockoutInstruction)request.Knockout);
                damage=DamageRecord(dice,total,words,next,result);next=result.NextRandomState;pending=result.Pending!=null;
                if(pending&&s.Receipts.Length>=511)return "ContinuationCapacityReached";
                if(!pending)ApplyLife(s,target,result.Outcome.State);
                if(request.PressInstruction==PressHitInstruction.ArmOrReplace&&(s.SchemaVersion<Snapshot.TacticalMovementSchema||s.Encounter.CurrentActor==c.Actor&&!TacticalActor(s,c.Actor).PressConsumed)) {
                    var press=new PressRecord(c.Actor,c.Target,s.Revision+1,FixedEncounterRules.Start(s.Encounter,s.Encounter.TurnOrdinal+s.Encounter.Order.Count));
                    s.Presses=s.Presses.Where(p=>p.ActorId!=c.Actor).Concat(new[]{press}).ToArray();
                }
            } else damage=new CombatDamageRoll(Array.Empty<int>(),0,0,next,next,0,0,0,0);
            s.RandomState=next;
            var record=new MeleeAttackRecord(attackId,s.Revision+1,pending?0:s.Revision+1,s.Encounter.TurnOrdinal,c.Actor,c.Target,unarmed?CombatProfileIds.OrdinaryUnarmed:weapon.Id,s.RuleClock,request.Knockout,attack,damage,opportunity,request.PressInstruction);
            s.MeleeAttacks=s.MeleeAttacks.Concat(new[]{record}).ToArray();return null;
        }
        private static string Complete(Snapshot s,Command c,MeleeAttackRecord pending)
        {
            var r=c.Combat;
            if(r==null||c.Actor!=pending.AttackerId||c.Target!=pending.Id||r.TurnId!=s.Encounter.CurrentTurnId||c.X!=0||c.Y!=0
                ||r.WeaponId!=""||r.Stance!=0||r.Knockout!=AttackKnockoutMode.OrdinaryOutcome||r.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidKnockoutChoice";
            var before=s.Lives.Single(l=>l.ActorId==pending.TargetId);var d=pending.Damage;
            // Reconstruct the immutable continuation from its retained seed and unchanged target facts.
            // The prior rolls are verified, never applied to the world random stream a second time.
            var targetCharacter=s.Characters.Single(x=>x.ActorId==pending.TargetId);
            int constitutionSave=checked(PlaytestCharacters.AbilityModifier(targetCharacter.Abilities[2])
                +CharacterAdvancementRules.SaveProficiencyBonus(s,pending.TargetId,"CON"));
            var prior=PlaytestDamageDice.Resolve(ActorLifeRules.Read(before),d.Total,pending.At,d.EffectsSeed,constitutionSaveModifier:constitutionSave,
                critical:pending.Attack.Critical,melee:true,knockout:KnockoutInstruction.AskIfEligible);
            if(prior.Pending==null||!d.SameAs(DamageRecord(d.Dice.ToArray(),d.Total,d.DiceWords,d.EffectsSeed,prior))||s.RandomState!=prior.NextRandomState)return "InvalidPendingKnockout";
            var result=prior.Pending.Complete(r.Choice);s.RandomState=result.NextRandomState;ApplyLife(s,before,result.Outcome.State);
            var resolved=new MeleeAttackRecord(pending.Id,pending.Revision,s.Revision+1,pending.TurnOrdinal,pending.AttackerId,pending.TargetId,pending.WeaponId,pending.At,
                pending.Instruction,pending.Attack,DamageRecord(d.Dice.ToArray(),d.Total,d.DiceWords,d.EffectsSeed,result),pending.Opportunity,pending.PressInstruction);
            s.MeleeAttacks=s.MeleeAttacks.Select(a=>a.Id==pending.Id?resolved:a).ToArray();return null;
        }
        internal static void ApplyLife(Snapshot s,ActorLifeRecord before,LifeState after)
        {
```

## `engine/com.decennium.foundation/Laboratory/Model/SharedWorldRangedCombat.cs` lines 480–522

```csharp
            var combatant=s.RangedCombatants.Single(x=>x.ActorId==c.Actor);
            var targetCombatant=s.RangedCombatants.SingleOrDefault(x=>x.ActorId==c.Target);
            int targetDex=targetCombatant?.DexterityScore??s.Characters.Single(x=>x.ActorId==c.Target).Abilities[1];
            var targetStance=TestOnlyClubAttackPolicy.ActiveStance(s,c.Target);
            int armorClass=checked(CharacterAdvancementRules.ArmorClass(s,c.Target,targetDex)
                +(targetStance?.Kind==CombatStance.Aggressive?-2:targetStance?.Kind==CombatStance.Guarded?1:0)
                +CharacterAdvancementRules.DefensivePositioningBonus(s,c.Target));
            bool targetLocationKnown=rangedCombat.TargetLocationKnown
                &&(s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.LocationKnown(s,c.Actor,c.Target));
            bool lineOfFireClear=rangedCombat.LineOfFireClear
                &&(s.SchemaVersion<Snapshot.ObservationSchema||ObservationGeometry.LineOfEffectClear(s,c.Actor,c.Target));
            bool targetVisible=rangedCombat.TargetVisible&&TestOnlyClubAttackPolicy.CanSee(s,c.Actor,c.Target);
            long distance=PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(target.X,target.Y));
            if(c.Kind==CommandKind.WarningShot&&(distance>60||!targetVisible))return "WarningShotRequiresVisibleTargetWithin60Feet";
            if(c.Kind==CommandKind.CoveringFire&&(!targetLocationKnown||!targetVisible))return "CoveringFireRequiresPerceivedTarget";
            bool attackerUnseen=!TestOnlyClubAttackPolicy.CanSee(s,c.Target,c.Actor);
            bool attackerInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,c.Target,c.Actor);
            bool targetInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,c.Actor,c.Target);
            bool targetUnseenDisadvantage=!targetVisible&&!(s.SchemaVersion>=Snapshot.ObservationSchema&&targetInvisibleKnown
                &&ObservationRules.InvisibleIsOnlySightBlocker(s,c.Actor,c.Target));
            bool attackerUnseenAdvantage=attackerUnseen&&!(s.SchemaVersion>=Snapshot.ObservationSchema&&attackerInvisibleKnown
                &&ObservationRules.InvisibleIsOnlySightBlocker(s,c.Target,c.Actor));
            bool closeHostile=s.WorldSchedule.Order.Where(id=>id!=c.Actor&&!SoldierTacticalFeatures.IsAlly(s,c.Actor,id)).Any(id=>{
                var other=s.Actors.Single(a=>a.Id==id);var otherLife=s.Lives.Single(l=>l.ActorId==id);
                bool incapacitated=otherLife.Dead||otherLife.Hp==0||TestOnlyClubAttackPolicy.ConditionsFor(s,id).View().Clauses.Incapacitated;
                return PlanarCombatGeometry.CloseHostileDisadvantage(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(other.X,other.Y)),true,incapacitated,TestOnlyClubAttackPolicy.CanSee(s,id,c.Actor));
            });
            var attackerLife=s.Lives.Single(x=>x.ActorId==c.Actor);
            var incomingEffects=SoldierTacticalFeatures.ForAttack(s,c.Actor,c.Target);
            int flatAttack=checked((attackerLife.LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0)-incomingEffects.CoveringFirePenalty
                +incomingEffects.TacticalAssessmentBonus);
            var rangedFacts=new RangedAttackRequest(distance,
                RepeatingCrossbowShotRules.NormalRangeFeet,RepeatingCrossbowShotRules.MaximumRangeFeet,armorClass,
                PlaytestCharacters.AbilityModifier(combatant.DexterityScore),combatant.ProficiencyBonus,combatant.CrossbowProficient,flatAttack,
                rangedCombat.TargetCover,targetLocationKnown,targetVisible,lineOfFireClear,attackerUnseen,closeHostile,
                TestOnlyClubAttackPolicy.CombatConditions(s,c.Actor),TestOnlyClubAttackPolicy.CombatConditions(s,c.Target),
                attackerInvisibleLocationKnown:attackerInvisibleKnown,targetInvisibleLocationKnown:targetInvisibleKnown,
                additionalDisadvantageSources:incomingEffects.WarningShot?1:0,
                targetUnseenDisadvantage:targetUnseenDisadvantage,attackerUnseenAdvantage:attackerUnseenAdvantage);
            int carriedBolts=s.AmmunitionLots.Where(x=>x.CustodianId==c.Actor&&x.Accessible).Sum(x=>x.AvailableQuantity);
            var shotFailure=RepeatingCrossbowShotRules.CheckLegality(rangedFacts,new RepeatingFiveMagazine(weapon.LoadedBoltLots.Count),carriedBolts);
            if(shotFailure!=RepeatingCrossbowShotFailure.None)return ShotFailureCode(shotFailure);
            assessment.AttackFacts=rangedFacts;assessment.CarriedBolts=carriedBolts;
```

## `engine/com.decennium.foundation/Laboratory/Model/SharedOverwatchExecution.cs` lines 132–158

```csharp
            bool closeHostile=s.WorldSchedule.Order.Where(id=>id!=offer.OwnerId&&!SoldierTacticalFeatures.IsAlly(s,offer.OwnerId,id)).Any(id=>{
                var other=s.Actors.Single(a=>a.Id==id);var otherLife=s.Lives.Single(l=>l.ActorId==id);
                bool incapacitated=otherLife.Dead||otherLife.Hp==0||TestOnlyClubAttackPolicy.ConditionsFor(s,id).View().Clauses.Incapacitated;
                return PlanarCombatGeometry.CloseHostileDisadvantage(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),
                    new CombatCell(other.X,other.Y)),true,incapacitated,TestOnlyClubAttackPolicy.CanSee(s,id,offer.OwnerId));
            });
            var incomingEffects=SoldierTacticalFeatures.ForAttack(s,offer.OwnerId,offer.TargetId);
            int flatAttack=checked((s.Lives.Single(x=>x.ActorId==offer.OwnerId).LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0)
                -incomingEffects.CoveringFirePenalty+incomingEffects.TacticalAssessmentBonus);
            bool attackerInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,offer.TargetId,offer.OwnerId);
            bool targetInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,offer.OwnerId,offer.TargetId);
            bool attackerUnseen=!TestOnlyClubAttackPolicy.CanSee(s,offer.TargetId,offer.OwnerId);
            bool attackerUnseenAdvantage=attackerUnseen&&!(s.SchemaVersion>=Snapshot.ObservationSchema&&attackerInvisibleKnown
                &&ObservationRules.InvisibleIsOnlySightBlocker(s,offer.TargetId,offer.OwnerId));
            var request=new RangedAttackRequest(distance,RepeatingCrossbowShotRules.NormalRangeFeet,RepeatingCrossbowShotRules.MaximumRangeFeet,ac,
                PlaytestCharacters.AbilityModifier(attacker.DexterityScore),attacker.ProficiencyBonus,attacker.CrossbowProficient,flatAttack,
                overwatchExecution.TargetCover,overwatchExecution.TargetLocationKnown,true,overwatchExecution.LineOfFireClear,
                attackerUnseen,closeHostile,
                TestOnlyClubAttackPolicy.CombatConditions(s,offer.OwnerId),TestOnlyClubAttackPolicy.CombatConditions(s,offer.TargetId),
                attackerInvisibleLocationKnown:attackerInvisibleKnown,targetInvisibleLocationKnown:targetInvisibleKnown,
                additionalDisadvantageSources:incomingEffects.WarningShot?1:0,
                targetUnseenDisadvantage:false,attackerUnseenAdvantage:attackerUnseenAdvantage);
            var attack=RangedAttackRules.Resolve(s.RandomState,request);if(!attack.Legal)return false;
            facts=new OverwatchShotFacts{Zone=zone,Weapon=weapon,Ammunition=ammunition,Attacker=attacker,Shooter=shooter,Target=target,
                TargetLife=targetLife,Attack=attack};
            return true;
        }
```

## `engine/com.decennium.foundation/Laboratory/Model/TacticalMovementPolicy.cs` lines 197–215

```csharp
                        SetMove(s,move.Progress(move.ResponseIndex,TacticalMoveStatus.Interrupted,s.Revision+1));continue;
                    }
                    int index=move.ResponseIndex;
                    while(index<move.Reactors.Count&&!EligibleOpportunity(s,move.Reactors[index],move))index++;
                    if(index!=move.ResponseIndex){move=move.Progress(index,move.Status);SetMove(s,move);}
                    if(index<move.Reactors.Count)return;
                    long cost=StepCost(s,move.ActorId,move.ToX,move.ToY);
                    if(move.Kind==TacticalMoveKind.Ordinary) {
                        SpendMovement(s,move.ActorId,cost);
                    }
                    else if(move.Kind==TacticalMoveKind.TacticalReposition)CharacterAdvancementRules.SpendReposition(s,move.ActorId,cost);
                    var actor=s.Actors.Single(a=>a.Id==move.ActorId);actor.X=move.ToX;actor.Y=move.ToY;
                    if(s.SchemaVersion>=Snapshot.ObservationSchema)ObservationRules.Refresh(s,s.RuleClock,s.Revision+1);
                    if(cost>0)CharacterAdvancementRules.MarkMoved(s,move.ActorId);
                    s.Clubs=s.Clubs.Select(w=>w.HeldBy==actor.Id?new ClubInstance(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,w.HeldBy,actor.X,actor.Y):w).ToArray();
                    if(s.SchemaVersion>=Snapshot.OverwatchExecutionSchema)
                        s.RepeatingCrossbows=s.RepeatingCrossbows.Select(w=>w.HeldBy==actor.Id
                            ?new RepeatingCrossbowRecord(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,w.HeldBy,w.GripHands,actor.X,actor.Y,w.LoadedBoltLots.ToArray()):w).ToArray();
                    var resources=TacticalActor(s,actor.Id);
```

## `engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs` lines 405–454

```csharp
                        && (s.Work.WorkerIntervals.Any(w => w.WorkerId == activity.ActorId && w.Start < horizon && w.End > s.RuleClock)
                            || WorldActivityValidation.ActiveLaborReference(s, activity.ActorId, s.RuleClock, horizon) != "");
                    if ((active.Any(e => e.ActorId == activity.ActorId && e.Status == WorldTraversalStatus.Moving)
                        || activeOffCalendarWork) && boundary > s.RuleClock && boundary < next) next = boundary;
                    var nextWorkStart = s.Work.WorkerIntervals.Where(w => w.WorkerId == activity.ActorId
                        && w.Start > s.RuleClock && w.Start < next).Select(w => w.Start).DefaultIfEmpty(next).Min();
                    if (nextWorkStart < next) next = nextWorkStart;
                }
                foreach (var activity in s.WorldActivityIntervals.Where(x => x.DashPaid
                    && WorldActivityValidation.HasActiveLabor(s, x.ActorId, segmentStart, next)))
                    throw new InvalidOperationException("OffCalendarActionAlreadySpent");
                var activityLabor = s.WorldActivityIntervals.ToDictionary(x => x.ActorId,
                    x => WorldActivityValidation.ActiveLaborReference(s, x.ActorId, segmentStart, next), StringComparer.Ordinal);
                var observationSegments = new System.Collections.Generic.List<ObservationMovementSegment>();
                foreach (var edge in active.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                    long multiplier = CostPerFoot(s, edge); var distance = new RuleQuantity(5) - edge.DistanceFeet;
                    bool scheduled=s.WorldSchedule.Order.Contains(edge.ActorId);
                    if(scheduled||IsOffCalendarActivity(s,edge.ActorId)) {
                        var available=scheduled?Remaining(s,edge.ActorId):ActivityRemaining(s,edge.ActorId);
                        var remaining = available.Scale(1, multiplier); if (remaining < distance) distance = remaining;
                    }
                    var duration = distance.Scale(6 * multiplier, checked(Speed(s, edge.ActorId) * (edge.Running ? 2 : 1)));
                    var end = CampGreens.Add(s.RuleClock, new RuleTime(duration.Numerator, duration.Denominator)); if (end < next) next = end;
                }
                var elapsed = CampGreens.Subtract(next, s.RuleClock);
                foreach (var edge in active.Where(x => x.Status == WorldTraversalStatus.Moving)) {
                    var priorDistance = edge.DistanceFeet;
                    long multiplier = CostPerFoot(s, edge);
                    var distance = new RuleQuantity(elapsed.Numerator, elapsed.Denominator).Scale(checked(Speed(s, edge.ActorId) * (edge.Running ? 2 : 1)), 6 * multiplier);
                    bool scheduled=s.WorldSchedule.Order.Contains(edge.ActorId);
                    if(scheduled)SetInterval(s, Interval(s, edge.ActorId).Spend(distance.Scale(multiplier)));
                    else if(IsOffCalendarActivity(s,edge.ActorId))SetActivityInterval(s,ActivityInterval(s,edge.ActorId).Spend(distance.Scale(multiplier)));
                    var progress = edge.DistanceFeet + distance;
                    if (distance > default(RuleQuantity)) observationSegments.Add(new ObservationMovementSegment(edge, priorDistance, progress));
                    if(distance>default(RuleQuantity))CharacterAdvancementRules.MarkMoved(s,edge.ActorId);
                    if (progress == new RuleQuantity(5)) {
                        var actor = s.Actors.Single(a => a.Id == edge.ActorId); actor.X = edge.ToX; actor.Y = edge.ToY;
                        s.Clubs = s.Clubs.Select(c => c.HeldBy == actor.Id ? new ClubInstance(c.Id, c.ProfileId, c.OwnerId, c.CustodianId, c.HeldBy, actor.X, actor.Y) : c).ToArray();
                        s.WorldTraversals = s.WorldTraversals.Where(x => x.ActorId != actor.Id).ToArray();
                    } else SetEdge(s, edge.With(progress, edge.Status));
                }
                ObservationRules.ProcessWorldTraversalSegments(s, observationSegments, segmentStart, next, s.Revision + 1);
                // Existing procedures own crop/food/water completion and their local ordering.
                // Movement duration was bounded before their advance, so they cannot over-credit it.
                long previousSlot=s.WorldSchedule.ProcessedSlot;
                var ready = new System.Collections.Generic.List<string>();
                var repairsReady = new System.Collections.Generic.List<string>();
                var manufacturingReady = new System.Collections.Generic.List<string>();
                if(connectedCombat==null) {
                    if(harvestFixture!=null||miningFixture!=null||prospectingFixture!=null)OrdinaryInventory.AdvanceTo(s,next,world=>{
```

## `engine/com.decennium.foundation/Laboratory/Model/TestOnlySharedWorldPolicy.cs` lines 503–535

```csharp
                    var job=s.RepairWork.Single(x=>x.Id==id);
                    if(RepairAccess(s,job.WorkerId,job.TargetId,false)==null)FinishRepair(s,job);
                }
                foreach(string id in manufacturingReady){
                    var job=s.ManufacturingOrders.Single(x=>x.Id==id);
                    if(ManufacturingAccess(s,job.WorkerId,false,true,job.RecipeId)==null)FinishManufacturingCheck(s,job);
                }
                PauseIncompatibleWork(s); CompleteSupplyCacheAttempts(s); CompleteOrdinaryReceptacleAttempts(s); ReconcileTraversal(s);
                ObservationRules.Refresh(s, s.RuleClock, s.Revision + 1);
                if(ManufacturingChoicePending(s)){
                    TestOnlyClubAttackPolicy.AdvanceConditions(s,".clock-final",true);
                    s.ManufacturingAdvance=continuation??new ManufacturingAdvanceRecord(target,exitAfterSlot,initiating.Id,s.Revision+1,
                        initiating.Kind==CommandKind.EndRegularTurn||initiating.Kind==CommandKind.EndFixedEncounter?initiating.Target:"");
                    if(connectedCombat!=null)ObserveCalendar(s);return;
                }
            }
            TestOnlyClubAttackPolicy.AdvanceConditions(s,".clock-final",true);
            if(connectedCombat!=null)ObserveCalendar(s);
        }
        private string ResolveCore(Snapshot s, Command c)
        {
            if (!s.Actors.Any(a => a.Id == c.Actor)) return "UnknownWorldActor";
            if (c.Kind == CommandKind.Hide || c.Kind == CommandKind.Search) return ResolveObservationAction(s, c);
            if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c)) {
                var activity = ActivityInterval(s, c.Actor);
                if (activity.Action == WorldActionCommitment.Dash
                    || activity.Action == WorldActionCommitment.ActiveLabor && !CanContinueActivityLabor(s, c.Actor))
                    return "OffCalendarActionAlreadySpent";
            }
            if((c.Kind==CommandKind.RespondOverwatch||c.Kind==CommandKind.ResolveOverwatchRider)&&(connectedCombat==null||!s.InventoryCombat))
                return "OverwatchRequiresTacticalCombat";
            if(c.Kind==CommandKind.AwardCharacterMilestone||c.Kind==CommandKind.AdvanceCharacterLevel)return ResolveCharacterAdvancement(s,c);
            if(PeriodicEventCommand(c.Kind))return ResolvePeriodicEvent(s,c);
```

## `engine/com.decennium.foundation/Runtime/Core/Simulation.cs` lines 92–107

```csharp
        public const int HarvestSchema = 41;
        public const int HarvestManifestSchema = 42;
        public const int MiningSchema = 43;
        public const int ProspectingSchema = 44;
        public const int MiningAssaySchema = 45;
        public const int DestructiveMiningAssaySchema = 46;
        public const int MiningExpeditionAssignmentSchema = 47;
        public const int MineralPreparationSchema = 48;
        public const int MiningToolCandidateSchema = 49;
        public const int OrdinaryReceptacleSchema = 50;
        public const int ObservationSchema = 51;
        public const int MaxActors = 64;
        public const int MaxCropBatches = 8;
        public const int MaxCropWorkRecords = 128;
        // Technical bound keeps the entire snapshot within the existing 1 MiB save limit,
        // including maximum-length identities and a full receipt history. Not a game rule.
```

## `engine/com.decennium.foundation/Runtime/Persistence/SnapshotCodec.cs` lines 72–95

```csharp
                if (state.SchemaVersion >= Snapshot.CharacterAdvancementSchema) CharacterAdvancementCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.RepeatingCrossbowSchema) RangedCombatCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.PeriodicRiderSchema) PeriodicRiderCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OverwatchSchema) OverwatchCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OverwatchExecutionSchema) OverwatchExecutionCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.SoldierInitialBuildSchema) CharacterAdvancementCodec.WriteInitialBuild(writer,state);
                if (state.SchemaVersion >= Snapshot.SoldierTacticalTechniquesSchema) SoldierTacticalFeatureCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.FishingTrapLegacySchema) FishingTrapCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.ExpeditionAssignmentSchema) ExpeditionAssignmentCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OffCalendarActivitySchema) WorldActivityCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.HarvestSchema) HarvestCodec.Write(writer, state, state.SchemaVersion);
                if (state.SchemaVersion >= Snapshot.MiningSchema) MiningCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.ProspectingSchema) ProspectingCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.MiningAssaySchema) MiningAssayCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.DestructiveMiningAssaySchema) DestructiveMiningAssayCodec.Write(writer, state);
                if (state.SchemaVersion >= Snapshot.MineralPreparationSchema) MineralPreparationCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.MiningToolCandidateSchema) MiningToolCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.OrdinaryReceptacleSchema) OrdinaryReceptacleCodec.Write(writer,state);
                if (state.SchemaVersion >= Snapshot.ObservationSchema) ObservationCodec.Write(writer,state);
                writer.Flush(); payload = stream.ToArray();
            }
            if (payload.Length + 32 > Limit(state.SchemaVersion)) throw new InvalidDataException("Save exceeds schema size limit.");
            using (var hash = SHA256.Create()) return payload.Concat(hash.ComputeHash(payload)).ToArray();
        }
```

## `engine/com.decennium.foundation/Runtime/Persistence/SnapshotCodec.cs` lines 166–188

```csharp
                    if(schema >= Snapshot.PeriodicRiderSchema)PeriodicRiderCodec.Read(reader,s);
                    if(schema >= Snapshot.OverwatchSchema)OverwatchCodec.Read(reader,s);
                    if(schema >= Snapshot.OverwatchExecutionSchema)OverwatchExecutionCodec.Read(reader,s);
                    if(schema >= Snapshot.SoldierInitialBuildSchema)CharacterAdvancementCodec.ReadInitialBuild(reader,s);
                    if(schema >= Snapshot.SoldierTacticalTechniquesSchema)SoldierTacticalFeatureCodec.Read(reader,s);
                    if(schema >= Snapshot.FishingTrapLegacySchema)FishingTrapCodec.Read(reader,s,schema);
                    if(schema >= Snapshot.ExpeditionAssignmentSchema)ExpeditionAssignmentCodec.Read(reader,s);
                    if(schema >= Snapshot.OffCalendarActivitySchema)WorldActivityCodec.Read(reader,s);
                    if(schema >= Snapshot.HarvestSchema)HarvestCodec.Read(reader,s,schema);
                    if(schema >= Snapshot.MiningSchema)MiningCodec.Read(reader,s);
                    if(schema >= Snapshot.ProspectingSchema)ProspectingCodec.Read(reader,s);
                    if(schema >= Snapshot.MiningAssaySchema)MiningAssayCodec.Read(reader,s);
                    if(schema >= Snapshot.DestructiveMiningAssaySchema)DestructiveMiningAssayCodec.Read(reader,s);
                    if(schema >= Snapshot.MineralPreparationSchema)MineralPreparationCodec.Read(reader,s);
                    if(schema >= Snapshot.MiningToolCandidateSchema)MiningToolCodec.Read(reader,s);
                    if(schema >= Snapshot.OrdinaryReceptacleSchema)OrdinaryReceptacleCodec.Read(reader,s);
                    if(schema >= Snapshot.ObservationSchema)ObservationCodec.Read(reader,s);
                    if (stream.Position != length) throw new InvalidDataException("Unexpected trailing save data.");
                    Validation.Snapshot(s); return s;
                }
            }
            catch (Exception ex) when (ex is ArgumentException || ex is EndOfStreamException || ex is OverflowException)
            { throw new InvalidDataException("Malformed save.", ex); }
```
