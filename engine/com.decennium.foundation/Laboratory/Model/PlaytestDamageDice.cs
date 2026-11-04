#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public enum KnockoutInstruction { OrdinaryOutcome, KnockOutIfEligible, AskIfEligible }

    /// <summary>Immutable result or continuation. A pending choice exposes no final life outcome.</summary>
    public sealed class RolledDamage
    {
        public uint InitialRandomState { get; }
        public uint NextRandomState { get; }
        public long WordsConsumed { get; }
        public D20Roll WoundRoll { get; }
        public int? InjuryD6 { get; }
        public int? StableD4 { get; }
        public DamageResolution Outcome { get; }
        public PendingKnockout Pending { get; }
        internal RolledDamage(uint initial,uint next,long words,D20Roll wound,int? injury,int? stable,DamageResolution outcome,PendingKnockout pending)
        {InitialRandomState=initial;NextRandomState=next;WordsConsumed=words;WoundRoll=wound;InjuryD6=injury;StableD4=stable;Outcome=outcome;Pending=pending;}
    }
    /// <summary>Post-damage eligibility decision belongs to the attacker. Inputs and rolled Wound results
    /// are retained; choosing neither charges an Action nor rerolls prior dice. The host must persist/gate it.</summary>
    public sealed class PendingKnockout
    {
        public LifeState Before { get; }
        public long ResolvedDamage { get; }
        public RuleTime At { get; }
        public int ConstitutionSaveModifier { get; }
        public bool Critical { get; }
        public bool Maiming { get; }
        public uint InitialRandomState { get; }
        public uint NextRandomState { get; }
        public long WordsConsumed { get; }
        public D20Roll WoundRoll { get; }
        public int? InjuryD6 { get; }
        internal PendingKnockout(LifeState before,long damage,RuleTime at,int con,bool critical,bool maiming,
            uint initial,uint next,long words,D20Roll wound,int? injury)
        {Before=before;ResolvedDamage=damage;At=at;ConstitutionSaveModifier=con;Critical=critical;Maiming=maiming;
            InitialRandomState=initial;NextRandomState=next;WordsConsumed=words;WoundRoll=wound;InjuryD6=injury;}
        public RolledDamage Complete(bool knockOut)
            =>PlaytestDamageDice.Finish(Before,ResolvedDamage,At,ConstitutionSaveModifier,Critical,Maiming,
                InitialRandomState,NextRandomState,WordsConsumed,WoundRoll,InjuryD6,knockOut);
    }
    /// <summary>Ordinary post-defense damage with a normal Wound d20 and no prevention/replacement features.
    /// Caller establishes legal damage, melee classification and all feature windows. No attack or Action is granted.</summary>
    public static class PlaytestDamageDice
    {
        public static RolledDamage Resolve(LifeState before,long resolvedDamage,RuleTime at,uint randomState,
            int constitutionSaveModifier=0,bool critical=false,bool maiming=false,bool melee=false,
            KnockoutInstruction knockout=KnockoutInstruction.OrdinaryOutcome)
        {
            if(before==null||before.Dead||resolvedDamage<0||randomState==0||!Enum.IsDefined(typeof(KnockoutInstruction),knockout)
                ||!melee&&knockout!=KnockoutInstruction.OrdinaryOutcome)throw new ArgumentException("Invalid ordinary damage input.");
            long post=resolvedDamage-Math.Min(before.TemporaryHp,resolvedDamage);
            long hp=Math.Max(0,before.Hp-post);
            bool instant=hp==0&&post-before.Hp>=before.MaximumHp;
            bool woundNeeded=!instant&&(before.Hp>0&&hp==0||post>=before.MaximumHp/2+before.MaximumHp%2||maiming);
            uint next=randomState;long words=0;D20Roll wound=null;int? injury=null;
            if(woundNeeded) {
                wound=PlaytestDice.RollD20(next);next=wound.NextRandomState;words=wound.WordsConsumed;
                long dc=Math.Max(10,post/2),total=(long)wound.Natural+constitutionSaveModifier-before.Wounds.Count;
                if(before.Wounds.Count<3&&total<dc&&dc-total>=5) {
                    var draw=DiceStream.Draw(next,6);injury=draw.Value+1;next=draw.NextState;words=checked(words+draw.WordsConsumed);
                }
            }
            // Reuse the established life procedure to resolve instant/fatal Wound branches before offering a choice.
            var ordinary=PlaytestLife.DamageAt(before,resolvedDamage,at,constitutionSaveModifier,wound?.Natural,injury,critical,maiming);
            bool fatalWound=ordinary.WoundTotal.HasValue&&ordinary.WoundTotal<ordinary.WoundDc&&before.Wounds.Count==3;
            bool eligible=melee&&before.Hp>0&&ordinary.State.Hp==0&&!ordinary.InstantDeath&&!fatalWound;
            if(eligible&&knockout==KnockoutInstruction.AskIfEligible) {
                var pending=new PendingKnockout(before,resolvedDamage,at,constitutionSaveModifier,critical,maiming,
                    randomState,next,words,wound,injury);
                return new RolledDamage(randomState,next,words,wound,injury,null,null,pending);
            }
            if(eligible&&knockout==KnockoutInstruction.KnockOutIfEligible)
                return Finish(before,resolvedDamage,at,constitutionSaveModifier,critical,maiming,randomState,next,words,wound,injury,true);
            return new RolledDamage(randomState,next,words,wound,injury,null,ordinary,null);
        }
        internal static RolledDamage Finish(LifeState before,long damage,RuleTime at,int con,bool critical,bool maiming,
            uint initial,uint next,long words,D20Roll wound,int? injury,bool knockOut)
        {
            int? stable=null;
            if(knockOut) {var draw=DiceStream.Draw(next,4);stable=draw.Value+1;next=draw.NextState;words=checked(words+draw.WordsConsumed);}
            var outcome=PlaytestLife.DamageAt(before,damage,at,con,wound?.Natural,injury,critical,maiming,knockOut,true,stable);
            return new RolledDamage(initial,next,words,wound,injury,stable,outcome,null);
        }
    }
    /// <summary>Owner-adopted prototype ordinary unarmored baseline, 2026-11-03. Other formulas/modifiers are separate.</summary>
    public static class PrototypeArmor
    {
        public static long UnarmoredBaseAc(int dexterity)=>10L+PlaytestCharacters.AbilityModifier(dexterity);
    }
}
#endif
