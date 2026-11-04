using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public sealed class CharacterLevelFact
    {
        public string ClassName { get; }
        public int BaseHp { get; }
        public CharacterLevelFact(string name,int baseHp)
        {
            if(string.IsNullOrEmpty(name)||name.Length>96||name.Any(c=>c<32||c>126)||baseHp<1)throw new ArgumentException("Invalid attained-level record.");
            ClassName=name;BaseHp=baseHp;
        }
    }
    /// <summary>Recorded numerical facts, not proof of complete character creation or feature acquisition.</summary>
    public sealed class ActorCharacterRecord
    {
        public string ActorId { get; }
        public string ProfileId { get; }
        public IReadOnlyList<int> Abilities { get; }
        public IReadOnlyList<CharacterLevelFact> Levels { get; }
        public ActorCharacterRecord(string actor,string profile,IEnumerable<int> abilities,IEnumerable<CharacterLevelFact> levels)
        {
            if(!Validation.ValidId(actor)||!Validation.ValidId(profile)||abilities==null||levels==null)throw new ArgumentException("Invalid character record.");
            var scores=abilities.ToArray();var gained=levels.ToArray();
            if(scores.Length!=6||gained.Length<1||gained.Length>20||gained.Any(x=>x==null))throw new ArgumentException("Invalid character collections.");
            ActorId=actor;ProfileId=profile;Abilities=Array.AsReadOnly(scores);Levels=Array.AsReadOnly(gained);
        }
    }
    /// <summary>Immutable persisted life facts. Source-specific transitions and condition permissions belong to the rule policy.</summary>
    public sealed class ActorLifeRecord
    {
        public string ActorId { get; }
        public long MaximumHp { get; }
        public long Hp { get; }
        public long TemporaryHp { get; }
        public IReadOnlyList<int> LinkedInjuries { get; }
        public bool Stable { get; }
        public bool Dead { get; }
        public bool UsesDeathSaves { get; }
        public int DeathSuccesses { get; }
        public int DeathFailures { get; }
        public RuleTime? StableUntil { get; }
        public long LastDeathTurn { get; }
        public bool Prone { get; }
        public IReadOnlyList<string> HeldItems { get; }
        public ActorLifeRecord(string actor,long maximumHp,long hp,long temporaryHp,IEnumerable<int> injuries,
            bool stable,bool dead,bool usesDeathSaves,int successes,int failures,RuleTime? stableUntil,long lastDeathTurn,
            bool prone,IEnumerable<string> heldItems)
        {
            if(!Validation.ValidId(actor)||maximumHp<1||hp<0||hp>maximumHp||temporaryHp<0||injuries==null||heldItems==null
                ||successes<0||successes>3||failures<0||failures>3||lastDeathTurn<0)throw new ArgumentException("Invalid life quantities.");
            var wounds=injuries.ToArray();var held=heldItems.ToArray();
            if(wounds.Length>3||wounds.Any(i=>i<0||i>6)||held.Length>32||held.Any(i=>!Validation.ValidId(i))||held.Distinct(StringComparer.Ordinal).Count()!=held.Length)
                throw new ArgumentException("Invalid life collections.");
            ActorId=actor;MaximumHp=maximumHp;Hp=hp;TemporaryHp=temporaryHp;LinkedInjuries=Array.AsReadOnly(wounds);
            Stable=stable;Dead=dead;UsesDeathSaves=usesDeathSaves;DeathSuccesses=successes;DeathFailures=failures;
            StableUntil=stableUntil;LastDeathTurn=lastDeathTurn;Prone=prone;HeldItems=Array.AsReadOnly(held);
        }
        public bool SameAs(ActorLifeRecord other)=>other!=null&&ActorId==other.ActorId&&MaximumHp==other.MaximumHp&&Hp==other.Hp
            &&TemporaryHp==other.TemporaryHp&&LinkedInjuries.SequenceEqual(other.LinkedInjuries)&&Stable==other.Stable&&Dead==other.Dead
            &&UsesDeathSaves==other.UsesDeathSaves&&DeathSuccesses==other.DeathSuccesses&&DeathFailures==other.DeathFailures
            &&StableUntil==other.StableUntil&&LastDeathTurn==other.LastDeathTurn&&Prone==other.Prone&&HeldItems.SequenceEqual(other.HeldItems);
    }
    public enum LifeEventKind { StableRecovery, DeathSave }
    public sealed class ActorLifeEvent
    {
        public string ActorId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public LifeEventKind Kind { get; }
        public int TurnOrdinal { get; }
        public int Natural { get; }
        public int RecoveryD4 { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public ActorLifeEvent(string actor,long revision,RuleTime at,LifeEventKind kind,int turnOrdinal,int natural,int recoveryD4,uint before,uint after,long words)
        {
            if(!Validation.ValidId(actor)||revision<1||!Enum.IsDefined(typeof(LifeEventKind),kind)||turnOrdinal< -1||natural<0||natural>20
                ||recoveryD4<0||recoveryD4>4||before==0||after==0||words<0)throw new ArgumentException("Invalid life event.");
            ActorId=actor;Revision=revision;At=at;Kind=kind;TurnOrdinal=turnOrdinal;Natural=natural;RecoveryD4=recoveryD4;
            RandomBefore=before;RandomAfter=after;WordsConsumed=words;
        }
        public bool SameOutcome(ActorLifeEvent other)=>other!=null&&ActorId==other.ActorId&&At==other.At&&Kind==other.Kind
            &&TurnOrdinal==other.TurnOrdinal&&Natural==other.Natural&&RecoveryD4==other.RecoveryD4&&RandomBefore==other.RandomBefore
            &&RandomAfter==other.RandomAfter&&WordsConsumed==other.WordsConsumed;
    }
    public static class ActorLifeValidation
    {
        public static void Validate(Snapshot s)
        {
            if(s.Characters==null||s.Lives==null||s.LifeEvents==null||s.Characters.Length>64||s.Lives.Length>64||s.LifeEvents.Length>256
                ||s.Characters.Any(x=>x==null)||s.Lives.Any(x=>x==null)||s.LifeEvents.Any(x=>x==null))throw new ArgumentException("Invalid actor life collections.");
            if(s.SchemaVersion<Snapshot.ActorLifeSchema) {
                if(s.Characters.Length!=0||s.Lives.Length!=0||s.LifeEvents.Length!=0)throw new ArgumentException("Actor life requires schema8.");return;
            }
            var actors=s.Actors.Select(x=>x.Id).OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            if(!actors.SequenceEqual(s.Characters.Select(x=>x.ActorId).OrderBy(x=>x,StringComparer.Ordinal))
                ||!actors.SequenceEqual(s.Lives.Select(x=>x.ActorId).OrderBy(x=>x,StringComparer.Ordinal))
                ||s.LifeEvents.Any(x=>!actors.Contains(x.ActorId)||x.Revision>s.Revision||x.At>s.RuleClock))throw new ArgumentException("Invalid actor life references.");
        }
    }
}
