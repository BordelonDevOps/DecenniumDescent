#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;

namespace Decennium.Foundation.Laboratory
{
    public enum MagazineReloadStatus { Loaded, NoFreeLoadingHand, NoCarriedBolts, MagazineFull }

    public sealed class MagazineReloadResult
    {
        public MagazineReloadStatus Status { get; }
        public RepeatingFiveMagazine Magazine { get; }
        public int CarriedBoltsRemaining { get; }
        public int BoltsLoaded { get; }
        internal MagazineReloadResult(MagazineReloadStatus status,RepeatingFiveMagazine magazine,int carriedRemaining,int loaded)
        {Status=status;Magazine=magazine;CarriedBoltsRemaining=carriedRemaining;BoltsLoaded=loaded;}
    }

    /// <summary>Immutable ammunition state for the source-defined Repeating 5 profile. Loading costs
    /// an Action in its caller; this value object moves only actual bolts between carried inventory
    /// and the five-bolt weapon magazine.</summary>
    public sealed class RepeatingFiveMagazine
    {
        public const int Capacity=5;
        public int LoadedBolts { get; }
        public bool CanFire=>LoadedBolts>0;

        public RepeatingFiveMagazine(int loadedBolts=0)
        {
            if(loadedBolts<0||loadedBolts>Capacity)throw new ArgumentOutOfRangeException(nameof(loadedBolts));
            LoadedBolts=loadedBolts;
        }

        /// <summary>One bolt is spent for each attack attempt, independent of its hit result.</summary>
        public bool TrySpendForAttack(out RepeatingFiveMagazine remaining)
        {
            if(LoadedBolts==0){remaining=this;return false;}
            remaining=new RepeatingFiveMagazine(LoadedBolts-1);return true;
        }

        /// <summary>Models the source-defined transfer of up to the free capacity from carried bolts.
        /// The tactical caller must separately validate and spend the required Action.</summary>
        public MagazineReloadResult Reload(int carriedBolts,bool hasFreeLoadingHand)
        {
            if(carriedBolts<0)throw new ArgumentOutOfRangeException(nameof(carriedBolts));
            if(!hasFreeLoadingHand)return new MagazineReloadResult(MagazineReloadStatus.NoFreeLoadingHand,this,carriedBolts,0);
            if(LoadedBolts==Capacity)return new MagazineReloadResult(MagazineReloadStatus.MagazineFull,this,carriedBolts,0);
            if(carriedBolts==0)return new MagazineReloadResult(MagazineReloadStatus.NoCarriedBolts,this,0,0);
            int loaded=Math.Min(Capacity-LoadedBolts,carriedBolts);
            return new MagazineReloadResult(MagazineReloadStatus.Loaded,new RepeatingFiveMagazine(LoadedBolts+loaded),carriedBolts-loaded,loaded);
        }
    }
}
#endif
