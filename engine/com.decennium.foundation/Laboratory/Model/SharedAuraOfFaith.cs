#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    internal static class AuraOfFaithRules
    {
        internal static AuraOfFaithQualification Qualify(Snapshot s,string target)
        {
            if(!BishopProfile.Earned(s)||!s.CharacterFeatureGrants.Any(x=>x.FeatureId==BishopProfile.Aura&&BishopProfile.ValidGrant(s,x)))return null;
            string owner=ClericRpProfile.Actor;
            var ownerLife=s.Lives.Single(x=>x.ActorId==owner);var targetLife=s.Lives.Single(x=>x.ActorId==target);
            var ownerConditions=TestOnlyClubAttackPolicy.ConditionsFor(s,owner).View();
            var targetConditions=TestOnlyClubAttackPolicy.ConditionsFor(s,target).View();
            bool conscious=!ownerLife.Dead&&ownerLife.Hp>0&&!ownerConditions.Unaware;
            bool recipientConscious=!targetLife.Dead&&targetLife.Hp>0&&!targetConditions.Unaware;
            bool perceived=recipientConscious&&!targetConditions.BlocksSight
                &&(target==owner||ObservationRules.CanSee(s,target,owner));
            var a=ObservationGeometry.Position(s,owner);var b=ObservationGeometry.Position(s,target);
            return new AuraOfFaithQualification(BishopProfile.Advancement(s).Revision,target,conscious,
                SoldierTacticalFeatures.IsAlly(s,owner,target),recipientConscious,perceived,a.X,a.Y,b.X,b.Y);
        }
        internal static int Modifier(AuraOfFaithQualification qualification,int basis,int otherTemporary=0)
        {
            if(otherTemporary<0)throw new ArgumentOutOfRangeException(nameof(otherTemporary));
            return checked(basis+Math.Max(otherTemporary,qualification?.Bonus??0));
        }
        internal static void RecordSave(Snapshot s,AuraOfFaithQualification qualification,AuraSaveConsumer consumer,string cause,
            int basis,long dc,int natural,bool automatic,bool success,uint before,uint after,long words,int otherTemporary=0)
        {
            if(qualification==null)return;
            string id="aura.save."+(s.Revision+1).ToString(CultureInfo.InvariantCulture)+"."+s.BishopEntry.AuraSaves.Count.ToString(CultureInfo.InvariantCulture);
            var record=new AuraOfFaithSaveRecord(id,cause,s.Revision+1,s.RuleClock,consumer,qualification,basis,otherTemporary,dc,
                natural,automatic,success,before,after,words);
            s.BishopEntry=s.BishopEntry.WithAuraSaves(s.BishopEntry.AuraSaves.Append(record));
        }
        /// <summary>Qualifies before committing the damage packet. Pending knockout reuses the original qualification and save.</summary>
        internal static RolledDamage Damage(Snapshot s,ActorLifeRecord before,string cause,long resolvedDamage,RuleTime at,uint randomState,
            int constitutionSaveModifier=0,bool critical=false,bool maiming=false,bool melee=false,
            KnockoutInstruction knockout=KnockoutInstruction.OrdinaryOutcome,bool reconstructPending=false)
        {
            var life=ActorLifeRules.ReadForResolution(s,before);
            var prior=reconstructPending?s.BishopEntry?.AuraSaves.SingleOrDefault(x=>x.Consumer==AuraSaveConsumer.Wound
                &&x.Qualification.TargetId==before.ActorId&&x.At==at&&x.RandomBefore==randomState&&x.CauseId==cause):null;
            var qualified=prior?.Qualification??Qualify(s,before.ActorId);
            int basis=checked(constitutionSaveModifier-life.Wounds.Count);
            if(prior!=null&&prior.BaseModifier!=basis)throw new ArgumentException("Pending Wound base modifier changed.");
            var result=PlaytestDamageDice.Resolve(life,resolvedDamage,at,randomState,
                Modifier(qualified,constitutionSaveModifier),critical,maiming,melee,knockout);
            if(result.WoundRoll!=null&&qualified!=null) {
                long post=resolvedDamage-Math.Min(life.TemporaryHp,resolvedDamage),dc=Math.Max(10,post/2);
                var roll=result.WoundRoll;bool success=(long)roll.Natural+Modifier(qualified,basis)>=dc;
                if(reconstructPending) {
                    if(prior==null||prior.Natural!=roll.Natural||prior.Success!=success||prior.Dc!=dc||prior.RandomAfter!=roll.NextRandomState)
                        throw new ArgumentException("Pending Wound lost its original Aura contribution.");
                } else RecordSave(s,qualified,AuraSaveConsumer.Wound,cause,basis,dc,roll.Natural,false,success,randomState,roll.NextRandomState,roll.WordsConsumed);
            }
            return result;
        }
        internal static void HealAfterRite(Snapshot s,Command c,HealingRiteRecord rite)
        {
            if(rite.ActualGain<=0)return;
            var qualified=Qualify(s,rite.TargetId);if(qualified==null)return;
            var before=s.Lives.Single(x=>x.ActorId==rite.TargetId);
            long potential=TestOnlyClubAttackPolicy.ConditionsFor(s,rite.TargetId).View().HealingPotential(qualified.Bonus);
            var healed=PlaytestLife.Heal(ActorLifeRules.ReadForResolution(s,before),potential);
            TestOnlyClubAttackPolicy.ApplyLife(s,before,healed);
            var record=new AuraOfFaithHealingRecord(c.Id,s.Revision+1,s.RuleClock,qualified,rite.ActualGain,before.Hp,potential,healed.Hp);
            s.BishopEntry=s.BishopEntry.WithAuraHealing(s.BishopEntry.AuraHealing.Append(record));
        }
    }
}
#endif
