#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>A detection observation contains no underlying effect, spell, rank, owner or source identity.</summary>
    public sealed class ExpeditionMagicAuraView
    {
        public string ObservationId { get; }
        public int X { get; }
        public int Y { get; }
        public bool Focused { get; }
        public string SchoolCategory { get; }
        internal ExpeditionMagicAuraView(string id,int x,int y,bool focused,string category)
        {ObservationId=id;X=x;Y=y;Focused=focused;SchoolCategory=category;}
    }
    public sealed class ExpeditionGuidanceBenefitView
    {
        public string EffectId { get; }
        public RuleTime ExpiresAt { get; }
        internal ExpeditionGuidanceBenefitView(SpellEffectRecord effect){EffectId=effect.Id;ExpiresAt=effect.ExpiresAt;}
    }
    public sealed class ExpeditionCastingView
    {
        public bool TestOnly => true;
        public bool ProductionAuthority => false;
        public bool CastingAdapterSupported { get; }
        public string ExecutionAvailability => "Target-specific command query required";
        public int? Dissonance { get; }
        public int? DissonanceLimit { get; }
        public string LastSpellId { get; }
        public int? Refrain { get; }
        public string ConcentrationEffectId { get; }
        public string ConcentrationSpellId { get; }
        public RuleTime? ConcentrationExpiresAt { get; }
        public IReadOnlyList<ExpeditionGuidanceBenefitView> GuidanceBenefits { get; }
        public IReadOnlyList<ExpeditionMagicAuraView> Auras { get; }
        public IReadOnlyList<string> UnsupportedCapabilities => Unsupported;
        internal static readonly IReadOnlyList<string> Unsupported=Array.AsReadOnly(new[]{
            "Other spells, classes, ranks, upcasting, spell preparation and replacement",
            "Casting before actual reinforcement or outside the owned regular Action",
            "Ordinary Counterspell, nested counters and readied spells",
            "Guidance outside tactical Hide, Search and existing Medicine stabilization",
            "Other sensory casting, nonparty willingness and unbound focus variants or storage",
            "New contamination acquisition, hazardous mixing, splitting and propagation",
            "Dormant or item magic, anti-divination and school-protection producers",
            "Retune, meditation, long-rest RP recovery and spendable Conviction venting",
            "Production authority"});
        internal ExpeditionCastingView(Snapshot state,string actor,IEnumerable<ExpeditionMagicAuraView> auras)
        {
            CastingAdapterSupported=actor==ClericRpProfile.Actor;
            var strain=state.CastingStrain.SingleOrDefault(x=>x.ActorId==actor);
            Dissonance=strain?.Dissonance;LastSpellId=strain?.LastSpellId??"";Refrain=strain?.Refrain;
            if(strain!=null) {
                var facts=CharacterRuleFacts.ForActor(state,actor);
                DissonanceLimit=CastingStrainRecord.Limit(facts.ProficiencyBonus,facts.AbilityModifier(CharacterAbility.Wisdom));
            }
            var concentration=state.SpellEffects.SingleOrDefault(x=>x.Present&&x.RequiresConcentration&&x.CasterId==actor);
            ConcentrationEffectId=concentration?.Id??"";ConcentrationSpellId=concentration?.SpellId??"";
            ConcentrationExpiresAt=concentration?.ExpiresAt;
            GuidanceBenefits=Array.AsReadOnly(state.SpellEffects.Where(x=>x.Present&&x.SpellId=="guidance"&&x.TargetId==actor&&x.ExpiresAt>state.RuleClock)
                .Select(x=>new ExpeditionGuidanceBenefitView(x)).ToArray());
            Auras=Array.AsReadOnly(auras.ToArray());
        }
    }
}
#endif
