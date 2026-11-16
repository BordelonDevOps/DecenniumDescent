#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed class ExpeditionKnownSpellView
    {
        public string Id { get; }
        public string Name { get; }
        public string CastingClass { get; }
        public string School { get; }
        public int Rank { get; }
        public string SourceRevision { get; }
        public string SourcePointer { get; }
        public string ProcedureSha256 { get; }
        public SpellAcquisitionOrigin Origin { get; }
        public int AcquiredClassLevel { get; }
        public long AcquiredRevision { get; }
        public bool Known => true;
        public bool CastingSupported { get; }
        internal ExpeditionKnownSpellView(KnownSpellRecord owned,bool selectedCasting=false,bool bishop=false)
        {
            CastingSupported=selectedCasting&&SpellCastingProfile.IsAdmittedSpell(owned.SpellId,bishop);
            var source = SpellSourceCatalog.Get(owned.SpellId);
            Id = owned.SpellId; Name = source.Name; CastingClass = owned.ClassName; School = owned.School; Rank = owned.Rank;
            SourceRevision = owned.SourceRevision; SourcePointer = SpellSourceCatalog.CatalogPath + "#" + source.WholeCardPointer;
            ProcedureSha256 = owned.ProcedureSha256; Origin = owned.Origin; AcquiredClassLevel = owned.ClassLevel;
            AcquiredRevision = owned.AcquiredRevision;
        }
    }
    public sealed class ExpeditionRepertoireView
    {
        public IReadOnlyList<ExpeditionKnownSpellView> KnownSpells { get; }
        public string FutureEarnedChoice => ClericRepertoireProfile.FutureChoice;
        public bool FutureChoiceOwned { get; }
        public string FutureChoiceRequirement => "Actual Cleric 2 advancement and its earned ranked selection";
        public IReadOnlyList<string> UnsupportedCapabilities { get; } = Array.AsReadOnly(new[] {
            "Ordinary spellcasting, including cantrips", "Earned acquisition before Cleric advancement",
            "Other spell acquisition", "Preparation, spellbooks, replacement and respec", "Multiclass repertoire" });
        internal ExpeditionRepertoireView(Snapshot state, string actor)
        {
            if(state.ConnectedClericCasting)UnsupportedCapabilities=ExpeditionCastingView.UnsupportedFor(state);
            FutureChoiceOwned = state.KnownSpells.Any(x => x.ActorId == actor && x.SpellId == ClericRepertoireProfile.FutureChoice);
            KnownSpells = Array.AsReadOnly(state.KnownSpells.Where(x => x.ActorId == actor)
                .OrderBy(x => x.SpellId, StringComparer.Ordinal).Select(x => new ExpeditionKnownSpellView(x,state.ConnectedClericCasting,state.BishopEntry!=null)).ToArray());
        }
    }
}
#endif
