using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum MaterialProvenance { Undocumented=1, Disputed, Documented, GateSealed }
    public enum MaterialDemand { Glut=1, Normal, Sought, Strategic }
    public enum MaterialCondition { Damaged=1, Worn, Sound, Exceptional }
    public enum MaterialUrgency { Forced=1, Normal, PatientAuction }
    public enum HavenAppraisalStatus { Working=1, Paused, PendingCompletion, Completed, Cancelled, Invalidated }

    /// <summary>FL-20 ordinary material arithmetic. A trusted caller establishes the facts and domain.</summary>
    public static class OrdinaryMaterialValuation
    {
        public static RuleQuantity ExactCopper(long? baseCopper,MaterialProvenance provenance,MaterialDemand demand,
            MaterialCondition condition,MaterialUrgency urgency)
        {
            if(!baseCopper.HasValue||baseCopper.Value<0)throw new ArgumentException("An actual whole-lot base reference is required.",nameof(baseCopper));
            var p=provenance switch {
                MaterialProvenance.Undocumented=>new RuleQuantity(1,2),MaterialProvenance.Disputed=>new RuleQuantity(3,4),
                MaterialProvenance.Documented=>new RuleQuantity(1),MaterialProvenance.GateSealed=>new RuleQuantity(5,4),
                _=>throw new ArgumentException("Unresolved provenance.",nameof(provenance))};
            var d=demand switch {
                MaterialDemand.Glut=>new RuleQuantity(3,4),MaterialDemand.Normal=>new RuleQuantity(1),
                MaterialDemand.Sought=>new RuleQuantity(5,4),MaterialDemand.Strategic=>new RuleQuantity(3,2),
                _=>throw new ArgumentException("Unresolved demand.",nameof(demand))};
            var c=condition switch {
                MaterialCondition.Damaged=>new RuleQuantity(1,2),MaterialCondition.Worn=>new RuleQuantity(3,4),
                MaterialCondition.Sound=>new RuleQuantity(1),MaterialCondition.Exceptional=>new RuleQuantity(5,4),
                _=>throw new ArgumentException("Unresolved condition.",nameof(condition))};
            var u=urgency switch {
                MaterialUrgency.Forced=>new RuleQuantity(3,4),MaterialUrgency.Normal=>new RuleQuantity(1),
                MaterialUrgency.PatientAuction=>new RuleQuantity(11,10),_=>throw new ArgumentException("Unresolved urgency.",nameof(urgency))};
            return RuleQuantity.FromFraction((BigInteger)baseCopper.Value*p.Numerator*d.Numerator*c.Numerator*u.Numerator,
                (BigInteger)p.Denominator*d.Denominator*c.Denominator*u.Denominator);
        }
    }

    public sealed class HavenAppraisalBasis
    {
        public string DeskId { get; }
        public string ProviderId { get; }
        public string UnitId { get; }
        public string DepositVersionId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public string EvidenceId { get; }
        public string ClearanceId { get; }
        public string ServiceTermsId { get; }
        public string AssessmentContextId { get; }
        public RuleQuantity Quantity { get; }
        public long BaseCopper { get; }
        public MaterialProvenance Provenance { get; }
        public MaterialDemand Demand { get; }
        public MaterialCondition Condition { get; }
        public MaterialUrgency Urgency { get; }

        public HavenAppraisalBasis(string deskId,string providerId,string unitId,string depositVersionId,string ownerId,string custodianId,
            string evidenceId,string clearanceId,string serviceTermsId,string assessmentContextId,RuleQuantity quantity,long baseCopper,MaterialProvenance provenance,
            MaterialDemand demand,MaterialCondition condition,MaterialUrgency urgency)
        {
            if(new[]{deskId,providerId,unitId,depositVersionId,ownerId,custodianId,evidenceId,clearanceId,serviceTermsId,assessmentContextId}.Any(x=>!Validation.ValidId(x))
                ||quantity==default)throw new ArgumentException("Invalid whole-unit appraisal basis.");
            DeskId=deskId;ProviderId=providerId;UnitId=unitId;DepositVersionId=depositVersionId;OwnerId=ownerId;
            CustodianId=custodianId;EvidenceId=evidenceId;AssessmentContextId=assessmentContextId;Quantity=quantity;BaseCopper=baseCopper;
            ClearanceId=clearanceId;ServiceTermsId=serviceTermsId;
            Provenance=provenance;Demand=demand;Condition=condition;Urgency=urgency;
            ExactCopper();
        }

        public RuleQuantity ExactCopper()=>OrdinaryMaterialValuation.ExactCopper(BaseCopper,Provenance,Demand,Condition,Urgency);
    }

    public sealed class HavenAppraisalRecord
    {
        public const int RequiredSeconds=1800;
        public string Id { get; }
        public string WorkerId { get; }
        public HavenAppraisalBasis Basis { get; }
        public long StartRevision { get; }
        public long UpdatedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public ActiveWorkProgress Work { get; }
        public HavenAppraisalStatus Status { get; }
        public string Reason { get; }
        public RuleQuantity? ResultCopper { get; }
        public string ReservationId=>Id+".subject";
        public bool Open=>Status==HavenAppraisalStatus.Working||Status==HavenAppraisalStatus.Paused||Status==HavenAppraisalStatus.PendingCompletion;

        public HavenAppraisalRecord(string id,string worker,HavenAppraisalBasis basis,long startRevision,long updatedRevision,
            RuleTime startedAt,RuleTime updatedAt,RuleTime labor,HavenAppraisalStatus status,string reason,RuleQuantity? resultCopper)
        {
            var required=new RuleTime(RequiredSeconds);
            if(!Validation.ValidId(id)||!Validation.ValidId(worker)||basis==null||startRevision<1||updatedRevision<startRevision
                ||updatedAt<startedAt||labor<default(RuleTime)||labor>required||!Enum.IsDefined(typeof(HavenAppraisalStatus),status)
                ||!Validation.ValidId(reason)||((status==HavenAppraisalStatus.Completed)!=resultCopper.HasValue)
                ||(status==HavenAppraisalStatus.Completed||status==HavenAppraisalStatus.PendingCompletion)&&labor!=required
                ||(status==HavenAppraisalStatus.Working||status==HavenAppraisalStatus.Paused)&&labor==required
                ||resultCopper.HasValue&&resultCopper.Value!=basis.ExactCopper())throw new ArgumentException("Invalid Haven appraisal record.");
            Id=id;WorkerId=worker;Basis=basis;StartRevision=startRevision;UpdatedRevision=updatedRevision;
            StartedAt=startedAt;UpdatedAt=updatedAt;Status=status;Reason=reason;ResultCopper=resultCopper;
            Work=new ActiveWorkProgress(new[]{required});
            if(labor>default(RuleTime))Work=Work.Credit(labor);
        }

        public HavenAppraisalRecord With(Snapshot s,RuleTime labor,HavenAppraisalStatus status,string reason)
            =>new HavenAppraisalRecord(Id,WorkerId,Basis,StartRevision,s.Revision+1,StartedAt,s.RuleClock,labor,status,reason,
                status==HavenAppraisalStatus.Completed?Basis.ExactCopper():(RuleQuantity?)null);
    }

    public static class HavenAppraisalValidation
    {
        public const int MaxRecords=8;

        public static void Validate(Snapshot s)
        {
            var jobs=s.HavenAppraisals;
            if(jobs==null||jobs.Length>MaxRecords||jobs.Any(x=>x==null)||jobs.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=jobs.Length
                ||s.SchemaVersion<Snapshot.HavenAppraisalSchema&&jobs.Length!=0||jobs.Count(x=>x.Open)>1
                ||jobs.Count(x=>x.Status==HavenAppraisalStatus.Completed)>1)
                throw new ArgumentException("Invalid Haven appraisal history.");
            foreach(var job in jobs)ValidateJob(s,job);
        }

        private static void ValidateJob(Snapshot s,HavenAppraisalRecord job)
        {
            var start=s.Receipts.SingleOrDefault(x=>x.Revision==job.StartRevision);
            if(start==null||!s.Receipts.Any(x=>x.Revision==job.UpdatedRevision)||job.UpdatedAt>s.RuleClock
                ||!s.Actors.Any(x=>x.Id==job.WorkerId))throw new ArgumentException("Haven appraisal lacks its command history.");
            var command=CommandHistory.Read(start);
            if(command.Kind!=CommandKind.StartHavenAppraisal||command.Actor!=job.WorkerId||command.Target!=job.Basis.DeskId)
                throw new ArgumentException("Haven appraisal start receipt mismatch.");
            var claim=s.Work.Reservations.SingleOrDefault(x=>x.Id==job.ReservationId);
            if(claim==null||claim.JobId!=job.Id||claim.LotId!=job.Basis.UnitId||claim.Amount!=job.Basis.Quantity
                ||claim.ConsumedAmount!=default||claim.ReleasedAmount!=(job.Open?default:claim.Amount)
                ||s.Work.Reservations.Count(x=>x.JobId==job.Id)!=1)
                throw new ArgumentException("Haven appraisal nonconsuming claim mismatch.");
            var intervals=s.Work.WorkerIntervals.Where(x=>x.JobId==job.Id).ToArray();
            if(intervals.Any(x=>x.WorkerId!=job.WorkerId||x.Start<job.StartedAt||x.Start>s.RuleClock
                ||!job.Open&&x.End>job.UpdatedAt))throw new ArgumentException("Invalid Haven appraisal labor provenance.");
            var elapsed=RuleQuantity.Sum(intervals.Select(x=>Duration(x.Start,x.End<s.RuleClock?x.End:s.RuleClock)));
            if(elapsed!=new RuleQuantity(job.Work.Labor.Numerator,job.Work.Labor.Denominator)
                ||intervals.Count(x=>x.End>s.RuleClock)!=(job.Status==HavenAppraisalStatus.Working?1:0))
                throw new ArgumentException("Haven appraisal labor differs from its ledger intervals.");
        }

        private static RuleQuantity Duration(RuleTime start,RuleTime end)
            =>new RuleQuantity(end.Numerator,end.Denominator)-new RuleQuantity(start.Numerator,start.Denominator);
    }
}
