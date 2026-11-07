using System;
using System.Collections.Generic;
using System.Linq;
using System.Globalization;

namespace Decennium.Foundation
{
    public enum CombatStance { Aggressive=1, Guarded, Mobile, Focused, Carrying }
    public enum AttackKnockoutMode { OrdinaryOutcome, KnockOutIfEligible, AskIfEligible }
    public enum PressHitInstruction { ArmOrReplace, KeepExisting }
    /// <summary>Exact command inputs for one ordinary Repeating heavy crossbow attack or reload.
    /// Attack uses an empty AmmoLotId and zero Amount; reload names one actual carried lot.</summary>
    public sealed class RangedRequest
    {
        public string TurnId { get; }
        public string WeaponId { get; }
        public string AmmoLotId { get; }
        public int Amount { get; }
        public RangedRequest(string turnId,string weaponId,string ammoLotId="",int amount=0)
        {
            if(!Validation.ValidId(turnId)||!Validation.ValidId(weaponId)||ammoLotId==null||ammoLotId!=""&&!Validation.ValidId(ammoLotId)||amount<0||amount>20)
                throw new ArgumentException("Invalid ranged request.");
            TurnId=turnId;WeaponId=weaponId;AmmoLotId=ammoLotId;Amount=amount;
        }
        internal string Fingerprint=>TurnId+"|"+WeaponId+"|"+AmmoLotId+"|"+Amount.ToString(CultureInfo.InvariantCulture);
    }
    public sealed class CombatRequest
    {
        public string TurnId { get; }
        public string WeaponId { get; }
        public int Stance { get; }
        public AttackKnockoutMode Knockout { get; }
        public bool Choice { get; }
        public PressHitInstruction PressInstruction { get; }
        public CombatRequest(string turnId,string weaponId="",int stance=0,AttackKnockoutMode knockout=AttackKnockoutMode.OrdinaryOutcome,bool choice=false,PressHitInstruction pressInstruction=PressHitInstruction.ArmOrReplace)
        {
            if(!Validation.ValidId(turnId)||weaponId==null||weaponId!=""&&!Validation.ValidId(weaponId)||stance<0||stance>5
                ||!Enum.IsDefined(typeof(AttackKnockoutMode),knockout)||!Enum.IsDefined(typeof(PressHitInstruction),pressInstruction))throw new ArgumentException("Invalid combat request.");
            TurnId=turnId;WeaponId=weaponId;Stance=stance;Knockout=knockout;Choice=choice;PressInstruction=pressInstruction;
        }
        internal string FingerprintVersion=>PressInstruction==PressHitInstruction.ArmOrReplace?"combat-v1":"combat-v2";
        internal string Fingerprint=>TurnId+"|"+WeaponId+"|"+Stance.ToString(CultureInfo.InvariantCulture)+"|"+((int)Knockout).ToString(CultureInfo.InvariantCulture)+"|"+(Choice?"1":"0")+(PressInstruction==PressHitInstruction.ArmOrReplace?"":"|1");
    }
    public sealed class ClubInstance
    {
        public string Id { get; }
        public string ProfileId { get; }
        public string OwnerId { get; }
        public string CustodianId { get; }
        public string HeldBy { get; }
        public int CellX { get; }
        public int CellY { get; }
        public ClubInstance(string id,string profile,string owner,string custodian,string heldBy,int x,int y)
        {
            if(new[]{id,profile,owner,custodian}.Any(s=>!Validation.ValidId(s))||heldBy==null||heldBy!=""&&!Validation.ValidId(heldBy))throw new ArgumentException("Invalid physical club.");
            Id=id;ProfileId=profile;OwnerId=owner;CustodianId=custodian;HeldBy=heldBy;CellX=x;CellY=y;
        }
        public bool SameAs(ClubInstance x)=>x!=null&&Id==x.Id&&ProfileId==x.ProfileId&&OwnerId==x.OwnerId&&CustodianId==x.CustodianId&&HeldBy==x.HeldBy&&CellX==x.CellX&&CellY==x.CellY;
    }
    public sealed class StanceSelectionRecord
    {
        public string ActorId { get; }
        public long Revision { get; }
        public int TurnOrdinal { get; }
        public CombatStance Kind { get; }
        public RuleTime ExpiresAt { get; }
        public StanceSelectionRecord(string actor,long revision,int ordinal,CombatStance kind,RuleTime expires)
        {
            if(!Validation.ValidId(actor)||revision<1||ordinal<0||!Enum.IsDefined(typeof(CombatStance),kind))throw new ArgumentException("Invalid stance selection.");
            ActorId=actor;Revision=revision;TurnOrdinal=ordinal;Kind=kind;ExpiresAt=expires;
        }
        public bool SameAs(StanceSelectionRecord x)=>x!=null&&ActorId==x.ActorId&&Revision==x.Revision&&TurnOrdinal==x.TurnOrdinal&&Kind==x.Kind&&ExpiresAt==x.ExpiresAt;
    }
    /// <summary>One ordinary Dodge Action, lasting until the actor's next regular start.</summary>
    public sealed class DodgeRecord
    {
        public string ActorId { get; }
        public long Revision { get; }
        public int TurnOrdinal { get; }
        public RuleTime ExpiresAt { get; }
        public DodgeRecord(string actorId,long revision,int turnOrdinal,RuleTime expiresAt)
        {
            if(!Validation.ValidId(actorId)||revision<1||turnOrdinal<0)throw new ArgumentException("Invalid Dodge record.");
            ActorId=actorId;Revision=revision;TurnOrdinal=turnOrdinal;ExpiresAt=expiresAt;
        }
        public bool SameAs(DodgeRecord x)=>x!=null&&ActorId==x.ActorId&&Revision==x.Revision&&TurnOrdinal==x.TurnOrdinal&&ExpiresAt==x.ExpiresAt;
    }
    public sealed class CombatAttackRoll
    {
        public int First { get; }
        public int Second { get; }
        public int Selected { get; }
        public int Modifier { get; }
        public int ArmorClass { get; }
        public bool Hit { get; }
        public bool Critical { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long Words { get; }
        public CombatAttackRoll(int first,int second,int selected,int modifier,int ac,bool hit,bool critical,uint before,uint after,long words)
        {
            if(first<1||first>20||second<0||second>20||selected<1||selected>20||ac<0||critical&&!hit||before==0||after==0||words<1)throw new ArgumentException("Invalid recorded attack roll.");
            First=first;Second=second;Selected=selected;Modifier=modifier;ArmorClass=ac;Hit=hit;Critical=critical;RandomBefore=before;RandomAfter=after;Words=words;
        }
        public bool SameAs(CombatAttackRoll x)=>x!=null&&First==x.First&&Second==x.Second&&Selected==x.Selected&&Modifier==x.Modifier&&ArmorClass==x.ArmorClass
            &&Hit==x.Hit&&Critical==x.Critical&&RandomBefore==x.RandomBefore&&RandomAfter==x.RandomAfter&&Words==x.Words;
    }
    public sealed class CombatDamageRoll
    {
        public IReadOnlyList<int> Dice { get; }
        public long Total { get; }
        public long DiceWords { get; }
        public uint EffectsSeed { get; }
        public uint FinalRandom { get; }
        public long EffectsWords { get; }
        public int WoundNatural { get; }
        public int InjuryD6 { get; }
        public int StableD4 { get; }
        public CombatDamageRoll(IEnumerable<int> dice,long total,long diceWords,uint effectsSeed,uint finalRandom,long effectsWords,int woundNatural,int injuryD6,int stableD4)
        {
            if(dice==null||total<0||diceWords<0||effectsSeed==0||finalRandom==0||effectsWords<0||woundNatural<0||woundNatural>20||injuryD6<0||injuryD6>6||stableD4<0||stableD4>4)
                throw new ArgumentException("Invalid recorded damage roll.");
            var d=dice.ToArray();if(d.Length>2||d.Any(n=>n<1||n>4))throw new ArgumentException("Invalid club damage dice.");
            Dice=Array.AsReadOnly(d);Total=total;DiceWords=diceWords;EffectsSeed=effectsSeed;FinalRandom=finalRandom;EffectsWords=effectsWords;WoundNatural=woundNatural;InjuryD6=injuryD6;StableD4=stableD4;
        }
        public bool SameAs(CombatDamageRoll x)=>x!=null&&Dice.SequenceEqual(x.Dice)&&Total==x.Total&&DiceWords==x.DiceWords&&EffectsSeed==x.EffectsSeed&&FinalRandom==x.FinalRandom
            &&EffectsWords==x.EffectsWords&&WoundNatural==x.WoundNatural&&InjuryD6==x.InjuryD6&&StableD4==x.StableD4;
    }
    public sealed class MeleeAttackRecord
    {
        public string Id { get; }
        public long Revision { get; }
        public long ResolvedRevision { get; }
        public int TurnOrdinal { get; }
        public string AttackerId { get; }
        public string TargetId { get; }
        public string WeaponId { get; }
        public RuleTime At { get; }
        public AttackKnockoutMode Instruction { get; }
        public CombatAttackRoll Attack { get; }
        public CombatDamageRoll Damage { get; }
        public bool Pending=>ResolvedRevision==0;
        public bool Opportunity { get; }
        public PressHitInstruction PressInstruction { get; }
        public MeleeAttackRecord(string id,long revision,long resolvedRevision,int ordinal,string actor,string target,string weapon,RuleTime at,
            AttackKnockoutMode instruction,CombatAttackRoll attack,CombatDamageRoll damage,bool opportunity=false,PressHitInstruction pressInstruction=PressHitInstruction.ArmOrReplace)
        {
            if(new[]{id,actor,target,weapon}.Any(s=>!Validation.ValidId(s))||revision<1||resolvedRevision<0||resolvedRevision!=0&&resolvedRevision<revision||ordinal<0
                ||!Enum.IsDefined(typeof(AttackKnockoutMode),instruction)||!Enum.IsDefined(typeof(PressHitInstruction),pressInstruction)||attack==null||damage==null)throw new ArgumentException("Invalid melee attack record.");
            Id=id;Revision=revision;ResolvedRevision=resolvedRevision;TurnOrdinal=ordinal;AttackerId=actor;TargetId=target;WeaponId=weapon;At=at;Instruction=instruction;Attack=attack;Damage=damage;Opportunity=opportunity;PressInstruction=pressInstruction;
        }
        public bool SameAs(MeleeAttackRecord x)=>x!=null&&Id==x.Id&&Revision==x.Revision&&ResolvedRevision==x.ResolvedRevision&&TurnOrdinal==x.TurnOrdinal
            &&AttackerId==x.AttackerId&&TargetId==x.TargetId&&WeaponId==x.WeaponId&&At==x.At&&Instruction==x.Instruction&&Attack.SameAs(x.Attack)&&Damage.SameAs(x.Damage)&&Opportunity==x.Opportunity&&PressInstruction==x.PressInstruction;
    }
    public sealed class PressRecord
    {
        public string ActorId { get; }
        public string TargetId { get; }
        public long ArmedRevision { get; }
        public RuleTime ExpiresAt { get; }
        public PressRecord(string actor,string target,long revision,RuleTime expires)
        {
            if(!Validation.ValidId(actor)||!Validation.ValidId(target)||revision<1)throw new ArgumentException("Invalid Press record.");
            ActorId=actor;TargetId=target;ArmedRevision=revision;ExpiresAt=expires;
        }
        public bool SameAs(PressRecord x)=>x!=null&&ActorId==x.ActorId&&TargetId==x.TargetId&&ArmedRevision==x.ArmedRevision&&ExpiresAt==x.ExpiresAt;
    }
    public static class ClubAttackValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.Clubs==null||s.Stances==null||s.Dodges==null||s.MeleeAttacks==null||s.Presses==null||s.Clubs.Length>64||s.Stances.Length>128||s.Dodges.Length>128||s.MeleeAttacks.Length>128||s.Presses.Length>64
                ||s.Clubs.Any(x=>x==null)||s.Stances.Any(x=>x==null)||s.Dodges.Any(x=>x==null)||s.MeleeAttacks.Any(x=>x==null)||s.Presses.Any(x=>x==null))throw new ArgumentException("Invalid combat collections.");
            if(s.SchemaVersion<Snapshot.ClubAttackSchema) {
                if(s.Clubs.Length+s.Stances.Length+s.Dodges.Length+s.MeleeAttacks.Length+s.Presses.Length!=0)throw new ArgumentException("Club combat requires schema9.");return;
            }
            bool Actor(string id)=>s.Actors.Any(a=>a.Id==id);
            if(s.Clubs.Select(w=>w.Id).Distinct(StringComparer.Ordinal).Count()!=s.Clubs.Length||s.Presses.Select(p=>p.ActorId).Distinct(StringComparer.Ordinal).Count()!=s.Presses.Length
                ||s.SchemaVersion<Snapshot.DodgeSchema&&s.Dodges.Length!=0
                ||s.SchemaVersion>=Snapshot.DodgeSchema&&(s.Dodges.Select(d=>d.Revision).Distinct().Count()!=s.Dodges.Length
                    ||s.Dodges.Any(d=>EncounterHistory.AtRevision(s,d.Revision)==null))
                ||s.Dodges.Any(d=>!Actor(d.ActorId)||d.Revision>s.Revision)
                ||s.Clubs.Any(w=>w.HeldBy!=""&&!Actor(w.HeldBy))||s.Stances.Any(t=>!Actor(t.ActorId)||t.Revision>s.Revision)
                ||s.MeleeAttacks.Count(a=>a.Pending)>1||s.MeleeAttacks.Select(a=>a.Id).Distinct(StringComparer.Ordinal).Count()!=s.MeleeAttacks.Length
                ||s.MeleeAttacks.Any(a=>!Actor(a.AttackerId)||!Actor(a.TargetId)||!s.Clubs.Any(w=>w.Id==a.WeaponId)&&!(s.SchemaVersion>=Snapshot.TacticalMovementSchema&&a.WeaponId==CombatProfileIds.OrdinaryUnarmed)||a.Revision>s.Revision||a.ResolvedRevision>s.Revision||a.At>s.RuleClock)
                ||s.SchemaVersion>=Snapshot.SharedWorldSchema&&s.MeleeAttacks.Any(a=>EncounterHistory.AtRevision(s,a.Revision)==null
                    ||a.Pending&&!EncounterHistory.InCurrent(s,a.Revision)||!a.Pending&&EncounterHistory.AtRevision(s,a.Revision)?.Id!=EncounterHistory.AtRevision(s,a.ResolvedRevision)?.Id)
                ||s.Presses.Any(p=>!Actor(p.ActorId)||!Actor(p.TargetId)||p.ArmedRevision>s.Revision))throw new ArgumentException("Invalid combat references.");
        }
    }
}
