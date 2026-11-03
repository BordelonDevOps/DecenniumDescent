#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public enum CarrierSize { Tiny, Small, Medium, Large }
    public sealed class CarryLimits
    {
        public RuleQuantity Pounds { get; }
        public RuleQuantity PushDragLiftPounds { get; }
        public RuleQuantity Load { get; }
        public RuleQuantity CasualtyLoad { get; }
        internal CarryLimits(RuleQuantity pounds,RuleQuantity load,RuleQuantity casualty)
        {Pounds=pounds;PushDragLiftPounds=pounds.Scale(2);Load=load;CasualtyLoad=casualty;}
    }
    /// <summary>Totals for actual physical objects. Each inclusive list names the exact descendant objects covered, independently by unit.</summary>
    public sealed class BurdenItem
    {
        public string Id { get; }
        public string ParentId { get; }
        public RuleQuantity? DocumentedPounds { get; }
        public RuleQuantity? PrintedLoad { get; }
        public IReadOnlyList<string> PoundsIncludes { get; }
        public IReadOnlyList<string> LoadIncludes { get; }
        public BurdenItem(string id,string parentId,RuleQuantity? documentedPounds,RuleQuantity? printedLoad,
            IEnumerable<string> poundsIncludes=null,IEnumerable<string> loadIncludes=null)
        {
            if(!Validation.ValidId(id)||(parentId!=null&&!Validation.ValidId(parentId)))throw new ArgumentException("Invalid burden identity.");
            string[] Detach(IEnumerable<string> ids){var copy=(ids??Array.Empty<string>()).ToArray();
                if(copy.Length>256||copy.Any(x=>!Validation.ValidId(x)||x==id)||copy.Distinct(StringComparer.Ordinal).Count()!=copy.Length)
                    throw new ArgumentException("Invalid inclusive burden references.");return copy;}
            var pounds=Detach(poundsIncludes);var load=Detach(loadIncludes);
            if((pounds.Length!=0&&!documentedPounds.HasValue)||(load.Length!=0&&!printedLoad.HasValue))throw new ArgumentException("Inclusive amount missing.");
            Id=id;ParentId=parentId;DocumentedPounds=documentedPounds;PrintedLoad=printedLoad;
            PoundsIncludes=Array.AsReadOnly(pounds);LoadIncludes=Array.AsReadOnly(load);
        }
    }
    public sealed class BurdenTotals
    {
        public RuleQuantity? Pounds { get; }
        public RuleQuantity? Load { get; }
        public bool PoundsDocumented { get; }
        public BurdenTotals(RuleQuantity? pounds,RuleQuantity? load,bool poundsDocumented)
        {if(poundsDocumented&&!pounds.HasValue)throw new ArgumentException("Documented mass requires an amount.");Pounds=pounds;Load=load;PoundsDocumented=poundsDocumented;}
        public RuleQuantity RequireDocumentedPounds()=>PoundsDocumented?Pounds.Value:throw new InvalidOperationException("Actual documented mass required.");
    }
    /// <summary>Reviewed provisional carrying calculations only; no anatomy, custody, movement, action or inventory permission is granted.</summary>
    public static class PlaytestCarrying
    {
        public static CarryLimits Limits(CarrierSize size,int strength)
        {
            if(strength<0||!Enum.IsDefined(typeof(CarrierSize),size))throw new ArgumentOutOfRangeException(nameof(strength));
            var score=new RuleQuantity(strength);
            switch(size){
                case CarrierSize.Tiny:return new CarryLimits(score.Scale(15,2),score.Scale(1,2),new RuleQuantity(3,2));
                case CarrierSize.Small:return new CarryLimits(score.Scale(15),new RuleQuantity(Math.Max(0,strength-2)),new RuleQuantity(3));
                case CarrierSize.Medium:return new CarryLimits(score.Scale(15),score,new RuleQuantity(6));
                default:return new CarryLimits(score.Scale(30),score.Scale(2),new RuleQuantity(12));
            }
        }
        public static bool IsBurdened(RuleQuantity carriedLoad,RuleQuantity capacity)
            =>carriedLoad>default(RuleQuantity)&&carriedLoad<=capacity
                &&(BigInteger)carriedLoad.Numerator*2*capacity.Denominator>=(BigInteger)capacity.Numerator*carriedLoad.Denominator;
        public static RuleQuantity SpeedWithBurden(RuleQuantity speed,bool burdened)
            =>!burdened?speed:speed>new RuleQuantity(10)?speed-new RuleQuantity(10):default;
        public static bool? CanCarry(CarryLimits limits,BurdenTotals inventory)
        {
            if(limits==null||inventory==null)throw new ArgumentNullException(nameof(limits));
            if((inventory.Pounds.HasValue&&inventory.Pounds.Value>limits.Pounds)||(inventory.Load.HasValue&&inventory.Load.Value>limits.Load))return false;
            return inventory.Pounds.HasValue&&inventory.Load.HasValue?(bool?)true:null;
        }
        public static bool CanLift(CarryLimits limits,RuleQuantity pounds)
            =>pounds<=(limits??throw new ArgumentNullException(nameof(limits))).PushDragLiftPounds;
        public static RuleQuantity? PushDragSpeed(CarryLimits limits,RuleQuantity pounds,RuleQuantity otherwiseCurrentSpeed)
        {
            if(limits==null)throw new ArgumentNullException(nameof(limits));
            if(pounds>limits.PushDragLiftPounds)return null;
            return pounds>limits.Pounds&&otherwiseCurrentSpeed>new RuleQuantity(5)?new RuleQuantity(5):otherwiseCurrentSpeed;
        }
        public static RuleQuantity BodyPounds(RuleQuantity basePounds,bool petrified)=>petrified?basePounds.Scale(10):basePounds;
        public static BurdenTotals Casualty(CarrierSize size,RuleQuantity documentedBasePounds,bool petrified,BurdenTotals allEquipment)
        {
            if(allEquipment==null)throw new ArgumentNullException(nameof(allEquipment));
            var casualty=Limits(size,0).CasualtyLoad;
            return new BurdenTotals(allEquipment.Pounds.HasValue?BodyPounds(documentedBasePounds,petrified)+allEquipment.Pounds.Value:(RuleQuantity?)null,
                allEquipment.Load.HasValue?casualty+allEquipment.Load.Value:(RuleQuantity?)null,allEquipment.PoundsDocumented);
        }
        public static BurdenTotals Total(IEnumerable<BurdenItem> source)
        {
            if(source==null)throw new ArgumentNullException(nameof(source));var items=source.ToArray();
            if(items.Length>256||items.Any(x=>x==null)||items.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=items.Length)throw new ArgumentException("Invalid burden set.");
            var byId=items.ToDictionary(x=>x.Id,StringComparer.Ordinal);var ancestors=new Dictionary<string,HashSet<string>>(StringComparer.Ordinal);
            foreach(var item in items){var chain=new HashSet<string>(StringComparer.Ordinal);string parent=item.ParentId;
                while(parent!=null){if(parent==item.Id||!chain.Add(parent)||!byId.TryGetValue(parent,out var record))throw new ArgumentException("Invalid containment tree.");parent=record.ParentId;}
                ancestors.Add(item.Id,chain);
            }
            foreach(var item in items)foreach(string id in item.PoundsIncludes.Concat(item.LoadIncludes))
                if(!ancestors.TryGetValue(id,out var chain)||!chain.Contains(item.Id))throw new ArgumentException("Inclusive amount must name actual descendants.");
            // Known inclusive totals must at least contain the separately documented disjoint contents.
            foreach(bool mass in new[]{true,false})foreach(var item in items) {
                var amount=mass?item.DocumentedPounds:item.PrintedLoad;if(!amount.HasValue)continue;
                var extent=new HashSet<string>(mass?item.PoundsIncludes:item.LoadIncludes,StringComparer.Ordinal);
                var counted=new HashSet<string>(StringComparer.Ordinal);BigInteger n=0,d=1;
                foreach(var child in items.Where(i=>extent.Contains(i.Id)).OrderBy(i=>ancestors[i.Id].Count)) {
                    var value=mass?child.DocumentedPounds:child.PrintedLoad;if(!value.HasValue)continue;
                    var childExtent=new[]{child.Id}.Concat(mass?child.PoundsIncludes:child.LoadIncludes).ToArray();
                    if(childExtent.Any(id=>!extent.Contains(id)))continue;
                    if(value.Value>amount.Value)throw new ArgumentException("Inclusive total is smaller than a known contained aggregate.");
                    if(childExtent.Any(counted.Contains))continue;
                    n=n*value.Value.Denominator+(BigInteger)value.Value.Numerator*d;d*=value.Value.Denominator;
                    if(n*amount.Value.Denominator>(BigInteger)amount.Value.Numerator*d)throw new ArgumentException("Inclusive total is smaller than known contents.");
                    var gcd=BigInteger.GreatestCommonDivisor(n,d);n/=gcd;d/=gcd;
                    foreach(string id in childExtent)counted.Add(id);
                }
            }
            bool allDocumented=true;
            RuleQuantity? SumDimension(bool mass){
                var covered=new HashSet<string>(StringComparer.Ordinal);var values=new List<RuleQuantity>();bool known=true;
                foreach(var item in items.OrderBy(i=>ancestors[i.Id].Count).ThenBy(i=>i.Id,StringComparer.Ordinal)) {
                    var includes=mass?item.PoundsIncludes:item.LoadIncludes;
                    // An inclusive aggregate cannot be partly suppressed: its omitted own/contents amounts are unknown.
                    var extent=new[]{item.Id}.Concat(includes).ToArray();int overlap=extent.Count(covered.Contains);
                    if(overlap==extent.Length)continue;
                    if(overlap!=0)throw new ArgumentException("Conflicting partial inclusive quantities.");
                    // Cross-unit fallback is atomic only. Gross amounts cannot identify an empty
                    // container's amount or override a child's independently printed other unit.
                    RuleQuantity? value=mass?(item.DocumentedPounds??(item.LoadIncludes.Count==0?item.PrintedLoad?.Scale(10):null))
                        :(item.PrintedLoad??(item.PoundsIncludes.Count==0?item.DocumentedPounds?.Scale(1,10):null));
                    if(!value.HasValue)known=false;else values.Add(value.Value);
                    if(mass&&!item.DocumentedPounds.HasValue)allDocumented=false;
                    foreach(string id in extent)covered.Add(id);
                }
                return known?RuleQuantity.Sum(values):(RuleQuantity?)null;
            }
            var pounds=SumDimension(true);var load=SumDimension(false);
            return new BurdenTotals(pounds,load,allDocumented&&pounds.HasValue);
        }
    }
}
#endif
