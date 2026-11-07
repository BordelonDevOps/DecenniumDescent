#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One explicitly placed ordinary locked chest and its finite one-day ration lot.</summary>
    public sealed class OrdinaryReceptacleDefinition
    {
        public string LockId { get; }
        public string ContainerId { get; }
        public string KeyItemId { get; }
        public string RationLotId { get; }
        public int X { get; }
        public int Y { get; }
        public OrdinaryReceptacleDefinition(string lockId,string containerId,string keyItemId,string rationLotId,int x,int y)
        {
            if(!Validation.ValidId(lockId)||!Validation.ValidId(containerId)||!Validation.ValidId(keyItemId)
                ||!Validation.ValidId(rationLotId)||x<0||y<0)throw new ArgumentException("Invalid authored receptacle definition.");
            LockId=lockId;ContainerId=containerId;KeyItemId=keyItemId;RationLotId=rationLotId;X=x;Y=y;
        }
        internal string Fingerprint=>LockId+"|"+ContainerId+"|"+KeyItemId+"|"+RationLotId+"|"+X.ToString(CultureInfo.InvariantCulture)+"|"+Y.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Bounded test content for ordinary stationary receptacles; this does not author arbitrary world objects.</summary>
    public sealed class OrdinaryReceptacleFixture
    {
        public const string ToolsId="TEST_ONLY.ordinary-thieves-tools";
        public System.Collections.ObjectModel.ReadOnlyCollection<OrdinaryReceptacleDefinition> Receptacles { get; }
        public System.Collections.ObjectModel.ReadOnlyCollection<string> AvailableKeyIds { get; }
        public bool HasTools { get; }
        public bool ToolsProficient { get; }
        public bool PickRequiresSight { get; }
        public uint Seed { get; }
        internal string Key { get; }
        public OrdinaryReceptacleFixture(OrdinaryReceptacleDefinition[] receptacles,string[] availableKeyIds=null,
            bool hasTools=true,bool toolsProficient=false,bool pickRequiresSight=true,uint seed=1)
        {
            if(seed==0||receptacles==null||receptacles.Length<1||receptacles.Length>OrdinaryReceptacleValidation.MaxLocks||receptacles.Any(x=>x==null))
                throw new ArgumentException("Ordinary receptacle fixture requires authored lock records.",nameof(receptacles));
            var rows=receptacles.OrderBy(x=>x.LockId,StringComparer.Ordinal).ToArray();
            if(rows.Select(x=>x.LockId).Distinct(StringComparer.Ordinal).Count()!=rows.Length
                ||rows.Select(x=>x.ContainerId).Distinct(StringComparer.Ordinal).Count()!=rows.Length
                ||rows.Select(x=>x.KeyItemId).Distinct(StringComparer.Ordinal).Count()!=rows.Length
                ||rows.Select(x=>x.RationLotId).Distinct(StringComparer.Ordinal).Count()!=rows.Length)
                throw new ArgumentException("Ordinary receptacle fixture identities must be unique.",nameof(receptacles));
            var available=(availableKeyIds??Array.Empty<string>()).ToArray();
            if(available.Any(x=>!Validation.ValidId(x)||!rows.Any(r=>r.KeyItemId==x))
                ||available.Distinct(StringComparer.Ordinal).Count()!=available.Length)
                throw new ArgumentException("Available keys must be distinct authored physical keys.",nameof(availableKeyIds));
            Receptacles=Array.AsReadOnly(rows);AvailableKeyIds=Array.AsReadOnly(available.OrderBy(x=>x,StringComparer.Ordinal).ToArray());
            HasTools=hasTools;ToolsProficient=toolsProficient;PickRequiresSight=pickRequiresSight;Seed=seed;
            Key="ordinary-receptacles-v1|chest=25lb,300lb,12cuft|ration=2lb|key-mass=unmodeled|pick=DEX-DC15-6-active-seconds|open=portable-one-second|"
                +HasTools+"|"+ToolsProficient+"|"+PickRequiresSight+"|seed="+Seed.ToString(CultureInfo.InvariantCulture)+"|"+string.Join(";",rows.Select(x=>x.Fingerprint))
                +"|keys="+string.Join(",",AvailableKeyIds);
        }
    }

    public enum OrdinaryReceptacleInteraction { UnlockWithKey=10,PickWithTools=11,Interrupt=12 }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private OrdinaryReceptacleFixture ordinaryReceptacles;

        public TestOnlySharedWorldPolicy(OrdinaryReceptacleFixture receptacles,int walkingSpeed=30,ConditionCombatFixture conditions=null,
            params TacticalTerrainCell[] terrain):this(receptacles,new SharedCombatFixture(seed:receptacles==null?1:receptacles.Seed),walkingSpeed,conditions,terrain) { }

        public TestOnlySharedWorldPolicy(OrdinaryReceptacleFixture receptacles,SharedCombatFixture combat,int walkingSpeed=30,
            ConditionCombatFixture conditions=null,params TacticalTerrainCell[] terrain):this(combat,walkingSpeed,conditions,terrain)
        {
            ordinaryReceptacles=receptacles??throw new ArgumentNullException(nameof(receptacles));
            ContentFingerprint=OrdinaryReceptacleFingerprint(ContentFingerprint,receptacles);
        }

        private static string OrdinaryReceptacleFingerprint(string prior,OrdinaryReceptacleFixture fixture)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.receptacle-v1-"+
                string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+fixture.Key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }

        private void InitializeOrdinaryReceptacles(Snapshot s)
        {
            if(ordinaryReceptacles==null)return;
            string owner=TestOnlyPolicy.ActorId;RuleQuantity Q(long value)=>new RuleQuantity(value);
            var definitions=ordinaryReceptacles.Receptacles;
            var stock=definitions.Select(x=>new ResourceLot(x.RationLotId,TestOnlyInventoryPolicy.FoodUnit,new RuleQuantity(2),x.ContainerId,owner)).ToArray();
            s.Work=new WorkLedger(s.Work.Lots.Concat(stock),s.Work.WorkerIntervals,s.Work.Reservations);
            s.InventoryLots=s.InventoryLots.Concat(definitions.Select(x=>new InventoryLotRecord(x.RationLotId,"",owner,Q(2),s.RuleClock,
                NutritionKind.FoodPounds,new RuleTime(2592000),InventoryAccess.Stowed))).ToArray();
            string toolsId=ordinaryReceptacles.HasTools?OrdinaryReceptacleFixture.ToolsId:"";
            var receptacleItems=definitions.SelectMany(x=>new PortableEquipmentRecord[]{
                new PortableEquipmentRecord(x.ContainerId,"adventuring-gear.chest",owner,owner,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Fixed,Q(25),Q(25),capacityPounds:Q(300),capacityCubicFeet:Q(12),
                    fitRuleId:"TEST_ONLY.ordinary-receptacle-fit",fitMemberIds:new[]{x.RationLotId},groundX:x.X,groundY:x.Y),
                new PortableEquipmentRecord(x.RationLotId,"adventuring-gear.rations-1-day",owner,owner,x.ContainerId,PortablePlacement.Contained,
                    PortableLinkKind.InventoryLot,x.RationLotId,PortableMassBasis.FoodPounds,Q(2),null)
            }).ToList();
            if(ordinaryReceptacles.HasTools)receptacleItems.Add(new PortableEquipmentRecord(OrdinaryReceptacleFixture.ToolsId,
                "tools.thieves-tools",owner,owner,"",PortablePlacement.Carried,PortableLinkKind.None,"",PortableMassBasis.Fixed,Q(1),Q(1)));
            foreach(string keyId in ordinaryReceptacles.AvailableKeyIds)
                receptacleItems.Add(new PortableEquipmentRecord(keyId,"adventuring-gear.key",owner,owner,"",PortablePlacement.Ground,
                    PortableLinkKind.None,"",PortableMassBasis.Unmodeled,null,null,groundX:0,groundY:0));
            s.PortableEquipment=s.PortableEquipment.Concat(receptacleItems).ToArray();
            s.OrdinaryReceptacleLocks=definitions.Select(x=>new OrdinaryReceptacleLockRecord(x.LockId,x.ContainerId,owner,x.KeyItemId,toolsId,locked:true)).ToArray();
            PortableEquipmentRules.SynchronizeLinks(s);
        }

        private bool IsOrdinaryReceptacleCommand(Snapshot s,Command c)
            =>ordinaryReceptacles!=null&&c.Kind==CommandKind.Interact&&s.OrdinaryReceptacleLocks.Any(x=>x.Id==c.Target);

        private static OrdinaryReceptacleLockRecord OrdinaryLock(Snapshot s,string id)
            =>s.OrdinaryReceptacleLocks.SingleOrDefault(x=>x.Id==id);
        private static void SetOrdinaryLock(Snapshot s,OrdinaryReceptacleLockRecord value)
            =>s.OrdinaryReceptacleLocks=s.OrdinaryReceptacleLocks.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void SetOrdinaryAttempt(Snapshot s,OrdinaryReceptacleAttemptRecord value)
            =>s.OrdinaryReceptacleAttempts=s.OrdinaryReceptacleAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();

        private bool OrdinaryCredentialAvailable(Snapshot s,OrdinaryReceptacleLockRecord lockState,OrdinaryReceptacleMethod method,
            string actor,out PortableEquipmentRecord item)
        {
            string id=method==OrdinaryReceptacleMethod.Key?lockState.KeyItemId:lockState.ToolsItemId;
            item=s.PortableEquipment.SingleOrDefault(x=>x.Id==id);
            return id!=""&&item!=null&&item.OwnerId==lockState.OwnerId&&item.CustodianId==actor
                &&(method==OrdinaryReceptacleMethod.Key||item.Placement!=PortablePlacement.Ground)
                &&PortableEquipmentRules.Accessible(s,actor,item);
        }

        private bool CanContinueOrdinaryAttempt(Snapshot s,OrdinaryReceptacleAttemptRecord attempt)
        {
            var lockState=OrdinaryLock(s,attempt.LockId);
            if(lockState==null||!lockState.Locked||attempt.ActorId!=lockState.OwnerId||!CapableWorker(s,attempt.ActorId)
                ||AvailableHands(s,attempt.ActorId)<1||s.WorldTraversals.Any(x=>x.ActorId==attempt.ActorId))return false;
            var container=s.PortableEquipment.SingleOrDefault(x=>x.Id==lockState.ContainerId);
            var credential=s.PortableEquipment.SingleOrDefault(x=>x.Id==attempt.CredentialItemId);
            return container!=null&&!container.Open&&PortableEquipmentRules.Accessible(s,attempt.ActorId,container)
                &&credential!=null&&credential.OwnerId==attempt.ActorId&&credential.CustodianId==attempt.ActorId
                &&(attempt.Method==OrdinaryReceptacleMethod.Key||credential.Placement!=PortablePlacement.Ground)
                &&PortableEquipmentRules.Accessible(s,attempt.ActorId,credential);
        }

        private void RecordOrdinaryAttempt(Snapshot s,OrdinaryReceptacleAttemptRecord prior,OrdinaryReceptacleAttemptStatus status,
            int natural,int modifier,bool automaticFailure=false)
        {
            var ended=new OrdinaryReceptacleAttemptRecord(prior.Id,prior.LockId,prior.ActorId,prior.CredentialItemId,prior.Method,
                prior.StartedAt,s.RuleClock,status,natural,modifier,prior.Tactical,automaticFailure);
            if(prior.Status==OrdinaryReceptacleAttemptStatus.Working)SetOrdinaryAttempt(s,ended);
            else s.OrdinaryReceptacleAttempts=s.OrdinaryReceptacleAttempts.Concat(new[]{ended}).ToArray();
        }

        private void ResolveOrdinaryAttempt(Snapshot s,OrdinaryReceptacleAttemptRecord attempt)
        {
            if(!CanContinueOrdinaryAttempt(s,attempt)) {
                RecordOrdinaryAttempt(s,attempt,OrdinaryReceptacleAttemptStatus.Interrupted,0,0);return;
            }
            if(attempt.Method==OrdinaryReceptacleMethod.Key) {
                RecordOrdinaryAttempt(s,attempt,OrdinaryReceptacleAttemptStatus.Succeeded,0,0);
                SetOrdinaryLock(s,OrdinaryLock(s,attempt.LockId).With(locked:false));return;
            }
            if(ordinaryReceptacles.PickRequiresSight&&View(s,attempt.ActorId).BlocksSight) {
                RecordOrdinaryAttempt(s,attempt,OrdinaryReceptacleAttemptStatus.Failed,0,0,automaticFailure:true);return;
            }
            var character=CharacterStateFacts.ForActor(s,attempt.ActorId);
            int modifier=SupplyCacheRules.PickCheckModifier(character,ordinaryReceptacles.ToolsProficient);
            var conditions=View(s,attempt.ActorId);
            var roll=PlaytestDice.RollD20(s.RandomState,disadvantageSources:conditions.Has(ConditionKind.Poisoned)?1:0);
            s.RandomState=roll.NextRandomState;
            bool success=PlaytestRolls.TaskCheck(roll.Natural,modifier,15).Success;
            RecordOrdinaryAttempt(s,attempt,success?OrdinaryReceptacleAttemptStatus.Succeeded:OrdinaryReceptacleAttemptStatus.Failed,
                roll.Natural,modifier);
            if(success)SetOrdinaryLock(s,OrdinaryLock(s,attempt.LockId).With(locked:false));
        }

        private string AssessOrdinaryReceptacleCommand(Snapshot s,Command c,out OrdinaryReceptacleLockRecord lockState,
            out OrdinaryReceptacleMethod method,out PortableEquipmentRecord credential)
        {
            lockState=null;method=default(OrdinaryReceptacleMethod);credential=null;
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.OverwatchRider!=OverwatchRider.None
                ||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.HarvestSelection!=null||c.MiningSelection!=null
                ||c.ProspectingExposure!=null||c.Target==""||c.Y!=0)return "InvalidOrdinaryReceptacleInteraction";
            lockState=OrdinaryLock(s,c.Target);if(lockState==null)return "UnknownOrdinaryReceptacleLock";
            string lockId=lockState.Id,containerId=lockState.ContainerId;
            if(c.Actor!=lockState.OwnerId)return "NoOrdinaryReceptaclePermission";
            var container=s.PortableEquipment.Single(x=>x.Id==containerId);
            if(!PortableEquipmentRules.Accessible(s,c.Actor,container))return "OrdinaryReceptacleOutOfReach";
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "TraversalRequiresStationaryInteraction";
            var operation=(OrdinaryReceptacleInteraction)c.X;
            if(!Enum.IsDefined(typeof(OrdinaryReceptacleInteraction),operation))return "InvalidOrdinaryReceptacleInteraction";
            if(operation==OrdinaryReceptacleInteraction.Interrupt) {
                var pending=s.OrdinaryReceptacleAttempts.SingleOrDefault(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working
                    &&x.LockId==lockId&&x.ActorId==c.Actor);
                if(pending==null)return "NoActiveOrdinaryReceptacleAttempt";
                return null;
            }
            if(s.OrdinaryReceptacleAttempts.Any(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working&&x.LockId==lockId))
                return "OrdinaryReceptacleBusy";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
            if(AvailableHands(s,c.Actor)<1)return "HandlingHandRequired";
            if(!lockState.Locked)return "OrdinaryReceptacleAlreadyUnlocked";
            method=operation==OrdinaryReceptacleInteraction.UnlockWithKey?OrdinaryReceptacleMethod.Key
                :operation==OrdinaryReceptacleInteraction.PickWithTools?OrdinaryReceptacleMethod.ThievesTools:(OrdinaryReceptacleMethod)(-1);
            if(!Enum.IsDefined(typeof(OrdinaryReceptacleMethod),method))return "InvalidOrdinaryReceptacleInteraction";
            if(!OrdinaryCredentialAvailable(s,lockState,method,c.Actor,out credential))
                return method==OrdinaryReceptacleMethod.Key?"PhysicalKeyUnavailable":"ActualThievesToolsRequired";
            var interval=Interval(s,c.Actor);
            if(interval.ActionSpent)return "ActionAlreadySpent";
            if(!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.InventoryCombat&&(s.Encounter==null||s.Encounter.CurrentActor!=c.Actor||PendingCalendarChoice(s)))return "TacticalChoicePending";
            return null;
        }

        private CommandQueryResult QueryOrdinaryReceptacleCommand(Snapshot s,Command c)
        {
            string failure=AssessOrdinaryReceptacleCommand(s,c,out _,out _,out _);
            var costs=new System.Collections.Generic.List<CommandCost>();
            if(failure==null&&(OrdinaryReceptacleInteraction)c.X!=OrdinaryReceptacleInteraction.Interrupt) {
                costs.Add(new CommandCost("action","",1));
                if(!s.InventoryCombat)costs.Add(new CommandCost("work-seconds","",6));
            }
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverOrdinaryReceptacleCommands(Snapshot s,string actor)
        {
            int index=0;
            if(ordinaryReceptacles==null)yield break;
            foreach(var lockState in s.OrdinaryReceptacleLocks.OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                if(lockState.OwnerId!=actor)continue;
                var container=s.PortableEquipment.SingleOrDefault(x=>x.Id==lockState.ContainerId);
                if(container==null||!PortableEquipmentRules.Accessible(s,actor,container))continue;
                var working=s.OrdinaryReceptacleAttempts.SingleOrDefault(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working
                    &&x.LockId==lockState.Id&&x.ActorId==actor);
                if(working!=null) {
                    yield return OrdinaryReceptacleOption(s,actor,lockState.Id,OrdinaryReceptacleInteraction.Interrupt,index++);
                    continue;
                }
                if(!lockState.Locked)continue;
                if(OrdinaryCredentialAvailable(s,lockState,OrdinaryReceptacleMethod.Key,actor,out _))
                    yield return OrdinaryReceptacleOption(s,actor,lockState.Id,OrdinaryReceptacleInteraction.UnlockWithKey,index++);
                if(OrdinaryCredentialAvailable(s,lockState,OrdinaryReceptacleMethod.ThievesTools,actor,out _))
                    yield return OrdinaryReceptacleOption(s,actor,lockState.Id,OrdinaryReceptacleInteraction.PickWithTools,index++);
            }
        }

        private static Command OrdinaryReceptacleOption(Snapshot s,string actor,string lockId,OrdinaryReceptacleInteraction operation,int index)
            =>new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".ordinary-receptacle."+index.ToString(CultureInfo.InvariantCulture),
                actor,s.Revision,CommandKind.Interact,lockId,(int)operation);

        private string ResolveOrdinaryReceptacle(Snapshot s,Command c)
        {
            string failure=AssessOrdinaryReceptacleCommand(s,c,out var lockState,out var method,out var credential);
            if(failure!=null)return failure;
            if((OrdinaryReceptacleInteraction)c.X==OrdinaryReceptacleInteraction.Interrupt) {
                var active=s.OrdinaryReceptacleAttempts.Single(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working
                    &&x.LockId==lockState.Id&&x.ActorId==c.Actor);
                InterruptOrdinaryAttempt(s,active);return null;
            }
            bool tactical=s.InventoryCombat;var actionInterval=Interval(s,c.Actor);
            if(tactical) {
                SetInterval(s,actionInterval.PayAction());
                var immediate=new OrdinaryReceptacleAttemptRecord(OrdinaryInventory.Identity(s,"ordinary-lock-attempt"),lockState.Id,c.Actor,
                    credential.Id,method,s.RuleClock,s.RuleClock,OrdinaryReceptacleAttemptStatus.Interrupted,tactical:true);
                ResolveOrdinaryAttempt(s,immediate);return null;
            }
            string id=OrdinaryInventory.Identity(s,"ordinary-lock-attempt");RuleTime start=s.RuleClock,end=start.AddSeconds(6);
            SetInterval(s,actionInterval.PayAction());
            s.Work=s.Work.Reserve(id,new[]{new WorkerInterval(id+".labor",id,c.Actor,start,end)},Array.Empty<ResourceReservation>());
            s.OrdinaryReceptacleAttempts=s.OrdinaryReceptacleAttempts.Concat(new[]{new OrdinaryReceptacleAttemptRecord(id,lockState.Id,
                c.Actor,credential.Id,method,start,null,OrdinaryReceptacleAttemptStatus.Working)}).ToArray();
            return null;
        }

        private static RuleTime? NextOrdinaryReceptacleBoundary(Snapshot s)
        {
            var due=s.OrdinaryReceptacleAttempts.Where(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working)
                .Select(x=>x.StartedAt.AddSeconds(6)).ToArray();
            return due.Length==0?(RuleTime?)null:due.Min();
        }
        private void CompleteOrdinaryReceptacleAttempts(Snapshot s)
        {
            foreach(var attempt in s.OrdinaryReceptacleAttempts.Where(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working
                &&x.StartedAt.AddSeconds(6)==s.RuleClock).ToArray())ResolveOrdinaryAttempt(s,attempt);
        }
        private void InterruptIncompatibleOrdinaryAttempts(Snapshot s)
        {
            foreach(var attempt in s.OrdinaryReceptacleAttempts.Where(x=>x.Status==OrdinaryReceptacleAttemptStatus.Working
                &&!CanContinueOrdinaryAttempt(s,x)).ToArray())InterruptOrdinaryAttempt(s,attempt);
        }
        private static void InterruptOrdinaryAttempt(Snapshot s,OrdinaryReceptacleAttemptRecord attempt)
        {
            if(attempt.Status!=OrdinaryReceptacleAttemptStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
            var ended=new OrdinaryReceptacleAttemptRecord(attempt.Id,attempt.LockId,attempt.ActorId,attempt.CredentialItemId,attempt.Method,
                attempt.StartedAt,s.RuleClock,OrdinaryReceptacleAttemptStatus.Interrupted);
            SetOrdinaryAttempt(s,ended);
        }
    }
}
#endif
