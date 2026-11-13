#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One authored ordinary unattended-Trap witness. It supplies a complete unenchanted
    /// Trap with bait holder, one finite compatible ordinary bait portion, one finite opportunity,
    /// and one compatible ordinary fish, without an equipment bonus.</summary>
    public sealed class SharedFishingTrapFixture
    {
        public const string TrapId="TEST_ONLY.fishing-trap",OpportunityId="TEST_ONLY.riverbank.opportunity",
            CreatureId="TEST_ONLY.river-fish",SiteId="TEST_ONLY.riverbank",BaitLotId="TEST_ONLY.trap-ordinary-bait",
            BaitUnit="ordinary-angling-bait-0.10lb";
        public int CatchDc { get; }
        public int ProficiencyRank { get; }
        public bool HasBait { get; }
        public string TrapIdentity { get; }
        public string OpportunityIdentity { get; }
        public string CreatureIdentity { get; }
        public string SiteIdentity { get; }
        public string BaitLotIdentity { get; }
        public string SupportIdentity { get; }
        public string ReceiverIdentity { get; }
        public string ReceiverSupportIdentity { get; }
        public string SharedStockIdentity { get; }
        public string StockVersionIdentity { get; }
        public int TrapX { get; }
        public int TrapY { get; }
        public int ReceiverX { get; }
        public int ReceiverY { get; }
        public int RecoveryPathFeet { get; }
        public string SetterId { get; }
        public string TrapOwnerId { get; }
        public int InitialSetterWisdomScore { get; }
        public int InitialSetterIntelligenceScore { get; }
        public SharedFishingTrapFixture(int catchDc=12,int proficiencyRank=1,bool hasBait=true,string identity="riverbank",
            int trapX=3,int trapY=4,int receiverX=3,int receiverY=3,int recoveryPathFeet=5,string setterId=null,
            string sharedSiteIdentity=null,string sharedCreatureIdentity=null,string sharedStockIdentity=null,string trapOwnerId=null,
            int setterWisdomScore=10,int setterIntelligenceScore=10)
        {
            setterId=setterId??TestOnlyPolicy.CompanionId;
            trapOwnerId=trapOwnerId??setterId;
            if(catchDc!=12&&catchDc!=15&&catchDc!=18||proficiencyRank<0||proficiencyRank>2||!Validation.ValidId(identity)
                ||setterId!=TestOnlyPolicy.CompanionId&&setterId!=AdditionalTacticalActor.Id
                ||trapOwnerId!=TestOnlyPolicy.ActorId&&trapOwnerId!=TestOnlyPolicy.CompanionId&&trapOwnerId!=AdditionalTacticalActor.Id
                ||sharedSiteIdentity!=null&&!Validation.ValidId(sharedSiteIdentity)
                ||sharedCreatureIdentity!=null&&!Validation.ValidId(sharedCreatureIdentity)
                ||sharedStockIdentity!=null&&!Validation.ValidId(sharedStockIdentity)
                ||setterWisdomScore<3||setterWisdomScore>20||setterIntelligenceScore<3||setterIntelligenceScore>20
                ||trapX<0||trapY<0||receiverX<0||receiverY<0||recoveryPathFeet<0||recoveryPathFeet>1000)
                throw new ArgumentException("Fishing Trap fixture requires a source-listed DC, valid world layout, supported setter and proficiency rank 0–2.");
            CatchDc=catchDc;ProficiencyRank=proficiencyRank;HasBait=hasBait;SetterId=setterId;TrapOwnerId=trapOwnerId;
            bool defaultIdentity=identity=="riverbank";
            string root="TEST_ONLY."+identity+".";
            TrapIdentity=defaultIdentity?TrapId:root+"trap";
            OpportunityIdentity=defaultIdentity?OpportunityId:root+"opportunity";
            CreatureIdentity=sharedCreatureIdentity??(defaultIdentity?CreatureId:root+"river-fish");
            SiteIdentity=sharedSiteIdentity??(defaultIdentity?SiteId:root+"site");
            BaitLotIdentity=defaultIdentity?BaitLotId:root+"ordinary-bait";
            SupportIdentity=root+"trap-support";ReceiverIdentity=root+"receiving-location";
            ReceiverSupportIdentity=root+"receiver-support";StockVersionIdentity=root+"stock-v1";
            SharedStockIdentity=sharedStockIdentity??root+"shared-stock";
            TrapX=trapX;TrapY=trapY;ReceiverX=receiverX;ReceiverY=receiverY;RecoveryPathFeet=recoveryPathFeet;
            InitialSetterWisdomScore=setterWisdomScore;InitialSetterIntelligenceScore=setterIntelligenceScore;
        }
        internal string Key=>"one-complete-unenchanted-trap-with-bait-holder|one-finite-compatible-ordinary-bait|one-finite-opportunity|one-compatible-ordinary-fish|no-equipment-bonus|bait="
            +HasBait.ToString(CultureInfo.InvariantCulture)+"|"
            +CatchDc.ToString(CultureInfo.InvariantCulture)+"|fishing-tackle-rank="+ProficiencyRank.ToString(CultureInfo.InvariantCulture)
            +"|"+TrapIdentity+"|"+OpportunityIdentity+"|"+CreatureIdentity+"|"+SiteIdentity+"|"+BaitLotIdentity
            +"|support="+SupportIdentity+"|receiver="+ReceiverIdentity+"|receiver-support="+ReceiverSupportIdentity
            +"|stock-version="+StockVersionIdentity
            +"|shared-stock="+SharedStockIdentity
            +"|trap="+TrapX.ToString(CultureInfo.InvariantCulture)+","+TrapY.ToString(CultureInfo.InvariantCulture)
            +"|receiver="+ReceiverX.ToString(CultureInfo.InvariantCulture)+","+ReceiverY.ToString(CultureInfo.InvariantCulture)
            +"|path-ft="+RecoveryPathFeet.ToString(CultureInfo.InvariantCulture)+"|alternate-worker=third-combatant-free-hands"
            +(SetterId==TestOnlyPolicy.CompanionId?"":"|setter="+SetterId)
            +(TrapOwnerId==SetterId?"":"|trap-owner="+TrapOwnerId);
        internal string HandoverKey=>Key+"|initial-setter-wisdom-score="+InitialSetterWisdomScore.ToString(CultureInfo.InvariantCulture)
            +"|initial-setter-intelligence-score="+InitialSetterIntelligenceScore.ToString(CultureInfo.InvariantCulture);
    }

    public enum FishingTrapInteraction { Set=1, Pause=2, Resume=3, Cancel=4, Abandon=5, Retrieve=6, PauseRetrieval=7, ResumeRetrieval=8 }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private bool connectedFishingTrap;

        internal TestOnlySharedWorldPolicy EnableConnectedFishingTrap(SharedFishingTrapFixture profile)
        {
            if (initializationStarted || !connectedRecipe4Batch || fishingTrapProfiles.Length != 0)
                throw new InvalidOperationException("Select the connected Fishing Trap before starting the recipe-4 expedition.");
            connectedFishingTrap = true;
            fishingTrapProfiles = new[] { profile };
            ContentFingerprint = ConnectedRecipe4Batch.FingerprintPrefix + RetreatHash(string.Join("|",
                ContentFingerprint, profile.Key,
                "connected-fishing-trap-v1|source=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|shared-wisdom|local-resume"));
            return this;
        }

        private static string FishingTrapFingerprint(string prior,SharedFishingTrapFixture fixture)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.fishing-trap-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+fixture.Key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string FishingTrapSetFingerprint(string prior,IEnumerable<SharedFishingTrapFixture> profiles)
        {
            string key=string.Join("||",profiles.OrderBy(x=>x.TrapIdentity,StringComparer.Ordinal).Select(x=>x.Key));
            using(var sha=SHA256.Create())return "TEST_ONLY.fishing-trap-set-v1-"+string.Concat(sha.ComputeHash(
                Encoding.UTF8.GetBytes(prior+"|world-profiles-v1|"+key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string FishingTrapHandoverFingerprint(string prior,IEnumerable<SharedFishingTrapFixture> profiles)
        {
            string key=string.Join("||",profiles.OrderBy(x=>x.TrapIdentity,StringComparer.Ordinal).Select(x=>x.HandoverKey));
            using(var sha=SHA256.Create())return "TEST_ONLY.fishing-transfer-v1-"+string.Concat(sha.ComputeHash(
                Encoding.UTF8.GetBytes(prior+"|mgt06-responsibility-handover-v1|source=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"+key))
                .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string BaitOnlyFishingTrapFingerprint(string prior,SharedFishingTrapFixture fixture)
        {
            string key="one-complete-unenchanted-trap-with-bait-holder|one-finite-compatible-ordinary-bait|one-finite-opportunity|one-compatible-ordinary-fish|no-equipment-bonus|bait="
                +fixture.HasBait.ToString(CultureInfo.InvariantCulture)+"|"+fixture.CatchDc.ToString(CultureInfo.InvariantCulture)
                +"|fishing-tackle-rank="+fixture.ProficiencyRank.ToString(CultureInfo.InvariantCulture)
                +(fixture.SetterId==TestOnlyPolicy.CompanionId?"":"|setter="+fixture.SetterId);
            using(var sha=SHA256.Create())return "TEST_ONLY.fishing-trap-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string LegacyFishingTrapFingerprint(string prior,SharedFishingTrapFixture fixture)
        {
            string key="one-complete-unenchanted-trap|one-finite-opportunity|one-compatible-ordinary-fish|no-bait|no-equipment-bonus|"
                +fixture.CatchDc.ToString(CultureInfo.InvariantCulture)+"|fishing-tackle-rank="+fixture.ProficiencyRank.ToString(CultureInfo.InvariantCulture)
                +(fixture.SetterId==TestOnlyPolicy.CompanionId?"":"|setter="+fixture.SetterId);
            using(var sha=SHA256.Create())return "TEST_ONLY.fishing-trap-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+key)).Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private void InitializeFishingTrap(Snapshot s)
        {
            if(fishingTrapProfiles.Length==0)return;
            if(fishingTrapResponsibilityHandoverEnabled) {
                foreach(var profile in fishingTrapProfiles.GroupBy(x=>x.SetterId,StringComparer.Ordinal).Select(x=>x.First())) {
                    var current=s.Characters.Single(x=>x.ActorId==profile.SetterId);
                    int[] abilities=current.Abilities.ToArray();
                    abilities[(int)CharacterAbility.Wisdom]=profile.InitialSetterWisdomScore;
                    abilities[(int)CharacterAbility.Intelligence]=profile.InitialSetterIntelligenceScore;
                    s.Characters=s.Characters.Select(x=>x.ActorId==profile.SetterId
                        ?new ActorCharacterRecord(x.ActorId,x.ProfileId,abilities,x.Levels):x).ToArray();
                }
            }
            // Snapshot schema is cumulative: schema35 also requires the shared Bonus Action
            // ledger introduced at schema24, even though this fixture does not grant Soldier features.
            if(!connectedFishingTrap)
                s.BonusActions=s.WorldIntervals.Select(x=>new ActorBonusActionRecord(x.ActorId,checked((int)x.LastStart))).ToArray();
            var skills=fishingTrapProfiles.GroupBy(x=>x.SetterId,StringComparer.Ordinal)
                .Select(g=>new SkillTrainingRecord(g.Key,"fishing-tackle",g.First().ProficiencyRank)).ToArray();
            s.SkillTraining=s.SkillTraining.Where(x=>x.SkillId!="fishing-tackle").Concat(skills).ToArray();
            if(!fishingTrapLegacy) {
                var baitLots=fishingTrapProfiles.Select(x=>new ResourceLot(x.BaitLotIdentity,SharedFishingTrapFixture.BaitUnit,
                    x.HasBait?1:0,x.TrapIdentity+".bait-holder",x.SetterId));
                s.Work=new WorkLedger(s.Work.Lots.Concat(baitLots),
                    s.Work.WorkerIntervals,s.Work.Reservations);
                s.InventoryLots=s.InventoryLots.Concat(fishingTrapProfiles.Select(x=>new InventoryLotRecord(x.BaitLotIdentity,"",
                    x.SetterId,new RuleQuantity(x.HasBait?1:0),default,NutritionKind.None,null,InventoryAccess.Ready))).ToArray();
            }
            if(s.SchemaVersion<Snapshot.FishingTrapSchema)return;
            var equipment=new System.Collections.Generic.List<PortableEquipmentRecord>();
            var structures=new System.Collections.Generic.List<ObjectStructureRecord>();
            foreach(var profile in fishingTrapProfiles) {
                var trapItem=new PortableEquipmentRecord(profile.TrapIdentity,"fishing-equipment.trap",profile.TrapOwnerId,profile.SetterId,"",
                    PortablePlacement.Ground,PortableLinkKind.None,"",PortableMassBasis.Fixed,new RuleQuantity(4),new RuleQuantity(4),
                    groundX:profile.TrapX,groundY:profile.TrapY);
                string trapLocation=PortableEquipmentValidation.GroundLocation(trapItem);
                equipment.Add(trapItem);
                structures.Add(new ObjectStructureRecord(profile.TrapIdentity,"fishing-equipment.trap",profile.TrapOwnerId,profile.SetterId,
                    trapLocation,ObjectMaterial.IronSteel,5,5,0,new RuleQuantity(4)));
                structures.Add(new ObjectStructureRecord(profile.SupportIdentity,"fishing-support.shoreline-anchor",profile.SetterId,profile.SetterId,
                    profile.SiteIdentity,ObjectMaterial.Stone,100,100,0,new RuleQuantity(1)));
                structures.Add(new ObjectStructureRecord(profile.ReceiverSupportIdentity,"fishing-support.receiving-platform",profile.SetterId,profile.SetterId,
                    profile.ReceiverIdentity,ObjectMaterial.WoodLeather,100,100,0,new RuleQuantity(1)));
            }
            s.PortableEquipment=s.PortableEquipment.Concat(equipment).ToArray();
            s.Structures=s.Structures.Concat(structures).ToArray();
            s.FishingOpportunities=fishingTrapProfiles.Select(profile=>new FishingOpportunityRecord(profile.OpportunityIdentity,profile.SiteIdentity,
                profile.StockVersionIdentity,profile.CreatureIdentity,FishingOpportunityStatus.Available,"",null,"",null,"",null)).ToArray();
            s.FishingCreatures=fishingTrapProfiles.GroupBy(profile=>profile.CreatureIdentity,StringComparer.Ordinal).Select(g=>g.First())
                .Select(profile=>new FishingCreatureBodyRecord(profile.CreatureIdentity,"TEST_ONLY.ordinary-river-fish.1lb",
                profile.SiteIdentity,profile.SiteIdentity,profile.SiteIdentity,"",profile.SiteIdentity,FishingCreatureLifeState.Alive,
                new RuleQuantity(1),RuleQuantity.FromFraction(1,10),"","","",null,0)).ToArray();
            if(s.SchemaVersion>=Snapshot.FishingStockSchema) {
                var manifests=fishingTrapProfiles.GroupBy(profile=>profile.SharedStockIdentity+"|"+profile.StockVersionIdentity,StringComparer.Ordinal)
                    .Select(group=> {
                        var profile=group.First();
                        string[] members=fishingTrapProfiles.Where(x=>x.SharedStockIdentity==profile.SharedStockIdentity)
                            .Select(x=>x.CreatureIdentity).Distinct(StringComparer.Ordinal).ToArray();
                        return new FishingStockManifestRecord(profile.StockVersionIdentity,profile.SharedStockIdentity,
                            profile.StockVersionIdentity,default, null,members);
                    }).ToArray();
                s.FishingStockManifests=manifests;
                s.FishingStockAllocations=fishingTrapProfiles.Select(profile=> {
                    var manifest=manifests.Single(x=>x.SharedStockId==profile.SharedStockIdentity
                        &&x.VersionId==profile.StockVersionIdentity);
                    string[] members={profile.CreatureIdentity};
                    return new FishingStockAllocationRecord(profile.OpportunityIdentity,manifest.Id,
                        profile.OpportunityIdentity,members.SequenceEqual(manifest.PhysicalMemberIds,StringComparer.Ordinal),members);
                }).ToArray();
            }
            s.FishingTraps=fishingTrapProfiles.Select(profile=>new FishingTrapPhysicalRecord(profile.TrapIdentity,profile.SiteIdentity,profile.SupportIdentity,
                FishingTrapPhysicalStatus.Staged,"","","",null,15,10,new RuleQuantity(1),new RuleQuantity(2),20,profile.TrapX,profile.TrapY)).ToArray();
            s.FishingReceiveLocations=fishingTrapProfiles.Select(profile=>new FishingReceiveLocationRecord(profile.ReceiverIdentity,profile.SiteIdentity,
                profile.ReceiverSupportIdentity,profile.ReceiverX,profile.ReceiverY,new RuleQuantity(20),new RuleQuantity(3),"",
                profile.RecoveryPathFeet)).ToArray();
            // The physical Trap witness includes a second capable recovery worker with two free
            // hands. Keep its supplied Club on the ground so retrieval does not waive grip rules.
            var alternateClub=connectedFishingTrap?null:s.Clubs.SingleOrDefault(x=>x.Id==AdditionalTacticalActor.ClubId&&x.HeldBy==AdditionalTacticalActor.Id);
            if(alternateClub!=null) {
                s.Clubs=s.Clubs.Select(x=>x.Id==alternateClub.Id?new ClubInstance(x.Id,x.ProfileId,x.OwnerId,x.CustodianId,"",x.CellX,x.CellY):x).ToArray();
                s.Lives=s.Lives.Select(l=>l.ActorId==AdditionalTacticalActor.Id
                    ?ActorLifeRules.Record(l.ActorId,ActorLifeRules.Read(l),l.Prone,s.Clubs.Where(x=>x.HeldBy==l.ActorId).Select(x=>x.Id)):l).ToArray();
            }
        }
        private SharedFishingTrapFixture FishingTrapProfile(string trapId)
            =>fishingTrapProfiles.SingleOrDefault(x=>x.TrapIdentity==trapId)
                ??throw new InvalidOperationException("Missing supplied fishing Trap profile: "+trapId);
        private bool IsFishingTrapCommand(Command c)=>fishingTrapProfiles.Length!=0&&c.Kind==CommandKind.Interact
            &&fishingTrapProfiles.Any(x=>x.TrapIdentity==c.Target);
        private bool IsFishingTrapResponsibilityHandoverCommand(Command c)
            =>fishingTrapResponsibilityHandoverEnabled&&c.Kind==CommandKind.HandoverFishingTrapResponsibility;
        private IEnumerable<Command> DiscoverFishingTrapResponsibilityHandoverCommands(Snapshot s,Authority authority,string actor)
        {
            if(!fishingTrapResponsibilityHandoverEnabled||s.InventoryCombat)yield break;
            var held=FishingTrapObligations(s,actor);
            if(held.Length!=1)yield break;
            int index=0;var attempt=held[0];
            foreach(var recipient in s.Actors.Select(x=>x.Id).Where(x=>x!=actor&&authority.ConsentsToHandover(x)
                &&FishingTrapObligations(s,x).Length==0).OrderBy(x=>x,StringComparer.Ordinal)) {
                string id="option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".fishing-handover."
                    +(index++).ToString(CultureInfo.InvariantCulture)+"."+attempt.Id;
                var command=new Command(id,actor,s.Revision,CommandKind.HandoverFishingTrapResponsibility,recipient);
                if(AssessFishingTrapResponsibilityHandover(s,command)==null)yield return command;
            }
        }
        private IEnumerable<Command> DiscoverFishingTrapControls(Snapshot s,string actor)
        {
            int index=0;
            foreach(var profile in fishingTrapProfiles.OrderBy(x=>x.TrapIdentity,StringComparer.Ordinal)) {
                foreach(var attempt in s.FishingTrapAttempts.Where(x=>x.TrapId==profile.TrapIdentity&&x.SetterId==actor
                    &&(x.Status==FishingTrapAttemptStatus.SettingUp||x.Status==FishingTrapAttemptStatus.Paused))
                    .OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                    if(attempt.Status==FishingTrapAttemptStatus.SettingUp)
                        yield return TrapControlOption(s,actor,profile.TrapIdentity,FishingTrapInteraction.Pause,index++);
                    else
                        yield return TrapControlOption(s,actor,profile.TrapIdentity,FishingTrapInteraction.Resume,index++);
                    yield return TrapControlOption(s,actor,profile.TrapIdentity,FishingTrapInteraction.Cancel,index++);
                }
                if(fishingTrapResponsibilityHandoverEnabled) {
                    var responsibility=CurrentFishingTrap(s,actor);
                    var physical=responsibility==null?null:s.FishingTraps.SingleOrDefault(x=>x.TrapId==responsibility.TrapId);
                    if(responsibility!=null&&responsibility.TrapId==profile.TrapIdentity&&responsibility.OpportunityCommitted
                        &&physical!=null&&physical.Status==FishingTrapPhysicalStatus.Deployed)
                        yield return TrapControlOption(s,actor,profile.TrapIdentity,FishingTrapInteraction.Abandon,index++);
                }
                foreach(var job in s.FishingTrapRetrievals.Where(x=>x.TrapId==profile.TrapIdentity
                    &&(x.Status==FishingTrapRetrievalStatus.Working&&x.WorkerId==actor||x.Status==FishingTrapRetrievalStatus.Paused))
                    .OrderBy(x=>x.Id,StringComparer.Ordinal)) {
                    yield return TrapControlOption(s,actor,profile.TrapIdentity,
                        job.Status==FishingTrapRetrievalStatus.Working?FishingTrapInteraction.PauseRetrieval:FishingTrapInteraction.ResumeRetrieval,index++);
                }
            }
        }
        private static Command TrapControlOption(Snapshot s,string actor,string trapId,FishingTrapInteraction operation,int index)
            =>new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".fishing-trap."+index.ToString(CultureInfo.InvariantCulture),
                actor,s.Revision,CommandKind.Interact,trapId,(int)operation);
        private CommandQueryResult QueryFishingTrapResponsibilityHandover(Snapshot s,Authority authority,Command c)
        {
            if(!IsFishingTrapResponsibilityHandoverCommand(c))
                return new CommandQueryResult(false,false,"UnsupportedOperation",s.Revision);
            if(!authority.ConsentsToHandover(c.Target))
                return new CommandQueryResult(true,false,"RecipientNotWilling",s.Revision);
            string failure=ResolveCore(s.Copy(),c);
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision);
        }
        private string AssessFishingTrapResponsibilityHandover(Snapshot s,Command c)
        {
            if(!fishingTrapResponsibilityHandoverEnabled||!PhysicalFishingEnabled)
                return "FishingTrapResponsibilityHandoverUnsupported";
            if(c.X!=0||c.Y!=0||c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.SuppressionFire!=null||c.DefensiveFormation!=null
                ||c.ExpeditionAssignment!=null||c.HarvestSelection!=null||c.MiningSelection!=null
                ||c.ProspectingExposure!=null||c.RouteMappingWork!=null)
                return "InvalidFishingTrapResponsibilityHandover";
            if(s.InventoryCombat)return "FishingRequiresExploration";
            if(c.Target==c.Actor||!s.Actors.Any(x=>x.Id==c.Target))return "InvalidFishingTrapRecipient";
            var held=FishingTrapObligations(s,c.Actor);
            if(held.Length==0)return "FishingTrapDeploymentUnavailable";
            if(held.Length!=1)return "FishingTrapResponsibilityAmbiguous";
            var attempt=held[0];
            if(!attempt.OpportunityCommitted)return "FishingTrapNotCommitted";
            var physical=s.FishingTraps.SingleOrDefault(x=>x.TrapId==attempt.TrapId);
            if(physical==null||physical.AttemptId!=attempt.Id||physical.Status!=FishingTrapPhysicalStatus.Deployed)
                return "FishingTrapDeploymentUnavailable";
            if(FishingTrapObligations(s,c.Target).Length!=0)return "FishingTrapDeploymentOccupied";
            return null;
        }
        private CommandQueryResult QueryFishingTrapControl(Snapshot s,Command c)
        {
            if(!IsFishingTrapCommand(c)||c.Combat!=null||c.Y!=0||!Enum.IsDefined(typeof(FishingTrapInteraction),c.X))
                return new CommandQueryResult(false,false,"UnsupportedOperation",s.Revision);
            var operation=(FishingTrapInteraction)c.X;
            if(operation!=FishingTrapInteraction.Pause&&operation!=FishingTrapInteraction.Resume&&operation!=FishingTrapInteraction.Cancel
                &&operation!=FishingTrapInteraction.Abandon&&operation!=FishingTrapInteraction.PauseRetrieval
                &&operation!=FishingTrapInteraction.ResumeRetrieval)
                return new CommandQueryResult(false,false,"UnsupportedOperation",s.Revision);
            string failure=AssessFishingTrapControl(s,c,operation);
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision);
        }
        private string AssessFishingTrapControl(Snapshot s,Command c,FishingTrapInteraction operation)
        {
            if((operation==FishingTrapInteraction.Resume||operation==FishingTrapInteraction.ResumeRetrieval)
                &&IsOffCalendarActivity(s,c.Actor)) {
                var activity=ActivityInterval(s,c.Actor);
                if(activity.Action==WorldActionCommitment.Dash
                    ||activity.Action==WorldActionCommitment.ActiveLabor&&!CanContinueActivityLabor(s,c.Actor))
                    return "OffCalendarActionAlreadySpent";
            }
            if(s.InventoryCombat)return "FishingRequiresExploration";
            var profile=FishingTrapProfile(c.Target);
            if(operation==FishingTrapInteraction.PauseRetrieval||operation==FishingTrapInteraction.ResumeRetrieval) {
                if(!PhysicalFishingEnabled||c.Inventory!=null)return "InvalidFishingTrapRetrieval";
                var job=operation==FishingTrapInteraction.PauseRetrieval
                    ?s.FishingTrapRetrievals.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity&&x.WorkerId==c.Actor&&x.Status==FishingTrapRetrievalStatus.Working)
                    :s.FishingTrapRetrievals.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity&&x.Status==FishingTrapRetrievalStatus.Paused);
                if(job==null)return operation==FishingTrapInteraction.PauseRetrieval?"FishingTrapRetrievalNotWorking":"FishingTrapRetrievalNotPaused";
                if(operation==FishingTrapInteraction.PauseRetrieval)return null;
                if(!FishingTrapWorkerCanContinue(s,c.Actor))return "FishingTrapWorkerUnavailable";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                var trap=s.FishingTraps.SingleOrDefault(x=>x.TrapId==job.TrapId);
                var receiver=s.FishingReceiveLocations.SingleOrDefault(x=>x.Id==job.DestinationId);
                var attempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==job.AttemptId);
                var creature=attempt==null?null:s.FishingCreatures.SingleOrDefault(x=>x.Id==attempt.CreatureId);
                if(trap==null||receiver==null||attempt==null||creature==null)return "FishingTrapDeploymentUnavailable";
                if(!FishingAccessFrom(s,c.Actor,trap.X,trap.Y))return "FishingTrapOutOfReach";
                if(!CanReceiveFishingTrap(s,trap,creature,receiver))return "FishingReceiveCapacityOrPathUnavailable";
                return null;
            }
            if(c.Inventory!=null)return "InvalidFishingTrapInteraction";
            if(operation==FishingTrapInteraction.Abandon&&fishingTrapResponsibilityHandoverEnabled) {
                var responsible=CurrentFishingTrap(s,c.Actor);
                if(responsible==null||responsible.TrapId!=profile.TrapIdentity)return "FishingTrapResponsibleHolderRequired";
            } else if(c.Actor!=profile.SetterId)return "FishingTrapSetterRequired";
            var current=CurrentFishingTrap(s,c.Actor);
            if(current==null||current.TrapId!=profile.TrapIdentity)return "FishingTrapDeploymentUnavailable";
            if(operation==FishingTrapInteraction.Pause)
                return current.Status==FishingTrapAttemptStatus.SettingUp?null:"FishingTrapNotSettingUp";
            if(operation==FishingTrapInteraction.Resume) {
                if(current.Status!=FishingTrapAttemptStatus.Paused)return "FishingTrapNotPaused";
                if(!FishingTrapWorkerCanContinue(s,c.Actor))return "FishingTrapSetterUnavailable";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                if(!FishingSetupResumeInReach(s,c,profile))return "FishingTrapOutOfReach";
                return null;
            }
            if(operation==FishingTrapInteraction.Abandon) {
                if(PhysicalFishingEnabled&&!current.OpportunityCommitted)return "FishingTrapNotCommitted";
                return null;
            }
            return current.Status==FishingTrapAttemptStatus.SettingUp||current.Status==FishingTrapAttemptStatus.Paused
                ?null:"FishingTrapAlreadyCommitted";
        }
        private bool PhysicalFishingEnabled=>fishingTrapProfiles.Length!=0&&!fishingTrapLegacy&&!fishingTrapBaitOnly;
        private static FishingTrapAttemptRecord[] FishingTrapObligations(Snapshot s,string actor)
            =>s.FishingTrapAttempts.Where(x=>x.ResponsibleHolderId==actor&&x.Status!=FishingTrapAttemptStatus.Cancelled
                &&x.Status!=FishingTrapAttemptStatus.Abandoned
                &&!(x.Status==FishingTrapAttemptStatus.CheckMissed&&!x.OpportunityCommitted)
                &&!s.FishingTraps.Any(t=>t.TrapId==x.TrapId&&t.AttemptId==x.Id&&t.Status==FishingTrapPhysicalStatus.Retrieved))
                .OrderByDescending(x=>x.StartedAt).ToArray();
        private static FishingTrapAttemptRecord CurrentFishingTrap(Snapshot s,string actor)
            =>FishingTrapObligations(s,actor).FirstOrDefault();
        private static void PutFishingTrap(Snapshot s,FishingTrapAttemptRecord value)
            =>s.FishingTrapAttempts=s.FishingTrapAttempts.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutFishingOpportunity(Snapshot s,FishingOpportunityRecord value)
            =>s.FishingOpportunities=s.FishingOpportunities.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutFishingCreature(Snapshot s,FishingCreatureBodyRecord value)
            =>s.FishingCreatures=s.FishingCreatures.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutFishingPhysical(Snapshot s,FishingTrapPhysicalRecord value)
            =>s.FishingTraps=s.FishingTraps.Select(x=>x.TrapId==value.TrapId?value:x).ToArray();
        private static void PutFishingReceiver(Snapshot s,FishingReceiveLocationRecord value)
            =>s.FishingReceiveLocations=s.FishingReceiveLocations.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutFishingRetrieval(Snapshot s,FishingTrapRetrievalRecord value)
            =>s.FishingTrapRetrievals=s.FishingTrapRetrievals.Select(x=>x.Id==value.Id?value:x).ToArray();
        private static void PutFishingStructure(Snapshot s,ObjectStructureRecord value)
            =>s.Structures=s.Structures.Select(x=>x.Id==value.Id?value:x).ToArray();
        internal static bool FishingAccessFrom(Snapshot s,string actor,int x,int y)
        {
            var body=s.Actors.SingleOrDefault(a=>a.Id==actor);
            return body!=null&&Math.Abs((long)body.X-x)+Math.Abs((long)body.Y-y)<=1;
        }
        private bool FishingSetupResumeInReach(Snapshot s,Command c,SharedFishingTrapFixture profile)
            => !connectedFishingTrap || FishingAccessFrom(s,c.Actor,profile.TrapX,profile.TrapY);
        private bool FishingTrapWorkerCanContinue(Snapshot s,string worker)
            =>CapableWorker(s,worker)&&AvailableHands(s,worker)>=2&&!s.WorldTraversals.Any(x=>x.ActorId==worker)
                &&!(s.InventoryCombat&&s.WorldSchedule.Order.Contains(worker));
        private void PauseFishingTrapSetupIfIncompatible(Snapshot s)
        {
            foreach(var attempt in s.FishingTrapAttempts.Where(x=>x.Status==FishingTrapAttemptStatus.SettingUp).ToArray()) {
                if(FishingTrapWorkerCanContinue(s,attempt.SetterId))continue;
                PauseFishingTrapSetup(s,attempt);
            }
            foreach(var job in s.FishingTrapRetrievals.Where(x=>x.Status==FishingTrapRetrievalStatus.Working).ToArray()) {
                if(FishingTrapWorkerCanContinue(s,job.WorkerId))continue;
                PauseFishingTrapRetrieval(s,job);
            }
        }
        private static void PauseFishingTrapSetup(Snapshot s,FishingTrapAttemptRecord attempt)
        {
            if(attempt.Status!=FishingTrapAttemptStatus.SettingUp)return;
            s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
            PutFishingTrap(s,new FishingTrapAttemptRecord(attempt.Id,attempt.SetterId,attempt.ResponsibleHolderId,attempt.TrapId,
                attempt.OpportunityId,attempt.CreatureId,attempt.CapturedCreatureId,attempt.SiteId,attempt.StartedAt,attempt.SetupLabor,
                null,attempt.CheckDueAt,null,null,FishingTrapAttemptStatus.Paused,false,0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,
                FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,attempt.BaitLotId,attempt.BaitReservationId,null));
        }
        private static void PauseFishingTrapForActor(Snapshot s,string actor)
        {
            foreach(var attempt in s.FishingTrapAttempts.Where(x=>x.SetterId==actor&&x.Status==FishingTrapAttemptStatus.SettingUp).ToArray())
                PauseFishingTrapSetup(s,attempt);
            foreach(var job in s.FishingTrapRetrievals.Where(x=>x.WorkerId==actor&&x.Status==FishingTrapRetrievalStatus.Working).ToArray())
                PauseFishingTrapRetrieval(s,job);
        }
        private static void PauseFishingTrapRetrieval(Snapshot s,FishingTrapRetrievalRecord job)
        {
            if(job.Status!=FishingTrapRetrievalStatus.Working)return;
            s.Work=s.Work.CancelFutureWork(job.Id,s.RuleClock);
            PutFishingRetrieval(s,job.WithPaused(s.RuleClock));
        }
        private void CreditFishingTrapWork(Snapshot s,RuleTime elapsed)
        {
            foreach(var attempt in s.FishingTrapAttempts.Where(x=>x.Status==FishingTrapAttemptStatus.SettingUp)
                .OrderBy(FishingTrapCommandSequence).ToArray()) {
                if(!s.Work.WorkerIntervals.Any(x=>x.JobId==attempt.Id&&x.Start<s.RuleClock&&x.End>=s.RuleClock))continue;
                RuleTime labor=AddTime(attempt.SetupLabor,elapsed);
                if(labor>new RuleTime(300))throw new InvalidOperationException("Fishing Trap setup was over-credited.");
                if(labor<new RuleTime(300)) {
                    PutFishingTrap(s,new FishingTrapAttemptRecord(attempt.Id,attempt.SetterId,attempt.ResponsibleHolderId,attempt.TrapId,
                        attempt.OpportunityId,attempt.CreatureId,"",attempt.SiteId,attempt.StartedAt,labor,null,attempt.CheckDueAt,null,null,
                        FishingTrapAttemptStatus.SettingUp,false,0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,
                        FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,attempt.BaitLotId,attempt.BaitReservationId,null));
                    continue;
                }
                // The schema38 responsibility-handover profile captures the pinned WIS check.
                // Earlier profiles retain their historical INT calculation and fingerprint so
                // existing snapshots continue to replay under their original behavior.
                var check=AbilityCheckRules.Derive(s,attempt.SetterId,"fishing-tackle",
                    fishingTrapResponsibilityHandoverEnabled || connectedFishingTrap ? CharacterAbility.Wisdom : CharacterAbility.Intelligence);
                RuleTime due=fishingTrapLegacy?s.RuleClock.AddSeconds(3000):attempt.CheckDueAt.Value;
                bool responseAvailable=true;
                // This witnessed dry-set sequence exposes its reserved bait when setup completes.
                if(PhysicalFishingEnabled) {
                    var opportunity=s.FishingOpportunities.Single(x=>x.Id==attempt.OpportunityId);
                    var creature=s.FishingCreatures.Single(x=>x.Id==opportunity.CandidateCreatureId);
                    if(opportunity.Status!=FishingOpportunityStatus.Reserved||opportunity.ReservedByAttemptId!=attempt.Id)
                        throw new InvalidOperationException("Reserved fishing opportunity changed before the exposure checkpoint.");
                    responseAvailable=creature.ActiveResponseAttemptId==""&&creature.ContainerId==""
                        &&creature.LifeState==FishingCreatureLifeState.Alive;
                    if(!fishingTrapLegacy)s.Work=s.Work.Consume(attempt.Id,attempt.BaitReservationId);
                    PutFishingOpportunity(s,opportunity.Commit(s.RuleClock));
                    if(responseAvailable)PutFishingCreature(s,creature.Reserve(attempt.Id));
                    PutFishingPhysical(s,s.FishingTraps.Single(x=>x.TrapId==attempt.TrapId).WithStatus(FishingTrapPhysicalStatus.Deployed,attempt.Id));
                } else if(!fishingTrapLegacy)s.Work=s.Work.Consume(attempt.Id,attempt.BaitReservationId);
                PutFishingTrap(s,new FishingTrapAttemptRecord(attempt.Id,attempt.SetterId,attempt.ResponsibleHolderId,attempt.TrapId,
                    attempt.OpportunityId,attempt.CreatureId,"",attempt.SiteId,attempt.StartedAt,labor,s.RuleClock,due,null,null,
                    responseAvailable?FishingTrapAttemptStatus.Soaking:FishingTrapAttemptStatus.NoResponse,true,
                    check.AbilityModifier,check.ProficiencyRank,check.ProficiencyBonus,
                    FishingTrapDiceSelection.None,0,0,0,0,0,FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,
                    attempt.BaitLotId,attempt.BaitReservationId,fishingTrapLegacy?(RuleTime?)null:s.RuleClock));
            }
            foreach(var job in s.FishingTrapRetrievals.Where(x=>x.Status==FishingTrapRetrievalStatus.Working&&x.WorkDone<new RuleTime(300)).ToArray()) {
                if(!s.Work.WorkerIntervals.Any(x=>x.JobId==job.Id&&x.Start<s.RuleClock&&x.End>=s.RuleClock))continue;
                RuleTime labor=AddTime(job.WorkDone,elapsed);
                if(labor>new RuleTime(300))throw new InvalidOperationException("Fishing Trap retrieval was over-credited.");
                PutFishingRetrieval(s,job.WithWork(labor,s.RuleClock));
            }
        }
        private static RuleTime AddTime(RuleTime a,RuleTime b)
        {
            var q=new RuleQuantity(a.Numerator,a.Denominator)+new RuleQuantity(b.Numerator,b.Denominator);
            return new RuleTime(q.Numerator,q.Denominator);
        }
        internal static long FishingTrapCommandSequence(FishingTrapAttemptRecord attempt)
        {
            const string prefix="fishing.trap.";
            if(!attempt.Id.StartsWith(prefix,StringComparison.Ordinal)
                ||!long.TryParse(attempt.Id.Substring(prefix.Length),NumberStyles.None,CultureInfo.InvariantCulture,out long sequence))
                throw new InvalidOperationException("Fishing deployment lacks its accepted command sequence.");
            return sequence;
        }
        private static RuleTime? NextFishingTrapBoundary(Snapshot s)
        {
            var values=s.FishingTrapAttempts.Where(x=>x.Status==FishingTrapAttemptStatus.SettingUp)
                .SelectMany(a=>s.Work.WorkerIntervals.Where(w=>w.JobId==a.Id&&w.End>s.RuleClock).Select(w=>(RuleTime?)w.End))
                .Concat(s.FishingTrapRetrievals.Where(x=>x.Status==FishingTrapRetrievalStatus.Working&&x.WorkDone<new RuleTime(300))
                    .SelectMany(j=>s.Work.WorkerIntervals.Where(w=>w.JobId==j.Id&&w.End>s.RuleClock).Select(w=>(RuleTime?)w.End)))
                .Concat(s.FishingTrapAttempts.Where(x=>x.Status!=FishingTrapAttemptStatus.Resolved
                    &&x.Status!=FishingTrapAttemptStatus.Cancelled&&x.Status!=FishingTrapAttemptStatus.Abandoned
                    &&x.Status!=FishingTrapAttemptStatus.CheckMissed&&x.Status!=FishingTrapAttemptStatus.RetrievedBeforeCheck
                    &&x.Status!=FishingTrapAttemptStatus.NoResponse
                    &&x.CheckDueAt>s.RuleClock).Select(x=>x.CheckDueAt))
                .ToArray();
            return values.Length==0?(RuleTime?)null:values.Min();
        }
        private void ResolveDueFishingTrapChecks(Snapshot s)
        {
            foreach(var attempt in s.FishingTrapAttempts.Where(x=>(x.Status==FishingTrapAttemptStatus.SettingUp
                ||x.Status==FishingTrapAttemptStatus.Paused||x.Status==FishingTrapAttemptStatus.Soaking)
                &&x.CheckDueAt==s.RuleClock).ToArray()) {
                var profile=FishingTrapProfile(attempt.TrapId);
                bool setupAndSoakEligible=attempt.Status==FishingTrapAttemptStatus.Soaking
                    &&(fishingTrapLegacy||attempt.SetupCompletedAt<=attempt.StartedAt.AddSeconds(300));
                if(!setupAndSoakEligible) {
                    if(attempt.Status==FishingTrapAttemptStatus.SettingUp)s.Work=s.Work.CancelFutureWork(attempt.Id,s.RuleClock);
                    if(!fishingTrapLegacy&&!attempt.BaitExposedAt.HasValue)s.Work=s.Work.Release(attempt.Id,attempt.BaitReservationId);
                    if(PhysicalFishingEnabled&&attempt.OpportunityCommitted) {
                        var candidate=s.FishingCreatures.Single(x=>x.Id==attempt.CreatureId);
                        if(candidate.ActiveResponseAttemptId==attempt.Id)PutFishingCreature(s,candidate.Release(attempt.Id));
                    }
                    if(PhysicalFishingEnabled&&!attempt.OpportunityCommitted) {
                        var opportunity=s.FishingOpportunities.Single(x=>x.Id==attempt.OpportunityId);
                        if(opportunity.Status==FishingOpportunityStatus.Reserved)PutFishingOpportunity(s,opportunity.Release(s.RuleClock));
                        PutFishingPhysical(s,s.FishingTraps.Single(x=>x.TrapId==attempt.TrapId).WithStatus(FishingTrapPhysicalStatus.Staged,""));
                    }
                    PutFishingTrap(s,new FishingTrapAttemptRecord(attempt.Id,attempt.SetterId,attempt.ResponsibleHolderId,attempt.TrapId,
                        attempt.OpportunityId,attempt.CreatureId,"",attempt.SiteId,attempt.StartedAt,attempt.SetupLabor,
                        attempt.SetupCompletedAt,attempt.CheckDueAt,s.RuleClock,null,FishingTrapAttemptStatus.CheckMissed,
                        attempt.OpportunityCommitted,0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,
                        FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,attempt.BaitLotId,
                        attempt.BaitReservationId,attempt.BaitExposedAt));
                    continue;
                }
                int extraDisadvantage=attempt.ProficiencyRank==0?1:0;
                if(TestOnlyClubAttackPolicy.ConditionsFor(s,attempt.SetterId).View().Has(ConditionKind.Poisoned))extraDisadvantage++;
                uint randomBefore=s.RandomState;
                var roll=PlaytestDice.RollD20(randomBefore,disadvantageSources:extraDisadvantage);
                int modifier=attempt.WisdomModifier+attempt.ProficiencyBonus;
                var check=PlaytestRolls.TaskCheck(roll.Natural,modifier,profile.CatchDc);
                var degree=check.Degree==TaskDegree.CriticalFailure?FishingTrapCheckDegree.CriticalFailure
                    :check.Degree==TaskDegree.Failure?FishingTrapCheckDegree.Failure
                    :check.Degree==TaskDegree.Success?FishingTrapCheckDegree.Success:FishingTrapCheckDegree.CriticalSuccess;
                s.RandomState=roll.NextRandomState;
                if(PhysicalFishingEnabled) {
                    var creature=s.FishingCreatures.Single(x=>x.Id==attempt.CreatureId);
                    if(check.Success)PutFishingCreature(s,creature.Capture(attempt.Id,attempt.TrapId,s.RuleClock));
                    else if(creature.ActiveResponseAttemptId==attempt.Id)PutFishingCreature(s,creature.Release(attempt.Id));
                }
                PutFishingTrap(s,new FishingTrapAttemptRecord(attempt.Id,attempt.SetterId,attempt.ResponsibleHolderId,attempt.TrapId,
                    attempt.OpportunityId,attempt.CreatureId,check.Success?attempt.CreatureId:"",attempt.SiteId,attempt.StartedAt,
                    attempt.SetupLabor,attempt.SetupCompletedAt,attempt.CheckDueAt,s.RuleClock,null,FishingTrapAttemptStatus.Resolved,true,
                    attempt.WisdomModifier,attempt.ProficiencyRank,attempt.ProficiencyBonus,
                    roll.Selection==D20Selection.Normal?FishingTrapDiceSelection.Normal:FishingTrapDiceSelection.Disadvantage,
                    roll.First,roll.Second??0,roll.Natural,modifier,profile.CatchDc,degree,
                    check.Success?FishingTrapCheckOutcome.CapturedInTrap:FishingTrapCheckOutcome.NoCatch,
                    randomBefore,roll.NextRandomState,roll.WordsConsumed,attempt.BaitLotId,attempt.BaitReservationId,attempt.BaitExposedAt));
            }
        }
        private bool CanReceiveFishingTrap(Snapshot s,FishingTrapPhysicalRecord trap,FishingCreatureBodyRecord creature,
            FishingReceiveLocationRecord receiver)
        {
            var receiverSupport=s.Structures.SingleOrDefault(x=>x.Id==receiver.SupportId);
            var item=s.PortableEquipment.SingleOrDefault(x=>x.Id==trap.TrapId);
            if(receiverSupport==null||receiverSupport.Broken||item==null||!item.OperationalWeightLb.HasValue
                ||receiver.SiteId!=trap.SiteId||receiver.RecoveryPathFeet<1||receiver.RecoveryPathFeet>trap.RecoveryCordFeet)return false;
            RuleQuantity mass=new RuleQuantity(0),volume=new RuleQuantity(0);
            foreach(var existing in s.FishingTraps.Where(x=>x.Status==FishingTrapPhysicalStatus.Retrieved&&x.ReceivingLocationId==receiver.Id)) {
                var existingItem=s.PortableEquipment.SingleOrDefault(x=>x.Id==existing.TrapId);
                if(existingItem==null||!existingItem.OperationalWeightLb.HasValue)return false;
                mass+=existingItem.OperationalWeightLb.Value;volume+=existing.BodyVolumeCubicFeet;
                var priorAttempt=s.FishingTrapAttempts.Single(x=>x.Id==existing.AttemptId);
                if(priorAttempt.CapturedCreatureId!="") {
                    var carried=s.FishingCreatures.SingleOrDefault(x=>x.Id==priorAttempt.CapturedCreatureId&&x.LocationId==receiver.Id);
                    if(carried!=null){mass+=carried.MassPounds;volume+=carried.VolumeCubicFeet;}
                }
            }
            mass+=item.OperationalWeightLb.Value;volume+=trap.BodyVolumeCubicFeet;
            if(creature.ContainerId==trap.TrapId){mass+=creature.MassPounds;volume+=creature.VolumeCubicFeet;}
            return mass<=receiver.CapacityPounds&&volume<=receiver.CapacityCubicFeet;
        }
        private string StartFishingTrapRetrieval(Snapshot s,Command c,FishingTrapAttemptRecord attempt)
        {
            if(!PhysicalFishingEnabled||c.Inventory==null||c.Inventory.Amount!=default(RuleQuantity)
                ||c.Inventory.Handling!=HandlingKind.Retrieve||!Validation.ValidId(c.Inventory.Destination))return "InvalidFishingTrapRetrieval";
            var trap=s.FishingTraps.SingleOrDefault(x=>x.TrapId==attempt.TrapId);
            var receiver=s.FishingReceiveLocations.SingleOrDefault(x=>x.Id==c.Inventory.Destination);
            if(trap==null||trap.Status!=FishingTrapPhysicalStatus.Deployed&&trap.Status!=FishingTrapPhysicalStatus.Abandoned)
                return "FishingTrapNotDeployed";
            if(attempt.Status==FishingTrapAttemptStatus.SettingUp||attempt.Status==FishingTrapAttemptStatus.Paused
                ||attempt.Status==FishingTrapAttemptStatus.Cancelled||!attempt.OpportunityCommitted)return "FishingTrapNotCommitted";
            if(s.FishingTrapRetrievals.Any(x=>x.AttemptId==attempt.Id&&x.Status!=FishingTrapRetrievalStatus.Complete))
                return "FishingTrapRetrievalAlreadyActive";
            if(receiver==null)return "FishingReceiveLocationUnavailable";
            if(!FishingAccessFrom(s,c.Actor,trap.X,trap.Y))return "FishingTrapOutOfReach";
            var body=s.Structures.SingleOrDefault(x=>x.Id==trap.TrapId);var support=s.Structures.SingleOrDefault(x=>x.Id==trap.SupportId);
            if(body==null||support==null||body.Broken||support.Broken)return "FishingTrapAssemblyUnavailable";
            if(receiver.ReservedByRetrievalId!="")return "FishingReceiveLocationReserved";
            if(!FishingTrapWorkerCanContinue(s,c.Actor))return "FishingTrapWorkerUnavailable";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            var creature=s.FishingCreatures.Single(x=>x.Id==attempt.CreatureId);
            if(!CanReceiveFishingTrap(s,trap,creature,receiver))return "FishingReceiveCapacityOrPathUnavailable";
            string id="fishing.trap.retrieval."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            RuleTime remaining=new RuleTime(300);
            var interval=new WorkerInterval(id+".work."+(s.Revision+1).ToString(CultureInfo.InvariantCulture),id,c.Actor,s.RuleClock,AddTime(s.RuleClock,remaining));
            s.Work=s.Work.Reserve(id,new[]{interval},Array.Empty<ResourceReservation>());
            PutFishingReceiver(s,receiver.Reserve(id));
            s.FishingTrapRetrievals=s.FishingTrapRetrievals.Concat(new[]{new FishingTrapRetrievalRecord(id,attempt.Id,trap.TrapId,
                c.Actor,receiver.Id,s.RuleClock,default,s.RuleClock,null,FishingTrapRetrievalStatus.Working)}).ToArray();
            return null;
        }
        private string ResumeFishingTrapRetrieval(Snapshot s,Command c,FishingTrapRetrievalRecord job)
        {
            if(job.Status!=FishingTrapRetrievalStatus.Paused)return "FishingTrapRetrievalNotPaused";
            if(!FishingTrapWorkerCanContinue(s,c.Actor))return "FishingTrapWorkerUnavailable";
            if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
            var trap=s.FishingTraps.Single(x=>x.TrapId==job.TrapId);
            var receiver=s.FishingReceiveLocations.Single(x=>x.Id==job.DestinationId);
            var attempt=s.FishingTrapAttempts.Single(x=>x.Id==job.AttemptId);
            var creature=s.FishingCreatures.Single(x=>x.Id==attempt.CreatureId);
            if(!FishingAccessFrom(s,c.Actor,trap.X,trap.Y))return "FishingTrapOutOfReach";
            if(!CanReceiveFishingTrap(s,trap,creature,receiver))return "FishingReceiveCapacityOrPathUnavailable";
            RuleTime remaining=RuleTime.FromFraction((System.Numerics.BigInteger)300*job.WorkDone.Denominator-job.WorkDone.Numerator,job.WorkDone.Denominator);
            string intervalId=job.Id+".work."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
            var interval=new WorkerInterval(intervalId,job.Id,c.Actor,s.RuleClock,AddTime(s.RuleClock,remaining));
            s.Work=s.Work.Reserve(job.Id,new[]{interval},Array.Empty<ResourceReservation>());
            PutFishingRetrieval(s,job.WithWorker(c.Actor,s.RuleClock));
            var latest=s.FishingTrapRetrievals.Single(x=>x.Id==job.Id);
            // WithWorker preserves pause state so construct the resumed work marker after booking.
            PutFishingRetrieval(s,new FishingTrapRetrievalRecord(latest.Id,latest.AttemptId,latest.TrapId,c.Actor,latest.DestinationId,
                latest.StartedAt,latest.WorkDone,s.RuleClock,null,FishingTrapRetrievalStatus.Working));
            return null;
        }
        private void CompleteFishingTrapRetrievals(Snapshot s)
        {
            foreach(var job in s.FishingTrapRetrievals.Where(x=>x.Status==FishingTrapRetrievalStatus.Working
                &&x.WorkDone==new RuleTime(300)&&x.UpdatedAt==s.RuleClock).ToArray()) {
                var attempt=s.FishingTrapAttempts.Single(x=>x.Id==job.AttemptId);
                var trap=s.FishingTraps.Single(x=>x.TrapId==job.TrapId);
                var receiver=s.FishingReceiveLocations.Single(x=>x.Id==job.DestinationId);
                var item=s.PortableEquipment.Single(x=>x.Id==job.TrapId);
                if(attempt.Status==FishingTrapAttemptStatus.Soaking) {
                    var candidate=s.FishingCreatures.Single(x=>x.Id==attempt.CreatureId);
                    if(candidate.ActiveResponseAttemptId==attempt.Id)PutFishingCreature(s,candidate.Release(attempt.Id));
                    PutFishingTrap(s,new FishingTrapAttemptRecord(attempt.Id,attempt.SetterId,attempt.ResponsibleHolderId,attempt.TrapId,
                        attempt.OpportunityId,attempt.CreatureId,"",attempt.SiteId,attempt.StartedAt,attempt.SetupLabor,
                        attempt.SetupCompletedAt,attempt.CheckDueAt,null,null,FishingTrapAttemptStatus.RetrievedBeforeCheck,true,
                        attempt.WisdomModifier,attempt.ProficiencyRank,attempt.ProficiencyBonus,FishingTrapDiceSelection.None,0,0,0,0,0,
                        FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,attempt.BaitLotId,attempt.BaitReservationId,attempt.BaitExposedAt));
                }
                attempt=s.FishingTrapAttempts.Single(x=>x.Id==job.AttemptId);
                var caught=s.FishingCreatures.Single(x=>x.Id==attempt.CreatureId);
                if(caught.ContainerId==trap.TrapId)PutFishingCreature(s,caught.RetrieveFromTrap(attempt.Id,receiver.Id,job.WorkerId));
                var moved=item.With(custodianId:job.WorkerId,groundX:receiver.X,groundY:receiver.Y,placement:PortablePlacement.Ground,parentId:"");
                s.PortableEquipment=s.PortableEquipment.Select(x=>x.Id==moved.Id?moved:x).ToArray();
                var structure=s.Structures.Single(x=>x.Id==moved.Id);
                PutFishingStructure(s,new ObjectStructureRecord(structure.Id,structure.ProfileId,structure.OwnerId,job.WorkerId,
                    PortableEquipmentValidation.GroundLocation(moved),structure.Material,structure.MaximumHp,structure.Hp,structure.BaselineCopper,structure.MassPounds));
                PutFishingPhysical(s,trap.WithRetrieved(job.Id,receiver.Id,s.RuleClock,receiver.X,receiver.Y));
                PutFishingReceiver(s,receiver.Release(job.Id));
                PutFishingRetrieval(s,job.WithCompleted(s.RuleClock));
            }
        }
        private string ResolveFishingTrap(Snapshot s,Command c)
        {
            if(c.Combat!=null||!fishingTrapProfiles.Any(x=>x.TrapIdentity==c.Target)||c.Y!=0
                ||!Enum.IsDefined(typeof(FishingTrapInteraction),c.X))return "InvalidFishingTrapInteraction";
            if(s.InventoryCombat)return "FishingRequiresExploration";
            var profile=FishingTrapProfile(c.Target);
            var operation=(FishingTrapInteraction)c.X;
            if(operation==FishingTrapInteraction.Retrieve) {
                if(!PhysicalFishingEnabled)return "FishingTrapRetrievalUnsupported";
                var physical=s.FishingTraps.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity);
                if(physical==null)return "FishingTrapDeploymentUnavailable";
                var deployedAttempt=s.FishingTrapAttempts.SingleOrDefault(x=>x.Id==physical.AttemptId);
                return deployedAttempt==null?"FishingTrapDeploymentUnavailable":StartFishingTrapRetrieval(s,c,deployedAttempt);
            }
            if(operation==FishingTrapInteraction.PauseRetrieval||operation==FishingTrapInteraction.ResumeRetrieval) {
                if(!PhysicalFishingEnabled||c.Inventory!=null)return "InvalidFishingTrapRetrieval";
                var job=operation==FishingTrapInteraction.PauseRetrieval
                    ?s.FishingTrapRetrievals.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity&&x.WorkerId==c.Actor&&x.Status==FishingTrapRetrievalStatus.Working)
                    :s.FishingTrapRetrievals.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity&&x.Status==FishingTrapRetrievalStatus.Paused);
                if(job==null)return operation==FishingTrapInteraction.PauseRetrieval?"FishingTrapRetrievalNotWorking":"FishingTrapRetrievalNotPaused";
                if(operation==FishingTrapInteraction.PauseRetrieval){PauseFishingTrapRetrieval(s,job);return null;}
                return ResumeFishingTrapRetrieval(s,c,job);
            }
            if(c.Inventory!=null)return "InvalidFishingTrapInteraction";
            if(operation==FishingTrapInteraction.Abandon&&fishingTrapResponsibilityHandoverEnabled) {
                var responsible=CurrentFishingTrap(s,c.Actor);
                if(responsible==null||responsible.TrapId!=profile.TrapIdentity)return "FishingTrapResponsibleHolderRequired";
            } else if(c.Actor!=profile.SetterId)return "FishingTrapSetterRequired";
            var current=CurrentFishingTrap(s,c.Actor);
            if(operation==FishingTrapInteraction.Set) {
                if(current!=null)return "FishingTrapDeploymentOccupied";
                if(s.FishingTrapAttempts.Length>=FishingTrapValidation.MaxAttempts)return "FishingTrapHistoryCapacityReached";
                if(!fishingTrapLegacy&&(s.Work.Lots.All(x=>x.Id!=profile.BaitLotIdentity)
                    ||s.Work.AvailableAmount(profile.BaitLotIdentity)<new RuleQuantity(1)))return "FishingTrapBaitUnavailable";
                if(!FishingTrapWorkerCanContinue(s,c.Actor))return "FishingTrapSetterUnavailable";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                if(PhysicalFishingEnabled) {
                    var physical=s.FishingTraps.SingleOrDefault(x=>x.TrapId==profile.TrapIdentity);
                    var opportunity=s.FishingOpportunities.SingleOrDefault(x=>x.Id==profile.OpportunityIdentity);
                    var creature=s.FishingCreatures.SingleOrDefault(x=>x.Id==profile.CreatureIdentity);
                    if(physical==null||physical.Status!=FishingTrapPhysicalStatus.Staged)return "FishingTrapBodyUnavailable";
                    if(opportunity==null||opportunity.Status!=FishingOpportunityStatus.Available)return "FishingOpportunityUnavailable";
                    if(creature==null||creature.SiteId!=physical.SiteId||creature.ContainerId!=""
                        ||creature.ActiveResponseAttemptId!=""||creature.LifeState!=FishingCreatureLifeState.Alive
                        ||creature.MassPounds>new RuleQuantity(physical.CatchCapacityPounds)||creature.VolumeCubicFeet>physical.CatchCapacityCubicFeet)
                        return "FishingCandidateUnavailable";
                    var trapBody=s.Structures.SingleOrDefault(x=>x.Id==physical.TrapId);
                    var support=s.Structures.SingleOrDefault(x=>x.Id==physical.SupportId);
                    if(trapBody==null||support==null||trapBody.Broken||support.Broken)return "FishingTrapAssemblyUnavailable";
                    if(!FishingAccessFrom(s,c.Actor,physical.X,physical.Y))return "FishingTrapOutOfReach";
                }
                string id="fishing.trap."+(s.Revision+1).ToString(CultureInfo.InvariantCulture);
                var interval=new WorkerInterval(id+".setup."+(s.Revision+1).ToString(CultureInfo.InvariantCulture),id,c.Actor,s.RuleClock,s.RuleClock.AddSeconds(300));
                string baitReservation=fishingTrapLegacy?"":id+".bait";
                var baitClaims=fishingTrapLegacy?Array.Empty<ResourceReservation>():new[]{new ResourceReservation(baitReservation,id,
                    profile.BaitLotIdentity,1)};
                s.Work=s.Work.Reserve(id,new[]{interval},baitClaims);
                string opportunityId=PhysicalFishingEnabled?profile.OpportunityIdentity:SharedFishingTrapFixture.OpportunityId;
                string creatureId=PhysicalFishingEnabled?s.FishingOpportunities.Single(x=>x.Id==opportunityId).CandidateCreatureId:SharedFishingTrapFixture.CreatureId;
                string siteId=PhysicalFishingEnabled?profile.SiteIdentity:SharedFishingTrapFixture.SiteId;
                if(PhysicalFishingEnabled) {
                    var opportunity=s.FishingOpportunities.Single(x=>x.Id==opportunityId);
                    PutFishingOpportunity(s,opportunity.Reserve(id,s.RuleClock));
                    PutFishingPhysical(s,s.FishingTraps.Single(x=>x.TrapId==profile.TrapIdentity).WithStatus(FishingTrapPhysicalStatus.Reserved,id));
                }
                s.FishingTrapAttempts=s.FishingTrapAttempts.Concat(new[]{new FishingTrapAttemptRecord(id,c.Actor,c.Actor,
                    profile.TrapIdentity,opportunityId,creatureId,"",siteId,s.RuleClock,default, null,fishingTrapLegacy?(RuleTime?)null:s.RuleClock.AddSeconds(3300),null,null,FishingTrapAttemptStatus.SettingUp,false,
                    0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,
                    fishingTrapLegacy?"":profile.BaitLotIdentity,baitReservation,null)}).ToArray();
                return null;
            }
            if(current==null||current.TrapId!=profile.TrapIdentity)return "FishingTrapDeploymentUnavailable";
            if(operation==FishingTrapInteraction.Pause) {
                if(current.Status!=FishingTrapAttemptStatus.SettingUp)return "FishingTrapNotSettingUp";
                s.Work=s.Work.CancelFutureWork(current.Id,s.RuleClock);
                PutFishingTrap(s,new FishingTrapAttemptRecord(current.Id,current.SetterId,current.ResponsibleHolderId,current.TrapId,
                    current.OpportunityId,current.CreatureId,"",current.SiteId,current.StartedAt,current.SetupLabor,null,current.CheckDueAt,null,null,
                    FishingTrapAttemptStatus.Paused,false,0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,
                    FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,current.BaitLotId,current.BaitReservationId,null));return null;
            }
            if(operation==FishingTrapInteraction.Resume) {
                if(current.Status!=FishingTrapAttemptStatus.Paused)return "FishingTrapNotPaused";
                if(!FishingTrapWorkerCanContinue(s,c.Actor))return "FishingTrapSetterUnavailable";
                if(OrdinaryInventory.Busy(s,c.Actor))return "WorkerBusy";
                if(!FishingSetupResumeInReach(s,c,profile))return "FishingTrapOutOfReach";
                RuleTime remaining=RuleTime.FromFraction((System.Numerics.BigInteger)300*current.SetupLabor.Denominator-current.SetupLabor.Numerator,
                    current.SetupLabor.Denominator);
                var interval=new WorkerInterval(current.Id+".setup."+(s.Revision+1).ToString(CultureInfo.InvariantCulture),current.Id,c.Actor,
                    s.RuleClock,AddTime(s.RuleClock,remaining));
                s.Work=s.Work.Reserve(current.Id,new[]{interval},Array.Empty<ResourceReservation>());
                PutFishingTrap(s,new FishingTrapAttemptRecord(current.Id,current.SetterId,current.ResponsibleHolderId,current.TrapId,
                    current.OpportunityId,current.CreatureId,"",current.SiteId,current.StartedAt,current.SetupLabor,null,current.CheckDueAt,null,null,
                    FishingTrapAttemptStatus.SettingUp,false,0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,
                    FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,current.BaitLotId,current.BaitReservationId,null));return null;
            }
            if(operation==FishingTrapInteraction.Cancel) {
                if(current.Status!=FishingTrapAttemptStatus.SettingUp&&current.Status!=FishingTrapAttemptStatus.Paused)return "FishingTrapAlreadyCommitted";
                s.Work=s.Work.CancelFutureWork(current.Id,s.RuleClock);
                if(!fishingTrapLegacy)s.Work=s.Work.Release(current.Id,current.BaitReservationId);
                if(PhysicalFishingEnabled) {
                    var opportunity=s.FishingOpportunities.Single(x=>x.Id==current.OpportunityId);
                    PutFishingOpportunity(s,opportunity.Release(s.RuleClock));
                    PutFishingPhysical(s,s.FishingTraps.Single(x=>x.TrapId==current.TrapId).WithStatus(FishingTrapPhysicalStatus.Staged,""));
                }
                PutFishingTrap(s,new FishingTrapAttemptRecord(current.Id,current.SetterId,current.ResponsibleHolderId,current.TrapId,
                    current.OpportunityId,current.CreatureId,"",current.SiteId,current.StartedAt,current.SetupLabor,null,current.CheckDueAt,null,null,
                    FishingTrapAttemptStatus.Cancelled,false,0,0,0,FishingTrapDiceSelection.None,0,0,0,0,0,
                    FishingTrapCheckDegree.None,FishingTrapCheckOutcome.None,0,0,0,current.BaitLotId,current.BaitReservationId,null));return null;
            }
            if(operation==FishingTrapInteraction.Abandon) {
                if(PhysicalFishingEnabled&&!current.OpportunityCommitted)return "FishingTrapNotCommitted";
                if(current.Status==FishingTrapAttemptStatus.SettingUp)s.Work=s.Work.CancelFutureWork(current.Id,s.RuleClock);
                if(!fishingTrapLegacy&&!current.BaitExposedAt.HasValue)s.Work=s.Work.Release(current.Id,current.BaitReservationId);
                if(PhysicalFishingEnabled) {
                    foreach(var job in s.FishingTrapRetrievals.Where(x=>x.AttemptId==current.Id&&x.Status==FishingTrapRetrievalStatus.Working).ToArray()) {
                        s.Work=s.Work.CancelFutureWork(job.Id,s.RuleClock);
                        PutFishingRetrieval(s,job.WithPaused(s.RuleClock));
                    }
                    var creature=s.FishingCreatures.Single(x=>x.Id==current.CreatureId);
                    if(creature.ActiveResponseAttemptId==current.Id)PutFishingCreature(s,creature.Release(current.Id));
                    PutFishingPhysical(s,s.FishingTraps.Single(x=>x.TrapId==current.TrapId).WithStatus(FishingTrapPhysicalStatus.Abandoned,current.Id));
                }
                PutFishingTrap(s,new FishingTrapAttemptRecord(current.Id,current.SetterId,current.ResponsibleHolderId,current.TrapId,
                    current.OpportunityId,current.CreatureId,current.CapturedCreatureId,current.SiteId,current.StartedAt,current.SetupLabor,
                    current.SetupCompletedAt,current.CheckDueAt,current.CheckResolvedAt,s.RuleClock,FishingTrapAttemptStatus.Abandoned,
                    current.OpportunityCommitted,current.WisdomModifier,current.ProficiencyRank,current.ProficiencyBonus,current.DiceSelection,
                    current.FirstDie,current.SecondDie,current.Natural,current.CheckModifier,current.CheckDc,current.CheckDegree,
                    current.CheckOutcome,current.RandomBefore,current.RandomAfter,current.WordsConsumed,current.BaitLotId,
                    current.BaitReservationId,current.BaitExposedAt));return null;
            }
            return "InvalidFishingTrapInteraction";
        }
        private string ResolveFishingTrapResponsibilityHandover(Snapshot s,Command c)
        {
            string failure=AssessFishingTrapResponsibilityHandover(s,c);
            if(failure!=null)return failure;
            var attempt=FishingTrapObligations(s,c.Actor).Single();
            PutFishingTrap(s,attempt.WithResponsibleHolder(c.Target));
            return null;
        }
    }
}
#endif
