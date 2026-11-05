using System;
using System.Linq;
using System.Collections.ObjectModel;

namespace Decennium.Foundation
{
    /// <summary>Persistent custody and physical magazine state for the authored Repeating heavy crossbow.</summary>
    public sealed class RepeatingCrossbowRecord
    {
        private readonly string[] loadedBoltLots;
        public string Id { get; }
        public string ProfileId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public string HeldBy { get; }
        public int GripHands { get; }
        public int CellX { get; }
        public int CellY { get; }
        public ReadOnlyCollection<string> LoadedBoltLots { get; }
        public RepeatingCrossbowRecord(string id,string profileId,string ownerId,string custodianId,string heldBy,int gripHands,
            int cellX,int cellY,string[] loadedBoltLots=null)
        {
            var loaded=loadedBoltLots??Array.Empty<string>();
            if(!Validation.ValidId(id)||!Validation.ValidId(profileId)||!Validation.ValidId(ownerId)||!Validation.ValidId(custodianId)
                ||heldBy==null||heldBy!=""&&!Validation.ValidId(heldBy)||heldBy==""&&gripHands!=0||heldBy!=""&&(gripHands<1||gripHands>2)
                ||loaded.Length>5||loaded.Any(x=>!Validation.ValidId(x)))throw new ArgumentException("Invalid repeating crossbow state.");
            Id=id;ProfileId=profileId;OwnerId=ownerId;CustodianId=custodianId;HeldBy=heldBy;GripHands=gripHands;CellX=cellX;CellY=cellY;
            this.loadedBoltLots=loaded.ToArray();LoadedBoltLots=Array.AsReadOnly(this.loadedBoltLots);
        }
        public RepeatingCrossbowRecord WithMagazine(string[] lots)=>new RepeatingCrossbowRecord(Id,ProfileId,OwnerId,CustodianId,HeldBy,GripHands,CellX,CellY,lots);
        public RepeatingCrossbowRecord WithGrip(int hands)=>new RepeatingCrossbowRecord(Id,ProfileId,OwnerId,CustodianId,HeldBy,hands,CellX,CellY,loadedBoltLots);
        public RepeatingCrossbowRecord DropAt(int x,int y)=>new RepeatingCrossbowRecord(Id,ProfileId,OwnerId,CustodianId,"",0,x,y,loadedBoltLots);
        public bool SameAs(RepeatingCrossbowRecord x)=>x!=null&&Id==x.Id&&ProfileId==x.ProfileId&&OwnerId==x.OwnerId&&CustodianId==x.CustodianId
            &&HeldBy==x.HeldBy&&GripHands==x.GripHands&&CellX==x.CellX&&CellY==x.CellY&&LoadedBoltLots.SequenceEqual(x.LoadedBoltLots);
    }

    /// <summary>One finite source ammunition bundle. Available units are on the carrier; loaded and
    /// expended units are accounted for by magazine and attack records, respectively.</summary>
    public sealed class AmmunitionLotRecord
    {
        public string Id { get; }
        public string ProfileId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public int OriginalQuantity { get; }
        public int AvailableQuantity { get; }
        public bool Accessible { get; }
        public AmmunitionLotRecord(string id,string profileId,string ownerId,string custodianId,int originalQuantity,int availableQuantity,bool accessible)
        {
            if(!Validation.ValidId(id)||profileId!="ammunition.crossbow-bolts-20"||!Validation.ValidId(ownerId)||!Validation.ValidId(custodianId)
                ||originalQuantity<1||originalQuantity>20||availableQuantity<0||availableQuantity>originalQuantity)
                throw new ArgumentException("Invalid ammunition provenance or quantity.");
            Id=id;ProfileId=profileId;OwnerId=ownerId;CustodianId=custodianId;OriginalQuantity=originalQuantity;
            AvailableQuantity=availableQuantity;Accessible=accessible;
        }
        public AmmunitionLotRecord WithAvailable(int amount)=>new AmmunitionLotRecord(Id,ProfileId,OwnerId,CustodianId,OriginalQuantity,amount,Accessible);
        public bool SameAs(AmmunitionLotRecord x)=>x!=null&&Id==x.Id&&ProfileId==x.ProfileId&&OwnerId==x.OwnerId&&CustodianId==x.CustodianId
            &&OriginalQuantity==x.OriginalQuantity&&AvailableQuantity==x.AvailableQuantity&&Accessible==x.Accessible;
    }

