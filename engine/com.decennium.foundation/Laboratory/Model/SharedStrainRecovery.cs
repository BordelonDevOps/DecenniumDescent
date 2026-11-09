#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation.Laboratory
{
    /// <summary>Explicit TEST_ONLY authorization for secure-rest eligibility. This is a separate
    /// authored fact and fingerprint from safe-berth and qualifying-Rest eligibility.</summary>
    public sealed class TestOnlyExpeditionStrainRecoveryProfile
    {
        public const string SourceId = "campaign.secure-long-rest";
        public const string TrackId = "expedition.strain";
        public const string SourceRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string StrainBlob = "7005aaf9558f0ce4f445ffe982dfa9b6f36c8ee4";
        public const string ExpeditionBookBlob = "466871fc128dc5f06043a874da2b9c1d94ed80a5";
        private readonly string[] secureRestSiteIds;
        public System.Collections.Generic.IReadOnlyList<string> SecureRestSiteIds
            => Array.AsReadOnly(secureRestSiteIds);

        public TestOnlyExpeditionStrainRecoveryProfile(System.Collections.Generic.IEnumerable<string> secureRestSiteIds = null)
        {
            this.secureRestSiteIds = (secureRestSiteIds ?? new[] { "TEST_ONLY.safe-berth" })
                .OrderBy(x => x, StringComparer.Ordinal).ToArray();
            if (this.secureRestSiteIds.Length == 0 || this.secureRestSiteIds.Any(x => !Validation.ValidId(x))
                || this.secureRestSiteIds.Distinct(StringComparer.Ordinal).Count() != this.secureRestSiteIds.Length)
                throw new ArgumentException("Secure Rest requires an explicit finite TEST_ONLY site list.");
        }

        internal string LegacyCanonicalKey => "expedition-strain-recovery-v1|source=" + SourceId + "|track=" + TrackId
            + "|book=" + ExpeditionBookBlob + "|strain=" + StrainBlob + "|revision=" + SourceRevision
            + "|long-rest=28800|max-beneficial-per-24h=1|secure-sites=" + string.Join(";", secureRestSiteIds)
            + "|legacy-base-vessel-handover=1|unlinked-carried-mass=1";

        internal string CanonicalKey => "expedition-strain-recovery-v2|source=" + SourceId + "|track=" + TrackId
            + "|book=" + ExpeditionBookBlob + "|strain=" + StrainBlob + "|revision=" + SourceRevision
            + "|long-rest=28800|max-beneficial-per-24h=1|beneficial-rest-recorded-at-completion=1"
            + "|clock-continuation-through-recovery-choice=1|secure-sites=" + string.Join(";", secureRestSiteIds)
            + "|legacy-base-vessel-handover=1|unlinked-carried-mass=1";

        internal bool IsSecure(string siteId) => secureRestSiteIds.Contains(siteId, StringComparer.Ordinal);

        internal string ValidateBindings(TestOnlyRestDebtProfile restProfile)
            => restProfile != null && secureRestSiteIds.All(id => restProfile.Sites.Any(site => site.Id == id
                && site.SafeBerth && site.QualifyingRestEligible)) ? null : "StrainRecoverySecureSiteNotQualified";

        internal static string BindFingerprint(string prior, TestOnlyExpeditionStrainRecoveryProfile profile, bool legacy = false)
        {
            using (var sha = SHA256.Create())
                return (legacy ? "TEST_ONLY.strain-recovery-v1-" : "TEST_ONLY.strain-recovery-v2-") + string.Concat(sha.ComputeHash(
                    Encoding.UTF8.GetBytes(prior + "|" + (legacy ? profile.LegacyCanonicalKey : profile.CanonicalKey)))
                    .Select(b => b.ToString("x2", CultureInfo.InvariantCulture)));
        }
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private TestOnlyExpeditionStrainRecoveryProfile strainRecoveryProfile;
        private bool legacyStrainRecoverySemantics;

        /// <summary>Selects schema64's bounded source-bound Expedition Strain recovery slice.
        /// Must follow daily provisioning and Rest Debt profile selection before Initial().</summary>
        public TestOnlySharedWorldPolicy EnableExpeditionStrainRecovery(
            TestOnlyExpeditionStrainRecoveryProfile profile = null)
        {
            if (initializationStarted) throw new InvalidOperationException("Strain recovery profile must be selected before Initial().");
            if (restDebtProfile == null) throw new InvalidOperationException("Strain recovery requires the Rest Debt profile.");
            if (strainRecoveryProfile != null) throw new InvalidOperationException("Strain recovery profile is already selected.");
            strainRecoveryProfile = profile ?? new TestOnlyExpeditionStrainRecoveryProfile();
            string error = strainRecoveryProfile.ValidateBindings(restDebtProfile);
            if (error != null) throw new ArgumentException(error, nameof(profile));
            ContentFingerprint = TestOnlyExpeditionStrainRecoveryProfile.BindFingerprint(ContentFingerprint, strainRecoveryProfile);
            return this;
        }

        /// <summary>Selects the prior schema64 recovery behavior and fingerprint so an already
        /// supported schema64 save can be loaded and replayed without applying newer Rest timing.
        /// Use only when opening a save created by the v1 profile.</summary>
        public TestOnlySharedWorldPolicy EnableLegacyExpeditionStrainRecovery(
            TestOnlyExpeditionStrainRecoveryProfile profile = null)
        {
            if (initializationStarted) throw new InvalidOperationException("Strain recovery profile must be selected before Initial().");
            if (restDebtProfile == null) throw new InvalidOperationException("Strain recovery requires the Rest Debt profile.");
            if (strainRecoveryProfile != null) throw new InvalidOperationException("Strain recovery profile is already selected.");
            strainRecoveryProfile = profile ?? new TestOnlyExpeditionStrainRecoveryProfile();
            string error = strainRecoveryProfile.ValidateBindings(restDebtProfile);
            if (error != null) throw new ArgumentException(error, nameof(profile));
            legacyStrainRecoverySemantics = true;
            ContentFingerprint = TestOnlyExpeditionStrainRecoveryProfile.BindFingerprint(
                ContentFingerprint, strainRecoveryProfile, legacy: true);
            return this;
        }

        private void InitializeStrainRecovery(Snapshot s)
        {
            if (strainRecoveryProfile == null) return;
            int expectedSchema = havenCareProfile != null ? Snapshot.HavenCareSchema
                : moraleRestProfile != null ? Snapshot.MoraleRestSchema : Snapshot.ExpeditionStrainRecoverySchema;
            if (s.SchemaVersion != expectedSchema)
                throw new InvalidOperationException("StrainRecoveryRequiresSelectedSchema");
            s.ExpeditionStrainRecoveryGateUpdates = Array.Empty<ExpeditionStrainRecoveryGateUpdateRecord>();
            s.ExpeditionBeneficialRests = Array.Empty<ExpeditionBeneficialRestRecord>();
            s.ExpeditionStrainRecoveryOffers = Array.Empty<ExpeditionStrainRecoveryOfferRecord>();
            s.ExpeditionStrainRemovals = Array.Empty<ExpeditionStrainRemovalRecord>();
        }

        private void ClampExpeditionStrainLife(Snapshot s)
        {
            if(strainRecoveryProfile==null)return;
            foreach(string actor in dailyProvisioning.Roster)
                ExpeditionStrainRules.ClampLife(s,actor,s.RuleClock,s.Revision+1);
        }

        private bool IsStrainRecoveryCommand(CommandKind kind)
            => kind == CommandKind.ResolveExpeditionStrainRecovery;

        private ExpeditionStrainRecoveryOfferRecord PendingRecoveryOffer(Snapshot s, string actorId)
            => strainRecoveryProfile == null ? null : s.ExpeditionStrainRecoveryOffers
                .SingleOrDefault(x => x.Pending && x.ActorId == actorId);

        private bool HasPendingRecoveryOffer(Snapshot s)
            => strainRecoveryProfile != null && s.ExpeditionStrainRecoveryOffers.Any(x => x.Pending);

        private string PendingRecoveryChoiceFailure(Snapshot s, Command c)
            => HasPendingRecoveryOffer(s) && !IsStrainRecoveryCommand(c.Kind)
                ? "ExpeditionStrainRecoveryChoicePending" : null;

        private string RecordProvisioningGateUpdates(Snapshot s, DailyProvisioningSettlementRecord settlement)
        {
            if (strainRecoveryProfile == null || settlement.HasShortfall) return null;
            var points = s.ExpeditionStrainGains.Where(g => g.ActorId == settlement.ActorId
                    && g.CauseKind == ExpeditionStrainCauseKind.DailyProvisioning && g.PointId != ""
                    && g.OrdinaryRemovable == true && g.RemovalGateMet == false && g.At < settlement.End
                    && !s.ExpeditionStrainRecoveryGateUpdates.Any(x => x.PointId == g.PointId)
                    && s.DailyProvisioningSettlements.Any(source => source.Id == g.CauseId
                        && source.DayOrdinal < settlement.DayOrdinal))
                .OrderBy(g => g.PointId, StringComparer.Ordinal).ToArray();
            if (s.ExpeditionStrainRecoveryGateUpdates.Length + points.Length
                > ExpeditionProvisioningValidation.MaxStrainRecoveryGateUpdates)
                return "ExpeditionStrainRecoveryGateHistoryCapacityReached";
            foreach (var gain in points)
            {
                string id = "strain.gate.r" + settlement.Revision.ToString(CultureInfo.InvariantCulture)
                    + ".e" + s.ExpeditionStrainRecoveryGateUpdates.Length.ToString(CultureInfo.InvariantCulture);
                var update = new ExpeditionStrainRecoveryGateUpdateRecord(id, gain.ActorId, gain.PointId,
                    settlement.Id, settlement.End, settlement.Revision);
                s.ExpeditionStrainRecoveryGateUpdates = s.ExpeditionStrainRecoveryGateUpdates.Concat(new[] { update }).ToArray();
            }
            return null;
        }

        private bool ProvisioningBlockActive(Snapshot s, string actorId, RuleTime at)
            => s.DailyProvisioningSettlements.Where(x => x.ActorId == actorId && x.End <= at)
                .OrderByDescending(x => x.End).FirstOrDefault()?.HasShortfall == true;

        private bool RestDebtOwedAt(Snapshot s, string actorId, RuleTime at, long revision)
        {
            bool owed = false;
            foreach (var e in s.RestDebtEvents.Where(x => x.ActorId == actorId && x.At <= at && x.Revision <= revision)
                .OrderBy(x => x.At).ThenBy(x => x.Revision).ThenBy(x => x.EventSequence))
            {
                if (e.Kind == RestDebtEventKind.Opened || e.Kind == RestDebtEventKind.MissedWhileIndebted) owed = true;
                else if (e.Kind == RestDebtEventKind.Cleared) owed = false;
            }
            return owed;
        }

        private RuleTime? LastBeneficialRest(Snapshot s, string actorId, RuleTime at, long revision,
            string excludeRestIntervalId = "")
            => s.ExpeditionBeneficialRests.Where(x => x.ActorId == actorId
                    && x.CompletedAt <= at && x.Revision <= revision
                    && x.RestIntervalId != excludeRestIntervalId)
                .Select(x => (RuleTime?)x.CompletedAt).OrderByDescending(x => x).FirstOrDefault();

        private string[] EligibleRecoveryPoints(Snapshot s, string actorId, RuleTime at, long revision)
        {
            if (strainRecoveryProfile == null || !restDebtProfile.IncludesActor(actorId)
                || ProvisioningBlockActive(s, actorId, at) || RestDebtOwedAt(s, actorId, at, revision))
                return Array.Empty<string>();
            return s.ExpeditionStrainGains.Where(g => g.ActorId == actorId && g.PointId != ""
                    && g.AddedAmount == 1 && g.OrdinaryRemovable == true
                    && ExpeditionStrainRules.RecoveryGateMet(s, g, at, revision)
                    && ExpeditionStrainRules.IsActivePoint(s, actorId, g.PointId, at, revision))
                .Select(g => g.PointId).OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }

        private string OpenStrainRecoveryOffers(Snapshot s, Command initiating)
        {
            if (strainRecoveryProfile == null) return null;
            if (moraleRestProfile != null) return OpenSchema65SecureRestOffers(s, initiating);
            var completed = s.RestIntervals.Where(x => x.Status == RestIntervalStatus.Completed
                    && x.EndedAt == s.RuleClock && strainRecoveryProfile.IsSecure(x.SiteId))
                .OrderBy(x => x.ActorId, StringComparer.Ordinal).ThenBy(x => x.Id, StringComparer.Ordinal).ToArray();
            foreach (var interval in completed)
            {
                if (s.ExpeditionBeneficialRests.Any(x => x.RestIntervalId == interval.Id)
                    || s.ExpeditionStrainRecoveryOffers.Any(x => x.RestIntervalId == interval.Id)) continue;
                var last = LastBeneficialRest(s, interval.ActorId, interval.EndedAt.Value, s.Revision + 1);
                if (last.HasValue && interval.EndedAt.Value < last.Value.AddSeconds(24 * 60 * 60)) continue;

                // The source's once-per-24-hours limit applies to this beneficial Rest even when
                // a persistent provisioning block or the absence of removable points prevents a
                // Strain reduction. Rest Debt remains a separate eligibility requirement.
                if (RestDebtOwedAt(s, interval.ActorId, interval.EndedAt.Value, s.Revision + 1)) continue;
                string[] points = EligibleRecoveryPoints(s, interval.ActorId, s.RuleClock, s.Revision + 1);
                if (legacyStrainRecoverySemantics)
                {
                    if (points.Length == 0) continue;
                    if (initiating == null) return "StrainRecoveryInitiatingCommandMissing";
                    if (s.ExpeditionStrainRecoveryOffers.Length >= ExpeditionProvisioningValidation.MaxStrainRecoveryOffers)
                        return "ExpeditionStrainRecoveryOfferHistoryCapacityReached";
                    string legacyOfferId = "strain.recovery.offer.r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture)
                        + ".n" + s.ExpeditionStrainRecoveryOffers.Length.ToString(CultureInfo.InvariantCulture);
                    var legacyOffer = new ExpeditionStrainRecoveryOfferRecord(legacyOfferId, interval.ActorId, interval.Id,
                        initiating.Id, interval.EndedAt.Value, s.Revision + 1, points);
                    s.ExpeditionStrainRecoveryOffers = s.ExpeditionStrainRecoveryOffers.Concat(new[] { legacyOffer }).ToArray();
                    continue;
                }
                if (s.ExpeditionBeneficialRests.Length >= ExpeditionProvisioningValidation.MaxBeneficialRests)
                    return "ExpeditionBeneficialRestHistoryCapacityReached";
                string offerId = "";
                if (points.Length != 0)
                {
                    if (initiating == null) return "StrainRecoveryInitiatingCommandMissing";
                    if (s.ExpeditionStrainRecoveryOffers.Length >= ExpeditionProvisioningValidation.MaxStrainRecoveryOffers)
                        return "ExpeditionStrainRecoveryOfferHistoryCapacityReached";
                    offerId = "strain.recovery.offer.r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture)
                        + ".n" + s.ExpeditionStrainRecoveryOffers.Length.ToString(CultureInfo.InvariantCulture);
                }
                string benefitId = "strain.benefit.r" + (s.Revision + 1).ToString(CultureInfo.InvariantCulture)
                    + ".n" + s.ExpeditionBeneficialRests.Length.ToString(CultureInfo.InvariantCulture);
                var benefit = new ExpeditionBeneficialRestRecord(benefitId, interval.ActorId, offerId,
                    interval.Id, interval.EndedAt.Value, s.Revision + 1);
                s.ExpeditionBeneficialRests = s.ExpeditionBeneficialRests.Concat(new[] { benefit }).ToArray();
                if (offerId != "")
                {
                    var offer = new ExpeditionStrainRecoveryOfferRecord(offerId, interval.ActorId, interval.Id,
                        initiating.Id, interval.EndedAt.Value, s.Revision + 1, points);
                    s.ExpeditionStrainRecoveryOffers = s.ExpeditionStrainRecoveryOffers.Concat(new[] { offer }).ToArray();
                }
            }
            return null;
        }

        private string AssessStrainRecoveryChoice(Snapshot s, Command c, out ExpeditionStrainRecoveryOfferRecord offer,
            out ExpeditionStrainGainRecord gain)
        {
            offer = null; gain = null;
            if (moraleRestProfile != null && s.SchemaVersion >= Snapshot.MoraleRestSchema)
                return AssessSchema65RecoveryChoice(s, c, out offer, out gain);
            if (strainRecoveryProfile == null || s.SchemaVersion != Snapshot.ExpeditionStrainRecoverySchema)
                return "StrainRecoveryNotSelected";
            if (c.X != 0 || c.Y != 0 || c.Target == "" || c.Inventory != null || c.Combat != null
                || c.Advancement != null || c.Ranged != null || c.OverwatchRider != OverwatchRider.None
                || c.SuppressionFire != null || c.DefensiveFormation != null || c.ExpeditionAssignment != null
                || c.HarvestSelection != null || c.MiningSelection != null || c.ProspectingExposure != null
                || c.RouteMappingWork != null)
                return "InvalidStrainRecoveryChoicePayload";
            var selectedOffer = PendingRecoveryOffer(s, c.Actor);
            offer = selectedOffer;
            if (selectedOffer == null) return "NoPendingStrainRecoveryChoice";
            if (!selectedOffer.PointIds.Contains(c.Target, StringComparer.Ordinal)) return "StrainRecoveryPointNotOffered";
            var interval = s.RestIntervals.SingleOrDefault(x => x.Id == selectedOffer.RestIntervalId && x.ActorId == c.Actor
                && x.Status == RestIntervalStatus.Completed && x.EndedAt == selectedOffer.CompletedAt);
            if (interval == null || !strainRecoveryProfile.IsSecure(interval.SiteId)
                || !restDebtProfile.Site(interval.SiteId).SafeBerth || !restDebtProfile.Site(interval.SiteId).QualifyingRestEligible)
                return "StrainRecoveryRestNoLongerSecure";
            if (s.RuleClock != selectedOffer.CompletedAt) return "StrainRecoveryOfferClockChanged";
            if (RestDebtOwedAt(s, c.Actor, selectedOffer.CompletedAt, s.Revision + 1)) return "RestDebtPreventsStrainRecovery";
            if (ProvisioningBlockActive(s, c.Actor, selectedOffer.CompletedAt)) return "ProvisioningBlockPreventsStrainRecovery";
            var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.RestIntervalId == selectedOffer.RestIntervalId
                && x.ActorId == c.Actor && x.CompletedAt == selectedOffer.CompletedAt
                && x.RecoveryOfferId == selectedOffer.Id);
            // Older schema64 pending-choice saves recorded a benefit only when the player
            // resolved the offer. Keep those already-supported saves playable.
            if (benefit == null && !selectedOffer.Pending) return "StrainRecoveryBenefitMissing";
            var last = LastBeneficialRest(s, c.Actor, selectedOffer.CompletedAt, s.Revision + 1,
                selectedOffer.RestIntervalId);
            if (last.HasValue && selectedOffer.CompletedAt < last.Value.AddSeconds(24 * 60 * 60))
                return "BeneficialLongRestLimitNotElapsed";
            gain = s.ExpeditionStrainGains.SingleOrDefault(x => x.ActorId == c.Actor && x.PointId == c.Target);
            if (gain == null || gain.AddedAmount != 1 || gain.OrdinaryRemovable != true
                || !ExpeditionStrainRules.RecoveryGateMet(s, gain, selectedOffer.CompletedAt, s.Revision + 1)
                || !ExpeditionStrainRules.IsActivePoint(s, c.Actor, c.Target, selectedOffer.CompletedAt, s.Revision + 1))
                return "StrainRecoveryPointNotEligible";
            return null;
        }

        private string ResolveStrainRecoveryChoice(Snapshot s, Command c)
        {
            if (moraleRestProfile != null && s.SchemaVersion >= Snapshot.MoraleRestSchema)
                return ResolveSchema65RecoveryChoice(s, c);
            string failure = AssessStrainRecoveryChoice(s, c, out var offer, out var gain);
            if (failure != null) return failure;
            if (s.ExpeditionStrainRemovals.Length >= ExpeditionProvisioningValidation.MaxStrainRemovals)
                return "ExpeditionStrainRecoveryHistoryCapacityReached";
            long revision = s.Revision + 1;
            var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.RestIntervalId == offer.RestIntervalId
                && x.ActorId == c.Actor && x.RecoveryOfferId == offer.Id);
            if (benefit == null)
            {
                if (s.ExpeditionBeneficialRests.Length >= ExpeditionProvisioningValidation.MaxBeneficialRests)
                    return "ExpeditionBeneficialRestHistoryCapacityReached";
                string benefitId = "strain.benefit.r" + revision.ToString(CultureInfo.InvariantCulture)
                    + ".n" + s.ExpeditionBeneficialRests.Length.ToString(CultureInfo.InvariantCulture);
                benefit = new ExpeditionBeneficialRestRecord(benefitId, c.Actor, offer.Id,
                    offer.RestIntervalId, offer.CompletedAt, revision);
                s.ExpeditionBeneficialRests = s.ExpeditionBeneficialRests.Concat(new[] { benefit }).ToArray();
            }
            int sequence = ExpeditionStrainRules.NextGainSequence(s, c.Actor, revision);
            string removalId = "strain.removal.r" + revision.ToString(CultureInfo.InvariantCulture)
                + ".n" + s.ExpeditionStrainRemovals.Length.ToString(CultureInfo.InvariantCulture);
            var removal = new ExpeditionStrainRemovalRecord(removalId, c.Actor, gain.PointId, gain.Id,
                benefit.Id, offer.CompletedAt, revision, sequence);
            var previous = ExpeditionStrainRules.Current(s, c.Actor);
            s.ExpeditionStrainRemovals = s.ExpeditionStrainRemovals.Concat(new[] { removal }).ToArray();
            s.ExpeditionStrainRecoveryOffers = s.ExpeditionStrainRecoveryOffers.Select(x => x.Id == offer.Id
                ? new ExpeditionStrainRecoveryOfferRecord(x.Id, x.ActorId, x.RestIntervalId, x.InitiatingCommandId,
                    x.CompletedAt, x.Revision, x.PointIds, c.Target, revision) : x).ToArray();
            var current = ExpeditionStrainRules.Project(s, c.Actor, s.RuleClock, revision);
            if (current.Level != previous.Level - 1) return "StrainRecoveryProjectionMismatch";
            if (previous.Level >= 3 && current.Level < 3)
                s.ExpeditionDashLocks = s.ExpeditionDashLocks.Where(x => x.ActorId != c.Actor).ToArray();
            // Effective maximum HP may rise, but this recovery never heals or revives.
            return legacyStrainRecoverySemantics || HasPendingRecoveryOffer(s) || ManufacturingChoicePending(s)
                ? null : ResumeManufacturingAdvance(s, c);
        }

        private CommandQueryResult QueryStrainRecoveryChoice(Snapshot s, Command c)
        {
            string failure = AssessStrainRecoveryChoice(s, c, out _, out _);
            return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision);
        }

        private System.Collections.Generic.IEnumerable<Command> DiscoverStrainRecoveryChoices(Snapshot s, string actor)
        {
            var offer = PendingRecoveryOffer(s, actor);
            if (offer == null) return Array.Empty<Command>();
            return offer.PointIds.Select((pointId, index) => new Command(
                "option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".strain-recovery." + index.ToString(CultureInfo.InvariantCulture),
                actor, s.Revision, CommandKind.ResolveExpeditionStrainRecovery, pointId)).ToArray();
        }

        private string ValidateStrainRecoveryState(Snapshot s)
        {
            if (moraleRestProfile != null) return ValidateSchema65StrainRecoveryState(s);
            if (strainRecoveryProfile == null)
                return s.SchemaVersion != Snapshot.ExpeditionStrainRecoverySchema
                    && s.ExpeditionStrainRecoveryGateUpdates.Length == 0 && s.ExpeditionBeneficialRests.Length == 0
                    && s.ExpeditionStrainRecoveryOffers.Length == 0 && s.ExpeditionStrainRemovals.Length == 0
                    ? null : "StrainRecoveryProfileMissing";
            if (s.SchemaVersion != Snapshot.ExpeditionStrainRecoverySchema || !s.TestOnly
                || s.ContentFingerprint != ContentFingerprint || strainRecoveryProfile.ValidateBindings(restDebtProfile) != null)
                return "StrainRecoveryProfileMismatch";
            foreach (var offer in s.ExpeditionStrainRecoveryOffers)
            {
                var interval = s.RestIntervals.Single(x => x.Id == offer.RestIntervalId);
                if (!strainRecoveryProfile.IsSecure(interval.SiteId) || !restDebtProfile.IncludesActor(offer.ActorId)
                    || RestDebtOwedAt(s, offer.ActorId, offer.CompletedAt, offer.Revision)
                    || ProvisioningBlockActive(s, offer.ActorId, offer.CompletedAt)
                    || EligibleRecoveryPointsWithoutDebt(s, offer.ActorId, offer.CompletedAt, offer.Revision)
                        .Except(offer.PointIds, StringComparer.Ordinal).Any())
                    return "StrainRecoveryOfferProfileMismatch";
                var benefit = s.ExpeditionBeneficialRests.SingleOrDefault(x => x.RestIntervalId == offer.RestIntervalId
                    && x.ActorId == offer.ActorId && x.CompletedAt == offer.CompletedAt
                    && x.RecoveryOfferId == offer.Id);
                if (benefit == null && !offer.Pending) return "StrainRecoveryOfferHasNoBeneficialRest";
                if (benefit != null && benefit.Revision != offer.Revision && benefit.Revision != offer.ResolvedRevision)
                    return "StrainRecoveryOfferBenefitRevisionMismatch";
                if (legacyStrainRecoverySemantics && (offer.Pending ? benefit != null
                    : benefit == null || benefit.Revision != offer.ResolvedRevision))
                    return "LegacyStrainRecoveryRecordMismatch";
                var prior = LastBeneficialRest(s, offer.ActorId, offer.CompletedAt, offer.Revision,
                    offer.RestIntervalId);
                if (prior.HasValue && offer.CompletedAt < prior.Value.AddSeconds(24 * 60 * 60))
                    return "StrainRecoveryOfferExceedsBeneficialRestLimit";
                foreach (string pointId in offer.PointIds)
                    if (!EligibleRecoveryPointsWithoutDebt(s, offer.ActorId, offer.CompletedAt, offer.Revision).Contains(pointId, StringComparer.Ordinal))
                        return "StrainRecoveryOfferContainsIneligiblePoint";
            }
            foreach (var benefit in s.ExpeditionBeneficialRests)
            {
                var interval = s.RestIntervals.Single(x => x.Id == benefit.RestIntervalId);
                if (!strainRecoveryProfile.IsSecure(interval.SiteId) || !restDebtProfile.IncludesActor(benefit.ActorId)
                    || RestDebtOwedAt(s, benefit.ActorId, benefit.CompletedAt, benefit.Revision)
                    || legacyStrainRecoverySemantics && ProvisioningBlockActive(s, benefit.ActorId, benefit.CompletedAt))
                    return "StrainRecoveryBenefitProfileMismatch";
                var linkedOffer = s.ExpeditionStrainRecoveryOffers.SingleOrDefault(x => x.RestIntervalId == benefit.RestIntervalId);
                if (benefit.RecoveryOfferId == "" ? linkedOffer != null
                    : linkedOffer == null || linkedOffer.Id != benefit.RecoveryOfferId)
                    return "StrainRecoveryBenefitOfferLinkMismatch";
                var prior = LastBeneficialRest(s, benefit.ActorId, benefit.CompletedAt, benefit.Revision,
                    benefit.RestIntervalId);
                if (prior.HasValue && benefit.CompletedAt < prior.Value.AddSeconds(24 * 60 * 60))
                    return "StrainRecoveryBenefitExceedsBeneficialRestLimit";
                if (legacyStrainRecoverySemantics)
                {
                    var removal = s.ExpeditionStrainRemovals.SingleOrDefault(x => x.BeneficialRestId == benefit.Id);
                    var gain = removal == null ? null : s.ExpeditionStrainGains.SingleOrDefault(x => x.Id == removal.GainId);
                    if (removal == null || gain == null
                        || !ExpeditionStrainRules.RecoveryGateMet(s, gain, benefit.CompletedAt, benefit.Revision))
                        return "LegacyStrainRecoveryBenefitHasNoEligibleRemoval";
                }
            }
            return null;
        }

        private string[] EligibleRecoveryPointsWithoutDebt(Snapshot s, string actorId, RuleTime at, long revision)
        {
            if (strainRecoveryProfile == null || !restDebtProfile.IncludesActor(actorId) || ProvisioningBlockActive(s, actorId, at))
                return Array.Empty<string>();
            return s.ExpeditionStrainGains.Where(g => g.ActorId == actorId && g.PointId != ""
                    && g.AddedAmount == 1 && g.OrdinaryRemovable == true
                    && ExpeditionStrainRules.RecoveryGateMet(s, g, at, revision)
                    && ExpeditionStrainRules.IsActivePoint(s, actorId, g.PointId, at, revision))
                .Select(g => g.PointId).OrderBy(x => x, StringComparer.Ordinal).ToArray();
        }
    }
}
#endif
