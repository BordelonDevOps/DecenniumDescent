using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text.Json;
using Decennium.Foundation;
using Decennium.Foundation.Laboratory;

public static class WorkTimingProbe
{
    static readonly SnapshotCodec Codec = new SnapshotCodec();
    static readonly JsonSerializerOptions J = new JsonSerializerOptions { IncludeFields = true, WriteIndented = true };
    static readonly Authority Grant = TestOnlySharedWorldPolicy.Host();
    const string Hero = ConnectedExpeditionSession.Hero, Cleric = ClericRpProfile.Actor;
    static string Root;
    static readonly List<object> Rows = new List<object>();
    static string Hash(byte[] bytes) { using (var h = SHA256.Create()) return string.Concat(h.ComputeHash(bytes).Select(x => x.ToString("x2"))); }
    static void Check(bool ok, string why) { if (!ok) throw new Exception(why); }
    static void Write(string name, object value) => File.WriteAllText(Path.Combine(Root, name + ".json"), JsonSerializer.Serialize(value, J));
    static ConnectedExpeditionSession New() => ConnectedExpeditionSession.StartWithOrdinaryMagicalActivity(ClericInitialSelection.AuthoredExample(), ClericRepertoireSelection.AuthoredExample(), ClericMilestoneDeclaration.AuthoredExample(), BishopEntryRecord.Announced());
    static Simulation Sim(ConnectedExpeditionSession session) => (Simulation)typeof(ConnectedExpeditionSession).GetField("simulation", BindingFlags.NonPublic | BindingFlags.Instance).GetValue(session);
    static ConnectedExpeditionSession Restore(string path)
    {
        var session = New(); session.Restore(path);
        Write("input", new { path, sha256 = Hash(File.ReadAllBytes(path)), scope = "Strict restore of unchanged authentic116 source; existing TEST_ONLY Simulation command API. ConnectedExpeditionSession does not expose water filling." });
        return session;
    }
    static object Inventory(Snapshot s) => new {
        s.Revision, clock = s.RuleClock.ToString(), s.InventoryCombat,
        actors = s.Actors.Select(a => new { a.Id, a.X, a.Y }),
        vessels = s.Vessels.Select(v => new { v.Id, profile = v.Profile.ToString(), v.OwnerId, v.LocationId, v.CustodianId, contents = WaterFilling.Contents(s, v.Id).ToString(), free = WaterFilling.FreeCapacity(s, v.Id).ToString() }),
        water = s.InventoryLots.Where(m => m.Nutrition == NutritionKind.WaterPints).Select(m => { var l = s.Work.Lots.Single(x => x.Id == m.LotId); return new { m.LotId, m.OwnerId, access = m.Access.ToString(), l.LocationId, l.CustodianId, amount = l.Amount.ToString(), available = s.Work.AvailableAmount(l.Id).ToString() }; }),
        portable = s.PortableEquipment.Where(x => x.OwnerId == Hero || x.OwnerId == Cleric).Select(x => new { x.Id, x.OwnerId, x.CustodianId, x.ParentId, placement = x.Placement.ToString(), x.Open }),
        fills = s.WaterFills.Select(x => new { x.Id, x.WorkerId, x.SourceLotId, x.DestinationId, progress = x.Progress.ToString(), status = x.Status.ToString() }),
        s.Clubs,
        s.OrdinaryMagic
    };
    public static void Inspect(string dir, string[] args)
    {
        Root = dir; var session = Restore(args[0]); var sim = Sim(session); var s = sim.Capture();
        byte[] before = Codec.Encode(s);
        Write("inventory", Inventory(s));
        Write("discovery", sim.DiscoverCommands(Grant, Hero).Select(x => new { x.Command.Id, kind = x.Command.Kind.ToString(), x.Command.Target, x.Query.Admissible, x.Query.Code }).ToArray());
        Check(before.SequenceEqual(Codec.Encode(sim.Capture())), "Inventory/discovery inspection mutated gameplay");
        Write("result", new { status = "INSPECTED", unchanged = true, s.Revision, sourceSha256 = Hash(File.ReadAllBytes(args[0])) });
    }
    static void Commit(Simulation sim, Command c)
    {
        byte[] before = Codec.Encode(sim.Capture());
        var query = sim.QueryCommand(Grant, c);
        Check(before.SequenceEqual(Codec.Encode(sim.Capture())), "Query changed state");
        var result = sim.Execute(Grant, c);
        Rows.Add(new { c.Id, kind = c.Kind.ToString(), c.Actor, c.Target, c.X, c.Y, querySupported = query.Supported, query.Admissible, query.Code, outcome = result.Outcome.ToString(), resultCode = result.Code, result.Revision, clock = sim.Capture().RuleClock.ToString() });
        Write("commands", Rows);
        if (result.Outcome != Outcome.Committed) {
            new FileSaveStore().Save(Path.Combine(Root, "failed-command-state.ddsave"), sim.Capture());
            Write("failed-command-inventory", Inventory(sim.Capture()));
        }
        Check(result.Outcome == Outcome.Committed, "Command rejected " + c.Id + ": " + result.Code);
    }
    static string Id(Simulation sim, string suffix) => "oma.work." + suffix + "." + sim.Capture().Revision;
    static RuleTime Difference(RuleTime end, RuleTime start) => new RuleTime(checked(end.Numerator * start.Denominator - start.Numerator * end.Denominator), checked(end.Denominator * start.Denominator));
    static void Advance(Simulation sim, RuleTime delta, string label)
    {
        Check(delta > default(RuleTime), "Nonpositive advance");
        Commit(sim, new Command(Id(sim, label), Hero, sim.Capture().Revision, CommandKind.AdvanceClock, x: checked((int)delta.Numerator), y: checked((int)delta.Denominator)));
    }
    static void Walk(Simulation sim, int x, int y)
    {
        for (int steps = 0; steps < 12; steps++) {
            var s = sim.Capture(); var a = s.Actors.Single(v => v.Id == Hero);
            if (a.X == x && a.Y == y) return;
            int dx = a.X == x ? 0 : Math.Sign(x - a.X), dy = dx == 0 ? Math.Sign(y - a.Y) : 0;
            Commit(sim, new Command(Id(sim, "walk"), Hero, s.Revision, CommandKind.BeginWorldStep, "walk", dx, dy));
            for (int seconds = 0; sim.Capture().WorldTraversals.Any(v => v.ActorId == Hero) && seconds < 8; seconds++) Advance(sim, new RuleTime(1), "walk-clock");
            Check(!sim.Capture().WorldTraversals.Any(v => v.ActorId == Hero), "Lawful traversal did not complete within bounded8 seconds");
        }
        throw new Exception("Bounded worksite route did not arrive");
    }
    static void Save(ConnectedExpeditionSession session, string name, bool strict = false)
    {
        byte[] bytes = Codec.Encode(Sim(session).Capture()); var path = Path.Combine(Root, name + ".ddsave");
        session.Save(path); Check(bytes.SequenceEqual(Codec.Encode(new FileSaveStore().Load(path))), "Codec roundtrip changed " + name);
        if (strict) { var restored = New(); restored.Restore(path); Check(bytes.SequenceEqual(Codec.Encode(Sim(restored).Capture())), "Strict restore changed " + name); }
        Write(name + ".binding", new { path, sha256 = Hash(File.ReadAllBytes(path)), canonicalEqual = true, strictCampaignRestore = strict });
    }
    public static void Run(string dir, string[] args)
    {
        Root = dir; var session = Restore(args[0]); var sim = Sim(session);
        try {
            Write("initial-inventory", Inventory(sim.Capture()));
            // Actual inspection found32pints in the existing clean pool and an empty Hero-owned base skin.
            // The actual declared map blocks(6,1); route through(7,2), retaining paid terrain traversal.
            // The prepared plot is(3,3); (3,2) satisfies existing cardinal access without contacting Ferry.
            Walk(sim, 7, 2);
            Walk(sim, 3, 2);
            var before = sim.Capture();
            Advance(sim, Difference(before.OrdinaryMagic.Current.Deadline, before.RuleClock), "align-owner-start");
            before = sim.Capture(); Check(before.RuleClock == before.OrdinaryMagic.Current.OriginAt, "Not actual owner Start");
            string source = TestOnlyFillingPolicy.SupplyId, destination = TestOnlyFillingPolicy.ActorSkinId;
            Check(before.Work.AvailableAmount(source) >= new RuleQuantity(1) && WaterFilling.FreeCapacity(before, destination) >= new RuleQuantity(1), "Actual finite water or capacity unavailable");
            var sourceAmount = before.Work.Lots.Single(x => x.Id == source).Amount;
            var destAmount = WaterFilling.Contents(before, destination);
            var origin = before.OrdinaryMagic.Current.Origin;
            var deadline = before.OrdinaryMagic.Current.Deadline;
            Commit(sim, new Command(Id(sim, "start-fill"), Hero, before.Revision, CommandKind.StartWaterFill, source, inventory: new InventoryRequest(new RuleQuantity(1), destination)));
            var job = sim.Capture().WaterFills.Single(x => x.Status == WaterFillStatus.Working);
            string jobId = job.Id; Check(job.WorkerId == Hero && job.Progress == default(RuleTime), "No real Hero fill created");
            Save(session, "fill-started");
            Advance(sim, new RuleTime(3), "late-clock");
            var late = sim.Capture(); Check(late.WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(3), "Work not credited exactly3 before late magic");
            Check(late.OrdinaryMagic.Current.Origin.SameAs(origin) && late.RuleClock == late.OrdinaryMagic.Current.OriginAt.AddSeconds(3), "Not genuine late outside interval");
            var magic = new Command(Id(sim, "late-guidance"), Cleric, late.Revision, CommandKind.CastKnownSpell, Cleric, spellCast: new SpellCastRequest("guidance", willingTarget: true));
            Check(session.QueryCastingCommand(ExpeditionSeat.Player, magic).Admissible, "Cleric late Guidance unavailable during Hero job");
            Commit(sim, magic);
            var paid = sim.Capture(); Check(paid.RuleClock == late.RuleClock && paid.WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(3), "Magic duplicated work credit");
            Save(session, "late-magic-while-filling");
            Advance(sim, Difference(deadline, paid.RuleClock), "exact-owner-boundary");
            var boundary = sim.Capture(); job = boundary.WaterFills.Single(x => x.Id == jobId);
            Check(job.Progress == new RuleTime(6) && job.Status == WaterFillStatus.Working, "Boundary work credit is not exactly6");
            Check(boundary.OrdinaryMagic.Settlements.Count(x => x.Origin.SameAs(origin)) == 1 && boundary.OrdinaryMagic.Settlements.Single(x => x.Origin.SameAs(origin)).MagicalActivity, "Late magic settlement not exact once");
            Check(boundary.Work.Lots.Single(x => x.Id == source).Amount == sourceAmount && WaterFilling.Contents(boundary, destination) == destAmount && job.OutputLotId == "", "Work transferred material before completion");
            Save(session, "exact-boundary-working");
            Commit(sim, new Command(Id(sim, "pause-fill"), Hero, boundary.Revision, CommandKind.PauseWaterFill, jobId));
            var paused = sim.Capture(); var claim = paused.Work.Reservations.Single(x => x.Id == job.ReservationId);
            Check(paused.WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(6) && claim.RemainingAmount == new RuleQuantity(1), "Pause lost progress or reservation");
            Advance(sim, new RuleTime(12), "paused-clock");
            Check(sim.Capture().WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(6), "Paused work accrued time");
            Commit(sim, new Command(Id(sim, "cancel-fill"), Hero, sim.Capture().Revision, CommandKind.CancelWaterFill, jobId));
            var cancelled = sim.Capture(); job = cancelled.WaterFills.Single(x => x.Id == jobId);
            Check(job.Status == WaterFillStatus.Cancelled && job.Progress == new RuleTime(6) && cancelled.Work.Reservations.Single(x => x.Id == job.ReservationId).RemainingAmount == default(RuleQuantity), "Cancellation did not release exact reservation");
            Check(cancelled.Work.Lots.Single(x => x.Id == source).Amount == sourceAmount && WaterFilling.Contents(cancelled, destination) == destAmount, "Cancellation moved water");
            Save(session, "paused-cancelled");
            session = New(); session.Restore(Path.Combine(Root, "exact-boundary-working.ddsave")); sim = Sim(session);
            Advance(sim, new RuleTime(54), "finish-fill");
            var complete = sim.Capture(); job = complete.WaterFills.Single(x => x.Id == jobId);
            Check(job.Status == WaterFillStatus.Complete && job.Progress == new RuleTime(60), "Fill did not complete at exact60 active seconds");
            Check(complete.Work.Lots.Single(x => x.Id == source).Amount == sourceAmount - new RuleQuantity(1) && WaterFilling.Contents(complete, destination) == destAmount + new RuleQuantity(1), "Completion transfer quantity incorrect");
            Check(complete.VesselContents.Count(x => x.LotId == job.OutputLotId) == 1, "Completion output duplicated");
            Save(session, "completed-once");
            Write("final-inventory", Inventory(complete));
            Write("result", new { status = "PASS", scope = "Genuine116 simulation-level real Hero filling with existing finite pool/skin; actual Cleric late Guidance; exact3/6/60 work credit; zero-time magic no credit; owner settlement once; pause preserves progress/reservation, cancel releases without transfer; alternate genuine checkpoint completion transfers once. Water filling is not exposed by ConnectedExpeditionSession and is not claimed as host discovery.", jobId, lateRevision = late.Revision, boundaryRevision = boundary.Revision, cancelRevision = cancelled.Revision, completeRevision = complete.Revision, sourceAmount = sourceAmount.ToString(), destinationBefore = destAmount.ToString(), finalSource = complete.Work.Lots.Single(x => x.Id == source).Amount.ToString(), finalDestination = WaterFilling.Contents(complete, destination).ToString() });
        } catch (Exception error) { Write("failure", new { error = error.ToString() }); throw; }
    }
    static void ClericWalk(Simulation sim, int x, int y)
    {
        for (int steps = 0; steps < 12; steps++) {
            var s = sim.Capture(); var a = s.Actors.Single(v => v.Id == Cleric);
            if (a.X == x && a.Y == y) return;
            int dx = a.X == x ? 0 : Math.Sign(x - a.X), dy = dx == 0 ? Math.Sign(y - a.Y) : 0;
            Commit(sim, new Command(Id(sim, "cleric-walk"), Cleric, s.Revision, CommandKind.BeginWorldStep, "walk", dx, dy));
            for (int seconds = 0; sim.Capture().WorldTraversals.Any(v => v.ActorId == Cleric) && seconds < 8; seconds++) Advance(sim, new RuleTime(1), "cleric-walk-clock");
            Check(!sim.Capture().WorldTraversals.Any(v => v.ActorId == Cleric), "Cleric traversal did not finish in bounded8 seconds");
        }
        throw new Exception("Bounded Cleric worksite route did not arrive");
    }
    public static void ClericWork(string dir, string[] args)
    {
        Root = dir; var session = Restore(args[0]); var sim = Sim(session);
        try {
            Write("initial-inventory", Inventory(sim.Capture()));
            // Genuine Hero obstruction is retained separately. Cleric has the existing dropped Club and worn focus.
            ClericWalk(sim, 7, 2); ClericWalk(sim, 4, 2); ClericWalk(sim, 4, 3);
            var ready = sim.Capture(); Advance(sim, Difference(ready.OrdinaryMagic.Current.Deadline, ready.RuleClock), "cleric-align-start");
            ready = sim.Capture(); var origin = ready.OrdinaryMagic.Current.Origin; var deadline = ready.OrdinaryMagic.Current.Deadline;
            Check(ready.RuleClock == ready.OrdinaryMagic.Current.OriginAt, "Not real owner Start");
            string source = TestOnlyFillingPolicy.SupplyId, destination = TestOnlyFillingPolicy.CompanionSkinId;
            var sourceBefore = ready.Work.Lots.Single(x => x.Id == source).Amount; var destBefore = WaterFilling.Contents(ready, destination);
            var availableBefore = ready.Work.AvailableAmount(source);
            Check(availableBefore >= new RuleQuantity(1) && WaterFilling.FreeCapacity(ready, destination) >= new RuleQuantity(1), "No actual water/capacity");
            Commit(sim, new Command(Id(sim, "cleric-fill"), Cleric, ready.Revision, CommandKind.StartWaterFill, source, inventory: new InventoryRequest(new RuleQuantity(1), destination)));
            var job = sim.Capture().WaterFills.Single(x => x.Status == WaterFillStatus.Working); string jobId = job.Id;
            Check(job.WorkerId == Cleric && job.Progress == default(RuleTime), "No actual Cleric fill");
            Save(session, "cleric-fill-started");
            Advance(sim, new RuleTime(2), "old-end-work"); Check(sim.Capture().WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(2), "Old End duplicated or omitted work");
            Advance(sim, new RuleTime(1), "late-work"); var busy = sim.Capture();
            Check(busy.WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(3), "Late work not exact3");
            var denied = new Command(Id(sim, "busy-guidance"), Cleric, busy.Revision, CommandKind.CastKnownSpell, Cleric, spellCast: new SpellCastRequest("guidance", willingTarget: true));
            byte[] busyBytes = Codec.Encode(busy); var query = sim.QueryCommand(Grant, denied); var rejection = sim.Execute(Grant, denied);
            Check(!query.Admissible && rejection.Outcome == Outcome.Rejected && busyBytes.SequenceEqual(Codec.Encode(sim.Capture())), "Active-worker magic did not reject atomically");
            Write("active-work-magic-denial", new { query.Code, result = rejection.Code, unchanged = true, busy.Revision, progress = "3/1" });
            Advance(sim, Difference(deadline, busy.RuleClock), "exact-work-start"); var boundary = sim.Capture(); job = boundary.WaterFills.Single(x => x.Id == jobId);
            Check(job.Progress == new RuleTime(6) && job.Status == WaterFillStatus.Working, "Owner Start work not exact6");
            Check(boundary.OrdinaryMagic.Settlements.Count(x => x.Origin.SameAs(origin)) == 1, "Calendar opportunity settled other than once");
            Check(boundary.Work.Lots.Single(x => x.Id == source).Amount == sourceBefore && WaterFilling.Contents(boundary, destination) == destBefore && job.OutputLotId == "", "Premature liquid transfer");
            Save(session, "cleric-boundary-working");
            Commit(sim, new Command(Id(sim, "cleric-pause"), Cleric, boundary.Revision, CommandKind.PauseWaterFill, jobId));
            var paused = sim.Capture(); Check(paused.WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(6) && paused.Work.Reservations.Single(x => x.Id == job.ReservationId).RemainingAmount == new RuleQuantity(1), "Pause lost work/claim");
            Advance(sim, Difference(paused.OrdinaryMagic.Current.Deadline.AddSeconds(3), paused.RuleClock), "paused-next-late");
            var late = sim.Capture(); Check(late.WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(6), "Paused work advanced");
            var magic = new Command(Id(sim, "paused-late-guidance"), Cleric, late.Revision, CommandKind.CastKnownSpell, Cleric, spellCast: new SpellCastRequest("guidance", willingTarget: true));
            Check(session.QueryCastingCommand(ExpeditionSeat.Player, magic).Admissible, "Paused-worker late magic unavailable");
            Commit(sim, magic); Check(sim.Capture().WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(6), "Magic credited paused work");
            Save(session, "paused-late-magic");
            Advance(sim, new RuleTime(12), "paused-after-magic");
            Check(sim.Capture().WaterFills.Single(x => x.Id == jobId).Progress == new RuleTime(6), "Paused work advanced across later boundaries");
            Commit(sim, new Command(Id(sim, "cleric-cancel"), Cleric, sim.Capture().Revision, CommandKind.CancelWaterFill, jobId));
            var cancel = sim.Capture(); job = cancel.WaterFills.Single(x => x.Id == jobId);
            Check(job.Status == WaterFillStatus.Cancelled && job.Progress == new RuleTime(6) && cancel.Work.Reservations.Single(x => x.Id == job.ReservationId).RemainingAmount == default(RuleQuantity), "Cancel failed to release retained claim");
            Check(cancel.Work.Lots.Single(x => x.Id == source).Amount == sourceBefore && WaterFilling.Contents(cancel, destination) == destBefore && cancel.Work.AvailableAmount(source) == availableBefore, "Cancellation moved water or lost stock");
            Save(session, "cleric-cancelled");
            var checkpoint = Path.Combine(Root, "cleric-boundary-working.ddsave"); session = New(); session.Restore(checkpoint); sim = Sim(session);
            Check(File.ReadAllBytes(checkpoint).SequenceEqual(Codec.Encode(sim.Capture())), "Active-work strict restore changed bytes");
            Advance(sim, new RuleTime(54), "cleric-completion"); var complete = sim.Capture(); job = complete.WaterFills.Single(x => x.Id == jobId);
            Check(job.Status == WaterFillStatus.Complete && job.Progress == new RuleTime(60), "Completion not exact60 active seconds");
            Check(complete.Work.Lots.Single(x => x.Id == source).Amount == sourceBefore - new RuleQuantity(1) && WaterFilling.Contents(complete, destination) == destBefore + new RuleQuantity(1), "Completion transferred incorrect water");
            Check(complete.VesselContents.Count(x => x.LotId == job.OutputLotId) == 1, "Duplicate output");
            Save(session, "cleric-completed-once", true); Write("final-inventory", Inventory(complete));
            Write("result", new { status = "PASS", scope = "Genuine116 simulation-level Cleric productive filling; exact2/3/6 active work through old End and owner Start, incompatible own magic rejects unchanged while active; pause retains6seconds/one-pint claim; later actual late Guidance succeeds while paused; further time does not credit paused work; cancel releases with no liquid transfer; separate strict-restored active checkpoint completes once at60seconds. Hero concurrent magic/work intersection is not claimed: Hero cannot release his held Club in this profile. Session water-fill exposure remains unsupported.", jobId, workActor = Cleric, busyDenial = rejection.Code, sourceBefore = sourceBefore.ToString(), destinationBefore = destBefore.ToString(), finalSource = complete.Work.Lots.Single(x => x.Id == source).Amount.ToString(), finalDestination = WaterFilling.Contents(complete, destination).ToString(), boundaryRevision = boundary.Revision, pausedMagicRevision = late.Revision + 1, cancelRevision = cancel.Revision, completionRevision = complete.Revision });
        } catch (Exception error) { Write("failure", new { error = error.ToString() }); throw; }
    }
}
