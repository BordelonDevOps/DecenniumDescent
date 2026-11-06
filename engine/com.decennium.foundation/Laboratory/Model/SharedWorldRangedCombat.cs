#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>One explicit numerical shooter and authored planar sight lane for the schema22
    /// Repeating heavy crossbow profile. Training, visibility, cover and line of fire are supplied
    /// facts; this fixture does not claim a complete Soldier build or general ranged geometry.</summary>
    public sealed class RepeatingCrossbowFixture
    {
        public const string WeaponId="TEST_ONLY.actor-repeating-crossbow";
        public const string AmmunitionId="TEST_ONLY.actor-crossbow-bolts";
        public const string TrainingId="TEST_ONLY.soldier-martial-ranged-training";
        public string ShooterId { get; }
        public string TargetId { get; }
        public int ShooterX { get; }
        public int ShooterY { get; }
        public int TargetX { get; }
        public int TargetY { get; }
        public bool TargetLocationKnown { get; }
        public bool TargetVisible { get; }
        public bool LineOfFireClear { get; }
        public CombatCover TargetCover { get; }
        public bool Proficient { get; }
        public string ProficiencySource { get; }
        public RepeatingCrossbowFixture(bool targetLocationKnown=true,bool targetVisible=true,bool lineOfFireClear=true,
            CombatCover targetCover=CombatCover.None,bool proficient=true,bool shooterIsAdditional=false)
        {
            ShooterId=shooterIsAdditional?AdditionalTacticalActor.Id:TestOnlyPolicy.ActorId;
            TargetId=shooterIsAdditional?TestOnlyPolicy.ActorId:AdditionalTacticalActor.Id;
            ShooterX=shooterIsAdditional?4:0;ShooterY=0;TargetX=shooterIsAdditional?0:4;TargetY=0;
            if(!Enum.IsDefined(typeof(CombatCover),targetCover))throw new ArgumentException("Unknown authored crossbow cover.");
            TargetLocationKnown=targetLocationKnown;TargetVisible=targetVisible;LineOfFireClear=lineOfFireClear;TargetCover=targetCover;
            Proficient=proficient;ProficiencySource=proficient?TrainingId:"";
        }
        internal string Key=>"repeating-crossbow-schema22-v1|new.repeating-heavy-crossbow:20lb:80/320:1d10-piercing:two-hands:repeating5|"
            +ShooterId+"|"+TargetId+"|lane="+ShooterX+","+ShooterY+">"+TargetX+","+TargetY+"|known="+TargetLocationKnown+"|visible="+TargetVisible
            +"|clear="+LineOfFireClear+"|cover="+(int)TargetCover+"|dex10|pb2|proficient="+Proficient+"|training="+ProficiencySource
            +"|kit=twenty-bolts-one-bundle-empty-magazine|combat-source=46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        internal static string BindFingerprint(string prior,RepeatingCrossbowFixture facts)
        {
            using(var sha=SHA256.Create())return "TEST_ONLY.repeating-crossbow-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior+"|"+facts.Key))
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy : ICommandQueryPolicy
    {
        private RepeatingCrossbowFixture rangedCombat;
        private sealed class RepeatingCrossbowAssessment
        {
            public bool Attack;
            public int Amount;
            public RepeatingCrossbowRecord Weapon;
            public AmmunitionLotRecord AmmoLot;
            public WorldIntervalRecord Interval;
            public RangedAttackRequest AttackFacts;
            public int CarriedBolts;
            public CommandKind Technique;
        }
        private sealed class SuppressionFireAssessment
        {
            public WorldIntervalRecord Interval;
            public RepeatingCrossbowRecord Weapon;
            public string[] AmmunitionLots;
            public string[] TargetIds;
            public int ClassLevel;
            public int SaveDc;
        }

        public bool SupportsCommand(CommandKind kind)=>kind==CommandKind.AttackRepeatingCrossbow||kind==CommandKind.ReloadRepeatingCrossbow
            ||kind==CommandKind.DoffPortableShield||kind==CommandKind.WarningShot||kind==CommandKind.CoveringFire
            ||kind==CommandKind.TacticalAssessment||kind==CommandKind.OfferCommandStep||kind==CommandKind.RespondCommandStep
            ||kind==CommandKind.SuppressionFire||kind==CommandKind.ActivateDefensiveFormation||kind==CommandKind.RespondDefensiveFormation
            ||kind==CommandKind.BeginWorldStep||kind==CommandKind.SuspendWorldStep||kind==CommandKind.ResumeWorldStep
            ||kind==CommandKind.StartToolRepair||kind==CommandKind.PauseToolRepair
            ||kind==CommandKind.ResumeToolRepair||kind==CommandKind.CancelToolRepair
            ||kind==CommandKind.StartHarvest||kind==CommandKind.PauseHarvest||kind==CommandKind.ResumeHarvest
            ||kind==CommandKind.StartMining||kind==CommandKind.PauseMining||kind==CommandKind.ResumeMining
            ||kind==CommandKind.StartProspecting||kind==CommandKind.PauseProspecting||kind==CommandKind.ResumeProspecting
            ||kind==CommandKind.RecordProspectingExposure
            ||kind==CommandKind.StartMiningAssay||kind==CommandKind.PauseMiningAssay||kind==CommandKind.ResumeMiningAssay
            ||kind==CommandKind.CancelMiningAssay
            ||kind==CommandKind.StartMineralPreparation||kind==CommandKind.PauseMineralPreparation||kind==CommandKind.ResumeMineralPreparation
            ||kind==CommandKind.TacticalStep||kind==CommandKind.TacticalRepositionStep||kind==CommandKind.Interact
            ||kind==CommandKind.ResolveManufacturingQuality||kind==CommandKind.PauseManufacturing
            ||kind==CommandKind.ResumeManufacturing||kind==CommandKind.CancelManufacturing;

        public IEnumerable<Command> DiscoverCommands(Snapshot s,Authority authority,string actor)
        {
            if(s==null||authority==null||!authority.Controls(actor)||!Validation.ValidId(actor))return Array.Empty<Command>();
            if(s.Encounter==null||!s.InventoryCombat)return DiscoverSharedWorldCommands(s,authority,actor);
            var options=new System.Collections.Generic.List<Command>();
            int optionIndex=0;
            options.AddRange(DiscoverManufacturingCommands(s,actor));
            if(PendingDefensiveFormationShift(s)!=null) {
                options.AddRange(DiscoverDefensiveFormationCommands(s,actor));return options;
            }
            var pendingStep=PendingCommandStepOffer(s);
            if(pendingStep!=null) {
                if(actor!=pendingStep.AllyActorId)return options;
                var decline=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".commandstep.decline",actor,s.Revision,
                    CommandKind.RespondCommandStep,pendingStep.Id,combat:new CombatRequest(s.Encounter.CurrentTurnId,choice:false));
                if(AssessCommandStepResponse(s,decline,out _) == null)options.Add(decline);
                var body=s.Actors.Single(x=>x.Id==actor);
                foreach(var delta in new[]{new[]{-1,-1},new[]{-1,0},new[]{-1,1},new[]{0,-1},new[]{0,1},new[]{1,-1},new[]{1,0},new[]{1,1}}) {
                    var response=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".commandstep.move."+(optionIndex++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.RespondCommandStep,pendingStep.Id,body.X+delta[0],body.Y+delta[1],
                        combat:new CombatRequest(s.Encounter.CurrentTurnId,choice:true));
                    if(AssessCommandStepResponse(s,response,out _) == null)options.Add(response);
                }
                return options;
            }
            options.AddRange(DiscoverDefensiveFormationCommands(s,actor));
            if(actor!=s.Encounter.CurrentActor)return options;
            string turnId=s.Encounter.CurrentTurnId;
            options.AddRange(DiscoverContextualInteractions(s,authority,actor));
            options.AddRange(DiscoverTacticalMovementCommands(s,actor));
            if(s.SchemaVersion>=Snapshot.CommandStepSchema&&s.CharacterFeatureGrants.Any(x=>x.ActorId==actor
                &&x.FeatureId==CharacterFeatureIds.CommandStep&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard)
                &&TestOnlyClubAttackPolicy.ActionSpent(s)) {
                string actionId=s.Receipts.OrderByDescending(x=>x.Revision)
                    .Select(x=>CommandStepActionReceipt(s,x.Id,actor,s.Encounter.TurnOrdinal,turnId)==null?"":x.Id)
                    .FirstOrDefault(x=>x!="")??"";
                if(actionId!="")foreach(var ally in s.TacticalAllies.Where(x=>x.Includes(actor)).Select(x=>x.Other(actor)).OrderBy(x=>x,StringComparer.Ordinal)) {
                    var offer=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".commandstep.offer."+(optionIndex++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.OfferCommandStep,ally,combat:new CombatRequest(turnId,actionId));
                    if(AssessCommandStepOffer(s,offer,out _) == null)options.Add(offer);
                }
            }
            if(s.SchemaVersion>=Snapshot.SoldierInitialBuildSchema) {
                var build=s.InitialCharacterLoadouts.SingleOrDefault(x=>x.ActorId==actor);
                if(build!=null) {
                    var doff=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".ranged."+(optionIndex++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.DoffPortableShield,build.ShieldId);
                    if(AssessPortableShieldDoff(s,doff,out var shield,out var doffCrossbow)==null
                        &&authority.MayUseInventory(shield.OwnerId)&&authority.MayUseInventory(doffCrossbow.OwnerId))options.Add(doff);
                }
            }
            if(rangedCombat==null||s.SchemaVersion<Snapshot.RepeatingCrossbowSchema||actor!=rangedCombat.ShooterId)return options;
            if(s.SchemaVersion>=Snapshot.TacticalAssessmentSchema
                &&s.CharacterFeatureGrants.Any(x=>x.ActorId==actor&&x.FeatureId==CharacterFeatureIds.TacticalAssessment
                    &&x.Origin==CharacterFeatureGrantOrigin.SelectedCard)) {
                var assessmentTurnId=s.Encounter.CurrentTurnId;
                foreach(var ally in s.TacticalAllies.Where(x=>x.Includes(actor)).Select(x=>x.Other(actor)).OrderBy(x=>x,StringComparer.Ordinal)) {
                    var assessment=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".assessment."+(optionIndex++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.TacticalAssessment,rangedCombat.TargetId,
                        combat:new CombatRequest(assessmentTurnId,ally));
                    if(AssessTacticalAssessment(s,assessment,out _) == null)options.Add(assessment);
                }
            }
            var weapon=s.RepeatingCrossbows.SingleOrDefault(x=>x.Id==RepeatingCrossbowFixture.WeaponId);
            if(weapon==null||weapon.OwnerId!=actor||weapon.CustodianId!=actor||weapon.HeldBy!=actor
                ||!authority.MayUseInventory(weapon.OwnerId)||!s.Lives.Single(x=>x.ActorId==actor).HeldItems.Contains(weapon.Id))
                return options;

            var ammo=s.AmmunitionLots.SingleOrDefault(x=>x.Id==RepeatingCrossbowFixture.AmmunitionId);
            if(ammo!=null&&ammo.CustodianId==actor&&ammo.OwnerId==actor&&ammo.Accessible&&authority.MayUseInventory(ammo.OwnerId)) {
                int reloadMaximum=Math.Min(5-weapon.LoadedBoltLots.Count,ammo.AvailableQuantity);
                for(int amount=1;amount<=reloadMaximum;amount++) {
                    var request=new RangedRequest(turnId,weapon.Id,ammo.Id,amount);
                    options.Add(new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".ranged."+(optionIndex++).ToString(CultureInfo.InvariantCulture),
                        actor,s.Revision,CommandKind.ReloadRepeatingCrossbow,ranged:request));
                }
            }
            if(rangedCombat.TargetLocationKnown) {
                var request=new RangedRequest(turnId,weapon.Id,"",0);
                options.Add(new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".ranged."+optionIndex.ToString(CultureInfo.InvariantCulture),
                    actor,s.Revision,CommandKind.AttackRepeatingCrossbow,rangedCombat.TargetId,ranged:request));
                if(s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema) {
                    foreach(var technique in new[]{CommandKind.WarningShot,CommandKind.CoveringFire})
                        if(s.CharacterFeatureGrants.Any(x=>x.ActorId==actor&&x.FeatureId==SoldierTacticalFeatures.Technique(technique)))
                            options.Add(new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".ranged."+(++optionIndex).ToString(CultureInfo.InvariantCulture),
                                actor,s.Revision,technique,rangedCombat.TargetId,ranged:request));
                }
                if(s.SchemaVersion>=Snapshot.SuppressionFireSchema&&s.CharacterFeatureGrants.Any(x=>x.ActorId==actor
                    &&x.FeatureId==CharacterFeatureIds.SuppressionFire&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard)) {
                    var targets=new[]{rangedCombat.TargetId}.Where(id=>s.WorldSchedule.Order.Contains(id)).ToArray();
                    if(targets.Length!=0) {
                        var suppressionRequest=new SuppressionFireRequest(turnId,weapon.Id,targets);
                        var command=new Command("option."+s.Revision.ToString(CultureInfo.InvariantCulture)+".suppression."+(optionIndex++).ToString(CultureInfo.InvariantCulture),
                            actor,s.Revision,CommandKind.SuppressionFire,x:rangedCombat.TargetX,y:rangedCombat.TargetY,suppressionFire:suppressionRequest);
                        if(AssessSuppressionFire(s,command,out _) == null)options.Add(command);
                    }
                }
            }
            return options;
        }

        public CommandQueryResult QueryCommand(Snapshot s,Authority authority,Command c)
        {
            var sharedWorld=QuerySharedWorldCommand(s,authority,c);
            if(sharedWorld!=null)return sharedWorld;
            if(c.Kind==CommandKind.ActivateDefensiveFormation||c.Kind==CommandKind.RespondDefensiveFormation)
                return QueryDefensiveFormation(s,c);
            if(c.Kind==CommandKind.OfferCommandStep) {
                string offerFailure=AssessCommandStepOffer(s,c,out _);
                return new CommandQueryResult(true,offerFailure==null,offerFailure??"Available",s.Revision,Array.Empty<CommandCost>());
            }
            if(c.Kind==CommandKind.RespondCommandStep) {
                string responseFailure=AssessCommandStepResponse(s,c,out _);
                return new CommandQueryResult(true,responseFailure==null,responseFailure??"Available",s.Revision,Array.Empty<CommandCost>());
            }
            if(c.Kind==CommandKind.TacticalAssessment) {
                string assessmentFailure=AssessTacticalAssessment(s,c,out _);
                var assessmentCosts=assessmentFailure==null?new[]{new CommandCost("bonus-action","",1)}:Array.Empty<CommandCost>();
                return new CommandQueryResult(true,assessmentFailure==null,assessmentFailure??"Available",s.Revision,assessmentCosts);
            }
            if(c.Kind==CommandKind.SuppressionFire) {
                string suppressionFailure=AssessSuppressionFire(s,c,out var facts);
                var suppressionCosts=new System.Collections.Generic.List<CommandCost>();
                if(suppressionFailure==null) {
                    suppressionCosts.Add(new CommandCost("action","",1));
                    foreach(var group in facts.AmmunitionLots.GroupBy(x=>x,StringComparer.Ordinal).OrderBy(x=>x.Key,StringComparer.Ordinal))
                        suppressionCosts.Add(new CommandCost("ammunition",group.Key,group.Count()));
                }
                return new CommandQueryResult(true,suppressionFailure==null,suppressionFailure??"Available",s.Revision,suppressionCosts);
            }
            if(c.Kind==CommandKind.DoffPortableShield) {
                string doffFailure=AssessPortableShieldDoff(s,c,out _,out _);
                var doffCosts=doffFailure==null?new[]{new CommandCost("action","",1)}:Array.Empty<CommandCost>();
                return new CommandQueryResult(true,doffFailure==null,doffFailure??"Available",s.Revision,doffCosts);
            }
            string failure=AssessRepeatingCrossbow(s,c,out var assessment);
            var costs=new System.Collections.Generic.List<CommandCost>();
            if(failure==null) {
                costs.Add(new CommandCost("action","",1));
                long bolts=c.Kind==CommandKind.ReloadRepeatingCrossbow?c.Ranged.Amount:1;
                string resource=c.Kind==CommandKind.ReloadRepeatingCrossbow?c.Ranged.AmmoLotId:c.Ranged.WeaponId;
                if(c.Kind==CommandKind.WarningShot||c.Kind==CommandKind.CoveringFire)resource=assessment.Weapon.LoadedBoltLots[0];
                costs.Add(new CommandCost("ammunition",resource,bolts));
            }
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,costs);
        }

        private sealed class TacticalAssessmentFacts
        {
            public string AllyId;
            public string ArmorCategory;
            public bool HasCover;
        }

        private string AssessTacticalAssessment(Snapshot s,Command c,out TacticalAssessmentFacts facts)
        {
            facts=null;
            if(rangedCombat==null||s.SchemaVersion<Snapshot.TacticalAssessmentSchema)return "TacticalAssessmentNotImplemented";
            if(c.Inventory!=null||c.Advancement!=null||c.Ranged!=null||c.Combat==null||c.X!=0||c.Y!=0
                ||c.Combat.Stance!=0||c.Combat.Choice||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome
                ||c.Combat.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidTacticalAssessmentRequest";
            if(!s.InventoryCombat||s.Encounter==null)return "TacticalAssessmentRequiresEncounter";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||c.Combat.TurnId!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
            if(c.Actor!=rangedCombat.ShooterId||c.Target!=rangedCombat.TargetId)return "AssessmentObservationUnavailable";
            if(!s.WorldSchedule.Order.Contains(c.Target)||SoldierTacticalFeatures.IsAlly(s,c.Actor,c.Target))return "TargetMustBeEnemy";
            if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor&&x.FeatureId==CharacterFeatureIds.TacticalAssessment
                &&x.ClassName=="Soldier"&&x.ClassLevel==3&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard))return "FeatureNotOwned";
            var runtime=s.CharacterFeatureRuntime.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(runtime==null)return "FeatureRuntimeUnavailable";
            if(runtime.TacticalAssessmentRechargeRemaining>0)return "TacticalAssessmentRecharging";
            if(!CharacterAdvancementRules.BonusActionAvailable(s,c.Actor))return "BonusActionUnavailable";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).BonusAction)return "ConditionPreventsBonusAction";
            var ally=s.TacticalAllies.Where(x=>x.Includes(c.Actor)).Select(x=>x.Other(c.Actor)).SingleOrDefault(x=>x==c.Combat.WeaponId);
            if(ally==null||ally==c.Actor||!s.WorldSchedule.Order.Contains(ally))return "InvalidAssessmentAlly";
            bool visible=rangedCombat.TargetVisible&&TestOnlyClubAttackPolicy.CanSee(s,c.Actor,c.Target);
            if(!visible)return "TacticalAssessmentRequiresVisibleEnemy";
            var shooter=s.Actors.Single(a=>a.Id==c.Actor);var target=s.Actors.Single(a=>a.Id==c.Target);
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(target.X,target.Y))>60)
                return "TacticalAssessmentOutOfRange";
            if(s.TacticalAssessments.Length>=SoldierTacticalFeatureValidation.MaxAssessments)return "TacticalAssessmentHistoryCapacityReached";
            var armor=s.PortableEquipment.Where(x=>x.CustodianId==c.Target&&x.ParentId==""&&x.Placement==PortablePlacement.Worn
                &&x.ProfileId.StartsWith("armor-and-shields.",StringComparison.Ordinal)&&x.ProfileId!="armor-and-shields.shield").ToArray();
            string category;
            if(armor.Length==0)category="unarmored";
            else if(armor.Length==1&&armor[0].ProfileId=="armor-and-shields.chain-mail")category="heavy";
            else return "AssessmentArmorCategoryUnbound";
            facts=new TacticalAssessmentFacts{AllyId=ally,ArmorCategory=category,HasCover=rangedCombat.TargetCover!=CombatCover.None};
            return null;
        }

        private string AssessSuppressionFire(Snapshot s,Command c,out SuppressionFireAssessment facts)
        {
            facts=null;
            if(rangedCombat==null||s.SchemaVersion<Snapshot.SuppressionFireSchema)return "SuppressionFireNotImplemented";
            var request=c.SuppressionFire;
            if(request==null||c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null||c.Target!=""
                ||c.OverwatchRider!=OverwatchRider.None||request.WeaponId!=RepeatingCrossbowFixture.WeaponId)
                return "InvalidSuppressionFireRequest";
            if(!s.InventoryCombat||s.Encounter==null)return "RangedCombatRequiresEncounter";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||request.TurnId!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
            var interval=Interval(s,c.Actor);
            if(interval.ActionSpent)return "ActionAlreadySpent";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(!TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
            var grants=s.CharacterFeatureGrants.Where(x=>x.ActorId==c.Actor&&x.FeatureId==CharacterFeatureIds.SuppressionFire
                &&x.ClassName=="Soldier"&&x.ClassLevel==3&&x.Origin==CharacterFeatureGrantOrigin.SelectedCard).ToArray();
            if(grants.Length!=1)return "FeatureNotOwned";
            var runtime=s.CharacterFeatureRuntime.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(runtime==null)return "FeatureRuntimeUnavailable";
            if(runtime.SuppressionFireRechargeRemaining>0)return "SuppressionFireRecharging";
            if(s.RepeatingCrossbows.Length!=1)return "CrossbowUnavailable";
            var weapon=s.RepeatingCrossbows.Single();
            if(weapon.Id!=RepeatingCrossbowFixture.WeaponId||weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor
                ||!s.Lives.Single(x=>x.ActorId==c.Actor).HeldItems.Contains(weapon.Id))return "CrossbowNotHeld";
            if(weapon.LoadedBoltLots.Count<3)return "InsufficientLoadedBolts";
            if(RepeatingCrossbowAttackHands(s,c.Actor,weapon)<2)return "TwoHandsRequired";
            string physicalFailure=TestOnlyClubAttackPolicy.PhysicalAttackFailure(s,c.Actor);if(physicalFailure!=null)return physicalFailure;
            if(s.SuppressionFireVolleys.Length>=SoldierTacticalFeatureValidation.MaxSuppressionVolleys)return "SuppressionFireHistoryCapacityReached";
            if(c.X!=rangedCombat.TargetX||c.Y!=rangedCombat.TargetY)return "SuppressionZoneOutsideAuthoredFixture";
            var shooter=s.Actors.Single(a=>a.Id==c.Actor);
            long range=PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(c.X,c.Y));
            if(range>RepeatingCrossbowShotRules.MaximumRangeFeet)return "SuppressionZoneOutOfRange";
            bool zoneLocationKnown=rangedCombat.TargetLocationKnown
                &&(s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.LocationKnown(s,c.Actor,rangedCombat.TargetId));
            bool zoneLineClear=rangedCombat.LineOfFireClear
                &&(s.SchemaVersion<Snapshot.ObservationSchema||ObservationGeometry.LineOfEffectClear(s,c.Actor,rangedCombat.TargetId));
            if(!zoneLocationKnown||!rangedCombat.TargetVisible||!zoneLineClear
                ||!TestOnlyClubAttackPolicy.CanSee(s,c.Actor,rangedCombat.TargetId))return "SuppressionZoneNotPerceived";
            var targetIds=request.TargetIds;
            if(targetIds.Length<1||targetIds.Length>3)return "SuppressionFireTargetCountInvalid";
            foreach(string targetId in targetIds) {
                if(targetId!=rangedCombat.TargetId||!s.WorldSchedule.Order.Contains(targetId)||SoldierTacticalFeatures.IsAlly(s,c.Actor,targetId))
                    return "SuppressionTargetOutsideAuthoredFixture";
                var target=s.Actors.Single(a=>a.Id==targetId);var targetLife=s.Lives.Single(l=>l.ActorId==targetId);
                if(targetLife.Dead)return "InvalidLivingTarget";
                if(Math.Abs((long)target.X-c.X)>1||Math.Abs((long)target.Y-c.Y)>1)return "SuppressionTargetOutsideZone";
                if(rangedCombat.TargetCover==CombatCover.Total)return "SuppressionTargetHasTotalCover";
                if(!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,targetId))return "ConditionHistoryCapacityReached";
            }
            var character=s.Characters.Single(x=>x.ActorId==c.Actor);
            int level=grants[0].ClassLevel;
            int dc=checked(8+PlaytestCharacters.ProficiencyBonus(character.Levels.Count)+PlaytestCharacters.AbilityModifier(character.Abilities[2]));
            facts=new SuppressionFireAssessment{Interval=interval,Weapon=weapon,AmmunitionLots=weapon.LoadedBoltLots.Take(3).ToArray(),
                TargetIds=targetIds,ClassLevel=level,SaveDc=dc};
            return null;
        }

        private string ResolveSuppressionFire(Snapshot s,Command c)
        {
            string failure=AssessSuppressionFire(s,c,out var facts);if(failure!=null)return failure;
            var weapon=facts.Weapon;
            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id?x.WithMagazine(x.LoadedBoltLots.Skip(3).ToArray()):x).ToArray();
            uint damageBefore=s.RandomState,damageState=damageBefore;long damageWords=0;var dice=new int[facts.ClassLevel];
            for(int i=0;i<dice.Length;i++){var draw=DiceStream.Draw(damageState,6);dice[i]=draw.Value+1;damageState=draw.NextState;damageWords=checked(damageWords+draw.WordsConsumed);}
            long sharedDamage=dice.Sum(x=>(long)x);s.RandomState=damageState;
            long expiry=SoldierTacticalFeatures.NextFutureStartSlot(s,c.Actor);
            var results=new System.Collections.Generic.List<SuppressionFireTargetResult>();var slows=new System.Collections.Generic.List<SuppressionSlowRecord>();
            int slowIndex=0;
            foreach(string targetId in facts.TargetIds.OrderBy(x=>x,StringComparer.Ordinal)) {
                var actor=s.Actors.Single(x=>x.Id==targetId);var life=s.Lives.Single(x=>x.ActorId==targetId);
                var character=s.Characters.Single(x=>x.ActorId==targetId);
                int modifier=checked(PlaytestCharacters.AbilityModifier(character.Abilities[1])+CharacterAdvancementRules.SaveProficiencyBonus(s,targetId,"DEX"));
                uint saveBefore=s.RandomState,saveAfter=saveBefore;long saveWords=0;int natural=0;long total=0;bool success=false;
                bool automaticFailure=life.Hp==0||life.Dead||TestOnlyClubAttackPolicy.ConditionsFor(s,targetId).View().AutomaticStrengthDexterityFailure;
                if(!automaticFailure) {
                    var save=PlaytestDice.RollD20(s.RandomState);natural=save.Natural;saveAfter=save.NextRandomState;saveWords=save.WordsConsumed;
                    var rolled=PlaytestRolls.SavingThrow(natural,modifier,facts.SaveDc);total=rolled.Total;success=rolled.Success;s.RandomState=saveAfter;
                }
                long targetDamage=success?sharedDamage/2:sharedDamage;
                long afterDefense=CharacterAdvancementRules.ReduceIncomingDamage(s,targetId,targetDamage);
                if(TestOnlyClubAttackPolicy.ConditionsFor(s,targetId).View().Has(ConditionKind.Petrified))
                    afterDefense=PlaytestConditions.PetrifiedDamage(afterDefense);
                uint lifeBefore=s.RandomState;
                var conCharacter=character;
                int constitutionSave=checked(PlaytestCharacters.AbilityModifier(conCharacter.Abilities[2])
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,targetId,"CON"));
                var rolledDamage=PlaytestDamageDice.Resolve(ActorLifeRules.Read(life),afterDefense,s.RuleClock,lifeBefore,
                    constitutionSaveModifier:constitutionSave,critical:false,melee:false,knockout:KnockoutInstruction.OrdinaryOutcome);
                s.RandomState=rolledDamage.NextRandomState;TestOnlyClubAttackPolicy.ApplyLife(s,life,rolledDamage.Outcome.State);
                results.Add(new SuppressionFireTargetResult(targetId,actor.X,actor.Y,natural,modifier,total,success,targetDamage,afterDefense,
                    saveBefore,saveAfter,saveWords,lifeBefore,rolledDamage.NextRandomState,rolledDamage.WordsConsumed));
                if(!success) {
                    if(s.SuppressionSlows.Length+slows.Count>=SoldierTacticalFeatureValidation.MaxSuppressionSlows)return "SuppressionSlowCapacityReached";
                    string slowId="suppression-slow."+N(s.Revision+1)+"."+N(slowIndex++);
                    slows.Add(new SuppressionSlowRecord(slowId,c.Id,c.Actor,targetId,s.Revision+1,expiry));
                }
            }
            var volley=new SuppressionFireVolleyRecord(c.Id,s.Revision+1,s.Encounter.TurnOrdinal,c.Actor,weapon.Id,facts.AmmunitionLots,
                s.RuleClock,c.X,c.Y,facts.ClassLevel,facts.SaveDc,dice,sharedDamage,damageBefore,damageState,damageWords,results.ToArray());
            s.SuppressionFireVolleys=s.SuppressionFireVolleys.Concat(new[]{volley}).ToArray();
            s.SuppressionSlows=s.SuppressionSlows.Concat(slows).ToArray();
            var runtime=s.CharacterFeatureRuntime.Single(x=>x.ActorId==c.Actor).UseSuppressionFire();
            s.CharacterFeatureRuntime=s.CharacterFeatureRuntime.Select(x=>x.ActorId==c.Actor?runtime:x).ToArray();
            SetInterval(s,facts.Interval.PayAction());return null;
        }

        private string ResolveTacticalAssessment(Snapshot s,Command c)
        {
            string failure=AssessTacticalAssessment(s,c,out var facts);if(failure!=null)return failure;
            if(!CharacterAdvancementRules.SpendBonusAction(s,c.Actor))return "BonusActionUnavailable";
            var runtime=s.CharacterFeatureRuntime.Single(x=>x.ActorId==c.Actor).UseTacticalAssessment();
            s.CharacterFeatureRuntime=s.CharacterFeatureRuntime.Select(x=>x.ActorId==c.Actor?runtime:x).ToArray();
            long expiry=SoldierTacticalFeatures.NextFutureStartSlot(s,c.Actor);
            var record=new TacticalAssessmentRecord(c.Id,c.Actor,facts.AllyId,c.Target,s.Revision+1,s.RuleClock,expiry,
                facts.ArmorCategory,facts.HasCover);
            s.TacticalAssessments=s.TacticalAssessments.Concat(new[]{record}).ToArray();
            return null;
        }

        private void InitializeRepeatingCrossbow(Snapshot s)
        {
            if(rangedCombat==null)return;
            if(s.SchemaVersion<Snapshot.RepeatingCrossbowSchema||s.Actors.All(a=>a.Id!=rangedCombat.ShooterId)
                ||s.Actors.All(a=>a.Id!=rangedCombat.TargetId)||s.Characters.Single(c=>c.ActorId==rangedCombat.ShooterId).Abilities[1]!=10)
                throw new ArgumentException("The explicit crossbow fixture does not match the selected actor roster.");
            var shooter=s.Actors.Single(a=>a.Id==rangedCombat.ShooterId);
            var target=s.Actors.Single(a=>a.Id==rangedCombat.TargetId);
            if(shooter.X!=rangedCombat.ShooterX||shooter.Y!=rangedCombat.ShooterY||target.X!=rangedCombat.TargetX||target.Y!=rangedCombat.TargetY)
                throw new ArgumentException("The authored ranged lane does not match the initial combat cells.");
            var oldWeapon=s.Clubs.Single(c=>c.HeldBy==rangedCombat.ShooterId);
            s.Clubs=s.Clubs.Select(c=>c.Id==oldWeapon.Id?new ClubInstance(c.Id,c.ProfileId,c.OwnerId,c.CustodianId,"",shooter.X,shooter.Y):c).ToArray();
            s.Lives=s.Lives.Select(l=>l.ActorId==rangedCombat.ShooterId?ActorLifeRules.Record(l.ActorId,ActorLifeRules.Read(l),l.Prone,new[]{RepeatingCrossbowFixture.WeaponId}):l).ToArray();
            var shooterCharacter=s.Characters.Single(c=>c.ActorId==rangedCombat.ShooterId);
            s.RepeatingCrossbows=new[]{new RepeatingCrossbowRecord(RepeatingCrossbowFixture.WeaponId,"new.repeating-heavy-crossbow",rangedCombat.ShooterId,
                rangedCombat.ShooterId,rangedCombat.ShooterId,2,shooter.X,shooter.Y)};
            s.AmmunitionLots=new[]{new AmmunitionLotRecord(RepeatingCrossbowFixture.AmmunitionId,"ammunition.crossbow-bolts-20",rangedCombat.ShooterId,
                rangedCombat.ShooterId,20,20,true)};
            s.RangedCombatants=new[]{new RangedCombatantRecord(rangedCombat.ShooterId,shooterCharacter.Abilities[1],PlaytestCharacters.ProficiencyBonus(shooterCharacter.Levels.Count),
                rangedCombat.Proficient,rangedCombat.ProficiencySource)};
        }

        private string AssessRepeatingCrossbow(Snapshot s,Command c,out RepeatingCrossbowAssessment assessment)
        {
            assessment=new RepeatingCrossbowAssessment{Attack=c.Kind==CommandKind.AttackRepeatingCrossbow||c.Kind==CommandKind.WarningShot||c.Kind==CommandKind.CoveringFire,
                Technique=c.Kind};
            if(rangedCombat==null||s.SchemaVersion<Snapshot.RepeatingCrossbowSchema)return "RangedCommandNotImplemented";
            if(assessment.Attack&&AttackingFromActiveOverwatchZone(s,c.Actor,c.Target))return "OverwatchAttackTriggerNotImplemented";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged==null||c.X!=0||c.Y!=0)return "InvalidRangedPayload";
            if(!s.InventoryCombat||s.Encounter==null)return "RangedCombatRequiresEncounter";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||c.Ranged.TurnId!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
            var interval=Interval(s,c.Actor);assessment.Interval=interval;
            if(interval.ActionSpent)return "ActionAlreadySpent";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.RepeatingCrossbows.Length!=1||c.Ranged.WeaponId!=RepeatingCrossbowFixture.WeaponId)return "CrossbowUnavailable";
            var weapon=s.RepeatingCrossbows.Single();assessment.Weapon=weapon;
            if(weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor||!s.Lives.Single(l=>l.ActorId==c.Actor).HeldItems.Contains(weapon.Id))return "CrossbowNotHeld";
            if(!assessment.Attack) {
                var request=c.Ranged;
                if(c.Target!=""||request.Amount<1||request.AmmoLotId=="")return "InvalidReloadRequest";
                var lot=s.AmmunitionLots.SingleOrDefault(x=>x.Id==request.AmmoLotId);
                if(lot==null||lot.CustodianId!=c.Actor||lot.OwnerId!=c.Actor||!lot.Accessible)return "AmmunitionInaccessible";
                if(weapon.LoadedBoltLots.Count==5)return "MagazineFull";
                if(request.Amount>5-weapon.LoadedBoltLots.Count)return "ReloadExceedsMagazineCapacity";
                if(request.Amount>lot.AvailableQuantity)return "InsufficientCarriedBolts";
                int available=AvailableHands(s,c.Actor)+(weapon.GripHands==2?1:0);
                if(available<1)return "LoadingHandRequired";
                assessment.Amount=request.Amount;assessment.AmmoLot=lot;
                return null;
            }

            var attackRequest=c.Ranged;
            if(c.Target==""||attackRequest.Amount!=0||attackRequest.AmmoLotId!="")return "InvalidRangedAttackRequest";
            if(c.Target!=rangedCombat.TargetId||!s.WorldSchedule.Order.Contains(c.Target))return "TargetOutsideEncounter";
            if(attackRequest.WeaponId!=weapon.Id||weapon.LoadedBoltLots.Count==0)return weapon.LoadedBoltLots.Count==0?"NoAmmunition":"CrossbowUnavailable";
            if(c.Kind==CommandKind.WarningShot||c.Kind==CommandKind.CoveringFire) {
                if(s.SchemaVersion<Snapshot.SoldierTacticalTechniquesSchema)return "TacticalFeatureNotImplemented";
                string feature=SoldierTacticalFeatures.Technique(c.Kind);
                if(!s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor&&x.FeatureId==feature
                    &&x.Origin==CharacterFeatureGrantOrigin.InitialClassSelection))return "FeatureNotOwned";
                var runtime=s.CharacterFeatureRuntime.SingleOrDefault(x=>x.ActorId==c.Actor);if(runtime==null)return "FeatureRuntimeUnavailable";
                if(c.Kind==CommandKind.WarningShot&&runtime.WarningShotRechargeRemaining>0)return "WarningShotRecharging";
                if(c.Kind==CommandKind.CoveringFire&&runtime.CoveringFireRechargeRemaining>0)return "CoveringFireRecharging";
                if(SoldierTacticalFeatures.IsAlly(s,c.Actor,c.Target))return "TargetMustBeEnemy";
            }
            if(!TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
            if(s.RangedAttacks.Length==128)return "RangedAttackHistoryCapacityReached";
            if(s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema&&s.TacticalAttackAudits.Length>=SoldierTacticalFeatureValidation.MaxAttackAudits)return "TacticalAttackAuditCapacityReached";
            var shooter=s.Actors.Single(a=>a.Id==c.Actor);var target=s.Actors.Single(a=>a.Id==c.Target);
            if(shooter.X!=rangedCombat.ShooterX||shooter.Y!=rangedCombat.ShooterY||target.X!=rangedCombat.TargetX||target.Y!=rangedCombat.TargetY)
                return "AuthoredRangedLaneRequired";
            var life=s.Lives.SingleOrDefault(l=>l.ActorId==c.Target);if(life==null||life.Dead)return "InvalidLivingTarget";
            if(!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,c.Target))return "ConditionHistoryCapacityReached";
            if(RepeatingCrossbowAttackHands(s,c.Actor,weapon)<2)return "TwoHandsRequired";
            string physicalFailure=TestOnlyClubAttackPolicy.PhysicalAttackFailure(s,c.Actor);if(physicalFailure!=null)return physicalFailure;
            var combatant=s.RangedCombatants.Single(x=>x.ActorId==c.Actor);
            var targetCombatant=s.RangedCombatants.SingleOrDefault(x=>x.ActorId==c.Target);
            int targetDex=targetCombatant?.DexterityScore??s.Characters.Single(x=>x.ActorId==c.Target).Abilities[1];
            var targetStance=TestOnlyClubAttackPolicy.ActiveStance(s,c.Target);
            int armorClass=checked(CharacterAdvancementRules.ArmorClass(s,c.Target,targetDex)
                +(targetStance?.Kind==CombatStance.Aggressive?-2:targetStance?.Kind==CombatStance.Guarded?1:0)
                +CharacterAdvancementRules.DefensivePositioningBonus(s,c.Target));
            bool targetLocationKnown=rangedCombat.TargetLocationKnown
                &&(s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.LocationKnown(s,c.Actor,c.Target));
            bool lineOfFireClear=rangedCombat.LineOfFireClear
                &&(s.SchemaVersion<Snapshot.ObservationSchema||ObservationGeometry.LineOfEffectClear(s,c.Actor,c.Target));
            bool targetVisible=rangedCombat.TargetVisible&&TestOnlyClubAttackPolicy.CanSee(s,c.Actor,c.Target);
            long distance=PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(target.X,target.Y));
            if(c.Kind==CommandKind.WarningShot&&(distance>60||!targetVisible))return "WarningShotRequiresVisibleTargetWithin60Feet";
            if(c.Kind==CommandKind.CoveringFire&&(!targetLocationKnown||!targetVisible))return "CoveringFireRequiresPerceivedTarget";
            bool attackerUnseen=!TestOnlyClubAttackPolicy.CanSee(s,c.Target,c.Actor);
            bool attackerInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,c.Target,c.Actor);
            bool targetInvisibleKnown=s.SchemaVersion<Snapshot.ObservationSchema||ObservationRules.InvisibleRevealed(s,c.Actor,c.Target);
            bool targetUnseenDisadvantage=!targetVisible&&!(s.SchemaVersion>=Snapshot.ObservationSchema&&targetInvisibleKnown
                &&ObservationRules.InvisibleIsOnlySightBlocker(s,c.Actor,c.Target));
            bool attackerUnseenAdvantage=attackerUnseen&&!(s.SchemaVersion>=Snapshot.ObservationSchema&&attackerInvisibleKnown
                &&ObservationRules.InvisibleIsOnlySightBlocker(s,c.Target,c.Actor));
            bool closeHostile=s.WorldSchedule.Order.Where(id=>id!=c.Actor&&!SoldierTacticalFeatures.IsAlly(s,c.Actor,id)).Any(id=>{
                var other=s.Actors.Single(a=>a.Id==id);var otherLife=s.Lives.Single(l=>l.ActorId==id);
                bool incapacitated=otherLife.Dead||otherLife.Hp==0||TestOnlyClubAttackPolicy.ConditionsFor(s,id).View().Clauses.Incapacitated;
                return PlanarCombatGeometry.CloseHostileDisadvantage(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(other.X,other.Y)),true,incapacitated,TestOnlyClubAttackPolicy.CanSee(s,id,c.Actor));
            });
            var attackerLife=s.Lives.Single(x=>x.ActorId==c.Actor);
            var incomingEffects=SoldierTacticalFeatures.ForAttack(s,c.Actor,c.Target);
            int flatAttack=checked((attackerLife.LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0)-incomingEffects.CoveringFirePenalty
                +incomingEffects.TacticalAssessmentBonus);
            var rangedFacts=new RangedAttackRequest(distance,
                RepeatingCrossbowShotRules.NormalRangeFeet,RepeatingCrossbowShotRules.MaximumRangeFeet,armorClass,
                PlaytestCharacters.AbilityModifier(combatant.DexterityScore),combatant.ProficiencyBonus,combatant.CrossbowProficient,flatAttack,
                rangedCombat.TargetCover,targetLocationKnown,targetVisible,lineOfFireClear,attackerUnseen,closeHostile,
                TestOnlyClubAttackPolicy.CombatConditions(s,c.Actor),TestOnlyClubAttackPolicy.CombatConditions(s,c.Target),
                attackerInvisibleLocationKnown:attackerInvisibleKnown,targetInvisibleLocationKnown:targetInvisibleKnown,
                additionalDisadvantageSources:incomingEffects.WarningShot?1:0,
                targetUnseenDisadvantage:targetUnseenDisadvantage,attackerUnseenAdvantage:attackerUnseenAdvantage);
            int carriedBolts=s.AmmunitionLots.Where(x=>x.CustodianId==c.Actor&&x.Accessible).Sum(x=>x.AvailableQuantity);
            var shotFailure=RepeatingCrossbowShotRules.CheckLegality(rangedFacts,new RepeatingFiveMagazine(weapon.LoadedBoltLots.Count),carriedBolts);
            if(shotFailure!=RepeatingCrossbowShotFailure.None)return ShotFailureCode(shotFailure);
            assessment.AttackFacts=rangedFacts;assessment.CarriedBolts=carriedBolts;
            return null;
        }

        private string ResolveRepeatingCrossbow(Snapshot s,Command c)
        {
            string failure=AssessRepeatingCrossbow(s,c,out var assessment);
            if(failure!=null)return failure;
            if(assessment.Attack)return ResolveRepeatingAttack(s,c,assessment);
            var lot=assessment.AmmoLot;var weapon=assessment.Weapon;var interval=assessment.Interval;
            s.AmmunitionLots=s.AmmunitionLots.Select(x=>x.Id==lot.Id?x.WithAvailable(x.AvailableQuantity-assessment.Amount):x).ToArray();
            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id
                ?new RepeatingCrossbowRecord(x.Id,x.ProfileId,x.OwnerId,x.CustodianId,x.HeldBy,1,x.CellX,x.CellY,x.LoadedBoltLots.Concat(Enumerable.Repeat(lot.Id,assessment.Amount)).ToArray()):x).ToArray();
            SetInterval(s,interval.PayAction());return null;
        }

        private string ResolveRepeatingAttack(Snapshot s,Command c,RepeatingCrossbowAssessment assessment)
        {
            var weapon=assessment.Weapon;var interval=assessment.Interval;
            if(weapon.LoadedBoltLots.Count>0&&weapon.GripHands==1)
                s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id?x.WithGrip(2):x).ToArray();
            weapon=s.RepeatingCrossbows.Single(x=>x.Id==weapon.Id);
            var combatant=s.RangedCombatants.Single(x=>x.ActorId==c.Actor);
            var life=s.Lives.Single(x=>x.ActorId==c.Target);
            uint randomBefore=s.RandomState;
            string attackId="ranged."+N(s.Revision+1);string technique=SoldierTacticalFeatures.Technique(c.Kind);
            string captureFailure=SoldierTacticalFeatures.CaptureAndConsume(s,attackId,c.Actor,c.Target,technique,out _);
            if(captureFailure!=null)return captureFailure;
            var shot=RepeatingCrossbowShotRules.Resolve(randomBefore,assessment.AttackFacts,new RepeatingFiveMagazine(weapon.LoadedBoltLots.Count),assessment.CarriedBolts);
            if(!shot.Legal)return ShotFailureCode(shot.Failure);
            var ammunitionLot=weapon.LoadedBoltLots[0];
            var magazine=weapon.LoadedBoltLots.Skip(1).ToArray();
            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id?x.WithMagazine(magazine):x).ToArray();
            uint effectsSeed=shot.RandomStateAfter,next=effectsSeed;int[] dice=shot.DamageDice.ToArray();long diceWords=shot.RandomWordsConsumed-shot.Attack.Roll.WordsConsumed;
            int flatDamage=0;long damageTotal=0,afterDefense=0;RolledDamage rolled=null;
            if(shot.Attack.Attack.Hit) {
                int aggressive=c.Kind==CommandKind.WarningShot?0:TestOnlyClubAttackPolicy.ActiveStance(s,c.Actor)?.Kind==CombatStance.Aggressive?2:0;
                flatDamage=c.Kind==CommandKind.WarningShot?0:checked(PlaytestCharacters.AbilityModifier(combatant.DexterityScore)+aggressive);
                damageTotal=Math.Max(0L,dice.Sum(x=>(long)x)+flatDamage);
                afterDefense=CharacterAdvancementRules.ReduceIncomingDamage(s,c.Target,damageTotal);
                if(TestOnlyClubAttackPolicy.ConditionsFor(s,c.Target).View().Has(ConditionKind.Petrified))
                    afterDefense=PlaytestConditions.PetrifiedDamage(afterDefense);
                var targetCharacter=s.Characters.Single(x=>x.ActorId==c.Target);
                int constitutionSave=checked(PlaytestCharacters.AbilityModifier(targetCharacter.Abilities[2])
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,c.Target,"CON"));
                rolled=PlaytestDamageDice.Resolve(ActorLifeRules.Read(life),afterDefense,s.RuleClock,effectsSeed,
                    constitutionSaveModifier:constitutionSave,critical:shot.Attack.Critical,melee:false,knockout:KnockoutInstruction.OrdinaryOutcome);
                next=rolled.NextRandomState;
            } else {dice=Array.Empty<int>();}
            var attack=shot.Attack.Attack;
            var damage=new RangedDamageRoll(dice,flatDamage,damageTotal,afterDefense,diceWords,effectsSeed,
                next,rolled?.WordsConsumed??0,rolled?.WoundRoll?.Natural??0,rolled?.InjuryD6??0,rolled?.StableD4??0);
            if(shot.Attack.Attack.Hit)TestOnlyClubAttackPolicy.ApplyLife(s,life,rolled.Outcome.State);
            var recordedAttack=new CombatAttackRoll(shot.Attack.Roll.First,shot.Attack.Roll.Second??0,shot.Attack.Roll.Natural,
                shot.Attack.AttackModifier,shot.Attack.EffectiveArmorClass,shot.Attack.Attack.Hit,shot.Attack.Critical,
                randomBefore,shot.Attack.Roll.NextRandomState,shot.Attack.Roll.WordsConsumed);
            s.RangedAttacks=s.RangedAttacks.Concat(new[]{new RangedAttackRecord(attackId,s.Revision+1,s.Encounter.TurnOrdinal,
                c.Actor,c.Target,weapon.Id,ammunitionLot,s.RuleClock,recordedAttack,damage)}).ToArray();
            if(shot.Attack.Attack.Hit)SoldierTacticalFeatures.ApplyHit(s,attackId,c.Actor,c.Target,c.Kind);
            SoldierTacticalFeatures.StartRecharge(s,c.Actor,c.Kind);
            s.RandomState=next;SetInterval(s,interval.PayAction());return null;
        }

        private static string ShotFailureCode(RepeatingCrossbowShotFailure failure)
        {
            if(failure==RepeatingCrossbowShotFailure.NoAmmunition)return "NoAmmunition";
            if(failure==RepeatingCrossbowShotFailure.WrongWeaponRangeProfile)return "RangedAttackWrongWeaponRangeProfile";
            if(failure==RepeatingCrossbowShotFailure.UnknownTargetLocation)return "RangedAttackUnknownTargetLocation";
            if(failure==RepeatingCrossbowShotFailure.BlockedLineOfFire)return "RangedAttackBlockedLineOfFire";
            if(failure==RepeatingCrossbowShotFailure.TotalCover)return "RangedAttackTotalCover";
            return "RangedAttackOutOfRange";
        }
        private static string N(long value)=>value.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Small headless driver for the admitted Repeating crossbow commands. It selects an
    /// admissible shot first, otherwise loads the largest legal quantity, then submits that normal
    /// command through Simulation.Execute. This is a development harness, not game AI.</summary>
    public sealed class RepeatingCrossbowHeadlessController
    {
        public CommandResult Act(Simulation simulation,Authority authority,string actor)
        {
            if(simulation==null)throw new ArgumentNullException(nameof(simulation));
            if(authority==null)throw new ArgumentNullException(nameof(authority));
            if(!Validation.ValidId(actor))throw new ArgumentException("Invalid actor.",nameof(actor));
            var options=simulation.DiscoverCommands(authority,actor);
            var selected=options.FirstOrDefault(x=>x.Query.Admissible&&x.Command.Kind==CommandKind.AttackRepeatingCrossbow)
                ??options.Where(x=>x.Query.Admissible&&x.Command.Kind==CommandKind.ReloadRepeatingCrossbow)
                    .OrderByDescending(x=>x.Command.Ranged.Amount).FirstOrDefault();
            return selected==null?null:simulation.Execute(authority,selected.Command);
        }
    }
}
#endif
