#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private BishopEntryRecord bishopDeclaration;
        internal TestOnlySharedWorldPolicy EnableBishopEntry(ClericInitialSelection initial,ClericRepertoireSelection repertoire,
            ClericMilestoneDeclaration opening,BishopEntryRecord declaration,bool companionConsents=true,bool directorAuthorizes=true)
        {
            if(declaration==null || declaration.Departure!=null)throw new ArgumentException("A fresh announced Bishop objective is required.");
            EnablePostRecoveryEncounter(initial,repertoire,opening,companionConsents,directorAuthorizes);
            bishopDeclaration=declaration;
            ContentFingerprint=BishopProfile.FingerprintPrefix+RetreatHash(string.Join("|",ContentFingerprint,
                declaration.DeclarationDigest,BishopProfile.Approval,BishopProfile.MechanicsApproval,
                BishopProfile.InvocationCardSha256,BishopProfile.AuraCardSha256,
                "earned3-preserves-current|radiance-invocation|conscious-perceived-aura|own-observed-guidance-dispel|historical-capacity-and-payment"));
            return this;
        }
        private void InitializeBishopEntry(Snapshot s)
        {
            if(bishopDeclaration!=null)s.BishopEntry=bishopDeclaration;
        }
        private static bool BishopDepartureEdge(WorldTraversalRecord edge) => edge!=null && edge.ActorId==ClericRpProfile.Actor
            && !edge.Running && edge.FromX==1 && edge.FromY==3 && edge.ToX==2 && edge.ToY==3;
        private static void RecordBishopDepartureStart(Snapshot s,Command c,WorldTraversalRecord edge)
        {
            if(s.BishopEntry==null || s.BishopEntry.Departure?.Complete==true || !BishopDepartureEdge(edge))return;
            var rest=s.ClericLongRestSettlements.FirstOrDefault(x=>x.Benefit==ClericLongRestBenefit.Eligible);
            if(rest==null)return;
            var rite=s.HealingRites.LastOrDefault(x=>x.ActorId==ClericRpProfile.Actor && x.TargetId==ConnectedVialRules.CarrierId
                && x.ActualGain>0 && x.RpPaid==2 && x.Revision>rest.Revision && x.At>rest.At);
            if(rite==null)return;
            s.BishopEntry=s.BishopEntry.WithDeparture(new BishopDepartureProof(rest.RestId,rite.CommandId,rite.Revision,
                c.Id,s.Revision+1,s.RuleClock));
        }
        private static void CompleteBishopDeparture(Snapshot s,Command initiating,WorldTraversalRecord edge)
        {
            var proof=s.BishopEntry?.Departure;
            if(proof==null || proof.Complete || !BishopDepartureEdge(edge) || edge.StartedRevision!=proof.StepRevision
                || initiating==null || s.RuleClock<=proof.StartedAt
                || s.Lives.Any(x=>(x.ActorId==ClericRpProfile.Actor || x.ActorId==ConnectedVialRules.CarrierId)&&x.Dead))return;
            // The caller supplies only an actually completed five-foot edge, after tied life/debt consequences.
            s.BishopEntry=s.BishopEntry.WithDeparture(proof.Finish(initiating.Id,s.Revision+1,s.RuleClock));
        }
        private string AssessBishopAdvancement(Snapshot s,Command c)
        {
            if(s.BishopEntry==null || c.Actor!=ClericRpProfile.Actor || c.Target!=BishopProfile.Milestone)return "UndeclaredMilestone";
            if(s.BishopEntry.Departure?.Complete!=true)return "MilestoneObjectiveIncomplete";
            if(c.Kind==CommandKind.AwardCharacterMilestone) {
                if(c.Advancement!=null)return "InvalidMilestoneAward";
                if(s.CharacterMilestones.Any(x=>x.ActorId==c.Actor && x.MilestoneId==c.Target))return "MilestoneAlreadyAwarded";
                return s.CharacterMilestones.Length>=256?"MilestoneCapacityReached":null;
            }
            if(c.Kind!=CommandKind.AdvanceCharacterLevel || c.Advancement==null)return "CharacterAdvancementCommandNotImplemented";
            var award=s.CharacterMilestones.SingleOrDefault(x=>x.ActorId==c.Actor && x.MilestoneId==c.Target);
            if(award==null)return "MilestoneNotAvailable";
            if(award.ConsumedRevision!=0)return "MilestoneAlreadyConsumed";
            if(s.InventoryCombat || s.Encounter!=null)return "TacticalControlActive";
            if(PendingCalendarChoice(s) || ManufacturingChoicePending(s) || HasPendingRecoveryOffer(s) || s.ManufacturingAdvance!=null)
                return "TacticalChoicePending";
            if(CharacterAdvancementRules.Busy(s,c.Actor) || OrdinaryInventory.Busy(s,c.Actor))return "CharacterBusy";
            if(!CapableWorker(s,c.Actor) || !Permissions(s,c.Actor).Action)return "ConditionPreventsAdvancement";
            var character=s.Characters.Single(x=>x.ActorId==c.Actor);
            if(character.ProfileId!=ClericRpProfile.CharacterProfile || character.Levels.Count!=2
                || character.Levels.Any(x=>x.ClassName!="Cleric") || character.Levels[0].BaseHp!=8 || character.Levels[1].BaseHp!=5
                || !character.Abilities.SequenceEqual(new[]{10,10,10,10,14,10}))return "UnsupportedAdvancementPath";
            if(!BishopProfile.ValidChoices(c.Advancement))return "BishopAdvancementChoiceUnsupported";
            var row=ClassAdvancementScheduleCatalog.Get("Cleric",3);
            if(row==null || row.RequiredSelections!=2 || row.MinimumActiveSelections!=1 || row.HasAsiOrFeatOpportunity!=false
                || !row.Bands.SequenceEqual(new[]{"Arch"}))return "ClassScheduleNeedsBinding";
            var options=ClassAdvancementOptionCatalog.Candidates(row);
            foreach(string id in c.Advancement.FeatureIds) {
                var card=ClassAdvancementOptionCatalog.Get("Cleric",id);
                if(card==null || !options.Contains(card) || card.HasPathConstraint || card.HasDeclaredPrerequisite)return "FeatureOutsideClassSchedule";
                if(s.CharacterFeatureGrants.Any(x=>x.ActorId==c.Actor && x.FeatureId==id))return "FeatureAlreadyOwned";
            }
            if(s.CharacterAdvancements.Count(x=>x.ActorId==c.Actor)!=1 || s.ClericInvocationPath?.PathId!=ClericSettlementProfile.Radiance
                || s.ConvictionCapacity?.PoolAcquiredRevision==0 || s.ConvictionBalance==null)return "PriorClericSettlementRequired";
            if(s.CharacterAdvancements.Length>=128 || s.CharacterFeatureGrants.Length+2>256 || s.CharacterHitDice.Length>=1280)
                return "AdvancementCapacityReached";
            var dice=s.CharacterHitDice.Where(x=>x.ActorId==c.Actor).OrderBy(x=>x.LevelOrdinal).ToArray();
            if(dice.Length!=2 || dice.Any(x=>x.ClassName!="Cleric" || x.DieSize!=8) || dice[0].LevelOrdinal!=1 || dice[1].LevelOrdinal!=2)
                return "HitDieLedgerMismatch";
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);
            var pool=s.ResonancePools.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(life.MaximumHp!=13 || pool==null || pool.Maximum!=4)return "AdvancementCapacityBasisMismatch";
            var known=s.KnownSpells.Where(x=>x.ActorId==c.Actor).ToArray();
            if(known.Length!=6 || known.Any(x=>!x.MatchesSource()) || known.Any(x=>x.SpellId==BishopProfile.Dispel)
                || BishopProfile.DispelSource.AccessFor("Cleric").MinimumClassLevel!=3)return "ClericEarnedRepertoireChoiceUnavailable";
            return null;
        }
        private static void SettleBishopAdvancement(Snapshot s,Command c)
        {
            long revision=s.Revision+1;
            if(c.Kind==CommandKind.AwardCharacterMilestone) {
                s.CharacterMilestones=s.CharacterMilestones.Append(new CharacterMilestoneRecord(c.Target,c.Actor,revision)).ToArray();return;
            }
            var before=s.Characters.Single(x=>x.ActorId==c.Actor);
            var levels=before.Levels.Append(new CharacterLevelFact("Cleric",5)).ToArray();
            var character=new ActorCharacterRecord(c.Actor,before.ProfileId,before.Abilities,levels);
            long maximum=PlaytestCharacters.BaseMaximumHp(levels.Select(x=>new CharacterLevelRecord(x.ClassName,x.BaseHp)).ToArray(),
                before.Abilities[(int)CharacterAbility.Constitution]).BaseMaximum;
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);long current=PlaytestCharacters.ClampAfterCapacityChange(life.Hp,maximum);
            var record=new CharacterAdvancementRecord(c.Actor,c.Target,revision,2,3,"Cleric",3,5,HitPointGainMethod.FixedAverage,
                life.MaximumHp,maximum,life.Hp,current,BishopProfile.SelectedCards.ToArray());
            s.Characters=s.Characters.Select(x=>x.ActorId==c.Actor?character:x).ToArray();
            s.Lives=s.Lives.Select(x=>x.ActorId!=c.Actor?x:new ActorLifeRecord(x.ActorId,maximum,current,x.TemporaryHp,x.LinkedInjuries,
                x.Stable,x.Dead,x.UsesDeathSaves,x.DeathSuccesses,x.DeathFailures,x.StableUntil,x.LastDeathTurn,x.Prone,x.HeldItems)).ToArray();
            s.CharacterHitDice=s.CharacterHitDice.Append(new CharacterHitDieRecord(c.Actor,3,"Cleric",8,false)).ToArray();
            s.CharacterFeatureGrants=s.CharacterFeatureGrants.Concat(BishopProfile.SelectedCards.Select(id=>
                new CharacterFeatureGrantRecord(c.Actor,id,"Cleric",3,c.Target,revision))).ToArray();
            s.ResonancePools=s.ResonancePools.Select(x=>x.ActorId==c.Actor?x.ReconcileCapacity(DeriveResonanceMaximum(character)):x).ToArray();
            s.CharacterMilestones=s.CharacterMilestones.Select(x=>x.ActorId==c.Actor && x.MilestoneId==c.Target?x.Consume(revision):x).ToArray();
            s.CharacterAdvancements=s.CharacterAdvancements.Append(record).ToArray();
            s.KnownSpells=s.KnownSpells.Append(KnownSpellRecord.FromSource(c.Actor,BishopProfile.Dispel,SpellAcquisitionOrigin.EarnedClassLevel,
                3,3,BishopProfile.RepertoireEntitlement,c.Target,revision)).ToArray();
        }
        private IEnumerable<Command> DiscoverBishopAdvancement(Snapshot s,string actor)
        {
            if(s.BishopEntry==null || actor!=ClericRpProfile.Actor || s.BishopEntry.Departure?.Complete!=true)yield break;
            string id="option."+s.Revision.ToString(System.Globalization.CultureInfo.InvariantCulture)+".bishop";
            var command=s.CharacterMilestones.Any(x=>x.ActorId==actor && x.MilestoneId==BishopProfile.Milestone)
                ?new Command(id,actor,s.Revision,CommandKind.AdvanceCharacterLevel,BishopProfile.Milestone,
                    advancement:new CharacterAdvancementRequest(BishopProfile.SelectedCards.ToArray(),"",BishopProfile.Dispel))
                :new Command(id,actor,s.Revision,CommandKind.AwardCharacterMilestone,BishopProfile.Milestone);
            if(AssessBishopAdvancement(s,command)==null)yield return command;
        }
    }
}
#endif
