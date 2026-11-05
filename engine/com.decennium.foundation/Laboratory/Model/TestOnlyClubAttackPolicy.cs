#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Two explicitly aligned Medium numerical actors, ordinary unarmored AC, one held Standard
    /// Club each, no proficiency grants, armor, shield, independent conditions, damage defenses, features,
    /// effects or extra attacks. Optional schema11 adds an explicit tactical arena, ordinary unarmed/OA,
    /// Press and an optional third actor. The legacy stationary profiles retain their original scope.
    /// This is a bounded source test, not full character creation or combat.</summary>
    public sealed partial class TestOnlyClubAttackPolicy : ICommandPolicy
    {
        public const string ClubProfile="TEST_ONLY.standard-club",ActorClub="TEST_ONLY.actor-club",CompanionClub="TEST_ONLY.companion-club";
        private readonly TestOnlyActorLifePolicy life;
        private readonly TestOnlyEncounterPolicy encounter;
        private readonly TacticalCombatFixture tactical;
        private readonly HashSet<string> deferredConditionTargets;
        private readonly TestOnlyFillingPolicy inventory=new TestOnlyFillingPolicy(movableVessels:true);
        private readonly int companionX,companionY;
        private readonly int? actorBaseSpeed,companionBaseSpeed;
        private bool Posture=>actorBaseSpeed.HasValue;
        public bool TestOnly=>true;
        public string ContentFingerprint { get; }
        public TestOnlyClubAttackPolicy(long actorHp=26,long companionHp=26,long actorTemporaryHp=0,long companionTemporaryHp=0,
            uint seed=1,RuleTime origin=default,int companionX=1,int companionY=0,bool actorProne=false,bool companionProne=false,
            int? actorBaseWalkingSpeed=null,int? companionBaseWalkingSpeed=null,TacticalCombatFixture tactical=null,ConditionCombatFixture conditions=null,
            string[] deferredConditionTargets=null)
        {
            if(actorHp<1||actorHp>26||companionHp<1||companionHp>26||companionX<1||companionX>4||companionY<0||companionY>1||companionY==1&&companionX!=1)
                throw new ArgumentException("Unsupported initial club fixture facts.");
            if(actorBaseWalkingSpeed.HasValue!=companionBaseWalkingSpeed.HasValue||actorBaseWalkingSpeed<0||companionBaseWalkingSpeed<0)
                throw new ArgumentException("Supply both explicit nonnegative fixture walking Speeds, or neither.");
            actorBaseSpeed=actorBaseWalkingSpeed;companionBaseSpeed=companionBaseWalkingSpeed;
            this.tactical=tactical;this.conditions=conditions;
            this.deferredConditionTargets=new HashSet<string>(deferredConditionTargets??Array.Empty<string>(),StringComparer.Ordinal);
            if(conditions!=null&&tactical==null)throw new ArgumentException("Conditions require the explicit tactical fixture.");
            if(tactical!=null&&!Posture)throw new ArgumentException("Tactical movement requires explicit walking Speeds.");
            if(tactical?.Third!=null&&((tactical.Third.X==0&&tactical.Third.Y==0)||(tactical.Third.X==companionX&&tactical.Third.Y==companionY)))throw new ArgumentException("Third actor overlaps an initial body.");
            encounter=new TestOnlyEncounterPolicy(tactical!=null,tactical?.Third==null?new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId}:new[]{TestOnlyPolicy.ActorId,TestOnlyPolicy.CompanionId,AdditionalTacticalActor.Id});
            life=new TestOnlyActorLifePolicy(new LifeState(26,actorHp,actorTemporaryHp),new LifeState(26,companionHp,companionTemporaryHp),origin,seed,
                actorProne:actorProne,companionProne:companionProne);this.companionX=companionX;this.companionY=companionY;
            string key="club-attack-v1|"+life.ContentFingerprint+"|"+N(companionX)+"|"+N(companionY);
            if(Posture)key+="|posture-v1|"+N(actorBaseSpeed.Value)+"|"+N(companionBaseSpeed.Value);
            if(tactical!=null)key+="|"+tactical.Fingerprint;
            if(conditions!=null)key+="|"+conditions.Fingerprint;
            using(var sha=SHA256.Create())ContentFingerprint="TEST_ONLY.club-v1-"+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(key)).Select(b=>b.ToString("x2",CultureInfo.InvariantCulture)));
        }
        private static string N(long n)=>n.ToString(CultureInfo.InvariantCulture);
        public Snapshot Initial()
        {
            var s=life.Initial();s.SchemaVersion=Snapshot.ClubAttackSchema;s.ContentFingerprint=ContentFingerprint;
            foreach(var a in s.Actors){a.X=a.Id==TestOnlyPolicy.ActorId?0:companionX;a.Y=a.Id==TestOnlyPolicy.ActorId?0:companionY;}
            if(tactical?.Third!=null) {
                var third=tactical.Third;var original=s.Characters[0];
                s.Actors=s.Actors.Concat(new[]{new ActorState{Id=AdditionalTacticalActor.Id,X=third.X,Y=third.Y}}).ToArray();
                s.Characters=s.Characters.Concat(new[]{new ActorCharacterRecord(AdditionalTacticalActor.Id,original.ProfileId,original.Abilities,original.Levels)}).ToArray();
                s.Lives=s.Lives.Concat(new[]{ActorLifeRules.Record(AdditionalTacticalActor.Id,new LifeState(26,third.Hp),false)}).ToArray();
            }
            if(Posture){s.SchemaVersion=tactical==null?Snapshot.PostureSchema:Snapshot.TacticalMovementSchema;s.ActorMovement=s.Actors.Select(a=>new ActorMovementRecord(a.Id,a.Id==TestOnlyPolicy.ActorId?actorBaseSpeed.Value:a.Id==TestOnlyPolicy.CompanionId?companionBaseSpeed.Value:tactical.Third.WalkingSpeed)).ToArray();}
            if(tactical!=null)s.TacticalActors=s.Actors.Select(a=>new ActorTacticalRecord(a.Id)).ToArray();
            s.Clubs=s.Actors.Select(a=>new ClubInstance(a.Id==TestOnlyPolicy.ActorId?ActorClub:a.Id==TestOnlyPolicy.CompanionId?CompanionClub:AdditionalTacticalActor.ClubId,ClubProfile,a.Id,a.Id,a.Id,a.X,a.Y)).ToArray();
            s.Lives=s.Lives.Select(l=>ActorLifeRules.Record(l.ActorId,ActorLifeRules.Read(l),l.Prone,new[]{s.Clubs.Single(w=>w.HeldBy==l.ActorId).Id})).ToArray();
            if(conditions!=null)InitializeConditions(s);return s;
        }
        public static StanceSelectionRecord ActiveStance(Snapshot s,string actor)=>s.Stances.LastOrDefault(t=>t.ActorId==actor&&s.RuleClock<t.ExpiresAt);
        public static PressRecord ActivePress(Snapshot s,string actor)=>s.Presses.SingleOrDefault(p=>p.ActorId==actor&&s.RuleClock<p.ExpiresAt);
        public static bool ActionSpent(Snapshot s)=>s.WorldSchedule!=null&&s.Encounter!=null?s.WorldIntervals.Single(x=>x.ActorId==s.Encounter.CurrentActor).ActionSpent:FixedEncounterRules.ActionSpent(s)||s.Encounter!=null&&s.MeleeAttacks.Any(a=>a.TurnOrdinal==s.Encounter.TurnOrdinal&&!a.Opportunity&&EncounterHistory.InCurrent(s,a.Revision))
            ||s.Encounter!=null&&s.TacticalActors.Any(a=>a.ActorId==s.Encounter.CurrentActor&&a.DisengageTurn==s.Encounter.TurnOrdinal);
        private bool Admitted(CommandKind k)=>k==CommandKind.AdvanceClock||k==CommandKind.BeginFixedEncounter||k==CommandKind.EndRegularTurn
            ||k==CommandKind.EncounterDash||k==CommandKind.SelectCombatStance||k==CommandKind.AttackClub||k==CommandKind.ResolveKnockout
            ||Posture&&(k==CommandKind.StandFromProne||k==CommandKind.DropProne)
            ||conditions!=null&&k==CommandKind.DispatchConditionEvent
            ||tactical!=null&&(k==CommandKind.AttackUnarmed||k==CommandKind.TacticalStep||k==CommandKind.TacticalRepositionStep||k==CommandKind.RespondOpportunityAttack||k==CommandKind.RespondPress||k==CommandKind.Disengage);
        public static long WalkingSpeed(Snapshot s,string actor)
        {
            var m=s.ActorMovement.Single(x=>x.ActorId==actor);var l=s.Lives.Single(x=>x.ActorId==actor);
            long flat=(ActiveStance(s,actor)?.Kind==CombatStance.Guarded?-5:0)-(l.LinkedInjuries.Contains((int)Injury.MobilityTrauma)?5:0)
                -(l.LinkedInjuries.Count==3?10:0)-CharacterAdvancementRules.ArmorStrengthSpeedPenalty(s,actor);
            long speed=l.Dead||l.Hp==0?0:WithConditions(s)?PlaytestConditions.EffectiveSpeed(m.BaseWalkingSpeed,flat,CombatConditions(s,actor)):Math.Max(0,m.BaseWalkingSpeed+flat);
            if(s.SchemaVersion>=Snapshot.OverwatchExecutionSchema&&s.OverwatchRiderChoices.Any(x=>x.TargetId==actor
                &&x.Choice==OverwatchRider.Snare&&x.Status==OverwatchRiderChoiceStatus.Resolved&&s.Encounter!=null
                &&s.Encounter.TurnOrdinal<=x.ExpiresAfterTurnOrdinal))speed=Math.Max(0,speed-10);
            if(s.SchemaVersion>=Snapshot.SuppressionFireSchema&&s.SuppressionSlows.Any(x=>x.TargetActorId==actor
                &&x.Status==SuppressionSlowStatus.Active&&s.WorldSchedule.ProcessedSlot<=x.ExpirySlot))speed=Math.Max(0,speed-10);
            if(s.SchemaVersion>=Snapshot.PortableEquipmentSchema&&speed>0&&PortableEquipmentRules.IsBurdened(s,actor))
                speed=PlaytestCarrying.SpeedWithBurden(new RuleQuantity(speed),true).Numerator;
            return speed;
        }
        public static MovementLedger WalkingLedger(Snapshot s)
        {
            if(s.WorldSchedule!=null)throw new ArgumentException("Use exact shared-world movement ledger.");
            if(s.Encounter==null)throw new ArgumentException("No current regular turn.");
            var m=s.ActorMovement.Single(x=>x.ActorId==s.Encounter.CurrentActor);
            if(m.TurnOrdinal!=s.Encounter.TurnOrdinal)throw new ArgumentException("Movement turn is not current.");
            return new MovementLedger(m.Spent,s.EncounterDashes.Count(d=>d.TurnOrdinal==m.TurnOrdinal&&EncounterHistory.InCurrent(s,d.Revision)));
        }
        private static RuleQuantity RemainingMovement(Snapshot s,string actor) {
            if(s.WorldSchedule==null)return new RuleQuantity(WalkingLedger(s).Remaining(WalkingSpeed(s,actor)));
            var a=s.WorldIntervals.Single(x=>x.ActorId==actor);var maximum=new RuleQuantity(WalkingSpeed(s,actor)).Scale(a.DashPaid?2:1);
            return maximum>a.MovementSpent?maximum-a.MovementSpent:default;
        }
        private static void SpendMovement(Snapshot s,string actor,long cost) {
            if(s.WorldSchedule!=null) {
                if(new RuleQuantity(cost)>RemainingMovement(s,actor))throw new ArgumentException("Insufficient shared movement.");
                s.WorldIntervals=s.WorldIntervals.Select(a=>a.ActorId==actor?a.Spend(new RuleQuantity(cost)):a).ToArray();return;
            }
            var ledger=WalkingLedger(s).Spend(cost,WalkingSpeed(s,actor));
            s.ActorMovement=s.ActorMovement.Select(m=>m.ActorId==actor?new ActorMovementRecord(m.ActorId,m.BaseWalkingSpeed,m.TurnOrdinal,ledger.Spent):m).ToArray();
        }
        private static void StartMovement(Snapshot s)
        {
            if(s.SchemaVersion>=Snapshot.TacticalMovementSchema)StartTactical(s);
            if(s.SchemaVersion<Snapshot.PostureSchema)return;
            s.ActorMovement=s.ActorMovement.Select(m=>m.ActorId==s.Encounter.CurrentActor?new ActorMovementRecord(m.ActorId,m.BaseWalkingSpeed,s.Encounter.TurnOrdinal):m).ToArray();
        }
        internal static bool HasStance(Snapshot s)=>s.Stances.Any(t=>t.TurnOrdinal==s.Encounter.TurnOrdinal&&EncounterHistory.InCurrent(s,t.Revision));
        public string Resolve(Snapshot s,Command c)
        {
            if(!Admitted(c.Kind))return "ClubCommandNotImplemented";
            bool combat=c.Kind==CommandKind.SelectCombatStance||c.Kind==CommandKind.AttackClub||c.Kind==CommandKind.ResolveKnockout
                ||c.Kind==CommandKind.AttackUnarmed||c.Kind==CommandKind.RespondOpportunityAttack||c.Kind==CommandKind.RespondPress;
            if(c.Inventory!=null||combat!=(c.Combat!=null))return "UnexpectedCombatPayload";
            var pending=s.MeleeAttacks.SingleOrDefault(a=>a.Pending);
            if(pending!=null) {
                if(c.Kind!=CommandKind.ResolveKnockout)return "KnockoutChoicePending";
                string choiceError=Complete(s,c,pending);if(choiceError==null&&tactical!=null)AdvanceTacticalFlow(s);return choiceError;
            }
            if(c.Kind==CommandKind.DispatchConditionEvent)return DispatchCondition(s,c);
            if(tactical!=null&&(PendingMove(s)!=null||CurrentPressOffer(s)!=null))return ResolveTacticalChoice(s,c);
            if(c.Kind==CommandKind.RespondOpportunityAttack||c.Kind==CommandKind.RespondPress)return "NoPendingMovementChoice";
            if(c.Kind==CommandKind.ResolveKnockout)return "NoPendingKnockout";
            if(c.Kind==CommandKind.BeginFixedEncounter||c.Kind==CommandKind.AdvanceClock) {
                string error=encounter.Resolve(s,c);if(error!=null)return error;
                AdvanceConditions(s);
                if(c.Kind==CommandKind.BeginFixedEncounter){StartMovement(s);ActorLifeRules.RegularStart(s,0);}return null;
            }
            var e=s.Encounter;
            bool moveCommand=c.Kind==CommandKind.TacticalStep||c.Kind==CommandKind.TacticalRepositionStep;
            if(e==null||c.Actor!=e.CurrentActor||!moveCommand&&(c.X!=0||c.Y!=0)||combat&&c.Combat.TurnId!=e.CurrentTurnId)return "WrongRegularTurn";
            if(c.Kind==CommandKind.EndRegularTurn) {
                if(Aware(s,c.Actor)&&!HasStance(s))return "StanceRequired";
                string error=encounter.Resolve(s,c);if(error!=null)return error;
                AdvanceConditions(s);StartMovement(s);ActorLifeRules.RegularStart(s,s.Encounter.TurnOrdinal);return null;
            }
            if(!ActorLifeRules.CanAct(s,c.Actor))return "ActorCannotAct";
            string restriction=ConditionActionFailure(s,c.Kind,c.Actor);if(restriction!=null)return restriction;
            if(c.Kind==CommandKind.StandFromProne||c.Kind==CommandKind.DropProne) {
                if(c.Target!=e.CurrentTurnId)return "WrongRegularTurn";
                var before=s.Lives.Single(l=>l.ActorId==c.Actor);bool standing=c.Kind==CommandKind.StandFromProne;
                if(standing&&!HasStance(s))return "StanceRequired"; // Standing uses current Speed, including Guarded.
                if(before.Prone!=standing)return standing?"ActorNotProne":"ActorAlreadyProne";
                if(standing) {
                    long speed=WalkingSpeed(s,c.Actor);
                    if(speed==0)return "ZeroSpeedCannotStand";
                    if(RemainingMovement(s,c.Actor)<new RuleQuantity(speed/2))return "InsufficientMovement";
                    SpendMovement(s,c.Actor,speed/2);
                }
                // Dropping voluntarily changes no position, spent cost or stance allowance. Zero Speed alone does not prohibit it.
                if(WithConditions(s)) {
                    if(standing)AppendCondition(s,c.Actor,ConditionOperation.Cure("host.stand."+N(s.Revision+1),s.Conditions.Single(j=>j.Target==c.Actor).Now,"Prone"));
                    else AddPhysicalProne(s,c.Actor,"voluntary-prone");
                } else s.Lives=s.Lives.Select(l=>l.ActorId==c.Actor?ActorLifeRules.Record(l.ActorId,ActorLifeRules.Read(l),!standing,l.HeldItems):l).ToArray();return null;
            }
            if(c.Kind==CommandKind.SelectCombatStance) {
                if(c.Target!=""||c.Combat.WeaponId!=""||c.Combat.Stance==0||c.Combat.Knockout!=AttackKnockoutMode.OrdinaryOutcome||c.Combat.Choice||c.Combat.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidStanceRequest";
                if(HasStance(s))return "StanceAlreadySelected";
                if((CombatStance)c.Combat.Stance==CombatStance.Carrying)return "NoApplicableCargoPenalty";
                if(s.Stances.Length==128)return "StanceHistoryCapacityReached";
                s.Stances=s.Stances.Concat(new[]{new StanceSelectionRecord(c.Actor,s.Revision+1,e.TurnOrdinal,(CombatStance)c.Combat.Stance,FixedEncounterRules.Start(e,e.TurnOrdinal+e.Order.Count))}).ToArray();return null;
            }
            if(c.Kind==CommandKind.TacticalStep) {
                if(c.Target!=e.CurrentTurnId)return "WrongRegularTurn";
                if(!HasStance(s))return "StanceRequired";
                return BeginOrdinaryStep(s,c);
            }
            if(c.Kind==CommandKind.TacticalRepositionStep) {
                if(c.Target!=e.CurrentTurnId)return "WrongRegularTurn";
                return BeginTacticalRepositionStep(s,c);
            }
            if(ActionSpent(s))return "ActionAlreadySpent";
            if(c.Kind==CommandKind.Disengage) {
                if(c.Target!=e.CurrentTurnId)return "WrongRegularTurn";
                var actor=TacticalActor(s,c.Actor);SetTactical(s,new ActorTacticalRecord(actor.ActorId,actor.LastRegularStart,actor.ReactionAvailable,actor.MobileFeet,actor.PressConsumed,e.TurnOrdinal));return null;
            }
            if(c.Kind==CommandKind.EncounterDash)return encounter.Resolve(s,c);
            if(!HasStance(s))return "StanceRequired";
            return Attack(s,c);
        }
        private static CombatDamageRoll DamageRecord(int[] dice,long total,long diceWords,uint seed,RolledDamage result)
            =>new CombatDamageRoll(dice,total,diceWords,seed,result.NextRandomState,result.WordsConsumed,result.WoundRoll?.Natural??0,result.InjuryD6??0,result.StableD4??0);
        private static string Attack(Snapshot s,Command c,bool opportunity=false)
        {
            string physical=PhysicalAttackFailure(s,c.Actor);if(physical!=null)return physical;
            var request=c.Combat;
            if(request.Stance!=0||request.Choice||s.SchemaVersion<Snapshot.TacticalMovementSchema&&request.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidAttackRequest";
            if(s.MeleeAttacks.Length==128)return "AttackHistoryCapacityReached";
            bool unarmed=c.Kind==CommandKind.AttackUnarmed;
            if(unarmed&&(s.SchemaVersion<Snapshot.TacticalMovementSchema||request.WeaponId!=""))return "InvalidUnarmedRequest";
            var weapon=s.Clubs.SingleOrDefault(w=>w.Id==request.WeaponId);
            var attacker=s.Lives.Single(l=>l.ActorId==c.Actor);
            if(!unarmed&&(weapon==null||weapon.ProfileId!=ClubProfile||weapon.HeldBy!=c.Actor||weapon.CustodianId!=c.Actor||!attacker.HeldItems.Contains(weapon.Id)))return "ClubNotHeld";
            var target=s.Lives.SingleOrDefault(l=>l.ActorId==c.Target);
            if(target==null||target.ActorId==c.Actor||target.Dead)return "InvalidLivingTarget";
            if(!DamageConditionCapacity(s,c.Target))return "ConditionHistoryCapacityReached";
            var a=s.Actors.Single(x=>x.Id==c.Actor);var t=s.Actors.Single(x=>x.Id==c.Target);
            if(PlanarCombatGeometry.DistanceFeet(new CombatCell(a.X,a.Y),new CombatCell(t.X,t.Y))>5)return "TargetOutOfReach";
            var modifiers=PlaytestConditions.Attack(CombatConditions(s,c.Actor),CombatConditions(s,c.Target),attackerInvisibleLocationKnown:true,targetInvisibleLocationKnown:true);
            var incomingEffects=SoldierTacticalFeatures.ForAttack(s,c.Actor,c.Target);
            bool advantage=modifiers.AdvantagePresent,disadvantage=modifiers.DisadvantagePresent||incomingEffects.WarningShot;
            int modifier=checked((attacker.LinkedInjuries.Contains((int)Injury.OffensiveTrauma)?-1:0)-incomingEffects.CoveringFirePenalty
                +incomingEffects.TacticalAssessmentBonus); // STR10, explicitly no Club proficiency grant.
            var defense=ActiveStance(s,c.Target);int dexterity=s.Characters.Single(x=>x.ActorId==c.Target).Abilities[1];
            int ac=checked(CharacterAdvancementRules.ArmorClass(s,c.Target,dexterity)+(defense?.Kind==CombatStance.Aggressive?-2:defense?.Kind==CombatStance.Guarded?1:0)
                +CharacterAdvancementRules.DefensivePositioningBonus(s,c.Target));
            string attackId="attack."+N(s.Revision+1);
            string captureFailure=SoldierTacticalFeatures.CaptureAndConsume(s,attackId,c.Actor,c.Target,"",out _);if(captureFailure!=null)return captureFailure;
            uint before=s.RandomState;var roll=PlaytestDice.RollD20(before,advantage?1:0,disadvantage?1:0);
            var hit=PlaytestRolls.AttackRoll(roll.Natural,modifier,ac);bool critical=hit.Hit&&(hit.Critical||modifiers.CriticalIfHit);
            var attack=new CombatAttackRoll(roll.First,roll.Second??0,roll.Natural,modifier,ac,hit.Hit,critical,before,roll.NextRandomState,roll.WordsConsumed);
            uint next=roll.NextRandomState;CombatDamageRoll damage;bool pending=false;
            if(hit.Hit) {
                var dice=new int[unarmed?0:critical?2:1];long words=0;
                for(int i=0;i<dice.Length;i++){var d=DiceStream.Draw(next,4);dice[i]=d.Value+1;next=d.NextState;words=checked(words+d.WordsConsumed);}
                int flat=ActiveStance(s,c.Actor)?.Kind==CombatStance.Aggressive?2:0;
                long total=unarmed?PrototypeUnarmed.Damage(10,flat):dice.Sum()+flat;
                total=CharacterAdvancementRules.ReduceIncomingDamage(s,c.Target,total);
                if(WithConditions(s)&&ConditionsFor(s,c.Target).View().Has(ConditionKind.Petrified))total=PlaytestConditions.PetrifiedDamage(total);
                var targetCharacter=s.Characters.Single(x=>x.ActorId==c.Target);
                int constitutionSave=checked(PlaytestCharacters.AbilityModifier(targetCharacter.Abilities[2])
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,c.Target,"CON"));
                var result=PlaytestDamageDice.Resolve(ActorLifeRules.Read(target),total,s.RuleClock,next,constitutionSaveModifier:constitutionSave,
                    critical:critical,melee:true,knockout:(KnockoutInstruction)request.Knockout);
                damage=DamageRecord(dice,total,words,next,result);next=result.NextRandomState;pending=result.Pending!=null;
                if(pending&&s.Receipts.Length>=511)return "ContinuationCapacityReached";
                if(!pending)ApplyLife(s,target,result.Outcome.State);
                if(request.PressInstruction==PressHitInstruction.ArmOrReplace&&(s.SchemaVersion<Snapshot.TacticalMovementSchema||s.Encounter.CurrentActor==c.Actor&&!TacticalActor(s,c.Actor).PressConsumed)) {
                    var press=new PressRecord(c.Actor,c.Target,s.Revision+1,FixedEncounterRules.Start(s.Encounter,s.Encounter.TurnOrdinal+s.Encounter.Order.Count));
                    s.Presses=s.Presses.Where(p=>p.ActorId!=c.Actor).Concat(new[]{press}).ToArray();
                }
            } else damage=new CombatDamageRoll(Array.Empty<int>(),0,0,next,next,0,0,0,0);
            s.RandomState=next;
            var record=new MeleeAttackRecord(attackId,s.Revision+1,pending?0:s.Revision+1,s.Encounter.TurnOrdinal,c.Actor,c.Target,unarmed?CombatProfileIds.OrdinaryUnarmed:weapon.Id,s.RuleClock,request.Knockout,attack,damage,opportunity,request.PressInstruction);
            s.MeleeAttacks=s.MeleeAttacks.Concat(new[]{record}).ToArray();return null;
        }
        private static string Complete(Snapshot s,Command c,MeleeAttackRecord pending)
        {
            var r=c.Combat;
            if(r==null||c.Actor!=pending.AttackerId||c.Target!=pending.Id||r.TurnId!=s.Encounter.CurrentTurnId||c.X!=0||c.Y!=0
                ||r.WeaponId!=""||r.Stance!=0||r.Knockout!=AttackKnockoutMode.OrdinaryOutcome||r.PressInstruction!=PressHitInstruction.ArmOrReplace)return "InvalidKnockoutChoice";
            var before=s.Lives.Single(l=>l.ActorId==pending.TargetId);var d=pending.Damage;
            // Reconstruct the immutable continuation from its retained seed and unchanged target facts.
            // The prior rolls are verified, never applied to the world random stream a second time.
            var targetCharacter=s.Characters.Single(x=>x.ActorId==pending.TargetId);
            int constitutionSave=checked(PlaytestCharacters.AbilityModifier(targetCharacter.Abilities[2])
                +CharacterAdvancementRules.SaveProficiencyBonus(s,pending.TargetId,"CON"));
            var prior=PlaytestDamageDice.Resolve(ActorLifeRules.Read(before),d.Total,pending.At,d.EffectsSeed,constitutionSaveModifier:constitutionSave,
                critical:pending.Attack.Critical,melee:true,knockout:KnockoutInstruction.AskIfEligible);
            if(prior.Pending==null||!d.SameAs(DamageRecord(d.Dice.ToArray(),d.Total,d.DiceWords,d.EffectsSeed,prior))||s.RandomState!=prior.NextRandomState)return "InvalidPendingKnockout";
            var result=prior.Pending.Complete(r.Choice);s.RandomState=result.NextRandomState;ApplyLife(s,before,result.Outcome.State);
            var resolved=new MeleeAttackRecord(pending.Id,pending.Revision,s.Revision+1,pending.TurnOrdinal,pending.AttackerId,pending.TargetId,pending.WeaponId,pending.At,
                pending.Instruction,pending.Attack,DamageRecord(d.Dice.ToArray(),d.Total,d.DiceWords,d.EffectsSeed,result),pending.Opportunity,pending.PressInstruction);
            s.MeleeAttacks=s.MeleeAttacks.Select(a=>a.Id==pending.Id?resolved:a).ToArray();return null;
        }
        internal static void ApplyLife(Snapshot s,ActorLifeRecord before,LifeState after)
        {
            bool newlyUnconscious=!after.Dead&&after.Hp==0&&before.Hp>0;
            // The initial HP/Wound facts and bounded Club damage exclude death while still holding equipment.
            bool dropEquipment=newlyUnconscious||after.Dead;
            var record=ActorLifeRules.Record(before.ActorId,after,before.Prone||newlyUnconscious&&!WithConditions(s),dropEquipment?Array.Empty<string>():before.HeldItems);
            s.Lives=s.Lives.Select(l=>l.ActorId==record.ActorId?record:l).ToArray();
            if(newlyUnconscious) {
                if(WithConditions(s))AddPhysicalProne(s,before.ActorId,"zero-hp");
            }
            if(dropEquipment) {
                var a=s.Actors.Single(x=>x.Id==before.ActorId);
                s.Clubs=s.Clubs.Select(w=>w.HeldBy==a.Id?new ClubInstance(w.Id,w.ProfileId,w.OwnerId,w.CustodianId,"",a.X,a.Y):w).ToArray();
                s.RepeatingCrossbows=s.RepeatingCrossbows.Select(w=>w.HeldBy==a.Id?w.DropAt(a.X,a.Y):w).ToArray();
            }
        }
        public string ValidateState(Snapshot s)
        {
            try {
                if(s.SchemaVersion!=(conditions!=null?Snapshot.ConditionSchema:tactical!=null?Snapshot.TacticalMovementSchema:Posture?Snapshot.PostureSchema:Snapshot.ClubAttackSchema))return "WrongClubSchema";
                string error=inventory.ValidateFillingState(s,true,true,true,Posture,tactical!=null,conditions!=null);if(error!=null)return error;
                if(s.Crops.Length+s.CropFood.Length+s.Handling.Length+s.VesselMoves.Length+s.Intakes.Length+s.WaterFills.Length!=0
                    ||s.Work.WorkerIntervals.Count+s.Work.Reservations.Count!=0||s.Receipts.Length!=s.Revision)return "InvalidClubFixture";
                var replay=Initial();
                foreach(var receipt in s.Receipts.OrderBy(r=>r.Revision)) {
                    var command=CommandHistory.Read(receipt);
                    if(!Admitted(command.Kind)||!replay.Actors.Any(a=>a.Id==command.Actor)||command.Inventory!=null
                        ||s.SchemaVersion<Snapshot.TacticalMovementSchema&&command.Combat?.PressInstruction==PressHitInstruction.KeepExisting)return "InvalidClubReceipt";
                    if(command.ExpectedRevision!=replay.Revision||Resolve(replay,command)!=null)return "InvalidClubCommandHistory";
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
            return Tables(s.ClosedEncounters,r.ClosedEncounters,(a,b)=>a.ClosedRevision==b.ClosedRevision&&a.ClosedAt==b.ClosedAt&&a.Reason==b.Reason
                    &&a.Encounter.Id==b.Encounter.Id&&a.Encounter.Origin==b.Encounter.Origin&&a.Encounter.Order.SequenceEqual(b.Encounter.Order)&&a.Encounter.StartRevisions.SequenceEqual(b.Encounter.StartRevisions))
                &&Tables(s.Conditions,r.Conditions,(a,b)=>a.SameAs(b))
                &&Tables(s.Actors,r.Actors,(a,b)=>a.Id==b.Id&&a.X==b.X&&a.Y==b.Y&&a.Tokens==b.Tokens)
                &&Tables(s.Objects,r.Objects,(a,b)=>a.Id==b.Id&&a.X==b.X&&a.Y==b.Y&&a.Opened==b.Opened)
                &&Tables(s.Characters,r.Characters,(a,b)=>a.ActorId==b.ActorId&&a.ProfileId==b.ProfileId&&a.Abilities.SequenceEqual(b.Abilities)
                    &&a.Levels.Count==b.Levels.Count&&!a.Levels.Where((x,i)=>x.ClassName!=b.Levels[i].ClassName||x.BaseHp!=b.Levels[i].BaseHp).Any())
                &&Tables(s.Lives,r.Lives,(a,b)=>a.SameAs(b))&&s.LifeEvents.Length==r.LifeEvents.Length
                &&!s.LifeEvents.Where((a,i)=>a.Revision!=r.LifeEvents[i].Revision||!a.SameOutcome(r.LifeEvents[i])).Any()
                &&Tables(s.EncounterDashes,r.EncounterDashes,(a,b)=>a.ActorId==b.ActorId&&a.Revision==b.Revision&&a.TurnOrdinal==b.TurnOrdinal)
                &&Tables(s.Clubs,r.Clubs,(a,b)=>a.SameAs(b))&&Tables(s.Stances,r.Stances,(a,b)=>a.SameAs(b))
                &&Tables(s.ActorMovement,r.ActorMovement,(a,b)=>a.SameAs(b))
                &&Tables(s.TacticalActors,r.TacticalActors,(a,b)=>a.SameAs(b))&&Tables(s.TacticalMoves,r.TacticalMoves,(a,b)=>a.SameAs(b))&&Tables(s.PressOffers,r.PressOffers,(a,b)=>a.SameAs(b))
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
