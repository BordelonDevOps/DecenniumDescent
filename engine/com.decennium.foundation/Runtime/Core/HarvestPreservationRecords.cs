using System;
using System.Linq;

namespace Decennium.Foundation
{
    // Ordinary and Spoiled are query-only projections for the agreed eligibility matrix.
    // The TEST_ONLY reservation/work adapter below deliberately persists Fresh only.
    public enum HarvestIngredientRequirement { Fresh = 1, Ordinary = 2, Spoiled = 3 }
    public enum HarvestRequirementWorkStatus { Working = 1, Paused = 2 }
    public enum HarvestRequirementPauseReason { None = 0, Explicit = 1, IngredientNotFresh = 2, WorkerUnavailable = 3 }
    public enum HarvestPreservationTreatmentStatus { Working = 1, Success = 2, Failure = 3 }
    public enum HarvestPreservationTreatmentDegree { None = 0, CriticalFailure = 1, Failure = 2, Success = 3, CriticalSuccess = 4 }
    public enum HarvestPreservationEvidenceKind { ControlledOpening = 1, InVesselPortion = 2, Exposure = 3 }
    public enum HarvestPreservationExposureCause { None = 0, Breach = 1, Contamination = 2, IncompatibleHeat = 3 }

    /// <summary>Immutable schema76 TEST_ONLY association between a committed command and the
    /// portable/inventory facts it caused. Current protection and age are derived from these
    /// records; this record never stores quantity, location, or an active protection flag.</summary>
    public sealed class HarvestPreservationEvidenceRecord
    {
        public string Id { get; }
        public HarvestPreservationEvidenceKind Kind { get; }
        public string TreatmentAttemptId { get; }
        public string VesselId { get; }
        public string CommandId { get; }
        public long AppliedRevision { get; }
        public RuleTime At { get; }
        public string PortableHandlingId { get; }
        public string ToolId { get; }
        public string CleanToolFactId { get; }
        public string OpeningEvidenceId { get; }
        public string ChildLotId { get; }
        public string OccurrenceId { get; }
        public HarvestPreservationExposureCause Cause { get; }

        public HarvestPreservationEvidenceRecord(string id,HarvestPreservationEvidenceKind kind,string treatmentAttemptId,
            string vesselId,string commandId,long appliedRevision,RuleTime at,string portableHandlingId="",string toolId="",
            string cleanToolFactId="",string openingEvidenceId="",string childLotId="",string occurrenceId="",
            HarvestPreservationExposureCause cause=HarvestPreservationExposureCause.None)
        {
            if(!Validation.ValidId(id)||!Enum.IsDefined(typeof(HarvestPreservationEvidenceKind),kind)
                ||!Validation.ValidId(treatmentAttemptId)||!Validation.ValidId(vesselId)||!Validation.ValidId(commandId)
                ||appliedRevision<1||at<default(RuleTime)
                ||portableHandlingId==null||portableHandlingId!=""&&!Validation.ValidId(portableHandlingId)
                ||toolId==null||toolId!=""&&!Validation.ValidId(toolId)
                ||cleanToolFactId==null||cleanToolFactId!=""&&!Validation.ValidId(cleanToolFactId)
                ||openingEvidenceId==null||openingEvidenceId!=""&&!Validation.ValidId(openingEvidenceId)
                ||childLotId==null||childLotId!=""&&!Validation.ValidId(childLotId)
                ||occurrenceId==null||occurrenceId!=""&&!Validation.ValidId(occurrenceId)
                ||!Enum.IsDefined(typeof(HarvestPreservationExposureCause),cause))
                throw new ArgumentException("Invalid harvest preservation evidence.");
            bool opening=kind==HarvestPreservationEvidenceKind.ControlledOpening
                &&portableHandlingId!=""&&toolId!=""&&cleanToolFactId!=""&&openingEvidenceId==""&&childLotId==""&&occurrenceId==""
                &&cause==HarvestPreservationExposureCause.None;
            bool portion=kind==HarvestPreservationEvidenceKind.InVesselPortion
                &&portableHandlingId==""&&toolId==""&&cleanToolFactId==""&&openingEvidenceId!=""&&childLotId!=""&&occurrenceId==""
                &&cause==HarvestPreservationExposureCause.None;
            bool exposure=kind==HarvestPreservationEvidenceKind.Exposure
                &&portableHandlingId==""&&toolId==""&&cleanToolFactId==""&&openingEvidenceId==""&&childLotId==""&&occurrenceId!=""
                &&cause!=HarvestPreservationExposureCause.None;
            if(!opening&&!portion&&!exposure)throw new ArgumentException("Evidence fields do not match its kind.");
            Id=id;Kind=kind;TreatmentAttemptId=treatmentAttemptId;VesselId=vesselId;CommandId=commandId;
            AppliedRevision=appliedRevision;At=at;PortableHandlingId=portableHandlingId;ToolId=toolId;CleanToolFactId=cleanToolFactId;
            OpeningEvidenceId=openingEvidenceId;ChildLotId=childLotId;OccurrenceId=occurrenceId;Cause=cause;
        }
    }

    public static class HarvestPreservationEvidenceValidation
    {
        public const int MaxRecords=128;
        public const int OpeningLimitSeconds=60;

