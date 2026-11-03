using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum CropStage { Planting, Growing, Mature, Harvested, Failed }
    public enum CropWorkKind { Plant, Tend, Harvest }
    public enum CropWorkStatus { Working, Paused, Complete, Cancelled }

    public sealed class CropPlotRecord
    {
        public string Id { get; }
        public string OwnerId { get; }
        public bool Suitable { get; }
        public CropPlotRecord(string id,string ownerId,bool suitable)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(ownerId))throw new ArgumentException("Invalid crop plot.");
            Id=id;OwnerId=ownerId;Suitable=suitable;
        }
    }

    /// <summary>Immutable recorded labor and input identities; duration and crop rules belong to the selected policy.</summary>
    public sealed class CropWorkRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public CropWorkKind Kind { get; }
        public CropWorkStatus Status { get; }
        public RuleTime StartedAt { get; }
        public RuleTime Progress { get; }
        public RuleTime? EndedAt { get; }
        public IReadOnlyList<string> InputReservations { get; }
        public CropWorkRecord(string id,string workerId,CropWorkKind kind,CropWorkStatus status,
            RuleTime startedAt,RuleTime progress,RuleTime? endedAt,IEnumerable<string> inputReservations)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(workerId)||!Enum.IsDefined(typeof(CropWorkKind),kind)
                ||!Enum.IsDefined(typeof(CropWorkStatus),status)||inputReservations==null) throw new ArgumentException("Invalid crop work record.");
            var inputs=inputReservations.ToArray();
            if(inputs.Length>2 || inputs.Any(x=>!Validation.ValidId(x)) || inputs.Distinct(StringComparer.Ordinal).Count()!=inputs.Length)
                throw new ArgumentException("Invalid crop input references.");
            bool terminal=status==CropWorkStatus.Complete||status==CropWorkStatus.Cancelled;
            if(terminal!=endedAt.HasValue || (endedAt.HasValue&&endedAt.Value<startedAt)) throw new ArgumentException("Invalid crop task endpoint.");
            Id=id;WorkerId=workerId;Kind=kind;Status=status;StartedAt=startedAt;Progress=progress;EndedAt=endedAt;
            InputReservations=Array.AsReadOnly(inputs);
        }
    }

    /// <summary>Persistent crop data, not an executable farming rule or release content approval.</summary>
    public sealed class CropBatchRecord
    {
        public const int MaxTasks=32; // Bounded save/session history, not a gameplay entitlement or capacity.
        public string Id { get; }
        public string PlotId { get; }
        public string SeedLotId { get; }
        public string OwnerId { get; }
        public RuleTime CreatedAt { get; }
        public RuleTime UpdatedAt { get; }
        public CropStage Stage { get; }
        public RuleTime Growth { get; }
        public RuleTime? CareUntil { get; }
        public RuleTime? UnsuitableSince { get; }
        public RuleTime? MaturedAt { get; }
        public RuleTime? ClosedAt { get; }
        public IReadOnlyList<CropWorkRecord> Tasks { get; }
        public CropBatchRecord(string id,string plotId,string seedLotId,string ownerId,RuleTime createdAt,RuleTime updatedAt,
            CropStage stage,RuleTime growth,RuleTime? careUntil,RuleTime? unsuitableSince,
            RuleTime? maturedAt,RuleTime? closedAt,IEnumerable<CropWorkRecord> tasks)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(plotId)||!Validation.ValidId(seedLotId)||!Validation.ValidId(ownerId)
                ||updatedAt<createdAt||!Enum.IsDefined(typeof(CropStage),stage)||tasks==null) throw new ArgumentException("Invalid crop batch.");
            var work=tasks.ToArray();
            if(work.Length<1 || work.Length>MaxTasks || work.Any(x=>x==null)
                || work.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=work.Length
                || work.Count(x=>x.Status==CropWorkStatus.Working)>1
                || work.Any(x=>x.StartedAt<createdAt||x.StartedAt>updatedAt||(x.EndedAt.HasValue&&x.EndedAt.Value>updatedAt)))
                throw new ArgumentException("Invalid crop task history.");
            bool closed=stage==CropStage.Harvested||stage==CropStage.Failed;
            if(closed!=closedAt.HasValue || (closedAt.HasValue&&(closedAt.Value<createdAt||closedAt.Value>updatedAt))
                || (unsuitableSince.HasValue&&(unsuitableSince.Value<createdAt||unsuitableSince.Value>updatedAt))
                || (maturedAt.HasValue&&(maturedAt.Value<createdAt||maturedAt.Value>updatedAt)))
                throw new ArgumentException("Invalid crop timestamps.");
            Id=id;PlotId=plotId;SeedLotId=seedLotId;OwnerId=ownerId;CreatedAt=createdAt;UpdatedAt=updatedAt;Stage=stage;
            Growth=growth;CareUntil=careUntil;UnsuitableSince=unsuitableSince;MaturedAt=maturedAt;ClosedAt=closedAt;
            Tasks=Array.AsReadOnly(work);
        }
    }

    /// <summary>Freshness belongs to the physical output lot, independently of later plot/batch cleanup.</summary>
    public sealed class CropFoodRecord
    {
        public string LotId { get; }
        public string BatchId { get; }
        public RuleTime FreshUntil { get; }
        public bool Expired { get; }
        public CropFoodRecord(string lotId,string batchId,RuleTime freshUntil,bool expired)
        {
            if(!Validation.ValidId(lotId)||!Validation.ValidId(batchId)) throw new ArgumentException("Invalid crop output identity.");
            LotId=lotId;BatchId=batchId;FreshUntil=freshUntil;Expired=expired;
        }
    }
}
