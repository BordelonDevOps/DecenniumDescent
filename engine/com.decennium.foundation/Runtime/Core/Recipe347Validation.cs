using System;
using System.Linq;

namespace Decennium.Foundation
{
    public static class Recipe347Validation
    {
        public const int MaxRecords=4096;
        private static readonly string[] ComponentUnits={"ing-347-0-wooden_handle","ing-347-1-metal_head",
            "ing-347-2-extraction_tools","ing-347-3-reinforced_grip","drop-silver_dragon_rib"};
        private static readonly long[] ComponentAmounts={5,3,1,1,1};
        private static readonly RuleTime[] Phases={new RuleTime(900),new RuleTime(27900),new RuleTime(28800),
            new RuleTime(28800),new RuleTime(28800),new RuleTime(28800)};
        private static RuleTime Add(RuleTime a,RuleTime b)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator*b.Denominator
                +(System.Numerics.BigInteger)b.Numerator*a.Denominator,(System.Numerics.BigInteger)a.Denominator*b.Denominator);
        private static RuleTime Subtract(RuleTime a,RuleTime b)
            =>RuleTime.FromFraction((System.Numerics.BigInteger)a.Numerator*b.Denominator
                -(System.Numerics.BigInteger)b.Numerator*a.Denominator,(System.Numerics.BigInteger)a.Denominator*b.Denominator);
        private static RuleTime Sum(System.Collections.Generic.IEnumerable<RuleTime> values)
        {
            var quantity=RuleQuantity.Sum(values.Select(x=>new RuleQuantity(x.Numerator,x.Denominator)));
            return new RuleTime(quantity.Numerator,quantity.Denominator);
        }
        private static bool Successful(CraftQuality quality)
            =>quality==CraftQuality.Flawed||quality==CraftQuality.Standard||quality==CraftQuality.Exceptional||quality==CraftQuality.Masterwork;
        private static long ExpectedMaximumHp(CraftQuality quality,CraftQualityChoice choice)
            =>quality==CraftQuality.Flawed?2:quality==CraftQuality.Exceptional&&choice==CraftQualityChoice.Durability?6
                :quality==CraftQuality.Masterwork&&choice==CraftQualityChoice.Durability?7:5;
        private static bool SegmentIsRemovalWork(Snapshot s,MiningAttemptRecord attempt,
            Recipe347MiningToolWorkSegmentRecord segment)
        {
            RuleTime cursor=default;
            RuleTime stageStart=new RuleTime(attempt.SetupSeconds);
            RuleTime stageEnd=new RuleTime(checked(attempt.SetupSeconds+attempt.RemovalSeconds));
            foreach(var interval in s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id)
                .OrderBy(x=>x.Start).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                if(interval.Start>=s.RuleClock)continue;
                RuleTime actualEnd=interval.End<s.RuleClock?interval.End:s.RuleClock;
                if(actualEnd<=interval.Start)continue;
                RuleTime activeEnd=Add(cursor,Subtract(actualEnd,interval.Start));
                RuleTime overlapStart=cursor>stageStart?cursor:stageStart;
                RuleTime overlapEnd=activeEnd<stageEnd?activeEnd:stageEnd;
                if(overlapEnd>overlapStart) {
                    RuleTime actualStart=Add(interval.Start,Subtract(overlapStart,cursor));
                    RuleTime actualStop=Add(interval.Start,Subtract(overlapEnd,cursor));
                    if(segment.Start>=actualStart&&segment.End<=actualStop)return true;
                }
                cursor=activeEnd;
            }
            return false;
        }

        public static void Validate(Snapshot s)
        {
            if(s.Recipe347FormulaAccess==null||s.Recipe347TradeSpecialties==null||s.Recipe347Workshops==null
                ||s.Recipe347WorkOrders==null||s.Recipe347Outputs==null||s.Recipe347MiningToolProfiles==null
                ||s.Recipe347MiningToolUseEvidence==null||s.Recipe347MiningToolWorkSegments==null
                ||s.Recipe347FormulaAccess.Length>MaxRecords||s.Recipe347TradeSpecialties.Length>MaxRecords
                ||s.Recipe347Workshops.Length>MaxRecords||s.Recipe347WorkOrders.Length>MaxRecords
                ||s.Recipe347Outputs.Length>MaxRecords||s.Recipe347MiningToolProfiles.Length>MaxRecords
                ||s.Recipe347MiningToolUseEvidence.Length>MaxRecords||s.Recipe347MiningToolWorkSegments.Length>MaxRecords
                ||s.Recipe347FormulaAccess.Any(x=>x==null)||s.Recipe347TradeSpecialties.Any(x=>x==null)
                ||s.Recipe347Workshops.Any(x=>x==null)||s.Recipe347WorkOrders.Any(x=>x==null)
                ||s.Recipe347Outputs.Any(x=>x==null)||s.Recipe347MiningToolProfiles.Any(x=>x==null)
                ||s.Recipe347MiningToolUseEvidence.Any(x=>x==null)||s.Recipe347MiningToolWorkSegments.Any(x=>x==null))
                throw new ArgumentException("Invalid recipe-347 collections.");
            int total=s.Recipe347FormulaAccess.Length+s.Recipe347TradeSpecialties.Length+s.Recipe347Workshops.Length
                +s.Recipe347WorkOrders.Length+s.Recipe347Outputs.Length+s.Recipe347MiningToolProfiles.Length
                +s.Recipe347MiningToolUseEvidence.Length+s.Recipe347MiningToolWorkSegments.Length;
            if(s.SchemaVersion<Snapshot.Recipe347Schema) {
                if(total!=0)throw new ArgumentException("Recipe-347 records require schema72.");
                return;
            }
            if(!s.TestOnly)throw new ArgumentException("Recipe-347 profile is TEST_ONLY.");
            Unique(s.Recipe347FormulaAccess.Select(x=>x.Id));
            Unique(s.Recipe347TradeSpecialties.Select(x=>x.Id));
            Unique(s.Recipe347Workshops.Select(x=>x.Id));
            Unique(s.Recipe347WorkOrders.Select(x=>x.Id));
            Unique(s.Recipe347Outputs.Select(x=>x.Id));
            Unique(s.Recipe347Outputs.Select(x=>x.OrderId));
            Unique(s.Recipe347MiningToolProfiles.Select(x=>x.Id));
            Unique(s.Recipe347MiningToolProfiles.Select(x=>x.ItemId));
            Unique(s.Recipe347MiningToolUseEvidence.Select(x=>x.Id));
            Unique(s.Recipe347MiningToolUseEvidence.Select(x=>x.AttemptId));
            if(s.Recipe347MiningToolWorkSegments.GroupBy(x=>x.AttemptId).Any(g=>g.OrderBy(x=>x.Start)
                .Zip(g.OrderBy(x=>x.Start).Skip(1),(a,b)=>a.End>b.Start).Any(x=>x)))
                throw new ArgumentException("Overlapping recipe-347 Mining Tool participation segments.");
            foreach(var access in s.Recipe347FormulaAccess)
                if(!Actor(s,access.ActorId)||access.RecipeId!="recipe-347")throw new ArgumentException("Unknown recipe-347 formula access.");
            foreach(var specialty in s.Recipe347TradeSpecialties) {
                var trade=s.Trades.SingleOrDefault(x=>x.WorkerId==specialty.ActorId&&x.TradeId==specialty.TradeId);
                if(!Actor(s,specialty.ActorId)||specialty.TradeId!="Mining"||specialty.ScopeId!="recipe-347"
                    ||trade==null||trade.Level<10)throw new ArgumentException("Recipe-347 specialty lacks its recorded level-10 Mining trade.");
            }
            foreach(var workshop in s.Recipe347Workshops)
                if(!workshop.ProperWorkshop||!s.Structures.Any(x=>x.Id==workshop.StationStructureId&&x.LocationId==workshop.SiteId)
                    ||!s.MiningDeposits.Any(x=>x.SiteId==workshop.SiteId&&x.SiteX==workshop.SiteX&&x.SiteY==workshop.SiteY
                        &&x.WorkSurfaceId==workshop.StationStructureId))
                    throw new ArgumentException("Recipe-347 workshop is not backed by its actual station and mining site.");

            foreach(var order in s.Recipe347WorkOrders)ValidateOrder(s,order);
            foreach(var output in s.Recipe347Outputs)ValidateOutput(s,output);
            foreach(var profile in s.Recipe347MiningToolProfiles)ValidateMiningToolProfile(s,profile);
            foreach(var evidence in s.Recipe347MiningToolUseEvidence)ValidateMiningEvidence(s,evidence);
            foreach(var segment in s.Recipe347MiningToolWorkSegments) {
                var attempt=s.MiningAttempts.SingleOrDefault(x=>x.Id==segment.AttemptId);
                var evidence=s.Recipe347MiningToolUseEvidence.SingleOrDefault(x=>x.AttemptId==segment.AttemptId);
                if(attempt==null||evidence==null||segment.End>s.RuleClock||!SegmentIsRemovalWork(s,attempt,segment))
                    throw new ArgumentException("Recipe-347 tool work segment is outside its actual extraction interval.");
            }
        }

        private static void ValidateOrder(Snapshot s,Recipe347WorkOrderRecord order)
        {
            var access=s.Recipe347FormulaAccess.SingleOrDefault(x=>x.Id==order.FormulaAccessId);
            var specialty=s.Recipe347TradeSpecialties.SingleOrDefault(x=>x.Id==order.SpecialtyId);
            var workshop=s.Recipe347Workshops.SingleOrDefault(x=>x.Id==order.WorkshopId);
            var worker=s.Actors.SingleOrDefault(x=>x.Id==order.WorkerId);
            var body=s.PortableEquipment.SingleOrDefault(x=>x.Id==order.BodyItemId);
            var structure=s.Structures.SingleOrDefault(x=>x.Id==order.BodyStructureId);
            var bodyLot=s.Work.Lots.SingleOrDefault(x=>x.Id==order.BodyLotId);
            var bodyInventory=s.InventoryLots.SingleOrDefault(x=>x.LotId==order.BodyLotId);
            var output=s.Recipe347Outputs.SingleOrDefault(x=>x.Id==order.OutputProvenanceId);
            bool success=Successful(order.Quality);
            if(worker==null||access==null||access.ActorId!=order.WorkerId||specialty==null||specialty.ActorId!=order.WorkerId
                ||workshop==null||body==null||structure==null||bodyLot==null||bodyInventory==null
                ||order.UpdatedAt>s.RuleClock||order.StartedAt>s.RuleClock||order.Ability!=CharacterAbility.Strength&&order.Ability!=CharacterAbility.Wisdom
                ||body.OwnerId!=bodyInventory.OwnerId||body.LinkedId!=order.BodyLotId||body.LinkKind!=PortableLinkKind.InventoryLot
                ||bodyLot.Amount!=new RuleQuantity(3)||bodyInventory.CreatedAmount!=new RuleQuantity(3)
                ||body.SourceWeightLb!=new RuleQuantity(3)||body.OperationalWeightLb.HasValue
                ||structure.MassPounds!=new RuleQuantity(3)||structure.Material!=ObjectMaterial.WoodLeather
                ||order.ComponentLotIds.Any(id=>!s.Work.Lots.Any(x=>x.Id==id))
                ||!order.ImplementIds.SequenceEqual(workshop.ImplementIds,StringComparer.Ordinal)
                ||!s.Work.Reservations.Any(x=>x.JobId==order.Id&&x.Id==order.Id+".body"&&x.LotId==order.BodyLotId
                    &&x.Amount==new RuleQuantity(3))
                ||order.Status==Recipe347OrderStatus.Complete&&(!success||output==null||output.OrderId!=order.Id)
                ||order.Status!=Recipe347OrderStatus.Complete&&output!=null
                ||success!=(order.Status==Recipe347OrderStatus.Complete||order.Status==Recipe347OrderStatus.AwaitingChoice
                    ||order.Status==Recipe347OrderStatus.AwaitingSettlement&&success)
                ||order.Status==Recipe347OrderStatus.AwaitingSettlement
                ||order.Status==Recipe347OrderStatus.AwaitingChoice&&output!=null
                ||s.Work.Reservations.Count(x=>x.JobId==order.Id)!=6)
                throw new ArgumentException("Recipe-347 order lost its authoritative worker, material or body claim.");
            var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==order.Id).ToArray();
            if(order.ComponentLotIds.Count!=5||!order.Work.Phases.SequenceEqual(Phases))
                throw new ArgumentException("Recipe-347 order changed its reviewed component plan or active-work phases.");
            if(intervals.Any(x=>x.WorkerId!=order.WorkerId||x.Start<order.StartedAt))
                throw new ArgumentException("Recipe-347 interval belongs to another worker.");
            RuleTime labor=Sum(intervals.Where(x=>x.Start<s.RuleClock).Select(x=>Subtract(x.End<s.RuleClock?x.End:s.RuleClock,x.Start)));
            if(labor!=order.Work.Labor)throw new ArgumentException("Recipe-347 credited labor differs from its booked work intervals.");
            var active=intervals.Where(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock).ToArray();
            if(order.Status==Recipe347OrderStatus.Working?active.Length!=1:active.Length!=0)
                throw new ArgumentException("Recipe-347 active status and worker interval disagree.");
            if(order.Status==Recipe347OrderStatus.Working&&active[0].End>s.RuleClock.AddSeconds(8*60*60))
                throw new ArgumentException("Recipe-347 work exceeds its booked Watch.");
            for(int i=0;i<5;i++) {
                var claim=s.Work.Reservations.SingleOrDefault(x=>x.JobId==order.Id&&x.Id==order.Id+".component"+i.ToString(System.Globalization.CultureInfo.InvariantCulture));
                var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==order.ComponentLotIds[i]);
                if(claim==null||claim.LotId!=order.ComponentLotIds[i]||claim.Amount!=new RuleQuantity(ComponentAmounts[i])
                    ||lot==null||lot.UnitId!=ComponentUnits[i])throw new ArgumentException("Recipe-347 component claim mismatch.");
                RuleQuantity expectedConsumed=default;
                bool finalized=!order.Open;
                bool abandonConsumed=order.Status==Recipe347OrderStatus.Cancelled&&order.Work.Labor>default(RuleTime);
                if(order.Status==Recipe347OrderStatus.Complete||order.Status==Recipe347OrderStatus.Mishap||abandonConsumed) {
                    if(i!=2)expectedConsumed=new RuleQuantity(ComponentAmounts[i]);
                } else if(order.Status==Recipe347OrderStatus.Failed&&i!=2) {
                    expectedConsumed=new RuleQuantity(ComponentAmounts[i])-new RuleQuantity(ComponentAmounts[i]/4);
                }
                if(claim.ConsumedAmount!=expectedConsumed
                    ||order.Open&&claim.ReleasedAmount!=default(RuleQuantity)
                    ||finalized&&claim.ReleasedAmount!=claim.Amount-expectedConsumed)
                    throw new ArgumentException("Recipe-347 settlement differs from the source component disposition.");
            }
            var bodyClaim=s.Work.Reservations.Single(x=>x.JobId==order.Id&&x.Id==order.Id+".body");
            if(bodyClaim.ConsumedAmount!=default(RuleQuantity)||order.Open&&bodyClaim.ReleasedAmount!=default(RuleQuantity)
                ||!order.Open&&bodyClaim.ReleasedAmount!=bodyClaim.Amount)
                throw new ArgumentException("Recipe-347 mundane body was consumed or not released exactly once.");
        }

        private static void ValidateOutput(Snapshot s,Recipe347OutputProvenanceRecord output)
        {
            var order=s.Recipe347WorkOrders.SingleOrDefault(x=>x.Id==output.OrderId);
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==output.ItemId);
            var structure=s.Structures.SingleOrDefault(x=>x.Id==output.StructureId);
            if(order==null||order.Status!=Recipe347OrderStatus.Complete||order.OutputProvenanceId!=output.Id
                ||order.BodyItemId!=output.ItemId||order.BodyStructureId!=output.StructureId
                ||output.CreatedAt!=order.UpdatedAt||output.Revision>s.Revision
                ||output.MaximumHp!=ExpectedMaximumHp(output.Quality,output.Choice)
                ||output.Hp!=Math.Max(0,output.MaximumHp-(output.PreviousMaximumHp-output.PreviousHp))
                ||item==null||structure==null||structure.MaximumHp!=output.MaximumHp||structure.Hp!=output.Hp
                ||item.Id!=output.ItemId||structure.Id!=output.StructureId)
                throw new ArgumentException("Recipe-347 output provenance does not match the transformed body.");
        }

        private static void ValidateMiningToolProfile(Snapshot s,Recipe347MiningToolProfileRecord profile)
        {
            var output=s.Recipe347Outputs.SingleOrDefault(x=>x.Id==profile.ProvenanceId);
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==profile.ItemId);
            var structure=s.Structures.SingleOrDefault(x=>x.Id==profile.StructureId);
            if(output==null||output.ItemId!=profile.ItemId||output.StructureId!=profile.StructureId
                ||output.MaximumHp!=profile.MaximumHp||item==null||structure==null
                ||structure.MaximumHp!=profile.MaximumHp||structure.Material!=ObjectMaterial.WoodLeather
                ||structure.MassPounds!=new RuleQuantity(3)||item.SourceWeightLb!=new RuleQuantity(3)
                ||item.OperationalWeightLb.HasValue)
                throw new ArgumentException("Reusable recipe-347 profile is not bound to its transformed item.");
        }

        private static void ValidateMiningEvidence(Snapshot s,Recipe347MiningToolUseEvidenceRecord evidence)
        {
            var attempt=s.MiningAttempts.SingleOrDefault(x=>x.Id==evidence.AttemptId);
            var profile=s.Recipe347MiningToolProfiles.SingleOrDefault(x=>x.Id==evidence.ProfileId);
            var deposit=s.MiningDeposits.SingleOrDefault(x=>x.Id==evidence.DepositId);
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==evidence.ItemId);
            var structure=s.Structures.SingleOrDefault(x=>x.Id==profile?.StructureId);
            bool selectedMatches=attempt!=null&&attempt.SelectedUnitIds.SequenceEqual(evidence.SelectedUnitIds,StringComparer.Ordinal);
            if(attempt==null||profile==null||deposit==null||item==null||structure==null
                ||attempt.DepositId!=evidence.DepositId||attempt.DepositVersionId!=evidence.DepositVersionId
                ||attempt.WorkerId!=evidence.WorkerId||attempt.StartedAt!=evidence.CapturedAt||profile.ItemId!=evidence.ItemId
                ||!selectedMatches||evidence.Placement!=PortablePlacement.Ground||evidence.GroundX!=deposit.SiteX
                ||evidence.GroundY!=deposit.SiteY||Math.Abs((long)evidence.WorkerX-deposit.SiteX)
                    +Math.Abs((long)evidence.WorkerY-deposit.SiteY)>1||evidence.StructureHp<=0
                ||evidence.StructureMaximumHp!=profile.MaximumHp||structure.LocationId!=evidence.StructureLocationId
                ||evidence.WorkSurfaceId!=deposit.WorkSurfaceId||evidence.WorkSurfaceBroken
                ||evidence.ReceiverId!=deposit.ReceiverId||!evidence.ReceiverOpen||evidence.AvailableHands<2
                ||evidence.CapturedAt>s.RuleClock||item.Id!=profile.ItemId||structure.Id!=profile.StructureId)
                throw new ArgumentException("Reusable Mining Tool evidence is not bound to its actual attempt and deposit version.");
        }

        private static bool Actor(Snapshot s,string actor)=>s.Actors.Any(x=>x.Id==actor);
        private static void Unique(System.Collections.Generic.IEnumerable<string> values)
        {if(values.Distinct(StringComparer.Ordinal).Count()!=values.Count())throw new ArgumentException("Duplicate recipe-347 identity.");}
    }
}
