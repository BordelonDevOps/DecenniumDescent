using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation
{
    public sealed class SpellClassAccess
    {
        public string ClassName { get; }
        public string School { get; }
        public int Rank { get; }
        public int MinimumClassLevel { get; }
        public int BaseRpCost { get; }
        internal SpellClassAccess(string name, string school, int rank, int minimum, int cost)
        { ClassName = name; School = school; Rank = rank; MinimumClassLevel = minimum; BaseRpCost = cost; }
    }

    public sealed class SpellSourcePlacement
    {
        public string School { get; }
        public int Rank { get; }
        public string Summary { get; }
        internal SpellSourcePlacement(string school, int rank, string summary)
        { School = school; Rank = rank; Summary = summary; }
    }

    /// <summary>Immutable source binding, not executable casting authority or a caller-supplied definition.</summary>
    public sealed class SpellSourceDefinition
    {
        public string Id { get; }
        public string Name { get; }
        public string WholeCardPointer { get; }
        public string ProcedurePointer => WholeCardPointer + "/operational";
        public string WholeCardSha256 { get; }
        public string ProcedureSha256 { get; }
        public string OriginalRecordSha256 { get; }
        public string AuthoredReviewSha256 { get; }
        public string SourceRevision => SpellSourceCatalog.SourceRevision;
        public string SourceStatus => "operational-playtest-draft";
        public string AuthoredStatus => "reviewed-authored-operational-playtest";
        public bool CastingSupported => false;
        public int AdditionalRpCost { get; }
        public ReadOnlyCollection<SpellClassAccess> ClassAccess { get; }
        public ReadOnlyCollection<SpellSourcePlacement> Placements { get; }
        internal SpellSourceDefinition(string id, string name, string pointer, string cardHash, string procedureHash,
            string originalHash, string reviewHash, int additionalCost, SpellClassAccess[] access, SpellSourcePlacement[] placements)
        {
            Id = id; Name = name; WholeCardPointer = pointer; WholeCardSha256 = cardHash; ProcedureSha256 = procedureHash;
            OriginalRecordSha256 = originalHash; AuthoredReviewSha256 = reviewHash; AdditionalRpCost = additionalCost;
            ClassAccess = Array.AsReadOnly(access.ToArray()); Placements = Array.AsReadOnly(placements.ToArray());
        }
        public SpellClassAccess AccessFor(string className) => ClassAccess.SingleOrDefault(x => x.ClassName == className);
    }

    public enum SpellAcquisitionOrigin { InitialClassRepertoire, EarnedClassLevel }

    /// <summary>Knowledge only. Resources, class cards, effects, preparation and inventory stay in their own shared ledgers.</summary>
    public sealed class KnownSpellRecord
    {
        public string ActorId { get; }
        public string ClassName { get; }
        public string SpellId { get; }
        public string SourceRevision { get; }
        public string WholeCardSha256 { get; }
        public string ProcedureSha256 { get; }
        public string School { get; }
        public int Rank { get; }
        public SpellAcquisitionOrigin Origin { get; }
        public int ClassLevel { get; }
        public int LevelOrdinal { get; }
        public string EntitlementId { get; }
        public string MilestoneId { get; }
        public long AcquiredRevision { get; }
        public KnownSpellRecord(string actor, string className, string spell, string sourceRevision, string wholeCardHash,
            string procedureHash, string school, int rank, SpellAcquisitionOrigin origin, int classLevel, int levelOrdinal,
            string entitlement, string milestone, long revision)
        {
            if (!Validation.ValidId(actor) || !Validation.ValidId(className) || !Validation.ValidId(spell)
                || sourceRevision == null || sourceRevision.Length != 40 || wholeCardHash == null || wholeCardHash.Length != 64
                || procedureHash == null || procedureHash.Length != 64 || !Validation.ValidId(school) || rank < 0 || rank > 9
                || !Enum.IsDefined(typeof(SpellAcquisitionOrigin), origin) || classLevel < 1 || classLevel > 20
                || levelOrdinal < classLevel || levelOrdinal > 20 || !Validation.ValidId(entitlement)
                || origin == SpellAcquisitionOrigin.InitialClassRepertoire && (milestone != "" || revision != 0)
                || origin == SpellAcquisitionOrigin.EarnedClassLevel && (!Validation.ValidId(milestone) || revision < 1))
                throw new ArgumentException("Invalid spell acquisition provenance.");
            ActorId = actor; ClassName = className; SpellId = spell; SourceRevision = sourceRevision;
            WholeCardSha256 = wholeCardHash; ProcedureSha256 = procedureHash; School = school; Rank = rank;
            Origin = origin; ClassLevel = classLevel; LevelOrdinal = levelOrdinal; EntitlementId = entitlement;
            MilestoneId = milestone; AcquiredRevision = revision;
        }
        public static KnownSpellRecord FromSource(string actor, string spell, SpellAcquisitionOrigin origin, int classLevel,
            int levelOrdinal, string entitlement, string milestone = "", long revision = 0)
        {
            var definition = SpellSourceCatalog.Get(spell) ?? throw new ArgumentException("SpellSourceAdmissionUnsupported");
            var access = definition.AccessFor("Cleric");
            return new KnownSpellRecord(actor, "Cleric", spell, definition.SourceRevision, definition.WholeCardSha256,
                definition.ProcedureSha256, access.School, access.Rank, origin, classLevel, levelOrdinal, entitlement, milestone, revision);
        }
        public bool MatchesSource()
        {
            var definition = SpellSourceCatalog.Get(SpellId); var access = definition?.AccessFor(ClassName);
            return access != null && SourceRevision == definition.SourceRevision && WholeCardSha256 == definition.WholeCardSha256
                && ProcedureSha256 == definition.ProcedureSha256 && School == access.School && Rank == access.Rank
                && ClassLevel >= access.MinimumClassLevel;
        }
    }

    public static class ClericRepertoireProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.cleric-repertoire-v1-";
        public const byte Marker = 11;
        public const string InitialEntitlement = "cleric.repertoire.initial1";
        public const string EarnedEntitlement = "cleric.repertoire.earned2";
        public const string FutureChoice = "detect-magic";
        public static IReadOnlyList<string> InitialSpells { get; } = Array.AsReadOnly(new[] {
            "arcane-ward", "guidance", "purify-food-and-drink", "sanctuary", "spare-the-dying" });
        public static bool SelectedFingerprint(string value) => value != null
            && (value.StartsWith(FingerprintPrefix, StringComparison.Ordinal) || FrightenedProfile.SelectedFingerprint(value));
        public static bool IsCommand(CommandKind kind) => kind == CommandKind.CastKnownSpell || kind == CommandKind.AcquireEarnedSpell;

        // These denials are shared by the read-only query and actual command resolver, including rank-zero casts.
        public static string CommandFailure(Snapshot state, Command command)
        {
            if (!state.ConnectedClericRepertoire || command.Actor != ClericRpProfile.Actor) return "SpellRepertoireUnavailable";
            return command.Kind == CommandKind.CastKnownSpell ? "OrdinarySpellcastingUnsupported"
                : state.ConnectedClericSettlement ? "EarnedSpellAcquisitionRequiresAdvancementTransaction" : "ClericEarnedAdvancementUnavailable";
        }

        public static string AssessChoice(string spell, int actualClericLevel, bool bishop = false)
        {
            if (actualClericLevel < 1 || actualClericLevel > (bishop?3:2)) return "ClericRepertoireLevelUnsupported";
            // Retain the distinct source boundaries, without admitting these controls into the supported catalog.
            if (spell == "flare-spark") return "SpellClassAccessDenied";
            if (spell == BishopProfile.Dispel && (!bishop || actualClericLevel<3)) return "SpellClassLevelDenied";
            if (spell == "light") return "SpellSourceAdmissionUnsupported";
            var definition = SpellSourceCatalog.Get(spell);
            if (definition == null) return "SpellSourceAdmissionUnsupported";
            var access = definition.AccessFor("Cleric");
            if (access == null) return "SpellClassAccessDenied";
            return access.MinimumClassLevel > actualClericLevel || access.Rank > (bishop?2:1) ? "SpellClassLevelDenied" : null;
        }

        public static string ValidateInitialChoices(IEnumerable<string> choices)
        {
            if (choices == null) return "InitialRepertoireRequired";
            var ids = choices.ToArray();
            if (ids.Length != 5 || ids.Distinct(StringComparer.Ordinal).Count() != 5) return "InitialRepertoireCountOrIdentity";
            foreach (string id in ids) { string failure = AssessChoice(id, 1); if (failure != null) return failure; }
            if (ids.Count(x => SpellSourceCatalog.Get(x).AccessFor("Cleric").Rank == 0) != 3
                || ids.Count(x => SpellSourceCatalog.Get(x).AccessFor("Cleric").Rank == 1) != 2) return "InitialRepertoireRankCounts";
            return ids.OrderBy(x => x, StringComparer.Ordinal).SequenceEqual(InitialSpells, StringComparer.Ordinal)
                ? null : "InitialRepertoireSelectionUnsupported";
        }

        internal static void Validate(Snapshot state)
        {
            bool selected = SelectedFingerprint(state.ContentFingerprint);
            if (state.KnownSpells == null || state.KnownSpells.Any(x => x == null) || state.ConnectedClericRepertoire != selected
                || !selected && state.KnownSpells.Length != 0) throw new ArgumentException("Invalid repertoire envelope.");
            if (!selected) return;
            bool earned = state.ConnectedClericSettlement && state.ClericInvocationPath != null;
            var initial = state.KnownSpells.Where(x => x.Origin == SpellAcquisitionOrigin.InitialClassRepertoire).ToArray();
            if (!state.TestOnly || !state.ConnectedClericRp || state.SchemaVersion != Snapshot.SurpriseEntrySchema
                || state.KnownSpells.Length != (BishopProfile.Earned(state) ? 7 : earned ? 6 : 5) || initial.Length != 5 || ValidateInitialChoices(initial.Select(x => x.SpellId)) != null
                || state.InitialClassSelections.Count(x => ClericRpProfile.ValidInitialSelection(state, x)) != 1
                || initial.Any(x => x.ActorId != ClericRpProfile.Actor || x.ClassName != "Cleric" || !x.MatchesSource()
                    || x.Origin != SpellAcquisitionOrigin.InitialClassRepertoire || x.ClassLevel != 1 || x.LevelOrdinal != 1
                    || x.EntitlementId != InitialEntitlement || x.MilestoneId != "" || x.AcquiredRevision != 0))
                throw new ArgumentException("Invalid connected initial Cleric repertoire. Earned ownership requires a later profile.");
            if (earned && state.KnownSpells.Count(x => x.ActorId == ClericRpProfile.Actor && x.ClassName == "Cleric"
                && x.Origin == SpellAcquisitionOrigin.EarnedClassLevel && x.SpellId == FutureChoice && x.MatchesSource()
                && x.ClassLevel == 2 && x.LevelOrdinal == 2 && x.EntitlementId == EarnedEntitlement
                && x.MilestoneId == state.ClericInvocationPath.MilestoneId && x.AcquiredRevision == state.ClericInvocationPath.AcquiredRevision) != 1)
                throw new ArgumentException("Invalid earned Cleric repertoire provenance.");
            if(BishopProfile.Earned(state)) {
                var a=BishopProfile.Advancement(state);
                if(state.KnownSpells.Count(x=>x.SpellId==BishopProfile.Dispel && x.ActorId==ClericRpProfile.Actor && x.ClassName=="Cleric"
                    && x.MatchesSource() && x.Origin==SpellAcquisitionOrigin.EarnedClassLevel && x.ClassLevel==3 && x.LevelOrdinal==3
                    && x.EntitlementId==BishopProfile.RepertoireEntitlement && x.MilestoneId==BishopProfile.Milestone && x.AcquiredRevision==a.Revision)!=1)
                    throw new ArgumentException("Invalid earned Bishop repertoire provenance.");
            }
        }
    }
}
