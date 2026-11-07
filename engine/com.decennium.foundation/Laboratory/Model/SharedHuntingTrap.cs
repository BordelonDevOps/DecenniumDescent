#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public sealed class HuntingTrapDefinition
    {
        private readonly string[] compatibleActorIds;
        public string ItemId { get; }
        public string OwnerId { get; }
        public int AnchorX { get; }
        public int AnchorY { get; }
        public string[] CompatibleActorIds => (string[])compatibleActorIds.Clone();
        internal string Key => ItemId+"|"+OwnerId+"|"+AnchorX.ToString(CultureInfo.InvariantCulture)+"|"
            +AnchorY.ToString(CultureInfo.InvariantCulture)+"|"+string.Join(",",compatibleActorIds);
        public HuntingTrapDefinition(string itemId,string ownerId,int anchorX,int anchorY,string[] compatibleActorIds)
        {
            if(!Validation.ValidId(itemId)||!Validation.ValidId(ownerId)||anchorX<0||anchorY<0||compatibleActorIds==null
                ||compatibleActorIds.Length<1||compatibleActorIds.Length>8||compatibleActorIds.Any(x=>!Validation.ValidId(x))
                ||compatibleActorIds.Distinct(StringComparer.Ordinal).Count()!=compatibleActorIds.Length)
                throw new ArgumentException("Invalid authored hunting-trap fixture facts.");
            ItemId=itemId;OwnerId=ownerId;AnchorX=anchorX;AnchorY=anchorY;
            this.compatibleActorIds=compatibleActorIds.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        }
        internal bool CanTrigger(string actor)=>compatibleActorIds.Contains(actor,StringComparer.Ordinal);
    }

    /// <summary>Explicit TEST_ONLY physical hunting-trap instances, anchors and compatibility facts.
    /// Those fixture facts stand in for authored content; they are not general anatomy or weight rules.</summary>
    public sealed class HuntingTrapFixture
    {
        private readonly HuntingTrapDefinition[] devices;
        public System.Collections.ObjectModel.ReadOnlyCollection<HuntingTrapDefinition> Devices { get; }
        internal string Key { get; }
        public HuntingTrapFixture(params HuntingTrapDefinition[] devices)
        {
            if(devices==null||devices.Length<1||devices.Length>8||devices.Any(x=>x==null))
                throw new ArgumentException("Hunting-trap fixture requires one to eight physical devices.",nameof(devices));
            var ordered=devices.OrderBy(x=>x.ItemId,StringComparer.Ordinal).ToArray();
            if(ordered.Select(x=>x.ItemId).Distinct(StringComparer.Ordinal).Count()!=ordered.Length
                ||ordered.Select(x=>x.AnchorX+","+x.AnchorY).Distinct(StringComparer.Ordinal).Count()!=ordered.Length)
                throw new ArgumentException("Hunting-trap item identities and grid anchors must be unique.",nameof(devices));
            this.devices=ordered;Devices=Array.AsReadOnly(ordered);
            Key="hunting-trap-prototype-v1|"+string.Join(";",ordered.Select(x=>x.Key));
        }
        internal HuntingTrapDefinition Find(string itemId)=>devices.SingleOrDefault(x=>x.ItemId==itemId);
    }

    /// <summary>Shared-clock ordinary hunting-trap execution (schema55 TEST_ONLY). Physical mass,
    /// Actions, life, deterministic rolls, traversal and tactical movement remain owned by their shared systems.</summary>
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private HuntingTrapFixture huntingTrapFixture;
        public static TestOnlySharedWorldPolicy WithHuntingTraps(HuntingTrapFixture fixture,uint seed=1,long enemyHp=26)
        {
            if(fixture==null)throw new ArgumentNullException(nameof(fixture));
            var policy=new TestOnlySharedWorldPolicy(new SharedCombatFixture(enemyHp,seed),walkingSpeed:30);
            return policy.EnableHuntingTraps(fixture);
        }
        public static TestOnlySharedWorldPolicy WithMiningAndHuntingTraps(SharedMiningFixture mining,HuntingTrapFixture traps,
            uint seed=1,long enemyHp=26)
        {
            if(mining==null)throw new ArgumentNullException(nameof(mining));
            var policy=WithMining(mining,seed,enemyHp);return policy.EnableHuntingTraps(traps);
        }
        public TestOnlySharedWorldPolicy EnableHuntingTraps(HuntingTrapFixture fixture)
        {AttachHuntingTraps(fixture);return this;}
        private void AttachHuntingTraps(HuntingTrapFixture fixture)
        {
            if(initializationStarted)throw new InvalidOperationException("Hunting traps must be configured before Initial().");
            if(fixture==null||huntingTrapFixture!=null)throw new ArgumentException("Select one hunting-trap profile before Initial().",nameof(fixture));
            huntingTrapFixture=fixture;
            ContentFingerprint=HuntingTrapFingerprint(ContentFingerprint,fixture);
        }
        private static string HuntingTrapFingerprint(string prior,HuntingTrapFixture fixture)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.hunting-traps-v1-"+
                string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+fixture.Key))
                    .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string HuntingTrapIdentity(string value)
        {
            using(var sha=SHA256.Create())return "htrap."+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value)).Take(20)
                .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string Number(long value)=>value.ToString(CultureInfo.InvariantCulture);
        private int HuntingTrapSelectionSchema(int prior)=>huntingTrapFixture==null?prior:Snapshot.HuntingTrapSchema;

        private void InitializeHuntingTrapDevices(Snapshot s)
        {
            if(huntingTrapFixture==null)return;
            if(s.SchemaVersion<Snapshot.HuntingTrapSchema)throw new ArgumentException("Hunting traps require schema55.");
            var initial=huntingTrapFixture.Devices.Select(x=>new PortableEquipmentRecord(x.ItemId,"adventuring-gear.hunting-trap",
                x.OwnerId,x.OwnerId,"",PortablePlacement.Carried,PortableLinkKind.None,"",PortableMassBasis.Fixed,
                new RuleQuantity(25),new RuleQuantity(25))).ToArray();
            if(initial.Any(x=>s.PortableEquipment.Any(y=>y.Id==x.Id)))throw new ArgumentException("Hunting-trap item identity already exists.");
            s.PortableEquipment=s.PortableEquipment.Concat(initial).ToArray();
        }

        private string ValidateHuntingTrapFixtureState(Snapshot s)
        {
            var registered=s.PortableEquipment.Where(x=>x.ProfileId=="adventuring-gear.hunting-trap").ToArray();
            if(huntingTrapFixture==null)
                return registered.Length==0&&s.HuntingTrapDeployments.Length==0&&s.HuntingTrapActions.Length==0
                    &&s.HuntingTrapTriggers.Length==0&&s.HuntingTrapTethers.Length==0?null:"HuntingTrapFixtureNotSelected";
            if((s.SchemaVersion!=Snapshot.HuntingTrapSchema&&!(dodgeActionEnabled&&s.SchemaVersion==Snapshot.DodgeSchema)
                &&!(readyActionEnabled&&s.SchemaVersion==Snapshot.ReadyActionSchema))
                ||registered.Length!=huntingTrapFixture.Devices.Count)
                return "InvalidHuntingTrapFixture";
            foreach(var definition in huntingTrapFixture.Devices) {
                if(!s.Actors.Any(x=>x.Id==definition.OwnerId)||definition.CompatibleActorIds.Any(actor=>!s.Actors.Any(x=>x.Id==actor))
                    ||!TestOnlyPolicy.Walkable(definition.AnchorX,definition.AnchorY))return "InvalidHuntingTrapFixture";
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==definition.ItemId);
                if(item==null||item.ProfileId!="adventuring-gear.hunting-trap"||item.OwnerId!=definition.OwnerId
                    ||item.MassBasis!=PortableMassBasis.Fixed||item.SourceWeightLb!=new RuleQuantity(25)
                    ||item.OperationalWeightLb!=new RuleQuantity(25))return "InvalidHuntingTrapFixture";
                if(s.HuntingTrapDeployments.Any(x=>x.TrapItemId==definition.ItemId
                    &&(x.SetterId!=definition.OwnerId||x.AnchorX!=definition.AnchorX||x.AnchorY!=definition.AnchorY)))
                    return "InvalidHuntingTrapFixture";
            }
            foreach(var trigger in s.HuntingTrapTriggers.Where(x=>x.EntryKind==HuntingTrapEntryKind.RouteTravelCheckpoint)) {
                var route=routeTravelFixture?.Find(trigger.RouteId);
                var binding=route?.Positions.SingleOrDefault(x=>x.Progress==trigger.RouteProgress);
                var deployment=s.HuntingTrapDeployments.SingleOrDefault(x=>x.Id==trigger.DeploymentId);
                if(binding==null||deployment==null||binding.X!=deployment.AnchorX||binding.Y!=deployment.AnchorY)
                    return "InvalidHuntingTrapRouteEntry";
            }
            return null;
        }

        private static HuntingTrapDeploymentRecord LatestHuntingTrapDeployment(Snapshot s,string itemId)
            =>s.HuntingTrapDeployments.Where(x=>x.TrapItemId==itemId).OrderByDescending(x=>x.ArmedRevision)
                .ThenByDescending(x=>x.Id,StringComparer.Ordinal).FirstOrDefault();
        private static HuntingTrapActionRecord WorkingHuntingTrapAction(Snapshot s,string actor,string itemOrActor)
            =>s.HuntingTrapActions.SingleOrDefault(x=>x.Status==HuntingTrapActionStatus.Working&&x.ActorId==actor
                &&(x.TrapItemId==itemOrActor||x.TargetActorId==itemOrActor));
        private static HuntingTrapTetherRecord ActiveHuntingTrapTether(Snapshot s,string actor)
            =>s.HuntingTrapTethers.SingleOrDefault(x=>x.ActorId==actor&&x.Status==HuntingTrapTetherStatus.Active);
        private static void SetHuntingTrapDeployment(Snapshot s,HuntingTrapDeploymentRecord value)
            =>s.HuntingTrapDeployments=s.HuntingTrapDeployments.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void SetHuntingTrapAction(Snapshot s,HuntingTrapActionRecord value)
            =>s.HuntingTrapActions=s.HuntingTrapActions.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void SetHuntingTrapTrigger(Snapshot s,HuntingTrapTriggerRecord value)
            =>s.HuntingTrapTriggers=s.HuntingTrapTriggers.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void SetHuntingTrapTether(Snapshot s,HuntingTrapTetherRecord value)
            =>s.HuntingTrapTethers=s.HuntingTrapTethers.Select(x=>x.Id==value.Id?value:x).ToArray();

        private bool IsHuntingTrapCommand(Snapshot s,Command c)
            =>huntingTrapFixture!=null&&c.Kind==CommandKind.Interact
                &&(huntingTrapFixture.Devices.Any(x=>x.ItemId==c.Target)||ActiveHuntingTrapTether(s,c.Target)!=null);
        private static bool WorldAdjacent(ActorState a,int x,int y)
            =>PlanarCombatGeometry.DistanceFeet(new CombatCell(a.X,a.Y),new CombatCell(x,y))<=5;

        private string AssessHuntingTrapCommand(Snapshot s,Command c,out HuntingTrapActionKind kind,out HuntingTrapActionRecord working,
            out HuntingTrapDefinition definition,out HuntingTrapDeploymentRecord deployment,out HuntingTrapTetherRecord tether)
        {
            kind=default(HuntingTrapActionKind);working=null;definition=null;deployment=null;tether=null;
            if(huntingTrapFixture==null||s.SchemaVersion<Snapshot.HuntingTrapSchema)return "HuntingTrapNotSelected";
            if(c.Kind!=CommandKind.Interact||c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.SuppressionFire!=null||c.DefensiveFormation!=null
                ||c.ExpeditionAssignment!=null||c.HarvestSelection!=null||c.MiningSelection!=null||c.ProspectingExposure!=null||c.Y!=0)
                return "InvalidHuntingTrapRequest";
            if(!s.Actors.Any(x=>x.Id==c.Actor))return "UnknownWorldActor";
            if(!s.WorldSchedule.Order.Contains(c.Actor))return "ActorOutsideActionSchedule";
            if(s.WorldTraversals.Any(x=>x.ActorId==c.Actor))return "TraversalRequiresStationaryInteraction";
            if(PendingCalendarChoice(s)||s.InventoryCombat&&s.HuntingTrapTriggers.Any(x=>x.Status==HuntingTrapTriggerStatus.Pending))
                return "TacticalChoicePending";
            if(c.X==(int)HuntingTrapInteraction.Interrupt) {
                working=WorkingHuntingTrapAction(s,c.Actor,c.Target);
                if(working==null)return "NoActiveHuntingTrapAction";
                kind=working.Kind;return null;
            }
            if(!Enum.IsDefined(typeof(HuntingTrapInteraction),c.X))return "InvalidHuntingTrapRequest";
            switch((HuntingTrapInteraction)c.X) {
                case HuntingTrapInteraction.Set:kind=HuntingTrapActionKind.Set;break;
                case HuntingTrapInteraction.Reset:kind=HuntingTrapActionKind.Reset;break;
                case HuntingTrapInteraction.Free:kind=HuntingTrapActionKind.Free;break;
                default:return "InvalidHuntingTrapRequest";
            }
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            if(!CapableWorker(s,c.Actor))return "WorkerCannotPerformTask";
            if(AvailableHands(s,c.Actor)<1)return "HandlingHandRequired";
            if(s.HuntingTrapActions.Length>=HuntingTrapValidation.MaxActions||s.Work.WorkerIntervals.Count>=Snapshot.MaxWorkRecords
                ||kind!=HuntingTrapActionKind.Free&&s.HuntingTrapDeployments.Length>=HuntingTrapValidation.MaxDeployments
                ||kind!=HuntingTrapActionKind.Free&&!HuntingTrapValidation.CanReserveEntries(s))
                return "HuntingTrapHistoryCapacityReached";
            var interval=Interval(s,c.Actor);
            if(interval.ActionSpent)return "ActionAlreadySpent";
            if(!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.InventoryCombat&&(connectedCombat==null||s.Encounter==null||s.Encounter.CurrentActor!=c.Actor))return "WrongRegularTurn";
            if(kind==HuntingTrapActionKind.Free) {
                tether=ActiveHuntingTrapTether(s,c.Target);
                if(tether==null)return "TargetNotTethered";
                var helper=s.Actors.Single(x=>x.Id==c.Actor);var target=s.Actors.Single(x=>x.Id==c.Target);
                if(!WorldAdjacent(helper,target.X,target.Y))return "TrappedCreatureOutOfReach";
                if(!WorldAdjacent(helper,tether.AnchorX,tether.AnchorY))return "HuntingTrapOutOfReach";
                if(WorkingHuntingTrapAction(s,c.Actor,c.Target)!=null)return "HuntingTrapTargetBusy";
                var selectedTether=tether;
                definition=huntingTrapFixture.Find(selectedTether.TrapItemId);
                deployment=s.HuntingTrapDeployments.Single(x=>x.Id==selectedTether.DeploymentId);
            } else {
                definition=huntingTrapFixture.Find(c.Target);
                if(definition==null)return "UnknownHuntingTrap";
                if(c.Actor!=definition.OwnerId)return "NoHuntingTrapPermission";
                var selectedDefinition=definition;
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==selectedDefinition.ItemId);
                if(item==null||item.ProfileId!="adventuring-gear.hunting-trap"||item.OwnerId!=c.Actor||item.CustodianId!=c.Actor)
                    return "HuntingTrapItemUnavailable";
                if(!PortableEquipmentRules.Accessible(s,c.Actor,item))return "HuntingTrapOutOfReach";
                if(WorkingHuntingTrapAction(s,c.Actor,item.Id)!=null)return "HuntingTrapBusy";
                deployment=LatestHuntingTrapDeployment(s,item.Id);
                var selectedDeployment=deployment;
                var actor=s.Actors.Single(x=>x.Id==c.Actor);
                if(kind==HuntingTrapActionKind.Set) {
                    if(item.Placement!=PortablePlacement.Carried||item.ParentId!="")return "HuntingTrapMustBeCarried";
                    if(selectedDeployment!=null&&selectedDeployment.Status==HuntingTrapDeploymentStatus.Armed)return "HuntingTrapAlreadySet";
                    if(!WorldAdjacent(actor,definition.AnchorX,definition.AnchorY))return "NoSuitableHuntingTrapAnchor";
                    if(s.Actors.Any(x=>x.Id!=actor.Id&&x.X==selectedDefinition.AnchorX&&x.Y==selectedDefinition.AnchorY))return "HuntingTrapAnchorOccupied";
                    if(ActiveHuntingTrapTether(s,c.Actor)!=null)return "ActorTethered";
                } else {
                    if(selectedDeployment==null||selectedDeployment.Status!=HuntingTrapDeploymentStatus.Sprung)return "HuntingTrapMustBeSprung";
                    if(s.HuntingTrapTethers.Any(x=>x.DeploymentId==selectedDeployment.Id&&x.Status==HuntingTrapTetherStatus.Active))
                        return "HuntingTrapCreatureStillTethered";
                    if(item.Placement!=PortablePlacement.Ground||item.GroundX!=selectedDeployment.AnchorX||item.GroundY!=selectedDeployment.AnchorY)
                        return "HuntingTrapNotAtAnchor";
                    if(!WorldAdjacent(actor,selectedDeployment.AnchorX,selectedDeployment.AnchorY))return "HuntingTrapOutOfReach";
                }
            }
            if(s.HuntingTrapActions.Any(x=>x.Status==HuntingTrapActionStatus.Working&&x.ActorId==c.Actor))return "WorkerBusy";
            return null;
        }

        private CommandQueryResult QueryHuntingTrapCommand(Snapshot s,Command c)
        {
            string error=AssessHuntingTrapCommand(s,c,out var kind,out _,out _,out _,out _);
            var costs=new System.Collections.Generic.List<CommandCost>();
            if(error==null&&c.X!=(int)HuntingTrapInteraction.Interrupt) {
                costs.Add(new CommandCost("action","",1));
                if(!s.InventoryCombat)costs.Add(new CommandCost("work-seconds","",6));
            }
            return new CommandQueryResult(true,error==null,error??"Available",s.Revision,costs);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverHuntingTrapCommands(Snapshot s,string actor)
        {
            if(huntingTrapFixture==null||!s.WorldSchedule.Order.Contains(actor))yield break;
            int index=0;
            foreach(var definition in huntingTrapFixture.Devices.Where(x=>x.OwnerId==actor)) {
                var working=WorkingHuntingTrapAction(s,actor,definition.ItemId);
                if(working!=null) {
                    yield return HuntingTrapOption(s,actor,working.TrapItemId==""?working.TargetActorId:working.TrapItemId,
                        HuntingTrapInteraction.Interrupt,index++);continue;
                }
                var deployment=LatestHuntingTrapDeployment(s,definition.ItemId);
                var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==definition.ItemId);
                if(item==null||!PortableEquipmentRules.Accessible(s,actor,item))continue;
                if(item.Placement==PortablePlacement.Carried&&(deployment==null||deployment.Status==HuntingTrapDeploymentStatus.Sprung)
                    &&WorldAdjacent(s.Actors.Single(x=>x.Id==actor),definition.AnchorX,definition.AnchorY))
                    yield return HuntingTrapOption(s,actor,definition.ItemId,HuntingTrapInteraction.Set,index++);
                else if(deployment!=null&&deployment.Status==HuntingTrapDeploymentStatus.Sprung
                    &&!s.HuntingTrapTethers.Any(x=>x.DeploymentId==deployment.Id&&x.Status==HuntingTrapTetherStatus.Active)
                    &&WorldAdjacent(s.Actors.Single(x=>x.Id==actor),deployment.AnchorX,deployment.AnchorY))
                    yield return HuntingTrapOption(s,actor,definition.ItemId,HuntingTrapInteraction.Reset,index++);
            }
            foreach(var tether in s.HuntingTrapTethers.Where(x=>x.Status==HuntingTrapTetherStatus.Active)
                .OrderBy(x=>x.ActorId,StringComparer.Ordinal)) {
                var working=WorkingHuntingTrapAction(s,actor,tether.ActorId);
                if(working!=null) {
                    yield return HuntingTrapOption(s,actor,tether.ActorId,HuntingTrapInteraction.Interrupt,index++);continue;
                }
                var body=s.Actors.Single(x=>x.Id==tether.ActorId);var helper=s.Actors.Single(x=>x.Id==actor);
                if(WorldAdjacent(helper,body.X,body.Y)&&WorldAdjacent(helper,tether.AnchorX,tether.AnchorY))
                    yield return HuntingTrapOption(s,actor,tether.ActorId,HuntingTrapInteraction.Free,index++);
            }
        }

        private static Command HuntingTrapOption(Snapshot s,string actor,string target,HuntingTrapInteraction action,int index)
            =>new Command("option."+Number(s.Revision)+".hunting-trap."+index.ToString(CultureInfo.InvariantCulture),actor,s.Revision,
                CommandKind.Interact,target,(int)action);

        private string ResolveHuntingTrapCommand(Snapshot s,Command c)
        {
            string error=AssessHuntingTrapCommand(s,c,out var kind,out var working,out var definition,out var deployment,out var tether);
            if(error!=null)return error;
            if(c.X==(int)HuntingTrapInteraction.Interrupt) {InterruptHuntingTrapAction(s,working);return null;}
            bool tactical=s.InventoryCombat;RuleTime start=s.RuleClock;string actionId=HuntingTrapIdentity("action|"+Number(s.Revision+1)+"|"+c.Actor+"|"+c.Target+"|"+Number(c.X));
            SetInterval(s,Interval(s,c.Actor).PayAction());
            var action=new HuntingTrapActionRecord(actionId,kind,c.Actor,kind==HuntingTrapActionKind.Free?tether.TrapItemId:definition.ItemId,
                kind==HuntingTrapActionKind.Free?c.Target:"",kind==HuntingTrapActionKind.Set?"":deployment.Id,start,null,
                HuntingTrapActionStatus.Working,tactical);
            if(tactical) {
                var resolved=ResolveHuntingTrapAction(s,action,definition,deployment,tether);
                s.HuntingTrapActions=s.HuntingTrapActions.Concat(new[]{resolved}).ToArray();return null;
            }
            if(s.Work.WorkerIntervals.Count>=Snapshot.MaxWorkRecords)return "WorkHistoryCapacityReached";
            s.Work=s.Work.Reserve(action.Id,new[]{new WorkerInterval(action.Id+".labor",action.Id,c.Actor,start,start.AddSeconds(6))},
                Array.Empty<ResourceReservation>());
            s.HuntingTrapActions=s.HuntingTrapActions.Concat(new[]{action}).ToArray();return null;
        }

        private HuntingTrapActionRecord ResolveHuntingTrapAction(Snapshot s,HuntingTrapActionRecord action,
            HuntingTrapDefinition definition,HuntingTrapDeploymentRecord deployment,HuntingTrapTetherRecord tether)
        {
            if(action.Kind==HuntingTrapActionKind.Set) {
                var item=s.PortableEquipment.Single(x=>x.Id==action.TrapItemId);
                s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==item.Id?item.With(placement:PortablePlacement.Ground,
                    groundX:definition.AnchorX,groundY:definition.AnchorY):x).ToArray();
                string id=HuntingTrapIdentity("deployment|"+action.Id);
                s.HuntingTrapDeployments=s.HuntingTrapDeployments.Concat(new[]{new HuntingTrapDeploymentRecord(id,item.Id,action.ActorId,
                    definition.AnchorX,definition.AnchorY,s.Revision+1,s.RuleClock)}).ToArray();
                return action.Resolve(s.RuleClock,HuntingTrapActionStatus.Succeeded,id);
            }
            if(action.Kind==HuntingTrapActionKind.Reset) {
                if(deployment==null||deployment.Status!=HuntingTrapDeploymentStatus.Sprung
                    ||s.HuntingTrapTethers.Any(x=>x.DeploymentId==deployment.Id&&x.Status==HuntingTrapTetherStatus.Active))
                    return action.Interrupt(s.RuleClock);
                string id=HuntingTrapIdentity("deployment|"+action.Id);
                s.HuntingTrapDeployments=s.HuntingTrapDeployments.Concat(new[]{new HuntingTrapDeploymentRecord(id,deployment.TrapItemId,
                    action.ActorId,deployment.AnchorX,deployment.AnchorY,s.Revision+1,s.RuleClock)}).ToArray();
                return action.Resolve(s.RuleClock,HuntingTrapActionStatus.Succeeded,id);
            }
            if(tether==null||tether.Status!=HuntingTrapTetherStatus.Active)return action.Interrupt(s.RuleClock);
            var actor=s.Characters.Single(x=>x.ActorId==action.ActorId);var target=s.Actors.Single(x=>x.Id==tether.ActorId);
            int modifier=CharacterRuleFacts.From(actor).AbilityModifier(CharacterAbility.Strength);int natural=0;long total=0;bool success=false;
            uint before=s.RandomState,after=before;long words=0;
            var checkConditions=TestOnlyClubAttackPolicy.ConditionsFor(s,action.ActorId).View();
            var roll=PlaytestDice.RollD20(before,disadvantageSources:checkConditions.Has(ConditionKind.Poisoned)?1:0);
            natural=roll.Natural;after=roll.NextRandomState;words=roll.WordsConsumed;
            success=PlaytestRolls.TaskCheck(natural,modifier,13).Success;total=(long)natural+modifier;s.RandomState=after;
            if(success) {
                var released=tether.Release(s.Revision+1,action.Id);SetHuntingTrapTether(s,released);
                return action.Resolve(s.RuleClock,HuntingTrapActionStatus.Succeeded,deployment.Id,false,natural,modifier,13,total,true,0,before,after,words);
            }
            var life=s.Lives.Single(x=>x.ActorId==target.Id);long damage=CharacterAdvancementRules.ReduceIncomingDamage(s,target.Id,1);
            int con=checked(CharacterRuleFacts.ForActor(s,target.Id).AbilityModifier(CharacterAbility.Constitution)
                +CharacterAdvancementRules.SaveProficiencyBonus(s,target.Id,"CON"));
            var hurt=PlaytestDamageDice.Resolve(ActorLifeRules.Read(life),damage,s.RuleClock,s.RandomState,constitutionSaveModifier:con,melee:false);
            s.RandomState=hurt.NextRandomState;TestOnlyClubAttackPolicy.ApplyLife(s,life,hurt.Outcome.State);
            words=checked(words+hurt.WordsConsumed);after=s.RandomState;
            return action.Resolve(s.RuleClock,HuntingTrapActionStatus.Failed,deployment.Id,false,natural,modifier,13,total,false,1,before,after,words);
        }

        private void CompleteHuntingTrapActions(Snapshot s)
        {
            foreach(var action in s.HuntingTrapActions.Where(x=>x.Status==HuntingTrapActionStatus.Working
                &&x.StartedAt.AddSeconds(6)==s.RuleClock).ToArray()) {
                if(!CanContinueHuntingTrapAction(s,action)) {InterruptHuntingTrapAction(s,action);continue;}
                var definition=huntingTrapFixture.Find(action.TrapItemId);var deployment=action.DeploymentId==""?LatestHuntingTrapDeployment(s,action.TrapItemId)
                    :s.HuntingTrapDeployments.SingleOrDefault(x=>x.Id==action.DeploymentId);
                var tether=action.TargetActorId==""?null:ActiveHuntingTrapTether(s,action.TargetActorId);
                SetHuntingTrapAction(s,ResolveHuntingTrapAction(s,action,definition,deployment,tether));
            }
        }
        private static RuleTime? NextHuntingTrapActionBoundary(Snapshot s)
        {
            var due=s.HuntingTrapActions.Where(x=>x.Status==HuntingTrapActionStatus.Working).Select(x=>x.StartedAt.AddSeconds(6)).ToArray();
            return due.Length==0?(RuleTime?)null:due.Min();
        }
        private bool CanContinueHuntingTrapAction(Snapshot s,HuntingTrapActionRecord action)
        {
            if(!CapableWorker(s,action.ActorId)||AvailableHands(s,action.ActorId)<1||s.WorldTraversals.Any(x=>x.ActorId==action.ActorId)
                ||!s.WorldSchedule.Order.Contains(action.ActorId))return false;
            if(s.WorldIntervals.All(x=>x.ActorId!=action.ActorId))return false;
            if(action.Kind==HuntingTrapActionKind.Free) {
                var tether=ActiveHuntingTrapTether(s,action.TargetActorId);if(tether==null)return false;
                var helper=s.Actors.Single(x=>x.Id==action.ActorId);var target=s.Actors.Single(x=>x.Id==action.TargetActorId);
                return WorldAdjacent(helper,target.X,target.Y)&&WorldAdjacent(helper,tether.AnchorX,tether.AnchorY);
            }
            var definition=huntingTrapFixture.Find(action.TrapItemId);var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==action.TrapItemId);
            if(definition==null||item==null||item.OwnerId!=action.ActorId||item.CustodianId!=action.ActorId)return false;
            var actor=s.Actors.Single(x=>x.Id==action.ActorId);
            if(!WorldAdjacent(actor,definition.AnchorX,definition.AnchorY))return false;
            if(action.Kind==HuntingTrapActionKind.Set)return item.Placement==PortablePlacement.Carried
                &&!s.HuntingTrapDeployments.Any(x=>x.TrapItemId==item.Id&&x.Status==HuntingTrapDeploymentStatus.Armed);
            var deployment=s.HuntingTrapDeployments.SingleOrDefault(x=>x.Id==action.DeploymentId);
            return deployment!=null&&deployment.Status==HuntingTrapDeploymentStatus.Sprung
                &&!s.HuntingTrapTethers.Any(x=>x.DeploymentId==deployment.Id&&x.Status==HuntingTrapTetherStatus.Active)
                &&item.Placement==PortablePlacement.Ground&&item.GroundX==deployment.AnchorX&&item.GroundY==deployment.AnchorY;
        }
        private static void InterruptHuntingTrapAction(Snapshot s,HuntingTrapActionRecord action)
        {
            if(action==null||action.Status!=HuntingTrapActionStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(action.Id,s.RuleClock);SetHuntingTrapAction(s,action.Interrupt(s.RuleClock));
        }
        private void InterruptIncompatibleHuntingTrapActions(Snapshot s)
        {
            foreach(var action in s.HuntingTrapActions.Where(x=>x.Status==HuntingTrapActionStatus.Working
                &&!CanContinueHuntingTrapAction(s,x)).ToArray())InterruptHuntingTrapAction(s,action);
        }

        private static HuntingTrapTriggerRecord PendingHuntingTrapTrigger(Snapshot s)
            =>s.HuntingTrapTriggers.Where(x=>x.Status==HuntingTrapTriggerStatus.Pending).OrderBy(x=>x.CreatedRevision)
                .ThenBy(x=>x.SourceAppliedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).FirstOrDefault();
        private string QueueHuntingTrapEntry(Snapshot s,string actor,string entryId,HuntingTrapEntryKind entryKind,int x,int y,long createdRevision,
            RuleTime? occurredAt=null,string routeId="",long routeStartedRevision=0,RuleQuantity routeProgress=default(RuleQuantity))
        {
            if(huntingTrapFixture==null)return null;
            foreach(var deployment in s.HuntingTrapDeployments.Where(d=>d.Status==HuntingTrapDeploymentStatus.Armed
                &&d.AnchorX==x&&d.AnchorY==y).OrderBy(d=>d.ArmedRevision).ThenBy(d=>d.Id,StringComparer.Ordinal).ToArray()) {
                var definition=huntingTrapFixture.Find(deployment.TrapItemId);
                if(definition==null||!definition.CanTrigger(actor))continue;
                if(!HuntingTrapValidation.CanReserveEntries(s))return "HuntingTrapHistoryCapacityReached";
                string id=HuntingTrapIdentity("entry|"+deployment.Id+"|"+entryId);
                var trigger=new HuntingTrapTriggerRecord(id,deployment.Id,entryId,entryKind,actor,createdRevision,0,
                    deployment.ArmedRevision,occurredAt??s.RuleClock,HuntingTrapTriggerStatus.Pending,
                    routeId:routeId,routeStartedRevision:routeStartedRevision,routeProgress:routeProgress);
                s.HuntingTrapTriggers=s.HuntingTrapTriggers.Concat(new[]{trigger}).ToArray();
                SetHuntingTrapDeployment(s,deployment.Sprung(id));
            }
            return null;
        }
        private void ResolveWorldHuntingTrapTriggers(Snapshot s)
        {
            if(s.InventoryCombat)return;
            foreach(var trigger in s.HuntingTrapTriggers.Where(x=>x.Status==HuntingTrapTriggerStatus.Pending
                &&(x.EntryKind==HuntingTrapEntryKind.ExplorationStep||x.EntryKind==HuntingTrapEntryKind.RouteTravelCheckpoint))
                .OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.SourceAppliedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray())
                ResolveHuntingTrapTrigger(s,trigger);
        }
        private void ResolveOrderedHuntingTrapTrigger(Snapshot s)
        {
            while(s.InventoryCombat&&s.MeleeAttacks.All(x=>!x.Pending)
                &&!s.OverwatchRiderChoices.Any(x=>x.Status==OverwatchRiderChoiceStatus.Pending)) {
                var next=NextPostStepChoice(s);if(next!=PostStepChoiceKind.HuntingTrap)break;
                var trigger=PendingHuntingTrapTrigger(s);if(trigger==null)break;
                ResolveHuntingTrapTrigger(s,trigger);
                NormalizePendingReadyOccurrences(s);
            }
        }
        private void ResolveHuntingTrapTrigger(Snapshot s,HuntingTrapTriggerRecord trigger)
        {
            if(trigger==null||trigger.Status!=HuntingTrapTriggerStatus.Pending)return;
            var deployment=s.HuntingTrapDeployments.Single(x=>x.Id==trigger.DeploymentId);
            var target=s.Actors.Single(x=>x.Id==trigger.EntrantId);var life=s.Lives.Single(x=>x.ActorId==trigger.EntrantId);
            var character=CharacterRuleFacts.ForActor(s,trigger.EntrantId);int modifier=checked(character.AbilityModifier(CharacterAbility.Dexterity)
                +CharacterAdvancementRules.SaveProficiencyBonus(s,target.Id,"DEX"));
            bool automatic=life.Hp==0||life.Dead||TestOnlyClubAttackPolicy.ConditionsFor(s,target.Id).View().AutomaticStrengthDexterityFailure;
            uint before=s.RandomState,after=before;long words=0;int natural=0;long total=0;bool success=false;
            if(!automatic) {
                var save=PlaytestDice.RollD20(before,TestOnlyClubAttackPolicy.DodgeEffective(s,target.Id)?1:0);natural=save.Natural;after=save.NextRandomState;words=save.WordsConsumed;
                var result=PlaytestRolls.SavingThrow(natural,modifier,13);total=result.Total;success=result.Success;s.RandomState=after;
            }
            int rolled=0;long applied=0;string tetherId="";
            if(!success) {
                var d4=DiceStream.Draw(s.RandomState,4);rolled=d4.Value+1;s.RandomState=d4.NextState;words=checked(words+d4.WordsConsumed);
                applied=CharacterAdvancementRules.ReduceIncomingDamage(s,target.Id,rolled);
                int con=checked(character.AbilityModifier(CharacterAbility.Constitution)
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,target.Id,"CON"));
                var hurt=PlaytestDamageDice.Resolve(ActorLifeRules.Read(life),applied,s.RuleClock,s.RandomState,
                    constitutionSaveModifier:con,melee:false);
                s.RandomState=hurt.NextRandomState;TestOnlyClubAttackPolicy.ApplyLife(s,life,hurt.Outcome.State);
                words=checked(words+hurt.WordsConsumed);
                tetherId=HuntingTrapIdentity("tether|"+trigger.Id);
                s.HuntingTrapTethers=s.HuntingTrapTethers.Concat(new[]{new HuntingTrapTetherRecord(tetherId,trigger.Id,
                    deployment.Id,deployment.TrapItemId,target.Id,deployment.AnchorX,deployment.AnchorY)}).ToArray();
            }
            SetHuntingTrapTrigger(s,trigger.Resolve(s.Revision+1,automatic,natural,modifier,total,success,rolled,applied,tetherId,before,s.RandomState,words));
            if(!success&&trigger.EntryKind==HuntingTrapEntryKind.RouteTravelCheckpoint) {
                var travel=s.RouteTravels.Single(x=>x.StartedRevision==trigger.RouteStartedRevision);
                if(travel.Status==ExpeditionRouteTravelStatus.Moving)
                    SetRouteTravel(s,travel.With(travel.NominalEffort,ExpeditionRouteTravelStatus.Paused));
            }
            if(!s.InventoryCombat)InterruptIncompatibleHuntingTrapActions(s);
        }

        private string QueueCompletedTacticalHuntingTrapEntries(Snapshot s)
        {
            if(huntingTrapFixture==null||!s.InventoryCombat)return null;
            foreach(var move in s.TacticalMoves.Where(x=>x.Status==TacticalMoveStatus.Completed&&x.ResolvedRevision==s.Revision+1)
                .OrderBy(x=>x.ResolvedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                string error=QueueHuntingTrapEntry(s,move.ActorId,move.Id,HuntingTrapEntryKind.TacticalStep,move.ToX,move.ToY,move.ResolvedRevision);
                if(error!=null)return error;
            }
            foreach(var push in s.OverwatchRiderChoices.Where(x=>x.Status==OverwatchRiderChoiceStatus.Resolved
                &&x.Choice==OverwatchRider.Push&&x.MovedFeet>0&&x.ResolvedRevision==s.Revision+1)
                .OrderBy(x=>x.ResolvedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                string error=QueueHuntingTrapEntry(s,push.TargetId,push.Id,HuntingTrapEntryKind.ForcedTacticalStep,push.ToX,push.ToY,push.ResolvedRevision);
                if(error!=null)return error;
            }
            return null;
        }
        private static bool HuntingTrapTetherBlocksGridMove(Snapshot s,string actor,int x,int y)
        {
            if(s.SchemaVersion<Snapshot.HuntingTrapSchema)return false;
            var tether=ActiveHuntingTrapTether(s,actor);if(tether==null)return false;
            return PlanarCombatGeometry.DistanceFeet(new CombatCell(x,y),new CombatCell(tether.AnchorX,tether.AnchorY))>tether.MaximumDistanceFeet;
        }
        public static bool PendingHuntingTrapEntryBlocksMove(Snapshot s,string actor,int x,int y)
        {
            if(s?.HuntingTrapTriggers==null||s.HuntingTrapDeployments==null)return false;
            foreach(var trigger in s.HuntingTrapTriggers.Where(t=>t.Status==HuntingTrapTriggerStatus.Pending&&t.EntrantId==actor)
                .OrderBy(t=>t.CreatedRevision).ThenBy(t=>t.SourceAppliedRevision).ThenBy(t=>t.Id,StringComparer.Ordinal)) {
                var deployment=s.HuntingTrapDeployments.SingleOrDefault(d=>d.Id==trigger.DeploymentId);
                if(deployment!=null&&PlanarCombatGeometry.DistanceFeet(new CombatCell(x,y),
                    new CombatCell(deployment.AnchorX,deployment.AnchorY))>3)return true;
            }
            return false;
        }
    }

    public enum HuntingTrapInteraction { Set=20,Reset=21,Free=22,Interrupt=23 }
}
#endif
