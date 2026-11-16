#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ConnectedExpeditionSession NewClericLongRestExpedition()
            => ConnectedExpeditionSession.StartWithClericLongRest(ClericInitialSelection.AuthoredExample(),
                ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());

        private static void LongRestAdvanceTo(ConnectedExpeditionSession session, long seconds)
        {
            var at=ShortRestCapture(session).RuleClock;
            var wait=new RuleTime(checked(seconds*at.Denominator-at.Numerator),at.Denominator);
            if(wait>default(RuleTime)) ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,
                x:checked((int)wait.Numerator),y:checked((int)wait.Denominator));
        }

        private static void LongRestGuidance(ConnectedExpeditionSession session,string id)
        {
            ReachClericOwnSlot(session);
            CommitVialRoute(session,new Command(id,ClericRpProfile.Actor,ShortRestCapture(session).Revision,
                CommandKind.CastKnownSpell,ClericRpProfile.Actor,spellCast:new SpellCastRequest("guidance",willingTarget:true)));
        }

        private static void RetainDetachedLongRestInterruptions(ConnectedExpeditionSession session,Snapshot active,string directory)
        {
            var flags=System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Static;
            var settle=typeof(TestOnlySharedWorldPolicy).GetMethod("SettleSpellDamage",flags);
            var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",flags);
            var reconcile=typeof(TestOnlySharedWorldPolicy).GetMethod("ReconcileClericLongRestAccess",
                System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance);
            var codec=new SnapshotCodec();const string actor=ClericRpProfile.Actor;
            var zero=active.Copy();var zeroBytes=codec.Encode(zero);
            settle.Invoke(null,new object[]{zero,actor,FrightenedProfile.Actor,"detached.long-rest.zero",0L,true});
            Require(zeroBytes.SequenceEqual(codec.Encode(zero)),"Fully prevented zero damage interrupted actual rest.");
            var damage=active.Copy();var before=damage.Lives.Single(x=>x.ActorId==actor);
            apply.Invoke(null,new object[]{damage,before,new LifeState(before.MaximumHp,before.Hp,temporaryHp:4)});
            before=damage.Lives.Single(x=>x.ActorId==actor);
            var packet=PlaytestDamageDice.Resolve(ActorLifeRules.ReadForResolution(damage,before),2,damage.RuleClock,damage.RandomState);
            damage.RandomState=packet.NextRandomState;apply.Invoke(null,new object[]{damage,before,packet.Outcome.State});
            settle.Invoke(null,new object[]{damage,actor,FrightenedProfile.Actor,"detached.long-rest.temp-damage",2L,true});
            Require(damage.ClericLongRests.Last().Interruption==ClericLongRestInterruption.Damage
                &&damage.Lives.Single(x=>x.ActorId==actor).Hp==before.Hp&&damage.Lives.Single(x=>x.ActorId==actor).TemporaryHp==2
                &&damage.ClericLongRestSettlements.Length==0&&damage.ConvictionBalance==null,
                "Positive damage absorbed by temporary HP must interrupt the actual shared rest path without recovery.");
            var controls=new List<object>();
            foreach(string kind in new[]{"access","encounter","body"}) {
                var candidate=active.Copy();
                if(kind=="access")candidate.Actors.Single(x=>x.Id==actor).X++;
                if(kind=="encounter")candidate.InventoryCombat=true;
                if(kind=="body") {
                    var body=candidate.Lives.Single(x=>x.ActorId==actor);
                    apply.Invoke(null,new object[]{candidate,body,new LifeState(body.MaximumHp,0)});
                }
                var cause=new Command("detached.long-rest."+kind,ConnectedExpeditionSession.Hero,candidate.Revision,CommandKind.AdvanceClock,"",1,1);
                reconcile.Invoke(ClericPolicy(session),new object[]{candidate,cause});
                var rest=candidate.ClericLongRests.Last();
                var expected=kind=="access"?ClericLongRestInterruption.AccessLost:kind=="encounter"?ClericLongRestInterruption.Encounter:ClericLongRestInterruption.BodyIneligible;
                Require(rest.Outcome==ClericLongRestOutcome.Interrupted&&rest.Interruption==expected
                    &&candidate.RestIntervals.Last().Status==RestIntervalStatus.Interrupted&&candidate.ClericLongRestSettlements.Length==0,
                    "Detached external invalidation did not use the actual shared interruption path.");
                controls.Add(new {kind,expected,rest.EndedAt,rest.EndCommandId});
            }
            File.WriteAllText(Path.Combine(directory,"long-rest-detached-interruptions.json"),System.Text.Json.JsonSerializer.Serialize(new {
                scope="Detached external event setup on a genuine active rest; actual shared damage and access reconciliation; no connected external attack, encounter entry, or supported mutated save is claimed",
                zeroUnchanged=true,tempHpDamage=damage.ClericLongRests.Last(),controls}));
        }

        private static void RetainDetachedLongRestCompletion(ConnectedExpeditionSession session,Snapshot completed,string label,string directory)
        {
            var finish=typeof(TestOnlySharedWorldPolicy).GetMethod("CompleteClericLongRest",
                System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance);
            var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",
                System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Static);
            var original=completed.ClericLongRestSettlements.Last();var rest=completed.ClericLongRests.Last();
            var command=CommandHistory.Read(completed.Receipts.Single(x=>x.Id==rest.EndCommandId));
            bool eligible=original.Benefit==ClericLongRestBenefit.Eligible;var reports=new List<object>();
            foreach(int wounds in new[]{0,3}) {
                var candidate=completed.Copy();candidate.Revision=original.Revision-1;
                var pending=new ClericLongRestRecord(rest.Sequence,rest.StartCommandId,rest.StartRevision,rest.StartedAt);
                candidate.ClericLongRests=candidate.ClericLongRests.Select(x=>x.Id==rest.Id?pending:x).ToArray();
                candidate.ClericLongRestSettlements=candidate.ClericLongRestSettlements.Where(x=>x.RestId!=rest.Id).ToArray();
                var pool=candidate.ResonancePools.Single();
                candidate.ResonancePools=new[]{new ResonancePoolRecord(pool.ActorId,pool.Maximum,original.RpBefore,pool.InitialFunding)};
                candidate.ConvictionBalance=original.ConvictionBefore.HasValue?new ConvictionBalanceRecord(
                    completed.ConvictionBalance.FundingRestId,completed.ConvictionBalance.FundingRevision,original.ConvictionBefore.Value):null;
                candidate.CastingStrain=new[]{new CastingStrainRecord(ClericRpProfile.Actor,3,original.LastSpellId,original.Refrain,original.LastCastRevision)};
                var before=candidate.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor);
                apply.Invoke(null,new object[]{candidate,before,new LifeState(before.MaximumHp,8,temporaryHp:4,wounds:Wounds(wounds))});
                uint random=candidate.RandomState;
                var failure=(string)finish.Invoke(ClericPolicy(session),new object[]{candidate,pending,command});
                var settled=candidate.ClericLongRestSettlements.Last();var after=candidate.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor);
                Require(failure==null&&settled.TemporaryHpBefore==4&&after.TemporaryHp==0&&after.LinkedInjuries.Count==wounds
                    &&after.Hp==(eligible?(wounds==3?12:13):8)&&settled.DissonanceBefore==3
                    &&settled.DissonanceAfter==(eligible?0:3)&&settled.Refrain==original.Refrain
                    &&settled.HitDiceRecovered==0&&candidate.RandomState==random,
                    "Detached completion must preserve wounds, obey Critical healing, and separate completion endings from beneficial recovery.");
                reports.Add(new{wounds,settled,after.Hp,after.TemporaryHp,randomUnchanged=true});
            }
            Require(ClericLongRestProfile.HitDiceAllowance(0,0)==0&&ClericLongRestProfile.HitDiceAllowance(1,0)==1
                &&ClericLongRestProfile.HitDiceAllowance(2,0)==1&&ClericLongRestProfile.HitDiceAllowance(2,1)==0
                &&ClericLongRestProfile.HitDiceAllowance(1,3)==0&&ClericLongRestProfile.HealingRequest(15,13)==0,
                "Source numeric recovery bounds must use expended dice, Wounds and a positive-only HP gap.");
            File.WriteAllText(Path.Combine(directory,"long-rest-detached-completion-"+label+".json"),System.Text.Json.JsonSerializer.Serialize(new {
                scope="Detached terminal resource/temporary-HP/Wound/Dissonance setup at a genuine completed shared interval; actual class-completion producer; no connected positive Hit Dice recovery or supported altered save is claimed",
                eligible,reports}));
        }

        private static void RetainLongRestForgedRestore(ConnectedExpeditionSession session,Snapshot actual,string directory)
        {
            var codec=new SnapshotCodec();var original=codec.Encode(actual);var x=actual.ClericLongRestSettlements.Single();
            var forged=actual.Copy();
            forged.ClericLongRestSettlements=new[]{new ClericLongRestSettlementRecord(x.RestId,x.CommandId,x.Revision,x.At,
                x.Benefit,x.BeneficialRestId,x.PreviousBeneficialRestId,x.CapacityAcquiredRevision,x.HpBefore-1,x.EffectiveMaximumHp,
                x.HealingRequested+1,x.HealingPotential+1,x.HpAfter,x.TemporaryHpBefore,x.TemporaryHpAfter,x.Wounds,
                x.ExpendedHitDice,x.HitDiceAllowance,x.HitDiceRecovered,x.RpBefore,x.RpMaximum,x.RpAfter,x.ConvictionBefore,
                x.ConvictionAfter,x.DissonanceBefore,x.DissonanceAfter,x.LastSpellId,x.Refrain,x.LastCastRevision)};
            var forgedBytes=codec.Encode(forged);string path=Path.Combine(directory,"long-rest-forged-historical-healing.ddsave");
            File.WriteAllBytes(path,forgedBytes);Throws<ArgumentException>(()=>session.Restore(path));
            Require(original.SequenceEqual(codec.Encode(ShortRestCapture(session)))&&forgedBytes.SequenceEqual(File.ReadAllBytes(path)),
                "Strict restore accepted or repaired a plausible but invented historical HP recovery.");
            File.WriteAllBytes(Path.Combine(directory,"long-rest-forged-restore-before.ddsave"),original);
            File.WriteAllBytes(Path.Combine(directory,"long-rest-forged-restore-after.ddsave"),codec.Encode(ShortRestCapture(session)));
            var unfunded=actual.Copy();unfunded.ConvictionBalance=new ConvictionBalanceRecord(x.RestId,x.Revision,4);
            Throws<ArgumentException>(()=>codec.Encode(unfunded));
            File.WriteAllText(Path.Combine(directory,"long-rest-forged-restore.json"),System.Text.Json.JsonSerializer.Serialize(new {
                scope="Actual strict public restore of a checksummed structurally valid forged history; live state and rejected file unchanged",
                historicalHealingRejected=true,terminalConvictionForgeryStructurallyRejected=true}));
        }

        private static void AddClericLongRestCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("mgt03_long_rest_genesis_and_unearned_denial", () => {
                Throws<ArgumentException>(()=>new RestIntervalRecord("legacy.rest",ClericRpProfile.Actor,"TEST_ONLY.safe-berth",
                    new RuleTime(0),new RuleTime(28800),new RuleTime(28800),RestIntervalStatus.Interrupted,1));
                Throws<ArgumentException>(()=>new RestIntervalRecord(ClericLongRestProfile.IntervalPrefix+"0",ClericRpProfile.Actor,
                    ClericLongRestProfile.SiteId,new RuleTime(0),new RuleTime(28800),new RuleTime(28800),RestIntervalStatus.Interrupted,1));
                var session=NewClericLongRestExpedition(); var before=ShortRestCapture(session); var codec=new SnapshotCodec();
                Require(before.WireSchemaVersion==110 && before.SchemaVersion==90 && before.ConnectedClericLongRest
                    && before.ConvictionBalance==null && !before.ConvictionCapacity.CurrentAvailable
                    && before.ClericLongRests.Length==0 && before.ClericLongRestSettlements.Length==0
                    && before.DailyProvisioningSettlements.Length==0 && before.RestDebtEvents.Length==0,
                    "New profile must begin with actual empty history and unavailable Conviction.");
                var player=session.View(ExpeditionSeat.Player);var opponent=session.View(ExpeditionSeat.FirstOpponent);
                Require(player.LongRest!=null&&player.LongRest.Attempts.Count==0&&opponent.LongRest==null
                    &&player.Actors.Single(x=>x.Position.Id==ClericRpProfile.Actor).ClericSettlement.ConvictionCurrent==null
                    &&!session.DiscoverCastingCommands(ExpeditionSeat.Player,ClericRpProfile.Actor)
                        .Any(x=>x.Command.Kind==CommandKind.BeginLongRest),
                    "Public rest view or command discovery leaked authority or implied unearned recovery.");
                string path=Path.Combine(directory,"long-rest-genesis.ddsave");session.Save(path);session.Restore(path);
                Require(codec.Encode(before).SequenceEqual(codec.Encode(ShortRestCapture(session))),"New genesis failed strict restore.");
                var simulation=CastingSimulation(session);var authority=CastingAuthority();
                RetainClericDenial(simulation,authority,new Command("long-rest.unearned",ClericRpProfile.Actor,0,
                    CommandKind.BeginLongRest,ClericLongRestProfile.SiteId),"LongRestRequiresEarnedCleric2",directory);
                RetainClericDenial(simulation,authority,new Command("long-rest.hero",ConnectedExpeditionSession.Hero,0,
                    CommandKind.BeginLongRest,ClericLongRestProfile.SiteId),"LongRestUnavailable",directory);
            });

            cases.Add("mgt03_long_rest_genuine_first_funding_and_paid_continuation", () => {
                var session=EarnClericObjective(true,directory,NewClericLongRestExpedition());
                AwardAndAdvanceCleric(session,directory);
                var state=ShortRestCapture(session);var actor=state.Actors.Single(x=>x.Id==ClericRpProfile.Actor);
                Require(actor.X==ClericLongRestProfile.X && actor.Y==ClericLongRestProfile.Y,
                    "Genuine route must actually reach its Long Rest berth; observed "+actor.X+","+actor.Y);
                Require(state.ResonancePools.Single().Current==1 && state.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).Hp==8,
                    "Rest witness requires genuine RP spending and missing HP after earned advancement.");
                LongRestGuidance(session,"long-rest.guidance.first");
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                LongRestGuidance(session,"long-rest.guidance.repeat");
                Require(ShortRestCapture(session).CastingStrain.Single().Refrain==1,"Actual repeated cantrip did not establish nonzero Refrain.");
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:60,y:1);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:100,y:1);
                var partial=ShortRestCapture(session);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.InterruptLongRest,ClericLongRestProfile.Active(partial).Id);
                var interrupted=ShortRestCapture(session);
                Require(interrupted.ClericLongRests.Single().Outcome==ClericLongRestOutcome.Interrupted
                    &&interrupted.ClericLongRestSettlements.Length==0&&interrupted.ConvictionBalance==null
                    &&interrupted.ResonancePools.Single().Current==1&&interrupted.RuleClock==partial.RuleClock,
                    "Explicit interruption must retain elapsed time and grant no recovery.");
                session.Save(Path.Combine(directory,"long-rest-interrupted.ddsave"));
                Require(interrupted.RuleClock < new RuleTime(57600),"Genuine preparation exceeded selected first Evening Watch.");
                LongRestAdvanceTo(session,57600);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                var started=ShortRestCapture(session);
                Require(started.ConvictionBalance==null && started.ClericLongRests.Last().Outcome==ClericLongRestOutcome.Active
                    &&started.ClericLongRests.Last().DueAt==new RuleTime(86400),
                    "A rest declaration must not fund Conviction.");
                RetainDetachedLongRestInterruptions(session,started,directory);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:1000,y:1);
                string pending=Path.Combine(directory,"long-rest-pending.ddsave");session.Save(pending);session.Restore(pending);
                var active=ShortRestCapture(session);
                RetainClericDenial(CastingSimulation(session),CastingAuthority(),new Command("long-rest.occupied",ClericRpProfile.Actor,
                    active.Revision,CommandKind.BeginWorldStep,"walk",1),"LongRestRequiresInterruption",directory);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:27800,y:1);
                var after=ShortRestCapture(session);var result=after.ClericLongRestSettlements.Single();
                Require(after.RuleClock==new RuleTime(86400) && result.Benefit==ClericLongRestBenefit.Eligible
                    && result.HpBefore==8 && result.HpAfter==13 && result.ActualHealing==5
                    && result.RpBefore==1 && result.RpAfter==4 && result.ConvictionBefore==null
                    && result.ConvictionAfter==5 && result.ConvictionRestored==null && after.ConvictionBalance.Current==5
                    && result.HitDiceRecovered==0 && after.CharacterHitDice.All(x=>!x.Spent)
                    && after.DailyProvisioningSettlements.Length==2 && after.RestWatchOutcomes.Length==2
                    && after.ExpeditionBeneficialRests.Length==1
                    &&result.Refrain==1&&result.LastSpellId=="guidance"&&after.CastingStrain.Single().Refrain==1,
                    "Actual completed rest must settle finite resources and real world obligations once.");
                var pressure=after.ExpeditionPressureCheckpoints.Last();
                Require(after.ExpeditionPressureCheckpoints.Length==started.ExpeditionPressureCheckpoints.Length+1
                    &&pressure.At==after.RuleClock&&pressure.RandomBefore==started.RandomState
                    &&pressure.RandomAfter==after.RandomState&&pressure.WordsConsumed==1,
                    "The rest interval's RNG change must come only from its actual scheduled pressure check.");
                var companionDay=after.DailyProvisioningSettlements.Single(x=>x.ActorId==ClericRpProfile.Actor);
                var heroDay=after.DailyProvisioningSettlements.Single(x=>x.ActorId==ConnectedExpeditionSession.Hero);
                Require(companionDay.FoodConsumed==new RuleQuantity(2,3)&&companionDay.WaterConsumed==default(RuleQuantity)
                    &&heroDay.FoodConsumed==default(RuleQuantity)&&heroDay.WaterConsumed==default(RuleQuantity)
                    &&companionDay.HasShortfall&&heroDay.HasShortfall,
                    "Provisioning must credit only the actual meal consumption and retain each recipient's shortfall.");
                RetainDetachedLongRestCompletion(session,after,"eligible",directory);
                RetainLongRestForgedRestore(session,after,directory);
                string complete=Path.Combine(directory,"long-rest-first-funded.ddsave");session.Save(complete);session.Restore(complete);
                LongRestGuidance(session,"long-rest.guidance.after-rest");
                Require(ShortRestCapture(session).SpellCasts.Last().AppliedRefrain==2,
                    "The next actual cantrip must continue the retained nonzero Refrain.");
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                ReachClericOwnSlot(session);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.UseHealingRite,ConnectedExpeditionSession.Hero);
                var continued=ShortRestCapture(session);
                Require(continued.ResonancePools.Single().Current==2 && continued.ConvictionBalance.Current==5,
                    "Existing paid continuation must consume the recovered RP without inventing Conviction spending.");
                string paidPath=Path.Combine(directory,"long-rest-paid-continuation.ddsave");session.Save(paidPath);
                foreach(long endpoint in new[]{172799L,172800L,172801L}) {
                    session.Restore(paidPath);
                    LongRestAdvanceTo(session,endpoint-ClericLongRestProfile.DurationSeconds);
                    ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                    ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:28800,y:1);
                    var boundary=ShortRestCapture(session);var last=boundary.ClericLongRestSettlements.Last();
                    bool eligible=endpoint>=172800;
                    Require(boundary.RuleClock==new RuleTime(endpoint)&&last.Benefit==(eligible?ClericLongRestBenefit.Eligible:ClericLongRestBenefit.CadenceLimited)
                        &&last.RpBefore==2&&last.RpAfter==(eligible?4:2)&&last.ConvictionBefore==5&&last.ConvictionAfter==5
                        &&last.ConvictionRestored==0&&boundary.ExpeditionBeneficialRests.Length==(eligible?2:1)
                        &&boundary.CastingStrain.Single().Refrain==2,
                        "A genuine completion disagrees with this actor's exact 24-hour benefit boundary.");
                    if(!eligible)RetainDetachedLongRestCompletion(session,boundary,"capped",directory);
                    session.Save(Path.Combine(directory,"long-rest-cadence-"+endpoint+".ddsave"));
                }
                // Genuine attrition branch: no new supplies, no exempt actor, no synthetic strain.
                session.Restore(Path.Combine(directory,"long-rest-cadence-172800.ddsave"));
                LongRestAdvanceTo(session,316800);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:28800,y:1);
                var exhausted=ShortRestCapture(session);
                Require(ExpeditionStrainRules.Current(exhausted,ClericRpProfile.Actor).Level==5
                    &&!exhausted.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).Dead,
                    "Actual missed Watch, unpaid debt and provisioning must establish the level-5 Rest-permission witness.");
                var viewBeforeRestore=System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player));
                string strainFivePath=Path.Combine(directory,"long-rest-strain-five.ddsave");
                session.Save(strainFivePath);session.Restore(strainFivePath);
                Require(viewBeforeRestore==System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player)),
                    "Simultaneous actors' debt events must keep the public view identical across strict restore.");
                LongRestAdvanceTo(session,403200);
                ClericCommit(session,ClericRpProfile.Actor,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
                var beforeLethal=ShortRestCapture(session);
                session.Save(Path.Combine(directory,"long-rest-before-lethal-provisioning.ddsave"));
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:28800,y:1);
                var terminal=ShortRestCapture(session);var fatal=terminal.ClericLongRests.Last();
                Require(terminal.RuleClock==new RuleTime(432000)&&terminal.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).Dead
                    &&fatal.Outcome==ClericLongRestOutcome.Interrupted&&fatal.Interruption==ClericLongRestInterruption.BodyIneligible
                    &&terminal.RestIntervals.Last().Status==RestIntervalStatus.Interrupted
                    &&terminal.ClericLongRestSettlements.Length==beforeLethal.ClericLongRestSettlements.Length
                    &&terminal.ExpeditionBeneficialRests.Length==beforeLethal.ExpeditionBeneficialRests.Length
                    &&!terminal.RestDebtEvents.Any(x=>x.Kind==RestDebtEventKind.Cleared&&x.EvidenceId==fatal.Id),
                    "Tied lethal provisioning must commit elapsed consequences and interruption before completion, debt clearance or recovery.");
                session.Save(Path.Combine(directory,"long-rest-terminal-provisioning.ddsave"));
            });
        }
    }
}
#endif