    /// <summary>Explicit TEST_ONLY numerical/training facts; this is not inferred from possession or a class label.</summary>
    public sealed class RangedCombatantRecord
    {
        public string ActorId { get; }
        public int DexterityScore { get; }
        public int ProficiencyBonus { get; }
        public bool CrossbowProficient { get; }
        public string TrainingId { get; }
        public RangedCombatantRecord(string actorId,int dexterityScore,int proficiencyBonus,bool crossbowProficient,string trainingId="")
        {
            if(!Validation.ValidId(actorId)||dexterityScore<1||dexterityScore>30||proficiencyBonus<0||proficiencyBonus>10||trainingId==null
                ||crossbowProficient&&!Validation.ValidId(trainingId)||!crossbowProficient&&trainingId!="")throw new ArgumentException("Invalid ranged combatant facts.");
            ActorId=actorId;DexterityScore=dexterityScore;ProficiencyBonus=proficiencyBonus;CrossbowProficient=crossbowProficient;TrainingId=trainingId;
        }
        public bool SameAs(RangedCombatantRecord x)=>x!=null&&ActorId==x.ActorId&&DexterityScore==x.DexterityScore&&ProficiencyBonus==x.ProficiencyBonus
            &&CrossbowProficient==x.CrossbowProficient&&TrainingId==x.TrainingId;
    }

    public sealed class RangedDamageRoll
    {
        private readonly int[] dice;
        public ReadOnlyCollection<int> Dice { get; }
        public int FlatModifier { get; }
        public long Total { get; }
        public long AfterDefense { get; }
        public long DiceWords { get; }
        public uint EffectsSeed { get; }
        public uint FinalRandom { get; }
        public long EffectsWords { get; }
        public int WoundNatural { get; }
        public int InjuryD6 { get; }
        public int StableD4 { get; }
        public RangedDamageRoll(int[] dice,int flatModifier,long total,long afterDefense,long diceWords,uint effectsSeed,uint finalRandom,long effectsWords,
            int woundNatural,int injuryD6,int stableD4)
        {
            if(dice==null||dice.Length>2||dice.Any(x=>x<1||x>10)||flatModifier< -100||flatModifier>100||total<0||diceWords<0
                ||afterDefense<0||afterDefense>total||effectsSeed==0||finalRandom==0||effectsWords<0||woundNatural<0||woundNatural>20||injuryD6<0||injuryD6>6||stableD4<0||stableD4>4
                ||total!=Math.Max(0L,dice.Sum(x=>(long)x)+flatModifier))throw new ArgumentException("Invalid ranged damage record.");
            this.dice=(int[])dice.Clone();Dice=Array.AsReadOnly(this.dice);FlatModifier=flatModifier;Total=total;AfterDefense=afterDefense;DiceWords=diceWords;
            EffectsSeed=effectsSeed;FinalRandom=finalRandom;EffectsWords=effectsWords;WoundNatural=woundNatural;InjuryD6=injuryD6;StableD4=stableD4;
        }
        public bool SameAs(RangedDamageRoll x)=>x!=null&&Dice.SequenceEqual(x.Dice)&&FlatModifier==x.FlatModifier&&Total==x.Total&&AfterDefense==x.AfterDefense&&DiceWords==x.DiceWords
            &&EffectsSeed==x.EffectsSeed&&FinalRandom==x.FinalRandom&&EffectsWords==x.EffectsWords&&WoundNatural==x.WoundNatural&&InjuryD6==x.InjuryD6&&StableD4==x.StableD4;
    }

    /// <summary>Settled ordinary ranged attack. A miss still records and spends its actual bolt.</summary>
    public sealed class RangedAttackRecord
    {
        public string Id { get; }
        public long Revision { get; }
        public int TurnOrdinal { get; }
        public string AttackerId { get; }
        public string TargetId { get; }
        public string WeaponId { get; }
        public string AmmunitionLotId { get; }
        public RuleTime At { get; }
        public CombatAttackRoll Attack { get; }
        public RangedDamageRoll Damage { get; }
        public RangedAttackRecord(string id,long revision,int turnOrdinal,string attackerId,string targetId,string weaponId,string ammunitionLotId,
            RuleTime at,CombatAttackRoll attack,RangedDamageRoll damage)
        {
            if(!Validation.ValidId(id)||revision<1||turnOrdinal<0||!Validation.ValidId(attackerId)||!Validation.ValidId(targetId)||attackerId==targetId
                ||!Validation.ValidId(weaponId)||!Validation.ValidId(ammunitionLotId)||attack==null||damage==null
                ||attack.Hit&&damage.Dice.Count!=(attack.Critical?2:1)||!attack.Hit&&damage.Dice.Count!=0)
                throw new ArgumentException("Invalid ranged attack result.");
            Id=id;Revision=revision;TurnOrdinal=turnOrdinal;AttackerId=attackerId;TargetId=targetId;WeaponId=weaponId;AmmunitionLotId=ammunitionLotId;At=at;Attack=attack;Damage=damage;
        }
        public bool SameAs(RangedAttackRecord x)=>x!=null&&Id==x.Id&&Revision==x.Revision&&TurnOrdinal==x.TurnOrdinal&&AttackerId==x.AttackerId
            &&TargetId==x.TargetId&&WeaponId==x.WeaponId&&AmmunitionLotId==x.AmmunitionLotId&&At==x.At&&Attack.SameAs(x.Attack)&&Damage.SameAs(x.Damage);
    }

