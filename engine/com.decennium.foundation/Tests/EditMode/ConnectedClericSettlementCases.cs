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
        private static ConnectedExpeditionSession NewClericSettlement() => ConnectedExpeditionSession.StartWithClericSettlement(
            ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),ClericMilestoneDeclaration.AuthoredExample());

        private static CharacterAdvancementRequest ClericEarnedChoices() => new CharacterAdvancementRequest(
            ClericSettlementProfile.SelectedCards.ToArray(),ClericSettlementProfile.Radiance,ClericRepertoireProfile.FutureChoice);

        private sealed class RejectAfterClericSettlement : ICommandPolicy
        {
            private readonly TestOnlySharedWorldPolicy inner;
            internal RejectAfterClericSettlement(TestOnlySharedWorldPolicy policy){inner=policy;}
            public string ContentFingerprint=>inner.ContentFingerprint;
            public bool TestOnly=>true;
            public Snapshot Initial()=>inner.Initial();
            public string ValidateState(Snapshot s)=>inner.ValidateState(s);
            public string Resolve(Snapshot candidate,Command command)
            {
                string failure=inner.Resolve(candidate,command);
                return failure==null && command.Kind==CommandKind.AdvanceCharacterLevel ? "InjectedAfterClericSettlement" : failure;
            }
        }

        private static void RetainClericDenial(Simulation simulation,Authority authority,Command command,string expected,string directory)
        {
            var before=Bytes(simulation);var query=simulation.QueryCommand(authority,command);var result=simulation.Execute(authority,command);
            var after=Bytes(simulation);
            File.WriteAllBytes(Path.Combine(directory,command.Id+"-before.ddsave"),before);
            File.WriteAllBytes(Path.Combine(directory,command.Id+"-after.ddsave"),after);
            File.WriteAllText(Path.Combine(directory,command.Id+"-denial.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Actual simulation command and query; canonical before/after snapshots",command,expected,
                queryCode=query.Code,resultCode=result.Code,outcome=result.Outcome.ToString()}));
            Require(!query.Admissible && query.Code==expected && result.Outcome==Outcome.Rejected && result.Code==expected
                && before.SequenceEqual(after),"Actual Cleric denial disagreed with its query or changed canonical state: "+expected);
        }

        private static ConnectedExpeditionSession EarnClericObjective(bool spendRite,string directory=null,
            ConnectedExpeditionSession selected=null,Action<ConnectedExpeditionSession> firstClericAction=null,
            Action<ConnectedExpeditionSession> beforeClosure=null,Func<int,int> heroStance=null,
            Action<ConnectedExpeditionSession> beforeInitialRite=null)
        {
            var session = StartVialScenario(selected??NewClericSettlement());
            const string routeHero = ConnectedExpeditionSession.Hero, routeAlly = ClericRpProfile.Actor;
            ClericCommit(session,routeAlly,CommandKind.BeginWorldStep,"walk",-1);
            ClericCommit(session,routeHero,CommandKind.AdvanceClock,x:6,y:1);
            ClericCommit(session,routeHero,CommandKind.BeginWorldStep,"walk",-1);
            ClericCommit(session,routeHero,CommandKind.AdvanceClock,x:12,y:1);
            ClericCommit(session,routeAlly,CommandKind.BeginReinforcementApproach,"TEST_ONLY.companion-reinforcement.v1");
            ClericGuard(session,routeHero);ClericCommit(session,routeHero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:2);
            ClericDefender(session);ClericEnd(session,routeHero);ClericDefender(session);
            ClericGuard(session,routeAlly);firstClericAction?.Invoke(session);ClericEnd(session,routeAlly);ClericGuard(session,routeHero);
            ClericCommit(session,routeHero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:1);
            ClericDefender(session);ClericEnd(session,routeHero);ClericDefender(session);
            // The composed Frightened defender spends its first available Action on Presence.
            // Two further genuine rounds produce the retained 1HP injury; no damage or RNG is injected.
            for(int round=0;round<2;round++) {
                ClericGuard(session,routeAlly);ClericEnd(session,routeAlly);ClericGuard(session,routeHero);
                ClericEnd(session,routeHero);ClericDefender(session);
            }
            Require(ShortRestCapture(session).Lives.Single(x=>x.ActorId==routeAlly).Hp==7,"Real defender attack must supply the selected injury.");
            const string hero = ConnectedExpeditionSession.Hero, ally = ClericRpProfile.Actor;
            ClericGuard(session,ally);
            beforeInitialRite?.Invoke(session);
            if(directory!=null)session.Save(Path.Combine(directory,"cleric-before-initial-rite.ddsave"));
            if (spendRite) {
                ClericCommit(session,ally,CommandKind.UseHealingRite,ally);
                if(directory!=null)session.Save(Path.Combine(directory,"cleric-after-initial-rite.ddsave"));
            }
            ClericEnd(session,ally); ClericGuard(session,hero);
            ClericCommit(session,hero,CommandKind.TacticalStep,session.View(ExpeditionSeat.Player).TurnId,y:2);
            ClericEnd(session,hero); ClericDefender(session); ClericGuard(session,ally); ClericEnd(session,ally);
            for (int round=0;;round++) {
                Require(round < 24,"Earned Cleric route failed to conclude genuine combat.");
                if(heroStance==null)ClericGuard(session,hero);
                else ClericCommit(session,hero,CommandKind.SelectCombatStance,
                    combat:new CombatRequest(session.View(ExpeditionSeat.Player).TurnId,stance:heroStance(round)));
                if (ShortRestCapture(session).Lives.Single(x => x.ActorId == FrightenedProfile.Actor).Dead) break;
                ClericCommit(session,hero,CommandKind.AttackClub,FrightenedProfile.Actor,
                    combat:new CombatRequest(session.View(ExpeditionSeat.Player).TurnId,"TEST_ONLY.actor-club"));
                ClericEnd(session,hero); ClericDefender(session); ClericGuard(session,ally); ClericEnd(session,ally);
            }
            if(directory!=null)session.Save(Path.Combine(directory,"cleric-before-objective.ddsave"));
            beforeClosure?.Invoke(session);
            ClericCommit(session,hero,CommandKind.EndFixedEncounter,session.View(ExpeditionSeat.Player).TurnId);
            Require(ShortRestCapture(session).ClericObjective != null,"Actual two-conflict/batch closure must earn the declared objective.");
            return session;
        }

        private static void AwardAndAdvanceCleric(ConnectedExpeditionSession session, string directory)
        {
            var codec = new SnapshotCodec(); var before = ShortRestCapture(session);
            const string ally = ClericRpProfile.Actor;
            Require(before.CharacterMilestones.Length == 0 && before.CharacterAdvancements.Length == 0
                && before.Characters.Single(x => x.ActorId == ally).Levels.Count == 1,"Objective completion must not award or advance automatically.");
            string path=Path.Combine(directory,"cleric-objective.ddsave"); session.Save(path); session.Restore(path);
            CommitVialRoute(session,new Command("chr03.award",ally,before.Revision,CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId));
            var awarded = ShortRestCapture(session);
            Require(awarded.CharacterMilestones.Single().ConsumedRevision == 0,"Trusted award must remain a separate unconsumed entitlement.");
            path=Path.Combine(directory,"cleric-awarded.ddsave"); session.Save(path); session.Restore(path);
            var simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
            var authority=new Authority("TEST_ONLY.host",new[]{ConnectedExpeditionSession.Hero,ally},canModifyWorld:true,
                inventoryOwners:new[]{ConnectedExpeditionSession.Hero,ally});
            var invalid=new[]{
                new CharacterAdvancementRequest(new[]{ClericSettlementProfile.ConvictionPool},ClericSettlementProfile.Radiance,"detect-magic"),
                new CharacterAdvancementRequest(new[]{ClericSettlementProfile.ConvictionPool,ClericSettlementProfile.ConvictionPool},ClericSettlementProfile.Radiance,"detect-magic"),
                new CharacterAdvancementRequest(new[]{ClericSettlementProfile.ConvictionPool,ClericSettlementProfile.Attunement},ClericSettlementProfile.Radiance,"detect-magic"),
                new CharacterAdvancementRequest(ClericSettlementProfile.SelectedCards.ToArray(),ClericRpProfile.HealingRite,"detect-magic"),
                new CharacterAdvancementRequest(ClericSettlementProfile.SelectedCards.ToArray(),ClericSettlementProfile.Radiance,"arcane-ward"),
                new CharacterAdvancementRequest(ClericSettlementProfile.SelectedCards.ToArray(),ClericSettlementProfile.Radiance,"dispel-magic-lesser"),
                new CharacterAdvancementRequest(ClericSettlementProfile.SelectedCards.ToArray(),"","")};
            for(int i=0;i<invalid.Length;i++)RetainClericDenial(simulation,authority,new Command("chr03.invalid-choice."+i,ally,
                awarded.Revision,CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:invalid[i]),
                "ClericSettlementChoiceUnsupported",directory);
            RetainClericDenial(simulation,authority,new Command("chr03.second-award",ally,awarded.Revision,CommandKind.AwardCharacterMilestone,
                ClericMilestoneDeclaration.FixedId),"MilestoneAlreadyAwarded",directory);
            var command = new Command("chr03.advance",ally,awarded.Revision,CommandKind.AdvanceCharacterLevel,
                ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices());
            RetainClericDenial(simulation,authority,new Command("chr03.stale-advance",ally,awarded.Revision-1,
                CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()),"StaleRevision",directory);
            RetainClericDenial(simulation,authority,new Command("chr03.award",ally,awarded.Revision,
                CommandKind.AdvanceCharacterLevel,ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()),"CommandIdConflict",directory);
            var preview=simulation.QueryCommand(authority,command);
            Require(preview.Admissible && codec.Encode(awarded).SequenceEqual(Bytes(simulation)),"Advancement query changed the earned predecessor.");
            var preflight=typeof(TestOnlySharedWorldPolicy).GetMethod("AssessClericAdvancement",BindingFlags.Instance|BindingFlags.NonPublic);
            var controls=new List<object>();
            void DetachedPreflight(string name,string expected,Action<Snapshot> setup) {
                var candidate=awarded.Copy();setup(candidate);string prior=ClericRaw(candidate);
                var code=(string)preflight.Invoke(ClericPolicy(session),new object[]{candidate,command});
                Require(code==expected && prior==ClericRaw(candidate),"Detached common assessment failed: "+name);
                controls.Add(new{name,expected,code,unchanged=true});
            }
            DetachedPreflight("tactical","TacticalControlActive",s=>s.InventoryCombat=true);
            DetachedPreflight("traversal","CharacterBusy",s=>s.WorldTraversals=new[]{new WorldTraversalRecord(ally,s.Revision,0,0,1,0)});
            DetachedPreflight("pending-ready","TacticalChoicePending",s=>s.ReadyOccurrences=new[]{new ReadyOccurrenceRecord(
                "detached.ready","detached.source","detached.move",ally,ConnectedExpeditionSession.Hero,0,0,s.Revision,s.Revision)});
            DetachedPreflight("pending-advance","ManufacturingChoicePending",s=>s.ManufacturingAdvance=new ManufacturingAdvanceRecord(
                s.RuleClock.AddSeconds(6),false,"detached.advance",s.Revision,""));
            DetachedPreflight("wrong-class","UnsupportedAdvancementPath",s=>s.Characters=s.Characters.Select(x=>x.ActorId!=ally?x:
                new ActorCharacterRecord(ally,x.ProfileId,x.Abilities,new[]{new CharacterLevelFact("Soldier",8)})).ToArray());
            DetachedPreflight("missing-old-die","HitDieLedgerMismatch",s=>s.CharacterHitDice=s.CharacterHitDice.Where(x=>x.ActorId!=ally).ToArray());
            DetachedPreflight("unearned","MilestoneNotAvailable",s=>s.CharacterMilestones=Array.Empty<CharacterMilestoneRecord>());
            File.WriteAllText(Path.Combine(directory,"detached-advancement-preflight.json"),System.Text.Json.JsonSerializer.Serialize(new{
                scope="Detached mechanical states exercising the actual shared query/execute assessment; not reachable campaign saves",controls}));
            var faulted=new Simulation(new RejectAfterClericSettlement(ClericPolicy(session)),awarded,ExecutionProfile.Laboratory);
            var rollbackBefore=Bytes(faulted);
            RejectUnchanged(faulted,authority,command,"InjectedAfterClericSettlement");
            File.WriteAllBytes(Path.Combine(directory,"chr03.injected-rollback-before.ddsave"),rollbackBefore);
            File.WriteAllBytes(Path.Combine(directory,"chr03.injected-rollback-after.ddsave"),Bytes(faulted));
            // Detached state preservation control: real advancement on an unavailable old
            // Hit Die and Stable zero-HP injury state, without claiming a reachable save.
            var detached=awarded.Copy();var oldLife=detached.Lives.Single(x=>x.ActorId==ally);
            detached.CharacterHitDice=detached.CharacterHitDice.Select(x=>x.ActorId==ally
                ?new CharacterHitDieRecord(x.ActorId,x.LevelOrdinal,x.ClassName,x.DieSize,true):x).ToArray();
            var stableUntil=detached.RuleClock.AddSeconds(900);
            detached.Lives=detached.Lives.Select(x=>x.ActorId!=ally?x:new ActorLifeRecord(ally,8,0,3,new[]{(int)Injury.Concussion},
                true,false,true,0,0,stableUntil,oldLife.LastDeathTurn,true,oldLife.HeldItems)).ToArray();
            Require(ClericPolicy(session).Resolve(detached,command)==null,"Detached existing-life advancement was denied.");
            var preserved=detached.Lives.Single(x=>x.ActorId==ally);
            Require(preserved.MaximumHp==13 && preserved.Hp==0 && preserved.Stable && !preserved.Dead && preserved.StableUntil==stableUntil
                && preserved.TemporaryHp==3 && preserved.LinkedInjuries.SequenceEqual(new[]{(int)Injury.Concussion}) && preserved.Prone
                && detached.CharacterHitDice.Single(x=>x.ActorId==ally&&x.LevelOrdinal==1).Spent
                && !detached.CharacterHitDice.Single(x=>x.ActorId==ally&&x.LevelOrdinal==2).Spent,
                "Advancement healed, recovered an old die or reset independent life facts.");
            var wrongSource=awarded.Copy();var firstSpell=wrongSource.KnownSpells[0];
            wrongSource.KnownSpells=wrongSource.KnownSpells.Select(x=>x!=firstSpell?x:KnownSpellRecord.FromSource(ally,x.SpellId,
                SpellAcquisitionOrigin.InitialClassRepertoire,1,1,"TEST_ONLY.wrong-entitlement")).ToArray();
            string sourceBefore=ClericRaw(wrongSource);
            Require(ClericPolicy(session).Resolve(wrongSource,command)=="ClericEarnedRepertoireChoiceUnavailable" && sourceBefore==ClericRaw(wrongSource),
                "Wrong initial source provenance escaped common preflight or partly advanced the character.");
            CommitVialRoute(session,command); var advanced=ShortRestCapture(session);
            Require(advanced.Lives.Single(x => x.ActorId == ally).MaximumHp == 13
                && advanced.Lives.Single(x => x.ActorId == ally).Hp == before.Lives.Single(x => x.ActorId == ally).Hp
                && advanced.ResonancePools.Single().Maximum == 4 && advanced.ResonancePools.Single().Current == before.ResonancePools.Single().Current
                && advanced.ConvictionCapacity.Maximum == 5 && !advanced.ConvictionCapacity.CurrentAvailable && advanced.ConvictionCapacity.Current == null
                && advanced.CharacterHitDice.Count(x => x.ActorId == ally && x.DieSize == 8) == 2
                && advanced.CharacterFeatureGrants.Count(x => ClericSettlementProfile.ValidEarnedGrant(advanced,x)) == 4
                && advanced.KnownSpells.Length == 6 && advanced.KnownSpells.Count(x => x.Origin == SpellAcquisitionOrigin.EarnedClassLevel) == 1
                && System.Text.Json.JsonSerializer.Serialize(before.KnownSpells)==System.Text.Json.JsonSerializer.Serialize(
                    advanced.KnownSpells.Where(x=>x.Origin==SpellAcquisitionOrigin.InitialClassRepertoire).ToArray())
                && advanced.RuleClock == before.RuleClock && advanced.RandomState == before.RandomState
                && advanced.ResonancePools.Single().InitialFunding.Id == before.ResonancePools.Single().InitialFunding.Id,
                "Earned settlement changed funding, current health/resources, chronology, choices, RNG or time.");
            var bytes=codec.Encode(advanced);path=Path.Combine(directory,"cleric-advanced.ddsave");session.Save(path);session.Restore(path);
            Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Earned settlement failed strict restore.");
            var forgeries=new List<object>();
            void Forgery(string name,Action<Snapshot> alter) {
                var candidate=advanced.Copy();alter(candidate);string prior=ClericRaw(candidate);
                string code=ClericPolicy(session).ValidateState(candidate);
                Require(code!=null && prior==ClericRaw(candidate),"Forged connected settlement passed or repaired: "+name);
                forgeries.Add(new{name,code,unchanged=true});
            }
            Forgery("missing-objective",s=>s.ClericObjective=null);
            Forgery("unconsumed-entitlement",s=>s.CharacterMilestones=new[]{new CharacterMilestoneRecord(
                ClericMilestoneDeclaration.FixedId,ally,awarded.Revision)});
            Forgery("missing-earned-grants",s=>s.CharacterFeatureGrants=s.CharacterFeatureGrants.Where(x=>x.GrantedRevision==0).ToArray());
            Forgery("missing-path",s=>s.ClericInvocationPath=null);
            Forgery("initial-capacity-after-advancement",s=>s.ConvictionCapacity=new ConvictionCapacityRecord(ally,ClericRpProfile.SourceRevision,"",0));
            Forgery("missing-earned-spell",s=>s.KnownSpells=s.KnownSpells.Where(x=>x.Origin==SpellAcquisitionOrigin.InitialClassRepertoire).ToArray());
            Forgery("old-envelope-with-new-ledgers",s=>s.ConnectedClericSettlement=false);
            File.WriteAllText(Path.Combine(directory,"connected-settlement-forgeries.json"),System.Text.Json.JsonSerializer.Serialize(forgeries));
            Require(session.Submit(ExpeditionSeat.Player,command).Response == ExpeditionResponse.Duplicate
                && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Earned advancement retry changed state.");
            File.WriteAllBytes(Path.Combine(directory,"chr03.advance-retry-before.ddsave"),bytes);
            File.WriteAllBytes(Path.Combine(directory,"chr03.advance-retry-after.ddsave"),codec.Encode(ShortRestCapture(session)));
            simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
            RetainClericDenial(simulation,authority,new Command("chr03.second-consumption",ally,advanced.Revision,CommandKind.AdvanceCharacterLevel,
                ClericMilestoneDeclaration.FixedId,advancement:ClericEarnedChoices()),"MilestoneAlreadyConsumed",directory);
            if (!advanced.ConnectedClericCasting) RetainClericDenial(simulation,authority,new Command("chr03.casting-unsupported",ally,advanced.Revision,CommandKind.CastKnownSpell,"detect-magic"),
                "OrdinarySpellcastingUnsupported",directory);
            RetainClericDenial(simulation,authority,new Command("chr03.independent-acquisition",ally,advanced.Revision,CommandKind.AcquireEarnedSpell,"detect-magic"),
                "EarnedSpellAcquisitionRequiresAdvancementTransaction",directory);
        }

        private static void ReachClericOwnSlot(ConnectedExpeditionSession session)
        {
            for(int step=0;step<3;step++) {
                var state=ShortRestCapture(session);var epoch=WorldTiming.ForActor(state,ClericRpProfile.Actor);
                if(epoch.Order[(int)(epoch.ProcessedSlot%epoch.Order.Count)]==ClericRpProfile.Actor)return;
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:2,y:1);
            }
            throw new Exception("Ordinary clock advancement did not reach the retained Cleric slot.");
        }

        private static void AddConnectedClericSettlementCases(Dictionary<string,Action> cases,string directory)
        {
            cases.Add("chr03_typed_choices_receipts_and_legacy_automatic_origin",() => {
                var features=ClericSettlementProfile.SelectedCards.ToArray();
                var request=new CharacterAdvancementRequest(features,ClericSettlementProfile.Radiance,ClericRepertoireProfile.FutureChoice);
                features[0]="changed";
                Require(ClericSettlementProfile.ValidChoices(request),"Earned choices retained mutable caller storage.");
                Throws<NotSupportedException>(()=>((IList<string>)request.FeatureIds)[0]="changed");
                var receipt=new CommandReceipt { Id="advance",Principal="TEST_ONLY.host",Revision=1,
                    Fingerprint=((int)CommandKind.AdvanceCharacterLevel).ToString(System.Globalization.CultureInfo.InvariantCulture)
                        +"|"+ClericRpProfile.Actor+"|"+ClericMilestoneDeclaration.FixedId+"|0|0|0|character-level-v4|"
                        +string.Join(",",ClericSettlementProfile.SelectedCards)+"|"+ClericSettlementProfile.Radiance+"|detect-magic" };
                Require(ClericSettlementProfile.ValidChoices(CommandHistory.Read(receipt).Advancement),"Earned receipt lost exact source choices.");
                foreach(var choice in new[]{RadianceCurePreference.None,RadianceCurePreference.Frightened,RadianceCurePreference.Poisoned}) {
                    var rite=receipt.Copy();rite.Fingerprint=((int)CommandKind.UseHealingRite).ToString(System.Globalization.CultureInfo.InvariantCulture)
                        +"|"+ClericRpProfile.Actor+"|"+ConnectedExpeditionSession.Hero+"|0|0|0|healing-rite-v1|"
                        +((int)choice).ToString(System.Globalization.CultureInfo.InvariantCulture);
                    Require(CommandHistory.Read(rite).HealingRite.CurePreference==choice,"Conditional cure choice changed on receipt reconstruction.");
                }
                Throws<ArgumentException>(()=>new HealingRiteRequest((RadianceCurePreference)3));
                Require((int)CharacterFeatureGrantOrigin.TestOnlyFixtureEntitlement==3
                    && (int)CharacterFeatureGrantOrigin.EarnedAutomaticClassFeature==4,"Historical feature-origin ordinals changed.");
                Throws<ArgumentException>(()=>new CharacterFeatureGrantRecord(ClericRpProfile.Actor,ClericSettlementProfile.Attunement,
                    "Cleric",2,ClericMilestoneDeclaration.FixedId,1,CharacterFeatureGrantOrigin.AutomaticClassFeature));
                Throws<ArgumentException>(()=>new CharacterFeatureGrantRecord(ClericRpProfile.Actor,ClericSettlementProfile.Attunement,
                    "Cleric",2,"",0,CharacterFeatureGrantOrigin.EarnedAutomaticClassFeature));
            });
            cases.Add("chr03_initial_declaration_capacity_and_wire_isolation",() => {
                var session=NewClericSettlement();var state=ShortRestCapture(session);var codec=new SnapshotCodec();
                Require(state.WireSchemaVersion == 108 && state.SchemaVersion == 90 && state.ConnectedFrightened
                    && state.ClericMilestone.DeclaredRevision == 0 && state.ClericObjective == null && state.ClericInvocationPath == null
                    && state.ConvictionCapacity.Maximum == 3 && !state.ConvictionCapacity.Current.HasValue
                    && state.KnownSpells.Length == 5 && state.ResonancePools.Single().Current == 3,"Initial declaration manufactured earned benefits.");
                var bytes=codec.Encode(state);Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Wire108 did not round-trip canonically.");
                string path=Path.Combine(directory,"chr03-initial.ddsave");session.Save(path);session.Restore(path);
                Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Initial strict replay changed the declaration.");
                var old=ShortRestCapture(NewFrightenedExpedition());var oldBytes=codec.Encode(old);
                Require(old.WireSchemaVersion == 107 && old.ClericMilestone == null && old.ConvictionCapacity == null
                    && oldBytes.SequenceEqual(codec.Encode(codec.Decode(oldBytes))),"Wire107 was backfilled.");
                old.ConvictionCapacity=state.ConvictionCapacity;Throws<ArgumentException>(()=>codec.Encode(old));
                Throws<ArgumentNullException>(()=>ConnectedExpeditionSession.StartWithClericSettlement(
                    ClericInitialSelection.AuthoredExample(),ClericRepertoireSelection.AuthoredExample(),null));
            });
            cases.Add("chr03_early_award_authority_and_payload_rollback",() => {
                var session=NewClericSettlement();var state=ShortRestCapture(session);var policy=ClericPolicy(session);
                var simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
                var command=new Command("chr03.early",ClericRpProfile.Actor,0,CommandKind.AwardCharacterMilestone,ClericMilestoneDeclaration.FixedId);
                var restricted=new Authority("TEST_ONLY.host",new[]{ClericRpProfile.Actor});
                RejectUnchanged(simulation,restricted,command,"NotAuthorized");
                RejectUnchanged(simulation,new Authority("TEST_ONLY.host",new[]{ClericRpProfile.Actor},canModifyWorld:true),command,"MilestoneObjectiveIncomplete");
                var choice=new Command("chr03.consent",ClericRpProfile.Actor,0,CommandKind.UseHealingRite,ConnectedExpeditionSession.Hero,
                    healingRite:new HealingRiteRequest(RadianceCurePreference.Poisoned));
                RejectUnchanged(simulation,restricted,choice,"NotAuthorized");
                Require(!simulation.QueryCommand(restricted,choice).Admissible,"Query bypassed current recipient authority.");
                var forged=state.Copy();forged.ConvictionCapacity=new ConvictionCapacityRecord(ClericRpProfile.Actor,
                    ClericRpProfile.SourceRevision,ClericMilestoneDeclaration.FixedId,1);
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(forged));
                Require(policy.ValidateState(forged)!=null,"Forged passive capacity passed strict replay.");
            });
            cases.Add("chr03_primary_genuine_earned_settlement",() => {
                var session=EarnClericObjective(true,directory);var state=ShortRestCapture(session);
                Require(state.Lives.Single(x=>x.ActorId==ClericRpProfile.Actor).Hp==8 && state.ResonancePools.Single().Current==1,
                    "Primary genuine route must reach its actual 8HP/1RP witness.");
                AwardAndAdvanceCleric(session,directory);
                ReachClericOwnSlot(session);
                var ready=ShortRestCapture(session);var bytes=new SnapshotCodec().Encode(ready);
                var command=new Command("chr03.insufficient",ClericRpProfile.Actor,ready.Revision,CommandKind.UseHealingRite,ClericRpProfile.Actor);
                var simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
                RetainClericDenial(simulation,new Authority("TEST_ONLY.host",new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor},
                    inventoryOwners:new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor}),command,"InsufficientResonance",directory);
                Require(ClericPolicy(session).Resolve(ready.Copy(),command)=="InsufficientResonance"
                    && session.Submit(ExpeditionSeat.Player,command).Response==ExpeditionResponse.Unavailable
                    && bytes.SequenceEqual(new SnapshotCodec().Encode(ShortRestCapture(session))),"Earned capacity manufactured spending power.");
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.BeginWorldStep,"walk",y:-1);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                string path=Path.Combine(directory,"cleric-primary-continued.ddsave");session.Save(path);session.Restore(path);
            });
            cases.Add("chr03_alternate_genuine_paid_radiance_and_continuation",() => {
                var session=EarnClericObjective(false,directory);var state=ShortRestCapture(session);var codec=new SnapshotCodec();
                Require(state.ResonancePools.Single().Current==3 && state.HealingRites.Length==0
                    && state.Lives.Single(x=>x.ActorId==ConnectedExpeditionSession.Hero).Hp==9,
                    "Alternate genuine combat must retain its actual injury and original RP3.");
                AwardAndAdvanceCleric(session,directory);ReachClericOwnSlot(session);
                var before=ShortRestCapture(session);string path=Path.Combine(directory,"cleric-before-radiance.ddsave");
                session.Save(path);session.Restore(path);
                var command=new Command("chr03.actual-radiance",ClericRpProfile.Actor,before.Revision,CommandKind.UseHealingRite,ConnectedExpeditionSession.Hero,
                    healingRite:new HealingRiteRequest(RadianceCurePreference.Poisoned));
                AssertPureUtility(session,command);
                var activeSimulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
                var casterAuthority=new Authority("TEST_ONLY.host",new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor},
                    inventoryOwners:new[]{ConnectedExpeditionSession.Hero,ClericRpProfile.Actor});
                Require(activeSimulation.QueryCommand(casterAuthority,command).Admissible
                    && codec.Encode(before).SequenceEqual(Bytes(activeSimulation)),"Actual paid Rite query changed state or denied a supported command.");
                CommitVialRoute(session,command);var after=ShortRestCapture(session);var use=after.RadianceUses.Single();var rite=after.HealingRites.Single();
                var epoch=WorldTiming.ForActor(before,ClericRpProfile.Actor);var draw=DiceStream.Draw(before.RandomState,8);
                Require(rite.ActualGain>0 && use.AdditionalGain==1 && use.BaseHpAfter==rite.HpAfter && use.HpAfter==rite.HpAfter+1
                    && after.ResonancePools.Single().Current==1 && after.ResonancePools.Single().Maximum==4
                    && after.RandomState==draw.NextState && rite.Die==draw.Value+1 && before.RuleClock==after.RuleClock
                    && use.EpochId==epoch.Id && use.LocalStart==epoch.ProcessedSlot
                    && use.GlobalStart==before.Reinforcement.Admission.Phase.GlobalTurn(use.LocalStart)
                    && use.EndedApplicationIds.Count==0 && use.CureOperationId==""
                    && before.Conditions.Zip(after.Conditions,(a,b)=>a.SameAs(b)).All(x=>x),
                    "Actual paid Radiance failed shared payment/healing, one-draw RNG, owned calendar or no-empty-cure semantics.");
                path=Path.Combine(directory,"cleric-after-radiance.ddsave");session.Save(path);session.Restore(path);
                var bytes=codec.Encode(after);Require(bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Radiance strict restore changed its effects.");
                Require(session.Submit(ExpeditionSeat.Player,command).Response==ExpeditionResponse.Duplicate
                    && bytes.SequenceEqual(codec.Encode(ShortRestCapture(session))),"Radiance retry repeated payment or healing.");
                File.WriteAllBytes(Path.Combine(directory,"chr03.radiance-retry-before.ddsave"),bytes);
                File.WriteAllBytes(Path.Combine(directory,"chr03.radiance-retry-after.ddsave"),codec.Encode(ShortRestCapture(session)));
                var simulation=(Simulation)typeof(ConnectedExpeditionSession).GetField("simulation",BindingFlags.Instance|BindingFlags.NonPublic).GetValue(session);
                var revokedRecipient=new Authority("TEST_ONLY.host",new[]{ClericRpProfile.Actor},inventoryOwners:new[]{ClericRpProfile.Actor});
                RetainClericDenial(simulation,revokedRecipient,command,"NotAuthorized",directory);
                Require(!simulation.QueryCommand(revokedRecipient,command).Admissible,"Duplicate cure query skipped current recipient authority.");
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.BeginWorldStep,"walk",y:-1);
                ClericCommit(session,ConnectedExpeditionSession.Hero,CommandKind.AdvanceClock,x:6,y:1);
                path=Path.Combine(directory,"cleric-alternate-continued.ddsave");session.Save(path);session.Restore(path);
            });
        }
    }
}
#endif
