#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static object ClericStoredFields(object value,int depth=0)
        {
            if(value==null)return null;
            Require(depth<80,"Detached field capture encountered a cycle.");
            var type=value.GetType();if(type.IsPrimitive||type.IsEnum||value is string||value is decimal)return value;
            if(value is System.Collections.IEnumerable sequence)return sequence.Cast<object>().Select(x=>ClericStoredFields(x,depth+1)).ToArray();
            var fields=new SortedDictionary<string,object>(StringComparer.Ordinal){{"$type",type.FullName}};
            foreach(var field in type.GetFields(BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic))
                fields.Add(field.Name,ClericStoredFields(field.GetValue(value),depth+1));
            return fields;
        }
        private static string ClericRaw(Snapshot s)=>System.Text.Json.JsonSerializer.Serialize(ClericStoredFields(s));

        private static Snapshot DetachedRadianceConditions(Snapshot ready,RadianceCurePreference preference,bool independent=true,ConditionStamp? expiry=null)
        {
            // Deliberately unearned condition applications. These are mechanical producer controls,
            // never supported saves or a claim that the condition survived a genuine earned campaign.
            var s=ready.Copy();const string target=ConnectedExpeditionSession.Hero;
            var at=new ConditionStamp(s.RuleClock);var history=ConditionHistory.Restore(s.Conditions.Single(x=>x.Target==target));
            if(!history.Journal.Now.Equals(at))history=history.Append(ConditionOperation.Advance("detached.sync",at)).State;
            string kind=preference.ToString();
            foreach(string id in new[]{"eligible","suppressed","protected"}) {
                var fear=preference==RadianceCurePreference.Frightened
                    ?new FrightenedRelationshipData(FrightenedProfile.Actor,"TEST_ONLY.detached-fear-"+id,FrightenedProfile.SourceRevision):null;
                history=history.Append(ConditionOperation.Apply("detached.apply."+id,at,new ConditionApplicationData("detached."+id,
                    "TEST_ONLY.detached-owner","TEST_ONLY.detached-cure-control",kind,expiry??new ConditionStamp(s.RuleClock.AddSeconds(60)),
                    "expiry",id!="protected",fear:fear))).State;
            }
            history=history.Append(ConditionOperation.Suppress("detached.suppress",at,"detached.suppressed",true)).State;
            if(independent) {
                string other=preference==RadianceCurePreference.Frightened?"Poisoned":"Frightened";
                var fear=other=="Frightened"?new FrightenedRelationshipData(FrightenedProfile.Actor,"TEST_ONLY.detached-other-use",FrightenedProfile.SourceRevision):null;
                history=history.Append(ConditionOperation.Apply("detached.other",at,new ConditionApplicationData("detached.other",
                    "TEST_ONLY.detached-owner","TEST_ONLY.detached-other",other,null,"source-end",true,fear:fear))).State;
                history=history.Append(ConditionOperation.Apply("detached.independent",at,new ConditionApplicationData("detached.independent",
                    "TEST_ONLY.detached-owner","TEST_ONLY.detached-other","Blinded",null,"source-end",true))).State;
            }
            s.Conditions=s.Conditions.Select(x=>x.Target==target?history.Journal:x).ToArray();return s;
        }

        private static void AddClericRadianceCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("chr03_detached_real_rite_named_cures_and_atomic_preflight",()=>{
                var session=EarnClericObjective(false,directory);AwardAndAdvanceCleric(session,directory);ReachClericOwnSlot(session);
                var ready=ShortRestCapture(session);var policy=ClericPolicy(session);var rows=new List<object>();
                const string target=ConnectedExpeditionSession.Hero,actor=ClericRpProfile.Actor;
                Command Use(Snapshot s,RadianceCurePreference preference)=>new Command("detached.radiance",actor,s.Revision,
                    CommandKind.UseHealingRite,target,healingRite:new HealingRiteRequest(preference));
                foreach(var preference in new[]{RadianceCurePreference.Frightened,RadianceCurePreference.Poisoned}) {
                    var epoch=WorldTiming.ForActor(ready,target);
                    long localEnd=FrightenedProfile.NextTargetEnd(epoch,target,ready.RuleClock);
                    var repeatAt=new ConditionStamp(epoch.Start(localEnd+1));var finalAt=new ConditionStamp(repeatAt.Time.AddSeconds(6));
                    var candidate=DetachedRadianceConditions(ready,preference,expiry:preference==RadianceCurePreference.Frightened?finalAt:(ConditionStamp?)null);
                    FrightenedTimingRecord timing=null;
                    if(preference==RadianceCurePreference.Frightened) {
                        // Synthetic application/producer setup, using the actual source's calendar formula.
                        // This is not inserted into a supported campaign or accepted by strict replay.
                        string useId="TEST_ONLY.detached-fear-eligible";
                        candidate.FrightenedUses=candidate.FrightenedUses.Append(new FrightenedUseRecord(useId,"TEST_ONLY.detached-source",
                            candidate.Revision+1,FrightenedProfile.Actor,FrightenedProfile.SourceId,FrightenedProfile.SourceRevision,
                            epoch.Id,epoch.LatestStart(FrightenedProfile.Actor,epoch.ProcessedSlot),candidate.RuleClock,10,new[]{target})).ToArray();
                        timing=new FrightenedTimingRecord("detached.eligible",useId,target,epoch.Id,localEnd,repeatAt,finalAt);
                        candidate.FrightenedTimings=candidate.FrightenedTimings.Append(timing).ToArray();
                    }
                    string original=ClericRaw(candidate);
                    // The normal paid Rite resolver invokes ForRadiance internally. No generic cure
                    // helper or ForDetachedTest invocation is used to create this result.
                    var staged=candidate.Copy();var command=Use(staged,preference);
                    Require(policy.Resolve(staged,command)==null,"Actual paid Rite producer denied the disclosed cure control.");
                    var use=staged.RadianceUses.Single();var rite=staged.HealingRites.Single();
                    var history=ConditionHistory.Restore(staged.Conditions.Single(x=>x.Target==target));
                    Require(use.EndedApplicationIds.SequenceEqual(new[]{"detached.eligible","detached.suppressed"})
                        && use.CureOperationId==command.Id+".radiance.cure" && use.AdditionalGain==1 && rite.ActualGain>0
                        && staged.ResonancePools.Single().Current==1 && staged.WorldIntervals.Single(x=>x.ActorId==actor).ActionSpent
                        && history.Ledger.Applications.Single(x=>x.Id=="detached.protected").Present(history.Ledger.Now)
                        && history.Ledger.Applications.Single(x=>x.Id=="detached.other").Present(history.Ledger.Now)
                        && history.Ledger.Applications.Single(x=>x.Id=="detached.independent").Present(history.Ledger.Now)
                        && candidate.Lives.Single(x=>x.ActorId==target).Prone==staged.Lives.Single(x=>x.ActorId==target).Prone
                        && candidate.RuleClock==staged.RuleClock && original==ClericRaw(candidate),
                        "Paid Radiance did not atomically preserve protected/independent effects and immutable input.");
                    var restored=ConditionHistory.Restore(new ConditionJournalCodec().Decode(new ConditionJournalCodec().Encode(history.Journal)));
                    Require(restored.Journal.SameAs(history.Journal),"Cure journal changed on component replay.");
                    if(timing!=null) {
                        var process=typeof(TestOnlySharedWorldPolicy).GetMethod("ProcessFrightenedRepeatMarkers",BindingFlags.Static|BindingFlags.NonPublic);
                        var control=candidate.Copy();control.RuleClock=repeatAt.Time;uint random=control.RandomState;int saves=control.FrightenedSaves.Length;
                        process.Invoke(null,new object[]{control});
                        Require(control.RandomState!=random && control.FrightenedSaves.Length==saves+1,"Uncured control did not reach the actual repeat-save processor.");
                        var ended=staged.Copy();ended.RuleClock=repeatAt.Time;random=ended.RandomState;saves=ended.FrightenedSaves.Length;
                        process.Invoke(null,new object[]{ended});
                        Require(ended.RandomState==random && ended.FrightenedSaves.Length==saves
                            && ClericSettlementProfile.CuredBeforeRepeat(ended,timing),"Cured fear rolled again or lost its causal early-ending exception.");
                        var due=candidate.Copy();due.RuleClock=repeatAt.Time;
                        long slot=epoch.SlotAt(due.RuleClock);
                        while(epoch.Order[(int)(slot%epoch.Order.Count)]!=actor)slot++;
                        due.RuleClock=epoch.Start(slot);due.Reinforcement=due.Reinforcement.At(slot);
                        due.WorldIntervals=due.WorldIntervals.Select(x=>x.ActorId==actor
                            ?new WorldIntervalRecord(actor,due.Reinforcement.Admission.Phase.GlobalTurn(slot)):x).ToArray();
                        string dueBefore=ClericRaw(due);
                        string dueCode=policy.Resolve(due,Use(due,preference));
                        Require(dueCode=="ConditionBoundaryPending" && dueBefore==ClericRaw(due),
                            "Due-before-input preflight returned "+dueCode+" or changed state.");
                    }
                    // Synthetic source applications cannot be smuggled into connected persistence.
                    staged.Revision=command.ExpectedRevision+1;
                    var receipt=new CommandReceipt {Id=command.Id,Principal="TEST_ONLY.host",Revision=staged.Revision,
                        Fingerprint=((int)command.Kind).ToString(System.Globalization.CultureInfo.InvariantCulture)+"|"+actor+"|"+target+"|"
                            +command.ExpectedRevision.ToString(System.Globalization.CultureInfo.InvariantCulture)+"|0|0|healing-rite-v1|"
                            +((int)preference).ToString(System.Globalization.CultureInfo.InvariantCulture)};
                    Require(command.MatchesReceipt(receipt),"Detached producer control did not retain its actual command identity.");
                    staged.Receipts=staged.Receipts.Append(receipt).ToArray();
                    Require(policy.ValidateState(staged)!=null,"Detached condition setup became supported connected history.");
                    rows.Add(new{kind=preference.ToString(),scope="DETACHED real paid Rite and internal Radiance factory",rite,use,
                        protectedPresent=true,independentPresent=true,strictConnectedRestoreAdmitted=false});
                }
                void Reject(Snapshot s,string expected) {
                    string before=ClericRaw(s);var command=Use(s,RadianceCurePreference.Poisoned);
                    Require(policy.Resolve(s,command)==expected && before==ClericRaw(s),"Preflight changed detached state: "+expected);
                }
                var denied=ready.Copy();denied.ResonancePools=new[]{denied.ResonancePools.Single().Pay(2)};Reject(denied,"InsufficientResonance");
                denied=ready.Copy();denied.WorldIntervals=denied.WorldIntervals.Select(x=>x.ActorId==actor?x.PayAction():x).ToArray();Reject(denied,"ActionAlreadySpent");
                denied=ready.Copy();denied.CharacterFeatureGrants=denied.CharacterFeatureGrants.Where(x=>x.FeatureId!=ClericSettlementProfile.Radiance).ToArray();
                Reject(denied,"HealingRiteContextUnsupported");
                denied=ready.Copy();var local=WorldTiming.ForActor(denied,actor).ProcessedSlot;
                denied.WorldIntervals=denied.WorldIntervals.Select(x=>x.ActorId==actor?new WorldIntervalRecord(actor,local):x).ToArray();
                Reject(denied,"WrongRegularTurn");
                denied=ready.Copy();denied.Reinforcement=denied.Reinforcement.At(local-1);Reject(denied,"WrongRegularTurn");
                denied=ready.Copy();var full=denied.Conditions.Single(x=>x.Target==target);
                for(int i=full.Operations.Count;i<ConditionJournal.MaxOperations;i++)full=full.Append(ConditionOperation.Advance("capacity."+i,full.Now));
                denied.Conditions=denied.Conditions.Select(x=>x.Target==target?full:x).ToArray();Reject(denied,"ConditionHistoryCapacityReached");
                File.WriteAllText(Path.Combine(directory,"detached-paid-cure-controls.json"),System.Text.Json.JsonSerializer.Serialize(rows,
                    new System.Text.Json.JsonSerializerOptions{WriteIndented=true}));
            });
            cases.Add("chr03_detached_real_rite_caps_full_health_and_empty_cure",()=>{
                var session=EarnClericObjective(false,directory);AwardAndAdvanceCleric(session,directory);ReachClericOwnSlot(session);
                var ready=ShortRestCapture(session);var policy=ClericPolicy(session);
                const string target=ConnectedExpeditionSession.Hero;
                void Hp(Snapshot s,long hp) {s.Lives=s.Lives.Select(x=>x.ActorId!=target?x:new ActorLifeRecord(x.ActorId,x.MaximumHp,hp,
                    x.TemporaryHp,x.LinkedInjuries,x.Stable,x.Dead,x.UsesDeathSaves,x.DeathSuccesses,x.DeathFailures,x.StableUntil,
                    x.LastDeathTurn,x.Prone,x.HeldItems)).ToArray();}
                Command Use(Snapshot s)=>new Command("detached.cap",ClericRpProfile.Actor,s.Revision,CommandKind.UseHealingRite,target,
                    healingRite:new HealingRiteRequest(RadianceCurePreference.Poisoned));
                var capped=DetachedRadianceConditions(ready,RadianceCurePreference.Poisoned);Hp(capped,25);
                Require(policy.Resolve(capped,Use(capped))==null && capped.HealingRites.Single().ActualGain==1
                    && capped.RadianceUses.Single().AdditionalGain==0 && capped.RadianceUses.Single().EndedApplicationIds.Count==2,
                    "Positive base healing must still qualify a named cure when the extra HP caps to zero.");
                var full=DetachedRadianceConditions(ready,RadianceCurePreference.Poisoned);Hp(full,26);
                var before=full.Conditions.Single(x=>x.Target==target);
                Require(policy.Resolve(full,Use(full))==null && full.HealingRites.Single().ActualGain==0 && full.RadianceUses.Length==0
                    && full.ResonancePools.Single().Current==1 && before.SameAs(full.Conditions.Single(x=>x.Target==target)),
                    "Full-HP paid Rite fabricated a Radiance trigger or cure.");
                var empty=ready.Copy();before=empty.Conditions.Single(x=>x.Target==target);
                Require(policy.Resolve(empty,Use(empty))==null && empty.RadianceUses.Single().EndedApplicationIds.Count==0
                    && empty.RadianceUses.Single().CureOperationId=="" && before.SameAs(empty.Conditions.Single(x=>x.Target==target)),
                    "No eligible condition must create no cure or synchronization mutation.");
                var corrupted=DetachedRadianceConditions(ready,RadianceCurePreference.Poisoned);
                var corruptedHistory=ConditionHistory.Restore(corrupted.Conditions.Single(x=>x.Target==target));
                corruptedHistory=corruptedHistory.Append(ConditionOperation.Apply("detached.corruption",corruptedHistory.Journal.Now,
                    new ConditionApplicationData("detached.corruption","TEST_ONLY.owner","TEST_ONLY.corruption","Corrupted",null,"source-end",true))).State;
                corrupted.Conditions=corrupted.Conditions.Select(x=>x.Target==target?corruptedHistory.Journal:x).ToArray();
                Require(policy.Resolve(corrupted,Use(corrupted))==null && corrupted.HealingRites.Single().ActualGain>0
                    && corrupted.RadianceUses.Single().AdditionalPotential==0 && corrupted.RadianceUses.Single().AdditionalGain==0
                    && corrupted.RadianceUses.Single().EndedApplicationIds.Count==2,"Corrupted extra-healing reduction improperly prevented the qualified cure.");
                foreach(var preference in new[]{RadianceCurePreference.Frightened,RadianceCurePreference.Poisoned}) {
                    var expired=ready.Copy();var at=new ConditionStamp(ready.RuleClock);
                    var origin=new EffectClockMarker(new RuleTime(checked(ready.RuleClock.Numerator-6*ready.RuleClock.Denominator),ready.RuleClock.Denominator));
                    var history=new ConditionHistory(target,origin,relationships:true);
                    var fear=preference==RadianceCurePreference.Frightened
                        ?new FrightenedRelationshipData(FrightenedProfile.Actor,"TEST_ONLY.expired-use",FrightenedProfile.SourceRevision):null;
                    history=history.Append(ConditionOperation.Apply("expired",history.Journal.Now,new ConditionApplicationData("expired",
                        "TEST_ONLY.owner","TEST_ONLY.expired-control",preference.ToString(),at,"expiry",true,fear:fear))).State;
                    history=history.Append(ConditionOperation.Advance("expired.boundary",at)).State;
                    expired.Conditions=expired.Conditions.Select(x=>x.Target==target?history.Journal:x).ToArray();
                    var expiredCommand=new Command("detached.expired",ClericRpProfile.Actor,expired.Revision,CommandKind.UseHealingRite,target,
                        healingRite:new HealingRiteRequest(preference));
                    Require(policy.Resolve(expired,expiredCommand)==null && expired.RadianceUses.Single().EndedApplicationIds.Count==0
                        && expired.RadianceUses.Single().CureOperationId=="" && history.Journal.SameAs(expired.Conditions.Single(x=>x.Target==target)),
                        "Already expired effects were misreported as Radiance cures.");
                }
                var spent=empty.Copy();spent.ResonancePools=new[]{ready.ResonancePools.Single()};
                spent.WorldIntervals=ready.WorldIntervals.ToArray();string original=ClericRaw(spent);
                Require(policy.Resolve(spent,new Command("detached.second-use",ClericRpProfile.Actor,spent.Revision,CommandKind.UseHealingRite,target,
                    healingRite:new HealingRiteRequest(RadianceCurePreference.Poisoned)))=="RadianceAlreadyUsedThisTurn" && original==ClericRaw(spent),
                    "Reset detached Action/RP facts bypassed the retained once-per-turn Radiance history.");
            });
        }
    }
}
#endif
