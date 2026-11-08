#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public static class ActorLifeRules
    {
        public static LifeState Read(ActorLifeRecord r)=>new LifeState(r.MaximumHp,r.Hp,r.TemporaryHp,r.LinkedInjuries.Select(i=>(Injury)i),
            r.Stable,r.Dead,r.DeathSuccesses,r.DeathFailures,r.UsesDeathSaves,lastDeathTurn:r.LastDeathTurn,stableUntil:r.StableUntil);
        /// <summary>Projects the active, source-qualified effective HP ceiling for a life resolution.
        /// The persisted ActorLifeRecord.MaximumHp remains the base character authority.</summary>
        public static LifeState ReadForResolution(Snapshot s,ActorLifeRecord record)
        {
            if(s==null||record==null)throw new ArgumentNullException(s==null?nameof(s):nameof(record));
            var baseLife=Read(record);
            long maximum=ExpeditionStrainRules.Current(s,record.ActorId).EffectiveMaximumHp(record.MaximumHp);
            long hp=Math.Min(baseLife.Hp,maximum);
            if(maximum==baseLife.MaximumHp&&hp==baseLife.Hp)return baseLife;
            return new LifeState(maximum,hp,baseLife.TemporaryHp,baseLife.Wounds,baseLife.Stable,baseLife.Dead,
                baseLife.DeathSuccesses,baseLife.DeathFailures,baseLife.UsesDeathSaves,lastDeathTurn:baseLife.LastDeathTurn,
                stableUntil:baseLife.StableUntil);
        }
        internal static ActorLifeRecord Record(string actor,LifeState state,bool prone,System.Collections.Generic.IEnumerable<string> held=null)=>new ActorLifeRecord(actor,state.MaximumHp,state.Hp,state.TemporaryHp,
            state.Wounds.Select(i=>(int)i),state.Stable,state.Dead,state.UsesDeathSaves,state.DeathSuccesses,state.DeathFailures,state.StableUntil,
            state.LastDeathTurn,prone,held??Array.Empty<string>());
        internal static ActorLifeRecord RecordFromResolution(ActorLifeRecord authority,LifeState state,bool prone,
            System.Collections.Generic.IEnumerable<string> held=null)
        {
            if(authority==null||state==null)throw new ArgumentNullException(authority==null?nameof(authority):nameof(state));
            return new ActorLifeRecord(authority.ActorId,authority.MaximumHp,state.Hp,state.TemporaryHp,
                state.Wounds.Select(i=>(int)i),state.Stable,state.Dead,state.UsesDeathSaves,state.DeathSuccesses,
                state.DeathFailures,state.StableUntil,state.LastDeathTurn,prone,held??Array.Empty<string>());
        }
        public static bool CanAct(Snapshot s,string actor){var l=s.Lives.Single(x=>x.ActorId==actor);return !l.Dead&&l.Hp>0;}
        public static bool ZeroHpUnconscious(Snapshot s,string actor){var l=s.Lives.Single(x=>x.ActorId==actor);return !l.Dead&&l.Hp==0;}
        private static void Set(Snapshot s,ActorLifeRecord record)=>s.Lives=s.Lives.Select(x=>x.ActorId==record.ActorId?record:x).ToArray();
        private static void Event(Snapshot s,ActorLifeEvent record)
        {if(s.LifeEvents.Length==256)throw new ArgumentException("Life event history full.");s.LifeEvents=s.LifeEvents.Concat(new[]{record}).ToArray();}
        internal static RuleTime? NextDeadline(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.ActorLifeSchema)return null;
            var due=s.Lives.Where(x=>x.Stable&&x.StableUntil>s.RuleClock).OrderBy(x=>x.StableUntil).FirstOrDefault();return due?.StableUntil;
        }
        internal static void RecoverDue(Snapshot s)
        {
            if(s.SchemaVersion<Snapshot.ActorLifeSchema)return;
            foreach(var before in s.Lives.Where(x=>x.Stable&&x.StableUntil<=s.RuleClock).OrderBy(x=>x.StableUntil).ThenBy(x=>x.ActorId,StringComparer.Ordinal).ToArray()) {
                var after=PlaytestLife.StableRecoveryAt(ReadForResolution(s,before),s.RuleClock);
                Set(s,RecordFromResolution(before,after,before.Prone,before.HeldItems));
                Event(s,new ActorLifeEvent(before.ActorId,s.Revision+1,s.RuleClock,LifeEventKind.StableRecovery,-1,0,0,s.RandomState,s.RandomState,0));
            }
        }
        internal static void RegularStart(Snapshot s,int ordinal)
        {
            SaveAtMarker(s,s.Encounter.Order[ordinal%s.Encounter.Order.Count],ordinal,(long)ordinal+1);
        }
        internal static void SaveAtMarker(Snapshot s,string actor,int ordinal,long marker)
        {
            RecoverDue(s);var before=s.Lives.Single(x=>x.ActorId==actor);var life=ReadForResolution(s,before);
            if(life.Dead||life.Stable||life.Hp!=0||!life.UsesDeathSaves)return;
            uint initial=s.RandomState;var d20=PlaytestDice.RollD20(initial);uint next=d20.NextRandomState;long words=d20.WordsConsumed;int? d4=null;
            int modifier=ExpeditionStrainRules.Current(s,actor).SavingThrowModifier;
            if(d20.Natural!=20&&d20.Natural!=1&&d20.Natural+modifier>=10&&life.DeathSuccesses==2) {
                var recovery=DiceStream.Draw(next,4);d4=recovery.Value+1;next=recovery.NextState;words=checked(words+recovery.WordsConsumed);
            }
            var after=PlaytestLife.DeathSaveAt(life,d20.Natural,marker,s.RuleClock,modifier:modifier,stableD4:d4);
            Set(s,RecordFromResolution(before,after,before.Prone,before.HeldItems));s.RandomState=next;
            Event(s,new ActorLifeEvent(actor,s.Revision+1,s.RuleClock,LifeEventKind.DeathSave,ordinal,d20.Natural,d4??0,initial,next,words));
        }
        internal static string Key(ActorLifeRecord r)=>r.ActorId+"|"+r.MaximumHp.ToString(CultureInfo.InvariantCulture)+"|"+r.Hp.ToString(CultureInfo.InvariantCulture)
            +"|"+r.TemporaryHp.ToString(CultureInfo.InvariantCulture)+"|"+string.Join(",",r.LinkedInjuries)+"|"+r.Stable+"|"+r.Dead+"|"+r.UsesDeathSaves
            +"|"+r.DeathSuccesses+"|"+r.DeathFailures+"|"+r.StableUntil+"|"+r.LastDeathTurn.ToString(CultureInfo.InvariantCulture)+"|"+r.Prone;
    }
    /// <summary>Numerical fixture profiles, not fully created class characters. Medium/STR10 and empty
    /// hands are explicit facts. Inventory handling, intake, attacks, standing and independent effects
    /// remain gated. The admitted life transitions never make a capable worker newly unconscious.</summary>
    public sealed class TestOnlyActorLifePolicy : ICommandPolicy
    {
        private readonly TestOnlyEncounterPolicy encounter;
        private readonly ActorLifeRecord[] initialLives;
        private readonly RuleTime origin;
        private readonly uint seed;
        public bool TestOnly=>true;
        public string ContentFingerprint { get; }
        private static ActorCharacterRecord Character(string actor)=>new ActorCharacterRecord(actor,"TEST_ONLY.numeric-warrior3",
            new[]{10,10,10,10,10,10},new[]{new CharacterLevelFact("Warrior",12),new CharacterLevelFact("Warrior",7),new CharacterLevelFact("Warrior",7)});
        public TestOnlyActorLifePolicy(LifeState actorLife=null,LifeState companionLife=null,RuleTime origin=default,uint seed=1,
            string[] resolvedOrder=null,bool actorProne=false,bool companionProne=false)
        {
            if(seed==0)throw new ArgumentException("Nonzero random seed required.");
            this.origin=origin;this.seed=seed;encounter=new TestOnlyEncounterPolicy(resolvedOrder??Array.Empty<string>());
            initialLives=new[]{ActorLifeRules.Record(TestOnlyPolicy.ActorId,actorLife??new LifeState(26,26),actorProne||(actorLife?.Hp==0)),
                ActorLifeRules.Record(TestOnlyPolicy.CompanionId,companionLife??new LifeState(26,26),companionProne||(companionLife?.Hp==0))};
            foreach(var life in initialLives) {
                if(life.MaximumHp!=26||life.LastDeathTurn!=0||life.StableUntil<=origin)throw new ArgumentException("Life facts do not fit this initial numerical profile.");
                ActorLifeRules.Read(life);
            }
            string key="actor-life-v1|"+encounter.ContentFingerprint+"|"+origin+"|"+seed.ToString(CultureInfo.InvariantCulture)+"|"+string.Join(";",initialLives.Select(ActorLifeRules.Key));
            using(var sha=SHA256.Create())ContentFingerprint="TEST_ONLY.actor-life-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        public Snapshot Initial()
        {
            var s=encounter.Initial();s.SchemaVersion=Snapshot.ActorLifeSchema;s.ContentFingerprint=ContentFingerprint;s.RuleClock=origin;s.RandomState=seed;
            s.Characters=s.Actors.Select(a=>Character(a.Id)).ToArray();s.Lives=initialLives.ToArray();return s;
        }
        private static bool Admitted(CommandKind kind)=>kind==CommandKind.AdvanceClock||kind==CommandKind.BeginFixedEncounter||kind==CommandKind.EndRegularTurn
            ||kind==CommandKind.EncounterDash||kind==CommandKind.PlantCrop||kind==CommandKind.TendCrop||kind==CommandKind.HarvestCrop
            ||kind==CommandKind.PauseCrop||kind==CommandKind.SetCropConditions;
        private static bool HostProgress(CommandKind kind)=>kind==CommandKind.AdvanceClock||kind==CommandKind.BeginFixedEncounter||kind==CommandKind.EndRegularTurn||kind==CommandKind.SetCropConditions;
        public string Resolve(Snapshot s,Command c)
        {
            if(!Admitted(c.Kind))return "ActorLifeCommandNotImplemented";
            if(!HostProgress(c.Kind)&&!ActorLifeRules.CanAct(s,c.Actor))return "ActorCannotAct";
            if(c.Kind==CommandKind.BeginFixedEncounter)ActorLifeRules.RecoverDue(s);
            string failure=encounter.Resolve(s,c);if(failure!=null)return failure;
            if(c.Kind==CommandKind.BeginFixedEncounter||c.Kind==CommandKind.EndRegularTurn)ActorLifeRules.RegularStart(s,s.Encounter.TurnOrdinal);
            return null;
        }
        public string ValidateState(Snapshot s)
        {
            try {
                string error=encounter.ValidateEncounterState(s,true);if(error!=null)return error;
                if(s.RuleClock<origin||s.Handling.Length!=0||s.VesselMoves.Length!=0||s.Intakes.Length!=0||s.WaterFills.Length!=0)return "InvalidActorLifeFixture";
                foreach(var character in s.Characters) {
                    var expected=Character(character.ActorId);
                    if(character.ProfileId!=expected.ProfileId||!character.Abilities.SequenceEqual(expected.Abilities)||character.Levels.Count!=expected.Levels.Count
                        ||character.Levels.Where((x,i)=>x.ClassName!=expected.Levels[i].ClassName||x.BaseHp!=expected.Levels[i].BaseHp).Any())return "UnknownCharacterFacts";
                    long maximum=PlaytestCharacters.BaseMaximumHp(character.Levels.Select(x=>new CharacterLevelRecord(x.ClassName,x.BaseHp)).ToArray(),
                        CharacterRuleFacts.From(character).AbilityScore(CharacterAbility.Constitution)).BaseMaximum;
                    var life=s.Lives.Single(x=>x.ActorId==character.ActorId);ActorLifeRules.Read(life);
                    if(life.MaximumHp!=maximum||life.HeldItems.Count!=0||life.Hp==0&&!life.Prone)return "InvalidLifeProjection";
                }
                // Re-run the bounded admitted commands from the fingerprinted initial facts.
                // This binds each automatic event to its actual command interval, not merely a plausible receipt kind.
                if(s.Receipts.Length!=s.Revision)return "IncompleteActorLifeHistory";
                var replay=Initial();
                foreach(var receipt in s.Receipts.OrderBy(r=>r.Revision)) {
                    var command=CommandHistory.Read(receipt);
                    if(!Admitted(command.Kind)||!replay.Actors.Any(a=>a.Id==command.Actor)||command.Inventory!=null||command.Combat!=null)return "InvalidActorLifeReceipt";
                    if(command.ExpectedRevision!=replay.Revision||Resolve(replay,command)!=null)return "InvalidActorLifeCommandHistory";
                    replay.Revision=receipt.Revision;replay.Receipts=replay.Receipts.Concat(new[]{receipt}).ToArray();
                }
                if(s.RuleClock!=replay.RuleClock||(s.Encounter==null)!=(replay.Encounter==null)
                    ||s.Encounter!=null&&(s.Encounter.Origin!=replay.Encounter.Origin||!s.Encounter.StartRevisions.SequenceEqual(replay.Encounter.StartRevisions))
                    ||s.RandomState!=replay.RandomState||s.Lives.Any(l=>!l.SameAs(replay.Lives.Single(a=>a.ActorId==l.ActorId)))
                    ||s.LifeEvents.Length!=replay.LifeEvents.Length)return "InvalidLifeReplay";
                for(int i=0;i<s.LifeEvents.Length;i++)
                    if(s.LifeEvents[i].Revision!=replay.LifeEvents[i].Revision||!s.LifeEvents[i].SameOutcome(replay.LifeEvents[i]))return "InvalidLifeHistory";
                return null;
            } catch(Exception ex) when(ex is ArgumentException||ex is InvalidOperationException||ex is OverflowException){return "InvalidActorLifeState";}
        }
    }
}
#endif
