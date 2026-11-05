#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>An exact source component occurrence. Divisibility is an explicit execution-profile
    /// fact; role, name, category, price and weight never imply it.</summary>
    public sealed class ManufacturingComponentDefinition
    {
        public string Id { get; }
        public int Quantity { get; }
        public RuleQuantity UnitMass { get; }
        public bool Consumed { get; }
        public bool Catalyst { get; }
        public bool Divisible { get; }
        public ManufacturingComponentDefinition(string id,int quantity,RuleQuantity unitMass,bool consumed,bool catalyst,bool divisible)
        {
            if(!Validation.ValidId(id)||quantity<1||unitMass<=default(RuleQuantity)||!consumed)
                throw new ArgumentException("Invalid manufacturing component definition.");
            Id=id;Quantity=quantity;UnitMass=unitMass;Consumed=consumed;Catalyst=catalyst;Divisible=divisible;
        }
    }

    /// <summary>Immutable, bounded source profile for one operational Alchemy recipe.</summary>
    public sealed class ManufacturingRecipeDefinition
    {
        private readonly ManufacturingComponentDefinition[] components;
        public string Id { get; }
        public int SkillLevel { get; }
        public int Difficulty { get; }
        public long MinimumResearchHours { get; }
        public RuleTime FirstPhase { get; }
        public RuleTime RemainingPhase { get; }
        public int StandardYield { get; }
        public int SourceVesselComponentIndex { get; }
        public int SourceVesselCount => SourceVesselComponentIndex < 0 ? 0 : components[SourceVesselComponentIndex].Quantity;
        public int MinimumSupplementaryVials => Math.Max(0,StandardYield-SourceVesselCount);
        public int MaximumSupplementaryVials => Math.Max(0,ManufacturingRules.Yield(CraftQuality.Masterwork,StandardYield,CraftQualityChoice.FullYield)-SourceVesselCount);
        public RuleQuantity ProductCompoundMass { get; }
        public IReadOnlyList<ManufacturingComponentDefinition> Components { get; }

        internal ManufacturingRecipeDefinition(string id,int skillLevel,int difficulty,long minimumResearchHours,RuleTime firstPhase,
            RuleTime remainingPhase,int standardYield,int sourceVesselComponentIndex,RuleQuantity productCompoundMass,
            IEnumerable<ManufacturingComponentDefinition> components)
        {
            this.components=(components??Array.Empty<ManufacturingComponentDefinition>()).ToArray();
            if(!Validation.ValidId(id)||skillLevel<1||skillLevel>20||difficulty<1||difficulty>100||minimumResearchHours<0
                ||firstPhase<=default(RuleTime)||remainingPhase<=default(RuleTime)||standardYield<1||this.components.Length<1||this.components.Length>8
                ||this.components.Any(x=>x==null)||this.components.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=this.components.Length
                ||sourceVesselComponentIndex < -1||sourceVesselComponentIndex>=this.components.Length||productCompoundMass<=default(RuleQuantity))
                throw new ArgumentException("Invalid manufacturing recipe definition.");
            Id=id;SkillLevel=skillLevel;Difficulty=difficulty;MinimumResearchHours=minimumResearchHours;FirstPhase=firstPhase;
            RemainingPhase=remainingPhase;StandardYield=standardYield;SourceVesselComponentIndex=sourceVesselComponentIndex;
            ProductCompoundMass=productCompoundMass;Components=Array.AsReadOnly(this.components);
        }
        public RuleQuantity NonVesselMass
        {
            get { RuleQuantity total=default;for(int i=0;i<components.Length;i++)if(i!=SourceVesselComponentIndex)total+=components[i].UnitMass.Scale(components[i].Quantity);return total; }
        }
        public IEnumerable<int> CatalystIndexes => Enumerable.Range(0,components.Length).Where(i=>components[i].Catalyst);
        public bool CanYield(CraftQuality quality,int reservedSupplementaryVials,int retainedCatalyst)
        {
            int yield=ManufacturingRules.Yield(quality,StandardYield,CraftQualityChoice.FullYield);
            if(yield>SourceVesselCount+reservedSupplementaryVials)return false;
            RuleQuantity compound=NonVesselMass;
            if(retainedCatalyst>=0){if(retainedCatalyst>=components.Length||!components[retainedCatalyst].Catalyst)return false;compound-=components[retainedCatalyst].UnitMass;}
            return ProductCompoundMass.Scale(yield)<=compound;
        }
    }

    public static class ManufacturingRules
    {
        public const string Recipe4Id="recipe-4",Recipe14Id="recipe-14";
        private static readonly ManufacturingRecipeDefinition Recipe4Definition=new ManufacturingRecipeDefinition(Recipe4Id,5,8,0,
            new RuleTime(900),new RuleTime(13500),5,1,new RuleQuantity(1,10),new[]{
                new ManufacturingComponentDefinition("ing-4-0-alchemical_catalyst",5,new RuleQuantity(1,10),true,true,true),
                new ManufacturingComponentDefinition("ing-4-1-crystal_vial",5,new RuleQuantity(1,10),true,false,false),
                new ManufacturingComponentDefinition("ing-4-2-alchemical_base",5,new RuleQuantity(1,10),true,false,true),
                new ManufacturingComponentDefinition("drop-black_blood_sample",1,new RuleQuantity(38,100),true,true,true)});
        private static readonly ManufacturingRecipeDefinition Recipe14Definition=new ManufacturingRecipeDefinition(Recipe14Id,5,11,0,
            new RuleTime(900),new RuleTime(13500),4,-1,new RuleQuantity(1,10),new[]{
                new ManufacturingComponentDefinition("ing-14-0-stabilizing_salts",5,new RuleQuantity(5,100),true,false,true),
                new ManufacturingComponentDefinition("ing-14-1-distilled_spirits",2,new RuleQuantity(1,2),true,false,true),
                new ManufacturingComponentDefinition("drop-black_blood_sample",1,new RuleQuantity(38,100),true,true,false)});
        public static ManufacturingRecipeDefinition Recipe(string recipeId)
            =>recipeId==Recipe4Id?Recipe4Definition:recipeId==Recipe14Id?Recipe14Definition:null;

        public static CraftQuality Quality(int natural, int modifier, int dc, bool takeTen = false)
        {
            if (natural < 1 || natural > 20 || takeTen && natural != 10) throw new ArgumentException("Invalid crafting die.");
            long margin = (long)natural + modifier - dc;
            return !takeTen && natural == 1 || margin <= -10 ? CraftQuality.Mishap : margin < -4 ? CraftQuality.Failed
                : margin < 0 ? CraftQuality.Flawed : margin < 5 ? CraftQuality.Standard : margin < 10 ? CraftQuality.Exceptional : CraftQuality.Masterwork;
        }
        public static bool Eligible(int tradeLevel, int skill, bool toolTrained, bool hasFormula, bool formulaRequired)
        {
            if (tradeLevel < 0 || tradeLevel > 20 || skill < 1 || skill > 20) throw new ArgumentException("Invalid trade level.");
            int effective = toolTrained ? tradeLevel : 0;
            return skill <= (effective == 0 ? 4 : Math.Max(4, effective)) && (!formulaRequired || hasFormula);
        }
        public static bool CanTakeTen(int tradeLevel, int skill, bool trained, bool safeSuitableWorkshop, bool disadvantage)
            => trained && tradeLevel - skill >= 5 && safeSuitableWorkshop && !disadvantage;
        public static int Yield(CraftQuality quality, int standard, CraftQualityChoice choice)
        {
            if (standard < 1 || !Enum.IsDefined(typeof(CraftQuality),quality) || quality == CraftQuality.None || !Enum.IsDefined(typeof(CraftQualityChoice),choice)) throw new ArgumentException("Invalid crafting yield.");
            if (quality == CraftQuality.Mishap || quality == CraftQuality.Failed) return 0;
            if (quality == CraftQuality.Flawed) return standard >= 2 ? standard / 2 : 0; // Caller must supply a reviewed singleton flaw profile.
            return choice == CraftQualityChoice.FullYield ? quality == CraftQuality.Masterwork ? checked((int)((long)standard * 3 / 2))
                : quality == CraftQuality.Exceptional ? checked((int)((long)standard * 5 / 4)) : standard : standard;
        }
        public static RuleQuantity FailureRecovery(RuleQuantity amount, bool consumed, bool catalyst, bool divisible)
        {
            if (!consumed) return amount;
            if (catalyst) return default;
            long scale = divisible ? 100 : 1;
            var units = ((BigInteger)amount.Numerator * scale) / ((BigInteger)amount.Denominator * 4);
            return RuleQuantity.FromFraction(units, scale);
        }
        public static int TradeAward(CraftQuality quality, int level, int recipeSkill, int trivialAt, bool trained,
            bool priorSuccess, bool priorFindingAtLevel, bool realInputsAndLabor, bool usableFinding, int mishap)
        {
            if (!trained || level >= trivialAt) return 0;
            if (quality >= CraftQuality.Standard) return priorSuccess ? 2 : 4;
            return quality != CraftQuality.None && recipeSkill >= level && !priorFindingAtLevel && realInputsAndLabor && usableFinding && mishap != 6 ? 1 : 0;
        }
        public static (int Level, int Xp) AdvanceTrade(int level, int xp, int award)
        {
            if (level < 1 || level > 20 || xp < 0 || award < 0) throw new ArgumentException("Invalid trade progression.");
            xp = checked(xp + award);
            while (level < 20 && xp >= 10 + level) { xp -= 10 + level; level++; }
            return (level, xp);
        }
        // Compatibility accessors for the pre-existing recipe-4 fixture and its pinned cases.
        public static readonly System.Collections.Generic.IReadOnlyList<string> Recipe4Components = Array.AsReadOnly(new[] { "ing-4-0-alchemical_catalyst", "ing-4-1-crystal_vial", "ing-4-2-alchemical_base", "drop-black_blood_sample" });
        public static readonly System.Collections.Generic.IReadOnlyList<int> Recipe4Amounts = Array.AsReadOnly(new[] { 5, 5, 5, 1 });
        public static RuleQuantity Recipe4Mass(int component) => component == 3 ? new RuleQuantity(38,100) : new RuleQuantity(1,10);
        public static bool Recipe4Catalyst(int component) => component == 0 || component == 3;
        public static bool Recipe4Divisible(int component) => component != 1;
        public static RuleQuantity Recipe4CompoundMass(int retainedCatalyst)
            => new RuleQuantity(138,100) - (retainedCatalyst < 0 ? default : Recipe4Mass(retainedCatalyst));
        public static bool Recipe4CanYield(CraftQuality quality, int reservedExtraVials, int retainedCatalyst)
        {
            return Recipe4Definition.CanYield(quality,reservedExtraVials,retainedCatalyst);
        }
    }
}
#endif
