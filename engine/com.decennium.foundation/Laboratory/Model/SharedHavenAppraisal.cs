#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One supplied no-charge institutional appointment with explicit upstream inspection,
    /// provenance, known evidence and a named glut-demand assessment context for the whole iron unit.</summary>
    public sealed class TestOnlyHavenAppraisalProfile
    {
        public const string DeskId="TEST_ONLY.haven-appraisal-desk",ProviderId="TEST_ONLY.haven-appraisal-office";
        public const string EvidenceId="TEST_ONLY.iron-inspection-provenance-dossier",ContextId="TEST_ONLY.haven-iron-glut-assessment";
        public const string ClearanceId="TEST_ONLY.iron-inspected-quarantine-cleared-authorized";
        public const string ServiceTermsId="TEST_ONLY.haven-institutional-self-appraisal-no-charge";
        public const string WorkerId=TestOnlyPolicy.CompanionId;
        internal const string SubjectMaterialId="TEST_ONLY.mineral.iron-ore";
        internal const int WholeUnitBaseCopper=10;
        internal static RuleQuantity WholeUnitMass=>new RuleQuantity(1);
        public const int SiteX=2,SiteY=3;
        public bool Cleared { get; }
        public bool EvidenceAccessible { get; }
        public bool TermsAuthorized { get; }
        public bool InstrumentsAvailable { get; }
        public bool DeskIntact { get; }
        public RuleTime AvailableFrom { get; }
        public RuleTime AvailableUntil { get; }

        public TestOnlyHavenAppraisalProfile(bool cleared=true,bool evidenceAccessible=true,bool termsAuthorized=true,
            bool instrumentsAvailable=true,bool deskIntact=true,int availableFrom=0,int availableUntil=7200)
        {
            if(availableFrom<0||availableUntil<=availableFrom)throw new ArgumentException("Invalid appraisal appointment interval.");
            Cleared=cleared;EvidenceAccessible=evidenceAccessible;TermsAuthorized=termsAuthorized;
            InstrumentsAvailable=instrumentsAvailable;DeskIntact=deskIntact;
            AvailableFrom=new RuleTime(availableFrom);AvailableUntil=new RuleTime(availableUntil);
        }

        internal string Key=>"FL19-FL20-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|whole-iron|documented-glut-sound-normal|"
            +DeskId+"|"+ProviderId+"|"+EvidenceId+"|"+ClearanceId+"|"+ServiceTermsId+"|"+ContextId+"|"+WorkerId+"|2,3|single-slot|"
            +SharedMiningFixture.UnitA+"|"+SharedMiningFixture.DepositVersionId+"|"+SharedMiningFixture.CategoryA+"|"
            +SubjectMaterialId+"|1 pound|10 copper unadjusted whole-unit base|"
            +AvailableFrom+"|"+AvailableUntil+"|"+Cleared+"|"+EvidenceAccessible+"|"+TermsAuthorized+"|"+InstrumentsAvailable+"|"+DeskIntact;
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyHavenAppraisalProfile havenAppraisalProfile;
        private const string AppraisalDeskStructure="TEST_ONLY.haven-appraisal-workbench";
        private static string AppraisalGround=>"ground.2.3";

        public TestOnlySharedWorldPolicy EnableHavenAppraisal(TestOnlyHavenAppraisalProfile profile)
        {
            if(profile==null)throw new ArgumentNullException(nameof(profile));
            if(initializationStarted||havenAppraisalProfile!=null||portableKit==null||connectedCombat==null||miningFixture==null
                ||SelectedSchema!=Snapshot.MiningSchema)
                throw new InvalidOperationException("Select one appraisal profile on the portable-capable direct mining host before initialization.");
            havenAppraisalProfile=profile;
            using(var sha=SHA256.Create())ContentFingerprint="TEST_ONLY.haven-appraisal-v1-"+string.Concat(sha.ComputeHash(
                Encoding.UTF8.GetBytes(ContentFingerprint+"|"+profile.Key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
            return this;
        }

        private void InitializeHavenAppraisal(Snapshot s)
        {
            if(havenAppraisalProfile==null)return;
            s.Structures=s.Structures.Concat(new[]{new ObjectStructureRecord(TestOnlyHavenAppraisalProfile.DeskId,AppraisalDeskStructure,
                TestOnlyPolicy.ActorId,TestOnlyPolicy.ActorId,AppraisalGround,ObjectMaterial.WoodLeather,5,
                havenAppraisalProfile.DeskIntact?5:0,0,new RuleQuantity(20))}).ToArray();
        }

        private static bool IsHavenAppraisalCommand(CommandKind kind)=>kind==CommandKind.StartHavenAppraisal
            ||kind==CommandKind.PauseHavenAppraisal||kind==CommandKind.ResumeHavenAppraisal||kind==CommandKind.CancelHavenAppraisal;

        private string AppraisalTermsFailure()
        {
            if(!havenAppraisalProfile.Cleared)return "AppraisalClearanceMissing";
            if(!havenAppraisalProfile.EvidenceAccessible)return "AppraisalEvidenceUnavailable";
            if(!havenAppraisalProfile.TermsAuthorized)return "AppraisalTermsUnauthorized";
            return null;
        }

        private string AppraisalSubject(Snapshot s,out HavenAppraisalBasis basis)
        {
            basis=null;
            var unit=s.MiningUnits.SingleOrDefault(x=>x.Id==SharedMiningFixture.UnitA);
            if(unit==null||unit.Status!=MiningUnitStatus.Extracted||unit.Condition!=MiningUnitCondition.Intact
                ||unit.ReceivedLotId!=unit.Id||unit.CategoryId!=SharedMiningFixture.CategoryA
                ||unit.MassPounds!=TestOnlyHavenAppraisalProfile.WholeUnitMass
                ||unit.ValueCopper!=TestOnlyHavenAppraisalProfile.WholeUnitBaseCopper)return "AppraisalSubjectUnsupported";
            var deposit=s.MiningDeposits.Single(x=>x.Id==unit.DepositId);
            var category=s.MiningCategories.Single(x=>x.Id==unit.CategoryId);
            if(deposit.VersionId!=SharedMiningFixture.DepositVersionId||category.MaterialId!=TestOnlyHavenAppraisalProfile.SubjectMaterialId)
                return "AppraisalEvidenceSubjectMismatch";
            if(!s.MiningAttempts.Any(x=>x.DepositId==deposit.Id&&x.DepositVersionId==deposit.VersionId
                &&x.SelectedUnitIds.Contains(unit.Id,StringComparer.Ordinal)
                &&(x.Status==MiningAttemptStatus.Success||x.Status==MiningAttemptStatus.CriticalSuccess)))
                return "AppraisalExtractionHistoryMissing";
            var physical=s.PortableEquipment.SingleOrDefault(x=>x.Id==unit.Id);
            var lot=s.Work.Lots.SingleOrDefault(x=>x.Id==unit.Id);
            var inventory=s.InventoryLots.SingleOrDefault(x=>x.LotId==unit.Id);
            const string worker=TestOnlyHavenAppraisalProfile.WorkerId;
            if(physical==null||lot==null||inventory==null||inventory.ParentId!=""||physical.LinkedId!=unit.Id
                ||physical.LinkKind!=PortableLinkKind.InventoryLot||physical.OwnerId!=worker||inventory.OwnerId!=worker
                ||physical.CustodianId!=worker||lot.CustodianId!=worker||lot.UnitId!="mass-pound"
                ||lot.Amount!=unit.MassPounds||inventory.CreatedAmount!=unit.MassPounds
                ||inventory.Access!=InventoryAccess.Ground||physical.Placement!=PortablePlacement.Ground||physical.ParentId!=""
                ||physical.GroundX!=TestOnlyHavenAppraisalProfile.SiteX||physical.GroundY!=TestOnlyHavenAppraisalProfile.SiteY
                ||lot.LocationId!=AppraisalGround)return "AppraisalWholeSubjectNotAtDesk";
            basis=new HavenAppraisalBasis(TestOnlyHavenAppraisalProfile.DeskId,TestOnlyHavenAppraisalProfile.ProviderId,
                unit.Id,deposit.VersionId,inventory.OwnerId,physical.CustodianId,TestOnlyHavenAppraisalProfile.EvidenceId,
                TestOnlyHavenAppraisalProfile.ClearanceId,TestOnlyHavenAppraisalProfile.ServiceTermsId,
                TestOnlyHavenAppraisalProfile.ContextId,lot.Amount,unit.ValueCopper.Value,MaterialProvenance.Documented,
                MaterialDemand.Glut,MaterialCondition.Sound,MaterialUrgency.Normal);
            return null;
        }

        private string AppraisalWorkerFailure(Snapshot s,string worker,bool finishing)
        {
            var desk=s.Structures.SingleOrDefault(x=>x.Id==TestOnlyHavenAppraisalProfile.DeskId);
            if(desk==null||desk.ProfileId!=AppraisalDeskStructure||desk.LocationId!=AppraisalGround||desk.Broken
                ||!havenAppraisalProfile.InstrumentsAvailable)return "AppraisalDeskUnavailable";
            if(CraftingRestrictions.StationUseBlocked(s,desk.Id))return "AppraisalDeskUseBlocked";
            if(s.RuleClock<havenAppraisalProfile.AvailableFrom||s.RuleClock>havenAppraisalProfile.AvailableUntil
                ||!finishing&&s.RuleClock==havenAppraisalProfile.AvailableUntil)return "AppraisalAppointmentClosed";
            if(s.InventoryCombat||s.Encounter!=null&&!ResolvedConflict(s)||PendingCalendarChoice(s))return "AppraisalCombatUnavailable";
            if(!CapableWorker(s,worker)||View(s,worker).BlocksSight||AvailableHands(s,worker)<1)return "AppraisalWorkerIncapable";
            var position=WorldPositionResolver.Position(s,worker);
            if(position.X!=new RuleQuantity(TestOnlyHavenAppraisalProfile.SiteX)
                ||position.Y!=new RuleQuantity(TestOnlyHavenAppraisalProfile.SiteY)||s.WorldTraversals.Any(x=>x.ActorId==worker)
                ||s.RouteTravels.Any(x=>x.TravelerId==worker&&x.Status==ExpeditionRouteTravelStatus.Moving))
                return "AppraisalWorkerNotAtDesk";
            return null;
        }

        private static bool SameAppraisalBasis(HavenAppraisalBasis first,HavenAppraisalBasis second)
            =>first.DeskId==second.DeskId&&first.ProviderId==second.ProviderId&&first.UnitId==second.UnitId
                &&first.DepositVersionId==second.DepositVersionId&&first.OwnerId==second.OwnerId&&first.CustodianId==second.CustodianId
                &&first.EvidenceId==second.EvidenceId&&first.ClearanceId==second.ClearanceId&&first.ServiceTermsId==second.ServiceTermsId
                &&first.AssessmentContextId==second.AssessmentContextId
                &&first.Quantity==second.Quantity&&first.BaseCopper==second.BaseCopper&&first.Provenance==second.Provenance
                &&first.Demand==second.Demand&&first.Condition==second.Condition&&first.Urgency==second.Urgency;

        private string AppraisalBasisFailure(Snapshot s,HavenAppraisalRecord job)
        {
            string failure=AppraisalTermsFailure();if(failure!=null)return failure;
            failure=AppraisalSubject(s,out var basis);
            if(failure!=null)return failure;
            return SameAppraisalBasis(job.Basis,basis)?null:"AppraisalBasisChanged";
        }

        private string AssessHavenAppraisal(Snapshot s,Command c,out HavenAppraisalRecord current,out HavenAppraisalBasis basis)
        {
            current=null;basis=null;
            if(havenAppraisalProfile==null||s.SchemaVersion!=Snapshot.HavenAppraisalSchema)return "HavenAppraisalNotSelected";
            if(c.Actor!=TestOnlyHavenAppraisalProfile.WorkerId)return "AppraisalWorkerUnauthorized";
            if(c.X!=0||c.Y!=0||c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null
                ||c.HarvestSelection!=null||c.MiningSelection!=null||c.ProspectingExposure!=null||c.RouteMappingWork!=null)
                return "InvalidAppraisalPayload";
            bool start=c.Kind==CommandKind.StartHavenAppraisal;
            if(start) {
                if(c.Target!=TestOnlyHavenAppraisalProfile.DeskId)return "AppraisalDeskNotRegistered";
                if(s.HavenAppraisals.Any(x=>x.Open))return "AppraisalServiceSlotOccupied";
                if(s.HavenAppraisals.Any(x=>x.Status==HavenAppraisalStatus.Completed))return "AppraisalBasisAlreadyReported";
                if(s.HavenAppraisals.Length>=HavenAppraisalValidation.MaxRecords)return "AppraisalHistoryCapacityReached";
                string terms=AppraisalTermsFailure();if(terms!=null)return terms;
                string subject=AppraisalSubject(s,out basis);if(subject!=null)return subject;
                if(s.Work.AvailableAmount(basis.UnitId)!=basis.Quantity)return "AppraisalSubjectReserved";
            } else {
                current=s.HavenAppraisals.SingleOrDefault(x=>x.Id==c.Target&&x.Open&&x.WorkerId==c.Actor);
                if(current==null)return "AppraisalWorkNotOpen";
                if(c.Kind==CommandKind.CancelHavenAppraisal)return null;
                if(c.Kind==CommandKind.PauseHavenAppraisal)
                    return current.Status==HavenAppraisalStatus.Working?null:"AppraisalWorkNotRunning";
                if(current.Status==HavenAppraisalStatus.Working)return "AppraisalWorkAlreadyRunning";
                string invalid=AppraisalBasisFailure(s,current);if(invalid!=null)return invalid;
            }
            bool finishing=current?.Work.Complete==true;
            string eligibility=AppraisalWorkerFailure(s,c.Actor,finishing);if(eligibility!=null)return eligibility;
            if(!finishing&&IsOffCalendarActivity(s,c.Actor)) {
                var activity=ActivityInterval(s,c.Actor);
                if(activity.Action==WorldActionCommitment.Dash
                    ||activity.Action==WorldActionCommitment.ActiveLabor&&!CanContinueActivityLabor(s,c.Actor))
                    return "OffCalendarActionAlreadySpent";
            }
            RuleTime remaining=current?.Work.Remaining??new RuleTime(HavenAppraisalRecord.RequiredSeconds);
            RuleTime end=AppraisalBookingEnd(s,remaining);
            if(s.ExpeditionAssignments.Any(x=>x.WorkerId==c.Actor&&x.Open)||OrdinaryInventory.Busy(s,c.Actor)
                ||end>s.RuleClock&&WorldActivityValidation.HasActiveLabor(s,c.Actor,s.RuleClock,end))return "AppraisalWorkerBusy";
            return null;
        }

        private RuleTime AppraisalBookingEnd(Snapshot s,RuleTime remaining)
        {
            var full=CampGreens.Add(s.RuleClock,remaining);
            return full<havenAppraisalProfile.AvailableUntil?full:havenAppraisalProfile.AvailableUntil;
        }

        private void BookAppraisal(Snapshot s,HavenAppraisalRecord job,bool reserveSubject)
        {
            string laborId=job.Id+".labor."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            var interval=new WorkerInterval(laborId,job.Id,job.WorkerId,s.RuleClock,AppraisalBookingEnd(s,job.Work.Remaining));
            var claims=reserveSubject?new[]{new ResourceReservation(job.ReservationId,job.Id,job.Basis.UnitId,job.Basis.Quantity)}
                :Array.Empty<ResourceReservation>();
            s.Work=s.Work.Reserve(job.Id,new[]{interval},claims);
        }

        private static void PutAppraisal(Snapshot s,HavenAppraisalRecord job)
            =>s.HavenAppraisals=s.HavenAppraisals.Select(x=>x.Id==job.Id?job:x).ToArray();

        private static void EndAppraisal(Snapshot s,HavenAppraisalRecord job,HavenAppraisalStatus status,string reason)
        {
            s.Work=s.Work.CancelFutureWork(job.Id,s.RuleClock).Release(job.Id,job.ReservationId);
            PutAppraisal(s,job.With(s,job.Work.Labor,status,reason));
        }

        private static void PauseAppraisal(Snapshot s,HavenAppraisalRecord job,string reason)
        {
            s.Work=s.Work.CancelFutureWork(job.Id,s.RuleClock);
            PutAppraisal(s,job.With(s,job.Work.Labor,HavenAppraisalStatus.Paused,reason));
        }

        private string ResolveHavenAppraisal(Snapshot s,Command c)
        {
            string failure=AssessHavenAppraisal(s,c,out var current,out var basis);if(failure!=null)return failure;
            if(c.Kind==CommandKind.StartHavenAppraisal) {
                long revision=s.Revision+1;
                var job=new HavenAppraisalRecord("haven.appraisal."+revision.ToString(CultureInfo.InvariantCulture),c.Actor,basis,
                    revision,revision,s.RuleClock,s.RuleClock,default,HavenAppraisalStatus.Working,"AppraisalAdmitted",null);
                BookAppraisal(s,job,true);s.HavenAppraisals=s.HavenAppraisals.Concat(new[]{job}).ToArray();
                CommitActivityLabor(s,c.Actor,job.Id);
            } else if(c.Kind==CommandKind.CancelHavenAppraisal)EndAppraisal(s,current,HavenAppraisalStatus.Cancelled,"AppraisalCancelled");
            else if(c.Kind==CommandKind.PauseHavenAppraisal)PauseAppraisal(s,current,"AppraisalPausedByWorker");
            else if(current.Work.Complete)EndAppraisal(s,current,HavenAppraisalStatus.Completed,"AppraisalFinalized");
            else {
                BookAppraisal(s,current,false);
                PutAppraisal(s,current.With(s,current.Work.Labor,HavenAppraisalStatus.Working,"AppraisalResumed"));
                CommitActivityLabor(s,c.Actor,current.Id);
            }
            return null;
        }

        private static RuleTime? NextAppraisalBoundary(Snapshot s)
        {
            var job=s.HavenAppraisals.SingleOrDefault(x=>x.Status==HavenAppraisalStatus.Working);
            return job==null?(RuleTime?)null:s.Work.WorkerIntervals.Single(x=>x.JobId==job.Id&&x.End>s.RuleClock).End;
        }

        private static void CreditHavenAppraisal(Snapshot s,RuleTime elapsed)
        {
            var job=s.HavenAppraisals.SingleOrDefault(x=>x.Status==HavenAppraisalStatus.Working);
            if(job==null)return;
            var progress=job.Work.Credit(elapsed);
            if(progress.Complete)PutAppraisal(s,job.With(s,progress.Labor,HavenAppraisalStatus.PendingCompletion,"AppraisalCompletionDue"));
            else if(!s.Work.WorkerIntervals.Any(x=>x.JobId==job.Id&&x.End>s.RuleClock))
                PutAppraisal(s,job.With(s,progress.Labor,HavenAppraisalStatus.Paused,"AppraisalAppointmentClosed"));
            else PutAppraisal(s,job.With(s,progress.Labor,HavenAppraisalStatus.Working,"AppraisalLaborCredited"));
        }

        private void ReconcileHavenAppraisal(Snapshot s)
        {
            if(havenAppraisalProfile==null)return;
            var job=s.HavenAppraisals.SingleOrDefault(x=>x.Open);
            if(job==null)return;
            string invalid=AppraisalBasisFailure(s,job);
            if(invalid!=null) {EndAppraisal(s,job,HavenAppraisalStatus.Invalidated,invalid);return;}
            if(job.Status!=HavenAppraisalStatus.Working)return;
            string ineligible=AppraisalWorkerFailure(s,job.WorkerId,false);
            if(ineligible!=null)PauseAppraisal(s,job,ineligible);
        }

        private void FinalizeDueAppraisal(Snapshot s)
        {
            var job=s.HavenAppraisals.SingleOrDefault(x=>x.Status==HavenAppraisalStatus.PendingCompletion&&x.Reason=="AppraisalCompletionDue");
            if(job==null)return;
            string invalid=AppraisalBasisFailure(s,job);
            if(invalid!=null) {EndAppraisal(s,job,HavenAppraisalStatus.Invalidated,invalid);return;}
            string temporary=AppraisalWorkerFailure(s,job.WorkerId,true);
            if(temporary==null)EndAppraisal(s,job,HavenAppraisalStatus.Completed,"AppraisalFinalized");
            else PutAppraisal(s,job.With(s,job.Work.Labor,HavenAppraisalStatus.PendingCompletion,temporary));
        }
    }
}
#endif