        public static void Validate(Snapshot s)
        {
            if(s.HarvestPreservationEvidence==null||s.HarvestPreservationEvidence.Length>MaxRecords
                ||s.HarvestPreservationEvidence.Any(x=>x==null)
                ||s.HarvestPreservationEvidence.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()
                    !=s.HarvestPreservationEvidence.Length)
                throw new ArgumentException("Invalid harvest preservation evidence collection.");
            if(s.SchemaVersion<Snapshot.HarvestPreservationExposureSchema||s.SchemaVersion==Snapshot.MiningAssistantSchema) {
                if(s.HarvestPreservationEvidence.Length!=0)
                    throw new ArgumentException("Harvest preservation evidence requires schema76.");
                return;
            }
            if(s.SchemaVersion!=Snapshot.HarvestPreservationExposureSchema||!s.TestOnly
                ||s.HarvestRequirementWorks.Length!=0)
                throw new ArgumentException("Schema76 is a TEST_ONLY treatment/exposure profile without schema74 work.");

            var ordered=s.HarvestPreservationEvidence.OrderBy(x=>x.AppliedRevision).ToArray();
            if(!s.HarvestPreservationEvidence.SequenceEqual(ordered)
                ||ordered.Select(x=>x.AppliedRevision).Distinct().Count()!=ordered.Length
                ||ordered.Zip(ordered.Skip(1),(a,b)=>a.At<=b.At).Any(x=>!x))
                throw new ArgumentException("Harvest preservation evidence must retain causal order.");
            if(ordered.Where(x=>x.Kind==HarvestPreservationEvidenceKind.ControlledOpening)
                    .Select(x=>x.PortableHandlingId).Distinct(StringComparer.Ordinal).Count()
                    !=ordered.Count(x=>x.Kind==HarvestPreservationEvidenceKind.ControlledOpening)
                ||ordered.Where(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion)
                    .Select(x=>x.OpeningEvidenceId).Distinct(StringComparer.Ordinal).Count()
                    !=ordered.Count(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion)
                ||ordered.Where(x=>x.Kind==HarvestPreservationEvidenceKind.Exposure)
                    .Select(x=>x.OccurrenceId).Distinct(StringComparer.Ordinal).Count()
                    !=ordered.Count(x=>x.Kind==HarvestPreservationEvidenceKind.Exposure))
                throw new ArgumentException("Harvest preservation openings, portions, and occurrences are once-only.");

            foreach(var evidence in ordered) {
                if(evidence.AppliedRevision>s.Revision||evidence.At>s.RuleClock)
                    throw new ArgumentException("Harvest preservation evidence is from the future.");
                var receipt=s.Receipts.SingleOrDefault(x=>x.Revision==evidence.AppliedRevision&&x.Id==evidence.CommandId);
                if(receipt==null)throw new ArgumentException("Harvest preservation evidence has no committed command receipt.");
                var command=CommandHistory.Read(receipt);
                var treatment=s.HarvestPreservationTreatmentAttempts.SingleOrDefault(x=>x.Id==evidence.TreatmentAttemptId
                    &&x.Status==HarvestPreservationTreatmentStatus.Success&&x.CompletedAt.HasValue
                    &&x.ContainerId==evidence.VesselId);
                if(treatment==null||treatment.CompletedAt.Value>evidence.At)
                    throw new ArgumentException("Harvest preservation evidence has no completed source treatment.");
                if(evidence.Kind==HarvestPreservationEvidenceKind.ControlledOpening) {
                    var handling=s.PortableHandling.SingleOrDefault(x=>x.Id==evidence.PortableHandlingId
                        &&x.Revision==evidence.AppliedRevision&&x.ItemId==evidence.VesselId
                        &&x.Operation==PortableOperation.Open&&x.ActorId==command.Actor&&x.EndedAt==evidence.At);
                    if(command.Kind!=CommandKind.OpenPortableContainer||command.Target!=evidence.VesselId
                        ||handling==null||handling.EndedAt!=handling.StartedAt.AddSeconds(1)
                        ||evidence.ToolId!=treatment.ToolId||!s.PortableEquipment.Any(x=>x.Id==evidence.ToolId))
                        throw new ArgumentException("Controlled opening does not match its physical handling and clean-tool binding.");
                    if(!HarvestPreservationRules.IsProtectedAtRevision(s,treatment.InventoryLotId,evidence.At,evidence.AppliedRevision))
                        throw new ArgumentException("Controlled opening evidence was not created during the treatment protection interval.");
                } else if(evidence.Kind==HarvestPreservationEvidenceKind.InVesselPortion) {
                    var opening=ordered.SingleOrDefault(x=>x.Id==evidence.OpeningEvidenceId
                        &&x.Kind==HarvestPreservationEvidenceKind.ControlledOpening
                        &&x.TreatmentAttemptId==evidence.TreatmentAttemptId&&x.VesselId==evidence.VesselId
                        &&x.AppliedRevision<evidence.AppliedRevision&&x.At<=evidence.At);
                    var child=s.InventoryLots.SingleOrDefault(x=>x.LotId==evidence.ChildLotId);
                    var childLot=s.Work.Lots.SingleOrDefault(x=>x.Id==evidence.ChildLotId);
                    var physical=s.PortableEquipment.SingleOrDefault(x=>x.Id==evidence.ChildLotId
                        &&x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==evidence.ChildLotId);
                    var laterHandling=s.PortableHandling.Where(x=>x.ItemId==evidence.ChildLotId
                        &&x.Revision>evidence.AppliedRevision).OrderBy(x=>x.Revision).ToArray();
                    var firstLaterHandling=laterHandling.FirstOrDefault();
                    bool closedBetween=opening!=null&&s.PortableHandling.Any(x=>x.ItemId==evidence.VesselId
                        &&x.Operation==PortableOperation.Close&&x.Revision>opening.AppliedRevision
                        &&x.Revision<evidence.AppliedRevision);
                    bool wasContainedAtCreation=physical!=null&&physical.ParentId==evidence.VesselId
                        &&physical.Placement==PortablePlacement.Contained
                        ||firstLaterHandling!=null&&firstLaterHandling.Operation==PortableOperation.Retrieve
                            &&firstLaterHandling.FromParentId==evidence.VesselId
                            &&firstLaterHandling.EndedAt>=evidence.At;
                    if(command.Kind!=CommandKind.PortionInventory||command.Target!=treatment.InventoryLotId
                        ||command.Inventory==null||command.Inventory.Destination!=""
                        ||command.Inventory.Handling!=HandlingKind.Pickup||opening==null||closedBetween
                        ||!HarvestPreservationRules.IsProtectedAtRevision(s,treatment.InventoryLotId,evidence.At,evidence.AppliedRevision)
                        ||child==null||child.ParentId!=treatment.InventoryLotId||child.CreatedAt!=evidence.At
                        ||child.Nutrition!=NutritionKind.None||child.FreshUntil!=s.InventoryLots.Single(x=>x.LotId==treatment.InventoryLotId).FreshUntil
                        ||childLot==null||childLot.UnitId!="mass-pound"
                        ||command.Inventory.Amount!=child.CreatedAmount||physical==null||!wasContainedAtCreation
                        ||physical.MassBasis!=PortableMassBasis.GenericPounds)
                        throw new ArgumentException("In-vessel portion does not match its opening, child lot, and causal command.");
                } else {
                    if(command.Kind!=CommandKind.RecordHarvestPreservationExposure||command.Target!=evidence.OccurrenceId
                        ||command.X!=0||command.Y!=0||command.Inventory!=null||command.Combat!=null
                        ||command.Advancement!=null||command.Ranged!=null||command.ProspectingExposure!=null
                        ||command.OverwatchRider!=OverwatchRider.None||command.SuppressionFire!=null
                        ||command.DefensiveFormation!=null||command.ExpeditionAssignment!=null
                        ||command.HarvestSelection!=null||command.MiningSelection!=null||command.RouteMappingWork!=null)
                        throw new ArgumentException("Harvest exposure does not match its committed occurrence command.");
                    if(!HarvestPreservationRules.IsProtectedAtRevision(s,treatment.InventoryLotId,evidence.At,evidence.AppliedRevision-1))
                        throw new ArgumentException("Harvest exposure did not occur while treatment protection was active.");
                }
            }
        }
    }

