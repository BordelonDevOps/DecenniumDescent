#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public enum StructuralDamageKind { Bludgeoning, Piercing, Slashing, Acid, Cold, Fire, Force, Lightning, Necrotic, Poison, Psychic, Radiant, Thunder }
    /// <summary>Ordinary mundane object procedure, without unprovided special defenses. Compatibility
    /// must be established before resolution. No attack, target eligibility or repair work is granted.</summary>
    public static class ObjectStructureRules
    {
        public static int MaterialAc(ObjectMaterial material) => material == ObjectMaterial.ClothPaperRope ? 11 : material == ObjectMaterial.GlassCrystal ? 13
            : material == ObjectMaterial.WoodLeather ? 15 : material == ObjectMaterial.Stone ? 17 : material == ObjectMaterial.IronSteel ? 19 : throw new ArgumentException("Unknown material.");
        public static ObjectStructureRecord Damage(ObjectStructureRecord item, long amount, StructuralDamageKind kind, bool physicallyCompatible)
        {
            if (item == null || amount < 0 || !Enum.IsDefined(typeof(StructuralDamageKind), kind)) throw new ArgumentException("Invalid structural damage.");
            if (!physicallyCompatible || kind == StructuralDamageKind.Poison || kind == StructuralDamageKind.Psychic) return item;
            return item.WithHp(amount >= item.Hp ? 0 : item.Hp - amount);
        }
        public static RuleQuantity RepairMaterialsCopper(ObjectStructureRecord item) => new RuleQuantity(item.BaselineCopper, 4);
        public static RuleTime RepairLabor(ObjectStructureRecord item) => new RuleTime(checked(Math.Max(10, item.MaximumHp) * 360));
        public static bool RepairSucceeds(int natural, int modifier) => PlaytestRolls.TaskCheck(natural, modifier, 10).Degree >= TaskDegree.Success;
    }
    /// <summary>Pre-authored occurrence for consequence integration. Result is already settled by a
    /// preceding order, whose ingredients/quality roll are outside this fixture. Not a damage command.</summary>
    public sealed class CraftingMishapFact
    {
        public string Id { get; }
        public string LeadId { get; }
        public RuleTime At { get; }
        public int Result { get; }
        public IReadOnlyList<string> Participants { get; }
        public CraftingMishapFact(string id, int result, string lead = TestOnlyPolicy.CompanionId, RuleTime at = default, string[] participants = null)
        {
            if (!Validation.ValidId(id) || result < 1 || result > 6
                || lead != TestOnlyPolicy.ActorId && lead != TestOnlyPolicy.CompanionId) throw new ArgumentException("Invalid supplied mishap fact.");
            var people = participants ?? new[] { lead };
            if (people.Length < 1 || people.Length > 3 || !people.Contains(lead) || people.Distinct().Count() != people.Length || people.Any(x => x != TestOnlyPolicy.ActorId && x != TestOnlyPolicy.CompanionId && x != AdditionalTacticalActor.Id)) throw new ArgumentException("Invalid participating workers.");
            Id = id; LeadId = lead; At = at; Result = result; Participants = Array.AsReadOnly(people.ToArray());
        }
        internal string Key => Id + "|" + LeadId + "|" + At + "|" + Result + "|" + string.Join(",", Participants);
    }
    public sealed class SharedCraftingFixture
    {
        public const string ToolId = "craft.alchemist-kit", StationId = TestOnlyCropPolicy.PlotId, TradeId = "Alchemy";
        public long HeroHp { get; }
        public long CompanionHp { get; }
        public int ToolHp { get; }
        public bool HeroProficient { get; }
        public IReadOnlyList<CraftingMishapFact> Events { get; }
        public SharedCraftingFixture(long heroHp = 26, long companionHp = 26, int toolHp = 5, bool heroProficient = false, params CraftingMishapFact[] events)
        {
            if (heroHp < 1 || heroHp > 26 || companionHp < 1 || companionHp > 26 || toolHp < 0 || toolHp > 5 || events == null
                || events.Length > 32 || events.Any(x => x == null) || events.Select(x => x.Id).Distinct().Count() != events.Length) throw new ArgumentException("Invalid crafting facts.");
            HeroHp = heroHp; CompanionHp = companionHp; ToolHp = toolHp; HeroProficient = heroProficient; Events = Array.AsReadOnly(events.ToArray());
        }
        internal string Key => "craft-consequences-v1|wood-load-bearing-case|ordinary-defenses|compatible-bludgeoning|Alchemy-acid|tool50gp8lbHP5|two-legal-watches|retain-remedy-labor|"
            + HeroHp + "|" + CompanionHp + "|" + ToolHp + "|" + HeroProficient + "|" + string.Join(";", Events.Select(x => x.Key));
    }
    public static class CraftingRestrictions
    {
        public static bool StationUseBlocked(Snapshot s, string station) => s.CraftingIncidents.Any(x => !x.Remedied && x.StationId == station && x.Result == 1);
        public static bool OrderWorkBlocked(Snapshot s, string station) => StationUseBlocked(s, station) || s.CraftingIncidents.Any(x => !x.Remedied && x.Result == 5 && x.StationId == station);
        public static bool NewOrderBlocked(Snapshot s, string lead, string station, string trade) => OrderWorkBlocked(s, station)
            || s.CraftingIncidents.Any(x => !x.Remedied && x.Result == 6 && x.LeadId == lead && x.TradeId == trade);
        public static bool CraftingCheckBlocked(Snapshot s, string tool) => s.Structures.Single(x => x.Id == tool).Broken || s.CraftingIncidents.Any(x => !x.Remedied && x.Result == 2 && x.ToolId == tool);
    }
    public sealed partial class TestOnlySharedWorldPolicy
    {
        private readonly SharedCraftingFixture crafting;
        private int SelectedSchema => expeditionPressureProfile != null ? Snapshot.ExpeditionPressureSchema
            : havenCareProfile != null ? Snapshot.HavenCareSchema
            : moraleRestProfile != null ? Snapshot.MoraleRestSchema
            : strainRecoveryProfile != null ? Snapshot.ExpeditionStrainRecoverySchema
            : restDebtProfile != null ? Snapshot.RestDebtSchema
            : dailyProvisioning!=null ? Snapshot.DailyProvisioningSchema
            : characterAdvancement!=null&&characterAdvancement.LevelFourAdvancementEnabled ? Snapshot.SharedCharacterAdvancementSchema
            : routeReconnaissanceFixture!=null ? Snapshot.RouteReconnaissanceSchema
            : routeMappingWorkFixture!=null ? Snapshot.RouteMappingWorkSchema
            : readyActionEnabled ? Snapshot.ReadyActionSchema : cacheExcavationEnabled ? Snapshot.BuriedCacheSchema : dodgeActionEnabled ? Snapshot.DodgeSchema : huntingTrapFixture!=null ? Snapshot.HuntingTrapSchema
            : routeMappingFixture!=null ? Snapshot.RouteMappingSchema
            : routeMotionFixture!=null ? Snapshot.RouteObservationSchema
            : routeTravelFixture!=null ? Snapshot.ExpeditionRouteSchema
            : observationFixture!=null ? Snapshot.ObservationSchema
            : ordinaryReceptacles!=null ? Snapshot.OrdinaryReceptacleSchema
            : prospectingFixture!=null ? Snapshot.ProspectingSchema
            : miningFixture!=null ? (miningFixture.MiningToolCandidateProfiles.Length>0?Snapshot.MiningToolCandidateSchema
                :miningFixture.MineralPreparationProfiles.Length>0?Snapshot.MineralPreparationSchema
                :expeditionAssignmentsEnabled?Snapshot.MiningExpeditionAssignmentSchema
                :miningFixture.DestructiveAssayProfiles.Length>0?Snapshot.DestructiveMiningAssaySchema
                :miningFixture.AssayProfiles.Length>0?Snapshot.MiningAssaySchema:Snapshot.MiningSchema)
            : harvestFixture!=null ? harvestFixture.SchemaVersion
            : offCalendarActivityEnabled ? Snapshot.OffCalendarActivitySchema
            : expeditionAssignmentsEnabled ? Snapshot.ExpeditionAssignmentSchema
            : fishingTrap!=null ? (fishingTrapLegacy?Snapshot.FishingTrapLegacySchema
            :fishingTrapBaitOnly?Snapshot.FishingTrapBaitSchema
            :fishingTrapProfiles.Length>1?Snapshot.FishingStockSchema:Snapshot.FishingTrapSchema)
            : characterAdvancement!=null&&characterAdvancement.DefensiveFormationSchemaEnabled ? Snapshot.DefensiveFormationSchema
            : characterAdvancement!=null&&characterAdvancement.SuppressionFireSchemaEnabled ? Snapshot.SuppressionFireSchema
            : characterAdvancement!=null&&characterAdvancement.CommandStepSchemaEnabled ? Snapshot.CommandStepSchema
            : characterAdvancement!=null&&characterAdvancement.TacticalAssessmentSchemaEnabled ? Snapshot.TacticalAssessmentSchema
            : characterAdvancement!=null&&characterAdvancement.HistorySchemaEnabled ? Snapshot.CharacterAdvancementHistorySchema
            : soldierCharacterBuild != null&&soldierCharacterBuild.TacticalTechniquesEnabled ? Snapshot.SoldierTacticalTechniquesSchema
            : soldierCharacterBuild != null ? Snapshot.SoldierInitialBuildSchema
            : soldierInitialLoadout != null ? Snapshot.SoldierInitialLoadoutSchema
            : overwatchExecution != null ? Snapshot.OverwatchExecutionSchema
            : overwatchRuntime != null ? Snapshot.OverwatchSchema
            : overwatchFoundation != null ? Snapshot.SharedBonusActionSchema
            : periodicRider != null ? Snapshot.PeriodicRiderSchema
            : rangedCombat != null ? Snapshot.RepeatingCrossbowSchema
            : characterAdvancement != null ? Snapshot.CharacterAdvancementSchema
            : portableKit != null ? Snapshot.PortableEquipmentSchema
            : supplyCache != null ? Snapshot.SupplyCacheSchema
            : manufacturing != null ? Snapshot.ManufacturingSchema
            : repair != null ? Snapshot.RepairWorkSchema
            : crafting != null ? Snapshot.CraftingConsequenceSchema
            : research != null ? Snapshot.FormulaWorkSchema
            : connectedCombat == null ? Snapshot.SharedWorldSchema
            : Snapshot.CalendarCombatSchema;
        private static string CraftingFingerprint(string prior, SharedCraftingFixture facts)
        {
            using (var sha = SHA256.Create()) return "TEST_ONLY.crafting-v1-" + string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(prior + "|" + facts.Key)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
        private void InitializeCrafting(Snapshot s)
        {
            if (crafting == null) return;
            s.Structures = new[] { new ObjectStructureRecord(SharedCraftingFixture.ToolId, "tools.alchemist-s-supplies", TestOnlyPolicy.CompanionId,
                TestOnlyPolicy.CompanionId, RepairSiteLocationId, ObjectMaterial.WoodLeather, 5, crafting.ToolHp, 5000, new RuleQuantity(8)) };
        }
        private static bool Dying(ActorLifeRecord life) => life.Hp == 0 && !life.Dead && !life.Stable && life.UsesDeathSaves;
        private static void ReconcileDyingCadences(Snapshot s)
        {
            if (s.SchemaVersion < Snapshot.CraftingConsequenceSchema) return;
            s.DyingCadences = s.DyingCadences.Where(x => Dying(s.Lives.Single(a => a.ActorId == x.ActorId))).ToArray();
            foreach (var life in s.Lives.Where(x => Dying(x) && !s.WorldSchedule.Order.Contains(x.ActorId)).OrderBy(x => x.ActorId, StringComparer.Ordinal))
                if (!s.DyingCadences.Any(x => x.ActorId == life.ActorId)) s.DyingCadences = s.DyingCadences.Concat(new[] { new DyingCadenceRecord(life.ActorId, s.RuleClock) }).ToArray();
        }
        private static RuleTime? NextDyingMarker(Snapshot s)
        {
            if (s.SchemaVersion < Snapshot.CraftingConsequenceSchema) return null;
            var deadlines = s.DyingCadences.Select(x => x.NextAt).ToList();
            foreach (var life in s.Lives.Where(x => Dying(x) && s.WorldSchedule.Order.Contains(x.ActorId))) {
                long ordinal = s.WorldSchedule.LatestStart(life.ActorId, s.WorldSchedule.ProcessedSlot);
                if (ordinal < 0) ordinal = s.WorldSchedule.Order.ToList().IndexOf(life.ActorId); else ordinal = checked(ordinal + s.WorldSchedule.Order.Count);
                deadlines.Add(s.WorldSchedule.Start(ordinal));
            }
            return deadlines.Count == 0 ? (RuleTime?)null : deadlines.Min();
        }
        private static void ProcessSharedLifeMarkers(Snapshot s, long previousSlot)
        {
            // Expiry and absolute Stable recovery have already run. At a tie, established calendar
            // actors precede unscheduled actors, whose stable identity supplies deterministic order.
            if (s.WorldSchedule.ProcessedSlot != previousSlot && s.WorldSchedule.Start(s.WorldSchedule.ProcessedSlot) == s.RuleClock) {
                string actor = s.WorldSchedule.Order[(int)(s.WorldSchedule.ProcessedSlot % s.WorldSchedule.Order.Count)];
                SaveWorldLifeMarker(s, actor, s.WorldSchedule.Id, s.WorldSchedule.Origin, s.WorldSchedule.ProcessedSlot, checked((int)s.WorldSchedule.ProcessedSlot));
            }
            foreach (var cadence in s.DyingCadences.Where(x => x.NextAt == s.RuleClock).OrderBy(x => x.ActorId, StringComparer.Ordinal).ToArray()) {
                SaveWorldLifeMarker(s, cadence.ActorId, "outside.dying", cadence.Onset, cadence.NextOrdinal, -1);
                s.DyingCadences = s.DyingCadences.Select(x => x.ActorId == cadence.ActorId ? new DyingCadenceRecord(x.ActorId, x.Onset, x.NextOrdinal + 1) : x).ToArray();
            }
            ReconcileDyingCadences(s);
        }
        private static void SaveWorldLifeMarker(Snapshot s, string actor, string calendar, RuleTime origin, long ordinal, int turnOrdinal)
        {
            long sequence = s.WorldLifeMarkers.Length + 1L;
            ActorLifeRules.SaveAtMarker(s, actor, turnOrdinal, sequence);
            if (s.LifeEvents.Count(x => x.Kind == LifeEventKind.DeathSave) == sequence)
                s.WorldLifeMarkers = s.WorldLifeMarkers.Concat(new[] { new WorldLifeMarkerRecord(actor, calendar, origin, ordinal, sequence, s.RuleClock) }).ToArray();
        }
        private static bool CraftingCommand(CommandKind kind) => kind == CommandKind.DispatchCraftingMishap || kind == CommandKind.StartCraftRemedy || kind == CommandKind.PauseCraftRemedy;
        private string ResolveCraftingConsequence(Snapshot s, Command c)
        {
            if (crafting == null) return "CraftingConsequencesNotSelected";
            if (c.Inventory != null || c.Combat != null || c.X != 0 || c.Y != 0) return "InvalidCraftingConsequenceRequest";
            if (PendingCalendarChoice(s)) return "TacticalChoicePending";
            if (c.Kind != CommandKind.DispatchCraftingMishap) return ResolveRemedy(s, c);
            var fact = crafting.Events.SingleOrDefault(x => x.Id == c.Target && x.LeadId == c.Actor);
            if (fact == null) return "UnknownCraftingMishap";
            if (s.CraftingIncidents.Any(x => x.Id == fact.Id)) return "CraftingMishapAlreadyResolved";
            if (s.RuleClock != fact.At) return "WrongCraftingMishapTime";
            return ApplyCraftingMishap(s,fact);
        }
        private string ApplyCraftingMishap(Snapshot s,CraftingMishapFact fact)
        {
            if (s.CraftingIncidents.Length == CraftingConsequenceValidation.MaxIncidents) return "CraftingIncidentCapacityReached";
            if (s.WorldTraversals.Any(x => x.ActorId == fact.LeadId && x.DistanceFeet != default)) return "OffGridPhysicalConsequenceUnsupported";
            var before = s.Lives.Single(x => x.ActorId == fact.LeadId);
            if (before.Dead) return "CraftingLeadDead";
            if (fact.Result == 4 && !TestOnlyClubAttackPolicy.DamageConditionCapacity(s, fact.LeadId)) return "ConditionHistoryCapacityReached";
            uint initial = s.RandomState; int d4 = 0, wound = 0, injury = 0; long damage = 0, words = 0;
            if (fact.Result == 3) {
                var kit = s.Structures.Single(x => x.Id == SharedCraftingFixture.ToolId);
                var after = ObjectStructureRules.Damage(kit, 1, StructuralDamageKind.Bludgeoning, true);
                s.Structures = s.Structures.Select(x => x.Id == kit.Id ? after : x).ToArray(); damage = kit.Hp - after.Hp;
            }
            if (fact.Result == 4) {
                var draw = DiceStream.Draw(s.RandomState, 4); d4 = draw.Value + 1; damage = d4;
                damage = CharacterAdvancementRules.ReduceIncomingDamage(s,fact.LeadId,damage);
                if (View(s, fact.LeadId).Has(ConditionKind.Petrified)) damage = PlaytestConditions.PetrifiedDamage(damage);
                var character = s.Characters.Single(x => x.ActorId == fact.LeadId);
                int constitutionSave=checked(CharacterRuleFacts.From(character).AbilityModifier(CharacterAbility.Constitution)
                    +CharacterAdvancementRules.SaveProficiencyBonus(s,fact.LeadId,"CON")
                    +ExpeditionStrainRules.Current(s,fact.LeadId).SavingThrowModifier);
                var result = PlaytestDamageDice.Resolve(ActorLifeRules.ReadForResolution(s,before), damage, s.RuleClock, draw.NextState, constitutionSave);
                s.RandomState = result.NextRandomState; words = checked(draw.WordsConsumed + result.WordsConsumed); wound = result.WoundRoll?.Natural ?? 0; injury = result.InjuryD6 ?? 0;
                TestOnlyClubAttackPolicy.ApplyLife(s, before, result.Outcome.State);
            }
            var required = new RuleTime(fact.Result == 1 || fact.Result == 6 ? 3600 : fact.Result == 2 ? 7200 : fact.Result == 5 ? 3600 * fact.Participants.Count : 0);
            s.CraftingIncidents = s.CraftingIncidents.Concat(new[] { new CraftingIncidentRecord(fact.Id, fact.LeadId, SharedCraftingFixture.ToolId, SharedCraftingFixture.StationId,
                SharedCraftingFixture.TradeId, fact.Result, fact.Participants, s.Revision + 1, s.RuleClock, s.RuleClock, required, default, Array.Empty<string>(), d4, damage, wound, injury, initial, s.RandomState, words) }).ToArray();
            ReconcileDyingCadences(s); PauseIncompatibleWork(s); ReconcileTraversal(s); return null;
        }
        private static void PutIncident(Snapshot s, CraftingIncidentRecord incident) => s.CraftingIncidents = s.CraftingIncidents.Select(x => x.Id == incident.Id ? incident : x).ToArray();
        private static string RemedyJobId(CraftingIncidentRecord incident) => "craft.remedy." + incident.Revision.ToString(CultureInfo.InvariantCulture);
        private bool RemedyCapable(Snapshot s, CraftingIncidentRecord incident, string actor)
        {
            if (incident.Result == 2 && ActiveManufacturing(s)) return false;
            if (incident.Result == 2 && TargetInActiveRepair(s, incident.ToolId)) return false;
            if (!CapableWorker(s, actor) || AvailableHands(s, actor) < 1 || s.WorldTraversals.Any(x => x.ActorId == actor)
                || s.InventoryCombat && s.WorldSchedule.Order.Contains(actor)) return false;
            var body = s.Actors.Single(x => x.Id == actor);
            if (Math.Max(Math.Abs(body.X - 3), Math.Abs(body.Y - 3)) > 1) return false;
            if (incident.Result == 6 && actor != incident.LeadId) return false;
            if (incident.Result == 2 && actor != TestOnlyPolicy.CompanionId && !(actor == TestOnlyPolicy.ActorId && crafting.HeroProficient)) return false;
            return true;
        }
        private static void BookRemedy(Snapshot s, CraftingIncidentRecord incident)
        {
            string job = RemedyJobId(incident);
            s.Work = s.Work.CancelFutureWork(job, s.RuleClock);
            if (incident.Workers.Count == 0) return;
            var left = CampGreens.Subtract(incident.RequiredLabor, incident.Labor);
            var duration = new RuleTime(left.Numerator, checked(left.Denominator * incident.Workers.Count));
            var end = CampGreens.Add(s.RuleClock, duration); var window = ResearchWindowEnd(s.RuleClock).Value; if (window < end) end = window;
            foreach (string worker in incident.Workers.OrderBy(x => x, StringComparer.Ordinal)) {
                string id = "remedy." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture) + "." + worker;
                // A single command may stop several workers; the old interval is truncated first.
                if (s.Work.WorkerIntervals.Any(x => x.Id == id)) id += "." + s.Work.WorkerIntervals.Count.ToString(CultureInfo.InvariantCulture);
                s.Work = s.Work.Reserve(job, new[] { new WorkerInterval(id, job, worker, s.RuleClock, end) }, Array.Empty<ResourceReservation>());
            }
        }
        private string ResolveRemedy(Snapshot s, Command c)
        {
            var incident = s.CraftingIncidents.SingleOrDefault(x => x.Id == c.Target);
            if (incident == null) return "UnknownCraftingIncident";
            if (incident.Remedied) return "CraftingRemedyComplete";
            var workers = incident.Workers.ToList();
            if (c.Kind == CommandKind.PauseCraftRemedy) {
                if (!workers.Remove(c.Actor)) return "CraftRemedyNotWorking";
            } else {
                if (workers.Contains(c.Actor)) return "CraftRemedyAlreadyWorking";
                if (!RemedyCapable(s, incident, c.Actor)) return "CraftRemedyWorkerIneligible";
                if (!ResearchWindowEnd(s.RuleClock).HasValue) return "CraftWorkWindowClosed";
                if (OrdinaryInventory.Busy(s, c.Actor)) return "WorkerBusy";
                if (incident.Result != 5 && workers.Count != 0) return "CraftRemedySingleWorker";
                workers.Add(c.Actor);
            }
            var changed = incident.WithWork(s.RuleClock, incident.Labor, workers); PutIncident(s, changed); BookRemedy(s, changed); return null;
        }
        private void PauseIncompatibleRemedies(Snapshot s)
        {
            if (crafting == null) return;
            foreach (var incident in s.CraftingIncidents.Where(x => x.Workers.Count != 0).ToArray()) {
                var eligible = incident.Workers.Where(x => RemedyCapable(s, incident, x)).ToArray();
                if (eligible.Length == incident.Workers.Count) continue;
                var changed = incident.WithWork(s.RuleClock, incident.Labor, eligible); PutIncident(s, changed); BookRemedy(s, changed);
            }
        }
        private static RuleTime? NextRemedyBoundary(Snapshot s)
        {
            var ends = s.CraftingIncidents.Where(x => x.Workers.Count != 0).Select(x => s.Work.WorkerIntervals.First(w => w.JobId == RemedyJobId(x) && w.End > s.RuleClock).End).ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }
        private static void CreditRemedyWork(Snapshot s, RuleTime elapsed)
        {
            foreach (var incident in s.CraftingIncidents.Where(x => x.Workers.Count != 0).ToArray()) {
                var labor = CampGreens.Add(incident.Labor, new RuleTime(checked(elapsed.Numerator * incident.Workers.Count), elapsed.Denominator));
                var workers = labor == incident.RequiredLabor || !s.Work.WorkerIntervals.Any(w => w.JobId == RemedyJobId(incident) && w.End > s.RuleClock) ? Array.Empty<string>() : incident.Workers.ToArray();
                PutIncident(s, incident.WithWork(s.RuleClock, labor, workers));
            }
        }
    }
}
#endif
