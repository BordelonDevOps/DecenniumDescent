using System;

namespace Decennium.Foundation
{
    /// <summary>Explicit provisional admission identity. Knowing a source is not executable casting authority.</summary>
    public static partial class SpellCastingProfile
    {
        public const string FingerprintPrefix = "TEST_ONLY.cleric-casting-v2-";
        public const string ClubPickupApproval = "67a07398-59b8-5af5-8410-ee42b2ce2ca2";
        public const string CompanionClubId = "TEST_ONLY.companion-club";
        public const string CompanionClubProfileId = "TEST_ONLY.standard-club";
        public const string ClubSourceId = "simple-melee-weapons.club";
        public const string ClubRulebookSha256 = "a346670f4244efe3641cfb06814819d83ffb8512153858205f0621bd8ab8a04b";
        public static bool AdmitsCompanionClub(Snapshot s,string id) => s.ConnectedClericCasting
            && SelectedFingerprint(s.ContentFingerprint) && id==CompanionClubId;
        public const byte Marker = 14;
        public const int MaxCasts = 512, MaxEffects = 512, MaxActivities = 1024, MaxTurnEnds = 2048,
            MaxSaves = 2048, MaxAdmissions = 512, MaxGuidanceUses = 512, MaxFocuses = 512, MaxContamination = 128;
        public const string ApprovalResponse = "384b9c53-9d93-56f3-901b-cede1f7d3028";
        public const string FocusId = "TEST_ONLY.cleric-casting.holy-symbol";
        public const string FocusProfileId = "holy-symbols.amulet";
        public const string ContaminatedWaterId = "TEST_ONLY.cleric-casting.contaminated-water";
        public const string ContaminationId = "TEST_ONLY.cleric-casting.ordinary-contamination";
        public const string InitialPhysicalOrigin = "TEST_ONLY.cleric-casting.initial-physical.v1";
        public const string FocusEquipmentSourceSha256 = "ff22f5974a1c95b4fb4e2a49b460726b956c093ce7990470c31eaa51238cf5c4";
        public static string LifeEndingCause(long revision,string actor)=>"spell.life."+revision.ToString(System.Globalization.CultureInfo.InvariantCulture)+"."+actor;
        public static bool IsFocus(Snapshot s, PortableEquipmentRecord item) => s.ConnectedClericCasting
            && item != null && item.Id == FocusId && item.ProfileId == FocusProfileId;
        public static bool HasUnsafeContamination(Snapshot s,string lotId) => s.ConnectedClericCasting
            && System.Linq.Enumerable.Any(s.ConsumableContamination,x=>x.LotId==lotId && x.Present);
        public static string PhysicalFailure(Snapshot s,Command c)
        {
            if(!s.ConnectedClericCasting)return null;
            if(HasUnsafeContamination(s,c.Target)) {
                if(c.Kind==CommandKind.StartIntake)return "UnsafeConsumableIntakeUnsupported";
                if(c.Kind==CommandKind.PortionInventory || c.Kind==CommandKind.HandleInventory || c.Kind==CommandKind.StartWaterFill)
                    return "ContaminationPropagationUnsupported";
            }
            if(c.Kind==CommandKind.StartWaterFill && c.Inventory!=null
                && System.Linq.Enumerable.Any(s.VesselContents,x=>x.VesselId==c.Inventory.Destination && HasUnsafeContamination(s,x.LotId)))
                return "ContaminationPropagationUnsupported";
            return null;
        }
        public static bool SelectedFingerprint(string value) => value != null && value.StartsWith(FingerprintPrefix, StringComparison.Ordinal);
        public static bool IsUtilityCommand(CommandKind kind) => kind == CommandKind.GroundCastingStrain
            || kind == CommandKind.EndSpellConcentration || kind == CommandKind.FocusDetectedAura || kind == CommandKind.RespondSanctuary;
        public static bool IsPhysicalCommand(CommandKind kind) => kind==CommandKind.StartIntake || kind==CommandKind.InterruptIntake
            || kind==CommandKind.PortionInventory || kind==CommandKind.HandleInventory || kind==CommandKind.StartWaterFill || kind==CommandKind.HandleVessel;
        public static bool IsAdmittedSpell(string id) => id == "arcane-ward" || id == "guidance" || id == "spare-the-dying"
            || id == "sanctuary" || id == "purify-food-and-drink" || id == "detect-magic";
        // Pure disclosure rules. These facts are supplied by registered source/observation adapters,
        // never by a command. The current cohort owns no blocking or school-protection producer.
        public static bool AuraOutlinePermitted(bool registeredActive,bool perceived,bool inRange,bool clearLineOfEffect,bool detectionBlocked)
            =>registeredActive&&perceived&&inRange&&clearLineOfEffect&&!detectionBlocked;
        public static string FocusedAuraSchool(string broadSchool,bool schoolProtected)
        {
            if(!Validation.ValidId(broadSchool))throw new ArgumentException("A registered broad school is required.");
            return schoolProtected?"":broadSchool;
        }
        // Mechanical composition only; callers must supply actual admitted contributors. Guard's
        // first-attack exception is retained here without inventing a Guard command in this cohort.
        public static int CombineFlatArmorBonuses(int ward,int guarded,int guardFirstAttack,int defensivePositioning)
        {
            if(ward<0||ward>1||guarded<0||guarded>1||guardFirstAttack!=0&&guardFirstAttack!=2
                ||defensivePositioning<0)throw new ArgumentException("Invalid temporary AC contributor.");
            return Math.Max(Math.Max(ward,defensivePositioning),guarded+guardFirstAttack);
        }
        private static bool LegacyPayload(Command c) => c.Inventory != null || c.Combat != null || c.Advancement != null
            || c.Ranged != null || c.OverwatchRider != OverwatchRider.None || c.SuppressionFire != null
            || c.DefensiveFormation != null || c.ExpeditionAssignment != null || c.HarvestSelection != null
            || c.MiningSelection != null || c.ProspectingExposure != null || c.RouteMappingWork != null
            || c.IntimidatingPresence != null || c.HealingRite != null;

        // Runs before query, execution and duplicate handling. Old profiles cannot silently ignore a new choice.
        public static string PayloadFailure(Snapshot s, Command c)
        {
            bool cast = c.SpellCast != null, guidance = c.Guidance != null, response = c.SanctuaryResponse != null;
            if (!cast && !guidance && !response && !IsUtilityCommand(c.Kind)) return null;
            if (!s.TestOnly || !SelectedFingerprint(s.ContentFingerprint)) return "OrdinarySpellcastingUnsupported";
            if ((cast ? 1 : 0) + (guidance ? 1 : 0) + (response ? 1 : 0) > 1 || LegacyPayload(c))
                return "UnexpectedSpellPayload";
            if (cast && (c.Kind != CommandKind.CastKnownSpell || c.Target == "" || c.X != 0 || c.Y != 0))
                return "UnexpectedSpellCastPayload";
            if (guidance && c.Kind != CommandKind.Hide && c.Kind != CommandKind.Search && c.Kind != CommandKind.StabilizeCompanion)
                return "GuidanceConsumerUnsupported";
            if ((c.Kind == CommandKind.RespondSanctuary) != response
                || response && (c.Target == "" || c.X != 0 || c.Y != 0)) return "UnexpectedSanctuaryPayload";
            if (IsUtilityCommand(c.Kind) && (cast || guidance || c.X != 0 || c.Y != 0)) return "UnexpectedSpellUtilityPayload";
            return null;
        }
    }
}
