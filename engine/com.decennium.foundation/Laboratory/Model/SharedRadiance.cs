#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    internal static class RadianceRules
    {
        internal static bool Owns(Snapshot s, string actor)
            => s.ConnectedClericSettlement && actor == ClericRpProfile.Actor && s.ClericInvocationPath?.PathId == ClericSettlementProfile.Radiance
                && s.ClericInvocationPath.AcquiredRevision <= s.Revision
                && s.CharacterFeatureGrants.Count(x => x.ActorId == actor
                    && (x.FeatureId == ClericSettlementProfile.Radiance || x.FeatureId == ClericSettlementProfile.Attunement)
                    && x.Origin == CharacterFeatureGrantOrigin.EarnedAutomaticClassFeature && ClericSettlementProfile.ValidEarnedGrant(s,x)) == 2;

        internal static string OwnTurnFailure(Snapshot s, string actor)
        {
            if(s.OrdinaryMagic!=null) {
                if(!Owns(s,actor))return "RadianceNotOwned";
                string context=OrdinaryMagicProfile.ContextFailure(s,actor); if(context!=null)return context;
            } else {
                if (!Owns(s,actor) || s.ClericObjective == null || s.ClericInvocationPath.AcquiredRevision <= s.ClericObjective.Revision
                    || !PostRecoveryProfile.Active(s) && !FerryWraithProfile.Active(s) && (s.InventoryCombat || s.Encounter != null)
                    || !s.ClosedEncounters.Any(x => x.Encounter.Id == s.ClericMilestone.LaterEncounterId))
                    return "HealingRiteContextUnsupported";
                var epoch = WorldTiming.ForActor(s,actor); var phase = s.Reinforcement?.Admission?.Phase;
                if (epoch == null || !FerryWraithProfile.IsEpoch(s,epoch.Id) && !PostRecoveryProfile.IsEpoch(s,epoch.Id) && epoch.Id != phase?.Epoch.Id) return "HealingRiteCalendarUnavailable";
                long slot = epoch.SlotAt(s.RuleClock);
                if (slot != epoch.ProcessedSlot || slot < 0 || epoch.Order[(int)(slot % epoch.Order.Count)] != actor
                    || epoch.LatestStart(actor,slot) != slot
                    || s.WorldIntervals.Single(x => x.ActorId == actor).LastStart != WorldTiming.TurnOrdinal(s,epoch.Id,slot)
                    || s.InventoryCombat && (s.Encounter.CurrentActor != actor || s.InventoryTurnActor != actor)) return "WrongRegularTurn";
            }
            if (TestOnlyClubAttackPolicy.HasUnprocessedConditionDeadline(s)
                || s.FrightenedTimings.Any(x => x.RepeatAt.Time <= s.RuleClock
                    && !s.FrightenedSaves.Any(save => save.Repeat && save.ApplicationId == x.ApplicationId)
                    && !ClericSettlementProfile.CuredBeforeRepeat(s,x))) return "ConditionBoundaryPending";
            return null;
        }

        internal static ConditionStamp TargetStamp(Snapshot s, string target)
        {
            var current=s.Conditions.Single(x=>x.Target==target).Now;
            return current.Time==s.RuleClock ? current : new ConditionStamp(s.RuleClock);
        }

        internal static bool Used(Snapshot s, string actor)
        {
            if(s.OrdinaryMagic!=null) {
                var origin=s.OrdinaryMagic.Current?.Origin;
                return origin!=null && s.RadianceUses.Any(x=>x.ActorId==actor && x.EpochId==origin.EpochId && x.LocalStart==origin.LocalStart);
            }
            var epoch = WorldTiming.ForActor(s,actor);
            return epoch != null && s.RadianceUses.Any(x => x.ActorId == actor && x.EpochId == epoch.Id
                && x.LocalStart == epoch.LatestStart(actor,epoch.ProcessedSlot));
        }

        internal static void ValidateCureTrigger(Snapshot s, Command c, HealingRiteRecord rite)
        {
            if (c.Kind != CommandKind.UseHealingRite || c.HealingRite == null || c.HealingRite.CurePreference == RadianceCurePreference.None
                || OwnTurnFailure(s,c.Actor) != null || Used(s,c.Actor) || rite == null || !s.HealingRites.Contains(rite)
                || rite.CommandId != c.Id || rite.Revision != s.Revision + 1 || c.ExpectedRevision != s.Revision
                || rite.ActorId != c.Actor || rite.TargetId != c.Target || rite.SourceId != ClericRpProfile.HealingRite
                || rite.SourceRevision != ClericRpProfile.SourceRevision || rite.At != s.RuleClock || rite.ActualGain <= 0
                || rite.RpPaid != 2 || rite.Modifier != 2 || s.RandomState != rite.RandomAfter
                || s.ResonancePools.Single(x => x.ActorId == c.Actor).Current != rite.RpAfter
                || !s.WorldIntervals.Single(x => x.ActorId == c.Actor).ActionSpent
                || s.Lives.Single(x => x.ActorId == c.Target).Dead || s.Lives.Single(x => x.ActorId == c.Target).Hp != ConsecrationProfile.AfterGround(s,rite))
                throw new ArgumentException("Radiance requires its actual staged paid healing trigger.");
            var draw = DiceStream.Draw(rite.RandomBefore,8);
            if (draw.Value + 1 != rite.Die || draw.NextState != rite.RandomAfter || draw.WordsConsumed != rite.WordsConsumed)
                throw new ArgumentException("Radiance Rite draw does not match its payment record.");
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static string RadiancePreflight(Snapshot state, Command command)
        {
            var preference = command.HealingRite?.CurePreference ?? RadianceCurePreference.None;
            bool owns = RadianceRules.Owns(state,command.Actor);
            if (preference != RadianceCurePreference.None && !owns) return "RadianceNotOwned";
            if (!owns) return null;
            string context = RadianceRules.OwnTurnFailure(state,command.Actor); if (context != null) return context;
            if (RadianceRules.Used(state,command.Actor)) return "RadianceAlreadyUsedThisTurn";
            if (state.RadianceUses.Length >= 128) return "RadianceHistoryFull";
            if (preference != RadianceCurePreference.None) {
                if (!Validation.ValidId(command.Id + ".radiance.cure") || !Validation.ValidId(command.Id + ".radiance.sync"))
                    return "RadianceIdentityCapacityReached";
                var journal = state.Conditions.Single(x => x.Target == command.Target);
                if (journal.Now.Time > state.RuleClock) return "ConditionCalendarMismatch";
                int worstCase = journal.Now.Equals(RadianceRules.TargetStamp(state,command.Target)) ? 1 : 2;
                if (journal.Operations.Count + worstCase > ConditionJournal.MaxOperations) return "ConditionHistoryCapacityReached";
            }
            return null;
        }

        private static void SettleRadiance(Snapshot state, Command command, HealingRiteRecord rite)
        {
            if (!RadianceRules.Owns(state,command.Actor) || rite.ActualGain <= 0 || RadianceRules.Used(state,command.Actor)) return;
            var preference = command.HealingRite?.CurePreference ?? RadianceCurePreference.None;
            var at = RadianceRules.TargetStamp(state,command.Target);
            ConditionCureInvocation invocation = preference == RadianceCurePreference.None ? null : ConditionCureInvocation.ForRadiance(state,command,rite);
            var before = state.Lives.Single(x => x.ActorId == command.Target);
            long potential = View(state,command.Target).HealingPotential(1);
            var healed = PlaytestLife.Heal(ActorLifeRules.ReadForResolution(state,before),potential);
            TestOnlyClubAttackPolicy.ApplyLife(state,before,healed);
            string[] ended = Array.Empty<string>(); string operation = "";
            if (invocation != null) {
                var journal = state.Conditions.Single(x => x.Target == command.Target);
                var projected = ConditionResolutionScope.Project(journal,true,new EffectClockMarker(state.RuleClock));
                var kind = preference == RadianceCurePreference.Frightened ? ConditionKind.Frightened : ConditionKind.Poisoned;
                if (projected.Applications.Any(x => x.Present(projected.Now) && x.Application.Kind == kind && x.Application.GenericCureAllowed)) {
                    if (!journal.Now.Equals(at)) TestOnlyClubAttackPolicy.AppendCondition(state,command.Target,
                        ConditionOperation.Advance(command.Id + ".radiance.sync",at));
                    var history = ConditionResolutionScope.Read(state.Conditions.Single(x => x.Target == command.Target));
                    var result = SourceQualifiedConditionCure.Settle(history,invocation,command.Target,kind);
                    TestOnlyClubAttackPolicy.CommitCondition(state,result.Transition);
                    ended = result.EndedApplications.ToArray(); operation = invocation.Id + ".cure";
                }
            }
            var origin=state.OrdinaryMagic?.Current?.Origin;
            var epoch = origin==null ? WorldTiming.ForActor(state,command.Actor) : WorldTiming.FindEpoch(state,origin.EpochId);
            var phase = state.Reinforcement.Admission.Phase;
            long local = origin?.LocalStart ?? epoch.LatestStart(command.Actor,epoch.ProcessedSlot);
            state.RadianceUses = state.RadianceUses.Append(new RadianceUseRecord(command.Id,state.Revision + 1,command.Actor,command.Target,
                ClericRpProfile.SourceRevision,epoch.Id,local,epoch.Id==phase.Epoch.Id?phase.FirstTurn:0,
                WorldTiming.TurnOrdinal(state,epoch.Id,local),at,rite.HpAfter,potential,healed.Hp,
                preference,operation,ended,before.Hp)).ToArray();
        }
    }
}
#endif
