#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private FerryWraithRecord ferryDeclaration;
        internal static string CreatureAttackFailure(Snapshot s,string actor,string feature)
        {
            if(s.FerryWraith==null||actor!=FerryWraithProfile.Actor||feature!=FerryWraithProfile.Feature
                ||!s.Creatures.Any(x=>x.ActorId==actor))return "CreatureAttackSourceUnavailable";
            if(s.FerryWraith.Admission==null)return "FerryWraithHoldsAuthoredPosition";
            if(s.FerryWraith.ClawSuppressed)return "CreatureAttackSourceSuppressed";
            return null;
        }
        internal static bool HasOrdinaryMeleeSource(Snapshot s,string actor)
            =>s.Creatures.Any(x=>x.ActorId==actor)
                ?CreatureAttackFailure(s,actor,FerryWraithProfile.Feature)==null:s.Characters.Any(x=>x.ActorId==actor);
        internal TestOnlySharedWorldPolicy EnableFerryWraith(bool companionConsents=true,bool directorAuthorizes=true)
        {
            if(initializationStarted||ferryDeclaration!=null||declaredGeometry==null||bishopDeclaration==null||observationFixture==null)
                throw new InvalidOperationException("Select the Ferry source once on a fresh qualified-geometry expedition.");
            ferryDeclaration=new FerryWraithRecord(ContentFingerprint,companionConsents,directorAuthorizes);
            bodies.RegisterDeferredConditionTarget(FerryWraithProfile.Actor);
            observationFixture=new ObservationFixture(observationFixture.Width,observationFixture.Height,observationFixture.Cells,
                observationFixture.Profiles.Append(new ObservationSightProfile(FerryWraithProfile.Actor,30,30)));
            ContentFingerprint=FerryWraithProfile.BindFingerprint(ferryDeclaration.PredecessorFingerprint,companionConsents,directorAuthorizes);
            return this;
        }
        private void InitializeFerryActor(Snapshot s)
        {
            if(ferryDeclaration==null)return;
            const string actor=FerryWraithProfile.Actor;
            s.FerryWraith=ferryDeclaration;
            s.Creatures=s.Creatures.Append(FerryWraithProfile.CreateCreature()).ToArray();
            s.Actors=s.Actors.Append(new ActorState{Id=actor,X=10,Y=2}).ToArray();
            s.Lives=s.Lives.Append(ActorLifeRules.Record(actor,new LifeState(9,9,usesDeathSaves:false),false)).ToArray();
            s.ActorMovement=s.ActorMovement.Append(new ActorMovementRecord(actor,40)).ToArray();
            s.TacticalActors=s.TacticalActors.Append(new ActorTacticalRecord(actor)).ToArray();
            s.Conditions=s.Conditions.Append(new ConditionJournal(ConditionHistory.PolicyId,actor,new ConditionStamp(s.RuleClock))).ToArray();
        }
        private void InitializeFerrySource(Snapshot s)
        {
            if(ferryDeclaration==null)return;
            var before=s.Conditions.Single(x=>x.Target==FerryWraithProfile.Actor);
            var immunity=new ConditionImmunityData(FerryWraithProfile.PoisonedImmunity,FerryWraithProfile.Actor,FerryWraithProfile.SourceId,
                new[]{"Poisoned"},null,"source-profile-only");
            var after=ConditionHistory.Restore(before).Append(ConditionOperation.Grant(FerryWraithProfile.PoisonedImmunityGrant,
                new ConditionStamp(s.RuleClock),immunity)).State.Journal;
            s.Conditions=s.Conditions.Select(x=>x.Target==after.Target?after:x).ToArray();
        }
        private static string AssessFerryWorldStep(Snapshot s,WorldTraversalRecord edge)
            =>s.FerryWraith!=null&&s.FerryWraith.Admission==null&&edge.ActorId==FerryWraithProfile.Actor
                ?"FerryWraithHoldsAuthoredPosition":null;
    }
}
#endif
