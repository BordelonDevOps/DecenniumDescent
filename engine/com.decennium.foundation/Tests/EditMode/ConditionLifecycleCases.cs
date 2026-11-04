#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static EffectClockMarker CLTime(long seconds, int phase = 0) => new EffectClockMarker(T(seconds), phase);
        private static ConditionApplication CLApp(ConditionLedger state, string id, ConditionKind kind,
            EffectClockMarker? expires = null, bool cure = true, string owner = "owner", int? dc = null,
            long? magnitude = null, bool? componentCure = null)
            => new ConditionApplication(id, owner, "source." + id, state.Target, kind, state.Now, expires,
                "source-expiry-or-cure", cure, dc, magnitude, componentCure);
        private static ConditionTransition CLApply(ConditionLedger state, string id, ConditionKind kind,
            EffectClockMarker? expires = null, bool cure = true, bool? componentCure = null)
            => state.Apply(CLApp(state, id, kind, expires, cure, componentCure: componentCure), kind == ConditionKind.Unconscious ? id + ".prone" : "");
        private static ConditionLedger CLImmune(ConditionLedger state, string id, ConditionKind[] kinds, EffectClockMarker? expires = null)
            => state.GrantImmunity(new ConditionImmunity(id, "protector", "immunity." + id, state.Target, kinds,
                state.Now, expires, "source-expiry-or-removal")).State;
        private static bool CLEvent(ConditionTransition transition, ConditionConsequenceKind kind)
            => transition.Consequences.Any(x => x.Kind == kind);
        private static string CLSignature(ConditionLedger state) => state.Now.Time + ":" + state.Now.Phase + "|"
            + string.Join(";", state.Applications.Select(x => x.Id + ":" + x.Present(state.Now) + ":" + x.Suppressed + ":"
                + x.EndedAt?.Time + ":" + x.EndedAt?.Phase + ":" + x.EndedReason + ":" + x.IncapacitatedPreventedAtAdmission + ":"
                + x.IncapacitatedComponentEndedAt?.Time + ":" + x.IncapacitatedComponentEndedAt?.Phase + ":" + x.ProneOnsetPrevented))
            + "|" + string.Join(";", state.Immunities.Select(x => x.Grant.Id + ":" + x.Present(state.Now) + ":" + x.EndedAt?.Time + ":" + x.EndedAt?.Phase))
            + "|" + string.Join(";", state.View().Components.Select(x => x.ApplicationId + ":" + x.Kind + ":" + x.Inherited));
        private static void AddConditionLifecycleCases(Dictionary<string, Action> cases)
        {
            cases.Add("condition_lifecycle_retains_independent_provenance_without_stacking_penalties", () => {
                var original = new ConditionLedger("target");
                var a = CLApp(original, "a", ConditionKind.Poisoned, CLTime(5), owner: "one", dc: 13, magnitude: 2);
                var state = original.Apply(a).State;
                state = state.Apply(CLApp(state, "b", ConditionKind.Poisoned, CLTime(8), owner: "two", dc: 17, magnitude: 4)).State;
                Require(original.Applications.Count == 0 && state.Applications.Count == 2 && state.Applications[0].Application == a
                    && a.Owner == "one" && a.ApplyingDc == 13 && a.Magnitude == 2 && a.Source == "source.a", "Source provenance lost or old state mutated.");
                Require(state.View().Sources(ConditionKind.Poisoned).SequenceEqual(new[] { "a", "b" })
                    && PlaytestConditions.Attack(state.View().Clauses, C()).RollMode == D20Selection.Disadvantage, "Independent sources duplicated dice or merged identity.");
                state = state.AdvanceTo(CLTime(5)).State;
                Require(state.View().Sources(ConditionKind.Poisoned).SequenceEqual(new[] { "b" }), "First expiry removed independent source.");
            });
            cases.Add("condition_lifecycle_records_and_query_collections_are_detached", () => {
                var kinds = new[] { ConditionKind.Blinded }; var initial = new ConditionLedger("target");
                var grant = new ConditionImmunity("i", "owner", "source", "target", kinds, initial.Now, null, "removal");
                kinds[0] = ConditionKind.Poisoned; var state = initial.GrantImmunity(grant).State;
                Require(state.ImmuneTo(ConditionKind.Blinded) && !state.ImmuneTo(ConditionKind.Poisoned), "Immunity retained caller array.");
                Throws<NotSupportedException>(() => ((IList<ConditionKind>)grant.Kinds)[0] = ConditionKind.Dazed);
                Throws<NotSupportedException>(() => ((IList<ConditionImmunityInstance>)state.Immunities).Clear());
                state = CLApply(state, "p", ConditionKind.Poisoned).State;
                Throws<NotSupportedException>(() => ((IList<ConditionInstance>)state.Applications).Clear());
                Throws<NotSupportedException>(() => ((IList<ResolvedConditionComponent>)state.View().Components).Clear());
                Throws<NotSupportedException>(() => ((IList<string>)state.View().Sources(ConditionKind.Poisoned)).Clear());
            });
            cases.Add("condition_lifecycle_invalid_source_metadata_is_rejected", () => {
                var s = new ConditionLedger("target");
                Throws<ArgumentException>(() => new ConditionLedger("bad target"));
                Throws<ArgumentException>(() => CLApp(s, "", ConditionKind.Blinded));
                Throws<ArgumentException>(() => CLApp(s, "a", (ConditionKind)14));
                Throws<ArgumentException>(() => CLApp(s, "a", ConditionKind.Blinded, CLTime(0)));
                Throws<ArgumentException>(() => CLApp(s, "a", ConditionKind.Blinded, dc: -1));
                Throws<ArgumentException>(() => CLApp(s, "a", ConditionKind.Blinded, magnitude: -1));
                Throws<ArgumentException>(() => CLApp(s, "a", ConditionKind.Blinded, componentCure: true));
                Throws<ArgumentException>(() => new ConditionApplication("a", "o", "s", "target", ConditionKind.Blinded, s.Now, null, "", true));
                Require(CLApp(s, "valid", ConditionKind.Blinded, dc: 0, magnitude: long.MaxValue).Magnitude == long.MaxValue, "Valid explicit numeric boundary rejected.");
            });
            cases.Add("condition_lifecycle_invalid_immunity_sets_and_endpoints_reject", () => {
                ConditionImmunity Grant(ConditionKind[] kinds, EffectClockMarker? expires = null) => new ConditionImmunity("i", "o", "s", "target", kinds, default, expires, "end");
                Throws<ArgumentException>(() => Grant(null)); Throws<ArgumentException>(() => Grant(Array.Empty<ConditionKind>()));
                Throws<ArgumentException>(() => Grant(new[] { ConditionKind.Prone, ConditionKind.Prone }));
                Throws<ArgumentException>(() => Grant(new[] { (ConditionKind)99 }));
                Throws<ArgumentException>(() => Grant(new[] { ConditionKind.Blinded }, CLTime(0)));
                Require(Grant((ConditionKind[])Enum.GetValues(typeof(ConditionKind))).Kinds.Count == 14, "Full admitted immunity set rejected.");
            });
            cases.Add("condition_lifecycle_requires_current_marker_target_and_unique_id", () => {
                var s = new ConditionLedger("target", CLTime(1)); string before = CLSignature(s);
                Throws<ArgumentException>(() => s.Apply(new ConditionApplication("a", "o", "s", "other", ConditionKind.Blinded, s.Now, null, "end", true)));
                Throws<ArgumentException>(() => s.Apply(new ConditionApplication("a", "o", "s", "target", ConditionKind.Blinded, CLTime(2), null, "end", true)));
                Throws<ArgumentException>(() => s.Apply(null));
                Throws<ArgumentException>(() => s.Apply(CLApp(s, "a", ConditionKind.Blinded), "stray-onset"));
                Throws<ArgumentException>(() => s.Apply(CLApp(s, "a", ConditionKind.Unconscious)));
                Throws<ArgumentException>(() => s.Apply(CLApp(s, "a", ConditionKind.Unconscious), "a"));
                Require(before == CLSignature(s), "Invalid application mutated source state.");
                s = CLApply(s, "a", ConditionKind.Blinded).State;
                Throws<ArgumentException>(() => CLApply(s, "a", ConditionKind.Poisoned));
                Throws<ArgumentException>(() => CLImmune(s, "a", new[] { ConditionKind.Poisoned }));
                s = s.Cure(ConditionKind.Blinded).State;
                Throws<ArgumentException>(() => CLApply(s, "a", ConditionKind.Blinded));
            });
            cases.Add("condition_lifecycle_initial_parent_immunity_prevents_application_and_onset", () => {
                var s = CLImmune(new ConditionLedger("target"), "i", new[] { ConditionKind.Unconscious }, CLTime(2));
                var blocked = CLApply(s, "sleep", ConditionKind.Unconscious, CLTime(4));
                Require(blocked.ApplicationPrevented && ReferenceEquals(s, blocked.State) && blocked.Consequences.Count == 0 && s.Applications.Count == 0, "Prevented effect left a dormant source or onset.");
                var later = s.AdvanceTo(CLTime(3));
                Require(!later.State.View().Has(ConditionKind.Unconscious) && later.Consequences.Count == 0, "Initially prevented application appeared after immunity.");
            });
            cases.Add("condition_lifecycle_initial_inherited_immunity_permanently_prevents_component", () => {
                foreach (var parent in new[] { ConditionKind.Paralyzed, ConditionKind.Petrified, ConditionKind.Stunned, ConditionKind.Unconscious }) {
                    var s = CLImmune(new ConditionLedger("target"), "i", new[] { ConditionKind.Incapacitated }, CLTime(1));
                    var change = CLApply(s, "parent", parent, CLTime(5)); s = change.State;
                    Require(s.Applications[0].IncapacitatedPreventedAtAdmission && !s.View().Has(ConditionKind.Incapacitated)
                        && !CLEvent(change, ConditionConsequenceKind.EndConcentration), "Inherited component was admitted through initial immunity.");
                    s = s.AdvanceTo(CLTime(2)).State;
                    Require(s.View().Has(parent) && !s.View().Has(ConditionKind.Incapacitated)
                        && PlaytestConditions.Permissions(s.View().Clauses).Action && !PlaytestConditions.Permissions(s.View().Clauses).VoluntarySpeed,
                        "Parent inference regenerated prevented Incapacitated or erased immobility.");
                    Require(s.View().AutomaticStrengthDexterityFailure && PlaytestConditions.Attack(C(), s.View().Clauses).AdvantagePresent, "Parent direct clauses erased.");
                    change = CLApply(s, "new", parent, CLTime(6));
                    Require(change.State.View().Has(ConditionKind.Incapacitated) && CLEvent(change, ConditionConsequenceKind.EndConcentration), "New application failed to reevaluate ended immunity.");
                }
            });
            cases.Add("condition_lifecycle_acquired_component_immunity_preserves_parent_constraints", () => {
                var s = CLApply(new ConditionLedger("target"), "stun", ConditionKind.Stunned, CLTime(5)).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Incapacitated }, CLTime(2));
                var view = s.View(); var permission = PlaytestConditions.Permissions(view.Clauses);
                Require(view.Has(ConditionKind.Stunned) && !view.Has(ConditionKind.Incapacitated) && permission.Action && permission.Reaction
                    && !permission.VoluntarySpeed && view.SpeechOnlyFaltering && view.AutomaticStrengthDexterityFailure, "Component immunity removed parent restrictions or retained Incapacitated.");
                Require(PlaytestConditions.EffectiveSpeed(30, 10, view.Clauses) == 0, "Suppressed Incapacitated restored Stunned movement.");
                var resumed = s.AdvanceTo(CLTime(2));
                Require(resumed.State.View().Has(ConditionKind.Incapacitated) && CLEvent(resumed, ConditionConsequenceKind.EndConcentration), "Admitted component failed to resume.");
            });
            cases.Add("condition_lifecycle_parent_immunity_suppresses_all_ongoing_parent_clauses", () => {
                var s = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious, CLTime(5)).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Unconscious }, CLTime(2));
                Require(!s.View().Has(ConditionKind.Unconscious) && !s.View().Has(ConditionKind.Incapacitated)
                    && s.View().Has(ConditionKind.Prone) && s.Applications.All(x => x.Present(s.Now)), "Parent immunity reversed completed Prone or failed to suppress parent.");
                var resumed = s.AdvanceTo(CLTime(2));
                Require(resumed.Consequences.Count == 1 && resumed.Consequences[0].Kind == ConditionConsequenceKind.EndConcentration,
                    "Resuming parent replayed drop/fall rather than concentration state constraint.");
            });
            cases.Add("condition_lifecycle_expiry_continues_under_suppression_and_never_restarts", () => {
                var s = CLApply(new ConditionLedger("target"), "stun", ConditionKind.Stunned, CLTime(2)).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Stunned }, CLTime(5));
                var later = s.AdvanceTo(CLTime(6));
                Require(later.State.Applications[0].EndedAt.Value.Equals(CLTime(2)) && later.State.Applications[0].EndedReason == "expired"
                    && !later.State.View().Has(ConditionKind.Stunned) && later.Consequences.Count == 0, "Suppression paused expiry or resurrected effect.");
                Throws<ArgumentException>(() => later.State.SuppressApplication("stun", false));
            });
            cases.Add("condition_lifecycle_generic_cure_removes_all_eligible_present_sources", () => {
                var s = CLApply(new ConditionLedger("target"), "a", ConditionKind.Blinded).State;
                s = CLApply(s, "b", ConditionKind.Blinded).State; s = CLApply(s, "protected", ConditionKind.Blinded, cure: false).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Blinded }); s = s.Cure(ConditionKind.Blinded).State;
                Require(!s.Applications[0].Present(s.Now) && !s.Applications[1].Present(s.Now) && s.Applications[2].Present(s.Now), "Suppression blocked cure or cure ignored protected source.");
                s = s.EndImmunity("i", "ended").State;
                Require(s.View().Sources(ConditionKind.Blinded).SequenceEqual(new[] { "protected" }), "Cured sources resumed.");
            });
            cases.Add("condition_lifecycle_curing_inherited_component_preserves_parent_and_endpoint", () => {
                var s = CLApply(new ConditionLedger("target"), "stun", ConditionKind.Stunned, CLTime(5)).State;
                s = s.AdvanceTo(CLTime(1)).State; s = s.Cure(ConditionKind.Incapacitated).State;
                Require(s.Applications[0].IncapacitatedComponentEndedAt.Value.Equals(CLTime(1)) && !s.Applications[0].IncapacitatedPreventedAtAdmission
                    && s.View().Has(ConditionKind.Stunned) && !s.View().Has(ConditionKind.Incapacitated)
                    && s.Applications[0].Application.Expires.Value.Equals(CLTime(5)), "Component cure erased parent, changed duration or conflated admission prevention.");
                s = CLImmune(s, "i", new[] { ConditionKind.Stunned }, CLTime(2));
                var later = s.AdvanceTo(CLTime(3));
                Require(later.State.View().Has(ConditionKind.Stunned) && !later.State.View().Has(ConditionKind.Incapacitated)
                    && later.Consequences.Count == 0, "Projection regenerated cured inherited component.");
            });
            cases.Add("condition_lifecycle_component_cure_reaches_suppressed_and_independent_sources", () => {
                var s = CLApply(new ConditionLedger("target"), "stun", ConditionKind.Stunned).State;
                s = CLApply(s, "paralysis", ConditionKind.Paralyzed).State; s = CLApply(s, "incap", ConditionKind.Incapacitated).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Incapacitated, ConditionKind.Stunned, ConditionKind.Paralyzed });
                s = s.Cure(ConditionKind.Incapacitated).State; s = s.EndImmunity("i", "ended").State;
                Require(s.View().Has(ConditionKind.Stunned) && s.View().Has(ConditionKind.Paralyzed) && !s.View().Has(ConditionKind.Incapacitated)
                    && !s.Applications.Single(x => x.Id == "incap").Present(s.Now), "Generic component cure missed suppressed parent or independent record.");
            });
            cases.Add("condition_lifecycle_parent_and_component_cure_exceptions_are_independent", () => {
                var s = CLApply(new ConditionLedger("target"), "parent-protected", ConditionKind.Stunned, cure: false, componentCure: true).State;
                s = CLApply(s, "component-protected", ConditionKind.Paralyzed, cure: true, componentCure: false).State;
                s = s.Cure(ConditionKind.Incapacitated).State;
                Require(s.View().Sources(ConditionKind.Incapacitated).SequenceEqual(new[] { "component-protected" }), "Parent cure eligibility substituted for component eligibility.");
                s = s.Cure(ConditionKind.Stunned).State; s = s.Cure(ConditionKind.Paralyzed).State;
                Require(s.View().Has(ConditionKind.Stunned) && !s.View().Has(ConditionKind.Paralyzed) && !s.View().Has(ConditionKind.Incapacitated), "Component exception prevented parent removal or removed protected parent.");
            });
            cases.Add("condition_lifecycle_selected_ending_removes_only_one_application", () => {
                var s = CLApply(new ConditionLedger("target"), "a", ConditionKind.Poisoned).State;
                s = CLApply(s, "b", ConditionKind.Poisoned).State; s = s.EndApplication("a", "selected-save-success").State;
                Require(s.View().Sources(ConditionKind.Poisoned).SequenceEqual(new[] { "b" }) && s.Applications[0].EndedReason == "selected-save-success", "Specific ending became all-source cure.");
                Throws<ArgumentException>(() => s.EndApplication("a", "again")); Throws<ArgumentException>(() => s.EndApplication("missing", "end"));
                Throws<ArgumentException>(() => s.EndApplication("b", ""));
            });
            cases.Add("condition_lifecycle_source_suppression_retains_deadline_and_allows_cure", () => {
                var s = CLApply(new ConditionLedger("target"), "p", ConditionKind.Poisoned, CLTime(5)).State;
                var suppressed = s.SuppressApplication("p", true); s = suppressed.State;
                Require(s.Applications[0].Present(s.Now) && !s.View().Has(ConditionKind.Poisoned) && s.Applications[0].Application.Expires.Value.Equals(CLTime(5)), "Source suppression ended or delayed condition.");
                s = s.Cure(ConditionKind.Poisoned).State;
                Throws<ArgumentException>(() => s.SuppressApplication("p", false));
            });
            cases.Add("condition_lifecycle_unconscious_onset_issues_separate_persistent_prone", () => {
                var change = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious, CLTime(2)); var s = change.State;
                Require(change.Consequences.Select(x => x.Kind).SequenceEqual(new[] { ConditionConsequenceKind.DropHeldItems, ConditionConsequenceKind.FallProne, ConditionConsequenceKind.EndConcentration })
                    && s.Applications[0].DropHeldOnsetIssued && s.Applications[0].ProneOnsetIssued, "Initial Unconscious outcomes not settled once.");
                var child = s.Applications.Single(x => x.Application.Kind == ConditionKind.Prone);
                Require(child.ParentApplicationId == "sleep" && !child.Application.Expires.HasValue && child.Application.EndingMethod == "stand-or-explicit-cure", "Prone inherited parent's expiry.");
                s = s.AdvanceTo(CLTime(3)).State;
                Require(!s.View().Has(ConditionKind.Unconscious) && s.View().Has(ConditionKind.Prone), "Parent expiry stood creature.");
            });
            cases.Add("condition_lifecycle_initial_prone_immunity_settles_prevented_fall", () => {
                var s = CLImmune(new ConditionLedger("target"), "i", new[] { ConditionKind.Prone }, CLTime(1));
                var change = CLApply(s, "sleep", ConditionKind.Unconscious, CLTime(5)); s = change.State;
                Require(s.Applications.Count == 1 && s.Applications[0].ProneOnsetPrevented && !s.Applications[0].ProneOnsetIssued
                    && CLEvent(change, ConditionConsequenceKind.DropHeldItems) && !CLEvent(change, ConditionConsequenceKind.FallProne), "Prone immunity blocked parent or retained delayed fall.");
                change = s.AdvanceTo(CLTime(2));
                Require(!change.State.View().Has(ConditionKind.Prone) && change.State.View().Has(ConditionKind.Unconscious) && change.Consequences.Count == 0, "Immunity ending replayed prevented onset.");
            });
            cases.Add("condition_lifecycle_existing_prone_resumes_without_new_fall", () => {
                var s = CLApply(new ConditionLedger("target"), "prone", ConditionKind.Prone).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Prone }, CLTime(1));
                Require(!s.View().Has(ConditionKind.Prone) && s.Applications[0].Present(s.Now), "Immunity removed existing posture record.");
                var later = s.AdvanceTo(CLTime(2));
                Require(later.State.View().Has(ConditionKind.Prone) && later.Consequences.Count == 0, "Existing Prone did not resume quietly.");
            });
            cases.Add("condition_lifecycle_direct_prone_application_issues_one_fall", () => {
                var change = CLApply(new ConditionLedger("target"), "trip", ConditionKind.Prone);
                Require(change.Consequences.Count == 1 && change.Consequences[0].Kind == ConditionConsequenceKind.FallProne
                    && change.State.Applications[0].ProneOnsetIssued && !change.State.Applications[0].DropHeldOnsetIssued,
                    "Direct Prone failed to emit its physical consequence or dropped held items.");
                var s = CLImmune(new ConditionLedger("target"), "i", new[] { ConditionKind.Prone });
                var blocked = CLApply(s, "trip", ConditionKind.Prone);
                Require(blocked.ApplicationPrevented && blocked.Consequences.Count == 0, "Prevented trip still emitted fall.");
            });
            cases.Add("condition_lifecycle_new_independent_unconscious_application_resolves_own_onset", () => {
                var s = CLApply(new ConditionLedger("target"), "a", ConditionKind.Unconscious).State;
                var second = CLApply(s, "b", ConditionKind.Unconscious); s = second.State;
                Require(second.Consequences.Count == 2 && CLEvent(second, ConditionConsequenceKind.DropHeldItems) && CLEvent(second, ConditionConsequenceKind.FallProne)
                    && !CLEvent(second, ConditionConsequenceKind.EndConcentration), "New source repeated aggregate concentration transition or omitted its onset.");
                Require(s.View().Sources(ConditionKind.Prone).Count == 2 && s.View().Clauses.Active.Count(x => x == ConditionClause.Prone) == 1, "Independent posture causes stacked penalty.");
                Throws<ArgumentException>(() => CLApply(s, "b", ConditionKind.Unconscious));
            });
            cases.Add("condition_lifecycle_curing_prone_does_not_end_or_retrigger_unconscious", () => {
                var s = CLApply(new ConditionLedger("target"), "a", ConditionKind.Unconscious).State;
                s = s.Cure(ConditionKind.Prone).State;
                Require(s.View().Has(ConditionKind.Unconscious) && !s.View().Has(ConditionKind.Prone), "Curing posture cleared parent or immediately regenerated posture.");
                var later = s.AdvanceTo(CLTime(4));
                Require(later.Consequences.Count == 0 && !later.State.View().Has(ConditionKind.Prone), "Passive time replayed onset.");
                var fresh = CLApply(later.State, "new", ConditionKind.Unconscious);
                Require(fresh.State.View().Has(ConditionKind.Prone) && CLEvent(fresh, ConditionConsequenceKind.FallProne), "New actual application could not cause fresh posture.");
            });
            cases.Add("condition_lifecycle_curing_parent_does_not_remove_its_prone_consequence", () => {
                var s = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious).State;
                s = s.Cure(ConditionKind.Unconscious).State;
                Require(!s.View().Has(ConditionKind.Unconscious) && s.View().Has(ConditionKind.Prone)
                    && !s.Applications[0].Present(s.Now) && s.Applications[1].Present(s.Now), "Parent cure cascaded into completed posture.");
            });
            cases.Add("condition_lifecycle_petrified_suppresses_existing_poison_with_provenance", () => {
                var s = CLApply(new ConditionLedger("target"), "poison", ConditionKind.Poisoned, CLTime(8)).State;
                s = CLApply(s, "stone", ConditionKind.Petrified, CLTime(3)).State;
                Require(s.ImmunitySources(ConditionKind.Poisoned).SequenceEqual(new[] { "stone" }) && !s.View().Has(ConditionKind.Poisoned)
                    && s.Applications[0].Present(s.Now), "Petrified lost grant provenance or removed existing poison.");
                s = s.AdvanceTo(CLTime(4)).State;
                Require(s.View().Has(ConditionKind.Poisoned) && !s.ImmuneTo(ConditionKind.Poisoned), "Existing poison failed to resume.");
            });
            cases.Add("condition_lifecycle_petrified_prevents_new_poison_without_dormant_record", () => {
                var s = CLApply(new ConditionLedger("target"), "stone", ConditionKind.Petrified, CLTime(2)).State;
                var blocked = CLApply(s, "poison", ConditionKind.Poisoned, CLTime(8));
                Require(blocked.ApplicationPrevented && blocked.State.Applications.Count == 1, "New poison admitted through Petrified.");
                s = blocked.State.AdvanceTo(CLTime(3)).State;
                Require(!s.View().Has(ConditionKind.Poisoned), "Prevented poison appeared after stone ended.");
            });
            cases.Add("condition_lifecycle_petrified_component_removal_keeps_poison_protection", () => {
                var s = CLApply(new ConditionLedger("target"), "stone", ConditionKind.Petrified).State;
                s = s.Cure(ConditionKind.Incapacitated).State;
                Require(s.View().Has(ConditionKind.Petrified) && !s.View().Has(ConditionKind.Incapacitated) && s.ImmuneTo(ConditionKind.Poisoned), "Curing component removed unrelated parent immunity.");
            });
            cases.Add("condition_lifecycle_petrified_suppression_removes_only_its_grant", () => {
                var s = CLApply(new ConditionLedger("target"), "poison", ConditionKind.Poisoned).State;
                s = CLApply(s, "stone", ConditionKind.Petrified).State;
                s = CLImmune(s, "other", new[] { ConditionKind.Poisoned });
                s = s.SuppressApplication("stone", true).State;
                Require(s.ImmunitySources(ConditionKind.Poisoned).SequenceEqual(new[] { "other" }) && !s.View().Has(ConditionKind.Poisoned), "Suppressing stone removed independent protection.");
                s = s.EndImmunity("other", "end").State;
                Require(s.View().Has(ConditionKind.Poisoned), "Suppressed stone continued granting immunity.");
            });
            cases.Add("condition_lifecycle_poison_cure_during_petrified_is_permanent", () => {
                var s = CLApply(new ConditionLedger("target"), "poison", ConditionKind.Poisoned).State;
                s = CLApply(s, "stone", ConditionKind.Petrified, CLTime(2)).State; s = s.Cure(ConditionKind.Poisoned).State;
                s = s.AdvanceTo(CLTime(3)).State;
                Require(!s.View().Has(ConditionKind.Poisoned) && s.Applications[0].EndedReason == "generic-condition-cure", "Suppressed cure did not end poison.");
            });
            cases.Add("condition_lifecycle_exact_fractional_phase_endpoints_are_preserved", () => {
                var at = new EffectClockMarker(T(1, 3), 10); var end = new EffectClockMarker(T(1, 3), 20);
                var s = new ConditionLedger("target", at); s = CLApply(s, "blind", ConditionKind.Blinded, end).State;
                Require(s.View().Has(ConditionKind.Blinded), "Same-instant future-phase effect not active.");
                s = s.AdvanceTo(new EffectClockMarker(T(1, 3), 19)).State;
                Require(s.View().Has(ConditionKind.Blinded), "Effect expired before its phase.");
                s = s.AdvanceTo(end).State;
                Require(!s.View().Has(ConditionKind.Blinded) && s.Applications[0].EndedAt.Value.Equals(end), "Exact endpoint failed to expire.");
                Throws<ArgumentException>(() => s.AdvanceTo(at));
            });
            cases.Add("condition_lifecycle_fast_forward_keeps_intermediate_concentration_loss", () => {
                var s = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious, CLTime(4)).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Incapacitated }, CLTime(2));
                var jump = s.AdvanceTo(CLTime(10));
                Require(!jump.State.View().Has(ConditionKind.Incapacitated) && jump.Consequences.Count == 1
                    && jump.Consequences[0].Kind == ConditionConsequenceKind.EndConcentration && jump.Consequences[0].At.Equals(CLTime(2)),
                    "Final inactive state hid intermediate effective Incapacitated.");
            });
            cases.Add("condition_lifecycle_simultaneous_parent_and_immunity_expiry_has_no_transient_incapacity", () => {
                var s = CLApply(new ConditionLedger("target"), "stun", ConditionKind.Stunned, CLTime(2)).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Incapacitated }, CLTime(2));
                var result = s.AdvanceTo(CLTime(3));
                Require(result.Consequences.Count == 0 && !result.State.View().Has(ConditionKind.Stunned), "Equal-marker endings manufactured transient Incapacitated.");
            });
            cases.Add("condition_lifecycle_split_and_whole_advancement_agree", () => {
                var s = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious, CLTime(5)).State;
                s = CLImmune(s, "i", new[] { ConditionKind.Incapacitated }, CLTime(2));
                var whole = s.AdvanceTo(CLTime(7)); var first = s.AdvanceTo(CLTime(3)); var second = first.State.AdvanceTo(CLTime(7));
                Require(CLSignature(whole.State) == CLSignature(second.State)
                    && whole.Consequences.Select(x => x.Kind + ":" + x.At.Time + ":" + x.At.Phase).SequenceEqual(first.Consequences.Concat(second.Consequences).Select(x => x.Kind + ":" + x.At.Time + ":" + x.At.Phase)),
                    "Chunked advancement changed state or transition effects.");
            });
            cases.Add("condition_lifecycle_zero_hp_death_and_independent_unconscious_remain_distinct", () => {
                var s = CLImmune(new ConditionLedger("target"), "i", new[] { ConditionKind.Unconscious, ConditionKind.Incapacitated });
                var zero = new LifeState(20, 0); var dead = new LifeState(20, 0, dead: true);
                Require(!s.View().PermissionsForLife(zero).Action && !s.View().PermissionsForLife(dead).VoluntarySpeed, "External immunity overrode zero HP or death.");
                var healthy = PlaytestLife.Heal(zero, 2);
                Require(s.View().PermissionsForLife(healthy).Action && zero.Hp == 0, "Life recovery altered condition or original state.");
                s = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious).State;
                Require(!s.View().PermissionsForLife(healthy).Action && s.View().Has(ConditionKind.Unconscious), "Healing erased independent Unconscious.");
                Throws<ArgumentException>(() => s.View().PermissionsForLife(null));
                Throws<ArgumentException>(() => s.View().PermissionsForLife(dead, actionsTaken: -1));
            });
            cases.Add("condition_lifecycle_corrupted_projection_preserves_guaranteed_recovery", () => {
                var s = CLApply(new ConditionLedger("target"), "corrupt", ConditionKind.Corrupted).State;
                Require(s.View().HealingPotential(5) == 2 && s.View().HealingPotential(1, HpRestorationKind.StableRecovery) == 1, "Corrupted projection changed guaranteed recovery.");
                s = s.Cure(ConditionKind.Corrupted).State;
                Require(s.View().HealingPotential(5) == 5, "Removed Corrupted kept healing penalty.");
            });
            cases.Add("condition_lifecycle_noncombat_clauses_remain_specific", () => {
                var s = CLApply(new ConditionLedger("target"), "deaf", ConditionKind.Deafened).State;
                Require(s.View().BlocksHearing && !s.View().BlocksSpeech && !s.View().BlocksAudibleFeatures, "Deafened incorrectly prohibited own speech.");
                s = CLApply(s, "silent", ConditionKind.Silenced).State;
                Require(s.View().BlocksAudibleFeatures && !s.View().BlocksSight, "Silenced became unrelated sense loss.");
                s = CLApply(s, "blind", ConditionKind.Blinded).State; Require(s.View().BlocksSight, "Blinded sight clause lost.");
            });
            cases.Add("condition_lifecycle_cure_does_not_turn_prevention_into_component_removal", () => {
                var s = CLImmune(new ConditionLedger("target"), "i", new[] { ConditionKind.Incapacitated });
                s = CLApply(s, "stun", ConditionKind.Stunned).State; s = s.Cure(ConditionKind.Incapacitated).State;
                Require(s.Applications[0].IncapacitatedPreventedAtAdmission && !s.Applications[0].IncapacitatedComponentEnded, "Prevention and removal history were conflated.");
            });
            cases.Add("condition_lifecycle_application_history_bounds_reserve_onset_atomically", () => {
                var s = new ConditionLedger("target");
                for (int i = 0; i < 127; i++) s = CLApply(s, "a" + i, ConditionKind.Blinded).State;
                string before = CLSignature(s); Throws<InvalidOperationException>(() => CLApply(s, "sleep", ConditionKind.Unconscious));
                Require(CLSignature(s) == before, "Failed onset partially admitted parent.");
                s = CLApply(s, "last", ConditionKind.Blinded).State;
                Throws<InvalidOperationException>(() => CLApply(s, "overflow", ConditionKind.Blinded));
                s = s.Cure(ConditionKind.Blinded).State;
                Throws<InvalidOperationException>(() => CLApply(s, "no-eviction", ConditionKind.Blinded));
            });
            cases.Add("condition_lifecycle_immunity_history_bound_never_evicts_ended_grants", () => {
                var s = new ConditionLedger("target");
                for (int i = 0; i < 64; i++) s = CLImmune(s, "i" + i, new[] { ConditionKind.Blinded });
                s = s.EndImmunity("i0", "end").State; string before = CLSignature(s);
                Throws<InvalidOperationException>(() => CLImmune(s, "overflow", new[] { ConditionKind.Poisoned }));
                Require(CLSignature(s) == before, "Rejected immunity mutated history.");
            });
            cases.Add("condition_lifecycle_projection_is_repeatable_without_onset_or_mutation", () => {
                var s = CLApply(new ConditionLedger("target"), "sleep", ConditionKind.Unconscious).State;
                string before = CLSignature(s);
                for (int i = 0; i < 10; i++) {
                    Require(s.View().Has(ConditionKind.Unconscious), "Repeated projection changed state.");
                    Require(s.AdvanceTo(s.Now).Consequences.Count == 0, "Same-marker query repeated onset.");
                }
                Require(CLSignature(s) == before, "Projection mutated ledger.");
            });
            cases.Add("condition_lifecycle_parent_component_admission_suppression_cure_grid", () => {
                int tested = 0;
                foreach (var parent in new[] { ConditionKind.Paralyzed, ConditionKind.Petrified, ConditionKind.Stunned, ConditionKind.Unconscious })
                for (int flags = 0; flags < 256; flags++) {
                    bool initialParent = (flags & 1) != 0, initialIncap = (flags & 2) != 0, initialProne = (flags & 4) != 0;
                    bool laterParent = (flags & 8) != 0, laterIncap = (flags & 16) != 0, cureIncap = (flags & 32) != 0;
                    bool cureParent = (flags & 64) != 0, laterProne = (flags & 128) != 0;
                    var s = new ConditionLedger("target"); var initial = new List<ConditionKind>();
                    if (initialParent) initial.Add(parent); if (initialIncap) initial.Add(ConditionKind.Incapacitated); if (initialProne) initial.Add(ConditionKind.Prone);
                    if (initial.Count != 0) s = CLImmune(s, "initial", initial.ToArray(), CLTime(1));
                    s = CLApply(s, "parent", parent, CLTime(10)).State; s = s.AdvanceTo(CLTime(2)).State;
                    var later = new List<ConditionKind>(); if (laterParent) later.Add(parent); if (laterIncap) later.Add(ConditionKind.Incapacitated); if (laterProne) later.Add(ConditionKind.Prone);
                    if (later.Count != 0) s = CLImmune(s, "later", later.ToArray());
                    if (cureIncap) s = s.Cure(ConditionKind.Incapacitated).State; if (cureParent) s = s.Cure(parent).State;
                    bool parentActive = !initialParent && !laterParent && !cureParent;
                    Require(s.View().Has(parent) == parentActive && s.View().Has(ConditionKind.Incapacitated) == (parentActive && !initialIncap && !laterIncap && !cureIncap)
                        && s.View().Has(ConditionKind.Prone) == (parent == ConditionKind.Unconscious && !initialParent && !initialProne && !laterProne),
                        "Independent reference grid mismatch: " + parent + "/" + flags);
                    Require(PlaytestConditions.Permissions(s.View().Clauses).VoluntarySpeed == !parentActive, "Parent movement restriction failed grid.");
                    tested++;
                }
                Require(tested == 1024, "Incomplete condition state grid.");
            });
        }
    }
}
#endif
