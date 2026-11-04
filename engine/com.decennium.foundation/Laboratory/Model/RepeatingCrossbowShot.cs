#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;

namespace Decennium.Foundation.Laboratory
{
    public enum RepeatingCrossbowShotFailure
    {
        None,
        NoAmmunition,
        WrongWeaponRangeProfile,
        UnknownTargetLocation,
        BlockedLineOfFire,
        TotalCover,
        OutOfRange
    }

    public sealed class RepeatingCrossbowShotResult
    {
        private readonly int[] damageDice;
        public bool Legal=>Failure==RepeatingCrossbowShotFailure.None;
        public bool Attempted { get; }
        public RepeatingCrossbowShotFailure Failure { get; }
        public RangedAttackResolution Attack { get; }
        public RepeatingFiveMagazine MagazineAfter { get; }
        public int CarriedBoltsAfter { get; }
        public IReadOnlyList<int> DamageDice { get; }
        public int DamageModifier { get; }
        public long RolledDamageBeforeDefense { get; }
        public string DamageType=>"piercing";
        public uint RandomStateAfter { get; }
        public long RandomWordsConsumed { get; }

        internal RepeatingCrossbowShotResult(RepeatingCrossbowShotFailure failure,uint initialState,
            RepeatingFiveMagazine magazine,int carriedBolts)
        {
            Failure=failure;RandomStateAfter=initialState;MagazineAfter=magazine;CarriedBoltsAfter=carriedBolts;
            damageDice=Array.Empty<int>();DamageDice=Array.AsReadOnly(damageDice);
        }
        internal RepeatingCrossbowShotResult(RangedAttackResolution attack,RepeatingFiveMagazine magazine,int carriedBolts,
            int damageModifier,int[] dice,long rolledDamage,uint randomStateAfter,long words)
        {
            Failure=RepeatingCrossbowShotFailure.None;Attempted=true;Attack=attack;MagazineAfter=magazine;
            CarriedBoltsAfter=carriedBolts;damageDice=(int[])dice.Clone();DamageDice=Array.AsReadOnly(damageDice);
            DamageModifier=damageModifier;
            RolledDamageBeforeDefense=rolledDamage;RandomStateAfter=randomStateAfter;RandomWordsConsumed=words;
        }
    }

    /// <summary>Atomic pure calculation for one source-profile Repeating heavy crossbow attack attempt:
    /// pre-roll legality, one magazine bolt, deterministic attack roll, and on-hit d10 damage dice.</summary>
    public static class RepeatingCrossbowShotRules
    {
        public const long NormalRangeFeet=80;
        public const long MaximumRangeFeet=320;
        public const int DamageDieSides=10;

        public static RepeatingCrossbowShotResult Resolve(uint initialRandomState,RangedAttackRequest request,
            RepeatingFiveMagazine magazine,int carriedBolts)
        {
            if(magazine==null)throw new ArgumentNullException(nameof(magazine));
            if(carriedBolts<0)throw new ArgumentOutOfRangeException(nameof(carriedBolts));
            if(request.NormalRangeFeet!=NormalRangeFeet||request.MaximumRangeFeet!=MaximumRangeFeet)
                return new RepeatingCrossbowShotResult(RepeatingCrossbowShotFailure.WrongWeaponRangeProfile,initialRandomState,magazine,carriedBolts);
            if(!magazine.CanFire)
                return new RepeatingCrossbowShotResult(RepeatingCrossbowShotFailure.NoAmmunition,initialRandomState,magazine,carriedBolts);

            var attack=RangedAttackRules.Resolve(initialRandomState,request);
            if(!attack.Legal) {
                var failure=attack.Failure==RangedAttackFailure.UnknownTargetLocation?RepeatingCrossbowShotFailure.UnknownTargetLocation
                    :attack.Failure==RangedAttackFailure.BlockedLineOfFire?RepeatingCrossbowShotFailure.BlockedLineOfFire
                    :attack.Failure==RangedAttackFailure.TotalCover?RepeatingCrossbowShotFailure.TotalCover:RepeatingCrossbowShotFailure.OutOfRange;
                return new RepeatingCrossbowShotResult(failure,initialRandomState,magazine,carriedBolts);
            }

            if(!magazine.TrySpendForAttack(out var after))throw new InvalidOperationException("A validated loaded magazine failed to spend its bolt.");
            if(!attack.Attack.Hit)
                return new RepeatingCrossbowShotResult(attack,after,carriedBolts,request.DexterityModifier,Array.Empty<int>(),0,
                    attack.RandomStateAfter,attack.Roll.WordsConsumed);

            int count=attack.Critical?2:1;var dice=new int[count];uint next=attack.RandomStateAfter;long words=attack.Roll.WordsConsumed;
            for(int i=0;i<count;i++){var draw=DiceStream.Draw(next,DamageDieSides);dice[i]=draw.Value+1;next=draw.NextState;words=checked(words+draw.WordsConsumed);}
            long damage=request.DexterityModifier;foreach(int die in dice)damage=checked(damage+die);damage=Math.Max(0,damage);
            return new RepeatingCrossbowShotResult(attack,after,carriedBolts,request.DexterityModifier,dice,damage,next,words);
        }
    }
}
#endif
