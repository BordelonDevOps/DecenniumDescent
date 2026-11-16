#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation.Laboratory
{
    public sealed partial class TestOnlySharedWorldPolicy
    {
        internal static SanctuaryAdmissionRecord PendingSanctuary(Snapshot s)=>s.ConnectedClericCasting
            ?s.SanctuaryAdmissions.SingleOrDefault(x=>x.Pending):null;

        private static bool SanctuaryAttackCommand(Command c)=>c.Kind==CommandKind.AttackClub || c.Kind==CommandKind.AttackUnarmed
            || c.Kind==CommandKind.RespondOpportunityAttack&&c.Combat?.Choice==true;

        private static string SanctuaryAttackTarget(Snapshot s,Command c)=>c.Kind==CommandKind.RespondOpportunityAttack
            ?TestOnlyClubAttackPolicy.PendingMove(s)?.ActorId:c.Target;

        private static SpellEffectRecord SanctuaryOn(Snapshot s,string target)=>s.ConnectedClericCasting
            ?s.SpellEffects.SingleOrDefault(x=>x.Present&&x.SpellId=="sanctuary"&&x.TargetId==target&&x.ExpiresAt>s.RuleClock):null;

        internal static bool SanctuaryTargetProhibited(Snapshot s,string actor,string target)
        {
            var ward=SanctuaryOn(s,target);if(ward==null)return false;
            var turn=CurrentCastingTurn(s,actor);if(turn==null)return false;
            return s.SpellSaves.Any(x=>x.Kind==SpellSaveKind.SanctuaryWisdom&&x.EffectId==ward.Id
                &&x.SubjectId==actor&&x.AttackerTurn.SameAs(turn)&&!x.Success);
        }

        // The probe follows the existing source's pure attack preflight. It never resolves
        // a future WIS save to decide whether an attack request can be submitted.
        private string AssessSanctuaryGate(Snapshot s,Command c,out SpellEffectRecord ward,out SpellTurnIdentity turn)
        {
            ward=SanctuaryOn(s,SanctuaryAttackTarget(s,c));turn=null;
            if(ward==null)return null;
            string failure=ResolveCore(s.Copy(),c,assessTactical:true,sanctuaryChecked:true);
            if(failure!=null)return failure;
            turn=CurrentCastingTurn(s,c.Actor);if(turn==null)return "SanctuaryAttackerCalendarUnsupported";
            string wardId=ward.Id;var attackerTurn=turn;
            var prior=s.SpellSaves.SingleOrDefault(x=>x.Kind==SpellSaveKind.SanctuaryWisdom&&x.EffectId==wardId
                &&x.SubjectId==c.Actor&&x.AttackerTurn.SameAs(attackerTurn));
            if(prior!=null)return prior.Success?null:"SanctuaryTargetProhibitedThisInterval";
            if(SpellDamageCapacityFailure(s,ward.TargetId,otherPossibleSaves:1)!=null
                || s.SanctuaryAdmissions.Length>=SpellCastingProfile.MaxAdmissions)
                return "CastingHistoryFull";
            return null;
        }

        private string BeginSanctuaryGate(Snapshot s,Command c,out bool suspended,bool assessOnly)
        {
            suspended=false;
            string failure=AssessSanctuaryGate(s,c,out var ward,out var turn);
            if(failure!=null || ward==null || assessOnly)return failure;
            if(s.SpellSaves.Any(x=>x.Kind==SpellSaveKind.SanctuaryWisdom&&x.EffectId==ward.Id
                &&x.SubjectId==c.Actor&&x.AttackerTurn.SameAs(turn)))return null;
            var cast=s.SpellCasts.Single(x=>x.CommandId==ward.CastId);
            int modifier=checked(CharacterRuleFacts.ForActor(s,c.Actor).AbilityModifier(CharacterAbility.Wisdom)
                +CharacterAdvancementRules.SaveProficiencyBonus(s,c.Actor,"WIS")+ExpeditionStrainRules.Current(s,c.Actor).SavingThrowModifier);
            int basis=modifier;var aura=AuraOfFaithRules.Qualify(s,c.Actor);modifier=AuraOfFaithRules.Modifier(aura,basis);
            uint before=s.RandomState;var roll=PlaytestDice.RollD20(before);
            string saveId="spell.save."+(s.Revision+1).ToString(CultureInfo.InvariantCulture)+"."+s.SpellSaves.Length.ToString(CultureInfo.InvariantCulture);
            var save=new SpellSaveRecord(saveId,SpellSaveKind.SanctuaryWisdom,ward.Id,c.Actor,c.Id,s.Revision+1,s.RuleClock,turn,0,
                cast.SpellDc,modifier,roll.First,roll.Second??0,roll.Natural,(long)roll.Natural+modifier>=cast.SpellDc,
                before,roll.NextRandomState,roll.WordsConsumed);
            AuraOfFaithRules.RecordSave(s,aura,AuraSaveConsumer.Sanctuary,saveId,basis,cast.SpellDc,roll.Natural,false,save.Success,before,roll.NextRandomState,roll.WordsConsumed);
            s.SpellSaves=s.SpellSaves.Append(save).ToArray();s.RandomState=roll.NextRandomState;
            if(save.Success)return null;
            bool reaction=c.Kind==CommandKind.RespondOpportunityAttack;
            var source=reaction?SanctuaryAttackSource.Opportunity:c.Kind==CommandKind.AttackUnarmed
                ?SanctuaryAttackSource.RegularUnarmed:SanctuaryAttackSource.RegularMelee;
            s.SanctuaryAdmissions=s.SanctuaryAdmissions.Append(SanctuaryAdmissionRecord.Begin(
                "sanctuary."+(s.Revision+1).ToString(CultureInfo.InvariantCulture),save.Id,ward.TargetId,c,
                source,reaction?c.Target:"")).ToArray();
            suspended=true;return null;
        }

        private static void FinishSanctuary(Snapshot s,SanctuaryAdmissionRecord pending,Command response)
        {
            bool retarget=response.SanctuaryResponse.Kind==SanctuaryResponseKind.Retarget;
            s.SanctuaryAdmissions=s.SanctuaryAdmissions.Select(x=>x.Id==pending.Id
                ?x.Finish(retarget?SanctuaryAdmissionStatus.Retargeted:SanctuaryAdmissionStatus.Forgone,response.Id,s.Revision+1,
                    retarget?response.SanctuaryResponse.TargetId:""):x).ToArray();
        }

        private string AssessSanctuaryResponse(Snapshot s,Command c,out Command continuation)
        {
            continuation=null;var pending=PendingSanctuary(s);
            if(pending==null)return "NoPendingSanctuaryAdmission";
            if(c.Kind!=CommandKind.RespondSanctuary)return "SanctuaryChoicePending";
            if(c.Actor!=pending.ActorId)return "WrongSanctuaryController";
            if(c.Target!=pending.Id || c.SanctuaryResponse==null || c.X!=0 || c.Y!=0 || c.Inventory!=null || c.Combat!=null
                ||c.Ranged!=null || c.Advancement!=null || c.SpellCast!=null || c.Guidance!=null)return "InvalidSanctuaryResponse";
            var source=CommandHistory.Read(s.Receipts.Single(x=>x.Id==pending.SourceCommandId&&x.Revision==pending.SourceRevision));
            bool retarget=c.SanctuaryResponse.Kind==SanctuaryResponseKind.Retarget;
            if(retarget) {
                // The sole target of this actual opportunity occurrence is its provoker.
                // Its failed ward gate cannot grant a different reaction target or an Action.
                if(pending.Source==SanctuaryAttackSource.Opportunity)return "SanctuaryRetargetOutsideOriginalSource";
                if(pending.Source!=SanctuaryAttackSource.RegularMelee&&pending.Source!=SanctuaryAttackSource.RegularUnarmed)
                    return "SanctuaryAttackSourceUnsupported";
                if(c.SanctuaryResponse.TargetId==pending.OriginalTargetId)return "SanctuaryTargetProhibitedThisInterval";
                continuation=new Command(c.Id,c.Actor,s.Revision,source.Kind,c.SanctuaryResponse.TargetId,combat:source.Combat);
            } else if(pending.Source==SanctuaryAttackSource.Opportunity) {
                continuation=new Command(c.Id,c.Actor,s.Revision,CommandKind.RespondOpportunityAttack,pending.OpportunityId,
                    combat:new CombatRequest(source.Combat.TurnId));
            } else if(pending.Source!=SanctuaryAttackSource.RegularMelee&&pending.Source!=SanctuaryAttackSource.RegularUnarmed)
                return "SanctuaryAttackSourceUnsupported";
            var save=s.SpellSaves.Single(x=>x.Id==pending.SaveId);
            if(!save.AttackerTurn.SameAs(CurrentCastingTurn(s,c.Actor)))return "SanctuarySourceIntervalExpired";
            if(continuation==null)return null;
            var candidate=s.Copy();FinishSanctuary(candidate,pending,c);
            return ResolveCore(candidate,continuation,assessTactical:true,sanctuaryChecked:true);
        }

        private string ResolveSanctuaryResponse(Snapshot s,Command c,bool assessOnly)
        {
            string failure=AssessSanctuaryResponse(s,c,out var continuation);
            if(failure!=null || assessOnly)return failure;
            var pending=PendingSanctuary(s);FinishSanctuary(s,pending,c);
            return continuation==null?null:ResolveCore(s,continuation,sanctuaryChecked:true);
        }

        private CommandQueryResult QuerySanctuaryCommand(Snapshot s,Command c)
        {
            string failure=ResolveCore(s.Copy(),c,assessTactical:true);
            bool reaction=c.Kind==CommandKind.RespondOpportunityAttack;
            return new CommandQueryResult(true,failure==null,failure??"Available",s.Revision,
                failure==null&&SanctuaryAttackCommand(c)?new[]{new CommandCost(reaction?"reaction":"action","",1)}:null);
        }
    }
}
#endif
