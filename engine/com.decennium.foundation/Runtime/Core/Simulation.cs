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
        HandlePortableEquipment, EquipPortableItem, RemovePortableItem, OpenPortableContainer, ClosePortableContainer,
        AwardCharacterMilestone, AdvanceCharacterLevel, ActivateTacticalReposition, TacticalRepositionStep,
        AttackRepeatingCrossbow, ReloadRepeatingCrossbow, DispatchFixturePeriodicRider, CurePeriodicRider,
        SetPeriodicRiderSuppression, SetPeriodicFamilyImmunity, ApplyFixtureMagicalHealing, DesignateOverwatch,
        RespondOverwatch, ResolveOverwatchRider, DoffPortableShield, WarningShot, CoveringFire, TacticalAssessment, OfferCommandStep, RespondCommandStep,
        SuppressionFire, ActivateDefensiveFormation, RespondDefensiveFormation,
        AssignExpeditionWork, CancelExpeditionWork, StartExpeditionWork,
        StartHarvest, PauseHarvest, ResumeHarvest, StartMining, PauseMining, ResumeMining,
        StartProspecting, PauseProspecting, ResumeProspecting, RecordProspectingExposure,
        StartMiningAssay, PauseMiningAssay, ResumeMiningAssay, CancelMiningAssay,
        StartMineralPreparation, PauseMineralPreparation, ResumeMineralPreparation, Hide, Search,
        StartRouteTravel, PauseRouteTravel, ResumeRouteTravel, ConsumeTestOnlyRouteMappingResult, Dodge,
        PauseCacheExcavation, ResumeCacheExcavation, Ready, RespondReady,
        StartRouteMappingWork, PauseRouteMappingWork, ResumeRouteMappingWork,
        StartRouteReconnaissance, PauseRouteReconnaissance, ResumeRouteReconnaissance,
        ScheduleRestWatch, BeginRest, InterruptRest, ResolveExpeditionStrainRecovery,
        BeginMoraleRest, InterruptMoraleRest, BeginHavenCare, InterruptHavenCare,
        BeginCampUse, EndCampUse, BeginLyingLow, EndLyingLow,
        StartTemporaryCampConstruction, PauseTemporaryCampConstruction,
        ResumeTemporaryCampConstruction, ResolveTemporaryCampConstruction,
        StartRecipe347, PauseRecipe347, ResumeRecipe347, CancelRecipe347, ResolveRecipe347Quality,
        StartHarvestRequirementWork, PauseHarvestRequirementWork, ResumeHarvestRequirementWork,
        StartHarvestPreservationTreatment, RecordHarvestPreservationExposure,
        HandoverFishingTrapResponsibility }
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
        public const int CharacterAdvancementSchema = 21;
        public const int RepeatingCrossbowSchema = 22;
        public const int PeriodicRiderSchema = 23;
        public const int SharedBonusActionSchema = 24;
        public const int OverwatchSchema = 25;
        public const int OverwatchExecutionSchema = 26;
        public const int SoldierInitialLoadoutSchema = 27;
        public const int SoldierInitialBuildSchema = 28;
        public const int SoldierTacticalTechniquesSchema = 29;
        public const int CharacterAdvancementHistorySchema = 30;
        public const int TacticalAssessmentSchema = 31;
        public const int CommandStepSchema = 32;
        public const int SuppressionFireSchema = 33;
        public const int DefensiveFormationSchema = 34;
        public const int FishingTrapLegacySchema = 35;
        public const int FishingTrapBaitSchema = 36;
        public const int FishingTrapSchema = 37;
        public const int FishingStockSchema = 38;
        public const int ExpeditionAssignmentSchema = 39;
        public const int OffCalendarActivitySchema = 40;
        public const int HarvestSchema = 41;
        public const int HarvestManifestSchema = 42;
        public const int MiningSchema = 43;
        public const int ProspectingSchema = 44;
        public const int MiningAssaySchema = 45;
        public const int DestructiveMiningAssaySchema = 46;
        public const int MiningExpeditionAssignmentSchema = 47;
        public const int MineralPreparationSchema = 48;
        public const int MiningToolCandidateSchema = 49;
        public const int OrdinaryReceptacleSchema = 50;
        public const int ObservationSchema = 51;
        public const int ExpeditionRouteSchema = 52;
        public const int RouteObservationSchema = 53;
        public const int RouteMappingSchema = 54;
        public const int HuntingTrapSchema = 55;
        public const int DodgeSchema = 56;
        public const int BuriedCacheSchema = 57;
        public const int ReadyActionSchema = 58;
        public const int RouteMappingWorkSchema = 59;
        public const int RouteReconnaissanceSchema = 60;
        public const int SharedCharacterAdvancementSchema = 61;
        public const int DailyProvisioningSchema = 62;
        public const int RestDebtSchema = 63;
        public const int ExpeditionStrainRecoverySchema = 64;
        public const int MoraleRestSchema = 65;
        public const int HavenCareSchema = 66;
        public const int ExpeditionPressureSchema = 67;
        public const int ExpeditionPressureLifecycleSchema = 68;
        public const int ExpeditionCampUseSchema = 69;
        public const int TemporaryCampConstructionSchema = 70;
        public const int PortableStorageSchema = 71;
        public const int Recipe347Schema = 72;
        public const int PortableCountedLotSchema = 73;
        public const int HarvestPreservationSchema = 74;
        public const int HarvestPreservationTreatmentSchema = 75;
        public const int HarvestPreservationExposureSchema = 76;
        public const int MiningAssistantSchema = 77;
        public const int MaxActors = 64;
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
        public DodgeRecord[] Dodges = Array.Empty<DodgeRecord>();
        public ReadyActionRecord[] ReadyActions = Array.Empty<ReadyActionRecord>();
        public ReadyOccurrenceRecord[] ReadyOccurrences = Array.Empty<ReadyOccurrenceRecord>();
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
        public BuriedCacheSiteRecord[] BuriedCacheSites = Array.Empty<BuriedCacheSiteRecord>();
        public CacheExcavationRecord[] CacheExcavations = Array.Empty<CacheExcavationRecord>();
        public PortableEquipmentRecord[] PortableEquipment = Array.Empty<PortableEquipmentRecord>();
        public PortableHandlingRecord[] PortableHandling = Array.Empty<PortableHandlingRecord>();
        public PortableStorageProfileRecord[] PortableStorageProfiles = Array.Empty<PortableStorageProfileRecord>();
        public EncounterDashRecord[] EncounterDashes = Array.Empty<EncounterDashRecord>();
        public CharacterMilestoneRecord[] CharacterMilestones = Array.Empty<CharacterMilestoneRecord>();
        public CharacterHitDieRecord[] CharacterHitDice = Array.Empty<CharacterHitDieRecord>();
        public CharacterFeatureGrantRecord[] CharacterFeatureGrants = Array.Empty<CharacterFeatureGrantRecord>();
        public CharacterAdvancementRecord[] CharacterAdvancements = Array.Empty<CharacterAdvancementRecord>();
        public CharacterFeatureRuntimeRecord[] CharacterFeatureRuntime = Array.Empty<CharacterFeatureRuntimeRecord>();
        public TacticalCoverRecord[] TacticalCovers = Array.Empty<TacticalCoverRecord>();
        public RepeatingCrossbowRecord[] RepeatingCrossbows = Array.Empty<RepeatingCrossbowRecord>();
        public AmmunitionLotRecord[] AmmunitionLots = Array.Empty<AmmunitionLotRecord>();
        public RangedCombatantRecord[] RangedCombatants = Array.Empty<RangedCombatantRecord>();
        public RangedAttackRecord[] RangedAttacks = Array.Empty<RangedAttackRecord>();
        public PeriodicRiderRecord[] PeriodicRiders = Array.Empty<PeriodicRiderRecord>();
        public PeriodicRiderEventRecord[] PeriodicRiderEvents = Array.Empty<PeriodicRiderEventRecord>();
        public PeriodicFamilyImmunityRecord[] PeriodicImmunities = Array.Empty<PeriodicFamilyImmunityRecord>();
        public SkillTrainingRecord[] SkillTraining = Array.Empty<SkillTrainingRecord>();
        public ActorBonusActionRecord[] BonusActions = Array.Empty<ActorBonusActionRecord>();
        public CharacterInitialClassSelectionRecord[] InitialClassSelections = Array.Empty<CharacterInitialClassSelectionRecord>();
        public CharacterInitialLoadoutRecord[] InitialCharacterLoadouts = Array.Empty<CharacterInitialLoadoutRecord>();
        public ShieldStationarityRecord[] ShieldStationarity = Array.Empty<ShieldStationarityRecord>();
        public OverwatchIntervalRecord[] OverwatchIntervals = Array.Empty<OverwatchIntervalRecord>();
        public OverwatchDesignationRecord[] OverwatchDesignations = Array.Empty<OverwatchDesignationRecord>();
        public OverwatchOfferRecord[] OverwatchOffers = Array.Empty<OverwatchOfferRecord>();
        public OverwatchRiderChoiceRecord[] OverwatchRiderChoices = Array.Empty<OverwatchRiderChoiceRecord>();
        public TacticalAllyRecord[] TacticalAllies = Array.Empty<TacticalAllyRecord>();
        public SoldierTacticalEffectRecord[] SoldierTacticalEffects = Array.Empty<SoldierTacticalEffectRecord>();
        public TacticalAttackAuditRecord[] TacticalAttackAudits = Array.Empty<TacticalAttackAuditRecord>();
        public TacticalAssessmentRecord[] TacticalAssessments = Array.Empty<TacticalAssessmentRecord>();
        public CommandStepOfferRecord[] CommandStepOffers = Array.Empty<CommandStepOfferRecord>();
        public SuppressionFireVolleyRecord[] SuppressionFireVolleys = Array.Empty<SuppressionFireVolleyRecord>();
        public SuppressionSlowRecord[] SuppressionSlows = Array.Empty<SuppressionSlowRecord>();
        public DefensiveFormationActivationRecord[] DefensiveFormations = Array.Empty<DefensiveFormationActivationRecord>();
        public FishingTrapAttemptRecord[] FishingTrapAttempts = Array.Empty<FishingTrapAttemptRecord>();
        public FishingOpportunityRecord[] FishingOpportunities = Array.Empty<FishingOpportunityRecord>();
        public FishingStockManifestRecord[] FishingStockManifests = Array.Empty<FishingStockManifestRecord>();
        public FishingStockAllocationRecord[] FishingStockAllocations = Array.Empty<FishingStockAllocationRecord>();
        public FishingCreatureBodyRecord[] FishingCreatures = Array.Empty<FishingCreatureBodyRecord>();
        public FishingTrapPhysicalRecord[] FishingTraps = Array.Empty<FishingTrapPhysicalRecord>();
        public FishingReceiveLocationRecord[] FishingReceiveLocations = Array.Empty<FishingReceiveLocationRecord>();
        public FishingTrapRetrievalRecord[] FishingTrapRetrievals = Array.Empty<FishingTrapRetrievalRecord>();
        public ExpeditionWorkAssignmentRecord[] ExpeditionAssignments = Array.Empty<ExpeditionWorkAssignmentRecord>();
        public WorldActivityIntervalRecord[] WorldActivityIntervals = Array.Empty<WorldActivityIntervalRecord>();
        public HarvestDonorRecord[] HarvestDonors = Array.Empty<HarvestDonorRecord>();
        public HarvestManifestRecord[] HarvestManifests = Array.Empty<HarvestManifestRecord>();
        public HarvestCategoryRecord[] HarvestCategories = Array.Empty<HarvestCategoryRecord>();
        public HarvestMaterialUnitRecord[] HarvestUnits = Array.Empty<HarvestMaterialUnitRecord>();
        public HarvestAttemptRecord[] HarvestAttempts = Array.Empty<HarvestAttemptRecord>();
        public HarvestRequirementWorkRecord[] HarvestRequirementWorks = Array.Empty<HarvestRequirementWorkRecord>();
        public HarvestPreservationTreatmentAttemptRecord[] HarvestPreservationTreatmentAttempts = Array.Empty<HarvestPreservationTreatmentAttemptRecord>();
        public HarvestPreservationEvidenceRecord[] HarvestPreservationEvidence = Array.Empty<HarvestPreservationEvidenceRecord>();
        public MiningDepositRecord[] MiningDeposits = Array.Empty<MiningDepositRecord>();
        public MiningCategoryRecord[] MiningCategories = Array.Empty<MiningCategoryRecord>();
        public MiningMaterialUnitRecord[] MiningUnits = Array.Empty<MiningMaterialUnitRecord>();
        public MiningAttemptRecord[] MiningAttempts = Array.Empty<MiningAttemptRecord>();
        public ProspectingPatchRecord[] ProspectingPatches = Array.Empty<ProspectingPatchRecord>();
        public ProspectingExposureRecord[] ProspectingExposures = Array.Empty<ProspectingExposureRecord>();
        public ProspectingAttemptRecord[] ProspectingAttempts = Array.Empty<ProspectingAttemptRecord>();
        public MiningAssayProfileRecord[] MiningAssayProfiles = Array.Empty<MiningAssayProfileRecord>();
        public MiningAssayAttemptRecord[] MiningAssayAttempts = Array.Empty<MiningAssayAttemptRecord>();
        public MiningAssaySampleRecord[] MiningAssaySamples = Array.Empty<MiningAssaySampleRecord>();
        public DestructiveMiningAssayProfileRecord[] DestructiveMiningAssayProfiles = Array.Empty<DestructiveMiningAssayProfileRecord>();
        public DestructiveMiningAssayAttemptRecord[] DestructiveMiningAssayAttempts = Array.Empty<DestructiveMiningAssayAttemptRecord>();
        public MineralPreparationProfileRecord[] MineralPreparationProfiles = Array.Empty<MineralPreparationProfileRecord>();
        public MineralPreparationAttemptRecord[] MineralPreparationAttempts = Array.Empty<MineralPreparationAttemptRecord>();
        public MiningToolCandidateProfileRecord[] MiningToolCandidateProfiles = Array.Empty<MiningToolCandidateProfileRecord>();
        public MiningToolInstanceStateRecord[] MiningToolInstanceStates = Array.Empty<MiningToolInstanceStateRecord>();
        public MiningToolUseRecord[] MiningToolUses = Array.Empty<MiningToolUseRecord>();
        public TestOnlyRecipe347FormulaAccessRecord[] Recipe347FormulaAccess = Array.Empty<TestOnlyRecipe347FormulaAccessRecord>();
        public TestOnlyTradeSpecialtyRecord[] Recipe347TradeSpecialties = Array.Empty<TestOnlyTradeSpecialtyRecord>();
        public TestOnlyRecipe347WorkshopRecord[] Recipe347Workshops = Array.Empty<TestOnlyRecipe347WorkshopRecord>();
        public Recipe347WorkOrderRecord[] Recipe347WorkOrders = Array.Empty<Recipe347WorkOrderRecord>();
        public Recipe347OutputProvenanceRecord[] Recipe347Outputs = Array.Empty<Recipe347OutputProvenanceRecord>();
        public Recipe347MiningToolProfileRecord[] Recipe347MiningToolProfiles = Array.Empty<Recipe347MiningToolProfileRecord>();
        public Recipe347MiningToolUseEvidenceRecord[] Recipe347MiningToolUseEvidence = Array.Empty<Recipe347MiningToolUseEvidenceRecord>();
        public Recipe347MiningToolWorkSegmentRecord[] Recipe347MiningToolWorkSegments = Array.Empty<Recipe347MiningToolWorkSegmentRecord>();
        public OrdinaryReceptacleLockRecord[] OrdinaryReceptacleLocks = Array.Empty<OrdinaryReceptacleLockRecord>();
        public OrdinaryReceptacleAttemptRecord[] OrdinaryReceptacleAttempts = Array.Empty<OrdinaryReceptacleAttemptRecord>();
        public int ObservationMapWidth, ObservationMapHeight;
        public ObservationMapCellRecord[] ObservationCells = Array.Empty<ObservationMapCellRecord>();
        public ObservationProfileRecord[] ObservationProfiles = Array.Empty<ObservationProfileRecord>();
        public ObservationActionRecord[] ObservationActions = Array.Empty<ObservationActionRecord>();
        public ObservationHideResultRecord[] ObservationHideResults = Array.Empty<ObservationHideResultRecord>();
        public ObserverKnowledgeRecord[] ObserverKnowledge = Array.Empty<ObserverKnowledgeRecord>();
        public ExpeditionRouteTravelRecord[] RouteTravels = Array.Empty<ExpeditionRouteTravelRecord>();
        public ExpeditionRouteSpatialRecord[] RouteTravelSpatial = Array.Empty<ExpeditionRouteSpatialRecord>();
        public ExpeditionRouteMappingResultRecord[] RouteMappingResults = Array.Empty<ExpeditionRouteMappingResultRecord>();
        public ExpeditionRouteMappingWorkAttemptRecord[] RouteMappingWorkAttempts = Array.Empty<ExpeditionRouteMappingWorkAttemptRecord>();
        public ExpeditionRouteSegmentRecord[] RouteSegments = Array.Empty<ExpeditionRouteSegmentRecord>();
        public ExpeditionRouteReconnaissanceAttemptRecord[] RouteReconnaissanceAttempts = Array.Empty<ExpeditionRouteReconnaissanceAttemptRecord>();
        public DailyProvisioningSettlementRecord[] DailyProvisioningSettlements = Array.Empty<DailyProvisioningSettlementRecord>();
        public DailyProvisioningConsumptionRecord[] DailyProvisioningConsumption = Array.Empty<DailyProvisioningConsumptionRecord>();
        public ExpeditionStrainGainRecord[] ExpeditionStrainGains = Array.Empty<ExpeditionStrainGainRecord>();
        public ExpeditionDashLockRecord[] ExpeditionDashLocks = Array.Empty<ExpeditionDashLockRecord>();
        public RestWatchScheduleRecord[] RestWatchSchedules = Array.Empty<RestWatchScheduleRecord>();
        public RestIntervalRecord[] RestIntervals = Array.Empty<RestIntervalRecord>();
        public RestWatchOutcomeRecord[] RestWatchOutcomes = Array.Empty<RestWatchOutcomeRecord>();
        public RestDebtEventRecord[] RestDebtEvents = Array.Empty<RestDebtEventRecord>();
        public ExpeditionStrainRecoveryGateUpdateRecord[] ExpeditionStrainRecoveryGateUpdates = Array.Empty<ExpeditionStrainRecoveryGateUpdateRecord>();
        public ExpeditionBeneficialRestRecord[] ExpeditionBeneficialRests = Array.Empty<ExpeditionBeneficialRestRecord>();
        public ExpeditionStrainRecoveryOfferRecord[] ExpeditionStrainRecoveryOffers = Array.Empty<ExpeditionStrainRecoveryOfferRecord>();
        public ExpeditionStrainRemovalRecord[] ExpeditionStrainRemovals = Array.Empty<ExpeditionStrainRemovalRecord>();
        public ExpeditionMoraleRestIntervalRecord[] ExpeditionMoraleRestIntervals = Array.Empty<ExpeditionMoraleRestIntervalRecord>();
        public ExpeditionMoraleRestBenefitRecord[] ExpeditionMoraleRestBenefits = Array.Empty<ExpeditionMoraleRestBenefitRecord>();
        public ExpeditionHavenCareIntervalRecord[] ExpeditionHavenCareIntervals = Array.Empty<ExpeditionHavenCareIntervalRecord>();
        public ExpeditionHavenCareAssessmentRecord[] ExpeditionHavenCareAssessments = Array.Empty<ExpeditionHavenCareAssessmentRecord>();
        public ExpeditionPressureCohortRecord[] ExpeditionPressureCohorts = Array.Empty<ExpeditionPressureCohortRecord>();
        public ExpeditionPressureExposureRecord[] ExpeditionPressureExposures = Array.Empty<ExpeditionPressureExposureRecord>();
        public ExpeditionPressureChangeRecord[] ExpeditionPressureChanges = Array.Empty<ExpeditionPressureChangeRecord>();
        public ExpeditionPressureCheckpointRecord[] ExpeditionPressureCheckpoints = Array.Empty<ExpeditionPressureCheckpointRecord>();
        public ExpeditionCampSiteRecord[] ExpeditionCampSites = Array.Empty<ExpeditionCampSiteRecord>();
        public ExpeditionCampActivityRecord[] ExpeditionCampActivities = Array.Empty<ExpeditionCampActivityRecord>();
        public TemporaryCampConstructionAttemptRecord[] TemporaryCampConstructionAttempts = Array.Empty<TemporaryCampConstructionAttemptRecord>();
        public TemporaryCampInstallationRecord[] TemporaryCampInstallations = Array.Empty<TemporaryCampInstallationRecord>();
        public HuntingTrapDeploymentRecord[] HuntingTrapDeployments = Array.Empty<HuntingTrapDeploymentRecord>();
        public HuntingTrapActionRecord[] HuntingTrapActions = Array.Empty<HuntingTrapActionRecord>();
        public HuntingTrapTriggerRecord[] HuntingTrapTriggers = Array.Empty<HuntingTrapTriggerRecord>();
        public HuntingTrapTetherRecord[] HuntingTrapTethers = Array.Empty<HuntingTrapTetherRecord>();
        public Snapshot Copy() => new Snapshot {
            DyingCadences = DyingCadences.ToArray(), Structures = Structures.ToArray(), CraftingIncidents = CraftingIncidents.ToArray(),
            WorldLifeMarkers = WorldLifeMarkers.ToArray(),
            RepairWork = RepairWork.ToArray(), ManufacturingOrders = ManufacturingOrders.ToArray(), Trades = Trades.ToArray(), AlchemyDoses = AlchemyDoses.ToArray(), ManufacturingAdvance = ManufacturingAdvance,
            SupplyCaches = SupplyCaches.ToArray(), SupplyCacheAttempts = SupplyCacheAttempts.ToArray(), SupplyCacheEquipment = SupplyCacheEquipment.ToArray(),
            BuriedCacheSites = BuriedCacheSites.ToArray(), CacheExcavations = CacheExcavations.ToArray(),
            PortableEquipment = PortableEquipment.ToArray(), PortableHandling = PortableHandling.ToArray(),
            PortableStorageProfiles = PortableStorageProfiles.ToArray(),
            CharacterMilestones = CharacterMilestones.ToArray(), CharacterHitDice = CharacterHitDice.ToArray(),
            CharacterFeatureGrants = CharacterFeatureGrants.ToArray(), CharacterAdvancements = CharacterAdvancements.ToArray(),
            CharacterFeatureRuntime = CharacterFeatureRuntime.ToArray(), TacticalCovers = TacticalCovers.ToArray(),
            RepeatingCrossbows = RepeatingCrossbows.ToArray(), AmmunitionLots = AmmunitionLots.ToArray(),
            RangedCombatants = RangedCombatants.ToArray(), RangedAttacks = RangedAttacks.ToArray(),
            PeriodicRiders = PeriodicRiders.ToArray(), PeriodicRiderEvents = PeriodicRiderEvents.ToArray(),
            PeriodicImmunities = PeriodicImmunities.ToArray(), SkillTraining = SkillTraining.ToArray(),
            BonusActions = BonusActions.ToArray(),
            InitialClassSelections = InitialClassSelections.ToArray(),
            InitialCharacterLoadouts = InitialCharacterLoadouts.ToArray(), ShieldStationarity = ShieldStationarity.ToArray(),
            OverwatchIntervals = OverwatchIntervals.ToArray(), OverwatchDesignations = OverwatchDesignations.ToArray(),
            OverwatchOffers = OverwatchOffers.ToArray(), OverwatchRiderChoices = OverwatchRiderChoices.ToArray(),
            ReadyActions = ReadyActions.ToArray(), ReadyOccurrences = ReadyOccurrences.ToArray(),
            TacticalAllies = TacticalAllies.ToArray(), SoldierTacticalEffects = SoldierTacticalEffects.ToArray(), TacticalAttackAudits = TacticalAttackAudits.ToArray(),
            TacticalAssessments = TacticalAssessments.ToArray(),
            CommandStepOffers = CommandStepOffers.ToArray(),
            SuppressionFireVolleys = SuppressionFireVolleys.ToArray(),
            SuppressionSlows = SuppressionSlows.ToArray(),
            DefensiveFormations = DefensiveFormations.ToArray(),
            FishingTrapAttempts = FishingTrapAttempts.ToArray(),
            FishingOpportunities = FishingOpportunities.ToArray(), FishingCreatures = FishingCreatures.ToArray(),
            FishingStockManifests = FishingStockManifests.ToArray(), FishingStockAllocations = FishingStockAllocations.ToArray(),
            FishingTraps = FishingTraps.ToArray(), FishingReceiveLocations = FishingReceiveLocations.ToArray(),
            FishingTrapRetrievals = FishingTrapRetrievals.ToArray(),
            ExpeditionAssignments = ExpeditionAssignments.ToArray(),
            WorldActivityIntervals = WorldActivityIntervals.ToArray(),
            HarvestDonors = HarvestDonors.ToArray(), HarvestManifests = HarvestManifests.ToArray(),
            HarvestCategories = HarvestCategories.ToArray(), HarvestUnits = HarvestUnits.ToArray(), HarvestAttempts = HarvestAttempts.ToArray(),
            HarvestRequirementWorks = HarvestRequirementWorks.ToArray(),
            HarvestPreservationTreatmentAttempts = HarvestPreservationTreatmentAttempts.ToArray(),
            HarvestPreservationEvidence = HarvestPreservationEvidence.ToArray(),
            MiningDeposits = MiningDeposits.ToArray(), MiningCategories = MiningCategories.ToArray(),
            MiningUnits = MiningUnits.ToArray(), MiningAttempts = MiningAttempts.ToArray(),
            ProspectingPatches = ProspectingPatches.ToArray(), ProspectingExposures = ProspectingExposures.ToArray(),
            ProspectingAttempts = ProspectingAttempts.ToArray(),
            MiningAssayProfiles = MiningAssayProfiles.ToArray(), MiningAssayAttempts = MiningAssayAttempts.ToArray(),
            MiningAssaySamples = MiningAssaySamples.ToArray(),
            DestructiveMiningAssayProfiles = DestructiveMiningAssayProfiles.ToArray(),
            DestructiveMiningAssayAttempts = DestructiveMiningAssayAttempts.ToArray(),
            MineralPreparationProfiles = MineralPreparationProfiles.ToArray(),
            MineralPreparationAttempts = MineralPreparationAttempts.ToArray(),
            MiningToolCandidateProfiles = MiningToolCandidateProfiles.ToArray(),
            MiningToolInstanceStates = MiningToolInstanceStates.ToArray(),
            MiningToolUses = MiningToolUses.ToArray(),
            Recipe347FormulaAccess = Recipe347FormulaAccess.ToArray(), Recipe347TradeSpecialties = Recipe347TradeSpecialties.ToArray(),
            Recipe347Workshops = Recipe347Workshops.ToArray(), Recipe347WorkOrders = Recipe347WorkOrders.ToArray(),
            Recipe347Outputs = Recipe347Outputs.ToArray(), Recipe347MiningToolProfiles = Recipe347MiningToolProfiles.ToArray(),
            Recipe347MiningToolUseEvidence = Recipe347MiningToolUseEvidence.ToArray(), Recipe347MiningToolWorkSegments = Recipe347MiningToolWorkSegments.ToArray(),
            OrdinaryReceptacleLocks = OrdinaryReceptacleLocks.ToArray(), OrdinaryReceptacleAttempts = OrdinaryReceptacleAttempts.ToArray(),
            ObservationMapWidth = ObservationMapWidth, ObservationMapHeight = ObservationMapHeight,
            ObservationCells = ObservationCells.ToArray(), ObservationProfiles = ObservationProfiles.ToArray(),
            ObservationActions = ObservationActions.ToArray(), ObservationHideResults = ObservationHideResults.ToArray(),
            ObserverKnowledge = ObserverKnowledge.ToArray(),
            RouteTravels = RouteTravels.ToArray(),
            RouteTravelSpatial = RouteTravelSpatial.ToArray(),
            RouteMappingResults = RouteMappingResults.ToArray(),
            RouteMappingWorkAttempts = RouteMappingWorkAttempts.ToArray(),
            RouteSegments = RouteSegments.ToArray(), RouteReconnaissanceAttempts = RouteReconnaissanceAttempts.ToArray(),
            DailyProvisioningSettlements = DailyProvisioningSettlements.ToArray(),
            DailyProvisioningConsumption = DailyProvisioningConsumption.ToArray(),
            ExpeditionStrainGains = ExpeditionStrainGains.ToArray(), ExpeditionDashLocks = ExpeditionDashLocks.ToArray(),
            RestWatchSchedules = RestWatchSchedules.ToArray(), RestIntervals = RestIntervals.ToArray(),
            RestWatchOutcomes = RestWatchOutcomes.ToArray(), RestDebtEvents = RestDebtEvents.ToArray(),
            ExpeditionStrainRecoveryGateUpdates = ExpeditionStrainRecoveryGateUpdates.ToArray(),
            ExpeditionBeneficialRests = ExpeditionBeneficialRests.ToArray(),
            ExpeditionStrainRecoveryOffers = ExpeditionStrainRecoveryOffers.ToArray(),
            ExpeditionStrainRemovals = ExpeditionStrainRemovals.ToArray(),
            ExpeditionMoraleRestIntervals = ExpeditionMoraleRestIntervals.ToArray(),
            ExpeditionMoraleRestBenefits = ExpeditionMoraleRestBenefits.ToArray(),
            ExpeditionHavenCareIntervals = ExpeditionHavenCareIntervals.ToArray(),
            ExpeditionHavenCareAssessments = ExpeditionHavenCareAssessments.ToArray(),
            ExpeditionPressureCohorts = ExpeditionPressureCohorts.ToArray(),
            ExpeditionPressureExposures = ExpeditionPressureExposures.ToArray(),
            ExpeditionPressureChanges = ExpeditionPressureChanges.ToArray(),
            ExpeditionPressureCheckpoints = ExpeditionPressureCheckpoints.ToArray(),
            ExpeditionCampSites = ExpeditionCampSites.ToArray(),
            ExpeditionCampActivities = ExpeditionCampActivities.ToArray(),
            TemporaryCampConstructionAttempts = TemporaryCampConstructionAttempts.ToArray(),
            TemporaryCampInstallations = TemporaryCampInstallations.ToArray(),
            HuntingTrapDeployments = HuntingTrapDeployments.ToArray(), HuntingTrapActions = HuntingTrapActions.ToArray(),
            HuntingTrapTriggers = HuntingTrapTriggers.ToArray(), HuntingTrapTethers = HuntingTrapTethers.ToArray(),
            FormulaWork = FormulaWork.ToArray(),
            WorldSchedule = WorldSchedule, WorldIntervals = WorldIntervals.ToArray(), WorldTraversals = WorldTraversals.ToArray(),
            Conditions = Conditions.ToArray(), ClosedEncounters = ClosedEncounters.ToArray(),
            TacticalActors = TacticalActors.ToArray(), TacticalMoves = TacticalMoves.ToArray(), PressOffers = PressOffers.ToArray(),
            ActorMovement = ActorMovement.ToArray(), Clubs = Clubs.ToArray(), Stances = Stances.ToArray(), Dodges = Dodges.ToArray(), MeleeAttacks = MeleeAttacks.ToArray(), Presses = Presses.ToArray(),
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

    /// <summary>Selected perceived targets for the bounded Soldier Suppression Fire command.
    /// The host still validates target perception, zone membership, weapon, ammunition and authority.</summary>
    public sealed class SuppressionFireRequest
    {
        private readonly string[] targetIds;
        public string TurnId { get; }
        public string WeaponId { get; }
        public string[] TargetIds => (string[])targetIds.Clone();
        internal string Fingerprint => TurnId + "|" + WeaponId + "|" + string.Join(",",targetIds);
        public SuppressionFireRequest(string turnId,string weaponId,IEnumerable<string> targetIds)
        {
            if(!Validation.ValidId(turnId)||!Validation.ValidId(weaponId)||targetIds==null)throw new ArgumentException("Invalid Suppression Fire request.");
            var ids=targetIds.ToArray();
            if(ids.Length<1||ids.Length>3||ids.Any(x=>!Validation.ValidId(x))
                ||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length)throw new ArgumentException("Suppression Fire requires one to three distinct targets.");
            TurnId=turnId;WeaponId=weaponId;this.targetIds=ids.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
        }
    }

    /// <summary>Ordered, distinct recipient selection for one TEST_ONLY Defensive Formation use.
    /// Order is gameplay state because optional shifts resolve sequentially.</summary>
    public sealed class DefensiveFormationRequest
    {
        private readonly string[] recipientIds;
        internal string Fingerprint=>TurnId+"|"+string.Join(",",recipientIds);
        public string TurnId { get; }
        public string[] RecipientIds=>(string[])recipientIds.Clone();
        public DefensiveFormationRequest(string turnId,IEnumerable<string> recipientIds)
        {
            if(!Validation.ValidId(turnId)||recipientIds==null)throw new ArgumentException("Invalid Defensive Formation request.");
            var ids=recipientIds.ToArray();
            if(ids.Length<1||ids.Length>3||ids.Any(x=>!Validation.ValidId(x))||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length)
                throw new ArgumentException("Defensive Formation requires one to three distinct recipients.");
            TurnId=turnId;this.recipientIds=ids;
        }
    }

    /// <summary>Canonical category selection for one finite harvest manifest. Conditional
    /// outcome preferences are supplied before the extraction roll and are validated against
    /// the exact selected allocation.</summary>
    public sealed class HarvestSelectionRequest
    {
        private readonly string[] categoryIds;
        public string ManifestVersionId { get; }
        public string FailureVictimPreference { get; }
        public string CriticalRecoveryPreference { get; }
        public string[] CategoryIds => (string[])categoryIds.Clone();
        internal string Fingerprint => ManifestVersionId + "|" + string.Join(",", categoryIds) + "|"
            + FailureVictimPreference + "|" + CriticalRecoveryPreference;
        public HarvestSelectionRequest(string manifestVersionId, IEnumerable<string> categoryIds,
            string failureVictimPreference = "", string criticalRecoveryPreference = "")
        {
            if (!Validation.ValidId(manifestVersionId) || categoryIds == null
                || failureVictimPreference == null || criticalRecoveryPreference == null
                || failureVictimPreference != "" && !Validation.ValidId(failureVictimPreference)
                || criticalRecoveryPreference != "" && !Validation.ValidId(criticalRecoveryPreference))
                throw new ArgumentException("Invalid finite harvest selection.");
            var ids = categoryIds.ToArray();
            if (ids.Length < 1 || ids.Length > HarvestValidation.MaxRecords
                || ids.Any(x => !Validation.ValidId(x))
                || ids.Distinct(StringComparer.Ordinal).Count() != ids.Length)
                throw new ArgumentException("Harvest selection requires distinct category identities.");
            ids = ids.OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (manifestVersionId.Length + failureVictimPreference.Length + criticalRecoveryPreference.Length
                + string.Join(",", ids).Length > 440)
                throw new ArgumentException("Harvest selection exceeds the receipt bound.");
            ManifestVersionId = manifestVersionId;
            FailureVictimPreference = failureVictimPreference;
            CriticalRecoveryPreference = criticalRecoveryPreference;
            this.categoryIds = ids;
        }
    }

    /// <summary>Explicit exposed-node choice. Category membership and difficulty are read from the
    /// versioned deposit record; the request only carries player choices made before work.</summary>
    public sealed class MiningSelectionRequest
    {
        private readonly string[] categoryIds;
        public string DepositVersionId { get; }
        public MiningAbilityChoice Ability { get; }
        public bool Hurried { get; }
        public string FailureVictimPreference { get; }
        public string CriticalRecoveryPreference { get; }
        public string AssistantId { get; }
        public string[] CategoryIds=>(string[])categoryIds.Clone();
        internal string FingerprintVersion=>AssistantId==""?"mining-selection-v1":"mining-selection-v2";
        internal string Fingerprint=>DepositVersionId+"|"+((int)Ability).ToString(System.Globalization.CultureInfo.InvariantCulture)
            +"|"+(Hurried?"1":"0")+"|"+string.Join(",",categoryIds)+"|"+FailureVictimPreference
            +"|"+CriticalRecoveryPreference+(AssistantId==""?"":"|"+AssistantId);
        public MiningSelectionRequest(string depositVersionId,IEnumerable<string> categoryIds,
            MiningAbilityChoice ability=MiningAbilityChoice.Wisdom,bool hurried=false,string failureVictimPreference="",
            string criticalRecoveryPreference="",string assistantId="")
        {
            if(!Validation.ValidId(depositVersionId)||categoryIds==null||!Enum.IsDefined(typeof(MiningAbilityChoice),ability)
                ||failureVictimPreference==null||failureVictimPreference!=""&&!Validation.ValidId(failureVictimPreference)
                ||criticalRecoveryPreference==null||criticalRecoveryPreference!=""&&!Validation.ValidId(criticalRecoveryPreference)
                ||assistantId==null||assistantId!=""&&!Validation.ValidId(assistantId))
                throw new ArgumentException("Invalid mining selection.");
            var ids=categoryIds.ToArray();
            if(ids.Length<1||ids.Length>MiningValidation.MaxRecords||ids.Any(x=>!Validation.ValidId(x))
                ||ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length)
                throw new ArgumentException("Mining selection requires distinct category identities.");
            ids=ids.OrderBy(x=>x,StringComparer.Ordinal).ToArray();
            if(depositVersionId.Length+failureVictimPreference.Length+criticalRecoveryPreference.Length+assistantId.Length+string.Join(",",ids).Length>400)
                throw new ArgumentException("Mining selection exceeds the receipt bound.");
            DepositVersionId=depositVersionId;Ability=ability;Hurried=hurried;FailureVictimPreference=failureVictimPreference;
            CriticalRecoveryPreference=criticalRecoveryPreference;AssistantId=assistantId;
            this.categoryIds=ids;
        }
    }

    /// <summary>Trusted world-event reference used to activate a pre-authored new exposure.</summary>
    public sealed class ProspectingExposureRequest
    {
        public string ExposureId { get; }
        public string CauseId { get; }
        internal string Fingerprint => ExposureId + "|" + CauseId;
        public ProspectingExposureRequest(string exposureId, string causeId)
        {
            if (!Validation.ValidId(exposureId) || !Validation.ValidId(causeId))
                throw new ArgumentException("Invalid prospecting exposure change reference.");
            ExposureId = exposureId; CauseId = causeId;
        }
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
        public CharacterAdvancementRequest Advancement { get; }
        public RangedRequest Ranged { get; }
        public OverwatchRider OverwatchRider { get; }
        public SuppressionFireRequest SuppressionFire { get; }
        public DefensiveFormationRequest DefensiveFormation { get; }
        public ExpeditionAssignmentRequest ExpeditionAssignment { get; }
        public HarvestSelectionRequest HarvestSelection { get; }
        public MiningSelectionRequest MiningSelection { get; }
        public ProspectingExposureRequest ProspectingExposure { get; }
        public RouteMappingWorkRequest RouteMappingWork { get; }
        public Command(string id, string actor, long revision, CommandKind kind,
            string target = "", int x = 0, int y = 0, InventoryRequest inventory = null, CombatRequest combat = null,
            CharacterAdvancementRequest advancement = null, RangedRequest ranged = null, OverwatchRider overwatchRider = OverwatchRider.None,
            SuppressionFireRequest suppressionFire = null,DefensiveFormationRequest defensiveFormation = null,
            ExpeditionAssignmentRequest expeditionAssignment = null,HarvestSelectionRequest harvestSelection = null,
            MiningSelectionRequest miningSelection = null, ProspectingExposureRequest prospectingExposure = null,
            RouteMappingWorkRequest routeMappingWork = null)
        { if(!Enum.IsDefined(typeof(OverwatchRider),overwatchRider))throw new ArgumentException("Invalid Overwatch rider selection.");
            Id = id; Actor = actor; ExpectedRevision = revision; Kind = kind; Target = target; X = x; Y = y; Inventory = inventory; Combat = combat; Advancement=advancement; Ranged=ranged; OverwatchRider=overwatchRider; SuppressionFire=suppressionFire;DefensiveFormation=defensiveFormation; ExpeditionAssignment=expeditionAssignment;HarvestSelection=harvestSelection;MiningSelection=miningSelection;ProspectingExposure=prospectingExposure;RouteMappingWork=routeMappingWork; }
        internal string Fingerprint => ((int)Kind).ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + Actor + "|" + Target + "|" + ExpectedRevision.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + X.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + "|" + Y.ToString(System.Globalization.CultureInfo.InvariantCulture)
            + (Inventory == null ? "" : "|inventory-v1|" + Inventory.Fingerprint)
            + (Combat == null ? "" : "|" + Combat.FingerprintVersion + "|" + Combat.Fingerprint)
            + (Advancement == null ? "" : Advancement.UsesLegacyPairReceipt
                ? "|character-level-v1|" + Advancement.FeatureOne + "|" + Advancement.FeatureTwo
                : Advancement.AsiAbilityIncreases.Count != 0 || Advancement.FeatId != ""
                    ? "|character-level-v3|" + string.Join(",",Advancement.FeatureIds) + "|"
                        + string.Join(",",Advancement.AsiAbilityIncreases.Select(x=>((int)x).ToString(System.Globalization.CultureInfo.InvariantCulture)))
                        + "|" + Advancement.FeatId
                    : "|character-level-v2|" + string.Join(",",Advancement.FeatureIds))
            + (Ranged == null ? "" : "|ranged-v1|" + Ranged.Fingerprint)
            + (OverwatchRider == OverwatchRider.None ? "" : "|overwatch-rider-v1|" + ((int)OverwatchRider).ToString(System.Globalization.CultureInfo.InvariantCulture))
            + (SuppressionFire == null ? "" : "|suppression-fire-v1|" + SuppressionFire.Fingerprint)
            + (DefensiveFormation == null ? "" : "|defensive-formation-v1|" + DefensiveFormation.Fingerprint)
            + (ExpeditionAssignment == null ? "" : ExpeditionAssignment.MiningSelection == null
                ? "|expedition-assignment-v1|" + ExpeditionAssignment.Fingerprint
                : "|expedition-mining-assignment-v1|" + ExpeditionAssignment.Fingerprint + "|" + ExpeditionAssignment.MiningSelection.Fingerprint)
            + (HarvestSelection == null ? "" : "|harvest-selection-v1|" + HarvestSelection.Fingerprint)
            + (MiningSelection == null ? "" : "|" + MiningSelection.FingerprintVersion + "|" + MiningSelection.Fingerprint)
            + (ProspectingExposure == null ? "" : "|prospecting-exposure-v1|" + ProspectingExposure.Fingerprint)
            + (RouteMappingWork == null ? "" : "|route-map-team-v1|" + RouteMappingWork.Fingerprint);
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
    public sealed class CommandCost
    {
        public string Kind { get; }
        public string ResourceId { get; }
        public long Amount { get; }
        public CommandCost(string kind, string resourceId, long amount)
        {
            if (!Validation.ValidId(kind) || resourceId == null || resourceId.Length > 96
                || resourceId.Length != 0 && !Validation.ValidId(resourceId) || amount < 1)
                throw new ArgumentException("Invalid command cost.");
            Kind = kind; ResourceId = resourceId; Amount = amount;
        }
    }
    public sealed class CommandQueryResult
    {
        private readonly CommandCost[] costs;
        private readonly string[] requiredChoices;
        public bool Supported { get; }
        public bool Admissible { get; }
        public string Code { get; }
        public long ObservedRevision { get; }
        public IReadOnlyList<CommandCost> Costs { get; }
        public IReadOnlyList<string> RequiredChoices { get; }
        public CommandQueryResult(bool supported, bool admissible, string code, long observedRevision,
            IEnumerable<CommandCost> costs = null, IEnumerable<string> requiredChoices = null)
        {
            if (observedRevision < 0 || string.IsNullOrEmpty(code) || code.Length > 96
                || code.Any(c => c < 32 || c > 126) || !supported && admissible)
                throw new ArgumentException("Invalid command-query result.");
            this.costs = (costs ?? Array.Empty<CommandCost>()).ToArray();
            this.requiredChoices = (requiredChoices ?? Array.Empty<string>()).ToArray();
            if (this.costs.Any(x => x == null) || this.requiredChoices.Any(x => string.IsNullOrEmpty(x)
                || x.Length > 96 || x.Any(c => c < 32 || c > 126))) throw new ArgumentException("Invalid command-query details.");
            Supported = supported; Admissible = admissible; Code = code; ObservedRevision = observedRevision;
            Costs = Array.AsReadOnly(this.costs); RequiredChoices = Array.AsReadOnly(this.requiredChoices);
        }
    }
    public sealed class CommandOption
    {
        public Command Command { get; }
        public CommandQueryResult Query { get; }
        public CommandOption(Command command, CommandQueryResult query)
        { Command = command ?? throw new ArgumentNullException(nameof(command)); Query = query ?? throw new ArgumentNullException(nameof(query)); }
    }
    /// <summary>Optional read-only command discovery. Query implementations inspect detached state only
    /// and must not roll RNG, write receipts, reserve resources, advance time, or resolve choices.</summary>
    public interface ICommandQueryPolicy
    {
        bool SupportsCommand(CommandKind kind);
        IEnumerable<Command> DiscoverCommands(Snapshot snapshot, Authority authority, string actor);
        CommandQueryResult QueryCommand(Snapshot snapshot, Authority authority, Command command);
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
            if (s.SchemaVersion == Foundation.Snapshot.ReadyActionSchema
                || s.SchemaVersion == Foundation.Snapshot.RouteMappingWorkSchema
                || s.SchemaVersion == Foundation.Snapshot.RouteReconnaissanceSchema
                || s.SchemaVersion == Foundation.Snapshot.DailyProvisioningSchema
                || s.SchemaVersion == Foundation.Snapshot.RestDebtSchema
                || s.SchemaVersion == Foundation.Snapshot.ExpeditionStrainRecoverySchema) { }
            else if (s.SchemaVersion == Foundation.Snapshot.MoraleRestSchema
                || s.SchemaVersion == Foundation.Snapshot.HavenCareSchema
                || s.SchemaVersion == Foundation.Snapshot.ExpeditionPressureSchema
                || s.SchemaVersion == Foundation.Snapshot.ExpeditionPressureLifecycleSchema
                || s.SchemaVersion == Foundation.Snapshot.ExpeditionCampUseSchema
                || s.SchemaVersion == Foundation.Snapshot.TemporaryCampConstructionSchema
                || s.SchemaVersion == Foundation.Snapshot.PortableStorageSchema
                || s.SchemaVersion == Foundation.Snapshot.Recipe347Schema
                || s.SchemaVersion == Foundation.Snapshot.PortableCountedLotSchema
                || s.SchemaVersion == Foundation.Snapshot.HarvestPreservationSchema
                || s.SchemaVersion == Foundation.Snapshot.HarvestPreservationTreatmentSchema
                || s.SchemaVersion == Foundation.Snapshot.HarvestPreservationExposureSchema
                || s.SchemaVersion == Foundation.Snapshot.MiningAssistantSchema) { }
            else if (s.SchemaVersion == Foundation.Snapshot.ProspectingSchema || s.SchemaVersion == Foundation.Snapshot.MiningAssaySchema
                || s.SchemaVersion == Foundation.Snapshot.DestructiveMiningAssaySchema
                || s.SchemaVersion == Foundation.Snapshot.MiningExpeditionAssignmentSchema
                || s.SchemaVersion == Foundation.Snapshot.MineralPreparationSchema
                || s.SchemaVersion == Foundation.Snapshot.MiningToolCandidateSchema || s.SchemaVersion == Foundation.Snapshot.OrdinaryReceptacleSchema
                || s.SchemaVersion == Foundation.Snapshot.ObservationSchema
                || s.SchemaVersion == Foundation.Snapshot.ExpeditionRouteSchema
                || s.SchemaVersion == Foundation.Snapshot.RouteObservationSchema
                || s.SchemaVersion == Foundation.Snapshot.RouteMappingSchema
                || s.SchemaVersion == Foundation.Snapshot.HuntingTrapSchema
                || s.SchemaVersion == Foundation.Snapshot.BuriedCacheSchema) { }
            else if (s.SchemaVersion != Foundation.Snapshot.Schema && s.SchemaVersion != Foundation.Snapshot.WorkSchema
                && s.SchemaVersion != Foundation.Snapshot.CropSchema && s.SchemaVersion != Foundation.Snapshot.InventorySchema && s.SchemaVersion != Foundation.Snapshot.VesselSchema && s.SchemaVersion != Foundation.Snapshot.MovableVesselSchema && s.SchemaVersion != Foundation.Snapshot.EncounterSchema && s.SchemaVersion != Foundation.Snapshot.ActorLifeSchema && s.SchemaVersion != Foundation.Snapshot.ClubAttackSchema && s.SchemaVersion != Foundation.Snapshot.PostureSchema && s.SchemaVersion != Foundation.Snapshot.TacticalMovementSchema && s.SchemaVersion != Foundation.Snapshot.ConditionSchema && s.SchemaVersion != Foundation.Snapshot.SharedWorldSchema && s.SchemaVersion != Foundation.Snapshot.CalendarCombatSchema && s.SchemaVersion != Foundation.Snapshot.FormulaWorkSchema && s.SchemaVersion != Foundation.Snapshot.CraftingConsequenceSchema && s.SchemaVersion != Foundation.Snapshot.RepairWorkSchema && s.SchemaVersion != Foundation.Snapshot.ManufacturingSchema && s.SchemaVersion != Foundation.Snapshot.SupplyCacheSchema && s.SchemaVersion != Foundation.Snapshot.PortableEquipmentSchema && s.SchemaVersion != Foundation.Snapshot.CharacterAdvancementSchema && s.SchemaVersion != Foundation.Snapshot.RepeatingCrossbowSchema && s.SchemaVersion != Foundation.Snapshot.PeriodicRiderSchema && s.SchemaVersion != Foundation.Snapshot.SharedBonusActionSchema && s.SchemaVersion != Foundation.Snapshot.OverwatchSchema && s.SchemaVersion != Foundation.Snapshot.OverwatchExecutionSchema && s.SchemaVersion != Foundation.Snapshot.SoldierInitialLoadoutSchema && s.SchemaVersion != Foundation.Snapshot.SoldierInitialBuildSchema && s.SchemaVersion != Foundation.Snapshot.SoldierTacticalTechniquesSchema && s.SchemaVersion != Foundation.Snapshot.CharacterAdvancementHistorySchema && s.SchemaVersion != Foundation.Snapshot.TacticalAssessmentSchema && s.SchemaVersion != Foundation.Snapshot.CommandStepSchema && s.SchemaVersion != Foundation.Snapshot.SuppressionFireSchema && s.SchemaVersion != Foundation.Snapshot.DefensiveFormationSchema && s.SchemaVersion != Foundation.Snapshot.FishingTrapLegacySchema && s.SchemaVersion != Foundation.Snapshot.FishingTrapBaitSchema && s.SchemaVersion != Foundation.Snapshot.FishingTrapSchema && s.SchemaVersion != Foundation.Snapshot.FishingStockSchema && s.SchemaVersion != Foundation.Snapshot.ExpeditionAssignmentSchema && s.SchemaVersion != Foundation.Snapshot.OffCalendarActivitySchema && s.SchemaVersion != Foundation.Snapshot.HarvestSchema && s.SchemaVersion != Foundation.Snapshot.HarvestManifestSchema && s.SchemaVersion != Foundation.Snapshot.MiningSchema && s.SchemaVersion != Foundation.Snapshot.DodgeSchema && s.SchemaVersion != Foundation.Snapshot.BuriedCacheSchema && s.SchemaVersion != Foundation.Snapshot.SharedCharacterAdvancementSchema && s.SchemaVersion != Foundation.Snapshot.MiningAssistantSchema)
                throw new ArgumentException("Unsupported snapshot schema.");
            if (s.SchemaVersion >= Foundation.Snapshot.RouteMappingSchema && !s.TestOnly)
                throw new ArgumentException("TEST_ONLY route-mapping state cannot be loaded as release content.");
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
                || s.Actors.Length > global::Decennium.Foundation.Snapshot.MaxActors || s.Objects.Length > 64 || s.Receipts.Length > MaxReceipts)
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
            ExpeditionAssignmentValidation.Validate(s);
            WorldActivityValidation.Validate(s);
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
            Recipe347Validation.Validate(s);
            SupplyCacheValidation.Validate(s);
            PortableEquipmentValidation.Validate(s);
            CharacterAdvancementValidation.Validate(s);
            RangedCombatValidation.Validate(s);
            PeriodicRiderValidation.Validate(s);
            OverwatchValidation.Validate(s);
            ReadyActionValidation.Validate(s);
            SoldierTacticalFeatureValidation.Validate(s);
            DefensiveFormationValidation.Validate(s);
            FishingTrapValidation.Validate(s);
            HarvestValidation.Validate(s);
            HarvestRequirementWorkValidation.Validate(s);
            HarvestPreservationTreatmentValidation.Validate(s);
            HarvestPreservationEvidenceValidation.Validate(s);
            MiningValidation.Validate(s);
            ProspectingValidation.Validate(s);
            MiningAssayValidation.Validate(s);
            DestructiveMiningAssayValidation.Validate(s);
            MineralPreparationValidation.Validate(s);
            MiningToolValidation.Validate(s);
            OrdinaryReceptacleValidation.Validate(s);
            ObservationValidation.Validate(s);
            ExpeditionRouteTravelValidation.Validate(s);
            ExpeditionRouteSpatialValidation.Validate(s);
            ExpeditionRouteMappingValidation.Validate(s);
            ExpeditionRouteMappingWorkValidation.Validate(s);
            ExpeditionRouteReconnaissanceValidation.Validate(s);
            ExpeditionProvisioningValidation.Validate(s);
            ExpeditionPressureValidation.Validate(s);
            ExpeditionCampValidation.Validate(s);
            TemporaryCampConstructionValidation.Validate(s);
            HuntingTrapValidation.Validate(s);
            CacheExcavationValidation.Validate(s);
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
        private string ValidateCommandAndAuthority(Authority authority, Command command)
        {
            if (authority == null || command == null || !Validation.ValidId(command.Id)
                || !Validation.ValidId(command.Actor) || command.Target == null || command.Target.Length > 96
                || (command.Target.Length != 0 && !Validation.ValidId(command.Target)) || command.ExpectedRevision < 0
                || !Enum.IsDefined(typeof(CommandKind), command.Kind)) return "InvalidCommand";
            bool combatKind=command.Kind==CommandKind.SelectCombatStance||command.Kind==CommandKind.AttackClub||command.Kind==CommandKind.ResolveKnockout||command.Kind==CommandKind.Dodge
                ||command.Kind==CommandKind.AttackUnarmed||command.Kind==CommandKind.RespondOpportunityAttack||command.Kind==CommandKind.RespondPress
                ||command.Kind==CommandKind.RespondOverwatch||command.Kind==CommandKind.Ready||command.Kind==CommandKind.RespondReady
                ||command.Kind==CommandKind.TacticalAssessment
                ||command.Kind==CommandKind.OfferCommandStep||command.Kind==CommandKind.RespondCommandStep||command.Kind==CommandKind.RespondDefensiveFormation;
            if(combatKind!=(command.Combat!=null)||command.Combat!=null&&command.Inventory!=null)return "UnexpectedCombatPayload";
            if((command.Kind==CommandKind.AdvanceCharacterLevel)!=(command.Advancement!=null)
                ||command.Advancement!=null&&(command.Inventory!=null||command.Combat!=null))return "UnexpectedCommandPayload";
            if(command.Fingerprint.Length>512)return "CommandFingerprintTooLong";
            if(command.Kind==CommandKind.ResolveExpeditionStrainRecovery
                &&(command.Target==""||command.X!=0||command.Y!=0||command.Inventory!=null||command.Combat!=null
                    ||command.Advancement!=null||command.Ranged!=null||command.OverwatchRider!=OverwatchRider.None
                    ||command.SuppressionFire!=null||command.DefensiveFormation!=null||command.ExpeditionAssignment!=null
                    ||command.HarvestSelection!=null||command.MiningSelection!=null||command.ProspectingExposure!=null
                    ||command.RouteMappingWork!=null))return "UnexpectedStrainRecoveryPayload";
            if ((command.Kind == CommandKind.RecordProspectingExposure) != (command.ProspectingExposure != null)
                || command.ProspectingExposure != null && (command.Inventory != null || command.Combat != null
                    || command.Advancement != null || command.Ranged != null || command.HarvestSelection != null
                    || command.MiningSelection != null || command.Target == "" || command.X != 0 || command.Y != 0))
                return "UnexpectedProspectingPayload";
            if(command.Kind==CommandKind.RecordHarvestPreservationExposure
                &&(command.Target==""||command.X!=0||command.Y!=0||command.Inventory!=null||command.Combat!=null
                    ||command.Advancement!=null||command.Ranged!=null||command.OverwatchRider!=OverwatchRider.None
                    ||command.SuppressionFire!=null||command.DefensiveFormation!=null||command.ExpeditionAssignment!=null
                    ||command.HarvestSelection!=null||command.MiningSelection!=null||command.ProspectingExposure!=null
                    ||command.RouteMappingWork!=null))return "UnexpectedHarvestExposurePayload";
            if ((command.Kind == CommandKind.StartRouteMappingWork) != (command.RouteMappingWork != null)
                || command.RouteMappingWork != null && (command.Inventory != null || command.Combat != null
                    || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                    || command.SuppressionFire != null || command.DefensiveFormation != null
                    || command.ExpeditionAssignment != null || command.HarvestSelection != null
                    || command.MiningSelection != null || command.ProspectingExposure != null
                    || command.Target == "" || command.X != 0 || command.Y != 0))
                return "UnexpectedRouteMappingWorkPayload";
            bool routeReconnaissanceCommand = command.Kind == CommandKind.StartRouteReconnaissance
                || command.Kind == CommandKind.PauseRouteReconnaissance || command.Kind == CommandKind.ResumeRouteReconnaissance;
            if (routeReconnaissanceCommand && (command.Inventory != null || command.Combat != null
                || command.Advancement != null || command.Ranged != null || command.OverwatchRider != OverwatchRider.None
                || command.SuppressionFire != null || command.DefensiveFormation != null
                || command.ExpeditionAssignment != null || command.HarvestSelection != null
                || command.MiningSelection != null || command.ProspectingExposure != null
                || command.RouteMappingWork != null || command.Target == "" || command.X != 0 || command.Y != 0))
                return "UnexpectedRouteReconnaissancePayload";
            if((command.Kind==CommandKind.ResolveOverwatchRider)!=(command.OverwatchRider!=OverwatchRider.None)
                ||command.OverwatchRider!=OverwatchRider.None&&(command.Inventory!=null||command.Combat!=null||command.Advancement!=null||command.Ranged!=null))
                return "UnexpectedOverwatchPayload";
            if((command.Kind==CommandKind.SuppressionFire)!=(command.SuppressionFire!=null)
                ||command.SuppressionFire!=null&&(command.Inventory!=null||command.Combat!=null||command.Advancement!=null||command.Ranged!=null
                    ||command.OverwatchRider!=OverwatchRider.None||command.DefensiveFormation!=null||command.Target!=""))return "UnexpectedSuppressionFirePayload";
            if((command.Kind==CommandKind.ActivateDefensiveFormation)!=(command.DefensiveFormation!=null)
                ||command.DefensiveFormation!=null&&(command.Inventory!=null||command.Combat!=null||command.Advancement!=null||command.Ranged!=null
                    ||command.OverwatchRider!=OverwatchRider.None||command.SuppressionFire!=null||command.Target!=""||command.X!=0||command.Y!=0))
                return "UnexpectedDefensiveFormationPayload";
            bool assignmentKind=command.Kind==CommandKind.AssignExpeditionWork;
            if(assignmentKind!=(command.ExpeditionAssignment!=null)
                ||command.ExpeditionAssignment!=null&&(command.Inventory!=null||command.Combat!=null||command.Advancement!=null||command.Ranged!=null
                    ||command.OverwatchRider!=OverwatchRider.None||command.SuppressionFire!=null||command.DefensiveFormation!=null
                    ||command.HarvestSelection!=null||command.MiningSelection!=null||command.ProspectingExposure!=null
                    ||command.Target!=""||command.X!=0||command.Y!=0)
                ||(command.Kind==CommandKind.CancelExpeditionWork||command.Kind==CommandKind.StartExpeditionWork)
                    &&(command.ExpeditionAssignment!=null||command.Inventory!=null||command.Combat!=null||command.Advancement!=null
                        ||command.Ranged!=null||command.OverwatchRider!=OverwatchRider.None||command.SuppressionFire!=null
                        ||command.DefensiveFormation!=null||command.Target==""||command.X!=0||command.Y!=0))
                return "UnexpectedExpeditionAssignmentPayload";
            if(!string.IsNullOrEmpty(command.ExpeditionAssignment?.MiningSelection?.AssistantId))
                return "MiningAssistantAssignmentUnsupported";
            if(command.ExpeditionAssignment?.MiningSelection!=null&&state.SchemaVersion<Snapshot.MiningExpeditionAssignmentSchema)
                return "MiningAssignmentRequiresSchema47";
            if(command.Kind==CommandKind.RespondDefensiveFormation&&(command.Inventory!=null||command.Advancement!=null||command.Ranged!=null
                ||command.OverwatchRider!=OverwatchRider.None||command.SuppressionFire!=null||command.DefensiveFormation!=null))
                return "UnexpectedDefensiveFormationResponsePayload";
            bool rangedKind=command.Kind==CommandKind.AttackRepeatingCrossbow||command.Kind==CommandKind.ReloadRepeatingCrossbow
                ||command.Kind==CommandKind.WarningShot||command.Kind==CommandKind.CoveringFire;
            if(rangedKind!=(command.Ranged!=null)||command.Ranged!=null&&(command.Inventory!=null||command.Combat!=null||command.Advancement!=null))return "UnexpectedRangedPayload";
            if ((!authority.Controls(command.Actor) && !(command.Kind==CommandKind.AwardCharacterMilestone&&authority.CanModifyWorld)) || (command.Kind == CommandKind.AdvanceClock && !authority.CanAdvanceClock)
                || ((command.Kind == CommandKind.SetCropConditions || command.Kind == CommandKind.EnterInventoryCombat || command.Kind == CommandKind.BeginFixedEncounter || command.Kind == CommandKind.EndFixedEncounter || command.Kind == CommandKind.DispatchConditionEvent || command.Kind == CommandKind.DispatchCraftingMishap || command.Kind==CommandKind.AwardCharacterMilestone
                    ||command.Kind==CommandKind.DispatchFixturePeriodicRider||command.Kind==CommandKind.SetPeriodicRiderSuppression||command.Kind==CommandKind.SetPeriodicFamilyImmunity||command.Kind==CommandKind.ApplyFixtureMagicalHealing
                    ||command.Kind==CommandKind.RecordProspectingExposure
                    ||command.Kind==CommandKind.RecordHarvestPreservationExposure) && !authority.CanModifyWorld))
                return "NotAuthorized";
            string requestedMiningAssistant=command.MiningSelection?.AssistantId??"";
            if(requestedMiningAssistant!=""&&!authority.Controls(requestedMiningAssistant))return "NotAuthorized";
            if(command.Kind==CommandKind.ResumeMining) {
                var miningAttempt=state.MiningAttempts.FirstOrDefault(x=>x.Id==command.Target&&x.WorkerId==command.Actor);
                if(miningAttempt?.Status==MiningAttemptStatus.Paused&&miningAttempt.AssistantId!=""
                    &&!authority.Controls(miningAttempt.AssistantId))return "NotAuthorized";
            }
            if(command.Kind==CommandKind.HandoverFishingTrapResponsibility&&!authority.ConsentsToHandover(command.Target))
                return "RecipientNotWilling";
            if (policy is ICommandInventoryClaims claims) {
                try {
                    if (claims.RequiredInventoryOwners(state.Copy(), command).Any(owner => !Validation.ValidId(owner) || !authority.MayUseInventory(owner))) return "InventoryNotAuthorized";
                } catch (Exception ex) when (ex is ArgumentException || ex is InvalidOperationException || ex is OverflowException) { return "InvalidInventoryClaims"; }
            }
            if (command.Kind == CommandKind.PortionInventory || command.Kind == CommandKind.HandleInventory || command.Kind == CommandKind.StartIntake) {
                var source = state.InventoryLots.FirstOrDefault(x => x.LotId == command.Target);
                if (source != null && !authority.MayUseInventory(source.OwnerId)) return "InventoryNotAuthorized";
                if (command.Kind == CommandKind.StartIntake && source != null && state.Vessels.Length != 0) {
                    var lot = state.Work.Lots.First(x => x.Id == source.LotId);
                    var vessel = state.Vessels.FirstOrDefault(x => x.Id == lot.LocationId);
                    if (vessel != null && !authority.MayUseInventory(vessel.OwnerId)) return "InventoryNotAuthorized";
                }
                if (command.Kind == CommandKind.HandleInventory && command.Inventory != null
                    && command.Inventory.Handling == HandlingKind.Handover && !authority.ConsentsToHandover(command.Inventory.Destination))
                    return "RecipientNotWilling";
            }
            if(command.Kind==CommandKind.HandlePortableEquipment||command.Kind==CommandKind.EquipPortableItem||command.Kind==CommandKind.RemovePortableItem
                ||command.Kind==CommandKind.DoffPortableShield
                ||command.Kind==CommandKind.OpenPortableContainer||command.Kind==CommandKind.ClosePortableContainer) {
                var item=state.PortableEquipment.FirstOrDefault(x=>x.Id==command.Target);
                if(item!=null&&!authority.MayUseInventory(item.OwnerId))return "InventoryNotAuthorized";
                if(command.Kind==CommandKind.HandlePortableEquipment&&command.Inventory!=null&&command.Inventory.Handling==HandlingKind.Handover
                    &&!authority.ConsentsToHandover(command.Inventory.Destination))return "RecipientNotWilling";
            }
            if (command.Kind == CommandKind.StartWaterFill || command.Kind == CommandKind.ResumeWaterFill) {
                var fill = command.Kind == CommandKind.ResumeWaterFill ? state.WaterFills.FirstOrDefault(x => x.Id == command.Target) : null;
                var source = state.InventoryLots.FirstOrDefault(x => x.LotId == (fill == null ? command.Target : fill.SourceLotId));
                var vessel = state.Vessels.FirstOrDefault(x => x.Id == (fill == null ? command.Inventory?.Destination : fill.DestinationId));
                var sourceLot = source == null ? null : state.Work.Lots.FirstOrDefault(x => x.Id == source.LotId);
                var sourceVessel = sourceLot == null ? null : state.Vessels.FirstOrDefault(x => x.Id == sourceLot.LocationId);
                if ((source != null && !authority.MayUseInventory(source.OwnerId)) || (vessel != null && !authority.MayUseInventory(vessel.OwnerId))
                    || (sourceVessel != null && !authority.MayUseInventory(sourceVessel.OwnerId)))
                    return "InventoryNotAuthorized";
            }
            if (command.Kind == CommandKind.HandleVessel) {
                var vessel = state.Vessels.FirstOrDefault(v => v.Id == command.Target);
                if (vessel != null && (!authority.MayUseInventory(vessel.OwnerId) || state.VesselContents.Where(x => x.VesselId == vessel.Id)
                    .Any(x => state.Work.Lots.First(l => l.Id == x.LotId).Amount != default
                        && !authority.MayUseInventory(state.InventoryLots.First(l => l.LotId == x.LotId).OwnerId)))) return "InventoryNotAuthorized";
                if (command.Inventory != null && command.Inventory.Handling == HandlingKind.Handover
                    && !authority.ConsentsToHandover(command.Inventory.Destination)) return "RecipientNotWilling";
            }
            // The admitted copying command uses its actor-owned writing allotment. Resume also
            // rechecks that owner's current grant before duplicate handling or deferred spending.
            if (command.Kind == CommandKind.StartFormulaCopy && !authority.MayUseInventory(command.Actor)) return "InventoryNotAuthorized";
            if (command.Kind == CommandKind.StartCraftRemedy) {
                var incident = state.CraftingIncidents.FirstOrDefault(x => x.Id == command.Target && x.Result == 2);
                var tool = incident == null ? null : state.Structures.FirstOrDefault(x => x.Id == incident.ToolId);
                if (tool != null && !authority.MayUseInventory(tool.OwnerId)) return "InventoryNotAuthorized";
            }
            if (command.Kind == CommandKind.ResumeFormulaWork) {
                var job = state.FormulaWork.FirstOrDefault(x => x.Id == command.Target && x.Kind == FormulaWorkKind.Copy);
                if (job != null && !authority.MayUseInventory(job.WorkerId)) return "InventoryNotAuthorized";
            }
            if(command.Kind==CommandKind.AttackClub||command.Kind==CommandKind.RespondOpportunityAttack&&command.Combat.Choice) {
                var club=state.Clubs.FirstOrDefault(w=>w.Id==command.Combat.WeaponId);
                if(club!=null&&!authority.MayUseInventory(club.OwnerId))return "InventoryNotAuthorized";
            }
            if(command.Kind==CommandKind.Ready) {
                var club=state.Clubs.FirstOrDefault(w=>w.Id==command.Combat.WeaponId);
                if(club!=null&&!authority.MayUseInventory(club.OwnerId))return "InventoryNotAuthorized";
            }
            if(command.Kind==CommandKind.RespondReady&&command.Combat.Choice) {
                var occurrence=state.ReadyOccurrences.FirstOrDefault(x=>x.Id==command.Target&&x.Pending);
                var ready=occurrence==null?null:state.ReadyActions.FirstOrDefault(x=>x.Id==occurrence.ReadyActionId);
                var club=ready==null?null:state.Clubs.FirstOrDefault(w=>w.Id==ready.WeaponId);
                if(club!=null&&!authority.MayUseInventory(club.OwnerId))return "InventoryNotAuthorized";
            }
            return null;
        }
        private bool AcceptedClockAwaitingChoice(CommandReceipt receipt)
            => receipt != null && (state.ManufacturingAdvance != null
                    && state.ManufacturingAdvance.CommandId == receipt.Id
                    && state.ManufacturingAdvance.CommandRevision == receipt.Revision
                || state.ExpeditionStrainRecoveryOffers.Any(x => x.Pending
                    && x.InitiatingCommandId == receipt.Id && x.Revision == receipt.Revision));
        public CommandResult Execute(Authority authority, Command command)
        {
            string preflightFailure=ValidateCommandAndAuthority(authority,command);
            if(preflightFailure!=null)return Reject(preflightFailure);
            CommandReceipt previous = state.Receipts.FirstOrDefault(r => r.Principal == authority.Principal && r.Id == command.Id);
            if (previous != null)
                return previous.Fingerprint == command.Fingerprint
                    ? new CommandResult(Outcome.Duplicate, AcceptedClockAwaitingChoice(previous)?"AlreadyAcceptedSuspended":"AlreadyCommitted",
                        previous.Revision,AcceptedClockAwaitingChoice(previous)) : Reject("CommandIdConflict");
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
            var acceptedReceipt=state.Receipts.Single(r=>r.Principal==authority.Principal&&r.Id==command.Id);
            bool awaitingChoice=AcceptedClockAwaitingChoice(acceptedReceipt);
            return new CommandResult(Outcome.Committed, awaitingChoice?"AcceptedSuspended":"Committed", state.Revision,awaitingChoice);
        }
        public CommandQueryResult QueryCommand(Authority authority, Command command)
        {
            long observedRevision=state.Revision;
            var queryPolicy=policy as ICommandQueryPolicy;
            if(queryPolicy==null||command==null||!Enum.IsDefined(typeof(CommandKind),command.Kind)||!queryPolicy.SupportsCommand(command.Kind))
                return new CommandQueryResult(false,false,"UnsupportedOperation",observedRevision);
            string failure=ValidateCommandAndAuthority(authority,command);
            if(failure!=null)return new CommandQueryResult(true,false,failure,observedRevision);
            CommandReceipt previous=state.Receipts.FirstOrDefault(r=>r.Principal==authority.Principal&&r.Id==command.Id);
            if(previous!=null)return new CommandQueryResult(true,false,previous.Fingerprint==command.Fingerprint?"AlreadyCommitted":"CommandIdConflict",observedRevision);
            if(command.ExpectedRevision!=state.Revision)return new CommandQueryResult(true,false,"StaleRevision",observedRevision);
            if(!state.Actors.Any(a=>a.Id==command.Actor))return new CommandQueryResult(true,false,"UnknownActor",observedRevision);
            if(state.Revision==long.MaxValue||state.Receipts.Length==(state.SchemaVersion>=Snapshot.InventorySchema?512:Validation.MaxReceipts))
                return new CommandQueryResult(true,false,"SessionCapacityReached",observedRevision);
            CommandQueryResult result;
            try { result=queryPolicy.QueryCommand(state.Copy(),authority,command); }
            catch(Exception ex) when(ex is ArgumentException||ex is OverflowException||ex is InvalidOperationException)
            { return new CommandQueryResult(true,false,"PolicyFailure",observedRevision); }
            if(result==null)return new CommandQueryResult(true,false,"PolicyFailure",observedRevision);
            if(!result.Supported)return new CommandQueryResult(false,false,"UnsupportedOperation",observedRevision);
            return new CommandQueryResult(true,result.Admissible,result.Code,observedRevision,result.Costs,result.RequiredChoices);
        }
        public IReadOnlyList<CommandOption> DiscoverCommands(Authority authority, string actor)
        {
            var queryPolicy=policy as ICommandQueryPolicy;
            if(queryPolicy==null||authority==null||!Validation.ValidId(actor)||!authority.Controls(actor))
                return Array.AsReadOnly(Array.Empty<CommandOption>());
            var candidates=queryPolicy.DiscoverCommands(state.Copy(),authority,actor)?.ToArray()??Array.Empty<Command>();
            var options=new List<CommandOption>();
            var ids=new HashSet<string>(StringComparer.Ordinal);
            foreach(var command in candidates) {
                if(command==null||command.Actor!=actor||!queryPolicy.SupportsCommand(command.Kind))continue;
                if(!ids.Add(command.Id))throw new InvalidOperationException("Command discovery produced duplicate option identities.");
                var result=QueryCommand(authority,command);
                if(result.Supported)options.Add(new CommandOption(command,result));
            }
            return Array.AsReadOnly(options.ToArray());
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
