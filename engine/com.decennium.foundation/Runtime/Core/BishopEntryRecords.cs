using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    /// <summary>Genesis declaration and actual recovery/care/departure evidence; neither is an XP award.</summary>
    public sealed class BishopEntryRecord
    {
        public string DeclarationDigest { get; }
        public BishopDepartureProof Departure { get; }
        public ReadOnlyCollection<DivineInvocationRecord> Invocations { get; }
        public ReadOnlyCollection<AuraOfFaithSaveRecord> AuraSaves { get; }
        public ReadOnlyCollection<AuraOfFaithHealingRecord> AuraHealing { get; }
        public ReadOnlyCollection<BishopDispelRecord> Dispels { get; }
        public BishopEntryRecord(string declarationDigest, BishopDepartureProof departure = null, IEnumerable<DivineInvocationRecord> invocations = null,
            IEnumerable<AuraOfFaithSaveRecord> auraSaves = null,IEnumerable<AuraOfFaithHealingRecord> auraHealing = null,IEnumerable<BishopDispelRecord> dispels = null)
        {
            if (declarationDigest != BishopProfile.DeclarationDigest) throw new ArgumentException("Unsupported Bishop objective declaration.");
            DeclarationDigest = declarationDigest; Departure = departure;
            var rows=(invocations??Array.Empty<DivineInvocationRecord>()).ToArray();
            if(rows.Length>128||rows.Any(x=>x==null))throw new ArgumentException("Invalid Invocation history.");
            Invocations=Array.AsReadOnly(rows);
            var saves=(auraSaves??Array.Empty<AuraOfFaithSaveRecord>()).ToArray();var healing=(auraHealing??Array.Empty<AuraOfFaithHealingRecord>()).ToArray();
            if(saves.Length>2048||healing.Length>128||saves.Any(x=>x==null)||healing.Any(x=>x==null))throw new ArgumentException("Invalid Aura history.");
            AuraSaves=Array.AsReadOnly(saves);AuraHealing=Array.AsReadOnly(healing);
            var endings=(dispels??Array.Empty<BishopDispelRecord>()).ToArray();
            if(endings.Length>128||endings.Any(x=>x==null))throw new ArgumentException("Invalid Dispel history.");
            Dispels=Array.AsReadOnly(endings);
        }
        public BishopEntryRecord WithDispels(IEnumerable<BishopDispelRecord> dispels) => new BishopEntryRecord(DeclarationDigest,Departure,Invocations,AuraSaves,AuraHealing,dispels);
        public static BishopEntryRecord Announced() => new BishopEntryRecord(BishopProfile.DeclarationDigest);
        public BishopEntryRecord WithDeparture(BishopDepartureProof proof) => new BishopEntryRecord(DeclarationDigest,proof,Invocations,AuraSaves,AuraHealing,Dispels);
        public BishopEntryRecord WithInvocations(IEnumerable<DivineInvocationRecord> uses) => new BishopEntryRecord(DeclarationDigest,Departure,uses,AuraSaves,AuraHealing,Dispels);
        public BishopEntryRecord WithAuraSaves(IEnumerable<AuraOfFaithSaveRecord> saves) => new BishopEntryRecord(DeclarationDigest,Departure,Invocations,saves,AuraHealing,Dispels);
        public BishopEntryRecord WithAuraHealing(IEnumerable<AuraOfFaithHealingRecord> healing) => new BishopEntryRecord(DeclarationDigest,Departure,Invocations,AuraSaves,healing,Dispels);
    }

    /// <summary>A real paid edge started after positive base Rite care. Partial traversal does not complete the objective.</summary>
    public sealed class BishopDepartureProof
    {
        public string RestId { get; }
        public string RiteCommandId { get; }
        public long RiteRevision { get; }
        public string StepCommandId { get; }
        public long StepRevision { get; }
        public RuleTime StartedAt { get; }
        public string CompletionCommandId { get; }
        public long CompletedRevision { get; }
        public RuleTime CompletedAt { get; }
        public bool Complete => CompletedRevision != 0;
        public BishopDepartureProof(string restId,string riteCommand,long riteRevision,string stepCommand,long stepRevision,
            RuleTime startedAt,string completionCommand = "",long completedRevision = 0,RuleTime completedAt = default)
        {
            if (!Validation.ValidId(restId) || !Validation.ValidId(riteCommand) || !Validation.ValidId(stepCommand)
                || riteRevision < 1 || stepRevision <= riteRevision || startedAt < default(RuleTime)
                || completedRevision == 0 && (completionCommand != "" || completedAt != default(RuleTime))
                || completedRevision != 0 && (!Validation.ValidId(completionCommand) || completedRevision <= stepRevision || completedAt <= startedAt))
                throw new ArgumentException("Invalid Bishop departure evidence.");
            RestId=restId; RiteCommandId=riteCommand; RiteRevision=riteRevision; StepCommandId=stepCommand;
            StepRevision=stepRevision; StartedAt=startedAt; CompletionCommandId=completionCommand;
            CompletedRevision=completedRevision; CompletedAt=completedAt;
        }
        public BishopDepartureProof Finish(string command,long revision,RuleTime at)
            => new BishopDepartureProof(RestId,RiteCommandId,RiteRevision,StepCommandId,StepRevision,StartedAt,command,revision,at);
    }

    public static partial class BishopProfile
    {
        public const string FingerprintPrefix="TEST_ONLY.bishop-entry-v1-";
        public const byte Marker=17;
        public const string Approval="0a1c9139-3116-532b-8ee8-c436c82e4e27";
        public const string MechanicsApproval="9730ae44-9e01-5291-a4b2-d3515fedf2f7";
        public const string Milestone="TEST_ONLY.cleric3-recovery-care-departure";
        public const string Invocation="cleric.arch.divine-invocation", Aura="cleric.arch.aura-of-faith";
        public const string Dispel="dispel-magic-lesser", RepertoireEntitlement="cleric.repertoire.earned3";
        // SHA256 of the UTF8, key-sorted, compact whole source-card JSON, not a replacement source registry.
        public const string InvocationCardSha256="7dae262ad987193dc14e8ce21c6d45c5a2ad7d0f2008377d0217f5959e2848c2";
        public const string AuraCardSha256="56acc5fb191e255889bc45374d73b2ba55798a82fe5b5ab193731ab3d57ad448";
        public static IReadOnlyList<string> SelectedCards { get; }=Array.AsReadOnly(new[]{Aura,Invocation});
        public static string DeclarationBinding => string.Join("|",Milestone,ClericRpProfile.Actor,ConnectedVialRules.CarrierId,
            ClericRpProfile.SourceRevision,"declared0",ClericMilestoneDeclaration.FixedId,ClericLongRestProfile.SiteId,
            "first-eligible-benefit-after-earned2|later-positive-base-paid-rite-on-hero|later-paid-walk1,3-to2,3|five-feet-completed|both-alive|once-only");
        public static string DeclarationDigest { get; }=Digest(DeclarationBinding);
        private static string Digest(string value)
        {
            using(var sha=SHA256.Create())return string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(value))
                .Select(x=>x.ToString("x2",System.Globalization.CultureInfo.InvariantCulture)));
        }
        public static bool SelectedFingerprint(string value) => value != null && value.StartsWith(FingerprintPrefix,StringComparison.Ordinal);
        public static CharacterAdvancementRecord Advancement(Snapshot s) => s.BishopEntry == null ? null
            : s.CharacterAdvancements.SingleOrDefault(x=>x.ActorId==ClericRpProfile.Actor && x.MilestoneId==Milestone);
        public static bool Earned(Snapshot s) => Advancement(s)!=null;
        public static long CapacityRevisionBefore(Snapshot s,long revision)
            => Advancement(s) is CharacterAdvancementRecord a && a.Revision<revision ? a.Revision : s.ConvictionCapacity.PoolAcquiredRevision;
        public static int RpMaximumBefore(Snapshot s,long revision)
            => Advancement(s) is CharacterAdvancementRecord a && a.Revision<revision ? 7 : 4;
        public static bool ValidChoices(CharacterAdvancementRequest request) => request != null && request.UsesClericSettlementReceipt
            && request.FeatureIds.SequenceEqual(SelectedCards) && request.InvocationPath=="" && request.EarnedSpell==Dispel
            && request.AsiAbilityIncreases.Count==0 && request.FeatId=="";
        public static bool ValidAdvancement(Snapshot s,CharacterAdvancementRecord a) => s.BishopEntry!=null
            && a.ActorId==ClericRpProfile.Actor && a.MilestoneId==Milestone && a.ClassName=="Cleric" && a.ClassLevel==3
            && a.PreviousTotalLevel==2 && a.NewTotalLevel==3 && a.BaseHpGain==5 && a.HitPointMethod==HitPointGainMethod.FixedAverage
            && a.MaximumHpBefore==13 && a.MaximumHpAfter==18 && a.CurrentHpBefore<=13 && a.CurrentHpAfter==a.CurrentHpBefore
            && a.SelectedFeatureIds.SequenceEqual(SelectedCards) && a.AsiAbilityIncreases.Count==0
            && a.AbilityScoresBefore.Count==0 && a.AbilityScoresAfter.Count==0;
        public static bool ValidGrant(Snapshot s,CharacterFeatureGrantRecord g) => s.BishopEntry!=null
            && g.ActorId==ClericRpProfile.Actor && g.ClassName=="Cleric" && g.ClassLevel==3 && g.MilestoneId==Milestone
            && g.Origin==CharacterFeatureGrantOrigin.SelectedCard && SelectedCards.Contains(g.FeatureId)
            && Advancement(s)?.Revision==g.GrantedRevision;
        internal static void Validate(Snapshot s)
        {
            if ((s.BishopEntry!=null)!=SelectedFingerprint(s.ContentFingerprint))throw new ArgumentException("Invalid Bishop profile envelope.");
            if(s.BishopEntry==null)return;
            ValidateInvocations(s);
            ValidateAura(s);
            ValidateDispels(s);
            if(!s.TestOnly || s.SchemaVersion!=Snapshot.SurpriseEntrySchema || s.PostRecoveryEncounter==null
                || !s.ConnectedClericLongRest || s.BishopEntry.DeclarationDigest!=DeclarationDigest)
                throw new ArgumentException("Bishop entry requires its announced connected profile.");
            var proof=s.BishopEntry.Departure;
            if(proof!=null) {
                var rest=s.ClericLongRestSettlements.FirstOrDefault(x=>x.Benefit==ClericLongRestBenefit.Eligible);
                var rite=s.HealingRites.SingleOrDefault(x=>x.CommandId==proof.RiteCommandId);
                var start=s.Receipts.SingleOrDefault(x=>x.Id==proof.StepCommandId && x.Revision==proof.StepRevision);
                var command=start==null?null:CommandHistory.Read(start);
                if(rest==null || rest.RestId!=proof.RestId || rite==null || rite.Revision!=proof.RiteRevision
                    || rite.Revision<=rest.Revision || rite.At<=rest.At || rite.ActualGain<=0 || rite.RpPaid!=2
                    || rite.ActorId!=ClericRpProfile.Actor || rite.TargetId!=ConnectedVialRules.CarrierId
                    || proof.StartedAt<rite.At || proof.StepRevision>s.Revision || proof.StartedAt>s.RuleClock
                    || start?.Principal!="TEST_ONLY.host" || command?.Kind!=CommandKind.BeginWorldStep
                    || command.Actor!=ClericRpProfile.Actor || command.Target!="walk" || command.X!=1 || command.Y!=0)
                    throw new ArgumentException("Unattributed Bishop recovery/care/departure.");
                if(proof.Complete && (proof.CompletedRevision>s.Revision || proof.CompletedAt>s.RuleClock
                    || !s.Receipts.Any(x=>x.Id==proof.CompletionCommandId && x.Revision==proof.CompletedRevision)))
                    throw new ArgumentException("Bishop objective lacks actual completed traversal.");
            }
            var award=s.CharacterMilestones.SingleOrDefault(x=>x.ActorId==ClericRpProfile.Actor && x.MilestoneId==Milestone);
            var advanced=Advancement(s);
            if(award!=null) {
                var receipt=s.Receipts.SingleOrDefault(x=>x.Revision==award.AwardedRevision);
                var command=receipt==null?null:CommandHistory.Read(receipt);
                if(proof?.Complete!=true || award.AwardedRevision<=proof.CompletedRevision || receipt?.Principal!="TEST_ONLY.host"
                    || command?.Kind!=CommandKind.AwardCharacterMilestone || command.Actor!=ClericRpProfile.Actor || command.Target!=Milestone)
                    throw new ArgumentException("Unattributed Bishop milestone award.");
            }
            if(advanced!=null) {
                var receipt=s.Receipts.SingleOrDefault(x=>x.Revision==advanced.Revision);
                var command=receipt==null?null:CommandHistory.Read(receipt);
                if(!ValidAdvancement(s,advanced) || award?.ConsumedRevision!=advanced.Revision
                    || receipt?.Principal!="TEST_ONLY.host" || command?.Kind!=CommandKind.AdvanceCharacterLevel
                    || command.Actor!=ClericRpProfile.Actor || command.Target!=Milestone || !ValidChoices(command.Advancement)
                    || s.CharacterFeatureGrants.Count(x=>ValidGrant(s,x))!=2
                    || s.CharacterHitDice.Count(x=>x.ActorId==ClericRpProfile.Actor && x.LevelOrdinal==3 && x.ClassName=="Cleric" && x.DieSize==8)!=1)
                    throw new ArgumentException("Invalid atomic earned Bishop provenance.");
            }
        }
    }
}
