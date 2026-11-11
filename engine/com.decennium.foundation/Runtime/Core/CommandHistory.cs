using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Strict reconstruction of an existing receipt payload. This supplies no authority,
    /// source eligibility or state validation; callers still replay through their selected policy.</summary>
    public static class CommandHistory
    {
        public static Command Read(CommandReceipt receipt)
        {
            if (receipt == null || !Validation.ValidId(receipt.Id) || !Validation.ValidId(receipt.Principal)
                || receipt.Revision < 1 || string.IsNullOrEmpty(receipt.Fingerprint) || receipt.Fingerprint.Length > 512)
                throw new ArgumentException("Invalid command receipt.");
            var p = receipt.Fingerprint.Split('|');
            if (p.Length != 6 && p.Length != 8 && p.Length != 9 && p.Length != 10 && p.Length != 11 && p.Length != 12 && p.Length != 13 && p.Length != 14 && p.Length != 16) throw new ArgumentException("Invalid receipt fields.");
            int Int(string value) => int.TryParse(value, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out int n)
                ? n : throw new ArgumentException("Invalid receipt integer.");
            long Long(string value) => long.TryParse(value, NumberStyles.None, CultureInfo.InvariantCulture, out long n)
                ? n : throw new ArgumentException("Invalid receipt quantity.");
            var kind = (CommandKind)Int(p[0]);
            if (!Enum.IsDefined(typeof(CommandKind), kind) || !Validation.ValidId(p[1]) || p[2] != "" && !Validation.ValidId(p[2]))
                throw new ArgumentException("Invalid receipt identity or command kind.");
            InventoryRequest inventory = null; CombatRequest combat = null; CharacterAdvancementRequest advancement=null; RangedRequest ranged=null;
            SuppressionFireRequest suppression=null;
            DefensiveFormationRequest defensiveFormation=null;
            ExpeditionAssignmentRequest expeditionAssignment=null;
            HarvestSelectionRequest harvestSelection=null;
            MiningSelectionRequest miningSelection=null;
            ProspectingExposureRequest prospectingExposure=null;
            RouteMappingWorkRequest routeMappingWork=null;
            OverwatchRider rider=OverwatchRider.None;
            if(p.Length==8&&p[6]=="overwatch-rider-v1") {
                rider=(OverwatchRider)Int(p[7]);
                if(kind!=CommandKind.ResolveOverwatchRider||p[6]!="overwatch-rider-v1"||rider==OverwatchRider.None
                    ||!Enum.IsDefined(typeof(OverwatchRider),rider))throw new ArgumentException("Invalid Overwatch rider receipt.");
            }
            if(p.Length==8&&p[6]=="character-level-v2") {
                if(kind!=CommandKind.AdvanceCharacterLevel)throw new ArgumentException("Invalid advancement choice-list receipt.");
                string[] choices=p[7].Length==0?Array.Empty<string>():p[7].Split(',');
                advancement=new CharacterAdvancementRequest(choices);
            }
            if(p.Length==10&&p[6]=="character-level-v3") {
                if(kind!=CommandKind.AdvanceCharacterLevel)throw new ArgumentException("Invalid advancement operation receipt.");
                string[] choices=p[7].Length==0?Array.Empty<string>():p[7].Split(',');
                CharacterAbility[] increases=p[8].Length==0?Array.Empty<CharacterAbility>()
                    :p[8].Split(',').Select(value=>(CharacterAbility)Int(value)).ToArray();
                advancement=new CharacterAdvancementRequest(choices,increases,p[9]);
            }
            if(p.Length==9&&p[6]=="defensive-formation-v1") {
                if(kind!=CommandKind.ActivateDefensiveFormation)throw new ArgumentException("Defensive Formation payload has the wrong command kind.");
                string[] recipients=p[8].Length==0?Array.Empty<string>():p[8].Split(',');
                defensiveFormation=new DefensiveFormationRequest(p[7],recipients);
            }
            if(p.Length==9&&p[6]!="defensive-formation-v1"&&p[6]!="prospecting-exposure-v1") {
                if(kind!=CommandKind.AdvanceCharacterLevel||p[6]!="character-level-v1"||p[7]!=""&&!Validation.ValidId(p[7])||p[8]!=""&&!Validation.ValidId(p[8]))throw new ArgumentException("Invalid advancement receipt version or choices.");
                advancement=new CharacterAdvancementRequest(p[7],p[8]);
            }
            if (p.Length == 10 && p[6] == "inventory-v1") {
                var q = p[7].Split('/'); if (q.Length != 2) throw new ArgumentException("Invalid receipt fraction.");
                inventory = new InventoryRequest(new RuleQuantity(Long(q[0]), Long(q[1])), p[8], (HandlingKind)Int(p[9]));
            }
            if(p.Length==10&&p[6]=="expedition-assignment-v1") {
                if(kind!=CommandKind.AssignExpeditionWork)throw new ArgumentException("Expedition assignment payload has the wrong command kind.");
                expeditionAssignment=new ExpeditionAssignmentRequest((ExpeditionWorkProcedure)Int(p[7]),p[8],p[9]);
            }
            if(p.Length==16&&p[6]=="expedition-mining-assignment-v1") {
                if(kind!=CommandKind.AssignExpeditionWork||p[12]!="0"&&p[12]!="1")
                    throw new ArgumentException("Mining assignment payload has the wrong command kind or hurry flag.");
                string[] categories=p[13].Length==0?Array.Empty<string>():p[13].Split(',');
                var selection=new MiningSelectionRequest(p[10],categories,(MiningAbilityChoice)Int(p[11]),p[12]=="1",p[14],p[15]);
                expeditionAssignment=new ExpeditionAssignmentRequest((ExpeditionWorkProcedure)Int(p[7]),p[8],p[9],selection);
            }
            if(p.Length==10&&p[6]=="suppression-fire-v1") {
                if(kind!=CommandKind.SuppressionFire)throw new ArgumentException("Suppression Fire payload has the wrong command kind.");
                string[] targets=p[9].Length==0?Array.Empty<string>():p[9].Split(',');
                suppression=new SuppressionFireRequest(p[7],p[8],targets);
            }
            if (p.Length == 11 && p[6] == "ranged-v1") {
                if ((kind != CommandKind.AttackRepeatingCrossbow && kind != CommandKind.ReloadRepeatingCrossbow
                    &&kind!=CommandKind.WarningShot&&kind!=CommandKind.CoveringFire) || p[6] != "ranged-v1")
                    throw new ArgumentException("Unknown ranged receipt version or command.");
                ranged = new RangedRequest(p[7], p[8], p[9], Int(p[10]));
            }
            if (p.Length >= 12 && p[6] != "mining-selection-v1" && p[6] != "mining-selection-v2"
                && p[6] != "expedition-mining-assignment-v1") {
                if (p[6] != (p.Length == 12 ? "combat-v1" : "combat-v2") || p.Length == 13 && p[12] != "1"
                    || p[11] != "0" && p[11] != "1") throw new ArgumentException("Invalid combat receipt version or flag.");
                combat = new CombatRequest(p[7], p[8], Int(p[9]), (AttackKnockoutMode)Int(p[10]), p[11] == "1",
                    p.Length == 13 ? PressHitInstruction.KeepExisting : PressHitInstruction.ArmOrReplace);
            }
            if(p.Length==11&&p[6]=="harvest-selection-v1") {
                if(kind!=CommandKind.StartHarvest)throw new ArgumentException("Harvest selection payload has the wrong command kind.");
                string[] categories=p[8].Length==0?Array.Empty<string>():p[8].Split(',');
                harvestSelection=new HarvestSelectionRequest(p[7],categories,p[9],p[10]);
            }
            if(p.Length==13&&p[6]=="mining-selection-v1") {
                if(kind!=CommandKind.StartMining||p[9]!="0"&&p[9]!="1")throw new ArgumentException("Mining selection payload has the wrong command kind or hurry flag.");
                string[] categories=p[10].Length==0?Array.Empty<string>():p[10].Split(',');
                miningSelection=new MiningSelectionRequest(p[7],categories,(MiningAbilityChoice)Int(p[8]),p[9]=="1",p[11],p[12]);
            }
            if(p.Length==14&&p[6]=="mining-selection-v2") {
                if(kind!=CommandKind.StartMining||p[9]!="0"&&p[9]!="1"||!Validation.ValidId(p[13]))
                    throw new ArgumentException("Mining selection v2 payload has the wrong command kind, hurry flag, or assistant.");
                string[] categories=p[10].Length==0?Array.Empty<string>():p[10].Split(',');
                miningSelection=new MiningSelectionRequest(p[7],categories,(MiningAbilityChoice)Int(p[8]),p[9]=="1",p[11],p[12],p[13]);
            }
            if(p.Length==9&&p[6]=="prospecting-exposure-v1") {
                if(kind!=CommandKind.RecordProspectingExposure)throw new ArgumentException("Prospecting exposure payload has the wrong command kind.");
                prospectingExposure=new ProspectingExposureRequest(p[7],p[8]);
            }
            if(p.Length==8&&p[6]=="route-map-team-v1") {
                if(kind!=CommandKind.StartRouteMappingWork)throw new ArgumentException("Map Route team payload has the wrong command kind.");
                routeMappingWork=new RouteMappingWorkRequest(p[7].Length==0?Array.Empty<string>():p[7].Split(','));
            }
            var command = new Command(receipt.Id, p[1], receipt.Revision - 1, kind, p[2], Int(p[4]), Int(p[5]), inventory, combat,advancement,ranged,rider,suppression,defensiveFormation,expeditionAssignment,harvestSelection,miningSelection,prospectingExposure,routeMappingWork);
            // Includes expected revision and exact canonical numeric representation, versions and fields.
            if (!command.MatchesReceipt(receipt)) throw new ArgumentException("Noncanonical or inconsistent command receipt.");
            return command;
        }
    }
}
