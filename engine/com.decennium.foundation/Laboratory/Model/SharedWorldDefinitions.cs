#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Immutable fixture content definition. It describes a supported numerical character
    /// profile and movement fact; it grants no class feature, training, equipment, or permission.</summary>
    public sealed class SharedActorDefinition
    {
        public string Id { get; }
        public string CharacterProfileId { get; }
        public int WalkingSpeed { get; }
        public SharedActorDefinition(string id, string characterProfileId, int walkingSpeed)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(characterProfileId) || walkingSpeed < 0)
                throw new ArgumentException("Invalid shared actor definition.");
            Id = id; CharacterProfileId = characterProfileId; WalkingSpeed = walkingSpeed;
        }
        internal string Canonical => Id + "|" + CharacterProfileId + "|" + WalkingSpeed.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Stable world-instance identity and authored starting placement, separate from its definition.</summary>
    public sealed class SharedActorInstanceDefinition
    {
        public string Id { get; }
        public string DefinitionId { get; }
        public int X { get; }
        public int Y { get; }
        public SharedActorInstanceDefinition(string id, string definitionId, int x, int y)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(definitionId)) throw new ArgumentException("Invalid shared actor instance.");
            Id = id; DefinitionId = definitionId; X = x; Y = y;
        }
        internal string Canonical => Id + "|" + DefinitionId + "|" + X.ToString(CultureInfo.InvariantCulture) + "|" + Y.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Authored work-site identity. This defines no access radius, work duration, or procedure rule.</summary>
    public sealed class SharedSiteDefinition
    {
        public const string ToolRepairProfile = "tool-repair";
        public const string FishHarvestProfile = "fish-harvest";
        public string Id { get; }
        public string ProcedureProfileId { get; }
        public SharedSiteDefinition(string id, string procedureProfileId)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(procedureProfileId)) throw new ArgumentException("Invalid shared site definition.");
            Id = id; ProcedureProfileId = procedureProfileId;
        }
        internal string Canonical => Id + "|" + ProcedureProfileId;
    }

    /// <summary>Stable physical site identity and placement; the location ID is reused by existing physical records.</summary>
    public sealed class SharedSiteInstanceDefinition
    {
        public string Id { get; }
        public string DefinitionId { get; }
        public int X { get; }
        public int Y { get; }
        public SharedSiteInstanceDefinition(string id, string definitionId, int x, int y)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(definitionId)) throw new ArgumentException("Invalid shared site instance.");
            Id = id; DefinitionId = definitionId; X = x; Y = y;
        }
        internal string Canonical => Id + "|" + DefinitionId + "|" + X.ToString(CultureInfo.InvariantCulture) + "|" + Y.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Data-only TEST_ONLY world configuration. Actor/site definitions and runtime instances
    /// are validated before world creation and included in the selected content fingerprint.</summary>
    public sealed class SharedWorldConfiguration
    {
        private readonly SharedActorDefinition[] actorDefinitions;
        private readonly SharedActorInstanceDefinition[] actors;
        private readonly SharedSiteDefinition[] siteDefinitions;
        public string Id { get; }
        public IReadOnlyList<SharedActorDefinition> ActorDefinitions { get; }
        public IReadOnlyList<SharedActorInstanceDefinition> Actors { get; }
        public IReadOnlyList<SharedSiteDefinition> SiteDefinitions { get; }
        public SharedSiteInstanceDefinition WorkSite { get; }
        /// <summary>The stable finite lot identity used by the selected existing procedure.</summary>
        public string FiniteLotId { get; }

        public SharedWorldConfiguration(string id, IEnumerable<SharedActorDefinition> actorDefinitions,
            IEnumerable<SharedActorInstanceDefinition> actors, IEnumerable<SharedSiteDefinition> siteDefinitions,
            SharedSiteInstanceDefinition workSite, string finiteLotId)
        {
            this.actorDefinitions = (actorDefinitions ?? Array.Empty<SharedActorDefinition>()).OrderBy(x => x?.Id, StringComparer.Ordinal).ToArray();
            this.actors = (actors ?? Array.Empty<SharedActorInstanceDefinition>()).OrderBy(x => x?.Id, StringComparer.Ordinal).ToArray();
            this.siteDefinitions = (siteDefinitions ?? Array.Empty<SharedSiteDefinition>()).OrderBy(x => x?.Id, StringComparer.Ordinal).ToArray();
            if (!Validation.ValidId(id) || this.actorDefinitions.Length < 1 || this.actorDefinitions.Length > 8
                || this.actors.Length < 1 || this.actors.Length > 8 || this.siteDefinitions.Length < 1
                || this.actorDefinitions.Any(x => x == null) || this.actors.Any(x => x == null)
                || this.siteDefinitions.Any(x => x == null) || workSite == null || !Validation.ValidId(finiteLotId)
                || this.actorDefinitions.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != this.actorDefinitions.Length
                || this.actors.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != this.actors.Length
                || this.siteDefinitions.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != this.siteDefinitions.Length
                || this.actors.Any(x => !this.actorDefinitions.Any(d => d.Id == x.DefinitionId))
                || !this.siteDefinitions.Any(x => x.Id == workSite.DefinitionId)
                || this.actorDefinitions.Any(d => !this.actors.Any(x => x.DefinitionId == d.Id))
                || this.siteDefinitions.Length != 1 || this.siteDefinitions.Any(d => d.Id != workSite.DefinitionId)
                || this.actors.Any(x => !TestOnlyPolicy.Walkable(x.X, x.Y))
                || !TestOnlyPolicy.Walkable(workSite.X, workSite.Y)
                || this.actors.Select(x => x.X + "," + x.Y).Distinct(StringComparer.Ordinal).Count() != this.actors.Length
                || this.actors.Any(x => x.Id == workSite.Id))
                throw new ArgumentException("Invalid or unresolved shared-world configuration.");
            Id = id; WorkSite = workSite; FiniteLotId = finiteLotId;
            ActorDefinitions = Array.AsReadOnly(this.actorDefinitions);
            Actors = Array.AsReadOnly(this.actors);
            SiteDefinitions = Array.AsReadOnly(this.siteDefinitions);
        }

        public string ValidateAgainst(Snapshot template)
        {
            if (template == null) return "SharedWorldTemplateUnavailable";
            if (actors.Any(instance => template.Actors.Any(a => a.Id == instance.Id))
                || actors.Any(instance => template.Objects.Any(o => o.Id == instance.Id))
                || actors.Any(instance => template.Structures.Any(o => o.Id == instance.Id))
                || actors.Any(instance => template.PortableEquipment.Any(o => o.Id == instance.Id))) return "SharedWorldActorIdentityCollision";
            if (template.Objects.Any(o => o.Id == WorkSite.Id) || template.Actors.Any(a => a.Id == WorkSite.Id)
                || template.Structures.Any(o => o.Id == WorkSite.Id) || template.PortableEquipment.Any(o => o.Id == WorkSite.Id))
                return "SharedWorldSiteIdentityCollision";
            if (template.Work != null && template.Work.Lots.Any(x => x.Id == FiniteLotId)) return "SharedWorldLotIdentityCollision";
            if (template.InventoryLots.Any(x => x.LotId == FiniteLotId)) return "SharedWorldLotIdentityCollision";
            if (template.HarvestUnits.Any(x => x.Id == FiniteLotId)) return "SharedWorldLotIdentityCollision";
            if (actors.Any(instance => template.Actors.Any(a => a.X == instance.X && a.Y == instance.Y))) return "SharedWorldActorPlacementCollision";
            var templateCharacter = template.Characters.SingleOrDefault(x => x.ActorId == TestOnlyPolicy.CompanionId);
            var templateMovement = template.ActorMovement.SingleOrDefault(x => x.ActorId == TestOnlyPolicy.CompanionId);
            foreach (var actor in actors)
            {
                var definition = actorDefinitions.Single(x => x.Id == actor.DefinitionId);
                if (templateCharacter == null || templateMovement == null
                    || definition.CharacterProfileId != templateCharacter.ProfileId
                    || definition.WalkingSpeed != templateMovement.BaseWalkingSpeed
                    || !template.Lives.Any(x => x.ActorId == TestOnlyPolicy.CompanionId)
                    || !template.TacticalActors.Any(x => x.ActorId == TestOnlyPolicy.CompanionId))
                    return "SharedWorldActorDefinitionUnresolved";
            }
            return null;
        }

        internal string Fingerprint(string prior)
        {
            if (string.IsNullOrEmpty(prior)) throw new ArgumentException("Missing prior content fingerprint.");
            string value = "shared-world-configuration-v1|" + Id + "|"
                + string.Join(";", actorDefinitions.Select(x => x.Canonical).OrderBy(x => x, StringComparer.Ordinal)) + "|"
                + string.Join(";", actors.Select(x => x.Canonical).OrderBy(x => x, StringComparer.Ordinal)) + "|"
                + string.Join(";", siteDefinitions.Select(x => x.Canonical).OrderBy(x => x, StringComparer.Ordinal)) + "|"
                + WorkSite.Canonical + "|" + FiniteLotId;
            return "TEST_ONLY.shared-config-v1-" + TestOnlyContentManifest.Hash(prior + "|" + value);
        }
    }

    /// <summary>Shared grid facts used by exploration, tactical movement and physical job access.
    /// Callers still apply their own sourced movement budgets, terrain costs and reaction rules.</summary>
    public enum SpatialStepFailure { None, NotNeighbor, Blocked, Occupied }

    public static class WorldSpatialQueries
    {
        public static long DistanceInCells(int fromX, int fromY, int toX, int toY)
            => Math.Max(Math.Abs((long)toX - fromX), Math.Abs((long)toY - fromY));

        public static bool WithinRange(int fromX, int fromY, int toX, int toY, long rangeInCells)
        {
            if (rangeInCells < 0) throw new ArgumentOutOfRangeException(nameof(rangeInCells));
            return DistanceInCells(fromX, fromY, toX, toY) <= rangeInCells;
        }

        public static long CardinalDistance(int fromX, int fromY, int toX, int toY)
            => checked(Math.Abs((long)toX - fromX) + Math.Abs((long)toY - fromY));

        public static bool WithinCardinalRange(int fromX, int fromY, int toX, int toY, long rangeInCells)
        {
            if (rangeInCells < 0) throw new ArgumentOutOfRangeException(nameof(rangeInCells));
            return CardinalDistance(fromX, fromY, toX, toY) <= rangeInCells;
        }

        public static bool Neighbor(int fromX, int fromY, int toX, int toY, bool diagonals)
        {
            long dx = Math.Abs((long)toX - fromX), dy = Math.Abs((long)toY - fromY);
            return diagonals ? dx <= 1 && dy <= 1 && dx + dy != 0 : dx + dy == 1;
        }

        public static bool Occupied(Snapshot state, string actorId, int x, int y)
        {
            if (state == null || !Validation.ValidId(actorId)) throw new ArgumentException("Invalid spatial query.");
            return state.Actors.Any(a => a.Id != actorId && a.X == x && a.Y == y)
                || state.WorldTraversals.Any(edge => edge.ActorId != actorId && edge.ToX == x && edge.ToY == y);
        }

        public static SpatialStepFailure Step(Snapshot state, string actorId, int fromX, int fromY, int toX, int toY,
            bool diagonals, bool cornerRule, Func<int, int, bool> walkable)
        {
            if (state == null || !Validation.ValidId(actorId) || walkable == null) throw new ArgumentException("Invalid spatial step query.");
            if (!Neighbor(fromX, fromY, toX, toY, diagonals)) return SpatialStepFailure.NotNeighbor;
            if (!walkable(toX, toY)) return SpatialStepFailure.Blocked;
            if (cornerRule && !PlanarCombatGeometry.NeighborPassesCornerRule(new CombatCell(fromX, fromY), new CombatCell(toX, toY),
                !walkable(toX, fromY), !walkable(fromX, toY))) return SpatialStepFailure.Blocked;
            return Occupied(state, actorId, toX, toY) ? SpatialStepFailure.Occupied : SpatialStepFailure.None;
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private SharedWorldConfiguration worldConfiguration;
        private string OffCalendarWorkerId => worldConfiguration?.Actors.FirstOrDefault()?.Id ?? TestOnlyPolicy.CompanionId;
        private string RepairSiteLocationId => worldConfiguration?.WorkSite.Id ?? TestOnlyCropPolicy.PlotId;
        private int RepairSiteX => worldConfiguration?.WorkSite.X ?? repair?.SiteX ?? 3;
        private int RepairSiteY => worldConfiguration?.WorkSite.Y ?? repair?.SiteY ?? 3;
        private string RepairMaterialsLotId => worldConfiguration?.FiniteLotId ?? SharedRepairFixture.Materials;
        private string HarvestSiteId => worldConfiguration?.WorkSite.Id ?? SharedHarvestFixture.SiteId;
        private int HarvestSiteX => worldConfiguration?.WorkSite.X ?? harvestFixture?.SiteX ?? 3;
        private int HarvestSiteY => worldConfiguration?.WorkSite.Y ?? harvestFixture?.SiteY ?? 3;
        private string HarvestFiniteLotId => worldConfiguration?.FiniteLotId ?? SharedHarvestFixture.UnitId;
        private string[] HarvestWorkerIds => worldConfiguration?.Actors.Select(x => x.Id).ToArray() ?? new[] { TestOnlyPolicy.CompanionId };
        private bool IsRepairWorker(string actorId) => actorId == TestOnlyPolicy.ActorId
            || (worldConfiguration == null ? actorId == TestOnlyPolicy.CompanionId : worldConfiguration.Actors.Any(x => x.Id == actorId));

        public TestOnlySharedWorldPolicy(SharedWorldConfiguration configuration, SharedCombatFixture combat,
            SharedResearchFixture research, SharedCraftingFixture crafting, SharedRepairFixture repair,
            SharedManufacturingFixture manufacturing = null, SupplyCacheFixture supplyCache = null,
            int walkingSpeed = 30, ConditionCombatFixture conditions = null, params TacticalTerrainCell[] terrain)
            : this(combat, research, crafting, repair, manufacturing, supplyCache, walkingSpeed, conditions, terrain, configuration)
        {
            BindWorldConfiguration(configuration, null, repair);
        }

        public TestOnlySharedWorldPolicy(SharedWorldConfiguration configuration, SharedCombatFixture combat,
            SharedHarvestFixture harvest, int walkingSpeed = 30, ConditionCombatFixture conditions = null,
            params TacticalTerrainCell[] terrain)
            : this(combat, null, null, null, null, null, walkingSpeed, conditions, terrain, configuration)
        {
            if (harvest == null) throw new ArgumentNullException(nameof(harvest));
            harvestFixture = harvest;
            BindWorldConfiguration(configuration, harvest, null);
        }

        private void BindWorldConfiguration(SharedWorldConfiguration configuration, SharedHarvestFixture harvest, SharedRepairFixture repairFacts)
        {
            if (configuration == null) throw new ArgumentNullException(nameof(configuration));
            string procedure = configuration.SiteDefinitions.Single(x => x.Id == configuration.WorkSite.DefinitionId).ProcedureProfileId;
            bool profileResolved = procedure == SharedSiteDefinition.ToolRepairProfile && repairFacts != null
                || procedure == SharedSiteDefinition.FishHarvestProfile && harvest != null;
            if (!profileResolved)
                throw new ArgumentException("Shared-world site profile does not resolve to its existing procedure handler.", nameof(configuration));
            var template = bodies.Initial();
            var allowedConditionTargets = template.Actors.Select(x => x.Id)
                .Concat(configuration.Actors.Select(x => x.Id)).ToArray();
            if (conditions.Events.Any(x => !allowedConditionTargets.Contains(x.Target, StringComparer.Ordinal)))
                throw new ArgumentException("Shared-world condition event targets an actor outside the configured world.", nameof(configuration));
            string error = configuration.ValidateAgainst(template);
            if (error != null) throw new ArgumentException(error, nameof(configuration));
            if (configuration.Actors.Any(x => x.X == configuration.WorkSite.X && x.Y == configuration.WorkSite.Y))
                throw new ArgumentException("Shared-world actor placement overlaps the configured work site.", nameof(configuration));
            worldConfiguration = configuration;
            offCalendarActivityEnabled = true;
            string fingerprintInput = harvest == null ? ContentFingerprint : ContentFingerprint + "|" + harvest.Key;
            ContentFingerprint = configuration.Fingerprint(fingerprintInput);
        }

        public Authority HostAuthority()
        {
            var initial = Initial();
            var actors = initial.Actors.Select(x => x.Id).ToArray();
            var owners = initial.InventoryLots.Select(x => x.OwnerId).Concat(initial.Structures.Select(x => x.OwnerId))
                .Concat(initial.PortableEquipment.Select(x => x.OwnerId)).Distinct(StringComparer.Ordinal).ToArray();
            return new Authority("TEST_ONLY.host", actors, true, true, owners, actors);
        }

        private void AddConfiguredActors(Snapshot s)
        {
            if (worldConfiguration == null) return;
            var templateCharacter = s.Characters.Single(x => x.ActorId == TestOnlyPolicy.CompanionId);
            var templateLife = s.Lives.Single(x => x.ActorId == TestOnlyPolicy.CompanionId);
            var templateMovement = s.ActorMovement.Single(x => x.ActorId == TestOnlyPolicy.CompanionId);
            var templateTactical = s.TacticalActors.Single(x => x.ActorId == TestOnlyPolicy.CompanionId);
            string clubProfile = s.Clubs.Single(x => x.HeldBy == "").ProfileId;
            foreach (var instance in worldConfiguration.Actors.OrderBy(x => x.Id, StringComparer.Ordinal))
            {
                var definition = worldConfiguration.ActorDefinitions.Single(x => x.Id == instance.DefinitionId);
                if (definition.CharacterProfileId != templateCharacter.ProfileId)
                    throw new InvalidOperationException("SharedWorldActorDefinitionUnresolved");
                s.Actors = s.Actors.Concat(new[] { new ActorState { Id = instance.Id, X = instance.X, Y = instance.Y } }).ToArray();
                s.Characters = s.Characters.Concat(new[] { new ActorCharacterRecord(instance.Id, templateCharacter.ProfileId,
                    templateCharacter.Abilities, templateCharacter.Levels) }).ToArray();
                s.Lives = s.Lives.Concat(new[] { ActorLifeRules.Record(instance.Id, ActorLifeRules.Read(templateLife), templateLife.Prone) }).ToArray();
                s.ActorMovement = s.ActorMovement.Concat(new[] { new ActorMovementRecord(instance.Id, definition.WalkingSpeed,
                    templateMovement.TurnOrdinal, templateMovement.Spent) }).ToArray();
                s.TacticalActors = s.TacticalActors.Concat(new[] { new ActorTacticalRecord(instance.Id, templateTactical.LastRegularStart,
                    templateTactical.ReactionAvailable, templateTactical.MobileFeet, templateTactical.PressConsumed, templateTactical.DisengageTurn) }).ToArray();
                s.Clubs = s.Clubs.Concat(new[] { new ClubInstance("scenario.club." + instance.Id,
                    clubProfile, instance.Id, instance.Id, "", instance.X, instance.Y) }).ToArray();
                s.Conditions = s.Conditions.Concat(new[] { new ConditionJournal(ConditionHistory.PolicyId, instance.Id,
                    new ConditionStamp(s.RuleClock)) }).ToArray();
            }
        }
    }
}
#endif
