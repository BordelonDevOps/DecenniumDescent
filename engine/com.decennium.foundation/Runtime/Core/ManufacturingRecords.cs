using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum CraftQuality { None, Mishap, Failed, Flawed, Standard, Exceptional, Masterwork }
    public enum CraftQualityChoice { StandardQuantity, FullYield, Durability }
    public enum ManufacturingStatus { Working, Paused, AwaitingCheck, AwaitingChoice, Complete, Cancelled }
    public sealed class ManufacturingAdvanceRecord
    {
        public RuleTime Target { get; } public bool ExitAfterSlot { get; }
        public string CommandId { get; } public long CommandRevision { get; } public string OutgoingSlotId { get; }
        // Compatibility name retained for existing saves and callers. This is the shared-world
        // advance continuation while any persisted manufacturing or schema64 recovery choice blocks it.
        // All due automatic work/expiry/recovery/life and completion checks at the current timestamp
        // have finished. Only settlement and the remaining authorized advance are next.
        public int NextPhase => 1;
        public ManufacturingAdvanceRecord(RuleTime target,bool exitAfterSlot,string command,long revision,string outgoingSlot)
        {
            if(!Validation.ValidId(command)||revision<1||outgoingSlot==null||outgoingSlot!=""&&!Validation.ValidId(outgoingSlot))throw new ArgumentException("Invalid manufacturing continuation.");
            Target=target;ExitAfterSlot=exitAfterSlot;CommandId=command;CommandRevision=revision;OutgoingSlotId=outgoingSlot;
        }
    }
    public sealed class ManufacturingOrderRecord
    {
        public string Id { get; } public string WorkerId { get; } public string RecipeId { get; }
        public int MaterialSet { get; } public int ExtraVials { get; } public bool TakeTen { get; }
        public ManufacturingStatus Status { get; } public ActiveWorkProgress Work { get; }
        public RuleTime StartedAt { get; } public RuleTime UpdatedAt { get; } public RuleTime? StabilizedAt { get; }
        public int First { get; } public int Second { get; } public int Natural { get; }
        public CraftQuality Quality { get; } public CraftQualityChoice Choice { get; }
        public int RetainedCatalyst { get; } public int Mishap { get; } public int XpAward { get; }
        public string FindingId { get; }
        public string MishapIncidentId { get; }
        public bool Open => Status != ManufacturingStatus.Complete && Status != ManufacturingStatus.Cancelled;
        public ManufacturingOrderRecord(string id, string worker, string recipe, int materialSet, int extraVials, bool takeTen,
            ManufacturingStatus status, ActiveWorkProgress work, RuleTime start, RuleTime updated, RuleTime? stabilized = null,
            int first = 0, int second = 0, int natural = 0, CraftQuality quality = CraftQuality.None, CraftQualityChoice choice = CraftQualityChoice.StandardQuantity,
            int catalyst = -1, int mishap = 0, int xp = 0, string finding = "", string incident = "")
        {
            if (new[] { id,worker,recipe }.Any(x => !Validation.ValidId(x)) || materialSet < 0 || materialSet > 7 || extraVials < 0 || extraVials > 6
                || !Enum.IsDefined(typeof(ManufacturingStatus),status) || work == null || updated < start || stabilized.HasValue && (stabilized < start || stabilized > updated)
                || first < 0 || first > 20 || second < 0 || second > 20 || natural < 0 || natural > 20 || !Enum.IsDefined(typeof(CraftQuality),quality)
                || !Enum.IsDefined(typeof(CraftQualityChoice),choice) || catalyst < -1 || catalyst > 3 || mishap < 0 || mishap > 6 || xp < 0 || xp > 4
                || finding == null || finding != "" && !Validation.ValidId(finding) || incident == null || incident!=""&&!Validation.ValidId(incident)) throw new ArgumentException("Invalid manufacturing order.");
            Id=id;WorkerId=worker;RecipeId=recipe;MaterialSet=materialSet;ExtraVials=extraVials;TakeTen=takeTen;Status=status;Work=work;
            StartedAt=start;UpdatedAt=updated;StabilizedAt=stabilized;First=first;Second=second;Natural=natural;Quality=quality;Choice=choice;RetainedCatalyst=catalyst;Mishap=mishap;XpAward=xp;FindingId=finding;MishapIncidentId=incident;
        }
    }
    public sealed class TradeProgressRecord
    {
        public string WorkerId { get; } public string TradeId { get; } public int Level { get; } public int Xp { get; }
        public IReadOnlyList<string> SuccessfulRecipes { get; } public IReadOnlyList<string> Findings { get; }
        public TradeProgressRecord(string worker,string trade,int level,int xp,IEnumerable<string> successes=null,IEnumerable<string> findings=null)
        {
            var a=(successes??Array.Empty<string>()).ToArray();var b=(findings??Array.Empty<string>()).ToArray();
            if(!Validation.ValidId(worker)||!Validation.ValidId(trade)||level<1||level>20||xp<0||a.Length>32||b.Length>32||a.Concat(b).Any(x=>!Validation.ValidId(x))
                ||a.Distinct(StringComparer.Ordinal).Count()!=a.Length||b.Distinct(StringComparer.Ordinal).Count()!=b.Length)throw new ArgumentException("Invalid trade progression.");
            WorkerId=worker;TradeId=trade;Level=level;Xp=xp;SuccessfulRecipes=Array.AsReadOnly(a);Findings=Array.AsReadOnly(b);
        }
    }
    /// <summary>An actual sealed single-use dose or its retained ordinary empty container. Location
    /// and custody are explicit; recipe provenance never restores consumed ingredient properties.</summary>
    public sealed class AlchemyDoseRecord
    {
        public string Id { get; } public string OrderId { get; } public string RecipeId { get; } public string MakerId { get; }
        public string OwnerId { get; } public string CustodianId { get; } public string LocationId { get; }
        public RuleTime CreatedAt { get; } public int MaximumHp { get; } public int Hp { get; }
        public RuleTime? UsedAt { get; } public string UserId { get; } public string RecipientId { get; }
        public int FirstD4 { get; } public int SecondD4 { get; } public long PotentialHealing { get; } public long ActualHealing { get; }
        public bool Spent => UsedAt.HasValue;
        public AlchemyDoseRecord(string id,string order,string recipe,string maker,string owner,string custodian,string location,RuleTime created,int maxHp,int hp,
            RuleTime? used=null,string user="",string recipient="",int first=0,int second=0,long potential=0,long actual=0)
        {
            if(new[]{id,order,recipe,maker,owner,custodian,location}.Any(x=>!Validation.ValidId(x))||maxHp<1||maxHp>2||hp<0||hp>maxHp
                ||user==null||recipient==null||used.HasValue&&(used<created||!Validation.ValidId(user)||!Validation.ValidId(recipient))
                ||first<0||first>4||second<0||second>4||potential<0||actual<0||actual>potential||!used.HasValue&&(user!=""||recipient!=""||first!=0||second!=0||potential!=0||actual!=0))throw new ArgumentException("Invalid Alchemy dose.");
            Id=id;OrderId=order;RecipeId=recipe;MakerId=maker;OwnerId=owner;CustodianId=custodian;LocationId=location;CreatedAt=created;MaximumHp=maxHp;Hp=hp;
            UsedAt=used;UserId=user;RecipientId=recipient;FirstD4=first;SecondD4=second;PotentialHealing=potential;ActualHealing=actual;
        }
        public RuleQuantity MassPounds => new RuleQuantity(Spent?1:2,10);

        public AlchemyDoseRecord WithPlacement(string custodian, string location)
            => new AlchemyDoseRecord(Id, OrderId, RecipeId, MakerId, OwnerId, custodian, location, CreatedAt, MaximumHp, Hp,
                UsedAt, UserId, RecipientId, FirstD4, SecondD4, PotentialHealing, ActualHealing);
    }
    public static class ManufacturingValidation
    {
        public const int MaxOrders=16,MaxDoses=112,MaxTrades=8;
        public static void Validate(Snapshot s)
        {
            if(s.ManufacturingOrders==null||s.Trades==null||s.AlchemyDoses==null||s.ManufacturingOrders.Length>MaxOrders||s.Trades.Length>MaxTrades||s.AlchemyDoses.Length>MaxDoses
                ||s.ManufacturingOrders.Any(x=>x==null)||s.Trades.Any(x=>x==null)||s.AlchemyDoses.Any(x=>x==null)
                ||s.SchemaVersion<Snapshot.ManufacturingSchema&&(s.ManufacturingOrders.Length!=0||s.Trades.Length!=0||s.AlchemyDoses.Length!=0||s.ManufacturingAdvance!=null))throw new ArgumentException("Invalid manufacturing collection.");
            bool pendingRecoveryChoice=s.SchemaVersion>=Snapshot.ExpeditionStrainRecoverySchema
                &&s.ExpeditionStrainRecoveryOffers!=null
                &&s.ExpeditionStrainRecoveryOffers.Any(x=>x.Pending);
            bool pendingRecipeChoice=s.SchemaVersion>=Snapshot.Recipe347Schema&&s.Recipe347WorkOrders!=null
                &&s.Recipe347WorkOrders.Any(x=>x.Status==Recipe347OrderStatus.AwaitingChoice);
            if(s.ManufacturingAdvance!=null&&(s.ManufacturingAdvance.Target<s.RuleClock
                ||s.ManufacturingAdvance.CommandRevision>s.Revision
                ||!s.ManufacturingOrders.Any(x=>x.Status==ManufacturingStatus.AwaitingChoice)&&!pendingRecoveryChoice&&!pendingRecipeChoice))
                throw new ArgumentException("Invalid suspended world advance.");
            if(s.ManufacturingOrders.Select(x=>x.Id).Distinct().Count()!=s.ManufacturingOrders.Length||s.AlchemyDoses.Select(x=>x.Id).Distinct().Count()!=s.AlchemyDoses.Length
                ||s.Trades.Select(x=>x.WorkerId+"|"+x.TradeId).Distinct().Count()!=s.Trades.Length)throw new ArgumentException("Duplicate manufacturing identity.");
            foreach(var job in s.ManufacturingOrders)if(!s.Actors.Any(x=>x.Id==job.WorkerId)||job.UpdatedAt>s.RuleClock)throw new ArgumentException("Invalid manufacturing reference.");
            foreach(var trade in s.Trades)if(!s.Actors.Any(x=>x.Id==trade.WorkerId))throw new ArgumentException("Invalid trade worker.");
            foreach(var dose in s.AlchemyDoses)if(!s.ManufacturingOrders.Any(x=>x.Id==dose.OrderId)||dose.CreatedAt>s.RuleClock||dose.UsedAt>s.RuleClock)throw new ArgumentException("Invalid dose history.");
        }
    }
}
