#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Two explicitly aligned Medium numerical actors, ordinary unarmored AC, one held Standard
    /// Club each, no proficiency grants, armor, shield, independent conditions, damage defenses, features,
    /// reactions, effects or extra attacks. Both have usable hands and clear mutual sight/line of effect
    /// on supported level ground. This is a bounded source test, not full character creation or combat.</summary>
    public sealed class TestOnlyClubAttackPolicy : ICommandPolicy
    {
        public const string ClubProfile="TEST_ONLY.standard-club",ActorClub="TEST_ONLY.actor-club",CompanionClub="TEST_ONLY.companion-club";
        private readonly TestOnlyActorLifePolicy life;
        private readonly TestOnlyEncounterPolicy encounter=new TestOnlyEncounterPolicy();
        private readonly TestOnlyFillingPolicy inventory=new TestOnlyFillingPolicy(movableVessels:true);
        private readonly int companionX,companionY;
        public bool TestOnly=>true;
        public string ContentFingerprint { get; }
        public TestOnlyClubAttackPolicy(long actorHp=26,long companionHp=26,long actorTemporaryHp=0,long companionTemporaryHp=0,
            uint seed=1,RuleTime origin=default,int companionX=1,int companionY=0,bool actorProne=false,bool companionProne=false)
        {
            if(actorHp<1||actorHp>26||companionHp<1||companionHp>26||companionX<1||companionX>4||companionY<0||companionY>1||companionY==1&&companionX!=1)
                throw new ArgumentException("Unsupported initial club fixture facts.");
            life=new TestOnlyActorLifePolicy(new LifeState(26,actorHp,actorTemporaryHp),new LifeState(26,companionHp,companionTemporaryHp),origin,seed,
                actorProne:actorProne,companionProne:companionProne);this.companionX=companionX;this.companionY=companionY;
            string key="club-attack-v1|"+life.ContentFingerprint+"|"+N(companionX)+"|"+N(companionY);
            using(var sha=SHA256.Create())ContentFingerprint="TEST_ONLY.club-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string N(long n)=>n.ToString(CultureInfo.InvariantCulture);
        public Snapshot Initial()
        {
            var s=life.Initial();s.SchemaVersion=Snapshot.ClubAttackSchema;s.ContentFingerprint=ContentFingerprint;
            foreach(var a in s.Actors){a.X=a.Id==TestOnlyPolicy.ActorId?0:companionX;a.Y=a.Id==TestOnlyPolicy.ActorId?0:companionY;}
            s.Clubs=s.Actors.Select(a=>new ClubInstance(a.Id==TestOnlyPolicy.ActorId?ActorClub:CompanionClub,ClubProfile,a.Id,a.Id,a.Id,a.X,a.Y)).ToArray();
            s.Lives=s.Lives.Select(l=>ActorLifeRules.Record(l.ActorId,ActorLifeRules.Read(l),l.Prone,new[]{s.Clubs.Single(w=>w.HeldBy==l.ActorId).Id})).ToArray();return s;
        }
        public static StanceSelectionRecord ActiveStance(Snapshot s,string actor)=>s.Stances.LastOrDefault(t=>t.ActorId==actor&&s.RuleClock<t.ExpiresAt);
        public static PressRecord ActivePress(Snapshot s,string actor)=>s.Presses.SingleOrDefault(p=>p.ActorId==actor&&s.RuleClock<p.ExpiresAt);
        public static bool ActionSpent(Snapshot s)=>FixedEncounterRules.ActionSpent(s)||s.Encounter!=null&&s.MeleeAttacks.Any(a=>a.TurnOrdinal==s.Encounter.TurnOrdinal);
        private static bool Admitted(CommandKind k)=>k==CommandKind.AdvanceClock||k==CommandKind.BeginFixedEncounter||k==CommandKind.EndRegularTurn
            ||k==CommandKind.EncounterDash||k==CommandKind.SelectCombatStance||k==CommandKind.AttackClub||k==CommandKind.ResolveKnockout;
        private static bool HasStance(Snapshot s)=>s.Stances.Any(t=>t.TurnOrdinal==s.Encounter.TurnOrdinal);
        public string Resolve(Snapshot s,Command c)
        {
            if(!Admitted(c.Kind))return "ClubCommandNotImplemented";
            bool combat=c.Kind==CommandKind.SelectCombatStance||c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.ResolveKnockout;
            if(c.Inventory!=null||combat!=(c.Combat!=null))return "UnexpectedCombatPayload";
            var pending=s.MeleeAttacks.SingleOrDefault(a=>a.Pending);
            if(pending!=null)return c.Kind==CommandKind.ResolveKnockout?Complete(s,c,pending):"KnockoutChoicePending";
            if(c.Kind==CommandKind.ResolveKnockout)return "NoPendingKnockout";
            if(c.Kind==CommandKind.BeginFixedEncounter||c.Kind==CommandKind.AdvanceClock) {
                string error=encounter.Resolve(s,c);if(error!=null)return error;
                if(c.Kind==CommandKind.BeginFixedEncounter)ActorLifeRules.RegularStart(s,0);return null;
            }
            var e=s.Encounter;
            if(e==null||c.Actor!=e.CurrentActor||c.X!=0||c.Y!=0||combat&&c.Combat.TurnId!=e.CurrentTurnId)return "WrongRegularTurn";
            if(c.Kind==CommandKind.EndRegularTurn) {
                if(ActorLifeRules.CanAct(s,c.Actor)&&!HasStance(s))return "StanceRequired";
                string error=encounter.Resolve(s,c);if(error!=null)return error;
                ActorLifeRules.RegularStart(s,s.Encounter.TurnOrdinal);return null;
            }
            if(!ActorLifeRules.CanAct(s,c.Actor))return "ActorCannotAct";
            if(c.Kind==CommandKind.SelectCombatStance) {
                if(c.Target!=""||c.Combat.WeaponId!=""||c.Combat.Stance==0||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome||c.Combat.Choice)return "InvalidStanceRequest";
                if(HasStance(s))return "StanceAlreadySelected";
                if((CombatStance)c.Combat.Stance==CombatStance.Carrying)return "NoApplicableCargoPenalty";
                if(s.Stances.Length==128)return "StanceHistoryCapacityReached";
                s.Stances=s.Stances.Concat(new[]{new StanceSelectionRecord(c.Actor,s.Revision+1,e.TurnOrdinal,(CombatStance)c.Combat.Stance,FixedEncounterRules.Start(e,e.TurnOrdinal+e.Order.Count))}).ToArray();return null;
            }
            if(ActionSpent(s))return "ActionAlreadySpent";
            if(c.Kind==CommandKind.EncounterDash)return encounter.Resolve(s,c);
            if(!HasStance(s))return "StanceRequired";
            return Attack(s,c);
        }
        private static CombatDamageRoll DamageRecord(int[] dice,long total,long diceWords,uint seed,RolledDamage result)
            =>new CombatDamageRoll(dice,total,diceWords,seed,result.NextRandomState,result.WordsConsumed,result.WoundRoll?.Natural??0,result.InjuryD6??0,result.StableD4??0);
        private static string Attack(Snapshot s,Command c)
        {
            var request=c.Combat;
            if(request.Stance!=0||request.Choice)return "InvalidAttackRequest";
            if(s.MeleeAttacks.Length==128)return "AttackHistoryCapacityReached";
            var weapon=s.Clubs.SingleOrDefault(w=>w.Id==request.WeaponId);
            var attacker=s.Lives.Single(l=>l.ActorId==c.Actor);
            if(weapon==null||weapon.ProfileId!=ClubProfile||weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor||!attacker.HeldItems.Contains(weapon.Id))return "ClubNotHeld";
            var target=s.Lives.SingleOrDefault(l=>l.ActorId==c.Target);
            if(target==null||target.ActorId==c.Actor||target.Dead)return "InvalidLivingTarget";
            var a=s.Actors.Single(x=>x.Id==c.Actor);var t=s.Actors.Single(x=>x.Id==c.Target);
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(a.X,a.Y),new CombatCell(t.X,t.Y))>5)return "TargetOutOfReach";
            bool advantage=target.Prone||ActorLifeRules.ZeroHpUnconscious(s,c.Target),disadvantage=attacker.Prone;
            uint before=s.RandomState;var roll=PlaytestDice.RollD20(before,advantage?1:0,disadvantage?1:0);
            int modifier=attacker.LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0; // STR10, explicitly no Club proficiency grant.
            var defense=ActiveStance(s,c.Target);int ac=checked((int)PrototypeArmor.UnarmoredBaseAc(10))+(defense?.Kind==CombatStance.Aggressive?-2:defense?.Kind==CombatStance.Guarded?1:0);
            var hit=PlaytestRolls.AttackRoll(roll.Natural,modifier,ac);bool critical=hit.Hit&&(hit.Critical||ActorLifeRules.ZeroHpUnconscious(s,c.Target));
            var attack=new CombatAttackRoll(roll.First,roll.Second??0,roll.Natural,modifier,ac,hit.Hit,critical,before,roll.NextRandomState,roll.WordsConsumed);
            uint next=roll.NextRandomState;CombatDamageRoll damage;bool pending=false;
            if(hit.Hit) {
                var dice=new int[critical?2:1];long words=0;
                for(int i=0;i<dice.Length;i++){var d=DiceStream.Draw(next,4);dice[i]=d.Value+1;next=d.NextState;words=checked(words+d.WordsConsumed);}
                long total=dice.Sum()+(ActiveStance(s,c.Actor).Kind==CombatStance.Aggressive?2:0);
                var result=PlaytestDamageDice.Resolve(ActorLifeRules.Read(target),total,s.RuleClock,next,critical:critical,melee:true,knockout:(KnockoutInstruction)request.Knockout);
                damage=DamageRecord(dice,total,words,next,result);next=result.NextRandomState;pending=result.Pending!=null;
                if(!pending)ApplyLife(s,target,result.Outcome.State);
                var press=new PressRecord(c.Actor,c.Target,s.Revision+1,FixedEncounterRules.Start(s.Encounter,s.Encounter.TurnOrdinal+s.Encounter.Order.Count));
                s.Presses=s.Presses.Where(p=>p.ActorId!=c.Actor).Concat(new[]{press}).ToArray();
            } else damage=new CombatDamageRoll(Array.Empty<int>(),0,0,next,next,0,0,0,0);
            s.RandomState=next;
            var record=new MeleeAttackRecord("attack."+N(s.Revision+1),s.Revision+1,pending?0:s.Revision+1,s.Encounter.TurnOrdinal,c.Actor,c.Target,weapon.Id,s.RuleClock,request.Knockout,attack,damage);
            s.MeleeAttacks=s.MeleeAttacks.Concat(new[]{record}).ToArray();return null;
        }
        private static string Complete(Snapshot s,Command c,MeleeAttackRecord pending)
        {
            var r=c.Combat;
            if(r==null||c.Actor!=pending.AttackerId||c.Target!=pending.Id||r.TurnId!=s.Encounter.CurrentTurnId||c.X!=0||c.Y!=0
                ||r.WeaponId!=""||r.Stance!=0||r.Knockout!=AttackKnockoutMode.OrdinaryOutcome)return "InvalidKnockoutChoice";
            var before=s.Lives.Single(l=>l.ActorId==pending.TargetId);var d=pending.Damage;
            // Reconstruct the immutable continuation from its retained seed and unchanged target facts.
            // The prior rolls are verified, never applied to the world random stream a second time.
            var prior=PlaytestDamageDice.Resolve(ActorLifeRules.Read(before),d.Total,pending.At,d.EffectsSeed,critical:pending.Attack.Critical,melee:true,knockout:KnockoutInstruction.AskIfEligible);
            if(prior.Pending==null||!d.SameAs(DamageRecord(d.Dice.ToArray(),d.Total,d.DiceWords,d.EffectsSeed,prior))||s.RandomState!=prior.NextRandomState)return "InvalidPendingKnockout";
            var result=prior.Pending.Complete(r.Choice);s.RandomState=result.NextRandomState;ApplyLife(s,before,result.Outcome.State);
            var resolved=new MeleeAttackRecord(pending.Id,pending.Revision,s.Revision+1,pending.TurnOrdinal,pending.AttackerId,pending.TargetId,pending.WeaponId,pending.At,
                pending.Instruction,pending.Attack,DamageRecord(d.Dice.ToArray(),d.Total,d.DiceWords,d.EffectsSeed,result));
            s.MeleeAttacks=s.MeleeAttacks.Select(a=>a.Id==pending.Id?resolved:a).ToArray();return null;
        }
        private static void ApplyLife(Snapshot s,ActorLifeRecord before,LifeState after)
        {
            bool newlyUnconscious=!after.Dead&&after.Hp==0&&before.Hp>0;
            // The initial HP/Wound facts and bounded Club damage exclude death while still holding equipment.
            if(after.Dead&&before.HeldItems.Count!=0)throw new ArgumentException("Death with held equipment is outside this profile.");
            var record=ActorLifeRules.Record(before.ActorId,after,before.Prone||newlyUnconscious,newlyUnconscious?Array.Empty<string>():before.HeldItems);
            s.Lives=s.Lives.Select(l=>l.ActorId==record.ActorId?record:l).ToArray();
            if(newlyUnconscious) {
                var a=s.Actors.Single(x=>x.Id==before.ActorId);
                s.Clubs=s.Clubs.Select(w=>w.HeldBy==a.Id?new ClubInstance(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,"",a.X,a.Y):w).ToArray();
            }
        }
        public string ValidateState(Snapshot s)
        {
            try {
                if(s.SchemaVersion!=Snapshot.ClubAttackSchema)return "WrongClubSchema";
                string error=inventory.ValidateFillingState(s,true,true,true);if(error!=null)return error;
                if(s.Crops.Length+s.CropFood.Length+s.Handling.Length+s.VesselMoves.Length+s.Intakes.Length+s.WaterFills.Length!=0
                    ||s.Work.WorkerIntervals.Count+s.Work.Reservations.Count!=0||s.Receipts.Length!=s.Revision)return "InvalidClubFixture";
                var replay=Initial();
                foreach(var receipt in s.Receipts.OrderBy(r=>r.Revision)) {
                    var p=receipt.Fingerprint.Split('|');CombatRequest request=null;
                    if(p.Length!=6&&p.Length!=12||!int.TryParse(p[0],NumberStyles.Integer,CultureInfo.InvariantCulture,out int kind)
                        ||!int.TryParse(p[4],NumberStyles.Integer,CultureInfo.InvariantCulture,out int x)||!int.TryParse(p[5],NumberStyles.Integer,CultureInfo.InvariantCulture,out int y)
                        ||!Admitted((CommandKind)kind)||!replay.Actors.Any(a=>a.Id==p[1]))return "InvalidClubReceipt";
                    if(p.Length==12) {
                        if(p[6]!="combat-v1"||!int.TryParse(p[9],NumberStyles.Integer,CultureInfo.InvariantCulture,out int stance)
                            ||!int.TryParse(p[10],NumberStyles.Integer,CultureInfo.InvariantCulture,out int knockout)||p[11]!="0"&&p[11]!="1")return "InvalidCombatPayloadHistory";
                        request=new CombatRequest(p[7],p[8],stance,(AttackKnockoutMode)knockout,p[11]=="1");
                    }
                    var command=new Command(receipt.Id,p[1],replay.Revision,(CommandKind)kind,p[2],x,y,combat:request);
                    if(!command.MatchesReceipt(receipt)||Resolve(replay,command)!=null)return "InvalidClubCommandHistory";
                    replay.Revision=receipt.Revision;replay.Receipts=replay.Receipts.Concat(new[]{receipt}).ToArray();
                }
                return SameState(s,replay)?null:"InvalidClubReplay";
            } catch(Exception ex) when(ex is ArgumentException||ex is InvalidOperationException||ex is OverflowException){return "InvalidClubState";}
        }
        private static bool Tables<T>(T[] a,T[] b,Func<T,T,bool> same)=>a.Length==b.Length&&a.All(x=>b.Count(y=>same(x,y))==1)&&b.All(y=>a.Count(x=>same(x,y))==1);
        private static bool SameState(Snapshot s,Snapshot r)
        {
            if(s.Clock!=r.Clock||s.RuleClock!=r.RuleClock||s.RandomState!=r.RandomState||s.InventoryCombat!=r.InventoryCombat||s.InventoryTurnActor!=r.InventoryTurnActor||s.InventoryInteractions!=r.InventoryInteractions
                ||(s.Encounter==null)!=(r.Encounter==null)||s.Encounter!=null&&(s.Encounter.Id!=r.Encounter.Id||s.Encounter.Origin!=r.Encounter.Origin
                    ||!s.Encounter.Order.SequenceEqual(r.Encounter.Order)||!s.Encounter.StartRevisions.SequenceEqual(r.Encounter.StartRevisions)))return false;
            return Tables(s.Actors,r.Actors,(a,b)=>a.Id==b.Id&&a.X==b.X&&a.Y==b.Y&&a.Tokens==b.Tokens)
                &&Tables(s.Objects,r.Objects,(a,b)=>a.Id==b.Id&&a.X==b.X&&a.Y==b.Y&&a.Opened==b.Opened)
                &&Tables(s.Characters,r.Characters,(a,b)=>a.ActorId==b.ActorId&&a.ProfileId==b.ProfileId&&a.Abilities.SequenceEqual(b.Abilities)
                    &&a.Levels.Count==b.Levels.Count&&!a.Levels.Where((x,i)=>x.ClassName!=b.Levels[i].ClassName||x.BaseHp!=b.Levels[i].BaseHp).Any())
                &&Tables(s.Lives,r.Lives,(a,b)=>a.SameAs(b))&&s.LifeEvents.Length==r.LifeEvents.Length
                &&!s.LifeEvents.Where((a,i)=>a.Revision!=r.LifeEvents[i].Revision||!a.SameOutcome(r.LifeEvents[i])).Any()
                &&Tables(s.EncounterDashes,r.EncounterDashes,(a,b)=>a.ActorId==b.ActorId&&a.Revision==b.Revision&&a.TurnOrdinal==b.TurnOrdinal)
                &&Tables(s.Clubs,r.Clubs,(a,b)=>a.SameAs(b))&&Tables(s.Stances,r.Stances,(a,b)=>a.SameAs(b))
                &&Tables(s.MeleeAttacks,r.MeleeAttacks,(a,b)=>a.SameAs(b))&&Tables(s.Presses,r.Presses,(a,b)=>a.SameAs(b))
                &&Tables(s.CropPlots,r.CropPlots,(a,b)=>a.Id==b.Id&&a.OwnerId==b.OwnerId&&a.Suitable==b.Suitable)
                &&Tables(s.Work.Lots.ToArray(),r.Work.Lots.ToArray(),(a,b)=>a.Id==b.Id&&a.UnitId==b.UnitId&&a.Amount==b.Amount&&a.LocationId==b.LocationId&&a.CustodianId==b.CustodianId)
                &&Tables(s.InventoryLots,r.InventoryLots,(a,b)=>a.LotId==b.LotId&&a.ParentId==b.ParentId&&a.OwnerId==b.OwnerId&&a.CreatedAmount==b.CreatedAmount&&a.CreatedAt==b.CreatedAt
                    &&a.Nutrition==b.Nutrition&&a.FreshUntil==b.FreshUntil&&a.Access==b.Access)
                &&Tables(s.Vessels,r.Vessels,(a,b)=>a.Id==b.Id&&a.Profile==b.Profile&&a.OwnerId==b.OwnerId&&a.LocationId==b.LocationId&&a.CustodianId==b.CustodianId)
                &&Tables(s.VesselContents,r.VesselContents,(a,b)=>a.LotId==b.LotId&&a.VesselId==b.VesselId);
        }
    }
}
#endif
