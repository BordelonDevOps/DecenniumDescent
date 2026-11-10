using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum Recipe347OrderStatus { Working, Paused, AwaitingCheck, AwaitingSettlement, AwaitingChoice, Complete, Failed, Mishap, Cancelled }
    public enum Recipe347StationKind { MineFace, AssayBench }

    /// <summary>Explicit TEST_ONLY access; it is not a fabricated Formula Research success.</summary>
    public sealed class TestOnlyRecipe347FormulaAccessRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string RecipeId { get; }
        public string AccessSourceId { get; }
        public TestOnlyRecipe347FormulaAccessRecord(string id,string actorId,string recipeId,string accessSourceId)
        {
            foreach(string value in new[]{id,actorId,recipeId,accessSourceId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid TEST_ONLY recipe formula access.");
            if(recipeId!="recipe-347")throw new ArgumentException("This access record is only for recipe-347.");
            Id=id;ActorId=actorId;RecipeId=recipeId;AccessSourceId=accessSourceId;
        }
    }

    /// <summary>An already-recorded Mining specialty fact in this TEST_ONLY scenario. It creates no
    /// acquisition or advancement transition; the trade level remains in TradeProgressRecord.</summary>
    public sealed class TestOnlyTradeSpecialtyRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string TradeId { get; }
        public string ScopeId { get; }
        public string SourceId { get; }
        public TestOnlyTradeSpecialtyRecord(string id,string actorId,string tradeId,string scopeId,string sourceId)
        {
            foreach(string value in new[]{id,actorId,tradeId,scopeId,sourceId})
                if(!Validation.ValidId(value))throw new ArgumentException("Invalid TEST_ONLY trade specialty.");
            Id=id;ActorId=actorId;TradeId=tradeId;ScopeId=scopeId;SourceId=sourceId;
        }
    }

    /// <summary>Fingerprint-bound explicit workshop fixture. Its station is a Mine Face or Assay Bench
    /// inside a proper workshop; the station name alone never supplies workshop access.</summary>
    public sealed class TestOnlyRecipe347WorkshopRecord
    {
        private readonly string[] implementIds;
        public string Id { get; }
        public string SiteId { get; }
        public int SiteX { get; }
        public int SiteY { get; }
        public string StationId { get; }
        public string StationStructureId { get; }
        public Recipe347StationKind StationKind { get; }
        public IReadOnlyList<string> ImplementIds { get; }
        public bool ProperWorkshop { get; }
        public TestOnlyRecipe347WorkshopRecord(string id,string siteId,int siteX,int siteY,string stationId,
            string stationStructureId,Recipe347StationKind stationKind,IEnumerable<string> implementIds,bool properWorkshop)
        {
            var implements=(implementIds??Array.Empty<string>()).ToArray();
            if(new[]{id,siteId,stationId,stationStructureId}.Any(x=>!Validation.ValidId(x))
                ||!Enum.IsDefined(typeof(Recipe347StationKind),stationKind)||implements.Length!=3
                ||implements.Any(x=>!Validation.ValidId(x))||implements.Distinct(StringComparer.Ordinal).Count()!=3
                ||!properWorkshop)throw new ArgumentException("Invalid recipe-347 workshop fixture.");
            Id=id;SiteId=siteId;SiteX=siteX;SiteY=siteY;StationId=stationId;StationStructureId=stationStructureId;
            StationKind=stationKind;this.implementIds=implements;ImplementIds=Array.AsReadOnly(this.implementIds);ProperWorkshop=true;
        }
    }

    /// <summary>One recipe-347 work order. Active labor and material/body claims remain in the shared
    /// WorkLedger; identity, choices and causal check results are stored here.</summary>
    public sealed class Recipe347WorkOrderRecord
    {
        private readonly string[] componentLotIds,implementIds;
        public string Id { get; }
        public string WorkerId { get; }
        public string RecipeId { get; }
        public CharacterAbility Ability { get; }
        public string FormulaAccessId { get; }
        public string SpecialtyId { get; }
        public string WorkshopId { get; }
        public string BodyItemId { get; }
        public string BodyStructureId { get; }
        public string BodyLotId { get; }
        public IReadOnlyList<string> ComponentLotIds { get; }
        public IReadOnlyList<string> ImplementIds { get; }
        public Recipe347OrderStatus Status { get; }
        public ActiveWorkProgress Work { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public int CheckModifier { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public int Difficulty { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public CraftQuality Quality { get; }
        public CraftQualityChoice Choice { get; }
        public int MishapResult { get; }
        public int XpAward { get; }
        public string IncidentId { get; }
        public string OutputProvenanceId { get; }
        public bool Open=>Status==Recipe347OrderStatus.Working||Status==Recipe347OrderStatus.Paused
            ||Status==Recipe347OrderStatus.AwaitingCheck||Status==Recipe347OrderStatus.AwaitingSettlement
            ||Status==Recipe347OrderStatus.AwaitingChoice;

        public Recipe347WorkOrderRecord(string id,string workerId,string recipeId,CharacterAbility ability,
            string formulaAccessId,string specialtyId,string workshopId,string bodyItemId,string bodyStructureId,
            string bodyLotId,IEnumerable<string> componentLotIds,IEnumerable<string> implementIds,
            Recipe347OrderStatus status,ActiveWorkProgress work,RuleTime startedAt,RuleTime updatedAt,
            int checkModifier=0,int first=0,int second=0,int natural=0,int difficulty=20,uint randomBefore=0,
            uint randomAfter=0,long wordsConsumed=0,CraftQuality quality=CraftQuality.None,
            CraftQualityChoice choice=CraftQualityChoice.StandardQuantity,int mishapResult=0,int xpAward=0,
            string incidentId="",string outputProvenanceId="")
        {
            var components=(componentLotIds??Array.Empty<string>()).ToArray();var implements=(implementIds??Array.Empty<string>()).ToArray();
            string[] required={id,workerId,recipeId,formulaAccessId,specialtyId,workshopId,bodyItemId,bodyStructureId,bodyLotId};
            bool resolved=status==Recipe347OrderStatus.AwaitingSettlement||status==Recipe347OrderStatus.AwaitingChoice||status==Recipe347OrderStatus.Complete
                ||status==Recipe347OrderStatus.Failed||status==Recipe347OrderStatus.Mishap;
            if(required.Any(x=>!Validation.ValidId(x))||recipeId!="recipe-347"
                ||ability!=CharacterAbility.Strength&&ability!=CharacterAbility.Wisdom
                ||components.Length!=5||components.Any(x=>!Validation.ValidId(x))
                ||components.Distinct(StringComparer.Ordinal).Count()!=components.Length
                ||implements.Length!=3||implements.Any(x=>!Validation.ValidId(x))
                ||implements.Distinct(StringComparer.Ordinal).Count()!=implements.Length
                ||!Enum.IsDefined(typeof(Recipe347OrderStatus),status)||work==null||updatedAt<startedAt
                ||difficulty!=20||checkModifier< -40||checkModifier>40||first<0||first>20||second<0||second>20
                ||natural<0||natural>20||wordsConsumed<0||!Enum.IsDefined(typeof(CraftQuality),quality)
                ||!Enum.IsDefined(typeof(CraftQualityChoice),choice)||mishapResult<0||mishapResult>6||xpAward<0||xpAward>4
                ||incidentId==null||incidentId!=""&&!Validation.ValidId(incidentId)
                ||outputProvenanceId==null||outputProvenanceId!=""&&!Validation.ValidId(outputProvenanceId)
                ||resolved&&(natural<1||randomBefore==0||randomAfter==0||wordsConsumed<1||quality==CraftQuality.None)
                ||!resolved&&(natural!=0||first!=0||second!=0||randomBefore!=0||randomAfter!=0||wordsConsumed!=0||quality!=CraftQuality.None)
                ||status==Recipe347OrderStatus.AwaitingSettlement&&(quality==CraftQuality.None||quality==CraftQuality.Exceptional||quality==CraftQuality.Masterwork)
                ||status==Recipe347OrderStatus.AwaitingChoice&&(quality!=CraftQuality.Exceptional&&quality!=CraftQuality.Masterwork)
                ||status==Recipe347OrderStatus.Mishap&&(quality!=CraftQuality.Mishap||mishapResult<1||incidentId=="")
                ||status==Recipe347OrderStatus.Failed&&quality!=CraftQuality.Failed
                ||(quality==CraftQuality.Flawed||quality==CraftQuality.Standard||quality==CraftQuality.Exceptional||quality==CraftQuality.Masterwork)
                    !=(status==Recipe347OrderStatus.Complete||status==Recipe347OrderStatus.AwaitingChoice
                        ||status==Recipe347OrderStatus.AwaitingSettlement&&(quality==CraftQuality.Flawed||quality==CraftQuality.Standard
                            ||quality==CraftQuality.Exceptional||quality==CraftQuality.Masterwork))
                ||(status==Recipe347OrderStatus.Complete||status==Recipe347OrderStatus.Failed||status==Recipe347OrderStatus.Mishap)
                    &&!work.Complete
                ||status==Recipe347OrderStatus.AwaitingSettlement&&!work.Complete
                ||status==Recipe347OrderStatus.Complete&&outputProvenanceId=="")
                throw new ArgumentException("Invalid recipe-347 work order.");
            Id=id;WorkerId=workerId;RecipeId=recipeId;Ability=ability;FormulaAccessId=formulaAccessId;SpecialtyId=specialtyId;
            WorkshopId=workshopId;BodyItemId=bodyItemId;BodyStructureId=bodyStructureId;BodyLotId=bodyLotId;
            this.componentLotIds=components;this.implementIds=implements;ComponentLotIds=Array.AsReadOnly(this.componentLotIds);
            ImplementIds=Array.AsReadOnly(this.implementIds);Status=status;Work=work;StartedAt=startedAt;UpdatedAt=updatedAt;
            CheckModifier=checkModifier;First=first;Second=second;Natural=natural;Difficulty=difficulty;RandomBefore=randomBefore;
            RandomAfter=randomAfter;WordsConsumed=wordsConsumed;Quality=quality;Choice=choice;MishapResult=mishapResult;
            XpAward=xpAward;IncidentId=incidentId;OutputProvenanceId=outputProvenanceId;
        }

        public Recipe347WorkOrderRecord WithWork(RuleTime at,ActiveWorkProgress work,Recipe347OrderStatus status)
            =>Copy(status,work,at);
        public Recipe347WorkOrderRecord WithCheck(RuleTime at,int modifier,int first,int second,int natural,
            uint before,uint after,long words,CraftQuality quality,Recipe347OrderStatus status)
            =>new Recipe347WorkOrderRecord(Id,WorkerId,RecipeId,Ability,FormulaAccessId,SpecialtyId,WorkshopId,
                BodyItemId,BodyStructureId,BodyLotId,componentLotIds,implementIds,status,Work,StartedAt,at,
                modifier,first,second,natural,Difficulty,before,after,words,quality,Choice,MishapResult,XpAward,IncidentId,OutputProvenanceId);
        public Recipe347WorkOrderRecord WithSettlement(RuleTime at,Recipe347OrderStatus status,CraftQualityChoice choice,
            int mishap,int xp,string incident,string outputId)
            =>new Recipe347WorkOrderRecord(Id,WorkerId,RecipeId,Ability,FormulaAccessId,SpecialtyId,WorkshopId,
                BodyItemId,BodyStructureId,BodyLotId,componentLotIds,implementIds,status,Work,StartedAt,at,
                CheckModifier,First,Second,Natural,Difficulty,RandomBefore,RandomAfter,WordsConsumed,Quality,choice,
                mishap,xp,incident,outputId);
        private Recipe347WorkOrderRecord Copy(Recipe347OrderStatus status,ActiveWorkProgress work,RuleTime at)
            =>new Recipe347WorkOrderRecord(Id,WorkerId,RecipeId,Ability,FormulaAccessId,SpecialtyId,WorkshopId,
                BodyItemId,BodyStructureId,BodyLotId,componentLotIds,implementIds,status,work,StartedAt,at,
                CheckModifier,First,Second,Natural,Difficulty,RandomBefore,RandomAfter,WordsConsumed,Quality,Choice,
                MishapResult,XpAward,IncidentId,OutputProvenanceId);
    }

    /// <summary>Recipe provenance attached to the same mundane body; it never creates inventory.</summary>
    public sealed class Recipe347OutputProvenanceRecord
    {
        public string Id { get; }
        public string OrderId { get; }
        public string ItemId { get; }
        public string StructureId { get; }
        public RuleTime CreatedAt { get; }
        public long Revision { get; }
        public CraftQuality Quality { get; }
        public CraftQualityChoice Choice { get; }
        public long PreviousMaximumHp { get; }
        public long PreviousHp { get; }
        public long MaximumHp { get; }
        public long Hp { get; }
        public Recipe347OutputProvenanceRecord(string id,string orderId,string itemId,string structureId,RuleTime createdAt,
            long revision,CraftQuality quality,CraftQualityChoice choice,long previousMaximumHp,long previousHp,
            long maximumHp,long hp)
        {
            if(new[]{id,orderId,itemId,structureId}.Any(x=>!Validation.ValidId(x))||revision<1
                ||!Enum.IsDefined(typeof(CraftQuality),quality)||!Enum.IsDefined(typeof(CraftQualityChoice),choice)
                ||quality<CraftQuality.Flawed||previousMaximumHp!=5||previousHp<1||previousHp>previousMaximumHp
                ||maximumHp<1||maximumHp>7||hp<0||hp>maximumHp)
                throw new ArgumentException("Invalid recipe-347 output provenance.");
            Id=id;OrderId=orderId;ItemId=itemId;StructureId=structureId;CreatedAt=createdAt;Revision=revision;
            Quality=quality;Choice=choice;PreviousMaximumHp=previousMaximumHp;PreviousHp=previousHp;MaximumHp=maximumHp;Hp=hp;
        }
    }

    /// <summary>Stable item-authored Mining Tool facts; deposit allocations belong to use records.</summary>
    public sealed class Recipe347MiningToolProfileRecord
    {
        public string Id { get; }
        public string ProvenanceId { get; }
        public string ItemId { get; }
        public string StructureId { get; }
        public long MaximumHp { get; }
        public int StructuralAc=>15;
        public int CheckBonus=>2;
        public RuleQuantity MassPounds=>new RuleQuantity(3);
        public Recipe347MiningToolProfileRecord(string id,string provenanceId,string itemId,string structureId,long maximumHp)
        {
            if(new[]{id,provenanceId,itemId,structureId}.Any(x=>!Validation.ValidId(x))||maximumHp<1||maximumHp>7)
                throw new ArgumentException("Invalid reusable recipe-347 Mining Tool profile.");
            Id=id;ProvenanceId=provenanceId;ItemId=itemId;StructureId=structureId;MaximumHp=maximumHp;
        }
    }

    /// <summary>Causal physical deployment evidence captured when a reusable item joins a mining
    /// attempt. It allows a completed result to survive later movement or damage to the tool.</summary>
    public sealed class Recipe347MiningToolUseEvidenceRecord
    {
        private readonly string[] selectedUnitIds;
        public string Id { get; }
        public string AttemptId { get; }
        public string ProfileId { get; }
        public string ItemId { get; }
        public string DepositId { get; }
        public string DepositVersionId { get; }
        public string WorkerId { get; }
        public RuleTime CapturedAt { get; }
        public int WorkerX { get; }
        public int WorkerY { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public PortablePlacement Placement { get; }
        public int GroundX { get; }
        public int GroundY { get; }
        public long StructureHp { get; }
        public long StructureMaximumHp { get; }
        public string StructureLocationId { get; }
        public string WorkSurfaceId { get; }
        public bool WorkSurfaceBroken { get; }
        public string ReceiverId { get; }
        public bool ReceiverOpen { get; }
        public int AvailableHands { get; }
        public IReadOnlyList<string> SelectedUnitIds { get; }
        public Recipe347MiningToolUseEvidenceRecord(string id,string attemptId,string profileId,string itemId,
            string depositId,string depositVersionId,string workerId,RuleTime capturedAt,int workerX,int workerY,
            string ownerId,string custodianId,PortablePlacement placement,int groundX,int groundY,long structureHp,
            long structureMaximumHp,string structureLocationId,string workSurfaceId,bool workSurfaceBroken,
            string receiverId,bool receiverOpen,int availableHands,IEnumerable<string> selectedUnitIds)
        {
            var selected=(selectedUnitIds??Array.Empty<string>()).ToArray();
            if(new[]{id,attemptId,profileId,itemId,depositId,depositVersionId,workerId,ownerId,custodianId,
                    structureLocationId,workSurfaceId,receiverId}.Any(x=>!Validation.ValidId(x))
                ||!Enum.IsDefined(typeof(PortablePlacement),placement)||structureHp<0||structureMaximumHp<1
                ||structureHp>structureMaximumHp||availableHands<0||availableHands>2||selected.Length==0
                ||selected.Any(x=>!Validation.ValidId(x))||selected.Distinct(StringComparer.Ordinal).Count()!=selected.Length)
                throw new ArgumentException("Invalid recipe-347 mining deployment evidence.");
            Id=id;AttemptId=attemptId;ProfileId=profileId;ItemId=itemId;DepositId=depositId;DepositVersionId=depositVersionId;
            WorkerId=workerId;CapturedAt=capturedAt;WorkerX=workerX;WorkerY=workerY;OwnerId=ownerId;CustodianId=custodianId;
            Placement=placement;GroundX=groundX;GroundY=groundY;StructureHp=structureHp;StructureMaximumHp=structureMaximumHp;
            StructureLocationId=structureLocationId;WorkSurfaceId=workSurfaceId;WorkSurfaceBroken=workSurfaceBroken;
            ReceiverId=receiverId;ReceiverOpen=receiverOpen;AvailableHands=availableHands;this.selectedUnitIds=selected;
            SelectedUnitIds=Array.AsReadOnly(this.selectedUnitIds);
        }
    }

    /// <summary>One positive-duration interval in which the reusable tool was physically deployed
    /// and eligible during actual extraction work. Intervals are derived from shared clock advances.</summary>
    public sealed class Recipe347MiningToolWorkSegmentRecord
    {
        public string AttemptId { get; }
        public RuleTime Start { get; }
        public RuleTime End { get; }
        public Recipe347MiningToolWorkSegmentRecord(string attemptId,RuleTime start,RuleTime end)
        {
            if(!Validation.ValidId(attemptId)||end<=start)throw new ArgumentException("Invalid Mining Tool work segment.");
            AttemptId=attemptId;Start=start;End=end;
        }
    }
}
