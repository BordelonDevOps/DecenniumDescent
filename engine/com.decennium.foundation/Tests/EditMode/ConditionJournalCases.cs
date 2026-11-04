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
        private static ConditionStamp CJAt(long seconds, int phase = 0) => new ConditionStamp(T(seconds), phase);
        private static ConditionApplicationData CJApp(string id, string kind, ConditionStamp? expires = null,
            bool cure = true, bool? inherited = null) => new ConditionApplicationData(id, "owner", "source." + id, kind, expires, "source-end", cure, inheritedCureAllowed: inherited);
        private static ConditionHistoryTransition CJApply(ConditionHistory history, string id, string kind,
            ConditionStamp? expires = null, bool cure = true, bool? inherited = null)
            => history.Append(ConditionOperation.Apply("apply." + id, history.Journal.Now, CJApp(id, kind, expires, cure, inherited), kind == "Unconscious" ? id + ".prone" : ""));
        private static ConditionHistory CJGrant(ConditionHistory history, string id, ConditionStamp? expires, params string[] kinds)
            => history.Append(ConditionOperation.Grant("grant." + id, history.Journal.Now, new ConditionImmunityData(id, "warder", "ward." + id, kinds, expires, "ward-end"))).State;
        private static ConditionHistory CJRestore(ConditionHistory history)
        {
            var codec = new ConditionJournalCodec(); var bytes = codec.Encode(history.Journal);
            var result = ConditionHistory.Restore(codec.Decode(bytes));
            Require(bytes.SequenceEqual(codec.Encode(result.Journal)) && CLSignature(history.Ledger) == CLSignature(result.Ledger), "Condition journal roundtrip changed state or canonical bytes.");
            return result;
        }
        private static long CJHeaderEnd(BinaryReader r)
        {
            r.ReadInt32(); r.ReadInt32(); r.ReadBytes(r.ReadInt32()); r.ReadBytes(r.ReadInt32());
            return r.BaseStream.Position;
        }
        private static int CJPayloadOffset(byte[] bytes)
        {
            using (var stream = new MemoryStream(bytes)) using (var r = new BinaryReader(stream)) {
                CJHeaderEnd(r); stream.Position += 20; r.ReadInt32(); r.ReadBytes(r.ReadInt32()); stream.Position += 24;
                return (int)stream.Position;
            }
        }
        private static void CJCorrupt(byte[] bytes, int offset, byte[] value)
        { Buffer.BlockCopy(value, 0, bytes, offset, value.Length); Resign(bytes); }
        private static void AddConditionJournalCases(Dictionary<string, Action> cases, string directory)
        {
            var codec = new ConditionJournalCodec();
            cases.Add("condition_journal_empty_exact_origin_roundtrips", () => {
                var origin = new EffectClockMarker(new RuleTime(1, 3), 19); var h = CJRestore(new ConditionHistory("target", origin));
                Require(h.Ledger.Now.Equals(origin) && h.Journal.Operations.Count == 0 && h.Ledger.Applications.Count == 0, "Empty journal invented state or rounded origin.");
                var minimal = new ConditionJournal("p", "t"); Require(codec.Encode(minimal).Length == 74 && codec.Decode(codec.Encode(minimal)).Target == "t", "Minimum component envelope rejected.");
            });
            cases.Add("condition_journal_retains_complete_source_payload", () => {
                var a = new ConditionApplicationData("stun", "caster", "feature", "Stunned", new ConditionStamp(new RuleTime(7, 3), 20), "specific-ending", false, 17, long.MaxValue, true);
                var h = new ConditionHistory("target").Append(ConditionOperation.Apply("operation", default, a)).State;
                var saved = CJRestore(h).Ledger.Applications.Single().Application;
                Require(saved.Id == a.Id && saved.Owner == a.Owner && saved.Source == a.Source && saved.Target == "target" && saved.EndingMethod == a.EndingMethod
                    && !saved.GenericCureAllowed && saved.InheritedIncapacitatedCureAllowed && saved.ApplyingDc == 17 && saved.Magnitude == long.MaxValue
                    && saved.Expires.Value.Time == new RuleTime(7, 3) && saved.Expires.Value.Phase == 20, "Source metadata or cure distinction lost.");
            });
            cases.Add("condition_journal_roundtrips_every_operation_and_explicit_ending", () => {
                var h = CJApply(new ConditionHistory("target"), "poison", "Poisoned").State;
                h = CJGrant(h, "ward", CJAt(5), "Poisoned", "Blinded");
                h = h.Append(ConditionOperation.Suppress("suppress", default, "poison", true)).State;
                h = h.Append(ConditionOperation.EndGrant("endward", default, "ward", "dispelled")).State;
                h = h.Append(ConditionOperation.Cure("cure", default, "Blinded")).State;
                h = h.Append(ConditionOperation.End("endpoison", default, "poison", "source-removed")).State;
                h = h.Append(ConditionOperation.Advance("time", CJAt(7))).State; h = CJRestore(h);
                Require(h.Journal.Operations.Select(x => x.Kind).Distinct().Count() == 7 && h.Ledger.Applications.Single().EndedReason == "source-removed"
                    && h.Ledger.Immunities.Single().EndedReason == "dispelled", "Tagged operation or ending lost.");
            });
            cases.Add("condition_journal_same_marker_order_preserves_initial_component_prevention", () => {
                var first = CJGrant(new ConditionHistory("target"), "ward", CJAt(1), "Incapacitated");
                first = CJApply(first, "stun", "Stunned").State;
                var second = CJApply(new ConditionHistory("target"), "stun", "Stunned").State;
                second = CJGrant(second, "ward", CJAt(1), "Incapacitated");
                first = CJRestore(first).Append(ConditionOperation.Advance("later", CJAt(1))).State;
                var resumed = CJRestore(second).Append(ConditionOperation.Advance("later", CJAt(1)));
                Require(!first.Ledger.View().Has(ConditionKind.Incapacitated) && resumed.State.Ledger.View().Has(ConditionKind.Incapacitated)
                    && resumed.Consequences.Single().Kind == ConditionConsequenceKind.EndConcentration, "Same-marker order was sorted or prevention became suppression.");
            });
            cases.Add("condition_journal_retains_prevented_attempt_without_dormant_application", () => {
                var h = CJGrant(new ConditionHistory("target"), "ward", CJAt(1), "Poisoned");
                var attempt = CJApply(h, "poison", "Poisoned"); h = CJRestore(attempt.State);
                Require(attempt.ApplicationPrevented && h.Journal.Operations.Count == 2 && h.Ledger.Applications.Count == 0, "Prevented operation missing or became dormant record.");
                h = h.Append(ConditionOperation.Advance("later", CJAt(2))).State;
                Require(!h.Ledger.View().Has(ConditionKind.Poisoned), "Prevented condition appeared after expiry.");
                Throws<ArgumentException>(() => h.Append(attempt.State.Journal.Operations.Last()));
            });
            cases.Add("condition_journal_restore_then_append_never_reissues_old_onset", () => {
                var application = CJApply(new ConditionHistory("target"), "sleep", "Unconscious", CJAt(5));
                Require(application.Consequences.Count == 3, "Expected drop, fall and concentration onset.");
                var h = CJRestore(application.State);
                var next = h.Append(ConditionOperation.Advance("later", CJAt(1)));
                Require(next.Consequences.Count == 0, "Restore left historical onset pending.");
                var second = CJApply(next.State, "sleep-two", "Unconscious");
                Require(second.Consequences.Count == 2 && second.Consequences.All(x => x.Cause == "sleep-two"), "New onset included old work or replayed concentration transition.");
            });
            cases.Add("condition_journal_cure_suppressed_component_stays_removed_after_restore", () => {
                var h = CJApply(new ConditionHistory("target"), "stun", "Stunned").State;
                h = CJGrant(h, "ward", CJAt(2), "Incapacitated");
                h = h.Append(ConditionOperation.Cure("cure", default, "Incapacitated")).State;
                var next = CJRestore(h).Append(ConditionOperation.Advance("later", CJAt(3)));
                Require(next.State.Ledger.View().Has(ConditionKind.Stunned) && !next.State.Ledger.View().Has(ConditionKind.Incapacitated)
                    && next.Consequences.Count == 0 && next.State.Ledger.Applications.Single().IncapacitatedComponentEndedAt.HasValue, "Cured component regenerated during restore.");
            });
            cases.Add("condition_journal_prone_survives_parent_expiry_and_cure_stays_ended", () => {
                var h = CJApply(new ConditionHistory("target"), "sleep", "Unconscious", CJAt(1)).State;
                h = CJRestore(h).Append(ConditionOperation.Advance("wake", CJAt(2))).State;
                Require(h.Ledger.View().Has(ConditionKind.Prone) && !h.Ledger.View().Has(ConditionKind.Unconscious), "Parent expiry removed posture.");
                h = CJRestore(h).Append(ConditionOperation.Cure("stand", CJAt(2), "Prone")).State;
                Require(!CJRestore(h).Ledger.View().Has(ConditionKind.Prone), "Removed posture revived on restore.");
            });
            cases.Add("condition_journal_fast_forward_preserves_only_new_intermediate_consequences", () => {
                var h = CJApply(new ConditionHistory("target"), "stun", "Stunned", CJAt(3)).State;
                h = CJGrant(h, "ward", CJAt(1), "Incapacitated");
                var next = CJRestore(h).Append(ConditionOperation.Advance("later", CJAt(4)));
                Require(next.Consequences.Count == 1 && next.Consequences[0].At.Time == T(1) && !next.State.Ledger.View().Has(ConditionKind.Incapacitated), "Intermediate state transition lost during advance.");
                var after = CJRestore(next.State).Append(ConditionOperation.Advance("again", CJAt(5)));
                Require(after.Consequences.Count == 0, "Intermediate historical concentration loss replayed.");
            });
            cases.Add("condition_journal_same_fraction_different_phases_survive_restore", () => {
                var h = new ConditionHistory("target", new EffectClockMarker(new RuleTime(1, 3), 10));
                h = CJApply(h, "blind", "Blinded", new ConditionStamp(new RuleTime(1, 3), 20)).State;
                h = CJRestore(h).Append(ConditionOperation.Advance("before", new ConditionStamp(new RuleTime(1, 3), 19))).State;
                Require(h.Ledger.View().Has(ConditionKind.Blinded), "Effect expired at earlier phase.");
                h = CJRestore(h).Append(ConditionOperation.Advance("deadline", new ConditionStamp(new RuleTime(1, 3), 20))).State;
                Require(!CJRestore(h).Ledger.View().Has(ConditionKind.Blinded), "Exact phased expiry lost.");
            });
            cases.Add("condition_journal_duplicate_operation_ids_reject_without_state_change", () => {
                var h = CJApply(new ConditionHistory("target"), "blind", "Blinded").State; var before = codec.Encode(h.Journal);
                Throws<ArgumentException>(() => h.Append(ConditionOperation.Cure("apply.blind", default, "Blinded")));
                Throws<ArgumentException>(() => h.Append(h.Journal.Operations[0]));
                Require(before.SequenceEqual(codec.Encode(h.Journal)), "Rejected operation modified immutable history.");
            });
            cases.Add("condition_journal_chronology_requires_explicit_monotonic_advancement", () => {
                var h = new ConditionHistory("target", CLTime(2, 10));
                Throws<ArgumentException>(() => h.Append(ConditionOperation.Cure("future", CJAt(3), "Blinded")));
                Throws<ArgumentException>(() => h.Append(ConditionOperation.Advance("back", CJAt(2, 9))));
                Throws<ArgumentException>(() => h.Append(ConditionOperation.Advance("backtime", CJAt(1))));
                Throws<ArgumentException>(() => ConditionOperation.Apply("bad", CJAt(2, 10), CJApp("blind", "Blinded", CJAt(2, 10))));
                Require(h.Journal.Operations.Count == 0, "Rejected chronology appended history.");
            });
            cases.Add("condition_journal_policy_and_names_need_semantic_interpreter", () => {
                Throws<ArgumentException>(() => ConditionHistory.Restore(codec.Decode(codec.Encode(new ConditionJournal("future-policy", "target")))));
                foreach (string name in new[] { "1", "blinded", "Bleed", "Frightened" }) {
                    var journal = new ConditionJournal(ConditionHistory.PolicyId, "target", operations: new[] { ConditionOperation.Apply("apply", default, CJApp("effect", name)) });
                    var decoded = codec.Decode(codec.Encode(journal));
                    Throws<ArgumentException>(() => ConditionHistory.Restore(decoded));
                }
            });
            cases.Add("condition_journal_structural_decode_does_not_authorize_invalid_history", () => {
                var invalid = new ConditionJournal(ConditionHistory.PolicyId, "target", operations: new[] { ConditionOperation.End("end", default, "missing", "ended") });
                Throws<ArgumentException>(() => ConditionHistory.Restore(codec.Decode(codec.Encode(invalid))));
                var a = ConditionOperation.Apply("one", default, CJApp("effect", "Blinded"));
                var b = ConditionOperation.Apply("two", default, CJApp("effect", "Poisoned"));
                invalid = new ConditionJournal(ConditionHistory.PolicyId, "target", operations: new[] { a, b });
                Throws<ArgumentException>(() => ConditionHistory.Restore(codec.Decode(codec.Encode(invalid))));
                var h = new ConditionHistory("target");
                Throws<ArgumentException>(() => h.Append(ConditionOperation.Apply("sleep", default, CJApp("effect", "Unconscious"))));
                Throws<ArgumentException>(() => h.Append(ConditionOperation.Apply("bad", default, CJApp("effect", "Blinded", inherited: true))));
                Require(h.Journal.Operations.Count == 0 && h.Ledger.Applications.Count == 0, "Failed semantics mutated state.");
            });
            cases.Add("condition_journal_input_collections_are_detached_and_bounded", () => {
                var kinds = new[] { "Poisoned", "Blinded" }; var immunity = new ConditionImmunityData("ward", "owner", "source", kinds, null, "end");
                var ops = new[] { ConditionOperation.Grant("grant", default, immunity) }; var j = new ConditionJournal(ConditionHistory.PolicyId, "target", operations: ops);
                kinds[0] = "Unconscious"; ops[0] = ConditionOperation.Advance("other", CJAt(1));
                Require(j.Operations[0].Kind == ConditionOperationKind.GrantImmunity && immunity.Kinds.SequenceEqual(new[] { "Blinded", "Poisoned" }), "Caller changed retained arrays.");
                Throws<ArgumentException>(() => new ConditionImmunityData("ward", "owner", "source", new[] { "Blinded", "Blinded" }, null, "end"));
                Throws<ArgumentException>(() => new ConditionImmunityData("ward", "owner", "source", Enumerable.Range(0, 15).Select(x => "kind" + x), null, "end"));
                Throws<ArgumentException>(() => new ConditionJournal("policy", "target", operations: new ConditionOperation[] { null }));
                Throws<ArgumentException>(() => new ConditionApplicationData("app", "owner", "source", "Blinded", null, "end", true, -1));
            });
            cases.Add("condition_journal_operation_capacity_is_atomic_without_eviction", () => {
                var h = new ConditionHistory("target");
                for (int i = 0; i < ConditionJournal.MaxOperations; i++) h = h.Append(ConditionOperation.Advance("time." + i, CJAt(i))).State;
                h = CJRestore(h); var before = codec.Encode(h.Journal);
                Throws<InvalidOperationException>(() => h.Append(ConditionOperation.Advance("overflow", CJAt(512))));
                Require(h.Journal.Operations.Count == 512 && before.SequenceEqual(codec.Encode(h.Journal)), "Capacity silently evicted history or advanced state.");
                Throws<ArgumentException>(() => new ConditionJournal("policy", "target", operations: h.Journal.Operations.Concat(new[] { ConditionOperation.Advance("overflow", CJAt(512)) })));
            });
            cases.Add("condition_journal_ledger_capacity_failure_does_not_append_operation", () => {
                var h = new ConditionHistory("target");
                for (int i = 0; i < 128; i++) h = CJApply(h, "effect" + i, "Blinded").State;
                h = CJRestore(h); byte[] before = codec.Encode(h.Journal);
                Throws<InvalidOperationException>(() => CJApply(h, "overflow", "Poisoned"));
                Require(before.SequenceEqual(codec.Encode(h.Journal)) && h.Journal.Operations.Count == 128, "Ledger overflow retained rejected operation.");
            });
            cases.Add("condition_journal_structural_maximum_fits_component_envelope", () => {
                string Long(string prefix) => prefix.PadRight(96, 'x');
                var operations = Enumerable.Range(0, 512).Select(i => ConditionOperation.Grant(Long("op" + i), default,
                    new ConditionImmunityData(Long("grant" + i), Long("owner"), Long("source"), Enumerable.Range(0, 14).Select(k => Long("kind" + k)),
                        new ConditionStamp(new RuleTime(long.MaxValue), int.MaxValue), Long("end")))).ToArray();
                var journal = new ConditionJournal(Long("policy"), Long("target"), operations: operations); byte[] bytes = codec.Encode(journal);
                Require(bytes.Length < ConditionJournalCodec.MaxBytes && codec.Encode(codec.Decode(bytes)).SequenceEqual(bytes), "Maximum structural component cannot be saved.");
                File.WriteAllBytes(Path.Combine(directory, "maximum-condition-journal.bin"), bytes);
                // Structural maximum is intentionally not semantically admitted: this is an envelope check.
            });
            cases.Add("condition_journal_corruption_truncation_and_version_rejected", () => {
                var bytes = codec.Encode(new ConditionHistory("target").Journal); var corrupt = bytes.ToArray(); corrupt[0] ^= 1;
                Throws<InvalidDataException>(() => codec.Decode(corrupt));
                Throws<InvalidDataException>(() => codec.Decode(bytes.Take(bytes.Length - 1).ToArray()));
                Throws<InvalidDataException>(() => codec.Decode(new byte[ConditionJournalCodec.MaxBytes + 1]));
                corrupt = bytes.ToArray(); CJCorrupt(corrupt, 4, BitConverter.GetBytes(2)); Throws<InvalidDataException>(() => codec.Decode(corrupt));
                corrupt = bytes.ToArray(); CJCorrupt(corrupt, 0, BitConverter.GetBytes(0)); Throws<InvalidDataException>(() => codec.Decode(corrupt));
                corrupt = bytes.Take(bytes.Length - 32).Concat(new byte[] { 99 }).Concat(new byte[32]).ToArray(); Resign(corrupt);
                Throws<InvalidDataException>(() => codec.Decode(corrupt));
            });
            cases.Add("condition_journal_noncanonical_time_and_bad_phase_rejected", () => {
                var bytes = codec.Encode(new ConditionJournal("policy", "target", new ConditionStamp(new RuleTime(1, 3))));
                int offset; using (var r = new BinaryReader(new MemoryStream(bytes))) offset = (int)CJHeaderEnd(r);
                var corrupt = bytes.ToArray(); CJCorrupt(corrupt, offset, BitConverter.GetBytes(2L)); CJCorrupt(corrupt, offset + 8, BitConverter.GetBytes(6L));
                Throws<InvalidDataException>(() => codec.Decode(corrupt));
                foreach (long denominator in new[] { 0L, -1L }) { corrupt = bytes.ToArray(); CJCorrupt(corrupt, offset + 8, BitConverter.GetBytes(denominator)); Throws<InvalidDataException>(() => codec.Decode(corrupt)); }
                corrupt = bytes.ToArray(); CJCorrupt(corrupt, offset + 16, BitConverter.GetBytes(-1)); Throws<InvalidDataException>(() => codec.Decode(corrupt));
                corrupt = bytes.ToArray(); CJCorrupt(corrupt, offset + 20, BitConverter.GetBytes(513)); Throws<InvalidDataException>(() => codec.Decode(corrupt));
            });
            cases.Add("condition_journal_invalid_operation_tag_boolean_and_utf8_rejected", () => {
                var h = CJApply(new ConditionHistory("target"), "blind", "Blinded").State; var bytes = codec.Encode(h.Journal);
                int payload = CJPayloadOffset(bytes); var corrupt = bytes.ToArray(); CJCorrupt(corrupt, payload - 4, BitConverter.GetBytes(99));
                Throws<InvalidDataException>(() => codec.Decode(corrupt));
                using (var r = new BinaryReader(new MemoryStream(bytes))) {
                    r.BaseStream.Position = payload;
                    for (int i = 0; i < 4; i++) r.ReadBytes(r.ReadInt32());
                    int flag = (int)r.BaseStream.Position; corrupt = bytes.ToArray(); CJCorrupt(corrupt, flag, new byte[] { 2 }); Throws<InvalidDataException>(() => codec.Decode(corrupt));
                    r.ReadByte(); r.ReadBytes(r.ReadInt32()); flag = (int)r.BaseStream.Position;
                    corrupt = bytes.ToArray(); CJCorrupt(corrupt, flag, new byte[] { 2 }); Throws<InvalidDataException>(() => codec.Decode(corrupt));
                }
                corrupt = bytes.ToArray(); CJCorrupt(corrupt, 12, new byte[] { 255 }); Throws<InvalidDataException>(() => codec.Decode(corrupt));
                corrupt = bytes.ToArray(); CJCorrupt(corrupt, 8, BitConverter.GetBytes(97)); Throws<InvalidDataException>(() => codec.Decode(corrupt));
            });
            cases.Add("condition_journal_disk_component_resume_keeps_independent_posture", () => {
                var h = CJApply(new ConditionHistory("target"), "sleep", "Unconscious", CJAt(1)).State;
                string path = Path.Combine(directory, "condition-component.bin"); File.WriteAllBytes(path, codec.Encode(h.Journal));
                var restored = ConditionHistory.Restore(codec.Decode(File.ReadAllBytes(path)));
                var next = restored.Append(ConditionOperation.Advance("wake", CJAt(2)));
                Require(next.Consequences.Count == 0 && next.State.Ledger.View().Has(ConditionKind.Prone) && !next.State.Ledger.View().Has(ConditionKind.Unconscious), "Disk component resume repeated fall or lost posture.");
            });
            cases.Add("condition_journal_256_parent_component_states_roundtrip_each_operation", () => {
                int sampled = 0;
                foreach (string parent in new[] { "Stunned", "Paralyzed", "Petrified", "Unconscious" })
                    for (int flags = 0; flags < 64; flags++) {
                        var h = new ConditionHistory("target");
                        if ((flags & 1) != 0) h = CJRestore(CJGrant(h, "initial", CJAt(2), "Incapacitated"));
                        if ((flags & 2) != 0) h = CJRestore(CJGrant(h, "prone", CJAt(2), "Prone"));
                        h = CJRestore(CJApply(h, "parent", parent, CJAt(4)).State);
                        if ((flags & 4) != 0) h = CJRestore(CJGrant(h, "later", CJAt(2), "Incapacitated"));
                        if ((flags & 8) != 0) h = CJRestore(h.Append(ConditionOperation.Suppress("suppress", default, "parent", true)).State);
                        if ((flags & 16) != 0) h = CJRestore(h.Append(ConditionOperation.Cure("cure-component", default, "Incapacitated")).State);
                        if ((flags & 32) != 0) h = CJRestore(h.Append(ConditionOperation.Cure("cure-parent", default, parent)).State);
                        h = CJRestore(h.Append(ConditionOperation.Advance("advance", CJAt(3))).State);
                        bool expectedParent = (flags & (8 | 32)) == 0;
                        Require(h.Ledger.View().Has((ConditionKind)Enum.Parse(typeof(ConditionKind), parent)) == expectedParent
                            && h.Ledger.View().Has(ConditionKind.Incapacitated) == (expectedParent && (flags & (1 | 16)) == 0)
                            && h.Ledger.View().Has(ConditionKind.Prone) == (parent == "Unconscious" && (flags & 2) == 0), "Saved component state disagrees with independent admission/cure expectations.");
                        sampled++;
                    }
                Require(sampled == 256, "Incomplete parent-component persistence grid.");
            });
        }
    }
}
#endif
