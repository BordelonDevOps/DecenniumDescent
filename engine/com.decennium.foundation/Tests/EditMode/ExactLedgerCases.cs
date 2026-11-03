#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static WorkLedger ExactLedger()=>new WorkLedger(new[]{new ResourceLot("food","food-pound",Q(1),"plot","worker")},
            reservations:new[]{new ResourceReservation("meal","eat","food",Q(2,3))});
        private static void AddExactLedgerCases(Dictionary<string,Action> cases)
        {
            var codec=new WorkLedgerCodec();
            cases.Add("exact_ledger_partial_consumption_preserves_reserved_remainder",()=>{
                var before=ExactLedger();var after=before.ConsumeThrough("eat","meal",Q(1,3));var r=after.Reservations[0];
                Require(before.Lots[0].Amount==Q(1)&&after.Lots[0].Amount==Q(2,3)&&r.Amount==Q(2,3)
                    &&r.ConsumedAmount==Q(1,3)&&r.RemainingAmount==Q(1,3)&&r.ReleasedAmount==Q(0)&&r.Status==ReservationStatus.Reserved
                    &&after.AvailableAmount("food")==Q(1,3),"Partial debit lost stock or reserved remainder."); });
            cases.Add("exact_ledger_cumulative_endpoint_is_idempotent",()=>{
                var ledger=ExactLedger().ConsumeThrough("eat","meal",Q(1,3));
                Require(ReferenceEquals(ledger,ledger.ConsumeThrough("eat","meal",Q(1,3))),"Endpoint replay spent again.");
                var full=ledger.Consume("eat","meal");Require(full.Lots[0].Amount==Q(1,3)&&full.Reservations[0].Status==ReservationStatus.Consumed
                    &&ReferenceEquals(full,full.Consume("eat","meal")),"Completion spent original amount twice."); });
            cases.Add("exact_ledger_interruption_releases_only_untouched_quantity",()=>{
                var ledger=ExactLedger().ConsumeThrough("eat","meal",Q(1,3)).Release("eat","meal");var r=ledger.Reservations[0];
                Require(ledger.Lots[0].Amount==Q(2,3)&&ledger.AvailableAmount("food")==Q(2,3)&&r.ConsumedAmount==Q(1,3)
                    &&r.ReleasedAmount==Q(1,3)&&r.RemainingAmount==Q(0)&&r.Status==ReservationStatus.Mixed,"Interrupted food refunded or stayed reserved.");
                Require(ReferenceEquals(ledger,ledger.Release("eat","meal"))&&ReferenceEquals(ledger,ledger.ConsumeThrough("eat","meal",Q(1,3))),"Settled replay changed history.");
                Throws<ArgumentException>(()=>ledger.Consume("eat","meal")); });
            cases.Add("exact_ledger_reversal_overspend_and_wrong_job_reject",()=>{
                var ledger=ExactLedger().ConsumeThrough("eat","meal",Q(1,3));var bytes=codec.Encode(ledger,2);
                Throws<ArgumentException>(()=>ledger.ConsumeThrough("eat","meal",Q(1,4)));
                Throws<ArgumentException>(()=>ledger.ConsumeThrough("eat","meal",Q(3,4)));
                Throws<ArgumentException>(()=>ledger.ConsumeThrough("other","meal",Q(1,3)));
                Throws<ArgumentException>(()=>ledger.Release("other","meal"));
                Require(bytes.SequenceEqual(codec.Encode(ledger,2)),"Rejected settlement mutated prior ledger."); });
            cases.Add("exact_ledger_partial_claim_cannot_be_injected_as_new_reservation",()=>{
                var partial=ExactLedger().ConsumeThrough("eat","meal",Q(1,3)).Reservations[0];
                var empty=new WorkLedger(new[]{new ResourceLot("food","food-pound",Q(1),"plot","worker")});
                Throws<ArgumentException>(()=>empty.Reserve("eat",Array.Empty<WorkerInterval>(),new[]{partial}));
                Require(empty.Reservations.Count==0&&empty.Lots[0].Amount==Q(1),"Injected historical consumption."); });
            cases.Add("exact_ledger_overlapping_claims_preserve_each_jobs_stock",()=>{
                var ledger=ExactLedger().Reserve("other",Array.Empty<WorkerInterval>(),new[]{new ResourceReservation("other-meal","other","food",Q(1,3))});
                ledger=ledger.ConsumeThrough("eat","meal",Q(1,3));Require(ledger.AvailableAmount("food")==Q(0),"Partial debit freed another job's stock.");
                Throws<ArgumentException>(()=>ledger.Reserve("extra",Array.Empty<WorkerInterval>(),new[]{new ResourceReservation("extra","extra","food",Q(1,100))}));
                ledger=ledger.Release("eat","meal").Consume("other","other-meal");Require(ledger.Lots[0].Amount==Q(1,3),"Other job consumed released or spent quantity twice."); });
            cases.Add("exact_ledger_unrepresentable_delta_can_have_representable_result",()=>{
                long m=long.MaxValue;var ledger=new WorkLedger(new[]{new ResourceLot("food","unit",Q(m-1,m),"plot","worker")},
                    reservations:new[]{new ResourceReservation("claim","job","food",Q(1),Q(1,m))});
                var after=ledger.ConsumeThrough("job","claim",Q(1,m-1));
                Require(after.Lots[0].Amount==Q(m-2,m-1)&&after.Reservations[0].RemainingAmount==Q(m-2,m-1),"Intermediate delta overflowed before exact final result."); });
            cases.Add("exact_ledger_wide_claim_sum_compares_before_materialization",()=>{
                var ledger=new WorkLedger(new[]{new ResourceLot("food","unit",Q(1),"plot","worker")},reservations:new[]{
                    new ResourceReservation("a","job","food",Q(1,long.MaxValue)),new ResourceReservation("b","job","food",Q(1,long.MaxValue-1))});
                Require(ledger.Reservations.Count==2,"Representable stored claims falsely rejected.");
                Throws<OverflowException>(()=>ledger.AvailableAmount("food")); });
            cases.Add("exact_ledger_legacy_accessors_never_truncate_fractions",()=>{
                var ledger=ExactLedger().ConsumeThrough("eat","meal",Q(1,3));
                Throws<InvalidOperationException>(()=>{var q=ledger.Lots[0].Quantity;});
                Throws<InvalidOperationException>(()=>{var q=ledger.Reservations[0].Quantity;});
                Throws<InvalidOperationException>(()=>ledger.Available("food")); });
            cases.Add("exact_ledger_invalid_settlement_totals_reject",()=>{
                Throws<ArgumentException>(()=>new ResourceReservation("a","job","lot",Q(0)));
                Throws<ArgumentException>(()=>new ResourceReservation("a","job","lot",Q(1),Q(2,3),Q(2,3)));
                Throws<ArgumentException>(()=>new ResourceReservation("a","job","lot",1,ReservationStatus.Mixed));
                Throws<ArgumentException>(()=>new ResourceReservation("a","job","lot",1,(ReservationStatus)99)); });
            cases.Add("exact_ledger_version2_roundtrip_resumes_partial_and_mixed_settlement",()=>{
                var original=ExactLedger().ConsumeThrough("eat","meal",Q(1,3));var bytes=codec.Encode(original,2);var restored=codec.Decode(bytes,2);
                Require(bytes.SequenceEqual(codec.Encode(restored,2))&&restored.Consume("eat","meal").Lots[0].Amount==Q(1,3),"Partial reservation lost on restore.");
                var mixed=restored.Release("eat","meal");var again=codec.Decode(codec.Encode(mixed,2),2);
                Require(again.Reservations[0].Status==ReservationStatus.Mixed&&again.Lots[0].Amount==Q(2,3)&&again.AvailableAmount("food")==Q(2,3),"Mixed settlement lost on restore."); });
            cases.Add("exact_ledger_version1_encoding_cannot_discard_partial_history",()=>{
                var integralPartial=new WorkLedger(new[]{Lot(quantity:10)},reservations:new[]{Claim("claim",6)}).ConsumeThrough("TEST_ONLY.job","claim",Q(2));
                Require(integralPartial.Lots[0].Quantity==8&&integralPartial.RequiresRationalSchema,"Integral partial settlement was considered legacy-safe.");
                Throws<InvalidDataException>(()=>codec.Encode(integralPartial));Throws<InvalidDataException>(()=>codec.Encode(ExactLedger()));
                var legacy=new WorkLedger(new[]{Lot()},reservations:new[]{Claim("claim")}).Consume("TEST_ONLY.job","claim");
                Require(!legacy.RequiresRationalSchema&&codec.Encode(legacy).SequenceEqual(codec.Encode(codec.Decode(codec.Encode(legacy),1))),"Legacy integer settlement changed."); });
            cases.Add("exact_ledger_explicit_component_version_and_unknown_future_guards",()=>{
                var old=codec.Encode(new WorkLedger());var current=codec.Encode(new WorkLedger(),2);
                Throws<InvalidDataException>(()=>codec.Decode(current,1));Throws<InvalidDataException>(()=>codec.Decode(old,2));
                var future=(byte[])current.Clone();future[4]=3;Resign(future);Throws<InvalidDataException>(()=>codec.Decode(future));
                Throws<ArgumentException>(()=>codec.Encode(new WorkLedger(),3)); });
            cases.Add("exact_ledger_codec_corruption_truncation_and_invalid_quantity_reject",()=>{
                var bytes=codec.Encode(ExactLedger(),2);var corrupt=(byte[])bytes.Clone();corrupt[20]^=1;Throws<InvalidDataException>(()=>codec.Decode(corrupt));
                Throws<InvalidDataException>(()=>codec.Decode(bytes.Take(bytes.Length-1).ToArray()));
                int numeratorAt=12+4+4+4+"food-pound".Length;var bad=(byte[])bytes.Clone();
                for(int i=numeratorAt+8;i<numeratorAt+16;i++)bad[i]=0;Resign(bad);Throws<InvalidDataException>(()=>codec.Decode(bad)); });
            cases.Add("exact_ledger_current_snapshots_require_explicit_new_schema",()=>{
                var s=new Decennium.Foundation.Laboratory.TestOnlyWorkPolicy().Initial();s.Work=ExactLedger();
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(s));
                s.Work=new WorkLedger(new[]{Lot()},reservations:new[]{Claim("claim",6)}).ConsumeThrough("TEST_ONLY.job","claim",Q(2));
                Throws<ArgumentException>(()=>new SnapshotCodec().Encode(s)); });
        }
    }
}
#endif
