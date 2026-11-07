#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Authored facts for one public knowledge-only project. The actor has Alchemy5 and
    /// primary-tool proficiency, ordinary suitable tools/station at the plot, visual sufficient
    /// evidence and two legal work Watches [0,8h),[8h,16h). This is not general character acquisition,
    /// evidence adjudication, rest, purchasing or permission to manufacture the formula's output.</summary>
    public sealed class SharedResearchFixture
    {
        public const string Recipe = "recipe-4", Recipe14 = "recipe-14", Evidence = "research.guild-notes", FreshEvidence = "research.independent-notes",
            LegibleFormula = "research.legible-formula", Recipe14Evidence = "research.recipe14.guild-notes",
            Recipe14FreshEvidence = "research.recipe14.independent-notes", Recipe14LegibleFormula = "research.recipe14.legible-formula",
            Supplies = "research.writing-supplies";
        private readonly string[] recipeIds;
        public IReadOnlyList<string> RecipeIds { get; }
        public string RecipeId => recipeIds.Length==1?recipeIds[0]:null;
        public string WorkerId { get; }
        public bool Qualified { get; }
        public bool Accessible { get; }
        public bool Sufficient { get; }
        public bool StationSuitable { get; }
        public SharedResearchFixture(string workerId = TestOnlyPolicy.CompanionId, bool qualified = true,
            bool accessible = true, bool sufficient = true, bool stationSuitable = true,string recipeId=Recipe,IEnumerable<string> recipeIds=null)
        {
            var selected=(recipeIds??new[]{recipeId}).ToArray();
            if ((workerId != TestOnlyPolicy.ActorId && workerId != TestOnlyPolicy.CompanionId)
                ||recipeIds!=null&&recipeId!=Recipe||selected.Length<1||selected.Length>2
                ||selected.Any(x=>x!=Recipe&&x!=Recipe14)||selected.Distinct(StringComparer.Ordinal).Count()!=selected.Length)
                throw new ArgumentException("Unknown supplied researcher or formula profile.");
            this.recipeIds=selected.OrderBy(x=>Selector(x)).ToArray();RecipeIds=Array.AsReadOnly(this.recipeIds);
            WorkerId = workerId; Qualified = qualified; Accessible = accessible; Sufficient = sufficient; StationSuitable = stationSuitable;
        }
        public bool SupportsRecipe(string recipeId)=>recipeIds.Contains(recipeId,StringComparer.Ordinal);
        public static int Selector(string recipeId)=>recipeId==Recipe?0:recipeId==Recipe14?1:-1;
        public static string RecipeForSelector(int selector)=>selector==0?Recipe:selector==1?Recipe14:null;
        public static string EvidenceFor(string recipeId,bool fresh=false,bool copy=false)
            =>recipeId==Recipe?(copy?LegibleFormula:fresh?FreshEvidence:Evidence)
                :recipeId==Recipe14?(copy?Recipe14LegibleFormula:fresh?Recipe14FreshEvidence:Recipe14Evidence):null;
        public static int Difficulty(string recipeId)=>recipeId==Recipe?8:recipeId==Recipe14?11:throw new ArgumentException("Unknown formula profile.",nameof(recipeId));
        public static long MinimumResearchHours(string recipeId)=>recipeId==Recipe?0:recipeId==Recipe14?0:throw new ArgumentException("Unknown formula profile.",nameof(recipeId));
        internal string Key
        {
            get {
                string facts=WorkerId+"|"+Qualified+"|"+Accessible+"|"+Sufficient+"|"+StationSuitable;
                if(RecipeId==Recipe)return "research-v1|recipe4-V4-32b2bf00c28584ad259c343bc5b961126d25078c094444c05bf3caf0c9edda5e|H8|INT-DC8|visual-evidence|retain-knowledge-work|retry-full-H|first-labor-copy-cost|windows0-8-16|"+facts;
                if(RecipeId==Recipe14)return "research-v2|recipe14-source-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|H8|INT-DC11|visual-evidence|retain-knowledge-work|retry-full-H|first-labor-copy-cost|windows0-8-16|"+facts;
                return "research-multi-v1|source-46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4|"+string.Join(",",recipeIds)+"|recipe-keyed-formula-history|H8|"+facts;
            }
        }
    }
    public static class FormulaResearchRules
    {
        public static RuleTime RequiredTime(long minimumResearchHours)
        {
            if (minimumResearchHours < 0) throw new ArgumentOutOfRangeException(nameof(minimumResearchHours));
            return new RuleTime(checked(Math.Max(8, minimumResearchHours) * 3600));
        }
        public static bool Succeeds(int natural, int modifier, int dc) => PlaytestRolls.TaskCheck(natural, modifier, dc).Degree >= TaskDegree.Success;
        public static bool Knows(Snapshot s, string actor, string recipe) => s.FormulaWork.Any(x => x.WorkerId == actor && x.RecipeId == recipe && x.Status == FormulaWorkStatus.Success);
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private readonly SharedResearchFixture research;
        private static string ResearchFingerprint(string body, SharedResearchFixture facts)
        {
            using (var sha = SHA256.Create()) return "TEST_ONLY.research-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(body + "|" + facts.Key)).Select(x => x.ToString("x2", CultureInfo.InvariantCulture)));
        }
        private void InitializeResearch(Snapshot s)
        {
            if (research == null) return;
            s.Work = new WorkLedger(s.Work.Lots.Concat(new[] { new ResourceLot(SharedResearchFixture.Supplies, "writing-allotment-1sp", 3, TestOnlyCropPolicy.PlotId, research.WorkerId) }), s.Work.WorkerIntervals, s.Work.Reservations);
            s.InventoryLots = s.InventoryLots.Concat(new[] { new InventoryLotRecord(SharedResearchFixture.Supplies, "", research.WorkerId, new RuleQuantity(3), default, NutritionKind.None, null, InventoryAccess.Ground) }).ToArray();
        }
        private string ValidateFormulaProfile(Snapshot s)
        {
            if(research==null)return s.FormulaWork.Length==0?null:"FormulaFixtureNotSelected";
            return s.FormulaWork.Any(x=>!research.SupportsRecipe(x.RecipeId))?"FormulaFixtureMismatch":null;
        }
        private static bool FormulaCommand(CommandKind kind) => kind == CommandKind.StartFormulaResearch || kind == CommandKind.StartFormulaCopy
            || kind == CommandKind.PauseFormulaWork || kind == CommandKind.ResumeFormulaWork || kind == CommandKind.CancelFormulaWork;
        private static bool FormulaOpen(FormulaWorkRecord job) => job.Status == FormulaWorkStatus.Working || job.Status == FormulaWorkStatus.Paused || job.Status == FormulaWorkStatus.AwaitingCheck;
        private static void PutFormula(Snapshot s, FormulaWorkRecord job) => s.FormulaWork = s.FormulaWork.Select(x => x.Id == job.Id ? job : x).ToArray();
        private static FormulaWorkRecord ChangeFormula(Snapshot s, FormulaWorkRecord job, FormulaWorkStatus status, ActiveWorkProgress progress = null,
            int first = 0, int second = 0, int natural = 0) => new FormulaWorkRecord(job.Id, job.WorkerId, job.RecipeId, job.EvidenceId, job.MethodId,
                job.Kind, status, job.StartedAt, s.RuleClock, progress ?? job.Work, first, second, natural, job.PreviousAttemptId);
        private static RuleTime? ResearchWindowEnd(RuleTime at) => at < new RuleTime(28800) ? new RuleTime(28800) : at < new RuleTime(57600) ? new RuleTime(57600) : (RuleTime?)null;
        private bool ResearchCapable(Snapshot s, string actor) => research != null && actor == research.WorkerId && CapableWorker(s, actor)
            && !View(s, actor).BlocksSight && AvailableHands(s, actor) >= 1;
        private string ResearchAccess(Snapshot s, string actor, bool requireWindow = true, bool requiresPrimaryTool = true)
        {
            if (actor != research.WorkerId || !research.Qualified) return "ResearchCredentialMissing";
            if (!research.Accessible || !research.Sufficient) return "ResearchEvidenceUnavailable";
            if (!research.StationSuitable) return "ResearchStationUnavailable";
            if(requiresPrimaryTool && TargetInActiveRepair(s,SharedCraftingFixture.ToolId))return "ResearchToolInRepair";
            if(crafting!=null&&(CraftingRestrictions.StationUseBlocked(s,SharedCraftingFixture.StationId)||requiresPrimaryTool && s.Structures.Single(x=>x.Id==SharedCraftingFixture.ToolId).Broken))return "ResearchToolsOrStationUnavailable";
            if (!ResearchCapable(s, actor)) return "ResearchWorkerIncapable";
            var body = s.Actors.Single(x => x.Id == actor);
            if (s.WorldTraversals.Any(x => x.ActorId == actor) || Math.Max(Math.Abs(body.X - 3), Math.Abs(body.Y - 3)) > 1) return "ResearchStationOutOfReach";
            if (s.InventoryCombat && s.WorldSchedule.Order.Contains(actor)) return "ResearchParticipantInCombat";
            if (requireWindow && !ResearchWindowEnd(s.RuleClock).HasValue) return "ResearchWorkWindowClosed";
            return null;
        }
        private static void BookFormula(Snapshot s, FormulaWorkRecord job)
        {
            var end = CampGreens.Add(s.RuleClock, job.Work.Remaining); var window = ResearchWindowEnd(s.RuleClock).Value; if (window < end) end = window;
            string id = job.Id + ".labor." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            s.Work = s.Work.Reserve(job.Id, new[] { new WorkerInterval(id, job.Id, job.WorkerId, s.RuleClock, end) }, Array.Empty<ResourceReservation>());
        }
        private static void PauseFormula(Snapshot s, FormulaWorkRecord job)
        {
            if (job.Status != FormulaWorkStatus.Working) return;
            s.Work = s.Work.CancelFutureWork(job.Id, s.RuleClock);
            PutFormula(s, ChangeFormula(s, job, FormulaWorkStatus.Paused, job.Work.Interrupt(false)));
        }
        private void PauseIncompatibleFormulaWork(Snapshot s)
        {
            if (research == null) return;
            foreach (var job in s.FormulaWork.Where(x => x.Status == FormulaWorkStatus.Working).ToArray())
                if (!ResearchCapable(s, job.WorkerId) || (s.InventoryCombat && s.WorldSchedule.Order.Contains(job.WorkerId))
                    || (s.SchemaVersion < 17 || job.Kind == FormulaWorkKind.Research) && TargetInActiveRepair(s,SharedCraftingFixture.ToolId)
                    || crafting!=null&&(CraftingRestrictions.StationUseBlocked(s,SharedCraftingFixture.StationId)
                        || (s.SchemaVersion < 17 || job.Kind == FormulaWorkKind.Research) && s.Structures.Single(x=>x.Id==SharedCraftingFixture.ToolId).Broken)) PauseFormula(s, job);
        }
        private static RuleTime? NextFormulaBoundary(Snapshot s)
        {
            var ends = s.FormulaWork.Where(x => x.Status == FormulaWorkStatus.Working).Select(x => s.Work.WorkerIntervals.Single(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock).End).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }
        private static void CreditFormulaWork(Snapshot s, RuleTime elapsed, ICollection<string> ready)
        {
            foreach (var job in s.FormulaWork.Where(x => x.Status == FormulaWorkStatus.Working).ToArray()) {
                if (job.Kind == FormulaWorkKind.Copy && job.Work.Labor == default) s.Work = s.Work.Consume(job.Id, job.Id + ".supplies");
                var progress = job.Work.Credit(elapsed); FormulaWorkStatus status = FormulaWorkStatus.Working;
                if (progress.Complete) {
                    status = job.Kind == FormulaWorkKind.Copy ? FormulaWorkStatus.Success : FormulaWorkStatus.AwaitingCheck;
                    if (status == FormulaWorkStatus.AwaitingCheck) ready.Add(job.Id);
                } else if (!s.Work.WorkerIntervals.Any(w => w.JobId == job.Id && w.Start <= s.RuleClock && w.End > s.RuleClock)) status = FormulaWorkStatus.Paused;
                PutFormula(s, ChangeFormula(s, job, status, progress));
            }
        }
        private void FinishFormulaCheck(Snapshot s, FormulaWorkRecord job)
        {
            var character = s.Characters.Single(x => x.ActorId == job.WorkerId);
            var facts = CharacterRuleFacts.From(character);
            int modifier = facts.AbilityModifier(CharacterAbility.Intelligence) + facts.ProficiencyBonus;
            // Schema16 histories retain their original check outcomes. Schema17 corrects actual tool checks.
            if (s.SchemaVersion >= 17) modifier += PlaytestLife.AbilityCheckInjuryPenalty(ActorLifeRules.Read(s.Lives.Single(x => x.ActorId == job.WorkerId)), 3, toolCheck: true);
            var roll = PlaytestDice.RollD20(s.RandomState, disadvantageSources: View(s, job.WorkerId).Has(ConditionKind.Poisoned) ? 1 : 0);
            s.RandomState = roll.NextRandomState;
            var status = FormulaResearchRules.Succeeds(roll.Natural, modifier, SharedResearchFixture.Difficulty(job.RecipeId)) ? FormulaWorkStatus.Success : FormulaWorkStatus.Failure;
            PutFormula(s, ChangeFormula(s, job, status, first: roll.First, second: roll.Second ?? 0, natural: roll.Natural));
        }
        private string ResolveFormulaWork(Snapshot s, Command c)
        {
            if (research == null) return "FormulaWorkNotSelected";
            if (c.Inventory != null || c.Combat != null) return "InvalidFormulaRequest";
            bool start = c.Kind == CommandKind.StartFormulaResearch || c.Kind == CommandKind.StartFormulaCopy;
            if (start) {
                if (c.X < 0 || c.X > 1 || c.Kind == CommandKind.StartFormulaCopy && c.X != 0) return "UnknownResearchMethod";
                string recipeId=SharedResearchFixture.RecipeForSelector(c.Y);
                if(!research.SupportsRecipe(recipeId))return "FormulaNotSelected";
                bool copy = c.Kind == CommandKind.StartFormulaCopy;
                if (copy ? c.Target != SharedResearchFixture.EvidenceFor(recipeId,copy:true)
                    : c.Target != SharedResearchFixture.EvidenceFor(recipeId) && c.Target != SharedResearchFixture.EvidenceFor(recipeId,fresh:true)) return "UnknownResearchEvidence";
                string access = ResearchAccess(s, c.Actor, requiresPrimaryTool: !copy || s.SchemaVersion < 17); if (access != null) return access;
                if (FormulaResearchRules.Knows(s, c.Actor, recipeId)) return "FormulaAlreadyKnown";
                if (s.FormulaWork.Any(x => x.WorkerId == c.Actor && FormulaOpen(x)) || OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
                if (copy && s.Work.AvailableAmount(SharedResearchFixture.Supplies) < new RuleQuantity(1)) return "WritingSuppliesUnavailable";
                string method = copy ? "method.transcription" : c.X == 0 ? "method.sequence-analysis" : "method.independent-comparison";
                if (!copy && s.FormulaWork.Any(x => x.WorkerId == c.Actor && x.RecipeId==recipeId&&x.EvidenceId == c.Target && x.MethodId == method && x.Status == FormulaWorkStatus.Failure)) return "UnchangedResearchEvidence";
                if (s.FormulaWork.Length == FormulaWorkValidation.MaxRecords) return "FormulaHistoryCapacityReached";
                var prior = s.FormulaWork.Where(x => x.WorkerId == c.Actor && x.RecipeId == recipeId && x.Status == FormulaWorkStatus.Failure)
                    .OrderByDescending(x=>x.UpdatedAt).ThenBy(x=>x.Id,StringComparer.Ordinal).FirstOrDefault();
                string id = "formula." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
                var job = new FormulaWorkRecord(id, c.Actor, recipeId, c.Target, method, copy ? FormulaWorkKind.Copy : FormulaWorkKind.Research,
                    FormulaWorkStatus.Working, s.RuleClock, s.RuleClock, new ActiveWorkProgress(new[] { copy ? new RuleTime(3600) : FormulaResearchRules.RequiredTime(SharedResearchFixture.MinimumResearchHours(recipeId)) }), previousAttemptId: prior?.Id ?? "");
                if (copy) s.Work = s.Work.Reserve(id, Array.Empty<WorkerInterval>(), new[] { new ResourceReservation(id + ".supplies", id, SharedResearchFixture.Supplies, 1) });
                BookFormula(s, job); s.FormulaWork = s.FormulaWork.Concat(new[] { job }).ToArray(); return null;
            }
            if (c.X != 0||c.Y!=0) return "InvalidFormulaRequest";
            var current = s.FormulaWork.SingleOrDefault(x => x.Id == c.Target && x.WorkerId == c.Actor); if (current == null) return "UnknownFormulaWork";
            if(!research.SupportsRecipe(current.RecipeId))return "FormulaNotSelected";
            if (!FormulaOpen(current)) return "FormulaWorkClosed";
            if (c.Kind == CommandKind.PauseFormulaWork) {
                if (current.Status != FormulaWorkStatus.Working) return "FormulaNotWorking";
                PauseFormula(s, current); return null;
            }
            if (c.Kind == CommandKind.CancelFormulaWork) {
                s.Work = s.Work.CancelFutureWork(current.Id, s.RuleClock);
                if (current.Kind == FormulaWorkKind.Copy && current.Work.Labor == default) s.Work = s.Work.Release(current.Id, current.Id + ".supplies");
                PutFormula(s, ChangeFormula(s, current, FormulaWorkStatus.Cancelled)); return null;
            }
            if (c.Kind == CommandKind.ResumeFormulaWork) {
                if (current.Status == FormulaWorkStatus.Working) return "FormulaAlreadyWorking";
                string access = ResearchAccess(s, c.Actor, current.Status != FormulaWorkStatus.AwaitingCheck, current.Kind == FormulaWorkKind.Research || s.SchemaVersion < 17); if (access != null) return access;
                if (OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
                if (current.Status == FormulaWorkStatus.AwaitingCheck) { FinishFormulaCheck(s, current); return null; }
                BookFormula(s, current); PutFormula(s, ChangeFormula(s, current, FormulaWorkStatus.Working)); return null;
            }
            return "InvalidFormulaRequest";
        }
    }
}
#endif