    public static class RangedCombatValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.RepeatingCrossbows==null||s.AmmunitionLots==null||s.RangedCombatants==null||s.RangedAttacks==null
                ||s.SuppressionFireVolleys==null
                ||s.RepeatingCrossbows.Length>64||s.AmmunitionLots.Length>128||s.RangedCombatants.Length>64||s.RangedAttacks.Length>128
                ||s.RepeatingCrossbows.Any(x=>x==null)||s.AmmunitionLots.Any(x=>x==null)||s.RangedCombatants.Any(x=>x==null)||s.RangedAttacks.Any(x=>x==null))
                throw new ArgumentException("Invalid ranged combat collections.");
            if(s.SchemaVersion<Snapshot.RepeatingCrossbowSchema) {
                if(s.RepeatingCrossbows.Length+s.AmmunitionLots.Length+s.RangedCombatants.Length+s.RangedAttacks.Length!=0)
                    throw new ArgumentException("Ranged combat requires schema22.");
                return;
            }
            bool Actor(string id)=>s.Actors.Any(x=>x.Id==id);
            if(s.RepeatingCrossbows.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.RepeatingCrossbows.Length
                ||s.AmmunitionLots.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.AmmunitionLots.Length
                ||s.RangedCombatants.Select(x=>x.ActorId).Distinct(StringComparer.Ordinal).Count()!=s.RangedCombatants.Length
                ||s.RangedAttacks.Select(x=>x.Id).Distinct(StringComparer.Ordinal).Count()!=s.RangedAttacks.Length
                ||s.RangedAttacks.Select(x=>x.Revision).Distinct().Count()!=s.RangedAttacks.Length
                ||s.RepeatingCrossbows.Any(x=>x.ProfileId!="new.repeating-heavy-crossbow"||!Actor(x.OwnerId)||!Actor(x.CustodianId)
                    ||x.HeldBy!=""&&(!Actor(x.HeldBy)||x.CustodianId!=x.HeldBy||!s.Lives.Single(l=>l.ActorId==x.HeldBy).HeldItems.Contains(x.Id))
                    ||x.HeldBy==""&&s.Lives.Any(l=>l.HeldItems.Contains(x.Id))
                    ||x.LoadedBoltLots.Any(id=>!s.AmmunitionLots.Any(a=>a.Id==id)))
                ||s.AmmunitionLots.Any(x=>!Actor(x.OwnerId)||!Actor(x.CustodianId))
                ||s.RangedCombatants.Any(x=>!Actor(x.ActorId)||!s.Characters.Any(c=>c.ActorId==x.ActorId&&c.Abilities[1]==x.DexterityScore))
                ||s.RangedAttacks.Any(x=>!Actor(x.AttackerId)||!Actor(x.TargetId)||x.Revision>s.Revision||x.At>s.RuleClock
                    ||!s.RepeatingCrossbows.Any(w=>w.Id==x.WeaponId)||!s.AmmunitionLots.Any(a=>a.Id==x.AmmunitionLotId)
                    ||!s.RangedCombatants.Any(a=>a.ActorId==x.AttackerId)
                    ||EncounterHistory.AtRevision(s,x.Revision)==null||!EncounterHistory.InCurrent(s,x.Revision)))
                throw new ArgumentException("Invalid ranged combat references.");
            foreach(var lot in s.AmmunitionLots) {
                int loaded=s.RepeatingCrossbows.Sum(w=>w.LoadedBoltLots.Count(id=>id==lot.Id));
                int spent=s.RangedAttacks.Count(a=>a.AmmunitionLotId==lot.Id);
                if(s.SchemaVersion>=Snapshot.SuppressionFireSchema)
                    spent=checked(spent+s.SuppressionFireVolleys.Sum(v=>v.AmmunitionLotIds.Count(id=>id==lot.Id)));
                if(checked(lot.AvailableQuantity+loaded+spent)!=lot.OriginalQuantity)throw new ArgumentException("Ammunition provenance is not conserved.");
            }
        }
    }
}
