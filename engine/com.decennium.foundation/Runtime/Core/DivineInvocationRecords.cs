using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Recipient choices only. Payment, source, healing and cadence are derived by the host.</summary>
    public sealed class DivineInvocationRequest
    {
        public ReadOnlyCollection<string> TargetIds { get; }
        public string CureTargetId { get; }
        public RadianceCurePreference CurePreference { get; }
        internal string Fingerprint => string.Join(",",TargetIds)+"|"+CureTargetId+"|"
            +((int)CurePreference).ToString(System.Globalization.CultureInfo.InvariantCulture);
        public DivineInvocationRequest(IEnumerable<string> targets,string cureTargetId="",RadianceCurePreference curePreference=RadianceCurePreference.None)
        {
            var ids=targets?.Take(4).ToArray();
            if(ids==null || ids.Length<1 || ids.Length>3 || ids.Any(x=>!Validation.ValidId(x))
                || ids.Distinct(StringComparer.Ordinal).Count()!=ids.Length || cureTargetId==null
                || !Enum.IsDefined(typeof(RadianceCurePreference),curePreference)
                || (curePreference==RadianceCurePreference.None?cureTargetId!="":!ids.Contains(cureTargetId)))
                throw new ArgumentException("Invocation requires one to three distinct recipients and at most one selected cure recipient.");
            TargetIds=Array.AsReadOnly(ids.OrderBy(x=>x,StringComparer.Ordinal).ToArray());
            CureTargetId=cureTargetId;CurePreference=curePreference;
        }
    }
    public sealed class InvocationHealingRecord
    {
        public string TargetId { get; }
        public long HpBefore { get; }
        public long Potential { get; }
        public long HpAfter { get; }
        public long ActualGain => HpAfter-HpBefore;
        public InvocationHealingRecord(string target,long before,long potential,long after)
        {
            if(!Validation.ValidId(target)||before<0||potential<0||after<before||after-before>potential)
                throw new ArgumentException("Invalid Invocation healing settlement.");
            TargetId=target;HpBefore=before;Potential=potential;HpAfter=after;
        }
    }
    public sealed class DivineInvocationRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public SpellTurnIdentity Turn { get; }
        public RuleTime At { get; }
        public string ActorId => Turn.ActorId;
        public string SourceId => BishopProfile.Invocation;
        public string SourceRevision => ClericRpProfile.SourceRevision;
        public DivineInvocationRequest Choice { get; }
        public int RpBefore { get; }
        public int RpPaid => 3;
        public int RpAfter => RpBefore-RpPaid;
        public int ConvictionBefore { get; }
        public int ConvictionPaid => 2;
        public int ConvictionAfter => ConvictionBefore-ConvictionPaid;
        public int DissonanceBefore { get; }
        public int DissonanceAfter => Math.Max(0,DissonanceBefore-1);
        public int ActualVent => DissonanceBefore-DissonanceAfter;
        public int Die { get; }
        public int Modifier => 2;
        public long RequestedHealing => Die+Modifier;
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public ReadOnlyCollection<InvocationHealingRecord> Recipients { get; }
        public ConditionStamp CureAt { get; }
        public string CureOperationId { get; }
        public ReadOnlyCollection<string> EndedApplicationIds { get; }
        public DivineInvocationRecord(string command,long revision,SpellTurnIdentity turn,RuleTime at,DivineInvocationRequest choice,
            int rpBefore,int convictionBefore,int dissonanceBefore,int die,uint randomBefore,uint randomAfter,long words,
            IEnumerable<InvocationHealingRecord> recipients,ConditionStamp cureAt,string cureOperation="",IEnumerable<string> ended=null)
        {
            var rows=recipients?.ToArray();var applications=(ended??Array.Empty<string>()).ToArray();
            if(!Validation.ValidId(command)||revision<1||turn==null||turn.IsCarried||choice==null
                ||rpBefore<3||rpBefore>7||convictionBefore<2||convictionBefore>5||dissonanceBefore<0||die<1||die>8||words<1
                ||rows==null||rows.Any(x=>x==null||x.Potential>die+2)||!rows.Select(x=>x.TargetId).SequenceEqual(choice.TargetIds)
                ||cureAt.Time!=at||cureOperation==null||applications.Length>128
                ||applications.Any(x=>!Validation.ValidId(x))||applications.Distinct(StringComparer.Ordinal).Count()!=applications.Length
                ||!applications.SequenceEqual(applications.OrderBy(x=>x,StringComparer.Ordinal))
                ||(applications.Length==0?cureOperation!="":choice.CurePreference==RadianceCurePreference.None||cureOperation!=command+".invocation.cure"))
                throw new ArgumentException("Invalid paid Divine Invocation history.");
            CommandId=command;Revision=revision;Turn=turn;At=at;Choice=choice;RpBefore=rpBefore;
            ConvictionBefore=convictionBefore;DissonanceBefore=dissonanceBefore;Die=die;RandomBefore=randomBefore;
            RandomAfter=randomAfter;WordsConsumed=words;Recipients=Array.AsReadOnly(rows);CureAt=cureAt;
            CureOperationId=cureOperation;EndedApplicationIds=Array.AsReadOnly(applications);
        }
        public DivineInvocationRecord WithCure(string operation,IEnumerable<string> ended)
            =>new DivineInvocationRecord(CommandId,Revision,Turn,At,Choice,RpBefore,ConvictionBefore,DissonanceBefore,Die,
                RandomBefore,RandomAfter,WordsConsumed,Recipients,CureAt,operation,ended);
    }
    public static partial class BishopProfile
    {
        public static IEnumerable<DivineInvocationRecord> Invocations(Snapshot s)
            =>s.BishopEntry?.Invocations??(IEnumerable<DivineInvocationRecord>)Array.Empty<DivineInvocationRecord>();
        public static string InvocationPayloadFailure(Snapshot s,Command c)
        {
            if(c.DivineInvocation==null)return c.Kind==CommandKind.UseDivineInvocation?"InvocationSelectionRequired":null;
            if(s.BishopEntry==null||c.Kind!=CommandKind.UseDivineInvocation)return "InvocationUnsupported";
            return c.Target!=""||c.X!=0||c.Y!=0||c.Inventory!=null||c.Combat!=null||c.Advancement!=null||c.Ranged!=null
                ||c.OverwatchRider!=OverwatchRider.None||c.SuppressionFire!=null||c.DefensiveFormation!=null||c.ExpeditionAssignment!=null
                ||c.HarvestSelection!=null||c.MiningSelection!=null||c.ProspectingExposure!=null||c.RouteMappingWork!=null
                ||c.IntimidatingPresence!=null||c.HealingRite!=null||c.SpellCast!=null||c.Guidance!=null||c.SanctuaryResponse!=null
                ?"UnexpectedInvocationPayload":null;
        }
        public static bool QualifiesInvocationCure(Snapshot s,string target,ConditionOperation operation)
            =>operation.Kind==ConditionOperationKind.Cure&&Invocations(s).Any(x=>x.Choice.CureTargetId==target
                &&x.CureOperationId==operation.Id&&x.CureAt.Equals(operation.At)&&operation.Subject==x.Choice.CurePreference.ToString()
                &&x.EndedApplicationIds.Count!=0);
        public static bool InvocationCuredBefore(Snapshot s,FrightenedTimingRecord timing,ConditionStamp deadline)
            =>Invocations(s).Any(x=>x.Choice.CureTargetId==timing.TargetId&&x.Choice.CurePreference==RadianceCurePreference.Frightened
                &&x.CureAt.CompareTo(deadline)<0&&x.EndedApplicationIds.Contains(timing.ApplicationId)
                &&s.Conditions.Single(j=>j.Target==timing.TargetId).Operations.Any(o=>o.Id==x.CureOperationId&&QualifiesInvocationCure(s,timing.TargetId,o)));
        internal static void ValidateInvocations(Snapshot s)
        {
            var uses=Invocations(s).ToArray();
            if(uses.Length>128||uses.Any(x=>x==null)||uses.Select(x=>x.CommandId).Distinct().Count()!=uses.Length
                ||uses.Select(x=>x.Turn.Binding).Distinct().Count()!=uses.Length
                ||!uses.Select(x=>x.Revision).SequenceEqual(uses.Select(x=>x.Revision).OrderBy(x=>x)))
                throw new ArgumentException("Duplicate or unordered Invocation history.");
            foreach(var use in uses) {
                var receipt=s.Receipts.SingleOrDefault(x=>x.Id==use.CommandId&&x.Revision==use.Revision);
                var command=receipt==null?null:CommandHistory.Read(receipt);
                var draw=DiceStream.Draw(use.RandomBefore,8);
                var activity=s.CastingActivities.SingleOrDefault(x=>x.CommandId==use.CommandId);
                if(!Earned(s)||use.ActorId!=ClericRpProfile.Actor||use.Revision<=Advancement(s).Revision||use.Revision>s.Revision
                    ||use.At>s.RuleClock||command?.Kind!=CommandKind.UseDivineInvocation||command.Actor!=use.ActorId
                    ||command.DivineInvocation?.Fingerprint!=use.Choice.Fingerprint||!SpellCastingProfile.ValidTurn(s,use.Turn,use.At,true)
                    ||use.RpBefore!=ClericLongRestProfile.RpBefore(s,use.Revision)
                    ||use.ConvictionBefore!=ClericLongRestProfile.ConvictionBefore(s,use.Revision)
                    ||draw.Value+1!=use.Die||draw.NextState!=use.RandomAfter||draw.WordsConsumed!=use.WordsConsumed
                    ||activity==null||activity.Kind!=CastingActivityKind.MagicalClassAbility||activity.Revision!=use.Revision
                    ||activity.At!=use.At||!activity.Turn.SameAs(use.Turn))throw new ArgumentException("Unattributed paid Invocation.");
                if(use.EndedApplicationIds.Count!=0) {
                    var journal=s.Conditions.Single(x=>x.Target==use.Choice.CureTargetId);
                    var operation=journal.Operations.SingleOrDefault(x=>x.Id==use.CureOperationId);
                    if(operation==null||!QualifiesInvocationCure(s,journal.Target,operation)
                        ||use.EndedApplicationIds.Any(id=>!journal.Operations.Any(x=>x.Kind==ConditionOperationKind.Apply
                            &&x.Application.Id==id&&x.Application.Kind==use.Choice.CurePreference.ToString()&&x.Application.GenericCureAllowed
                            &&x.At.CompareTo(use.CureAt)<=0&&(!x.Application.Expires.HasValue||x.Application.Expires.Value.CompareTo(use.CureAt)>0))))
                        throw new ArgumentException("Unattributed Invocation cure.");
                }
            }
            if(s.Receipts.Count(x=>CommandHistory.Read(x).Kind==CommandKind.UseDivineInvocation)!=uses.Length)
                throw new ArgumentException("Invocation receipt coverage differs.");
            var recharges=s.AbilityRecharges.Where(x=>x.AbilityId==Invocation).ToArray();
            if(recharges.Length!=(uses.Length==0?0:1))throw new ArgumentException("Missing Invocation recharge.");
            foreach(var recharge in recharges) {
                var epoch=WorldTiming.FindEpoch(s,recharge.EpochId);var last=uses.Last();
                if(recharge.ActorId!=ClericRpProfile.Actor||epoch==null||recharge.Remaining>3
                    ||epoch.LatestStart(recharge.ActorId,recharge.LastLocalStart)!=recharge.LastLocalStart
                    ||epoch.Start(recharge.LastLocalStart)!=recharge.LastStartAt||recharge.LastStartAt>s.RuleClock
                    ||recharge.LastStartAt<WorldTiming.FindEpoch(s,last.Turn.EpochId).Start(last.Turn.LocalStart)
                    ||recharge.EpochId==last.Turn.EpochId&&recharge.Remaining!=Math.Max(0L,3L-(recharge.LastLocalStart-last.Turn.LocalStart)/epoch.Order.Count))
                    throw new ArgumentException("Invalid Invocation recharge cursor.");
                // Cross-epoch Start count and all historical geometry/life facts are independently reconstructed by strict replay.
            }
        }
    }
}