    /// <summary>Read-only preservation facts derived from one physical inventory descendant and its
    /// extracted harvest root. No age, stage or value is copied into saved state.</summary>
    public sealed class HarvestPreservationView
    {
        public string InventoryLotId { get; }
        public string HarvestUnitId { get; }
        public RuleTime EvaluatedAt { get; }
        public RuleTime UnprotectedAge { get; }
        public HarvestPreservationState State { get; }
        public RuleQuantity ValueMultiplier { get; }

        internal HarvestPreservationView(string inventoryLotId,string harvestUnitId,RuleTime evaluatedAt,RuleTime unprotectedAge,
            HarvestPreservationState state,RuleQuantity valueMultiplier)
        {
            InventoryLotId=inventoryLotId;HarvestUnitId=harvestUnitId;EvaluatedAt=evaluatedAt;UnprotectedAge=unprotectedAge;
            State=state;ValueMultiplier=valueMultiplier;
        }
    }

    /// <summary>Schema-74 projection over the existing harvest and inventory authorities.</summary>
    public static class HarvestPreservationRules
    {
        public static bool SatisfiesRequirement(HarvestPreservationView view,HarvestIngredientRequirement requirement)
        {
            if(view==null||!Enum.IsDefined(typeof(HarvestIngredientRequirement),requirement))return false;
            switch(requirement) {
                case HarvestIngredientRequirement.Fresh:return view.State==HarvestPreservationState.Fresh;
                case HarvestIngredientRequirement.Ordinary:return view.State==HarvestPreservationState.Fresh
                    ||view.State==HarvestPreservationState.Degraded;
                case HarvestIngredientRequirement.Spoiled:return view.State==HarvestPreservationState.Spoiled;
                default:return false;
            }
        }

        public static bool TryProject(Snapshot s,string inventoryLotId,out HarvestPreservationView view)
            =>TryProjectAt(s,inventoryLotId,s?.RuleClock??default,out view);

        /// <summary>Reports coverage derived from treatment, opening, exposure, and physical
        /// retrieval history. Schema75 retains its exact-lot rule; schema76 admits only a
        /// directly evidenced in-vessel child.</summary>
        public static bool IsProtectedAt(Snapshot s,string inventoryLotId,RuleTime at)
        {
            if(s==null||s.HarvestPreservationTreatmentAttempts==null)return false;
            if(s.SchemaVersion==Snapshot.HarvestPreservationTreatmentSchema)
                return s.HarvestPreservationTreatmentAttempts.Any(x=>x.Status==HarvestPreservationTreatmentStatus.Success
                    &&x.InventoryLotId==inventoryLotId&&x.CompletedAt.HasValue&&x.CompletedAt.Value<=at
                    &&at<x.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds));
            if(s.SchemaVersion!=Snapshot.HarvestPreservationExposureSchema)return false;
            var attempt=s.HarvestPreservationTreatmentAttempts.SingleOrDefault(x=>x.Status==HarvestPreservationTreatmentStatus.Success
                &&x.CompletedAt.HasValue&&(x.InventoryLotId==inventoryLotId
                    ||s.HarvestPreservationEvidence.Any(e=>e.Kind==HarvestPreservationEvidenceKind.InVesselPortion
                        &&e.TreatmentAttemptId==x.Id&&e.ChildLotId==inventoryLotId)));
            if(attempt==null||attempt.CompletedAt.Value>at)return false;
            RuleTime end=ProtectionEnd(s,attempt,inventoryLotId,at,long.MaxValue);
            if(attempt.InventoryLotId==inventoryLotId)return at<end;
            var portion=s.HarvestPreservationEvidence.SingleOrDefault(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion
                &&x.TreatmentAttemptId==attempt.Id&&x.ChildLotId==inventoryLotId);
            return portion!=null&&portion.At<=at&&at<end;
        }

        internal static bool IsProtectedAtRevision(Snapshot s,string inventoryLotId,RuleTime at,long throughRevision)
        {
            if(s==null||s.SchemaVersion!=Snapshot.HarvestPreservationExposureSchema||throughRevision<0)return false;
            var attempt=s.HarvestPreservationTreatmentAttempts.SingleOrDefault(x=>x.Status==HarvestPreservationTreatmentStatus.Success
                &&x.CompletedAt.HasValue&&(x.InventoryLotId==inventoryLotId
                    ||s.HarvestPreservationEvidence.Any(e=>e.AppliedRevision<=throughRevision
                        &&e.Kind==HarvestPreservationEvidenceKind.InVesselPortion
                        &&e.TreatmentAttemptId==x.Id&&e.ChildLotId==inventoryLotId)));
            if(attempt==null||attempt.CompletedAt.Value>at)return false;
            RuleTime end=ProtectionEnd(s,attempt,inventoryLotId,at,throughRevision);
            if(attempt.InventoryLotId==inventoryLotId)return at<end;
            var portion=s.HarvestPreservationEvidence.SingleOrDefault(x=>x.AppliedRevision<=throughRevision
                &&x.Kind==HarvestPreservationEvidenceKind.InVesselPortion&&x.TreatmentAttemptId==attempt.Id
                &&x.ChildLotId==inventoryLotId);
            return portion!=null&&portion.At<=at&&at<end;
        }

