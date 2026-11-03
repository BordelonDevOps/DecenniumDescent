#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ResourceLot Lot(string id="TEST_ONLY.material",long quantity=10)
            => new ResourceLot(id,"TEST_ONLY.unit",quantity,"TEST_ONLY.store","TEST_ONLY.owner");
        private static WorkerInterval Work(string id,long start,long end,string job="TEST_ONLY.job",string worker="TEST_ONLY.worker")
            => new WorkerInterval(id,job,worker,T(start),T(end));
        private static ResourceReservation Claim(string id,long quantity=3,string job="TEST_ONLY.job",string lot="TEST_ONLY.material")
            => new ResourceReservation(id,job,lot,quantity);
        private static void AddWorkLedgerCases(Dictionary<string,Action> cases)
        {
            cases.Add("work_reserve_is_not_consumption_or_transfer", () => {
                var initial=new WorkLedger(new[]{Lot()});
                var reserved=initial.Reserve("TEST_ONLY.job",new[]{Work("setup",0,300)},new[]{Claim("inputs")});
                Require(reserved.Lots[0].Quantity==10 && reserved.Available("TEST_ONLY.material")==7 && reserved.Lots[0].LocationId=="TEST_ONLY.store"
                    && reserved.Lots[0].CustodianId=="TEST_ONLY.owner" && initial.Reservations.Count==0,"Reservation does not consume or move stock."); });
            cases.Add("work_atomic_rejection_on_stock_or_worker_conflict", () => {
                var initial=new WorkLedger(new[]{Lot()},new[]{Work("prior",0,300)});
                Throws<ArgumentException>(()=>initial.Reserve("TEST_ONLY.other",new[]{Work("conflict",299,400,"TEST_ONLY.other")},new[]{Claim("new",3,"TEST_ONLY.other")}));
                Throws<ArgumentException>(()=>initial.Reserve("TEST_ONLY.other",new[]{Work("valid",300,600,"TEST_ONLY.other")},new[]{Claim("too-many",11,"TEST_ONLY.other")}));
                Require(initial.WorkerIntervals.Count==1 && initial.Reservations.Count==0 && initial.Available("TEST_ONLY.material")==10,"Failed batch partially reserved."); });
            cases.Add("work_adjacent_intervals_allowed_overlap_rejected", () => {
                var ok=new WorkLedger(workerIntervals:new[]{Work("b",300,600),Work("a",0,300)});
                Require(ok.WorkerIntervals.Select(x=>x.Id).SequenceEqual(new[]{"a","b"}),"Half-open intervals share endpoint.");
                Throws<ArgumentException>(()=>new WorkLedger(workerIntervals:new[]{Work("a",0,300),Work("b",1,2)}));
                var fractional=new WorkLedger(workerIntervals:new[]{new WorkerInterval("a","job","worker",T(0),T(1,3)),new WorkerInterval("b","job","worker",T(1,3),T(2,3))});
                Require(fractional.WorkerIntervals.Count==2,"Exact fractional endpoint."); });
            cases.Add("work_different_workers_and_passive_time", () => {
                var ledger=new WorkLedger(workerIntervals:new[]{Work("a",0,300),Work("b",0,300,worker:"TEST_ONLY.assistant"),
                    Work("retrieval",3300,3600),Work("independent",300,3300,"TEST_ONLY.other")});
                Require(ledger.WorkerIntervals.Count==4,"Trap passive elapsed soak does not reserve the setter as active labor."); });
            cases.Add("work_multiple_claims_cannot_overreserve", () => {
                Throws<ArgumentException>(()=>new WorkLedger(new[]{Lot()},reservations:new[]{Claim("a",6),Claim("b",5)}));
                var exact=new WorkLedger(new[]{Lot()},reservations:new[]{Claim("a",6),Claim("b",4)});
                Require(exact.Available("TEST_ONLY.material")==0,"Exact capacity."); });
            cases.Add("work_consumption_once_and_replay_safe", () => {
                var reserved=new WorkLedger(new[]{Lot()},reservations:new[]{Claim("a",3),Claim("b",4)});
                var consumed=reserved.Consume("TEST_ONLY.job","a");var replay=consumed.Consume("TEST_ONLY.job","a");
                Require(consumed.Lots[0].Quantity==7 && consumed.Available("TEST_ONLY.material")==3 && replay.Lots[0].Quantity==7
                    && consumed.Reservations.Single(x=>x.Id=="a").Status==ReservationStatus.Consumed,"Debit once and release only spent reservation quantity.");
                Throws<ArgumentException>(()=>consumed.Release("TEST_ONLY.job","a")); });
            cases.Add("work_release_once_has_no_refund_or_physical_transfer", () => {
                var reserved=new WorkLedger(new[]{Lot()},reservations:new[]{Claim("a")});
                var released=reserved.Release("TEST_ONLY.job","a").Release("TEST_ONLY.job","a");
                Require(released.Lots[0].Quantity==10 && released.Available("TEST_ONLY.material")==10
                    && released.Lots[0].LocationId=="TEST_ONLY.store","Free reservation only.");
                Throws<ArgumentException>(()=>released.Consume("TEST_ONLY.job","a"));
                Throws<ArgumentException>(()=>released.Reserve("TEST_ONLY.job",Array.Empty<WorkerInterval>(),new[]{Claim("a")})); });
            cases.Add("work_settlement_cannot_use_another_jobs_claim", () => {
                var ledger=new WorkLedger(new[]{Lot()},reservations:new[]{Claim("a")});
                Throws<ArgumentException>(()=>ledger.Consume("other-job","a"));
                Throws<ArgumentException>(()=>ledger.Release("other-job","a"));
                Throws<ArgumentException>(()=>ledger.Consume("TEST_ONLY.job","missing"));
                Require(ledger.Lots[0].Quantity==10,"Wrong-job request spent resources."); });
            cases.Add("work_cancel_future_preserves_prior_time_and_costs", () => {
                var ledger=new WorkLedger(new[]{Lot()},new[]{Work("earlier",0,10),Work("current",10,20),Work("future",20,30),Work("other",30,40,"other-job")},new[]{Claim("a")});
                var cancelled=ledger.Consume("TEST_ONLY.job","a").CancelFutureWork("TEST_ONLY.job",T(15));
                Require(cancelled.WorkerIntervals.Count==3 && cancelled.WorkerIntervals.Single(x=>x.Id=="current").End==T(15)
                    && cancelled.WorkerIntervals.Any(x=>x.Id=="other") && cancelled.Lots[0].Quantity==7
                    && cancelled.Reservations[0].Status==ReservationStatus.Consumed,"Cancellation cannot undo committed materials or previous intervals."); });
            cases.Add("work_identity_references_and_record_guards", () => {
                Throws<ArgumentException>(()=>new WorkLedger(new[]{Lot(),Lot()}));
                Throws<ArgumentException>(()=>new WorkLedger(new[]{Lot()},reservations:new[]{Claim("a",lot:"unknown")}));
                Throws<ArgumentException>(()=>new WorkLedger(workerIntervals:new[]{Work("a",0,1),Work("a",1,2)}));
                Throws<ArgumentException>(()=>new ResourceLot("bad id","unit",1,"place","owner"));
                Throws<ArgumentException>(()=>Lot(quantity:-1));
                Throws<ArgumentException>(()=>Claim("a",0));
                Throws<ArgumentException>(()=>Work("a",1,1));
                Throws<ArgumentException>(()=>new WorkLedger(new ResourceLot[]{null}));
                Throws<ArgumentException>(()=>new WorkLedger(new[]{Lot()}).Reserve("wrong-job",new[]{Work("a",0,1)},Array.Empty<ResourceReservation>())); });
            cases.Add("work_detached_immutable_records", () => {
                var lots=new[]{Lot()};var workers=new[]{Work("a",0,1)};var claims=new[]{Claim("a")};
                var ledger=new WorkLedger(lots,workers,claims);lots[0]=Lot(quantity:1);workers[0]=Work("b",2,3);claims[0]=Claim("b");
                Require(ledger.Lots[0].Quantity==10 && ledger.WorkerIntervals[0].Id=="a" && ledger.Reservations[0].Id=="a","Caller aliases.");
                Throws<NotSupportedException>(()=>((IList<ResourceLot>)ledger.Lots).Clear());
                Throws<NotSupportedException>(()=>((IList<WorkerInterval>)ledger.WorkerIntervals).Clear());
                Throws<NotSupportedException>(()=>((IList<ResourceReservation>)ledger.Reservations).Clear()); });
            cases.Add("work_large_quantities_do_not_overflow_reservation_sum", () => {
                var ledger=new WorkLedger(new[]{Lot(quantity:long.MaxValue)},reservations:new[]{Claim("all",long.MaxValue)});
                Require(ledger.Available("TEST_ONLY.material")==0 && ledger.Consume("TEST_ONLY.job","all").Lots[0].Quantity==0,"Exact long maximum.");
                Throws<ArgumentException>(()=>new WorkLedger(new[]{Lot(quantity:long.MaxValue)},reservations:new[]{Claim("all",long.MaxValue),Claim("extra",1)})); });
            cases.Add("work_component_roundtrip_retains_settlement_and_intervals", () => {
                var codec=new WorkLedgerCodec();
                var initial=new WorkLedger(new[]{Lot()},new[]{new WorkerInterval("w","TEST_ONLY.job","worker",T(1,3),T(20,3))},new[]{Claim("a"),Claim("b",2)});
                var consumed=initial.Consume("TEST_ONLY.job","a");var bytes=codec.Encode(consumed);var restored=codec.Decode(bytes);
                Require(codec.Encode(restored).SequenceEqual(bytes) && restored.WorkerIntervals[0].Start==T(1,3)
                    && restored.Consume("TEST_ONLY.job","a").Lots[0].Quantity==7
                    && restored.Consume("TEST_ONLY.job","b").Lots[0].Quantity==5,"Resume cannot double spend.");
                Require(codec.Decode(codec.Encode(new WorkLedger())).Lots.Count==0,"Empty component supported."); });
            cases.Add("work_component_encoding_stable_across_input_order", () => {
                var a=new WorkLedger(new[]{Lot("b"),Lot("a")},new[]{Work("b",1,2),Work("a",0,1)},new[]{Claim("b",lot:"b"),Claim("a",lot:"a")});
                var b=new WorkLedger(a.Lots.Reverse(),a.WorkerIntervals.Reverse(),a.Reservations.Reverse());
                var codec=new WorkLedgerCodec();Require(codec.Encode(a).SequenceEqual(codec.Encode(b)),"Canonical component ordering."); });
            cases.Add("work_component_corruption_unknown_schema_and_malformed_count", () => {
                var codec=new WorkLedgerCodec();var original=codec.Encode(new WorkLedger(new[]{Lot()}));
                var corrupt=(byte[])original.Clone();corrupt[15]^=1;Throws<InvalidDataException>(()=>codec.Decode(corrupt));
                var schema=(byte[])original.Clone();schema[4]=3;Resign(schema);Throws<InvalidDataException>(()=>codec.Decode(schema));
                var count=(byte[])original.Clone();for(int i=8;i<12;i++)count[i]=255;Resign(count);Throws<InvalidDataException>(()=>codec.Decode(count));
                Throws<InvalidDataException>(()=>codec.Decode(original.Take(original.Length-1).ToArray()));
                Throws<InvalidDataException>(()=>codec.Decode(new byte[WorkLedgerCodec.MaxBytes+1]));
                Throws<InvalidDataException>(()=>codec.Decode(null)); });
        }
    }
}
#endif
