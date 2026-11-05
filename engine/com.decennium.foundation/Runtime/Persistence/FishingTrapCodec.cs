using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class FishingTrapCodec
    {
        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);
        private static void Text(BinaryWriter w,string x){var b=Utf8.GetBytes(x);w.Write(b.Length);w.Write(b);}
        private static string Text(BinaryReader r){int n=r.ReadInt32();if(n<0||n>512)throw new InvalidDataException("Invalid fishing-trap identity length.");var b=r.ReadBytes(n);if(b.Length!=n)throw new EndOfStreamException();return Utf8.GetString(b);}
        private static int Count(BinaryReader r){int n=r.ReadInt32();if(n<0||n>FishingTrapValidation.MaxAttempts)throw new InvalidDataException("Invalid fishing-trap attempt count.");return n;}
        private static bool Bool(BinaryReader r){byte x=r.ReadByte();if(x>1)throw new InvalidDataException("Invalid fishing-trap boolean.");return x==1;}
        private static void Time(BinaryWriter w,RuleTime t){w.Write(t.Numerator);w.Write(t.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());
        private static void OptionalTime(BinaryWriter w,RuleTime? t){w.Write(t.HasValue);if(t.HasValue)Time(w,t.Value);}
        private static RuleTime? OptionalTime(BinaryReader r)=>Bool(r)?Time(r):(RuleTime?)null;
        private static void Quantity(BinaryWriter w,RuleQuantity q){w.Write(q.Numerator);w.Write(q.Denominator);}
        private static RuleQuantity Quantity(BinaryReader r)=>new RuleQuantity(r.ReadInt64(),r.ReadInt64());
        public static void Write(BinaryWriter w,Snapshot s)
        {
            w.Write(s.FishingTrapAttempts.Length);
            foreach(var a in s.FishingTrapAttempts.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,a.Id);Text(w,a.SetterId);Text(w,a.ResponsibleHolderId);Text(w,a.TrapId);Text(w,a.OpportunityId);
                Text(w,a.CreatureId);Text(w,a.CapturedCreatureId);Text(w,a.SiteId);Time(w,a.StartedAt);Time(w,a.SetupLabor);
                OptionalTime(w,a.SetupCompletedAt);OptionalTime(w,a.CheckDueAt);OptionalTime(w,a.CheckResolvedAt);OptionalTime(w,a.AbandonedAt);
                w.Write((int)a.Status);w.Write(a.OpportunityCommitted);w.Write(a.WisdomModifier);w.Write(a.ProficiencyRank);w.Write(a.ProficiencyBonus);
                w.Write((int)a.DiceSelection);w.Write(a.FirstDie);w.Write(a.SecondDie);w.Write(a.Natural);w.Write(a.CheckModifier);w.Write(a.CheckDc);
                w.Write((int)a.CheckDegree);w.Write((int)a.CheckOutcome);w.Write(a.RandomBefore);w.Write(a.RandomAfter);w.Write(a.WordsConsumed);
                if(s.SchemaVersion>=Snapshot.FishingTrapBaitSchema) {
                    Text(w,a.BaitLotId);Text(w,a.BaitReservationId);OptionalTime(w,a.BaitExposedAt);
                }
            }
            if(s.SchemaVersion<Snapshot.FishingTrapSchema)return;
            w.Write(s.FishingOpportunities.Length);
            foreach(var x in s.FishingOpportunities.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.SiteId);Text(w,x.StockVersionId);Text(w,x.CandidateCreatureId);w.Write((int)x.Status);
                Text(w,x.ReservedByAttemptId);OptionalTime(w,x.ReservedAt);Text(w,x.CommittedByAttemptId);OptionalTime(w,x.CommittedAt);
                Text(w,x.LastReleasedAttemptId);OptionalTime(w,x.LastReleasedAt);
            }
            w.Write(s.FishingCreatures.Length);
            foreach(var x in s.FishingCreatures.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ProfileId);Text(w,x.OriginId);Text(w,x.SiteId);Text(w,x.LocationId);Text(w,x.ContainerId);Text(w,x.CustodianId);
                w.Write((int)x.LifeState);Quantity(w,x.MassPounds);Quantity(w,x.VolumeCubicFeet);Text(w,x.ActiveResponseAttemptId);
                Text(w,x.LastResponseAttemptId);Text(w,x.CapturedByAttemptId);OptionalTime(w,x.RecoveryEvaluatedAt);w.Write(x.RecoveryExtraUnits);
            }
            w.Write(s.FishingTraps.Length);
            foreach(var x in s.FishingTraps.OrderBy(x=>x.TrapId,StringComparer.Ordinal)) {
                Text(w,x.TrapId);Text(w,x.SiteId);Text(w,x.SupportId);w.Write((int)x.Status);Text(w,x.AttemptId);
                Text(w,x.LatestRetrievalId);Text(w,x.ReceivingLocationId);OptionalTime(w,x.RetrievedAt);w.Write(x.StructuralAc);
                w.Write(x.CatchCapacityPounds);Quantity(w,x.CatchCapacityCubicFeet);Quantity(w,x.BodyVolumeCubicFeet);
                w.Write(x.RecoveryCordFeet);w.Write(x.X);w.Write(x.Y);
            }
            w.Write(s.FishingReceiveLocations.Length);
            foreach(var x in s.FishingReceiveLocations.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.SiteId);Text(w,x.SupportId);w.Write(x.X);w.Write(x.Y);Quantity(w,x.CapacityPounds);
                Quantity(w,x.CapacityCubicFeet);w.Write(x.RecoveryPathFeet);Text(w,x.ReservedByRetrievalId);
            }
            w.Write(s.FishingTrapRetrievals.Length);
            foreach(var x in s.FishingTrapRetrievals.OrderBy(x=>x.StartedAt).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.AttemptId);Text(w,x.TrapId);Text(w,x.WorkerId);Text(w,x.DestinationId);
                Time(w,x.StartedAt);Time(w,x.WorkDone);Time(w,x.UpdatedAt);OptionalTime(w,x.CompletedAt);w.Write((int)x.Status);
            }
            if(s.SchemaVersion<Snapshot.FishingStockSchema)return;
            w.Write(s.FishingStockManifests.Length);
            foreach(var x in s.FishingStockManifests.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.SharedStockId);Text(w,x.VersionId);Time(w,x.EffectiveFrom);OptionalTime(w,x.EffectiveUntil);
                w.Write(x.PhysicalMemberIds.Length);foreach(string member in x.PhysicalMemberIds)Text(w,member);
            }
            w.Write(s.FishingStockAllocations.Length);
            foreach(var x in s.FishingStockAllocations.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                Text(w,x.Id);Text(w,x.ManifestId);Text(w,x.OpportunityId);w.Write(x.WholePool);
                w.Write(x.PhysicalMemberIds.Length);foreach(string member in x.PhysicalMemberIds)Text(w,member);
            }
        }
        public static void Read(BinaryReader r,Snapshot s,int schema)
        {
            s.FishingTrapAttempts=new FishingTrapAttemptRecord[Count(r)];
            for(int i=0;i<s.FishingTrapAttempts.Length;i++) {
                string id=Text(r),setter=Text(r),holder=Text(r),trap=Text(r),opportunity=Text(r),creature=Text(r),captured=Text(r),site=Text(r);
                RuleTime started=Time(r),labor=Time(r);RuleTime? setup=OptionalTime(r),due=OptionalTime(r),resolved=OptionalTime(r),abandoned=OptionalTime(r);
                int status=r.ReadInt32();bool opportunityCommitted=Bool(r);int wisdom=r.ReadInt32(),rank=r.ReadInt32(),proficiency=r.ReadInt32();
                var selection=(FishingTrapDiceSelection)r.ReadInt32();int first=r.ReadInt32(),second=r.ReadInt32(),natural=r.ReadInt32();
                int modifier=r.ReadInt32(),dc=r.ReadInt32();var degree=(FishingTrapCheckDegree)r.ReadInt32();var outcome=(FishingTrapCheckOutcome)r.ReadInt32();
                uint randomBefore=r.ReadUInt32(),randomAfter=r.ReadUInt32();long words=r.ReadInt64();
                string baitLot=schema>=Snapshot.FishingTrapBaitSchema?Text(r):"";
                string baitReservation=schema>=Snapshot.FishingTrapBaitSchema?Text(r):"";
                RuleTime? baitExposed=schema>=Snapshot.FishingTrapBaitSchema?OptionalTime(r):(RuleTime?)null;
                s.FishingTrapAttempts[i]=new FishingTrapAttemptRecord(id,setter,holder,trap,opportunity,creature,captured,site,started,labor,
                    setup,due,resolved,abandoned,(FishingTrapAttemptStatus)status,opportunityCommitted,wisdom,rank,proficiency,
                    selection,first,second,natural,modifier,dc,degree,outcome,randomBefore,randomAfter,words,baitLot,baitReservation,baitExposed);
            }
            if(schema<Snapshot.FishingTrapSchema)return;
            s.FishingOpportunities=new FishingOpportunityRecord[Count(r)];
            for(int i=0;i<s.FishingOpportunities.Length;i++) {
                string id=Text(r),site=Text(r),stock=Text(r),candidate=Text(r);var status=(FishingOpportunityStatus)r.ReadInt32();
                string reserved=Text(r);RuleTime? reservedAt=OptionalTime(r);string committed=Text(r);RuleTime? committedAt=OptionalTime(r);
                string released=Text(r);RuleTime? releasedAt=OptionalTime(r);
                s.FishingOpportunities[i]=new FishingOpportunityRecord(id,site,stock,candidate,status,reserved,reservedAt,committed,committedAt,released,releasedAt);
            }
            s.FishingCreatures=new FishingCreatureBodyRecord[Count(r)];
            for(int i=0;i<s.FishingCreatures.Length;i++) {
                string id=Text(r),profile=Text(r),origin=Text(r),site=Text(r),location=Text(r),container=Text(r),custodian=Text(r);
                var life=(FishingCreatureLifeState)r.ReadInt32();RuleQuantity mass=Quantity(r),volume=Quantity(r);
                string active=Text(r),last=Text(r),captured=Text(r);RuleTime? recovered=OptionalTime(r);int extra=r.ReadInt32();
                s.FishingCreatures[i]=new FishingCreatureBodyRecord(id,profile,origin,site,location,container,custodian,life,mass,volume,
                    active,last,captured,recovered,extra);
            }
            s.FishingTraps=new FishingTrapPhysicalRecord[Count(r)];
            for(int i=0;i<s.FishingTraps.Length;i++) {
                string id=Text(r),site=Text(r),support=Text(r);var status=(FishingTrapPhysicalStatus)r.ReadInt32();string attempt=Text(r),retrieval=Text(r),receiver=Text(r);
                RuleTime? retrievedAt=OptionalTime(r);int ac=r.ReadInt32();long pounds=r.ReadInt64();RuleQuantity volume=Quantity(r),bodyVolume=Quantity(r);
                int cord=r.ReadInt32(),x=r.ReadInt32(),y=r.ReadInt32();
                s.FishingTraps[i]=new FishingTrapPhysicalRecord(id,site,support,status,attempt,retrieval,receiver,retrievedAt,ac,pounds,volume,bodyVolume,cord,x,y);
            }
            s.FishingReceiveLocations=new FishingReceiveLocationRecord[Count(r)];
            for(int i=0;i<s.FishingReceiveLocations.Length;i++) {
                string id=Text(r),site=Text(r),support=Text(r);int x=r.ReadInt32(),y=r.ReadInt32();RuleQuantity pounds=Quantity(r),volume=Quantity(r);
                int path=r.ReadInt32();string reserved=Text(r);
                s.FishingReceiveLocations[i]=new FishingReceiveLocationRecord(id,site,support,x,y,pounds,volume,reserved,path);
            }
            s.FishingTrapRetrievals=new FishingTrapRetrievalRecord[Count(r)];
            for(int i=0;i<s.FishingTrapRetrievals.Length;i++) {
                string id=Text(r),attempt=Text(r),trap=Text(r),worker=Text(r),destination=Text(r);
                RuleTime started=Time(r),work=Time(r),updated=Time(r);RuleTime? completed=OptionalTime(r);
                var status=(FishingTrapRetrievalStatus)r.ReadInt32();
                s.FishingTrapRetrievals[i]=new FishingTrapRetrievalRecord(id,attempt,trap,worker,destination,started,work,updated,completed,status);
            }
            if(schema<Snapshot.FishingStockSchema)return;
            s.FishingStockManifests=new FishingStockManifestRecord[Count(r)];
            for(int i=0;i<s.FishingStockManifests.Length;i++) {
                string id=Text(r),shared=Text(r),version=Text(r);RuleTime from=Time(r);RuleTime? until=OptionalTime(r);
                string[] members=new string[Count(r)];for(int j=0;j<members.Length;j++)members[j]=Text(r);
                s.FishingStockManifests[i]=new FishingStockManifestRecord(id,shared,version,from,until,members);
            }
            s.FishingStockAllocations=new FishingStockAllocationRecord[Count(r)];
            for(int i=0;i<s.FishingStockAllocations.Length;i++) {
                string id=Text(r),manifest=Text(r),opportunity=Text(r);bool whole=Bool(r);
                string[] members=new string[Count(r)];for(int j=0;j<members.Length;j++)members[j]=Text(r);
                s.FishingStockAllocations[i]=new FishingStockAllocationRecord(id,manifest,opportunity,whole,members);
            }
        }
    }
}
