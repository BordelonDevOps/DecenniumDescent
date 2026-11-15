#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        internal static string SpellDamageCapacityFailure(Snapshot s,string target,int otherPossibleSaves=0)
        {
            if(!s.ConnectedClericCasting)return null;
            int needed=otherPossibleSaves+(s.SpellEffects.Any(x=>x.Present&&x.RequiresConcentration&&x.CasterId==target)?1:0);
            return needed>SpellCastingProfile.MaxSaves-s.SpellSaves.Length?"CastingHistoryFull":null;
        }
        internal static int EffectiveArmorClass(Snapshot s,string target,int dexterity)
        {
            var stance=TestOnlyClubAttackPolicy.ActiveStance(s,target);
            int baseAc=CharacterAdvancementRules.ArmorClass(s,target,dexterity);
            int penalty=stance?.Kind==CombatStance.Aggressive?-2:0,guarded=stance?.Kind==CombatStance.Guarded?1:0;
            int positioning=CharacterAdvancementRules.DefensivePositioningBonus(s,target);
            if(!s.ConnectedClericCasting)return checked(baseAc+penalty+guarded+positioning);
            int ward=s.SpellEffects.Any(x=>x.Present&&x.SpellId=="arcane-ward"&&x.TargetId==target&&x.ExpiresAt>s.RuleClock)?1:0;
            return checked(baseAc+penalty+SpellCastingProfile.CombineFlatArmorBonuses(ward,guarded,0,positioning));
        }
        internal static void EndCastingConcentration(Snapshot s,string actor,string cause,RuleTime at,SpellEffectEndReason reason)
        {
            if(!s.ConnectedClericCasting)return;
            foreach(var effect in s.SpellEffects.Where(x=>x.Present&&x.RequiresConcentration&&x.CasterId==actor).ToArray())
                EndSpellEffect(s,effect,cause,s.Revision+1,at,reason);
        }

        internal static void EndCastingForLife(Snapshot s,ActorLifeRecord before,LifeState after)
        {
            if(!s.ConnectedClericCasting || !after.Dead&&after.Hp>0)return;
            EndCastingConcentration(s,before.ActorId,SpellCastingProfile.LifeEndingCause(s.Revision+1,before.ActorId),s.RuleClock,
                after.Dead?SpellEffectEndReason.Dead:SpellEffectEndReason.Incapacitated);
        }

        internal static void BreakSanctuaryForHostileSave(Snapshot s,string actor,string cause)
        {
            if(!s.ConnectedClericCasting)return;
            foreach(var effect in s.SpellEffects.Where(x=>x.Present&&x.SpellId=="sanctuary"&&x.TargetId==actor).ToArray())
                EndSpellEffect(s,effect,cause,s.Revision+1,s.RuleClock,SpellEffectEndReason.SanctuaryHostileSave);
        }

        /// <summary>Called once after an actual positive post-mitigation packet's complete life settlement.
        /// Damage includes temporary-HP absorption. Healing and deferred knockout work never call this hook.</summary>
        internal static void SettleSpellDamage(Snapshot s,string target,string attacker,string cause,long damage,bool intentional=true)
        {
            if(!s.ConnectedClericCasting || damage<=0)return;
            if(!Validation.ValidId(cause))throw new ArgumentException("Spell damage requires the actual resolving command.");
            if(intentional && attacker!="")foreach(var ward in s.SpellEffects.Where(x=>x.Present&&x.SpellId=="sanctuary"&&x.TargetId==attacker).ToArray())
                EndSpellEffect(s,ward,cause,s.Revision+1,s.RuleClock,SpellEffectEndReason.SanctuaryDamage);
            var concentration=s.SpellEffects.SingleOrDefault(x=>x.Present&&x.RequiresConcentration&&x.CasterId==target);
            if(concentration==null)return;
            var life=s.Lives.Single(x=>x.ActorId==target);
            if(life.Dead || life.Hp==0 || !Permissions(s,target).ConcentrationMayContinue) {
                EndSpellEffect(s,concentration,cause,s.Revision+1,s.RuleClock,life.Dead?SpellEffectEndReason.Dead:SpellEffectEndReason.Incapacitated);
                return;
            }
            if(s.SpellSaves.Length>=SpellCastingProfile.MaxSaves)throw new ArgumentException("CastingHistoryFull");
            int dc=checked((int)Math.Max(10,damage/2));
            int modifier=checked(CharacterRuleFacts.ForActor(s,target).AbilityModifier(CharacterAbility.Constitution)
                +CharacterAdvancementRules.SaveProficiencyBonus(s,target,"CON")+ExpeditionStrainRules.Current(s,target).SavingThrowModifier);
            uint random=s.RandomState;
            // This cohort has no CON-save advantage/disadvantage source. Incapacitation has already
            // ended the slot; Poisoned and Frightened check penalties are not save penalties.
            var roll=PlaytestDice.RollD20(random); bool success=(long)roll.Natural+modifier>=dc;
            string id="spell.save."+(s.Revision+1).ToString(CultureInfo.InvariantCulture)+"."+s.SpellSaves.Length.ToString(CultureInfo.InvariantCulture);
            var save=new SpellSaveRecord(id,SpellSaveKind.ConcentrationConstitution,concentration.Id,target,cause,s.Revision+1,s.RuleClock,
                null,damage,dc,modifier,roll.First,roll.Second??0,roll.Natural,success,random,roll.NextRandomState,roll.WordsConsumed);
            s.RandomState=roll.NextRandomState; s.SpellSaves=s.SpellSaves.Append(save).ToArray();
            if(!success)EndSpellEffect(s,concentration,cause,s.Revision+1,s.RuleClock,SpellEffectEndReason.DamageSaveFailed);
        }
    }
}
#endif
