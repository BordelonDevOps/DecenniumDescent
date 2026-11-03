#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public sealed class CaseResult
    {
        public string Name { get; set; }
        public bool Passed { get; set; }
        public string Error { get; set; }
    }
    public static partial class FoundationCases
    {
        private static Simulation New() => new Simulation(new TestOnlyPolicy(), new TestOnlyPolicy().Initial(), ExecutionProfile.Laboratory);
        private static Command Open(string id = "open", long revision = 0) => new Command(id, TestOnlyPolicy.ActorId, revision,
            CommandKind.Interact, TestOnlyPolicy.ContainerId);
        private static byte[] Bytes(Simulation sim) => new SnapshotCodec().Encode(sim.Capture());
        private static void Require(bool condition, string message) { if (!condition) throw new Exception(message); }
        private static void Throws<T>(Action action) where T : Exception
        { try { action(); } catch (T) { return; } throw new Exception("Expected " + typeof(T).Name); }
        private static void RejectUnchanged(Simulation sim, Authority auth, Command command, string code)
        {
            var before = Bytes(sim); var result = sim.Execute(auth, command);
            Require(result.Outcome == Outcome.Rejected && result.Code == code, "Expected rejection " + code + ", got " + result.Code);
            Require(before.SequenceEqual(Bytes(sim)), "Rejection mutated state, receipts, clock or RNG.");
        }
        private static Dictionary<string, Action> Cases(string directory)
        {
            var host = TestOnlyPolicy.Host(); var codec = new SnapshotCodec();
            var cases = new Dictionary<string, Action>(StringComparer.Ordinal) {
                ["interaction_commits_one_token"] = () => {
                    var s = New(); var r = s.Execute(host, Open()); var v = s.Capture();
                    Require(r.Outcome == Outcome.Committed && v.Revision == 1 && v.Objects[0].Opened && v.Actors[0].Tokens == 1,
                        "One interaction must transfer exactly one synthetic token."); },
                ["duplicate_is_idempotent"] = () => {
                    var s = New(); s.Execute(host, Open()); var b = Bytes(s); var r = s.Execute(host, Open());
                    Require(r.Outcome == Outcome.Duplicate && r.Revision == 1 && b.SequenceEqual(Bytes(s)), "Duplicate changed state."); },
                ["command_id_reuse_with_new_payload_rejected"] = () => {
                    var s = New(); s.Execute(host, Open()); RejectUnchanged(s, host,
                        new Command("open", TestOnlyPolicy.ActorId, 1, CommandKind.Move, x:-1), "CommandIdConflict"); },
                ["stale_command_has_no_effect"] = () => {
                    var s = New(); s.Execute(host, Open()); RejectUnchanged(s, host, Open("other"), "StaleRevision"); },
                ["unauthorized_actor_has_no_effect"] = () => {
                    RejectUnchanged(New(), new Authority("guest", new[] { TestOnlyPolicy.CompanionId }), Open(), "NotAuthorized"); },
                ["revocation_applies_to_retries"] = () => {
                    var s = New(); s.Execute(host, Open()); RejectUnchanged(s,
                        new Authority(host.Principal, Array.Empty<string>()), Open(), "NotAuthorized"); },
                ["ids_are_scoped_to_authenticated_principal"] = () => {
                    var s = New(); s.Execute(host, Open("shared"));
                    var guest = new Authority("guest", new[] { TestOnlyPolicy.CompanionId });
                    Require(s.Execute(guest, new Command("shared", TestOnlyPolicy.CompanionId, 1, CommandKind.Move, x:-1)).Outcome
                        == Outcome.Committed, "Another principal's command ID collided."); },
                ["malformed_commands_are_bounded"] = () => {
                    var s = New(); RejectUnchanged(s, host, null, "InvalidCommand");
                    RejectUnchanged(s, host, new Command(new string('a',97),TestOnlyPolicy.ActorId,0,CommandKind.Move), "InvalidCommand");
                    RejectUnchanged(s, host, new Command("bad",TestOnlyPolicy.ActorId,0,(CommandKind)99), "InvalidCommand");
                    RejectUnchanged(s, host, new Command("bad",TestOnlyPolicy.ActorId,0,CommandKind.Move,x:int.MinValue), "InvalidStep"); },
                ["wall_blocks_movement"] = () => RejectUnchanged(New(),host,
                    new Command("wall",TestOnlyPolicy.ActorId,0,CommandKind.Move,x:1), "Blocked"),
                ["occupied_position_blocks_movement"] = () => {
                    var p = new TestOnlyPolicy(); var v = p.Initial(); v.Actors[1].X=1;v.Actors[1].Y=0;
                    var s = new Simulation(p,v,ExecutionProfile.Laboratory);
                    RejectUnchanged(s,host,new Command("occupied",TestOnlyPolicy.ActorId,0,CommandKind.Move,y:-1), "Occupied"); },
                ["unknown_object_has_no_effect"] = () => RejectUnchanged(New(),host,
                    new Command("missing",TestOnlyPolicy.ActorId,0,CommandKind.Interact,"TEST_ONLY.unknown"), "UnknownObject"),
                ["distant_interaction_has_no_effect"] = () => {
                    var p = new TestOnlyPolicy(); var v = p.Initial();v.Actors[0].X=4;v.Actors[0].Y=4;
                    RejectUnchanged(new Simulation(p,v,ExecutionProfile.Laboratory),host,Open(),"OutOfReach"); },
                ["fresh_id_cannot_reopen_container"] = () => {
                    var s=New();s.Execute(host,Open());RejectUnchanged(s,host,Open("again",1),"AlreadyOpened"); },
                ["equivalent_manual_clock_advances_agree"] = () => {
                    var a=New();var b=New();
                    a.Execute(host,new Command("clock",TestOnlyPolicy.ActorId,0,CommandKind.AdvanceClock,x:3));
                    for(int i=0;i<3;i++) b.Execute(host,new Command("clock"+i,TestOnlyPolicy.ActorId,i,CommandKind.AdvanceClock,x:1));
                    Require(a.Capture().Clock==3 && b.Capture().Clock==3 && a.Capture().RandomState==b.Capture().RandomState,
                        "Clock advancement was not additive."); },
                ["clock_requires_host_permission"] = () => RejectUnchanged(New(),
                    new Authority("guest",new[]{TestOnlyPolicy.ActorId}),
                    new Command("clock",TestOnlyPolicy.ActorId,0,CommandKind.AdvanceClock,x:1),"NotAuthorized"),
                ["clock_overflow_rolls_back"] = () => {
                    var p=new TestOnlyPolicy();var v=p.Initial();v.Clock=long.MaxValue;
                    RejectUnchanged(new Simulation(p,v,ExecutionProfile.Laboratory),host,
                        new Command("clock",TestOnlyPolicy.ActorId,0,CommandKind.AdvanceClock,x:1),"PolicyFailure"); },
                ["rng_has_known_versioned_sequence"] = () => {
                    uint state=1;Require(RandomV1.Next(ref state)==270369u,"RNG vector 1 differs.");
                    Require(RandomV1.Next(ref state)==67634689u,"RNG vector 2 differs.");
                    Require(RandomV1.Next(ref state)==2647435461u,"RNG vector 3 differs.");
                    uint zero=0;Throws<ArgumentException>(()=>RandomV1.Next(ref zero)); },
                ["read_snapshot_cannot_mutate_owner"] = () => {
                    var s=New();var b=Bytes(s);var v=s.Capture();v.Actors[0].Tokens=99;v.RandomState=12;v.Objects[0].Opened=true;
                    Require(b.SequenceEqual(Bytes(s)),"Read view mutated the simulation."); },
                ["constructor_takes_ownership_of_copy"] = () => {
                    var p=new TestOnlyPolicy();var v=p.Initial();var s=new Simulation(p,v,ExecutionProfile.Laboratory);var b=Bytes(s);
                    v.Actors[0].X=4;Require(b.SequenceEqual(Bytes(s)),"External initial state remained authoritative."); },
                ["snapshot_round_trip_preserves_all_fields"] = () => {
                    var s=New();s.Execute(host,Open());s.Execute(host,new Command("tick",TestOnlyPolicy.ActorId,1,CommandKind.AdvanceClock,x:7));
                    var v=s.Capture();RandomV1.Next(ref v.RandomState);var encoded=codec.Encode(v);
                    Require(encoded.SequenceEqual(codec.Encode(codec.Decode(encoded))),"Snapshot changed across round trip."); },
                ["reloaded_receipt_prevents_double_award"] = () => {
                    var s=New();s.Execute(host,Open());var loaded=new Simulation(new TestOnlyPolicy(),codec.Decode(Bytes(s)),ExecutionProfile.Laboratory);
                    var b=Bytes(loaded);Require(loaded.Execute(host,Open()).Outcome==Outcome.Duplicate && b.SequenceEqual(Bytes(loaded)),
                        "Reload allowed a duplicate award."); },
                ["continuation_after_reload_matches"] = () => {
                    var a=New();a.Execute(host,Open());var b=new Simulation(new TestOnlyPolicy(),codec.Decode(Bytes(a)),ExecutionProfile.Laboratory);
                    var next=new Command("move",TestOnlyPolicy.ActorId,1,CommandKind.Move,x:-1);
                    Require(a.Execute(host,next).Outcome==Outcome.Committed && b.Execute(host,next).Outcome==Outcome.Committed
                        && Bytes(a).SequenceEqual(Bytes(b)),"Continuation diverged."); },
                ["content_fingerprint_mismatch_rejected"] = () => {
                    var p=new TestOnlyPolicy();var v=p.Initial();v.ContentFingerprint="TEST_ONLY.other";
                    Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Laboratory)); },
                ["release_profile_rejects_test_only_content"] = () => {
                    var p=new TestOnlyPolicy();Throws<InvalidOperationException>(()=>new Simulation(p,p.Initial(),ExecutionProfile.Release));
                    var v=p.Initial();v.TestOnly=false;Throws<ArgumentException>(()=>new Simulation(p,v,ExecutionProfile.Release)); },
                ["checksum_corruption_rejected"] = () => {
                    byte[] bytes=Bytes(New());bytes[20]^=1;Throws<InvalidDataException>(()=>codec.Decode(bytes)); },
                ["truncation_and_future_schema_rejected"] = () => {
                    byte[] bytes=Bytes(New());Throws<InvalidDataException>(()=>codec.Decode(bytes.Take(bytes.Length-1).ToArray()));
                    bytes[4]=4;Resign(bytes);Throws<InvalidDataException>(()=>codec.Decode(bytes)); },
                ["unknown_fixture_identity_rejected_on_restore"] = () => {
                    var v=new TestOnlyPolicy().Initial();v.Actors[0].Id="TEST_ONLY.unknown";
                    Throws<ArgumentException>(()=>new Simulation(new TestOnlyPolicy(),codec.Decode(codec.Encode(v)),ExecutionProfile.Laboratory)); },
                ["duplicate_entity_and_receipt_ids_rejected"] = () => {
                    var v=new TestOnlyPolicy().Initial();v.Actors[1].Id=v.Actors[0].Id;Throws<ArgumentException>(()=>codec.Encode(v));
                    var s=New();s.Execute(host,Open());v=s.Capture();v.Receipts=new[]{v.Receipts[0],v.Receipts[0].Copy()};
                    Throws<ArgumentException>(()=>codec.Encode(v)); },
                ["non_ascii_receipt_fingerprint_rejected_before_encoding"] = () => {
                    var s=New();s.Execute(host,Open());var v=s.Capture();v.Receipts[0].Fingerprint=new string('\u754c',180);
                    Throws<ArgumentException>(()=>codec.Encode(v));
                    v.Receipts[0].Fingerprint=new string('a',512);var bytes=codec.Encode(v);
                    Require(bytes.SequenceEqual(codec.Encode(codec.Decode(bytes))),"Accepted ASCII boundary failed round trip."); },
                ["disk_save_retains_previous_good_backup"] = () => {
                    string path=Path.Combine(directory,"backup.ddsave");var store=new FileSaveStore();var s=New();
                    store.Save(path,s.Capture());s.Execute(host,Open());store.Save(path,s.Capture());
                    Require(store.Load(path).Revision==1 && store.Load(path+".bak").Revision==0,"Wrong current/backup state."); },
                ["corrupt_current_does_not_overwrite_backup"] = () => {
                    string path=Path.Combine(directory,"corrupt.ddsave");var store=new FileSaveStore();var s=New();
                    store.Save(path,s.Capture());s.Execute(host,Open());store.Save(path,s.Capture());byte[] backup=File.ReadAllBytes(path+".bak");
                    File.WriteAllText(path,"corrupt");Throws<InvalidDataException>(()=>store.Save(path,s.Capture()));
                    Require(backup.SequenceEqual(File.ReadAllBytes(path+".bak")) && File.ReadAllText(path)=="corrupt",
                        "Corrupt current destroyed recovery evidence."); },
                ["commit_failure_preserves_current_and_backup"] = () => {
                    string path=Path.Combine(directory,"interrupted.ddsave");var store=new FileSaveStore();var s=New();
                    store.Save(path,s.Capture());s.Execute(host,Open());store.Save(path,s.Capture());
                    byte[] current=File.ReadAllBytes(path),backup=File.ReadAllBytes(path+".bak");
                    Throws<IOException>(()=>new FileSaveStore(new FailingCommit()).Save(path,s.Capture()));
                    Require(current.SequenceEqual(File.ReadAllBytes(path)) && backup.SequenceEqual(File.ReadAllBytes(path+".bak")),
                        "Failed commit changed persistent state.");
                    Require(!Directory.GetFiles(directory,"interrupted.ddsave.tmp-*").Any(),"Temporary file was not cleaned up."); },
                ["explicit_recovery_preserves_evidence_and_restores_saving"] = () => {
                    string path=Path.Combine(directory,"recover.ddsave");var store=new FileSaveStore();var s=New();
                    store.Save(path,s.Capture());s.Execute(host,Open());store.Save(path,s.Capture());
                    byte[] backup=File.ReadAllBytes(path+".bak");File.WriteAllText(path,"corrupt primary");
                    Simulation recovered=null;
                    string evidence=store.RecoverBackup(path,v=>recovered=new Simulation(new TestOnlyPolicy(),v,ExecutionProfile.Laboratory));
                    Require(File.ReadAllText(evidence)=="corrupt primary" && backup.SequenceEqual(File.ReadAllBytes(path+".bak"))
                        && store.Load(path).Revision==0,"Recovery lost evidence or restored wrong state.");
                    Require(recovered.Execute(host,Open("after-recovery")).Outcome==Outcome.Committed,"Recovery could not continue.");
                    store.Save(path,recovered.Capture());Require(store.Load(path).Revision==1,"Recovery did not restore saving."); },
                ["recovery_failure_leaves_primary_and_backup_unchanged"] = () => {
                    string path=Path.Combine(directory,"recover-failure.ddsave");var store=new FileSaveStore();
                    store.Save(path,New().Capture());store.Save(path,New().Capture());File.WriteAllText(path,"corrupt primary");
                    byte[] backup=File.ReadAllBytes(path+".bak");
                    Throws<IOException>(()=>new FileSaveStore(new FailingCommit()).RecoverBackup(path,v=>{}));
                    Require(File.ReadAllText(path)=="corrupt primary" && backup.SequenceEqual(File.ReadAllBytes(path+".bak"))
                        && Directory.GetFiles(directory).Length==2,"Failed recovery changed evidence or left temp files."); },
                ["recovery_checks_content_before_any_disk_change"] = () => {
                    string path=Path.Combine(directory,"recover-invalid.ddsave");var store=new FileSaveStore();
                    var wrong=New().Capture();wrong.ContentFingerprint="TEST_ONLY.other";
                    store.Save(path,New().Capture());File.WriteAllBytes(path+".bak",codec.Encode(wrong));
                    byte[] current=File.ReadAllBytes(path),backup=File.ReadAllBytes(path+".bak");
                    Throws<ArgumentException>(()=>store.RecoverBackup(path,v=>new Simulation(new TestOnlyPolicy(),v,ExecutionProfile.Laboratory)));
                    Require(current.SequenceEqual(File.ReadAllBytes(path)) && backup.SequenceEqual(File.ReadAllBytes(path+".bak"))
                        && Directory.GetFiles(directory).Length==2,"Domain rejection altered files."); },
                ["corrupt_backup_is_never_recovered"] = () => {
                    string path=Path.Combine(directory,"bad-backup.ddsave");var store=new FileSaveStore();store.Save(path,New().Capture());
                    byte[] current=File.ReadAllBytes(path);File.WriteAllText(path+".bak","bad backup");
                    Throws<InvalidDataException>(()=>store.RecoverBackup(path,v=>{}));
                    Require(current.SequenceEqual(File.ReadAllBytes(path)) && File.ReadAllText(path+".bak")=="bad backup",
                        "Corrupt backup altered current or recovery evidence."); },
                ["recovery_restores_missing_primary"] = () => {
                    string path=Path.Combine(directory,"missing.ddsave");var store=new FileSaveStore();store.Save(path+".bak",New().Capture());
                    string evidence=store.RecoverBackup(path,v=>new Simulation(new TestOnlyPolicy(),v,ExecutionProfile.Laboratory));
                    Require(evidence==null && store.Load(path).Revision==0 && File.Exists(path+".bak"),"Missing primary not restored."); },
                ["oversized_save_rejected"] = () => Throws<InvalidDataException>(()=>codec.Decode(new byte[SnapshotCodec.MaxBytes+1])),
                ["policy_failure_rolls_back_partial_mutation"] = () => {
                    var p=new BadPolicy(false);var s=new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);
                    RejectUnchanged(s,host,Open(),"SyntheticFailure"); },
                ["invalid_policy_result_rolls_back"] = () => {
                    var p=new BadPolicy(true);var s=new Simulation(p,p.Initial(),ExecutionProfile.Laboratory);
                    RejectUnchanged(s,host,Open(),"InvalidResult"); },
                ["receipt_capacity_fails_closed"] = () => {
                    var p=new TestOnlyPolicy();var v=p.Initial();v.Revision=Validation.MaxReceipts;
                    v.Receipts=Enumerable.Range(1,Validation.MaxReceipts).Select(i=>new CommandReceipt {
                        Principal=host.Principal,Id="receipt"+i,Fingerprint="synthetic",Revision=i }).ToArray();
                    RejectUnchanged(new Simulation(p,v,ExecutionProfile.Laboratory),host,Open("new",v.Revision),"SessionCapacityReached"); }
            };
            AddRollCases(cases);
            AddCharacterCases(cases);
            AddCharacterBuildCases(cases);
            AddLifeCases(cases);
            AddCombatBudgetCases(cases);
            AddTimingCases(cases);
            AddWorkLedgerCases(cases);
            AddDiceCases(cases);
            AddWorkSessionCases(cases, directory);
            AddPrototypePolicyCases(cases);
            AddCropCases(cases, directory);
            return cases;
        }
        private static void Resign(byte[] bytes)
        { using(var sha=SHA256.Create()) Buffer.BlockCopy(sha.ComputeHash(bytes,0,bytes.Length-32),0,bytes,bytes.Length-32,32); }
        public static string[] Names() => Cases("").Keys.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        public static CaseResult Run(string name, string directory)
        {
            Directory.CreateDirectory(directory);
            try { Cases(directory)[name](); return new CaseResult {Name=name,Passed=true,Error=""}; }
            catch(Exception e) { return new CaseResult {Name=name,Passed=false,Error=e.ToString()}; }
        }
        public static CaseResult[] RunAll(string directory) => Names().Select(name=>Run(name,Path.Combine(directory,name))).ToArray();
        private sealed class FailingCommit : IFileCommit
        { public void Commit(string temporary,string destination,string backup) { throw new IOException("Injected failure before replace."); } }
        private sealed class BadPolicy : ICommandPolicy
        {
            private readonly bool success;private readonly TestOnlyPolicy fixture=new TestOnlyPolicy();
            public BadPolicy(bool success) { this.success=success; }
            public string ContentFingerprint=>fixture.ContentFingerprint;public bool TestOnly=>true;
            public Snapshot Initial()=>fixture.Initial();public string ValidateState(Snapshot s)=>fixture.ValidateState(s);
            public string Resolve(Snapshot candidate,Command c) {candidate.Actors[0].Tokens=99;candidate.Clock=5;candidate.RandomState=123;
                return success ? null : "SyntheticFailure";}
        }
    }
}
#endif
