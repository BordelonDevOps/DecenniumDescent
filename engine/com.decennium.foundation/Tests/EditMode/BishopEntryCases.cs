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
        private static ConnectedExpeditionSession NewBishopExpedition() => ConnectedExpeditionSession.StartWithBishopEntry(
            ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample(),BishopEntryRecord.Announced());
        private static Simulation BishopSimulation(ConnectedExpeditionSession session) => (Simulation)typeof(ConnectedExpeditionSession)
            .GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
        private static void BishopCommit(ConnectedExpeditionSession session,Command command)
        {
            var seat=command.Actor==PostRecoveryEncounterDefinition.Actor?ExpeditionSeat.RecoveryOpponent:ExpeditionSeat.Player;
            var result=command.Kind==CommandKind.AdvanceClock||command.Kind==CommandKind.EndFixedEncounter
                ?session.SubmitSessionCommand(command):session.Submit(seat,command);
            Require(result.Response==ExpeditionResponse.Committed,"Bishop typed command failed: "+command.Id+" / "+result.Response);
        }
        private static void BishopCheckpoint(ConnectedExpeditionSession session,string directory,string name,bool restore=true)
        {
            var before=new SnapshotCodec().Encode(ShortRestCapture(session));
            string discovery=System.Text.Json.JsonSerializer.Serialize(session.DiscoverCastingCommands(ExpeditionSeat.Player,ClericRpProfile.Actor));
            string path=Path.Combine(directory,name+".ddsave");session.Save(path);
            if(restore)session.Restore(path);
            string restoredDiscovery=System.Text.Json.JsonSerializer.Serialize(session.DiscoverCastingCommands(ExpeditionSeat.Player,ClericRpProfile.Actor));
            File.WriteAllText(Path.Combine(directory,name+".discovery-before.json"),discovery);
            File.WriteAllText(Path.Combine(directory,name+".discovery-after.json"),restoredDiscovery);
            Require(discovery==restoredDiscovery,"Bishop public command discovery changed across strict restore: "+name);
            Require(before.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Bishop save/strict restore changed "+name);
            File.WriteAllText(Path.Combine(directory,name+".player.json"),System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.Player)));
            File.WriteAllText(Path.Combine(directory,name+".opponent.json"),System.Text.Json.JsonSerializer.Serialize(session.View(ExpeditionSeat.RecoveryOpponent)));
        }
        private static CharacterAdvancementRequest BishopChoices() => new CharacterAdvancementRequest(BishopProfile.SelectedCards.ToArray(),"",BishopProfile.Dispel);
        private static void BishopRejectForgedInvocation(ConnectedExpeditionSession session,string directory)
        {
            var actual=ShortRestCapture(session);var use=actual.BishopEntry.Invocations.Single();var codec=new SnapshotCodec();var before=codec.Encode(actual);
            var rows=use.Recipients.Select((x,i)=>i==0?new InvocationHealingRecord(x.TargetId,x.HpBefore-1,x.Potential,x.HpAfter-1):x).ToArray();
            var altered=new DivineInvocationRecord(use.CommandId,use.Revision,use.Turn,use.At,use.Choice,use.RpBefore,use.ConvictionBefore,use.DissonanceBefore,
                use.Die,use.RandomBefore,use.RandomAfter,use.WordsConsumed,rows,use.CureAt,use.CureOperationId,use.EndedApplicationIds);
            var forged=actual.Copy();forged.BishopEntry=forged.BishopEntry.WithInvocations(new[]{altered});
            string path=Path.Combine(directory,"forged-invocation-healing.ddsave");var bytes=codec.Encode(forged);File.WriteAllBytes(path,bytes);
            Throws<ArgumentException>(()=>session.Restore(path));
            Require(before.SequenceEqual(codec.Encode(ShortRestCapture(session)))&&bytes.SequenceEqual(File.ReadAllBytes(path)),"Strict restore accepted or repaired invented historical Invocation healing.");
            File.WriteAllBytes(Path.Combine(directory,"forged-invocation-before.ddsave"),before);
            File.WriteAllBytes(Path.Combine(directory,"forged-invocation-after.ddsave"),codec.Encode(ShortRestCapture(session)));
        }
        private static ConnectedExpeditionSession FundBishop(string directory,bool controls=false,ConnectedExpeditionSession expedition=null,
            Func<int,int> heroStance=null)
        {
            const string hero=ConnectedExpeditionSession.Hero,cleric=ClericRpProfile.Actor;
            var session=EarnClericObjective(true,directory,expedition??NewBishopExpedition(),heroStance:heroStance,beforeInitialRite:live=>{
                if(controls) {
                    Require(ShortRestCapture(live).Revision==145,"Discovery regression must reach genuine uninterrupted revision145.");
                    BishopCheckpoint(live,directory,"r145-companion-discovery");
                }
            });
            BishopCommit(session,new Command("bishop.typed.earned2.award",cleric,ShortRestCapture(session).Revision,CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
            BishopCommit(session,new Command("bishop.typed.earned2.advance",cleric,ShortRestCapture(session).Revision,CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()));
            ClericCommit(session,cleric,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
            var firstRestDue = ShortRestCapture(session).ClericLongRests.Last().DueAt;
            void Intake(string item,int amount,int seconds) {
                BishopCommit(session,new Command("bishop.typed.intake."+item,hero,ShortRestCapture(session).Revision,CommandKind.StartIntake,item,inventory:new InventoryRequest(Q(amount))));
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:seconds,y:1);
            }
            Intake("TEST_ONLY.pack-rations",2,1800);Intake("TEST_ONLY.ready-water",4,240);Intake("TEST_ONLY.pack-water",4,240);
            PostRecoveryStep(session,hero,1,0);PostRecoveryAdvanceTo(session,firstRestDue);
            BishopCheckpoint(session,directory,"first-rest");
            Require(ShortRestCapture(session).ClericLongRestSettlements.Single().RpMaximum==4,"Historical level2 rest lost its own capacity.");
            ReachClericOwnSlot(session);LongRestGuidance(session,"bishop.typed.guidance.before-care");
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
            ClericCommit(session,cleric,CommandKind.UseHealingRite,hero);
            Require(ShortRestCapture(session).HealingRites.Last().ActualGain>0,"Bishop objective requires real positive base care.");
            ClericCommit(session,cleric,CommandKind.BeginWorldStep,"walk",1,0);
            var started=ShortRestCapture(session);
            Require(started.BishopEntry.Departure!=null&&!started.BishopEntry.Departure.Complete,"Starting departure must not complete objective.");
            if(controls) {
                var denied=new Command("bishop.typed.premature-award",cleric,started.Revision,CommandKind.AwardCharacterMilestone,BishopProfile.Milestone);
                var before=new SnapshotCodec().Encode(started);Require(session.Submit(ExpeditionSeat.Player,denied).Response==ExpeditionResponse.Unavailable,"Partial departure awarded advancement.");
                Require(before.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Premature award changed state.");
                BishopCheckpoint(session,directory,"departure-pending");
            }
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:1,y:1);
            var departed=ShortRestCapture(session);Require(departed.BishopEntry.Departure.Complete,"Paid departure did not complete objective.");
            BishopCheckpoint(session,directory,"departure-complete");
            var award=new Command("bishop.typed.earned3.award",cleric,departed.Revision,CommandKind.AwardCharacterMilestone,BishopProfile.Milestone);
            var awardQuery=session.QueryCastingCommand(ExpeditionSeat.Player,award);
            var awardOption=session.DiscoverCastingCommands(ExpeditionSeat.Player,cleric).Single(x=>x.Command.Kind==CommandKind.AwardCharacterMilestone&&x.Command.Target==BishopProfile.Milestone);
            Require(awardQuery.Admissible&&awardOption.Query.Admissible,"Genuine available Bishop award disagrees across query/discovery and submission.");
            var beforeAward=new SnapshotCodec().Encode(departed);session.SetSeatEnabled(ExpeditionSeat.Player,false);
            Require(session.QueryCastingCommand(ExpeditionSeat.Player,award).Code=="NotAuthorized"&&session.DiscoverCastingCommands(ExpeditionSeat.Player,cleric).Count==0
                &&session.Submit(ExpeditionSeat.Player,award).Response==ExpeditionResponse.NotAuthorized
                &&beforeAward.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Revoked Player received trusted milestone authority.");
            session.SetSeatEnabled(ExpeditionSeat.Player,true);BishopCommit(session,award);
            Require(session.QueryCastingCommand(ExpeditionSeat.Player,award).Code=="AlreadyCommitted"&&session.Submit(ExpeditionSeat.Player,award).Response==ExpeditionResponse.Duplicate,
                "Bishop award query/submission retry protection differs.");
            var awardedBytes=new SnapshotCodec().Encode(ShortRestCapture(session));session.SetSeatEnabled(ExpeditionSeat.Player,false);
            Require(session.QueryCastingCommand(ExpeditionSeat.Player,award).Code=="NotAuthorized"&&session.Submit(ExpeditionSeat.Player,award).Response==ExpeditionResponse.NotAuthorized
                &&session.DiscoverCastingCommands(ExpeditionSeat.Player,cleric).Count==0&&awardedBytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),
                "Revocation disclosed an existing Bishop award or repeated it.");session.SetSeatEnabled(ExpeditionSeat.Player,true);
            File.WriteAllText(Path.Combine(directory,"bishop-award-authority.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Genuine completed departure; command-specific host authority across public query, discovery, execution, duplicate and revoked-seat boundaries",awardQuery,awardOption.Query,
                available=true,committed=true,duplicateProtected=true,revokedBeforeAndAfter=true,denialsUnchanged=true}));
            BishopCheckpoint(session,directory,"earned3-awarded");
            var beforeAdvance=ShortRestCapture(session);
            var advance=new Command("bishop.typed.earned3.advance",cleric,beforeAdvance.Revision,CommandKind.AdvanceCharacterLevel,BishopProfile.Milestone,advancement:BishopChoices());
            if(controls) {
                var bad=new CharacterAdvancementRequest(new[]{BishopProfile.Aura,BishopProfile.Aura},"",BishopProfile.Dispel);
                var denied=new Command("bishop.typed.duplicate-card",cleric,beforeAdvance.Revision,CommandKind.AdvanceCharacterLevel,BishopProfile.Milestone,advancement:bad);
                Require(session.Submit(ExpeditionSeat.Player,denied).Response==ExpeditionResponse.Unavailable,"Duplicate Arch selected.");
                Require(new SnapshotCodec().Encode(beforeAdvance).SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Invalid advancement partially committed.");
            }
            BishopCommit(session,advance);var advanced=ShortRestCapture(session);
            Require(advanced.Lives.Single(x=>x.ActorId==cleric).Hp==13&&advanced.Lives.Single(x=>x.ActorId==cleric).MaximumHp==18
                &&advanced.ResonancePools.Single().Current==2&&advanced.ResonancePools.Single().Maximum==7
                &&advanced.ConvictionBalance.Current==5&&advanced.KnownSpells.Length==7
                &&advanced.CharacterHitDice.Count(x=>x.ActorId==cleric)==3&&advanced.RandomState==beforeAdvance.RandomState
                &&advanced.RuleClock==beforeAdvance.RuleClock,"Earned3 manufactured resources or omitted its atomic grants.");
            BishopCheckpoint(session,directory,"earned3");
            var sim=BishopSimulation(session);var authority=new Authority("TEST_ONLY.host",new[]{hero,cleric},canModifyWorld:true,inventoryOwners:new[]{hero,cleric});
            RetainClericDenial(sim,authority,new Command("bishop.typed.unfunded",cleric,advanced.Revision,CommandKind.UseDivineInvocation,
                divineInvocation:new DivineInvocationRequest(new[]{hero,cleric})),"InsufficientResonance",directory);
            Require(session.Submit(ExpeditionSeat.Player,advance).Response==ExpeditionResponse.Duplicate,"Earned3 retry was not idempotent.");
            PostRecoveryStep(session,cleric,-1,0);PostRecoveryAdvanceTo(session,firstRestDue.AddSeconds(
                ClericLongRestProfile.BenefitCadenceSeconds-ClericLongRestProfile.DurationSeconds));
            ClericCommit(session,cleric,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);ClericCommit(session,hero,CommandKind.AdvanceClock,x:28800,y:1);
            var funded=ShortRestCapture(session);Require(funded.ResonancePools.Single().Current==7&&funded.ConvictionBalance.Current==5
                &&funded.ClericLongRestSettlements.Last().RpMaximum==7,"Eligible level3 rest did not fund actual capacity.");
            BishopCheckpoint(session,directory,"second-rest");return session;
        }
        private static void BishopSupplementalInvocation(ConnectedExpeditionSession session,Snapshot ready,string directory)
        {
            // Approved cardinality supplement: existing opponent is declared allied in this detached candidate only.
            // No third-ally acquisition or supported altered save is claimed.
            const string hero=ConnectedExpeditionSession.Hero,cleric=ClericRpProfile.Actor,third=PostRecoveryEncounterDefinition.Actor;
            var candidate=ready.Copy();candidate.TacticalAllies=candidate.TacticalAllies.Append(new TacticalAllyRecord(cleric,third)).ToArray();
            var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.NonPublic|BindingFlags.Static);
            var thirdLife=candidate.Lives.Single(x=>x.ActorId==third);apply.Invoke(null,new object[]{candidate,thirdLife,new LifeState(thirdLife.MaximumHp,1)});
            var request=new DivineInvocationRequest(new[]{third,cleric,hero},hero,RadianceCurePreference.Frightened);
            var command=new Command("bishop.supplement.three",cleric,candidate.Revision,CommandKind.UseDivineInvocation,divineInvocation:request);
            var policy=ClericPolicy(session);string failure=policy.Resolve(candidate,command);
            Require(failure==null,"Actual paid three-target producer rejected: "+failure);
            var use=candidate.BishopEntry.Invocations.Last();
            Require(use.Recipients.Count==3&&use.Recipients.All(x=>x.ActualGain>0)&&use.Recipients.Select(x=>x.TargetId).SequenceEqual(request.TargetIds)
                &&use.RpAfter==2&&use.ConvictionAfter==3&&use.EndedApplicationIds.Count>0&&candidate.RandomState==use.RandomAfter
                &&candidate.HealingRites.Length==ready.HealingRites.Length&&candidate.RadianceUses.Length==ready.RadianceUses.Length
                &&candidate.BishopEntry.AuraHealing.Count==ready.BishopEntry.AuraHealing.Count,"Three-target producer did not share one paid draw or improperly invoked Rite riders.");
            var capped=ready.Copy();var heroLife=capped.Lives.Single(x=>x.ActorId==hero);
            apply.Invoke(null,new object[]{capped,heroLife,new LifeState(heroLife.MaximumHp,heroLife.MaximumHp)});
            var cappedUse=new Command("bishop.supplement.capped-cure",cleric,capped.Revision,CommandKind.UseDivineInvocation,
                divineInvocation:new DivineInvocationRequest(new[]{hero},hero,RadianceCurePreference.Frightened));
            Require(policy.Resolve(capped,cappedUse)==null&&capped.BishopEntry.Invocations.Last().Recipients.Single().ActualGain==0
                &&capped.BishopEntry.Invocations.Last().EndedApplicationIds.Count>0,"Invocation imported the positive-Rite prerequisite into its independent cure.");
            var protectedCure=DetachedRadianceConditions(ready,RadianceCurePreference.Poisoned,independent:false);
            var cure=new Command("bishop.supplement.poisoned",cleric,protectedCure.Revision,CommandKind.UseDivineInvocation,
                divineInvocation:new DivineInvocationRequest(new[]{hero},hero,RadianceCurePreference.Poisoned));
            Require(policy.Resolve(protectedCure,cure)==null&&protectedCure.BishopEntry.Invocations.Last().EndedApplicationIds.SequenceEqual(new[]{"detached.eligible","detached.suppressed"}),
                "Invocation missed suppressed eligible Poisoned or cured a protected application.");
            var poisonHistory=ConditionHistory.Restore(protectedCure.Conditions.Single(x=>x.Target==hero));
            Require(poisonHistory.Ledger.Applications.Single(x=>x.Id=="detached.protected").Present(poisonHistory.Ledger.Now),"Protected poison ended.");
            var vented=ready.Copy();var priorStrain=vented.CastingStrain.Single(x=>x.ActorId==cleric);
            vented.CastingStrain=vented.CastingStrain.Select(x=>x.ActorId==cleric?new CastingStrainRecord(cleric,3,x.LastSpellId,x.Refrain,x.LastCastRevision):x).ToArray();
            Require(policy.Resolve(vented,new Command("bishop.supplement.positive-vent",cleric,vented.Revision,CommandKind.UseDivineInvocation,
                divineInvocation:new DivineInvocationRequest(new[]{hero,cleric})))==null,"Positive vent paid producer failed.");
            var vent=vented.BishopEntry.Invocations.Last();var afterStrain=vented.CastingStrain.Single(x=>x.ActorId==cleric);
            Require(vent.DissonanceBefore==3&&vent.DissonanceAfter==2&&vent.ActualVent==1&&afterStrain.Dissonance==2
                &&afterStrain.LastSpellId==priorStrain.LastSpellId&&afterStrain.Refrain==priorStrain.Refrain&&afterStrain.LastCastRevision==priorStrain.LastCastRevision,
                "Actual Conviction payment did not vent positive Dissonance once or changed spell/Refrain history.");
            var denials=new List<object>();
            foreach(string kind in new[]{"rp","conviction","hostile","unknown","range","history"}) {
                var denied=ready.Copy();string target=hero,expected="InvocationTargetUnavailable";
                if(kind=="rp"){denied.ResonancePools=denied.ResonancePools.Select(x=>x.Pay(3)).ToArray();expected="InsufficientResonance";}
                if(kind=="conviction"){var balance=denied.ConvictionBalance;denied.ConvictionBalance=new ConvictionBalanceRecord(balance.FundingRestId,balance.FundingRevision,1);expected="InsufficientConviction";}
                if(kind=="hostile")target=third;
                if(kind=="unknown")target="TEST_ONLY.unknown";
                if(kind=="range")denied.Actors.Single(x=>x.Id==hero).X=denied.Actors.Single(x=>x.Id==cleric).X+7;
                if(kind=="history"){denied.BishopEntry=denied.BishopEntry.WithInvocations(Enumerable.Repeat(use,128));expected="InvocationHistoryFull";}
                string before=ClericRaw(denied);
                string failureCode=policy.Resolve(denied,new Command("bishop.supplement.denied."+kind,cleric,denied.Revision,CommandKind.UseDivineInvocation,
                    divineInvocation:new DivineInvocationRequest(new[]{target})));
                Require(failureCode==expected&&before==ClericRaw(denied),"Invocation preflight changed detached state or returned an incorrect denial: "+kind+" / "+failureCode);
                denials.Add(new{kind,expected,unchanged=true});
            }
            File.WriteAllText(Path.Combine(directory,"supplemental-three-and-capped-cure.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Detached allied third target, resource, condition and full-HP setup; actual paid producer and preflight; no connected acquisition or supported altered save",
                three=use,capped=capped.BishopEntry.Invocations.Last(),protectedPoisoned=protectedCure.BishopEntry.Invocations.Last(),positiveVent=vent,denials}));
        }
        private static AuraOfFaithQualification BishopQualification(Snapshot state,string actor) => (AuraOfFaithQualification)typeof(TestOnlySharedWorldPolicy).Assembly
            .GetType("Decennium.Foundation.Laboratory.AuraOfFaithRules").GetMethod("Qualify",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{state,actor});
        private static void BishopSupplementalAura(Snapshot ready,string directory)
        {
            const string hero=ConnectedExpeditionSession.Hero,cleric=ClericRpProfile.Actor;
            var results=new List<object>();
            void Condition(Snapshot s,string target,string kind) {
                var at=new ConditionStamp(s.RuleClock);var history=ConditionHistory.Restore(s.Conditions.Single(x=>x.Target==target));
                if(!history.Journal.Now.Equals(at))history=history.Append(ConditionOperation.Advance("bishop.supplement.sync",at)).State;
                history=history.Append(ConditionOperation.Apply("bishop.supplement.condition",at,new ConditionApplicationData("bishop.supplement.condition",
                    "TEST_ONLY.owner","TEST_ONLY.supplement",kind,null,"source-end",true),kind=="Unconscious"?"bishop.supplement.prone":"")).State;
                s.Conditions=s.Conditions.Select(x=>x.Target==target?history.Journal:x).ToArray();
            }
            foreach(string kind in new[]{"Incapacitated","Unconscious","Blinded"}) {
                var s=ready.Copy();Condition(s,cleric,kind);var q=BishopQualification(s,cleric);
                Require(q.Qualified==(kind=="Incapacitated"),"Aura conflated incapacity, consciousness or perception: "+kind);results.Add(new{kind,qualification=q});
            }
            var blind=ready.Copy();Condition(blind,hero,"Blinded");Require(!BishopQualification(blind,hero).Qualified,"Blind recipient perceived Aura owner.");
            var q0=BishopQualification(ready,hero);Require(q0.Qualified,"Genuine ready geometry lost Aura.");
            foreach(int other in new[]{0,1,2}) {
                var record=new AuraOfFaithSaveRecord("bishop.supplement.save."+other,"bishop.supplement.cause",ready.Revision+1,ready.RuleClock,
                    AuraSaveConsumer.Frightened,q0,0,other,10,9,false,true,1,2,1);
                Require(record.Modifier==Math.Max(1,other)&&record.AuraContribution==(other==0?1:0),"Strongest-flat Aura stacked.");results.Add(record);
            }
            var edge=new AuraOfFaithQualification(q0.AcquiredRevision,hero,true,true,true,true,Q(0),Q(0),Q(3),Q(0));
            var beyond=new AuraOfFaithQualification(q0.AcquiredRevision,hero,true,true,true,true,Q(0),Q(0),new RuleQuantity(3001,1000),Q(0));
            Require(edge.Qualified&&!beyond.Qualified,"Aura rounded fractional geometry into range.");
            var pending=ready.Copy();var apply=typeof(TestOnlyClubAttackPolicy).GetMethod("ApplyLife",BindingFlags.NonPublic|BindingFlags.Static);
            var heroLife=pending.Lives.Single(x=>x.ActorId==hero);apply.Invoke(null,new object[]{pending,heroLife,new LifeState(heroLife.MaximumHp,1)});
            heroLife=pending.Lives.Single(x=>x.ActorId==hero);
            var damage=typeof(TestOnlySharedWorldPolicy).Assembly.GetType("Decennium.Foundation.Laboratory.AuraOfFaithRules")
                .GetMethod("Damage",BindingFlags.Static|BindingFlags.NonPublic);
            var first=(RolledDamage)damage.Invoke(null,new object[]{pending,heroLife,"bishop.supplement.pending",1L,pending.RuleClock,pending.RandomState,
                0,false,false,true,KnockoutInstruction.AskIfEligible,false});
            int saves=pending.BishopEntry.AuraSaves.Count;var wound=pending.BishopEntry.AuraSaves.Last();
            Require(first.Pending!=null&&first.Outcome==null&&wound.Consumer==AuraSaveConsumer.Wound&&wound.AuraContribution==1
                &&pending.Lives.Single(x=>x.ActorId==hero).Hp==1,"Incoming Wound qualification did not preserve pre-damage pending life.");
            var ownerLife=pending.Lives.Single(x=>x.ActorId==cleric);apply.Invoke(null,new object[]{pending,ownerLife,new LifeState(ownerLife.MaximumHp,0)});
            Require(!BishopQualification(pending,hero).Qualified,"Unconscious owner still supplied current Aura.");
            var rebuilt=(RolledDamage)damage.Invoke(null,new object[]{pending,heroLife,"bishop.supplement.pending",1L,pending.RuleClock,pending.RandomState,
                0,false,false,true,KnockoutInstruction.AskIfEligible,true});
            Require(rebuilt.Pending!=null&&rebuilt.NextRandomState==first.NextRandomState&&rebuilt.WordsConsumed==first.WordsConsumed
                &&rebuilt.WoundRoll.Natural==first.WoundRoll.Natural&&pending.BishopEntry.AuraSaves.Count==saves,
                "Pending Wound recalculated current Aura, rerolled, or duplicated history.");
            results.Add(new{scope="Detached incoming-life and changed-owner control through actual pending damage producer; no supported changed-owner save",wound,
                first.NextRandomState,first.WordsConsumed});
            File.WriteAllText(Path.Combine(directory,"supplemental-aura-boundaries.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Detached qualification and numeric arbitration controls; genuine save and healing consumers are separately required",results,edge,beyond}));
        }
        private static void BishopSelfObservationBlindness(string directory)
        {
            const string cleric=ClericRpProfile.Actor,hero=ConnectedExpeditionSession.Hero;
            var branch=NewBishopExpedition();branch.Restore(Path.Combine(directory,"third-rest.ddsave"));ReachClericOwnSlot(branch);
            void Cast(string id,string spell)=>BishopCommit(branch,new Command(id,cleric,ShortRestCapture(branch).Revision,CommandKind.CastKnownSpell,cleric,
                spellCast:new SpellCastRequest(spell,spell=="guidance"?"":"TEST_ONLY.cleric-casting.holy-symbol",spell=="guidance")));
            Cast("bishop.sight.guidance","guidance");ClericCommit(branch,hero,CommandKind.AdvanceClock,x:6,y:1);
            Cast("bishop.sight.detect","detect-magic");ClericCommit(branch,hero,CommandKind.AdvanceClock,x:6,y:1);
            var option=branch.DiscoverCastingCommands(ExpeditionSeat.Player,cleric).Single(x=>x.Query.Admissible
                &&x.Command.Kind==CommandKind.CastKnownSpell&&x.Command.SpellCast.SpellId==BishopProfile.Dispel);
            Require(option.Query.Admissible&&branch.QueryCastingCommand(ExpeditionSeat.Player,option.Command).Admissible,"Sighted self-hosted Guidance is not observable/selectable.");
            BishopCheckpoint(branch,directory,"self-guidance-observed");var ready=ShortRestCapture(branch);var candidate=ready.Copy();
            var at=new ConditionStamp(candidate.RuleClock);var history=ConditionHistory.Restore(candidate.Conditions.Single(x=>x.Target==cleric));
            if(!history.Journal.Now.Equals(at))history=history.Append(ConditionOperation.Advance("bishop.sight.sync",at)).State;
            history=history.Append(ConditionOperation.Apply("bishop.sight.apply",at,new ConditionApplicationData("bishop.sight.blinded",
                "TEST_ONLY.supplement","TEST_ONLY.sight-control","Blinded",null,"source-end",true))).State;
            candidate.Conditions=candidate.Conditions.Select(x=>x.Target==cleric?history.Journal:x).ToArray();
            var authority=new Authority("TEST_ONLY.host",new[]{hero,cleric},inventoryOwners:new[]{hero,cleric});var policy=ClericPolicy(branch);
            var queryPolicy=(ICommandQueryPolicy)policy;string before=ClericRaw(candidate);
            var observe=typeof(TestOnlySharedWorldPolicy).GetMethod("ObserveCasting",BindingFlags.NonPublic|BindingFlags.Static);
            var view=(ExpeditionCastingView)observe.Invoke(null,new object[]{candidate,cleric});
            var query=queryPolicy.QueryCommand(candidate.Copy(),authority,option.Command);
            var discoveries=queryPolicy.DiscoverCommands(candidate.Copy(),authority,cleric).Where(x=>x.Kind==CommandKind.CastKnownSpell&&x.SpellCast.SpellId==BishopProfile.Dispel).ToArray();
            string failure=policy.Resolve(candidate,option.Command);
            Require(view.Auras.Count==0&&!query.Admissible&&query.Code=="AuraObservationUnavailable"&&discoveries.Length==0
                &&failure=="AuraObservationUnavailable"&&before==ClericRaw(candidate),"Blinded self-hosted Guidance retained a selectable old observation or paid for Dispel.");
            File.WriteAllText(Path.Combine(directory,"supplemental-self-observation-blinded.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Actual own Guidance/Detect and public observation token, then detached actual Blinded lifecycle; actual views/discovery/query/resolver reject; no connected blindness acquisition or altered save claimed",
                tokenBeforeSightLoss=option.Command.Target,query,failure,outlineCount=view.Auras.Count,dispelOptions=discoveries.Length,
                unchanged=true,rpBefore=ready.ResonancePools.Single().Current,rpAfter=candidate.ResonancePools.Single().Current,
                randomBefore=ready.RandomState,randomAfter=candidate.RandomState}));
        }
        private static void RunBishopTypedCampaign(string directory)
        {
            const string hero=ConnectedExpeditionSession.Hero,cleric=ClericRpProfile.Actor,npc=PostRecoveryEncounterDefinition.Actor;
            var session=FundBishop(directory,true);int sequence=0;
            Command Make(CommandKind kind,string actor=cleric,string target="",CombatRequest combat=null,DivineInvocationRequest invocation=null,SpellCastRequest spell=null,
                IntimidatingPresenceRequest fear=null,HealingRiteRequest rite=null) => new Command("bishop.typed.campaign."+(++sequence),actor,
                    ShortRestCapture(session).Revision,kind,target,combat:combat,divineInvocation:invocation,spellCast:spell,intimidatingPresence:fear,healingRite:rite);
            void Cast(string id,string target,bool willing=false) => BishopCommit(session,Make(CommandKind.CastKnownSpell,target:target,
                spell:new SpellCastRequest(id,id=="guidance"?"":"TEST_ONLY.cleric-casting.holy-symbol",willing)));
            PostRecoveryStep(session,cleric,1,0);PostRecoveryStep(session,cleric,1,0);PostRecoveryStep(session,cleric,0,1);
            PostRecoveryStep(session,hero,1,0);PostRecoveryStep(session,hero,1,0);
            var staged=ShortRestCapture(session);var epoch=staged.Reinforcement.Admission.Phase.Epoch;var duration=new RuleTime(30,TestOnlyClubAttackPolicy.WalkingSpeed(staged,hero));
            var earliest=new RuleTime(staged.RuleClock.Numerator*duration.Denominator+duration.Numerator*staged.RuleClock.Denominator,staged.RuleClock.Denominator*duration.Denominator);
            long slot=epoch.SlotAt(staged.RuleClock);while(epoch.Order[(int)(slot%epoch.Order.Count)]!="TEST_ONLY.later-defender"||epoch.Start(slot)<earliest)slot++;
            var arrival=epoch.Start(slot);PostRecoveryAdvanceTo(session,new RuleTime(arrival.Numerator*duration.Denominator-duration.Numerator*arrival.Denominator,arrival.Denominator*duration.Denominator));
            BishopCheckpoint(session,directory,"before-contact");PostRecoveryStep(session,hero,0,1);BishopCheckpoint(session,directory,"entered");
            var initial=ShortRestCapture(session);long heroHp=initial.Lives.Single(x=>x.ActorId==hero).Hp,clericHp=initial.Lives.Single(x=>x.ActorId==cleric).Hp;
            bool feared=false,detected=false,invoked=false,cared=false;int deadEnds=0;
            for(int turn=0;turn<100;turn++) {
                var s=ShortRestCapture(session);string actor=s.Encounter.CurrentActor,turnId=s.Encounter.CurrentTurnId;
                var life=s.Lives.Single(x=>x.ActorId==actor);var enemy=s.Lives.Single(x=>x.ActorId==npc);
                var h=s.Lives.Single(x=>x.ActorId==hero);var a=s.Lives.Single(x=>x.ActorId==cleric);
                if(life.Hp>0&&!life.Dead) {
                    BishopCommit(session,Make(CommandKind.SelectCombatStance,actor,combat:new CombatRequest(turnId,stance:1)));
                    if(enemy.Dead&&deadEnds>=3&&actor==hero) {BishopCommit(session,Make(CommandKind.EndFixedEncounter,hero,turnId));break;}
                    if(actor==npc) {
                        var recharge=s.AbilityRecharges.SingleOrDefault(x=>x.ActorId==npc&&x.AbilityId==FrightenedProfile.SourceId);
                        if(!feared||!invoked&&h.Hp<heroHp&&a.Hp<clericHp&&recharge?.Remaining==0) {
                            BishopCommit(session,Make(CommandKind.UseIntimidatingPresence,npc,fear:new IntimidatingPresenceRequest(new[]{hero,cleric})));feared=true;
                        } else {
                            string target=!invoked&&h.Hp>=heroHp?hero:!invoked&&a.Hp>=clericHp?cleric:invoked&&!cared&&h.Hp>13?hero:"";
                            if(target!="")BishopCommit(session,Make(CommandKind.AttackClub,npc,target,new CombatRequest(turnId,"TEST_ONLY.recovery-defender-club")));
                        }
                    } else if(actor==cleric) {
                        string cure=new[]{hero,cleric}.FirstOrDefault(x=>TestOnlyClubAttackPolicy.ConditionsFor(s,x).View().Has(ConditionKind.Frightened));
                        if(!detected){Cast("detect-magic",cleric);detected=true;}
                        else if(!invoked&&h.Hp<heroHp&&a.Hp<clericHp&&cure!=null) {
                            var ready=ShortRestCapture(session);BishopSupplementalInvocation(session,ready,directory);BishopSupplementalAura(ready,directory);
                            var command=Make(CommandKind.UseDivineInvocation,invocation:new DivineInvocationRequest(new[]{hero,cleric},cure,RadianceCurePreference.Frightened));
                            AssertPureUtility(session,command);
                            BishopCommit(session,command);invoked=true;var paid=ShortRestCapture(session);var use=paid.BishopEntry.Invocations.Single();
                            Require(use.Recipients.Count(x=>x.ActualGain>0)==2&&use.EndedApplicationIds.Count>0&&use.ActualVent==0,"Genuine two-target healing, positive cure or zero-floor vent missing.");
                            BishopCheckpoint(session,directory,"invocation-cure");
                            BishopRejectForgedInvocation(session,directory);
                            Require(session.Submit(ExpeditionSeat.Player,command).Response==ExpeditionResponse.Duplicate,"Paid Invocation retry repeated.");
                            var restricted=new Authority("TEST_ONLY.host",new[]{cleric},inventoryOwners:new[]{cleric});
                            RetainClericDenial(BishopSimulation(session),restricted,command,"NotAuthorized",directory);
                            Require(paid.SpellEffects.Any(x=>x.Present&&x.SpellId=="detect-magic"),"Invocation replaced concentration.");
                        } else if(invoked&&!cared&&h.Hp<=13) {
                            var rite=Make(CommandKind.UseHealingRite,target:hero,rite:new HealingRiteRequest(RadianceCurePreference.None));
                            AssertPureUtility(session,rite);BishopCommit(session,rite);cared=true;
                            var care=ShortRestCapture(session);Require(care.HealingRites.Last().ActualGain>0&&care.RadianceUses.Last().AdditionalGain>0
                                &&care.BishopEntry.AuraHealing.Last().ActualGain>0,"Positive base, Radiance and Aura healing not reached.");BishopCheckpoint(session,directory,"rite-radiance-aura");
                        }
                    } else if(actor==hero&&!enemy.Dead&&invoked&&cared)BishopCommit(session,Make(CommandKind.AttackClub,hero,npc,new CombatRequest(turnId,"TEST_ONLY.actor-club")));
                }
                BishopCommit(session,Make(CommandKind.EndRegularTurn,actor,turnId));if(enemy.Dead)deadEnds++;
            }
            var closed=ShortRestCapture(session);Require(!closed.InventoryCombat&&invoked&&cared,"Connected Bishop combat did not close.");
            Require(closed.BishopEntry.AuraSaves.Any(x=>x.OutcomeChangedByAura)&&closed.BishopEntry.AuraSaves.Any(x=>x.Consumer==AuraSaveConsumer.Concentration&&x.AuraContribution==1),
                "Genuine outcome-changing Aura and concentration saves are mandatory.");BishopCheckpoint(session,directory,"closed");
            PostRecoveryStep(session,hero,-1,0);PostRecoveryStep(session,hero,-1,0);PostRecoveryStep(session,hero,0,-1);
            PostRecoveryStep(session,cleric,0,-1);PostRecoveryStep(session,cleric,-1,0);PostRecoveryStep(session,cleric,-1,0);
            foreach(var effect in ShortRestCapture(session).SpellEffects.Where(x=>x.Present&&x.RequiresConcentration&&x.CasterId==cleric))
                BishopCommit(session,Make(CommandKind.EndSpellConcentration,target:effect.Id));
            PostRecoveryAdvanceTo(session,new RuleTime(459041,2));ClericCommit(session,cleric,CommandKind.BeginLongRest,ClericLongRestProfile.SiteId);
            ClericCommit(session,hero,CommandKind.AdvanceClock,x:28800,y:1);BishopCheckpoint(session,directory,"third-rest");
            BishopSelfObservationBlindness(directory);
            ReachClericOwnSlot(session);Cast("guidance",hero,true);ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);Cast("detect-magic",cleric);
            BishopCheckpoint(session,directory,"guidance-detect");ClericCommit(session,hero,CommandKind.AdvanceClock,x:6,y:1);
            var view=session.View(ExpeditionSeat.Player);var position=view.Actors.Single(x=>x.Position.Id==hero).Position;
            string observation=view.Actors.Single(x=>x.Position.Id==cleric).Casting.Auras.Single(x=>x.X==position.X&&x.Y==position.Y).ObservationId;
            var beforeDispel=ShortRestCapture(session);
            var authority=new Authority("TEST_ONLY.host",new[]{hero,cleric},canModifyWorld:true,inventoryOwners:new[]{hero,cleric});
            var internalEffect=beforeDispel.SpellEffects.Single(x=>x.Present&&x.SpellId=="guidance");
            RetainClericDenial(BishopSimulation(session),authority,Make(CommandKind.CastKnownSpell,target:internalEffect.Id,
                spell:new SpellCastRequest(BishopProfile.Dispel,"TEST_ONLY.cleric-casting.holy-symbol")),"AuraObservationUnavailable",directory);
            RetainClericDenial(BishopSimulation(session),authority,Make(CommandKind.CastKnownSpell,target:"aura.unknown",
                spell:new SpellCastRequest(BishopProfile.Dispel,"TEST_ONLY.cleric-casting.holy-symbol")),"AuraObservationUnavailable",directory);
            var dispel=Make(CommandKind.CastKnownSpell,target:observation,spell:new SpellCastRequest(BishopProfile.Dispel,"TEST_ONLY.cleric-casting.holy-symbol"));
            AssertPureUtility(session,dispel);
            BishopCommit(session,dispel);var dispelled=ShortRestCapture(session);
            Require(dispelled.BishopEntry.Dispels.Count==1&&!dispelled.SpellEffects.Any(x=>x.Present&&x.SpellId=="guidance")
                &&dispelled.SpellEffects.Any(x=>x.Present&&x.SpellId=="detect-magic")&&dispelled.RandomState==beforeDispel.RandomState
                &&dispelled.ResonancePools.Single().Current==2,"Dispel failed effect-specific ending, no RNG or payment.");
            BishopCheckpoint(session,directory,"guidance-dispelled");
            var stable=new SnapshotCodec().Encode(ShortRestCapture(session));Require(session.Submit(ExpeditionSeat.Player,dispel).Response==ExpeditionResponse.Duplicate
                &&stable.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Dispel retry repeated ending or payment.");
            PostRecoveryStep(session,cleric,1,0);BishopCheckpoint(session,directory,"continued");
            var final=ShortRestCapture(session);File.WriteAllText(Path.Combine(directory,"bishop-connected-facts.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Independent typed commands from genesis with genuine funding, fear, injury, positive cure, two recipients, changed Aura save, concentration, healing, Dispel and travel",
                final.Revision,final.RuleClock,final.BishopEntry,final.ClericLongRestSettlements}));
        }
        private static void AddBishopEntryCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("chr03_bishop_recharge_actual_outside_starts_and_epoch_transfer",()=>{
                const string hero=ConnectedExpeditionSession.Hero,cleric=ClericRpProfile.Actor;
                var session=FundBishop(directory);ReachClericOwnSlot(session);
                int Remaining()=>ShortRestCapture(session).AbilityRecharges.Single(x=>x.ActorId==cleric&&x.AbilityId==BishopProfile.Invocation).Remaining;
                void Invoke(string id)=>BishopCommit(session,new Command(id,cleric,ShortRestCapture(session).Revision,CommandKind.UseDivineInvocation,
                    divineInvocation:new DivineInvocationRequest(new[]{cleric})));
                Invoke("bishop.recharge.first");Require(Remaining()==3,"Resolution did not set recharge3.");BishopCheckpoint(session,directory,"outside-recharge3");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:11,y:2);Require(Remaining()==3,"Elapsed partial six seconds ticked recharge.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:1,y:2);Require(Remaining()==2,"First actual outside owner Start did not tick exactly once.");
                ClericCommit(session,hero,CommandKind.AdvanceClock,x:12,y:1);Require(Remaining()==0,"Three actual Starts did not ready Invocation.");
                var ready=ShortRestCapture(session);Require(ready.ResonancePools.Single().Current==4&&ready.ConvictionBalance.Current==3,"Recharge refilled resources.");
                PostRecoveryStep(session,cleric,1,0);PostRecoveryStep(session,cleric,1,0);PostRecoveryStep(session,cleric,0,1);
                PostRecoveryStep(session,hero,1,0);PostRecoveryStep(session,hero,1,0);
                var s=ShortRestCapture(session);var epoch=s.Reinforcement.Admission.Phase.Epoch;var duration=new RuleTime(30,TestOnlyClubAttackPolicy.WalkingSpeed(s,hero));
                var earliest=new RuleTime(s.RuleClock.Numerator*duration.Denominator+duration.Numerator*s.RuleClock.Denominator,s.RuleClock.Denominator*duration.Denominator);
                long slot=epoch.SlotAt(s.RuleClock);
                while(epoch.Order[(int)(slot%epoch.Order.Count)]!=PostRecoveryEncounterDefinition.PriorDefender||epoch.Start(slot)<earliest
                    ||epoch.LatestStart(cleric,slot)<0||epoch.Start(epoch.LatestStart(cleric,slot))<s.RuleClock)slot++;
                var arrival=epoch.Start(slot);var ownStart=epoch.Start(epoch.LatestStart(cleric,slot));
                var departure=new RuleTime(arrival.Numerator*duration.Denominator-duration.Numerator*arrival.Denominator,arrival.Denominator*duration.Denominator);
                if(ownStart<=departure){PostRecoveryAdvanceTo(session,ownStart);Invoke("bishop.recharge.before-contact");PostRecoveryAdvanceTo(session,departure);ClericCommit(session,hero,CommandKind.BeginWorldStep,"walk",0,1);}
                else {PostRecoveryAdvanceTo(session,departure);ClericCommit(session,hero,CommandKind.BeginWorldStep,"walk",0,1);PostRecoveryAdvanceTo(session,ownStart);Invoke("bishop.recharge.before-contact");}
                Require(Remaining()==3,"Invocation paid before contact lost its initial counter.");BishopCheckpoint(session,directory,"approach-recharge3");
                PostRecoveryAdvanceTo(session,arrival);var entered=ShortRestCapture(session);Require(entered.InventoryCombat,"Paid contact failed after actual Invocation.");
                var admitted=entered.PostRecoveryEncounter.Admission.Epoch;int starts=admitted.Order[0]==cleric?1:0;
                Require(Remaining()==3-starts,"Admission or old calendar double-ticked recharge.");BishopCheckpoint(session,directory,"entered-with-recharge");
                while(starts<3){
                    var current=ShortRestCapture(session);var actor=current.Encounter.CurrentActor;
                    BishopCommit(session,new Command("bishop.recharge.stance."+current.Revision,actor,current.Revision,CommandKind.SelectCombatStance,
                        combat:new CombatRequest(current.Encounter.CurrentTurnId,stance:1)));
                    current=ShortRestCapture(session);
                    BishopCommit(session,new Command("bishop.recharge.end."+current.Revision,actor,current.Revision,CommandKind.EndRegularTurn,current.Encounter.CurrentTurnId));
                    if(ShortRestCapture(session).Encounter.CurrentActor==cleric)starts++;
                    Require(Remaining()==3-starts,"Only actual new-epoch owner Starts may tick recharge.");
                }
                var final=ShortRestCapture(session);Require(final.ResonancePools.Single().Current==1&&final.ConvictionBalance.Current==1,"Cross-epoch recharge refilled paid balances.");
                BishopCheckpoint(session,directory,"new-epoch-ready");
            });
            cases.Add("chr03_bishop_connected_earned_funded_cure_aura_dispel_continue",()=>RunBishopTypedCampaign(directory));
            cases.Add("chr03_bishop_request_cardinality_and_old_profile_denial",()=>{
                const string h=ConnectedExpeditionSession.Hero,a=ClericRpProfile.Actor;
                foreach(var targets in new[]{Array.Empty<string>(),new[]{h,h},new[]{h,a,"TEST_ONLY.third","TEST_ONLY.fourth"}})
                    Throws<ArgumentException>(()=>new DivineInvocationRequest(targets));
                Throws<ArgumentException>(()=>new DivineInvocationRequest(new[]{h},a,RadianceCurePreference.Frightened));
                Throws<ArgumentException>(()=>new DivineInvocationRequest(new[]{h},h,RadianceCurePreference.None));
                var session=NewPostRecoveryExpedition();var sim=BishopSimulation(session);var authority=new Authority("TEST_ONLY.host",new[]{h,a},inventoryOwners:new[]{h,a});
                var command=new Command("bishop.old.denial",a,0,CommandKind.UseDivineInvocation,divineInvocation:new DivineInvocationRequest(new[]{h}));
                var before=new SnapshotCodec().Encode(ShortRestCapture(session));var query=sim.QueryCommand(authority,command);var result=sim.Execute(authority,command);
                Require(!query.Supported&&query.Code=="UnsupportedOperation"&&result.Outcome==Outcome.Rejected&&result.Code=="InvocationUnsupported"
                    &&before.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Old profile admitted the new capability or changed state.");
                File.WriteAllText(Path.Combine(directory,"old-profile-denial.json"),System.Text.Json.JsonSerializer.Serialize(new{query,result}));
                Require(new DivineInvocationRequest(new[]{a,h}).TargetIds.SequenceEqual(new[]{h,a}),"Recipient order is not deterministic.");
            });
            cases.Add("chr03_bishop_announced_genesis_and_unearned_denial",()=>{
                var session=NewBishopExpedition();var s=ShortRestCapture(session);
                Require(s.BishopEntry!=null&&!BishopProfile.Earned(s)&&s.BishopEntry.Departure==null&&s.CharacterAdvancements.Length==0,
                    "Bishop genesis backfilled an earned grant.");BishopCheckpoint(session,directory,"genesis");
                var authority=new Authority("TEST_ONLY.host",new[]{ClericRpProfile.Actor,ConnectedExpeditionSession.Hero});
                RetainClericDenial(BishopSimulation(session),authority,new Command("bishop.unearned",ClericRpProfile.Actor,0,CommandKind.UseDivineInvocation,
                    divineInvocation:new DivineInvocationRequest(new[]{ClericRpProfile.Actor})),"DivineInvocationNotOwned",directory);
            });
        }
    }
}
#endif
