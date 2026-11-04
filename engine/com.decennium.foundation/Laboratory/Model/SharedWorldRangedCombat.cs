#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
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

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private RepeatingCrossbowFixture rangedCombat;
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

        private string ResolveRepeatingCrossbow(Snapshot s,Command c)
        {
            bool attack=c.Kind==CommandKind.AttackRepeatingCrossbow;
            if(rangedCombat==null||s.SchemaVersion<Snapshot.RepeatingCrossbowSchema)return "RangedCommandNotImplemented";
            if(c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged==null||c.X!=0||c.Y!=0)return "InvalidRangedPayload";
            if(!s.InventoryCombat||s.Encounter==null)return "RangedCombatRequiresEncounter";
            if(PendingCalendarChoice(s))return "TacticalChoicePending";
            if(c.Actor!=s.Encounter.CurrentActor||c.Ranged.TurnId!=s.Encounter.CurrentTurnId)return "WrongRegularTurn";
            var interval=Interval(s,c.Actor);
            if(interval.ActionSpent)return "ActionAlreadySpent";
            if(!CapableWorker(s,c.Actor)||!Permissions(s,c.Actor).Action)return "ConditionPreventsAction";
            if(s.RepeatingCrossbows.Length!=1||c.Ranged.WeaponId!=RepeatingCrossbowFixture.WeaponId)return "CrossbowUnavailable";
            var weapon=s.RepeatingCrossbows.Single();
            if(weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor||!s.Lives.Single(l=>l.ActorId==c.Actor).HeldItems.Contains(weapon.Id))return "CrossbowNotHeld";
            if(attack) return ResolveRepeatingAttack(s,c,weapon,interval);
            return ResolveRepeatingReload(s,c,weapon,interval);
        }

        private string ResolveRepeatingReload(Snapshot s,Command c,RepeatingCrossbowRecord weapon,WorldIntervalRecord interval)
        {
            var request=c.Ranged;
            if(c.Target!=""||request.Amount<1||request.AmmoLotId=="")return "InvalidReloadRequest";
            var lot=s.AmmunitionLots.SingleOrDefault(x=>x.Id==request.AmmoLotId);
            if(lot==null||lot.CustodianId!=c.Actor||lot.OwnerId!=c.Actor||!lot.Accessible)return "AmmunitionInaccessible";
            if(weapon.LoadedBoltLots.Count==5)return "MagazineFull";
            if(request.Amount>5-weapon.LoadedBoltLots.Count)return "ReloadExceedsMagazineCapacity";
            if(request.Amount>lot.AvailableQuantity)return "InsufficientCarriedBolts";
            int available=AvailableHands(s,c.Actor)+(weapon.GripHands==2?1:0);
            if(available<1)return "LoadingHandRequired";
            s.AmmunitionLots=s.AmmunitionLots.Select(x=>x.Id==lot.Id?x.WithAvailable(x.AvailableQuantity-request.Amount):x).ToArray();
            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id
                ?new RepeatingCrossbowRecord(x.Id,x.ProfileId,x.OwnerId,x.CustodianId,x.HeldBy,1,x.CellX,x.CellY,x.LoadedBoltLots.Concat(Enumerable.Repeat(lot.Id,request.Amount)).ToArray()):x).ToArray();
            SetInterval(s,interval.PayAction());return null;
        }

        private string ResolveRepeatingAttack(Snapshot s,Command c,RepeatingCrossbowRecord weapon,WorldIntervalRecord interval)
        {
            var request=c.Ranged;
            if(c.Target==""||request.Amount!=0||request.AmmoLotId!="")return "InvalidRangedAttackRequest";
            if(c.Target!=rangedCombat.TargetId||!s.WorldSchedule.Order.Contains(c.Target))return "TargetOutsideEncounter";
            if(request.WeaponId!=weapon.Id||weapon.LoadedBoltLots.Count==0)return weapon.LoadedBoltLots.Count==0?"NoAmmunition":"CrossbowUnavailable";
            if(!TestOnlyClubAttackPolicy.HasStance(s))return "StanceRequired";
            if(s.RangedAttacks.Length==128)return "RangedAttackHistoryCapacityReached";
            var shooter=s.Actors.Single(a=>a.Id==c.Actor);var target=s.Actors.Single(a=>a.Id==c.Target);
            if(shooter.X!=rangedCombat.ShooterX||shooter.Y!=rangedCombat.ShooterY||target.X!=rangedCombat.TargetX||target.Y!=rangedCombat.TargetY)
                return "AuthoredRangedLaneRequired";
            var life=s.Lives.SingleOrDefault(l=>l.ActorId==c.Target);if(life==null||life.Dead)return "InvalidLivingTarget";
            if(!TestOnlyClubAttackPolicy.DamageConditionCapacity(s,c.Target))return "ConditionHistoryCapacityReached";
            if(AvailableHands(s,c.Actor)+(weapon.GripHands==1?1:0)<2)return "TwoHandsRequired";
            string physicalFailure=TestOnlyClubAttackPolicy.PhysicalAttackFailure(s,c.Actor);if(physicalFailure!=null)return physicalFailure;
            if(weapon.LoadedBoltLots.Count>0&&weapon.GripHands==1)
                s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id?x.WithGrip(2):x).ToArray();
            weapon=s.RepeatingCrossbows.Single(x=>x.Id==weapon.Id);
            var combatant=s.RangedCombatants.Single(x=>x.ActorId==c.Actor);
            var attackerLife=s.Lives.Single(x=>x.ActorId==c.Actor);
            var targetCombatant=s.RangedCombatants.SingleOrDefault(x=>x.ActorId==c.Target);
            int targetDex=targetCombatant?.DexterityScore??s.Characters.Single(x=>x.ActorId==c.Target).Abilities[1];
            var targetStance=TestOnlyClubAttackPolicy.ActiveStance(s,c.Target);
            int armorClass=checked((int)PrototypeArmor.UnarmoredBaseAc(targetDex)
                +(targetStance?.Kind==CombatStance.Aggressive?-2:targetStance?.Kind==CombatStance.Guarded?1:0)
                +CharacterAdvancementRules.DefensivePositioningBonus(s,c.Target));
            bool targetVisible=rangedCombat.TargetVisible&&TestOnlyClubAttackPolicy.CanSee(s,c.Actor,c.Target);
            bool attackerUnseen=!TestOnlyClubAttackPolicy.CanSee(s,c.Target,c.Actor);
            bool closeHostile=s.WorldSchedule.Order.Where(id=>id!=c.Actor).Any(id=>{
                var other=s.Actors.Single(a=>a.Id==id);var otherLife=s.Lives.Single(l=>l.ActorId==id);
                bool incapacitated=otherLife.Dead||otherLife.Hp==0||TestOnlyClubAttackPolicy.ConditionsFor(s,id).View().Clauses.Incapacitated;
                return PlanarCombatGeometry.CloseHostileDisadvantage(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(other.X,other.Y)),true,incapacitated,TestOnlyClubAttackPolicy.CanSee(s,id,c.Actor));
            });
            int flatAttack=attackerLife.LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0;
            var rangedFacts=new RangedAttackRequest(PlanarCombatGeometry.DistanceFeet(new CombatCell(shooter.X,shooter.Y),new CombatCell(target.X,target.Y)),
                RepeatingCrossbowShotRules.NormalRangeFeet,RepeatingCrossbowShotRules.MaximumRangeFeet,armorClass,
                PlaytestCharacters.AbilityModifier(combatant.DexterityScore),combatant.ProficiencyBonus,combatant.CrossbowProficient,flatAttack,
                rangedCombat.TargetCover,rangedCombat.TargetLocationKnown,targetVisible,rangedCombat.LineOfFireClear,attackerUnseen,closeHostile,
                TestOnlyClubAttackPolicy.CombatConditions(s,c.Actor),TestOnlyClubAttackPolicy.CombatConditions(s,c.Target),
                attackerInvisibleLocationKnown:true,targetInvisibleLocationKnown:true);
            uint randomBefore=s.RandomState;
            var shot=RepeatingCrossbowShotRules.Resolve(randomBefore,rangedFacts,new RepeatingFiveMagazine(weapon.LoadedBoltLots.Count),
                s.AmmunitionLots.Where(x=>x.CustodianId==c.Actor&&x.Accessible).Sum(x=>x.AvailableQuantity));
            if(!shot.Legal)return "RangedAttack"+shot.Failure;
            var ammunitionLot=weapon.LoadedBoltLots[0];
            var magazine=weapon.LoadedBoltLots.Skip(1).ToArray();
            s.RepeatingCrossbows=s.RepeatingCrossbows.Select(x=>x.Id==weapon.Id?x.WithMagazine(magazine):x).ToArray();
            uint effectsSeed=shot.RandomStateAfter,next=effectsSeed;int[] dice=shot.DamageDice.ToArray();long diceWords=shot.RandomWordsConsumed-shot.Attack.Roll.WordsConsumed;
            int flatDamage=0;long damageTotal=0,afterDefense=0;RolledDamage rolled=null;
            if(shot.Attack.Attack.Hit) {
                int aggressive=TestOnlyClubAttackPolicy.ActiveStance(s,c.Actor)?.Kind==CombatStance.Aggressive?2:0;
                flatDamage=checked(PlaytestCharacters.AbilityModifier(combatant.DexterityScore)+aggressive);
                damageTotal=Math.Max(0L,dice.Sum(x=>(long)x)+flatDamage);
                afterDefense=TestOnlyClubAttackPolicy.ConditionsFor(s,c.Target).View().Has(ConditionKind.Petrified)?PlaytestConditions.PetrifiedDamage(damageTotal):damageTotal;
                rolled=PlaytestDamageDice.Resolve(ActorLifeRules.Read(life),afterDefense,s.RuleClock,effectsSeed,
                    constitutionSaveModifier:0,critical:shot.Attack.Critical,melee:false,knockout:KnockoutInstruction.OrdinaryOutcome);
                next=rolled.NextRandomState;
            } else {dice=Array.Empty<int>();}
            var attack=shot.Attack.Attack;
            var damage=new RangedDamageRoll(dice,flatDamage,damageTotal,afterDefense,diceWords,effectsSeed,
                next,rolled?.WordsConsumed??0,rolled?.WoundRoll?.Natural??0,rolled?.InjuryD6??0,rolled?.StableD4??0);
            if(shot.Attack.Attack.Hit)TestOnlyClubAttackPolicy.ApplyLife(s,life,rolled.Outcome.State);
            var recordedAttack=new CombatAttackRoll(shot.Attack.Roll.First,shot.Attack.Roll.Second??0,shot.Attack.Roll.Natural,
                shot.Attack.AttackModifier,shot.Attack.EffectiveArmorClass,shot.Attack.Attack.Hit,shot.Attack.Critical,
                randomBefore,shot.Attack.Roll.NextRandomState,shot.Attack.Roll.WordsConsumed);
            s.RangedAttacks=s.RangedAttacks.Concat(new[]{new RangedAttackRecord("ranged."+N(s.Revision+1),s.Revision+1,s.Encounter.TurnOrdinal,
                c.Actor,c.Target,weapon.Id,ammunitionLot,s.RuleClock,recordedAttack,damage)}).ToArray();
            s.RandomState=next;SetInterval(s,interval.PayAction());return null;
        }
        private static string N(long value)=>value.ToString(CultureInfo.InvariantCulture);
    }
}
#endif
