#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    public enum ContentVisibility { Public, Internal }
    public enum ContentViewerAccess { VisibleWithoutGrant, RequiresExistingKnowledge, InternalOnly }
    public enum ContentAuthorityStatus { CanonicalSource, ReviewedAuthoredPlaytest, PrototypeFixture }
    public enum ContentOperation { PortableInteraction, PortableEquipment, ClubAttack, FormulaResearch, FormulaCopy, Manufacture, UseProducedItem, ToolRepair }
    public enum ContentValueState { Value, Unknown, Null, NotApplicable, Unsupported }

    public sealed class ContentHandlerBinding
    {
        public ContentOperation Operation { get; }
        public string HandlerId { get; }
        public int Version { get; }
        public ContentHandlerBinding(ContentOperation operation,string handlerId,int version)
        {
            if(!Enum.IsDefined(typeof(ContentOperation),operation)||!Validation.ValidId(handlerId)||version<1)throw new ArgumentException("Invalid content handler binding.");
            Operation=operation;HandlerId=handlerId;Version=version;
        }
        internal string Canonical=>((int)Operation).ToString(CultureInfo.InvariantCulture)+"@"+HandlerId+"@"+Version.ToString(CultureInfo.InvariantCulture);
    }

    /// <summary>Preserves distinctions a nullable number cannot represent.</summary>
    public sealed class ContentValue
    {
        public ContentValueState State { get; }
        public string Value { get; }
        public ContentValue(ContentValueState state, string value = "")
        {
            if (!Enum.IsDefined(typeof(ContentValueState), state) || value == null
                || state == ContentValueState.Value && value == "" || state != ContentValueState.Value && value != "")
                throw new ArgumentException("Invalid content fact state.");
            State = state; Value = value;
        }
        public static ContentValue Known(string value) => new ContentValue(ContentValueState.Value, value);
        public static ContentValue Unknown() => new ContentValue(ContentValueState.Unknown);
        public static ContentValue Null() => new ContentValue(ContentValueState.Null);
        public static ContentValue NotApplicable() => new ContentValue(ContentValueState.NotApplicable);
        public static ContentValue Unsupported() => new ContentValue(ContentValueState.Unsupported);
    }

    /// <summary>A source address and executable binding. Source identity, visibility, viewer access,
    /// implementation support, and build status are independent fields; the record owns no rule prose.</summary>
    public sealed class ContentDefinitionBinding
    {
        private readonly ContentOperation[] operations;
        private readonly ContentHandlerBinding[] handlerBindings;
        private readonly string[] runtimeAliases;
        private readonly string[] authorityReferences;
        public string Domain { get; }
        public string SemanticId { get; }
        public string SourceRevision { get; }
        public string SourcePath { get; }
        public string SourceBlobId { get; }
        public string JsonPointer { get; }
        public ContentAuthorityStatus AuthorityStatus { get; }
        public ContentVisibility Visibility { get; }
        public ContentViewerAccess ViewerAccess { get; }
        public ContentValue SourceMass { get; }
        public ContentValue OperationalMass { get; }
        public bool TestOnly { get; }
        public IReadOnlyList<ContentOperation> Operations { get; }
        public IReadOnlyList<ContentHandlerBinding> Handlers { get; }
        public IReadOnlyList<string> RuntimeAliases { get; }
        public IReadOnlyList<string> AuthorityReferences { get; }

        public ContentDefinitionBinding(string domain, string semanticId, string sourceRevision, string sourcePath,
            string sourceBlobId, string jsonPointer, ContentAuthorityStatus authorityStatus, ContentVisibility visibility,
            ContentViewerAccess viewerAccess, ContentValue sourceMass, ContentValue operationalMass, string handlerId,
            int handlerVersion, bool testOnly, IEnumerable<ContentOperation> operations, IEnumerable<string> runtimeAliases = null,
            IEnumerable<string> authorityReferences = null, IEnumerable<ContentHandlerBinding> handlerBindings = null)
        {
            var ops = (operations ?? Array.Empty<ContentOperation>()).ToArray();
            var aliases = (runtimeAliases ?? Array.Empty<string>()).ToArray();
            var authority = (authorityReferences ?? Array.Empty<string>()).ToArray();
            var boundHandlers = handlerBindings == null ? ops.Select(x => new ContentHandlerBinding(x, handlerId, handlerVersion)).ToArray() : handlerBindings.ToArray();
            if (!Validation.ValidId(domain) || semanticId == null || semanticId != "" && !Validation.ValidId(semanticId)
                || !Validation.ValidId(sourceRevision) || string.IsNullOrWhiteSpace(sourcePath) || !IsHex(sourceBlobId, 40)
                || string.IsNullOrWhiteSpace(jsonPointer) || !Enum.IsDefined(typeof(ContentAuthorityStatus), authorityStatus)
                || !Enum.IsDefined(typeof(ContentVisibility), visibility) || !Enum.IsDefined(typeof(ContentViewerAccess), viewerAccess)
                || sourceMass == null || operationalMass == null || handlerId == null || handlerId != "" && !Validation.ValidId(handlerId)
                || handlerVersion < 0 || (handlerId == "") != (handlerVersion == 0)
                || handlerBindings == null && ((ops.Length > 0) != (handlerId != ""))
                || handlerBindings != null && (handlerId != "" || handlerVersion != 0)
                || ops.Any(x => !Enum.IsDefined(typeof(ContentOperation), x)) || ops.Distinct().Count() != ops.Length
                || boundHandlers.Length != ops.Length || boundHandlers.Any(x => x == null)
                || boundHandlers.Select(x => x.Operation).Distinct().Count() != boundHandlers.Length
                || boundHandlers.Any(x => !ops.Contains(x.Operation))
                || aliases.Any(x => !Validation.ValidId(x)) || aliases.Distinct(StringComparer.Ordinal).Count() != aliases.Length
                || authority.Any(string.IsNullOrWhiteSpace) || authority.Distinct(StringComparer.Ordinal).Count() != authority.Length
                || semanticId == "" && aliases.Length != 0
                || viewerAccess == ContentViewerAccess.InternalOnly && visibility != ContentVisibility.Internal)
                throw new ArgumentException("Invalid source content binding.");
            Domain = domain; SemanticId = semanticId; SourceRevision = sourceRevision; SourcePath = sourcePath;
            SourceBlobId = sourceBlobId; JsonPointer = jsonPointer; AuthorityStatus = authorityStatus;
            Visibility = visibility; ViewerAccess = viewerAccess; SourceMass = sourceMass; OperationalMass = operationalMass;
            TestOnly = testOnly;
            this.operations = ops; this.handlerBindings = boundHandlers; this.runtimeAliases = aliases; this.authorityReferences = authority;
            Operations = Array.AsReadOnly(ops); Handlers = Array.AsReadOnly(boundHandlers); RuntimeAliases = Array.AsReadOnly(aliases);
            AuthorityReferences = Array.AsReadOnly(authority);
        }

        internal string Canonical => string.Join("|", new[] { Domain, SemanticId, SourceRevision, SourcePath, SourceBlobId, JsonPointer,
            ((int)AuthorityStatus).ToString(CultureInfo.InvariantCulture), ((int)Visibility).ToString(CultureInfo.InvariantCulture),
            ((int)ViewerAccess).ToString(CultureInfo.InvariantCulture), ValueCanonical(SourceMass), ValueCanonical(OperationalMass),
            string.Join(",", handlerBindings.OrderBy(x => x.Operation).Select(x => x.Canonical)), TestOnly ? "1" : "0",
            string.Join(",", operations.OrderBy(x => x).Select(x => ((int)x).ToString(CultureInfo.InvariantCulture))),
            string.Join(",", runtimeAliases.OrderBy(x => x, StringComparer.Ordinal)),
            string.Join(",", authorityReferences.OrderBy(x => x, StringComparer.Ordinal)) });
        private static string ValueCanonical(ContentValue value) => ((int)value.State).ToString(CultureInfo.InvariantCulture) + ":" + value.Value;
        private static bool IsHex(string s, int length) => s != null && s.Length == length && s.All(c => (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'));
    }

    /// <summary>Finite source-bound support for the schema20 portable kit and already connected
    /// recipe-4/Club handlers. It neither imports a catalog nor grants possession or knowledge.</summary>
    public sealed class TestOnlyContentManifest
    {
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string PrototypeRevision = "f0019fe5b6e1d3a1eb506203dca933a004cf05b2";
        public const string TrustedDigest = "85bbdb47e144f2877334feda0108eb9c485d182db8ea4ff7a18a167c40594dae";
        public const string Recipe14TrustedDigest = "5e1c8f3c1d796f4174d0c6eec334fc310e4473085edd9f288954024f9dcc8e79";
        private readonly ContentDefinitionBinding[] entries;
        public int SchemaVersion { get; }
        public string Digest { get; }
        public IReadOnlyList<ContentDefinitionBinding> Entries { get; }

        public TestOnlyContentManifest(IEnumerable<ContentDefinitionBinding> definitions, int schemaVersion = 1)
        {
            entries = (definitions ?? Array.Empty<ContentDefinitionBinding>()).ToArray();
            if (schemaVersion != 1 || entries.Length == 0 || entries.Length > 64
                || entries.Any(x => x == null) || entries.Select(x => x.Domain + "|" + x.SourcePath + "|" + x.JsonPointer).Distinct(StringComparer.Ordinal).Count() != entries.Length
                || entries.Where(x => x.SemanticId != "").GroupBy(x => x.Domain + "|" + x.SemanticId, StringComparer.Ordinal).Any(g => g.Select(x => x.SourcePath + "|" + x.JsonPointer).Distinct(StringComparer.Ordinal).Count() != g.Count())
                || entries.SelectMany(x => x.RuntimeAliases).Distinct(StringComparer.Ordinal).Count() != entries.Sum(x => x.RuntimeAliases.Count))
                throw new ArgumentException("Invalid finite content manifest.");
            SchemaVersion = schemaVersion; Entries = Array.AsReadOnly(entries);
            Digest = Hash("content-manifest-v1|" + schemaVersion.ToString(CultureInfo.InvariantCulture) + "|" + string.Join("\n", entries.Select(x => x.Canonical).OrderBy(x => x, StringComparer.Ordinal)));
        }

        public static TestOnlyContentManifest CreateSelectedProfile() => new TestOnlyContentManifest(SelectedEntries());
        public static TestOnlyContentManifest CreateManufacturingExpansionProfile()
            =>new TestOnlyContentManifest(SelectedEntries().Concat(Recipe14Entries()));
        public static TestOnlyContentManifest CreateSelectedProfileWithout(string domain, string semanticId)
            => new TestOnlyContentManifest(SelectedEntries().Where(x => !(x.Domain == domain && x.SemanticId == semanticId)));
        public bool IsTrustedBuildMetadata => Digest == TrustedDigest || Digest == Recipe14TrustedDigest;
        public string BindFingerprint(string existingFingerprint)
        {
            if (!Validation.ValidId(existingFingerprint) || !IsTrustedBuildMetadata) throw new InvalidOperationException("ContentManifestBuildMismatch");
            string handlers = string.Join(",", entries.SelectMany(x => x.Handlers).Select(x => x.HandlerId + "@" + x.Version.ToString(CultureInfo.InvariantCulture)).Distinct().OrderBy(x => x, StringComparer.Ordinal));
            return "TEST_ONLY.content-v1-" + Hash(existingFingerprint + "|manifest=" + Digest + "|handlers=" + handlers);
        }

        public ContentDefinitionBinding ResolveSemantic(string domain, string id)
            => entries.SingleOrDefault(x => x.Domain == domain && x.SemanticId == id);
        public ContentDefinitionBinding ResolveRuntime(string alias)
            => entries.SingleOrDefault(x => x.RuntimeAliases.Contains(alias, StringComparer.Ordinal));
        public IReadOnlyList<ContentDefinitionBinding> PlayerProjection()
            => Array.AsReadOnly(entries.Where(x => x.Visibility == ContentVisibility.Public && x.ViewerAccess != ContentViewerAccess.InternalOnly).ToArray());
        public bool Supports(ContentDefinitionBinding binding, ContentOperation operation)
            => binding != null && binding.TestOnly && binding.Handlers.Any(x => x.Operation == operation && HandlerVersionSupported(x.HandlerId, x.Version));

        public string ValidateBindings()
        {
            foreach(var recipe in entries.Where(x=>x.Domain=="crafting"&&x.Operations.Contains(ContentOperation.Manufacture))) {
                string[] components=ComponentsFor(recipe.SemanticId);string result=ResultFor(recipe.SemanticId);
                if(components==null||components.Any(id=>ResolveSemantic("crafting-component",id)==null)
                    ||ResolveSemantic("equipment","alchemical-containers.glass-vial")==null
                    ||ResolveSemantic("recipe-result",result)==null)return "ContentRequiredReferenceUnresolved";
            }
            if (entries.Any(x => x.Operations.Contains(ContentOperation.PortableInteraction))
                && (ResolveSemantic("equipment", "pack.explorer") == null || ResolveSemantic("equipment", "adventuring-gear.backpack") == null)) return "ContentRequiredReferenceUnresolved";
            if (!IsTrustedBuildMetadata) return "ContentManifestBuildMismatch";
            if (entries.Any(x => x.AuthorityStatus == ContentAuthorityStatus.CanonicalSource && x.SourceRevision != SourceRevision
                || x.AuthorityStatus == ContentAuthorityStatus.ReviewedAuthoredPlaytest && x.SourceRevision != SourceRevision
                || x.AuthorityStatus == ContentAuthorityStatus.PrototypeFixture && x.SourceRevision != PrototypeRevision)) return "ContentSourceRevisionMismatch";
            if (entries.Any(x => x.Handlers.Any(h => !HandlerVersionSupported(h.HandlerId, h.Version)))) return "ContentHandlerVersionMismatch";
            return null;
        }

        public string ValidateOperation(string domain, string semanticId, ContentOperation operation)
        {
            var binding = ResolveSemantic(domain, semanticId);
            return binding == null ? "ContentIdentityUnknown" : Supports(binding, operation) ? null : "ContentOperationUnsupported";
        }

        public string ValidateCommand(Snapshot state, Command command)
        {
            if (state == null || command == null) return "ContentResolutionUnavailable";
            ContentOperation operation;
            ContentDefinitionBinding binding = null;
            if (IsPortableCommand(command.Kind)) {
                operation = command.Kind == CommandKind.EquipPortableItem || command.Kind == CommandKind.RemovePortableItem || command.Kind == CommandKind.DoffPortableShield
                    ? ContentOperation.PortableEquipment : ContentOperation.PortableInteraction;
                var item = state.PortableEquipment.FirstOrDefault(x => x.Id == command.Target);
                if (item == null) return null;
                binding = ResolveRuntime(item.ProfileId);
            }
            else if (command.Kind == CommandKind.Interact && command.Target == SupplyCacheFixture.CacheId) {
                operation = ContentOperation.PortableEquipment;
                binding = ResolveRuntime(PortableKitFixture.Tools);
            }
            else if (command.Kind == CommandKind.StartToolRepair && command.Target == PortableKitFixture.Tools) {
                operation = ContentOperation.ToolRepair;
                binding = ResolveRuntime(PortableKitFixture.Tools);
            }
            else if (command.Kind == CommandKind.AttackClub || command.Kind == CommandKind.RespondOpportunityAttack && command.Combat != null && command.Combat.Choice) {
                operation = ContentOperation.ClubAttack;
                string weaponId = command.Combat?.WeaponId ?? "";
                var weapon = state.Clubs.FirstOrDefault(x => x.Id == weaponId);
                binding = weapon == null ? null : ResolveRuntime(weapon.ProfileId);
                if (weapon == null && command.Kind == CommandKind.RespondOpportunityAttack) return null;
            }
            else if (command.Kind == CommandKind.StartFormulaResearch || command.Kind == CommandKind.ResumeFormulaWork
                || command.Kind == CommandKind.PauseFormulaWork || command.Kind == CommandKind.CancelFormulaWork) {
                var job = state.FormulaWork.FirstOrDefault(x => x.Id == command.Target);
                operation = command.Kind == CommandKind.StartFormulaResearch || job == null || job.Kind == FormulaWorkKind.Research
                    ? ContentOperation.FormulaResearch : ContentOperation.FormulaCopy;
                binding = ResolveSemantic("crafting",job?.RecipeId??RecipeForSelector(command.Y));
            }
            else if (command.Kind == CommandKind.StartFormulaCopy) {
                operation = ContentOperation.FormulaCopy; binding = ResolveSemantic("crafting",RecipeForSelector(command.Y));
            }
            else if (IsManufacturingCommand(command.Kind)) {
                var dose = command.Kind == CommandKind.UseAlchemyDose ? state.AlchemyDoses.FirstOrDefault(x => x.Id == command.Target) : null;
                var order=command.Kind==CommandKind.UseAlchemyDose?null:state.ManufacturingOrders.FirstOrDefault(x=>x.Id==command.Target);
                operation = command.Kind == CommandKind.UseAlchemyDose ? ContentOperation.UseProducedItem : ContentOperation.Manufacture;
                string recipeId=dose?.RecipeId??order?.RecipeId??(command.Kind==CommandKind.StartManufacturing?command.Target:"recipe-4");
                binding = ResolveSemantic("crafting",recipeId);
                if (command.Kind == CommandKind.StartManufacturing && state.SchemaVersion >= Snapshot.ManufacturingSchema) {
                    string[] components=ComponentsFor(recipeId);
                    if(components==null)return "ContentRequiredReferenceUnresolved";
                    foreach (string component in components)
                        if (!Supports(ResolveSemantic("crafting-component", component), ContentOperation.Manufacture)) return "ContentRequiredReferenceUnresolved";
                    if (!Supports(ResolveSemantic("equipment", "alchemical-containers.glass-vial"), ContentOperation.Manufacture)) return "ContentRequiredReferenceUnresolved";
                    if (!Supports(ResolveSemantic("recipe-result",ResultFor(recipeId)), ContentOperation.UseProducedItem)) return "ContentRequiredReferenceUnresolved";
                }
            }
            else return null;
            if (binding == null) return "ContentIdentityUnknown";
            if (!Supports(binding, operation)) return "ContentOperationUnsupported";
            return null;
        }

        public string ValidatePortableSnapshot(Snapshot state)
        {
            if (state.SchemaVersion < Snapshot.PortableEquipmentSchema) return null;
            foreach (var item in state.PortableEquipment) if (ResolveRuntime(item.ProfileId) == null) return "ContentRequiredReferenceUnresolved";
            var pack = state.PortableEquipment.SingleOrDefault(x => x.Id == PortableKitFixture.Pack);
            return pack != null && (ResolveRuntime(pack.ProfileId)?.SemanticId != "adventuring-gear.backpack"
                || !ResolveSemantic("equipment", "pack.explorer").TestOnly) ? "ContentPortableIdentityMismatch" : null;
        }

        private static bool IsPortableCommand(CommandKind k) => k == CommandKind.HandlePortableEquipment || k == CommandKind.EquipPortableItem
            || k == CommandKind.RemovePortableItem || k == CommandKind.DoffPortableShield || k == CommandKind.OpenPortableContainer || k == CommandKind.ClosePortableContainer;
        private static bool IsManufacturingCommand(CommandKind k) => k == CommandKind.StartManufacturing || k == CommandKind.PauseManufacturing
            || k == CommandKind.ResumeManufacturing || k == CommandKind.CancelManufacturing || k == CommandKind.ResolveManufacturingQuality || k == CommandKind.UseAlchemyDose;
        private static bool HandlerVersionSupported(string id, int version)
            => id == "portable-equipment" && version == 1 || id == "club-attack" && version == 1
                || id == "formula-research" && (version==1||version==2) || id == "manufacturing" && (version==1||version==2)
                || id == "alchemy-dose" && (version==1||version==2);
        private static string RecipeForSelector(int selector)=>selector==0?"recipe-4":selector==1?"recipe-14":null;
        private static string[] ComponentsFor(string recipeId)=>recipeId=="recipe-4"
            ?new[]{"ing-4-0-alchemical_catalyst","ing-4-1-crystal_vial","ing-4-2-alchemical_base","drop-black_blood_sample"}
            :recipeId=="recipe-14"?new[]{"recipe-14.ing-14-0-stabilizing_salts","recipe-14.ing-14-1-distilled_spirits","recipe-14.drop-black_blood_sample"}:null;
        private static string ResultFor(string recipeId)=>recipeId=="recipe-4"?"":recipeId=="recipe-14"?"recipe-14":null;
        internal static string Hash(string value)
        {
            using (var sha = SHA256.Create()) return string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value)).Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }

        private static IEnumerable<ContentDefinitionBinding> SelectedEntries()
        {
            const string equipment = "DescentReviewChanges/ReviewBible/data/playtest/equipment_acquisition_candidate.json";
            const string recipe = "DescentReviewChanges/ReviewBible/data/crafting/Decennium_Descent_Crafting_Bible_v4.json";
            const string review = "DescentReviewChanges/ReviewBible/data/director/crafting_recipe_review_catalog.json";
            const string equipBlob = "afd06198e19409385408ac258be7dc1d0b2600fb";
            const string recipeBlob = "74b948a92e30e0bacbaafa8529432c265d4bf0af";
            const string reviewBlob = "8d4acc4a13d42ff299b19116f6e70a34e79f2c6d";
            string[] carryingAuthority = {
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:docs/canon/CANON_MANIFEST.json@003b9c45d3b36be43a16c431fe341de725f7f406",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:docs/canon/REPOSITORY_PROMOTION.md@15c9fbc9553ec3f04f6f5ad032bdef96d41b65a3",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_02.json@5f79508c1930976f331441fc4ba9cff6d679c4bc#docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md#carrying-and-load",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md@60f81c5706857c5528d9d19e3da9ac15dcd7fb85",
                "Engine:docs/unity/PORTABLE_EQUIPMENT_RULE_DECISIONS.md@25776c3ef2c6287f9dd373b0136a1ad5ad1d9d69"
            };
            var items = new[] {
                ("pack.explorer", "/packs/4", "portable-equipment", new[]{ContentOperation.PortableInteraction}, new[]{"pack.explorer"}),
                ("adventuring-gear.backpack", "/items/80", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.backpack"}),
                ("adventuring-gear.bedroll", "/items/84", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.bedroll"}),
                ("adventuring-gear.mess-kit", "/items/124", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.mess-kit"}),
                ("adventuring-gear.tinderbox", "/items/154", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.tinderbox"}),
                ("adventuring-gear.torch", "/items/155", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.torch"}),
                ("adventuring-gear.rations-1-day", "/items/139", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.rations-1-day"}),
                ("adventuring-gear.waterskin", "/items/157", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.waterskin"}),
                ("adventuring-gear.rope-hempen-50-feet", "/items/141", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.rope-hempen-50-feet"}),
                ("adventuring-gear.pouch", "/items/136", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"adventuring-gear.pouch"}),
                ("tools.thieves-tools", "/items/194", "portable-equipment", new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{"tools.thieves-tools"}),
                ("simple-melee-weapons.club", "/items/17", "club-attack", new[]{ContentOperation.ClubAttack}, new[]{"TEST_ONLY.standard-club"}),
                ("alchemical-containers.glass-vial", "/items/70", "manufacturing", new[]{ContentOperation.Manufacture}, new[]{"ordinary.glass-vial-1gp"}),
                ("tools.alchemist-s-supplies", "/items/159", "manufacturing", new[]{ContentOperation.Manufacture}, new[]{"tools.alchemist-s-supplies"})
            };
            foreach (var item in items) yield return new ContentDefinitionBinding("equipment", item.Item1, SourceRevision, equipment, equipBlob,
                item.Item2, ContentAuthorityStatus.ReviewedAuthoredPlaytest, ContentVisibility.Public, ContentViewerAccess.VisibleWithoutGrant,
                item.Item1 == "alchemical-containers.glass-vial" ? ContentValue.Null() : ContentValue.Unknown(), ContentValue.NotApplicable(),
                item.Item3, item.Item3 == "" ? 0 : 1, true, item.Item4, item.Item5, carryingAuthority);
            yield return new ContentDefinitionBinding("equipment", "prototype.food-lot", PrototypeRevision,
                "engine/com.decennium.foundation/Laboratory/Model/PortableEquipment.cs", "6cbdc77783c1aa4d332e6c29a2810372deea2c4e", "/prototype.food-lot",
                ContentAuthorityStatus.PrototypeFixture, ContentVisibility.Internal, ContentViewerAccess.InternalOnly, ContentValue.NotApplicable(),
                ContentValue.Unknown(), "portable-equipment", 1, true, new[]{ContentOperation.PortableInteraction}, new[]{"prototype.food-lot"});
            yield return new ContentDefinitionBinding("equipment", "prototype.potable-water.pint", PrototypeRevision,
                "engine/com.decennium.foundation/Laboratory/Model/PortableEquipment.cs", "6cbdc77783c1aa4d332e6c29a2810372deea2c4e", "/prototype.potable-water.pint",
                ContentAuthorityStatus.PrototypeFixture, ContentVisibility.Internal, ContentViewerAccess.InternalOnly, ContentValue.NotApplicable(),
                ContentValue.Unknown(), "portable-equipment", 1, true, new[]{ContentOperation.PortableInteraction}, new[]{"prototype.potable-water.pint"});
            yield return new ContentDefinitionBinding("equipment", "portable.tool-fixture", PrototypeRevision,
                "engine/com.decennium.foundation/Laboratory/Model/PortableEquipment.cs", "6cbdc77783c1aa4d332e6c29a2810372deea2c4e", "/tools.thieves-tools",
                ContentAuthorityStatus.PrototypeFixture, ContentVisibility.Internal, ContentViewerAccess.InternalOnly, ContentValue.NotApplicable(),
                ContentValue.Known("1lb"), "portable-equipment", 1, true, new[]{ContentOperation.PortableEquipment,ContentOperation.PortableInteraction}, new[]{PortableKitFixture.Tools});

            string[] researchAuthority = {
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:docs/canon/CANON_MANIFEST.json@003b9c45d3b36be43a16c431fe341de725f7f406#crafting",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md@a71c2e54ad86a8b35377323f16a9f4ff7df986e0#recipe-4",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md@a253486adc64daaaa9d105f8911dcd267c971e06",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md@b2c15e1bd56bb62e0f1729f4f6d68413e62f9be9",
                "Engine:docs/unity/FORMULA_RESEARCH_RULE_DECISIONS.md@7d13fabbb80ecaa9f9fcd28c68aa05d4c354e522",
                "Engine:docs/unity/evidence/2026-11-03-manufacturing/sources/MANUFACTURING_RULE_SCOPE.md@11a4a0310d44fb337ba92c20187fc69d81095ee3"
            };
            yield return new ContentDefinitionBinding("crafting", "recipe-4", SourceRevision, recipe, recipeBlob, "/recipes/3",
                ContentAuthorityStatus.ReviewedAuthoredPlaytest, ContentVisibility.Public, ContentViewerAccess.RequiresExistingKnowledge,
                ContentValue.NotApplicable(), ContentValue.NotApplicable(), "", 0, true,
                new[]{ContentOperation.FormulaResearch,ContentOperation.FormulaCopy,ContentOperation.Manufacture,ContentOperation.UseProducedItem}, null, researchAuthority,
                new[]{new ContentHandlerBinding(ContentOperation.FormulaResearch,"formula-research",1),new ContentHandlerBinding(ContentOperation.FormulaCopy,"formula-research",1),
                    new ContentHandlerBinding(ContentOperation.Manufacture,"manufacturing",1),new ContentHandlerBinding(ContentOperation.UseProducedItem,"alchemy-dose",1)});
            string[] componentIds = { "ing-4-0-alchemical_catalyst", "ing-4-1-crystal_vial", "ing-4-2-alchemical_base", "drop-black_blood_sample" };
            for (int i = 0; i < componentIds.Length; i++) yield return new ContentDefinitionBinding("crafting-component", componentIds[i], SourceRevision,
                recipe, recipeBlob, "/recipes/3/components/" + i.ToString(CultureInfo.InvariantCulture), ContentAuthorityStatus.ReviewedAuthoredPlaytest,
                ContentVisibility.Public, ContentViewerAccess.RequiresExistingKnowledge, ContentValue.NotApplicable(), ContentValue.NotApplicable(),
                "manufacturing", 1, true, new[]{ContentOperation.Manufacture}, null, researchAuthority);
            yield return new ContentDefinitionBinding("recipe-result", "", SourceRevision, recipe, recipeBlob, "/recipes/3/resultItem",
                ContentAuthorityStatus.ReviewedAuthoredPlaytest, ContentVisibility.Public, ContentViewerAccess.RequiresExistingKnowledge,
                ContentValue.NotApplicable(), ContentValue.NotApplicable(), "alchemy-dose", 1, true,
                new[]{ContentOperation.UseProducedItem}, null, researchAuthority);
            yield return new ContentDefinitionBinding("crafting-review", "recipe-4", SourceRevision, review, reviewBlob, "/recipes/3",
                ContentAuthorityStatus.ReviewedAuthoredPlaytest, ContentVisibility.Internal, ContentViewerAccess.InternalOnly,
                ContentValue.NotApplicable(), ContentValue.NotApplicable(), "", 0, true, Array.Empty<ContentOperation>(), null, researchAuthority);
        }

        private static IEnumerable<ContentDefinitionBinding> Recipe14Entries()
        {
            const string candidate="DescentReviewChanges/ReviewBible/data/playtest/alchemy_recipe_candidate.json";
            const string candidateBlob="67d2bbc5ead75f331a2c99f41a75941f03fe431f";
            const string review="DescentReviewChanges/ReviewBible/data/director/crafting_recipe_review_catalog.json";
            const string reviewBlob="8d4acc4a13d42ff299b19116f6e70a34e79f2c6d";
            string[] authority={
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:docs/canon/CANON_MANIFEST.json@003b9c45d3b36be43a16c431fe341de725f7f406#crafting",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_PUBLIC_RECIPE_CARDS.md@a71c2e54ad86a8b35377323f16a9f4ff7df986e0#recipe-14",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/ALCHEMY_RECIPE_PLAYTEST.md@a253486adc64daaaa9d105f8911dcd267c971e06",
                "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4:DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md@b2c15e1bd56bb62e0f1729f4f6d68413e62f9be9#material-identity-consumption-and-substitution",
                "Engine:docs/unity/FORMULA_RESEARCH_RULE_DECISIONS.md@7d13fabbb80ecaa9f9fcd28c68aa05d4c354e522"
            };
            yield return new ContentDefinitionBinding("crafting","recipe-14",SourceRevision,candidate,candidateBlob,"/cards/13",
                ContentAuthorityStatus.ReviewedAuthoredPlaytest,ContentVisibility.Public,ContentViewerAccess.RequiresExistingKnowledge,
                ContentValue.NotApplicable(),ContentValue.NotApplicable(),"",0,true,
                new[]{ContentOperation.FormulaResearch,ContentOperation.FormulaCopy,ContentOperation.Manufacture,ContentOperation.UseProducedItem},null,authority,
                new[]{new ContentHandlerBinding(ContentOperation.FormulaResearch,"formula-research",2),new ContentHandlerBinding(ContentOperation.FormulaCopy,"formula-research",2),
                    new ContentHandlerBinding(ContentOperation.Manufacture,"manufacturing",2),new ContentHandlerBinding(ContentOperation.UseProducedItem,"alchemy-dose",2)});
            string[] components={"ing-14-0-stabilizing_salts","ing-14-1-distilled_spirits","drop-black_blood_sample"};
            for(int i=0;i<components.Length;i++)yield return new ContentDefinitionBinding("crafting-component","recipe-14."+components[i],SourceRevision,candidate,candidateBlob,
                "/cards/13/sourceRequirements/components/"+i.ToString(CultureInfo.InvariantCulture),ContentAuthorityStatus.ReviewedAuthoredPlaytest,
                ContentVisibility.Public,ContentViewerAccess.RequiresExistingKnowledge,ContentValue.NotApplicable(),ContentValue.NotApplicable(),
                "",0,true,new[]{ContentOperation.Manufacture},null,authority,
                new[]{new ContentHandlerBinding(ContentOperation.Manufacture,"manufacturing",2)});
            yield return new ContentDefinitionBinding("recipe-result","recipe-14",SourceRevision,candidate,candidateBlob,"/cards/13/operational",
                ContentAuthorityStatus.ReviewedAuthoredPlaytest,ContentVisibility.Public,ContentViewerAccess.RequiresExistingKnowledge,
                ContentValue.NotApplicable(),ContentValue.NotApplicable(),"",0,true,new[]{ContentOperation.UseProducedItem},null,authority,
                new[]{new ContentHandlerBinding(ContentOperation.UseProducedItem,"alchemy-dose",2)});
            yield return new ContentDefinitionBinding("crafting-review","recipe-14",SourceRevision,review,reviewBlob,"/recipes/13",
                ContentAuthorityStatus.ReviewedAuthoredPlaytest,ContentVisibility.Internal,ContentViewerAccess.InternalOnly,
                ContentValue.NotApplicable(),ContentValue.NotApplicable(),"",0,true,Array.Empty<ContentOperation>(),null,authority);
        }
    }
}
#endif
