using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Decennium.Foundation
{
    public sealed class FerryWraithContact
    {
        public long ApproachRevision { get; }
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }
        public RuleTime RequestedUntil { get; }
        public string Failure { get; }
        public FerryWraithContact(long approachRevision,long revision,string commandId,RuleTime at,RuleTime requestedUntil,string failure)
        {
            if(approachRevision<1||revision<=approachRevision||!Validation.ValidId(commandId)||requestedUntil<at
                ||failure==null||failure!=""&&!Validation.ValidId(failure))throw new ArgumentException("Invalid Ferry contact.");
            ApproachRevision=approachRevision;Revision=revision;CommandId=commandId;At=at;RequestedUntil=requestedUntil;Failure=failure;
        }
    }

    /// <summary>Historical admission proof; only Snapshot's existing current ledgers are spendable.</summary>
    public sealed class FerryWraithAdmission
    {
        public WorldScheduleRecord Epoch { get; }
        public string PreviousPartyEpochId { get; }
        public long PriorDefenderLocalStart { get; }
        public IReadOnlyList<LaterInitiativeDraw> Draws { get; }
        public IReadOnlyList<ReinforcementCarry> PartyCarried { get; }
        public WorldActivityIntervalRecord CreatureActivity { get; }
        public IReadOnlyList<string> InitialReactionActors { get; }
        public FerryWraithAdmission(WorldScheduleRecord epoch,string previousPartyEpochId,long priorDefenderLocalStart,
            IEnumerable<LaterInitiativeDraw> draws,IEnumerable<ReinforcementCarry> partyCarried,
            WorldActivityIntervalRecord creatureActivity,IEnumerable<string> initialReactionActors)
        {
            var rolls=draws?.ToArray();var carried=partyCarried?.ToArray();var reactions=initialReactionActors?.ToArray();
            if(epoch==null||epoch.Id!=FerryWraithProfile.Calendar||epoch.Order.Count!=3
                ||previousPartyEpochId!=PostRecoveryEncounterDefinition.Calendar||priorDefenderLocalStart<0
                ||rolls==null||rolls.Length!=3||rolls.Any(x=>x==null)
                ||!rolls.Select(x=>x.ActorId).SequenceEqual(FerryWraithProfile.Participants.OrderBy(x=>x,StringComparer.Ordinal))
                ||rolls.Skip(1).Where((x,i)=>rolls[i].RandomAfter!=x.RandomBefore).Any()
                ||!epoch.Order.SequenceEqual(rolls.OrderByDescending(x=>x.Total).ThenBy(x=>FerryWraithProfile.TieOrder(x.ActorId)).Select(x=>x.ActorId))
                ||carried==null||carried.Length!=2||carried.Any(x=>x==null)
                ||!carried.Select(x=>x.Interval.ActorId).OrderBy(x=>x,StringComparer.Ordinal).SequenceEqual(FerryWraithProfile.Party)
                ||creatureActivity==null||creatureActivity.ActorId!=FerryWraithProfile.Actor
                ||reactions==null||reactions.Any(x=>!FerryWraithProfile.IsParticipant(x))
                ||!reactions.SequenceEqual(reactions.Distinct(StringComparer.Ordinal).OrderBy(x=>x,StringComparer.Ordinal)))
                throw new ArgumentException("Invalid Ferry admission provenance.");
            Epoch=epoch;PreviousPartyEpochId=previousPartyEpochId;PriorDefenderLocalStart=priorDefenderLocalStart;
            Draws=Array.AsReadOnly(rolls);PartyCarried=Array.AsReadOnly(carried.OrderBy(x=>x.Interval.ActorId,StringComparer.Ordinal).ToArray());
            CreatureActivity=creatureActivity;InitialReactionActors=Array.AsReadOnly(reactions);
        }
        public FerryWraithAdmission At(long slot)=>slot==Epoch.ProcessedSlot?this:new FerryWraithAdmission(Epoch.At(slot),
            PreviousPartyEpochId,PriorDefenderLocalStart,Draws,PartyCarried,CreatureActivity,InitialReactionActors);
        public WorldIntervalRecord CarriedInterval(string actor)
        {
            if(FerryWraithProfile.IsParty(actor))return PartyCarried.Single(x=>x.Interval.ActorId==actor).Interval;
            if(actor!=FerryWraithProfile.Actor)throw new ArgumentException("Unknown Ferry participant.");
            return new WorldIntervalRecord(actor,-1,CreatureActivity.MovementSpent,CreatureActivity.Action!=WorldActionCommitment.None,
                CreatureActivity.DashPaid,InitialReactionActors.Contains(actor));
        }
    }

    public enum SealActionLedger { Scheduled = 1, OffCalendar = 2 }
    /// <summary>One irreversible physical rupture with its original paid Action and clock basis.</summary>
    public sealed class SealRuptureRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public string ActorId { get; }
        public int ActorX { get; }
        public int ActorY { get; }
        public RuleTime At { get; }
        public SealActionLedger ActionLedger { get; }
        public string ActionCalendarId { get; }
        public long ActionInterval { get; }
        public bool InInitiative { get; }
        public string OriginalEpochId { get; }
        public RuleTime OriginalEpochOrigin { get; }
        public long OriginalCycle { get; }
        public RuleTime ExpiresAt { get; }
        public SealRuptureRecord(string commandId,long revision,string actorId,int actorX,int actorY,RuleTime at,
            SealActionLedger actionLedger,string actionCalendarId,long actionInterval,bool inInitiative,
            string originalEpochId,RuleTime originalEpochOrigin,long originalCycle,RuleTime expiresAt)
        {
            if(!Validation.ValidId(commandId)||revision<1||!Validation.ValidId(actorId)||actorX<0||actorY<0
                ||!Enum.IsDefined(typeof(SealActionLedger),actionLedger)||!Validation.ValidId(actionCalendarId)||actionInterval< -1
                ||originalEpochId==null||expiresAt<=at)
                throw new ArgumentException("Invalid seal rupture provenance.");
            if(inInitiative) {
                if(actionLedger!=SealActionLedger.Scheduled||!Validation.ValidId(originalEpochId)||originalCycle<0
                    ||at<originalEpochOrigin.AddSeconds(checked(originalCycle*6))
                    ||at>=originalEpochOrigin.AddSeconds(checked((originalCycle+1)*6))
                    ||expiresAt!=originalEpochOrigin.AddSeconds(checked((originalCycle+2)*6)))
                    throw new ArgumentException("Invalid original initiative suppression endpoint.");
            } else if(originalEpochId!=""||originalEpochOrigin!=default||originalCycle!= -1||expiresAt!=at.AddSeconds(6))
                throw new ArgumentException("Invalid ordinary-world suppression endpoint.");
            CommandId=commandId;Revision=revision;ActorId=actorId;ActorX=actorX;ActorY=actorY;At=at;ActionLedger=actionLedger;
            ActionCalendarId=actionCalendarId;ActionInterval=actionInterval;InInitiative=inInitiative;OriginalEpochId=originalEpochId;
            OriginalEpochOrigin=originalEpochOrigin;OriginalCycle=originalCycle;ExpiresAt=expiresAt;
        }
    }

    public sealed class FerryWraithRecord
    {
        public const int MaxContacts=32;
        public string PredecessorFingerprint { get; }
        public bool CompanionConsents { get; }
        public bool DirectorAuthorizes { get; }
        public IReadOnlyList<FerryWraithContact> Contacts { get; }
        public FerryWraithAdmission Admission { get; }
        public FerryWraithContact Entered=>Contacts.SingleOrDefault(x=>x.Failure=="");
        public SealRuptureRecord Rupture { get; }
        public long SuppressionExpiredRevision { get; }
        public bool SealDestroyed=>Rupture!=null;
        public bool ClawSuppressed=>Rupture!=null&&SuppressionExpiredRevision==0;
        public FerryWraithRecord(string predecessorFingerprint,bool companionConsents=true,bool directorAuthorizes=true,
            IEnumerable<FerryWraithContact> contacts=null,FerryWraithAdmission admission=null,
            SealRuptureRecord rupture=null,long suppressionExpiredRevision=0)
        {
            var rows=(contacts??Array.Empty<FerryWraithContact>()).ToArray();
            if(!FerryWraithProfile.IsGeometryPredecessor(predecessorFingerprint)||rows.Length>MaxContacts||rows.Any(x=>x==null)
                ||rows.Skip(1).Where((x,i)=>x.ApproachRevision<=rows[i].Revision||x.At<rows[i].At).Any()
                ||rows.Count(x=>x.Failure=="")>1||rows.Any(x=>x.Failure==""&&x!=rows.Last())
                ||(admission!=null)!=rows.Any(x=>x.Failure=="")
                ||admission!=null&&(rows.Last().At!=admission.Epoch.Origin||!companionConsents||!directorAuthorizes)
                ||suppressionExpiredRevision<0||rupture==null&&suppressionExpiredRevision!=0
                ||rupture!=null&&suppressionExpiredRevision!=0&&suppressionExpiredRevision<=rupture.Revision)
                throw new ArgumentException("Invalid Ferry source/encounter/seal history.");
            PredecessorFingerprint=predecessorFingerprint;CompanionConsents=companionConsents;DirectorAuthorizes=directorAuthorizes;
            Contacts=Array.AsReadOnly(rows);Admission=admission;Rupture=rupture;SuppressionExpiredRevision=suppressionExpiredRevision;
        }
        public FerryWraithRecord Append(FerryWraithContact contact,FerryWraithAdmission admission=null)=>new FerryWraithRecord(
            PredecessorFingerprint,CompanionConsents,DirectorAuthorizes,Contacts.Append(contact),admission??Admission,Rupture,SuppressionExpiredRevision);
        public FerryWraithRecord At(long slot)=>new FerryWraithRecord(PredecessorFingerprint,CompanionConsents,DirectorAuthorizes,
            Contacts,Admission.At(slot),Rupture,SuppressionExpiredRevision);
        public FerryWraithRecord Tear(SealRuptureRecord rupture)
        {
            if(Rupture!=null||rupture==null)throw new InvalidOperationException("The exposed paper can be torn only once.");
            return new FerryWraithRecord(PredecessorFingerprint,CompanionConsents,DirectorAuthorizes,Contacts,Admission,rupture);
        }
        public FerryWraithRecord Expire(long revision)
        {
            if(!ClawSuppressed||revision<=Rupture.Revision)throw new InvalidOperationException("Only an active suppression can expire once.");
            return new FerryWraithRecord(PredecessorFingerprint,CompanionConsents,DirectorAuthorizes,Contacts,Admission,Rupture,revision);
        }
    }

    public static partial class FerryWraithProfile
    {
        public const string Actor="TEST_ONLY.ferry-wraith",Feature="TEST_ONLY.ferry-wraith.hellfire-claw";
        public const string Post="TEST_ONLY.ferry-post",Seal="TEST_ONLY.ferry-seal";
        public const string Calendar="TEST_ONLY.ferry-calendar",Encounter="TEST_ONLY.ferry-encounter";
        public const string Hero="TEST_ONLY.actor",Companion="TEST_ONLY.companion";
        public const string FingerprintPrefix="TEST_ONLY.ferry-wraith-v1-";
        public const string Approval="1ffe0cc9-bc09-5957-95a3-9249973de253";
        public const string SourceId="ferry-wraith-of-the-hush",SourceRevision="46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string SourcePath="docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/Monster_Manual_of_the_Known_Descent_Source/entries/ferry-wraith-of-the-hush.md";
        public const string SourceSha256="393a659464c3cbc49c349df5376fb44eeea8d169984e0f3933fc2a125db52895";
        public const string PoisonedImmunity="TEST_ONLY.ferry-wraith.Poisoned-immunity",PoisonedImmunityGrant="TEST_ONLY.ferry-wraith.source-immunity-grant";
        public const byte Marker=19;
        public static IReadOnlyList<string> Party { get; }=Array.AsReadOnly(new[]{Hero,Companion});
        public static IReadOnlyList<string> Participants { get; }=Array.AsReadOnly(new[]{Hero,Companion,Actor});
        public static CreatureActorRecord CreateCreature()=>new CreatureActorRecord(Actor,SourceId,SourceRevision,SourcePath,SourceSha256,
            new[]{12,14,14,9,11,16},10,9,40,true,new[]{"Undead"},LivingRecipientQualification.NotLiving,
            new[]{"necrotic"},new[]{"poison"},new[]{"Poisoned"});
        public static bool IsParty(string actor)=>actor==Hero||actor==Companion;
        public static bool IsParticipant(string actor)=>IsParty(actor)||actor==Actor;
        public static int TieOrder(string actor)=>actor==Hero?0:actor==Companion?1:2;
        public static bool MatchesApproach(WorldTraversalRecord edge)=>edge!=null&&edge.ActorId==Hero&&!edge.Running
            &&edge.FromX==8&&edge.FromY==1&&edge.ToX==8&&edge.ToY==2;
        public static bool SelectedFingerprint(string value)=>value!=null&&(value.StartsWith(FingerprintPrefix,StringComparison.Ordinal)||ConsecrationProfile.SelectedFingerprint(value));
        public static bool Active(Snapshot state)=>state.FerryWraith?.Admission!=null&&state.Encounter?.Id==Encounter;
        public static bool OwnsCurrent(Snapshot state,string actor)=>state.FerryWraith?.Admission!=null&&IsParticipant(actor);
        public static bool IsEpoch(Snapshot state,string epoch)=>epoch!=null&&state.FerryWraith?.Admission?.Epoch.Id==epoch;
        public static bool IsGeometryPredecessor(string value)=>value!=null&&value.StartsWith(DeclaredGeometryProfile.FingerprintPrefix,StringComparison.Ordinal)
            &&CreatureActorRecord.Hex(value.Substring(DeclaredGeometryProfile.FingerprintPrefix.Length),64);
        public static string BindFingerprint(string predecessor,bool companionConsents,bool directorAuthorizes)
        {
            if(!IsGeometryPredecessor(predecessor))throw new ArgumentException("Ferry requires its qualified geometry predecessor.");
            string binding=string.Join("|",predecessor,Approval,SourceRevision,SourcePath,SourceSha256,
                companionConsents?"consent":"no-consent",directorAuthorizes?"mandate":"no-mandate",
                "source-origin|no-PB|ordinary-monster|not-living-recipient|AC10-HP9-Speed40|12,14,14,9,11,16",
                "necrotic-half-poison-zero-Poisoned-prevention|claw-action-melee5-plus3-d4fire-crit2d4|no-fallback",
                "Petrified-poison-zero|condition-policy-origin-prefix-application-evaluation-marker-provenance",
                "bright-ordinary-sight30|actor10,2|post-seal9,3-nonblocking|paid8,1-to8,2-companion8,3",
                "current-recovery-defender-start|settled-party-ends|carry-owned-ledgers|hero-companion-creature-ties",
                "paid-exposed-paper-once|original-next-round-or-world-six-seconds|no-extra-action-or-clock",
                "Guarded-known-source-controller|seven-owned-spells|dead-only-closure|no-reward");
            using(var sha=SHA256.Create())return FingerprintPrefix+string.Concat(sha.ComputeHash(Encoding.UTF8.GetBytes(binding))
                .Select(x=>x.ToString("x2",CultureInfo.InvariantCulture)));
        }
        internal static void Validate(Snapshot state)
        {
            if((state.FerryWraith!=null)!=SelectedFingerprint(state.ContentFingerprint))throw new ArgumentException("Ferry envelope mismatch.");
            if(state.FerryWraith==null) {
                if(state.Creatures.Length!=0)throw new ArgumentException("Creature origins require their trusted selected profile.");
                return;
            }
            var record=state.FerryWraith;
            if(!state.TestOnly||state.SchemaVersion!=Snapshot.SurpriseEntrySchema||state.DeclaredGeometry==null||state.BishopEntry==null
                ||record.PredecessorFingerprint!=DeclaredGeometryProfile.BindFingerprint(state.DeclaredGeometry.PredecessorFingerprint)
                ||(state.Consecration?.PredecessorFingerprint??state.ContentFingerprint)!=BindFingerprint(record.PredecessorFingerprint,record.CompanionConsents,record.DirectorAuthorizes)
                ||state.Creatures.Length!=1||!CreateCreature().SameAs(state.Creatures[0])
                ||record.Contacts.Any(x=>x.Revision>state.Revision||x.At>state.RuleClock)
                ||record.Rupture!=null&&(record.Rupture.Revision>state.Revision||record.Rupture.At>state.RuleClock)
                ||record.SuppressionExpiredRevision>state.Revision
                ||record.SuppressionExpiredRevision>0&&record.Rupture.ExpiresAt>state.RuleClock)
                throw new ArgumentException("Invalid trusted Ferry source composition.");
            var life=state.Lives.Single(x=>x.ActorId==Actor);
            if(life.MaximumHp!=9||life.UsesDeathSaves||life.HeldItems.Count!=0||state.Characters.Any(x=>x.ActorId==Actor))
                throw new ArgumentException("Invalid non-class Ferry life origin.");
            var journal=state.Conditions.Single(x=>x.Target==Actor);
            var grants=journal.Operations.Where(x=>x.Kind==ConditionOperationKind.GrantImmunity).ToArray();
            if(grants.Length!=1||grants[0].Id!=PoisonedImmunityGrant||!grants[0].At.Equals(journal.Origin)
                ||grants[0].Immunity.Id!=PoisonedImmunity||grants[0].Immunity.Owner!=Actor||grants[0].Immunity.Source!=SourceId
                ||!grants[0].Immunity.Kinds.SequenceEqual(new[]{"Poisoned"})||grants[0].Immunity.Expires!=null
                ||grants[0].Immunity.EndingMethod!="source-profile-only"
                ||journal.Operations.Any(x=>x.Kind==ConditionOperationKind.EndImmunity))
                throw new ArgumentException("Ferry named immunity requires its immutable genesis source.");
            ValidateAdmission(state);
            ValidateSeal(state);
        }
        public static bool SealPayloadValid(Command c)
            =>c!=null&&c.Kind==CommandKind.TearExposedSeal&&c.Target==Seal&&c.X==0&&c.Y==0
                &&c.Inventory==null&&c.Combat==null&&c.Advancement==null&&c.Ranged==null&&c.OverwatchRider==OverwatchRider.None
                &&c.SuppressionFire==null&&c.DefensiveFormation==null&&c.ExpeditionAssignment==null&&c.HarvestSelection==null
                &&c.MiningSelection==null&&c.ProspectingExposure==null&&c.RouteMappingWork==null&&c.IntimidatingPresence==null
                &&c.HealingRite==null&&c.SpellCast==null&&c.Guidance==null&&c.SanctuaryResponse==null&&c.DivineInvocation==null;

        public static bool DashPayloadValid(Command c)
            =>c!=null&&c.Kind==CommandKind.EncounterDash&&c.X==0&&c.Y==0
                &&c.Inventory==null&&c.Combat==null&&c.Advancement==null&&c.Ranged==null&&c.OverwatchRider==OverwatchRider.None
                &&c.SuppressionFire==null&&c.DefensiveFormation==null&&c.ExpeditionAssignment==null&&c.HarvestSelection==null
                &&c.MiningSelection==null&&c.ProspectingExposure==null&&c.RouteMappingWork==null&&c.IntimidatingPresence==null
                &&c.HealingRite==null&&c.SpellCast==null&&c.Guidance==null&&c.SanctuaryResponse==null&&c.DivineInvocation==null;

        private static void ValidateSeal(Snapshot s)
        {
            var seal=s.FerryWraith.Rupture;if(seal==null)return;
            var command=ContactReceipt(s,seal.Revision);
            if(!SealPayloadValid(command)||command.Actor!=seal.ActorId||command.Id!=seal.CommandId
                ||!s.Characters.Any(x=>x.ActorId==seal.ActorId)
                ||Math.Max(Math.Abs((long)seal.ActorX-9),Math.Abs((long)seal.ActorY-3))>1
                ||!DeclaredGeometryProfile.SupportsAnchorAt(s,seal.ActorX,seal.ActorY)
                ||s.FerryWraith.ClawSuppressed&&s.RuleClock>=seal.ExpiresAt)
                throw new ArgumentException("Invalid physical seal rupture history.");
            var calendar=WorldTiming.FindEpoch(s,seal.ActionCalendarId);
            if(calendar==null)throw new ArgumentException("Seal Action calendar unavailable.");
            if(seal.ActionLedger==SealActionLedger.OffCalendar) {
                if(seal.ActionCalendarId!=s.WorldSchedule.Id
                    ||seal.ActionInterval!=WorldActivityIntervalRecord.IndexAt(s.WorldSchedule,seal.At))
                    throw new ArgumentException("Seal Action activity interval mismatch.");
            } else if(!calendar.Order.Contains(seal.ActorId))throw new ArgumentException("Seal Action owner absent from calendar.");
            if(seal.InInitiative) {
                var original=WorldTiming.FindEpoch(s,seal.OriginalEpochId);
                if(original==null||original.Id!=seal.ActionCalendarId||original.Origin!=seal.OriginalEpochOrigin)
                    throw new ArgumentException("Seal original initiative basis unavailable.");
            }
        }
        private static void ValidateAdmission(Snapshot s)
        {
            var record=s.FerryWraith;
            foreach(var contact in record.Contacts) {
                var approach=ContactReceipt(s,contact.ApproachRevision);var arrival=ContactReceipt(s,contact.Revision);
                if(approach.Kind!=CommandKind.BeginWorldStep||approach.Actor!=Hero||approach.Target!="walk"||approach.X!=0||approach.Y!=1
                    ||arrival.Kind!=CommandKind.AdvanceClock||arrival.Id!=contact.CommandId)
                    throw new ArgumentException("Invalid Ferry paid-contact provenance.");
            }
            var admission=record.Admission;var closed=s.ClosedEncounters.SingleOrDefault(x=>x.Encounter.Id==Encounter);
            if(admission==null) {
                if(closed!=null||s.Encounter?.Id==Encounter||s.WorldIntervals.Any(x=>x.ActorId==Actor)
                    ||s.WorldActivityIntervals.Count(x=>x.ActorId==Actor)!=1)
                    throw new ArgumentException("Premature Ferry encounter or allowance.");
                return;
            }
            var entry=record.Entered;var epoch=admission.Epoch;var prior=s.PostRecoveryEncounter?.Admission?.Epoch;
            if(prior==null||admission.PreviousPartyEpochId!=prior.Id||epoch.Origin!=entry.At
                ||prior.Start(admission.PriorDefenderLocalStart)!=entry.At
                ||prior.LatestStart(PostRecoveryEncounterDefinition.Actor,admission.PriorDefenderLocalStart)!=admission.PriorDefenderLocalStart
                ||epoch.ProcessedSlot!=epoch.SlotAt(s.RuleClock)||s.WorldActivityIntervals.Any(x=>x.ActorId==Actor)
                ||!s.ClosedEncounters.Any(x=>x.Encounter.Id==PostRecoveryEncounterDefinition.Encounter&&x.ClosedRevision<entry.Revision)
                ||!s.Lives.Single(x=>x.ActorId==PostRecoveryEncounterDefinition.Actor).Dead)
                throw new ArgumentException("Ferry admission lacks settled prior closure and exact recovery Start.");
            var activity=admission.CreatureActivity;long index=WorldActivityIntervalRecord.IndexAt(s.WorldSchedule,entry.At);
            if(activity.CalendarId!=s.WorldSchedule.Id||activity.IntervalIndex!=index
                &&(activity.IntervalIndex!=index-1||WorldActivityIntervalRecord.EndAt(s.WorldSchedule,activity.IntervalIndex)!=entry.At))
                throw new ArgumentException("Ferry admission lacks the actual creature activity interval.");
            foreach(var carry in admission.PartyCarried) {
                long local=prior.LatestStart(carry.Interval.ActorId,admission.PriorDefenderLocalStart);
                if(local<0||prior.Start(local+1)>entry.At||carry.Interval.LastStart!=WorldTiming.TurnOrdinal(s,prior.Id,local)
                    ||admission.InitialReactionActors.Contains(carry.Interval.ActorId)&&!carry.Interval.ReactionAvailable)
                    throw new ArgumentException("Ferry admission invented or refunded a carried party allowance.");
                if(carry.Interval.ActorId==ClericRpProfile.Actor
                    &&s.CastingActivities.Any(x=>x.Turn.EpochId==prior.Id&&x.Turn.LocalStart==local)
                    &&s.OrdinaryMagic==null&&!s.CastingTurnEnds.Any(x=>x.Turn.EpochId==prior.Id&&x.Turn.LocalStart==local
                        &&x.At==prior.Start(local+1)&&x.Revision<=entry.Revision))
                    throw new ArgumentException("Ferry admission bypassed an eligible old casting End.");
            }
            foreach(var draw in admission.Draws) {
                var die=DiceStream.Draw(draw.RandomBefore,20);
                if(draw.Natural!=die.Value+1||draw.RandomAfter!=die.NextState||draw.WordsConsumed!=die.WordsConsumed)
                    throw new ArgumentException("Ferry initiative differs from its actual RNG words.");
            }
            var encounter=Active(s)?s.Encounter:closed?.Encounter;
            if(encounter==null||encounter.Id!=Encounter||encounter.Origin!=epoch.Origin||encounter.RosterPhase!=null||encounter.InheritedPhase!=null
                ||!encounter.InitialOrder.SequenceEqual(epoch.Order)||encounter.StartRevisions[0]!=entry.Revision||encounter.ObservedOrdinals[0]!=0
                ||Active(s)&&(closed!=null||!s.InventoryCombat||encounter.TurnOrdinal!=epoch.ProcessedSlot)
                ||!Active(s)&&(s.InventoryCombat||s.Encounter!=null||closed==null))
                throw new ArgumentException("Invalid independent Ferry encounter history.");
            if(closed!=null) {
                var cause=ContactReceipt(s,closed.ClosedRevision);
                if(!s.Lives.Single(x=>x.ActorId==Actor).Dead||cause.Kind!=CommandKind.EndFixedEncounter||cause.Id!=closed.Reason
                    ||cause.Actor!=encounter.CurrentActor||cause.Target!=encounter.CurrentTurnId
                    ||closed.ClosedAt!=epoch.Start(encounter.TurnOrdinal+1)||closed.ClosedAt>s.RuleClock)
                    throw new ArgumentException("Invalid Ferry death and outgoing-End closure.");
            }
        }
        private static Command ContactReceipt(Snapshot s,long revision)
        {
            var row=s.Receipts.SingleOrDefault(x=>x.Revision==revision);
            return row==null?throw new ArgumentException("Missing Ferry command receipt."):CommandHistory.Read(row);
        }
    }
}
