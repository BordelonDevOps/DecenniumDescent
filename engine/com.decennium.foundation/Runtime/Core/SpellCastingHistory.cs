using System;

namespace Decennium.Foundation
{
    /// <summary>A committed cast, with the actual paid transaction and historical source/character facts.</summary>
    public sealed class SpellCastRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string TargetId { get; }
        public string SpellId { get; }
        public string SourceRevision => SpellSourceCatalog.SourceRevision;
        public string ProcedureSha256 => SpellSourceCatalog.Get(SpellId).ProcedureSha256;
        public long KnownAcquiredRevision { get; }
        public int ClassLevel { get; }
        public int Rank { get; }
        public int Proficiency { get; }
        public int CastingModifier { get; }
        public int SpellDc { get; }
        public long StanceRevision { get; }
        public bool FocusedDcElected { get; }
        public string FocusItemId { get; }
        public bool FocusHeld { get; }
        public int AvailableHands { get; }
        public bool WillingTarget { get; }
        public SpellTurnIdentity Turn { get; }
        public RuleTime At { get; }
        public int RpBefore { get; }
        public int BaseRp { get; }
        public int Surcharge { get; }
        public int RpAfter { get; }
        public int DissonanceBefore { get; }
        public int DissonanceAfter { get; }
        public int AppliedRefrain { get; }
        public string EffectId { get; }
        public int StableRecoveryD4 { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public SpellCastRecord(string commandId, long revision, string actorId, string targetId, string spellId,
            long knownAcquiredRevision, int classLevel, int rank, int proficiency, int castingModifier, int spellDc,
            long stanceRevision, bool focusedDcElected, string focusItemId, bool focusHeld, int availableHands,
            bool willingTarget, SpellTurnIdentity turn, RuleTime at, int rpBefore, int baseRp, int surcharge, int rpAfter,
            int dissonanceBefore, int dissonanceAfter, int appliedRefrain, string effectId, int stableRecoveryD4,
            uint randomBefore, uint randomAfter, long wordsConsumed, bool bishop = false)
        {
            var access = SpellSourceCatalog.Get(spellId)?.AccessFor("Cleric");
            if (!Validation.ValidId(commandId) || revision < 1 || !Validation.ValidId(actorId) || !Validation.ValidId(targetId)
                || !SpellCastingProfile.IsAdmittedSpell(spellId,bishop) || access == null || knownAcquiredRevision < 0 || knownAcquiredRevision >= revision
                || classLevel < access.MinimumClassLevel || classLevel > (bishop?3:2) || rank != access.Rank || proficiency < 0
                || spellDc != checked(8 + proficiency + castingModifier + (focusedDcElected ? 1 : 0)) || stanceRevision < 0
                || focusedDcElected && (spellId != "sanctuary" || stanceRevision == 0)
                || focusItemId == null || focusItemId != "" && !Validation.ValidId(focusItemId)
                || focusHeld && focusItemId == "" || availableHands < 0 || availableHands > 2
                || turn == null || turn.IsCarried || turn.ActorId != actorId || rpBefore < 0 || baseRp != access.BaseRpCost
                || surcharge < 0 || surcharge > 3 || rank == 0 && surcharge != 0 || rpAfter < 0
                || rpAfter != rpBefore - baseRp - surcharge || dissonanceBefore < 0 || appliedRefrain < 0 || appliedRefrain > 3
                || dissonanceAfter != checked(dissonanceBefore + (rank == 0 ? 0 : 1) + appliedRefrain)
                || effectId == null || effectId != "" && !Validation.ValidId(effectId)
                || (spellId == "spare-the-dying" ? stableRecoveryD4 < 1 || stableRecoveryD4 > 4 : stableRecoveryD4 != 0)
                || wordsConsumed < 0 || wordsConsumed == 0 && randomBefore != randomAfter)
                throw new ArgumentException("Invalid ordinary casting transaction history.");
            CommandId = commandId; Revision = revision; ActorId = actorId; TargetId = targetId; SpellId = spellId;
            KnownAcquiredRevision = knownAcquiredRevision; ClassLevel = classLevel; Rank = rank; Proficiency = proficiency;
            CastingModifier = castingModifier; SpellDc = spellDc; StanceRevision = stanceRevision; FocusedDcElected = focusedDcElected;
            FocusItemId = focusItemId; FocusHeld = focusHeld; AvailableHands = availableHands; WillingTarget = willingTarget;
            Turn = turn; At = at; RpBefore = rpBefore; BaseRp = baseRp; Surcharge = surcharge; RpAfter = rpAfter;
            DissonanceBefore = dissonanceBefore; DissonanceAfter = dissonanceAfter; AppliedRefrain = appliedRefrain;
            EffectId = effectId; StableRecoveryD4 = stableRecoveryD4; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
    }

    public enum GuidanceCheckKind { Hide, Search, MedicineStabilization }
    public sealed class GuidanceUseRecord
    {
        public string EffectId { get; }
        public string ActorId { get; }
        public string CommandId { get; }
        public long Revision { get; }
        public string CheckId { get; }
        public GuidanceCheckKind CheckKind { get; }
        public RuleTime At { get; }
        public int D4 { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public GuidanceUseRecord(string effectId, string actorId, string commandId, long revision, string checkId,
            GuidanceCheckKind checkKind, RuleTime at, int d4, uint randomBefore, uint randomAfter, long wordsConsumed)
        {
            if (!Validation.ValidId(effectId) || !Validation.ValidId(actorId) || !Validation.ValidId(commandId) || revision < 1
                || !Validation.ValidId(checkId) || !Enum.IsDefined(typeof(GuidanceCheckKind), checkKind)
                || d4 < 1 || d4 > 4 || wordsConsumed < 1) throw new ArgumentException("Invalid Guidance consumption.");
            EffectId = effectId; ActorId = actorId; CommandId = commandId; Revision = revision; CheckId = checkId;
            CheckKind = checkKind; At = at; D4 = d4; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
    }

    public enum SpellSaveKind { SanctuaryWisdom, ConcentrationConstitution }
    public sealed class SpellSaveRecord
    {
        public string Id { get; }
        public SpellSaveKind Kind { get; }
        public string EffectId { get; }
        public string SubjectId { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public SpellTurnIdentity AttackerTurn { get; }
        public long Damage { get; }
        public int Dc { get; }
        public int Modifier { get; }
        public int First { get; }
        public int Second { get; }
        public int Natural { get; }
        public bool Success { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public SpellSaveRecord(string id, SpellSaveKind kind, string effectId, string subjectId, string causeId,
            long revision, RuleTime at, SpellTurnIdentity attackerTurn, long damage, int dc, int modifier,
            int first, int second, int natural, bool success, uint randomBefore, uint randomAfter, long wordsConsumed)
        {
            if (!Validation.ValidId(id) || !Enum.IsDefined(typeof(SpellSaveKind), kind) || !Validation.ValidId(effectId)
                || !Validation.ValidId(subjectId) || !Validation.ValidId(causeId) || revision < 1 || dc < 0
                || kind == SpellSaveKind.SanctuaryWisdom && (attackerTurn == null || attackerTurn.ActorId != subjectId || damage != 0)
                || kind == SpellSaveKind.ConcentrationConstitution && (attackerTurn != null || damage <= 0 || dc != Math.Max(10, damage / 2))
                || first < 1 || first > 20 || second < 0 || second > 20 || natural < 1 || natural > 20
                || natural != first && natural != second || success != ((long)natural + modifier >= dc) || wordsConsumed < 1)
                throw new ArgumentException("Invalid spell saving throw.");
            Id = id; Kind = kind; EffectId = effectId; SubjectId = subjectId; CauseId = causeId; Revision = revision; At = at;
            AttackerTurn = attackerTurn; Damage = damage; Dc = dc; Modifier = modifier; First = first; Second = second;
            Natural = natural; Success = success; RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
    }

    public enum SanctuaryAttackSource { RegularMelee, RegularUnarmed, RegularRanged, Opportunity, Overwatch, Ready, RegularCreatureFeature }
    public enum SanctuaryAdmissionStatus { Pending, Retargeted, Forgone, Invalidated }
    /// <summary>A suspended real attack request, never a new attack budget or target entitlement.</summary>
    public sealed class SanctuaryAdmissionRecord
    {
        public string Id { get; }
        public string SaveId { get; }
        public string ActorId { get; }
        public string OriginalTargetId { get; }
        public string SourceCommandId { get; }
        public long SourceRevision { get; }
        public string SourceFingerprint { get; }
        public SanctuaryAttackSource Source { get; }
        public string OpportunityId { get; }
        public SanctuaryAdmissionStatus Status { get; }
        public string ResolvedTargetId { get; }
        public string ResolutionCauseId { get; }
        public long ResolvedRevision { get; }
        public bool Pending => Status == SanctuaryAdmissionStatus.Pending;
        public static SanctuaryAdmissionRecord Begin(string id,string saveId,string targetId,Command command,
            SanctuaryAttackSource source,string occurrenceId)
        {
            if(command==null)throw new ArgumentNullException(nameof(command));
            return new SanctuaryAdmissionRecord(id,saveId,command.Actor,targetId,command.Id,checked(command.ExpectedRevision+1),
                command.Fingerprint,source,occurrenceId);
        }
        public SanctuaryAdmissionRecord(string id, string saveId, string actorId, string originalTargetId,
            string sourceCommandId, long sourceRevision, string sourceFingerprint, SanctuaryAttackSource source, string opportunityId,
            SanctuaryAdmissionStatus status = SanctuaryAdmissionStatus.Pending, string resolvedTargetId = "", string resolutionCauseId = "", long resolvedRevision = 0)
        {
            bool reaction = source == SanctuaryAttackSource.Opportunity || source == SanctuaryAttackSource.Overwatch || source == SanctuaryAttackSource.Ready;
            if (!Validation.ValidId(id) || !Validation.ValidId(saveId) || !Validation.ValidId(actorId) || !Validation.ValidId(originalTargetId)
                || !Validation.ValidId(sourceCommandId) || sourceRevision < 1 || string.IsNullOrEmpty(sourceFingerprint) || sourceFingerprint.Length > 512
                || !Enum.IsDefined(typeof(SanctuaryAttackSource), source) || !Enum.IsDefined(typeof(SanctuaryAdmissionStatus), status)
                || opportunityId == null || (reaction ? !Validation.ValidId(opportunityId) : opportunityId != "")
                || resolvedTargetId == null || resolutionCauseId == null
                || status == SanctuaryAdmissionStatus.Pending && (resolvedTargetId != "" || resolutionCauseId != "" || resolvedRevision != 0)
                || status != SanctuaryAdmissionStatus.Pending && (!Validation.ValidId(resolutionCauseId) || resolvedRevision < sourceRevision)
                || status == SanctuaryAdmissionStatus.Retargeted && (!Validation.ValidId(resolvedTargetId) || resolvedTargetId == originalTargetId)
                || status != SanctuaryAdmissionStatus.Retargeted && resolvedTargetId != "")
                throw new ArgumentException("Invalid Sanctuary attack continuation.");
            Id = id; SaveId = saveId; ActorId = actorId; OriginalTargetId = originalTargetId; SourceCommandId = sourceCommandId;
            SourceRevision = sourceRevision; SourceFingerprint = sourceFingerprint; Source = source; OpportunityId = opportunityId;
            Status = status; ResolvedTargetId = resolvedTargetId; ResolutionCauseId = resolutionCauseId; ResolvedRevision = resolvedRevision;
        }
        public SanctuaryAdmissionRecord Finish(SanctuaryAdmissionStatus status, string causeId, long revision, string targetId = "")
        {
            if (!Pending || status == SanctuaryAdmissionStatus.Pending) throw new InvalidOperationException("Attack continuation must finish once.");
            return new SanctuaryAdmissionRecord(Id, SaveId, ActorId, OriginalTargetId, SourceCommandId, SourceRevision,
                SourceFingerprint, Source, OpportunityId, status, targetId, causeId, revision);
        }
    }

    public sealed class DetectMagicFocusRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public string DetectionEffectId { get; }
        public string ObservedEffectId { get; }
        public string ObservationId { get; }
        public SpellTurnIdentity Turn { get; }
        public RuleTime At { get; }
        public bool SchoolWithheld { get; }
        public string BroadSchool { get; }
        public DetectMagicFocusRecord(string commandId, long revision, string actorId, string detectionEffectId, string observedEffectId,
            string observationId, SpellTurnIdentity turn, RuleTime at, bool schoolWithheld, string broadSchool)
        {
            if (!Validation.ValidId(commandId) || revision < 1 || !Validation.ValidId(actorId) || !Validation.ValidId(detectionEffectId)
                || !Validation.ValidId(observedEffectId) || !Validation.ValidId(observationId) || turn == null || turn.IsCarried || turn.ActorId != actorId
                || broadSchool == null || (schoolWithheld ? broadSchool != "" : !Validation.ValidId(broadSchool)))
                throw new ArgumentException("Invalid paid aura focus.");
            CommandId = commandId; Revision = revision; ActorId = actorId; DetectionEffectId = detectionEffectId;
            ObservedEffectId = observedEffectId; ObservationId = observationId; Turn = turn; At = at; SchoolWithheld = schoolWithheld; BroadSchool = broadSchool;
        }
    }
}
