#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Schema26 TEST_ONLY execution of the first source-bound movement-triggered Base
    /// Overwatch lane. It uses the shared tactical Reaction, ranged attack, ammunition, life,
    /// calendar and periodic-rider records. Geometry remains restricted to the authored cardinal lane.</summary>
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private enum PostStepChoiceKind { None, Press, Overwatch, HuntingTrap }

        private sealed class OverwatchShotFacts
        {
            public OverwatchDesignationRecord Zone;
            public RepeatingCrossbowRecord Weapon;
            public AmmunitionLotRecord Ammunition;
            public RangedCombatantRecord Attacker;
            public ActorState Shooter;
            public ActorState Target;
            public ActorLifeRecord TargetLife;
            public RangedAttackResolution Attack;
        }

        private static string OverwatchIdentity(string input)
        {
            using(var sha=SHA256.Create())return "overwatch."+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(input)).Take(16)
                .Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }

        private static OverwatchOfferRecord PendingOverwatchOffer(Snapshot s)
            =>s.OverwatchOffers.SingleOrDefault(x=>x.Status==OverwatchOfferStatus.Pending);

        public static bool AutomaticPushStrengthSaveFailure(Snapshot s,string targetId)
            =>TestOnlyClubAttackPolicy.ConditionsFor(s,targetId).View().AutomaticStrengthDexterityFailure;

        private static PostStepChoiceKind NextPostStepChoice(Snapshot s)
        {
            var events=new System.Collections.Generic.List<(long Created,long Source,string Id,PostStepChoiceKind Kind)>();
            var press=TestOnlyClubAttackPolicy.CurrentPressOffer(s);if(press!=null)
                events.Add((press.CreatedRevision,press.ArmedRevision,press.Id,PostStepChoiceKind.Press));
            var ow=PendingOverwatchOffer(s);if(ow!=null)
                events.Add((ow.CreatedRevision,ow.SourceAppliedRevision,ow.Id,PostStepChoiceKind.Overwatch));
            var trap=PendingHuntingTrapTrigger(s);if(trap!=null)
                events.Add((trap.CreatedRevision,trap.SourceAppliedRevision,trap.Id,PostStepChoiceKind.HuntingTrap));
            return events.OrderBy(x=>x.Created).ThenBy(x=>x.Source).ThenBy(x=>x.Id,StringComparer.Ordinal)
                .Select(x=>x.Kind).FirstOrDefault();
        }

        internal static bool OverwatchHasPriorityOverPress(Snapshot s)=>NextPostStepChoice(s)==PostStepChoiceKind.Overwatch;

        private static bool AttackingFromActiveOverwatchZone(Snapshot s,string actor,string target)
            =>s.SchemaVersion>=Snapshot.OverwatchExecutionSchema&&s.OverwatchDesignations.Any(z=>z.Status==OverwatchDesignationStatus.Active
                &&z.OwnerId!=actor&&z.OwnerId==target&&CurrentOverwatchInterval(s,z.OwnerId)?.LastRegularStart==z.LastRegularStart
                &&z.Contains(s.Actors.Single(a=>a.Id==actor).X,s.Actors.Single(a=>a.Id==actor).Y));

        private string QueueCompletedMovementOverwatch(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.OverwatchExecutionSchema||overwatchExecution==null)return null;
            var completed=s.TacticalMoves.Where(x=>x.Status==TacticalMoveStatus.Completed&&x.ResolvedRevision==s.Revision+1)
                .OrderBy(x=>x.ResolvedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal).ToArray();
            foreach(var move in completed) {
                foreach(var zone in s.OverwatchDesignations.Where(x=>x.Status==OverwatchDesignationStatus.Active&&x.OwnerId!=move.ActorId
                    &&CurrentOverwatchInterval(s,x.OwnerId)?.LastRegularStart==x.LastRegularStart)
                    .OrderBy(x=>x.CreatedRevision).ThenBy(x=>x.Id,StringComparer.Ordinal)) {
                    bool horizontal=move.ToY==zone.Y0+1&&move.ToX>=zone.X0&&move.ToX<=zone.X0+2;
                    bool vertical=move.ToX==zone.X0+1&&move.ToY>=zone.Y0&&move.ToY<=zone.Y0+2;
                    if(move.ActorId!=rangedCombat?.TargetId||!zone.Contains(move.ToX,move.ToY)||!horizontal&&!vertical)continue;
                    if(!overwatchExecution.TargetVisible||!TestOnlyClubAttackPolicy.CanSee(s,zone.OwnerId,move.ActorId))continue;
                    if(s.OverwatchOffers.Any(x=>x.DesignationId==zone.Id))continue; // one occurrence per zone and interval
                    if(s.OverwatchOffers.Length>=OverwatchExecutionValidation.MaxOffers)return "OverwatchHistoryCapacityReached";
                    string id=OverwatchIdentity("offer|"+move.Id+"|"+zone.Id);
                    s.OverwatchOffers=s.OverwatchOffers.Concat(new[]{new OverwatchOfferRecord(id,move.Id,zone.OwnerId,move.ActorId,
                        zone.Id,s.Revision+1,zone.CreatedRevision)}).ToArray();
                }
            }
            NormalizePendingOverwatchOffers(s);
            return null;
        }

        private void NormalizePendingOverwatchOffers(Snapshot s)
        {
            foreach(var offer in s.OverwatchOffers.Where(x=>x.Status==OverwatchOfferStatus.Pending).ToArray())
                if(!TryBuildOverwatchShot(s,offer,out _))
                    s.OverwatchOffers=s.OverwatchOffers.Select(x=>x.Id==offer.Id?x.Resolve(OverwatchOfferStatus.Invalidated,s.Revision+1):x).ToArray();
        }

        private bool TryBuildOverwatchShot(Snapshot s,OverwatchOfferRecord offer,out OverwatchShotFacts facts)
        {
            facts=null;
            if(overwatchExecution==null||rangedCombat==null||s.SchemaVersion<Snapshot.OverwatchExecutionSchema||!s.InventoryCombat||s.Encounter==null
                ||!s.WorldSchedule.Order.Contains(offer.OwnerId)||!s.WorldSchedule.Order.Contains(offer.TargetId)
                ||offer.OwnerId!=rangedCombat.ShooterId||offer.TargetId!=rangedCombat.TargetId)return false;
            var zone=s.OverwatchDesignations.SingleOrDefault(x=>x.Id==offer.DesignationId&&x.OwnerId==offer.OwnerId
                &&x.CreatedRevision==offer.SourceAppliedRevision&&x.Status==OverwatchDesignationStatus.Active
                &&CurrentOverwatchInterval(s,offer.OwnerId)?.LastRegularStart==x.LastRegularStart);
            if(zone==null)return false;
            // The source interval is the designation's regular-start ordinal, not its application revision.
            var entitlement=s.OverwatchIntervals.SingleOrDefault(x=>x.ActorId==offer.OwnerId&&x.LastRegularStart==zone.LastRegularStart);
            if(entitlement==null||entitlement.ShotStatus!=OverwatchShotStatus.Available
                ||s.OverwatchOffers.Any(x=>x.Id!=offer.Id&&x.DesignationId==zone.Id))return false;
            var shooter=s.Actors.Single(x=>x.Id==offer.OwnerId);var target=s.Actors.Single(x=>x.Id==offer.TargetId);
            bool horizontal=target.Y==zone.Y0+1&&target.X>=zone.X0&&target.X<=zone.X0+2&&shooter.Y==target.Y;
            bool vertical=target.X==zone.X0+1&&target.Y>=zone.Y0&&target.Y<=zone.Y0+2&&shooter.X==target.X;
            if(!zone.Contains(target.X,target.Y)||!horizontal&&!vertical)return false;
            var tactical=s.TacticalActors.SingleOrDefault(x=>x.ActorId==offer.OwnerId);
            var world=Interval(s,offer.OwnerId);
            var weapon=s.RepeatingCrossbows.SingleOrDefault(x=>x.Id==RepeatingCrossbowFixture.WeaponId);
            var targetLife=s.Lives.SingleOrDefault(x=>x.ActorId==offer.TargetId);
            if(tactical==null||!tactical.ReactionAvailable||!world.ReactionAvailable||!Permissions(s,offer.OwnerId).Reaction
                ||!ActorLifeRules.CanAct(s,offer.OwnerId)||TestOnlyClubAttackPolicy.PhysicalAttackFailure(s,offer.OwnerId)!=null
                ||!s.CharacterFeatureGrants.Any(x=>x.ActorId==offer.OwnerId&&x.FeatureId==CharacterFeatureIds.Overwatch)
                ||weapon==null||weapon.HeldBy!=offer.OwnerId||weapon.CustodianId!=offer.OwnerId||weapon.LoadedBoltLots.Count==0
                ||AvailableHands(s,offer.OwnerId)+weapon.GripHands<2||targetLife==null||targetLife.Dead
                ||s.RangedAttacks.Length>=128||s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema&&s.TacticalAttackAudits.Length>=SoldierTacticalFeatureValidation.MaxAttackAudits
                ||s.OverwatchRiderChoices.Length>=OverwatchExecutionValidation.MaxRiderChoices
                ||!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,offer.TargetId))return false;
            var ammunition=s.AmmunitionLots.SingleOrDefault(x=>x.Id==weapon.LoadedBoltLots[0]);
            var attacker=s.RangedCombatants.SingleOrDefault(x=>x.ActorId==offer.OwnerId);
            if(ammunition==null||attacker==null||ammunition.CustodianId!=offer.OwnerId)return false;
            long distance=PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(target.X,target.Y));
            if(distance>RepeatingCrossbowShotRules.MaximumRangeFeet||!overwatchExecution.TargetVisible
                ||!TestOnlyClubAttackPolicy.CanSee(s,offer.OwnerId,offer.TargetId))return false;
            int dex=PlaytestCharacters.AbilityModifier(s.Characters.Single(x=>x.ActorId==offer.TargetId).Abilities[1]);
            var defense=TestOnlyClubAttackPolicy.ActiveStance(s,offer.TargetId);
            int targetDexterity=s.Characters.Single(x=>x.ActorId==offer.TargetId).Abilities[1];
            int ac=checked(CharacterAdvancementRules.ArmorClass(s,offer.TargetId,targetDexterity)
                +(defense?.Kind==CombatStance.Aggressive?-2:defense?.Kind==CombatStance.Guarded?1:0)
                +CharacterAdvancementRules.DefensivePositioningBonus(s,offer.TargetId));
            bool closeHostile=s.WorldSchedule.Order.Where(id=>id!=offer.OwnerId&&!SoldierTacticalFeatures.IsAlly(s,offer.OwnerId,id)).Any(id=>{
                var other=s.Actors.Single(a=>a.Id==id);var otherLife=s.Lives.Single(l=>l.ActorId==id);
                bool incapacitated=otherLife.Dead||otherLife.Hp==0||TestOnlyClubAttackPolicy.ConditionsFor(s,id).View().Clauses.Incapacitated;
                return PlanarCombatGeometry.CloseHostileDisadvantage(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),
                    new CombatCell(other.X,other.Y)),true,incapacitated,TestOnlyClubAttackPolicy.CanSee(s,id,offer.OwnerId));
            });
            var incomingEffects=SoldierTacticalFeatures.ForAttack(s,offer.OwnerId,offer.TargetId);
            int flatAttack=checked((s.Lives.Single(x=>x.ActorId==offer.OwnerId).LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0)
                -incomingEffects.CoveringFirePenalty+incomingEffects.TacticalAssessmentBonus);
            bool attackerInvisibleKnown=!ObservationRules.Enabled(s)||ObservationRules.InvisibleRevealed(s,offer.TargetId,offer.OwnerId);
            bool targetInvisibleKnown=!ObservationRules.Enabled(s)||ObservationRules.InvisibleRevealed(s,offer.OwnerId,offer.TargetId);
            bool attackerUnseen=!TestOnlyClubAttackPolicy.CanSee(s,offer.TargetId,offer.OwnerId);
            bool attackerUnseenAdvantage=attackerUnseen&&!(ObservationRules.Enabled(s)&&attackerInvisibleKnown
                &&ObservationRules.InvisibleIsOnlySightBlocker(s,offer.TargetId,offer.OwnerId));
            var request=new RangedAttackRequest(distance,RepeatingCrossbowShotRules.NormalRangeFeet,RepeatingCrossbowShotRules.MaximumRangeFeet,ac,
                PlaytestCharacters.AbilityModifier(attacker.DexterityScore),attacker.ProficiencyBonus,attacker.CrossbowProficient,flatAttack,
                overwatchExecution.TargetCover,overwatchExecution.TargetLocationKnown,true,overwatchExecution.LineOfFireClear,
                attackerUnseen,closeHostile,
                TestOnlyClubAttackPolicy.CombatConditions(s,offer.OwnerId),TestOnlyClubAttackPolicy.CombatConditions(s,offer.TargetId),
                attackerInvisibleLocationKnown:attackerInvisibleKnown,targetInvisibleLocationKnown:targetInvisibleKnown,
                additionalDisadvantageSources:(incomingEffects.WarningShot?1:0)
                    +(TestOnlyClubAttackPolicy.DodgeEffective(s,offer.TargetId)&&TestOnlyClubAttackPolicy.CanSee(s,offer.TargetId,offer.OwnerId)?1:0),
                targetUnseenDisadvantage:false,attackerUnseenAdvantage:attackerUnseenAdvantage);
            var attack=RangedAttackRules.Resolve(s.RandomState,request);if(!attack.Legal)return false;
            facts=new OverwatchShotFacts{Zone=zone,Weapon=weapon,Ammunition=ammunition,Attacker=attacker,Shooter=shooter,Target=target,
                TargetLife=targetLife,Attack=attack};
            return true;
        }

        private string ResolveOverwatchResponse(Snapshot s,Command c)
        {
            var offer=PendingOverwatchOffer(s);var request=c.Combat;
            if(offer==null)return "NoPendingOverwatchChoice";
            if(NextPostStepChoice(s)!=PostStepChoiceKind.Overwatch)return "EarlierPostStepChoicePending";
            if(request==null||c.Actor!=offer.OwnerId||c.Target!=offer.Id||request.TurnId!=s.Encounter.CurrentTurnId
                ||request.WeaponId!=""||request.Stance!=0||request.Knockout!=AttackKnockoutMode.OrdinaryOutcome
                ||request.PressInstruction!=PressHitInstruction.ArmOrReplace||c.X!=0||c.Y!=0)return "InvalidOverwatchResponse";
            if(!TryBuildOverwatchShot(s,offer,out var facts)) {
                s.OverwatchOffers=s.OverwatchOffers.Select(x=>x.Id==offer.Id?x.Resolve(OverwatchOfferStatus.Invalidated,s.Revision+1):x).ToArray();
                return null;
            }
            if(!request.Choice) {
                s.OverwatchIntervals=s.OverwatchIntervals.Select(x=>x.ActorId==offer.OwnerId&&x.LastRegularStart==facts.Zone.LastRegularStart
                    ?x.WithStatus(OverwatchShotStatus.Forfeited):x).ToArray();
                s.OverwatchOffers=s.OverwatchOffers.Select(x=>x.Id==offer.Id?x.Resolve(OverwatchOfferStatus.Declined,s.Revision+1):x).ToArray();
                return null;
            }
            if(s.RangedAttacks.Length>=128||s.OverwatchRiderChoices.Length>=OverwatchExecutionValidation.MaxRiderChoices)return "OverwatchHistoryCapacityReached";
            if(s.SchemaVersion>=Snapshot.SoldierTacticalTechniquesSchema&&s.TacticalAttackAudits.Length>=SoldierTacticalFeatureValidation.MaxAttackAudits)
                return "TacticalAttackAuditCapacityReached";
            string attackId="ranged.ow."+N(s.Revision+1);
            s.TacticalActors=s.TacticalActors.Select(x=>x.ActorId==offer.OwnerId
                ?new ActorTacticalRecord(x.ActorId,x.LastRegularStart,false,x.MobileFeet,x.PressConsumed,x.DisengageTurn):x).ToArray();
            SetInterval(s,Interval(s,offer.OwnerId).WithReaction(false));
            s.OverwatchIntervals=s.OverwatchIntervals.Select(x=>x.ActorId==offer.OwnerId&&x.LastRegularStart==facts.Zone.LastRegularStart
                ?x.WithStatus(OverwatchShotStatus.Spent):x).ToArray();
            if(facts.Weapon.GripHands<2)s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==facts.Weapon.Id?x.WithGrip(2):x).ToArray();
            var magazine=facts.Weapon.LoadedBoltLots.ToArray();string ammunitionId=magazine[0];
            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==facts.Weapon.Id?x.WithMagazine(magazine.Skip(1).ToArray()):x).ToArray();
            string captureFailure=SoldierTacticalFeatures.CaptureAndConsume(s,attackId,offer.OwnerId,offer.TargetId,"",out _);
            if(captureFailure!=null)return captureFailure;
            uint before=s.RandomState;var shot=facts.Attack;uint next=shot.RandomStateAfter;int[] dice=Array.Empty<int>();long diceWords=0,total=0,afterDefense=0;RolledDamage rolled=null;
            int flatDamage=checked(PlaytestCharacters.AbilityModifier(facts.Attacker.DexterityScore)
                +(TestOnlyClubAttackPolicy.ActiveStance(s,offer.OwnerId)?.Kind==CombatStance.Aggressive?2:0));
            if(shot.Attack.Hit) {
                int count=shot.Critical?2:1;dice=new int[count];
                for(int i=0;i<count;i++){var die=DiceStream.Draw(next,8);dice[i]=die.Value+1;next=die.NextState;diceWords=checked(diceWords+die.WordsConsumed);}
                total=Math.Max(0L,dice.Sum(x=>(long)x)+flatDamage);
                afterDefense=CharacterAdvancementRules.ReduceIncomingDamage(s,offer.TargetId,total);
                if(TestOnlyClubAttackPolicy.ConditionsFor(s,offer.TargetId).View().Has(ConditionKind.Petrified))
                    afterDefense=PlaytestConditions.PetrifiedDamage(afterDefense);
                var targetCharacter=s.Characters.Single(x=>x.ActorId==offer.TargetId);
                int con=checked(PlaytestCharacters.AbilityModifier(targetCharacter.Abilities[2])
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,offer.TargetId,"CON"));
                rolled=PlaytestDamageDice.Resolve(ActorLifeRules.Read(facts.TargetLife),afterDefense,s.RuleClock,next,
                    constitutionSaveModifier:con,critical:shot.Critical,melee:false,knockout:KnockoutInstruction.OrdinaryOutcome);
                next=rolled.NextRandomState;
                TestOnlyClubAttackPolicy.ApplyLife(s,facts.TargetLife,rolled.Outcome.State);
            } else flatDamage=0;
            long effectsWords=rolled?.WordsConsumed??0;uint effectsSeed=shot.RandomStateAfter;
            var damage=new RangedDamageRoll(dice,flatDamage,total,afterDefense,diceWords,effectsSeed,next,effectsWords,
                rolled?.WoundRoll?.Natural??0,rolled?.InjuryD6??0,rolled?.StableD4??0);
            var attackRecord=new CombatAttackRoll(shot.Roll.First,shot.Roll.Second??0,shot.Roll.Natural,shot.AttackModifier,
                shot.EffectiveArmorClass,shot.Attack.Hit,shot.Critical,before,shot.Roll.NextRandomState,shot.Roll.WordsConsumed);
            var record=new RangedAttackRecord(attackId,s.Revision+1,s.Encounter.TurnOrdinal,offer.OwnerId,offer.TargetId,
                facts.Weapon.Id,ammunitionId,s.RuleClock,attackRecord,damage);
            s.RangedAttacks=s.RangedAttacks.Concat(new[]{record}).ToArray();s.RandomState=next;
            s.OverwatchOffers=s.OverwatchOffers.Select(x=>x.Id==offer.Id?x.Resolve(OverwatchOfferStatus.Accepted,s.Revision+1,attackId):x).ToArray();
            var targetLife=s.Lives.Single(x=>x.ActorId==offer.TargetId);
            if(shot.Attack.Hit&&!targetLife.Dead) {
                string choiceId=OverwatchIdentity("choice|"+offer.Id+"|"+attackId);
                s.OverwatchRiderChoices=s.OverwatchRiderChoices.Concat(new[]{new OverwatchRiderChoiceRecord(choiceId,offer.Id,attackId,
                    offer.OwnerId,offer.TargetId,s.Revision+1)}).ToArray();
            }
            return null;
        }

        private string ResolveOverwatchRiderChoice(Snapshot s,Command c)
        {
            var pending=s.OverwatchRiderChoices.SingleOrDefault(x=>x.Status==OverwatchRiderChoiceStatus.Pending);
            if(pending==null)return "NoPendingOverwatchRiderChoice";
            if(c.Kind!=CommandKind.ResolveOverwatchRider||c.Actor!=pending.OwnerId||c.Target!=pending.Id||c.X!=0||c.Y!=0
                ||c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null)return "InvalidOverwatchRiderChoice";
            var target=s.Actors.Single(x=>x.Id==pending.TargetId);var owner=s.Actors.Single(x=>x.Id==pending.OwnerId);
            int expires=-1,natural=0,modifier=0,dc=0;long total=0,words=0;bool success=false;uint randomBefore=s.RandomState,randomAfter=s.RandomState;
            int fromX=target.X,fromY=target.Y,toX=fromX,toY=fromY,moved=0;
            switch(c.OverwatchRider) {
                case OverwatchRider.Snare:
                    expires=checked((int)NextStartSlot(s,pending.TargetId));
                    if(expires<=s.Encounter.TurnOrdinal)return "OverwatchSnareExpiryUnavailable";
                    break;
                case OverwatchRider.Bleed:
                    if(periodicRider==null||s.PeriodicRiders.Length>=PeriodicRiderValidation.MaxRiders
                        ||s.PeriodicRiderEvents.Length>=PeriodicRiderValidation.MaxEvents)return "PeriodicRiderCapacityReached";
                    ApplyOverwatchBleed(s,pending);
                    break;
                case OverwatchRider.Push:
                    if(TestOnlyClubAttackPolicy.ConditionsFor(s,pending.TargetId).View().Clauses.Has(ConditionClause.Staggered))return "UnsupportedStaggeredPush";
                    if(owner.X!=target.X&&owner.Y!=target.Y)return "UnsupportedOverwatchPushGeometry";
                    int directionX=Math.Sign(target.X-owner.X),directionY=Math.Sign(target.Y-owner.Y);
                    if((directionX!=0||directionY!=0)
                        &&PendingHuntingTrapEntryBlocksMove(s,pending.TargetId,target.X+directionX,target.Y+directionY))
                        return "UnsupportedPendingTrapDisplacement";
                    if((directionX!=0||directionY!=0)
                        &&HuntingTrapValidation.BlocksGridMove(s,pending.TargetId,target.X+directionX,target.Y+directionY))
                        return "HuntingTrapTetherPreventsPush";
                    var charTarget=s.Characters.Single(x=>x.ActorId==pending.TargetId);
                    var charOwner=s.Characters.Single(x=>x.ActorId==pending.OwnerId);
                    dc=checked(8+PlaytestCharacters.ProficiencyBonus(charOwner.Levels.Count)+PlaytestCharacters.AbilityModifier(charOwner.Abilities[2]));
                    modifier=checked(PlaytestCharacters.AbilityModifier(charTarget.Abilities[0])
                        +CharacterAdvancementRules.SaveProficiencyBonus(s,pending.TargetId,"STR")
                        +overwatchExecution.AdditionalStrengthSaveModifier);
                    bool automaticFailure=AutomaticPushStrengthSaveFailure(s,pending.TargetId);
                    if(automaticFailure) {success=false;}
                    else {
                        var save=PlaytestDice.RollD20(s.RandomState);natural=save.Natural;randomAfter=save.NextRandomState;words=save.WordsConsumed;
                        var result=PlaytestRolls.SavingThrow(natural,modifier,dc);total=result.Total;success=result.Success;s.RandomState=randomAfter;
                    }
                    if(!success) {
                        toX=target.X+directionX;toY=target.Y+directionY;
                        if((directionX!=0||directionY!=0)&&TestOnlyPolicy.Walkable(toX,toY)
                            &&(!ObservationRules.Enabled(s)||ObservationGeometry.SupportsAnchorAt(s,toX,toY))
                            &&!s.Actors.Any(x=>x.Id!=target.Id&&x.X==toX&&x.Y==toY)) {
                            target.X=toX;target.Y=toY;moved=5;
                            CharacterAdvancementRules.MarkMoved(s,target.Id);
                            s.Clubs=s.Clubs.Select(x=>x.HeldBy==target.Id?new ClubInstance(x.Id,x.ProfileId,x.OwnerId,x.CustodianId,x.HeldBy,toX,toY):x).ToArray();
                            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.HeldBy==target.Id
                                ?new RepeatingCrossbowRecord(x.Id,x.ProfileId,x.OwnerId,x.CustodianId,x.HeldBy,x.GripHands,toX,toY,x.LoadedBoltLots.ToArray()):x).ToArray();
                        } else {toX=fromX;toY=fromY;}
                    }
                    break;
                default:return "InvalidOverwatchRiderChoice";
            }
            var resolved=pending.Resolve(c.OverwatchRider,s.Revision+1,expires,natural,modifier,dc,total,success,randomBefore,randomAfter,words,
                c.OverwatchRider==OverwatchRider.Push?fromX:0,c.OverwatchRider==OverwatchRider.Push?fromY:0,
                c.OverwatchRider==OverwatchRider.Push?toX:0,c.OverwatchRider==OverwatchRider.Push?toY:0,
                c.OverwatchRider==OverwatchRider.Push?moved:0);
            s.OverwatchRiderChoices=s.OverwatchRiderChoices.Select(x=>x.Id==pending.Id?resolved:x).ToArray();
            return null;
        }

        private void ApplyOverwatchBleed(Snapshot s,OverwatchRiderChoiceRecord choice)
        {
            string eventId=EventIdentity("overwatch-bleed",choice.Id);uint random=s.RandomState;
            if(ImmuneToPeriodicFamily(s,choice.TargetId,PeriodicRiderFixture.FamilyId)) {
                AppendPeriodicEvent(s,new PeriodicRiderEventRecord(eventId,PeriodicRiderEventKind.Prevented,PeriodicRiderOutcome.Immune,
                    s.Revision+1,s.RuleClock,-1,choice.OwnerId,choice.TargetId,"",PeriodicRiderFixture.SourceId,true,0,0,0,0,0,0,random,random,0));return;
            }
            long marker=NextStartSlot(s,choice.TargetId);
            var prior=s.PeriodicRiders.SingleOrDefault(x=>x.Present&&x.OwnerId==choice.OwnerId&&x.TargetId==choice.TargetId
                &&x.SourceId==PeriodicRiderFixture.SourceId&&x.ProfileId==PeriodicRiderFixture.ProfileId);
            var character=s.Characters.Single(x=>x.ActorId==choice.OwnerId);
            int dc=checked(8+PlaytestCharacters.ProficiencyBonus(character.Levels.Count)+PlaytestCharacters.AbilityModifier(character.Abilities[2]));
            if(prior!=null) {
                s.PeriodicRiders=s.PeriodicRiders.Select(x=>x.Id==prior.Id?x.Refresh(marker):x).ToArray();
                AppendPeriodicEvent(s,new PeriodicRiderEventRecord(eventId,PeriodicRiderEventKind.Refreshed,PeriodicRiderOutcome.None,
                    s.Revision+1,s.RuleClock,-1,choice.OwnerId,choice.TargetId,prior.Id,PeriodicRiderFixture.SourceId,false,0,0,dc,0,0,0,random,random,0));
            } else {
                string riderId=OverwatchIdentity("bleed|"+choice.Id);
                s.PeriodicRiders=s.PeriodicRiders.Concat(new[]{new PeriodicRiderRecord(riderId,PeriodicRiderFixture.ProfileId,
                    PeriodicRiderFixture.FamilyId,choice.OwnerId,PeriodicRiderFixture.SourceId,choice.TargetId,eventId,"piercing",dc,
                    s.Revision+1,s.RuleClock,marker,1)}).ToArray();
                AppendPeriodicEvent(s,new PeriodicRiderEventRecord(eventId,PeriodicRiderEventKind.Applied,PeriodicRiderOutcome.None,
                    s.Revision+1,s.RuleClock,-1,choice.OwnerId,choice.TargetId,riderId,PeriodicRiderFixture.SourceId,false,0,0,dc,0,0,0,random,random,0));
            }
        }

        private static void ExpireOverwatchSnares(Snapshot s,string actor,int turnOrdinal,long revision)
        {
            s.OverwatchRiderChoices=s.OverwatchRiderChoices.Select(x=>x.Status==OverwatchRiderChoiceStatus.Resolved
                &&x.Choice==OverwatchRider.Snare&&x.TargetId==actor&&x.ExpiresAfterTurnOrdinal==turnOrdinal?x.Expire(revision):x).ToArray();
        }
    }
}
#endif
