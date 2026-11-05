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
        private static TestOnlySharedWorldPolicy ResolvedPolicy(uint seed=1)
            =>new TestOnlySharedWorldPolicy(TestOnlyContentManifest.CreateSelectedProfile(),new PortableKitFixture(),new SharedCombatFixture(seed:seed),
                new SharedResearchFixture(),new SharedCraftingFixture(),new SharedRepairFixture(),new SharedManufacturingFixture(),new SupplyCacheFixture());

        private static void AddContentResolutionCases(Dictionary<string,Action> cases,string directory)
        {
            var host=TestOnlySharedWorldPolicy.Host();
            cases.Add("content_manifest_recipe14_is_versioned_without_rebinding_legacy_profile",()=>{
                var manifest=TestOnlyContentManifest.CreateManufacturingExpansionProfile();
                var legacy=TestOnlyContentManifest.CreateSelectedProfile();
                Require(manifest.ValidateBindings()==null&&manifest.IsTrustedBuildMetadata&&manifest.Digest==TestOnlyContentManifest.Recipe14TrustedDigest
                    &&legacy.ValidateBindings()==null&&legacy.IsTrustedBuildMetadata&&legacy.Digest==TestOnlyContentManifest.TrustedDigest,
                    "Recipe-14 content was not separately pinned or changed the legacy manifest.");
                Require(manifest.ResolveSemantic("crafting","recipe-14").JsonPointer=="/cards/13"
                    &&manifest.ResolveSemantic("crafting-component","recipe-14.ing-14-0-stabilizing_salts").JsonPointer=="/cards/13/sourceRequirements/components/0"
                    &&manifest.ResolveSemantic("recipe-result","recipe-14").JsonPointer=="/cards/13/operational"
                    &&manifest.Supports(manifest.ResolveSemantic("crafting","recipe-14"),ContentOperation.Manufacture)
                    &&!legacy.Entries.Any(x=>x.Domain=="crafting"&&x.SemanticId=="recipe-14"),
                    "Recipe-14 source rows, operation binding or legacy profile boundary drifted.");
            });
            cases.Add("content_manifest_binds_source_identity_visibility_and_legacy_profile_separately",()=>{
                var manifest=TestOnlyContentManifest.CreateSelectedProfile();var resolved=ResolvedPolicy();
                var legacy=PortablePolicy();var sameManifestProfile=new TestOnlySharedWorldPolicy(manifest,new PortableKitFixture(),new SharedCombatFixture(),new SupplyCacheFixture());
                var state=resolved.Initial();
                Require(manifest.ValidateBindings()==null&&manifest.IsTrustedBuildMetadata&&state.SchemaVersion==Snapshot.PortableEquipmentSchema
                    &&sameManifestProfile.ContentFingerprint!=legacy.ContentFingerprint,"Manifest was not added to its selected profile without a schema bump or legacy fingerprint change.");
                Require(manifest.ResolveSemantic("equipment","pack.explorer").JsonPointer=="/packs/4"
                    &&manifest.ResolveSemantic("crafting","recipe-4").JsonPointer=="/recipes/3"
                    &&manifest.ResolveSemantic("crafting-component","ing-4-1-crystal_vial").JsonPointer=="/recipes/3/components/1"
                    &&manifest.ResolveSemantic("recipe-result","").JsonPointer=="/recipes/3/resultItem"
                    &&manifest.ResolveSemantic("crafting","recipe-4").ViewerAccess==ContentViewerAccess.RequiresExistingKnowledge,
                    "Source-scoped identities or formula knowledge access were collapsed.");
                var players=manifest.PlayerProjection();
                Require(players.Any(x=>x.Domain=="crafting"&&x.SemanticId=="recipe-4")
                    &&!players.Any(x=>x.Domain=="crafting-review")
                    &&!FormulaResearchRules.Knows(state,TestOnlyPolicy.CompanionId,SharedResearchFixture.Recipe),
                    "Public definition visibility leaked director metadata or granted formula knowledge.");
                var glass=manifest.ResolveSemantic("equipment","alchemical-containers.glass-vial");
                Require(glass.SourceMass.State==ContentValueState.Null&&glass.OperationalMass.State==ContentValueState.NotApplicable
                    &&ContentValue.Known("0").Value=="0"&&ContentValue.Unknown().State!=ContentValueState.Null
                    &&ContentValue.Unsupported().State!=ContentValueState.NotApplicable,
                    "Source null, unknown, zero, N/A and unsupported were conflated.");
                var internalRecord=manifest.ResolveSemantic("crafting-review","recipe-4");
                Require(internalRecord.Visibility==ContentVisibility.Internal&&internalRecord.ViewerAccess==ContentViewerAccess.InternalOnly,
                    "Internal review metadata lost its explicit visibility boundary.");
            });
            cases.Add("content_manifest_missing_required_reference_and_unsupported_operation_fail_closed",()=>{
                var missing=TestOnlyContentManifest.CreateSelectedProfileWithout("crafting-component","ing-4-1-crystal_vial");
                Require(missing.ValidateBindings()=="ContentRequiredReferenceUnresolved","Missing required source component did not fail closed.");
                var manifest=TestOnlyContentManifest.CreateSelectedProfile();
                Require(manifest.ValidateOperation("equipment","simple-melee-weapons.club",ContentOperation.Manufacture)=="ContentOperationUnsupported"
                    &&manifest.ValidateOperation("equipment","unregistered.item",ContentOperation.PortableEquipment)=="ContentIdentityUnknown",
                    "Unsupported operation and unknown identity collapsed.");
                var p=ResolvedPolicy();var s=World(p);var before=Bytes(s);
                var rejected=new Command("content.unsupported.repair",TestOnlyPolicy.ActorId,s.Capture().Revision,CommandKind.StartToolRepair,PortableKitFixture.Tools);
                RejectUnchanged(s,host,rejected,"ContentOperationUnsupported");
                Require(before.SequenceEqual(Bytes(s)),"Unsupported content operation advanced time, resources, RNG, revision or receipts.");
            });
            cases.Add("content_manifest_portable_command_replay_and_restore_use_frozen_binding",()=>{
                var p=ResolvedPolicy(PortableToolSeed());var s=World(p);var before=s.Capture();var legacy=PortablePolicy().Initial();
                Require(before.PortableEquipment.Any(x=>x.Id==PortableKitFixture.Pack&&x.ProfileId=="adventuring-gear.backpack")
                    &&before.PortableEquipment.Length==legacy.PortableEquipment.Length
                    &&!FormulaResearchRules.Knows(before,TestOnlyPolicy.CompanionId,SharedResearchFixture.Recipe),
                    "Selecting the manifest granted inventory or knowledge instead of binding existing fixture identities.");
                PortableCommit(s,Portable(s,CommandKind.HandlePortableEquipment,PortableKitFixture.Tools,handling:HandlingKind.Retrieve));
                PortableMoveToCache(s);SupplyCommit(s,SupplyCommand(s,SupplyCacheInteraction.PickWithTools));WorldAdvance(s,6);
                Require(s.Capture().SupplyCacheAttempts.Any(x=>x.Status==SupplyCacheAttemptStatus.Succeeded),"Resolved tool binding did not reach the selected cache operation.");
                byte[] bytes=Bytes(s);var restored=new Simulation(p,new SnapshotCodec().Decode(bytes),ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)),"Manifest-bound portable command history did not restore identically.");
            });
            cases.Add("content_manifest_club_attack_and_recipe_manufacture_restore_pending_continuation",()=>{
                var p=ResolvedPolicy(SeedForDeath(16));var s=World(p);LearnManufacturing(s);ManufactureStart(s,extra:2);
                var advance=IC(s,CommandKind.AdvanceClock,x:14401,y:1);var result=s.Execute(host,advance);
                Require(result.Outcome==Outcome.Committed&&result.IsSuspended&&s.Capture().ManufacturingAdvance!=null,
                    "Manifest-bound recipe-4 manufacturing did not reach the existing saved quality continuation.");
                byte[] pending=Bytes(s);var restored=new Simulation(p,new SnapshotCodec().Decode(pending),ExecutionProfile.Laboratory);
                Require(pending.SequenceEqual(Bytes(restored)),"Pending manifest-bound manufacturing continuation changed on restore.");
                foreach(var sim in new[]{s,restored})ManufactureChoice(sim,catalyst:3);
                Require(Bytes(s).SequenceEqual(Bytes(restored))&&s.Capture().AlchemyDoses.Length>0
                    &&s.Capture().AlchemyDoses.All(x=>x.RecipeId=="recipe-4"),"Resolved recipe result did not replay identically or preserve recipe provenance.");
                var steps=new[]{(0,1),(0,1),(0,1),(1,0),(1,0)};
                for(int index=0;index<steps.Length;index++) {
                    if(s.Capture().WorldTraversals.Length!=0)throw new Exception("Unexpected traversal before workshop step "+index+" at "+s.Capture().RuleClock);
                    WorldStep(s,steps[index].Item1,steps[index].Item2);WorldAdvance(s,2);
                    if(s.Capture().WorldTraversals.Length!=0)throw new Exception("Workshop step did not finish "+index+" at "+s.Capture().RuleClock);
                }
                WorldAdvance(s,1);BeginEncounter(s);
                WorldCommit(s,DoseCommand(s,s.Capture().AlchemyDoses[0].Id));
                var used=s.Capture().AlchemyDoses.Single(x=>x.Spent);byte[] usedBytes=Bytes(s);
                Require(used.RecipeId=="recipe-4"&&used.ActualHealing>=0
                    &&usedBytes.SequenceEqual(Bytes(new Simulation(p,new SnapshotCodec().Decode(usedBytes),ExecutionProfile.Laboratory))),
                    "The typed recipe result did not resolve through its existing use handler and restore path.");
                var combat=new TestOnlySharedWorldPolicy(TestOnlyContentManifest.CreateSelectedProfile(),new PortableKitFixture(),
                    new SharedCombatFixture(seed:SeedForDeath(6)),new SupplyCacheFixture());var arena=World(combat);
                WorldStep(arena,1,0);WorldAdvance(arena,2);WorldStep(arena,1,0);WorldAdvance(arena,2);WorldStep(arena,1,0);
                Require(arena.Capture().InventoryCombat,"Source-resolved combat fixture did not enter its connected encounter.");
                for(int count=0;arena.Capture().Encounter.CurrentActor!=TestOnlyPolicy.ActorId&&count<4;count++) {
                    WorldCommit(arena,Tac(arena,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));
                    WorldCommit(arena,Tac(arena,CommandKind.EndRegularTurn));
                }
                Require(arena.Capture().Encounter.CurrentActor==TestOnlyPolicy.ActorId,"Could not reach the controlled actor's regular slot.");
                WorldCommit(arena,Tac(arena,CommandKind.SelectCombatStance,stance:(int)CombatStance.Aggressive));TacStep(arena,3,0);
                WorldCommit(arena,Tac(arena,CommandKind.AttackClub,AdditionalTacticalActor.Id,weapon:TestOnlyClubAttackPolicy.ActorClub));
                Require(arena.Capture().MeleeAttacks.Length==1&&arena.Capture().WorldIntervals.Single(x=>x.ActorId==TestOnlyPolicy.ActorId).ActionSpent,
                    "Source-bound Club profile did not resolve through the actual connected attack handler.");
            });
        }
    }
}
#endif
