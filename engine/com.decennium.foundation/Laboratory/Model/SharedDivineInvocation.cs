#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    internal static class DivineInvocationRules
    {
        internal static void ValidateCureTrigger(Snapshot s,Command c,DivineInvocationRecord use)
        {
            if(c.Kind!=CommandKind.UseDivineInvocation||c.DivineInvocation?.CurePreference==RadianceCurePreference.None
                ||use==null||!BishopProfile.Invocations(s).Contains(use)||use.CommandId!=c.Id||use.Revision!=s.Revision+1
                ||use.ActorId!=c.Actor||!use.Choice.TargetIds.SequenceEqual(c.DivineInvocation.TargetIds)||use.Choice.CureTargetId!=c.DivineInvocation.CureTargetId||use.Choice.CurePreference!=c.DivineInvocation.CurePreference||use.At!=s.RuleClock
                ||RadianceRules.OwnTurnFailure(s,c.Actor)!=null||!BishopProfile.Earned(s)
                ||s.ResonancePools.Single(x=>x.ActorId==c.Actor).Current!=use.RpAfter
                ||s.ConvictionBalance?.Current!=use.ConvictionAfter||s.CastingStrain.Single(x=>x.ActorId==c.Actor).Dissonance!=use.DissonanceAfter
                ||!s.WorldIntervals.Single(x=>x.ActorId==c.Actor).ActionSpent||s.RandomState!=use.RandomAfter
                ||use.Recipients.Any(x=>s.Lives.Single(l=>l.ActorId==x.TargetId).Dead||s.Lives.Single(l=>l.ActorId==x.TargetId).Hp!=x.HpAfter))
                throw new ArgumentException("Invocation cure requires its actual staged paid producer.");
            var draw=DiceStream.Draw(use.RandomBefore,8);
            if(draw.Value+1!=use.Die||draw.NextState!=use.RandomAfter||draw.WordsConsumed!=use.WordsConsumed)
                throw new ArgumentException("Invocation shared healing draw differs.");
        }
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private string AssessDivineInvocation(Snapshot s,Command c)
        {
            string shape=BishopProfile.InvocationPayloadFailure(s,c);if(shape!=null)return shape;
            if(s.BishopEntry==null||c.Actor!=ClericRpProfile.Actor||!BishopProfile.Earned(s)
                ||!s.CharacterFeatureGrants.Any(x=>x.FeatureId==BishopProfile.Invocation&&BishopProfile.ValidGrant(s,x))
                ||!RadianceRules.Owns(s,c.Actor))return "DivineInvocationNotOwned";
            var pool=s.ResonancePools.SingleOrDefault(x=>x.ActorId==c.Actor);
            if(pool==null||pool.Maximum!=DeriveResonanceMaximum(s.Characters.Single(x=>x.ActorId==c.Actor)))return "ResonancePoolUnavailable";
            if(pool.Current<3)return "InsufficientResonance";
            if(s.ConvictionBalance==null)return "ConvictionBalanceUnavailable";
            if(s.ConvictionBalance.Current<2)return "InsufficientConviction";
            string context=RadianceRules.OwnTurnFailure(s,c.Actor);if(context!=null)return context;
            string action=CastingActionFailure(s,c);if(action!=null)return action;
            if(s.AbilityRecharges.Any(x=>x.ActorId==c.Actor&&x.AbilityId==BishopProfile.Invocation&&x.Remaining>0))return "DivineInvocationRecharging";
            if(s.BishopEntry.Invocations.Count>=128)return "InvocationHistoryFull";
            var turn=CurrentMagicalActionOrigin(s,c.Actor);
            if(s.BishopEntry.Invocations.Any(x=>x.Turn.SameAs(turn)))return "InvocationAlreadyUsedThisTurn";
            foreach(string id in c.DivineInvocation.TargetIds) {
                var target=s.Actors.SingleOrDefault(x=>x.Id==id);var life=s.Lives.SingleOrDefault(x=>x.ActorId==id);
                if(target==null||life==null||life.Dead||!SoldierTacticalFeatures.IsAlly(s,c.Actor,id))return "InvocationTargetUnavailable";
                // This active producer uses the existing stationary spell/healing access envelope.
                if(s.WorldTraversals.Any(x=>x.ActorId==id))return "InvocationRequiresStationaryAccess";
                var actor=s.Actors.Single(x=>x.Id==c.Actor);
                if(PlanarCombatGeometry.DistanceFeet(new CombatCell(actor.X,actor.Y),new CombatCell(target.X,target.Y))>30
                    ||!ObservationGeometry.LineOfEffectClear(s,c.Actor,id)
                    ||id!=c.Actor&&!ObservationRules.CanSee(s,c.Actor,id))return "InvocationTargetUnavailable";
                if(s.PeriodicRiders.Any(x=>x.TargetId==id&&x.Present))return "InvocationSourceInteractionUnsupported";
            }
            if(c.DivineInvocation.CurePreference!=RadianceCurePreference.None) {
                if(!Validation.ValidId(c.Id+".invocation.cure")||!Validation.ValidId(c.Id+".invocation.sync"))return "InvocationIdentityCapacityReached";
                var journal=s.Conditions.Single(x=>x.Target==c.DivineInvocation.CureTargetId);
                if(journal.Now.Time>s.RuleClock)return "ConditionCalendarMismatch";
                int count=journal.Now.Equals(RadianceRules.TargetStamp(s,journal.Target))?1:2;
                if(journal.Operations.Count+count>ConditionJournal.MaxOperations)return "ConditionHistoryCapacityReached";
            }
            return null;
        }
        private CommandQueryResult QueryDivineInvocation(Snapshot s,Command c)
        {
            string failure=AssessDivineInvocation(s,c);
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,failure==null?
                new[]{new CommandCost("action","",1),new CommandCost("rp",c.Actor,3),new CommandCost("conviction",c.Actor,2)}:null);
        }
        private string ResolveDivineInvocation(Snapshot s,Command c)
        {
            string failure=AssessDivineInvocation(s,c);if(failure!=null)return failure;
            var pool=s.ResonancePools.Single(x=>x.ActorId==c.Actor);var conviction=s.ConvictionBalance;
            var strain=s.CastingStrain.Single(x=>x.ActorId==c.Actor);var turn=CurrentMagicalActionOrigin(s,c.Actor);
            var draw=DiceStream.Draw(s.RandomState,8);var rows=new List<InvocationHealingRecord>();
            uint random=s.RandomState;
            SetInterval(s,Interval(s,c.Actor).PayAction());
            s.ResonancePools=s.ResonancePools.Select(x=>x.ActorId==c.Actor?x.Pay(3):x).ToArray();
            s.ConvictionBalance=new ConvictionBalanceRecord(conviction.FundingRestId,conviction.FundingRevision,conviction.Current-2);
            s.CastingStrain=s.CastingStrain.Select(x=>x.ActorId==c.Actor?x.ReduceAtSettledEnd(1):x).ToArray();
            RecordCastingActivity(s,c,CastingActivityKind.MagicalClassAbility);
            foreach(string id in c.DivineInvocation.TargetIds) {
                var before=s.Lives.Single(x=>x.ActorId==id);long potential=View(s,id).HealingPotential(draw.Value+1L+2);
                var healed=PlaytestLife.Heal(ActorLifeRules.ReadForResolution(s,before),potential);
                TestOnlyClubAttackPolicy.ApplyLife(s,before,healed);
                rows.Add(new InvocationHealingRecord(id,before.Hp,potential,healed.Hp));
            }
            s.RandomState=draw.NextState;
            string target=c.DivineInvocation.CureTargetId;
            var at=target==""?new ConditionStamp(s.RuleClock):RadianceRules.TargetStamp(s,target);
            var use=new DivineInvocationRecord(c.Id,s.Revision+1,turn,s.RuleClock,c.DivineInvocation,pool.Current,
                conviction.Current,strain.Dissonance,draw.Value+1,random,draw.NextState,draw.WordsConsumed,rows,at);
            s.BishopEntry=s.BishopEntry.WithInvocations(s.BishopEntry.Invocations.Append(use));
            if(target!="") {
                var invocation=ConditionCureInvocation.ForDivineInvocation(s,c,use);
                var journal=s.Conditions.Single(x=>x.Target==target);
                var projected=ConditionResolutionScope.Project(journal,true,new EffectClockMarker(s.RuleClock));
                var kind=c.DivineInvocation.CurePreference==RadianceCurePreference.Frightened?ConditionKind.Frightened:ConditionKind.Poisoned;
                if(projected.Applications.Any(x=>x.Present(projected.Now)&&x.Application.Kind==kind&&x.Application.GenericCureAllowed)) {
                    if(!journal.Now.Equals(at))TestOnlyClubAttackPolicy.AppendCondition(s,target,ConditionOperation.Advance(c.Id+".invocation.sync",at));
                    var result=SourceQualifiedConditionCure.Settle(ConditionResolutionScope.Read(s.Conditions.Single(x=>x.Target==target)),invocation,target,kind);
                    TestOnlyClubAttackPolicy.CommitCondition(s,result.Transition);
                    var finished=use.WithCure(invocation.Id+".cure",result.EndedApplications);
                    s.BishopEntry=s.BishopEntry.WithInvocations(s.BishopEntry.Invocations.Select(x=>x==use?finished:x));
                }
            }
            var epoch=s.OrdinaryMagic==null ? WorldTiming.ForActor(s,c.Actor) : WorldTiming.FindEpoch(s,turn.EpochId);
            s.AbilityRecharges=s.AbilityRecharges.Where(x=>x.ActorId!=c.Actor||x.AbilityId!=BishopProfile.Invocation)
                .Append(new CharacterAbilityRechargeRecord(c.Actor,BishopProfile.Invocation,epoch.Id,turn.LocalStart,epoch.Start(turn.LocalStart),3)).ToArray();
            ReconcileDyingCadences(s);PauseIncompatibleWork(s);
            return null;
        }
        private IEnumerable<Command> DiscoverDivineInvocation(Snapshot s,string actor)
        {
            if(s.BishopEntry==null||actor!=ClericRpProfile.Actor||!BishopProfile.Earned(s))yield break;
            var allies=s.Actors.Where(x=>SoldierTacticalFeatures.IsAlly(s,actor,x.Id)&&!s.Lives.Single(l=>l.ActorId==x.Id).Dead)
                .OrderBy(x=>x.Id,StringComparer.Ordinal).Select(x=>x.Id).ToArray();
            // Discovery presents singleton and the admitted party set; commands may select any legal one-to-three subset.
            var choices=allies.Select(x=>new[]{x}).Concat(allies.Length>1&&allies.Length<=3?new[]{allies}:Array.Empty<string[]>());
            int index=0;
            foreach(var selected in choices) {
                var command=new Command("option."+s.Revision+".invocation."+(index++),actor,s.Revision,CommandKind.UseDivineInvocation,
                    divineInvocation:new DivineInvocationRequest(selected));
                if(AssessDivineInvocation(s,command)==null)yield return command;
            }
        }
    }
}
#endif
