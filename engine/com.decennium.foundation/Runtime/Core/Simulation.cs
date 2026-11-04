using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExecutionProfile { Laboratory, Release }
    public enum CommandKind { Move, Interact, AdvanceClock, ReserveWork, ConsumeReservation, ReleaseReservation,
        PlantCrop, TendCrop, HarvestCrop, PauseCrop, SetCropConditions,
        PortionInventory, HandleInventory, StartIntake, InterruptIntake, EnterInventoryCombat, StartWaterFill, PauseWaterFill, ResumeWaterFill, CancelWaterFill, HandleVessel, BeginFixedEncounter, EndRegularTurn, EncounterDash, SelectCombatStance, AttackClub, ResolveKnockout, StandFromProne, DropProne,
        AttackUnarmed, TacticalStep, RespondOpportunityAttack, RespondPress, Disengage, DispatchConditionEvent,
        BeginWorldStep, SuspendWorldStep, ResumeWorldStep, EndFixedEncounter,
        StartFormulaResearch, StartFormulaCopy, PauseFormulaWork, ResumeFormulaWork, CancelFormulaWork,
        DispatchCraftingMishap, StartCraftRemedy, PauseCraftRemedy,
        StartToolRepair, PauseToolRepair, ResumeToolRepair, CancelToolRepair,
        StartManufacturing, PauseManufacturing, ResumeManufacturing, CancelManufacturing, ResolveManufacturingQuality, UseAlchemyDose,
        HandlePortableEquipment, EquipPortableItem, RemovePortableItem, OpenPortableContainer, ClosePortableContainer }
    public enum Outcome { Rejected, Committed, Duplicate }

    // DTOs are detached copies. No caller ever receives the owned simulation state.
    public sealed class ActorState
    {
        public string Id;
        public int X, Y, Tokens;
        public ActorState Copy() => (ActorState)MemberwiseClone();
    }
    public sealed class ObjectState
    {
        public string Id;
        public int X, Y;
        public bool Opened;
        public ObjectState Copy() => (ObjectState)MemberwiseClone();
    }
    public sealed class CommandReceipt
    {
        public string Principal, Id, Fingerprint;
        public long Revision;
        public CommandReceipt Copy() => (CommandReceipt)MemberwiseClone();
    }
    public sealed class Snapshot
    {
        public const int Schema = 1;
        public const int WorkSchema = 2;
        public const int CropSchema = 3;
        public const int InventorySchema = 4;
        public const int VesselSchema = 5;
        public const int MovableVesselSchema = 6;
        public const int EncounterSchema = 7;
        public const int ActorLifeSchema = 8;
        public const int ClubAttackSchema = 9;
        public const int PostureSchema = 10;
        public const int TacticalMovementSchema = 11;
        public const int ConditionSchema = 12;
        public const int SharedWorldSchema = 13;
        public const int CalendarCombatSchema = 14;
        public const int FormulaWorkSchema = 15;
        public const int CraftingConsequenceSchema = 16;
        public const int RepairWorkSchema = 17;
        public const int ManufacturingSchema = 18;
        public const int SupplyCacheSchema = 19;
        public const int PortableEquipmentSchema = 20;
        public const int MaxCropBatches = 8;
        public const int MaxCropWorkRecords = 128;
        // Technical bound keeps the entire snapshot within the existing 1 MiB save limit,
        // including maximum-length identities and a full receipt history. Not a game rule.
        public const int MaxWorkRecords = 256;
        public int SchemaVersion = Schema;
        public string ContentFingerprint;
        public bool TestOnly;
        public long Revision, Clock;
        public uint RandomState;
        public ActorState[] Actors;
        public ObjectState[] Objects;
        public CommandReceipt[] Receipts;
        // Schema 1 uses synthetic Clock ticks only. Schema 2 uses exact RuleClock only,
        // with Clock fixed at zero. No conversion or implicit save migration exists.
        public RuleTime RuleClock;
        public WorkLedger Work;
        public CropBatchRecord[] Crops = Array.Empty<CropBatchRecord>();
        public CropPlotRecord[] CropPlots = Array.Empty<CropPlotRecord>();
        public CropFoodRecord[] CropFood = Array.Empty<CropFoodRecord>();
        public InventoryLotRecord[] InventoryLots = Array.Empty<InventoryLotRecord>();
        public IntakeRecord[] Intakes = Array.Empty<IntakeRecord>();
        public HandlingRecord[] Handling = Array.Empty<HandlingRecord>();
        public bool InventoryCombat;
        public string InventoryTurnActor = "";
        public int InventoryInteractions;
        public WaterVesselRecord[] Vessels = Array.Empty<WaterVesselRecord>();
        public VesselContentRecord[] VesselContents = Array.Empty<VesselContentRecord>();
        public WaterFillRecord[] WaterFills = Array.Empty<WaterFillRecord>();
        public VesselHandlingRecord[] VesselMoves = Array.Empty<VesselHandlingRecord>();
        public ActorCharacterRecord[] Characters = Array.Empty<ActorCharacterRecord>();
        public ActorLifeRecord[] Lives = Array.Empty<ActorLifeRecord>();
        public ActorLifeEvent[] LifeEvents = Array.Empty<ActorLifeEvent>();
        public ActorMovementRecord[] ActorMovement = Array.Empty<ActorMovementRecord>();
        public ClubInstance[] Clubs = Array.Empty<ClubInstance>();
        public StanceSelectionRecord[] Stances = Array.Empty<StanceSelectionRecord>();
        public MeleeAttackRecord[] MeleeAttacks = Array.Empty<MeleeAttackRecord>();
        public PressRecord[] Presses = Array.Empty<PressRecord>();
        public ActorTacticalRecord[] TacticalActors = Array.Empty<ActorTacticalRecord>();
        public TacticalMoveRecord[] TacticalMoves = Array.Empty<TacticalMoveRecord>();
        public PressOfferRecord[] PressOffers = Array.Empty<PressOfferRecord>();
        public ConditionJournal[] Conditions = Array.Empty<ConditionJournal>();
        public FixedEncounterRecord Encounter;
        public ClosedEncounterRecord[] ClosedEncounters = Array.Empty<ClosedEncounterRecord>();
        public WorldScheduleRecord WorldSchedule;
        public WorldIntervalRecord[] WorldIntervals = Array.Empty<WorldIntervalRecord>();
        public WorldTraversalRecord[] WorldTraversals = Array.Empty<WorldTraversalRecord>();
        public FormulaWorkRecord[] FormulaWork = Array.Empty<FormulaWorkRecord>();
        public DyingCadenceRecord[] DyingCadences = Array.Empty<DyingCadenceRecord>();
        public WorldLifeMarkerRecord[] WorldLifeMarkers = Array.Empty<WorldLifeMarkerRecord>();
        public ObjectStructureRecord[] Structures = Array.Empty<ObjectStructureRecord>();
        public CraftingIncidentRecord[] CraftingIncidents = Array.Empty<CraftingIncidentRecord>();
        public RepairWorkRecord[] RepairWork = Array.Empty<RepairWorkRecord>();
        public ManufacturingOrderRecord[] ManufacturingOrders = Array.Empty<ManufacturingOrderRecord>();
        public TradeProgressRecord[] Trades = Array.Empty<TradeProgressRecord>();
        public AlchemyDoseRecord[] AlchemyDoses = Array.Empty<AlchemyDoseRecord>();
        public ManufacturingAdvanceRecord ManufacturingAdvance;
        public SupplyCacheRecord[] SupplyCaches = Array.Empty<SupplyCacheRecord>();
        public SupplyCacheAttemptRecord[] SupplyCacheAttempts = Array.Empty<SupplyCacheAttemptRecord>();
        public SupplyCacheEquipmentRecord[] SupplyCacheEquipment = Array.Empty<SupplyCacheEquipmentRecord>();
        public PortableEquipmentRecord[] PortableEquipment = Array.Empty<PortableEquipmentRecord>();
        public PortableHandlingRecord[] PortableHandling = Array.Empty<PortableHandlingRecord>();
        public EncounterDashRecord[] EncounterDashes = Array.Empty<EncounterDashRecord>();
        public Snapshot Copy() => new Snapshot {
            DyingCadences = DyingCadences.ToArray(), Structures = Structures.ToArray(), CraftingIncidents = CraftingIncidents.ToArray(),
            WorldLifeMarkers = WorldLifeMarkers.ToArray(),
            RepairWork = RepairWork.ToArray(), ManufacturingOrders = ManufacturingOrders.ToArray(), Trades = Trades.ToArray(), AlchemyDoses = AlchemyDoses.ToArray(), ManufacturingAdvance = ManufacturingAdvance,
            SupplyCaches = SupplyCaches.ToArray(), SupplyCacheAttempts = SupplyCacheAttempts.ToArray(), SupplyCacheEquipment = SupplyCacheEquipment.ToArray(),
            PortableEquipment = PortableEquipment.ToArray(), PortableHandling = PortableHandling.ToArray(),
            FormulaWork = FormulaWork.ToArray(),
            WorldSchedule = WorldSchedule, WorldIntervals = WorldIntervals.ToArray(), WorldTraversals = WorldTraversals.ToArray(),
            Conditions = Conditions.ToArray(), ClosedEncounters = ClosedEncounters.ToArray(),
            TacticalActors = TacticalActors.ToArray(), TacticalMoves = TacticalMoves.ToArray(), PressOffers = PressOffers.ToArray(),
            ActorMovement = ActorMovement.ToArray(), Clubs = Clubs.ToArray(), Stances = Stances.ToArray(), MeleeAttacks = MeleeAttacks.ToArray(), Presses = Presses.ToArray(),
            Characters = Characters.ToArray(), Lives = Lives.ToArray(), LifeEvents = LifeEvents.ToArray(),
            Encounter = Encounter, EncounterDashes = EncounterDashes.ToArray(), VesselMoves = VesselMoves.ToArray(), Vessels = Vessels.ToArray(), VesselContents = VesselContents.ToArray(), WaterFills = WaterFills.ToArray(),
            InventoryLots = InventoryLots.ToArray(), Intakes = Intakes.ToArray(), Handling = Handling.ToArray(),
            InventoryCombat = InventoryCombat, InventoryTurnActor = InventoryTurnActor, InventoryInteractions = InventoryInteractions,
            SchemaVersion = SchemaVersion, RuleClock = RuleClock, Work = Work,
            Crops = Crops.ToArray(), CropFood = CropFood.ToArray(), CropPlots = CropPlots.ToArray(),
            ContentFingerprint = ContentFingerprint, TestOnly = TestOnly,
            Revision = Revision, Clock = Clock, RandomState = RandomState,
            Actors = Actors.Select(x => x.Copy()).ToArray(),
            Objects = Objects.Select(x => x.Copy()).ToArray(),
            Receipts = Receipts.Select(x => x.Copy()).ToArray()
        };
    }

    public sealed class Command
    {
        public string Id { get; }
        public string Actor { get; }
        public string Target { get; }
        public long ExpectedRevision { get; }
        public CommandKind Kind { get; }
        public int X { get; }
        public int Y { get; }
        public InventoryRequest Inventory { get; }
        public CombatRequest Combat { get; }
        public Command(string id, string actor, long revision, CommandKind kind,
            string target = "", int x = 0, int y = 0, InventoryRequest inventory = null, CombatRequest combat = null)
        { Id = id; Actor = actor; ExpectedRevision = revision; Kind = kind; Target = target; X = x; Y = y; Inventory = inventory; Combat = combat; }
        internal string Fingerprint => ((int)Kind).ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + Actor + "|" + Target + "|" + ExpectedRevision.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + X.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + Y.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + (Inventory == null ? "" : "|inventory-v1|" + Inventory.Fingerprint)
            + (Combat == null ? "" : "|" + Combat.FingerprintVersion + "|" + Combat.Fingerprint);
        // Structural history consistency only; receipts are not authentication credentials.
        public bool MatchesReceipt(CommandReceipt receipt) => receipt != null && ExpectedRevision >= 0
            && ExpectedRevision < long.MaxValue && receipt.Revision == ExpectedRevision + 1
            && receipt.Id == Id && receipt.Fingerprint == Fingerprint;
    }

    // Constructed by the trusted local/host adapter, never from a claimed command identity.
    // Pass the current grant each time so revocation also applies to duplicate requests.
    public sealed class Authority
    {
        public string Principal { get; }
        public bool CanAdvanceClock { get; }
        public bool CanModifyWorld { get; }
        private readonly HashSet<string> actors, inventoryOwners, willingRecipients;
        public Authority(string principal, IEnumerable<string> controlledActors, bool canAdvanceClock = false, bool canModifyWorld = false,
            IEnumerable<string> inventoryOwners = null, IEnumerable<string> willingRecipients = null)
        {
            if (!Validation.ValidId(principal) || controlledActors == null) throw new ArgumentException("Invalid authority.");
            Principal = principal; CanAdvanceClock = canAdvanceClock; CanModifyWorld = canModifyWorld;
            actors = new HashSet<string>(controlledActors, StringComparer.Ordinal);
            this.inventoryOwners = new HashSet<string>(inventoryOwners ?? Array.Empty<string>(), StringComparer.Ordinal);
            this.willingRecipients = new HashSet<string>(willingRecipients ?? Array.Empty<string>(), StringComparer.Ordinal);
            if (actors.Concat(this.inventoryOwners).Concat(this.willingRecipients).Any(x => !Validation.ValidId(x))) throw new ArgumentException("Invalid actor grant.");
        }
        public bool Controls(string actor) => actors.Contains(actor);
        public bool MayUseInventory(string owner) => inventoryOwners.Contains(owner);
        public bool ConsentsToHandover(string recipient) => willingRecipients.Contains(recipient);
    }

    public interface ICommandPolicy
    {
        string ContentFingerprint { get; }
        bool TestOnly { get; }
        // Return null for success. Work on the detached candidate only.
        string Resolve(Snapshot candidate, Command command);
        string ValidateState(Snapshot candidate);
    }
    /// <summary>Policy-resolved physical inputs; host authority remains outside client payloads.
    /// Called on detached state before duplicate handling and any mutation.</summary>
    public interface ICommandInventoryClaims
    {
        IEnumerable<string> RequiredInventoryOwners(Snapshot state, Command command);
    }

    public sealed class CommandResult
    {
        public Outcome Outcome { get; }
        public string Code { get; }
        public long Revision { get; }
        public bool IsSuspended { get; }
        internal CommandResult(Outcome outcome, string code, long revision, bool suspended = false)
        { Outcome = outcome; Code = code; Revision = revision; IsSuspended = suspended; }
    }

    public static class Validation
    {
        public const int MaxReceipts = 1024;
        public static bool ValidId(string value)
        {
            if (string.IsNullOrEmpty(value) || value.Length > 96) return false;
            return value.All(c => (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                || (c >= '0' && c <= '9') || c == '_' || c == '-' || c == '.');
        }
        public static void Snapshot(Snapshot s)
        {
            if (s == null || !ValidId(s.ContentFingerprint) || s.Revision < 0 || s.Clock < 0 || s.RandomState == 0)
                throw new ArgumentException("Invalid snapshot header.");
            if (s.SchemaVersion != Foundation.Snapshot.Schema && s.SchemaVersion != Foundation.Snapshot.WorkSchema
                && s.SchemaVersion != Foundation.Snapshot.CropSchema && s.SchemaVersion != Foundation.Snapshot.InventorySchema && s.SchemaVersion != Foundation.Snapshot.VesselSchema && s.SchemaVersion != Foundation.Snapshot.MovableVesselSchema && s.SchemaVersion != Foundation.Snapshot.EncounterSchema && s.SchemaVersion != Foundation.Snapshot.ActorLifeSchema && s.SchemaVersion != Foundation.Snapshot.ClubAttackSchema && s.SchemaVersion != Foundation.Snapshot.PostureSchema && s.SchemaVersion != Foundation.Snapshot.TacticalMovementSchema && s.SchemaVersion != Foundation.Snapshot.ConditionSchema && s.SchemaVersion != Foundation.Snapshot.SharedWorldSchema && s.SchemaVersion != Foundation.Snapshot.CalendarCombatSchema && s.SchemaVersion != Foundation.Snapshot.FormulaWorkSchema && s.SchemaVersion != Foundation.Snapshot.CraftingConsequenceSchema && s.SchemaVersion != Foundation.Snapshot.RepairWorkSchema && s.SchemaVersion != Foundation.Snapshot.ManufacturingSchema && s.SchemaVersion != Foundation.Snapshot.SupplyCacheSchema && s.SchemaVersion != Foundation.Snapshot.PortableEquipmentSchema)
                throw new ArgumentException("Unsupported snapshot schema.");
            if (s.SchemaVersion == Foundation.Snapshot.Schema && (s.Work != null || s.RuleClock != default))
                throw new ArgumentException("Legacy snapshot cannot contain unsaved work or exact time.");
            if (s.SchemaVersion >= Foundation.Snapshot.WorkSchema && (s.Work == null || s.Clock != 0
                || s.Work.Lots.Count > Foundation.Snapshot.MaxWorkRecords
                || s.Work.WorkerIntervals.Count > Foundation.Snapshot.MaxWorkRecords
                || s.Work.Reservations.Count > Foundation.Snapshot.MaxWorkRecords))
                throw new ArgumentException("Invalid work snapshot or session capacity exceeded.");
            if(s.SchemaVersion<Foundation.Snapshot.InventorySchema&&s.Work!=null&&s.Work.RequiresRationalSchema)throw new ArgumentException("Fractional/partial ledger requires an explicit later snapshot schema.");
            if (s.Crops == null || s.CropFood == null || s.CropPlots == null || s.Crops.Length > Foundation.Snapshot.MaxCropBatches
                || s.CropPlots.Length > Foundation.Snapshot.MaxCropBatches || s.CropPlots.Any(p => p == null)
                || s.CropFood.Length > Foundation.Snapshot.MaxCropBatches || s.Crops.Any(c => c == null) || s.CropFood.Any(f => f == null)
                || (s.SchemaVersion < Foundation.Snapshot.CropSchema && (s.Crops.Length != 0 || s.CropFood.Length != 0 || s.CropPlots.Length != 0)))
                throw new ArgumentException("Invalid crop snapshot collections or schema.");
            if (s.SchemaVersion >= Foundation.Snapshot.CropSchema && (s.Work.Lots.Count > Foundation.Snapshot.MaxCropWorkRecords
                || s.Work.WorkerIntervals.Count > Foundation.Snapshot.MaxCropWorkRecords
                || s.Work.Reservations.Count > Foundation.Snapshot.MaxCropWorkRecords))
                throw new ArgumentException("Crop session ledger capacity exceeded.");
            if (s.Actors == null || s.Objects == null || s.Receipts == null || s.Actors.Length == 0
                || s.Actors.Length > 64 || s.Objects.Length > 64 || s.Receipts.Length > MaxReceipts)
                throw new ArgumentException("Invalid snapshot counts.");
            if (s.Actors.Any(a => a == null || !ValidId(a.Id) || a.Tokens < 0)
                || s.Objects.Any(o => o == null || !ValidId(o.Id))) throw new ArgumentException("Invalid entity.");
            if (s.Actors.Select(a => a.Id).Concat(s.Objects.Select(o => o.Id)).Distinct(StringComparer.Ordinal).Count()
                != s.Actors.Length + s.Objects.Length) throw new ArgumentException("Duplicate entity ID.");
            if (s.Work != null && s.Work.WorkerIntervals.Any(w => !s.Actors.Any(a => a.Id == w.WorkerId)))
                throw new ArgumentException("Work interval references an unknown actor.");
            if (s.Crops.Select(c => c.Id).Distinct(StringComparer.Ordinal).Count() != s.Crops.Length
                || s.CropPlots.Select(p => p.Id).Distinct(StringComparer.Ordinal).Count() != s.CropPlots.Length
                || s.Crops.SelectMany(c => c.Tasks).Select(t => t.Id).Distinct(StringComparer.Ordinal).Count() != s.Crops.Sum(c => c.Tasks.Count)
                || s.CropFood.Select(f => f.LotId).Distinct(StringComparer.Ordinal).Count() != s.CropFood.Length
                || s.CropFood.Select(f => f.BatchId).Distinct(StringComparer.Ordinal).Count() != s.CropFood.Length)
                throw new ArgumentException("Duplicate crop, work or output identity.");
            foreach (var crop in s.Crops)
            {
                if (crop.UpdatedAt != s.RuleClock || !s.Work.Lots.Any(l => l.Id == crop.SeedLotId) || !s.CropPlots.Any(p => p.Id == crop.PlotId))
                    throw new ArgumentException("Crop clock or seed provenance mismatch.");
                foreach (var task in crop.Tasks)
                    if (!s.Actors.Any(a => a.Id == task.WorkerId)
                        || task.InputReservations.Any(id => !s.Work.Reservations.Any(r => r.Id == id && r.JobId == task.Id)))
                        throw new ArgumentException("Unknown crop worker or input reservation.");
            }
            if (s.CropFood.Any(f => !s.Crops.Any(c => c.Id == f.BatchId) || !s.Work.Lots.Any(l => l.Id == f.LotId)))
                throw new ArgumentException("Unknown crop output lot or source batch.");
            if (s.Receipts.Any(r => r == null || !ValidId(r.Principal) || !ValidId(r.Id)
                || string.IsNullOrEmpty(r.Fingerprint) || r.Fingerprint.Length > 512
                || r.Fingerprint.Any(c => c < 32 || c > 126) || r.Revision < 1 || r.Revision > s.Revision))
                throw new ArgumentException("Invalid receipt.");
            if (s.Receipts.Select(r => r.Principal + "|" + r.Id).Distinct(StringComparer.Ordinal).Count() != s.Receipts.Length)
                throw new ArgumentException("Duplicate receipt.");
            InventoryValidation.Validate(s);
            WaterVesselValidation.Validate(s);
            VesselHandlingValidation.Validate(s);
            EncounterHistory.Validate(s);
            FixedEncounterValidation.Validate(s);
            ActorLifeValidation.Validate(s);
            ClubAttackValidation.Validate(s);
            ActorMovementValidation.Validate(s);
            TacticalMovementValidation.Validate(s);
            ActorConditionValidation.Validate(s);
            WorldScheduleValidation.Validate(s);
            FormulaWorkValidation.Validate(s);
            CraftingConsequenceValidation.Validate(s);
            RepairWorkValidation.Validate(s);
            ManufacturingValidation.Validate(s);
            SupplyCacheValidation.Validate(s);
            PortableEquipmentValidation.Validate(s);
        }
    }

    // Single-threaded host owner. Network transport, cadence and production rules are outside this increment.
    public sealed class Simulation
    {
        private Snapshot state;
        private readonly ICommandPolicy policy;
        public Simulation(ICommandPolicy policy, Snapshot initial, ExecutionProfile profile)
        {
            this.policy = policy ?? throw new ArgumentNullException(nameof(policy));
            if (!Enum.IsDefined(typeof(ExecutionProfile), profile)) throw new ArgumentException("Invalid profile.");
            ValidateCandidate(initial);
            if (profile == ExecutionProfile.Release && (policy.TestOnly || initial.TestOnly))
                throw new InvalidOperationException("TEST_ONLY content is forbidden in release.");
            state = initial.Copy();
        }
        public Snapshot Capture() => state.Copy();
        private void ValidateCandidate(Snapshot candidate)
        {
            Validation.Snapshot(candidate);
            if (candidate.ContentFingerprint != policy.ContentFingerprint || candidate.TestOnly != policy.TestOnly)
                throw new ArgumentException("Content fingerprint or scope mismatch.");
            string error = policy.ValidateState(candidate);
            if (error != null) throw new ArgumentException(error);
        }
        public CommandResult Execute(Authority authority, Command command)
        {
            if (authority == null || command == null || !Validation.ValidId(command.Id)
                || !Validation.ValidId(command.Actor) || command.Target == null || command.Target.Length > 96
                || (command.Target.Length != 0 && !Validation.ValidId(command.Target)) || command.ExpectedRevision < 0
                || !Enum.IsDefined(typeof(CommandKind), command.Kind)) return Reject("InvalidCommand");
            bool combatKind=command.Kind==CommandKind.SelectCombatStance||command.Kind==CommandKind.AttackClub||command.Kind==CommandKind.ResolveKnockout
                ||command.Kind==CommandKind.AttackUnarmed||command.Kind==CommandKind.RespondOpportunityAttack||command.Kind==CommandKind.RespondPress;
            if(combatKind!=(command.Combat!=null)||command.Combat!=null&&command.Inventory!=null)return Reject("UnexpectedCombatPayload");
            if (!authority.Controls(command.Actor) || (command.Kind == CommandKind.AdvanceClock && !authority.CanAdvanceClock)
                || ((command.Kind == CommandKind.SetCropConditions || command.Kind == CommandKind.EnterInventoryCombat || command.Kind == CommandKind.BeginFixedEncounter || command.Kind == CommandKind.EndFixedEncounter || command.Kind == CommandKind.DispatchConditionEvent || command.Kind == CommandKind.DispatchCraftingMishap) && !authority.CanModifyWorld))
                return Reject("NotAuthorized");
            if (policy is ICommandInventoryClaims claims) {
                try {
                    if (claims.RequiredInventoryOwners(state.Copy(), command).Any(owner => !Validation.ValidId(owner) || !authority.MayUseInventory(owner))) return Reject("InventoryNotAuthorized");
                } catch (Exception ex) when (ex is ArgumentException || ex is InvalidOperationException || ex is OverflowException) { return Reject("InvalidInventoryClaims"); }
            }
            if (command.Kind == CommandKind.PortionInventory || command.Kind == CommandKind.HandleInventory || command.Kind == CommandKind.StartIntake) {
                var source = state.InventoryLots.FirstOrDefault(x => x.LotId == command.Target);
                if (source != null && !authority.MayUseInventory(source.OwnerId)) return Reject("InventoryNotAuthorized");
                if (command.Kind == CommandKind.StartIntake && source != null && state.Vessels.Length != 0) {
                    var lot = state.Work.Lots.First(x => x.Id == source.LotId);
                    var vessel = state.Vessels.FirstOrDefault(x => x.Id == lot.LocationId);
                    if (vessel != null && !authority.MayUseInventory(vessel.OwnerId)) return Reject("InventoryNotAuthorized");
                }
                if (command.Kind == CommandKind.HandleInventory && command.Inventory != null
                    && command.Inventory.Handling == HandlingKind.Handover && !authority.ConsentsToHandover(command.Inventory.Destination))
                    return Reject("RecipientNotWilling");
            }
            if(command.Kind==CommandKind.HandlePortableEquipment||command.Kind==CommandKind.EquipPortableItem||command.Kind==CommandKind.RemovePortableItem
                ||command.Kind==CommandKind.OpenPortableContainer||command.Kind==CommandKind.ClosePortableContainer) {
                var item=state.PortableEquipment.FirstOrDefault(x=>x.Id==command.Target);
                if(item!=null&&!authority.MayUseInventory(item.OwnerId))return Reject("InventoryNotAuthorized");
                if(command.Kind==CommandKind.HandlePortableEquipment&&command.Inventory!=null&&command.Inventory.Handling==HandlingKind.Handover
                    &&!authority.ConsentsToHandover(command.Inventory.Destination))return Reject("RecipientNotWilling");
            }
            if (command.Kind == CommandKind.StartWaterFill || command.Kind == CommandKind.ResumeWaterFill) {
                var fill = command.Kind == CommandKind.ResumeWaterFill ? state.WaterFills.FirstOrDefault(x => x.Id == command.Target) : null;
                var source = state.InventoryLots.FirstOrDefault(x => x.LotId == (fill == null ? command.Target : fill.SourceLotId));
                var vessel = state.Vessels.FirstOrDefault(x => x.Id == (fill == null ? command.Inventory?.Destination : fill.DestinationId));
                var sourceLot = source == null ? null : state.Work.Lots.FirstOrDefault(x => x.Id == source.LotId);
                var sourceVessel = sourceLot == null ? null : state.Vessels.FirstOrDefault(x => x.Id == sourceLot.LocationId);
                if ((source != null && !authority.MayUseInventory(source.OwnerId)) || (vessel != null && !authority.MayUseInventory(vessel.OwnerId))
                    || (sourceVessel != null && !authority.MayUseInventory(sourceVessel.OwnerId)))
                    return Reject("InventoryNotAuthorized");
            }
            if (command.Kind == CommandKind.HandleVessel) {
                var vessel = state.Vessels.FirstOrDefault(v => v.Id == command.Target);
                if (vessel != null && (!authority.MayUseInventory(vessel.OwnerId) || state.VesselContents.Where(x => x.VesselId == vessel.Id)
                    .Any(x => state.Work.Lots.First(l => l.Id == x.LotId).Amount != default
                        && !authority.MayUseInventory(state.InventoryLots.First(l => l.LotId == x.LotId).OwnerId)))) return Reject("InventoryNotAuthorized");
                if (command.Inventory != null && command.Inventory.Handling == HandlingKind.Handover
                    && !authority.ConsentsToHandover(command.Inventory.Destination)) return Reject("RecipientNotWilling");
            }
            // The admitted copying command uses its actor-owned writing allotment. Resume also
            // rechecks that owner's current grant before duplicate handling or deferred spending.
            if (command.Kind == CommandKind.StartFormulaCopy && !authority.MayUseInventory(command.Actor)) return Reject("InventoryNotAuthorized");
            if (command.Kind == CommandKind.StartCraftRemedy) {
                var incident = state.CraftingIncidents.FirstOrDefault(x => x.Id == command.Target && x.Result == 2);
                var tool = incident == null ? null : state.Structures.FirstOrDefault(x => x.Id == incident.ToolId);
                if (tool != null && !authority.MayUseInventory(tool.OwnerId)) return Reject("InventoryNotAuthorized");
            }
            if (command.Kind == CommandKind.ResumeFormulaWork) {
                var job = state.FormulaWork.FirstOrDefault(x => x.Id == command.Target && x.Kind == FormulaWorkKind.Copy);
                if (job != null && !authority.MayUseInventory(job.WorkerId)) return Reject("InventoryNotAuthorized");
            }
            if(command.Kind==CommandKind.AttackClub||command.Kind==CommandKind.RespondOpportunityAttack&&command.Combat.Choice) {
                var club=state.Clubs.FirstOrDefault(w=>w.Id==command.Combat.WeaponId);
                if(club!=null&&!authority.MayUseInventory(club.OwnerId))return Reject("InventoryNotAuthorized");
            }
            CommandReceipt previous = state.Receipts.FirstOrDefault(r => r.Principal == authority.Principal && r.Id == command.Id);
            if (previous != null)
                return previous.Fingerprint == command.Fingerprint
                    ? new CommandResult(Outcome.Duplicate, (state.ManufacturingAdvance?.CommandId==command.Id && state.ManufacturingAdvance.CommandRevision==previous.Revision)?"AlreadyAcceptedSuspended":"AlreadyCommitted", previous.Revision,(state.ManufacturingAdvance?.CommandId==command.Id && state.ManufacturingAdvance.CommandRevision==previous.Revision)) : Reject("CommandIdConflict");
            if (command.ExpectedRevision != state.Revision) return Reject("StaleRevision");
            if (!state.Actors.Any(a => a.Id == command.Actor)) return Reject("UnknownActor");
            if (state.Revision == long.MaxValue || state.Receipts.Length == (state.SchemaVersion >= Snapshot.InventorySchema ? 512 : Validation.MaxReceipts)) return Reject("SessionCapacityReached");
            Snapshot candidate = state.Copy();
            string failure;
            try { failure = policy.Resolve(candidate, command); }
            catch (Exception ex) when (ex is ArgumentException || ex is OverflowException || ex is InvalidOperationException)
            { return Reject("PolicyFailure"); }
            if (failure != null) return Reject(failure);
            if (candidate.SchemaVersion != state.SchemaVersion) return Reject("SchemaChangeForbidden");
            // Policy cannot rewrite command history, revision, identity or content scope.
            candidate.Revision = state.Revision + 1;
            candidate.Receipts = state.Receipts.Select(r => r.Copy()).Concat(new[] { new CommandReceipt {
                Principal = authority.Principal, Id = command.Id, Fingerprint = command.Fingerprint, Revision = candidate.Revision
            }}).ToArray();
            if (candidate.Clock < state.Clock || candidate.RuleClock < state.RuleClock) return Reject("ClockReversal");
            try { ValidateCandidate(candidate); }
            catch (ArgumentException) { return Reject("InvalidResult"); }
            state = candidate.Copy();
            return new CommandResult(Outcome.Committed, state.ManufacturingAdvance?.CommandId==command.Id?"AcceptedSuspended":"Committed", state.Revision,state.ManufacturingAdvance?.CommandId==command.Id);
        }
        private CommandResult Reject(string reason) => new CommandResult(Outcome.Rejected, reason, state.Revision);
    }

    public static class RandomV1
    {
        public const string Algorithm = "xorshift32-v1";
        public static uint Next(ref uint state)
        {
            if (state == 0) throw new ArgumentException("RNG state cannot be zero.");
            unchecked { state ^= state << 13; state ^= state >> 17; state ^= state << 5; }
            return state;
        }
    }
}