        public static RuleTime? NextCoverageBoundary(Snapshot s)
        {
            if(s==null||s.SchemaVersion!=Snapshot.HarvestPreservationExposureSchema)return null;
            RuleTime? next=null;
            void Consider(RuleTime value)
            { if(value>s.RuleClock&&(!next.HasValue||value<next.Value))next=value; }
            foreach(var attempt in s.HarvestPreservationTreatmentAttempts.Where(x=>x.Status==HarvestPreservationTreatmentStatus.Success
                &&x.CompletedAt.HasValue))Consider(attempt.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds));
            foreach(var opening in s.HarvestPreservationEvidence.Where(x=>x.Kind==HarvestPreservationEvidenceKind.ControlledOpening)) {
                RuleTime deadline=opening.At.AddSeconds(HarvestPreservationEvidenceValidation.OpeningLimitSeconds);
                var close=s.PortableHandling.Where(x=>x.ItemId==opening.VesselId&&x.Operation==PortableOperation.Close
                    &&x.Revision>opening.AppliedRevision).OrderBy(x=>x.Revision).FirstOrDefault();
                if(close==null||close.EndedAt>=deadline)Consider(deadline);
            }
            return next;
        }

        public static bool TryProjectAt(Snapshot s,string inventoryLotId,RuleTime at,out HarvestPreservationView view)
        {
            view=null;
            if(s==null||s.SchemaVersion<Snapshot.HarvestPreservationSchema||s.InventoryLots==null
                ||s.HarvestUnits==null||s.Work==null||!Validation.ValidId(inventoryLotId))return false;
            var lot=s.InventoryLots.SingleOrDefault(x=>x.LotId==inventoryLotId);
            var resource=s.Work.Lots.SingleOrDefault(x=>x.Id==inventoryLotId);
            if(lot==null||resource==null||lot.Nutrition!=NutritionKind.None||resource.UnitId!="mass-pound")return false;
            if(s.SchemaVersion==Snapshot.HarvestPreservationExposureSchema&&at<lot.CreatedAt)return false;

            var seen=new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal){lot.LotId};
            var root=lot;
            while(root.ParentId!="") {
                if(!seen.Add(root.ParentId))return false;
                root=s.InventoryLots.SingleOrDefault(x=>x.LotId==root.ParentId);
                if(root==null)return false;
            }
            var unit=s.HarvestUnits.SingleOrDefault(x=>x.Id==root.LotId);
            if(unit==null||unit.Status!=HarvestUnitStatus.Extracted
                ||root.FreshUntil!=unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds))return false;
            var physical=s.PortableEquipment?.SingleOrDefault(x=>x.LinkKind==PortableLinkKind.InventoryLot
                &&x.LinkedId==lot.LotId);
            if(physical==null||physical.Id!=lot.LotId||physical.MassBasis!=PortableMassBasis.GenericPounds)return false;

            if(at<unit.OriginAt)return false;
            RuleTime age=UnprotectedAgeAt(s,lot,root,unit,at);
            RuleTime firstBoundary=new RuleTime(unit.PreservationIntervalSeconds);
            RuleTime secondBoundary=new RuleTime(checked(unit.PreservationIntervalSeconds*2L));
            HarvestPreservationState state=age<firstBoundary?HarvestPreservationState.Fresh
                :age<secondBoundary?HarvestPreservationState.Degraded:HarvestPreservationState.Spoiled;
            RuleQuantity multiplier=state==HarvestPreservationState.Fresh?new RuleQuantity(1)
                :state==HarvestPreservationState.Degraded?new RuleQuantity(1,2):default;
            view=new HarvestPreservationView(lot.LotId,unit.Id,at,age,state,multiplier);
            return true;
        }

        private static RuleQuantity Quantity(RuleTime value)=>new RuleQuantity(value.Numerator,value.Denominator);
        private static RuleTime Time(RuleQuantity value)=>new RuleTime(value.Numerator,value.Denominator);
        private static RuleTime Max(RuleTime a,RuleTime b)=>a>b?a:b;
        private static RuleTime Min(RuleTime a,RuleTime b)=>a<b?a:b;
        private static RuleTime UnprotectedAgeAt(Snapshot s,InventoryLotRecord lot,InventoryLotRecord root,
            HarvestMaterialUnitRecord unit,RuleTime at)
        {
            var lineage=new System.Collections.Generic.List<InventoryLotRecord>();
            var lineageIndex=new System.Collections.Generic.Dictionary<string,int>(StringComparer.Ordinal);
            var current=lot;
            while(true) {
                lineageIndex.Add(current.LotId,lineage.Count);
                lineage.Add(current);
                if(current.ParentId=="")break;
                current=s.InventoryLots.Single(x=>x.LotId==current.ParentId);
            }
            var intervals=new System.Collections.Generic.List<(RuleTime Start,RuleTime End)>();
            foreach(var attempt in s.HarvestPreservationTreatmentAttempts??Array.Empty<HarvestPreservationTreatmentAttemptRecord>()) {
                if(attempt.Status!=HarvestPreservationTreatmentStatus.Success||!attempt.CompletedAt.HasValue
                    ||!lineageIndex.TryGetValue(attempt.InventoryLotId,out int treatedIndex)||attempt.CompletedAt.Value>=at)continue;
                RuleTime protectionEnd=s.SchemaVersion==Snapshot.HarvestPreservationExposureSchema
                    ?ProtectionEnd(s,attempt,attempt.InventoryLotId,at,long.MaxValue)
                    :attempt.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds);
                RuleTime branchEnd=treatedIndex==0?at:Min(at,lineage[treatedIndex-1].CreatedAt);
                RuleTime start=Max(unit.OriginAt,attempt.CompletedAt.Value);
                RuleTime end=Min(Min(at,protectionEnd),branchEnd);
                if(end>start)intervals.Add((start,end));
            }
            if(s.SchemaVersion==Snapshot.HarvestPreservationExposureSchema) {
                foreach(var portion in (s.HarvestPreservationEvidence??Array.Empty<HarvestPreservationEvidenceRecord>())
                    .Where(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion&&lineageIndex.ContainsKey(x.ChildLotId)&&x.At<at)) {
                    var attempt=s.HarvestPreservationTreatmentAttempts.SingleOrDefault(x=>x.Id==portion.TreatmentAttemptId
                        &&x.Status==HarvestPreservationTreatmentStatus.Success&&x.CompletedAt.HasValue);
                    if(attempt==null)continue;
                    int portionIndex=lineageIndex[portion.ChildLotId];
                    RuleTime branchEnd=portionIndex==0?at:Min(at,lineage[portionIndex-1].CreatedAt);
                    RuleTime end=Min(Min(at,ProtectionEnd(s,attempt,portion.ChildLotId,at,long.MaxValue)),branchEnd);
                    if(end>portion.At)intervals.Add((portion.At,end));
                }
            }
            intervals.Sort((a,b)=>a.Start.CompareTo(b.Start));
            RuleTime protectedTime=default;
            if(intervals.Count>0) {
                RuleTime start=intervals[0].Start,end=intervals[0].End;
                for(int i=1;i<intervals.Count;i++) {
                    if(intervals[i].Start<=end)end=Max(end,intervals[i].End);
                    else {protectedTime=Time(Quantity(protectedTime)+(Quantity(end)-Quantity(start)));start=intervals[i].Start;end=intervals[i].End;}
                }
                protectedTime=Time(Quantity(protectedTime)+(Quantity(end)-Quantity(start)));
            }
            return Time(Quantity(at)-Quantity(unit.OriginAt)-Quantity(protectedTime));
        }

        private static RuleTime ProtectionEnd(Snapshot s,HarvestPreservationTreatmentAttemptRecord attempt,
            string inventoryLotId,RuleTime at,long throughRevision)
        {
            RuleTime end=attempt.CompletedAt.Value.AddSeconds(HarvestPreservationTreatmentValidation.ProtectionSeconds);
            if(s.SchemaVersion!=Snapshot.HarvestPreservationExposureSchema)return end;
            foreach(var opening in s.HarvestPreservationEvidence.Where(x=>x.Kind==HarvestPreservationEvidenceKind.ControlledOpening
                &&x.AppliedRevision<=throughRevision&&x.TreatmentAttemptId==attempt.Id&&x.VesselId==attempt.ContainerId&&x.At<=at)) {
                RuleTime deadline=opening.At.AddSeconds(HarvestPreservationEvidenceValidation.OpeningLimitSeconds);
                var close=s.PortableHandling.Where(x=>x.ItemId==opening.VesselId&&x.Operation==PortableOperation.Close
                    &&x.Revision>opening.AppliedRevision&&x.Revision<=throughRevision).OrderBy(x=>x.Revision).FirstOrDefault();
                if(close==null||close.EndedAt>=deadline)end=Min(end,deadline);
            }
            foreach(var exposure in s.HarvestPreservationEvidence.Where(x=>x.Kind==HarvestPreservationEvidenceKind.Exposure
                &&x.AppliedRevision<=throughRevision&&x.TreatmentAttemptId==attempt.Id&&x.VesselId==attempt.ContainerId&&x.At<=at)) {
                bool affected=inventoryLotId==attempt.InventoryLotId;
                if(!affected) {
                    var portion=s.HarvestPreservationEvidence.SingleOrDefault(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion
                        &&x.AppliedRevision<=throughRevision&&x.TreatmentAttemptId==attempt.Id&&x.ChildLotId==inventoryLotId);
                    var removal=portion==null?null:s.PortableHandling.Where(x=>x.ItemId==inventoryLotId
                        &&x.Operation==PortableOperation.Retrieve&&x.FromParentId==attempt.ContainerId
                        &&x.Revision>portion.AppliedRevision&&x.Revision<=throughRevision).OrderBy(x=>x.Revision).FirstOrDefault();
                    affected=portion!=null&&(removal==null||exposure.At<=removal.EndedAt);
                }
                if(affected)end=Min(end,exposure.At);
            }
            if(inventoryLotId!=attempt.InventoryLotId) {
                var portion=s.HarvestPreservationEvidence.SingleOrDefault(x=>x.Kind==HarvestPreservationEvidenceKind.InVesselPortion
                    &&x.AppliedRevision<=throughRevision&&x.TreatmentAttemptId==attempt.Id&&x.ChildLotId==inventoryLotId);
                var removal=portion==null?null:s.PortableHandling.Where(x=>x.ItemId==inventoryLotId
                    &&x.Operation==PortableOperation.Retrieve&&x.FromParentId==attempt.ContainerId
                    &&x.Revision>portion.AppliedRevision&&x.Revision<=throughRevision).OrderBy(x=>x.Revision).FirstOrDefault();
                if(removal!=null)end=Min(end,removal.EndedAt);
            }
            return end;
        }
    }

    /// <summary>One immutable TEST_ONLY treatment history bound to its exact physical descendant.
    /// The current preservation state and protection deadline are always derived from this history.</summary>
    public sealed class HarvestPreservationTreatmentAttemptRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string SkillId { get; }
        public string InventoryLotId { get; }
        public RuleQuantity TreatedAmount { get; }
        public string ContainerId { get; }
        public string ToolId { get; }
        public string SupplyLotId { get; }
        public string TargetReservationId { get; }
        public string SupplyReservationId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public HarvestPreservationTreatmentStatus Status { get; }
        public RuleTime? CompletedAt { get; }
        public RuleTime? SealedAt { get; }
        public int AbilityModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int Natural { get; }
        public HarvestPreservationTreatmentDegree Degree { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long RandomWordsConsumed { get; }

        public HarvestPreservationTreatmentAttemptRecord(string id,string workerId,string skillId,string inventoryLotId,
            RuleQuantity treatedAmount,string containerId,string toolId,string supplyLotId,string targetReservationId,
            string supplyReservationId,RuleTime startedAt,RuleTime updatedAt,ActiveWorkProgress work,
            HarvestPreservationTreatmentStatus status,RuleTime? completedAt=null,RuleTime? sealedAt=null,
            int abilityModifier=0,int proficiencyRank=0,int proficiencyBonus=0,int natural=0,
            HarvestPreservationTreatmentDegree degree=HarvestPreservationTreatmentDegree.None,
            uint randomBefore=0,uint randomAfter=0,long randomWordsConsumed=0)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(workerId)||!Validation.ValidId(skillId)
                ||!Validation.ValidId(inventoryLotId)||treatedAmount<=default(RuleQuantity)
                ||!Validation.ValidId(containerId)||!Validation.ValidId(toolId)||!Validation.ValidId(supplyLotId)
                ||!Validation.ValidId(targetReservationId)||!Validation.ValidId(supplyReservationId)
                ||startedAt>updatedAt||work==null||!Enum.IsDefined(typeof(HarvestPreservationTreatmentStatus),status)
                ||completedAt.HasValue&&completedAt.Value<startedAt||sealedAt.HasValue&&(!completedAt.HasValue||sealedAt.Value!=completedAt.Value)
                ||proficiencyRank<0||proficiencyRank>2||proficiencyBonus<0
                ||!Enum.IsDefined(typeof(HarvestPreservationTreatmentDegree),degree)||natural<0||natural>20
                ||randomWordsConsumed<0)
                throw new ArgumentException("Invalid harvest preservation treatment attempt.");
            Id=id;WorkerId=workerId;SkillId=skillId;InventoryLotId=inventoryLotId;TreatedAmount=treatedAmount;
            ContainerId=containerId;ToolId=toolId;SupplyLotId=supplyLotId;TargetReservationId=targetReservationId;
            SupplyReservationId=supplyReservationId;StartedAt=startedAt;UpdatedAt=updatedAt;Work=work;Status=status;
            CompletedAt=completedAt;SealedAt=sealedAt;AbilityModifier=abilityModifier;ProficiencyRank=proficiencyRank;
            ProficiencyBonus=proficiencyBonus;Natural=natural;Degree=degree;RandomBefore=randomBefore;
            RandomAfter=randomAfter;RandomWordsConsumed=randomWordsConsumed;
        }

        public HarvestPreservationTreatmentAttemptRecord WithProgress(RuleTime at,ActiveWorkProgress work)
            =>new HarvestPreservationTreatmentAttemptRecord(Id,WorkerId,SkillId,InventoryLotId,TreatedAmount,ContainerId,
                ToolId,SupplyLotId,TargetReservationId,SupplyReservationId,StartedAt,at,work,Status,CompletedAt,SealedAt,
                AbilityModifier,ProficiencyRank,ProficiencyBonus,Natural,Degree,RandomBefore,RandomAfter,RandomWordsConsumed);

        public HarvestPreservationTreatmentAttemptRecord Complete(RuleTime at,ActiveWorkProgress work,
            HarvestPreservationTreatmentStatus status,int abilityModifier,int proficiencyRank,int proficiencyBonus,
            int natural,HarvestPreservationTreatmentDegree degree,uint randomBefore,uint randomAfter,long wordsConsumed)
            =>new HarvestPreservationTreatmentAttemptRecord(Id,WorkerId,SkillId,InventoryLotId,TreatedAmount,ContainerId,
                ToolId,SupplyLotId,TargetReservationId,SupplyReservationId,StartedAt,at,work,status,at,
                status==HarvestPreservationTreatmentStatus.Success?at:(RuleTime?)null,abilityModifier,proficiencyRank,
                proficiencyBonus,natural,degree,randomBefore,randomAfter,wordsConsumed);
    }

    /// <summary>Persisted TEST_ONLY ingredient/work binding. Work progress is the existing exact
    /// ActiveWorkProgress record; current preservation remains a derived query.</summary>
    public sealed class HarvestRequirementWorkRecord
    {
        public string Id { get; }
        public string WorkerId { get; }
        public string InventoryLotId { get; }
        public string ReservationId { get; }
        public RuleQuantity RequiredAmount { get; }
        public HarvestIngredientRequirement Requirement { get; }
        public HarvestRequirementWorkStatus Status { get; }
        public HarvestRequirementPauseReason PauseReason { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }

        public HarvestRequirementWorkRecord(string id,string workerId,string inventoryLotId,string reservationId,
            RuleQuantity requiredAmount,HarvestIngredientRequirement requirement,HarvestRequirementWorkStatus status,
            HarvestRequirementPauseReason pauseReason,RuleTime startedAt,RuleTime updatedAt,ActiveWorkProgress work)
        {
            if(!Validation.ValidId(id)||!Validation.ValidId(workerId)||!Validation.ValidId(inventoryLotId)
                ||!Validation.ValidId(reservationId)||requiredAmount==default
                ||!Enum.IsDefined(typeof(HarvestIngredientRequirement),requirement)
                ||!Enum.IsDefined(typeof(HarvestRequirementWorkStatus),status)
                ||!Enum.IsDefined(typeof(HarvestRequirementPauseReason),pauseReason)||updatedAt<startedAt||work==null)
                throw new ArgumentException("Invalid harvest requirement work binding.");
            Id=id;WorkerId=workerId;InventoryLotId=inventoryLotId;ReservationId=reservationId;
            RequiredAmount=requiredAmount;Requirement=requirement;Status=status;PauseReason=pauseReason;
            StartedAt=startedAt;UpdatedAt=updatedAt;Work=work;
        }

        public HarvestRequirementWorkRecord With(RuleTime at,ActiveWorkProgress work,
            HarvestRequirementWorkStatus status,HarvestRequirementPauseReason pauseReason)
            =>new HarvestRequirementWorkRecord(Id,WorkerId,InventoryLotId,ReservationId,RequiredAmount,
                Requirement,status,pauseReason,StartedAt,at,work);
    }

    public static class HarvestRequirementWorkValidation
    {
        public const int MaxRecords=16;

        private static RuleTime Add(RuleTime first,RuleTime second)
        {
            var sum=new RuleQuantity(first.Numerator,first.Denominator)+new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(sum.Numerator,sum.Denominator);
        }

        private static RuleTime Subtract(RuleTime first,RuleTime second)
        {
            if(second>first)throw new ArgumentException("Negative work interval.");
            var difference=new RuleQuantity(first.Numerator,first.Denominator)-new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(difference.Numerator,difference.Denominator);
        }

        public static void Validate(Snapshot s)
        {
            if(s.HarvestRequirementWorks==null||s.HarvestRequirementWorks.Length>MaxRecords
                ||s.HarvestRequirementWorks.Any(x=>x==null)
                ||s.HarvestRequirementWorks.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.HarvestRequirementWorks.Length)
                throw new ArgumentException("Invalid harvest requirement work collection.");
            if(s.SchemaVersion<Snapshot.HarvestPreservationSchema) {
                if(s.HarvestRequirementWorks.Length!=0)throw new ArgumentException("Harvest requirement work requires schema 74.");
                return;
            }
            if(s.SchemaVersion==Snapshot.HarvestPreservationTreatmentSchema
                ||s.SchemaVersion==Snapshot.HarvestPreservationExposureSchema||s.SchemaVersion==Snapshot.MiningAssistantSchema) {
                if(s.HarvestRequirementWorks.Length!=0)
                    throw new ArgumentException("The selected schema does not contain the schema74 Fresh-work adapter.");
                return;
            }
            if(s.SchemaVersion!=Snapshot.HarvestPreservationSchema||!s.TestOnly)
                throw new ArgumentException("Harvest preservation schema 74 is TEST_ONLY.");

            foreach(var job in s.HarvestRequirementWorks) {
                if(!s.Actors.Any(x=>x.Id==job.WorkerId)||job.StartedAt>s.RuleClock||job.UpdatedAt>s.RuleClock
                    ||job.Requirement!=HarvestIngredientRequirement.Fresh||job.Work.Phases.Count!=1
                    ||job.Work.Complete||job.Work.Retained!=job.Work.Labor)
                    throw new ArgumentException("Invalid harvest requirement work progress.");
                if(!HarvestPreservationRules.TryProject(s,job.InventoryLotId,out var view))
                    throw new ArgumentException("Harvest requirement work has no resolved physical harvest root.");
                if(job.Work.Required!=new RuleTime(checked(s.HarvestUnits.Single(x=>x.Id==view.HarvestUnitId).PreservationIntervalSeconds*2L)))
                    throw new ArgumentException("Invalid TEST_ONLY harvest requirement work duration.");
                var reservation=s.Work.Reservations.SingleOrDefault(x=>x.Id==job.ReservationId);
                if(reservation==null||reservation.JobId!=job.Id||reservation.LotId!=job.InventoryLotId
                    ||reservation.Amount!=job.RequiredAmount||reservation.ConsumedAmount!=default
                    ||reservation.ReleasedAmount!=default||reservation.RemainingAmount!=job.RequiredAmount)
                    throw new ArgumentException("Harvest requirement reservation changed unexpectedly.");
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==job.Id).ToArray();
                if(intervals.Any(x=>x.WorkerId!=job.WorkerId||x.Start<job.StartedAt||x.Start>s.RuleClock))
                    throw new ArgumentException("Invalid harvest requirement work interval.");
                RuleTime booked=default;
                foreach(var interval in intervals)booked=Add(booked,Subtract(interval.End,interval.Start));
                RuleTime expectedBooked=job.Status==HarvestRequirementWorkStatus.Working?job.Work.Required:job.Work.Labor;
                if(booked!=expectedBooked)throw new ArgumentException("Harvest requirement work booking does not match active or retained work.");
                RuleTime credited=default;
                foreach(var interval in intervals) {
                    if(interval.Start>=s.RuleClock)continue;
                    RuleTime end=interval.End<s.RuleClock?interval.End:s.RuleClock;
                    if(end>interval.Start)credited=Add(credited,Subtract(end,interval.Start));
                }
                if(credited!=job.Work.Labor)throw new ArgumentException("Harvest requirement work does not match credited labor.");
                bool active=intervals.Any(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock);
                if(job.Status==HarvestRequirementWorkStatus.Working) {
                    if(job.UpdatedAt!=s.RuleClock||job.PauseReason!=HarvestRequirementPauseReason.None
                        ||view.State!=HarvestPreservationState.Fresh||!active
                        ||intervals.Count(x=>x.Start<=s.RuleClock&&x.End>s.RuleClock)!=1)
                        throw new ArgumentException("Invalid active Fresh-required work.");
                } else if(job.Status==HarvestRequirementWorkStatus.Paused) {
                    if(active||job.PauseReason==HarvestRequirementPauseReason.None
                        ||job.PauseReason==HarvestRequirementPauseReason.IngredientNotFresh&&view.State==HarvestPreservationState.Fresh)
                        throw new ArgumentException("Invalid paused Fresh-required work.");
                } else throw new ArgumentException("Unknown harvest requirement work status.");
            }
        }
    }

    public static class HarvestPreservationTreatmentValidation
    {
        public const int WorkSeconds=1800;
        public const int ProtectionSeconds=86400;
        public const int DifficultyClass=10;
        public static readonly RuleQuantity SupplyAmount=RuleQuantity.FromFraction(1,2);
        public const int MaxRecords=1;

        private static RuleTime Add(RuleTime first,RuleTime second)
        {
            var sum=new RuleQuantity(first.Numerator,first.Denominator)+new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(sum.Numerator,sum.Denominator);
        }
        private static RuleTime Subtract(RuleTime first,RuleTime second)
        {
            var value=new RuleQuantity(first.Numerator,first.Denominator)-new RuleQuantity(second.Numerator,second.Denominator);
            return new RuleTime(value.Numerator,value.Denominator);
        }
        private static RuleTime Duration(RuleTime value)=>new RuleTime(value.Numerator,value.Denominator);
        private static bool Successful(HarvestPreservationTreatmentDegree degree)
            =>degree==HarvestPreservationTreatmentDegree.Success||degree==HarvestPreservationTreatmentDegree.CriticalSuccess;
        private static HarvestPreservationTreatmentDegree Grade(int natural,int modifier)
        {
            long total=(long)natural+modifier;
            var grade=total>=DifficultyClass+10?HarvestPreservationTreatmentDegree.CriticalSuccess
                :total>=DifficultyClass?HarvestPreservationTreatmentDegree.Success
                :total<=DifficultyClass-10?HarvestPreservationTreatmentDegree.CriticalFailure
                :HarvestPreservationTreatmentDegree.Failure;
            if(natural==20&&grade<HarvestPreservationTreatmentDegree.CriticalSuccess)
                grade=(HarvestPreservationTreatmentDegree)((int)grade+1);
            else if(natural==1&&grade>HarvestPreservationTreatmentDegree.CriticalFailure)
                grade=(HarvestPreservationTreatmentDegree)((int)grade-1);
            return grade;
        }

        public static void Validate(Snapshot s)
        {
            if(s.HarvestPreservationTreatmentAttempts==null
                ||s.HarvestPreservationTreatmentAttempts.Length>MaxRecords
                ||s.HarvestPreservationTreatmentAttempts.Any(x=>x==null)
                ||s.HarvestPreservationTreatmentAttempts.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()
                    !=s.HarvestPreservationTreatmentAttempts.Length)
                throw new ArgumentException("Invalid harvest preservation treatment collection.");
            if(s.SchemaVersion<Snapshot.HarvestPreservationTreatmentSchema||s.SchemaVersion==Snapshot.MiningAssistantSchema) {
                if(s.HarvestPreservationTreatmentAttempts.Length!=0)
                    throw new ArgumentException("Harvest treatment history requires schema75.");
                return;
            }
            if((s.SchemaVersion!=Snapshot.HarvestPreservationTreatmentSchema
                    &&s.SchemaVersion!=Snapshot.HarvestPreservationExposureSchema)||!s.TestOnly
                ||s.HarvestRequirementWorks.Length!=0)
                throw new ArgumentException("Schemas75 and76 are TEST_ONLY treatment profiles.");

            foreach(var attempt in s.HarvestPreservationTreatmentAttempts) {
                if(!s.Actors.Any(x=>x.Id==attempt.WorkerId)||s.WorldSchedule==null
                    ||!s.WorldSchedule.Order.Contains(attempt.WorkerId)||attempt.SkillId!="cooking"
                    ||attempt.StartedAt>s.RuleClock||attempt.UpdatedAt>s.RuleClock
                    ||attempt.Work.Required!=new RuleTime(WorkSeconds)||attempt.Work.Phases.Count!=1
                    ||attempt.Work.Complete!=(attempt.Status!=HarvestPreservationTreatmentStatus.Working)
                    ||attempt.Work.Retained!=attempt.Work.Labor
                    ||attempt.Work.Labor>attempt.Work.Required)
                    throw new ArgumentException("Invalid harvest treatment work progress or worker binding.");
                if(!HarvestPreservationRules.TryProject(s,attempt.InventoryLotId,out _))
                    throw new ArgumentException("Harvest treatment is not bound to physical harvested material.");
                if(!s.PortableEquipment.Any(x=>x.Id==attempt.InventoryLotId
                        &&x.LinkKind==PortableLinkKind.InventoryLot&&x.LinkedId==attempt.InventoryLotId
                        &&x.MassBasis==PortableMassBasis.GenericPounds)
                    ||!s.PortableEquipment.Any(x=>x.Id==attempt.ContainerId&&x.CapacityPounds.HasValue&&x.CapacityCubicFeet.HasValue)
                    ||!s.PortableEquipment.Any(x=>x.Id==attempt.ToolId)
                    ||!s.PortableEquipment.Any(x=>x.Id==attempt.SupplyLotId&&x.LinkKind==PortableLinkKind.InventoryLot
                        &&x.LinkedId==attempt.SupplyLotId&&x.MassBasis==PortableMassBasis.GenericPounds))
                    throw new ArgumentException("Harvest treatment lacks its bound physical equipment or stock.");
                if(!HarvestPreservationRules.TryProjectAt(s,attempt.InventoryLotId,attempt.StartedAt,out var atStart)
                    ||atStart.State==HarvestPreservationState.Spoiled)
                    throw new ArgumentException("Harvest treatment began after the material Spoiled.");

                RuleTime finish=Add(attempt.StartedAt,new RuleTime(WorkSeconds));
                var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==attempt.Id).ToArray();
                if(intervals.Length!=1||intervals[0].WorkerId!=attempt.WorkerId||intervals[0].Start!=attempt.StartedAt
                    ||intervals[0].End!=finish)
                    throw new ArgumentException("Harvest treatment worker booking does not match its fixed active work.");
                RuleTime elapsed=s.RuleClock<finish?Subtract(s.RuleClock,attempt.StartedAt):new RuleTime(WorkSeconds);
                if(attempt.Work.Labor!=elapsed)
                    throw new ArgumentException("Harvest treatment active progress does not match its worker interval.");

                var target=s.Work.Reservations.SingleOrDefault(x=>x.Id==attempt.TargetReservationId);
                var supply=s.Work.Reservations.SingleOrDefault(x=>x.Id==attempt.SupplyReservationId);
                if(target==null||supply==null||target.JobId!=attempt.Id||supply.JobId!=attempt.Id
                    ||target.LotId!=attempt.InventoryLotId||target.Amount!=attempt.TreatedAmount
                    ||target.ConsumedAmount!=default(RuleQuantity)||supply.LotId!=attempt.SupplyLotId
                    ||supply.Amount!=SupplyAmount)
                    throw new ArgumentException("Harvest treatment reservations do not match the selected materials.");
                bool working=attempt.Status==HarvestPreservationTreatmentStatus.Working;
                if(working) {
                    if(attempt.UpdatedAt!=s.RuleClock||attempt.CompletedAt.HasValue||attempt.SealedAt.HasValue
                        ||attempt.Work.Complete||target.RemainingAmount!=target.Amount||target.ReleasedAmount!=default(RuleQuantity)
                        ||supply.RemainingAmount!=supply.Amount||supply.ConsumedAmount!=default(RuleQuantity)
                        ||s.RuleClock>=finish||attempt.Degree!=HarvestPreservationTreatmentDegree.None||attempt.Natural!=0
                        ||attempt.RandomBefore!=0||attempt.RandomAfter!=0||attempt.RandomWordsConsumed!=0)
                        throw new ArgumentException("Invalid active harvest treatment attempt.");
                    var container=s.PortableEquipment.Single(x=>x.Id==attempt.ContainerId);
                    var targetItem=s.PortableEquipment.Single(x=>x.Id==attempt.InventoryLotId);
                    if(!container.Open||targetItem.ParentId!=container.Id)
                        throw new ArgumentException("Active treatment requires its target inside the open bound container.");
                } else {
                    var training=s.SkillTraining.SingleOrDefault(x=>x.ActorId==attempt.WorkerId&&x.SkillId==attempt.SkillId);
                    if(!attempt.CompletedAt.HasValue||attempt.CompletedAt.Value!=finish||attempt.UpdatedAt!=finish
                        ||attempt.Work.Labor!=attempt.Work.Required||attempt.Natural<1||attempt.Natural>20
                        ||attempt.RandomBefore==0||attempt.RandomAfter==0||attempt.RandomWordsConsumed<1
                        ||!Enum.IsDefined(typeof(HarvestPreservationTreatmentDegree),attempt.Degree)
                        ||attempt.Degree==HarvestPreservationTreatmentDegree.None
                        ||training==null||training.ProficiencyRank!=attempt.ProficiencyRank
                        ||target.RemainingAmount!=default(RuleQuantity)||target.ReleasedAmount!=target.Amount
                        ||supply.RemainingAmount!=default(RuleQuantity)||supply.ConsumedAmount!=supply.Amount
                        ||supply.ReleasedAmount!=default(RuleQuantity))
                        throw new ArgumentException("Invalid settled harvest treatment attempt.");
                    var draw=DiceStream.Draw(attempt.RandomBefore,20);
                    if(draw.Value+1!=attempt.Natural||draw.NextState!=attempt.RandomAfter
                        ||draw.WordsConsumed!=attempt.RandomWordsConsumed
                        ||Grade(attempt.Natural,checked(attempt.AbilityModifier+attempt.ProficiencyBonus))!=attempt.Degree)
                        throw new ArgumentException("Harvest treatment check or random trace does not resolve from its recorded evidence.");
                    if((attempt.Status==HarvestPreservationTreatmentStatus.Success)!=Successful(attempt.Degree))
                        throw new ArgumentException("Treatment outcome disagrees with its task check.");
                    if((attempt.Status==HarvestPreservationTreatmentStatus.Success)!=(attempt.SealedAt==attempt.CompletedAt))
                        throw new ArgumentException("Successful treatment must seal at its completion instant.");
                    if(!HarvestPreservationRules.TryProjectAt(s,attempt.InventoryLotId,finish,out var atFinish)
                        ||atFinish.State==HarvestPreservationState.Spoiled)
                        throw new ArgumentException("A treatment cannot complete after the material Spoiled.");
                    if(s.SchemaVersion==Snapshot.HarvestPreservationTreatmentSchema
                        &&attempt.Status==HarvestPreservationTreatmentStatus.Success
                        &&s.RuleClock<attempt.CompletedAt.Value.AddSeconds(ProtectionSeconds)) {
                        var container=s.PortableEquipment.Single(x=>x.Id==attempt.ContainerId);
                        var targetItem=s.PortableEquipment.Single(x=>x.Id==attempt.InventoryLotId);
                        if(container.Open||targetItem.ParentId!=container.Id)
                            throw new ArgumentException("Protected material must remain inside its closed treatment container.");
                        if(s.InventoryLots.Any(x=>x.ParentId==attempt.InventoryLotId
                            &&x.CreatedAt>=attempt.CompletedAt.Value
                            &&x.CreatedAt<attempt.CompletedAt.Value.AddSeconds(ProtectionSeconds)))
                            throw new ArgumentException("Protected contents cannot be separated before protection expires.");
                    }
                }
            }
        }
    }
}
